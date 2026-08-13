# All-2-power branched covers cannot reach a nonsolvable field ramified only at 2: the moduli-field obstruction

**Status:** at `k = 4` (the group `PΓL₂(16)`), unconditional and fully explicit: every
computed all-2-power cover object — sixteen genus-0 covers in two triple passports, four
genus-1 covers in a third, and every short 4-point Hurwitz component — has the *same*
degree-8 moduli field `K`, ramified at `{2, 5, 17}`; hence no specialization of any of
them is ramified only at 2. For the whole family `PΓL₂(2^k)` (and the Suzuki groups) the
conclusion is conditional on a *transfer hypothesis* calibrated twice at `k = 4`; its
combinatorial core (the fixing congruence for `q+1`-torus primes) is proved. A concrete
falsification target for `k = 8` is stated in §8.

This document consolidates the 2026-08-11/13 investigation (repository directory
`dembele/rigidity/`), which was triggered by Huang–Jackson–Lee–Poonen–Pries–Zhang,
*The Mathieu group M₂₃ is a Galois group over Q* (arXiv:2608.08538) — whose computational
engine is the numerical Belyi machinery of Klug–Musty–Schiavone–Sijsling–Voight — and by
Zhang's companion note *How AI entered our collaboration on M₂₃* (coordinates, not
precision). It is the sequel, one level up, to `main-result.md`: after 2-group covers were
(conditionally) blocked by the centralizer mechanism, the natural evasion is almost-simple
covers with all-2-power ramification, and this document records why that evasion fails too.

---

## 1. Setup: the four gates, and why all-2-power passports over `PΓL` are forced

Let `q = 2^k` and `Ĝ = PΓL₂(q) = SL₂(F_q) ⋊ C_k` (Frobenius on `F_q`). Dembélé's field has
`Gal ≅ SL₂(F₂₅₆)² ⋊ C₈`; the almost-simple quotient shape `SL₂(F₂₅₆)⋊C₈ = PΓL₂(256)` is
the natural cover-theoretic target (its `C₈`-part, for an only-at-2 field, is forced by
Kronecker–Weber into `Q(ζ₂^∞)`, whose totally real `C₈`-subfield is exactly Dembélé's
`F = Q(ζ₃₂)⁺`).

A Galois extension of `Q` obtained by specializing a branched cover `ψ: X → P¹` at
`t₀ ∈ Q` is ramified only within four sources:

1. **wild primes** — primes dividing a ramification index `e_i`;
2. **bad reduction** of the cover;
3. **collision primes** of `t₀` with the branch locus (finite, searchable — M23's
   Example 3.7 move);
4. **the moduli field** `K` of the cover — every specialization tower contains `K`.

Gate 1 forces every `e_i` to be a 2-power. In the *simple* group `SL₂(F_q)` the 2-Sylow is
elementary abelian: the only 2-power-order elements are involutions, and a triple of
involutions with product 1 generates a Klein group — no nonsolvable Belyi triple exists.
Four involutions land on the Euclidean orbifold `(2,2,2,2)`, all of whose quotients are
solvable. The almost-simple `Ĝ` evades this: its outer cosets carry classes of order 8 and
16 (Lang correspondence with `SL₂(2^gcd)`-classes), and all-2-power generating triples
exist (§2). Their character fields have 2-power conductor, so gate 4's *forced cyclotomic
layer* is only-at-2 as well. Everything then hinges on the residual arithmetic of gates 2
and 4 — which is what the rest of this document computes.

## 2. The k = 4 pilot: sixteen exact genus-0 covers

`PΓL₂(16)` (order 16320, acting on the 17 points of `P¹(F₁₆)`) has exactly four
all-2-power triple passports with generating Nielsen classes:

| passport (class@coset) | cycle types (degree 17) | genus | Ni (generating) |
|---|---|---|---|
| `(2@0, 4@φ, 8@φ³)` | `(1·2⁸, 1³·2·4³, 1·8²)` | 0 | 4 |
| `(4@φ, 4@φ, 4@φ²)` | `(1³·2·4³, ·, 1·4⁴)` | 0 | 4 |
| `(2@φ², 8@φ, 8@φ)` | `(1⁵2⁶, 1·8², ·)` | 1 | 4 |
| `(2@0, 8@φ, 8@φ³)` | | 2 | 12 |

(plus `ε`-conjugates; scripts `04`, `05`). Both genus-0 passports were computed exactly
(scripts `10`–`16`): each cover is `ψ = c·y·S(y)²/T(y)⁸` (resp. the `(4,4,4)` shape), the
passport identity `c·y·S² − T⁸ = c·(y−1)²·A⁴·C` holds identically over the coefficient
field, and the monodromy of a fiber is certified `PΓL₂(16)` by a rigorous `GaloisGroup`
computation. Recognition required the M23 lessons: a Galois-equivariant gauge (the unique
simple zero, double point over 1, and simple pole pinned to `0, 1, ∞`) and recognition of
the *Newton factors* rather than expanded polynomials (multiple-root extraction loses
`accuracy^(1/multiplicity)`; naive LLL fits sat exactly at the noise floor
`10^{prec/(deg+1)}` and were unstable under precision change — the two-precision test is
the practical criterion for spurious relations). Exact data:
`dembele/rigidity/out/exact_map_248_rep1_data.m`, `out/exact_map_444_rep*_data.m`.

