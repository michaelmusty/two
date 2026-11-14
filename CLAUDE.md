# Project: making Dembélé's field explicit

<!-- D158 methodology pivot -->

**Current direction: D158 — methodology pivot (2026-11-13).** The user
adopted the [D158 review](dembele/certificates/methodology-pivot-d158.md):
stop proving that the genus-16 candidate is the Shimura quotient; assume
it, compute the degree-257 polynomial by p-adic torsion at a prime chosen
for small Frobenius order, and verify the final polynomial directly. The
P10480 bank is off the route. New-track work lives in `dembele/pivot/`
and runs on Chatelet without the 180-second/2 GiB/three-worker limits or
the frozen-replay requirement; logs are kept, and DECISIONS, HANDOFF and
REFERENCES are updated as work proceeds. All earlier frozen artifacts stay
untouched. Blocks below this one are historical.

**Next steps (D158 plan):** (1) Frobenius-order scan,
`dembele/pivot/01_frobenius_order_scan.m`, one Magma process per rational
prime on Chatelet (`HMF_ROOT=two_hilbertmodularforms`); (2) rebuild the
p-adic model of Y at the chosen prime; (3) cost one torsion point (go/no-go);
(4) compute, recognize and verify the polynomial. Scan done (D159); the
model is degenerate mod 17, so step 2 runs at norm 673 (D160); see the
top of HANDOFF. Local Magma is not
licensed on host `otto`; use Chatelet. The D157 replay cannot pass on
`otto` and is not required.

<!-- D157 higher pilot timing checkpoint -->

**Current checkpoint: D157 — the approved column-2 P3200-to-P6400 pilot
is complete.** The [D157 report](dembele/certificates/dyadic-higher-pilot-timing-d157.md),
[fixed review](dembele/data/computed/dyadic_higher_pilot_timing_review_d157.json),
[completion record](dembele/data/computed/dyadic_higher_pilot_timing_completion_d157.json) and
[source ledger](dembele/data/computed/dyadic_higher_pilot_timing_sources_d157.json)
record its results, bounded reviewer repair and timing reassessment.

All 24456 production phases, 97 archives and 24 independent audits passed.
The corrected column review and replay also passed: **24579 successful
column jobs**, including the inherited create. No production or audit job
failed or was rerun. Source 647's final review failed on its obsolete
D153 audit-label assertion. That receipt, log and source snapshot remain
frozen. Source 651 corrects the execution-label assertion and the indexed
receipt-inventory branch; source 652 accepts the actual audits and rejects
seven malformed fixtures. Arithmetic sources are unchanged.

Use `dyadic_higher_pilot_col02_review_r2_d157` as the completed column review
for the unchanged `dyadic_staged_P6400_col02_config_d156` configuration.
The original config's `dyadic_higher_pilot_col02_review_d156` output remains
absent. The CM interface `dyadic_CM_P6400_col02_d156` is now published.
The supervisor's original stopped-after-failure status is preserved;
the separate D157 completion records its successful review recovery.
Do not restart the supervisor, production/audit coordinators, setup or
create, and do not reuse completed output stems. The owned coordinator
locks are free and the temporary power assertion ended.

The successful column cycle measured **9.397 active hours**, or 9.405
including the failed review and regression controls. Production itself
used 9.378 active hours and spanned 12.385 wall-clock hours; this checkpoint
does not establish the cause of the clock gap. It separately accounts for
active time and wall time. Updated remaining scenarios are **19.7–26.5
active days** for 1022790 column jobs. P10480 is still unmeasured, and
one column does not bound other columns or later stages.

The full-bank capacity gap persists. Remaining planned free space is
69.85 GiB including the full largest active-store extra and 10 GiB reserve;
the rounded gate is **70 GiB**. On October 13 at 12:56:44 UTC, 43.87 GiB
was free, leaving **26.13 GiB to the rounded gate**. Preserve all frozen
files; no deletion, relocation or alternate destination is authorized.
The full bank, other columns and P10480 launches remain paused.

**Actual data:** the complete bank remains P1600; columns 0 and 2 are
P6400. Full new equations and complete old overlaps are authenticated;
independent new-equation checks remain samples. D155's conditional proof
criterion still requires actual future errors and exact successive
vanishing. Exact positive vanishing, candidate identification and the
field polynomial remain open. D151 stays parked; spectral/census,
new-level, Hecke and cubic pauses persist.

Keep every mathematical/control/audit/review job under the 180-second
private-process-group cap, at most three workers, 2 GiB per worker/store
and 6 GiB aggregate. Set PYTHONDONTWRITEBYTECODE=1 and the OPENBLAS, OMP,
MKL, VECLIB and NUMEXPR thread counts to one. Sources 651–654 and bound
artifacts are frozen; source 655 is next unused. Source 654 `--check`
with a fresh capped receipt performs the transitive replay. Entry-document
hashes stay editable; earlier D156 blocks are historical.

D157 completion is finished: **24584 new passing bounded jobs and one
preserved failed review attempt**. Fixed provenance review and replay
passed in 86.12/85.10 seconds; completion checked 28 current links across
seven entry documents and records 55 direct source bindings. All jobs
owned by this continuation have exited. No next computation is running.

<!-- End D157 higher pilot timing checkpoint -->

<!-- D156 pilot preparation checkpoint -->

**Current preparation: D156 — storage plan and one column-2 P3200-to-P6400 timing pilot.**
The [D156 report](dembele/certificates/dyadic-higher-pilot-preparation-d156.md),
[fixed admission](dembele/data/computed/dyadic_higher_pilot_preparation_review_d156.json),
[completion record](dembele/data/computed/dyadic_higher_pilot_preparation_completion_d156.json) and
[source ledger](dembele/data/computed/dyadic_higher_pilot_preparation_sources_d156.json)
bind the exact configuration, inputs, controls, storage and launch sequence.

The single pilot is `dyadic_staged_P6400_col02_config_d156`, using the
completed D154 P3200 seed. There are **24579 column jobs**: 24456 production,
97 archives, 24 independent audits and two column reviews. The empty-store
create preflight is complete and must be reused; all 174 row commitments
remain empty. No new harmonic moments or production coordinator have run.

The column-cycle model is 9.55–11.98 active hours, or **10.79–13.79 hours**
with conservative shared allowances. These are scenarios, not measured
runtimes. The working-store bound is 973167872 bytes. A fresh **12 GiB**
free-space gate includes the 10 GiB reserve. Source 650 `--launch-check`
checks the initial state, fixed replay and current space before a launch.
The report contains the exact sequence. After a separate launch decision,
run only this column, all audits and both reviews, then reassess.

**Full-bank storage remains unresolved.** The October 12 observation is
44.63 GiB free, against 71.02 GiB modeled; the rounded **72 GiB** full-bank
gate needs 27.37 GiB more. No separate volume is selected. Retain all
frozen data; no deletion or relocation is authorized. The pilot fits the
observed space, but no other column, P10480 stage or bank is admitted.

The full bank remains P1600, column 0 P6400 and column 2 P3200. D155's
P10480 sufficient criterion remains conditional on actual certified errors
and exact successive vanishing. Candidate identification and the field
polynomial are open. D151 stays parked; spectral/census, new-level, Hecke
and cubic pauses persist. P10480 timing remains unmeasured.

Keep the 180-second private-process-group cap, at most three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate. Preparation jobs are
sequential. Sources 645–650 and their successful bound artifacts freeze
after admission; source 651 is next unused. Use source 650 `--check` with
a fresh capped receipt for transitive replay. Do not recreate setup,
create, fixed review, recheck01 or completion outputs. Earlier blocks
remain historical, and entry-document hashes remain editable.

D156 completion: all 13 bounded preparation jobs pass with no failures.
Fixed admission and replay took 89.07/84.67 seconds, below the unchanged
180-second limit. Completion checks 28 current artifact links across seven
entry documents and records 93 direct bindings. All jobs owned by this
preparation have finished; no production or audit coordinator was launched.

<!-- End D156 pilot preparation checkpoint -->

<!-- D155 proof criterion checkpoint -->

**Current reviewed checkpoint: D155 — P10480 remains a valid conditional
base-curve identification criterion after rigorous review.**
The [D155 report](dembele/certificates/proof-criterion-review-d155.md),
[fixed review](dembele/data/computed/proof_criterion_review_d155.json),
[completion record](dembele/data/computed/proof_criterion_completion_d155.json) and
[source ledger](dembele/data/computed/proof_criterion_sources_d155.json)
record the proof, exact finite checks and inherited provenance.

The actual rank-45 minor plus the Riemann–Roch dimension 45 proves that
orders zero through two suffice; the argument explicitly needs D106's
rational descent. All 6528 actual matrix entries were replayed at both
96 and 160 bits. Exact CM-frame vanishing of all 91 quadrics and the
height thresholds were independently checked.

The P10480 strict margins are 6.104656 for order one and 0.169368 for
order two. P10472 fails the second test. An additional uniform loss of
four beta-digits would exhaust the latter margin. Future data must pass
the complete error ledger, zero-containment tests and successive exact
vanishing argument. Reaching a precision label is insufficient.

The review reconciles a factor-of-two discrepancy in Zhao's proof from
the integral line-bundle identity, retaining the existing height bound.
This is a mathematical source reconciliation, not an author-confirmed
correction or formal verification of the inherited geometry.

**Decision:** retain the conditional criterion and keep the larger bank
paused. The base curve, positive exact vanishing and final field polynomial
are still unproved. P32/B3 and the upstairs cover remain separate.
Full-bank precision stays P1600; column 0 stays P6400 and column 2 P3200.
D154's timing and storage limitations and D151's parked search persist.
No new column, higher stage or bank is admitted.

Keep the 180-second private-process-group cap, at most three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate. D155 jobs are
sequential. Sources 642–644 and their bound reports/artifacts are frozen;
source 645 is next unused. Source 644 --check is the transitive replay,
using a fresh receipt stem. Preserve earlier checkpoints as history.

D155 completion: all five bounded jobs pass, with no failed attempts.
Fixed review and replay took 68.18/66.96 seconds, with peak RSS below
280 MB. Completion checks 28 artifact links across seven entry documents
and records 35 direct bindings. All owned mathematical jobs have finished.

<!-- End D155 proof criterion checkpoint -->

<!-- D154 pilot timing checkpoint -->

**Current reviewed checkpoint: D154 — the column-2 P1600-to-P3200 pilot is complete.**
The [D154 report](dembele/certificates/dyadic-pilot-timing-d154.md),
[fixed review](dembele/data/computed/dyadic_pilot_timing_review_d154.json),
[completion record](dembele/data/computed/dyadic_pilot_timing_completion_d154.json) and
[source ledger](dembele/data/computed/dyadic_pilot_timing_sources_d154.json)
record the actual column, measured timing and limited remaining-route scenarios.

All 12570 column jobs pass: 12495 production phases, 49 archives,
24 independent audits and both column reviews. One empty-store create
receipt was inherited from D153; 12569 column jobs are new. The original
coordinator survived the server restart and completed without replaying
jobs. The P3200 store is sealed and its lossless CM interface is published.
Full new equations use authenticated production checks; independent
original-equation samples retain their narrower scope. No attempt failed.

The measured column cycle is 2.126 active hours, versus modeled per-column
costs 2.56--3.02 hours (2.9--3.4 with shared planning allowances).
Production spans 3.624 wall-clock hours; the power log records 5450 seconds
of host sleep. Monotonic computation time and filesystem observations
remain separate. Temporary idle-sleep prevention changed no permanent setting.

**Decision:** keep the larger bank paused. Replacing only the remaining
14 P3200 column costs gives conditional remaining scenarios of 20.2--28.5
active days; higher-stage costs remain unmeasured. The remaining storage
plan calls for 71.02 GiB free including reserve, versus 48.07 GiB observed,
a 22.95 GiB shortfall. Resolve the storage plan and separately review a
bounded higher-stage timing measurement before another launch. No next
column, higher stage or full bank is admitted by D154.

The full bank remains P1600; column 0 remains P6400 and column 2 is now
P3200. P10480 remains a conditional sufficient target, not attained data.
The relation-height upper remains 15237 versus the P1600 target 623.
Exact positive vanishing, candidate identification and the field polynomial
remain open. D151 stays parked; spectral/census, new-level, Hecke and
cubic pauses persist.

Retain the 180-second private-process-group cap, at most three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate. The observed working
store maximum was 291519605 bytes, below its 304049792-byte bound.
Sources 640--641 and their bound artifacts are frozen; source 642 is next unused.
Use source 641 --check through run_dyadic_capped.py with a fresh receipt
stem for transitive replay. It retains 380188 inherited hash occurrences
and checks the new 38446-binding column catalogue. Preserve all frozen
sources, stores and receipts. Entry documents remain editable; earlier
checkpoint blocks are historical.

D154 completion: all 12573 new bounded jobs pass, with no failed attempts;
one prior create receipt is reused. The fixed review and replay took
65.76/64.84 seconds. Completion checks 28 artifact links across the seven
entry documents and records 36 direct bindings. All owned mathematical
jobs have finished, both coordinator locks are free, and the temporary
idle-sleep assertion has been removed.

<!-- End D154 pilot timing checkpoint -->

<!-- D153 pilot preparation checkpoint -->

**Current reviewed checkpoint: D153 — the single column-2 P1600-to-P3200 timing pilot is prepared.**
The [D153 report](dembele/certificates/dyadic-pilot-preparation-d153.md),
[fixed admission](dembele/data/computed/dyadic_pilot_preparation_review_d153.json),
[preparation completion](dembele/data/computed/dyadic_pilot_preparation_completion_d153.json) and
[source ledger](dembele/data/computed/dyadic_pilot_preparation_sources_d153.json)
bind the exact configuration, input closure, controls and launch sequence.

The admission permits only column 2 at P3200 from its existing P1600 seed,
using the frozen D139 indexed coordinator. No production schedule has
been launched. Source-554 create passed with all 174 row commitments empty;
no new moments were evaluated. Its passing receipt will be reused.
The seed bridge directly binds all 30 seed/CM/native dependencies in D138.

The plan has 12570 jobs (12495 production, 49 archives, 24 audits, two
reviews), including the completed empty-store create. The working-store
bound is 304049792 bytes. Modeled active time remains 2.9--3.4 hours;
10.59 GiB free is recommended including reserve, versus the saved 51.50 GiB
observation. These are planning scenarios, not runtime or allocation bounds.

Source 635 supports the weighted old seed and reproduces five known
P6400 audit phases. Source 636 reproduces the completed P6400 review,
accepts the indexed archive format and retains bounded provenance checks.
Source 638 tests packed overlaps, malformed inputs and all job specifications.
Independent full old overlaps and sampled original-equation checks retain
separate scopes. Complete new equations use authenticated production jobs.

**Next:** run the one prepared pilot through production, all audits and
both reviews, then record integrated timing and reassess before another
column or stage. The full bank is not admitted. P3200 alone does not
identify the candidate. The full bank remains P1600, column 0 remains
P6400, and D152's conditional sufficient target remains P10480 (old P10552).
The relation-height upper remains 15237 versus the P1600 target 623.
Exact positive vanishing and the field polynomial remain open. D151 stays
parked; spectral/census, new-level, Hecke and cubic pauses persist.

Keep the 180-second process-group cap, at most three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate. Preparation jobs are sequential.
Source 639 --check replays the transitive preparation with a fresh receipt
stem. Preserve frozen sources, stores, passing artifacts and failed snapshots;
source 640 is next unused. Earlier checkpoint blocks are historical.

D153 preparation completion: all 12 bounded jobs pass, with no failed
bounded attempts. Admission/replay took 77.87/76.54 seconds; completion
checked 28 artifact links across seven entry documents. All jobs owned
by this preparation have completed. The production pilot is not running.

<!-- End D153 pilot preparation checkpoint -->

<!-- D152 precision cost checkpoint -->

**Current reviewed checkpoint: D152 — rank 45 lowers the conditional precision target to P10480; the bank still costs about three to four active weeks.**
The [D152 report](dembele/certificates/precision-route-cost-d152.md),
[fixed review](dembele/data/computed/precision_route_review_d152.json),
[completion record](dembele/data/computed/precision_route_completion_d152.json) and
[source applicability ledger](dembele/data/computed/precision_route_sources_d152.json)
record the sufficient-precision argument, cost scenarios and provenance.

The existing actual rank-45 restriction makes exact vanishing through
coarse order two sufficient. Combining it with the proved uniform section
error law gives conditional P10480, versus P10552 for the order-four
argument. Future actual zero enclosures and all arithmetic error hypotheses
are still required. All sixteen columns remain inputs to the current frame
evaluator. The observed extra P1600 digits are not extrapolated.

The staged P10480 plan has 1,059,939 bounded column jobs and modeled active
time 20.6--29.2 days. It needs about 71.5 GiB free including the 10 GiB
planning reserve; the saved observation is 51.5 GiB, about 20.0 GiB short.
These are empirical scenarios, not runtime or allocation bounds. Direct
P1600-to-P10480 refinement violates the unchanged working-store cap.
D136 already supplies complete synthetic target CM memory controls.

**Next preparation:** a separately reviewed column-2 P1600-to-P3200 timing
pilot using its existing seed/CM data and the D139 indexed coordinator.
The estimate is 2.9--3.4 active hours and 0.46--0.59 GiB additional retained
space. Preserve source-554 direct seed/native dependency admission,
stage-specific independent audits and bounded provenance. No pilot or bank
launch follows from this cost checkpoint; P3200 alone does not identify C.

D151's finite rational transfer search stays parked. The proved actual
relation-height upper remains 15237; the P1600 sufficient target remains
623. Positive exact vanishing, identification, P32/B3, downstream
cover/Hecke/torsion obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged, as are all spectral/census,
new-level, Hecke and cubic pauses. Sources 632--634 are frozen;
source 635 is next unused. Earlier checkpoint blocks are historical.

The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate persist. D152 jobs are
sequential. Use source 634 with --check and a fresh receipt stem for a
transitive replay; do not recreate completed outputs. Finite checks do
not mechanically verify the companion rank argument or inherited geometry.

D152 completion: all five bounded jobs pass, with no failed bounded
attempts. The completion record checks 28 checkpoint links across the
seven entry documents. All jobs owned by this continuation are complete.

<!-- End D152 precision cost checkpoint -->

<!-- D151 summed transfer checkpoint -->

**Current reviewed checkpoint: D151 — the finite rational summed-transfer witness search is parked.**
The [D151 report](dembele/certificates/summed-transfer-obstruction-d151.md),
[fixed review](dembele/data/computed/summed_transfer_review_d151.json),
[completion record](dembele/data/computed/summed_transfer_completion_d151.json) and
[source applicability ledger](dembele/data/computed/summed_transfer_sources_d151.json)
record the companion proof, exact finite witnesses and inherited provenance.

The first positive CM coefficient of saved candidate quadric 0 is a
nonconstant cleared polynomial of degree 240 in 288 scalar integral
inputs. Invariant principal-part functionals preserve every polynomial
moment while assigning those CM inputs freely. They therefore exclude
D150's finite rational tensor transfer certificate for this residual,
including summed cancellations and arbitrary rational witness poles.
These functionals are discontinuous: the proof neither changes the
actual bounded measure nor refutes the candidate.

**Decision:** do not expand this finite witness search. Any continuation
must name additional analytic or geometric input, or reassess the cost
of the established sufficient precision/height route. A cost assessment
does not admit a larger bank. Retain the rank-45 or order-four implication
as the exact identification target. The proved actual relation-height
upper bound remains 15237; the sufficient target remains 623.

Exact positive vanishing, candidate identification, P32/B3 markings,
the subsequent cover/Hecke/torsion obligations and the field polynomial
remain open. P1600 and column 0/P6400 are unchanged. All existing
spectral, census, new-level, Hecke and cubic pauses persist.
Sources 629--631 and passing artifacts are frozen;
source 632 is next unused. Earlier checkpoint blocks are historical.

D151 completion: five bounded jobs pass, with no failed bounded attempts.
The two finite arithmetic jobs use independent quadric derivative
checks and matrix controls. Finite checks do not mechanically verify the
infinite-dimensional functional construction or inherited geometric proofs.
The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate persist. All D151 jobs
are sequential. Use source 631 with --check and a fresh receipt stem
for a transitive replay; do not recreate completed output names.

<!-- End D151 summed transfer checkpoint -->

<!-- D150 structural identification checkpoint -->

**Current reviewed checkpoint: D150 — the structural audit isolates the exact comparison and excludes finite branchwise rational closure.**
The [D150 report](dembele/certificates/structural-identification-audit-d150.md),
[fixed review](dembele/data/computed/structural_identification_review_d150.json),
[completion record](dembele/data/computed/structural_identification_completion_d150.json) and
[source applicability ledger](dembele/data/computed/structural_identification_sources_d150.json)
record the scope, finite witnesses and inherited provenance.

The actual rational frame and rank-45 jet map, and the candidate's
smooth canonical scheme, are established separately. The inspected
descent, Shimizu and cover certificates do not supply the missing
exact multiplication comparison. The best proved actual relation-height
upper bound remains 15237; the sufficient target remains 623.

All 348 child contractions are checked. Among them, 275 have a certified
nonzero denominator slope and a target distinct from the other child.
An explicit reachable cycle supports the proof that finite-dimensional
rational-function spaces closed under every individual child pullback
cannot contain the CM Poisson kernel. This excludes that particular
finite exact-solve proposal. It does not exclude summed cancellations.

**Next proof task:** test a finite exact identity using the summed
transfer operator for one cleared positive-order candidate residual,
or a multiplication-compatible geometric comparison. The report gives
a sufficient tensor identity; a candidate witness is not constructed.
Do not substitute finite congruence, marked automorphism rigidity or
matching invariants for the missing comparison. A height alternative
still needs new actual-curve input.

