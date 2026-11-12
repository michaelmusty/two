# Explicit Dembélé field

<!-- D157 higher pilot timing checkpoint -->

**Current checkpoint: D157 — the approved column-2 P3200-to-P6400 pilot
is complete.** The [D157 report](certificates/dyadic-higher-pilot-timing-d157.md),
[fixed review](data/computed/dyadic_higher_pilot_timing_review_d157.json),
[completion record](data/computed/dyadic_higher_pilot_timing_completion_d157.json) and
[source ledger](data/computed/dyadic_higher_pilot_timing_sources_d157.json)
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
The [D156 report](certificates/dyadic-higher-pilot-preparation-d156.md),
[fixed admission](data/computed/dyadic_higher_pilot_preparation_review_d156.json),
[completion record](data/computed/dyadic_higher_pilot_preparation_completion_d156.json) and
[source ledger](data/computed/dyadic_higher_pilot_preparation_sources_d156.json)
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
The [D155 report](certificates/proof-criterion-review-d155.md),
[fixed review](data/computed/proof_criterion_review_d155.json),
[completion record](data/computed/proof_criterion_completion_d155.json) and
[source ledger](data/computed/proof_criterion_sources_d155.json)
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
The [D154 report](certificates/dyadic-pilot-timing-d154.md),
[fixed review](data/computed/dyadic_pilot_timing_review_d154.json),
[completion record](data/computed/dyadic_pilot_timing_completion_d154.json) and
[source ledger](data/computed/dyadic_pilot_timing_sources_d154.json)
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
The [D153 report](certificates/dyadic-pilot-preparation-d153.md),
[fixed admission](data/computed/dyadic_pilot_preparation_review_d153.json),
[preparation completion](data/computed/dyadic_pilot_preparation_completion_d153.json) and
[source ledger](data/computed/dyadic_pilot_preparation_sources_d153.json)
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
The [D152 report](certificates/precision-route-cost-d152.md),
[fixed review](data/computed/precision_route_review_d152.json),
[completion record](data/computed/precision_route_completion_d152.json) and
[source applicability ledger](data/computed/precision_route_sources_d152.json)
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
The [D151 report](certificates/summed-transfer-obstruction-d151.md),
[fixed review](data/computed/summed_transfer_review_d151.json),
[completion record](data/computed/summed_transfer_completion_d151.json) and
[source applicability ledger](data/computed/summed_transfer_sources_d151.json)
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
The [D150 report](certificates/structural-identification-audit-d150.md),
[fixed review](data/computed/structural_identification_review_d150.json),
[completion record](data/computed/structural_identification_completion_d150.json) and
[source applicability ledger](data/computed/structural_identification_sources_d150.json)
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
The [D149 report](certificates/P1600-primitive-frame-limits-d149.md),
[fixed review](data/computed/P1600_primitive_frame_review_d149.json),
[completion record](data/computed/P1600_primitive_frame_completion_d149.json) and
[source applicability ledger](data/computed/P1600_primitive_frame_sources_d149.json)
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
The [D148 report](certificates/P1600-forward-frame-bound-d148.md),
[fixed review](data/computed/P1600_forward_frame_review_d148.json),
[completion record](data/computed/P1600_forward_frame_completion_d148.json) and
[source applicability ledger](data/computed/P1600_forward_frame_sources_d148.json)
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
The [D147 report](certificates/P1600-multiplication-determinant-d147.md),
[fixed review](data/computed/P1600_multiplication_review_d147.json),
[completion record](data/computed/P1600_multiplication_completion_d147.json) and
[source applicability ledger](data/computed/P1600_multiplication_sources_d147.json)
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
The [D146 report](../dembele/certificates/P1600-elliptic-intersections-d146.md),
[fixed review](../dembele/data/computed/P1600_intersection_review_d146.json),
[completion record](../dembele/data/computed/P1600_intersection_completion_d146.json) and
[source applicability ledger](../dembele/data/computed/P1600_intersection_sources_d146.json)
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
The [D145 report](../dembele/certificates/P1600-spectral-feasibility-d145.md),
[fixed review](../dembele/data/computed/P1600_spectral_review_d145.json),
[completion record](../dembele/data/computed/P1600_spectral_completion_d145.json) and
[source applicability ledger](../dembele/data/computed/P1600_spectral_sources_d145.json)
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
The [D144 report](../dembele/certificates/P1600-joint-adjunction-RR-d144.md),
[fixed review](../dembele/data/computed/P1600_joint_RR_review_d144.json),
[completion record](../dembele/data/computed/P1600_joint_RR_completion_d144.json) and
[source applicability ledger](../dembele/data/computed/P1600_joint_RR_sources_d144.json)
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
The [D143 report](certificates/P1600-finite-model-cotangents-d143.md),
[fixed review](data/computed/P1600_finite_model_review_d143.json),
[completion record](data/computed/P1600_finite_model_completion_d143.json) and
[source applicability ledger](data/computed/P1600_finite_model_sources_d143.json)
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
The [D142 report](certificates/P1600-two-height-routes-d142.md),
[fixed review](data/computed/P1600_two_height_review_d142.json),
[completion record](data/computed/P1600_two_height_completion_d142.json) and
[source applicability ledger](data/computed/P1600_two_height_sources_d142.json)
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
The [D141 report](certificates/P1600-proof-gap-d141.md),
[fixed review](data/computed/P1600_proof_gap_review_d141.json),
[completion record](data/computed/P1600_proof_gap_completion_d141.json) and
[source applicability ledger](data/computed/P1600_proof_gap_sources_d141.json)
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
The [D140 report](certificates/dyadic-P1600-recognition-d140.md),
[fixed review](data/computed/dyadic_P1600_recognition_review_d140.json) and
[completion record](data/computed/dyadic_P1600_recognition_completion_d140.json)
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
The [D139 report](certificates/dyadic-indexed-recost-d139.md), [fixed review](data/computed/dyadic_indexed_recost_review_r2_d139.json) and [revised cost model](data/computed/dyadic_indexed_bank_recost_r2_d139.json) record the bookkeeping work following D138. The [completion record](data/computed/dyadic_indexed_recost_completion_d139.json) confirms six passing bounded jobs; the one diagnosed review-parser failure is preserved.
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
The [D138 report](certificates/dyadic-precision1600-bank-d138.md), [fixed review](data/computed/dyadic_precision1600_review_d138.json) and [completion record](data/computed/dyadic_precision1600_completion_d138.json) supersede the running/ETA notes below.
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
[Progress observed 2026-10-07 10:26 EDT](data/computed/dyadic_checkpoint_bank_r2_d137_observation03.json): twelve of the fourteen new columns
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
full bank remains unapproved. The [D137 revision-2 admission](certificates/dyadic-checkpoint-revision-d137.md), [fixed review](data/computed/dyadic_checkpoint_admission_r2_d137.json) and [admission completion](data/computed/dyadic_checkpoint_admission_completion_r2_d137.json)
record passing bounded admission and replay over 94,126 hashes.
The first launch exposed the frozen store's required `_d132` suffix before
any store or arithmetic was created. Its failed receipt/log/snapshot and
original configurations are preserved; revision 2 fixes only the interfaces.
The actual revised column-2 storage-creation preflight passed before relaunch.

[launch record](data/computed/dyadic_checkpoint_bank_r2_d137_launch01.json); [live coordinator log](data/computed/dyadic_checkpoint_bank_r2_d137_run01.log). Started 2026-10-06T20:33:48.236162+00:00 under a detached coordinator,
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

See the [target-chart report](certificates/dyadic-target-charts-d136.md), [cost report](certificates/dyadic-bank-recost-d135.md) and [completion record](data/computed/dyadic_target_chart_completion_d136.json).

<!-- D135 reviewed bank-cost checkpoint -->

**Previous reviewed checkpoint: D135.**

D135 cost analysis and independent review/replay pass, preserving all 93,912 D134 hashes. The staged target bank is estimated at 22.0--30.5 active days with at most three workers; these are empirical scenarios, not an ETA or admission. Incremental reviews would put additional retention at about 53--65 GiB; plan for at least 80 GiB free, versus roughly 51 GiB observed. A full-bank P1600 checkpoint is estimated at 15--18 hours and 3--4 GiB. Direct P800/P1600-to-target stores violate the unchanged 2 GiB cap. Next resolve target CM peak memory, seed/CM metadata interfaces and bounded incremental review; a scope/storage preference has been requested from the user. No new harmonic stage or bank has launched. Certified precisions remain P800 for the full bank, P6400 for column 0 and P1600 for column 1. Sources 560/561 and reviewed artifacts are frozen. D136 source 562 is running the finite 17-chart synthetic target-memory controls; source 563 is its drafted review/CM adapter. Source 564 is next unused. Inspect the D136 receipts and control lock before any other mathematical job. Preserve every earlier freeze and the three-worker/180-second limits.

See the [cost report](certificates/dyadic-bank-recost-d135.md) and [completion record](data/computed/dyadic_bank_recost_completion_d135.json).

<!-- D134 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D134.**

D134 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. The D134 replay and both reviews pass; its fixed review binds 93,912 hashes and preserves the D133 catalogue. The conditional route uses the odd canonical Jacobian order to fix the F-rational branch half, then D77 cubic inertia to fix its scalar. The marked-base and canonical Hecke hypotheses remain essential. The continuation coordinator has no further mathematical jobs after this checkpoint. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](certificates/arithmetic-twist-classification-d134.md) and [completion record](data/computed/arithmetic_cover_criterion_completion_d134.json).

<!-- D133 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D133.**

D133 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. All 24,577 D133 input jobs and both reviews pass. The fixed review binds 93,638 hashes. The completion coordinator next runs the D134 finite replay and review; inspect its live session and receipts before starting any other mathematical job. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](certificates/dyadic-precision6400-d133.md) and [completion record](data/computed/dyadic_precision6400_completion_d133.json).

