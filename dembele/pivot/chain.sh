#!/bin/bash
# usage: chain.sh N [FIRST LAST]; runs scripts 15, 16, 17 at precision N in directory prec_N
N=$1; FIRST=${2:-1}; LAST=${3:-2}
mkdir -p prec_$N; cd prec_$N
for f in state_in.m cubic_in.m ymodel_in.m exact_lists.m padic_lib.m padic_points.m padic_vals.m witt_lib.m hdr12.m cm_frame_curve_candidate.m cm_frame_marks.m makdisi_gen.m 15_lift_X_padic.m 16_lift_Y_padic.m 17_lift_points_padic.m; do ln -sf ../$f .; done
PREC=$N OUT=lx_in.m magma -b 15_lift_X_padic.m > s15.out 2>&1
PREC=$N OUT=ly_in.m magma -b 16_lift_Y_padic.m > s16.out 2>&1
PREC=$N VB=../../pivot_tors/vb_0.txt FIRST=$FIRST LAST=$LAST OUT=fx.txt magma -b 17_lift_points_padic.m > s17.out 2>&1
echo CHAIN_DONE >> s17.out
