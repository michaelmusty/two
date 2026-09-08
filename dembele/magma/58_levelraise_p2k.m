// Level raising at the prime p2 above 2: conductor p2^k, k >= 2 (the
// "supercuspidal family" left untested by D36 / 57_levelraise_p2.m).
//
// Question: does Dembélé's residual system rho-bar_f (level 1, mod lambda | 2)
// occur in the p2^k-NEW part of the level-p2^k Brandt module of the definite
// discriminant-1 algebra, for some k >= 2?  D36 showed the p2-new part (k = 1,
// Steinberg at p2) carries no copy (a-bar_p2 = omega, not 1).  For k >= 2 the
// p2-component of a new form is supercuspidal or a ramified principal series
// (trivial central character), U_p2 = 0 on it, and nothing is a theorem at
// ell = p = 2 with e = 8, so we compute.
//
// Method (basis-free, char 0): let cp_k = charpoly(T_31) on the raw level-p2^k
// module and cp_new(j) the p2^j-new charpoly (cp_new(0) = raw level 1, which
// includes the Eisenstein factor t - 32 once).  Then
//     cp_new(k) = cp_k / gcd(cp_k, prod_{j<k} cp_new(j)^(k-j+1)),
// whose degree must equal the new dimension, and the residual multiplicity of
// each degree-8 factor f_i of g16bar in cp_new(k) mod 2 is the answer.  Total
// multiplicity in cp_k mod 2 minus the old baseline is printed as a check.
//
// Env: K_MAX (default 4), CONFIRM97 (default 1: at the first k with excess > 0,
// build T_97 and test the joint residual kernel on the saturated new lattice).
// Output markers: R58|... ; per-level verdict R58|VERDICT|k=..|...
SetColumns(0);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");

kmax := StringToInteger(GetEnv("K_MAX") eq "" select "4" else GetEnv("K_MAX"));
confirm97 := GetEnv("CONFIRM97") ne "0";

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
assert Norm(p31) eq 31;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];

// D36 / 57 output, used as a cross-check on the recomputed level-1 invariant
g16bar_ref := zz^16 + zz^14 + zz^13 + zz^12 + zz^11 + zz^9 + zz^8 + zz^7 + zz^6 + zz^4 + zz^2 + zz + 1;

// ---------------- level 1 -------------------------------------------------
t0 := Cputime();
M1 := HilbertCuspForms(F, 1*OF, wt);
assert Dimension(M1) eq 57;
T31_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
printf "R58|level1 T31 built [%o s] raw dim %o\n", Cputime(t0), Nrows(T31_1);
cp1 := Zz!CharacteristicPolynomial(T31_1);
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
g16bar := F2z!g16;
printf "R58|g16bar(31) = %o ; matches D36 reference: %o\n", g16bar, g16bar eq g16bar_ref;
res := [ f[1] : f in Factorization(g16bar) ];
assert #res eq 2 and &and[ Degree(f) eq 8 : f in res ];
printf "R58|residual factors f1 = %o ; f2 = %o\n", res[1], res[2];
printf "R58|level1 residual multiplicities in cp1 mod 2: %o\n", [ Valuation(F2z!cp1, f) : f in res ];

cpnew := AssociativeArray();
cpnew[0] := cp1;
dimnew := AssociativeArray();
dimnew[0] := 58;
// expected new dims from the cuspidal dimensions: 154, 299, 580, 1142, 2249
expected_new := [ 40, 48, 136, 281, 545 ];

