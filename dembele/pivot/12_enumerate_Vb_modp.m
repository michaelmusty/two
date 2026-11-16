// D166 step 4.3: enumerate V_b mod p by Frobenius orbits and store, for each
// orbit representative, the six functions g_ij (coordinates in G44) and f_x.
// V_b = F'*y1 + F'*y2, F' = F_2[Frob]/g; representatives of (V_b - 0)/<Frob>:
// (gamma^k, c2), k = 0..14, c2 in F' (job C1IDX = k), and (0, gamma^k) (job 15).
// Env: BASE1, BASE2 (point tags), C1IDX, OUT. Output lines: masks, g, f.
// Header of script 11 follows.
// G44 = H^0(Y, pi^*O(44*P32)) (69-dim). For x in J(Y)[2] and a basis s1,s2,s3
// of S_x = H^0(x (x) pi^*O(22*P32)), the six functions g_ij = s_i*s_j/phi lie
// in G44 and satisfy the 2x2 minor equations g_ij*g_kl = g_ik*g_jl. Unknowns
// 6*69 = 414, gauge GL_3 (9). If the linearized minor map has rank 405 the
// solution is isolated and can be Hensel-lifted without Jacobian arithmetic
// on Y. Header of script 10 follows (same notation).
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


// --- G44 = {gamma/Q^2 : gamma in L(2*D0), gamma*q'*q'' in Q^2*L(2*D0)} ---
ANY := ChangeRing(Solution(S0v, ANv), Fp)*RowSubmatrix(W1, 1, 28);     // A_N at the points of Y
QYp := Vector(Fp, Qs)*RowSubmatrix(W1, 1, 28);
ra := [Vector(Fp, [Random(Fp) : i in [1..6]])*ANY : n in [1..12]];
rb := [Vector(Fp, [Random(Fp) : i in [1..6]])*ANY : n in [1..12]];
AA := Matrix(Fp, [[ra[n][r]*rb[n][r] : r in [1..NY]] : n in [1..12]]);
L4 := ZeroMatrix(Fp, 0, NY);
for trial in [1..12] do
    L4 := Matrix(Basis(RowSpace(VerticalJoin(L4, Scale(W2, Vector(Fp, [Random(Fp) : i in [1..195]])*W2)))));
    if Nrows(L4) eq 453 then break; end if;
end for;
printf "S11|L(4*D0) on Y: dimension %o (Riemann-Roch 453)\n", Nrows(L4);
assert Nrows(L4) eq 453;
Q2Y := Vector(Fp, [QYp[r]^2 : r in [1..NY]]);
good := [r : r in [1..NY] | Q2Y[r] ne 0];           // Q may vanish at a few evaluation points
printf "S11|evaluation points with Q nonzero: %o of %o\n", #good, NY;
G44n := QS(AA, Scale(W2, Q2Y), W2, 69, "G44 = H^0(Y, pi^*O(44*P32))");
G44 := Matrix(Fp, [[G44n[i,r]/Q2Y[r] : r in good] : i in [1..69]]);
assert Rank(G44) eq 69;
G44K := ChangeRing(G44, K);
printf "S11|G44 built [%o s]\n", Cputime(started);


