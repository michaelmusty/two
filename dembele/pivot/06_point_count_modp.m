// D158 step 2d: count points of the normalized genus-64 cubic over F_p
// (port of script 180, extension degree 1 only), resolving exceptional fibres.
// Files in the current directory: state_in.m, cubic_in.m (from script 05),
// the exact data files. Env: EXPECTED (Hecke prediction, compared only).
SetQuitOnError(true); SetColumns(0); SetSeed(80);
started := Cputime();
load "state_in.m";
load "cubic_in.m";
p := st_p; assert cub_p eq p;
k := GF(p);
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
load "cm_frame_B3_rational_model.m";
load "cm_frame_B3_fiber_structure.m";
function Monomial(e, R)
    return &*[R.i^e[i] : i in [1..16]];
end function;
function Form(row, mons)
    return &+[row[i]*mons[i] : i in [1..#mons]];
end function;
m4 := [Monomial(e, R) : e in cub_quartic_monomials];
m10 := [Monomial(e, R) : e in cub_decic_monomials];
A4 := Form(cub_A, m4); Q4 := Form(cub_den, m4); P10 := Form(cub_num, m10);
mon := [R.(pr[1])*R.(pr[2]) : pr in pairs];
num := Form(rational_numerator, mon); den := Form(rational_denominator, mon);
ell := &+[branch_parameter_linear_form[i]*R.i : i in [1..16]];
even := [Monomial(e, R) : e in st_exps2];
oddmons := [Monomial(e, R) : e in st_exps3];
odd := [Form(row, oddmons) : row in st_oddrows];
IC := Ideal(C_candidate); GC := GroebnerBasis(IC);
assert Dimension(IC + ideal<R | R.15, R.16>) eq 0;
pointset := {}; fibers := 0;
for a in k do
    S := Scheme(P, IC + ideal<R | R.15 - a*R.16>);
    assert Dimension(S) eq 0 and Degree(S) eq 30;
    pointset join:= {Eltseq(x) : x in Points(S)};
    fibers +:= 1;
    if fibers mod 100 eq 0 then
        printf "S06|fibres %o, points %o [%o s]\n", fibers, #pointset, Cputime(started);
    end if;
end for;
S := Scheme(P, IC + ideal<R | R.16>);
assert Dimension(S) eq 0 and Degree(S) eq 30;
pointset join:= {Eltseq(x) : x in Points(S)}; points := Setseq(pointset);
assert &and[Evaluate(z, x) eq 0 : z in polys, x in points];
printf "S06|#C(F_%o) = %o [%o s]\n", p, #points, Cputime(started);

// A certified unit Jacobian minor gives a smooth local parameter.
function LocalCoordinates(pt, polys, R, prec)
    kk := BaseRing(R); anchor := Min([i : i in [1..16] | pt[i] ne 0]);
    pt := [x/pt[anchor] : x in pt]; vars := [i : i in [1..16] | i ne anchor];
    J := Matrix(kk, [[Evaluate(Derivative(z, j), pt) : j in vars] : z in polys]);
    assert Rank(J) eq 14;
    inds := []; rowlist := [];
    for i in [1..#polys] do
        trial := rowlist cat [Eltseq(J[i])];
        if Rank(Matrix(kk, trial)) gt #rowlist then
            Append(~rowlist, Eltseq(J[i])); Append(~inds, i);
        end if;
        if #inds eq 14 then break; end if;
    end for;
    found := false; parameter := 0;
    for candidate in vars do
        deps := [j : j in vars | j ne candidate];
        mat := Matrix(kk, [[Evaluate(Derivative(polys[i], j), pt) : j in deps] : i in inds]);
        if Determinant(mat) ne 0 then found := true; parameter := candidate; break; end if;
    end for;
    assert found;
    PS<t> := PowerSeriesRing(kk, prec);
    xs := [PS!x + O(t^prec) : x in pt]; xs[parameter] +:= t;
    for n in [1..prec-1] do
        rhs := Vector(kk, [-Coefficient(Evaluate(polys[i], xs), n) : i in inds]);
        corr := Solution(Transpose(mat), rhs);
        for j in [1..14] do xs[deps[j]] +:= corr[j]*t^n; end for;
    end for;
    assert &and[Evaluate(z, xs) eq 0 : z in polys];
    return xs, anchor, parameter;
end function;

U<T> := PolynomialRing(k); total := 0; counts := [0,0,0,0];
exceptional := 0; branch := 0; b3pts := 0; d17pts := 0;
for idx in [1..#points] do
    pt := points[idx];
    onB3 := &and[Evaluate(z, pt) eq 0 : z in B3_linear_forms];
    onD17 := &and[Evaluate(z, pt) eq 0 : z in D17_extra_quadrics];
    if onB3 then
        // Total ramification (order-three inertia): one point above.
        assert not onD17; amount := 1; b3pts +:= 1;
    elif onD17 or C_candidate!pt eq P32_candidate then
        // Transposition inertia has normalizer itself: both inertia orbits are rational.
        amount := 2; branch +:= 1;
        if onD17 then d17pts +:= 1; end if;
    else
        av := Evaluate(A4, pt); qv := Evaluate(Q4, pt); pv := Evaluate(P10, pt);
        if qv ne 0 and 108*av^3 - 27*(pv/qv)^2 ne 0 then
            f := T^3 - 3*av*T - pv/qv;
            assert GCD(f, Derivative(f)) eq 1;
            amount := #Roots(f);
        else
            exceptional +:= 1; xs, anchor, parameter := LocalCoordinates(pt, polys, R, 32);
            LS<t> := LaurentSeriesRing(k, 32); xs := [LS!x : x in xs];
            ns := Evaluate(num, xs); ds := Evaluate(den, xs);
            assert ns ne 0 and ds ne 0;
            ratio := ns/ds; v2 := Valuation(ratio);
            assert v2 mod 2 eq 0;
            lead := Coefficient(ratio, v2); split, r := IsSquare(lead);
            if not split then
                // Frobenius is a transposition in S3: exactly one fixed sheet.
                amount := 1;
            else
                sq := LS!r + O(t^AbsolutePrecision(ratio/t^v2));
                for iteration in [1..6] do sq := (sq + (ratio/t^v2)/sq)/2; end for;
                w := t^(v2 div 2)*sq; assert w^2 eq ratio;
                lv := Evaluate(ell, xs); assert lv ne 0 and xs[16] ne 0;
                vals1 := [Evaluate(z, xs)/xs[16]^2 : z in even] cat
                    [w*Evaluate(z, xs)/(lv*xs[16]^2) : z in odd];
                vals2 := [vals1[pr[1]]*vals1[pr[2]] : pr in st_pairs2];
                vals3 := [vals1[pr[1]]*vals2[pr[2]] : pr in st_pairs3];
                vals4 := [vals1[pr[1]]*vals3[pr[2]] : pr in cub_pairs4];
                qq := &+[cub_q_coefficients[j]*vals1[j] : j in [1..81]];
                u := &+[cub_u_coefficients[j]*vals4[j] : j in [1..441]];
                assert qq ne 0 and u ne 0;
                h := cub_norm_scalar*u/qq; val := Valuation(h);
                assert val mod 3 eq 0 and AbsolutePrecision(h) gt val;
                unit := Coefficient(h, val); assert unit ne 0;
                amount := unit^((#k-1) div 3) eq 1 select 3 else 0;
                printf "S06|local jet at point %o: anchor %o, parameter %o, v2 %o, val %o\n", idx, anchor, parameter, v2, val;
            end if;
        end if;
    end if;
    total +:= amount; counts[amount+1] +:= 1;
end for;
assert branch eq 1 + d17pts and &+counts eq #points;
printf "S06|rational points on D17: %o, on B3: %o\n", d17pts, b3pts;
expected := StringToInteger(GetEnv("EXPECTED"));
printf "S06|fibre count distribution (0,1,2,3 points): %o; exceptional fibres %o\n", counts, exceptional;
printf "S06|cubic point count %o; Hecke prediction %o; match %o [%o s]\n", total, expected, total eq expected, Cputime(started);
print "DONE|06_POINT_COUNT";
quit;