// level p2 (k = 1): recomputed here so the old-part subtraction is exact
first_excess_k := 0;
Ms := AssociativeArray();
T31s := AssociativeArray();
for k in [1..kmax] do
    t0 := Cputime();
    M := HilbertCuspForms(F, p2^k, wt);
    d := Dimension(M);
    T31 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p31));
    printf "R58|k=%o cuspidal dim %o raw dim %o ; T31 built [%o s]\n", k, d, Nrows(T31), Cputime(t0);
    Ms[k] := M; T31s[k] := T31;
    cpk := Zz!CharacteristicPolynomial(T31);
    old := &*[ cpnew[j]^(k-j+1) : j in [0..k-1] ];
    g := GCD(cpk, old);
    cpnew[k] := ExactQuotient(cpk, g);
    dimnew[k] := Degree(cpnew[k]);
    printf "R58|k=%o old-part degree %o (product of lower new charpolys has degree %o) ; new degree %o (expected %o)\n",
        k, Degree(g), Degree(old), dimnew[k], expected_new[k];
    facs := Factorization(cpnew[k]);
    printf "R58|k=%o new factor degrees over Q: %o\n", k, [ <Degree(f[1]), f[2]> : f in facs ];
    fm := Factorization(F2z!cpnew[k]);
    printf "R58|k=%o new charpoly(T31) mod 2 factors: %o\n", k, [ <f[1], f[2]> : f in fm ];
    mnew := [ Valuation(F2z!cpnew[k], f) : f in res ];
    mtot := [ Valuation(F2z!cpk, f) : f in res ];
    base := [ &+[ (k-j+1)*Valuation(F2z!cpnew[j], f) : j in [0..k-1] ] : f in res ];
    printf "R58|k=%o residual multiplicities [f1,f2]: total %o, old baseline %o, NEW %o\n", k, mtot, base, mnew;
    // which char-0 new factors carry the residual systems (their degree = d_g at this level)
    for f in facs do
        v := [ Valuation(F2z!f[1], r) : r in res ];
        if v ne [0,0] then
            printf "R58|k=%o char-0 new factor of degree %o (mult %o) reduces with residual multiplicities %o\n", k, Degree(f[1]), f[2], v;
        end if;
    end for;
    // U_p2 on the residual generalized eigenspaces mod 2 (whole raw module)
    try
        t0 := Cputime();
        U := Matrix(InternalHMFRawHeckeDefinite(M, p2));
        printf "R58|k=%o U_p2 built [%o s]\n", k, Cputime(t0);
        T31b := ChangeRing(T31, F2);
        Ub := ChangeRing(U, F2);
        for i in [1..2] do
            Vi := Kernel(Evaluate(res[i], T31b)^mtot[i]);
            BV := BasisMatrix(Vi);
            UV := Solution(BV, BV*Ub);
            printf "R58|k=%o U_p2 on generalized f%o-eigenspace mod 2 (dim %o): charpoly %o\n", k, i, Dimension(Vi), Factorization(CharacteristicPolynomial(UV));
        end for;
        // U_p2 on the char-0 new subspace: expect nilpotent (supercuspidal / ramified PS) for k >= 2
        Wnew := &+[ Kernel(Evaluate(f[1], T31)) : f in facs ];
        printf "R58|k=%o W_new (sum of T31-kernels of new factors) dim %o\n", k, Dimension(Wnew);
        Bn := BasisMatrix(Wnew);
        Un := Solution(Bn, Bn*ChangeRing(U, Rationals()));
        printf "R58|k=%o U_p2 charpoly on W_new (char 0): %o\n", k, Factorization(Zz!CharacteristicPolynomial(Un));
    catch e
        printf "R58|k=%o U_p2 block failed: %o\n", k, e`Object;
    end try;
    if mnew ne [0,0] then
        printf "R58|VERDICT|k=%o|LEVEL RAISING at p2^%o: residual system(s) present in the new part with multiplicities %o\n", k, k, mnew;
        if first_excess_k eq 0 then first_excess_k := k; end if;
    else
        printf "R58|VERDICT|k=%o|no copy of rho-bar_f in the p2^%o-new part (T31 residual multiplicity)\n", k, k;
    end if;
end for;

// ---------------- confirmation at a second prime --------------------------
if confirm97 and first_excess_k gt 0 then
    k := first_excess_k;
    M := Ms[k]; T31 := T31s[k];
    t0 := Cputime();
    T97_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p97));
    printf "R58|confirm k=%o: level1 T97 built [%o s]\n", k, Cputime(t0);
    W16 := Kernel(Evaluate(g16, T31_1));
    B16 := BasisMatrix(W16);
    T97_on16 := Solution(B16, B16*T97_1);
    g16_97 := Zz!CharacteristicPolynomial(T97_on16);
    g16bar97 := F2z!g16_97;
    res97 := [ f[1] : f in Factorization(g16bar97) ];
    printf "R58|confirm k=%o: g16bar(97) = %o ; factors %o\n", k, g16bar97, res97;
    t0 := Cputime();
    T97 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p97));
    printf "R58|confirm k=%o: level p2^%o T97 built [%o s]\n", k, k, Cputime(t0);
    cp97 := Zz!CharacteristicPolynomial(T97);
    printf "R58|confirm k=%o: residual(97) multiplicities in cp(T97) at level p2^%o: %o (level 1: %o)\n", k, k,
        [ Valuation(F2z!cp97, f) : f in res97 ], [ Valuation(F2z!(Zz!CharacteristicPolynomial(T97_1)), f) : f in res97 ];
    facs := Factorization(cpnew[k]);
    Wnew := &+[ Kernel(Evaluate(f[1], T31)) : f in facs ];
    Bn := BasisMatrix(Wnew);
    den := LCM([ Denominator(e) : e in Eltseq(Bn) ]);
    Bz := Saturation(ChangeRing(den*Bn, Integers()));
    Bq := ChangeRing(Bz, Rationals());
    T31n := Solution(Bq, Bq*ChangeRing(T31, Rationals()));
    T97n := Solution(Bq, Bq*ChangeRing(T97, Rationals()));
    assert &and[ Denominator(e) eq 1 : e in Eltseq(T31n) cat Eltseq(T97n) ];
    n := Dimension(Wnew);
    MA := MatrixAlgebra(F2, n);
    T31n2 := MA!ChangeRing(T31n, F2); T97n2 := MA!ChangeRing(T97n, F2);
    for i in [1..2] do
        K31 := Kernel(Evaluate(res[i], T31n2)^n);
        K97s := [ Kernel(Evaluate(f, T97n2)^n) : f in res97 ];
        joint := [ Dimension(K31 meet K) : K in K97s ];
        printf "R58|confirm k=%o: on W_new mod 2, gen. f%o(31)-space dim %o ; joint with gen. spaces of residual(97) factors: %o\n",
            k, i, Dimension(K31), joint;
    end for;
    printf "R58|VERDICT|confirm k=%o|see joint dimensions above (nonzero joint = same residual system at 31 and 97)\n", k;
end if;
print "PASS|58_levelraise_p2k";
quit;
