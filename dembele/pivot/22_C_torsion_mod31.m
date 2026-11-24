// D174, package 1: one 2-torsion point of J(C) over K = F_31^17, C the
// genus-16 base curve (exact canonical model, 91 quadrics in P^15).
// Makdisi arithmetic with D0 = 2K: L(D0), L(2*D0), L(3*D0) = quadrics (45),
// quartics (105), sextics (165) modulo the ideal, as value vectors at NORB
// Frobenius orbits of K-points of C. x random in J(C)(K); x1 = Frob(x) - x
// lies in G = ker Phi_17(Frob), a Z[zeta_17]-module killed by L(zeta);
// y = e(Frob) x1 with e a short element of L(zeta)*P^-2 outside P, P one of
// the two primes above 2 (index PIDX). Then y is in the P-primary part of G.
// Files: cm_frame_curve_candidate.m, cm_frame_marks.m, makdisi_gen.m.
// Env: SEED, PIDX (1 or 2), OUT, NORB (optional, default 22).
SetQuitOnError(true); SetColumns(0);
seed := StringToInteger(GetEnv("SEED")); SetSeed(seed);
PIDX := StringToInteger(GetEnv("PIDX")); OUT := GetEnv("OUT");
NORB := GetEnv("NORB") eq "" select 22 else StringToInteger(GetEnv("NORB"));
started := Cputime();
p := 31; Fp := GF(p); AEXT := 17; K := GF(p, AEXT); ZZ := Integers();
k := Fp;
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";

// --- the multiplier e ---
hk_Z<z> := PolynomialRing(ZZ);
T31 := (z^4 - 8*z^3 - 36*z^2 + 433*z - 899)*(z^4 + 2*z^3 - 56*z^2 + 133*z - 19)*(z^4 + 7*z^3 - 51*z^2 - 407*z - 359)*(z^4 + 17*z^3 + 69*z^2 - 87*z - 649);
QQ2<aa, tt> := PolynomialRing(Rationals(), 2);
Lp := hk_Z!UnivariatePolynomial(Resultant(Evaluate(T31, aa), tt^2 - aa*tt + p, aa));
assert Degree(Lp) eq 32;
Qz<zeta> := CyclotomicField(AEXT); O := MaximalOrder(Qz);
I := ideal<O | O!Evaluate(Lp, zeta)>;
P2 := [pp[1] : pp in Factorization(ideal<O | 2>)];
assert #P2 eq 2 and [Valuation(I, pp) : pp in P2] eq [2, 2];
ptarget := P2[PIDX];
Aodd := I*ptarget^-2;
Ml := LLL(Matrix(ZZ, [Eltseq(Qz!bb) : bb in Basis(Aodd)]));
evec := [];
for r in Rows(Ml) do
    if Valuation(O!(Qz!Eltseq(r)), ptarget) eq 0 then evec := Eltseq(r); break; end if;
