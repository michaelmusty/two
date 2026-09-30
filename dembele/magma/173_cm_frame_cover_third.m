// D78: scalar search with an exact test of the resulting divisor relation.
SetQuitOnError(true); SetColumns(0); SetSeed(781);
started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/data/computed/cm_frame_cover_third_input.m";
D:=Dec(third_delta_rows,k);
assert Nrows(D) eq 81 and Ncols(D) eq 640 and Rank(D) eq 81;
assert third_heuristic_prym_order eq third_cofactor*3^third_three_valuation;
assert 3*third_scalar+1 eq 2*third_cofactor;
chain:=third_chain; assert chain[1][1] eq 1 and chain[#chain][1] eq third_scalar;
classes:=[*D*];
for i in [2..#chain] do
    n,a,b:=Explode(chain[i]); assert a ge 1 and a lt i and b ge 0 and b lt i;
    if b eq 0 then
        assert n eq -chain[a][1]; next:=NegClass(classes[a]);
    else
        assert n eq -chain[a][1]-chain[b][1]; next:=ChordClass(classes[a],classes[b]);
    end if;
    Append(~classes,next);
    if i mod 25 eq 0 then printf "SCALAR_PROGRESS|%o|%o|%o\n",i,#chain,Cputime(started); end if;
end for;
candidate:=classes[#classes];
minusA:=NegClass(candidate); twiceA:=ChordClass(minusA,minusA);
threeA:=AddClass(twiceA,candidate); residual:=AddClass(threeA,D);
success:=ZeroClass(residual);
minusR:=NegClass(residual); twiceR:=ChordClass(minusR,minusR);
threeR:=AddClass(twiceR,residual); killed3:=ZeroClass(threeR);
minusR3:=NegClass(threeR); twiceR3:=ChordClass(minusR3,minusR3);
nineR:=AddClass(twiceR3,threeR); killed9:=ZeroClass(nineR);
assert EqualClass(FrobeniusClass(candidate),candidate);
assert EqualClass(DeckClass(candidate),minusA);
printf "THREE_DIVISION_VERIFIED|%o\n",success;
printf "RESIDUAL_KILLED_BY_THREE|%o\n",killed3;
printf "RESIDUAL_KILLED_BY_NINE|%o\n",killed9;
printf "CANDIDATE_SECTION_ROWS|%o\n",EncRows(candidate);
printf "RESIDUAL_SECTION_ROWS|%o\n",EncRows(residual);
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|173_CM_FRAME_COVER_THIRD";
quit;
