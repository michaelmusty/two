"""One-shot transition helper: retire the lane processes that predate a script
change, without discarding any in-flight work.

A lane already running has the old script in memory, so a deploy only takes
effect on restart -- but restarting mid-prime throws away up to 20 h. This
waits until a lane *prints a result* (i.e. is between primes, so a restart
costs nothing) and only then kills it; the watchdog relaunches it fresh on the
new script within its 10-minute cycle.

Targets are recorded as (lane, pid) pairs at startup and matched by BOTH, so a
lane that gets relaunched in the meantime -- new pid -- is never killed by
mistake (the D18 lesson: identify processes, never assume by slot).

    python3 remote_magma/recycle_lanes.py 1,2,3,4,5,6
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from remote_magma.cocalc import env, rexec

POLL = 600


def census(conf):
    """Map lane -> pid for the live lane processes."""
    out = rexec(conf,
                "for p in $(ps -u $(id -u) -o pid,args | grep 37_levelraise "
                "| grep -v grep | awk '{print $1}'); do "
                "lane=$(tr '\\0' '\\n' < /proc/$p/environ 2>/dev/null "
                "| grep ^LANE= | cut -d= -f2); echo \"$lane $p\"; done",
                timeout=120).get("stdout", "")
    live = {}
    for line in out.split("\n"):
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            live[int(parts[0])] = int(parts[1])
    return live


def counts(conf, lanes):
    """Completed-prime count per lane, from its log."""
    out = rexec(conf,
                "cd two_remote_magma && for L in " + " ".join(str(x) for x in lanes) +
                "; do echo \"$L $(grep -c 'Nq=' scan2_lane$L.out 2>/dev/null || echo 0)\"; done",
                timeout=120).get("stdout", "")
    res = {}
    for line in out.split("\n"):
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            res[int(parts[0])] = int(parts[1])
    return res


def main():
    lanes = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else list(range(8))
    conf = env()

    targets = {l: p for l, p in census(conf).items() if l in lanes}
    base = counts(conf, lanes)
    print(f"[recycle] targeting {sorted(targets.items())}, baseline results {base}",
          flush=True)

    while targets:
        time.sleep(POLL)
        try:
            live = census(conf)
            now = counts(conf, list(targets))
        except Exception as exc:                      # transient API failure
            print(f"[recycle] poll failed ({exc}); continuing", flush=True)
            continue

        for lane in sorted(targets):
            pid = targets[lane]
            if live.get(lane) != pid:                 # already gone or replaced
                print(f"[recycle] lane {lane} pid {pid} no longer current; dropping",
                      flush=True)
                del targets[lane]
                continue
            if now.get(lane, 0) > base.get(lane, 0):
                rexec(conf, f"kill {pid}", timeout=60)
                print(f"[recycle] lane {lane} finished a prime; retired pid {pid} "
                      f"-- watchdog will relaunch it on the new script", flush=True)
                del targets[lane]

    print("[recycle] all targeted lanes retired", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
