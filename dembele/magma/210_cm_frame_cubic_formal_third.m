// D82: correct a genuine divisor lift by division by three in the formal kernel.
SetQuitOnError(true); SetColumns(0); SetSeed(82210+formal_chain_start); started:=Cputime();
load "dembele/magma/199_cm_frame_cubic_precision_model.m";
classes:=AssociativeArray(Integers());
lifted:=RMultiply(RBase(Matrix(ZZ,formal_divisor_coordinates)),RV2);
if #formal_saved_indices eq 0 then
    delta:=RChord(RNegClass(RWP,RV2),RWM,RV1,RV2,RV3);
    minusLifted:=RNegClass(lifted,RV2);
    tripleLifted:=RChord(RChord(lifted,lifted,RV1,RV2,RV3),minusLifted,RV1,RV2,RV3);
    classes[1]:=RChord(tripleLifted,delta,RV1,RV2,RV3); // -(3A'+Delta)
else
    delta:=RMultiply(RDecode(formal_saved_delta),RV2);
end if;
for i in [1..#formal_saved_indices] do
    classes[formal_saved_indices[i]]:=RMultiply(RDecode(formal_saved_coordinates[i]),RV2);
end for;
for j in [formal_chain_start..formal_chain_end] do
    item:=formal_chain[j];
    if j eq 2 then classes[j]:=RNegClass(classes[1],RV2);
    else
        assert item[1] eq -formal_chain[item[2]][1]-formal_chain[item[3]][1];
        classes[j]:=RChord(classes[item[2]],classes[item[3]],RV1,RV2,RV3);
    end if;
end for;
if formal_chain_end eq #formal_chain then
    corrected:=RNegClass(RChord(lifted,classes[#formal_chain],RV1,RV2,RV3),RV2);
    minusA:=RNegClass(corrected,RV2);
    triple:=RChord(RChord(corrected,corrected,RV1,RV2,RV3),minusA,RV1,RV2,RV3);
    assert REqual(triple,RNegClass(delta,RV2),RV2);
    assert REqual(corrected,RFrob(corrected,makdisi_evaluation_frobenius),RV2);
    assert REqual(minusA,RTau(corrected,makdisi_evaluation_involution),RV2);
    printf "FORMAL_CORRECTED_COORDINATES|%o\n",REncode(RCoordinates(RV2,corrected));
    print "PASS|FORMAL_THIRD_RELATION_AND_SYMMETRIES";
end if;
printf "CHECKPOINT_INDICES|%o\n",formal_keep_indices;
printf "CHECKPOINT_COORDINATES|%o\n",[REncode(RCoordinates(RV2,classes[i])):i in formal_keep_indices];
printf "CHECKPOINT_DELTA|%o\n",REncode(RCoordinates(RV2,delta));
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|210_CM_FRAME_CUBIC_FORMAL_THIRD";quit;
