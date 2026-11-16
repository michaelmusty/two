// D168 step 4, package 7a: power sums of r(x) over all nonzero x in V_b and
// their recognition. r(x) = (coefficient of t^-42)/(coefficient of t^-43) of
// f_x. p_k = sum over the Frobenius-orbit representatives of Tr_{W/Z_p} r^k
// does not depend on the F_256-structure. Recognition by LLL in Q, Q(sqrt 2)
// and F = Q(zeta_32)^+ (all 8 embeddings into Q_p).
// Env: PREC, LIST (comma-separated output files of script 17), KMAX.
SetQuitOnError(true); SetColumns(0);
started := Cputime();
N := StringToInteger(GetEnv("PREC")); KMAX := StringToInteger(GetEnv("KMAX"));
p := 673; Fp := GF(p); ZN := Integers(p^N); ZZ := Integers(); LIBP := p; LIBF := Fp; LC0 := 0; LC1 := 0;
load "padic_lib.m";
K := GF(p, 17);
load "witt_lib.m";
CM := CompanionMatrix(PWZ!phiZ);
trs := [Trace(CM^i) : i in [0..WD-1]];
function WTrace(x) s := PadTo(Coefficients(PWZ!x), WD); return &+[s[i]*trs[i] : i in [1..WD]]; end function;
function WElt(seq) return WQ!(PWZ!seq); end function;
function WInv(x)
    xk := K![Fp!(ZZ!c) : c in PadTo(Coefficients(PWZ!x), WD)];
    assert xk ne 0;
    y := WElt([ZZ!c : c in Eltseq(xk^-1)]); e := 1;
    while e lt N do y := y*(2 - x*y); e *:= 2; end while;
    assert x*y eq 1;
    return y;
end function;
sums := [ZN!0 : k in [1..KMAX]]; count := 0; seen := {}; rk := {};
for fn in Split(GetEnv("LIST"), ",") do
    body := Read(fn);
    i0 := Position(body, "\n<");
    if i0 eq 0 then continue; end if;
    i0 +:= 1;
    j0 := #body; while body[j0] ne ">" do j0 -:= 1; end while;
    for rec in eval ("[* " cat body[i0..j0] cat " *]") do
        assert not <rec[1], rec[2]> in seen; Include(~seen, <rec[1], rec[2]>);
        r := WElt(rec[3][2])*WInv(WElt(rec[3][1]));
        Include(~rk, [Fp!(ZZ!c) : c in PadTo(Coefficients(PWZ!r), WD)]);
        rp := WQ!1;
        for k in [1..KMAX] do rp *:= r; sums[k] +:= WTrace(rp); end for;
        count +:= 1;
    end for;
end for;
printf "S18|records %o; distinct r(x) mod p among representatives: %o; N = %o [%o s]\n", count, #rk, N, Cputime(started);
M := p^N; bitsM := Log(2, M);
function Short(B)
    L := LLL(Matrix(ZZ, B));
    return L[1];
end function;
P8<x> := PolynomialRing(ZZ); oct := x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2;
roots8 := [];
for rt in Roots(PolynomialRing(Fp)!oct) do
    b := ZN!(ZZ!rt[1]); e := 1;
    while e lt N do b := b - Evaluate(oct, b)*(Evaluate(Derivative(oct), b))^-1; e *:= 2; end while;
    assert Evaluate(oct, b) eq 0; Append(~roots8, b);
end for;
assert #roots8 eq 8;
for k in [1..KMAX] do
    v := ZZ!sums[k];
    printf "S18|p_%o mod p = %o\n", k, v mod p;
    s1 := Short([[M, 0], [v, 1]]);
    printf "S18|p_%o in Q: num/den bits %o, %o (random: %o each)\n", k, Ilog2(Abs(s1[1]) + 1), Ilog2(Abs(s1[2]) + 1), Round(bitsM/2);
    best := 10^9;
    for b in roots8 do
        s := ZZ!(b^4 - 4*b^2 + 2);
        s2 := Short([[M, 0, 0], [-s, 1, 0], [v, 0, 1]]);
        best := Min(best, Max([Ilog2(Abs(c) + 1) : c in Eltseq(s2)]));
    end for;
    printf "S18|p_%o in Q(sqrt 2): max coefficient bits %o (random: %o)\n", k, best, Round(bitsM/3);
    res := [];
    for b in roots8 do
        B := [[M] cat [0 : i in [1..8]]] cat [[-ZZ!(b^i)] cat [j eq i select 1 else 0 : j in [1..8]] : i in [1..7]] cat [[v] cat [0 : i in [1..7]] cat [1]];
        s3 := Short(B);
        Append(~res, Max([Ilog2(Abs(c) + 1) : c in Eltseq(s3)]));
    end for;
    printf "S18|p_%o in F: max coefficient bits per embedding %o (random: %o)\n", k, res, Round(bitsM/9);
end for;
printf "DONE|18_POWER_SUMS [%o s]\n", Cputime(started);
quit;
