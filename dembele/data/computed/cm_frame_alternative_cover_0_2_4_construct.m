// D84 specialization of dembele/magma/176_cm_frame_kummer_function.m; SHA256 185592c4d823c3f97f53d270c628f8e55e88060b2a40ac6e83fc5467b0794f6f
// D79: descend the third's representative and construct the Kummer function.
SetQuitOnError(true); SetColumns(0); SetSeed(79);
started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/data/computed/cm_frame_cover_sections.m";
load "/Users/musty/two/dembele/data/computed/cm_frame_alternative_cover_0_2_4_third.m";
load "dembele/data/computed/cm_frame_B3_fiber.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
oldthird:=Dec(third_check_candidate_rows,k);
thirdcoords:=Solution(V2,oldthird); assert thirdcoords*V2 eq oldthird;
pts:=[[k!row:row in pt]:pt in sections_evaluation_point_coordinates];
fp:=sections_frobenius_permutation; tp:=sections_involution_permutation;
indices:=makdisi_evaluation_indices; used:=Seqset(indices);
for i in [1..#pts] do
    orb:={i,fp[i],tp[i],fp[tp[i]]};
    if #(orb meet used) ne 0 then continue; end if;
    if #indices+#orb le 1024 then indices cat:=Setseq(orb); used join:=orb; end if;
    if #indices eq 1024 then break; end if;
end for;
assert #indices eq 1024 and #Seqset(indices) eq 1024;
ff:=[Index(indices,fp[i]):i in indices]; tt:=[Index(indices,tp[i]):i in indices];
assert &and[i ne 0:i in ff cat tt];
function FrobRows(M,perm)
    return Matrix(BaseRing(M),[[v[i]^31:i in perm]:v in Rows(M)]);
end function;
function TauRows(M,perm)
    return Matrix(BaseRing(M),[[v[i]:i in perm]:v in Rows(M)]);
end function;
function MonValue(exps,pt)
    return &*[pt[i]^exps[i]:i in [1..16]];
end function;
evrows:=[];
for i in indices do
    pt:=pts[i]; xs:=pt[1..16];
    lv:=&+[branch_parameter_linear_form[j]*xs[j]:j in [1..16]];
    ev2:=[MonValue(e,xs):e in sections_even_monomial_exponents];
    ev3:=Vector(k,[MonValue(e,xs):e in sections_odd_monomial_exponents]);
    odd:=ev3*Transpose(Matrix(k,sections_odd_section_rows));
    Append(~evrows,ev2 cat [pt[17]/lv*c:c in Eltseq(odd)]);
end for;
G1:=Transpose(Matrix(k,evrows));
G2:=Matrix(k,[[G1[p[1],r]*G1[p[2],r]:r in [1..1024]]:p in makdisi_product2_pairs]);
G3:=Matrix(k,[[G1[p[1],r]*G2[p[2],r]:r in [1..1024]]:p in makdisi_product3_pairs]);
assert Submatrix(G1,1,1,81,640) eq V1 and Submatrix(G2,1,1,201,640) eq V2;
assert Submatrix(G3,1,1,321,640) eq V3;
function IndependentIndices(M)
    e:=EchelonForm(Transpose(M)); out:=[];
    for v in Rows(e) do
        if v ne 0 then Append(~out,Min([j:j in [1..Ncols(e)]|v[j] ne 0])); end if;
    end for;
    return out;
end function;
G4:=ZeroMatrix(k,0,1024); pairs4:=[];
for i in [1..81] do
    np:=[[i,j]:j in [1..321]];
    cand:=ScaleRows(G3,G1[i]); both:=VerticalJoin(G4,cand); pp:=pairs4 cat np;
    ii:=IndependentIndices(both); G4:=Matrix([both[j]:j in ii]); pairs4:=[pp[j]:j in ii];
    assert #pairs4 le 441;
    if #pairs4 eq 441 then break; end if;
end for;
assert Rank(G4) eq 441;
print "PASS|EXPANDED_EVALUATION_THROUGH_EIGHT_D0";

WE:=thirdcoords*G2; Wsigma:=FrobRows(WE,ff);
WE3:=ProductSpace(WE,G1,201);
UA<a>:=PolynomialRing(k); A<aa>:=quo<UA|UA!fiber_nonic_coefficients>;
plus1:=[A!UA!row:row in sections_branch_plus_section_values];
minus1:=[A!UA!row:row in sections_branch_minus_section_values];
plus2:=[plus1[p[1]]*plus1[p[2]]:p in makdisi_product2_pairs];
bp2:=Matrix(k,[[Coefficient(UA!v,j):j in [0..8]]:v in plus2]);
bm1:=Matrix(k,sections_branch_minus_section_values);
qker:=Matrix(Basis(Nullspace(bm1))); assert Nrows(qker) eq 72;
Sminus:=qker*G1;
qfound:=false;
for trial in [1..16] do
    qcoeff:=Vector(k,[k!Random(GF(31)):i in [1..72]])*qker;
    qplus:=&+[qcoeff[i]*plus1[i]:i in [1..81]];
    if not IsUnit(qplus) then continue; end if;
    q:=qcoeff*G1;
    WQ:=QuotientSpace(Sminus,ScaleRows(G2,q),G2,90);
    Qcoeff:=Solution(G2,WQ); assert Qcoeff*G2 eq WQ;
    bker:=Matrix(Basis(Nullspace(Qcoeff*bp2))); assert Nrows(bker) eq 81;
    WB:=bker*WQ;
    WB3:=ProductSpace(WB,G1,201);
    if Rank(VerticalJoin(WE3,WB3)) ne 321 then continue; end if;
    qfound:=true; break;
end for;
assert qfound;
assert RowSpace(FrobRows(WB,ff)) eq RowSpace(WB);
WB4:=ProductSpace(WB,G2,321);
traceSpace:=ProductSpace(WE,Wsigma,201);
moving:=Matrix(Basis(RowSpace(traceSpace) meet RowSpace(WB4)));
assert Nrows(moving) eq 81;
movingcoeff:=Matrix(Basis(RowSpace(Solution(G4,moving))));
assert &and[c^31 eq c:c in Eltseq(movingcoeff)];
moving:=movingcoeff*G4;
efound:=false;
for trial in [1..16] do
    move_coeff:=Vector(k,[k!Random(GF(31)):i in [1..81]])*movingcoeff;
    move:=move_coeff*G4;
    if move eq 0 then continue; end if;
    WR:=QuotientSpace(moving,ScaleRows(G2,move),G2,81);
    WR3:=ProductSpace(WR,G1,201);
    if Rank(VerticalJoin(WR3,WB3)) ne 321 then continue; end if;
    efound:=true; break;
end for;
assert efound;
assert RowSpace(FrobRows(WR,ff)) eq RowSpace(WR);
assert EqualClass(Submatrix(WR,1,1,81,640),oldthird);
WRcoords:=Matrix(Basis(RowSpace(Solution(G2,WR))));
assert &and[c^31 eq c:c in Eltseq(WRcoords)];
WR:=WRcoords*G2;
print "PASS|F31_EFFECTIVE_REPRESENTATIVE_OF_THIRD";

// q has divisor D-+Q-D0; B=D++Q. Recover u with divisor 3E+B-4D0.
cubeSpace:=ProductSpace(ProductSpace(WR,WR,201),WR,321);
tripleVanishing:=QuotientSpace(G2,cubeSpace,G4,81);
uline:=Matrix(Basis(RowSpace(tripleVanishing) meet RowSpace(WB4)));
assert Nrows(uline) eq 1;
ucoeff:=Solution(G4,uline[1]);
pivot:=Min([j:j in [1..441]|ucoeff[j] ne 0]); ucoeff/:=ucoeff[pivot];
assert &and[c^31 eq c:c in Eltseq(ucoeff)];
u:=ucoeff*G4;
normSpace:=ProductSpace(WR,TauRows(WR,tt),201);
ok,f:=DegreeZeroQuotient(G2,normSpace,G2); assert ok;
fcoeff:=Solution(G2,f);
pivot:=Min([j:j in [1..201]|fcoeff[j] ne 0]); fcoeff/:=fcoeff[pivot];
assert &and[c^31 eq c:c in Eltseq(fcoeff)];
f:=fcoeff*G2;
assert Vector(k,[f[i]:i in tt]) eq f;
ut:=Vector(k,[u[i]:i in tt]); qt:=Vector(k,[q[i]:i in tt]);
good:=Min([j:j in [1..1024]|f[j]*q[j]*qt[j] ne 0]);
c:=u[good]*ut[good]/(f[good]^3*q[good]*qt[good]);
assert c ne 0 and c^31 eq c;
assert &and[u[j]*ut[j] eq c*f[j]^3*q[j]*qt[j]:j in [1..1024]];
assert &or[u[j]*qt[j]-ut[j]*q[j] ne 0:j in [1..1024]];
print "PASS|KUMMER_DIVISOR_AND_NORM_NORMALIZATION";

// The reflection quotient has y^3-3*a*y-btrace=0, a=c*f, h=c*u/q.
// Recover invariant coefficients as canonical forms on the base C.
load "dembele/data/computed/cm_frame_curve_candidate.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC); LM:=[LeadingMonomial(z):z in GC];
FB:=[R!1]; layer:=[R!1];
repeat
    layer:=Setseq({m*R.i:m in layer,i in [1..14]|not &or[IsDivisibleBy(m*R.i,l):l in LM]});
    FB cat:=layer;
until #layer eq 0;
Sort(~FB); assert #FB eq 30;
function CanonMons(deg,FB,R)
    return &cat[[m*R.15^j*R.16^(deg-TotalDegree(m)-j):j in [0..deg-TotalDegree(m)]]:m in FB];
end function;
base4:=CanonMons(4,FB,R); base10:=CanonMons(10,FB,R);
assert #base4 eq 105 and #base10 eq 285;
xs:=[pts[i][1..16]:i in indices];
C4:=Matrix(k,[[Evaluate(m,p):p in xs]:m in base4]);
C10:=Matrix(k,[[Evaluate(m,p):p in xs]:m in base10]);
assert Rank(C4) eq 105 and Rank(C10) eq 285;
avec:=c*f;
denvec:=Vector(k,[q[j]*qt[j]:j in [1..1024]]);
numvec:=Vector(k,[c*(u[j]*qt[j]+ut[j]*q[j]):j in [1..1024]]);
arow:=Solution(C4,avec); denrow:=Solution(C4,denvec); numrow:=Solution(C10,numvec);
assert arow*C4 eq avec and denrow*C4 eq denvec and numrow*C10 eq numvec;
assert &and[z^31 eq z:z in Eltseq(arow) cat Eltseq(denrow) cat Eltseq(numrow)];
printf "KUMMER_EVALUATION_INDICES|%o\n",indices;
printf "KUMMER_PRODUCT4_PAIRS|%o\n",pairs4;
printf "KUMMER_THIRD_COORDINATES|%o\n",EncRows(thirdcoords);
printf "KUMMER_DESCENDED_DIVISOR_COORDINATES|%o\n",EncRows(WRcoords);
printf "KUMMER_MOVING_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(move_coeff)];
printf "KUMMER_Q_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(qcoeff)];
printf "KUMMER_U_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(ucoeff)];
printf "KUMMER_F_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(fcoeff)];
printf "KUMMER_NORM_SCALAR|%o\n",Integers()!(GF(31)!c);
printf "CUBIC_QUARTIC_MONOMIALS|%o\n",[Exponents(m):m in base4];
printf "CUBIC_DECIC_MONOMIALS|%o\n",[Exponents(m):m in base10];
printf "CUBIC_A_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(arow)];
printf "CUBIC_DENOMINATOR_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(denrow)];
printf "CUBIC_TRACE_NUMERATOR_COEFFICIENTS|%o\n",[Integers()!(GF(31)!z):z in Eltseq(numrow)];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|176_CM_FRAME_KUMMER_FUNCTION";
quit;
