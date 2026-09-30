"""Joint projective F-recognition of A2 in its exact 25-dimensional Q-space."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


prior = module("adjoint_joint_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
checks = prior.checks


def worker(n, train, root_index):
    from sage.all import GF, QQ, ZZ, Zmod, NumberField, PolynomialRing, identity_matrix, matrix, vector
    rec = module("adjoint_joint_methods", ROOT / "dembele/pari/132_cm_frame_denominator_recognition.py")
    path = DATA / f"cm_frame_cubic_adjoint_{n}_recognition.json"
    source = json.loads(path.read_text()); checks.verify_records(source)
    basis_path = DATA / "cm_frame_cubic_adjoint_quadratic_space.json"
    basis = json.loads(basis_path.read_text()); checks.verify_records(basis)
    target = source["a_reduced_coordinates"]; assert len(target) == 25
    U = PolynomialRing(ZZ, "t"); f = U([2, 0, -16, 0, 20, 0, -8, 0, 1])
    F = NumberField(f.change_ring(QQ), "theta")
    roots = sorted(int(r) for r, m in f.change_ring(GF(31)).roots() if m == 1)
    initial = roots[root_index]; root = rec.hensel_root(f, initial, n)
    valid_modulus, train_modulus = 31**n, 31**train

    def candidate(row, values, anchor, index):
        evaluated = [sum(int(row[8*i+j])*pow(root, j, valid_modulus) for j in range(8)) % valid_modulus for i in range(25)]
        if evaluated[anchor] % 31 == 0: return None
        defects = [(evaluated[i]*values[anchor]-evaluated[anchor]*values[i]) % valid_modulus for i in range(25) if i != anchor]
        matching = min(rec.valuation(x, n) for x in defects); assert matching >= train
        return {"row_index": index, "height": max(abs(int(x)) for x in row),
                "matching_digits": matching, "validates_unused_digits": matching == n}

    def experiment(label, values, exact=None):
        Z = Zmod(train_modulus); anchor = next(i for i, x in enumerate(values) if x % 31)
        others = [i for i in range(25) if i != anchor]
        powers = [Z(root)**j for j in range(8)]
        ratios = [Z(v)/Z(values[anchor]) for v in values]
        H = matrix(Z, 24, 200)
        for k, i in enumerate(others):
            for j in range(8):
                H[k, 8*i+j] = powers[j]; H[k, 8*anchor+j] = -ratios[i]*powers[j]
        active = [8*i for i in others]
        assert H.matrix_from_columns(active) == identity_matrix(Z, 24)
        B = identity_matrix(ZZ, 200)
        for i in range(200):
            if i in active: B[i, i] = train_modulus
            else:
                for k, col in enumerate(active): B[i, col] = -ZZ(H[k, i])
        assert B.change_ring(Z)*H.transpose() == 0
        print("ADJOINT_JOINT_LATTICE_READY", label, initial, flush=True)
        reduced = B.LLL(); assert reduced.change_ring(Z)*H.transpose() == 0
        assert abs(reduced.det()) == train_modulus**24
        rows = [[int(x) for x in row] for row in reduced]
        candidates = [c for i, row in enumerate(rows) if (c := candidate(row, values, anchor, i)) is not None]
        survivors = [c for c in candidates if c["validates_unused_digits"]]
        points = [[F(rows[c["row_index"]][8*i:8*i+8]) for i in range(25)] for c in survivors]
        if exact is not None:
            assert points
            assert all(all(p[i]*exact[anchor] == p[anchor]*exact[i] for i in range(25)) for p in points)
            changed = list(values); j = others[0]; changed[j] = (changed[j]+31**train) % valid_modulus
            assert not any((c := candidate(row, changed, anchor, i)) and c["validates_unused_digits"] for i, row in enumerate(rows))
        consistent = all(all(p[i]*points[0][anchor] == p[anchor]*points[0][i] for i in range(25)) for p in points) if points else None
        result = {"label": label, "anchor": anchor, "lattice_rank": 200,
                  "congruence_count": 24, "determinant_verified": True,
                  "rows": rows, "candidates": candidates, "survivors": survivors,
                  "survivors_give_same_exact_F_point": consistent}
        if points and consistent:
            weights = [QQ(a)/b for a, b in basis["data"]["basis_leading_weights"]]
            scale = sum(points[0][i]*weights[i] for i in range(25)); assert scale != 0
            normalized = [3*x/scale for x in points[0]]
            def encoded(x):
                row = list(x); row += [QQ(0)]*(8-len(row))
                return [[int(a.numerator()), int(a.denominator())] for a in row]
            result["normalized_F_basis_coordinates"] = [encoded(x) for x in normalized]
        print("ADJOINT_JOINT_SURVIVORS", label, initial, len(survivors), flush=True)
        return result

    rng = random.Random(82259)
    known = [[rng.randint(-7, 7) for _ in range(8)] for _ in range(25)]
    values = [sum(row[j]*pow(root, j, valid_modulus) for j in range(8)) % valid_modulus for row in known]
    control = experiment("known_F_point", values, exact=[F(row) for row in known])
    result = experiment("adjoint_A2", target)
    report = {"status": "pass", "sources": [checks.source(p) for p in (Path(__file__), Path(rec.__file__), path, basis_path)],
              "precision_digits": n, "training_digits": train, "validation_digits": n-train,
              "root_mod31": initial, "root_mod_validation": root, "known_control": control,
              "unused_digit_error_rejected": True, "result": result,
              "exact_curve_equation_certified": False, "coefficient_field_excluded": False}
    base = DATA / f"cm_frame_cubic_adjoint_joint_{n}_{train}_{root_index}"
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|259_CM_FRAME_CUBIC_ADJOINT_JOINT_RECOGNITION", n, train, root_index, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=32)
    parser.add_argument("--train", type=int, default=24)
    parser.add_argument("--root-index", type=int, choices=range(8), default=0)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args(); assert 1 < args.train < args.digits
    if args.worker: worker(args.digits, args.train, args.root_index); return
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    base = DATA / f"cm_frame_cubic_adjoint_joint_{args.digits}_{args.train}_{args.root_index}"
    job = prior.jobs.run_job([prior.jobs.SAGE, "-python", str(Path(__file__)), "--digits", str(args.digits),
        "--train", str(args.train), "--root-index", str(args.root_index), "--worker"], base.with_suffix(".out"),
        180, "PASS|259_CM_FRAME_CUBIC_ADJOINT_JOINT_RECOGNITION", env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] = [checks.source(Path(__file__)), checks.source(ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")]
    jpath = Path(str(base)+"_job.json"); jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"joint adjoint recognition: {job['status']}")
    report = json.loads(base.with_suffix(".json").read_text()); report["sources"].append(checks.source(jpath))
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n"); checks.verify_records(report)
    print("PASS|259_CM_FRAME_CUBIC_ADJOINT_JOINT_RECOGNITION_JOB", args.root_index, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
