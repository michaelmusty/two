// Delta' at q0, step (a) of gate5-delta-prime-plan.md Addendum 2026-08-31:
// determine d_g and the global Hecke factor h_g by 2-adic block lifting.
//
// For each deg-8 residual factor f of the level-1 g16 (f1 and f2), lift the
// f-primary block of T_31 at level q0 from mod 2 to mod 2^K, take its block
// charpoly cp_m, divide out the old part u^2 (u = the 2-adic Hensel factor of
// the EXACT level-1 g16 with u = f mod 2), giving h_f (mod 2^K) = the charpoly
// of T_31 on the NEW f-primary part.  By gate 1, only the f1 side raises at
// q0: expected multiplicities are [4, 2] and the f2 block must come out purely
// old (cp_m = u2^2 exactly) -- a built-in machinery check.  A candidate global
// factor is certified by the Deligne bound: roots |a| <= 2*sqrt(31), so a
// degree-d factor has |coeffs| <= C(d, d/2) (2 sqrt 31)^d < 2^141 for d = 32,
// while a NON-global product balanced-lifts to ~2^K-size coefficients; K = 192
// is decisive.  If lift(h_f1) passes, d_g | 16 (its Z-factorization refines);
// if it fails, d_g > 16 and gate 4 is in trouble -- that is a finding, not an
// error.
//
// Block lifting (heavy objects are mod-2 dense, bit-packed):
//   P := f(Tbar), Tbar = T mod 2 sparse;  Pm := P^m, m minimal with
//   dim ker P^m = 8*mult(f);  U = left-ker(Pm) (the block), V = rowspace(Pm)
//   (the stable complement); phi := f^m annihilates the block action Rbar.
//   One RREF with transform on Pm gives the kernel basis B0 AND a solver for
//   x*Pm = y;  one more on E1*Pm (E1 = RREF(Pm)) gives the V-projector.
//   Lift step j -> j+1 with B*T - R*B = 2^j*Err mod 2^{j+1}:
//     Ev := V-part of Err;  H := sum_i phi_i sum_{l<i} Rbar^l (-Ev) Tbar^{i-1-l};
//     C := solve C*Pm = H  (then C*Tbar - Rbar*C = -Ev up to U-rows);
//     S := (C*Tbar - Rbar*C + Err) solved against B0 (rows verified in U);
//     B +:= 2^j*C;  R +:= 2^j*S.
//
// Self-test (small prime level, e.g. G3_LEVEL=31 G3_OPP=97 G3_SELFTEST=1):
// compares the block charpoly against the product of the 2-adic factors of
// the EXACT integer charpoly whose reductions are powers of f.
//
// Env: HMF_ROOT, G3_MEMCAP (GB), G3_LEVEL (norm; default 2401 = q0),
//      G3_OPP (operator's rational split prime; default 31),
//      G3_TBANK (optional banked sparse integer T, e.g. gk_s3_T31.m),
//      G3_MULT (optional comma-separated residual multiplicities, skips the
//               mod-2 charpoly; at q0 use the gate-3 banked values),
//      G3_PREC (default 192), G3_SELFTEST, HG_BANK (output path prefix).
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

function deg1primes(n)
    return [ p[1] : p in Factorization(n*OF) | Norm(p[1]) eq n ];
end function;

lev := GetEnv("G3_LEVEL"); if lev eq "" then lev := "2401"; end if;
ln := StringToInteger(lev);
if ln eq 1 then
    q0 := 1*OF;              // level-1 machinery test: blocks have no old part
elif ln eq 2401 then
    q0 := [p[1]: p in Factorization(7*OF) | Norm(p[1]) eq 2401][1];
else
    q0 := deg1primes(ln)[1];
end if;
opp := GetEnv("G3_OPP"); if opp eq "" then opp := "31"; end if;
ell := StringToInteger(opp);
pell := deg1primes(ell)[1];
K := GetEnv("G3_PREC") eq "" select 192 else StringToInteger(GetEnv("G3_PREC"));
R2K := Integers(2^K);
printf "HG|level norm %o, operator T_%o, precision 2^%o\n", Norm(q0), ell, K;

