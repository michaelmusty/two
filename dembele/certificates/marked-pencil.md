# The five marked points of the canonical pencil (D55)

Date: 2026-09-15. The user authorized the proposed scan of all 60
normalizations of D54's weight-22 pencil, followed by comparison and
bounded recognition over F = Q(zeta_32)^+.

**Outcome:** the scan is complete. Recovering this pencil directly from
25 differential products, instead of the previously interpolated full
quadric ideal, reduces the discrepancy between two fits by factors of
162 and 60 in the two selected coordinates. The earlier apparent field
match is one candidate in two equivalent charts; both direct
reconstructions reject it at their stated empirical tolerances. No field
candidate survives. No exact curve or target field polynomial is obtained.

**Additional mathematical result:** the marked configuration depends only
on the vanishing flag at P. Its conditional F-definition does not need
D52's intrinsic formal parameter or weight-one scaling coefficients.
A simpler complex basis recovers the same configuration numerically, and
exact controls verify the basis invariance. This simplifies the target;
it does not establish an arithmetic height bound or certified accuracy.

Implementation: [`90_marked_pencil.py`](../pari/90_marked_pencil.py).
Detailed results: [`marked_pencil_comparison_16384.json`](../data/computed/marked_pencil_comparison_16384.json).

## Why the marked configuration is defined over F

Retain the canonical-model interpretation and F-rational point P from
[`genus64-cover.md`](genus64-cover.md). The following argument is conditional
on the numerical differential space being the true H^0(C,K), on P having
vanishing orders 0,...,15, and on the rank and nonvanishing assumptions below.

Let V = H^0(C,K), with filtration V_i = H^0(C,K-iP). Each nonzero graded
piece is one-dimensional over F. Choose any basis X_i adapted to this
flag, so ord_P(X_i)=i. It may be a complex basis for numerical purposes.
The intrinsic induced filtration on Sym^2(V) has step

    S_22 = span{X_i X_j : 0 <= i <= j <= 15, i+j >= 22},

of dimension 25. Multiplication sends it into H^0(C,2K-22P), which has
dimension 23 by Riemann--Roch: deg(2K-22P)=38>30=2g-2. Assuming this
restricted multiplication map has rank 23, its kernel W is a
two-dimensional F-defined space of canonical quadratic relations.

The degree-22 graded piece of Sym^2(V) is the direct sum of the five
one-dimensional spaces corresponding to

| Label | Leading monomial |
| --- | --- |
| 0 | X7 X15 |
| 1 | X8 X14 |
| 2 | X9 X13 |
| 3 | X10 X12 |
| 4 | X11^2 |

Project W to each summand. A nonzero projection has a one-dimensional
kernel, an F-rational point of P(W). Assume these five points are distinct.
Their ordered cross-ratios then belong to F.

Indeed, a flag-adapted change replaces X_i by a nonzero multiple of X_i
plus terms of higher vanishing order. On the degree-22 graded piece,
each of the five components changes only by a nonzero scalar. Its kernel
in W is unchanged. A change of basis of W applies one common projective
transformation to all five points, leaving the cross-ratios unchanged.
This proves invariance under the entire flag-preserving triangular group,
including arbitrary complex diagonal balancing. It does not assert that
the coefficients of the balanced numerical pencil themselves lie in F.

The hypotheses are numerically supported here, not certified by the
floating-point rank computation. These are points on the **parameter
line of a quadric pencil**; they have not been identified as branch points
of a Belyi map on C.

## Normalization and the size of the search

For a basis Q0,Q1 of W, let ell_i=(a_i,b_i) be the coefficient covector
of marked monomial i. Its zero is p_i=(b_i:-a_i). For ordered distinct
labels (a,b,c), the transformation sending their zeros to (0,infinity,1)
gives the remaining point j the coordinate

    z_j = det(ell_j,ell_a) det(ell_c,ell_b)
          / (det(ell_j,ell_b) det(ell_c,ell_a)).

All 5*4*3=60 choices are evaluated. Their 120 displayed coordinates
contain only 30 distinct cross-ratio expressions, after the Klein-four
symmetries. For each four-point subset the remaining six expressions are
Mobius transforms of one another. They are not independent evidence of
an algebraic match, nor 30 algebraically independent invariants.