Exact positive vanishing, candidate identification, P32/B3 markings,
the subsequent cover/Hecke/torsion obligations and the field polynomial
remain open. P1600 and column 0/P6400 are unchanged. All existing
spectral, census, new-level, Hecke and cubic pauses persist.
Sources 626--628 and passing artifacts are frozen;
source 629 is next unused. Earlier checkpoint blocks are historical.
No user decision is pending for this bounded theoretical work.

The two finite jobs pass in about 0.35/0.29 seconds. The review and
completion packet retain the 180-second private-process-group cap,
maximum three mathematical workers, 2 GiB per worker/store and
6 GiB aggregate. Finite checks do not mechanically verify the
companion pole-orbit, functional-identity or geometric proofs.

<!-- End D150 structural identification checkpoint -->


<!-- D149 primitive frame checkpoint -->

**Current reviewed checkpoint: D149 — the primitive-frame comparison closes several isolated repairs; the actual height target 623 remains open.**
The [D149 report](dembele/certificates/P1600-primitive-frame-limits-d149.md),
[fixed review](dembele/data/computed/P1600_primitive_frame_review_d149.json),
[completion record](dembele/data/computed/P1600_primitive_frame_completion_d149.json) and
[source applicability ledger](dembele/data/computed/P1600_primitive_frame_sources_d149.json)
record the proofs, independent controls and inherited provenance.

- The correctly normalized primitive forward pencil map reproduces
  D148's bound exactly. The best proved actual relation-height upper
  bound remains 15237.
- The actual pencil degree is at most -0.4117287, while improving only
  that degree in the frozen estimate would require at least 24.3665.
  Even the favorable pencil endpoint with the field-size term removed
  leaves this majorant above 1162. This is not an actual-height lower
  bound and does not refute the candidate.
- A rank-91 control on an integral nondegenerate curve disproves a
  universal forward cofactor-product cancellation. It does not exclude
  an additional identity specific to the actual CM curve.
- Existing determinant data bound any additional dyadic frame-index
  saving by 986 log(2), less than 684. Refining this index alone cannot
  close the current gap; no additional precision work is admitted.

**Next proof task:** inspect the saved candidate-scheme, canonical-model
and correspondence certificates for an exact automorphic identity or
correspondence with a proved uniqueness implication identifying the
actual marked curve. Reuse established candidate checks. Finite jet
agreement and candidate height do not supply that implication. A new
height comparison must identify an additional actual-curve input.

Exact positive vanishing, candidate identification, the later markings,
cover/Hecke obligations and the field polynomial remain open. P1600 and
column 0/P6400 are unchanged. Existing spectral, new-level, Hecke and
cubic pauses persist. Sources 623--625 and passing artifacts are frozen;
source 626 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the structural certificate audit.

D149 completion: five bounded jobs pass with no new failed attempts.
The two mathematical jobs use independent 192/224-bit ball evaluations
and different rank-91 controls. Finite checks do not mechanically verify
the companion geometric proofs. The 180-second private-process-group
cap, maximum three mathematical workers, 2 GiB per worker/store and
6 GiB aggregate persist.


<!-- D148 forward frame checkpoint -->

**Current reviewed checkpoint: D148 — the actual relation-height upper bound improves to 15237; the target 623 remains open.**
The [D148 report](dembele/certificates/P1600-forward-frame-bound-d148.md),
[fixed review](dembele/data/computed/P1600_forward_frame_review_d148.json),
[completion record](dembele/data/computed/P1600_forward_frame_completion_d148.json) and
[source applicability ledger](dembele/data/computed/P1600_forward_frame_sources_d148.json)
record the proof and independent arithmetic checks.

- The actual fixed-coordinate relation space satisfies
  `h_ext(I_2)<15237`, improving D142's 83240 by more than a factor
  of five. The unrounded upper expression is 15236.599070671391.
  This is still too weak for the sufficient P1600 target 623.
- The proof combines the multiplication-image filtration, with worst
  ranks 17/15/13, and an integral trace-dual forward residue map.
  Symmetric metrics and dyadic frame content are retained. It also
  bounds `R-t_mu<15193`; it does not bound R alone or prove R<=578.
- Removing the entire positive field-vector size term leaves this
  majorant above 11266. Sharpening only that term cannot reach 623.
  This is a limitation of the estimate, not a lower bound on the actual
  height or evidence against the candidate.

**Next proof task:** assess a comparison specific to the actual relation
space, or one using the primitive principal-parts pencil, that avoids
the full rank-91 ambient cofactor-frame estimate. Any cancellation must
retain D119's horizontal order and global normalization. Exact structural
identification remains an alternative.

D147's dyadic multiplication surjectivity and D146's `h_Fal(C)<4.2`
persist. Exact positive vanishing, candidate identification, the later
marking/Hecke/cover obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged. Existing spectral, new-level,
Hecke and cubic pauses persist; no new bank or arithmetic search is
admitted. Sources 620--622 and passing artifacts are frozen;
source 623 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the bounded theoretical work.

D148 completion: five bounded jobs pass. One archived audit attempt
failed on a Sage rational-constructor API call in a control; the fix
and full rerun pass. The mathematical height formulas were unchanged.
Finite checks do not mechanically verify the companion geometric
proofs. The 180-second private-process-group cap, maximum three
mathematical workers, 2 GiB per worker/store and 6 GiB aggregate persist.


<!-- D147 multiplication determinant checkpoint -->

**Current reviewed checkpoint: D147 — dyadic multiplication is surjective; the determinant height comparison remains open.**
The [D147 report](dembele/certificates/P1600-multiplication-determinant-d147.md),
[fixed review](dembele/data/computed/P1600_multiplication_review_d147.json),
[completion record](dembele/data/computed/P1600_multiplication_completion_d147.json) and
[source applicability ledger](dembele/data/computed/P1600_multiplication_sources_d147.json)
record the proof and independent finite checks.

- Actual canonical multiplication has rank 45 on the stable dyadic
  fibre. A pivot-minor calculation and 45 independent cycle-pair
  witnesses prove surjectivity; its dyadic cokernel length is zero.
- The normalized identity is
  `h_ext(I_2)=-4F-delta-60log(2)+R-t_mu`, with `t_mu>=0`.
  Here R retains the Mumford metric, multiplication volume and rational
  residue-frame comparison. Existing bounds make `R<=578` sufficient
  for `h_ext(I_2)<=623`; **R has not been bounded by 578**.
  D142's 83240 remains the best proved numerical height upper bound.
- Orbifold weight-four differentials have dimension 72, with 27 extra
  elliptic principal parts beyond the desired rank 45. Their spectral
  determinant cannot be substituted directly. A determinant-one frame
  control also shows why full-frame volume alone is insufficient.

**Next proof task:** bound the actual combined comparison R using the
CM residue construction and the ordinary bicanonical multiplication
quotient metric, retaining cancellations. An orbifold n=2 approach
first needs its extra principal parts and metric/lattice comparisons.
Exact structural identification remains an alternative.

D146's `h_Fal(C)<4.2` and the closure of the Faltings-only P1600 repair
persist. Exact positive vanishing, candidate identification, the later
marking/Hecke/cover obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged; existing spectral, new-level,
Hecke and cubic pauses persist. No new bank or arithmetic search is
admitted. Sources 617--619 and passing artifacts are frozen;
source 620 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the bounded theoretical work.

D147 completion: five bounded jobs pass. One archived final-review
attempt failed on D99's legacy uppercase status format and was fixed;
both mathematical jobs passed unchanged. Finite checks do not
mechanically verify the companion geometric proofs. The 180-second
private-process-group cap, maximum three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate caps persist.


<!-- D146 elliptic intersection checkpoint -->

**Current reviewed checkpoint: D146 — the Faltings-only P1600 repair is ruled out.**
The [D146 report](dembele/certificates/P1600-elliptic-intersections-d146.md),
[fixed review](dembele/data/computed/P1600_intersection_review_d146.json),
[completion record](dembele/data/computed/P1600_intersection_completion_d146.json) and
[source applicability ledger](dembele/data/computed/P1600_intersection_sources_d146.json)
record the proof and independent finite checks.

- The actual combined elliptic term satisfies `48 < Psi+I < 79`.
  All dyadic intersections on Q are accounted for. Distinct elliptic
  points stay disjoint away from 2 and 3; at 3 the local groups C3
  and S3 give total pair cost between `18log(3)` and `45log(3)`.
- Together with D144's corrected RR identity and D145's spectral
  bound, this proves `h_Fal(C)<4.2`. The target `h_Fal(C)>=29`
  is false, and all three D141 critical height thresholds are excluded.
  Improving only that lower bound cannot repair the existing P1600
  jet criterion. The prior CM/RR source reconciliations remain part
  of the proof; they are not author-confirmed errata.
- The actual relation-space height target `h_ext(I_2)<=623` is
  still open. This result does not refute the recognized candidate.
  Exact positive vanishing, identification, the later marking/Hecke/
  cover obligations and the field polynomial remain unproved.

**Next proof task:** investigate the determinant of the canonical
multiplication sequence in the fixed rational residue frame as a
route to the actual relation-space height bound. Retain integral
indices and archimedean quotient metrics; no bound from this proposal
is yet claimed. D142's jet-row bound 83240 remains too weak. Exact
structural identification remains an alternative.

P1600 and column 0/P6400 are unchanged. Existing spectral, new-level,
Hecke and cubic pauses persist. No new bank or arithmetic search is
admitted. Sources 614--616 and passing artifacts are frozen;
source 617 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the continuing bounded theoretical
investigation.

D146 completion: five bounded jobs pass (primary calculation,
independent audit, fixed review, replay and completion audit);
no D146 job failed. Finite checks do not mechanically verify the
companion geometric proofs or published theorems. The 180-second
private-process-group cap, maximum three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate caps persist.

<!-- D145 spectral feasibility checkpoint -->

**Current reviewed checkpoint: D145 — the proposed spectral target is ruled out.**
The [D145 report](dembele/certificates/P1600-spectral-feasibility-d145.md),
[fixed review](dembele/data/computed/P1600_spectral_review_d145.json),
[completion record](dembele/data/computed/P1600_spectral_completion_d145.json) and
[source applicability ledger](dembele/data/computed/P1600_spectral_sources_d145.json)
record the proof and independent finite checks.

- Every complex embedding satisfies `log Zprime(1) > -41`, hence
  `average(log Zprime(1)) > -41`. D144's proposed sufficient upper
  target `-96.820` is false. The spectral lower bound is independent
  of D144's reconstructed Riemann--Roch constants.
- Exhaustive scalar trace checks give systole `>acosh(25)>3.9`.
  Two independent enumerations through bound 80 check all 4,093 sign
  pairs. The congruence spectral-gap theorem and a positive heat-trace
  argument then prove the bound; no numerical eigenvalues or closed
  geodesic census are used.
- Under the D144 RR identity, `h_Fal(C)>=29` now requires
  `Psi+I < -249`. This is a necessary condition, not a proved or
  sufficient bound. The current joint upper bound is 85.172.
  The desired height itself has neither been proved nor disproved.

**Next proof task:** assess the omitted geometric intersections using
saved derivative contents and local constraints against this necessary
threshold. Exact structural identification remains an alternative.
Do not pursue the false D144 spectral target or increase precision
to address it. No new user decision is needed for this bounded
theoretical investigation.

Exact positive vanishing, identification, marking/Hecke/cover
obligations and the field polynomial remain open. The sufficient
relation-space height bound 623 remains open. P1600 and column
0/P6400 are unchanged. Existing spectral, new-level, Hecke and cubic
pauses persist. Sources 609--613 and passing artifacts are frozen;
source 614 is next unused. Earlier checkpoint blocks are historical.

D145 completion: seven bounded jobs pass (four inputs, fixed review,
replay and completion audit); no D145 job failed. Finite checks do
not mechanically verify the companion proofs or published theorems.
The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate caps persist.

<!-- D144 joint adjunction and compact RR checkpoint -->

**Current reviewed checkpoint: D144 — joint elliptic bound and compact RR normalization reconstructed.**
The [D144 report](dembele/certificates/P1600-joint-adjunction-RR-d144.md),
[fixed review](dembele/data/computed/P1600_joint_RR_review_d144.json),
[completion record](dembele/data/computed/P1600_joint_RR_completion_d144.json) and
[source applicability ledger](dembele/data/computed/P1600_joint_RR_sources_d144.json)
record the derivations and independent finite checks.

- Adjunction bounds the actual combined term `Psi+I < 85.172`.
  Unknown intersections have a favorable sign. The bound uses the
  recovered anchor order-2/order-32 intersection, the saved ordinary
  pairs, marked tail corrections, and derivative integrality at 3.
- The compact comparison has
  `log(C_*)=15log(pi)+(5081/192)log(2)+log(3)-485/64`.
  Its derivation corrects the cone, boundary and metric-adjunction
  factors, with cutoff-independence and a separate Teo spectral check.
  These are our documented source corrections, not author-confirmed
  errata or a claim about cusps. Finite audits do not mechanically
  verify the companion mathematical proofs.
- The remaining sufficient target is
  `average(log Zprime(1)) <= -96.820`, which would prove
  `h_Fal(C)>=29`. This inequality is unproved and untested on C.
  The existing upper height bound also implies the consistency bound
  `average(log Zprime(1)) > -98.900`.

**Next proof task:** derive a certified analytic route to the remaining
spectral upper bound and assess its feasibility before admitting an
actual-curve numerical computation. Exact structural identification
remains an alternative. No new user decision is needed for that
continuing theoretical investigation.

The sufficient targets `h_ext(I_2)<=623` and `h_Fal(C)>=29` remain
unproved. Exact positive vanishing, identification, marking/Hecke/cover
obligations and the field polynomial remain open. P1600 and column
0/P6400 are unchanged. The spectral, new-level, Hecke and cubic pauses
persist; no higher bank is admitted. Sources 606--608 and the passing
bound artifacts are frozen; source 609 is next unused. The failed first
607 attempt is preserved (a path-length control used 28 instead of 20);
its corrected replay passes. Earlier checkpoint blocks are historical.

D144 completion: four bounded jobs pass (primary calculation, independent
audit, fixed review and replay); one failed control attempt is preserved.
The final review/replay took 59.86/59.77 seconds. All scoped whitespace
checks pass. No D144 mathematical worker remains active.

<!-- D143 finite model and elliptic cotangent checkpoint -->

**Current reviewed checkpoint: D143 — finite-model comparison and both missing cotangent bounds established.**
The [D143 report](dembele/certificates/P1600-finite-model-cotangents-d143.md),
[fixed review](dembele/data/computed/P1600_finite_model_review_d143.json),
[completion record](dembele/data/computed/P1600_finite_model_completion_d143.json) and
[source applicability ledger](dembele/data/computed/P1600_finite_model_sources_d143.json)
record the proofs and independent finite checks.

- The actual normalizer model correction is
  `E_model=-(12421/6144)*log(2)`, approximately `-1.401299012`.
  All 58 component-degree identities hold; independent stabilizer and
  graph calculations agree, including the marked rational-tail correction.
  C has good reduction away from 2, so `delta_other=0`.
- The order-3 and order-32 cotangent heights satisfy
  `H_3<3.948`, `H_32<99.372`; the full elliptic cotangent sum is
  `Psi<164.846`. The two CM fields use different applicable height
  theorems, with independent character and field-discriminant checks.
- Under the complete corrected Riemann--Roch comparison, a sufficient
  remaining target is `I+6 average(log(C_* Zprime(1))) <= -486.385`.
  The full intersection bound and corrected global analytic comparison
  remain open. This target is not a proved inequality.

**Next proof task:** control the remaining intersection contribution and
reconcile the complete corrected global RR constant, then assess the
required analytic inequality. An adjunction bound for `Psi+I` together
is worth investigating before computing every intersection separately.
Exact structural identification remains an alternative.

The sufficient targets `h_ext(I_2)<=623` and `h_Fal(C)>=29` remain
unproved. D142's actual upper bounds 83240 and 30.039246 stand, as does
D140's independent recognition. Exact positive vanishing, identification,
marking/Hecke/cover obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged; no higher bank or numerical
spectral work on C is admitted. All six bounded D143 jobs pass,
including two independent input audits and fixed review/replay; no D143
job failed. Sources 601--605 and all bound artifacts are frozen;
source 606 is next unused. Existing pauses and resource caps persist.
Earlier checkpoint blocks and next-task statements below are historical.

<!-- D142 both P1600 height routes investigated -->

**Current reviewed checkpoint: D142 — both D141 height targets investigated; neither proved.**
The [D142 report](dembele/certificates/P1600-two-height-routes-d142.md),
[fixed review](dembele/data/computed/P1600_two_height_review_d142.json),
[completion record](dembele/data/computed/P1600_two_height_completion_d142.json) and
[source applicability ledger](dembele/data/computed/P1600_two_height_sources_d142.json)
contain the derivations and independent finite audit.

- The existing geometry now gives a proved upper bound
  `h_ext(I_2) < 83240` for the actual relation space, in the fixed
  coordinates. Joint ratio-jet bounds improve to 871 and 3532.
  This estimate does not reach the sufficient target 623; it does
  not prove that the actual height exceeds 623.
- Cauchy--Binet improves the actual Faltings upper bound to
  `h_Fal(C) < 30.039246`. The sufficient lower bound 29 remains
  unproved. The Riemann--Roch comparison now retains the metric
  conversion, finite-model difference, cotangent heights, intersections
  and analytic term with their required signs. The local cone correction
  is checked; the complete corrected global constant is not certified.

**Next proof task:** establish the finite Hodge-line comparison for the
actual normalizer and the order-3/order-32 cotangent terms, then assess
the analytic estimate required by the comparison. The report quantifies
that remaining combination; none of its unknown terms is assigned zero.
The current jet-height estimate alone cannot certify the relation-space
target. Exact structural identification remains an alternative.

D140's independent recognition stands. Exact positive vanishing, curve
identification, the later marking/Hecke/cover obligations and the field
polynomial remain open. P1600 and column 0/P6400 are unchanged. No higher
bank or numerical spectral work on C is admitted; existing search pauses
persist. All four bounded D142 jobs pass, including independent audit and
final review/replay; no D142 job failed. Sources 598--600 and the bound
artifacts are frozen; source 601 is next unused. Resource limits are
unchanged. Earlier next-task statements below are historical and
superseded by this checkpoint.

<!-- D141 P1600 proof-gap investigation checkpoint -->

**Current reviewed checkpoint: D141 — two precise sufficient proof targets at P1600.**
The [D141 report](dembele/certificates/P1600-proof-gap-d141.md),
[fixed review](dembele/data/computed/P1600_proof_gap_review_d141.json),
[completion record](dembele/data/computed/P1600_proof_gap_completion_d141.json) and
[source applicability ledger](dembele/data/computed/P1600_proof_gap_sources_d141.json)
record the completed investigation and independent finite audit.
D140's independent recognition of all 91 quadrics remains valid.

- A bound `h_ext(I_2) <= 623` for the true relation space would identify it
  with the recovered space. Here `h_ext` is half the natural logarithm of
  the Gram determinant of a saturated integer basis, in the fixed 136
  monomial coordinates. The certified strict threshold is about 623.347163.
  It is independent of the lattice basis, not of the ambient coordinates.
  The candidate's height 547.226455 does not bound the true space's height.
- A proved `h_Fal(C) >= 29`, in D118's normalization, would make all three
  exact-vanishing tests succeed at the existing P1600 precision. Their
  critical values are approximately 27.304628, 27.749242 and 28.084617.
  This is compatible with the known upper bound 30.970856; the proved
  lower endpoint remains about -23.146370. D120's negative conclusion
  at P200 does not carry over unchanged to the completed bank.

**Neither missing height bound is proved.** Exact positive vanishing,
candidate identification and the field polynomial remain open, as do
the later marking, canonical Hecke and cover/torsion obligations.
Shorter recovered equations improve the old sufficient section thresholds
by only nine valuation units and cannot close that gap by themselves.

**Next proof task:** derive a corrected arithmetic Riemann--Roch comparison
for the actual normalizer curve, retaining finite-model, elliptic-fibre,
metric and analytic terms. Assess whether it can prove the Faltings height
above 28.084618 before admitting numerical spectral work. A true
relation-space height bound at most 623 remains an alternative.
Existing spectral, new-level, Hecke-bank and cubic-search pauses persist.
No higher bank is admitted; P1600 and column 0/P6400 remain unchanged.

Four bounded jobs pass, including independent audit and final review/replay;
two diagnosed failed attempts remain preserved. The review binds 48 direct
sources and traverses D140, D139, D138 and fifteen inherited catalogues
(380,188 hash occurrences, 379,923 distinct files). Sources 593--597,
the report and bound artifacts are frozen; source 598 is next unused.
The three-worker, 180-second, 2 GiB per-worker/store and 6 GiB summed-RSS
limits remain unchanged. Earlier next-task statements below are historical
and superseded by this checkpoint.

<!-- D140 independent P1600 recognition checkpoint -->

**Current reviewed checkpoint: D140 — P1600 independently recovers all 91 candidate quadrics.**
The [D140 report](dembele/certificates/dyadic-P1600-recognition-d140.md),
[fixed review](dembele/data/computed/dyadic_P1600_recognition_review_d140.json) and
[completion record](dembele/data/computed/dyadic_P1600_recognition_completion_d140.json)
record successful discovery without reading the old candidate equations.
One nonanchor CM chart, orders 0–2, and only 96 of 180 usable binary digits
recover 91 independent integer quadrics; an independent 160-digit run agrees.
Their largest coefficients are 968 and 981. Exact unimodular changes of
basis identify both recovered lattices with the old saturated candidate
lattice. Each basis passes all 6,188 independent coefficient checks,
including 5,915 structurally withheld coefficients, with zero mismatches.

