# D125: complete P=800 harmonic bank and candidate comparison

Completed 2026-09-28. All sixteen actual harmonic columns now reach
P=800, including their CM values. The complete candidate comparison and
all independent audits pass with no certified mismatch. The section
bounds improve, but remain insufficient for positive exact vanishing.
No candidate identification or target field polynomial is proved.
See the [source ledger](../data/computed/dyadic_precision800_sources_d125.json).
This continues the frozen [D124 pilot](dyadic-precision1600-d124.md) using
the original residual kernels.

## Construction and verification

Column 0 reuses the certified D123 P=800 state and separate extension-based
CM calculation. Source 505 refines columns 1..15 from their D122 P=400
states. The older metadata layout is supported explicitly. The weighted
storage, seed extension, low Schur inverse and shrinking active bands
follow D123/D124. The only arithmetic dispatch change is the small-product
backend controlled by sources 502--503.

Each column has twelve corrections, from weighted residual valuation
400 to 796 in increments of 33. Moments 0..32 retain full precision,
while moment k>32 retains precision P-k. Once only the low band remains,
GMP reconstructs all 174 states through moment 799 at uniform precision
800. A second GMP application checks every original equation, using a
backend separate from the adaptive production path. Exact masses,
556,800 old low coefficients and 1,113,600 extended old-precision
coefficients are checked for each new column.

Each sweep has three disjoint chunks of 58 states. There are seventeen
sweeps and 81 state phases per new column. The coordinator records
individual receipts, payload hashes, peak memory and elapsed times. It
resumes only successful receipts with the same command and source/log
hashes, refusing incomplete files. At most three workers run; each
mathematical phase retains the 180-second private-process-group cap,
assertions and one BLAS thread. Successful sources are immutable.

Source 506 computes all seventeen CM charts directly from the weighted
state. It normalizes the composition of each CM map with both original
child maps, checks the normalization/determinant equations with separate
integer quotient arithmetic, and verifies that c and determinant remain
pi-divisible. D124's proof then bounds every positive input column k
by pi^k, so P input moments suffice for all outputs. No 3P extension is
needed for these fifteen columns. All 108,800 old CM scalars and 68 old
coarse values overlap for each column. The new moments run through
1599, and the coarse beta-errors are [1632,1648,1632,1664].

Source 507 assembles sixteen columns only after their full residuals,
metadata and hashes have passed. The complete bank contains 17,817,600
state scalar coefficients, 3,481,600 CM scalar coefficients and 1088
coarse values. All sixteen columns and these complete counts are verified.

## Frame, quadrics and independent arithmetic

Source 508 raises the ball arithmetic's internal beta precision to 2048
and repeats its multiplication, scaling, inversion and unresolved-division
controls. Source 509 uses the actual differential bank and the frozen
algebraic CM values at beta precision 21168 to recover the residue frame.
It compares all 256 change-of-basis entries and all 1088 differential-jet
values with the P=400 result. Candidate equations enter only source 510,
which evaluates all 91 quadrics at all 17 CM points through coarse order
3 and records any certified mismatch as a mathematical result.

Source 511 imports no production arithmetic. For each new column it
checks all old overlaps, saved full residuals, masses, complete coverage
of seventeen sweeps, 348 child-column divisibility conditions, sampled
original and high-seed recurrences, all thirteen weighted checkpoints
and their error bounds, all 68 coarse values through a different series
formula, and sampled CM recurrences. Column 0's D123 audits remain bound.

Source 512 independently checks assembly of all 1088 values, bounds the
frame change via its residual and the inherited inverse norm, and tests
all 6188 quadric coefficients using gradients and polar forms in an
integer quotient with absolute error bounds. It also recomputes the
anchor-dependent thresholds using a separate rational enclosure of log 2.
These finite calculations do not machine-formalize the geometric proof.

## Results and measured costs

All **6188 quadric coefficients**, including **4641 positive-order
coefficients**, contain zero. No mismatch is certified. The separate
integer-quotient audit reproduces all 1088 actual jets and every quadric
coefficient, checks the frame residual bounds and the inherited inverse
norm, and independently verifies the sufficient thresholds.

| Order | Nonanchor lower bound | Anchor lower bound | Sufficient nonanchor bound | Gap |
|---|---:|---:|---:|---:|
| 1 | 4994 | 4776 | 25255 | 20261 |
| 2 | 4945 | 4448 | 25369 | 20424 |
| 3 | 4928 | 4184 | 25476 | 20548 |

Each measured section bound rises by 800 beta-digits compared with D122.
The stronger anchor lowers each sufficient nonanchor threshold by 50.
The global height budget itself is unchanged. The W Gaussian remains
certified nonzero at valuation 1024, now with error 2025 and relative
precision 1001; it has not been inverted. The minimum change-of-basis
entry error is 1336, and the relation error is 1301.

