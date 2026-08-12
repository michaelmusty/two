// Recover the genus-4 17T7 reference point used by the pinned
// EichlerShimuraHMF implementation.  This is a control case for replacing
// restricted Siegel E4 by a directly evaluated Hilbert modular form.
//
// Usage:
//   ESHMF_ROOT=/path/to/EichlerShimuraHMF magma -b \
//       dembele/magma/40_genus4_reference_point.m

eshmf_root := GetEnv("ESHMF_ROOT");
if eshmf_root eq "" then
    error "Set ESHMF_ROOT to the pinned EichlerShimuraHMF checkout";
end if;
chimp_root := GetEnv("CHIMP_ROOT");
if chimp_root eq "" then
    error "Set CHIMP_ROOT to the pinned CHIMP checkout with submodules";
end if;
AttachSpec(chimp_root cat "/endomorphisms/endomorphisms/magma/spec");
Attach(chimp_root cat "/Magma/utils.m");
Attach(chimp_root cat "/Theta.magma/PythonFlint.m");
Attach(chimp_root cat "/Theta.magma/Theta.m");
Attach("dembele/magma/period_matrix_compat.m");
for source in [
    "CremonaTrick.m", "Eigenvalues.m", "HeckeCharacters.m", "Labels.m",
    "OmegaValues.m", "PeriodMatrices.m", "Schottky.m",
    "TwistedLfunction.m", "TwoTorsion.m", "Utils.m", "Wrapper.m"
] do
    Attach(eshmf_root cat "/src/" cat source);
end for;

CC<I> := ComplexFieldExtra(85);
z := [
    2.782906766939281866286997098793034902684847793476160747541940388977040015293085779903p85*I,
    0.7541581715676831945358505929000519382740764490517232237587776084375822688125537085498p85*I,
    1.427741289884804796261342526038346079673690287432208818191983875543595519551820976113p85*I,
    5.044828437439746283467218454713589608799941187512688000112646894245916708603880833717p85*I
];

Qx<x> := PolynomialRing(Rationals());
H<a> := NumberField(x^4 - 10*x^3 + 20*x^2 + 25*x - 25);
OH := Integers(H);

neighbors := IsogenousModuli(z, 2*OH);
schottky_values := [
    Abs(EvaluateSchottkyModularForm(SmallPeriodMatrix(w, 1*OH, 1*OH)))
    : w in neighbors
];
minimum, selected_index := Min(schottky_values);
selected := neighbors[selected_index];

printf "RESULT|neighbor_count|%o\n", #neighbors;
printf "RESULT|selected_index|%o\n", selected_index;
printf "RESULT|schottky_abs|%o\n", minimum;
for i in [1..#selected] do
    printf "RESULT|generator_embedding|%o|%o\n",
        i, Evaluate(H.1, InfinitePlaces(H)[i] : Precision := 85);
    printf "RESULT|z|%o|%o\n", i, selected[i];
end for;
print "PASS|genus4_reference_point";
