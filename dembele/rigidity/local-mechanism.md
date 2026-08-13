# The local mechanism at 3, 5, 17 (k = 4 pilot)

Date: 2026-08-12. Scripts `17` (passport (2,4,8)), `18` (passport (4,4,4));
outputs `out/local_mechanism_248.txt`, `out/local_mechanism_444.txt`.
Both passports have the **same** degree-8 moduli field
K = Q[z]/(z⁸+4z⁷+4z⁶+2z⁴+12z³+20z²+8z+2), disc 2¹⁸·5²·17
(`IsIsomorphic` verified), so one field governs all sixteen genus-0
all-2-power covers of PΓL₂(16).

## The data

Place structure of K and reduction behavior of the exact covers (identical for
both passports; "weight" = e·f = number of complex embeddings at the place):

| p | places (e,f) | behavior | good weight |
|---|---|---|---|
| 3 | inert (1,8) | étale, full ramification divisor (deg 32) survives | **8 / 8** |
| 5 | (1,1), (1,1), (3,1), (1,3) | one unramified place: **map collapses to degree 2** (deg-15 cancellation, all quadruple/octuple/most double points coalesce); the e=3 place: fiber points escape to ∞; other two places good | **4 / 8** |
| 17 | (2,1), (1,1), (1,2), (1,3) | bad exactly at the ramified e=2 place (pole escape, v(c) = −16, disc(S) picks up 17¹⁴); all three unramified places good | **6 / 8** |

## What this means

1. **Good and bad reduction coexist inside one Galois orbit.** At p = 5 and 17
   (both exactly dividing |PΓL₂(16)| = 2⁶·3·5·17, both tame here since the
   ramification indices are 2-powers), the eight conjugate covers split into
   ordinary-like members (good reduction) and supersingular-like members
   (degenerate). This is the Raynaud / Bouw–Wewers picture of three-point
   covers at primes p ∥ |G|, realized completely explicitly; the mild
   ramification of the moduli field at the bad primes (e = 3 above 5, e = 2
   above 17) matches Wewers' predictions.

2. **Some covers are good at every odd prime.** Counting embeddings:
   good-at-5 (4) + good-at-17 (6) − total (8) ≥ 2, and 3 is uniformly good, so
   **at least two of the eight conjugate covers have good reduction at all odd
   primes** — their only bad prime is 2. The "all-2-power geometry ramified
   only at 2" dream is *achieved by the covers themselves*.

3. **The obstruction lives in the moduli field, not the geometry.** Every
   specialization tower contains K, and K is ramified at 5 and 17. That —
   not bad reduction of the cover — is what keeps k=4 realizations away from
   "ramified only at 2", consistently with the LMFDB/HMF nonexistence of
   only-at-2 SL₂(F₁₆)⋊C₄ fields.

4. **Why 5 but not 3?** Not because of |G|-divisibility (3 | |G| too). The
   good-reduction weights (8, 4, 6 at 3, 5, 17) are an arithmetic invariant of
   the passport — the sizes of the ordinary locus at each prime. At 3 the
   whole passport is ordinary; at 5 and 17 it is not. The degeneration shapes
   (collapse to a *degree-2* separable map at 5; pole-escape at the ramified
   17-place) are the fingerprints of the respective special fibers.

## Consequence for the k = 8 program

The decisive question for the Dembélé target is no longer "can a cover of
PΓL₂(256) have good reduction outside 2" (the k=4 analogue is YES for some
conjugates) but:

> **Is the moduli field of the k=8 all-2-power passports ((2,8,8) genus 28,
> (2,8,16) genus 34) ramified only at 2?**

If, as at k=4, it must pick up torus primes (3, 5, 17 | 255 or 257), the cover
route to Dembélé's exact field closes with a clean explanation; if some k=8
passport has an only-2-ramified moduli field, the route is live.

## The k=8 probe (script `19`, output `out/twist_probe.txt`)

**Dead end recorded first**: counting char-p tame covers directly via the
genus-0 shape identity over F̄_p (Gröbner) fails at degree 17+ — the
ramification profile does not isolate PΓL-monodromy covers (the profile's
Hurwitz number includes a flood of A₁₇-type covers), so the solution variety
counts the wrong thing.