**Execution resumed (2026-10-05):** D133 resumed from correction 10 after
transfer and dependency verification. Its continuation waits for sealed
production before D133 audits/review and D134. See [HANDOFF.md](../HANDOFF.md)
and the [resumption record](checkpoints/d133-resume-2026-10-05.json) for
durable logs and restart checks. Certified precision stays P800/P3200/P1600
(bank/column 0/column 1). The transfer pause below is historical.

**Transfer checkpoint (2026-09-30):** D133 is paused after correction 9 and
its archive, before `low_begin_010`; both coordinators are stopped. All 2,682
production/archive receipts pass. Use [CHECKPOINT.md](../CHECKPOINT.md) for
Git LFS retrieval, integrity verification and native execution dependencies.
P6400 and D134 remain unfinished; bank/column-0/column-1 certified precision
stays P800/P3200/P1600. Earlier active-session statements are historical.

This directory contains the new computation aimed at constructing an explicit polynomial
whose splitting field is Dembélé's nonsolvable extension of \(\mathbf Q\), ramified only at
\(2\).

The initial, completed milestone was to reproduce the level-one,
parallel-weight-two mod-\(2\) Hilbert Hecke module over

\[
F=\mathbf Q(\zeta_{32})^+
 =\mathbf Q(\beta),\qquad
\beta^8-8\beta^6+20\beta^4-16\beta^2+2=0,
\]

recover its two nonzero eight-dimensional constituents, and determine exactly how they
arise from the integral characteristic-zero Hecke algebra. Current work compares
the explicit candidates with the prescribed arithmetic genus-64 cover.

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
See the [snapshot](data/computed/dyadic_close_session_snapshot_d133_20260929.json)
and [resume procedure](../HANDOFF.md). This is not a new precision certificate.

Until that review, certified precision stays P800 for the full bank,
P3200 for column 0 and P1600 for column 1. Exact base identification,
marked arithmetic covers/Y64 and the original-kernel polynomial remain
open. No automatic full-bank launch. Keep at most three mathematical
workers, unchanged 180-second process-group caps and all prior freezes.
See the [D132 report](certificates/dyadic-staged-integration-d132.md) and
[active handoff](../HANDOFF.md). Earlier next-task statements are historical.

D131 (previous completed checkpoint, 2026-09-28).

The weighted-only certificate replays all 4,454,400 state coordinates,
174 masses and 870,400 CM coordinates against actual D129 data. D129
already evaluated CM from weighted inputs; D131 supplies streaming/row
authentication and GMP replay. A new row journal recovers nineteen
distinct process-interruption boundaries and rejects four corruption or
stale-journal cases. A freshly recomputed known P=1600 correction passes
through it, including all 44,544 low equations and 1,067,664 new residual
scalars. Independent ordinary-arithmetic checks are sampled.

All 54 input jobs and both reviews pass; review 546 binds 16567 hashes
and preserves all 16142 D130 hashes. Freeze 541--546, `run_d131_batch.py`,
bound artifacts and sealed stores. Full bank P=800, column 0 P=3200 and
column 1 P=1600 remain unchanged. No positive exact zero, candidate
identification or original-kernel polynomial follows from these controls.

Next use source 547 onward for the complete resumable staged driver:
separate low-RHS chunks and multi-digit solves, one working store, full
file lifetimes and a separate concurrent-RAM budget. The target sparse
reservation fits the 2 GiB per-store cap, but complete target execution
is not yet certified. Select the next actual refinement after these gates.
Keep at most three mathematical workers and unchanged 180-second caps.
D130 timings remain a pre-redesign baseline. Marked arithmetic cover and
Y64 section construction remain separate research tasks.
See the [D131 report](certificates/dyadic-weighted-journal-d131.md) and
[handoff](../HANDOFF.md); all earlier next-task instructions are historical.

D130 (previous completed checkpoint, 2026-09-28).

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

See the [feasibility report](certificates/dyadic-target-feasibility-d130.md) and
[arithmetic construction specification](certificates/arithmetic-construction-d130.md).
Earlier next steps below are historical.

D129 (previous completed checkpoint, 2026-09-28).

One actual harmonic column now reaches P=3200. All 4,454,400 original
residual scalars, old overlaps, exact masses, 17 CM charts and 22 independent
audit jobs pass. All 1934 input jobs and both fixed reviews pass. Review 532
binds 15600 sources and preserves all 9648 D128 hashes. Peak scratch is
1,229,041,837 bytes under the enforced 2 GiB cap; the highest measured single-process
input peak is 491,929,600 bytes. Four sealed state payloads total 558,829,536 bytes.
Freeze 528--532, both operational schedulers and all bound artifacts.
Column 1 remains P=1600 and the complete bank P=800. Exact vanishing,
candidate identification and the target field polynomial remain open.

D129 plan (superseded by D130): the [stocktake after D129](certificates/stocktake-2026-09-28.md)
retains the dyadic route and makes exact genus-16 identification the next
major mathematical milestone. Source 533 onward should cost the complete
P=10552 certificate, including all columns, CM/frame/quadric arithmetic,
verification and retention, and compare staged/direct schedules. Specify
the downstream marked-cover and arithmetic Y64 construction alongside
that budget before a long full-bank commitment. No automatic next precision
doubling; the target cost and eventual field polynomial remain open.
Keep the three-worker, 180-second process-group limits and all freezes.
See the [report](certificates/dyadic-precision3200-d129.md) and current handoff. Earlier next steps are historical.

D128 (previous completed checkpoint, 2026-09-28).

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
See the [report](certificates/dyadic-selective-scaling-d128.md) and current handoff. Earlier next steps are historical.

D127 (previous completed checkpoint, 2026-09-28).

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
[report](certificates/dyadic-rolling-pilot-d127.md) and current handoff. Earlier next steps are historical.

D126 (previous completed checkpoint, 2026-09-28).

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
[report](certificates/dyadic-resource-controls-d126.md) and current handoff. Source 519 is next unused.

D125 (previous completed checkpoint, 2026-09-28). The complete sixteen-column bank is now certified at P=800, including
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

D124 (previous completed checkpoint, 2026-09-28). One actual column now reaches P=1600 with all original residuals, CM
charts, old overlaps and four independent audits passing. All 242 input
jobs pass under the 180-second cap. Review 504 binds 3535 sources and
preserves all 2532 D123 hashes. The full sixteen-column bank remains
P=400, so section and Gaussian bounds are unchanged. Direct weighted CM
is validated against every P=800/P=1600 CM moment; a compiled small-product
path passes independent controls. Freeze 496--504, their coordinator and
bound report/ledger. Next: combine these improvements in new source 505,
complete columns 1..15 at P=800, reuse column 0, then recompute and audit
the full frame and quadrics. No field polynomial is yet constructed.

D123 (previous completed checkpoint, 2026-09-27) refines one actual harmonic
column and all seventeen CM charts to P=800. A weighted input using
51.5625% of the uniform storage reconstructs the verified column exactly.
The shrinking Schur loop then reproduces it in twelve corrections,
checking every intermediate state and residual against the uniform run.
Both independent audits pass. Read
[the result and proof](certificates/dyadic-staged-pilot-d123.md) and
[the current handoff](../HANDOFF.md).

All 148 input jobs pass; review 495 binds 2532 sources, preserving all
1884 D122 hashes. Freeze 488--495, both coordinators and bound outputs.
The full sixteen-column bank remains P=400; its section and Gaussian
results are unchanged. Exact curve and field identification remain open.
Next combine the weighted solver with resumable chunks and cost one
P=1600 column, including factor, seed, full original residual, CM and
peak memory. No such larger run has started. All workers have completed;
all resource pauses and downstream requirements stand.
Earlier next tasks below are historical.

D122 (previous completed checkpoint, 2026-09-27) now includes the residue-frame
comparison and independent review of all sixteen P=400 columns. All 1088
coarse values and 6188 quadratic coefficients are checked; no certified
mismatch is found. Read [the final report](certificates/dyadic-precision400-d122.md)
and [the current handoff](../HANDOFF.md).

Actual section bounds are 4194/4145/4128, with anchor 3976/3648/3384 and
sufficient non-anchor bounds 25305/25419/25526. The Gaussian at W is now
certified nonzero, valuation 1024 with error 1225; it has not been inverted.
No exact positive zero, candidate identification or field polynomial is
proved. Source 486 supplies seven independent arithmetic phases; review
487 binds 1884 sources, preserving all 1079 D121 and 1844 interim hashes.
All 167 input jobs pass, and no worker remains running.

Freeze successful 476--487 and outputs. Next generalize the lift with
state-chunk checkpoints and measure a single P=800 column from P=400,
including final residual and CM costs. This next implementation has not
started. Preserve all resource pauses and downstream requirements.
Earlier next tasks below are historical.


D122 (previous interim checkpoint, 2026-09-27) completes all sixteen actual
harmonic columns at P=400, including seventeen CM charts and four coarse
coefficients with beta-errors [832,848,832,864]. Source 482 consolidates
the bank; the algebraic CM frame eta is separately refined to beta-error
21168. All 155 computation jobs pass, and all batch workers have finished.
Read [the progress checkpoint](certificates/dyadic-precision400-progress-d122.md)
and [the exact resume commands](../HANDOFF.md).

Sources 483--484 are drafted but unrun: next compute the residue frame,
then all 91 quadrics and updated anchor-dependent section thresholds.
An independent D122 mathematical review is pending. Source 485 is only
a provenance/completion snapshot: creation and hash replay pass, binding
1844 sources and preserving all 1079 D121 hashes and completed receipts.
Freeze successful 476--482 and bound artifacts;
the two unrun drafts remain editable. Use the persistent capped wrapper.
No P=400 quadric verdict, positive exact zero, candidate identification
or field polynomial is claimed. Keep D118's accepted section bounds,
all caps/pauses and downstream requirements. Earlier next tasks are historical.


