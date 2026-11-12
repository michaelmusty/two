# D157: completed column-2 P6400 timing pilot

Date: 2026-10-13. Actual execution following the approved D156 preparation.

**Result:** the column-2 P3200-to-P6400 pilot has completed all production,
archives, independent audits, the corrected column review and its replay.
The successful column cycle measured **9.397 active hours**. The original
review failed on a stale checkpoint-label assertion; its receipt, log and
source snapshot remain preserved. No production or audit job was rerun.

The [timing packet](../data/computed/dyadic_higher_pilot_timing_d157.json),
[fixed review](../data/computed/dyadic_higher_pilot_timing_review_d157.json),
[completion record](../data/computed/dyadic_higher_pilot_timing_completion_d157.json)
and [source ledger](../data/computed/dyadic_higher_pilot_timing_sources_d157.json)
bind the measurements, repair, provenance and current checkpoint.

## Completed computation

The [D156 preparation](dyadic-higher-pilot-preparation-d156.md) admitted
only `dyadic_staged_P6400_col02_config_d156`. The fresh launch check passed
on October 12 at 17:19:01 UTC with 47,923,200,000 bytes free, above the
12 GiB gate. The existing create receipt was reused.

Production completed **24,456 phases and 97 archives**. All **24 independent
audits** passed. With the two successful column reviews, there are
**24,579 passing column jobs**, including the one inherited create;
24,578 passing column jobs are new in this continuation. No production
or audit attempt failed. The separate failed review is additional to
these successful-job counts.

The [revised column review](../data/computed/dyadic_higher_pilot_col02_review_r2_d157.json)
authenticates 8,908,800 full original weighted-equation scalar checks,
174 fixed masses, 1,740,800 CM scalars and 68 coarse values. Coarse error
exponents are **12832, 12848, 12832 and 12864**. The store is sealed and
the [lossless CM interface](../data/computed/dyadic_CM_P6400_col02_d156.json)
is published without a duplicate assembled binary.

The independent audits check all 4,454,400 old state scalar overlaps,
870,400 old CM overlaps, 174 masses and final residual rows, and 68 old
coarse overlaps. Original-recurrence samples cover 72 state and 72 CM
scalars; sampled integer-quotient Horner checks cover 96 beta scalars.
These samples do not independently recompute the complete new operators.
The full new equations are certified by the authenticated production jobs.

## Reviewer failure and bounded recovery

The durable supervisor stopped at the first column review, as designed.
Frozen source 647 incorrectly required the older execution label `D153`
on audit packets whose correct label is `D156`. Its D153-only branch also
omitted indexed receipt-inventory checks on the D156 path. The failed
attempt reached the audit-label assertion after reviewing production.

[Source 651](../pari/651_dyadic_higher_pilot_column_review_revision.py)
makes exactly two functional changes: it requires the configured execution
label and applies indexed-summary validation to both D153 and D156.
Only the descriptive docstring and pass markers change otherwise.
Production and auditor arithmetic are unchanged. Frozen source 647,
the D156 configuration and admission, and the failed snapshot are retained.
The new column result uses the fresh `dyadic_higher_pilot_col02_review_r2_d157`
stem; the original config's failed review output is deliberately absent.

