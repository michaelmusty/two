// D85 redirected loads; original SHA256 a7858500b1eca5220147f14dbd7bad24c05e8f3eb0edcb3266fc3a556dac1128
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
// H = pi*(div(X16)) + R_ram + 2*P = K_X + 2*P, degree 80.
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m";
can1:=RFromNative(Transpose(Matrix(AG,[pt[1..16]:pt in liftpts[1..1024]])));
D17ev:=RFromNative(Matrix(AG,[[&+[row[j]*pt[pairs[j][1]]*pt[pairs[j][2]]:j in [1..136]]:pt in liftpts[1..1024]]:row in D17_extra_rows]));
assert Rank(RReduce(D17ev)) eq 28;
pt0:=[ZZ!x:x in P32_coordinates]; pt0:=[x*pt0[16]^-1:x in pt0];
values:=RBase(Matrix(ZZ,28,1,[&+[row[j]*pt0[pairs[j][1]]*pt0[pairs[j][2]]:j in [1..136]]:row in D17_extra_rows]));
B2ker:=RKernelRelaxed(values); assert Nrows(B2ker[1]) eq 27;
assert RIsZero(RMultiply(B2ker,values));
B2quadrics:=RMultiply(B2ker,D17ev);
Ueven:=RProduct(B2quadrics,can1,57);
Uodd:=RProduct(RRows(RG1,[46..81]),can1,66);
U0:=RJoin(Ueven,Uodd); assert Rank(RReduce(U0)) eq 123;
Uc:=RCoordinates(RG2,U0);
jetconditions:=RMultiply(Uc,RCols(chartjets,[1..3]));
assert RIsZero(RCols(jetconditions,[1]));
UK:=RKernelRelaxed(jetconditions); assert Nrows(UK[1]) eq 121;
assert RIsZero(RMultiply(UK,jetconditions));
UH:=RMultiply(UK,U0); UHc:=RNormalize(RCoordinates(RG2,UH));
oldC:=RBase(Matrix(ZZ,pointed_cubic_descended_divisor_coordinates));
oldW:=RMultiply(oldC,RG2); found:=false;
for trial in [1..16] do
    gc:=RMultiply(RBaseRow([Integers()!Random(GF(31)):i in [1..81]]),oldC);
    g:=RMultiply(gc,RG2);
    N:=RQuotient(oldW,RScaleRows(RG2,g),RG2,81);
    nc:=RCoordinates(RG2,N);
    conditions:=RMultiply(N,REquations(UH));
    line:=RKernelRelaxed(conditions);
    assert RIsZero(RMultiply(line,conditions));
    if Nrows(line[1]) eq 1 then found:=true; break; end if;
end for;
assert found;
rc:=RNormalize(RMultiply(line,nc)); r:=RMultiply(rc,RG2);
WR:=RQuotient(N,RScaleRows(RG2,r),RG2,81);
WRcoords:=RNormalize(RCoordinates(RG2,WR)); assert WRcoords[2] eq 0;
WR:=RMultiply(WRcoords,RG2);
assert RFrob(WR,ff) eq WR;
assert REqual(RCols(WR,[1..640]),RCols(oldW,[1..640]),RV2);
assert Rank(RReduce(RJoin(RProduct(WR,RG1,201),WB3))) eq 321;
Wjets:=RMultiply(WRcoords,chartjets);
assert RIsZero(RCols(Wjets,[1..3])) and not RIsZero(RCols(Wjets,[4]));
print "PASS|UNIQUE_ADJOINT_REPRESENTATIVE_KX_PLUS_TWO_P";

printf "CHECKPOINT_DIVISOR_COORDINATES|%o\n",BaseCoefficients(WRcoords);
printf "CHECKPOINT_MOVE_G_COEFFICIENTS|%o\n",BaseCoefficients(gc)[1];
printf "CHECKPOINT_MOVE_R_COEFFICIENTS|%o\n",BaseCoefficients(rc)[1];
printf "CHECKPOINT_FIXED_SPACE_COORDINATES|%o\n",BaseCoefficients(UHc);
printf "CHECKPOINT_Q_COEFFICIENTS|%o\n",BaseCoefficients(qcoeff)[1];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|262_ADJOINT_FIRST";quit;
