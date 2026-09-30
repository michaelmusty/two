# Actual torsion backend and its current scaling limit (D62)

Date: 2026-09-16. This implements D61's proposed backend check, using
the user's Q8 curve as an independent known answer.

**D63 update:** the [memory audit and repair](lifttors-memory.md) resolves
the two measured lifting allocations. The same genus-64 control now
passes with the original 2 GB stack cap. This report retains the D62
observations; current build/runner defaults include the D63 adaptations.

**Result:** Mascot's actual Makdisi implementation now runs locally.
On the known genus-2 curve it constructs the full 2-torsion over F49,
lifts it to precision 7^64, evaluates it and recovers a separating
degree-15 polynomial whose splitting field is exactly Q(i). A separate
genus-16 control passes. A genus-64 control completes initialization and
doubling but fails during lifting at a 2 GB PARI stack limit.
The backend is therefore exercised, but is not yet demonstrated at the
target's scale. No target section, torsion point or polynomial is obtained.

## 1. Source and local build

The source is [Nicolas Mascot's LiftTors](https://github.com/nmascot/LiftTors),
pinned at `fd6403caf7147b21b67dcb17dbedccea762d6262`, with PARI 2.17.1.
The arithmetic/lifting method is described in
[Mascot, *Hensel-lifting torsion points on Jacobians and Galois representations*](https://arxiv.org/abs/1808.03939).
This is the actual section-space divisor representation and Hensel lift,
not the specialized hyperelliptic group law used by D51's Magma control.
Hyperelliptic formulas supply known arithmetic sections for the controls.

`pari/build_lifttors.py` builds one shared library, since the upstream
separate-library loader has unresolved cross-library symbols on this Mac.
It checks the pinned revision and that the upstream tracked files are
unmodified. There is no system installation. The upstream checkout is
ignored by git; the build recipe, source hashes and adaptation are saved.
No explicit license file was found in the downloaded revision; the lock
file records that fact rather than assigning a license.

The first complete genus-2 run used the original C algorithms, simply
linked into one library. The default build subsequently adds the exact
batched validator described below. `--upstream` builds the unadapted
version. The JSON distinguishes the untouched checkout from the
adapted compiled copy.

## 2. End-to-end Q8 control

The input is y^2=16*x^5-x, already independently checked in
`magma/82_belyi_torsion_control.m`. Its full 2-torsion field is Q(i).
To supply a generic evaluation map, script 100 uses the birational model

    v^2 = 15*u^6+79*u^5+160*u^4+160*u^3+80*u^2+16*u,
    x = 1+1/u, v = u^3*y.

The auxiliary points are (1,sqrt(510)) and (2,16*sqrt(30)), represented
in the quartic field with generator sqrt(510)+sqrt(30). All embeddings
of that auxiliary field occur in the unramified quadratic extension of
Q7. The evaluation routine combines the conjugate auxiliary data to
obtain rational functions. These auxiliary fields are not the resulting
torsion field.

The initial branch-point choice stalled in an evaluation-space dimension
search and was interrupted. Replacing those auxiliary points resolved
the genericity failure; no increase of the analytic CM bank was involved.
The upstream high-level probe increased p-adic precision from 7^32 to
7^64 to recognize a separating polynomial. The reproducible control uses
the fixed final precision, with no unbounded precision loop.

Script 100 checks:

* The coordinate change and auxiliary points exactly, the unchanged
  Euler factor, and #J(F49)=4096 against the independent Magma result.
* A Makdisi model of degree d0=6, 32 evaluation points, and section
  dimensions 5,11,17 for L, L^2, L^3.
* Four independent torsion generators, including exhaustive comparison
  of all sixteen sums over the residue field.
* Membership, reduction, [2]P=0 and Frobenius compatibility of the four
  lifted generators modulo 7^64.
* Frobenius order two, rank(Frob-1)=1 and eight fixed points including
  zero; these agree with Magma without requiring the same basis.
* Evaluation on eleven nonzero Frobenius orbits, fifteen distinct values,
  a squarefree degree-15 rational polynomial, and its agreement with
  every computed value modulo 7^64.

The rational polynomial factors into seven linear and four quadratic
factors. Every quadratic has negative-square discriminant, so its
splitting field is exactly Q(i). This is an independent exact check of
the recovered field. Coefficient recognition itself remains a p-adic
recognition step; we do not claim an a priori coefficient-height theorem
or an independent symbolic formula for every evaluation value.

After initialization, the script removes the equation, symbolic section
bases and list of curve coordinates from the Jacobian object. Group
operations, lifting and evaluation still work using the arithmetic
evaluation matrices, Frobenius and auxiliary evaluation spaces. This
tests the equationless interface; it does not manufacture those matrices
for an unknown curve.

## 3. A real memory issue, and a limited repair

The original exact validator `DivSub_dimval` stacks one large block of
equations for every basis vector. At genus 64 its membership diagnostic
overflows a 2 GB PARI stack before the intended group/lifting benchmark.
This is a matrix-allocation problem observed in the actual backend.

`pari/lifttors_bounded.c` changes only this validation criterion. It
selects a full independent row set modulo p, retaining those rows with
their original coefficients modulo p^e. It lifts the kernel of that
row set, then checks **all** the original equations block by block
modulo p^e. It omits no equations and uses no probabilistic acceptance.
The upstream routine remains callable for comparison.

Why this is the same criterion: an independent row set modulo p has a
unit pivot minor and a free, normalized kernel over Zq/p^e. The full
matrix has the requested kernel dimension modulo p exactly when this
row set does. At precision p^k, its remaining rows belong to the span
of the selected rows exactly when they annihilate that normalized
kernel modulo p^k. Testing the minimum valuation of all residuals is
therefore the same rank/valuation test, regardless of the selected row
basis. The temporary matrix need only hold a bounded number of blocks.

Script 102 compares both implementations in 70 exact cases. These
include zero and nonzero torsion, equality between different divisor
representatives, incorrect requested dimensions, and deliberately
modified entries with residual valuations 0 through 5. All agree.
The complete Q8 pipeline was rerun successfully with the adaptation.

This repair reduces peak validator allocation; it does not make the
general membership diagnostic inexpensive. The larger benchmark starts
with a point whose membership follows from an explicit exact
Riemann--Roch basis, and verifies its lift against that known point.
It does not time the generic membership diagnostic as a group operation.

## 4. Larger controls and the stopping point

Script 101 uses the known curve y^2=x^(2g+1)-x at p=97, residue degree
two, and precision 97^4. It takes D0=(2g+1)*infinity. The supplied
nonzero 2-torsion class is [(0,0)-(1,0)], represented by the exact space

    L((2g+3)*infinity-(0,0)-(1,0))
      = < x(x-1), x^2(x-1), ..., x^g(x-1), y, x*y >.

Thus the intended lift has an independent exact answer. All actual
addition and lifting calls use Makdisi arithmetic, not a hyperelliptic
shortcut. The repeated auxiliary space passed to the initializer is
unused for evaluation in these scaling controls.

| Control | Observed result |
|---|---|
| Genus 2, a=2, e=64 | Initialization 0.018 s; basis 0.731 s; four lifts 0.875 s; span/evaluation 0.567 s |
| Genus 16, a=2, e=4 | 166 points, dimensions 18/51/84; initialization 0.186 s; doubling and zero check 0.665 s; one lift 10.184 s; lift checks 0.829 s |
| Genus 64, a=2, e=4 | Initialization and doubling/zero check complete; `PicLiftTors` exceeds stack limit 2,000,011,264 bytes; no completed lift or timing claimed |

Times are single-thread local observations, with verification costs
separated where recorded. They are not predictions for Y. In particular,
the candidate norm-97 target Frobenius order is 51, not two; neither
that extension degree, production precision nor 65,535 target vectors
has been benchmarked. The auxiliary evaluation points are also unusually
explicit in these controls.

**Stopping rule:** do not expand this into a large arithmetic-model or
precision run on the strength of the genus-2 success. The next backend
task is to inspect the allocation in `PicLiftTors`, make a justified
bounded-memory change or select a supported resource budget, and rerun
the same genus-64 known-answer control. Merely raising the stack limit
has not been adopted as the solution. The original source's kernels and
lifting algebra remain available for exact comparisons.

## 5. Reproduction and artifacts

```sh
python3 dembele/pari/build_lifttors.py
python3 dembele/pari/run_lifttors_controls.py
```

At D62 the runner executed scripts 100, 102 and the genus-16/genus-64 versions
of 101, with a per-process timeout. It checks explicit PASS markers and
rejects GP errors even when GP exits with code zero. It saves
`data/computed/lifttors_controls.json` and individual logs. The
recorded D62 genus-64 stack failure made the runner exit **1**, deliberately;
those logs are now retained with `_d62` suffixes. D63 adds scripts 103–104
and its passing larger control; the current runner exits **0**.
`--collect` collects existing logs without repeating the arithmetic.
The binary Q8 checkpoint contains section matrices and lifted points;
its reader handles GP's append-only binary records.

The existing Python/Sage regression suite passes all 111 tests, saved in
`data/computed/d62_tests_20260916.out`. The 70 GP comparisons are separate
from that count. The exact target-input choices and remaining arithmetic
gap are in [the section interface](arithmetic-section-interface.md).
