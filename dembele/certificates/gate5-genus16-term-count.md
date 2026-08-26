# Gate 5: the Eisenstein term count at genus 16, made quantitative

**Date:** 2026-08-26. Desk work plus two short Sage checks
(`dembele/scratch_validation/eisenstein_count_law_check.sage`,
`dembele/scratch_validation/hecke_subfield_h8_zeta.sage`). Answers handoff items 3 and 4 as far as they can be answered
before gate 4, and replaces the planned genus-16 "separation test" with a
statement of what it would cost and what it depends on.

## Summary

- The number of Fourier terms needed to evaluate a Hilbert modular form of
  parallel weight `k` over a totally real field of degree `n`, discriminant `D`,
  to cutoff `C` at a point with imaginary part `y` obeys the volume law

      #terms(C) ≈ sqrt(D) · C^n / (n! · N(y)).                          (1)

  **Validated** on the genus-4 control (`n = 4`, `D = 725`): predicted
  5017 / 80274 / 314 against observed 5007 / 80286 / 315 for the base, half, and
  double points — all within 0.3%.

- For the q0-adic evaluation the same law holds with the period-valuation
  vector `w` in place of `y` and the precision `M` (in units of `v_q0`) in place
  of `C`. Because the valuation pairing is integral, its determinant is at least
  1, and (1) becomes the **upper bound**

      #terms(M) ≤ sqrt(D_H) · M^16 / 16!  ·  1/Δ'  ≈  1.1·10^4 · M^16 / Δ',     (2)

  where `Δ' ≥ 1` is the determinant of the valuation pairing relative to its
  unimodular minimum (definition in §3). `Δ'` is **the** unknown of handoff item
  4: "depends on period valuations; never estimated". It is now a defined,
  computable quantity — see §5.

- Consequence. At `Δ' = 1` (unimodular pairing, leading term at valuation ~1),
  the count is `1.1·10^4 · M^16`: precision `M = 30` costs `2·10^27` terms. The
  route is feasible only if `Δ'` is large — `Δ' ≳ 10^20` for `M ≈ 30`,
  `Δ' ≳ 10^30` for `M ≈ 100` — which is the same as saying the periods have
  large valuations (`t_min ≳ 0.108·Δ'^{1/16}`, §4). Large valuations in turn
  raise the precision needed. Whether a consistent window exists is decided by
  two numbers, `Δ'` and the recognition precision `M_rec`, neither of which is
  known. **Do not start the gate-4 build before `Δ'` is computed** (§5): if
  `Δ'` is small the Fourier-expansion back end cannot reach recognition
  precision at genus 16, whatever gate 4 delivers.

- A side finding on the archimedean prototype: `ζ_H(−3) ≈ 10^{87.7}`, so the
  constant-term-1 normalisation puts the non-constant part of `E_4` at scale
  `2^16/ζ_H(−3) ≈ 1.4·10^{−83}`. On the fundamental domain for `H` the invariant
  is `1 + O(10^{−13})` or smaller; the genus-4 "separation vs truncation"
  criterion is meaningless at genus 16 without rescaling by `ζ_H(−3)/2^16`,
  which requires `ζ_H(−3)` **exactly** — itself a nontrivial computation at
  degree 16 (`L`-series methods need ~`sqrt(D_H) = 2·10^17` coefficients; a
  Shintani/Siegel-type evaluation is needed). This is a scale effect, not a
  dimension effect (it is visible already at genus 8, `ζ_{H_8}(−3) ≈ 1.7·10^18`),
  and it disappears q0-adically, where only `v_q0(ζ_H(−3))` enters.

## 1. The volume law and its validation

Terms of the `q`-expansion are indexed by totally positive `ν` in the
codifferent `d^{-1}` with `Tr(ν y) ≤ C` (archimedean; `C = −log(ε)/2π` for a
bare-exponential tolerance `ε`). The region `{x ≫ 0 : Σ x_i y_i ≤ C}` is a
simplex of volume `C^n/(n!·N(y))`, and `d^{-1}` has covolume `1/sqrt(D)`.
Hence (1).

Check on `dembele/tests/hilbert_eisenstein_genus4.sage` (`ε = 10^{−22}`,
`C = 8.0623`, `N(y) = 0.94479`, `sqrt(725) = 26.93`):

