// D109 bounded export of the actual level-one definite HMF order.
// No new ideal-class or Bruhat--Tits tree enumeration is requested.
SetColumns(0);
SetQuitOnError(true);
SetMemoryLimit(2000000000);
SetSeed(990370);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
search := map<PowerStructure(RngOrd) -> Integers() | O :-> GRHBound(O)>;
proof := map<PowerStructure(RngOrd) -> Integers() | O :-> MinkowskiBound(O)>;
SetClassGroupBoundMaps(search,proof);
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8-8*x^6+20*x^4-16*x^2+2);
OF := Integers(F);
assert Discriminant(OF) eq 2^31;
assert #ClassGroup(OF : Proof:="Full") eq 1;
assert #NarrowClassGroup(OF) eq 1;
p := Factorization(2*OF)[1][1];
assert Norm(p) eq 2 and b*OF eq p;
M := HilbertCuspForms(F,1*OF,[2 : i in [1..8]]);
O := QuaternionOrder(M);
B := Algebra(O);
assert IsDefinite(B) and Discriminant(B) eq 1*OF;
assert IsMaximal(O) and Discriminant(O) eq 1*OF;
assert B.1^2 in F and B.2^2 in F and B.1*B.2 eq B.3;
assert B.2*B.1 eq -B.3;
printf "ORDER|a=%o; b=%o; Z-rank=%o\n",F!(B.1^2),F!(B.2^2),#ZBasis(O);
MR,phi,toK := pMatrixRing(O,p : Precision:=96);
K := BaseRing(MR);
printf "LOCAL|%o\n",K;
printf "VAL|pi=%o; two=%o\n",Valuation(toK(b)),Valuation(toK(F!2));
printf "RELATIONS|%o\n",[[Valuation(c) : c in Eltseq(mat)] : mat in
 [phi(B.1)^2+Identity(MR),phi(B.2)^2+Identity(MR),phi(B.1)*phi(B.2)+phi(B.2)*phi(B.1)]];
// Approximate centers are proposals; the independent Hensel check certifies them.
// Checking 32 mapped Z-basis elements stalls in this installed Magma map.
// Export the four algebra matrices only; 398/399 certify order integrality.
print "STAGE|preparing local power basis";
// Direct local power-basis conversion avoids the expensive global inverse map.
power_basis := Matrix([Eltseq(toK(b^j)) : j in [0..7]]);
assert Nrows(power_basis) eq 8 and Ncols(power_basis) eq 8;
inverse_power_basis := power_basis^-1;
function Center(c)
  coords := Eltseq(Vector(Eltseq(c))*inverse_power_basis);
  lifted := [];
  for v in coords do
    denominator := 2^Max(0,-Valuation(v));
    Append(~lifted,Rationals()!(Integers()!(denominator*v))/denominator);
  end for;
  return &+[F!lifted[j+1]*b^j : j in [0..7]];
end function;
function JS(a)
  return "[" cat Join(["\"" cat Sprint(Rationals()!c) cat "\"" : c in Eltseq(F!a)],",") cat "]";
end function;
function JQ(q)
  return "[" cat Join([JS(c) : c in Eltseq(B!q)],",") cat "]";
end function;
function JM(mat)
  return "[" cat Join([JS(Center(c)) : c in Eltseq(mat)],",") cat "]";
end function;
// Exact rational centers of the approximate local matrix images.
matrices := [JM(phi(q)) : q in [B!1,B.1,B.2,B.3]];
print "STAGE|matrix centers exported";
U,umap := NormOneGroup(O : ModScalars);
printf "UNITS|order=%o; generators=%o\n",#U,Ngens(U);
units := [B!umap(U.i) : i in [1..Ngens(U)]];
out := "dembele/data/computed/definite_dyadic_export_d109.json";
Write(out,"{\"status\":\"pass\",\"milestone\":\"D109\",\"seed\":990370," cat
  "\"field_polynomial_ascending\":[2,0,-16,0,20,0,-8,0,1]," cat
  "\"quaternion_parameters\":[" cat JS(F!(B.1^2)) cat "," cat JS(F!(B.2^2)) cat "]," cat
  "\"order_Z_basis\":[" cat Join([JQ(q) : q in ZBasis(O)],",") cat "]," cat
  "\"OF_Z_basis\":[" cat Join([JS(q) : q in Basis(OF)],",") cat "]," cat
  "\"approximate_basis_matrices\":[" cat Join(matrices,",") cat "]," cat
  "\"projective_unit_generators\":[" cat Join([JQ(q) : q in units],",") cat "]," cat
  "\"projective_unit_group_order\":" cat Sprint(#U) cat "," cat
  "\"Magma_version\":\"" cat Sprint(GetVersion()) cat "\"," cat
  "\"requested_local_precision\":96,\"order_discriminant_norm\":1," cat
  "\"field_discriminant\":2147483648,\"definite_at_all_real_places\":true," cat
  "\"new_ideal_class_or_tree_enumeration\":false}" : Overwrite:=false);
print "PASS|397_definite_dyadic_export";
