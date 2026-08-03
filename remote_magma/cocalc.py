#!/usr/bin/env python3
"""Run shell commands and Magma programs on chatelet via CoCalc."""

from __future__ import annotations

import argparse
import base64
import json
import socket
import ssl
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENV_PATH = ROOT / ".env"
REMOTE_DIR = "two_remote_magma"

try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

EXTRA_CA = HERE / "ca_extra.pem"
if EXTRA_CA.is_file():
    SSL_CONTEXT.load_verify_locations(cafile=str(EXTRA_CA))


def env(path: Path = ENV_PATH) -> dict[str, str]:
    """Load the CoCalc connection settings without exporting or printing them."""
    values: dict[str, str] = {}
    if path.is_file():
        for raw_line in path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\"'")

    key = values.get("COCALC_ACCOUNT_API_KEY") or values.get("COCALC_API_KEY")
    project_id = values.get("COCALC_PROJECT_ID")
    base = values.get("COCALC_BASE")
    if not key or not project_id or not base:
        raise RuntimeError(
            f"COCALC_ACCOUNT_API_KEY, COCALC_PROJECT_ID, and COCALC_BASE "
            f"must be set in {path}"
        )
    return {"key": key, "project_id": project_id, "base": base.rstrip("/")}


def rexec(
    conf: dict[str, str],
    command: str,
    *,
    timeout: int = 120,
    max_output: int = 2_000_000,
    sock_timeout: int | None = None,
) -> dict:
    """Execute a shell command through CoCalc's synchronous project API.

    CoCalc also applies ``timeout`` as RLIMIT_CPU. Detached jobs therefore
    need a large timeout, plus a short independent ``sock_timeout``.
    """
    auth = base64.b64encode(f"{conf['key']}:".encode()).decode()
    request = urllib.request.Request(
        f"{conf['base']}/api/v1/project_exec",
        method="POST",
        data=json.dumps(
            {
                "project_id": conf["project_id"],
                "command": command,
                "bash": True,
                "timeout": timeout,
                "max_output": max_output,
                "err_on_exit": False,
            }
        ).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
            "User-Agent": "michaelmusty-two-remote-magma/1",
        },
    )
    try:
        with urllib.request.urlopen(
            request,
            timeout=sock_timeout if sock_timeout is not None else timeout + 60,
            context=SSL_CONTEXT,
        ) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as error:
        detail = error.read()[:500].decode(errors="replace")
        raise RuntimeError(f"CoCalc HTTP {error.code}: {detail}") from error
    except (TimeoutError, socket.timeout):
        if sock_timeout is None:
            raise
        return {
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "sock_timeout": True,
        }

    if result.get("event") == "error":
        raise RuntimeError(f"CoCalc error: {result.get('error')}")
    return result


def run_magma_text(
    conf: dict[str, str], source: str, *, timeout: int = 120
) -> dict:
    """Run a short Magma program without creating a remote file."""
    encoded = base64.b64encode(source.encode()).decode()
    command = (
        f"printf '%s' '{encoded}' | base64 -d | /usr/local/bin/magma -b"
    )
    return rexec(conf, command, timeout=timeout)


def run_magma_file(
    conf: dict[str, str], path: Path, *, timeout: int = 120
) -> dict:
    """Upload one Magma source file in 64 KB chunks, run it, then remove it."""
    data = path.read_bytes()
    encoded = base64.b64encode(data).decode()
    token = uuid.uuid4().hex
    remote_base = f"{REMOTE_DIR}/{token}.m"
    remote_b64 = f"{remote_base}.b64"

    rexec(conf, f"mkdir -p {REMOTE_DIR} && rm -f {remote_b64}")
    for offset in range(0, len(encoded), 64_000):
        chunk = encoded[offset : offset + 64_000]
        rexec(
            conf,
            f"printf '%s' '{chunk}' >> {remote_b64}",
            timeout=300,
        )

    check = rexec(
        conf,
        f"base64 -d {remote_b64} > {remote_base} && wc -c < {remote_base}",
        timeout=300,
    )
    if check.get("stdout", "").strip() != str(len(data)):
        raise RuntimeError(
            "remote upload size mismatch: "
            f"{check.get('stdout', '').strip()!r} != {len(data)}"
        )

    try:
        return rexec(
            conf,
            f"/usr/local/bin/magma -b < {remote_base}",
            timeout=timeout,
        )
    finally:
        rexec(conf, f"rm -f {remote_base} {remote_b64}")


def emit(result: dict) -> int:
    """Print remote output and return a conventional process exit code."""
    if result.get("stdout"):
        print(result["stdout"], end="")
    if result.get("stderr"):
        print(result["stderr"], end="", file=sys.stderr)
    exit_code = result.get("exit_code")
    return int(exit_code) if exit_code is not None else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="remote CPU and synchronous request limit in seconds",
    )
    commands = parser.add_subparsers(dest="mode", required=True)

    shell_parser = commands.add_parser("exec", help="run a remote shell command")
    shell_parser.add_argument("command")

    eval_parser = commands.add_parser("eval", help="run short inline Magma source")
    eval_parser.add_argument("source")

    file_parser = commands.add_parser("run", help="upload and run a Magma file")
    file_parser.add_argument("path", type=Path)

    args = parser.parse_args()
    conf = env()
    if args.mode == "exec":
        result = rexec(conf, args.command, timeout=args.timeout)
    elif args.mode == "eval":
        result = run_magma_text(conf, args.source, timeout=args.timeout)
    else:
        result = run_magma_file(conf, args.path, timeout=args.timeout)
    return emit(result)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
