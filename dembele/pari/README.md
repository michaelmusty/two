# Fuchsian domain and local level cover

<!-- D157 higher pilot timing checkpoint -->

**Current checkpoint: D157 — the approved column-2 P3200-to-P6400 pilot
is complete.** The [D157 report](../certificates/dyadic-higher-pilot-timing-d157.md),
[fixed review](../data/computed/dyadic_higher_pilot_timing_review_d157.json),
[completion record](../data/computed/dyadic_higher_pilot_timing_completion_d157.json) and
[source ledger](../data/computed/dyadic_higher_pilot_timing_sources_d157.json)
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
The [D156 report](../certificates/dyadic-higher-pilot-preparation-d156.md),
[fixed admission](../data/computed/dyadic_higher_pilot_preparation_review_d156.json),
[completion record](../data/computed/dyadic_higher_pilot_preparation_completion_d156.json) and
[source ledger](../data/computed/dyadic_higher_pilot_preparation_sources_d156.json)
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
The [D155 report](../certificates/proof-criterion-review-d155.md),
[fixed review](../data/computed/proof_criterion_review_d155.json),
[completion record](../data/computed/proof_criterion_completion_d155.json) and
[source ledger](../data/computed/proof_criterion_sources_d155.json)
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
The [D154 report](../certificates/dyadic-pilot-timing-d154.md),
[fixed review](../data/computed/dyadic_pilot_timing_review_d154.json),
[completion record](../data/computed/dyadic_pilot_timing_completion_d154.json) and
[source ledger](../data/computed/dyadic_pilot_timing_sources_d154.json)
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
The [D153 report](../certificates/dyadic-pilot-preparation-d153.md),
[fixed admission](../data/computed/dyadic_pilot_preparation_review_d153.json),
[preparation completion](../data/computed/dyadic_pilot_preparation_completion_d153.json) and
[source ledger](../data/computed/dyadic_pilot_preparation_sources_d153.json)
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
The [D152 report](../certificates/precision-route-cost-d152.md),
[fixed review](../data/computed/precision_route_review_d152.json),
[completion record](../data/computed/precision_route_completion_d152.json) and
[source applicability ledger](../data/computed/precision_route_sources_d152.json)
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
The [D151 report](../certificates/summed-transfer-obstruction-d151.md),
[fixed review](../data/computed/summed_transfer_review_d151.json),
[completion record](../data/computed/summed_transfer_completion_d151.json) and
[source applicability ledger](../data/computed/summed_transfer_sources_d151.json)
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
The [D150 report](../certificates/structural-identification-audit-d150.md),
[fixed review](../data/computed/structural_identification_review_d150.json),
[completion record](../data/computed/structural_identification_completion_d150.json) and
[source applicability ledger](../data/computed/structural_identification_sources_d150.json)
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
The [D149 report](../certificates/P1600-primitive-frame-limits-d149.md),
[fixed review](../data/computed/P1600_primitive_frame_review_d149.json),
[completion record](../data/computed/P1600_primitive_frame_completion_d149.json) and
[source applicability ledger](../data/computed/P1600_primitive_frame_sources_d149.json)
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
The [D148 report](../certificates/P1600-forward-frame-bound-d148.md),
[fixed review](../data/computed/P1600_forward_frame_review_d148.json),
[completion record](../data/computed/P1600_forward_frame_completion_d148.json) and
[source applicability ledger](../data/computed/P1600_forward_frame_sources_d148.json)
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

Sources 620/621 are the primary and independent arithmetic calculations;
622 supplies fixed review, --check replay and --finish completion. Use
only the frozen capped wrapper. Preserve 621 attempt01's failed source
snapshot and use attempt02 for its passing audit. Mathematical workers
are stopped at completion; entry-document hashes are intentionally
not frozen.


<!-- D147 multiplication determinant checkpoint -->

**Current reviewed checkpoint: D147 — dyadic multiplication is surjective; the determinant height comparison remains open.**
The [D147 report](../certificates/P1600-multiplication-determinant-d147.md),
[fixed review](../data/computed/P1600_multiplication_review_d147.json),
[completion record](../data/computed/P1600_multiplication_completion_d147.json) and
[source applicability ledger](../data/computed/P1600_multiplication_sources_d147.json)
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

Sources 617 and 618 contain the primary and independent mathematical
checks. Source 619 builds the fixed review, replays with `--check`, and
closes with `--finish`; invoke each only through the frozen capped
wrapper. Preserve review attempt01's failed source snapshot and use the
successful attempt02 receipt. No mathematical worker remains active
at completion. Entry-document hashes are intentionally not frozen.


<!-- D146 elliptic intersection checkpoint -->

**Current reviewed checkpoint: D146 — the Faltings-only P1600 repair is ruled out.**
The [D146 report](../../dembele/certificates/P1600-elliptic-intersections-d146.md),
[fixed review](../../dembele/data/computed/P1600_intersection_review_d146.json),
[completion record](../../dembele/data/computed/P1600_intersection_completion_d146.json) and
[source applicability ledger](../../dembele/data/computed/P1600_intersection_sources_d146.json)
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

D146 drivers: `614_P1600_elliptic_intersections.py` (Arb192,
local algebra controls and height consequences),
`615_P1600_intersection_audit.py` (Arb224, independent different,
marked-tail and numerical reconstruction), and
`616_P1600_intersection_review.py` (fixed review, `--check`
replay, `--finish` completion). Use the frozen capped wrapper.

<!-- D145 spectral feasibility checkpoint -->

**Current reviewed checkpoint: D145 — the proposed spectral target is ruled out.**
The [D145 report](../../dembele/certificates/P1600-spectral-feasibility-d145.md),
[fixed review](../../dembele/data/computed/P1600_spectral_review_d145.json),
[completion record](../../dembele/data/computed/P1600_spectral_completion_d145.json) and
[source applicability ledger](../../dembele/data/computed/P1600_spectral_sources_d145.json)
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

D145 drivers: `609_P1600_trace_systole.py` (bound 40, exact LDL),
`610_P1600_trace_systole_audit.py` (orthogonal bases, bound 80),
`611_P1600_spectral_feasibility.py` (Arb heat inequalities),
`612_P1600_spectral_feasibility_audit.py` (independent rational
trace and analytic audit), and `613_P1600_spectral_review.py`
(fixed review, `--check` replay, `--finish` completion).
Run every mathematical or review job with the frozen capped wrapper.

<!-- D144 joint adjunction and compact RR checkpoint -->

**Current reviewed checkpoint: D144 — joint elliptic bound and compact RR normalization reconstructed.**
The [D144 report](../../dembele/certificates/P1600-joint-adjunction-RR-d144.md),
[fixed review](../../dembele/data/computed/P1600_joint_RR_review_d144.json),
[completion record](../../dembele/data/computed/P1600_joint_RR_completion_d144.json) and
[source applicability ledger](../../dembele/data/computed/P1600_joint_RR_sources_d144.json)
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

D144 drivers: `606_P1600_joint_adjunction.py` (Arb192),
`607_P1600_adjunction_RR_audit.py` (Arb224, independent marked replay and
formal normalization controls), and `608_P1600_joint_RR_review.py`
(fixed review, replay with `--check`). Run only through
`run_dyadic_capped.py`; retain the global three-worker and memory caps.
The failed first 607 snapshot differs only in its erroneous expected
order-three tail length. Its source, log and receipt remain bound.

D144 completion: four bounded jobs pass (primary calculation, independent
audit, fixed review and replay); one failed control attempt is preserved.
The final review/replay took 59.86/59.77 seconds. All scoped whitespace
checks pass. No D144 mathematical worker remains active.

<!-- D143 finite model and elliptic cotangent checkpoint -->

**Current reviewed checkpoint: D143 — finite-model comparison and both missing cotangent bounds established.**
The [D143 report](../certificates/P1600-finite-model-cotangents-d143.md),
[fixed review](../data/computed/P1600_finite_model_review_d143.json),
[completion record](../data/computed/P1600_finite_model_completion_d143.json) and
[source applicability ledger](../data/computed/P1600_finite_model_sources_d143.json)
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
The [D142 report](../certificates/P1600-two-height-routes-d142.md),
[fixed review](../data/computed/P1600_two_height_review_d142.json),
[completion record](../data/computed/P1600_two_height_completion_d142.json) and
[source applicability ledger](../data/computed/P1600_two_height_sources_d142.json)
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
The [D141 report](../certificates/P1600-proof-gap-d141.md),
[fixed review](../data/computed/P1600_proof_gap_review_d141.json),
[completion record](../data/computed/P1600_proof_gap_completion_d141.json) and
[source applicability ledger](../data/computed/P1600_proof_gap_sources_d141.json)
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
The [D140 report](../certificates/dyadic-P1600-recognition-d140.md),
[fixed review](../data/computed/dyadic_P1600_recognition_review_d140.json) and
[completion record](../data/computed/dyadic_P1600_recognition_completion_d140.json)
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
The [D139 report](../certificates/dyadic-indexed-recost-d139.md), [fixed review](../data/computed/dyadic_indexed_recost_review_r2_d139.json) and [revised cost model](../data/computed/dyadic_indexed_bank_recost_r2_d139.json) record the bookkeeping work following D138. The [completion record](../data/computed/dyadic_indexed_recost_completion_d139.json) confirms six passing bounded jobs; the one diagnosed review-parser failure is preserved.
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
The [D138 report](../certificates/dyadic-precision1600-bank-d138.md), [fixed review](../data/computed/dyadic_precision1600_review_d138.json) and [completion record](../data/computed/dyadic_precision1600_completion_d138.json) supersede the running/ETA notes below.
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
[Progress observed 2026-10-07 10:26 EDT](../data/computed/dyadic_checkpoint_bank_r2_d137_observation03.json): twelve of the fourteen new columns
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
full bank remains unapproved. The [D137 revision-2 admission](../certificates/dyadic-checkpoint-revision-d137.md), [fixed review](../data/computed/dyadic_checkpoint_admission_r2_d137.json) and [admission completion](../data/computed/dyadic_checkpoint_admission_completion_r2_d137.json)
record passing bounded admission and replay over 94,126 hashes.
The first launch exposed the frozen store's required `_d132` suffix before
any store or arithmetic was created. Its failed receipt/log/snapshot and
original configurations are preserved; revision 2 fixes only the interfaces.
The actual revised column-2 storage-creation preflight passed before relaunch.

[launch record](../data/computed/dyadic_checkpoint_bank_r2_d137_launch01.json); [live coordinator log](../data/computed/dyadic_checkpoint_bank_r2_d137_run01.log). Started 2026-10-06T20:33:48.236162+00:00 under a detached coordinator,
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

See the [target-chart report](../certificates/dyadic-target-charts-d136.md), [cost report](../certificates/dyadic-bank-recost-d135.md) and [completion record](../data/computed/dyadic_target_chart_completion_d136.json).

<!-- D135 reviewed bank-cost checkpoint -->

**Previous reviewed checkpoint: D135.**

D135 cost analysis and independent review/replay pass, preserving all 93,912 D134 hashes. The staged target bank is estimated at 22.0--30.5 active days with at most three workers; these are empirical scenarios, not an ETA or admission. Incremental reviews would put additional retention at about 53--65 GiB; plan for at least 80 GiB free, versus roughly 51 GiB observed. A full-bank P1600 checkpoint is estimated at 15--18 hours and 3--4 GiB. Direct P800/P1600-to-target stores violate the unchanged 2 GiB cap. Next resolve target CM peak memory, seed/CM metadata interfaces and bounded incremental review; a scope/storage preference has been requested from the user. No new harmonic stage or bank has launched. Certified precisions remain P800 for the full bank, P6400 for column 0 and P1600 for column 1. Sources 560/561 and reviewed artifacts are frozen. D136 source 562 is running the finite 17-chart synthetic target-memory controls; source 563 is its drafted review/CM adapter. Source 564 is next unused. Inspect the D136 receipts and control lock before any other mathematical job. Preserve every earlier freeze and the three-worker/180-second limits.

See the [cost report](../certificates/dyadic-bank-recost-d135.md) and [completion record](../data/computed/dyadic_bank_recost_completion_d135.json).

<!-- D134 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D134.**

D134 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. The D134 replay and both reviews pass; its fixed review binds 93,912 hashes and preserves the D133 catalogue. The conditional route uses the odd canonical Jacobian order to fix the F-rational branch half, then D77 cubic inertia to fix its scalar. The marked-base and canonical Hecke hypotheses remain essential. The continuation coordinator has no further mathematical jobs after this checkpoint. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](../certificates/arithmetic-twist-classification-d134.md) and [completion record](../data/computed/arithmetic_cover_criterion_completion_d134.json).

<!-- D133 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D133.**

D133 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. All 24,577 D133 input jobs and both reviews pass. The fixed review binds 93,638 hashes. The completion coordinator next runs the D134 finite replay and review; inspect its live session and receipts before starting any other mathematical job. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](../certificates/dyadic-precision6400-d133.md) and [completion record](../data/computed/dyadic_precision6400_completion_d133.json).

**Execution resumed (2026-10-05):** frozen coordinator 553 and driver 554
resumed D133 from correction 10 after all transfer/dependency hashes and
lock checks passed. `run_d133_completion.py` waits for production before
audits/review and D134. See [HANDOFF.md](../../HANDOFF.md) and the
[resumption record](../checkpoints/d133-resume-2026-10-05.json) before any
restart. Keep three mathematical workers and 180-second caps. Certified
precision remains P800/P3200/P1600; the transfer pause below is historical.

**Transfer checkpoint (2026-09-30):** D133 is paused before `low_begin_010`,
with correction 9 and its archive committed in journal `ready009`, epoch 20.
Both coordinators are stopped. Read [CHECKPOINT.md](../../CHECKPOINT.md)
before running anything on a new host: Git LFS payloads, absolute receipt
paths and macOS ARM64 libraries all matter. P6400 and D134 remain pending;
source 560 is next unused. Earlier active-session instructions are historical.

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
See the [snapshot](../data/computed/dyadic_close_session_snapshot_d133_20260929.json)
and [resume procedure](../../HANDOFF.md). This is not a new precision certificate.

Until that review, certified precision stays P800 for the full bank,
P3200 for column 0 and P1600 for column 1. Exact base identification,
marked arithmetic covers/Y64 and the original-kernel polynomial remain
open. No automatic full-bank launch. Keep at most three mathematical
workers, unchanged 180-second process-group caps and all prior freezes.
See the [D132 report](../certificates/dyadic-staged-integration-d132.md) and
[active handoff](../../HANDOFF.md). Earlier next-task statements are historical.

**Previous checkpoint: D131 weighted certificate and row journal reviewed (2026-09-28).**

Sources 541--546 and `run_d131_batch.py` complete the weighted-only replay
and core recoverable storage controls. All 54 input jobs and both reviews
pass; review 546 binds 16567 hashes, preserving all 16142 D130 sources.
Freeze these sources, bound outputs and 24 sealed stores. Source 547 is
next unused. No mathematical worker remains.

