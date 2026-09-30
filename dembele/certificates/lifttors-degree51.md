# Degree-51 scaling and precision-reduction correction (D66)

Date: 2026-09-17. This continues D65's explicitly bounded genus-16
control at p=97, residue degree 51 and precision exponent 4. The
2 GB PARI stack cap and 900-second per-process timeout are unchanged.
All D63–D65 source files, builds and recorded computational results
are preserved and checked by digest. The pinned checkout is untouched.

Subsequent work: [D67's allocation audit](lifttors-allocation.md)
completes the proposed measurement and selects two workspace-cleanup
changes to test. The D66 build and results below remain preserved.

**Result:** the unchanged D65 library completes the degree-51 control
in 439.776 seconds, including a 364.194-second lift and independent
comparison with the exact branch divisor. A separate source audit
finds an upstream precision-reduction bug in auxiliary evaluation
tables. The local correction preserves their embedding structure and
passes independent reduction and projective-evaluation checks. The
corrected large control also passes, in 440.569 seconds overall.

The collected report is
[`lifttors_degree51.json`](../data/computed/lifttors_degree51.json).
This is a known-curve backend calibration. It supplies neither target
sections nor target torsion, and no genus-64/degree-51 job is run.

## The original bounded experiment

Script 107's optional `genus16_a51` job uses y^2=x^33-x and the exact
nonzero 2-torsion class [(0,0)-(1,0)]. It initializes d0=33 with 204
evaluation points and section dimensions 18/51/84. The complete
control verifies the initial doubling, equality of the lifted point
with the independently supplied divisor, and annihilation by 2.

| Unchanged D65 build | a=2, saved D65 | a=51, D66 |
|---|---:|---:|
| Evaluation points | 166 | 204 |
| Jacobian object-tree bytes | 6,058,784 | 120,428,336 |
| Lift, seconds | 10.070 | 364.194 |
| Whole process, seconds | 12.401 | 439.776 |

At degree 51, initialization takes 6.380 s, the initial doubling and
zero check 20.008 s, and final lift checks 25.248 s. Whole-process time
also includes constructing the known point and checking nonvanishing.
The lift is about 36.2 times the saved degree-two timing, with a
different evaluation count. This is a single local comparison, not
a pure field-degree multiplier or a genus-64 runtime forecast.

Both derivative systems have 2,160 equations, 67 columns, rank 33
and nullity 34. All 18 blocks are scanned and replayed in each solve.

| Object or checkpoint | First precision step | Second precision step |
|---|---:|---:|
| S,H cache bytes | 22,280,904 | 22,341,016 |
| Largest equation block bytes | 13,280,240 | 13,315,080 |
| Selected-row bytes | 3,652,536 | 3,662,416 |
| Kernel bytes | 974,528 | 1,887,344 |
| Internal kernel stack checkpoint bytes | 47,978,040 | 49,157,744 |
| Kernel solve and replay, seconds | 20.188 | 20.065 |

The kernel stages account for 40.253 s, about 11% of the lift. Their
checkpoints exclude caller objects and caches. Other operations grow
the PARI stack to the 2 GB cap. No peak RSS was measured.

## An independent correctness issue in PicRed

In the pinned `rr.c`, `RRspaceEval` returns a **vector of matrices**,
one matrix per embedding of an auxiliary divisor's field. `RREvalInit`
stores these vectors in J[13][1] and J[13][2], and `RREval` consumes
that nested structure. However, the pinned `PicRed` passes each entire
vector to the matrix-only `FpXM_red`. That routine treats a matrix's
columns as scalar entries and produces an object with the wrong type
and incorrect contents.

Script 110 reproduces the discrepancy on the saved Q8 Jacobian at
precision exponents 1, 2, 8, 32 and 64. Both auxiliary vectors are
changed into `t_MAT` objects and disagree with independent GP modular
reduction: ten table failures. The main section and equation matrices
reduce correctly. The script's PASS marker means that the audit
completed; its result explicitly records the backend defect. It does
not call the evaluator on malformed data.

The earlier lifting checks remain valid within their stated scope.
The affected auxiliary fields are not read by those group/lifting
operations; Q8's earlier evaluation uses the unreduced full-precision
Jacobian. Those controls did not assert that evaluation on a reduced
Jacobian was correct. They therefore missed this separate defect.

`build_lifttors_reduction.py` creates `.build/lifttors_reduction` from
the verified D65 inputs and compiler command. Its only arithmetic
source change is to reduce each auxiliary embedding matrix separately,
preserving the outer vector and checking its expected types. It keeps
`PicRed_original` for the audit and retains the three lifting paths.
Neither the upstream checkout nor either earlier build is edited.

## Verification of the correction

Script 111 uses the saved full-precision Q8 Jacobian and four known
lifted torsion generators. At exponents 1, 2, 8, 32 and 64 it checks:

* All 25 embedding matrices against independent GP reduction, including
  shapes. The auxiliary embedding counts are 4 and 1.
* Unaffected Jacobian components against the original routine.
* Idempotence and all 15 pairs of nested precision reductions.
* Twenty actual point evaluations, comprising 80 projective coordinate
  vectors, against reduction of the full-precision evaluations. Each
  embedding pair is compared projectively with primitive coordinates
  and exact cross-products modulo the field polynomial and p^e.
* Two malformed table shapes, both rejected with the specific error.

The corrected build also passes all 60 three-way lift comparisons
and the full Q8 torsion, Frobenius, evaluation and polynomial recovery
control, again obtaining Q(i). Those comparisons share the corrected
reduction primitive; the independent GP and saved-point checks above
test that primitive itself. These are native GP controls, separate
from D63's still-latest full run of 111 Python/Sage regression tests.

The corrected genus-16/degree-51 result passes in its own log,
`lifttors_reduction_genus16_a51.out`: initialization 6.436 s, initial
doubling/zero check 20.620 s, lift 364.732 s, and final exact-divisor/
torsion checks 24.995 s. Whole-process time is 440.569 s. Its two
kernel stages take 20.011 and 20.731 s; the ranks, sizes and complete
replay counts match the baseline. The same cap and timeout apply.
These timings are not substituted for the unchanged-library result.
No genus-64 control has yet been rerun with the corrected library.
The complete D66 collector exits 0; no jobs remain running.

## Retained storage and the next gate

Script 109 rebuilds the same seeded genus-16 Jacobian, checks that its
size matches the scale control, and measures its correctly reduced
components. It verifies an irreducible residue polynomial of degree
51, four Frobenius cycles of length 51, and a section entry outside
both F_(97^3) and F_(97^17). The known torsion point itself is rational;
these field witnesses concern the arithmetic used by the backend.

The corrected Jacobian object trees occupy 120,112,192, 120,425,152
and 120,428,336 bytes at exponents 1, 2 and 4. Lowering precision from
97^4 to 97^2 scarcely changes the representation cost: both have
small integer coefficients but the same extension degree. At exponent
2, the principal matrix objects account for 120,337,360 bytes.

The collector projects those matrix components separately to genus
64 with 663 evaluation points, assuming full length-51 cycles and the
same known-curve basis structure. It accounts for the dense blocks,
constant columns, sparse identities, and matrix container sizes, using
each observed component's entry costs. The model exactly reproduces
the genus-16 component sizes and projects **1,472,765,199 bytes** for
the genus-64 principal matrices at exponent 2. This is a conditional
object-tree estimate, not a measured peak, a stack lower bound, or a
prediction for the actual Y. It does not account for shared storage.

The source retains a reduced J2 during the first lifting step, then
forms GWV and the Schur data. At the projected dimensions, GWV alone
has 663*390=258,570 entries, before Schur matrices and temporaries.
This identifies caller allocations to measure; it does not prove
that a full genus-64/degree-51 run must overflow.

**Decision:** do not launch genus 64 at degree 51 or raise the cap.
The next bounded backend task is an allocation audit of the reduced
Jacobian, GWV/Schur setup and group operations on the corrected
genus-16/degree-51 control. Attach stack checkpoints to those existing
stages before choosing an adaptation. More kernel tuning has little
justification when its solves occupy only about 11% of the measured
lift. No production-precision commitment is made.

The principal mathematical gap is unchanged: arithmetic sections
and their compatible p-adic lifting mechanism for the actual Y still
need construction. See the [section interface](arithmetic-section-interface.md).
The descent qualifications remain in force; repeated CM scans stay
paused. No target torsion or nonsolvable polynomial is obtained.

## Reproduction and attribution

From the repository root, preserving the recorded baseline builds:

```sh
python3 dembele/pari/107_lifttors_rows.py --only genus16_a51
python3 dembele/pari/build_lifttors_reduction.py
python3 dembele/pari/108_lifttors_degree51.py
```

The last command runs the audit, reduction/evaluation validation,
storage diagnostic, three-way comparisons, Q8 recovery and corrected
scale control. `--collect` checks existing logs and provenance without
rerunning; `--only` selects jobs without issuing a full report. Each
process has the same 2 GB stack cap and 900-second timeout. The parser
requires one data record and a PASS marker and rejects GP errors;
normal stack-growth warnings are allowed.

Mascot's pinned [PicRed implementation](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/pic.c),
[evaluation implementation](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/rr.c)
and [matrix reduction](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/linalg.c)
are the inspected sources. The shape correction, regression controls
and conditional storage projection are local work. PARI's
[object-size definition](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Conversions_and_similar_elementary_functions_or_commands.html#sizebyte)
governs the storage measurements. No new geometric or descent theorem
is invoked. No remote job, external message, commit or cleanup occurs.
