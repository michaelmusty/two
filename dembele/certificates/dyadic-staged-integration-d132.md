# D132: complete resumable staged driver and next-column admission

Date: 2026-09-28. This executes the driver integration following
[D131](dyadic-weighted-journal-d131.md).

**A complete known P=800 column passes through the new driver, including
all corrections, original weighted equations, CM moments and coarse
values. The same low-solve phases reach 1319 bits and match the complete
D130 reference.** The next admitted mathematical execution is one actual
P=6400 column from the certified P=3200 column. The full bank is not launched.

All 471 input jobs pass under the unchanged 180-second private-process-group
cap, assertions and one BLAS thread. At most three mathematical workers
run concurrently. Summed bounded-job durations are 1628.259 seconds;
the longest is 24.607 seconds. There are eight intentional interrupted
children, all inside passing controls, and no failed bounded jobs.

See the [ledger](../data/computed/dyadic_staged_integration_sources_d132.json),
[fixed review](../data/computed/dyadic_staged_integration_review_d132.json)
and [completion record](../data/computed/dyadic_staged_integration_completion_d132.json).
Sources 547--555 are new; earlier frozen sources and data remain unchanged.

## Complete arithmetic path

Source 547 extends the D131 row journal with reserved row pools and
resumable initialization. Source 548 separates seed extension, low-RHS
chunks, each exact residual/factor/verification digit, journal preparation,
original correction sweeps, final verification, CM publication and sealing.
Every arithmetic phase uses the unchanged capped wrapper. Source 549
executes a deterministic schedule, verifies passing receipts and preserves
completed work on restart. Partial row writes are never accepted without
their committed digests; a complete internal job record can regenerate a
missing external completion record.

The seed is passed to the original operator using its weighted residue
representative, with exact masses restored. Moment-k error at old precision
S has valuation at least S-k, while operator column k has valuation at
least k. The omitted k>=S tail has the same uniform error bound S.
The actual replay checks every old uniform overlap. Final verification
checks Q T(w)=w and every fixed mass; D130's T Q=T argument certifies the
uniform fixed point T(w) without retaining a new uniform payload.

The P=400-to-P=800 column-0 replay has 432 arithmetic/publication phases,
including twelve corrections after the seed solve. The seed deliberately
uses two 50-bit digits, testing the multi-stage path at actual harmonic
input. Every digit checks all 44,544 original low equations. At the end,
all 1,113,600 uniform outputs agree with D123, all 1,113,600 weighted
coordinates agree with their prescribed projection, and all 174 masses
pass. The final residual is zero. No candidate curve equations are inputs
to this refinement.

The CM stages calculate all 217,600 scalar moments in seventeen charts,
then all 68 coarse values of orders zero through three. Every moment
agrees with the corresponding reduction of the frozen D129 P=3200 CM
reference. Coarse errors are [1632,1648,1632,1664], and every value agrees
with the existing higher-precision reference to that error. These are
new computations of previously known data, not a precision increase.
D129 already used weighted input for CM; D132 integrates its publication
with the recoverable staged lifecycle.

The full smaller-column coordinator takes 705.765 seconds. Its maximum
measured successful-worker RSS is 97,714,176 bytes. Timing includes the
intentional interruptions and their recovery; it is not a forecast of
the target schedule.

## Interruption and archival evidence

Source 550 interrupts seven actual workers: after an initialized row
commits; after a low-RHS job commits internally but before its external
record; during low-answer publication; after an in-place state write;
after a residual-row write; after a coarse-value job commits; and after
sealing but before the final external record. Every interrupted child
exits without Python cleanup, inside its capped parent's process group.
The ordinary schedule resumes and reaches the complete reference result.

Long runs also accumulate metadata. Source 551 retires duplicate internal
job records only after checking identical external phase JSON, a passing
receipt, its driver and log hashes, and the log's metadata binding. A
durable archive intent precedes any removal. All external records remain
frozen. Arithmetic payloads, row manifests, low contexts and coarse records
are not removed by this operation.

The target low control interrupts archival after the first of three
duplicate records is removed. The intent and all external copies survive;
the next invocation completes removal. Seven archive barriers preserve
all 21 low-phase records outside the store. This is the eighth intentional
interrupted child. Source 553 integrates archival after complete sweep
barriers in the full schedule. Earlier frozen stores are never cleaned up.

These are process-interruption controls. Power loss, hardware faults and
filesystem failure are not certified. Ordinary arithmetic samples do not
constitute a second complete independent operator.

## Target low-solve integration

