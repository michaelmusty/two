// Archimedean probe (review 2026-09-08 §3(d)): the Shimura curve X_p2 over
// F = Q(zeta_32)^+ for the quaternion algebra ramified at p2 and seven real
// places. Area 571 (genus 40) is inside the range where Voight's fundamental
// domain algorithm has been run; the base field (degree 8, disc 2^31) is the
// stress. Prints signature/area, then attempts FundamentalDomain under the
// shell's CPU cap. Output markers: R61|...
SetColumns(0);
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
p2 := Factorization(2*OF)[1][1];
inf := InfinitePlaces(F);
// ramify at p2 and at all real places except the first
B := QuaternionAlgebra(p2, inf[2..8]);
printf "R61|algebra: disc %o, ramified real places %o, definite %o\n", Norm(Discriminant(B)), #RamifiedPlaces(B), IsDefinite(B);
O := MaximalOrder(B);
t0 := Cputime();
G := FuchsianGroup(O);
printf "R61|FuchsianGroup created [%o s]\n", Cputime(t0);
t0 := Cputime();
printf "R61|ArithmeticVolume %o [%o s]\n", ArithmeticVolume(G), Cputime(t0);
t0 := Cputime();
sig := Signature(G);
printf "R61|Signature (genus; elliptic orders) %o [%o s]\n", sig, Cputime(t0);
t0 := Cputime();
D := FundamentalDomain(G);
printf "R61|FundamentalDomain: %o sides [%o s]\n", #D, Cputime(t0);
t0 := Cputime();
gens := Generators(G);
printf "R61|Generators: %o [%o s]\n", #gens, Cputime(t0);
print "PASS|61_fuchsian_p2_probe";
quit;
