// D82: independent class relation and normalized representative.
SetQuitOnError(true); SetColumns(0); SetSeed(82234); started:=Cputime();
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
function Included(A,B) return RIsZero(RMultiply(A,REquations(B))); end function;
function BaseRow(cs) return RBase(Matrix(ZZ,1,#cs,cs)); end function;
WE:=RMultiply(RDecode(precision_third_coordinates),RG2);
delta:=RChord(RNegClass(RWP,RV2),RWM,RV1,RV2,RV3);
assert REqual(delta,RMultiply(RDecode(precision_third_delta_coordinates),RV2),RV2);
candidate:=RCols(WE,[1..640]); minusA:=RNegClass(candidate,RV2);
threeA:=RChord(RChord(candidate,candidate,RV1,RV2,RV3),minusA,RV1,RV2,RV3);
assert REqual(threeA,RNegClass(delta,RV2),RV2);
assert REqual(candidate,RFrob(candidate,makdisi_evaluation_frobenius),RV2);
assert REqual(minusA,RTau(candidate,makdisi_evaluation_involution),RV2);
WRcoords:=RBase(Matrix(ZZ,pointed_cubic_descended_divisor_coordinates));
WR:=RMultiply(WRcoords,RG2); assert Rank(RReduce(WR)) eq 81;
assert RFrob(WR,ff) eq WR and REqual(RCols(WR,[1..640]),candidate,RV2);
assert WRcoords eq RNormalize(WRcoords);
print "PASS|INDEPENDENT_THIRD_RELATION_AND_REDUCTION_AT_HIGHER_PRECISION";


printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|234_CM_FRAME_CUBIC_POINTED_CLASS_CHECK";quit;