541 checks every D129 uniform/weighted coordinate (4,454,400 each), all
174 masses and 870,400 CM scalars using streaming and row authentication.
D129 530 already computes CM from weighted inputs. 542 supplies independent
ordinary recurrence samples. 543 implements generation barriers, row
undo/redo, commit before retirement and an enforced 2 GiB per-store cap.
544 recovers nineteen abrupt-exit points, rejects four corruption/stale
journal cases and controls actual saved and target-width transitions.
Its 22 intentional child exits are not failed bounded jobs; no power-loss
or hardware-durability claim follows.

545 freshly recomputes D124's first P=1600 correction: 348 low-RHS actions,
the streamed 100-bit factor, all 44,544 low equations and 348 correction
actions. All 1,067,664 new residual scalars match the reference. 546
audits all current store hashes and adds separate ordinary samples through
degree 33. No new harmonic precision is obtained. Full bank P=800,
column 0 P=3200 and column 1 P=1600 remain unchanged.

Next integrate the complete resumable staged driver, including separately
capped low-RHS chunks and multi-digit solves, authenticated saved low
answers, weighted initialization, CM publication and all restart states.
Use one working store and inventory every lifetime, with a separate
concurrent-RAM budget. The target sparse reservation peaks at
2,035,873,922 bytes including a 64 MiB reserve; it is not complete target
execution or an aggregate-store/RAM certificate. Select an actual higher
precision column only after these gates. Keep three workers maximum,
unchanged runner 272 caps, assertions and one BLAS thread. D130 timings
are the pre-redesign baseline. See the
[D131 report](../certificates/dyadic-weighted-journal-d131.md) and
[handoff](../../HANDOFF.md). Earlier next-task ordering is historical.

**Previous checkpoint: D130 feasibility reviewed (2026-09-28).**

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

See the [feasibility report](../certificates/dyadic-target-feasibility-d130.md) and
[arithmetic construction specification](../certificates/arithmetic-construction-d130.md).
Earlier next steps below are historical.

**Previous checkpoint: D129 actual P=3200 reviewed (2026-09-28).**

One actual harmonic column now reaches P=3200. All 4,454,400 original
residual scalars, old overlaps, exact masses, 17 CM charts and 22 independent
audit jobs pass. All 1934 input jobs and both fixed reviews pass. Review 532
binds 15600 sources and preserves all 9648 D128 hashes. Peak scratch is
1,229,041,837 bytes under the enforced 2 GiB cap; the highest measured single-process
input peak is 491,929,600 bytes. Four sealed state payloads total 558,829,536 bytes.
Freeze 528--532, both operational schedulers and all bound artifacts.
Column 1 remains P=1600 and the complete bank P=800. Exact vanishing,
candidate identification and the target field polynomial remain open.

D129 plan (superseded by D130): the [stocktake after D129](../certificates/stocktake-2026-09-28.md)
retains the dyadic route and makes exact genus-16 identification the next
major mathematical milestone. Source 533 onward should cost the complete
P=10552 certificate, including all columns, CM/frame/quadric arithmetic,
verification and retention, and compare staged/direct schedules. Specify
the downstream marked-cover and arithmetic Y64 construction alongside
that budget before a long full-bank commitment. No automatic next precision
doubling; the target cost and eventual field polynomial remain open.
Keep the three-worker, 180-second process-group limits and all freezes.
See the [report](../certificates/dyadic-precision3200-d129.md) and current handoff. Earlier next steps are historical.

**Previous checkpoint: D128 selective scaling reviewed (2026-09-28).**

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
See the [report](../certificates/dyadic-selective-scaling-d128.md) and current handoff. Earlier next steps are historical.

**Previous checkpoint: D127 rolling pilot reviewed (2026-09-28).**

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
[report](../certificates/dyadic-rolling-pilot-d127.md) and current handoff. Earlier next steps are historical.

**Previous checkpoint: D126 resource controls reviewed (2026-09-28).**

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
[report](../certificates/dyadic-resource-controls-d126.md) and current handoff. Source 519 is next unused.

**Previous checkpoint: D125 P=800 full bank and comparison reviewed (2026-09-28).**

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

**Previous checkpoint: D124 P=1600 pilot and controls reviewed (2026-09-28).**

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

**Previous checkpoint: D123 P=800 pilot and weighted solver reviewed (2026-09-27).**
Read [the report](../certificates/dyadic-staged-pilot-d123.md),
[the ledger](../data/computed/dyadic_staged_pilot_sources_d123.json)
and [the resume instructions](../../HANDOFF.md).

- 488 factors the P=800, r=32 low block and preserves all P=400 factors.
- 489 and `run_dyadic_staged_pilot.py` complete one column in 126 bounded
  phases, with state-chunk sweeps and a full original GMP residual.
- 490 completes all seventeen CM charts, with coarse beta-errors
  [1632,1648,1632,1664]; 491 independently audits the column and CM values.
- 492 verifies weighted storage and full original reconstruction.
- 493 and `run_dyadic_shrinking_pilot.py` reproduce the column from the
  saved uniform seed in twelve shrinking corrections; all intermediate
  weighted state/residual overlaps pass. 494 independently audits them.
- 495 binds 2532 hashes, preserving all 1884 D122 hashes and all 148
  successful input receipts. Its --check replays the fixed manifest.

The complete bank remains P=400, with unchanged quadric/Gaussian bounds.
No positive exact zero, curve identification or field polynomial is
proved. Both coordinators have completed; do not rerun them. Freeze
488--495 and bound files. Next use a new source (496 next unused) to
combine weighted storage and shrinking bands with resumable chunks,
then measure one P=1600 column including peak memory and every phase.
No P=1600 job has run. The serial shrinking experiment imports a saved
seed and does not establish an elapsed speedup over the parallel pilot.
Keep the persistent wrapper, fresh receipts, assertions, one BLAS thread
and 180-second process-group caps. All resource pauses and downstream
requirements remain. Earlier next tasks below are historical.

**Previous checkpoint: D122 comparison and independent review complete (2026-09-27).**
Read [the final report](../certificates/dyadic-precision400-d122.md),
[the final ledger](../data/computed/dyadic_precision400_review_sources_d122.json)
and [the resume/recovery instructions](../../HANDOFF.md).

- 483 now constructs and checks the actual P=400 residue frame.
- 484 now evaluates all 91 quadrics through four orders at all 17 CM points.
  All 6188 coefficient balls contain zero; no mismatch is certified.
- 486 passes seven independent arithmetic phases, including every coarse
  value and quadratic coefficient, roots/eta, low-state overlaps, sampled
  original recurrences and residual certification of the frame change.
- 487 binds 1884 sources in the completed review, preserving all 1079 D121
  hashes and 1844 interim hashes. All 167 input receipts pass. Its `--check` replays
  the fixed final manifest; 485 remains the historical provenance snapshot.

Section lower bounds are 4194/4145/4128, anchors 3976/3648/3384 and
sufficient non-anchor bounds 25305/25419/25526. W's Gaussian is independently
certified nonzero, valuation 1024 with error 1225, but remains uninverted.
Finite congruences do not prove positive exact zeros or identify the curve.

Freeze 476--487 and bound artifacts. Source 488 is next unused: generalize
the lift, persist state chunks of original-operator sweeps, then time one
actual P=800 column from P=400 with r=32, including all residual and CM
work. No such driver or P=800 run exists yet. Continue using
`run_dyadic_capped.py`, fresh receipt stems, assertions enabled, one BLAS
thread and the 180-second process-group cap. Do not rerun completed 483/484;
after a transport error inspect receipts and partial files before retrying.
All jobs have completed. Resource pauses and downstream field tasks remain.
Earlier next steps below are historical.


**Previous interim checkpoint: D122 complete P=400 bank; comparison and audit pending (2026-09-27).**
Read [the progress report](../certificates/dyadic-precision400-progress-d122.md),
[the source ledger](../data/computed/dyadic_precision400_sources_d122.json)
and [the handoff with exact commands](../../HANDOFF.md).

- 476--477 compile and control FLINT polynomial multiplication against
  GMP, synthetic transports and five actual P=400 state equations.
- 478 lifts columns 1--15 using the Schur solver; final full residuals use
  the older GMP polynomial backend. Audited column 0 remains in D121.
- 479 computes each new column's seventeen CM charts and four coefficients.
- 480 controls arbitrary-integer beta arithmetic and valuation balls.
- 481 refines the algebraic CM frame eta to beta-error 21168 on the
  original seventeen root branches.
- 482 consolidates all sixteen actual P=400 columns and 1088 coarse
  values, with beta-errors [832,848,832,864].
- 483--484 are **drafted but unrun**: actual residue frame first, then
  all 91 quadrics through four orders and updated section thresholds.
- 485 checks provenance/completion and binds a fixed snapshot. It is
  **not the independent D122 mathematical review**, which is still pending;
  486 is the next unused source number.

All 155 computation jobs pass, and no workers remain running. The
checkpoint and hash replay pass, binding 1844 sources and preserving
all 1079 D121 hashes. Freeze successful 476--482,
completed outputs and the bound report/ledger; leave drafts 483--484
editable. All states have moments through 399, only nine required
CM-target states were extended through 1198, and CM moments run through 799.

Use `run_dyadic_capped.py DRIVER FRESH_STEM PASS_MARKER [ARGS...]` from
the repository root with its full path `dembele/pari/run_dyadic_capped.py`.
It preserves frozen runner 272's 180-second private-process-group cap,
sets one BLAS thread, rejects existing receipts/logs and archives failures.
Keep assertions enabled and inspect a successful receipt before launching
a dependent phase. Recheck 485 with `--check` and a fresh stem; its saved
manifest remains valid after new D122 artifacts are added. No temporary
runner or completed-column restart is needed. No P=400 quadric verdict,
positive exact zero, candidate identification or field polynomial is
claimed; all existing pauses and downstream requirements remain.
Earlier next tasks below are historical.


**Previous checkpoint: D121 Schur solver and actual precision lift (2026-09-27).**
Read [the proof and next task](../certificates/dyadic-schur-lift-d121.md).

- 464--465 implement first-moment elimination and verify full Schur iteration.
- 466 prepares reusable arbitrary-precision polynomial transport plans.
- 467--468 implement sparse block LU through r=64 and check original residuals.
- 469--470 compile and independently control the FLINT block multiplication kernel.
- 471 refines all 399 actual transport maps to P=10552 on the original branch.
- 472 factors the actual P=400, r=32 low block with arbitrary integers.
- 473 lifts actual harmonic column 0 from P=200 to P=400 in capped checkpoints.
- 475 computes its seventeen CM charts and all four coarse coefficients.
- 474 independently reviews parameters, interpolation, actual moments, all
  68 coarse values and provenance: 1079 sources, all 961 D120 hashes intact.

The complete sixteen-column bank remains at P=200; the new column has
coarse beta-errors [832,848,832,864]. Twenty-one of 24 input attempts pass;
all three rejected attempts are archived. Freeze 464--475 and bound files.
Recheck 474 --check through runner 272, one BLAS thread and its 180-second
process-group cap. Next accelerate polynomial transport, complete all
sixteen P=400 columns and recompute quadrics. No exact curve or field
identification is proved; target-size iteration still needs lower cost.


**Previous checkpoint: D120 reassessment, precision design and norm-97 isolation (2026-09-26).**
Read [the proof and next task](../certificates/construction-reassessment-d120.md).
Keep D118's direct certificate; the inverse-frame estimate is worse and
a Faltings-only rescue is excluded. Actual P=200 data remain unchanged.

- 458 derives the full inverse-frame budget and the Faltings upper bound.
- 459 implements division-free Möbius moment transport and arbitrary
  integer products, checking one column on all 174 states and 17 charts.
- 460 deduces norm-97 cofactor separation from banked Hecke data. The
  first target has order 51, the second order 257; one wrong initial
  expectation is caught and archived.
- 461 proves the conditional sufficient P=10552 error budget, prices
  storage and measures synthetic transport costs.
- 463 uses installed GMP and integral binomial powers. The actual-bank
  controls pass again, and a synthetic P=10552 action takes 50.408 seconds.
- 462 independently checks the budgets, inverse norm, error propagation,
  target polynomials and provenance: 961 sources, all 922 D119 hashes intact.

Seven input jobs pass. Probe/final reviews pass in 5.261/6.791 seconds;
the reproducibility recheck passes in 7.093 seconds.
Freeze 458--463 and bound artifacts. Recheck through runner 272 with
one BLAS thread and its 180-second private-process-group cap:

    python3 dembele/pari/462_construction_reassessment_review.py --check

Next implement r=1 low-moment elimination on the frozen P=200 bank,
verify the original full residual and precision gains, and cost the
174-dimensional low-block solve and streaming storage. Individual
target-size operations do not make thousands of full sweeps affordable.
No exact positive jet, candidate identification or field polynomial is
proved. All resource pauses and downstream cover/field requirements stand.


**Previous checkpoint: D119 actual Cartier CM divisor and dyadic residue index (2026-09-26).**
Read [the model proof and next task](../certificates/cm-cartier-frame-d119.md).
The actual Cartier divisor keeps eight ordinary pairs intersecting with
length 33, and the disjoint anchor. Its algebra is R x product_8
R[t]/(t^2+4*(2+b)); normalization index 264, discriminant valuation 528.

- 456 reconstructs the principal-parts restriction matrix from the frozen
  P=200 leading harmonic coefficients. Smith values [0x9,2x7] give H1
  torsion length 14. The primitive principal-part norm valuation is 2.
- 457 independently uses integer polynomial quotients and Schur
  complements to check all 272 entries, all 17 maximal minors, the
  primitive kernel and the full residue map. The latter has Smith
  values [0x8,2x8]: index 16 and cokernel killed by beta^2.

Review 457 binds 922 sources and preserves all 911 D118 hashes. An
initial wrong expected graph-pruning count is fully archived. The
corrected calculation takes 3.882 seconds; probe/final review take
2.642/4.159 seconds; the reproducibility recheck passes in 4.622 seconds.
Freeze sources 456--457 and bound files. Recheck
through runner 272, OPENBLAS_NUM_THREADS=1 and its 180-second cap:

    python3 dembele/pari/457_cm_cartier_frame_review.py --check

D119 bounds the pencil line, not the inverse-frame quadratic sections.
Next derive and compare that complete budget. D118's thresholds
25330/25444/25551 and actual 3794/3745/3728 remain current. No positive
exact zero, candidate identification or field polynomial is proved.
Keep all resource pauses; do not substitute index 16 for defect 245
in an unrelated lattice or double-count measured vertical zeros.


**Previous checkpoint: D118 finite CM height and tropical Faltings correction (2026-09-26).**
Read [the proof and next task](../certificates/cm-finite-height-d118.md).
Current sufficient section beta-valuations are **25330/25444/25551**,
versus actual lower bounds **3794/3745/3728**. No positive exact zero,
candidate identification or target field polynomial is proved.

