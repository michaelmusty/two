// Resume the ell=97 test from the banked operator.
// The 60-minute T_97 build succeeded (10,699,599 nonzeros, 97.94 per column
// against the predicted Norm(p)+1 = 98) and was written to disk before the
// charpoly hit a memory cap I had set from the ell=31 job's 4.6 GB peak -- the
// charpoly here wants ~7.5 GB.  Only the charpoly and the level-1 invariant
// need redoing.
SetColumns(0);
SetMemoryLimit(StringToInteger(GetEnv("G3_MEMCAP"))*1024^3);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2); F2z<zz> := PolynomialRing(F2);
g31e := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31e>;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];

M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
T31 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp31, rem := Quotrem(Zz!CharacteristicPolynomial(T31), z - (Norm(p31)+1));
assert rem eq 0;
g16_31 := [ f[1] : f in Factorization(cp31) | Degree(f[1]) eq 16 ][1];
B16 := BasisMatrix(Kernel(Evaluate(g16_31, ChangeRing(T31, Rationals()))));
T97_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p97));
cp16_97 := Zz!CharacteristicPolynomial(Solution(B16, B16 * ChangeRing(T97_1, Rationals())));
fac := Factorization(F2z!cp16_97);
Write("gate3_inv97.m", Sprintf("cp16_97 := %m;", cp16_97) : Overwrite := true);
printf "R97|level-1 invariant factors: %o\n", [<Degree(t[1]), t[2]> : t in fac];

load "gate3_T97_sparse.m";
printf "R97|loaded T_97 at q0: %o nonzeros\n", #Support(T97);
t0 := Cputime();
cp := CharacteristicPolynomial(Matrix(ChangeRing(T97, F2)));
printf "R97|charpoly degree %o [%o s]\n", Degree(cp), Cputime(t0);
Write("gate3_charpoly97_q0.m", Sprintf("cp97 := %m;", cp) : Overwrite := true);

printf "R97|oldform baseline is 2 per level-1 factor multiplicity\n";
for t in fac do
    h := t[1];
    if Degree(h) eq 0 then continue; end if;
    m := 0; cc := cp;
    while true do
        qq, r := Quotrem(cc, h);
        if r ne 0 then break; end if;
        m +:= 1; cc := qq;
    end while;
    printf "R97|RESULT deg %o : multiplicity %o at q0, baseline %o, EXCESS %o\n",
        Degree(h), m, 2*t[2], m - 2*t[2];
end for;
printf "R97|done\n";
quit;
