// D168 step 4, packages 1-3: the cubic cover data on X over Z/p^N.
// Lifts: evaluation points, the odd cubics (hence L(D0), ..., L(4*D0) as
// value matrices), the branch data, and the third, by Newton iteration on
// the cube system of script 13. The effective representative of the third
// is E' = S + S'_1 (S = 79 lifted auxiliary points), not the E_R of script
// 05; the Kummer function is h' = c'*c111/q, with h'/h = (c'/c)*beta1^3.
// Files: state_in.m, cubic_in.m, exact_lists.m, padic_lib.m.
// Env: PREC (N), OUT.
SetQuitOnError(true); SetColumns(0); SetSeed(215);
started := Cputime();
N := StringToInteger(GetEnv("PREC")); OUT := GetEnv("OUT");
NPAIR := 256;
load "state_in.m";
load "cubic_in.m";
load "exact_lists.m";
p := st_p; Fp := GF(p); ZN := Integers(p^N); Z1 := Integers(p);
LIBP := p; LIBF := Fp;
assert #st_modulus eq 3 and st_modulus[3] eq 1;
m0 := st_modulus[1]; m1 := st_modulus[2];
LC0 := -m0; LC1 := -m1;
load "padic_lib.m";
Up<tt> := PolynomialRing(Fp); k4<b> := ext<Fp | Up!st_modulus>;
function DecE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..2]];
    return k4!s;
