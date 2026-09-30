"""D86: isolated Chatelet Magma worker with per-job CPU/wall/memory bounds."""
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


def main():
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    directory = spec_path.parent
    assert not (directory / "started.json").exists(), "Do not relaunch a recorded job"
    assert not (directory / "status.json").exists()
    for name, digest in spec["inputs"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    command = ["/usr/local/bin/magma", "-bn", "-l", str(spec["memory_limit_bytes"]), spec["wrapper"]]
    started = time.monotonic()
    (directory / "started.json").write_text(json.dumps({"pid": os.getpid(), "epoch": time.time(),
        "command": command, "input_hashes_verified": True})+"\n")

    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (spec["timeout_seconds"], spec["timeout_seconds"]+5))

    log_path = directory / "output.log"
    with log_path.open("w") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   stdin=subprocess.DEVNULL, start_new_session=True, preexec_fn=limits)
        (directory / "magma.pid").write_text(str(process.pid)+"\n")
        timed_out = False
        try:
            exit_code = process.wait(timeout=spec["timeout_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            exit_code = process.wait()
    raw = log_path.read_bytes()
    text = raw.decode()
    marker, expected = spec["marker"], spec["expected_failure"]
    status = "failed"
    errors = ("Runtime error", "User error", "Assertion failed", "Error:", "Traceback (most recent call last)")
    if timed_out or exit_code == -signal.SIGXCPU:
        status = "timeout"
    elif expected is None:
        if exit_code == 0 and marker in text and not any(s in text for s in errors):
            status = "pass"
    elif exit_code != 0 and expected in text and "Assertion failed" in text and marker not in text:
        status = "pass"
    result = {"status": status, "exit_code": exit_code,
        "wall_seconds": time.monotonic()-started,
        "timeout_seconds": spec["timeout_seconds"], "memory_limit_bytes": spec["memory_limit_bytes"],
        "maximum_resident_bytes": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024,
        "timeout_terminates_process_group": True, "private_process_group": process.pid,
        "input_hashes_verified": True, "output_bytes": len(raw),
        "output_sha256": hashlib.sha256(raw).hexdigest(), "command": command}
    temporary = directory / "status.tmp"
    temporary.write_text(json.dumps(result, indent=2)+"\n")
    temporary.rename(directory / "status.json")


if __name__ == "__main__":
    main()