// ---------- level 1: the exact deg-16 factor and its mod-2 / 2-adic pieces --
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
t1bank := GetEnv("G3_T1BANK");
if t1bank ne "" then
    t1txt := Read(t1bank);
    i0 := Index(t1txt, ":=");
    j0 := #t1txt; while t1txt[j0] ne ";" do j0 -:= 1; end while;
    S1 := eval t1txt[i0+2..j0-1];
    printf "HG|banked level-1 T_%o loaded\n", ell;
else
    t0 := Cputime();
    S1 := InternalHMFRawHeckeDefiniteSparse(M1, pell);
    printf "HG|level-1 T_%o built [%o s]\n", ell, Cputime(t0);
    if GetEnv("G3_T1BANKOUT") ne "" then
        Write(GetEnv("G3_T1BANKOUT"), Sprintf("S1 := %m;", S1) : Overwrite := true);
        printf "HG|level-1 T_%o banked to %o\n", ell, GetEnv("G3_T1BANKOUT");
    end if;
end if;
T1 := Matrix(S1);
cp1, rem1 := Quotrem(Zz!CharacteristicPolynomial(T1), z - (ell+1));
assert rem1 eq 0;
g16 := [ t[1] : t in Factorization(cp1) | Degree(t[1]) eq 16 ][1];
resfacs := [ t[1] : t in Factorization(F2z!g16) ];
printf "HG|level-1 deg-16 factor: residual factor degrees %o\n",
    [Degree(h): h in resfacs];
Zp := pAdicRing(2, K + 32);
Zpz := PolynomialRing(Zp);
ufacs := Factorization(Zpz!g16);
umatch := [* *];
for f in resfacs do
    hits := [ t[1] : t in ufacs |
              F2z![GF(2)| Integers()!c : c in Coefficients(t[1])] eq f ];
    error if #hits ne 1, "2-adic factor of g16 does not match residual factor uniquely";
    Append(~umatch, hits[1]);
end for;

// ---------- the operator at the target level -------------------------------
bank := GetEnv("G3_TBANK");
if bank ne "" then
    txt := Read(bank);
    i0 := Index(txt, ":=");
    j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
    T := eval txt[i0+2..j0-1];
    printf "HG|banked T_%o loaded: %o x %o, %o nonzeros\n",
        ell, Nrows(T), Ncols(T), #Support(T);
elif ln eq 1 then
    T := S1;    // level-1 machinery test: the operator IS the level-1 one
else
    M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
    t0 := Cputime();
    T := InternalHMFRawHeckeDefiniteSparse(M, pell);
    printf "HG|T_%o built [%o s]\n", ell, Cputime(t0);
    if GetEnv("G3_TBANKOUT") ne "" then
        Write(GetEnv("G3_TBANKOUT"), Sprintf("T := %m;", T) : Overwrite := true);
        printf "HG|T_%o banked to %o\n", ell, GetEnv("G3_TBANKOUT");
    end if;
end if;
N := Ncols(T);
Tbar := ChangeRing(T, F2);                       // sparse mod 2 (0/1 entries)
T2K := ChangeRing(T, R2K);                       // sparse mod 2^K

// Tbar * D for dense D, via sparse rows (all nonzero entries are 1 mod 2)
spmul := function(D)
    Rres := Matrix(F2, N, Ncols(D), []);
    for i in [1..N] do
        s := Support(Tbar, i);
        if #s gt 0 then Rres[i] := &+[ D[j] : j in s ]; end if;
    end for;
    return Rres;
end function;

mults := [];
gm := GetEnv("G3_MULT");
if gm ne "" then
    mults := [ StringToInteger(s) : s in Split(gm, ",") ];
    printf "HG|residual multiplicities (given): %o\n", mults;
else
    t0 := Cputime();
    cpbar := CharacteristicPolynomial(Matrix(Tbar));
    printf "HG|charpoly mod 2 [%o s]\n", Cputime(t0);
    for f in resfacs do
        mlt := 0; cc := cpbar;
        while true do
            qq, rr := Quotrem(cc, f);
            if rr ne 0 then break; end if;
            mlt +:= 1; cc := qq;
        end while;
        Append(~mults, mlt);
    end for;
    printf "HG|residual multiplicities in cp mod 2: %o\n", mults;