451 checks the composite derivative W_C -> L(Q)^2 and its dyadic
contents [280,17x16]. The companion small-level argument identifies
the integral Hodge generator dz/z, giving correction (69/34)*log(2)
and H_CM<8/3. 452 computes the intermediate fibre-only budgets.
453 computes the known graph's grounded Laplacian inverse, tau
67889/27075 and tropical moment 223268/27075. 454 combines its
Faltings lower bound with the corrected fibre height for the current
budget. Use `cm_arithmetic_height_budget_d118.json`.

455 independently revalues all 272 leading coefficients, verifies the
matrix inverse, integrates resistance derivatives by exact Simpson
quadrature at all thirty vertices, and uses a separate logarithm series.
It binds 911 sources and preserves all 891 D117 hashes. All four input
jobs pass first attempts; the probe/final audit pass in 4.396/5.784 seconds
and the reproducibility recheck passes in 6.336 seconds.
Freeze sources 451--455 and bound artifacts. Recheck through runner 272
with OPENBLAS_NUM_THREADS=1 and its 180-second private-process-group cap:

    python3 dembele/pari/455_cm_finite_height_review.py --check

The dyadic combined correction is fully accounted for; its two summands
are not individually computed. No auxiliary level, new graph or higher
moment precision was run. Higher intrinsic jets require preceding exact
zeros. Next test a lower-degree frame via D102's principal-parts sequence,
first checking the actual Cartier divisor and both index terms. The stable
evaluation defect 245 is not that index. All resource pauses remain;
decisions, references and handoff are current.


**Previous checkpoint: D117 uniform CM disks and arithmetic exactness (2026-09-26).**
Read [the proof and revised plan](../certificates/cm-disk-and-exactness-d117.md).
Sources 446--450 certify uniform embedded CM disks with radius squared 3/5
and sufficient successive integral-section beta-valuations
**35947/36096/36237**. Actual lower bounds remain **3794/3745/3728**;
no positive exact zero, candidate identification or field polynomial follows.

446 excludes a commutator-trace outlier in (2,8] by enumerating 6167
real-lattice vectors. 447 computes the preliminary radius-9/19 thresholds.
448 proves the stronger CM projection bound using 376935 vectors, excluding
a squared absolute value outlier in (4,64]. 449 supplies the current
radius-squared-3/5 budget, its radius-one limit and dense-state storage counts.
450 independently checks support-pattern enumeration, Gram matrices, root
sign changes, interval recurrences and a different logarithm series.

The final review binds 891 sources and preserves 868 D116 hashes. Four
input jobs pass. The first 447 job failed only when serializing enormous
rational endpoints; its source, log and receipt are archived. Certified
outward dyadic rounding fixes it. The probe and final review pass within
ten seconds. Freeze sources 446--450 and bound artifacts. Recheck through
runner 272 with OPENBLAS_NUM_THREADS=1 and the 180-second process cap:

    python3 dembele/pari/450_cm_disk_exactness_review.py --check

Even the optimistic radius-one substitution leaves thresholds
32928/33064/33193 with the other inputs fixed. Next recover the finite
ramification and Hodge/stable lattice corrections from D104, with proved
upstairs nodal generators, then assess the remaining budget. No correction
has been computed yet. No new moments were needed; keep the actual P=200
data. Higher intrinsic jets require preceding exact zeros. Keep all
resource pauses and D99/D108 conclusions. Decisions and references are current.


**Previous checkpoint: D116 integral quadric identification criterion (2026-09-26).**
Read [the proof and revised plan](../certificates/cm-compound-height-d116.md).
Sources 432--445 give a direct integral-section certificate, the actual
coarse jets through order three, and independent checks. Sufficient
successive non-anchor beta-valuations are **119806/120284/120758**;
actual lower bounds are **3794/3745/3728**. No positive-order exact
vanishing, candidate identification or field polynomial is proved.

432/434 certify actual J3 rank at least 33, independently reviewed by
exact center inverses and a Neumann bound in 435. Candidate-centered
rank-45 precision trials are predictions only. 433 removes common
determinant powers from exterior adjugates. 436/437 prove harmonic
saturation and a unimodular weighted graph-cycle comparison. The
companion stable-residue argument supplies the integral lattice
interpretation used by 438/439. Reduced Gaussian/Wronskian contents
improve the alternative ratio equality beta-bounds to 132444/524481.
The horizontal CM residue-map index remains uncomputed.

441 proves a first direct quadric bound. 444 supersedes its analytic
pencil estimate with an explicit adjacent-pair complementary-minor
formula, giving tensor norm below 2^4855 and the thresholds above.
The divided nodal jet theorem requires preceding jets to vanish
exactly; finite enclosures cannot activate those hypotheses.

442 evaluates the third coarse coefficient from the frozen precision-200
moment bank, giving four-order errors 432/448/432/448. 443 evaluates
all 91 quadrics at all 17 points. 445 independently checks all third
coarse entries, 4641 positive quadratic coefficients, lattice witnesses,
finite contents, logarithm bounds and provenance. Exact order-four
vanishing would give the D88 certificate via 68>60, without rank 45.

Freeze sources 432--445 and bound artifacts. Final review 445 binds
868 sources and preserves 814 D115 hashes. All thirteen input jobs,
the calculation probe, final review and recheck pass within the cap.
435/440 ran as probes only; their obsolete draft final-build counts
are not the current audit entry point. Recheck through
runner 272 with the 180-second private-process-group cap:

    python3 dembele/pari/445_cm_arithmetic_identification_review.py --check

The next task is a sharper effective norm/content bound on the actual
reduced tensors or an exact arithmetic identity. Any large precision
implementation first needs proved limb arithmetic, transport accuracy,
memory and phase costs. Keep all census, level, Hecke and cubic pauses,
and D108's spectral rejection. Decisions, references and handoff are
current; earlier next steps are historical.


**Previous checkpoint: D115 actual rational-frame comparison and revised strategy (2026-09-25).**
Read [the report and plan](../certificates/dyadic-comparison-and-strategy-d115.md).
Sources 417--431 carry the actual moment/Poisson computation through
the rational residue frame and two ratio orders. The final candidate
differences have beta-error bounds **101/70** at the sixteen non-anchor
CM points. No mismatch is certified, and no exact identification is claimed.

417 uses full Eisenstein quotient arithmetic and restores exact zeroth
masses before lifting a previous bank. 420 propagates only the contracting
correction. 422/426 batch all coefficient tables, with separately capped
operator and solve jobs. 429 limits intermediate matrix storage. Working
precision 200 gives 1,667,616 state entries, 108,800 CM A-chart entries
and harmonic coarse beta-errors 432/448/432. The W leading valuation
296 is resolved, and all 816 harmonic coarse entries are nonzero.

425 refines D109's same Hensel root to error 352 and re-normalizes the
saved exact matrices, with child/CM errors 331/337. 418/427 construct
the actual rational frame before reading candidate jets, and propagate
local balls through every inversion. The chosen Gaussian has valuation
153 and error 254 at the sixteen non-anchor points. It remains numerically
unresolved at W; rationality and transitivity prove nonvanishing on D.

421/424/428 independently review the operators, moment equations, CM
transfers and coarse kernels. 430 verifies the Gaussian formulas by
direct series division and parameter reversion. 423 proves the dyadic
equality budgets: the current height argument requires beta-errors
274241/820774, or integer pi-errors 137121/410387, at the degree-16 place.
These sufficient bounds are far beyond the achieved ratio accuracy.

431 binds 814 sources and preserves all 713 D114 hashes. Four failed
implementation probes are archived; corrected runs pass. No job times
out, and the longest takes 145.02 seconds. Freeze sources 417--431 and
bound files. Recheck through runner 272 and its 180-second cap:

    python3 dembele/pari/431_dyadic_strategy_review.py --check

The next requirement is an exact arithmetic identification certificate:
a substantially sharper bound on actual unknowns or an exact identity
with proved uniqueness. Another routine precision increase is not the
default plan. Exact marked-cover, global cubic and target-torsion work
remain downstream; the field polynomial is unconstructed. Decisions,
references and handoff are current; retain all resource pauses.
Earlier next steps are historical.


**Previous checkpoint: D114 actual coarse differential jets and anchor precision gate (2026-09-25).**
Read [the proof](../certificates/dyadic-coarse-d114.md).
Python 414 solves the low-degree fixed moment system at precision
16, then recovers state rows through degree 46. It produces 130,848
state entries and 26,112 CM entries through degree 31, all modulo
pi^16 and agreeing with the D113 bank on overlap. The existing
bit-plane quotient is used only within its P<=16 range.

Python 415 evaluates the first three actual coarse differential
coefficients in u=((z-beta)/(z+beta))^2. Integral combined kernels
and full degree-16 CM arithmetic avoid approximate division by beta.
Its three-chart errors are 24,32,24 pi-digits, with 250 certified
nonzero entries per order. Review 416 checks all moment equations
using separate integer convolutions and all 288 kernel coefficients
using an independent rational formula, paying the division-by-two
loss explicitly at temporary precision beta^96.

The actual CM involution exchanges A with its complement, yielding
g_j=2*integral_A K_j dmu and stronger errors **32,40,32 pi-digits**.
Use `certificates.Poisson.symmetry_refined_CM_values` in the final
review artifact; the original source-415 enclosures remain frozen.
All 256 non-anchor entries per order are now certified nonzero.
At W, monic division by (X^2-X)^16 proves all polynomial A moments
divisible by pi^16, from the computed degrees 0..31. Coarse
valuation lower bounds are 32.5,40.5,32.5; no exact vanishing,
nonvanishing or normalization is inferred.

The moment/evaluator jobs pass in 4.59/0.40 seconds. An archived
probe failed on a NumPy-integer bit_length call; converting to a
Python integer fixes it. The corrected probe/final review pass
in 1.69/2.16 seconds. Review 416 binds 713 sources, preserving all
696 D113 hashes. Freeze sources 414--416 and bound artifacts.
Recheck using Python/NumPy through runner 272 and its 180-second cap:

    python3 dembele/pari/416_dyadic_coarse_review.py --check

Next raise working precision to 24, initially evaluating W's A
chart. Use low cutoff 23, iterations 24, state cutoff 70 and CM
cutoff 47; coarse design errors are 40,48,40 pi-digits. More degrees
alone at precision 16 cannot resolve the anchor. A new full
Eisenstein quotient is required: the -20*pi^4 correction has
valuation 20 and cannot be dropped. Use at least beta^96 for CM
arithmetic, with extra precision for independent divisions. Check
overlap with the frozen bank and reuse the existing transports.

These actual harmonic-basis jets precede the rational-frame ratio
jet. Frame change, cofactor propagation, a Gaussian pivot and
dyadic equality thresholds remain needed. Candidate identification
and the target polynomial remain open. Decisions, references and
handoff are current; all resource pauses remain. Earlier next steps
are historical.


**Previous checkpoint: D113 actual positive moments by finite contraction (2026-09-25).**
Read [the proof](../certificates/dyadic-moments-d113.md).
Python 411 constructs all 348 contracting child maps from the
existing 174 edge slots, together with 51 exact CM ball isomorphisms.
Normalized matrix-center errors are at least 159/165 pi-digits.
Each child has phi=b+delta*x/(1+c*x), with v(delta)=1 and v(c)>=1;
thus [x^k]phi^n has valuation at least k. Fixing the zeroth masses
gives a positive-moment operator divisible by pi.

Python 412 executes twelve iterations through degree 11 modulo
pi^12. It saves 33,408 state moments, and CM-chart degrees 1,2,3
with errors 11,10,9. Of the positive CM entries, 2043 are certified
nonzero; all 144 W-anchor entries remain zero modulo their bounds.
The bit-plane quotient arithmetic is restricted to P<=16; beyond
that use the full Eisenstein polynomial. No anchor nonvanishing or
normalization is inferred.

Review 413 uses separate integer polynomial arithmetic to certify
all moment residuals and transfers. It also checks 192 scalar
positive-moment comparisons using 32 independently reduced leaf
balls. The transport/pilot/probe/final jobs pass first attempts in
6.18/1.32/5.83/6.12 seconds. The review binds 696 sources, preserving
all 682 D112 hashes. Freeze sources 411--413 and bound artifacts.
Recheck with Python and NumPy, without Sage or Magma, through 272:

    python3 dembele/pari/413_dyadic_moment_review.py --check

Next use a new source for a modest actual coarse-Poisson pilot:
target 16 pi-digits, CM cutoff 31, state cutoff 46, precision and
iteration count 16. The columns k>=P vanish modulo pi^P, so solve
the low-degree system then evaluate higher rows. Certify actual
nonzero coarse values at W before normalizing. Actual frame change,
cofactor propagation, a Gaussian pivot and dyadic equality thresholds
remain later gates. No actual differential value/jet, candidate
identification or target polynomial is claimed. Decisions, references
and handoff are current; retain the 180-second cap and all resource
pauses. Earlier next steps are historical.


**Previous checkpoint: D112 dyadic CM coordinates and arithmetic frame matching (2026-09-25).**
Read [the proof](../certificates/dyadic-cm-matching-d112.md).
Sage 407 constructs W and both normalized signs at eight ordinary
inverted edges, proving full O_M embeddings, exact fixed-point
charts and localized ideal relations. Sage 408 exports principal
witnesses for all seventeen class labels and for the exponent-10
class action of sigma(beta)=beta^3+3*beta. Magma 409 proposes the
seventeen local root centers.

Rational review 410 independently certifies quaternion/chart
identities, exact ideal lattices, all Hensel roots and the resolvent
choice fixing the Artin direction. The report supplies the geometric
anchor and CM reciprocity argument in the normalized local character.
Root error is at least 688 beta-digits; the actual saved algebraic
residue-frame basis is evaluated with error at least 384 beta-digits
= 192 pi-digits. At the anchor eta1=theta-2/17 has v2=7. The inverse
Artin cycle and an altered root are rejected.

All 51 actual CM boundary-chart zeroth masses are certified using
405: A0=0 and B0+C0=0, with some nonzero B0. Sources 407/408/409
passed in 11.46/5.77/1.54 seconds; one failed expected-valuation
probe is archived and the corrected probe passed in 29.90 seconds.
Final review 410 binds 682 sources and preserves all 661 D111 hashes.
Freeze sources 407--410 and bound artifacts. Recheck without Sage
or Magma, through bounded runner 272:

    python3 dembele/pari/410_dyadic_cm_matching_review.py --check

Next derive finite positive-moment transport/recursion in these
charts, prove the ramified-field error/contraction bound, and run
a small bounded pilot. Retain d=0 and the 180-second process-group
cap. No positive-degree moments, actual harmonic-to-residue change
of basis, jet, candidate identification or target polynomial has
been obtained. Decisions, references and handoff are current;
retain all resource pauses. Earlier next steps are historical.


