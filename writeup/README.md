# Write-up: branched covers and nonsolvable fields ramified only at 2

Consolidated results of the investigation into Musty (2019) Q1.2.5 / Q6.2.1, and its
sequel.

- **`all-2-power-covers.md`** — the sequel (2026-08): after 2-groups, the natural evasion
  is almost-simple covers `PΓL₂(2^k)` with all-2-power ramification indices. At `k = 4`
  this is closed unconditionally and explicitly: one universal degree-8 moduli field
  (disc `2¹⁸·5²·17`) catches every computed cover object — sixteen exact genus-0 covers,
  the genus-1 passport (via its j-invariant), and every short 4-point Hurwitz component
  (via boundary gluing). Family-wide closure (all `k`, and Suzuki groups) is conditional
  on a twice-calibrated transfer hypothesis whose combinatorial core — the `+1`-torus
  prime fixes every all-2-power passport — is proved. Includes the explicit
  Raynaud/Bouw–Wewers mixed-reduction data and a falsifiable `k = 8` prediction.

- **`main-result.md`** — the complete argument: 2-group Belyi maps (Galois *and*
  non-Galois) cannot produce a nonsolvable number field ramified only at 2. Rigorous
  except for one geometric input (Lemma B), which is verified computationally for all
  `|G| ≤ 128` (2008/2008 cases). The algebraic core (Lemma A) is formally proved in Lean 4
  (`../aristotle_solvable/FiniteLocalSolvable.lean`).

- **`lemma-B-open-problem.md`** — the sole remaining gap: proving `H¹(X, F₂)` is an
  indecomposable `F₂[G]`-module. Precise statement, the Gruenberg-relation-module
  framework, what has been ruled out (simple socle/top), a proof strategy (cyclic case
  first), the relevant literature, and computational experiments to pursue.

## One-paragraph summary

A nonsolvable number field ramified only at 2 **exists** (Dembélé 2009), but is not a small
explicit object. The thesis hoped to obtain an explicit one as `Q(J[2])` of a 2-group Belyi
curve. This fails: for such a curve, arithmetic Frobenius acts `F₂[G]`-linearly on
`J[2] = H¹(X, F₂)`, so the Galois image lies in `Aut_{F₂[G]}(J[2])`; when `J[2]` is
indecomposable this centralizer is solvable (Lemma A, Lean-verified), forcing `Q(J[2^∞])`
solvable. `J[2]` is indecomposable in all 2008 feasible cases (Lemma B, conjectural in
general). The non-Galois version is controlled by its Galois closure and dies with it. Hence
the construction provably cannot reach the (existing) field — a negative answer to Q1.2.5
for the torsion field, contingent only on Lemma B.
