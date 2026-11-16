// Section values on X and branch data over Z/p^N. Requires padic_points.m and
// oddMN (75 x 36, the lifted odd cubics).
oddG := ChangeRing(oddMN, GG);
ellG := [GG!Q2Z(c) : c in branch_parameter_linear_form];
function Vals(x, w, top)
    lv := &+[ellG[j]*x[j] : j in [1..16]];
    odd := Eltseq(Matrix(GG, 1, 75, Mons(x, st_exps3))*oddG);
    wl := w*InvG(lv);
    v1 := Mons(x, st_exps2) cat [wl*c : c in odd];
    v2 := [v1[pr[1]]*v1[pr[2]] : pr in st_pairs2];
    if top eq 2 then return v1, v2, 0, 0; end if;
    v3 := [v1[pr[1]]*v2[pr[2]] : pr in st_pairs3];
    v4 := [v1[pr[1]]*v3[pr[2]] : pr in cub_pairs4];
    return v1, v2, v3, v4;
end function;
// Branch data over Z/p^N.
UA<a> := PolynomialRing(ZN);
fA := UA![Q2Z(c) : c in fiber_nonic_coefficients]; fA := fA*LeadingCoefficient(fA)^-1;
A<aa> := quo<UA | fA>;
function Coefs(v)
    s := Coefficients(UA!v); s cat:= [ZN!0 : i in [#s+1..9]];
    return s;
end function;
s3 := ZN!st_sqrt_minus3; e := 1;
while e lt N do s3 := (s3 - 3*s3^-1)*(ZN!2)^-1; e *:= 2; end while;
assert s3^2 eq ZN!-3;
bpt := [A!UA![Q2Z(c) : c in row] : row in fiber_point_coordinates];
wr := s3*(A!UA![Q2Z(c) : c in branch_branch_ratio]);
ev2b := Mons(bpt, st_exps2);
ev3b := Eltseq(Matrix(A, 1, 75, Mons(bpt, st_exps3))*ChangeRing(oddMN, A));
plus1 := ev2b cat [wr*v : v in ev3b]; minus1 := ev2b cat [-wr*v : v in ev3b];
bp1 := Matrix(ZN, [Coefs(v) : v in plus1]); bm1 := Matrix(ZN, [Coefs(v) : v in minus1]);
assert Red(bp1) eq Matrix(Fp, st_branch_plus) and Red(bm1) eq Matrix(Fp, st_branch_minus);
bp2 := Matrix(ZN, [Coefs(plus1[pr[1]]*plus1[pr[2]]) : pr in st_pairs2]);
minus2 := [minus1[pr[1]]*minus1[pr[2]] : pr in st_pairs2];
bm2 := Matrix(ZN, [Coefs(v) : v in minus2]);
