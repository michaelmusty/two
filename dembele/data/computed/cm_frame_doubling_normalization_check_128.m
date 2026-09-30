// D74 generated verifier/transfer; only the displayed data paths differ.
// D73: independently check the saved pair, without repeating the transfer solve.
SetQuitOnError(true); SetColumns(0); SetSeed(73);
started:=Cputime(); k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_doubling_128.m";
load "dembele/data/computed/cm_frame_doubling_normalized_128.m";
assert normalized_modulus eq lift_modulus;
assert #normalized_numerator eq 136 and #normalized_denominator eq 136;
assert GCD(normalized_numerator) eq 1;
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function QValue(row,x,pairs)
    return &+[row[i]*x[pairs[i][1]]*x[pairs[i][2]]:i in [1..#pairs]];
end function;
function QDerivative(row,x,v,pairs)
    return &+[row[i]*(x[pairs[i][1]]*v[pairs[i][2]]+v[pairs[i][1]]*x[pairs[i][2]])
              :i in [1..#pairs]];
end function;
qn:=&+[normalized_numerator[i]*mon[i]:i in [1..136]];
qd:=&+[normalized_denominator[i]*mon[i]:i in [1..136]];
oldn:=&+[lift_numerator[i]*mon[i]:i in [1..136]];
oldd:=&+[lift_denominator[i]*mon[i]:i in [1..136]];
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
assert qn in D17_ideal;

// Independent exact rational implicit jets at P32.
point:=[c/P32_coordinates[1]:c in P32_coordinates];
JQ:=Matrix(k,[[Evaluate(Derivative(q,j),point):j in [2..15]]:q in polys]);
J0:=Matrix(GF(31),JQ); inds:=[]; rowlist:=[];
for i in [1..Nrows(J0)] do
    trial:=rowlist cat [Eltseq(J0[i])];
    if Rank(Matrix(GF(31),trial)) gt #rowlist then
        Append(~rowlist,Eltseq(J0[i])); Append(~inds,i);
    end if;
    if #inds eq 14 then break; end if;
end for;
assert #inds eq 14;
inv:=Submatrix(JQ,inds,[1..14])^-1;
PS<t>:=PowerSeriesRing(k,16); xs:=[PS!c+O(t^16):c in point]; xs[16]+:=t;
for n in [1..15] do
    rhs:=Vector(k,[-Coefficient(Evaluate(polys[i],xs),n):i in inds]);
    correction:=rhs*Transpose(inv);
    for j in [1..14] do xs[j+1]+:=correction[j]*t^n; end for;
end for;
assert &and[Evaluate(q,xs) eq 0:q in polys];
series:=Evaluate(qn,xs);
assert &and[Coefficient(series,n) eq 0:n in [0..14]];
assert Coefficient(series,15) ne 0;
print "PASS|EXACT_RATIONAL_NUMERATOR_CONDITIONS";

Z:=Integers(normalized_modulus);
residual:=NormalForm(oldn*qd-qn*oldd,IC);
assert &and[Denominator(c) mod 31 ne 0:c in Coefficients(residual)];
// This global quartic identity is the central preservation certificate.
assert &and[Numerator(c) mod normalized_modulus eq 0:c in Coefficients(residual)];
print "PASS|SAME_RADICAND_MODULO_31_POWER";

// Check the local orders retained at the fixed supports, at full precision.
U<s>:=PolynomialRing(GF(31)); totals:=AssociativeArray(); totals["D17"]:=0; totals["E"]:=0;
for component in lift_components do
    label,d,h,cs,vs,ws:=Explode(component);
    if label eq "F" then continue; end if;
    T<z>:=PolynomialRing(Z); A<a>:=quo<T|T!h>;
    f:=U!h;
    if d eq 1 then A0:=GF(31); b:=-Coefficient(f,0); else A0<b>:=ext<GF(31)|f>; end if;
    xx:=[A!T!c:c in cs]; vv:=[A!T!c:c in vs];
    x0:=[Evaluate(U!c,b):c in cs]; v0:=[Evaluate(U!c,b):c in vs];
    assert &and[QValue(q,xx,pairs) eq 0:q in rows];
    assert &and[QDerivative(q,xx,vv,pairs) eq 0:q in rows];
    if label eq "D17" then
        assert QValue(normalized_numerator,xx,pairs) eq 0;
        assert QDerivative(normalized_numerator,x0,v0,pairs) ne 0;
        assert QValue(normalized_denominator,x0,pairs) ne 0;
    else
        assert label eq "E";
        assert QValue(normalized_numerator,x0,pairs) ne 0;
        assert QValue(normalized_denominator,xx,pairs) eq 0;
        assert QDerivative(normalized_denominator,xx,vv,pairs) eq 0;
        w0:=[Evaluate(U!c,b):c in ws];
        assert QDerivative(normalized_denominator,x0,w0,pairs)
               +QValue(normalized_denominator,v0,pairs) ne 0;
    end if;
    totals[label]+:=d;
end for;
assert totals["D17"] eq 17 and totals["E"] eq 16;
ps<t>:=PowerSeriesRing(Z,16);
xx:=[(&+[ps!lift_point_jets[n+1][j]*t^n:n in [0..15]])+O(t^16):j in [1..16]];
ns:=QValue(normalized_numerator,xx,pairs); ds:=QValue(normalized_denominator,xx,pairs);
assert &and[Coefficient(ns,n) eq 0:n in [0..14]];
assert GF(31)!Coefficient(ns,15) ne 0 and GF(31)!Coefficient(ds,0) ne 0;
print "PASS|FIXED_SUPPORT_ORDERS_AT_FULL_PRECISION";

// Recheck the new degree-28 common divisor as an exact projective ideal.
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
IC:=Ideal(C_candidate); mon:=[R.(p[1])*R.(p[2]):p in pairs];
qn:=QValue(normalized_numerator,[R.i:i in [1..16]],pairs);
qd:=QValue(normalized_denominator,[R.i:i in [1..16]],pairs);
ps<t>:=PowerSeriesRing(k,16);
xx:=[(&+[ps!resolvent_point_jets[n+1][j]*t^n:n in [0..15]])+O(t^16):j in [1..16]];
jmat:=Matrix(k,[[Coefficient(Evaluate(q,xx),n):q in mon]:n in [0..14]]);
ker:=Basis(Nullspace(Transpose(jmat)));
IP15:=Saturation(ideal<R|[&+[v[i]*mon[i]:i in [1..136]]:v in ker]>);
ID32:=D17_ideal meet IP15;
Eqs:=[QValue(row,[R.i:i in [1..16]],pairs):row in resolvent_E_quadrics];
IE:=Saturation(IC+ideal<R|Eqs>); IE2:=Saturation(IC+ideal<R|[q*r:q,r in Eqs]>);
J:=Saturation(ColonIdeal(IC+ideal<R|qn>,ID32));
assert Degree(Scheme(P,J)) eq 28 and Dimension(J+ID32) eq 0 and Dimension(J+IE) eq 0;
assert Saturation(IC+ideal<R|qn>) eq ID32 meet J;
assert Saturation(IC+ideal<R|qd>) eq IE2 meet J;
assert Dimension(J+ideal<R|R.16>) eq 0;
U<z>:=PolynomialRing(k); h:=U!normalized_residual_modulus;
assert Degree(h) eq 28 and Degree(GCD(h,Derivative(h))) eq 0;
coords:=[U!c:c in normalized_residual_coordinates];
assert #coords eq 16 and coords[15] eq z and coords[16] eq 1;
assert &and[Evaluate(f,coords) mod h eq 0:f in Basis(J)];
S:=PolynomialRing(k,15,"grevlex");
ia:=ideal<S|[Evaluate(f,[S.i:i in [1..15]] cat [S!1]):f in Basis(J)]>;
shape:=ideal<S|[S.i-Evaluate(coords[i],S.15):i in [1..14]] cat [Evaluate(h,S.15)]>;
assert ia eq shape;
for factor in Factorization(h) do
    ff,e:=Explode(factor); assert e eq 1; d:=Degree(ff);
    if d eq 1 then A0:=k; b:=-Coefficient(ff,0); else A0<b>:=ext<k|ff>; end if;
    x0:=[Evaluate(c,b):c in coords];
    jac:=Matrix(A0,[[Evaluate(Derivative(q,j),x0):j in [1..14]]:q in polys]);
    assert Rank(jac) eq 14;
    jacn:=Matrix(A0,[[Evaluate(Derivative(q,j),x0):j in [1..15]]:q in polys cat [qn]]);
    assert Rank(jacn) eq 15;
end for;
print "PASS|NEW_REDUCED_RESIDUAL_DIVISOR_DEGREE_28";
printf "MODULUS|%o\n",normalized_modulus;
printf "HEIGHT|%o\n",Maximum([Abs(c):c in normalized_numerator]);
print "DIVISOR_IDENTITY|D17 + 15*P32 - 2*E";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|129_CM_FRAME_NORMALIZATION_CHECK";
quit;
