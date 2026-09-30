# Compiled arbitrary-precision residual evaluation (D49)

Date: 2026-09-15. This continues the immediate D48 handoff objective.
The new code solves finite stabilized differential systems with arbitrary-
precision residuals and accumulated coefficients, using a reusable double
LU factorization for approximate corrections. Independent quadrature and
side checks remain necessary to assess differential accuracy.

## Operator and arithmetic

For n coefficients, m sampling nodes, and offset s, the operator is

    (Ac)_k = exp(-2*pi*i*k*s/m)/m *
             sum_t weight_t H(node_t) exp(-2*pi*i*k*t/m),
    H(z) = sum_(j=0)^(n-1) c_j z^j.

`pari/cm_acb.c` evaluates the finite polynomial using FLINT's compiled
Horner or rectangular evaluation and applies a reusable arbitrary-precision
DFT plan. Its sign and normalization agree with the independent direct DFT
in script 78. Independent column workers each own their FFT plan and scratch
storage; the threaded and serial outputs agree bit for bit in the controls.
The native operator uses linear storage in the samples and
coefficient count; polynomial evaluation still costs O(mn) per column.
It is not a fast multipoint algorithm of quasilinear complexity. The dense
double correction matrix still needs O(n^2) memory and O(n^3) factorization.

The implementation uses the
[FLINT polynomial interface](https://flintlib.org/doc/acb_poly.html) and
[DFT interface](https://raw.githubusercontent.com/flintlib/flint/v3.6.0/doc/source/acb_dft.rst).
The latter documents the negative-exponent transform and reuse of a plan
initialized at the working precision. The build uses the development
headers and library exposed by `pkg-config flint`, records the compiled
version, and caches the library by source, flags, and version. In Sage's
local environment this selects FLINT 3.1.0; the separate Homebrew FLINT
3.6.0 installation is not implicitly selected by these runs.

The double seed is orthonormalized to B. One double factorization of

    M = I - A + B B*

is reused for every correction and right-hand side. The native code
evaluates r = B - M X, chooses a separate power-of-two scale per column,
converts only the scaled residual to double, and accumulates the rescaled
double correction at arbitrary precision. Thus residuals beyond the double
exponent range survive conversion. Accumulated iterates are dyadic points:
after each correction the midpoint is retained, and the next residual
evaluation encloses the action on that point.

FLINT balls account for arithmetic rounding on the supplied decimal data.
They **do not enclose the exact geometric inputs or any omitted infinite
series**. At 50 requested decimal digits the backend uses 207 bits,
including 40 guard bits. Geometry is replayed at 70 digits to suppress
additional rounding, but the source still contains only about 57 decimal
digits; replay does not manufacture further geometric accuracy. Even the
SU(1,1) metric check of that source has a residual near 1e-49.

## Validation and saved results

Eight native regression tests cover the independent DFT, complex phases,
prime-length transforms, batched columns, the conjugate stabilizing
projection, independent polynomial evaluation, decimal information below
double precision, per-column residual scaling at 1e-450 and 1e450, exact
checkpoint round trips, and rejection of invalid inputs. The serial/threaded
comparison also checks reuse of independent worker plans. The existing
double node/operator path agrees exactly after extracting its matrix
assembly into `operator_from_nodes`.

At n=64 with two right-hand sides, the compiled action agrees with script
78 to relative 2.64e-61. The worst finite-system residual progresses

    2.00e-14 -> 5.19e-28 -> 1.64e-41.

This run uses one factorization and three solves, including the initial
solve. It takes about 0.34 seconds locally, including direct-reference and
independent audits. As expected, the unused-side residual is about 1.4
and the changed-quadrature residual about 1.7: this small truncation is
not a differential basis. This is a useful negative control for the
distinction between solving M X = B and approximating automorphic forms.

The n=4096 experiment refines all sixteen columns with one factorization
and two corrections. Its maximum linear residual is 3.48e-41, but the
original finite Cauchy defect is 1.99e-6, the larger-quadrature defect is
1.86e-6, and the unused-side defect is 1.87e-4. The normalized jets still
have relative imaginary norm 4.64e-4. This directly exposes the truncation
limitation, despite accurate solution of the finite linear system.
That serial run takes 255 seconds, including a redundant final operator
evaluation removed in the subsequent implementation. Its checkpoint is
5.6 MiB. Saved artifacts are `data/computed/acb_refinement_4096.*`.

At n=8192, all sixteen columns converge with one factorization and two
corrections. Four independent workers reduce each residual evaluation to
38–44 seconds; the entire run, including assembly, factorization, larger
quadrature, and side checks, takes 246 seconds. The checkpoint is 10.7 MiB.
The 24,576-node independent quadrature uses a different phase offset.

| Diagnostic (maximum over columns where applicable) | n=4096 | n=8192 |
|---|---:|---:|
| Stabilized linear relative residual | 3.48e-41 | 1.54e-41 |
| Original finite Cauchy relative defect | 1.99e-6 | 5.69e-12 |
| Larger quadrature relative defect | 1.86e-6 | 5.86e-12 |
| All 275 side transformations, relative defect | 1.87e-4 | 1.42e-9 |
| Normalized first-64-jet imaginary relative norm | 4.64e-4 | 1.32e-11 |

These ratios use column infinity norms, whereas earlier script 70 reports
column Euclidean norms and may use different basis choices. Do not compare
the two sets of side residuals as if they were the same diagnostic.
Normalized jets change by relative 5.13e-4 from n=4096 to n=8192. Together
with the independent side checks, this supports improvement with increasing
truncation, without supplying a rigorous error bound. It does **not**
establish 40 accurate decimal digits of differentials: that number refers
only to the finite linear residual. Nor does the n=8192 checkpoint supersede
the larger n=10240/12288 double runs as the best analytic approximation
merely because its coefficients use arbitrary precision.

Reloading the n=8192 native checkpoint and recomputing its gauge agrees
with the 50-digit jets in its JSON to relative 1.28e-50, consistent with
decimal serialization. Against the earlier double n=8192 and n=10240
banks, the first-64 normalized jets differ by 6.72e-12 and 4.85e-10,
respectively. Those comparisons use D46's normalization at 70 working
digits on the stored inputs; they do not add accuracy to a double bank.
They are saved in `data/computed/acb_gauge_comparison.json` and support
the interpretation that truncation still dominates the present results.

Artifacts are `data/computed/acb_refinement_8192.{json,out,acb}`. The current
native source hash begins `ac1826c0`; n=64/4096 were computed before the
column-worker optimization, with hash beginning `3be6c42f`. A subsequent
n=64 threaded replay reproduces the same residuals and independent audits.
All 42 repository tests pass; Python compilation and `git diff --check`
also pass. No remote job was started or changed during D49.

Script 79 writes a JSON report, a matching `.out`, and an exact FLINT
`.acb` checkpoint. The checkpoint retains arbitrary-precision values;
it is not a complex128 NPZ. The report records all sixteen columns when
requested, per-step residual and arithmetic-radius diagnostics, timings,
source/seed hashes, unused quadrature, and every nonrotational side action.
For sixteen columns it also computes D46's first-64-jet gauge at arbitrary
precision, retaining the complex values for comparisons.

## Reproduction and interpretation

From the repository root, with a C compiler, `pkg-config`, and FLINT
development files available in the Sage environment:

```sh
OPENBLAS_NUM_THREADS=4 sage -python -m unittest discover -s dembele/tests -v
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/79_acb_refinement.py \
  --n 64 --columns 2 --output /private/tmp/acb_refinement_64.json
```

Choose a new output stem for each run; the script refuses to overwrite
reports or checkpoints. Increase `--n` and use `--columns 16` for full-space
experiments. `--comparison` accepts an earlier sixteen-column script 79
report and compares the normalized jets. The default independent Cauchy
test increases the sample count from 2n to 3n and changes the phase offset
from 0.37 to 0.19. The all-side test uses 275 transformations at points
independent of either quadrature, with native high-precision evaluation.

A tiny stabilized residual alone is not a basis-error bound. In particular,
M X = B allows (I-A)X = B(I-B*X), which need not be zero for a finite
truncation. Increasing working precision cannot remove this defect.
Independent enlargement of the coefficient count and quadrature, and
eventually rigorous geometric and truncation estimates, must precede
validated arithmetic recognition. No exact curve equation, Jacobian
torsion, or defining polynomial for Dembélé's field is obtained here.

The next practical experiment is to apply this same native solver at
n=12288 and compare its normalized jets with n=8192 and the completed
Châtelet double run. Dense LU and O(mn) polynomial evaluation remain the
scaling costs. Beyond that, justified finite-polynomial tail shortcuts,
multiple expansion centers, or a structured correction solve may be more
useful than simply increasing a dense matrix. None is implemented or
assumed valid by this result.
