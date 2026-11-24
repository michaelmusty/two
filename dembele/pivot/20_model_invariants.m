// D172: canonical invariants of the lifted model of Y -> C, and their
// recognition. Uses only the output of script 16 (ly_in.m): G44 =
// H^0(Y, pi^*O(44*P32)) at the points of complete fibres, L_C(44*P32) at the
// fibre base points and its Laurent coefficients at P32. No torsion point.
//  1. Tr: G44 -> L_C(44*P32); W = trace-zero part (expected dimension 40).
//  2. L_C(88*P32) from products of pairs in L_C(44*P32) (values at the base
//     points, Laurent coefficients t^-88..t^-44).
//  3. B_k(g, g') = coefficient of t^(-88+k) of Tr(g*g'). Filtration
//     F_n = {g : B_k(g, .) = 0 on G44 for k < 44 - n}
//         = H^0(Y, pi^*(n*P32) + (ramified point above P32)).
//  4. n0 = smallest n with W meet F_n nonzero. If that space is a line, with
//     generator g0 (canonical up to a scalar), the ratios of the Laurent
//     coefficients of Tr(g0^2) are numbers attached to the cover Y -> C, the
//     point P32 and the parameter t (rational). They lie in the field of
//     definition of the cover.
//  5. LLL recognition in Q, Q(sqrt 2), Q(sqrt -3), Q(sqrt 2, sqrt -3),
//     F = Q(zeta_32)^+ and F(sqrt -3).
// Files: ly_in.m, padic_lib.m. Env: PREC.
SetQuitOnError(true); SetColumns(0);
started := Cputime();
N := StringToInteger(GetEnv("PREC"));
load "ly_in.m";
p := ly_p; assert ly_N eq N; Fp := GF(p); ZN := Integers(p^N);
LIBP := p; LIBF := Fp; LC0 := 0; LC1 := 0;
load "padic_lib.m";
G := Matrix(ZN, ly_G44); NG := Ncols(G); fibs := ly_fibs; NF := #fibs;
Lfib := Matrix(ZN, ly_Lfib); Laur := Matrix(ZN, ly_Laur); NL := Ncols(Laur);
assert Nrows(G) eq 69 and Nrows(Lfib) eq 29 and NL eq 45 and Ncols(Lfib) eq NF;
printf "S20|N = %o; %o points, %o complete fibres [%o s]\n", N, NG, NF, Cputime(started);
fc := [[f[t] : f in fibs] : t in [1..3]];
Gt := [Cols_(G, fc[t]) : t in [1..3]];

// 1. trace
TG := Gt[1] + Gt[2] + Gt[3];
Jc := PivCols(Red(Lfib)); assert #Jc eq 29;
X := Cols_(TG, Jc)*InvN(Cols_(Lfib, Jc));
assert X*Lfib eq TG;
printf "S20|Tr(G44) lies in L_C(44*P32) at all %o fibres mod p^%o; rank of Tr mod p: %o\n", NF, N, Rank(Red(X));
W := KerN(X);
printf "S20|trace-zero part: dimension %o (expected 40)\n", Nrows(W);

// 2. L_C(88*P32)
prs := [[a, b] : b in [a..29], a in [1..29]];
PV := Matrix(ZN, [[Lfib[pr[1], c]*Lfib[pr[2], c] : c in [1..NF]] : pr in prs]);
I88 := IndRows(Red(PV));
printf "S20|products of pairs in L_C(44*P32): rank %o (expected 73)\n", #I88;
assert #I88 eq 73;
PV := Rows_(PV, I88);
PL := Matrix(ZN, [[&+[Laur[prs[k][1], m+1]*Laur[prs[k][2], n-m+1] : m in [0..n]] : n in [0..NL-1]] : k in I88]);
J88 := PivCols(Red(PV)); assert #J88 eq 73;
Pinv := InvN(Cols_(PV, J88));
function LaurOfTr(T)      // rows: values at the fibre base points of elements of L_C(88*P32)
    co := Cols_(T, J88)*Pinv;
    assert co*PV eq T;    // membership in L_C(88*P32): NF - 73 conditions per row
    return co*PL;         // coefficients of t^-88..t^-44
