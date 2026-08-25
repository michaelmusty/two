# Gate 5: can the Eisenstein back end run on q0-adic input?

**Date:** 2026-08-25. Desk work, no compute. Prompted by an over-broad criticism
of my own (see "correction" below).

## First, a correction

I claimed the plan's step 5 was under-specified — that going from a q0-adic
period lattice to a *global* polynomial had no stated mechanism, and that naming
torsion points algebraically would require a model of a 16-dimensional abelian
variety (theta-level difficulty, which the plan says it escapes).

**That was wrong**, and `csv-paper-adaptation.md` says so plainly:

> `#P^1(F_256) = 257` ... so a separating modular invariant gives a degree-257
> polynomial whose splitting field [is E] ... where the 257 matrices `gamma`
> represent the `lambda`-isogeny neighbours.

The mechanism is the Costa–Schiavone–Voight isogeny-polynomial construction.
The **257 λ-isogeny neighbours of `B` correspond to the 257 points of
`P^1(F_256)`**, Galois permutes them, and a separating invariant evaluated at
each yields 257 *algebraic* numbers whose minimal polynomial is the target. The
"square roots of lattice data" produce the neighbours (index-2 sublattices of
`Λ`); the invariant is what makes them algebraically nameable. No model of `B`
is needed — only an invariant that **separates**. That is exactly what the
Eisenstein prototype was built and tested for.

## The real question, and a reason for optimism

The prototype is **archimedean**: it evaluates

    E_4(z) = 1 + (240/541) * sum_{0 << nu in d^-1} sigma_3((nu) d) exp(2 pi i Tr(nu z))

with a complex cutoff, enumerating totally positive codifferent elements as
lattice points via Normaliz. It was built for the Oda route — which is dead. The
CD route delivers **q0-adic** periods, so the invariant must be evaluated
q0-adically.

**This looks like a small change, not a reimplementation.** For a
Mumford/CD-uniformized abelian variety the period-lattice generators
`q_ij` in `K^x` are topologically nilpotent, so the *same q-expansion* converges
q0-adically with `exp(2 pi i Tr(nu z))` replaced by the period monomial `q^nu` —
exactly how `E_4` is evaluated on a Tate curve. So:

| step | archimedean | q0-adic |
|---|---|---|
| enumerate totally positive `nu` in `d^-1` | Normaliz polytope | **same** |
| divisor sums `sigma_3` | exact | **same** |
| evaluate the term | `exp(2 pi i Tr(nu z))` | `q^nu`, a period monomial |
| cutoff | `abs(exp) < eps` | `v_q0(q^nu) > M` |

The expensive arithmetic is shared; the analytic evaluation is the only genuine
change. Calling the back end "READY" still overstates it — it is ready for input
this route does not produce — but the gap is narrower than "build a p-adic
theory".

## Two things that remain genuinely unverified

1. **Separation at our point.** The genus-4 control separated 17 neighbours. The
   certificate's own to-do says "prove or verify that its ratios separate the
   257 neighbours at our point". If the invariant fails to separate, the
   degree-257 polynomial degenerates. Untested at genus 16.
2. **Term count.** The archimedean run needed 5 007 to 80 286 terms at genus 4.
   The q0-adic term count is governed by the *valuations* of the periods: we
   need every `nu` with `v(q^nu)` below the precision target, so periods of
   small valuation mean many terms. Nobody has estimated this, and it enters the
   cost directly.

## Consequence for sequencing

Both items are desk-or-small-compute questions, and both gate roughly two months
of engineering (the definite S-arithmetic group class plus the kernel rewrite).
Item 1 in particular is a property of the invariant, testable in principle at
smaller genus before any of gate 4 is written.
