// Analyze the degree-8 moduli field of cover 1 of the (2,4,8) passport,
// from the recognized minimal polynomial of T1 (coefficient of the octuple-pole
// factor), and check ramification of the field.
SetColumns(0);
R<z> := PolynomialRing(Rationals());
// T1 minpoly from 12_recognize_248_factors.m output (rep 1):
f := 5*z^8 + 400*z^7 + 46320*z^6 + 664256*z^5 + 4898528*z^4 + 6182656*z^3 - 15575296*z^2 - 106212352*z + 154400000;
f /:= LeadingCoefficient(f);
K<t1> := NumberField(f);
printf "K degree %o\n", Degree(K);
ZK := Integers(K);
dK := Discriminant(ZK);
printf "disc(K) = %o\n", Factorization(dK);
printf "Galois group of K: %o\n", GaloisGroup(K);
L := OptimizedRepresentation(K);
printf "polredabs-style model: %o\n", DefiningPolynomial(L);
// subfields
subs := Subfields(K);
printf "subfields:\n";
for s in subs do
    if Degree(s[1]) in {2,4} then
        printf "  deg %o: %o (disc %o)\n", Degree(s[1]),
            DefiningPolynomial(OptimizedRepresentation(s[1])),
            Factorization(Discriminant(Integers(s[1])));
    end if;
end for;
quit;
