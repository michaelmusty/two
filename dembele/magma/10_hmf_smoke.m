// Compatibility smoke test for the pinned edgarcosta/hilbertmodularforms package.
//
// Usage:
//   HMF_ROOT=/path/to/hilbertmodularforms magma -b dembele/magma/10_hmf_smoke.m

hmf_root := GetEnv("HMF_ROOT");
if hmf_root eq "" then
    error "Set HMF_ROOT to the pinned hilbertmodularforms checkout";
end if;
AttachSpec(hmf_root cat "/spec");

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
level := 1*OF;
weight := [2 : i in [1..Degree(F)]];

M := HilbertCuspForms(F, level, weight);
assert IsDefinite(M);
assert Dimension(M) eq 57;

quaternion_order := QuaternionOrder(M);
assert Norm(Discriminant(quaternion_order)) eq 1;

raw := InternalHMFRawDataDefinite(M : Verbose := false);
assert #raw`RightIdealClassReps eq 58;

print "RESULT|algorithm|definite";
print "RESULT|quaternion_finite_discriminant_norm|1";
print "RESULT|cusp_dimension|57";
print "RESULT|raw_right_ideal_classes|58";
print "PASS|hilbertmodularforms_smoke";
