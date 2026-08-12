// Assemble the exact Belyi map of cover 1 of the (2,4,8) passport over its
// degree-8 moduli field K, verify the passport identity exactly, and compute
// the bad primes of the model.  Prepend the preprocessed rep-1 dump.
SetColumns(0);

// ---------- numerical gauge (as in 12) ----------
CC0 := Parent(u);
R0<x0> := PolynomialRing(CC0);
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
p0 := -Coefficient(z0fac,0); poo := -Coefficient(pfac,0);
srts := [ r[1] : r in Roots(Sfac) ];
trts := [ r[1] : r in Roots(Tfac) ];
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
p1 := [ g[1] : g in groups | g[2] eq 2 ][1];
q4 := [ g[1] : g in groups | g[2] eq 4 ];
q1 := [ g[1] : g in groups | g[2] eq 1 ];
mo := func< z | ((z-p0)*(p1-poo))/((z-poo)*(p1-p0)) >;
s8 := [ mo(z) : z in srts ];  t2 := [ mo(z) : z in trts ];
a3 := [ mo(z) : z in q4 ];    c3 := [ mo(z) : z in q1 ];
Snum := &*[ x0 - s : s in s8 ];  Tnum := &*[ x0 - t : t in t2 ];
Anum := &*[ x0 - a : a in a3 ];  Cnum := &*[ x0 - c : c in c3 ];
qq := c3[1];
cnum := Evaluate(Tnum,qq)^8 / (qq * Evaluate(Snum,qq)^2);

// ---------- the moduli field ----------
QR<zq> := PolynomialRing(Rationals());
fT1 := zq^8 + 80*zq^7 + 9264*zq^6 + 664256/5*zq^5 + 4898528/5*zq^4
       + 6182656/5*zq^3 - 15575296/5*zq^2 - 106212352/5*zq + 30880000;
