"""Self-healing restore for the chatelet scan lanes: environ-census, relaunch
whatever is missing (append mode). Prints one line per action; silent if all 8
lanes are present.

CONCURRENCY (2026-08-17). The census and the relaunch are separate round trips,
so two overlapping invocations -- e.g. the 10-minute watchdog and a hand-run --
both see the same lane missing and both launch it. That happened: lanes 3 and 4
ended up with two processes each, quietly duplicating a 14-20 h prime, which is
the exact waste the self-harvest was introduced to stop. Two guards now:

  * a local flock, so overlapping invocations on this machine serialise;
  * a re-check of the lane immediately before each launch, narrowing the
    remaining window (the watchdog and a run on another machine could still
    race, but nothing here launches from two machines).
"""
import fcntl
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from remote_magma.cocalc import env, rexec

LOCK = Path(__file__).resolve().parent / ".restore_scan.lock"
CENSUS = (
    "for p in $(ps -u $(id -u) -o pid,args | grep 37_levelraise | grep -v grep "
    "| awk '{print $1}'); do "
    "tr '\\0' '\\n' < /proc/$p/environ 2>/dev/null | grep ^LANE=; done"
)


def live_lanes(conf):
    """Lanes currently alive, or None if the census could not be taken.

    A transient API failure must NOT be read as "no lanes are alive" -- that
    would relaunch all eight on top of a healthy fleet. Returning None lets the
    caller skip the pass instead (the host is often loaded enough that SSL reads
    time out; observed 2026-08-23).
    """
    try:
        r = rexec(conf, CENSUS, timeout=120)
    except Exception as exc:
        print(f"census failed ({type(exc).__name__}); skipping this pass")
        return None
    return {int(l.split("=")[1]) for l in r.get("stdout", "").split()
            if l.startswith("LANE=")}


def main():
    lock = open(LOCK, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another restore_scan is running; skipping this pass")
        return 0

    conf = env()
    live = live_lanes(conf)
    if live is None:
        return 0
    missing = sorted(set(range(8)) - live)
    if not missing:
        return 0
    for lane in missing:
        # re-check: the lane may have been launched since the census above
        recheck = live_lanes(conf)
        if recheck is None or lane in recheck:
            print(f"lane {lane} appeared since census (or recheck failed); not launching")
            continue
        rexec(conf,
              f"cd two_remote_magma && HMF_ROOT=../two_hilbertmodularforms "
              f"LANE={lane} NLANES=8 "
              f"nohup /usr/local/bin/magma -b ../two_scanjob2/37_levelraise_lane.m "
              f">> scan2_lane{lane}.out 2>&1 < /dev/null & echo ok",
              timeout=86400 * 3, sock_timeout=60)
        print(f"RESTORED lane {lane}")
        time.sleep(10)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
