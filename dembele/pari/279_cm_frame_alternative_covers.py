"""D84: construct and independently count covers from certified alternative thirds.

Frozen D79/D80 sources are specialized only at their input filenames. Base
point enumeration is reused from the independently certified complete lists.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


prior = module("alternative_cover_prior", "277_cm_frame_rational_three_torsion.py")
jobs, helpers, checks = prior.jobs, prior.helpers, prior.checks


def immutable_write(path, content):
    if path.exists():
        assert path.read_text() == content, f"Existing content changed: {path}"
    else:
        path.write_text(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ambiguity", default="cm_frame_third_ambiguity_0_2.json")
    parser.add_argument("--case", type=int, required=True)
    args = parser.parse_args()
    source = DATA / args.ambiguity
    record = json.loads(source.read_text()); checks.verify_records(record)
    assert record["status"] == "pass" and 0 <= args.case < len(record["third_coordinates"])
    label = source.stem.removeprefix("cm_frame_third_ambiguity_") + f"_{args.case}"
    base = DATA / f"cm_frame_alternative_cover_{label}"
    report_path = base.with_suffix(".json")
    if report_path.exists():
        result = json.loads(report_path.read_text()); checks.verify_records(result)
        assert result["status"] == "pass"
        print("PASS|279_EXISTING_ALTERNATIVE_COVER", label)
        return
    # Bind an immutable snapshot of this executed orchestration source.
    driver = Path(__file__)
    snapshot = DATA / ("d84_alternative_driver_" + jobs.source(driver)["sha256"][:16] + ".py")
    immutable_write(snapshot, driver.read_text())
    common = [source, snapshot, ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m"]
    for name in ("cm_frame_cover_makdisi.m", "cm_frame_cover_sections.m", "cm_frame_cover_third_check_input.m",
                 "cm_frame_B3_fiber.m", "cm_frame_B3_fiber_structure.m", "cm_frame_B3_rational_model.m",
                 "cm_frame_curve_candidate.m", "cm_frame_marks.m"):
        common.append(DATA / name)
    input_path = Path(str(base)+"_third.m")
    coordinates = record["third_coordinates"][args.case]
    immutable_write(input_path, 'load "dembele/data/computed/cm_frame_cover_third_check_input.m";\n' +
        f"third_check_candidate_rows := EncRows(Dec({helpers.magma(coordinates)},k)*V2);\n")

    def specialize(original_name, stage, replacements, skip_enumeration=False):
        original = ROOT / "dembele/magma" / original_name
        content = original.read_text()
        for old, new in replacements:
            assert content.count(old) == 1, (original_name, old)
            content = content.replace(old, new)
        if skip_enumeration:
            start = content.index("pointset:={}; seen:={k|}; fibers:=0;")
            end = content.index("// A certified unit Jacobian minor", start)
            replacement = """// D84: reuse D80's complete, independently certified base point list.
points:=[[extension_degree eq 1 select k!c else k!(c mod 31)+k.1*(c div 31):c in row]:row in point_count_base_points];
assert #points eq (extension_degree eq 1 select 50 else 1400);
assert #Seqset([Eltseq(C_candidate!p):p in points]) eq #points;
assert &and[Evaluate(z,p) eq 0:z in polys,p in points];

