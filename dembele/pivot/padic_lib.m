// Linear algebra over Z/p^N by lifting from F_p, and evaluation
// representation with Frobenius pairs of points.
// Requires globals: LIBP (prime), LIBF = GF(LIBP), LC0, LC1 (integers with
// theta^2 = LC1*theta + LC0 in the unramified quadratic ring).
// A value vector at h conjugate pairs of points is a real vector of length
// 2h: (a_1..a_h | b_1..b_h), value a_j + b_j*theta at the chosen point.
// All kernels are verified exactly (K*M eq 0): this fails if the rank over
// Z/p^N exceeds the rank mod p.
ZZ := Integers();
function Red(M)
    return ChangeRing(ChangeRing(M, ZZ), LIBF);
end function;
function IndRows(Mp)
    E := EchelonForm(Transpose(Mp));
    return [Depth(E[i]) : i in [1..Rank(E)]];
end function;
function PivCols(Mp)
    E := EchelonForm(Mp);
    return [Depth(E[i]) : i in [1..Rank(E)]];
end function;
function Rows_(M, I)
    return Submatrix(M, I, [1..Ncols(M)]);
end function;
function Cols_(M, J)
    return Submatrix(M, [1..Nrows(M)], J);
end function;
function InvN(A)
    R := BaseRing(A); n := Nrows(A);
    X := ChangeRing(ChangeRing(Red(A)^-1, ZZ), R);
    prec := 1; Nn := Valuation(#R, LIBP);
    two := ScalarMatrix(R, n, 2);
    while prec lt Nn do X := X*(two - A*X); prec *:= 2; end while;
    return X;
end function;
// Left kernel {v : v*M = 0}, basis independent mod p.
function KerN(M)
    R := BaseRing(M); nr := Nrows(M);
    Mp := Red(M); I := IndRows(Mp); rho := #I;
    Ibar := [i : i in [1..nr] | not i in I];
    if #Ibar eq 0 then return ZeroMatrix(R, 0, nr); end if;
    if rho eq 0 then assert IsZero(M); return IdentityMatrix(R, nr); end if;
    MI := Rows_(M, I);
    Jc := PivCols(Red(MI)); assert #Jc eq rho;
    X := -Cols_(Rows_(M, Ibar), Jc)*InvN(Cols_(MI, Jc));
    KP := HorizontalJoin(X, IdentityMatrix(R, #Ibar));
    order := I cat Ibar; pos := [0 : i in [1..nr]];
    for t in [1..nr] do pos[order[t]] := t; end for;
    K := Cols_(KP, pos);
    assert IsZero(K*M);
    return K;
end function;
// X with X*A = V; rows of A independent mod p.
function SolN(A, V)
    Jc := PivCols(Red(A)); assert #Jc eq Nrows(A);
    X := Cols_(V, Jc)*InvN(Cols_(A, Jc));
    assert X*A eq V;
    return X;
end function;
function BasisN(M)
    return Rows_(M, IndRows(Red(M)));
end function;
function ScaleRows(A, f)
    R := BaseRing(A); h := Ncols(A) div 2; r := Nrows(A);
    Da := DiagonalMatrix(R, [f[j] : j in [1..h]]);
    Db := DiagonalMatrix(R, [f[h+j] : j in [1..h]]);
    Aa := Submatrix(A, 1, 1, r, h); Ab := Submatrix(A, 1, h+1, r, h);
    AbDb := Ab*Db;
    return HorizontalJoin(Aa*Da + LC0*AbDb, Aa*Db + Ab*Da + LC1*AbDb);
end function;
function MulVec(u, f)
    return ScaleRows(Matrix(u), f)[1];
end function;
function InvVec(f)
    R := BaseRing(f); h := Ncols(f) div 2;
    a := [f[j] : j in [1..h]]; b := [f[h+j] : j in [1..h]];
    nr := [(a[j]^2 + LC1*a[j]*b[j] - LC0*b[j]^2)^-1 : j in [1..h]];
    return Vector(R, [(a[j] + LC1*b[j])*nr[j] : j in [1..h]] cat [-b[j]*nr[j] : j in [1..h]]);
end function;
function IsUnitVec(f)
    h := Ncols(f) div 2;
    return &and[(ZZ!f[j]) mod LIBP ne 0 or (ZZ!f[h+j]) mod LIBP ne 0 : j in [1..h]];
end function;
function RandSec(A)
    R := BaseRing(A);
    repeat
        v := Vector(R, [Random(0, LIBP-1) : i in [1..Nrows(A)]])*A;
    until not IsZero(Red(Matrix(v)));
    return v;
end function;
function ProductN(A, B, dim)
    out := ZeroMatrix(BaseRing(A), 0, Ncols(A));
    for trial in [1..32] do
        out := BasisN(VerticalJoin(out, ScaleRows(B, RandSec(A))));
        assert Nrows(out) le dim;
        if Nrows(out) eq dim then return out; end if;
    end for;
    error "ProductN: dimension not reached";
end function;
// {s in V : s*A in B}
function QuotN(A, B, V, dim)
    // Conditions from several random multipliers are stacked until the kernel
    // mod p has the expected dimension; only then is the kernel lifted (a single
    // multiplier with a zero mod p on the base locus would make the rank jump).
    eqs := Transpose(KerN(Transpose(B)));
    cons := ZeroMatrix(BaseRing(V), Nrows(V), 0);
    for trial in [1..16] do
        cons := HorizontalJoin(cons, ScaleRows(V, RandSec(A))*eqs);
        d := Nrows(V) - Rank(Red(cons));
        assert d ge dim;
        if d eq dim then return KerN(cons)*V; end if;
    end for;
    error "QuotN: dimension not reached";
end function;
// Intersection of row spaces (rows of A and of B independent mod p).
function MeetN(A, B)
    K := KerN(VerticalJoin(A, B));
    return BasisN(Submatrix(K, 1, 1, Nrows(K), Nrows(A))*A);
end function;
function DeckN(A, perm)
    h := Ncols(A) div 2;
    return Cols_(A, perm cat [h + j : j in perm]);
end function;
// Plain versions (all evaluation points rational): pointwise product = column scaling.
function ScaleP(A, f)
    return A*DiagonalMatrix(BaseRing(A), Eltseq(f));
end function;
function ProductP(A, B, dim)
    out := ZeroMatrix(BaseRing(A), 0, Ncols(A));
    for trial in [1..32] do
        out := BasisN(VerticalJoin(out, ScaleP(B, RandSec(A))));
        assert Nrows(out) le dim;
        if Nrows(out) eq dim then return out; end if;
    end for;
    error "ProductP: dimension not reached";
end function;
function QuotP(A, B, V, dim)
    // Conditions from several random multipliers are stacked until the kernel
    // mod p has the expected dimension; only then is the kernel lifted (a single
    // multiplier with a zero mod p on the base locus would make the rank jump).
    eqs := Transpose(KerN(Transpose(B)));
    cons := ZeroMatrix(BaseRing(V), Nrows(V), 0);
    for trial in [1..16] do
        cons := HorizontalJoin(cons, ScaleP(V, RandSec(A))*eqs);
        d := Nrows(V) - Rank(Red(cons));
        assert d ge dim;
        if d eq dim then return KerN(cons)*V; end if;
    end for;
    error "QuotP: dimension not reached";
end function;
