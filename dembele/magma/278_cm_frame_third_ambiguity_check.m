// D84: independently verify kernel points, their independence, and actual thirds.
SetQuitOnError(true); SetColumns(0); SetSeed(84278); started:=Cputime();
assert assigned torsion_coordinates;
if not assigned corrupt_torsion then corrupt_torsion:=false; end if;
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/data/computed/cm_frame_cover_third_check_input.m";
Delta:=Dec(third_check_delta_rows,k); A:=Dec(third_check_candidate_rows,k);
function Triple(W)
    mW:=NegClass(W); return AddClass(ChordClass(mW,mW),W);
end function;
assert ZeroClass(AddClass(Triple(A),Delta));
span:=[*V1*]; labels:=[[]]; generators:=[* *];
for n in [1..#torsion_coordinates] do
    T:=Dec(torsion_coordinates[n],k)*V2;
    assert Nrows(T) eq 81 and Rank(T) eq 81;
    if corrupt_torsion and n eq 1 then T:=AddClass(T,Delta); end if;
    torsion_relation_ok:=ZeroClass(Triple(T)); assert torsion_relation_ok;
    assert not ZeroClass(T);
    assert EqualClass(FrobeniusClass(T),T);
    assert EqualClass(DeckClass(T),NegClass(T));
    independent:=not &or[EqualClass(T,S):S in span];
    printf "TORSION_INDEPENDENT|%o|%o\n",n,independent;
    if independent and #generators lt 2 then
        newspan:=[* *]; newlabels:=[];
        for a in [0..2] do
            for j in [1..#span] do
                S:=a eq 0 select span[j] else AddClass(span[j],a eq 1 select T else NegClass(T));
                Append(~newspan,S); Append(~newlabels,labels[j] cat [a]);
            end for;
        end for;
        span:=newspan; labels:=newlabels; Append(~generators,T);
    end if;
end for;
assert #generators ge 1 and #span eq 3^#generators;
assert &and[not EqualClass(span[i],span[j]):i,j in [1..#span]|i lt j];
thirds:=[* *];
for i in [1..#span] do
    B:=i eq 1 select A else AddClass(A,span[i]);
    assert ZeroClass(AddClass(Triple(B),Delta));
    assert EqualClass(FrobeniusClass(B),B);
    assert EqualClass(DeckClass(B),NegClass(B));
    coordinates:=Solution(V2,B); assert coordinates*V2 eq B;
    Append(~thirds,EncRows(coordinates));
end for;
printf "VERIFIED_TORSION_RANK_LOWER_BOUND|%o\n",#generators;
printf "THIRD_LABELS|%o\n",labels;
printf "THIRD_COORDINATES|%o\n",thirds;
printf "GENERATOR_COORDINATES|%o\n",[* EncRows(Solution(V2,T)):T in generators *];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|278_THIRD_AMBIGUITY";
quit;
