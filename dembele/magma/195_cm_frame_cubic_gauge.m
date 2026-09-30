// D82: choose persistent algebraic coordinates on the 80-dimensional linear system.
SetQuitOnError(true); SetColumns(0); SetSeed(82195); started:=Cputime();
load "dembele/magma/187_cm_frame_cubic_lift_model.m";
load "dembele/data/computed/cm_frame_cubic_lift.m";
function Normalize(A)
    return RMultiply(RInverse(RCols(A,FPivots(RReduce(A)))),A);
end function;
function FScale(A,f)
    return Matrix(BaseRing(A),[[A[i,j]*f[j]:j in [1..Ncols(A)]]:i in [1..Nrows(A)]]);
end function;
C:=RBase(Matrix(ZZ,cubic961_descended_divisor_coordinates));
assert C eq Normalize(C); W:=RMultiply(C,RG2);
found:=false;
for trial in [1..128] do
    gcoeff:=RBase(Matrix(ZZ,1,81,[Integers()!Random(GF(31)):i in [1..81]]));
    g:=RMultiply(gcoeff,W);
    good:=[j:j in [1..1024]|RReduce(g)[1,j] ne 0];
    if #good gt 960 then found:=true; break; end if;
end for;
assert found;
N:=RQuotient(W,RScaleRows(RG2,g),RG2,81);
Ncoeff:=Normalize(RCoordinates(RG2,N)); assert Ncoeff[2] eq 0;
N:=RMultiply(Ncoeff,RG2);
assert RIsZero(RMultiply(g,REquations(N)));
G0:=RReduce(RCols(RG2,good)); C0:=RReduce(C); W0:=C0*G0;
N0:=RReduce(RCols(N,good)); g0:=RReduce(RCols(g,good))[1];
gInN:=Solution(N0,g0); assert gInN*N0 eq g0;
omit:=Min([i:i in [1..81]|gInN[i] ne 0]); other:=[i:i in [1..81]|i ne omit];
jW:=FPivots(C0); jG:=FPivots(G0); Ginv:=Submatrix(G0,[1..201],jG)^-1;
derivatives:=[];
for i in other do
    xi:=Vector(kk,[N0[i,j]/g0[j]:j in [1..#good]]);
    product:=FScale(W0,xi);
    coeff:=Submatrix(product,[1..81],jG)*Ginv;
    assert coeff*G0 eq product;
    tangent:=coeff-Submatrix(coeff,[1..81],jW)*C0;
    assert &and[z^31 eq z:z in Eltseq(tangent)];
    Append(~derivatives,[GF(31)!z:z in Eltseq(tangent)]);
end for;
DD:=Matrix(GF(31),derivatives); assert Rank(DD) eq 80;
pins:=FPivots(DD); assert #pins eq 80;
minor:=Submatrix(DD,[1..80],pins); assert Determinant(minor) ne 0;
targets:=[Integers()!Eltseq(C[1])[j]:j in pins];
print "PASS|EIGHTY_PARAMETER_GAUGE_UNIT_MINOR";

// An actual equivalent divisor, changed only in the second digit, must return
// to precisely the saved representative after solving the pinned coordinates.
perturb:=Vector(GF(31),[Random(GF(31)):i in [1..80]]); assert perturb ne 0;
coeffR:=RBase(Matrix(ZZ,1,80,[Integers()!z:z in Eltseq(perturb)]));
r:=RMultiply(coeffR,RRows(N,other));
gBad:=RAdd(g,<31*r[1],31*r[2]>);
WBad:=RQuotient(N,RScaleRows(RG2,gBad),RG2,81);
CBad:=Normalize(RCoordinates(RG2,WBad)); assert CBad[2] eq 0;
predicted:=Matrix(ZZ,81,201,[Integers()!z:z in Eltseq(perturb*DD)]);
assert CBad[1] eq C[1]+31*predicted;
rhs:=Vector(GF(31),[(targets[i]-Integers()!Eltseq(CBad[1])[pins[i]]) div 31:i in [1..80]]);
fix:=rhs*minor^-1;
correction:=RMultiply(RBase(Matrix(ZZ,1,80,[Integers()!z:z in Eltseq(fix)])),RRows(N,other));
gFixed:=RAdd(gBad,<31*correction[1],31*correction[2]>);
WFixed:=RQuotient(N,RScaleRows(RG2,gFixed),RG2,81);
assert Normalize(RCoordinates(RG2,WFixed)) eq C;
assert REqual(RCols(WBad,[1..640]),RCols(W,[1..640]),RV2);
print "PASS|EQUIVALENT_DIVISOR_RETURNS_TO_SAME_GAUGE";

branch0:=Matrix(GF(31),sections_branch_minus_section_values);
qdep:=FPivots(Transpose(branch0)); qfree:=[i:i in [1..81]|not i in qdep];
assert #qfree eq 72;
printf "GAUGE_PIN_INDICES|%o\n",pins;
printf "GAUGE_PIN_VALUES|%o\n",targets;
printf "GAUGE_DIVISOR_PIVOTS|%o\n",jW;
printf "GAUGE_JACOBIAN_MOD31|%o\n",[[Integers()!z:z in Eltseq(row)]:row in Rows(minor)];
printf "GAUGE_JACOBIAN_DETERMINANT_MOD31|%o\n",Integers()!Determinant(minor);
printf "GAUGE_Q_FREE_INDICES|%o\n",qfree;
printf "GAUGE_Q_FREE_VALUES|%o\n",[cubic961_q_coefficients[i]:i in qfree];
printf "GAUGE_U_PIVOT|%o\n",Min([i:i in [1..441]|cubic961_u_coefficients[i] mod 31 ne 0]);
printf "GAUGE_F_PIVOT|%o\n",Min([i:i in [1..201]|cubic961_f_coefficients[i] mod 31 ne 0]);
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|195_CM_FRAME_CUBIC_GAUGE";quit;
