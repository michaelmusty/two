#!/bin/bash
# usage: full.sh N ; scripts 15, 16 (unless prec_N/ly_in.m is complete), then script 17 on all records (31 jobs)
N=$1
mkdir -p prec_$N; cd prec_$N
for f in state_in.m cubic_in.m ymodel_in.m exact_lists.m padic_lib.m padic_points.m padic_vals.m witt_lib.m hdr12.m cm_frame_curve_candidate.m cm_frame_marks.m makdisi_gen.m 15_lift_X_padic.m 16_lift_Y_padic.m 17_lift_points_padic.m 18_power_sums_padic.m; do ln -sf ../$f .; done
if ! grep -q ly_LaurHdr ly_in.m 2>/dev/null; then
  PREC=$N OUT=lx_in.m magma -b 15_lift_X_padic.m > s15.out 2>&1
  PREC=$N OUT=ly_in.m magma -b 16_lift_Y_padic.m > s16.out 2>&1
fi
for k in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  for a in 1 129; do
    b=$((a+127))
    PREC=$N VB=../../pivot_tors/vb_$k.txt FIRST=$a LAST=$b OUT=fx_${k}_$a.txt nohup magma -b 17_lift_points_padic.m > s17_${k}_$a.out 2>&1 &
  done
done
PREC=$N VB=../../pivot_tors/vb_15.txt FIRST=1 LAST=15 OUT=fx_15_1.txt nohup magma -b 17_lift_points_padic.m > s17_15_1.out 2>&1 &
wait
LIST=$(ls fx_*_*.txt | tr '\n' ',' | sed 's/,$//')
PREC=$N LIST=$LIST KMAX=3 magma -b 18_power_sums_padic.m > s18.out 2>&1
echo FULL_DONE >> s18.out
