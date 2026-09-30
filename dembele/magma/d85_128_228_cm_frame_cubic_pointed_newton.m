// D85 redirected loads; original SHA256 e350824c5cab6f79c930aec89993c79929609fffbba014f52aac592493b5751f
// D82: square-zero class correction in unique pointed coordinates.
SetQuitOnError(true); SetColumns(0); SetSeed(82228); started:=Cputime();
load "dembele/magma/d85_128_199_cm_frame_cubic_precision_model.m";
load "dembele/magma/227_cm_frame_cubic_pointed_class_chart.m";
if newton_mode eq "classes" then
    A:=RMultiply(RBase(Matrix(ZZ,formal_divisor_coordinates)),RV2);
    delta:=RChord(RNegClass(RWP,RV2),RWM,RV1,RV2,RV3);
    twiceA:=RNegClass(RChord(A,A,RV1,RV2,RV3),RV2);
    B:=RChord(twiceA,delta,RV1,RV2,RV3); // -2*A-Delta = A-(3*A+Delta)
    printf "NEWTON_TARGET_COORDINATES|%o\n",REncode(RCoordinates(RV2,B));
    printf "NEWTON_DELTA_COORDINATES|%o\n",REncode(RCoordinates(RV2,delta));
else
    W:=newton_mode eq "normalize_a" select
        RMultiply(RBase(Matrix(ZZ,formal_divisor_coordinates)),RG2) else
        RMultiply(RDecode(newton_target_coordinates),RG2);
    C,g,r,mu:=PointedClassChart(W,RG2,RV2,chartjets);
    assert [[x mod previous_cubic_modulus:x in row]:row in BaseCoefficients(C)] eq previous_cubic_descended_divisor_coordinates;
    printf "NEWTON_POINTED_COORDINATES|%o\n",BaseCoefficients(C);
    printf "NEWTON_G_COEFFICIENTS|%o\n",REncode(g)[1];
    printf "NEWTON_R_COEFFICIENTS|%o\n",REncode(r)[1];
    printf "NEWTON_G_VANISHING_ORDER|%o\n",mu;
end if;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|228_CM_FRAME_CUBIC_POINTED_NEWTON";quit;
