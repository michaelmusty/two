# Rigidity/Belyi front end for the Dembélé group (after the M23 paper)

Date: 2026-08-11. Prompted by Huang–Jackson–Lee–Poonen–Pries–Zhang,
*The Mathieu group M23 is a Galois group over Q* (arXiv:2608.08538), which realized
M23 explicitly via a non-rigid triple, the KMSV numerical Belyi algorithm, and
BelyiDB — i.e., the machinery built in Klug–Musty–Schiavone–Sijsling–Voight.

Everything below is Magma character theory + randomized generation checks on
`PGammaL(2,q)`; scripts `01`–`05`, raw outputs in `out/`.

## Setup

Dembélé's target is `Gal(K/Q) ≅ SL₂(F₂₅₆)² ⋊ C₈` with `C₈ = Gal(F/Q)`,
`F = Q(ζ₃₂)⁺`, ramified only at 2. The almost-simple "half" of this group is

    Ĝ := SL₂(F₂₅₆) ⋊ C₈ = PΓL₂(256)   (order 134 215 680, min. faithful degree 257).

A regular Ĝ-extension of Q(t) plus its Frobenius-twisted partner sharing the same
C₈-quotient would fiber-product to the full `S²⋊C₈` shape. So Ĝ is the natural
rigidity target.

## Finding 1: all-2-power generating triples exist in Ĝ (but not in S)

`SL₂(F₂ᵏ)` has elementary abelian 2-Sylow: its only 2-power-order elements are
involutions, and an involution triple with product 1 generates a Klein group. So the
**simple** group admits no Belyi triple with all ramification indices 2-powers —
consistent with the thesis's legacy obstruction philosophy (all-2-power ramification
forces solvable monodromy in the settings previously considered; likewise the
Euclidean orbifold (2,2,2,2) only has solvable quotients).

The **almost-simple** group evades this: outer cosets carry classes of order 8 and 16
(Lang correspondence with `SL₂(2)`-classes: orders 8, 16, 24 over the cosets of φ^±1,
φ^±3). Exhaustive structure-constant census over all class multisets with orders in
{2,4,8,16}, coset images summing to 0 mod 8 and generating C₈ (`03`, output
`out/allpow2_256.txt`): many multisets have nonzero counts **and random triples
generate Ĝ at rates 70–100%**. Best generating candidates:

| multiset (order@coset) | Nielsen bound n | genus (deg-257 quotient) | sampled gen. rate |
|---|---|---|---|
| (2@0, 8@φ⁷, 8@φ) inner invol. | 3655/16 ≈ 228 | **28** | 13/15 |
| (2@φ⁴, 8@φ, 16@φ³) | **40** | **34** | 13–14/15 |
| (2@φ⁴, 16@φ³, 16@φ) | 137 | 44 | 14–15/15 |
| (4@φ², 8@φ⁷, 8@φ⁷) | ~1050 | 57 | ~14/15 |

Cycle types for (2@φ⁴, 8@φ, 16@φ³), degree 257:
`(1¹⁷2¹²⁰, 1³2¹4³8³⁰, 1¹16¹⁶)`, genus 34.
For (2@0, 8@φ⁷, 8@φ): `(1¹2¹²⁸, 1³2¹4³8³⁰, 1³2¹4³8³⁰)`, genus 28.

Caveat: the a priori most attractive multiset (2@φ⁴, 8@φ, 8@φ³), n ≈ 19, genus 24,
**never generates** (0/27 samples): all three classes are conjugates of *pure* field
automorphisms (φ⁴, φ, φ³ — Lang class of the identity), and the samples land in
`PSL₂(16)⋊C₈` (order 32640) and 2-local subgroups. Pure-Frobenius triples are dead;
mixing in the identity-coset or non-identity Lang classes is what works.

## Finding 2: the branch-cycle arithmetic of these triples is purely 2-cyclotomic

The order-8 outer classes have character values in `Q(ζ₁₆)` (checked directly), degree
4 over Q; the cyclotomic action ε(σ) permutes the four classes 8@φ, 8@φ³, 8@φ⁵, 8@φ⁷
by 2-power-coprime exponentiation, which moves cosets — so 𝔊_Q-stable multisets and
conjugate-branch-point matchings à la M23 exist with **all class fields of 2-power
conductor**. Combined with all-2-power ramification indices, nothing in the
tame/cyclotomic layer of these covers forces ramification at any odd prime:

