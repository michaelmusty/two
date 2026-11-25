// D174, package 5: recognition of the symmetric functions of the Taylor ratios
// r_j(x) = c_(88+j)/c_88, j = 1..5, of f_x over the 2-torsion classes of J(C)
// lifted by script 25 (p = 31). SET selects the points: 1 (N1), 2 (N2) or 0
// (both; 510 points, Galois-stable over Q). Lattices as in script 21: joint
// reconstruction with one denominator in Q, Q(sqrt 2) and F.
// Env: PREC, LIST (comma-separated output files of script 25), KMAX, SET.
SetQuitOnError(true); SetColumns(0);
started := Cputime();
N := StringToInteger(GetEnv("PREC")); KMAX := StringToInteger(GetEnv("KMAX")); SET := StringToInteger(GetEnv("SET"));
p := 31; Fp := GF(p); ZN := Integers(p^N); ZZ := Integers(); AEXT := 17; K := GF(p, AEXT);
phiZ := PolynomialRing(ZZ)![ZZ!c : c in Coefficients(DefiningPolynomial(K))];
PWZ<yy> := PolynomialRing(ZN);
WQ<om> := quo<PWZ | PWZ!phiZ>;
function WElt(seq) return WQ!(PWZ!seq); end function;
function WSeq(x) s := Coefficients(PWZ!x); return [ZN!c : c in s] cat [ZN!0 : i in [#s+1..AEXT]]; end function;
trs := [ZN!0 : i in [1..AEXT]]; pw := WQ!1;
// traces of om^i from the regular representation
for i in [0..AEXT-1] do
    trs[i+1] := &+[WSeq(pw*om^j)[j+1] : j in [0..AEXT-1]]; pw *:= om;
end for;
function WTrace(x) s := WSeq(x); return &+[s[i]*trs[i] : i in [1..AEXT]]; end function;
function WInv(x)
    xk := K![Fp!(ZZ!c) : c in WSeq(x)];
    assert xk ne 0;
    y := WElt([ZZ!c : c in Eltseq(xk^-1)]); e := 1;
    while e lt N do y := y*(2 - x*y); e *:= 2; end while;
    assert x*y eq 1;
    return y;
end function;
NR := 5;
sums := [[ZN!0 : k in [1..KMAX]] : j in [1..NR]]; count := 0; seen := {};
for fn in Split(GetEnv("LIST"), ",") do
    body := Read(fn);
    i0 := Position(body, "\n<");
    if i0 eq 0 then continue; end if;
    i0 +:= 1;
    j0 := #body; while body[j0] ne ">" do j0 -:= 1; end while;
    for rec in eval ("[* " cat body[i0..j0] cat " *]") do
        if SET ne 0 and rec[1] ne SET then continue; end if;
        assert not <rec[1], rec[2]> in seen; Include(~seen, <rec[1], rec[2]>);
        assert #rec[3] eq NR + 1;
        ci := WInv(WElt(rec[3][1]));
        for j in [1..NR] do
            r := WElt(rec[3][j+1])*ci; rp := WQ!1;
            for k in [1..KMAX] do rp *:= r; sums[j][k] +:= WTrace(rp); end for;
        end for;
        count +:= 1;
    end for;
end for;
printf "S26|SET %o: records %o (points %o); N = %o [%o s]\n", SET, count, 17*count, N, Cputime(started);
// Newton: k e_k = sum_{i=1..k} (-1)^(i-1) e_(k-i) p_i
es := [];
for j in [1..NR] do
    e := [ZN!1];
    for k in [1..KMAX] do
        Append(~e, (ZN!k)^-1 * &+[(-1)^(i-1)*e[k-i+1]*sums[j][i] : i in [1..k]]);
    end for;
    Append(~es, [ZZ!e[k+1] : k in [1..KMAX]]);
end for;
M := p^N; bitsM := Log(2, M);
function Bits(v) return Max([Ilog2(Abs(c) + 1) : c in Eltseq(v)]); end function;
procedure Report(tag, L, rnd)
    v := L[1]; b := Bits(v);
    printf "S26|%o: shortest vector max bits %o, denominator bits %o (random: %o)%o [%o s]\n", tag, b, Ilog2(Abs(v[Ncols(L)]) + 1), Round(rnd),
        (b lt rnd - 40 and v[Ncols(L)] ne 0) select " BELOW RANDOM" else "", Cputime(started);
    if b lt rnd - 40 and v[Ncols(L)] ne 0 then printf "S26VEC|%o|%o\n", tag, Eltseq(v); end if;
end procedure;
function LatQ(vs)
    n := #vs;
    B := [[i eq j select M else 0 : j in [1..n+1]] : i in [1..n]] cat [vs cat [1]];
    return LLL(Matrix(ZZ, B));
end function;
// numerators in Z + Z*w_1 + ... + Z*w_d (ws = p-adic values of w_1..w_d), denominator in Z
function LatW(vs, ws)
    n := #vs; d := #ws; dim := n*(d+1) + 1; B := [];
    for i in [1..n] do
        row := [0 : c in [1..dim]]; row[i] := M; Append(~B, row);
        for m in [1..d] do
            row := [0 : c in [1..dim]]; row[i] := -ws[m] mod M; row[n + (m-1)*n + i] := 1; Append(~B, row);
        end for;
    end for;
    Append(~B, vs cat [0 : c in [1..n*d]] cat [1]);
    return LLL(Matrix(ZZ, B));
end function;
P8<x> := PolynomialRing(ZZ); oct := x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2;
roots8 := [];
for rt in Roots(PolynomialRing(Fp)!oct) do
    b := ZN!(ZZ!rt[1]); e := 1;
    while e lt N do b := b - Evaluate(oct, b)*(Evaluate(Derivative(oct), b))^-1; e *:= 2; end while;
    assert Evaluate(oct, b) eq 0; Append(~roots8, b);
end for;
assert #roots8 eq 8;
s2 := ZZ!(roots8[1]^4 - 4*roots8[1]^2 + 2);
e1 := [es[j][1] : j in [1..NR]];
sets := [* *];
for n in [1..NR] do Append(~sets, <Sprintf("e_1 of ratios 1..%o", n), e1[1..n]>); end for;
for K in [2..KMAX] do Append(~sets, <Sprintf("e_1..e_%o of ratio 1", K), es[1][1..K]>); end for;
for K in [2..KMAX] do Append(~sets, <Sprintf("e_1..e_%o of ratios 1..5", K), &cat[[es[j][k] : j in [1..NR]] : k in [1..K]]>); end for;
for s in sets do
    n := #s[2];
    Report("Q, " cat s[1] cat Sprintf(" (n = %o)", n), LatQ(s[2]), bitsM*n/(n+1));
end for;
for s in sets do
    n := #s[2];
    if n gt 20 then continue; end if;
    Report("Q(sqrt 2), " cat s[1] cat Sprintf(" (n = %o)", n), LatW(s[2], [s2]), bitsM*n/(2*n+1));
end for;
for ib in [1..8] do
    b := roots8[ib];
    Report(Sprintf("F embedding %o, e_1 of ratios 1..5 (n = 5)", ib), LatW(e1, [ZZ!(b^m) : m in [1..7]]), bitsM*5/41);
end for;
printf "DONE|26_C_RECOGNIZE [%o s]\n", Cputime(started);
quit;
