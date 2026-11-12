# D156: storage plan and prepared column-2 P6400 timing pilot

Date: 2026-10-12. Continuation from the completed D155 handoff.

**Result:** the next integrated measurement is prepared for column 2,
from its certified P3200 seed to P6400. Its exact configuration, direct
input bridge, independent audit plan, reviewer and bounded admission are
ready. The empty-store create preflight passed; all 174 row commitments
remain empty. No new harmonic moments or production schedule have run.

The column-cycle model is **9.55–11.98 active hours**. Including the
retained provenance and common-comparison allowances gives **10.79–13.79
active hours**. These are unmeasured planning scenarios. The pilot requires
a fresh observation of at least **12 GiB free**, including the unchanged
10 GiB reserve. It is a single-column measurement, with reassessment
required after its audits and reviews.

The larger bank remains paused. The refreshed workspace observation is
**44.63 GiB free**, against **71.02 GiB** in the remaining-route model.
The concrete full-bank gate is **72 GiB free** on the workspace volume,
requiring **27.37 GiB more** than observed. This preparation supplies a
storage plan; it does not supply the missing capacity.

The [storage and timing packet](../data/computed/dyadic_storage_timing_plan_d156.json),
[setup](../data/computed/dyadic_higher_pilot_setup_d156.json),
[controls](../data/computed/dyadic_higher_pilot_controls_d156.json),
[fixed admission](../data/computed/dyadic_higher_pilot_preparation_review_d156.json),
[source ledger](../data/computed/dyadic_higher_pilot_preparation_sources_d156.json)
and [completion record](../data/computed/dyadic_higher_pilot_preparation_completion_d156.json)
record the evidence and exact scope.

## 1. Concrete storage decision

[Source 645](../pari/645_dyadic_storage_timing_plan.py) reconstructs the
remaining schedule from [D152](precision-route-cost-d152.md), debiting only
the column completed in [D154](dyadic-pilot-timing-d154.md). It retains
every frozen input, output, failed snapshot and receipt. It assumes no
deletion, relocation, compression, cloning credit or remote storage.

The remaining 1,047,369 column jobs require 65,170,102,688 bytes of modeled
retained allocation. The single largest additional working allowance is
349,629,168 bytes. Adding the 10 GiB reserve gives exactly
**76,257,150,096 bytes**, reproducing D154's remaining-space requirement.
The working allowance is a maximum across sequential columns, not a sum
of simultaneous stores. The retained allowances accumulate across every
column and stage.

| Remaining stage | Columns | Jobs per column | Retained allowance per column | Logical working-store bound |
| --- | ---: | ---: | ---: | ---: |
| P1600 to P3200 | 14 | 12,570 | 483,532,544 bytes | 304,049,792 bytes |
| P3200 to P6400 | 15 | 24,579 | 1,254,739,040 bytes | 973,167,872 bytes |
| P6400 to P10480 | 16 | 31,419 | 2,473,722,592 bytes | 2,005,700,320 bytes |

The inventory reproduces the frozen scheduler's complete phase counts at
all three precisions. A separate check reconstructs packed byte widths,
retained metadata, job counts, accumulated storage and rounded gates.
These retained-allocation figures are planning allowances; the logical
per-store inventory is a separate 2 GiB limit.

The filesystem observation at **2026-10-12 16:54:08 UTC** records
47,923,200,000 available bytes. The model shortfall is 28,333,950,096 bytes
(26.39 GiB); the rounded 72 GiB gate shortfall is 29,386,211,328 bytes
(27.37 GiB). `/Volumes` exposes only `Macintosh HD`, resolving to the
same filesystem device as the workspace. No separate volume is selected.
The observation is neither a reservation nor a statement about future
available capacity.

Use the current workspace for the one admitted measurement, with a fresh
12 GiB free-space check immediately before launch. Preserve the full-bank
pause until the same volume has at least 72 GiB free, or a separately
reviewed destination and path-aware provenance plan supplies equivalent
capacity. Existing certificates contain absolute paths; blindly moving
their files is not such a plan. No frozen file may be reclaimed or moved
under this checkpoint.

For comparison, the cumulative storage scenarios through the remaining
P3200, P6400 and P10480 stages are 17,654,008,544, 36,677,588,624 and
76,257,150,096 free bytes, each including reserve and its largest active
allowance. Their apparent fit does not admit those banks or stages.
Capacity must be refreshed when making each later commitment.

