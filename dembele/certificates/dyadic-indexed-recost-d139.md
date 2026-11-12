# D139: bounded receipt lookup and next-stage costs

D138 remains the mathematical checkpoint: all sixteen columns reach P1600,
with column 0 retained at P6400. Exact positive-order quadric vanishing,
candidate/cover identification and a field polynomial remain unproved.
D139 changes bookkeeping and planning; it admits no precision bank.

## Lookup and preservation

The frozen source-551 archiver scans the entire computed-results directory
for each duplicate record. Source 577 preserves its transaction and every
receipt/log/metadata/driver check, replacing that glob with 100 exact probes
covering attempts `00` through `99`. It retains the durable archive intent,
external records, coarse records and arithmetic payloads. Frozen source 551
and all completed stores remain unchanged.

Source 576 supplies a prefix inventory for the production coordinator. The
candidate `run_d139_indexed_production.py` constructs it under the exclusive
column lock, registers each checked new attempt, and reconciles the inventory
before completion. The inventory is rebuilt on resume; it requires exclusive
ownership of the output prefix. Failed receipts, duplicate passing receipts,
orphan metadata and partial logs still stop execution for inspection. The
mathematical schedule, three-worker window and complete receipt verification
functions have identical syntax trees to the frozen D137 coordinator. A new,
hash-bound admission and its replay are required before this candidate runs.

Source 578's two bounded jobs pass. Discovery checks include eight synthetic
cases, attempt endpoints, malformed log suffixes, a broken symlink, rejection
of unexpected writes, and registration/resume. All 13,176 production receipts
from completed columns 2 and 15 match the new inventory and their saved hashes.
With 372,522 directory entries, sampled old lookups take about 0.41 seconds;
100 exact probes take about 0.001 seconds. A single inventory scan takes
0.44 seconds; checking and rehashing all 6,588 receipts takes 1.5–1.6 seconds.

In a new synthetic store, the complete 422-record archive takes 0.6803 seconds
and matches every item of column 15's original archive. The recorded original
archive job took 157.6806 seconds. These timings compare a replayed transaction
with a historical job, not simultaneous production measurements. Both injected
interruptions—after committing the intent and after removing one record—resume
idempotently. Payload/coarse/reserve sentinels remain byte-identical, and all
three synthetic fixtures are sealed. Intentional child exit 73 is a passing
interruption control, not a failed capped job.

## Reviewed planning scenarios

Source 580 is the revised model. Source 579 and its passing receipt are retained
as a superseded planning calculation. The revision uses measured P1600 per-job
floors, avoiding multiplication of already measured larger-job costs by a
small-job forecast discrepancy. Higher-precision arithmetic retains D135's
quadratic/cubic scenarios, with measured wrapper overhead and explicit new
archive, directory, incremental-catalogue and graph-review allowances.

| Scope | Bounded column jobs | Active time | Additional retained files | Free space including 10 GiB reserve |
| --- | ---: | ---: | ---: | ---: |
| Full P3200 checkpoint; lift columns 1–15 | 188,550 | 38.7–45.7 hours | 5.0–6.9 GiB | 16.9 GiB |
| Remaining staged bank to conditional P10552 | 1,068,035 | 20.8–29.4 days | 51.4–62.0 GiB | 72.0 GiB |
| One existing P6400 column to P10552 | 31,925 | 20.4–31.0 hours | 2.4–2.7 GiB | 12.7 GiB |

Job counts include each column's archives, audits and review/replay allowances;
bank comparison and provenance-shard jobs are additional. Times are active
compute scenarios, not promised calendar ETAs or certified runtime bounds.
Disk observations show 54.55 GiB free. P3200 fits with the proposed reserve;
the full conditional target requires additional space. Existing artifacts are
retained in every scenario. The P3200 logical working-store bound is
304,049,792 bytes, below the unchanged 2 GiB cap.

Reconstructing the completed P1600 production groups with the new bookkeeping
allowances gives about 9.0 hours for fourteen columns. This is a counterfactual,
not an optimized production run or a replacement for the recorded 22.05-hour
D137 bank runtime. In particular, the first new column must validate integrated
timing before relying on this model for a longer bank.

## Review and next decision

Source 582 independently checks receipt bindings, archived bytes, interruption
results, schedule preservation, job counts, cost arithmetic and storage totals,
without importing production arithmetic or either cost model. Its review and
replay traverse D138's fifteen inherited catalogues: 380,188 hash occurrences,
379,923 distinct inherited files, plus D138's direct bindings and the new D139
sources. Repeated identical bindings may share a digest check within one replay.

The initial source-581 review stopped after its provenance checks on a
`KeyError` in the reviewer's parsing of numbered prepare/sweep phases. Its
failed receipt, log and source snapshot are retained. Source 582 corrects that
parser, adds explicit regression checks, and authenticates the failed review.
No production arithmetic, control output or cost calculation changes.

The recommended next scope is the P3200 checkpoint, subject to a new user scope
decision and separately reviewed stage admission. Required preparation includes
the column-1 CM metadata adapter, stage-specific independent audit/review,
bounded provenance replays, and an initial-column timing check. The remaining
conditional target is substantially longer and needs more disk space. P10552
is a sufficient precision target under the existing hypotheses, not a necessary
precision or a guarantee of identifying Dembélé's field.

Keep all existing limits: at most three mathematical workers, a 180-second
private-process-group timeout per job, 2 GiB logical per working store,
2 GiB measured RSS per successful worker and a conservative 6 GiB sum.
Measured RSS admission is not an OS hard RAM limit. Sources 576–582, the
candidate coordinator, both cost records, controls, this report and fixed
review artifacts are frozen when D139 review/replay completes.