**Previous checkpoint: D111 arithmetic edge reduction and harmonic cocycles (2026-09-25).**
Read [the proof](../certificates/dyadic-harmonic-d111.md).
Magma 403 exports all 58 ideals, 174 neighbor transports and 164
projective stabilizer elements from the existing norm-two calculation.
Sage 404 certifies exact local frames and all three neighbor directions
at every vertex, using the fixed D109 splitting. P-supported global
indices and local equalities prove the global ideal sandwiches.

The scalar harmonic system has 376 integer relations in 174 slots,
rank 158 and dimension 16. Its integral basis has coefficients of
absolute size at most four and measure denominator bound d=0.
The nine inverted edge orbits have value zero. Python 405 implements
terminating edge reduction, returning quaternion transport words,
decreasing distance traces and all sixteen values. It refines the
same Hensel root when the residue decision needs more precision.

Rational review 406 independently replays the arithmetic and ranks,
and reruns reduction tests through depth 32. These check reversal,
harmonicity, invariance under u/W/h and recovery from shortened
precision. Altered cocycle and nonadjacent-input controls pass.
Export/certificate/reducer/probe/review passed on first attempts in
29.86/9.19/6.59/15.01/15.22 seconds under 180-second process-group caps.
The review binds 661 sources, preserving all 643 D110 hashes.
Freeze sources 403--406 and bound artifacts. Recheck without Sage
or Magma, through bounded runner 272:

    python3 dembele/pari/406_dyadic_harmonic_review.py --check

Next certify W's dyadic fixed points and CM coordinate change, match
the embedding/orientation to the saved CM labels and rational frame,
then compute a bounded moment pilot with a proved ramified-field
error bound. No actual moments, CM/frame matching, jet, candidate
identification or target polynomial has been obtained. Decisions,
references and handoff are current; retain all resource pauses.
Earlier next steps are historical.


**Previous checkpoint: D110 explicit dyadic group and moving-vertex transports (2026-09-25).**
Read [the proof](../certificates/dyadic-group-transport-d110.md).
Magma 400 reconstructs the existing 58-class norm-two arithmetic and
exports four right ideals and seven cached quaternions in the same
session. The matrix/stabilizers match D99 and the order matches D109.
Sage 401 certifies both inclusions pi*I_i subset t_ji*I_j subset I_i,
each of Z-index four, and normalizes the odd product to W^2=-(2+b).

The norm-parity quotient is G/Gamma=C2, represented by [W], which acts
as w_p in the geometric uniformization. W moves the base vertex seven
edges. The norm-one element g=WuW^(-1) moves it fourteen, with certified
target lattice and transition error at least 162. It has projective
order three. Independent replay 402 also verifies that h=ug is
hyperbolic of translation length fourteen, using trace valuation -7.
No complete generating set or full fundamental domain is claimed.

Export/certificate/probe/review passed on first attempts in
28.77/8.03/2.88/3.11 seconds under 180-second process-group caps.
Review 402 binds 643 sources and preserves all 629 D109 hashes.
It checks 4096 right-order products, exact ideal inclusions, localized
conjugation, matrix valuations and transported lattices. Freeze sources
400--402 and bound artifacts. Recheck without Sage or Magma:

    python3 dembele/pari/402_dyadic_group_transport_review.py --check

Next certify complete adjacency/stabilizer data for these same 58
classes, implement finite edge reduction and compute the invariant
harmonic space, expected dimension 16, with a measure bound. Preserve
same-session ordering; no expanded census, level or Hecke-prime bank.
Actual moments, dyadic CM/frame matching, jets and identification
remain open. Decisions, references and handoff are current; retain
resource pauses. Earlier next steps are historical.


**Previous checkpoint: D109 integral dyadic splitting and edge transport (2026-09-25).**
Read [the proof](../certificates/definite-dyadic-d109.md).
Magma export 397 records the actual HMF definite order in (-1,-1)_F
and proposes four local algebra matrices. Sage certificate 398 checks
the 32-dimensional integer lattice and constructs an exact Hensel
splitting: residual valuation 188, derivative valuation 8, root error
180. Order images have error at least 176 and span M2(F2), proving
the integral isomorphism with M2(O_K).

The norm-one unit (1-i-j-k)/2 induces neighbor permutation [2,0,1].
The actual lattice transition is integral with determinant one and
entry-error lower bound 175. It fixes the base vertex; a full domain
or a transport moving that vertex has not been obtained.

Independent rational replay 399 checks the order, exact splitting and
transport, and rejects wrong-root/wrong-target controls. Successful
export/certificate/probe/review jobs took 0.63/6.15/0.78/1.04 seconds
under 180-second process-group caps. One equality failure and two
timeouts at the direct 32-basis mapping stage are archived. Review
399 binds 629 sources and preserves all 606 D108 hashes. Freeze
sources 397--399 and bound artifacts. Recheck without Sage or Magma:

    python3 dembele/pari/399_definite_dyadic_review.py --check

Next make D99's group and Atkin--Lehner quotient explicit in these
coordinates, reconcile the saved 58-class arithmetic and verify one
transport moving the base vertex. Preserve same-session ideal ordering;
no full new census. Actual cocycles, moments, dyadic CM/frame matching,
Shimura jets and candidate identification remain open. D108's formula
is conditional and its spectral rejection unchanged. Retain resource
pauses. Decisions, references and handoff are current; earlier next-step
instructions are historical.


**Previous checkpoint: D108 evaluator feasibility and dyadic interface (2026-09-25).**
Read [the report](../certificates/shimura-evaluator-d108.md).
Main 394 certifies H_31(1)=462.99971524852148... with the completed
Mellin cancellation. The global maximum of h_p(1), and the seven
omitted norm-31 primes, force the specified per-ideal absolute
comparison above 460891.49, over 60.32 times the saved partial.
The rejection permits positive mixtures of power kernels but retains
absolute Hecke envelopes and the unsigned geometric diagonal bound.
It is not a lower bound on the actual omitted sum.

Script 395 verifies conditional dyadic formulas on four synthetic
measure controls. With v(pi)=1 and v(2)=8, moments through J with
precision P and denominator bound d give coarse orders 0,1,2 with
error min((J+1)/2-d,P). The first sign-corruption control failed
because a factor two can hide an error at low precision; its source
and receipt are archived. The corrected control detects the sign
error at J=31 and a missing infinity chart in all cases.

Review 396 reconstructs conservative rational quadrature errors and
the comparison floor, and checks formal coordinate/valuation identities.
Main/corrected-local/probe/review passed in 7.47/2.97/0.09/0.38 seconds
under 180-second process-group caps. It binds 606 sources and preserves
all 588 D107 hashes. Freeze sources 394--396 and bound artifacts.
Recheck:

    python3 dembele/pari/396_shimura_evaluator_review.py --check

Next export the definite quaternion order, certify its integral
dyadic splitting and verify one vertex/edge transport witness. This
does not authorize a full new census. No actual harmonic cocycle,
moment bank, dyadic CM/frame match, Shimura jet or candidate
identification has been produced. D98's full enclosure is unchanged;
a complex restart must change the comparison's hypotheses. Keep
enumeration/Hecke/cubic-precision pauses. Inert-31 precision thresholds
do not transfer numerically to 2. Decisions, references and handoff
are current; earlier next steps are historical.


**Previous checkpoint: D107 certified CM point/root matching (2026-09-25).**
Read [the proof](../certificates/cm-root-matching-d107.md).
Script 390 verifies an exact negative normalizer, the real CM
reference point, its embedding sign and the class of (31,beta-19).
Script 392 exports a positive-unit witness and rational root centers.
Magma 391 proves rank 271 for the 272 ordered-pair root monomials.

Review 393 independently replays quaternion identities, rational
Sturm/square bounds, eighteen integer Rouche inequalities, the
resolvent norm bound, the rank calculation and Hensel lifts modulo
31^8. With marked rigidity and reciprocity, these certify exactly
the old lookup. The approximate complex/p-adic root comparison is
not trusted. Recheck:

    python3 dembele/pari/393_cm_root_matching_review.py --check

Real-structure/rank/witness/probe/final-review jobs passed in
4.30/1.06/3.97/1.60/1.90 seconds under 180-second process-group caps.
The review binds 588 sources, preserving all 562 D106 hashes.
Two initial implementation failures and source snapshots are archived.
Freeze sources 390--393 and bound results. Finite checks do not
machine-verify the geometric proof or cited reciprocity theorem.

The labels now identify the rational residue frame for true CM
evaluations. No actual differential bank, change matrix, tangent/jet
or particular nonzero G12 is certified. Next establish an executable
Shimura evaluator with a complete error bound and valid chart.
Retain D98's spectral pilot gate and resource pauses; local root
lifting is not a 31-adic differential evaluator. Candidate
identification and the target polynomial remain open. Decisions,
references and handoff are current; earlier next steps are historical.


**Previous checkpoint: D106 rational frame and higher jets (2026-09-24).**
Read [the proof](../certificates/cm-rational-frame-jets-d106.md).
Aut(C_Qbar,D)=1 removes the F-twist in D58's geometric Q-descent.
The residue frame is rational up to a common scalar, and its ratio
jets lie in the saved degree-17 field. Numerical root labels and the
particular actual G12 chart still need certification.

Main 387 independently enumerates the graph group by collapsing
identical neighborhoods, checks all affine point stabilizers, and
tests higher-derivative formulas by formal series reversion.
Magma 388 computes candidate-only ratio coefficients through t^3.
Review 389 checks 364 exact quadric coefficients, the D101 tangent
and direct D88 mod-31 comparison, with ranks 17,34,45,45.
D88 already uses X1=1; no extra raw-coordinate scale belongs in its
second coefficient. Recheck:

    python3 dembele/pari/389_cm_ratio_jet_review.py --check

Target heights 10504,31518,52533 and candidate heights 677,1947,3218
give sufficient inert-31 valuations 3257,9746,16236. Thus J3 needs
a common precision 9746, J4 needs 16236, in a matched rational frame
and common valid chart. No actual errors are certified.

The main/Magma/probe/review jobs passed in 0.15/42.91/1.11/1.42 seconds
under 180-second process-group caps. Review 389 binds 562 sources,
preserving all 543 D105 hashes. The initial main syntax failure and
source snapshot are archived. Freeze sources 387--389 and bound
results. The cited geometric proofs are not machine-verified.

Next obtain an independent arithmetic tangent/jet evaluator. No actual
Shimura jet or candidate identification has been obtained, and no
31-adic Shimura evaluator is implemented. Keep the spectral pilot
gate/resource pauses. Decisions, references and handoff are current;
earlier next steps are historical.


**Previous checkpoint: D105 actual CM frame (2026-09-24).**
Read [the proof](../certificates/cm-frame-arithmetic-d105.md).
The actual CM divisor satisfies `H0(K_C-D)=0`; transitivity gives all
nonzero evaluation cofactors. Main 385 checks all nine possible
specializations of P32. Audit 386 independently reconstructs the marks
from Brandt data and verifies integer potentials and burning orders.
It also checks the auxiliary CM class field, candidate projective
height and sufficient equality thresholds. Recheck:

    python3 dembele/pari/386_cm_frame_arithmetic_review.py --check

Probe/main/audit passed in 0.35/0.95/0.71 seconds under 180-second
process-group caps. The audit binds 543 sources and checks all 479
D99 and 53 D104 hashes unchanged. The original conditional probe
remains preserved. The geometric lemmas are proved in the report,
not machine-verified by the audit.

Any fixed root bijection gives a frame over H of degree 272; its
projective tangent height is below 10504. At least one of fifteen
charts works. Candidate height below 677 gives sufficient absolute
errors `10^(-1320873)` at one embedding or `10^(-4857)` at every
embedding of H, with consistently transported labels and a common
valid chart. No existing evaluation is certified to these thresholds.
The saved D59 orientation, specific G12 pivot and F descent remain
open. Next assess an independent tangent/jet evaluator; arbitrary
H-labels require all seventeen point checks for higher jets. No
candidate identification, and D98's enclosure still contains zero.
Retain the spectral gate/resource pauses and freeze sources 384--386
and bound results. Earlier next steps are historical.

**Previous checkpoint: D104 intrinsic CM height (2026-09-24).**
Read [the proof](../certificates/cm-intrinsic-height-d104.md). The
stable ramification derivative and auxiliary small levels give
`H_CM,disk<=2*h_L(Q)+log(2)`. Exact conductor-64 character arithmetic
and rational Gamma bounds prove `h_L<17/10`, hence `H_CM,disk<41/10`
and the conditional tangent-height bound `h(v_j)<10504`.

Main 382 and audit 383 passed in 1.09 and 1.11 seconds under the
180-second process-group cap. The audit uses a different character
generator, conjugate-product inverse, and Gamma Taylor series.
It binds 53 sources and checks all 45 D103 hashes unchanged.
Both computational attempts passed. Recheck:

    python3 dembele/pari/383_cm_intrinsic_height_review.py --check

Candidate-only height bounds give sufficient conditional absolute
errors `10^(-660791)` at one embedding, or `10^(-4859)` at every
embedding. These are not minimum precision or existing evaluator
accuracy. Actual arithmetic labels and frame/chart nonvanishing
remain open; no independent tangent has been computed. Next settle
those hypotheses and assess a certified evaluator. D98 still contains
zero. Keep all resource pauses, the spectral pilot gate and frozen
sources 382--383/bound outputs. Decisions, references and handoff are
current. Earlier next steps are historical.

**Previous checkpoint: D103 adjugate tangent-height bound (2026-09-24).**
Read [the proof](../certificates/cm-adjugate-height-d103.md). Script
380 checks integral adjugate frames, Gaussian cancellation, nodal
integrality and the exact constants in `h(v_j)<=513*H_CM,disk+8400`.
Audit 381 independently checks dense frames in ranks 3 and 16, field
bounds and integration constants; it binds 45 sources and preserves
all D102/D101 hashes. The main and audit jobs passed in 0.24 and 0.40
seconds under 180-second process-group caps. An initial toy-jet
nonvanishing failure and its source snapshot are retained. Recheck:

```sh
python3 dembele/pari/381_cm_adjugate_height_review.py --check
```

H_CM,disk remains unbounded. Next prove its integral comparison with
the Hodge height at the wild dyadic normalizer quotient. Arithmetic
CM labels and frame/chart nonvanishing remain hypotheses. The height
argument no longer needs a separate residue-index or evaluation-minor
lower bound, but no independent tangent or usable tolerance has been
obtained. Keep sources 380--381 and bound outputs frozen, all resource
pauses, and the spectral pilot gate. Decisions, references and handoff
are current; earlier next steps are historical.

**Previous checkpoint: D102 integral residue frame (2026-09-24).**
Read [the result](../certificates/cm-residue-lattice-d102.md).
Script 378 checks the saved field order, trace-dual clearing factor
32, centered-basis factor 17 and trace-zero index 2^79*17^15. It also
checks the two-term residue-index formula and cofactor inverse bounds
on exact controls. Audit 379 uses independent trace/determinant
algorithms, a nonhyperelliptic quartic family, and unchanged D101 hashes.
Both initial jobs passed in under one second with 180-second
process-group caps. Recheck with:

