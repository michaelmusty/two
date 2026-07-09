#!/bin/bash
cd /Users/musty/two
RES=/tmp/pgresults.txt; : > $RES
for c in "32 15 0" "32 17 3" "32 5 1" "32 8 0" "32 17 1"; do
  set -- $c
  sage belyi/export_steps.sage "$1" "$2" "$3" /tmp/b_$1_$2_$3.json >/dev/null 2>&1
  out=$(STOP_PG=1 julia --project=belyi_jl belyi_jl/tower_solver.jl /tmp/b_$1_$2_$3.json 2>/dev/null | grep -E "PGRUNG|MISMATCH")
  echo "[$1,$2] quo$3 -> ${out:-ERROR/no-pg}" >> $RES
  echo "DONE [$1,$2] quo$3"
done
echo "ALLDONE"
