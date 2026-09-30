"""Extract canonical local coefficients for a less basis-dependent recognition pilot."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("pointed_local_build", ROOT / "dembele/pari/221_cm_frame_cubic_pointed_function.py")
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
prior, checks, stem = build.prior, build.checks, build.stem


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, choices=(8, 16, 32), required=True)
    args = parser.parse_args(); n = args.digits
    paths, wrapper, previous = build.inputs_and_wrapper(n)
    for suffix in ("", "_check"):
        path = stem(n, suffix).with_suffix(".json"); checks.verify_records(json.loads(path.read_text())); paths.append(path)
    wrapper += prior.loadline(stem(n).with_suffix(".m"))
    script = ROOT / "dembele/magma/237_cm_frame_cubic_pointed_local_invariants.m"
    base = stem(n, "_local_invariants")
    job, jpath = prior.run(script, base, "PASS|237_CM_FRAME_CUBIC_POINTED_LOCAL_INVARIANTS",
        prior.CORE+[Path(__file__), Path(build.__file__), ROOT / "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m"]+paths, wrapper, False)
    output = Path(job["log"]["path"]).read_text()
    data = {key: prior.helpers.field(output, "LOCAL_"+key.upper()) for key in ("normalized_coefficients", "a_coefficients")}
    sources = [Path(__file__), jpath]
    if n > 8:
        previous = stem(n//2, "_local_invariants").with_suffix(".json"); sources.append(previous)
        old = json.loads(previous.read_text()); checks.verify_records(old)
        for key in data: assert [x % 31**(n//2) for x in data[key]] == old["data"][key]
    report = {"status": "pass", "sources": [checks.source(p) for p in sources],
              "data": data, "precision_digits": n, "modulus": 31**n,
              "definitions": ["a[w^162]", "h[w^241]/sqrt(-3)", "h[w^242]", "h[w^243]/sqrt(-3)"],
              "exact_finite_precision_norm_relation": "2*gamma+3*beta^2=3*alpha",
              "characteristic_zero_recognition": False}
    base.with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|238_CM_FRAME_CUBIC_POINTED_LOCAL_INVARIANTS", n, data["normalized_coefficients"], round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
