// All-2-power class multisets in PGammaL(2,16) = SL_2(F_16):C_4, degree 17:
// structure constants, genus, generation, rationality — pilot for the k=8 program.
SetColumns(0);
G := PGammaL(2, 16);
S := Socle(G);
Q, pi := quo< G | S >;
cls := Classes(G);
T := CharacterTable(G);
k := #cls;
n := Degree(G);
printf "PGammaL(2,16): order %o, degree %o, #classes %o\n", #G, n, k;
g0 := Q.1; for x in Q do if Order(x) eq 4 then g0 := x; break; end if; end for;
imgof := function(g)
    y := pi(g);
    for e in [0..3] do if y eq g0^e then return e; end if; end for;
end function;
img := [ imgof(cls[i][3]) : i in [1..k] ];
contrib := [];
for i in [1..k] do
    cs := CycleStructure(cls[i][3]);
    Append(~contrib, n - &+[ t[2] : t in cs ]);
end for;
ratdeg := [];
for j in [1..k] do
    d := 1;
    for t in [1..k] do d := LCM(d, Degree(MinimalPolynomial(T[t][j]))); end for;
    Append(~ratdeg, d);
end for;
// which cyclotomic field the values live in (conductor check)
condof := function(j)
    for c in [1,4,8,16,32,3,5,12,15,20,60] do
        C := CyclotomicField(c);
        if forall{ t : t in [1..k] | IsCoercible(C, T[t][j]) } then return c; end if;
    end for;
    return 0;
end function;

idx2 := [ i : i in [1..k] | cls[i][1] in {2,4,8,16} ];
printf "2-power classes <class, order, coset, size, ratdeg, cyc-conductor>:\n";
for i in idx2 do
    printf "  <%o, %o, %o, %o, %o, %o>\n", i, cls[i][1], img[i], cls[i][2], ratdeg[i], condof(i);
end for;

for a in [1..#idx2] do
 for b in [a..#idx2] do
  for c in [b..#idx2] do
    i := idx2[a]; j := idx2[b]; l := idx2[c];
    if (img[i]+img[j]+img[l]) mod 4 ne 0 then continue; end if;
    if GCD([img[i], img[j], img[l], 4]) ne 1 then continue; end if;
    s := &+[ T[t][i]*T[t][j]*T[t][l]/T[t][1] : t in [1..k] ];
    if s eq 0 then continue; end if;
    N := cls[i][2]*cls[j][2]*cls[l][2]*s/#G;
    nn := N/#G;
    if nn eq 0 then continue; end if;
    twogm2 := -2*n + contrib[i] + contrib[j] + contrib[l];
    if twogm2 lt -2 or IsOdd(Integers()!twogm2) then continue; end if;
    g := (Integers()!twogm2 + 2) div 2;
    x0 := cls[i][3]; y0 := cls[j][3]; z0 := cls[l][3];
    ol := cls[l][1];
    hits := 0; gens := 0; tries := 0; orders := {* *};
    while hits lt 30 and tries lt 200000 do
        tries +:= 1;
        x := x0^Random(G); y := y0^Random(G);
        w := (x*y)^-1;
        if Order(w) eq ol and IsConjugate(G, w, z0) then
            hits +:= 1;
            H := sub< G | x, y >;
            Include(~orders, #H);
            if #H eq #G then gens +:= 1; end if;
        end if;
    end while;
    printf "classes(%o,%o,%o) orders[%o,%o,%o] cosets[%o,%o,%o] n=%o genus=%o ratdeg[%o,%o,%o] : hits=%o gen=%o sub=%o\n",
        i, j, l, cls[i][1], cls[j][1], cls[l][1], img[i], img[j], img[l],
        nn, g, ratdeg[i], ratdeg[j], ratdeg[l], hits, gens, orders;
  end for;
 end for;
end for;
