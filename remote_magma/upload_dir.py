"""Upload a local directory to chatelet as a tarball and unpack it.

Usage:
    python3 remote_magma/upload_dir.py LOCAL_DIR REMOTE_NAME

Creates/replaces the project-relative directory REMOTE_NAME on chatelet with
the contents of LOCAL_DIR (tar.gz, base64-chunked through project_exec, same
transport as cocalc.run_magma_file).
"""
import base64
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from remote_magma.cocalc import env, rexec


def main() -> int:
    local = Path(sys.argv[1]).expanduser().resolve()
    remote_name = sys.argv[2]
    assert local.is_dir(), local
    conf = env()

    with tempfile.NamedTemporaryFile(suffix=".tgz") as tmp:
        subprocess.run(
            ["tar", "czf", tmp.name, "-C", str(local.parent), local.name],
            check=True,
        )
        data = Path(tmp.name).read_bytes()
    print(f"tarball: {len(data)} bytes")
    encoded = base64.b64encode(data).decode()
    token = uuid.uuid4().hex
    rb64 = f"upload_{token}.tgz.b64"
    rtgz = f"upload_{token}.tgz"

    rexec(conf, f"rm -f {rb64}")
    nchunks = (len(encoded) + 63999) // 64000
    for i, offset in enumerate(range(0, len(encoded), 64_000)):
        chunk = encoded[offset : offset + 64_000]
        rexec(conf, f"printf '%s' '{chunk}' >> {rb64}", timeout=300)
        if (i + 1) % 5 == 0 or i + 1 == nchunks:
            print(f"  chunk {i+1}/{nchunks}")
    check = rexec(conf, f"base64 -d {rb64} > {rtgz} && wc -c < {rtgz}", timeout=300)
    got = check.get("stdout", "").strip()
    assert got == str(len(data)), (got, len(data))
    res = rexec(
        conf,
        f"rm -rf {remote_name} && mkdir -p {remote_name}.tmp && "
        f"tar xzf {rtgz} -C {remote_name}.tmp && "
        f"mv {remote_name}.tmp/{local.name} {remote_name} && "
        f"rmdir {remote_name}.tmp && rm -f {rtgz} {rb64} && "
        f"ls {remote_name} | head -5 && du -sh {remote_name}",
        timeout=300,
    )
    print(res.get("stdout", ""))
    print("exit:", res.get("exit_code"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