K<w> := NumberField(fT1);
printf "K disc: %o\n", Factorization(Discriminant(Integers(K)));
// pick the complex embedding matching the numerical T1 coefficient
T1num := Coefficient(Tnum, 1);
pls := InfinitePlaces(K);
CCm := ComplexField(200);
best := 0; bestd := Infinity();
for j in [1..#pls] do
    for cnj in [false, true] do
        val := Evaluate(w, pls[j] : Precision := 200);
        if cnj then val := Conjugate(val); end if;
        d := Abs(CCm!val - CCm!T1num);
        if d lt bestd then bestd := d; best := <j, cnj>; end if;
    end for;
end for;
printf "embedding match: place %o conj %o, |diff| = %o\n", best[1], best[2], RealField(6)!bestd;
v := pls[best[1]]; usecnj := best[2];
emb := func< a | usecnj select Conjugate(Evaluate(a, v : Precision := 200)) else Evaluate(a, v : Precision := 200) >;

// identify an exact K-element from its integer minpoly + numerical value
function toK(z, K, emb)
    for d in [1,2,4,8] do
        pol := PowerRelation(ComplexField(1000)!z, d : Al := "LLL");
        if Degree(pol) lt 1 then continue; end if;
        ht := Max([ Abs(cf) : cf in Coefficients(pol) ]);
        if ht gt 10^(Round(1000/(2*(Degree(pol)+1)))) then continue; end if;
        rts := Roots(PolynomialRing(K)!pol);
        for r in rts do
            if Abs(emb(r[1]) - ComplexField(200)!z) lt 10^(-80) then
                return true, r[1];
            end if;
        end for;
    end for;
    return false, K!0;
end function;

RK<y> := PolynomialRing(K);
SK := RK!0; TK := RK!0; AK := RK!0; CK := RK!0; cK := K!0;
ok := true;
polys := [* <"S", Snum, 8>, <"T", Tnum, 2>, <"A", Anum, 3>, <"C", Cnum, 3> *];
exact := [* *];
for P in polys do
    coeffs := [];
    for j in [0..P[3]-1] do
        bl, a := toK(Coefficient(P[2], j), K, emb);
        if not bl then printf "FAILED to lift %o%o\n", P[1], j; ok := false; end if;
        Append(~coeffs, a);
    end for;
    Append(~exact, RK!(coeffs cat [K!1]));
end for;
bl, cK := toK(cnum, K, emb);
if not bl then printf "FAILED to lift c\n"; ok := false; end if;
SK := exact[1]; TK := exact[2]; AK := exact[3]; CK := exact[4];

if ok then
    lhs := cK*y*SK^2 - TK^8;
    rhs := cK*(y-1)^2*AK^4*CK;
    if lhs eq rhs then
        printf "EXACT PASSPORT IDENTITY VERIFIED over K: c*y*S^2 - T^8 = c*(y-1)^2*A^4*C\n";
    else
        printf "IDENTITY FAILED\n";
        printf "max coeff of difference: %o\n", Max([ Abs(emb(cf)) : cf in Coefficients(lhs-rhs) ]);
    end if;
    printf "c = %o\n", cK;
    printf "S = %o\n", SK;
    printf "T = %o\n", TK;
    printf "A = %o\n", AK;
    printf "C = %o\n", CK;
    // bad primes of the model: where fibers collide or degenerate mod p
    ZK := Integers(K);
    bad := 1*ZK;
    items := [* Resultant(y*SK^2, TK), Resultant(SK, TK), Discriminant(SK),
               Discriminant(TK), Discriminant(AK), Discriminant(CK),
               Resultant(AK, CK), Resultant(y*SK^2, AK), Resultant(TK, AK),
               Resultant(TK, CK), Evaluate(SK, 0), Evaluate(TK, 0),
               Evaluate(SK, 1), Evaluate(TK, 1), K!cK *];
    badN := 1;
    for it in items do
        n := Norm(it);
        if n ne 0 then
            badN *:= Numerator(Rationals()!n) * Denominator(Rationals()!n);
        end if;
    end for;
    printf "bad primes of the model (Q-support): %o\n",
        [ f[1] : f in Factorization(AbsoluteValue(badN)) ];
end if;
// save exact data as loadable Magma file
if ok then
    DF := Open("out/exact_map_248_rep1_data.m", "w");
    Puts(DF, "QR<zq> := PolynomialRing(Rationals());");
    Puts(DF, Sprintf("K<w> := NumberField(%m);", DefiningPolynomial(K)));
    Puts(DF, "RK<y> := PolynomialRing(K);");
    Puts(DF, Sprintf("cK := K!%m;", Eltseq(cK)));
    Puts(DF, Sprintf("SK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(SK) ]));
    Puts(DF, Sprintf("TK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(TK) ]));
    Puts(DF, Sprintf("AK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(AK) ]));
    Puts(DF, Sprintf("CK := RK![ K!s : s in %m ];", [ Eltseq(cf) : cf in Coefficients(CK) ]));
    Puts(DF, "// psi = cK*y*SK^2/TK^8; identity: cK*y*SK^2 - TK^8 = cK*(y-1)^2*AK^4*CK");
    delete DF;
    printf "exact data saved to out/exact_map_248_rep1_data.m\n";
end if;

// monodromy certification: Galois group of a specialization over K
if ok then
    try
        P3 := cK*y*SK^2 - 3*TK^8;
        printf "specialization t=3: irreducible over K: %o\n", IsIrreducible(P3);
        d := LCM([ Denominator(cf) : cf in Coefficients(P3) ]);
        Kopt, iso := OptimizedRepresentation(K);
        printf "optimized model: %o\n", DefiningPolynomial(Kopt);
        P3o := PolynomialRing(Kopt)![ iso(K!(d*cf)) : cf in Coefficients(P3) ];
        t0 := Cputime();
        Ggal, _, _ := GaloisGroup(P3o);
        printf "GaloisGroup(t=3) over K: order %o (PGammaL(2,16) has order 16320)  [%o s]\n", #Ggal, Cputime(t0);
        if #Ggal eq 16320 then
            printf "MONODROMY CERTIFIED: arithmetic Galois group of the t=3 fiber is PGammaL(2,16)\n";
        end if;
    catch e
        printf "Galois certification errored: %o\n", e`Object;
        printf "falling back to Frobenius cycle-type sampling:\n";
        ZKo := Integers(K);
        shapes := {* *};
        p := 100;
        found := 0;
        while found lt 25 and p lt 3000 do
            p := NextPrime(p);
            if p in {2,3,5,17} then continue; end if;
            dec := Decomposition(ZKo, p);
            for pr in dec do
                if InertiaDegree(pr[1]) eq 1 and found lt 25 then
                    Fp, red := ResidueClassField(pr[1]);
                    RF := PolynomialRing(Fp);
                    ok2, Pp := IsCoercible(RF, [ red(ZKo!(LCM([Denominator(cf) : cf in Coefficients(P3)])*cf)) : cf in Coefficients(P3) ]);
                    if not ok2 then continue; end if;
                    if Degree(Pp) ne 17 or Discriminant(Pp) eq 0 then continue; end if;
                    shape := Sort([ Degree(f[1]) : f in Factorization(Pp) ]);
                    Include(~shapes, shape);
                    found +:= 1;
                end if;
            end for;
        end while;
        printf "observed Frobenius factorization shapes (%o samples):\n%o\n", found, shapes;
    end try;
end if;
printf "DONE\n";
quit;
