// Gate 3, step 7 done right: the eigensystem of the NEW quotient.
//
// WHY 47 WAS NOT ENOUGH (2026-08-26).  W = ker f1(T_31) at level q0 is
// 16-dimensional.  The mod-2 old subspace on the f1 side is ALSO 16-dimensional
// (two copies of the level-1 f1-part, on which T_31 acts semisimply since f1 is
// irreducible with multiplicity 1 at level 1), so O is contained in W, and if
// the mod-2 degeneracy map is injective (Ihara) then W = O exactly.  Restricting
// T_ell to W then only re-derives level-1 data; it says nothing about the new
// forms.  Building O explicitly is expensive (the second degeneracy map needs
// get_tps at q0, the U_q0 cost), but it is not needed:
//
//   charpoly(T_ell | G) = charpoly(T_ell | O) * charpoly(T_ell | G/O),
//
// where G = ker f1(T_31)^2 is the 32-dimensional generalised eigenspace, and
// charpoly(T_ell | O) = (f1^(ell))^2 is forced by the local theory (T_ell
// commutes with both degeneracy maps and acts on each copy as at level 1).
// So   charpoly(T_ell | G) = (f1^(ell))^4   <=>   the new quotient G/O has
// residual T_ell-system f1^(ell) -- the statement gate 3 needs, prime by prime.
//
// Same-session discipline as 46/47: the package basis is not reproducible
// across sessions, so every operator is rebuilt here.
//
// Env: HMF_ROOT, G3_MEMCAP (GB), optional G3_LEVEL (norm of a prime level for
// smoke tests; default q0 = the prime above 7 of norm 2401), optional G3_PRIMES
// (comma-separated rational primes after 31; default 97,127,191).
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2); F2z<zz> := PolynomialRing(F2);
g31e := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31e>;
lev := GetEnv("G3_LEVEL");
if lev eq "" then
    q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
else
    ln := StringToInteger(lev);
    q0 := [ p[1] : p in Factorization(ln*OF) | Norm(p[1]) eq ln ][1];
end if;
prs := [p31];
plist := GetEnv("G3_PRIMES");
if plist eq "" then plist := "97,127,191"; end if;
for s in Split(plist, ",") do
    q := StringToInteger(s);
    pp := [ p[1] : p in Factorization(q*OF) | Norm(p[1]) eq q ];
    if #pp gt 0 and pp[1] ne q0 then Append(~prs, pp[1]); end if;
end for;
printf "GK|level norm %o, primes: %o\n", Norm(q0), [Norm(p) : p in prs];

