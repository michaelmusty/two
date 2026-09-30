// D85 redirected loads; original SHA256 b227210f49a3b36aa3a2676cb5fcceed2f7fcedce163261fa864176474971a1c
// D83: split script 231's independent relation and symmetry checks.
SetQuitOnError(true); SetColumns(0); SetSeed(83264); started:=Cputime();
load "dembele/magma/d85_128_199_cm_frame_cubic_precision_model.m";
C:=RBase(Matrix(ZZ,newton_average_coordinates));
assert C eq RNormalize(C) and C[1]*Matrix(ZZ,pointed_jet2_coefficients) eq 0;
assert [[x mod previous_cubic_modulus:x in row]:row in BaseCoefficients(C)] eq previous_cubic_descended_divisor_coordinates;
A:=RMultiply(C,RV2);
minusA:=RNegClass(A,RV2);
if class_check_mode eq "relation" then
    delta:=RChord(RNegClass(RWP,RV2),RWM,RV1,RV2,RV3);
    threeA:=RChord(RChord(A,A,RV1,RV2,RV3),minusA,RV1,RV2,RV3);
    assert REqual(threeA,RNegClass(delta,RV2),RV2);
    printf "NEWTON_DELTA_COORDINATES|%o\n",REncode(RCoordinates(RV2,delta));
    print "PASS|264_CLASS_TRIPLING_RELATION";
else
    assert class_check_mode eq "symmetries";
    assert REqual(A,RFrob(A,makdisi_evaluation_frobenius),RV2);
    assert REqual(minusA,RTau(A,makdisi_evaluation_involution),RV2);
    print "PASS|264_CLASS_FROBENIUS_AND_INVOLUTION";
end if;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|264_CM_FRAME_CUBIC_CLASS_CHECKS";quit;
