// Common setup for the p-adic lift (scripts 15-17): rings, the curve C over
// Z/p^N, Hensel lifting of points of C and X.
// Requires: N, st_* (state), cub_* (cubic), the exact lists, loaded before.
p := st_p; Fp := GF(p); ZN := Integers(p^N); Z1 := Integers(p);
LIBP := p; LIBF := Fp;
assert #st_modulus eq 3 and st_modulus[3] eq 1;
m0 := st_modulus[1]; m1 := st_modulus[2];
LC0 := -m0; LC1 := -m1;
load "padic_lib.m";
Up<tt> := PolynomialRing(Fp); k4<b> := ext<Fp | Up!st_modulus>;
function DecE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..2]];
    return k4!s;
end function;
PZ<xx> := PolynomialRing(ZN); GG<th> := quo<PZ | xx^2 + m1*xx + m0>;
function Pair(g)
    s := Coefficients(PZ!g); s cat:= [ZN!0 : i in [#s+1..2]];
    return s;
end function;
function LiftK(c)
    s := Eltseq(c);
    return GG!(PZ![ZZ!s[1], ZZ!s[2]]);
end function;
function InvG(g)
    s := Pair(g);
    nr := s[1]^2 + LC1*s[1]*s[2] - LC0*s[2]^2;
    return GG!(PZ![(s[1] + LC1*s[2])*nr^-1, -s[2]*nr^-1]);
end function;
function Q2Z(x)
    x := Rationals()!x;
    return ZN!Numerator(x)*(ZN!Denominator(x))^-1;
end function;
function ToZ1(M)
    return ChangeRing(ChangeRing(M, ZZ), Z1);
end function;
function ToZN(M)
    return ChangeRing(ChangeRing(M, ZZ), ZN);
end function;
rowsZ := Matrix(ZN, [[Q2Z(c) : c in r] : r in rows]);
rowsK := ChangeRing(Red(rowsZ), k4); rowsG := ChangeRing(rowsZ, GG);
Lmat := [ZeroMatrix(ZN, 91, 16) : j in [1..16]];
for t in [1..#pairs] do
    a := pairs[t][1]; c := pairs[t][2];
    for i in [1..91] do
        Lmat[a][i, c] +:= rowsZ[i, t];
        Lmat[c][i, a] +:= rowsZ[i, t];
    end for;
end for;
LmatK := [ChangeRing(Red(L), k4) : L in Lmat]; LmatG := [ChangeRing(L, GG) : L in Lmat];
numG := Matrix(GG, 1, #pairs, [GG!Q2Z(c) : c in rational_numerator]);
denG := Matrix(GG, 1, #pairs, [GG!Q2Z(c) : c in rational_denominator]);
function Mon2(x)
    return [x[pr[1]]*x[pr[2]] : pr in pairs];
end function;
function Mons(x, exps)
    return [&*[x[t]^e[t] : t in [1..16] | e[t] ne 0] : e in exps];
end function;
halfG := GG!((ZN!2)^-1);
// Hensel lift of a point (16 coordinates with x16 = 1, and w) of X. The
// coordinate kept fixed is the first of x15, x14, ... with a unit Jacobian minor.
function LiftC(x0)
    assert x0[16] eq 1;
    xc := Matrix(k4, 16, 1, x0);
    Jall := HorizontalJoin([LmatK[j]*xc : j in [1..15]]);
    par := 0;
    for cand in [15..1 by -1] do
        vars := [j : j in [1..15] | j ne cand];
        Jk := Cols_(Jall, vars);
        if Rank(Jk) eq 14 then par := cand; break; end if;
    end for;
    if par eq 0 then return false, 0; end if;
    inds := IndRows(Jk);
    Jinv := Matrix(GG, 14, 14, [LiftK(c) : c in Eltseq(Rows_(Jk, inds)^-1)]);
    Lsel := [Rows_(LmatG[j], inds) : j in vars];
    rsel := Rows_(rowsG, inds);
    x := [LiftK(c) : c in x0];
    two := ScalarMatrix(GG, 14, 2);
    e := 1;
    while e lt N do
        X := Matrix(GG, 16, 1, x);
        J := HorizontalJoin([Lsel[j]*X : j in [1..14]]);
        Jinv := Jinv*(two - J*Jinv);
        d := Jinv*(rsel*Matrix(GG, #pairs, 1, Mon2(x)));
        for j in [1..14] do x[vars[j]] -:= d[j, 1]; end for;
        e *:= 2;
    end while;
    assert IsZero(rowsG*Matrix(GG, #pairs, 1, Mon2(x)));
    return true, x;
end function;
function LiftW(x, w0)
    mon := Matrix(GG, #pairs, 1, Mon2(x));
    target := (numG*mon)[1, 1]*InvG((denG*mon)[1, 1]);
    w := LiftK(w0); e := 1;
    while e lt N do w := (w + target*InvG(w))*halfG; e *:= 2; end while;
    assert w^2 eq target;
    return w;
end function;
function LiftPoint(pt)
    ok, x := LiftC(pt[1..16]);
    if not ok then return false, 0, 0; end if;
    return true, x, LiftW(x, pt[17]);
end function;
function RealMatrix(cols)   // cols: sequences of GG elements (one per point); rows = sections
    A := []; B := [];
    for c in cols do
        prs := [Pair(g) : g in c];
        Append(~A, [s[1] : s in prs]); Append(~B, [s[2] : s in prs]);
    end for;
    return Transpose(Matrix(ZN, A cat B));
end function;
function RatMatrix(cols)    // the same for rational points (theta-part zero)
    A := [];
    for c in cols do
        prs := [Pair(g) : g in c];
        assert &and[s[2] eq 0 : s in prs];
        Append(~A, [s[1] : s in prs]);
    end for;
    return Transpose(Matrix(ZN, A));
end function;
