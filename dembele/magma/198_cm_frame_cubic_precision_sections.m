// D82: lift actual supports and points from the preceding saved precision.
// The wrapper loads cubic_lift_* at precision_previous_digits first.
SetQuitOnError(true); SetColumns(0); SetSeed(82198); started:=Cputime();
assert precision_digits gt precision_previous_digits;
old_modulus:=31^precision_previous_digits; new_modulus:=31^precision_digits;
assert cubic_lift_modulus eq old_modulus;
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_B3_veronese.m";
load "dembele/data/computed/cm_frame_B3_fiber.m";
load "dembele/data/computed/cm_frame_B3_fiber_structure.m";
load "dembele/data/computed/cm_frame_cover_sections.m";
Z:=Integers(new_modulus); PZ:=PolynomialRing(Z,16);
zm:=[PZ.(p[1])*PZ.(p[2]):p in pairs];
function Quad(row,mon)
    Z:=BaseRing(Parent(mon[1]));
    return &+[(Z!Numerator(row[i]))*(Z!Denominator(row[i]))^-1*mon[i]:i in [1..#mon]];
end function;
curveZ:=[Quad(row,zm):row in rows];
ellZ:=&+[branch_parameter_linear_form[i]*PZ.i:i in [1..16]];
vdZ:=Quad(veronese_section_rows[2],zm); vaZ:=Quad(veronese_section_rows[4],zm);
vfZ:=Quad(veronese_section_rows[1],zm);
numZ:=Quad(rational_numerator,zm); denZ:=Quad(rational_denominator,zm);
function Cs(x) return Type(x) eq RngIntResElt select [x] else Eltseq(x); end function;
function Red(x,F)
    cs:=[Integers()!z:z in Cs(x)];
    return Degree(F) eq 1 select F!cs[1] else F!cs;
end function;
function Lift(x,A)
    cs:=[Integers()!z:z in Eltseq(x)];
    return Type(A) eq RngIntRes select A!cs[1] else A!cs;
end function;
function Residual(x,F,power)
    cs:=[Integers()!z:z in Cs(x)]; assert &and[z mod power eq 0:z in cs];
    return Degree(F) eq 1 select F!(cs[1] div power) else F![z div power:z in cs];
end function;
function Pivots(M)
    E:=EchelonForm(M); return [Min([j:j in [1..Ncols(E)]|E[i,j] ne 0]):i in [1..Rank(M)]];
end function;
UQ<tq>:=PolynomialRing(Integers()); components:=[* *]; constraints:=ZeroMatrix(Z,75,0);
for component in cubic_lift_odd_support_components do
    side,hcoeff,coords,selected:=Explode(component); degree:=#hcoeff-1;
    F:=ext<GF(31)|PolynomialRing(GF(31))!hcoeff>;
    A:=degree eq 1 select Z else GaloisRing(31,precision_digits,UQ!hcoeff);
    pt:=degree eq 1 select [A!c[1]:c in coords] else [A!c:c in coords];
    equations:=curveZ cat [side eq 1 select vdZ else ellZ];
    jac:=Matrix(F,[[Red(Evaluate(Derivative(equations[i],j),pt),F):j in [1..15]]:i in selected]);
    assert Determinant(jac) ne 0; inv:=Transpose(jac)^-1;
    for digits in [precision_previous_digits..precision_digits-1] do
        power:=31^digits;
        rhs:=Vector(F,[-Residual(Evaluate(equations[i],pt),F,power):i in selected]);
        corr:=rhs*inv;
        for j in [1..15] do pt[j]+:=power*Lift(corr[j],A); end for;
    end for;
    assert &and[Evaluate(f,pt) eq 0:f in equations];
    assert [[(Integers()!z) mod old_modulus:z in Cs(x)]:x in pt] eq coords;
    if side eq 1 then
        assert IsUnit(Evaluate(vaZ,pt)) and IsUnit(Evaluate(numZ,pt));
        assert Evaluate(vfZ,pt) eq 0 and Evaluate(denZ,pt) eq 0;
    end if;
    vals:=[&*[pt[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
    constraints:=HorizontalJoin(constraints,Matrix(Z,[[Z!z:z in Cs(x)]:x in vals]));
    Append(~components,<side,hcoeff,[[Integers()!z:z in Cs(x)]:x in pt],selected>);
end for;
oldodd:=Matrix(GF(31),sections_odd_section_rows); piv:=Pivots(oldodd);
rest:=[j:j in [1..75]|not j in piv];
dep:=Submatrix(constraints,rest,[1..39]); assert IsUnit(Determinant(dep));
sol:=-Submatrix(constraints,piv,[1..39])*dep^-1; odd:=ZeroMatrix(Z,36,75);
for i in [1..36] do
    odd[i,piv[i]]:=1;
    for j in [1..39] do odd[i,rest[j]]:=sol[i,j]; end for;
end for;
assert odd*constraints eq 0;
assert [[(Integers()!z) mod old_modulus:z in Eltseq(row)]:row in Rows(odd)] eq cubic_lift_odd_section_rows;
print "PASS|SUPPORTS_AND_ODD_SECTIONS_AT_HIGHER_PRECISION";

F<b>:=ext<GF(31)|PolynomialRing(GF(31))!sections_evaluation_field_modulus>;
A<bb>:=GaloisRing(31,precision_digits,UQ!sections_evaluation_field_modulus);
function Sigma(x,A) cs:=Eltseq(x); return A!cs[1]+(A!cs[2])*(-29-A.1); end function;
indices:=cubic_lift_point_indices; fp:=sections_frobenius_permutation; tp:=sections_involution_permutation;
assignedpts:=AssociativeArray();
for index in [1..#indices] do
    idx:=indices[index]; if IsDefined(assignedpts,idx) then continue; end if;
    oldpt:=cubic_lift_point_coordinates[index]; pt:=[A!c:c in oldpt]; xs:=pt[1..16];
    jac:=Matrix(F,[[Red(Evaluate(Derivative(f,j),xs),F):j in [1..15]]:f in curveZ]);
    deps:=Pivots(jac); assert #deps eq 14;
    selected:=Pivots(Transpose(Submatrix(jac,[1..91],deps)));
    inv:=Transpose(Submatrix(jac,selected,deps))^-1;
    for digits in [precision_previous_digits..precision_digits-1] do
        power:=31^digits;
        rhs:=Vector(F,[-Residual(Evaluate(curveZ[i],xs),F,power):i in selected]); corr:=rhs*inv;
        for j in [1..14] do xs[deps[j]]+:=power*Lift(corr[j],A); end for;
    end for;
    assert &and[Evaluate(f,xs) eq 0:f in curveZ];
    nv:=Evaluate(numZ,xs); dv:=Evaluate(denZ,xs); w:=pt[17]; digits:=precision_previous_digits;
    while digits lt precision_digits do w-:=(w^2*dv-nv)*(2*w*dv)^-1; digits*:=2; end while;
    assert w^2*dv eq nv and IsUnit(w*nv*dv*Evaluate(ellZ,xs));
    lifted:=xs cat [w]; labels:=[idx,fp[idx],tp[idx],fp[tp[idx]]];
    values:=[lifted,[Sigma(x,A):x in lifted],xs cat [-w],[Sigma(x,A):x in xs] cat [-Sigma(w,A)]];
    for j in [1..4] do
        oldindex:=Index(indices,labels[j]);
        if oldindex ne 0 then
            assert [[(Integers()!z) mod old_modulus:z in Cs(x)]:x in values[j]] eq cubic_lift_point_coordinates[oldindex];
        end if;
        if IsDefined(assignedpts,labels[j]) then assert assignedpts[labels[j]] eq values[j]; end if;
        assignedpts[labels[j]]:=values[j];
    end for;
end for;
liftedpts:=[assignedpts[i]:i in indices];
print "PASS|EVALUATION_POINTS_AT_HIGHER_PRECISION";
UZ<az>:=PolynomialRing(Z); AZ<za>:=quo<UZ|UZ![Z!Numerator(c)*(Z!Denominator(c))^-1:c in fiber_nonic_coefficients]>;
bpt:=[AZ!UZ![Z!Numerator(c)*(Z!Denominator(c))^-1:c in row]:row in fiber_point_coordinates];
root:=Z!11; digits:=1;
while digits lt precision_digits do root-:=(root^2+3)*(2*root)^-1; digits*:=2; end while;
assert root^2 eq -3;
wr:=root*(AZ!UZ![Z!Numerator(c)*(Z!Denominator(c))^-1:c in branch_branch_ratio]);
assert &and[Evaluate(f,bpt) eq 0:f in curveZ];
b2:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_even_monomial_exponents];
b3:=[&*[bpt[j]^e[j]:j in [1..16]]:e in sections_odd_monomial_exponents];
bo:=[&+[odd[i,j]*b3[j]:j in [1..75]]:i in [1..36]];
bp:=b2 cat [wr*x:x in bo]; bm:=b2 cat [-wr*x:x in bo];
branchplus:=[[Integers()!Coefficient(UZ!v,j):j in [0..8]]:v in bp];
branchminus:=[[Integers()!Coefficient(UZ!v,j):j in [0..8]]:v in bm];
assert [[z mod old_modulus:z in row]:row in branchplus] eq cubic_lift_branch_plus_values;
assert [[z mod old_modulus:z in row]:row in branchminus] eq cubic_lift_branch_minus_values;
printf "PRECISION_DIGITS|%o\n",precision_digits;
printf "LIFT_MODULUS|%o\n",new_modulus;
printf "LIFT_ODD_SECTION_ROWS|%o\n",[[Integers()!z:z in Eltseq(row)]:row in Rows(odd)];
printf "LIFT_ODD_SUPPORT_COMPONENTS|%o\n",components;
printf "LIFT_POINT_INDICES|%o\n",indices;
printf "LIFT_POINT_COORDINATES|%o\n",[[[Integers()!z:z in Cs(x)]:x in pt]:pt in liftedpts];
printf "LIFT_BRANCH_PLUS_VALUES|%o\n",branchplus;
printf "LIFT_BRANCH_MINUS_VALUES|%o\n",branchminus;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|198_CM_FRAME_CUBIC_PRECISION_SECTIONS";quit;
