// The F16 Steinberg systems at level p2 over F = Q(zeta_32)^+ (review 2026-09-08).
//
// D36 found that the p2-new part of the level-p2 Brandt module (dim 40; five
// rational Hecke orbits of degrees 4,4,4,4,24) has cp(T_31) mod 2 =
// (t^4+t+1)^5 (t^4+t^3+t^2+t+1)^5: residue field F16, "not F256", and moved on.
// But every such residual system is a 2-dimensional mod-2 representation of
// G_F unramified outside p2 with trace field F16, so (if irreducible and not
// dihedral) it has image SL2(F16): a NONSOLVABLE extension of F, hence of Q,
// ramified only at 2 -- with a 4-dimensional carrier A_g that is Steinberg at
// p2, i.e. has multiplicative reduction at the norm-2 prime.
//
// This script certifies the image and prices the carrier:
//  (1) new subspace W_new (dim 40) and its five orbits, from the banked cp_new;
//  (2) Hecke action of the 8 primes above 31, of p97 (optional, slow), U_p2;
//  (3) joint residual eigensystems over F16 on W_new mod 2 (count of distinct
//      SL2(16)-representations up to Frobenius);
//  (4) irreducibility (automatic: ray class groups mod p2^k are 2-groups since
//      h(F)=1 and the residue field is F2) and the anti-dihedral certificate:
//      for every d in <-1, units, pi> mod squares (511 classes) exhibit a prime
//      q among the computed ones with abar_q != 0 and d a non-square mod q;
//  (5) monodromy Gram matrices (stabilizer-order pairing, D31) of the rank-4
//      isotypic sublattices: the Tate valuations v(q) = <v,v>/2 (D33);
//  (6) tau^4-invariance test (base change from Q(zeta_16)^+?);
//  (7) sweep of 2-power levels over Q(zeta_16)^+ and Q(sqrt 2) for any residual
//      system with trace field bigger than F2.
// Env: DO97 (default 1). Output markers: R60|...
SetColumns(0);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
do97 := GetEnv("DO97") ne "0";

Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2);
F2z<zz> := PolynomialRing(F2);
F16<w> := GF(16);
wt := [2 : i in [1..8]];
p2 := Factorization(2*OF)[1][1];
q31 := [ p[1] : p in Factorization(31*OF) ];
assert #q31 eq 8;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
// order the 8 primes above 31 with p31 first, then along the Galois orbit
auts := Automorphisms(F);
function autorder(a) nn := 1; y := a(b); while y ne b do y := a(y); nn +:= 1; end while; return nn; end function;
tau := [ a : a in auts | autorder(a) eq 8 ][1];
function applyaut(a, I) return ideal<OF | [ OF!a(F!g) : g in Generators(I) ]>; end function;
orbit31 := [ p31 ];
for i in [1..7] do Append(~orbit31, applyaut(tau, orbit31[#orbit31])); end for;
assert Seqset(orbit31) eq Seqset(q31);
printf "R60|8 primes above 31 ordered along the tau-orbit; tau of order %o\n", autorder(tau);

// ---------------- (7) smaller base fields ----------------------------------
procedure sweep(name, Fs, kmax, qgen)
    OFs := Integers(Fs);
    ps := Factorization(2*OFs)[1][1];
    q := ideal<OFs | OFs!qgen>;
    printf "R60|sweep %o: prime above 2 norm %o, test prime norm %o\n", name, Norm(ps), Norm(q);
    wts := [2 : i in [1..Degree(Fs)]];
    for k in [1..kmax] do
        Mk := HilbertCuspForms(Fs, ps^k, wts);
        dk := Dimension(Mk);
        if dk eq 0 then printf "R60|sweep %o: k=%o dim 0\n", name, k; continue; end if;
        Tk := Matrix(InternalHMFRawHeckeDefiniteSparse(Mk, q));
        cpk := Zz!CharacteristicPolynomial(Tk);
        fm := Factorization(F2z!cpk);
        big := [ <f[1], f[2]> : f in fm | Degree(f[1]) ge 2 ];
        printf "R60|sweep %o: k=%o cusp dim %o ; mod-2 factors of degree >= 2: %o ; degree-1 factors: %o\n", name, k, dk, big, [ <f[1], f[2]> : f in fm | Degree(f[1]) eq 1 ];
    end for;
end procedure;
try
    F4<c> := NumberField(x^4 - 4*x^2 + 2);        // Q(zeta_16)^+
    // a generator of a degree-1 prime above 17 (17 = 1 mod 16 splits completely)
    O4 := Integers(F4);
    q17 := [ p[1] : p in Factorization(17*O4) | Norm(p[1]) eq 17 ][1];
    _, g17 := IsPrincipal(q17);
    sweep("Q(zeta16)+", F4, 10, F4!g17);
catch err
    printf "R60|sweep Q(zeta16)+ failed: %o\n", err`Object;
end try;
try
    F2f<s> := NumberField(x^2 - 2);
    O2 := Integers(F2f);
    q7 := [ p[1] : p in Factorization(7*O2) | Norm(p[1]) eq 7 ][1];
    _, g7 := IsPrincipal(q7);
    sweep("Q(sqrt2)", F2f, 14, F2f!g7);
catch err
    printf "R60|sweep Q(sqrt2) failed: %o\n", err`Object;
end try;
// NOTE (2026-09-08): Magma's InternalNeighbors hits its own flagged assertion
// (ideals.m:237, "!! problem - if min_val is not 0") for the conjugate primes
// tau^i(p31), i >= 1, at level p2. They are not needed: for every residual
// system g and every i, abar_{tau^i q}(g) = abar_q(g^{tau^-i}), and g^{tau^-i}
// is again one of the level-p2 systems; so if the NEW charpoly of T_q mod 2 has
// no factor t, every system has nonzero trace at all 8 conjugates of q, and the
// anti-dihedral test only needs Legendre symbols there. Operators built: T_p31,
// U_p2, T_p97.

// ---------------- (1) level p2, T's, orbits -------------------------------
cp_bank := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
cpnew1 := cp_bank[2];
assert Degree(cpnew1) eq 40;
t0 := Cputime();
M := HilbertCuspForms(F, p2, wt);
T1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p31));
printf "R60|T_p31 built [%o s]\n", Cputime(t0);
n := Nrows(T1);
U := Matrix(InternalHMFRawHeckeDefinite(M, p2));
printf "R60|level p2 raw dim %o; U_p2 built; commutes with T_p31: %o\n", n, T1*U eq U*T1;
Ts := [ T1 ];

facs := Factorization(cpnew1);
printf "R60|new orbits (charpoly of T_p31): %o\n", [ <Degree(f[1]), f[1]> : f in facs ];
orbits := [ Kernel(Evaluate(f[1], T1)) : f in facs ];
assert [ Dimension(V) : V in orbits ] eq [ Degree(f[1]) : f in facs ];
Wnew := &+orbits;
assert Dimension(Wnew) eq 40;
printf "R60|new charpoly(T_p31) mod 2 has factor t: %o (if false, every system has abar != 0 at all 8 primes above 31)\n", Evaluate(F2z!cpnew1, 0) eq 0;

// stabilizer orders (monodromy pairing diagonal, D31)
e, ulcm, g := InternalHMFRawStabOrdersDefinite(M);
printf "R60|stab orders: distinct values %o, ulcm %o, g %o\n", Seqset(e), ulcm, g;
E := DiagonalMatrix(Rationals(), [ Rationals()!x : x in e ]);
Tq := ChangeRing(T1, Rationals());
printf "R60|T_p31 self-adjoint under stab-order diagonal: %o\n", E*Tq eq Transpose(Tq)*E;

// ---------------- (2)+(5) per orbit ---------------------------------------
for k in [1..#orbits] do
    V := orbits[k];
    BV := BasisMatrix(V);
    d := Dimension(V);
    cp31 := Zz!CharacteristicPolynomial(Solution(BV, BV*ChangeRing(T1, Rationals())));
    cpU := Zz!CharacteristicPolynomial(Solution(BV, BV*ChangeRing(U, Rationals())));
    printf "R60|orbit %o (dim %o): U_p2 charpoly %o ; charpoly(T_p31) mod 2 %o\n", k, d, Factorization(cpU), Factorization(F2z!cp31);
    if d eq 4 then
        Hg := NumberField(cp31);
        f2 := Factorization(2*Integers(Hg));
        printf "R60|orbit %o: Hecke field %o, disc %o, primes above 2 (e,f): %o\n", k, cp31, Discriminant(Integers(Hg)), [ <RamificationIndex(pp[1]), InertiaDegree(pp[1])> : pp in f2 ];
        den := LCM([ Denominator(x) : x in Eltseq(BV) ]);
        Bz := Saturation(ChangeRing(den*BV, Integers()));
        Gram := Bz * DiagonalMatrix(Integers(), e) * Transpose(Bz);
        printf "R60|orbit %o: monodromy Gram (stab-order pairing) = %o ; det %o\n", k, Eltseq(Gram), Determinant(Gram);
        L := LatticeWithGram(Gram);
        printf "R60|orbit %o: successive minima of the monodromy lattice %o ; LLL Gram %o\n", k, SuccessiveMinima(L), Eltseq(GramMatrix(LLL(L)));
    end if;
end for;

// ---------------- (3) joint residual systems over F16 (T_p31, U) ----------
Bn := BasisMatrix(Wnew);
den := LCM([ Denominator(x) : x in Eltseq(Bn) ]);
Bz := Saturation(ChangeRing(den*Bn, Integers()));
Bq := ChangeRing(Bz, Rationals());
MA := MatrixAlgebra(F16, 40);
function to16(T)
    op := Solution(Bq, Bq*ChangeRing(T, Rationals()));
    assert &and[ Denominator(x) eq 1 : x in Eltseq(op) ];
    return MA!ChangeRing(ChangeRing(op, Integers()), F16);
end function;
ops16 := [ to16(T1), to16(U) ];
function refine(spaces, op)
    newspaces := [];
    for S in spaces do
        BS := BasisMatrix(S);
        opS := MatrixAlgebra(F16, Nrows(BS))!Solution(BS, BS*op);
        cp := CharacteristicPolynomial(opS);
        for f in Factorization(cp) do
            assert Degree(f[1]) eq 1;
            a := -Coefficient(f[1], 0);
            K := Kernel((opS - a)^f[2]);
            Append(~newspaces, sub<S | [ &+[ v[i]*BS[i] : i in [1..Nrows(BS)] ] : v in Basis(K) ]>);
        end for;
    end for;
    return newspaces;
end function;
function eigtuple(S, ops)
    BS := BasisMatrix(S);
    return [ -Coefficient(Factorization(CharacteristicPolynomial(MatrixAlgebra(F16, Nrows(BS))!Solution(BS, BS*op)))[1][1], 0) : op in ops ];
end function;
function frobclasses(systems)
    frob := func< tup | [ a^2 : a in tup ] >;
    classes := []; seen := {};
    for i in [1..#systems] do
        if i in seen then continue; end if;
        cl := [ i ]; Include(~seen, i);
        t := systems[i][1];
        for j in [1..3] do
            t := frob(t);
            for m in [1..#systems] do
                if m notin seen and systems[m][1] eq t then Append(~cl, m); Include(~seen, m); end if;
            end for;
        end for;
        Append(~classes, cl);
    end for;
    return classes;
end function;
spaces := [ VectorSpace(F16, 40) ];
for op in ops16 do spaces := refine(spaces, op); end for;
systems := [ <eigtuple(S, ops16), Dimension(S)> : S in spaces ];
classes := frobclasses(systems);
printf "R60|(T_p31, U_p2) residual systems over F16: %o spaces, dims %o; distinct up to Frobenius: %o\n", #systems, [ s[2] : s in systems ], #classes;
for c in classes do
    t := systems[c[1]][1];
    printf "R60|class %o: a(p31) = %o (min poly %o), U = %o, F2-orbit size %o, total dim %o\n", Index(classes, c), t[1], MinimalPolynomial(t[1]), t[2], #c, &+[ systems[i][2] : i in c ];
end for;

// ---------------- (4) Legendre functionals ----------------------------------
UF, mU := UnitGroup(OF);
gens := [ F!mU(UF.i) : i in [1..Ngens(UF)] ];
_, pi := IsPrincipal(p2);
gens := gens cat [ F!pi ];
printf "R60|F^x/(F^x)^2 unramified outside 2: %o generators (incl. -1 and pi)\n", #gens;
function legendre_rows(primes)
    rows := [];
    for q in primes do
        _, m := ResidueClassField(q);
        Append(~rows, [ IsSquare(m(OF!gg)) select 0 else 1 : gg in gens ]);
    end for;
    return rows;   // one row per prime, entries indexed by generator
end function;
leg31 := legendre_rows(q31);
r31 := Rank(Matrix(F2, leg31));
printf "R60|Legendre functionals at the 8 primes above 31: rank %o of %o\n", r31, #gens;
function survivors(rows)
    // quadratic classes d (as bit masks over gens) with (d/q) = +1 for every row
    surv := [];
    for mask in [1..2^#gens-1] do
        bits := Intseq(mask, 2, #gens);
        if not &or[ (&+[ bits[i]*row[i] : i in [1..#gens] ] mod 2) eq 1 : row in rows ] then Append(~surv, mask); end if;
    end for;
    return surv;
end function;
surv31 := survivors(leg31);
printf "R60|quadratic classes not excluded by the primes above 31 (needs abar != 0 there, true for all systems): %o\n", #surv31;

// ---------------- (2b) T_p97 and the certificate ----------------------------
if do97 then
    t1 := Cputime();
    T97 := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p97));
    printf "R60|T_p97 built [%o s]; commutes with T_p31: %o\n", Cputime(t1), T97*T1 eq T1*T97;
    cp97new := Zz!CharacteristicPolynomial(Solution(Bq, Bq*ChangeRing(T97, Rationals())));
    printf "R60|new charpoly(T_p97) mod 2: %o\n", Factorization(F2z!cp97new);
    all97 := Evaluate(F2z!cp97new, 0) ne 0;
    printf "R60|every system has abar != 0 at all 8 primes above 97: %o\n", all97;
    op97 := to16(T97);
    spaces := refine(spaces, op97);
    ops3 := ops16 cat [ op97 ];
    systems := [ <eigtuple(S, ops3), Dimension(S)> : S in spaces ];
    classes := frobclasses(systems);
    printf "R60|(T_p31, U, T_p97) residual systems: %o spaces; distinct up to Frobenius: %o\n", #systems, #classes;
    q97 := [ p[1] : p in Factorization(97*OF) ];
    leg97 := legendre_rows(q97);
    for c in classes do
        t := systems[c[1]][1];
        rows := leg31;
        if t[3] ne 0 then rows := rows cat leg97; end if;   // a(p97) != 0 for this system => (by conjugation, if all97) all 8 primes above 97 usable
        if t[3] ne 0 and not all97 then rows := leg31 cat [ leg97[1] ]; end if;  // conservative: only p97 itself
        sv := survivors(rows);
        printf "R60|class %o: a(p31) = %o, U = %o, a(p97) = %o (min poly deg %o), total dim %o ; Legendre rank %o ; dihedral survivors %o\n",
            Index(classes, c), t[1], t[2], t[3], Degree(MinimalPolynomial(t[3])), &+[ systems[i][2] : i in c ], Rank(Matrix(F2, rows)), #sv;
        if #sv eq 0 then
            printf "R60|VERDICT|class %o|image contains SL2(F16): irreducible (ray class groups mod p2^k are 2-groups), not dihedral (every quadratic class unramified outside 2 has an inert prime with abar != 0), trace field F16 => Dickson\n", Index(classes, c);
        else
            // fallback: class numbers of the surviving quadratic extensions (GRH); dihedral needs an odd-order (15) character
            bad := [];
            for mask in sv do
                bits := Intseq(mask, 2, #gens);
                dd := &*[ gens[i]^bits[i] : i in [1..#gens] ];
                Mf := ext<F | Polynomial([-dd, 0, 1])>;
                h := ClassNumber(AbsoluteField(Mf));
                if h mod 3 eq 0 or h mod 5 eq 0 then Append(~bad, <mask, h>); end if;
            end for;
            printf "R60|class %o: survivors' class numbers checked; those divisible by 3 or 5: %o\n", Index(classes, c), bad;
            printf "R60|VERDICT|class %o|%o\n", Index(classes, c), #bad eq 0 select "image contains SL2(F16) (dihedral excluded via class numbers, GRH)" else "dihedral NOT excluded for the listed classes";
        end if;
    end for;
end if;

print "PASS|60_f16_steinberg";
quit;
