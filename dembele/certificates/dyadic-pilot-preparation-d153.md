# D153: one column-2 P3200 timing pilot is prepared

Date: 2026-10-09. Preparation after the D152 cost assessment.

**Result:** the exact column-2 P1600-to-P3200 pilot has a configuration,
direct input provenance, working-store inventory, independent audit plan
and bounded column reviewer. The fixed admission permits only this one
configuration with the frozen D139 indexed coordinator. No production
schedule has been launched. The successful source-554 `create` preflight
allocated the initial pool; all 174 row commitments remain empty and no
new moments have been evaluated.

The next work is the integrated pilot, followed by its audits and review,
then a timing reassessment before another column or stage. The estimate
remains **2.9--3.4 active hours**, not a measured runtime or deadline.
The full multiweek bank is outside this admission. P3200 by itself does
not prove exact positive vanishing or identify the candidate curve.

## 1. Exact scope and inputs

The [D152 cost assessment](precision-route-cost-d152.md) recommends this
measurement because the [D139 indexed coordinator](dyadic-indexed-recost-d139.md)
has not yet supplied integrated new-column timing. Column 2 already has
the necessary [D137 seed and CM interface](dyadic-checkpoint-revision-d137.md)
and [D138 bank provenance](dyadic-precision1600-bank-d138.md).
The column-1 metadata adapter is unnecessary for this pilot.

The frozen [configuration](../data/computed/dyadic_staged_P3200_col02_config_d153.json)
sets P=3200, S=1600, column=2, digit width 200, state/CM chunk 1 and
right-hand-side chunk 3. Its owned namespace is
`dyadic_rowjournal_P3200_col02_d153_d132`; its production prefix is
`dyadic_staged_P3200_col02_d153`.

The [seed bridge](../data/computed/dyadic_pilot_seed_bridge_d153.json)
directly binds 30 inputs: the sealed weighted seed and its binary, the
lossless CM interface and binary, transport and harmonic certificates,
and the complete source-554 Python/native dependency closure. Every
binding occurs directly in the D138 review. The bridge authorizes no
schedule itself. This satisfies the engine's actual direct-lookup
contract instead of relying on an indirect catalogue reference.

[Source 637](../pari/637_dyadic_pilot_setup.py) prepares these inputs.
[Its packet](../data/computed/dyadic_pilot_setup_d153.json) carries the
full phase inventory and a dated free-space observation. The
[create preflight](../data/computed/dyadic_staged_P3200_col02_d153_create.json)
uses the frozen production engine, so it exercises that exact dependency
contract. The indexed coordinator will reuse its existing passing receipt.
Mutable pool files are not hash-frozen in the admission; the immutable
INPUTS manifest is bound. Existing sealed stores remain unchanged.

## 2. Audit and archive compatibility

The old independent auditor assumed a uniform old seed. This pilot's
P1600 seed is packed with degree-dependent precision. New
[source 635](../pari/635_dyadic_pilot_independent.py) reads both formats
and compares each scalar at its certified old precision. Its quotient
arithmetic, recurrence, CM and Horner functions are unchanged from 564.
It never imports production arithmetic.

The [24-job audit plan](../data/computed/dyadic_pilot_col02_audit_plan_d153.json)
checks all 2,227,200 old state scalars, all 435,200 old CM scalars,
174 masses and residual rows, and all 68 old coarse overlaps. Separate
original-recurrence checks sample degrees 1,2,3 at states 0,83,173 and
CM charts 0,8,16; six Horner evaluations cover charts 0,8,16 and orders
0,3. These samples do not independently recompute the complete new
operator. Complete original weighted equations remain certified by the
authenticated production phases.

New [source 636](../pari/636_dyadic_pilot_column_review.py) retains the
existing store, phase and receipt checks, selects the indexed archiver
577 and coordinator 139 for this exact pilot, and checks the reconciled
receipt inventory. It publishes the lossless P3200 CM interface only
after successful production and all audits. Its D137 packet/audit-plan
schema is retained for the frozen audit harness; `execution_milestone`
identifies D153. This wire-format label does not imply old precision.

The [control packet](../data/computed/dyadic_pilot_controls_d153.json)
from [source 638](../pari/638_dyadic_pilot_controls.py) records:

- All five independent phase types reproduce known P6400 certificates.
- The revised reviewer reproduces the completed P6400 store and all
  24,553 production/archive receipt checks in 33.40 seconds.
- Actual weighted seed rows 0,83,173 match the existing native reader.
  Synthetic extension fixtures exercise both uniform and weighted old
  overlaps; eight malformed-input checks reject bad data.