- specializations are wild only above 2; at odd p they ramify only through bad
  reduction of the cover or branch-point collisions mod p;
- any Ĝ-field ramified only at 2 has its C₈-subfield cyclic of degree 8 unramified
  outside 2, hence one of the three C₈-subfields of `Q(ζ₂^∞)` (Kronecker–Weber);
  the totally real one is exactly Dembélé's `F = Q(ζ₃₂)⁺`.

The uncontrolled ingredient is good reduction of the cover at the odd primes dividing
|Ĝ| (3, 5, 17, 257): Beckmann's criterion does not apply, and nothing supplies it.
That is now the *precise* residual obstruction on this route — a question about the
3-, 5-, 17-, 257-adic geometry of two specific curves (genus 28 and 34) rather than a
structural impossibility. Contrast: the legacy 2-group route was conditionally blocked
outright (Lemma A + B); the almost-simple route is combinatorially open.

## Finding 3: a fully computable pilot at k=4 — genus 0, degree 17, Ni = 4

`PΓL₂(16) = SL₂(F₁₆)⋊C₄` (order 16320, degree 17) has the same phenomenon with tiny
numbers (`04`, `05`; outputs `out/pilot_16.txt`, `out/exact_ni_16.txt`):

| passport (order@coset) | cycle types (deg 17) | genus | exact Ni (generating) |
|---|---|---|---|
| (2@0, 4@φ, 8@φ³) | (1¹2⁸, 1³2¹4³, 1¹8²) | **0** | **4** |
| (4@φ, 4@φ, 4@φ²) | (1³2¹4³, 1³2¹4³, 1¹4⁴) | **0** | **4** |
| (2@φ², 8@φ, 8@φ) | — | 1 | 4 |
| (2@0, 8@φ, 8@φ³) | — | 2 | 12 |

Character values: conductor 4, i.e. `Q(i)`; the (2,4,8)-passport and its partner
(2@0, 4@φ³, 8@φ) are swapped by `Gal(Q(i)/Q)` — exactly the M23 conjugate-branch-point
situation. Genus-0 degree-17 three-point covers with 4 Nielsen classes are *strictly
easier* than the M23 computation (7 classes, genus 4, degree 23) and squarely within
KMSV/BelyiDB range: each cover is a degree-17 rational function.

Built-in control experiment: the inverse-galois-hmf sweep found **no**
`SL₂(F₁₆)⋊C₄`-field ramified only at 2 (consistent with Dembélé's minimality claim),
so these k=4 covers must have odd bad primes. Computing them shows concretely *where
the odd ramification enters* on the cover route, before attempting k=8 where
Dembélé's field does exist. Independent cross-check available: the 17T7 paper
(vBCEKSV, arXiv:2411.07857) produced PΓL₂(16)-polynomials by the HMF/Eichler–Shimura
route.

## What transfers from the M23 paper wholesale

1. **Non-rigid + 𝔊-equivariant branch points**: match Galois orbits of classes with
   conjugate branch points (here `Q(i)` at k=4, `Q(ζ₁₆)`-subfields at k=8).
2. **Numerics-then-certify**: KMSV power series → PSLQ → exact verification; no rigor
   needed mid-computation.
3. **Mod-p certification of monodromy** (their Prop 3.5): specialize mod a good prime
   p > degree, use the tame specialization isomorphism to certify
   G_geom = G_arith; directly reusable for any polynomial we eventually produce.
4. **Descent for center-trivial covers** ([CH85], [DD97]): Z(PΓL₂(q)) = 1, so field of
   moduli = field of definition, as for M23.
5. Endgame `polredabs`/`polredbest` + specialization search over t₀ to minimize the
   ramification set (their Example 3.7 got {2,7,23}; we would hunt for
   {2} ∪ (bad primes of the cover)).

## What does not transfer

An M23-style realization controls the *group*, not the *ramification*. For the
specific Dembélé field the HMF route (`dembele/`) remains the only unconditional
approach; the covers here would give (a) regular Ĝ-realizations over Q(t) — new for
k=8, complementing the existence-only HMF certificates — and (b) a concrete geometric
attack surface for the only-at-2 question via good-reduction analysis.

## Next steps (in order)

1. **k=4 pilot (actionable now)**: compute the four genus-0 (2,4,8) covers with the
   KMSV/BelyiDB pipeline; recognize fields of moduli; specialize; factor the
   discriminants → measure the odd bad primes. Also do (4,4,4).
2. Exact generating Nielsen counts at k=8 via maximal-subgroup inclusion–exclusion
   (Borel⋊C₈, two dihedral normalizers, PSL₂(16)⋊C₈) instead of sampling.
3. Braid-free 𝔊-orbit analysis of the 4 pilot covers (lifting invariants vanish:
   Schur multiplier of PSL₂(16), PSL₂(256) trivial).
4. If the pilot's bad primes show structure (e.g., only the Lang/torus primes 3,5,17
   appear), formulate the good-reduction question for the k=8 genus-28/34 curves
   precisely; consider stable-model computations at 17 and 257.
