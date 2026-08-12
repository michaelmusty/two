// Equivariant renormalization + recognition for the (2@0, 4@phi, 8@phi^3)
// genus-0 degree-17 passport of PGammaL(2,16).  Prepend a dump file defining
// u, phixnum_seq, phixden_seq (from 10_dump_numerics_248.m), e.g.
//   cat out/dump_248_rep1.m 11_recognize_248_body.m > /tmp/rec1.m && magma -b /tmp/rec1.m
//
// Lesson from the M23 team (Zhang, how-we-found-m23): triangle-group
// coordinates are NOT Galois-equivariant and coefficient heights explode;
// coordinates pinned by the Belyi map itself are equivariant and heights
// collapse.  Our passport has canonical points in all three fibers:
//   p0  = the unique unramified point over 0   (cycle type 1 2^8)
//   p1  = the unique 2-ramified point over 1   (cycle type 1^3 2 4^3)
//   poo = the unique simple pole               (cycle type 1 8^2)
// Sending (p0,p1,poo) -> (0,1,oo) kills all PGL_2 freedom equivariantly.
SetColumns(0);

CC0 := Parent(u);
prec := Min(Precision(CC0), 1200);   // cap: dumps carry escalated Newton precision
CC := ComplexField(prec);
u := CC!u;
printf "working precision: %o digits (dump had %o)\n", prec, Precision(CC0);
R<x> := PolynomialRing(CC);
N := R![ CC!z : z in phixnum_seq ];
D := R![ CC!z : z in phixden_seq ];
printf "deg num = %o, deg den = %o\n", Degree(N), Degree(D);

DEG := 17;
eps_cluster := RealField(10)!10^(-25);  // multiplicity-m roots split at ~eps^(1/m); true points are O(1) apart
INF := CC!(10^100);  // sentinel for the point at infinity

// roots of a polynomial as a multiset of CC points, plus infinity to fill degree
function fiberPoints(pol, fulldeg)
    rts := &cat[ [ r[1] : j in [1..r[2]] ] : r in Roots(pol) ];
    while #rts lt fulldeg do Append(~rts, INF); end while;
    return rts;
end function;

// cluster points into groups within eps; returns list of <representative, multiplicity>
function clusterPoints(rts, eps)
    groups := [];
    used := [ false : r in rts ];
    for i in [1..#rts] do
        if used[i] then continue; end if;
        grp := [ rts[i] ]; used[i] := true;
        for j in [i+1..#rts] do
            if not used[j] and Abs(rts[j] - rts[i]) lt eps then
                Append(~grp, rts[j]); used[j] := true;
            end if;
        end for;
        Append(~groups, < &+grp/#grp, #grp >);
    end for;
    return groups;
end function;

E := u*N - D;
f0 := clusterPoints(fiberPoints(N, DEG), eps_cluster);
foo := clusterPoints(fiberPoints(D, DEG), eps_cluster);
f1 := clusterPoints(fiberPoints(E, DEG), eps_cluster);
printf "fiber over 0:  %o\n", Sort([ g[2] : g in f0 ]);
printf "fiber over 1:  %o\n", Sort([ g[2] : g in f1 ]);
printf "fiber over oo: %o\n", Sort([ g[2] : g in foo ]);

// canonical points
p0c  := [ g[1] : g in f0  | g[2] eq 1 ];
p1c  := [ g[1] : g in f1  | g[2] eq 2 ];
pooc := [ g[1] : g in foo | g[2] eq 1 ];
assert #p0c eq 1 and #p1c eq 1 and #pooc eq 1;
p0 := p0c[1]; p1 := p1c[1]; poo := pooc[1];
printf "canonical points located (p0 at inf: %o, p1 at inf: %o, poo at inf: %o)\n",
    Abs(p0) gt 10^50, Abs(p1) gt 10^50, Abs(poo) gt 10^50;

isinf := func< z | Abs(z) gt 10^50 >;
// Moebius sending (p0, p1, poo) -> (0, 1, oo)
function moebius(z, p0, p1, poo)
    if isinf(z) then
        if isinf(poo) then return INF; end if;
        if isinf(p0) then return Parent(p1)!0; end if;
        if isinf(p1) then return Parent(p0)!1; end if;
        return (p1-poo)/(p1-p0);
    end if;
    if isinf(p0)  then return (p1-poo)/(z-poo); end if;
    if isinf(p1)  then return (z-p0)/(z-poo); end if;
    if isinf(poo) then return (z-p0)/(p1-p0); end if;
    return ((z-p0)*(p1-poo))/((z-poo)*(p1-p0));
end function;

// transformed fiber data
s8  := [ moebius(g[1],p0,p1,poo) : g in f0  | g[2] eq 2 ];   // 8 double zeros
t2  := [ moebius(g[1],p0,p1,poo) : g in foo | g[2] eq 8 ];   // 2 octuple poles
q4  := [ moebius(g[1],p0,p1,poo) : g in f1  | g[2] eq 4 ];   // 3 quadruple points over 1
q1  := [ moebius(g[1],p0,p1,poo) : g in f1  | g[2] eq 1 ];   // 3 simple points over 1
assert #s8 eq 8 and #t2 eq 2 and #q4 eq 3 and #q1 eq 3;
assert forall{ z : z in s8 cat t2 cat q4 cat q1 | not isinf(z) };

S := &*[ x - s : s in s8 ];    // monic deg 8
T := &*[ x - t : t in t2 ];    // monic deg 2
A := &*[ x - q : q in q4 ];    // monic deg 3
Cs := &*[ x - q : q in q1 ];   // monic deg 3
// constant c from psi = 1 on the simple 1-fiber point q1[1]:
q := q1[1];
c := Evaluate(T,q)^8 / (q * Evaluate(S,q)^2);

// numerical consistency of the passport identity
lhs := c*x*S^2 - T^8;
rhs := c*(x-1)^2*A^4*Cs;
errid := Max([ Abs(Coefficient(lhs-rhs,j)) : j in [0..DEG] ]);
printf "numerical passport identity residual: %o\n", RealField(6)!errid;

// recognize a complex number: try degrees 1,2,4,8; return minpoly or 0
function recog(z, prec)
    for d in [1,2,4,8] do
        pol := PowerRelation(z, d : Al := "LLL");
        if Degree(pol) ge 1 and Degree(pol) le d then
            // verify residual
            resid := Abs(Evaluate(pol, z)) / Max(1, Abs(LeadingCoefficient(pol)));
            ht := Max([ Abs(cf) : cf in Coefficients(pol) ]);
            if resid lt 10^(-Round(prec/3)) * ht then
                return pol, ht;
            end if;
        end if;
    end for;
    return PolynomialRing(Integers())!0, 0;
end function;

printf "\nrecognition of equivariant coefficients:\n";
targets := [* < "c", c > *];
for j in [0..7] do Append(~targets, < Sprintf("S%o", j), Coefficient(S,j) >); end for;
for j in [0..1] do Append(~targets, < Sprintf("T%o", j), Coefficient(T,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("A%o", j), Coefficient(A,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("C%o", j), Coefficient(Cs,j) >); end for;
nrec := 0;
for t in targets do
    pol, ht := recog(t[2], prec);
    if Degree(pol) ge 1 then
        nrec +:= 1;
        printf "  %-3o: deg %o, height %o, minpoly %o\n", t[1], Degree(pol), ht, pol;
    else
        printf "  %-3o: NOT RECOGNIZED, value = %o\n", t[1], ComplexField(30)!t[2];
    end if;
end for;
printf "recognized %o of %o coefficients\n", nrec, #targets;
printf "DONE\n";
quit;
