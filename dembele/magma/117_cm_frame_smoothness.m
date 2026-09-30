// D69: exact smoothness certificate for the D68 curve candidate.
// The squarefree-discriminant argument is proved in cm-frame-verification.md.
// It certifies this algebraic curve, not its Shimura identification.
SetColumns(0); SetSeed(69); SetQuitOnError(true);
started := Cputime();

function FreeBasis(I)
    R := Generic(I); n := Rank(R); G := GroebnerBasis(I);
    LM := [LeadingMonomial(f) : f in G];
    assert &and[Exponents(m)[n-1] eq 0 and Exponents(m)[n] eq 0 : m in LM];
    B := [R!1]; layer := [R!1];
    repeat
        layer := Setseq({m*R.i : m in layer, i in [1..n-2] |
            not &or[IsDivisibleBy(m*R.i,l) : l in LM]});
        B cat:= layer;
        assert #B le 1000;
    until #layer eq 0;
    Sort(~B);
    return B;
end function;

function CoordinatesOverLine(f,I,B,T,chart)
    R := Generic(I); n := Rank(R);
    nf := NormalForm(f,I); out := [T!0 : b in B];
    cs,ms := CoefficientsAndMonomials(nf);
    for a in [1..#cs] do
        ee := Exponents(ms[a]);
        m := ExactQuotient(ms[a],R.(n-1)^ee[n-1]*R.n^ee[n]);
        j := Index(B,m); assert j gt 0;
        out[j] +:= cs[a]*T.1^ee[chart];
    end for;
    return out;
end function;

function TraceData(I,B,chart)
    T<t> := PolynomialRing(BaseRing(Generic(I))); r := #B;
    products := AssociativeArray(); traces := [T!0 : b in B];
    for i in [1..r] do
        for j in [i..r] do
            v := CoordinatesOverLine(B[i]*B[j],I,B,T,chart);
            products[<i,j>] := v;
            traces[i] +:= v[j];
            if i ne j then traces[j] +:= v[i]; end if;
        end for;
    end for;
    H := ZeroMatrix(T,r,r);
    for i in [1..r] do
        for j in [i..r] do
            H[i,j] := &+[products[<i,j>][a]*traces[a] : a in [1..r]];
            H[j,i] := H[i,j];
        end for;
    end for;
    assert traces[1] eq r;
    return Determinant(H),H,products;
end function;

procedure CheckTraceByMatrices(H,products,a)
    // An independent construction of the trace form on a specialized fiber.
    // Row j of M_i is the product b_j*b_i in the standard basis.
    k := Parent(a); r := Nrows(H);
    mats := [Matrix(k,r,r,&cat[
        [Evaluate(c,a) : c in products[<Minimum(i,j),Maximum(i,j)>]]
        : j in [1..r]]) : i in [1..r]];
    for i in [1..r] do
        for j in [i..r] do
            assert Trace(mats[i]*mats[j]) eq Evaluate(H[i,j],a);
        end for;
    end for;
end procedure;

// Controls exercise both outcomes and show that this is only a sufficient test.
k := GF(31); Ptest<x,y,z> := ProjectiveSpace(k,2);
for f in [x^2-y*z, x^3-y^2*z, x^3+y^3+z^3] do
    Itest := ideal<CoordinateRing(Ptest)|f>; Btest := FreeBasis(Itest);
    d,H,products := TraceData(Itest,Btest,2);
    CheckTraceByMatrices(H,products,k!2);
    if f eq x^2-y*z then
        assert d eq 4*Parent(d).1;
        dinf := TraceData(Itest,Btest,3);
        assert dinf eq 4*Parent(dinf).1;
        assert IsNonsingular(Curve(Ptest,f));
    elif f eq x^3-y^2*z then
        assert d eq -27*Parent(d).1^4;
        assert Degree(GCD(d,Derivative(d))) gt 0;
        assert not IsNonsingular(Curve(Ptest,f));
    else
        assert d eq -27*(Parent(d).1^3+1)^2;
        assert Degree(GCD(d,Derivative(d))) gt 0;
        assert IsNonsingular(Curve(Ptest,f));
    end if;
end for;
print "PASS|DISCRIMINANT_CONTROLS|SMOOTH_CONIC|SINGULAR_CUSP|SMOOTH_REPEATED_BRANCH";

// Recheck the generic curve and the monic Groebner model over Z_(31).
k := Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
IQ := Ideal(C_candidate); GQ := GroebnerBasis(IQ); BQ := FreeBasis(IQ);
hp := HilbertPolynomial(IQ);
assert Dimension(IQ) eq 2 and hp eq 30*Parent(hp).1-15;
assert #BQ eq 30;
den := LCM(&cat[[Denominator(c) : c in Coefficients(f)] : f in GQ]);
assert GCD(den,31) eq 1;
assert &and[LeadingCoefficient(f) eq 1 : f in GQ];
function ReducePolynomial(f,S)
    kk := BaseRing(S); cs,ms := CoefficientsAndMonomials(f); ans := S!0;
    for i in [1..#cs] do
        ee := Exponents(ms[i]); cc := (kk!Numerator(cs[i]))/(kk!Denominator(cs[i]));
        ans +:= cc*&*[S.j^ee[j] : j in [1..Rank(S)]];
    end for;
    return ans;
end function;
P31 := ProjectiveSpace(GF(31),15); R31 := CoordinateRing(P31);
polys31 := [ReducePolynomial(f,R31) : f in polys];
I31 := ideal<R31|polys31>; G31 := GroebnerBasis(I31);
assert G31 eq [ReducePolynomial(f,R31) : f in GQ];
print "PASS|FLAT_MONIC_GROEBNER_MODEL_AT_31";

B := FreeBasis(I31); ds := [TotalDegree(b) : b in B];
assert ds eq [0] cat [1 : i in [1..14]] cat [2 : i in [1..14]] cat [3];
assert [Exponents(b) : b in B] eq [Exponents(b) : b in BQ];
// The last two coordinates have no common projective zero.
assert Dimension(I31+ideal<R31|R31.15,R31.16>) eq 0;
printf "BASIS_EXPONENTS|%o\n", [Exponents(b) : b in B];
printf "BASIS_DEGREES|%o\n", ds;
print "PASS|FINITE_FREE_PROJECTION|DEGREE_30";

d,H,products := TraceData(I31,B,15);
dinf,Hinf,productsinf := TraceData(I31,B,16);
assert Degree(d) eq 90 and Degree(dinf) eq 90;
assert Degree(GCD(d,Derivative(d))) eq 0;
assert Degree(GCD(dinf,Derivative(dinf))) eq 0;
assert dinf eq Parent(dinf)!Reverse(Coefficients(d));
assert Evaluate(dinf,0) ne 0;
for a in [0,1,2] do CheckTraceByMatrices(H,products,GF(31)!a); end for;
CheckTraceByMatrices(Hinf,productsinf,GF(31)!0);
printf "DISCRIMINANT_COEFFICIENTS|%o\n", [Integers()!c : c in Coefficients(d)];
printf "DISCRIMINANT_FACTOR_DEGREES|%o\n", [Degree(f[1]) : f in Factorization(d)];
printf "INFINITY_DISCRIMINANT|%o\n", Integers()!Evaluate(dinf,0);
print "PASS|TWO_CHART_SQUAREFREE_DISCRIMINANTS";
print "PASS|SPECIALIZED_TRACE_MATRIX_CHECKS";

C31 := Curve(P31,I31);
assert IsIrreducible(C31) and IsReduced(C31);
assert ArithmeticGenus(C31) eq 16 and Degree(C31) eq 30;
S0 := Scheme(P31,I31+ideal<R31|R31.15>);
pts := Points(S0); assert #pts gt 0;
pt := Eltseq(pts[1]);
assert &and[Evaluate(f,pt) eq 0 : f in polys31];
// This point, integrality and smoothness imply geometric integrality.
printf "RATIONAL_POINT_MOD31|%o\n", [Integers()!a : a in pt];
print "PASS|SMOOTH_GEOMETRICALLY_INTEGRAL_SPECIAL_FIBER_GENUS16";
// Properness + the flat model give smoothness over Q. The graded free basis
// gives h0(O)=1 and h0(O(1))=16 after any ground-field extension. Thus the
// generic curve is geometrically integral and its degree-30 embedding is canonical.
print "PASS|SMOOTH_GEOMETRICALLY_INTEGRAL_CANONICAL_CURVE_OVER_Q";
printf "CPU_SECONDS|%o\n", Cputime(started);
print "PASS|117_CM_FRAME_SMOOTHNESS";
quit;
