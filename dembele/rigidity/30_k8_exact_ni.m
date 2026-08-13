// Exact generating Nielsen counts for the two key k=8 all-2-power passports
// of PGammaL(2,256), by full enumeration with the smallest-centralizer element
// fixed; plus the forced 2-cyclotomic layer (epsilon-stabilizer) of each
// multiset.
SetColumns(0);
G := PGammaL(2, 256);
cls := Classes(G);
S := Socle(G);
Q, pi := quo< G | S >;
g0 := Q.1; for x in Q do if Order(x) eq 8 then g0 := x; break; end if; end for;
imgof := function(g)
    y := pi(g);
    for e in [0..7] do if y eq g0^e then return e; end if; end for;
end function;
// class indices (as in scripts 03/19): 2 = 2@4, 3 = 2@0,
// o8 by coset (1,3,5,7) = [11,10,13,12]; o16 = [22,23,20,21] wait recompute
inv0 := 0; inv4 := 0; o8 := AssociativeArray(); o16 := AssociativeArray();
for i in [1..#cls] do
    o := cls[i][1]; im := imgof(cls[i][3]);
    if o eq 2 and im eq 0 then inv0 := i; end if;
    if o eq 2 and im eq 4 then inv4 := i; end if;
    if o eq 8 and im in {1,3,5,7} then o8[im] := i; end if;
    if o eq 16 and im in {1,3,5,7} then o16[im] := i; end if;
end for;
printf "classes: inv0=%o inv4=%o 8@1=%o 16@3=%o 8@7=%o 8@1=%o\n",
    inv0, inv4, o8[1], o16[3], o8[7], o8[1];

// ---- passport (2@4, 8@1, 16@3): fix a = 16@3 rep (|C| = 16) ----
// count triples (x,y,a) with x in 2@4, y in 8@1, x*y*a = 1
// <=> y = x^-1 * a^-1 with x in class 2@4: enumerate x over the 4112-element class
procedure countpassport(G, cls, c2, c8, c16, name)
    a := cls[c16][3];
    Ca := Centralizer(G, a);
    C2 := Class(G, cls[c2][3]);
    total := 0; gen := 0;
    rep8 := cls[c8][3];
    for x in C2 do
        y := x^-1 * a^-1;
        if Order(y) ne cls[c8][1] then continue; end if;
        if not IsConjugate(G, y, rep8) then continue; end if;
        total +:= 1;
        if #sub< G | x, y > eq #G then gen +:= 1; end if;
    end for;
    printf "%o: with a fixed: total=%o gen=%o |C(a)|=%o -> Ni_total=%o Ni_gen=%o\n",
        name, total, gen, #Ca, total/#Ca, gen/#Ca;
end procedure;

countpassport(G, cls, inv4, o8[1], o16[3], "(2@4, 8@1, 16@3)");

// ---- passport (2@0, 8@7, 8@1): fix a = 8@1 rep (|C| = 48) ----
procedure countpassport2(G, cls, c2, c8a, c8b, name)
    a := cls[c8b][3];       // 8@1, smallest centralizer among the three
    Ca := Centralizer(G, a);
    C2 := Class(G, cls[c2][3]);   // inner involutions, 65535 elements
    rep8a := cls[c8a][3];
    total := 0; gen := 0;
    cnt := 0;
    for x in C2 do
        cnt +:= 1;
        if cnt mod 10000 eq 0 then printf "  ...%o of %o\n", cnt, #C2; end if;
        y := x^-1 * a^-1;
        if Order(y) ne cls[c8a][1] then continue; end if;
        if not IsConjugate(G, y, rep8a) then continue; end if;
        total +:= 1;
        if #sub< G | x, y > eq #G then gen +:= 1; end if;
    end for;
    printf "%o: with a fixed: total=%o gen=%o |C(a)|=%o -> Ni_total=%o Ni_gen=%o\n",
        name, total, gen, #Ca, total/#Ca, gen/#Ca;
end procedure;

countpassport2(G, cls, inv0, o8[7], o8[1], "(2@0, 8@7, 8@1)");

// ---- forced 2-cyclotomic layer: epsilon-stabilizers of the multisets ----
cm := ClassMap(G);
for msdata in [ <[inv4, o8[1], o16[3]], "(2@4,8@1,16@3)">,
                <[inv0, o8[7], o8[1]], "(2@0,8@7,8@1)"> ] do
    ms := msdata[1];
    stab := [];
    for e in [1,3,5,7,9,11,13,15] do   // (Z/16)^x
        img := Sort([ cm(cls[i][3]^e) : i in ms ]);
        if img eq Sort(ms) then Append(~stab, e); end if;
    end for;
    printf "multiset %o: epsilon-stabilizer mod 16 = %o\n", msdata[2], stab;
end for;
printf "DONE\n";
quit;
