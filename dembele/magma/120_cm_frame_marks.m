// D70: exact marked divisors on the D68/D69 canonical curve.
// The CM labels are numerical identifications, not conclusions of this script.
SetColumns(0); SetSeed(70); SetQuitOnError(true);
started := Cputime();
k := Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
IC := Ideal(C_candidate);
assert &and[Evaluate(f,P32_coordinates) eq 0 : f in polys];
pt := Eltseq(P32_candidate);
anchor := Minimum([i : i in [1..16] | pt[i] ne 0]);
IP := ideal<R|[pt[anchor]*R.i-pt[i]*R.anchor : i in [1..16] | i ne anchor]>;
assert Degree(Scheme(P,IP)) eq 1;
assert Degree(B3_candidate) eq 9 and IsReduced(B3_candidate) and IsIrreducible(B3_candidate);
assert Degree(D17_candidate) eq 17 and IsReduced(D17_candidate) and IsIrreducible(D17_candidate);
assert Dimension(B3_ideal+D17_ideal) eq 0;
assert Dimension(B3_ideal+IP) eq 0 and Dimension(D17_ideal+IP) eq 0;
assert B3_ideal eq Saturation(B3_ideal) and D17_ideal eq Saturation(D17_ideal);
IB2 := D17_ideal meet IP;
assert Degree(Scheme(P,IB2)) eq 18;
printf "MARK_DEGREES|%o\n", [1,17,9];
print "PASS|REDUCED_DISJOINT_CLOSED_MARKS_OVER_Q";

// X15/X16 generates the nonic residue field; the last coordinate never vanishes.
assert Dimension(B3_ideal+ideal<R|R.16>) eq 0;
E := EliminationIdeal(B3_ideal,{R.15,R.16});
assert #Basis(E) eq 1;
T<t> := PolynomialRing(Rationals());
f := Evaluate(Basis(E)[1],[T!0 : i in [1..14]] cat [t,T!1]);
f /:= LeadingCoefficient(f);
assert Degree(f) eq 9 and IsIrreducible(f);
printf "NONIC_POLYNOMIAL_COEFFICIENTS|%o\n", Coefficients(f);
G,roots,galois_data := GaloisGroup(f : Prime:=31);
assert #G eq 72 and TransitiveGroupIdentification(G) eq 15;
assert GaloisProof(f,galois_data);
N := SylowSubgroup(G,3); H := Stabilizer(G,1);
assert IsNormal(G,N) and IsAbelian(N) and Exponent(N) eq 3;
assert #N eq 9 and #H eq 8 and IsCyclic(H);
assert #sub<G|Generators(N) join Generators(H)> eq 72;
printf "NONIC_GALOIS|%o|%o\n", #G,TransitiveGroupIdentification(G);
print "PASS|NONIC_GALOIS_PROOF";

function ReducePolynomial(f,S)
    kk := BaseRing(S); cs,ms := CoefficientsAndMonomials(f); ans := S!0;
    for i in [1..#cs] do
        ee := Exponents(ms[i]);
        cc := (kk!Numerator(cs[i]))/(kk!Denominator(cs[i]));
        ans +:= cc*&*[S.j^ee[j] : j in [1..Rank(S)]];
    end for;
    return ans;
end function;

// Certify flat closures at 31 by comparing monic Groebner bases.
P31 := ProjectiveSpace(GF(31),15); R31 := CoordinateRing(P31);
ideals31 := [];
for I in [IC,IP,D17_ideal,B3_ideal] do
    basisQ := GroebnerBasis(I);
    assert &and[LeadingCoefficient(g) eq 1 : g in basisQ];
    assert &and[GCD(Denominator(c),31) eq 1 : c in &cat[Coefficients(g) : g in basisQ]];
    I31 := ideal<R31|[ReducePolynomial(g,R31) : g in Basis(I)]>;
    assert GroebnerBasis(I31) eq [ReducePolynomial(g,R31) : g in basisQ];
    Append(~ideals31,I31);
end for;
IC31,IP31,D1731,B331 := Explode(ideals31);
for pair in [<IP31,1>,<D1731,17>,<B331,9>] do
    D := Scheme(P31,pair[1]);
    assert Degree(D) eq pair[2] and IsReduced(D);
end for;
assert Dimension(IP31+D1731) eq 0 and Dimension(IP31+B331) eq 0;
assert Dimension(D1731+B331) eq 0;
print "PASS|FLAT_REDUCED_DISJOINT_MARKS_AT_31";

// Test the tempting relation B2 ~ 2 B3 using residual ideals on the smooth curve.
// If it held over Q, proper-flat semicontinuity would give a section at 31.
IB231 := D1731 meet IP31;
L31 := [ReducePolynomial(a,R31) : a in B3_linear_forms];
J2 := IC31+ideal<R31|[a*b : a,b in L31]>;
assert Degree(Scheme(P31,J2)) eq 18;
line := L31[1];
assert Dimension(IB231+ideal<R31|line>) eq 0;
IE := Saturation(ColonIdeal(IC31+ideal<R31|line^2>,J2));
assert Degree(Scheme(P31,IE)) eq 42;
required := Saturation(IE meet IB231);
assert Degree(Scheme(P31,required)) eq 60;
series := PowerSeriesRing(Rationals());
hf_curve := Coefficient(series!HilbertSeries(IC31),2);
hf_required := Coefficient(series!HilbertSeries(required),2);
assert hf_curve eq 45 and hf_required eq 45;
printf "RR_DIMENSION_2B3_MINUS_B2_MOD31|%o\n", hf_curve-hf_required;
printf "RESIDUAL_DEGREES|%o\n", [18,42,60];
print "PASS|SIMPLE_BRANCH_DIVISOR_RELATION_EXCLUDED";
printf "CPU_SECONDS|%o\n", Cputime(started);
print "PASS|120_CM_FRAME_MARKS";
quit;