```sh
python3 dembele/pari/379_cm_residue_lattice_review.py --check
```

The actual principal-parts norm, cohomology Fitting ideal and compatible
arithmetic metrics remain unbounded. The field-only factors do not
clear the unknown tangent. No independent Shimura tangent was computed
and the spectral pilot gate remains unmet. Preserve sources 378--379,
bound outputs, old sources and the existing resource pauses. Decisions,
references and handoff are current; earlier next steps are historical.

**Previous checkpoint: D101 CM-tangent exactness (2026-09-24).**
Read [the result](../certificates/cm-tangent-exactness-d101.md).
Magma 375 computes the exact candidate tangent; Python 376 independently
verifies it using integer arithmetic, mod-31 ranks and formal Gaussian
controls. Audit 377 `--check` binds the report and replays the candidate,
strict norm-separation controls and common dyadic ramification test.
The candidate's 269-digit clearing integer is not a target height bound.

The conditional recognition criterion lacks the actual arithmetic frame
and lattice comparison. No independent Shimura tangent was computed;
the spectral pilot gate remains unmet. The new height sources are
potential inputs to that arithmetic comparison, not a computed bound.
Preserve completed sources 375–377, the failed collector snapshot,
bound results, the 180-second process-group cap and existing resource
pauses. The original successful arithmetic job was reused after the
parser repair. Decisions, references and handoff are current.

**Previous checkpoint: D100 methodology review (2026-09-24).**
Read [the review](../certificates/construction-methodology-d100.md) and
the top of `HANDOFF.md`. No new arithmetic script or result was produced.
The next research objective is a complete independent arithmetic
identification method, including exactness as well as analytic accuracy.
D98's completed spectral multiplier is an option, not an automatic next
job. Exact global cubic/section data and target-scale torsion remain
separate gaps. Preserve old bound artifacts, the 180-second process-group
cap, and enumeration/Hecke/cubic-precision pauses. Earlier next steps
below are historical; their evidence and audit commands remain valid.

**Previous checkpoint: D99 hyperellipticity review (2026-09-24).**
Read [the full review](../certificates/hyperellipticity-review-d99.md).
The intended genus-16 C is geometrically nonhyperelliptic. Fresh Brandt
arithmetic 371 and standard-Python graph program 372 rebuild the stable
30-vertex, 45-edge graph. All 1,035 one/two-edge deletions remain
connected, excluding a tree quotient by an involution. A separate new
enumeration finds 64 automorphisms and 19 involutions, with no tree
quotient. The theorem chain was checked at the primary sources,
including Kurihara's integral quotient with torsion at 2.

```sh
python3 dembele/pari/374_hyperellipticity_review_audit.py --check
```

The root verifies 479 hashes and replays the entire graph calculation.
Script 373 reruns the saved-order check; Magma 117 reruns the exact
candidate canonical-curve certificate. Neither identifies the candidate
with C. All jobs finished within the 180-second process-group cap.
The failed Magma 370 attempt is preserved; corrected 371 passes.
Sources 370--374 and bound reports/results are frozen. No old bound
output was overwritten. D98's completed spectral multiplier remains
the next construction investigation; the CM anchor is still uncertified.

**Previous checkpoint: D98 spectral ideal bound (2026-09-24).**
Read [the D98 proof and pilot](../certificates/nelson-spectral-ideal-d98.md).
Script 368 evaluates an explicit spectral comparison for every complete
norm-ideal family. The omitted-ideal S11 bound improves by >272.48 to
<24,784,932,714. Including the unchanged two-family tails gives full
error <24,784,942,340; the CM anchor remains uncertified.

```sh
python3 dembele/pari/369_nelson_spectral_ideal_audit.py --check
```

The K-type-four transform produces a factor lambda+2, cancelling its
lowest-weight-four discrete series. Gamma log-concavity bounds the
remaining spectrum by a positive pretrace kernel. A 7/64 finite Hecke
exponent makes the complete ideal mass a squared-divisor series,
convergent for c>71/64. Ten contours are tested; c=5/4 is best.
The method needs no unproved infinite signed-count estimate.

Root `nelson_spectral_ideal_d98.json` verifies 169 hashes, 20,480
rectangle endpoints and 107 dyadic interval records. Rational replay
checks normalization identities, Euler coefficients, tail polynomial,
algebraic powers and final error assembly; analytic arguments and Arb
evaluations are bound to the proof and successful run. Both jobs passed,
maximum <5.38 seconds. Sources 368--369 and bound artifacts are frozen.
Next test the completed spectral multiplier before absolute values,
with uniform spectral and infinite norm control. Preserve the original
partials, exact endpoints, timeout and enumeration/precision pauses.

**Previous checkpoint: D97 signed orbital blocks (2026-09-24).**
Read [the D97 report](../certificates/nelson-signed-orbit-d97.md).
Scripts 363/366 certify finite shell/Abel cancellation and conditional
infinite-tail transfer constants. Audit 367 verifies 162 hashes,
163 exact phase identities and 944 radical bounds. No infinite signed
counting law is proved, and the finite-prefix constants must not be
extrapolated. Sources 363--367 and bound artifacts are frozen; the
two earlier type-conversion failures remain preserved.

**Previous checkpoint: D96 completed majorant pilot (2026-09-23).**
Read [the D96 report](../certificates/nelson-completed-majorant-d96.md).
Script 360 computes uniform degree-31 Taylor enclosures for 96 dyadic
scalar blocks. Script 361 proves positivity and monotonicity through
A=2^72, applies the orbit disk count by Stieltjes integration, and
sums the complete positive ideal majorant through its zeta factors.
The omitted-ideal S11 bound improves by >3.967 to <6.754e12; it is
still about 884 million times the partial sum. The pilot does not
justify new quaternion enumeration or Hecke computation.

```sh
python3 dembele/pari/362_nelson_completed_majorant_audit.py --check
```

Root `nelson_completed_majorant_d96.json` verifies 145 source hashes
and 7,505 dyadic intervals, binding the D95 provenance, new report
and runs. Audit 362 replays 6,840 Bernstein inequalities,
the rational tail polynomial, final directed bounds and finite-family
cancellation diagnostics. Arb evaluations are bound to the successful
runs, which took <11.95 seconds each. Sources 360--362 and bound
artifacts/report are frozen. The original kernel and D93 partials are
unchanged. Next review a bound for signed Hecke blocks or quaternion
orbit sums with an explicit remainder; further precision or a small
enumeration increase does not fix the measured positive majorant.

**Previous checkpoint: D95 global kernel identification (2026-09-23).**
Read [the D95 proof](../certificates/nelson-global-identification-d95.md).
Script 358 certifies the field hypotheses and checks local level,
Gaussian matrix paths and Mellin powers. The accompanying proof
identifies the classical theta integral and full Mellin series with
the nonzero rank-one tensor, up to a positive scalar. Its `(a,1)`
pair differentiates the conjugated factor a times: conditional on
S11!=0, the disk ratios are `conjugate(S_(a,1)/S11)/a!`.

```sh
python3 dembele/pari/359_nelson_global_identification_audit.py --check
```

Root `nelson_global_identification_d95.json` binds 134 files, including
the proof and D94 root. The independent rational replay checks unit
signatures, 1,056 norm conditions and Gaussian coefficients. PARI
certification and Sage symbolic checks are bound to the successful
run. Both computation and audit passed, maximum <5.49 seconds.
Sources 358--359 and bound artifacts/report are frozen. No numerical
full-series evaluation or arithmetic CM jet was obtained. D94's
<2.680e13 error bound remains unchanged; next improve summation accuracy.

**Previous checkpoint: D94 contour review and local nonvanishing
(2026-09-23).** Read
[the D94 report](../certificates/nelson-test-vector-and-contour-d94.md).
Script 355 tests 28 contour/weight choices. The original weight on
c=25/16 bounds the omitted ideals by <2.680e13 for `(1,1)`, still far
too wide against a partial sum about 7641. Nonzero polynomial weight
powers change the partial sums; do not use them with D93 partials.
Script 356 verifies exact arithmetic for the local norm-one
contractions, whose real product is exp(-2*pi) with the stated measures.
The global kernel comparison and CM derivative remain open.

```sh
python3 dembele/pari/357_nelson_kernel_review_audit.py --check
```

Root `nelson_kernel_review_d94.json` verifies 127 hashes, 505 dyadic
intervals, 168 tail polynomials, and exact local field/order arithmetic.
The corrected D93 root and D94 proof report are bound; Arb nodes and
the earlier exhaustive enumeration are not repeated. Both computations
and the audit passed, maximum <7.21 seconds. Sources 355--357 and bound
artifacts/report are frozen. Next compare the classical kernel with
the similitude formulation before asserting global identification.
Further enumeration needs a useful bound retaining more cancellation.

**Previous checkpoint: D93 norm-31 family and global accuracy review
(2026-09-23).** Read
[the D93 report](../certificates/nelson-prime31-and-global-tail-d93.md).
Scripts 344--346 enumerate 586 classes through A=25600 at `(31,b-27)`,
independently prove coverage and certify exactly 32 right norm-one
orbits. Scripts 347--348 weight the infinite prime family and derive
an all-ideal bound. The latter is <2.685e16 for `(1,1)`, against a
partial sum about 7641: it does not establish useful CM accuracy.
The nonzero global test-vector identification also remains open.

```sh
python3 dembele/pari/354_nelson_prime31_certified_audit.py --check
```

Use root `nelson_prime31_exact_d93.json`. Script 351 replays five
analytic stages with exact dyadic endpoints, replacing the original
`QQ(MPFR_endpoint)` exports, which can move inward. Its corrected
`*_exact_d93.json` artifacts supersede the D91 sum, D92 final sum/tail
and D93 prime/global bounds. Scripts 349, 350, 352 and 353 preserve audit
development; 354 is the governing final audit. Coverage and exact
arithmetic are unaffected, and the norm-one positivity is re-established.
Thirteen computational jobs passed, maximum <94.44 seconds; three failed
audit attempts are retained. Sources 344--354 are frozen. Next review
the global kernel/summation and identification before a larger search
or Hecke rebuild. No independent tangent or target field is obtained.

**Previous checkpoint: D92 complete norm-one control (2026-09-23).**
Read [the D92 report](../certificates/nelson-norm-one-control-d92.md).
Scripts 338--343 fix reduced norm to 1, enumerate 541 classes through
A=25600, independently prove coverage by interval recursion, and bound
the entire omitted norm-one family. Its `(1,1)` sum lies in [6193,8443]
in the D91 normalization. Other ideals and the global test-vector
comparison remain; there is no complete CM tangent evaluation.

```sh
python3 dembele/pari/343_nelson_norm_one_audit.py --check
```

Root `nelson_norm_one_d92.json` binds 51 files. The rational audit
replays majorants, all cutoff vectors/classifications, unit signatures,
LDL identities, nesting, inverse pairing and disk-average sums. Arb
recursion and Gamma/zeta nodes are bound to their runs. Twelve jobs
finished, eleven passes and one retained PARI flag-0 precision failure;
the maximum is 81.44 seconds. Sources 338--343 are frozen. Next test
the norm-31 prime b=27 using its saved Hecke data and prove its tail
argument before proceeding to other ideals. Do not just enlarge the
norm-one cutoff; higher derivative tails remain too wide for jets.

**Previous checkpoint: D91 Hilbert unfolding and partial evaluation
(2026-09-23).** Read [the D91 report](../certificates/nelson-hilbert-unfolding-d91.md).
Scripts 327--337 prove the cusp identity, remove central-unit duplicates,
extract 29 primitive classes, and enclose 42 Mellin kernels with all
auxiliary ideals and all beta powers. Missing Hecke coefficients remain
explicit variables. No complete eigenform or CM tangent is evaluated.

```sh
python3 dembele/pari/337_nelson_hilbert_audit.py --check
```

Root `nelson_hilbert_d91.json` has 44 hashes. The standard-Python audit
replays exact quaternion/unit identities and interval-output checks;
the Arb node and unit-logarithm calculations are hash-bound to their
bounded runs. Nine jobs completed: five passes and four preserved
development failures. Sources 327--337 and their artifacts are frozen.
The complete unit-cover bound is too large for direct enumeration;
next develop norm-ideal/hyperbolic enumeration and a tail bound, then
supply matched Hecke data and the global Shimizu test-vector comparison.
The report records a derivative scale discrepancy in the arXiv-v1
display and the independent calibration used by the implementation.

**Previous checkpoint: D90 Nelson kernel components (2026-09-23).** Read
[the implementation report](../certificates/nelson-totally-real-kernel-d90.md).
Scripts 320--326 implement local Fourier and derivative kernels, the
exact CM lattice splitting and bounded shells, and a numerical Mellin
prototype. There is no global theta-lift evaluation yet. Next derive
the Hilbert cusp/unit sum and evaluate one quartic-orbit eigenform with
a truncation bound. Recheck with standard Python:

```sh
python3 dembele/pari/326_nelson_kernel_audit.py --check
```

Root `nelson_kernel_d90.json` verifies 27 hashes, exact finite and lattice
arithmetic, 9,910 vectors and eight rational interval proofs. Six jobs
are complete, with three retained development failures. Their sources
and artifacts are frozen; D86--D89 files are unchanged.

**Previous checkpoint: D89 CM tangent input audit (2026-09-23).** Read
[the local arithmetic report](../certificates/cm-tangent-local-arithmetic-d89.md).
The order-two quotient needs upstairs differential degrees 1/3/5; the
Hecke correspondence introduces thirty conductor-changing branches with
unknown section derivatives. No independent arithmetic tangent is
computed. The new exact local calculation reads no candidate equations
or differential banks:

```sh
python3 dembele/pari/319_cm_tangent_local_arithmetic.py --check
```

Root `cm_tangent_local_arithmetic_d89.json` retains the local identities,
all neighbor multiplier tests, trace controls and source hashes. The
global section evaluator remains missing; prior bound files are unchanged.

**Previous checkpoint: D88 identification reviews (2026-09-23).** Read
[the CM-expansion review](../certificates/d88-cm-expansion-identification-review.md)
and [the cubic-shortcut review](../certificates/d88-cubic-identification-shortcut-review.md).
Independent arithmetic CM jets remain missing. After a marked arithmetic
identification of C and X, the existing nine-cover data would select the
canonical cubic by a conditional uniqueness argument. That identification
remains open, and further precision remains paused.
The D86/D87 computation sources and certificates remain unchanged.

The new small candidate diagnostic proves ranks 17/34/45 for the first
one/two/three coefficients at D17. Thus independent exact arithmetic
jets through t^2 would suffice with the rank and kernel checks in the
review. This does not compute those Shimura-side jets. Recheck with
`python3 dembele/pari/d88_candidate_cm_jet_rank_check.py --check`.
The successful Magma source is `../magma/d88_candidate_cm_jet_rank_v2.m`;
the failed first layout attempt and both bounded job records are retained.

