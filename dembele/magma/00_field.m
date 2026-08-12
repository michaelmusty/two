// Exact base-field and published-prime certificate for Dembélé's construction.

Qx<x> := PolynomialRing(Rationals());
defining_polynomial := x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2;
F<beta> := NumberField(defining_polynomial);
OF := Integers(F);

assert Degree(F) eq 8;
r1, r2 := Signature(F);
assert r1 eq 8 and r2 eq 0;
assert Discriminant(OF) eq 2^31;
assert Index(OF, EquationOrder(F)) eq 1;

sigma := hom< F -> F | -beta^3 + 3*beta >;
assert (sigma^8)(beta) eq beta;
assert &and[(sigma^i)(beta) ne beta : i in [1..7]];

sqrt2 := beta^4 - 4*beta^2 + 2;
assert sqrt2^2 eq 2;
assert (sigma^2)(sqrt2) eq sqrt2;

factor_2 := Factorization(2*OF);
assert #factor_2 eq 1;
assert factor_2[1][2] eq 8;
assert Norm(factor_2[1][1]) eq 2;

factor_31 := Factorization(31*OF);
factor_97 := Factorization(97*OF);
assert #factor_31 eq 8;
assert #factor_97 eq 8;
assert &and[item[2] eq 1 and Norm(item[1]) eq 31 : item in factor_31];
assert &and[item[2] eq 1 and Norm(item[1]) eq 97 : item in factor_97];

g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
g97 := F![1, -12, -4, 19, 1, -8, 0, 1];
assert Abs(Norm(g31)) eq 31;
assert Abs(Norm(g97)) eq 97;

orbit_31_generators := [g31];
orbit_97_generators := [g97];
for i in [2..8] do
    Append(~orbit_31_generators, sigma(orbit_31_generators[#orbit_31_generators]));
    Append(~orbit_97_generators, sigma(orbit_97_generators[#orbit_97_generators]));
end for;

orbit_31 := [ideal<OF | OF!generator> : generator in orbit_31_generators];
orbit_97 := [ideal<OF | OF!generator> : generator in orbit_97_generators];
assert &and[orbit_31[i] ne orbit_31[j] : i, j in [1..8] | i lt j];
assert &and[orbit_97[i] ne orbit_97[j] : i, j in [1..8] | i lt j];

product_31 := orbit_31[1];
product_97 := orbit_97[1];
for i in [2..8] do
    product_31 *:= orbit_31[i];
    product_97 *:= orbit_97[i];
end for;
assert product_31 eq 31*OF;
assert product_97 eq 97*OF;

class_group, class_map := ClassGroup(OF);
assert #class_group eq 1;
assert NarrowClassNumber(F) eq 1;

print "RESULT|field_degree|8";
print "RESULT|signature|8,0";
print "RESULT|field_discriminant|2^31";
print "RESULT|equation_order_is_maximal|true";
print "RESULT|galois_generator_order|8";
print "RESULT|fixed_quadratic_element|beta^4-4*beta^2+2";
print "RESULT|prime_2|count=1,e=8,norm=2";
print "RESULT|prime_31|count=8,e=1,norm=31";
print "RESULT|prime_97|count=8,e=1,norm=97";
print "RESULT|class_number|1";
print "RESULT|narrow_class_number|1";
print "PASS|dembele_field_certificate";
