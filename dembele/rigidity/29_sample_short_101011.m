// Extract the twelve length-12 braid orbits of the (8@phi,8@phi,8@phi^3,8@phi^3)
// multiset [10,10,11,11] by random sampling with capped BFS (the full-closure
// approach of script 22 was killed by the 1.5M-element giant orbit), then
// boundary-map their cusps against the genus-2 (2@0,8@phi,8@phi^3) passport.
SetColumns(0);
G := PGammaL(2, 16);
cls := Classes(G);
cm := ClassMap(G);
centElts := AssociativeArray();
for i in [1..#cls] do centElts[i] := [ z : z in Centralizer(G, cls[i][3]) ]; end for;
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

CAP := 60;
g1 := cls[10][3];
C10 := Class(G, cls[10][3]);
C10s := SetToSequence(C10);
C11rep := cls[11][3];
found := [* *];
foundsigs := {};
tries := 0;
while #found lt 12 and tries lt 400000 do
    tries +:= 1;
    g2 := Random(C10s);
    g3 := C11rep^Random(G);
    g4 := (g1*g2*g3)^-1;
    if Order(g4) ne 8 or cm(g4) ne 11 then continue; end if;
    if #sub<G|g1,g2,g3> ne #G then continue; end if;
    t0 := [g1,g2,g3,g4];
    // capped BFS
    orbit := { canon(t0) };
    reps := [ t0 ]; allreps := [ t0 ];
    big := false;
    while #reps gt 0 and not big do
        newreps := [];
        for t in reps do
            for bi in [1..3] do for inv in [false,true] do
                u := braid(t, bi, inv);
                cu := canon(u);
                if cu notin orbit then
                    Include(~orbit, cu);
                    if #orbit gt CAP then big := true; break; end if;
                    Append(~newreps, u); Append(~allreps, u);
                end if;
            end for; if big then break; end if; end for;
            if big then break; end if;
        end for;
        reps := newreps;
    end while;
    if big then continue; end if;
    sig := Min([ s : s in orbit ]);
    if sig in foundsigs then continue; end if;
    Include(~foundsigs, sig);
    Append(~found, < orbit, allreps >);
    printf "short orbit %o found (length %o) after %o tries\n", #found, #orbit, tries;
end while;
printf "total distinct short orbits: %o (tries %o)\n", #found, tries;

// reference: genus-2 passport (2@0, 8@phi, 8@phi^3) = classes (3,10,11)
a := cls[3][3];
ref := [];
for b in C10 do
    w := (a*b)^-1;
    if Order(w) ne 8 or cm(w) ne 11 then continue; end if;
    if #sub<G|a,b> ne #G then continue; end if;
    cn := canon([a,b,w]);
    if Position(ref, cn) eq 0 then Append(~ref, cn); end if;
end for;
printf "genus-2 reference classes: %o\n", #ref;

for oi in [1..#found] do
    cusps := {};
    other := {};
    for t in found[oi][2] do
        m := [ t[4]*t[1], t[2], t[3] ];   // the geometrically-consistent convention
        kk := [ cm(x) : x in m ];
        if kk eq [3,10,11] then
            Include(~cusps, Position(ref, canon(m)));
        else
            Include(~other, kk);
        end if;
    end for;
    printf "orbit %o: genus-2 cusp classes %o, other merge signatures %o\n",
        oi, cusps, other;
end for;
printf "DONE\n";
quit;