**Previous checkpoint: D87 (2026-09-23).** The rational genus-40 candidate
has the expected numerical sign character on all 277 saved side generators.
Both saved differential banks and an alternative path family agree. Read
[the comparison](../certificates/cm-frame-double-cover-character.md).

```sh
python3 dembele/pari/318_cm_frame_double_cover_character_audit.py --check
```

This independently unwraps 192,405 retained samples and verifies 2,187
file hashes / 875 JSON records, including D86. It is not a certified
analytic comparison: geometry and differential tails remain uncertified.
The existing exact D77 fibre condition selects the scalar twist within
the fixed geometric half. Marked arithmetic identification and the
selected cubic class remain the next issues.

Scripts 306–310 evaluate the saved cover function and construct checked
finite-polynomial caches. Perturbed side points avoid elliptic fixed
points. Scripts 311–314 preserve uniform-mesh pilots and perform adaptive
continuation. Scripts 315–317 skip only ball-bounded finite-polynomial
tails, retaining every accepted continuation sample. This does not bound
the infinite differential tail. Script 318 uses standard Python for
independent phase reconstruction, sign comparison and provenance checks.
All 52 jobs are finished: 51 pass and the initial midpoint cache attempt
is rejected and preserved. Bound sources and outputs are immutable.

**Previous checkpoint: D86 (2026-09-23).** The actual cubic is now
independently verified modulo 31^128 in both models, including all
highest-digit error controls. The 112/16 joint F-recognition experiment
is negative at every embedding. Exact integer certificates exclude
homogeneous height <=348,750,355,384,078 in the fixed bases; they do not
exclude F. Read [the completed run](../certificates/cm-frame-cubic-128-chatelet.md)
and the top of [HANDOFF.md](../../HANDOFF.md).

```sh
python3 dembele/pari/303_cm_frame_cubic128_audit.py --check
```

This verifies 2009 file hashes / 769 JSON records, all eight exact
integer height identities, the 64-digit reduction and 21 remote job
records. All jobs are finished. Scripts 298–300 run bounded remote Magma;
302 schedules independent checks; 304/305 resume idempotent transfers
through transient network errors while preserving guarded launches.
The mathematical sources, earlier failures and successful receipts are
immutable. Recognition uses 274 with `--digits 128 --train 112`; height
certificates use 301. The standalone coefficient package is
`cm_frame_cubic_adjoint_package_128.json`.

Further precision is paused. Next compare the explicit marked cover
with the canonical arithmetic cover or prove the missing global class
action. D85's review remains relevant, but 297's historical no-result
assertions no longer describe this workspace. Use 303 for the current
audit. The descriptions below are historical.

These scripts implement D43–D80. They compute a domain for Dembélé's genus-16
normalizer quotient, then its exact local S3 monodromy and genus-64 cover
data. They do not yet compute exact target curve models or target torsion.

D80 adds scripts 180–183: the normalized cubic has 68/2818 points
over F31/F31^2, matching the Hecke prediction. Exact local expansions
resolve 6/12 exceptional fibres. A separate check counts every fibre
using quadratic splitting and Kummer cube tests, with different local
parameters, and rejects a changed count. The two measured power traces
are -36,-1856. Read [the D80 report](../certificates/cm-frame-cubic-frobenius.md).

```sh
python3 dembele/pari/183_cm_frame_cubic_point_check.py --collect-only
python3 dembele/pari/183_cm_frame_cubic_point_check.py
python3 dembele/pari/183_cm_frame_cubic_point_check.py --rebuild
```

The data and completed certificate are `cm_frame_cubic_point_counts.json`
and `cm_frame_cubic_point_check.json`. Next attempt a bounded lift modulo
31^2 of the marked cubic class and function identities. The two traces
support the candidate; they do not prove the full Euler factor or
identify the prescribed arithmetic cover.

D79 adds scripts 176–179: an explicit cubic over the candidate C modulo
31, with smooth projective normalization of genus 64. The S3 closure
has genus 136 and quadratic resolvent the saved X. The equation
Q4*T^3-3*A4*Q4*T-P10=0 has coefficients in F31 and weight(T)=2.
The constructor descends the third's representative, recovers h=27*u/q
and a=27*f, and proves h*tau(h)=a^3. The separate verifier checks all
saved divisor/function identities and coefficients on 1,024 points;
wrong norm and trace coefficients are rejected. Read
[the D79 report](../certificates/cm-frame-cubic-cover.md).

```sh
python3 dembele/pari/179_cm_frame_cubic_check.py --collect-only
python3 dembele/pari/179_cm_frame_cubic_check.py
python3 dembele/pari/179_cm_frame_cubic_check.py --rebuild
```

Data are `cm_frame_cubic.{json,m}`; the completed verification is in
`cm_frame_cubic_check.json`. D80 completes two Frobenius comparisons;
lifting the marked cubic 31-adically is next. The intended monodromy and arithmetic
identification remain open; the denominator-cleared equation alone
does not give normalized special fibres for point counting.

D78 adds scripts 164–175 and a verified third of the cubic branch
class on the genus-40 candidate modulo 31: 3[A]=-[D+-D-]. A is
fixed by Frobenius and negated by the cover involution. Exact section
spaces have dimensions 81,201,321 on 640 evaluation points, with
explicit branch representatives. The proposed class order only guides
a scalar search; the saved relation is verified without it and a
wrong class is rejected. Read
[the D78 report](../certificates/cm-frame-cover-class-arithmetic.md).

```sh
python3 dembele/pari/174_cm_frame_cover_check.py --collect-only
python3 dembele/pari/174_cm_frame_cover_check.py
python3 dembele/pari/174_cm_frame_cover_check.py --rebuild
```

D79 completes the function, representative descent and genus-64
quotient modulo 31. No characteristic-zero cubic or arithmetic
monodromy match is yet obtained. GP 169's 180-second class
arithmetic timeout is archived; the finite-field Magma replacement
170–175 succeeds. Do not repeat that unchanged timeout.

D77 adds scripts 157–163. The normalized B3 fibre of D76's rational
genus-40 cover is exactly K(sqrt(-3)), with K the degree-nine residue
field. Exact jets give its leading unit alpha, and an explicit witness
proves alpha=-3*s^2. A rational linear parameter gives two oriented
degree-nine divisors over Q(sqrt(-3)), exchanged by the involution.
Modulo 31 each has factor degrees [3,3,3]. Independent verification
passes and rejects a corrupted unit. Read
[the D77 report](../certificates/cm-frame-B3-fiber.md).

```sh
python3 dembele/pari/162_cm_frame_B3_fiber_check.py --collect-only
python3 dembele/pari/162_cm_frame_B3_fiber_check.py
python3 dembele/pari/162_cm_frame_B3_fiber_check.py --rebuild
python3 dembele/pari/163_cm_frame_B3_branch_class.py
```

The necessary cubic inertia condition now selects the F-scalar twist
of this fixed branch half. Script 163 proves D+-D- nonprincipal from
h0_X(pi^*B3)=1. D78 represents this difference in the genus-40 divisor
class group and finds a third modulo 31. D79 constructs its function
and cubic; the prescribed S3 monodromy match remains open.

D76 adds scripts 146–156 and an **exact rational double cover** of the
certified genus-16 candidate. Its integral numerator and denominator
have heights 583 and 2935433, and its normalization has genus 40.
The moving section lift uses h*q=g*s to avoid lifting G's points.
Its six products give a rational space with short representatives;
exact Veronese identities then supply a square section. Rational
witnesses and good reduction prove the divisor statement. The saved
square-factor map agrees with the old cover through 31^128.
Independent checks pass and reject both a highest-digit error and
a wrong twist. Read [the D76 report](../certificates/cm-frame-rational-double-cover.md).

```sh
python3 dembele/pari/148_cm_frame_B3_lift_check.py --collect-only
python3 dembele/pari/148_cm_frame_B3_lift_check.py --rebuild
python3 dembele/pari/156_cm_frame_B3_rational_check.py --collect-only
python3 dembele/pari/156_cm_frame_B3_rational_check.py
python3 dembele/pari/156_cm_frame_B3_rational_check.py --reconstruct
```

Runner 156's reconstruction mode repeats 150–154 against saved lifts;
148 rebuilds those lifts separately. The equation and witnesses are
`cm_frame_B3_rational_model.{json,m}`, with combined certificate
`cm_frame_B3_rational_check.json`. D77 computes the normalized fibre
over B3 and its involution and constrains the scalar twist. Arithmetic
Shimura/half identification remains unproved; no genus-64
Y or target field polynomial is obtained. No additional precision
is the default next action.

D75 adds scripts 138–145. Joint projective F recognition fits at 64 digits
and validates at 128; all 765 tested denominator rows fail, while an
exact nontrivial F control succeeds. A separate inverse-matrix argument
excludes coefficient boxes up to 8066216 in the old bases. The geometric
normalization using B3 then produces an exact numerator of height 583.
Its square-factor transfer is independently certified modulo 31, including
rejection of a wrong twist. Read [the D75 report](../certificates/cm-frame-joint-field-and-B3-normalization.md).

```sh
python3 dembele/pari/141_cm_frame_joint_field_check.py --collect-only
python3 dembele/pari/141_cm_frame_joint_field_check.py --search
python3 dembele/pari/144_cm_frame_B3_check.py --collect-only
python3 dembele/pari/144_cm_frame_B3_check.py --rebuild
```

Both runners default to independent checks. D76 completes the B3
transfer using the saved 128-digit lift and recognizes a rational
cover through the full product space. The archived rational-ideal probe
timed out at 180 s/2 GB; its linear-membership/good-reduction replacement
finishes in 20.390 s. Do not repeat the old probe unchanged.

D74 adds scripts 130–137. Exact Newton doubling reaches 31^128 in
52.198 s including a 4->8 regression control. Independent divisor
certificates and transfers preserve the radicand at every saved stage.
Coefficientwise Q/F recognition fails unused-digit validation; this is
not a nonmembership proof. Scripts 134–136 construct, reduce and certify
the 17-dimensional rational denominator space. Its integer section
basis has heights 39–96 digits and exact paired polynomial witnesses.
Read [the precision-doubling report](../certificates/cm-frame-precision-doubling.md).

```sh
python3 dembele/pari/131_cm_frame_doubling_check.py --collect-only
python3 dembele/pari/131_cm_frame_doubling_check.py --lift --digits 128
python3 dembele/pari/137_cm_frame_arithmetic_check.py
python3 dembele/pari/137_cm_frame_arithmetic_check.py --collect-only
python3 dembele/pari/137_cm_frame_arithmetic_check.py --recognize
```

Runner 137's default independently checks the exact space and rejects
a changed highest coordinate digit. Its optional recognition mode
repeats the bounded searches and basis construction. The archived
generic-nullspace probe timed out at 300 s; the corrected script 135
uses the existing identity block and completes in 59.463 s. Do not
repeat the old probe unchanged. D75 implements the proposed joint
projective F recognition and moves on to a B3 normalization.

D73 adds `127_cm_frame_numerator_lattice.py`, Magma scripts 128–129,
and runner `129_cm_frame_normalization_check.py`. Saturated integer
kernels and LLL reduce the numerator's primitive height from 631 to
48 digits in the old section chart and to 39 digits when curve
relations are allowed. The denominator transfer preserves the same
ratio modulo 31^8, independently checked, with a highest-digit error
correctly rejected. Read [the normalization report](../certificates/cm-frame-normalization.md).

```sh
python3 dembele/pari/129_cm_frame_normalization_check.py
python3 dembele/pari/129_cm_frame_normalization_check.py --collect-only
python3 dembele/pari/129_cm_frame_normalization_check.py --rebuild
```

The search takes 53.058 s (240 s timeout, no Sage memory cap); transfer
9.987 s, verification 20.524 s and corruption control 14.501 s
(Magma: 180 s/2 GB). D74 implements the proposed precision doubling;
recognition over F remains open. The denominator's global height is unknown;
retain explicit scalar/isomorphism checks when changing normalization.

D72 adds Sage scripts `124_cm_frame_resolvent_lift.py` and
`126_cm_frame_lift_numerator.py`, Magma scripts 123 and 125, and the
standard-library runner `125_cm_frame_resolvent_lift_check.py`.
They lift the double-cover equation compatibly through 31⁸ and
independently certify the full divisor relation. Read
[the lifting report](../certificates/cm-frame-resolvent-lift.md).

```sh
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py --collect-only
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py --lift --digits 8
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py --calibrate
```

Each lifting step solves 32 numerator constraints, 44 denominator
constraints, and the positions of sixteen double zeros in exact
finite étale algebras. All stages reduce compatibly. The full Sage
lift takes 38.547 s including startup (240 s timeout); the independent
Magma certificate takes 2.351 s (120 s/2 GB), and a newest-digit error
is rejected. Sage jobs have no imposed 2 GB memory cap.
Script 126 independently recovers the numerator over Q and matches
all eight digits. Its primitive height has 631 decimal digits in
that earlier normalization; D73 above replaces it with a 39-digit
numerator and transfers the denominator. The full cover over a number
field and its Shimura identification remain open.

D71 adds the runner `122_cm_frame_resolvent_check.py` and Magma
scripts 121–122. They construct and independently certify an exact
genus-40 double cover of the candidate over F31, branched at D17+P32.
Its two constant twists have 45 and 55 rational points, with 45
matching the norm-one Hecke prediction. Read
[the resolvent report](../certificates/cm-frame-resolvent.md).

```sh
python3 dembele/pari/122_cm_frame_resolvent_check.py
python3 dembele/pari/122_cm_frame_resolvent_check.py --collect-only
# Optional: repeat the full divisor-halving discovery before checking.
python3 dembele/pari/122_cm_frame_resolvent_check.py --discover
```

The independent verifier takes 10.897 s under a 120 s/2 GB limit;
discovery takes 466.760 s under 900 s/2 GB. The Hecke Jacobian-order
guess proposes a half class; the final exact divisor identity makes
the finite-field cover independent of that assumption. It does not
prove the guessed order or uniqueness. A changed numerator is rejected
by a saved negative control. The next gate is a first 31-adic lift of
the half line bundle modulo 31², then recognition over F and matching
the sign monodromy. Those steps and the genus-64 cover remain open.
The function-field conversion/reduction timeouts are retained;
canonical quadric/colon-ideal arithmetic succeeds instead.

D70 adds Sage script `119_cm_frame_marks.py` and the standard-library
runner `120_cm_frame_marks_check.py`, with Magma script 120. They recover
an exact ordinary rational point and exact closed divisors of degrees
17 and 9 on the verified curve candidate. Seven integer linear forms
of height at most 54 cut out the nonic divisor, whose residue field has
proved Galois group 9T15. All marks are disjoint and reduce well at 31.
The CM labels remain numerical. Read [the marked-divisor report](../certificates/cm-frame-marks.md).

