"""D86: execute the existing 128-digit stages on Chatelet with more resources.

The mathematical adapters and precision-aware kernel are those of 282/283.
Python parsing and certificate assembly remain local. Failed local jobs
and the D85 review are preserved; remote execution has separate receipts.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
PARI = ROOT / "dembele/pari"
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PARI / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


driver = module("chatelet128_driver", "282_cm_frame_cubic_precision128.py")
transport = module("chatelet128_transport", "299_cm_frame_chatelet_transport.py")
checks = driver.checks
PREPARE_ONLY = False


class PreparedOnly(Exception):
    pass


def snapshot():
    path = Path(__file__)
    target = DATA / ("d86_precision128_driver_"+checks.source(path)["sha256"][:16]+".py")
    driver.immutable(target, path.read_text())
    return target


def remote_run(script, base, marker, inputs, wrapper_text, rebuild=False, expected_failure=None):
    assert not rebuild
    original = Path(str(base)+"_job.json")
    if original.exists() and json.loads(original.read_text())["status"] != "pass":
        checks.verify_records(json.loads(original.read_text()))
        inputs = list(inputs)+[original]
        base = Path(str(base)+"_chatelet_d86")
    jpath = Path(str(base)+"_job.json")
    if jpath.exists():
        record = json.loads(jpath.read_text()); checks.verify_records(record)
        assert record["status"] == "pass", "Preserve failed attempt: "+str(jpath)
        output = Path(record["log"]["path"]).read_text()
        if expected_failure is None:
            assert marker in output
        else:
            assert expected_failure in output and "Assertion failed" in output and marker not in output
        return record, jpath
    dependencies = set()
    mapped = driver.magma_source(script, dependencies)
    wrapper = Path(str(base)+"_run.m")
    driver.immutable(wrapper, "SetQuitOnError(true);\nSetNthreads(1);\n"+wrapper_text+driver.prior.loadline(mapped))
    if PREPARE_ONLY:
        import re
        from urllib.parse import urlsplit
        paths = transport.magma_inputs(wrapper) | {transport.WORKER}
        destination = urlsplit(transport.env()["base"]).hostname
        assert destination == "chatelet.mit.edu"
        denied = re.compile(rb"COCALC_(?:ACCOUNT_API_KEY|API_KEY)|Authorization:|BEGIN [A-Z ]*PRIVATE KEY|sk_[A-Za-z0-9]{16,}")
        assert all(not denied.search(p.read_bytes()) for p in paths)
        manifest = {"status": "prepared_only", "destination": destination,
            "remote_directory": transport.REMOTE, "job": base.name,
            "file_count": len(paths), "total_bytes": sum(p.stat().st_size for p in paths),
            "files": [dict(checks.source(p), bytes=p.stat().st_size) for p in sorted(paths)],
            "payload_scope": "Magma mathematical inputs and scripts, plus the standalone bounded job worker",
            "credentials_included": False, "unrelated_project_files_included": False,
            "credential_marker_scan_passed": True,
            "per_job_wall_limit_seconds": 1800, "per_job_memory_limit_bytes": 8000000000}
        path = DATA / (base.name+"_planned_transfer.json")
        driver.immutable(path, json.dumps(manifest, indent=2)+"\n")
        print("PREPARED_REMOTE_TRANSFER", path, len(paths), manifest["total_bytes"], flush=True)
        raise PreparedOnly
    record = transport.execute(wrapper, base, marker, expected_failure)
    sources = set(inputs) | dependencies | set(driver.PROCESS_SOURCES) | {
        snapshot(), wrapper, Path(driver.__file__), driver.snapshot()}
    record["sources"] += [checks.source(p) for p in sorted(sources, key=str)]
    jpath.write_text(json.dumps(record, indent=2)+"\n")
    assert record["status"] == "pass", f"{base.name}: {record['status']}"
    return record, jpath


def check_run(script, base, marker, inputs, wrapper_text, expected_failure=None):
    return remote_run(script, base, marker, inputs, wrapper_text, expected_failure=expected_failure)[0]


def main():
    global PREPARE_ONLY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=tuple(driver.STAGES), required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    PREPARE_ONLY = args.prepare_only
    root = DATA / "cm_frame_cubic_128_attempt_review.json"
    checks.verify_records(json.loads(root.read_text()))
    receipt = DATA / ("cm_frame_cubic_precision128_chatelet_"+args.stage+"_receipt.json")
    if receipt.exists():
        record = json.loads(receipt.read_text()); checks.verify_records(record)
        assert record["status"] == "pass"
        print("PASS|300_EXISTING_CHATELET_STAGE", args.stage, flush=True); return
    if args.stage in ("sections", "jets"):
        raise ValueError("Reuse the completed D85 sections/jets; no remote repetition is needed")
    driver.run, driver.check_run = remote_run, check_run
    for filename in driver.HARDCODED:
        driver.generated_python(filename)
    filename, output = driver.STAGES[args.stage]
    target = driver.generated_python(filename) if filename in driver.HARDCODED or filename in driver.CHOICES else PARI / filename
    obj = driver.module("chatelet128_stage", target); driver.configure(obj)
    if args.stage == "divisor":
        obj.divisor(128, False)
    else:
        arguments = []
        if filename in driver.CHOICES:
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
    receipt.write_text(json.dumps({"status": "pass", "milestone": "D86", "stage": args.stage,
        "precision_digits": 128, "execution_host": "chatelet.mit.edu",
        "per_job_wall_limit_seconds": 1800, "per_job_memory_limit_bytes": 8000000000,
        "sources": [checks.source(p) for p in sorted(set(driver.PROCESS_SOURCES+[
            snapshot(), Path(driver.__file__), Path(transport.__file__), root, result]), key=str)],
        "previous_certificates_unmodified": True}, indent=2)+"\n")
    print("PASS|300_CHATELET_PRECISION128_STAGE", args.stage, flush=True)


if __name__ == "__main__":
    try:
        main()
    except PreparedOnly:
        pass
