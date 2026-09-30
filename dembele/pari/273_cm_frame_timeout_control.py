"""Regression test: a timed-out Sage job must not leave a child writing later."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("timeout_control_runner", ROOT / "dembele/pari/272_cm_frame_bounded_jobs.py")
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)


def main():
    env = dict(os.environ, DOT_SAGE="/private/tmp/dembele_pointed_recognition_sage")
    with tempfile.TemporaryDirectory(prefix="dembele_timeout_control_", dir="/private/tmp") as tmp:
        flag = Path(tmp) / "late_child_write"
        child = "import time; time.sleep(2); open("+repr(str(flag))+", 'w').write('late'); print('LATE_CHILD_OUTPUT', flush=True)"
        parent = "import os,subprocess,sys,time; print('START_GROUP',os.getpgrp(),flush=True); subprocess.Popen([sys.executable,'-c',"+repr(child)+"]); time.sleep(10)"
        log = DATA / "cm_frame_bounded_sage_timeout_control.out"
        timed = runner.run_job([runner.SAGE, "-python", "-c", parent], log, 1, "UNREACHED_COMPLETION", env=env)
        assert timed["status"] == "timeout"
        assert "START_GROUP "+str(timed["private_process_group"]) in log.read_text()
        captured = timed["log"]["sha256"]
        time.sleep(2.3)
        assert not flag.exists() and "LATE_CHILD_OUTPUT" not in log.read_text()
        assert hashlib.sha256(log.read_bytes()).hexdigest() == captured
    positive = runner.run_job([runner.SAGE, "-python", "-c", "print('PASS|BOUNDED_SAGE_POSITIVE')"],
        DATA / "cm_frame_bounded_sage_positive.out", 10, "PASS|BOUNDED_SAGE_POSITIVE", env=env)
    assert positive["status"] == "pass"
    report = {"status": "pass", "milestone": "D83", "date": "2026-09-22",
        "sources": [runner.source(Path(__file__)), runner.source(Path(runner.__file__))],
        "timeout_case": timed, "positive_case": positive,
        "sage_worker_in_private_process_group": True, "descendant_late_write_prevented": True,
        "log_hash_stable_after_child_write_deadline": True}
    (DATA / "cm_frame_bounded_sage_timeout_control.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|273_CM_FRAME_TIMEOUT_CONTROL", flush=True)


if __name__ == "__main__":
    main()
