// D165 step 4.1: a global evaluation function on J(Y), tested mod p on V_b.
// For a class x (2-torsion) represented by W = L(2*D0 - D'), D0 = pi^*(2H - G):
//   S_x = H^0(x (x) pi^*O(22 P32)) = {s in W vanishing on pi^*Z}, where Q is a
//         quadric through G + 22*P32 and Z = div(Q) - G - 22*P32 (3-dimensional);
//   b(s,s') = Tr_{Y/C}(s*s'/(phi*Q^2)) in L_C(44*P32), div(phi) = 2D' - 2D0;
//   lambda = leading coefficient at P32; the radical of lambda o b on S_x is the
//   line of sections vanishing at both points of Y above P32; s_x spans it;
//   f_x = b(s_x, s_x) in L_C(44*P32), up to a scalar.
// The space L_C(44*P32), lambda and the map pi are global; G, Q, Z are not.
// Files: state_in.m, ymodel_in.m, exact data, makdisi_gen.m, <tag>.pt.
// Env: TAGS (comma-separated point tags), OUT.
SetQuitOnError(true); SetColumns(0); SetSeed(101);
started := Cputime();
load "state_in.m";
load "ymodel_in.m";
p := ym_p; Fp := GF(p); k := Fp; AEXT := 17; K := GF(p, AEXT);
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
// --- Y-level model and library ---
W1 := Matrix(Fp, ym_W1); NY := Ncols(W1);
W2 := Matrix(Fp, [[W1[pr[1],r]*W1[pr[2],r] : r in [1..NY]] : pr in ym_pairs2]);
W3 := Matrix(Fp, [[W1[pr[1],r]*W2[pr[2],r] : r in [1..NY]] : pr in ym_pairs3]);
V1 := ChangeRing(W1, K); V2 := ChangeRing(W2, K); V3 := ChangeRing(W3, K);
MK_n1 := 66; MK_n2 := 195; q := p; efrob := [1..NY]; etau := [1..NY];
load "makdisi_gen.m";
function FrobPow(W, i)
    return Matrix(K, [[Frobenius(c, i) : c in Eltseq(v)] : v in Rows(W)]);
end function;
function DecKE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..AEXT]];
    return K!s;
end function;
function ReadPoint(tag)
    s := Read(tag cat ".pt");
    i := Position(s, "tp_point := ");
    j := #s; while s[j] ne "]" do j -:= 1; end while;
    rows := eval s[i+12..j];
    return Matrix(K, [[DecKE(c) : c in row] : row in rows]);
end function;

// --- rational points of C (chart x16 = 1) and quadric/quartic value matrices ---
IC := Ideal(C_candidate);
pointset := {};
for a in k do
    S := Scheme(P, IC + ideal<R | R.15 - a*R.16>);
    pointset join:= {Eltseq(x) : x in Points(S)};
end for;
cpts := [[c/x[16] : c in x] : x in Setseq(pointset) | x[16] ne 0];
NC := #cpts;
function MonVals(e, xs) return &*[xs[t]^e[t] : t in [1..16] | e[t] ne 0]; end function;
E2 := Matrix(Fp, [[MonVals(e, x) : x in cpts] : e in st_exps2]);
assert Rank(E2) eq 45;
function IndependentIndices(M)
    e := EchelonForm(Transpose(M)); out := [];
    for v in Rows(e) do
        if v ne 0 then Append(~out, Min([j : j in [1..Ncols(e)] | v[j] ne 0])); end if;
    end for;
    return out;
end function;
allpairs := [[i,j] : j in [i..45], i in [1..45]];
big := Matrix(Fp, [[E2[pr[1],r]*E2[pr[2],r] : r in [1..NC]] : pr in allpairs]);
ii := IndependentIndices(big); assert #ii eq 105;
pairs4 := [allpairs[i] : i in ii]; E4 := Matrix([big[i] : i in ii]);
printf "S10|rational affine points of C: %o; quadrics 45, quartics 105 [%o s]\n", NC, Cputime(started);

// --- local parameter at P32 (as in script 06) ---
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
    return xs, pt;
end function;
NP := 22;
xser, p32 := LocalCoordinates(Eltseq(P32_candidate), polys, R, NP + 2);
mser := [MonVals(e, xser) : e in st_exps2];
cond := Matrix(Fp, [[Coefficient(m, j) : j in [0..NP-1]] : m in mser]);   // 45 x 22
lead := Vector(Fp, [Coefficient(m, NP) : m in mser]);
S0c := Matrix(Fp, ym_S0_coefficients);                // quadrics through G
ANc := Matrix(Basis(Nullspace(S0c*cond)))*S0c;        // quadrics through G + 22*P32
printf "S10|quadrics through G + %o*P32: dimension %o (expected 6)\n", NP, Nrows(ANc);
assert Nrows(ANc) eq 6;
repeat
    Qc := Vector(Fp, [Random(Fp) : i in [1..6]])*ANc;
    q22 := (Qc, lead);
until q22 ne 0;
ANv := ANc*E2; Qv := Qc*E2; S0v := S0c*E2;
function Scale(A, f) return Matrix(BaseRing(A), [[v[j]*f[j] : j in [1..Ncols(A)]] : v in Rows(A)]); end function;
// T_Z = quadrics through G + Z = {t in S0 : t*A_N in Q*quadrics}
function QS(A, B, V, dim, name)
    eqs := Transpose(Matrix(Basis(Nullspace(Transpose(B)))));
    current := V;
    for trial in [1..16] do
        ker := Matrix(Basis(Nullspace(Scale(current, RandSection(A))*eqs)));
        current := ker*current;
        if Nrows(current) le dim then break; end if;
    end for;
    printf "S10|%o: dimension %o (expected %o)\n", name, Nrows(current), dim;
    assert Nrows(current) eq dim;
    return current;
