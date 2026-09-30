// D84: search for rational anti-invariant 3-torsion; verify all orders directly.
SetQuitOnError(true); SetColumns(0);
assert assigned search_seed and assigned search_chain;
SetSeed(8400+search_seed); started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
// Impose a reduced, Frobenius-stable degree-120 divisor in the evaluation set.
indices:=[]; used:={Integers()|};
for i in [1..640] do
    if i in used then continue; end if;
    orb:=Setseq({i,makdisi_evaluation_frobenius[i]});
    used join:=Seqset(orb);
    if Random(0,1) eq 1 and #indices+#orb le 120 then indices cat:=orb; end if;
    if #indices eq 120 then break; end if;
end for;
assert #indices eq 120 and #Seqset(indices) eq 120;
conditions:=Transpose(Submatrix(V2,[1..201],indices));
assert Rank(conditions) eq 120;
coeffs:=Matrix(Basis(Nullspace(Transpose(conditions))));
W:=coeffs*V2; assert Nrows(W) eq 81 and Rank(W) eq 81;
assert EqualClass(FrobeniusClass(W),W);
B:=AddClass(W,NegClass(DeckClass(W)));
assert EqualClass(FrobeniusClass(B),B);
assert EqualClass(DeckClass(B),NegClass(B));
chain:=search_chain; assert chain[1][1] eq 1;
classes:=[*B*];
for i in [2..#chain] do
    n,a,b:=Explode(chain[i]); assert a ge 1 and a lt i and b ge 0 and b lt i;
    if b eq 0 then
        assert n eq -chain[a][1]; next:=NegClass(classes[a]);
    else
        assert n eq -chain[a][1]-chain[b][1]; next:=ChordClass(classes[a],classes[b]);
    end if;
    Append(~classes,next);
    if i mod 40 eq 0 then printf "THREE_TORSION_PROGRESS|%o|%o|%o\n",i,#chain,Cputime(started); end if;
end for;
R:=classes[#classes];
threeR:=AddClass(ChordClass(NegClass(R),NegClass(R)),R);
nineR:=AddClass(ChordClass(NegClass(threeR),NegClass(threeR)),threeR);
z1:=ZeroClass(R); z3:=ZeroClass(threeR); z9:=ZeroClass(nineR);
printf "SCALAR_IMAGE_KILLED_BY_ONE_THREE_NINE|%o\n",[z1,z3,z9];
// The cofactor is a heuristic search aid. Accept only an actual verified kernel point.
found:=not z1 and z9;
printf "NONZERO_THREE_TORSION_FOUND|%o\n",found;
if found then
    T:=z3 select R else threeR;
    assert not ZeroClass(T);
    assert ZeroClass(AddClass(ChordClass(NegClass(T),NegClass(T)),T));
    assert EqualClass(FrobeniusClass(T),T);
    assert EqualClass(DeckClass(T),NegClass(T));
    coordinates:=Solution(V2,T); assert coordinates*V2 eq T;
    printf "TORSION_COORDINATES|%o\n",EncRows(coordinates);
end if;
printf "SEED_DIVISOR_INDICES|%o\n",indices;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|276_RATIONAL_THREE_TORSION";
quit;