Rank each chart by its maximum same-checkpoint, two-fit **chordal**
discrepancy divided by the minimum chordal separation of its five points.
The discrepancy across checkpoints breaks ties. This avoids calling a
mere shrinkage of affine coordinate size an improvement. All three
reconstruction methods select labels (0,4,3) for (0,infinity,1). The
minimum separation is approximately 0.04146785. On the quotient input,
the score improves by only 2.45 times versus the baseline (0,1,2);
changing the reconstruction method supplies the much larger gain.

## Direct recovery and independent checks

The first scan used D54's 45-by-25 quotient matrix extracted from its
full set of quadrics. The default implementation now constructs only the
25 required products directly from the native differential checkpoints.
It interpolates 23 constraints and checks every available product jet.
This avoids propagating error from interpolation of all 91 quadrics.

The current and alternative fits use 256 and 61 training jets, checking
512 and 128 jets respectively. The 12288 and 8192 checkpoints each use
the longer window. These are the same saved banks used by D54; no new
large analytic solve was launched. Native ball polynomial arithmetic
controls arithmetic on supplied point data, not geometric error.

The selected chart, from the direct reconstruction in D52's basis, is

    p1 ~ 0.4524253658944293154321026 - 1.932e-22 i,
    p2 ~ 0.0415035453978846651218881 - 2.999e-22 i.

The displayed decimals preserve the computation; they are not all
asserted correct digits of an exact algebraic number.

| Diagnostic | p1 | p2 |
| --- | ---: | ---: |
| Quotient reconstruction: difference between current fits | 2.802e-20 | 2.394e-19 |
| Direct reconstruction: difference between current fits | 1.732e-22 | 3.970e-21 |
| Reduction in that discrepancy | 161.8 times | 60.3 times |
| Direct: change from n=12288 to n=16384 | 1.175e-16 | 1.882e-16 |
| Direct: difference after replacing D52's basis by the simple flag basis | 2.433e-22 | 1.894e-21 |
| Direct arithmetic-basis exploratory tolerance | 1e-20 | 1e-19 |

The simple flag basis inverts only the first 16 raw jets, then balances
each differential by its coefficient norm. It never constructs the D52
formal parameter or scale. All 30 cross-ratio expressions agree between
these two bases within both of their exploratory tolerances; the largest
discrepancy is 0.0812 times the smaller tolerance. Both bases nevertheless
use the same current checkpoint. This is a normalization check, not an
independent geometric approximation.

The direct product constraint residuals for n=16384,12288,8192 are
1.96e-25, 4.76e-20, and 5.38e-15 respectively. The alternative current fit
has residual 7.35e-25. All four direct product matrices exhibit numerical
rank 23 at the 1e-12 relative threshold. The older **quotient** matrix has
numerical rank 25 at that threshold; using it as a noisy comparison is
explicit in the report and requires a large singular-value gap. It is
not silently treated as an exact rank-23 matrix.

The exploratory error estimate uses the equally spaced n=8192,12288,16384
sequence. If q is the latest difference divided by the preceding one,
and q<1/2, it estimates the remaining tail by latest_difference*q/(1-q).
The search tolerance is ten times the largest of that estimate, the
two-fit discrepancy and the imaginary part, rounded up to a power of ten.
Without a decreasing ratio it uses the full latest checkpoint change.
**Geometric convergence is not proved.** These are discovery tolerances;
they do not replace the substantially larger measured checkpoint changes
with certified error bounds.

## Recognition and the rejected candidate

The search uses script 87's integral cosine bases, with
b=2*cos(7*pi/16), a root of b^8-8b^6+20b^4-16b^2+2. Its integer-relation
coefficient limits are 1000,100,8 for degrees 1,2,4 and 4,8,16,32 for
degree 8. All 30 expressions are searched. The best two coordinates are
also tested with degree-eight limit 64. A relation-height setting bounds
the integer coefficients and denominator in the chosen basis; it is not
a bound on absolute Weil height. PSLQ failure is not a height lower bound
or a proof that no relation in that range exists.

