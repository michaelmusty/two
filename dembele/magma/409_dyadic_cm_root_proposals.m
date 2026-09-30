// D112 finite algebraic root proposals, independently Hensel-certified later.
// This is the fixed degree-17 CM residue polynomial, not a new target search.
SetColumns(0); SetQuitOnError(true); SetMemoryLimit(2000000000);
Q2 := pAdicField(2,48); P<x> := PolynomialRing(Q2);
fM := x^16+16*x^14+104*x^12+352*x^10+660*x^8+672*x^6+336*x^4+64*x^2+2;
M<beta> := ext<Q2 | fM>; R<z> := PolynomialRing(M);
cs := [68,-2,-128,16,80,40,32,-80,-32,64,0,-16,16,8,0,0,-2,1];
roots := Roots(R!cs); assert #roots eq 17 and &and[r[2] eq 1 : r in roots];
function JS(z)
  row := Eltseq(z); assert #row eq 16;
  return "[" cat Join(["\"" cat Sprint(Rationals()!c) cat "\"" : c in row],",") cat "]";
end function;
out := "dembele/data/computed/dyadic_cm_root_proposals_d112.json";
Write(out,"{\"status\":\"proposals\",\"milestone\":\"D112\",\"base_precision_binary\":48," cat
  "\"CM_polynomial\":[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]," cat
  "\"root_polynomial\":" cat Sprint(cs) cat ",\"root_centers\":[" cat
  Join([JS(r[1]) : r in roots],",") cat "]}" : Overwrite:=false);
print "ROOTS|17 proposals over the ramified degree-16 completion";
print "PASS|409_dyadic_cm_root_proposals";
