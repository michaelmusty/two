// D81: one bounded, checkpointed part of the scalar multiplication.
SetQuitOnError(true); SetColumns(0); started:=Cputime();
// The wrapper loads this chunk's immutable input first.
SetSeed(8100+lift_chain_start);
load "dembele/magma/187_cm_frame_cubic_lift_model.m";
classes:=AssociativeArray(Integers());
for j in [1..#lift_saved_indices] do
    classes[lift_saved_indices[j]]:=RMultiply(RDecode(lift_saved_coordinates[j]),RV2);
end for;
for j in [lift_chain_start..lift_chain_end] do
    item:=lift_chain[j];
    if j eq 2 then
        classes[j]:=RNegClass(classes[1],RV2);
    else
        assert item[1] eq -lift_chain[item[2]][1]-lift_chain[item[3]][1];
        classes[j]:=RChord(classes[item[2]],classes[item[3]],RV1,RV2,RV3);
    end if;
    if j mod 10 eq 0 then printf "CHAIN_PROGRESS|%o %o\n",j,Cputime(started); end if;
end for;
if lift_chain_end eq #lift_chain then
    candidate:=classes[#lift_chain]; delta:=classes[1];
    minusA:=RNegClass(candidate,RV2);
    minusTwoA:=RChord(candidate,candidate,RV1,RV2,RV3);
    threeA:=RChord(minusTwoA,minusA,RV1,RV2,RV3);
    assert REqual(threeA,RNegClass(delta,RV2),RV2);
    assert REqual(RFrob(candidate,makdisi_evaluation_frobenius),candidate,RV2);
    assert REqual(RTau(candidate,makdisi_evaluation_involution),minusA,RV2);
    print "PASS|THIRD_RELATION_AND_SYMMETRIES_MOD961";
end if;
printf "CHECKPOINT_INDICES|%o\n",lift_keep_indices;
printf "CHECKPOINT_COORDINATES|%o\n",[REncode(RCoordinates(RV2,classes[j])):j in lift_keep_indices];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|190_CM_FRAME_CUBIC_LIFT_THIRD";quit;
