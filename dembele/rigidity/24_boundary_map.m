// Boundary (cusp) identification for the short degree-2 genus-0 Hurwitz
// components: merge maps at the lambda = 0 and lambda = 1 cusps.
// Merging positions (i,4): (g1,g2,g3,g4) degenerates to a TRIPLE by
// replacing (g_i, g4) with the product (in the appropriate order); for the
// loop pairing A14 (lambda around 0) the merged triple is
// (g4*g1, g2, g3) up to convention; for A24: (g1, g4*g2, g3).
// We identify each merged triple against the exactly-known Nielsen classes
// of the target 3-point passports of PGammaL(2,16).
SetColumns(0);
G := PGammaL(2, 16);
cls := Classes(G);
cm := ClassMap(G);

centElts := AssociativeArray();
for i in [1..#cls] do
    centElts[i] := [ z : z in Centralizer(G, cls[i][3]) ];
end for;
canon3 := function(t)   // canonical form of a triple up to simultaneous conj
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
canon4 := canon3;  // same routine works for 4-tuples

braid := function(t, i, inv)
    u := t;
    if not inv then
        u[i] := t[i]*t[i+1]*t[i]^-1; u[i+1] := t[i];
    else
        u[i] := t[i+1]; u[i+1] := t[i+1]^-1*t[i]*t[i+1];
    end if;
    return u;
end function;
A14 := func< t | braid(braid(braid(braid(braid(braid(t,3,true),2,true),1,false),1,false),2,false),3,false) >;
A24 := func< t | braid(braid(braid(braid(t,3,true),2,false),2,false),3,false) >;

// ---- reference Nielsen classes of the relevant 3-point passports ----
// (2@0, 4@phi, 8@phi^3) = classes (3,5,11): the golden passport (4 classes)
// (2@phi^2, 8@phi, 8@phi) = (2,10,10): genus-1 (4 classes)
// (4@phi^2, 8@phi, 8@phi) = (7,10,10): genus-4
// (2@phi^2, 8@phi^3, 8@phi^3) = (2,11,11), (4@phi^2, 8@phi^3, 8@phi^3) = (7,11,11)
// and coset-variants; enumerate all generating Nielsen classes for each.
refsets := AssociativeArray();
procedure buildref(~refsets, c1, c2, c3)
    key := [c1,c2,c3];
    if IsDefined(refsets, key) then return; end if;
    a := cls[c1][3];
    S := {};
    for b in Class(G, cls[c2][3]) do
        w := (a*b)^-1;
        if cm(w) ne c3 then continue; end if;
        if #sub<G|a,b> ne #G then continue; end if;
        Include(~S, canon3([a,b,w]));
    end for;
    refsets[key] := SetToSequence(S);
    printf "reference passport %o: %o generating Nielsen classes\n", key, #S;
end procedure;

load "out/short_orbit_tuples_16.m";
printf "loaded %o stored orbits\n", #shortorbits;

for oi in [1..#shortorbits] do
    ms := shortorbits[oi][1];
    plist := [ [ G!s : s in tt ] : tt in shortorbits[oi][2] ];
    printf "\n== stored orbit %o, multiset %o (%o pure tuples) ==\n", oi, ms, #plist;
    // recompute pure components
    idx := AssociativeArray();
    for j in [1..#plist] do idx[canon4(plist[j])] := j; end for;
    d := #plist;
    permA14 := Sym(d)![ idx[canon4(A14(t))] : t in plist ];
    permA24 := Sym(d)![ idx[canon4(A24(t))] : t in plist ];
    P := sub< Sym(d) | permA14, permA24 >;
    comps := Orbits(P);
    for co in comps do
        pts := [ j : j in co ];
        printf "-- component {%o} --\n", pts;
        for j in pts do
            t := plist[j];
            // lambda -> 0 cusp: merge via A14 pairing: (g4*g1, g2, g3)
            m0 := [ t[4]*t[1], t[2], t[3] ];
            k0 := [ cm(x) : x in m0 ];
            // lambda -> 1 cusp: (g1, g4*g2, g3)
            m1 := [ t[1], t[4]*t[2], t[3] ];
            k1 := [ cm(x) : x in m1 ];
            printf "  tuple %o: merge0 classes %o (orders %o), merge1 classes %o (orders %o)\n",
                j, k0, [ Order(x) : x in m0 ], k1, [ Order(x) : x in m1 ];
            for pr in [ <k0, m0>, <k1, m1> ] do
                kk := pr[1]; mm := pr[2];
                if 1 in [ Order(x) : x in mm ] then
                    printf "    (degenerate merge: identity entry)\n"; continue;
                end if;
                // put smallest class first by cycling reference build
                buildref(~refsets, kk[1], kk[2], kk[3]);
                ref := refsets[[kk[1],kk[2],kk[3]]];
                cn := canon3(mm);
                pos := Position(ref, cn);
                printf "    -> passport %o Nielsen class #%o of %o%o\n",
                    kk, pos, #ref, pos eq 0 select "  (NOT generating / not found)" else "";
            end for;
        end for;
    end for;
end for;
printf "DONE\n";
quit;
