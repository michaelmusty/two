// D106: exact candidate jets in the RATIO parameter t=X2/X1-r2(P).
// No independently evaluated arithmetic Shimura section is read.
SetColumns(0); SetSeed(106388); SetQuitOnError(true);
started := Cputime();
k := Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_tangent_candidate_height_d101_input.m";
Qx<x> := PolynomialRing(Rationals());
H := Qx!Hcoeffs;
E<theta> := NumberField(H);
raw := [ &+[E!c[j]*theta^(j-1) : j in [1..17]] : c in point_coeffs ];
assert raw[1] ne 0;
point := [z/raw[1] : z in raw];
assert point[1] eq 1;
J := ZeroMatrix(E,91,16);
for q in [1..91] do
  assert &+[E!rows[q][h]*point[pairs[h][1]]*point[pairs[h][2]] : h in [1..136]] eq 0;
  for h in [1..136] do
    i,j := Explode(pairs[h]);
    J[q,i] +:= E!rows[q][h]*point[j];
    J[q,j] +:= E!rows[q][h]*point[i];
  end for;
end for;
A := ZeroMatrix(E,2,16); A[1,1] := 1; A[2,2] := 1;
M := VerticalJoin(J,A);
assert Rank(J) eq 14 and Rank(M) eq 16;
jets := [Vector(E,point)];
for n in [1..3] do
  rhs := [];
  for q in [1..91] do
    c := E!0;
    for ell in [1..n-1] do
      c +:= &+[E!rows[q][h]*jets[ell+1][pairs[h][1]]*jets[n-ell+1][pairs[h][2]] : h in [1..136]];
    end for;
    Append(~rhs,-c);
  end for;
  rhs := Vector(E,rhs cat [0,(n eq 1) select 1 else 0]);
  v := Solution(Transpose(M),rhs);
  assert v*Transpose(M) eq rhs and v[1] eq 0;
  assert v[2] eq ((n eq 1) select 1 else 0);
  Append(~jets,v);
end for;
for n in [0..3] do
  for q in [1..91] do
    assert &+[E!rows[q][h]*(&+[jets[ell+1][pairs[h][1]]*jets[n-ell+1][pairs[h][2]] : ell in [0..n]]) : h in [1..136]] eq 0;
  end for;
  coeff := [Eltseq(z) : z in Eltseq(jets[n+1])];
  assert &and[GCD(Denominator(c),31) eq 1 : c in &cat coeff];
  printf "JET%o_NUMERATORS|%o\n", n, [[Numerator(c) : c in row] : row in coeff];
  printf "JET%o_DENOMINATORS|%o\n", n, [[Denominator(c) : c in row] : row in coeff];
end for;
printf "CPU_SECONDS|%o\n", Cputime(started);
print "PASS|D106_CANDIDATE_RATIO_JETS";
quit;
