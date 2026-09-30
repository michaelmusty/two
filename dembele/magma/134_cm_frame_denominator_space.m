// D74: an exact 17-dimensional space containing the denominator.
// If n has divisor A+T and r has divisor A+T_r with T disjoint from T_r,
// then r*d=n*s in degree four is equivalent to d vanishing on T.
SetQuitOnError(true); SetColumns(0); SetSeed(74);
started:=Cputime(); k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_numerator_lattice.m";
load "dembele/data/computed/cm_frame_normalized_resolvent.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function Quadric(row,mon)
    return &+[row[i]*mon[i]:i in [1..#mon]];
end function;
n:=Quadric(normalized_numerator,mon);
U<z>:=PolynomialRing(GF(31)); h:=U!normalized_residual_modulus;
coords:=[U!c:c in normalized_residual_coordinates];
chosen:=0;
for j in [1..#normalized_numerator_candidates] do
    row:=normalized_numerator_candidates[j];
    value:=(&+[U!row[i]*coords[pairs[i][1]]*coords[pairs[i][2]]:i in [1..#pairs]]) mod h;
    if Degree(GCD(value,h)) eq 0 then chosen:=j; break; end if;
end for;
assert chosen gt 0;
r:=Quadric(normalized_numerator_candidates[chosen],mon);
products:=[NormalForm(r*mon[j],IC):j in normalization_chart]
          cat [-NormalForm(n*mon[j],IC):j in normalization_chart];
quartics:=Setseq(Seqset(&cat[Monomials(f):f in products])); Sort(~quartics);
assert #quartics eq 105;
M:=Matrix(k,[[MonomialCoefficient(f,m):m in quartics]:f in products]);
V:=Nullspace(M); assert Dimension(V) eq 17;
B:=BasisMatrix(V);
assert B*M eq 0;
assert Rank(Submatrix(B,[1..17],[1..45])) eq 17;
printf "SECOND_NUMERATOR_CANDIDATE|%o\n",chosen;
printf "MULTIPLICATION_RANK|%o\n",Rank(M);
printf "DENOMINATOR_SPACE_DIMENSION|%o\n",Dimension(V);
printf "PAIRED_BASIS_RATIONAL_STRINGS|%o\n",[[Sprint(c):c in Eltseq(v)]:v in Rows(B)];
printf "SECOND_NUMERATOR|%o\n",normalized_numerator_candidates[chosen];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|134_CM_FRAME_DENOMINATOR_SPACE";
quit;