D121 (previous checkpoint, 2026-09-27) implements low-moment Schur
elimination and raises one actual harmonic column to P=400. All seventeen
CM charts and four coarse coefficients are checked, with beta-errors
[832,848,832,864]. All 399 transport parameters are certified at P=10552.
The full sixteen-column bank remains at P=200. Read
[the solver proof and actual lift](certificates/dyadic-schur-lift-d121.md).

The original state residual, old overlaps and independent CM evaluation
pass. Review 474 binds 1079 sources, preserving all 961 D120 hashes.
Next accelerate the polynomial backend, finish the sixteen-column P=400
bank and recompute quadrics. A complete target-size run is still too
expensive with current per-action timings. Exact curve identification,
the marked cover and field polynomial remain open. Freeze 464--475 and
bound outputs; retain all caps, pauses and preceding exact-zero hypotheses.


D120 (previous checkpoint, 2026-09-26) completes the frame comparison and
retains D118's direct integral-section route. Read
[the reassessment and proofs](certificates/construction-reassessment-d120.md).
The inverse-frame bound is worse after consistent local normalization;
known minors give h_Fal<30.970856, excluding a Faltings-only rescue.
Explicit error propagation gives conditional sufficient P=10552, provided
future quadratic enclosures contain zero. No actual precision is increased.

Polynomial/GMP transport code checks 332800 coefficients from the frozen
P=200 bank on one harmonic column. One synthetic target-size action takes
50.408 seconds, but a complete solve still needs fewer expensive iterations.
Next test r=1 low-moment elimination, its 174-dimensional low-block solve,
full original residual and storage cost on P=200. A large run is not ready.
Existing Hecke input now proves norm-97 cofactor separation in canonical
Y64; only the first norm-97 target has order 51, matching the second T31
system. The other has order 257. The combined genus-64 degree-51 backend
and the curve, cover and field construction remain open.

Review 462 binds 961 sources, preserving all 922 D119 hashes. Seven input
jobs pass; one caught norm-97 expectation error is archived. Freeze
458--463 and bound files; recheck 462 --check through runner 272. Retain
all resource pauses and preceding exact-zero hypotheses. Decisions and
references are current; earlier next tasks below are historical.


D119 (previous checkpoint, 2026-09-26) determines the actual Cartier
CM divisor and its dyadic residue map. Read
[the proof and next task](certificates/cm-cartier-frame-d119.md).
Eight ordinary pairs have intersection length 33; the anchor is disjoint.
The correct horizontal order has normalization index 264. Its H1 torsion
length is 14 and its primitive principal-part norm valuation is 2.
The residue index is **16** and its cokernel is **(R/(beta^2))^8**.
These are model-dependent data; the old evaluation defect 245 is different.

This supplies a local clearing map and a bound for the pencil line,
but not yet an improved quadratic-section height bound. Current sufficient
valuations remain **25330/25444/25551**, versus actual **3794/3745/3728**.
Next derive the full intrinsic-frame budget with consistent metrics and
compare degree minus measured zeros with D118. Non-dyadic residue indices,
global normalization, exact candidate identification and the target
polynomial remain open.

Review 457 binds 922 sources and preserves all 911 D118 hashes. It
independently reconstructs the matrix, all maximal minors and the residue
map. The corrected calculation and probe/final audit pass; one initial
graph-count failure is archived. Freeze 456--457 and bound artifacts.
Retain the P=200 bank, D99/D108, all resource pauses and downstream
marking, cover, section and torsion requirements. Decisions and references
are current; earlier next steps below are historical.


D118 (previous checkpoint, 2026-09-26) computes the combined dyadic
Hodge/ramification correction exactly and incorporates the tropical
moment of the existing reduction graph into the Faltings lower bound.
The sufficient section valuations are now **25330/25444/25551**, versus
actual **3794/3745/3728**. Read
[the proof and revised plan](certificates/cm-finite-height-d118.md).
Exact candidate identification and the target field polynomial remain open.

The composite W_C -> L(Q)^2 has dyadic contents [280,17x16], giving
H_CM <=2*h_L-(35/34)*log(2)<8/3. The graph has length 76,
tau=67889/27075 and tropical moment 223268/27075. In the matching
metric, its contribution yields h_Fal(C)>-23.146371. The small-level
model is a proof device; no auxiliary level or new graph is computed.

Review 455 binds 911 sources and preserves all 891 D117 hashes. All
four input jobs and the independent probe/final review pass. Freeze
sources 451--455 and bound artifacts. Higher integral jets still require
preceding exact zeros. The current actual data remain the P=200 bank.

The remaining gap is 21536--21823. Next test a lower-degree integral
CM frame via D102, first verifying the actual Cartier divisor,
principal-part norm and cohomology torsion. The evaluation defect 245
does not compute that index. Keep D99/D108, every resource pause,
and the downstream marking, cover, section and torsion requirements.
Decisions and references are current; earlier next steps are historical.


D117 (previous checkpoint, 2026-09-26) certifies uniform CM disks of radius
squared **3/5** and lowers the sufficient integral-section thresholds to
**35947/36096/36237**. Actual lower bounds remain **3794/3745/3728**.
The candidate is not yet identified and the field polynomial remains
unconstructed. Read [the proof and revised plan](certificates/cm-disk-and-exactness-d117.md).

The stronger CM projection-lattice argument checks 376935 vectors and
applies to every CM point and conjugate. Review 450 independently checks
the enumeration and bounds, binding 891 sources and preserving all 868
D116 hashes. Sources 446--450 and bound artifacts are frozen. One failed
serialization probe is archived; corrected jobs and the independent review
pass under the existing cap. No moment precision was increased.

With all other inputs fixed, even rho=1 leaves sufficient thresholds
32928/33064/33193. Further disk refinement alone cannot certify the actual
data. Next compute the dyadic finite corrections omitted in D104's height
comparison, after proving the upstairs integral model generators. Assess
those gains before choosing further precision. The higher jet tests still
require preceding exact zeros. Keep all census, level, Hecke and cubic
pauses, and all downstream marking, cover and torsion requirements.
Decisions and references are current; earlier next steps are historical.


D116 (previous checkpoint, 2026-09-26) supplies an integral quadratic-section
criterion for exact identification and the actual jets through its required
order. Read [the proof and plan](certificates/cm-compound-height-d116.md).
For the three successive positive jets, sufficient degree-16-place
beta-valuations are **119806/120284/120758**, using the certified anchor
contributions. Actual lower bounds are **3794/3745/3728**. These are
section valuations, not ratio errors; the higher integral jets require
all preceding jets to vanish exactly. No positive jet is proved zero,
the candidate remains unidentified, and the target field polynomial
remains unconstructed.

The third coarse coefficient comes from the existing P=200 bank, with
four-order beta-errors 432/448/432/448. Every one of the 1088 harmonic
entries is nonzero. All 91 quadrics have zero-containing residuals at
all 17 CM points through order three. Review 445 independently checks
the third coefficients and all 4641 positive residual coefficients.

The harmonic basis has all Smith factors one. Stabilizer-weighted
residues give a unimodular graph-cycle basis; the nodal model proof
identifies it with the stable differential lattice. Integral cofactor
contents also improve the alternative ratio bounds to 132444/524481
beta-errors, versus achieved 101/70. The actual J3 rank is at least 33,
not 45. The direct four-coefficient test avoids that rank prerequisite.

Review 445 binds 868 sources and preserves all 814 D115 hashes. Sources
432--445 and bound artifacts are frozen. The audit and recheck pass.
Continue with a sharper norm/content bound for
the actual reduced quadric tensors, or an exact identity with uniqueness.
A larger precision run needs a limb-safe costed design first. Markings,
the upstairs cover, global cubic/section data and target torsion remain
downstream. Decisions, references and all resource pauses are current;
earlier next steps are historical.


D115 (previous checkpoint, 2026-09-25) carries the dyadic route through
an actual rational-frame comparison. The W leading value is resolved,
the harmonic-to-residue basis change is computed, and the first two
ratio coefficients agree with the candidate within beta-errors **101/70**
at the sixteen non-anchor CM points. Read
[the reassessment and result](certificates/dyadic-comparison-and-strategy-d115.md).

The final moment precision is 200, with 1,667,616 state and 108,800
CM A-chart entries. Full Eisenstein arithmetic, batched operators and
correction refinement retain the 180-second job cap. The same splitting
root now has error 352, giving transport errors at least 331/337.
The first W leading coefficient has beta-valuation 296; all 816
harmonic coarse entries are certified nonzero. The chosen Gaussian
is numerically nonzero at the other sixteen points, hence qualitatively
nonzero throughout the transitive CM divisor in the rational frame.

Independent moment/kernel and series-reversion checks pass. Review
431 binds 814 sources and preserves all 713 D114 hashes. The actual
frame and ratio data are in `dyadic_comparison200_d115.json`.

The revised priority is exact arithmetic identification. The current
height bound needs beta-errors 274241/820774 at the degree-16 place,
equivalently integer pi-errors 137121/410387, to prove equality at
orders 1/2. The present agreement does not meet those bounds. A
sharper bound on the actual unknowns or an exact identity with a
uniqueness argument remains necessary. Marked-cover identification,
global cubic data, target torsion and the field polynomial remain
open. Decisions and references are current; all resource pauses
remain. Earlier next steps are historical.


D114 (previous checkpoint) computes actual coarse
differential 2-jets in the sixteen-element harmonic basis at all
seventeen matched CM points. The local parameter is
u=((z-beta)/(z+beta))^2, and the first three coefficient errors
are 32,40,32 pi-digits. All 256 non-anchor entries at each order
are certified nonzero. Read
[the D114 proof](certificates/dyadic-coarse-d114.md).

