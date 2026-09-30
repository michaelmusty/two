// D69: independent finite-field fingerprint of the D68 candidate.
// Matching these two counts is not a Shimura-curve identification theorem.
SetColumns(0); SetSeed(69); SetQuitOnError(true);
if not assigned extension_degree then extension_degree := 1; end if;
assert extension_degree in [1,2];
started := Cputime(); k := GF(31^extension_degree);
load "dembele/data/computed/cm_frame_curve_candidate.m";
I := Ideal(C_candidate); G := GroebnerBasis(I);
assert Dimension(I+ideal<R|R.15,R.16>) eq 0;
seen := {}; total := 0; checked := 0;
for a in k do
    if a in seen then continue; end if;
    orb := {a^(31^j) : j in [0..extension_degree-1]};
    seen join:= orb;
    S := Scheme(P,I+ideal<R|R.15-a*R.16>);
    assert Dimension(S) eq 0 and Degree(S) eq 30;
    pts := Points(S); total +:= #orb*#pts; checked +:= 1;
    assert &and[Evaluate(f,Eltseq(p)) eq 0 : f in polys, p in pts];
    assert &and[p[16] ne 0 and p[15] eq a*p[16] : p in pts];
    printf "FIBER|%o|%o|%o\n", [Integers()!c : c in Eltseq(a)], #orb, #pts;
end for;
assert #seen eq #k;
Sinf := Scheme(P,I+ideal<R|R.16>);
assert Dimension(Sinf) eq 0 and Degree(Sinf) eq 30;
pts := Points(Sinf); total +:= #pts;
assert &and[Evaluate(f,Eltseq(p)) eq 0 : f in polys, p in pts];
assert &and[p[16] eq 0 and p[15] ne 0 : p in pts];
printf "FIBER_INFINITY|%o\n", #pts;
printf "POINT_COUNT|%o|%o\n", extension_degree,total;

// Extract the four quartics belonging to the genus-16 quotient from the
// previously computed level-p2-new Hecke bank (scripts 58,60,64).
Z<z> := PolynomialRing(Integers());
bank := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
fs := [a[1] : a in Factorization(Z!bank[2]) | Degree(a[1]) eq 4];
assert #fs eq 4; p16 := &*fs; assert Degree(p16) eq 16;
frob := &+[Coefficient(p16,i)*z^(16-i)*(z^2+31)^i : i in [0..16]];
assert Degree(frob) eq 32;
trace1 := -Coefficient(frob,31);
trace2 := Coefficient(frob,31)^2-2*Coefficient(frob,30);
expected := 31^extension_degree+1-(extension_degree eq 1 select trace1 else trace2);
assert total eq expected;
printf "HECKE_TRACE_POLYNOMIAL|%o\n", Coefficients(p16);
printf "EXPECTED_POINT_COUNTS|%o|%o\n", 32-trace1,962-trace2;
printf "FIBERS_CHECKED|%o\n", checked+1;
printf "CPU_SECONDS|%o\n", Cputime(started);
print "PASS|118_CM_FRAME_POINT_COUNTS";
quit;
