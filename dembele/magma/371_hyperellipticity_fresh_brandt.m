// D99: fresh arithmetic input for the hyperellipticity review.
// No previous matrix, graph, curve candidate or numerical differential is read.
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
pp := Factorization(2*OF);
assert #pp eq 1 and pp[1][2] eq 8 and Norm(pp[1][1]) eq 2;
p := pp[1][1];
M := HilbertCuspForms(F,1*OF,[2 : i in [1..8]]);
t := Cputime();
// Use the ordinary dense entry point, not the old sparse entry point.
T := Matrix(InternalHMFRawHeckeDefinite(M,p));
e,ulcm,gg := InternalHMFRawStabOrdersDefinite(M);
B := Algebra(QuaternionOrder(M));
assert IsDefinite(B) and Discriminant(B) eq 1*OF;
z := DedekindZetaExact(F,-1);
mass := &+[1/Rationals()!v : v in e];
assert z eq 5820 and mass eq z/128;
assert Nrows(T) eq #e and Nrows(T) eq 58;
assert &and[ &+[T[i,j] : i in [1..58]] eq 3 : j in [1..58]];
assert &and[e[i]*T[i,j] eq e[j]*T[j,i] : i,j in [1..58]];
rows := [[Integers()!T[i,j] : j in [1..58]] : i in [1..58]];
out := "dembele/data/computed/hyperellipticity_fresh_brandt_d99.json";
Write(out,"{\"matrix\":" cat Sprint(rows) cat ",\"stabilizers\":" cat Sprint(e) cat
 ",\"field_discriminant\":2147483648,\"class_number\":1,\"narrow_class_number\":1" cat
 ",\"class_group_proof\":\"Minkowski\",\"residue_norm\":2,\"ramification_index\":8" cat
 ",\"definite_algebra_finite_discriminant_norm\":1,\"mass\":\"1455/32\",\"zeta_minus_one\":5820" cat
 ",\"seed\":990370,\"entry_point\":\"InternalHMFRawHeckeDefinite\"}" : Overwrite:=false);
printf "FRESH_BRANDT|58 classes; mass %o; cpu %o\n",mass,Cputime(t);
print "PASS|371_hyperellipticity_fresh_brandt";