// --- level 1: V16, the residual factors of T_31, and for each factor the
// --- T_ell charpoly ON that factor's level-1 primary part (so the pairing
// --- f1 <-> f1^(ell) is by the same prime lambda, not by index guessing) ---
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
T31_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp1, rem := Quotrem(Zz!CharacteristicPolynomial(T31_1), z - (Norm(p31)+1));
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
fac31 := [ t[1] : t in Factorization(F2z!g16) ];
printf "GK|level-1 T_31 residual factors: degrees %o\n", [Degree(h) : h in fac31];
A1 := ChangeRing(T31_1, F2);
T1 := AssociativeArray();
for pr in prs do T1[Norm(pr)] := ChangeRing(Matrix(InternalHMFRawHeckeDefiniteSparse(M1, pr)), F2); end for;
// lvl1[idx][n] = charpoly of T_n on the level-1 f_idx-primary part (full generalised kernel)
lvl1 := [* *];
for idx in [1..#fac31] do
    P1 := Evaluate(fac31[idx], A1);
    K1 := Kernel(P1^Nrows(A1));   // generalised eigenspace at level 1
    B1 := BasisMatrix(K1);
    printf "GK|level-1 factor %o: primary dim %o (expect %o = deg*1)\n", idx, Dimension(K1), Degree(fac31[idx]);
    rec := AssociativeArray();
    for pr in prs do
        n := Norm(pr);
        R1 := Solution(B1, B1 * T1[n]);
        rec[n] := CharacteristicPolynomial(R1);
        printf "GK|  level-1 factor %o, T_%o charpoly factors %o\n", idx, n,
            [<Degree(t[1]), t[2]> : t in Factorization(rec[n])];
    end for;
    Append(~lvl1, rec);
end for;

// --- level q0: all operators, one session ---
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
printf "GK|level q0 dim %o\n", Dimension(M);
A := AssociativeArray();
for pr in prs do
    t0 := Cputime();
    S := InternalHMFRawHeckeDefiniteSparse(M, pr);
    // keep the operators SPARSE (dense GF(2) copies cost 1.5 GB each and the
    // first run of this script died at its 16 GB cap at the kernel step)
    A[Norm(pr)] := ChangeRing(S, F2);
    printf "GK|T_%o built [%o s], %o per column, memory %o MB\n",
        Norm(pr), Cputime(t0), RealField(6)!(#Support(S)/Ncols(S)), GetMemoryUsage() div 1024^2;
    // bank the integer operator with a session tag: the four form a commuting
    // set in ONE basis, usable together later (e.g. the Delta' computation over Z)
    if GetEnv("G3_BANK") ne "" then
        Write(Sprintf("%o_T%o.m", GetEnv("G3_BANK"), Norm(pr)), Sprintf("T%o := %m;", Norm(pr), S) : Overwrite := true);
    end if;
end for;
V := VectorSpace(F2, Ncols(A[31])); bad := 0;
for i in [1..3] do
    v := Random(V);
    for pr in prs do for ps in prs do
        if (v*A[Norm(pr)])*A[Norm(ps)] ne (v*A[Norm(ps)])*A[Norm(pr)] then bad +:= 1; end if;
    end for; end for;
end for;
printf "GK|COMMUTE all pairs: failures %o\n", bad;
if bad ne 0 then printf "GK|ABORT: operators do not commute\n"; quit; end if;

// --- which factor carries the excess?  charpoly(T_31 mod 2) at level q0 is
// --- basis-independent, so the banked one (gate3_charpoly_q0.m, variable cp)
// --- can be used to order the factors and skip the non-raising side, whose
// --- generalised kernel is old forms only.  Set G3_ALL=1 to process every factor.
order := [1..#fac31];
bank := GetEnv("G3_CPBANK");
if bank ne "" then
    txt := Read(bank);                       // "cp := Polynomial(GF(2), [...]);"
    i := Index(txt, ":=");
    rhs := txt[i+2..#txt];
    j := Index(rhs, ";");
    cp := eval rhs[1..j-1];
    if Degree(cp) ne Ncols(A[31]) then
        printf "GK|WARNING banked charpoly degree %o != raw dim %o; ignoring bank\n", Degree(cp), Ncols(A[31]);
        cp := F2z!1;
    end if;
    mults := [];
    for idx in [1..#fac31] do
        m := 0; cc := cp;
        while true do
            q, r := Quotrem(cc, fac31[idx]);
            if r ne 0 then break; end if;
            m +:= 1; cc := q;
        end while;
        Append(~mults, m);
    end for;
    printf "GK|banked level-q0 charpoly: factor multiplicities %o (old baseline 2 each)\n", mults;
    order := [ idx : idx in [1..#fac31] | mults[idx] gt 2 ];
    if #order eq 0 or GetEnv("G3_ALL") ne "" then order := [1..#fac31]; end if;
    printf "GK|processing factors in order %o\n", order;
end if;

// --- generalised kernel per residual factor; restrict every operator to it ---
for idx in order do
    f1 := fac31[idx];
    t0 := Cputime();
    A31d := Matrix(A[31]);
    P := Evaluate(f1, A31d);
    delete A31d;
    printf "GK|=== T_31 factor %o (degree %o): f(T_31) evaluated [%o s], memory %o MB\n",
        idx, Degree(f1), Cputime(t0), GetMemoryUsage() div 1024^2;
    t0 := Cputime();
    P2 := P * P;
    printf "GK|  f(T_31)^2 [%o s], memory %o MB\n", Cputime(t0), GetMemoryUsage() div 1024^2;
    t0 := Cputime();
    G := Kernel(P2);
    printf "GK|  dim ker f(T_31)^2 = %o [%o s], memory %o MB\n", Dimension(G), Cputime(t0), GetMemoryUsage() div 1024^2;
    delete P2;
    if Dimension(G) eq 0 then continue; end if;
    BG := BasisMatrix(G);
    // Jordan structure of T_31 on G from the rank of f(T_31) restricted to G
    RP := Solution(BG, BG * P);
    printf "GK|  rank of f(T_31) on G = %o  (0 = semisimple; dim ker f(T_31) = %o)\n",
        Rank(RP), Dimension(G) - Rank(RP);
    delete P;
    for pr in prs do
        n := Norm(pr);
        R := Solution(BG, BG * A[n]);
        cw := CharacteristicPolynomial(R);
        expectedOld := lvl1[idx][n];           // charpoly of T_n on the level-1 primary part
        m := Dimension(G) div Degree(f1);      // multiplicity of f1 at level q0
        // old part contributes expectedOld^2 (two Iwahori-fixed vectors per level-1 form);
        // the new quotient G/O carries whatever remains
        ok, quo := IsDivisibleBy(cw, expectedOld^2);
        printf "GK|  T_%o on G: charpoly factors %o ; divisible by (level-1 charpoly)^2: %o\n",
            n, [<Degree(t[1]), t[2]> : t in Factorization(cw)], ok;
        if ok then
            printf "GK|  T_%o on NEW quotient G/O: charpoly factors %o ; equals level-1 charpoly^%o: %o\n",
                n, [<Degree(t[1]), t[2]> : t in Factorization(quo)], m - 2,
                (m gt 2) select (quo eq expectedOld^(m-2)) else (quo eq 1);
        end if;
    end for;
end for;
printf "GK|done\n";
quit;