| point | `N(y)` | predicted | observed |
|---|---|---|---|
| base | `0.9448` | 5017 | 5007 |
| half (`y/2`) | `0.9448/16` | 80274 | 80286 |
| double (`2y`) | `0.9448·16` | 314 | 315 |

The law is exact to the lattice-point error even at the double point, where
`C` is only 4.3 times the smallest trace that occurs. The smallest trace
observed at the base point is `0.9301`; the AM–GM floor `n·(N(y)/D)^{1/n}`
(using `N(ν) ≥ N(d^{-1}) = 1/D`) is `0.7604`, so the slack `ρ = t_min/floor` is
`1.22` there.

## 2. Genus-16 numbers

| quantity | value | source |
|---|---|---|
| `D_H` | `5.1537·10^34 = 5^14·89^7·661^4` | `lift_field_structure.json` |
| `sqrt(D_H)` | `2.2702·10^17` | |
| `16^16/16!` | `8.817·10^5` | (vs `10.7` at `n = 4`, `416` at `n = 8`) |
| `sqrt(D_H)/16!` | `1.085·10^4` | the constant in (2) |
| `ζ_H(−3)` | `≈ 4.7·10^87` | functional equation, `ζ_H(4) ≈ 1`; the same formula gives `1.7324·10^18` for `H_8` against the exact `8662826887079588992/5 = 1.7326·10^18`, and `36.06` for the genus-4 field against `541/15 = 36.07` |
| `2^16/ζ_H(−3)` | `≈ 1.4·10^{−83}` | normalisation of the non-constant part |

Degree-8 subfield `H_8` (for reference; it does **not** give a 257-neighbour
test — 2 splits there into two primes of residue degree 4, so a
`λ`-neighbourhood has 17 points, not 257): `D = 5^6·89^3 = 1.1·10^10`,
`h = 1`, `h^+ = 2`, polredabs
`x^8 − x^7 − 15x^6 + 16x^5 + 59x^4 − 64x^3 − 20x^2 + 4x + 1`.

## 3. The q0-adic count and the integrality bound

For the CD-uniformised `B_g` the `q`-expansion is evaluated with `q^ν` in place
of `exp(2πi Tr(νz))` (`gate5-padic-eisenstein.md`), and

    v_q0(q^ν) = Tr_{H/Q}(ν w)

for a totally positive `w ∈ H ⊗ Q` (the valuation vector of the period lattice)
and `ν` in a lattice `L ⊂ H` (the index lattice of the relevant component). All
these valuations are integers, so `w` lies in the trace-dual `L^∨ = (L d)^{-1}`,
whence `N(w) ≥ N(L^∨) = 1/(N(L)·D)`. Writing

    Δ' := N(w) · N(L) · D  ≥ 1,

(1) becomes

    #terms(M) = M^16 / (16! · N(w) · covol(L)) = M^16 · sqrt(D) / (16! · Δ'),

which is (2). `Δ'` is the determinant of the Gram matrix `(Tr(l_i l_j w))` of
the valuation pairing on a `Z`-basis of `L`, divided by `N(L)^2·D` — i.e. it
measures how far the pairing is from unimodular. (Archimedean sanity check: with
`w = y`, `L = d^{-1}`, `Δ' = N(y) = 0.945` at the genus-4 base point, and (2)
reproduces the 5017.)

## 4. What `Δ'` controls, both ways

- **Term count**, downward: `#terms(M) ≈ 1.1·10^4 · M^16 / Δ'`.

  | `M` | `Δ' = 1` | `Δ' = 10^20` | `Δ' = 10^30` | `Δ' = 10^40` |
  |---|---|---|---|---|
  | 30 | `2·10^27` | `2·10^7` | — | — |
  | 100 | `1·10^40` | `1·10^20` | `1·10^10` | `1` |
  | 180 | `1·10^44` | `1·10^24` | `1·10^14` | `10^4` |

  (Each term costs one ideal factorisation in a degree-16 field; `10^9` terms
  is roughly the practical ceiling.)

- **Leading valuation**, upward: by AM–GM,
  `t_min = min Tr(νw) ≥ 16·(N(w)N(L))^{1/16} = 16·(Δ'/D)^{1/16} = 0.108·Δ'^{1/16}`,
  times a slack `ρ ≥ 1` (`1.22` at genus 4). So `Δ' = 10^20` means `t_min ≳ 2`,
  `10^30` means `≳ 8`, `10^40` means `≳ 34`. The 257 invariant values are then
  `1 + O(q0^{t_min})`, the isogeny polynomial's coefficients are congruent to
  binomials modulo `q0^{t_min}`, and their heights — hence `M_rec` — are at
  least `3.4·t_min` decimal digits.

