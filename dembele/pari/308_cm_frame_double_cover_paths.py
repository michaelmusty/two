"""D87: sampled square-root continuation, with immutable polynomial caches.

This is a numerical character diagnostic, not a certified analytic comparison.
No differential bank is recomputed.  Path subdivisions, an alternative path,
and a second bank test sensitivity to numerical choices.
"""
import argparse
import ctypes as ct
import importlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import time

import mpmath as mp

from cm_acb import Backend, Vector, evaluate, check

base = importlib.import_module("306_cm_frame_double_cover_endpoints")
HERE, DATA = base.HERE, base.DATA


def build_library():
    import hashlib
    source_path = HERE/"307_cm_frame_double_cover_pullback.c"
    flags = shlex.split(subprocess.check_output(["pkg-config", "--cflags", "--libs", "flint"], text=True))
    version = subprocess.check_output(["pkg-config", "--modversion", "flint"], text=True).strip()
    compiler = shlex.split(os.environ.get("CC", "cc"))
    identity = source_path.read_bytes() + repr((flags, version, compiler)).encode()
    path = HERE/".build"/("cover_"+hashlib.sha256(identity).hexdigest()[:20]+".so")
    if not path.exists():
        fd, temporary = tempfile.mkstemp(prefix="cover_", suffix=".so", dir=path.parent)
        os.close(fd)
        try:
            subprocess.run([*compiler, "-std=c11", "-O3", "-Wall", "-Wextra", "-Werror",
                            "-fPIC", "-shared", str(source_path), "-o", temporary, *flags], check=True)
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)
    library = ct.CDLL(str(path))
    library.cover_quadrics.restype = ct.c_int
    library.cover_quadrics.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p,
                                       ct.POINTER(ct.c_long), ct.POINTER(ct.c_long), ct.c_long, ct.c_long]
    return library


def folded_points(radius):
    sides = base.side_points(radius)
    endpoints, merges = [], []
    for side in sides:
        if side["rotation"]:
            continue
        for key in ("v", "gv"):
            z = side[key]
            hits = [j for j, q in enumerate(endpoints) if abs(q-z) < mp.mpf("1e-40")]
            assert len(hits) <= 1
            if hits:
                j = hits[0]
                merges.append(abs(z-endpoints[j]))
            else:
                j = len(endpoints)
                endpoints.append(z)
            side[key+"_path"] = j
    return sides, endpoints, max(merges, default=mp.mpf(0))


def cache_paths(bank):
    return DATA/f"cm_frame_double_cover_polynomials_{bank}_d87.acb", DATA/f"cm_frame_double_cover_polynomials_{bank}_d87.json"


def make_cache(bank):
    started = time.monotonic()
    cache, receipt = cache_paths(bank)
    assert not cache.exists() and not receipt.exists(), "preserve earlier cache builds"
    pullback = base.Pullback(bank)
    change = pullback.backend.vector(pullback.change.tolist())
    assert pullback.pairs == [[i, j] for i in range(16) for j in range(i, 16)]
    numerator = (ct.c_long*136)(*pullback.numerator)
    denominator = (ct.c_long*136)(*pullback.denominator)
    polynomial = Vector(pullback.backend, 2*pullback.bank.rows-1, 2)
    library = build_library()
    check(library.cover_quadrics(polynomial.ptr, pullback.bank.ptr, change.ptr,
                                numerator, denominator, pullback.bank.rows, pullback.backend.bits))
    print(json.dumps({"stage": "full polynomial products formed", "seconds": time.monotonic()-started}), flush=True)
    sides, points, merge = folded_points(pullback.radius)
    # Independent route: evaluate H first and then substitute into the quadrics.
    # This tests full convolution, matrix ordering and the complete endpoint set.
    actual = evaluate(polynomial, pullback.backend.vector(points)).to_mpmath()
    expected = pullback.values(points)
    differences = [abs(actual[i, q]/value[key]-1)
                   for i, value in enumerate(expected) for q, key in enumerate(("n", "d"))]
    maximum = max(differences)
    assert maximum < mp.mpf("1e-42"), "convolution differs from independent substitution"
    polynomial.write(cache)
    result = {"status": "numerical polynomial cache checked", "bank": bank,
              "sources": pullback.sources()+[base.source(Path(__file__)),
                                            base.source(HERE/"307_cm_frame_double_cover_pullback.c")],
              "cache": base.source(cache), "rows": polynomial.rows,
              "columns": 2, "radius": base.decimal(pullback.radius),
              "origin": pullback.origin, "folded_endpoint_count": len(points),
              "maximum_merged_endpoint_displacement": base.decimal(merge),
              "full_convolution_substitution_relative_error_max": base.decimal(maximum),
              "independent_checked_endpoints": len(points),
              "wall_seconds": time.monotonic()-started}
    receipt.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("sources", "origin")}), flush=True)


