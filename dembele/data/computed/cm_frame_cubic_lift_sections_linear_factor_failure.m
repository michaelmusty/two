// D81: genuine sections and evaluation points modulo 31^2.
SetQuitOnError(true); SetColumns(0); SetSeed(81); started:=Cputime();
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_veronese.m";
load "dembele/data/computed/cm_frame_B3_fiber.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
load "dembele/data/computed/cm_frame_cover_sections.m";
load "dembele/data/computed/cm_frame_cover_makdisi.m";
load "dembele/data/computed/cm_frame_cubic.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function Quad(row,mon) return &+[row[i]*mon[i]:i in [1..#mon]]; end function;
ell:=&+[branch_parameter_linear_form[i]*R.i:i in [1..16]];
IB3:=IC+ideal<R|B3_linear_forms>;
IU:=Saturation(ColonIdeal(IC+ideal<R|ell>,IB3));
IE:=Saturation(IC+ideal<R|[Quad(row,mon):row in rational_E_quadrics_F31]>);
assert Degree(Scheme(P,IE)) eq 18 and Degree(Scheme(P,IU)) eq 21;
assert IsReduced(Scheme(P,IE)) and IsReduced(Scheme(P,IU));
assert Dimension(IE+IU) eq 0;
vd:=Quad(veronese_section_rows[2],mon); va:=Quad(veronese_section_rows[4],mon);
assert vd in IE and Dimension(IE+ideal<R|va>) eq 0;

