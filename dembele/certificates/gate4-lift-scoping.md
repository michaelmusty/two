# Scoping the overconvergent lift for a 16-dimensional component

**Date:** 2026-08-16. Follows `gate4-darmonpoints-assessment.md`. Question: what
has to change in the overconvergent lift when the Hecke eigensystem takes values
in a degree-16 field `H` rather than in `Q`?

## Answer: much less than expected — and not where the previous note said

**Correction first.** The previous note concluded that "the overconvergent lift
is the piece that must be rewritten over `H ⊗ Q_q0`". That was wrong, and it was
wrong because I read the `ZZ(...)` coercion at cohomology_arithmetic.py:489
without asking *which* eigenvalue it coerces. It is the `U_p` eigenvalue, and
for our situation that is `±1`. The lift needs no rewriting; one Eisenstein
normalisation does.

**The structural point.** The 16-dimensional isotypic component is
**`Q`-rational**: it is the sum of the 16 Galois-conjugate eigensystems, so it
is cut out over `Q` and is a `Q_q0`-subspace of the cohomology. The
overconvergent lift is `Q_q0`-linear and Hecke-equivariant, so it applies to a
*basis* of that component without ever meeting `H`. The `H ⊗ Q_q0`-module
structure is needed only afterwards, to organise the resulting 16 periods into
the rank-1 `H ⊗ Q_q0`-module whose quotient is `B_g`. So:

> Do the lift over `Q_q0` on the rational rank-16 component. `H ⊗ Q_q0` enters
> only at period assembly, after all the overconvergent work is finished.

## The three sites where rationality appears, and their verdicts

| site | what it divides by | verdict |
|---|---|---|
| `cohomology_arithmetic.py:489` `scale = ZZ(self.Tq_eigenvalue(p))**-1` | the `U_p` eigenvalue | **survives** |
| `cohomology_arithmetic.py:354` `scale = (self.Tq_eigenvalue(q) - q - 1)**-1` | an auxiliary `T_q` eigenvalue | **the one real fix** |
| the component search (`U0.dimension() == 2`) | — | driver-level; bypassed |

