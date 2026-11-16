// D168 step 4, package 5: lift points of V_b to precision p^N and evaluate f_x.
// For a record of vb_<k>.txt (g_ij mod p in the G44 basis):
//  1. s_A, s_B in S_x vanish at two points of the first, second complete fibre;
//     g = s_A^2/phi', g' = s_B^2/phi', h = s_A*s_B/phi' (phi' = phi*Q^2) in G44.
//     Newton on g*g' = h^2 over W = W_N(F_p^17): 199 unknowns, 2 pinned.
//  2. A third section s_C: (gamma, gamma') = (s_A*s_C, s_B*s_C)/phi' solves the
//     linear system gamma*h = g*gamma' (kernel of rank 3, 3 coordinates pinned).
//  3. Trace forms b(s,s') in L_C(44*P32) from the complete fibres, their Laurent
//     coefficients at P32; the radical of the leading coefficient gives s_x and
//     f_x = b(s_x,s_x). Output: Laurent coefficients t^-43..t^-38 of f_x (global
//     functionals, up to one scalar per point; the coefficient of t^-44 is zero).
// All linear solves use an inverse at precision p^M0 (M0 = min(N,16)) and
// iterative refinement; all residuals are checked at every evaluation point.
// Files: ly_in.m (script 16), padic_lib.m, witt_lib.m. Env: PREC, VB, FIRST,
// LAST, OUT.
SetQuitOnError(true); SetColumns(0); SetSeed(317);
started := Cputime();
N := StringToInteger(GetEnv("PREC")); OUT := GetEnv("OUT"); VB := GetEnv("VB");
FIRST := StringToInteger(GetEnv("FIRST")); LAST := StringToInteger(GetEnv("LAST"));
load "ly_in.m";
p := ly_p; assert ly_N eq N; Fp := GF(p); ZN := Integers(p^N);
LIBP := p; LIBF := Fp; LC0 := 0; LC1 := 0;
load "padic_lib.m";
K := GF(p, 17);
load "witt_lib.m";
M0 := Min(N, 16); ZM := Integers(p^M0);
function ToR(M, R) return ChangeRing(ChangeRing(M, ZZ), R); end function;
G44N := Matrix(ZN, ly_G44); NG := Ncols(G44N); fibs := ly_fibs; NF := #fibs;
LfibN := Matrix(ZN, ly_Lfib); LaurN := Matrix(ZN, ly_Laur);
LaurHdrK := ChangeRing(Matrix(Fp, ly_LaurHdr), K);
pa := [fibs[1][2], fibs[1][3]]; pb := [fibs[2][2], fibs[2][3]];
GAc := KerN(Cols_(G44N, pa)); GBc := KerN(Cols_(G44N, pb)); GCc := KerN(Cols_(G44N, pa cat pb));
nA := Nrows(GAc); nB := Nrows(GBc); nC := Nrows(GCc); NU := nA + nB + nC;
assert [nA, nB, nC] eq [67, 67, 65];
function Data(R)
    G := ToR(G44N, R);
    return <ToR(GAc, R)*G, ToR(GBc, R)*G, ToR(GCc, R)*G, G>;
end function;
DN := Data(ZN); DM := Data(ZM);
G44K := ChangeRing(Red(G44N), K);
GAcK := ChangeRing(Red(GAc), K); GBcK := ChangeRing(Red(GBc), K); GCcK := ChangeRing(Red(GCc), K);
GAK := GAcK*G44K; GBK := GBcK*G44K; GCK := GCcK*G44K;
// fibres used for traces: all but the first (g vanishes there)
fcols := &cat[fibs[m] : m in [2..NF]]; NFU := NF - 1;
TRM := ZeroMatrix(ZN, 3*NFU, NFU);
for m in [1..NFU] do for j in [1..3] do TRM[3*(m-1)+j, m] := 1; end for; end for;
Lf := Cols_(LfibN, [2..NF]);
Jc3 := PivCols(Red(Lf)); assert #Jc3 eq 29;
Linv := InvN(Cols_(Lf, Jc3));
idx := [[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]];
function DecKE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..17]];
    return K!s;
end function;
function DiagK(v) return DiagonalMatrix(K, Eltseq(v)); end function;
// values (g, g', h) of the unknown x (1 x 199 over W) at all points
function XVals(x, D)
    g := [Submatrix(x[i], 1, 1, 1, nA)*D[1] : i in [1..WD]];
    gp := [Submatrix(x[i], 1, nA+1, 1, nB)*D[2] : i in [1..WD]];
    h := [Submatrix(x[i], 1, nA+nB+1, 1, nC)*D[3] : i in [1..WD]];
    return g, gp, h;
end function;
function XRes(x, D)
    g, gp, h := XVals(x, D);
    return WSub(WHad(g, gp), WHad(h, h));
