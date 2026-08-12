// Passport-mode computation (ExactAl := "GaloisOrbits") of the four genus-0
// degree-17 covers for the all-2-power passport (2@0, 4@phi, 8@phi^3) of
// PGammaL(2,16).  Recognition uses symmetric functions across the Galois orbit.
SetColumns(0);
AttachSpec("/Users/musty/Belyi/Code/spec");
SetVerbose("Shimura", 1);

G := PGammaL(2, 16);
cls := Classes(G);
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

t0 := Cputime();
Xs, phis := BelyiMap(reps : prec := 500, precNewton := 750);
printf "passport done in %o s\n", Cputime(t0);
printf "Xs = %o\n", Xs;
printf "phis = %o\n", phis;
for i in [1..#phis] do
    printf "---- cover %o ----\n", i;
    X := Xs[i]; phi := phis[i];
    K := BaseRing(X);
    printf "base field: %o\n", DefiningPolynomial(K);
    if Type(K) ne FldRat then
        printf "field disc: %o\n", Factorization(Discriminant(Integers(K)));
    end if;
    FF<x> := FunctionField(K);
    f := FF!phi;
    R<T> := PolynomialRing(K);
    fn := R!Numerator(f); fd := R!Denominator(f); fm := fn - fd;
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
    bq := Rationals()!bad;
    badZ := Numerator(bq) * Denominator(bq);
    printf "bad-prime support (first pass): %o\n", Factorization(Integers()!badZ);
end for;
printf "\nALL DONE\n";
