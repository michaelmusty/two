// Braid-orbit census for r=4 all-2-power passports of PGammaL(2,16).
// For each class multiset (orders in {2,4,8}, coset sums = 0 mod 4, images
// generating C4, hyperbolic i.e. not (2,2,2,2)): enumerate all generating
// Nielsen classes (tuples (g1,g2,g3,g4), product 1, up to simultaneous
// conjugation), then partition into orbits under the Hurwitz braid moves
// Q_i : (g_i, g_{i+1}) -> (g_i g_{i+1} g_i^-1, g_i),  i = 1,2,3.
// Search target: orbits of length 1 or 2 (M23-paper pattern).
SetColumns(0);
G := PGammaL(2, 16);
cls := Classes(G);
cm := ClassMap(G);
S := Socle(G);
Q, pi := quo< G | S >;
g0 := Q.1; for x in Q do if Order(x) eq 4 then g0 := x; break; end if; end for;
imgof := function(g)
    y := pi(g);
    for e in [0..3] do if y eq g0^e then return e; end if; end for;
end function;
k := #cls;
img := [ imgof(cls[i][3]) : i in [1..k] ];
T := CharacterTable(G);

idx2 := [ i : i in [1..k] | cls[i][1] in {2,4,8} ];
printf "2-power classes: %o\n", [ <i, cls[i][1], img[i], cls[i][2]> : i in idx2 ];

// precompute centralizer element lists for canonicalization
centElts := AssociativeArray();
for i in idx2 do
    centElts[i] := [ z : z in Centralizer(G, cls[i][3]) ];
end for;

canon := function(t)
    c1 := cm(t[1]);
    _, h := IsConjugate(G, t[1], cls[c1][3]);
    u := [ x^h : x in t ];
    best := [];
    for z in centElts[c1] do
        s := &cat[ Eltseq(x^z) : x in u ];
        if #best eq 0 or s lt best then best := s; end if;
    end for;
    return best;
end function;

braid := function(t, i, inv)
    u := t;
    if not inv then
        u[i] := t[i]*t[i+1]*t[i]^-1; u[i+1] := t[i];
    else
        u[i] := t[i+1]; u[i+1] := t[i+1]^-1*t[i]*t[i+1];
    end if;
    return u;
end function;

// multisets
mss := [];
for a in [1..#idx2] do for b in [a..#idx2] do
 for c in [b..#idx2] do for d in [c..#idx2] do
    ms := [ idx2[a], idx2[b], idx2[c], idx2[d] ];
    ords := [ cls[i][1] : i in ms ];
    if ords eq [2,2,2,2] then continue; end if;   // Euclidean
    ims := [ img[i] : i in ms ];
    if (&+ims) mod 4 ne 0 then continue; end if;
    if GCD(ims cat [4]) ne 1 then continue; end if;
    // structure-constant prefilter (any ordering has same total by braid inv)
    s := &+[ T[t][ms[1]]*T[t][ms[2]]*T[t][ms[3]]*T[t][ms[4]]/T[t][1]^2 : t in [1..k] ];
    if s eq 0 then continue; end if;
    Append(~mss, ms);
 end for; end for;
end for; end for;
printf "candidate multisets: %o\n", #mss;

for ms in mss do
    ords := [ cls[i][1] : i in ms ];
    ims := [ img[i] : i in ms ];
    // enumerate: fix g1 = rep of ms[1]; free g2 in ms[2], g3 in ms[3]; g4 derived
    g1 := cls[ms[1]][3];
    C2 := Class(G, cls[ms[2]][3]);
    C3 := Class(G, cls[ms[3]][3]);
    target4 := ms[4];
    NiSet := {};
    for g2 in C2 do
        h12 := g1*g2;
        for g3 in C3 do
            g4 := (h12*g3)^-1;
            if cm(g4) ne target4 then continue; end if;
            if #sub< G | g1, g2, g3 > ne #G then continue; end if;
            Include(~NiSet, canon([g1,g2,g3,g4]));
        end for;
    end for;
    // NiSet covers only sorted-position tuples; braid closure finds the rest.
    // BFS orbits under braid moves
    seen := {};
    orbitlens := [];
    for s0 in NiSet do
        if s0 in seen then continue; end if;
        // rebuild tuple from canonical sequence
        t0 := [ G!s0[1+17*(j-1)..17*j] : j in [1..4] ];
        frontier := { canon(t0) };
        orbit := frontier;
        reps := [ t0 ];
        while #frontier gt 0 do
            newf := {};
            newreps := [];
            for t in reps do
                for i in [1..3] do for inv in [false,true] do
                    u := braid(t, i, inv);
                    cu := canon(u);
                    if cu notin orbit then
                        Include(~orbit, cu); Include(~newf, cu);
                        Append(~newreps, u);
                    end if;
                end for; end for;
            end for;
            frontier := newf; reps := newreps;
        end while;
        seen := seen join orbit;
        Append(~orbitlens, #orbit);
    end for;
    // total distinct canonical classes encountered (all orderings)
    printf "multiset %o (orders %o cosets %o): sorted-seed Ni = %o, braid orbits (all orderings) lengths = %o%o\n",
        ms, ords, ims, #NiSet, Sort(orbitlens),
        (#orbitlens gt 0 and Min(orbitlens) le 2*24) select "  <== SHORT?" else "";
end for;
printf "DONE\n";
quit;
