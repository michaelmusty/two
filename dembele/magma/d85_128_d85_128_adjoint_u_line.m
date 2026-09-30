// D85 redirected loads; original SHA256 f0e5036fab89f7e4c89f7aa4a38d41698237f99c744ee6226b14bdb83b16e7b6
// D85 checkpoint split of 249_cm_frame_cubic_adjoint_probe.m; SHA256 031cdf67ad52f8bd03207ec538445c1c0d9fad9f4f0d0b58d5473de31c1ac4da
// D82: field-preserving pointed normalization E=80*P32+E40.
SetQuitOnError(true); SetColumns(0); SetSeed(82249); started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/magma/d85_128_199_cm_frame_cubic_precision_model.m";

load "dembele/data/computed/cm_frame_cubic_gauge.m";
function LiftSectionInSpace(B,old)
    coeff:=Solution(RReduce(B),old); assert coeff*RReduce(B) eq old;
    return RMultiply(RLift(coeff),B);
end function;
WE:=RMultiply(RDecode(precision_third_coordinates),RG2);
Wsigma:=RFrob(WE,ff); WE3:=RProduct(WE,RG1,201);
qkernel:=RKernelRelaxed(RBase(Matrix(ZZ,cubic_lift_branch_minus_values)));
assert Nrows(qkernel[1]) eq 72 and qkernel[2] eq 0;
assert RCols(qkernel,gauge_q_free_indices) eq RId(72);
root:=ZZ!11; rootdigits:=1;
while rootdigits lt precision_digits do root-:=(root^2+3)*(2*root)^-1; rootdigits*:=2; end while;
assert root^2 eq -3;
qfree:=[ZZ!gauge_q_free_values[j]*(gauge_q_free_indices[j] le 45 select ZZ!1 else root*(ZZ!11)^-1):j in [1..72]];
qcoeff:=RMultiply(RBaseRow(qfree),qkernel);
assert qcoeff[2] eq 0;
assert &+[qcoeff[1][1,i]*bm1[i]:i in [1..81]] eq 0;
assert IsUnit(&+[qcoeff[1][1,i]*bp1[i]:i in [1..81]]);
q:=RMultiply(qcoeff,RG1); Sminus:=RMultiply(qkernel,RG1);
WQ:=RQuotient(Sminus,RScaleRows(RG2,q),RG2,90);
Qcoeff:=RCoordinates(RG2,WQ);
bconstraints:=RMultiply(Qcoeff,RBplus);
bkernel:=RKernelRelaxed(bconstraints); assert Nrows(bkernel[1]) eq 81;
assert RIsZero(RMultiply(bkernel,bconstraints));
WB:=RMultiply(bkernel,WQ); WB3:=RProduct(WB,RG1,201); WB4:=RProduct(WB,RG2,321);
assert Rank(RReduce(RJoin(WE3,WB3))) eq 321;
load "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m";
WRcoords:=RBase(Matrix(ZZ,checkpoint_divisor_coordinates));
WR:=RMultiply(WRcoords,RG2);
gc:=RBaseRow(checkpoint_move_g_coefficients);
rc:=RBaseRow(checkpoint_move_r_coefficients);
UHc:=RBase(Matrix(ZZ,checkpoint_fixed_space_coordinates));
assert qcoeff eq RBaseRow(checkpoint_q_coefficients);
cubeSpace:=RProduct(RProduct(WR,WR,201),WR,321);
ok,uline:=RDegreeZero(RG2,cubeSpace,WB4); assert ok;
ucoeff:=RNormalize(RCoordinates(RG4,uline)); assert ucoeff[2] eq 0;
u:=RMultiply(ucoeff,RG4);
printf "FUNCTION_DIVISOR_COORDINATES|%o\n",BaseCoefficients(WRcoords);
printf "FUNCTION_MOVE_G_COEFFICIENTS|%o\n",BaseCoefficients(gc)[1];
printf "FUNCTION_MOVE_R_COEFFICIENTS|%o\n",BaseCoefficients(rc)[1];
printf "FUNCTION_FIXED_SPACE_COORDINATES|%o\n",BaseCoefficients(UHc);
printf "FUNCTION_Q_COEFFICIENTS|%o\n",BaseCoefficients(qcoeff)[1];
printf "FUNCTION_U_COEFFICIENTS|%o\n",BaseCoefficients(ucoeff)[1];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|267_ADJOINT_U_LINE";quit;
