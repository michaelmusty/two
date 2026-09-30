// D76 generated copy: only the input precision path changes.
// D76: recover the three moving sections by multiplication identities,
// then transfer all six products using the recorded radicand and scalar.
SetQuitOnError(true); SetColumns(0); SetSeed(76);
started:=Cputime();
load "dembele/data/computed/cm_frame_B3_moving_64.m";
load "dembele/data/computed/cm_frame_B3_transfer.m";
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function Quadric(row,mon)
    return &+[(Integers()!row[j])*mon[j]:j in [1..#mon]];
end function;
g:=Quadric(moving_g,mon);
IE:=Saturation(IC+ideal<R|[Quadric(row,mon):row in resolvent_E_quadrics]>);
IEB3:=IE meet B3_ideal;
assert Degree(Scheme(P,IEB3)) eq 25 and g in IEB3;
IG:=Saturation(ColonIdeal(IC+ideal<R|g>,IEB3));
assert Degree(Scheme(P,IG)) eq 35 and IsReduced(Scheme(P,IG));
assert Dimension(IG+IEB3) eq 0;
chosen_h:=0;
for i in [1..#moving_g_basis] do
    h:=Quadric(moving_g_basis[i],mon);
    assert h in IEB3;
    if Dimension(IG+ideal<R|h>) eq 0 then chosen_h:=i; break; end if;
end for;
assert chosen_h ne 0;
printf "H_BASIS_INDEX|%o\n",chosen_h;

k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
IQ:=Ideal(C_candidate); GQ:=GroebnerBasis(IQ);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
Z:=Integers(moving_modulus); kk:=GF(31);
function Red(c,Z)
    assert Denominator(c) mod 31 ne 0;
    return (Z!Numerator(c))/(Z!Denominator(c));
end function;
// Keep coefficients reduced between multiplications to limit intermediate size.
function ReducedNormalForm(f,I,Z)
    out:=Parent(f)!0; cs,ms:=CoefficientsAndMonomials(NormalForm(f,I));
    for i in [1..#cs] do out+:=(Integers()!Red(cs[i],Z))*ms[i]; end for;
    return out;
end function;
g:=Quadric(moving_g,mon); h:=Quadric(moving_g_basis[chosen_h],mon);
products:=[ReducedNormalForm(h*mon[j],IQ,Z):j in moving_chart]
      cat [-ReducedNormalForm(g*mon[j],IQ,Z):j in moving_chart];
quartics:=Setseq(Seqset(&cat[Monomials(f):f in products])); Sort(~quartics);
assert #quartics eq 105;
M:=Matrix(Z,[[Red(MonomialCoefficient(f,m),Z):m in quartics]:f in products]);
jmat:=Matrix(Z,moving_q_jets);
M:=HorizontalJoin(M,VerticalJoin(Transpose(jmat),ZeroMatrix(Z,45,7)));
assert Nrows(M) eq 90 and Ncols(M) eq 112 and Rank(Matrix(kk,M)) eq 87;
active:=[j:j in [1..90]|not j in moving_q_free];
A:=Submatrix(M,active,[1..112]);
ech:=EchelonForm(Matrix(kk,A)); assert Rank(ech) eq 87;
cols:=[Min([j:j in [1..112]|ech[i,j] ne 0]):i in [1..87]];
inverse:=Submatrix(A,[1..87],cols)^-1;
B:=ZeroMatrix(Z,3,90);
for i in [1..3] do
    free:=moving_q_free[i]; B[i,free]:=1;
    sol:=-Vector(Z,[M[free,j]:j in cols])*inverse;
    for j in [1..87] do B[i,active[j]]:=sol[j]; end for;
end for;
assert B*M eq 0;
function FullRow(row,chart)
    out:=[0:j in [1..136]];
    for i in [1..45] do out[chart[i]]:=Integers()!row[i]; end for;
    return out;
end function;
qrows:=[FullRow(Eltseq(B[i])[1..45],moving_chart):i in [1..3]];
srows:=[FullRow(Eltseq(B[i])[46..90],moving_chart):i in [1..3]];
qs:=[Quadric(row,mon):row in qrows];
for i in [1..3] do
    assert ReducedNormalForm(h*qs[i]-g*Quadric(srows[i],mon),IQ,Z) eq 0;
end for;
printf "MOVING_KERNEL_RANK|%o\n",Rank(Matrix(kk,M));
print "MOVING_SECTION_DIMENSION|3";
printf "KERNEL_CPU_SECONDS|%o\n",Cputime(started);
oldn:=Quadric(moving_old_numerator,mon); oldd:=Quadric(moving_old_denominator,mon);
newn:=Quadric(moving_new_numerator,mon);
multiplier:=ReducedNormalForm(ReducedNormalForm(oldn*g,IQ,Z)*g,IQ,Z);
mults:=[ReducedNormalForm(multiplier*mon[j],IQ,Z):j in moving_chart];
indices:=[[i,j]:i,j in [1..3]|i le j];
start_rhs:=ReducedNormalForm(newn*oldd,IQ,Z);
targets:=[ReducedNormalForm(ReducedNormalForm(start_rhs*qs[v[1]],IQ,Z)*qs[v[2]],IQ,Z):v in indices];
degree8:=Setseq(Seqset(&cat[Monomials(f):f in mults cat targets])); Sort(~degree8);
N:=Matrix(Z,[[Red(MonomialCoefficient(f,m),Z):m in degree8]:f in mults]);
assert Rank(Matrix(kk,N)) eq 45;
ech:=EchelonForm(Matrix(kk,N));
cols:=[Min([j:j in [1..#degree8]|ech[i,j] ne 0]):i in [1..45]];
inverse:=Submatrix(N,[1..45],cols)^-1;
denrows:=[];
for rhs_poly in targets do
    rhs:=Vector(Z,[Red(MonomialCoefficient(rhs_poly,m),Z):m in degree8]);
    sol:=Vector(Z,[rhs[j]:j in cols])*inverse;
    assert sol*N eq rhs;
    Append(~denrows,FullRow(Eltseq(sol),moving_chart));
end for;
coeffs:=[Z!x:x in moving_q_selected_free];
selected_q:=&+[coeffs[i]*Vector(Z,qrows[i]):i in [1..3]];
selected_d:=&+[(v[1] eq v[2] select Z!1 else Z!2)*coeffs[v[1]]*coeffs[v[2]]*Vector(Z,denrows[i]):
                i->v in indices];
assert ReducedNormalForm(multiplier*Quadric(Eltseq(selected_d),mon)
    -ReducedNormalForm(ReducedNormalForm(start_rhs*Quadric(Eltseq(selected_q),mon),IQ,Z)
                       *Quadric(Eltseq(selected_q),mon),IQ,Z),IQ,Z) eq 0;
// Compare section classes with D75 without relying on its monomial representatives.
qdiff:=NormalForm(Quadric([Integers()!x:x in Eltseq(selected_q)],mon)-Quadric(B3_square_denominator,mon),IQ);
ddiff:=NormalForm(Quadric([Integers()!x:x in Eltseq(selected_d)],mon)-Quadric(B3_new_denominator,mon),IQ);
assert &and[Red(c,Integers(31)) eq 0:c in Coefficients(qdiff) cat Coefficients(ddiff)];
printf "MODULUS|%o\n",moving_modulus;
printf "H_COEFFICIENTS|%o\n",moving_g_basis[chosen_h];
printf "Q_BASIS_COEFFICIENTS|%o\n",qrows;
printf "Q_WITNESS_COEFFICIENTS|%o\n",srows;
printf "PRODUCT_INDICES|%o\n",indices;
printf "PRODUCT_DENOMINATOR_COEFFICIENTS|%o\n",denrows;
printf "PRODUCT_SPACE_RANK_MOD31|%o\n",Rank(Matrix(kk,denrows));
printf "SELECTED_Q_COEFFICIENTS|%o\n",[Integers()!x:x in Eltseq(selected_q)];
printf "SELECTED_DENOMINATOR_COEFFICIENTS|%o\n",[Integers()!x:x in Eltseq(selected_d)];
printf "DEGREE_EIGHT_COORDINATES|%o\n",#degree8;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|147_CM_FRAME_B3_PRODUCT_SPACE";
quit;
