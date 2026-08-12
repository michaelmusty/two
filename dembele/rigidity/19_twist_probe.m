// Frobenius-twist probe: how p-th powering acts on the all-2-power class
// multisets of PGammaL(2,16) (calibration) and PGammaL(2,256) (prediction).
// Rationale (local-mechanism.md): at k=4 the weight-deficient primes {5,17}
// are exactly the primes FIXING each passport-multiset under x -> x^p, and
// the full-weight prime 3 MOVES it (swaps the conjugate passports).
SetColumns(0);

procedure probe(q, multisets, primes)
    G := PGammaL(2, q);
    cls := Classes(G);
    cm := ClassMap(G);
    S := Socle(G);
    Q, pi := quo< G | S >;
    g0 := Q.1;
    for x in Q do if Order(x) eq #Q then g0 := x; break; end if; end for;
    imgof := function(g)
        y := pi(g);
        for e in [0..#Q-1] do if y eq g0^e then return e; end if; end for;
    end function;
    printf "\n==== PGammaL(2,%o) ====\n", q;
    for ms in multisets do
        printf "multiset %o = %o:\n", ms,
            [ <cls[i][1], imgof(cls[i][3])> : i in ms ];
        for p in primes do
            img := Sort([ cm(cls[i][3]^p) : i in ms ]);
            fixed := img eq Sort(ms);
            printf "  p = %-4o: image classes %o  -> %o\n",
                p, img, fixed select "FIXES (deficiency predicted)"
                                else "MOVES (full weight predicted)";
        end for;
    end for;
end procedure;

// k=4 calibration: class indices as in 04/05:
//   (2@0, 4@phi, 8@phi^3) = [3,5,11]; conjugate [3,6,10];
//   (4@phi, 4@phi, 4@phi^2) = [5,5,7]; genus-1 (2@phi^2,8@phi,8@phi) = [2,10,10]
probe(16, [ [3,5,11], [5,5,7], [2,10,10] ], [3,5,7,17]);

// k=8 targets: recompute class indices fresh
G := PGammaL(2, 256);
cls := Classes(G);
S := Socle(G); Q, pi := quo< G | S >;
g0 := Q.1; for x in Q do if Order(x) eq 8 then g0 := x; break; end if; end for;
imgof := function(g)
    y := pi(g);
    for e in [0..7] do if y eq g0^e then return e; end if; end for;
end function;
// find: inner involution; involution over phi^4; order-8 over each odd coset;
// order-16 over each odd coset
inv0 := 0; inv4 := 0; o8 := [0,0,0,0]; o16 := [0,0,0,0]; // indexed by (coset-1)/2+1 for cosets 1,3,5,7
for i in [1..#cls] do
    o := cls[i][1]; im := imgof(cls[i][3]);
    if o eq 2 and im eq 0 then inv0 := i; end if;
    if o eq 2 and im eq 4 then inv4 := i; end if;
    if o eq 8 and im in {1,3,5,7} then o8[(im+1) div 2] := i; end if;
    if o eq 16 and im in {1,3,5,7} then o16[(im+1) div 2] := i; end if;
end for;
printf "\nk=8 class indices: inv0=%o inv4=%o o8(c1,c3,c5,c7)=%o o16=%o\n",
    inv0, inv4, o8, o16;
// passports: (2@4, 8@1, 16@3) and (2@0, 8@7, 8@1)
probe(256, [ [inv4, o8[1], o16[2]], [inv0, o8[4], o8[1]] ], [3,5,7,17,257]);
quit;
