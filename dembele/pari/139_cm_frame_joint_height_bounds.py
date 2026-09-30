"""D75: exact coefficient-box exclusions for the joint F lattices.

For a row basis R of the full congruence lattice, D=m*R^-1 is integral.
If S is the largest column l1 norm of D, H*S<m forces every lattice
vector with coordinates bounded by H to be zero. This is an exact
bound in the specified section and field power bases, not non-descent.
"""
import importlib.util
import json
from pathlib import Path
import time

from sage.all import QQ, ZZ, identity_matrix, matrix

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


checks = module("height_checks", ROOT / "dembele/pari/129_cm_frame_normalization_check.py")


def bound(trial, m):
    started = time.monotonic()
    R = matrix(ZZ, trial["reduced_rows"])
    inverse_scaled = (m*R.change_ring(QQ).inverse()).change_ring(ZZ)
    assert R*inverse_scaled == m*identity_matrix(ZZ, 136)
    column_norms = [sum(abs(x) for x in col) for col in inverse_scaled.columns()]
    largest = max(column_norms)
    H = (m-1)//largest
    assert H*largest < m <= (H+1)*largest
    print("EXACT_BOX_EXCLUSION", trial["label"], trial["root_mod31"], int(H),
          "SECONDS", round(time.monotonic()-started, 3), flush=True)
    return {"label": trial["label"], "root_mod31": trial["root_mod31"],
            "scaled_inverse_integral": True, "exact_inverse_identity_checked": True,
            "maximum_inverse_column_l1_norm": str(largest),
            "coefficient_box_excluded_through": int(H),
            "wall_seconds": time.monotonic()-started}


def main():
    started = time.monotonic()
    input_path = DATA / "cm_frame_joint_field_recognition.json"
    job_path = DATA / "cm_frame_joint_field_recognition_job.json"
    checks.read_job(job_path, "PASS|138_CM_FRAME_JOINT_FIELD_RECOGNITION")
    data = json.loads(input_path.read_text())
    checks.verify_records(data)
    assert data["status"] == "pass"
    m = 31**data["training_digits"]
    control = bound(data["control"], m)
    known_height = max(abs(x) for row in data["control"]["exact_control_coefficients"] for x in row)
    assert control["coefficient_box_excluded_through"] < known_height
    results = [bound(trial, m) for trial in data["denominator_trials"]]
    report = {"status": "pass", "milestone": "D75", "date": "2026-09-18",
              "sources": [checks.source(p) for p in (__file__, input_path, job_path,
                          ROOT / "dembele/pari/129_cm_frame_normalization_check.py")],
              "training_digits": data["training_digits"], "field_degree": 8,
              "section_space_dimension": 17, "control": control, "denominator_bounds": results,
              "uniform_coefficient_box_excluded_through": min(r["coefficient_box_excluded_through"] for r in results),
              "basis_dependent": True, "nonmembership_in_F_proved": False,
              "proof": "For v=zR, z=vD/m is integral; ||v||_infinity<=H and H*S<m imply every |z_j|<1.",
              "wall_seconds": time.monotonic()-started}
    (DATA / "cm_frame_joint_height_bounds.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|139_CM_FRAME_JOINT_HEIGHT_BOUNDS", report["uniform_coefficient_box_excluded_through"],
          round(report["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()