There is also an exhaustive coefficient-height certificate: every integer
relation in the 160-digit congruence lattice with maximum absolute
coefficient at most 223,818,092,532,287,707,686,732,450,725,941,069 lies in
the recovered 91-dimensional rational space. This follows from exact Gram
determinants and the full lattice basis; it is stronger than testing the
LLL output. The actual canonical ideal has not been proved to admit
91 integral quadrics below this bound in the fixed residue coordinates.

**Next research task: justify that true-ideal height hypothesis, or identify
the recovered curve by an exact structural argument.** P1600 suffices for
equation recognition. D139's recommendation to make P3200 the default next
action is superseded; its costs remain planning scenarios. No higher bank
is admitted or launched. Exact positive vanishing, marked-base/canonical
Hecke identification, the later cover/torsion construction and the field
polynomial remain open. D138's section-bound gaps and the conditional
P10552 target are unchanged.

Eleven input jobs and both final review/replay jobs pass. Three diagnosed
interface failures are preserved with their logs and source snapshots.
The review binds 80 direct sources and transitively replays D139, D138 and
380,188 inherited hash occurrences (379,923 distinct files). Sources 583–592,
the D140 report and bound artifacts are frozen; source 593 is next unused.
The three-worker, 180-second, 2 GiB per-worker/store and 6 GiB summed-RSS
limits remain unchanged. Earlier next-task statements below are historical
and superseded by this checkpoint.

<!-- D139 indexed receipt and cost checkpoint -->

**Current reviewed checkpoint: D139 — bookkeeping controls, revised costs and final replay pass.**
The [D139 report](dembele/certificates/dyadic-indexed-recost-d139.md), [fixed review](dembele/data/computed/dyadic_indexed_recost_review_r2_d139.json) and [revised cost model](dembele/data/computed/dyadic_indexed_bank_recost_r2_d139.json) record the bookkeeping work following D138. The [completion record](dembele/data/computed/dyadic_indexed_recost_completion_d139.json) confirms six passing bounded jobs; the one diagnosed review-parser failure is preserved.
The new lookup matches all 13,176 checked production receipts. A copied
422-record archive completes in 0.6803 seconds versus the original recorded
157.6806 seconds; both archive interruption/recovery controls pass. The new
coordinator preserves the mathematical schedule and requires a separate,
hash-bound bank admission. Completed arithmetic stores remain frozen.

The recommended next scope is the full P3200 checkpoint: lift columns 1–15,
reuse column 0/P6400, and validate integrated timing after the first column.
Planning scenarios are 38.7–45.7 active hours and 5.0–6.9 GiB additional
retention, with 16.9 GiB free including a 10 GiB reserve. Observed free space
is 54.55 GiB. The remaining staged conditional P10552 bank is 20.8–29.4
active days and 51.4–62.0 GiB additional retention, needing about 72 GiB free.
These are empirical scenarios, not runtime bounds or calendar ETAs. No
P3200-or-higher bank is admitted; a new scope decision and stage-specific
admission/replay are required. Existing three-worker/180-second/2 GiB limits
remain unchanged, and no frozen artifacts are deleted.

The mathematical checkpoint remains D138: full bank P1600, column 0/P6400,
91 quadrics compatible at 17 CM points, zero certified mismatches. Exact
positive-order vanishing, candidate/cover identification and the field
polynomial remain unproved; the conditional target and D134 hypotheses stay
conditional. Source 580 supersedes source 579's first cost calculation.
The failed source-581 review was a phase-name parser error, preserved with
its log and source snapshot; corrected source 582's independent review and full replay pass.
Sources 576–582, the candidate coordinator, report, models and controls must
remain unchanged. Source 583 is next unused. Earlier next-task instructions
below are historical and superseded by this status.

<!-- D138 completed P1600 comparison checkpoint -->

**Current reviewed checkpoint: D138 — the full P1600 bank and comparison are complete.**
The [D138 report](dembele/certificates/dyadic-precision1600-bank-d138.md), [fixed review](dembele/data/computed/dyadic_precision1600_review_d138.json) and [completion record](dembele/data/computed/dyadic_precision1600_completion_d138.json) supersede the running/ETA notes below.
All sixteen columns are certified at least to P1600; column 0 retains P6400.
The fourteen-column D137 run finished 2026-10-07 at 2:36 p.m. Eastern after
22.05 hours, passing 92,946 bounded production/archive/audit/review jobs.
D138's 22 bounded assembly/control/comparison/provenance/review jobs also pass.
The earlier namespace startup failure remains preserved; no revision-2
arithmetic or D138 job failed. The completed coordinators must not be rerun.

All 91 candidate quadrics remain compatible at 17 CM points through orders
0–3. Independent integer-quotient arithmetic checks all 6,188 coefficients
and reports zero certified mismatches. Degree-16 lower bounds are
`[6594, 6545, 6528]`, anchor bounds `[6376, 6048, 5784]`; the remaining
sufficient-bound gaps are `[18561, 18724, 18848]`. Both sets of lower bounds
improved by 1600 from P800. Positive exact vanishing, candidate/cover
identification and a field polynomial remain unproved. Orders 2 and 3 retain
their previous-order exactness conditions; D134's hypotheses remain open.

The final replay checks 380,188 inherited hash occurrences (379,923 distinct
files) through fifteen immutable catalogue roots; the new flat source list
has 315 direct bindings. Sources 569–575, `run_d138_manifest_rechecks.py`,
the report, all passing artifacts and the review are frozen. Source 576 is
next unused. Keep the three-worker/180-second/2 GiB limits. No higher bank
is admitted. Next remove the growing directory-wide receipt-lookup overhead
with bounded controls, then re-cost the next precision stage before a new
scope decision. Do not use the old 15–18-hour forecast as an actual runtime.


<!-- D137 approved P1600 checkpoint running -->

**Current action: the approved full-bank P1600 checkpoint is running (D137, revision 2).**
<!-- D137 progress 2026-10-07 late morning -->
[Progress observed 2026-10-07 10:26 EDT](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_observation03.json): twelve of the fourteen new columns
(2–13) have passed their 24 independent audits and fixed review/replay;
column 14 is running and column 15 remains. Including existing columns 0
and 1, fourteen of sixteen columns now have reviewed precision at least
P1600. There have been no new worker failures since the revision-2 launch.
The revised estimate of approximately 2–3 p.m. Eastern today for the column
run still looks reasonable; common-bank comparison and final review follow.
This is an advisory forecast, not a completion claim. No additional user
decision is needed now. Earlier morning progress is retained in
`dyadic_checkpoint_bank_r2_d137_observation02.json`.

The user's 2026-10-06 “proceed” selected the recommended P1600 checkpoint;
no further scope/storage approval is needed for it. The multiweek P10552
full bank remains unapproved. The [D137 revision-2 admission](dembele/certificates/dyadic-checkpoint-revision-d137.md), [fixed review](dembele/data/computed/dyadic_checkpoint_admission_r2_d137.json) and [admission completion](dembele/data/computed/dyadic_checkpoint_admission_completion_r2_d137.json)
record passing bounded admission and replay over 94,126 hashes.
The first launch exposed the frozen store's required `_d132` suffix before
any store or arithmetic was created. Its failed receipt/log/snapshot and
original configurations are preserved; revision 2 fixes only the interfaces.
The actual revised column-2 storage-creation preflight passed before relaunch.

[launch record](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_launch01.json); [live coordinator log](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_run01.log). Started 2026-10-06T20:33:48.236162+00:00 under a detached coordinator,
with idle sleep inhibited only while it runs. Columns 2–15 are lifted
sequentially from P800 to P1600; existing columns 0/P6400 and 1/P1600 are
reused. Every column gets 24 independent audits and fixed review/replay.
At most three mathematical jobs run globally, with the unchanged 180-second
wrapper, 2 GiB per store/worker measured-RSS admission and 6 GiB summed-RSS
limit. Do not start competing mathematical jobs while this coordinator runs.
D135 forecasts 15–18 active hours and about 3–4 GiB additional retention.
The fixed lifetime working-store bound is 141,761,896 bytes.

The bank coordinator stops after reviewed columns in
`dyadic_checkpoint_columns_completed_r2_d137.json`. Common-P1600 bank assembly,
residue-frame/quadric comparison and final review remain required within this
approved checkpoint scope. Until then the completed full-bank comparison
remains P800. No new exact quadric vanishing, curve identification or field
polynomial is claimed. Earlier “scope decision pending/no run started” notes
below are historical and superseded by this authorization and launch.


<!-- D136 reviewed target-chart checkpoint -->

**Current reviewed checkpoint: D136.**

All 17 integrated P10552 CM chart controls and independent review/replay pass. The largest observed job peak is 1,914,568,704 bytes (1.783 GiB), and the longest job takes 69.749 seconds. The controls use synthetic compatible high digits; they certify no new harmonic precision. Independent byte checks cover all 1,740,800 old CM scalar overlaps. The lossless P6400 CM metadata adapter now supplies the reference interface for the existing weighted seed. Review binds 94,006 hashes, preserving all 93,928 D135 bindings. Freeze sources 562/563, run_d136_chart_controls.py, the passing controls, adapter and reviews. No mathematical worker from this work remains active, and no actual bank has launched. Certified precisions remain P800 for the full bank, P6400 for column 0 and P1600 for column 1. Next prepare lower-column CM adapters and bounded bank provenance review. The D135 scope/storage question is still pending: recommended P1600 checkpoint 15--18 active hours and 3--4 GiB, versus the full target bank at 22--31 active days with at least 80 GiB free after incremental-review design. Source 564 is next unused. Keep all frozen artifacts and the existing three-worker/180-second/2 GiB limits.

See the [target-chart report](dembele/certificates/dyadic-target-charts-d136.md), [cost report](dembele/certificates/dyadic-bank-recost-d135.md) and [completion record](dembele/data/computed/dyadic_target_chart_completion_d136.json).

<!-- D135 reviewed bank-cost checkpoint -->

**Previous reviewed checkpoint: D135.**

D135 cost analysis and independent review/replay pass, preserving all 93,912 D134 hashes. The staged target bank is estimated at 22.0--30.5 active days with at most three workers; these are empirical scenarios, not an ETA or admission. Incremental reviews would put additional retention at about 53--65 GiB; plan for at least 80 GiB free, versus roughly 51 GiB observed. A full-bank P1600 checkpoint is estimated at 15--18 hours and 3--4 GiB. Direct P800/P1600-to-target stores violate the unchanged 2 GiB cap. Next resolve target CM peak memory, seed/CM metadata interfaces and bounded incremental review; a scope/storage preference has been requested from the user. No new harmonic stage or bank has launched. Certified precisions remain P800 for the full bank, P6400 for column 0 and P1600 for column 1. Sources 560/561 and reviewed artifacts are frozen. D136 source 562 is running the finite 17-chart synthetic target-memory controls; source 563 is its drafted review/CM adapter. Source 564 is next unused. Inspect the D136 receipts and control lock before any other mathematical job. Preserve every earlier freeze and the three-worker/180-second limits.

See the [cost report](dembele/certificates/dyadic-bank-recost-d135.md) and [completion record](dembele/data/computed/dyadic_bank_recost_completion_d135.json).

<!-- D134 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D134.**

D134 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. The D134 replay and both reviews pass; its fixed review binds 93,912 hashes and preserves the D133 catalogue. The conditional route uses the odd canonical Jacobian order to fix the F-rational branch half, then D77 cubic inertia to fix its scalar. The marked-base and canonical Hecke hypotheses remain essential. The continuation coordinator has no further mathematical jobs after this checkpoint. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](dembele/certificates/arithmetic-twist-classification-d134.md) and [completion record](dembele/data/computed/arithmetic_cover_criterion_completion_d134.json).

<!-- D133 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D133.**

D133 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. All 24,577 D133 input jobs and both reviews pass. The fixed review binds 93,638 hashes. The completion coordinator next runs the D134 finite replay and review; inspect its live session and receipts before starting any other mathematical job. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](dembele/certificates/dyadic-precision6400-d133.md) and [completion record](dembele/data/computed/dyadic_precision6400_completion_d133.json).

**Execution resumed (2026-10-05):** D133 production resumed from correction
10 after transfer, dependency and lock checks passed. Its continuation
waits to run D133 audits/review and D134. Read [HANDOFF.md](HANDOFF.md) and
the [resumption record](dembele/checkpoints/d133-resume-2026-10-05.json)
before starting any worker. Certified precision remains P800/P3200/P1600;
the three-worker and 180-second caps remain unchanged. Earlier stopping
points below are historical. Source 560 is still next unused.

**Historical stopping point (2026-09-30): D133 paused for transfer to dots.**
Correction 9 and its archive are complete; `ready009`, epoch 20,
`(u,count,bits)=(3497,2903,363)`. Both coordinators are stopped and all
2,682 production/archive receipts pass. The frozen D132 hashes still match.
Read [CHECKPOINT.md](CHECKPOINT.md) for Git LFS, verification and host-specific
resume requirements. D133/D134 are unfinished; certified precisions remain
P800/P3200/P1600 (bank/column 0/column 1). Source 560 is next unused.
Older active-session instructions below are historical; do not auto-start work.

The current objective is to construct an explicit polynomial whose splitting field is
Dembélé's nonsolvable Galois extension of `Q`, ramified only at `2`. The base field is
`F = Q(zeta_32)^+`; the target group fits into
`1 → SL₂(F₂₅₆)² → Gal(K/Q) → C₈ → 1`.

**Historical checkpoint: D132 reviewed; D133 P=6400 column active (2026-09-29).**

All 471 D132 input jobs and both reviews pass. Review 555 binds 18589 hashes,
preserving all 16567 D131 hashes. The complete known P800 column passes
432 phases and twelve corrections, with every final weighted equation,
174 masses, all 217,600 CM scalars and 68 coarse values checked. The same
resumable low phases reach 1319 bits and match the complete D130 reference.
Eight intentional child interruptions recover, including verified archival
of duplicate internal job records. Freeze 547--555 and all bound controls.

The complete single-store budget is 973,167,872 bytes for P6400 and
2,046,552,040 for the conditional target stage, below the unchanged 2 GiB
cap. Archival after each sweep is required. Separate RAM admission uses
measured job peaks; it is not an OS hard limit. D132 admits one actual
P6400 column using sources 554/553. Its initialization is followed by a
planned coordinator pause/resume, then 96 corrections and full weighted/CM
verification. The planned initialization pause completed with 176 passing
receipts; the full run resumed and passed the four seed low-solve stages.
Sources 556/557 and a 24-job independent audit plan are drafted but unrun;
D134 is revisiting the cover step using the odd canonical Jacobian order
and D77's exact B3 fibre criterion. Sources 558/559 draft that route
and remain unrun. Source 560 is next unused.

The completion coordinator is now waiting for production to finish. It will
run the 24 audits, create/replay the D133 review, then execute/review D134
and update all seven entry documents. Its six operational fixture checks
pass without launching mathematical jobs. Inspect sessions 37950
(production) and 32689 (continuation), their locks and receipts before
any restart. No new mathematical job may bypass this three-worker chain.

**Session-close snapshot (2026-09-29, 11:34:55 UTC):** seed and eight
corrections committed; correction 9 underway. All 2,493 inspected saved
receipts report pass, with both coordinator locks held. Processes are
left running; survival after closing the session is unverified. A new
session must inspect completion records, lock ownership and in-flight
work before restarting; tool-session IDs alone are insufficient.
See the [snapshot](dembele/data/computed/dyadic_close_session_snapshot_d133_20260929.json)
and [resume procedure](HANDOFF.md). This is not a new precision certificate.

Until that review, certified precision stays P800 for the full bank,
P3200 for column 0 and P1600 for column 1. Exact base identification,
marked arithmetic covers/Y64 and the original-kernel polynomial remain
open. No automatic full-bank launch. Keep at most three mathematical
workers, unchanged 180-second process-group caps and all prior freezes.
See the [D132 report](dembele/certificates/dyadic-staged-integration-d132.md) and
[active handoff](HANDOFF.md). Earlier next-task statements are historical.

**Previous checkpoint: D131 weighted certificate and row journal reviewed, 2026-09-28.**

All 54 input jobs and both reviews pass. Review 546 binds 16567 hashes,
preserving all 16142 from D130. Freeze 541--546, `run_d131_batch.py`,
bound artifacts and all 24 sealed stores. Source 547 is next unused.
No mathematical worker remains; never rerun completed phases or review creation.

The weighted certificate replays all 4,454,400 uniform/weighted coordinates,
174 masses and 870,400 CM scalars against D129 without another uniform/CM
binary. D129 CM already used weighted inputs; D131 adds streaming/row
authentication and GMP replay. Nineteen abrupt-exit boundaries recover;
four corruption/stale-journal controls reject invalid data. The 22
intentional child exits are passing control events, not failed jobs.
Source 545 freshly recomputes the first D124 P=1600 correction through
the journal: all 44,544 low equations and 1,067,664 new residual scalars
match. Separate ordinary-arithmetic audits are sampled, not full operators.

Next complete the staged driver with resumable low-RHS chunks and
multi-digit factor stages, authenticated low answers before state updates,
one working store, a complete lifetime inventory and separate concurrent
RAM budget. The target logical reservation is 2,035,873,922 bytes under
the 2 GiB per-store cap, including a 64 MiB reserve; this sparse capacity
control is not complete target execution or an aggregate-store/RAM bound.
Select the next actual refinement after integration gates pass. D130's
9--14 ideal three-worker days remains a pre-redesign baseline, not an ETA.

Full bank P=800, column 0 P=3200, column 1 P=1600; no precision increase,
positive exact zero, base identification or field polynomial. Marked
arithmetic X/Y64, combined torsion and global F256 action remain open.
Keep original kernels, all freezes and pauses, at most three mathematical
workers, runner 272's unchanged 180-second private-process-group cap,
assertions and one BLAS thread. Inspect receipts/partials after disconnects.
Continue the recorded bounded work autonomously. No correspondence.
See the [D131 report](dembele/certificates/dyadic-weighted-journal-d131.md)
and [handoff](HANDOFF.md). All earlier next-task ordering is historical.

**Previous checkpoint: D130 feasibility reviewed, 2026-09-28.**

D130 completes the target feasibility controls and arithmetic construction
specification. All 137 input jobs and both fixed reviews pass; one failed
budget-script attempt is retained and resolved. Review 540 binds 16142
hashes, preserving every one of D129's 15600. Freeze 533--540,
`run_d130_batch.py`, their successful artifacts, reports and ledger.
No actual precision increases: the complete bank remains P=800,
column 0 P=3200 and column 1 P=1600. Exact candidate identification
and the original-kernel polynomial remain open.

The empirical model favors staged refinement: roughly 9--14 ideal
three-worker days, before extra I/O and contention; these are scenarios,
not bounds or an ETA. The inherited storage protocol fails the 2 GiB
scratch cap even at P=6400. Compact final retention alone does not fix it.
A new weighted-only fixed-point deduction gives a concrete redesign:
T Q=T and Q T(w)=w imply that T(w) is a uniform fixed point. Review 540
checks the required divisibilities on all 348 original and 34 composed
CM maps. Its implementation and full D129 replay are the next task.

Source 541 is next unused. Implement that replay and a resumable row
journal that retains one weighted state and two scaled residual slots,
with generation-bound streaming/per-row authentication. Inventory every
phase and inject interruption/corruption controls before an actual lift.
Keep the unchanged 180-second process-group cap and at most three workers.
The marked arithmetic cover and Y64 section construction remain separate
research tasks: the new unit 1+b is globally nonsquare yet locally square
at the saved norm-31 place, so local agreement does not determine the
arithmetic double-cover twist. No automatic precision doubling is admitted.

See the [feasibility report](dembele/certificates/dyadic-target-feasibility-d130.md) and
[arithmetic construction specification](dembele/certificates/arithmetic-construction-d130.md).
Earlier next steps below are historical.

**Previous checkpoint: D129 actual P=3200 reviewed, 2026-09-28.**

One actual harmonic column now reaches P=3200. All 4,454,400 original
residual scalars, old overlaps, exact masses, 17 CM charts and 22 independent
audit jobs pass. All 1934 input jobs and both fixed reviews pass. Review 532
binds 15600 sources and preserves all 9648 D128 hashes. Peak scratch is
1,229,041,837 bytes under the enforced 2 GiB cap; the highest measured single-process
input peak is 491,929,600 bytes. Four sealed state payloads total 558,829,536 bytes.
Freeze 528--532, both operational schedulers and all bound artifacts.
Column 1 remains P=1600 and the complete bank P=800. Exact vanishing,
candidate identification and the target field polynomial remain open.

D129 plan (superseded by D130): the [stocktake after D129](dembele/certificates/stocktake-2026-09-28.md)
retains the dyadic route and makes exact genus-16 identification the next
major mathematical milestone. Source 533 onward should cost the complete
P=10552 certificate, including all columns, CM/frame/quadric arithmetic,
verification and retention, and compare staged/direct schedules. Specify
the downstream marked-cover and arithmetic Y64 construction alongside
that budget before a long full-bank commitment. No automatic next precision
doubling; the target cost and eventual field polynomial remain open.
Keep the three-worker, 180-second process-group limits and all freezes.
See the [report](dembele/certificates/dyadic-precision3200-d129.md) and current handoff. Earlier next steps are historical.

**Previous checkpoint: D128 selective scaling reviewed, 2026-09-28.**

