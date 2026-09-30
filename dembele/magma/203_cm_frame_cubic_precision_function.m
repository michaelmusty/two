// D82: normalized cubic at higher precision, preserving every saved lower digit.
SetQuitOnError(true); SetColumns(0); SetSeed(82203); started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
load "dembele/magma/202_cm_frame_cubic_gauge_arithmetic.m";
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
qcoeff:=RMultiply(RBaseRow(gauge_q_free_values),qkernel);
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
moving:=RIntersection(RProduct(WE,Wsigma,201),WB4,81);
movingcoeff:=RNormalize(RCoordinates(RG4,moving));
assert movingcoeff[2] eq 0;
moving:=RMultiply(movingcoeff,RG4);

// Choose the move so its residual divisor reduces to the saved D79 divisor.
// This fixes the old gauge and gives coefficientwise reduction of the cubic.
oldWR:=DecodeOld(kummer_descended_divisor_coordinates,kk)*RReduce(RG2);
oldWR4:=ProductSpace(oldWR,RReduce(RG2),321);
line:=Matrix(Basis(RowSpace(RReduce(moving)) meet RowSpace(oldWR4)));
assert Nrows(line) eq 1;
oldmove:=Solution(RReduce(RG4),line);
piv:=FPivots(oldmove); oldmove:=oldmove*(oldmove[1,piv[1]]^-1);
assert &and[z^31 eq z:z in Eltseq(oldmove)];
move_coeff:=LiftSectionInSpace(movingcoeff,oldmove);
assert move_coeff[2] eq 0;
move:=RMultiply(move_coeff,RG4);
WR:=RQuotient(moving,RScaleRows(RG2,move),RG2,81);
WRcoords:=RNormalize(RCoordinates(RG2,WR)); assert WRcoords[2] eq 0;
WRcoords:=RGaugeNormalize(WRcoords,RG2,gauge_pin_indices,gauge_pin_values);
assert FPivots(RReduce(WRcoords)) eq gauge_divisor_pivots;
WR:=RMultiply(WRcoords,RG2);
assert RowSpace(RReduce(WR)) eq RowSpace(oldWR);
assert Rank(RReduce(RJoin(RProduct(WR,RG1,201),WB3))) eq 321;
assert REqual(RCols(WR,[1..640]),RCols(WE,[1..640]),RV2);
assert RFrob(WR,ff) eq WR;
print "PASS|PERSISTENT_DIVISOR_NORMALIZATION_AT_HIGHER_PRECISION";

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

xs:=[pt[1..16]:pt in liftpts[1..1024]];
C4:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in cubic_quartic_monomials]));
C10:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in cubic_decic_monomials]));
assert Rank(RReduce(C4)) eq 105 and Rank(RReduce(C10)) eq 285;
arow:=RCoordinates(C4,RMultiply(c,f));
denrow:=RCoordinates(C4,RScaleRows(q,qt));
numrow:=RCoordinates(C10,RMultiply(c,RAdd(RScaleRows(u,qt),RScaleRows(ut,q))));
assert [[z mod previous_cubic_modulus:z in row]:row in BaseCoefficients(WRcoords)] eq previous_cubic_descended_divisor_coordinates;
for item in [* <qcoeff,previous_cubic_q_coefficients>, <ucoeff,previous_cubic_u_coefficients>,
    <fcoeff,previous_cubic_f_coefficients>, <arow,previous_cubic_a_coefficients>,
    <denrow,previous_cubic_denominator_coefficients>, <numrow,previous_cubic_trace_numerator_coefficients> *] do
    assert [z mod previous_cubic_modulus:z in BaseCoefficients(item[1])[1]] eq item[2];
end for;
assert (Integers()!c[1][1,1]) mod previous_cubic_modulus eq previous_cubic_norm_scalar;
assert ucoeff[1][1,gauge_u_pivot] eq 1 and fcoeff[1][1,gauge_f_pivot] eq 1;
print "PASS|COEFFICIENTWISE_REDUCTION_TO_PRECEDING_PRECISION";
printf "PRECISION_DESCENDED_DIVISOR_COORDINATES|%o\n",BaseCoefficients(WRcoords);
printf "PRECISION_Q_COEFFICIENTS|%o\n",BaseCoefficients(qcoeff)[1];
printf "PRECISION_U_COEFFICIENTS|%o\n",BaseCoefficients(ucoeff)[1];
printf "PRECISION_F_COEFFICIENTS|%o\n",BaseCoefficients(fcoeff)[1];
printf "PRECISION_NORM_SCALAR|%o\n",Integers()!c[1][1,1];
printf "PRECISION_A_COEFFICIENTS|%o\n",BaseCoefficients(arow)[1];
printf "PRECISION_DENOMINATOR_COEFFICIENTS|%o\n",BaseCoefficients(denrow)[1];
printf "PRECISION_TRACE_NUMERATOR_COEFFICIENTS|%o\n",BaseCoefficients(numrow)[1];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|203_CM_FRAME_CUBIC_PRECISION_FUNCTION";quit;
