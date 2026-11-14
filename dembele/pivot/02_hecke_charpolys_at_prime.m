// D158 step 2 input: characteristic polynomials of T_P, P a prime of F, on
// the p2-new (40-dim, split as 16 + 24) and p2^2-new (48-dim) spaces, the
// spaces being cut out by the banked T31 new characteristic polynomials
// (dembele/data/computed/levelraise_p2k_charpolys.m, script 58).
// Env: HMF_ROOT, BANK (path to the bank file), GEN (8 comma-separated
// integer coordinates of a generator of P in the power basis of b).
// Output: C02|... lines; polynomials in z are charpolys of T_P.
SetColumns(0);
SetQuitOnError(true);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
wt := [2 : i in [1..8]];
p2 := Factorization(2*OF)[1][1];
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
gen := F![StringToInteger(s) : s in Split(GetEnv("GEN"), ",")];
P := ideal<OF | OF!gen>;
assert IsPrime(P);
printf "C02|prime gen %o norm %o\n", Eltseq(gen), Norm(P);
bank := eval Read(GetEnv("BANK"));
cp40 := Zz!bank[2]; cp48 := Zz!bank[3];
assert Degree(cp40) eq 40 and Degree(cp48) eq 48;
f40 := [f[1] : f in Factorization(cp40)];
quartics := [f : f in f40 | Degree(f) eq 4];
f24 := [f : f in f40 | Degree(f) eq 24];
assert #quartics eq 4 and #f24 eq 1;
restrict := function(T31, TP, f)
    W := Kernel(Evaluate(f, ChangeRing(T31, Rationals())));
    assert Dimension(W) eq Degree(f);
    B := BasisMatrix(W);
    return Zz!CharacteristicPolynomial(Solution(B, B*ChangeRing(TP, Rationals())));
end function;
for k in [1, 2] do
    t0 := Cputime();
    M := HilbertCuspForms(F, p2^k, wt);
    T31 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p31));
    printf "C02|k=%o raw dim %o T31 built [%o s]\n", k, Nrows(T31), Cputime(t0);
    t0 := Cputime();
    TP := Matrix(InternalHMFRawHeckeDefiniteSparse(M, P));
    printf "C02|k=%o TP built [%o s]\n", k, Cputime(t0);
    assert T31*TP eq TP*T31;
    PrintFile(GetEnv("OUTDIR") cat "/TP_k" cat IntegerToString(k) cat ".m", Eltseq(TP) : Overwrite := true);
    if k eq 1 then
        for i in [1..4] do
            printf "C02|k=1|quartic %o|T31 factor %o|TP charpoly %o\n", i, quartics[i], restrict(T31, TP, quartics[i]);
        end for;
        printf "C02|k=1|p16|%o\n", &*[restrict(T31, TP, q) : q in quartics];
        printf "C02|k=1|p24|%o\n", restrict(T31, TP, f24[1]);
    else
        printf "C02|k=2|p48|%o\n", restrict(T31, TP, cp48);
    end if;
end for;
printf "C02|DONE\n";
quit;
