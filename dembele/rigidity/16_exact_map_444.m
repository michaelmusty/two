// Equivariant recognition + exact assembly for the (4@phi, 4@phi, 4@phi^2)
// genus-0 degree-17 passport of PGammaL(2,16).  Prepend a preprocessed dump
// (u, phixnum_seq, phixden_seq, factor_seqs, factor_exps, factor_roles over
// ComplexField(4800); replace $.1 by CCi with a prepended generator line).
//
// Gauge: p0 = unique double zero -> 0, p1 = unique double point over 1 -> 1,
//        poo = unique simple pole -> oo.  Shape:
//   psi = c * y^2 * F(y)^4 * E1(y) / G(y)^4,
//   F, E1 monic deg 3, G monic deg 4, and
//   c*y^2*F^4*E1 - G^4 = c*(y-1)^2*H^4*J,  H, J monic deg 3.
SetColumns(0);

CC0 := Parent(u);
R0<x0> := PolynomialRing(CC0);
fs := [ R0!f : f in factor_seqs ];
Ffac := 0; d0fac := 0; e1fac := 0; Gfac := 0; pfac := 0;
for i in [1..#fs] do
    f := fs[i] / LeadingCoefficient(fs[i]);
    if factor_roles[i] eq 1 then
        if factor_exps[i] eq 4 then Ffac := f;
        elif factor_exps[i] eq 2 then d0fac := f;
        elif factor_exps[i] eq 1 then e1fac := f;
        end if;
    else
        if factor_exps[i] eq 4 then Gfac := f;
        elif factor_exps[i] eq 1 then pfac := f;
        end if;
    end if;
end for;
printf "factor degrees: F=%o d0=%o e1=%o G=%o p=%o\n",
    Degree(Ffac), Degree(d0fac), Degree(e1fac), Degree(Gfac), Degree(pfac);
assert Degree(Ffac) eq 3 and Degree(d0fac) eq 1 and Degree(e1fac) eq 3
   and Degree(Gfac) eq 4 and Degree(pfac) eq 1;
p0  := -Coefficient(d0fac, 0);
poo := -Coefficient(pfac, 0);
f4rts := [ r[1] : r in Roots(Ffac) ];
e1rts := [ r[1] : r in Roots(e1fac) ];
g4rts := [ r[1] : r in Roots(Gfac) ];
assert #f4rts eq 3 and #e1rts eq 3 and #g4rts eq 4;

// 1-fiber from expanded E = u*N - D
N0 := R0!phixnum_seq; D0 := R0!phixden_seq;
E0 := u*N0 - D0;
eps_cluster := RealField(10)!10^(-25);
rtsE := &cat[ [ r[1] : j in [1..r[2]] ] : r in Roots(E0) ];
groups := []; used := [ false : r in rtsE ];
for i in [1..#rtsE] do
    if used[i] then continue; end if;
    grp := [ rtsE[i] ]; used[i] := true;
    for j in [i+1..#rtsE] do
        if not used[j] and Abs(rtsE[j]-rtsE[i]) lt eps_cluster then
            Append(~grp, rtsE[j]); used[j] := true;
        end if;
    end for;
    Append(~groups, < &+grp/#grp, #grp >);
end for;
printf "fiber over 1: %o\n", Sort([ g[2] : g in groups ]);
p1 := [ g[1] : g in groups | g[2] eq 2 ][1];
h4 := [ g[1] : g in groups | g[2] eq 4 ];
j1 := [ g[1] : g in groups | g[2] eq 1 ];
assert #h4 eq 3 and #j1 eq 3;

isinf := func< z | Abs(z) gt 10^50 >;
assert not isinf(p0) and not isinf(p1) and not isinf(poo);
mo := func< z | isinf(z) select (p1-poo)/(p1-p0) else ((z-p0)*(p1-poo))/((z-poo)*(p1-p0)) >;

f4 := [ mo(z) : z in f4rts ];  e1 := [ mo(z) : z in e1rts ];
g4 := [ mo(z) : z in g4rts ];
h4m := [ mo(z) : z in h4 ];    j1m := [ mo(z) : z in j1 ];
assert forall{ z : z in f4 cat e1 cat g4 cat h4m cat j1m | not isinf(z) };

F  := &*[ x0 - z : z in f4 ];
E1 := &*[ x0 - z : z in e1 ];
G  := &*[ x0 - z : z in g4 ];
H  := &*[ x0 - z : z in h4m ];
J  := &*[ x0 - z : z in j1m ];
q := j1m[1];
c := Evaluate(G,q)^4 / (q^2 * Evaluate(F,q)^4 * Evaluate(E1,q));
lhs := c*x0^2*F^4*E1 - G^4;
rhs := c*(x0-1)^2*H^4*J;
errid := Max([ Abs(Coefficient(lhs-rhs,j)) : j in [0..17] ]);
printf "passport identity residual (full precision): %o\n", RealField(6)!errid;

// ---------- recognition ----------
precL := 1000; precV := 2000;
CCL := ComplexField(precL); CCV := ComplexField(precV);
function recogpoly(z)
    zL := CCL!z; zV := CCV!z;
    for d in [1,2,4,8] do
        pol := PowerRelation(zL, d : Al := "LLL");
        dd := Degree(pol);
        if dd lt 1 then continue; end if;
        ht := Max([ Abs(cf) : cf in Coefficients(pol) ]);
        if ht gt 10^(Round(precL/(2*(dd+1)))) then continue; end if;
        resid := Abs(Evaluate(PolynomialRing(CCV)!pol, zV));
        if resid lt ht * Max(1, Abs(zV))^dd * 10^(-1500) then
            return pol, ht;
        end if;
    end for;
    return PolynomialRing(Integers())!0, 0;
end function;

targets := [* < "c", c > *];
for j in [0..2] do Append(~targets, < Sprintf("F%o", j), Coefficient(F,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("E%o", j), Coefficient(E1,j) >); end for;
for j in [0..3] do Append(~targets, < Sprintf("G%o", j), Coefficient(G,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("H%o", j), Coefficient(H,j) >); end for;
for j in [0..2] do Append(~targets, < Sprintf("J%o", j), Coefficient(J,j) >); end for;
minpolys := [* *];
nrec := 0; refidx := 0; refdeg := 0;
for ti in [1..#targets] do
    pol, ht := recogpoly(targets[ti][2]);
    Append(~minpolys, pol);
    if Degree(pol) ge 1 then
        nrec +:= 1;
        printf "  %-3o: deg %o, height %o\n", targets[ti][1], Degree(pol), ht;
        if Degree(pol) gt refdeg then refdeg := Degree(pol); refidx := ti; end if;
    else
        printf "  %-3o: NOT RECOGNIZED, value = %o\n", targets[ti][1], ComplexField(30)!targets[ti][2];
    end if;
end for;
printf "recognized %o of %o coefficients; reference = %o (deg %o)\n",
    nrec, #targets, targets[refidx][1], refdeg;
printf "reference minpoly: %o\n", minpolys[refidx];
error if nrec ne #targets, "not all coefficients recognized; aborting";

// ---------- exact lift over the moduli field ----------
QR<zq> := PolynomialRing(Rationals());
fref := QR!minpolys[refidx];
fref /:= LeadingCoefficient(fref);
K<w> := NumberField(fref);
printf "K degree %o, disc %o\n", Degree(K), Factorization(Discriminant(Integers(K)));
refnum := targets[refidx][2];
pls := InfinitePlaces(K);
CCm := ComplexField(200);
best := <1, false>; bestd := Infinity();
for j in [1..#pls] do
    for cnj in [false, true] do
        val := CCm!Evaluate(w, pls[j] : Precision := 200);
        if cnj then val := Conjugate(val); end if;
        d := Abs(CCm!val - CCm!refnum);
        if d lt bestd then bestd := d; best := <j, cnj>; end if;
    end for;
end for;
printf "embedding match: place %o conj %o, |diff| = %o\n", best[1], best[2], RealField(6)!bestd;
v := pls[best[1]]; usecnj := best[2];
emb := func< a | usecnj select Conjugate(CCm!Evaluate(a, v : Precision := 200)) else CCm!Evaluate(a, v : Precision := 200) >;

function toK(z, K, emb, pol)
    rts := Roots(PolynomialRing(K)!pol);
    for r in rts do
        if Abs(emb(r[1]) - ComplexField(200)!z) lt 10^(-80) then
            return true, r[1];
        end if;
    end for;
    return false, K!0;
end function;

RK<y> := PolynomialRing(K);
vals := [ K!0 : t in targets ];
ok := true;
for ti in [1..#targets] do
    bl, a := toK(targets[ti][2], K, emb, minpolys[ti]);
    if not bl then printf "FAILED to lift %o\n", targets[ti][1]; ok := false; end if;
    vals[ti] := a;
end for;
error if not ok, "lift failed";
cK  := vals[1];
FK  := RK![ vals[2], vals[3], vals[4], 1 ];
EK  := RK![ vals[5], vals[6], vals[7], 1 ];
GK  := RK![ vals[8], vals[9], vals[10], vals[11], 1 ];
HK  := RK![ vals[12], vals[13], vals[14], 1 ];
JK  := RK![ vals[15], vals[16], vals[17], 1 ];

lhsK := cK*y^2*FK^4*EK - GK^4;
rhsK := cK*(y-1)^2*HK^4*JK;
if lhsK eq rhsK then
    printf "EXACT PASSPORT IDENTITY VERIFIED over K: c*y^2*F^4*E1 - G^4 = c*(y-1)^2*H^4*J\n";
else
    printf "IDENTITY FAILED\n";
end if;

// bad primes of the model
ZK := Integers(K);
items := [* Resultant(FK, GK), Resultant(EK, GK), Resultant(FK, EK),
           Discriminant(FK), Discriminant(EK), Discriminant(GK),
           Discriminant(HK), Discriminant(JK), Resultant(HK, JK),
           Resultant(FK, HK), Resultant(GK, HK), Resultant(GK, JK),
           Resultant(EK, HK), Resultant(EK, JK), Resultant(FK, JK),
           Evaluate(FK,0), Evaluate(EK,0), Evaluate(GK,0),
           Evaluate(FK,1), Evaluate(EK,1), Evaluate(GK,1), K!cK *];
badN := 1;
for it in items do
    n := Norm(it);
    if n ne 0 then
        badN *:= Numerator(Rationals()!n) * Denominator(Rationals()!n);
    end if;
end for;
printf "bad primes of the model (Q-support): %o\n",
    [ f[1] : f in Factorization(AbsoluteValue(badN)) ];

// save exact data
DF := Open("out/exact_map_444_rep1_data.m", "w");
Puts(DF, "QR<zq> := PolynomialRing(Rationals());");
Puts(DF, Sprintf("K<w> := NumberField(%m);", DefiningPolynomial(K)));
Puts(DF, "RK<y> := PolynomialRing(K);");
Puts(DF, Sprintf("cK := K!%m;", Eltseq(cK)));
Puts(DF, Sprintf("FK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(FK) ]));
Puts(DF, Sprintf("EK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(EK) ]));
Puts(DF, Sprintf("GK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(GK) ]));
Puts(DF, Sprintf("HK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(HK) ]));
Puts(DF, Sprintf("JK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(JK) ]));
Puts(DF, "// psi = cK*y^2*FK^4*EK/GK^4; identity: cK*y^2*FK^4*EK - GK^4 = cK*(y-1)^2*HK^4*JK");
delete DF;
printf "exact data saved to out/exact_map_444_rep1_data.m\n";

// monodromy certification
try
    P3 := cK*y^2*FK^4*EK - 3*GK^4;
    printf "specialization t=3: irreducible over K: %o\n", IsIrreducible(P3);
    d := LCM([ Denominator(cf) : cf in Coefficients(P3) ]);
    Kopt, iso := OptimizedRepresentation(K);
    printf "optimized model: %o\n", DefiningPolynomial(Kopt);
    P3o := PolynomialRing(Kopt)![ iso(K!(d*cf)) : cf in Coefficients(P3) ];
    t0 := Cputime();
    Ggal, _, _ := GaloisGroup(P3o);
    printf "GaloisGroup(t=3) over K: order %o (PGammaL(2,16) = 16320)  [%o s]\n", #Ggal, Cputime(t0);
    if #Ggal eq 16320 then
        printf "MONODROMY CERTIFIED: arithmetic Galois group of the t=3 fiber is PGammaL(2,16)\n";
    end if;
catch e
    printf "Galois certification errored: %o\n", e`Object;
end try;
printf "DONE\n";
quit;
