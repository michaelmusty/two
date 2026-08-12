// Class, narrow-class, lambda-principality, and polarization-ideal data for
// the degree-16 Hecke field.

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

class_group, class_map := ClassGroup(OH);
narrow_class_group, narrow_class_map := NarrowClassGroup(H);
factor_2 := Decomposition(OH, 2);
assert #factor_2 eq 2;

printf "RESULT|class_group_invariants|%o\n", Invariants(class_group);
printf "RESULT|class_number|%o\n", #class_group;
printf "RESULT|narrow_class_group_invariants|%o\n",
    Invariants(narrow_class_group);
printf "RESULT|narrow_class_number|%o\n", #narrow_class_group;

for index in [1..2] do
    prime := factor_2[index][1];
    ordinary_class := prime @@ class_map;
    narrow_class := prime @@ narrow_class_map;
    printf
        "PRIME2|%o|ordinary_class|%o|narrow_class|%o|principal|%o|narrowly_principal|%o\n",
        index, ordinary_class, narrow_class,
        IsIdentity(ordinary_class), IsIdentity(narrow_class);
end for;

codifferent := Different(OH)^-1;
codifferent_class := codifferent @@ class_map;
codifferent_narrow_class := codifferent @@ narrow_class_map;
codifferent_principal := IsIdentity(codifferent_class);
codifferent_narrow := IsIdentity(codifferent_narrow_class);
printf "RESULT|codifferent_class|%o\n", codifferent_class;
printf "RESULT|codifferent_narrow_class|%o\n", codifferent_narrow_class;
printf "RESULT|codifferent_principal|%o\n", codifferent_principal;
printf "RESULT|codifferent_narrowly_principal|%o\n", codifferent_narrow;

print "PASS|dembele_lift_field_ideals";
