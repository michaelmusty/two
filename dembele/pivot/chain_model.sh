#!/bin/bash
# usage: chain_model.sh N ; scripts 15, 16 (model of X and Y at 673^N) and 20
# (invariants of the cover Y -> C and their recognition; no torsion points),
# in directory prec_N. Launch from an exec call with a large --timeout.
N=$1
mkdir -p prec_$N; cd prec_$N
for f in state_in.m cubic_in.m ymodel_in.m exact_lists.m padic_lib.m padic_points.m padic_vals.m witt_lib.m hdr12.m cm_frame_curve_candidate.m cm_frame_marks.m makdisi_gen.m 15_lift_X_padic.m 16_lift_Y_padic.m 20_model_invariants.m; do ln -sf ../$f .; done
PREC=$N OUT=lx_in.m magma -b 15_lift_X_padic.m > s15.out 2>&1
PREC=$N OUT=ly_in.m magma -b 16_lift_Y_padic.m > s16.out 2>&1
PREC=$N magma -b 20_model_invariants.m > s20.out 2>&1
echo MODEL_DONE >> s20.out