5. Optional theory: r = 5 all-involution covers of SL₂(F₂ᵏ) (the only other shape
   whose specializations are wild only at 2; (2,2,2,2) is Euclidean hence solvable,
   so r ≥ 5 is forced). Hurwitz dimension 2; park unless 1–4 stall.

## PILOT RESULT (2026-08-11): the (2,4,8) covers are computed and certified

Following Zhang's account of the M23 computation (how-we-found-m23.pdf: recognition
fails in triangle-group coordinates at any precision; Galois-equivariant coordinates
collapse the heights), scripts `10`–`14` complete the k=4 pilot:

- **Gauge**: every fiber of the (2,4,8) passport has a canonical point (unique
  simple zero, unique double point over 1, unique simple pole). Sending them to
  0, 1, ∞ kills all PGL₂ freedom equivariantly. Crucially the coefficients are
  extracted from the dumped **Newton factors** (multiple-root extraction from the
  expanded polynomials loses accuracy^(1/multiplicity) and made every naive LLL fit
  spurious — heights at the noise floor 10^(prec/(deg+1)) and unstable under
  precision changes, the tell-tale we used to reject them).
- **All 4 covers recognized** (17/17 coefficients each, LLL at 1000 digits verified
  independently at 2000 digits; passport identity residual ~10⁻⁴⁷⁸⁰). All four have
  the SAME degree-8 moduli field: 𝔊_Q permutes the 8 covers (this passport and its
  Q(i)-conjugate) transitively — no M23-style fixed point, as in their (2A,8A,8A).
- **The moduli field** K = Q[w]/(w⁸+4w⁷+4w⁶+2w⁴+12w³+20w²+8w+2) has
  **disc = 2¹⁸·5²·17**, unique quadratic subfield Q(i).
- **Exact certificate**: the map ψ = c·y·S(y)²/T(y)⁸ (S monic deg 8, T monic deg 2)
  satisfies c·y·S² − T⁸ = c·(y−1)²·A⁴·C exactly in K[y] (`14`, output
  `out/exact_map_248_rep1.txt` with the full coefficients).
- **Bad primes of the model: exactly {2, 5, 17}** (support of all pairwise fiber
  resultants, fiber discriminants, and c). Away from them the branch divisors stay
  étale-disjoint and all odd ramification is tame (indices 2,4,8) — wildness only
  at 2. **3 does not appear**, although 3 | |PΓL₂(16)|: the obstruction primes are
  the torus primes 5 | q−1 and 17 = q+1 = degree, NOT all odd primes of |G|.

- **Monodromy certified**: `GaloisGroup` (rigorous, Magma) of the t=3 fiber of the
  exact map over K has order 16320 = |PΓL₂(16)| — so the arithmetic monodromy of
  ψ over K(t) contains (hence realizes) PΓL₂(16), and the t=3 fiber is already a
  certified PΓL₂(16)-extension of K. Exact map data (loadable):
  `out/exact_map_248_rep1_data.m`.

