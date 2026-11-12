# D135: full-bank cost after the completed P6400 column

Date: 2026-10-06. This is a planning calculation from the completed D133
receipts, not a precision increase or permission to launch the bank.
Acceptance is recorded in the D135 completion record after independent
review and replay. Earlier frozen sources, reports, receipts and stores
remain unchanged.

**Retain staged refinement. Prepare the missing execution interfaces and
target-memory controls before a larger run. A complete target bank needs
a multiweek compute commitment and additional disk capacity.** Direct
refinement from the existing P800/P1600 columns violates the 2 GiB working
store limit. Skipping the P1600 stage saves little space and costs more time.

## Measured starting point

D133 certifies column 0 at P6400; column 1 is at P1600 and columns 2--15
at P800. Its 24,579 jobs, including 24 audits and two reviews, passed.
The sum of all worker durations including review is 83,076.577 seconds,
or 23.08 worker-hours. Reconstructing its complete three-worker schedule
with serial barriers gives 9.79 active hours. The resumed coordinator's
28,534.211 seconds exclude earlier execution; neither figure is the
calendar interval across pauses and machine sleep.

The 24,553 production/archive jobs produced about 74,000 external files.
Their logical sizes total only about 90 MB, but their observed allocated
size is about 319 MB. Small-file allocation therefore matters. D133's
sealed store occupies about 652 MB, including metadata. These observations
are read from the actual files, not inferred from their logical payloads.

Source 560 verifies the input metadata/receipt bindings and reconstructs
phase durations, exact job counts, store inventories and retention scenarios.
Its [result](../data/computed/dyadic_bank_recost_d135.json) contains the full
assumptions, measurements, input hashes and per-stage costs. Source 561
independently checks counts, inventories, arithmetic totals and provenance;
it does not establish a statistical confidence interval for future runtimes.

## Remaining schedules

All estimates retain a global maximum of three workers. One column-stage
runs at a time, with parallel row jobs and serial low solves, state updates,
archives and review. Days mean 24 hours of active execution, excluding sleep.

| Remaining work | Jobs including archives/audits/reviews | Modeled active time | Assessment |
| --- | ---: | ---: | --- |
| Full staged bank to P10552 | 1,160,981 | 22.0--30.5 days | Preferred complete schedule, subject to execution gates |
| Skip P1600 for fourteen columns | 1,152,077 | 22.7--31.4 days | Slight storage saving, slower |
| Direct from current seeds to P10552 | 1,163,678 | 75.0--99.6 days | Rejected by the unchanged store cap |
| Full-bank P1600 checkpoint | 92,946 | 15.2--17.7 hours | Smaller useful commitment after interfaces/review are ready |
| One P6400-to-P10552 column | 31,925 | 19.5--29.5 hours | Possible calibration stage after target-memory checks |

The staged plan is fourteen 800-to-1600 lifts, fifteen 1600-to-3200
lifts, fifteen 3200-to-6400 lifts and sixteen 6400-to-10552 lifts.
The completed D133 lift is not charged again. Estimated total worker
time is 1,214--1,650 hours. Simple division by three understates elapsed
time because the schedule has serial dependencies.

These are empirical scenarios, not runtime bounds or a field-polynomial
ETA. The first scenario uses quadratic scaling for full-size operations;
the second uses cubic scaling and 25 percent extra job duration. Correction
bands within the observed range interpolate complete D133 all-state timings.
Larger bands use the saved GMP state-83 shape controls to scale the observed
anchor. This does not bound unseen maps or column-dependent data effects.
Factor sharing across columns and additional workers are not assumed.

The model includes seed extension, every low residual/solve/verification,
all correction jobs, serial preparation, per-sweep archives, full weighted
verification, all CM charts/coarse values, audits, review growth, and
target-size frame/quadric processing. The latter uses existing synthetic
controls. No I/O surcharge is added to already measured end-to-end times.
Extra contention and final arithmetic-input/zero-certification issues remain
unmeasured. The earlier D130 9--14-day ideal-worker model is superseded for
planning purposes by this completed-stage analysis.

## Storage and review design

At the recorded observation, about 50.7 GiB was free. This changes as other
applications use the volume and is not a reservation. Every existing frozen
artifact and all proposed intermediate stages are retained in this analysis.

| Retention/review design for staged target bank | Additional storage scenario | Free space including proposed 10 GiB reserve |
| --- | ---: | ---: |
| Repeated full cumulative catalogues | 69.2--80.7 GiB | 79.2--90.7 GiB |
| Incremental catalogue shards, still to implement | 53.0--64.6 GiB | 63.0--74.6 GiB |

The lower scenario scales measured allocated bytes and store metadata.
The second uses logical metadata ceilings and a 20 KiB external-record
allowance per job. Neither is a filesystem allocation bound. The catalogue
model uses 220 bytes per entry and three external records per job; store
manifest growth, filesystem metadata and future format changes can add cost.
The proposed 10 GiB reserve is a planning margin, not a changed resource cap.

Incremental review would avoid repeatedly copying all earlier catalogue
entries. Each new shard must bind the prior reviewed root and authenticate
its new artifacts, with a bounded complete replay. Merely omitting old hashes
from an unverified catalogue would not meet the project's preservation rule.
This design is not implemented or admitted by D135.

With that review design, plan for **at least 80 GiB free on the working
volume**, roughly 30 GiB more than the current observation, and check space
before admitting each stage. No frozen file may be deleted to obtain it.
The smaller full-bank P1600 checkpoint needs approximately 2.6--3.5 GiB
with cumulative review, so it does not itself require more disk capacity.

## Execution gates and recommendation

The staged P6400-to-P10552 inventory remains 2,046,552,040 logical bytes,
leaving 100,931,608 bytes under the 2 GiB store cap. Direct P800-to-P10552
and P1600-to-P10552 stages require approximately 5.43 GB and 4.78 GB,
respectively, under the same inventory and are rejected.

Before admitting another actual stage:

1. Publish reviewed seed/CM metadata adapters for the sealed weighted
   journal. The state seed interface is present; the complete CM reference
   interface is not published by the current seal output.
2. Measure complete target CM chart jobs within the 2 GiB per-job RSS rule.
   D133's largest chart used 862,683,136 bytes. Quadratic extrapolation to
   P10552 is about 2.18 GiB, above the rule; this is a risk indicator, not
   an observed failure. Existing target-size single-child controls reached
   at most 1.66 GiB and do not establish the two-child chart's peak.
3. Partition enlarged provenance review so each process remains under
   180 seconds. Full cumulative rehashes at millions of entries are not
   admitted. Preserve all 93,912 D134 source bindings.
4. Review the new configurations, audit plans and final full-frame comparison
   while preserving the global three-worker limit and all existing caps.

The next bounded work should resolve the target CM memory question and
the seed/review interfaces. Then the smaller P1600 full-bank checkpoint
offers a measured 15--18-hour step along the preferred staged route.
The user-facing decision is whether to commit to the multiweek full-bank
run and provide the necessary disk capacity, or prioritize further optimization
before that commitment. More workers or a Chatelet deployment are separate
choices: this model uses the local host and does not assume portability of
the frozen macOS libraries.

P10552 remains a conditional sufficient precision. Exact marked-base
identification, arithmetic genus-64 construction and the original-kernel
polynomial remain open. D134's conditional double-cover criterion is
reviewed, and its marked-base and canonical-Hecke hypotheses remain required.