The precision-16 bank contains 130,848 state moments through degree
46 and 26,112 CM moments through degree 31. Independent moment
arithmetic and kernel expansion verify the coarse evaluation.
The CM involution gives g_j=2*integral_A K_j dmu and sharper errors;
use the refined values in the final review artifact. The original
three-chart enclosures remain frozen. Review 416 binds 713 sources,
preserving all 696 D113 hashes. One failed implementation probe is
archived; the corrected probe and final review pass.

At W the coefficient valuations are at least 32.5,40.5,32.5.
All integral polynomial moments on A are divisible by pi^16:
monic division by (X^2-X)^16 extends the computed degree-31 result
to every degree. Thus more degrees at this precision cannot resolve
the anchor, and no normalization is available. Next use precision
24, low cutoff 23, 24 iterations, state cutoff 70 and CM cutoff
47, initially focusing on W. Implement the full Eisenstein quotient;
the old shortcut loses a term of valuation 20. Check the existing
bank on overlap and retain the 180-second cap and transport data.

Rational-frame ratio jets, the actual frame change, a Gaussian
pivot, dyadic equality thresholds, candidate identification and
the target polynomial remain open. Decisions and references are
current; all resource pauses remain. Earlier next steps are historical.


D113 (previous checkpoint) computes actual positive-degree
moments using a finite contracting system. The existing 174 edge
charts give 348 maps covering their two child balls, each contracting
by pi. Direct coefficient estimates over the ramified K prove a
one-digit gain per iteration and explicit moment-truncation bounds.
Read [the D113 proof](certificates/dyadic-moments-d113.md).

The pilot produces 33,408 state moments through degree 11 modulo
pi^12. Transfer to the 51 matched CM charts certifies degrees 1,2,3
with errors 11,10,9; 2043 entries are certified nonzero. At W all
144 positive-degree entries are zero modulo their error bounds.
This does not establish exact vanishing or a usable normalization.
Review 413 independently verifies all moment equations with separate
polynomial arithmetic and checks direct integration on 32 leaf
balls. It binds 696 sources and preserves all 682 D112 hashes.
All bounded jobs pass first attempts; sources 411--413 are frozen.

Next feed actual moments into D108's coarse Poisson formulas with
a modest target of 16 pi-digits. CM cutoff 31, state cutoff 46 and
precision/iterations 16 suffice for the proved tails. Higher state
moments can be recovered after solving the low-degree fixed system.
Establish a nonzero coarse value at W before normalizing. The current
quotient shortcut supports only precision at most 16. An actual
frame change, Gaussian pivot and dyadic equality thresholds remain
needed; no actual differential value/jet, candidate identification
or target polynomial has been obtained. Decisions and references
are current; all resource pauses and the 180-second job cap remain.
Earlier next steps are historical.


D112 (previous checkpoint) gives exact dyadic charts and
arithmetic labels for all seventeen CM points. W is the unique
K-rational anchor, certified using the norm-one unit k that exchanges
its fixed points. All relative ideal classes have exact principal
witnesses. CM reciprocity in the normalized local character, followed
by an independently certified Galois resolvent, matches the points
to the saved complex labels and rational residue frame.
Read [the D112 proof](certificates/dyadic-cm-matching-d112.md).

All seventeen dyadic roots have errors at least 688 beta-digits;
the 17-by-16 algebraic residue-frame matrix has error at least 384
beta-digits = 192 pi-digits. These entries do not yet give actual
harmonic differential values. The 51 boundary-chart zeroth-moment
vectors are computed: A0=0 and B0+C0=0. Review 410 binds 682 sources
and preserves all 661 D111 hashes. One failed valuation-expectation
probe is archived; the corrected probe and final review pass.
Sources 407--410 and bound artifacts are frozen.

Next establish finite positive-moment transport/recursion with
proved ramified-field bounds, then run a bounded actual pilot.
Positive-degree moments, the actual harmonic-to-residue change of
basis, a Gaussian pivot and dyadic equality thresholds remain needed.
No actual jet, candidate identification or target polynomial has
been obtained. Decisions and references are current; all resource
pauses and the 180-second job cap remain. Earlier next steps are historical.


D111 (previous checkpoint) constructs sixteen actual
G-invariant scalar harmonic cocycles and a terminating arithmetic
edge reducer. All 174 outgoing neighbor entries and 164 projective
stabilizer elements for the same 58 classes are certified. The 376
integer harmonic relations have rank 158, checked independently.
All nine inverted edge orbits receive zero. The integral basis gives
boundary measures with uniform denominator bound d=0.
Read [the D111 proof](certificates/dyadic-harmonic-d111.md).

Reducer 405 returns exact quaternion transport words and all sixteen
values, refining the fixed Hensel root when needed. Tests through
depth 32 check reversal, harmonicity and arithmetic invariance.
Review 406 binds 661 sources, preserving all 643 D110 hashes;
all five bounded jobs passed on first attempts. Sources 403--406
and bound artifacts are frozen.

Next certify the dyadic fixed points and CM coordinate change for W,
match the embedding and orientation to the saved CM labels/rational
frame, then perform a bounded moment pilot with a proved error bound.
Actual moments, CM/frame matching, jets and candidate identification
remain open. The target polynomial is unconstructed. Decisions and
references are current; all resource pauses remain. Earlier next
steps are historical.


D110 (previous checkpoint) makes the dyadic group and
Atkin--Lehner coset explicit. The same-session Brandt matrix and
stabilizers match D99 exactly, and the order basis matches D109.
Seven certified ideal correspondences produce a projective involution
W with W^2=-(2+b), moving the base vertex seven edges. A norm-one
conjugate of the known unit moves it fourteen edges. Multiplying the
original unit by that conjugate gives a hyperbolic translation of length fourteen.
Read [the D110 proof](certificates/dyadic-group-transport-d110.md).
Review 402 binds 643 sources, preserving all 629 D109 hashes.

Next complete adjacency transports and vertex stabilizers for the
existing 58 classes, build finite edge reduction and construct the
expected 16-dimensional invariant harmonic space with a measure bound.
No full fundamental domain or complete generating set is claimed yet.
Actual moments, dyadic CM/frame matching, jets and candidate identification
remain open. The target polynomial is unconstructed. Decisions and
references are current; resource pauses remain. Earlier next steps
are historical.


D109 (previous checkpoint) completes the bounded local
arithmetic plan. The actual definite order in B=(-1,-1)_F is exported;
an exact Hensel certificate proves its integral dyadic matrix splitting;
and the norm-one unit (1-i-j-k)/2 cycles the three edges at the base
vertex. Exact lattice checks prove order closure, trace discriminant
2^124, residue rank four and an integral transport of determinant one.
Read [the D109 proof](certificates/definite-dyadic-d109.md).
Review 399 binds 629 sources and preserves all 606 D108 hashes.

The transport fixes the base vertex. Next instantiate the known
arithmetic group/normalizer quotient in these coordinates, reconcile
it with the saved 58-class data, and certify a transport moving the
base vertex. No full new tree census was run or is justified yet.
Harmonic cocycles, moments and dyadic CM/frame matching remain missing.
No actual tangent/jet, candidate identification or target polynomial
has been obtained. Decisions and references are current; retain
enumeration/Hecke/cubic-precision pauses. Earlier next steps are historical.


D108 (previous checkpoint) rules out the proposed
completed per-ideal absolute spectral comparison: its unavoidable
floor exceeds 60.32 times the saved partial. This is not a lower
bound on the actual error. A direct dyadic alternative now has
explicit conditional moment-to-coarse-jet formulas and error bounds,
verified on synthetic measures in the actual CM field. Read
[the D108 report](certificates/shimura-evaluator-d108.md).
Review 396 passes and binds 606 sources, preserving all 588 D107 hashes.

Next export the definite order, certify its integral dyadic matrix
embedding, and verify one edge transport. The saved Brandt graph
does not contain the boundary matrices needed for evaluation. Actual
harmonic cocycles, moments, dyadic frame matching and a Gaussian chart
remain required. No actual tangent/jet, candidate identification or
target polynomial has been obtained. Retain resource pauses; the
complex method would need additional cancellation or a different
diagonal estimate. Earlier next steps are historical.


D107 (previous checkpoint) certifies the saved CM
point/root correspondence. Point 8 and root 2 are the unique real
points; an exact quaternion witness and matrix sign fix the real
structure and CM orientation. Certified root disks, an integral
norm and a rank-271 certificate establish the saved Frobenius cycle.
Independent local lifts and reciprocity recover the old lookup.
Read [the D107 proof](certificates/cm-root-matching-d107.md).
Review 393 passes and binds 588 sources, preserving all 562 D106 hashes.

The rational CM frame now has certified labels in the saved complex
point order. Its actual differential evaluations, change matrices
and a specific valid tangent chart remain uncertified. Next establish
an executable independent tangent/jet evaluator with a complete
error bound. No candidate identification or target field polynomial
has been obtained. Retain D98's spectral pilot gate and the resource
pauses. Earlier next steps are historical.


D106 (previous checkpoint) proves Aut(C_Qbar,D)=1 using stable specialization, the odd CM
orbit and the canonical projective frame. The given F-model therefore
has compatible Q-descent, and the residue construction gives a
canonical rational CM frame in the degree-17 field. Read
[the D106 proof](certificates/cm-rational-frame-jets-d106.md).
Ratio Taylor heights for orders 1,2,3 are below 10504,31518,52533.
Exact candidate-only jets pass 364 coefficient identities; sufficient
inert-31 comparison precisions are 3257,9746,16236. The J3 identification
test needs only the first two positive orders.

