// Gate 3, step 2: does the excess persist at a SECOND prime?
//
// At ell = 31 the two degree-8 residual factors had multiplicities 4 and 2 at
// level q0, against an oldform baseline of 2 each -- exactly one system carries
// an excess, and it is the one gate 1 singled out.  One prime leaves room for
// coincidence.  This repeats the measurement at ell = 97.
//
// Note the invariant is ell-specific: for each ell it is the degree-16 charpoly
// of T_ell restricted to V16 at level 1, reduced mod 2 and factored.  (V16
// itself is still cut out by T_31, as in the scan.)
SetColumns(0);
SetMemoryLimit(StringToInteger(GetEnv("G3_MEMCAP"))*1024^3);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2); F2z<zz> := PolynomialRing(F2);
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];

// --- level 1: cut out V16 with T_31, then take T_97 on it ---
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M1) eq 57;
T31 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp31, rem := Quotrem(Zz!CharacteristicPolynomial(T31), z - (Norm(p31)+1));
assert rem eq 0;
g16_31 := [ f[1] : f in Factorization(cp31) | Degree(f[1]) eq 16 ][1];
V16 := Kernel(Evaluate(g16_31, ChangeRing(T31, Rationals())));
assert Dimension(V16) eq 16;
B16 := BasisMatrix(V16);
printf "E97|V16 built (dim %o)\n", Dimension(V16);

T97_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p97));
Sol := Solution(B16, B16 * ChangeRing(T97_1, Rationals()));
cp16_97 := Zz!CharacteristicPolynomial(Sol);
printf "E97|charpoly(T_97|V16) degree %o\n", Degree(cp16_97);
fac := Factorization(F2z!cp16_97);
printf "E97|mod 2 factors: %o\n", [<Degree(t[1]), t[2]> : t in fac];

// --- level q0 ---
q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
printf "E97|level q0 dim %o\n", Dimension(M);
t0 := Cputime();
T := InternalHMFRawHeckeDefiniteSparse(M, p97);
printf "E97|T_97 at q0: %o nonzeros, %o per column [%o s]\n",
    #Support(T), RealField(6)!(#Support(T)/Ncols(T)), Cputime(t0);
Write("gate3_T97_sparse.m", Sprintf("T97 := %m;", T) : Overwrite := true);
t0 := Cputime();
cp := CharacteristicPolynomial(Matrix(ChangeRing(T, F2)));
printf "E97|charpoly degree %o [%o s]\n", Degree(cp), Cputime(t0);
Write("gate3_charpoly97_q0.m", Sprintf("cp97 := %m;", cp) : Overwrite := true);

printf "E97|oldform baseline is multiplicity 2 per factor\n";
for t in fac do
    h := t[1];
    if Degree(h) eq 0 then continue; end if;
    m := 0; cc := cp;
    while true do
        qq, r := Quotrem(cc, h);
        if r ne 0 then break; end if;
        m +:= 1; cc := qq;
    end while;
    printf "E97|RESULT factor deg %o (mult %o in the level-1 invariant): multiplicity %o at q0, EXCESS %o\n",
        Degree(h), t[2], m, m - 2*t[2];
end for;
printf "E97|done\n";
quit;
