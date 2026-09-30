"""Certify the formal-route cubic, its persistent gauge, and high-digit controls."""
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


construct = module("formal_cert_construct", ROOT / "dembele/pari/214_cm_frame_cubic_formal_function.py")
verify = module("formal_cert_verify", ROOT / "dembele/pari/205_cm_frame_cubic_precision_check.py")
prior, checks = construct.prior, construct.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args(); n = args.digits
    result = prior.stem(n, "_formal_cubic_check").with_suffix(".json")
    if args.collect_only:
        report = json.loads(result.read_text()); checks.verify_records(report)
        assert report["independent_verification_completed"]
        print("PASS|215_CM_FRAME_CUBIC_FORMAL_PRECISION_PROVENANCE", n)
        return
    bases = [prior.stem(n, "_sections"), prior.stem(n, "_formal_third"), prior.stem(n, "_formal_cubic")]
    prev = construct.previous_base(n)
    previous_root = DATA / "cm_frame_cubic_lift_check.json" if n == 4 else prior.stem(n//2, "_check").with_suffix(".json")
    if not previous_root.exists(): previous_root = prior.stem(n//2, "_formal_cubic_check").with_suffix(".json")
    algebra_check = prior.stem(n, "_formal_comparison").with_suffix(".json")
    if not algebra_check.exists(): algebra_check = prior.stem(n, "_formal_check").with_suffix(".json")
    inputs = prior.CORE+[Path(__file__), ROOT / "dembele/magma/202_cm_frame_cubic_gauge_arithmetic.m",
                        ROOT / "dembele/pari/205_cm_frame_cubic_precision_check.py",
                        DATA / "cm_frame_cubic_gauge.json", previous_root, algebra_check,
                        prev.with_suffix(".json")]+[p.with_suffix(".json") for p in bases]
    for path in inputs:
        if path.suffix == ".json": checks.verify_records(json.loads(path.read_text()))
    verify.check_section_reduction(n)
    previous = json.loads(prev.with_suffix(".json").read_text())["data"].copy()
    previous["modulus"] = 31**(n//2)
    wrapper = f"precision_digits := {n};\n"+"".join(prior.loadline(p.with_suffix(".m")) for p in bases)
    wrapper += prior.binding("previous_cubic_", previous)
    script = ROOT / "dembele/magma/204_cm_frame_cubic_precision_check.m"
    marker = "PASS|204_CM_FRAME_CUBIC_PRECISION_CHECK"
    positive = verify.run(script, prior.stem(n, "_formal_cubic_check"), marker, inputs, wrapper)
    controls = {}
    for name, mutation, assertion in (
        ("norm", "precision_cubic_norm_scalar := (precision_cubic_norm_scalar+31^(precision_digits-1)) mod 31^precision_digits;", "assert norm_ok;"),
        ("trace", "precision_cubic_trace_numerator_coefficients[1] := (precision_cubic_trace_numerator_coefficients[1]+31^(precision_digits-1)) mod 31^precision_digits;", "assert trace_ok;"),
    ):
        controls[name] = verify.run(script, prior.stem(n, f"_formal_cubic_{name}_control"), marker,
                                    inputs, wrapper+mutation+"\n", expected_failure=assertion)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), previous_root, algebra_check,
                  bases[-1].with_suffix(".json"), Path(str(prior.stem(n, "_formal_cubic_check"))+"_job.json"),
                  Path(str(prior.stem(n, "_formal_cubic_norm_control"))+"_job.json"),
                  Path(str(prior.stem(n, "_formal_cubic_trace_control"))+"_job.json")]],
              "precision_digits": n, "modulus": 31**n, "persistent_gauge_verified": True,
              "independent_verification_completed": True, "coefficientwise_reduction_verified": True,
              "idempotent_divisor_lift_verified": True, "formal_kernel_correction_verified": True,
              "function_divisors_and_norm_verified": True, "reflection_quotient_genus": 64,
              "positive_check": positive, "highest_digit_norm_control": controls["norm"],
              "highest_digit_trace_control": controls["trace"], "class_number_assumed": False,
              "characteristic_zero_cubic_constructed": False, "arithmetic_identification_certified": False,
              "target_field_constructed": False, "proof": "dembele/certificates/cm-frame-cubic-precision.md"}
    result.write_text(json.dumps(report, indent=2)+"\n")
    checks.verify_records(report)
    print("PASS|215_CM_FRAME_CUBIC_FORMAL_PRECISION_CHECK", n, "both highest-digit controls rejected")


if __name__ == "__main__":
    main()
