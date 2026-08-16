"""Read-only survey of the chatelet gate-1 scan after a credential outage.

Answers, in order: does the key work; do the project files still exist; which
lanes are alive (uid-filtered, identified by LANE= in /proc/PID/environ, per
D18 -- never by launch order); what has each lane finished; did anything hit.

Nothing here launches or kills a job. Relaunch with restore_scan.py once the
survey looks sane, and harvest finished rationals into the script's DONE set
before editing it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from remote_magma.cocalc import env, rexec


def sh(conf, cmd, timeout=120):
    return rexec(conf, cmd, timeout=timeout).get("stdout", "").rstrip()


def main():
    conf = env()

    print("== auth")
    print(sh(conf, "id -un; hostname; date -u"))

    print("\n== project files")
    print(sh(conf, "ls -la two_scanjob2/ 2>&1 | head -20"))
    print(sh(conf, "ls -la two_remote_magma/scan2_lane*.out 2>&1 | head -20"))

    print("\n== live lanes (uid-filtered, LANE= from environ)")
    print(sh(conf,
             "for p in $(ps -u $(id -u) -o pid,args | grep 37_levelraise "
             "| grep -v grep | awk '{print $1}'); do "
             "lane=$(tr '\\0' '\\n' < /proc/$p/environ 2>/dev/null | grep ^LANE=); "
             "etime=$(ps -o etime= -p $p); echo \"pid=$p $lane etime=$etime\"; done"))

    print("\n== per-lane progress (last 3 lines each)")
    print(sh(conf,
             "for f in two_remote_magma/scan2_lane*.out; do "
             "echo \"--- $f ($(wc -l < $f) lines, mtime $(date -r $f -u '+%Y-%m-%dT%H:%MZ'))\"; "
             "tail -3 $f; done 2>&1"))

    print("\n== finished rationals per lane (DONE harvest source)")
    print(sh(conf,
             "grep -hoE '(DONE|done|COMPLETED)[^ ]* [0-9]+' two_remote_magma/scan2_lane*.out "
             "2>/dev/null | sort | uniq -c | tail -40"))

    print("\n== hits / errors")
    print(sh(conf,
             "grep -inE 'HIT|a_q0|even|FOUND|error|Runtime' two_remote_magma/scan2_lane*.out "
             "2>/dev/null | tail -30"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