Source 552 initializes the same deterministic synthetic RHS used by D130.
Source 553 drives source 548 through seven separately capped stages at
200,400,600,800,1000,1200 and 1319 bits, with existing factors of at most
200 bits. Each stage forms the original sparse residual, checks exact
binary division, solves the correction and verifies every original low
equation before the next stage. Obsolete quotient and answer payloads
retire only after verification.

All 7,349,760 final answer bytes match D130. The low coordinator has
21 arithmetic phases, seven archive phases and one archive-interruption
control; it finishes in 288.818 seconds. The maximum measured successful
low-worker RSS is 122,978,304 bytes. No larger factor is built. This RHS
is synthetic; it does not increase harmonic precision.

Review 555 imports only the independent integer quotient for arithmetic.
It checks every retained weighted coordinate and CM coefficient, all
coarse reference congruences, current payload and row hashes, archive
copies, generation history, receipts and every inherited D131 hash.
Separate ordinary recurrences check 72 state scalars through degree 33,
72 CM scalars and 48 scalars in the final 1319-bit original low equations.
The sampled/full distinctions remain explicit.

## Complete file inventory and RAM admission

The lifecycle includes initialization, low RHS, previous answer, quotient,
new answer, row undo/redo copies, old and new residuals, verification,
CM output, metadata replacement, archive intent, history and crash states.
It uses one working store and retains the D131 64 MiB reserve in addition
to the actual low payloads. Dynamic store reservations enforce 2 GiB.

| Stage | Largest conservative working-store total | Margin below 2 GiB |
|---|---:|---:|
| P=400 to 800 | 100,749,888 bytes | 2,046,733,760 bytes |
| P=3200 to 6400 | 973,167,872 bytes | 1,174,315,776 bytes |
| P=6400 to 10552 | 2,046,552,040 bytes | 100,931,608 bytes |

The totals use exact payload lengths and conservative metadata allowances
for the specified schedule. They require archival after every completed
sweep. They account for one-state operator/RHS tasks, so the selected
three-state P=6400 RHS chunks use fewer job records. Existing frozen
factor files and earlier input stores remain outside this new working
namespace and are read with streaming hashes and bounded row/block reads.
Permanent phase JSON/logs/receipts are counted separately from scratch;
the complete long bank's retention and runtime must still be reassessed
from an actual new stage.

RAM has a separate admission policy: at most three mathematical workers,
each successful job's measured peak at most 2 GiB, and a conservative sum
of at most 6 GiB. This is a measured admission policy, not an OS-enforced
hard RAM limit or a proof of physical free memory. Process-table and
hardware-memory queries are unavailable in this sandbox. Interrupted-child
RSS was not separately recorded. The actual P=800 and low controls stay
well below the per-job threshold. A future timeout or excessive measured
peak stops admission and requires a smaller arithmetic job before resuming.
No resource cap has been raised.

## Next actual execution

Source 554 is the production form of 548. Review 555 checks that its
arithmetic code is unchanged: it only adds an explicit prior-review
selection and updates its identity/marker. This permits a later weighted
seed to be authenticated against its own completed review. Source 553
adds verified duplicate-metadata archival to the completed schedule.

After both fixed reviews pass, use the
[P=6400 configuration](../data/computed/dyadic_staged_P6400_col00_config_d133.json)
for column 0: the frozen D129 seed, 200-bit low-factor digits, one-state
operator tasks, three-state low-RHS tasks and one-chart CM tasks. Run
initialization to a planned coordinator pause, then resume from its saved
receipts to test that boundary on the actual new stage. Continue through
all 96 corrections, original weighted verification and CM publication,
with independent review before claiming P=6400. D132 admits this one
column; it does not admit the sixteen-column bank automatically.

The D132 controls leave the full bank at P=800, column 0 at P=3200 and
column 1 at P=1600. The 6188 actual quadric balls contain zero, with no
positive exact zero. D125 bounds/anchors, the uninverted W Gaussian and
successive-zero hypotheses remain unchanged. P=10552 is a conditional
sufficient design. Exact base identification and the original-kernel
field polynomial remain open.

The [arithmetic construction specification](arithmetic-construction-d130.md)
still requires marked P32/B3, the geometric double-cover character and
arithmetic twist, actual Y64 sections, combined genus64/degree51 torsion,
global F256 action and coefficient/kernel certification. D120 norm-97
separation remains settled. No new external theorem or fresh external
source verification is invoked by this implementation milestone.

Freeze 547--555, successful bound controls, the two sealed stores, their
histories and archive records, report, ledger and fixed review. Preserve
all prior freezes. No remote job, correspondence or frozen-data cleanup.
