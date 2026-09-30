// An exact finite-field torsion control from the user's Q8 Belyi example.
// This tests divisor arithmetic and Frobenius on a known answer. It is
// NOT a Makdisi/p-adic lifting benchmark or a candidate for Dembélé's field.
SetColumns(0);
SetQuitOnError(true);
Q<x> := PolynomialRing(Rationals());
f := 16*x^5-x;
assert Discriminant(f) eq -2^20;
// beta=(4*x^2+1)^2/(16*x^2); beta-1=(4*x^2-1)^2/(16*x^2).
// The six hyperelliptic branch points fall in three pairs, and each has
// index 2 for beta on P1 and index 2 for the hyperelliptic map: passport
// (4,4),(4,4),(4,4), degree 8, genus 2 by Riemann-Hurwitz.
assert (4*x^2+1)^2-16*x^2 eq (4*x^2-1)^2;
assert 2*2-2 eq -2*8+3*(2*(4-1));
k0 := GF(7); R0<t> := PolynomialRing(k0);
k<i> := ext<k0 | t^2+1>;
R<u> := PolynomialRing(k);
C := HyperellipticCurve(16*u^5-u);
assert Genus(C) eq 2;
J := Jacobian(C);
roots := [k | 0,1/2,-1/2,i/2,-i/2];
assert &and[ Evaluate(16*u^5-u,r) eq 0 : r in roots ];
zero := J!0;
basis := [J![u-roots[j], R!0] : j in [1..4]];
assert &and[ 2*D eq zero : D in basis ];
pts := [];
for mask in [0..15] do
    D := zero;
    for j in [0..3] do
        if (mask div 2^j) mod 2 eq 1 then D +:= basis[j+1]; end if;
    end for;
    Append(~pts,D);
end for;
assert #Seqset(pts) eq 16;
for a in [1..5] do
    assert J![u-roots[a],R!0] in pts;
    for b in [a+1..5] do
        assert J![(u-roots[a])*(u-roots[b]),R!0] in pts;
    end for;
end for;
function frobenius(D)
    return J![R![c^7 : c in Coefficients(D[1])],R![c^7 : c in Coefficients(D[2])]];
end function;
rows := [];
for D in basis do
    pos := Index(pts,frobenius(D))-1;
    assert pos ge 0;
    Append(~rows,[(pos div 2^j) mod 2 : j in [0..3]]);
end for;
M := Matrix(GF(2),rows);
assert M ne 1 and M^2 eq 1 and Rank(M-1) eq 1;
fixed := #[D : D in pts | frobenius(D) eq D];
assert fixed eq 8;
t0 := Cputime(); cardinality := #J; elapsed := Cputime(t0);
assert cardinality mod 16 eq 0;
out := "dembele/data/computed/belyi_torsion_control.json";
txt := Sprintf("{\n  \"curve\": \"y^2=16*x^5-x\",\n  \"belyi_map\": \"(4*x^2+1)^2/(16*x^2)\",\n  \"genus\": 2,\n  \"belyi_degree\": 8,\n  \"residue_characteristic\": 7,\n  \"residue_degree\": 2,\n  \"geometric_two_torsion_count\": 16,\n  \"frobenius_fixed_count\": 8,\n  \"frobenius_matrix_mod2\": %o,\n  \"jacobian_cardinality_over_F49\": %o,\n  \"cardinality_cpu_seconds\": %o,\n  \"makdisi_backend_tested\": false,\n  \"padic_lift_tested\": false\n}\n",rows,cardinality,elapsed);
Write(out,txt : Overwrite:=true);
printf "R82|Q8 Belyi control: degree 8, genus 2, branch orders 4,4,4\n";
printf "R82|all 16 two-torsion points constructed over F49; Frob7 fixes 8; order 2; rank(Frob-1)=1\n";
printf "R82|#J(F49)=%o; cardinality CPU %o seconds\n",cardinality,elapsed;
print "PASS|82_belyi_torsion_control";
quit;
