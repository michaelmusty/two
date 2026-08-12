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
passport has an only-2-ramified moduli field, the route is live. Because the
moduli-field ramification at p reflects the good/bad partition of the passport
at p, this may be probeable by counting char-p tame covers group-theoretically
— *before* computing any genus-28 equations. That count (good-reduction
weights for the k=8 passports at p = 3, 5, 17, 257, calibrated against the
verified k=4 weights 8/4/6) is the recommended next computation.
