// D111: serialize the existing 58-class calculation and its cached data.
// Same field, seed, maximal level and norm-two prime as D99/D110.
SetColumns(0); SetQuitOnError(true); SetMemoryLimit(2000000000);
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
assert #ClassGroup(OF : Proof:="Full") eq 1 and #NarrowClassGroup(OF) eq 1;
pp := Factorization(2*OF); p := pp[1][1];
assert #pp eq 1 and pp[1][2] eq 8 and Norm(p) eq 2;
M := HilbertCuspForms(F,1*OF,[2 : i in [1..8]]);
T := Matrix(InternalHMFRawHeckeDefinite(M,p));
e,ulcm,gg := InternalHMFRawStabOrdersDefinite(M);
O := QuaternionOrder(M); B := Algebra(O);
rids := get_rids(M); tps := get_tps(M,p);
assert #rids eq 58 and rids[1] eq rideal<O | 1>;
assert B.1^2 eq -1 and B.2^2 eq -1 and B.1*B.2 eq B.3;
function JS(a)
  return "[" cat Join(["\"" cat Sprint(Rationals()!c) cat "\"" : c in Eltseq(F!a)],",") cat "]";
end function;
function JQ(q)
  return "[" cat Join([JS(c) : c in Eltseq(B!q)],",") cat "]";
end function;
function JB(qs)
  return "[" cat Join([JQ(q) : q in qs],",") cat "]";
end function;
ideals := []; edges := [];
for j in [1..58] do
  nj := Valuation(Norm(rids[j]),p);
  assert Norm(rids[j]) eq p^nj;
  U,umap := NormOneGroup(LeftOrder(rids[j]) : ModScalars);
  assert #U eq e[j];
  units := [B!umap(v) : v in U];
  assert &and[Norm(v) eq 1 : v in units];
  Append(~ideals,"{\"class_index\":" cat Sprint(j-1) cat
    ",\"norm_exponent\":" cat Sprint(nj) cat
    ",\"Z_basis\":" cat JB(ZBasis(rids[j])) cat
    ",\"stabilizer_units\":" cat JB(units) cat "}");
  outgoing := 0;
  for i in [1..58] do
    if IsDefined(tps,<j,i>) then
      ts := tps[<j,i>]; assert #ts eq T[i,j];
      for k in [1..#ts] do
        t := ts[k];
        assert (Norm(t)*OF)*Norm(rids[j]) eq p*Norm(rids[i]);
        Append(~edges,"{\"source_class\":" cat Sprint(j-1) cat
          ",\"target_class\":" cat Sprint(i-1) cat
          ",\"representative_index\":" cat Sprint(k-1) cat
          ",\"quaternion\":" cat JQ(t) cat "}");
        outgoing +:= 1;
      end for;
    end if;
  end for;
  assert outgoing eq 3;
end for;
assert #edges eq 174;
printf "QUOTIENT|58 classes; 174 neighbor representatives; %o projective stabilizer elements\n",&+e;
out := "dembele/data/computed/dyadic_quotient_export_d111.json";
Write(out,"{\"status\":\"pass\",\"milestone\":\"D111\",\"seed\":990370," cat
  "\"matrix\":" cat Sprint([[Integers()!T[i,j] : j in [1..58]] : i in [1..58]]) cat "," cat
  "\"stabilizers\":" cat Sprint(e) cat ",\"base_class\":0," cat
  "\"order_Z_basis\":" cat JB(ZBasis(O)) cat "," cat
  "\"ideals\":[" cat Join(ideals,",") cat "]," cat
  "\"edges\":[" cat Join(edges,",") cat "]," cat
  "\"new_level_or_prime\":false,\"expanded_class_census\":false}" : Overwrite:=false);
print "PASS|403_dyadic_quotient_export";