```sh
DOT_SAGE=/private/tmp/dembele-d70-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/119_cm_frame_marks.py
python3 dembele/pari/120_cm_frame_marks_check.py
python3 dembele/pari/120_cm_frame_marks_check.py --collect-only
```

Script 119 uses the existing two differential banks and takes about
20 seconds. Script 120 imposes a 120-second/2 GB limit; its recorded
Magma job passes in 46.070 seconds. The exact residual-ideal test also
excludes `B2 ~ 2 B3`, where B2=D17+P32. The next cover task requires
the correct quadratic-resolvent square class and the full S3
monodromy, not just the branch supports. No such reconstruction
algorithm is yet implemented. A separate default nonic maximal-order
probe timed out at 90 seconds; its failure record is preserved.

D69 adds the standard-library Python runner `117_cm_frame_verification.py`
and Magma scripts 117–118. They prove that the unchanged D68 equations
define a smooth canonical genus-16 curve over Q with good reduction at 31.
Direct counts 50 over F31 and 1,400 over F31² match the saved Hecke data.
Identification with the intended Shimura curve remains open. Read
[the verification report](../certificates/cm-frame-verification.md).

```sh
python3 dembele/pari/117_cm_frame_verification.py
python3 dembele/pari/117_cm_frame_verification.py --collect-only
```

The runner gives each of its three Magma jobs a 180-second timeout and
2 GB memory cap, checks explicit completion/error markers, and records
source/log hashes. Its smoothness certificate uses squarefree trace
discriminants of a finite free projection, avoiding the failed D68
Jacobian-minor and normalization probes. Collection checks the saved
hashes and recomputes point totals from individual fiber records.

D68 adds scripts 114–116. They use the seventeen CM points to fix
arithmetic canonical coordinates, discover 91 integer quadrics, and
check the resulting candidate over Q and modulo 31. The equation
coefficients are bounded by 1,514; degree 30 and arithmetic genus 16
are verified. D69 subsequently proves smoothness; identification with
the intended curve remains open. Read [the construction report](../certificates/curve-construction-sources-2026-09-18.md).
This is the current research direction; D67's optional backend
cleanup is paused. The candidate is saved as
`../data/computed/cm_frame_curve_candidate.{json,m}`.

```sh
DOT_SAGE=/tmp/dembele-d68-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/114_cm_projective_frame.py
DOT_SAGE=/tmp/dembele-d68-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/115_cm_frame_quadric_search.py
DOT_SAGE=/tmp/dembele-d68-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/116_cm_frame_curve_check.py
```

Script 115's 60-second timeout covers its final LLL subprocess, not
the preceding exact lattice setup. Its complete recorded run takes
86.61 seconds. Script 116 applies a 180-second limit and 2 GB memory
limit to its Magma job and requires explicit pass markers with no
Magma error messages. Separate general-smoothness and normalization
probes respectively hit a minor-count limit and a 180-second timeout;
they do not certify a smooth genus-16 curve.

D62 adds `99_curve_identification.py`, an audit of the saved maximal
order, unit signatures and full genus-40 reduction graph. Read
[`curve-identification-audit.md`](../certificates/curve-identification-audit.md).
It supports the identification behind D45, including reversed edges at 2.

D62 also builds Mascot's pinned LiftTors and exercises its actual divisor
arithmetic. `100_lifttors_control.gp` completes the known Q8 example through
7-adic lifting and field recovery. `101_lifttors_scale.gp` passes at genus
16; D62's genus-64 lift failed at a 2 GB stack limit. The exact batched
validator in `lifttors_bounded.c` is compared with upstream by script 102.
Read [`lifttors-control.md`](../certificates/lifttors-control.md) for scope,
timings and the original memory failure.

D63 adds `lifttors_lift.py` and `lifttors_streamed.c`: products are
formed inside workers, and the lifting kernel is solved using selected
rows with verification against every equation. The genus-64 control now
passes under the same cap, with one lift taking about 10.2 minutes.
Script 103 compares 60 lifts with upstream; script 104 checks 12 known
kernels and 6 rank-drop rejections. Read
[`lifttors-memory.md`](../certificates/lifttors-memory.md). The default
build includes both changes; `--products-only`, `--validator-only` and
`--upstream` reproduce progressively earlier algorithms for diagnosis.

```sh
DOT_SAGE=/tmp/dembele-d62-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/99_curve_identification.py
python3 dembele/pari/build_lifttors.py
python3 dembele/pari/run_lifttors_controls.py
```

The pinned checkout lives in ignored `../vendor/LiftTors`; revision and
source URL are in `../upstream.lock`. Build once from that revision.
The control runner uses a 900-second per-process timeout and the 2 GB
PARI stack cap, writes `lifttors_controls.json`, and currently exits 0
with all controls passing. `--collect` reuses existing logs. Historical
failed runs remain recorded as failures in the memory diagnostics.
The GP comparisons and 111 existing regression tests are separate counts.
Genus-64/residue-degree-51 cost and production precision remain untested;
no target arithmetic evaluation construction has been supplied.

D64 adds `105_lifttors_extension.py` and `106_lifttors_row_system.gp`.
The genus-4 control passes at a=2 and a=51, with one lift taking
0.264 s and 8.356 s respectively. A row-generation formula agrees with
all 11,172 entries in four small systems and passes every kernel check.
It is a GP prototype; the C backend is unchanged. Entry-size projections
motivate integrating that formula before a genus-64/a=51 attempt. Read
[`lifttors-extension.md`](../certificates/lifttors-extension.md).

```sh
python3 dembele/pari/105_lifttors_extension.py
```

The existing D63 build and report are checked by digest. This runner
uses the same cap/timeout, writes `lifttors_extension.json`, and supports
`--collect` for the four saved logs. It never launches genus 64 at
degree 51. Object-tree sizes and projections are not peak-memory
measurements. The target arithmetic section construction is still open.

D65 implements the checked formula in `lifttors_rows.c`, with source
adaptation in `lifttors_rows.py`. A separate build preserves the D63
library and every D63/D64 source and log. The new library's
`PicLiftTors` generates row blocks and verifies every equation;
`PicLiftTors_D63` and `PicLiftTors_original` retain both comparison paths.
Read [`lifttors-rows.md`](../certificates/lifttors-rows.md) for results,
storage diagnostics and scope.
The genus-64/a=2 lift passes in 514.585 s (690.829 s for the full
control), and its largest equation block is 7.34 MB. This reduces
equation storage by 66 in entry count; other allocations still reach
the same 2 GB stack cap. All nine D65 jobs pass.

```sh
python3 dembele/pari/build_lifttors_rows.py
python3 dembele/pari/107_lifttors_rows.py
```

The runner generates checked copies of the existing GP controls under
`.build/lifttors_rows/controls`, preserving their original sources.
`--collect` reuses logs; `--only` runs named controls without issuing a
full-suite report. Its equation comparisons, three-way lift comparisons,
known kernels, rejection cases and Q8 field recovery exercise the native
path. Stack cap and timeout remain 2 GB and 900 seconds per process.
There is no genus-64/a=51 job in this suite.
D66 runs the optional intermediate control
`python3 dembele/pari/107_lifttors_rows.py --only genus16_a51`.
It passes in 439.776 s overall, including a 364.194-second lift, under
the unchanged cap/timeout. Its two kernel stages account for about
11% of lift time. The next allocation audit concerns retained Jacobian
data, Schur setup and group operations before any genus-64/a=51 job.

D66 also finds a separate upstream defect: `PicRed` reduces vectors
of auxiliary embedding matrices as though they were ordinary matrices.
`build_lifttors_reduction.py` creates a separate corrected build,
preserving D63–D65 and retaining `PicRed_original` for diagnosis.
Script 110 reproduces the error; script 111 tests correct reduction,
composition and projective evaluation; script 109 measures retained
component storage. Script 108 runs or collects these and the corrected
lifting/known-field controls. Read
[`lifttors-degree51.md`](../certificates/lifttors-degree51.md).

```sh
python3 dembele/pari/build_lifttors_reduction.py
python3 dembele/pari/108_lifttors_degree51.py
```

`--collect` checks saved logs and source hashes. `--only` selects jobs
without writing a full report. The report is `lifttors_degree51.json`.
The old-library and corrected-library scale logs are separate. No
genus-64 job is included in the corrected-build suite; the saved D65
genus-64 result remains specific to its recorded library. No target
arithmetic sections or nonsolvable polynomial have been obtained.

D67 adds a separate diagnostic build via `build_lifttors_profile.py`
and `lifttors_profile.{h,c,py}`. Removing its hooks recovers the original
C tokens; twenty tracing-off/on cases preserve exact matrices and RNG
states. Genus-4/a=51 and genus-16/a=51 controls both pass under the
same cap/timeout. The larger control takes 444.494 s overall and shows
an obsolete product workspace retained through group operations.
Read [`lifttors-allocation.md`](../certificates/lifttors-allocation.md).

```sh
python3 dembele/pari/build_lifttors_profile.py
python3 dembele/pari/112_lifttors_profile.py
```

`--collect` checks saved results, source equivalence, provenance and
trace nesting; `--only` selects jobs without writing a full report.
The report is `lifttors_profile.json`. Measurements are stack checkpoints
and object-tree sizes, not peak RSS. The next experiment moves the
Schur cleanup mark before GWV and collects `DivMul` outputs. Those
changes are not yet implemented. All D63–D66 artifacts remain preserved;
no genus-64/a=51 job, cap increase or target section construction follows.

D60 adds `98_cm_flag_height.py`. It forms exact rational chart boxes
from D59's saved decimal coordinates, then proves height exclusions
for Q X, Q Y and span(X,Y) using lattice and exterior-power bounds.
The boxes are empirical: the certificate proves an exclusion inside
each box, not target membership or an unconditional target-height bound.
Read [`cm-flag-height.md`](../certificates/cm-flag-height.md).

```sh
DOT_SAGE=/tmp/dembele-d60-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/98_cm_flag_height.py
DOT_SAGE=/tmp/dembele-d60-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/98_cm_flag_height.py \
  --verify dembele/data/computed/cm_flag_height.json
```

Outputs are identical `../data/computed/cm_flag_height.{json,out}`,
including exact matrices, interval definitions, bounds and source hashes.
The verification command uses exact arithmetic without a new LLL run.
Eight new controls bring the full suite to 111 passing tests. No new
analytic bank is generated and no exact target value is recognized.

D59 adds `96_cm_orbit.py`, `97_cm_field_recognition.py` and the companion
`../magma/96_cm_root_action.m`. Read
[`cm-orbit-recognition.md`](../certificates/cm-orbit-recognition.md) for
the exact ideal-class construction, arithmetic Frobenius matching and
explicit numerical/software inputs to complex orientation. The joint
reconstruction uses all seventeen CM values in a stable trace-centered
basis of the known degree-17 field. It accepts no direction at the
default height cap 10^9; this is not exhaustive height exclusion.

```sh
/Applications/Magma/magma -b dembele/magma/96_cm_root_action.m \
  > dembele/data/computed/cm_root_action.out
DOT_SAGE=/tmp/dembele-d59-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/96_cm_orbit.py
DOT_SAGE=/tmp/dembele-d59-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/97_cm_field_recognition.py
```

Run sequentially from the repository root. Outputs are the Magma log
and identical pairs `../data/computed/cm_orbit.{json,out}` and
`cm_field_recognition.{json,out}`, including source hashes and all
bases/permutations. The existing domain, Rickards plugin and four
CM-value banks are required. Script 96 supports `--gp` and `--root-action`;
script 97 supports `--height-cap`. Seven new controls bring the full
suite to 103 passing tests. No new analytic bank is generated.

D58 adds `95_marked_descent.py`. Read
[`marked-descent.md`](../certificates/marked-descent.md) for the compatible
marked descent argument, the conditional Q-definition of X,Y, and its
literature dependencies. The script verifies class numbers and invariant
prime identities, then runs exact bounded rational-interval tests on the
four saved CM polynomial banks. These intervals are empirical, not
certified errors. No complete polynomial is recovered at the default
denominator bounds 10^3,10^4,10^5,10^6.

```sh
DOT_SAGE=/tmp/dembele-d58-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/95_marked_descent.py
```

Results are the identical `../data/computed/marked_descent.{json,out}`.
Six new controls include exhaustive small-denominator comparisons,
semilinear normalization, and recovery of a known exact polynomial.
All 96 tests pass. The script does not compute explicit descent maps
or create new analytic banks; `--bounds` changes the bounded pilot.

D57 adds `94_cm_arithmetic.py`, an exact audit using the saved domain,
Elkies's CM residue-field polynomial, and the existing CM-value report.
It checks all seventeen quadratic embeddings, the cyclic CM field,
finite residue algebras, and two exact counterexamples to field-only
reconstruction. It does not recompute analytic differentials or recognize
target values. Read `../certificates/cm-arithmetic-input-audit.md` for the
precise missing evaluation flag and the source-theorem dependencies.

```sh
DOT_SAGE=/tmp/dembele-d57-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/94_cm_arithmetic.py
```

The JSON and identical `.out` are `../data/computed/cm_arithmetic_audit.*`.
Use `--gp` to override the PARI executable. The existing Rickards plugin
and domain are required. All 90 tests pass, including six new exact
controls; the known field polynomial is not the desired nonsolvable
field polynomial or the polynomial of the target X-values.

D51 adds `80_cover_geometry.gp` and `81_belyi_cover.py`, which feed the
user's existing Belyi Cauchy/Arnoldi implementation with this cover's
geometry and separate the standard S3 component. See
`../certificates/belyi-cover-pilot.md` and `../certificates/target-realization.md`.
The current cover bank is `belyi_cover_pilot_4096.npz`, containing 48
numerical candidate directions with worst sampled side error 2.75e-5.
It is not an exact model or a certified basis. Set `BELYI_ROOT` or use
`--belyi-root` to select the existing Belyi checkout; it is read, not edited.

D52 adds `83_pointed_normalization.py` and the independent exact reference
`../../belyi/pointed_series.py`. Read
`../certificates/pointed-normalization.md` for the conditional F-parameter
argument, exact thesis-curve controls, and the remaining conditioning
problem. The default numerical comparison selects 48 coefficient indices
among 60 and keeps those indices fixed across the 4096/2048 cover banks:

```sh
DOT_SAGE=/tmp/dembele-pointed-sage sage -python belyi/pointed_series.py \
  --output dembele/data/computed/pointed_normalization_control.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/83_pointed_normalization.py \
  --output dembele/data/computed/pointed_evaluation_4096_60.json
```

Run these commands from the repository root. `--gauge initial --length 64`
retains the ill-conditioned first-48 diagnostic; `--length 96` reproduces
the longer selection trial. Sixty-digit arithmetic acts on double source
inputs. The default trial's unselected coefficients still disagree by
about 10%; no algebraic recognition has been attempted or justified.

