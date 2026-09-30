// D82: precision-parameterized unit-pivot arithmetic, adapted from D81 script 186.
// The wrapper sets precision_digits; a pair represents M0+b*M1.
precision_modulus:=31^precision_digits; ZZ:=Integers(precision_modulus); UF<tF>:=PolynomialRing(GF(31));
kk<bF>:=ext<GF(31)|tF^2+29*tF+3>;
function RZero(n,m) return <ZeroMatrix(ZZ,n,m),ZeroMatrix(ZZ,n,m)>; end function;
function RBase(M) return <M,ZeroMatrix(ZZ,Nrows(M),Ncols(M))>; end function;
function RId(n) return RBase(IdentityMatrix(ZZ,n)); end function;
function RAdd(A,B) return <A[1]+B[1],A[2]+B[2]>; end function;
function RNegate(A) return <-A[1],-A[2]>; end function;
function RSubtract(A,B) return RAdd(A,RNegate(B)); end function;
function RTranspose(A) return <Transpose(A[1]),Transpose(A[2])>; end function;
function RRows(A,ii) return <Submatrix(A[1],ii,[1..Ncols(A[1])]),Submatrix(A[2],ii,[1..Ncols(A[2])])>; end function;
function RCols(A,jj) return <Submatrix(A[1],[1..Nrows(A[1])],jj),Submatrix(A[2],[1..Nrows(A[2])],jj)>; end function;
function RJoin(A,B) return <VerticalJoin(A[1],B[1]),VerticalJoin(A[2],B[2])>; end function;
function RIsZero(A) return A[1] eq 0 and A[2] eq 0; end function;
function RMultiply(A,B)
    p:=A[1]*B[1]; q:=A[2]*B[2]; r:=(A[1]+A[2])*(B[1]+B[2]);
    return <p-3*q,r-p-30*q>;
end function;
function RReduce(A)
    return Matrix(kk,Nrows(A[1]),Ncols(A[1]),[kk!(Integers()!c):c in Eltseq(A[1])])+
        bF*Matrix(kk,Nrows(A[2]),Ncols(A[2]),[kk!(Integers()!c):c in Eltseq(A[2])]);
end function;
function RLift(M)
    cs:=[Eltseq(c):c in Eltseq(M)];
    return <Matrix(ZZ,Nrows(M),Ncols(M),[Integers()!c[1]:c in cs]),
        Matrix(ZZ,Nrows(M),Ncols(M),[Integers()!c[2]:c in cs])>;
end function;
function RFromNative(M)
    cs:=[Eltseq(c):c in Eltseq(M)];
    return <Matrix(ZZ,Nrows(M),Ncols(M),[c[1]:c in cs]),Matrix(ZZ,Nrows(M),Ncols(M),[c[2]:c in cs])>;
end function;
function RInverse(A)
    red:=RReduce(A); assert Nrows(red) eq Ncols(red) and Rank(red) eq Nrows(red);
    init:=RLift(red^-1); identity:=RId(Nrows(red));
    out:=init; digits:=1;
    while digits lt precision_digits do
        out:=RMultiply(out,RSubtract(RAdd(identity,identity),RMultiply(A,out)));
        digits*:=2;
    end while;
    assert RMultiply(out,A) eq identity;
    return out;
end function;
function FPivots(M)
    E:=EchelonForm(M);
    return [Min([j:j in [1..Ncols(E)]|E[i,j] ne 0]):i in [1..Rank(M)]];
end function;
function RIndependentRows(A)
    return RRows(A,FPivots(Transpose(RReduce(A))));
end function;
function RCoordinates(B,A)
    jj:=FPivots(RReduce(B)); assert #jj eq Nrows(B[1]);
    out:=RMultiply(RCols(A,jj),RInverse(RCols(B,jj)));
    assert RMultiply(out,B) eq A;
    return out;
