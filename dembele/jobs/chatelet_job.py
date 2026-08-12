#!/usr/bin/env python3
"""Launch, inspect, and fetch one persistent detached Magma job on chatelet."""

from __future__ import annotations

import argparse
import base64
import re
import shlex
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from remote_magma.cocalc import env, environment_prefix, rexec  # noqa: E402


NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
REMOTE_ROOT = "two_remote_magma/dembele_jobs"
LOCAL_ROOT = ROOT / "dembele" / "data" / "computed" / "jobs"


def paths(name: str) -> dict[str, str]:
    directory = f"{REMOTE_ROOT}/{name}"
    return {
        "directory": directory,
        "script": f"{directory}/job.m",
        "out": f"{directory}/job.out",
        "err": f"{directory}/job.err",
        "exit": f"{directory}/job.exit",
        "pid": f"{directory}/job.pid",
    }


def upload(conf: dict[str, str], name: str, script: Path) -> None:
    remote = paths(name)
    data = script.read_bytes()
    encoded = base64.b64encode(data).decode()
    temporary = remote["script"] + ".b64"
    rexec(
        conf,
        f"mkdir -p {remote['directory']} && rm -f {temporary}",
    )
    for offset in range(0, len(encoded), 64_000):
        chunk = encoded[offset : offset + 64_000]
        rexec(conf, f"printf '%s' '{chunk}' >> {temporary}", timeout=300)
    result = rexec(
        conf,
        f"base64 -d {temporary} > {remote['script']} && "
        f"rm -f {temporary} && wc -c < {remote['script']}",
        timeout=300,
    )
    if result.get("stdout", "").strip() != str(len(data)):
        raise RuntimeError("remote upload size mismatch")


def start(
    conf: dict[str, str],
    name: str,
    script: Path,
    remote_environment: list[str],
) -> None:
    upload(conf, name, script)
    remote = paths(name)
    magma = (
        f"{environment_prefix(remote_environment)}/usr/local/bin/magma "
        f"-b {remote['script']} > {remote['out']} 2> {remote['err']} "
        f"< /dev/null; printf \"%s\\n\" \"$?\" > {remote['exit']}"
    )
    command = (
        f"rm -f {remote['out']} {remote['err']} {remote['exit']} {remote['pid']}; "
        f"nohup bash -c {shlex.quote(magma)} > /dev/null 2>&1 < /dev/null & "
        f"pid=$!; printf '%s\\n' \"$pid\" > {remote['pid']}; echo PID=$pid"
    )
    result = rexec(conf, command, timeout=86_400, sock_timeout=60)
    if result.get("sock_timeout"):
        print("launch response timed out; use status to verify")
    else:
        print(result.get("stdout", "").strip())


def status(conf: dict[str, str], name: str, marker: str | None) -> None:
    remote = paths(name)
    marker_command = ""
    if marker:
        marker_command = (
            f"markers=$(awk -v marker={shlex.quote(marker)} "
            f"'$0 == marker {{n++}} END {{print n+0}}' {remote['out']} "
            f"2>/dev/null); "
        )
    else:
        marker_command = "markers=-; "
    command = (
        f"if [ -f {remote['exit']} ]; then "
        f"code=$(tr -d '\\n' < {remote['exit']}); {marker_command}"
        f"echo 'JOB|done|'\"$code\"'|'\"$markers\"; "
        f"elif [ -f {remote['pid']} ] && "
        f"kill -0 $(tr -d '\\n' < {remote['pid']}) 2>/dev/null; then "
        f"echo 'JOB|running|-|-'; "
        f"else echo 'JOB|missing|-|-'; fi"
    )
    result = rexec(conf, command)
    print(result.get("stdout", ""), end="")


def fetch(conf: dict[str, str], name: str) -> None:
    remote = paths(name)
    local = LOCAL_ROOT / name
    local.mkdir(parents=True, exist_ok=True)
    for key in ("out", "err", "exit"):
        result = rexec(
            conf,
            f"if [ -f {remote[key]} ]; then cat {remote[key]}; fi",
            timeout=300,
            max_output=10_000_000,
        )
        (local / f"job.{key}").write_text(result.get("stdout", ""))
    print(f"fetched to {local}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("start", "status", "fetch"))
    parser.add_argument("name")
    parser.add_argument("script", type=Path, nargs="?")
    parser.add_argument("--marker")
    parser.add_argument(
        "--remote-env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
    )
    args = parser.parse_args()
    if not NAME_PATTERN.fullmatch(args.name):
        parser.error("name may contain only letters, numbers, dot, underscore, and dash")
    if args.command == "start" and args.script is None:
        parser.error("start requires a Magma script path")

    conf = env()
    if args.command == "start":
        start(conf, args.name, args.script, args.remote_env)
    elif args.command == "status":
        status(conf, args.name, args.marker)
    else:
        fetch(conf, args.name)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
