"""Normalize the certified class using K_X+2P and recover a weight-one cubic."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("adjoint_lift_build", ROOT / "dembele/pari/221_cm_frame_cubic_pointed_function.py")
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
prior, checks = build.prior, build.checks
NAMES = ("divisor_coordinates", "move_g_coefficients", "move_r_coefficients", "fixed_space_coordinates",
         "q_coefficients", "u_coefficients", "f_coefficients", "norm_scalar", "scaling_scalar",
         "a_quadratic_coefficients", "trace_quartic_coefficients")
CORE = tuple(key for key in NAMES if not key.startswith("move_"))


def stem(n, suffix=""):
    return DATA / f"cm_frame_cubic_adjoint_{n}{suffix}"


def inputs_and_wrapper(n):
    paths, wrapper, previous = build.inputs_and_wrapper(n)
    root = build.stem(n, "_check").with_suffix(".json")
    checks.verify_records(json.loads(root.read_text()))
    wrapper += prior.loadline(build.stem(n).with_suffix(".m"))
    paths += [root, Path(build.__file__), ROOT / "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m"]
    return paths, wrapper


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(1, 2, 4, 8, 16, 32), required=True)
    args = parser.parse_args(); n = args.digits
    base = stem(n)
    if n == 1:
        source = DATA / "cm_frame_cubic_adjoint_probe.json"
        old = json.loads(source.read_text()); checks.verify_records(old)
        data = old["data"]; paths = [source]
    else:
        paths, wrapper = inputs_and_wrapper(n)
        previous = stem(n//2).with_suffix(".json")
        old = json.loads(previous.read_text()); checks.verify_records(old)
        script = ROOT / "dembele/magma/249_cm_frame_cubic_adjoint_probe.m"
        job, jpath = prior.run(script, base, "PASS|249_CM_FRAME_CUBIC_ADJOINT_PROBE",
            prior.CORE+[Path(__file__), previous]+paths, wrapper, False)
        output = Path(job["log"]["path"]).read_text()
        data = {key: prior.helpers.field(output, "ADJOINT_"+key.upper()) for key in NAMES}
        for key in CORE: assert build.reduced(data[key], 31**(n//2)) == old["data"][key], key
        paths = [jpath, previous]
        print("ADJOINT_CUBIC_LIFT_PASS", n, round(job["wall_seconds"], 3), flush=True)
    mpath = base.with_suffix(".m"); mpath.write_text(prior.binding("adjoint_", data))
    report = {"status": "pass", "milestone": "D82", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__)]+paths],
              "magma_artifact": checks.source(mpath), "data": data, "precision_digits": n,
              "modulus": 31**n, "fixed_divisor": "K_X+2P", "fixed_divisor_degree": 80,
              "equation": "ell*T^3 - 3*A2*ell*T - R4 = 0; weight(T)=1",
              "coefficientwise_reduction_verified": n > 1,
              "characteristic_zero_cubic_constructed": False, "target_field_constructed": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|253_CM_FRAME_CUBIC_ADJOINT_LIFT", n, flush=True)


if __name__ == "__main__":
    main()