end if;

selftest := GetEnv("G3_SELFTEST") ne "";
cpZ := Zz!0;   // assigned unconditionally: the factor loop compiles as a unit,
               // so every identifier it mentions must exist even when unused
if selftest then
    t0 := Cputime();
    cpZ := Zz!CharacteristicPolynomial(Matrix(T));
    printf "HG|SELFTEST exact charpoly [%o s]\n", Cputime(t0);
end if;

// quadratic Hensel split of monic cf over Z_2: returns A mod 2^K with
// A = A0 mod 2, A*B = cf mod 2^K, deg A = deg A0; needs gcd(A0, B0) = 1.
function henselSplit(cf, A0z, K)
    cfbar := F2z!cf;
    B0z := cfbar div A0z;
    error if A0z*B0z ne cfbar, "henselSplit: A0 does not divide cf mod 2";
    g, U0, V0 := XGCD(A0z, B0z);
    error if g ne 1, "henselSplit: A0, B0 not coprime mod 2";
    A := Zz![ Integers()!c : c in Coefficients(A0z) ];
    B := Zz![ Integers()!c : c in Coefficients(B0z) ];
    U := Zz![ Integers()!c : c in Coefficients(U0) ];
    V := Zz![ Integers()!c : c in Coefficients(V0) ];
    prec := 1;
    while prec lt K do
        Rh := Integers(2^(2*prec));
        Rhz := PolynomialRing(Rh);
        e := Rhz!cf - (Rhz!A)*(Rhz!B);
        A2 := (Rhz!A) + ((Rhz!V)*e mod Rhz!A);
        B2 := (Rhz!B) + ((Rhz!U)*e mod Rhz!B);
        dd := (Rhz!U)*A2 + (Rhz!V)*B2 - 1;
        U2 := (Rhz!U) - ((Rhz!U)*dd mod B2);
        V2 := (Rhz!V) - ((Rhz!V)*dd mod A2);
        A := Zz![ Integers()!c : c in Coefficients(A2) ];
        B := Zz![ Integers()!c : c in Coefficients(B2) ];
        U := Zz![ Integers()!c : c in Coefficients(U2) ];
        V := Zz![ Integers()!c : c in Coefficients(V2) ];
        prec := 2*prec;
    end while;
    RK := Integers(2^K); RKz := PolynomialRing(RK);
    error if (RKz!cf) ne (RKz!A)*(RKz!B), "henselSplit: lift failed to converge";
    return RKz!A;
end function;

