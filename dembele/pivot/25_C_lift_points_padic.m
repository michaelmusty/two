// D174, package 4: lift 2-torsion classes of J(C) to precision 31^N and
// evaluate f_x. Everything is expressed in Taylor coefficients at P32:
//  - the expansion of C at P32 over Z/p^N (same anchor and parameter as mod p),
//    Taylor coefficients of the 105 quartic monomials;
//  - B_j = quartics vanishing to order >= j at P32 (kernels lifted from mod p);
//  - unknowns (g, h, g') in B_88 x B_87 x B_86 over W = W_N(F_p^17), equation
//    g*g' = h^2. A section of 8K - 174*P32 (degree 66) vanishing to order 67
//    more is zero, so the equation is the vanishing of the coefficients of
//    t^174..t^240 of g*g' - h^2: 67 equations, 54 unknowns, 3 pinned (gauge
//    s_A -> nu*s_A, s_B -> lambda*s_B + mu*s_A), Jacobian rank 51.
//  - Newton with the inverse Jacobian updated at each step (precision doubles;
//    each step runs in the ring of its target precision, and the last step
//    does not update the inverse).
// Output: Taylor coefficients c_88..c_93 of f_x = g (up to one scalar per point).
// Files: curve and marks, padic_lib.m, output of script 24.
// Env: PREC, IN, OUT, FIRST, LAST.
SetQuitOnError(true); SetColumns(0);
started := Cputime();
N := StringToInteger(GetEnv("PREC")); OUT := GetEnv("OUT");
FIRST := StringToInteger(GetEnv("FIRST")); LAST := StringToInteger(GetEnv("LAST"));
p := 31; Fp := GF(p); AEXT := 17; K := GF(p, AEXT); ZN := Integers(p^N);
LIBP := p; LIBF := Fp; LC0 := 0; LC1 := 0;
load "padic_lib.m";
k := Rationals();
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
c16_in := Read(GetEnv("IN")); c16_stmts := Split(c16_in, ";");
quad := eval Split(c16_stmts[1], "=")[2]; pairs4 := eval Split(c16_stmts[2], "=")[2];
c16_modulus := eval Split(c16_stmts[3], "=")[2]; recs := eval Split(c16_stmts[4], "=")[2];
assert [ZZ!c : c in Coefficients(DefiningPolynomial(K))] eq c16_modulus;
function DecKE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..AEXT]];
    return K!s;
end function;