- The volume law is an asymptotic; at genus 4 it held down to `C/t_min ≈ 4`.
  For `M` within a small factor of `t_min` the true count is *below* (2), which
  helps, but that regime gives only a few valuation units beyond the leading
  term — not recognition precision.

So the window that makes the Fourier back end viable is: `Δ'` large enough that
`#terms(M_rec)` is affordable, with `M_rec` (set by coefficient heights, which
grow with `t_min`, which grows with `Δ'`) small enough that gate 4's `M^2`
scaling is affordable (`~4000 core-h` at `M = 100`, `Nq0 = 2401`). Whether that
window is non-empty cannot be decided by desk work; it is decided by `Δ'`.

## 5. The computation that decides it — before gate 4

`w` is not needed; `Δ'` is a determinant, and it comes from the monodromy
pairing on the `g`-isotypic part of the character group of the level-`q0`
dual graph. That graph is already in hand: its edge space is the level-`q0`
Brandt module (`dim 109240`, the sparse operators of gate 3), its vertices are
the two copies of the level-1 class set, and the pairing is the edge-count
pairing (edge lengths 1, up to stabiliser factors). Concretely:

1. `X = ker(∂ : Z^{edges} → Z^{vertices})`, rank `109240 − 116 + 1`.
2. `X_g = X ∩ V_g` where `V_g` is the characteristic-zero eigenspace of the
   newform(s) carrying the excess (the `f1`-side, gate 3). Rank 16.
3. Gram matrix of the dot product on a `Z`-basis of `X_g` (or of the quotient
   lattice, depending on whether `B_g` is taken as sub or quotient — both
   determinants are needed; they differ by the polarisation degree).
4. `Δ' = det / (N(L)^2·D_H)` with the identification `X_g ≅ L` as an
   `O_H`-module.

The obstacle is step 2 over `Z` on a `109240`-dimensional space — the same
object gate 3 handles mod 2 — and it needs a sparse integral (or multi-modular
plus saturation) kernel rather than a dense one. That is a bounded piece of
work, and it is the right next computation: it can invalidate the gate-4 build,
and it reuses gate-3 machinery.

A cheaper proxy exists but is weaker: Ribet-style level-raising relates the
component group of the optimal quotient at `q0` to the congruence module
between `g` and the old space, which here is a power of 2 — suggesting a
*small* `Δ'` for the quotient. That would be the bad case. It is a heuristic
about the wrong lattice (quotient vs sub, and modulo the polarisation degree,
which for a newform in a genus-`10^5` Jacobian can be enormous), so it should be
replaced by the computation, not trusted.

## 6. What this changes in the plan

- Handoff item 3 ("test whether the invariant separates at genus 16"): at genus
  16 the archimedean test is not the right question. Separation is generic;
  the binding constraint is (2). A genus-16 archimedean run at the genus-4
  protocol (`C/t_min ≈ 8.7`, `ρ ≈ 1.2`) would cost of order
  `(8.7·1.2)^16 · 8.8·10^5 / 2.3·10^17 ≈ 10^5` terms at a *unimodular-like*
  point, which is affordable — but such a point is not our point, and the
  quantity it would measure (`ρ`) is secondary to `Δ'`.
- Handoff item 4 ("estimate the q0-adic term count"): done as far as possible;
  the count is (2), and the missing input is `Δ'`, computable as in §5.
- Handoff item 6 (gate-4 build): **blocked on §5**. The plan of record's
  ordering ("do the cheap invalidating test before the expensive build") is
  unchanged; the cheap test is `Δ'`, not a separation run.

## Caveats

- (1) is asymptotic; validated at `n = 4` only. The dimension-16 constant
  `16^16/16!` is exact, but lattice-point error at `M/t_min` near 1 is
  uncharacterised.
- The identification of the period-valuation lattice with `(L, w)` and the
  exact normalisation (component, polarisation, sub vs quotient) are stated at
  the level of `csv-paper-adaptation.md`, not proved here. `Δ'` as defined is
  robust to a bounded factor; it is not robust to which lattice is meant, so §5
  computes both.
- `ζ_H(−3)` is estimated, not computed. Its 7-adic valuation shifts `t_min` by
  a bounded amount and is irrelevant to (2).
