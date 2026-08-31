// Delta' at q0, final step: combine the per-prime L_g banks (from
// 52_delta_prime_q0_lg.m) into the exact saturated lattice, and form the
// mass-pairing Gram determinants (gate5-delta-prime-plan.md, Addendum).
//
//   1. Read all banks LG_OUT_p*.m (p, pivs, Brows).  Keep the majority pivot
//      set; discard mismatched primes (non-generic reductions).
//   2. Entrywise CRT (iterative, matrix-level) of the reduced echelon bases:
//      canonical w.r.t. the common pivot set, hence CRT-compatible.
//   3. Rational reconstruction entry-by-entry; failure => need more primes
//      (reported, exit).  Clear denominators per row, saturate over Z.
//   4. EXACT certificate: B * h_g(T) = 0 over Z (Horner with the banked T).
//   5. Gamma_sub = B W B^t with the mass vector from 50 (dp_W.m);
//      det, elementary divisors, positive-definiteness.
//   6. Quotient lattice: image of Z^N under the W-orthogonal projection onto
//      L_g x Q, in B-coordinates: rows of DW * B^t * Gamma^{-1}.  Z^d is a
//      sublattice of it; det Gamma_quot = det Gamma_sub / idx^2.
//
// The normalisation Delta' = det/(N(L)^2 * D_{K_g}) needs the maximal order
// of K_g = Q[z]/h_g (disc factorization may be hard); this script reports
// det, elementary divisors, and disc(h_g) so the certificate step can decide
// the valuations it needs.
//
// Env: G3_MEMCAP (GB), LG_TBANK (banked sparse integer T, same basis as W!),
//      LG_HG (file: hg := [c0..1]), LG_WBANK (file: Wmass := [...]),
//      LG_BANKS (comma-separated bank files from 52).
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
Zz<z> := PolynomialRing(Integers());

