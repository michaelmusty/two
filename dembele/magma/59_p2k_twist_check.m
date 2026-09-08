// Companion to 58_levelraise_p2k.m (D39).  At level p2^4 the residual system
// is carried by char-0 new orbits of degrees 16, 48, 64, 72 -- the degrees of
// Dembélé's form and of the p2^2-, p2^3-new orbits.  Test the explanation:
// they are twists by the quadratic character chi of Q(zeta_32)/F, whose
// conductor is p2^2, so f (x) chi has conductor p2^4 and a depth-zero or
// depth-1/2 supercuspidal (x) chi has conductor p2^4.  Twisting sends
// charpoly(T_31)(t) to charpoly(chi(p31) t) with chi(p31) = +-1.
//
// Also banks every new charpoly cp_new(k), k = 0..4, to
// dembele/data/computed/levelraise_p2k_charpolys.m (58 did not).
// Output markers: R59|...
SetColumns(0);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2);
F2z<zz> := PolynomialRing(F2);
wt := [2 : i in [1..8]];
p2 := Factorization(2*OF)[1][1];
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;

// chi = character of Q(zeta_32)/F = F(sqrt(-1)); its conductor and chi(p31)
Fy<y> := PolynomialRing(F);
L := ext<F | y^2 + 1>;
OL := Integers(L);
disc := Discriminant(OL);
printf "R59|relative discriminant of F(i)/F = p2^%o (norm %o)\n", Valuation(disc, p2), Norm(disc);
dec := Decomposition(OL, p31);
chi31 := #dec eq 2 select 1 else -1;
printf "R59|p31 in F(i)/F: %o prime(s) above => chi(p31) = %o\n", #dec, chi31;

expected_new := [ 58, 40, 48, 136, 281 ];
cpnew := [];
bankin := GetEnv("BANK_IN");
if bankin ne "" then
    // replay mode: load cp_new from a previous run's bank instead of rebuilding T_31
    cpnew := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
    printf "R59|loaded banked cp_new, degrees %o\n", [ Degree(c) : c in cpnew ];
else
for k in [0..4] do
    t0 := Cputime();
    M := HilbertCuspForms(F, p2^k, wt);
    T := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p31));
    cpk := Zz!CharacteristicPolynomial(T);
    if k eq 0 then
        Append(~cpnew, cpk);
    else
        old := &*[ cpnew[j+1]^(k-j+1) : j in [0..k-1] ];
        Append(~cpnew, ExactQuotient(cpk, GCD(cpk, old)));
    end if;
    printf "R59|k=%o raw dim %o, T31 [%o s], new degree %o (expected %o)\n", k, Nrows(T), Cputime(t0), Degree(cpnew[k+1]), expected_new[k+1];
end for;
end if;
assert [ Degree(c) : c in cpnew ] eq expected_new;

// bank (skipped in replay mode)
if bankin eq "" then
bank := GetEnv("BANK_OUT");
if bank eq "" then bank := "dembele/data/computed/levelraise_p2k_charpolys.m"; end if;
fh := Open(bank, "w");
fprintf fh, "// cp_new[k+1] = charpoly of T_31 on the p2^k-new part of the raw level-p2^k Brandt module, k = 0..4 (k = 0 raw level 1 incl. Eisenstein t-32). D39. Pure Magma expression (a sequence of 5 polynomials in z): use  cp_new := eval Read(file);  after  Zz<z> := PolynomialRing(Integers());\n";
fprintf fh, "[\n";
for k in [0..4] do
    fprintf fh, "%o%o\n", cpnew[k+1], k lt 4 select "," else "";
end for;
fprintf fh, "]\n";
delete fh;
printf "R59|banked to %o\n", bank;
end if;

// twist accounting at level p2^4
facs4 := Factorization(cpnew[5]);
lower := [ <j, h[1]> : h in Factorization(cpnew[j+1]), j in [0..3] ];
twist := func< h | Zz!(Evaluate(h, chi31*z) * (chi31 eq -1 and IsOdd(Degree(h)) select -1 else 1)) >;
explained := 0;
for h in facs4 do
    hits := [ l[1] : l in lower | l[2] eq twist(h[1]) ];
    same := [ l[1] : l in lower | l[2] eq h[1] ];
    printf "R59|k=4 new factor deg %o mult %o: chi-twist of a level-p2^j new factor for j in %o ; identical (untwisted) to one for j in %o\n",
        Degree(h[1]), h[2], hits, same;
    if #hits gt 0 then explained +:= h[2]*Degree(h[1]); end if;
end for;
printf "R59|k=4: degree %o of the new part explained by chi-twists, %o twist-minimal\n", explained, Degree(cpnew[5]) - explained;
// residual carriers among the twist-minimal part
res := [ zz^8 + zz^4 + zz^3 + zz + 1, zz^8 + zz^6 + zz^5 + zz^2 + 1 ];
tmfacs := [ h[1]^h[2] : h in facs4 | #[ l : l in lower | l[2] eq twist(h[1]) ] eq 0 ];
tm := #tmfacs eq 0 select Zz!1 else &*tmfacs;
printf "R59|k=4 twist-minimal part: degree %o, residual multiplicities %o\n", Degree(tm), [ Valuation(F2z!tm, f) : f in res ];
// the level-1 Eisenstein line (t-32) must NOT reappear twisted (chi.Nrd is not level-p2^4 invariant)
printf "R59|k=4 contains t+32 (twisted Eisenstein)? %o (expect false)\n", Evaluate(cpnew[5], -32) eq 0;
printf "R59|k=4 accounting: 57 level-1 cusp twists + 40 + 48 + 136 = %o vs new dim %o\n", 57+40+48+136, Degree(cpnew[5]);
// same accounting at k = 3 and k = 2 (twists of lower levels landing at p2^3 or p2^2 would be a surprise)
for k in [2,3] do
    facsk := Factorization(cpnew[k+1]);
    lowk := [ <j, h[1]> : h in Factorization(cpnew[j+1]), j in [0..k-1] ];
    ex := &+[ Integers() | h[2]*Degree(h[1]) : h in facsk | #[ l : l in lowk | l[2] eq twist(h[1]) ] gt 0 ];
    printf "R59|k=%o: degree %o of the new part is a chi-twist of a lower level (expect 0)\n", k, ex;
end for;
print "PASS|59_p2k_twist_check";
quit;
