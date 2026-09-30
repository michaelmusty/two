"""Run bounded jobs in a private process group, terminating all descendants on timeout.

The older frozen runner kills only the immediate process. A Sage launcher
can leave a Python child running and writing its log after that timeout.
Future bounded Sage jobs should import this runner instead.
"""
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("bounded_jobs_prior", ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py")
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
source, MAGMA, SAGE, ERRORS = prior.source, prior.MAGMA, prior.SAGE, prior.ERRORS


def run_job(command, log_path, timeout, marker, env=None, expected_failure=None):
    log_path = Path(log_path)
    started = time.monotonic()
    status = "failed"; timed_out = False
    with log_path.open("w") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                   env=env, start_new_session=True)
        group = process.pid
        try:
            exit_code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try: os.killpg(group, signal.SIGKILL)
            except ProcessLookupError: pass
            exit_code = process.wait()
            status = "timeout"
    output = log_path.read_text()
    if not timed_out:
        if expected_failure is None:
            if exit_code == 0 and marker in output and not any(e in output for e in ERRORS):
                status = "pass"
        elif exit_code != 0 and expected_failure in output and "Assertion failed" in output and marker not in output:
            status = "pass"
    job = {"command": command, "status": status, "exit_code": exit_code,
           "wall_seconds": time.monotonic()-started, "timeout_seconds": timeout,
           "log": source(log_path), "private_process_group": group,
           "timeout_terminates_process_group": True,
           "sources": [source(Path(__file__)), source(Path(prior.__file__))]}
    if command[0] == MAGMA: job["memory_limit_bytes"] = 2_000_000_000
    return job
