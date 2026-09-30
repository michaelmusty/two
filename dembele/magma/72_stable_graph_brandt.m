// Recompute the norm-2 Brandt operator for the stable-graph audit.
SetColumns(0);
SetQuitOnError(true);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
// Small search factor base, but unconditional Minkowski proof bound.
search_bound := map<PowerStructure(RngOrd) -> Integers() | O :-> GRHBound(O)>;
proof_bound := map<PowerStructure(RngOrd) -> Integers() | O :-> MinkowskiBound(O)>;
SetClassGroupBoundMaps(search_bound,proof_bound);
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8-8*x^6+20*x^4-16*x^2+2);
OF := Integers(F);
assert #ClassGroup(OF : Proof:="Full") eq 1;
assert #NarrowClassGroup(OF) eq 1;
printf "R72|ordinary and narrow class numbers 1; Minkowski proof bounds\n";
p := Factorization(2*OF)[1][1];
M := HilbertCuspForms(F,1*OF,[2 : i in [1..8]]);
t := Cputime();
T := Matrix(InternalHMFRawHeckeDefiniteSparse(M,p));
e,ulcm,gg := InternalHMFRawStabOrdersDefinite(M);
mass := &+[1/Rationals()!v : v in e];
zeta := DedekindZetaExact(F,-1);
assert zeta eq 5820 and mass eq zeta/128 and mass eq 1455/32;
printf "R72|mass %o matches exact zeta(-1)/128 = %o/128\n",mass,zeta;
assert Nrows(T) eq 58;
assert &and[ &+[T[i,j] : i in [1..58]] eq 3 : j in [1..58] ];
forward_pairing := &and[e[i]*T[i,j] eq e[j]*T[j,i] : i,j in [1..58]];
reverse_pairing := &and[e[j]*T[i,j] eq e[i]*T[j,i] : i,j in [1..58]];
printf "R72|e_i T_ij = e_j T_ji: %o; reversed identity: %o\n",forward_pairing,reverse_pairing;
assert forward_pairing or reverse_pairing;
rows := [ [Integers()!T[i,j] : j in [1..58]] : i in [1..58]];
out := "dembele/data/computed/stable_graph_brandt.json";
Write(out,"{\"matrix\":" cat Sprint(rows) cat ",\"stabilizers\":" cat Sprint(e) cat
    ",\"class_group_proof\":\"Minkowski\",\"mass\":\"1455/32\",\"zeta_minus_one\":5820}" : Overwrite:=true);
printf "R72|58 classes; norm-2 Brandt matrix and stabilizers exported; cpu %o\n", Cputime(t);
print "PASS|72_stable_graph_brandt";
