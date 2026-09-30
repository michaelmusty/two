# D85 precision adapter; original SHA256 1c8322e21df8c560499929e9f376f0292488a40972a917bf56f92f7f6900c2c2
"""D85: independently verify adjoint geometry and functions in bounded jobs."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


build = module("adjoint128_checker_build", "253_cm_frame_cubic_adjoint_lift.py")
runner = module("adjoint128_checker_runner", "205_cm_frame_cubic_precision_check.py")
prior, checks, stem = build.prior, build.checks, build.stem


def generated():
    source = ROOT / "dembele/magma/251_cm_frame_cubic_adjoint_check.m"
    original = source.read_text(); before, after = original.split("cubeSpace:=", 1)
    header = "// D85 bounded split of checker 251, original SHA256 " + hashlib.sha256(source.read_bytes()).hexdigest()+"\n"
    move = before+'printf "CPU_SECONDS|%o\\n",Cputime(started);\nprint "PASS|268_ADJOINT_MOVE_CHECK";quit;\n'
    functions = before.split("// H =", 1)[0]+'''load "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m";
WRcoords:=RBase(Matrix(ZZ,adjoint_divisor_coordinates));
WR:=RMultiply(WRcoords,RG2);
cubeSpace:='''+after.replace("PASS|251_CM_FRAME_CUBIC_ADJOINT_CHECK", "PASS|268_ADJOINT_FUNCTION_CHECK")
    paths = []
    for label, text in (("move", move), ("functions", functions)):
        path = ROOT / "dembele/magma" / ("d85_128_adjoint_"+label+"_check.m")
        text = header+text
        if path.exists(): assert path.read_text() == text
        else: path.write_text(text)
        paths.append(path)
    return source, paths


def main():
    paths, wrapper = build.inputs_and_wrapper(128)
    cubic = stem(128).with_suffix(".json")
    checks.verify_records(json.loads(cubic.read_text()))
    wrapper += prior.loadline(cubic.with_suffix(".m"))
    original, scripts = generated()
    inputs = prior.CORE+[Path(__file__), Path(build.__file__), original, cubic]+paths
    positive, jobs = {}, []
    for label, script, marker in zip(("move", "functions"), scripts,
        ("PASS|268_ADJOINT_MOVE_CHECK", "PASS|268_ADJOINT_FUNCTION_CHECK")):
        base = stem(128, "_"+label+"_check")
        positive[label] = runner.run(script, base, marker, inputs, wrapper)
        jobs.append(Path(str(base)+"_job.json"))
        print("ADJOINT128_INDEPENDENT_CHECK_PASS", label, round(positive[label]["wall_seconds"], 3), flush=True)
    controls = {}
    for name, mutation, assertion in (
        ("norm", "adjoint_norm_scalar := (adjoint_norm_scalar+31^127) mod 31^128;", "assert norm_ok;"),
        ("trace", "adjoint_trace_quartic_coefficients[1] := (adjoint_trace_quartic_coefficients[1]+31^127) mod 31^128;", "assert trace_ok;"),
    ):
        base = stem(128, "_"+name+"_control")
        controls[name] = runner.run(scripts[1], base, "PASS|268_ADJOINT_FUNCTION_CHECK", inputs,
                                   wrapper+mutation+"\n", expected_failure=assertion)
        jobs.append(Path(str(base)+"_job.json"))
        print("ADJOINT128_DIGIT_CONTROL_REJECTED", name, round(controls[name]["wall_seconds"], 3), flush=True)
    report = {"status": "pass", "milestone": "D85", "date": "2026-09-22",
        "sources": [checks.source(p) for p in [Path(__file__), cubic, *jobs]],
        "precision_digits": 128, "modulus": 31**128, "independent_verification_completed": True,
        "same_class_verified": True, "unique_adjoint_representative_verified": True,
        "function_divisors_and_norm_verified": True, "quadratic_and_quartic_coefficients_verified": True,
        "positive_check": positive, "highest_digit_norm_control": controls["norm"],
        "highest_digit_trace_control": controls["trace"], "characteristic_zero_cubic_constructed": False,
        "arithmetic_identification_certified": False, "target_field_constructed": False}
    stem(128, "_check").with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|268_CM_FRAME_CUBIC_ADJOINT128_CHECK", flush=True)


if __name__ == "__main__":
    main()