## 2. Exact pilot and provenance

The [configuration](../data/computed/dyadic_staged_P6400_col02_config_d156.json)
sets P=6400, S=3200, column=2, digit width 200, state/CM chunk 1 and
right-hand-side chunk 3. The fresh owned store is
`dyadic_rowjournal_P6400_col02_d156_d132`; the production prefix is
`dyadic_staged_P6400_col02_d156`.

[Source 648](../pari/648_dyadic_higher_pilot_setup.py) builds the
[direct seed bridge](../data/computed/dyadic_higher_pilot_seed_bridge_d156.json)
from the completed D154 column catalogue and the D138 native dependency
catalogue. It binds the exact P3200 seal, packed state, lossless CM
interface, CM payload, transports, harmonic certificate and complete
source-554 Python/native closure. The engine's direct input lookup is
checked explicitly; an indirect provenance root is insufficient.

The [source-554 create preflight](../data/computed/dyadic_staged_P6400_col02_d156_create.json)
has already run and will be reused. It allocates a 449,407,200-byte
initial state payload without initializing any rows. The admission binds
the immutable INPUTS manifest and seed row hashes. Prospective mutable
pool files are not frozen as future data. Do not rerun setup or create.

There are **24,579 jobs** in the column cycle: 24,456 production phases,
97 metadata archives, 24 independent audits and two column reviews.
The completed create is included in that count; **24,578 remain**.
The logical working-store bound is **973,167,872 bytes**. The pilot's
modeled retained allowance plus active extra is 1,604,368,208 bytes;
including reserve gives 12,341,786,448 bytes. Rounding upward yields the
12 GiB launch gate. Keeping the already allocated create inside the
planning allowance is conservative.

## 3. Independent controls and audit scope

The former pilot reviewer accepted only the P3200 column-2 execution.
New [source 647](../pari/647_dyadic_higher_pilot_column_review.py) adds this
exact P6400 column-2 case, retaining the original receipt, store and
arithmetic-certificate checks. New
[source 646](../pari/646_dyadic_higher_pilot_independent.py) retains the
weighted and uniform seed arithmetic and labels the new execution D156.
Neither independent reviewer imports production arithmetic.

[Source 649](../pari/649_dyadic_higher_pilot_controls.py) checks:

- All five independent arithmetic phase types against completed P6400
  certificates and the complete known P6400 column against all 24,553
  production/archive receipts.
- Equality of ten independent arithmetic functions and five core reviewer
  functions with their frozen predecessors; all 24,456 new schedule
  specifications match the separately written reviewer specification.
- Actual P3200 packed seed rows 0, 83 and 173 against the existing native
  reader; synthetic P6400 extensions exercise both old seed formats.
  Eight malformed overlap, flag, digest, length and high-bit cases fail.
- The inherited synthetic indexed-archive fixture, including rejection
  of the wrong archiver, and the frozen D139 interruption controls.
- Independent storage totals and rational timing sums, including the
  exact free-space boundary and rejection of one byte below the gate.

The [24-job independent plan](../data/computed/dyadic_higher_pilot_col02_audit_plan_d156.json)
checks all 4,454,400 old state scalars, 870,400 old CM scalars, 174 masses
and final residual rows, and 68 old coarse overlaps. Separate samples
check 72 original state and 72 original CM recurrence scalars and 96
Horner beta scalars. Those samples do not independently recompute the
complete new operator. Authenticated production jobs must certify all
8,908,800 new weighted-equation scalars and 1,740,800 CM scalars, with
coarse errors 12832, 12848, 12832 and 12864.

Synthetic control fixtures are not actual new harmonic values. No actual
precision is gained by preparation.

## 4. Timing experiment and resource limits

The two D152 per-column P6400 scenarios are retained unchanged:
34,364.671 and 43,133.740 active seconds. D154's P3200 speed ratio is not
applied to P6400. For conservative shared planning overhead, the pilot
retains D139's larger one-target-column provenance allowances of
4,052.731/6,079.096 seconds and D152's 424.369-second common comparison
allowance. This yields 10.79–13.79 active hours overall. Shared allowances
are not measurements or extra scheduled harmonic columns.

