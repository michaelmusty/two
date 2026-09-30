// D84 specialization of dembele/magma/180_cm_frame_cubic_point_count.m; SHA256 fff71d0eefbd901f69b83bb54f668485817bcefb37a5f648c03cb550c4bbb8f0
// D80: count the normalized cubic over F31 or F31^2, resolving exceptional fibres.
SetQuitOnError(true); SetColumns(0); SetSeed(80);
if not assigned extension_degree then extension_degree:=1; end if;
assert extension_degree in [1,2];
started:=Cputime();
U0<s>:=PolynomialRing(GF(31));
k:=extension_degree eq 1 select GF(31) else ext<GF(31)|s^2+29*s+3>;
function Enc(c)
    cs:=Eltseq(c); return &+[Integers()!cs[i]*31^(i-1):i in [1..#cs]];
end function;
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
load "dembele/data/computed/cm_frame_cover_sections.m";
load "dembele/data/computed/cm_frame_cover_makdisi.m";
load "/Users/musty/two/dembele/data/computed/cm_frame_alternative_cover_0_2_3_data.m";
function Monomial(e,R)
    return &*[R.i^e[i]:i in [1..16]];
end function;
function Form(row,mons)
    return &+[row[i]*mons[i]:i in [1..#mons]];
end function;
m4:=[Monomial(e,R):e in cubic_quartic_monomials];
m10:=[Monomial(e,R):e in cubic_decic_monomials];
A4:=Form(cubic_a_coefficients,m4); Q4:=Form(cubic_denominator_coefficients,m4);
P10:=Form(cubic_trace_numerator_coefficients,m10);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
num:=Form(rational_numerator,mon); den:=Form(rational_denominator,mon);
ell:=&+[branch_parameter_linear_form[i]*R.i:i in [1..16]];
even:=[Monomial(e,R):e in sections_even_monomial_exponents];
oddmons:=[Monomial(e,R):e in sections_odd_monomial_exponents];
odd:=[Form(row,oddmons):row in sections_odd_section_rows];
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
assert Dimension(IC+ideal<R|R.15,R.16>) eq 0;
// D84: reuse D80's complete, independently certified base point list.
points:=[[extension_degree eq 1 select k!c else k!(c mod 31)+k.1*(c div 31):c in row]:row in point_count_base_points];
assert #points eq (extension_degree eq 1 select 50 else 1400);
assert #Seqset([Eltseq(C_candidate!p):p in points]) eq #points;
assert &and[Evaluate(z,p) eq 0:z in polys,p in points];

// A certified unit Jacobian minor gives a smooth local parameter.
function LocalCoordinates(pt,polys,R,prec)
    kk:=BaseRing(R); anchor:=Min([i:i in [1..16]|pt[i] ne 0]);
    pt:=[x/pt[anchor]:x in pt]; vars:=[i:i in [1..16]|i ne anchor];
    J:=Matrix(kk,[[Evaluate(Derivative(z,j),pt):j in vars]:z in polys]);
    assert Rank(J) eq 14;
    inds:=[]; rowlist:=[];
    for i in [1..#polys] do
        trial:=rowlist cat [Eltseq(J[i])];
        if Rank(Matrix(kk,trial)) gt #rowlist then
            Append(~rowlist,Eltseq(J[i])); Append(~inds,i);
        end if;
        if #inds eq 14 then break; end if;
    end for;
    found:=false; parameter:=0;
    for candidate in vars do
        deps:=[j:j in vars|j ne candidate];
        mat:=Matrix(kk,[[Evaluate(Derivative(polys[i],j),pt):j in deps]:i in inds]);
        if Determinant(mat) ne 0 then found:=true; parameter:=candidate; break; end if;
    end for;
    assert found;
    PS<t>:=PowerSeriesRing(kk,prec);
    xs:=[PS!x+O(t^prec):x in pt]; xs[parameter]+:=t;
    for n in [1..prec-1] do
        rhs:=Vector(kk,[-Coefficient(Evaluate(polys[i],xs),n):i in inds]);
        corr:=Solution(Transpose(mat),rhs);
        for j in [1..14] do xs[deps[j]]+:=corr[j]*t^n; end for;
    end for;
    assert &and[Evaluate(z,xs) eq 0:z in polys];
    return xs,anchor,parameter;
end function;

U<T>:=PolynomialRing(k); total:=0; counts:=[0,0,0,0]; rows:=[];
exceptional:=0; branch:=0;
for idx in [1..#points] do
    pt:=points[idx];
    assert not &and[Evaluate(z,pt) eq 0:z in B3_linear_forms];
    assert not &and[Evaluate(z,pt) eq 0:z in D17_extra_quadrics];
    if C_candidate!pt eq P32_candidate then
        // Transposition inertia has normalizer itself: both inertia orbits are rational.
        amount:=2; branch+:=1; mode:=1; val:=0; unit:=k!0;
    else
        av:=Evaluate(A4,pt); qv:=Evaluate(Q4,pt); pv:=Evaluate(P10,pt);
        if qv ne 0 and 108*av^3-27*(pv/qv)^2 ne 0 then
            f:=T^3-3*av*T-pv/qv;
            assert GCD(f,Derivative(f)) eq 1;
            amount:=#Roots(f); mode:=0; val:=0; unit:=k!0;
        else
            exceptional+:=1; xs,anchor,parameter:=LocalCoordinates(pt,polys,R,32);
            LS<t>:=LaurentSeriesRing(k,32); xs:=[LS!x:x in xs];
            ns:=Evaluate(num,xs); ds:=Evaluate(den,xs);
            assert ns ne 0 and ds ne 0;
            ratio:=ns/ds; v2:=Valuation(ratio);
            assert v2 mod 2 eq 0;
            lead:=Coefficient(ratio,v2); split,r:=IsSquare(lead);
            if not split then
                // Frobenius is a transposition in S3: exactly one fixed sheet.
                amount:=1; mode:=2; val:=v2; unit:=lead;
            else
                sq:=LS!r+O(t^AbsolutePrecision(ratio/t^v2));
                for iteration in [1..6] do sq:=(sq+(ratio/t^v2)/sq)/2; end for;
                w:=t^(v2 div 2)*sq; assert w^2 eq ratio;
                lv:=Evaluate(ell,xs); assert lv ne 0 and xs[16] ne 0;
                vals1:=[Evaluate(z,xs)/xs[16]^2:z in even] cat
                    [w*Evaluate(z,xs)/(lv*xs[16]^2):z in odd];
                vals2:=[vals1[p[1]]*vals1[p[2]]:p in makdisi_product2_pairs];
                vals3:=[vals1[p[1]]*vals2[p[2]]:p in makdisi_product3_pairs];
                vals4:=[vals1[p[1]]*vals3[p[2]]:p in kummer_product4_pairs];
                q:=&+[kummer_q_coefficients[j]*vals1[j]:j in [1..81]];
                u:=&+[kummer_u_coefficients[j]*vals4[j]:j in [1..441]];
                assert q ne 0 and u ne 0;
                h:=kummer_norm_scalar*u/q; val:=Valuation(h);
                assert val mod 3 eq 0 and AbsolutePrecision(h) gt val;
                unit:=Coefficient(h,val); assert unit ne 0;
                amount:=unit^((#k-1) div 3) eq 1 select 3 else 0; mode:=3;
                printf "LOCAL_JET|%o|%o|%o|%o|%o\n",idx,anchor,parameter,v2,val;
            end if;
        end if;
    end if;
    total+:=amount; counts[amount+1]+:=1;
    Append(~rows,[idx,mode,amount,val,Enc(unit)]);
end for;
assert branch eq 1 and &+counts eq #points;
Z<z>:=PolynomialRing(Integers());
bank:=eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
cp40:=Z!bank[2]; cp48:=Z!bank[3];
fs:=[a[1]:a in Factorization(cp40)|Degree(a[1]) eq 4];
assert #fs eq 4 and Degree(cp48) eq 48;
cp64:=(&*fs)*cp48; assert Degree(cp64) eq 64;
trace1:=-Coefficient(cp64,63);
trace2:=Coefficient(cp64,63)^2-2*(Coefficient(cp64,62)+64*31);
expected:=#k+1-(extension_degree eq 1 select trace1 else trace2);
printf "EXTENSION_DEGREE|%o\n",extension_degree;
printf "BASE_POINTS|%o\n",[[Enc(c):c in p]:p in points];
printf "CUBIC_FIBER_COUNTS|%o\n",rows;
printf "FIBER_COUNT_DISTRIBUTION|%o\n",counts;
printf "EXCEPTIONAL_FIBERS|%o\n",exceptional;
printf "CUBIC_POINT_COUNT|%o\n",total;
printf "HECKE_EXPECTED_POINT_COUNT|%o\n",expected;
printf "HECKE_COUNT_MATCH|%o\n",total eq expected;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|180_CM_FRAME_CUBIC_POINT_COUNT";
quit;
