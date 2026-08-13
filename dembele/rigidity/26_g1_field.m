// Offline moduli-field verdict for the genus-1 (2@phi^2, 8@phi, 8@phi)
// passport: recognize the j-invariant (gauge-invariant!) from the dumped
// Newton solution (c4 = cfs_pts[1], c6 = cfs_pts[2]).
SetColumns(0);
load "out/g1_rep1_cfs.m";
c4 := cfs_pts[1]; c6 := cfs_pts[2];
j := 1728*c4^3/(c4^3 - c6^2);
printf "j (30 digits) = %o\n", ComplexField(30)!j;
precL := 1000; precV := 2000;
CCL := ComplexField(precL); CCV := ComplexField(precV);
for d in [1,2,4,8] do
    pol := PowerRelation(CCL!j, d : Al := "LLL");
    dd := Degree(pol);
    if dd lt 1 then continue; end if;
    ht := Max([ Abs(cf) : cf in Coefficients(pol) ]);
    if ht gt 10^(Round(precL/(2*(dd+1)))) then
        printf "deg %o: noise-floor fit (height %o), rejected\n", d, RealField(4)!Log(10,ht);
        continue;
    end if;
    resid := Abs(Evaluate(PolynomialRing(CCV)!pol, CCV!j));
    if resid lt ht * Max(1, Abs(CCV!j))^dd * 10^(-1500) then
        printf "RECOGNIZED: degree %o, height ~1e%o\n", dd, Round(Log(10, ht));
        printf "minpoly: %o\n", pol;
        QR<zz> := PolynomialRing(Rationals());
        f := QR!pol; f /:= LeadingCoefficient(f);
        K := NumberField(f);
        printf "j-field disc: %o\n", Factorization(Discriminant(Integers(K)));
        printf "optimized: %o\n", DefiningPolynomial(OptimizedRepresentation(K));
        break;
    else
        printf "deg %o: verification failed (resid 1e%o)\n", d, Round(Log(10,Max(resid,1e-9999)));
    end if;
end for;
printf "DONE\n";
quit;