function Support(J,P,R,polys)
    kk:=BaseRing(R); degree:=Degree(Scheme(P,J));
    assert Dimension(J+ideal<R|R.16>) eq 0;
    S:=PolynomialRing(kk,15,"grevlex");
    ia:=ideal<S|[Evaluate(f,[S.i:i in [1..15]] cat [S!1]):f in Basis(J)]>;
    L:=PolynomialRing(kk,15,"lex"); il:=ideal<L|[L!f:f in GroebnerBasis(ia)]>;
    gl:=GroebnerBasis(il); assert #gl eq 15;
    U<t>:=PolynomialRing(kk);
    h:=Evaluate(gl[#gl],[U!0:i in [1..14]] cat [t]); h/:=LeadingCoefficient(h);
    assert Degree(h) eq degree and Degree(GCD(h,Derivative(h))) eq 0;
    cs:=[Evaluate(NormalForm(L.i,il),[U!0:j in [1..14]] cat [t]):i in [1..15]] cat [U!1];
    assert &and[Evaluate(f,cs) mod h eq 0:f in polys];
    return h,cs;
end function;
eh,ec:=Support(IE,P,R,polys); uh,uc:=Support(IU,P,R,polys);
print "PASS|LIFT_ODD_SUPPORTS_18_AND_21";

Z:=Integers(961); PZ:=PolynomialRing(Z,16);
zm:=[PZ.(p[1])*PZ.(p[2]):p in pairs];
curveZ:=[Quad(row,zm):row in rows];
ellZ:=&+[Z!branch_parameter_linear_form[i]*PZ.i:i in [1..16]];
vdZ:=Quad([Z!Numerator(c)/(Z!Denominator(c)):c in veronese_section_rows[2]],zm);
vfZ:=Quad([Z!Numerator(c)/(Z!Denominator(c)):c in veronese_section_rows[1]],zm);
vaZ:=Quad([Z!Numerator(c)/(Z!Denominator(c)):c in veronese_section_rows[4]],zm);
numZ:=Quad(rational_numerator,zm); denZ:=Quad(rational_denominator,zm);
function LiftElt(x,A)
    return A![Integers()!c:c in Eltseq(x)];
end function;
function ReduceElt(x,kk)
    return kk![Integers()!c:c in Eltseq(x)];
end function;
function Residual(x,kk)
    cs:=[Integers()!c:c in Eltseq(x)]; assert &and[c mod 31 eq 0:c in cs];
    return kk![c div 31:c in cs];
end function;
function PivotColumns(M)
    E:=EchelonForm(M); return [Min([j:j in [1..Ncols(E)]|E[i,j] ne 0]):i in [1..Rank(M)]];
end function;
// Hensel lift a smooth isolated point of 15 equations in the X16=1 chart.
function LiftIsolated(point,cut,curve,A,kk)
    init:=[LiftElt(x,A):x in point]; equations:=curve cat [cut];
    jac:=Matrix(kk,[[ReduceElt(Evaluate(Derivative(f,j),init),kk):j in [1..15]]:f in equations]);
    selected:=PivotColumns(Transpose(jac)); assert #selected eq 15;
    small:=Submatrix(jac,selected,[1..15]);
    rhs:=Vector(kk,[-Residual(Evaluate(equations[i],init),kk):i in selected]);
    correction:=Eltseq(Solution(Transpose(small),rhs)) cat [kk!0];
    point2:=[init[i]+31*LiftElt(correction[i],A):i in [1..16]];
    assert &and[Evaluate(f,point2) eq 0:f in equations];
    return point2,selected;
end function;
UQ<tq>:=PolynomialRing(Integers()); components:=[* *];
constraints:=ZeroMatrix(Z,75,0);
for side in [1,2] do
    h:=side eq 1 select eh else uh; cs:=side eq 1 select ec else uc;
    cut:=side eq 1 select vdZ else ellZ;
    for factor in Factorization(h) do
        hh:=factor[1]; degree:=Degree(hh); assert factor[2] eq 1;
        kk<aa>:=ext<GF(31)|hh>;
        A<bb>:=GaloisRing(31,2,UQ![Integers()!c:c in Coefficients(hh)]);
        pt:=[Evaluate(c,aa):c in cs];
        pt2,selected:=LiftIsolated(pt,cut,curveZ,A,kk);
        if side eq 1 then
            assert IsUnit(Evaluate(vaZ,pt2)) and Evaluate(vfZ,pt2) eq 0;
            assert IsUnit(Evaluate(numZ,pt2));
        end if;
        values:=[&*[pt2[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
        block:=Matrix(Z,[[Z!c:c in Eltseq(v)]:v in values]);
        assert Ncols(block) eq degree; constraints:=HorizontalJoin(constraints,block);
        Append(~components,<side,[Integers()!c:c in Coefficients(hh)],
            [[Integers()!c:c in Eltseq(v)]:v in pt2],selected>);
    end for;
end for;
assert Ncols(constraints) eq 39;
oldodd:=Matrix(GF(31),sections_odd_section_rows);
piv:=PivotColumns(oldodd); assert #piv eq 36 and Submatrix(oldodd,[1..36],piv) eq IdentityMatrix(GF(31),36);
rest:=[j:j in [1..75]|not j in piv];
dep:=Submatrix(constraints,rest,[1..39]); assert IsUnit(Determinant(dep));
sol:=-Submatrix(constraints,piv,[1..39])*dep^-1;
odd2:=ZeroMatrix(Z,36,75);
for i in [1..36] do
    odd2[i,piv[i]]:=1;
    for j in [1..39] do odd2[i,rest[j]]:=sol[i,j]; end for;
end for;
assert odd2*constraints eq 0 and ChangeRing(odd2,GF(31)) eq oldodd;
print "PASS|ODD_SECTION_BASIS_LIFT_MOD961";

// Lift one representative of each Frobenius/deck orbit, then transport it.
kk<b>:=ext<GF(31)|PolynomialRing(GF(31))!sections_evaluation_field_modulus>;
A<bb>:=GaloisRing(31,2,UQ!sections_evaluation_field_modulus);
function Sigma(x,A)
    cs:=Eltseq(x); return A!cs[1]+(A!cs[2])*(-29-A.1);
end function;
oldpts:=[[kk!row:row in pt]:pt in sections_evaluation_point_coordinates];
fp:=sections_frobenius_permutation; tp:=sections_involution_permutation;
indices:=kummer_evaluation_indices cat makdisi_auxiliary_indices;
wanted:=Seqset(indices); assignedpts:=AssociativeArray();
for idx in indices do
    if IsDefined(assignedpts,idx) then continue; end if;
    pt:=oldpts[idx]; init:=[LiftElt(x,A):x in pt[1..16]];
    jac:=Matrix(kk,[[ReduceElt(Evaluate(Derivative(f,j),init),kk):j in [1..15]]:f in curveZ]);
    deps:=PivotColumns(jac); assert #deps eq 14;
    selected:=PivotColumns(Transpose(Submatrix(jac,[1..91],deps)));
    small:=Submatrix(jac,selected,deps);
    rhs:=Vector(kk,[-Residual(Evaluate(curveZ[i],init),kk):i in selected]);
    corr:=Eltseq(Solution(Transpose(small),rhs)); xs:=init;
    for j in [1..14] do xs[deps[j]]+:=31*LiftElt(corr[j],A); end for;
    assert &and[Evaluate(f,xs) eq 0:f in curveZ];
    w:=LiftElt(pt[17],A); nv:=Evaluate(numZ,xs); dv:=Evaluate(denZ,xs);
    assert IsUnit(w*nv*dv*Evaluate(ellZ,xs));
    w-:=(w^2*dv-nv)/(2*w*dv); assert w^2*dv eq nv;
    lifted:=xs cat [w];
    labels:=[idx,fp[idx],tp[idx],fp[tp[idx]]];
    values:=[lifted,[Sigma(x,A):x in lifted],xs cat [-w],
        [Sigma(x,A):x in xs] cat [-Sigma(w,A)]];
    for j in [1..4] do
        assert [ReduceElt(x,kk):x in values[j]] eq oldpts[labels[j]];
        if IsDefined(assignedpts,labels[j]) then assert assignedpts[labels[j]] eq values[j]; end if;
        assignedpts[labels[j]]:=values[j];
    end for;
end for;
liftedpts:=[assignedpts[i]:i in indices];
assert &and[pt[16] eq 1:pt in liftedpts];
print "PASS|EVALUATION_POINT_LIFT_MOD961";

// The branch algebra and regular W values are already known over Q.
UZ<az>:=PolynomialRing(Z); AZ<za>:=quo<UZ|UZ![Z!Numerator(c)/(Z!Denominator(c)):c in fiber_nonic_coefficients]>;
bpt:=[AZ!UZ![Z!Numerator(c)/(Z!Denominator(c)):c in row]:row in fiber_point_coordinates];
root:=Z!11; root-:=(root^2+3)/(2*root); assert root^2 eq -3;
wr:=root*(AZ!UZ![Z!Numerator(c)/(Z!Denominator(c)):c in branch_branch_ratio]);
assert &and[Evaluate(f,bpt) eq 0:f in curveZ] and bpt[16] eq 1;
b2:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_even_monomial_exponents];
b3:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
bo:=[&+[odd2[i,j]*b3[j]:j in [1..75]]:i in [1..36]];
bp:=b2 cat [wr*x:x in bo]; bm:=b2 cat [-wr*x:x in bo];
branchplus:=[[Integers()!Coefficient(UZ!v,j):j in [0..8]]:v in bp];
branchminus:=[[Integers()!Coefficient(UZ!v,j):j in [0..8]]:v in bm];
assert [[x mod 31:x in row]:row in branchplus] eq sections_branch_plus_section_values;
assert [[x mod 31:x in row]:row in branchminus] eq sections_branch_minus_section_values;
printf "LIFT_MODULUS|961\n";
printf "LIFT_ODD_SECTION_ROWS|%o\n",[[Integers()!c:c in Eltseq(v)]:v in Rows(odd2)];
printf "LIFT_ODD_SUPPORT_COMPONENTS|%o\n",components;
printf "LIFT_POINT_INDICES|%o\n",indices;
printf "LIFT_POINT_COORDINATES|%o\n",[[[Integers()!c:c in Eltseq(x)]:x in pt]:pt in liftedpts];
printf "LIFT_BRANCH_PLUS_VALUES|%o\n",branchplus;
printf "LIFT_BRANCH_MINUS_VALUES|%o\n",branchminus;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|184_CM_FRAME_CUBIC_LIFT_SECTIONS";
quit;
