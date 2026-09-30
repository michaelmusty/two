"""Bounded Q/F recognition pilot with half the digits reserved for validation.

No surviving finite-precision relation is treated as an exact certificate.
Failure of this small-height search is not a field-of-definition exclusion.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


prior = module("pointed_recognition_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
checks = prior.checks


def worker(n):
    from sage.all import GF, QQ, ZZ, Zmod, NumberField, PolynomialRing, matrix, vector
    rec = module("pointed_recognition_methods", ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")
    train, valid = n//2, n
    cubic = DATA / f"cm_frame_cubic_adjoint_{n}.json"
    root = DATA / f"cm_frame_cubic_pointed_{n}_check.json"
    for path in (cubic, root): checks.verify_records(json.loads(path.read_text()))
    data = json.loads(cubic.read_text())["data"]
    U = PolynomialRing(ZZ, "t"); f = U([2, 0, -16, 0, 20, 0, -8, 0, 1])
    F = NumberField(f.change_ring(QQ), "theta"); theta = F.gen()
    roots31 = sorted(int(x) for x, multiplicity in f.change_ring(GF(31)).roots() if multiplicity == 1)
    assert len(roots31) == 8
    roots = [rec.hensel_root(f, x, valid) for x in roots31]
    modulus = 31**valid
    rational_control = 3*pow(7, -1, modulus) % modulus
    qc = rec.rational_candidate(rational_control, train, valid)
    assert qc and qc["validates_unused_digits"]
    assert not rec.rational_candidate((rational_control+31**train) % modulus, train, valid)["validates_unused_digits"]
    fc = rec.field_candidates((roots[0]+1) % modulus, roots[0], train, valid)
    survivors = [c for c in fc if c["validates_unused_digits"]]
    assert survivors
    for candidate in survivors:
        row = list(map(int, candidate["coefficients_and_denominator"]))
        assert F(row[:8])/row[8] == theta+1
    changed = rec.field_candidates((roots[0]+1+31**train) % modulus, roots[0], train, valid)
    assert not any(c["validates_unused_digits"] for c in changed)
    basis_path = DATA / "cm_frame_cubic_adjoint_quadratic_space.json"
    basis_report = json.loads(basis_path.read_text()); checks.verify_records(basis_report)
    basis = basis_report["data"]; Z = Zmod(modulus)
    B = matrix(Z, basis["integer_basis_rows"]); piv = basis["unit_pivot_indices_zero_based"]
    target = vector(Z, data["a_quadratic_coefficients"])
    coordinates = vector(Z, [target[i] for i in piv])*B.matrix_from_columns(piv).inverse()
    assert coordinates*B == target
    weights = vector(Z, [Z(a)/Z(b) for a, b in basis["basis_leading_weights"]])
    assert coordinates*weights == 3
    data["a_reduced_coordinates"] = [int(x) for x in coordinates]
    model_check = DATA / f"cm_frame_cubic_adjoint_{n}_check.json"
    independent = model_check.exists()
    if independent: checks.verify_records(json.loads(model_check.read_text()))
    groups = []
    for key in ("a_quadratic_coefficients", "trace_quartic_coefficients", "a_reduced_coordinates"):
        values = data[key]; anchor = next(i for i, v in enumerate(values) if v % 31)
        inverse = pow(values[anchor], -1, modulus)
        groups.append((key, list(enumerate(values)), None))
        groups.append((key+"_projective", [(i, v*inverse % modulus) for i, v in enumerate(values) if i != anchor], anchor))
    results = []
    for label, values, anchor in groups:
        rational = [{"index_zero_based": i, "candidate": rec.rational_candidate(v, train, valid)} for i, v in values]
        rational_survivors = [r for r in rational if r["candidate"] and r["candidate"]["validates_unused_digits"]]
        # All rational entries, but only a fixed modest sample for the degree-eight LLL search.
        sample = values[:12]
        field = []
        for initial, lifted in zip(roots31, roots):
            rows = [{"index_zero_based": i, "candidates": rec.field_candidates(v, lifted, train, valid)} for i, v in sample]
            passing = [r["index_zero_based"] for r in rows if any(c["validates_unused_digits"] for c in r["candidates"])]
            field.append({"root_mod31": initial, "candidates": rows, "surviving_indices": passing})
        results.append({"label": label, "anchor_index_zero_based": anchor,
                        "rational_tested": len(values), "rational_survivors": rational_survivors,
                        "field_sample_size": len(sample), "field_roots": field})
        print("ADJOINT_RECOGNITION", n, label, "Q survivors", len(rational_survivors),
              "F sampled survivors", sum(len(r["surviving_indices"]) for r in field), flush=True)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), Path(rec.__file__), cubic, root, basis_path]+([model_check] if independent else [])],
              "precision_digits": n, "training_digits": train, "validation_digits": valid-train,
              "known_rational_control_passed": True, "known_field_control_passed": True,
              "first_unused_digit_corruptions_rejected": True, "results": results,
              "exact_equation_certified": False, "coefficient_field_excluded": False,
              "a_reduced_coordinates": data["a_reduced_coordinates"],
              "independent_final_precision_model_check": independent,
              "scope": "bounded small-height candidates; monomial and separate projective coordinates"}
    path = DATA / f"cm_frame_cubic_adjoint_{n}_recognition.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|232_CM_FRAME_CUBIC_ADJOINT_RECOGNITION", n, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(8, 16, 32, 64, 128), required=True)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.worker:
        worker(args.digits); return
    base = DATA / f"cm_frame_cubic_adjoint_{args.digits}_recognition"
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    env = dict(os.environ, DOT_SAGE=str(cache))
    job = prior.jobs.run_job([prior.jobs.SAGE, "-python", str(Path(__file__)), "--digits", str(args.digits), "--worker"],
        base.with_suffix(".out"), 180, "PASS|232_CM_FRAME_CUBIC_ADJOINT_RECOGNITION", env=env)
    job["sources"] = [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(base)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"recognition: {job['status']}")
    report = json.loads(base.with_suffix(".json").read_text())
    report["sources"].append(checks.source(jpath))
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|232_CM_FRAME_CUBIC_ADJOINT_RECOGNITION_JOB", args.digits, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