Audit 389 binds 562 sources and preserves all 543 D105 hashes.
The saved numerical labels and specific actual G12 pivot remain
uncertified; no independent arithmetic tangent/jet evaluator or
candidate identification has been obtained. The precision thresholds
are sufficient bounds, not achieved errors. Next establish an actual
evaluation mechanism in the rational frame. Retain the spectral
pilot gate and resource pauses. The target field polynomial remains
unconstructed; earlier next steps are historical.


D105 (previous checkpoint) proves the actual CM projective frame: dyadic specialization
gives `H0(K_C-D)=0`, and Galois transitivity makes all cofactors
nonzero. Over the degree-272 CM Hilbert class field H, any fixed
point-to-root bijection gives an algebraic frame with projective
tangent height below 10504. Nonhyperellipticity guarantees at least
one of fifteen charts works. Read
[the D105 proof](certificates/cm-frame-arithmetic-d105.md). Audit 386
passes all nine graph witnesses and binds 543 unchanged/new sources.
The saved numerical labels, a specific pivot and F descent remain
uncertified. Next address an independent tangent/jet evaluator and
exact equality; over H, arbitrary labels require checks at all
seventeen points. No candidate identification or target field
polynomial has been obtained. Retain the spectral pilot gate and
resource pauses. Earlier next-step instructions are historical.

D104 (previous checkpoint) proves the stable CM-fibre/Hodge comparison, including the
dyadic prime, and gives `H_CM,disk<41/10`. D103 then yields
`h(v_j)<10504`, conditional on the arithmetic labels and frame/chart
nonvanishing. Two exact analytic methods verify the numerical bound;
audit 383 checks all D103 sources unchanged. Read
[the D104 proof](certificates/cm-intrinsic-height-d104.md). Conservative
conditional equality tolerances are now explicit, but no independent
tangent or candidate identification has been obtained. Next prove the
arithmetic labels and nonvanishing before assessing a certified
evaluator. The spectral pilot gate and resource pauses remain.
Earlier next-step instructions are historical.

D103 (previous checkpoint) constructs integral adjugate sections whose common determinant
cancels in tangent ratios. A uniform arithmetic CM disk and exact
field bounds yield `h(v_j) <= 513*H_CM,disk + 8400`, under the stated
arithmetic frame hypotheses. This removes the need to bound the
residue index separately for this height argument. H_CM,disk is still
unbounded: next compare the stable coarse-canonical CM fibre with
Zhao's Hodge bundle through the normalizer quotient, especially at 2.
Read [the D103 proof](certificates/cm-adjugate-height-d103.md) and run
audit 381. No independent tangent, numerical tolerance or new spectral
pilot follows yet. Earlier next-step instructions are historical.

D102 (previous checkpoint) continues the integral-frame comparison. The residue index is
the principal-part norm valuation plus a cohomology-torsion length;
exact controls show why good reduction does not bound it. The saved
degree-17 field order and its trace lattices are now independently
checked, including clearing factors 32 and 17. These do not bound the
actual Shimura tangent. A cofactor formula specifies the required
archimedean inverse bound. Read
[the D102 result](certificates/cm-residue-lattice-d102.md) and run
audit 379. Next address the actual geometric defects and compatible
norms, or construct the arithmetic section restrictions. No new
spectral pilot is justified yet. Earlier instructions are historical.

D101 executes the first exactness task. The CM tangent can be computed
from Gaussian sections of 3K; explicit conditional norm/height tests
now isolate the required arithmetic lattice and normalization bounds.
Those bounds remain unproved for the actual Shimura curve. A new exact
candidate tangent is independently verified and matches D88 modulo 31;
its 269-digit integral-lattice clearing integer is a candidate diagnostic,
not a bound on the unknown tangent. Read
[the D101 result](certificates/cm-tangent-exactness-d101.md) and run
audit 377. The next task is the arithmetic frame/lattice comparison or
an actual section restriction map, before more spectral computation.
The candidate identification, exact global cubic and target torsion
remain open. Earlier next-step instructions below are historical.

D100 reviews the construction methodology. The canonical genus-64
Jacobian is a proved carrier of the original residual kernels, but our
candidate has not been arithmetically identified with it. Exact global
cubic/section data and target-scale torsion are further separate gaps.
The next research objective is an executable exact-identification
certificate, including an arithmetic frame and exact equality mechanism;
a better analytic bound alone is insufficient. Read
[the D100 review](certificates/construction-methodology-d100.md).
No new arithmetic job was run. The earlier checkpoints below retain
their evidence but their next-step instructions are historical.

D99 completes the requested fresh hyperellipticity review. The intended
genus-16 C is geometrically nonhyperelliptic: its newly recomputed stable
graph remains connected after all 1,035 deletions of one or two edges,
which excludes an involution with tree quotient. Primary-source checks
justify the arithmetic reduction and specialization at 2. New exhaustive
involution checks, the saved-order audit and the exact candidate check
also pass. The candidate remains unidentified with C. Read
[the D99 review](certificates/hyperellipticity-review-d99.md) and run
`python3 dembele/pari/374_hyperellipticity_review_audit.py --check`.
The audit verifies 479 hashes and replays the graph. D98's CM error
bound and the construction bottleneck remain unchanged.

D98 gives a proved spectral bound for all omitted norm ideals,
retaining cancellation within each full Hecke correspondence. The
omitted-ideal error improves by >272.48 to <24,784,932,714; the full
error remains too large to certify the CM anchor. A Gamma inequality
controls the entire relevant unitary spectrum, and a finite Hecke
bound changes the norm mass to a squared-divisor series. No unproved
signed-count estimate is used. Read [the D98 proof and pilot](certificates/nelson-spectral-ideal-d98.md)
and run audit 369. Next test a completed spectral multiplier with
uniform spectral and infinite norm bounds before more enumeration.

D97 tested signed orbital cancellation on all saved unit/prime-31 data.
Exact phase sums and Abel summation improve the outer finite block
bounds by factors >6.45 and >8.16. Certified transfer constants now
translate a specified uniform signed-count estimate into an infinite
remainder bound; the required counting estimate remains unproved.
The actual omitted-ideal bound stays <6.754e12 and the CM anchor is
uncertified. Next establish explicit spectral/translated-orbit or
signed Hecke-block bounds and test the complete norm sum. Read
[the D97 report](certificates/nelson-signed-orbit-d97.md) and run audit
367. More enumeration is not justified by finite cancellation alone.

D96 completed the preceding bounded summation pilot: retaining scalar Mellin
cancellation and summing the positive ideal majorant improves the
omitted-ideal S11 bound to <6.754e12, a factor >3.967. It remains
about 884 million times the partial sum. The far-tail/splice error is
<1.4e-6; the positive orbital and Hecke estimates are the remaining
loss. A larger enumeration is not justified by this test. Read
[the D96 report](certificates/nelson-completed-majorant-d96.md) and
run audit 362. Next test a concrete signed arithmetic bound with an
explicit remainder. The CM tangent and field remain unconstructed.

The following paragraphs record earlier checkpoints. D95 identifies
the full theta/Mellin series with the intended
Jacquet–Langlands derivative pairing up to a positive scalar. The
central-average comparison and nonzero forward coefficient close the
global identification gap. The derivative-ratio rule now explicitly
includes complex conjugation and factorials. Useful numerical accuracy
and a certified CM anchor are still missing. Read
[the D95 proof](certificates/nelson-global-identification-d95.md) and
run audit 359. The next task is a bounded summation pilot that retains
more cancellation; the target field remains unconstructed.

D94 reviewed the global evaluator: a contour change improves the
omitted-ideal bound to <2.680e13, still far too loose for a CM value.
The local norm-one contractions of our actual Schwartz factors are
proved nonzero, with real product exp(-2*pi) in the stated measures.
The next proof step compares the classical kernel with the global
similitude lift; the global identification and CM anchor remain open.
Read [the D94 report](certificates/nelson-test-vector-and-contour-d94.md)
and run audit 357. Decisions and references are current. Further
enumeration needs a useful error estimate; the target field remains
unconstructed.

D93 completed the norm-31 family at the saved Hecke prime b=27:
586 classes through A=25600, 32 exact norm-one orbits, and a rigorous
weighted-family tail. An all-ideal majorant proves convergence of the
formal expression, but its error bound is far too loose for a CM tangent.
Next review the global summation and nonzero test-vector identification
before extending the coefficient bank or cutoff. Exact-endpoint replays
correct the analytic export chain without changing the reported results.
Use [the D93 report](certificates/nelson-prime31-and-global-tail-d93.md)
and its final audit; the target field remains unconstructed.

