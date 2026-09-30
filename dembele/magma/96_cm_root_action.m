// D59: an arithmetic-to-complex comparison for Elkies's CM residue field.
// Run locally with magma -b. The polynomial is not the nonsolvable target.
SetColumns(0);
SetSeed(59);
Z := Integers();
R<t> := PolynomialRing(Rationals());
f := t^17-2*t^16+8*t^13+16*t^12-16*t^11+64*t^9-32*t^8
     -80*t^7+32*t^6+40*t^5+80*t^4+16*t^3-128*t^2-2*t+68;
GC, rc, SC := GaloisGroup(f : Type := "Complex", Prec := 100);
GP, rp, SP := GaloisGroup(f : Prime := 31);
assert #GC eq 272 and #GP eq 272 and IsSolvable(GP);
assert GaloisProof(f, SP);
perm := GaloisGroupConjugation(SC, SP);
assert GC^perm eq GP;
print "GROUP_ORDER|", #GP;
print "PADIC_PROOF|true";
print "COMPLEX_TO_PADIC|", [i^perm : i in [1..17]];
print "COMPLEX_GENERATORS|", [[i^g : i in [1..17]] : g in Generators(GC)];
rp := [GaloisRoot(i, SP : Prec := 80) : i in [1..17]];
k, red := ResidueClassField(Parent(rp[1]));
assert Characteristic(k) eq 31 and Degree(k) eq 17;
pf := Sym(17)![Index([red(r) : r in rp], red(r)^31) : r in rp];
assert pf in GP and Order(pf) eq 17;
cf := perm*pf*perm^-1;
assert cf in GC;
print "PADIC_FROBENIUS|", [i^pf : i in [1..17]];
print "COMPLEX_FROBENIUS|", [i^cf : i in [1..17]];
for i in [1..17] do
    printf "ROOT|%o|%o|%o\n", i, Real(rc[i]), Imaginary(rc[i]);
end for;

// The normal C17 fixes kappa=sum_j r_j^2*r_Frob(j). Its sixteen
// conjugates are obtained by replacing Frob by its nonidentity powers.
assert IsNormal(GP, sub<GP | pf>);
vals := [&+[rp[j]^2*rp[j^(pf^a)] : j in [1..17]] : a in [1..16]];
pol := &*[PolynomialRing(Parent(rp[1])).1-v : v in vals];
// Rouche gives |r_j|<4, hence |kappa|<1088. Every coefficient is
// bounded by (1+1088)^16; 70 base-31 digits suffice for unique lifting.
assert &+[Abs(Coefficient(f,j))*4^j : j in [0..16]] lt 4^17;
pp := 31^70;
assert pp gt 2*1089^16;
QP := pAdicField(31,80);
coeff := [];
for c in Coefficients(pol) do
    n := (Z!QP!c) mod pp;
    if n gt pp div 2 then n -:= pp; end if;
    Append(~coeff,n);
end for;
assert Maximum([Abs(v) : v in coeff]) lt 1089^16;
assert IsIrreducible(R!coeff);
print "RESOLVENT|", coeff;
print "RESOLVENT_COEFFICIENT_BOUND|", 1089^16;
print "LIFT_MODULUS|", pp;
print "PADIC_KAPPA_MOD31_60|", (Z!QP!vals[1]) mod 31^60;
cval := &+[rc[j]^2*rc[j^cf] : j in [1..17]];
print "COMPLEX_KAPPA|", Real(cval), "|", Imaginary(cval);
print "COMPLEX_RESOLVENT_RESIDUAL|", Abs(Evaluate(R!coeff,cval));
assert Abs(Evaluate(R!coeff,cval)) lt 10^-65;
print "PASS|96_cm_root_action";
quit;
