// D158 step 2b: a third of -Delta on the genus-40 cover mod p (port of 173).
// Env: STATE (state file from script 03), ORDER (predicted Prym order over
// F_q from the Hecke data; a search aid, verified only through the relations
// actually tested), OUT (file for the result).
SetQuitOnError(true); SetColumns(0); SetSeed(1581);
started := Cputime();
load "state_in.m";
load "state_lib.m";
load "makdisi_lib.m";
N := StringToInteger(GetEnv("ORDER"));
v := Valuation(N, 3); m := N div 3^v;
printf "S04|predicted order N = 3^%o * m, m = %o\n", v, m;
function AddC(A, B)
    return NegClass(ChordClass(A, B));
end function;
function Mul(n, D)
    assert n ge 1;
    bits := Reverse(Intseq(n, 2)); R := D;
    for i in [2..#bits] do
        R := AddC(R, R);
        if bits[i] eq 1 then R := AddC(R, D); end if;
    end for;
    return R;
end function;
assert not ZeroClass(Delta);
Dm := Mul(m, Delta);
printf "S04|m*Delta computed [%o s]\n", Cputime(started);
j := 0; T := Dm;
while not ZeroClass(T) do
    j +:= 1; assert j le v + 2;
    T := Mul(3, T);
end while;
printf "S04|order of the 3-part of Delta: 3^%o (predicted 3-valuation %o); N*Delta = 0: %o\n", j, v, j le v;
if j eq 0 then
    // 3c = -1 mod m
    c := (-Modinv(3, m)) mod m; assert (3*c + 1) mod m eq 0;
    A := Mul(c, Delta);
    res := AddC(Mul(3, A), Delta);
    ok := ZeroClass(res);
    printf "S04|3*A + Delta = 0: %o [%o s]\n", ok, Cputime(started);
    assert ok;
    assert EqualClass(FrobeniusClass(A), A);
    assert EqualClass(DeckClass(A), NegClass(A));
    PrintFile(GetEnv("OUT"), Sprintf("st_third_scalar := %o;\nst_third := %o;", c, EncM(A)) : Overwrite := true);
    print "PASS|04_THIRD";
else
    print "S04|Delta has a nontrivial 3-part; a Sylow-3 search is required. No third written.";
end if;
quit;
