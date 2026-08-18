#!/bin/sh
# Remote lane supervisor for the gate-1 scan.
#
# WHY THIS EXISTS (2026-08-18).  The lane script now does one prime per process
# and exits (bounding memory, see D20), which made the fleet DEPEND on something
# restarting it.  That something was a watchdog running in the local Claude
# session -- and monitors die when the session closes, so the fleet would drain
# to zero within one prime-time (14-20 h) of the session ending.  This
# supervisor runs ON chatelet, so it survives session close.  It still dies when
# the project restarts (D18); the local watchdog covers that case when a session
# is open, and will also restart this supervisor.
#
#   start:  setsid nohup flock -n ~/two_scanjob2/.sup.lock \
#             sh ~/two_scanjob2/supervise.sh >> ~/two_remote_magma/supervisor.log 2>&1 &
#   stop:   touch ~/two_scanjob2/STOP_SUPERVISOR
#
# The flock means a second launch is a no-op rather than a double-launch --
# the D22 lesson, applied at the source this time.

cd "$HOME/two_remote_magma" || exit 1
STOP="$HOME/two_scanjob2/STOP_SUPERVISOR"
NLANES=8

while [ ! -f "$STOP" ]; do
  for L in 0 1 2 3 4 5 6 7; do
    [ -f "$STOP" ] && break
    found=0
    for p in $(ps -u "$(id -u)" -o pid,args | grep 37_levelraise | grep -v grep | awk '{print $1}'); do
      if tr '\0' '\n' < "/proc/$p/environ" 2>/dev/null | grep -q "^LANE=$L\$"; then
        found=1; break
      fi
    done
    if [ "$found" = "0" ]; then
      echo "--- supervisor relaunch lane $L $(date -u +%FT%TZ) ---" >> "scan2_lane$L.out"
      HMF_ROOT=../two_hilbertmodularforms LANE=$L NLANES=$NLANES \
        nohup /usr/local/bin/magma -b ../two_scanjob2/37_levelraise_lane.m \
        >> "scan2_lane$L.out" 2>&1 &
      sleep 15
    fi
  done
  sleep 120
done
echo "supervisor stopped $(date -u +%FT%TZ)" >> "$HOME/two_remote_magma/supervisor.log"