Consequence: specializations give PΓL₂(16)-extensions of K unramified outside
{2, 5, 17} ∪ {primes forced by t₀} — and K itself is ramified only at {2,5,17}.
For the k=8 program this is the key structural encouragement: the odd obstruction
is a short, structured list (torus primes), not everything dividing |G|.

**Second passport (4,4,4)** (scripts `15`, `16`; outputs `out/*444*`): all four
covers computed and certified the same way (exact identity
c·y²·F⁴·E₁ − G⁴ = c·(y−1)²·H⁴·J over K; monodromy certified per rep).
**Same answer**: degree-8 moduli field, disc 2¹⁸·5²·17, **bad primes {2, 5, 17}**.
Two independent passports with different coset structures ((1, φ, φ³) vs
(φ, φ, φ²)) produce identical odd obstruction primes {5, 17} — evidence the
obstruction is structural at fixed q (torus primes 5 | q−1, 17 = q+1), not an
artifact of the class choice. Exact data: `out/exact_map_444_rep{1..4}_data.m`.

**Local mechanism at 3, 5, 17** (scripts `17`, `18`; **`local-mechanism.md`** for
the full analysis): both passports share the SAME moduli field (IsIsomorphic
verified). Good-reduction weights of the 8 conjugate covers: 8/8 at p=3, 4/8 at
p=5 (one place collapses the map to degree 2, the e=3 place sends points to ∞),
6/8 at p=17 (bad only at the ramified e=2 place). Hence ≥2 conjugate covers have
good reduction at EVERY odd prime — the obstruction to only-at-2 lives in the
moduli field K (ramified at 5, 17), not in the cover geometry. The k=8 question
becomes: is the moduli field of the k=8 all-2-power passports only-2-ramified?

k=4 control: the inverse-galois-hmf sweep found no only-at-2 SL₂(F₁₆)⋊C₄ field,
consistent with {5,17} being genuinely unavoidable here; at k=8 (torus primes
3·5·17 and 257) Dembélé's field exists, and the question of a cover with bad
reduction only at 2 is now a sharply posed geometry question.

## Status of the earlier passport-mode attempts (superseded)

Scripts `06`–`09` drive the actual Belyi map computation through the local clone of
the Belyi package (`~/Belyi`, spec `Code/spec`, C solver `Cext/powser_arnoldi`,
certified relation finder `Cext/makek_relfinder` — both built; export
`POWSER_ARNOLDI_BIN` and `MAKEK_RELFINDER_BIN`). Findings so far:

- The four Nielsen representatives of each genus-0 passport are constructed and
  verified (`sigma[3]*sigma[2]*sigma[1] = 1`, package convention).
- At the default working precision (115 digits) the numerics converge (Newton
  residual pushed to ~10⁻⁹⁵⁰⁰ by the escalation ladder) but **field recognition
  fails**: `MakeK` certifies nothing at degrees 6→2 and the certified relation
  finder confirms "no coefficient relation certifies at this precision" — i.e. the
  coefficient heights need more digits, the true moduli field is not found at 115.
- Passport mode (`ExactAl := "GaloisOrbits"`) falls back to per-cover recognition in
  genus 0, so it is not a workaround by itself.
- A rerun at `prec := 500, precNewton := 750` (scripts as committed) was in flight
  when paused: Arnoldi iterations ~156 s each at that precision, so budget several
  hours per passport; run the two passports sequentially (the C solver is
  multithreaded and two jobs contend). Partial logs in `out/passport_*_p500.txt`.

To resume: rerun `08` then `09` exactly as committed with the two env vars set.

## Provenance

- `01_nielsen_census.m` — census procedure; runs q=16, 64 as calibration.
- `02_nielsen_census_256.m` — full census for PΓL₂(256) (64 classes; char table 0.12s).
- `03_allpow2_gencheck_256.m` — all-2-power multisets at q=256 + generation sampling.
- `04_pilot_census_16.m` — same at q=16 with conductor checks.
- `05_exact_ni_16.m` — exact Nielsen counts at q=16 by direct enumeration.
- Magma V2.29-8 local. Random generation checks use 12–30 hits per multiset.
