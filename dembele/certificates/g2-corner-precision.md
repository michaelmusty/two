# The k=4 genus-2 corner: not decided at 285 digits, and why

**Date:** 2026-08-16. **Scripts:** `dembele/rigidity/31_g2_local.m` (24 h local
run, working precision 285), `dembele/rigidity/32_g2_field.m` (offline
gauge-invariant recognition). **Dump:** `dembele/rigidity/out/g2_rep1_cfs.m`.

## Result

The moduli field of rep 1 of the (2@0, 8@phi, 8@phi^3) passport is **not
determined by this run**. No absolute Igusa invariant admits a certifiable
algebraic relation of degree ≤ 24. This is a *precision* verdict, not a
mathematical one: it says nothing about whether the corner closes.

## The measurement that settles the interpretation

The numerical curve carries **~25 correct digits**, not the 285 it formally
reports. Three independent facts pin this down:

1. **No relation, and provably noise.** Fitting each absolute invariant at a
   ladder of LLL precisions (114 / 156 / 199 / 228), the fitted height grows
   linearly with precision at *every* degree from 1 to 24 — `h ≈ P/(d+1)`, the
   signature of LLL saturating the lattice on noise. A genuine minimal
   polynomial locks onto a fixed height once `P > d·log10(H)` and stops moving.
2. **The invariant formulas are not the problem.** Applying a nontrivial gauge
   `t -> (at+b)/(ct+d)`, `y -> λy/(ct+d)^3` to the dumped curve and recomputing
   reproduces the absolute invariants to **257–274 digits**. The Igusa pipeline
   preserves essentially full precision.
3. **The package's own two outputs disagree at digit 25.** `hyperelliptic.m`
   prints `curve_coeffs` after the kernel solve; `recognition.m` dumps them
   after `TriangleRescaleCoefficients`. Their ratios satisfy
   `log|r_i| = -2log|β| + i·log|α|` — exactly a weighted gauge, so the two are
   the *same curve* and their absolute invariants are mathematically equal.
   They agree to **24–26 digits**.

(2) rules out the recognition step and (3) localises the loss upstream, in the
power-series → `NumericalKernel` construction of the curve. Note the Arnoldi
eigenvector itself converged to ~1e-273, so the loss is in the kernel solve
that turns the series into curve coefficients, not in the series.

There is **no Newton refinement in this path** — the log contains no Newton
output at all. The genus-2 flow runs power series → curve → Belyi map →
recognition, so nothing recovers the lost digits downstream.

## Consequences

- Recognising a degree-`d` invariant of height `H` needs `≳ d·log10(H)` digits.
  At 25 usable digits, nothing beyond degree 1 is certifiable. The negative
  result is therefore uninformative about the moduli field.
- The `MakeK` search the package runs at `DegreeBound = 24` is working from the
  same ~25-digit data and cannot succeed legitimately; a "success" there would
  be a spurious field and should not be trusted.

## Options

1. **Rerun at higher working precision.** Conditioning loss is a property of
   the matrix, not of the working precision, so the ~260-digit loss should be
   roughly constant: ~500 digits in should leave ~240 usable. Cost is the
   issue — Arnoldi iteration count scales with the target `eps_thresh` (253
   iterations to reach 1e-276) and per-iteration cost with precision, so
   285 → 500 digits is plausibly 6–8×: **roughly a week**.
2. **Diagnose the kernel solve.** If the ill-conditioning is a fixable
   construction detail (basis choice, evaluation points), the fix is far
   cheaper than brute-force precision. Higher value, uncertain payoff.
3. **Leave it.** This corner is a *verification* of an arc that is already
   closed and written up negatively; it is not on the critical path to the
   polynomial. The period-route scan is.

## What was gained

`32_g2_field.m` is now a working, validated instrument: gauge-invariant by
construction, using low-weight Igusa ratios (the classical `I2^5/I10` triple is
weight 30 and reaches height 1e22 at degree 12 — uncertifiable at 285 digits),
with a precision-ladder noise test that a fixed height threshold cannot
replicate. It correctly refused to report a field here rather than emitting a
plausible-looking wrong one, and it recovers `Q(sqrt 2)` and `Q` from
gauge-transformed synthetic dumps. Whenever a higher-precision dump exists,
the verdict is seconds away.
