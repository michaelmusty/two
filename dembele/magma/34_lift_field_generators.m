// Explicit positive generators for the two primes above 2 and the codifferent.
// Discovery uses GRH class-group bounds; the printed ideal equalities and signs
// provide direct certificates for the resulting principality statements.

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

// Populate the maps first so that principality searches use the GRH-certified
// class and narrow-class groups.
class_group, class_map := ClassGroup(OH);
narrow_class_group, narrow_class_map := NarrowClassGroup(H);
assert Invariants(class_group) eq [2];
assert Invariants(narrow_class_group) eq [2, 2];

function IsTotallyPositiveExact(element)
    return &and[
        Evaluate(element, place) gt 0
        : place in InfinitePlaces(H)
    ];
end function;

factor_2 := Decomposition(OH, 2);
assert #factor_2 eq 2;
for index in [1..2] do
    prime := factor_2[index][1];
    success, generator := IsNarrowlyPrincipal(prime);
    assert success;
    assert ideal<OH | generator> eq prime;
    assert IsTotallyPositiveExact(generator);
    printf "GENERATOR|prime2|%o|%o\n", index, generator;
    printf "VERIFY|prime2|%o|norm|%o|positive|true\n",
        index, Abs(Norm(generator));
end for;

codifferent := Different(OH)^-1;
success, generator := IsNarrowlyPrincipal(codifferent);
assert success;
assert ideal<OH | generator> eq codifferent;
assert IsTotallyPositiveExact(generator);
printf "GENERATOR|codifferent|%o\n", generator;
printf "VERIFY|codifferent|norm|%o|positive|true\n", Abs(Norm(generator));

print "PASS|dembele_lift_field_generators";
