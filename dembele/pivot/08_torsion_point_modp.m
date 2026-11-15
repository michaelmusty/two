// D162 step 3b: one point of the target 2-torsion space V_b in J(Y) over
// K = F_p^17 (p = 673), with checkpoints.
// x random in J(K); x1 = Frob(x) - x lies in G = ker Phi_17(Frob); G is a
// Z[zeta_17]-module killed by L(zeta); y = e(Frob) x1 with e a short element
// of the odd part of the ideal (L(zeta)), e not in the prime above 2 that
// supports V_b. Then y is in V_b.
// Files: state_in.m, cubic_in.m, ymodel_in.m, hecke_in.m, exact data,
// makdisi_gen.m. Env: SEED, TAG (checkpoint/result prefix), MAXOPS (optional
// cap on additions for timing runs), NFIB (fibres for K-points, default 8).
SetQuitOnError(true); SetColumns(0);
seed := StringToInteger(GetEnv("SEED")); SetSeed(seed);
TAG := GetEnv("TAG");
maxops := GetEnv("MAXOPS") eq "" select 10^9 else StringToInteger(GetEnv("MAXOPS"));
nfib := GetEnv("NFIB") eq "" select 8 else StringToInteger(GetEnv("NFIB"));
started := Cputime();
load "state_in.m";
load "cubic_in.m";
load "ymodel_in.m";
load "hecke_in.m";
p := st_p; assert ym_p eq p and cub_p eq p;
Fp := GF(p); AEXT := 17;

// --- the multiplier e ---
QQ2<aa, tt> := PolynomialRing(Rationals(), 2);
function LPoly(f)
    return hk_Z!UnivariatePolynomial(Resultant(Evaluate(f, aa), tt^2 - aa*tt + p, aa));
end function;
Lp := LPoly(hk_p16)*LPoly(hk_p48); assert Degree(Lp) eq 128;
Qz<zeta> := CyclotomicField(AEXT); O := MaximalOrder(Qz);
I := ideal<O | O!Evaluate(Lp, zeta)>;
P2 := [pp[1] : pp in Factorization(ideal<O | 2>)];
v2 := [Valuation(I, pp) : pp in P2];
assert Sort(v2) eq [0, 2];
ptarget := P2[Index(v2, 2)];
Aodd := I*ptarget^-2;
Mb := Matrix(Integers(), [Eltseq(Qz!bb) : bb in Basis(Aodd)]);
Ml := LLL(Mb);
evec := [];
for r in Rows(Ml) do
    if Valuation(O!(Qz!Eltseq(r)), ptarget) eq 0 then evec := Eltseq(r); break; end if;
end for;
assert #evec eq AEXT - 1;
nbits := Max([Ilog2(Abs(c)) + 2 : c in evec | c ne 0]);
printf "S08|multiplier: 16 coefficients, at most %o bits [%o s]\n", nbits, Cputime(started);
function NAF(n)
    s := Sign(n); n := Abs(n); out := [];
    while n gt 0 do
        if n mod 2 eq 1 then d := 2 - (n mod 4); n -:= d; else d := 0; end if;
        Append(~out, s*d); n div:= 2;
    end while;
    return out;
