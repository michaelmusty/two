# Precision refinement and hyperelliptic reconstruction (D48)

Date: 2026-09-15. Both user suggestions were tested. No algebraic model
or full-size arbitrary-precision differential basis was obtained.

**Later implementation:** [D49's compiled refinement](compiled-precision-refinement.md)
now evaluates arbitrary-precision residuals and refines all sixteen columns
at N=8192. The small-prototype limitation below is historical; independent
truncation checks still prevent interpreting its tiny linear residual as
40-digit differential accuracy.

## Completed remote run

Châtelet's N=12288 job finished with exit code zero and CANONICAL_JOB_OK.
Its independent 275-side residual is 4.01e-14. Against N=10240, normalized
jets differ by relative 1.51e-11 and quadric coefficients by 5.60e-12
(maximum absolute difference 1.01e-9). These are empirical diagnostics,
not certified errors. Full artifacts remain in `two_canonical_d46_20260915`.

## Newton / iterative refinement

For fixed geometry the differential problem is linear. With stabilized
matrix M=I-A+B B*, Newton's correction is iterative refinement:

    r=b-Mx; solve M delta=r; accumulate x <- x+delta.

A reusable double LU can supply approximate corrections while residuals
and accumulated coefficients use arbitrary precision. This requires a
sufficiently good approximate inverse; convergence at full size is not
automatic. See [Carson–Higham, Iterative Refinement in Three Precisions](https://eprints.maths.manchester.ac.uk/2629/1/cahi18.pdf).

Script 78 uses our actual N=64 Cauchy operator and QR-normalized truncated
basis for stabilization, solving one right-hand side. **N=64 is too small
for the target curve**: this is a solver-mechanism test. At 50 digits,
estimated matrix condition 2266, the relative residual progresses through

    2.01e-14 -> 4.86e-28 -> 9.83e-42 -> 1.05e-49.

The residual path uses arbitrary-precision nodes, Horner evaluation, and
DFT without forming a matrix. An independently assembled high-precision
matrix agrees to relative 7.90e-51. Solving the rounded matrix at high
precision instead leaves residual 7.88e-16 against the original matrix.
Therefore high-precision residual evaluation is essential.

Runtime is about three seconds locally. Direct Python Horner/DFT and the
explicit reference matrix are not a full-size production solver. Script
68 now optionally returns high-precision nodes via `as_numpy=False`;
its default interface still returns double arrays.

Next implementation: compiled matrix-free residual evaluation, e.g.
FLINT/Arb Horner plus FFT, checked against script 78; reusable double LU;
high-precision accumulation. Truncation and quadrature must be checked
independently. Existing geometry has only about 57 decimal digits, so
larger precision goals require a new geometry export. At our radius,
R^(32N) reaches roughly 1e-40 near N=32000, but this is **not an error bound
or a sufficient truncation criterion**. Multiple centers may be preferable
to a much larger dense system. Newton on internally consistent canonical
equations alone would not fix their analytic moduli.

## Hyperelliptic reconstruction attempt

Script 77 normalizes sixteen jets to I, with differentials H_i(u) du.
For a hyperelliptic curve at an ordinary point, the differential space is
spanned by h*x^i du, i=0,...,15. The two highest-vanishing forms force

    x=H15/H14; h=H14/x^14.

Construct these sixteen forms and normalize their first sixteen jets.
Those fitted coefficients match automatically; later coefficients test the
hypothesis. If the space matches, recover y=x'/h and check that y^2 is a
polynomial in x of degree at most 34. At a hyperelliptic branch point the
ordinary sixteen-jet matrix would be singular, unlike our computed matrix.

The target fails already at coefficient 16:

| Truncation | Maximum absolute coefficient-16 discrepancy |
|---|---:|
| 8192 | 745.5897317356 |
| 10240 | 745.5897317440 |

The discrepancy uses this fixed normalization, not an invariant distance.
Its cross-truncation stability and occurrence in the first unused jet are
the evidence. No target polynomial is accepted after this test fails.

Positive controls use the smooth genus-16 curve y^2=1+x+x^33, first in
its ordinary chart, then with x=u/(1-u/10), the appropriate derivative,
and a nontrivial basis change. Both pass the unused jets and polynomial
degree test. Formal-series arithmetic uses 100 decimal digits; it adds
no accuracy to the double-precision target inputs. At 70 digits the
changed-chart polynomial-tail control initially missed the strict 1e-45
tolerance (4.45e-40); increasing working precision resolves that conditioning
issue. The target discrepancy persists.

This independent reconstruction attempt supports D45's exact graph
obstruction and D46's gonality bound. Assuming hyperellipticity currently
does not provide an alternative model of the same curve.

## Reproduction

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/77_hyperelliptic_reconstruction.py
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/78_mixed_precision_refinement.py
```

Reports are `data/computed/hyperelliptic_reconstruction.{json,out}` and
`data/computed/mixed_precision_refinement.{json,out}`. Full-size arbitrary
precision remains unimplemented.
