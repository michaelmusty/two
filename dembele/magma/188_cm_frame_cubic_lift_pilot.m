// D81 arithmetic pilot before the scalar multiplication.
SetQuitOnError(true); SetColumns(0); SetSeed(81); started:=Cputime();
load "dembele/magma/187_cm_frame_cubic_lift_model.m";
// Independent native-ring comparison for pair arithmetic.
native1:=RandomMatrix(AG,4,7); native2:=RandomMatrix(AG,7,4);
assert RMultiply(RFromNative(native1),RFromNative(native2)) eq RFromNative(native1*native2);
sq:=RandomMatrix(AG,4,4);
while Rank(RReduce(RFromNative(sq))) ne 4 do sq:=RandomMatrix(AG,4,4); end while;
assert RInverse(RFromNative(sq)) eq RFromNative(sq^-1);
printf "MODEL_CPU_SECONDS|%o\n",Cputime(started);
t:=Cputime(); minusP:=RNegClass(RWP,RV2);
RD:=RChord(minusP,RWM,RV1,RV2,RV3);
printf "DELTA_CPU_SECONDS|%o\n",Cputime(t);
ok,witness:=RDegreeZero(RV1,RD,RV1); assert not ok;
minusD:=RNegClass(RD,RV2);
assert REqual(minusD,RTau(RD,makdisi_evaluation_involution),RV2);
assert REqual(RD,RFrob(RD,makdisi_evaluation_frobenius),RV2);
zero:=RChord(RD,minusD,RV1,RV2,RV3);
assert RDegreeZero(RV1,zero,RV1);
printf "LIFT_DELTA_COORDINATES|%o\n",REncode(RCoordinates(RV2,RD));
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|188_CM_FRAME_CUBIC_LIFT_PILOT";quit;
