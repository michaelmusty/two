// D163 follow-up: do two points of V_b (from script 08) span it?
// V_b is a 2-dimensional vector space over F_256 = F_2[Frob]/g. The point
// TEST is in the F_256-line of BASE exactly if TEST = c(Frob) BASE for one
// of the 255 nonzero c of degree < 8; all are enumerated by a Gray code.
// Files: ymodel_in.m, makdisi_gen.m, <BASE>.pt, <TEST>.pt. Env: BASE, TEST.
SetQuitOnError(true); SetColumns(0); SetSeed(90);
started := Cputime();
load "ymodel_in.m";
p := ym_p; Fp := GF(p); AEXT := 17; K := GF(p, AEXT);
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
BASE := GetEnv("BASE"); TEST := GetEnv("TEST");
y1 := ReadPoint(BASE); y2 := ReadPoint(TEST);
assert not ZeroClass(y1) and not ZeroClass(y2);
assert not EqualClass(y1, FrobPow(y1, 1));
B := [FrobPow(y1, i) : i in [0..7]];
z := B[1]; mask := 1; found := 0; fmask := 0;
t0 := Cputime(); e := EqualClass(z, y2); teq := Cputime(t0);
if e then found +:= 1; fmask := mask; end if;
for n in [2..255] do
    // Gray code: flip the bit at the 2-adic valuation of n-1... (standard: gray(n) = n xor (n div 2))
    g1 := BitwiseXor(n, n div 2); g0 := BitwiseXor(n-1, (n-1) div 2);
    bit := Valuation(BitwiseXor(g1, g0), 2);
    z := AddC(z, B[bit+1]); mask := g1;
    if EqualClass(z, y2) then found +:= 1; fmask := mask; printf "S09|%o = c(Frob) %o with c mask %o\n", TEST, BASE, mask; end if;
    if n mod 32 eq 0 then printf "S09|%o of 255 multiples tested, one equality test %o s [%o s]\n", n, teq, Cputime(started); end if;
end for;
assert mask eq 128;
// control: the walk is consistent (last element is Frob^7 y1)
printf "S09|control last element = Frob^7 base: %o\n", EqualClass(z, B[8]);
printf "S09|base %o, test %o: multiples equal to test %o (mask %o); independent over F_256: %o [%o s]\n", BASE, TEST, found, fmask, found eq 0, Cputime(started);
print "DONE|09_SPAN_CHECK";
quit;
