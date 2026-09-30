"""D84: empirical height calibration of the frozen joint recognition algorithm.

Synthetic points only: increasing the synthetic precision does not lift the
candidate curve. Failures concern the LLL basis-row search, not all vectors.
"""
import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


jobs = module("calibration_jobs", "272_cm_frame_bounded_jobs.py")


def worker(args, path):
    from sage.all import GF, QQ, ZZ, Zmod, NumberField, PolynomialRing, identity_matrix, matrix
    rec = module("calibration_recognition", "132_cm_frame_denominator_recognition.py")
    U = PolynomialRing(ZZ, "t")
    f = U([2, 0, -16, 0, 20, 0, -8, 0, 1])
    F = NumberField(f.change_ring(QQ), "theta")
    roots = sorted(int(r) for r, m in f.change_ring(GF(31)).roots() if m == 1)
    initial = roots[args.root_index]
    root = rec.hensel_root(f, initial, args.digits)
    modulus, training = 31**args.digits, 31**args.train
    results = []
    for exponent in args.powers:
        started = time.monotonic()
        height = 10**exponent
        rng = random.Random(840000 + args.seed * 1000 + exponent)
        known = [[rng.randint(-height, height) for _ in range(8)] for _ in range(25)]
        known[0][0], known[0][1] = height, height - 1
        assert math.gcd(*(c for row in known for c in row)) == 1
        raw = [sum(row[j]*pow(root, j, modulus) for j in range(8)) % modulus for row in known]
        anchor = next(i for i, x in enumerate(raw) if x % 31)
        # An arbitrary common 31-adic unit makes the inputs projective data.
        scale = rng.randrange(1, modulus)
        while scale % 31 == 0:
            scale = rng.randrange(1, modulus)
        values = [(scale*x) % modulus for x in raw]
        Z = Zmod(training)
        others = [i for i in range(25) if i != anchor]
        powers = [Z(root)**j for j in range(8)]
        ratios = [Z(v)/Z(values[anchor]) for v in values]
        H = matrix(Z, 24, 200)
        for k, i in enumerate(others):
            for j in range(8):
                H[k, 8*i+j] = powers[j]
                H[k, 8*anchor+j] = -ratios[i]*powers[j]
        active = [8*i for i in others]
        assert H.matrix_from_columns(active) == identity_matrix(Z, 24)
        B = identity_matrix(ZZ, 200)
        for i in range(200):
            if i in active:
                B[i, i] = training
            else:
                for k, col in enumerate(active):
                    B[i, col] = -ZZ(H[k, i])
        assert B.change_ring(Z)*H.transpose() == 0
        reduced = B.LLL()
        assert reduced.change_ring(Z)*H.transpose() == 0
        assert abs(reduced.det()) == training**24
        exact = [F(row) for row in known]
        changed = list(values)
        changed[others[0]] = (changed[others[0]] + 31**args.train) % modulus
        candidates, survivors = [], []
        best_row, best_digits = None, -1
        changed_survivors = 0
        for index, sage_row in enumerate(reduced):
            row = [int(x) for x in sage_row]
            ev = [sum(row[8*i+j]*pow(root, j, modulus) for j in range(8)) % modulus for i in range(25)]
            if ev[anchor] % 31 == 0:
                continue
            defects = [(ev[i]*values[anchor]-ev[anchor]*values[i]) % modulus for i in others]
            matching = min(rec.valuation(x, args.digits) for x in defects)
            assert matching >= args.train
            info = {"row_index": index, "height": max(abs(x) for x in row), "matching_digits": matching}
            candidates.append(info)
            if matching > best_digits:
                best_row, best_digits = row, matching
            if matching == args.digits:
                p = [F(row[8*i:8*i+8]) for i in range(25)]
                assert all(p[i]*exact[anchor] == p[anchor]*exact[i] for i in range(25)), "False held-out survivor"
                survivors.append({**info, "row": row})
            if all((ev[i]*changed[anchor]-ev[anchor]*changed[i]) % modulus == 0 for i in others):
                changed_survivors += 1
        assert changed_survivors == 0
        result = {"exponent": exponent, "input_height": height, "known_coordinates": known,
                  "common_padic_scale": scale, "values": values, "anchor": anchor,
                  "eligible_rows": len(candidates), "survivor_count": len(survivors),
                  "recovered": bool(survivors), "exact_projective_equality_checked": bool(survivors),
                  "first_survivor": survivors[0] if survivors else None,
                  "best_row": best_row, "best_matching_digits": best_digits,
                  "corrupted_unused_digit_survivors": changed_survivors,
                  "candidates": candidates, "wall_seconds": time.monotonic()-started}
        results.append(result)
        print("CALIBRATION", args.digits, args.train, args.seed, initial, exponent,
              len(survivors), best_digits, round(result["wall_seconds"], 3), flush=True)
    record = {"status": "pass", "milestone": "D84", "synthetic_only": True,
              "precision_digits": args.digits, "training_digits": args.train,
              "validation_digits": args.digits-args.train, "seed": args.seed,
              "root_index": args.root_index, "root_mod31": initial, "root_mod_precision": root,
              "lattice_rank": 200, "congruence_count": 24, "results": results,
              "target_height_bound_claimed": False,
              "sources": [jobs.source(p) for p in (Path(__file__), Path(rec.__file__),
                    ROOT / "dembele/pari/259_cm_frame_cubic_adjoint_joint_recognition.py")]}
    path.write_text(json.dumps(record, indent=2)+"\n")
    print("PASS|275_RECOGNITION_CALIBRATION", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=64)
    parser.add_argument("--train", type=int, default=60)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--root-index", type=int, choices=range(8), default=0)
    parser.add_argument("--powers", type=int, nargs="+", default=[4, 6, 8, 9, 10, 11, 12, 14])
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    assert 1 < args.train < args.digits and min(args.powers) >= 1
    label = "_".join(map(str, args.powers))
    base = DATA / f"cm_frame_recognition_calibration_{args.digits}_{args.train}_{args.seed}_{args.root_index}_{label}"
    path, jpath = base.with_suffix(".json"), Path(str(base)+"_job.json")
    if args.worker:
        worker(args, path)
        return
    if path.exists() or jpath.exists():
        assert path.exists() and jpath.exists(), "Archive incomplete attempts before rerunning."
        report = json.loads(path.read_text())
        job = json.loads(jpath.read_text())
        assert report["status"] == job["status"] == "pass"
        for item in report["sources"] + job["sources"] + [job["log"]]:
            assert jobs.source(item["path"]) == item
        print("PASS|275_EXISTING_CALIBRATION", base.name)
        return
    command = [jobs.SAGE, "-python", str(Path(__file__)), "--worker", "--digits", str(args.digits),
               "--train", str(args.train), "--seed", str(args.seed), "--root-index", str(args.root_index),
               "--powers", *map(str, args.powers)]
    env = dict(os.environ, DOT_SAGE="/private/tmp/dembele_pointed_recognition_sage")
    job = jobs.run_job(command, base.with_suffix(".out"), 180, "PASS|275_RECOGNITION_CALIBRATION", env=env)
    job["sources"].append(jobs.source(Path(__file__)))
    jpath.write_text(json.dumps(job, indent=2)+"\n")
    assert job["status"] == "pass", job["status"]
    report = json.loads(path.read_text())
    report["sources"].append(jobs.source(jpath))
    path.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|275_BOUNDED_CALIBRATION", base.name, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
