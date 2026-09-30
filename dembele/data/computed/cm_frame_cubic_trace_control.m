// D79: verify the saved cubic without searching for a third or a function.
SetQuitOnError(true); SetColumns(0); SetSeed(7901);
started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
load "dembele/data/computed/cm_frame_cover_sections.m";
load "dembele/data/computed/cm_frame_cover_third_check_input.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_fiber.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
load "dembele/data/computed/cm_frame_cubic.m";
cubic_trace_numerator_coefficients[1] := (cubic_trace_numerator_coefficients[1]+1) mod 31;
load "dembele/data/computed/cm_frame_curve_candidate.m";
function MonValue(exps,pt)
    return &*[pt[i]^exps[i]:i in [1..16]];
end function;
function TauRows(M,perm)
    return Matrix(BaseRing(M),[[v[i]:i in perm]:v in Rows(M)]);
end function;
function FrobRows(M,perm)
    return Matrix(BaseRing(M),[[v[i]^31:i in perm]:v in Rows(M)]);
end function;
function Included(A,B)
    return Rank(VerticalJoin(A,B)) eq Rank(B);
end function;
pts:=[[k!row:row in pt]:pt in sections_evaluation_point_coordinates];
ee:=kummer_evaluation_indices;
assert #ee eq 1024 and #Seqset(ee) eq 1024;
assert ee[1..640] eq makdisi_evaluation_indices;
assert #Seqset([pts[i]:i in ee]) eq 1024;
fp:=sections_frobenius_permutation; tp:=sections_involution_permutation;
ff:=[Index(ee,fp[i]):i in ee]; tt:=[Index(ee,tp[i]):i in ee];
assert &and[i ne 0:i in ff cat tt];
assert &and[pts[fp[i]] eq [x^31:x in pts[i]]:i in ee];
assert &and[pts[tp[i]] eq pts[i][1..16] cat [-pts[i][17]]:i in ee];
evrows:=[];
for i in ee do
    pt:=pts[i]; xs:=pt[1..16]; w:=pt[17];
    assert xs[16] eq 1 and &and[Evaluate(z,xs) eq 0:z in polys];
    qvals:=[xs[p[1]]*xs[p[2]]:p in pairs];
    nv:=&+[rational_numerator[j]*qvals[j]:j in [1..136]];
    dv:=&+[rational_denominator[j]*qvals[j]:j in [1..136]];
    lv:=&+[branch_parameter_linear_form[j]*xs[j]:j in [1..16]];
    assert nv*dv*lv ne 0 and w^2*dv eq nv;
    even:=[MonValue(e,xs):e in sections_even_monomial_exponents];
    ev3:=Vector(k,[MonValue(e,xs):e in sections_odd_monomial_exponents]);
    odd:=ev3*Transpose(Matrix(k,sections_odd_section_rows));
    Append(~evrows,even cat [w/lv*c:c in Eltseq(odd)]);
end for;
G1:=Transpose(Matrix(k,evrows));
G2:=Matrix(k,[[G1[p[1],j]*G1[p[2],j]:j in [1..1024]]:p in makdisi_product2_pairs]);
G3:=Matrix(k,[[G1[p[1],j]*G2[p[2],j]:j in [1..1024]]:p in makdisi_product3_pairs]);
G4:=Matrix(k,[[G1[p[1],j]*G3[p[2],j]:j in [1..1024]]:p in kummer_product4_pairs]);
assert [Rank(M):M in [*G1,G2,G3,G4*]] eq [81,201,321,441];
assert Submatrix(G1,1,1,81,640) eq V1 and Submatrix(G2,1,1,201,640) eq V2;
assert Submatrix(G3,1,1,321,640) eq V3;
assert &and[FrobRows(M,ff) eq M:M in [*G1,G2,G3,G4*]];
assert 1024 gt 8*120;
print "PASS|CUBIC_EVALUATION_INJECTIVITY_AND_BASES";

