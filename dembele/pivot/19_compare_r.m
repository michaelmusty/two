// Compares r(x) = c(t^-42)/c(t^-43) between two output files of script 17
// (possibly at different precisions) for the records they share.
// Env: PREC (the smaller precision), FA, FB.
SetQuitOnError(true); SetColumns(0);
N := StringToInteger(GetEnv("PREC"));
p := 673; Fp := GF(p); ZN := Integers(p^N); ZZ := Integers(); LIBP := p; LIBF := Fp; LC0 := 0; LC1 := 0;
load "padic_lib.m";
K := GF(p, 17);
load "witt_lib.m";
function WElt(seq) return WQ!(PWZ![ZN!c : c in seq]); end function;
function WInv(x)
    xk := K![Fp!(ZZ!c) : c in PadTo(Coefficients(PWZ!x), WD)];
    y := WElt([ZZ!c : c in Eltseq(xk^-1)]); e := 1;
    while e lt N do y := y*(2 - x*y); e *:= 2; end while;
    assert x*y eq 1; return y;
end function;
function Recs(fn)
    body := Read(fn); i0 := Position(body, "\n<") + 1;
    j0 := #body; while body[j0] ne ">" do j0 -:= 1; end while;
    return eval ("[* " cat body[i0..j0] cat " *]");
end function;
A := Recs(GetEnv("FA")); B := Recs(GetEnv("FB"));
nc := 0;
for a in A do for b in B do
    if a[1] eq b[1] and a[2] eq b[2] then
        ra := WElt(a[3][2])*WInv(WElt(a[3][1])); rb := WElt(b[3][2])*WInv(WElt(b[3][1]));
        d := [ZZ!c : c in PadTo(Coefficients(PWZ!(ra - rb)), WD)];
        val := Min([c eq 0 select N else Valuation(c, p) : c in d]);
        printf "S19|record (%o,%o): r agrees mod p^%o (N = %o)\n", a[1], a[2], val, N; nc +:= 1;
    end if;
end for; end for;
printf "DONE|19_COMPARE %o common records\n", nc;
quit;