end for;
assert #evec eq AEXT - 1;
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
// generators of ptarget as polynomials in Frobenius: 2 and g(zeta), g the factor of Phi_17 mod 2
P2x<u> := PolynomialRing(GF(2));
fac := [f[1] : f in Factorization(P2x!CyclotomicPolynomial(AEXT))];
gsel := [f : f in fac | Valuation(O!Evaluate(hk_Z!f, zeta), ptarget) gt 0];
assert #gsel eq 1;
gco := [ZZ!c : c in Coefficients(gsel[1])];
printf "S22|multiplier: NAF length %o, nonzero digits %o; prime %o: g = %o [%o s]\n", nd, &+[#[x : x in d | x ne 0] : d in digits], PIDX, gsel[1], Cputime(started);

// --- points of C over K ---
RK := ChangeRing(R, K); PK := ProjectiveSpace(RK);
polysK := [RK!f : f in polys];
function SlicePoints()
    a0 := Random(K);
    S := Scheme(PK, polysK cat [RK.15 - a0*RK.16]);
    return [[c/x[16] : c in Eltseq(x)] : x in Points(S) | x[16] ne 0];
end function;
orbs := []; extra := []; seenx := {};
while #orbs lt NORB or #extra lt 60 do
    for pt in SlicePoints() do
        if pt in seenx or pt[15] in Fp then continue; end if;
        Include(~seenx, pt);
        if #orbs lt NORB then Append(~orbs, pt); elif #extra lt 60 then Append(~extra, pt); end if;
    end for;
end while;
evpts := &cat[[[c^(p^i) : c in pt] : i in [0..AEXT-1]] : pt in orbs];
NE := #evpts;
efrob := [((j - 1) mod AEXT) eq 0 select j + AEXT - 1 else j - 1 : j in [1..NE]];
etau := [1..NE]; q := p;
printf "S22|evaluation points: %o orbits, %o points; %o further K-points [%o s]\n", NORB, NE, #extra, Cputime(started);

// --- quadrics, quartics, sextics ---
function IndependentIndices(M)
    e := EchelonForm(Transpose(M)); out := [];
    for v in Rows(e) do
        if v ne 0 then Append(~out, Min([j : j in [1..Ncols(e)] | v[j] ne 0])); end if;
    end for;
    return out;
end function;
allq := [[i, j] : j in [i..16], i in [1..16]];
big := Matrix(K, [[x[pr[1]]*x[pr[2]] : x in evpts] : pr in allq]);
i2 := IndependentIndices(big); assert #i2 eq 45;
quad := [allq[i] : i in i2];
function Q2(x) return [x[pr[1]]*x[pr[2]] : pr in quad]; end function;
V1 := Matrix([big[i] : i in i2]);
all4 := [[i, j] : j in [i..45], i in [1..45]];
big := Matrix(K, [[V1[pr[1], r]*V1[pr[2], r] : r in [1..NE]] : pr in all4]);
i4 := IndependentIndices(big); assert #i4 eq 105;
pairs4 := [all4[i] : i in i4];
V2 := Matrix([big[i] : i in i4]);
function Q4(x) v := Q2(x); return [v[pr[1]]*v[pr[2]] : pr in pairs4]; end function;
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
function AddC(A, B) return NegClass(ChordClass(A, B)); end function;
function FrobPow(W, i)
    for n in [1..i] do W := FrobeniusClass(W); end for;
    return W;
end function;
printf "S22|spaces 45, 105, 165 at %o points [%o s]\n", NE, Cputime(started);

// --- a random class and x1 = Frob(x) - x ---
cond := Transpose(Matrix(K, [Q4(x) : x in extra]));           // 105 x 60
x := Matrix(Basis(Nullspace(cond)))*V2;
assert Nrows(x) eq 45;
t0 := Cputime(); nx := NegClass(x); tneg := Cputime(t0);
t0 := Cputime(); x1 := AddC(FrobPow(x, 1), nx); tadd := Cputime(t0);
printf "S22|one negation %o s, one addition %o s over K\n", tneg, tadd;
assert ZeroClass(AddC(x, nx));
assert EqualClass(FrobPow(x, AEXT), x);
assert not ZeroClass(x1);
nx1 := NegClass(x1);
B := [FrobPow(x1, i) : i in [0..AEXT-2]];
NB := [FrobPow(nx1, i) : i in [0..AEXT-2]];
printf "S22|setup done [%o s]\n", Cputime(started);

// --- Straus multi-scalar multiplication, most significant digit first ---
have := false; ops := 0; y := x1;
for pos in [nd..1 by -1] do
    if have then y := AddC(y, y); ops +:= 1; end if;
    for i in [1..AEXT-1] do
        d := digits[i][pos];
        if d eq 0 then continue; end if;
        S := d eq 1 select B[i] else NB[i];
        if have then y := AddC(y, S); ops +:= 1; else y := S; have := true; end if;
    end for;
    if pos mod 10 eq 0 then printf "S22|position %o, %o additions [%o s]\n", pos, ops, Cputime(started); end if;
end for;
printf "S22|y = e(Frob) x1 after %o additions; zero: %o [%o s]\n", ops, ZeroClass(y), Cputime(started);
function GFrob(w)          // g(Frob) w, coefficients of g mod 2 (w is 2-torsion)
    out := 0; first := true;
    for i in [0..#gco-1] do
        if gco[i+1] eq 0 then continue; end if;
        t := FrobPow(w, i);
        if first then out := t; first := false; else out := AddC(out, t); end if;
    end for;
    return out;
end function;
if not ZeroClass(y) then
    y2 := AddC(y, y); z2 := ZeroClass(y2);
    printf "S22|2*y zero: %o\n", z2;
    if not z2 then
        printf "S22|4*y zero: %o; replacing y by 2*y\n", ZeroClass(AddC(y2, y2));
        y := y2;
    end if;
    printf "S22|g(Frob) y zero: %o\n", ZeroClass(GFrob(y));
    yc := Solution(V2, y);
    assert yc*V2 eq y;
    enc := [[Seqint(ChangeUniverse(Eltseq(c), ZZ), p) : c in Eltseq(v)] : v in Rows(yc)];
    PrintFile(OUT, Sprintf("c16_p := %o;\nc16_quad := %o;\nc16_pairs4 := %o;\nc16_modulus := %o;\nc16_point := %o;", p, quad, pairs4, [ZZ!c : c in Coefficients(DefiningPolynomial(K))], enc) : Overwrite := true);
    printf "S22|written %o (45 x 105 coefficients of W_D in the quartic basis)\n", OUT;
end if;
printf "DONE|22_C_TORSION [%o s]\n", Cputime(started);
quit;
