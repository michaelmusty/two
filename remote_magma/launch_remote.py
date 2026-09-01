"""Upload a Magma script to chatelet's two_gate3/ and launch it detached.

Usage: launch_remote.py LOCAL.m ENVSTR OUTFILE CPULIMIT_SECONDS
The job survives the client: `timeout` sets RLIMIT_CPU inherited by the
detached child; the shell exits immediately (`& echo PID`).  Poll OUTFILE.
"""
import base64, sys, uuid
from pathlib import Path

sys.path.insert(0, "/Users/musty/two")
from remote_magma.cocalc import env, rexec

local = Path(sys.argv[1])
envstr = sys.argv[2]
outfile = sys.argv[3]
cpulimit = int(sys.argv[4])
conf = env()

name = local.name
data = local.read_bytes()
enc = base64.b64encode(data).decode()
rb64 = f"two_gate3/up_{uuid.uuid4().hex}.b64"
rexec(conf, f"rm -f {rb64}")
for off in range(0, len(enc), 64_000):
    rexec(conf, f"printf '%s' '{enc[off:off+64_000]}' >> {rb64}", timeout=300)
r = rexec(conf, f"base64 -d {rb64} > two_gate3/{name} && rm -f {rb64} && wc -c < two_gate3/{name}")
assert r.get("stdout", "").strip() == str(len(data)), r
print(f"uploaded {name} ({len(data)} bytes)")

cmd = (
    f"cd two_gate3 && {envstr} "
    f"nohup /usr/local/bin/magma -b {name} > {outfile} 2>&1 < /dev/null & echo PID=$!"
)
res = rexec(conf, cmd, timeout=cpulimit, sock_timeout=60)
print("launch:", res.get("stdout", "").strip() or "(socket timed out; job likely started)")
chk = rexec(conf, f"sleep 3; ps aux | grep '[m]agma -b {name}' | head -2; tail -3 two_gate3/{outfile} 2>/dev/null")
print(chk.get("stdout", ""))
