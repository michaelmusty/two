# Scope: the optimized overconvergent inner loop

**Date:** 2026-08-16. Follows `gate4-dim2-calibration.md`, which measured the
existing Python stack at ~1.6e5 core-hours for our case — infeasible — against a
raw-arithmetic floor three orders of magnitude below it. This is the scope of
closing that gap.

## What the inner loop actually is

From `cohomology_arithmetic.py:772` (`apply_Up`, non-Shapiro branch), stripped
to its essentials:

```python
for gamma in gammas:                                   # "positions"
    vals.append(sum(sk * c.evaluate(Gpn.get_hecke_ti(g, gamma))
                    for sk, g in zip(repslocal, Up_reps)))   # "cosets"
```

and the action itself, `ocmodule.py:239` + `:409`:

```python
tmp = self._parent._get_powers(x) * self._val     # (M x M integer matrix) * (M-vector)
```

`_get_powers(a,b,c,d)` builds the `M x M` integer matrix whose rows are the
coefficients of `((b+az)/(d+cz))^i`, and it is **cached on `(a,b,c,d)`**.

So each `(gamma, g)` pair costs: one group-theoretic coset reduction
`get_hecke_ti`, one cocycle evaluation, one `M x M` by `M` integer
matrix-vector product mod `q0^M`, and an accumulation.

## The three facts that make this a good rewrite target

1. **The action matrices are fixed.** `repslocal` is the same `Nq0+1` local
   representatives on every iteration and for every one of the 16 classes.
   There are only `Nq0+1` distinct `M x M` matrices in the entire computation,
   and the existing code already caches them.
2. **The combinatorial table is fixed.** `get_hecke_ti(g_k, gamma_j)` depends
   only on `(g_k, gamma_j)`, both fixed throughout. The map
   `(j,k) -> index of t_i` is therefore a **static table**, computable once and
   reused across all `~M` iterations and all 16 classes.
3. **Therefore `U_q0` is a fixed sparse block operator.** Precompute its
   structure once; every subsequent application is pure linear algebra with no
   group theory and no Python object churn:

   ```
   v_new[j] = sum_k  A_k * v_old[ T[j][k] ]        A_k : M x M over Z/q0^M
   ```

That reframing — from "iterate an object-oriented Hecke operator" to "apply a
precomputed sparse block matrix `M` times" — is where the speedup lives. The
existing implementation redoes the group theory and rebuilds Python objects
inside the innermost loop.

## Cost model, and what the rewrite buys

Per iteration: `positions x cosets x M^2` modular multiply-accumulates.
Iterations `~M`. So `positions x cosets x M^3` overall, matching the calibration.

For `Nq0 = 2111`, positions `58(Nq0+1) ~ 1.2e5`, all 16 classes:

| `M` | mulmods (per class) | entry size | optimised estimate (16 classes) |
|---|---|---|---|
| 20 | 1.9e12 | ~220 bits | ~85–2 000 core-h |
| 100 | 2.4e14 | ~1 100 bits | ~1e4–4e4 core-h |

against ~1.6e5 core-hours (`M = 20`) measured for the Python stack. The span in
the last column is the honest uncertainty in the per-mulmod constant (10 ns with
flint on 220-bit operands, up to ~100 ns with overhead). Even the pessimistic
end is days-to-weeks on 24 cores rather than decades.

Note the consequence for the precision worry: **`M = 100` becomes reachable**.
Since `M` is what the untested recognition step sets, and it enters cubically,
the rewrite is also what buys insurance against that unknown.

Memory is not a constraint: the state vector is `positions x M` entries of a few
hundred bits, ~67 MB per class at `M = 20`; the `Nq0+1` action matrices are
~22 MB.

## The work, in order

1. **Table construction.** Build `T[j][k]` and the `A_k`. In the Fuchsian
   setting this means `Nq0+1` times `positions` word problems (~2.4e8 calls —
   the one genuinely expensive setup step, though it is one-time and shared
   across all 16 classes). **In our definite/CD setting this table is the Brandt
   neighbour structure at level `q0`, which we already compute** — this is
   exactly the plan's "the tree quotient and Hecke action are already in our
   hands", and it is the single biggest saving available.
2. **The kernel.** C or Cython over flint (`fmpz`/`nmod` depending on how
   `q0^M` is represented): a fixed sparse block matvec, `A_k` applied to
   indexed slices of the state vector, accumulating. Parallel over `j` trivially,
   and over the 16 classes trivially. Perhaps 500–1000 lines.
3. **The driver.** Greenberg's iteration (apply twice per loop, watch the
   valuation) around the kernel — a direct transcription of `improve`, which is
   short and eigenvalue-agnostic.
4. **Eisenstein projector.** Replace the scalar division by the inverse of
   `T_ell - N(ell) - 1` restricted to the component (see
   `gate4-lift-scoping.md`).

Rough effort: kernel 1–2 weeks, table reuse ~1 week, glue and validation ~1
week. Call it a focused month, with the caveat that item 1 in the definite
setting has not been prototyped.

## Validation is already available

The calibration gives a **hard regression test**: `p = 5`, level 33, `prec = 20`
produces a specific overconvergent class `Phi0` in 41.6 s through the reference
implementation. Any rewrite must reproduce its moments exactly. That is a
much stronger test than a smoke test, and it exists now.

Staged validation:

1. Rewrite reproduces `Phi0` at `p = 5`, level 33, `M = 20` — bitwise.
2. Same at `p = 13` and `M = 40`, to exercise the scaling paths.
3. Timing curve in `Nq0` and `M`, checked against the `positions x cosets x M^3`
   model before committing to the degree-8 run.

## Recommendation, and what would stop this

The rewrite is well-defined, has a fixed target, a hard regression test, and no
unknown mathematics. But it is a month of work whose value is entirely
contingent on two things not yet known:

- whether gate 1 produces a hit at usable norm (currently 32 primes, 0 hits);
- whether the recognition step closes at all, and at what `M`.

The second is still the cheapest unknown to attack, and it does **not** need the
fast kernel — the reference implementation can compute periods at `p = 5` in
under a minute. **So the order should be: finish the dimension-2 calibration
through periods and recognition first, and only then write the kernel.** The
kernel is what makes the degree-8 case runnable; the recognition step is what
decides whether the degree-8 case is worth running.
