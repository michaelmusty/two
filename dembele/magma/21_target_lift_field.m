// Identify the characteristic-zero Hecke field of the 16-dimensional target
// component and its primes above 2.
//
// Required environment:
//   HMF_ROOT=/path/to/hilbertmodularforms

SetColumns(0);

hmf_root := GetEnv("HMF_ROOT");
if hmf_root eq "" then
    error "Set HMF_ROOT to the pinned hilbertmodularforms checkout";
end if;
AttachSpec(hmf_root cat "/spec");

function TwoAdicLog(value)
    exponent := 0;
    while value gt 1 do
        assert IsDivisibleBy(value, 2);
        value div:= 2;
        exponent +:= 1;
    end while;
    return exponent;
end function;

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
M := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M) eq 57;

pieces := NewformDecomposition(M : Dimensions := [16]);
assert #pieces eq 1;
target := pieces[1];
assert Dimension(target) eq 16;

form := Eigenform(target);
H := BaseField(form);
assert Degree(H) eq 16;
defining_polynomial := DefiningPolynomial(H);
assert IsIrreducible(defining_polynomial);

equation_order := EquationOrder(H);
two_maximal_order := pMaximalOrder(equation_order, 2);
two_index := Index(two_maximal_order, equation_order);
factor_2 := Decomposition(two_maximal_order, 2);
residue_degrees := [
    TwoAdicLog(Norm(item[1])) : item in factor_2
];
ramification_indices := [item[2] : item in factor_2];
assert &+[
    ramification_indices[index]*residue_degrees[index]
    : index in [1..#factor_2]
] eq 16;

F2y<y> := PolynomialRing(GF(2));
polynomial_mod_2 := F2y!defining_polynomial;
factor_polynomial_mod_2 := Factorization(polynomial_mod_2);

printf "RESULT|target_dimension|16\n";
printf "RESULT|hecke_field_polynomial|%o\n", defining_polynomial;
printf "RESULT|equation_order_2_maximal_index|%o\n", two_index;
printf "RESULT|equation_order_2_index_valuation|%o\n", TwoAdicLog(two_index);
printf "RESULT|defining_polynomial_mod2|%o\n", polynomial_mod_2;
printf "RESULT|defining_polynomial_mod2_factorization|%o\n",
    factor_polynomial_mod_2;
printf "RESULT|prime_2_count|%o\n", #factor_2;
for index in [1..#factor_2] do
    printf "PRIME2|%o|e|%o|f|%o|norm|%o\n",
        index,
        ramification_indices[index],
        residue_degrees[index],
        Norm(factor_2[index][1]);
end for;
print "PASS|dembele_target_lift_field";
