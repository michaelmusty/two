# Write-up: 2-group Belyi maps and nonsolvable fields ramified only at 2

Consolidated results of the investigation into Musty (2019) Q1.2.5 / Q6.2.1.

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