D53 adds `84_relative_cubic.py`, a bounded comparison of symmetric trace
data for the degree-three Y/C cover. It reuses the saved banks and script
81's geometry. Read `../certificates/m23-coordinate-review.md` for the
M23 sources, recovered earlier-session code, relative-cubic argument,
successful complex comparison and unsuccessful arithmetic line choices.

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/84_relative_cubic.py \
  --marked-scan --output dembele/data/computed/relative_cubic_4096.json
```

Without `--marked-scan`, only the complex alignment and trace comparisons
run. The default complex direction is not proved F-defined. The optional
scan uses 50 working digits for formal substitutions on double inputs;
it does not produce 50 accurate digits. Next: adapt the base-quadric
recovery to D52's arithmetic normalization before further recognition;
D54 implements this step below.

D54 adds `85_arithmetic_quadrics.py`, `86_precise_quadrics.py`,
`87_quadric_recognition.py`, `88_pointed_invariant.py`, and
`89_quadric_lattice.py`. Read
`../certificates/arithmetic-quadrics.md` for the fixed, short change of
canonical basis, independent truncation checks, bounded recognition
results and exact controls. Long formal-coordinate substitution is
unnecessary for recovering homogeneous equations. Script 86 preserves
arbitrary-precision coefficient strings; its arithmetic balls do not
bound geometric or infinite-series errors.

```sh
DOT_SAGE=/tmp/dembele-d54-sage OPENBLAS_NUM_THREADS=4 \
  sage -python dembele/pari/86_precise_quadrics.py \
  --basis dembele/data/computed/acb_refinement_16384.acb \
  --rows-from dembele/data/computed/precise_quadrics_8192.json \
  --comparison dembele/data/computed/precise_quadrics_12288.json \
  --output /private/tmp/precise_quadrics_16384.json
OPENBLAS_NUM_THREADS=1 sage -python dembele/pari/87_quadric_recognition.py \
  --basis dembele/data/computed/precise_quadrics_16384.json \
  --comparison dembele/data/computed/precise_quadrics_12288.json \
  --samples 4095 --tolerance 1e-18 --field-height 16 \
  --field-basis cosine --scale-invariant \
  --output /private/tmp/quadric_recognition_invariants_16384.json
```

Script 87's `--field-height` changes the degree-eight search bound only.
`--scale-invariant` uses ratios with matching monomial weight. All hits
are tentative. Script 88 instead checks `A3^2/A2^3`, the simplest
scale-free pointed jet invariant, using native checkpoints directly.
The n=16384 equation searches find no candidates in either integral
basis or the scale-invariant ratios. The native side defect is 3.86e-20;
this is a sampled diagnostic, not certified coefficient accuracy.

Script 89 also searches the whole space of equations by bounded LLL,
with an integer height limit and full-precision residual checks. Its
`--min-weight 20` and `--min-weight 22` options isolate subspaces of
dimensions 11 and 2 using the marked-point flag. Both smaller searches
finish without accepted equations. Candidate checks include all 45
quotient constraints, even when fewer enter the lattice. No exact C or
Y has been recovered. D54's 71 tests pass.

D55 adds `90_marked_pencil.py`. Read `../certificates/marked-pencil.md`.
It tests all 60 normalizations of the five leading coefficient-zero
points of the weight-22 pencil, giving 30 distinct cross-ratio expressions.
The default `--method direct` reconstructs this pencil from 25 native
differential products and improves fit agreement over the saved quotient
matrix. `--method quotient` reproduces the initial approach.

```sh
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/90_marked_pencil.py \
  --heights 4 8 16 32 --output /private/tmp/marked_pencil_direct.json
DOT_SAGE=/tmp/dembele-d55-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/90_marked_pencil.py --basis-gauge flag \
  --best-only --heights 4 8 16 32 64 \
  --audit-candidates dembele/data/computed/marked_pencil_16384.json \
  --output /private/tmp/marked_pencil_flag.json
```

`--basis-gauge flag` uses only the first 16 raw jets and column balancing;
the marked cross-ratios are invariant under this triangular basis change.
`--best-only` searches the two coordinates of the best chart, while
`--skip-recognition` only computes the charts and comparisons.
The optional candidate audit deduplicates previous matches exactly in F
and checks all six equivalent charts against the current empirical
accuracy. The initial apparent match fails; the direct searches find
no replacement. No geometric error bound or exact algebraic equality is
certified. All 78 tests pass, including the user's thesis Q8 control.

D56 adds `91_pointed_map.py`, `92_cm_fibers.py`, and
`93_pointed_map_model.py`. See `../certificates/cm-pointed-maps.md` for
the conditional arithmetic construction and the numerical limitations.
Script 91 obtains functions with poles 17P and 18P by section
multiplication; script 92 normalizes them by traces over the seventeen
order-two CM points. These X,Y have a conditional F-definition independent
of the complex input basis, and their coprime degrees imply F(C)=F(X,Y).

```sh
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/91_pointed_map.py --basis-gauge flag \
  --output /private/tmp/pointed_map_flag.json
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/92_cm_fibers.py \
  --map /private/tmp/pointed_map_flag.json \
  --output /private/tmp/cm_pointed_maps_flag.json
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/93_pointed_map_model.py \
  --cm-report /private/tmp/cm_pointed_maps_flag.json --y-shift 3 \
  --output /private/tmp/pointed_map_model_balanced3.json
```

Script 91's alternative `--basis-gauge arithmetic` uses the older D52
normalization. Script 93 compares rational uniformizers and attempts
a 172-term plane relation after clearing denominators. The shifted
coordinate improves numerical rank, but all equation fits fail unused
or held-out unweighted rows. The final saved diagnostic is
`pointed_map_model_balanced3_16384.*`; earlier unshifted/shifted reports
are exploratory records. Rejected coefficients must not be recognized
or used as height estimates. No exact equation is recovered. All 84
tests pass, including the user's thesis Q8 curve and a corrupted-equation
rejection control. Arithmetic balls still do not bound geometric errors.
The full test output is saved in
[`pointed_maps_tests_20260916.out`](../data/computed/pointed_maps_tests_20260916.out).

## Software and build

Upstream: [James Rickards, Fundamental domains for Shimura curves](https://github.com/JamesRickards-Canada/Fundamental-domains-for-Shimura-curves),
`klein` branch, commit `79a12d3f108edce3e78d30c4a59dfc0fb01012d8`.
The checkout is ignored by the parent repository; preserve its upstream GPL
license when redistributing it. The local scripts and patch are tracked here.

The tested PARI is 2.17.1, bundled with SageMath 10.6 on arm64 macOS. Two
matrix-trace calls in current upstream need the equivalent generic `gtrace`
and reduction modulo p on this version. The patch changes only these calls.
The loader uses an absolute shared-library path because the bundled GP
binary rejects relative paths. `build_rickards.py` makes both adjustments
and overrides the stale build-machine paths in Sage's `pari.cfg`.

From the repository root, with an existing compatible PARI installation:

```sh
git clone --branch klein https://github.com/JamesRickards-Canada/Fundamental-domains-for-Shimura-curves.git dembele/vendor/rickards-fdom
git -C dembele/vendor/rickards-fdom checkout 79a12d3f108edce3e78d30c4a59dfc0fb01012d8
python3 dembele/pari/build_rickards.py
python3 dembele/pari/run_fdom.py smoke
python3 dembele/pari/run_fdom.py domain
python3 dembele/pari/run_fdom.py cover
```

The build script's `--pari-local` and runner's `--gp` options select another
installation. The default paths match this workstation. The runner terminates
its child after `--timeout` seconds (default 600), captures output, and requires
the stage's final PASS marker because GP may exit zero after an error. It
publishes generated artifacts atomically after success, preventing GP's
append-style output functions from accumulating duplicate records.

The domain already exists in `data/computed/normalizer_domain.bin`; `cover`
replays from it in about a second. Binary compatibility is PARI-dependent;
rebuild `domain` with the pinned setup if loading it fails.

## Outputs and checks

- `normalizer_domain.bin`: PARI object with algebra, order, polygon and presentation.
- `normalizer_domain_presentation.gp`: exact quaternion generators and relations.
- `normalizer_s3_images.gp`: images of presentation generators and elliptic elements.
- `genus64_cosets.gp`: images of side generators, coset words and quaternion representatives.
- `normalizer_domain.out`, `local_s3_cover.out`, `rickards_smoke.out`: validation logs.

Script 65 checks signature `(16; 2^17,3^9,32)`, absence of cusps and
`afuchcheck`. Script 66 constructs the residue field as the semisimple
quotient of O/2, checks the local homomorphism on relations and products,
proves its image has six elements, determines elliptic monodromy, and
computes first rational Betti number 128 from the lifted presentation.
Its coset representatives specify three translated parent polygons for the
genus-64 subgroup; they are not a normalized Dirichlet polygon for that subgroup.

The geometric radius output only measures decay of `r^N`. It is not a
Taylor-tail estimate or a prediction of total model-construction cost.
See `../certificates/genus64-cover.md` for the mathematical interpretation.

## Numerical differentials and canonical relations (D44)

See `../certificates/genus16-differentials.md` for the results, failed
pilots, and an unresolved conflict with published hyperellipticity.
The strongest output has 16 differential candidates and 91 numerical
canonical quadrics. It is not an algebraic model over a number field.

Run from the repository root (Sage Python supplies NumPy/SciPy/mpmath):

```sh
python3 dembele/pari/run_fdom.py geometry
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/69_cm_sector.py
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/68_cm_differentials.py --n 4096 --radius 0.99991 --output dembele/data/computed/cm_differentials_4096_fullradius.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/68_cm_differentials.py --n 8192 --radius 0.99991 --solver eigen --output dembele/data/computed/cm_differentials_8192_eigen.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/68_cm_differentials.py --n 8192 --radius 0.99991 --solver refine --initial dembele/data/computed/cm_differentials_8192_eigen.npz --replay-digits 50 --output dembele/data/computed/cm_differentials_8192_refined.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/70_differential_audit.py
```

The dense 8192-square complex matrix alone occupies about 1 GiB, with extra
workspace needed by the solver. Scripts write JSON diagnostics and NPZ
arrays; operator selection alone never certifies a basis. Inspect the
independent residuals. Avoid the retained `8192_mp` and `8192_block`
outputs, which are failed pilots. The successful solve uses a stabilization
of I-A, since ordinary power iteration diverges for this Cauchy operator.

`differential_audit.npz` stores a right basis transformation and 91 quadric
columns, indexed by monomials X_i X_j for 0<=i<=j<16 in lexicographic order.
The product rank is 45 rather than the hyperelliptic 31. The D44 certificate
explains the numerical evidence; D45 resolves the discrepancy as follows.

## Exact hyperellipticity obstruction (D45)

The curve is nonhyperelliptic by its stable-reduction graph. See
`../certificates/hyperellipticity-audit.md` for the proof and assumptions.

```sh
sage -python dembele/pari/71_stable_graph.sage.py
HMF_ROOT=/Users/musty/hilbertmodularforms /Applications/Magma/magma -b dembele/magma/72_stable_graph_brandt.m
sage -python dembele/pari/73_brandt_graph_check.py
```

Script 71 checks all 19 involutions using two independent automorphism
enumerators and constructs their quotients; none is a tree. Script 72
recomputes the norm-2 Brandt operator with Minkowski proof bounds and an
exact mass check. Script 73 constructs and stabilizes its weighted graph,
then verifies its isomorphism to the graph tested in script 71.
Outputs: `stable_graph_audit.*`, `stable_graph_brandt.*`,
`brandt_graph_check.*`. This is independent of the Taylor-series solver.

## Quadratic generation and fixed CM normalization (D46)

See `../certificates/canonical-gauge.md`. Script 76 supplies an exact
minor witness excluding trigonality, so Petri guarantees that quadrics
generate the canonical ideal. Script 74 fixes the basis/period gauge and
exports real numerical equations, still awaiting arithmetic recognition.

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/68_cm_differentials.py --n 10240 --radius 0.99991 --solver refine --initial dembele/data/computed/cm_differentials_8192_refined.npz --replay-digits 50 --output dembele/data/computed/cm_differentials_10240_refined.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/74_canonical_gauge.py
sage -python dembele/pari/75_gauge_recognition.py
sage -python dembele/pari/76_quadric_generation.py
```

The first step is ~87 seconds on this workstation and needs several GiB
of memory. The other scripts finish quickly. Outputs are
`canonical_gauge.*`, `gauge_recognition.*`, `quadric_generation.*`.
The NPZ quadric columns use the included monomial order and have one
designated free monomial of coefficient one each. Small relation residuals
are not error bounds for their coefficients. The recognition pilot is
explicitly tentative and found no candidates within its small bounds.

## Mixed precision and hyperelliptic reconstruction (D48)

See `../certificates/newton-and-hyperelliptic-ansatz.md` for the distinction
between a successful small linear-solver prototype and full-size accuracy.
Script 77 tests reconstruction on the target and known hyperelliptic controls.
Script 78 uses high-precision residuals and double LU corrections at N=64.

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/77_hyperelliptic_reconstruction.py
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/78_mixed_precision_refinement.py
```

## Compiled arbitrary-precision refinement (D49)

`cm_acb.c`, `cm_acb.py`, and script 79 provide native FLINT polynomial
evaluation and FFT, high-precision residuals and accumulated coefficients,
and a reusable double LU correction solver. See
`../certificates/compiled-precision-refinement.md` for the measured results
and the distinction between a finite-system residual and differential error.

The build needs a C compiler and the FLINT development files exposed by
`pkg-config flint`. It caches a shared library under the ignored `.build/`
directory; it does not install software. Under local Sage, pkg-config selects
FLINT 3.1.0. Each native column worker has a separate FFT plan and scratch
storage. `--threads` defaults to four and is separate from BLAS threads.

```sh
OPENBLAS_NUM_THREADS=4 sage -python -m unittest discover -s dembele/tests -v
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/79_acb_refinement.py \
  --n 64 --columns 2 --output /private/tmp/acb_refinement_64.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/79_acb_refinement.py \
  --n 8192 --columns 16 --threads 4 \
  --output /private/tmp/acb_refinement_8192.json
```

Always choose a new output stem. The JSON and `.out` include convergence,
arithmetic-rounding diagnostics, a larger quadrature with a changed offset,
and all 275 independent side transformations. For sixteen columns, the
JSON also contains high-precision normalized jets. `--comparison` accepts
an earlier sixteen-column script 79 JSON to compare those jets.

The `.acb` checkpoint preserves native values exactly. To read one with
Sage Python, add `dembele/pari` to `sys.path`, set `mpmath.mp.dps=70`, and
use `Backend(50).read(path, n, columns)` from `cm_acb`. The returned vector's
`to_mpmath(rows=64)` obtains its first 64 coefficients without rounding to
double. The checkpoint stores a finite-system solution, not a certified
differential basis. Geometry still has about 57 source digits; neither a
70-digit replay nor a tiny linear residual removes geometric/truncation error.
