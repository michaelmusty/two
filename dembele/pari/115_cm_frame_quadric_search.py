"""D68: one bounded rational-quadric search in the CM frame.

Every searched integer vector vanishes EXACTLY at the known CM frame.
Remaining canonical relations are numerical, checked in both saved banks.
Passing these checks would give a candidate, not a certified target equation.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import mpmath as mp
from sage.all import QQ, ZZ, matrix, vector


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def worker(input_path, output_path):
    rows = matrix(ZZ, json.loads(Path(input_path).read_text()))
    started = time.monotonic()
    reduced = rows.LLL(delta=0.99, algorithm="fpLLL:wrapper")
    Path(output_path).write_text(json.dumps({
        "coefficient_vectors": [[int(c) for c in row[:136]] for row in reduced.rows()],
        "lll_seconds": time.monotonic()-started}))


def quotient(record):
    result = mp.matrix(45, 136)
    for i, p in enumerate(record["pivots"]):
        result[i, p] = 1
        for j, f in enumerate(record["free"]):
            result[i, f] = -mp.mpc(*record["pivot_coefficients"][i][j])
    return result


def residual(q, row):
    v = mp.matrix(list(map(int, row)))
    return mp.norm(q*v)/(mp.norm(q)*mp.norm(v))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame", type=Path, default=DATA/"cm_projective_frame.json")
    parser.add_argument("--scale-digits", type=int, default=18)
    parser.add_argument("--max-height", type=int, default=10000)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output", type=Path, default=DATA/"cm_frame_quadric_search.json")
    args = parser.parse_args()
    if not 1 <= args.scale_digits <= 25 or min(args.max_height, args.timeout) < 1:
        parser.error("invalid bounded search parameters")
    started = time.monotonic()
    mp.mp.dps = 80
    frame = module("quadric_cm_frame", "114_cm_projective_frame.py")
    saved = json.loads(args.frame.read_text())
    _, _, evaluation = frame.field_frame()
    integral = (evaluation.denominator()*evaluation).change_ring(ZZ)
    kernel = integral.right_kernel_matrix()
    assert kernel.dimensions() == (119, 136) and integral*kernel.transpose() == 0
    assert all(d == 1 for d in kernel.elementary_divisors())
    kernel = kernel.LLL(delta=0.99)
    assert integral*kernel.transpose() == 0
    equations = {name: data["equations"] for name, data in saved["banks"].items()}
    for record in equations.values():
        assert record["pivots"] == equations["current"]["pivots"]
        assert record["free"] == equations["current"]["free"]
    qs = {name: quotient(record) for name, record in equations.items()}
    q = qs["current"]
    constraints = q*mp.matrix([[int(c) for c in row] for row in kernel.rows()]).T
    row_norms = [mp.norm(q[i, :]) for i in range(45)]
    scale = mp.mpf(10)**args.scale_digits
    tail = matrix(ZZ, [[int(mp.nint(scale*component(constraints[j, i])/row_norms[j]))
                       for component in (mp.re, mp.im) for j in range(45)]
                      for i in range(119)])
    lattice = kernel.augment(tail)
    result = {"status": "bounded discovery only; no exact target equation certified",
              "script_source": frame.source(__file__), "frame_source": frame.source(args.frame),
              "helper_source": frame.source(frame.__file__),
              "exact_CM_constraint_rank": 17, "saturated_integer_kernel_rank": 119,
              "integer_kernel_saturation_checked": True,
              "lattice_shape": list(lattice.dimensions()), "scale_digits": args.scale_digits,
              "coefficient_height_cap": args.max_height,
              "tolerances": {"current": "1e-18", "other_radius": "1e-18", "previous": "1e-12"},
              "residual_definition": "norm(Q*c)/(norm(Q)*norm(c)); complex residual, all 45 constraints",
              "accepted_candidates": [], "best_vectors": []}
    with tempfile.TemporaryDirectory(prefix="dembele-d68-quadric-") as directory:
        input_path, output_path = Path(directory)/"input.json", Path(directory)/"output.json"
        input_path.write_text(json.dumps([[int(c) for c in row] for row in lattice.rows()]))
        try:
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker",
                                  str(input_path), str(output_path)], capture_output=True,
                                 text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            result["worker"] = {"status": "timeout", "timeout_seconds": args.timeout}
        else:
            if run.returncode:
                raise RuntimeError("LLL worker failed: "+run.stderr[-2000:])
            output = json.loads(output_path.read_text())
            result["worker"] = {"status": "complete", "lll_seconds": output["lll_seconds"]}
            scores = []
            for row in output["coefficient_vectors"]:
                assert any(row) and integral*vector(ZZ, row) == 0
                scores.append((residual(q, row), row))
            scores.sort(key=lambda item: item[0])
            for index, (_, row) in enumerate(scores):
                height = max(map(abs, row))
                errors = {name: residual(value, row) for name, value in qs.items()}
                accepted = height <= args.max_height and all(
                    errors[name] < mp.mpf(bound) for name, bound in result["tolerances"].items())
                record = {"height": height, "exact_CM_values_zero": True,
                          "residuals": {name: mp.nstr(value, 25) for name, value in errors.items()},
                          "coefficients": row}
                if index < 5:
                    result["best_vectors"].append(record)
                if accepted:
                    result["accepted_candidates"].append(record)
            result["vectors_checked"] = len(scores)
    result["limitations"] = [
        "The search does not exhaust coefficient vectors below the height cap.",
        "The CM point constraints are exact; derivative banks and tolerances are empirical.",
        "Exact vanishing at D alone does not identify a relation on C.",
        "Independent exact verification of a global target relation remains required."]
    result["wall_seconds"] = time.monotonic()-started
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(result["worker"], "accepted", len(result["accepted_candidates"]), flush=True)
    if result["best_vectors"]:
        best = result["best_vectors"][0]
        print("Best vector height", best["height"], "residuals", best["residuals"], flush=True)
    print("Saved", args.output, "in", result["wall_seconds"], "seconds", flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--worker":
        worker(sys.argv[2], sys.argv[3])
    else:
        main()