"""
            content = content[:start]+replacement+content[end:]
        generated = Path(str(base)+f"_{stage}.m")
        immutable_write(generated, "// D84 specialization of " + str(original.relative_to(ROOT)) +
            "; SHA256 " + jobs.source(original)["sha256"] + "\n" + content)
        return generated, original

    def run(generated, original, stage, marker, extra=(), prefix=""):
        stage_base = Path(str(base)+"_"+stage)
        jpath = Path(str(stage_base)+"_job.json")
        if jpath.exists():
            return checks.read_job(jpath, marker), jpath
        runfile = Path(str(stage_base)+"_run.m")
        immutable_write(runfile, prefix+f"load {json.dumps(str(generated))};\n")
        job = jobs.run_job(jobs.prior.magma_command(runfile), stage_base.with_suffix(".out"), 180, marker)
        job["sources"] += [checks.source(p) for p in (generated, original, runfile, *common, *extra)]
        jpath.write_text(json.dumps(job, indent=2)+"\n")
        assert job["status"] == "pass", (stage, job["status"])
        print("ALTERNATIVE_STAGE", label, stage, round(job["wall_seconds"], 3), flush=True)
        return job, jpath

    third_replace = [('load "dembele/data/computed/cm_frame_cover_third_check_input.m";',
                      f'load {json.dumps(str(input_path))};')]
    generated, original = specialize("176_cm_frame_kummer_function.m", "construct", third_replace)
    construction, cjob = run(generated, original, "construct", "PASS|176_CM_FRAME_KUMMER_FUNCTION", [input_path])
    output = re.sub(r'^Loading .*\n', '', Path(construction["log"]["path"]).read_text(), flags=re.M)
    names = ("kummer_evaluation_indices", "kummer_product4_pairs", "kummer_third_coordinates",
             "kummer_descended_divisor_coordinates", "kummer_moving_coefficients", "kummer_q_coefficients",
             "kummer_u_coefficients", "kummer_f_coefficients", "kummer_norm_scalar", "cubic_quartic_monomials",
             "cubic_decic_monomials", "cubic_a_coefficients", "cubic_denominator_coefficients",
             "cubic_trace_numerator_coefficients")
    data = {name: helpers.field(output, name.upper()) for name in names}
    mpath = Path(str(base)+"_data.m")
    immutable_write(mpath, "// D84 alternative cubic and function witnesses.\n" +
        "\n".join(f"{name} := {helpers.magma(value)};" for name, value in data.items())+"\n")
    cubic_replace = [('load "dembele/data/computed/cm_frame_cubic.m";', f'load {json.dumps(str(mpath))};')]
    generated, original = specialize("178_cm_frame_cubic_check.m", "verify", third_replace+cubic_replace)
    verification, vjob = run(generated, original, "verify", "PASS|178_CM_FRAME_CUBIC_CHECK", [input_path, mpath, cjob])
    counts, count_jobs = [], []
    for degree in (1, 2):
        field_label = "F31" if degree == 1 else "F31_squared"
        saved = DATA / ("cm_frame_cubic_point_count_"+field_label+"_input.m")
        assert saved.exists(), saved
        generated, original = specialize("180_cm_frame_cubic_point_count.m", f"count_{degree}", cubic_replace, True)
        prefix = f"extension_degree := {degree};\nload {json.dumps(str(saved))};\n"
        job, count_job = run(generated, original, f"count_{degree}", "PASS|180_CM_FRAME_CUBIC_POINT_COUNT",
            [mpath, vjob, saved, DATA / "cm_frame_cubic_point_check.json", DATA / "levelraise_p2k_charpolys.m"], prefix)
        text = re.sub(r'^Loading .*\n', '', Path(job["log"]["path"]).read_text(), flags=re.M)
        field = lambda name: helpers.field(text, name)
        points, fibers, total = field("BASE_POINTS"), field("CUBIC_FIBER_COUNTS"), field("CUBIC_POINT_COUNT")
        new_input = Path(str(base)+f"_count_{degree}_input.m")
        definitions = {"point_count_extension_degree": degree, "point_count_base_points": points,
                       "point_count_fiber_counts": fibers, "point_count_expected_total": total}
        immutable_write(new_input, "\n".join(f"{key} := {helpers.magma(value)};" for key, value in definitions.items())+"\n")
        generated, original = specialize("182_cm_frame_cubic_point_check.m", f"count_check_{degree}", cubic_replace)
        prefix = f"extension_degree := {degree};\nload {json.dumps(str(new_input))};\n"
        check, check_job = run(generated, original, f"count_check_{degree}", "PASS|182_CM_FRAME_CUBIC_POINT_CHECK",
                              [mpath, new_input, count_job], prefix)
        counts.append({"extension_degree": degree, "point_count": total,
                       "Hecke_expected": field("HECKE_EXPECTED_POINT_COUNT"),
                       "fiber_distribution": field("FIBER_COUNT_DISTRIBUTION"),
                       "independently_verified": True})
        count_jobs.extend((count_job, check_job))
    result = {"status": "pass", "milestone": "D84", "case": args.case,
              "third_label": record["third_labels"][args.case], "counts": counts,
              "matches_both_Hecke_counts": all(c["point_count"] == c["Hecke_expected"] for c in counts),
              "genus": 64, "cover_independently_verified": True,
              "arithmetic_identification_certified": False, "complete_third_enumeration": False,
              "sources": [checks.source(p) for p in (snapshot, source, cjob, vjob, mpath, *count_jobs)]}
    report_path.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|279_ALTERNATIVE_COVER", label, [c["point_count"] for c in counts], flush=True)


if __name__ == "__main__":
    main()
