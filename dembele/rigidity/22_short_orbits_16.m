// Re-extract the short braid orbits of the r=4 all-2-power passports of
// PGammaL(2,16) (census: script 20), storing tuples, then for each short
// orbit compute:
//   - the pure-braid (lambda-line) monodromy: actions of the loops of the
//     4th point around the three fixed points,
//       A34 = Q3^2,  A24 = Q3 Q2^2 Q3^-1,  A14 = Q3 Q2 Q1^2 Q2^-1 Q3^-1,
//     on the position-fixed sub-orbit; degree d over the lambda-line and
//     genus via Riemann-Hurwitz: 2g-2 = -2d + sum_(three loops) (d - #cycles);
//   - conjugation-invariant statistics (orders of pairwise products) to test
//     whether sibling orbits are combinatorially distinguishable.
// Only one multiset per epsilon-conjugate pair is computed.
SetColumns(0);
G := PGammaL(2, 16);
cls := Classes(G);
cm := ClassMap(G);
CAP := 60;   // store orbits of size <= CAP

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

// pure braid loop actions on ordered tuples
A34 := func< t | braid(braid(t,3,false),3,false) >;
A24 := func< t | braid(braid(braid(braid(t,3,true),2,false),2,false),3,false) >;
A14 := func< t | braid(braid(braid(braid(braid(braid(t,3,true),2,true),1,false),1,false),2,false),3,false) >;

DF := Open("out/short_orbit_tuples_16.m", "w");
Puts(DF, "// short braid orbit representatives: lists of 4 x Eltseq(17)");
Puts(DF, "shortorbits := [* *];");

for ms in [ [10,10,10,10], [5,5,11,11], [10,10,11,11] ] do
    printf "\n============ multiset %o (orders %o) ============\n",
        ms, [ cls[i][1] : i in ms ];
    g1 := cls[ms[1]][3];
    C2 := Class(G, cls[ms[2]][3]);
    C3 := Class(G, cls[ms[3]][3]);
    NiSet := {};
    tupOf := AssociativeArray();
    for g2 in C2 do
        h12 := g1*g2;
        for g3 in C3 do
            g4 := (h12*g3)^-1;
            if cm(g4) ne ms[4] then continue; end if;
            if #sub< G | g1, g2, g3 > ne #G then continue; end if;
            cs := canon([g1,g2,g3,g4]);
            if cs notin NiSet then
                Include(~NiSet, cs);
                tupOf[cs] := [g1,g2,g3,g4];
            end if;
        end for;
    end for;
    printf "sorted-seed Ni = %o\n", #NiSet;

    seen := {};
    orbnum := 0;
    for s0 in NiSet do
        if s0 in seen then continue; end if;
        t0 := tupOf[s0];
        orbit := { s0 };
        reps := [ t0 ];
        allreps := [ t0 ];
        while #reps gt 0 do
            newreps := [];
            for t in reps do
                for i in [1..3] do for inv in [false,true] do
                    u := braid(t, i, inv);
                    cu := canon(u);
                    if cu notin orbit then
                        Include(~orbit, cu);
                        Append(~newreps, u);
                        Append(~allreps, u);
                    end if;
                end for; end for;
            end for;
            reps := newreps;
        end while;
        seen := seen join orbit;
        if #orbit gt CAP then continue; end if;
        orbnum +:= 1;
        printf "\n-- SHORT ORBIT %o: length %o (all orderings) --\n", orbnum, #orbit;
        // invariant statistics: multiset of orders of pairwise products over the orbit
        invstats := {* *};
        for t in allreps do
            Include(~invstats, Sort([ Order(t[1]*t[2]), Order(t[1]*t[3]), Order(t[1]*t[4]),
                                      Order(t[2]*t[3]), Order(t[2]*t[4]), Order(t[3]*t[4]) ]));
        end for;
        printf "pairwise-product order profiles: %o\n", invstats;
        // pure-braid lambda-line monodromy: restrict to tuples with the SAME
        // ordered class assignment as t0
        assign0 := [ cm(x) : x in t0 ];
        pure := [ t : t in allreps | [ cm(x) : x in t ] eq assign0 ];
        purecs := [ canon(t) : t in pure ];
        // dedupe
        pureidx := AssociativeArray();
        plist := [];
        for j in [1..#purecs] do
            if not IsDefined(pureidx, purecs[j]) then
                pureidx[purecs[j]] := #plist + 1;
                Append(~plist, pure[j]);
            end if;
        end for;
        d := #plist;
        printf "pure (position-fixed) suborbit degree over lambda-line: %o\n", d;
        perms := [];
        for A in [ A14, A24, A34 ] do
            im := [];
            for t in plist do
                cu := canon(A(t));
                assert IsDefined(pureidx, cu);
                Append(~im, pureidx[cu]);
            end for;
            Append(~perms, Sym(d)!im);
        end for;
        printf "loop around 0 (A14): %o\n", CycleStructure(perms[1]);
        printf "loop around 1 (A24): %o\n", CycleStructure(perms[2]);
        printf "loop around oo(A34): %o\n", CycleStructure(perms[3]);
        prodcheck := perms[1]*perms[2]*perms[3];
        printf "product of loops trivial: %o (else acts as: %o)\n",
            IsIdentity(prodcheck), CycleStructure(prodcheck);
        twogm2 := -2*d + &+[ d - #CycleDecomposition(p) : p in perms ];
        printf "component genus (if loops multiply to 1): (2g-2) = %o -> g = %o\n",
            twogm2, (twogm2 + 2) / 2;
        printf "transitive on pure suborbit: %o\n",
            IsTransitive(sub< Sym(d) | perms >);
        // save
        Puts(DF, Sprintf("Append(~shortorbits, <%m, %m>);", ms,
            [ [ Eltseq(x) : x in t ] : t in plist ]));
    end for;
end for;
delete DF;
printf "\nDONE\n";
quit;
