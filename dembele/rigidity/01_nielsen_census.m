// Nielsen-class census for PGammaL(2,q) = SL_2(F_q) : C_m  (q = 2^m),
// following step 1 of Huang-Jackson-Lee-Poonen-Pries-Zhang (M23 paper):
// enumerate class triples, compute normalized structure constants
// n(C1,C2,C3) = |C1||C2||C3|/|G| * sum_chi chi(c1)chi(c2)chi(c3)/chi(1),
// then report candidates with small n/|G| (upper bound for |Ni|, before
// removing non-generating triples), plus the genus of the degree-(q+1)
// quotient cover and rationality data for each class.

SetColumns(0);

procedure census(q, m, topN)
    G := PGammaL(2, q);
    n := Degree(G);
    printf "\n==== PGammaL(2,%o): order %o, perm degree %o ====\n", q, #G, n;
    S := Socle(G);
    Q, pi := quo< G | S >;
    printf "outer quotient: %o\n", GroupName(Q);

    t0 := Cputime();
    cls := Classes(G);
    printf "#classes: %o  (%o s)\n", #cls, Cputime(t0);
    t0 := Cputime();
    T := CharacterTable(G);
    printf "character table done (%o s)\n", Cputime(t0);

    k := #cls;
    ords  := [ cls[i][1] : i in [1..k] ];
    sizes := [ cls[i][2] : i in [1..k] ];
    reps  := [ cls[i][3] : i in [1..k] ];

    // image of each class in the cyclic outer quotient, as residue mod m
    g0 := Q.1;
    for x in Q do if Order(x) eq #Q then g0 := x; break; end if; end for;
    img := [];
    for i in [1..k] do
        y := pi(reps[i]);
        for e in [0..#Q-1] do
            if y eq g0^e then Append(~img, e); break; end if;
        end for;
    end for;

    // ramification contribution of class i in the degree-n action: n - #cycles
    contrib := [];
    for i in [1..k] do
        cs := CycleStructure(reps[i]);
        ncyc := &+[ t[2] : t in cs ];
        Append(~contrib, n - ncyc);
    end for;

    // degree of field of character values on class i (1 = rational class)
    ratdeg := [];
    for j in [1..k] do
        d := 1;
        for t in [1..k] do
            d := LCM(d, Degree(MinimalPolynomial(T[t][j])));
        end for;
        Append(~ratdeg, d);
    end for;

    // enumerate multisets {i,j,l} of nontrivial classes whose images
    // generate the C_m quotient with product trivial
    results := [* *];
    for i in [1..k] do
        if ords[i] eq 1 then continue; end if;
        for j in [i..k] do
            if ords[j] eq 1 then continue; end if;
            for l in [j..k] do
                if ords[l] eq 1 then continue; end if;
                if (img[i] + img[j] + img[l]) mod #Q ne 0 then continue; end if;
                if GCD([img[i], img[j], img[l], #Q]) ne 1 then continue; end if;
                // structure constant
                s := &+[ T[t][i]*T[t][j]*T[t][l]/T[t][1] : t in [1..k] ];
                if s eq 0 then continue; end if;
                N := sizes[i]*sizes[j]*sizes[l]*s/#G;
                nn := N/#G;   // Nielsen-ish upper bound
                if nn eq 0 then continue; end if;
                twogm2 := -2*n + contrib[i] + contrib[j] + contrib[l];
                if twogm2 lt -2 or IsOdd(Integers()!twogm2) then continue; end if;
                g := (Integers()!twogm2 + 2) div 2;
                Append(~results, < nn, [ords[i],ords[j],ords[l]],
                                   [img[i],img[j],img[l]],
                                   g, [ratdeg[i],ratdeg[j],ratdeg[l]], [i,j,l] >);
            end for;
        end for;
    end for;

    // sort by Nielsen bound, then genus
    idx := [1..#results];
    vals := [ results[i][1] : i in idx ];
    Sort(~vals, ~perm);
    printf "total nonzero triples (C_m-generating): %o\n", #results;
    printf "\n%-12o %-16o %-10o %-7o %-12o\n",
        "n=|Sig|/|G|", "orders", "cosets", "genus", "ratdegs";
    count := 0;
    for pos in [1..#results] do
        r := results[pos^perm];
        printf "%-12o %-16o %-10o %-7o %-12o\n",
            r[1], r[2], r[3], r[4], r[5];
        count +:= 1;
        if count ge topN then break; end if;
    end for;

    // also: smallest-genus triples regardless of n
    gens_g := [ results[i][4] : i in [1..#results] ];
    if #results gt 0 then
        Sort(~gens_g, ~permg);
        printf "\nsmallest genus candidates:\n";
        for pos in [1..Min(topN, #results)] do
            r := results[pos^permg];
            printf "n=%-10o orders=%-16o cosets=%-10o genus=%-6o ratdegs=%o\n",
                r[1], r[2], r[3], r[4], r[5];
        end for;
    end if;
end procedure;

census(16, 4, 25);
census(64, 6, 25);
