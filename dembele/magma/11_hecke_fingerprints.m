// Recover Dembélé's two published mod-2 characteristic polynomials from
// integral Hecke matrices on the raw level-one Brandt module.
//
// Usage:
//   HMF_ROOT=/path/to/hilbertmodularforms \
//     magma -b dembele/magma/11_hecke_fingerprints.m

hmf_root := GetEnv("HMF_ROOT");
require hmf_root ne "" :
    "Set HMF_ROOT to the pinned hilbertmodularforms checkout";
AttachSpec(hmf_root cat "/spec");

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
M := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M) eq 57;
assert NarrowClassNumber(F) eq 1;

p2 := Factorization(2*OF)[1][1];
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
assert IsPrime(p31);
assert Norm(p31) eq 31;

T2_raw := InternalHMFRawHeckeDefinite(M, p2);
T31_raw := InternalHMFRawHeckeDefinite(M, p31);
assert Nrows(T2_raw) eq 58 and Ncols(T2_raw) eq 58;
assert Nrows(T31_raw) eq 58 and Ncols(T31_raw) eq 58;
assert &and[Denominator(Rationals()!entry) eq 1 : entry in Eltseq(T2_raw)];
assert &and[Denominator(Rationals()!entry) eq 1 : entry in Eltseq(T31_raw)];

Zz<z> := PolynomialRing(Integers());
raw_cp2 := Zz!CharacteristicPolynomial(T2_raw);
raw_cp31 := Zz!CharacteristicPolynomial(T31_raw);

// At level 1 and narrow class number 1, the raw module is the cuspidal
// module plus one Eisenstein line, on which T_p acts by Norm(p)+1.
cusp_cp2, remainder_2 := Quotrem(raw_cp2, z - (Norm(p2) + 1));
cusp_cp31, remainder_31 := Quotrem(raw_cp31, z - (Norm(p31) + 1));
assert remainder_2 eq 0;
assert remainder_31 eq 0;
assert Degree(cusp_cp2) eq 57;
assert Degree(cusp_cp31) eq 57;

F2t<t> := PolynomialRing(GF(2));
cusp_cp2_mod2 := F2t!cusp_cp2;
cusp_cp31_mod2 := F2t!cusp_cp31;
expected_2 := t^41*(t^2 + t + 1)^8;
expected_31 :=
    t^41
    *(t^8 + t^4 + t^3 + t + 1)
    *(t^8 + t^6 + t^5 + t^2 + 1);

assert cusp_cp2_mod2 eq expected_2;
assert cusp_cp31_mod2 eq expected_31;

print "RESULT|raw_dimension|58";
print "RESULT|raw_hecke_matrices_integral|true";
printf "RESULT|charpoly_T_p2_mod2|%o\n", cusp_cp2_mod2;
printf "RESULT|charpoly_T_p31_1_mod2|%o\n", cusp_cp31_mod2;
print "PASS|dembele_hecke_fingerprints";
