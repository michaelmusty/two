// D83 checkpoint split of 240_cm_frame_cubic_pointed_direct_function.m; SHA256 51046f3a71cd609bda05b31d7702feceda7f6b20801e517b25c2fa435058a5be
// D82: field-preserving pointed normalization E=80*P32+E40.
SetQuitOnError(true); SetColumns(0); SetSeed(82240); started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/magma/199_cm_frame_cubic_precision_model.m";

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
// The input is the independently certified pointed Newton divisor itself.
WRcoords:=RNormalize(RDecode(precision_third_coordinates)); assert WRcoords[2] eq 0;
assert WRcoords[1]*Matrix(ZZ,pointed_jet2_coefficients) eq 0;
WR:=RMultiply(WRcoords,RG2);
assert RFrob(WR,ff) eq WR;
assert Rank(RReduce(RJoin(RProduct(WR,RG1,201),WB3))) eq 321;
assert IsUnit((qcoeff[1]*Matrix(ZZ,pointed_jet1_coefficients))[1,1]);
print "PASS|CERTIFIED_POINTED_NEWTON_DIVISOR_USED_DIRECTLY";

cubeSpace:=RProduct(RProduct(WR,WR,201),WR,321);
tripleVanishing:=RQuotient(RG2,cubeSpace,RG4,81);
uline:=RIntersection(tripleVanishing,WB4,1);
ucoeff:=RNormalize(RCoordinates(RG4,uline)); assert ucoeff[2] eq 0;
u:=RMultiply(ucoeff,RG4);
normSpace:=RProduct(WR,RTau(WR,tt),201);
ok,f:=RDegreeZero(RG2,normSpace,RG2); assert ok;
fcoeff:=RNormalize(RCoordinates(RG2,f)); assert fcoeff[2] eq 0;
f:=RMultiply(fcoeff,RG2); assert RTau(f,tt) eq f;
ut:=RTau(u,tt); qt:=RTau(q,tt);
normleft:=RScaleRows(u,ut);
normright:=RScaleRows(RScaleRows(RScaleRows(RScaleRows(f,f),f),q),qt);
good:=Min([j:j in [1..1024]|RReduce(RCols(normright,[j]))[1,1] ne 0]);
c:=RMultiply(RCols(normleft,[good]),RInverse(RCols(normright,[good])));
assert c[2] eq 0 and IsUnit(c[1][1,1]);
assert normleft eq RMultiply(c,normright);
assert not RIsZero(RSubtract(RScaleRows(u,qt),RScaleRows(ut,q)));
assert RIsZero(RMultiply(RScaleRows(RG2,u),REquations(cubeSpace)));
assert RIsZero(RMultiply(RScaleRows(RG2,f),REquations(normSpace)));
print "PASS|KUMMER_DIVISOR_AND_NORM_AT_HIGHER_PRECISION";

printf "CHECKPOINT_DESCENDED_DIVISOR_COORDINATES|%o\n",BaseCoefficients(WRcoords);
printf "CHECKPOINT_Q_COEFFICIENTS|%o\n",BaseCoefficients(qcoeff)[1];
printf "CHECKPOINT_U_COEFFICIENTS|%o\n",BaseCoefficients(ucoeff)[1];
printf "CHECKPOINT_F_COEFFICIENTS|%o\n",BaseCoefficients(fcoeff)[1];
printf "CHECKPOINT_NORM_SCALAR|%o\n",Integers()!c[1][1,1];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|262_POINTED_FIRST";quit;
