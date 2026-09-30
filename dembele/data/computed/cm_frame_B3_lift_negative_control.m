// D76: verify saved moving sections, products and the square map independently.
// No linear solve or section selection is repeated.
SetQuitOnError(true); SetColumns(0); SetSeed(76);
started:=Cputime();
load "dembele/data/computed/cm_frame_B3_product_lift_128.m";
product_selected_denominator[92] +:= product_modulus div 31;
load "dembele/data/computed/cm_frame_doubling_128.m";
load "dembele/data/computed/cm_frame_B3_transfer.m";
assert product_modulus eq lift_modulus;
Z:=Integers(product_modulus); k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
IQ:=Ideal(C_candidate); GQ:=GroebnerBasis(IQ);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function Quadric(row,mon)
    return &+[(Integers()!row[j])*mon[j]:j in [1..#mon]];
end function;
function Red(c,Z)
    assert Denominator(c) mod 31 ne 0;
    return (Z!Numerator(c))/(Z!Denominator(c));
end function;
function ReducedNormalForm(f,I,Z)
    out:=Parent(f)!0; cs,ms:=CoefficientsAndMonomials(NormalForm(f,I));
    for i in [1..#cs] do out+:=(Integers()!Red(cs[i],Z))*ms[i]; end for;
    return out;
end function;
function QValue(row,x,pairs)
    return &+[row[i]*x[pairs[i][1]]*x[pairs[i][2]]:i in [1..#pairs]];
end function;
g:=Quadric(product_g,mon); h:=Quadric(product_h,mon);
assert ReducedNormalForm(g,B3_ideal,Z) eq 0;
assert ReducedNormalForm(h,B3_ideal,Z) eq 0;
etotal:=0;
for component in lift_components do
    label,degree,f,cs,vs,ws:=Explode(component);
    if label ne "E" then continue; end if;
    T<z>:=PolynomialRing(Z); A<a>:=quo<T|T!f>;
    xs:=[A!T!c:c in cs];
    assert QValue(product_g,xs,pairs) eq 0;
    assert QValue(product_h,xs,pairs) eq 0;
    etotal+:=degree;
end for;
assert etotal eq 16;
PS<t>:=PowerSeriesRing(Z,8);
xs:=[(&+[PS!lift_point_jets[n+1][j]*t^n:n in [0..7]])+O(t^8):j in [1..16]];
assert #product_q_basis eq 3 and #product_q_witnesses eq 3;
qs:=[Quadric(row,mon):row in product_q_basis];
for i in [1..3] do
    assert ReducedNormalForm(h*qs[i]-g*Quadric(product_q_witnesses[i],mon),IQ,Z) eq 0;
    jet:=QValue(product_q_basis[i],xs,pairs);
    assert &and[Coefficient(jet,n) eq 0:n in [0..6]];
end for;
assert Rank(Matrix(GF(31),rows cat product_q_basis)) eq 94;
oldn:=Quadric(lift_numerator,mon); oldd:=Quadric(lift_denominator,mon);
newn:=Quadric(B3_new_numerator,mon);
multiplier:=ReducedNormalForm(ReducedNormalForm(oldn*g,IQ,Z)*g,IQ,Z);
start_rhs:=ReducedNormalForm(newn*oldd,IQ,Z);
assert product_indices eq [[i,j]:i,j in [1..3]|i le j];
assert #product_denominators eq 6;
for index in [1..6] do
    ij:=product_indices[index]; d:=Quadric(product_denominators[index],mon);
    left:=ReducedNormalForm(multiplier*d,IQ,Z);
    right:=ReducedNormalForm(ReducedNormalForm(start_rhs*qs[ij[1]],IQ,Z)*qs[ij[2]],IQ,Z);
    assert left eq right;
end for;
assert Rank(Matrix(GF(31),product_denominators)) eq product_space_rank;
assert Rank(Matrix(GF(31),rows cat product_denominators)) eq 91+product_space_rank;
q:=Quadric(product_selected_q,mon); d:=Quadric(product_selected_denominator,mon);
selected_left:=ReducedNormalForm(multiplier*d,IQ,Z);
selected_right:=ReducedNormalForm(ReducedNormalForm(start_rhs*q,IQ,Z)*q,IQ,Z);
assert selected_left eq selected_right;
assert selected_left ne 0;
assert Integers()!Coefficient(QValue(product_selected_q,xs,pairs),7) mod 31 ne 0;
assert &and[Red(c,Integers(31)) eq 0:c in Coefficients(NormalForm(q-Quadric(B3_square_denominator,mon),IQ))
    cat Coefficients(NormalForm(d-Quadric(B3_new_denominator,mon),IQ))
    cat Coefficients(NormalForm(g-Quadric(B3_square_numerator,mon),IQ))];
print "PASS|ALL_SIX_PRODUCT_IDENTITIES_AND_SELECTED_SQUARE_MAP";

// The second section h is a unit along the entire reduced residual G.
// This certifies the meaning of h*q=g*s without reconstructing G at high precision.
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
IE:=Saturation(IC+ideal<R|[Quadric(row,mon):row in resolvent_E_quadrics]>);
IEB3:=IE meet B3_ideal;
g:=Quadric(product_g,mon); h:=Quadric(product_h,mon);
assert g in IEB3 and h in IEB3;
IG:=Saturation(ColonIdeal(IC+ideal<R|g>,IEB3));
assert Degree(Scheme(P,IG)) eq 35 and IsReduced(Scheme(P,IG));
assert Dimension(IG+IEB3) eq 0 and Dimension(IG+ideal<R|h>) eq 0;
assert Saturation(IC+ideal<R|g>) eq (IEB3 meet IG);
printf "MODULUS|%o\n",product_modulus;
printf "PRODUCT_SPACE_RANK|%o\n",product_space_rank;
print "BRANCH_DEGREE|18";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|149_CM_FRAME_B3_LIFT_CHECK";
quit;