end function;
function REquations(B)
    nr:=Nrows(B[1]); nc:=Ncols(B[1]); jj:=FPivots(RReduce(B)); assert #jj eq nr;
    other:=[j:j in [1..nc]|not j in jj];
    coeff:=RMultiply(RInverse(RCols(B,jj)),RCols(B,other));
    E:=RZero(nc,#other);
    for j in [1..#other] do
        E[1][other[j],j]:=1;
        for i in [1..nr] do
            E[1][jj[i],j]:=-coeff[1][i,j]; E[2][jj[i],j]:=-coeff[2][i,j];
        end for;
    end for;
    assert RIsZero(RMultiply(B,E)); return E;
end function;
// This is the kernel of a maximal set of unit-pivot constraints. Until
// the proved target rank is reached it may relax nonunit constraints.
function RKernelRelaxed(M)
    red:=RReduce(M); n:=Nrows(red); r:=Rank(red);
    if r eq 0 then return RId(n); end if;
    if r eq n then return RZero(0,n); end if;
    jj:=FPivots(red); ii:=FPivots(Transpose(Submatrix(red,[1..n],jj)));
    other:=[i:i in [1..n]|not i in ii];
    mp:=RCols(M,jj);
    dep:=RNegate(RMultiply(RRows(mp,other),RInverse(RRows(mp,ii))));
    out:=RZero(n-r,n);
    for j in [1..n-r] do
        out[1][j,other[j]]:=1;
        for i in [1..r] do out[1][j,ii[i]]:=dep[1][j,i]; out[2][j,ii[i]]:=dep[2][j,i]; end for;
    end for;
    assert RIsZero(RMultiply(out,mp)); return out;
end function;
function RScaleRows(A,f)
    return RMultiply(A,<DiagonalMatrix(Eltseq(f[1])),DiagonalMatrix(Eltseq(f[2]))>);
end function;
function RRandomSection(A)
    repeat
        c:=RandomMatrix(kk,1,Nrows(A[1]));
    until c ne 0;
    return RMultiply(RLift(c),A);
end function;
function RProduct(A,B,dim)
    out:=RZero(0,Ncols(A[1]));
    for trial in [1..16] do
        out:=RIndependentRows(RJoin(out,RScaleRows(B,RRandomSection(A))));
        assert Nrows(out[1]) le dim;
        if Nrows(out[1]) eq dim then return out; end if;
    end for;
    error "bounded lifted product did not reach the proved RR rank";
end function;
function RQuotient(A,B,V,dim)
    eqs:=REquations(B); current:=V; samples:=[* *];
    for trial in [1..16] do
        f:=RRandomSection(A); Append(~samples,f);
        constraints:=RMultiply(RScaleRows(current,f),eqs);
        ker:=RKernelRelaxed(constraints); current:=RMultiply(ker,current);
        assert Nrows(current[1]) ge dim;
        if Nrows(current[1]) eq dim then
            // A free RR target of rank dim lies in current; Nakayama gives
            // equality. Verify all sampled constraints over the whole ring.
            assert &and[RIsZero(RMultiply(RScaleRows(current,g),eqs)):g in samples];
            return current;
        end if;
    end for;
    error "bounded lifted quotient did not reach the proved RR rank";
end function;
function RDegreeZero(A,B,V)
    eqs:=REquations(B); current:=V;
    for trial in [1..16] do
        ker:=RKernelRelaxed(RMultiply(RScaleRows(current,RRandomSection(A)),eqs));
        if Nrows(ker[1]) eq 0 then return false,RZero(1,Ncols(V[1])); end if;
        current:=RMultiply(ker,current);
        if Nrows(current[1]) eq 1 then
            return RIsZero(RMultiply(RScaleRows(A,current),eqs)),current;
        end if;
    end for;
    error "bounded degree-zero quotient did not reach rank at most one";
end function;
function RNegClass(W,V2)
    return RQuotient(W,RScaleRows(V2,RRows(W,[1])),V2,81);
end function;
function RChord(A,B,V1,V2,V3)
    prod:=RProduct(A,B,201); small:=RQuotient(V1,prod,V3,81);
    return RQuotient(small,RScaleRows(V2,RRows(small,[1])),V2,81);
end function;
function REqual(A,B,V2)
    return RDegreeZero(A,RScaleRows(B,RRows(A,[1])),V2);
end function;
function RTau(M,tt) return RCols(M,tt); end function;
function RFrob(M,ff)
    out:=RCols(M,ff); return <out[1]-29*out[2],-out[2]>;
end function;
function REncode(M)
    return [[Integers()!M[1][i,j]+precision_modulus*(Integers()!M[2][i,j]):j in [1..Ncols(M[1])]]:i in [1..Nrows(M[1])]];
end function;
function RDecode(rows)
    return <Matrix(ZZ,[[c mod precision_modulus:c in row]:row in rows]),Matrix(ZZ,[[c div precision_modulus:c in row]:row in rows])>;
end function;
function RNormalize(A)
    return RMultiply(RInverse(RCols(A,FPivots(RReduce(A)))),A);
end function;
function RBaseRow(cs) return RBase(Matrix(ZZ,1,#cs,cs)); end function;
function RScalar(c,A) return <c*A[1],c*A[2]>; end function;
function RPointInverse(f)
    n:=Ncols(f[1]); out:=RZero(1,n);
    for i in [1..n] do
        a:=f[1][1,i]; b:=f[2][1,i]; norm:=a^2-29*a*b+3*b^2;
        assert IsUnit(norm); inv:=norm^-1;
        out[1][1,i]:=(a-29*b)*inv; out[2][1,i]:=-b*inv;
    end for;
    assert RScaleRows(f,out) eq RBaseRow([1:i in [1..n]]); return out;
end function;
function RIntersection(A,B,dim)
    eqs:=REquations(B); out:=RMultiply(RKernelRelaxed(RMultiply(A,eqs)),A);
    assert Nrows(out[1]) eq dim and RIsZero(RMultiply(out,eqs)); return out;
end function;
function BaseCoefficients(A)
    assert A[2] eq 0;
    return [[Integers()!z:z in Eltseq(row)]:row in Rows(A[1])];
end function;
