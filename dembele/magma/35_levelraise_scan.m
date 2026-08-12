// Level-raising prime scan (period route, gate 1).
// Find primes q0 of F with abar_{q0} = 0 in F_256 for Dembele's constituents,
// i.e. lambda | a_{q0} in the Hecke field H of the unique 16-dimensional
// characteristic-zero component.  Since Nq is odd, the level-raising
// congruence a_q = +-(Nq+1) mod lambda is exactly abar_q = 0, and
// lambda | a_q  <=>  the constant term of charpoly(T_q | V16) is even
// (Norm(lambda) = 2^8; v_2(Norm(a_q)) = 8 v_lambda + 8 v_lambda').
//
// Usage:
//   HMF_ROOT=/path/to/hilbertmodularforms magma -b dembele/magma/35_levelraise_scan.m
SetColumns(0);
hmf_root := GetEnv("HMF_ROOT");
require hmf_root ne "" : "Set HMF_ROOT";
AttachSpec(hmf_root cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
M := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M) eq 57;

Zz<z> := PolynomialRing(Integers());

// build the 16-dimensional constituent subspace from T_31
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
T31 := InternalHMFRawHeckeDefinite(M, p31);
cp31, rem := Quotrem(Zz!CharacteristicPolynomial(T31), z - (Norm(p31) + 1));
assert rem eq 0;
fac := Factorization(cp31);
deg16 := [ f[1] : f in fac | Degree(f[1]) eq 16 ];
assert #deg16 eq 1;
g16 := deg16[1];
printf "degree-16 factor at 31 found; building V16...\n";
T31q := ChangeRing(T31, Rationals());
V16 := Kernel(Evaluate(g16, T31q));
assert Dimension(V16) eq 16;
B16 := BasisMatrix(V16);
printf "V16 built.\n";

// primes of F by norm
NORMBOUND := 5000;
prs := [];
for q in PrimesUpTo(NORMBOUND) do
    if q eq 2 then continue; end if;
    for pr in Factorization(q*OF) do
        if Norm(pr[1]) le NORMBOUND then Append(~prs, pr[1]); end if;
    end for;
end for;
Sort(~prs, func< a, b | Norm(a) - Norm(b) >);
printf "scanning %o primes of F with norm <= %o\n", #prs, NORMBOUND;

hits := 0;
for pr in prs do
    t0 := Cputime();
    Tq := InternalHMFRawHeckeDefinite(M, pr);
    Tqq := ChangeRing(Tq, Rationals());
    // restrict to V16: rows of B16 * Tq expressed in basis B16
    R := B16 * Tqq;
    Sol := Solution(B16, R);   // Sol * B16 = R
    cp16 := Zz!CharacteristicPolynomial(Sol);
    c0 := Integers()!Coefficient(cp16, 0);
    tr := Integers()!(-Coefficient(cp16, 15));
    ev := IsEven(c0);
    printf "Nq=%o (q over %o): trace=%o const2val=%o %o  [%o s]\n",
        Norm(pr), Factorization(Norm(pr))[1][1], tr mod 2,
        c0 eq 0 select -1 else Valuation(c0, 2),
        ev select "<== LEVEL-RAISING PRIME" else "",
        RealField(4)!Cputime(t0);
    if ev then hits +:= 1; end if;
    if hits ge 4 then printf "found %o admissible primes; stopping\n", hits; break; end if;
end for;
printf "DONE (%o hits)\n", hits;
quit;