**What discriminates 3 from {5, 17} at k=4**: the Frobenius twist. For p | |G|
consider x ↦ xᵖ on the class multiset. At k=4 (all three all-2-power
passports, including the uncomputed genus-1 one): p = 5, 17 (≡ 1 mod 4) FIX
each passport; p = 3 MOVES it (swaps the conjugate passports). The measured
weights: fixing primes are weight-deficient (4/8, 6/8), the moving prime is
full (8/8). *Transfer hypothesis* (empirical, calibrated on this one group;
"moves ⇒ full" has no proof — ε-conjugation makes conjugate passports behave
identically at every p, so moving is a marker, not yet a mechanism):
twist-fixing primes dividing |G| are weight-deficient and produce moduli
ramification; twist-moving primes are full-weight and unramified.

**k=8 result of the probe** (both passports, (2@φ⁴, 8@φ, 16@φ³) genus 34 and
(2@inner, 8@φ⁷, 8@φ) genus 28):

| p | twist action | prediction |
|---|---|---|
| 3 | MOVES | full weight — K₈ unramified at 3 |
| 5 | MOVES | full weight — K₈ unramified at 5 |
| 17 | FIXES (17 ≡ 1 mod 16) | deficient — K₈ ramified at 17 |
| 257 | FIXES (257 ≡ 1 mod 16) | deficient — K₈ ramified at 257 |

Predicted: **ram(K₈) ⊆ {2, 17, 257}, with the q−1 torus primes 3 and 5
dropping out** (unlike k=4, where 5 ≡ 1 mod 4 fixed the passports; at k=8 the
class orders reach 16, and 3, 5 ≢ 1 mod 16 move everything).

**Structural corollary of the fixing criterion** (unconditional): any p ≡ 1
mod 2^(max class order) acts trivially on every all-2-power class, so it fixes
EVERY all-2-power passport. For q = 2^k the nonsplit-torus prime divides
q + 1 ≡ 1 mod 2^k — it always fixes. So under the transfer hypothesis the
q+1-prime(s) obstruct the only-at-2 dream for **every** all-2-power passport
of PΓL₂(2^k), at every k: the cover route would close for the whole family,
mirroring (one level up) the legacy 2-group obstruction. Falsifiable: compute
the k=8 moduli field (the genus-28 (2,8,8) computation) and check its
ramification against the prediction {2, 17, 257}; or replace the hypothesis
with a real count via Bouw–Wewers deformation data at p ∥ |G|.

## Postscript (2026-08-12/13): the k=4 universal field, and closure of the r=4 track

The genus-1 (2@φ², 8@φ, 8@φ) passport — linchpin for the (8@φ)⁴ short braid
components via the boundary bijection (script 24) — was computed on chatelet
(scripts 25–26, offline j-invariant recognition from the dumped Newton data:
j has an exact degree-8 minimal polynomial with leading coefficient 5²⁰).
Its j-field is **isomorphic to the same degree-8 field K** with
disc = 2¹⁸·5²·17 as every other all-2-power moduli field at k=4.

Conclusion: ONE universal moduli field K governs all all-2-power covers of
PΓL₂(16) — r=3 passports of genus 0 and 1, and (via cusp equivariance) all
short r=4 Hurwitz components. The braid/λ freedom does NOT evade the moduli
obstruction: sibling components glue through the boundary Galois action into
K. The r=4 short-orbit track at k=4 is CLOSED by the same mechanism as r=3,
and the failure mode of the control experiment is identified as
moduli-field gluing (not bad reduction, not absence of short orbits).

Together with the twice-calibrated twist analysis, the covers program now
supports a sharp conjectural conclusion: every all-2-power cover object over
PΓL₂(2^k) (any r, any k) has moduli field ramified at the +1-torus prime
(≡ 1 mod the 2-exponent, provably twist-fixing), so no cover specialization
in this family is ramified only at 2. The explicit k=4 universal field is
the complete worked example.
