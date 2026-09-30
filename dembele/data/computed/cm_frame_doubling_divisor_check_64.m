// D74 generated verifier/transfer; only the displayed data paths differ.
// D72: independent exact certificate over Z/31^n, using local finite algebras.
// Does not replay the Sage linear solves or use its asserted ranks.
SetQuitOnError(true); SetColumns(0); SetSeed(72);
started:=Cputime(); k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
load "dembele/data/computed/cm_frame_doubling_64.m";
assert lift_modulus ge 31^2;
assert &and[k!lift_numerator[i] eq k!resolvent_numerator[i] : i in [1..136]];
assert &and[k!lift_denominator[i] eq k!resolvent_denominator[i] : i in [1..136]];
Z:=Integers(lift_modulus);
function QValue(row,x,pairs)
    return &+[row[i]*x[pairs[i][1]]*x[pairs[i][2]] : i in [1..#pairs]];
end function;
function QDerivative(row,x,v,pairs)
    return &+[row[i]*(x[pairs[i][1]]*v[pairs[i][2]]+v[pairs[i][1]]*x[pairs[i][2]])
              : i in [1..#pairs]];
end function;

totals:=AssociativeArray(); support_polynomials:=AssociativeArray();
U<s>:=PolynomialRing(k);
for label in ["D17","E","F"] do
    totals[label]:=0; support_polynomials[label]:=U!1;
end for;
for component in lift_components do
    label,d,h,cs,vs,ws:=Explode(component);
    f:=U!h; assert Degree(f) eq d and IsIrreducible(f);
    assert Degree(GCD(f,Derivative(f))) eq 0;
    assert Degree(GCD(f,support_polynomials[label])) eq 0;
    support_polynomials[label]*:=f;
    T<z>:=PolynomialRing(Z); A<a>:=quo<T|T!h>;
    if d eq 1 then
        A0:=k; b:=-Coefficient(f,0);
    else
        A0<b>:=ext<k|f>;
    end if;
    xs:=[A!T!c:c in cs]; v:=[A!T!c:c in vs];
    x0:=[Evaluate(U!c,b):c in cs]; v0:=[Evaluate(U!c,b):c in vs];
    assert #xs eq 16 and #v eq 16;
    assert x0[15] eq b and xs[16] eq 1;
    assert v[15] eq 1 and v[16] eq 0;
    // The unramified coordinate and unit Jacobian give a local parameter.
    Jac:=Matrix(A0,[[A0!Evaluate(Derivative(q,j),x0):j in [1..14]]:q in polys]);
    assert Rank(Jac) eq 14;
    assert &and[QValue(q,xs,pairs) eq 0:q in rows];
    assert &and[QDerivative(q,xs,v,pairs) eq 0:q in rows];
    nv:=QValue(lift_numerator,xs,pairs); dv:=QValue(lift_denominator,xs,pairs);
    nd0:=QDerivative(lift_numerator,x0,v0,pairs);
    dd0:=QDerivative(lift_denominator,x0,v0,pairs);
    if label eq "D17" then
        assert &and[QValue(q,xs,pairs) eq 0:q in D17_extra_rows];
        assert nv eq 0 and nd0 ne 0;
        assert QValue(lift_denominator,x0,pairs) ne 0;
    elif label eq "F" then
        assert nv eq 0 and dv eq 0 and nd0 ne 0 and dd0 ne 0;
    else
        assert label eq "E";
        assert &and[QValue(q,x0,pairs) eq 0:q in resolvent_E_quadrics];
        assert dv eq 0 and QDerivative(lift_denominator,xs,v,pairs) eq 0;
        assert QValue(lift_numerator,x0,pairs) ne 0;
        w0:=[Evaluate(U!c,b):c in ws];
        assert #w0 eq 16 and w0[15] eq 0 and w0[16] eq 0;
        assert &and[QDerivative(q,x0,w0,pairs)+QValue(q,v0,pairs) eq 0:q in rows];
        coefficient2:=QDerivative(lift_denominator,x0,w0,pairs)+QValue(lift_denominator,v0,pairs);
        assert coefficient2 ne 0;
    end if;
    totals[label]+:=d;
    printf "COMPONENT_PASS|%o|%o\n",label,d;
end for;
assert [totals[label]:label in ["D17","E","F"]] eq [17,16,28];
for a,b in ["D17","E","F"] do
    if a ne b then assert Degree(GCD(support_polynomials[a],support_polynomials[b])) eq 0; end if;
end for;

// A full order-16 jet of the fixed rational point, in the X1=1 chart.
PS<t>:=PowerSeriesRing(Z,16);
xs:=[(&+[PS!lift_point_jets[n+1][j]*t^n:n in [0..15]])+O(t^16):j in [1..16]];
point:=[Z!c/(Z!P32_coordinates[1]):c in P32_coordinates];
assert [Coefficient(x,0):x in xs] eq point;
assert xs[1] eq 1 and xs[16]-point[16] eq t;
assert &and[QValue(q,xs,pairs) eq 0:q in rows];
Jac:=Matrix(k,[[Evaluate(Derivative(q,j),[k!x:x in point]):j in [2..15]]:q in polys]);
assert Rank(Jac) eq 14;
ns:=QValue(lift_numerator,xs,pairs); ds:=QValue(lift_denominator,xs,pairs);
assert &and[Coefficient(ns,n) eq 0:n in [0..14]];
assert k!Coefficient(ns,15) ne 0 and k!Coefficient(ds,0) ne 0;
for label in ["D17","E","F"] do
    assert Evaluate(support_polynomials[label],k!point[15]/k!point[16]) ne 0;
end for;

// Flat divisors with these disjoint reductions exhaust both degree-60
// canonical quadric divisors: 17+15+28 and 2*16+28 respectively.
assert totals["D17"]+15+totals["F"] eq 60;
assert 2*totals["E"]+totals["F"] eq 60;
printf "MODULUS|%o\n",lift_modulus;
print "DIVISOR_IDENTITY|D17 + 15*P32 - 2*E";
print "HALF_LINE_BUNDLE_DEGREE|9";
print "BRANCH_DEGREE|18";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|125_CM_FRAME_RESOLVENT_LIFT_CHECK";
quit;
