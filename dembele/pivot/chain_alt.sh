#!/bin/bash
# usage: chain_alt.sh N [FIRST LAST]; control run in prec_Nalt with different auxiliary
# choices: other seed in script 15 (another r, so other T0 and s1-space), other seed and
# other points of fibres 1, 2 for s_A, s_B in script 17.
# r(x) must agree with the standard run (it depends only on x).
N=$1; FIRST=${2:-1}; LAST=${3:-2}
mkdir -p prec_${N}alt; cd prec_${N}alt
for f in state_in.m cubic_in.m ymodel_in.m exact_lists.m padic_lib.m padic_points.m padic_vals.m witt_lib.m hdr12.m cm_frame_curve_candidate.m cm_frame_marks.m makdisi_gen.m 16_lift_Y_padic.m; do ln -sf ../$f .; done
sed -e 's/SetSeed(215)/SetSeed(2215)/' ../15_lift_X_padic.m > 15_lift_X_padic.m
sed -e 's/SetSeed(317)/SetSeed(2317)/' -e 's/^pa := \[fibs\[1\]\[2\], fibs\[1\]\[3\]\]; pb := \[fibs\[2\]\[2\], fibs\[2\]\[3\]\];/pa := [fibs[1][1], fibs[1][3]]; pb := [fibs[2][1], fibs[2][2]];/' ../17_lift_points_padic.m > 17_lift_points_padic.m
PREC=$N OUT=lx_in.m magma -b 15_lift_X_padic.m > s15.out 2>&1
PREC=$N OUT=ly_in.m magma -b 16_lift_Y_padic.m > s16.out 2>&1
PREC=$N VB=../../pivot_tors/vb_0.txt FIRST=$FIRST LAST=$LAST OUT=fx.txt magma -b 17_lift_points_padic.m > s17.out 2>&1
echo CHAIN_DONE >> s17.out
