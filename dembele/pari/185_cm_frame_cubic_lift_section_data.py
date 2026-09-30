"""Collect genuine section, branch and point lifts modulo 31^2 (D81)."""
import ast
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("lift_section_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
helpers = importlib.util.module_from_spec(spec); spec.loader.exec_module(helpers)
checks = helpers.checks


def main():
    job_path = DATA / "cm_frame_cubic_lift_sections_job.json"
    job = checks.read_job(job_path, "PASS|184_CM_FRAME_CUBIC_LIFT_SECTIONS")
    output = Path(job["log"]["path"]).read_text()
    names = ("modulus", "odd_section_rows", "odd_support_components", "point_indices",
             "point_coordinates", "branch_plus_values", "branch_minus_values")
    data = {}
    for key in names:
        raw = re.search(r"^LIFT_"+key.upper()+r"\|(.*?)(?=^[A-Z][A-Z_0-9]*\||\Z)", output, re.M | re.S).group(1)
        raw = raw.replace("[*", "[").replace("*]", "]").replace("<", "[").replace(">", "]")
        data[key] = ast.literal_eval(raw.strip())
    assert data["modulus"] == 961
    assert len(data["odd_section_rows"]) == 36 and all(len(row) == 75 for row in data["odd_section_rows"])
    assert len(data["point_indices"]) == 1135 and len(data["point_coordinates"]) == 1135
    assert all(len(p) == 17 and all(len(x) == 2 and all(0 <= c < 961 for c in x) for x in p)
               for p in data["point_coordinates"])
    assert [sum(len(c[1])-1 for c in data["odd_support_components"] if c[0] == side) for side in (1, 2)] == [18, 21]
    for key in ("branch_plus_values", "branch_minus_values"):
        assert len(data[key]) == 81 and all(len(row) == 9 for row in data[key])
    path = DATA / "cm_frame_cubic_lift_sections.m"
    def binding(key, value):
        if key == "odd_support_components":
            value_text = "[*"+", ".join("<"+", ".join(helpers.magma(x) for x in c)+">" for c in value)+"*]"
        else:
            value_text = helpers.magma(value)
        return f"cubic_lift_{key} := {value_text};"
    path.write_text("// D81 genuine points/sections modulo 31^2. Entries use [c0,c1].\n"+
                   "\n".join(binding(key, value) for key, value in data.items())+"\n")
    report = {"status": "pass", "milestone": "D81", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), job_path,
                          ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")],
              "magma_artifact": checks.source(path), "data": data,
              "precision_digits": 2, "modulus": 961, "evaluation_field_polynomial": [3, 29, 1],
              "evaluation_rows": 1024, "auxiliary_rows": 111,
              "odd_support_degrees": [18, 21], "odd_section_rank": 36,
              "class_lift_computed": False, "cubic_lift_computed": False}
    (DATA / "cm_frame_cubic_lift_sections.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|185_CM_FRAME_CUBIC_LIFT_SECTION_DATA")


if __name__ == "__main__":
    main()
