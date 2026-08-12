// Systematic generation check for ALL all-2-power class multisets in PGammaL(2,256)
// whose coset images sum to 0 mod 8 and generate C8, with nonzero structure constant.
SetColumns(0);
G := PGammaL(2, 256);
S := Socle(G);
Q, pi := quo< G | S >;
cls := Classes(G);
T := CharacterTable(G);
k := #cls;
n := Degree(G);
g0 := Q.1; for x in Q do if Order(x) eq 8 then g0 := x; break; end if; end for;
imgof := function(g)
    y := pi(g);
    for e in [0..7] do if y eq g0^e then return e; end if; end for;
end function;
img := [ imgof(cls[i][3]) : i in [1..k] ];
contrib := [];
for i in [1..k] do
    cs := CycleStructure(cls[i][3]);
    Append(~contrib, n - &+[ t[2] : t in cs ]);
end for;

idx2 := [ i : i in [1..k] | cls[i][1] in {2,4,8,16} ];
printf "2-power classes: %o\n", [ <i, cls[i][1], img[i]> : i in idx2 ];

for a in [1..#idx2] do
 for b in [a..#idx2] do
  for c in [b..#idx2] do
    i := idx2[a]; j := idx2[b]; l := idx2[c];
    if (img[i]+img[j]+img[l]) mod 8 ne 0 then continue; end if;
    if GCD([img[i], img[j], img[l], 8]) ne 1 then continue; end if;
    s := &+[ T[t][i]*T[t][j]*T[t][l]/T[t][1] : t in [1..k] ];
    if s eq 0 then continue; end if;
    N := cls[i][2]*cls[j][2]*cls[l][2]*s/#G;
    nn := N/#G;
    if nn eq 0 then continue; end if;
    twogm2 := -2*n + contrib[i] + contrib[j] + contrib[l];
    if twogm2 lt -2 or IsOdd(Integers()!twogm2) then continue; end if;
    g := (Integers()!twogm2 + 2) div 2;
    // generation sampling: x in class i, y in class j, need (xy)^-1 in class l
    x0 := cls[i][3]; y0 := cls[j][3]; z0 := cls[l][3];
    ol := cls[l][1];
    hits := 0; gens := 0; tries := 0; orders := {* *};
    while hits lt 15 and tries lt 400000 do
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
    printf "classes(%o,%o,%o) orders[%o,%o,%o] cosets[%o,%o,%o] n=%o genus=%o : hits=%o gen=%o sub=%o\n",
        i, j, l, cls[i][1], cls[j][1], cls[l][1], img[i], img[j], img[l],
        nn, g, hits, gens, orders;
  end for;
 end for;
end for;