end function;
digits := [NAF(c) : c in evec];
nd := Max([#d : d in digits]);
digits := [d cat [0 : i in [#d+1..nd]] : d in digits];
printf "S08|NAF length %o, nonzero digits %o\n", nd, &+[#[x : x in d | x ne 0] : d in digits];

// --- fields and the model over K ---
K := GF(p, AEXT); K2 := GF(p, 2*AEXT); k2 := GF(p, 2);
k := Fp;
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
load "cm_frame_B3_rational_model.m";
load "cm_frame_B3_fiber_structure.m";
RK := ChangeRing(R, K); PK := ProjectiveSpace(RK); RK2 := ChangeRing(R, K2);
polysK := [RK!f : f in polys];
function Form(row, mons) return &+[row[i]*mons[i] : i in [1..#mons]]; end function;
mon := [R.(pr[1])*R.(pr[2]) : pr in pairs];
num := RK2!Form(rational_numerator, mon); den := RK2!Form(rational_denominator, mon);
QK := p^AEXT;
ellc := [K2!(Fp!c) : c in branch_parameter_linear_form];
oddMk := Transpose(Matrix(K2, st_oddrows));
qc := cub_q_coefficients; uc := cub_u_coefficients; fc := cub_f_coefficients; cn := K2!cub_norm_scalar;
rc := ym_r_coefficients;
Tc := Matrix(K2, ym_T_coefficients); S0c := Matrix(K2, ym_S0_coefficients);
function Vals(xs, w)
    lv := &+[ellc[j]*xs[j] : j in [1..16]];
    ev2 := [&*[xs[t]^e[t] : t in [1..16] | e[t] ne 0] : e in st_exps2];
    odd := Vector(K2, [&*[xs[t]^e[t] : t in [1..16] | e[t] ne 0] : e in st_exps3])*oddMk;
    v1 := ev2 cat [w/lv*c : c in Eltseq(odd)];
    v2 := [v1[pr[1]]*v1[pr[2]] : pr in st_pairs2];
    return v1, v2;
end function;
// The 195 sections of L(2*D0_Y) at the point (xs, w, v) of Y; values in K.
function YSections(xs, w, v)
    v1, v2 := Vals(xs, w); v1t, v2t := Vals(xs, -w);
    fv := &+[fc[j]*v2[j] : j in [1..201]]; av := cn*fv;
    rx := &+[rc[j]*v2[j] : j in [1..201]]; rt := &+[rc[j]*v2t[j] : j in [1..201]];
    if rx eq 0 or rt eq 0 then return false, _; end if;
    s0 := S0c*Matrix(K2, 45, 1, v1[1..45]);
    s1 := Tc*Matrix(K2, 201, 1, v2)*(v/rx) + Tc*Matrix(K2, 201, 1, v2t)*(av/(v*rt));
    col := [K!c : c in Eltseq(s0) cat Eltseq(s1)];
    return true, [col[pr[1]]*col[pr[2]] : pr in ym_pairs2];
end function;
function KummerAt(xs, w)
    v1, v2 := Vals(xs, w);
    v3 := [v1[pr[1]]*v2[pr[2]] : pr in st_pairs3];
    v4 := [v1[pr[1]]*v3[pr[2]] : pr in cub_pairs4];
    qv := &+[qc[j]*v1[j] : j in [1..81]];
    uv := &+[uc[j]*v4[j] : j in [1..441]];
    fv := &+[fc[j]*v2[j] : j in [1..201]];
    return qv, uv, cn*fv;
end function;
W1 := Matrix(Fp, ym_W1); NY := Ncols(W1);
W2 := Matrix(Fp, [[W1[pr[1],r]*W1[pr[2],r] : r in [1..NY]] : pr in ym_pairs2]);
W3 := Matrix(Fp, [[W1[pr[1],r]*W2[pr[2],r] : r in [1..NY]] : pr in ym_pairs3]);
assert Rank(W2) eq 195 and Rank(W3) eq 324;
V1 := ChangeRing(W1, K); V2 := ChangeRing(W2, K); V3 := ChangeRing(W3, K);
MK_n1 := 66; MK_n2 := 195; q := p; efrob := [1..NY]; etau := [1..NY];
load "makdisi_gen.m";
function AddC(A, B) return NegClass(ChordClass(A, B)); end function;
function FrobPow(W, i)
    return Matrix(K, [[Frobenius(c, i) : c in Eltseq(v)] : v in Rows(W)]);
end function;
function EncK(W)
    return [[Seqint(ChangeUniverse(Eltseq(c), Integers()), p) : c in Eltseq(v)] : v in Rows(W)];
end function;
function DecKE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..AEXT]];
    return K!s;
end function;
function DecK(rows)
    return Matrix(K, [[DecKE(c) : c in row] : row in rows]);
end function;

ckfile := TAG cat ".ck";
resume := false; ck := [* *];
try
    ck := eval Read(ckfile); resume := true;
catch err
    resume := false;
end try;
if resume then
    pos := ck[1]; ops := ck[2]; R := DecK(ck[3]); x1 := DecK(ck[4]); have := true;
    printf "S08|resumed at digit position %o after %o additions\n", pos, ops;
else
    // --- points of Y over K ---
    U3<T> := PolynomialRing(K2);
    pool := [];   // columns of 195 section values
    fib := 0;
    while fib lt nfib do
        a0 := Random(K); fib +:= 1;
        t0 := Cputime();
        S := Scheme(PK, polysK cat [RK.15 - a0*RK.16]);
        cpts := [Eltseq(x) : x in Points(S)];
        printf "S08|fibre %o: %o points of C over K [%o s]\n", fib, #cpts, Cputime(t0);
        for pt in cpts do
            if pt[16] eq 0 then continue; end if;
            xs := [K2!(c/pt[16]) : c in pt];
            nv := Evaluate(num, xs); dv := Evaluate(den, xs);
            if nv eq 0 or dv eq 0 or &+[ellc[j]*xs[j] : j in [1..16]] eq 0 then continue; end if;
            w := Sqrt(nv/dv); split := w^QK eq w;
            qv, uv, av := KummerAt(xs, w);
            if qv eq 0 or uv eq 0 or av eq 0 then continue; end if;
            hv := cn*uv/qv;
            rts := [r[1] : r in Roots(T^3 - hv)];
            if split then rts := [r : r in rts | r^QK eq r];
            else rts := [r : r in rts | r^(QK + 1) eq av]; assert #rts eq 1; end if;
            for v in rts do
                for i in [0..AEXT-1] do
                    ok, col := YSections([c^(p^i) : c in xs], w^(p^i), v^(p^i));
                    if ok then Append(~pool, col); end if;
                end for;
            end for;
        end for;
    end while;
    printf "S08|points of Y over K in the pool: %o [%o s]\n", #pool, Cputime(started);
    assert #pool ge 40;
    // --- a random class: 30 K-points and 99 rational evaluation points ---
    sel := {};
    while #sel lt 30 do Include(~sel, Random(1, #pool)); end while;
    rat := {};
    while #rat lt 99 do Include(~rat, Random(1, NY)); end while;
    cond := HorizontalJoin(Transpose(Matrix(K, [pool[i] : i in sel])), Matrix(K, [[V2[i,j] : j in rat] : i in [1..195]]));
    x := Matrix(Basis(Nullspace(cond)))*V2;
    assert Nrows(x) eq 66;
    t0 := Cputime(); nx := NegClass(x); tneg := Cputime(t0);
    t0 := Cputime(); x1 := AddC(FrobPow(x, 1), nx); tadd := Cputime(t0);
    printf "S08|one negation %o s, one addition %o s over K\n", tneg, tadd;
    assert not ZeroClass(x1);
    pos := nd; ops := 0; have := false; R := x1;
end if;
nx1 := NegClass(x1);
B := [FrobPow(x1, i) : i in [0..AEXT-2]];
NB := [FrobPow(nx1, i) : i in [0..AEXT-2]];
assert ZeroClass(AddC(B[2], NB[2]));
printf "S08|setup done [%o s]\n", Cputime(started);

// --- Straus multi-scalar multiplication, most significant digit first ---
lastck := Cputime();
while pos ge 1 and ops lt maxops do
    if have then R := AddC(R, R); ops +:= 1; end if;
    for i in [1..AEXT-1] do
        d := digits[i][pos];
        if d eq 0 then continue; end if;
        S := d eq 1 select B[i] else NB[i];
        if have then R := AddC(R, S); ops +:= 1; else R := S; have := true; end if;
    end for;
    pos -:= 1;
    if Cputime(lastck) gt 1800 or pos eq 0 then
        PrintFile(ckfile, Sprintf("[* %o, %o, %o, %o *]", pos, ops, EncK(R), EncK(x1)) : Overwrite := true);
        printf "S08|checkpoint: position %o of %o, %o additions [%o s]\n", pos, nd, ops, Cputime(started);
        lastck := Cputime();
    end if;
end while;
if pos ge 1 then
    printf "S08|stopped by MAXOPS at position %o of %o after %o additions [%o s]\n", pos, nd, ops, Cputime(started);
    quit;
end if;
y := R;
isz := ZeroClass(y);
two := ZeroClass(AddC(y, y));
printf "S08|y = e(Frob)(Frob - 1)x: zero %o; 2*y = 0: %o [%o s]\n", isz, two, Cputime(started);
// g(Frob) y = 0 for the factor g of t^17 - 1 mod 2 attached to ptarget.
F2x<u> := PolynomialRing(GF(2));
gs := [f[1] : f in Factorization(u^AEXT - 1) | Degree(f[1]) eq 8];
res := [];
for g in gs do
    terms := [FrobPow(y, i) : i in [0..8] | Coefficient(g, i) eq 1];
    acc := terms[1];
    for j in [2..#terms] do acc := AddC(acc, terms[j]); end for;
    Append(~res, ZeroClass(acc));
end for;
printf "S08|g(Frob) y = 0 for the two degree-8 factors %o: %o\n", gs, res;
PrintFile(TAG cat ".pt", Sprintf("tp_seed := %o;\ntp_zero := %o;\ntp_two_torsion := %o;\ntp_point := %o;", seed, isz, two, EncK(y)) : Overwrite := true);
printf "DONE|08_TORSION_POINT|additions %o|cpu %o\n", ops, Cputime(started);
quit;
