// D82: rational-base jets for H0(4K_C-80*P32), independent of the cubic class.
SetQuitOnError(true); SetColumns(0); started:=Cputime();
k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_B3_rational_model.m";
load "dembele/data/computed/cm_frame_cubic.m";
Z:=Integers(31^precision_digits); PZ:=PolynomialRing(Z,16);
mon:=[PZ.(p[1])*PZ.(p[2]):p in pairs];
curve:=[&+[row[i]*mon[i]:i in [1..136]]:row in rows];
num:=&+[rational_numerator[i]*mon[i]:i in [1..136]];
den:=&+[rational_denominator[i]*mon[i]:i in [1..136]];
pt:=[Z!z:z in P32_coordinates]; pt:=[z*pt[16]^-1:z in pt];
assert &and[Evaluate(f,pt) eq 0:f in curve] and Evaluate(num,pt) eq 0;
assert IsUnit(Evaluate(den,pt)); equations:=curve cat [num];
J:=Matrix(Z,[[Evaluate(Derivative(f,j),pt):j in [1..15]]:f in equations]);
E:=EchelonForm(Transpose(ChangeRing(J,GF(31))));
selected:=[Min([j:j in [1..92]|E[i,j] ne 0]):i in [1..15]];
assert Rank(ChangeRing(J,GF(31))) eq 15;
inv:=Transpose(Submatrix(J,selected,[1..15]))^-1;
PS<s>:=PowerSeriesRing(Z,80); xs:=[PS!z+O(s^80):z in pt];
for degree in [1..79] do
    rhs:=Vector(Z,[-Coefficient(Evaluate(equations[i],xs)-(i eq 92 select s*Evaluate(den,xs) else PS!0),degree):i in selected]);
    corr:=rhs*inv;
    for j in [1..15] do xs[j]+:=corr[j]*s^degree; end for;
end for;
assert &and[Evaluate(f,xs) eq 0:f in curve];
assert Evaluate(num,xs) eq s*Evaluate(den,xs);
curvejets:=[[Integers()!Coefficient(x,j):j in [0..79]]:x in xs];
assert [[x mod 31^32:x in row]:row in curvejets] eq
    [[pointed_curve_jets[i][2*j+1]:j in [0..79]]:i in [1..16]];
quartics:=[&*[xs[j]^e[j]:j in [1..16]]:e in cubic_quartic_monomials];
jets:=Matrix(Z,[[Coefficient(f,j):j in [0..79]]:f in quartics]);
assert Rank(ChangeRing(jets,GF(31))) eq 80;
printf "QUARTIC_SPACE_JETS|%o\n",[[Integers()!z:z in Eltseq(row)]:row in Rows(jets)];
printf "QUARTIC_CURVE_JETS|%o\n",curvejets;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|246_CM_FRAME_CUBIC_QUARTIC_SPACE_JETS";quit;
