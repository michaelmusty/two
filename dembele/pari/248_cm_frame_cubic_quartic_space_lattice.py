"""Search for a small rational basis of the quartic vanishing space.

Only the training jet matrix enters LLL. Separate higher precision checks
every candidate. Passing this pilot is not yet an exact Q certificate.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


prior = module("quartic_lattice_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
checks = prior.checks


def worker(train, valid):
    from sage.all import GF, ZZ, Zmod, identity_matrix, matrix
    paths = [DATA / f"cm_frame_cubic_quartic_space_{n}.json" for n in (train, valid)]
    records = [json.loads(path.read_text()) for path in paths]
    for record in records: checks.verify_records(record)
    modulus = 31**train
    J = matrix(Zmod(modulus), records[0]["data"]["quartic_jets"])
    V = matrix(Zmod(31**valid), records[1]["data"]["quartic_jets"])
    assert V.change_ring(Zmod(modulus)) == J
    active = list(J.change_ring(GF(31)).transpose().pivots()); assert len(active) == 80
    free = [i for i in range(105) if i not in active]
    C = J*J.matrix_from_rows(active).inverse()
    assert C.matrix_from_rows(active) == identity_matrix(Zmod(modulus), 80)
    B = identity_matrix(ZZ, 105)
    for i in active: B[i, i] = modulus
    for i in free:
        for j, col in enumerate(active):
            value = -int(C[i, j]) % modulus
            B[i, col] = value if 2*value <= modulus else value-modulus
    assert B.change_ring(J.base_ring())*J == 0
    print("QUARTIC_LATTICE_READY", train, valid, "rank", 105, "kernel dimension", 25, flush=True)
    reduced = B.LLL()
    assert reduced.change_ring(J.base_ring())*J == 0
    # The congruence basis has determinant modulus^80; exact LLL preserves it.
    assert abs(reduced.det()) == modulus**80
    residuals = reduced.change_ring(V.base_ring())*V
    survivors = [i for i in range(105) if residuals.row(i).is_zero()]
    rows = [[int(x) for x in row] for row in reduced.rows()]
    heights = [max(abs(x) for x in row) for row in rows]
    rank = matrix(ZZ, [rows[i] for i in survivors]).rank() if survivors else 0
    assert rank <= 25
    report = {"status": "pass", "sources": [checks.source(p) for p in [Path(__file__)]+paths],
              "training_digits": train, "validation_digits": valid-train,
              "lattice_rank": 105, "constraint_rank": 80, "rational_space_dimension": 25,
              "determinant_verified": True, "candidate_rows": rows,
              "candidate_height_digits": [len(str(h)) for h in heights],
              "surviving_row_indices": survivors, "survivor_rank": int(rank),
              "exact_rational_basis_certified": False,
              "scope": "bounded LLL basis-row search, validated at unused precision"}
    (DATA / f"cm_frame_cubic_quartic_lattice_{train}_{valid}.json").write_text(json.dumps(report, indent=2)+"\n")
    print("QUARTIC_LATTICE_SURVIVORS", survivors, "rank", rank, "height digits", [len(str(heights[i])) for i in survivors], flush=True)
    print("PASS|248_CM_FRAME_CUBIC_QUARTIC_SPACE_LATTICE", train, valid, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=int, default=128)
    parser.add_argument("--valid", type=int, default=256)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args(); assert 32 < args.train < args.valid
    if args.worker: worker(args.train, args.valid); return
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    base = DATA / f"cm_frame_cubic_quartic_lattice_{args.train}_{args.valid}"
    job = prior.jobs.run_job([prior.jobs.SAGE, "-python", str(Path(__file__)), "--train", str(args.train), "--valid", str(args.valid), "--worker"],
        base.with_suffix(".out"), 180, "PASS|248_CM_FRAME_CUBIC_QUARTIC_SPACE_LATTICE", env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] = [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(base)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"quartic lattice: {job['status']}")
    report = json.loads(base.with_suffix(".json").read_text()); report["sources"].append(checks.source(jpath))
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|248_CM_FRAME_CUBIC_QUARTIC_SPACE_LATTICE_JOB", args.train, args.valid, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