// --- expansion of C at P32 over Z/p^N ---
PT := 155;
rowsZ := Matrix(ZN, rows);
Lmat := [ZeroMatrix(ZN, 91, 16) : j in [1..16]];
for t in [1..#pairs] do
    a := pairs[t][1]; c := pairs[t][2];
    for i in [1..91] do
        Lmat[a][i, c] +:= rowsZ[i, t];
        Lmat[c][i, a] +:= rowsZ[i, t];
    end for;
end for;
ptq := [ZN!c : c in P32_coordinates];
anchor := Min([i : i in [1..16] | (ZZ!ptq[i]) mod p ne 0]);
ptq := [c*ptq[anchor]^-1 : c in ptq];
vars := [i : i in [1..16] | i ne anchor];
ptc := Matrix(ZN, 16, 1, ptq);
Jq := HorizontalJoin([Lmat[j]*ptc : j in vars]);
indsP := IndRows(Red(Jq)); assert #indsP eq 14;
param := 0;
for cand in vars do
    depsP := [j : j in vars | j ne cand];
    matP := Rows_(HorizontalJoin([Lmat[j]*ptc : j in depsP]), indsP);
    if Determinant(Red(matP)) ne 0 then param := cand; break; end if;
end for;
assert param ne 0;
Minv := InvN(matP);
rsel := Rows_(rowsZ, indsP);
xsc := [[ptq[j]] : j in [1..16]];
for n in [1..PT-1] do
    for j in [1..16] do Append(~xsc[j], ZN!((n eq 1 and j eq param) select 1 else 0)); end for;
    conv := Matrix(ZN, #pairs, 1, [&+[xsc[pr[1]][m+1]*xsc[pr[2]][n-m+1] : m in [0..n]] : pr in pairs]);
    corr := -Minv*(rsel*conv);
    for j in [1..14] do xsc[depsP[j]][n+1] := corr[j, 1]; end for;
end for;
PZ<xx> := PolynomialRing(ZN);
xpol := [PZ!s : s in xsc];
function Trunc(f) return PZ![Coefficient(f, j) : j in [0..PT-1]]; end function;
assert &and[IsZero(Trunc(&+[rowsZ[i, t]*xpol[pairs[t][1]]*xpol[pairs[t][2]] : t in [1..#pairs]])) : i in [1..91]];
s2 := [Trunc(xpol[pr[1]]*xpol[pr[2]]) : pr in quad];
s4 := [Trunc(s2[pr[1]]*s2[pr[2]]) : pr in pairs4];
T4N := Matrix(ZN, [[Coefficient(m, j) : j in [0..PT-1]] : m in s4]);            // 105 x PT
printf "S25|N = %o; expansion at P32 to t^%o (anchor %o, parameter %o) [%o s]\n", N, PT, anchor, param, Cputime(started);
BN := [* KerN(ColumnSubmatrix(T4N, 1, j)) : j in [88, 87, 86] *];
dims := [Nrows(B) : B in BN]; assert dims eq [17, 18, 19];
NU := &+dims; NEQ := 67;
// Taylor coefficients t^j..t^(j+66) of the bases
SBN := [* BN[i]*ColumnSubmatrix(T4N, [88, 87, 86][i] + 1, NEQ) : i in [1..3] *];
BK := [* ChangeRing(Red(B), K) : B in BN *];
SBK := [* ChangeRing(Red(S), K) : S in SBN *];
printf "S25|bases of B_88, B_87, B_86 lifted [%o s]\n", Cputime(started);

// --- W = W_e(K) at each precision level e ---
phiZ := PolynomialRing(ZZ)![ZZ!c : c in Coefficients(DefiningPolynomial(K))];
function Level(e)
    Re := Integers(p^e);
    PWZe := PolynomialRing(Re);
    WQe := quo<PWZe | PWZe!phiZ>;
    PWe := PolynomialRing(WQe);
    SBWe := [* [PWe![WQe!(Re!(ZZ!c)) : c in Eltseq(S[b])] : b in [1..Nrows(S)]] : S in SBN *];
    return <Re, PWZe, WQe, PWe, SBWe>;
end function;
function WSeqL(x, L) s := Coefficients(L[2]!x); return [ZZ!c : c in s] cat [0 : i in [#s+1..AEXT]]; end function;
function ToL(seq, L) return L[3]!(L[2]!seq); end function;
function Series(x, L)       // x: sequence of NU elements of W -> G, H, Gp (polynomials of degree <= 66)
    S := L[5];
    G := &+[x[b]*S[1][b] : b in [1..17]];
    H := &+[x[17+b]*S[2][b] : b in [1..18]];
    Gp := &+[x[35+b]*S[3][b] : b in [1..19]];
    return G, H, Gp;
end function;
function Res(x, L)
    G, H, Gp := Series(x, L);
    f := G*Gp - H^2;
    return [Coefficient(f, j) : j in [0..NEQ-1]], G;
end function;
function Jac(x, I, Jc, L)
    G, H, Gp := Series(x, L); S := L[5];
    rws := [];
    for u in I do
        if u le 17 then f := S[1][u]*Gp;
        elif u le 35 then f := -2*S[2][u-17]*H;
        else f := S[3][u-35]*G; end if;
        Append(~rws, [Coefficient(f, j-1) : j in Jc]);
    end for;
    return Matrix(L[3], #I, #Jc, &cat rws);
end function;

// Newton: at each level the ring has the target precision e2 = min(2e, N); the
// inverse Jacobian (correct mod p^e) is lifted, x is corrected, and the inverse
// is updated only if another level follows.
function LiftRecord(rec)
    t0 := Cputime();
    v := [Vector(K, [DecKE(c) : c in rec[2+i]]) : i in [1..3]];        // g, h, g' in the quartic basis
    x0 := &cat[Eltseq(Solution(BK[i], v[i])) : i in [1..3]];
    PK<tk> := PolynomialRing(K);
    sk := [* [PK!Eltseq(SBK[i][b]) : b in [1..dims[i]]] : i in [1..3] *];
    GK := &+[x0[b]*sk[1][b] : b in [1..17]]; HK := &+[x0[17+b]*sk[2][b] : b in [1..18]]; GpK := &+[x0[35+b]*sk[3][b] : b in [1..19]];
    assert &and[Coefficient(GK*GpK - HK^2, j) eq 0 : j in [0..NEQ-1]];
    JK := Matrix(K, [[Coefficient(f, j) : j in [0..NEQ-1]] : f in [sk[1][b]*GpK : b in [1..17]] cat [-2*sk[2][b]*HK : b in [1..18]] cat [sk[3][b]*GK : b in [1..19]]]);
    I := IndRows(JK); assert #I eq NU - 3;
    Jc := PivCols(Rows_(JK, I)); assert #Jc eq #I;
    XK := Cols_(Rows_(JK, I), Jc)^-1;
    xs := [[ZZ!c : c in Eltseq(u)] : u in x0];                         // integer coordinates of x
    Xs := [[ZZ!c : c in Eltseq(u)] : u in Eltseq(XK)];                 // of the inverse (row-major)
    steps := 0; e := 1; tl := [];
    while e lt N do
        ts := Cputime();
        e2 := Min(2*e, N); L := Level(e2);
        x := [ToL(u, L) : u in xs];
        Xinv := Matrix(L[3], #I, #I, [ToL(u, L) : u in Xs]);
        F := Res(x, L);
        d := Matrix(L[3], 1, #Jc, [F[j] : j in Jc])*Xinv;
        for i in [1..#I] do x[I[i]] -:= d[1, i]; end for;
        if e2 lt N then
            Xinv := Xinv*(ScalarMatrix(L[3], #I, 2) - Jac(x, I, Jc, L)*Xinv);
            Xs := [WSeqL(u, L) : u in Eltseq(Xinv)];
        end if;
        xs := [WSeqL(u, L) : u in x];
        steps +:= 1; e := e2; Append(~tl, Cputime(ts));
    end while;
    L := Level(N); x := [ToL(u, L) : u in xs];
    F, G := Res(x, L);
    assert &and[c eq 0 : c in F];
    co := [WSeqL(Coefficient(G, j), L) : j in [0..5]];
    // mod p: the stored r = (c_89..c_93)/c_88
    rst := [DecKE(c) : c in rec[6]];
    ck := [K![Fp!c : c in u] : u in co];
    okp := ck[1] ne 0 and [ck[j+1]/ck[1] : j in [1..5]] eq rst;
    return co, okp, steps, Cputime(t0), tl;
end function;

PrintFile(OUT, Sprintf("// f_x Taylor coefficients t^88..t^93 at P32 modulo %o^%o; <prime index, representative, 6 x 17 integers>", p, N) : Overwrite := true);
for ri in [FIRST..Min(LAST, #recs)] do
    rec := recs[ri];
    co, okp, steps, tm, tl := LiftRecord(rec);
    PrintFile(OUT, Sprintf("<%o, %o, %o>,", rec[1], rec[2], co));
    printf "S25|record %o (%o,%o): Newton steps %o; all 67 residuals zero mod p^%o; reduces to the stored r: %o; %o s; last steps %o\n", ri, rec[1], rec[2], steps, N, okp, tm, tl[Max(1, #tl-2)..#tl];
    assert okp;
end for;
printf "DONE|25_C_LIFT [%o s]\n", Cputime(started);
quit;
