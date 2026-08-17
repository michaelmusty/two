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

---

## Stage 2 (periods): abandoned — the package's period path has bit-rotted

Four distinct version-drift failures in one code path, each a level deeper:

1. `homology.py:483` `f_ell = R(f_ell_0)` — `get_twodim_cocycle` returns Hecke
   *matrices*, `get_homology_kernel` needs *polynomials* to form `f_ell(Aq)`.
   (`TypeError: rational_reconstruction()`.) Fixed by passing `T.charpoly()`.
2. Dropping the `Infinity` entry then breaks `assert len(ker) == 2` — the
   sign-at-infinity condition is load-bearing. Fixed by keeping it.
3. `pair_with_cycle` iterates `for g, a in xi`, but `get_homology_kernel`
   returns `ArithHomology` elements, which expose `.values()` indexed by group
   generators and are not iterable. Two incompatible homology conventions
   coexist in the package; the bridge is its own idiom from `homology.py:466`,
   `zip(group.gens(), x.values())`.
4. With that bridged, `self.evaluate(g)` returns a bare
   `Vector_integer_dense`, which has no `.pair_with`.

Stopped at (4). Beyond that point the work is reverse-engineering internal type
contracts, where a wrong guess yields **silently wrong periods** rather than an
error — the one failure mode a calibration cannot tolerate.

**This is itself a finding for the roadmap.** The fallback plan assumed
`darmonpoints` could serve as a working reference implementation to validate a
port against. "Reproduce the published dimension-2 result" is not turnkey; it is
a repair project of uncertain size.

## What replaced it: the recognition law, measured directly

The quantity the roadmap needs is *how much precision recognition consumes*, and
that reduces to a question independent of how the `q0`-adic approximation was
produced: given an algebraic number of degree `d` and height `H` known to `M`
digits, when does LLL recover its minimal polynomial? Measured at `q0 = 2003`:

| `d` | `log10 H` | `M` needed | `M / (d log_{q0} H)` |
|---|---|---|---|
| 2 | 10 | 12 | 1.98 |
| 4 | 5 / 10 | 8 / 16 | 1.32 |
| 8 | 5 / 10 | 16 / 28 | 1.32 / 1.16 |
| 16 | 5 / 10 / 20 | 28 / 56 / 108 | 1.16 / 1.16 / 1.11 |

So `M ~ 1.1-1.3 * d * log_{q0}(H)`, the classical LLL bound with a small
constant, confirmed at the `q0` we would actually use.

## The consequence, and the new binding unknown

For our target the recognition degree is **small**: the degree-257 polynomial
has coefficients in `Q(sqrt 2)`, so `d = 2`, giving

    M ~ 0.7 * log10(H)

with `H` the height of those coefficients. Since gate-4 cost goes as `M^3`, and
the optimised kernel is ~85-2000 core-hours at `M = 20`:

| `log10 H` | `M` | kernel cost multiplier vs `M=20` |
|---|---|---|
| 30 | ~21 | 1x |
| 100 | ~70 | ~43x |
| 300 | ~210 | ~1160x |

**The binding unknown is therefore `H`, the height of a defining polynomial of
`E/Q(sqrt 2)` — a property of the target field, not of the method.** No amount
of dimension-2 experimentation determines it, which is worth saying plainly:
even a fully repaired period pipeline would have given a height data point for
an abelian *surface*, and heights do not extrapolate from dimension 2 to 16.

`H` is estimable from arithmetic rather than experiment. `E` is ramified only at
2, so its discriminant is a power of 2 and its **root discriminant**
`|disc|^{1/n}` is what controls the size of a reduced defining polynomial. That
computation — bound `v_2(disc)` via the ramification filtration at 2, hence the
root discriminant, hence the expected height — is the next thing to do, and it
is cheap compared with repairing the pipeline.