Selective serial controls match over 305 million bytes of saved actual
P=1600 data, with assembly peak 366 MB. Precision-3200 original-map
samples agree between adaptive and GMP backends in all 926,352 scalars;
all sampled old actual overlaps pass. All 13 input jobs pass; review 527
binds 9648 sources and preserves all 9599 D127 hashes. Freeze 525--527
and bound artifacts. These are implementation controls: no actual P=3200
column or new streamed binary writer has run. The full bank remains
P=800, columns 0 and 1 P=1600; the field polynomial remains open.
Next: source 528 onward for one actual P=3200 rolling column, integrating
selective serial phases, small chunks and existing-factor residual lifts.
The prospective 1,510,359,376-byte scratch inventory fits a proposed
2 GiB cap; the new driver must enforce it. Retain full original residuals,
CM and independent audit. Complete P=10552 cost remains unestablished.
See the [report](dembele/certificates/dyadic-selective-scaling-d128.md) and current handoff. Earlier next steps are historical.

**Previous checkpoint: D127 rolling pilot reviewed, 2026-09-28.**

The complete rolling P=800-to-P=1600 refinement for column 1 passes,
including every original equation, CM values and four independent audits.
Peak scratch is 308,327,101 bytes under the 512 MiB cap; retained payloads
are 140,237,736 bytes. Serial assembly still peaks at 1.117 GB of RAM.
All 235 input jobs pass; review 523 binds 9599 hashes and preserves all
8816 D126 hashes. Freeze 519--524 and all bound artifacts/sealed scratch.
Columns 0 and 1 reach P=1600; the full bank remains P=800. Exact vanishing,
curve identification and the field polynomial remain open.
Existing half-precision factors now pass low-system solves at P=3200,
so a new P=3200 factor is unnecessary. Next use source 525 onward to
control selective serial assembly/preparation and P=3200 transport/RHS
chunks, then inventory resources before a larger actual column.
The complete P=10552 solve remains uncosted. See the
[report](dembele/certificates/dyadic-rolling-pilot-d127.md) and current handoff. Earlier next steps are historical.

**Previous checkpoint: D126 resource controls reviewed, 2026-09-28.**

Resource controls now pass: both complete P=1600 original sweeps use
selective reads, every weighted coordinate agrees, and all 25 rolling
checkpoints survive the interruption/corruption controls. Streamed low
factors reduce the two-RHS peak from 786 MB to 293 MB; combined actual
low solves pass for two harmonic columns and a saved correction.
All 22 input jobs pass. Review 518 binds 8816 sources and preserves all
8729 D125 hashes. Freeze 514--518, their outputs and the sealed scratch.
The full bank remains P=800, one column P=1600. Exact vanishing, curve
identification and the field polynomial remain open. Next: integrate a
complete rolling P=1600 column-1 refinement with a proven/enforced
512 MiB total scratch ceiling, full original residual and direct CM.
Transport arithmetic remains the main measured cost; a larger full bank
and the complete P=10552 solve still require costing. See the
[report](dembele/certificates/dyadic-resource-controls-d126.md) and current handoff. Source 519 is next unused.

**Previous checkpoint: D125 P=800 full bank and comparison reviewed, 2026-09-28.**

The complete sixteen-column bank is now certified at P=800, including
all original residuals and CM values. All 6188 quadric coefficients still
contain zero, and independent audits find no mismatch. Section bounds
improve to 4994/4945/4928, against sufficient 25255/25369/25476; exact
vanishing and the target polynomial remain unproved. W Gaussian remains
nonzero at valuation 1024, now with error 2025, and is uninverted.
All 1250 input jobs pass. Review 513 binds 8729 hashes and preserves all
3535 D124 hashes. Freeze successful 505--513, both coordinators and bound
outputs. Next: selective state reads and a controlled rolling scratch
protocol, starting with a P=1600 control in new source 514, before another
larger full bank. Existing frozen artifacts remain preserved.

**Previous checkpoint: D124 P=1600 pilot and controls reviewed, 2026-09-28.**

One actual column now reaches P=1600 with all original residuals, CM
charts, old overlaps and four independent audits passing. All 242 input
jobs pass under the 180-second cap. Review 504 binds 3535 sources and
preserves all 2532 D123 hashes. The full sixteen-column bank remains
P=400, so section and Gaussian bounds are unchanged. Direct weighted CM
is validated against every P=800/P=1600 CM moment; a compiled small-product
path passes independent controls. Freeze 496--504, their coordinator and
bound report/ledger. Next: combine these improvements in new source 505,
complete columns 1..15 at P=800, reuse column 0, then recompute and audit
the full frame and quadrics. No field polynomial is yet constructed.

**Previous checkpoint: D123 P=800 pilot and weighted correction reviewed, 2026-09-27.**
Read the top of `HANDOFF.md` and `dembele/certificates/dyadic-staged-pilot-d123.md`.
One actual harmonic column and all seventeen CM charts reach P=800;
coarse beta-errors are [1632,1648,1632,1664]. The complete bank remains
P=400, so all D122 section and Gaussian bounds remain unchanged.
No positive exact quadric zero, candidate identification or field polynomial.

The weighted error lattice v_pi(e_k)>=P-k is killed by the original T
modulo pi^P. Certify its residual, then apply T once to reconstruct
uniform moments. Source 493 uses full precision for moments 0..32,
weighted precision above them, and shrinks active indices to k<P-u.
Twelve corrections from the saved uniform seed reproduce the verified
column. Its serial timing excludes seed construction; do not compare it
as an elapsed speedup against the parallel uniform run. All intermediate
states/residuals agree; independent sources 491/494 pass. All 148 input
jobs pass. Review 495 binds 2532 hashes, preserving all 1884 D122 hashes.

Freeze 488--495, both new coordinators and bound artifacts. Replay
495 --check through the persistent capped wrapper with a fresh stem;
never rerun either completed coordinator. All workers have finished.
Next combine weighted storage and shrinking bands with state chunks,
then measure one P=1600 column from verified P=800 with r=32, including
factor, seed, correction, original residual, CM and peak memory costs.
Source 496 is next unused; no larger job or combined driver exists yet.
Retain all caps/pauses, D99/D108, D120's conditional target, preceding
exact-zero hypotheses and downstream cover/field tasks. Continue
autonomously; inspect receipts after a chat disconnect before retrying.
Earlier next tasks below are historical.

**Previous checkpoint: D122 comparison and independent review complete, 2026-09-27.**
Read the top of `HANDOFF.md` and `dembele/certificates/dyadic-precision400-d122.md`.
Sources 483--484 are now executed successfully and frozen. Source 486's
seven independent phases validate all 1088 coarse values and 6188 quadratic
coefficients; none is certified nonzero. Review 487 binds 1884 sources in
the completed audit, preserving all 1079 D121 and 1844 interim hashes.
All 167 input receipts pass. Source 485 is only the historical provenance checkpoint.

Current section lower bounds: 4194/4145/4128; anchors: 3976/3648/3384;
sufficient non-anchor bounds with those anchors: 25305/25419/25526.
Higher intrinsic jets remain conditional on preceding exact zeros.
W's Gaussian is now certified nonzero, valuation 1024 with absolute error
1225. It has not been inverted; any later division must carry this error.
Do not repeat the historical claim that it is unresolved. No positive
exact quadric zero, candidate identification or field polynomial is proved.

Next generalize the lift and checkpoint original-operator sweeps by state
chunks, then cost one actual P=800 column from P=400 with r=32, including
all residual and CM work. Source 488 is next unused; no generalized driver
or P=800 computation exists yet. A full target-size solve remains uncosted.
Freeze 476--487 and bound files. Use the persistent capped wrapper and
487 --check with a fresh receipt stem; do not rerun completed 483/484.
All jobs have completed. After a chat transport error, inspect saved
receipts and outputs before replacing a job. Continue without an approval
pause. All resource pauses, D99/D108, D120's conditional target and remaining
marked-cover/field tasks stand. Earlier next steps below are historical.


**Previous interim checkpoint: D122 complete P=400 bank; comparison and audit pending, 2026-09-27.**
Read the top of `HANDOFF.md` and
`dembele/certificates/dyadic-precision400-progress-d122.md`.
All sixteen actual harmonic columns and seventeen CM charts now reach
P=400, with four coarse beta-errors [832,848,832,864]. Source 482's
consolidated artifact is `dyadic_precision400_d122.json`. The algebraic
CM frame eta has beta-error 21168; actual harmonic moment precision is
still P=400. All 155 computation jobs pass, and no jobs remain running.

Sources 483--484 are **unrun, unfrozen drafts**. Resume with the exact
handoff commands: recheck 485's fixed manifest, run 483 for the residue
frame, inspect its receipt, then run 484 for the quadrics and updated
anchor-dependent height thresholds. Independent mathematical review
is pending; 486 is the next unused source number. Source 485 only checks
provenance/completion, binding 1844 sources and preserving all 1079 D121
hashes and 155 input receipts. Its checkpoint and hash replay both pass.
Do not describe it as the independent mathematical review.

Freeze successful sources 476--482, completed outputs and the bound
report/ledger. Use persistent `dembele/pari/run_dyadic_capped.py`, fresh
receipt stems, assertions enabled, one BLAS thread and the 180-second
private-process-group cap. No temporary runner or completed-column restart
is needed. No new approval pause is needed for the recorded next tasks.
D118's accepted section bounds remain current until the comparison;
W's Gaussian remains unresolved and uninverted. No positive exact zero,
candidate identification or field polynomial is proved. Keep D99/D108,
D120's conditional P=10552 target, all resource pauses and downstream
requirements. Decisions and references are current; earlier next tasks
below are historical.


**Previous checkpoint: D121 Schur solver and actual precision lift, 2026-09-27.**
Read the top of `HANDOFF.md` and `dembele/certificates/dyadic-schur-lift-d121.md`.
All 399 transports have certified P=10552 parameters. Low-moment Schur
iteration is implemented and checked through r=64. One actual harmonic
column now has P=400 state and CM moments and four coarse coefficients
with beta-errors [832,848,832,864]. The full sixteen-column bank remains
at P=200. No exact quadric zero, curve identification or field polynomial.

Next accelerate the polynomial backend and complete all sixteen columns
at P=400 before a target-size lift. Current target-size per-action costs
still make full sweeps expensive. Review 474 binds 1079 sources and
preserves all 961 D120 hashes. Freeze 464--475 and bound artifacts;
use 474 --check through runner 272 and the 180-second process-group cap.
No approval pause is needed. All resource pauses and downstream
requirements remain; decisions and references are current.


**Previous checkpoint: D120 reassessment, precision design and norm-97 isolation, 2026-09-26.**
Read the top of `HANDOFF.md` and `dembele/certificates/construction-reassessment-d120.md`.
Keep D118's direct section certificate. The complete D119 inverse-frame
bound is worse, and h_Fal<30.970856 rules out rescuing the current D118
bound by improving that input alone. No positive exact zero, candidate
identification or field polynomial is proved.

A proved error-propagation design gives conditional sufficient P=10552,
provided refined quadric enclosures contain zero. The actual bank remains
P=200. New polynomial/GMP transport implementations reproduce 332800
scalar coefficients on one harmonic column. A synthetic target-size
action passes in 50.408 seconds; a complete large run is not ready.
Next implement r=1 low-moment elimination on P=200, check the original
residual and precision gains, and price its 174-dimensional low-block
solve and streaming storage. Do not launch thousands of full sweeps.

Existing Hecke data now prove norm-97 cofactor separation in canonical
Y64. The first target has order 51 and is the second T31 system; the
other has order 257. The curve/cover realization, genus-64 degree-51
torsion backend, global F256 action and field invariant remain open.
Review 462 binds 961 sources, preserving all 922 D119 hashes. Seven
input jobs pass and one caught norm-97 expectation error is archived.
Freeze 458--463 and bound files; recheck 462 --check through runner 272.
All resource pauses and the 180-second private-process-group cap stand.
Decisions and references are current; proceed autonomously.


**Previous checkpoint: D119 actual Cartier CM divisor and dyadic residue index, 2026-09-26.**
Read the top of `HANDOFF.md` and `dembele/certificates/cm-cartier-frame-d119.md`.
The actual divisor is finite flat Cartier on the minimal regular model.
Eight ordinary pairs intersect with length 33 each; the anchor is disjoint.
Its algebra is R x product_8 R[t]/(t^2+4*(2+b)), with normalization index
264 and discriminant valuation 528. It is not the abstract field order.

The principal-parts matrix has Smith valuations [0x9,2x7]. Its H1 torsion
has length 14, the primitive principal-part norm has valuation 2, and
the residue map has index valuation 16. Its cokernel is (R/(beta^2))^8,
so beta^2 clears the local frame for a primitive pencil generator.
The earlier evaluation defect 245 is a different quantity.

D119 gives a lower bound for the pencil line in its induced metric,
not yet a replacement quadric bound. Next derive the full inverse-frame
norm and quadratic-section budget, keeping the codifferent and finite
clearing in that normalization. Compare degree minus measured zeros
with D118; do not count known vertical content twice. Non-dyadic residue
indices and a global choice of h remain uncomputed.

Sufficient section valuations remain **25330/25444/25551**, actual
**3794/3745/3728**. No positive exact zero, curve identification or field
polynomial follows. Review 457 binds 922 sources, preserving all 911
D118 hashes. Corrected computation and independent probe/final audit
pass; one graph-count failure is archived. Freeze 456--457 and bound
files; recheck 457 --check through runner 272 and its 180-second cap.
Retain the P=200 bank, D99/D108 and all resource pauses. Decisions and
references are current; downstream cover and field tasks remain open.


**Previous checkpoint: D118 finite CM height and tropical Faltings correction, 2026-09-26.**
Read the top of `HANDOFF.md` and `dembele/certificates/cm-finite-height-d118.md`.
The combined dyadic Hodge/ramification correction is now computed exactly:
contents [280,17x16] give (69/34)*log(2), lowering H_CM below 8/3.
The existing reduction graph has tropical moment 223268/27075; the
de Jong--Shokrieh formula improves the Faltings lower bound above -23.146371.
No auxiliary level or new graph was computed.

The current sufficient section beta-valuations are **25330/25444/25551**,
versus actual **3794/3745/3728**. Use `cm_arithmetic_height_budget_d118.json`.
Source 452's fibre-only bounds are intermediate. Higher intrinsic jets
require preceding exact zeros. No exact curve or field construction follows.

Review 455 binds 911 sources, preserving all 891 D117 hashes. All four
input jobs and the independent probe/final review pass. Freeze sources
451--455 and bound artifacts; recheck 455 --check through runner 272.
The dyadic correction is fully counted; separating its two terms cannot
improve the total. Common vertical content already in measured jet
valuations cannot be counted again as a height gain.

Next test a lower-degree integral frame using D102's principal-parts
sequence, first checking an actual Cartier CM divisor, intersections,
principal-part norm and cohomology torsion. The evaluation defect 245
is not that index. No smaller bound from this alternative is yet proved.
Retain the P=200 data, D99/D108 and every resource pause. Decisions and
references are current; downstream cover and field tasks remain open.


**Previous checkpoint: D117 uniform CM disks and arithmetic exactness, 2026-09-26.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-disk-and-exactness-d117.md`. A uniform arithmetic
CM projection-lattice argument certifies embedded disks with radius squared
3/5 at every CM point and conjugate. The direct integral-section thresholds
fall to **35947/36096/36237**, versus actual lower bounds **3794/3745/3728**.
Use `cm_uniform_disk_budget_d117.json`. Higher intrinsic jets still require
preceding exact zeros. No positive jet, curve identification or field
polynomial has been proved.

The exact CM lattice search has 376935 vectors. Independent support-pattern
enumeration, multiplication traces, root sign checks and a separate logarithm
series agree. Review 450 binds 891 sources and preserves all 868 D116 hashes.
Four input jobs pass; one serialization failure is completely archived and
fixed by certified outward rounding. Freeze sources 446--450 and bound files;
recheck 450 --check through runner 272 and its 180-second process cap.

Even rho=1 with the other inputs fixed leaves thresholds 32928/33064/33193.
Further disk refinement alone cannot certify the current data. Next compute
proved dyadic contributions to D104's ramification-derivative zero degree
and Hodge/stable lattice correction, after proving the upstairs integral
generators. Neither correction is currently computed. Assess their effect
before selecting further precision; a large run requires a different costed,
limb-safe implementation and transport refinement. Keep the frozen P=200
bank, D99, D108 and every resource pause. All downstream cover and field
requirements remain open. Decisions and references are current.


**Previous checkpoint: D116 integral quadric identification criterion, 2026-09-26.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-compound-height-d116.md`. The preferred certificate
uses Q(s)/Delta as an integral quadratic section. Complementary minors
give tensor norm below 2^4855; successive vanishing jets need non-anchor
beta-valuations **119806/120284/120758**, including measured anchor bounds.
Actual lower bounds are **3794/3745/3728**. These are section valuations,
not ratio-error digits. Higher intrinsic jets require preceding jets
to vanish exactly. No positive jet is proved zero and no curve or field
identification follows yet.

All four required coarse coefficients are now computed. Source 442 uses
the frozen P=200 bank to give errors 432/448/432/448 beta-digits; all 1088
entries are nonzero. Source 443 evaluates all 91 quadrics at all 17 points
through order three. Review 445 independently checks the 272 third coarse
coefficients and 4641 positive quadratic coefficients. Exact four-term
vanishing would identify (C,D) by 68>60, without a rank-45 prerequisite.

The harmonic basis is saturated and its weighted residues c_e/|Gamma_e|
are unimodular graph cycles. The report's nodal-residue proof identifies
it with the stable integral differential lattice. Fibre exponents are
296/33, cofactor valuations 280/245, Delta has valuation 4200 and the
common D103/D115 section factor has valuation 3920. The evaluation defect
245 is not the uncomputed horizontal CM residue-map index.

The alternative ratio method now has sufficient beta-error bounds
132444/524481, versus achieved 101/70. Actual J3 rank is at least 33;
candidate-centered +96-beta rank-45 trials are predictions only. W's
Gaussian remains unresolved numerically and must not be inverted.
The next task is a sharper effective bound for the actual reduced
quadratic tensors or an exact identity with uniqueness. A large precision
run needs a costed, limb-safe implementation and transport precision;
another small precision pilot is not the default plan.

Review 445 binds 868 sources and preserves 814 D115 hashes. Freeze sources
432--445 and bound artifacts; use 445 --check through runner 272 and its
180-second process cap. Input jobs, the audit and its recheck pass. Sources 435/440
are probe-only predecessors; source 444 supersedes 441's looser bound.
Retain D99, D108's spectral rejection and all resource pauses. Marked
cover, cubic/section, torsion and final polynomial tasks remain open.
Decisions and references are current; earlier next steps are historical.