def continue_root(values, anchor, stride):
    root = mp.sqrt(anchor)
    old_value = anchor
    maximum_jump = mp.mpf(0)
    for value in values[stride-1::stride]:
        maximum_jump = max(maximum_jump, abs(mp.arg(value/old_value)))
        new_root = mp.sqrt(value)
        if abs(new_root-root) > abs(-new_root-root):
            new_root = -new_root
        root, old_value = new_root, value
    return root, maximum_jump


def path_nodes(endpoint, steps, bend):
    """Hyperbolic radial spacing; optional angular arc with the same endpoints."""
    length = mp.atanh(abs(endpoint))
    direction = endpoint/abs(endpoint)
    return [mp.tanh(length*k/steps)*direction*mp.exp(1j*bend*mp.sin(mp.pi*k/steps))
            for k in range(1, steps+1)]


def run_paths(args):
    started = time.monotonic()
    cache, receipt_path = cache_paths(args.bank)
    receipt = json.loads(receipt_path.read_text())
    assert base.source(cache) == receipt["cache"]
    for record in receipt["sources"]:
        assert base.source(record["path"]) == record
    backend = Backend(digits=50)
    polynomials = backend.read(cache, receipt["rows"], 2)
    sides, endpoints, merge = folded_points(mp.mpf(receipt["radius"]))
    stop = min(len(endpoints), args.stop)
    assert 0 <= args.first < stop and args.steps >= 16 and args.steps % 4 == 0
    anchor = mp.mpc(*receipt["origin"]["R0_from_linear_term"])
    records = []
    for first in range(args.first, stop, 8):
        last = min(first+8, stop)
        paths = [path_nodes(endpoints[i], args.steps, mp.mpf(args.bend)) for i in range(first, last)]
        nodes = [z for path in paths for z in path]
        values = evaluate(polynomials, backend.vector(nodes)).to_mpmath()
        for offset, i in enumerate(range(first, last)):
            path = paths[offset]
            ratios = [values[offset*args.steps+k, 0]/values[offset*args.steps+k, 1]/z
                      for k, z in enumerate(path)]
            roots = [continue_root(ratios, anchor, stride) for stride in (4, 2, 1)]
            root, jump = roots[-1]
            agreement = max(abs(r/root-1) for r, _ in roots)
            records.append({"path_index": i, "endpoint": base.pair(endpoints[i]),
                            "sqrt_R_endpoint": base.pair(root),
                            "R_endpoint": base.pair(ratios[-1]),
                            "nested_meshes": [{"steps": args.steps//stride,
                                               "sqrt_R_endpoint": base.pair(r),
                                               "maximum_principal_argument_step": base.decimal(j)}
                                              for stride, (r, j) in zip((4, 2, 1), roots)],
                            "mesh_agreement_error": base.decimal(agreement),
                            "finest_argument_step_max": base.decimal(jump),
                            "sample_R_absolute_min": base.decimal(min(map(abs, ratios))),
                            "sample_R_absolute_max": base.decimal(max(map(abs, ratios)))})
        print(json.dumps({"completed_paths": len(records), "total": stop-args.first,
                          "seconds": time.monotonic()-started}), flush=True)
    report = {"status": "sampled continuation; not a rigorous path certificate", "bank": args.bank,
              "sources": [base.source(Path(__file__)), base.source(receipt_path), base.source(cache)],
              "first": args.first, "stop": stop, "steps": args.steps, "bend_radians": args.bend,
              "paths": records, "wall_seconds": time.monotonic()-started}
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|308_SAMPLED_PATHS", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", choices=["current", "previous"], required=True)
    parser.add_argument("--build-cache", action="store_true")
    parser.add_argument("--first", type=int, default=0)
    parser.add_argument("--stop", type=int, default=273)
    parser.add_argument("--steps", type=int, default=128)
    parser.add_argument("--bend", default="0")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    mp.mp.dps = 70
    if args.build_cache:
        make_cache(args.bank)
    else:
        if not args.output or args.output.exists():
            parser.error("a new output path is required")
        run_paths(args)


if __name__ == "__main__":
    main()
