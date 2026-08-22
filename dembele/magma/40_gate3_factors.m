// Gate 3, step 1b: test the DEGREE-8 factors, not the degree-16 invariant.
//
// H has degree 16 with two primes lambda, lambda' above 2, each of residue
// degree 8 -- Dembele's two residual systems.  So g16 mod 2 factors into
// degree-8 pieces, one per system.  The gate-1 hit was const2val = 8, i.e.
// v_lambda + v_lambda' = 1: EXACTLY ONE system has abar_q0 = 0.  So the right
// test at level q0 is whether the corresponding degree-8 factor divides
// charpoly(T_31 mod 2) -- testing the full degree-16 product would report a
// false negative precisely in the expected case.
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

M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
T1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp1, rem := Quotrem(Zz!CharacteristicPolynomial(T1), z - (Norm(p31)+1));
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
g16bar := F2z!g16;
fac := Factorization(g16bar);
printf "F|g16bar factors as: %o\n", fac;
for t in fac do
    printf "F|  factor degree %o multiplicity %o irreducible %o\n",
        Degree(t[1]), t[2], IsIrreducible(t[1]);
end for;

load "gate3_charpoly_q0.m";      // cp := charpoly(T_31 mod 2) at level q0
printf "F|loaded charpoly of degree %o\n", Degree(cp);
for t in fac do
    h := t[1];
    m := 0; cc := cp;
    while true do
        q, r := Quotrem(cc, h);
        if r ne 0 then break; end if;
        m +:= 1; cc := q;
    end while;
    printf "F|RESULT factor of degree %o : multiplicity %o at level q0 => eigenspace <= %o\n",
        Degree(h), m, m*Degree(h);
end for;
printf "F|done\n";
quit;
