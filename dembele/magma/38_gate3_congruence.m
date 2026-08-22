// Gate 3: verify the level-raising congruence directly at level q0.
//
// q0 = prime of F above 7, norm 2401 (D23).  Ribet-style level raising
// PREDICTS a newform g of level q0, Steinberg at q0, with rho-bar_g = rho-bar_f.
// The plan of record deliberately verifies this rather than assuming it.
//
// Method.  Work mod 2.  The level-q0 space has dim 109240; over F_2 even a
// dense matrix is only 109240^2/8 = 1.49 GB, so the linear algebra is cheap
// once the operators can be BUILT (which needs the two sparse patches, see
// dembele/patches/).
//
//   1. From level 1, recover the mod-2 factor g16 cutting out rho-bar
//      (the degree-16 factor of charpoly(T_31), reduced mod 2).
//   2. At level q0, compute T_ell sparsely for several small ell, reduce mod 2.
//   3. Intersect the kernels of g16(T_ell) -- the subspace where the residual
//      eigensystem matches rho-bar_f.
//   4. On that subspace, check U_q0 = +-1: Steinberg at q0.
//
// A nonzero result at step 3 with step 4 passing IS the congruence, verified.
SetColumns(0);
SetMemoryLimit(StringToInteger(GetEnv("G3_MEMCAP"))*1024^3);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2);
F2z<zz> := PolynomialRing(F2);

// ---- step 1: the residual invariant, from level 1 -------------------------
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M1) eq 57;
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
T31 := InternalHMFRawHeckeDefiniteSparse(M1, p31);
cp, rem := Quotrem(Zz!CharacteristicPolynomial(Matrix(T31)), z - (Norm(p31)+1));
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp) | Degree(f[1]) eq 16 ][1];
g16bar := F2z!g16;
printf "G3|g16 mod 2 = %o  (irreducible: %o)\n", g16bar, IsIrreducible(g16bar);

// ---- step 2/3: at level q0, cut out the matching residual eigenspace ------
q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
t0 := Cputime();
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
d := Dimension(M);
printf "G3|level q0 dim %o [%o s]\n", d, Cputime(t0);

ells := [];
for q in [31, 97, 127, 191] do
    pp := [ p[1] : p in Factorization(q*OF) | Norm(p[1]) eq q ];
    if #pp gt 0 then Append(~ells, pp[1]); end if;
end for;

V := 0;
for pr in ells do
    t0 := Cputime();
    T := InternalHMFRawHeckeDefiniteSparse(M, pr);
    printf "G3|T_%o built, %o nonzeros [%o s]\n", Norm(pr), #Support(T), Cputime(t0);
    T2 := Matrix(ChangeRing(T, F2));           // dense over F_2: ~1.5 GB
    K := Kernel(Evaluate(g16bar, T2));
    printf "G3|ker g16bar(T_%o) has dim %o\n", Norm(pr), Dimension(K);
    V := (V cmpeq 0) select K else V meet K;
    printf "G3|running intersection dim %o\n", Dimension(V);
    if Dimension(V) eq 0 then
        printf "G3|FAIL no residual eigenspace matches rho-bar at level q0\n";
        quit;
    end if;
end for;

// ---- step 4: Steinberg at q0 ---------------------------------------------
printf "G3|RESIDUAL EIGENSPACE dim %o\n", Dimension(V);
U := InternalHMFRawHeckeDefiniteSparse(M, q0);
U2 := Matrix(ChangeRing(U, F2));
BV := BasisMatrix(V);
img := BV * U2;
sol := Solution(BV, img);                       // U_q0 restricted to V
printf "G3|U_q0 on V: scalar=%o\n", sol eq Parent(sol)!1;
printf "G3|U_q0 charpoly on V = %o\n", Factorization(CharacteristicPolynomial(sol));
printf "G3|done\n";
quit;
