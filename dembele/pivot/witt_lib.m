// Arithmetic over W = W_N(K), K = F_p^17, in coordinates: an element, vector
// or matrix over W is a sequence of 17 objects over Z/p^N (coefficients of
// 1, om, ..., om^16, om a root of the lifted defining polynomial of K).
// Products use evaluation at 33 integer points and interpolation, so that a
// product over W costs 33 products over Z/p^N (fast matrix kernel).
// Requires: p, N, ZN, ZZ, K = GF(p,17), padic_lib.m.
WD := 17;
phiZ := PolynomialRing(ZZ)![ZZ!c : c in Coefficients(DefiningPolynomial(K))];
PWZ<yy> := PolynomialRing(ZN);
WQ<om> := quo<PWZ | PWZ!phiZ>;
function PadTo(s, n) return s cat [Universe(s)!0 : i in [#s+1..n]]; end function;
redZ := [[ZZ!c : c in PadTo(Coefficients(PWZ!(om^t)), WD)] : t in [0..2*WD-2]];
NEVP := 2*WD - 1;
VinvZ := [[ZZ!c : c in Eltseq(r)] : r in Rows(InvN(Matrix(ZN, NEVP, NEVP, [(ZN!e)^t : t in [0..NEVP-1], e in [0..NEVP-1]])))];
// VinvZ[t][e]: coefficient of om^(t-1) from the value at the point e-1.
// Interpolation and reduction mod phi combined: 17 x 33 integer matrix mod p^N.
IVMZ := [[(VinvZ[s][e] + &+[redZ[t][s]*VinvZ[t][e] : t in [WD+1..NEVP]]) mod LIBP^N : e in [1..NEVP]] : s in [1..WD]];
function WEvalM(A)      // 33 x (r*c) matrix: flattened values at the points 0..32
    R := BaseRing(A[1]);
    C := Matrix(R, WD, Nrows(A[1])*Ncols(A[1]), &cat[Eltseq(A[i]) : i in [1..WD]]);
    return Matrix(R, NEVP, WD, [(R!e)^i : i in [0..WD-1], e in [0..NEVP-1]])*C;
end function;
function WUnflat(Cm, r, c)
    return [Matrix(BaseRing(Cm), r, c, Eltseq(Cm[s])) : s in [1..Nrows(Cm)]];
end function;
function WInterpM(Pm, r, c)
    R := BaseRing(Pm);
    return WUnflat(Matrix(R, WD, NEVP, &cat IVMZ)*Pm, r, c);
end function;
function WMul(A, B)
    R := BaseRing(A[1]); r := Nrows(A[1]); c := Ncols(B[1]);
    Ea := WUnflat(WEvalM(A), r, Ncols(A[1])); Eb := WUnflat(WEvalM(B), Nrows(B[1]), c);
    return WInterpM(Matrix(R, NEVP, r*c, &cat[Eltseq(Ea[j]*Eb[j]) : j in [1..NEVP]]), r, c);
end function;
function WPre(B)         // evaluated form of a fixed right factor
    return WUnflat(WEvalM(B), Nrows(B[1]), Ncols(B[1]));
end function;
function WMulPre(A, Eb)
    R := BaseRing(A[1]); r := Nrows(A[1]); c := Ncols(Eb[1]);
    Ea := WUnflat(WEvalM(A), r, Ncols(A[1]));
    return WInterpM(Matrix(R, NEVP, r*c, &cat[Eltseq(Ea[j]*Eb[j]) : j in [1..NEVP]]), r, c);
end function;
function WHad(A, B)     // pointwise product of vectors over W (1 x n matrices)
    R := BaseRing(A[1]); n := Ncols(A[1]);
    ea := Eltseq(WEvalM(A)); eb := Eltseq(WEvalM(B));
    return WInterpM(Matrix(R, NEVP, n, [ea[t]*eb[t] : t in [1..#ea]]), 1, n);
end function;
function WAdd(A, B) return [A[i] + B[i] : i in [1..WD]]; end function;
function WSub(A, B) return [A[i] - B[i] : i in [1..WD]]; end function;
function WScal(c, A) return [c*A[i] : i in [1..WD]]; end function;
function WIsZero(A) return &and[IsZero(A[i]) : i in [1..WD]]; end function;
function WRightZ(A, M) return [A[i]*M : i in [1..WD]]; end function;       // times a matrix over Z/p^N
function WCols(A, J) return [Cols_(A[i], J) : i in [1..WD]]; end function;
function WRows(A, I) return [Rows_(A[i], I) : i in [1..WD]]; end function;
function WRing(A, R) return [ChangeRing(ChangeRing(A[i], ZZ), R) : i in [1..WD]]; end function;
function WFromField(Mk, R)   // matrix over K -> lift over R (coefficients in [0, p))
    E := [Eltseq(c) : c in Eltseq(Mk)];
    return [Matrix(R, Nrows(Mk), Ncols(Mk), [ZZ!e[i] : e in E]) : i in [1..WD]];
end function;
function WToField(A)         // reduction mod p, matrix over K
    return &+[K.1^(i-1)*ChangeRing(Red(A[i]), K) : i in [1..WD]];
end function;
function WOne(R, n)
    return [ScalarMatrix(R, n, 1)] cat [ZeroMatrix(R, n, n) : i in [2..WD]];
end function;
// One Newton step for the inverse: X <- X*(2 - A*X).
function WInvStep(A, X)
    R := BaseRing(A[1]); n := Nrows(A[1]);
    T := WMul(A, X);
    T := WSub(WScal(2, WOne(R, n)), T);
    return WMul(X, T);
end function;
// Pointwise inverse of a vector over W (1 x n) with unit entries.
function WInvVec(A)
    R := BaseRing(A[1]); n := Ncols(A[1]);
    ak := WToField(A);
    Y := WFromField(Matrix(K, 1, n, [c^-1 : c in Eltseq(ak)]), R);
    two := [Matrix(R, 1, n, [2 : r in [1..n]])] cat [ZeroMatrix(R, 1, n) : i in [2..WD]];
    prec := 1; Nn := Valuation(#R, LIBP);
    while prec lt Nn do Y := WHad(Y, WSub(two, WHad(A, Y))); prec *:= 2; end while;
    return Y;
end function;