All fifteen new column audits pass. They check 2400 sampled original
recurrence scalars, 360 high-seed scalars, 1080 CM recurrence scalars,
all 1020 new coarse values, all 195 weighted checkpoints (217,152,000
state scalars and 55,436,400 scaled residual scalars), every old overlap
and complete coverage of 255 sweeps. The inherited column-zero audits
supply the other 68 independently checked coarse values. The full
original residual checks use the older GMP polynomial backend; the
additional integer-quotient recurrence checks are sampled.

The fifteen state-column coordinator durations total **5409.946 seconds
(90.166 minutes)**. Their CM phases total **196.843 seconds**. Each new
column has 81 state jobs plus one CM job. The retained state checkpoints
total **3,656,839,680 bytes**, excluding CM and reused factor files.
Maximum measured single-process resident memory is **811,401,216 bytes**;
the aggregate of concurrent processes was not measured.

All **1250 input jobs pass**, with no failed mathematical attempt. The
longest job takes **69.292 seconds**, within the unchanged 180-second cap.
Summed job durations are 11128.152 seconds, including overlapping jobs;
this is neither elapsed time nor measured CPU time. Column audits take
50.367--51.004 seconds each, and the independent comparison takes 19.448
seconds. A reconstruction batch varied up to 63.741 seconds, so the
initial columns alone are not used to forecast later cost. These are
measurements of this complete P=800 run, not a target-size solve.


## Interpretation and continuation

Finite balls containing zero do not prove exact positive quadric
vanishing. Higher intrinsic jets still require the preceding exact zeros.
The global arithmetic height budget, original residual kernels,
nonhyperelliptic genus-16 base, marked X40/Y64 covers and genus-64
section/degree-51 torsion construction remain the same. The global F256
action and final invariant are still required for the original field.
W's Gaussian is not inverted. All resource pauses and earlier freezes
remain in force. No correspondence.

The complete P=800 falsification check supports retaining the candidate
and the integral-section method. It does not close the exactness gap.
The next bounded task is a selective-read control at the already
certified P=1600: check every weighted projection against the frozen
uniform state and selected full original GMP equations, measuring peak
memory without decoding the entire bank. Then implement and control a
bounded rolling scratch protocol, and profile factor decoding/solves
and map reuse before choosing a larger full-bank refinement. Source 514
is next unused; no D126 driver has been written. The conditional P=10552
design remains unchanged, subject to its zero-containment and other
stated hypotheses.

The eventual precision target also has an I/O and retention gate. D120's
exact packed-size calculation gives 2,423,583,360 bytes for one uniform
P=10552 state column, before Python objects or temporary arrays. The
current driver decodes all 174 input states for every chunk and retains
every correction checkpoint. Its success at P=800/1600 does not establish
an acceptable target-memory or target-disk bound. Future target work must
cost selective state reads, reuse of decoded low factors and prepared
maps across columns, and a checkpoint protocol whose storage bound is
explicit. Existing frozen artifacts remain preserved. No target-size
full solve is claimed affordable from these pilots.

The final moment certificate is independent of the iteration history.
Fix the exact masses and reduce the original operator to moments k<P.
The omitted input columns vanish modulo pi^P, while every positive
input column is divisible by pi. If v has the certified original
residual zero and the prescribed masses, its difference from the actual
moments satisfies e=T_+ e modulo pi^P. Iterating this identity P times
gives e=0 modulo pi^P. Thus the original residual, exact masses,
transport/truncation certificate and final state determine correctness
without the seed or intermediate correction payloads. A future rolling
scratch protocol can preserve resumability with the latest complete
checkpoint and permanent receipts, while retaining the final verified
state and its certificate. This is a prospective change: no existing
frozen artifact is deleted, and the new protocol still needs implementation
and controls. Metadata hashes alone are not being substituted for the
final original-equation verification.

## Provenance and resume

Both coordinators and all mathematical workers have returned. The input
jobs comprise 1215 state phases, fifteen CM phases, one ball-control job,
one bank assembly, one frame, one quadric comparison, fifteen column
audits and one independent global comparison. Source 513 verifies their
coverage, hashes, receipts and all 3535 inherited D124 hashes, then creates
a fixed review manifest. Run creation and its `--check` replay through
the persistent wrapper with fresh receipt names.

Freeze successful 505--512, both coordinators and their artifacts. After
513 passes, freeze it, this report, the ledger and its fixed manifest as
well. The completion coordinator's record predates final provenance
review; its historical pending-review flag is not the final review status.
No existing frozen artifact has been changed or deleted. On interruption,
inspect receipts and partial outputs before resuming; completed phases
must not be rerun.
