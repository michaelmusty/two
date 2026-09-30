"""Collect D78's exact genus-40 section and point data, with source hashes."""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


helpers = module("section_data_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
checks = helpers.checks


def main():
    job_path = DATA / "cm_frame_cover_sections_job.json"
    job = checks.read_job(job_path, "PASS|164_CM_FRAME_COVER_SECTIONS")
    output = re.sub(r'^Loading .*\n', '', Path(job["log"]["path"]).read_text(), flags=re.M)
    names = ("section_dimensions", "even_monomial_exponents", "odd_monomial_exponents",
             "odd_section_rows", "branch_plus_section_values", "branch_minus_section_values",
             "evaluation_field_modulus", "good_point_count", "evaluation_point_coordinates",
             "frobenius_permutation", "involution_permutation")
    data = {name: helpers.field(output, name.upper()) for name in names}
    assert data["section_dimensions"] == [45, 36, 81]
    assert len(data["odd_section_rows"]) == 36
    assert all(len(row) == 75 for row in data["odd_section_rows"])
    count = data["good_point_count"]
    assert count > 751 and len(data["evaluation_point_coordinates"]) == count
    assert all(len(pt) == 17 and all(len(x) == 2 for x in pt)
               for pt in data["evaluation_point_coordinates"])
    for name in ("frobenius_permutation", "involution_permutation"):
        perm = data[name]
        assert sorted(perm) == list(range(1, count+1))
        assert all(perm[perm[i]-1] == i+1 for i in range(count))
    for name in ("branch_plus_section_values", "branch_minus_section_values"):
        assert len(data[name]) == 81 and all(len(row) == 9 for row in data[name])
    mpath = DATA / "cm_frame_cover_sections.m"
    mpath.write_text("// D78: exact genus-40 section and evaluation data over F31.\n"+
                     "\n".join(f"sections_{key} := {helpers.magma(value)};"
                               for key, value in data.items())+"\n")
    report = {"status": "pass", "milestone": "D78", "date": "2026-09-21",
              "sources": [checks.source(p) for p in (__file__, job_path,
                          ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")],
              "magma_artifact": checks.source(mpath), "data": data,
              "base_divisor": "D0=pi^*(2*div(X16)), linearly equivalent to pi^*(2K_C)",
              "base_divisor_degree": 120, "cover_genus": 40,
              "section_interpretation": "even quadrics and (w/(ell/X16))*odd cubics, divided by X16^2 and X16^3 respectively",
              "odd_cubic_vanishing_divisor_degree": 39,
              "class_division_computed": False, "cyclic_cubic_constructed": False}
    (DATA / "cm_frame_cover_sections.json").write_text(json.dumps(report, indent=2)+"\n")
    print("SECTION_DIMENSIONS", data["section_dimensions"], "GOOD_POINTS", count)
    print("PASS|165_CM_FRAME_COVER_SECTION_DATA")


if __name__ == "__main__":
    main()