end function;

// 3. bilinear forms on G44
BG := [];
for j in [1..69] do
    T := &+[ScaleP(Gt[t], Gt[t][j]) : t in [1..3]];
    Append(~BG, LaurOfTr(T));          // 69 x 45: B_k(g_j, g_i), rows i, columns k
end for;
printf "S20|Tr(g*g') lies in L_C(88*P32) for all pairs, mod p^%o [%o s]\n", N, Cputime(started);
function Cond(V, n)        // V: r x 69; conditions B_k(v, g_i) = 0, k < 44 - n
    if n ge 44 then return ZeroMatrix(ZN, Nrows(V), 0); end if;
    return V*HorizontalJoin([Cols_(BG[j], [1..44-n]) : j in [1..69]]);
end function;
dG := [69 - Rank(Red(Cond(IdentityMatrix(ZN, 69), n))) : n in [0..44]];
dW := [Nrows(W) - Rank(Red(Cond(W, n))) : n in [0..44]];
printf "S20|dim F_n (n = 0..44), all of G44: %o\n", dG;
printf "S20|dim F_n (n = 0..44), trace-zero part: %o\n", dW;
n0 := Min([n : n in [0..44] | dW[n+1] gt 0]);
d0 := dW[n0+1];
printf "S20|n0 = %o, dimension %o\n", n0, d0;
K0 := KerN(Cond(W, n0))*W;            // exact kernel mod p^N (asserted in KerN)
assert Nrows(K0) eq d0;
printf "S20|the kernel lifts to p^%o with the same dimension [%o s]\n", N, Cputime(started);

// 4. Laurent coefficients of Tr(k_a*k_b)
kv := K0*G; kt := [Cols_(kv, fc[t]) : t in [1..3]];
QL := [[LaurOfTr(Matrix(ZN, 1, NF, [&+[kt[t][a, c]*kt[t][b, c] : t in [1..3]] : c in [1..NF]])) : b in [1..d0]] : a in [1..d0]];
for a in [1..d0] do for b in [a..d0] do
    supp := [k : k in [1..NL] | (ZZ!QL[a][b][1, k]) mod p ne 0];
    ex := [k : k in [1..NL] | QL[a][b][1, k] ne 0];
    printf "S20|Tr(k_%o*k_%o): first nonzero coefficient mod p at t^-%o, mod p^%o at t^-%o (expected at most %o)\n", a, b, 89 - supp[1], N, 89 - ex[1], 2*n0 + 1;
end for; end for;
invs := [];
// 0. control with a known answer type: a function on C with the smallest pole
// order n1 >= 2 at P32 (unique up to scalar and constants); the ratios of its
// Laurent coefficients are rational numbers (C, P32 and t are defined over Q).
dC := [29 - Rank(Red(Cols_(Laur, [1..44-n]))) : n in [0..43]] cat [29];
printf "S20|dim L_C(n*P32), n = 0..44: %o\n", dC;
n1 := Min([n : n in [2..44] | dC[n+1] gt dC[n]]);
KC := KerN(Cols_(Laur, [1..44-n1]))*Laur;
rw := [i : i in [1..Nrows(KC)] | (ZZ!KC[i, 45-n1]) mod p ne 0][1];
assert &and[KC[i, k] eq 0 : k in [1..44-n1], i in [1..Nrows(KC)]];
for j in [1..Min(3, n1-1)] do
    Append(~invs, <Sprintf("CONTROL on C: c(t^-%o)/c(t^-%o) of the function with pole order %o", n1 - j, n1, n1), KC[rw, 45-n1+j]*KC[rw, 45-n1]^-1>);
