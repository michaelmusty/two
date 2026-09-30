// D74 generated verifier/transfer; only the displayed data paths differ.
// D73: transfer a short rational numerator without changing the saved radicand.
SetQuitOnError(true); SetColumns(0); SetSeed(73);
started:=Cputime(); k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_doubling_128.m";
load "dembele/data/computed/cm_frame_numerator_lattice.m";
IQ:=Ideal(C_candidate); GQ:=GroebnerBasis(IQ);
monQ:=[R.(p[1])*R.(p[2]):p in pairs];
function Quadric(row,mon)
    return &+[row[j]*mon[j]:j in [1..#mon]];
end function;
oldn:=Quadric(lift_numerator,monQ); oldd:=Quadric(lift_denominator,monQ);
products:=[NormalForm(oldn*monQ[j],IQ):j in normalization_chart];
quartics:=Setseq(Seqset(&cat[Monomials(f):f in products])); Sort(~quartics);
Z:=Integers(lift_modulus); kk:=GF(31);
function ReduceCoefficient(c,Z)
    assert Denominator(c) mod 31 ne 0;
    return (Z!Numerator(c))/(Z!Denominator(c));
end function;
N:=Matrix(Z,[[ReduceCoefficient(MonomialCoefficient(f,m),Z):m in quartics]:f in products]);
N0:=Matrix(kk,N); assert Rank(N0) eq 45;
ech:=EchelonForm(N0);
cols:=[Min([j:j in [1..Ncols(ech)]|ech[i][j] ne 0]):i in [1..45]];
square:=Submatrix(N,[1..45],cols); inv:=square^-1;
assert square*inv eq IdentityMatrix(Z,45);
printf "MULTIPLICATION_RANK|%o\n",Rank(N0);
printf "QUARTIC_COORDINATES|%o\n",#quartics;

// Select a candidate whose new common zero divisor is reduced and finite
// in the X16=1 chart. These checks are only for convenient future lifting.
RQ:=R;
k:=kk;
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
IC:=Ideal(C_candidate); mon:=[R.(p[1])*R.(p[2]):p in pairs];
Eqs:=[Quadric(row,mon):row in resolvent_E_quadrics];
IE:=Saturation(IC+ideal<R|Eqs>);
IE2:=Saturation(IC+ideal<R|[q*r:q,r in Eqs]>);
PS<t>:=PowerSeriesRing(k,16);
xs:=[(&+[PS!resolvent_point_jets[n+1][j]*t^n:n in [0..15]])+O(t^16):j in [1..16]];
jmat:=Matrix(k,[[Coefficient(Evaluate(q,xs),n):q in mon]:n in [0..14]]);
ker:=Basis(Nullspace(Transpose(jmat)));
IP15:=Saturation(ideal<R|[Quadric(Eltseq(v),mon):v in ker]>);
ID32:=D17_ideal meet IP15;
assert Degree(Scheme(P,ID32)) eq 32;
chosen:=0;
for trial in [1..#normalized_numerator_candidates] do
    qn:=Quadric(normalized_numerator_candidates[trial],mon);
    assert qn in ID32 and not qn in IC;
    J:=Saturation(ColonIdeal(IC+ideal<R|qn>,ID32));
    if Degree(Scheme(P,J)) ne 28 or Dimension(J+ID32) ne 0
       or Dimension(J+IE) ne 0 or Dimension(J+ideal<R|R.16>) ne 0 then
        printf "REJECT_CANDIDATE|%o|support_geometry\n",trial; continue;
    end if;
    S:=PolynomialRing(k,15,"grevlex");
    ia:=ideal<S|[Evaluate(f,[S.i:i in [1..15]] cat [S!1]):f in Basis(J)]>;
    L:=PolynomialRing(k,15,"lex"); il:=ideal<L|[L!f:f in GroebnerBasis(ia)]>;
    gl:=GroebnerBasis(il);
    if #gl ne 15 then printf "REJECT_CANDIDATE|%o|projection_shape\n",trial; continue; end if;
    U<z>:=PolynomialRing(k);
    h:=Evaluate(gl[#gl],[U!0:i in [1..14]] cat [z]); h/:=LeadingCoefficient(h);
    if Degree(h) ne 28 or Degree(GCD(h,Derivative(h))) ne 0 then
        printf "REJECT_CANDIDATE|%o|projection_separability\n",trial; continue;
    end if;
    cs:=[Evaluate(NormalForm(L.i,il),[U!0:j in [1..14]] cat [z]):i in [1..15]];
    assert cs[15] eq z;
    shape:=ideal<L|[L.i-Evaluate(cs[i],L.15):i in [1..14]] cat [Evaluate(h,L.15)]>;
    assert shape eq il;
    cs cat:=[U!1];
    chosen:=trial; break;
end for;
assert chosen ne 0;
newrow:=normalized_numerator_candidates[chosen];
newn:=Quadric(newrow,monQ);
rhs_poly:=NormalForm(newn*oldd,IQ);
assert Seqset(Monomials(rhs_poly)) subset Seqset(quartics);
rhs:=Vector(Z,[ReduceCoefficient(MonomialCoefficient(rhs_poly,m),Z):m in quartics]);
sol:=Vector(Z,[rhs[j]:j in cols])*inv;
assert sol*N eq rhs;
newden:=[0:j in [1..136]];
for i in [1..45] do newden[normalization_chart[i]]:=Integers()!sol[i]; end for;
newd:=Quadric(newden,monQ);
residual:=NormalForm(oldn*newd-newn*oldd,IQ);
assert &and[ReduceCoefficient(c,Z) eq 0:c in Coefficients(residual)];
qd:=Quadric(newden,mon);
assert Saturation(IC+ideal<R|qn>) eq (ID32 meet J);
assert Saturation(IC+ideal<R|qd>) eq (IE2 meet J);
assert NormalForm(Quadric(lift_numerator,mon)*qd-qn*Quadric(lift_denominator,mon),IC) eq 0;
printf "SELECTED_CANDIDATE|%o\n",chosen;
printf "NORMALIZED_NUMERATOR|%o\n",newrow;
printf "NORMALIZED_DENOMINATOR|%o\n",newden;
printf "RESIDUAL_MODULUS|%o\n",[Integers()!Coefficient(h,i):i in [0..28]];
printf "RESIDUAL_COORDINATES|%o\n",[[Integers()!Coefficient(c,i):i in [0..27]]:c in cs];
printf "RESIDUAL_FACTOR_DEGREES|%o\n",[Degree(a[1]):a in Factorization(h)];
printf "MODULUS|%o\n",lift_modulus;
print "IDENTITY|q_num*q_den_new = q_num_new*q_den on C";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|128_CM_FRAME_NORMALIZATION_TRANSFER";
quit;
