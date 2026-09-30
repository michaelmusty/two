"""Run or collect the actual divisor, lifting and evaluation controls.

Build first with build_lifttors.py. A successful job must contain its PASS
marker, one JSON record and no GP error. A recorded genus-64 lifting
failure makes this runner exit with code 1.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = HERE.parent / "data/computed"
VENDOR = HERE.parent / "vendor/LiftTors"
GP = "/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/10.6/local/bin/gp"
JOBS = [
    ("q8", "100_lifttors_control.gp", "lifttors_q8_control.out"),
    ("validator", "102_lifttors_validation.gp", "lifttors_validation.out"),
    ("lift_validator", "103_lifttors_lift_validation.gp", "lifttors_lift_validation.out"),
    ("kernel_validator", "104_lifttors_kernel_validation.gp", "lifttors_kernel_validation.out"),
    ("genus16", "101_lifttors_scale.gp", "lifttors_g16_scale.out"),
    ("genus64", "101_lifttors_scale.gp", "lifttors_g64_scale.out"),
]


def source(path):
    path = Path(path)
    return {"path":str(path.relative_to(ROOT)),
            "sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_log(text, marker):
    if marker not in text or "at top-level:" in text or "skipping file" in text:
        raise ValueError(f"GP control failed or incomplete: expected {marker}")
    records = [json.loads(line[5:]) for line in text.splitlines() if line.startswith("DATA|")]
    if len(records) != 1:
        raise ValueError("Expected one DATA record")
    return records[0]


def run_job(gp, script, path, prelude, timeout):
    command = [gp,"-q","-f","-s","512M","-D","parisizemax=2G"]
    commands = prelude+f"read({json.dumps(str(HERE/script))});\n"
    with path.open("w") as log:
        start = time.monotonic()
        process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True,
            cwd=VENDOR, stdout=log, stderr=subprocess.STDOUT,
            env={**os.environ, "LIFTTORS_TRACE":"1"}, start_new_session=True)
        try:
            process.communicate(commands, timeout=timeout)
        except subprocess.TimeoutExpired:
            # Kill the whole local job, including any descendants.
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            log.write(f"\nFAILURE|timeout_seconds={timeout}\n")
            raise SystemExit(f"Job exceeded {timeout}s and was stopped; see {path}")
        log.write(f"\nRESOURCE|wall_seconds={time.monotonic()-start:.3f}\n")
    if process.returncode:
        raise SystemExit(f"Job exited {process.returncode}; see {path}")


def memory_diagnostics():
    result = {}
    for name, filename in [
        ("eager_products", "lifttors_g64_eager_d63.out"),
        ("streamed_products_only", "lifttors_g64_streamed_probe.out"),
        ("streamed_products_and_batched_kernel", "lifttors_g64_scale.out"),
    ]:
        path = DATA/filename
        if not path.exists():
            continue
        contents = path.read_text()
        result[name] = {
            "source":source(path),
            "stack_overflow":"the PARI stack overflows" in contents,
            "complete_control_pass":"PASS|101_lifttors_scale" in contents,
            "eager_product_checkpoints":[
                {"count":int(n),"stack_bytes_relative_to_lift_entry":int(b)}
                for n,b in re.findall(r"TRACE\|eager_v0\|count=(\d+)\|stack_bytes=(\d+)",contents)],
            "lifting_systems":[
                {"rows":int(m),"columns":int(n),"stack_bytes_relative_to_lift_entry":int(b)}
                for m,n,b in re.findall(r"TRACE\|lift_system\|rows=(\d+)\|columns=(\d+)\|stack_bytes=(\d+)",contents)],
            "kernel_checks":[
                {"rank":int(r),"nullity":int(n),"rows":int(m)}
                for r,n,m in re.findall(r"TRACE\|lift_kernel_basis\|rank=(\d+)\|nullity=(\d+)\|rows=(\d+)",contents)],
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", default=GP)
    parser.add_argument("--collect", action="store_true", help="collect existing control logs")
    parser.add_argument("--timeout", type=int, default=900, help="per-process timeout in seconds, including independent checks")
    args = parser.parse_args()
    reports = {}
    paths = [Path(__file__), HERE/"build_lifttors.py", HERE/"lifttors_bounded.c",
             HERE/"lifttors_lift.py", HERE/"lifttors_streamed.c",
             DATA/"lifttors_q8_control.bin"]
    for name, script, output in JOBS:
        path = DATA/output
        if not args.collect:
            prelude = "bench_genus=16;" if name=="genus16" else ""
            run_job(args.gp, script, path, prelude, args.timeout)
        contents = path.read_text()
        try:
            reports[name] = parse_log(contents,"PASS|"+Path(script).stem)
        except ValueError:
            # A measured larger failure is a result, never a passing test.
            if name!="genus64" or "PicLiftTors: the PARI stack overflows" not in contents:
                raise
            reports[name] = {
                "status":"FAILED: PARI stack overflow in PicLiftTors",
                "genus":64,"d0":129,"p":97,"a":2,"precision_exponent":4,
                "minimum_evaluation_points":646,
                "stack_limit_bytes":int(re.findall(r"current stack size: (\d+)",contents)[-1]),
                "initialization_and_doubling_check_completed":
                    "STAGE|doubling_checked" in contents,
                "lift_completed":False,
                "timing_ms":None,
            }
        rss = re.findall(r"(\d+)\s+maximum resident set size", contents)
        if rss:
            reports[name]["maximum_resident_set_bytes"] = int(rss[-1])
        wall = re.findall(r"RESOURCE\|wall_seconds=([\d.]+)", contents)
        if wall:
            reports[name]["wall_seconds"] = float(wall[-1])
        paths += [HERE/script,path]
        print(f"{name}: {reports[name].get('status', 'PASS')}; {reports[name].get('timing_ms')}")
    build_path = HERE/".build/lifttors/build.json"
    build = json.loads(build_path.read_text())
    assert build["compiled_adaptation"]=="exact batched DivSub_dimval; streamed PicLiftTors products; batched lifting kernel"
    assert build["adapter_sha256"]==source(HERE/"lifttors_bounded.c")["sha256"]
    for name, digest in build["lift_adapter_sha256"].items():
        assert digest == source(HERE/name)["sha256"]
    reports["backend"] = build
    reports["memory_diagnostics"] = memory_diagnostics()
    reports["execution_policy"] = {
        "initial_pari_stack":"512M", "maximum_pari_stack":"2G",
        "per_process_timeout_seconds":args.timeout,
        "memory_checkpoints_are_peak_rss":False,
    }
    reports["pari_version"] = subprocess.check_output([args.gp,"--version-short"],text=True).strip()
    reports["sources"] = [source(p) for p in paths]
    reports["scope"] = {
        "known_q8_torsion_field_recovered":"Q(i)",
        "generic_divisor_backend_exercised":True,
        "padic_lifting_and_evaluation_exercised":True,
        "genus64_control_is_target_Y":False,
        "genus64_lift_succeeded":reports["genus64"].get("lift_completed",True),
        "target_residue_degree_51_benchmarked":False,
        "target_arithmetic_sections_available":False,
        "target_polynomial_obtained":False,
    }
    text = json.dumps(reports,indent=2)+"\n"
    (DATA/"lifttors_controls.json").write_text(text)
    print(DATA/"lifttors_controls.json")
    if not reports["scope"]["genus64_lift_succeeded"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