Earlier checkpoints record how this evaluator was built.
D92 completes the norm-one control: 541 classes through A=25600,
independent interval proof of enumeration coverage, and a bound on
the entire remaining norm-one family. Its `(1,1)` subsum is positive;
this does not establish a full lift or CM tangent. Next extend the
fixed-norm search to the norm-31 prime b=27, with its saved Hecke
polynomials, and prove the corresponding coset/tail argument. Other
norm ideals and the global test-vector comparison remain open. See
[the D92 report](certificates/nelson-norm-one-control-d92.md).
D91 proves the cusp identity and central-unit reductions and evaluates
certified partial sums for 29 primitive classes, with all auxiliary
ideals and beta powers included. The full eigenform and CM tangent
remain uncomputed. Missing Hecke coefficients, an economical complete
enumeration with a tail bound, and the global test-vector identification
remain. See [the D91 report](certificates/nelson-hilbert-unfolding-d91.md).
The first complete unit cutoff is too large for direct enumeration;
next test enumeration by norm ideal and hyperbolic displacement.
D90 implements local components of Nelson's Shimizu method over F:
Fourier normalization, derivative kernels, CM lattices and a calibrated
scalar Mellin prototype. The global Hilbert unfolding and independent
differential evaluation are the next step. See
[the implementation report](certificates/nelson-totally-real-kernel-d90.md).
D89 supplies exact local quotient and Hecke-branch calculations for
the proposed CM tangent route. An independent global section evaluator
is still missing; no arithmetic tangent has been obtained.
D88's independent reviews give an exact-jet criterion for the base and
a conditional uniqueness proof for the selected cubic. Independent
Shimura-side arithmetic jets and the marked base/double-cover
identification remain missing.
D87 matches the genus-40 candidate's numerical sign character on all
277 Fuchsian generators, in two differential banks and a second path family.
This supports the geometric double-cover choice; the marked arithmetic
identification and selected cubic class remain open.
Start with [the current handoff](../HANDOFF.md),
[the CM tangent local-input report](certificates/cm-tangent-local-arithmetic-d89.md),
[the CM-expansion review](certificates/d88-cm-expansion-identification-review.md),
[the cubic-shortcut review](certificates/d88-cubic-identification-shortcut-review.md),
[the double-cover character comparison](certificates/cm-frame-double-cover-character.md),
[the completed 128-digit Châtelet run](certificates/cm-frame-cubic-128-chatelet.md),
[the bounded 128-digit attempt and descent review](certificates/cm-frame-cubic-128-review.md),
[the cover-choice and recognition checkpoint](certificates/cm-frame-structural-checkpoint.md),
[the 64-digit lift and reconstruction report](certificates/cm-frame-cubic-64.md),
[the normalization and precision report](certificates/cm-frame-cubic-precision.md),
[the two genus-64 Frobenius comparisons](certificates/cm-frame-cubic-frobenius.md),
[the explicit genus-64 cubic modulo 31](certificates/cm-frame-cubic-cover.md),
[the verified branch-class division](certificates/cm-frame-cover-class-arithmetic.md),
[the normalized B3 fibre and cubic-input certificate](certificates/cm-frame-B3-fiber.md),
[the rational double-cover certificate](certificates/cm-frame-rational-double-cover.md),
[the joint recognition and B3 normalization report](certificates/cm-frame-joint-field-and-B3-normalization.md),
[the precision-doubling report](certificates/cm-frame-precision-doubling.md),
[the normalization certificate](certificates/cm-frame-normalization.md),
[the 31-adic lifting certificate](certificates/cm-frame-resolvent-lift.md),
[the finite-field double-cover certificate](certificates/cm-frame-resolvent.md),
[the marked branch-divisor report](certificates/cm-frame-marks.md),
[the smoothness proof and arithmetic comparison](certificates/cm-frame-verification.md),
[the lifting memory audit](certificates/lifttors-memory.md),
[the geometry audit](certificates/curve-identification-audit.md),
[the backend controls](certificates/lifttors-control.md),
[the arithmetic section interface](certificates/arithmetic-section-interface.md),
[the strategic stocktake](certificates/stocktake-2026-09-16.md),
[the evaluation-space height report](certificates/cm-flag-height.md),
[the labelled CM orbit report](certificates/cm-orbit-recognition.md),
[the marked descent report](certificates/marked-descent.md),
[the arithmetic-input audit](certificates/cm-arithmetic-input-audit.md),
and [the construction report](certificates/cm-pointed-maps.md).

## Layout

- `upstream.lock` — exact software and source revisions used by the computation.
- `data/published/` — machine-readable transcription of published checkpoints.
- `data/computed/` — exact data and explicitly labeled numerical diagnostics;
  large outputs should be reproducible and checksummed rather than committed blindly.
- `magma/` — exact Magma computations, ordered by milestone.
- `pari/` — Fuchsian geometry, Belyi adapters, numerical differentials and function
  reconstruction; see its [README](pari/README.md).
- `tests/` — lightweight validation of source data and generated artifacts.
- `jobs/` — resumable local and chatelet job manifests.
- `certificates/` — mathematical arguments and experiment reports, distinguishing
  exact results from conditional claims and numerical evidence.
- `polynomials/` — eventual defining polynomials and their certificates.

## First checkpoints

1. Certify the field \(F\), its \(C_8\)-action, and the ordered prime orbits above
   \(2,31,97\).
