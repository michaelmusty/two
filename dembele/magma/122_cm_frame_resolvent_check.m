// D71: verify a supplied quadratic square class independently of its discovery.
// No Hecke cardinality assumption or scalar multiplication is used here.
SetColumns(0); SetSeed(71); SetQuitOnError(true);
started := Cputime(); k := GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
IC := Ideal(C_candidate); GC := GroebnerBasis(IC);
mon := [R.(p[1])*R.(p[2]) : p in resolvent_pairs];
function Quadric(row,mon)
    return &+[row[j]*mon[j] : j in [1..#mon]];
end function;
qn := Quadric(resolvent_numerator,mon);
qd := Quadric(resolvent_denominator,mon);
Eqs := [Quadric(row,mon) : row in resolvent_E_quadrics];
IE := Saturation(IC+ideal<R|Eqs>);
IE2 := Saturation(IC+ideal<R|[q*r : q,r in Eqs]>);
assert Dimension(IE) eq 1 and Degree(Scheme(P,IE)) eq 16;
assert Dimension(IE2) eq 1 and Degree(Scheme(P,IE2)) eq 32;
assert Saturation(IC+ideal<R|Eqs>) eq IE;

// Recheck the supplied exact jets, including the implicit-function condition.
PS<t> := PowerSeriesRing(k,16);
xs := [(&+[PS!resolvent_point_jets[n+1][j]*t^n : n in [0..15]])+O(t^16) : j in [1..16]];
pt := Eltseq(P32_candidate);
assert [Coefficient(x,0) : x in xs] eq [p/pt[1] : p in pt];
assert xs[1] eq 1 and xs[16]-Coefficient(xs[16],0) eq t;
assert &and[Evaluate(q,xs) eq 0 : q in polys];
dependent := [2..15];
Jac := Matrix(k,[[Evaluate(Derivative(q,j),[p/pt[1] : p in pt])
                 : j in dependent] : q in polys]);
assert Rank(Jac) eq 14;
jets := Matrix(k,[[Coefficient(Evaluate(q,xs),n) : q in mon] : n in [0..14]]);
ker := Basis(Nullspace(Transpose(jets)));
IP15 := Saturation(ideal<R|[Quadric(Eltseq(v),mon) : v in ker]>);
IP := ideal<R|[R.i-pt[i]/pt[1]*R.1 : i in [2..16]]>;
assert Dimension(IP15) eq 1 and Degree(Scheme(P,IP15)) eq 15;
assert Dimension(IE+IP) eq 0;
assert Dimension(D17_ideal+IP) eq 0;
ID32 := D17_ideal meet IP15;
assert Degree(Scheme(P,ID32)) eq 32;
assert qn in ID32 and not qn in IC;
IF := Saturation(ColonIdeal(IC+ideal<R|qn>,ID32));
assert Degree(Scheme(P,IF)) eq 28;
assert Dimension(IF+ID32) eq 0;
assert Dimension(IF+IE2) eq 0;
assert Saturation(IC+ideal<R|qn>) eq (ID32 meet IF);
assert Saturation(IC+ideal<R|qd>) eq (IE2 meet IF);
printf "DIVISOR_IDENTITY|D17 + 15*P32 - 2*E\n";
printf "E_DEGREE|%o\n", Degree(Scheme(P,IE));
printf "ODD_BRANCH_DEGREE|18\n";
printf "DOUBLE_COVER_GENUS|40\n";

// All F31-rational points, using D69's unramified degree-30 projection.
pts := [];
for a in k do
    fiber := Scheme(P,IC+ideal<R|R.15-a*R.16>);
    assert Degree(fiber) eq 30 and Dimension(fiber) eq 0;
    pts cat:= [Eltseq(p) : p in Points(fiber)];
end for;
pts cat:= [Eltseq(p) : p in Points(Scheme(P,IC+ideal<R|R.16>))];
assert #pts eq 50;

// Formal coordinates through order 7, used only when qn/qd is 0/0 or a pole.
// Linear equations are solved with fixed unit Jacobian minor and all 91
// original equations are checked afterwards.
function LocalCoordinates(pt,polys,R)
    k := BaseRing(R); anchor := Min([i : i in [1..16] | pt[i] ne 0]);
    pt := [x/pt[anchor] : x in pt];
    vars := [i : i in [1..16] | i ne anchor];
    J := Matrix(k,[[Evaluate(Derivative(q,j),pt) : j in vars] : q in polys]);
    assert Rank(J) eq 14;
    inds := []; rowlist := [];
    for i in [1..#polys] do
        trial := rowlist cat [Eltseq(J[i])];
        if Rank(Matrix(k,trial)) gt #rowlist then
            Append(~rowlist,Eltseq(J[i])); Append(~inds,i);
        end if;
        if #inds eq 14 then break; end if;
    end for;
    good := false; parameter := 0; deps := []; A := ZeroMatrix(k,14,14);
    for j in vars do
        ds := [i : i in vars | i ne j];
        mat := Matrix(k,[[Evaluate(Derivative(polys[i],v),pt) : v in ds] : i in inds]);
        if Determinant(mat) ne 0 then
            good := true; parameter := j; deps := ds; A := mat; break;
        end if;
    end for;
    assert good;
    PS<t> := PowerSeriesRing(k,8); xs := [PS!x+O(t^8) : x in pt];
    xs[parameter] +:= t;
    for n in [1..7] do
        b := Vector(k,[-Coefficient(Evaluate(polys[i],xs),n) : i in inds]);
        correction := Solution(Transpose(A),b);
        for j in [1..14] do xs[deps[j]] +:= correction[j]*t^n; end for;
    end for;
    assert &and[Evaluate(q,xs) eq 0 : q in polys];
    return xs;
end function;

counts := [0,0]; ramified := 0; exceptional := 0;
nonsquare := PrimitiveElement(k); assert not IsSquare(nonsquare);
for pt in pts do
    if &and[Evaluate(q,pt) eq 0 : q in Basis(IP)] then
        counts := [c+1 : c in counts]; ramified +:= 1;
        printf "COVER_FIBER|%o|ramified|1|1\n", [Integers()!x : x in pt];
        continue;
    end if;
    // D17 is irreducible at 31; also exclude rational branch points directly.
    assert not &and[Evaluate(q,pt) eq 0 : q in D17_extra_quadrics];
    nv := Evaluate(qn,pt); dv := Evaluate(qd,pt);
    if nv ne 0 and dv ne 0 then
        unit := nv/dv; valuation := 0;
    else
        exceptional +:= 1; xs := LocalCoordinates(pt,polys,R);
        ns := Evaluate(qn,xs); ds := Evaluate(qd,xs);
        vn := Valuation(ns); vd := Valuation(ds);
        assert vn lt 8 and vd lt 8;
        valuation := vn-vd;
        assert valuation mod 2 eq 0;
        unit := Coefficient(ns,vn)/Coefficient(ds,vd);
    end if;
    n1 := IsSquare(unit) select 2 else 0;
    n2 := IsSquare(nonsquare*unit) select 2 else 0;
    assert n1+n2 eq 2;
    counts := [counts[1]+n1,counts[2]+n2];
    printf "COVER_FIBER|%o|%o|%o|%o\n", [Integers()!x : x in pt],valuation,n1,n2;
end for;
assert ramified eq 1 and &+counts eq 100;
printf "TWIST_NONSQUARE|%o\n", nonsquare;
printf "POINT_COUNTS|%o|%o\n", counts[1],counts[2];
printf "EXCEPTIONAL_FIBERS|%o\n", exceptional;
Z<z> := PolynomialRing(Integers());
bank := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
p40 := Z!bank[2]; assert Degree(p40) eq 40;
// Comparison with the norm-one genus-40 Shimura model, not identification.
printf "HECKE_EXPECTED_POINTS|%o\n", 32+Coefficient(p40,39);
printf "CPU_SECONDS|%o\n", Cputime(started);
print "PASS|122_CM_FRAME_RESOLVENT_CHECK";
quit;
