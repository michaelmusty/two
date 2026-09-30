#!/usr/bin/env python3
"""Verify the retained D133 transfer payloads without running mathematical jobs.

Paths in this inventory are relative to the checkout. Historical certificates
and receipts retain their original absolute paths and are never rewritten.
This checks transferred bytes, not mathematical correctness or executability.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = "dembele/checkpoints/d133-transfer-2026-09-30.json"


def verify(root, manifest):
    failures = []
    total = 0
    seen = set()
    for record in manifest["files"]:
        name = record["path"]
        path = (root / name).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(root) or name in seen:
            failures.append(f"invalid or duplicate path: {name}")
            continue
        seen.add(name)
        if not path.is_file():
            failures.append(f"missing: {name}")
            continue
        if path.stat().st_size != record["bytes"]:
            failures.append(f"size mismatch (run git lfs pull if needed): {name}")
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            while chunk := stream.read(1 << 20):
                digest.update(chunk)
        if digest.hexdigest() != record["sha256"]:
            failures.append(f"SHA-256 mismatch: {name}")
            continue
        total += record["bytes"]
    if len(manifest["files"]) != manifest["file_count"]:
        failures.append("manifest file count mismatch")
    if not failures and total != manifest["total_bytes"]:
        failures.append("manifest byte count mismatch")
    return failures, total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root / args.manifest).read_text())
    failures, total = verify(root, manifest)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(f"PASS: {manifest['file_count']} retained files, {total:,} bytes; all SHA-256 hashes match.")
    print("Transfer integrity only; see CHECKPOINT.md before resuming computation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
