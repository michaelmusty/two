// Independent check of the algebra used by the PARI domain computation.
// Dembélé, arXiv:1906.06772, section 5.1.
SetQuitOnError(true);
SetColumns(0);
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8-8*x^6+20*x^4-16*x^2+2);
B<i,j,k> := QuaternionAlgebra<F | b-b^2,-1>;
O := MaximalOrder(B);
d := Norm(Discriminant(O));
s := Signature(FuchsianGroup(O));
assert d eq 2;
assert s eq <40, [3 : i in [1..18]] cat [16]>;
printf "R65M|discriminant norm %o; signature %o\n",d,s;
print "PASS|65_explicit_quaternion";
quit;
