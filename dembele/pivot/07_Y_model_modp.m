// D162 step 3a: evaluation model of the genus-64 curve Y mod p, and a
// group-order test of its Jacobian over F_p.
// Y = Z/sigma, Z: v^3 = h over X, sigma = (tau, v -> a/v), h*tau(h) = a^3.
// Sections of pi^*(D_C), D_C = 2H - G (deg 43): s0 + s1*v + tau(s1)*a/v with
//   s0 in L_C(2H - G)             (28-dim, even quadrics vanishing on G),
//   s1 in L_X(E_R - Dminus - pi^*G) (38-dim), written s1 = t/r with r in
//   L(2D0 - E_R) fixed and t in L(2D0 - R' - Dminus - pi^*G).
// Evaluation points: rational points of Y. G: 17 rational points of C, split
// in X, with no rational point of Y above.
// Files: state_in.m, cubic_in.m, exact data, state_lib.m, makdisi_lib.m,
// makdisi_gen.m. Env: ORDER (#J(Y)(F_p) predicted from Hecke), OUT.
SetQuitOnError(true); SetColumns(0); SetSeed(162);
started := Cputime();
load "state_in.m";
load "state_lib.m";
load "makdisi_lib.m";
load "cubic_in.m";
Fp := GF(p); k := Fp; assert cub_p eq p;
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
load "cm_frame_B3_rational_model.m";
function Form(row, mons) return &+[row[i]*mons[i] : i in [1..#mons]]; end function;
mon := [R.(pr[1])*R.(pr[2]) : pr in pairs];
num := Form(rational_numerator, mon); den := Form(rational_denominator, mon);
ellF := &+[branch_parameter_linear_form[i]*R.i : i in [1..16]];
IC := Ideal(C_candidate);
pointset := {};
for a in k do
    S := Scheme(P, IC + ideal<R | R.15 - a*R.16>);
    pointset join:= {Eltseq(x) : x in Points(S)};
end for;
cpoints := Setseq(pointset);   // points with x16 = 0 are omitted on purpose
printf "S07|affine rational points of C: %o [%o s]\n", #cpoints, Cputime(started);

// Section values of the X-level bases at a point (xs with x16 = 1, w).
oddMk := Transpose(Matrix(k4, st_oddrows));
qc := Vector(k4, cub_q_coefficients); uc := Vector(k4, cub_u_coefficients);
fc := Vector(k4, cub_f_coefficients); cn := k4!cub_norm_scalar;
function Vals(xs, w)
    lv := &+[ellc[j]*xs[j] : j in [1..16]];
    ev2 := [&*[xs[t]^e[t] : t in [1..16]] : e in st_exps2];
    odd := Vector(k4, [&*[xs[t]^e[t] : t in [1..16]] : e in st_exps3])*oddMk;
    v1 := ev2 cat [w/lv*c : c in Eltseq(odd)];
    v2 := [v1[pr[1]]*v1[pr[2]] : pr in st_pairs2];
    return v1, v2;
end function;
function Kummer(v1, v2)
    v3 := [v1[pr[1]]*v2[pr[2]] : pr in st_pairs3];
    v4 := [v1[pr[1]]*v3[pr[2]] : pr in cub_pairs4];
    qv := &+[qc[j]*v1[j] : j in [1..81]];
    uv := &+[uc[j]*v4[j] : j in [1..441]];
    fv := &+[fc[j]*v2[j] : j in [1..201]];
    return qv, uv, cn*fv;   // q, u, a
end function;
U3<T> := PolynomialRing(k4);
recs := [* *]; zero := []; nsplit := 0; nskip := 0;
for pt in cpoints do
    if pt[16] eq 0 then continue; end if;
    xs := [k4!(c/pt[16]) : c in pt];
    if &and[Evaluate(z, pt) eq 0 : z in B3_linear_forms] or &and[Evaluate(z, pt) eq 0 : z in D17_extra_quadrics]
       or C_candidate!pt eq P32_candidate then nskip +:= 1; continue; end if;
    nv := Evaluate(num, pt); dv := Evaluate(den, pt); lv := Evaluate(ellF, pt);
    if nv eq 0 or dv eq 0 or lv eq 0 then nskip +:= 1; continue; end if;
    w := Sqrt(k4!(nv/dv)); split := w^p eq w;
    v1, v2 := Vals(xs, w); v1t, v2t := Vals(xs, -w);
    qv, uv, av := Kummer(v1, v2);
    if qv eq 0 or uv eq 0 or av eq 0 then nskip +:= 1; continue; end if;
    hv := cn*uv/qv;
    rts := [r[1] : r in Roots(T^3 - hv)];
    if split then
        nsplit +:= 1;
        assert hv^p eq hv;
        rts := [r : r in rts | r^p eq r];
        if #rts eq 0 then Append(~zero, <xs, w, v1, v2, v1t, v2t>); end if;
    else
        rts := [r : r in rts | r^(p+1) eq av];
        assert #rts eq 1;
    end if;
    for v in rts do Append(~recs, <xs, w, v, av, v1, v2, v1t, v2t, split>); end for;
end for;
printf "S07|candidate points of Y: %o; split base points %o; base points with empty fibre %o; skipped %o [%o s]\n", #recs, nsplit, #zero, nskip, Cputime(started);

// The fixed section r of L(2D0 - E_R) and the auxiliary divisor G.
WRc := Matrix(k4, cub_WR_coordinates); WR := WRc*V2;
UA<a> := PolynomialRing(k4);
load "cm_frame_B3_fiber.m";
A<aa> := quo<UA | UA![Fp!c : c in fiber_nonic_coefficients]>;
minus1 := [A!UA![DecE(c) : c in row] : row in st_branch_minus];
minus2 := [minus1[pr[1]]*minus1[pr[2]] : pr in st_pairs2];
bm2 := Matrix(k4, [[Coefficient(UA!v, j) : j in [0..8]] : v in minus2]);
Gsel := zero[1..17];
repeat
    lam := Vector(k4, [k4!Random(Fp) : i in [1..81]]);
    rc := lam*WRc;
    okr := IsUnit(&+[rc[i]*minus2[i] : i in [1..201]]);
    okr and:= &and[&+[rc[j]*z[4][j] : j in [1..201]] ne 0 and &+[rc[j]*z[6][j] : j in [1..201]] ne 0 : z in Gsel];
until okr;
rvec := rc*V2;
T0 := QuotientSpace(WR, ScaleRows(V2, rvec), V2, 81);
Tc0 := Matrix(Basis(RowSpace(Solution(V2, T0))));
assert Nrows(Tc0) eq 81 and &and[c^p eq c : c in Eltseq(Tc0)];
conds := Tc0*bm2;
for z in Gsel do conds := HorizontalJoin(conds, Tc0*Transpose(Matrix(k4, [z[4], z[6]]))); end for;
assert Ncols(conds) eq 43;
Tc := Matrix(Basis(Nullspace(conds)))*Tc0;
Tc := Matrix(Basis(RowSpace(Tc)));
assert Nrows(Tc) eq 38 and &and[c^p eq c : c in Eltseq(Tc)];
E0 := Matrix(k4, [[z[3][j] : j in [1..45]] : z in Gsel]);   // even sections at G
S0c := Matrix(Basis(Nullspace(Transpose(E0))));
assert Nrows(S0c) eq 28 and &and[c^p eq c : c in Eltseq(S0c)];
printf "S07|section spaces: 28 + 38 [%o s]\n", Cputime(started);

// Evaluate the 66 sections at the rational points of Y.
cols := []; kept := [];
for i in [1..#recs] do
    xs, w, v, av, v1, v2, v1t, v2t, split := Explode(recs[i]);
    rx := &+[rc[j]*v2[j] : j in [1..201]]; rt := &+[rc[j]*v2t[j] : j in [1..201]];
    if rx eq 0 or rt eq 0 then continue; end if;
    s0 := S0c*Matrix(k4, 45, 1, v1[1..45]);
    s1 := Tc*Matrix(k4, 201, 1, v2)*(v/rx) + Tc*Matrix(k4, 201, 1, v2t)*(av/(v*rt));
    col := Eltseq(s0) cat Eltseq(s1);
    assert &and[c^p eq c : c in col];
    Append(~cols, [Fp!c : c in col]); Append(~kept, i);
end for;
NY := #cols;
W1 := Transpose(Matrix(Fp, cols));
printf "S07|evaluation points on Y: %o; rank of 66 sections: %o [%o s]\n", NY, Rank(W1), Cputime(started);
assert Rank(W1) eq 66;
function IndependentIndices(M)
    e := EchelonForm(Transpose(M)); out := [];
    for v in Rows(e) do
        if v ne 0 then Append(~out, Min([j : j in [1..Ncols(e)] | v[j] ne 0])); end if;
    end for;
    return out;
end function;
function Grow(Lo, Hi, target)
    acc := ZeroMatrix(Fp, 0, NY); prs := [];
    for i in [1..Nrows(Lo)] do
        cand := Matrix(Fp, [[Lo[i,r]*Hi[j,r] : r in [1..NY]] : j in [1..Nrows(Hi)]]);
        both := VerticalJoin(acc, cand); pp := prs cat [[i,j] : j in [1..Nrows(Hi)]];
        ii := IndependentIndices(both); acc := Matrix([both[j] : j in ii]); prs := [pp[j] : j in ii];
    end for;
    return acc, prs;
end function;
W2, ypairs2 := Grow(W1, W1, 195);
printf "S07|rank of products in L(2*D0): %o (Riemann-Roch 195)\n", Nrows(W2);
assert Nrows(W2) eq 195;
W3, ypairs3 := Grow(W1, W2, 324);
printf "S07|rank of products in L(3*D0): %o (Riemann-Roch 324) [%o s]\n", Nrows(W3), Cputime(started);
assert Nrows(W3) eq 324;

// Jacobian arithmetic on Y over F_p and the group-order test.
V1 := W1; V2 := W2; V3 := W3; MK_n1 := 66; MK_n2 := 195;
q := p; efrob := [1..NY]; etau := [1..NY];
load "makdisi_gen.m";
function AddC(A, B) return NegClass(ChordClass(A, B)); end function;
function Mul(n, D)
    bits := Reverse(Intseq(n, 2)); Rr := D;
    for i in [2..#bits] do
        Rr := AddC(Rr, Rr);
        if bits[i] eq 1 then Rr := AddC(Rr, D); end if;
    end for;
    return Rr;
end function;
function RandomClass()
    repeat
        J := [Random(1, NY) : i in [1..129]];
    until #Seqset(J) eq 129;
    W := Matrix(Basis(Nullspace(Matrix(Fp, [[V2[i,j] : j in J] : i in [1..195]]))))*V2;
    assert Nrows(W) eq 66;
    return W;
end function;
N := StringToInteger(GetEnv("ORDER"));
D := RandomClass();
t0 := Cputime(); D2 := AddC(D, D); printf "S07|one addition over F_%o: %o s\n", p, Cputime(t0);
assert not ZeroClass(D);
Z0 := Mul(N, D);
okN := ZeroClass(Z0);
printf "S07|[#J(Y)(F_p) predicted] * random class = 0: %o [%o s]\n", okN, Cputime(started);
D3 := RandomClass(); ok3 := ZeroClass(Mul(N, D3));
ctl := ZeroClass(Mul(N + 2, D3));
printf "S07|second random class: %o; control with order+2 is zero: %o [%o s]\n", ok3, ctl, Cputime(started);
function FpM(M) return [[Integers()!c : c in Eltseq(r)] : r in Rows(M)]; end function;
OUT := GetEnv("OUT");
PrintFile(OUT, Sprintf("ym_p := %o;\nym_r_coefficients := %o;\nym_T_coefficients := %o;\nym_S0_coefficients := %o;", p, [Integers()!(Fp!c) : c in Eltseq(rc)], FpM(ChangeRing(Tc, Fp)), FpM(ChangeRing(S0c, Fp))) : Overwrite := true);
PrintFile(OUT, Sprintf("ym_G_points := %o;", [[Integers()!(Fp!c) : c in z[1]] cat [Integers()!(Fp!z[2])] : z in Gsel]));
PrintFile(OUT, Sprintf("ym_points := %o;", [[Enc(c) : c in recs[i][1]] cat [Enc(recs[i][2]), Enc(recs[i][3])] : i in kept]));
PrintFile(OUT, Sprintf("ym_pairs2 := %o;\nym_pairs3 := %o;\nym_W1 := %o;", ypairs2, ypairs3, FpM(W1)));
assert okN and ok3 and not ctl;
print "PASS|07_Y_MODEL";
quit;
