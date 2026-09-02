// Level raising at the prime p2 above 2 itself (HANDOFF 2026-09-01, "norm-2 door").
//
// Question: does Dembélé's residual system rho-bar_f (level 1, mod lambda | 2)
// occur in the p2-NEW part of the level-p2 Brandt module of the definite
// discriminant-1 algebra?  If yes, rho-bar_f sits in Jac(X_p2)[lambda] for the
// Shimura curve X_p2 of discriminant p2 over F, which is 2-adically uniformized
// by our definite order on the 3-regular tree.
//
// Ribet's criterion at a prime q away from 2 would need a_q^2 = (Nq+1)^2 mod
// lambda, i.e. a-bar_p2 = 1 here; the level-1 fingerprint says a-bar_p2 = omega
// (charpoly (t^2+t+1)^8).  The criterion is not a theorem at p2 | 2 with e = 8,
// so we compute.
//
// Output markers: R57|... ; final verdict R57|VERDICT|...
SetColumns(0);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2);
F2z<zz> := PolynomialRing(F2);
wt := [2 : i in [1..8]];

p2 := Factorization(2*OF)[1][1];
assert Norm(p2) eq 2;
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];

// ---------------- level 1: residual invariants ----------------------------
t0 := Cputime();
M1 := HilbertCuspForms(F, 1*OF, wt);
assert Dimension(M1) eq 57;
T31_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
T2_1  := Matrix(InternalHMFRawHeckeDefinite(M1, p2));
printf "R57|level1 T31,T2 built [%o s] raw dim %o\n", Cputime(t0), Nrows(T31_1);
cp1_31 := Zz!CharacteristicPolynomial(T31_1);
g16 := [ f[1] : f in Factorization(cp1_31) | Degree(f[1]) eq 16 ][1];
g16bar := F2z!g16;
printf "R57|g16bar(31) = %o\n", g16bar;
// T2 on the 16-block (char 0), then mod 2
W16 := Kernel(Evaluate(g16, T31_1));
assert Dimension(W16) eq 16;
B16 := BasisMatrix(W16);
T2_on16 := Solution(B16, B16*T2_1);
cp2_16 := Zz!CharacteristicPolynomial(T2_on16);
printf "R57|charpoly T_p2 on 16-block: %o\n", cp2_16;
printf "R57|... mod 2: %o\n", Factorization(F2z!cp2_16);
// also T97 on the 16-block, for a second residual invariant
t0 := Cputime();
T97_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p97));
printf "R57|level1 T97 built [%o s]\n", Cputime(t0);
T97_on16 := Solution(B16, B16*T97_1);
g16_97 := Zz!CharacteristicPolynomial(T97_on16);
g16bar97 := F2z!g16_97;
printf "R57|g16bar(97) = %o (irreducible %o)\n", g16bar97, IsIrreducible(g16bar97);
cp1_97 := Zz!CharacteristicPolynomial(T97_1);

// ---------------- level p2 ------------------------------------------------
t0 := Cputime();
M := HilbertCuspForms(F, p2, wt);
d := Dimension(M);
printf "R57|level p2 cuspidal dim %o [%o s]\n", d, Cputime(t0);
t0 := Cputime();
T31 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p31));
printf "R57|level p2 T31 built, raw dim %o [%o s]\n", Nrows(T31), Cputime(t0);
cp_31 := Zz!CharacteristicPolynomial(T31);

// old part: two copies of the level-1 raw charpoly
q, r := Quotrem(cp_31, cp1_31^2);
if r ne 0 then
    printf "R57|WARNING cp1_31^2 does not divide cp_31; gcd degree %o\n", Degree(GCD(cp_31, cp1_31^2));
    cp_new31 := ExactQuotient(cp_31, GCD(cp_31, cp1_31^2));
else
    cp_new31 := q;
