// Analytic feasibility gate for recovering Oda periods from quadratic twists.
//
// Required environment:
//   HMF_ROOT=/path/to/hilbertmodularforms

SetColumns(0);
SetClassGroupBounds("GRH");

hmf_root := GetEnv("HMF_ROOT");
if hmf_root eq "" then
    error "Set HMF_ROOT to the pinned hilbertmodularforms checkout";
end if;
AttachSpec(hmf_root cat "/spec");

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
places := InfinitePlaces(F);

desired_signs :=
    [[1 : j in [1..8]]] cat
    [[j eq i select -1 else 1 : j in [1..8]] : i in [1..8]];
counts := [0 : sign in desired_signs];
minimum_conductor_norms := [0 : sign in desired_signs];

ideals := IdealsUpTo(1000, F);
for modulus in ideals do
    characters := HeckeCharacterGroup(modulus, [1..8]);
    for chi in Elements(characters) do
        if Order(chi) gt 2 or Conductor(chi) ne modulus then
            continue;
        end if;
        signs := [
            IsIdentity(Component(chi, place)) select 1 else -1
            : place in places
        ];
        index := Index(desired_signs, signs);
        if index gt 0 then
            counts[index] +:= 1;
            if minimum_conductor_norms[index] eq 0 then
                minimum_conductor_norms[index] := Norm(modulus);
            end if;
        end if;
    end for;
end for;

assert counts eq [1, 1, 1, 1, 1, 1, 1, 1, 1];
assert minimum_conductor_norms eq [1, 991, 991, 991, 991, 991, 991, 991, 991];

field_discriminant := Discriminant(OF);
assert field_discriminant eq 2^31;
gamma := &cat[[0, 1] : i in [1..8]];

function DummyCoefficient(p, degree)
    R<T> := PowerSeriesRing(Integers(), 17);
    return 1 + O(T^(degree + 1));
end function;

precisions := [1, 2, 5, 10, 20, 40, 80];
expected_untwisted := [
    4246733, 13290701, 95631975, 1056532017,
    29589598005, 1869269484654, 212410318900588
];
expected_single_negative := [
    13529146983, 38171521844, 210790200116, 1902989662695,
    43635994803076, 2351241006596040, 240341865945550376
];

for item in [
    <1, expected_untwisted>,
    <991, expected_single_negative>
] do
    conductor_norm := item[1];
    analytic_conductor := field_discriminant^2 * conductor_norm^2;
    L := LSeries(
        2, gamma, analytic_conductor, DummyCoefficient : Precision := 5
    );
    bounds := [LCfRequired(L : Precision := precision) : precision in precisions];
    assert bounds eq item[2];
    printf "RESULT|coefficient_bounds|conductor_norm|%o|%o\n",
        conductor_norm, bounds;
end for;

printf "RESULT|ideal_count_through_1000|%o\n", #ideals;
printf "RESULT|required_sign_character_counts|%o\n", counts;
printf "RESULT|required_sign_minimum_conductor_norms|%o\n",
    minimum_conductor_norms;
printf "RESULT|field_discriminant|%o\n", field_discriminant;
print "PASS|dembele_period_feasibility";