**Previous checkpoint: D115 actual rational-frame comparison and revised strategy, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/dyadic-comparison-and-strategy-d115.md`.
The user's request for reassessment and continued execution has been
carried through to an actual two-order comparison. W is resolved,
the harmonic-to-rational-residue frame is computed, and the chosen
Gaussian is certified at all sixteen non-anchor CM points. Actual
ratio coefficients agree with the candidate within beta-errors **101/70**
for orders 1/2. This is not exact curve identification or a field polynomial.

Full Eisenstein arithmetic, batched operators and correction-only
refinement reach moment precision 200. The final bank has 1,667,616
state and 108,800 CM A-chart entries, with coarse errors 432/448/432
beta-digits. The first W leading coefficient has beta-valuation 296.
The same splitting root is refined to error 352; normalized transport
errors are 331/337. No arithmetic labels or quotient data are changed.

Use `dyadic_comparison200_d115.json` for the actual frame and ratio
coefficients and `dyadic_precision200_d115.json` for the harmonic jets.
W's Gaussian remains numerically unresolved; nonvanishing on the whole
CM divisor follows qualitatively from the rational frame and transitivity.
No division by an unresolved local ball is allowed. Reviews 428/430
check the moments/kernels and independent formal-series reversion.

The revised priority is **exact arithmetic identification**, rather than
another default precision pilot. At the degree-16 place, the current
height bounds require beta-errors 274241/820774, or integer pi-errors
137121/410387. A sharper effective bound on the actual unknowns or an
exact identity with uniqueness is still needed. Finite matching and
candidate-only heights do not close this gap. Downstream marked-cover,
global cubic and target-torsion requirements remain open.

Review 431 binds 814 sources and preserves all 713 D114 hashes. Four
implementation probes are archived; the corrected runs and independent
reviews pass. Freeze sources 417--431 and bound artifacts. Recheck
431 --check through runner 272 and its 180-second cap. Keep D108's
spectral rejection and all census/level/Hecke/cubic resource pauses.
Decisions and references are current; earlier next steps are historical.


**Previous checkpoint: D114 actual coarse differential jets and anchor precision gate, 2026-09-25.**
Read the top of `HANDOFF.md` and `dembele/certificates/dyadic-coarse-d114.md`.
Sources 414--416 compute the actual harmonic-basis coarse differential
2-jets at all seventeen CM points, in u=((z-beta)/(z+beta))^2.
The first three coefficient errors are 32,40,32 pi-digits; every
one of the 256 non-anchor entries per order is certified nonzero.
At W the valuation lower bounds are 32.5,40.5,32.5, with no exact
vanishing or nonvanishing conclusion. Rational-frame ratio jets,
frame change, a Gaussian pivot and candidate identification remain open.

The extended bank has 130,848 state entries through degree 46 and
26,112 CM entries through degree 31, all modulo pi^16. Only the
low-degree fixed system is solved; higher rows use its solution.
Independent moment arithmetic and rational-kernel expansion verify
the evaluation. The CM involution exchanges A=pi*O_K with its
complement, giving g_j=2*integral_A K_j dmu. This yields the stronger
errors above; use `certificates.Poisson.symmetry_refined_CM_values`
in `dyadic_coarse_review_d114.json`. The initial three-chart artifact
remains frozen with its weaker bounds 24,32,24.

At W, degrees 0..31 on A vanish modulo pi^16. Monic division by
(X^2-X)^16 proves this for all integral polynomial moments. More
degrees at the same precision cannot resolve the anchor. Next raise
working precision to 24, with low cutoff 23, iterations 24, state
cutoff 70 and CM cutoff 47, initially focusing on W's A chart.
The coarse design errors are 40,48,40 pi-digits; nonvanishing is
not guaranteed. Implement the full Eisenstein quotient in a new
source: the pi^8=-2 shortcut omits a term of valuation 20. Use
sufficient CM precision, check overlap with the frozen bank, and
retain existing transport centers and the 180-second cap.

Review 416 binds 713 sources and preserves all 696 D113 hashes.
One implementation-only failed probe is archived; corrected probe
and final review pass. Freeze sources 414--416 and bound artifacts;
recheck 416 --check through runner 272 using Python/NumPy.
No normalization or target polynomial is obtained. Actual frame
change, cofactor propagation, a Gaussian pivot and dyadic equality
thresholds remain needed. Retain D108's spectral rejection and all
resource pauses. Decisions and references are current; earlier next
steps are historical.


**Previous checkpoint: D113 actual positive moments by finite contraction, 2026-09-25.**
Read the top of `HANDOFF.md` and `dembele/certificates/dyadic-moments-d113.md`.
Sources 411--413 certify a finite moment recursion on the existing
174 edge charts. All 348 child maps contract by pi and cover the
two residue balls; all 51 CM chart maps are certified isomorphisms.
Their normalized errors are at least 159 and 165, respectively.

For the child maps, [x^k]phi(x)^n has valuation at least k. With
the exact zeroth masses and d=0, the positive-moment operator gains
one pi-digit per iteration. The direct ramified-field proof gives
error min(J+1,N,P), without importing a Qp control theorem.
The pilot J=11, N=P=12 produces 33,408 state moments. CM degrees
1,2,3 have errors 11,10,9; 2043 of 2448 entries are certified nonzero.
The 144 positive entries at W are all zero modulo their bounds;
this does not prove exact vanishing or permit normalization there.

Review 413 uses independent polynomial arithmetic for every
fixed-point residual and CM transfer, plus 32 independently reduced
leaf balls for direct integration checks. It binds 696 sources,
preserving all 682 D112 hashes. All jobs pass first attempts.
Freeze sources 411--413 and bound files. Recheck 413 --check through
runner 272 with Python/NumPy and the 180-second cap.

Next run a modest actual coarse-Poisson pilot using D108: target
T=16, CM cutoff 31, state cutoff 46, precision/iterations 16. Solve
the low-degree state system and obtain higher moments by row
evaluation, since columns k>=P vanish modulo pi^P. Keep the current
sources frozen. The bit-plane quotient shortcut is restricted to
P<=16; larger P needs the full Eisenstein arithmetic. Certify a
nonzero coarse value at W before normalizing. Actual frame change,
cofactor propagation, a Gaussian pivot and dyadic equality thresholds
remain needed. No actual differential value/jet, candidate
identification or target polynomial has been obtained. Retain
D108's spectral rejection and all resource pauses. Decisions and
references are current; earlier next steps are historical.


**Previous checkpoint: D112 dyadic CM coordinates and arithmetic frame matching, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/dyadic-cm-matching-d112.md`.
W and the sixteen signed ordinary reversed-edge embeddings have
exact fixed-point charts S*(beta:1), beta^2=-(2+b). All relative
ideal classes have independent principal witnesses. The norm-one
unit k exchanges W's fixed points, identifying its orbit with the
unique K-rational point of the CM divisor.

The local branch is normalized by W's CM eigenvalue character.
Canonical CM reciprocity and prime-to-p adelic equivariance give
the arithmetic Artin labels; the report states this geometric input.
The class action of sigma(beta)=beta^3+3*beta is exponent 10.
Its root cycle and D107's exact resolvent independently fix the
root-label direction. All seventeen Hensel roots have errors at
least 688 beta-digits; the rational residue-frame values have errors
at least 384 beta-digits = 192 pi-digits. These are algebraic frame
entries, not actual harmonic differential evaluations.

All 51 actual boundary-chart zeroth masses are certified, with
A0=0 and B0+C0=0. At the anchor eta1=theta-2/17 has v2=7; preserve
this cancellation in later division bounds. Review 410 binds 682
sources and preserves all 661 D111 hashes. One failed expected-
valuation probe is archived; the corrected probe and final review
pass. Freeze sources 407--410 and bound artifacts. Recheck with
410 --check through runner 272 and its 180-second cap.

Next derive finite positive-moment transport/recursion in these
charts with a proved ramified-field error/contraction bound, then
run a bounded pilot. D111's d=0 is available; positive-degree
moments, the actual harmonic-to-residue change of basis, a Gaussian
pivot and dyadic equality thresholds remain needed. No actual jet,
candidate identification or target polynomial has been obtained.
Retain D108's spectral rejection and all resource pauses. Decisions
and references are current; earlier next steps are historical.


**Previous checkpoint: D111 arithmetic edge reduction and harmonic cocycles, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/dyadic-harmonic-d111.md`.
All adjacency transports and stabilizers for the existing 58 classes
are certified: 174 outgoing entries and 164 projective stabilizer
elements. Exact local frames, p-supported indices and localized
membership prove the global ideal and sandwich assertions. The matrix
and stabilizers match D99; the order and splitting remain D109's.

There are 16 actual G-invariant scalar harmonic cocycles, given by
integer vectors in 174 slots. The 376 relations have rank 158.
All nine inverted edge orbits have value zero. Basis coefficients
have absolute value at most four and the measure denominator bound
is d=0. Source 405 gives terminating arithmetic edge reduction with
adaptive precision on the same Hensel root. Tests cover depth 32,
reversal, harmonicity and invariance under u, W and h.

Review 406 binds 661 sources, preserving all 643 D110 hashes.
All five bounded jobs passed on first attempts. Freeze sources
403--406 and bound artifacts; recheck with 406 --check through runner
272 and the 180-second cap. No connected fundamental subtree or
group presentation is additionally claimed.

Next certify W's dyadic fixed points and coordinate change to the CM
model, then match the embedding/orientation to the seventeen saved
labels and rational residue frame with arithmetic evidence. Follow
with a bounded actual moment pilot and a proved ramified-field error
bound. No moment bank, CM/frame match, actual jet, candidate
identification or target polynomial has been obtained. Retain D108's
spectral rejection, all resource pauses and the 180-second cap.
Decisions and references are current; earlier next steps are historical.


**Previous checkpoint: D110 explicit dyadic group and moving-vertex transports, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/dyadic-group-transport-d110.md`.
The group G=O[1/b]*/O_F[1/b]* has norm-parity kernel Gamma=image(O[1/b]^1).
Its odd coset represents w_p in the geometric dyadic uniformization.
The existing 58-class matrix and stabilizers match D99 entry for entry;
the order basis matches D109. Seven exact ideal correspondences give
W=(1+b/2)i+cj, c=(b^7-7b^5+14b^3-7b)/2, with W^2=-(2+b).

W is a projective involution moving the base vertex seven edges.
For D109's unit u, g=WuW^(-1) has norm one, projective order three,
and displacement fourteen. The product h=ug is hyperbolic of translation
length fourteen. Exact localized membership, conjugation, matrix-error
bounds and target lattices are certified. No complete generating set
or full fundamental domain is claimed. Review 402 binds 643 sources,
preserving all 629 D109 hashes. All four jobs passed on first attempts.
Freeze sources 400--402 and bound artifacts; recheck with 402 --check.

Next certify the remaining adjacency transports and vertex stabilizers
for the existing 58 classes, build finite edge reduction, and compute
the expected 16-dimensional G-invariant scalar harmonic space with a
measure bound. Preserve same-session ordering; no expanded class
census, new level or Hecke prime. Actual moments, dyadic CM/frame
matching and a Gaussian chart remain needed. No actual jet, candidate
identification or target polynomial was obtained. Retain D108's
spectral rejection, resource pauses and 180-second process-group cap.
Decisions and references are current; earlier next steps are historical.


**Previous checkpoint: D109 integral dyadic splitting and edge transport, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/definite-dyadic-d109.md`.
The authorized three-part plan is complete: actual definite order
exported, integral dyadic splitting certified, and one norm-one
arithmetic edge transport verified. B=(-1,-1)_F; exact checks prove
closure of the 32-dimensional lattice and trace determinant 2^124.
An exact Hensel certificate (residual valuation 188, derivative 8)
defines the local splitting. Order-image errors are at least 176,
and residue rank four proves the image is all M2(O_K).

The unit (1-i-j-k)/2 reduces to [1,1;1,0] and cycles the base vertex's
three edges. The lattice transition is integral with determinant one.
It fixes the base vertex; no full domain or cross-vertex side-pairing
has been computed. Review 399 binds 629 sources and preserves all
606 D108 hashes; wrong-root and wrong-target controls pass. Three
unsuccessful export attempts are archived. Sources 397--399 and bound
artifacts are frozen; recheck with 399 --check.

Next make D99's known group/Atkin--Lehner quotient explicit in these
coordinates, reconcile it with the saved 58-class data, and certify
one transport moving the base vertex. Preserve same-session ideal
ordering. Do not restart a full census. Harmonic cocycles, actual
moments, dyadic CM/frame matching and a Gaussian chart remain needed.
No actual tangent/jet, candidate identification or target polynomial
was obtained. D108's conditional evaluator and spectral rejection
remain in force. Retain the 180-second process-group cap and
enumeration/Hecke/cubic-precision pauses. Decisions and references
are current; earlier next-step instructions are historical.


**Previous checkpoint: D108 evaluator feasibility and dyadic interface, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/shimura-evaluator-d108.md`.
The completed multiplier at mu=1 proves that the seven omitted norm-31
primes alone force the retained per-ideal absolute spectral comparison
above 460891.49, over 60.32 times the saved partial. This covers all
power kernels and positive mixtures with the unsigned diagonal bound.
It is a method floor, not the actual error. Do not build the full-spectrum
version of that same bound; a complex restart needs new cancellation
or a different diagonal estimate. D98's old enclosure is unchanged.

A conditional direct dyadic moment-to-jet formula is proved. With
v(pi)=1, v(2)=8, bounded-measure moments through J at precision P
give the first three coarse coefficients with error at least
min((J+1)/2-d,P). Exact synthetic controls pass; they are not Shimura
data. The initial low-precision sign control failure is archived.
Review 396 binds 606 sources and preserves all 588 D107 hashes.
Freeze sources 394--396 and bound results; recheck with 396 --check.

Next export the actual definite order, certify an integral dyadic
matrix splitting, and verify one vertex/edge transport witness.
The saved graph lacks these matrices. Inspect the existing HMF
order/ideal interface and the newly cited totally-real tree-domain
method before a full construction. No actual cocycle, moment bank,
dyadic CM matching, tangent/jet, valid Gaussian chart, candidate
identification or target polynomial was obtained. D107's complex
labels and D106's frame remain proved; inert-31 thresholds do not
transfer numerically to 2. Keep the 180-second process-group cap and
enumeration/Hecke/cubic-precision pauses. Decisions and references
are current; earlier next-step instructions are historical.


**Previous checkpoint: D107 certified CM point/root matching, 2026-09-25.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-root-matching-d107.md`.
The old seventeen-point lookup is now certified. D106 marked rigidity
identifies an exact negative normalizer with complex conjugation;
a positive unit witness proves point 8 is the unique real point.
It matches the unique real polynomial root 2. Exact matrix signs
fix beta=-i*sqrt(2+b) in the saved Rickards embedding.

Rational root disks and an integral norm prove the resolvent identity.
A rank-271 certificate separates directed 17-cycle sums and proves
the proposed cycle is Galois. Independent local lifts identify
arithmetic Frobenius at (31,beta-19), of saved class 3. Reciprocity
recovers the original lookup without trusting the old root-order
comparison. Review 393 binds 588 sources and preserves all 562 D106
hashes; the final review passed in 1.90 seconds. Two implementation
failures are archived. Freeze sources 390--393 and bound artifacts;
recheck with 393 --check.

The labels identify D106's rational residue frame for true CM
evaluations. Saved differential values and change matrices remain
uncertified. No actual tangent/jet, particular G12 nonvanishing,
candidate identification or target polynomial has been obtained.
Next establish an executable evaluator, its error bound and a valid
chart before requesting more precision. Retain D98's full-spectrum
and infinite-tail pilot gate, enumeration/Hecke/cubic-precision pauses,
and the 180-second process-group cap. Root Hensel lifting is not a
31-adic Shimura evaluator. Decisions and references are current;
earlier next-step instructions are historical.


**Previous checkpoint: D106 rational CM frame and higher jets, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-rational-frame-jets-d106.md`.
Stable specialization embeds Aut(C_Qbar) in the 64-element graph group.
The odd CM orbit, Galois transitivity and D105 projective frame prove
Aut(C_Qbar,D)=1. D58's geometric descent is therefore compatible with
the given F-model, without D56 ordinarity/moment assumptions.

The degree-17 residue field is uniquely Q-isomorphic to the saved
root field. Residues give a rational CM frame up to a common scalar.
This proves abstract descent, not the saved numerical CM-point/root
matching or a particular actual G12 pivot. The old arbitrary H-frame
does not automatically become that rational frame.

Target ratio Taylor heights for orders 1,2,3 are below
10504,31518,52533. Exact candidate-only jets through order three pass
364 independent quadric checks and the D101/D88 comparisons.
D88 already uses X1=1 and the ratio parameter; no raw-X1 factor
belongs in its second-coefficient comparison.
Inert prime31 gives sufficient valuation thresholds 3257,9746,16236.
Common precision 9746 suffices for the J3 rank test, 16236 for J4,
with matched arithmetic frame/embedding and a valid chart. These
are sufficient thresholds, not existing errors or minimum precision.

Review 389 binds 562 sources and preserves all 543 D105 hashes.
Main/Magma/probe/review passed in 0.15/42.91/1.11/1.42 seconds.
The initial main syntax failure is archived. Sources 387--389 and
bound artifacts are frozen; recheck with 389 --check.

Next obtain an independent arithmetic tangent/jet evaluator. Exact
CM reciprocity orientation is a useful bounded prerequisite for
reusing the analytic route. No independent tangent, candidate
identification or target polynomial has been obtained. No 31-adic
Shimura evaluator is implemented. Keep D98's spectral pilot gate,
the resource pauses and 180-second process-group cap. Decisions
and references are current; earlier next-step instructions are historical.


**Previous checkpoint: D105 actual CM frame and tangent atlas, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-frame-arithmetic-d105.md`. Dyadic specialization
and nine exact graph certificates prove `H0(K_C-D)=0` on the actual
curve. CM transitivity proves every evaluation cofactor nonzero. The
seventeen-point projective frame is now established, independently of
the candidate. The annulus fixed-point argument permits residue
characteristic 2 and does not guess the location of P32.

The polynomial splitting field is the CM Hilbert class field H of
degree 272. This uses a degree-16 resolvent, the proved D59 group/class
number and local unramifiedness, without the numerical orientation.
Any fixed bijection of points and roots gives an H-frame. Its Gaussian
projective tangent has height below 10504 and at least one of fifteen
charts works. The saved D59 labelling, particular G12 pivot and frame
descent to F remain uncertified. H is an auxiliary solvable field.

Audit 386 binds 543 sources, checks all 479 D99 and 53 D104 hashes,
and independently verifies the marked graph and all nine witnesses.
The first audit passed in 0.71 seconds. Candidate height below 677
gives sufficient errors `10^(-1320873)` at one embedding or
`10^(-4857)` at every embedding of H, with consistent labels and a
common valid chart. These are not minimum precision or certified errors.

Next assess an actual independent tangent/jet evaluator and feasible
equality mechanism. The H-route requires jets at all seventeen points
unless equivariant labels/descent are established; first tangent
equality alone does not identify the curve. No independent tangent,
candidate identification or F descent has been obtained. Keep D98's
spectral pilot gate, resource pauses and 180-second process-group cap.
Sources 384--386 and bound artifacts are frozen. Decisions/references
are current; earlier next-step instructions are historical.

**Previous checkpoint: D104 intrinsic CM height, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-intrinsic-height-d104.md`. The stable-model
ramification derivative and auxiliary-level Hodge comparison prove
`H_CM,disk<=2*h_L(Q)+log(2)<41/10`. D103 therefore gives
`h(v_j)<10504`, conditional on arithmetic CM labels, nonzero frame
cofactors and the chosen Gaussian denominator.

Zhao 7.4 and the published averaged/nearby CM identities give
`h_L=-R/8+log(2)/16`; exact finite-product and independent
Taylor-series bounds both prove `h_L<17/10`. The report records the
absolute-height normalization and a dropped discriminant factor in
Zhao's final proof display. The excluded older CM-point formulas
remain unused. No candidate data enters the target-height calculation.

Audit 383 binds 53 sources and checks all 45 D103 hashes unchanged,
including D102/D101 sources. Main/audit passed in 1.09/1.11 seconds.
It also gives conservative conditional recognition thresholds:
`10^(-660791)` at one embedding or `10^(-4859)` at every embedding
in a correctly labelled common field of degree at most 136. These
are sufficient bounds, not minimum precision or existing error bounds.

Next prove actual arithmetic labelling and qualitative frame/chart
nonvanishing, then assess a certified evaluator. No independent
tangent or candidate identification; D98 still contains zero. Keep
the spectral pilot gate, resource pauses and 180-second process-group
cap. Sources 382--383 and bound results are frozen. Decisions and
references are current; earlier next-step instructions are historical.

**Previous checkpoint: D103 adjugate tangent-height bound, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-adjugate-height-d103.md`. Integral adjugate
sections remove the need for a separate residue-index bound in the
height argument: their common determinant cancels from tangent ratios.
A uniform arithmetic CM disk, exact field-vector bounds and Bost's
lower Faltings-height bound give
`h(v_j) <= 513*H_CM,disk + 8400`.

The stable coarse-canonical fibre height H_CM,disk is still unbounded.
Arithmetic CM field labels, nonzero frame cofactors and a nonzero
Gaussian denominator remain hypotheses. Next compare this height
with Zhao's Hodge height through the genus-40/genus-16 quotient,
including its wild dyadic model. The generic u=z^2 identity alone
does not establish that integral comparison. No independent tangent,
numeric target tolerance or candidate identification was obtained.

Audit 381 `--check` passes independent dense-frame, field and constant
checks, binds 45 sources, and verifies all D102/D101 hashes unchanged.
The corrected main and audit jobs took 0.24 and 0.40 seconds. A toy
nonvanishing failure is preserved with its original source and receipt.
Keep sources 380--381 and bound results frozen, the 180-second process
group cap, and the existing resource pauses. No new spectral pilot
is justified yet. Decisions and references are current. Earlier
next-step instructions are historical.

**Previous checkpoint: D102 integral residue frame, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-residue-lattice-d102.md`. The local residue
index is now expressed exactly as the principal-part norm valuation
plus length H1(O(D)), under explicit integral-model hypotheses.
Good reduction and an etale marked divisor do not force this index
to vanish; exact controls include a fixed nonhyperelliptic quartic.

The saved degree-17 field order is independently checked: discriminant
2^79, trace ideal Z, trace-dual clearing integer 32. Multiplying the
centered field basis by 17 places it in the trace-zero codifferent,
with index 2^79*17^15. This does not bound the unknown Shimura frame.
A cofactor-product identity gives an explicit archimedean inverse
bound once independently certified evaluation minors are available.

Next bound the two geometric defects on the actual marked curve and
match the arithmetic norms, or construct actual Gaussian-section
restrictions. No independent tangent or effective target tolerance
was obtained. The analytic pilot gate and existing resource pauses
remain in force. Audit 379 `--check` replays the arithmetic, independent
trace/determinant checks and quartic control, and verifies unchanged
D101 hashes. New jobs took under one second each; completed sources
378--379 and bound results are frozen. Decisions and references are
current. Earlier next-step instructions are historical.

**Previous checkpoint: D101 CM-tangent exactness, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/cm-tangent-exactness-d101.md`. The authorized first
bounded investigation is complete. The tangent is a ratio of Gaussian
sections in H0(3K); conditional norm and height certificates are now
explicit, but their target arithmetic inputs remain unproved. No
independent Shimura tangent or effective target tolerance was obtained.

The missing comparison involves the actual residue-frame lattice index,
compatible arithmetic normalization and metrics. Zhao's CM-height
theorem allows the common dyadic ramification; Yuan's quoted CM-point
Theorem 1.2 excludes it and must not be applied directly. A PEL moduli
description still needs actual section restrictions. Work on that
arithmetic comparison before another spectral pilot; retain D100's
three separate construction gaps and the existing resource pauses.

Magma 375 supplies an exact candidate tangent, with a 269-digit clearing
integer in the saved integral lattice. Python 376 independently checks
its linearizations, normalization and mod-31 comparison; this is only a
candidate reference. Audit 377 `--check` binds the report and replays
those checks, formal identities and the ramification test. Magma took
8.81 seconds, its bounded independent recheck 1.92 seconds. The initial
collector parser failure is preserved; the arithmetic job was reused.
Completed sources 375–377 and bound results are frozen. Earlier
next-step instructions below are historical. Decisions and references
are current; no global model or field polynomial was constructed.

**Previous checkpoint: D100 construction methodology review, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/construction-methodology-d100.md`. The user requested
a strategic review, not automatic continuation of the D98 spectral pilot.
The route has separate arithmetic-identification, exact-cubic/section,
and target-scale-torsion gaps. D51 identifies the original kernels on
the canonical Y, not on our still-unidentified candidate.

