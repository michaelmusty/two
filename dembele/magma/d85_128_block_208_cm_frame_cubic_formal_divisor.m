// D85 redirected loads; original SHA256 a205d5dac56b8dbda13db55b0640c78a8180109ddf6b3ec57885880678f61f55
// D82: lift the saved effective divisor by a finite-algebra idempotent.
// This supplies an actual class lift before a short formal-kernel correction.
SetQuitOnError(true); SetColumns(0); SetSeed(82208); started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/magma/294_cm_frame_block_model.m";
oldC:=Matrix(kk,previous_cubic_descended_divisor_coordinates);
oldW:=oldC*RReduce(RG2); oldG1:=RReduce(RG1); oldG2:=RReduce(RG2); oldG3:=RReduce(RG3);
// A coefficient lift of C is used only to choose one genuine global section g.
// Its row space is NOT assumed to define a divisor at the new precision.
naiveC:=RBase(Matrix(ZZ,previous_cubic_descended_divisor_coordinates));
found:=false;
for trial in [1..32] do
    gcoeff:=RMultiply(RBaseRow([Integers()!Random(GF(31)):i in [1..81]]),naiveC);
    g:=RMultiply(gcoeff,RG2); g0:=RReduce(g)[1];
    oldN:=QuotientSpace(oldW,ScaleRows(oldG2,g0),oldG2,81);
    oldW3:=ProductSpace(oldW,oldG1,201); oldN3:=ProductSpace(oldN,oldG1,201);
    if Rank(VerticalJoin(oldW3,oldN3)) eq 321 then found:=true; break; end if;
end for;
assert found;
gG1:=RScaleRows(RG1,g); both:=RJoin(gG1,RG3);
selected:=FPivots(Transpose(RReduce(both)));
assert #selected eq 321 and selected[1..81] eq [1..81];
bindices:=[j-81:j in selected[82..321]]; B:=RRows(RG3,bindices);
K3:=RJoin(B,gG1); assert Rank(RReduce(K3)) eq 321;
found:=false;
for trial in [1..128] do
    hcoeff:=RBaseRow([Integers()!Random(GF(31)):i in [1..81]]);
    h:=RMultiply(hcoeff,RG1);
    K4:=RJoin(RScaleRows(B,h),RScaleRows(RG2,g));
    if Rank(RReduce(K4)) eq 441 then found:=true; break; end if;
end for;
assert found;
h3:=RScaleRows(RScaleRows(h,h),h);
K6:=RJoin(RScaleRows(B,h3),RScaleRows(RG4,g));
assert Rank(RReduce(K6)) eq 681;
j6:=FPivots(RReduce(K6)); inv6:=RInverse(RCols(K6,j6));
function ProductInAlgebra(x,y,B,K6,j6,inv6)
    prod:=RScaleRows(RMultiply(x,B),RMultiply(y,B));
    coeff:=RMultiply(RCols(prod,j6),inv6); assert RMultiply(coeff,K6) eq prod;
    return RCols(coeff,[1..240]);
end function;
one:=RCols(RCoordinates(K3,h3),[1..240]); assert one[2] eq 0;
assert ProductInAlgebra(one,one,B,K6,j6,inv6) eq one;
// Chinese remainder on the special fibre: u vanishes on E and u-h^3 on E'.
wc:=Matrix(Basis(RowSpace(Solution(oldG3,oldW3))));
nc:=Matrix(Basis(RowSpace(Solution(oldG3,oldN3))));
assert &and[z^31 eq z:z in Eltseq(wc) cat Eltseq(nc)];
hh:=Solution(oldG3,RReduce(h3)[1]);
uv:=Solution(VerticalJoin(wc,nc),hh);
u0:=(Vector(kk,Eltseq(uv)[1..201])*wc)*oldG3;
e0coeff:=Solution(RReduce(K3),u0);
e:=RLift(Matrix(kk,1,240,Eltseq(e0coeff)[1..240])); assert e[2] eq 0;
known:=1;
while known lt precision_digits do
    e2:=ProductInAlgebra(e,e,B,K6,j6,inv6);
    e3:=ProductInAlgebra(e,e2,B,K6,j6,inv6);
    e:=RSubtract(RScalar(ZZ!3,e2),RScalar(ZZ!2,e3)); known*:=2;
end while;
assert ProductInAlgebra(e,e,B,K6,j6,inv6) eq e and e[2] eq 0;
// 1-e projects to the lifted E summand of O(div(g)), of rank 120.
d:=RSubtract(one,e); deval:=RMultiply(d,B);
multd:=RScaleRows(B,deval);
multcoords:=RMultiply(RCols(multd,j6),inv6);
assert RMultiply(multcoords,K6) eq multd;
Md:=RCols(multcoords,[1..240]); assert Md[2] eq 0;
assert RMultiply(Md,Md) eq Md and Rank(RReduce(Md)) eq 120;
fcoords:=RCols(RCoordinates(K3,RScaleRows(RG2,h)),[1..240]);
conditions:=RMultiply(fcoords,Md);
C:=RNormalize(RKernelRelaxed(conditions));
assert Nrows(C[1]) eq 81 and C[2] eq 0 and RIsZero(RMultiply(C,conditions));
assert [[z mod previous_cubic_modulus:z in row]:row in BaseCoefficients(C)] eq previous_cubic_descended_divisor_coordinates;
W:=RMultiply(C,RG2); assert RFrob(W,ff) eq W;
print "PASS|ACTUAL_DIVISOR_LIFT_BY_IDEMPOTENT";
printf "FORMAL_DIVISOR_COORDINATES|%o\n",BaseCoefficients(C);
printf "FORMAL_G_COEFFICIENTS|%o\n",BaseCoefficients(gcoeff)[1];
printf "FORMAL_H_COEFFICIENTS|%o\n",BaseCoefficients(hcoeff)[1];
printf "FORMAL_QUOTIENT_BASIS_INDICES|%o\n",bindices;
printf "FORMAL_IDEMPOTENT_COEFFICIENTS|%o\n",BaseCoefficients(e)[1];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|208_CM_FRAME_CUBIC_FORMAL_DIVISOR";quit;