And the lift iteration itself (`improve` / Greenberg's method, lines 845–900)
is **eigenvalue-agnostic**: it calls `apply_Up(..., scale=1)` twice per loop and
iterates until the valuation stops rising. Nothing about `H` can reach it. Note
that applying `U_p` *twice* per iteration is exactly what makes the fixed-point
iteration converge when the eigenvalue is `±1` — our case precisely.

### Why site 489 survives: `a_q = ±1`, verified

For a newform Steinberg at `q` (`q || N`, parallel weight 2) the `U_q`
eigenvalue is `±1` — rational, however large the Hecke field. Checked on 15
newforms with Hecke fields of degree 1–4 (levels 43, 61, 67, 73, 97, 109): in
every case `a_q = ±1` while the other eigenvalues generate the whole field, e.g.
level 97, Hecke field `x^4 - 3x^3 - x^2 + 6x - 1`, `a_97 = 1`, `a_2` a generator.

The operationally relevant statement is stronger, since the class we lift is an
arbitrary element of the component rather than an eigenvector: **`U_q` acts as a
scalar on the entire isotypic component.** Verified on the modular symbols
directly — for the 4-dimensional components at levels 97 and 109 and the
3-dimensional one at level 61, the matrix of `U_q` restricted to the component
is `±1` times the identity, charpoly `(x-1)^4` resp. `(x-1)^3`. Hence
`Tq_eigenvalue`'s `ans = ZZ(f/f0)` returns `±1` for *any* class in the
component, and the `ZZ` coercion is safe.

Two consequences beyond the coercion: the `U_q` slope is **0**, so the
overconvergent lift exists and is **unique**; and the sign is Galois-stable, so
it is the same `±1` across all 16 conjugates.

### Why site 354 is the real fix, and what replaces it

For an auxiliary prime `q`, `a_q` genuinely generates `H` — verified in the same
experiment: `T_2` restricted to the level-97 component has irreducible charpoly
`x^4 - 3x^3 - x^2 + 6x - 1`, i.e. it is *not* a scalar, so `ZZ(f/f0)` fails
structurally (not merely by coercion — `f` is not a multiple of `f0` at all).

The purpose of that line is only to make `T_q - Nq - 1` a projector onto the
cuspidal part. The generalisation is to stop treating it as a scalar and invert
it as an **endomorphism of the component**. That is legitimate exactly when the
restriction is invertible, which was verified in the same experiment:

| component | `det(T_2 - 3)` | `det(T_3 - 4)` |
|---|---|---|
| level 97, dim 4 | 8 | 176 |
| level 109, dim 4 | 54 | 36 |
| level 61, dim 3 | −10 | −20 |

all nonzero (these determinants are the norms `N_{H/Q}(a_q - Nq - 1)`, nonzero
precisely because the component is cuspidal and `q` is a good prime). So the
replacement is: apply `T_q - Nq - 1` to the lifted class and then apply the
inverse of the `16 x 16` matrix of that operator on the component — or,
equivalently, multiply by `(a_q - Nq - 1)^-1 ∈ (H ⊗ Q_q0)^×` once the component
is presented as a rank-1 `H ⊗ Q_q0`-module.

## What the new code actually is

1. **Component supply.** Cut the 16-dimensional isotypic component out of the
   level-`q0` cohomology using our own Brandt data, bypassing the dimension-2
   component search entirely.
2. **Eisenstein projector.** Replace the scalar division at site 354 by the
   inverse of the endomorphism `T_q - Nq - 1` restricted to the component.
3. **Lift a basis.** Run the existing Greenberg iteration unchanged on each of
   16 basis classes.
4. **Period assembly.** Only here does `H ⊗ Q_q0 = prod_{λ | q0} H_λ` appear,
   organising the 16 integrals into the period lattice `Λ` with
   `B_g ≅ (K_q0^×)^16 / Λ`.

Items 1, 2 and 4 are new; item 3, the part that looked like the hard core, is
reuse.

## Cost, and the risk that has not been retired

The remaining risk is not algebraic but computational, and it is concentrated in
step 3. Rough figures for `Nq0 ~ 2000`:

- the cocycle lives on the level-`q0` structure of size `58·(Nq0+1) ~ 1.2e5`
  (the plan's gate-2 figure), so a lifted class is ~`1.2e5` overconvergent
  distributions;
- at ~20 moments and ~28 bytes per moment that is ~65 MB per class, ~1 GB for
  all 16 — comfortable;
- but each `apply_Up` sums over `Nq0+1 ~ 2000` coset representatives at each of
  `1.2e5` positions, i.e. ~`2.4e8` distribution operations per application, and
  the iteration wants ~20 of them.

That is ~`5e9` moment-level operations for one class, ~`8e10` for sixteen.

**Measured, rather than guessed.** Timing the inner operation (scale-and-
accumulate on a moment vector) in Sage's `Zp` arithmetic at the `q0` we would
actually use:

| `p` | moments `M` | per operation | one class | sixteen classes |
|---|---|---|---|---|
| 2003 | 20 | 5.3 us | 6.9 core-hours | **110 core-hours** |
| 2003 | 40 | 10.6 us | 13.7 core-hours | **219 core-hours** |

So the dominant loop is of order `1e2` core-hours, and the sixteen basis
classes are **independent — embarrassingly parallel**. That is days on one
core, well under a day spread across the machine. This is feasible, and it
revises the earlier "not in the Python layer these modules are written in":
even generic Sage `p`-adic vector arithmetic is fast enough at this size.

Caveats, so the figure is not over-read: it counts only the inner loop, and
ignores per-position group bookkeeping inside `apply_Up`, which could add a
constant factor; `M = 20` moments and ~20 iterations are placeholders until the
precision analysis is done (the table shows the cost is close to linear in `M`);
and it assumes the level-`q0` structure really is `58·(Nq0+1)`. Treat it as a
lower bound of the right order, not a schedule.

## Validation performed

- `a_q = ±1` for Steinberg newforms with Hecke field of degree up to 4 — 15
  newforms, levels 43–109 (`scratchpad/steinberg.sage`).
- `U_q` acts as a scalar on the whole isotypic component; `T_ell` does not;
  `T_ell - ell - 1` is invertible on the component — dimensions 3 and 4, levels
  61, 97, 109 (`scratchpad/isotypic.sage`).
- darmonpoints' own pipeline runs end to end in this environment: the classical
  Stark–Heegner point `darmon_point(7, EllipticCurve('35a1'), 41, 20)` in 9.1 s.

Not yet validated: the lift on a component of dimension > 1 (their dimension-2
path is the natural test, and reproducing a published Guitart–Masdeu abelian
surface remains the right next check), and everything in the cost section.
