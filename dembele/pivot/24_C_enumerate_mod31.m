// D174, package 3: the 15 Frobenius-orbit representatives of N = F_256*y (y from
// script 22, N = ker g(Frob) in J(C)[2]) and the evaluation data of each:
// representatives c^j(Frob)*y, j = 0..14, c a generator of (F_2[x]/g)^*.
// The construction of the map is that of script 23 (header below).
// Input: W_D = H^0(2*D0 - D) (script 22; x = [D - D0], D0 = 2K) as coefficients
// in the quartic basis. B_j = quartics vanishing to order >= j at P32.
//  S_x = H^0(x + N), N = 2K - 43*P32 (degree 17, dimension 2):
//        S_x*w = {v in B_43 : v*W_D in w*B_43}, w = W_D[1], zeros D + D'.
//  q in H^0(2*D0 - 2*D') (dimension 1 because 2x = 0); g_ij = v_i*v_j/q are
//  quartics in B_86 with g_11*g_22 = g_12^2.
//  s_x = the section of S_x vanishing to order 44 at P32; f_x = s_x^2 in B_88;
//  r(x) = c_89/c_88 (Taylor coefficients at P32 in the parameter t).
// Checks: independence of w; f(Frob x) = Frob f(x).
// Output for the lift: (g, h, g') = (s_x^2, s_x*s_B, s_B^2) in the quartic basis.
// Env: IN (file of script 22), OUT, SEED, PIDX, NORB (optional).
SetQuitOnError(true); SetColumns(0);
SetSeed(StringToInteger(GetEnv("SEED"))); OUT := GetEnv("OUT");
NORB := GetEnv("NORB") eq "" select 22 else StringToInteger(GetEnv("NORB"));
started := Cputime();
p := 31; Fp := GF(p); AEXT := 17; K := GF(p, AEXT); ZZ := Integers();
k := Fp;
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
c16_in := Read(GetEnv("IN")); c16_stmts := Split(c16_in, ";");
c16_p := eval Split(c16_stmts[1], "=")[2]; c16_quad := eval Split(c16_stmts[2], "=")[2];
c16_pairs4 := eval Split(c16_stmts[3], "=")[2]; c16_modulus := eval Split(c16_stmts[4], "=")[2];
c16_point := eval Split(c16_stmts[5], "=")[2];
assert c16_p eq p and [ZZ!c : c in Coefficients(DefiningPolynomial(K))] eq c16_modulus;
quad := c16_quad; pairs4 := c16_pairs4;
function DecKE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..AEXT]];
    return K!s;
end function;
// --- points of C over K ---
RK := ChangeRing(R, K); PK := ProjectiveSpace(RK);
polysK := [RK!f : f in polys];
function SlicePoints()
    a0 := Random(K);
    S := Scheme(PK, polysK cat [RK.15 - a0*RK.16]);
    return [[c/x[16] : c in Eltseq(x)] : x in Points(S) | x[16] ne 0];
end function;
orbs := []; extra := []; seenx := {};
while #orbs lt NORB or #extra lt 0 do
    for pt in SlicePoints() do
        if pt in seenx or pt[15] in Fp then continue; end if;
        Include(~seenx, pt);
        if #orbs lt NORB then Append(~orbs, pt); elif #extra lt 0 then Append(~extra, pt); end if;
    end for;
end while;
evpts := &cat[[[c^(p^i) : c in pt] : i in [0..AEXT-1]] : pt in orbs];
NE := #evpts;
efrob := [((j - 1) mod AEXT) eq 0 select j + AEXT - 1 else j - 1 : j in [1..NE]];
etau := [1..NE]; q := p;
printf "S22|evaluation points: %o orbits, %o points; %o further K-points [%o s]\n", NORB, NE, #extra, Cputime(started);

