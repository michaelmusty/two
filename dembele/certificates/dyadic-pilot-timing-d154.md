# D154: measured column-2 P3200 pilot

Date: 2026-10-09. Actual execution after the D153 preparation.

**Result:** the admitted column-2 P1600-to-P3200 pilot is complete,
including every production phase, archive, independent audit and both
column reviews. Its measured column cycle is **2.126 active
hours**, compared with D152's **2.56--3.02-hour per-column scenarios**
(2.9--3.4 hours when its shared graph/comparison allowances were included).
This measures one column at this stage; higher-stage costs remain unmeasured.

The [timing packet](../data/computed/dyadic_pilot_timing_d154.json),
[fixed review](../data/computed/dyadic_pilot_timing_review_d154.json),
[completion record](../data/computed/dyadic_pilot_timing_completion_d154.json)
and [source ledger](../data/computed/dyadic_pilot_timing_sources_d154.json)
record the observations, bounded receipts and inherited provenance.

## 1. Completed computation

The exact configuration and admission are those of the
[D153 preparation](dyadic-pilot-preparation-d153.md). The frozen
[D139 indexed coordinator](dyadic-indexed-recost-d139.md) ran 12,495
production phases and 49 archives. It reused only the already completed
empty-store `create` receipt. All 24 independent audits and both column
reviews passed: **12,570 column jobs, including one inherited job**.
No bounded attempt failed. The coordinator survived the server restart;
its original run completed without a second coordinator or repeated job.

The [column review](../data/computed/dyadic_pilot_col02_review_d153.json)
certifies all 4,454,400 original weighted-equation scalar checks, 174
fixed masses, 870,400 CM scalars and 68 coarse values. The four coarse
error exponents are 6432, 6448, 6432 and 6464. The new store is sealed.
The [lossless CM interface](../data/computed/dyadic_CM_P3200_col02_d153.json)
is available without a duplicate assembled binary.

The independent auditor verifies all 2,227,200 old state scalar overlaps,
435,200 old CM overlaps, 174 final residual rows and masses, and 68 old
coarse overlaps. Separate original-recurrence checks cover 72 state and
72 CM scalars; sampled Horner checks cover 96 beta scalars. Those samples
do not independently recompute the complete new operator. Complete new
weighted equations are certified through authenticated production jobs.

## 2. Observed time and resources

| Component | Measured seconds |
| --- | ---: |
| Production coordinator, including archives and scheduling | 7626.237 |
| Independent audit coordinator | 6.490 |
| Column review and hash replay | 15.317 + 5.248 |
| Previously completed create, separately charged | 0.187 |
| Complete column cycle | 7653.480 |

The active total uses the coordinators' monotonic clocks and bounded
review receipts. It excludes D153 preparation other than the separately
charged create and excludes the D154 timing/transitive-review jobs.
Summed production worker time is 17858.032 seconds;
archive worker time is 31.986 seconds; audit worker
time is 18.213 seconds. Concurrent worker sums are not
elapsed column time. The timing packet retains every phase's counts,
sum, median, maximum and coordinator-callback overhead.

The production log spans 2026-10-09 19:38:49 to 2026-10-09 23:16:17 UTC,
or 3.624 wall-clock hours. The captured macOS power
log reports 5450 seconds of host sleep during that span.
The filesystem span exceeds the production monotonic measurement by
5421.835 seconds. These are separate observations; filesystem
timestamps are not an exact launch timer. Temporary idle-sleep prevention
was used after the sleep delays were noticed. No permanent power setting
was changed.

Maximum recorded production concurrency was 3. Maximum
production/audit RSS was 297,304,064 bytes; the conservative sum of
concurrent production peaks was 842,891,264 bytes. The
largest observed working store was 291,519,605 bytes,
below its proved 304,049,792-byte inventory bound. The longest column
input job took 15.317 seconds; the slowest archive
took 1.914 seconds.

All mathematical, control, audit and review jobs retained the 180-second
private-process-group timeout, at most three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate. RSS checks are measured
admission, not an OS-enforced hard RAM limit. No cap changed.

The sealed store and owned external column artifacts occupy
224,856,279 logical bytes and 343,166,976
allocated bytes in the dated filesystem observation. This excludes
preparation controls and D154 closing artifacts; allocation measurements
do not predict future APFS sharing or free space.

## 3. Reassessment

The [D152 cost model](precision-route-cost-d152.md) supplied empirical
scenarios, not time bounds. Relative to its two modeled per-column
P3200 costs, this observed cycle has ratios 0.831 and 0.705. Shared
graph-review/comparison allowances in the original pilot totals remain
separate from the measured column cycle.

There are **1,047,369 planned column jobs remaining** on the original
route. Replacing only the other 14 P3200 column costs with this measured
cycle, while retaining D152's unmeasured higher-stage costs and common
allowances, gives **485.2--683.9 active hours**, or
**20.2--28.5 active days**, still conditional scenarios.
One column supplies no bound for the other columns or higher precision.
The report does not apply its speed ratio to the P6400 or P10480 stages.

After debiting the completed pilot's modeled retained allowance, the
remaining route still calls for 71.02 GiB free including
the full largest active-store allowance and the 10 GiB planning reserve.
The dated observation is 48.07 GiB, leaving a modeled
shortfall of 22.95 GiB. These retained planning allowances
are not an allocation guarantee.

**Decision:** keep the larger bank paused. This pilot provides an
integrated first-stage timing but does not remove the higher-stage
runtime uncertainty or disk-space gap. A continuation should first
resolve the storage plan and separately review a bounded higher-stage
timing measurement. No next column or higher stage is admitted here.

## 4. Provenance and remaining mathematical obligations

[Source 640](../pari/640_dyadic_pilot_timing.py) calculates the measured
timing and limited repeat scenarios.
[Source 641](../pari/641_dyadic_pilot_timing_review.py) independently checks
the totals and scenarios, authenticates the complete coordinator logs,
rehashes the new column catalogue, and traverses the frozen D153/D152
provenance chain. Its `--check` mode replays the fixed review with a fresh
capped receipt; `--finish` verifies both review receipts and 28 artifact
links across the seven entry documents. Entry-document hashes remain
unfrozen. Sources 640--641 and their successful bound artifacts freeze
after review; source 642 is next unused. These finite checks do not
mechanically verify the inherited geometric arguments.

The full sixteen-column bank remains at P1600; column 0 remains at P6400
and column 2 is now at P3200. P10480 remains only a conditional sufficient
target requiring future actual zero enclosures and all error hypotheses.
The proved relation-height upper remains 15237 versus the P1600
sufficient target 623. No exact positive vanishing, actual/candidate
identification or original-kernel field polynomial is proved by this
pilot. D151's finite rational transfer search remains parked. All
spectral/census, new-level, Hecke and cubic pauses persist.