end for;
if d0 eq 1 then
    q := QL[1][1]; L := Min([k : k in [1..NL] | (ZZ!q[1, k]) mod p ne 0]);
    for j in [1..Min(4, NL - L)] do
        Append(~invs, <Sprintf("c(t^-%o)/c(t^-%o) of Tr(g0^2)", 89 - L - j, 89 - L), q[1, L+j]*q[1, L]^-1>);
    end for;
else
    // d0 >= 2: invariants of the pair of forms (leading, next) under GL_d0
    L := Min([Min([k : k in [1..NL] | (ZZ!QL[a][b][1, k]) mod p ne 0]) : b in [a..d0], a in [1..d0]]);
    M0 := Matrix(ZN, d0, d0, [QL[a][b][1, L] : b in [1..d0], a in [1..d0]]);
    printf "S20|leading form at t^-%o: rank mod p %o\n", 89 - L, Rank(Red(M0));
    if Rank(Red(M0)) eq d0 then
        for j in [1..Min(3, NL - L)] do
            Mj := Matrix(ZN, d0, d0, [QL[a][b][1, L+j] : b in [1..d0], a in [1..d0]]);
            cp := CharacteristicPolynomial(InvN(M0)*Mj);
            for i in [0..d0-1] do
                Append(~invs, <Sprintf("coefficient %o of charpoly(M(t^-%o)^-1 * M(t^-%o))", i, 89 - L, 89 - L - j), Coefficient(cp, i)>);
            end for;
        end for;
    end if;
end if;

K := GF(p, 17);
load "witt_lib.m";
CM := CompanionMatrix(PWZ!phiZ);
trs := [Trace(CM^i) : i in [0..WD-1]];
function WTrace(xx) sq := PadTo(Coefficients(PWZ!xx), WD); return &+[sq[i]*trs[i] : i in [1..WD]]; end function;
function WElt(seq) return WQ!(PWZ!seq); end function;
function WInv(xx)
    xk := K![Fp!(ZZ!c) : c in PadTo(Coefficients(PWZ!xx), WD)];
    assert xk ne 0;
    y := WElt([ZZ!c : c in Eltseq(xk^-1)]); e := 1;
    while e lt N do y := y*(2 - xx*y); e *:= 2; end while;
    assert xx*y eq 1;
    return y;
end function;
// 4b. Combinations that do not depend on the parameter t. For a function u
// with pole order m at P32 let r_u = c(t^(-m+1))/c(t^-m). Under t = alpha*s*(1 + beta*s),
// r_u -> alpha*r_u - m*beta, so D(u, w) = r_u/m - r_w/n scales by alpha and
// ratios of two D's are independent of t. Functions: f17 on C (pole order 17),
// q0 = Tr(g0^2) (49), z = Norm(g0) (pole order mz), f_x (43).
r17 := invs[1][2];
if d0 eq 1 then
    NZ := Matrix(ZN, 1, NF, [kt[1][1, c]*kt[2][1, c]*kt[3][1, c] : c in [1..NF]]);
    zl := LaurOfTr(NZ);
    Lz := Min([k : k in [1..NL] | (ZZ!zl[1, k]) mod p ne 0]); mz := 89 - Lz;
    assert &and[zl[1, k] eq 0 : k in [1..Lz-1]];
    printf "S20|Norm(g0) lies in L_C(88*P32); pole order %o at P32 (at most 73 expected)\n", mz;
    q := QL[1][1]; L := Min([k : k in [1..NL] | (ZZ!q[1, k]) mod p ne 0]); mq := 89 - L;
    rho := q[1, L+1]*q[1, L]^-1; rz := zl[1, Lz+1]*zl[1, Lz]^-1;
    D1 := rho*(ZN!mq)^-1 - rz*(ZN!mz)^-1; D2 := rho*(ZN!mq)^-1 - r17*(ZN!17)^-1;
    assert (ZZ!D2) mod p ne 0;
    Append(~invs, <"J_Y = D(q0, z)/D(q0, f17), independent of t", D1*D2^-1>);
    LIST := GetEnv("LIST");
    if LIST ne "" then
        p1 := ZN!0; count := 0;
        for fn in Split(LIST, ",") do
            body := Read(fn);
            i0 := Position(body, "\n<");
            if i0 eq 0 then continue; end if;
            i0 +:= 1;
            j0 := #body; while body[j0] ne ">" do j0 -:= 1; end while;
            for rec in eval ("[* " cat body[i0..j0] cat " *]") do
                p1 +:= WTrace(WElt(rec[3][2])*WInv(WElt(rec[3][1]))); count +:= 1;
            end for;
        end for;
        printf "S20|p_1 from %o records; mod p = %o [%o s]\n", count, (ZZ!p1) mod p, Cputime(started);
        npts := 17*count;
        E1 := p1*(ZN!43)^-1 - npts*r17*(ZN!17)^-1;
        Append(~invs, <"P1_inv = sum over x of D(f_x, f17)/D(q0, f17), independent of t", E1*D2^-1>);
        Append(~invs, <"sum over x of D(f_x, f17) (scales with t only)", E1>);
    end if;