2. Using the pinned
   [`hilbertmodularforms`](https://github.com/edgarcosta/hilbertmodularforms) revision,
   reproduce the 58-dimensional raw Brandt module and 57-dimensional cuspidal module.
3. Extract a saturated integral Hecke-stable lattice before reducing modulo \(2\).
4. Match Dembélé's characteristic polynomials, eigenvalue tables, and Frobenius orders.
5. Localize the integral Hecke algebra at the two residue-degree-eight maximal ideals and
   issue a definitive characteristic-zero lift report.

The finite-field constructors in `hilbertmodularforms` deliberately reject parallel
weight \(2\). Therefore the mod-\(2\) calculation must be derived from, and checked
against, the integral raw Brandt module; reducing an arbitrary rational cusp basis is not
a valid substitute.

## Current result

**2026-09-23, D89:** exact local arithmetic specifies the order-two
quotient and the needed upstairs differential degrees 1/3/5. The
degree-31 Hecke correspondence has two horizontal and thirty descending
branches, whose unknown derivatives prevent a closed computation using
the known CM orbit alone. Script 319 `--check` passes without reading
candidate equations or differential banks. No independent arithmetic
tangent or global section evaluator has been constructed. Read
[the report](certificates/cm-tangent-local-arithmetic-d89.md). Prior bound
artifacts remain unchanged, and precision remains paused.

**2026-09-23, D88:** independent reviews confirm that the expansion paper
can certify the candidate using exact jets at the degree-17 CM point,
but does not supply those jets. A new candidate-side rank certificate
reduces the required expansion to three coefficients, through t^2;
independent replay verifies ranks 17/34/45 and rejects a corruption.
Projective ratios remove the common period normalization.
Once the marked arithmetic C and X are identified,
the Prym order makes the existing nine thirds exhaustive; global branch
irreducibility and the S3 norm remove orientation and constant-twist
ambiguities, and injectivity of reduction on 3-torsion identifies the
selected algebraic lift. These conditions remain unproved for the
candidate. The next research target is an independent arithmetic
projective tangent evaluation, with its underlying model and theorem
specified. Read the two reviews linked above. Precision remains paused;
the exact number-field cubic and target field are unconstructed.

**2026-09-23, D86:** the Châtelet retry completes both cubic models at
31^128, with independent geometry/class/function checks, all four
highest-digit error controls and reduction to 64 digits. All 21 remote
jobs finish; peak RSS is 2.25 GB and the longest takes 299.709 seconds.
Joint F recognition at 112/16 digits is negative in all eight embeddings,
with successful controls. Exact integer certificates exclude homogeneous
coordinate height <=348,750,355,384,078 in the specified bases; F itself
is not excluded. The 128-digit package and audit are
`cm_frame_cubic_adjoint_package_128.json` and
`cm_frame_cubic_adjoint_audit_128.json`; 303 checks 2009 hashes / 769 JSON
records. All jobs are finished. Next pursue the D85 marked arithmetic
comparison/global class action, with no automatic 256-digit increase.
Read [the completed run](certificates/cm-frame-cubic-128-chatelet.md).
The entries below are historical. D85's absence assertions no longer
apply to this workspace, but all its bound source hashes are preserved.

**2026-09-22, D85:** sections and local expansions pass at 31^128;
the actual-divisor stage hits 2 GB twice and a 180-second timeout in
the blocked version. The verified cubic remains at 31^64. No 128-digit
recognition test ran, so this supplies no new coefficient-field exclusion.
The requested review is complete: normalization adds no extra root
choice, but the selected third's global Galois action is unproved.
The geometric third torsor has 3^48 members; nine local solutions and
two Hecke traces do not establish its arithmetic identity. The cubic
has no automorphisms over the fixed base, so field of moduli is the
descent gate. Pause precision escalation and prepare the marked arithmetic
comparison. Runner 297 checks 1744 hashes / 612 JSON records in
`cm_frame_cubic_128_attempt_review.json`. Read
[the D85 report](certificates/cm-frame-cubic-128-review.md).

**2026-09-22, D84:** two independently verified compatible 3-torsion
classes give nine actual choices of third. All nine genus-64 covers are
constructed and independently verified; only the current choice has
the predicted counts 68/2818. The subgroup is not proved exhaustive.
Sixty-seven synthetic recognition cases calibrate the same joint lattice:
three seeds recover example heights 10^9 with 60/4 digits and 10^18 with
112/16 digits. These are empirical results, not target height bounds.
The actual curve remains at 64 digits. The checks support one bounded
128-digit experiment, with arithmetic identification still a separate
requirement. Runner 281 checks 1666 file hashes / 593 JSON records in
`cm_frame_structural_checkpoint.json`. Read
[the D84 report](certificates/cm-frame-structural-checkpoint.md).
The entries below record earlier milestones.

**2026-09-22, D83:** the internal and smaller cubics are independently
verified modulo 31^64, including highest-digit coefficient-error controls.
All earlier digits are preserved. Joint recognition over F is negative
in all eight embeddings at both 48/16 and 60/4 training/validation splits.
Exact integer certificates exclude integral homogeneous coordinate
height <=1,301,123 in the specified bases; this does not exclude F.
The package is `cm_frame_cubic_adjoint_package_64.json`, and the final
audit verifies 1329 hashes across 493 JSON records. An optional Sage
timeout exposed a descendant-process bug; its late output is archived,
and the corrected runner is tested. Use 274 for future recognition jobs.
Next test 128 digits with bounded stages. Read
[the D83 report](certificates/cm-frame-cubic-64.md). An exact
characteristic-zero equation and the target field remain unreconstructed.

**2026-09-22, D82:** the smaller cubic ell*T^3-3*A2*ell*T-R4=0,
weight(T)=1, is independently verified through 31^32. The unique divisor
E=K_X+2P+E40 gives 45 quadratic and 105 quartic coefficients; the 80P
chart remains internal to the verified linear class lift. Explicit
isomorphisms preserve D79's special fibre and D80's counts 68/2818.
Independent checks include highest-digit norm/trace error controls.
An exact rational basis for the 25-dimensional space containing A2 has
integer coefficients at most 5430 in absolute value. Joint recognition
in all eight embeddings of F, with eight unused validation digits, has
no surviving candidate. Next lift to 64 digits and repeat this bounded
search. The equation package and audit are
`cm_frame_cubic_adjoint_package_32.json` and
`cm_frame_cubic_adjoint_audit_32.json`. Read
[the precision report](certificates/cm-frame-cubic-precision.md).
A characteristic-zero equation and arithmetic identification remain open.

**2026-09-22, D81:** the marked genus-64 cubic is now **lifted and
independently verified modulo 961**, including its third, function
divisors, Frobenius descent and norm identity. The norm scalar lifts
from 27 to 58. All coefficients reduce to D79's equation; corruptions
adding 31 to the norm or a trace coefficient are rejected. Read
[the lift report](certificates/cm-frame-cubic-lift.md). Data:
`cm_frame_cubic_lift.{json,m}`; combined certificate:
`cm_frame_cubic_lift_check.json`; runner 194 checks/rebuilds/collects.
Next fix the representative's remaining normalization choices before
increasing precision. A characteristic-zero cubic and arithmetic
identification remain open.

**2026-09-22, D80:** the genus-64 cubic has **68 / 2,818 points over
F31 / F31^2**, exactly matching the existing old-plus-new Hecke
prediction. Independent Kummer fibre checks agree and reject a
changed count. The two power traces are -36,-1856; the full Euler
factor is not computed. Next start a bounded lift modulo 31^2 of
the marked cubic class and norm identities. Arithmetic identification
remains open. Read [the D80 report](certificates/cm-frame-cubic-frobenius.md).

**2026-09-21, D79:** an explicit cubic over the candidate C modulo 31
has smooth projective normalization of **genus 64**. Its equation is
Q4*T^3-3*A4*Q4*T-P10=0 with T of weight two. A descended divisor
representative and the exact Kummer norm identity give the S3 closure
and reflection quotient. Independent verification passes and rejects
changed norm and trace coefficients. Next compare its Frobenius data
with the intended Hecke prediction, then lift the marked cover 31-adically.
The arithmetic identification and characteristic-zero cubic remain open.
Read [the D79 report](certificates/cm-frame-cubic-cover.md).

**2026-09-21, D78:** a verified class A on the genus-40 candidate
modulo 31 satisfies **3[A]=-[D+-D-]**. It is fixed by Frobenius and
negated by the involution. Exact section spaces of dimensions
81,201,321 support the class operations. The saved relation is
checked without the proposed class number, and a wrong class is
rejected. Next recover the Kummer function, handling the representative's
constant-field descent, then construct the cubic and reflection
quotient. Read [the D78 report](certificates/cm-frame-cover-class-arithmetic.md).

**2026-09-19, D77:** the normalized B3 fibre on the rational genus-40
cover is **K(sqrt(-3))**, degree 18 over Q. Exact jets and a square
witness give two explicit degree-nine divisors after adjoining sqrt(-3).
Independent checks certify the parameter change, involution and
specialization at 31. The cubic inertia condition selects the F-scalar
twist within this fixed branch-half class. Their difference is proved
nonprincipal, so the next step requires a nontrivial 3-division in the
divisor class group. No cyclic cubic or genus-64 Y is constructed.
Read [the D77 report](certificates/cm-frame-B3-fiber.md).

**2026-09-18, D76:** an exact rational double-cover equation on the
certified genus-16 candidate now has integral numerator/denominator
heights **583 / 2935433**. Its smooth normalization has genus 40 and
odd branch divisor D17+P32, degree 18. Recognizing the full six-product
space succeeds; exact Veronese identities and rational membership
witnesses then prove the divisor statement. Independent checks match
the old cover through 31^128 and reject a wrong twist. The global
arithmetic identification and twist remain open. Next compute the
normalized degree-18 fibre over B3 for the cyclic cubic step.
Read [the D76 report](certificates/cm-frame-rational-double-cover.md).

**2026-09-18, D75:** a new geometric normalization gives an exact rational
numerator of height **583**. Replacing the auxiliary 7*P32 by B3 preserves
the branch half; an explicit square factor certifies the same cover at 31.
The independent certificate rejects a wrong quadratic twist. The old
31^128 lift remains available; transferring this normalization to that
precision is next. Joint F recognition in the old 17-dimensional space
has no survivors, with a separate exact coefficient-box exclusion of
8066216 in those bases. No number-field cover or target polynomial is
obtained. Read [the D75 report](certificates/cm-frame-joint-field-and-B3-normalization.md).

**2026-09-18, D74:** precision doubling reaches 31^128, with independent
divisor and same-radicand certificates at all four new stages. The
39-digit numerator is retained. No tested Q/F coefficient candidate
passes validation against unused digits. A known-section control
reveals substantial coordinate growth, and an exact 17-dimensional
denominator space is constructed and reduced. Its seventeen section
heights range from 39 to 96 digits; their multiplication identities
and expression for the 128-digit denominator are independently checked.
Next test joint projective recognition over F with a common F-valued
scale. No number-field cover or target polynomial is obtained.
Read [the full report](certificates/cm-frame-precision-doubling.md).

**2026-09-18, D73:** the exact rational numerator now has 39-digit
primitive coefficient height, down from 631. The fixed section-chart
lattice gives 48 digits; allowing all 91 curve equations gives 39.
The denominator is transferred by a verified cross-product identity,
preserving the same radicand modulo 31^8. Independent exact checks and
a highest-digit corruption control pass. The new degree-28 common
residual is reduced, with factor degrees [1,1,26]. Next extend precision
and seek recognition over F, tracking scalar changes explicitly.
The denominator's arithmetic height and the number-field cover remain
unknown. Read [the normalization report](certificates/cm-frame-normalization.md).

**2026-09-18, D72:** the double-cover equation lifts exactly through
31⁸=852891037441. An independent Magma check certifies the divisor
identity at that modulus and rejects a highest-digit error. The
seven lifting steps take 38.547 s including startup; checking takes
2.351 s. The numerator is independently recovered over Q and matches
the lift. Its 631-digit primitive height motivates reducing the
13-dimensional numerator space before higher-precision reconstruction.
The denominator and full cover over F remain unrecognized, and the
Shimura identification remains open.
Read [the lifting report](certificates/cm-frame-resolvent-lift.md).

**2026-09-18, D71:** explicit quadrics give a double cover over F31
with divisor identity `div(u)=D17+15P32-2E`, deg(E)=16. Its branch
divisor is B2=D17+P32 and its genus is 40. Its two constant twists
have 45 and 55 points; 45 matches the norm-one Hecke prediction.
Geometric divisor halving took 466.760 s; the independent certificate
and counts took 10.897 s. A corrupted numerator is rejected.
This is a finite-field cover, with no characteristic-zero lift or
Shimura identification yet. Next implement a first lift of its
degree-nine half line bundle modulo 31², before arithmetic recognition
over F and the specified cubic construction.
Read [the resolvent report](certificates/cm-frame-resolvent.md).

**2026-09-18, D70:** the verified candidate now has an exact ordinary
rational point and disjoint closed points of degrees 17 and 9. Seven
small linear forms cut out the nonic divisor; its residue field has
proved Galois group 9T15, of order 72. All marks reduce well at 31.
These are candidates for all the cover's branch locations, with CM
labels still numerical. The exact computation `h0(2B3-B2)=0` rules
out one simple quadratic-resolvent recipe. Next recover the correct
cover extension data using the saved S3 monodromy; independent
Shimura identification also remains open. Scripts 119 and 120 pass.
Read [the marked-divisor report](certificates/cm-frame-marks.md).

**2026-09-18, D69:** D68's equations provably define a smooth,
geometrically integral canonical genus-16 curve over Q, with good
reduction at 31. A rank-30 free coordinate algebra gives squarefree
trace discriminants on both charts. Direct point counts 50 over F31
and 1,400 over F31² agree with the saved Hecke predictions. The three
bounded verification jobs pass. Identification with the specified
Shimura curve still requires independent arithmetic input; the counts
do not prove it. Then the actual degree-three Y/C remains to be built.
Read [the verification report](certificates/cm-frame-verification.md).

**2026-09-18, D68:** the source review leads to a CM projective-frame
construction and 91 independent integer quadrics for a candidate base
curve. The maximum coefficient is 1,514. Exact checks give degree 30
and arithmetic genus 16 over Q, an integral special fiber in a flat
model at 31, and the prescribed degree-17 CM point. Smoothness and
identification with the specified Shimura curve remain unproved.
Next verify the candidate, then construct the genus-64 cover; backend
cleanup stays paused. Read [the construction report](certificates/curve-construction-sources-2026-09-18.md)
and use [the Magma candidate](data/computed/cm_frame_curve_candidate.m).
The old assertion that no candidate equations exist is superseded;
the required target arithmetic input is still not certified.

**2026-09-17, D67:** all three allocation-audit jobs pass. The
instrumented genus-16/a=51 control takes 444.494 s overall under the
same 2 GB/900 s limits. Group multiplication accounts for about 82%
of lift time. A 34.5 MB product matrix adds 136.5 MB to the stack,
and that workspace remains after its last use. Next test two explicit
cleanup changes in a separate build. Twenty tracing-off/on comparisons
preserve exact matrices and random states; original C tokens and
D63–D66 provenance are verified. No optimization or target arithmetic
construction is claimed. See [the allocation report](certificates/lifttors-allocation.md).

**2026-09-17, D66:** the genus-16, a=51, e=4 control passes under the
unchanged 2 GB cap and 900-second timeout: one lift takes 364.194 s
and the complete control 439.776 s with the D65 library. Both kernels
verify every equation. A separate D66 build fixes an upstream shape
error when reducing auxiliary evaluation tables. Independent reduction
and projective evaluation controls, 60 lift comparisons and Q8 recovery
pass. The corrected scale control also passes in 440.569 s overall.
Reduced Jacobian data still occupy about 120 MB at genus 16; the next
allocation audit concerns retained data and group operations.
No genus-64/a=51 run or actual target section construction is claimed.
See [the degree-51 report](certificates/lifttors-degree51.md).

**2026-09-17, D65:** native equation generation passes all nine controls.
At genus 64, a=2, e=4, one lift takes 514.585 s and the complete control
690.829 s under the same 2 GB stack cap. It checks the exact branch
divisor and 2-torsion, storing at most 83,398 equation entries instead
of 5,504,268. Every equation is regenerated for verification. Other
operations still grow the stack to the cap. The 11,172 entry comparisons,
60 three-way lift cases, 12 known kernels, 6 rank-drop rejections and
Q8 field recovery pass. The separate build preserves D63/D64 artifacts.
Next measure genus 16 at degree 51 under the same limits; that optional
job has not run. Actual target sections and the polynomial remain open.
See [the native report](certificates/lifttors-rows.md).

**2026-09-16, D64:** the genus-4 control passes at residue degree 51,
with one lift taking 8.356 s versus 0.264 s at degree two. The same
stack cap and timeout apply. Measured entry sizes project to roughly
9.1 GB for the existing genus-64 equation matrix; this is a conditional
object-size estimate, not measured peak memory. A row-generation
prototype passes all 11,172 entry comparisons and four kernel checks.
Next integrate that formula into a native path with complete residual
verification. No genus-64/a=51 job was launched. D63's library and
recorded source digests are unchanged. Target arithmetic sections,
torsion and the polynomial remain open. See
[the extension report](certificates/lifttors-extension.md).

**2026-09-16, D63:** the genus-64 known-answer control now passes under
the unchanged 2 GB PARI stack cap. Streamed product matrices and a
batched exact kernel solve resolve two distinct allocation failures.
One lift to 97^4 over residue degree two takes 613.521 s; the complete
control takes 784.161 s and checks the known exact divisor and 2-torsion.
The full Q8 and genus-16 controls pass, with 70 validator comparisons,
60 lift comparisons, 12 known kernels and 6 rank-drop rejections. All
111 existing tests pass. See [the report](certificates/lifttors-memory.md).
The next small-curve calibration concerns residue degree 51; target
arithmetic sections, torsion and the nonsolvable polynomial remain open.

**2026-09-16, D62:** the saved quaternion order, full genus-40 graph and
Kurihara's quotient theorem support D45's geometric identification at 2.
The actual LiftTors backend recovers the known Q(i) torsion field of the
Q8 control after lifting to 7^64. A genus-16 control passes; genus 64
overflows a 2 GB PARI stack in the lifting routine. The next backend task
is that allocation issue, before major target model work. A separate
validator memory adaptation passes 70 exact comparisons with upstream;
all 111 existing tests pass. See [the results](certificates/lifttors-control.md).
No target arithmetic section/model, torsion point or polynomial is obtained.

**2026-09-16, D61:** the user's requested stocktake recommends retaining
the broad curve/Jacobian route while pausing repeated CM-coordinate
recognition scans. The next work needs a concrete arithmetic section
construction and a specified connection to the global model or Jacobian
input. Exact CM restrictions alone would not finish that step. The
generic torsion backend and its relevant cost remain untested. See
[the review](certificates/stocktake-2026-09-16.md). No new computation;
the latest implementation suite remains 111 passing tests.

**2026-09-16, D60:** the evaluation plane span(X,Y) is tested independently
of its generators. Exact lattice/exterior-power certificates exclude
every rational space inside the empirical chart boxes up to heights
about 1.99e10 for Q X, 1.35e10 for Q Y and 4.32e19 for the plane.
These heights refer to primitive coordinates/minors in the fixed
D59 field basis. The target's membership in the boxes remains uncertified,
so these are not unconditional target-height bounds. All 111 tests pass;
see [the proof and results](certificates/cm-flag-height.md) and
[test log](data/computed/cm_flag_height_tests_20260916.out).

**2026-09-16, D59:** exact quaternion intertwiners and ideal intersections
label the seventeen CM points by Cl(K)=C17, now independently proved.
Frobenius at (31,beta-19), class 3, matches their order to Elkies's roots.
The complex orientation and reference point retain explicit numerical
inputs. A trace-centered residue-field basis has evaluation condition
40.9175. A bounded joint LLL search accepts no exact X or Y direction;
the existing values do not complete this reconstruction at the tested
bounds. All 103 tests pass. See
[the orbit and reconstruction report](certificates/cm-orbit-recognition.md)
and [test log](data/computed/cm_orbit_tests_20260916.out).

**2026-09-16, D58:** the canonical double cover and its distinguished CM
point give marked descent to Q without hyperellipticity. Under D56's
existing hypotheses, the normalized X,Y rigidify the marked curve and
are Q-defined. Script 95 checks exact arithmetic prerequisites and runs
a bounded rational reconstruction on saved CM polynomial data. No full
polynomial is recovered; all hits at denominator cap 10^6 are ambiguous.
All 96 tests pass. See [the proof and pilot](certificates/marked-descent.md)
and [test log](data/computed/marked_descent_tests_20260916.out).

**2026-09-16, D57:** the exact CM-input audit verifies the fields of all
seventeen saved elliptic generators and computes reductions of the
known degree-17 CM residue algebra. This algebra does not supply section
evaluations. The precise missing input is the nested pair of evaluation
spaces `ev_D L(17P) subset ev_D L(18P)`, which would determine the
CM-normalized restrictions. Exact counterexamples show why the field
and trace conditions alone cannot select them. All 90 tests pass; see
[the report](certificates/cm-arithmetic-input-audit.md) and
[test log](data/computed/cm_arithmetic_tests_20260916.out).

**2026-09-16, D56:** section multiplication constructs numerical functions
with sole poles 17P and 18P on the genus-16 curve. Traces over the seventeen
order-two CM points fix their arithmetic normalization. Under the stated
ordinary-point and nonvanishing hypotheses, the resulting X,Y are F-defined
and generate F(C). Their exact coefficients remain unknown, and every
attempted plane-equation fit fails independent validation. All 84 tests
pass, including the thesis Q8 control; the
[test log](data/computed/pointed_maps_tests_20260916.out) is saved locally.

The original target has a conditional realization in the Jacobian of a
genus-64 cover; see [target-realization.md](certificates/target-realization.md).
Neither an exact model of the base or cover nor the required torsion points
have been computed. D58 narrows the CM reconstruction target to Q,
and D59 supplies the labelled orbit for simultaneous recognition in
its known residue field. D60 strengthens the bounded negative result
with exact exclusions inside empirical boxes. Exact evaluation data,
a specified special-divisor function, or a justified reconstruction
height/accuracy budget remain missing. See
[cm-pointed-maps.md](certificates/cm-pointed-maps.md) for the construction,
failed fits, hypotheses and reproduction commands.

## Earlier completed milestones

The first five checkpoints are complete. The characteristic-zero space decomposes with
dimensions `[1, 2, 2, 4, 16, 32]`, and Dembélé's two mod-\(2\) systems are the reductions
of the unique 16-dimensional component at the two unramified residue-degree-8 primes above
\(2\) in its Hecke field. The exact argument and defining polynomial are recorded in
`certificates/lift-report.md`.

The Eisenstein back end for the Costa–Schiavone–Voight isogeny polynomial has passed a
genus-4 control, and the characteristic-zero lift / residual match / \(C_8\)-equivariance
/ (GRH) polarization gates are complete. An exhaustive audit of remaining constructive
ideas — twisted-\(L\) periods, Shimura-curve periods, dense and sparse Frobenius–Hunter
search, \(\Omega^+\)+RM sign recovery, classical mod-\(2\) forms, HMF/RieSrf hacks, and
CSV without a new front end — is recorded in `certificates/idea-exhaustion.md`.
Those experiments did not produce the required periods or torsion. That
historical audit predates the current curve route summarized above; it
should not be used as the latest project status.

Supporting certificates: `eisenstein-prototype.md`, `period-feasibility.md`,
`frob-disc-gate.md`, `torsion-construction-scorecard.md`, `char0-equivariance.md`,
`cunningham-dembele-audit.md`. Polarization data:
`data/computed/lift_field_ideals.json`, `data/computed/brauer_local_data.json`.

## Running computations

Run the source-data checks:

```sh
python3 dembele/tests/test_published_data.py
```

Run the base-field certificate locally:

```sh
python3 dembele/tests/run_magma_certificate.py \
  dembele/magma/00_field.m PASS\|dembele_field_certificate
```

The wrapper requires an explicit `PASS` marker because Magma may report process status
zero even after a source-level runtime error.

Long Magma jobs can be sent to chatelet using the checked-in client:

```sh
python3 remote_magma/cocalc.py --timeout 3600 run dembele/magma/job.m
```

See `remote_magma/CHATELET.md` before launching detached work. In particular, CoCalc's
API timeout is also the remote process's CPU limit.

## Reproducibility policy

- Exact inputs, source revisions, and Magma versions are part of every result.
- Expensive precomputation must have a manifest and checksum.
- Numerical period calculations may discover a polynomial but cannot certify it.
- The notation
  \(\operatorname{SL}_2(\mathbf F_{256})^2\mathbin{\cdot}8\) in Dembélé's paper is not,
  without further work, a certificate that the group extension splits.