function Q2(x) return [x[pr[1]]*x[pr[2]] : pr in quad]; end function;
function Q4(x) v := Q2(x); return [v[pr[1]]*v[pr[2]] : pr in pairs4]; end function;
V2 := Transpose(Matrix(K, [Q4(x) : x in evpts]));
assert Rank(V2) eq 105;
V1 := Transpose(Matrix(K, [Q2(x) : x in evpts]));
V3 := ZeroMatrix(K, 0, NE);
for trial in [1..12] do
    rws := [];
    for n in [1..60] do
        i := Random(1, 45); j := Random(1, 105);
        Append(~rws, [V1[i, r]*V2[j, r] : r in [1..NE]]);
    end for;
    V3 := Matrix(Basis(RowSpace(VerticalJoin(V3, Matrix(K, rws)))));
    if Nrows(V3) eq 165 then break; end if;
end for;
assert Nrows(V3) eq 165;
MK_n1 := 45; MK_n2 := 105;
load "makdisi_gen.m";

// --- Taylor expansion at P32 (as in LocalCoordinates of the Y header) ---
PT := 96;
function LocalCoordinates(pt, polys, R, prec)
    kk := BaseRing(R); anchor := Min([i : i in [1..16] | pt[i] ne 0]);
    pt := [x/pt[anchor] : x in pt]; vars := [i : i in [1..16] | i ne anchor];
    J := Matrix(kk, [[Evaluate(Derivative(z, j), pt) : j in vars] : z in polys]);
    assert Rank(J) eq 14;
    inds := []; rowlist := [];
    for i in [1..#polys] do
        trial := rowlist cat [Eltseq(J[i])];
        if Rank(Matrix(kk, trial)) gt #rowlist then
            Append(~rowlist, Eltseq(J[i])); Append(~inds, i);
        end if;
        if #inds eq 14 then break; end if;
    end for;
    found := false; parameter := 0;
    for candidate in vars do
        deps := [j : j in vars | j ne candidate];
        mat := Matrix(kk, [[Evaluate(Derivative(polys[i], j), pt) : j in deps] : i in inds]);
        if Determinant(mat) ne 0 then found := true; parameter := candidate; break; end if;
    end for;
    assert found;
    PS<t> := PowerSeriesRing(kk, prec);
    xs := [PS!x + O(t^prec) : x in pt]; xs[parameter] +:= t;
    for n in [1..prec-1] do
        rhs := Vector(kk, [-Coefficient(Evaluate(polys[i], xs), n) : i in inds]);
        corr := Solution(Transpose(mat), rhs);
        for j in [1..14] do xs[deps[j]] +:= corr[j]*t^n; end for;
    end for;
    assert &and[Evaluate(z, xs) eq 0 : z in polys];
    return xs, pt, anchor, parameter;
end function;
xser, p32, anchor, parameter := LocalCoordinates(Eltseq(P32_candidate), polys, R, PT);
s4 := Q4(xser);
T4 := Matrix(Fp, [[Coefficient(m, j) : j in [0..PT-1]] : m in s4]);              // 105 x PT
for j in [43, 86, 87, 88] do assert Rank(ColumnSubmatrix(T4, 1, j)) eq j; end for;
T4K := ChangeRing(T4, K);
function Bc(j) return Matrix(Basis(Nullspace(ColumnSubmatrix(T4, 1, j)))); end function;
B43 := ChangeRing(Bc(43), K)*V2;
printf "S23|Taylor expansion at P32 to t^%o (anchor %o, parameter %o); orders 43, 86, 87, 88 impose independent conditions [%o s]\n", PT, anchor, parameter, Cputime(started);

function Evaluate2T(W, iw)
    w := RandSection(W);      // W may be row-reduced on the evaluation points; a random section has no zeros there
    Sx := QuotientSpace(W, ScaleRows(B43, w), B43, 2);
    Wn := QuotientSpace(W, ScaleRows(V2, w), V2, 45);
    qd := QuotientSpace(W, ScaleRows(Wn, w), Wn, 1)[1];
    assert &and[c ne 0 : c in Eltseq(qd)];
    G := [];
    for pr in [[1,1],[1,2],[2,2]] do
        vals := Vector(K, [Sx[pr[1], r]*Sx[pr[2], r]/qd[r] : r in [1..NE]]);
        ok, co := IsConsistent(V2, vals); assert ok;
        Append(~G, co);
    end for;
    TG := [g*T4K : g in G];
    assert &and[IsZero(Vector(Eltseq(tg)[1..86])) : tg in TG];
    l := [tg[87] : tg in TG];                      // coefficients of t^86: a^2, a*b, b^2
    assert l[1]*l[3] eq l[2]^2 and (l[1] ne 0 or l[3] ne 0);
    if l[1] ne 0 then al := l[2]; be := -l[1]; jB := 1; else al := K!1; be := K!0; jB := 2; end if;
    // s_x = al*s_1 + be*s_2; s_B = s_jB
    f := al^2*G[1] + 2*al*be*G[2] + be^2*G[3];
    h := jB eq 1 select al*G[1] + be*G[2] else al*G[2] + be*G[3];
    gp := jB eq 1 select G[1] else G[3];
    tf := f*T4K;
    assert IsZero(Vector(Eltseq(tf)[1..88]));
    return f, h, gp, tf;
end function;

W := Matrix(K, [[DecKE(c) : c in row] : row in c16_point])*V2;
function AddC(A, B) return NegClass(ChordClass(A, B)); end function;
PIDX := StringToInteger(GetEnv("PIDX"));
P2x<u> := PolynomialRing(GF(2));
fac := [f[1] : f in Factorization(P2x!CyclotomicPolynomial(AEXT))];
gF := [f : f in fac | f eq (PIDX eq 1 select u^8 + u^5 + u^4 + u^3 + 1 else u^8 + u^7 + u^6 + u^4 + u^2 + u + 1)][1];
F256<w> := ext<GF(2) | gF>;
cgen := [c : c in [w + 1, w^2 + w + 1, w^3 + w + 1, w^3 + w^2 + 1, w^4 + w + 1, w^5 + w^2 + 1] | Order(c) eq 255][1];
assert Order(w) eq 17;
WF := [W];
for i in [1..7] do Append(~WF, FrobeniusClass(WF[i])); end for;
// g(Frob) y = 0: the sum of the Frobenius images with the coefficients of g is zero
function Comb(co)
    out := 0; first := true;
    for i in [1..#co] do
        if co[i] eq 0 then continue; end if;
        if first then out := WF[i]; first := false; else out := AddC(out, WF[i]); end if;
    end for;
    return out;
end function;
gl := [Integers()!c : c in Coefficients(gF)];
assert EqualClass(Comb(gl[1..8]), FrobeniusClass(WF[8]));
function Enc(v) return [Seqint(ChangeUniverse(Eltseq(c), ZZ), p) : c in Eltseq(v)]; end function;
PrintFile(OUT, Sprintf("c16n_quad := %o;\nc16n_pairs4 := %o;\nc16n_modulus := %o;\nc16n_recs := [*", quad, pairs4, c16_modulus) : Overwrite := true);
rs := {};
for j in [0..14] do
    co := [Integers()!c : c in Eltseq(cgen^j)];
    Wj := Comb(co);
    f, h, gp, tf := Evaluate2T(Wj, 1);
    assert tf[89] ne 0;
    r := [tf[89+i]/tf[89] : i in [1..5]];
    assert Degree(MinimalPolynomial(r[1], Fp)) eq 17;
    Include(~rs, MinimalPolynomial(r[1], Fp));
    gv := f*V2; hv := h*V2; gpv := gp*V2;
    assert &and[gv[i]*gpv[i] eq hv[i]^2 : i in [1..NE]];
    PrintFile(OUT, Sprintf("<%o, %o, %o, %o, %o, %o>%o", PIDX, j, Enc(f), Enc(h), Enc(gp), Enc(Vector(r)), j lt 14 select "," else ""));
    printf "S24|representative %o: coefficients %o; r(x) of degree 17 [%o s]\n", j, co, Cputime(started);
end for;
PrintFile(OUT, "*];");
printf "S24|distinct Frobenius orbits of r(x): %o of 15\n", #rs;
assert #rs eq 15;
printf "DONE|24_C_ENUM [%o s]\n", Cputime(started);
quit;
