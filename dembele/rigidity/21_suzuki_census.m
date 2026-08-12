// All-2-power triple census for the Suzuki groups Sz(8), Sz(32).
// Sz(q) (q = 2^(2n+1)) has 2-Sylow of exponent 4, so the SIMPLE group has
// order-4 classes; (4,4,4) is the only hyperbolic all-2-power triple shape
// ((2,4,4) is Euclidean).  For each multiset of order-4 classes: structure
// constants, generation sampling, genus of the degree-(q^2+1) cover,
// character-field conductor, and the p-power twist action at the torus primes.
SetColumns(0);

procedure census(q)
    Gm := SuzukiGroup(q);
    V := RSpace(Gm);
    G := OrbitImage(Gm, sub<V|V.1>);   // ovoid action, degree q^2+1
    n := Degree(G);
    printf "\n==== Sz(%o): order %o = %o, degree %o ====\n", q, #G, Factorization(#G), n;
    cls := Classes(G);
    cm := ClassMap(G);
    T := CharacterTable(G);
    k := #cls;
    printf "#classes %o; element orders %o\n", k, Sort(SetToSequence({ c[1] : c in cls }));
    o4 := [ i : i in [1..k] | cls[i][1] eq 4 ];
    printf "order-4 classes: %o (sizes %o)\n", o4, [ cls[i][2] : i in o4 ];
    // character field conductor of order-4 classes
    for i in o4 do
        d := 1;
        for t in [1..k] do d := LCM(d, Degree(MinimalPolynomial(T[t][i]))); end for;
        cond := 0;
        for c in [1,4,8,16] do
            C := CyclotomicField(c);
            if forall{ t : t in [1..k] | IsCoercible(C, T[t][i]) } then cond := c; break; end if;
        end for;
        printf "  class %o: ratdeg %o, cyclotomic conductor %o\n", i, d, cond;
    end for;
    // twist: which classes do p-th powers land in, p = torus primes and small primes
    torusps := [ f[1] : f in Factorization(#G) | f[1] ne 2 ];
    for i in o4 do
        printf "  twist of class %o: %o\n", i,
            [ <p, cm(cls[i][3]^p)> : p in torusps ];
    end for;
    // contribution to genus of degree-n action
    contrib := AssociativeArray();
    for i in o4 do
        cs := CycleStructure(cls[i][3]);
        contrib[i] := n - &+[ t[2] : t in cs ];
    end for;
    // triples
    for a in [1..#o4] do for b in [a..#o4] do for c in [b..#o4] do
        i := o4[a]; j := o4[b]; l := o4[c];
        s := &+[ T[t][i]*T[t][j]*T[t][l]/T[t][1] : t in [1..k] ];
        if s eq 0 then printf "multiset [%o,%o,%o]: structure constant 0\n", i, j, l; continue; end if;
        N := cls[i][2]*cls[j][2]*cls[l][2]*s/#G;
        nn := N/#G;
        twogm2 := -2*n + contrib[i] + contrib[j] + contrib[l];
        g := (Integers()!twogm2 + 2) div 2;
        // generation sampling
        x0 := cls[i][3]; y0 := cls[j][3]; z0 := cls[l][3];
        hits := 0; gens := 0; tries := 0; subs := {* *};
        while hits lt 15 and tries lt 300000 do
            tries +:= 1;
            x := x0^Random(G); y := y0^Random(G);
            w := (x*y)^-1;
            if Order(w) eq 4 and cm(w) eq l then
                hits +:= 1;
                H := sub< G | x, y >;
                Include(~subs, #H);
                if #H eq #G then gens +:= 1; end if;
            end if;
        end while;
        printf "multiset [%o,%o,%o]: n=%o genus=%o hits=%o gen=%o subs=%o\n",
            i, j, l, nn, g, hits, gens, subs;
    end for; end for; end for;
end procedure;

census(8);
census(32);
printf "DONE\n";
quit;
