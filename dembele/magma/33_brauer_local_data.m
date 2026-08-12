// Local arithmetic relevant to the possible Schur-index-2 descent obstruction.

SetColumns(0);
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
hecke_polynomial :=
    x^16 - 12*x^15 - 255*x^14 + 3655*x^13 + 18005*x^12
    - 393541*x^11 + 119362*x^10 + 17669515*x^9 - 50861545*x^8
    - 286668975*x^7 + 1402550907*x^6 + 756001636*x^5
    - 11972369685*x^4 + 12087897420*x^3 + 26153849155*x^2
    - 54404306283*x + 26601321401;
H<theta> := NumberField(hecke_polynomial);
OH := Integers(H);

quadratic_subfields := Subfields(H, 2);
assert #quadratic_subfields eq 1;
K := quadratic_subfields[1][1];
OK := Integers(K);
assert Discriminant(OK) eq 5;

is_subfield, embedding := IsSubfield(K, H);
assert is_subfield;
Hrel := RelativeField(K, H);
OHrel := Integers(Hrel);
assert Degree(Hrel) eq 8;

printf "RESULT|base_field_polynomial|%o\n", DefiningPolynomial(K);
printf "RESULT|relative_degree|%o\n", Degree(Hrel);
printf "RESULT|relative_discriminant_norm|%o\n",
    Abs(Discriminant(OH) div Discriminant(OK)^8);

for rational_prime in [2, 5, 89, 661] do
    base_factors := Factorization(rational_prime*OK);
    for base_index in [1..#base_factors] do
        base_prime := base_factors[base_index][1];
        relative_factors := Factorization(OHrel!!base_prime);
        data := [
            <
                factor[2],
                InertiaDegree(factor[1]),
                AbsoluteNorm(factor[1])
            >
            : factor in relative_factors
        ];
        printf
            "LOCAL|rational_prime|%o|base_index|%o|base_norm|%o|relative|%o\n",
            rational_prime, base_index, Norm(base_prime), data;
    end for;
end for;

print "PASS|dembele_brauer_local_data";
