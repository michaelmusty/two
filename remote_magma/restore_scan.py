"""Self-healing restore for the chatelet scan lanes: environ-census, relaunch
whatever is missing (append mode). Prints one line per action; silent if all 8
lanes are present."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from remote_magma.cocalc import env, rexec

def main():
    conf = env()
    r = rexec(conf,
        "for p in $(ps -u $(id -u) -o pid,args | grep 37_levelraise | grep -v grep | awk '{print $1}'); do "
        "tr '\\0' '\\n' < /proc/$p/environ 2>/dev/null | grep ^LANE=; done",
        timeout=120)
    have = {int(l.split("=")[1]) for l in r.get("stdout","").split() if l.startswith("LANE=")}
    missing = sorted(set(range(8)) - have)
    if not missing:
        return 0
    for lane in missing:
        rexec(conf,
            f"cd two_remote_magma && HMF_ROOT=../two_hilbertmodularforms LANE={lane} NLANES=8 "
            f"nohup /usr/local/bin/magma -b ../two_scanjob2/37_levelraise_lane.m "
            f">> scan2_lane{lane}.out 2>&1 < /dev/null & echo ok", timeout=86400*3, sock_timeout=60)
        print(f"RESTORED lane {lane}")
        time.sleep(10)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
