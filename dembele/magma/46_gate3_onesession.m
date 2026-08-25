// Gate 3: recompute BOTH operators in ONE session, prove they commute, then do
// the eigensystem test.
//
// The banked T_31 and T_97 do not commute (5/5 random vectors).  Two possible
// causes, and they must be distinguished:
//   (a) different bases -- they were assembled in separate Magma sessions, and
//       the package's internal ordering need not be reproducible.  Benign for
//       characteristic polynomials, which are basis-independent, so the
//       multiplicity results stand; only JOINT analysis is affected.
//   (b) the sparse patch produces wrong operators at level q0 -- which would
//       invalidate everything built on them.
// Computing both in one session decides it: same basis by construction, so they
// MUST commute if the assembly is correct.
SetColumns(0);
SetMemoryLimit(StringToInteger(GetEnv("G3_MEMCAP"))*1024^3);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
F2 := GF(2); F2z<zz> := PolynomialRing(F2);
g31e := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31e>;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];
q0  := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];

// --- level-1 invariants (same session, so consistent) ---
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
T31_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp1, rem := Quotrem(Zz!CharacteristicPolynomial(T31_1), z - (Norm(p31)+1));
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
B16 := BasisMatrix(Kernel(Evaluate(g16, ChangeRing(T31_1, Rationals()))));
fac31 := Factorization(F2z!g16);
T97_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p97));
cp16_97 := Zz!CharacteristicPolynomial(Solution(B16, B16 * ChangeRing(T97_1, Rationals())));
fac97 := Factorization(F2z!cp16_97);
printf "O|level-1 invariants: 31 -> %o, 97 -> %o\n",
    [Degree(t[1]) : t in fac31], [Degree(t[1]) : t in fac97];

// --- BOTH level-q0 operators in this one session ---
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
printf "O|level q0 dim %o\n", Dimension(M);
t0 := Cputime();
S31 := InternalHMFRawHeckeDefiniteSparse(M, p31);
printf "O|T_31 built [%o s], %o per column\n", Cputime(t0), RealField(6)!(#Support(S31)/Ncols(S31));
t0 := Cputime();
S97 := InternalHMFRawHeckeDefiniteSparse(M, p97);
printf "O|T_97 built [%o s], %o per column\n", Cputime(t0), RealField(6)!(#Support(S97)/Ncols(S97));
Write("gate3_T31_same.m", Sprintf("T31s := %m;", S31) : Overwrite := true);
Write("gate3_T97_same.m", Sprintf("T97s := %m;", S97) : Overwrite := true);

A := ChangeRing(S31, F2); B := ChangeRing(S97, F2);
n := Ncols(A); V := VectorSpace(F2, n);
bad := 0;
for i in [1..8] do v := Random(V); if (v*A)*B ne (v*B)*A then bad +:= 1; end if; end for;
printf "O|COMMUTE(same session)=%o  (failures %o of 8)\n", bad eq 0, bad;
if bad ne 0 then
    printf "O|VERDICT: assembly is WRONG at level q0 -- not a basis artefact\n";
    printf "O|done\n"; quit;
end if;
printf "O|VERDICT: the banked mismatch was a BASIS artefact; charpoly results stand\n";

// --- eigensystem test, now legitimate ---
Ad := Matrix(A); Bd := Matrix(B);
for idx in [1..#fac31] do
    f1 := fac31[idx][1];
    t0 := Cputime();
    W := Kernel(Evaluate(f1, Ad));
    printf "O|factor %o: dim ker f(T_31) = %o [%o s]\n", idx, Dimension(W), Cputime(t0);
    if Dimension(W) eq 0 then continue; end if;
    BW := BasisMatrix(W);
    R97 := Solution(BW, BW * Bd);
    printf "O|  charpoly(T_97|W) = %o\n", [<Degree(t[1]), t[2]> : t in Factorization(CharacteristicPolynomial(R97))];
    printf "O|  level-1 a_97 invariant factors: %o\n", [Degree(t[1]) : t in fac97];
    for t in Factorization(CharacteristicPolynomial(R97)) do
        for s in fac97 do
            if t[1] eq s[1] then
                printf "O|  MATCH deg-%o factor of the level-1 a_97 invariant, multiplicity %o\n", Degree(t[1]), t[2];
            end if;
        end for;
    end for;
end for;
printf "O|done\n";
quit;