The quotient reconstruction produced two positive trials at degree 8
and limit 32. Their displayed values are approximately -23.09432713 and
24.09432713, related by z -> 1-z. Exact arithmetic in F identifies them
as **one** candidate on the same four labels (0,2,3,4). One relation was

    [-15,-9,2,0,-26,-27,-29,29,-6]

in the eight cosine basis elements followed by the target value. Its
quotient residual was 5.26e-16, within the then-used 1e-14 tolerance and
even the ten-times-tighter trial. Those checks alone were misleading.

With direct products, all six equivalent charts fail their new
exploratory tolerances by factors between 5.78 and 10.84. The simple flag
basis independently reproduces this failure, by factors 5.77--10.82.
The retained status is **incompatible with current empirical accuracy**,
not a theorem of inequality to an exact invariant. No replacement
candidate was found in 210 full-scan trials, or the 16 trials for the
best chart through limit 64 in either direct basis.

## Controls, provenance and reproduction

Seven tests in [`test_marked_pencil.py`](../tests/test_marked_pencil.py)
cover independently specified pencil reconstruction, unused constraints
and wrong ranks, exact Mobius transformations, infinity, complex basis
changes, coincident-point rejection, known F/subfield recognition,
convergence diagnostics, and exact triangular invariance.
The five finite branch points of the user's actual thesis Q8 curve are
loaded from [`belyi/validate_q8.sage`](../../belyi/validate_q8.sage) for an
exact reference configuration. This does not claim that the genus-two
control has the target's quadric pencil. All **78** repository tests pass.

From the repository root, using existing checkpoints:

```sh
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/90_marked_pencil.py --method quotient \
  --heights 4 8 16 32 --output /private/tmp/marked_pencil_quotient.json
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/90_marked_pencil.py --method direct \
  --heights 4 8 16 32 --output /private/tmp/marked_pencil_direct.json
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/90_marked_pencil.py --method direct \
  --best-only --heights 4 8 16 32 64 \
  --audit-candidates dembele/data/computed/marked_pencil_16384.json \
  --output /private/tmp/marked_pencil_direct_audit.json
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/90_marked_pencil.py --method direct \
  --basis-gauge flag --best-only --heights 4 8 16 32 64 \
  --audit-candidates dembele/data/computed/marked_pencil_16384.json \
  --output /private/tmp/marked_pencil_flag.json
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python -m unittest discover -s dembele/tests -v
```

Saved JSON and matching `.out` stems in `data/computed/`:

- `marked_pencil_scan_16384`: initial quotient scan without recognition.
- `marked_pencil_16384`: quotient scan and its rejected candidate.
- `marked_pencil_direct_16384`: all 30 expressions with direct products.
- `marked_pencil_direct_audit_16384`: best-chart search through 64 and
  exact deduplication/numerical rejection of the older candidate.
- `marked_pencil_flag_16384`: the same search and audit in the simple basis.
- `marked_pencil_comparison_16384`: differences, conditioning ratios and
  SHA256 hashes of the three compared reports. Its entries are calculated
  by matching `cross_ratio_orbit` keys in their `normalizations` arrays.

The initial quotient report's SHA256 is
`fd4b37e082637170af2a8c5856fad5864b9ae10bd3f8a31e6a0e27db17d060fd`.
Both candidate audits record this hash. Input checkpoint/report provenance,
interpolation choices, numerical ranks and residuals are retained in the
reports. Recognition scans take about 5--12 seconds locally.

## Consequence for the route to the field

The promised coordinate experiment is finished. It gives a simpler,
intrinsic arithmetic target and a more stable way to compute it, but
no exact relation for reducing the relative cubic. Rescanning the same
60 charts or changing a flag-preserving basis cannot change these
intrinsic cross-ratios. The hypothesis that this particular normalization
would reveal readily recognizable small coefficients was unsuccessful
at the available accuracy and bounds.

The next substantive input must address arithmetic reconstruction:
an independently justified height/precision budget for these two
invariants, or additional arithmetic data such as corresponding
conjugates or reductions with which to recover them. First audit which
of those inputs can actually be computed for this pointed Shimura curve;
the saved single-embedding numerical data do not supply them. Raising
n again without that information has no demonstrated success threshold.
An exact pencil would still be only part of an exact C model; the cover's
48 new directions, exact Y and target torsion remain separate tasks.
