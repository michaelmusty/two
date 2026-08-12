#!/usr/bin/env python3
"""Run a Magma certificate and require its explicit PASS marker.

Magma can return process status zero after a source-level runtime error, so process status
alone is not a sufficient test result.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("marker", help="required complete output line, such as PASS|name")
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    result = subprocess.run(
        ["magma", "-b", str(args.script)],
        text=True,
        capture_output=True,
        timeout=args.timeout,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    lines = {*result.stdout.splitlines(), *result.stderr.splitlines()}
    if result.returncode != 0:
        print(f"FAIL|magma_process_status|{result.returncode}", file=sys.stderr)
        return 1
    if args.marker not in lines:
        print(f"FAIL|missing_marker|{args.marker}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