end if;
printf "R57|p2-new charpoly(T31) degree %o\n", Degree(cp_new31);
printf "R57|p2-new factor degrees over Q: %o\n", [ <Degree(f[1]), f[2]> : f in Factorization(cp_new31) ];
fm := Factorization(F2z!cp_new31);
printf "R57|p2-new charpoly(T31) mod 2 factors: %o\n", [ <f[1], f[2]> : f in fm ];
mult_new := Valuation(F2z!cp_new31, g16bar);
mult_all := Valuation(F2z!cp_31, g16bar);
printf "R57|multiplicity of g16bar in cp_31: total %o, old %o, new %o\n", mult_all, 2*Valuation(F2z!cp1_31, g16bar), mult_new;

// residual eigenspace mod 2 at level p2 (T31 only), and old-part reference
V := Kernel(Evaluate(g16bar, ChangeRing(T31, F2)));
V1 := Kernel(Evaluate(g16bar, ChangeRing(T31_1, F2)));
printf "R57|ker g16bar(T31) mod 2: level1 dim %o, level p2 dim %o (old expectation %o)\n", Dimension(V1), Dimension(V), 2*Dimension(V1);

// U_p2 at level p2
t0 := Cputime();
U := Matrix(InternalHMFRawHeckeDefinite(M, p2));
printf "R57|level p2 U_p2 built [%o s]\n", Cputime(t0);
BV := BasisMatrix(V);
UV := Solution(BV, BV*ChangeRing(U, F2));
printf "R57|U_p2 on V: charpoly %o\n", Factorization(CharacteristicPolynomial(UV));

// char-0 new subspace for T31 and the joint residual test with T97
newfacs := [ f[1] : f in Factorization(cp_new31) ];
Wnew := &+[ Kernel(Evaluate(f, T31)) : f in newfacs ];
printf "R57|W_new (sum of T31-kernels of new factors) dim %o\n", Dimension(Wnew);
t0 := Cputime();
T97 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p97));
printf "R57|level p2 T97 built [%o s]\n", Cputime(t0);
cp_97 := Zz!CharacteristicPolynomial(T97);
printf "R57|multiplicity of g16bar97 in cp_97: total %o, old %o\n", Valuation(F2z!cp_97, g16bar97), 2*Valuation(F2z!cp1_97, g16bar97);

// saturated integral lattice of W_new, reduce Hecke action mod 2
Bn := BasisMatrix(Wnew);
den := LCM([ Denominator(e) : e in Eltseq(Bn) ]);
Bz := Saturation(ChangeRing(den*Bn, Integers()));
Bq := ChangeRing(Bz, Rationals());
T31n := Solution(Bq, Bq*T31);  T97n := Solution(Bq, Bq*T97);  Un := Solution(Bq, Bq*U);
assert &and[ Denominator(e) eq 1 : e in Eltseq(T31n) cat Eltseq(T97n) cat Eltseq(Un) ];
// Solution() returns a vector-space matrix (ModMatFldElt); coerce into the
// matrix algebra so Evaluate(poly, .) accepts it.
MA := MatrixAlgebra(F2, Dimension(Wnew));
T31n2 := MA!ChangeRing(T31n, F2); T97n2 := MA!ChangeRing(T97n, F2); Un2 := MA!ChangeRing(Un, F2);
K31 := Kernel(Evaluate(g16bar, T31n2));
K97 := Kernel(Evaluate(g16bar97, T97n2));
K := K31 meet K97;
printf "R57|on W_new mod 2: ker g16bar(T31) dim %o, ker g16bar97(T97) dim %o, intersection dim %o\n", Dimension(K31), Dimension(K97), Dimension(K);
printf "R57|U_p2 charpoly on W_new (char 0): %o\n", Factorization(Zz!CharacteristicPolynomial(Un));
if Dimension(K) gt 0 then
    BK := BasisMatrix(K);
    UK := Solution(BK, BK*Un2);
    printf "R57|U_p2 on the joint residual space: %o\n", Factorization(CharacteristicPolynomial(UK));
    printf "R57|VERDICT|CONGRUENCE PRESENT: rho-bar_f matches a p2-new eigensystem mod 2 at 31 and 97 (joint dim %o)\n", Dimension(K);
else
    printf "R57|VERDICT|NO CONGRUENCE: rho-bar_f does not occur in the p2-new part (mod 2 at 31 and 97)\n";
end if;
print "PASS|57_levelraise_p2";
quit;
