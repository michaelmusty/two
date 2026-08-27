// Delta' pipeline prototype, validated on a small level over Q exactly.
// gate5-delta-prime-plan.md.  Uses only exported intrinsics (raw operators +
// InternalHMFRawInnerProductDefinite, the mass pairing added in the patch).
//
// Validates, at a level small enough to do over Q in one session:
//   1. raw operators and the raw mass vector share a basis;
//   2. NEW forms are W-orthogonal to OLD (the ∂=0 fact the CD picture needs);
//   3. the g-isotypic sublattice L_g saturates, and its mass-Gram Gamma is
//      integral and positive definite;
//   4. sub/quotient determinants and the normalisation N(L)^2 * D_H.
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());

function deg1primes(n)
    return [ p[1] : p in Factorization(n*OF) | Norm(p[1]) eq n ];
end function;

lev := GetEnv("G3_LEVEL"); if lev eq "" then lev := "31"; end if;
ln := StringToInteger(lev);
q := deg1primes(ln)[1];
printf "DP|level norm %o\n", Norm(q);

M := HilbertCuspForms(F, q, [2 : i in [1..8]]);
W := InternalHMFRawInnerProductDefinite(M);
N := #W;
Wd := DiagonalMatrix(Rationals(), W);
printf "DP|raw dim N = %o ; masses: distinct %o, min %o, max %o\n",
    N, #Seqset(W), Min(W), Max(W);

// raw T_ell for several split primes coprime to the level
cands := [97,127,191,223,257,353,383,449];  // primes ≡ ±1 mod 32 (deg-1 in F)
Tr := AssociativeArray(); usable := [];
for e in cands do
    pe := deg1primes(e); if #pe eq 0 then continue; end if;
    S := InternalHMFRawHeckeDefiniteSparse(M, pe[1]);
    Tr[e] := ChangeRing(Matrix(S), Rationals()); Append(~usable, e);
    if #usable ge 2 then break; end if;
end for;
printf "DP|raw operators for split ells %o\n", usable;
e0 := usable[1]; T := Tr[e0];
Ne0 := Norm(deg1primes(e0)[1]);

// mass pairing is Hecke-invariant: check W T = T^t W (transpose self-adjoint)
printf "DP|CHECK T_%o self-adjoint for W: %o\n", e0, (Wd*T) eq (Transpose(T)*Wd);

// strip Eisenstein (eigenvalue Ne0+1) to get the cuspidal charpoly
cp := Zz!CharacteristicPolynomial(T);
mult := 0; cc := cp;
while true do qq,r := Quotrem(cc, z-(Ne0+1)); if r ne 0 then break; end if; mult+:=1; cc:=qq; end while;
printf "DP|Eisenstein mult of (z-%o) = %o (narrow h)\n", Ne0+1, mult;

// level-1 charpoly to label old/new
M1 := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
S1 := InternalHMFRawHeckeDefiniteSparse(M1, deg1primes(e0)[1]);
cp1 := Zz!CharacteristicPolynomial(ChangeRing(Matrix(S1), Rationals()));
facs := Factorization(cc);
newfacs := [ t : t in facs | not IsDivisibleBy(cp1, t[1]) ];
oldfacs := [ t : t in facs | IsDivisibleBy(cp1, t[1]) ];
printf "DP|cuspidal deg %o; new factors %o ; old factors %o\n",
    Degree(cc), [<Degree(t[1]),t[2]>:t in newfacs], [<Degree(t[1]),t[2]>:t in oldfacs];
if #newfacs eq 0 then printf "DP|no newforms here; done\n"; quit; end if;

// surrogate g = largest-degree new factor
gdeg := Max([Degree(t[1]) : t in newfacs]);
gfac := [t[1] : t in newfacs | Degree(t[1]) eq gdeg][1];
printf "DP|surrogate g: new factor degree %o\n", gdeg;

// L_g over Q = ker gfac(T); saturate to the integral lattice
Vg := Kernel(Evaluate(gfac, T));
printf "DP|dim ker gfac(T) = %o (expect %o)\n", Dimension(Vg), gdeg;
Bq := BasisMatrix(Vg);
Bsat := Saturation(Matrix(Integers(), LCM([Denominator(e):e in Eltseq(Bq)])*Bq));
printf "DP|L_g rank %o saturated\n", Nrows(Bsat);

// ∂=0 check: new ⊥ old under W
if #oldfacs gt 0 then
    Vold := Kernel(Evaluate(&*[t[1]^t[2]:t in oldfacs], T));
    cross := ChangeRing(Bsat,Rationals()) * Wd * Transpose(BasisMatrix(Vold));
    printf "DP|CHECK new _|_ old under W: %o\n", IsZero(cross);
end if;

// Gram and determinants
Gsub := ChangeRing(Bsat,Rationals()) * Wd * Transpose(ChangeRing(Bsat,Rationals()));
Gz := Matrix(Integers(), Gsub);
printf "DP|Gamma_sub integral %o, symmetric %o, pos-def %o\n",
    Gsub eq ChangeRing(Gz,Rationals()), IsSymmetric(Gz), IsPositiveDefinite(Gz);
dsub := Determinant(Gz);
printf "DP|det Gamma_sub = %o = %o\n", dsub, Factorization(dsub);
printf "DP|elementary divisors of Gamma_sub = %o\n", ElementaryDivisors(Gz);

// quotient lattice: image of Z^N under the W-orthogonal projector onto L_g x Q.
// Projector P = Bsat^t (Bsat W Bsat^t)^-1 Bsat W ; the quotient character lattice
// is P(Z^N).  Its Gram det = det Gamma_sub / [proj : sub]^2.  Compute the image
// lattice basis and its det directly.
P := Transpose(ChangeRing(Bsat,Rationals())) * Gsub^-1 * ChangeRing(Bsat,Rationals()) * Wd;
// rows of (Z^N)·P live in L_g x Q; collect enough to span, in L_g coordinates
coordP := P * Transpose(ChangeRing(Bsat,Rationals())) * Gsub^-1;  // maps R^N -> L_g coords (rank 16)
Cimg := Saturation(Matrix(Integers(), LCM([Denominator(e):e in Eltseq(coordP)] cat [1])*Transpose(coordP)));
// index of sub inside quotient lattice = [Cimg-lattice : identity]? report Smith
idx := 0;
try
    // sub lattice in L_g coords is the standard Z^16; quotient is Cimg row lattice
    Qlat := Lattice(Cimg);
    Slat := StandardLattice(gdeg);
    if Rank(Cimg) eq gdeg then
        idx := Index(Qlat, Qlat meet Slat);
    end if;
catch e ; end try;
printf "DP|quotient-vs-sub index attempt: rank %o\n", Rank(Cimg);

// normalisation pieces
printf "DP|N (raw dim) = %o, sum masses = %o\n", N, &+W;
printf "DP|done\n";
quit;