The execution-readiness follow-up is in D100 section 7. No further broad
planning is needed. The first bounded research task is to establish an
exactness mechanism for the independent CM tangent, assessing effective
separation bounds or an exact verification identity for the existing
Nelson/Shimizu route before another spectral pilot. The arithmetic frame
and labels are required inputs. Record any missing theorem precisely;
do not treat more precision as its replacement. DECISIONS and REFERENCES
now record the task and the scope of each source.

The next research objective is an executable independent arithmetic
comparison, with the D88 three/four-coefficient criterion, correct
arithmetic frame, and a mechanism proving exact equality. A nonzero
analytic anchor would be only an intermediate result. D98's completed
spectral multiplier remains an option, not a prescribed next job.
After marked X identification, the nine-cover shortcut still leaves
exact coefficient construction. Norm-97 full cofactor separation and
genus-64/degree-51 target arithmetic also remain open. The endpoint is
a degree-257 polynomial over F and normal closure over Q.

No new computation or certificate was produced. Preserve frozen sources,
the 180-second process-group cap, and enumeration/precision pauses.
D99 settles nonhyperellipticity without identifying the candidate.
This checkpoint supersedes earlier instructions about what to run next.

**Previous checkpoint: D99 hyperellipticity review, 2026-09-24.**
The requested fresh review is complete; read the top of `HANDOFF.md`
and `dembele/certificates/hyperellipticity-review-d99.md`.
The intended genus-16 C is geometrically nonhyperelliptic. A fresh
58-class Brandt computation gives the same simple cubic stable graph,
with 30 vertices and 45 edges. All 1,035 one/two-edge deletions remain
connected; an involution with tree quotient would force such a cut.
Baker specialization and Chan's theorem finish the argument. The
primary integral reduction theorem permits torsion at 2. No numerical
rank or curve-automorphism specialization injection is used.

A new enumeration also finds 64 automorphisms and 19 involutions,
none with tree quotient. Saved-order and exact candidate checks pass
again. The candidate remains unidentified with C. The published local
proof confuses the upstairs coordinate with the coarse quotient ring;
u du is an explicit counterexample to the alleged parity implication.
Audit 374 `--check` verifies 479 hashes and replays the graph. All jobs
finished within 180 seconds; the first Brandt intrinsic-name failure
is retained. Sources 370--374 and bound artifacts are frozen.

If construction resumes, D98's completed spectral multiplier remains
the next analytic task. Its error bound and all enumeration/precision
pauses are unchanged. Arithmetic CM jets, marked identification,
cubic recognition and the target field remain open.

**Previous checkpoint: D98 spectral ideal bound, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-spectral-ideal-d98.md`. The actual
omitted-ideal bound improves by >272.48 to <24,784,932,714. The full
error, including the unchanged saved-family tails, is <24,784,942,340.
It remains about 3.244 million times the partial sum; the CM anchor
is uncertified and enumeration remains paused.

The complete norm-a sum is a Hecke kernel on K type four. Its explicit
radial transform cancels the lowest-weight-four discrete series.
Gamma log-concavity uniformly controls the remaining unitary spectrum
by a positive pretrace kernel, whose CM diagonal is <=1795/1792.
Blomer--Brumley's 7/64 exponent controls the auxiliary Hecke spectrum;
the target holomorphic form keeps its stronger Ramanujan bound. The
ideal mass becomes the squared-divisor series with exponent c-7/64,
convergent for c>71/64. No unproved signed-count law is used.

Script 368 tests ten contours; the best tested is c=5/4. Audit 369
`--check` verifies 169 hashes, 20,480 rectangle endpoints, 107 dyadic
interval records, transform/discrete-series controls, Euler arithmetic
and the final enclosure. Both jobs passed, maximum <5.38 seconds.
Sources 368--369 and bound report/artifacts are frozen.

Next test a completed spectral multiplier, preserving its Mellin
cancellation before uniformly bounding all spectral parameters and
the full norm remainder. Do not repeat the contour scan at more digits,
extrapolate D97 finite counts or expand the Hecke/quaternion census.
Keep corrected endpoints, the 180-second process-group cap, D95's
proved identification/ratio convention and the cubic precision pause.
Arithmetic CM jets and the field remain open.

**Previous checkpoint: D97 signed orbital blocks, 2026-09-24.**
Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-signed-orbit-d97.md`. Exact displacement
shells and Abel summation certify finite cancellation: the outer saved
unit/prime-31 block bounds improve by factors >6.45 and >8.16. No signed
counting law has been proved beyond A=25600. The actual omitted-ideal
error stays <6.754e12 and the CM anchor is uncertified.

Script 363 derives all 163 shell phases from exact reduced traces.
Script 366 gives rigorous conditional tail-transfer constants, with an
explicit infinite analytic tail. It does not prove its signed-count
premise. The observed bounds for the whole ideal families are finite
only; do not extrapolate or reinterpret them as individual-orbit bounds.
The relevant phase is the (2,2) Cartan harmonic. Next instantiate an
effective spectral bound, including exceptional terms, numerical
constants, threshold and uniformity over translates, or a direct signed
Hecke-block bound. Then test the complete norm sum: improving the
displacement exponent alone does not improve its norm exponent.

Audit 367 `--check` verifies 162 hashes, 163 exact phase identities,
finite Abel and prefix bounds, 944 algebraic radical enclosures and
the unchanged actual global error. Sources 363--367 and bound artifacts
are frozen; two type-conversion failures are preserved. All jobs have
finished, successful computations <6.20 seconds each. Do not repeat this
finite pilot, D96's positive comparison or D95's completed identification.
Keep enumeration and cubic precision paused, exact endpoints and the
180-second process-group cap. Arithmetic CM jets and the field remain open.

**Previous checkpoint: D96 completed majorant pilot, 2026-09-23.**
Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-completed-majorant-d96.md`. Completed
scalar blocks and the summed ideal Euler majorant improve the
omitted-ideal S11 error to <6.754e12, a factor >3.967. This remains
about 884 million times the partial sum; the CM anchor is uncertified.
The far-tail/splice error is <1.4e-6, so more quadrature precision
cannot fix this positive comparison.

Script 360 encloses 96 dyadic scalar blocks. Script 361 certifies
0<K3<K4 and decreasing K4/A through A=2^72, uses disjoint disks and
Stieltjes integration, and evaluates the whole positive ideal sum by
its completed Mellin integral. No new quaternion or Hecke data are
needed. Audit 362 `--check` independently replays 6,840 rational
Bernstein inequalities, tail-polynomial arithmetic, final bounds and
finite-family cancellation diagnostics; the report and Arb runs are
bound. Sources 360--362 and bound artifacts are frozen. The two
computations pass in <11.95 seconds each.

Next seek a concrete bound retaining signed Hecke or quaternion-orbit
cancellation, with an explicit remainder estimate, before expanding
enumeration. The tested majorant does not make expansion feasible.
Do not repeat D95's completed global identification. Its positive
scalar and conjugated factorial ratio rule remain valid. The original
weight and D93 partial sums are unchanged. Preserve exact endpoints,
the 180-second process-group limit and cubic precision pause. Exact
CM jets, marked identification and the target field remain open.

**Previous checkpoint: D95 global kernel identification, 2026-09-23.**
Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-global-identification-d95.md`. The classical
theta integral and full implemented Mellin series are identified with
the nonzero Jacquet–Langlands tensor up to a positive scalar. The proof
uses a central average, certified class number one and positive-unit
squares, local fixed types, the norm-one forward coefficient and
adjointness. No global numerical evaluation was made.

The derivative convention is now explicit: `(a,1)` differentiates
the conjugated first factor a times. If S11!=0, the fixed disk
differential ratios are `c_a/c_1=conjugate(S_(a,1)/S11)/a!`, a=1/3/5.
The stored sums remain valid. No prior ratio or arithmetic jet was
certified. The full S11 is nonnegative, but the chosen CM anchor
is still not certified nonzero. D94's <2.680e13 omitted-ideal bound
remains too wide. Next test a bounded numerical method retaining more
cancellation before more enumeration or Hecke computation; do not
repeat the now completed global identification task.

Script 359 `--check` verifies 134 hashes and independently replays the
unit, order and Gaussian arithmetic; the mathematical proof and
certified PARI run are bound. The computation and audit passed, maximum
<5.49 seconds. Sources 358--359 and bound report are frozen. Preserve
corrected endpoints, D91's derivative-display caveat, the cubic
precision pause and 180-second process-group limit. Arithmetic jets,
marked identification and the target field remain open.

**Previous checkpoint: D94 contour review and local nonvanishing,
2026-09-23.** Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-test-vector-and-contour-d94.md`. Moving
the unchanged Mellin contour to 25/16 improves the all-other-ideal
`(1,1)` bound to <2.680e13, still far too large against the partial
sum about 7641. Tested polynomial weights give little further gain
and change finite partial sums; their bounds cannot use D93 partials.
Keep the original weight and require a useful pilot that retains
more cancellation before more enumeration or Hecke computation.

The actual Schwartz factors now have a proved nonzero local norm-one
contraction at every place. The eight real factors multiply to
exp(-2*pi) with the stated Haar measures, using Tr(delta^-1)=1.
This is not D91's global scalar or CM first-derivative nonvanishing.
Next match the fixed-character classical kernel to the similitude
formulation in Disegni section 5.1, accounting for the extra variable,
determinant/unit integration and dual convention; Watson's forward-
lift/adjoint argument guides that comparison. The global identification
flag remains false. Script 357 `--check` verifies 127 hashes, 505
dyadic intervals, exact tail polynomials and local field/order facts.
The two computations and final audit passed, maximum <7.21 seconds.
Sources 355--357 and the bound report are frozen. Preserve corrected
D93 endpoints, D91's derivative caveat, the cubic precision pause and
the 180-second process-group limit. No CM tangent or target field exists.

**Previous checkpoint: D93 norm-31 family and global accuracy review,
2026-09-23.** Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-prime31-and-global-tail-d93.md`. Complete
norm-31 enumeration at `(31,b-27)` gives 586 classes through A=25600
and exactly 32 right norm-one orbits, with exact witnesses and an
independent coverage replay. The saved quartic Hecke data give a
weighted family bound. For the smallest root, the unit-plus-prime
`(1,1)` partial is 7640.758 with tail <9626.300, which includes zero.
An all-ideal Ramanujan/divisor majorant proves absolute convergence of
the D91 expression, but the uncomputed-ideal bound <2.685e16 gives no
useful CM accuracy. The global nonzero test-vector identification is
also open. Next review the global kernel/summation and identification
before another Hecke build or larger enumeration.

The audit exposed inward endpoint movement from `QQ(MPFR_endpoint)`.
Script 351 replays five analytic stages with `.exact_rational()`;
use the `*_exact_d93.json` outputs and final root
`nelson_prime31_exact_d93.json`. Original analytic endpoint exports are
superseded, with no frozen files edited. Enumeration coverage is
unaffected and D92's norm-one positivity is re-established. Recheck
with `354_nelson_prime31_certified_audit.py --check`. Thirteen computational
jobs passed; three failed audit attempts are retained. Largest job
<94.44 seconds. Sources 344--354 are frozen. Preserve D91's derivative
normalization caveat, the cubic precision pause and the 180-second
process-group limit. No independent CM tangent or target field exists.

**Previous checkpoint: D92 complete norm-one control, 2026-09-23.**
Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-norm-one-control-d92.md`. Fixing reduced
norm to 1 avoids the large central-unit cover: 541 classes through
A=25600 are complete, proved by a separate interval recursion.
A disjoint-disk argument bounds the entire omitted norm-one tail.
In the D91 normalization, 6193<S11<8443 for this infinite family,
including auxiliary ideals and beta powers. This proves positivity
of one subsum, not a full lift or CM tangent. Higher derivative
tails are still too wide for ratios. Next enumerate the norm-31
prime b=27 with its already saved Hecke data and establish the
corresponding coset/tail argument; then address other ideals and
the global test-vector comparison. Do not merely enlarge norm-one
cutoffs or cubic precision. Script 343 `--check` verifies 51 hashes
and exact arithmetic/interval-output checks. Twelve computational
jobs finished, eleven passes and one retained PARI precision failure;
maximum 81.44 seconds. Scripts 338--343 are frozen. Prior certificates
and the cubic precision pause remain.

**Previous checkpoint: D91 Hilbert unfolding and partial evaluation,
2026-09-23.** Read the top of `HANDOFF.md` and
`dembele/certificates/nelson-hilbert-unfolding-d91.md`. Exact cusp identity
`O#=beta^(-1)O` and central-unit reduction lead to 29 primitive classes.
Forty-two interval kernels include all auxiliary ideals and all beta
powers; the three derivative-pair sums are affine in missing Hecke
coefficients at b=10/20/21 mod31. Saved T31 data are at b=27. No complete
eigenform, global lift or independent tangent has been evaluated.
The first proved unit cutoff is too large for direct enumeration
(A<=359 needs Q<=333, versus the saved Q<=2.02). Next develop complete
norm-ideal/hyperbolic enumeration and a tail bound, starting with the
norm-one control; build matched Hecke data and finish the global
test-vector identification. Direct derivative calibration passes but
records a scale discrepancy in the arXiv-v1 display; see the report.
Script 337 `--check` validates 44 hashes and the exact/interval-output
audit. Nine bounded jobs finished; scripts 327--337 are frozen. Prior
certificates and the cubic precision pause remain.

**Previous checkpoint: D90 Nelson kernel components, 2026-09-23.** Read
the top of `HANDOFF.md` and
`dembele/certificates/nelson-totally-real-kernel-d90.md`. Local test
lattices, finite Fourier normalization, derivative polynomials and a
scalar Mellin prototype are implemented. The normalized dual quotient
has order 4; the CM lattice splitting has 65,536 cosets. A bounded
shell has 9,910 vectors, including 9,360 mixed vectors. The scalar
kernel passes rational Bessel calibration beyond 40 digits.
No global theta lift or independent tangent was evaluated. Next finish
the Hilbert cusp/unit unfolding and test one of the four quartic
level-p2-new eigenforms with a truncation bound. A CM value anchor
vanishes; use first-derivative anchoring. Script 326 `--check` verifies
27 hashes, exact finite and lattice arithmetic, and eight rational
interval proofs. All six jobs are complete; sources 320--326 and their
artifacts are frozen. Prior certificates and the precision pause remain.

**Previous checkpoint: D89 CM tangent input audit, 2026-09-23.** Read
the top of `HANDOFF.md` and
`dembele/certificates/cm-tangent-local-arithmetic-d89.md`. No independent
arithmetic tangent was obtained. Exact local calculations show that the
order-two quotient needs upstairs differential degrees 1/3/5 for the
three coarse coefficients. Of 32 local Hecke branches at 31, only two
stay at maximal CM conductor; thirty introduce unknown neighbor jets.
The known seventeen-point orbit and Hecke matrix therefore do not give
a closed tangent calculation. A global section evaluator is still missing.
Script 319 `--check` replays the local arithmetic without candidate
curve inputs. Prior bound artifacts are unchanged; precision remains
paused. A totally real Shimizu derivative formula is a research lead,
not an implemented exact evaluator.

**Previous checkpoint: D88 identification reviews, 2026-09-23.** Read
the top of `HANDOFF.md` and the two `dembele/certificates/d88-*-review.md`
reports. A rank refinement reduces base verification to independent
arithmetic projective jets through t^2 at the degree-17 CM point: the
quadratic-product matrix must have rank 45 and the saved kernel. The
candidate's ranks 17/34/45 are now independently checked by
`dembele/pari/d88_candidate_cm_jet_rank_check.py --check`; these are not
Shimura-side jets. The paper's four-term degree bound remains a fallback.
Ratios remove the common CM period, but no exact Shimura-side evaluator
has been supplied. P32/B3 markings also need certification.

The cubic shortcut is valid conditionally on the marked arithmetic
identification of C and X. Then the Prym order makes D84's nine thirds
exhaustive; the count 68 selects the current one. Global branch
irreducibility fixes orientation, the S3 norm removes constant cubic
twists, and reduction is injective on 3-torsion. Use the Hecke place
beta=27 modulo 31. This does not establish those missing identifications.
Next seek an independent arithmetic projective tangent computation;
retain D87's need for analytic certification and the hyperellipticity
conflict. No new precision run or target torsion computation follows.

**Previous checkpoint: D87 complete, 2026-09-23.** Read the top of
`HANDOFF.md` and `dembele/certificates/cm-frame-double-cover-character.md`.
The genus-40 candidate's numerical sign character matches the exact S3
sign on all 277 saved side generators, in both differential banks and a
second path family. Independent phase unwrapping checks 192,405 samples.
This supports the geometric double-cover choice; it is not an interval
certificate or arithmetic identification. D77 already selects the
F-scalar twist within a fixed branch half by the B3 inertia condition.
Do not restart arbitrary twist searches, including the excluded -3 twist.

Next retain this double cover and address the marked arithmetic base
identification and selected cubic class/global Galois action. The cubic
class and published hyperellipticity conflict remain unresolved. No
automatic 256-digit run or target torsion follows. Root
`cm_frame_double_cover_character_d87.json`; 318 `--check` verifies 2,187
file hashes / 875 JSON records, including unchanged D86 provenance.
The 52 jobs are complete (51 successful, one rejected midpoint attempt).
All bound sources and exploratory outputs remain immutable.

**Previous checkpoint: D86 complete, 2026-09-23.** Read the top of
`HANDOFF.md` and `dembele/certificates/cm-frame-cubic-128-chatelet.md`.
Both cubic models are independently verified at 31^128, including all
highest-digit controls and reduction to 64 digits. Châtelet completed
21 bounded jobs using kernel 283; peak RSS 2.25 GB, longest job 299.709 s.
The user explicitly authorized this run's mathematical uploads; that
permission persists and must not be requested again. Credentials were
excluded. Sources and earlier failed jobs remain immutable. Adapters
304/305 handle transient transfer errors without retrying job launches.
All remote and local jobs have finished.

Joint F recognition with 112 training / 16 validation digits is negative
at all eight embeddings; controls pass. Exact integer certificates
exclude homogeneous height <=348,750,355,384,078 in the fixed bases.
This does not exclude F or certify arithmetic identity. No exact
number-field cubic or target field polynomial has been constructed.
Next pursue the D85 marked arithmetic comparison/global class action,
including the base/branch marking, twist and hyperellipticity discrepancy.
Do not automatically double to 256 or start target torsion.

Package: `cm_frame_cubic_adjoint_package_128.json`. Root:
`cm_frame_cubic_adjoint_audit_128.json`; 303 `--check` verifies 2009
file hashes / 769 JSON records and the independent integer height
identities. D85's 297 absence assertions are historical and no longer
apply to the current workspace; its source hashes remain unchanged.

**Previous work: D85, 2026-09-22.** Read the top of `HANDOFF.md` and
`dembele/certificates/cm-frame-cubic-128-review.md`. The user authorized
trying 128, followed by review on failure. Sections and jets pass at
31^128, but the actual-divisor stage reaches 2 GB in two versions and
times out at 180 seconds in the blocked version. The verified cubic
remains at 31^64; no 128-digit coefficient recognition ran. This is a
resource failure, not a negative field-recognition result.

The review is complete. The geometric third torsor has 3^48 members;
the nine locally tested solutions do not determine its global action.
The K_X+2P normalization uses linear spaces and the explicit scale
lambda=sqrt(-3)*a0/h0, so adds no new root choice. The S3 cubic has
Aut_C(Y)=1; after proving its field of moduli over the fixed base,
unique comparison maps satisfy descent automatically. The missing
global condition on the selected class is sigma(A)=epsilon_sigma*A,
epsilon_sigma=sigma(sqrt(-3))/sqrt(-3). Script 296 checks an exact
local-rationality counterexample and the reflection normalizer, not
that unproved class condition or arithmetic identification.

Pause precision escalation. Next prepare a marked comparison with the
canonical quaternionic cover, starting with the certification available
for the base/branch marking in the saved analytic data. Keep the global
twist and hyperellipticity discrepancy in scope. Do not automatically
start 256 digits, an arbitrary larger-field search, or target torsion.
Root `cm_frame_cubic_128_attempt_review.json`; 297 `--check` verifies
1744 hashes / 612 JSON records and frozen D84/D83/D78 provenance.
All jobs finished. Failed jobs and bound sources remain immutable;
reuse successful sections/jets if a new divisor algorithm is later
pursued. Preserve the 180 s / 2 GB limits and process-group runner 272.

The descriptions below are historical; D89 and the top handoff govern.

**Previous work: D84, 2026-09-22.** Start with the top of `HANDOFF.md`
and `dembele/certificates/cm-frame-structural-checkpoint.md`. The user
paused doubling to investigate the choice of third and calibrate
recognition. Both checks are complete. Two independently verified
rational anti-invariant 3-torsion points give nine distinct thirds.
Runner 279 constructs and independently verifies every genus-64 cover
and both normalized point counts. Only the current third matches
68/2818; all eight alternatives fail. The subgroup is not proved
exhaustive, and a direct Fuchsian monodromy comparison remains open.

Scripts 275/280 calibrate the joint recognition algorithm on 67 exact
synthetic F-points. Three seeds recover height 10^9 with 60/4 digits
and 10^18 with 112/16; they fail at the next tested decade. These are
empirical example heights, not target bounds or uniform guarantees.
Synthetic 128-digit tests do not lift the actual curve.
Root: `cm_frame_structural_checkpoint.json`; runner 281 `--check`
verifies 1666 hashes / 593 JSON records, including frozen D83/D78 roots.
One random degree-120 support search failed before class arithmetic;
its seed-1 job/log remain preserved. All accepted results have independent
checks and all jobs have finished.

