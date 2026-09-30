// D84 specialization of dembele/magma/182_cm_frame_cubic_point_check.m; SHA256 75f5c32bbae81b7186644befc2c6c5b7385d05bbb38a9743f5c6e572aa415a63
// D80: verify each saved fibre via quadratic/Kummer splitting, not cubic roots.
SetQuitOnError(true); SetColumns(0); SetSeed(8001);
if not assigned extension_degree then extension_degree:=1; end if;
started:=Cputime(); U0<s>:=PolynomialRing(GF(31));
k:=extension_degree eq 1 select GF(31) else ext<GF(31)|s^2+29*s+3>;
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
load "dembele/data/computed/cm_frame_cover_sections.m";
load "dembele/data/computed/cm_frame_cover_makdisi.m";
load "/Users/musty/two/dembele/data/computed/cm_frame_alternative_cover_0_2_7_data.m";
// The runner loads the degree-specific saved point list before this script.
assert point_count_extension_degree eq extension_degree;
function Dec(c,k)
    return Degree(k) eq 1 select k!c else k!(c mod 31)+k.1*(c div 31);
end function;
points:=[[Dec(c,k):c in row]:row in point_count_base_points];
// Completeness follows from D69's independently certified base point counts.
assert #points eq (extension_degree eq 1 select 50 else 1400);
assert #Seqset([Eltseq(C_candidate!p):p in points]) eq #points;
assert &and[Evaluate(z,p) eq 0:z in polys,p in points];
function Monomial(e,R)
    return &*[R.i^e[i]:i in [1..16]];