end function;
TZv := QS(ANv, Scale(E2, Qv), S0v, 7, "T_Z");
TZs := Solution(S0v, TZv);                            // coordinates in the S0 basis (7 x 28)
Qs := Solution(S0v, Qv);
// L_C(44*P32) = {F/Q^2 : F quartic, F*q'*q'' in Q^2*quartics for q', q'' in A_N}
// (q', q'' must not be forced to vanish on G, or poles on G would be allowed.)
APv := Matrix(Basis(Nullspace(cond)))*E2;            // quadrics with order >= 22 at P32
assert Nrows(APv) eq 23;
ra := [Vector(Fp, [Random(Fp) : i in [1..23]])*APv : n in [1..12]];
rb := [Vector(Fp, [Random(Fp) : i in [1..23]])*APv : n in [1..12]];
ANN := Matrix(Fp, [[ra[n][r]*rb[n][r] : r in [1..NC]] : n in [1..12]]);
Q2v := Vector(Fp, [Qv[r]^2 : r in [1..NC]]);
LFv := QS(ANN, Scale(E4, Q2v), E4, 2*NP + 1 - 16, "L_C(44*P32)");
LFc := Solution(E4, LFv);                             // 29 x 105 coefficients on pairs4
m2P := [MonVals(e, p32) : e in st_exps2];
m4P := Vector(Fp, [m2P[pr[1]]*m2P[pr[2]] : pr in pairs4]);
lamF := LFc*Transpose(Matrix(m4P));                   // lambda on the basis (up to q22^2)
assert not IsZero(lamF);
printf "S10|T_Z dimension 7, L_C(%o*P32) dimension %o, lambda nonzero [%o s]\n", 2*NP, Nrows(LFv), Cputime(started);

// --- complete rational fibres of Y -> C among the evaluation points ---
bases := [[Fp!c : c in pt[1..16]] : pt in ym_points];
groups := AssociativeArray();
for i in [1..NY] do
    key := bases[i];
    if IsDefined(groups, key) then Append(~groups[key], i); else groups[key] := [i]; end if;
end for;
fibs := [groups[key] : key in Keys(groups) | #groups[key] eq 3];
fibc := [Index(cpts, bases[f[1]]) : f in fibs];
assert &and[c gt 0 : c in fibc] and &and[Qv[c] ne 0 : c in fibc];
NF := #fibs;
Lfib := Matrix(K, [[LFv[i,c]/Q2v[c] : c in fibc] : i in [1..Nrows(LFv)]]);
assert Rank(Lfib) eq Nrows(LFv);
printf "S10|complete fibres: %o [%o s]\n", NF, Cputime(started);
Tprime := RowSubmatrix(V1, 1, 28);
TZY := ChangeRing(TZs, K)*Tprime;
QY := Vector(K, Qs)*Tprime;
lamK := ChangeRing(lamF, K);

function EvalClass(W)
    t0 := Cputime();
    WTZ := ProductSpace(TZY, W, 132);
    Sx := QuotientSpace(Tprime, WTZ, W, 3);
    WW := ProductSpace(W, W, 195);
    phi := QuotientSpace(V2, WW, V2, 1)[1];
    assert &and[phi[i] ne 0 : i in f, f in fibs];
    bco := [[* 0, 0, 0 *], [* 0, 0, 0 *], [* 0, 0, 0 *]];
    M := ZeroMatrix(K, 3, 3);
    for i in [1..3] do for j in [i..3] do
        bv := Vector(K, [&+[Sx[i,y]*Sx[j,y]/phi[y] : y in fibs[n]]/QY[fibs[n][1]]^2 : n in [1..NF]]);
        ok, co := IsConsistent(Lfib, bv);
        assert ok;                                   // b(s,s') lies in L_C(44*P32)
        bco[i][j] := co; bco[j][i] := co;
        M[i,j] := (co*lamK)[1]; M[j,i] := M[i,j];
    end for; end for;
    rk := Rank(M);
    ker := Basis(Nullspace(M));
    assert rk eq 2 and #ker eq 1;
    c := ker[1];
    f := &+[c[i]*c[j]*bco[i][j] : i, j in [1..3]];
    piv := Min([i : i in [1..Ncols(f)] | f[i] ne 0]);
    return f/f[piv], Cputime(t0);
end function;

TAGS := Split(GetEnv("TAGS"), ",");
vals := [* *];
for tag in TAGS do
    y := ReadPoint(tag);
    f1, t1 := EvalClass(y);
    printf "S10|%o: trace forms lie in L_C(44*P32), rank of lambda-form 2, f computed [%o s]\n", tag, t1;
    f2 := EvalClass(NegClass(y));
    printf "S10|%o: second representative of the same class gives the same f: %o\n", tag, f1 eq f2;
    f3 := EvalClass(FrobPow(y, 1));
    fr := Vector(K, [Frobenius(c, 1) : c in Eltseq(f1)]);
    printf "S10|%o: f(Frob y) = Frob(f(y)): %o; f(Frob y) = f(y): %o\n", tag, f3 eq fr, f3 eq f1;
    printf "S10|%o: nonzero coordinates of f: %o of %o; coordinates in F_p: %o\n", tag, #[c : c in Eltseq(f1) | c ne 0], Ncols(f1), #[c : c in Eltseq(f1) | c^p eq c];
    Append(~vals, f1);
end for;
for i in [1..#TAGS] do for j in [i+1..#TAGS] do
    printf "S10|f(%o) = f(%o): %o\n", TAGS[i], TAGS[j], vals[i] eq vals[j];
end for; end for;
printf "DONE|10_EVAL_FUNCTION [%o s]\n", Cputime(started);
quit;
