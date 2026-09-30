"""Construct the cubic with a unique pointed divisor and fixed linear denominator."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_function_jets", ROOT / "dembele/pari/219_cm_frame_cubic_pointed_jets.py")
jets = importlib.util.module_from_spec(spec); spec.loader.exec_module(jets)
prior, helpers, checks = jets.prior, jets.helpers, jets.checks
stem = jets.pointed_stem
CORE_NAMES = ("descended_divisor_coordinates", "q_coefficients", "u_coefficients", "f_coefficients",
              "norm_scalar", "a_coefficients", "denominator_coefficients", "trace_numerator_coefficients",
              "trace_septic_coefficients", "scaling_scalar")
MOVE_NAMES = ("initial_divisor_coordinates", "initial_moving_coefficients", "move_g_coefficients", "move_r_coefficients")


def third_base(n):
    if n == 1: return stem(1, "_third")
    if n == 2: return DATA / "cm_frame_cubic_lift_third"
    pointed = stem(n, "_third")
    return pointed if pointed.with_suffix(".json").exists() else prior.stem(n, "_formal_third")


def inputs_and_wrapper(n):
    sections, third, jet = jets.sections_base(n), third_base(n), stem(n, "_jets")
    paths = [x.with_suffix(".json") for x in (sections, third, jet)]
    paths += [DATA / "cm_frame_cubic_gauge.json"]
    for path in paths: checks.verify_records(json.loads(path.read_text()))
    wrapper = f"precision_digits := {n};\n"+prior.loadline(sections.with_suffix(".m"))
    wrapper += prior.loadline(third.with_suffix(".m"))+prior.loadline(jet.with_suffix(".m"))
    if n == 2:
        wrapper += "precision_third_coordinates := lift_third_coordinates;\nprecision_third_delta_coordinates := lift_delta_coordinates;\n"
    previous = {"modulus": 1}
    if n > 1:
        path = stem(n//2).with_suffix(".json"); paths.append(path)
        old = json.loads(path.read_text()); checks.verify_records(old)
        previous = {key: old["data"][key] for key in CORE_NAMES}
        previous["modulus"] = 31**(n//2)
    else:
        previous.update({key: 0 if key.endswith("scalar") else [] for key in CORE_NAMES})
    wrapper += prior.binding("previous_cubic_", previous)
    return paths, wrapper, previous


def reduced(value, modulus):
    return [reduced(x, modulus) for x in value] if isinstance(value, list) else value % modulus


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(1, 2, 4, 8, 16, 32), required=True)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    paths, wrapper, previous = inputs_and_wrapper(n)
    script = ROOT / "dembele/magma/220_cm_frame_cubic_pointed_function.m"
    base = stem(n)
    job, jpath = prior.run(script, base, "PASS|220_CM_FRAME_CUBIC_POINTED_FUNCTION",
        prior.CORE+[Path(__file__), Path(jets.__file__)]+paths, wrapper, args.rebuild)
    output = Path(job["log"]["path"]).read_text()
    data = {key: helpers.field(output, "POINTED_"+key.upper()) for key in CORE_NAMES+MOVE_NAMES}
    if n > 1:
        for key in CORE_NAMES: assert reduced(data[key], previous["modulus"]) == previous[key], key
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("pointed_cubic_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), jpath]],
              "magma_artifact": checks.source(mpath), "data": data,
              "precision_digits": n, "modulus": 31**n, "pointed_divisor_multiplicity": 80,
              "pointed_condition_rank": 80, "residual_divisor_degree": 40,
              "leading_a_coefficient": 1, "leading_trace_coefficient": 2,
              "equation": "ell*T^3 - 3*A4*ell*T - R7 = 0; T has canonical weight 2",
              "normalization_uses_only_linear_algebra_and_unit_division": True,
              "coefficientwise_reduction_verified": n > 1,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|221_CM_FRAME_CUBIC_POINTED_FUNCTION", n, round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()