end function;
PZ<xx> := PolynomialRing(ZN); GG<th> := quo<PZ | xx^2 + m1*xx + m0>;
function Pair(g)
    s := Coefficients(PZ!g); s cat:= [ZN!0 : i in [#s+1..2]];
    return s;
end function;
function LiftK(c)
    s := Eltseq(c);
    return GG!(PZ![ZZ!s[1], ZZ!s[2]]);
end function;
function InvG(g)
    s := Pair(g);
    nr := s[1]^2 + LC1*s[1]*s[2] - LC0*s[2]^2;
    return GG!(PZ![(s[1] + LC1*s[2])*nr^-1, -s[2]*nr^-1]);
end function;
function Q2Z(x)
    x := Rationals()!x;
    return ZN!Numerator(x)*(ZN!Denominator(x))^-1;
end function;
function ToZ1(M)
    return ChangeRing(ChangeRing(M, ZZ), Z1);
end function;
function ToZN(M)
    return ChangeRing(ChangeRing(M, ZZ), ZN);
end function;
rowsZ := Matrix(ZN, [[Q2Z(c) : c in r] : r in rows]);
rowsK := ChangeRing(Red(rowsZ), k4); rowsG := ChangeRing(rowsZ, GG);
Lmat := [ZeroMatrix(ZN, 91, 16) : j in [1..16]];
for t in [1..#pairs] do
    a := pairs[t][1]; c := pairs[t][2];
    for i in [1..91] do
        Lmat[a][i, c] +:= rowsZ[i, t];
        Lmat[c][i, a] +:= rowsZ[i, t];
    end for;
end for;
LmatK := [ChangeRing(Red(L), k4) : L in Lmat]; LmatG := [ChangeRing(L, GG) : L in Lmat];
numG := Matrix(GG, 1, #pairs, [GG!Q2Z(c) : c in rational_numerator]);
denG := Matrix(GG, 1, #pairs, [GG!Q2Z(c) : c in rational_denominator]);
function Mon2(x)
    return [x[pr[1]]*x[pr[2]] : pr in pairs];
end function;
function Mons(x, exps)
    return [&*[x[t]^e[t] : t in [1..16] | e[t] ne 0] : e in exps];
end function;
halfG := GG!((ZN!2)^-1);
// Hensel lift of a point (16 coordinates with x16 = 1, and w) of X.
function LiftPoint(pt)
    x0 := pt[1..16]; assert x0[16] eq 1;
    xc := Matrix(k4, 16, 1, x0);
    Jk := HorizontalJoin([LmatK[j]*xc : j in [1..14]]);
    inds := IndRows(Jk);
    if #inds ne 14 then return false, 0, 0; end if;
    Jinv := Matrix(GG, 14, 14, [LiftK(c) : c in Eltseq(Rows_(Jk, inds)^-1)]);
    Lsel := [Rows_(LmatG[j], inds) : j in [1..14]];
    rsel := Rows_(rowsG, inds);
    x := [LiftK(c) : c in x0];
    two := ScalarMatrix(GG, 14, 2);
    e := 1;
    while e lt N do
        X := Matrix(GG, 16, 1, x);
        J := HorizontalJoin([Lsel[j]*X : j in [1..14]]);
        Jinv := Jinv*(two - J*Jinv);
        d := Jinv*(rsel*Matrix(GG, #pairs, 1, Mon2(x)));
        for j in [1..14] do x[j] -:= d[j, 1]; end for;
        e *:= 2;
    end while;
    mon := Matrix(GG, #pairs, 1, Mon2(x));
    assert IsZero(rowsG*mon);
    target := (numG*mon)[1, 1]*InvG((denG*mon)[1, 1]);
    w := LiftK(pt[17]); e := 1;
    while e lt N do w := (w + target*InvG(w))*halfG; e *:= 2; end while;
    assert w^2 eq target;
    return true, x, w;
end function;

plist := [[DecE(c) : c in x] : x in st_points]; nn := #plist;
orbs := []; used := {Integers()|};
for i in [1..nn] do
    if i in used then continue; end if;
    o := {i, st_frob[i], st_tau[i], st_frob[st_tau[i]]};
    used join:= o;
    if #o eq 4 then Append(~orbs, [i, st_tau[i]]); end if;
end for;
ratpts := [i : i in [1..nn] | st_frob[i] eq i];
printf "S15|N = %o; %o orbits of size 4, %o rational points in the state [%o s]\n", N, #orbs, #ratpts, Cputime(started);
lifted := [* *]; reps := []; oi := 0;
while #reps lt 2*NPAIR do
    oi +:= 1; o := orbs[oi];
    ok1, x1, w1 := LiftPoint(plist[o[1]]);
    if not ok1 then continue; end if;
    ok2, x2, w2 := LiftPoint(plist[o[2]]);
    if not ok2 then continue; end if;
    assert x1 eq x2 and w1 eq -w2;
    Append(~lifted, <x1, w1>); Append(~lifted, <x2, w2>);
    reps cat:= o;
end while;
h := #reps; etau := &cat[[2*j, 2*j-1] : j in [1..NPAIR]];
printf "S15|%o evaluation points lifted (orbits used up to %o) [%o s]\n", h, oi, Cputime(started);
function RealMatrix(cols)   // cols: list of sequences of GG elements (one per point); rows = sections
    A := []; B := [];
    for c in cols do
        prs := [Pair(g) : g in c];
        Append(~A, [s[1] : s in prs]); Append(~B, [s[2] : s in prs]);
    end for;
    return Transpose(Matrix(ZN, A cat B));
end function;

// Odd cubics: cubic forms on C vanishing on E + U, by exact linear conditions.
hc := NPAIR;
cx := [lifted[2*j-1][1] : j in [1..NPAIR]];
M3 := RealMatrix([Mons(x, st_exps3) : x in cx]);
assert Rank(Red(M3)) eq 75;
function FormVals(row)   // quadric in the pairs basis at the points cx
    return RealMatrix([[&+[Q2Z(row[t])*m[t] : t in [1..#pairs] | row[t] ne 0] where m is Mon2(x)] : x in cx])[1];
end function;
function LinVals(row)
    return RealMatrix([[&+[Q2Z(row[t])*x[t] : t in [1..16]]] : x in cx])[1];
end function;
assert B3_linear_rows[1] eq branch_parameter_linear_form;
lamv := [LinVals(r) : r in B3_linear_rows];
verv := [FormVals(veronese_section_rows[i]) : i in [1..3]];
conds := [<lamv[i], lamv[1]> : i in [2..#lamv]] cat [<verv[2], verv[1]>, <verv[3], verv[1]>];
Kodd := IdentityMatrix(ZN, 75);
for cd in conds do
    Aa := ScaleRows(Kodd*M3, cd[1]); Bb := ScaleRows(M3, cd[2]);
    KK := KerN(VerticalJoin(Aa, Bb));
    Kodd := Submatrix(KK, 1, 1, Nrows(KK), Nrows(Kodd))*Kodd;
end for;
printf "S15|odd cubics: dimension %o (expected 36) [%o s]\n", Nrows(Kodd), Cputime(started);
assert Nrows(Kodd) eq 36;
oddF := Matrix(Fp, st_oddrows);
assert RowSpace(Red(Kodd)) eq RowSpace(oddF);
piv := PivCols(oddF);
Kodd := InvN(Cols_(Kodd, piv))*Kodd;
assert Red(Kodd) eq oddF;
oddMN := Transpose(Kodd); oddG := ChangeRing(oddMN, GG);
print "S15|odd cubics reduce to the stored basis mod p";

ellG := [GG!Q2Z(c) : c in branch_parameter_linear_form];
function Vals(x, w, top)
    lv := &+[ellG[j]*x[j] : j in [1..16]];
    odd := Eltseq(Matrix(GG, 1, 75, Mons(x, st_exps3))*oddG);
    wl := w*InvG(lv);
    v1 := Mons(x, st_exps2) cat [wl*c : c in odd];
    v2 := [v1[pr[1]]*v1[pr[2]] : pr in st_pairs2];
    if top eq 2 then return v1, v2, 0, 0; end if;
    v3 := [v1[pr[1]]*v2[pr[2]] : pr in st_pairs3];
    v4 := [v1[pr[1]]*v3[pr[2]] : pr in cub_pairs4];
    return v1, v2, v3, v4;
end function;
c1 := []; c2 := []; c3 := []; c4 := [];
for z in lifted do
    v1, v2, v3, v4 := Vals(z[1], z[2], 4);
    Append(~c1, v1); Append(~c2, v2); Append(~c3, v3); Append(~c4, v4);
end for;
G1 := RealMatrix(c1); G2 := RealMatrix(c2); G3 := RealMatrix(c3); G4 := RealMatrix(c4);
delete c1, c2, c3, c4;
assert Rank(Red(G1)) eq 81 and Rank(Red(G2)) eq 201 and Rank(Red(G3)) eq 321 and Rank(Red(G4)) eq 441;
printf "S15|ranks 81, 201, 321, 441 mod p [%o s]\n", Cputime(started);

// Branch data over Z/p^N.
UA<a> := PolynomialRing(ZN);
fA := UA![Q2Z(c) : c in fiber_nonic_coefficients]; fA := fA*LeadingCoefficient(fA)^-1;
A<aa> := quo<UA | fA>;
function Coefs(v)
    s := Coefficients(UA!v); s cat:= [ZN!0 : i in [#s+1..9]];
    return s;
end function;
s3 := ZN!st_sqrt_minus3; e := 1;
while e lt N do s3 := (s3 - 3*s3^-1)*(ZN!2)^-1; e *:= 2; end while;
assert s3^2 eq ZN!-3;
bpt := [A!UA![Q2Z(c) : c in row] : row in fiber_point_coordinates];
wr := s3*(A!UA![Q2Z(c) : c in branch_branch_ratio]);
ev2b := Mons(bpt, st_exps2);
ev3b := Eltseq(Matrix(A, 1, 75, Mons(bpt, st_exps3))*ChangeRing(oddMN, A));
plus1 := ev2b cat [wr*v : v in ev3b]; minus1 := ev2b cat [-wr*v : v in ev3b];
bp1 := Matrix(ZN, [Coefs(v) : v in plus1]); bm1 := Matrix(ZN, [Coefs(v) : v in minus1]);
assert Red(bp1) eq Matrix(Fp, st_branch_plus) and Red(bm1) eq Matrix(Fp, st_branch_minus);
bp2 := Matrix(ZN, [Coefs(plus1[pr[1]]*plus1[pr[2]]) : pr in st_pairs2]);
printf "S15|branch data lifted; reductions match the state [%o s]\n", Cputime(started);

// q in L(D0 - Dminus), B = Dplus + Q, L(4*D0 - B).
qker := KerN(bm1); assert Nrows(qker) eq 72;
lam := Solution(Red(qker), Vector(Fp, cub_q_coefficients));
qcoef := Vector(ZN, [ZZ!c : c in Eltseq(lam)])*qker;
qv := qcoef*G1;
Sminus := qker*G1;
WQ := QuotN(Sminus, ScaleRows(G2, qv), G2, 90);
Qcoeff := SolN(G2, WQ);
bker := KerN(Qcoeff*bp2); assert Nrows(bker) eq 81;
WB := bker*WQ;
WB4 := ProductN(WB, G2, 321);
printf "S15|L(4*D0 - B): 321 [%o s]\n", Cputime(started);

// Auxiliary points S: 39 Frobenius pairs and one rational point.
Scols := []; si := oi; npair := 0;
while npair lt 39 do
    si +:= 1;
    ok, x, w := LiftPoint(plist[orbs[si][1]]);
    if not ok then continue; end if;
    v1, v2 := Vals(x, w, 2);
    prs := [Pair(g) : g in v2];
    Append(~Scols, [s[1] : s in prs]); Append(~Scols, [s[2] : s in prs]);
    npair +:= 1;
end while;
ri := 0;
repeat
    ri +:= 1;
    ok, x, w := LiftPoint(plist[ratpts[ri]]);
until ok;
v1, v2 := Vals(x, w, 2);
prs := [Pair(g) : g in v2];
assert &and[s[2] eq 0 : s in prs];
Append(~Scols, [s[1] : s in prs]);
VS := Transpose(Matrix(ZN, Scols)); assert Ncols(VS) eq 79;
L2Sc := KerN(VS); assert Nrows(L2Sc) eq 122;
L2S := L2Sc*G2;
L4S := ProductN(L2S, L2S, 283);
L6S := ProductN(L4S, L2S, 444);
printf "S15|L(6*D0 - 3*S): 444 [%o s]\n", Cputime(started);
U1 := QuotN(G2, L6S, G4, 204);
U := MeetN(U1, WB4);
printf "S15|U = L(4*D0 - 3*S - B): dimension %o (expected 84) [%o s]\n", Nrows(U), Cputime(started);
assert Nrows(U) eq 84;

// Solution mod p from the stored model (script 05): beta_i in L(E_R - S).
G2p := ToZ1(G2); G4p := ToZ1(G4);
WRcold := Matrix(Z1, cub_WR_coordinates); WRold := WRcold*G2p;
repeat
    rc := Vector(Z1, [Random(0, p-1) : i in [1..81]])*WRcold;
    rvec := rc*G2p;
until IsUnitVec(rvec);
T0 := QuotN(WRold, ScaleRows(G2p, rvec), G2p, 81);
Tc0 := SolN(G2p, T0);
kb := KerN(Tc0*ToZ1(VS));
printf "S15|L(E_R - S) mod p: dimension %o (expected 2)\n", Nrows(kb);
assert Nrows(kb) eq 2;
bc := kb*Tc0; rinv := InvVec(rvec);
beta := [MulVec((bc*G2p)[i], rinv) : i in [1..2]];
uold := Vector(Z1, cub_u_coefficients)*G4p;
idx := [[1,1,1],[1,1,2],[1,2,2],[2,2,2]];
cs := Matrix([MulVec(MulVec(MulVec(beta[t[1]], beta[t[2]]), beta[t[3]]), uold) : t in idx]);
X0 := SolN(ToZ1(U), cs);
print "S15|the four c_ijk mod p lie in U mod p";
function CubeRes(X)
    c := X*U;
    return Vector(Eltseq(MulVec(c[1], c[3]) - MulVec(c[2], c[2])) cat Eltseq(MulVec(c[2], c[4]) - MulVec(c[3], c[3]))
        cat Eltseq(MulVec(c[1], c[4]) - MulVec(c[2], c[3])));
end function;
function CubeJac(X)
    c := X*U; S := [ScaleRows(U, c[i]) : i in [1..4]]; Z := ZeroMatrix(BaseRing(U), Nrows(U), Ncols(U));
    return VerticalJoin([HorizontalJoin([S[3], Z, S[4]]), HorizontalJoin([-2*S[2], S[4], -S[3]]),
        HorizontalJoin([S[1], -2*S[3], -S[2]]), HorizontalJoin([Z, S[2], S[1]])]);
end function;
X := ToZN(X0);
assert IsZero(Red(Matrix(CubeRes(X))));
J := CubeJac(X); I := IndRows(Red(J));
printf "S15|cube system: %o unknowns, rank %o mod p (expected 332) [%o s]\n", Nrows(J), #I, Cputime(started);
assert #I eq 332;
JI := Rows_(J, I); Jc := PivCols(Red(JI)); Ai := InvN(Cols_(JI, Jc));
delete J, JI;
steps := 0;
for it in [1..N+3] do
    F := CubeRes(X);
    if IsZero(F) then break; end if;
    d := -Vector(ZN, [F[j] : j in Jc])*Ai;
    xf := Eltseq(X);
    for t in [1..#I] do xf[I[t]] +:= d[t]; end for;
    X := Matrix(ZN, 4, 84, xf); steps +:= 1;
end for;
assert IsZero(CubeRes(X));
printf "S15|cube system solved mod p^%o in %o steps (all %o equations vanish) [%o s]\n", N, steps, 3*Ncols(U), Cputime(started);

// E' = S + S'_1: L(2*D0 - E'), u' = c111, norm function, norm scalar.
cc := X*U; c111 := cc[1]; c112 := cc[2];
KK := KerN(VerticalJoin(ScaleRows(L2S, c112), ScaleRows(G2, c111)));
printf "S15|L(2*D0 - E'): dimension %o (expected 81)\n", Nrows(KK);
assert Nrows(KK) eq 81;
WRc := Submatrix(KK, 1, 1, 81, 122)*L2Sc; WR := WRc*G2;
// same class as the stored E_R mod p
WRp := ToZ1(WR);
eqs := Transpose(KerN(Transpose(BasisN(ScaleRows(WRold, WRp[1])))));
cur := G2p; same := true;
for trial in [1..16] do
    ker := KerN(ScaleRows(cur, RandSec(WRp))*eqs);
    if Nrows(ker) eq 0 then same := false; break; end if;
    cur := ker*cur;
    if Nrows(cur) eq 1 then break; end if;
end for;
same and:= Nrows(cur) eq 1 and IsZero(ScaleRows(WRp, cur[1])*eqs);
printf "S15|E' is linearly equivalent to the stored E_R mod p: %o [%o s]\n", same, Cputime(started);
assert same;
ucoef := (Matrix(X[1])*SolN(G4, U))[1];
assert ucoef*G4 eq c111;
normSpace := ProductN(WR, DeckN(WR, etau), 201);
fm := QuotN(G2, normSpace, G2, 1);
fcoef := SolN(G2, fm)[1];
j0 := Min([j : j in [1..201] | (ZZ!fcoef[j]) mod p ne 0]); fcoef *:= fcoef[j0]^-1;
fv := fcoef*G2;
assert DeckN(Matrix(fv), etau)[1] eq fv;
ut := DeckN(Matrix(c111), etau)[1]; qt := DeckN(Matrix(qv), etau)[1];
lhs := MulVec(c111, ut); rhs := MulVec(MulVec(MulVec(fv, fv), fv), MulVec(qv, qt));
j0 := Min([j : j in [1..h] | (ZZ!rhs[j]) mod p ne 0 or (ZZ!rhs[h+j]) mod p ne 0]);
rat := MulVec(Vector(ZN, [lhs[j0], lhs[h+j0]]), InvVec(Vector(ZN, [rhs[j0], rhs[h+j0]])));
assert rat[2] eq 0;
cN := rat[1];
assert lhs eq cN*rhs;
ratio := (Fp!(ZZ!cN))/(Fp!cub_norm_scalar);
printf "S15|norm identity u*tau(u) = c*f^3*q*tau(q) holds at all points; c'/c is a cube mod p: %o [%o s]\n", IsPower(ratio, 3), Cputime(started);

function IntSeq(v) return [ZZ!c : c in Eltseq(v)]; end function;
function IntMat(M) return [IntSeq(r) : r in Rows(M)]; end function;
PrintFile(OUT, Sprintf("lx_p := %o;\nlx_N := %o;\nlx_c := %o;", p, N, ZZ!cN) : Overwrite := true);
PrintFile(OUT, Sprintf("lx_odd := %o;", IntMat(Kodd)));
PrintFile(OUT, Sprintf("lx_q := %o;\nlx_u := %o;\nlx_f := %o;", IntSeq(qcoef), IntSeq(ucoef), IntSeq(fcoef)));
PrintFile(OUT, Sprintf("lx_WR := %o;", IntMat(WRc)));
PrintFile(OUT, Sprintf("lx_beta1_num := %o;\nlx_beta1_den := %o;", IntSeq(bc[1]), IntSeq(rc)));
printf "S15|written %o [%o s]\n", OUT, Cputime(started);
print "DONE|15_LIFT_X";
quit;