function AddC(A, B) return NegClass(ChordClass(A, B)); end function;
QK2 := ChangeRing(Q2Y, K);
idx := [[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]];
G44f := Matrix(K, [[G44K[i,Index(good, f[j])] : j in [1..3], f in fibs] : i in [1..69]]);   // j is the inner index  // G44 at fibre points
function EncKE(c) return Seqint(ChangeUniverse(Eltseq(c), Integers()), p); end function;
function Data(W)
    WTZ := ProductSpace(TZY, W, 132);
    Sx := QuotientSpace(Tprime, WTZ, W, 3);
    WW := ProductSpace(W, W, 195);
    phi := QuotientSpace(V2, WW, V2, 1)[1];
    assert &and[phi[r] ne 0 : r in good];
    gco := [];
    for pr in idx do
        ok, co := IsConsistent(G44K, Vector(K, [Sx[pr[1],r]*Sx[pr[2],r]/(phi[r]*QK2[r]) : r in good]));
        assert ok; Append(~gco, co);
    end for;
    // trace forms and f_x
    M := ZeroMatrix(K, 3, 3); bco := [];
    for n in [1..6] do
        gv := gco[n]*G44f;
        bv := Vector(K, [gv[3*m-2] + gv[3*m-1] + gv[3*m] : m in [1..NF]]);
        ok, co := IsConsistent(Lfib, bv); assert ok;
        Append(~bco, co);
        M[idx[n][1], idx[n][2]] := (co*lamK)[1]; M[idx[n][2], idx[n][1]] := M[idx[n][1], idx[n][2]];
    end for;
    ker := Basis(Nullspace(M)); assert #ker eq 1;
    c := ker[1];
    f := &+[(idx[n][1] eq idx[n][2] select 1 else 2)*c[idx[n][1]]*c[idx[n][2]]*bco[n] : n in [1..6]];
    piv := Min([i : i in [1..Ncols(f)] | f[i] ne 0]);
    return gco, f/f[piv];
end function;
assert &and[Index(good, f[j]) gt 0 : f in fibs, j in [1..3]];
// F' = F_2[t]/g and a generator gamma
F2x<u> := PolynomialRing(GF(2));
gpol := u^8 + u^7 + u^6 + u^4 + u^2 + u + 1;
FF<tt> := ext<GF(2) | gpol>;
gam := PrimitiveElement(FF);
function Mask(c) return Seqint([Integers()!e : e in Eltseq(c)], 2); end function;
y1 := ReadPoint(GetEnv("BASE1")); y2 := ReadPoint(GetEnv("BASE2"));
B1 := [FrobPow(y1, i) : i in [0..7]]; B2 := [FrobPow(y2, i) : i in [0..7]];
function Combo(B, mask)
    bits := [i : i in [1..8] | BitwiseAnd(mask, 2^(i-1)) ne 0];
    z := B[bits[1]];
    for j in [2..#bits] do z := AddC(z, B[bits[j]]); end for;
    return z;
end function;
C1 := StringToInteger(GetEnv("C1IDX")); OUT := GetEnv("OUT");
PrintFile(OUT, Sprintf("// job %o; G44 basis checksum %o; generator mask %o", C1, &+[Integers()!c : c in Eltseq(G44)] mod 10^12, Mask(gam)) : Overwrite := true);
procedure Emit(OUT, m1, m2, W)
    gco, f := Data(W);
    PrintFile(OUT, Sprintf("<%o, %o, %o, %o>,", m1, m2, [[EncKE(c) : c in Eltseq(v)] : v in gco], [EncKE(c) : c in Eltseq(f)]));
end procedure;
count := 0;
if C1 eq 15 then
    for kk in [0..14] do
        m2 := Mask(gam^kk);
        Emit(OUT, 0, m2, Combo(B2, m2)); count +:= 1;
    end for;
else
    m1 := Mask(gam^C1);
    z := Combo(B1, m1);
    Emit(OUT, m1, 0, z); count +:= 1; mask := 0;
    for n in [1..255] do
        g1 := BitwiseXor(n, n div 2);
        bit := Valuation(BitwiseXor(g1, mask), 2);
        z := AddC(z, B2[bit+1]); mask := g1;
        Emit(OUT, m1, mask, z); count +:= 1;
        if n mod 16 eq 0 then printf "S12|job %o: %o of 256 points [%o s]\n", C1, n + 1, Cputime(started); end if;
    end for;
    // control: the walk ends at z0 + Frob^7 y2
    printf "S12|control: end of walk = base + Frob^7 y2: %o\n", EqualClass(z, AddC(Combo(B1, m1), B2[8]));
end if;
printf "DONE|12_ENUMERATE|job %o|points %o [%o s]\n", C1, count, Cputime(started);
quit;
