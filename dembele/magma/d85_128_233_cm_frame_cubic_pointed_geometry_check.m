// D85 redirected loads; original SHA256 6879c22e5f8331f97448f1fff550918bed8ca2cef9400c87c8287e73e2104bd6
// D82: independent saved-data verification at the requested precision.
SetQuitOnError(true); SetColumns(0); SetSeed(82233); started:=Cputime();
load "dembele/magma/d85_128_199_cm_frame_cubic_precision_model.m";
load "dembele/data/computed/cm_frame_cubic_gauge.m";
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
    A:=d eq 1 select ZZ else GaloisRing(31,precision_digits,UZ!hcoeff);
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
sqrtm3:=ZZ!11; rootdigits:=1;
while rootdigits lt precision_digits do sqrtm3-:=(sqrtm3^2+3)*(2*sqrtm3)^-1; rootdigits*:=2; end while;
assert sqrtm3^2 eq -3 and GF(31)!sqrtm3 eq 11;
wr:=sqrtm3*(AB!UB![ZZ!Numerator(c)*(ZZ!Denominator(c))^-1:c in branch_branch_ratio]);
b2:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_even_monomial_exponents];
b3:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
bo:=[&+[odd[i,j]*b3[j]:j in [1..75]]:i in [1..36]];
assert bp1 eq b2 cat [wr*x:x in bo] and bm1 eq b2 cat [-wr*x:x in bo];
print "PASS|SAVED_POINTS_SECTIONS_AND_BRANCH_LIFTS_AT_HIGHER_PRECISION";

J2:=Matrix(ZZ,pointed_jet2_coefficients);
// Reconstruct all formal jets, checking the curve equations and the local parameter.
PS<t>:=PowerSeriesRing(ZZ,244);
pj:=[&+[PS!row[j+1]*t^j:j in [0..243]]+O(t^244):row in pointed_curve_jets];
assert pj[16] eq 1 and &and[Evaluate(f,pj) eq 0:f in curveZ];
assert Evaluate(numZ,pj) eq t^2*Evaluate(denZ,pj);
pt0:=[ZZ!z:z in P32_coordinates]; pt0:=[z*pt0[16]^-1:z in pt0];
assert [Coefficient(x,0):x in pj] eq pt0;
assert IsUnit(Evaluate(denZ,pt0)*Evaluate(ellZ,pt0));
jac:=Matrix(ZZ,[[Evaluate(Derivative((curveZ cat [numZ])[i],j),pt0):j in [1..15]]:i in pointed_jacobian_rows]);
assert IsUnit(Determinant(jac));
function Mon(e,xs) return &*[xs[j]^e[j]:j in [1..16]]; end function;
ej:=[Mon(e,pj):e in sections_even_monomial_exponents];
om:=[Mon(e,pj):e in sections_odd_monomial_exponents];
oj:=[&+[odd[i,j]*om[j]:j in [1..75]]:i in [1..36]];
j1:=ej cat [t*x*Evaluate(ellZ,pj)^-1:x in oj];
j2:=[j1[p[1]]*j1[p[2]]:p in makdisi_product2_pairs];
assert Matrix(ZZ,[[Coefficient(f,j):j in [0..79]]:f in j1]) eq Matrix(ZZ,pointed_jet1_coefficients);
assert Matrix(ZZ,[[Coefficient(f,j):j in [0..79]]:f in j2]) eq J2;
af:=[Mon(e,pj):e in cubic_quartic_monomials];
bf:=[Mon(e,pj)*Evaluate(ellZ,pj)^-1:e in pointed_septic_monomials];
assert [Coefficient(f,160):f in af] eq [ZZ!z:z in pointed_a_leading_weights];
assert [Coefficient(f,240):f in bf] eq [ZZ!z:z in pointed_trace_leading_weights];
aser:=&+[pointed_cubic_a_coefficients[i]*af[i]:i in [1..105]];
bser:=&+[pointed_cubic_trace_septic_coefficients[i]*bf[i]:i in [1..195]];
assert &and[Coefficient(aser,j) eq 0:j in [0..159]] and Coefficient(aser,160) eq 1;
assert &and[Coefficient(bser,j) eq 0:j in [0..239]] and Coefficient(bser,240) eq 2;
if previous_cubic_modulus gt 1 then
    assert [[x mod previous_cubic_modulus:x in row]:row in pointed_cubic_descended_divisor_coordinates] eq previous_cubic_descended_divisor_coordinates;
    for item in [* <pointed_cubic_q_coefficients,previous_cubic_q_coefficients>,
        <pointed_cubic_u_coefficients,previous_cubic_u_coefficients>,
        <pointed_cubic_f_coefficients,previous_cubic_f_coefficients>,
        <pointed_cubic_a_coefficients,previous_cubic_a_coefficients>,
        <pointed_cubic_denominator_coefficients,previous_cubic_denominator_coefficients>,
        <pointed_cubic_trace_numerator_coefficients,previous_cubic_trace_numerator_coefficients>,
        <pointed_cubic_trace_septic_coefficients,previous_cubic_trace_septic_coefficients> *] do
        assert [x mod previous_cubic_modulus:x in item[1]] eq item[2];
    end for;
    assert pointed_cubic_norm_scalar mod previous_cubic_modulus eq previous_cubic_norm_scalar;
    assert pointed_cubic_scaling_scalar mod previous_cubic_modulus eq previous_cubic_scaling_scalar;
end if;
print "PASS|INDEPENDENT_POINTED_JETS_SCALING_AND_PRECEDING_DIGITS";

printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|233_CM_FRAME_CUBIC_POINTED_GEOMETRY_CHECK";quit;
