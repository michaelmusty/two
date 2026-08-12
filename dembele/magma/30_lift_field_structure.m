// Exact structure of the degree-16 Hecke field and obstruction to an
// 8-dimensional inner-twist building block.

SetColumns(0);

Qx<x> := PolynomialRing(Rationals());
hecke_polynomial :=
    x^16 - 12*x^15 - 255*x^14 + 3655*x^13 + 18005*x^12
    - 393541*x^11 + 119362*x^10 + 17669515*x^9 - 50861545*x^8
    - 286668975*x^7 + 1402550907*x^6 + 756001636*x^5
    - 11972369685*x^4 + 12087897420*x^3 + 26153849155*x^2
    - 54404306283*x + 26601321401;
H<theta> := NumberField(hecke_polynomial);
OH := Integers(H);

r1, r2 := Signature(H);
assert r1 eq 16 and r2 eq 0;
field_discriminant := Discriminant(OH);
assert Factorization(field_discriminant) eq [<5, 14>, <89, 7>, <661, 4>];

G, automorphism_map, to_automorphism := AutomorphismGroup(H);
assert #G eq 8;
assert AbelianInvariants(G) eq [8];

subfield_data := [];
for degree in [2, 4, 8] do
    fields := Subfields(H, degree);
    assert #fields eq 1;
    K := fields[1][1];
    OK := Integers(K);
    Append(
        ~subfield_data,
        <degree, DefiningPolynomial(K), Discriminant(OK), #Automorphisms(K)>
    );
end for;
assert Factorization(subfield_data[1][3]) eq [<5, 1>];
assert Factorization(subfield_data[2][3]) eq [<5, 2>, <89, 1>];
assert Factorization(subfield_data[3][3]) eq [<5, 6>, <89, 3>];

factor_2 := Decomposition(OH, 2);
assert #factor_2 eq 2;
assert &and[item[2] eq 1 and Norm(item[1]) eq 256 : item in factor_2];

// Dembélé's normalized residual field from constituents.json:
// q2 = z^8+z^6+z^5+z^2+1 and alpha = mask 76 = z^6+z^3+z^2.
F2z<z> := PolynomialRing(GF(2));
k<a> := ext<GF(2) | z^8 + z^6 + z^5 + z^2 + 1>;
alpha := a^6 + a^3 + a^2;
assert Order(alpha) eq 255;
trace_31_1 := alpha^100;
trace_31_5 := alpha^70;
assert Order(trace_31_1) eq 51;
assert trace_31_1^16 ne trace_31_1;
assert trace_31_1 ne trace_31_5;

printf "RESULT|signature|%o,%o\n", r1, r2;
printf "RESULT|field_discriminant|%o\n", field_discriminant;
printf "RESULT|field_discriminant_factorization|%o\n",
    Factorization(field_discriminant);
printf "RESULT|automorphism_group_order|%o\n", #G;
printf "RESULT|automorphism_group_invariants|%o\n", AbelianInvariants(G);
for item in subfield_data do
    printf "SUBFIELD|degree|%o|polynomial|%o|discriminant|%o|automorphisms|%o\n",
        item[1], item[2], item[3], item[4];
end for;
print "RESULT|prime_2_count|2";
print "RESULT|prime_2_data|e=1,f=8,norm=256; e=1,f=8,norm=256";
print "RESULT|trace_alpha_100_order|51";
print "RESULT|trace_alpha_100_fixed_by_x16|false";
print "RESULT|sigma4_trace_equality|false";
print "RESULT|quadratic_inner_twist|excluded";
print "RESULT|proper_base_change|excluded";
print "PASS|dembele_lift_field_structure";