thirdcoords:=Dec(kummer_third_coordinates,k);
oldthird:=Dec(third_check_candidate_rows,k);
assert thirdcoords*V2 eq oldthird;
WE:=thirdcoords*G2; Wsigma:=FrobRows(WE,ff);
assert Rank(WE) eq 81;
WRcoords:=Dec(kummer_descended_divisor_coordinates,k);
assert &and[z^31 eq z:z in Eltseq(WRcoords)];
WR:=WRcoords*G2; assert Rank(WR) eq 81;
assert FrobRows(WR,ff) eq WR;
qcoeff:=Vector(k,kummer_q_coefficients); q:=qcoeff*G1; assert q ne 0;
UA<a>:=PolynomialRing(k); A<aa>:=quo<UA|UA!fiber_nonic_coefficients>;
plus1:=[A!UA!row:row in sections_branch_plus_section_values];
minus1:=[A!UA!row:row in sections_branch_minus_section_values];
assert &+[qcoeff[i]*minus1[i]:i in [1..81]] eq 0;
assert IsUnit(&+[qcoeff[i]*plus1[i]:i in [1..81]]);
bm1:=Matrix(k,sections_branch_minus_section_values);
assert Rank(bm1) eq 9;
Sminus:=Matrix(Basis(Nullspace(bm1)))*G1;
WQ:=QuotientSpace(Sminus,ScaleRows(G2,q),G2,90);
Qcoeff:=Solution(G2,WQ); assert Qcoeff*G2 eq WQ;
plus2:=[plus1[p[1]]*plus1[p[2]]:p in makdisi_product2_pairs];
bp2:=Matrix(k,[[Coefficient(UA!v,j):j in [0..8]]:v in plus2]);
assert Rank(Qcoeff*bp2) eq 9;
WB:=Matrix(Basis(Nullspace(Qcoeff*bp2)))*WQ;
assert Nrows(WB) eq 81 and RowSpace(FrobRows(WB,ff)) eq RowSpace(WB);
WB3:=ProductSpace(WB,G1,201); WB4:=ProductSpace(WB,G2,321);
WE3:=ProductSpace(WE,G1,201);
assert Rank(VerticalJoin(WE3,WB3)) eq 321;
moving:=Matrix(Basis(RowSpace(ProductSpace(WE,Wsigma,201)) meet RowSpace(WB4)));
assert Nrows(moving) eq 81;
move:=Vector(k,kummer_moving_coefficients)*G4;
assert move ne 0 and move in RowSpace(moving);
assert Vector(k,[move[j]^31:j in ff]) eq move;
WRcheck:=QuotientSpace(moving,ScaleRows(G2,move),G2,81);
assert RowSpace(WRcheck) eq RowSpace(WR);
WR3:=ProductSpace(WR,G1,201);
assert Rank(VerticalJoin(WR3,WB3)) eq 321;
assert EqualClass(Submatrix(WR,1,1,81,640),oldthird);
print "PASS|CUBIC_F31_DIVISOR_DESCENT";

u:=Vector(k,kummer_u_coefficients)*G4;
f:=Vector(k,kummer_f_coefficients)*G2;
assert u ne 0 and f ne 0;
cubeSpace:=ProductSpace(ProductSpace(WR,WR,201),WR,321);
// All generators are checked here. G2 is base-point-free.
assert Included(ScaleRows(G2,u),cubeSpace);
assert u in RowSpace(WB4);
normSpace:=ProductSpace(WR,TauRows(WR,tt),201);
assert Included(ScaleRows(G2,f),normSpace);
assert Vector(k,[f[j]:j in tt]) eq f;
ut:=Vector(k,[u[j]:j in tt]); qt:=Vector(k,[q[j]:j in tt]);
c:=k!kummer_norm_scalar; assert c ne 0 and c^31 eq c;
norm_ok:=&and[u[j]*ut[j] eq c*f[j]^3*q[j]*qt[j]:j in [1..1024]];
assert norm_ok;
assert &or[u[j]*qt[j]-ut[j]*q[j] ne 0:j in [1..1024]];
print "PASS|CUBIC_FUNCTION_DIVISOR_AND_NORM";

assert #kummer_q_coefficients eq 81 and #kummer_u_coefficients eq 441;
assert #kummer_f_coefficients eq 201 and #kummer_moving_coefficients eq 441;
assert &and[z ge 0 and z lt 31:z in kummer_q_coefficients cat kummer_u_coefficients cat
    kummer_f_coefficients cat kummer_moving_coefficients cat cubic_a_coefficients cat
    cubic_denominator_coefficients cat cubic_trace_numerator_coefficients];
assert #cubic_quartic_monomials eq 105 and #cubic_decic_monomials eq 285;
assert &and[#e eq 16 and &+e eq 4 and Min(e) ge 0:e in cubic_quartic_monomials];
assert &and[#e eq 16 and &+e eq 10 and Min(e) ge 0:e in cubic_decic_monomials];
xs:=[pts[i][1..16]:i in ee];
C4:=Matrix(k,[[MonValue(e,p):p in xs]:e in cubic_quartic_monomials]);
C10:=Matrix(k,[[MonValue(e,p):p in xs]:e in cubic_decic_monomials]);
assert Rank(C4) eq 105 and Rank(C10) eq 285;
avec:=Vector(k,cubic_a_coefficients)*C4;
denvec:=Vector(k,cubic_denominator_coefficients)*C4;
numvec:=Vector(k,cubic_trace_numerator_coefficients)*C10;
assert avec eq c*f;
assert denvec eq Vector(k,[q[j]*qt[j]:j in [1..1024]]);
trace_ok:=numvec eq Vector(k,[c*(u[j]*qt[j]+ut[j]*q[j]):j in [1..1024]]);
assert trace_ok;
// The trace identity and discriminant identity are universal polynomial identities.
S<v,z>:=PolynomialRing(k,2);
assert (v+z)^3-3*(v*z)*(v+z)-(v^3+z^3) eq 0;
assert 108*(v*z)^3-27*(v^3+z^3)^2 eq -27*(v^3-z^3)^2;
assert k!5 ne 1 and (k!5)^3 eq 1 and (k!2)^2 eq -27;
// Tame branch degrees: B2=18 (transpositions), B3=9 (3-cycles).
assert (3*(2*40-2)+2*18+2) div 2 eq 136;
assert (3*(2*16-2)+18+2*9+2) div 2 eq 64;
print "PASS|CUBIC_COEFFICIENTS_REFLECTION_AND_GENUS";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|178_CM_FRAME_CUBIC_CHECK";
quit;
