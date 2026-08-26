// Gate 3, step 7 strengthened: eigensystem match at FOUR primes.
//
// Design note.  The kernels are the expensive part (~1.7 h each); building an
// operator is 20 min to 2 h.  So compute each kernel ONCE and restrict every
// operator to it, rather than repeating the whole test per prime.
//
// Everything must be in ONE session: the package's internal basis is not
// reproducible across sessions (see gate3-method-audit.md), so banked operators
// from different runs cannot be combined.  That is why T_31 and T_97 are rebuilt
// here rather than loaded.
//
// This also fixes a reporting gap: it prints WHICH level-1 factor matches, not
// just the degree, so the correspondence can be checked for consistency.
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
q0  := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
prs := [p31];
for q in [97, 127, 191] do
    pp := [ p[1] : p in Factorization(q*OF) | Norm(p[1]) eq q ];
    if #pp gt 0 then Append(~prs, pp[1]); end if;
end for;
printf "MP|primes: %o\n", [Norm(p) : p in prs];

// --- level 1: V16 and the residual invariant for each prime ---
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
T31_1 := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, p31));
cp1, rem := Quotrem(Zz!CharacteristicPolynomial(T31_1), z - (Norm(p31)+1));
assert rem eq 0;
g16 := [ f[1] : f in Factorization(cp1) | Degree(f[1]) eq 16 ][1];
B16 := BasisMatrix(Kernel(Evaluate(g16, ChangeRing(T31_1, Rationals()))));
inv := AssociativeArray();
for pr in prs do
    Tl := Matrix(InternalHMFRawHeckeDefiniteSparse(M1, pr));
    cpl := Zz!CharacteristicPolynomial(Solution(B16, B16 * ChangeRing(Tl, Rationals())));
    inv[Norm(pr)] := [ t[1] : t in Factorization(F2z!cpl) ];
    printf "MP|level-1 invariant at %o: %o factors of degrees %o\n",
        Norm(pr), #inv[Norm(pr)], [Degree(h) : h in inv[Norm(pr)]];
end for;
fac31 := inv[31];

// --- level q0: all operators, one session ---
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
printf "MP|level q0 dim %o\n", Dimension(M);
A := AssociativeArray();
for pr in prs do
    t0 := Cputime();
    S := InternalHMFRawHeckeDefiniteSparse(M, pr);
    A[Norm(pr)] := Matrix(ChangeRing(S, F2));
    printf "MP|T_%o built [%o s], %o per column\n",
        Norm(pr), Cputime(t0), RealField(6)!(#Support(S)/Ncols(S));
end for;
// commutativity sanity check across the whole set
V := VectorSpace(F2, Ncols(A[31])); bad := 0;
for i in [1..3] do
    v := Random(V);
    for pr in prs do for ps in prs do
        if (v*A[Norm(pr)])*A[Norm(ps)] ne (v*A[Norm(ps)])*A[Norm(pr)] then bad +:= 1; end if;
    end for; end for;
end for;
printf "MP|COMMUTE all pairs: failures %o\n", bad;
if bad ne 0 then printf "MP|ABORT: operators do not commute\n"; quit; end if;

// --- kernel once per residual factor, then restrict every operator ---
for idx in [1..#fac31] do
    f1 := fac31[idx][1];
    t0 := Cputime();
    W := Kernel(Evaluate(f1, A[31]));
    printf "MP|=== T_31 factor %o: dim ker = %o [%o s]\n", idx, Dimension(W), Cputime(t0);
    if Dimension(W) eq 0 then continue; end if;
    BW := BasisMatrix(W);
    for pr in prs do
        n := Norm(pr);
        R := Solution(BW, BW * A[n]);
        cw := CharacteristicPolynomial(R);
        matched := [ j : j in [1..#inv[n]] | IsDivisibleBy(cw, inv[n][j]) ];
        printf "MP|  T_%o on W: charpoly factors %o ; matches level-1 invariant factor INDEX %o\n",
            n, [<Degree(t[1]), t[2]> : t in Factorization(cw)], matched;
    end for;
end for;
printf "MP|done\n";
quit;
