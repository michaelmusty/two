// D82: Newton normalization inside the complete linear system of a divisor.
// Loaded after the precision arithmetic/model. Each step is an actual
// complementary-divisor move, not an entrywise matrix correction.
function RGaugeChart(C,G2,pins)
    assert C[2] eq 0 and C eq RNormalize(C); W:=RMultiply(C,G2);
    found:=false; good:=[];
    for trial in [1..128] do
        g:=RMultiply(RBaseRow([Integers()!Random(GF(31)):i in [1..81]]),W);
        redg:=RReduce(g); good:=[j:j in [1..Ncols(G2[1])]|redg[1,j] ne 0];
        if #good gt 960 then found:=true; break; end if;
    end for;
    assert found;
    N:=RQuotient(W,RScaleRows(G2,g),G2,81);
    Ncoeff:=RNormalize(RCoordinates(G2,N)); assert Ncoeff[2] eq 0;
    N:=RMultiply(Ncoeff,G2); gInN:=RCoordinates(N,g);
    omit:=Min([i:i in [1..81]|RReduce(gInN)[1,i] ne 0]);
    other:=[i:i in [1..81]|i ne omit];
    Ggood:=RCols(G2,good); Wgood:=RCols(W,good);
    quotients:=RScaleRows(RCols(RRows(N,other),good),RPointInverse(RCols(g,good)));
    jG:=FPivots(RReduce(Ggood)); invG:=RInverse(RCols(Ggood,jG));
    jW:=FPivots(RReduce(C)); derivative:=ZeroMatrix(ZZ,80,80);
    for i in [1..80] do
        product:=RScaleRows(Wgood,RRows(quotients,[i]));
        coeff:=RMultiply(RCols(product,jG),invG);
        assert RMultiply(coeff,Ggood) eq product;
        tangent:=RSubtract(coeff,RMultiply(RCols(coeff,jW),C));
        assert tangent[2] eq 0;
        vals:=Eltseq(tangent[1]);
        for j in [1..80] do derivative[i,j]:=vals[pins[j]]; end for;
    end for;
    assert IsUnit(Determinant(derivative));
    return derivative,N,g,other,#good;
end function;

function RGaugeNormalize(C,G2,pins,targets)
    C:=RNormalize(C); assert C[2] eq 0;
    known:=1;
    assert &and[(Integers()!(Eltseq(C[1])[pins[i]]-targets[i])) mod 31 eq 0:i in [1..80]];
    for step in [1..8] do
        vals:=Eltseq(C[1]); rhs:=Vector(ZZ,[ZZ!targets[i]-vals[pins[i]]:i in [1..80]]);
        if rhs eq 0 then return C; end if;
        assert &and[(Integers()!x) mod 31^known eq 0:x in Eltseq(rhs)];
        derivative,N,g,other,ngood:=RGaugeChart(C,G2,pins);
        correction:=rhs*derivative^-1;
        assert &and[(Integers()!x) mod 31^known eq 0:x in Eltseq(correction)];
        r:=RMultiply(RBase(Matrix(ZZ,1,80,Eltseq(correction))),RRows(N,other));
        moved:=RQuotient(N,RScaleRows(G2,RAdd(g,r)),G2,81);
        C:=RNormalize(RCoordinates(G2,moved)); assert C[2] eq 0;
        nextknown:=Min(2*known,precision_digits);
        assert &and[(Integers()!(Eltseq(C[1])[pins[i]]-targets[i])) mod 31^nextknown eq 0:i in [1..80]];
        printf "GAUGE_NEWTON_PROGRESS|%o %o %o %o\n",known,nextknown,
            Integers()!(GF(31)!Determinant(derivative)),ngood;
        known:=nextknown;
    end for;
    error "bounded divisor normalization did not converge";
end function;
