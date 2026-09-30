// D78: genus-40 Makdisi evaluation spaces and representatives of D+ and D-.
SetQuitOnError(true); SetColumns(0); SetSeed(78);
started:=Cputime();
load "dembele/data/computed/cm_frame_cover_sections.m";
load "dembele/data/computed/cm_frame_B3_fiber.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
U<t>:=PolynomialRing(GF(31));
k<b>:=ext<GF(31)|U!sections_evaluation_field_modulus>;
pts:=[[k!row:row in pt]:pt in sections_evaluation_point_coordinates];
nn:=#pts; frob:=sections_frobenius_permutation; tau:=sections_involution_permutation;

// A common degree-111 auxiliary divisor, stable under Frobenius.
aux:=[]; used:={Integers()|};
for i in [1..nn] do
    if i in used then continue; end if;
    orb:=Setseq({i,frob[i]});
    if #aux+#orb le 111 then aux cat:=orb; used join:=Seqset(orb); end if;
    if #aux eq 111 then break; end if;
end for;
assert #aux eq 111;
// At least 601 distinct evaluation points ensure injectivity through 5D0.
evals:=[];
for i in [1..nn] do
    orb:={i,frob[i],tau[i],frob[tau[i]]};
    if #(orb meet used) ne 0 then continue; end if;
    if #evals+#orb le 640 then evals cat:=Setseq(orb); used join:=orb; end if;
    if #evals eq 640 then break; end if;
end for;
assert #evals eq 640;
efrob:=[Index(evals,frob[i]):i in evals]; etau:=[Index(evals,tau[i]):i in evals];
assert &and[i ne 0:i in efrob cat etau];
function MonValue(exps,pt)
    return &*[pt[i]^exps[i]:i in [1..16]];
end function;
V1all:=ZeroMatrix(k,nn,81);
for i in [1..nn] do
    pt:=pts[i]; xs:=pt[1..16];
    lv:=&+[branch_parameter_linear_form[j]*xs[j]:j in [1..16]];
    assert xs[16] eq 1 and lv ne 0;
    ev2:=[MonValue(e,xs):e in sections_even_monomial_exponents];
    ev3:=Vector(k,[MonValue(e,xs):e in sections_odd_monomial_exponents]);
    odd:=ev3*Transpose(Matrix(k,sections_odd_section_rows));
    vals:=ev2 cat [pt[17]/lv*c:c in Eltseq(odd)];
    for j in [1..81] do V1all[i,j]:=vals[j]; end for;
end for;
V1:=Matrix([V1all[i]:i in evals]);
assert Rank(V1) eq 81;
printf "V1_RANK|%o\n",Rank(V1);

function IndependentIndices(M)
    echelon:=EchelonForm(Transpose(M));
    out:=[];
    for v in Rows(echelon) do
        if v eq 0 then continue; end if;
        Append(~out,Min([j:j in [1..Ncols(echelon)]|v[j] ne 0]));
    end for;
    return out;
end function;
pairs2:=[[i,j]:i,j in [1..81]|i le j];
products:=Matrix(k,[[V1[r,p[1]]*V1[r,p[2]]:r in [1..640]]:p in pairs2]);
ind:=IndependentIndices(products); assert #ind eq 201;
pairs2:=[pairs2[i]:i in ind];
V2all:=Matrix(k,[[V1all[r,p[1]]*V1all[r,p[2]]:p in pairs2]:r in [1..nn]]);
V2:=Matrix([V2all[i]:i in evals]); assert Rank(V2) eq 201;
printf "V2_RANK|%o\n",Rank(V2);
delete products;

pairs3:=[]; prod3:=ZeroMatrix(k,0,640);
for i in [1..81] do
    newpairs:=[[i,j]:j in [1..201]];
    cand:=Matrix(k,[[V1[r,p[1]]*V2[r,p[2]]:r in [1..640]]:p in newpairs]);
    both:=VerticalJoin(prod3,cand); allpairs:=pairs3 cat newpairs;
    ind:=IndependentIndices(both);
    pairs3:=[allpairs[j]:j in ind]; prod3:=Matrix([both[j]:j in ind]);
    assert #pairs3 le 321;
    if #pairs3 eq 321 then break; end if;
end for;
assert #pairs3 eq 321; V3:=Transpose(prod3);
printf "V3_RANK|%o\n",Rank(V3);

// Impose the degree-111 common divisor and the nine conditions at D+/-.
UA<a>:=PolynomialRing(k); A<aa>:=quo<UA|UA!fiber_nonic_coefficients>;
Wcoeffs:=[* *]; Ws:=[* *];
for values in [sections_branch_plus_section_values,sections_branch_minus_section_values] do
    branch:=[A!UA!row:row in values];
    bv:=[branch[p[1]]*branch[p[2]]:p in pairs2];
    bm:=Transpose(Matrix(k,[[Coefficient(UA!v,i):i in [0..8]]:v in bv]));
    constraints:=VerticalJoin(Matrix([V2all[i]:i in aux]),bm);
    assert Rank(constraints) eq 120;
    ker:=Matrix(Basis(Nullspace(Transpose(constraints))));
    assert Nrows(ker) eq 81 and ker*Transpose(constraints) eq 0;
    ww:=V2*Transpose(ker); assert Rank(ww) eq 81;
    Append(~Wcoeffs,ker); Append(~Ws,ww);
end for;

// Check field action and deck involution on the full section spaces.
signs:=[k!1:i in [1..45]] cat [k!-1:i in [1..36]];
assert &and[V1[efrob[i],j] eq V1[i,j]^31:i in [1..640],j in [1..81]];
assert &and[V1[etau[i],j] eq signs[j]*V1[i,j]:i in [1..640],j in [1..81]];
function Enc(c)
    return Integers()!Eltseq(c)[1]+31*(Integers()!Eltseq(c)[2]);
end function;
function EncMatrix(M)
    return [[Enc(M[i,j]):j in [1..Ncols(M)]]:i in [1..Nrows(M)]];
end function;
printf "AUXILIARY_INDICES|%o\n",aux;
printf "EVALUATION_INDICES|%o\n",evals;
printf "EVALUATION_FROBENIUS|%o\n",efrob;
printf "EVALUATION_INVOLUTION|%o\n",etau;
printf "PRODUCT2_PAIRS|%o\n",pairs2;
printf "PRODUCT3_PAIRS|%o\n",pairs3;
printf "PLUS_COEFFICIENT_ROWS|%o\n",EncMatrix(Wcoeffs[1]);
printf "MINUS_COEFFICIENT_ROWS|%o\n",EncMatrix(Wcoeffs[2]);
printf "V1_EVALUATIONS|%o\n",EncMatrix(V1);
printf "V2_EVALUATIONS|%o\n",EncMatrix(V2);
printf "V3_EVALUATIONS|%o\n",EncMatrix(V3);
printf "PLUS_EVALUATIONS|%o\n",EncMatrix(Ws[1]);
printf "MINUS_EVALUATIONS|%o\n",EncMatrix(Ws[2]);
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|166_CM_FRAME_COVER_MAKDISI";
quit;