// ---------- per residual factor: lift the block ----------------------------
R2Kz := PolynomialRing(R2K);
results := [* *];
for idx in [1..#resfacs] do
    f := resfacs[idx];
    mult := mults[idx];
    if mult eq 0 then printf "HG|factor %o: multiplicity 0, skipping\n", idx; continue; end if;
    dblk := Degree(f)*mult;
    printf "HG|=== factor %o (deg %o, mult %o): block dim %o\n",
        idx, Degree(f), mult, dblk;

    // P = f(Tbar) dense, Horner with sparse-row products
    t0 := Cputime();
    cfs := Coefficients(f);
    P := MatrixRing(F2, N) ! cfs[#cfs];
    for i := #cfs-1 to 1 by -1 do
        P := spmul(P);
        if cfs[i] eq 1 then P +:= 1; end if;
    end for;
    printf "HG|  P = f(Tbar) dense [%o s]\n", Cputime(t0);

    // smallest m with dim ker P^m = dblk
    m := 1; Pm := P;
    E := 0; Tr := 0; rk := 0;
    while true do
        t0 := Cputime();
        E, Tr := EchelonForm(Pm);                // Tr*Pm = E, E reduced
        rk := Rank(E);
        printf "HG|  rank P^%o = %o (kernel %o, want %o) [%o s]\n",
            m, rk, N-rk, dblk, Cputime(t0);
        if N - rk eq dblk then break; end if;
        error if N - rk gt dblk, "kernel exceeds block dimension: multiplicity wrong";
        error if m ge 2*mult, "kernel did not stabilize by m = 2*mult";
        m +:= 1; Pm := Pm * P;
    end while;
    delete P;
    phi := f^m;
    E1 := RowSubmatrix(E, 1, rk);
    Tr1 := RowSubmatrix(Tr, 1, rk);
    B0 := RowSubmatrix(Tr, rk+1, N-rk);          // block basis mod 2
    delete Tr;
    pivots := [ Min(Support(E1[i])) : i in [1..rk] ];
    delete E;

    // solver: x with x*Pm = y; consistent iff y is in rowspace(Pm) = V
    solvePm := function(y)
        zc := Vector(F2, [ y[pivots[i]] : i in [1..rk] ]);
        return zc*Tr1, (zc*E1) eq y;
    end function;

    // V-projector: yV = (V-component of y) = w*E1 where w*(E1*Pm) = y*Pm
    t0 := Cputime();
    E1Pm := E1*Pm;
    EV, TrV := EchelonForm(E1Pm);
    rkV := Rank(EV);
    error if rkV ne rk, "E1*Pm rank defect: V-projector construction failed";
    pivV := [ Min(Support(EV[i])) : i in [1..rkV] ];
    EV1 := RowSubmatrix(EV, 1, rkV);
    TrV1 := RowSubmatrix(TrV, 1, rkV);
    delete EV; delete TrV; delete E1Pm;
    printf "HG|  V-projector built [%o s]\n", Cputime(t0);
    projV := function(y)
        q := y*Pm;
        wc := Vector(F2, [ q[pivV[i]] : i in [1..rkV] ]);
        error if (wc*EV1) ne q, "V-projection inconsistent";
        return (wc*TrV1)*E1;
    end function;

    // block action mod 2 and the pivot-minor solver for S
    Rbar := Solution(B0, Matrix([ Vector(v*Tbar) : v in Rows(B0) ]));
    EB := EchelonForm(B0);
    bpiv := [ Min(Support(EB[i])) : i in [1..dblk] ];
    BPinv := Submatrix(B0, [1..dblk], bpiv)^-1;
    delete EB;

    // lift to Z/2^K
    B := ChangeRing(ChangeRing(B0, Integers()), R2K);
    R := ChangeRing(ChangeRing(Rbar, Integers()), R2K);
    phicf := Coefficients(phi);
    dphi := Degree(phi);
    t0 := Cputime();
    for j in [1..K-1] do
        BT := Matrix([ Vector(v*T2K) : v in Rows(B) ]);
        ErrZ := ChangeRing(BT - R*B, Integers());
        ErrQ := ChangeRing(ErrZ, Rationals()) * (1/2^j);
        ok := true;
        try G2 := ChangeRing(ChangeRing(ErrQ, Integers()), F2);
        catch e ok := false; end try;
        error if not ok, Sprintf("lift residual not divisible by 2^%o at step %o", j, j);
        if IsZero(G2) then continue; end if;
        Ev := Matrix([ projV(Vector(G2[i])) : i in [1..dblk] ]);
        // H = sum_i phicf[i+1] sum_{l<i} Rbar^l * (-Ev) * Tbar^{i-1-l}
        GT := [ -Ev ];
        for t in [1..dphi-1] do
            Append(~GT, Matrix([ Vector(v*Tbar) : v in Rows(GT[#GT]) ]));
        end for;
        H := Matrix(F2, dblk, N, []);
        Rpow := IdentityMatrix(F2, dblk);
        for l in [0..dphi-1] do
            acc := Matrix(F2, dblk, N, []);
            for i in [l+1..dphi] do
                if phicf[i+1] eq 1 then acc +:= GT[i-l]; end if;
            end for;
            H +:= Rpow*acc;
            Rpow := Rpow*Rbar;
        end for;
        Crows := []; allok := true;
        for i in [1..dblk] do
            xi, oki := solvePm(Vector(H[i]));
            allok and:= oki;
            Append(~Crows, xi);
        end for;
        error if not allok, Sprintf("phi-trick solve inconsistent at step %o", j);
        C := Matrix(Crows);
        // S from the U-part: Delta = C*Tbar - Rbar*C + G2 must have rows in U
        Delta := Matrix([ Vector(v*Tbar) : v in Rows(C) ]) - Rbar*C + G2;
        error if not IsZero(Delta*Pm), Sprintf("residual not in the block at step %o", j);
        S := Submatrix(Delta, [1..dblk], bpiv) * BPinv;
        error if S*B0 ne Delta, Sprintf("S-solve failed at step %o", j);
        B +:= (R2K!2)^j * ChangeRing(ChangeRing(C, Integers()), R2K);
        R +:= (R2K!2)^j * ChangeRing(ChangeRing(S, Integers()), R2K);
    end for;
    printf "HG|  lifted block to 2^%o [%o s]\n", K, Cputime(t0);
    BT := Matrix([ Vector(v*T2K) : v in Rows(B) ]);
    error if BT ne R*B, "lifted block is not T-stable at full precision";
    printf "HG|  CHECK block T-stable mod 2^%o: true\n", K;
    delete Pm; delete E1; delete Tr1; delete EV1; delete TrV1;

    cpm := CharacteristicPolynomial(ChangeRing(R, Integers()));
    cpmK := R2Kz!cpm;
    printf "HG|  block charpoly degree %o\n", Degree(cpmK);

    if selftest then
        exK := R2Kz!henselSplit(cpZ, f^mult, K);
        printf "HG|  SELFTEST block charpoly matches exact 2-adic factor: %o\n",
            cpmK eq exK;
    end if;

    // old part: u^mult_old, mult_old = 2 at prime level
    uK := R2Kz![ R2K!(Integers()!c) : c in Coefficients(umatch[idx]) ];
    hf, remf := Quotrem(cpmK, uK^2);
    exact := IsZero(remf);
    printf "HG|  CHECK cp_m divisible by u^2 (old part): %o ; new-part degree %o\n",
        exact, Degree(hf);
    Append(~results, <idx, exact select hf else R2Kz!0>);

    if GetEnv("HG_BANK") ne "" then
        Write(Sprintf("%o_f%o.m", GetEnv("HG_BANK"), idx),
              Sprintf("Rblk%o := %m;\n", idx, ChangeRing(R, Integers()))
              : Overwrite := true);
    end if;
end for;

// ---------- candidates and the Deligne coefficient bound -------------------
function balanced(pol, K)
    return Zz![ (c lt 2^(K-1)) select c else c - 2^K where c is Integers()!co
              : co in Coefficients(pol) ];
end function;
bound := func< d, l | Binomial(d, d div 2) * Ceiling(2*Sqrt(l))^d >;
cands := [* *];
for t in results do
    if Degree(t[2]) gt 0 then Append(~cands, <Sprintf("h_f%o", t[1]), t[2]>); end if;
end for;
if #cands eq 2 then Append(~cands, <"h_f1*h_f2", cands[1][2]*cands[2][2]>); end if;
printf "HG|candidate global factors (balanced lifts, Deligne bound test):\n";
for c in cands do
    bl := balanced(c[2], K);
    d := Degree(bl);
    mx := Max([ Abs(co) : co in Coefficients(bl) ]);
    okb := mx le bound(d, ell);
    printf "HG|  %o: degree %o, max |coeff| ~2^%o, bound ~2^%o, GLOBAL: %o\n",
        c[1], d, Ilog2(Max(mx,1)), Ilog2(bound(d, ell)), okb;
    if okb then
        printf "HG|  %o = %o\n", c[1], bl;
        printf "HG|  %o factors over Z: %o\n", c[1],
            [ <Degree(u[1]), u[2]> : u in Factorization(bl) ];
        printf "HG|  %o mod 2 factors: %o\n", c[1],
            [ <Degree(u[1]), u[2]> : u in Factorization(F2z!bl) ];
    end if;
end for;
printf "HG|done\n";
quit;
