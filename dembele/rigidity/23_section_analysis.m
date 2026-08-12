// Pure-orbit partition analysis of the saved short braid orbits (script 22
// output out/short_orbit_tuples_16.m): decompose each pure suborbit under the
// lambda-line loops A14, A24, A34; report per-component degree, cycle types,
// genus, and especially degree-1 SECTIONS (Nielsen classes fixed by all three
// loops: monodromy-free one-parameter families).
SetColumns(0);
G := PGammaL(2, 16);
cls := Classes(G);
cm := ClassMap(G);

centElts := AssociativeArray();
for i in [1..#cls] do
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
A34 := func< t | braid(braid(t,3,false),3,false) >;
A24 := func< t | braid(braid(braid(braid(t,3,true),2,false),2,false),3,false) >;
A14 := func< t | braid(braid(braid(braid(braid(braid(t,3,true),2,true),1,false),1,false),2,false),3,false) >;

load "out/short_orbit_tuples_16.m";
printf "loaded %o short orbits\n", #shortorbits;

for oi in [1..#shortorbits] do
    ms := shortorbits[oi][1];
    plist := [ [ G!s : s in tt ] : tt in shortorbits[oi][2] ];
    d := #plist;
    printf "\n== orbit %o, multiset %o, pure degree %o ==\n", oi, ms, d;
    idx := AssociativeArray();
    for j in [1..d] do idx[canon(plist[j])] := j; end for;
    perms := [];
    for A in [ A14, A24, A34 ] do
        Append(~perms, Sym(d)![ idx[canon(A(t))] : t in plist ]);
    end for;
    P := sub< Sym(d) | perms >;
    orbs := Orbits(P);
    printf "pure-group orbit sizes: %o\n", Sort([ #o : o in orbs ]);
    for o in orbs do
        pts := [ j : j in o ];
        deg := #pts;
        if deg eq 1 then
            j := pts[1];
            printf "  SECTION (degree-1 component): tuple #%o fixed by all loops\n", j;
            t := plist[j];
            printf "    orders of entries: %o, pairwise products: %o\n",
                [ Order(x) : x in t ],
                [ Order(t[a]*t[b]) : a,b in [1..4] | a lt b ];
            printf "    <t1,t2> order: %o (index %o)\n",
                #sub<G|t[1],t[2]>, #G div #sub<G|t[1],t[2]>;
        else
            // restricted cycle types and genus
            twogm2 := -2*deg;
            for p in perms do
                pr := [ Position(pts, j^p) : j in pts ];
                pp := Sym(deg)!pr;
                twogm2 +:= deg - #CycleDecomposition(pp);
            end for;
            printf "  component of degree %o: genus (2g-2) = %o -> g = %o\n",
                deg, twogm2, (twogm2+2)/2;
        end if;
    end for;
end for;
printf "DONE\n";
quit;
