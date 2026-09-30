"""Collect normalized cubic fibre counts over F31 and F31^2."""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("point_data_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
helpers = importlib.util.module_from_spec(spec); spec.loader.exec_module(helpers)
checks = helpers.checks


def main():
    counts = []; sources = [Path(__file__), ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py",
                           DATA / "cm_frame_cubic_check.json", DATA / "cm_frame_curve_verification.json"]
    artifacts = []
    for degree, stem in ((1, "cm_frame_cubic_point_count_F31"), (2, "cm_frame_cubic_point_count_F31_squared")):
        path = DATA / f"{stem}_job.json"
        job = checks.read_job(path, "PASS|180_CM_FRAME_CUBIC_POINT_COUNT")
        output = re.sub(r'^Loading .*\n', '', Path(job["log"]["path"]).read_text(), flags=re.M)
        names = ("extension_degree", "base_points", "cubic_fiber_counts", "fiber_count_distribution",
                 "exceptional_fibers", "cubic_point_count", "hecke_expected_point_count")
        row = {name: helpers.field(output, name.upper()) for name in names}
        assert row["extension_degree"] == degree
        n = 50 if degree == 1 else 1400
        assert len(row["base_points"]) == n and len(set(map(tuple, row["base_points"]))) == n
        assert all(len(p) == 16 and all(0 <= c < 31**degree for c in p) for p in row["base_points"])
        fibers = row["cubic_fiber_counts"]
        assert len(fibers) == n and [p[0] for p in fibers] == list(range(1, n+1))
        assert all(len(p) == 5 and p[1] in range(4) and p[2] in range(4) for p in fibers)
        assert [sum(p[2] == j for p in fibers) for j in range(4)] == row["fiber_count_distribution"]
        assert sum(p[2] for p in fibers) == row["cubic_point_count"]
        assert sum(p[1] in (2, 3) for p in fibers) == row["exceptional_fibers"]
        row["hecke_count_match"] = row["cubic_point_count"] == row["hecke_expected_point_count"]
        mpath = DATA / f"{stem}_input.m"
        bindings = {"extension_degree": degree, "base_points": row["base_points"],
                    "fiber_counts": fibers, "expected_total": row["cubic_point_count"]}
        mpath.write_text("// D80 saved fibres, field elements encoded c0+31*c1.\n"+
                        "\n".join(f"point_count_{key} := {helpers.magma(value)};" for key, value in bindings.items())+"\n")
        sources.append(path); artifacts.append(checks.source(mpath)); counts.append(row)
    report = {"status": "pass", "milestone": "D80", "date": "2026-09-22",
              "sources": [checks.source(p) for p in sources], "magma_inputs": artifacts,
              "field_modulus": [3, 29, 1], "point_counts": counts,
              "independent_fiber_verification_completed": False,
              "arithmetic_identification_certified": False,
              "full_Euler_factor_computed": False, "characteristic_zero_cubic_constructed": False}
    checks.verify_records(report)
    (DATA / "cm_frame_cubic_point_counts.json").write_text(json.dumps(report, indent=2)+"\n")
    print("CUBIC_POINT_COUNTS", [r["cubic_point_count"] for r in counts],
          "HECKE_EXPECTED", [r["hecke_expected_point_count"] for r in counts])
    print("PASS|181_CM_FRAME_CUBIC_POINT_DATA")


if __name__ == "__main__":
    main()