## 3. The universal moduli field

All eight `(2,4,8)`-covers and all eight `(4,4,4)`-covers have the **same** degree-8
moduli field

    K = Q[z]/(z⁸ + 4z⁷ + 4z⁶ + 2z⁴ + 12z³ + 20z² + 8z + 2),   disc K = 2¹⁸·5²·17,

with unique quadratic subfield `Q(i)` (`IsIsomorphic` verified). The Galois action on each
passport-pair's eight covers is transitive: there is no M23-style fixed point, and the
excess over the forced 2-cyclotomic layer is where 5 and 17 enter.

The genus-1 passport `(2@φ², 8@φ, 8@φ)` was computed on chatelet (scripts `25`–`26`);
its gauge-invariant j-invariant has an exact degree-8 minimal polynomial (leading
coefficient `5²⁰`) whose field is again **isomorphic to `K`**. Thus every computed
all-2-power triple passport of `PΓL₂(16)` has moduli field `K`. (Unchecked corners: the
genus-2 passport `(2@0,8,8)` with Ni = 12 and the genus-4 `(4@φ²,8,8)`; both are
boundary-linked to the same web and are expected to conform.)

**Unconditional consequence.** Every specialization of every computed cover contains `K`,
hence is ramified at 5 and 17. These constructions cannot produce a field ramified only
at 2 — independently of modularity conjectures, and consistently with the (conditional)
nonexistence of any only-at-2 `SL₂(F₁₆)⋊C₄`-field from the LMFDB/HMF sweep.

## 4. The local mechanism: the obstruction is not the geometry

Place-by-place reduction analysis of the exact covers over `K` (scripts `17`–`18`):

| p | places (e,f) of K | reduction of the 8 conjugate covers | good weight |
|---|---|---|---|
| 3 | inert (1,8) | étale; full ramification divisor survives | 8/8 |
| 5 | (1,1),(1,1),(3,1),(1,3) | one unramified place: map collapses to degree 2; the e=3 place: pole escape; two good | 4/8 |
| 17 | (2,1),(1,1),(1,2),(1,3) | bad exactly at the ramified e=2 place; three good | 6/8 |

This is the Raynaud/Bouw–Wewers mixed ordinary/supersingular picture at `p ∥ |G|` made
fully explicit. Counting embeddings: `good₅ (4) + good₁₇ (6) − 8 ≥ 2`, and 3 is uniformly
good — **at least two of the eight conjugate covers have good reduction at every odd
prime**. The all-2-power *geometry* achieves "bad only at 2"; the obstruction lives
entirely in the moduli field. "Why 5 but not 3" is answered by the passport's ordinary-locus
weights, not by divisibility of `|G|`.

## 5. The braid layer: short orbits exist and are also caught

For 4-point passports (Hurwitz spaces of dimension 1 over the λ-line), a census of all 47
all-2-power class multisets (script `20`) shows most are braid-transitive, but five split
off short orbits — including four orbits of length 2-per-ordering in
`(4@φ,4@φ,8@φ³,8@φ³)` (the Häfner/M23 signature) and four orbits of length 6 inside a
Nielsen set of 259 808 for `(8@φ)⁴`. All short orbits decompose over the λ-line into
**degree-2, genus-0 components** (scripts `22`–`23`); no monodromy-free sections exist.

The decisive step is the **boundary map** (script `24`): coalescing the fourth branch
point degenerates each component to a 3-point cover, and the component ↔ cusp
correspondence is a Galois-equivariant *bijection* onto known Nielsen classes:

- the four `(4,4,8,8)` components ↔ the four golden `(2@0,4@φ,8@φ³)` covers;
- the paired `(8@φ)⁴` components ↔ the four genus-1 `(2@φ²,8@φ,8@φ)` covers;
- the third `(8@φ)⁴` components ↔ four classes of the genus-4 `(4@φ²,8,8)` passport.

Since the boundary objects' moduli field is `K` (§3), Galois permutes the components as it
permutes the cusps, and every short component is defined over (a conjugate of) `K`. The
λ-freedom does not evade the obstruction: **the r = 4 track closes at k = 4 by
moduli-field gluing through the boundary** — not by bad reduction, and not for lack of
short orbits.

## 6. The fixing congruence and the transfer hypothesis

