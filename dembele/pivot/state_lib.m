// Rebuild the evaluation model from a state file written by script 03.
// Requires: the state file already loaded (st_* variables).
// Defines p, q, k4, NEV, V1, V2, V3 (rows = sections, columns = points),
// V1all, V2all (rows = all points), efrob, etau, WP, WM, Delta, Dec, EncM.
p := st_p;
Up<tt> := PolynomialRing(GF(p));
k4<b> := ext<GF(p) | Up!st_modulus>;
deg4 := Degree(k4);
q := p^(deg4 div 2);
function DecE(c)
    s := Intseq(c, p); s cat:= [0 : i in [#s+1..deg4]];
    return k4!s;
end function;
function Dec(rows)
    return Matrix(k4, [[DecE(c) : c in row] : row in rows]);
end function;
function Enc(c)
    return Seqint([Integers()!e : e in Eltseq(c)], p);
end function;
function EncM(M)
    return [[Enc(M[i,j]) : j in [1..Ncols(M)]] : i in [1..Nrows(M)]];
end function;
plist := [[DecE(c) : c in x] : x in st_points];
nn := #plist; evals := st_evals; NEV := #evals;
efrob := [Index(evals, st_frob[i]) : i in evals];
etau := [Index(evals, st_tau[i]) : i in evals];
load "cm_frame_B3_fiber_structure.m";
ellc := [k4!(GF(p)!c) : c in branch_parameter_linear_form];
oddM := Transpose(Matrix(k4, st_oddrows));
V1all := ZeroMatrix(k4, nn, 81);
for i in [1..nn] do
    x := plist[i]; xs := x[1..16];
    lv := &+[ellc[j]*xs[j] : j in [1..16]];
    ev2 := [&*[xs[t]^e[t] : t in [1..16]] : e in st_exps2];
    odd := Vector(k4, [&*[xs[t]^e[t] : t in [1..16]] : e in st_exps3])*oddM;
    vals := ev2 cat [x[17]/lv*c : c in Eltseq(odd)];
    for j in [1..81] do V1all[i,j] := vals[j]; end for;
end for;
V2all := Matrix(k4, [[V1all[r,pr[1]]*V1all[r,pr[2]] : pr in st_pairs2] : r in [1..nn]]);
V1 := Transpose(Matrix([V1all[i] : i in evals]));
V2 := Transpose(Matrix([V2all[i] : i in evals]));
V3 := Matrix(k4, [[V1[pr[1],r]*V2[pr[2],r] : r in [1..NEV]] : pr in st_pairs3]);
assert Rank(V1) eq 81 and Rank(V2) eq 201 and Rank(V3) eq 321;
WP := Dec(st_WP); WM := Dec(st_WM); Delta := Dec(st_Delta);
