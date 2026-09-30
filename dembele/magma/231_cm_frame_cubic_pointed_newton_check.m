// D82: direct verification of the interpolated actual divisor's class.
SetQuitOnError(true); SetColumns(0); SetSeed(82231); started:=Cputime();
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
C:=RBase(Matrix(ZZ,newton_average_coordinates));
assert C eq RNormalize(C) and C[1]*Matrix(ZZ,pointed_jet2_coefficients) eq 0;
assert [[x mod previous_cubic_modulus:x in row]:row in BaseCoefficients(C)] eq previous_cubic_descended_divisor_coordinates;
A:=RMultiply(C,RV2);
delta:=RChord(RNegClass(RWP,RV2),RWM,RV1,RV2,RV3);
minusA:=RNegClass(A,RV2);
threeA:=RChord(RChord(A,A,RV1,RV2,RV3),minusA,RV1,RV2,RV3);
assert REqual(threeA,RNegClass(delta,RV2),RV2);
assert REqual(A,RFrob(A,makdisi_evaluation_frobenius),RV2);
assert REqual(minusA,RTau(A,makdisi_evaluation_involution),RV2);
if comparison_available then
    assert REqual(A,RMultiply(RDecode(comparison_third_coordinates),RV2),RV2);
    print "PASS|POINTED_NEWTON_AND_SCALAR_CLASSES_AGREE";
end if;
if #expected_pointed_coordinates gt 0 then
    assert BaseCoefficients(C) eq expected_pointed_coordinates;
    print "PASS|POINTED_NEWTON_COORDINATES_EQUAL_THE_EXISTING_MODEL";
end if;
printf "NEWTON_DELTA_COORDINATES|%o\n",REncode(RCoordinates(RV2,delta));
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|231_CM_FRAME_CUBIC_POINTED_NEWTON_CHECK";quit;
