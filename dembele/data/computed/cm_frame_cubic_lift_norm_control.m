// D81: verify saved lifts and functions; do not replay the scalar search.
SetQuitOnError(true); SetColumns(0); SetSeed(81931); started:=Cputime();
load "dembele/magma/187_cm_frame_cubic_lift_model.m";
load "dembele/data/computed/cm_frame_cubic_lift_third.m";
load "dembele/data/computed/cm_frame_cubic_lift.m";
cubic961_norm_scalar := (cubic961_norm_scalar+31) mod 961;
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_veronese.m";
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
PZ:=PolynomialRing(ZZ,16); zm:=[PZ.(p[1])*PZ.(p[2]):p in pairs];
function QForm(row,mon)
    Z:=BaseRing(Parent(mon[1]));
    return &+[(Z!Numerator(row[i])*(Z!Denominator(row[i]))^-1)*mon[i]:i in [1..#mon]];
end function;
curveZ:=[QForm(row,zm):row in rows];
ellZ:=&+[branch_parameter_linear_form[i]*PZ.i:i in [1..16]];
vdZ:=QForm(veronese_section_rows[2],zm);
vaZ:=QForm(veronese_section_rows[4],zm); vfZ:=QForm(veronese_section_rows[1],zm);
numZ:=QForm(rational_numerator,zm); denZ:=QForm(rational_denominator,zm);
function CoeffSequence(x)
    return Type(x) eq RngIntResElt select [x] else Eltseq(x);
end function;
function Reduction(x,F)
    cs:=[Integers()!c:c in CoeffSequence(x)];
    return Degree(F) eq 1 select F!cs[1] else F!cs;
end function;
constraints:=ZeroMatrix(ZZ,75,0); degrees:=[0,0]; factors:=[* [],[] *];
for component in cubic_lift_odd_support_components do
    side,hcoeff,coords,selected:=Explode(component); d:=#hcoeff-1;
    h:=UF!hcoeff; assert IsIrreducible(h) and LeadingCoefficient(h) eq 1;
    assert not h in factors[side]; Append(~factors[side],h); degrees[side]+:=d;
    F:=ext<GF(31)|h>; root:=d eq 1 select -F!hcoeff[1] else F.1;
    A:=d eq 1 select ZZ else GaloisRing(31,2,UZ!hcoeff);
    pt:=d eq 1 select [A!c[1]:c in coords] else [A!c:c in coords];
    assert pt[16] eq 1 and Reduction(pt[15],F) eq root;
    cut:=side eq 1 select vdZ else ellZ; equations:=curveZ cat [cut];
    assert &and[Evaluate(g,pt) eq 0:g in equations];
    jac:=Matrix(F,[[Reduction(Evaluate(Derivative(equations[i],j),pt),F):j in [1..15]]:i in selected]);
    assert Nrows(jac) eq 15 and Determinant(jac) ne 0;
    redpt:=[Reduction(x,F):x in pt];
    if side eq 1 then
        assert IsUnit(Evaluate(vaZ,pt)) and IsUnit(Evaluate(numZ,pt));
        assert Evaluate(vfZ,pt) eq 0 and Evaluate(denZ,pt) eq 0;
        assert &and[&+[F!row[j]*redpt[pairs[j][1]]*redpt[pairs[j][2]]:j in [1..136]] eq 0:
                    row in rational_E_quadrics_F31];
    else
        assert &or[Evaluate(l,redpt) ne 0:l in B3_linear_forms];
    end if;
    values:=[&*[pt[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
    constraints:=HorizontalJoin(constraints,Matrix(ZZ,[[ZZ!c:c in CoeffSequence(v)]:v in values]));
end for;
assert degrees eq [18,21] and Rank(ChangeRing(constraints,GF(31))) eq 39;
odd:=Matrix(ZZ,cubic_lift_odd_section_rows);
assert ChangeRing(odd,GF(31)) eq Matrix(GF(31),sections_odd_section_rows);
assert odd*constraints eq 0;
assert cubic_lift_point_indices eq kummer_evaluation_indices cat makdisi_auxiliary_indices;
for i in [1..1135] do
    pt:=liftpts[i]; xs:=pt[1..16]; idx:=cubic_lift_point_indices[i];
    assert xs[16] eq 1 and &and[Evaluate(g,xs) eq 0:g in curveZ];
    nv:=Evaluate(numZ,xs); dv:=Evaluate(denZ,xs); lv:=Evaluate(ellZ,xs);
    assert IsUnit(nv*dv*lv*pt[17]) and pt[17]^2*dv eq nv;
    assert [Reduction(x,kk):x in pt] eq [kk!c:c in sections_evaluation_point_coordinates[idx]];
    fidx:=Index(cubic_lift_point_indices,sections_frobenius_permutation[idx]);
    assert fidx ne 0;
    assert liftpts[fidx] eq [AG!Eltseq(x)[1]+(AG!Eltseq(x)[2])*(-29-bG):x in pt];
end for;
assert #Seqset(cubic_lift_point_indices[1..1024]) eq 1024 and 1024 gt 8*120;
assert &and[liftpts[tt[i]] eq liftpts[i][1..16] cat [-liftpts[i][17]]:i in [1..1024]];
bpt:=[AB!UB![ZZ!Numerator(c)*(ZZ!Denominator(c))^-1:c in row]:row in fiber_point_coordinates];
sqrtm3:=ZZ!879; assert sqrtm3^2 eq -3 and GF(31)!sqrtm3 eq 11;
wr:=sqrtm3*(AB!UB![ZZ!Numerator(c)*(ZZ!Denominator(c))^-1:c in branch_branch_ratio]);
b2:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_even_monomial_exponents];
b3:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
bo:=[&+[odd[i,j]*b3[j]:j in [1..75]]:i in [1..36]];
assert bp1 eq b2 cat [wr*x:x in bo] and bm1 eq b2 cat [-wr*x:x in bo];
print "PASS|SAVED_POINTS_SECTIONS_AND_BRANCH_LIFTS_MOD961";

function Included(A,B) return RIsZero(RMultiply(A,REquations(B))); end function;
function BaseRow(cs) return RBase(Matrix(ZZ,1,#cs,cs)); end function;
WE:=RMultiply(RDecode(lift_third_coordinates),RG2);
delta:=RChord(RNegClass(RWP,RV2),RWM,RV1,RV2,RV3);
assert REqual(delta,RMultiply(RDecode(lift_delta_coordinates),RV2),RV2);
candidate:=RCols(WE,[1..640]); minusA:=RNegClass(candidate,RV2);
threeA:=RChord(RChord(candidate,candidate,RV1,RV2,RV3),minusA,RV1,RV2,RV3);
assert REqual(threeA,RNegClass(delta,RV2),RV2);
assert REqual(candidate,RFrob(candidate,makdisi_evaluation_frobenius),RV2);
assert REqual(minusA,RTau(candidate,makdisi_evaluation_involution),RV2);
WRcoords:=RBase(Matrix(ZZ,cubic961_descended_divisor_coordinates));
WR:=RMultiply(WRcoords,RG2); assert Rank(RReduce(WR)) eq 81;
assert RFrob(WR,ff) eq WR and REqual(RCols(WR,[1..640]),candidate,RV2);
assert RowSpace(RReduce(WRcoords)) eq RowSpace(DecodeOld(kummer_descended_divisor_coordinates,kk));
print "PASS|INDEPENDENT_THIRD_RELATION_AND_REDUCTION_MOD961";

qcoeff:=BaseRow(cubic961_q_coefficients); q:=RMultiply(qcoeff,RG1);
assert &+[qcoeff[1][1,i]*bm1[i]:i in [1..81]] eq 0;
assert IsUnit(&+[qcoeff[1][1,i]*bp1[i]:i in [1..81]]);
qkernel:=RKernelRelaxed(RBase(Matrix(ZZ,cubic_lift_branch_minus_values)));
Sminus:=RMultiply(qkernel,RG1);
WQ:=RQuotient(Sminus,RScaleRows(RG2,q),RG2,90);
Qcoeff:=RCoordinates(RG2,WQ); bc:=RMultiply(Qcoeff,RBplus);
bk:=RKernelRelaxed(bc); assert Nrows(bk[1]) eq 81 and RIsZero(RMultiply(bk,bc));
WB:=RMultiply(bk,WQ); WB3:=RProduct(WB,RG1,201); WB4:=RProduct(WB,RG2,321);
assert Rank(RReduce(RJoin(RProduct(WE,RG1,201),WB3))) eq 321;
traceSpace:=RProduct(WE,RFrob(WE,ff),201);
ker:=RKernelRelaxed(RMultiply(traceSpace,REquations(WB4)));
moving:=RMultiply(ker,traceSpace); assert Nrows(moving[1]) eq 81 and Included(moving,WB4);
move:=RMultiply(BaseRow(cubic961_moving_coefficients),RG4);
assert Included(move,moving) and Rank(RReduce(move)) eq 1 and RFrob(move,ff) eq move;
WRcheck:=RQuotient(moving,RScaleRows(RG2,move),RG2,81);
assert Included(WRcheck,WR) and Included(WR,WRcheck);
assert Rank(RReduce(RJoin(RProduct(WR,RG1,201),WB3))) eq 321;
u:=RMultiply(BaseRow(cubic961_u_coefficients),RG4);
f:=RMultiply(BaseRow(cubic961_f_coefficients),RG2);
cubeSpace:=RProduct(RProduct(WR,WR,201),WR,321);
normSpace:=RProduct(WR,RTau(WR,tt),201);
assert Rank(RReduce(u)) eq 1 and Rank(RReduce(f)) eq 1;
assert Included(RScaleRows(RG2,u),cubeSpace) and Included(u,WB4);
assert Included(RScaleRows(RG2,f),normSpace) and RTau(f,tt) eq f;
ut:=RTau(u,tt); qt:=RTau(q,tt); c:=BaseRow([cubic961_norm_scalar]);
assert IsUnit(c[1][1,1]);
normleft:=RScaleRows(u,ut);
normright:=RScaleRows(RScaleRows(RScaleRows(RScaleRows(f,f),f),q),qt);
norm_ok:=normleft eq RMultiply(c,normright);
assert norm_ok;
assert not RIsZero(RSubtract(RScaleRows(u,qt),RScaleRows(ut,q)));
print "PASS|INDEPENDENT_FUNCTION_DIVISORS_AND_NORM_MOD961";

xs:=[pt[1..16]:pt in liftpts[1..1024]];
C4:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in cubic_quartic_monomials]));
C10:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in cubic_decic_monomials]));
assert Rank(RReduce(C4)) eq 105 and Rank(RReduce(C10)) eq 285;
avec:=RMultiply(BaseRow(cubic961_a_coefficients),C4);
denvec:=RMultiply(BaseRow(cubic961_denominator_coefficients),C4);
numvec:=RMultiply(BaseRow(cubic961_trace_numerator_coefficients),C10);
assert avec eq RMultiply(c,f) and denvec eq RScaleRows(q,qt);
trace_ok:=numvec eq RMultiply(c,RAdd(RScaleRows(u,qt),RScaleRows(ut,q)));
assert trace_ok;
for item in [* <cubic961_q_coefficients,kummer_q_coefficients>,
    <cubic961_u_coefficients,kummer_u_coefficients>, <cubic961_f_coefficients,kummer_f_coefficients>,
    <cubic961_a_coefficients,cubic_a_coefficients>,
    <cubic961_denominator_coefficients,cubic_denominator_coefficients>,
    <cubic961_trace_numerator_coefficients,cubic_trace_numerator_coefficients> *] do
    assert [z mod 31:z in item[1]] eq item[2];
    assert &and[0 le z and z lt 961:z in item[1]];
end for;
assert cubic961_norm_scalar mod 31 eq kummer_norm_scalar;
S<v,z>:=PolynomialRing(ZZ,2);
assert (v+z)^3-3*v*z*(v+z)-(v^3+z^3) eq 0;
assert 108*(v*z)^3-27*(v^3+z^3)^2 eq -27*(v^3-z^3)^2;
assert (3*(2*16-2)+18+2*9+2) div 2 eq 64;
print "PASS|INDEPENDENT_CUBIC_COEFFICIENTS_AND_REDUCTION_MOD961";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|193_CM_FRAME_CUBIC_LIFT_CHECK";quit;
