#!/bin/bash
cd /Users/musty/two
# candidates: (order gid quo) with a positive-genus intermediate base
for c in "16 6 1" "16 6 2" "32 5 1" "32 8 0" "32 15 0" "32 17 1" "32 17 3"; do
  set -- $c
  sage belyi/export_steps.sage $1 $2 $3 /tmp/b.json >/dev/null 2>&1
  echo -n "[$1,$2] quo$3: "
  STOP_PG=1 julia --project=belyi_jl belyi_jl/tower_solver.jl /tmp/b.json 2>/dev/null | grep -E "PGRUNG" || echo "(no pg rung reached / error)"
done
