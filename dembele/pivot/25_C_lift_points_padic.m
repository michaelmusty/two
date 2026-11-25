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
//  - Newton with the inverse Jacobian updated at each step (precision doubles).
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

// --- W = W_N(K) ---
phiZ := PolynomialRing(ZZ)![ZZ!c : c in Coefficients(DefiningPolynomial(K))];
PWZ<yy> := PolynomialRing(ZN);
WQ<om> := quo<PWZ | PWZ!phiZ>;
PW<t> := PolynomialRing(WQ);
function KtoW(c) return WQ!(PWZ![ZZ!e : e in Eltseq(c)]); end function;
function WSeq(x) s := Coefficients(PWZ!x); return [ZZ!c : c in s] cat [0 : i in [#s+1..AEXT]]; end function;
function WtoK(x) return K![Fp!c : c in WSeq(x)]; end function;
SBW := [* [PW![WQ!c : c in Eltseq(S[b])] : b in [1..Nrows(S)]] : S in SBN *];
function Series(x)       // x: sequence of NU elements of WQ -> G, H, Gp (polynomials of degree <= 66)
    G := &+[x[b]*SBW[1][b] : b in [1..17]];
    H := &+[x[17+b]*SBW[2][b] : b in [1..18]];
    Gp := &+[x[35+b]*SBW[3][b] : b in [1..19]];
    return G, H, Gp;
end function;
function Lo(f) return [Coefficient(f, j) : j in [0..NEQ-1]]; end function;
function Res(x)
    G, H, Gp := Series(x);
    return Lo(G*Gp - H^2), G;
end function;
function Jac(x, I, Jc)
    G, H, Gp := Series(x);
    rws := [];
    for u in I do
        if u le 17 then f := SBW[1][u]*Gp;
        elif u le 35 then f := -2*SBW[2][u-17]*H;
        else f := SBW[3][u-35]*G; end if;
        Append(~rws, [Coefficient(f, j-1) : j in Jc]);
    end for;
    return Matrix(WQ, #I, #Jc, &cat rws);
end function;

function LiftRecord(rec)
    t0 := Cputime();
    v := [Vector(K, [DecKE(c) : c in rec[2+i]]) : i in [1..3]];        // g, h, g' in the quartic basis
    x0 := &cat[Eltseq(Solution(BK[i], v[i])) : i in [1..3]];
    // Jacobian mod p
    PK<tk> := PolynomialRing(K);
    sk := [* [PK!Eltseq(SBK[i][b]) : b in [1..dims[i]]] : i in [1..3] *];
    GK := &+[x0[b]*sk[1][b] : b in [1..17]]; HK := &+[x0[17+b]*sk[2][b] : b in [1..18]]; GpK := &+[x0[35+b]*sk[3][b] : b in [1..19]];
    assert &and[Coefficient(GK*GpK - HK^2, j) eq 0 : j in [0..NEQ-1]];
    JK := Matrix(K, [[Coefficient(f, j) : j in [0..NEQ-1]] : f in [sk[1][b]*GpK : b in [1..17]] cat [-2*sk[2][b]*HK : b in [1..18]] cat [sk[3][b]*GK : b in [1..19]]]);
    I := IndRows(JK); assert #I eq NU - 3;
    Jc := PivCols(Rows_(JK, I)); assert #Jc eq #I;
    XK := Cols_(Rows_(JK, I), Jc)^-1;
    Xinv := Matrix(WQ, #I, #I, [KtoW(c) : c in Eltseq(XK)]);
    x := [KtoW(c) : c in x0];
    two := ScalarMatrix(WQ, #I, 2);
    steps := 0; e := 1;
    while true do
        F, G := Res(x);
        if &and[c eq 0 : c in F] then break; end if;
        assert e lt 2*N;
        d := Matrix(WQ, 1, #Jc, [F[j] : j in Jc])*Xinv;
        for i in [1..#I] do x[I[i]] -:= d[1, i]; end for;
        Xinv := Xinv*(two - Jac(x, I, Jc)*Xinv);
        steps +:= 1; e *:= 2;
    end while;
    F, G := Res(x);
    assert &and[c eq 0 : c in F];
    co := [Coefficient(G, j) : j in [0..5]];
    // mod p: the stored r = (c_89..c_93)/c_88
    rst := [DecKE(c) : c in rec[6]];
    okp := WtoK(co[1]) ne 0 and [WtoK(co[j+1])/WtoK(co[1]) : j in [1..5]] eq rst;
    return co, okp, steps, Cputime(t0);
end function;

PrintFile(OUT, Sprintf("// f_x Taylor coefficients t^88..t^93 at P32 modulo %o^%o; <prime index, representative, 6 x 17 integers>", p, N) : Overwrite := true);
for ri in [FIRST..Min(LAST, #recs)] do
    rec := recs[ri];
    co, okp, steps, tm := LiftRecord(rec);
    PrintFile(OUT, Sprintf("<%o, %o, %o>,", rec[1], rec[2], [WSeq(c) : c in co]));
    printf "S25|record %o (%o,%o): Newton steps %o; all 67 residuals zero mod p^%o; reduces to the stored r: %o; %o s\n", ri, rec[1], rec[2], steps, N, okp, tm;
    assert okp;
end for;
printf "DONE|25_C_LIFT [%o s]\n", Cputime(started);
quit;
