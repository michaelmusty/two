// D158 step 2a: the genus-40 double cover X of the candidate C modulo p (env PRIME),
// its section spaces and the branch class Delta = [D+ - D-], over F_289.
// Port of scripts 153 (divisor E), 164, 166, 170, 171 from p = 31.
// The constant field is F_q, q = p or p^2 according to whether -3 is a square
// mod p; evaluation points lie in F_q^2 and Frobenius is x -> x^q.
// Run from a directory DATA (env) holding the five exact data files.
// Writes STATE (env) with Magma-readable integer encodings.
SetQuitOnError(true); SetColumns(0); SetSeed(158);
started := Cputime();
DATA := GetEnv("DATA"); STATE := GetEnv("STATE");
p := StringToInteger(GetEnv("PRIME"));
rdeg := IsSquare(GF(p)!-3) select 1 else 2; q := p^rdeg; NEV := 1024; NAUX := 111;
k := GF(p);
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
load "cm_frame_B3_rational_model.m";
load "cm_frame_B3_fiber.m";
load "cm_frame_B3_fiber_structure.m";
function Quad(row, mon)
    return &+[row[j]*mon[j] : j in [1..#mon]];
end function;
IC := Ideal(C_candidate); GC := GroebnerBasis(IC);
assert Dimension(IC) eq 2 and Degree(Scheme(P, IC)) eq 30;
LM := [LeadingMonomial(g) : g in GC];
mons2 := [m : m in MonomialsOfDegree(R,2) | not &or[IsDivisibleBy(m,l) : l in LM]];
mons3 := [m : m in MonomialsOfDegree(R,3) | not &or[IsDivisibleBy(m,l) : l in LM]];
assert #mons2 eq 45 and #mons3 eq 75;
mon := [R.(pr[1])*R.(pr[2]) : pr in pairs];
n := Quad(rational_numerator, mon); den := Quad(rational_denominator, mon);
ell := &+[branch_parameter_linear_form[i]*R.i : i in [1..16]];
printf "S03|curve mod %o: dimension and degree pass [%o s]\n", p, Cputime(started);

// Divisors: div(n) = B2 + 2 B3 + T, div(den) = T + 2 E (script 153).
pt := Eltseq(P32_candidate);
i0 := Min([i : i in [1..16] | pt[i] ne 0]);
IP := ideal<R | [R.i - pt[i]/pt[i0]*R.i0 : i in [1..16] | i ne i0]>;
IB2 := D17_ideal meet IP;
IB3 := IC + ideal<R | B3_linear_forms>;
assert Degree(Scheme(P, IB3)) eq 9 and IsReduced(Scheme(P, IB3));
assert Degree(Scheme(P, IB2)) eq 18 and IsReduced(Scheme(P, IB2));
IB3twice := Saturation(IC + ideal<R | [a*b : a, b in B3_linear_forms]>);
IA := IB2 meet IB3twice;
IT := Saturation(ColonIdeal(IC + ideal<R | n>, IA));
assert Degree(Scheme(P, IT)) eq 24;
assert Saturation(IC + ideal<R | n>) eq (IA meet IT);
IE2 := Saturation(ColonIdeal(IC + ideal<R | den>, IT));
assert Degree(Scheme(P, IE2)) eq 36;
IE := Saturation(Radical(IE2));
assert Degree(Scheme(P, IE)) eq 18;
assert Dimension(IE + IT) le 1 and Dimension(IE + IA) le 1;
printf "S03|divisors T (24), E (18), B2 (18), B3 (9) pass [%o s]\n", Cputime(started);

IU := Saturation(ColonIdeal(IC + ideal<R | ell>, IB3));
assert Degree(Scheme(P, IU)) eq 21;
assert Dimension(IU + IB3) le 1;
IJ := Saturation(IE*IU + IC);
assert Degree(Scheme(P, IJ)) eq 39;
candidates := [R|];
for g in GroebnerBasis(IJ) do
    e := TotalDegree(g);
    if e le 3 then
        candidates cat:= [NormalForm(g*m, IC) : m in MonomialsOfDegree(R, 3-e)];
    end if;
end for;
oddmat := Matrix(k, [[MonomialCoefficient(g, m) : m in mons3] : g in candidates]);
oddrows := Basis(RowSpace(oddmat)); assert #oddrows eq 36;
oddpolys := [&+[v[j]*mons3[j] : j in [1..75]] : v in oddrows];
assert &and[g in IJ : g in oddpolys];
exps2 := [Exponents(m) : m in mons2]; exps3 := [Exponents(m) : m in mons3];
oddint := [[Integers()!c : c in Eltseq(v)] : v in oddrows];
printf "S03|section dimensions 45 + 36 = 81 [%o s]\n", Cputime(started);

// Evaluation field F_17^4, constant field F_289 inside it.
k4<b> := GF(p, 2*rdeg);
s3 := Sqrt(k4!-3); assert s3^q eq s3;
fnon := [k!c : c in fiber_nonic_coefficients];
UA<a> := PolynomialRing(k4); fA := UA!fnon;
assert Degree(fA) eq 9 and Discriminant(fA) ne 0;
A<aa> := quo<UA | fA>;
bpt := [A!UA![k!c : c in row] : row in fiber_point_coordinates];
wr := s3*(A!UA![k!c : c in branch_branch_ratio]);
R4 := ChangeRing(R, k4);
ev2b := [Evaluate(R4!m, bpt) : m in mons2];
ev3b := [Evaluate(R4!g, bpt) : g in oddpolys];
branchvals := [* ev2b cat [wr*v : v in ev3b], ev2b cat [-wr*v : v in ev3b] *];
printf "S03|branch algebra: nonic separable mod %o, sqrt(-3) = %o\n", p, Eltseq(s3);

// Points on the chart X16 = 1 away from ell*n*den = 0, w in F_17^4.
P4 := ProjectiveSpace(k4, 15); R4 := CoordinateRing(P4);
polys4 := [R4!g : g in polys]; IC4 := ideal<R4 | polys4>;
n4 := R4!n; den4 := R4!den; ell4 := R4!ell;
points := {@ @}; seen := {k4|}; checked := 0;
while #points lt 1700 do
    // The first 60 fibres are over the prime field, to obtain F_q-points
    // (the odd-degree auxiliary divisor needs a Frobenius-fixed point).
    if #seen lt 60 then a0 := k4!#seen;
    else repeat a0 := Random(k4); until not a0 in seen; end if;
    seen join:= {a0, a0^q};
    S := Scheme(P4, IC4 + ideal<R4 | R4.15 - a0*R4.16>);
    if Dimension(S) ne 0 then continue; end if;
    checked +:= 1;
    for pp in Points(S) do
        xs := Eltseq(pp); if xs[16] eq 0 then continue; end if;
        xs := [c/xs[16] : c in xs];
        nv := Evaluate(n4, xs); dv := Evaluate(den4, xs); lv := Evaluate(ell4, xs);
        if nv*dv*lv eq 0 then continue; end if;
        ok, w := IsSquare(nv/dv);
        if not ok then continue; end if;
        for ww in [w, -w] do
            ptx := xs cat [ww]; Include(~points, ptx);
            Include(~points, [c^q : c in ptx]);
        end for;
    end for;
    if checked mod 20 eq 0 then
        printf "S03|points progress: %o fibres, %o points [%o s]\n", checked, #points, Cputime(started);
    end if;
end while;
plist := Setseq(points); nn := #plist;
frob := [Index(points, [c^q : c in x]) : x in plist];
tau := [Index(points, x[1..16] cat [-x[17]]) : x in plist];
assert &and[frob[frob[i]] eq i and tau[tau[i]] eq i and frob[tau[i]] eq tau[frob[i]] : i in [1..nn]];
printf "S03|%o evaluation points [%o s]\n", nn, Cputime(started);

// Auxiliary divisor (degree 111, Frobenius stable) and evaluation set.
aux := []; used := {Integers()|};
for i in [1..nn] do
    if i in used then continue; end if;
    orb := Setseq({i, frob[i]});
    if #aux + #orb le NAUX then aux cat:= orb; used join:= Seqset(orb); end if;
    if #aux eq NAUX then break; end if;
end for;
assert #aux eq NAUX; assert #[i : i in aux | frob[i] eq i] ge 1;
evals := [];
for i in [1..nn] do
    orb := {i, frob[i], tau[i], frob[tau[i]]};
    if #(orb meet used) ne 0 then continue; end if;
    if #evals + #orb le NEV then evals cat:= Setseq(orb); used join:= orb; end if;
    if #evals eq NEV then break; end if;
end for;
assert #evals eq NEV;
efrob := [Index(evals, frob[i]) : i in evals]; etau := [Index(evals, tau[i]) : i in evals];
function MonValue(exps, x)
    return &*[x[i]^exps[i] : i in [1..16]];
end function;
oddM := Transpose(Matrix(k4, oddint));
V1all := ZeroMatrix(k4, nn, 81);
ellc := [k4!(k!c) : c in branch_parameter_linear_form];
for i in [1..nn] do
    x := plist[i]; xs := x[1..16];
    lv := &+[ellc[j]*xs[j] : j in [1..16]];
    ev2 := [MonValue(e, xs) : e in exps2];
    odd := Vector(k4, [MonValue(e, xs) : e in exps3])*oddM;
    vals := ev2 cat [x[17]/lv*c : c in Eltseq(odd)];
    for j in [1..81] do V1all[i,j] := vals[j]; end for;
end for;
V1 := Matrix([V1all[i] : i in evals]);
assert Rank(V1) eq 81;
function IndependentIndices(M)
    ech := EchelonForm(Transpose(M)); out := [];
    for v in Rows(ech) do
        if v eq 0 then continue; end if;
        Append(~out, Min([j : j in [1..Ncols(ech)] | v[j] ne 0]));
    end for;
    return out;
end function;
pairs2 := [[i,j] : i, j in [1..81] | i le j];
products := Matrix(k4, [[V1[r,pr[1]]*V1[r,pr[2]] : r in [1..NEV]] : pr in pairs2]);
ind := IndependentIndices(products); assert #ind eq 201;
pairs2 := [pairs2[i] : i in ind];
V2all := Matrix(k4, [[V1all[r,pr[1]]*V1all[r,pr[2]] : pr in pairs2] : r in [1..nn]]);
V2 := Matrix([V2all[i] : i in evals]); assert Rank(V2) eq 201;
delete products;
pairs3 := []; prod3 := ZeroMatrix(k4, 0, NEV);
for i in [1..81] do
    newpairs := [[i,j] : j in [1..201]];
    cand := Matrix(k4, [[V1[r,pr[1]]*V2[r,pr[2]] : r in [1..NEV]] : pr in newpairs]);
    both := VerticalJoin(prod3, cand); allpairs := pairs3 cat newpairs;
    ind := IndependentIndices(both);
    pairs3 := [allpairs[j] : j in ind]; prod3 := Matrix([both[j] : j in ind]);
    assert #pairs3 le 321;
    if #pairs3 eq 321 then break; end if;
end for;
assert #pairs3 eq 321; V3 := Transpose(prod3);
printf "S03|ranks V1, V2, V3 = 81, 201, 321 [%o s]\n", Cputime(started);

// W+- = L(2 D0 - B - D+-).
Wcoeffs := [* *]; Ws := [* *];
for branch in branchvals do
    bv := [branch[pr[1]]*branch[pr[2]] : pr in pairs2];
    bm := Transpose(Matrix(k4, [[Coefficient(UA!v, i) : i in [0..8]] : v in bv]));
    constraints := VerticalJoin(Matrix([V2all[i] : i in aux]), bm);
    assert Rank(constraints) eq 120;
    ker := Matrix(Basis(Nullspace(Transpose(constraints))));
    assert Nrows(ker) eq 81;
    ww := V2*Transpose(ker); assert Rank(ww) eq 81;
    Append(~Wcoeffs, ker); Append(~Ws, ww);
end for;
assert &and[V1[efrob[i],j] eq V1[i,j]^q : i in [1..NEV], j in [1..81]];
signs := [k4!1 : i in [1..45]] cat [k4!-1 : i in [1..36]];
assert &and[V1[etau[i],j] eq signs[j]*V1[i,j] : i in [1..NEV], j in [1..81]];
V1 := Transpose(V1); V2 := Transpose(V2); V3 := Transpose(V3);
WP := Transpose(Ws[1]); WM := Transpose(Ws[2]);
printf "S03|branch spaces W+, W- built; Frobenius and involution actions pass [%o s]\n", Cputime(started);

load "makdisi_lib.m";
ok := EqualClass(WP, WM); assert not ok;
ok := ZeroClass(V1); assert ok;
assert EqualClass(FrobeniusClass(WP), WP) and EqualClass(FrobeniusClass(WM), WM);
D := ChordClass(NegClass(WP), WM);
ok := ZeroClass(D); assert not ok;
assert EqualClass(FrobeniusClass(D), D);
minusD := NegClass(D);
assert EqualClass(DeckClass(D), minusD);
assert ZeroClass(AddClass(D, minusD));
tripleD := AddClass(ChordClass(minusD, minusD), D);
printf "S03|Delta nonzero, F_q-rational, anti-invariant; killed by three: %o [%o s]\n", ZeroClass(tripleD), Cputime(started);

function Enc(c)
    return Seqint([Integers()!e : e in Eltseq(c)], p);
end function;
function EncM(M)
    return [[Enc(M[i,j]) : j in [1..Ncols(M)]] : i in [1..Nrows(M)]];
end function;
PrintFile(STATE, Sprintf("st_p := %o;\nst_modulus := %o;\nst_sqrt_minus3 := %o;", p, [Integers()!c : c in Coefficients(DefiningPolynomial(k4))], Enc(s3)) : Overwrite := true);
PrintFile(STATE, Sprintf("st_points := %o;", [[Enc(c) : c in x] : x in plist]));
PrintFile(STATE, Sprintf("st_frob := %o;\nst_tau := %o;\nst_aux := %o;\nst_evals := %o;", frob, tau, aux, evals));
PrintFile(STATE, Sprintf("st_exps2 := %o;\nst_exps3 := %o;\nst_oddrows := %o;", exps2, exps3, oddint));
PrintFile(STATE, Sprintf("st_pairs2 := %o;\nst_pairs3 := %o;", pairs2, pairs3));
PrintFile(STATE, Sprintf("st_branch_plus := %o;\nst_branch_minus := %o;", [[Enc(Coefficient(UA!v, i)) : i in [0..8]] : v in branchvals[1]], [[Enc(Coefficient(UA!v, i)) : i in [0..8]] : v in branchvals[2]]));
PrintFile(STATE, Sprintf("st_WP := %o;\nst_WM := %o;\nst_Delta := %o;", EncM(WP), EncM(WM), EncM(D)));
printf "S03|state written [%o s]\n", Cputime(started);
print "PASS|03_COVER_CLASS";
quit;
