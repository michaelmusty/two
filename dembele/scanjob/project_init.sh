#!/bin/bash
# CoCalc project init script -- deployed to ~/project_init.sh on chatelet.
#
# CoCalc runs this at PROJECT START (see doc.cocalc.com/project-init.html), which
# is the one failure mode nothing else covered: the project restarts on an
# hours-scale (D18) and kills the lane supervisor along with every lane, and the
# supervisor cannot restart itself. Before this, recovery needed a live Claude
# session with the watchdog armed; on 2026-08-19 that cost ~6 h of dead scan time.
#
# Contract notes:
#   * CoCalc's Supervisor restarts this script if it exits with anything other
#     than 0 or 2, so it must exit 0 -- launch and get out of the way.
#   * It runs NON-interactively; ~/.bashrc is not sourced. Use absolute paths.
#   * flock makes a duplicate launch a no-op, so this is safe alongside the
#     remote supervisor already running and the local watchdog (D22's lesson).
#
# To disable everything:  touch ~/two_scanjob2/STOP_SUPERVISOR

[ -f "$HOME/two_scanjob2/STOP_SUPERVISOR" ] && exit 0
[ -x /usr/bin/flock ] || exit 0
[ -f "$HOME/two_scanjob2/supervise.sh" ] || exit 0

setsid nohup flock -n "$HOME/two_scanjob2/.sup.lock" \
  sh "$HOME/two_scanjob2/supervise.sh" \
  >> "$HOME/two_remote_magma/supervisor.log" 2>&1 < /dev/null &

exit 0
