// Gate 3: verify the oldform baseline, which the whole excess argument rests on.
//
// At level q0 the factor f1 has multiplicity 4 in charpoly(T_31 mod 2).  I read
// that as "oldform baseline 2, excess 2".  But the baseline is 2 * m1, where m1
// is the multiplicity of f1 in the charpoly at LEVEL 1 -- each level-1 form with
// residual system f1 contributes two oldforms.  I assumed m1 = 1 (i.e. V16 is
// the only level-1 component with that residual system).  If m1 = 2 the baseline
// is 4 and the observed excess is ZERO, and the gate-3 evidence collapses.
//
// This is a 58 x 58 computation.  Worth doing before anything else.
SetColumns(0);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2); F2z<zz> := PolynomialRing(F2);
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;

M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M1) eq 57;
T := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
printf "B|level 1 raw dim %o\n", Nrows(T);

cpZ := Zz!CharacteristicPolynomial(T);
cp1, rem := Quotrem(cpZ, z - (Norm(p31)+1));       // strip Eisenstein
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
fac16 := Factorization(F2z!g16);
printf "B|g16 mod 2 factors: %o\n", [<Degree(t[1]), t[2]> : t in fac16];

// multiplicity of each degree-8 factor in the FULL level-1 charpoly mod 2
cpbar := F2z!cpZ;
printf "B|full level-1 charpoly mod 2, degree %o\n", Degree(cpbar);
for t in fac16 do
    h := t[1];
    m := 0; cc := cpbar;
    while true do
        q, r := Quotrem(cc, h);
        if r ne 0 then break; end if;
        m +:= 1; cc := q;
    end while;
    printf "B|RESULT deg-8 factor: multiplicity m1 = %o at level 1  => oldform baseline at q0 = %o\n",
        m, 2*m;
end for;
printf "B|observed at q0 was 4 and 2\n";
printf "B|done\n";
quit;
