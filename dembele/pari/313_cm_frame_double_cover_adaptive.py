"""D87: adaptive sampled continuation guided by logarithmic derivatives.

Endpoint derivative estimates guide refinement; they are not interval bounds.
All samples are retained for an independent phase-unwrapping audit.  Numerical
truncation/geometry errors and constant arithmetic twists remain unresolved.
"""
import argparse
import ctypes as ct
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import time

import mpmath as mp

shifted = importlib.import_module("310_cm_frame_double_cover_shifted")
prior, base = shifted.prior, shifted.base


def library():
    path = base.HERE/"312_cm_frame_double_cover_derivative.c"
    flags = shlex.split(subprocess.check_output(["pkg-config", "--cflags", "--libs", "flint"], text=True))
    version = subprocess.check_output(["pkg-config", "--modversion", "flint"], text=True).strip()
    compiler = shlex.split(os.environ.get("CC", "cc"))
    digest = hashlib.sha256(path.read_bytes()+repr((flags, version, compiler)).encode()).hexdigest()[:20]
    target = base.HERE/".build"/f"cover_derivative_{digest}.so"
    if not target.exists():
        fd, temporary = tempfile.mkstemp(prefix="cover_derivative_", suffix=".so", dir=target.parent)
        os.close(fd)
        try:
            subprocess.run([*compiler, "-std=c11", "-O3", "-Wall", "-Wextra", "-Werror",
                            "-fPIC", "-shared", str(path), "-o", temporary, *flags], check=True)
            os.replace(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
    lib = ct.CDLL(str(target))
    lib.cover_evaluate2.restype = ct.c_int
    lib.cover_evaluate2.argtypes = [ct.c_void_p]*3+[ct.c_long]*2
    return lib


def nodes(endpoint, t, bend):
    length = mp.atanh(abs(endpoint))
    a = mp.tanh(length*t)
    direction = endpoint/abs(endpoint)*mp.exp(1j*bend*mp.sin(mp.pi*t))
    return direction*a, direction*(length*(1-a*a)+1j*bend*mp.pi*mp.cos(mp.pi*t)*a)


class Continuation:
    def __init__(self, bank, bend):
        self.cache, self.receipt_path = prior.cache_paths(bank)
        self.receipt = json.loads(self.receipt_path.read_text())
        for record in [self.receipt["cache"], *self.receipt["sources"]]:
            assert base.source(record["path"]) == record
        self.backend = prior.Backend(digits=50)
        self.poly = self.backend.read(self.cache, self.receipt["rows"], 2)
        self.lib = library()
        self.bend = mp.mpf(bend)
        _, self.endpoints, _ = prior.folded_points(mp.mpf(self.receipt["radius"]))
        first = self.poly.to_mpmath(rows=3)
        self.r0 = first[1, 0]/first[0, 1]
        self.log_derivative0 = first[2, 0]/first[1, 0]-first[1, 1]/first[0, 1]

    def evaluate(self, points):
        native = self.backend.vector(points)
        result = prior.Vector(self.backend, len(points), 4)
        prior.check(self.lib.cover_evaluate2(result.ptr, self.poly.ptr, native.ptr,
                                           self.poly.rows, self.backend.bits))
        return result.to_mpmath()

    def check_derivative(self):
        points = [nodes(self.endpoints[i], mp.mpf(".613"), self.bend)[0] for i in (0, 8, 15, 275, 549)]
        values = self.evaluate(points)
        h = mp.mpf("1e-14")
        direct = prior.evaluate(self.poly, self.backend.vector([z for p in points for z in (p-h, p, p+h)])).to_mpmath()
        value_error = max(abs(values[i, q]/direct[3*i+1, q]-1) for i in range(5) for q in range(2))
        derivative_error = max(abs((direct[3*i+2, q]-direct[3*i, q])/(2*h*values[i, q+2])-1)
                               for i in range(5) for q in range(2))
        assert value_error < mp.mpf("1e-45") and derivative_error < mp.mpf("1e-12")
        return {"independent_value_error": base.decimal(value_error),
                "symmetric_difference_derivative_error": base.decimal(derivative_error),
                "difference_step": base.decimal(h)}

    def add_samples(self, samples, requests):
        locations = [nodes(self.endpoints[i], t, self.bend) for i, t in requests]
        values = self.evaluate([z for z, _ in locations])
        for row, ((i, t), (z, dz)) in enumerate(zip(requests, locations)):
            n, d, dn, dd = list(values[row, :])
            samples[i][t] = (n/d/z, (dn/n-dd/d-1/z)*dz)

    def refine(self, samples, tolerance):
        rounds = 0
        while True:
            requests = []
            for i, path in samples.items():
                ts = sorted(path)
                for a, b in zip(ts, ts[1:]):
                    ra, da = path[a]; rb, db = path[b]
                    estimate = (b-a)*max(abs(da), abs(db))
                    argument = abs(mp.arg(rb/ra))
                    log_size = abs(mp.log(abs(rb/ra)))
                    if max(estimate, argument, log_size) > tolerance:
                        requests.append((i, (a+b)/2))
            if not requests:
                return rounds
            assert rounds < 24 and all(len(p) < 12000 for p in samples.values()), "bounded refinement exhausted"
            for first in range(0, len(requests), 256):
                self.add_samples(samples, requests[first:first+256])
            rounds += 1

    def run(self, indices):
        samples = {i: {mp.mpf(0): (self.r0, self.log_derivative0*nodes(self.endpoints[i], 0, self.bend)[1])}
                   for i in indices}
        requests = [(i, mp.mpf(k)/32) for i in indices for k in range(1, 33)]
        self.add_samples(samples, requests)
        coarse_rounds = self.refine(samples, mp.mpf(".30"))
        coarse = {i: prior.continue_root([path[t][0] for t in sorted(path) if t], self.r0, 1)[0]
                  for i, path in samples.items()}
        fine_rounds = self.refine(samples, mp.mpf(".15"))
        records = []
        for i, path in samples.items():
            ts = sorted(path)
            root, argument = prior.continue_root([path[t][0] for t in ts if t], self.r0, 1)
            agreement = abs(root/coarse[i]-1)
            assert agreement < mp.mpf("1e-35"), "adaptive coarse/fine branches disagree"
            estimates = [(b-a)*max(abs(path[a][1]), abs(path[b][1])) for a,b in zip(ts,ts[1:])]
            sizes = [abs(mp.log(abs(path[b][0]/path[a][0]))) for a,b in zip(ts,ts[1:])]
            records.append({"path_index": i, "endpoint": base.pair(self.endpoints[i]),
                            "sqrt_R_endpoint": base.pair(root), "coarse_sqrt_R_endpoint": base.pair(coarse[i]),
                            "coarse_fine_agreement_error": base.decimal(agreement),
                            "maximum_principal_argument_step": base.decimal(argument),
                            "maximum_log_modulus_step": base.decimal(max(sizes)),
                            "maximum_endpoint_derivative_step_estimate": base.decimal(max(estimates)),
                            "coarse_refinement_rounds": coarse_rounds, "fine_refinement_rounds": fine_rounds,
                            "samples": [{"t": base.decimal(t), "R": base.pair(path[t][0]),
                                         "logarithmic_derivative_along_path": base.pair(path[t][1])} for t in ts]})
        return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", choices=["current", "previous"], required=True)
    parser.add_argument("--first", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--bend", default="0")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists() and 0 <= args.first < args.stop <= 550
    mp.mp.dps = 70
    started = time.monotonic()
    calc = Continuation(args.bank, args.bend)
    control = calc.check_derivative()
    results = []
    for first in range(args.first, args.stop, 4):
        results += calc.run(range(first, min(first+4, args.stop)))
        print(json.dumps({"completed_paths": len(results), "total": args.stop-args.first,
                          "sample_count": sum(len(x["samples"]) for x in results),
                          "seconds": time.monotonic()-started}), flush=True)
    report = {"status": "adaptive numerical continuation; not an interval certificate",
              "bank": args.bank, "first": args.first, "stop": args.stop, "bend_radians": args.bend,
              "sources": [base.source(Path(__file__)), base.source(base.HERE/"312_cm_frame_double_cover_derivative.c"),
                          base.source(calc.receipt_path), base.source(calc.cache)],
              "coarse_tolerance": "0.30", "fine_tolerance": "0.15",
              "derivative_control": control, "paths": results, "wall_seconds": time.monotonic()-started}
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|313_ADAPTIVE_PATHS", flush=True)


if __name__ == "__main__":
    main()
