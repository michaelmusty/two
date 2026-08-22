// Gate 3, step 1: does rho-bar_f occur at level q0?
//
// Decisive necessary condition: the mod-2 invariant g16bar that cuts out
// rho-bar_f at level 1 must divide charpoly(T_ell mod 2) at level q0, and its
// multiplicity bounds the eigenspace.  Measured cost of a dense GF(2) charpoly
// at n = 109240 is ~1.2 h, so this is affordable.
SetColumns(0);
SetMemoryLimit(15*1024^3);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2); F2z<zz> := PolynomialRing(F2);
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;

// --- the residual invariant, from level 1 ---
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M1) eq 57;
T1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp1, rem := Quotrem(Zz!CharacteristicPolynomial(T1), z - (Norm(p31)+1));
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
g16bar := F2z!g16;
printf "C|g16bar = %o\n", g16bar;
printf "C|g16bar irreducible over F_2: %o, degree %o\n",
    IsIrreducible(g16bar), Degree(g16bar);

// --- level q0 ---
load "gate3_T31_sparse.m";                       // sparse T_31 at level q0
printf "C|loaded T31 at level q0: %o x %o\n", Nrows(T31), Ncols(T31);
t0 := Cputime();
A := Matrix(ChangeRing(T31, F2));                // dense GF(2), ~1.49 GB
printf "C|densified [%o s]\n", Cputime(t0);
t0 := Cputime();
cp := CharacteristicPolynomial(A);
printf "C|charpoly done [%o s], degree %o\n", Cputime(t0), Degree(cp);

// --- the test ---
q, r := Quotrem(cp, g16bar);
printf "C|g16bar divides charpoly: %o\n", r eq 0;
m := 0; cc := cp;
while true do
    q, r := Quotrem(cc, g16bar);
    if r ne 0 then break; end if;
    m +:= 1; cc := q;
end while;
printf "C|MULTIPLICITY of g16bar in charpoly(T_31 mod 2) at level q0: %o\n", m;
printf "C|=> residual eigenspace dimension is at most %o\n", m*Degree(g16bar);
printf "C|done\n";
quit;
