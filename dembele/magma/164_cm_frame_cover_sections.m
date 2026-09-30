// D78: exact sections and evaluation points on the genus-40 cover over F31.
// D0=pi^*(2K_C), degree 120. This constructs arithmetic input, not a cubic.
SetQuitOnError(true); SetColumns(0); SetSeed(78);
started:=Cputime(); k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_fiber.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
LM:=[LeadingMonomial(q):q in GC];
mons2:=[m:m in MonomialsOfDegree(R,2)|not &or[IsDivisibleBy(m,l):l in LM]];
mons3:=[m:m in MonomialsOfDegree(R,3)|not &or[IsDivisibleBy(m,l):l in LM]];
assert #mons2 eq 45 and #mons3 eq 75;
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function Quad(row,mon)
    return &+[row[j]*mon[j]:j in [1..#mon]];
end function;
ell:=&+[branch_parameter_linear_form[i]*R.i:i in [1..16]];
IB3:=IC+ideal<R|B3_linear_forms>;
IU:=Saturation(ColonIdeal(IC+ideal<R|ell>,IB3));
IE:=Saturation(IC+ideal<R|[Quad(row,mon):row in rational_E_quadrics_F31]>);
assert Degree(Scheme(P,IU)) eq 21 and Degree(Scheme(P,IE)) eq 18;
assert Dimension(IU+IB3) eq 0;
// If E and U meet, vanishing at their sum requires the product ideal.
IJ:=Saturation(IE*IU+IC);
assert Degree(Scheme(P,IJ)) eq 39;
candidates:=[R|];
for q in GroebnerBasis(IJ) do
    e:=TotalDegree(q);
    if e le 3 then
        candidates cat:=[NormalForm(q*m,IC):m in MonomialsOfDegree(R,3-e)];
    end if;
end for;
oddmat:=Matrix(k,[[MonomialCoefficient(q,m):m in mons3]:q in candidates]);
oddrows:=Basis(RowSpace(oddmat)); assert #oddrows eq 36;
oddpolys:=[&+[v[j]*mons3[j]:j in [1..75]]:v in oddrows];
assert &and[q in IJ:q in oddpolys];
assert Rank(Matrix(oddrows)) eq 36;
printf "SECTION_DIMENSIONS|%o\n",[45,36,81];
printf "EVEN_MONOMIAL_EXPONENTS|%o\n",[Exponents(m):m in mons2];
printf "ODD_MONOMIAL_EXPONENTS|%o\n",[Exponents(m):m in mons3];
printf "ODD_SECTION_ROWS|%o\n",[[Integers()!c:c in Eltseq(v)]:v in oddrows];
printf "SECTION_CPU_SECONDS|%o\n",Cputime(started);

// The branch values use the regular coordinate W=w/(ell/X16), not w=0.
U<a>:=PolynomialRing(k); f:=U!fiber_nonic_coefficients;
A<aa>:=quo<U|f>;
bpt:=[A!U!row:row in fiber_point_coordinates];
wr:=11*(A!U!branch_branch_ratio);
evplus:=[Evaluate(q,bpt):q in mons2] cat [wr*Evaluate(q,bpt):q in oddpolys];
evminus:=[Evaluate(q,bpt):q in mons2] cat [-wr*Evaluate(q,bpt):q in oddpolys];
printf "BRANCH_PLUS_SECTION_VALUES|%o\n",[[Integers()!Coefficient(U!v,i):i in [0..8]]:v in evplus];
printf "BRANCH_MINUS_SECTION_VALUES|%o\n",[[Integers()!Coefficient(U!v,i):i in [0..8]]:v in evminus];

// Collect good evaluation points in Frobenius and involution orbits.
// All lie in X16=1 away from ell*n*d=0, hence on a smooth etale chart.
k<b>:=GF(31,2);
load "dembele/data/computed/cm_frame_curve_candidate.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
n:=Quad(rational_numerator,mon); den:=Quad(rational_denominator,mon);
ell:=&+[branch_parameter_linear_form[i]*R.i:i in [1..16]];
seen:={k|}; points:={@ @}; checked:=0;
for a in k do
    if a in seen then continue; end if;
    orb:={a,a^31}; seen join:=orb;
    S:=Scheme(P,IC+ideal<R|R.15-a*R.16>);
    assert Dimension(S) eq 0 and Degree(S) eq 30;
    pts:=Points(S); checked+:=1;
    for p in pts do
        xs:=Eltseq(p); assert xs[16] ne 0;
        xs:=[c/xs[16]:c in xs];
        nv:=Evaluate(n,xs); dv:=Evaluate(den,xs); lv:=Evaluate(ell,xs);
        if nv*dv*lv eq 0 then continue; end if;
        ok,w:=IsSquare(nv/dv);
        if not ok then continue; end if;
        assert &and[Evaluate(q,xs) eq 0:q in polys];
        for ww in [w,-w] do
            pt:=xs cat [ww]; Include(~points,pt);
            Include(~points,[c^31:c in pt]);
        end for;
    end for;
    if checked mod 80 eq 0 then
        printf "EVALUATION_PROGRESS|%o|%o|%o\n",checked,#points,Cputime(started);
    end if;
end for;
assert #points gt 751;
plist:=Setseq(points);
frob:=[Index(points,[c^31:c in pt]):pt in plist];
involution:=[Index(points,pt[1..16] cat [-pt[17]]):pt in plist];
assert &and[frob[frob[i]] eq i and involution[involution[i]] eq i:i in [1..#points]];
assert &and[frob[involution[i]] eq involution[frob[i]]:i in [1..#points]];
printf "EVALUATION_FIELD_MODULUS|%o\n",[Integers()!c:c in Coefficients(DefiningPolynomial(k))];
printf "GOOD_POINT_COUNT|%o\n",#points;
printf "EVALUATION_POINT_COORDINATES|%o\n",[[[Integers()!c:c in Eltseq(v)]:v in pt]:pt in plist];
printf "FROBENIUS_PERMUTATION|%o\n",frob;
printf "INVOLUTION_PERMUTATION|%o\n",involution;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|164_CM_FRAME_COVER_SECTIONS";
quit;
