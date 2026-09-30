"""Independently verify the adjoint representative and cubic, with digit controls."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


build = module("adjoint_check_build", ROOT / "dembele/pari/253_cm_frame_cubic_adjoint_lift.py")
runner = module("adjoint_check_runner", ROOT / "dembele/pari/205_cm_frame_cubic_precision_check.py")
prior, checks, stem = build.prior, build.checks, build.stem


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(1, 2, 4, 8, 16, 32), required=True)
    args = parser.parse_args(); n = args.digits
    paths, wrapper = build.inputs_and_wrapper(n)
    source = stem(n).with_suffix(".json"); record = json.loads(source.read_text()); checks.verify_records(record)
    wrapper += prior.loadline(source.with_suffix(".m"))
    script = ROOT / "dembele/magma/251_cm_frame_cubic_adjoint_check.m"
    marker = "PASS|251_CM_FRAME_CUBIC_ADJOINT_CHECK"
    inputs = prior.CORE+[Path(__file__), Path(build.__file__), source]+paths
    positive = runner.run(script, stem(n, "_check"), marker, inputs, wrapper)
    print("ADJOINT_INDEPENDENT_CHECK_PASS", n, round(positive["wall_seconds"], 3), flush=True)
    controls = {}
    for name, mutation, assertion in (
        ("norm", "adjoint_norm_scalar := (adjoint_norm_scalar+31^(precision_digits-1)) mod 31^precision_digits;", "assert norm_ok;"),
        ("trace", "adjoint_trace_quartic_coefficients[1] := (adjoint_trace_quartic_coefficients[1]+31^(precision_digits-1)) mod 31^precision_digits;", "assert trace_ok;"),
    ):
        controls[name] = runner.run(script, stem(n, f"_{name}_control"), marker, inputs, wrapper+mutation+"\n", expected_failure=assertion)
        print("ADJOINT_DIGIT_CONTROL_REJECTED", n, name, round(controls[name]["wall_seconds"], 3), flush=True)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), source,
                  Path(str(stem(n, "_check"))+"_job.json"), Path(str(stem(n, "_norm_control"))+"_job.json"),
                  Path(str(stem(n, "_trace_control"))+"_job.json")]],
              "precision_digits": n, "modulus": 31**n,
              "independent_verification_completed": True, "same_class_verified": True,
              "unique_adjoint_representative_verified": True, "function_divisors_and_norm_verified": True,
              "quadratic_and_quartic_coefficients_verified": True, "positive_check": positive,
              "highest_digit_norm_control": controls["norm"], "highest_digit_trace_control": controls["trace"],
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    stem(n, "_check").with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|252_CM_FRAME_CUBIC_ADJOINT_CHECK", n, flush=True)


if __name__ == "__main__":
    main()
