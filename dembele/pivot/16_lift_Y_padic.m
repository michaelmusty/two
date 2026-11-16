// D168 step 4, package 4: the model of Y over C and G44 over Z/p^N.
// Input: the X-level lift of script 15 (file LX). The points of Y of the
// mod-p model (ymodel_in.m) are lifted; the Kummer coordinate changes from v
// (v^3 = h) to v' = lambda*beta1*v (v'^3 = h' = c'*c111/q). Sections of
// pi^*(2H - G): s0 + s1*v' + tau(s1)*a'/v', s1 in L_X(E' - Dminus - pi^*G), written
// s1 = t/r with r in L(2*D0 - E') and t in L(2*D0 - R'' - Dminus - pi^*G).
// Checks: the lifted L(D0_Y) and G44 reduce to the stored spaces mod p (the
// bases are then chosen to reduce to the stored bases).
// Output: G44 at the good points, complete fibres, L_C(44*P32) at the fibre
// base points and its Laurent coefficients at P32 (global functionals).
// Files: hdr12.m and its inputs, cubic_in.m, exact_lists.m, padic_*.m.
// (lx_in.m = output of script 15 at the same precision). Env: PREC, OUT.
load "hdr12.m";
chk := &+[Integers()!c : c in Eltseq(G44)] mod 10^12;
printf "S16|G44 basis checksum mod p: %o\n", chk;
assert chk eq 15772820;
N := StringToInteger(GetEnv("PREC")); OUT := GetEnv("OUT");
load "cubic_in.m";
load "exact_lists.m";
load "lx_in.m";
assert lx_N eq N;
load "padic_points.m";
oddMN := Transpose(Matrix(ZN, lx_odd));
load "padic_vals.m";
printf "S16|N = %o; X-level data loaded [%o s]\n", N, Cputime(started);
function ColG(v) return Matrix(GG, #v, 1, [GG!(ZN!c) : c in v]); end function;
function DotG(vals, col) return (Matrix(GG, 1, #vals, vals)*col)[1, 1]; end function;
function RedG(g)
    s := Pair(g);
    return k4![Fp!(ZZ!s[1]), Fp!(ZZ!s[2])];
end function;
qG := ColG(lx_q); uG := ColG(lx_u); fG := ColG(lx_f);
b1n := ColG(lx_beta1_num); b1d := ColG(lx_beta1_den); foldG := ColG(cub_f_coefficients);
cN := ZN!lx_c; cold := Fp!cub_norm_scalar;
lamcands := [r[1] : r in Roots(PolynomialRing(Fp)![-(Fp!lx_c)/cold, 0, 0, 1])];
assert #lamcands eq 3;

// Sections vanishing on G, and s1-space.
gpts := [];
for z in ym_G_points do
    ok, x, w := LiftPoint([k4!(Fp!c) : c in z]); assert ok;
    Append(~gpts, <x, w>);
end for;
E0N := RatMatrix([Mons(z[1], st_exps2) : z in gpts]);          // 45 x 17
KS := KerN(E0N); assert Nrows(KS) eq 28;
S0p := Matrix(Fp, ym_S0_coefficients);
S0N := ToZN(Solution(Red(KS), S0p))*KS;
assert Red(S0N) eq S0p;
gcols := [];
for z in gpts do
    for sg in [1, -1] do
        v1, v2 := Vals(z[1], sg*z[2], 2);
        Append(~gcols, v2);
    end for;
end for;
VG := RatMatrix(gcols);                                          // 201 x 34
rG := ColG(lx_r);
assert &and[RedG(DotG(v2, rG)) ne 0 : v2 in gcols];
Tc0 := Matrix(ZN, lx_T0);
KT := KerN(Tc0*HorizontalJoin(bm2, VG));
printf "S16|numerators of the s1-space, L(2*D0 - R'' - Dminus - pi^*G): dimension %o (expected 38)\n", Nrows(KT);
assert Nrows(KT) eq 38;
TcN := KT*Tc0; TcG := ChangeRing(TcN, GG); S0G := ChangeRing(S0N, GG);

// Points of Y.
NYp := #ym_points; assert NYp eq NY;
lam := Fp!0; cols := []; nbad := 0;
for i in [1..NY] do
    z := [DecE(c) : c in ym_points[i]];
    ok, x, w := LiftPoint(z[1..17]); assert ok;
    v1, v2, v3, v4 := Vals(x, w, 4);
    v1t, v2t := Vals(x, -w, 2);
    qv := DotG(v1, qG); uv := DotG(v4, uG);
    av := GG!cN*DotG(v2, fG);
    hv := GG!cN*uv*InvG(qv);
    bden := RedG(DotG(v2, b1d)); bdent := RedG(DotG(v2t, b1d));
    assert bden ne 0 and bdent ne 0;
    beta := RedG(DotG(v2, b1n))/bden; betat := RedG(DotG(v2t, b1n))/bdent;
    aold := cold*RedG(DotG(v2, foldG));
    lam2 := RedG(av)/(beta*betat*aold);
    if lam eq 0 then
        cand := [l : l in lamcands | k4!(l^2) eq lam2]; assert #cand eq 1;
        lam := cand[1];
    end if;
    assert k4!(lam^2) eq lam2;
    vk := lam*beta*z[18];
    assert vk^3 eq RedG(hv);
    v := LiftK(vk); e := 1; third := GG!((ZN!3)^-1);
    while e lt N do v := v - (v^3 - hv)*InvG(v^2)*third; e *:= 2; end while;
    assert v^3 eq hv;
    s0 := Eltseq(S0G*Matrix(GG, 45, 1, v1[1..45]));
    rx := DotG(v2, rG); rt := DotG(v2t, rG);
    assert RedG(rx) ne 0 and RedG(rt) ne 0;
    s1 := Eltseq(TcG*Matrix(GG, 201, 1, v2)*(v*InvG(rx)) + TcG*Matrix(GG, 201, 1, v2t)*(av*InvG(v*rt)));
    Append(~cols, s0 cat s1);
end for;
W1new := RatMatrix(cols);
printf "S16|%o points of Y lifted; lambda = %o [%o s]\n", NY, lam, Cputime(started);
W1p := Matrix(Fp, ym_W1);
same := RowSpace(Red(W1new)) eq RowSpace(W1p);
printf "S16|L(D0_Y) of the lifted model reduces to the stored space: %o\n", same;
assert same;
Mb := Solution(Red(W1new), W1p);
assert Submatrix(Mb, 1, 1, 28, 28) eq IdentityMatrix(Fp, 28) and IsZero(Submatrix(Mb, 1, 29, 28, 38));
W1N := ToZN(Mb)*W1new;
assert Red(W1N) eq W1p;
W2N := Matrix(ZN, [[W1N[pr[1], r]*W1N[pr[2], r] : r in [1..NY]] : pr in ym_pairs2]);
assert Rank(Red(W2N)) eq 195;

// Expansion of C at P32 over Z/p^N (same choices as LocalCoordinates mod p).
PREC_T := 70;
ptq := [Q2Z(c) : c in P32_coordinates];
anchor := Min([i : i in [1..16] | (ZZ!ptq[i]) mod p ne 0]);
ptq := [c*ptq[anchor]^-1 : c in ptq];
vars := [i : i in [1..16] | i ne anchor];
ptc := Matrix(ZN, 16, 1, ptq);
Jq := HorizontalJoin([Lmat[j]*ptc : j in vars]);                 // 91 x 15
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
for n in [1..PREC_T-1] do
    for j in [1..16] do Append(~xsc[j], ZN!((n eq 1 and j eq param) select 1 else 0)); end for;
    conv := Matrix(ZN, #pairs, 1, [&+[xsc[pr[1]][m+1]*xsc[pr[2]][n-m+1] : m in [0..n]] : pr in pairs]);
    corr := -Minv*(rsel*conv);
    for j in [1..14] do xsc[depsP[j]][n+1] := corr[j, 1]; end for;
end for;
xpol := [PZ!s : s in xsc];
function Trunc(f) return PZ![Coefficient(f, j) : j in [0..PREC_T-1]]; end function;
assert &and[IsZero(Trunc(&+[rowsZ[i, t]*xpol[pairs[t][1]]*xpol[pairs[t][2]] : t in [1..#pairs]])) : i in [1..91]];
assert &and[Fp!(ZZ!xsc[j][n+1]) eq Coefficient(xser[j], n) : n in [0..NP+1], j in [1..16]];
mserN := [Trunc(&*[xpol[t]^e[t] : t in [1..16] | e[t] ne 0]) : e in st_exps2];
condN := Matrix(ZN, [[Coefficient(m, j) : j in [0..NP-1]] : m in mserN]);
assert Red(condN) eq cond;
printf "S16|expansion at P32 to t^%o; reduces to the mod-p jets [%o s]\n", PREC_T, Cputime(started);

// Quadrics through G + 22*P32, Q, and G44.
KA := KerN(S0N*condN); assert Nrows(KA) eq 6;
ANc0 := KA*S0N;
ANcN := ToZN(Solution(Red(ANc0), ANc))*ANc0; assert Red(ANcN) eq ANc;
QcN := (ToZN(Matrix(Solution(ANc, Qc)))*ANcN)[1];
assert Red(Matrix(QcN)) eq Matrix(Qc);
QsN := SolN(S0N, Matrix(QcN))[1]; ANsN := SolN(S0N, ANcN);
TprN := RowSubmatrix(W1N, 1, 28);
ANYN := ANsN*TprN; QYN := QsN*TprN;
Q2YN := Vector(ZN, [QYN[r]^2 : r in [1..NY]]);
assert good eq [r : r in [1..NY] | (ZZ!Q2YN[r]) mod p ne 0];
function RandProducts(A, count)
    rws := [];
    for n in [1..count] do
        ra := RandSec(A); rb := RandSec(A);
        Append(~rws, [ra[r]*rb[r] : r in [1..Ncols(A)]]);
    end for;
    return Matrix(BaseRing(A), rws);
end function;
AAN := RandProducts(ANYN, 12);
G44n := QuotP(AAN, ScaleP(W2N, Q2YN), W2N, 69);
Bg := Matrix(ZN, [[G44n[i, r]*Q2YN[r]^-1 : r in good] : i in [1..69]]);
okg, Mg := IsConsistent(Red(Bg), G44);
printf "S16|G44 of the lifted model reduces to the stored G44: %o [%o s]\n", okg, Cputime(started);
assert okg;
G44N := ToZN(Mg)*Bg;
assert Red(G44N) eq G44;

// L_C(44*P32) over Z/p^N, values at the fibre base points, Laurent coefficients.
ccols := [];
for x in cpts do
    ok, xl := LiftC([k4!c : c in x]); assert ok;
    Append(~ccols, Mons(xl, st_exps2));
end for;
E2N := RatMatrix(ccols); assert Red(E2N) eq E2;
E4N := Matrix(ZN, [[E2N[pr[1], r]*E2N[pr[2], r] : r in [1..NC]] : pr in pairs4]);
APvN := KerN(condN)*E2N; assert Nrows(APvN) eq 23;
ANN_N := RandProducts(APvN, 12);
QvN := QcN*E2N; Q2vN := Vector(ZN, [QvN[r]^2 : r in [1..NC]]);
LFvN := QuotP(ANN_N, ScaleP(E4N, Q2vN), E4N, 2*NP + 1 - 16);
LFcN := SolN(E4N, LFvN);
m4rows := [];
for pr in pairs4 do
    f4 := mserN[pr[1]]*mserN[pr[2]];
    Append(~m4rows, [Coefficient(f4, j) : j in [0..2*NP]]);
end for;
M4 := Matrix(ZN, m4rows);
FL := LFcN*M4;                                                   // 29 x 45, numerators
Qser := &+[QcN[i]*mserN[i] : i in [1..45]];
assert &and[Coefficient(Qser, j) eq 0 : j in [0..NP-1]];
Usq := [Coefficient(Qser^2, 2*NP + j) : j in [0..2*NP]];
Uinv := [Usq[1]^-1];
for n in [1..2*NP] do Append(~Uinv, -Uinv[1]*&+[Usq[m+1]*Uinv[n-m+1] : m in [1..n]]); end for;
LaurN := Matrix(ZN, [[&+[FL[i, m+1]*Uinv[n-m+1] : m in [0..n]] : n in [0..2*NP]] : i in [1..29]]);
printf "S16|L_C(44*P32): 29; rank of the Laurent coefficients t^-44..t^0 mod p: %o [%o s]\n", Rank(Red(LaurN)), Cputime(started);
assert Rank(Red(LaurN)) eq 29;
LfibN := Matrix(ZN, [[LFvN[i, c]*Q2vN[c]^-1 : c in fibc] : i in [1..29]]);
LaurHdr := Solution(Red(LFvN), LFv)*Red(LaurN);                  // Laurent coefficients of the header basis, mod p
assert Rank(Red(LfibN)) eq 29;

function IntSeq(v) return [ZZ!c : c in Eltseq(v)]; end function;
function IntMat(M) return [IntSeq(r) : r in Rows(M)]; end function;
PrintFile(OUT, Sprintf("ly_p := %o;\nly_N := %o;\nly_good := %o;", p, N, good) : Overwrite := true);
PrintFile(OUT, Sprintf("ly_fibs := %o;", [[Index(good, f[j]) : j in [1..3]] : f in fibs]));
PrintFile(OUT, Sprintf("ly_G44 := %o;", IntMat(G44N)));
PrintFile(OUT, Sprintf("ly_Lfib := %o;\nly_Laur := %o;", IntMat(LfibN), IntMat(LaurN)));
PrintFile(OUT, Sprintf("ly_LaurHdr := %o;", IntMat(LaurHdr)));
printf "S16|written %o [%o s]\n", OUT, Cputime(started);
print "DONE|16_LIFT_Y";
quit;