**Lemma (fixing congruence; proved).** Let `q = 2^k` with `k = 2^j`, and let `p` be a
prime dividing `q + 1`. Then `2^k ≡ −1 (mod p)`, so `ord_p(2) = 2k/odd`, whence
`2^{j+1} | p − 1`. Since every 2-power-order class of `PΓL₂(2^k)` has order dividing
`2k = 2^{j+1}`, the twist `x ↦ x^p` **fixes every all-2-power class multiset**. Similarly
every prime `p | q² + 1` satisfies `p ≡ 1 (mod 4)` (as `ord_p(q) = 4`), which is the
2-Sylow exponent of the Suzuki groups `Sz(q)`: the `q²+1`-torus primes fix every
all-2-power Suzuki passport.

**Calibration at k = 4** (all three computed passports): the twist-fixing primes 5, 17
(`≡ 1 mod 4`) are exactly the weight-deficient, moduli-ramified ones; the twist-moving
prime 3 is full-weight and unramified.

**Transfer hypothesis** (empirical; calibrated on one group, two deficient primes, three
passports): *twist-fixing primes dividing `|G|` are weight-deficient and ramify the moduli
field; twist-moving primes are full-weight and do not.* The arrow "fixing ⇒ deficient ⇒
ramified" has no proof; `ε`-conjugation shows "moving" cannot be the mechanism itself, so
it is a marker awaiting a deformation-theoretic explanation (Bouw–Wewers).

**Conditional conclusion for the family.** Under the hypothesis, every all-2-power cover
object over `PΓL₂(2^k)` (any number of branch points, any `k = 2^j`) — and over `Sz(q)` —
has moduli field ramified at its `+1`-torus prime, because that prime provably fixes every
such passport. No cover specialization in these families is ramified only at 2. Suzuki
data (script `21`: `Sz(8)` has four `(4,4,4)` passports with `Ni = 6`, genus 8, `Q(i)`
class fields; twist: 5, 13 fix, 7 moves) conforms.

## 7. The no-go ladder

| construction | blocked by | status |
|---|---|---|
| 2-group Belyi maps (`main-result.md`) | Frobenius centralizer: `Aut_{F₂[G]}(J[2])` solvable (Lemma A, Lean) given indecomposability (Lemma B, 2008/2008 verified) | conditional on Lemma B |
| simple `SL₂(2^k)`, r = 3 | no all-2-power triples (elementary abelian 2-Sylow) | proved |
| any group, r = 4 all-involution | Euclidean `(2,2,2,2)` ⇒ solvable | proved |
| `PΓL₂(16)`, r = 3 and short r = 4 | the universal moduli field `K`, disc `2¹⁸·5²·17` | proved, explicit |
| `PΓL₂(2^k)` all `k`; `Sz(q)` | `+1`-torus prime fixes every passport (proved) ⇒ moduli ramification (transfer hypothesis) | conditional |
| simple `SL₂(2^k)`, r = 5 all-involution | 2-dim Hurwitz spaces; twist marker vacuous | unexplored |

## 8. What would decide the remaining questions

1. **k = 8 falsification target.** The twist probe predicts `ram(K₈) ⊆ {2, 17, 257}` for
   the `(2,8,8)` (genus 28) and `(2,8,16)` (genus 34) passports of `PΓL₂(256)` — the
   `q−1`-torus primes 3, 5 *move* at k = 8 and are predicted unramified. Computing the
   k = 8 moduli field (a heavy but M23-lineage computation) tests both the hypothesis and
   the family-wide closure at once.
2. **A theorem in place of the hypothesis**: count good-reduction covers at `p ∥ |G|` via
   Bouw–Wewers special deformation data; the k = 4 weights 8/4/6 are the test data.
   (Recorded dead end: counting char-p covers by Gröbner on the shape identity fails at
   degree ≥ 17 — the ramification profile does not isolate `PΓL`-monodromy.)
3. **The unchecked k = 4 corners**: the genus-2 `(2@0,8,8)` (Ni = 12) and genus-4
   `(4@φ²,8,8)` passports; expected to have moduli `K` (they are cusps of the same web).
4. **r = 5 all-involution covers** of the simple group: the one shape outside every
   argument above; 2-parameter families, no rigidity, marker vacuous — parked.

## 9. Provenance

All computations: Magma V2.29-8 (local; heavy jobs on chatelet via `remote_magma/`), the
Belyi package (`michaelmusty/Belyi`, with two patches made during this work: a
`TrialDivision` guard in `MakeKFromPoly` and a genus-1 `BELYI_DUMP_CFS` hook). Scripts and
outputs in `dembele/rigidity/` (`01`–`26` with `out/`); commits `20ea911` (census),
`7a8f949` (exact (2,4,8) covers), `6738c34` ((4,4,4)), `a9c916f` (local mechanism),
`77d019d` (twist probe), `52474ea` (Suzuki), `dd96d39`/`bee8611` (braid census, boundary
map), `95fefb5` (genus-1 j-field; k = 4 closure). The M23 reference points: arXiv:2608.08538
and Zhang's *how-we-found-m23* note (`dembele/rigidity/refs_how-we-found-m23.pdf`).
