"""Collect the D78 Makdisi spaces and export them to the pinned LiftTors API."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


helpers = module("makdisi_data_helpers", ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")
checks = helpers.checks


def main():
    job_path = DATA / "cm_frame_cover_makdisi_job.json"
    job = checks.read_job(job_path, "PASS|166_CM_FRAME_COVER_MAKDISI")
    output = Path(job["log"]["path"]).read_text()
    names = ("auxiliary_indices", "evaluation_indices", "evaluation_frobenius",
             "evaluation_involution", "product2_pairs", "product3_pairs",
             "plus_coefficient_rows", "minus_coefficient_rows", "v1_evaluations",
             "v2_evaluations", "v3_evaluations", "plus_evaluations", "minus_evaluations")
    data = {name: helpers.field(output, name.upper()) for name in names}
    assert len(data["auxiliary_indices"]) == 111 and len(data["evaluation_indices"]) == 640
    assert not set(data["auxiliary_indices"]) & set(data["evaluation_indices"])
    assert len(data["product2_pairs"]) == 201 and len(data["product3_pairs"]) == 321
    for key, dim in (("v1_evaluations", 81), ("v2_evaluations", 201),
                     ("v3_evaluations", 321), ("plus_evaluations", 81), ("minus_evaluations", 81)):
        assert len(data[key]) == 640 and all(len(row) == dim for row in data[key])
        assert all(0 <= x < 31**2 for row in data[key] for x in row)
    spath = DATA / "cm_frame_cover_sections.json"
    section = json.loads(spath.read_text())
    checks.verify_records(section)
    modulus = section["data"]["evaluation_field_modulus"]
    data["field_modulus"] = modulus
    mpath = DATA / "cm_frame_cover_makdisi.m"
    mpath.write_text("// D78: GF(31^2) elements encoded as c0+31*c1.\n"+
                     "\n".join(f"makdisi_{key} := {helpers.magma(value)};"
                               for key, value in data.items())+"\n")
    gp = [r"\\ D78 exact arithmetic input; polynomial representatives for the pinned C API.",
          "cover_T="+"+".join(f"{c}*t^{i}" for i, c in enumerate(modulus) if c)+";",
          "cover_decode(c)=(c%31)+(c\\31)*t;"]
    for key in ("v1_evaluations", "v2_evaluations", "v3_evaluations", "plus_evaluations", "minus_evaluations"):
        name = "cover_"+key
        rows = data[key]
        gp.append(name+"=apply(cover_decode,["+";".join(",".join(map(str, row)) for row in rows)+"]);")
    for key in ("evaluation_frobenius", "evaluation_involution"):
        gp.append("cover_"+key+"=Vecsmall("+str(data[key])+");")
    gpath = DATA / "cm_frame_cover_makdisi.gp"
    gpath.write_text("\n".join(gp)+"\n")
    report = {"status": "pass", "milestone": "D78", "date": "2026-09-21",
              "sources": [checks.source(p) for p in (__file__, job_path, spath,
                          ROOT / "dembele/pari/158_cm_frame_B3_fiber_data.py")],
              "magma_artifact": checks.source(mpath), "gp_artifact": checks.source(gpath),
              "genus": 40, "base_divisor_degree": 120, "evaluation_count": 640,
              "section_dimensions": [81, 201, 321], "branch_representative_dimension": 81,
              "branch_representatives": "D+ + A - D0 and D- + A - D0, deg(A)=111",
              "data": data, "class_division_computed": False, "cyclic_cubic_constructed": False}
    (DATA / "cm_frame_cover_makdisi.json").write_text(json.dumps(report, indent=2)+"\n")
    print("MAKDISI_DIMENSIONS [81,201,321] EVALUATION_POINTS 640 BRANCH_REPRESENTATIVES 81")
    print("PASS|167_CM_FRAME_COVER_MAKDISI_DATA")


if __name__ == "__main__":
    main()