The actual cubic ell*T^3-3*A2*ell*T-R4=0 remains verified through 31^64,
normalized by E=K_X+2P+E40. Package:
`cm_frame_cubic_adjoint_package_64.json`. No exact number-field equation
or target field is certified. The new evidence supports one bounded
actual 128-digit experiment with 112 training / 16 validation digits;
it has not run. If negative, revisit coefficient-field/descent and
identification assumptions before another doubling. Do not modify frozen
sources or prior certificate hashes. Retain 180 s / 2 GB Magma limits.
Use process-group timeout runner 272; 274 wraps existing recognition
workers. The old parent-only timeout defect is documented in D83.

The milestone descriptions below are historical; the D84 report and
new top handoff section govern the current next steps.

**New-session entry point:** read the top "RESUME HERE" section of
`HANDOFF.md` first. **D81 (2026-09-22) lifts and independently verifies
the marked genus-64 cubic modulo 961.** Read
`dembele/certificates/cm-frame-cubic-lift.md`. Genuine support and point
lifts give complete section spaces; the 121-bit scalar computes A2 with
3A2=-Delta2, Frobenius fixed and tau antiinvariant. A moving section
chosen to recover the old E_R on reduction gives the same coefficient
gauge modulo 31. The lifted norm is u*tau(u)=58*f^3*q*tau(q).
All three coefficient arrays reduce exactly to D79, and adding 31 to
the norm scalar or a trace coefficient is rejected independently.
Data: `cm_frame_cubic_lift.{json,m}`; combined certificate:
`cm_frame_cubic_lift_check.json`; runner 194 checks/rebuilds/collects.
Scripts 184–194 implement the lift, with 161 class operations split
into five bounded checkpoints. All jobs finish within 180 s/2 GB.

**D80 (2026-09-22) verifies 68 and 2,818 points on
the genus-64 cubic over F31 and F31^2, exactly matching the Hecke
prediction.** Read `dembele/certificates/cm-frame-cubic-frobenius.md`.
Script 180 resolves exceptional fibres locally; 182 independently
checks every fibre using quadratic/Kummer splitting with different
local coordinates. A changed fibre count is rejected. The measured
power traces are -36,-1856; the Euler polynomial begins 1+36T+1576T^2.
This is two traces at one prime, not a complete arithmetic identification.
Data: `cm_frame_cubic_point_counts.json`; combined certificate:
`cm_frame_cubic_point_check.json`; runner 183 checks/rebuilds/collects.

**D79 (2026-09-21) constructs an explicit genus-64
cubic modulo 31:** Q4*T^3-3*A4*Q4*T-P10=0 over the candidate C,
with weight(T)=2. Read `dembele/certificates/cm-frame-cubic-cover.md`.
The curve means the smooth projective normalization of this function
field. Its S3 closure has genus 136 and quadratic resolvent X of genus 40.

Script 176 descends D78's effective representative to E_R over F31 and
recovers div(h)=D+-D-+3E_R-3D0. The exact norm identity yields
h=27*u/q, a=27*f, h*tau(h)=a^3 and tau(a)=a. The reflection quotient
is y=v+a/v for v^3=h. Evaluation now uses 1,024 points, faithful through
L(8D0), and section dimensions 81,201,321,441. The old 640 points and
class relation are unchanged. No class-number assumption is used.

`cm_frame_cubic.{json,m}` saves coefficient arrays of lengths 105,105,285,
their monomial exponents and all function/divisor witnesses. Verifier 178
checks saved data with a new seed and full final divisor inclusions;
wrong norm and trace coefficients are rejected. Combined certificate:
`cm_frame_cubic_check.json`; runner 179 checks/rebuilds/collects. All jobs
finished within 180 s/2 GB; corrected Magma syntax/API failures are archived.

Next fix persistent algebraic conditions for the effective representative
before lifting to 31^4 and 31^8. D81 fixes its reduction, but leaves
80 linear-system parameters at higher precision. The report proposes
pinning 80 row-reduced coordinates after checking a unit derivative
minor. Do not treat changing scalar-chain representatives as a fixed
recognition gauge. The scalar c2=31*c+10 has now been executed and
checked; no full class number is assumed.
The two successful comparisons support this candidate. The prescribed Fuchsian
monodromy, arithmetic identification, characteristic-zero cubic and
field polynomial remain open. DECISIONS and REFERENCES are current
through D81. All D68–D80 arithmetic artifacts and hashes are preserved.
Do not repeat GP 169's unchanged timeout; the successful finite-field
arithmetic and point checks are in 170–183. All jobs finished.

**Previous fibre milestone:** D77 (2026-09-19) computes the normalized fibre
above B3 on the rational genus-40 cover: **K(sqrt(-3))**, degree 18
over Q, with K the known nonic field. The involution fixes K and
negates sqrt(-3). Over Q(sqrt(-3)) the fibre gives two explicit
degree-nine divisors D+ and D-. Read
`dembele/certificates/cm-frame-B3-fiber.md`.

Scripts 157–160 export exact coordinate jets, prove the leading unit
alpha=-3*s^2, and use the first B3 linear form ell as a rational local
parameter. W=w/(ell/X16) has values +/-sqrt(-3)*r(a). Magma 161
independently checks every jet, the unit and square witness, parameter
change, involution and splitting idempotents. A corrupted unit is
rejected. At 31 take sqrt(-3)=11; each oriented divisor consists of
three degree-three points. Data: `cm_frame_B3_fiber.{json,m}` and
`cm_frame_B3_fiber_structure.{json,m}`; combined certificate
`cm_frame_B3_fiber_check.json`. Runner 162 checks, rebuilds or collects.

The cube-root-of-unity condition for tame total ramification in a
constant cyclic cubic cover singles out the F-scalar twist of this
fixed branch half: [KF:F]=9, so an F element square in KF is already
square in F. This is a necessary condition, not identification of the
half or of the arithmetic cover. The base/marking identification and
hyperellipticity conflict remain unresolved.

Script 163 proves D+-D- nonprincipal: coordinate evaluation at B3 has
rank 9 (minor determinant 17 mod 31), giving h0_C(B3)=1. D70 excludes
L~B3, hence h0_X(pi^*B3)=1. D78 completes the next class-division
step modulo 31, and D79 constructs the function and cubic there. The
prescribed S3 monodromy match remains open. Preserve all earlier data
and follow the current step above.

**Previous equation milestone:** D76 (2026-09-18) constructs an exact rational
double cover w^2=n/d of the certified genus-16 candidate C. The
integral quadrics have heights 583 and 2935433. The smooth normalization
has genus 40 and odd branch divisor B2=D17+P32, degree 18.
Read `dembele/certificates/cm-frame-rational-double-cover.md`.
The equation and its explicit 31^128 square-factor map to the old
lift are in `cm_frame_B3_rational_model.{json,m}`. Independent checks
pass and reject a wrong twist. This is a cover of the candidate C;
the arithmetic Shimura/sign-cover identification is still open.

Scripts 146–149 transfer the B3 normalization at 64 and 128 digits.
Use h*q=g*s with h a unit on G, plus seven P32 jet conditions, to
obtain the full three-dimensional moving space without lifting G's
points. Its six products have rank 6. Script 150 recognizes that
space over Q: six quadrics of six-digit height pass unused-digit
validation. The arbitrary previously selected denominator's ratios
still fail; the space provides a new rational choice.

Scripts 151–152 compute six exact product relations and explicitly
split their Veronese surface over Q. The resulting forms satisfy
F0*A0=D0^2 and the other five rank-one identities. Choose d=9*F0.
Script 153 proves all six forms vanish on the rational residual T
using exact witnesses r*v=n*s_v integral at 31. After subtracting T,
F0 and A0 have no common zeros. Their identity proves even remaining
zeros of F0, giving div(d)=T+2E_Q, deg E_Q=18. This is an exact Q
divisor proof, not a numerical recognition claim.

Script 154 fixes the recorded local twist by a scalar square root;
no nonsquare multiplier is required. Script 155 independently checks
the rational relations/witnesses, special-fibre divisor ideals and
the square-factor identity at 31^128. Negating d leaves the divisors
unchanged but fails the square map. Local agreement does not identify
the global arithmetic quadratic twist.

The D76 next step was to compute the normalized fibre above B3, its degree-18 étale
algebra and involution, as input to the cyclic cubic cover Z->X and
its genus-64 reflection quotient. Use local leading units because
n/d has order two at B3; naive substitution is not the normalized
fibre. Match the specified arithmetic S3 monodromy before accepting
a cubic extension. Runner 148 checks/rebuilds the lift; runner 156
checks/reconstructs the rational model; both have `--collect-only`.
D77 completes that fibre calculation; follow its next step above.

Preserve the archived 180 s/2 GB rational-ideal timeout: the replacement
uses exact linear membership integral at 31 and good reduction, finishing
in 20.390 s. Do not repeat the old probe unchanged. D71's function-field
and D74's generic-nullspace timeout records also remain applicable.
The rational candidate cover is constructed; genus-64 Y and the target
field remain open. Independent Shimura
identification and the earlier hyperellipticity conflict remain separate.
Optional backend cleanup and the old CM-function scans remain paused.
Research files are local and uncommitted; no computation remains running.
Follow the top handoff rather than historical next-step notes.

**User preference (2026-09-15):** prioritize Belyi maps and the user's code
where useful; this is optional. They specifically named `belyi/`, their
thesis and their two coauthored Belyi papers. Local copies are under
`/Users/musty/michaelmusty.github.io/assets/`; `/Users/musty/Belyi` is the
existing external package, which D51–D52 did not edit.

**Previous work (2026-09-17, D67):** Read `lifttors-allocation.md`.
All three diagnostic jobs pass under the unchanged 2 GB/900 s limits.
The genus-16/a=51 lift takes 368.023 s, whole control 444.494 s.
About 82% of lift time is in group multiplication; reduced-J copying
takes only 0.098 s. A 34.5 MB product matrix adds 136.5 MB to the
PARI stack, and the source retains that workspace after its last use.
The largest observed checkpoint is 1.054 GB during inflation; it is
not peak memory. Next test moving the Schur cleanup mark before GWV
and collecting `DivMul` outputs, in a separate build with preserved
comparison paths and the same bounds. Neither optimization is yet
implemented. Twenty tracing off/on comparisons preserve exact matrices
and RNG states; genus-4/a=51 also passes. Removing instrumentation
recovers every original C token in four generated sources. Script 112
runs/collects, script 113 validates, and `.build/lifttors_profile`
preserves D63–D66. No genus-64/a=51 run or cap increase. Actual target
arithmetic sections and their lift remain missing; no target torsion
or polynomial is obtained. CM scans stay paused. D63's 111 tests remain
the latest full Python/Sage run. No jobs remain running; ledgers are D67.

**Previous work (2026-09-17, D66):** Read `lifttors-degree51.md`.
The genus-16/a=51 control passes under the same 2 GB/900 s limits:
364.194 s per lift and 439.776 s overall with D65; 364.732 s and
440.569 s with the separately corrected build. Both verify the exact
branch divisor and 2-torsion. Pinned `PicRed` corrupts the shape of
auxiliary embedding tables; D66 reduces their matrices individually.
Twenty-five matrix reductions, 80 projective vectors from 20 point
evaluations, 15 nested reductions, two malformed-shape rejections,
60 lift comparisons and Q8 field recovery pass. Earlier lifting and
unreduced-J evaluation controls did not consume the damaged tables.
The new build preserves D63–D65 and their recorded hashes. Corrected
genus-64 cost is not measured. Retained genus-16 J occupies about
120 MB even at exponent 2; a conditional genus-64 component model
gives about 1.47 GB, not a peak or stack lower bound. Next instrument
retained Jacobian, GWV/Schur and group-operation allocations under
the same limits. Do not automatically launch genus64/a51 or raise
the cap. Target arithmetic sections and their lift remain missing;
CM scans stay paused. No target torsion or polynomial is obtained.
Script 108 runs/collects D66; D63's 111 tests remain the latest full
Python/Sage run. No jobs remain running. Ledgers are current through D66.

**Previous work (2026-09-17, D65):** Read `lifttors-rows.md`. The new
native path passes at g=64,a=2,e=4 under the same 2 GB stack cap:
514.585 s per lift, 690.829 s for the full control. It stores at most
83,398 equation entries versus 5,504,268, and regenerates every equation
to verify the kernel. Other operations still grow the stack to its cap.
All 11,172 equation comparisons, 60 three-way lift cases, 12 kernels,
6 rank-drop rejections and the Q8 field recovery pass. The genus-4
degree-51 control passes in 8.263 s per lift. A separate build retains
D63 and upstream entry points; D63/D64 recorded inputs stay unchanged.
Next use script 107 with `--only genus16_a51` under the same limits;
this optional intermediate control has not been launched. Genus-64/a=51
feasibility and actual target arithmetic sections remain unresolved.
No further kernel tuning without a measured cause; CM scans stay paused.
The latest full Python/Sage regression run remains D63's 111 tests.
No jobs are running. Ledgers and handoff are current through D65.

**Previous work (2026-09-16, D64):** Read `lifttors-extension.md`.
The genus-4 control passes at a=51, e=4 under the same 2 GB stack cap
and 900-second timeout: one lift takes 8.356 s versus 0.264 s at a=2.
Full-field entry witnesses confirm actual degree-51 arithmetic; the
known torsion point itself is rational. Entry-size measurements project
to about 9.1 GB for the existing genus-64 full matrix, conditionally
on comparable representations. No genus-64/a=51 job was launched.
Script 106's row formula passes 11,172 entry comparisons and all kernel
checks on four small systems. It is a GP prototype; next integrate it
into a selectable native path with complete equation verification and
comparison controls. The equation buffer has 1/66 as many entries at
g=64; total cost is unresolved. Script 105 runs/collects these controls
into `lifttors_extension.json`. The D63 library, sources and report
remain unchanged, and its 111-test result is the latest full regression
run. Target arithmetic section construction remains missing; CM scans
stay paused. No jobs are running. Ledgers and handoff are current through D64.

**Previous work (2026-09-16, D63):** Read `lifttors-memory.md`. The
genus-64 known-answer control now passes under the unchanged 2 GB
PARI stack cap: one lift to 97^4 over residue degree two takes 613.521 s;
the full control takes 784.161 s and checks the exact branch divisor
and 2-torsion. Streamed products remove the first allocation failure;
a batched row-basis kernel solve with all-equations verification removes
the second. The pinned checkout is untouched. The full Q8 and genus-16
controls pass, along with 70 validator comparisons, 60 lift comparisons,
12 known kernels and 6 rank-drop rejections. All 111 existing tests pass.
Next calibrate residue-degree-51 cost on a smaller known curve (g=4,
e=4, same cap/timeout); that run has not been launched. The full lifting
matrix still has 5,504,268 entries at g=64. Target degree-51 feasibility,
arithmetic section construction and the field polynomial remain open.
No jobs remain running. DECISIONS, REFERENCES and HANDOFF are current
through D63; preserve all uncommitted research files.

**Previous work (2026-09-16, D62):** Read the new curve-identification,
LiftTors-control and arithmetic-section-interface reports in
`dembele/certificates/`. The actual saved quaternion order and full
genus-40 reduction graph support D45's identification of C, including
Kurihara's integral quotient theorem at 2. LiftTors now passes an actual
genus-2 torsion/lift/evaluation control, recovering the known Q(i) field,
and a genus-16 lifting control. The genus-64 control fails in PicLiftTors
at a 2 GB PARI stack limit. A preceding validator allocation issue has
an exact batched adaptation, checked against upstream in 70 cases.
The 111 existing regression tests also pass. Next address the measured
genus-64 lift allocation and repeat that known-answer control before a
large arithmetic frontend effort. D0=pi^*(43P) specifies degree 129 and
66 initial sections, but their target arithmetic evaluations remain
unconstructed. No target model, torsion or field polynomial is obtained.
DECISIONS.md, REFERENCES.md and HANDOFF.md are current through D62.

**Previous work (2026-09-16, D61):** The user asked whether to take stock.
Read `dembele/certificates/stocktake-2026-09-16.md`. The broad curve/Jacobian
route remains credible but its practical completion is unproved. Descent
and orbit labels were substantive gains; recent exclusions have not
produced the first exact target function value. Even recognizing all
seventeen CM restrictions would leave a global model/section and cover
construction before target torsion arithmetic. Recommendation: pause
repeated CM-coordinate scans; choose a new arithmetic construction or
changed hypothesis with a specified exact output and downstream use.
Arithmetic section values remain required even for an equationless
Jacobian approach. Revisit the foundational curve-identification conflict
and test an actual generic torsion backend before major investment.
No new computation or replacement method; latest tests remain 111 passing.
DECISIONS.md, REFERENCES.md and HANDOFF.md are current through D61.

**Previous work (2026-09-16, D60):** Tested the entire evaluation plane
span(X,Y) in the labelled residue field. An exact exterior-lattice
certificate excludes every rational line/plane inside the declared
empirical chart boxes up to heights 19,927,223,139 for Q X,
13,481,861,693 for Q Y, and 43,166,965,625,539,309,014 for the plane.
These are primitive Pluecker heights in D59's fixed trace-centered
basis. They are independent of generators within each subspace, not
of the ambient basis. All certificate arithmetic is exact on saved
decimals, but target membership in the boxes is NOT certified; do not
call them unconditional target-height bounds. Script 98 verifies saved
certificates without LLL. All 111 tests pass, including a known exact
plane recovered after complex mixing/noise. Read
`dembele/certificates/cm-flag-height.md`. Next obtain arithmetic flag
evaluations or justified error and upper-height bounds; repeating the
same low-height scans or increasing precision automatically is not
supported. DECISIONS.md and REFERENCES.md are current through D60.

**Previous work (2026-09-16, D59):** Constructed exact ideal-class labels
for all seventeen saved CM embeddings and independently proved h(K)=17.
An exact Frobenius resolvent selects (31,beta-19), class 3, and matches
the points to Elkies's roots. The complex orientation and reference
point use saved numerical geometry/conjugation checks; root numbering
uses Magma's complex/p-adic comparison. The 31-adic group is proved,
but no new analytic enclosure is supplied. In a trace-centered field
basis with evaluation condition 40.9175, simultaneous reconstruction
accepts no X or Y direction at the stated LLL scales and height cap
10^9. Individual ratio tests at denominator cap 10^6 give only 10/15
hits for each. These are empirical intervals and a nonexhaustive LLL
search, not height lower bounds. Read
`dembele/certificates/cm-orbit-recognition.md`. All 103 tests pass.
Next obtain the exact evaluation line/plane or justify a height and
accuracy budget; the labelled identification is now available. Do not
repeat the same scans or automatically increase precision. No jobs run.

**Previous work (2026-09-16, D58):** Established marked descent to Q using
the canonical Atkin--Lehner cover, its unique high-order CM point and
Sijsling--Voight's marked-map theorem. Dembélé's Lemma 5.2 is independent
of hyperellipticity and was overlooked in D57. Under D56's existing
ordinarity/nonvanishing hypotheses, the normalized X,Y make (C,P,D)
rigid, resolve the F-twist ambiguity and are Q-defined. Their CM
polynomial is a rational, irreducible degree-17 target. No descent
matrices or exact coefficients have been computed. The saved-data
pilot at denominator caps 10^3 through 10^6 finds no full polynomial;
at 10^6 ten of fifteen intervals have hits, all ambiguous. These
empirical intervals are not certified enclosures or height bounds.
Read `dembele/certificates/marked-descent.md`. Script 95 and six new
controls bring the suite to 96 passing tests. Next assess a labelled
CM class-group orbit identification with embeddings of Q(theta) for
simultaneous recognition; do not repeat the coefficient scan or
automatically increase precision. No jobs remain running.

**Previous work (2026-09-16, D57):** Audited exact arithmetic input for D56's
CM-normalized functions. All seventeen saved elliptic generators have
the expected CM field, checked exactly. Elkies's known degree-17
polynomial presents the abstract CM residue algebra, with exact
reductions at 31,97,127,191. It does not evaluate the target functions.
Two exact counterexamples in the same algebra satisfy all five trace
conditions with different spectra. The missing input is the flag
`<1> subset ev_D L(17P) subset ev_D L(18P)` in that algebra; under
D56's hypotheses it determines the normalized restrictions. No exact
target value, reduction or height bound is available from the inspected
data. CM-norm formulas require a specified special-divisor function,
which has not been constructed. Read
`dembele/certificates/cm-arithmetic-input-audit.md`. All 90 tests pass;
no jobs remain. Do not repeat this audit or launch another precision
increase without a new arithmetic evaluation input. No exact C/Y,
target torsion or nonsolvable field polynomial.

**Previous work (2026-09-16, D56):** Constructed numerical global functions
with sole poles 17P and 18P using Riemann–Roch section multiplication.
Traces over the seventeen order-two CM points canonically normalize
them to X,Y; conditional on ordinarity, the exact ranks and nonzero
moments, they are F-defined and generate F(C). This removes input-basis
and D52-scale choices for these functions. Two basis choices agree at
CM points within 5.35e-17; checkpoint changes are about 2e-12. No exact
coefficients are known. Script 93's rational shift improves parameter
conditioning, but all plane-equation fits fail unweighted validation,
including fits with impressive weighted singular gaps. Their coefficients
are rejected and give no height information. Read
`dembele/certificates/cm-pointed-maps.md` and the new HANDOFF first.
All 84 tests pass, including independent exact maps and the thesis Q8
control. All jobs finished. Next seek concrete arithmetic data for the
section ratios/CM normalization; do not repeat the failed plane fits.
No exact C/Y, target torsion or field polynomial.

