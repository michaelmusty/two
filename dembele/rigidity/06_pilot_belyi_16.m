// Compute the four genus-0 degree-17 Belyi maps for the all-2-power passport
// (2@0, 4@phi, 8@phi^3) of PGammaL(2,16) = SL2(F16):C4, using the Belyi package
// (Klug-Musty-Schiavone-Sijsling-Voight).  Convention: sigma[3]*sigma[2]*sigma[1] = Id,
// sigma[1] over 0, sigma[2] over 1, sigma[3] over oo.
// Cycle types: 0 -> 1^1 2^8, 1 -> 1^3 2^1 4^3, oo -> 1^1 8^2.  Run:
//   POWSER_ARNOLDI_BIN=~/Belyi/Cext/powser_arnoldi magma -b dembele/rigidity/06_pilot_belyi_16.m
SetColumns(0);
AttachSpec("/Users/musty/Belyi/Code/spec");
SetVerbose("Shimura", 1);

G := PGammaL(2, 16);
cls := Classes(G);
// class indices as in 04/05: 3 = inner involution, 5 = order 4 over phi, 11 = order 8 over phi^3
a := cls[3][3];
Ca := Centralizer(G, a);
CaElts := [ u : u in Ca ];
C5 := Class(G, cls[5][3]);
reps := [];
seen := {};
for b in C5 do
    c := (b*a)^-1;
    if Order(c) ne 8 then continue; end if;
    if #sub< G | a, b > ne #G then continue; end if;
    canon := Min([ Eltseq(b^u) : u in CaElts ]);
    if canon in seen then continue; end if;
    Include(~seen, canon);
    Append(~reps, [Sym(17)| a, b, c ]);
end for;
printf "Nielsen representatives found: %o\n", #reps;
for i in [1..#reps] do
    s := reps[i];
    assert s[3]*s[2]*s[1] eq Id(Sym(17));
    printf "rep %o: sigma0 %o | sigma1 %o | sigmaoo %o\n", i,
        CycleStructure(s[1]), CycleStructure(s[2]), CycleStructure(s[3]);
end for;

for i in [1..#reps] do
    printf "\n==================== computing Belyi map for rep %o ====================\n", i;
    t0 := Cputime();
    X, phi := BelyiMap(reps[i]);
    printf "rep %o done in %o s\n", i, Cputime(t0);
    printf "X = %o\n", X;
    K := BaseRing(X);
    printf "base field: %o\n", DefiningPolynomial(K);
    if Type(K) ne FldRat then
        ZK := Integers(K);
        printf "field disc: %o\n", Factorization(Discriminant(ZK));
    end if;
    printf "phi = %o\n", phi;
    // bad-prime first pass: norms of disc(num), disc(den), disc(num-den), res(num,den)
    FF<x> := FunctionField(K);
    f := FF!phi;
    num := Numerator(f); den := Denominator(f);
    R<T> := PolynomialRing(K);
    fn := R!num; fd := R!den; fm := fn - fd;
    bad := 1;
    for pol in [fn, fd, fm] do
        if Degree(pol) gt 1 then
            d := Discriminant(pol);
            if d ne 0 then bad *:= Norm(d); end if;
        end if;
        bad *:= Norm(LeadingCoefficient(pol));
    end for;
    r := Resultant(fn, fd);
    if r ne 0 then bad *:= Norm(r); end if;
    badZ := Numerator(Rationals()!bad) * Denominator(Rationals()!bad);
    printf "bad-prime support (first pass): %o\n", Factorization(Integers()!badZ);
end for;
printf "\nALL DONE\n";
