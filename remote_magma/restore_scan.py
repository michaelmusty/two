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
    r = rexec(conf, CENSUS, timeout=120)
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
    missing = sorted(set(range(8)) - live_lanes(conf))
    if not missing:
        return 0
    for lane in missing:
        # re-check: the lane may have been launched since the census above
        if lane in live_lanes(conf):
            print(f"lane {lane} appeared since census; not launching")
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
