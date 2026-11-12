# References and attributions

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

D148 reuses [Bertram's Clifford equality criterion](https://www.math.utah.edu/~bertram/6180/Special.pdf)
to bound the degree-four line 2D-K. D102 supplies the trace-dual lattice,
D103/D106 the actual rational residue construction, D116 the integral
leading jets and dyadic cofactor contents, D117 the uniform disks,
D118 the height endpoints, and D140/D142 the actual jet rank. The joint
filtered degree and exterior-frame inequalities are derived in the new
report. No Mumford isometry or spectral n=2 substitution is used.


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

D147 uses [Freixas i Montplet, Theorem 4.5 and Lemma 4.6](https://arxiv.org/pdf/0803.2366v1)
for the algebraic unpointed stable-curve Mumford isomorphism, with its
metric discrepancy retained. [Teo, sections 5--6](https://www.imath.kiev.ua/~sigma/2021/083/sigma21-083.pdf)
concerns orbifold n-differentials; the rank-72/rank-45 distinction prevents
a direct substitution. The stable-fibre multiplication proof, determinant
metric bookkeeping, residue-frame comparison and local pole calculation
are derived in the companion report, not claimed as published isometries.


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

D146 uses [Yuan, Proposition 4.1 and its proof](https://arxiv.org/pdf/2205.13995v3)
for the smooth quotient and local stabilizer framework, and
[Stacks, 49.12.5--49.12.6](https://stacks.math.columbia.edu/tag/0BWB)
for the two descriptions of the different. The extension to the
normalizer, tame separation, C3/S3 classification, fixed-section
estimate and weighted intersection bounds are our companion
derivations. No explicit CM lift or coordinate formula is assumed.

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

D145 uses [Garbin--Jorgenson, equations (2.7)--(2.8)](https://www.jstage.jst.go.jp/article/kodaimath/43/1/43_84/_pdf)
for the positive compact heat trace and
[Blomer--Brumley, Definition 1 and Theorem 1](https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p18-p.pdf)
at the split real place after Jacquet--Langlands transfer.
The trace normalization, uniformity over conjugates, two-time
inequality, elementary tails and regularized Zprime formula are
our derivations, with applicability arguments in the report.
PDF fingerprints are retained in the ledger.

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

D144 uses the [final author Freixas--von Pippich PDF](https://perso.pages.math.cnrs.fr/users/gerard.freixas/articles/freixas-pippich-JEMS.pdf),
[Kalvin's corrected cone determinant](https://arxiv.org/pdf/2011.05407v1),
and [Teo's independent spectral constant](https://www.imath.kiev.ua/~sigma/2021/083/sigma21-083.pdf).
The ledger pins downloaded hashes and exact formula locations. The
compact proof rederives the boundary anomaly and the sign obtained by
solving the truncated Deligne pairing identity. The final author
spectral formula has denominator m, unlike the older arXiv v2 formula.
Neither the printed collected constant nor a cone-only repair is used.
D143's CM theorem applicability and Zhao normalization caveat persist.

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

D143 adds the specific applicability checks for
[Yuan, Theorem 1.2 and Proposition 4.1](https://arxiv.org/pdf/2205.13995v3)
and [Zhao, Theorem 7.4](https://arxiv.org/pdf/2309.08886v1).
The former applies to E_3; the latter applies to the common dyadic
ramification of E_32. The ledger records downloaded hashes, the inherited
D104 normalization reconciliation, stable-map and quotient inputs, and
the distinction between finite checks and the report's geometric proof.

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

D142 adds [Bertram's strict Clifford equality case](https://www.math.utah.edu/~bertram/6180/Special.pdf)
for the rank bound through first jets. The new ledger records the exact
RR and cone-paper versions, downloaded-file hashes, metric locations and
the modular-height normalization. The report distinguishes the locally
checked correction from any claim about the complete global theorem.

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

D141 source applicability: the bound report and ledger above record exact
locations and distinguish sourced statements from local deductions.

- [LLL, section 1](https://ir.cwi.nl/pub/9304/9304D.pdf):
  Gram--Schmidt background; D141 derives the outside-space exterior criterion.
- [de Jong--Shokrieh, Theorem A and (1.11)](https://arxiv.org/pdf/1810.02637):
  the relevant Faltings invariant, with positive contributions still unestimated.
- [Yuan, v3, section 1.1 and Theorem 1.1](https://arxiv.org/pdf/2205.13995v3):
  modular Hodge self-intersection requires a proved comparison to Faltings height.
- [Freixas i Montplet--von Pippich, v2, sections 1 and 10](https://arxiv.org/pdf/1604.00284v2):
  a possible orbifold Riemann--Roch comparison, with additional required terms.
- [Kalvin, v1, Corollary 1.2 and Remark 3.2](https://arxiv.org/pdf/2011.05407v1):
  reconcile the model-cone determinant correction before numerical use.

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

**Operational update (2026-10-05):** D133 resumed after verification of the
September 30 transfer inventory and all external dependency hashes. The
[preflight record](dembele/checkpoints/d133-resume-2026-10-05-preflight.json)
and [resumption record](dembele/checkpoints/d133-resume-2026-10-05.json)
record execution provenance, without a new mathematical certificate.
See [HANDOFF.md](HANDOFF.md) for the active production/continuation chain.

- **Git LFS / GitHub documentation**, [About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).
  **Role: repository transfer infrastructure, 2026-09-30.** Git LFS preserves
  the computed binary payloads and seven large JSON files listed in
  `.gitattributes`. Git LFS 3.8.0 was installed locally for the transfer.
  `scripts/verify_transfer.py` checks a relative-path SHA-256 inventory after
  retrieval; this is transfer integrity, not a mathematical certificate.
  See [CHECKPOINT.md](CHECKPOINT.md).

- **Erin Carson and Nicholas J. Higham**, *Accelerating the Solution of
  Linear Systems by Iterative Refinement in Three Precisions*, SIAM J.
  Scientific Computing (2018), [author manuscript](https://eprints.maths.manchester.ac.uk/2629/1/cahi18.pdf).
  **[numerical method, D48]** High-precision residuals and accumulated
  solutions with lower-precision correction solves. Script 78 tests the
  mechanism on a small actual Cauchy operator; full-size convergence and
  differential truncation remain separate questions.

A running ledger of the papers, people, and software this project pulls from,
with *how each is used* — maintained alongside `DECISIONS.md` so that any
eventual writeup can cite accurately and generously. Conventions: role tags are
**[target]** (defines the problem), **[method]** (we execute or adapt their
technique), **[theory]** (results we invoke), **[tool]** (software we run),
**[context]** (orientation/verification). Repo pointers say where the use
happens.

**Latest reviewed execution: D132 complete resumable staged integration, 2026-09-28.**

See the [report](dembele/certificates/dyadic-staged-integration-d132.md),
[ledger](dembele/data/computed/dyadic_staged_integration_sources_d132.json)
and [fixed review](dembele/data/computed/dyadic_staged_integration_review_d132.json).
All 471 inputs and both reviews pass. Review 555 binds 18589 hashes,
preserving all 16567 D131 hashes. Freeze 547--555 and bound controls.

**[inherited theory, complete implementation control]** D121's coefficient
valuation and fixed-mass contraction, and D130's weighted fixed-point
argument, justify direct weighted seeding and final verification. D123's
complete P800 column, D129's CM output and D130's complete synthetic
1319-bit low answer supply exact finite references. Sources 547--554
implement resumable phases and receipt-verified metadata archival. Source
555 independently checks complete retained comparisons plus sampled
ordinary recurrences from source 486. The production arithmetic of 554
is unchanged from controlled 548; only prior-review provenance and identity
differ. FLINT/GMP and prior-factor attributions remain inherited.

**[implementation evidence, limited scope]** Eight interrupted children
recover; this is not a power-loss/hardware guarantee. Complete working-file
inventories fit 2 GiB with archival, while measured RAM admission is
separate from OS enforcement. No new external theorem or fresh external
source verification is invoked. D132 leaves mathematical precision
unchanged and admits one actual P6400 column, now executing as D133.
The long bank and downstream arithmetic cover/section construction remain
open. Earlier next-task statements below are historical.

**[D133 execution in progress]** The
[initialization pause](dembele/data/computed/dyadic_staged_P6400_col00_pause_d133.json)
records 176 passing phases; the resumed coordinator has passed the seed
low system through 800 bits. Draft source 556 uses source 486's ordinary
integer quotient for independent recurrence samples and Horner checks of
the coarse sums, with complete comparisons to the frozen P3200 references.
Draft source 557 specifies full phase/generation and provenance coverage.
The [24-job audit plan](dembele/data/computed/dyadic_precision6400_audit_plan_d133.json)
runs only after completion and sealing. These drafts are unexecuted and
provide no new certified precision yet; no fresh external reference is used.

**[D133 continuation controls]** The
[completion coordinator](dembele/pari/run_d133_completion.py) waits on the
production lock and completed sealed result before admitting the 24 audits,
D133 review/replay and D134 replay/review. Its
[six operational controls](dembele/data/computed/dyadic_continuation_controls_d133.json)
check locks, failure stops, receipt authentication, document links and
immutable artifacts in temporary fixtures. They launch no mathematical
driver and do not certify the pending arithmetic. All prior caps remain.

**[session-close observation, 2026-09-29 11:34:55 UTC]** The
[snapshot](dembele/data/computed/dyadic_close_session_snapshot_d133_20260929.json)
records eight committed corrections, 2,493 receipts reporting pass and
both coordinator locks held. It binds the latest committed sweep evidence,
the earlier pause record and continuation controls. Its current-state
fields become historical as execution advances; it is not an arithmetic
certificate or evidence that processes survive session closure. The
[handoff](HANDOFF.md) gives the exact completion filenames, lock checks
and restart ordering. No new external reference or mathematical claim is
introduced by this documentation checkpoint.

**[D134 conditional cover criterion, unexecuted replay drafts]** The
[revised note](dembele/certificates/arithmetic-twist-classification-d134.md)
restores [D77's exact fibre/inertia condition](dembele/certificates/cm-frame-B3-fiber.md),
already retained in D87/D88. It fixes the F-scalar twist once the half
and the B3 marking are identified. The odd value P16(32), used only for
candidate discovery in D71, supplies a further conditional deduction:
after arithmetic base identification and the canonical Hecke interpretation,
good reduction rules out F-rational Jacobian 2-torsion and makes the
arithmetic branch half unique. Candidate point-count agreement alone is
insufficient. The D130 local-twist witness remains correct but does not
preserve the stronger B3 inertia condition.

**[primary theory, freshly checked 2026-09-29]**
[Stacks tag 09EE](https://stacks.math.columbia.edu/tag/09EE) supplies the
faithful tame inertia character in characteristic zero.
[Tag 0BFH](https://stacks.math.columbia.edu/tag/0BFH) and
[tag 03RP](https://stacks.math.columbia.edu/tag/03RP) supply étaleness of
multiplication by an invertible integer and the finite torsion group
scheme. The specialization and branch-half deductions are ours; the
sources do not identify the candidate. Drafts 558/559 check the exact
D77 witness and Hecke polynomial arithmetic by separate methods. Their
D77 input chain will be merged separately from the dyadic catalogue.
No new marked base, cover, Y section model or field polynomial is claimed.

**Previous execution: D131 weighted certificate and recoverable arithmetic, 2026-09-28.**

See the [report](dembele/certificates/dyadic-weighted-journal-d131.md),
[ledger](dembele/data/computed/dyadic_weighted_journal_sources_d131.json),
[fixed review](dembele/data/computed/dyadic_weighted_journal_review_d131.json)
and [completion record](dembele/data/computed/dyadic_weighted_journal_completion_d131.json).
Sources 541--546 supply complete weighted replay, streaming and per-row
authentication, a row journal, interruption/corruption controls, a fresh
known correction and independent review. All 54 input jobs and both
reviews pass. Review 546 binds 16567 hashes, preserving all 16142 D130
hashes. Actual precisions and mathematical identification status are unchanged.

**[inherited theory, new implementation]**
[D121](dembele/certificates/dyadic-schur-lift-d121.md) supplies the original
column-k valuation bound and fixed-mass contraction;
[D130](dembele/certificates/dyadic-target-feasibility-d130.md) supplies
the weighted deduction T Q=T and Q T(w)=w. The complete reference is
[D129](dembele/certificates/dyadic-precision3200-d129.md), whose source 530
already evaluated CM directly from weighted moments. D131 changes
authentication and replays with GMP; it does not introduce the first
weighted CM method. The new arithmetic/storage integration recomputes
the first correction from [D124](dembele/certificates/dyadic-precision1600-d124.md).
FLINT/GMP and existing-factor attributions remain inherited. The ordinary
integer-quotient audits are sampled independently of production arithmetic.
No new external theorem or fresh external-source verification is invoked.

**[local implementation evidence]** Nineteen distinct process-interruption
boundaries and four corruption/stale-journal cases pass. These controls
do not prove power-loss or hardware durability. Target logical reservations
fit the per-store cap; complete target phase lifetimes and concurrent RAM
remain to be integrated. D130's runtime model is the pre-redesign baseline,
not an updated ETA. Next complete the resumable staged driver using source
547 onward. The marked-cover, arithmetic-twist and Y-section obligations
in D130 remain open. All earlier next-task statements below are historical.

**Previous execution: D130 target feasibility and arithmetic bridge, 2026-09-28.**

See the [feasibility report](dembele/certificates/dyadic-target-feasibility-d130.md),
[construction specification](dembele/certificates/arithmetic-construction-d130.md),
[ledger](dembele/data/computed/dyadic_target_feasibility_sources_d130.json) and
[fixed review](dembele/data/computed/dyadic_target_feasibility_review_d130.json).
Sources 533--540 supply target map/low/CM/frame/quadric controls, compact
retention, streaming authentication, independent audits and an empirical
phase model. All 137 input jobs and both reviews pass; one budget-script
failure is preserved and resolved. Review 540 binds 16142 hashes and
preserves all 15600 D129 hashes. Synthetic controls do not increase the
actual bank's precision. Runtime scenarios are not bounds or an ETA.

**[inherited operator theory, new elementary deduction]** D121's expansion
of a contracting fractional-linear map gives column-k valuation at least k.
Hence T Q=T modulo pi^P for the weighted projection, and Q T(w)=w implies
that T(w) is a full fixed point. The reviewer checks the required original
and composed-CM parameter divisibilities independently; a new weighted-only
production replay remains to be implemented. FLINT/GMP and existing-factor
attribution remain inherited. Byte inventories are exact but the proposed
row-journal layout is not yet a resource certificate.

**[primary theory, checked 2026-09-28]**
[Stacks Project, Kummer theory, tag 03PK](https://stacks.math.columbia.edu/tag/03PK),
particularly the invertible-n Kummer sequence and the classification using
a line bundle with a trivialized nth power, separates a geometric cover
from its scalar arithmetic twist. **[our exact deduction]** Source 538 and
independent review 540 check Norm_F/Q(1+b)=-1 and 1+b=28=20^2 at the chosen
b=27 mod31 place. Hensel lifting and the unit discriminant away from 2
show that this globally nontrivial quadratic twist is locally invisible
there. This does not identify or disprove the candidate twist. The marked
arithmetic-X hypothesis of D88 and the D62 Y-section interface remain open.

Next implement weighted-only D129 replay and the bounded row-journal
protocol, while keeping the arithmetic cover construction on the research
path. No new precision run, resource cap or field claim follows.

**Previous planning review: stocktake after D129, 2026-09-28.**

The [stocktake](dembele/certificates/stocktake-2026-09-28.md) distinguishes
evaluator scaling from exact geometric identification and the remaining
field construction. **[local synthesis, no new theorem or computation]**
It reviews the saved arguments and specifications; it does not claim a
fresh verification of their external primary sources. D129 remains the
latest completed arithmetic checkpoint.

The proof chain uses [D51](dembele/certificates/target-realization.md)
for the original residual systems in canonical Y64,
[D99](dembele/certificates/hyperellipticity-review-d99.md) for the intended
base's nonhyperellipticity, and
[D116](dembele/certificates/cm-compound-height-d116.md),
[D118](dembele/certificates/cm-finite-height-d118.md) and
[D120](dembele/certificates/construction-reassessment-d120.md) for the
integral-section exactness argument and conditional P=10552 design.
The [D88 expansion criterion](dembele/certificates/d88-cm-expansion-identification-review.md)
explains why exact vanishing on 4D identifies the base. Its remaining
marked-cover obligations are separated in the
[D88 cubic review](dembele/certificates/d88-cubic-identification-shortcut-review.md).

The [D62 section interface](dembele/certificates/arithmetic-section-interface.md),
[D66 degree-51 control](dembele/certificates/lifttors-degree51.md) and
[D67 allocation audit](dembele/certificates/lifttors-allocation.md)
specify the unresolved arithmetic input and combined torsion scaling.
D120 supersedes D100's older open norm-97 cofactor question; global
F256 action and exact field certification remain open. Existing finite
cubic congruences and their height exclusions are not an exact global
model or an upper reconstruction bound.

Next cost the complete identification certificate and controlled future
retention, and specify the downstream construction before a long bank
commitment. No new paper, software attribution or arithmetic source
number is introduced by this planning review.

**Previous execution: D129 actual P=3200 refinement reviewed, 2026-09-28.**

See [report](dembele/certificates/dyadic-precision3200-d129.md),
[ledger](dembele/data/computed/dyadic_precision3200_sources_d129.json) and
[fixed review](dembele/data/computed/dyadic_precision3200_review_d129.json).
Sources 528--529 complete one actual column with streamed serial phases,
reserved file lengths and prospective retirement. The separate original
GMP residual checks every one of 4,454,400 scalar coefficients. Source 530
computes all 17 CM charts in six retained chunks and combines metadata
without duplicating the binary. Source 531 uses separate integer arithmetic
for 22 audit jobs; its ordinary original/CM recurrence checks are samples,
while its retained residual and weighted-coordinate checks are complete.
Review 532 independently replays all 103 allocation/retirement barriers,
binds 15600 source hashes and preserves all 9648 D128 hashes. All 1934
inputs and both capped reviews pass. The complete bank remains P=800.

**[inherited mathematics, finite arithmetic and storage control]** No new
external theorem is invoked. Fixed masses, the original full residual and
the contracting transport/truncation proof certify the final moments
independently of retired iteration history. The weighted proof, integral
low inverse, exact residual lift, direct CM tails and installed FLINT/GMP
attribution remain inherited. Logical scratch reservations do not certify
aggregate RAM or target-size cost; the writer control injects no crash.
The proposed seven-block lift to 1319 binary digits is elementary exact
residual algebra and remains unexecuted at target size. Next cost that
lift and original-map actions, compare precision schedules and control
compact retention before a further complete refinement. Exact curve and
field identification remain open.

**Previous execution: D128 selective serial and P=3200 controls reviewed, 2026-09-28.**

See [report](dembele/certificates/dyadic-selective-scaling-d128.md),
[ledger](dembele/data/computed/dyadic_selective_scaling_sources_d128.json)
and [fixed review](dembele/data/computed/dyadic_selective_scaling_review_d128.json).
Source 525 incrementally serializes and directly compares fourteen actual
D124 payloads, including full reconstruction and selected preparations;
305,582,280 bytes and 133,632 low sparse equations pass. Source 526 checks
P=3200 original-map samples with adaptive and GMP polynomial backends,
using actual old inputs for extension and explicitly synthetic inputs
for full/RHS actions. No new harmonic precision or geometric result is
inferred. Source 527 independently checks inventories/coverage/provenance,
binding 9648 hashes and preserving all 9599 D127 hashes. All 13 input jobs pass.

**[implementation control, inherited mathematics]** No new external theorem
is invoked. Original transports, low inverse, weighted error lattice,
fixed-mass contraction and D127's exact residual lifting remain the
mathematical inputs. FLINT/GMP attribution remains inherited. The proposed
P=3200 scratch inventory is exact layout arithmetic, not an executed
cap or complete runtime bound. Next integrate an actual P=3200 column
using source 528 onward; full-bank/field conclusions remain unchanged.

**Previous execution: D127 rolling refinement and factor reuse reviewed, 2026-09-28.**

See [report](dembele/certificates/dyadic-rolling-pilot-d127.md),
[ledger](dembele/data/computed/dyadic_rolling_sources_d127.json) and
[fixed review](dembele/data/computed/dyadic_rolling_review_d127.json).
Sources 519--522 complete and independently audit a second P=1600
column with prospective scratch retirement and retained final original
residuals. Review 523 binds 9599 sources, preserving all 8816 D126 hashes,
and independently replays all 54 retirement barriers. All 235 input jobs
pass. No exact curve or field identification follows.

**[elementary algebraic deduction and finite control]** Source 524 reuses
a factor modulo 2^m: solve x0, divide the higher-precision residual
b-A*x0 exactly by 2^m, solve the correction with the same factor, and
add 2^m times that correction. Substitution proves the result modulo
2^(2m); all original sparse equations pass at P=1600 and P=3200.
This is a local-ring residual lift, distinct from floating-point error
estimates in the Carson--Higham context above. No new external theorem
is invoked. It does not produce actual P=3200 harmonic data.
D125's fixed-mass contraction remains the basis for final certification
without retained iteration payloads. Installed FLINT/GMP attribution,
all original mathematical inputs and exact-zero prerequisites remain.
Next: selective serial phases and bounded P=3200 transport/RHS controls
using the existing P=1600 factor; source 525 is next unused.

**Previous execution: D126 resource controls reviewed, 2026-09-28.**

See [report](dembele/certificates/dyadic-resource-controls-d126.md),
[ledger](dembele/data/computed/dyadic_resource_controls_sources_d126.json)
and [fixed review](dembele/data/computed/dyadic_resource_controls_review_d126.json).
Source 514 checks complete original P=1600 sweeps with selective reads;
515 controls a new bounded scratch store with expected process exits
and corrupt-payload rollback; 516 controls streamed factor solves and
map reuse; 517 combines these methods on actual harmonic/correction data.
Source 518 independently reviews weighted bytes, row digests, coverage,
scratch records and receipts, preserving all 8729 D125 hashes in 8816
sources. All 22 input jobs pass. The scratch protocol is controlled but
has not yet been integrated in a full arithmetic refinement.
No new external theorem is used. D125's fixed-mass contraction remains
the mathematical basis for discarding prospective scratch history after
successors commit while retaining final original-equation certification.
FLINT/GMP attribution and all prior mathematical sources remain bound.
Next: new source 519 onward for a complete P=1600 column-1 rolling pilot,
with a proven/enforced 512 MiB scratch ceiling before larger work.
The full bank remains P=800; all exact curve/field obligations remain.

**Previous execution: D125 complete P=800 bank and comparison reviewed, 2026-09-28.**

See [report](dembele/certificates/dyadic-precision800-d125.md),
[ledger](dembele/data/computed/dyadic_precision800_sources_d125.json) and
[fixed review](dembele/data/computed/dyadic_precision800_review_d125.json).
Sources 505--507 complete the full P=800 harmonic/CM bank, reusing D123
column 0. Sources 508--510 control 2048-beta ball arithmetic and compute
the residue frame and quadrics. Source 511 independently reviews all
fifteen new columns; 512 reviews the full frame, 6188 quadric coefficients
and sufficient thresholds. All finite enclosures contain zero; no exact
positive vanishing or field polynomial is proved. Section bounds are
4994/4945/4928 against sufficient 25255/25369/25476. W Gaussian remains
valuation 1024, error 2025, uninverted. Source 513 binds 8729 hashes and
1250 passing input receipts, preserving all 3535 D124 hashes.

No new external theorem is invoked. D120's fixed-mass contraction shows
that final residual certification is independent of iteration history;
the report gives the argument and its role in a prospective bounded
scratch protocol. That protocol is not yet implemented. Installed
FLINT/GMP attribution and all earlier mathematical inputs remain bound.
The next control is selective reads of the already certified P=1600 state,
using new source 514 before any larger full-bank refinement.

**Previous execution: D124 actual P=1600 pilot and controls reviewed, 2026-09-28.**

See [the D124 report](dembele/certificates/dyadic-precision1600-d124.md),
[ledger](dembele/data/computed/dyadic_precision1600_sources_d124.json) and
[fixed review](dembele/data/computed/dyadic_precision1600_review_d124.json).
Sources 496--499 certify and independently audit one P=1600 column,
including all CM charts. Source 500 checks direct CM composition from
weighted data at P=800 and 1600. The composition proof is given in the
report and invokes no new external theorem. Sources 501--503 profile and
control compiled small products; installed FLINT 3.6/GMP 6.3 headers and
libraries retain their inherited attribution and hashes. Source 504 binds
3535 sources and all 242 passing input receipts, preserving 2532 prior
hashes. Finite congruences do not prove positive exact vanishing. The next
full-bank comparison is P=800 using source 505 and later new drivers.

**Previous execution: D123 actual P=800 pilot and weighted solver reviewed, 2026-09-27.**
See [the proof and measurements](dembele/certificates/dyadic-staged-pilot-d123.md)
and [the source ledger](dembele/data/computed/dyadic_staged_pilot_sources_d123.json).
One column and all seventeen CM charts reach P=800, with coarse errors
[1632,1648,1632,1664]. The complete bank and quadric bounds remain P=400.

**[inherited theory, new deduction and finite computation]** D120/D121's
pi^k divisibility of the k-th child column implies that T kills the
weighted error lattice v_pi(e_k)>=P-k modulo pi^P. A weighted residual
therefore yields a full-precision fixed point after one original
application. The integral Schur inverse supplies gain r+1 and shrinking
active bands. This deduction is proved in the D123 report; no additional
external theorem is invoked. Sources 492--493 test the coordinate-specific
storage and twelve-step correction loop against the complete uniform
calculation. Exact seed extension, masses, branches and CM error estimates
are inherited from D121/D122.

**[independent arithmetic]** Sources 491 and 494 reuse only source 486's
separate integer quotient implementation. They check ordinary coefficient
recurrences, the high seed tail, alternate CM kernels, all weighted
checkpoint overlaps, exact masses and column-divisibility hypotheses.
Production FLINT/GMP attribution remains as recorded below. No new web
source was needed or consulted for these algebraic deductions.
All 148 input jobs pass; review 495 binds 2532 hashes and preserves all
1884 D122 hashes. No improved global quadric bound, positive exact zero,
curve identification or field polynomial follows. No correspondence.

**Previous execution: D122 comparison and independent review complete, 2026-09-27.**
See [the completed report](dembele/certificates/dyadic-precision400-d122.md)
and [the final ledger](dembele/data/computed/dyadic_precision400_review_sources_d122.json).
All 1088 coarse values and 6188 quadratic coefficients are independently
checked. No certified mismatch is found; no positive exact zero or field
construction is proved. Current section bounds are 4194/4145/4128, anchor
3976/3648/3384 and sufficient non-anchor 25305/25419/25526.

**[inherited theory, new finite arithmetic]** D120's inverse norm -35
persists by Neumann stability under the measured 399-digit overlap.
Source 486 certifies q and the frame change from their residuals without
repeating the production inversion. It uses a separately implemented
integer quotient, absolute-error balls, alternate binomial-series CM
kernels and quadratic gradients/polar forms. A separate atanh series
checks the new anchor-dependent D118 inequalities. W's Gaussian is now
certified nonzero, valuation 1024 with error 1225; no inversion or improved
global ratio-height theorem follows from this calculation. D121, D112,
D115/D111 and D116/D118 supply the remaining inputs described in the ledger.
All 167 input receipts pass; review 487 binds 1884 sources, preserving
the 1079 D121 hashes and 1844 interim hashes. The FLINT/GMP attributions
below remain unchanged.

**[operational context, not mathematical input]** Official OpenAI
[recovery guidance](https://learn.chatgpt.com/docs/reference/troubleshooting),
[resume commands](https://learn.chatgpt.com/docs/developer-commands),
[stream retry configuration](https://learn.chatgpt.com/docs/config-file/config-reference)
and [provider configuration limits](https://learn.chatgpt.com/docs/config-file/config-advanced)
were opened for the user's disconnect question. The installed Codex
0.154.0 native executable's `resume --help` confirms `--last`. The documented
SSE retry default is five; provider configuration applies to custom
providers, and built-in provider IDs cannot be overridden. No setting
was changed, no cause was diagnosed and no retry daemon was installed.


**Previous interim execution: D122 complete P=400 bank; comparison and audit pending, 2026-09-27.**
See [the progress checkpoint](dembele/certificates/dyadic-precision400-progress-d122.md)
and [the source ledger](dembele/data/computed/dyadic_precision400_sources_d122.json).
All sixteen actual harmonic columns and seventeen CM charts reach P=400;
the four coarse coefficients have beta-errors [832,848,832,864]. The
algebraic CM frame eta reaches 21168 beta-digits on the original root
branches. This is separate from harmonic moment precision.

**[tool] FLINT 3.6.0**, installed public `fmpz_mod_poly.h` and library,
inspected and hashed in source 477. Source 476 uses `fmpz_mod_poly_mullow`
for fifteen scalar polynomial products and reuses D121's integer Newton
interpolation with eleven guard bits. The
[arbitrary-integer documentation](https://raw.githubusercontent.com/flintlib/flint/v3.6.0/doc/source/fmpz.rst)
attribution is inherited from D121; no new polynomial web documentation
is claimed to have been read. **[tool] GNU MP 6.3.0**, inherited
[import/export interface](https://gmplib.org/manual/Integer-Import-and-Export),
supplies controls and the separate older polynomial backend used for
each new column's final full original residual.

**[inherited method and new computations]** D121 supplies the Schur
iteration, low factor, refined transports and audited column 0. D112
supplies root labels and the fixed rational CM residue basis; D115
supplies old overlaps and exact masses. Sources 478--482 complete the
remaining columns, control arbitrary-integer beta balls, refine eta and
consolidate the bank. D116/D118 supply the unchanged quadratic-section
interface and height budget; D120 supplies the conditional P=10552 target.

All 155 computation jobs pass. Source 485 binds 1844 source hashes,
preserving all 1079 D121 hashes; checkpoint creation and hash replay pass.
It checks provenance and completion, **not an independent mathematical
audit**. Draft sources 483--484 have not run, and independent D122 review
is pending. No improved quadric bound, positive exact zero, candidate
identification or field polynomial is claimed. No correspondence.


**Previous execution: D121 Schur solver and actual precision lift, 2026-09-27.**
See [the proof and result](dembele/certificates/dyadic-schur-lift-d121.md)
and [the source ledger](dembele/data/computed/dyadic_schur_sources_d121.json).
One actual harmonic column reaches P=400, including seventeen CM charts
and four coarse coefficients. All transport parameters reach P=10552;
the complete sixteen-column bank remains at P=200.

**[tool] FLINT 3.6.0**, [public arbitrary-integer documentation](https://raw.githubusercontent.com/flintlib/flint/v3.6.0/doc/source/fmpz.rst).
Installed public modular-matrix headers and library were also inspected
and hashed. The modular-matrix web documentation returned 403. Sources
469--470 use fifteen modular matrix products; integer Newton interpolation
with eleven guard bits is derived and independently checked here. The
new normalization uses the existing D109 Hensel branch; its cross-product
verification is independent of the production division algorithm.

**[method and new deductions]** Integral low-moment elimination yields
Schur gain r+1; the measured r=64 iteration gains 65 digits. D120's
generating function and GMP interface are reused. Review 474 checks
an independent recurrence and alternate CM kernel/Horner evaluation,
binding 1079 sources and preserving all 961 prior hashes. Exact curve
identification and the field polynomial remain open. No correspondence.


**Previous execution: D120 reassessment, precision design and norm-97 isolation, 2026-09-26.**
See [the proof and decision](dembele/certificates/construction-reassessment-d120.md)
and [the source ledger](dembele/data/computed/construction_reassessment_sources_d120.json).
The inverse-frame estimate is rejected; known minors give h_Fal<30.970856,
excluding a Faltings-only rescue. Error propagation
gives conditional sufficient P=10552; actual data remain P=200.

**[tool] GNU MP 6.3.0**, [Integer Import and Export](https://gmplib.org/manual/Integer-Import-and-Export)
and [Integer Arithmetic](https://gmplib.org/manual/Integer-Arithmetic).
Primary documentation and installed public header inspected. Source 463
uses exact packed products, checks caller-owned buffer sizes, and hashes
the installed library/header. Integral binomial powers avoid local-ring
division by even integers. A synthetic target-size action takes 50.408
seconds; this is not an actual moment refinement or a complete solver.

**[method, scope check] van Bommel--Costa--Poonen--Srinivasan**,
[Curve equations from expansions of 1-forms at a nonrational point](https://arxiv.org/pdf/2506.14026),
Theorem 3.1 and Lemma 4.1. The primary exact-input hypothesis does not
bridge the present approximate-to-exact equality gap. No new curve
identification is attributed to that theorem.

**[inherited theory and new deductions]** D119 supplies the actual
principal-parts lattices and metrics; D116--D118 supply the direct section
certificate. The full inverse-map comparison and cofactor upper bound
are proved in D120. D51 and frozen sources 58/60/64 supply canonical Y64
and all-Hecke occurrence: old/new multiplicities settle norm-97 cofactor
separation, without recomputing Hecke matrices. Only the first norm-97
factor has order 51, matching the second T31 target; the other has order
257. Review 462 binds 961 sources and preserves all 922 D119 hashes.
Next test low-moment elimination on the existing bank. Exact curve and
field construction remain open; no correspondence was sent.


**Previous execution: D119 actual Cartier CM divisor and dyadic residue index, 2026-09-26.**
See [the proof](dembele/certificates/cm-cartier-frame-d119.md) and
[the source ledger](dembele/data/computed/cm_cartier_frame_sources_d119.json).
The actual finite flat Cartier divisor has eight intersections of length
33. Its residue index has beta-valuation 16=14+2; the full cokernel is
(R/(beta^2))^8. No improved quadric threshold or exact identification follows.

**[theory, local model]**
[Kurihara, Proposition 3-2 and Lemma 3-3](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf)
give the integral quotient and the smooth image of an inverted edge.
The cached primary pages 285, 287 and 288 were visually inspected again;
the new network fetch failed. D119 proves the ordinary quotient ring
R[[x,y]]/(xy-(2+b)) invariant under (x,y)->(-y,-x) is R[[x-y]] directly.

**[theory, models and principal parts]** The Stacks Project:
[0CDF](https://stacks.math.columbia.edu/tag/0CDF) for smooth images of
contracted exceptional tails; [0C9Y](https://stacks.math.columbia.edu/tag/0C9Y)
for the minimal regular model;
[0E7B](https://stacks.math.columbia.edu/tag/0E7B) for stabilization and
its structure-sheaf/cohomology properties;
[0B9D](https://stacks.math.columbia.edu/tag/0B9D) for relative Cartier
divisors in the smooth locus; and
[0E6N](https://stacks.math.columbia.edu/tag/0E6N) for Gorenstein duality.
These primary texts were inspected. D102's residue-index theorem is
now applied with actual dyadic hypotheses; D119 supplies the deduction.

**[new deductions and verification]** The horizontal order has normalization
index 264 and discriminant valuation 528. Cohomology torsion contributes
14 and the principal-part norm 2. Review 457 independently reconstructs
272 matrix entries, 17 minors and the residue map, binding 922 sources
and preserving all 911 D118 hashes. The geometric applications remain
mathematical proofs. A determinant identity bounds the pencil line;
the next task is the complete intrinsic-frame quadric height budget.
Non-dyadic indices and exact curve/field construction remain open.
No correspondence was sent.


**Previous execution: D118 finite CM height and tropical Faltings correction, 2026-09-26.**
See [the proof](dembele/certificates/cm-finite-height-d118.md) and
[the source ledger](dembele/data/computed/cm_finite_height_sources_d118.json).
The sufficient section valuations are 25330/25444/25551, versus actual
3794/3745/3728. No exact candidate identification or field polynomial follows.

**[theory, canonical Hodge lattice]**
[Yuan--Zhang, Theorems 4.5 and 4.7](https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n2-p04-p.pdf),
[Nekovar, section 1.5.3](https://doi.org/10.4153/CJM-2011-077-6), and
[Liu--Lorenzini, Proposition 4.4(a)](https://www.math.u-bordeaux.fr/~qliu/articles/modcove.pdf).
The small-level dualizing identification and stable extension permit
computing W_C -> L(Q)^2 on the standard node. D118 derives the exact
contents [280,17x16] and combined dyadic correction (69/34)*log(2).
No auxiliary level is computed. The Hodge/ramification summands are not
individually evaluated. The primary statements were inspected again.

**[theory, Faltings height and graph moment]** Robin de Jong and Farbod
Shokrieh, [Faltings height and Neron--Tate height of a theta divisor](https://arxiv.org/pdf/1810.02637),
Theorems A/B, equation (1.11) and the metric in section 12.1; and
[Tropical moments of tropical Jacobians](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7D168E767FECB100AF1FCF3EA6EF81F9/S0008414X22000220a.pdf/tropical-moments-of-tropical-jacobians.pdf),
Theorems 11.2/11.4. The existing graph has tropical moment 223268/27075.
Their metric agrees with D103's determinant L2 metric; its normalized
dyadic contribution is (55817/54150)*log(2). The remaining theta-height
and local terms are discarded by nonnegativity. Both primary papers
and the normalization warning were inspected.

**[new deductions and verification]** The corrected CM height is below
8/3 and the new Faltings lower bound is above -23.146371. Review 455
checks leading valuations, a graph inverse, independent resistance
integrals and logarithm budgets, binding 911 sources and preserving
891 D117 hashes. All four input jobs pass. The geometric theorem
applications are supplied by the report, not machine verification.
Next test the D102 principal-parts construction with its actual divisor
hypotheses; index 245 is not inferred. No correspondence was sent.


**Previous execution: D117 uniform CM disks and arithmetic exactness, 2026-09-26.**
See [the proof](dembele/certificates/cm-disk-and-exactness-d117.md) and
[the source ledger](dembele/data/computed/cm_disk_sources_d117.json).
The new CM projection-lattice argument certifies disks of radius squared
3/5 at every CM point and conjugate. Joint norm/height bounds reduce the
sufficient section valuations to 35947/36096/36237, versus actual lower
bounds 3794/3745/3728. Exact curve and field construction remain open.

**[theory, Arakelov normalization]** Ariyan Javanpeykar,
[*Polynomial bounds for Arakelov invariants of Belyi curves*, Lemma 2.4.4](https://msp.org/ant/2014/8-1/ant-v8-n1-p04-s.pdf),
for h_Fal(C)>=-g*log(2*pi), in D103's L2 convention. The primary PDF was
inspected; D117 retains its pi factor in the combined bound. D104's saved
CM Hodge height and its stable-model comparison remain the height input.

**[inherited theory]** D116's integral complementary-minor identity and
conditional nodal jets, and D88/D69's exact 68>60 identification criterion,
are unchanged. The Aitken DOI refetch returned InternalError; D116's
primary-source reading is reused without claiming a fresh inspection.

**[new deductions and verification]** The integral commutator trace and CM
projection yield exact weighted-lattice exclusions. Review 450 independently
checks both searches and logarithm budgets, binding 891 sources and preserving
868 D116 hashes. These geometric applications are proved in the companion
report; the finite tests do not machine-verify uniformization. The radius-one
fixed-input limits 32928/33064/33193 show that further disk refinement alone
cannot close the gap. The next calculation concerns the finite corrections
discarded in D104, not an unproved numerical equality. One serialization-only
failure is archived. No correspondence was sent; all resource pauses remain.


**Previous execution: D116 integral quadric identification criterion, 2026-09-26.**
See [the proof](dembele/certificates/cm-compound-height-d116.md) and
[the source ledger](dembele/data/computed/cm_compound_sources_d116.json).
Direct quadratic-section bounds replace ratio reconstruction as the
primary exactness route. Sufficient successive beta-valuations are
119806/120284/120758, versus achieved lower bounds 3794/3745/3728.
No positive jet has been proved exactly zero.

**[theory, determinant identities]** A. C. Aitken,
[*On the Evaluation of Determinants, the Formation of their Adjugates, and the Practical Solution of Simultaneous Linear Equations*](https://doi.org/10.1017/S001309150000794X),
for the classical complementary-minor framework. D116 proves the
integral polynomial cancellation and the explicit adjacent-pair identity
for Q(s)/Delta, with its tensor norm below 2^4855.

**[theory, integral quotient and duality]**
[Nekovar, section 1.5.3](https://doi.org/10.4153/CJM-2011-077-6)
and [Stacks, 0E6N](https://stacks.math.columbia.edu/tag/0E6N).
The quotient has rational normalized components and nodes of stabilizer
thickness; the relative dualizing line is invertible and compatible with
base change. D99's inspected Kurihara Proposition 3-2/Lemma 3-3 remain
the wild-quotient input. The current Kurihara fetch returned HTTP 429;
no new reading is claimed. D116's integral residue isomorphism,
canonical generation and conditional nodal divided-jet arguments are
our deductions, backed by exact lattice and graph witnesses.

**[theory, finite-place averaging]**
[Milne, Class Field Theory](https://www.jmilne.org/math/CourseNotes/CFT.pdf):
the principal dyadic prime (beta) splits in H/M. D105's Hilbert class
field identification and the equivariant cofactor construction permit
averaging the seventeen local CM values over the seventeen primes of H.
This reduces the alternative ratio equality bounds to 132444/524481.

**[theory, exact identification]**
[van Bommel--Costa--Poonen--Srinivasan, Lemma 4.1/Corollary 4.2](https://arxiv.org/pdf/2506.14026)
and D88: exact four-coefficient quadric vanishing gives 68>60 and
identifies the base candidate using D69. The new section criterion
does not need a rank-45 witness. Higher integral jets require preceding
exact zeros; numerical agreement does not satisfy that hypothesis.

**[method and computation]** [Franc--Masdeu](https://arxiv.org/pdf/1201.0356)
provides the moment/Poisson framework. The direct ramified-field proof
and D115 bank give the third coarse coefficient without new moments.
Review 445 independently checks all third coefficients, 4641 positive
quadratic coefficients, actual rank at least 33, and the bounds, preserving
814 prior hashes in the 868-source final review; its recheck also passes.
The stable-model interpretation is a mathematical proof, not a
machine-verified uniformization theorem. Exact curve and
field construction remain open. All resource pauses remain; no
correspondence was sent. Earlier next steps are historical.


**Previous execution: D115 actual rational-frame comparison and revised strategy, 2026-09-25.**
See [the report](dembele/certificates/dyadic-comparison-and-strategy-d115.md)
and [the ledger](dembele/data/computed/dyadic_comparison_sources_d115.json).
The actual rational residue frame and first two ratio coefficients are
computed, with candidate-difference beta-bounds **101/70** at the sixteen
non-anchor CM points. This is finite agreement, not exact identification.

**[target]** [Dembélé's original construction](https://arxiv.org/pdf/0811.4379)
specifies the residual kernels and nonsolvable extension. No new target
polynomial or substitute-kernel claim is made.

**[method]** [Franc--Masdeu](https://arxiv.org/pdf/1201.0356), section 6.1,
for moment/Poisson evaluation. Their introduction also distinguishes
numerical equation recognition from proof. D108/D113 supply the direct
ramified-field convergence and precision arguments used here. No Qp
control theorem or precision proposition is transferred unchanged.

**[theory, reconstruction criterion]**
[van Bommel--Costa--Poonen--Srinivasan](https://arxiv.org/abs/2506.14026)
provides the expansion-based framework used by D88/D106. Exact expansion
equality is still required; finite local agreement does not activate
the rank-45 identification criterion without an exactness mechanism.

**[our computations and deductions]** Full polynomial arithmetic reaches
moment precision 200. The same splitting root is refined to error 352,
with normalized transport errors 331/337. The W leading valuation 296
is resolved. The seventeen projective CM rows determine the actual
rational residue frame; the chosen Gaussian is numerically nonzero at
sixteen points and hence qualitatively nonzero on the whole CM divisor.
Independent formal-series division and reversion checks the first two
ratio coefficients. Source 423 applies the product formula with dyadic
local degrees 1 and 16, using rational logarithm enclosures. At the
degree-16 place the current sufficient equality bounds are beta-errors
274241/820774, or pi-errors 137121/410387. These are not achieved and
are not asserted necessary for every proof.

**[tool]** Python and NumPy perform exact bounded integer/rational
operations, with explicit overflow bounds and a 180-second process cap.
Review 431 binds 814 sources and preserves all 713 D114 hashes. Failed
implementation probes are archived; the corrected and independent
checks pass. The next requirement is an exact arithmetic identification
certificate. Global cubic data, target torsion and the field polynomial
remain open. All resource pauses remain; no correspondence was sent.
Earlier next steps are historical.


**Previous execution: D114 actual coarse differential jets and anchor precision gate, 2026-09-25.**
See [the proof](dembele/certificates/dyadic-coarse-d114.md) and
[the ledger](dembele/data/computed/dyadic_coarse_sources_d114.json).
The first three actual coarse differential coefficients are computed
in the harmonic basis at all seventeen matched CM points.

**[method, Poisson evaluation from moments]** Cameron Franc and
Marc Masdeu,
[*Computing fundamental domains for the Bruhat--Tits tree for GL2(Qp), p-adic automorphic forms, and the canonical embedding of Shimura curves*](https://arxiv.org/pdf/1201.0356),
section 6.1 and Remark 6.5, provide the computational framework
for integrating locally analytic kernels from moments. The required
ramified-field convergence, contraction and tail estimates are the
direct proofs in D108/D113, refined in D114. Their Qp control
theorem and precision propositions are not transferred unchanged.

**[our proof and computation]** Sources 414--416 extend the actual
bank to 130,848 state entries and 26,112 CM entries modulo pi^16.
Only low-degree moments require a fixed-system solve. Combining
the D108 coarse formula with chart expansions gives integral kernels
and errors 24,32,24 pi-digits. Separate expansion of
K_j(t)=(1-((beta+t)/(beta-t))^(2j+2))/2 verifies all coefficients,
with the dyadic division loss accounted for explicitly.

The D112 embedded CM involution and D111 measure invariance give
g_j=2*integral_A K_j dmu. The resulting stronger errors are
32,40,32 pi-digits, and all 256 non-anchor entries per order are
certified nonzero. At W, monic division by (X^2-X)^16 proves every
integral polynomial A moment divisible by pi^16; adding degrees
alone at this precision cannot resolve the anchor. The coefficient
valuations there are bounded below by 32.5,40.5,32.5. These are
our deductions from the actual certified moment bank, not external
theorem statements or exact vanishing claims.

**[tool]** Python and NumPy supply exact bounded integer arithmetic;
no floating-point solve or numerical tolerance enters the certificate.
Review 416 binds 713 sources and preserves all 696 D113 hashes.
The failed implementation probe is archived; the corrected probe
and final review pass. The next bounded pilot raises precision to
24 with the full Eisenstein quotient, retaining the existing charts.
Actual rational-frame ratio jets, basis change, a Gaussian pivot,
candidate identification and the target polynomial remain open.
All resource pauses remain. No correspondence was sent. Earlier
next steps are historical.


**Previous execution: D113 actual positive moments by finite contraction, 2026-09-25.**
See [the proof](dembele/certificates/dyadic-moments-d113.md) and
[the ledger](dembele/data/computed/dyadic_moment_sources_d113.json).
The finite moment recursion and actual pilot over ramified K are
complete, with certified positive moments in all 51 matched CM charts.

**[method, moments and iterative lifting]** Cameron Franc and
Marc Masdeu,
[*Computing fundamental domains for the Bruhat--Tits tree for GL2(Qp), p-adic automorphic forms, and the canonical embedding of Shimura curves*](https://arxiv.org/pdf/1201.0356),
sections 4.1--4.2 and 6.1, especially Theorems 6.2--6.3. Their
finite-chart moment and Poisson-evaluation framework motivates the
construction. We prove the required scalar contraction directly
from the two residue-ball maps and the existing bound d=0. Their
Qp control theorem, precision constants and software are not
transferred unchanged to our ramified degree-eight completion.

**[method, tree coordinates]**
[Masdeu--Torrents](https://arxiv.org/pdf/2510.09356), section 2.2
and Lemma 2.2 in the version consulted here, for column lattices and
edge representatives over completions of totally real fields. The
existing D111 arithmetic supplies every transport; no external domain
implementation or expanded census is run.

**[our proof and computation]** Sources 411--413 certify 348 child
contractions and 51 CM ball isomorphisms. The coefficient estimate
v([x^k]phi^n)>=k gives one pi-digit per iteration; state cutoff J,
N iterations and precision P give error min(J+1,N,P). A CM degree-n
transfer has error min(P,J+1-n). The pilot saves 33,408 state moments
modulo pi^12 and CM degrees 1,2,3 with errors 11,10,9. Independent
polynomial arithmetic checks all residuals, and direct integration
over 32 leaf balls supplies separate sample checks. NumPy performs
bounded integer operations only; it supplies no analytic error theorem.

Review 413 binds 696 sources and preserves all 682 D112 hashes.
All 144 positive entries at W remain zero modulo their bounds;
no exact vanishing or normalization is proved. Next feed a modest
higher-degree bank into D108's coarse Poisson formulas. No actual
differential value/jet, frame change, candidate identification or
target polynomial is obtained. No correspondence was sent.
Earlier next steps are historical.


**Previous execution: D112 dyadic CM coordinates and arithmetic frame matching, 2026-09-25.**
See [the proof](dembele/certificates/dyadic-cm-matching-d112.md) and
[the ledger](dembele/data/computed/dyadic_cm_matching_sources_d112.json).
All seventeen CM embeddings now have exact coordinates, relative
class witnesses and arithmetic root/frame labels. The harmonic
measures' actual zeroth masses on 51 boundary charts are also certified.

**[theory, canonical CM reciprocity]** John Voight,
[*Shimura curve computations*](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf),
sections 4.3 and 4.5, for CM points over totally real base fields and
Atkin--Lehner quotients. His
[*Computing CM points on Shimura curves arising from cocompact arithmetic triangle groups*](https://jvoight.github.io/articles/shimcm-fixed-errata.pdf),
Theorem 5.1 and Algorithm 5.2, states the arithmetic Artin convention:
iota(a)O=xi O sends the point to xi^(-1)P. We use that general CM law,
not triangle-group analytic algorithms or the separate descent claim.

**[theory, prime-to-p equivariance]**
[Dembélé](https://arxiv.org/pdf/1906.06772), section 4.1, Theorem 4.3
and Proposition 4.4, supplies the canonical adelic presentation and
dyadic uniformization over the completed maximal unramified extension.
The retained prime-to-p action gives the localized Artin formula
with the normalized CM eigenvalue character. The principal dyadic
prime loses no class under localization. The report explains this
application over ramified K; an inert-Qp CM theorem is not applied
outside its hypotheses. The paper's hyperellipticity assertion is unused.

**[our deductions and computations]** Sources 407--410 give exact
coordinate conjugations, the kW=-Wk anchor witness and seventeen
principal ideal-class relations. The unique K-root and the local
class action of sigma(beta)=beta^3+3*beta, with exponent 10, combine
with D107's exact resolvent to certify the root orientation. Rational
replay proves 688-beta-digit root errors and 384-beta-digit algebraic
residue-frame errors. D111's reducer certifies the zeroth chart
masses A0=0 and B0+C0=0. One incorrect valuation expectation at the
anchor is archived; eta1 has v2=7 there.

Review 410 binds 682 sources, preserving all 661 D111 hashes.
The geometric reciprocity argument is a stated mathematical input,
not a machine-verified theorem. Positive-degree moments and the
actual harmonic-to-residue change of basis remain needed before
jet evaluation. No candidate identification or target polynomial
is obtained. No correspondence was sent. Earlier next steps are historical.


**Previous execution: D111 arithmetic edge reduction and harmonic cocycles, 2026-09-25.**
See [the proof](dembele/certificates/dyadic-harmonic-d111.md) and
[the ledger](dembele/data/computed/dyadic_harmonic_sources_d111.json).
Sixteen actual invariant cocycles and their bounded boundary measures
are constructed, with complete neighbor/stabilizer data for the same
58 classes and a terminating arithmetic edge reducer.

**[method, harmonic cocycles and boundary measures]** Cameron Franc
and Marc Masdeu, [*Computing fundamental domains for the Bruhat--Tits
tree for GL2(Qp), p-adic automorphic forms, and the canonical embedding
of Shimura curves*](https://arxiv.org/pdf/1201.0356), sections 4.1--4.2
and 4.4. Their scalar harmonic and boundary-distribution framework is
used with an explicit ball-partition proof over our ramified K.
Finite integral values give the bound d=0. Their Qp overconvergent
control theorem and precision constants are not transferred to K.

**[method, local tree coordinates]**
[Masdeu--Torrents](https://arxiv.org/pdf/2510.09356), section 2.1 and
Lemma 2.2: column lattices, adjacency and representatives with global
integral entries. No external domain implementation is run. Existing
HMF get_rids/get_tps and norm-one unit routines supply the same-session
data; complete class/unit counts retain their certified provenance.

**[our deductions and computations]** Sources 403--406 certify all
58 local frames, 174 neighbor entries and 164 stabilizer elements.
P-supported indices and local equality prove the global right-ideal
and sandwich assertions. Exact annihilation and ranks modulo 101
certify a 16-dimensional kernel of the 376-by-174 relation matrix.
There are 155 oriented edge orbits, nine inverted orbits and 73
reversal pairs. Adaptive Hensel refinement supports the arithmetic
reducer; tests cover depth 32 and invariance under u/W/h.

Review 406 binds 661 sources, preserving all 643 D110 hashes.
All five bounded jobs pass on first attempts. D110's geometric
uniformization and D99's nonhyperelliptic conclusion are unchanged.
Next match the dyadic CM embedding and marked frame, then establish
actual moments with a proved local error bound. No actual jet,
candidate identification or target polynomial is claimed.


**Previous execution: D110 explicit dyadic group and moving-vertex transports, 2026-09-25.**
See [the proof](dembele/certificates/dyadic-group-transport-d110.md) and
[the ledger](dembele/data/computed/dyadic_group_transport_sources_d110.json).
The arithmetic now supplies an explicit odd Atkin--Lehner coset and
certified transports moving the base vertex. No complete domain or
generating set, harmonic cocycle or actual Shimura jet is claimed.

**[theory, geometric uniformization]** Lassina Dembélé,
[*A hyperelliptic Shimura quotient of genus 16*](https://arxiv.org/pdf/1906.06772),
Theorem 4.3 and Proposition 4.4: geometric Cerednik--Drinfeld
uniformization, the two-layer Brandt graph and the Atkin--Lehner layer
interchange. The paper's hyperellipticity assertion is not used; D99's
nonhyperelliptic conclusion is unchanged. Our specialization uses D99's
class-number-one and positive-unit-square certificates to identify
the projective norm-one subgroup with the norm-parity kernel.

**[method, arithmetic action]**
[Masdeu--Torrents](https://arxiv.org/pdf/2510.09356), sections 2.1--2.2,
provides the norm-one S-arithmetic setting and column-lattice action.
The local HMF get_rids/get_tps interfaces supply same-session witnesses;
their exact ideal sandwiches are independently checked. Reconstructing
the old 58-class calculation adds no new level or Hecke prime.

**[our deductions and certificates]** With R=O[1/b], G=R*/O_F[1/b]*,
the projective norm-one group Gamma has quotient G/Gamma=C2. An exact
odd witness normalizes to W=(1+b/2)i+cj with W^2=-(2+b). It displaces
the base vertex seven edges. For D109's unit u, g=WuW^(-1) has norm
one and displacement fourteen. The product ug has trace valuation -7,
proving hyperbolic translation length fourteen. These calculations
use D109's unchanged exact splitting, not a new local approximation.
Review 402 binds 643 sources, preserving all 629 D109 hashes; all
four bounded jobs pass on first attempts. Dyadic CM/frame labeling,
moments, actual jets and candidate identification remain open.


**Previous execution: D109 integral dyadic splitting and edge transport, 2026-09-25.**
See [the proof](dembele/certificates/definite-dyadic-d109.md) and
[the source ledger](dembele/data/computed/definite_dyadic_sources_d109.json).
The actual definite order, exact integral splitting and one norm-one
edge transport are certified. The witness fixes the base vertex and
cycles its three neighbors; no full fundamental domain is claimed.

**[tool, local matrix proposal]**
[Magma Handbook, Hilbert Symbols and Embeddings](https://magma.maths.usyd.edu.au/magma/handbook/text/1074),
`pMatrixRing(O,p)` with its precision parameter. Its hypothesis is
that the quaternion algebra splits at p; it permits our ramified K.
The proposed matrices are converted to exact rational centers.
Hensel lifting, quaternion relations, integral order images and residue
rank four independently certify the final splitting. Approximate
matrix equality is not used as a proof of exact relations.

**[method, group and tree action]** Marc Masdeu and Eloi Torrents,
[*Fundamental domains for quaternionic S-arithmetic groups over
totally real fields*](https://arxiv.org/pdf/2510.09356), sections 2.1--2.2
and 3, give the norm-one S-arithmetic setting, integral splitting,
column-lattice action and arithmetic equivalence witnesses. We verify
one such witness directly. Their full algorithm and public software
have not been run here; no degree-eight runtime claim is inferred.

**[tool, actual order provenance]** The existing HMF `hackobj.m`
selects (-1,-1)_F in `QuaternionOrder(M)`. Its `precompute.m` supplies
the inspected local-splitting and ideal/transport interfaces. These
files were read only and are hash-bound. No new ideal-class census
was requested, and the level-one `SplittingMap` was not used.

**[our computations and deductions]** Scripts 397--399 check all 1024
order-basis products and trace determinant 2^124. Hensel residual and
derivative valuations 188 and 8 define an exact local root with error
180. Order-image errors are at least 176; residue rank four proves
the integral isomorphism. The unit (1-i-j-k)/2 has norm one and gives
neighbor permutation [2,0,1], with a certified integral lattice
transition of determinant one. Wrong-root and wrong-target controls
are rejected. Review 399 binds 629 sources and preserves all 606 D108
hashes. One equality failure and two bounded timeouts are archived.

Next make D99's known group and normalizer quotient explicit in these
coordinates and verify a transport moving the base vertex, reconciling
the saved 58-class data. Actual harmonic cocycles, moments, dyadic
CM/frame matching, Shimura jets and candidate identification remain
open. The new splitting does not close those separate requirements.


**Previous execution: D108 evaluator feasibility and dyadic interface, 2026-09-25.**
See [the report](dembele/certificates/shimura-evaluator-d108.md)
and [the ledger](dembele/data/computed/shimura_evaluator_sources_d108.json).
The completed per-ideal absolute spectral comparison fails a necessary
condition. A conditional dyadic moment-to-jet formula has explicit
errors; actual Shimura moments are not supplied.

**[theory and project deduction, spectral rejection]**
[DLMF 5.5.1](https://dlmf.nist.gov/5.5.E1) specializes D98's multiplier
by Gamma recurrence. The completed value, global maximum of h_p(1)
and seven-prime comparison floor are our calculations. D91's quadrature
proof applies at k=1. The floor concerns the retained absolute Hecke
and unsigned diagonal comparison, including positive power-kernel
mixtures; it is not a theorem excluding Nelson's method.

**[method, direct moment evaluation]** Cameron Franc and Marc Masdeu,
[*Computing fundamental domains for the Bruhat-Tits tree for GL2(Qp),
p-adic automorphic forms, and the canonical embedding of Shimura curves*](https://arxiv.org/pdf/1201.0356),
section 6.1. The updated arXiv footnote in section 5.2 corrects the
harmonicity/eigencondition. Its Q_p control theorem is not claimed to
apply unchanged over our ramified degree-eight completion. Our
three-chart tails and coarse-coordinate error calculation are proved
directly for bounded measures.

**[method, arithmetic tree input]** Marc Masdeu and Eloi Torrents,
[*Fundamental domains for quaternionic S-arithmetic groups over
totally real fields*](https://arxiv.org/pdf/2510.09356), section 3.
This provides an algorithm for the missing domain and transport data.
The [public implementation](https://github.com/Eloitor/btquotients)
has not been pinned or run here. The existing local HMF order/ideal
interface was inspected; a certified dyadic splitting remains needed.

**[tool scope]**
[Sage p-adic automorphic form documentation](https://doc.sagemath.org/html/en/reference/modsym/sage/modular/btquotients/pautomorphicform.html)
distinguishes Riemann refinement from moment evaluation. Its Q_p
examples are not an implementation for our K. The old complex bank
is likewise not certified by the numerical method of
[Voight--Willis](https://jvoight.github.io/articles/ModFormPaper-090317.pdf),
whose introduction explicitly leaves correctness unproved.

**[our computations]** Scripts 394--396 certify the comparison floor
and test the conditional moment interface. Review 396 binds 606
sources and checks all 588 D107 hashes unchanged. The controls are
synthetic measures, not arithmetic Shimura forms. No actual tangent,
dyadic CM match, chart or candidate identification is obtained.


**Previous execution: D107 certified CM point/root matching, 2026-09-25.**
See [the proof](dembele/certificates/cm-root-matching-d107.md)
and [the source ledger](dembele/data/computed/cm_root_matching_sources_d107.json).
The old seventeen-point lookup is certified by exact real structure,
rational root disks, an integral norm, finite rank and local lifting.
No actual Shimura differential evaluation is supplied.

**[theory, CM reciprocity convention]** John Voight,
[*Computing CM points on Shimura curves arising from cocompact
arithmetic triangle groups*](https://jvoight.github.io/articles/shimcm-fixed-errata.pdf),
Theorem 5.1 and Algorithm 5.2, printed page 8: an ideal with
iota(a)O=xi O acts by z -> xi^(-1)z under arithmetic Artin action.
The general totally real canonical-curve setting and the normalizer
quotient are in his
[*Shimura curve computations*](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf),
sections 4.3 and 4.5. We reuse D59's exact ideal labels, not its
approximate root comparison. The triangle parametrization and the
first paper's separate descent assertions are not used.

**[theory, root certification]** Terence Tao,
[*Math 246A, Notes 4: singularities of holomorphic functions*](https://terrytao.wordpress.com/2016/10/11/math-246a-notes-4-singularities-of-holomorphic-functions/),
Theorem 37 (Rouche). Our cleared-denominator inequalities bound each
Taylor remainder and prove one root in each proposed rational disk.
The centers come from Newton iteration; their accuracy is established
by these inequalities, not assumed from working precision.

**[context, complex conjugation]** Don Blasius and Lucio Guerberoff,
[*Complex conjugation and Shimura varieties*](https://msp.org/ant/2017/11-10/ant-v11-n10-p02-s.pdf),
section 2.2, especially the discussion after Lemma 2.2.4, printed
page 2297. D107 identifies its antiholomorphic map with canonical
conjugation using D106 rigidity instead of applying their later
CM-reflex-field descent theorem.

**[tool and convention]**
[SageMath ideal documentation](https://doc.sagemath.org/html/en/reference/number_fields/sage/rings/number_field/number_field_ideal.html),
gens_reduced(proof=True), supplies a principal generator witness;
independent rational arithmetic verifies the resulting order unit
and inverse. The actual matrix convention is read from
[Rickards's fdom.c](dembele/vendor/rickards-fdom/fdom.c),
afuch_make_m2rmats, lines 2709--2740. Its off-diagonal signs determine
the CM embedding orientation.

**[our deductions and checks]** Marked rigidity identifies the real
structure. A unit witness fixes point 8; rational signs select
beta=-i*sqrt(2+b). The field norm makes kappa_f=gamma exact, and
rank 271 makes directed cycle sums injective. Independent lifts
identify Frobenius at beta=19, of saved class 3. Review 393 binds
588 sources and preserves all 562 D106 hashes. The geometric proof
and literature inputs are not machine-verified. Neither the old
differential bank nor a particular actual Gaussian chart is certified.


**Previous execution: D106 rational CM frame and higher jets, 2026-09-24.**
See [the proof](dembele/certificates/cm-rational-frame-jets-d106.md)
and [the source ledger](dembele/data/computed/cm_rational_frame_sources_d106.json).
The actual D-marked automorphism group is trivial. D58's geometric
Q-descent is compatible with the F-model, and the residue frame is
rational up to a scalar. Height bounds through order three and exact
candidate references give finite comparison thresholds. No independent
Shimura evaluator or numerical root-matching certificate is obtained.

**[theory, faithful stable specialization]** The Stacks Project:
[Lemma 109.24.2, tag 0E97](https://stacks.math.columbia.edu/tag/0E97)
extends generic automorphisms to stable models;
[Theorem 109.25.3, tag 0E9C](https://stacks.math.columbia.edu/tag/0E9C)
gives proper Deligne--Mumford moduli and hence finite unramified
automorphism schemes;
[Theorem 41.6.2, tag 024U](https://stacks.math.columbia.edu/tag/024U)
makes specialization injective on sections over a connected base.
These statements permit residue characteristic 2. The further
injection into the graph group uses the actual three attaching
points on every rational component.

**[theory, compatible marked descent]** Lassina Dembélé,
[Lemma 5.2](https://arxiv.org/pdf/1906.06772), and Jeroen Sijsling--John Voight,
[*On explicit descent of marked curves and maps*](https://jvoight.github.io/articles/birch-descent-021420.pdf),
Theorems 1.3.2 and 2.1.1, section 2.2 and Corollary 2.2.3 in the
2020 author version. D58's canonical-conjugation and smooth-source
marking give geometric descent. D106's new rigidity proof removes
its conditional F-twist issue. The graph computation does not
reprove canonical conjugation. Dembélé's hyperellipticity and
admissibility/exponent assertions are not used.

**[theory, exact jet identification]** Raymond van Bommel, Edgar
Costa, Bjorn Poonen and Padmavathi Srinivasan,
[*Curve equations from expansions of 1-forms at a nonrational point*](https://arxiv.org/pdf/2506.14026),
Lemma 4.1 and Corollary 4.2. D88 applies their degree/order test
and derives the J3 rank refinement. D106 supplies the rational-frame
proof and higher-jet separation bounds; the paper does not supply
our missing arithmetic Shimura expansions.

**[our deductions and checks]** Odd orbit plus Galois transitivity
and the CM projective frame prove marked rigidity. Self-normalizing
affine stabilizers give a unique degree-17 residue-field isomorphism.
Higher integral differential expressions extend D103 and yield heights
10504,31518,52533. Candidate heights 677,1947,3218 give sufficient
inert-31 valuations 3257,9746,16236. Scripts 387--389 check finite
graph/group facts, formal identities and 364 exact quadric coefficients;
the review binds 562 sources and preserves all 543 D105 hashes.
No existing actual errors are certified by these thresholds.


**Previous execution: D105 actual CM frame and tangent atlas, 2026-09-24.**
See [the proof](dembele/certificates/cm-frame-arithmetic-d105.md)
and [the source ledger](dembele/data/computed/cm_frame_arithmetic_sources_d105.json).
Nine exact graph witnesses prove H0(K-D)=0 on the actual curve;
CM transitivity gives all nonzero cofactors. The height bound now
applies to an atlas over H without the old numerical orientation.
Saved labels, a specific chart and F descent remain open.

**[theory, annulus geometry]** Matthew Baker, Sam Payne and Joseph
Rabinoff, [*On the structure of nonarchimedean analytic curves*](https://arxiv.org/pdf/1404.0279),
Propositions 2.2, 2.5, 2.10, Corollary 2.6 and Proposition 4.3.
Units, skeleton slopes, zero counting and node tubes support our
deduction that an ends-interchanging involution has two simple generic
fixed points even in residue characteristic 2.

**[theory, integral quotient]** Akira Kurihara,
[*On some examples of equations defining Shimura curves and the Mumford uniformization*](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf),
Proposition 3-2 and Lemma 3-3, pp. 284--288. The inverted node's
quotient is smooth. D99's saved scan, including pp. 287--288, was
inspected again. No assumption that invariants commute with reduction.

**[theory, specialization]** Matthew Baker,
[*Specialization of linear systems from curves to graphs*](https://arxiv.org/pdf/math/0701075),
Corollary 2.10 and Lemma 4.19. Rank and the canonical divisor class
specialize as required on the totally degenerate curve. D105 supplies
the marked locations and a direct metric-graph maximum argument for
its integer-potential/burning certificates.

**[theory, common auxiliary field]** John Voight,
[*Shimura curve computations*, §4.3](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf),
gives Hilbert-class-field definition and reciprocity for maximal-order
CM points over general totally real F. J. S. Milne,
[*Class Field Theory*, I.1.8--1.11 and V.3.9](https://www.jmilne.org/math/CourseNotes/CFT.pdf),
supplies local units/unramifiedness and the Hilbert class field.
Combining these with D59's proved arithmetic and the exact resolvent
identifies the common field H of degree 272. Numerical orientation
and the disputed hyperellipticity/Jacobian implication are unused.

**[theory, tangent chart]** Ravi Vakil,
[*Foundations of Algebraic Geometry, Class 46*, Exercise 1.A](https://math.stanford.edu/~vakil/0708-216/216class46.pdf).
The canonical map of a nonhyperelliptic curve is an embedding. This
ensures one of fifteen Gaussian coordinates is nonzero; it does not
select G12. D105 extends D103's max-norm bound to the whole projective
vector and uses D104's CM height.

**[our deductions and checks]** Scripts 384--386 preserve the conditional
probe, verify all nine branch allocations and independently reconstruct
the marks from Brandt data. The audit binds 543 sources. Candidate-only
height below 677 gives sufficient errors 10^(-1320873) at one embedding
or 10^(-4857) at every embedding of H; these do not certify an evaluator.
Higher-jet equality and descent still need proof.

**Previous execution: D104 intrinsic CM height, 2026-09-24.**
See [the proof and numerical certificate](dembele/certificates/cm-intrinsic-height-d104.md)
and [the detailed source ledger](dembele/data/computed/cm_intrinsic_height_sources_d104.json).

**[theory, stable extension]** Qing Liu and Dino Lorenzini,
[*Models of curves and finite covers*](https://www.math.u-bordeaux.fr/~qliu/articles/modcove.pdf),
Compositio Mathematica 118 (1999), 61--102. Proposition 4.4(a) and
Corollary 4.7 extend generic maps between stable models. D104 derives
the integral differential and its second map at ramification, even
when the section meets a node. Minimal regular models are not assumed
functorial.

**[theory, Hodge models and CM identities]** Xinyi Yuan and Shou-Wu Zhang,
[*On the averaged Colmez conjecture*](https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n2-p04-p.pdf),
Annals of Mathematics 187 (2018), 533--638. Theorems 4.5/4.7 give the
semistable small-level models and canonical Hodge system used in our
fibre comparison. Theorem 1.1 and Corollary 2.6/Theorem 2.7 provide the
averaged and nearby CM identities. Their Shimura-point height divides
by degree over F; D104 uses absolute degree. CM-point Theorems 1.6/1.7,
which exclude common ramification, are not applied.

**[theory, common ramification permitted]** Roy Zhao,
[*Heights of Special Points on Quaternionic Shimura Varieties*](https://arxiv.org/pdf/2309.08886),
v1, 16 September 2023, Theorem 7.4. Our specialization gives
`h_L=-R/8+log(2)/16`. The final proof display of 7.5 drops d_Sigma
from log(d_B*d_Sigma), unlike 7.4 and the statements of 1.1/7.5;
D104 derives its formula from 7.4 and retains the factor. No author
confirmation is claimed. CM and curve Faltings metric conventions
are kept separate.

**[analytic identities]** NIST DLMF,
[Dirichlet/Hurwitz relation](https://dlmf.nist.gov/25.15.E3),
[Hurwitz values](https://dlmf.nist.gov/25.11.E18), and
[Gamma series](https://dlmf.nist.gov/5.7).
Our exact traces and explicit rational remainder bounds prove
`h_L<17/10` by two methods. The stable-fibre inequality, resulting
`H_CM,disk<41/10`, conditional `h(v_j)<10504`, and recognition
thresholds are project deductions. Arithmetic CM labels and
frame/chart nonvanishing remain hypotheses.

**Previous execution: D103 adjugate tangent-height bound, 2026-09-24.**
See [the proof and exact controls](dembele/certificates/cm-adjugate-height-d103.md).

**[theory, metric normalization and universal lower bound]** Ariyan
Javanpeykar, with an appendix by Peter Bruin,
[*Polynomial bounds for Arakelov invariants of Belyi curves*](https://msp.org/ant/2014/8-1/ant-v8-n1-p04-s.pdf),
Algebra & Number Theory 8 (2014), 89--140. Sections 2.1--2.3 fix the
L2/determinant metrics and normalized degree; Lemma 2.4.4 states
Bost's bound `h_Fal(C)>=-g*log(2*pi)` in that convention. D103 uses
only this universal lower bound, not a Belyi-degree estimate or a
numerical upper bound for the curve's height.

**[theory, integral extension]** The Stacks Project,
[0E6N](https://stacks.math.columbia.edu/tag/0E6N), provides the
invertible relative dualizing sheaf and base change for nodal curves.
D103 proves the integral Gaussian extension from the local map
`dx -> x*xi, dy -> -y*xi` on `xy=a`; no residue-characteristic
denominator is introduced.

**[our deductions]** The adjugate construction, arithmetic CM
displacement bound and inequality `h(v_j)<=513*H_CM,disk+8400`
are project deductions, with exact controls in scripts 380--381.
Their arithmetic inputs are the saved quaternionic CM data and the
D102 field basis. They use no candidate equations or jets. The
inequality avoids a separate residue-index bound but remains
conditional on the actual arithmetic frame and chart hypotheses.

**[next comparison, not established]** Roy Zhao,
[*Heights of Special Points on Quaternionic Shimura Varieties*](https://arxiv.org/pdf/2309.08886),
Theorem 1.1 and section 6 (v1, 16 September 2023). The height and
metric could bound the remaining H_CM,disk after an integral
comparison with our stable coarse normalizer quotient. The generic
double-cover identity alone does not prove this comparison, especially
at 2. The D101 common-ramification applicability restrictions remain.

**Previous execution: D102 integral residue frame, 2026-09-24.**
See [the local index formula and exact checks](dembele/certificates/cm-residue-lattice-d102.md).

**[theory, specialized here]** The Stacks Project,
[0E6N: relative dualizing sheaves](https://stacks.math.columbia.edu/tag/0E6N),
[0B4A: Cartier-divisor adjunction](https://stacks.math.columbia.edu/tag/0B4A),
and [0BUK: finite dualizing modules](https://stacks.math.columbia.edu/tag/0BUK).
The reviewed statements provide relative duality, the principal-parts
sequence and the lattice Hom_R(A,R). D102 derives its two-term
residue-index formula from these inputs. No source is asserted to
provide an actual integral marked Shimura model or a bound for the
principal-part norm and cohomology torsion in this application.

**[our derivations and exact arithmetic]** The fixed good-reduction
genus-two and nonhyperelliptic quartic examples, cofactor product and
inverse-matrix bound are project calculations. They concern varying
split local divisors and do not refute a CM-specific height bound.
Scripts 378--379 independently verify the saved degree-17 field order
from D57/D59: trace discriminant 2^79, trace-dual denominator 32 and
the factor-17 centered-basis conversion. The polynomial's Elkies
attribution remains that of the saved arithmetic audit. These field
lattice facts do not identify the horizontal divisor's order or bound
the actual Shimura tangent. Zhao/Yuan remain potential height inputs
with the D101 applicability restrictions unchanged.

**Previous execution: D101 CM-tangent exactness, 2026-09-24.**
See [the D101 proof, source review and computation](dembele/certificates/cm-tangent-exactness-d101.md).

**[theory, specialized here]** Marian Aprodu et al.,
[*Koszul modules with vanishing resonance in algebraic geometry*](https://link.springer.com/article/10.1007/s00029-023-00912-4).
The Gaussian-map construction identifies the canonical tangent line
through the sections f_i df_j-f_j df_i. D101 derives the tangent-ratio
formula, its coordinate covariance and the factor 8*z^3 at our coarse
order-two point. The integral and height comparisons are separately
stated hypotheses, not consequences of the map's existence.

**[potential arithmetic input, not yet instantiated]** Roy Zhao,
[*Heights of Special Points on Quaternionic Shimura Varieties*](https://arxiv.org/pdf/2309.08886),
Theorem 1.1 and sections 3–7 (v1, 16 September 2023). The theorem
expresses a maximal-level CM point's arithmetic Hodge height in terms
of CM Faltings heights and discriminants; its finite ramification
hypothesis matches our CM extension and quaternion algebra at 2.
The related PEL/deformation/Kodaira–Spencer construction supplies a
possible arithmetic setting. It does not compute our residue-framed
canonical sections or bound their integral-lattice index.

**[potential arithmetic input; excluded application recorded]**
Xinyi Yuan,
[*Modular Heights of Quaternionic Shimura Curves*](https://arxiv.org/pdf/2205.13995),
section 1.1 and Theorem 1.1 (v3, 26 May 2024), give a modular-height
identity with a specified arithmetic Hodge bundle. The CM-point formula
quoted as Theorem 1.2 requires no common finite ramification of the CM
field and quaternion algebra. D101 proves that hypothesis fails at 2
here, so does not apply that formula. The curve-height theorem remains
a potential input to an additional lattice/metric comparison.

**[context, integral-model normalization]** Ziqi Guo,
[*Modular Heights of Unitary Shimura Varieties II: Arithmetic Generating Series of Divisors*](https://arxiv.org/pdf/2606.18579),
sections 2.2–2.3 and the introductory normalization convention (v2,
23 August 2026). The arithmetic construction uses an auxiliary PEL
RSZ model and normalized intersections. This does not assert that
our original quotient comes with a directly executable PEL equation
or a global section evaluator.

**[our proofs and computation]** D101 gives conditional norm and
projective-height certificates, explicitly retaining their unproved
target hypotheses. The S-unit counterexamples, Gaussian pullback
calculation and 2-Eisenstein test are elementary derivations replayed
by scripts 376–377. Magma 375 and independent Python 376 compute and
check a candidate tangent, not an arithmetic Shimura tangent. No
candidate clearing integer is promoted to an unknown-coefficient bound.
The new source ledger records URLs, reviewed versions and scope; it
does not claim PDF-byte fingerprints or formal proofs of the papers.

**Previous review: D100 methodology and execution readiness, 2026-09-24.**
See [the methodology review](dembele/certificates/construction-methodology-d100.md)
and its [first bounded task](dembele/certificates/construction-methodology-d100.md#7-execution-readiness-first-bounded-task).
The sources below support different steps; none is cited as a complete
implemented construction for our datum.

**[target]** Lassina Dembélé,
[*A non-solvable Galois extension of Q ramified at 2 only*](https://arxiv.org/pdf/0811.4379).
The original residual representations define the desired kernels and
field independently of the later hyperellipticity claim. The degree-257
projective output over F is our use of their faithful action on
P^1(F256), followed by normal closure over Q.

**[theory and our application]** Raymond van Bommel, Edgar Costa,
Bjorn Poonen and Padmavathi Srinivasan,
[*Curve equations from expansions of 1-forms at a nonrational point*](https://arxiv.org/pdf/2506.14026),
Theorem 3.1, Lemma 4.1 and Corollary 4.2. The input is an arithmetic
differential basis with exact expansions. D88 applies the relation
bound to our quadrics: four coarse coefficients suffice because
4*17>60; its three-coefficient alternative also requires rank 45 and
the correct kernel. D100 observes that the divisor proof works over
F as well, given a degree-17 CM residue field and an F-rational frame.
This reformulation is our deduction, not a source-supplied evaluation
algorithm or a proof of those input hypotheses.

**[method adapted, missing exactness distinguished]**
[Nelson, *Evaluating modular forms on Shimura curves*](https://arxiv.org/pdf/1210.1243),
[Voight–Willis, *Computing power series expansions of modular forms*](https://arxiv.org/pdf/1205.0045),
and [Mori, *Power series expansions of modular forms and their interpolation properties*](https://arxiv.org/pdf/math/0406388)
are the analytic-evaluation, CM-algebraicity, and deformation sources
reviewed in D88–D95. The detailed octic-field evaluator and its bounds
are our adaptations. These citations do not supply an effective height
bound or an implemented arithmetic restriction map for this curve.
D100's first execution task addresses that exactness gap before another
large numerical investment; its outcome remains open.

**[method and certification scope]** Nicolas Mascot,
[*Hensel-lifting torsion points on Jacobians and Galois representations*](https://arxiv.org/pdf/1808.03939),
Remarks 1.3–1.5, permits the broader field settings while distinguishing
coefficient recognition from certification. His
[*Certification of modular Galois representations*](https://www.maths.tcd.ie/~mascotn/research/Certification.pdf),
Introduction and section 3, gives a separate certification strategy for
classical modular representations over Q; the stated setup restricts
the coefficient residue degree to one. D100 uses this as a precedent,
not an instantiated certificate for our Hilbert/F256 representation.
The latter paper's title and scope were checked directly for this
ledger update.

**[context, applicability limit]** Hashimoto–Lido–Lombardo–Mascot–Parent,
[*Equationless quadratic Chabauty for non-split Cartan modular curves*](https://arxiv.org/pdf/2608.10919),
section 4.1.6, uses arithmetic moduli evaluations in place of global
curve equations. It does not construct the corresponding quaternionic
section matrices here. Its title and author list were rechecked at the
primary arXiv record.

**[project evidence]** D51 supplies the canonical Jacobian's original
residual kernels; D69/D86/D87 certify candidate geometry and local
lifts; D88 supplies conditional identification criteria; D98 measures
the remaining analytic error; D62–D67 give backend controls. Their
reports are linked from D100. The three open tasks and the execution
order are our assessment. No new arithmetic result is attributed to
these sources or to this documentation update.

**Previous review: D99 hyperellipticity, 2026-09-24.**
See [the fresh proof and evidence ledger](dembele/certificates/hyperellipticity-review-d99.md).

**[theory, reread at the primary sources]**
[Baker, *Specialization of linear systems from curves to graphs*](https://arxiv.org/pdf/math/0701075),
Lemma 2.8, Corollary 2.10 and section 3.1, gives the divisor-rank
specialization without excluding residue characteristic 2.
[Chan, *Tropical hyperelliptic curves*](https://arxiv.org/pdf/1110.0273),
Theorem 1.3 / 3.13 and section 2.2, supplies the metric-graph
involution/tree criterion and the precise quotient convention.
[Kurihara, original scan, section 3, pp. 284--288](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf),
Proposition 3-2 and Lemma 3-3, permits cocompact groups with torsion
over a p-adic field and removes only self-reversing oriented edge
classes. Nekovar's section 1.5.3--1.5.5 independently records the
double-coset graph, rational components and node thicknesses.

**[claim under review]**
[Dembele, *A hyperelliptic Shimura quotient of genus 16*](https://arxiv.org/pdf/1906.06772),
Theorem 5.9, has an invalid inference from an upstairs stabilizer to
vanishing orders on the coarse quotient. Figure 2 is nevertheless
reproduced by fresh Brandt arithmetic and supplies a nonhyperelliptic
reduction graph. D99 does not rely on the admissibility argument of
Proposition 4.7(2) or on tame involution specialization.

**[our derivation and verification]** D99's short edge-cut lemma:
an involution/tree quotient on a graph with at least three vertices
forces an edge cut of size at most two. New script 372 checks all
1,035 possible cuts and separately enumerates the involutions.
The fresh Brandt run still uses the existing HMF library. The
saved-order and candidate checks are explicitly recorded as reruns.
Audit 374 binds 479 sources/artifacts, replays the graph and preserves
the candidate-identification gap. PDF fingerprints are in
`hyperellipticity_sources_d99.json`.

**Previous continuation: D98 spectral ideal bound, 2026-09-24.**
See [the D98 proof and pilot](dembele/certificates/nelson-spectral-ideal-d98.md).

**[theory]** Valentin Blomer and Farrell Brumley,
[*On the Ramanujan conjecture over number fields*](https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p18-p.pdf),
Annals of Mathematics 174 (2011), 581--605, Definition 1 and Theorem 1.
The finite-place exponent 7/64 controls the auxiliary automorphic Hecke
spectrum after Jacquet--Langlands transfer. The target holomorphic form
retains the stronger D93 Ramanujan bound. This produces the new
squared-divisor norm mass; it is not an assumed numerical spectral gap.

**[theory and normalization]** Bourgain--Kontorovich--Sarnak,
[*Sector estimates for hyperbolic isometries*, equation (2.14)](https://www.math.ias.edu/files/avi/Bourgain_Kontrovich_Sarnak.pdf),
supplies the matching hypergeometric K-type coefficient at n=k=2.
[NIST DLMF 15.4.20](https://dlmf.nist.gov/15.4.E20) evaluates its
radial transform. [DLMF 5.15.6 and 5.15.8](https://dlmf.nist.gov/5.15)
give the trigamma reflection and asymptotic identities used with the
minimum principle to prove vertical Gamma log-concavity. The Binet
tail estimate is the same one used in D94.

**[our derivation and computation]** The transformed S11 multiplier,
its lambda+2 cancellation, uniform positive-kernel comparison and
complete omitted-ideal bound are derived in D98. Script 368 evaluates
ten contours with interval rectangles and an explicit infinite tail;
audit 369 replays the rational arithmetic and binds the proof and runs.
The new bound improves D96 by >272.48 but does not certify the CM
anchor. Neither D97's finite-prefix constants nor an unspecified
angular-counting constant is used as an infinite estimate.

**Previous continuation: D97 signed orbital blocks, 2026-09-24.**
See [the D97 report](dembele/certificates/nelson-signed-orbit-d97.md).

**[context, not an instantiated bound]** Jean Bourgain, Alex Kontorovich
and Peter Sarnak, [*Sector estimates for hyperbolic isometries*](https://www.math.ias.edu/files/avi/Bourgain_Kontrovich_Sarnak.pdf),
Theorem 1.1, recording Good's lattice theorem. It identifies the spectral
shape relevant to our two-angle harmonic; numerical constants and
exceptional terms remain unbounded here.

**[method under review]** Alexander Gorodnik and Amos Nevo,
[*Counting lattice points*](https://arxiv.org/pdf/0903.1515), Theorem 1.9,
Corollary 1.11 and Remark 1.12. The translated-count framework needs
quantitative ergodic and geometric inputs before it supplies a numerical
error estimate for this computation.

**[our derivations and calculations]** The exact trace formula for shell
phases, finite Abel summation, derivative remainder interface and uniform
Taylor bounds are derived in D97. Scripts 363/366 use existing D92/D93
classes and D96 scalar blocks. Audit 367 independently replays the
rational arithmetic and binds all prior provenance and the new runs.
The observed finite-prefix constants are not literature constants and
are not extrapolated. No improved actual infinite error bound is claimed;
the complete norm sum and arithmetic CM anchor remain unresolved.

**Previous continuation: D96 completed majorant pilot, 2026-09-23.**
See [the D96 report](dembele/certificates/nelson-completed-majorant-d96.md).

**[method reused]** Nelson's completed-kernel strategy and the D91
Hilbert specialization remain unchanged. The D93 Ramanujan input,
local orbit counts and divisor Euler identity still supply the
positive arithmetic comparison. D95's global identification remains
in force; it is not inferred from the new numerical majorant.

**[our derivations and calculations]** Scripts 360--361 use Taylor
remainders and Bernstein signs to certify 0<K3<K4 and decreasing
K4/A over a finite range. D92's disjoint disks and Stieltjes
integration give an orbit bound. Summing its completed scalar over
the full divisor Euler series cancels zeta_F(2s), leaving two squared
zeta factors and the explicit norm-two correction. This adaptation,
its finite-range splice and numerical fourfold improvement are our
calculations, not a claimed theorem from Nelson's paper. The Gamma
tail uses the Binet bound already cited under D92/D94. No new
external literature result is needed for this pilot.

**[verification and scope]** Audit 362 replays the rational Bernstein
signs, tail polynomial and directed final error assembly. Its saved
finite-family cancellation diagnostics have no extrapolative claim.
The <6.754e12 bound remains far too wide for a CM anchor. The report
records a negative feasibility decision for this positive comparison;
it does not measure the actual omitted sum or rule out methods that
retain signed arithmetic cancellation.

**Previous continuation: D95 global kernel identification, 2026-09-23.**
See [the D95 proof](dembele/certificates/nelson-global-identification-d95.md).

**[theory, specialized here]** Daniel Disegni,
[*The p-adic Gross–Zagier formula on Shimura curves*](https://arxiv.org/pdf/1510.02114),
sections 3.1 and 5.1: the similitude Weil action and general-number-field
Shimizu correspondence. D95 uses the central action
`Phi(x,u) -> Phi(c*x,c^(-2)*u)` and proves its own comparison with
our classical kernel by unfolding rational squares. The cited theorem
supplies the representation-theoretic target and local uniqueness;
our support, level, component and normalization calculations supply
the specialization. No unchecked earlier Tamagawa scalar is imported.

**[theory, components]** John Voight, *Quaternion Algebras* (2021),
[chapter 28, Corollaries 28.5.12 and 28.5.17](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_28):
strong approximation and the norm description of the ideal class set
for an indefinite, locally norm-maximal order. D95 combines this with
the certified narrow class number one to identify the single classical
component; it is not an assumption about a definite quaternion class set.

**[method adapted]** Thomas C. Watson,
[*Rankin Triple Products and Quantum Chaos*](https://arxiv.org/pdf/0810.0425),
sections 2.2.1--2.3: the norm-fibre forward-lift and adjoint strategy.
D95 calculates the norm-one coefficient for our F using D94's explicit
local integrals. Watson's global theorem over Q is not re-labelled as
a general-F theorem; the latter input is Disegni's formulation.

**[convention checked visually]** Paul D. Nelson,
[*Evaluating modular forms on Shimura curves*](https://arxiv.org/pdf/1210.1243),
equation (13), printed page 18: the first quaternionic factor and the
Hilbert form in the integral are conjugated. The rendered saved PDF
was inspected because text extraction drops overbars. Our independent
Cayley-matrix and nilpotent-path calculation confirms that the code's
first derivative index belongs to that conjugated factor.

**[our proof and calculations]** The normalized bump extension,
central square-class unfolding, local-level check, norm-one coefficient,
positive classical scalar and derivative-ratio rule are derived in
D95. Script 358 re-proves class and narrow class numbers with PARI
certification and checks exact field/order and symbolic identities.
Script 359 independently replays the rational parts and binds the
analytic proof. The full series is now identified; useful global
numerical accuracy and a nonzero CM anchor remain unproved.

**Previous continuation: D94 contour review and local nonvanishing, 2026-09-23.**
See [the D94 report](dembele/certificates/nelson-test-vector-and-contour-d94.md).

**[method adapted]** Paul D. Nelson,
[*Evaluating modular forms on Shimura curves*](https://arxiv.org/pdf/1210.1243),
section 5.6, equation (18) and Theorem 5.6: the freedom to choose H
with H(0)=0, H(1)=1. Script 355 tests polynomial multipliers satisfying
the required antisymmetry, using our D91 Hilbert completion. The
changed weights require changed partial sums. This is our adaptation;
Remark 5.1 is not an explicit totally real evaluation theorem.

**[theory, general-field framework]** Daniel Disegni,
[*The p-adic Gross–Zagier formula on Shimura curves*](https://arxiv.org/pdf/1510.02114),
section 5.1, especially (5.1.1)--(5.1.3): Shimizu lifting over a number
field, the local intertwining space and global factorization. The
Schwartz space includes a similitude variable. Our fixed-character
classical kernel still needs an explicit comparison with this setup.
Footnote 31 identifies a normalization issue in an earlier cited
formulation; we do not copy that earlier scalar. The definite real
normalization in this source is not substituted for our split place.

**[method, scope checked]** Thomas C. Watson,
[*Rankin Triple Products and Quantum Chaos*](https://arxiv.org/pdf/0810.0425),
sections 2.2.1--2.3: forward lift by norm fibres, multiplicity-one and
adjointness, and explicit local Schwartz data. The theorem is over Q;
the local norm-one calculation for our degree-eight data is derived
in D94 rather than attributed to a global F theorem in this source.

**[our calculations]** Fractional-contour Gamma bounds reuse Binet's
formula cited under D92. The 28 contour/weight probes, their rational
tail polynomials, and the improved <2.680e13 unchanged-kernel bound
are new computations. The norm-one contractions are calculated on
the actual order and real Gaussians: finite factors 1 and real product
exp(-2*pi) with the stated measures. The dual K-type convention is
essential. Local nonvanishing does not certify the D91 global scalar
or the CM anchor derivative. Script 357 binds the report and inputs;
the global comparison remains open.

**Previous continuation: D93 norm-31 family and global bounds, 2026-09-23.**
See [the D93 report](dembele/certificates/nelson-prime31-and-global-tail-d93.md).

**[theory, coefficient bounds]** Don Blasius,
[*Hilbert modular forms and the Ramanujan conjecture*](https://arxiv.org/pdf/math/0511007),
Theorem 1 and section 2.2. Its finite-place theorem applies to the
parallel-weight-two cuspidal forms here. Together with the Hecke
recurrences it gives `|a_f(a)|<=d(a)*sqrt(Norm(a))` away from p2.
We use it to bound omitted norm ideals, not to identify our Shimizu
test vector or assert nonvanishing at the CM point.

**[tool, endpoint correction]** SageMath,
[MPFR exact rational extraction](https://doc.sagemath.org/html/en/reference/rings_numerical/sage/rings/real_mpfr.html#sage.rings.real_mpfr.RealNumber.exact_rational)
and [simple rational conversion](https://doc.sagemath.org/html/en/reference/rings_numerical/sage/rings/real_mpfr.html#sage.rings.real_mpfr.RealNumber.simplest_rational).
The default QQ conversion of a directed MPFR endpoint can move inward.
Script 351 demonstrates this locally, then replays five analytic stages
with `.exact_rational()`. The corrected `*_exact_d93.json` exports and
354 final audit supersede the original analytic endpoint exports.
This correction leaves the reported bounds unchanged at displayed
precision; no outward guarantee is inferred from the old conversions.

**[our calculations]** Positive fixed-norm majorants, exhaustive
coverage, the exact quotient `O/nO=M2(F31)` and its 32 image lines,
and the transfer of the disk bound to right norm-one orbits. Local
rank-two Hermite-form counting gives the sigma_1(a) orbit upper bound;
a positive disk average gives the whole-orbit moment. The Euler identity
for d(a)*sigma_1(a) and the resulting all-ideal majorant are derived
in D93. No class-number/principal-ideal assumption is used to turn
this upper bound into an equality. The bound proves convergence of
the D91 expression but does not give useful full-form accuracy.
Nelson, D91 quadrature theory and D92 disk estimates are reused within
the scope recorded below; no explicit totally real theorem is claimed
from Nelson's paper.

**Previous continuation: D92 complete norm-one control, 2026-09-23.**
See [the D92 report](dembele/certificates/nelson-norm-one-control-d92.md).

**[tool, guarantee checked]** The PARI/GP
[`qfminim` documentation](https://pari.math.u-bordeaux.fr/dochtml/html-stable/Vectors__matrices__linear_algebra_and_sets.html#qfminim)
explains flag 0's integer-size restriction and flag 2's lack of rigorous
roundoff tracking. Script 338's flag-0 failure is preserved; 339 uses
flag 2 at 256 bits. Exhaustiveness comes from our separate script 340:
exact rational LDL, outward Arb branch bounds and exact leaf tests.
It is not inferred from checking only PARI's returned vectors.

**[analytic theory]** NIST Digital Library of Mathematical Functions,
[Binet's formula (5.9.10_2)](https://dlmf.nist.gov/5.9.E10_2), supplies
the log-Gamma remainder integral. Script 341 uses the derived bound
|R(c+it)|<=1/(12c) for an explicit exponential vertical-tail majorant.
Arb interval rectangles bound the finite absolute Gamma integrals;
the D91 quadrature and zeta implementation are reused unchanged.

**[our calculations]** Unit-signature rank 8 permits exact norm-one
normalization. The anisotropic fixed-norm majorant, complete cutoffs,
and positive angular disk-average tail argument are proved in D92.
The 129-term binomial lower sums and algebraic-power bounds are
independently replayed with rational arithmetic. Nelson motivates the
evaluation method; these computations are not attributed to an explicit
totally real theorem in his paper. The result bounds one infinite
norm-one family and does not identify a global lift or CM tangent.

**Previous continuation: D91 Hilbert unfolding and partial evaluation,
2026-09-23.** See [the D91 report](dembele/certificates/nelson-hilbert-unfolding-d91.md).

**[method adapted]** Paul D. Nelson,
[*Evaluating modular forms on Shimura curves*, arXiv v1](https://arxiv.org/pdf/1210.1243v1),
sections 5.2--5.6 and Appendix A: theta normalization, residue-one
Eisenstein unfolding, cusp Fourier transforms and the rational Bessel
calibration. Our totally real Gamma product, argument, exact beta-dual
identity, central-unit classes and interval partial sums are adaptations
and new calculations, not a theorem quoted from Remark 5.1. Direct
derivative calibration detects an absolute-X scale discrepancy in a
literal reading of display (11); the implementation follows the checked
Gaussian derivatives. The 2015 publisher PDF returned HTTP 403, so no
claim about that version's display is made.

**[theory, normalization]** Riad Masri,
[*CM cycles and nonvanishing of class group L-functions*](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806604636373020674-1806604636373020674-6e788fc744157b0b48d40b90be793f0e.pdf),
Math. Res. Lett. 17 (2010), 749--760, section 2: the Hilbert Eisenstein
constant term, completion and functional equation. For this degree-eight
class-number-one field they give completed residue 64*R_F. This fixes
the unfolding normalization; it does not identify our theta test vector.

**[theory, scope checked]** Haruzo Hida,
[*Anticyclotomic Main Conjectures*](https://www.emis.de/ft/9824),
Documenta Math., Extra Volume Coates (2006), 465--532, section 3.1:
cusp stabilizer and integration modulo unit squares. Section 5.3,
Proposition 5.2 and its discussion point to quaternionic matrix
coefficients and Shimura, *On certain zeta functions attached to two
Hilbert modular forms II*, [Annals 114 (1981), 569--607](https://annals.math.princeton.edu/1981/114-3/04).
The original Shimura theorem was not read in full; a nonzero global
identification for our exact Schwartz function remains unproved here.

**[numerical theory]** Lloyd N. Trefethen and J. A. C. Weideman,
[*The Exponentially Convergent Trapezoidal Rule*](https://people.maths.ox.ac.uk/trefethen/publication/PDF/2014_149.pdf),
SIAM Review 56 (2014), 385--458, section 5 and equation (5.15): contour
error bound from the two strip boundaries. Script 333 combines it with
an explicit polynomial Gamma majorant and a vertical-tail bound. Arb
balls in Sage enclose the nodes and algebraic inputs. The interval
certificate covers a finite primitive subset, with the auxiliary ideal
sum and beta strings completed; it does not bound omitted classes.

**[our calculation, feasibility]** Explicit cyclotomic units and an LLL
change give a proved central-unit cover constant 2126 in script 336.
The resulting full 32-dimensional ellipsoid is too large to enumerate.
The hyperbolic-displacement reformulation is the next algorithmic lead.
The nine bounded jobs, exact arithmetic replay, source discrepancy and
remaining matched-Hecke/test-vector requirements are recorded in D91.

**Previous continuation: D90 Nelson kernel components, 2026-09-23.**
See [the implementation report](dembele/certificates/nelson-totally-real-kernel-d90.md).

**[method adapted, local implementation]** Paul D. Nelson,
[*Evaluating modular forms on Shimura curves*](https://arxiv.org/pdf/1210.1243),
sections 3.2--3.5, 5.1--5.2 and Appendices A--B. Scripts 320--326
implement and check the derivative polynomials, disk conversion,
CM lattice decomposition and Fourier-dual normalization for our saved
quaternion order. The rational Bessel identity independently calibrates
a scalar Mellin prototype. The different generator, four-element finite
quadratic module, 65,536 CM cosets and rational majorant bounds are our
explicit calculations over F. The compact real factors lead to a
different Gamma product from eight split factors. The Hilbert
cusp/unit unfolding and global normalization remain unproved here;
Remark 5.1 explicitly defers the totally real application. No global
lift, exact CM derivative, or curve identification is attributed to D90.

**Previous continuation: D89 CM tangent input audit, 2026-09-23.**
See [the local arithmetic report](dembele/certificates/cm-tangent-local-arithmetic-d89.md).

**[theory, scope checked]** [Andrea Mori, Proposition 3.3 and Theorem
3.6](https://arxiv.org/pdf/math/0406388) provide ordinary deformation and
derivative comparisons in the stated modular/quaternionic setting over
Q. They presuppose the modular forms and test objects. The application
to our real-octic datum and the section evaluator remain unconstructed.
The order-two invariant-coordinate and differential-ratio formulas in
D89 are direct local deductions, checked with rational arithmetic.

**[context]** Frederick Saia, [*CM points on Shimura curves via
QM-equivariant isogeny volcanoes*, sections 3–4](https://arxiv.org/pdf/2212.12635),
describes horizontal and conductor-changing isogenies over Q. D89 proves
its needed local statement directly for R-lattices and checks all 32
lines over F31; no global CM census over F is attributed to that paper.

**[method investigated]** [Nelson, section 3.4 and Remark 5.1](https://arxiv.org/pdf/1210.1243)
supplies explicit analytic derivative evaluation in the rational case
and leaves the totally real application for further work.
[Haruzo Hida, *Anticyclotomic Main Conjectures*, sections 4–5](https://www.emis.de/ft/9824)
gives CM-value and integral theta-correspondence results for specified
lifts. Neither source is used to claim an exact arithmetic tangent or
an identification of the candidate's canonical multiplication.

**Previous continuation: D88 identification reviews, 2026-09-23.**
See [the CM-expansion review](dembele/certificates/d88-cm-expansion-identification-review.md)
and [the cubic-shortcut review](dembele/certificates/d88-cubic-identification-shortcut-review.md).

**[theory, re-audit]** Raymond van Bommel, Edgar Costa, Bjorn Poonen and
Padmavathi Srinivasan, [*Curve equations from expansions of 1-forms at a
nonrational point*, Theorem 3.1, Lemma 4.1 and Corollary 4.2](https://arxiv.org/pdf/2506.14026).
The input is exact expansion data for a ground-field differential basis.
Our order-four criterion is the specialization 4*17 > 2*(2*16-2).
Lemma 4.3's distinction between hyperelliptic and nonhyperelliptic
quadratic-product dimensions yields our sharper three-term criterion
when the truncated matrix has rank 45. The new candidate diagnostic
certifies that rank; it does not supply independent arithmetic jets.
The period-free projective-ratio interface and degree-one comparison
with D69's curve are local deductions. The paper does not compute our
missing Shimura-side jets.

**[context, investigated rather than implemented]**
[Voight–Willis](https://jvoight.github.io/articles/ModFormPaper-090317.pdf)
provides CM algebraicity and numerical expansions, with rigorous
approximation left open. Andrea Mori's [*Power series expansions of
modular forms and their interpolation properties*](https://arxiv.org/abs/math/0406388)
relates ordinary CM deformation to normalized derivatives. Paul D.
Nelson's [*Evaluating modular forms on Shimura curves*](https://arxiv.org/abs/1210.1243)
gives a convergent analytic evaluation method. None supplies a ready
exact arithmetic section-restriction implementation for our real-octic
quaternionic datum. A formal parameter alone is insufficient.

**[theory, reused]** [Multiplication by three is étale away from three](https://stacks.math.columbia.edu/tag/0BFH)
and [étale sections lift uniquely across nilpotent thickenings](https://stacks.math.columbia.edu/tag/06NE).
Applied to the fixed smooth marked Jacobian, these justify the local
uniqueness step in the conditional cubic comparison. Prym 3-torsion,
global branch orientation, and removal of constant Kummer twists are
proved directly in the review from the norm identities and coprime
field degrees. The saved canonical Hecke data and D84's exact nine-cover
checks supply the conditional counting input; their transfer to the
candidate still requires marked arithmetic identification.

**Previous continuation: D87, 2026-09-23.**
See [the double-cover character comparison](dembele/certificates/cm-frame-double-cover-character.md).
The new numerical calculation compares the rational double cover with
the signs of all 277 saved quaternionic S3 images, using both saved
differential banks and a second path family. All signs agree; this does
not certify the analytic input or identify the selected cubic class.

**[tool, reused]** Rickards's pinned fundamental-domain code supplies
the ordered side elements and disk actions. Inspection of `afuchelts`,
`afuchactions` and their shared boundary construction checks the ordering
used by scripts 66/67. The exact S3 calculation is the existing local
division-algebra reduction, not a new monodromy computation by Rickards's
package. The source and citation appear in its entry below.

**[tool, local numerical method]** The existing FLINT interface supplies
complex-ball polynomial arithmetic. New scripts 307/312/315 form full
quadratic pullbacks, evaluate derivatives and rigorously bound omitted
tails of those finite polynomials. Adaptive square-root continuation,
the altered paths and independent argument accumulation in 318 are local
implementation work. No FLINT arithmetic radius is used as a bound for
the geometry or infinite differential expansion. The report records the
rejected midpoint and under-resolved path attempts.

**[theory, retained]** D77's [normalized fibre and inertia argument](dembele/certificates/cm-frame-B3-fiber.md)
already proves uniqueness of the F-scalar twist for the fixed branch
half. Its tame inertia input and odd-degree norm argument remain in
force. The present complex signs cannot see constant twists; after a
certified marked comparison, that existing condition would select the
arithmetic double cover. No new twist search or descent theorem is claimed.

**[context, re-audit]** [Dembélé, Theorem 4.1 and Lemma 5.2](https://arxiv.org/pdf/1906.06772)
were checked for the canonical level-map and maximal-level descent
statements. They do not identify the reconstructed curve or third.
The hyperellipticity conflict remains as in D85. Root 318 verifies 2,187
hashes / 875 JSON records; the unchanged D86 audit also passes.

**Previous continuation: D86, 2026-09-23.**
See [the Châtelet lift and reconstruction report](dembele/certificates/cm-frame-cubic-128-chatelet.md).
Scripts 298–300 reuse
[the repository's CoCalc client](remote_magma/cocalc.py) and
[Châtelet operational notes](remote_magma/CHATELET.md), including the
warning that detached children inherit the API CPU limit. The new worker
sets explicit CPU/wall/memory bounds and preserves hashed mathematical
inputs and outputs. The user explicitly authorized the mathematical
uploads; credentials and unrelated files were excluded. Both cubic
forms are independently verified at 128 digits, with 64-digit compatibility
and all highest-digit error controls. All 21 remote jobs have finished.
Adapters 304/305 resume hash-checked transfers after transient connection
failures without changing the guarded job launch or mathematical sources.

**[method, existing implementation]** Joint projective recognition uses
259's same rank-200 lattice and exact 25-dimensional rational A2 space,
with 112 training / 16 validation digits. It is negative at all eight
embeddings, while known-F and unused-digit error controls pass. Sage
jobs run locally through process-group runner 272/274. Adapter 301
extends 271's scaled-inverse height certificate, and 303 independently
checks `B*K=31^112*I` with integer arithmetic. The uniform excluded height
is 348,750,355,384,078 in the fixed bases. The bound is the elementary
matrix inequality documented in the report, not a new external theorem
or an intrinsic height estimate. No coefficient-field exclusion,
descent or arithmetic-identification claim is added; the D85 source
review below still governs those issues. Root 303 verifies 2009 file
hashes / 769 JSON records.

**Previous continuation: D85, 2026-09-22.**
See [the bounded 128-digit attempt and review](dembele/certificates/cm-frame-cubic-128-review.md).
The attempt extends the existing Khuri-Makdisi arithmetic and idempotent
lift. Local implementation changes schedule Newton inversion by precision,
release temporary matrices, and bound multiplication workspaces. Native
Magma controls pass, but the actual-divisor construction reaches the
memory/time limits. No 128-digit cubic or recognition result is obtained.
The [Magma matrix handbook](https://magma.maths.usyd.edu.au/magma/handbook/matrices)
was consulted for matrix operations; the precision and memory scheduling
are local implementation work, not an attributed new upstream algorithm.

**[theory]** [Stacks, Proposition 39.9.11](https://stacks.math.columbia.edu/tag/0BF9)
gives geometric n-torsion of rank 2g when n is invertible.
The pullback/norm identities for this double cover give invariant
3-torsion dimension 32 and anti-invariant dimension 48. The resulting
3^48 geometric third count is a local deduction from those identities,
not a computed global Galois orbit or coefficient-field degree.
[Étaleness](https://stacks.math.columbia.edu/tag/0BFH) and
[nilpotent lifting](https://stacks.math.columbia.edu/tag/06NE) distinguish
unique local lifting from global definition over F.

**[theory, re-audit]** [Sijsling–Voight, Theorems 1.3.2 and 3.2.4](https://jvoight.github.io/articles/birch-descent-021420.pdf)
descend a map with a smooth source marking to its existing field of
moduli. They do not determine that field for the selected third.
The elementary calculation N_S3(C2)=C2, checked by 296, shows that
the cubic has no automorphisms over the fixed base; unique comparison
maps then satisfy the Weil cocycle once their existence is proved.
The present normalization's field preservation follows directly from
its unique linear spaces and lambda=sqrt(-3)*a0/h0, conditionally on the
required global class action. No height bound follows.

**[context, re-audit]** [Dembélé, Lemma 5.2 and Theorem 5.9](https://arxiv.org/pdf/1906.06772)
were reread to separate the earlier descent lemma from the disputed
hyperellipticity argument. D58's marked maximal-level descent and
D62's graph/group audit remain the relevant local reports. Extending
canonical conjugation to the reflection level is a proposed comparison,
not a completed identification or a new Q-descent theorem.

Script 296 uses exact Sage number-field arithmetic to check the
illustrative local root of x^2−5, which is not in F, and finite S3
calculations. This supplies no coefficient-field candidate. Runner 297
binds successful preparations, failed jobs, review checks and frozen
prior provenance. No new M23 method, external communication or global
arithmetic identification is claimed.

**Previous continuation: D84, 2026-09-22.**
The [structural checkpoint](dembele/certificates/cm-frame-structural-checkpoint.md)
uses the existing Khuri-Makdisi evaluation arithmetic to construct two
independent rational anti-invariant 3-torsion classes. The identity
3(A+T)=-Delta and its converse show that compatible thirds form a torsor
under this kernel; this is a local elementary deduction. The cofactor
suggested by Hecke data remains a search aid, with actual orders and
symmetries verified independently and no group order assumed.

[Stacks, Kummer theory](https://stacks.math.columbia.edu/tag/03PK)
supplies the relation between torsion line bundles with trivializations
and cyclic covers. Runner 279 adapts the frozen D79/D80 constructors and
verifiers to nine thirds; cached, certified base point lists support
independent normalized fibre counts. The original choice alone matches
both Hecke predictions in this subgroup. This does not prove an exhaustive
census or a Fuchsian monodromy match. The intrinsic arithmetic S3 map
remains the one computed from the quaternionic order in script 66.
[Étaleness of multiplication](https://stacks.math.columbia.edu/tag/0BFH)
and [unique nilpotent lifting](https://stacks.math.columbia.edu/tag/06NE)
explain why successful lifting does not by itself select the correct third.

Script 275 calibrates the existing Sage LLL projective-recognition method
with 67 synthetic exact F-points; 280 independently checks exact recovered
projective identities using integer polynomial arithmetic. The reported
10^7 / 10^9 / 10^18 example heights at the three tested precision splits
are empirical findings, not height bounds or uniform algorithm guarantees.
All 128-digit examples are synthetic; the actual cubic stays at 64 digits.
No new upstream algorithm, M23 attribution or global coefficient-field
claim is introduced. Runner 281 binds the complete new checkpoint and
the frozen prior certificates.

**Previous continuation: D83, 2026-09-22.**
The [64-digit experiment](dembele/certificates/cm-frame-cubic-64.md)
uses the same D82 arithmetic, normalization and recognition arguments.
Runner 261 extends only orchestration; 262/264–269 introduce bounded
stages for construction and verification. The direct degree-zero search
for u imposes its known WB4 condition from the start; full function-space
inclusions and the independent checker verify the same divisor identity.
This is local linear algebra in the existing Khuri-Makdisi framework,
with no new group-order assumption or upstream dependency.
Held-out digits remain a diagnostic, not an exact equation
certificate. D82 source and data hashes remain frozen.

Script 271's height exclusion is the elementary inequality obtained
from the exact identity B*K=31^60*I; 263 independently checks the saved
integer matrices. It bounds integral homogeneous coefficients in the
specified bases, including a common F-valued scale. This is a local
deduction, not a claim of a general Weil-height bound or field exclusion.
Sage supplies the exact inverse. The reviewed
[Gram-Schmidt interface](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.gram_schmidt)
was used only by the archived timeout diagnostic 270; its late child
output is excluded. Scripts 272–274 correct and test process-group
timeout handling for future recognition jobs. No new mathematical
assumption, upstream code import or remote computation is introduced.

**Previous source audit: D82, 2026-09-22.**
See [the cubic precision report](dembele/certificates/cm-frame-cubic-precision.md).
Khuri-Makdisi's evaluation/section framework remains the arithmetic base.
Scripts 195/202 implement a local 80-coordinate gauge; its unit derivative
and complementary-divisor corrections are local calculations. The
[Stacks nilpotent-lifting theorem](https://stacks.math.columbia.edu/tag/06NE)
explains uniqueness of that local lift, not preservation of the global
coefficient field. The unique 80P divisor chart supersedes this gauge
for class arithmetic. Riemann–Roch and a measured rank-80 condition give
a unique representative without additional algebraic choices.

Scripts 208–213/226 adapt the explicit idempotent Newton polynomial
**3e²−2e³** from
[Stacks, Lemma 10.32.6](https://stacks.math.columbia.edu/tag/00J9).
The section zero algebra and its rank-120 summand are local work.
Scripts 227–231 use square-zero linear interpolation in the unique
pointed divisor chart; the first-order Taylor formula and the
Riemann–Roch criterion for the Abel map to be étale justify the step.
The actual-divisor certificate, direct class checks and comparisons
with scalar routes are local implementations. No group order is inferred.

The separate K_X+2P output normalization, the degree-four equation,
its orientation-compatible leading terms, and both explicit cover
isomorphisms are local deductions (249–257). They are not attributed
to an unverified step in the M23 paper. Scripts 254/255 construct an
exact rational Riemann–Roch coefficient space, then use Sage's integer
lattice saturation and LLL. Scripts 258/259 adapt the existing D74/D75
recognition methods, especially a common F-valued projective scale,
and reserve unused digits; no finite-precision relation alone is an
exact field or curve certificate.

[Magma's Galois-ring interface](https://magma.maths.usyd.edu.au/magma/handbook/text/606)
supports lifted point arithmetic; its
[multivariate monomial API](https://magma.maths.usyd.edu.au/magma/handbook/text/246)
provides Exponents in the exact quadratic-space calculation. No new
upstream code, remote jobs or external messages are introduced.

Previous source audit: **D81, 2026-09-22.** See
[the first cubic lift](dembele/certificates/cm-frame-cubic-lift.md).
Scripts 184–194 implement and independently verify the cubic modulo
961. Khuri-Makdisi supplies the evaluation/section-arithmetic framework;
the adaptation to unit pivots over the finite ring, lifted support
bases, checkpoint schedule and coefficient normalization are local work.
[Magma's Galois-ring documentation](https://magma.maths.usyd.edu.au/magma/handbook/text/606)
specifies the point arithmetic. Dense products use our matrix-pair
implementation over Z/961, checked against native ring operations.
The earlier Stacks étaleness and nilpotent-lifting references explain
uniqueness with a chosen reduction; they do not select the arithmetic
third. The scalar c2 is now executed and the class relation checked
directly. No group order, number-field reconstruction or arithmetic
identification is inferred. The proposed persistent 80-coordinate
representative gauge remains to be implemented.

Previous source audit: **D80, 2026-09-22.** See
[the cubic Frobenius report](dembele/certificates/cm-frame-cubic-frobenius.md).
Scripts 180/182 count normalized fibres using the explicit D79 cubic,
its quadratic resolvent and Kummer function. The implicit local-series
calculations and independent coordinate choices are local work;
[Stacks, Kummer theory](https://stacks.math.columbia.edu/tag/03PK)
supplies the unit-root framework. The comparison uses the existing
script-58 Hecke bank and script-64 old-plus-new prediction, not a new
Hecke computation. Agreement of 68/2818 points is two power traces at
one prime, not a full Euler factor or identification theorem.
For the next-step scalar deduction, [Stacks, Lemma 39.9.9](https://stacks.math.columbia.edu/tag/0BFH)
gives the multiplication-by-three differential/étaleness criterion,
and [Theorem 41.15.1](https://stacks.math.columbia.edu/tag/06NE) gives
unique lifting across nilpotent thickenings. The formula c2=31c+10
uses our verified annihilator and the square-zero reduction kernel;
it is a local deduction, not a computed class lift or a group-order claim.

Previous source audit: **D79, 2026-09-21.** See
[the explicit cubic-cover report](dembele/certificates/cm-frame-cubic-cover.md).
Khuri-Makdisi's evaluation/section arithmetic supports the exact
moving-divisor and function calculations. The representative descent,
norm scalar 27, reflection quotient and saved cubic coefficients are
our computations, checked separately. [Stacks, Kummer theory,
section 59.28](https://stacks.math.columbia.edu/tag/03PK) supplies the
unit-root and line-bundle framework; [section 53.12, Riemann–Hurwitz](https://stacks.math.columbia.edu/tag/0C1B)
supplies the tame genus calculation. These uses establish a genus-64
curve over F31 on the candidate base, not its arithmetic identification
or characteristic-zero lift. Two deliberately corrupted inputs fail.

Previous source audit: **D78, 2026-09-21.** See
[the genus-40 class-arithmetic report](dembele/certificates/cm-frame-cover-class-arithmetic.md).
The exact section construction and branch evaluations are local work
using the existing rational cover. Khuri-Makdisi's
[evaluation representation and section arithmetic](https://arxiv.org/pdf/math/0409209)
provide the framework; the concrete negation/chord schedule is adapted
from Mascot's pinned LiftTors `pic.c`. Magma finite-field matrices
replace the slow native probe without changing upstream code.
Riemann–Roch dimensions and full checks of surviving degree-zero
sections make the acceptance exact. The Hecke-derived order only
suggests a scalar; an independent saved-relation check verifies the
third without it. Neither a class number, a Kummer function, nor an
arithmetic monodromy identification is inferred from these references.

Previous source audit: **D77, 2026-09-19.** See
[the normalized B3 fibre report](dembele/certificates/cm-frame-B3-fiber.md).
The local jets, explicit square witness, rational parameter and
oriented branch data are our exact computations. Magma supplies
number-field square roots and independent polynomial checks.
[Stacks, Lemma 15.114.5](https://stacks.math.columbia.edu/tag/09EE)
supplies the tame inertia character: total ramification in a constant
cyclic cubic forces mu3 into the residue field. The ensuing unique
F-scalar twist restriction uses the local odd-degree norm argument;
it neither identifies the branch half nor constructs the cubic.
[Alexeev–Pardini, §1.1](https://arxiv.org/pdf/1102.4184) supplies the
eigensheaf framework for the double-cover pushforward used with our
rank and vanishing certificates to prove D+-D- nonprincipal.
The [Kummer sequence](https://stacks.math.columbia.edu/tag/03PK)
explains the remaining divisor-class and scalar choices, not an
implemented 3-division algorithm or an arithmetic monodromy match.

Previous source audit: **D76, 2026-09-18.** See
[the rational double-cover certificate](dembele/certificates/cm-frame-rational-double-cover.md).
The multiplication-kernel lift h*q=g*s, six-space congruence lattice,
and explicit cubic-polar/two-jet Veronese splitting are local
constructions. Sage supplies exact finite-ring/rational linear algebra
and LLL; Magma independently checks polynomial identities and divisor
ideals. The [Magma linear-systems example](https://docs.magma-maths.org/AlgebraicGeometry/Schemes/introduction.html#linear-systems)
gives the standard six equations of the second Veronese embedding;
no general surface-parametrization routine is invoked here.
The rational divisor proof combines the earlier good model with
[relative Cartier divisors](https://stacks.math.columbia.edu/tag/056P),
[reduced special fibre over a DVR](https://stacks.math.columbia.edu/tag/0574),
properness, exact membership witnesses and a square-product identity.
These give an exact rational genus-40 cover on the candidate C.
The recorded local scalar is checked through 31^128; arithmetic
Shimura identification and the global twist remain open. M23's prior
role is reduction modulo curve relations, not the new splitting method.

Previous source audit: **D75, 2026-09-18.** See
[the joint recognition and B3 report](dembele/certificates/cm-frame-joint-field-and-B3-normalization.md).
Joint F recognition, its exact inverse-matrix coefficient-box bound,
and the B3 auxiliary-divisor change are local constructions. Sage's
integer-matrix interface supplies LLL, kernels and exact inverses;
Magma verifies the saved lattices, field control and square-factor map.
The rational residual certificate uses the Stacks Project's
[relative Cartier divisors and their differences](https://stacks.math.columbia.edu/tag/056P)
and [reduced special fibre over a DVR, Lemma 37.26.6](https://stacks.math.columbia.edu/tag/0574),
applied to the previously certified good model and flat marks.
The numerator has height 583, but its denominator and square factor
are only transferred modulo 31. No arithmetic cover follows from the
failed field-recognition searches. M23 motivates the prior reduction
modulo curve relations; this new divisor choice is not attributed to it.

Previous source audit: **D74, 2026-09-18.** See
[the precision-doubling report](dembele/certificates/cm-frame-precision-doubling.md).
The local Newton derivation extends D72's exact étale-support method;
no additional geometric theorem is claimed. Sage's rational
reconstruction and integer-matrix documentation supplies software
interfaces for bounded recognition, LLL and saturation checks. The
unused-digit validation, whole-quadric congruence lattice and exact
17-dimensional complementary-divisor space are local constructions.
Independent Magma checks certify the 128-digit lift, unchanged ratio,
and reduced rational section identities. No field recognition is
claimed from unsuccessful searches or finite-precision fitting.

Previous source audit: **D73, 2026-09-18.** The user's M23 suggestion
prompted a fresh reading of §3 and Zhang's companion account. See
[the normalization report](dembele/certificates/cm-frame-normalization.md)
for the source-to-implementation distinction. Our integer-kernel/LLL
adaptation reduces the numerator from 631 to 39 digits. Sage supplies
exact lattices and Smith invariants; Magma certifies the transferred
ratio modulo 31^8. The transfer argument and local certificates are
our computations, with no claim to implement unpublished M23 code.

Previous source audit: **D70, 2026-09-18.** The
[marked-divisor report](dembele/certificates/cm-frame-marks.md) uses
Magma's residual-divisor ideal construction and the Stacks Project's
cohomology semicontinuity to exclude a proposed branch-divisor relation.
The nonic Galois group is followed by a successful `GaloisProof` call.
Dembélé's order-three CM class-number calculation supplies context,
not an identification of the computed residue field. Voight–Willis
and the new Guillemot–Voight verification paper are reviewed for the
still-missing independent Shimura identification. The latter verifies
specified Belyi maps/passports; it is not run here. Rational-point
recognition, implicit ordinarity jets and the seven hyperplanes are
local computations, not results attributed to those papers.

Previous source audit: **D69, 2026-09-18.** The
[curve-verification report](dembele/certificates/cm-frame-verification.md)
uses the Stacks Project's finite locally free trace discriminant,
normality/smoothness criterion for curves over perfect fields, and
flat-fiber smoothness criterion. A local index-squared argument and
the computed free Gröbner basis turn these into an exact certificate
for D68's curve. Direct counts over F31 and F31² agree with the saved
Hecke predictions. The vBCPS nonrational-point vanishing bound supplies
a sufficient next identification criterion; the required independent
arithmetic Shimura-side jets are not yet available. Smoothness is now
proved, while Shimura identification and the field remain open.

Previous source audit: **D68, 2026-09-18.** The user's M23/Belyi/17T7/HMF
suggestions are assessed in
[the curve-construction review](dembele/certificates/curve-construction-sources-2026-09-18.md).
M23 supplies the geometry-to-coordinates template; KMSV supplies
canonical reconstruction from differential products. The 17T7
period/invariant reconstruction is genus four, and the HMF Fourier
ring does not itself supply the quaternionic curve's multiplication.
The van Bommel–Costa–Poonen–Srinivasan algorithm explicitly assumes
arithmetic differential input. These distinctions prompted a local
projective-frame/residue adaptation using all seventeen CM points.
It is not an algorithm attributed to the cited papers. Scripts 114–116
produce 91 integer candidate quadrics and verify their degree,
arithmetic genus and CM point; smoothness and Shimura identification
remain open. Source hashes, primary links and local worktree status
are saved in `curve_construction_sources_20260918.json`.

Previous source audit: **D67, 2026-09-17**. The
[allocation report](dembele/certificates/lifttors-allocation.md)
traces the preserved lifting, divisor and linear-algebra implementations
without changing their arithmetic or reclamation points. It identifies
an obsolete product workspace retained through group operations and
selects explicit cleanup changes to test. Instrumentation, exact
tracing comparisons and lifetime analysis are local work. PARI stack
checkpoints and object-tree sizes are distinguished from peak memory;
no new geometric or descent theorem is invoked.

The D66
[degree-51 and reduction report](dembele/certificates/lifttors-degree51.md)
checks the pinned `RRspaceEval`, `RREvalInit`, `RREval`, `PicRed` and
`FpXM_red` against their actual data shapes. It finds and locally fixes
an auxiliary-table reduction defect, with independent modular arithmetic
and projective evaluation checks. The genus-16/degree-51 calibration,
correction and conditional component-storage projection are local work;
no new geometric or descent theorem is invoked.

The D65
[native row-generation report](dembele/certificates/lifttors-rows.md)
implements D64's identity in C, retaining the pinned and D63 lifting
paths for comparison. The selected-row argument and complete residual
verification are local work. No new geometric or descent theorem is
invoked, and target arithmetic section construction remains missing.

The D64
[residue-degree calibration](dembele/certificates/lifttors-extension.md)
checks the pinned implementation's extension construction, Frobenius
orbits, Schur derivative and flattening order. A genus-4 lift passes at
degree 51. The row-generation identity, exact prototype comparisons and
conditional storage projections are local work; PARI's object-size
documentation fixes the meaning of the measurements. No genus-64/a=51
control or target arithmetic construction is claimed.

The D63
[lifting memory audit](dembele/certificates/lifttors-memory.md) traces
the actual pinned C implementation, adapts its product scheduling and
kernel allocation, and checks those adaptations against the original.
PARI's library manual supplies the stack-management API; the memory
changes and their all-equations verification are local work.
The genus-64 control now passes under the unchanged 2 GB stack cap at
residue degree two; it does not establish genus-64/a=51 feasibility.

The D62
[curve-identification audit](dembele/certificates/curve-identification-audit.md)
checks Kurihara's original integral quotient theorem and Nekovář's
uniformization description against the saved quaternion and Brandt data.
It supports D45's identification; no external resolution of the published
hyperellipticity conflict is claimed. Mascot's actual LiftTors software
is used in [the D62 backend controls](dembele/certificates/lifttors-control.md):
genus-2 end-to-end and genus-16 lifting controls passed, while genus 64
then failed at the stated stack limit. The exact batched validator is our local
adaptation, compared with the retained upstream routine. The
[section interface](dembele/certificates/arithmetic-section-interface.md)
specifies D0=pi^*(43P); it does not supply an arithmetic construction.

The D61
[strategic stocktake](dembele/certificates/stocktake-2026-09-16.md)
rechecks Mascot's arithmetic input requirements, Dembélé's descent lemma
and Sijsling--Voight's marked-map theorem. This confirms the distinction
between descent, CM restrictions and usable Jacobian data; it does not
provide a new quaternionic section-evaluation algorithm or resolve the
published hyperellipticity conflict afresh. The D60
[evaluation-space height report](dembele/certificates/cm-flag-height.md)
uses LLL and exact Gram--Schmidt arithmetic, then derives an exterior-power
bound excluding rational subspaces inside empirical coordinate boxes.
The proof is written in the report; neither the cited lattice literature
nor the computation certifies analytic target membership in those boxes.
The D59
[CM orbit report](dembele/certificates/cm-orbit-recognition.md) applies
Shimura reciprocity in Voight's explicit ideal convention to label the
saved embeddings. Magma's Galois documentation specifies the distinction
between the proved p-adic group and the complex-root comparison.
No exact target function value is obtained. The D58
[marked descent report](dembele/certificates/marked-descent.md) applies
Sijsling--Voight to the canonical cover with its distinguished CM point.
It recovers Dembélé's earlier Lemma 5.2, independent of hyperellipticity,
which D57's audit overlooked. No explicit descent matrices are computed.
The earlier
[CM arithmetic-input audit](dembele/certificates/cm-arithmetic-input-audit.md)
checks the distinction between an exact CM residue algebra and evaluations
of the particular functions. It uses the published CM class-field data
and Elkies's polynomial, and checks the input requirements of CM-norm
formulas over Q and totally real fields. No cited formula has been
applied to evaluate D56's target functions.

## The problem and its history

- **A. Kurihara**, *On some examples of equations defining Shimura curves
  and the Mumford uniformization*, J. Fac. Sci. Univ. Tokyo Sect. IA Math.
  25 (1979), 277–300,
  [institutional original](https://repository.dl.itc.u-tokyo.ac.jp/records/39680),
  [scanned PDF](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf).
  **[theory, D62]** Section 3, Proposition 3-2 and Lemma 3-3, pp. 284–288,
  were inspected in the original scan. They treat discrete cocompact
  groups with torsion and the local quotient interchanging two components,
  without an odd-residue-characteristic hypothesis. The graph operation
  removes self-reversing oriented-edge classes, not arbitrary loops.
  This is the geometric bridge in `curve-identification-audit.md`.
- **J. Nekovář**, *Level raising and anticyclotomic Selmer groups for
  Hilbert modular forms of weight two*, Canad. J. Math. 64 (2012), 588–668,
  [publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2A11114CBB9FC75C2DBF56F766BFE7BF/S0008414X00009196a.pdf/level-raising-and-anticyclotomic-selmer-groups-for-hilbert-modular-forms-of-weight-two.pdf).
  **[theory, D62]** Sections 1.4–1.5, especially Proposition 1.5.5,
  supply the geometric bipartite graph and uniformization conventions
  used to audit S before taking its Atkin--Lehner quotient. The script
  verifies the corresponding 116/155 graph and 16/24 eigenspace dimensions.

- **A. K. Lenstra, H. W. Lenstra Jr. & L. Lovasz**, *Factoring polynomials
  with rational coefficients*, Math. Ann. 261 (1982), 515–534,
  [CWI author preprint](https://ir.cwi.nl/pub/9304/9304D.pdf).
  **[method/theory, D60]** Section 1 develops lattice basis reduction
  and Gram--Schmidt length bounds. Script 98 uses LLL to find a useful
  integral basis but verifies its transformation and Gram data exactly.
  The report derives its own exterior-power/empirical-box exclusion
  from these elementary lattice ideas and Hadamard's inequality.
  No analytic error estimate or target height upper bound is attributed
  to this paper. See `cm-flag-height.md`.

- **J. Voight**, *Computing CM points on Shimura curves arising from
  cocompact arithmetic triangle groups* (2006),
  [corrected author version](https://jvoight.github.io/articles/shimcm-fixed-errata.pdf).
  **[theory/method, D59]** Theorem 5.1 and Algorithm 5.2 give the ideal
  action convention: iota(c)*O=xi*O acts by xi^-1 on the CM fixed point
  for arithmetic Frobenius. Script 96 constructs xi through an exact
  intertwiner/intersection and norm equality. We use reciprocity on
  the canonical curve, not the triangle hypergeometric parametrization
  or genus-zero descent argument. See `cm-orbit-recognition.md`.
- **J. Voight**, *Shimura curve computations*, Clay Mathematics
  Proceedings 8 (2009),
  [author manuscript](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf).
  **[theory, D59]** Section 4.3 gives the CM Hilbert-class-field and
  reciprocity description for quaternionic curves over totally real
  fields; section 4.5 describes the normalizer quotient. This supplies
  the general setting for the ideal action used in the orbit report.

- **J. Sijsling & J. Voight**, *On explicit descent of marked curves and
  maps*, Research in Number Theory 2 (2016), article 27,
  [author version, 2020](https://jvoight.github.io/articles/birch-descent-021420.pdf).
  **[theory, D58]** Theorem 1.3.2 (published Theorem 1.8) descends a marked
  map with a smooth source marking to its field of moduli. We establish
  that field as Q for the Atkin--Lehner cover with its unique high-order
  CM point; an F-rational point alone would not establish it. Theorem
  2.1.1 and section 2.2 give the marked Weil cocycle criterion, used with
  the rigidity supplied by D56's normalized functions. See
  `marked-descent.md` for the remaining function hypotheses.
- **P. L. Clark & J. Voight**, *Algebraic curves uniformized by congruence
  subgroups of triangle groups*,
  [author manuscript](https://jvoight.github.io/articles/triangle-031622.pdf).
  **[theory/context, D58]** Example 10.3 formulates Galois conjugation
  through canonical quaternionic models and invariant arithmetic data.
  Its triangle-rigidity argument is not applied to the genus-16 curve.

- **N. Elkies**, [answer to *Degree 17 number fields ramified only at 2*](https://mathoverflow.net/questions/172148/degree-17-number-fields-ramified-only-at-2).
  **[exact input, D57]** The degree-17 Harbater polynomial, also reproduced
  in Dembélé's Remark 6.2, presents the abstract CM residue algebra.
  Script 94 verifies its discriminant, power-order index and selected
  reductions. Its generator is not asserted to be a value of D56's X.
- **J.-W. Guo & Y. Yang**, *Equations of hyperelliptic Shimura curves*,
  [preprint](https://arxiv.org/pdf/1510.06193).
  **[method assessed, D57]** Constructs Borcherds forms and uses CM norms
  for equations of Shimura curves over Q. No corresponding input form
  for the present target functions has been constructed.
- **J. H. Bruinier & T. Yang**, *CM values of automorphic Green functions
  on orthogonal groups over totally real fields*,
  [author manuscript](https://www.mathematik.tu-darmstadt.de/media/algebra/homepages/bruinier/publikationen/shim-cm7b.pdf).
  **[method assessed, D57]** Theorem 1.1 and section 7 give CM-norm
  formulas with specified Whittaker-form/special-divisor input. This
  addresses totally real fields; the obstacle here is the absent input
  function, not a blanket restriction of the theory to Q. It does not
  provide additive traces of D56's unspecified exact sections.

- **J. van Dobben de Bruyn & D. Gijswijt**, *Treewidth is a lower bound on
  graph gonality*, Algebraic Combinatorics 3 (2020), 941–953,
  [paper](https://alco.centre-mersenne.org/articles/10.5802/alco.124/).
  **[theory, used D46]** Includes metric graphs. Our explicit minor of
  minimum degree four gives gonality(C)>=4 after specialization.
- **M. Green & R. Lazarsfeld**, *A simple proof of Petri's theorem on
  canonical curves*,
  [paper](https://www.math.stonybrook.edu/robert.lazarsfeld/Reprints/Green.Laz.Simple.Pf.Petri.pdf).
  **[theory, used D46]** With nontrigonality established, genus 16 excludes
  the plane-quintic exception, proving the canonical ideal is generated
  by its 91 quadrics. See `canonical-gauge.md`.

- **M. Baker**, *Specialization of linear systems from curves to graphs*,
  Algebra & Number Theory 2 (2008), 613–653,
  [preprint](https://arxiv.org/pdf/math/0701075). **[theory, used D45]**
  Specialization cannot decrease divisor rank; a hyperelliptic curve's
  reduction metric graph must be hyperelliptic. §2 and §3.2 underpin the
  exact obstruction in `hyperellipticity-audit.md`.
- **M. Chan**, *Tropical hyperelliptic curves*,
  [preprint](https://arxiv.org/pdf/1110.0273). **[theory, used D45]**
  Theorem 1.3 characterizes hyperelliptic metric graphs by tree-quotient
  involutions of their canonical loopless models. Supplies the metric
  step, so arbitrary edge lengths and subdivisions do not evade our
  exhaustive finite graph test.

- **C. Qiu**, *Hyperelliptic Shimura curves and L-functions of central
  vanishing order at least 3* (2025),
  [v2, section 8](https://arxiv.org/html/2509.06175v2#S8). **[theory]** Explicit
  adelic description of the same genus-16 quotient and sign conventions;
  informs D42's proposed reflection-subgroup level. No curve equations supplied.
  **D50 check:** v2's Theorem 8.1 cites Dembélé's Theorem 5.9 for
  hyperellipticity; it is not an independent resolution of the D45 conflict.

- **L. Dembélé**, *An intriguing hyperelliptic Shimura curve quotient of genus
  16*, Algebra & Number Theory 14 (2020), 2713–2742,
  [doi:10.2140/ant.2020.14.2713](https://doi.org/10.2140/ant.2020.14.2713),
  [revised preprint](https://arxiv.org/pdf/1906.06772). **[theory]** Theorem 6.4
  resolves D40 as the solvable Harbater field; geometric input to D42's
  proposed higher-level curve route. See `review-2026-09-14.md`.
  **D44 audit:** numerical product rank 45 conflicts with Theorem 5.9's
  hyperellipticity. An apparent upstairs/quotient-coordinate gap in its
  proof is analyzed in `genus16-differentials.md`. This is not a certified
  refutation. Proposition 6.5 supplies a separate induced-character route
  to Theorem 6.4; do not conflate the two arguments.
  **D45 supersedes the numerical-only verdict:** Figure 2 is independently
  recovered from Brandt arithmetic and has no tree-quotient involution.
  The exact obstruction contradicts the hyperellipticity claim. Use the
  reduction data and separate residual arguments with their specific
  justifications; see `hyperellipticity-audit.md`.
  **D56:** uses Theorem 5.1's signatures and the seventeen order-two CM
  points for the F-rational divisor in `cm-pointed-maps.md`; this use
  does not invoke the hyperellipticity claim.
  **D57:** uses sections 5.2/5.4's CM field and class-number input, CM
  reciprocity, and Remark 6.2's Harbater polynomial. The exact algebra
  and its reductions do not supply the target function values; see
  `cm-arithmetic-input-audit.md`.
  **D58 corrects D57's descent-source omission:** Lemma 5.2 gives descent
  of the genus-40 curve and its Atkin--Lehner involution before the
  hyperellipticity argument. Carrying its canonical-conjugation argument
  through the marked cover supplies the field-of-moduli input for
  Sijsling--Voight; the branch divisor then descends with P. This use
  does not invoke Theorems 5.9 or 5.13. See `marked-descent.md`.
- **K. Khuri-Makdisi**, *Linear algebra algorithms for divisors on an algebraic
  curve*, Math. Comp. 73 (2004), 333–357,
  [preprint](https://arxiv.org/abs/math/0105182). **[method]** Curve
  divisor arithmetic proposed for D42. D56 uses the section-multiplication
  and intersection viewpoint of section 3 to construct pointed functions
  numerically; this is not yet a Jacobian arithmetic implementation on
  the target carrier. See `cm-pointed-maps.md`.
- **K. Khuri-Makdisi**, *Asymptotically fast group operations on Jacobians
  of general curves*, [author preprint, 2006](https://arxiv.org/pdf/math/0409209).
  **[method/theory, D78]** Representation B and §§2–3 supply section
  evaluations, multiplication/division and complementary-divisor
  operations. The local implementation uses exact Riemann–Roch
  dimensions to validate partial products and constraints, and checks
  all generators in a surviving degree-zero quotient. The explicit
  genus-40 section bases, points, branch-class third and corruption
  controls are our computations. No class number or cover identification
  is attributed to this paper.
  **D79:** the same operations recover an F31 effective representative
  and explicit functions with prescribed divisors. The evaluation set
  is expanded to 1,024 points, faithful through L(8D0). Full final
  multiplication inclusions and the global norm identity certify the
  cubic; the paper is not credited with our specific descent formula.
  **D81:** the same divisor operations now run over the unramified
  quadratic extension of Z/961. Unit minors, complete free RR targets
  and Nakayama justify the lifted module operations; all final
  degree-zero and function inclusions are checked in the whole ring.
  The actual point/section lifts and the choice retaining D79's
  coefficient reduction are local computations in 184–194.
- **J. Weinstein**, *The local Jacquet–Langlands correspondence via Fourier
  analysis*, Journal de Théorie des Nombres de Bordeaux 22 (2010), 483–512,
  [paper](https://www.numdam.org/item/10.5802/jtnb.728.pdf).
  **[theory, D51]** §2.2 and §6.1–6.2 identify the depth-zero finite cuspidal
  GL2 type with the induced division-algebra type. Applied at residue field
  F2 to sign and Std in `target-realization.md`.
- **H. Carayol**, *Sur les représentations l-adiques associées aux formes
  modulaires de Hilbert*, Ann. Sci. ENS 19 (1986), 409–468,
  [paper](https://numdam.org/item/10.24033/asens.1512.pdf).
  **[theory, D51]** Theorem B, §0.10 and §2.2 supply the Shimura-curve
  cohomological realization and compatibility used in `target-realization.md`.
- **N. Mascot**, *Hensel-lifting torsion points on Jacobians and Galois
  representations*, Math. Comp. 89 (2020), 1417–1455,
  [preprint](https://arxiv.org/pdf/1808.03939),
  [LiftTors implementation](https://github.com/nmascot/LiftTors).
  **[method/tool, used D62–D67]** Actual Makdisi divisor arithmetic and
  odd-prime lifting of 2-torsion. Revision
  `fd6403caf7147b21b67dcb17dbedccea762d6262` is pinned in `upstream.lock`.
  **D78:** the pinned `pic.c` negation/chord and equality schedules are
  adapted in `170_cm_frame_cover_class_arithmetic.m` to the actual
  genus-40 candidate's finite-field evaluation matrices. The native
  GP probe validates branch representatives but times out at 180 s;
  the Magma adaptation completes the class operations and third search.
  This is a local finite-field frontend/implementation, without changes
  to LiftTors, a new torsion lift, or an arithmetic monodromy match.
  Scripts 100–104 and the build/runner exercise the Q8 example, recover
  its known Q(i) field, and measure larger controls. D62's genus-64
  failure motivates D63's streamed products and batched kernel solve.
  Those changes and the exact batched validator are local adaptations,
  with comparisons against the retained upstream routines. See
  [the memory audit](dembele/certificates/lifttors-memory.md) for the
  genus-64/a=2 result. D64's scripts 105–106 calibrate degree 51 at
  genus 4 and verify a local row-generation identity against
  `PicLift_worker`. `RRInit` constructs the unramified field and closes
  evaluation points under Frobenius; `mat2col` fixes the row ordering.
  The new formula is only a GP prototype, not a native backend change.
  See [the extension report](dembele/certificates/lifttors-extension.md).
  D65 implements that formula in a separate native build with both
  preceding lifting paths retained. Script 107 compares its equations,
  kernels and torsion lifts, including complete residual replay and
  good-reduction rejection. The original source and D63/D64 computational artifacts
  remain unchanged; see [the native report](dembele/certificates/lifttors-rows.md).
  D66's genus-16/degree-51 control passes with that library. Inspection
  of `rr.c` establishes that auxiliary spaces are vectors of embedding
  matrices; `pic.c` incorrectly sends those vectors to `FpXM_red` in
  `linalg.c`. Script 110 reproduces the defect, and the separate D66
  build reduces each embedding matrix. Script 111 verifies reduction
  and projective evaluation on saved Q8 points; script 109 measures
  component storage. The corrected genus-16/degree-51 control and
  Q8 field recovery also pass. This is a local correction to the pinned source,
  not an upstream release or a new theorem. See
  [the D66 report](dembele/certificates/lifttors-degree51.md).
  D67 instruments copies of the corrected source and checks that removing
  hooks recovers every original C token. The audit follows `PicLiftTors`,
  `PicInflate_U`, `PicMul`, `PicChord`, `DivSub`, `matkerpadic` and related
  calls. The position of `avrho` explains retention of GWV beyond its
  last use; `DivMul` returns without collecting intermediate products.
  These observations motivate proposed local cleanups, not a change
  already made to the pinned software. See
  [the allocation audit](dembele/certificates/lifttors-allocation.md).
  No target-scale feasibility or target
  arithmetic frontend is attributed to the source.
- **N. Mascot**, *Certification of modular Galois representations*,
  [author manuscript, 5 September 2016](https://www.maths.tcd.ie/~mascotn/research/Certification.pdf).
  **[context/method to adapt, D100]** Separates approximate polynomial
  computation from a subsequent arithmetic certification. The paper's
  introduction assumes classical modular forms over Q and residue
  degree one. It is a model for a possible separate proof, not a
  ready implementation for our base field F and coefficients F256.
  No certification algorithm for the present representation is claimed.
- **PARI/GP developers**, *User's Guide to the PARI Library*,
  [stack handling and garbage collection](https://pari.math.u-bordeaux.fr/dochtml/html-stable/usersch5.html).
  **[tool/API, D63]** Documents `avma`, `gerepilecopy` and `gerepileall`,
  used to release worker temporaries and keep only selected rows and
  kernels. The runs use PARI 2.17.1. These APIs manage storage; they do
  not prove the arithmetic equivalence of the local adaptation, which
  is justified separately in the report and checked by scripts 103–104.
  **D64:** the [GP object-size documentation](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Conversions_and_similar_elementary_functions_or_commands.html#sizebyte)
  defines `sizebyte` as the size of an object's representing tree.
  Script 106 uses it for equation matrices, blocks and caches. It is
  not a peak RSS or stack measurement; larger storage projections are
  conditional on comparable entry representations.
  **D65:** `gerepilecopy` and `gerepileall` reclaim generated blocks
  and row-basis temporaries. Stack checkpoints exclude callers' live
  objects and are not peak process memory. The native adaptation's
  arithmetic correctness is argued and checked separately.
  **D66:** component `sizebyte` measurements count the representing
  trees, including sparse entries and containers. The genus-64
  projection assumes comparable entries and known-curve basis shapes;
  it is neither a peak measurement nor a stack lower bound.
  **D67:** `pari_mainstack->top-avma` supplies instantaneous stack-use
  checkpoints, with current capacity recorded separately. The installed
  2.17.1 headers and a local timer check distinguish cumulative
  `walltimer_get` from resetting `walltimer_delay`. The instrumentation
  uses the former. Neither the APIs nor tracing prove peak-memory bounds
  or future savings from the proposed cleanup.
- **J. Voight & J. Willis**, *Computing power series expansions of modular
  forms*, [preprint](https://arxiv.org/pdf/1205.0045). **[method, used D44]**
  Cauchy/Fourier power-series computation of differentials on a cocompact
  Fuchsian quotient. Implemented with order 32 sparsity in scripts 67–70;
  yields numerical canonical relations, still requiring algebraic recognition.
  D46 uses the CM coefficient/period grading in §2 to motivate the fixed
  jet normalization in script 74. Reality and numerical stability do not
  yet identify a field of definition or certify exact coefficients.
  **D70:** §3 of the [author manuscript](https://jvoight.github.io/articles/ModFormPaper-090317.pdf)
  distinguishes numerical checks from rigorous verification. This
  method and CM algebraicity do not supply our missing exact
  Shimura-side jets. Script 119 reuses the numerical banks only for
  discovering marks, with separate exact tests on the candidate.
- **J. Rickards**, *Improved computation of fundamental domains for arithmetic
  Fuchsian groups*, Math. Comp. 91 (2022), 2929–2954,
  [doi:10.1090/mcom/3777](https://doi.org/10.1090/mcom/3777),
  [maintained code](https://github.com/JamesRickards-Canada/Fundamental-domains-for-Shimura-curves).
  **[tool, used in D43]** Computed the genus-16 normalizer domain in ~257 s;
  pinned code and compatibility patch in `dembele/pari/README.md`. The domain
  supports the exact local S3 cover calculation in `genus64-cover.md`.
- **R. Baït & A. Page**, *Computing the cohomology of Shimura curves in
  quasi-linear time*, ANTS XVII (2026),
  [paper](https://antsmath.org/ANTSXVII/papers/antsxvii-bait_page-paper.pdf),
  [code](https://github.com/rayanebait/Cohomology-of-Shimura-curves).
  **[method, proposed]** Improves cohomology given a fundamental polygon;
  does not solve the algebraic-model gate.
- **N. Mascot**, *Moduli-friendly Eisenstein series over the p-adics and the
  computation of modular Galois representations*,
  [preprint](https://arxiv.org/abs/2004.14683). **[context]** Equationless
  Jacobian data for modular curves; D42 distinguishes its elliptic moduli
  input from the missing quaternionic input here.
  **D50:** §8.1 includes a genus-22 example, residue degree four, under
  eleven hours on 84 cores. A useful backend reference, not a runtime
  prediction for the genus-64 target; evaluation functions affect precision.
  **D61:** rechecked Definition 2.1.1 and Remark 2.1.6. An equationless
  Makdisi model still needs a positive line bundle, points with Frobenius
  action, local trivializations, a section-evaluation matrix of the
  required reduction rank, and a local Euler factor. The modular paper's
  elliptic-moduli construction does not supply these quaternionic target
  data. This is the arithmetic interface used in the new stocktake.
  **D62:** the control successfully removes the equation after generating
  arithmetic evaluation matrices. The proposed divisor pi^*(43P) on Y
  has degree 129, 66 initial sections and requires at least 646 points.
  These are interface dimensions, not computed target values.
- **S. Hashimoto, G. M. Lido, D. Lombardo, N. Mascot & P. Parent**,
  *Equationless quadratic Chabauty for non-split Cartan modular curves*
  (August 2026), [preprint](https://arxiv.org/abs/2608.10919).
  **[context, reviewed D50]** Uses elliptic curves and Cartan level structures
  in place of projective equations. No immediate arithmetic evaluation
  construction for our quaternionic curve follows from this input.

- **L. Dembélé**, *A non-solvable Galois extension of Q ramified at 2 only*
  (arXiv:0811.4379). **[target]** The field we are trying to make explicit; his
  level-one mod-2 Hilbert Hecke computation over Q(ζ₃₂)⁺ is reproduced exactly
  in `dembele/` (checkpoints 1–5), and his published eigenvalue/Frobenius
  tables are our ground truth (`dembele/data/published/dembele_2009.json`).
- **J-P. Serre**, supplement to Dembélé's result (C. R. Acad. Sci.,
  doi:10.1016/j.crma.2008.12.006). **[context]** Image/ramification analysis of
  the residual representations.
- **C. Cunningham & L. Dembélé**, descent of the 16-dimensional abelian
  variety (arXiv:1705.03054). **[context]** Audited in
  `dembele/certificates/cunningham-dembele-audit.md`; we identified a gap in
  the cyclic-degree-8 case (Schur-index-2 alternative).
- **M. Musty**, *2-Group Belyi Maps* (Dartmouth thesis, 2019; advisor
  J. Voight). **[target]** Source of the open questions Q1.2.5/Q6.2.1; the
  legacy negative arc (`writeup/main-result.md`) and the present covers arc
  (`writeup/all-2-power-covers.md`) are its sequels. User explicitly prioritized
  this thesis and their two coauthored Belyi papers in D52. Local copy:
  `/Users/musty/michaelmusty.github.io/assets/musty_thesis_final.pdf`;
  [author's copy](https://michaelmusty.github.io/assets/musty_thesis_final.pdf).
  Chapter 5 supplies the exact Q8 control and divisor/Picard methodology;
  its quadratic tower algorithm does not directly construct our degree-three Y/C.
  D56 constructs exact functions with poles 3P and 4P on that Q8 curve,
  checking the new trace normalization and plane-relation solver against
  independently known algebraic data. The target's trace prescription
  is derived in `cm-pointed-maps.md`, not attributed to the thesis.

## The M23 cluster (the trigger and the method template)

- **X. Huang, B. Jackson, K.-H. Lee, B. Poonen, R. Pries, S. Zhang**, *The
  Mathieu group M₂₃ is a Galois group over Q*
  ([arXiv:2608.08538](https://arxiv.org/abs/2608.08538)). **[method]**
  The template for the whole rigidity arc: non-rigid triples with
  𝔊-equivariant branch data, numerics-then-certify, tame mod-p monodromy
  certification (their Prop 3.5 pattern is our `GaloisGroup`-certification
  step), and the polred/specialization endgame. `dembele/rigidity/README.md`.
  **D73:** [§3, p. 6](https://arxiv.org/pdf/2608.08538) motivates allowing
  known curve equations in the numerator search. The integral adaptation
  and measured 631→48→39-digit comparison are documented in
  `dembele/certificates/cm-frame-normalization.md`.
- **S. Zhang**, [*Where to Point the Telescope: AI, Mathematical Judgment,
  and M23*](https://www.shaowuzhang.com/files/how-we-found-m23.pdf).
  The saved August 11 preliminary version has the older title *How AI
  Entered Our Collaboration on M23 and How We Found the Case*, at
  `dembele/rigidity/refs_how-we-found-m23.pdf`; it has been preserved.
  **[method]** The coordinates-not-precision lesson (DECISIONS D3) and the
  4-tuple → triple discovery narrative; directly caused our equivariant-gauge
  pivot. D53 compares the revised public note with that copy and audits
  the actual code/results from D3, D9 and D21; see
  `dembele/certificates/m23-coordinate-review.md`. The separate cubic
  reduction algorithm mentioned in the account is not published in the
  linked M23 verification repository as inspected on 2026-09-15.
- **F. Häfner**, braid orbits and M₂₃ (arXiv:2202.08222; also Diplomarbeit,
  Karlsruhe 1987). **[method]** The 4-point-orbit → boundary-triple
  correspondence (their Thm 5.1) is the conceptual basis of our boundary/cusp
  maps (scripts `24`, `29`), which became our cheap oracle for component
  arithmetic.
- **M. Klug, M. Musty, S. Schiavone, J. Voight**, *Numerical
  calculation of three-point branched covers of the projective line*
  (LMS J. Comput. Math. 17, 2014;
  [arXiv:1311.2081](https://arxiv.org/abs/1311.2081)),
  and **M. Musty, S. Schiavone, J. Sijsling, J. Voight**, *A database of Belyi
  maps* (ANTS XIII, 2019;
  [arXiv:1805.07751](https://arxiv.org/abs/1805.07751)). **[tool/method]** The `~/Belyi` package is our main
  computational engine for all cover computations; we made four local patches
  during this work (TrialDivision guard, genus-1 and hyperelliptic dump hooks,
  genus-scaled column count). D52 rereads the first paper's general canonical
  reconstruction and the second paper's marked descent/weighted normalization.
  Remark 4.4.1 is a numerical observation, not a general coefficient-field
  theorem. The new formal-coordinate argument and exact controls are in
  `dembele/certificates/pointed-normalization.md`. No upstream communication
  is authorized or implied by this reference note.
- **R. van Bommel, E. Costa, B. Poonen, P. Srinivasan**, *Curve equations from
  expansions of 1-forms at a nonrational point* (LuCaNT, 2026;
  [arXiv:2506.14026](https://arxiv.org/abs/2506.14026)). **[method, D68 audit]**
  Theorem 3.1 requires expansions of a ground-field basis of regular
  differentials; it does not supply that basis from complex data.
  Corollary 4.2 uses the full conjugate divisor to shorten the exact
  jet bound. For a rational quadric on our genus-16 curve at a degree-17
  point, vanishing to order four would suffice (`4*17>60`), provided
  the needed arithmetic expansions were exact. D68's projective frame
  addresses the basis choice and supplies exact zeroth-order CM
  constraints, not those higher exact jets. The M23 paper also cites
  its canonical-quadrics dimension test.
- **A. Guillemot and J. Voight**, *Belyi map verification using certified
  path tracking*, [arXiv:2604.15562v2](https://arxiv.org/abs/2604.15562v2),
  19 August 2026. **[context, D70]** Certifies monodromy of exact
  Belyi map candidates against input triples using certified path
  tracking. Reviewed as an identification mechanism, not executed.
  We have no Belyi map/passport identifying the present Shimura
  candidate, so this does not fill the exact-jet gap automatically.

## Rigidity, Hurwitz spaces, reduction of covers

- **M. Fried & H. Völklein** (Math. Ann. 290, 1991). **[theory]** Hurwitz
  spaces, Nielsen classes, the rigidity framework; the braid action we compute
  in scripts `20`, `22`, `29`.
- **M. Fried**, branch cycle lemma. **[theory]** The ε-cyclotomy constraints
  on class multisets — our "forced 2-cyclotomic layer" computations.
- **K. Coombes & D. Harbater** (Duke 1985); **P. Dèbes & J-C. Douai** (Ann.
  ENS 1997). **[theory]** Field of moduli = field of definition for
  center-trivial covers; invoked for every moduli-field statement.
- **S. Beckmann** (J. Algebra 1989). **[theory]** Good reduction of covers
  away from |G|; the gate-2 analysis in `writeup/all-2-power-covers.md` §1, §4.
- **M. Raynaud** (Invent. Math. 1999); **S. Wewers** (J. AMS 2003);
  **I. Bouw & S. Wewers** (Crelle 2004 and related). **[theory]** Bad
  reduction of three-point covers at p ∥ |G|: the mixed ordinary/supersingular
  picture our local-mechanism data exemplifies (`local-mechanism.md`), the mild
  moduli ramification we observe, and the deformation-data machinery that is
  the named route to replacing our transfer hypothesis with a theorem.
- **A. Grothendieck** (SGA 1), with **F. Orgogozo & I. Vidal** for the tame
  specialization refinements. **[theory]** Tame specialization isomorphism —
  underlies both the good-reduction lifting arguments and the M23-style mod-p
  certification.
- **Conway–Parker** (unpublished; via Fried–Völklein). **[context]** The
  braid-transitivity expectation against which our short orbits are the
  interesting exception.
- **L. E. Dickson**. **[theory]** Subgroup classification of PSL₂(q) — the
  generation filters in every census.
- **R. Lang** — Lang's theorem. **[theory]** The outer-coset class
  correspondence (classes over φʲ ↔ classes of SL₂(2^gcd)) used throughout the
  censuses.
- **M. Suzuki** (1962). **[theory]** The Sz(q) family and its 2-Sylow
  structure — the independent-family test (script `21`).
- **J-P. Serre**, *Topics in Galois Theory*; **G. Malle & B. H. Matzat**,
  *Inverse Galois Theory*. **[context]** Rigidity background and the
  realization landscape.

## The period route (Hilbert modular / quaternionic side)

- **M. Eichler; G. Shimura**. **[theory]** Brandt matrices; Eichler–Shimura
  theory relating weight-2 forms to abelian varieties — the reason λ-torsion of
  B_g gives the field.
- **H. Jacquet & R. Langlands**. **[theory]** The correspondence moving
  Dembélé's form between definite and indefinite quaternion algebras; the
  parity constraint that forces the auxiliary prime.
- **K. Ribet**; **A. Rajaei** (*On the levels of mod ell Hilbert modular
  forms*, J. reine angew. Math. 2001); **R. Taylor**; **F. Jarvis**.
  **[theory]** Level raising and lowering. The congruence condition
  `a_q = +-(Nq+1) mod lambda` is what the gate-1 scan searches for. We
  deliberately **do not invoke** these theorems for gate 3: they are general for
  `ell > 2`, whereas `ell = 2` is a separate delicate case (cf. *Level raising
  mod 2 and arbitrary 2-Selmer ranks*, arXiv:1501.01344), and Rajaei's
  even-degree hypothesis asks for a special or supercuspidal place, which our
  level-one form does not have. Hence the direct computation (D24,
  `dembele/certificates/gate3-status.md`).
- **D. Mumford; J. Tate**. **[theory]** Non-archimedean uniformization of
  abelian varieties with multiplicative reduction. Why the Eisenstein
  q-expansion can be evaluated on q₀-adic periods at all: the period generators
  are topologically nilpotent, exactly as for a Tate curve
  (`gate5-padic-eisenstein.md`). Also the source of the Kummer description
  of torsion, `0 → Hom(X/n, μ_n) → J[n] → Λ/nΛ → 0`, used to answer the
  `λ`-torsion localization question negatively-for-the-goal
  (`lambda-torsion-localization.md`, D38): torsion localizes as a *local*
  Galois module, but the uniformization coordinates of torsion points are
  transcendental (`q^{1/2}`, not `j(q)`), so no algebraic data leaves `q₀`
  without globally algebraic functions. D42 corrects the implication that
  this requires an explicit theta model of the full variety: a curve model
  and divisor arithmetic are another possible source of such functions.
- **I. Cerednik; V. Drinfeld**. **[theory]** p-adic uniformization of Shimura
  curves with a finite disc prime — the pivot that eliminates the genus wall
  (`levelraise-cd-plan.md`).
- **L. E. Dickson** (finite subgroups of `PGL₂(F̄_p)`; e.g. Huppert, *Endliche
  Gruppen I*, II.8.27) and **H. Moon & Y. Taguchi** (nonexistence of mod-2
  representations unramified outside 2 over small fields). **[theory]** The
  attempted image argument of D40. Its anti-dihedral premise failed (D41),
  and the published identification with the Harbater field settles the
  branch (D42). Do not attribute the incorrect large-image conclusion to
  these sources. The smaller-field single-operator sweeps do not establish
  a general nonexistence theorem.
- **V. Drinfeld** (coverings of the p-adic upper half plane) and
  **J. Teitelbaum**, *Geometry of an étale covering of the p-adic upper half
  plane* (Ann. Inst. Fourier 1990). **[theory]** The level-`1+𝔭_D` Shimura
  curve carrying the `𝔭²`-new forms of D39 is uniformized by a quotient of the
  first Drinfeld covering `Σ¹ → Ω`, whose reduction has Deligne–Lusztig
  components of genus `q(q−1)/2 = 1` at `q = 2`: not a Mumford curve, no
  toric period lattice — an obstruction to the existing period pipeline
  (`levelraise-p2k.md` §3), not to D42's proposed curve/Jacobian construction.
- **C. Bushnell & G. Henniart**, *The local Langlands conjecture for GL(2)*
  (depth-zero / conductor-`𝔭²` supercuspidals, Jacquet–Langlands for the
  division algebra). **[theory]** Identifies the `𝔭²`-new forms as depth-zero
  supercuspidal (`U_𝔭 = 0`, tame inertial type `Ind χ`, `χ` of order 3 on
  `F₄^×`), hence potentially good supersingular reduction of `A_g` at `𝔭`
  (`levelraise-p2k.md` §3, D39).
- **C. Breuil & A. Mézard; T. Gee & M. Kisin** (Breuil–Mézard multiplicities,
  potentially Barsotti–Tate lifts) and **K. Buzzard, F. Diamond, F. Jarvis**
  (Serre weights for Hilbert modular forms). **[theory, heuristic only]** The
  prediction behind D39: with residue field `F₂` there are two Serre weights
  and `ρ̄_f` carries both, so every inertial type at `𝔭` should admit a
  modular lift, with the depth-zero type at multiplicity equal to the level-1
  one (both reduce to the trivial weight). Confirmed at `𝔭²` (new multiplicity
  `[1,1]`); none of it is a theorem at `p = 2`, `e = 8`.
- **J. Teitelbaum**. **[method]** First explicit p-adic periods of Shimura
  curves; the lineage of our planned computation.
- **M. Greenberg** (2006–09). **[method]** Numerical p-adic integration on the
  Bruhat–Tits tree; with **J. Voight** (Math. Comp.), the definite
  Hecke-eigenvalue algorithms behind `hilbertmodularforms`.
- **X. Guitart, M. Masdeu, M. H. Şengün** (JLMS 2014; J. Algebra 2016; PLMS).
  **[method]** Overconvergent quaternionic Darmon points; *p-adic periods →
  algebraically recognized equations* — the published proof-of-concept for our
  endgame pattern. **M. Masdeu**'s `darmonpoints` (Sage/Magma) is the closest
  existing implementation and the designated de-risking vehicle for gate 4.
  **Assessed 2026-08-16** (`gate4-*.md`): the overconvergent *lift* works and is
  timed (dimension-2 case reproduced, matching an independent modular-symbols
  ground truth), but the *period* path has bit-rotted under Sage 10.6 — four
  version-drift failures, abandoned rather than risk silently wrong periods — and
  `padicperiods` is genus-2 specific (three half-periods, Igusa recognition),
  while the group layer only offers the Fuchsian construction for totally real
  base fields. So it is a source of algorithms and a partial reference, not a
  drop-in engine. **Update 2026-09-01 (Tate pilot):** confirmed empirically
  that definite discriminants are rejected even over `Q` (the Magma Fuchsian
  layer errors), so the pilot builds a definite S-arithmetic group class
  against the ~14-method seam (`tate_pilot/README.md`), over `Q` first with
  `E.tate_curve(p).parameter()` as ground truth, then retargeted at `F` via a
  Magma element export.
- **B. Gross**, *Heights and the special values of L-series* (1987).
  **[theory]** The definite-quaternion height pairing `⟨e_i, e_j⟩ = w_i δ_ij`
  with `w_i` the stabilizer orders, and the Brandt symmetry
  `w_j B_ij = w_i B_ji`. Source of the **D31 correction**: the monodromy
  diagonal is the stabilizer orders, not the Eichler masses — re-derived
  empirically from `T`'s entry ratios before being recognized as Gross's
  pairing. Verified on all 3 494 618 support entries at q0
  (`54_delta_prime_q0_wfix.m`).
- **P. Deligne** (Weil II), with **J-L. Brylinski & J-P. Labesse / D. Blasius**
  for Hilbert modular forms. **[theory]** The Ramanujan bound
  `|a_v| ≤ 2√(Nv)` — the load-bearing inequality of the D30/D32 balanced-lift
  certification (a degree-`d` global factor has coefficients under
  `C(d,d/2)·⌈2√Nv⌉^d`, observed non-global lifts sit at `~2^{190}`).
- **K. Ribet**, *Mod p Hecke operators and component groups of Jacobians*
  (and the Bertolini–Darmon usage). **[theory]** Component groups and the
  monodromy pairing on the character lattice with stabilizer edge lengths —
  the frame for `Δ'` and for the Tate pilot's valuation rule
  `v(q) = ⟨v,v⟩_stab/2` (empirically exact on six curve classes,
  `tate_pilot/overq_monodromy2.sage`; the uniform /2 still owes its
  derivation to this literature).
- **Y. Maeda** (the Hida–Maeda conjecture and its heuristics). **[context]**
  Giant-Galois-orbit expectation for newspaces — the reason the D32 no-go
  generalizes: a small orbit carrying the residual system would be a
  Maeda-violating accident, and the structured exceptions (CM, base change,
  twists) are forbidden by the nonsolvable residual image
  (`stocktake-2026-09-01.md` §1).
- **H. Shimizu**. **[theory]** The volume formula behind the archimedean
  infeasibility computation (ζ_F(−1) = 5820 ⇒ genus ≥ ~91(Nq₀−1)/2).
- **M. Kirschmer & J. Voight**. **[tool/theory]** Quaternion ideal-class
  algorithms (inside Magma) — the Brandt infrastructure and, prospectively, the
  CD dual graph. *Practical note (2026-08-26):* the ideal-class representatives,
  unit generators and `P^1` enumeration underlying these are **not reproducible
  across Magma sessions**, so Hecke operators banked in different runs sit in
  different bases and cannot be combined for eigenspace work. Characteristic
  polynomials are basis-independent and therefore safe (`gate3-method-audit.md`).
- **K. Ribet (1984, level-raising; Ihara's lemma); F. Diamond & R. Taylor,
  *Non-optimal levels of mod l modular representations* (Invent. 1994, the
  Hilbert / definite-quaternion Ihara lemma).** **[theory]** Two uses. (i) The
  structural reading of the non-semisimplicity seen in gate 3 (D26) — with the
  **correction of 2026-08-26** that a Jordan block of `T_31` on the generalised
  eigenspace is *not* by itself evidence of old/new gluing (a new form with a
  non-maximal order at 2 gives the same data with a split module). (ii) The
  decisive one: Ihara's lemma (injectivity of the mod-2 degeneracy map on the
  non-Eisenstein part) makes the eigenspace `ker f1(T_31)` at level `q0` equal
  to the old subspace, which is why the eigensystem test of D26(c) was vacuous
  and `48_gate3_genkernel.m` works on the generalised eigenspace instead
  (`gate3-method-audit.md`, 2026-08-26; D27). Caveat: Diamond–Taylor is stated
  for odd `l`; at `l = 2` the lemma is expected but not cited, which is one
  more reason to compute rather than assume.
- **Iwahori fixed vectors (local theory, e.g. Casselman)**. **[theory]** An
  unramified principal series of `GL_2(F_q0)` has a two-dimensional space of
  Iwahori-fixed vectors; this is what fixes the old contribution
  `(f1^{(ell)})^2` to `charpoly(T_ell | G)` without building degeneracy maps.
- **J. Voight**, *Quaternion Algebras* (book) and the Magma Fuchsian/arithmetic
  machinery. **[theory/tool]** Reference frame for the whole quaternionic side.
- **E. Costa, S. Schiavone, J. Voight et al.** (the 17T7 project,
  arXiv:2411.07857 and companions; `edgarcosta/hilbertmodularforms`,
  `SamSchiavone/17T7`). **[method/tool]** The pinned HMF package our Brandt
  computations run on; the isogeny-polynomial/Eisenstein framework adapted in
  `dembele/certificates/eisenstein-prototype.md` — and, as relocated on
  2026-08-25, **the mechanism by which the route terminates in a polynomial**:
  the 257 λ-isogeny neighbours of `B` are the 257 points of `P¹(F₂₅₆)`, Galois
  permutes them, and a separating invariant evaluated at each yields the
  degree-257 polynomial (`csv-paper-adaptation.md`,
  `gate5-padic-eisenstein.md`); and (with van Bommel, Elkies,
  Keller) the descent-congruence certification method behind the
  `inverse-galois-hmf` sweep that supplies our k=4 nonexistence control.
- **J. Bosman**, *On the computation of Galois representations associated to
  level one modular forms* (arXiv:0710.1237), with **B. Edixhoven,
  J-M. Couveignes** et al. **[context/method]** Explicit polynomials for
  projectivised mod-`ell` level-one representations — degree `ell+1`, ramified
  only at `ell`, Galois group `PGL_2(F_ell)`: the same *shape* as our degree-257
  target one scale down. Table 1 supplies the only empirical anchor we have for
  the **height** of the polynomial we are trying to produce, and hence for the
  precision `M` the endgame needs (`dembele/certificates/target-height-estimate.md`).
- **A. Odlyzko**. **[theory]** Discriminant lower bounds. Used twice: to note
  that effective Chebotarev is vacuous at our conductor, and — with the
  ramification analysis at 2 — to prove `L` **cannot be totally real**
  (`rd(L) <= 31.9 < 60.8`), so complex conjugation acts as a unipotent
  involution.
- **J. Igusa**. **[theory]** Genus-2 invariants — the gauge-invariant
  recognition planned for the genus-2 corner verdict.
- **Kronecker–Weber**; **J. Lagarias & A. Odlyzko**. **[theory/context]** The
  C₈-subfield forcing into Q(ζ₂^∞); the (vacuous-at-our-conductor) effective
  Chebotarev bounds, cited to justify treating equidistribution as heuristic.

## Software and infrastructure

- **FLINT / Arb / ACB** (FLINT contributors; Arb developed by F. Johansson)
  **[tool/method]** — arbitrary-precision complex ball polynomial evaluation
  and Fourier transforms in `dembele/pari/cm_acb.c` and script 79 (D49).
  The [DFT documentation](https://raw.githubusercontent.com/flintlib/flint/v3.6.0/doc/source/acb_dft.rst)
  fixes the sign convention and precision requirement for reusable plans.
  Local Sage selects FLINT 3.1.0 via pkg-config; Homebrew also has 3.6.0.
  The balls enclose arithmetic on supplied data, not our geometric input
  error or the omitted analytic tail. See `compiled-precision-refinement.md`.
- **Magma** (Bosma–Cannon–Playoust), V2.29-8/9 — every exact computation.
  **D81:** [Galois rings](https://magma.maths.usyd.edu.au/magma/handbook/text/606)
  and their [creation functions](https://magma.maths.usyd.edu.au/magma/handbook/text/607)
  supply finite unramified coefficient rings for support/point lifts.
  Scripts 186–194 use native Z/961 matrices in coefficient pairs for
  fast products, with checked unit inverses and exact inclusions.
  The highest-digit norm and trace controls test genuine mod961 data.
  **D80:** script 180 enumerates base points, counts étale cubic roots
  and resolves exceptional fibres by exact implicit series. Script
  182 independently checks every fibre through quadratic/Kummer
  splitting, with different anchors, minors and parameters. The old
  certified base counts prove completeness of the saved lists; no
  point search is repeated by the verifier. A wrong count is rejected.
  **D79:** scripts 176/178 construct and independently verify the
  descended representative, Kummer function and genus-64 cubic modulo
  31. Matrices, ranks and exact evaluations suffice; no native
  function-field normalization or maximal-order search is invoked.
  Changed norm and trace coefficients are rejected. Corrected
  monomial-comprehension and matrix-universe failures are archived.
  **D78:** scripts 164/166 construct exact section spaces, evaluation
  points and branch kernels. Script 168 checks the saved data without
  discovery. Scripts 170–175 use finite-field matrix arithmetic for
  complementary divisors and a verified third of the branch class.
  Corrupted evaluations and a wrong third are rejected. The first
  matrix-constructor API failure is archived; native function-field
  reduction and maximal-order probes are not repeated.
  **D77:** scripts 157/159 compute the exact normalized B3 fibre and
  a witness alpha=-3*s^2 using
  [number-field element operations](https://magma.maths.usyd.edu.au/magma/handbook/text/386).
  Script 161 independently checks the saved jets, units, square
  identity, involution, splitting idempotents and reduction at 31.
  A changed leading unit is rejected. No maximal-order or class-group
  computation is invoked; the archived nonic timeout is not repeated.
  **D76:** scripts 147/149 construct and independently check the lifted
  moving space and all six products at 64/128 digits, including the
  scalar. Scripts 151/153/155 compute exact rational product relations
  and verify saved membership witnesses and divisor ideals. The
  [linear-systems example](https://docs.magma-maths.org/AlgebraicGeometry/Schemes/introduction.html#linear-systems)
  supplies the standard Veronese equations used to interpret the
  invertible coordinate change. The rational cover passes an independent
  certificate; a wrong twist passes its divisor checks but fails the
  128-digit square map. No general surface parametrizer or rational
  residual-ideal timeout probe is used.
  **D75:** script 140 independently checks joint F candidate rows and
  exact inverse-norm bounds. Scripts 143/145 construct and independently
  verify the B3 square-factor change over F31, and exact rational
  numerator membership integral at 31. Negating the denominator
  preserves the divisor but fails the global identity. A rational-ideal
  timeout is archived; the successful certificate uses good reduction
  and linear algebra under the unchanged limits.
  **D74:** runner 131 reuses scripts 125/128/129 with hashed data-path-only
  substitutions at 16, 32, 64 and 128 digits. Script 134 constructs the
  rational denominator space using an exact multiplication kernel;
  script 136 checks its reduced section identities independently.
  Highest-digit perturbations in both a polynomial coefficient and a
  basis coordinate are rejected. Read `cm-frame-precision-doubling.md`.
  **D73:** script 128 transfers the denominator by exact linear algebra
  in the degree-four coordinate ring modulo 31^8. Script 129 verifies
  the saved identity independently, computes rational implicit jets,
  checks saturated divisor ideals and rejects a highest-digit error.
  The unchanged radicand inherits D72's full divisor certificate.
  **D72:** script 123 uses the existing complementary-divisor model
  and exact lexicographic ideal equalities to export finite étale
  supports. Script 125 independently verifies the lifted coordinates,
  jets and orders over Z/31^8; degree accounting proves the divisor
  relation. It correctly rejects a changed highest digit. These are
  local algebra certificates, not a replay of the Sage Newton solves.
  See `cm-frame-resolvent-lift.md` for the flat-divisor argument.
  **D71:** the same [divisor/sheaf handbook](https://docs.magma-maths.org/AlgebraicGeometry/Sheaves/div_maps.html)
  supplies the complementary-divisor construction used for class
  arithmetic in |2K|. Scripts 121–122 recover a branch half over F31
  and independently certify its radicand by saturated-ideal equalities.
  Exact local jets resolve 0/0 values in the double-cover point count.
  The [function-field creation/order](https://docs.magma-maths.org/GlobalFields/AlgebraicFunctionFields/creation.html)
  and [function-field divisor](https://docs.magma-maths.org/GlobalFields/AlgebraicFunctionFields/divisors.html)
  documentation guides the retained alternative probe: explicit
  integral bases and genus succeed, but native Reduction times out.
  `SetOrderMaximal` is used only after a trace-discriminant proof;
  the setter is not a proof. See `cm-frame-resolvent.md`.
  **D70:** the [divisor/sheaf handbook](https://docs.magma-maths.org/AlgebraicGeometry/Sheaves/div_maps.html)
  explains complementary divisors computed by `ColonIdeal` and
  `Saturation`. Script 120 uses that construction to compute
  `h0(2B3-B2)=0` modulo 31, and verifies flat marked models.
  Elimination gives the nonic residue polynomial; `GaloisProof`
  certifies its group of order 72. A default maximal-order call
  timed out without a result, as recorded separately.
  **D69:** scripts 117–118 use Gröbner normal forms, exact polynomial
  determinants, and rational points on zero-dimensional fibers. The
  trace-discriminant certificate and its controls are local adaptations;
  they do not rely on the general curve normalization or full Jacobian
  minor routines that failed to complete in D68.
  **D59:** the [Galois-group handbook](https://docs.magma-maths.org/GlobalFields/GaloisGroupsAndAutomorphisms/galois.html)
  specifies `GaloisProof`, labelled `GaloisRoot`, and
  `GaloisGroupConjugation`. Script `96_cm_root_action.m` proves the
  31-adic group, compares complex and p-adic root orderings, and lifts
  a resolvent using an explicit coefficient bound. The installed
  complex `GaloisProof` is unavailable; the complex comparison is
  retained as a software input, not a separate certified root enclosure.
- **V. Alexeev and R. Pardini**, *Non-normal abelian covers* (2011),
  [author preprint](https://arxiv.org/pdf/1102.4184).
  **[theory, D77]** Section 1.1, equation (1.1), describes the character
  eigensheaves of an abelian cover. For our double cover, the projectors
  (1+/-tau)/2 are defined over Q and give pi_*O_X=O_C+L^(-1).
  Together with the independently certified h0_C(B3)=1 and L not
  equivalent to B3, this proves h0_X(pi^*B3)=1 and excludes a
  principal oriented branch difference. Arithmetic identification,
  descent and our numerical certificates are not attributed to this paper.
- **The Stacks Project authors**, **[theory, D69–D77]** —
  [§49.3, trace discriminants](https://stacks.math.columbia.edu/tag/0BVH),
  [Lemma 33.43.8, normal and smooth curves](https://stacks.math.columbia.edu/tag/0B8Y),
  and [Lemma 29.35.14, flat-fiber smoothness](https://stacks.math.columbia.edu/tag/01V4).
  Used in `cm-frame-verification.md`: squarefree discriminants force
  normality by the explicitly given index-squared argument; the flat
  proper model at 31 then certifies smoothness over Q. The graded-basis
  and canonical-embedding deductions are written out in that report.
  **D70:** [Lemma 36.32.1, cohomology semicontinuity](https://stacks.math.columbia.edu/tag/0BDN)
  transfers the vanishing of H0(2B3-B2) at 31 to Q, using the
  verified flat Cartier markings in the proper smooth model.
  **D71:** [Lemma 39.9.9, étaleness of multiplication](https://stacks.math.columbia.edu/tag/0BFH)
  identifies the differential of doubling as multiplication by two,
  invertible in characteristic 31. It motivates lifting the verified
  finite-field branch half via Newton/Hensel on the relative Picard
  variety. Such a lift and arithmetic reconstruction are not yet
  implemented or certified; the current cover is over F31 only.
  **D72:** the lift is now implemented through 31^8 by explicit
  local equations, with denominator double-zero corrections divided
  by a unit 2c. This is consistent with the same étaleness lemma;
  no number-field reconstruction of the full cover is claimed.
  **D75:** [relative Cartier divisors, §31.19](https://stacks.math.columbia.edu/tag/056P)
  supplies the flat residual after subtracting the verified marked
  divisor. [Lemma 37.26.6](https://stacks.math.columbia.edu/tag/0574)
  transfers reducedness of that proper residual from the special
  fibre at 31 to Q. This replaces the archived rational-ideal timeout;
  it certifies the numerator's residual, not a number-field denominator.
  **D76:** the same relative-divisor framework now applies to the
  recognized rational denominator. Exact witnesses, integral at 31,
  prove six rational sections vanish on T. After removing T, the
  empty common zero locus of two sections in the special fibre and
  properness rule out generic common zeros. Their exact product-square
  identity proves even remaining zeros and hence the rational cover.
  These computations and the local argument are detailed in
  `cm-frame-rational-double-cover.md`; they do not identify the arithmetic
  Shimura cover or its global quadratic twist.
  **D77:** [Lemma 15.114.5, tame inertia](https://stacks.math.columbia.edu/tag/09EE)
  supplies the faithful cotangent character used for the necessary
  mu3 condition at cubic branch points. Our exact K(sqrt(-3)) fibre
  and odd-degree norm argument then constrain scalar twists within
  the fixed half. [§59.28, Kummer theory](https://stacks.math.columbia.edu/tag/03PK)
  explains the line-bundle and scalar choices in the proposed cubic.
  No 3-division class or cubic extension is computed by these references.
  **D79:** [section 59.28, Kummer theory](https://stacks.math.columbia.edu/tag/03PK)
  supplies the étale unit-root construction with 3 invertible.
  [Section 53.12, Riemann–Hurwitz](https://stacks.math.columbia.edu/tag/0C1B)
  supplies the tame branch contribution. The actual functions,
  norm adjustment, S3 involution, reflection equation and branch
  degrees are proved locally in `cm-frame-cubic-cover.md`; the
  references do not select the intended arithmetic cover.
  **D81:** multiplication-by-three étaleness and nilpotent lifting
  justify uniqueness of the class lift with D78's chosen reduction.
  The square-zero formal-group argument giving c2=31c+10 is written
  out locally; 189/190 execute it and 193 checks its actual relation.
  The Kummer norm construction extends the marked cubic modulo 961.
  Neither the references nor this finite-precision result identify
  the characteristic-zero arithmetic cover.
- **The Belyi package** (Musty–Schiavone–Sijsling–Voight) with our four local
  patches — all cover numerics.
  D44 also inspected local `Code/powser_iter_arfed.m` and
  `Cext/powser_arnoldi.c` for multi-center/Arnoldi methods. Their triangle
  geometry was not directly used for the new arbitrary polygon solver.
  **D51:** directly reuse `Cext/powser_arnoldi.c` by including it in the
  workspace adapter `dembele/pari/belyi_cauchy_bridge.c`. The existing
  operator handles the supplied cover orbit blocks; the wrapper supplies
  the standard projection. Source hashes and the failed small Arnoldi
  pilot are recorded in `belyi-cover-pilot.md`; the package is unchanged.
- **`hilbertmodularforms`** (Costa et al., pinned commit in
  `dembele/upstream.lock`) — Brandt/Hecke computations, carrying our two
  local patches (`dembele/patches/`): sparse Hecke assembly and the D31
  pairing intrinsics (`InternalHMFRawStabOrdersDefinite`,
  `InternalHMFRawInnerProductDefinite`) — candidates for upstreaming.
- **Sage `BrandtModule`** (A. Pizer's algorithms; implementation
  Kohel–Stein–Tornaría lineage) — the over-`Q` ground-truth layer of the
  Tate pilot (`tate_pilot/overq_*.sage`): Brandt eigensystems, ideal classes,
  and `EllipticCurve.tate_curve` as the independent check of the monodromy
  rule.
- **`darmonpoints` 8.3** (M. Masdeu et al.; installed in Sage 10.6) — the
  overconvergent/integration layers targeted for reuse in the Tate pilot;
  see the assessment entry above for what is and is not usable.
- **chatelet.mit.edu** (MIT-hosted CoCalc; Magma license courtesy of the host
  institution) — remote heavy compute; client in `remote_magma/`.
  D47's canonical solver deployment and measured Sage dependency versions
  are documented in `dembele/jobs/canonical/README.md`; the existing
  `remote_magma/CHATELET.md` documents inherited API CPU limits.
- **Aristotle** (Harmonic) + **Lean 4 / Mathlib** — formalization of Lemma A
  (legacy) and the fixing congruence (in progress, `aristotle_fixing/`).
- **SageMath / GAP, PARI/GP, LMFDB** — the legacy scans, polred endgame
  (planned), and the modular-forms data environment.
  **D77:** script 160 uses exact quotient-field arithmetic to change
  to a rational local parameter and export the oriented branches.
  Pure Python script 163 checks a determinant modulo 31 and records
  the Riemann–Roch/pushforward deduction. These are local calculations;
  no class-group computation or descent algorithm is invoked.
  **D76:** script 146 lifts the 20-dimensional section space by exact
  unit-minor linear algebra. Script 150 uses the
  [integer-matrix interface](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
  to recognize the six-product span, fitting at 64 digits and validating
  at 128, with an exact known-space control. Script 152 performs the
  explicit rational Veronese splitting; script 154 recovers the scalar
  square root and exports the rational equation. Exact Magma certificates
  establish the geometry beyond recognition. No height optimality or
  arithmetic identification is attributed to LLL.
  **D75:** the [integer-matrix interface](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
  supplies LLL for the rank-136 joint recognition lattice and exact
  inverses for the independently certified coefficient-box bound.
  Script 142 computes the rank-100 saturated numerator lattice for
  B2+2B3. Its short section directions mix with curve relations; rank
  modulo 31 selects nine independent representatives. No optimality
  or non-descent theorem is attributed to lattice reduction.
  **D74:** [rational reconstruction](https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html#sage.arith.misc.rational_reconstruction)
  supplies bounded Q candidates. Scripts 132/135 test them, and local
  F-lattice candidates, against unused higher digits. Script 133 fits
  whole quadrics; script 135 computes the saturated exact denominator
  lattice and checks Smith invariants. These are bounded searches,
  without a nonmembership or optimal-height conclusion. Script 130
  implements exact block Newton steps; scalar unit inverses avoid
  the unavailable polynomial xgcd over composite coefficient rings.
  **D73:** the [integer-matrix reference](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
  supplies LLL and Smith-invariant operations. Script 127 computes
  integer kernels using PARI and verifies unit Smith invariants, exact
  kernel equations and ranks. This certifies saturation independently
  of the small-vector search. No shortest-vector guarantee is claimed.
  **D72:** Sage's [polynomial quotient-ring documentation](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_quotient_ring.html)
  supplies the exact finite-ring interface used for
  (Z/31^n)[a]/f(a), with f monic and separable modulo 31.
  Script 124 implements the local corrections and checks all curve
  equations after solving selected unit Jacobian minors. Script 126
  separately uses exact number-field evaluation and rational jets
  to recover the numerator over Q and measure its 631-digit height.
  Its uniform reconstruction bound follows from the elementary
  cross-difference argument written in `cm-frame-resolvent-lift.md`.
  **D60:** Sage's [integer-matrix reference](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
  documents `LLL(transformation=True)` and integral saturation. The
  returned unimodular transformation is independently checked, and
  primitive Pluecker coordinates remove the index of an unsaturated
  row lattice. Exact Q(i) arithmetic defines the saved chart boxes;
  `98_cm_flag_height.py --verify` checks the exclusions without rerunning
  LLL. Software exactness does not certify the analytic input errors.

## People (beyond the papers)

The M23 team's decision to publish not only their result but *how they found
it* (Zhang's note) materially changed this project's trajectory — twice (D3,
D16-meta). If any of this reaches publication, that intellectual debt — and
the KMSV/MSSV/17T7/HMF software lineage from the Voight school that both
projects run on — should be acknowledged prominently.

---

*Maintenance: add an entry when a new source enters the work; state the role
tag and where in the repo the use lives. Prefer over-attribution to under.*

## D150 source applicability, 2026-10-09

**Rechecked sources.**
[Van Bommel--Costa--Poonen--Srinivasan](https://arxiv.org/pdf/2506.14026),
Lemma 4.1 and Corollary 4.2, supply the exact divisor-degree vanishing
criterion assuming arithmetic expansions. They do not compute the
missing expansions for this datum; the three-coefficient rank refinement
is the project's D88 argument.
[Franc--Masdeu](https://arxiv.org/pdf/1201.0356), Introduction and section
6.2, distinguish p-adic recognition of equations from their proof.
The ramified scalar moment contraction is the project's D113 derivation.

**New companion arguments.** The infinite pole-orbit obstruction to
finite branchwise rational closure, the summed-transfer identity and its
tensor extension in the
[D150 report](dembele/certificates/structural-identification-audit-d150.md)
are deductions here, not theorems attributed to those papers. The finite
checks certify their stated arithmetic witnesses, not the full proofs.
The identity criterion has no constructed candidate witness. The
[D150 source ledger](dembele/data/computed/structural_identification_sources_d150.json)
binds the 17 inspected structural reports and records these limits.
