#!/bin/bash
# usage: rerun_job.sh N K A ; reruns records A..A+127 of vb_K as 16 jobs of 8 records
# (outputs fx_Kr_<a>.txt), then script 18 on all complete files -> s18b.out.
N=$1; k=$2; A=$3; cd prec_$N
for i in $(seq 0 15); do
  a=$((A+8*i)); b=$((a+7))
  PREC=$N VB=../../pivot_tors/vb_$k.txt FIRST=$a LAST=$b OUT=fx_${k}r_$a.txt nohup magma -b 17_lift_points_padic.m > s17_${k}r_$a.out 2>&1 &
  sleep 20
done
wait
LIST=$(ls fx_*_*.txt | grep -v "^fx_${k}_$A.txt$" | tr '\n' ',' | sed 's/,$//')
PREC=$N LIST=$LIST KMAX=3 magma -b 18_power_sums_padic.m > s18b.out 2>&1
echo FULL_DONE >> s18b.out
