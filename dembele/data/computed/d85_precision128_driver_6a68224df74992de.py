"""D85: memory-bounded 128-digit extension, with frozen sources and explicit adapters.

The only arithmetic change is the precision schedule of Newton matrix
inversion (283). Generated Magma copies redirect loads to that kernel.
Python copies extend accepted/hardcoded precisions and previous inputs.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
PARI = ROOT / "dembele/pari"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


prior = module("precision128_prior", PARI / "201_cm_frame_cubic_precision.py")
jobs = module("precision128_jobs", PARI / "272_cm_frame_bounded_jobs.py")
checks = prior.checks
PROCESS_SOURCES = []


def immutable(path, text):
    if path.exists():
        assert path.read_text() == text, path
    else:
        path.write_text(text)
    return path


def snapshot():
    path = Path(__file__)
    return immutable(DATA / ("d85_precision128_driver_"+jobs.source(path)["sha256"][:16]+".py"), path.read_text())


def magma_source(path, dependencies):
    path = Path(path).resolve(); dependencies.add(path)
    if path.name == "197_cm_frame_cubic_precision_arithmetic.m":
        replacement = ROOT / "dembele/magma/289_cm_frame_block_arithmetic.m"
        dependencies.add(replacement)
        return replacement
    if path.name == "199_cm_frame_cubic_precision_model.m":
        replacement = ROOT / "dembele/magma/290_cm_frame_block_model.m"
        dependencies.add(replacement)
        dependencies.add(ROOT / "dembele/magma/289_cm_frame_block_arithmetic.m")
        for dep in re.findall(r'load "(dembele/data/computed/[^"\n]+\.m)";', replacement.read_text()):
            dependencies.add(ROOT / dep)
        return replacement
    old = path.read_text()
    def redirect(match):
        dependency = ROOT / match.group(1)
        if not dependency.exists():
            return match.group(0)
        if match.group(1).startswith("dembele/magma/"):
            mapped = magma_source(dependency, dependencies)
        else:
            dependencies.add(dependency); mapped = dependency
        return 'load "'+str(mapped.relative_to(ROOT))+'";'
    new = re.sub(r'load "(dembele/(?:magma|data/computed)/[^"\n]+\.m)";', redirect, old)
    if new == old:
        return path
    target = ROOT / "dembele/magma" / ("d85_128_block_"+path.name)
    content = "// D85 redirected loads; original SHA256 "+jobs.source(path)["sha256"]+"\n"+new
    immutable(target, content); dependencies.add(target)
    return target


def run(script, base, marker, inputs, wrapper_text, rebuild=False, expected_failure=None):
    assert not rebuild, "Use a distinct immutable attempt for changes or failures."
    original_job = Path(str(base)+"_job.json")
    if original_job.exists() and json.loads(original_job.read_text())["status"] != "pass":
        checks.verify_records(json.loads(original_job.read_text()))
        inputs = list(inputs)+[original_job, Path(str(base)+"_memory2_job.json")]
        base = Path(str(base)+"_block3")
    jpath = Path(str(base)+"_job.json")
    if jpath.exists():
        record = json.loads(jpath.read_text()); checks.verify_records(record)
        assert record["status"] == "pass", f"Preserve unsuccessful job: {jpath}"
        output = Path(record["log"]["path"]).read_text()
        if expected_failure is None:
            assert marker in output
        else:
            assert expected_failure in output and "Assertion failed" in output and marker not in output
        return record, jpath
    dependencies = set()
    mapped = magma_source(script, dependencies)
    wrapper = Path(str(base)+"_run.m")
    immutable(wrapper, "SetQuitOnError(true);\n"+wrapper_text+prior.loadline(mapped))
    record = jobs.run_job(jobs.prior.magma_command(wrapper), base.with_suffix(".out"), 180, marker,
                          expected_failure=expected_failure)
    all_paths = set(inputs) | dependencies | set(PROCESS_SOURCES) | {snapshot(), wrapper}
    record["sources"] += [checks.source(p) for p in sorted(all_paths, key=str)]
    jpath.write_text(json.dumps(record, indent=2)+"\n")
    assert record["status"] == "pass", f"{base.name}: {record['status']}"
    return record, jpath


def check_run(script, base, marker, inputs, wrapper_text, expected_failure=None):
    return run(script, base, marker, inputs, wrapper_text, expected_failure=expected_failure)[0]


def configure(obj, seen=None):
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return
    seen.add(id(obj))
    filename = Path(getattr(obj, "__file__", "/"))
    if filename.parent == PARI:
        PROCESS_SOURCES.append(filename)
        if filename.name == "201_cm_frame_cubic_precision.py":
            obj.run = run
        if filename.name == "205_cm_frame_cubic_precision_check.py":
            obj.run = check_run
        for value in list(vars(obj).values()):
            if isinstance(value, types.ModuleType) and Path(getattr(value, "__file__", "/") or "/").parent == PARI:
                configure(value, seen)


HARDCODED = ["262_cm_frame_cubic_staged_functions.py", "264_cm_frame_cubic_class_checks.py",
    "265_cm_frame_cubic_pointed64_check.py", "266_cm_frame_cubic_pointed64_functions.py",
    "267_cm_frame_cubic_adjoint64_functions.py", "268_cm_frame_cubic_adjoint64_check.py",
    "269_cm_frame_cubic_adjoint64_move.py"]
CHOICES = {"219_cm_frame_cubic_pointed_jets.py": "(1, 2, 4, 8, 16, 32)",
           "229_cm_frame_cubic_pointed_newton.py": "(8, 16, 32)",
           "244_cm_frame_cubic_pointed_publish.py": "(32,)"}


def scale(text):
    return re.sub(r"(?<!\d)(32|63|64)(?!\d)", lambda m: {"32":"64", "63":"127", "64":"128"}[m.group()], text)


def generated_python(filename):
    source = PARI / filename
    old = source.read_text()
    if filename in HARDCODED:
        new = scale(old)
        for dependency in HARDCODED:
            new = new.replace(scale(dependency), "d85_128_"+dependency)
    else:
        choice = "choices="+CHOICES[filename]
        assert old.count(choice) == 1
        new = old.replace(choice, "choices=(128,)")
    new = new.replace("D83", "D85").replace("d83_", "d85_")
    new = new.replace('"milestone": "D82"', '"milestone": "D85"')
    target = PARI / ("d85_128_"+filename)
    immutable(target, "# D85 precision adapter; original SHA256 "+jobs.source(source)["sha256"]+"\n"+new)
    PROCESS_SOURCES.extend((source, target))
    return target


STAGES = {
    "sections": ("201_cm_frame_cubic_precision.py", "cm_frame_cubic_precision_128_sections"),
    "jets": ("219_cm_frame_cubic_pointed_jets.py", "cm_frame_cubic_pointed_128_jets"),
    "divisor": ("226_cm_frame_cubic_pointed_class_lift.py", "cm_frame_cubic_pointed_128_formal_divisor"),
    "charts": ("229_cm_frame_cubic_pointed_newton.py", "cm_frame_cubic_pointed_128_newton_average"),
    "newton_divisor": ("229_cm_frame_cubic_pointed_newton.py", "cm_frame_cubic_pointed_128_newton_divisor"),
    "class_check": ("264_cm_frame_cubic_class_checks.py", "cm_frame_cubic_pointed_128_newton_third"),
    "publish_third": ("244_cm_frame_cubic_pointed_publish.py", "cm_frame_cubic_pointed_128_third"),
    "pointed_functions": ("266_cm_frame_cubic_pointed64_functions.py", "cm_frame_cubic_pointed_128_function_checkpoint"),
    "pointed_fit": ("262_cm_frame_cubic_staged_functions.py", "cm_frame_cubic_pointed_128_direct"),
    "pointed_check": ("265_cm_frame_cubic_pointed64_check.py", "cm_frame_cubic_pointed_128_direct_check"),
    "publish_cubic": ("244_cm_frame_cubic_pointed_publish.py", "cm_frame_cubic_pointed_128_check"),
    "adjoint_move": ("269_cm_frame_cubic_adjoint64_move.py", "cm_frame_cubic_adjoint_128_function_checkpoint"),
    "adjoint_functions": ("267_cm_frame_cubic_adjoint64_functions.py", "cm_frame_cubic_adjoint_128"),
    "adjoint_check": ("268_cm_frame_cubic_adjoint64_check.py", "cm_frame_cubic_adjoint_128_check"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=tuple(STAGES), required=True)
    args = parser.parse_args()
    root = DATA / "cm_frame_structural_checkpoint.json"
    checks.verify_records(json.loads(root.read_text()))
    receipt = DATA / ("cm_frame_cubic_precision128_"+args.stage+"_receipt.json")
    if receipt.exists():
        record = json.loads(receipt.read_text()); checks.verify_records(record)
        assert record["status"] == "pass"
        print("PASS|282_EXISTING_PRECISION128", args.stage)
        return
    for filename in HARDCODED:
        generated_python(filename)
    filename, output = STAGES[args.stage]
    target = generated_python(filename) if filename in HARDCODED or filename in CHOICES else PARI / filename
    obj = module("precision128_stage", target); configure(obj)
    if args.stage == "sections":
        obj.sections(128, False)
    elif args.stage == "divisor":
        obj.divisor(128, False)
    else:
        arguments = []
        if filename in CHOICES:
            arguments += ["--digits", "128"]
        if args.stage in ("charts", "newton_divisor"):
            arguments += ["--stage", "charts" if args.stage == "charts" else "divisor"]
        if args.stage in ("publish_third", "publish_cubic"):
            arguments += ["--stage", "third" if args.stage == "publish_third" else "cubic"]
        if args.stage == "pointed_fit":
            arguments += ["--family", "pointed", "--stage", "last"]
        sys.argv = [str(target), *arguments]
        obj.main()
    result = DATA / (output+".json")
    record = json.loads(result.read_text()); checks.verify_records(record)
    assert record["status"] == "pass"
    receipt.write_text(json.dumps({"status": "pass", "milestone": "D85", "stage": args.stage,
        "precision_digits": 128, "sources": [checks.source(p) for p in
            sorted(set(PROCESS_SOURCES+[snapshot(), root, result]), key=str)],
        "previous_certificates_unmodified": True}, indent=2)+"\n")
    print("PASS|282_PRECISION128_STAGE", args.stage, flush=True)


if __name__ == "__main__":
    main()
