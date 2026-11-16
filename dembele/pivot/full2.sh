#!/bin/bash
# usage: full2.sh N ; like full.sh but starts the 31 jobs of script 17 twenty seconds apart
# (31 simultaneous loads at N = 213 reached 64 GB and were killed), skips jobs already running.
N=$1; cd prec_$N
for k in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  for a in 1 129; do
    b=$((a+127)); [ $k = 15 ] && [ $a = 129 ] && continue
    pgrep -f "OUTTAG=${k}_$a " > /dev/null && continue
    ps -u $(id -u) -o args | grep -q "[f]x_${k}_$a.txt" && continue
    if [ -f running_${k}_$a ]; then continue; fi
    touch running_${k}_$a
    PREC=$N VB=../../pivot_tors/vb_$k.txt FIRST=$a LAST=$b OUT=fx_${k}_$a.txt nohup magma -b 17_lift_points_padic.m > s17_${k}_$a.out 2>&1 &
    sleep 20
  done
done
wait
LIST=$(ls fx_*_*.txt | tr '\n' ',' | sed 's/,$//')
PREC=$N LIST=$LIST KMAX=3 magma -b 18_power_sums_padic.m > s18.out 2>&1
echo FULL_DONE >> s18.out
