#!/usr/bin/env python3
"""Manage the eight detached chatelet constituent-orbit lanes."""

from __future__ import annotations

import argparse
import base64
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from remote_magma.cocalc import env, rexec  # noqa: E402


LOCAL_SCRIPT = ROOT / "dembele" / "magma" / "12_constituent_orbit_job.m"
LOCAL_RESULTS = ROOT / "dembele" / "data" / "computed" / "constituent_lanes"
REMOTE_DIR = "two_remote_magma/dembele_constituents"
REMOTE_SCRIPT = f"{REMOTE_DIR}/constituent_orbit_job.m"
HMF_ROOT = "two_hilbertmodularforms"


def upload(conf: dict[str, str]) -> None:
    data = LOCAL_SCRIPT.read_bytes()
    encoded = base64.b64encode(data).decode()
    remote_b64 = REMOTE_SCRIPT + ".b64"
    rexec(conf, f"mkdir -p {REMOTE_DIR} && rm -f {remote_b64}")
    for offset in range(0, len(encoded), 64_000):
        chunk = encoded[offset : offset + 64_000]
        rexec(conf, f"printf '%s' '{chunk}' >> {remote_b64}", timeout=300)
    result = rexec(
        conf,
        f"base64 -d {remote_b64} > {REMOTE_SCRIPT} && "
        f"rm -f {remote_b64} && wc -c < {REMOTE_SCRIPT}",
        timeout=300,
    )
    remote_size = result.get("stdout", "").strip()
    if remote_size != str(len(data)):
        raise RuntimeError(f"upload size mismatch: {remote_size!r} != {len(data)}")
    print(f"uploaded {len(data)} bytes to {REMOTE_SCRIPT}")


def start_lane(conf: dict[str, str], lane: int) -> None:
    prefix = f"{REMOTE_DIR}/lane_{lane}"
    inner = (
        f"env HMF_ROOT={HMF_ROOT} ORBIT_INDEX={lane} "
        f"/usr/local/bin/magma -b {REMOTE_SCRIPT} "
        f"> {prefix}.out 2> {prefix}.err < /dev/null; "
        f"printf \"%s\\n\" \"$?\" > {prefix}.exit"
    )
    command = (
        f"rm -f {prefix}.out {prefix}.err {prefix}.exit {prefix}.pid; "
        f"nohup bash -c '{inner}' > /dev/null 2>&1 < /dev/null & "
        f"pid=$!; printf '%s\\n' \"$pid\" > {prefix}.pid; echo PID=$pid"
    )
    result = rexec(conf, command, timeout=86_400, sock_timeout=60)
    if result.get("sock_timeout"):
        print(f"lane {lane}: launch response timed out; status check required")
    else:
        print(f"lane {lane}: {result.get('stdout', '').strip()}")


def start(conf: dict[str, str]) -> None:
    upload(conf)
    for lane in range(1, 9):
        start_lane(conf, lane)


def status(conf: dict[str, str]) -> tuple[int, int]:
    commands = []
    for lane in range(1, 9):
        prefix = f"{REMOTE_DIR}/lane_{lane}"
        commands.append(
            f"if [ -f {prefix}.exit ]; then "
            f"code=$(tr -d '\\n' < {prefix}.exit); "
            f"passes=$(awk '/^PASS\\|constituent_orbit\\|/ {{n++}} END {{print n+0}}' "
            f"{prefix}.out 2>/dev/null); "
            f"echo 'LANE|{lane}|done|'\"$code\"'|'\"$passes\"; "
            f"elif [ -f {prefix}.pid ] && "
            f"kill -0 $(tr -d '\\n' < {prefix}.pid) 2>/dev/null; then "
            f"echo 'LANE|{lane}|running|-|-'; "
            f"else echo 'LANE|{lane}|missing|-|-'; fi"
        )
    result = rexec(conf, "; ".join(commands))
    output = result.get("stdout", "")
    print(output, end="")
    done = 0
    passed = 0
    for line in output.splitlines():
        fields = line.split("|")
        if len(fields) == 5 and fields[0] == "LANE" and fields[2] == "done":
            done += 1
            if fields[3] == "0" and fields[4] == "1":
                passed += 1
    return done, passed


def fetch(conf: dict[str, str]) -> None:
    LOCAL_RESULTS.mkdir(parents=True, exist_ok=True)
    for lane in range(1, 9):
        prefix = f"{REMOTE_DIR}/lane_{lane}"
        for suffix in ("out", "err", "exit"):
            result = rexec(
                conf,
                f"if [ -f {prefix}.{suffix} ]; then cat {prefix}.{suffix}; fi",
                timeout=300,
                max_output=10_000_000,
            )
            (LOCAL_RESULTS / f"lane_{lane}.{suffix}").write_text(
                result.get("stdout", "")
            )
    print(f"fetched lane outputs to {LOCAL_RESULTS}")


def run(conf: dict[str, str], poll_seconds: int) -> None:
    start(conf)
    while True:
        time.sleep(poll_seconds)
        done, passed = status(conf)
        if done == 8:
            fetch(conf)
            if passed != 8:
                raise RuntimeError(f"only {passed}/8 lanes passed")
            return


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("upload", "start", "status", "fetch", "run"))
    parser.add_argument("--poll", type=int, default=120)
    args = parser.parse_args()
    conf = env()

    if args.command == "upload":
        upload(conf)
    elif args.command == "start":
        start(conf)
    elif args.command == "status":
        status(conf)
    elif args.command == "fetch":
        fetch(conf)
    else:
        run(conf, args.poll)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