**Previous work (2026-09-15, D55):** Completed all 60 marked-pencil
normalizations, giving 30 distinct cross-ratio expressions. Script 90
now reconstructs the pencil directly from 25 differential products;
the two-fit discrepancies improve by factors of 162 and 60. The marked
configuration depends only on the vanishing flag, giving a conditional
F-definition without D52's formal-coordinate normalization. A simpler
complex flag basis confirms the values. An earlier apparent F match
is one candidate in two equivalent charts; both direct reconstructions
reject it at their empirical tolerances. No candidate in the full
height-32 scan or best-chart height-64 trials. These are bounded numerical
searches, not height lower bounds or certified accuracy. Read
`dembele/certificates/marked-pencil.md` and the new HANDOFF first.
All 78 tests pass; all jobs finished. Next audit actual availability of
additional arithmetic data or a justified height/precision budget before
another precision increase. No exact C/Y, target torsion or field polynomial.

**Previous work (2026-09-15, D54):** Executed the base-quadric reconstruction
in D52's conditional F-basis. A fixed change determined by 32 jets avoids
long formal substitution. Scripts 85–86 recover 91 numerical equations;
the native n=16384 bank has independent side defect 3.86e-20, and two
interpolation choices agree to relative 7.31e-21. These are empirical
checks, not certified coefficient accuracy. Script 87 finds no candidates
among 3,003 nontrivial coefficients or 2,933 scale-invariant ratios at
the recorded bounds. Scripts 88–89 reject a fragile invariant near-match
and test direct equation-space lattices, also without accepted equations.
The weight-22 restriction isolates a two-dimensional numerical pencil
for focused coordinate reduction. Read
`dembele/certificates/arithmetic-quadrics.md` and the new HANDOFF first.
All 71 tests pass; all jobs finished. No exact C/Y, target torsion or
field polynomial. No automatic further n increase is justified by these
bounded negative searches.

**Previous work (2026-09-15, D53):** Revisited the M23 paper, Zhang's updated
note, and the actual prior D3/D9/D21 implementations. See
`dembele/certificates/m23-coordinate-review.md`. A trace-zero differential
ratio gives a relative cubic for Y/C, conditional on arithmetic inputs.
Its two trace sections have ambient dimensions 72 and 111 on C. Script 84
finds stable complex trace data in the saved Belyi banks (side error
2.97e-6), but five simple arithmetic line choices using both marked points
remain unstable. Next: recover the base's quadratic equations in D52's
arithmetic normalization, then use known relations to reduce later
reconstruction. This does not yet solve the F-generator or exact-model
problem. All 58 tests pass; no new large/remote solve or external edit.

**Previous work (2026-09-15, D52):** Gave a marked-point formal-coordinate
argument for an F-defined normalization, conditional on the base jet rank
and scale nonvanishing. Exact Q8 controls reuse `belyi/validate_q8.sage`;
see `dembele/certificates/pointed-normalization.md`. The new n=4096 cover
bank has side defect 2.75e-5, a 330-fold improvement, but its first-48 jet
normalization is ill-conditioned. Selecting later coefficients removes
the need to assume new vanishing orders; the best small trial still has
matrix condition 7.79e6 and 10% disagreement on unused coefficients.
Next: improve arithmetic coordinate/basis conditioning on saved data
before another larger solve or recognition. All 52 tests pass. No exact
new coefficient, Y model, target torsion or field polynomial.

**Previous work (2026-09-15, D51):** Wrote the local-type/JL and integral
Hecke argument realizing the original residual systems in canonical J(Y)[2],
with exact CRT projectors checked by script 80. See
`dembele/certificates/target-realization.md`. Reused the user's Belyi Cauchy
operator through a geometry/standard-component adapter. The n=2048 cover
pilot exhibits 48 separated near-unit eigenvalues and improving sampled
side residuals, currently 0.00908. See `belyi-cover-pilot.md`; these are
numerical candidates, not exact equations. An exact Q8 Belyi control
constructs all 16 two-torsion points over F49. All 47 tests pass.
Next: justify arithmetic section normalization on Y, inspect the Belyi
reconstruction routines, and set up generic torsion lifting with the Q8
control. Norm 97's cofactor test and actual genus-64 costs remain open.
No exact Y, target torsion points, or field polynomial.

**Previous review (2026-09-15, D50):** The curve/Jacobian route remains the
strongest concrete candidate identified, but an end-to-end practical path
is not yet demonstrated. Read `dembele/certificates/route-review-2026-09-15.md`.
Next: finish the local-type/geometric target comparison, pilot the 48 new
differential directions on Y with the standard S3 representation, justify
the CM coefficient field, and assess the actual torsion backend. Increasing
genus-16 precision is supporting work, not the automatic next milestone.
The degree-three map splits old/new 2-torsion, but an actual Galois-stable
target subspace still needs proof. Norm 97's full cofactor test is open.
No new large run, arithmetic curve model, torsion or field polynomial.

**Previous work (2026-09-15, D49):** Implemented compiled FLINT arbitrary-
precision Cauchy actions, residuals, and coefficient accumulation, with one
double LU reused for corrections. All sixteen columns at N=4096 and 8192
converge to finite-system residuals below 4e-41. The N=8192 run takes
246 seconds with four native workers; its independent 275-side residual
is 1.42e-9 (infinity norm), and larger-quadrature defect 5.86e-12.
These show truncation limits, not 40 accurate digits of differentials.
Native checkpoints and reports are `acb_refinement_{64,4096,8192}.*` in
`dembele/data/computed/`; N=8192 is the latest arbitrary-precision finite
solution, not automatically a better analytic approximation than the
larger double banks. Read `dembele/certificates/compiled-precision-refinement.md`.
Next: N=12288 with the native solver and further independent truncation
control before recognition. All 42 tests pass. No exact model or field
polynomial, and no new remote computation.

**Previous work (2026-09-15, D48):** Actual hyperelliptic reconstruction from
the highest-vanishing differentials fails the first unused jet at both
truncations; known hyperelliptic controls pass. Mixed-precision refinement
on a small actual Cauchy operator reaches residual ~1e-49 using double LU
and high-precision residuals. This is a mechanism prototype, not a full-size
basis. Châtelet's separate N=12288 double-precision numerical job finished
and passed its audits (side residual 4e-14). It obtained no exact algebraic
equations or field polynomial; full-size arbitrary precision is unimplemented.
See `dembele/certificates/newton-and-hyperelliptic-ansatz.md`. Next: scalable
arbitrary-precision residuals and independently controlled truncation.

**Geometric state (2026-09-15, D46):** Proved gonality at least four via an
explicit stable-graph minor. Petri therefore guarantees that the canonical
ideal is generated by 91 quadrics; 61 exact local coefficients suffice to
determine them. Computed a real CM jet/period normalization and extended
the differential basis to N=10240. The normalized quadric coefficients
agree across truncations to relative 1.2e-10. No exact coefficient or
number-field model recognized: bounded rational/small-height F searches
found no candidates for six sample jets. Read
`dembele/certificates/canonical-gauge.md`. Next: higher-precision jets and
validated field/coefficient recognition; avoid treating more mpmath working
digits or longer double-precision matrices as arbitrary precision.

**Remote execution (D47):** Deployed the numerical pipeline to Châtelet in
`two_canonical_d46_20260915`, with N=12288 and all downstream audits.
Use `python3 dembele/jobs/canonical/chatelet.py status` for current status;
deployment and result retrieval are documented in that directory's README.
This still uses double-precision linear algebra.

**Previous state (2026-09-15, D45):** The genus-16 quotient is
**nonhyperelliptic by an exact stable-graph obstruction**. Independently
reconstructed its weighted graph from the norm-2 Brandt matrix with
Minkowski class-group proof bounds and an exact mass check. Stabilization
gives the published 30-vertex/45-edge graph. Two independent algorithms
enumerate the same 64 automorphisms; all 19 involutions have quotient
genus 8,10,12,or14, never a tree. Baker specialization plus Chan's metric
criterion excludes hyperellipticity. Read
`dembele/certificates/hyperellipticity-audit.md`. General canonical
reconstruction is the next route; no algebraic model or field polynomial.
The raw norm-2 pairing identity also contradicts the helper's documentation;
see the audit before reusing old pairing-dependent calculations.

**Previous state (2026-09-15, D44):** Computed a stable numerical space of
16 differentials on the genus-16 base and 91 numerical canonical quadrics.
Independent side residuals are below 3.2e-10. Products have rank **45**, not
the rank 31 expected from published hyperellipticity; a local-coordinate
audit identifies an apparent gap in the opening step of that proof.
Read `dembele/certificates/genus16-differentials.md` before assuming a
hyperelliptic model. This is not a certified refutation or an algebraic
model. Best basis: `cm_differentials_8192_refined.npz`; the `8192_mp` and
`8192_block` pilots failed. Next: independent discrepancy audit and
arithmetic normalization of general canonical relations.

**Previous state (2026-09-15, D43):** The genus-16 normalizer domain has been
computed and validated (277 sides, ~257 seconds), and exact local S3
monodromy plus lifted homology verifies the proposed genus-64 cover
(b1=128). See `dembele/certificates/genus64-cover.md` and the newest HANDOFF.
Replay from the saved domain with `python3 dembele/pari/run_fdom.py cover`.
Next: differential/section data and algebraic curve recognition; the
integral target comparison also remains. No algebraic model or polynomial yet.

**Review (2026-09-14, D42):** Dembélé's 2020 genus-16 paper proves the
D40/F16 branch is the solvable Harbater field. It is closed as a nonsolvable
target. Earlier universal route-closure claims are withdrawn. Read
`dembele/certificates/review-2026-09-14.md` and the newest HANDOFF entry.
The proposal uses the original F256 p² carrier in the Jacobian of a
curve, with odd-prime torsion lifting. D43 verifies the local genus-64 cover
construction; no algebraic model or target polynomial exists yet.
Scripts 63 and 64 pass: the sign-type comparison includes both original
target constituents (quotient polynomial t^10), and the finite-field/genus
consistency checks support the proposed construction. The precise integral
geometric comparison remains to be written.

Start new work in **`dembele/`**. The level-one module and degree-16 lift have
already been reproduced. D51 supplies the target comparison for the
specified canonical level; the next milestones are arithmetic section data,
the curve's algebraic model and a usable torsion backend. The pinned local HMF package is
`/Users/musty/hilbertmodularforms`; heavy Magma jobs can run through `remote_magma/`.

## Legacy 2-group Belyi investigation

**Original goal:** find an *explicit* nonsolvable number field ramified only at 2 — the
thesis's "long-term application" (open questions Q1.2.5, Q6.2.1). Mechanism: a 2-group Belyi
map has good reduction outside 2 (Beckmann), so `Q(J[2^n])` is ramified only at 2; if the
Galois image in `Sp_{2g}(F₂)` were nonsolvable you'd get such a field explicitly.

**What we found (a strong conditional obstruction):** assuming Lemma B below, the 2-group
Belyi construction cannot produce one. Such a field exists (Dembélé 2009) but is not
explicit. Full argument in **`writeup/main-result.md`**. In brief:
- Frobenius acts `F₂[G]`-linearly on `J[2] = H¹(X,F₂)`, so the arithmetic image lies in
  `Aut_{F₂[G]}(J[2])` (the centralizer of the deck group).
- **Lemma A** (indecomposable module ⟹ solvable automorphism group) — **PROVED, formalized
  in Lean 4**: `aristotle_solvable/FiniteLocalSolvable.lean` (0 sorry/axiom). The
  multiplicity-free version (End/rad a product of fields ⟹ solvable) is the same proof, not in Lean.
- **Lemma B** (`J[2]` is always **multiplicity-free** — no repeated indecomposable summand) —
  **OPEN**, verified for ALL genus-≥2 triples with `|G| ≤ 128` (**2008/2008**). **CORRECTED
  2026-09-03:** the older phrasing "indecomposable" is FALSE — `Q_{2^m}`, `m ≥ 4`, gives
  `J[2] = A ⊕ B`, `A ≇ B` (`writeup/lemma-B-cyclic.md` §4). This is the one remaining gap.
- Non-Galois covers are controlled by their Galois closure (a Galois 2-group Belyi map), so
  they are conditionally blocked with the Galois route.

## Status ledger

| Component | Status |
|---|---|
| Frobenius ⟹ image in centralizer | standard (Beckmann + NOS) |
| Indecomposable ⟹ solvable (Lemma A) | **proved + Lean-formalized** |
| pro-2: `J[2]` controls `J[2^∞]` | standard |
| non-Galois ⟹ Galois-closure subquotient | rigorous (boundary term to tidy) |
| `J[2]` multiplicity-free (Lemma B, corrected) | **OPEN** in general; **PROVED for cyclic `G`**; "indecomposable" is FALSE for `Q_{2^m}`, `m ≥ 4`; multiplicity-free verified `\|G\| ≤ 128` |

## The one open problem (Lemma B)

Prove `H¹(X,F₂)` is a **multiplicity-free** `F₂[G]`-module for 2-group Belyi maps. Full
attack plan in **`writeup/lemma-B-open-problem.md`**: Gruenberg relation-module framework
`0 → H¹(X°,F₂) → F₂[G]² → I_G → 0` + puncture quotient. **Cyclic `G` is DONE**
(`writeup/lemma-B-cyclic.md`: Hopf-formula coinvariant count; general formula
`dim M_G = 2 + d(M(G)) − r`, `r` = rank of `res: H²(G,F₂) → ⊕_b H²(⟨σ_b⟩,F₂)`). **Census
`|G| ≤ 64` DONE** (`lemmaB/census_top.sage`, 707 triples): `J[2]` is indecomposable for
every group except `Q_{2^m}`, `m ≥ 4` (two non-isomorphic summands of dim `g`, socles
spanned by the fibre classes over `0` and `1`); `End/rad = F₂` except `Q_8` (`F₄`). Next:
test whether summand socles are always spanned by distinct fibre classes (would reduce B′
to a statement about the three fibre classes in `M^G`); prove B′ for `Q_{2^m}` via the
hyperelliptic model `y² = x(x^{2g}−1)`.

## File map

- **`dembele/`** — CURRENT WORK: published data, exact Magma computations, tests,
  certificates, and eventual explicit polynomials.
- **`remote_magma/`** — tested CoCalc/chatelet client for Magma V2.29-10; operational
  details in `remote_magma/CHATELET.md`.
- **`writeup/`** — START HERE. `main-result.md`, `lemma-B-open-problem.md`,
  `all-2-power-covers.md` (the covers negative arc), `README.md`.
- **`DECISIONS.md`** — running decision log: every fork, the alternatives, the
  reason, the outcome. Append an entry whenever a significant choice is made.
- **`REFERENCES.md`** — running ledger of papers/people/software and *how each
  is used* (role tags + repo pointers). Add an entry when a new source enters
  the work; prefer over-attribution.
- **`aristotle_solvable/FiniteLocalSolvable.lean`** — Lean proof of Lemma A (via Aristotle).
- **`torsion_module.sage`** — `analyze(G,s0,s1)` builds `H¹(X,F₂)` as `F₂[G]`-module + exact
  centralizer solvability (commutant/Wedderburn). CLI: `scan`, `ng`, `ngr`.
- **`torsion_fast.sage`, `torsion_shard.sage`** — MeatAxe multiplicity-free screen (80× faster
  multiplicity-free test — not an indecomposability test). `torsion_shard.sage ORDER LO HI` or `... list i1,i2,...` →
  `/tmp/shard_*.csv`. This ran the order-16/32/64/128 scans.
- **`belyi/`** — equation toolkit: `verify.sage` (M1), `cyclic.sage` (M2), `towers.sage`,
  `groups.sage`, `reconstruct.sage`; **`combinatorial_tower.sage`** (fast group-theoretic
  span oracle), `export_steps.sage` (Sage→JSON for the Hecke solver), scan scripts.
- **`belyi_jl/`** — Julia/Hecke: `tower_solver.jl` + `radicand.jl` (span-first + Riemann-Roch
  radicand solver, validated to genus 5). Run: `julia --project=belyi_jl belyi_jl/tower_solver.jl <steps.json>`.
- **`aristotle_deg4/`** — earlier Aristotle proof (Thm 1.2.2 d=4 counts).
- `NOTES.md` — tool inventory (Sage 10.6, Hecke, PARI, Aristotle, lmfdb-lite).

## Key facts / gotchas

- Only **2-generated** 2-groups occur (monodromy = quotient of `F₂ = π₁(P¹∖{0,1,∞})`). At
  order 128 that's 159 of 2313 nonabelian groups — makes scans feasible.
- MeatAxe `max_multiplicity == 1` ⟺ **multiplicity-free** (NOT indecomposable!) ⟹ solvable
  centralizer. A `J[2]` with a repeated summand would be a prize candidate — none found.
  `MTX` functions must be fetched via `libgap.eval("MTX.X")`; attribute access fails.
  Background jobs launched from the agent shell can get duplicated — check `ps` before
  trusting a shared output file.
- Sage's `class_group()` is the AFFINE class group, not `Pic⁰`; `is_square`/relative-tower
  places are unimplemented → the Hecke pivot exists for exactly these gaps.
- Hecke has no packaged function-field class group; it does have `is_principal` (true
  `Pic⁰`), `riemann_roch_space`. Genus-3+ non-metacyclic tower builds are slow (>15 min).
- **Aristotle CLI**: `. .venv/bin/activate`; key in `.env` (`ARISTOTLE_API_KEY`);
  `aristotle submit "<short, <255 bytes>" --project-dir DIR`; `aristotle list` for status
  (`show`/`tasks` hang — they stream); `aristotle download <id> --destination FILE.zip` (a
  FILE path, gzip-tar; a directory path errors). Prompt >255 bytes crashes the CLI.
- `.env` (API keys) is gitignored — do not commit it.

## Cross-machine setup (nothing here travels with `git`)

The repo is code + prose only; every tool below is an external install and must be
provisioned on a new machine. Verified versions on the original host (macOS):

| Tool | Version | Provides / used for | Install |
|---|---|---|---|
| **Magma** | 2.29-8 local; 2.29-10 Chatelet | Current `dembele/` Hilbert modular forms and exact number-field computations; both installations tested 2026-10-05. | licensed Magma install; remote setup in `remote_magma/CHATELET.md` |
| `hilbertmodularforms` | commit `f5ce6582…` | Definite quaternionic Hilbert Hecke/Brandt machinery; pin recorded in `dembele/upstream.lock`. | clone `edgarcosta/hilbertmodularforms` outside this repo |
| **SageMath** | 10.6 | `sage`, `libgap`; bundles **GAP 4.14.0** + SmallGroups library + MeatAxe. Core of `torsion_module/fast/shard.sage`, `belyi/`. | conda `sage`, or sagemath.org binaries |
| **Julia** | 1.12.6 | `belyi_jl/` Hecke tower + radicand solver | julialang.org |
| Julia pkgs | Hecke, Combinatorics, JSON | pinned in `belyi_jl/{Project,Manifest}.toml` | `julia --project=belyi_jl -e 'using Pkg; Pkg.instantiate()'` |
| **Python** | 3.10 | Aristotle CLI (`aristotlelib`) in `.venv/` | `python3 -m venv .venv && . .venv/bin/activate && pip install aristotlelib` |
| PARI/GP | 2.17.x | `nflist` number-field enumeration (earlier route) — **optional** | pari.math.u-bordeaux.fr |
| lmfdb-lite | — | `lmf` package for LMFDB Postgres queries (genus-2 verdict) — **optional**, external | see `[[lmfdb-lite]]` / user's setup |

**Secrets (gitignored — recreate by hand):** `.env` at repo root contains the Aristotle
key and the `COCALC_ACCOUNT_API_KEY`, `COCALC_PROJECT_ID`, and `COCALC_BASE` settings used
by remote Magma. See `remote_magma/CHATELET.md`. `.env` must never be committed.

**Magma access check (2026-10-05):** installing Rosetta restored the local
Intel V2.29-8 binary; the shared smoke test and small number-field/finite-field
checks pass. The Chatelet client includes the missing YR1 intermediate with
TLS verification enabled. The user replaced the rejected account key using
`remote_magma/set_key.py` in their own Terminal. Chatelet V2.29-10 now passes
authentication, uploaded-file execution and inline field-arithmetic tests.
See the [local test record](dembele/checkpoints/magma-access-2026-10-05-local.json),
[remote test record](dembele/checkpoints/magma-access-2026-10-05-remote-restored.json)
and [connection notes](remote_magma/CHATELET.md). D133 resumed after each
brief test admission hold; preserve the global three-worker limit.

**Minimum to reproduce the headline result** (the 2008/2008 multiplicity-free scans): just
**SageMath 10.6** — no Julia, Python-venv, PARI, or LMFDB needed. Julia/Hecke is only for the
equation/tower solver; the Aristotle venv is only for re-running/continuing the Lean proof
(the proof itself, `aristotle_solvable/FiniteLocalSolvable.lean`, is a static artifact and
needs only a Lean 4 + Mathlib toolchain — `leanprover/lean4:v4.28.0` — to recompile).

**Project memory:** the current portable state is in `HANDOFF.md`, this
`CLAUDE.md`, `DECISIONS.md`, `REFERENCES.md`, and `dembele/certificates/`.
Start at the top of `HANDOFF.md`. Additional historical notes may exist
in the user's `~/.claude/…/memory/`; they do not travel with the repository
and may predate the latest handoff. The legacy Belyi results are in `writeup/`.

## Reproduce the headline scan

```
sage torsion_shard.sage 64 1 68        # → /tmp/shard_64_1_68.csv ; all maxmult=1
awk '$1!="#"{print $5}' /tmp/shard_64_*.csv | sort | uniq -c   # → all "1" (multiplicity-free)
```
