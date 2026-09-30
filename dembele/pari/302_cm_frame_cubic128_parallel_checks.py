"""D86: pre-run independent frozen cubic checks in two remote lanes.

After every job completes, the original checker assembles its unchanged
report by verifying/reusing the immutable job receipts. No mathematical
assertion or corruption control is changed.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import sys
import threading

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
PARI = ROOT / "dembele/pari"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


remote = module("parallel_checks_remote", PARI / "300_cm_frame_cubic_precision128_chatelet.py")
driver, checks = remote.driver, remote.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=("class", "pointed", "adjoint"), required=True)
    args = parser.parse_args(); family = args.family
    stage = family+"_check"
    receipt = DATA / ("cm_frame_cubic_precision128_chatelet_"+stage+"_receipt.json")
    if receipt.exists():
        record = json.loads(receipt.read_text()); checks.verify_records(record)
        assert record["status"] == "pass"
        print("PASS|302_EXISTING_PARALLEL_CHECKS", family, flush=True); return
    driver.run, driver.check_run = remote.remote_run, remote.check_run
    filename = {"class": "264_cm_frame_cubic_class_checks.py",
                "pointed": "265_cm_frame_cubic_pointed64_check.py",
                "adjoint": "268_cm_frame_cubic_adjoint64_check.py"}[family]
    target = driver.generated_python(filename)
    obj = driver.module("parallel_frozen_checker", target); driver.configure(obj)
    prior = obj.prior
    if family != "class":
        build, stem = obj.build, obj.stem
    n = 128; jobs = []
    if family == "class":
        names = ["cm_frame_cubic_precision_128_sections", "cm_frame_cubic_pointed_128_jets",
                 "cm_frame_cubic_pointed_128_newton_average", "cm_frame_cubic_pointed_128_newton_divisor",
                 "cm_frame_cubic_pointed_64", "cm_frame_cubic_pointed_64_check"]
        paths = [DATA / (name+".json") for name in names]
        records = [json.loads(path.read_text()) for path in paths]
        for record in records: checks.verify_records(record)
        assert records[3]["actual_interpolated_divisor_verified"]
        assert records[3]["data"]["divisor_coordinates"] == records[2]["data"]["average_coordinates"]
        wrapper = "precision_digits := 128;\n" + "".join(prior.loadline(path.with_suffix(".m")) for path in paths[:3])
        wrapper += prior.binding("previous_cubic_", {"modulus": 31**64,
            "descended_divisor_coordinates": records[4]["data"]["descended_divisor_coordinates"]})
        script = ROOT / "dembele/magma/264_cm_frame_cubic_class_checks.m"
        inputs = prior.CORE+[target, Path(__file__)]+paths
        for mode in ("relation", "symmetries"):
            base = DATA / ("cm_frame_cubic_pointed_128_newton_"+mode+"_check")
            jobs.append((script, base, "PASS|264_CM_FRAME_CUBIC_CLASS_CHECKS", inputs,
                         wrapper+f'class_check_mode := "{mode}";\n', None))
        result_path = DATA / "cm_frame_cubic_pointed_128_newton_third.json"
    elif family == "pointed":
        paths, wrapper, previous = build.inputs_and_wrapper(n)
        cubic_path, class_path = stem(n, "_direct").with_suffix(".json"), stem(n, "_newton_third").with_suffix(".json")
        previous_root = stem(64, "_check").with_suffix(".json")
        cubic, cls, prev = [json.loads(p.read_text()) for p in (cubic_path, class_path, previous_root)]
        for record in (cubic, cls, prev): checks.verify_records(record)
        assert cls["actual_divisor_verified"] and cls["three_division_verified"]
        assert cls["frobenius_fixed"] and cls["antiinvariant"]
        assert cubic["data"]["descended_divisor_coordinates"] == cls["data"]["coordinates"]
        wrapper += prior.loadline(cubic_path.with_suffix(".m"))
        inputs = prior.CORE+[target, Path(__file__), Path(build.__file__), Path(build.jets.__file__),
                             previous_root, cubic_path, class_path]+paths
        for label, name, marker in (
            ("geometry", "233_cm_frame_cubic_pointed_geometry_check.m", "PASS|233_CM_FRAME_CUBIC_POINTED_GEOMETRY_CHECK"),
            ("functions", "242_cm_frame_cubic_pointed_direct_function_check.m", "PASS|242_CM_FRAME_CUBIC_POINTED_DIRECT_FUNCTION_CHECK")):
            script = ROOT / "dembele/magma" / name
            jobs.append((script, stem(n, "_direct_"+label+"_check"), marker, inputs, wrapper, None))
        for name, mutation, assertion in (
            ("norm", "pointed_cubic_norm_scalar := (pointed_cubic_norm_scalar+31^127) mod 31^128;", "assert norm_ok;"),
            ("septic", "pointed_cubic_trace_septic_coefficients[1] := (pointed_cubic_trace_septic_coefficients[1]+31^127) mod 31^128;", "assert septic_ok;")):
            jobs.append((script, stem(n, "_direct_"+name+"_control"), marker, inputs, wrapper+mutation+"\n", assertion))
        result_path = stem(n, "_direct_check").with_suffix(".json")
    else:
        paths, wrapper = build.inputs_and_wrapper(n)
        cubic_path = stem(n).with_suffix(".json")
        checks.verify_records(json.loads(cubic_path.read_text()))
        wrapper += prior.loadline(cubic_path.with_suffix(".m"))
        original, scripts = obj.generated()
        inputs = prior.CORE+[target, Path(__file__), Path(build.__file__), original, cubic_path]+paths
        for label, script, marker in zip(("move", "functions"), scripts,
                ("PASS|268_ADJOINT_MOVE_CHECK", "PASS|268_ADJOINT_FUNCTION_CHECK")):
            jobs.append((script, stem(n, "_"+label+"_check"), marker, inputs, wrapper, None))
        for name, mutation, assertion in (
            ("norm", "adjoint_norm_scalar := (adjoint_norm_scalar+31^127) mod 31^128;", "assert norm_ok;"),
            ("trace", "adjoint_trace_quartic_coefficients[1] := (adjoint_trace_quartic_coefficients[1]+31^127) mod 31^128;", "assert trace_ok;")):
            jobs.append((scripts[1], stem(n, "_"+name+"_control"), "PASS|268_ADJOINT_FUNCTION_CHECK",
                         inputs, wrapper+mutation+"\n", assertion))
        result_path = stem(n, "_check").with_suffix(".json")
    # Materialize shared sources serially before independent jobs use them.
    driver.snapshot(); remote.snapshot()
    for script, *_ in jobs:
        driver.magma_source(script, set())
    upload = remote.transport.upload_files
    lock = threading.Lock()
    def serialized_upload(paths):
        with lock:
            return upload(paths)
    remote.transport.upload_files = serialized_upload
    def run(item):
        script, base, marker, inputs, wrapper, expected = item
        return remote.remote_run(script, base, marker, inputs, wrapper, expected_failure=expected)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, item) for item in jobs]
        for future in futures:
            future.result()
    # This is the original checker, including every original report assertion.
    sys.argv = [str(target)]
    obj.main()
    record = json.loads(result_path.read_text()); checks.verify_records(record)
    assert record["status"] == "pass"
    if family == "class":
        assert all(record[key] for key in ("actual_divisor_verified", "three_division_verified", "frobenius_fixed", "antiinvariant"))
    else:
        assert record["independent_verification_completed"]
    report = {"status": "pass", "milestone": "D86", "stage": stage,
        "precision_digits": n, "execution_host": "chatelet.mit.edu", "parallel_remote_lanes": 2,
        "original_checker_unmodified": True,
        "sources": [checks.source(p) for p in sorted(set(driver.PROCESS_SOURCES+[
            Path(__file__), remote.snapshot(), target, result_path]), key=str)]}
    receipt.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|302_PARALLEL_CUBIC_CHECKS", family, flush=True)


if __name__ == "__main__":
    main()