- A synthetic indexed-archive fixture preserves and checks 6,326 external
  records. It accepts the indexed archiver source and rejects the old
  source. No old store is written; synthetic fixtures are not new actual
  harmonic data.
- The coordinator's 12,495 phase specifications exactly match the separate
  reviewer specification. The frozen D139 receipt/interruption controls
  are retained, including both idempotent archive recovery points.

## 3. Resource and timing inventory

There are **12,570 jobs**: 12,495 production phases, 49 metadata archives,
24 independent audits and two column reviews. One production phase,
`create`, has already passed without initializing rows. The remaining
scheduled count is therefore 12,569 if that receipt is reused.

The largest logical working store is **304,049,792 bytes** (about
290 MiB), including workspace and metadata allowances. Initial state
payload is 113,343,600 bytes. D152 models 0.46--0.59 GiB additional
retained space and recommends 11,368,085,472 free bytes (10.59 GiB),
including its 10 GiB planning reserve. The setup observed 55,296,000,000
free bytes (51.50 GiB) at 2026-10-09T19:19:40 UTC. These dated planning
figures do not promise future free space or total allocation.

Every mathematical, control, audit and review job uses the unchanged
180-second private-process-group wrapper. Maximum concurrency remains
three mathematical workers, with 2 GiB per worker/store and 6 GiB
aggregate. RSS admission uses measured peaks; it is not an OS-enforced
hard RAM limit. Keep only one production/audit coordinator active and
include manual jobs in the same three-worker allowance. Preparation jobs
are sequential. The completed D136 target CM controls remain applicable;
no obsolete memory experiment is reopened.

The integrated measurement should report production coordinator elapsed
time, audit elapsed time, both review times, summed worker/archive time,
per-phase timing, maximum RSS and observed store size. Separate active
time from pauses/restarts and the already completed preparation. Compare
with the D152 scenarios before scheduling another column. Retain failures
and inspect them; do not overwrite or bypass a failed receipt.

## 4. Concrete launch sequence

The [fixed admission](../data/computed/dyadic_pilot_preparation_review_d153.json),
[source ledger](../data/computed/dyadic_pilot_preparation_sources_d153.json) and
[preparation completion](../data/computed/dyadic_pilot_preparation_completion_d153.json)
bind the exact inputs, code and successful bounded preparation receipts.
[Source 639](../pari/639_dyadic_pilot_preparation_review.py) traverses the
D152 chain, retaining 380188 inherited hash occurrences and 379923 unique
inherited files, and independently replays the new finite controls.
Its passing `--check` receipt is the coordinator's admission gate.

The following is the prepared sequence from the repository root. It has
not been launched. Run each step only after its predecessor passes;
completed coordinator outputs must not be recreated. Preserve the single
column boundary. Both coordinators invoke the capped wrapper internally.

```sh
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1

python3 dembele/pari/run_d139_indexed_production.py --config dyadic_staged_P3200_col02_config_d153 --workers 3
python3 dembele/pari/run_d137_audits.py --plan dyadic_pilot_col02_audit_plan_d153 --workers 3

python3 dembele/pari/run_dyadic_capped.py dembele/pari/636_dyadic_pilot_column_review.py dyadic_pilot_col02_review_d153_attempt01 'PASS|636_DYADIC_PILOT_COLUMN_REVIEW' --config dyadic_staged_P3200_col02_config_d153 --output dyadic_pilot_col02_review_d153
python3 dembele/pari/run_dyadic_capped.py dembele/pari/636_dyadic_pilot_column_review.py dyadic_pilot_col02_review_d153_recheck01 'PASS|636_DYADIC_PILOT_COLUMN_REVIEW' --config dyadic_staged_P3200_col02_config_d153 --output dyadic_pilot_col02_review_d153 --check
```

After these steps, record the integrated timing and its receipts in a
fresh checkpoint and reassess. Neither a second column nor P6400 follows
automatically. The D153 admission's `--check` can be replayed through the
wrapper with a fresh stem; do not overwrite its fixed recheck receipt or
re-run setup, create, or completion against existing names.

## 5. Mathematical status remains unchanged

The full bank remains at P1600, with column 0 at P6400. The D152
conditional sufficient target remains P10480 and depends on future
certified zero enclosures and all stated error hypotheses. The old
order-four target is P10552. The proved relation-height upper remains
15237, versus the P1600 sufficient target 623. D151's finite rational
transfer search remains parked.

Exact positive vanishing, actual/candidate identification, the
original-kernel field polynomial and subsequent marking/cover/Hecke/torsion
obligations remain open. All spectral/census, new-level, Hecke and cubic
pauses persist. No remote computation or correspondence is part of this
preparation. Sources 635--639 and passing artifacts are frozen after
review; source 640 is next unused.
