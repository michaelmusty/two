// Independent repair of script 60's class-number fallback: order 17, not 15.
// No HMF build required. Class numbers are conditional on GRH.
SetColumns(0);
SetQuitOnError(true);
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
p2 := Factorization(2*OF)[1][1];
UF, mU := UnitGroup(OF);
gens := [ F!mU(UF.i) : i in [1..Ngens(UF)] ];
ok, pi := IsPrincipal(p2); assert ok;
Append(~gens, F!pi);
rows := [];
for pp in Factorization(31*OF) do
    k, m := ResidueClassField(pp[1]);
    Append(~rows, [ IsSquare(m(OF!gg)) select 0 else 1 : gg in gens ]);
end for;
K := Kernel(Transpose(Matrix(GF(2), rows)));
assert Dimension(K) eq 1;
bits := [ Integers()!a : a in Eltseq(Basis(K)[1]) ];
dd := &*[ gens[i]^bits[i] : i in [1..#gens] ];
printf "R62|survivor squareclass representative %o\n", dd;
M := AbsoluteField(ext<F | Polynomial([-dd, 0, 1])>);
OM := Integers(M);
h := ClassNumber(M);
C, mC := ClassGroup(M);
assert #C eq h;
r1, r2 := Signature(M);
printf "R62|signature (%o,%o); class group invariants (GRH) %o\n", r1, r2, Invariants(C);
localdata := [ <RamificationIndex(pp[1]), InertiaDegree(pp[1])> : pp in Factorization(2*OM) ];
printf "R62|survivor degree %o; discriminant %o; class number (GRH) %o; primes above 2 (e,f) %o\n", Degree(M), Discriminant(OM), h, localdata;
// Quadratic M/F has residue degree at most 2 at 2: local odd factors
// divide 2^f-1 in {1,3}; higher unit groups and real signs are 2-groups.
assert &and[ t[2] le 2 : t in localdata ];
assert &and[ (2^t[2]-1) mod 17 ne 0 : t in localdata ];
k<w> := GF(16); kt<t> := PolynomialRing(k);
for a in [w, w^3] do
    f := t^2+a*t+1;
    assert IsIrreducible(f);
    l<r> := ext<k | f>;
    assert Order(r) eq 17;
    printf "R62|trace %o: Frobenius order %o; cycle type 17\n", a, Order(r);
end for;
// Necessary cycle types for induction of a nontrivial unramified character
// of order 17 on M. Inert primes give a reflection; split primes give a
// rotation, whose order is the order of the ideal class when h = 17.
if h eq 17 then
    for ell in [31, 97, 127, 191] do
        assert &and[ InertiaDegree(pp[1]) eq 1 : pp in Factorization(ell*OF) ];
        data := [];
        for pp in Factorization(ell*OM) do
            f := InertiaDegree(pp[1]);
            ord := Order(pp[1] @@ mC);
            assert f in [1,2];
            cyc := f eq 2 select "1 2^8" else (ord eq 17 select "17" else "1^17");
            Append(~data, <f, ord, cyc>);
        end for;
        printf "R62|dihedral candidate at %o: (residue degree over Q, ideal class order, cycle type) %o\n", ell, data;
    end for;
end if;
if h mod 17 ne 0 then
    print "R62|VERDICT|dihedral excluded for both quartic trace classes (GRH): no order-17 ray class character on the sole quadratic survivor";
else
    print "R62|VERDICT|dihedral NOT excluded: surviving quadratic field has class number divisible by 17";
end if;
print "PASS|62_f16_dihedral_audit";
quit;
