// Offline feasibility checks for a curve-first construction. No curve model
// is claimed. T31 input is the bank from script 58; T97 target polynomials
// are the two level-one factors printed by that script's confirmation.
SetColumns(0);
SetQuitOnError(true);
Z<z> := PolynomialRing(Integers());
P<x> := PolynomialRing(GF(2));
bank := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
cp40 := Z!bank[2]; cp48 := Z!bank[3];
assert Degree(cp40) eq 40 and Degree(cp48) eq 48;
quartics := [a[1] : a in Factorization(cp40) | Degree(a[1]) eq 4];
assert #quartics eq 4;
// Under the proposed Atkin-Lehner quotient: 16 old + 48 new = genus 64.
cp64 := (&*quartics)*cp48;
assert Degree(cp64) eq 64;
function frobpoly(f)
    d := Degree(f);
    return &+[ Coefficient(f,i)*x^(d-i)*(x^2+1)^i : i in [0..d] ];
end function;
chi := frobpoly(P!cp64);
assert Degree(chi) eq 128;
traces31 := [x^8+x^4+x^3+x+1, x^8+x^6+x^5+x^2+1];
traces97 := [x^8+x^4+x^3+x^2+1, x^8+x^6+x^5+x+1];
for ell in [31,97] do
    traces := ell eq 31 select traces31 else traces97;
    for h in traces do
        psi := frobpoly(h);
        fac := Factorization(psi);
        orders := [];
        for a in fac do
            L<r> := ext<GF(2) | a[1]>;
            Append(~orders, Order(r));
        end for;
        assert Degree(psi) eq 16 and GCD(psi,Derivative(psi)) eq 1;
        if ell eq 31 then
            assert chi mod psi eq 0;
            assert GCD(psi,ExactQuotient(chi,psi)) eq 1;
        end if;
        printf "R64|prime %o; trace polynomial %o; torsion polynomial %o; factor degrees %o; root orders %o\n", ell,h,psi,[Degree(a[1]) : a in fac],orders;
    end for;
end for;
print "R64|T31: both target 16-dimensional F2 torsion factors are coprime to their cofactors in the proposed genus-64 Euler polynomial";
// Finite-group and Riemann-Hurwitz consistency, conditional on the level
// cover and involution having the indicated canonical-model realizations.
gC := 16; gX := 40; gZ := 136; gY := 64;
assert 2*gX-2 eq 2*(2*gC-2)+18;
assert 2*gZ-2 eq 3*(2*gX-2)+18*2;
assert 2*gZ-2 eq 2*(2*gY-2)+18;
assert 2*gY-2 eq 3*(2*gC-2)+18+9*2;
print "R64|Riemann-Hurwitz checks: X40 -> C16 degree 2, Z136 -> X40 degree 3, Z136 -> Y64 degree 2, Y64 -> C16 degree 3";
orbC := 2*gC-2 + 17*(1-1/2) + 9*(1-1/3) + (1-1/32);
orbY := 2*gY-2 + 17*(1-1/2) + (1-1/16) + (1-1/32);
orbZ := 2*gZ-2 + 3*(1-1/16);
assert orbY eq 3*orbC and orbZ eq 6*orbC;
print "R64|predicted orbifold signatures: Y (64; 2^17,16,32), Z (136; 16^3); co-area ratios to C are 3 and 6";
printf "R64|nonzero vectors %o; projective lines %o; vectors/line %o; order-51 Frobenius vector orbits %o\n", 256^2-1,257,255,(256^2-1) div 51;
// If genus 64 carrier is correct, it cannot be hyperelliptic: hyperelliptic
// 2-torsion is controlled by at most 130 branch points, whereas SL2(256)
// has an element of prime order 257.
assert 2*gY+2 lt 257;
print "PASS|64_curve_first_frobenius";
quit;
