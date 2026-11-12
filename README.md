# Making Dembélé's field explicit

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

**Execution resumed (2026-10-05):** D133 resumed from correction 10 after
all transfer and dependency hashes passed. Production and the continuation
for D133 audits/review and D134 are running at the recorded observation.
See [HANDOFF.md](HANDOFF.md) and the [resumption record](dembele/checkpoints/d133-resume-2026-10-05.json)
for logs and restart checks. Certified precision remains P800 for the bank,
P3200 for column 0 and P1600 for column 1. The transfer pause below is historical.

**Transfer checkpoint (2026-09-30):** D133 is paused cleanly after correction 9,
before `low_begin_010`, for continued work with dots. The source, receipts and
retained payloads are versioned; large artifacts require `git lfs pull`.
Read [CHECKPOINT.md](CHECKPOINT.md) for integrity verification, native dependency
constraints and resumption. P6400 is unfinished; certified precision remains
P800 for the bank, P3200 for column 0 and P1600 for column 1. Earlier descriptions
of running sessions below are historical.

This repository is a computational research project whose main goal is to construct an
explicit defining polynomial for the nonsolvable Galois extension of
\(\mathbf Q\), ramified only at \(2\), whose existence was proved by
[Lassina Dembélé](https://arxiv.org/abs/0811.4379).

The earlier work in this repository investigated whether the same goal could be reached
through 2-group Belyi maps arising from Musty's thesis. That investigation produced useful
code, computations, and a nearly complete obstruction argument, but it did not construct
Dembélé's field. Current work uses Shimura curves to realize Dembélé's original
Hilbert-modular representations, reusing the Belyi code where useful.

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

**Previous state (2026-09-28, D131 complete):**

The weighted-only certificate and recoverable row journal pass their
controls. All 4,454,400 state coordinates and 870,400 CM coordinates
replay against the actual P=3200 reference. Recovery passes nineteen
distinct interruption boundaries and four corruption/stale-journal
checks. A fresh computation of a known P=1600 correction also passes
through the journal, including every original low equation and residual.
D129 already evaluated CM from weighted inputs; D131 adds streaming
authentication and GMP replay without retaining another uniform state.

All 54 input jobs and both reviews pass. Review 546 binds 16567 hashes,
preserving all 16142 from D130. Freeze 541--546, `run_d131_batch.py`,
bound artifacts and sealed stores. No mathematical precision increases:
the full bank remains P=800, column 0 P=3200 and column 1 P=1600.
Exact candidate identification and the original-kernel polynomial remain open.

Source 547 is next unused. Complete the staged driver with resumable
low-RHS chunks and multi-digit solves, one working store, a full file
lifetime inventory and a separate concurrent-RAM budget. The target
reservation fits the 2 GiB per-store cap; complete target execution is
not yet certified. Select the next actual refinement after those gates.
Keep at most three mathematical workers and the unchanged 180-second
process-group cap. D130's timing model is a pre-redesign baseline, not
an updated ETA. Marked arithmetic covers and Y64 sections remain open.

See the [D131 report](dembele/certificates/dyadic-weighted-journal-d131.md)
and [current handoff](HANDOFF.md). All earlier next-step instructions below
are historical; the D130 packet proposed below is now completed.

**Previous state (2026-09-28, D130 complete):**

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

**Previous state (2026-09-28, D129 complete):**

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

**Previous state (2026-09-28, D128 complete):**

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

**Previous state (2026-09-28, D127 complete):**

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

**Previous state (2026-09-28, D126 complete):**

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

**Previous state (2026-09-28, D125 complete):**

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

**Previous state (2026-09-28, D124 complete):**

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

**Previous completed state (2026-09-27, D123 complete):** one actual harmonic column
now reaches precision 800, including all seventeen CM charts and an
independent audit. A weighted representation and twelve shrinking
corrections reproduce the same verified column with substantially smaller
checkpoint files. All 148 input jobs pass; the final review binds 2532
source hashes and preserves all 1884 D122 hashes.

The full sixteen-column bank remains at precision 400. The accepted
quadric bounds are unchanged; exact curve identification and the field
polynomial remain open. Read
[the new result and proof](dembele/certificates/dyadic-staged-pilot-d123.md)
and [the handoff](HANDOFF.md). Next combine the weighted solver with
resumable state chunks and cost one precision-1600 column, including
memory use. That larger run has not started. All workers have completed;
decisions and references are current. Earlier next tasks are historical.

**Previous completed state (2026-09-27, D122):** the sixteen-column P=400
bank, residue-frame comparison and independent arithmetic audit pass;
the final review binds 1884 source hashes.
All 6188 quadratic coefficients contain zero in their certified balls;
no mismatch is found. Exact equality and the field polynomial remain open.
The section bounds improve to 4194/4145/4128, still below the sufficient
25305/25419/25526. W's Gaussian is now certified nonzero and has not been
inverted.

Read [the reviewed result](dembele/certificates/dyadic-precision400-d122.md)
and [the handoff](HANDOFF.md), including recovery after a disconnected
chat. Next cost one P=800 column using a generalized lift with state-chunk
checkpoints. That implementation has not started. All jobs have completed;
decisions, references and entry documents are current. Earlier next tasks
are historical.


**Previous interim checkpoint (2026-09-27, D122):** all sixteen actual harmonic columns
and all seventeen CM charts now reach P=400. All 155 computation jobs
pass, with four coarse coefficients certified to beta-errors
[832,848,832,864]. The algebraic CM frame is refined separately to
21168 beta-digits. All batch workers have finished; no jobs remain running.

The residue-frame and quadric comparison scripts are drafted but unrun;
an independent D122 mathematical review is still pending. The provenance
checkpoint and hash replay pass, binding 1844 sources and preserving all
1079 D121 hashes and the completed job receipts.
Exact curve identification and the field polynomial remain open. Read
[the progress checkpoint](dembele/certificates/dyadic-precision400-progress-d122.md)
and [the handoff with exact resume commands](HANDOFF.md). Decisions,
references and all entry documents are current; earlier next tasks are
historical.


**Previous checkpoint (2026-09-27, D121):** the low-moment solver now works,
and one actual harmonic column has been refined from 200 to 400 digits,
including all seventeen CM charts and four differential coefficients.
All transport parameters have certified precision of 10552 digits.
The complete sixteen-column bank remains at 200 digits; exact curve
identification and the field polynomial remain open.

The next work accelerates polynomial transport, then completes the
sixteen-column 400-digit bank and tests the quadrics again. Independent
review binds 1079 sources, preserving all 961 prior hashes. Read
[the result and next task](dembele/certificates/dyadic-schur-lift-d121.md)
and [the handoff](HANDOFF.md). Decisions and references are updated.


**Previous checkpoint (2026-09-26, D120):** retain the direct integral-section
certificate. A complete comparison rejects the proposed inverse-frame
bound, and a Faltings-height upper bound excludes improving that input
alone as a rescue. A conditional working-precision target is now proved:
**P=10552**, provided the refined quadratic enclosures contain zero.

New transport code passes the frozen-data checks and a synthetic operation
at that precision. A complete run still needs an affordable iteration;
the next test eliminates low moments on the existing P=200 bank. Existing
Hecke data also settle norm-97 target cofactor separation, with the useful
target available over residue degree 51. Exact curve identification and
the field polynomial remain open. Review 462 binds 961 sources and
preserves all 922 prior hashes. Read
[the reassessment and next task](dembele/certificates/construction-reassessment-d120.md)
and [the handoff](HANDOFF.md). Decisions and references are updated.


**Previous checkpoint (2026-09-26, D119):** the actual CM divisor and its
dyadic principal-parts lattice are now determined. The residue-map
index has beta-valuation **16**, with contributions **14** from
cohomology torsion and **2** from the primitive principal part.
Its cokernel is killed by beta squared. This resolves a local
normalization problem; exact curve identification and the target
field polynomial remain open.

Independent review binds 922 sources and preserves all 911 prior
hashes. Read [the D119 proof and next task](dembele/certificates/cm-cartier-frame-d119.md)
and [the handoff](HANDOFF.md). The next task tests the full height
budget for this intrinsic frame. Current sufficient section valuations
remain **25330/25444/25551**, versus actual **3794/3745/3728**.
Decisions and references are updated; no moment precision was increased.


**Previous checkpoint (2026-09-26, D118):** the omitted dyadic CM height
correction is now certified, and the known reduction graph supplies
a stronger Faltings-height bound. Together they reduce the sufficient
exact-identification section valuations to **25330/25444/25551**, versus
actual lower bounds **3794/3745/3728**. Exact curve identification and
the target field polynomial remain open.

The independent review binds 911 sources and preserves all 891 prior
hashes. All four input jobs pass. Read
[the D118 proof and next task](dembele/certificates/cm-finite-height-d118.md)
and [the handoff](HANDOFF.md). The next task tests a different integral
frame construction, starting with the actual CM divisor and principal-parts
lattice. No moment precision was increased. Decisions, references and
resource pauses are current.


**Previous checkpoint (2026-09-26, D117):** a uniform arithmetic CM disk
bound reduces the sufficient exact-identification thresholds from roughly
120000 to **35947/36096/36237**. The actual integral-section lower bounds
remain **3794/3745/3728**, so exact curve identification and the target
field polynomial remain open.

An exhaustive CM lattice calculation and an independent enumeration certify
the larger disks at all seventeen CM points and conjugates. Review 450
binds 891 sources, preserving all 868 prior hashes. Read
[the D117 proof and next arithmetic task](dembele/certificates/cm-disk-and-exactness-d117.md)
and [the handoff](HANDOFF.md). Even an ideal disk would leave this bound's
thresholds above 33000 for the higher orders. The next task is to recover
the omitted finite arithmetic height corrections; another routine precision
increase is not the main plan. Decisions, references and resource pauses
are current.


**Previous checkpoint (2026-09-26, D116):** we have a stronger arithmetic
identification criterion and all four required coarse differential
coefficients. It tests the 91 candidate quadrics directly as integral
sections, avoiding ratio denominators and a separate rank-45 test.
The sufficient successive beta-valuations are **119806/120284/120758**;
the actual lower bounds are **3794/3745/3728**. The higher tests require
the preceding jets to vanish exactly. No positive jet has met its
exact-vanishing bound, so the curve identification and field polynomial
remain open.

The proof also identifies the harmonic basis with the stable integral
differential lattice. Independent checks cover all third coarse
coefficients and all 4641 positive quadratic coefficients, preserving
814 prior source hashes in the 868-source final review. Read
[the D116 proof and revised plan](dembele/certificates/cm-compound-height-d116.md)
and [the handoff](HANDOFF.md). The next task is to close the exactness
gap through a sharper bound on the actual sections or an exact identity;
another small precision increase is not the main plan. Decisions,
references and resource pauses are current.


**Previous checkpoint (2026-09-25, D115):** the independent Shimura computation
now reaches the actual rational residue frame and its first two ratio
coefficients. They agree with the candidate within certified beta-error
bounds **101 and 70** at the sixteen non-anchor CM points. W's leading
value is resolved, and the chosen ratio chart is proved valid on the
CM divisor. Review 431 binds 814 sources and preserves 713 prior hashes.
Read [the reassessment and results](dembele/certificates/dyadic-comparison-and-strategy-d115.md)
and [the handoff](HANDOFF.md).

This supports the route, but exact identification remains open. The
current height bound would require 137121/410387 pi-digits for equality
at orders 1/2; the achieved comparisons do not meet it. The revised
priority is an exact arithmetic identification certificate, rather than
another routine precision increase. Global cubic data, target torsion
and the field polynomial remain unfinished. Decisions, references and
resource pauses are current; earlier next steps are historical.


**Previous checkpoint (D114):** we have computed the first
three coarse coefficients of all sixteen actual harmonic differentials
at all seventeen matched CM points. Their certified errors are
32,40,32 pi-digits. All 256 non-anchor entries at each order are
certified nonzero. Independent review binds 713 sources and preserves
all 696 prior hashes.
Read [the D114 proof](dembele/certificates/dyadic-coarse-d114.md)
and [the handoff](HANDOFF.md).

The W anchor remains unresolved: the coefficient valuations are
at least 32.5,40.5,32.5, without a claim of exact vanishing. We
proved that increasing the moment degree alone at precision 16
cannot resolve it. Next raise working precision to 24 with the
full local-field arithmetic. These are actual differential jets
in the harmonic basis; rational-frame ratio jets, candidate
identification and the target polynomial remain open. Decisions
and references are updated; resource pauses remain. Earlier next
steps are historical.


**Previous checkpoint (D113):** we have computed certified
positive-degree moments of the sixteen actual harmonic measures.
A finite contracting system replaces an expanding tree search.
It gives 33,408 moments in the saved edge charts and the first
three positive moments in all 51 matched CM charts, with explicit
error bounds. Independent arithmetic and direct integration checks
pass; the review binds 696 sources and preserves 682 prior hashes.
Read [the D113 proof](dembele/certificates/dyadic-moments-d113.md)
and [the handoff](HANDOFF.md).

Next use a modest higher-degree moment bank to evaluate the actual
coarse differential coefficients. The W anchor is unresolved at
the current precision, so normalization still needs a nonvanishing
certificate. Actual Shimura jets, candidate identification and the
target polynomial remain open. Decisions and references are updated;
resource pauses remain. Earlier next steps are historical.


**Previous checkpoint (D112):** all seventeen CM points now
have certified dyadic coordinates and arithmetic labels, matched
to the saved rational residue frame. Exact ideal witnesses and a
certified Galois resolvent fix the label correspondence and its
direction. We also have the sixteen harmonic measures' zeroth
masses on all 51 CM boundary charts. Independent review binds
682 sources and preserves all 661 prior hashes.
Read [the D112 proof](dembele/certificates/dyadic-cm-matching-d112.md)
and [the handoff](HANDOFF.md).

Next compute positive-degree moments in these charts with proved
error bounds over the ramified dyadic field. Actual Shimura jets,
candidate identification and the target polynomial remain open.
Decisions and references are updated; resource pauses remain in force.
Earlier next steps are historical.


**Previous checkpoint (D111):** we have constructed sixteen
actual invariant harmonic cocycles and an arithmetic evaluator for
their boundary-ball masses. All neighbor transports and stabilizers
for the existing 58 classes are certified. The measures have integral
values, giving denominator bound zero. Independent review binds
661 sources and preserves all 643 prior hashes.
Read [the D111 proof](dembele/certificates/dyadic-harmonic-d111.md)
and [the handoff](HANDOFF.md).

Next identify the dyadic CM embedding and its marked frame, then
compute certified moments in those coordinates. Actual Shimura jets,
candidate identification and the target polynomial remain open.
Decisions and references are updated; resource pauses remain in force.
Earlier next steps are historical.


**Previous checkpoint (D110):** the dyadic arithmetic group and
its Atkin--Lehner coset now have explicit certified witnesses. An
involution moves the base vertex seven edges, a norm-one element moves
it fourteen, and an explicit hyperbolic element has translation length
fourteen. The arithmetic matches the saved 58-class Brandt data exactly.
Read [the D110 proof](dembele/certificates/dyadic-group-transport-d110.md)
and [the handoff](HANDOFF.md). Independent review binds 643 sources,
preserving all 629 prior hashes.

Next complete the finite edge-reduction data for those same classes
and construct the invariant harmonic cocycles. Actual moments, dyadic
CM/frame matching, Shimura jets and candidate identification remain
open; the target polynomial is unconstructed. Decisions and references
are updated, and resource pauses remain. Earlier next steps are historical.


**Previous checkpoint (D109):** the definite quaternion order
is exported, its integral dyadic matrix embedding is certified, and
an explicit norm-one unit is verified to cycle the three edges at
the base vertex. This completes the bounded local-arithmetic plan.
Read [the D109 proof](dembele/certificates/definite-dyadic-d109.md)
and [the handoff](HANDOFF.md). The independent replay binds 629
sources and preserves all 606 D108 hashes.

Next make the known arithmetic group and normalizer quotient explicit
in these coordinates and verify a transport moving the base vertex,
using the saved 58-class data. Actual harmonic cocycles, moments and
dyadic CM/frame matching remain needed. No actual Shimura tangent,
candidate identification or target polynomial has been obtained.
Decisions and references are updated; resource pauses remain in force.
Earlier next steps are historical.


**Previous checkpoint (D108):** a certified feasibility check
rules out the proposed refinement of the current absolute spectral
bound: the seven omitted norm-31 primes alone force it above 60.32
times the saved partial sum. This limits that comparison method,
not the field's existence or the actual error.

We now have a conditional 2-adic formula with explicit errors for
the first three local differential coefficients. Its tests use
synthetic measures; actual Shimura moments remain missing. Next
construct the definite order's dyadic matrix embedding and a verified
edge transport. Read [the D108 report](dembele/certificates/shimura-evaluator-d108.md)
and [the handoff](HANDOFF.md). The review passes and binds 606 sources,
preserving all 588 D107 hashes. Decisions and references are updated.
No actual tangent, candidate identification or target polynomial
has been obtained. Earlier next steps are historical.


**Previous checkpoint (D107):** the correspondence between the
seventeen CM points and the degree-17 polynomial roots is certified.
An exact real-structure witness fixes the reference point; rational
root disks, a field-norm argument and a finite rank certificate
establish the Frobenius action and recover the old lookup.
Read [the D107 proof](dembele/certificates/cm-root-matching-d107.md)
and [the handoff](HANDOFF.md). The independent review passes,
binding 588 sources and preserving all 562 D106 hashes.

This identifies the arithmetic labels for the rational CM frame.
Certified differential values, a tangent chart and an independent
Shimura tangent/jet evaluation remain needed to identify the candidate.
The target polynomial is unconstructed. Decisions and references
are updated; the spectral pilot gate and resource pauses remain.
Earlier next steps are historical.


**Previous checkpoint (D106):** the CM-marked curve has trivial
geometric automorphism group. This removes the remaining twist
ambiguity in its Q-descent and gives a canonical rational CM frame.
Its ratio jets lie in the degree-17 residue field, with explicit
height bounds through order three. Exact candidate reference jets
are independently checked; the shorter identification test has
a sufficient common precision of 31^9746 at the inert prime 31.
Read [the D106 proof](dembele/certificates/cm-rational-frame-jets-d106.md)
and [the handoff](HANDOFF.md). Audit 389 binds 562 sources and preserves
all 543 D105 hashes. An independent Shimura evaluator, the saved
numerical point/root matching and candidate identification remain
open. The target polynomial is unconstructed. Decisions and
references are updated; earlier next steps are historical.


**Previous checkpoint (D105):** the actual seventeen CM points
are now proved to form a projective frame. Nine exact specialization
certificates establish `H0(K_C-D)=0`; CM transitivity makes every
evaluation cofactor nonzero. A frame over the degree-272 CM class
field has projective tangent height below 10504, with at least one
of fifteen valid charts. This bypasses the old numerical labelling
for work over that auxiliary field; the saved labels and descent
remain uncertified. Read
[the D105 proof](dembele/certificates/cm-frame-arithmetic-d105.md)
and [the handoff](HANDOFF.md). The independent audit passes and binds
543 sources. An actual tangent/jet evaluation and candidate
identification remain open; the target polynomial is unconstructed.
Decisions and references are updated. Earlier next steps are historical.

**Previous checkpoint (D104):** the stable CM fibre height is now
bounded by `H_CM,disk<4.1`. Together with D103 this gives the conditional
tangent-height bound `h(v_j)<10504`. Two rational analytic calculations
agree, and the audit preserves all previous bound sources.
Read [the D104 proof](dembele/certificates/cm-intrinsic-height-d104.md)
and [the handoff](HANDOFF.md). Arithmetic CM labelling and frame/chart
nonvanishing still need certification; no independent tangent or
candidate identification has been obtained. Conservative conditional
equality tolerances are now explicit. The field polynomial remains
unconstructed. Earlier next-step instructions below are historical.

**Previous checkpoint (D103):** an integral adjugate construction
gives the conditional tangent-height bound `h(v_j) <= 513*H_CM,disk + 8400`.
It avoids separately bounding the residue-frame index. Exact checks
pass, but the actual CM fibre height H_CM,disk remains unbounded, and
the arithmetic frame hypotheses still need certification. Next address
its comparison with a known Hodge-height formula at the dyadic
quotient. Read [the D103 proof](dembele/certificates/cm-adjugate-height-d103.md)
and [the handoff](HANDOFF.md). No independent Shimura tangent or usable
recognition tolerance has been obtained; the field polynomial remains
unconstructed.

**Previous checkpoint (D102):** the arithmetic-normalization task
now has an exact local formula for the residue-frame index and a
verified conversion for the saved field basis. Two geometric terms
still need bounds on the actual Shimura curve; good reduction alone
does not remove them. An explicit cofactor formula isolates the
archimedean comparison too. Read
[the D102 result](dembele/certificates/cm-residue-lattice-d102.md)
and [the handoff](HANDOFF.md). The arithmetic checks pass, but no
independent Shimura tangent or effective recognition tolerance has
been obtained. The field polynomial remains unconstructed.

**Previous checkpoint (D101):** the first exactness investigation
expresses the CM tangent as ratios of algebraic tricanonical sections
and gives explicit conditional recognition criteria. The actual
arithmetic frame and lattice bounds remain missing, so no independent
Shimura tangent or usable target precision has been certified. An exact
candidate tangent is now independently checked, including its mod-31
comparison; it does not identify the candidate. Read
[the D101 result](dembele/certificates/cm-tangent-exactness-d101.md)
and [the handoff](HANDOFF.md). Next address the arithmetic lattice
comparison before another spectral-bound pilot. The field polynomial
remains unconstructed.

**Previous checkpoint (D100):** the methodology review retains the
Shimura-curve/Jacobian route while separating three open requirements:
arithmetic identification of the candidate, exact global cubic or
section data, and target-scale torsion. The next research objective is
an executable exact-identification certificate; another analytic bound
alone would not complete it. The intended first polynomial has degree
257 over F, followed by normal closure over Q. Read
[the D100 review](dembele/certificates/construction-methodology-d100.md)
and [the handoff](HANDOFF.md). No new arithmetic computation was run;
the target field polynomial remains unconstructed.

**Previous checkpoint (D99):** a fresh review establishes geometric
nonhyperellipticity of the intended genus-16 quotient. A new arithmetic
graph computation and an elementary edge-cut obstruction support the
conclusion independently of numerical differentials. The published
hyperellipticity proof has an invalid local-coordinate inference.
Our exact candidate is also nonhyperelliptic, but remains unidentified
with the intended curve. Read [the D99 review](dembele/certificates/hyperellipticity-review-d99.md)
and [the handoff](HANDOFF.md). The root audit passes; the CM anchor and
target field remain unconstructed.

**Previous checkpoint (D98):** a proved spectral comparison
retains cancellation within each complete Hecke family and improves
the omitted-ideal error bound by more than 272 times, to <2.479e10.
The full interval still contains zero, so the CM anchor remains
uncertified. The independent audit passes. Next evaluate the completed
spectral multiplier before taking absolute values; a larger enumeration
is still unjustified. Read [the D98 proof and pilot](dembele/certificates/nelson-spectral-ideal-d98.md)
and [the handoff](HANDOFF.md). The target field remains unconstructed.

**Previous checkpoint (D97):** exact shell grouping and partial
summation certify cancellation in the saved quaternion data, improving
the outer-block bounds by factors >6.45 and >8.16. A new calculation
quantifies the infinite remainder that a uniform signed counting bound
would provide, but that bound remains unproved. The actual global error
is unchanged and the CM anchor is uncertified. Next establish explicit
angular-counting or signed Hecke-block estimates before more enumeration.
Read [the D97 report](dembele/certificates/nelson-signed-orbit-d97.md)
and [the handoff](HANDOFF.md). The independent audit passes; the CM
tangent and target field remain unconstructed.

**Previous checkpoint (D96):** the completed-kernel summation
pilot improves the rigorous omitted-ideal bound by a factor of about
four, to <6.754e12. It remains about 884 million times the current
partial sum, so the pilot does not justify expanding enumeration.
The remaining loss is in the positive orbital and Hecke comparison;
quadrature and far-tail errors are negligible. Next investigate a
bound retaining signed arithmetic cancellation. Read
[the D96 report](dembele/certificates/nelson-completed-majorant-d96.md)
and [the handoff](HANDOFF.md). Decisions and references are updated;
the CM tangent and target field remain unconstructed.

**Previous checkpoint (D95):** the full theta/Mellin expression
is now identified with the intended Shimizu derivative pairing, up to
a positive common scalar. The proof also fixes the conjugation needed
when recovering differential ratios. Numerical error bounds remain
too wide to certify a CM tangent. Next improve global summation accuracy
before extending the computation. Read
[the D95 proof](dembele/certificates/nelson-global-identification-d95.md)
and [the handoff](HANDOFF.md). Decisions and references are updated;
the target field remains unconstructed.

**Previous checkpoint (D94):** the global review improves the
rigorous omitted-ideal bound by about a factor of 1000, but it remains
too loose to certify a CM value. A new local calculation proves that
our Schwartz factors have nonzero norm-one contractions. Matching
these to the implemented global kernel is the next proof step; more
enumeration is paused pending a useful error bound. Read
[the D94 report](dembele/certificates/nelson-test-vector-and-contour-d94.md)
and [the handoff](HANDOFF.md). Decisions and references are updated;
the CM tangent and target field remain unconstructed.

**Previous checkpoint (D93):** the norm-31 family is now
controlled: 586 classes, 32 exact norm-one orbits, and a weighted
infinite-family bound using saved Hecke data. A bound for all other
norm ideals proves convergence but is far too loose for a CM tangent.
Next review the global summation and lift identification before more
enumeration. An interval-export correction has been replayed through
the analytic chain; use the corrected artifacts in
[the D93 report](dembele/certificates/nelson-prime31-and-global-tail-d93.md)
and [the handoff](HANDOFF.md). Decisions and references are updated;
the target field remains unconstructed.

**Previous checkpoint (D92):** the norm-one control now has a
complete enumeration of 541 classes through displacement parameter
A=25600 and a bound on the entire omitted norm-one tail. Its first
derivative-kernel subsum is proved positive. Other norm ideals and
the global lift identification remain; no CM tangent or target field
has been constructed. Next extend the search to the norm-31 prime
with saved Hecke data. Read [the D92 report](dembele/certificates/nelson-norm-one-control-d92.md)
and [the handoff](HANDOFF.md). Decisions and references are updated.

**Previous checkpoint (D91):** the Hilbert theta-sum implementation
now has exact cusp and central-unit identities and certified partial
sums for 29 primitive quaternion classes. Missing Hecke coefficients
and omitted classes prevent a complete eigenform or CM-tangent
evaluation. A first complete cutoff is too large for direct enumeration;
the next step is enumeration by norm ideal and hyperbolic displacement.
Read [the D91 report](dembele/certificates/nelson-hilbert-unfolding-d91.md)
and [the handoff](HANDOFF.md). Decisions and references are updated.
The target field remains unconstructed.

**Previous checkpoint (D90):** local components of an independent
Shimizu evaluator are implemented: the Fourier normalization at 2,
derivative kernels, the actual CM lattice decomposition, and a scalar
Mellin prototype calibrated against Nelson's rational formula. The
global Hilbert theta lift and arithmetic CM tangent remain uncomputed.
Next assemble the cusp/unit unfolding and evaluate one Hecke eigenform
with a truncation bound. Read [the implementation report](dembele/certificates/nelson-totally-real-kernel-d90.md)
and [the handoff](HANDOFF.md). Decisions and references are updated;
the target field remains unconstructed.

**Previous checkpoint (D89):** the independent arithmetic CM
tangent remains uncomputed. Exact local calculations now specify the
order-two quotient and show that the Hecke equations introduce unknown
derivatives at additional CM points. The missing input is a global
section evaluator; the known CM orbit and Hecke matrix do not already
supply it. Read [the local arithmetic report](dembele/certificates/cm-tangent-local-arithmetic-d89.md)
and [the handoff](HANDOFF.md). Prior curve and lift certificates remain
unchanged; the target field remains unconstructed.

**Previous checkpoint (D88):** two independent reviews clarify the
identification problem. The expansion paper gives a short certificate
for the base once independent exact CM jets are available; those jets
are still missing. The cubic uniqueness shortcut is sound conditionally
on identifying the marked arithmetic base and double cover. Under that
condition, the existing nine-cover calculation selects our cubic.
Read [the expansion review](dembele/certificates/d88-cm-expansion-identification-review.md),
[the shortcut review](dembele/certificates/d88-cubic-identification-shortcut-review.md),
and [the handoff](HANDOFF.md). Further precision remains paused, and the
target field remains unconstructed.

**Previous checkpoint (D87):** the genus-40 double-cover candidate
matches the exact Fuchsian S3 sign character on all **277 generators**
in both saved differential expansions and along a second family of paths.
This is numerical evidence for the geometric cover choice; arithmetic
identification remains open. The existing B3 fibre certificate selects
the scalar twist within that choice. Next address the marked base and
selected cubic class, with further precision still paused. See
[the character comparison](dembele/certificates/cm-frame-double-cover-character.md)
and [the handoff](HANDOFF.md). The target field remains unconstructed.

**Previous checkpoint (D86):** the Châtelet run completes the
actual cubic lift and independent verification through **31^128**.
Both models preserve their 64-digit coefficients and reject all tested
highest-digit corruptions. Joint F recognition with 112 training / 16
validation digits finds no surviving candidate in any of the eight
embeddings. Exact integer certificates exclude homogeneous coordinate
height through **348,750,355,384,078** in the specified bases; this does
not exclude F. The target field is still unconstructed. Next pursue the
marked arithmetic comparison and global Galois action on the selected
cover, with no automatic further precision increase. Read
[the completed run](dembele/certificates/cm-frame-cubic-128-chatelet.md)
and [the descent review](dembele/certificates/cm-frame-cubic-128-review.md).

**Previous checkpoint (D84):** structural checks distinguish the
selected genus-64 cover among nine actual alternatives: only the current
third matches the predicted point counts 68 / 2,818. The subgroup of
alternatives is verified, but is not proved exhaustive. Recognition
calibration on 67 known F-points shows recovery of examples with coefficient
height 10^9 at 64 digits and 10^18 at synthetic 128-digit precision.
These are empirical results, not target height bounds. At that checkpoint the cubic
ell*T^3-3*A2*ell*T-R4=0 was independently verified through 31^64;
its exact coefficients over a number field are not recovered. The checks
supported the bounded 128-digit experiment reported above. Arithmetic identification,
the characteristic-zero cubic and field polynomial remain open.
Start
with [HANDOFF.md](HANDOFF.md), the
[cover-choice and recognition checkpoint](dembele/certificates/cm-frame-structural-checkpoint.md), the
[64-digit lift and reconstruction report](dembele/certificates/cm-frame-cubic-64.md), the
[pointed normalization and precision report](dembele/certificates/cm-frame-cubic-precision.md), the
[first cubic lift](dembele/certificates/cm-frame-cubic-lift.md), the
[two genus-64 Frobenius comparisons](dembele/certificates/cm-frame-cubic-frobenius.md), the
[explicit genus-64 cubic](dembele/certificates/cm-frame-cubic-cover.md), the
[verified branch-class division](dembele/certificates/cm-frame-cover-class-arithmetic.md), the
[normalized B3 fibre and cubic-input certificate](dembele/certificates/cm-frame-B3-fiber.md), the
[rational double-cover certificate](dembele/certificates/cm-frame-rational-double-cover.md), the
[joint recognition and B3 normalization report](dembele/certificates/cm-frame-joint-field-and-B3-normalization.md), the
[precision-doubling and recognition report](dembele/certificates/cm-frame-precision-doubling.md), the
[normalization certificate](dembele/certificates/cm-frame-normalization.md), the
[31-adic lifting certificate](dembele/certificates/cm-frame-resolvent-lift.md), the
[finite-field double-cover certificate](dembele/certificates/cm-frame-resolvent.md), the
[marked branch-divisor report](dembele/certificates/cm-frame-marks.md), the
[smoothness proof and arithmetic comparison](dembele/certificates/cm-frame-verification.md), the
[candidate curve and source review](dembele/certificates/curve-construction-sources-2026-09-18.md), the
[allocation audit](dembele/certificates/lifttors-allocation.md), the
[degree-51 and reduction report](dembele/certificates/lifttors-degree51.md), the
[native implementation report](dembele/certificates/lifttors-rows.md), the
[extension calibration](dembele/certificates/lifttors-extension.md), the
[memory audit](dembele/certificates/lifttors-memory.md), the
[geometry audit](dembele/certificates/curve-identification-audit.md),
[backend results](dembele/certificates/lifttors-control.md),
[section interface](dembele/certificates/arithmetic-section-interface.md), the
[stocktake](dembele/certificates/stocktake-2026-09-16.md), the
[evaluation-space height report](dembele/certificates/cm-flag-height.md), the
[CM orbit and reconstruction report](dembele/certificates/cm-orbit-recognition.md), the
[marked descent report](dembele/certificates/marked-descent.md), the
[arithmetic-input audit](dembele/certificates/cm-arithmetic-input-audit.md),
and the [function construction](dembele/certificates/cm-pointed-maps.md).

## The target

Let

\[
F=\mathbf Q(\zeta_{32})^+
  =\mathbf Q(\beta),\qquad
\beta^8-8\beta^6+20\beta^4-16\beta^2+2=0.
\]

Dembélé computed two eight-dimensional irreducible constituents of the space
\(S_2(1,\mathbf F_2)\) of mod-\(2\) Hilbert cusp forms over \(F\). Their Hecke eigensystems
give surjective representations

\[
\bar\rho_f,\bar\rho_{f'}:
\operatorname{Gal}(\overline F/F)\longrightarrow
\operatorname{SL}_2(\mathbf F_{2^8}).
\]

If \(E\) and \(E'\) are the fixed fields of their kernels, then \(E\) and \(E'\) are
linearly disjoint over \(F\), and

\[
K=EE'
\]

is Galois over \(\mathbf Q\), ramified only at \(2\), and fits into

\[
1\longrightarrow
\operatorname{SL}_2(\mathbf F_{256})^2
\longrightarrow \operatorname{Gal}(K/\mathbf Q)
\longrightarrow C_8
\longrightarrow 1.
\]

In particular,

\[
[K:\mathbf Q]
=2^{19}(3\cdot5\cdot17\cdot257)^2
=2\,251\,731\,094\,732\,800.
\]

The desired output is not a power basis for this enormous Galois field. It is a manageable
polynomial over \(\mathbf Q\) whose splitting field is \(K\), together with reproducible
certificates of its Galois group and ramification. A natural first target is a degree-\(257\)
polynomial over \(F\): the projective-line action of
\(\operatorname{SL}_2(\mathbf F_{256})\) has degree \(257\), so such a polynomial can have
splitting field \(E/F\). Its Galois conjugates can then be combined and descended to
\(\mathbf Q\).

## Research program

### 1. Reproduce Dembélé's computation

- Construct \(F\), its ring of integers, and the action of
  \(\operatorname{Gal}(F/\mathbf Q)\).
- Recompute \(S_2(1,\mathbf F_2)\) and its Hecke algebra.
- Recover the two eight-dimensional eigensystems \(f,f'\).
- Match Dembélé's traces and Frobenius orders at the primes above \(31\) and \(97\).
- Record exact, machine-readable Hecke data rather than only the published table.

This phase is complete, using quaternionic modular forms in Magma.

The Magma package
[`edgarcosta/hilbertmodularforms`](https://github.com/edgarcosta/hilbertmodularforms)
is now pinned and validated for this computation. Its integral raw Brandt matrices
reproduce the 58-dimensional raw module, the 57-dimensional cuspidal module, both published
mod-\(2\) characteristic polynomials, and every trace and Frobenius order in Dembélé's
table.

### 2. Determine which constructive route is available

The method of
[van Bommel–Costa–Elkies–Keller–Schiavone–Voight](https://arxiv.org/abs/2411.07857)
turns a characteristic-zero Hilbert newform into a period matrix and then an explicit
isogeny polynomial. The lift decision has now been resolved positively: the two mod-\(2\)
systems are reductions of the unique 16-dimensional characteristic-zero component at the
two unramified residue-degree-8 primes above \(2\) in its Hecke field. The integral Hecke
generator is already \(2\)-maximal, and its defining polynomial modulo \(2\) factors as
exactly Dembélé's two degree-8 polynomials. See
`dembele/certificates/lift-report.md`.

Subsequent period and torsion feasibility investigations are recorded in
[DECISIONS.md](DECISIONS.md). The current curve route has a conditional
realization of the original residual systems in the Jacobian of a genus-64
cover; see [target-realization.md](dembele/certificates/target-realization.md).
There are now exact rational models of a genus-16 base candidate and its
genus-40 double cover, plus a verified genus-64 cubic over F31 lifted
through 31^128. The curve models still require arithmetic identification
before the representation argument applies to their Jacobians.

D84 tests the choice of cubic against eight alternatives and calibrates
the coefficient reconstruction method. D86 completes the 128-digit lift,
but recognition over F remains negative; next address marked arithmetic
identification and the selected class's global action. The remaining
route is an exact, identified
arithmetic genus-64 curve, followed by target 2-torsion, a degree-257
polynomial over F, and certification of its required normal closure.

### 3. Construct and descend the field

- Construct a polynomial over \(F\) whose splitting field is \(E\).
- Apply the \(C_8=\operatorname{Gal}(F/\mathbf Q)\) action explicitly.
- Recover \(E'\) as the appropriate conjugate and form \(K=EE'\).
- Descend to a polynomial over \(\mathbf Q\), initially without optimizing its degree or
  coefficient size.
- Search afterward for smaller subfields, better invariants, and reduced polynomials.

### 4. Certify the result

An explicit candidate is complete only after exact verification:

- its splitting field is unramified away from \(2\);
- its residual Frobenius traces agree with the two published eigensystems;
- each geometric image is \(\operatorname{SL}_2(\mathbf F_{256})\);
- the two fields are linearly disjoint over \(F\);
- the normal closure over \(\mathbf Q\) has the required extension by \(C_8\).

Numerical period calculations may be used to discover the polynomial, but the final
identification must use exact arithmetic.

## Current repository

- `dembele/` — current computation: pinned dependencies, machine-readable published data,
  exact Magma certificates, tests, and eventual defining polynomials.
- `remote_magma/` — tested client and operational documentation for running Magma V2.29-10
  on chatelet through the CoCalc API.
- `nonsolvable_at_2_examples.md` — preliminary comparison with other explicit
  nonsolvable fields.
- `writeup/` — results and remaining gap from the 2-group Belyi-map investigation.
- `belyi/`, `belyi_jl/` — Sage and Julia/Hecke experiments for constructing Belyi curves.
- `torsion_module.sage`, `torsion_fast.sage`, `torsion_shard.sage` — mod-\(2\) Jacobian
  module and centralizer computations.
- `aristotle_solvable/` — Lean formalization of the algebraic solvability lemma.
- `HANDOFF.md`, `CLAUDE.md` — current resumption instructions and environment notes.
- `DECISIONS.md`, `REFERENCES.md` — research decisions and source attributions.
- `NOTES.md` — earlier working notes.

New Hilbert-modular computations should be added in a separate top-level directory so
that the original Belyi-map investigation remains reproducible.

## References

1. L. Dembélé,
   [*A non-solvable Galois extension of \(\mathbf Q\) ramified at 2 only*](https://arxiv.org/abs/0811.4379),
   C. R. Math. Acad. Sci. Paris **347** (2009), 111–116.
2. J.-P. Serre,
   [*Un complément à la Note de Lassina Dembélé*](https://doi.org/10.1016/j.crma.2008.12.006),
   C. R. Math. Acad. Sci. Paris **347** (2009), 117–118.
3. R. van Bommel, E. Costa, N. D. Elkies, T. Keller, S. Schiavone, and J. Voight,
   [*The constructive inverse Galois problem via Hilbert modular forms: realizing the
   transitive group 17T7*](https://arxiv.org/abs/2411.07857).
4. M. Musty, *2-Group Belyi Maps*, Ph.D. thesis, Dartmouth College, 2019.

## Secrets

API keys and other credentials belong in the gitignored `.env` file at the repository
root and must never be committed. For Aristotle, the expected variable is
`ARISTOTLE_API_KEY`.
