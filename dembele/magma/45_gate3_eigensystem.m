// Gate 3, the real test: isolate the f1-eigenspace at level q0 and read its
// eigensystem, rather than counting multiplicities.
//
// The multiplicity method shows the residual invariant appears more often than
// oldforms explain.  It does NOT show that the extra forms have f's eigensystem
// -- matching at two primes is not an eigensystem, and a shared minimal
// polynomial permits a Galois conjugate (audit step 7).
//
// Here: W = ker f1(T_31) at level q0.  T_97 commutes with T_31 so preserves W,
// and dim W <= 32, so on W the comparison is exact.  If the extra forms carry
// f's residual system, charpoly(T_97|W) must be built from the SAME degree-8
// factor that f's a_97 satisfies -- computed independently from V16 at level 1.
//
// Both operators are already banked, so this costs only the polynomial
// evaluation: f1 has degree 8, so ~8 dense GF(2) multiplies at ~22 min each.
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

// --- level 1: the two residual invariants, for 31 and for 97 ---
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
printf "E|level-1 invariant at 31: %o\n", [Degree(t[1]) : t in fac31];
printf "E|level-1 invariant at 97: %o\n", [Degree(t[1]) : t in fac97];

// --- level q0: W = ker f1(T_31) for EACH degree-8 factor ---
load "gate3_T31_sparse.m";
load "gate3_T97_sparse.m";
A31 := Matrix(ChangeRing(T31, F2));
A97 := Matrix(ChangeRing(T97, F2));
printf "E|operators densified\n";

for idx in [1..#fac31] do
    f1 := fac31[idx][1];
    t0 := Cputime();
    W := Kernel(Evaluate(f1, A31));
    printf "E|factor %o (deg %o): dim ker f(T_31) = %o [%o s]\n",
        idx, Degree(f1), Dimension(W), Cputime(t0);
    if Dimension(W) eq 0 then continue; end if;
    BW := BasisMatrix(W);
    R97 := Solution(BW, BW * A97);              // T_97 restricted to W
    cpW := CharacteristicPolynomial(R97);
    printf "E|  charpoly(T_97|W) factors: %o\n",
        [<Degree(t[1]), t[2]> : t in Factorization(cpW)];
    printf "E|  level-1 a_97 factors were: %o\n", [Degree(t[1]) : t in fac97];
    for t in Factorization(cpW) do
        for s in fac97 do
            if t[1] eq s[1] then
                printf "E|  MATCH: degree-%o factor of the level-1 a_97 invariant occurs, multiplicity %o\n",
                    Degree(t[1]), t[2];
            end if;
        end for;
    end for;
end for;
printf "E|done\n";
quit;