end if;

// 5. recognition
M := p^N; bitsM := Log(2, M);
PZp<x> := PolynomialRing(ZZ);
function PRoots(f)
    out := [];
    for rt in Roots(PolynomialRing(Fp)!f) do
        b := ZN!(ZZ!rt[1]); e := 1;
        while e lt N do b := b - Evaluate(f, b)*(Evaluate(Derivative(f), b))^-1; e *:= 2; end while;
        assert Evaluate(f, b) eq 0; Append(~out, b);
    end for;
    return out;
end function;
oct := x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2;
r8 := PRoots(oct); assert #r8 eq 8;
r3 := PRoots(x^2 + 3); assert #r3 eq 2;
w := r3[1]; b := r8[1]; s := b^4 - 4*b^2 + 2; assert s^2 eq 2;
fields := [* <"Q", [ZN!1]>, <"Q(sqrt 2)", [1, s]>, <"Q(sqrt -3)", [1, w]>, <"Q(sqrt 2, sqrt -3)", [1, s, w, s*w]>,
             <"F", [b^i : i in [0..7]]>, <"F(sqrt -3)", [b^i : i in [0..7]] cat [w*b^i : i in [0..7]]> *];
function Recognize(v, bas)
    d := #bas;
    B := [[M] cat [0 : i in [1..d]]] cat [[-ZZ!bas[i]] cat [j eq i select 1 else 0 : j in [2..d+1]] : i in [2..d]] cat [[ZZ!v] cat [0 : i in [1..d-1]] cat [1]];
    Lm := LLL(Matrix(ZZ, B));
    return Max([Ilog2(Abs(c) + 1) : c in Eltseq(Lm[1])]), Eltseq(Lm[1]);
end function;
for iv in invs do
    v := iv[2];
    printf "S20|%o: mod p^%o = %o\n", iv[1], Min(N, 4), (ZZ!v) mod p^Min(N, 4);
    for fd in fields do
        bits, vec := Recognize(v, fd[2]);
        rnd := Round(bitsM/(#fd[2] + 1));
        printf "S20|  in %o: max coefficient bits %o (random: %o)%o\n", fd[1], bits, rnd, (bits lt 0.8*rnd and vec[#vec] ne 0) select "  RECOGNIZED" else ((bits lt rnd - 40 and vec[#vec] ne 0) select "  NEAR (below random by more than 40 bits)" else "");
        if bits lt rnd - 40 and vec[#vec] ne 0 and (bits lt 400 or #fd[2] eq 1) then printf "S20|  vector (x0, a_1.., denominator): %o\n", vec; end if;
    end for;
end for;
printf "DONE|20_MODEL_INVARIANTS [%o s]\n", Cputime(started);
quit;