Record the production and audit coordinators' monotonic elapsed times,
both column-review times, summed worker/archive times, phase timing
distributions, callback overhead, maximum RSS and largest observed store.
Charge the previously completed create separately when measuring the
column cycle. Preserve filesystem wall spans and host sleep observations
as separate evidence. Reassess after all audits and both reviews; do not
automatically launch another column or stage.

This experiment measures P3200-to-P6400 with the indexed coordinator.
It does not measure the P10480 stage. Until actual measurements justify
an update, D154's remaining **20.2–28.5 active-day** scenarios remain
unchanged. There is no field-polynomial completion estimate.

All mathematical, control, audit and review jobs retain the **180-second
private-process-group timeout**, at most **three mathematical workers**,
**2 GiB per worker/store** and **6 GiB aggregate**. Preparation jobs are
sequential. RSS admission uses measured peaks, not an OS-enforced hard RAM
limit. Source 650 checks the fresh launch-space boundary and thread
environment. No permanent power settings are changed, and no remote job
or correspondence is part of this preparation.

## 5. Prepared launch sequence

[Source 650](../pari/650_dyadic_higher_pilot_preparation_review.py) traverses
the D155 proof review and the complete inherited catalogues, checks all
new controls, and admits only the hash-bound configuration. Its fixed
`--check` receipt is the frozen D139 coordinator's admission gate.
The preparation does not start that coordinator.

After a separate decision to run this one measurement, use the sequence
below from the repository root. Run each command only after its predecessor
passes. Use a fresh launch-check receipt stem if that name already exists.
The space check starts no coordinator and reserves no capacity.

```sh
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

python3 dembele/pari/run_dyadic_capped.py dembele/pari/650_dyadic_higher_pilot_preparation_review.py dyadic_higher_pilot_launchcheck_d156_attempt01 'PASS|650_DYADIC_HIGHER_PILOT_PREPARATION_REVIEW' --launch-check
python3 dembele/pari/run_d139_indexed_production.py --config dyadic_staged_P6400_col02_config_d156 --workers 3
python3 dembele/pari/run_d137_audits.py --plan dyadic_higher_pilot_col02_audit_plan_d156 --workers 3

python3 dembele/pari/run_dyadic_capped.py dembele/pari/647_dyadic_higher_pilot_column_review.py dyadic_higher_pilot_col02_review_d156_attempt01 'PASS|647_DYADIC_HIGHER_PILOT_COLUMN_REVIEW' --config dyadic_staged_P6400_col02_config_d156 --output dyadic_higher_pilot_col02_review_d156
python3 dembele/pari/run_dyadic_capped.py dembele/pari/647_dyadic_higher_pilot_column_review.py dyadic_higher_pilot_col02_review_d156_recheck01 'PASS|647_DYADIC_HIGHER_PILOT_COLUMN_REVIEW' --config dyadic_staged_P6400_col02_config_d156 --output dyadic_higher_pilot_col02_review_d156 --check
```

Keep only one production/audit coordinator active and count manual jobs
toward the same three-worker limit. Preserve failed attempts and inspect
them before resuming. Never recreate completed coordinator outputs.
The initial-only launch-space check deliberately rejects a partially
executed store; any interrupted production continuation needs an explicit
state inspection and fresh space observation under the same admission.

## 6. Mathematical status and checkpoint

[D155](proof-criterion-review-d155.md)'s P10480 criterion remains
conditional on actual certified error and zero-containment tests, with
exact order-one vanishing preceding order two. The full bank remains
P1600, column 0 P6400 and column 2 P3200. The relation-height upper remains
15237 versus the P1600 target 623. Positive exact vanishing, actual/candidate
identification, P32/B3, the upstairs cover and final field polynomial are
still open. D151's finite transfer search stays parked, and the spectral/
census, new-level, Hecke and cubic pauses persist.

Sources 645–650 and the successful bound preparation artifacts freeze
after admission. Source 651 is next unused. `650 --check` is the transitive
replay, with a fresh capped receipt stem; it does not recreate setup,
create, fixed review or completion. Entry-document hashes remain editable.
The completion step verifies the current artifact links in all seven entry
documents. This checkpoint prepares one measurement and leaves the
full-bank capacity shortfall unresolved.
