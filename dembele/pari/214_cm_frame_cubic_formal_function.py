"""Recover the fixed-gauge cubic from the short formal-kernel class lift."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("formal_function_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
helpers, checks = prior.helpers, prior.checks


def previous_base(n):
    preferred = prior.previous_cubic(n)
    return preferred if preferred.with_suffix(".json").exists() else prior.stem(n//2, "_formal_cubic")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(4, 8, 16, 32), required=True)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    sections = prior.stem(n, "_sections"); third = prior.stem(n, "_formal_third"); prev = previous_base(n)
    for path in (sections, third, prev): checks.verify_records(json.loads(path.with_suffix(".json").read_text()))
    names = ("descended_divisor_coordinates", "q_coefficients", "u_coefficients", "f_coefficients",
             "norm_scalar", "a_coefficients", "denominator_coefficients", "trace_numerator_coefficients")
    old = json.loads(prev.with_suffix(".json").read_text())["data"]
    previous = {key: old[key] for key in names}; previous["modulus"] = 31**(n//2)
    wrapper = f"precision_digits := {n};\n"+prior.loadline(sections.with_suffix(".m"))
    wrapper += prior.loadline(third.with_suffix(".m"))+prior.binding("previous_cubic_", previous)
    script = ROOT / "dembele/magma/203_cm_frame_cubic_precision_function.m"
    base = prior.stem(n, "_formal_cubic")
    job, jpath = prior.run(script, base, "PASS|203_CM_FRAME_CUBIC_PRECISION_FUNCTION",
        prior.CORE+[Path(__file__), ROOT / "dembele/magma/202_cm_frame_cubic_gauge_arithmetic.m",
                    sections.with_suffix(".json"), third.with_suffix(".json"),
                    prev.with_suffix(".json"), DATA / "cm_frame_cubic_gauge.json"], wrapper, args.rebuild)
    output = Path(job["log"]["path"]).read_text()
    data = {key: helpers.field(output, "PRECISION_"+key.upper()) for key in names}
    for key in names:
        if key == "norm_scalar": assert data[key] % previous["modulus"] == old[key]
        elif key == "descended_divisor_coordinates":
            assert [[x % previous["modulus"] for x in row] for row in data[key]] == old[key]
        else: assert [x % previous["modulus"] for x in data[key]] == old[key]
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("precision_cubic_", data))
    sources = [Path(__file__), jpath, DATA / "cm_frame_cubic_gauge.json"]
    comparison = prior.stem(n).with_suffix(".json"); compared = comparison.exists()
    if compared:
        original = json.loads(comparison.read_text()); checks.verify_records(original)
        assert data == original["data"]; sources.append(comparison)
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in sources], "magma_artifact": checks.source(mpath),
              "data": data, "precision_digits": n, "modulus": 31**n,
              "persistent_gauge_verified": True, "coefficientwise_reduction_verified": True,
              "global_route_coefficient_comparison_completed": compared,
              "previous_precision_digits": n//2, "characteristic_zero_cubic_constructed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|214_CM_FRAME_CUBIC_FORMAL_FUNCTION", n, "global comparison", compared, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
