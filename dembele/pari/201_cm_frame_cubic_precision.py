"""Lift the marked cubic with fixed algebraic gauges to 31^4, 31^8, ... .

Each Magma job is bounded separately; class multiplication is checkpointed.
Earlier D81 artifacts are read-only inputs. Use --stage for bounded resumption.
"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("precision_prior", ROOT / "dembele/pari/189_cm_frame_cubic_lift_third.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, jobs, checks = prior.helpers, prior.jobs, prior.checks
CORE = [ROOT / "dembele/magma/197_cm_frame_cubic_precision_arithmetic.m",
        ROOT / "dembele/magma/199_cm_frame_cubic_precision_model.m"]


def stem(n, suffix=""):
    return DATA / f"cm_frame_cubic_precision_{n}{suffix}"


def loadline(path):
    return f'load "{path.relative_to(ROOT)}";\n'


def binding(prefix, data):
    lines = []
    for key, value in data.items():
        if key == "odd_support_components":
            text = "[*"+", ".join("<"+", ".join(helpers.magma(x) for x in c)+">" for c in value)+"*]"
        else:
            text = helpers.magma(value)
        lines.append(f"{prefix}{key} := {text};")
    return "\n".join(lines)+"\n"


def run(script, base, marker, inputs, wrapper_text, rebuild):
    jpath = Path(str(base)+"_job.json")
    if jpath.exists() and not rebuild:
        return checks.read_job(jpath, marker), jpath
    wrapper = Path(str(base)+"_run.m")
    wrapper.write_text("SetQuitOnError(true);\n"+wrapper_text+loadline(script))
    job = jobs.run_job(jobs.magma_command(wrapper), base.with_suffix(".out"), 180, marker)
    job["sources"] = [checks.source(p) for p in [Path(__file__), script, wrapper,
        ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]+inputs]
    jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass":
        raise RuntimeError(f"{base.name}: {job['status']}")
    return job, jpath


def previous_sections(n):
    return DATA / "cm_frame_cubic_lift_sections" if n == 4 else stem(n//2, "_sections")


def previous_cubic(n):
    return DATA / "cm_frame_cubic_lift" if n == 4 else stem(n//2)


def sections(n, rebuild):
    prev = previous_sections(n); base = stem(n, "_sections")
    checks.verify_records(json.loads(prev.with_suffix(".json").read_text()))
    script = ROOT / "dembele/magma/198_cm_frame_cubic_precision_sections.m"
    job, jpath = run(script, base, "PASS|198_CM_FRAME_CUBIC_PRECISION_SECTIONS",
        [prev.with_suffix(".json"), DATA / "cm_frame_cubic_lift_check.json"],
        f"precision_digits := {n};\nprecision_previous_digits := {n//2};\n"+loadline(prev.with_suffix(".m")), rebuild)
    output = Path(job["log"]["path"]).read_text()
    names = ("modulus", "odd_section_rows", "odd_support_components", "point_indices",
             "point_coordinates", "branch_plus_values", "branch_minus_values")
    data = {}
    for key in names:
        raw = re.search(r"^LIFT_"+key.upper()+r"\|(.*?)(?=^[A-Z][A-Z_0-9]*\||\Z)", output, re.M | re.S).group(1)
        data[key] = ast.literal_eval(raw.replace("[*", "[").replace("*]", "]").replace("<", "[").replace(">", "]").strip())
    assert data["modulus"] == 31**n and len(data["point_coordinates"]) == 1135
    mpath = base.with_suffix(".m"); mpath.write_text(binding("cubic_lift_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), jpath, prev.with_suffix(".json"))],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": n,
              "modulus": 31**n, "previous_precision_digits": n//2, "compatible_reduction_verified": True}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PRECISION_SECTIONS_PASS", n, round(job["wall_seconds"], 3), flush=True)


def third(n, rebuild):
    section_base = stem(n, "_sections")
    checks.verify_records(json.loads(section_base.with_suffix(".json").read_text()))
    old = json.loads((DATA / "cm_frame_cover_third.json").read_text())
    N = 3*old["proposed_scalar"]+1
    scalar = (31**(n-1)*N-1)//3
    assert 3*scalar+1 == 31**(n-1)*N
    chain = prior.old.addflip_chain(scalar)
    saved_indices, saved_coordinates = [], []
    chunk_jobs = []; chunk_size = 20 if n <= 4 else 12
    script = ROOT / "dembele/magma/200_cm_frame_cubic_precision_third.m"
    for start in range(2, len(chain)+1, chunk_size):
        end = min(start+chunk_size-1, len(chain))
        keep = sorted({1, end} | {i for item in chain[end:] for i in item[1:] if 0 < i <= end})
        base = stem(n, f"_third_{end:03d}")
        inputs = {"chain": chain, "chain_start": start, "chain_end": end,
                  "saved_indices": saved_indices, "saved_coordinates": saved_coordinates, "keep_indices": keep}
        wrapper = f"precision_digits := {n};\n"+loadline(section_base.with_suffix(".m"))+binding("lift_", inputs)
        job, jpath = run(script, base, "PASS|200_CM_FRAME_CUBIC_PRECISION_THIRD",
            CORE+[section_base.with_suffix(".json"), DATA / "cm_frame_cover_third.json"]+chunk_jobs[-1:], wrapper, rebuild)
        output = Path(job["log"]["path"]).read_text()
        saved_indices = helpers.field(output, "CHECKPOINT_INDICES")
        saved_coordinates = helpers.field(output, "CHECKPOINT_COORDINATES")
        assert saved_indices == keep; chunk_jobs.append(jpath)
        print("PRECISION_SCALAR_CHUNK_PASS", n, start, end, round(job["wall_seconds"], 3), flush=True)
    assert "PASS|THIRD_RELATION_AND_SYMMETRIES_AT_HIGHER_PRECISION" in output
    data = {"coordinates": saved_coordinates[saved_indices.index(len(chain))],
            "delta_coordinates": saved_coordinates[saved_indices.index(1)]}
    base = stem(n, "_third"); mpath = base.with_suffix(".m")
    mpath.write_text(binding("precision_third_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), *chunk_jobs]],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": n,
              "modulus": 31**n, "scalar": scalar, "class_number_assumed": False,
              "addflip_steps": len(chain)-1, "three_division_verified": True,
              "frobenius_fixed": True, "antiinvariant": True}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")


def function(n, rebuild):
    section_base = stem(n, "_sections"); third_base = stem(n, "_third"); prev = previous_cubic(n)
    for p in (section_base.with_suffix(".json"), third_base.with_suffix(".json"), prev.with_suffix(".json")):
        checks.verify_records(json.loads(p.read_text()))
    data_prev = json.loads(prev.with_suffix(".json").read_text())["data"]
    names = ("descended_divisor_coordinates", "q_coefficients", "u_coefficients", "f_coefficients",
             "norm_scalar", "a_coefficients", "denominator_coefficients", "trace_numerator_coefficients")
    previous = {key: data_prev[key] for key in names}
    previous["modulus"] = 31**(n//2)
    wrapper = f"precision_digits := {n};\n"+loadline(section_base.with_suffix(".m"))
    wrapper += loadline(third_base.with_suffix(".m"))+binding("previous_cubic_", previous)
    script = ROOT / "dembele/magma/203_cm_frame_cubic_precision_function.m"
    job, jpath = run(script, stem(n), "PASS|203_CM_FRAME_CUBIC_PRECISION_FUNCTION",
        CORE+[ROOT / "dembele/magma/202_cm_frame_cubic_gauge_arithmetic.m",
              section_base.with_suffix(".json"), third_base.with_suffix(".json"),
              prev.with_suffix(".json"), DATA / "cm_frame_cubic_gauge.json"], wrapper, rebuild)
    output = Path(job["log"]["path"]).read_text()
    data = {key: helpers.field(output, "PRECISION_"+key.upper()) for key in names}
    for key in names:
        if key == "norm_scalar": assert data[key] % previous["modulus"] == previous[key]
        elif key == "descended_divisor_coordinates":
            assert [[x % previous["modulus"] for x in row] for row in data[key]] == previous[key]
        else: assert [x % previous["modulus"] for x in data[key]] == previous[key]
    mpath = stem(n).with_suffix(".m"); mpath.write_text(binding("precision_cubic_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in (Path(__file__), jpath, DATA / "cm_frame_cubic_gauge.json")],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": n,
              "modulus": 31**n, "persistent_gauge_verified": True,
              "previous_precision_digits": n//2, "coefficientwise_reduction_verified": True,
              "norm_verified": True, "characteristic_zero_cubic_constructed": False}
    stem(n).with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PRECISION_CUBIC_PASS", n, round(job["wall_seconds"], 3), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--stage", choices=("sections", "third", "function", "all"), default="all")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    checks.verify_records(json.loads((DATA / "cm_frame_cubic_gauge.json").read_text()))
    for name, action in (("sections", sections), ("third", third), ("function", function)):
        if args.stage in (name, "all"):
            action(args.digits, args.rebuild)
    print("PASS|201_CM_FRAME_CUBIC_PRECISION", args.digits, args.stage)


if __name__ == "__main__":
    main()
