// D110: replay the saved 58-class level-one calculation to export missing
// arithmetic witnesses. No higher level, extra prime, or tree census.
SetColumns(0);
SetQuitOnError(true);
SetMemoryLimit(2000000000);
SetSeed(990370);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
import "/Users/musty/hilbertmodularforms/ModFrmHil/precompute.m": get_rids, get_tps;
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
T := Matrix(InternalHMFRawHeckeDefinite(M,p));
e,ulcm,gg := InternalHMFRawStabOrdersDefinite(M);
O := QuaternionOrder(M); B := Algebra(O);
assert IsDefinite(B) and Discriminant(B) eq 1*OF;
assert B.1^2 eq -1 and B.2^2 eq -1 and B.1*B.2 eq B.3;
rids := get_rids(M); tps := get_tps(M,p);
assert #rids eq 58 and Nrows(T) eq 58;
assert rids[1] eq rideal<O | 1>;
assert &and[ &+[T[i,j] : i in [1..58]] eq 3 : j in [1..58]];
assert &and[e[i]*T[i,j] eq e[j]*T[j,i] : i,j in [1..58]];
printf "BRANDT|58 classes; base ideal O; stabilizer %o\n",e[1];
function JS(a)
  return "[" cat Join(["\"" cat Sprint(Rationals()!c) cat "\"" : c in Eltseq(F!a)],",") cat "]";
end function;
function JQ(q)
  return "[" cat Join([JS(c) : c in Eltseq(B!q)],",") cat "]";
end function;
function JB(qs)
  return "[" cat Join([JQ(q) : q in qs],",") cat "]";
end function;
// This short odd walk was chosen from the already saved D99 matrix.
walk := [1,2,4,5,5,4,2,1];
edges := []; w := B!1;
for k in [1..#walk-1] do
  j := walk[k]; i := walk[k+1];
  assert IsDefined(tps,<j,i>) and #tps[<j,i>] eq T[i,j];
  t := tps[<j,i>][1];
  assert (Norm(t)*OF)*Norm(rids[j]) eq p*Norm(rids[i]);
  Append(~edges,"{\"source_class\":" cat Sprint(j-1) cat
    ",\"target_class\":" cat Sprint(i-1) cat
    ",\"representative_index\":0,\"brandt_multiplicity\":" cat Sprint(#tps[<j,i>]) cat
    ",\"quaternion\":" cat JQ(t) cat "}");
  w := t*w;
end for;
assert Norm(w)*OF eq p^7;
assert w in O;
u := (1-B.1-B.2-B.3)/2;
assert u in O and Norm(u) eq 1;
g := w*u/w;
assert Norm(g) eq 1;
classes := [1,2,4,5];
ideals := ["{\"class_index\":" cat Sprint(j-1) cat
  ",\"Z_basis\":" cat JB(ZBasis(rids[j])) cat
  ",\"absolute_norm\":" cat Sprint(Norm(Norm(rids[j]))) cat "}" : j in classes];
major,minor,patch := GetVersion();
out := "dembele/data/computed/dyadic_brandt_transport_export_d110.json";
Write(out,"{\"status\":\"pass\",\"milestone\":\"D110\",\"seed\":990370," cat
  "\"magma_version\":[" cat Sprint(major) cat "," cat Sprint(minor) cat "," cat Sprint(patch) cat "]," cat
  "\"matrix\":" cat Sprint([[Integers()!T[i,j] : j in [1..58]] : i in [1..58]]) cat "," cat
  "\"stabilizers\":" cat Sprint(e) cat ",\"base_class\":0," cat
  "\"order_Z_basis\":" cat JB(ZBasis(O)) cat "," cat
  "\"selected_ideals\":[" cat Join(ideals,",") cat "]," cat
  "\"walk\":" cat Sprint([j-1 : j in walk]) cat "," cat
  "\"edges\":[" cat Join(edges,",") cat "]," cat
  "\"odd_element\":" cat JQ(w) cat ",\"odd_element_norm\":" cat JS(Norm(w)) cat "," cat
  "\"norm_one_moving_element\":" cat JQ(g) cat "," cat
  "\"new_level_or_prime\":false,\"new_tree_census\":false}" : Overwrite:=false);
print "PASS|400_dyadic_brandt_transport_export";