end function;
function Form(row,mons)
    return &+[row[i]*mons[i]:i in [1..#mons]];
end function;
mon:=[R.(p[1])*R.(p[2]):p in pairs];
num:=Form(rational_numerator,mon); den:=Form(rational_denominator,mon);
ell:=&+[branch_parameter_linear_form[i]*R.i:i in [1..16]];
even:=[Monomial(e,R):e in sections_even_monomial_exponents];
oddmons:=[Monomial(e,R):e in sections_odd_monomial_exponents];
odd:=[Form(row,oddmons):row in sections_odd_section_rows];
function FunctionValues(xs,w,ell,even,odd,pairs2,pairs3,pairs4,qrow,urow)
    lv:=Evaluate(ell,xs);
    v1:=[Evaluate(z,xs)/xs[16]^2:z in even] cat
        [w*Evaluate(z,xs)/(lv*xs[16]^2):z in odd];
    v2:=[v1[p[1]]*v1[p[2]]:p in pairs2];
    v3:=[v1[p[1]]*v2[p[2]]:p in pairs3];
    v4:=[v1[p[1]]*v3[p[2]]:p in pairs4];
    return &+[qrow[j]*v1[j]:j in [1..81]],&+[urow[j]*v4[j]:j in [1..441]];
end function;

// Use the last nonzero anchor and reverse variable order, unlike constructor 180.
function LocalCoordinates(pt,polys,R)
    kk:=BaseRing(R); anchor:=Max([i:i in [1..16]|pt[i] ne 0]);
    pt:=[x/pt[anchor]:x in pt]; vars:=Reverse([i:i in [1..16]|i ne anchor]);
    J:=Matrix(kk,[[Evaluate(Derivative(z,j),pt):j in vars]:z in polys]);
    assert Rank(J) eq 14; inds:=[]; rows:=[];
    for i in Reverse([1..#polys]) do
        if Rank(Matrix(kk,rows cat [Eltseq(J[i])])) gt #rows then
            Append(~rows,Eltseq(J[i])); Append(~inds,i);
        end if;
        if #inds eq 14 then break; end if;
    end for;
    parameter:=0;
    for candidate in vars do
        deps:=[j:j in vars|j ne candidate];
        M:=Matrix(kk,[[Evaluate(Derivative(polys[i],j),pt):j in deps]:i in inds]);
        if Determinant(M) ne 0 then parameter:=candidate; break; end if;
    end for;
    assert parameter ne 0; inv:=Transpose(M)^-1;
    PS<t>:=PowerSeriesRing(kk,24); xs:=[PS!x+O(t^24):x in pt]; xs[parameter]+:=t;
    for n in [1..23] do
        rhs:=Vector(kk,[-Coefficient(Evaluate(polys[i],xs),n):i in inds]); corr:=rhs*inv;
        for j in [1..14] do xs[deps[j]]+:=corr[j]*t^n; end for;
    end for;
    assert &and[Evaluate(z,xs) eq 0:z in polys];
    return xs;
end function;

total:=0; jets:=0; split_count:=0; nonsplit_count:=0; branch_count:=0;
for idx in [1..#points] do
    pt:=points[idx];
    assert not &and[Evaluate(z,pt) eq 0:z in B3_linear_forms];
    assert not &and[Evaluate(z,pt) eq 0:z in D17_extra_quadrics];
    if C_candidate!pt eq P32_candidate then
        amount:=2; branch_count+:=1;
    else
        nv:=Evaluate(num,pt); dv:=Evaluate(den,pt); lv:=Evaluate(ell,pt);
        done:=false;
        if nv*dv ne 0 then
            split,w:=IsSquare(nv/dv);
            if not split then
                amount:=1; nonsplit_count+:=1; done:=true;
            elif lv*pt[16] ne 0 then
                q,u:=FunctionValues(pt,w,ell,even,odd,makdisi_product2_pairs,
                    makdisi_product3_pairs,kummer_product4_pairs,kummer_q_coefficients,kummer_u_coefficients);
                if q*u ne 0 then
                    h:=kummer_norm_scalar*u/q;
                    amount:=h^((#k-1) div 3) eq 1 select 3 else 0;
                    split_count+:=1; done:=true;
                end if;
            end if;
        end if;
        if not done then
            jets+:=1; ys:=LocalCoordinates(pt,polys,R);
            LS<t>:=LaurentSeriesRing(k,24); xs:=[LS!y:y in ys];
            ns:=Evaluate(num,xs); ds:=Evaluate(den,xs); assert ns ne 0 and ds ne 0;
            ratio:=ns/ds; v:=Valuation(ratio); assert v mod 2 eq 0;
            split,r:=IsSquare(Coefficient(ratio,v));
            if not split then
                amount:=1; nonsplit_count+:=1;
            else
                unit:=ratio/t^v; sq:=LS!r+O(t^AbsolutePrecision(unit));
                for iteration in [1..6] do sq:=(sq+unit/sq)/2; end for;
                w:=sq*t^(v div 2); assert w^2 eq ratio;
                q,u:=FunctionValues(xs,w,ell,even,odd,makdisi_product2_pairs,
                    makdisi_product3_pairs,kummer_product4_pairs,kummer_q_coefficients,kummer_u_coefficients);
                assert q ne 0 and u ne 0;
                h:=kummer_norm_scalar*u/q; vh:=Valuation(h);
                assert vh mod 3 eq 0 and AbsolutePrecision(h) gt vh;
                lead:=Coefficient(h,vh); assert lead ne 0;
                amount:=lead^((#k-1) div 3) eq 1 select 3 else 0; split_count+:=1;
            end if;
        end if;
    end if;
    fiber_ok:=amount eq point_count_fiber_counts[idx][3];
    assert fiber_ok;
    total+:=amount;
end for;
assert total eq point_count_expected_total;
assert branch_count eq 1 and branch_count+split_count+nonsplit_count eq #points;
printf "CHECKED_EXTENSION_DEGREE|%o\n",extension_degree;
printf "CHECKED_POINT_COUNT|%o\n",total;
printf "QUADRATIC_SPLITTING_COUNTS|%o\n",[split_count,nonsplit_count,branch_count];
printf "INDEPENDENT_LOCAL_JET_COUNT|%o\n",jets;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|182_CM_FRAME_CUBIC_POINT_CHECK";
quit;