[Source 652's controls](../data/computed/dyadic_higher_pilot_review_controls_d157.json)
verify that exact source difference, accept all 24 actual D156 audits,
and reject seven malformed in-memory fixtures: previous, unknown or
missing execution labels, an unsupported weighted seed, wrong indexed
summary milestone, unreconciled inventory and wrong receipt-lookup source.
They also exercise the actual indexed-summary guard on valid D156 and
D153 schemas. Real artifacts were not modified by these fixtures.

The [original failed receipt](../data/computed/dyadic_higher_pilot_col02_review_d156_attempt01.job.json)
records 26.704 seconds. The regression controls took 1.218 seconds.
The corrected full column review and replay passed in 33.697 and 12.302
seconds. The original supervisor status remains a stopped-after-failure
record; the D157 completion packet records the separate successful recovery.
The supervisor's temporary idle-sleep assertion ended with it, and no
permanent power setting changed. The owned coordinator locks were free
when the timing assessment checked them.

## Measured timing and resources

| Component | Seconds |
| --- | ---: |
| Production coordinator, including archives and scheduling | 33762.175 |
| Independent audit coordinator | 20.485 |
| Corrected column review | 33.697 |
| Column hash replay | 12.302 |
| Earlier create, separately charged | 0.348 |
| Successful column cycle | 33829.007 |
| Cycle plus failed review and regression controls | 33856.929 |

The successful cycle uses coordinator monotonic clocks and bounded review
receipts. It excludes preparation other than create, the separately
reported failed review and regression overhead, and final timing/provenance
assessment. Including that failed review and regression overhead gives
9.405 active hours. Summed production worker time is 81,144.013 seconds;
archives contribute 69.256 worker seconds and audits 59.356. Concurrent
worker sums are not elapsed column time. Per-phase timing statistics are
retained in the timing packet.

The supervisor observed production from **2026-10-12 17:21:19 UTC to
2026-10-13 05:44:26 UTC**, a 44,587.465-second wall span (12.385 hours).
Its monotonic span was 33,762.582 seconds, about 10,824.882 seconds shorter.
These are distinct clock observations. This checkpoint does not establish
the cause of the wall-clock gap and does not count it as active computation.
It also does not add the later idle interval before review recovery to
the active column cycle.

Maximum production concurrency was 3. Maximum production/audit RSS was
957,874,176 bytes; the conservative sum of concurrent production peaks
was 2,715,713,536 bytes. The largest observed store was 960,593,766 bytes,
below its proved 973,167,872-byte inventory bound. The longest successful
column job was the 33.697-second corrected review; the longest production
job was 29.166 seconds and the longest archive 2.000 seconds.

All mathematical, control, audit and review jobs retain the **180-second
private-process-group timeout**, at most **three mathematical workers**,
**2 GiB per worker/store** and **6 GiB aggregate**. RSS checks are measured
admission, not an OS-enforced hard RAM limit. Recovery and final assessment
run sequentially. No cap changed.

The dated allocation observation records 650,457,594 logical bytes in the
sealed store and 107,020,468 logical bytes in external successful-column
artifacts. Allocated amounts were 652,419,072 and 336,261,120 bytes,
respectively. Those categories exclude preparation controls, failed-review
recovery records and final closing artifacts. They do not predict APFS
sharing or future free space.

## Remaining runtime and storage

The [D156 timing plan](../data/computed/dyadic_storage_timing_plan_d156.json)
modeled a 9.55–11.98-hour column cycle, or 10.79–13.79 hours including
shared review/comparison allowances. The measured successful-cycle ratios
are 0.984 and 0.784 against those per-column scenarios. Shared allowances
remain separate; the larger totals were not per-column measurements.

The remaining route has **1,022,790 planned column jobs**: 14 P3200
columns, 14 P6400 columns and 16 P10480 columns. Applying D154's observed
P3200 cycle and this P6400 cycle only to their respective remaining
columns, while retaining the P10480 and shared-overhead scenarios from
the [D152 model](precision-route-cost-d152.md), gives:

| Remaining component | Active-hour scenario |
| --- | ---: |
| 14 P3200 columns, same cost as measured column 2 | 29.8 |
| 14 P6400 columns, same cost as measured column 2 | 131.6 |
| 16 P10480 columns, still unmeasured | 303.7–461.5 |
| Retained graph and comparison allowances | 8.6–12.8 |
| Total | **473.6–635.7** |

That is **19.7–26.5 active days**, a conditional scenario rather than a
deadline or bound. One measured column does not bound other columns.
P10480 remains the dominant unmeasured stage; this report does not apply
the P6400 speed ratio to it.

The completed pilot debits 1,254,739,040 bytes from the prior retained-data
allowance. Remaining planned free space is **75,002,411,056 bytes
(69.85 GiB)**, preserving the full 349,629,168-byte largest active-store
extra and the 10 GiB reserve. The rounded bank gate is **70 GiB**.
The October 13 12:56:44 UTC observation is **47,104,000,000 bytes
(43.87 GiB)** free, leaving a modeled shortfall of 25.98 GiB, or
**26.13 GiB to the rounded gate**. These are dated observations, not
reservations. All frozen files remain retained; no deletion, relocation
or separate storage destination is authorized by this checkpoint.

**Decision:** the single pilot is complete and the larger bank remains
paused. Further preparation should resolve the capacity gap and separately
review any P10480 timing experiment before a new launch. No new column,
P10480 stage or full bank is admitted here.

## Provenance and mathematical scope

[Source 654](../pari/654_dyadic_higher_pilot_timing_review.py) authenticates
the D156 admission, its inherited graph through D155 and D154, the new
P6400 catalogue, corrected-review controls, failed attempt, supervisor
records and durable production/audit transcripts. It independently
recomputes timing totals, phase statistics, repeat scenarios and the
remaining storage formula without importing source 653. The inherited
P3200 catalogue remains separately identified.

Once fixed review, replay and completion pass, the checkpoint ledger
contains **24,584 newly passing bounded jobs and one preserved failure**.
This includes 24,578 new successful column jobs plus launch check,
regression controls, timing assessment, two fixed reviews and completion.
The earlier create is inherited. Completion checks four current artifact
links in each of seven entry documents and the three owned coordinator
locks. The original supervisor is never restarted.

The actual complete sixteen-column bank remains **P1600**; columns **0
and 2 are P6400**. D155's [conditional proof criterion](proof-criterion-review-d155.md)
still requires future actual certified errors and exact successive
vanishing. No exact positive quadric vanishing, candidate identification,
or final field polynomial is proved by this precision increase.
D151's finite transfer search remains parked; all spectral/census,
new-level, Hecke and cubic pauses persist.

Sources 651–654 and their bound artifacts freeze after admission;
source 655 is next unused. Do not recreate fixed outputs or rerun
completed coordinators, setup or create. Future replay uses source 654
`--check` through `run_dyadic_capped.py` with a fresh receipt stem,
`PYTHONDONTWRITEBYTECODE=1` and all five numerical-library thread counts
set to one. Entry documents remain editable.
