// D101: exact candidate tangent only; no arithmetic Shimura identification.
SetColumns(0); SetSeed(101375); SetQuitOnError(true);
started := Cputime();
k := Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_tangent_candidate_height_d101_input.m";
Qx<x> := PolynomialRing(Rationals());
H := Qx!Hcoeffs;
assert Degree(H) eq 17 and IsIrreducible(H);
E<theta> := NumberField(H);
point := [ &+[E!c[j]*theta^(j-1) : j in [1..17]] : c in point_coeffs ];
assert point[1] ne 0;
assert &and[ &+[E!row[h]*point[pairs[h][1]]*point[pairs[h][2]] : h in [1..136]] eq 0 : row in rows ];

J := ZeroMatrix(E,91,16);
for q in [1..91] do
  for h in [1..136] do
    i,j := Explode(pairs[h]);
    J[q,i] +:= E!rows[q][h]*point[j];
    J[q,j] +:= E!rows[q][h]*point[i];
  end for;
end for;
assert Rank(J) eq 14;
A := ZeroMatrix(E,2,16); A[1,1] := 1; A[2,2] := 1;
M := VerticalJoin(J,A);
assert Rank(M) eq 16;
rhs := Vector(E,[0 : i in [1..92]] cat [1]);
v := Solution(Transpose(M),rhs);
assert v*Transpose(M) eq rhs and v[1] eq 0 and v[2] eq 1;
bad := v; bad[3] +:= 1;
assert bad*Transpose(M) ne rhs;

// The saved integral basis is checked as an integral lattice, not assumed
// maximal. Maximality is unnecessary for a valid clearing integer.
ib := [ &+[E!c[j]*theta^(j-1) : j in [1..17]] : c in integral_basis_coeffs ];
assert #ib eq 17;
for z in ib do
  f := MinimalPolynomial(z);
  assert IsMonic(f) and &and[Denominator(c) eq 1 : c in Coefficients(f)];
end for;
ibm := Matrix(Rationals(),integral_basis_coeffs);
assert Determinant(ibm) ne 0;
traces := Matrix(Rationals(),17,17,[Trace(a*b) : a,b in ib]);
assert Determinant(traces) eq expected_basis_discriminant;
power := [Eltseq(z) : z in Eltseq(v)];
icoords := [Eltseq(Vector(Rationals(),c)*ibm^-1) : c in power];
Dp := LCM(&cat[[Denominator(c) : c in row] : row in power]);
Di := LCM(&cat[[Denominator(c) : c in row] : row in icoords]);
assert GCD(Dp,31) eq 1 and GCD(Di,31) eq 1;
printf "TANGENT_NUMERATORS|%o\n", [[Numerator(c) : c in row] : row in power];
printf "TANGENT_DENOMINATORS|%o\n", [[Denominator(c) : c in row] : row in power];
printf "INTEGRAL_NUMERATORS|%o\n", [[Numerator(c) : c in row] : row in icoords];
printf "INTEGRAL_DENOMINATORS|%o\n", [[Denominator(c) : c in row] : row in icoords];
printf "CLEARING_INTEGERS|%o|%o\n", Dp,Di;
printf "BASIS_DISCRIMINANT|%o\n", Determinant(traces);
printf "CPU_SECONDS|%o\n", Cputime(started);
print "PASS|D101_EXACT_CANDIDATE_TANGENT";
quit;
