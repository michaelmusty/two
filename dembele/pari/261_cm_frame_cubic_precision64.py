"""D83: extend frozen D82 orchestration to 64 digits without editing its sources.

Generated runners differ only in their accepted precision, milestone, and
provenance header. Arithmetic sources are unchanged. Each successful stage
gets an immutable receipt binding the driver, original/generated runners,
and resulting certificate. Existing successful stages are verified and reused.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
PARI = ROOT / "dembele/pari"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PARI / filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


prior = module("precision64_prior", "201_cm_frame_cubic_precision.py")
checks = prior.checks

# Explicit single textual changes keep the executable copies reviewable.
RUNNERS = {
    "jets": ("219_cm_frame_cubic_pointed_jets.py", "(1, 2, 4, 8, 16, 32)"),
    "newton": ("229_cm_frame_cubic_pointed_newton.py", "(8, 16, 32)"),
    "pointed": ("241_cm_frame_cubic_pointed_direct_function.py", "(16, 32)"),
    "pointed_check": ("243_cm_frame_cubic_pointed_direct_check.py", "(16, 32)"),
    "publish": ("244_cm_frame_cubic_pointed_publish.py", "(32,)"),
    "adjoint": ("253_cm_frame_cubic_adjoint_lift.py", "(1, 2, 4, 8, 16, 32)"),
    "adjoint_check": ("252_cm_frame_cubic_adjoint_check.py", "(1, 2, 4, 8, 16, 32)"),
}
STAGES = {
    "sections": (None, [], "cm_frame_cubic_precision_64_sections"),
    "jets": ("jets", [], "cm_frame_cubic_pointed_64_jets"),
    "divisor": (None, [], "cm_frame_cubic_pointed_64_formal_divisor"),
    "charts": ("newton", ["--stage", "charts"], "cm_frame_cubic_pointed_64_newton_average"),
    "newton_divisor": ("newton", ["--stage", "divisor"], "cm_frame_cubic_pointed_64_newton_divisor"),
    "newton_check": ("newton", ["--stage", "check"], "cm_frame_cubic_pointed_64_newton_third"),
    "publish_third": ("publish", ["--stage", "third"], "cm_frame_cubic_pointed_64_third"),
    "pointed": ("pointed", [], "cm_frame_cubic_pointed_64_direct"),
    "pointed_check": ("pointed_check", [], "cm_frame_cubic_pointed_64_direct_check"),
    "publish_cubic": ("publish", ["--stage", "cubic"], "cm_frame_cubic_pointed_64_check"),
    "adjoint": ("adjoint", [], "cm_frame_cubic_adjoint_64"),
    "adjoint_check": ("adjoint_check", [], "cm_frame_cubic_adjoint_64_check"),
}


def materialize(name):
    filename, choice = RUNNERS[name]
    source = PARI / filename
    text = source.read_text()
    old = "choices=" + choice
    assert text.count(old) == 1
    generated = "# D83 generated precision extension; original SHA256: " + hashlib.sha256(source.read_bytes()).hexdigest() + "\n"
    generated += "# Original: " + str(source.relative_to(ROOT)) + "; generator: 261_cm_frame_cubic_precision64.py\n"
    generated += text.replace(old, "choices=(64,)").replace('"milestone": "D82"', '"milestone": "D83"')
    target = PARI / ("d83_64_" + filename)
    if target.exists():
        assert target.read_text() == generated, target
    else:
        target.write_text(generated)
    return source, target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=tuple(STAGES), required=True)
    args = parser.parse_args()
    root = DATA / "cm_frame_cubic_adjoint_audit_32.json"
    checks.verify_records(json.loads(root.read_text()))
    receipt = DATA / ("cm_frame_cubic_precision64_" + args.stage + "_receipt.json")
    if receipt.exists():
        report = json.loads(receipt.read_text())
        checks.verify_records(report)
        assert report["status"] == "pass"
        print("PASS|261_PRECISION64_EXISTING_STAGE", args.stage, flush=True)
        return
    runner, arguments, output = STAGES[args.stage]
    sources = [Path(__file__), root]
    if args.stage == "sections":
        prior.sections(64, False)
        sources.append(Path(prior.__file__))
    elif args.stage == "divisor":
        formal = module("precision64_formal", "226_cm_frame_cubic_pointed_class_lift.py")
        formal.divisor(64, False)
        sources.append(Path(formal.__file__))
    else:
        source, target = materialize(runner)
        sources += [source, target]
        subprocess.run([sys.executable, str(target), "--digits", "64", *arguments], cwd=ROOT, check=True)
    result = DATA / (output + ".json")
    report = json.loads(result.read_text())
    checks.verify_records(report)
    assert report["status"] == "pass"
    sources.append(result)
    receipt.write_text(json.dumps({"status": "pass", "milestone": "D83", "date": "2026-09-22",
        "stage": args.stage, "precision_digits": 64,
        "sources": [checks.source(p) for p in sources],
        "frozen_32_digit_sources_unmodified": True}, indent=2) + "\n")
    print("PASS|261_PRECISION64_STAGE", args.stage, flush=True)


if __name__ == "__main__":
    main()