function readAssign(path)   // file of "name := expr;\n" lines -> list of exprs
    txt := Read(path);
    parts := Split(txt, ";");
    vals := [* *];
    for s in parts do
        i := Index(s, ":=");
        if i eq 0 then continue; end if;
        Append(~vals, eval s[i+2..#s]);
    end for;
    return vals;
end function;

txt := Read(GetEnv("LG_TBANK"));
i0 := Index(txt, ":="); j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
T := eval txt[i0+2..j0-1];
N := Ncols(T);
printf "CB|T loaded: %o x %o\n", Nrows(T), N;

hgv := readAssign(GetEnv("LG_HG"));
hgcf := hgv[1]; hgZ := Zz!hgcf; d := Degree(hgZ);
Wv := readAssign(GetEnv("LG_WBANK"));
W := Wv[1];
error if #W ne N, "mass vector length differs from T dimension";
printf "CB|h_g degree %o; mass vector: distinct %o, min %o, max %o\n",
    d, #Seqset(W), Min(W), Max(W);

banks := [* *];
for f in Split(GetEnv("LG_BANKS"), ",") do
    v := readAssign(f);           // p, pivs, Brows
    Append(~banks, <v[1], v[2], v[3]>);
    printf "CB|bank %o: p = %o, pivots %o...\n", f, v[1], v[2][1..Min(4,#v[2])];
end for;
error if #banks eq 0, "no banks";

// majority pivot set
pivsets := {* b[2]^^1 : b in banks *};
maxmult := Max([ Multiplicity(pivsets, s) : s in MultisetToSet(pivsets) ]);
pivs := [ s : s in MultisetToSet(pivsets) | Multiplicity(pivsets, s) eq maxmult ][1];
use := [ b : b in banks | b[2] eq pivs ];
printf "CB|using %o/%o banks with the majority pivot set\n", #use, #banks;

// iterative entrywise CRT, matrix-level
Bcrt := Matrix(Integers(), d, N, use[1][3]);
Mod := use[1][1];
for k in [2..#use] do
    p := use[k][1];
    Bp := Matrix(GF(p), d, N, use[k][3]);
    Dk := Bp - ChangeRing(Bcrt, GF(p));
    Minv := (GF(p)!(Mod mod p))^-1;
    Bcrt := Bcrt + Mod * ChangeRing(Minv*Dk, Integers());
    Mod *:= p;
end for;
printf "CB|CRT done: modulus %o bits\n", Ilog2(Mod)+1;

// rational reconstruction
RM := Integers(Mod);
BQ := Matrix(Rationals(), d, N, []);
fails := 0;
for i in [1..d] do
    for j in [1..N] do
        c := Bcrt[i,j];
        if c eq 0 then continue; end if;
        ok, q := RationalReconstruction(RM!c);
        if not ok then fails +:= 1; else BQ[i,j] := q; end if;
    end for;
end for;
if fails gt 0 then
    printf "CB|FAIL rational reconstruction failed on %o entries: need more primes\n", fails;
    quit;
end if;
printf "CB|rational reconstruction complete\n";

// integral, saturated basis
den := LCM([ Denominator(e) : e in Eltseq(BQ) ] cat [1]);
BZ := Matrix(Integers(), den*BQ);
BS := Saturation(BZ);
printf "CB|saturated basis: %o x %o, entry height ~2^%o\n",
    Nrows(BS), N, Ilog2(Max([Abs(e): e in Eltseq(BS)] cat [1]));

// exact certificate: BS * hg(T) = 0 over Z (Horner on rows)
Tz := T;   // sparse integer
okall := true;
for i in [1..d] do
    v := Vector(BS[i]);
    w := hgcf[#hgcf]*v;
    for k := #hgcf-1 to 1 by -1 do w := w*Tz + hgcf[k]*v; end for;
    okall and:= IsZero(w);
end for;
printf "CB|CHECK B * h_g(T) = 0 over Z: %o\n", okall;
error if not okall, "reconstructed lattice is not h_g(T)-annihilated: more primes or bug";

// Gram with the mass pairing
DW := SparseMatrix(Integers(), N, N);
for j in [1..N] do SetEntry(~DW, j, j, W[j]); end for;
BW := Matrix([ Vector(Vector(BS[i])*DW) : i in [1..d] ]);
Gamma := BW * Transpose(BS);
printf "CB|Gamma symmetric %o, positive definite %o\n",
    IsSymmetric(Gamma), IsPositiveDefinite(Gamma);
dsub := Determinant(Gamma);
printf "CB|det Gamma_sub = %o\n", dsub;
printf "CB|det Gamma_sub ~ 2^%o\n", Ilog2(Abs(dsub));
printf "CB|elementary divisors: %o\n", ElementaryDivisors(Gamma);

// quotient lattice index
GiQ := ChangeRing(Gamma, Rationals())^-1;
Mq := ChangeRing(Transpose(BW), Rationals()) * GiQ;    // N x d, rows generate L_quot
lq := LCM([ Denominator(e) : e in Eltseq(Mq) ] cat [1]);
MqZ := Matrix(Integers(), lq*Mq);
H := HermiteForm(MqZ);
Hd := RowSubmatrix(H, 1, d);
idxnum := lq^d;  // [ (1/lq) L : Z^d ] denominator bookkeeping via det
detH := &*[ Hd[i,i] : i in [1..d] ];
// L_quot = (1/lq)*rowlattice(MqZ); [L_quot : Z^d] = lq^d/detH
idx := idxnum / detH;
printf "CB|quotient/sub index = %o\n", idx;
dquot := dsub / idx^2;
printf "CB|det Gamma_quot = %o\n", dquot;
printf "CB|det Gamma_quot ~ 2^%o\n", Ilog2(Numerator(AbsoluteValue(dquot))) - Ilog2(Denominator(AbsoluteValue(dquot))+0);

// normalisation ingredients
printf "CB|disc(h_g) = %o\n", Discriminant(hgZ);
printf "CB|disc(h_g) ~ 2^%o\n", Ilog2(Abs(Discriminant(hgZ)));
printf "CB|done\n";
quit;
