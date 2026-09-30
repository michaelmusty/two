// D78: finite-field Makdisi arithmetic, using the verified evaluation spaces.
// Space rows are section values. Every product/quotient has its RR dimension
// checked; random choices only accelerate a calculation with a verified result.
load "dembele/data/computed/cm_frame_cover_makdisi.m";
U<t>:=PolynomialRing(GF(31));
k<b>:=ext<GF(31)|U!makdisi_field_modulus>;
function Dec(rows,k)
    return Matrix(k,[[k!(c mod 31)+k.1*(c div 31):c in row]:row in rows]);
end function;
V1:=Transpose(Dec(makdisi_v1_evaluations,k));
V2:=Transpose(Dec(makdisi_v2_evaluations,k));
V3:=Transpose(Dec(makdisi_v3_evaluations,k));
WP:=Transpose(Dec(makdisi_plus_evaluations,k));
WM:=Transpose(Dec(makdisi_minus_evaluations,k));

function ScaleRows(A,f)
    kk:=BaseRing(A);
    return Matrix(kk,[[v[j]*f[j]:j in [1..Ncols(A)]]:v in Rows(A)]);
end function;
function RandSection(A)
    kk:=BaseRing(A);
    repeat
        v:=Vector(kk,[Random(kk):i in [1..Nrows(A)]])*A;
    until v ne 0;
    return v;
end function;
function ProductSpace(A,B,dim)
    out:=ZeroMatrix(BaseRing(A),0,Ncols(A));
    for trial in [1..16] do
        out:=Matrix(Basis(RowSpace(VerticalJoin(out,ScaleRows(B,RandSection(A))))));
        assert Nrows(out) le dim;
        if Nrows(out) eq dim then return out; end if;
    end for;
    error "bounded product search did not reach the proved RR dimension";
end function;
function QuotientSpace(A,B,V,dim)
    eqs:=Transpose(Matrix(Basis(Nullspace(Transpose(B)))));
    current:=V;
    for trial in [1..16] do
        constraints:=ScaleRows(current,RandSection(A))*eqs;
        ker:=Matrix(Basis(Nullspace(constraints)));
        current:=ker*current;
        assert Nrows(current) ge dim;
        if Nrows(current) eq dim then return current; end if;
    end for;
    error "bounded quotient search did not reach the proved RR dimension";
end function;
function NegClass(W)
    return QuotientSpace(W,ScaleRows(V2,W[1]),V2,81);
end function;
function ChordClass(A,B)
    AB:=ProductSpace(A,B,201);
    small:=QuotientSpace(V1,AB,V3,81);
    return QuotientSpace(small,ScaleRows(V2,small[1]),V2,81);
end function;
function AddClass(A,B)
    return NegClass(ChordClass(A,B));
end function;

// For a degree-zero quotient the answer has dimension at most one.
// In the one-dimensional case check every generator, not a random sample.
function DegreeZeroQuotient(A,B,V)
    eqs:=Transpose(Matrix(Basis(Nullspace(Transpose(B)))));
    current:=V;
    for trial in [1..16] do
        ker:=Matrix(Basis(Nullspace(ScaleRows(current,RandSection(A))*eqs)));
        if Nrows(ker) eq 0 then return false,V[1]*0; end if;
        current:=ker*current;
        if Nrows(current) eq 1 then
            h:=current[1];
            return ScaleRows(A,h)*eqs eq 0,h;
        end if;
    end for;
    error "bounded degree-zero quotient did not reach dimension at most one";
end function;
function ZeroClass(W)
    return DegreeZeroQuotient(V1,W,V1);
end function;
function EqualClass(A,B)
    return DegreeZeroQuotient(A,ScaleRows(B,A[1]),V2);
end function;
function DeckClass(W)
    return Matrix(BaseRing(W),[[v[i]:i in makdisi_evaluation_involution]:v in Rows(W)]);
end function;
function FrobeniusClass(W)
    return Matrix(BaseRing(W),[[v[i]^31:i in makdisi_evaluation_frobenius]:v in Rows(W)]);
end function;
function EncRows(M)
    return [[Integers()!Eltseq(c)[1]+31*(Integers()!Eltseq(c)[2]):c in Eltseq(v)]:v in Rows(M)];
end function;
