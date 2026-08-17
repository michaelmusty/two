# Dimension-2 end-to-end calibration

**Date:** 2026-08-16. The experiment recommended by `roadmap-reevaluation.md`:
run the chain we had never run, at a scale where it is known to work, and
measure what it costs.

## Result 1: the chain works, and it finds the right object

Using `darmonpoints` **unmodified**, at `p = 5`, level 33 over `Q`
(`BigArithGroup(5, (1,1), 33, base=QQ, grouptype='PSL2')`):

```
STAGE group:                0.5 s
STAGE cohomology:           0.0 s   dimension = 49
STAGE twodim cocycle:       3.8 s   T_2 charpoly = x^2 - 3  (irreducible)
STAGE overconvergent lift f0: 41.6 s   (prec = 20)
STAGE overconvergent lift f1: 17.7 s
```

Independently of the package, the abelian surface here should be a
2-dimensional new component of level `165 = 5 * 33`, Steinberg at 5. Computing
that directly from modular symbols: level 165 has exactly two such components,
with `T_2` charpolys `x^2 + 2x - 1` and `x^2 - 3`, **both with `U_5 = -1` acting
as a scalar**. The package found the `x^2 - 3` one. Ground truth and pipeline
agree.

This also re-confirms, in exactly the setting the machinery is built for, the
claim the whole lift scoping rests on: `U_p = ±1` is a **scalar on the entire
component**, so the lift's eigenvalue normalisation is safe and the slope is 0.

## Result 2: the cost model was optimistic by three orders of magnitude

`gate4-lift-scoping.md` estimated the inner loop from raw Sage `p`-adic vector
arithmetic at 5.3 us per operation, giving ~110 core-hours for all 16 classes at
`Nq0 ~ 2000`, `M = 20`. Against the measurement:

- measured: 41.6 s at 49 positions, `p+1 = 6` cosets, `M = 20`
- implied per-operation cost: `41.6 / (49 * 6 * 20) = 7.1 ms`
- **1300x the synthetic 5.3 us**

The gap is structural, not incidental. Acting on a distribution by a group
element is an `O(M^2)` triangular action, not the `O(M)` vector scaling I timed;
that accounts for a factor ~`M = 20`. The remaining ~65x is Python object
overhead per call: group element arithmetic, embedding, and the distribution
class machinery. So the honest cost model is

    cost ~ positions x cosets x M^3        (iterations ~ M, action ~ M^2)

Calibrating the constant on the measurement (`c = 1.77e-5 s`) and extrapolating
to `Nq0 = 2111`, positions `58*(Nq0+1) ~ 1.2e5`:

| | `M = 20` | `M = 100` |
|---|---|---|
| per class | ~10 000 core-h | ~1.2e6 core-h |
| all 16 classes | **~1.6e5 core-h (18 core-years)** | ~2e7 core-h |

**With the existing Python stack, gate 4 is infeasible** — not marginal,
infeasible by three to five orders of magnitude.

## Result 3: but the floor is feasible, so this is an implementation problem

The same `O(M^3)` model applied to the *raw arithmetic* floor (5.3 us per `O(M)`
op, so ~`M` times that per distribution action) gives ~2 000 core-hours for all
16 classes at `M = 20` — four days on 24 cores. So:

| implementation | all 16 classes, `Nq0 ~ 2111`, `M = 20` |
|---|---|
| existing Python (`darmonpoints`) | ~1.6e5 core-h — infeasible |
| optimised (Cython/C, flint) | ~2e3 core-h — days |

The ~70x between them is an ordinary Python-to-C speedup for exactly this kind
of tight numeric loop. **Gate 4 therefore stands or falls on writing an
optimised overconvergent lift, not on any mathematical obstruction.** That is a
different project from "extend `darmonpoints`", and it should be scoped as one.

## What this changes

- The roadmap's gate-4 estimate of ~0.6 success should be read as: the
  mathematics is fine (scoping held up — `Q`-rational component, `U_p = ±1`,
  tree word problem), but the engineering is a rewrite of the inner loop, not
  an extension.
- The `Nq0^2` sensitivity is now sharper, since the constant is 1300x larger
  than assumed. A hit at low norm matters much more than the earlier table
  suggested.
- The remaining untested link is still the last one: periods -> square roots ->
  **recognition of the global 2-torsion field**. The lift is now validated; the
  recognition step is not, and it is what sets `M`, which enters cubically.

## Note on the root-choice ambiguity

`build_Lambdalist_from_AB` enumerates *all* root choices
(`our_nroot(..., return_all=True)`) and tests which yields recognisable Igusa
invariants — an enumeration that would grow exponentially in the dimension. It
appears not to threaten us: that search exists to pin one normalised period
matrix for the Igusa front end, whereas the 2-torsion **field** is the
compositum of all the square roots and is canonical. The ambiguity names a
point; it does not change the field.