end function;
function XJac(x, D, I, Jc)     // Jacobian rows I, columns Jc
    g, gp, h := XVals(x, D);
    A1 := Cols_(D[1], Jc); A2 := Cols_(D[2], Jc); A3 := Cols_(D[3], Jc);
    return [Rows_(VerticalJoin(ScaleP(A1, Cols_(gp[i], Jc)[1]), VerticalJoin(ScaleP(A2, Cols_(g[i], Jc)[1]), -2*ScaleP(A3, Cols_(h[i], Jc)[1]))), I) : i in [1..WD]];
end function;
procedure Update(~x, I, d)
    for i in [1..WD] do
        for t in [1..#I] do x[i][1, I[t]] -:= d[i][1, t]; end for;
    end for;
end procedure;

function LiftRecord(rec)
    t0 := Cputime();
    gco := [Vector(K, [DecKE(c) : c in v]) : v in rec[3]];
    gv := [v*G44K : v in gco];
    function GP(col)
        M := ZeroMatrix(K, 3, 3);
        for n in [1..6] do M[idx[n][1], idx[n][2]] := gv[n][col]; M[idx[n][2], idx[n][1]] := gv[n][col]; end for;
        return M;
    end function;
    ka := Basis(Nullspace(HorizontalJoin(GP(pa[1]), GP(pa[2]))));
    kb := Basis(Nullspace(HorizontalJoin(GP(pb[1]), GP(pb[2]))));
    assert #ka eq 1 and #kb eq 1;
    a := ka[1]; b := kb[1];
    k3 := Min([j : j in [1..3] | Rank(Matrix([a, b, Vector(K, [i eq j select 1 else 0 : i in [1..3]])])) eq 3]);
    c := Vector(K, [i eq k3 select 1 else 0 : i in [1..3]]);
    function Comb(u, v)
        return &+[(idx[n][1] eq idx[n][2] select u[idx[n][1]]*v[idx[n][1]] else u[idx[n][1]]*v[idx[n][2]] + u[idx[n][2]]*v[idx[n][1]])*gco[n] : n in [1..6]];
    end function;
    g0 := Comb(a, a); gp0 := Comb(b, b); h0 := Comb(a, b); ga0 := Comb(a, c); gb0 := Comb(b, c);
    x0 := Vector(K, Eltseq(Solution(GAcK, g0)) cat Eltseq(Solution(GBcK, gp0)) cat Eltseq(Solution(GCcK, h0)));
    gK := g0*G44K; gpK := gp0*G44K; hK := h0*G44K;
    assert &and[gK[r]*gpK[r] eq hK[r]^2 : r in [1..NG]];
    JK := VerticalJoin(GAK*DiagK(gpK), VerticalJoin(GBK*DiagK(gK), -2*GCK*DiagK(hK)));
    I := IndRows(JK); assert #I eq NU - 2;
    JKI := Rows_(JK, I); Jc := PivCols(JKI);
    // phase A: precision p^M0, quadratic
    x := WFromField(Matrix(x0), ZM);
    Xinv := WFromField(Cols_(JKI, Jc)^-1, ZM);
    e := 1;
    while e lt M0 do
        Xinv := WInvStep(XJac(x, DM, I, Jc), Xinv);
        Update(~x, I, WMul(WCols(XRes(x, DM), Jc), Xinv));
        e *:= 2;
    end while;
    Xinv := WInvStep(XJac(x, DM, I, Jc), Xinv);
    assert WIsZero(XRes(x, DM));
    // phase B: precision p^N, M0 digits per step
    x := WRing(x, ZN); XinvN := WPre(WRing(Xinv, ZN)); steps := 0;
    for it in [1..(N div M0) + 3] do
        F := XRes(x, DN);
        if WIsZero(F) then break; end if;
        Update(~x, I, WMulPre(WCols(F, Jc), XinvN)); steps +:= 1;
    end for;
    assert WIsZero(XRes(x, DN));
    t1 := Cputime();
    g, gp, h := XVals(x, DN);
    // the third section: (gamma, gamma') with gamma*h = g*gamma'
    AK := VerticalJoin(G44K*DiagK(hK), -G44K*DiagK(gK));
    y0 := Vector(K, Eltseq(ga0) cat Eltseq(gb0));
    assert IsZero(y0*AK);
    I2 := IndRows(AK); assert #I2 eq 135;
    AKI := Rows_(AK, I2); Jc2 := PivCols(AKI);
    function YRes(y, D, gg, hh)
        ga := [Submatrix(y[i], 1, 1, 1, 69)*D[4] : i in [1..WD]];
        gb := [Submatrix(y[i], 1, 70, 1, 69)*D[4] : i in [1..WD]];
        return WSub(WHad(ga, hh), WHad(gg, gb)), ga, gb;
    end function;
    gM := WRing(g, ZM); hM := WRing(h, ZM);
    G4s := Cols_(DM[4], Jc2);
    A2 := [Rows_(VerticalJoin(ScaleP(G4s, Cols_(hM[i], Jc2)[1]), -ScaleP(G4s, Cols_(gM[i], Jc2)[1])), I2) : i in [1..WD]];
    X2 := WFromField(Cols_(AKI, Jc2)^-1, ZM);
    e := 1;
    while e lt 2*M0 do X2 := WInvStep(A2, X2); e *:= 2; end while;
    X2N := WPre(WRing(X2, ZN));
    y := WFromField(Matrix(y0), ZN);
    for it in [1..(N div M0) + 3] do
        r := YRes(y, DN, g, h);
        if WIsZero(r) then break; end if;
        Update(~y, I2, WMulPre(WCols(r, Jc2), X2N));
    end for;
    r, ga, gb := YRes(y, DN, g, h);
    assert WIsZero(r);
    t2 := Cputime();
    // products s*s'/phi' for s, s' in (s_A, s_B, s_C), at the fibre points
    gF := WCols(g, fcols); gaF := WCols(ga, fcols);
    assert &and[cc ne 0 : cc in Eltseq(WToField(gF))];
    prods := [gF, WCols(h, fcols), gaF, WCols(gp, fcols), WCols(gb, fcols), WHad(WHad(gaF, gaF), WInvVec(gF))];
    Ls := [];
    for P in prods do
        tr := WRightZ(P, TRM);
        co := WRightZ(WCols(tr, Jc3), Linv);
        assert WIsZero(WSub(WRightZ(co, Lf), tr));
        Append(~Ls, WRightZ(co, LaurN));
    end for;
    lead := [[Cols_(L[i], [1]) : i in [1..WD]] : L in Ls];        // 1 x 1 over W
    MK := ZeroMatrix(K, 3, 3);
    for n in [1..6] do
        MK[idx[n][1], idx[n][2]] := WToField(lead[n])[1, 1]; MK[idx[n][2], idx[n][1]] := MK[idx[n][1], idx[n][2]];
    end for;
    assert Rank(MK) eq 2;
    function Ld(i, j) return lead[Index(idx, i le j select [i, j] else [j, i])]; end function;
    rr := [u : u in [[1,2],[1,3],[2,3]] | Rank(Matrix([MK[u[1]], MK[u[2]]])) eq 2][1];
    r1 := rr[1]; r2 := rr[2];
    cv := [WSub(WMul(Ld(r1, 2), Ld(r2, 3)), WMul(Ld(r1, 3), Ld(r2, 2))),
           WSub(WMul(Ld(r1, 3), Ld(r2, 1)), WMul(Ld(r1, 1), Ld(r2, 3))),
           WSub(WMul(Ld(r1, 1), Ld(r2, 2)), WMul(Ld(r1, 2), Ld(r2, 1)))];
    for i in [1..3] do
        assert WIsZero(WAdd(WAdd(WMul(Ld(i, 1), cv[1]), WMul(Ld(i, 2), cv[2])), WMul(Ld(i, 3), cv[3])));
    end for;
    fL := [ZeroMatrix(ZN, 1, Ncols(LaurN)) : i in [1..WD]];
    for n in [1..6] do
        coef := WMul(cv[idx[n][1]], cv[idx[n][2]]);
        if idx[n][1] ne idx[n][2] then coef := WScal(2, coef); end if;
        fL := WAdd(fL, WMul(coef, Ls[n]));
    end for;
    // mod p: the stored f_x (coordinates in the header basis of L_C(44*P32))
    fst := Vector(K, [DecKE(cc) : cc in rec[4]])*LaurHdrK;
    okp := Rank(VerticalJoin(Matrix(fst), WToField(fL))) eq 1;
    return fL, okp, steps, [t1 - t0, t2 - t1, Cputime() - t2];
end function;

body := Read(VB);
i0 := Position(body, "<"); j0 := #body;
while body[j0] ne ">" do j0 -:= 1; end while;
recs := eval ("[* " cat body[i0..j0] cat " *]");
printf "S17|N = %o, M0 = %o; %o records in %o; records %o..%o [%o s]\n", N, M0, #recs, VB, FIRST, LAST, Cputime(started);
NCOEF := 6;
PrintFile(OUT, Sprintf("// f_x Laurent coefficients t^-43..t^-%o at P32 modulo %o^%o; <mask1, mask2, %o x 17 integers>", 44 - NCOEF, p, N, NCOEF) : Overwrite := true);
for ri in [FIRST..Min(LAST, #recs)] do
    rec := recs[ri];
    fL, okp, steps, tm := LiftRecord(rec);
    fK := WToField(fL);
    supp := [j : j in [1..Ncols(fK)] | fK[1, j] ne 0];
    assert &and[fL[i][1, 1] eq 0 : i in [1..WD]];      // the coefficient of t^-44 vanishes exactly
    PrintFile(OUT, Sprintf("<%o, %o, %o>,", rec[1], rec[2], [[ZZ!fL[i][1, j] : i in [1..WD]] : j in [2..NCOEF+1]]));
    printf "S17|record %o (%o,%o): Newton steps %o; all residuals zero mod p^%o; reduces to the stored f_x: %o; first nonzero Laurent index mod p: %o; times %o\n", ri, rec[1], rec[2], steps, N, okp, supp[1], tm;
    assert okp;
end for;
printf "DONE|17_LIFT_POINTS [%o s]\n", Cputime(started);
quit;
