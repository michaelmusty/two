"""Test division of the class error by linear interpolation in pointed coordinates.

The interpolated matrix must pass an independent actual-divisor certificate
and direct class identities. No unconstrained matrix lift is accepted.
"""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_newton_prior", ROOT / "dembele/pari/201_cm_frame_cubic_precision.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
checks, helpers = prior.checks, prior.helpers


def stem(n, suffix=""):
    return DATA / f"cm_frame_cubic_pointed_{n}{suffix}"


def save(base, data, prefix, paths, n, **extra):
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding(prefix, data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__)]+paths],
              "magma_artifact": checks.source(mpath), "data": data,
              "precision_digits": n, "modulus": 31**n, **extra}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(8, 16, 32), required=True)
    parser.add_argument("--stage", choices=("charts", "divisor", "check", "all"), default="all")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(); n = args.digits
    prev = stem(n//2); sections = prior.stem(n, "_sections"); jets = stem(n, "_jets")
    divisor = stem(n, "_formal_divisor") if n > 8 else prior.stem(n, "_formal_divisor")
    paths = [p.with_suffix(".json") for p in (prev, sections, jets, divisor)]
    paths.append(stem(n//2, "_check").with_suffix(".json"))
    for path in paths: checks.verify_records(json.loads(path.read_text()))
    old = json.loads(prev.with_suffix(".json").read_text())["data"]
    previous = {"descended_divisor_coordinates": old["descended_divisor_coordinates"], "modulus": 31**(n//2)}
    wrapper = f"precision_digits := {n};\n"
    wrapper += "".join(prior.loadline(p.with_suffix(".m")) for p in (sections, jets, divisor))
    wrapper += prior.binding("previous_cubic_", previous)
    inputs = prior.CORE+[Path(__file__), ROOT / "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m"]+paths
    classes = stem(n, "_newton_classes")
    average = stem(n, "_newton_average")
    if args.stage in ("charts", "all"):
        script = ROOT / "dembele/magma/228_cm_frame_cubic_pointed_newton.m"
        for mode in ("classes", "normalize_a", "normalize_b"):
            base = stem(n, "_newton_"+mode)
            active = wrapper+f'newton_mode := "{mode}";\n'
            sources = inputs.copy()
            if mode != "classes":
                checks.verify_records(json.loads(classes.with_suffix(".json").read_text()))
                active += prior.loadline(classes.with_suffix(".m")); sources.append(classes.with_suffix(".json"))
            else:
                active += "newton_target_coordinates := [];\n"
            job, jpath = prior.run(script, base, "PASS|228_CM_FRAME_CUBIC_POINTED_NEWTON", sources, active, args.rebuild)
            output = Path(job["log"]["path"]).read_text()
            names = ("target_coordinates", "delta_coordinates") if mode == "classes" else (
                "pointed_coordinates", "g_coefficients", "r_coefficients", "g_vanishing_order")
            data = {key: helpers.field(output, "NEWTON_"+key.upper()) for key in names}
            save(base, data, "newton_", [jpath], n)
            print("POINTED_NEWTON_STAGE_PASS", n, mode, round(job["wall_seconds"], 3), flush=True)
        sources = [stem(n, "_newton_normalize_"+c).with_suffix(".json") for c in ("a", "b")]
        left, right = [json.loads(p.read_text())["data"]["pointed_coordinates"] for p in sources]
        q, m = 31**(n//2), 31**n
        assert all((x-y) % q == 0 for aa, bb in zip(left, right) for x, y in zip(aa, bb))
        inv3 = pow(3, -1, m)
        data = {"average_coordinates": [[((2*x+y)*inv3) % m for x, y in zip(aa, bb)] for aa, bb in zip(left, right)]}
        save(average, data, "newton_", sources, n, actual_divisor_verified=False)
    if args.stage in ("divisor", "check", "all"):
        checks.verify_records(json.loads(average.with_suffix(".json").read_text()))
        wrapper += prior.loadline(average.with_suffix(".m")); inputs.append(average.with_suffix(".json"))
    actual = stem(n, "_newton_divisor")
    if args.stage in ("divisor", "all"):
        script = ROOT / "dembele/magma/230_cm_frame_cubic_pointed_newton_divisor.m"
        job, jpath = prior.run(script, actual, "PASS|230_CM_FRAME_CUBIC_POINTED_NEWTON_DIVISOR",
            inputs+[ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m"], wrapper, args.rebuild)
        output = Path(job["log"]["path"]).read_text()
        data = {key: helpers.field(output, "FORMAL_"+key.upper()) for key in (
            "divisor_coordinates", "g_coefficients", "h_coefficients", "quotient_basis_indices", "idempotent_coefficients")}
        save(actual, data, "formal_", [jpath], n, actual_interpolated_divisor_verified=True)
        print("POINTED_NEWTON_ACTUAL_DIVISOR_PASS", n, round(job["wall_seconds"], 3), flush=True)
    if args.stage in ("check", "all"):
        checks.verify_records(json.loads(actual.with_suffix(".json").read_text()))
        inputs.append(actual.with_suffix(".json"))
        comparison = prior.stem(n, "_third") if n == 8 else stem(n, "_third")
        available = comparison.with_suffix(".json").exists()
        if available:
            path = comparison.with_suffix(".json"); report = json.loads(path.read_text()); checks.verify_records(report)
            inputs.append(path); wrapper += prior.binding("comparison_", {"third_coordinates": report["data"]["coordinates"]})
        else:
            wrapper += "comparison_third_coordinates := [];\n"
        wrapper += f"comparison_available := {'true' if available else 'false'};\n"
        expected = stem(n).with_suffix(".json")
        if expected.exists():
            record = json.loads(expected.read_text()); checks.verify_records(record); inputs.append(expected)
            wrapper += prior.binding("expected_", {"pointed_coordinates": record["data"]["descended_divisor_coordinates"]})
        else:
            wrapper += "expected_pointed_coordinates := [];\n"
        script = ROOT / "dembele/magma/231_cm_frame_cubic_pointed_newton_check.m"
        base = stem(n, "_newton_check")
        job, jpath = prior.run(script, base, "PASS|231_CM_FRAME_CUBIC_POINTED_NEWTON_CHECK", inputs, wrapper, args.rebuild)
        output = Path(job["log"]["path"]).read_text()
        data = {"coordinates": json.loads(average.with_suffix(".json").read_text())["data"]["average_coordinates"],
                "delta_coordinates": helpers.field(output, "NEWTON_DELTA_COORDINATES")}
        save(stem(n, "_newton_third"), data, "precision_third_", [jpath], n,
             actual_divisor_verified=True, three_division_verified=True,
             scalar_comparison_completed=available, matches_existing_pointed_model=expected.exists())
        print("POINTED_NEWTON_CLASS_CHECK_PASS", n, round(job["wall_seconds"], 3), flush=True)
    print("PASS|229_CM_FRAME_CUBIC_POINTED_NEWTON", n, args.stage, flush=True)


if __name__ == "__main__":
    main()
