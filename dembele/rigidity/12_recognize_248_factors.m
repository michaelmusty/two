// Equivariant renormalization + recognition for the (2@0, 4@phi, 8@phi^3)
// genus-0 degree-17 passport of PGammaL(2,16), USING THE DUMPED NEWTON FACTORS
// (no multiple-root extraction, no precision loss).  Prepend a preprocessed
// dump file defining u, phixnum_seq, phixden_seq, factor_seqs, factor_exps,
// factor_roles over ComplexField(4800).
//
// Gauge (Galois-equivariant, kills all PGL2 freedom):
//   p0  = unique simple zero        -> 0
//   p1  = unique double point over 1 -> 1
//   poo = unique simple pole        -> oo
// Shape: psi = c * y * S(y)^2 / T(y)^8, S monic deg 8, T monic deg 2, and
//   c*y*S^2 - T^8 = c*(y-1)^2*A^4*C,  A, C monic deg 3.
// Recognition: LLL at 1000 digits, verified independently at 2000 digits.
SetColumns(0);

CC0 := Parent(u);
prec0 := Precision(CC0);
printf "dump precision: %o digits\n", prec0;
R0<x0> := PolynomialRing(CC0);

// --- identify factors ---------------------------------------------------
fs := [ R0!f : f in factor_seqs ];
Sfac := 0; z0fac := 0; Tfac := 0; pfac := 0;
for i in [1..#fs] do
    f := fs[i] / LeadingCoefficient(fs[i]);
    if factor_roles[i] eq 1 and factor_exps[i] eq 2 then Sfac := f;
    elif factor_roles[i] eq 1 and factor_exps[i] eq 1 then z0fac := f;
    elif factor_roles[i] ne 1 and factor_exps[i] eq 8 then Tfac := f;
    elif factor_roles[i] ne 1 and factor_exps[i] eq 1 then pfac := f;
    end if;
end for;
assert Degree(Sfac) eq 8 and Degree(z0fac) eq 1 and Degree(Tfac) eq 2 and Degree(pfac) eq 1;
p0  := -Coefficient(z0fac, 0);
poo := -Coefficient(pfac, 0);
srts := [ r[1] : r in Roots(Sfac) ];   // 8 simple roots, full accuracy
trts := [ r[1] : r in Roots(Tfac) ];   // 2 simple roots, full accuracy
assert #srts eq 8 and #trts eq 2;

// --- 1-fiber from expanded E (roots: double p1 ~prec/2, quadruple ~prec/4, simple ~full)
N := R0!phixnum_seq; D := R0!phixden_seq;
E := u*N - D;
eps_cluster := RealField(10)!10^(-25);
INF := CC0!(10^100);
function fiberPoints(pol, fulldeg, INF)
    rts := &cat[ [ r[1] : j in [1..r[2]] ] : r in Roots(pol) ];
    while #rts lt fulldeg do Append(~rts, INF); end while;
    return rts;
end function;
function clusterPoints(rts, eps)
    groups := []; used := [ false : r in rts ];
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
f1 := clusterPoints(fiberPoints(E, 17, INF), eps_cluster);
printf "fiber over 1: %o\n", Sort([ g[2] : g in f1 ]);
p1c := [ g[1] : g in f1 | g[2] eq 2 ];  assert #p1c eq 1;
p1  := p1c[1];
q4  := [ g[1] : g in f1 | g[2] eq 4 ];  assert #q4 eq 3;
q1  := [ g[1] : g in f1 | g[2] eq 1 ];  assert #q1 eq 3;

isinf := func< z | Abs(z) gt 10^50 >;
assert not isinf(p0) and not isinf(p1) and not isinf(poo);
mo := func< z | isinf(z) select (p1-poo)/(p1-p0) else ((z-p0)*(p1-poo))/((z-poo)*(p1-p0)) >;

s8 := [ mo(z) : z in srts ];
t2 := [ mo(z) : z in trts ];
a3 := [ mo(z) : z in q4 ];
c3 := [ mo(z) : z in q1 ];
assert forall{ z : z in s8 cat t2 cat a3 cat c3 | not isinf(z) };

S := &*[ x0 - s : s in s8 ];
T := &*[ x0 - t : t in t2 ];
A := &*[ x0 - a : a in a3 ];
Cs := &*[ x0 - c : c in c3 ];
q := c3[1];
c := Evaluate(T,q)^8 / (q * Evaluate(S,q)^2);
lhs := c*x0*S^2 - T^8;
rhs := c*(x0-1)^2*A^4*Cs;
errid := Max([ Abs(Coefficient(lhs-rhs,j)) : j in [0..17] ]);
printf "passport identity residual (full precision): %o\n", RealField(6)!errid;

// --- recognition: LLL at 1000 digits, verify at 2000 -------------------
precL := 1000; precV := 2000;
CCL := ComplexField(precL); CCV := ComplexField(precV);
function recog(z)
    zL := CCL!z; zV := CCV!z;
    for d in [1,2,4,8] do
        pol := PowerRelation(zL, d : Al := "LLL");
        dd := Degree(pol);
        if dd lt 1 then continue; end if;
        ht := Max([ Abs(cf) : cf in Coefficients(pol) ]);
        // noise filter: reject fits at the LLL noise floor
        if ht gt 10^(Round(precL/(2*(dd+1)))) then continue; end if;
        // independent verification at higher precision
        resid := Abs(Evaluate(PolynomialRing(CCV)!pol, zV));
        scale := ht * Max(1, Abs(zV))^dd;
        if resid lt scale * 10^(-1500) then
            return pol, ht;
        end if;
    end for;
    return PolynomialRing(Integers())!0, 0;
end function;

printf "\nrecognition (verified):\n";
targets := [* < "c", c > *];
for j in [0..7] do Append(~targets, < Sprintf("S%o", j), Coefficient(S,j) >); end for;
for j in [0..1] do Append(~targets, < Sprintf("T%o", j), Coefficient(T,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("A%o", j), Coefficient(A,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("C%o", j), Coefficient(Cs,j) >); end for;
nrec := 0;
for t in targets do
    pol, ht := recog(t[2]);
    if Degree(pol) ge 1 then
        nrec +:= 1;
        printf "  %-3o: deg %o, height %o, minpoly %o\n", t[1], Degree(pol), ht, pol;
    else
        printf "  %-3o: NOT RECOGNIZED, value = %o\n", t[1], ComplexField(30)!t[2];
    end if;
end for;
printf "recognized %o of %o coefficients (verified at %o digits)\n", nrec, #targets, precV;
printf "DONE\n";
quit;
