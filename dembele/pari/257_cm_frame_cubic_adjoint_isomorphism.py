"""Certify the pointed special fibre is the D79 cover, preserving its D80 counts."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_isomorphism_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks = prior.checks


def main():
    roots = [DATA / "cm_frame_cubic_adjoint_1_check.json", DATA / "cm_frame_cubic_pointed_isomorphism.json"]
    for path in roots: checks.verify_records(json.loads(path.read_text()))
    script = ROOT / "dembele/magma/256_cm_frame_cubic_adjoint_isomorphism.m"
    base = DATA / "cm_frame_cubic_adjoint_isomorphism"
    job, jpath = prior.run(script, base, "PASS|256_CM_FRAME_CUBIC_ADJOINT_ISOMORPHISM",
        [Path(__file__), ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m"]+roots, "", False)
    output = Path(job["log"]["path"]).read_text()
    scalar = prior.helpers.field(output, "ADJOINT_ISOMORPHISM_SCALAR")
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), jpath]+roots],
              "isomorphism": "v_adjoint = delta*(r/g)*v_pointed", "delta_mod31": scalar,
              "evaluation_points": 2048, "maximum_pole_degree": 1200,
              "global_kummer_and_involution_identities_verified": True,
              "point_counts_inherited": {"F31": 68, "F961": 2818},
              "characteristic_zero_cubic_constructed": False, "arithmetic_identification_certified": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|257_CM_FRAME_CUBIC_ADJOINT_ISOMORPHISM", scalar, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
