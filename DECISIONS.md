# Decision log

<!-- D163 -->

**D163 (2026-11-15): step 3 gate measured: about 9 CPU-hours per torsion point; go.**
Model of Y mod 673 verified by Riemann-Roch ranks and the group order.
Multiplier: x1 = (Frob-1)x, then e(Frob) with e a short vector (LLL) of
the ideal (L(zeta_17)) * p2^-2 in Z[zeta_17], p2 the prime above 2 with
valuation 2; e not in p2; coefficients at most 601 bits; Straus
multi-scalar multiplication with NAF digits (3,187 nonzero digits).
Alternative (integer cofactor of about 10,200 bits) rejected as about
three times slower. Measured: one addition 8-9 s on Chatelet. Since
Frobenius has order 17 on V_b and acts through F_2[Frob], each nonzero
point gives an 8-dimensional F_2-space; three points should suffice.
Not yet verified: that the computed points are nonzero 2-torsion (runs
in progress); the p-adic lifting stage is not designed in detail.

<!-- D162 -->

**D162 (2026-11-15): step-3 design; target isolation holds at 673.**
Isolation: L_Y mod 2 = (t+1)^96 * (two degree-8 factors, system a,
multiplicity 1) * g^2, g | t^17-1; so V_b is exactly ker g(Frob) on
J(Y)[2], and #J(Y)(F_673^17)/#J(Y)(F_673) has 2-valuation 16. A torsion
point: x random in J(K), (Frob-1)x, times the odd part of
Res(L, Phi_17) (about 10200 bits). Engine choice: own Makdisi
evaluation-representation code in Magma on Chatelet (already used on X),
rather than Mascot's PARI code, for the mod-p gate; alternative kept for
the p-adic stage. Benchmark: Makdisi-size primitives over F_673^17 take
1-3 s, so one point is estimated at about a day of one core (estimate,
not measured). Model of Y: sections of pi^*(D_C) on Y are
s0 + s1*v + tau(s1)*a/v with v^3 = h, s0 in L_C(D_C),
s1 in L_X(E_R - D_minus - pi^*G); with D_C = 2H - G, G = 17 rational
points of C with no rational point of Y above, D0_Y has degree 129 and
66 sections (28 + 38). Evaluation points: the rational points of Y
(692 > 4*129), so no extension-field points are needed in the model;
K-points of Y are needed only to form random classes. Possible later
saving: replace the integer cofactor by a short element of Z[zeta_17]
(about 600-bit coefficients).

<!-- D161 -->

**D161 (2026-11-15): genus-64 cover built mod 673; point count matches Hecke.**
Inputs: T_P charpolys at the norm-673 prime on the p2-new (16+24) and
p2^2-new (48) spaces. Outcome: Prym order prediction 3^2*m verified in
the form m*Delta = 0; Delta has trivial 3-part, so the third is c*Delta
as at 31. #C(F_673) = 670 and #Y(F_673) = 692 match the predictions.
Choice: accept this third without constructing the other eight
candidates, since the first matched; alternative (build all nine, count
over F_673^2 as in D84) deferred as an optional check. New fact: at 673
the CM divisor D17 has one rational point (none at 31); such a point has
transposition inertia and contributes 2 points to Y; script 06 handles
rational D17 and B3 points. The redundant level-p2^2 recomputation in the
first Hecke job was stopped by PID after the parallel job finished.

<!-- D160 -->

**D160 (2026-11-14): 17 is unusable with the current model; use 673.**
Reducing the exact data mod 17: C keeps dimension 1 and degree 30, but the
B3 scheme is nonreduced, the D17 ideal has degree 33 instead of 17, and
the B3 nonic has 17 in its denominators. The coordinates were normalized
by traces over the degree-17 CM divisor, so 17 is special for the model
whatever the reduction of the curve itself is. Alternatives: change the
model at 17 (unknown effort); 641 (-3 nonsquare, constants F_641^2); 673
(-3 is a square, B3 nonic splits 3+3+3 as at 31, so scripts port
directly). Chosen: 673. Only system b has order 17 at the scanned prime;
that suffices if, as the group structure SL2(F256)^2.C8 indicates, a and b
are exchanged by Gal(F/Q) up to automorphisms of F256 (not checked).
Torsion field F_673^17, about 2^160.

<!-- D159 -->

**D159 (2026-11-14): provisional prime choice 17.** The
[scan](dembele/pivot/results/frobenius_order_scan.md) of 19 primes (norm
up to 991) reproduces Dembélé's orders at 97 and finds order 17 for both
systems at the norm-289 prime above 17; 641 and 673 give 17 for one
system; the rest are 51, 85, 255 or 257. Alternatives: 641/673 (larger
field, one system only), or wait for 7 and 47 (norms 2401, 2209), which
win only if the order there is 3 or 5. Decision: plan step 2 at 17,
revisit when 7 and 47 finish. Unchecked: target isolation in J(Y)[2] at 17
and whether Y has good, usable reduction data there.

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

**D158 (2026-11-13). Pivot from certified identification to compute-then-verify.**
*Fork:* (a) build a Linux adapter and run the 20–27-day P10480 bank to
prove the base identification; (b) de-risk downstream links first, keeping
the bank as the goal; (c) drop the identification proof and verify only
the final polynomial. *Chosen:* (c), by the user, after reviewing the M23
method (final-object verification, coordinate choice over precision, CRT).
*Reasons:* identification is not needed for the stated goal; quadratic
twists cannot change the mod-2 field; a p-adic Y plus functions from the
exact C replaces the exact cubic; the bottleneck is the residue extension
degree, which a better prime may shrink (255/257 at norm 31, 51/257 at
norm 97 are the only known values). *Also decided:* relaxed process for
the new track; the frozen D157 replay is not required on `otto` since
seven external files are unavailable. *Rejected as routes to the field:*
rigidity and Belyi maps (ramification at primes dividing |G|; 2-group
case is the legacy obstruction).

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


A running record of the choices made in the hunt for an explicit polynomial for
Dembélé's nonsolvable field ramified only at 2 — what was considered, what was
chosen, why, and how it turned out. Maintained so that if this project succeeds
(or closes), the path is reconstructible. Results live in `writeup/` and
`dembele/certificates/`; this file records the *forks*.

For the pre-2026-08-11 history (the 2-group Belyi arc → Lemma A/B; the Brandt/HMF
reproduction of Dembélé's computation; the killed constructive routes), see
`writeup/main-result.md`, `HANDOFF.md`, and `dembele/certificates/idea-exhaustion.md`.

---

## 2026-08-11

**D1. Take the M23 paper seriously as a signpost.** Trigger: arXiv:2608.08538
(engine = the KMSV/BelyiDB machinery). Options: dismiss (rigidity controls groups,
not ramification) or investigate whether the method's shape transfers. Chose to
run the M23 "step 1" (Nielsen census) on the Dembélé group's almost-simple
quotient PΓL₂(256). Rationale: cheap (character theory), and the HMF route was at
a hard stop. Outcome: found the all-2-power triple phenomenon — the single
structural discovery the whole arc grew from.

**D2. Pilot at k=4 before attempting k=8.** Options: attack PΓL₂(256) directly
(genus 28+, unknown feasibility) or calibrate on PΓL₂(16) (genus 0, M23-easier).
Chose k=4, explicitly as a *negative control*: the k=4 target field doesn't exist
(LMFDB/HMF sweep), so the pilot's guaranteed failure would reveal the obstruction
mechanism. This framing ("where does the guaranteed failure materialize?") drove
everything after.

## 2026-08-11/12 — the pilot

**D3. Precision vs coordinates.** The Belyi package's recognition failed at every
precision (115 → 500 digits; certified relation finder confirmed "insufficient").
First response (wrong): raise precision — the same reflex Zhang's note records the
AI systems having in the M23 project. The user supplied Zhang's account; pivoted
to Galois-equivariant coordinates (canonical points → 0, 1, ∞) and recognition of
Newton *factors* instead of expanded polynomials. Outcome: instant success at
existing precision. Lesson institutionalized: gauge first, digits second; detect
spurious LLL fits by noise-floor height + precision-instability.

**D4. Trust but verify the numerics: certificates over faith.** Every exact cover
was required to pass (i) the exact passport identity over its field and (ii) a
rigorous `GaloisGroup` monodromy certificate. Cost: hours. Benefit: the k=4
conclusions are unconditional, which mattered later when the whole negative arc
leaned on them.

**D5. Compute the local mechanism rather than accept "bad primes = {2,5,17}".**
Options: record the disc and move on, or do place-by-place reduction analysis.
Chose the latter; found the mixed ordinary/supersingular structure and that ≥ 2
conjugate covers are good at every odd prime — relocating the obstruction from
geometry to the moduli field. This reframing produced the decisive question for
everything downstream ("is the k=8 moduli field only-2-ramified?").

## 2026-08-12 — probing the family

**D6. The twist probe instead of a k=8 computation.** To predict k=8 without the
genus-28 computation: sought a group-theoretic marker separating the ramified
primes {5,17} from the unramified {3} at k=4. Rejected en route: char-p Gröbner
counting of covers (the profile doesn't isolate the monodromy group at degree
≥ 17 — recorded as a dead end). Found: the Frobenius-twist fixing criterion,
with the (later proved) congruence that +1-torus primes always fix. Honestly
labeled the inductive step ("fixing ⇒ deficiency ⇒ ramification") a *transfer
hypothesis*, n=1-group calibration.

**D7. Search breadth before depth.** With rigidity "predicted dead," options were
(a) accept and pivot entirely, or (b) run cheap breadth searches for escape
hatches before closing. User chose (b): braid-orbit census (r=4), Suzuki census.
Outcome: Suzuki closed by the same congruence (now proved for q²+1); the braid
census found genuinely short orbits — the escape hatch candidates.

**D8. Boundary maps as the cheap oracle.** To determine the short components'
fields, options: compute a family explicitly (heavy) or exploit degeneration to
already-computed triples (cheap, convention-risk). Chose boundary maps; the
(4,4,8,8) components landed bijectively on the golden triples (inheriting K), and
the (8@φ)⁴ components on the *uncomputed* genus-1 passport — concentrating
everything in one new computation instead of many.

**D9. Genus-1 verdict via j-invariant, not package recognition.** The package's
genus-1 recognition crashed (bug found, patched: TrialDivision guard + dump
hooks). Rather than debug the full pipeline, recognized the gauge-invariant j
from dumped Newton data. Outcome: degree-8 minpoly, field ≅ K — the k=4 closure.
Same philosophy as D3: choose the invariant, not the coordinates.

## 2026-08-13 — the pivot and the period route

**D10. Declare the covers arc closed and write it up.** With k=4 closed and the
family conditionally closed, options: push k=8 numerics anyway, or bank the
result and pivot. User asked for the step-back; chose to write
`writeup/all-2-power-covers.md` (the sequel to the thesis's negative result) and
pivot to the period route. k=8 left as a *falsification target*, not a project.

**D11. Reopen the audit's one unkilled door: level-raising + CD.** Re-read
`idea-exhaustion.md`; the entry "Level-raising + CD at an auxiliary prime —
speculative" was the only non-dead constructive route. Computed the archimedean
feasibility first: ζ_F(−1) = 5820 ⇒ Shimura-curve genus ≥ 91(Nq₀−1)/2 — dead.
Recognized that Cerednik–Drinfeld (the "CD" in the audit's own label) converts
the problem to q₀-adic periods computed from Dembélé's *definite* algebra — the
Greenberg–Voight method, previously killed only because level 1 has no finite
disc prime. Level-raising manufactures the prime. Plan of record:
`dembele/certificates/levelraise-cd-plan.md`.

**D12. Gate the route; scan first.** Ordered the gates by cost: (1) find q₀ with
ā_{q₀} = 0 (scan), (3) verify the congruence at level q₀ directly (don't trust
mod-2 level-raising theorems), (4) CD/GV implementation (de-risk via
`darmonpoints` on a small case). Launched the scan on chatelet after measuring
local cost (950 s/prime — never scan locally).

**D13. The conjugate-grouping correction.** User challenged the Chebotarev
heuristics ("asymptotic — could take a while"). Re-examination found worse: V16
is Gal(F/Q)-stable, so the 8 primes above a rational prime share one parity
verdict — the sample size was 8× overstated (and the v1 scan wasted 8× compute).
Deployed scan v2 (one prime per rational prime, norm ≤ 20000, ~280 independent
samples, ~2/3 heuristic odds; honestly noted that effective Chebotarev is vacuous
at this conductor). Lesson: user-side skepticism of statistical claims pays.

## 2026-08-13/14 — adversarial audit and parallel probes

**D14. Adversarial self-audit of the covers arc.** On user request, ranked the
weak links: transfer hypothesis > boundary-map convention > weight overclaims >
genus-1 "=" vs "⊇" > completeness. Fixed the writeup (weights → certified
bounds; ⊇; k=2 rung). Two items resolved by *argument*: completeness/transitivity
certified by the degree-8 coefficient; the boundary convention forced by the
generating-vs-subgroup dichotomy (exactly one merge ordering gives generating
triples, and it is bijective). Submitted the fixing congruence to Aristotle for
Lean formalization (project 11dcaed0, `aristotle_fixing/`). **Outcome (2026-08-16):
all three theorems proved — 0 sorries, no new axioms — and Aristotle noted the
Suzuki evenness hypothesis is unnecessary, slightly strengthening the lemma.**

**D15. Probe everything cheap in parallel while the scan runs.** User chose
breadth: Sz(8) covers (independent-family hypothesis test), the k=4 genus-2
corner (universality test; also decides the twelve [10,10,11,11] components via
their cusps — found cusp-bijective by capped-BFS sampling after the full-closure
approach was killed by a 1.5M-element orbit), exact k=8 Nielsen counts
(Ni_gen = 32 for (2,8,16), 200 for (2,8,8); forced layers Q(ζ₈) and Q(√2)).
Operational lessons accumulated: chatelet detached-nohup for everything heavy;
memory pressure kills the biggest local jobs; the recognition/optimization layer
(not numerics) is always the failure point — genus-2 stalled in Polredbestabs on
degree-24 junk-gauge fields (response: hyperelliptic dump hook + offline Igusa
plan), Sz(8) needed a precision sweet spot (40 too low for the hyperelliptic
rank test, 115 too high for memory; trying 70).

**D16. Diagnose "try higher precision" as a bug, not a precision problem.** The
Sz(8) hyperelliptic test failed identically at 40 and 70 digits ("multiple
relations"). Precision-independence of a numerical failure ⇒ structural cause:
found the relation-matrix column count hard-coded (`+15` hack, flagged TODO in
the package source) — sufficient at genus ≤ 4, under-determined at genus 8, so
the kernel keeps noise vectors at any precision. Patched to scale with genus
(fourth upstream-worthy `~/Belyi` patch: TrialDivision guard, two dump hooks,
column count). Meta-lesson, same family as D3: when raising precision doesn't
change the failure, the failure is not about precision.

**D17. Park the Sz(8) probe.** The widened matrix (D16) did not fix the
hyperelliptic test: the kernel is genuinely multi-dimensional — the package's
automatic coordinate choice (ratios of the first basis forms) degenerates on
this curve, independent of precision. Fixing coordinate selection is a rabbit
hole; the right tool for a genus-8 (likely non-hyperelliptic) curve is the
vBCPS26 canonical-embedding method — a proper mini-project. Parked with blocker
documented; the independent-family hypothesis test is deferred, not abandoned.
The genus-2 corner (imminent) carries the audit's validation weight meanwhile.

**D18. Ops incident: fleet deaths, real and imagined.** The chatelet project
restarted (twice), killing all detached jobs — real. The subsequent "instant
deaths" of relaunched jobs were **not** real: the verification pattern
`pgrep -f "magma -b"` never matched the actual process (`magma.exe -b` after
the wrapper exec), so healthy fleets read as dead, triggering an escalating
false diagnosis (session reaping? memory kills? — sentinel and memory-hog
probes both came back clean, which was the tell). Resolutions: (a) scan
progress is checkpointed via the DONE skip-set, so restarts lose little;
(b) staggered relaunches (30 s gaps) — the one bulk 11-job relaunch died,
plausibly a startup stampede; (c) liveness monitoring on *verified* process
patterns, since a dead fleet writes nothing and looks identical to a quiet
one. Meta-lesson, the operational cousin of D16: before theorizing about a
mysterious failure, verify the measurement instrument. Final resolution: the
"unkillable survivors" were other tenants' Magma jobs — the shared host exposes
other CoCalc projects' processes in ps, so every unfiltered count was polluted.
All fleet accounting now filters by uid (`ps -u $(id -u)`).

**D19. The fixing congruence is now machine-checked.** (Same event as the
outcome line appended to D14 by a concurrent session in `d50f0c4`; this entry
carries the detail.) The Aristotle project
`aristotle_fixing` (submitted 2026-08-13) returned proved: `FixingCongruence.lean`
contains three theorems — `fixing_congruence_gl` (`p | 2^{2^j}+1 ⟹ 2^{j+1} | p−1`),
`fixing_congruence_sz` (`p | q²+1 ⟹ p ≡ 1 mod 4`), and `twist_fixes`
(`x^{2^m} = 1` and `2^m | p−1 ⟹ x^p = x`) — with no `sorry` and no new axioms
beyond `propext`/`Classical.choice`/`Quot.sound`. All three route through one
helper: if `a^{2^n} = −1` in `ZMod p` then `ord(a) = 2^{n+1}`, so `2^{n+1} | p−1`
by Fermat. Note the reported slack: the Suzuki statement never uses evenness of
`q`; it holds for every natural `q`. Banked in `aristotle_fixing/` alongside its
toolchain pin (`leanprover/lean4:v4.28.0`) and cited in
`writeup/all-2-power-covers.md` §6. This is the second Lean-certified component
of the project after Lemma A. The *transfer* hypothesis ("fixing ⇒ deficient ⇒
ramified") remains empirical — formalization does not touch it.

**D20. Credential outage, and the duplicate-work bug it exposed.** The
chatelet account API key stopped authenticating (`/api/v1/ping`, which takes no
arguments, returned "No account found" under all four auth encodings, while
`/customize` served 200 — so: key revoked or expired, not an outage). The key
was rotated by hand; `remote_magma/set_key.py` now does that rewrite without
echoing the key, and `.env.bak` was added to `.gitignore`, which the bare
`.env` rule did not cover.

The reconnect survey (`remote_magma/reconnect.py`, read-only by design) found
all 8 lanes alive at 19.5 h uptime — the fleet had survived the whole outage —
but every lane had spent that time **recomputing a prime it had already
finished**: 1249, 1279, 1409, 1439, 1471, 1567, 1601, 1663, at 14–20 h each,
≈130 CPU-hours lost. Cause: a restarted lane always resumes at its first
non-`DONE` prime, and `DONE` is a static literal in the script, so results not
hand-harvested are replayed. HANDOFF said "harvest before any rescan edits";
`restore_scan.py` restarts lanes automatically and never harvests, so the
instruction could not hold in practice. **Lesson: a manual step in the recovery
path of an automated restart loop is a bug, not a procedure.**

Fix, in the script rather than the runbook: (a) *self-harvest* — `DONE` is
augmented at startup from every prime recorded in the lane logs, matched on the
full `q over NNN): trace` pattern so a half-written line from a killed process
cannot register a truncated prime; (b) *stable assignment* — lanes are assigned
by position in the FULL sorted prime list before done-filtering, since with the
filter applied first, two lanes restarting with different harvest sets can be
handed the same prime. (b) is backward-compatible: the 24 statically-DONE
primes are exactly the 24 smallest by norm and 24 ≡ 0 mod 8, so the historical
assignment is unchanged — verified by recomputing the ordering independently in
Python and matching all 8 observed lane-to-prime pairs. Results are now banked
in the repo (`dembele/scanjob/scan_results.csv`) instead of living only in
remote `*.out` files, and the lane script itself
(`dembele/scanjob/37_levelraise_lane.m`) is committed — it had existed only on
chatelet, so a project wipe would have made gate 1 unreproducible.

Scan state after harvest: 32 rationals scanned, `const2val = 0` throughout, 0
hits. Cost is 14–20 h per prime and rising with norm.

**D21. The genus-2 corner is precision-blocked, and the instrument says so
honestly.** The 24 h local run produced its dump; no absolute Igusa invariant
admits a certifiable relation of degree ≤ 24. The verdict is *precision*, not
mathematics: the numerical curve carries ~25 correct digits of the 285 it
formally reports. Established three ways — LLL heights growing linearly with
precision at every degree (noise, not a relation); a gauge probe showing the
Igusa formulas themselves preserve 257–274 digits; and the package's own two
outputs of the same curve (pre- and post-`TriangleRescaleCoefficients`, proved
identical up to a weighted gauge by the ratio pattern) agreeing to only 24–26
digits. The loss is upstream, in the power-series → `NumericalKernel` curve
solve; the Arnoldi eigenvector itself converged to 1e-273, and there is no
Newton refinement anywhere in the genus-2 path to recover it. Corollary: the
package's own `MakeK` search at `DegreeBound = 24` was running on the same
~25-digit data and could not have succeeded legitimately — a hit there would
have been spurious. Full argument in
`dembele/certificates/g2-corner-precision.md`.

**Lesson worth keeping:** a recogniser must be able to *fail*. The first
version of `32_g2_field.m` used a fixed height threshold, which neither
rejects a marginal noise fit nor accepts a genuine large-height one; the
precision-ladder test (does the fitted polynomial stop moving as precision
rises?) distinguishes them structurally, and it is what turned "no answer"
into the diagnosis above rather than a plausible wrong field. Also switched to
the low-weight ratios `I4/I2^2, I6/I2^3, I10/I2^5`: same field, but the
classical `I2^5/I10` triple is weight 30 and reaches height 1e22 at degree 12,
beyond certification at any precision this run could offer.

Options recorded, none taken unilaterally: rerun at ~500 digits (~a week,
since the ~260-digit conditioning loss is roughly constant in the working
precision); diagnose the kernel solve (cheaper if the ill-conditioning is a
construction detail); or leave it — this corner verifies an arc already closed
and written up negatively, and is not on the critical path.

**D22. Ops: the fixer caused the fault it was built to prevent.** After the
recycler retired four lanes at once, half the fleet sat idle waiting for the
watchdog's 10-minute sweep, so I ran `restore_scan.py` by hand to bring them
back sooner. The watchdog swept at the same moment; both censused, both saw the
same lanes missing, and both launched them. Lanes 3 and 4 ended up with two
processes each — quietly duplicating a 14-20 h prime, which is precisely the
waste D20's self-harvest was introduced to stop. Duplicates were identified by
the uid-filtered, environ-based census (D18) and the younger process of each
pair killed.

The bug was latent in `restore_scan.py` from the start: census and relaunch are
separate round trips, with no interlock. Impatience only exposed it. Fixed with
a local `flock` plus a re-check of each lane immediately before launching.
**Lesson: an idempotent-looking repair tool that is not actually idempotent is
a loaded gun, and the moment you reach for it manually is exactly when the
automation is also running.** Prefer waiting for the scheduled sweep, or make
the tool safe to run concurrently — we did the latter.

**D23. GATE 1 IS SATISFIED: q0 = the prime above 7 of norm 2401.** On
2026-08-22, after 53 rationals scanned, lane 0 returned
`Nq=2401 (q over 7): trace=0 const2val=8 <== LEVEL-RAISING PRIME` (128 700 s).
Since `v_2(Norm a_q) = 8 v_lambda + 8 v_lambda'`, a valuation of exactly **8**
forces `v_lambda + v_lambda' = 1`: precisely one of the two primes above 2
divides `a_q`, i.e. `abar_q = 0` for exactly one of Dembele's two residual
systems. That the valuation is exactly 8 — the residue degree — rather than
some arbitrary even number is itself a consistency check that a spurious or
buggy verdict would be unlikely to pass. Single occurrence, no conflicting
verdict for q = 7 anywhere in the logs.

**This is what the entire period route was dammed behind.** Every gate from 3
onward was scoped, costed and waiting on it.

**Two pieces of luck worth recording.** (i) The norm is 2401, comfortably inside
the affordable window: gate-4 cost goes as `Nq0^2`, and 2401 sits close to the
2111 used in the cost tables (a 1.29x multiplier — ~157 core-hours at M = 20),
far from the norm-5000 decision point where a hit would have become painful and
20000 where it would have been useless. (ii) It arrived at the 53rd rational
rather than deep in the tail; the cumulative-odds table put ~28% by norm 5000.

**Not yet trusted.** The plan of record deliberately makes gate 3 a
*verification* rather than an assumption: compute the level-`q0` Brandt module
and find the Steinberg eigensystem congruent to `f` mod `lambda`, instead of
relying on mod-2 level-raising theorems. That is now the immediate next action.
Note `q0` has residue degree 4 (`2401 = 7^4`), which is fine for the parity and
CD arguments — they need only *a* finite prime — but means the local field at
`q0` is the unramified quartic extension of `Q_7`.

The scan continues: a second hit at lower norm would be cheaper downstream, and
redundancy matters if gate 3 rejects this `q0`.

**D24. Gate 3: surgery on the pinned HMF package, and why we are verifying
rather than invoking Ribet.** Two forks resolved on 2026-08-22.

*(a) The package could not build the objects.* Level `q0` has dim **109240**
(14 s to compute — the mathematics was never the issue), but `definite.m`
materialises dense `dim x dim` matrices, 45.5 GB apiece here. Two sites, both
patched additively and recorded in `dembele/patches/`: the Hecke assembly, and —
the binding one, since it fires first — `BasisMatrixDefinite`. The finding there
is worth keeping: at parallel weight 2 every per-factor `basis_matrix` is the
**identity** (the package's own `TO DO` calls them removable), so
`basis_matrix_big` *is* the identity, built densely and inverted by a global
`Solution` call. 45.5 GB twice plus an O(n^3) solve, to construct and invert an
identity matrix. Downstream it is read only through `Ncols`/`Nrows`, and its
inverse never at all. Verified by comparing against the pristine package: level 1
for the Hecke hunk (`Matrix(sparse) eq dense`, V16's degree-16 factor unchanged),
and — since level 1 takes the "easy" branch and never reaches the basis-matrix
code — **level 31** for that one, matching on dimension, `Nrows`, trace, and the
sum and sum-of-squares of every entry of `T_97`. At level `q0` the operator now
builds in 963 s with 3 494 618 nonzeros, **31.99 per column** against the
predicted `Norm(p)+1 = 32`. This surgery was required for gate 4 regardless: the
level-`q0` module *is* the Bruhat–Tits tree quotient.

*(b) Verify, or invoke the theorem?* The plan said "verify, don't trust mod-2
level-raising theorems", and on inspection that instinct was right. Level raising
for Hilbert modular forms is general **for `ell > 2`**; `ell = 2` is a separate
and delicate case (there is a dedicated literature on it). Worse, Rajaei's
theorem carries a hypothesis for even `d = [F:Q]` requiring the automorphic
representation to be **special or supercuspidal at some finite prime** — and our
`f` has level 1, so it is unramified at every finite prime. Our configuration
(`ell = 2`, `d = 8` even, level 1) sits exactly in the corner the theorems avoid.
So: **direct verification**, not invocation. *(This reading is from secondary
sources; the primary text should be checked before either conclusion is
published.)* Running: `charpoly(T_31 mod 2)` at level `q0`, testing whether the
residual invariant `g16bar` divides it and with what multiplicity.

*Method lesson, twice earned.* Both of this session's serious mis-estimates were
unmeasured guesses about constants: the overconvergent inner loop (wrong by
1300x, because a distribution action is `O(M^2)` with Python overhead, not the
`O(M)` vector op I timed) and dense `GF(2)` multiplication (wrong by ~15x in the
*pessimistic* direction — Magma is bitsliced, so `n = 109240` costs ~22 min, not
the ~5 h I asserted; that error nearly discarded a viable approach). **Measure
the constant before letting it decide anything.**

**D25. Gate 3 has positive evidence; U_q0 is the first job the durability
chain did not cover; and a self-correction on gate 5.** Three things since D24.

*(a) The congruence shows up, twice.* With the package surgery done, the test is
whether the residual invariant of `rho-bar_f` appears at level `q0` beyond what
oldforms explain. It does, and only on one side. `g16bar` splits into two
*distinct* irreducible degree-8 factors — one per prime above 2 in `H`, i.e. one
per residual system — and against an oldform baseline of 2 each:

| `ell` | one factor | the other |
|---|---|---|
| 31 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |
| 97 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |

The `ell = 97` invariant is a different polynomial tested against a different
operator, so it is a second draw, not a restatement. And the side carrying the
excess is the side gate 1 predicted: `const2val = 8` means
`v_lambda + v_lambda' = 1`, so exactly one system has `abar_q0 = 0`. Three
computations sharing almost no machinery agree. **The baseline is not an
assumption either** — the non-raising system is its own control, sitting at
exactly 2 in both rows.

Not yet established: that the two excesses are the *same* subspace, and
Steinberg. One computation settles both — `dim ker(U_q0 - 1)` on the excess
subspace. Note the naive test is vacuous: oldforms satisfy
`x^2 - a_q0 x + Nq0`, which mod 2 is `(x+1)^2` precisely *because* `a_q0 = 0`
mod `lambda` — the very hit that makes `q0` interesting collapses the obvious
Steinberg check, and the separation has to come from `U - 1` being nilpotent
nonzero on the old part but zero on the new.

*(b) A 40–50 h job cannot run unprotected on this host.* `U_q0` was launched as
a bare `nohup` and chatelet restarted after ~18 h, destroying it. The scan's
chain (`project_init.sh` → supervisor → lanes) came back automatically with
exactly one process per lane and no duplicates — its first real test against a
project restart, passed — but `U_q0` was outside that chain. Observed uptimes
between restarts: ~3 days, ~5 days, then this one. A job needing two days is a
coin flip, and without checkpointing each failure costs everything. Response:
chunk it. `HeckeOperatorDefiniteBig` already takes `Columns`, so the operator
can be assembled in column blocks that are disjoint and simply add; each block
is banked, so a restart costs one block. **Lesson: durability is a property of
the *job*, not of the host — and "it survives session close" is not the same as
"it survives the host".**

*(c) I was wrong that gate 5 was under-specified.* I claimed reaching a global
polynomial from q0-adic periods had no stated mechanism and would need a model
of a 16-dimensional abelian variety. `csv-paper-adaptation.md` states the
mechanism: the **257 λ-isogeny neighbours are the 257 points of `P^1(F_256)`**,
Galois permutes them, and a separating invariant evaluated at each gives the
degree-257 polynomial. No model is needed — only separation. The narrower real
gap is that the Eisenstein prototype is archimedean while the route is q0-adic;
but for a Mumford-uniformized variety the periods are topologically nilpotent,
so the same q-expansion converges with `q^nu` replacing
`exp(2 pi i Tr(nu z))`, as on a Tate curve. Enumeration and divisor sums carry
over; only evaluation and cutoff change. What genuinely remains unverified:
whether the invariant separates 257 neighbours at genus 16 (17 at genus 4 is
all that is tested), and the q0-adic term count, which depends on period
valuations. Detail: `dembele/certificates/gate5-padic-eisenstein.md`.

**D26. Gate 3 is verified to the eigensystem level, and the audit that got it
there.** On request I re-audited the chain step by step
(`dembele/certificates/gate3-method-audit.md`) rather than trusting it, and two
of the seven links turned out to be load-bearing assumptions I had never checked.

*(a) The oldform baseline — the one that could have voided everything.* The
excess argument reads "multiplicity 4 at `q0`, baseline 2, excess 2". But the
baseline is `2*m1`, where `m1` is the multiplicity of the residual factor at
**level 1** — each level-1 form with that residual system contributes two
oldforms. I had assumed `m1 = 1` without checking, and at `m1 = 2` the baseline
would be 4, the excess zero, and the `ell = 97` "corroboration" would have been
the same error twice. **Verified:** against the *full* level-1 charpoly mod 2
(degree 58, not just `V16`), both degree-8 factors occur with multiplicity
exactly 1. Baseline 2 confirmed; the excess is real.

*(b) Banked operators from different sessions are incomparable.* The eigensystem
test failed with `Solution: No solution exists` — `T_97` did not preserve
`ker f1(T_31)`, impossible for commuting operators. Direct check: the banked
pair failed to commute on 5 of 5 random vectors. They had been built in separate
Magma sessions, and the package's internal ordering (ideal-class reps, unit
generators, `P^1` enumeration) is not reproducible across sessions. Crucially
this does **not** touch the multiplicity results — characteristic polynomials
are basis-independent — but it invalidates any *joint* analysis. The alternative
explanation, that the sparse patch was simply wrong at level `q0`, had to be
excluded rather than assumed: rebuilding both in one session gave
`COMMUTE = true` (0 failures of 8), which also became **the strongest validation
the patch has had at level `q0`**, where previously only the
nonzeros-per-column shape check applied. **Rule: never combine banked operators
from different sessions.**

*(c) The eigensystem evidence itself.* `W = ker f(T_31)` at level `q0` is
16-dimensional, and `charpoly(T_97|W)` is a *single* degree-8 irreducible
squared, matching a factor of the independently computed level-1 `a_97`
invariant — a two-prime eigensystem match on the actual subspace, which the
multiplicity method could not reach (audit step 7).

*(d) A third signature, unlooked for.* The kernel dimensions give the Jordan
structure over the residue field. `f1`: primary dimension 32, `dim ker = 16`,
so blocks of **size 2** — non-semisimple. `f2`: primary dimension 16,
`dim ker = 16` — semisimple. Congruence between an oldform and a newform
produces exactly that non-split gluing, and it appears **only** on the factor
carrying the excess. Three independent observations now agree: the gate-1
valuation, the multiplicity excess at two primes, and the Jordan structure.

Running at session close: a four-prime test (31, 97, 127, 191) in one session,
computing each kernel once and restricting every operator to it, and printing
*which* level-1 factor matches so the correspondence is checked rather than
assumed.

**D27. Three forks on 2026-08-26: the scan is wound down, the four-prime job
was vacuous and is replaced, and the Eisenstein back end has a computable
go/no-go.** Resumed from handoff; every item below is recorded before its
outcome is known.

*(a) Scan: `STOP_SUPERVISOR` set, fresh lane 0 retired.* The host had 0 GB
available (7 lanes at 14–17 GB each, plus a just-relaunched lane 0 about to
grow into the same 16 GB the gate-3 job needs). The handoff itself recommended
winding down to 2–3 lanes: `q0` is banked, the primes now cost ~2 days each
(norms ≈ 3000), and further hits are redundancy. Chosen: stop relaunches
(`touch two_scanjob2/STOP_SUPERVISOR`), kill only the 52-minute-old lane 0,
let the seven in-flight lanes finish their primes and exit. Not chosen: killing
in-flight lanes (43 h of work each), or editing `NLANES` while lanes with
`NLANES=8` are mid-prime (the position-mod-`NLANES` assignment would double-
assign their primes). **To resume at 3 lanes** once the fleet has drained: set
`NLANES=3` and the loop `for L in 0 1 2` in `two_scanjob2/supervise.sh`,
mirror it in `remote_magma/restore_scan.py`, remove the STOP file, relaunch the
supervisor with the command in its header. Doing that before the lanes drain
duplicates work.

*(b) `47_gate3_multiprime.m` retired; `48_gate3_genkernel.m` launched.* While
writing the closure argument I found that the eigenspace `W = ker f1(T_31)`
used for the step-7 "eigensystem match" is, under Ihara's lemma, exactly the
mod-2 old subspace: `O` (two copies of the level-1 `f1`-part, `T_31`
semisimple on it) sits inside `W`, and both are 16-dimensional. Restricting
`T_ell` to `W` then re-derives level-1 data by construction; the running
four-prime job could not have distinguished "new forms congruent to `f`" from
"not". Full argument in `gate3-method-audit.md` (2026-08-26 section). The
replacement restricts to the 32-dimensional generalised eigenspace
`G = ker f1(T_31)^2` and tests `charpoly(T_ell | G) = (f1^{(ell)})^4`, which is
equivalent to the **new quotient** carrying `f`'s system at `ell` because the
old contribution `(f1^{(ell)})^2` is forced by local theory (two Iwahori-fixed
vectors per unramified principal series). No degeneracy maps are built — the
second one needs `get_tps` at `q0`, the `U_q0` cost. Extra cost over 47: one
dense `GF(2)` multiply and one kernel. The banked, basis-independent level-`q0`
characteristic polynomial selects the excess factor so the non-raising side
(old forms only) is skipped. The script's level-1 phase was validated locally
at level 31 and its tail on a synthetic commuting pair with the expected
Jordan structure (`[4, 2]` multiplicities, quotient `= level-1^2`). Killing 47
cost 3.3 h of sunk compute; its four operator builds could not be reused (they
die with the session) and its output was uninterpretable.

*(c) Gate 5: term count quantified; gate-4 build blocked on one determinant.*
`gate5-genus16-term-count.md`. The Fourier-term count obeys
`sqrt(D)·C^n/(n!·N(y))`, validated on all three genus-4 counts to 0.3%. At
genus 16, with the integrality of the q0-adic valuation pairing, it is bounded
by `1.1·10^4 · M^16 / Δ'`, `Δ'` = determinant of the period-valuation pairing
relative to unimodular. Feasibility needs `Δ' ≳ 10^20–10^30`, i.e. period
valuations of tens, and large valuations raise the recognition precision `M`
which gate 4 pays for quadratically. `Δ'` is computable now from the level-`q0`
character group (monodromy pairing on the `g`-isotypic part) — the right next
computation and the one that can invalidate the gate-4 build. The handoff's
item 3 (an archimedean "separation test" at genus 16) is not the binding
question and is not being run. Side finding: `ζ_H(−3) ≈ 10^{87.7}` makes the
constant-term-1 `E_4` equal to `1 + O(10^{−13})` on the whole fundamental
domain — a scale artefact of the discriminant, removable by rescaling but
requiring `ζ_H(−3)` exactly; irrelevant q0-adically.

*Operational.* `Bash run_in_background` here kills its process after ~2 h; the
local smoke test died at the level-31 phase and was relaunched with
`nohup … & disown` (macOS has no `setsid`). The first chatelet launch of 48
through `cocalc.py exec` died silently after ~15 min: CoCalc applies the
`project_exec` timeout to the command tree as `RLIMIT_CPU` (default 120
CPU-seconds), and `setsid`/`nohup` do not shed an rlimit. Relaunched via
`rexec(..., timeout=86400*3, sock_timeout=60)` — the pattern `CHATELET.md`
and `restore_scan.py` already prescribe. Lesson re-learned: a detached launch
must go through `rexec` with an explicit CPU limit, never through a plain
`exec`. Attempt 2 then ran 11 h, built all four level-`q0` operators
(**commuting pairwise, 0 failures of 27 checks** — the sparse patch validated
at four primes in one session), evaluated `f1(T_31)` (3938 s) and squared it
(585 s), and died at its own 16 GB cap on the kernel: four dense `GF(2)`
operators at 1.5 GB each plus two dense polynomials plus the kernel workspace.
The cap was inherited from 47 without re-measuring — the D24 lesson again.
Attempt 3 (2026-08-27 03:xxZ) keeps the operators sparse (dense only for the
polynomial evaluation), prints memory at each checkpoint, runs under a 40 GB
cap (47 GB free after four lanes exited), and **banks the four integer sparse
operators** (`two_gate3/gk_s3_T{31,97,127,191}.m`, ~120 MB each) — a
commuting set in one basis, which the `Δ'` computation over `Z` will need.

**D28. GATE 3 IS CLOSED: the level-`q0` new quotient carries `f`'s residual
system at 31, 97, 127 and 191.** `48_gate3_genkernel.m`, attempt 3, finished
2026-08-27 10:26Z (`dembele/data/computed/gate3_genkernel_q0.out`,
`gate3-closure.md`). On the 32-dimensional generalised eigenspace
`G = ker f1(T_31)^2` every one of the four commuting operators has
characteristic polynomial `(f1^{(ell)})^4`; the old part accounts for
`(f1^{(ell)})^2` by local theory, so the new quotient has `f`'s system at all
four primes, with the pairing of the four polynomials fixed by the single
prime `lambda` on the `f` side. `T_31` has Jordan blocks of size 2 on `G`
(rank 16), semisimple on the old part — now a corollary of the congruence, not
a signature (D27b). Steinberg at `q0` follows from newness at prime level with
trivial character. Not proved and not needed: `rho-bar_g = rho-bar_f` itself
(no affordable Sturm bound; a Galois-conjugate system cuts out the same field;
the gate-5 certification is the backstop).

*Decision:* the Hecke side of the route is done; no more primes will be added
(each costs a full same-session rebuild, ~5 h, for evidence that cannot become
a proof this way). The four integer operators are banked from this session
(`two_gate3/gk_s3_T*.m`, commuting, one basis) as the input for the next
computation, `Delta'` (D27c), which is now the binding question of the whole
route. The scan stays stopped: `q0` is confirmed level-raising in the strongest
sense a finite computation gives, so redundancy has little value; resume at
three lanes only if a *second* `q0` is wanted for downstream reasons (e.g. a
smaller norm for gate 4).

*Method note.* Two of the three "independent signatures" of D26 turned out to
be one signature (the multiplicity excess) plus one vacuous test plus one
ambiguous one; the version that actually decides the question needed a
quotient, not a subspace, and it needed no new mathematics — only asking
what output the test would produce if the claim were false.

**D29. `Δ'` is computed as the mass-Gram of the `g`-sublattice, not a graph
kernel — the character group needs no boundary map.** With gate 3 closed, the
binding question is `Δ'` (`gate5-genus16-term-count.md`). The certificate
framed it as a monodromy pairing on `X = ker(∂: Z[edges] → Z[vertices])` and
flagged the integral kernel of `∂` on the 109240-dim space as the obstacle.
That obstacle is illusory: `g` is **new** at `q0`, so it lies in the kernel of
both degeneracy maps to level 1, i.e. `∂ = 0` on the whole `g`-part. Hence the
`g`-isotypic part of the raw Brandt lattice already *is* its character lattice,
and the monodromy pairing is the diagonal Brandt mass pairing
(`InnerProductMatrixBig`, verified diagonal at parallel weight 2,
`definite.m:748`) restricted to it. `Δ'` is therefore
`det(B W Bᵀ)/(N(𝓛)²·D_H)` for a saturated `Z`-basis `B` of the `g`-sublattice
and mass vector `W` — no graph, no `get_tps`, no boundary operator. Plan in
`gate5-delta-prime-plan.md`; the raw operators we banked (`gk_s3_T*.m`) and the
mass vector share a basis, so they compose directly.

*Package change (recorded as a patch, D-worthy because results depend on it):*
the mass pairing was not reachable from outside the package —
`InnerProductMatrixBig` is internal and the cuspidal `InnerProductMatrix`
errors "Not implemented" on these spaces. Added a two-line additive intrinsic
`InternalHMFRawInnerProductDefinite` (+ a `forward` declaration),
`dembele/patches/hmf-raw-innerproduct.patch`, applied locally, **not yet on
chatelet**. First fact it produced: at level 31 the masses are `{1,3}`, not all
equal — some ideal class has an order-3 unit stabiliser — so `W` is genuinely
non-scalar and the pairing cannot be replaced by the standard dot product.

*Status:* the pipeline prototype `49_delta_prime_proto.m` (validate over `Q` at
a small level: self-adjointness of `T` under `W`, new ⊥ old, saturation, the
sub/quotient Gram determinants) is **running at level 31** (`~/dp31_proto.out`),
not yet verified — the level-31 raw operator builds are ~1 h each, so it is
slow for a prototype. Once it passes, the `q0` computation is multimodular:
`det(Γ) mod p` for ~20–50 primes, CRT'd — parallel, ~1–2 core-days, no
host-scale job. Sub vs quotient determinant and the polarisation factor remain
the real ambiguity (`gate5-genus16-term-count.md` §; both reported).

**D30 (2026-08-31). The q0 `Δ'` run identifies `h_g` 2-adically and builds
`L_g` by Wiedemann projection — per-prime full charpolys are rejected; and
`d_g` (16 vs 32) is promoted to the first output.** The D29 plan's step 2 left
"take the `g`-factor `h_p`" unspecified. Costing the naive reading killed it:
a dense mod-`p` charpoly at `N = 109240` over an odd word-size prime is
47–95 GB (no bit-packing) and ~a day per prime — unaffordable for 20–50
primes. *Decision:* (a) recognize the global factor `h_g` from the 2-adic side,
where everything is mod-2 dense (bit-packed, cheap) or 32×32: Hensel-lift the
gate-3 block `ker f1(T_31)²` to `Z/2^192`, take the block charpoly, divide out
the exact level-1 old part `u1²`, and balanced-lift under the Deligne
coefficient bound (`|a_31| ≤ 2√31` ⇒ deg-16 coefficients `< 2^70 ≪ 2^192`);
(b) per word-size prime, get `μ mod p` by Wiedemann (sparse matvecs only),
verify `h_g | μ`, and span `L_g ⊗ F_p` by `(μ/h_g)(T_31)·v` projections —
valid because `W ≻ 0` and `W`-self-adjointness force `μ` squarefree; CRT the
canonical echelon bases, saturate, `Γ = B W Bᵀ` exact. *Alternative rejected:*
computing `charpoly(T_31) mod p` per prime and guessing the factor by degree —
memory-infeasible and the factor is not identifiable mod odd `p` anyway.
*Promoted question:* gate 3's residual multiplicity on the new part is 2
(vs 1 at level 1), so the char-0 orbit could be a single degree-32 orbit; then
`dim B_g = 32` and gate 4's term count is `M^32/Δ'` — a probable no-go. `d_g`
is therefore the run's first deliverable, before `Δ'`. Full mechanics in
`gate5-delta-prime-plan.md` (Addendum 2026-08-31); step-1 script
`dembele/magma/50_delta_prime_q0_W.m` (rebuild `W` + `T_31`, assert equality
with banked `gk_s3_T31` before trusting the pairing).

**D31 (2026-08-31). The monodromy pairing diagonal is the STABILIZER ORDERS
`e_i`, not the Eichler masses — D29's identification of `W` was off by a
reciprocal.** The q0 self-adjointness check (`50_delta_prime_q0_W.m`) failed:
with the Eichler-mass diagonal of `InternalHMFRawInnerProductDefinite`
(`m_i = (ulcm/g)/e_i`, the package's `InnerProductMatrixBig` weights),
`W_i T_ij = W_j T_ji` fails on 304/1197 support entries already at level 1.
Deriving the unique consistent diagonal directly from `T_31`'s entry ratios
along the support graph (connected; zero cycle inconsistencies) gives exactly
the reciprocal pattern: `W'_i · m_i = ulcm/g` for every `i` — i.e. `W' = e_i`,
the stabilizer orders, which is the classical Brandt relation
`e_j T_ij = e_i T_ji` and the Cerednik–Drinfeld monodromy edge lengths
(Gross/Ribet), as it should have been from the start. *Fixes:* new intrinsic
`InternalHMFRawStabOrdersDefinite` (returns `e_i`, `ulcm`, `g`; patch file
revised); since `m_i e_i = ulcm/g` is **basis-independent**, the banked q0
mass vector converts offline — `54_delta_prime_q0_wfix.m` read `C = 48` at q0
(`ulcm 96, g 2`; `e_i ∈ {1,2,3,4,8,16}`) and verified the converted diagonal
is self-adjoint for the banked `dp_T31` on **all 3 494 618** support entries;
`dp_Wtrue.m` banked in the `dp_T31` basis. The level-31 prototype was
relaunched (chatelet) with the corrected pairing. *Unaffected:* `h_g`/`d_g`
(51) and the `L_g` construction (52) are pairing-independent; only the Gram
step uses `W`. *Also learned:* the raw basis is confirmed session-dependent
(rebuilt `T_31` ≠ `gk_s3_T31`), so the authoritative Δ' inputs are the
same-session trio `dp_T31.m` + `dp_W.m` + `dp_Wtrue.m` on chatelet;
`gk_s3_T97/127/191` cannot be paired with them. And
`InternalHMFRawInnerProductDefinite` originally went through
`InnerProductMatrixBig`, whose `return Matrix(...)` densifies the diagonal —
95 GB at q0, which killed the first run of 50; the intrinsic now computes the
masses directly (patch revised; regression: level-31 masses unchanged).

**D32 (2026-09-01). GATE 5 ANSWERS NO-GO: `d_g > 16` at q0 — the residual
system has no rational 16-dimensional isotypic piece, so the gate-4 genus-16
construction is unavailable at this auxiliary prime.** The q0 run of
`51_delta_prime_q0_hg.m` (banked `dp_T31`, precision `2^192`) lifted both
residual blocks T-stably with every internal check exact: the `f1` block
(dim 32) has `cp_m = u1² · h'` with zero remainder and `deg h' = 16`; the
`f2` block (dim 16) is purely old (`cp_m = u2²`, new-part degree 0), exactly
as gate 1 predicted. Over `Z_2`, `h'` splits into TWO irreducible degree-8
pieces (matching residual multiplicity 2). The Deligne coefficient bound
(`|a_31| ≤ 2√31`; a degree-d global factor balanced-lifts under
`C(d,d/2)·12^d`) rejects **all** sub-products: `h'` itself and each degree-8
piece lift to coefficients ~`2^190` against bounds `2^71`/`2^35`
(`55_subproduct_f1block.m`, 0 of 3 pass). Hence every global Hecke orbit
meeting the `f1`-side new block has degree > 16 — its other 2-adic pieces lie
over residual factors other than `f1` and `f2` — so `dim B_g > 16` (compare:
already at level 31 the new orbits have degrees 656/684), the
`gate5-genus16-term-count` premise `genus = 16` fails, and the term count
`~M^{d_g}` is out of reach for any plausible `Δ'`. Moreover the `f1`-new
lattice is only `Z_2`-rational, so the `Δ'`-as-integer framing (D27c/D29/D30)
loses its object: scripts 52/53 are moot at this prime. *Evidence:*
`dembele/data/computed/dp_hg_q0.out`, `dp_hg_f1_block.m` (the lifted 32×32
block action). *What remains open:* `d_g` is a property of the CHOSEN q0; the
options are (a) resume the gate-1 scan for a different auxiliary prime and
re-run 51 there (the whole pipeline is now banked + validated; marginal cost
per candidate ≈ one 51 run, ~8 h), (b) rework gate 4 to use only the
16-dimensional 2-adic toric data rather than the global abelian variety —
a genuine research question, (c) the contingencies of
`levelraise-cd-plan.md`. The route is NOT killed; this q0 is.

**D33 (2026-09-01). The Tate pilot answers at phase 1: `M_rec ~ 10⁴` — the
recognition wall kills the q0-adic-period route (option (b)) on precision,
and retro-confirms gate 4 was precision-infeasible independently of D32.**
The five rational newforms at level p31 have `ord(q_E) = ⟨v,v⟩_stab/2 ∈
{7960, ..., 62872}` (56_tate_pilot_lattice.m; the /2 normalization was
ground-truthed over Q on six curve classes first — Gross pairing, CD-optimal
member selected each time). Heights of the j-invariants follow by the product
formula: ~10³–10⁴ digits, so algebraic recognition needs `M_rec ≈ 10⁴–10⁵`
q0-adic digits; the overconvergent lift at that precision costs ≳10¹³ ops at
an optimistic C floor (O(M) moment updates) and ~10¹⁷ realistically — out of
reach; Python out by orders more. *Decision:* pilot phases 2–4 are not
built; the roadmap's `M_rec` question is ANSWERED (feared ~100, actual ~10⁴).
The level-raising/CD arc is now closed by two independent obstructions
(D32: no rational small-orbit piece; D33: recognition precision), both
measured, both documented. *What could reopen it:* a quadratically
convergent overconvergent lift (log M iterations), or a small-height
recognition target — neither identified; heights of this scale are intrinsic
to conductor-p31 objects over the disc-2³¹ field. *Assets that stand:* the
over-Q-validated monodromy layer (v(q) = ⟨v,v⟩/2), the orbit-degree
certification method, the D31 pairing intrinsics, all banks.

**D34 (2026-09-01). A feasible one-pass lift algorithm was identified for the
level-31 computation — and declined, to stay on the original goal.** Analysis
prompted by "would Newton make recognition feasible?": the recognition (LLL)
is cheap and the lift equation is linear, so Newton per se is moot — but the
M-fold Pollack–Stevens iteration is not fundamental. The `U_p` coset maps act
by `t ↦ pt + a`, so the level-`j` moment block is `1 − a⁻¹p^j A ≡ 1 mod p^j`
(Neumann-invertible): a **filtration-ordered direct solve** computes the lift
in one pass; with the precision profile (moment `j` at `M−j` digits) and
online convolution for the binomial sums, the best level-31 curve
(`M ≈ 9000`) prices at ~10²–10³ core-hours and 40–80 GB — feasible on
chatelet with a bespoke C-level implementation. This would yield a genuine
standalone: explicit equations of conductor-norm-31 modular elliptic curves
over the degree-8 field via p-adic uniformization (~1500-digit heights).
*But it does not transfer:* at any usable q0 the positions (~75×) and the
Γ-diagonal heights (10–100× in `M`) put the target 10⁵–10⁷× beyond even this
algorithm, and D32 closed the route independently. *Decision (user):* stay
on the original goal; the standalone is not pursued. D33's "no escape
identified" is hereby refined to "escape identified, priced, and out of
scope for the goal." The level-raising/CD arc remains closed.

**D35 (2026-09-01). Dembélé front end has no live candidate (D32–D34); the
session moved to Lemma B per the handoff, and step (a) of the attack plan is
now a theorem: Lemma B holds for every cyclic 2-group.** Proof
(`writeup/lemma-B-cyclic.md`): coinvariants of the relation module are
`(N/[F,N]) ⊗ F_2`, which by Hopf's formula is an extension of `L/2L` (`L` the
index-`|G^{ab}|` lattice in `Z²`) by `M(G)/2`; the three puncture classes map to
`(e_0,0), (0,e_1), (e_∞,e_∞)`; for cyclic `G` the multiplier vanishes and
`(n,0) ∉ 2L` when `a` is odd, so `dim H_1(X,F_2)_G = 1`, and a module with
1-dimensional top over the local ring `F_2[G]` is cyclic hence indecomposable.
By-product: the general **coinvariant formula**
`dim H_1(X,F_2)_G = 2 + d(M(G)) − r`, `r ≤ 3` = rank of the puncture classes,
which explains the census socle dimensions (up to 3) structurally and shows
the socle/top criterion can only work when `d(M(G)) ≤ 2`. Numerics:
`lemmaB/cyclic_check.sage` (930 cyclic triples, `n ≤ 32`, all `dim M_G = 1`),
`lemmaB/coinv_formula_check.sage`. *Alternatives:* invent a new Dembélé
front end with no candidate (declined — nothing on the table, see
stocktake §1–2); Lean-formalize now (deferred: the topological
identification of the module is outside Mathlib, the algebra is short).
*Next:* `d(M(G)) = 0` groups (generalized quaternion, semidihedral) via
`r ≥ 1`; tabulate `r` vs `d(M(G))` over the census to isolate the genuinely
glued cases.

**D36 (2026-09-02). The norm-2 level-raising door is closed by direct
computation: no Steinberg newform at the prime `𝔭 | 2` carries Dembélé's
residual system.** The stock-take review found one unpriced door — level
raising at `𝔭` itself (the gate-1 scan assumed odd norm and skipped it), where
every downstream cost collapses (level-`𝔭` cuspidal dim **154** vs 109240 at
q0, tree 3-regular, D34 one-pass lift applies). `57_levelraise_p2.m`
(`dembele/data/computed/levelraise_p2.out`) computes the level-`𝔭` Brandt
module and settles it: the residual invariant `g16bar` (the degree-16 mod-2
factor of `cp(T_31)` at level 1) divides `cp(T_31)` at level `𝔭` with
multiplicity **2 = old baseline (2), new part 0**; `ker g16bar(T_31)` mod 2
has dim 32 = 2×(level-1 dim 16), entirely oldforms. Sharper: the `𝔭`-new part
(dim 40) has `cp(T_31)` mod 2 `= (t⁴+t+1)⁵·(t⁴+t³+t²+t+1)⁵` — the two
irreducible **quartics** over F₂, i.e. residue field **F₁₆**, not F₂₅₆; so
`f`'s F₂₅₆ system cannot occur in the `𝔭`-new part for a residue-field reason.
*Why, in one line:* Steinberg level raising at 𝔮 needs `ā_𝔮 = ±(N𝔮+1) mod λ`;
at `𝔭`, `N𝔭+1 = 3 ≡ 1 mod 2`, so it needs `ā_𝔭 = 1`, but the level-1
fingerprint gives `cp(T_𝔭)|₁₆-block ≡ (z²+z+1)⁸ mod 2`, i.e. `ā_𝔭 = ω` (a
cube root of unity) `≠ 1`. The computation confirms the eigenvalue prediction
in the `ℓ = 2` corner where it is not a theorem. *Closed:* the cheap
(conductor `𝔭¹`, Steinberg) norm-2 door — the obstruction is intrinsic to `ω`.
*NOT touched:* conductor `𝔭^k`, k≥2 (supercuspidal at `𝔭`) — different
congruence, larger space, murkier theory; a real computation, not an
afternoon. *Unaffected:* the two paper-math holes from the arc review — does
`λ`-torsion localize in the CD uniformization (would make `d_g > 16`
irrelevant, D32 option (b)), and recognizing a smaller-height invariant than
the degree-257 polynomial (attacks D33's `M_rec ~ 10⁴`); neither depends on
the auxiliary prime. *Cost:* ~1 h real compute (laptop slept overnight,
inflating wall clock).

**D37 (2026-09-03/04). Lemma B is false as stated and is restated as
multiplicity-freeness; the census tabulation is done to `|G| ≤ 64`; the
session then returns to the Dembélé goal.** Following D35's plan, the
coinvariant formula was tabulated with `r` computed directly from the module
(`lemmaB/census_top.sage`, 707 Aut-classes of positive-genus triples,
`|G| ≤ 64`). The formula `dim M_G = 2 + d(M(G)) − r` holds in every case, and
`r` is identified as the rank of restriction `H²(G,F_2) → ⊕_b H²(⟨σ_b⟩,F_2)`
(the coinvariant group `V = N/[F,N]N²` is the kernel of the universal
2-generated central `F_2`-extension, `H² = V^*`, and `res_{⟨σ_b⟩} λ ≠ 0` iff
`λ([w_b^{e_b}]) ≠ 0`). *The finding:* the same run computed indecomposability
outright and found `J[2]` **decomposable** for `Q_16, Q_32, Q_64` — two
non-isomorphic summands of dimension `g` each (`End/rad = F_2 × F_2`), confirmed
by MeatAxe, by the commutant/Wedderburn computation, and by the explicit
hyperelliptic model `y² = x(x^{2g}−1)` with `G/z = D_{2g}` on the Weierstrass
points (`lemmaB/quaternion_*.sage`). For `Q_8`, `End/rad = F_4`. *Root cause of
the misstatement:* `torsion_fast/shard.sage` test `max_multiplicity == 1`
(multiplicity-free), which the writeups and CLAUDE.md called "indecomposable";
the 2008/2008 tally is correct for the property actually tested. *Impact on the
main result:* none — Lemma A's proof goes through verbatim for multiplicity-free
`M` (`End/rad` a product of finite fields); the Lean file covers only the local
case (extension not formalized). *Alternatives:* leave the wording (rejected:
the claim is false and checkable); try to rescue "indecomposable" by excluding
quaternion groups (recorded as the refined conjecture B″, verified `≤ 64`, but
B′ is the honest statement). The handoff's "show `r ≥ 1` for quaternion" was
already contradicted by §3 of the cyclic writeup (`r = 0`); it is retired.
Subgroup-determinacy: `M` is determined by the conjugacy classes of the three
cyclic subgroups in 151/155 bins (4 exceptions at order 64). *Decision (user):*
commit the correction, then **stop the Belyi side and return to the Dembélé
goal** on paper-math hole (1) — whether `λ`-torsion localizes in the CD
uniformization — since a positive answer reopens the CD route closed by D32.
*Cost:* ~1 h compute at `≤ 32`, ~75 min at 64 (once the harness's duplicate
launches were killed).

**D38 (2026-09-04). Paper-math hole (1) — "does `λ`-torsion localize in the
CD uniformization?" — is answered: yes, and it does not reopen the route.**
`dembele/certificates/lambda-torsion-localization.md`. Kummer theory for the
totally degenerate `B_g = T_g/Λ_g` over `F_{q₀}` gives
`0 → Hom(X_g/λ, μ₂) → B_g[λ] → Λ_g/λΛ_g → 0` with trivial local Galois action
on both ends and extension class = the `λ`-block of the period pairing modulo
squares — an `8×8` matrix over `F₂` with values in `F_{q₀}^×/(F_{q₀}^×)² =
(Z/2)²`. So the `G_{F_{q₀}}`-module `B_g[λ]` is determined by the banked
rank-16 2-adic block plus 64 period values mod squares (cheaper than the
stocktake's budget). *Why it is not a lever:* this is local data at `q₀`; the
global field `F(B_g[λ]) = K_Dembélé` can only be reached from it through
algebraic functions on `B_g` (theta series over `Λ_g`, rank `d_g`), because the
uniformization coordinates `√u(l,x)` of torsion points are transcendental (as
`q^{1/2}` is for a Tate curve) — so stocktake question 2 ("`λ`-division + LLL")
has no algebraic target, and the `λ`-block is not the 2-torsion of any
16-dimensional variety (that would be a degree-16 Hecke orbit, excluded by
D32 and heuristically everywhere). Local data at one prime, or at all primes,
gives only the shape of `K` (Frobenius data already known from `a_p mod λ`).
Hence `d_g` remains the operative parameter of gate 4; D32 option (b) is
closed; hole (1) collapses into hole (2) (an algebraic invariant of `K`
computable without a `d_g`-dimensional variety — no candidate). *Byproduct:*
a free consistency check for any future `q₀` run — `ρ̄_f` has level 1, so the
Kummer class must be unramified: the monodromy pairing on the `f1`-new block
must have even valuations mod 2. *Alternatives considered:* base change
(never creates Steinberg places, so no Shimura curve for `A_f`); the level-1
`A_f` itself (good reduction everywhere over `F`, no multiplicative
uniformization anywhere — only the killed archimedean routes). *State of the
goal after D38:* the CD arc has no conceptual door left; what remains is the
auxiliary-prime lottery (`~10⁻³`), the untested supercuspidal `𝔭^k` family
(D36; also subject to a `d_g` question), and the front-end problem itself.
*Cost:* paper only.

**D39 (2026-09-08). The supercuspidal conductor-`𝔭^k` family at the prime
above 2 is computed: the congruence exists, the route does not.**
`dembele/magma/58_levelraise_p2k.m` + `59_p2k_twist_check.m`
(`dembele/data/computed/levelraise_p2k.out`, `p2k_twist_check.out`,
`levelraise_p2k_charpolys.m`), certificate `levelraise-p2k.md`. Levels
`𝔭^k`, k = 1..4 (cuspidal dims 154, 299, 580, 1142; new 40, 48, 136, 281),
basis-free `T_31` characteristic-polynomial counts on the raw Brandt module.
*Result:* the `𝔭^k`-new multiplicity of each residual system `f1, f2` is
**0, 1, 2, 4** for k = 1, 2, 3, 4 (old baselines 2, 3, 6, 12 — all exact).
The carriers: at `𝔭²` ONE rational Hecke orbit of degree **48** (the whole
new space; depth-zero supercuspidal, `U_𝔭 = 0`, `cp mod 2 = t³²·f1·f2`); at
`𝔭³` two orbits of degrees **64, 72**; at `𝔭⁴` the four copies are all
twists by the quadratic character of `Q(ζ₃₂)/F` (conductor exactly `𝔭²`,
`χ(𝔭₃₁) = −1`) of the level-1 form (degree 16 = `A_f` twisted, same field)
and of the `𝔭²`, `𝔭³` carriers — verified factor-by-factor: the entire
`𝔭⁴`-new part is `57 + 40 + 48 + 136` twists, twist-minimal remainder 0.
*Why the congruence was expected:* residue field `F₂` has two Serre weights,
`ρ̄_f` carries both, every type at `𝔭` should lift (Breuil–Mézard heuristic;
not a theorem at p = 2, e = 8) — D36's Steinberg failure was the eigenvalue
condition `ā_𝔭 = 1`, not a Serre-weight obstruction. *Why it is not a route
(certificate §3):* supercuspidal at `𝔭` means `ρ_g|G_𝔭` irreducible of tame
type, so `A_g` (dim 48) has potentially good **supersingular** reduction at
`𝔭` (good over the tame cubic extension, special fibre `~ E₀⁴⁸`, `j = 0`);
the Shimura curve carrying it (level `1+𝔭_D`, genus 136, degree-3 cover of
the genus-40 discriminant-`𝔭` curve) is uniformized by a quotient of
Drinfeld's `Σ¹`, whose reduction components are genus-1 Deligne–Lusztig
curves: no Mumford curve, no period lattice, no monodromy pairing. Nothing
from the CD arc applies, D38's locality objection applies verbatim, and
`d_g = 48 > 16` anyway. *Alternatives considered:* k = 5 (dim 2249; would
only add depth-1 supercuspidals and principal-series types, same geometry —
not run); building the confirmatory `T_97` at every level (only k = 2 is
confirmed, sufficient for the verdict). *State of the goal after D39:* item
(ii) of the D38 list is closed; what remains is the auxiliary-prime lottery
(`~10⁻³`) and the front-end problem (hole 2), unchanged. *Byproduct worth
keeping:* the local shape of `K_Dembélé` at 2 — the `λ`-torsion of a
48-dimensional variety with supersingular reduction after a tame cubic base
change of `F_𝔭`. *Cost:* ~4 h local Magma (two detached jobs), paper for §3.

**D40 (2026-09-08). Comprehensive review after D39; the overlooked object:
the level-`𝔭` Steinberg forms over `F` carry `SL₂(F₁₆)`-representations
ramified only at 2 — a second nonsolvable field, with 4-dimensional carriers
of split multiplicative reduction at the norm-2 prime. New target adopted.**
`dembele/certificates/review-2026-09-08.md`; job `60_f16_steinberg.m`
(`f16_steinberg.out`), probe `61_fuchsian_p2_probe.m`. *Review verdict:* for
`ρ̄_f` itself no closed door reopens — every route died on a measured number
(table in §1). *The gap:* D36 recorded the `𝔭`-new part (dim 40; orbits
4,4,4,4,24) as "residue field F₁₆, not F₂₅₆" and moved on; but each of those
mod-2 systems is a 2-dimensional representation of `G_F` unramified outside
`𝔭` with trace field `F₁₆`, irreducible (ray class groups mod `𝔭^k` are
2-groups, `h(F)=1`, residue field `F₂`), and not dihedral (for every quadratic
class `d` unramified outside 2 there is a prime `𝔮` inert in `F(√d)` with
`ā_𝔮 ≠ 0` — 510/511 classes killed by the eight primes above 31 alone, the
last by 97 [T_97 block: see review §2.5]) ⇒ image `SL₂(F₁₆)` by Dickson.
Invisible to Dembélé's level-1 search because its only Serre weight at `𝔭` is
the Steinberg weight `V₁` (très ramifié). *Numbers:* Hecke fields `Q(ζ₁₅)⁺`
(×2) and the conductor-95 cyclic quartic (×2), 2 inert, `a_𝔭 = +1` (split
multiplicative); two residual classes up to Frobenius (`ā_31` of order 15 and
5), swapped by `C₈` ⇒ expected Galois group over `Q` is `SL₂(16)² ⋊ C₈`
(order `1.3·10⁸`, vs `~10¹⁵` for Dembélé's); Frobenius above 31 is a 17-cycle
on `P¹(F₁₆)`; monodromy Gram valuation diagonals `20, 20, 64, 194` and
`20, 20, 320, 458` (vs 7960–62872 at level 31, D33) — heights 20–300× smaller,
2-adic, with 174 tree positions. Nothing exists lower in the tower: 2-power
levels over `Q(ζ₁₆)⁺` (`k ≤ 10`, dim 159) and `Q(√2)` (`k ≤ 14`, dim 1023) have
all mod-2 eigenvalues in `F₂`. The Fuchsian group of the discriminant-`𝔭`
algebra has signature `⟨40; 3¹⁸, 16⟩` (Magma, 20 s), area 571 — inside the
range where fundamental domains have been computed. *Decision:* adopt the
`F₁₆` field as the explicit target (degree-17 polynomial over `F`): it answers
the thesis question (an explicit nonsolvable field ramified only at 2), it is
the cheapest possible instance of the never-run link `periods → 2-torsion →
recognition` (`d_g = 4`, `N𝔭 = 2`, the validated genus-4/17-neighbour back
end), and it is the only object on which hole (2) can be measured rather than
extrapolated. Dembélé's field stays the long-term goal; everything learned
transfers. *Alternatives considered:* auxiliary-prime lottery (kept as
background only), k=8 covers falsification target (does not bear on
explicitness), Lemma B (self-contained, unchanged). *Plan:* review §4 —
Phase 1 write-up + Frobenius table; Phase 2 the CD-at-`𝔭` pipeline at
dimension 4 (tree quotient banked in kind, one-pass lift D34, Eisenstein
invariant on 17 neighbours, LLL, `GaloisGroup` certification), with the
Fuchsian fundamental domain as the archimedean cross-check. *Cost:* review
paper + ~3 h local Magma.

**D41 (2026-09-14). The completed D40 job exposes an invalid anti-dihedral
fallback; withdraw the claimed nonsolvable F16 target pending an image test.**
T97 completed (8805.560 CPU s): trace zero on the entire new part, eight
joint generalized eigenspaces, two tested Frobenius classes of total dimension
20, Legendre rank 8 and one survivor each. Both original VERDICT lines claim
large image via class numbers, but test factors 3 and 5. Frobenius at 31 has
order **17**, not the multiplicative order of its trace. Independent script
`62_f16_dihedral_audit.m` finds the survivor has degree 16, discriminant 2^79,
signature (0,8), and class group **C17 (GRH)**. Thus the fallback misses exactly
the relevant factor. Script 60 repaired; historical output preserved; review
§2.5 updated. Certificate: `f16-dihedral-audit.md`. Candidate Frobenius cycles
at 31/97/127/191 are 17 / 1 2^8 / 1 2^8 / 1 2^8. *Decision:* resolve the
image before spending on periods. T127 with a nonzero trace would exclude the
sole candidate; another zero does not prove dihedrality. *Alternatives:* blindly
copying the old verdict or proceeding to periods would rely on a false check.
Full residual congruences, the number of fields and the C8 action remain open;
the smaller-field single-operator scans likewise do not prove nonexistence.
*Cost:* seconds for the independent Magma audit; no new heavy Hecke build.

---

**D42 (2026-09-14). Close the F16 detour by the published theorem; reopen the
original p² carrier through curve/Jacobian arithmetic.** The review found a
missing directly applicable source: Dembélé's genus-16 paper (ANT 2020),
Theorem 6.4, identifies the normal closures of the simple factors' 2-torsion
fields with the solvable Harbater field. D41's uncertainty and next T127
test are superseded. D39's lack of toric uniformization only closes the
existing period pipeline. It does not exclude an algebraic curve model and
odd-prime Jacobian torsion computation. A proposed involution quotient of
the genus-136 carrier has genus 64, retaining 16 old dimensions and the
48-dimensional target carrier. Script 64 passes branching/genus consistency
and the T31 Frobenius isolation test; an order-51 Frobenius at 97 is promising.
The quotient's canonical model and integral representation are unproved.
Script 63 passes the finite calculation for an all-Hecke sign-type comparison
on the original 58-class module: 48 classes are admissible, and the quotient
has T31 polynomial t^10, excluding both target factors. Its supported
polynomial matches the p²-new bank. The first attempt used the wrong column
convention; corrected to the package's row convention and a ten-column
quotient test, which passed in 64.630 CPU s. Failed output preserved separately.
*Decision:* prioritize this geometric route with explicit gates in
`dembele/certificates/review-2026-09-14.md`, not another F16 image scan or
an extrapolation from theta costs. Rickards's current domain code and
Baït–Page's 2026 cohomology code are relevant untested tools, not completed
model algorithms. Unsupported inertia/height estimates are marked withdrawn.
No target polynomial was constructed. Validation: scripts 62/63/64 PASS,
34 Python unit tests pass, and diff whitespace checks pass. The bank's
self-contained expression was checked to preserve all five polynomials.

**D43 (2026-09-15). Compute the normalizer domain and verify the genus-64
local cover.** Proceeded from D42 using Rickards's maintained `klein` code
(commit 79a12d3f108edce3e78d30c4a59dfc0fb01012d8) and Dembélé's small
presentation D=(b-b²,-1)/F. A two-call trace compatibility patch builds on
Sage's PARI 2.17.1; an absolute loader path is needed on this macOS bundle.
The genus-16 normalizer domain, selected directly with type=3, has 277 sides
and passes signature, relation and side-pairing checks in 257.443 wall
seconds. Script 66 constructs the F4 residue quotient of O/2 and the
actual local S3 map on the saved generators. All relations and product
checks pass; image order 6; elliptic monodromy yields Y genus 64 and Z
genus 136. Independently, lifted homology gives b1(Y)=128. Coset
representatives identity/side 2/side 8 and side images are exported.
Magma independently verifies the explicit algebra and X40 signature.
*Decision:* the domain/cover gate is passed computationally; proceed to
holomorphic differentials and algebraic section data, retaining the need
for a precise integral target comparison. A single Taylor series across
the present domain has slow geometric decay (max radius 0.9997819873), so
test multiple centers or a CM-centered sparse expansion. Do not interpret
this as universal closure. *Artifacts:* `genus64-cover.md`, `dembele/pari/`,
`normalizer_domain.bin`, presentation/monodromy/coset data and passing logs.
No algebraic model or field polynomial constructed. No external messages
sent. The numerical polygon is validated at finite precision, while the
residue and lifted homology calculations are exact.

**D44 (2026-09-15). Compute genus-16 differentials first; retain general
canonical reconstruction after a hyperellipticity discrepancy.** The
order-32 CM center reduces expansions to w^31 H(w^32)dw. Reconstructing its
Dirichlet sector showed that R=0.9998 was too small; R=0.99991 covers the
numerical sector. At N=4096 there are exactly 16 small singular values;
N=8192 with 50-digit geometry replay and stabilized refinement gives
independent side residuals below 3.2e-10. Products have rank 45, yielding 91
quadrics verified on unused coefficients to 1.44e-12. Their linear multiples
leave degree-3 quotient dimension 75. Hyperellipticity would require rank 31.
An audit of the opening step of the published Theorem 5.9 identifies an
apparent confusion between an upstairs elliptic parameter and the coarse
quotient parameter. This is an unresolved source/computation discrepancy,
not a certified refutation. *Decision:* preserve these numerical canonical
data and pursue independent validation/arithmetic normalization; do not
force a hyperelliptic equation. D43's local cover remains valid. The F16
claim has a separate published induced-character proof, whose full
independent audit remains outside this computation. *Failed alternatives:*
small-radius kernels, single-vector ARPACK after precision replay (missed
multiplicity), and block power iteration (unwanted expanding eigenvalues).
The final stabilized solve took about 50seconds. See
`dembele/certificates/genus16-differentials.md` and scripts 67–70. No algebraic
model or target polynomial; no external messages. Existing 34 tests pass.

**D45 (2026-09-15). Resolve hyperellipticity by exact stable reduction.**
The genus-16 curve is nonhyperelliptic: its stable metric graph has no
tree-quotient involution. Two independent automorphism enumerators agree
on 64 automorphisms and 19 involutions, whose quotient genera are 8,10,12,14.
The graph was first read from Figure 2, then independently reconstructed
from the norm-2 Brandt operator: 58 classes/73 edges stabilize to 30/45 with
an explicit weight-preserving isomorphism. The final Magma run uses
Minkowski class-group proof bounds and checks mass 1455/32 against exact
zeta_F(-1)=5820; ~27 CPU seconds. Baker specialization and Chan's criterion
give the obstruction, including residue characteristic 2. *Decision:*
supersede D44's unresolved verdict and proceed through general canonical
relations rather than a hyperelliptic model. This contradicts the cited
Theorem 5.9; the local-coordinate gap explains why its opening inference
does not establish the claim. Separate F16 induced-character claims are
not automatically invalidated. *Additional finding:* the norm-2 pairing
identity is the reverse of the helper documentation, directly tested;
review old pairing-dependent work before reuse. *Alternatives:* further
Taylor precision would only strengthen numerical evidence; exact graph
arithmetic gives an independent obstruction. *Artifacts:*
`hyperellipticity-audit.md`, scripts 71–73 and their exact JSON/logs. No
algebraic model, target polynomial, external messages, or commits.

**D46 (2026-09-15). Prove quadratic generation and fix a CM arithmetic
normalization before recognition.** A seven-vertex minor of the verified
stable graph has minimum degree four; treewidth/metric gonality and
specialization give gonality(C)>=4. Petri guarantees that the canonical
ideal is generated by 91 quadrics. Only 61 exact local coefficients are
needed for the quadratic relation space. Script 74 fixes the first 16
jets and divides out a common coordinate/period scale using
alpha=3*a_(16,15). The resulting numerical equations are real and have
coefficient magnitudes <=152. Extending to N=10240 costs ~87 seconds and
gives relative cross-truncation coefficient stability 1.15e-10, with a
1.95e-8 worst absolute difference. Six bounded recognition tests found
no candidates. *Decision:* retain this fixed normalization and pursue
higher-precision jets/field recognition; do not claim equations over F
from reality or promote short integer relations without validation.
*Alternative:* a numerical Hecke eigenbasis is not needed just to remove
the common period scale, although Hecke data may help identify the field.
Dense double-precision enlargement alone cannot supply arbitrary digits.
Artifacts: `canonical-gauge.md`, scripts 74–76 and numerical/exact outputs.
Independent 275-side audit gives maximum residual 7.18e-13, product rank
45 and cubic quotient dimension 75; all 34 repository tests pass.
No number-field model, target polynomial, external messages, or commits.

**D47 (2026-09-15). Deploy the canonical numerical pipeline to Châtelet.**
At the user's request, package eleven required scripts/data files in an
isolated, hash-verified directory and launch a detached N=12288 refinement
seeded from N=10240. Run graph, differential, quadratic and recognition
audits afterward. Use Sage Python's existing dependencies and four BLAS
threads. Preserve all existing remote banks; refuse directory replacement.
Provide status and checksum-verified result retrieval. This establishes
remote execution and a larger-truncation check, not arbitrary-precision
arithmetic. The latter still requires a new solver. See
`dembele/jobs/canonical/README.md`.

**D48 (2026-09-15). Test Newton refinement and the hyperelliptic ansatz.**
The fixed-geometry differential problem is linear: implement mixed-precision
iterative refinement before a nonlinear solver. An actual N=64 operator
test reaches ~1e-49 residual with double LU and arbitrary-precision
matrix-free residuals; this is not a valid full curve truncation. Next is
a compiled residual evaluator plus truncation validation. Independently
try hyperelliptic reconstruction via H15/H14 and H14/x^14: it fails the
first unused jet by ~745.59 at both truncations, while genuine genus-16
hyperelliptic controls pass. Do not adopt hyperellipticity to force a
model inconsistent with these data and the exact graph obstruction.
Châtelet N=12288 completed all audits. Scripts 77–78 and
`newton-and-hyperelliptic-ansatz.md` record results and limitations.

*Session-close clarification:* the completed Châtelet run is solely a
double-precision numerical computation. Script 78's arbitrary-precision
N=64 prototype ran locally. No full-size arbitrary-precision basis, exact
curve equations, or field polynomial has been obtained. `HANDOFF.md` now
starts with concrete resumption steps and separate local/remote locations.

**D49 (2026-09-15). Compile the actual Cauchy action and validate full-size
mixed-precision refinement before algebraic recognition.** FLINT polynomial
evaluation and reusable DFT plans replace the small Python action; residuals
and accumulated iterates remain arbitrary precision, while one double LU
handles the initial solve and both corrections. Separate power-of-two scales
preserve even residuals outside the double exponent range. Independent
column workers share only immutable input and disjoint output; serial and
threaded outputs agree bit for bit in tests. *Outcome:* all sixteen columns
at N=4096 and 8192 reach finite-system residuals below 4e-41. The N=8192 run
takes 246 seconds locally, with 38–44 seconds per residual evaluation. But
independent side residuals are 1.87e-4 and 1.42e-9 respectively, and the larger
quadrature at N=8192 has defect 5.86e-12. This separates linear solver accuracy
from the still-limiting analytic truncation. *Decision:* retain native exact
checkpoints, increase truncation next, and do not infer 40-digit differential
accuracy or exact coefficients. *Alternative:* quasilinear multipoint
evaluation and multiple centers were not needed to validate this gate;
native polynomial evaluation remains O(mn), and the double LU remains dense.
Eight new meaningful backend tests and the existing 34 pass; Python compile,
default-double interface, and diff checks pass. See script 79, `cm_acb.*`,
`compiled-precision-refinement.md`, and `acb_refinement_{64,4096,8192}.*`.
No algebraic model, torsion, field polynomial, remote launch, or commit.

**D50 (2026-09-15). Review the entire route and prioritize the missing
arithmetic and torsion steps over automatic genus-16 precision growth.**
At the user's request, re-read the project audits and primary algorithm
papers. *Assessment:* the curve/Jacobian route is still the strongest
concrete candidate identified, not an established practical end-to-end
construction or a proved optimal route. D49 validates a solver; C is the
base, while the target is expected in the 48-dimensional new factor of
J(Y), genus 64. *Decision:* finish the precise local-type/geometric target
comparison, pilot the standard S3-valued differentials on Y, justify the
CM coefficient field and benchmark the torsion backend. A recognized
arithmetic curve or equivalent evaluation data remain absent. The norm-97
cofactor check and invariant heights remain open. The odd-degree map
splits old/new 2-torsion; the CM standard component uses exponents 31 and
15 modulo 32. Small exact representation and Frobenius-cycle checks pass.
An integral Hecke projector and irreducibility may establish an actual
target subspace without a full integral homology calculation; mere
semisimplification or local Frobenius isolation does not suffice alone.
Checked the later Mascot genus-22 benchmark and the August 2026 equationless
modular paper; neither establishes our missing quaternionic input or cost.
Qiu v2 still cites the disputed hyperellipticity theorem. *Alternatives:*
retain other routes as bounded possibilities, with their specific audited
obstacles; do not revive universal impossibility claims. See
`dembele/certificates/route-review-2026-09-15.md`. Documentation only;
no new large/remote run, field polynomial, external message or commit.

**D51 (2026-09-15). Prefer the user's Belyi code while advancing the target
proof and direct cover pilot.** User approved D50 and requested optional
priority for Belyi maps and their code. *Decision:* reuse
`/Users/musty/Belyi/Cext/powser_arnoldi.c` with an adapter for the actual
polygon, S3 monodromy and standard component. No triangle presentation
or Belyi map for Y is asserted. All 277 side images align with their
quaternion elements. At n=2048, 48 eigenvalues are within 0.000470 of one,
the 49th is ~0.398 away; changed-quadrature defect is 0.000642 and worst
sampled side defect 0.00908. Native operator checks agree to 2.8e-16.
The small Arnoldi pilot failed. Wide arithmetic balls are reported
separately from midpoints, and zero returns are invalid. *Proof outcome:*
the written transfer and integral Hecke argument realizes both original
systems in canonical J(Y)[2]; script 80 checks exact CRT projectors.
This relies on the recorded Hecke input and standard cohomology theorems;
a future recognized model must still be identified with Y. *Control:*
the user's Q8 Belyi curve supplies all 16 torsion points over F49 and the
expected Frobenius action. This is an exact control, not generic
Makdisi/p-adic lifting. *Next:* arithmetic section normalization and
reconstruction, preferring Belyi routines where applicable, and generic
torsion setup. All 47 tests pass. See `target-realization.md` and
`belyi-cover-pilot.md`. No Belyi package edits, remote run, field polynomial,
external message or commit.

**D52 (2026-09-15). Use the user's thesis and Belyi normalization methods
to address the arithmetic field before recognition.** User clarified
priority for `belyi/`, the thesis and both coauthored papers. Read the
general canonical reconstruction in KMSV and the marked descent and
weighted rescaling in MSSV; corrected the first paper's author list.
*Mathematical outcome:* a formal integral of a distinguished differential
removes nonlinear parameter ambiguity, and a weight-one rescaling gives
a parameter over the marked curve's field. Apply this conditionally on C
and pull back to the unramified F-rational P32 point of Y. This is an
explicit argument beyond MSSV's numerical observation. *Control:* exact
Q8 coordinate/basis invariance, rejection of a root ambiguity, independent
Lagrange inversion, nonordinary quartic and fixed-index checks all pass.
*Numerical outcome:* a bounded n=4096 cover run improves the side error to
2.75e-5 in 234 seconds, but initial first-48 normalization becomes badly
conditioned. This does not prove the assumed vanishing sequence false.
Any fixed invertible coefficient selection in the arithmetic parameter
gives an F-basis, so the final method removes that assumption. The best
small selection trial still has condition 7.79e6 and 0.101 unused-jet
relative disagreement. *Decision:* address parameter/basis conditioning
on saved data before further large solves or recognition. See
`pointed-normalization.md`, `belyi/pointed_series.py` and script 83.
All 52 tests pass. No exact Y coefficient/model, target torsion, field
polynomial, external package edit, remote launch, message or commit.

**D53 (2026-09-15). Reuse the M23 and earlier-session lessons in staged
reconstruction.** User pointed to the recent paper, previous repository
work, and Zhang's companion note. Re-read the paper and both versions of
the note; the current public title differs, the mathematical account
agrees. Audited the implementations behind D3, D9 and D21. The published
M23 verification repository does not contain the separate cubic-reduction
algorithm mentioned in the note. Corrected the README's claim of failure
at every possible precision. *Adaptation:* a trace-zero differential
ratio generates the degree-three Y/C function field. Its symmetric trace
sections belong to spaces of dimensions 72 and 111, including both
transposition and three-cycle branch divisors. *Experiment:* saved Belyi
banks give complex trace differences up to 0.00220 on the sampled rings
and homogeneous cubic side error 2.97e-6. Five simple two-point arithmetic
line normalizations remain unstable (0.673–1.343 disagreement). Thus the
complex success does not solve the field-of-definition gate. *Decision:*
next recover base quadrics in D52's arithmetic normalization, then reduce
subsequent unknowns using known exact relations/Riemann–Roch data. Avoid
making recognition of every differential coefficient a prerequisite or
automatically launching another large solve. Details and reproduction:
`m23-coordinate-review.md`, script 84, `relative_cubic_4096.{json,out}`.
All 58 tests pass. No exact model, target torsion, field polynomial,
external package edit, remote work, message or commit.

**D54 (2026-09-15). Execute arithmetic quadric reconstruction and test
recognition beyond the review milestone.** The user explicitly asked to
continue. *Implementation:* a short formal calculation determines the
F-normalized canonical basis up to common scalar; recover homogeneous
equations in the original coordinate by that fixed matrix change. This
avoids the long-substitution conditioning problem. Scripts 85–86 recover
91 numerical quadrics with fixed monomial normalization and precise
coefficient serialization. Exact genus-four controls pass and reuse the
Belyi formal-series reference. *Analytic check:* retrieved and verified
the already completed Châtelet double bank, then ran native n=12288 and
16384 locally. The latter's independent side defect is 3.86e-20, while
early-/late-jet equation fits differ by 7.31e-21. Neither is a certified
coefficient bound. In-place dense LU allows the larger run with less
matrix storage than the previous implementation. *Recognition:* all
3,003 eligible coefficients in two field bases and 2,933 scaling-invariant
ratios give zero candidates at the recorded bounds. A small pointed
invariant's older near-match fails at the improved truncation. Direct
LLL searches over the full equation space and weight-20/22 subspaces
also give no accepted equations; these are bounded failures, not height
lower bounds. *Next coordinate choice:* the well-separated weight-22
space is a pencil, with five leading coefficient-zero points available
for map-defined normalization. A preliminary unconditioned cross-ratio
probe loses digits; address this before another automatic n increase.
See `arithmetic-quadrics.md`, scripts 85–89 and their saved reports.
All 71 tests pass. All jobs finished; no exact curve, torsion or field
polynomial, external package edit, new remote launch, message or commit.

**D55 (2026-09-15). Exhaust the proposed marked-pencil normalizations;
recover the pencil directly and remove unnecessary normalization
assumptions.** User authorized the 60-chart scan. Script 90 compares
all charts and their 30 distinct cross-ratio expressions using the saved
8192/12288/16384 banks and two current fits. Direct recovery from 25
differential products improves fit agreement by factors 162 and 60,
more than the roughly 2.45-fold improvement from the chart choice itself.
*Mathematics:* the five coefficient-zero points arise from projections
of the intrinsic weight-22 relation space to graded lines of the
vanishing flag. Their cross-ratios have a conditional F-definition
independent of D52's formal parameter and scale. Exact triangular-change
controls pass, and a complex basis using only 16 jets reproduces them.
*Recognition:* two initial positive trials are one F candidate under
exact cross-ratio transformations. Both direct bases reject it in all
six equivalent charts at the new empirical tolerances. No replacement
in the full scan through limit 32 or the best chart through 64. The
tail estimate remains empirical and PSLQ failure is not a height bound.
*Decision:* this focused coordinate experiment is complete; changing
flag-preserving bases cannot change its invariants. Next audit feasible
arithmetic input (corresponding conjugates/reductions or a justified
height/precision budget) before another large solve. A successful exact
pencil would still be only part of the required curve reconstruction.
See `marked-pencil.md`, script 90 and `marked_pencil_*16384.*`.
All 78 tests pass, reusing the thesis Q8 control. All jobs finished;
no exact C/Y, target torsion or field polynomial, external package edit,
new analytic bank, remote launch, message, cleanup or commit.

**D56 (2026-09-16). Specify global arithmetic functions using the marked
point and CM traces; test their reconstruction instead of another blind
precision increase.** User chose this direction explicitly. Script 91
computes L(17P) and L(18P) as kernels of A*b^2=B*a^2 for two canonical
differentials, with independent product-span and multiplication-rank
checks. Script 92 evaluates at the seventeen order-two CM points D.
The proposed principal divisor D-17P fails numerically, but D supplies
a useful normalization: center x, scale by its second/third trace-moment
ratio, then remove the constant and X components of y and normalize
its moments likewise. This is invariant under triangular generator
changes and gives F-defined X,Y subject to the stated exact hypotheses.
Their pole degrees 17,18 imply F(C)=F(X,Y). Arithmetic and complex flag
bases agree at CM points within 5.35e-17; checkpoint changes remain
about 2e-12. These are empirical comparisons, not certified digits.
*Conditioning experiment:* X/(Y+3X) improves the canonical jet condition
from 7.27e20 to 1.72e10, still worse than the existing local normalization.
The 172-term weighted plane relation fails triangular and balanced fits;
even a singular gap 9.14e12 can coexist with unweighted validation
residuals near one. All such equation coefficients are explicitly
rejected, with no recognition or height inference. *Decision:* preserve
the arithmetic characterization and more stable section ratios; seek
corresponding exact arithmetic data or justified accuracy/height bounds
before further equation recovery. This does not prove the plane model
impossible or the broader curve route unsuccessful. See
`cm-pointed-maps.md`, scripts 91–93 and their eight report pairs.
All 84 tests pass, including independent exact divisor controls and the
user's thesis Q8 curve. No new analytic bank, remote work, external
Belyi edit, message, commit or cleanup. No exact curve or field polynomial.

*Session close, 2026-09-16:* user requested a resumable handoff. D56 remains
the latest research result; no new experiment was launched for closeout.
The first resume task is an audit of available exact data for the specific
CM traces/section ratios, not a repeat of rejected plane fits. Main and
component READMEs now point to the current curve route. The full 84-test
log is preserved as `dembele/data/computed/pointed_maps_tests_20260916.out`.
Research files remain saved locally and uncommitted; all session jobs
are finished. `HANDOFF.md` records the branch, base commit and entry point.

**D57 (2026-09-16). Complete the requested exact CM-input audit and specify
the missing evaluation flag.** On resumption, script 94 tied all seventeen
saved elliptic generators to K=F(sqrt(-2-b)) by exact square witnesses,
verified K/Q cyclic of order 16, and instantiated the known Harbater
degree-17 residue algebra. Reductions have type 17 at 31 and 1,2^8 at
97,127,191. These are usable exact arithmetic inputs, but are not values
of the functions. Two exact pairs in the same algebra satisfy all five
normalization conditions and have different second moments, including
after finite reduction. Thus the field, Galois permutations and moment
conditions cannot replace the geometric flag
`<1> subset ev_D L(17P) subset ev_D L(18P)`.
*Availability:* no independent exact target value, target reduction or
height bound is supplied by the inspected Hecke, Brandt, graph, CM,
Belyi or section-ratio data. CM-norm formulas over totally real fields
exist, but require a constructed special-divisor/Whittaker input which
is not currently available. *Decision:* a new arithmetic evaluation
construction must supply the flag or the tensors that determine it,
or construct a particular function to which such a CM formula applies.
Do not repeat the field-only audit or automatically increase precision.
This is an input gap, not a proof that the curve route fails. See
`cm-arithmetic-input-audit.md` and `cm_arithmetic_audit.*`.
All 90 tests pass, including six new independent exact controls.
No new analytic bank, remote job, external Belyi edit, message, commit
or cleanup; no exact C/Y, target torsion or nonsolvable field polynomial.

**D58 (2026-09-16). Descend the marked objects before rational CM
reconstruction.** The user authorized the proposed descent investigation
and endorsed the descent reference. Dembélé's Lemma 5.2 was overlooked
in D57: its descent statement for the genus-40 curve and Atkin--Lehner
involution is independent of hyperellipticity. Canonical conjugation
of the norm-one/normalizer cover preserves the unique Q(zeta_32) CM
point, giving field of moduli Q for the marked cover. Sijsling--Voight's
marked-map theorem then descends P and D=Branch(pi)-P with the curve.
Under D56's existing ordinary-point/nonzero-moment hypotheses, any
marked automorphism fixes X,Y and hence the function field. Rigidity
removes the F-twist ambiguity and supplies a unique Weil cocycle;
the normalized functions and their degree-17 CM polynomial are Q-defined.
This is a theorem-level argument, not computed descent matrices, and
does not certify those D56 numerical hypotheses.
*Pilot:* script 95 checks exact class numbers and prime invariance and
reuses four saved CM polynomial banks. Exact rational-interval tests
at denominator caps 10^3,10^4,10^5,10^6 give 0,0,5,10 hits among fifteen
independent coefficients, with no full candidate and no unique hits
at 10^6. The intervals are empirical. A simple exact normalized field
generator has monic denominators up to 2.15e23, so coefficient caps
give no intrinsic-height conclusion. *Decision:* preserve Q as the
justified coefficient field; next construct a labelled CM class-group
orbit identification with the embeddings of Q(theta) for simultaneous
recognition, or obtain the exact evaluation flag. Whether current
data suffice for that identification remains to be assessed. Do not
repeat this coefficient scan or automatically increase precision.
See `marked-descent.md`, script 95 and `marked_descent.{json,out}`.
All 96 tests pass, including six new exact controls. No new analytic
bank, remote job, external Belyi edit, message, commit or cleanup.
No exact target CM polynomial, C/Y, torsion or nonsolvable field polynomial.

**D59 (2026-09-16). Make the descended CM residue field usable through
explicit orbit labels, then test joint reconstruction.** The user asked
to continue descent. Script 96 constructs optimal embeddings and exact
ideal classes from the saved quaternion domain. Saturated intersections
I_i={a : u_i*iota_0(a) in O} and a norm equality prove I_i*O=u_i^-1*O;
Shimura reciprocity then identifies their action. Sage/PARI independently
proves h(K)=17. A proved 31-adic Galois calculation and a bounded exact
degree-16 resolvent select (31,beta-19), class 3, resolving the class
generator's action on Elkies's complex roots. Complex orientation and
the real reference point use saved numerical data; Magma supplies the
complex/p-adic root comparison. These limitations are recorded.
*Experiment:* in a 256-bit reduced integral basis centered by trace,
the evaluation matrix has infinity-norm condition 40.9175. All four
existing banks give fifteen independent projective ratios for each
function. At denominator cap 10^6 each has only 10/15 interval hits.
The joint LLL search examines 58 and 59 directions, accepts none at
height cap 10^9, and rejects generic fits of heights about 1.04e12 and
6.14e11. Intervals are empirical and LLL is not exhaustive; there is no
true-height exclusion. A known field element is recovered exactly from
perturbed evaluations by the same machinery. *Decision:* retain the
labelled field identification. The next arithmetic target is the exact
evaluation line and compatible plane, or a justified height/accuracy
budget for them. Do not repeat the same scans or automatically create
larger analytic banks. See `cm-orbit-recognition.md`, Magma script 96,
Python scripts 96–97 and their saved reports. All 103 tests pass. No new
analytic bank, remote job, external Belyi edit, message, commit or cleanup.
Exact target evaluations, C/Y, torsion and nonsolvable polynomial remain open.

**D60 (2026-09-16). Test the evaluation plane and replace bounded LLL
failures with exact exclusions inside empirical boxes.** The user asked
to continue the descended CM-field approach and had explicitly checked
that this ledger and REFERENCES.md were being maintained. A maximal-minor
chart removes all generator choices from span(X,Y); its 28 free entries
still give no complete rational reconstruction at denominator cap 10^7.
Rather than increase analytic precision without an upper-height input,
script 98 uses exact Q(i) arithmetic on D59's saved decimal coordinates
to define the same empirical error rule and certify what it excludes.
For the lattice [I_r R;0 S*I], exact Gram--Schmidt data give a lower
bound on nonzero exterior-lattice vectors. Hadamard bounds those coming
from a rational subspace in the chart box. The resulting inequality
excludes all spaces up to primitive Pluecker heights 19,927,223,139 for
Q X, 13,481,861,693 for Q Y, and 43,166,965,625,539,309,014 for their
plane in the fixed D59 trace-centered basis. The saved certificates
verify without LLL; this is no longer merely failure of a finite
candidate list. *Scope:* the boxes remain empirical, so these are not
unconditional height lower bounds for the target. They supply no upper
bound or exact evaluation. *Decision:* a small-generator change within
these boxes cannot solve the reconstruction at those heights. Seek
arithmetic flag evaluations or justified error and upper-height bounds;
do not repeat the same low-height scans or automatically create another
analytic bank. See `cm-flag-height.md`, script 98 and
`cm_flag_height.{json,out}`. Eight new controls include exterior-matrix
verification, exhaustive small-plane enumeration, tamper rejection and
recovery of a known exact plane after complex mixing/noise. All 111
tests pass. No new analytic bank, remote job, external Belyi edit,
message, commit or cleanup; exact target evaluations and the original
nonsolvable field polynomial remain open.

**D61 (2026-09-16). Take stock before extending the CM reconstruction
branch.** The user asked whether to keep going or step back. The review
compares the saved work with D50's three priorities. D51 supplied the
abstract target comparison; D58–D59 removed the coefficient-field and
CM-label ambiguities. D60 strengthened negative reconstruction results,
but no exact target function value or usable arithmetic curve model has
been obtained. Even exact recovery of the seventeen CM restrictions
would leave global section/model and cover construction before the
genus-64 torsion computation. The auxiliary solvable CM field is not
the nonsolvable target. *Recommendation:* retain the broad curve/Jacobian
strategy, whose practical completion remains unproved, and pause
repetition of the same recognition scans. A new experiment needs a
specified arithmetic output, independent check and downstream use.
Seek a new section/evaluation construction or a changed, testable
reconstruction hypothesis; D57 already inventoried available input.
Exact error and upper-height bounds would justify a budget, but are not
universal prerequisites for heuristic discovery followed by verification.
Recheck the arithmetic identification behind the published geometric
conflict and establish an actual generic divisor/torsion-lifting control
before major investment. Mascot's model definition confirms that an
equationless approach still needs arithmetic section values. This
stocktake does not supply a replacement construction or prove a no-go.
See `stocktake-2026-09-16.md`. No new computation; latest implementation
check remains D60's 111 passing tests. Both this ledger and REFERENCES.md
are updated. No remote job, external message, commit or cleanup.

**D62 (2026-09-16). Execute the geometry audit and actual backend controls
before more recognition work.** The user approved D61's recommendations.
Script 99 checks the saved maximal order, its trace determinant 2^126,
ramification, proved class number and full unit signatures. It retains
the full 116-vertex/155-edge genus-40 graph before quotienting: nine
reversed edges, no fixed vertices, H1 eigenspaces 16/24, and the same
stable weighted genus-16 graph as D45. Kurihara's original §3 explicitly
handles torsion and reversed edge classes at arbitrary residue
characteristic. This supports the geometric identification underlying
the nonhyperellipticity conclusion; it does not claim an external
resolution of the published conflict or new analytic error certification.

Mascot's pinned LiftTors now runs locally. The user's Q8 curve exercises
actual section-space divisor arithmetic, a full 2-torsion basis, lifting
to 7^64, Frobenius, evaluation and a separating degree-15 polynomial.
Exact factorization recovers the known Q(i) field. Generic nonbranch
auxiliary points are needed; the branch-point evaluation trial stalled.
The equation is removed after initialization, testing the matrix interface.
A genus-16 known-answer lift passes at 97^4 in about 10.2 s. A genus-64
control initializes and doubles but exceeds a 2 GB stack in PicLiftTors.
A preceding validator allocation issue has an exact batched replacement;
70 comparisons with upstream, including corrupted inputs, all agree.
The existing 111 regression tests also pass. Do not count the failed
genus-64 lift as a passing control or infer production cost from genus 2.

*Decision:* next address the measured allocation inside PicLiftTors and
repeat the same genus-64 known-answer control before major target model
work. Do not automatically raise memory, precision or the CM bank. The
eventual frontend is specified by D0=pi^*(43P), degree 129, with 66 initial
sections (trace split 28+38) and at least 646 evaluation points. Their
arithmetic construction on the actual Y remains missing. See
`curve-identification-audit.md`, `lifttors-control.md` and
`arithmetic-section-interface.md`. The runner records the larger failure
and deliberately exits 1. No target curve/model, torsion or nonsolvable
polynomial is claimed; no remote job, external message, commit or cleanup.
This ledger, REFERENCES and handoff are updated.

**D63 (2026-09-16). Repair the measured lifting allocations and repeat
the genus-64 known-answer control under the same memory cap.** The
user approved this next step. Instrumenting the original routine shows
1.71 GB used after only 48 of 129 precomputed product matrices. Moving
each product into its derivative worker removes that allocation, but
exposes a second overflow in the full 21,252-by-259 kernel solve.
The final adaptation selects independent original rows modulo p in
batches of 256, solves the smaller system, and verifies every equation
at full precision. A unit pivot minor and the complete residual check
prove equality with the original kernel on its good-reduction domain;
no equation is randomly omitted. Original routines remain callable and
the pinned vendor checkout is unchanged.

The genus-64 control at p=97, a=2, e=4 now passes with the original
2 GB PARI stack cap. One lift takes 613.521 s; the complete control
takes 784.161 s. The result matches the independently known exact
branch divisor and is killed by 2. The Q8 end-to-end and genus-16
controls pass, as do 70 validator comparisons, 60 lift comparisons,
12 prescribed kernels, 6 rank-drop rejection cases, and the separate
111 existing regression tests. Historical failures are retained as
failures; the current runner exits 0. See `lifttors-memory.md` and
`lifttors_controls.json` for code, hashes, scope and timings.

*Decision:* this clears the measured genus-64/a=2 gate, not production
feasibility. The full system still stores 5,504,268 field entries.
Next measure residue-degree-51 cost on a smaller known curve (g=4,
e=4, same cap and timeout) before any genus-64/a=51 attempt. That
calibration is not yet run. The target's arithmetic section entries
and a mechanism to construct and lift them remain missing; no target
torsion or nonsolvable polynomial is obtained. Further CM scans stay
paused. This ledger, REFERENCES and handoff are updated. No remote job,
external message, external checkout edit, commit or cleanup.

**D64 (2026-09-16). Calibrate residue degree 51 and verify a way to avoid
storing the full lifting matrix.** The user asked to continue D63's
bounded experiment. The same genus-4 known curve at p=97, e=4 passes
at a=2 and a=51 under the unchanged 2 GB PARI stack cap and 900-second
timeout. One lift takes 0.264 s versus 8.356 s; the full controls take
0.405 s and 10.116 s. Evaluation counts also change from 46 to 51,
so the 31.65 timing ratio is not a pure field-degree multiplier or a
genus-64 forecast. The control point is rational, while irreducibility,
Frobenius cycles and equation-entry witnesses verify use of the full
degree-51 coefficient field. It is not the target representation.

The degree-51 equation matrices occupy about 5.1 MB for 3,078 entries.
Their measured entry payloads project to 9.10–9.11 GB for D63's
5,504,268-entry genus-64 matrix. This is a conditional object-size
extrapolation, not measured peak memory or a target lower bound.
A row-generation formula derived from the existing Schur-complement
derivative avoids materializing that matrix. Script 106 checks all
11,172 entries in four small systems, equality of their kernels, and
every equation at full derivative precision. All pass. At g=64 the
equation buffer would have 1/66 as many entries; other storage remains.

*Decision:* integrate the checked formula into a separately selectable
native path, retaining comparisons and complete residual verification,
before any genus-64/a=51 attempt. This session supplies a GP prototype,
not that production integration or a proof it fits the cap. Script 105
collects the four passing controls, source hashes and projections into
`lifttors_extension.json`; see `lifttors-extension.md`. The D63 backend
and recorded source digests are unchanged; its 111-test result remains
the latest full regression run. No larger job was launched. Actual
target arithmetic sections and their lifting mechanism still need
construction; no target torsion or nonsolvable polynomial is obtained.
CM scans remain paused. DECISIONS, REFERENCES and handoff are current;
no remote job, external message, checkout edit, commit or cleanup.

**D65 (2026-09-17). Integrate generated equation blocks into native
torsion lifting, preserving the preceding comparison paths.** The user
asked to continue after D64. A separate build uses `lifttors_rows.c`
and the checked source adapter `lifttors_rows.py`; the original and
D63 lifting functions remain callable. The native path retains only
S,H caches, an equation block, selected original rows and their kernel.
It regenerates every equation at full derivative precision, including
precision p. A unit pivot minor and complete residual verification give
the same kernel; rank drop raises the explicit good-reduction error.
No full derivative matrix or eager product bank is allocated by this path.

All nine D65 jobs pass: 11,172 native/GP/original entry comparisons,
60 three-way lift cases, 12 prescribed kernels, 6 rank-drop rejections,
the Q8 field recovery, genus-4 a=2/51 controls, and genus-16/64 a=2
controls. The genus-64 lift takes 514.585 s and its whole control
690.829 s under the unchanged 2 GB cap and 900-second timeout. It
equals the exact branch divisor modulo 97^4 and is killed by 2.
Both kernels have rank 129 and nullity 130, scanning and replaying all
66 blocks. The largest block is 7,343,000 bytes and has 83,398 entries,
versus 5,504,268 in the full matrix. Other group operations still grow
the stack to its cap. Object sizes and internal stack checkpoints are
not peak RSS. The 16% shorter lift time than D63 is one local comparison,
not a production forecast; most runtime lies outside the kernel stage.

*Decision:* the native integration and its bounded controls are complete.
Next run genus 16 at a=51, e=4 with the same cap and timeout to measure
the remaining cost before a genus-64/a=51 attempt. That optional job
has not been launched; script 107 exposes it through `--only genus16_a51`.
Do not continue kernel tuning without a measured bottleneck. The actual
target arithmetic section construction and lift mechanism remain missing;
no target torsion or nonsolvable polynomial is obtained. CM scans remain
paused. See `lifttors-rows.md` and `lifttors_rows.json`. D63/D64 recorded
source digests, builds and computational outputs remain unchanged;
their 111-test result is still the latest full Python/Sage run. An initial
collector rejected a normal GP stack-growth warning; the corrected
collector and invalid-log controls pass without repeating the arithmetic.
DECISIONS, REFERENCES and handoff are current. No jobs remain running;
no remote job, external message, checkout edit, commit or cleanup.

**D66 (2026-09-17). Complete the bounded degree-51 calibration and
correct auxiliary evaluation-table reduction before further scaling.**
The user asked to continue D65's approach. The unchanged D65 library
passes the genus-16 control at p=97,a=51,e=4 under the same 2 GB stack
cap and 900-second timeout. The lift takes 364.194 s; the whole process
439.776 s. Equality with the exact branch divisor and annihilation by
2 are checked. All 18 blocks are scanned and replayed in both kernels,
which account for 40.253 s, about 11% of lift time. The rational control
point is not the target residual representation.

An audit of retained data finds an independent upstream bug:
`RRspaceEval` supplies vectors of embedding matrices, but `PicRed`
passes those vectors to the matrix-only reducer. Script 110 reproduces
ten incorrect auxiliary reductions while checking that the main section
and equation matrices reduce correctly. Earlier lift controls do not
read the damaged fields, and earlier Q8 evaluation uses the unreduced
Jacobian. Their stated results remain valid; they did not test this
compatibility. A separate build reduces each embedding matrix and
retains `PicRed_original` for diagnosis, preserving D63–D65 artifacts.

The correction passes 25 independent embedding-matrix reductions,
80 projective vectors from 20 point evaluations across five precisions,
15 nested reductions, idempotence and two malformed-shape rejections.
All 60 three-way lift comparisons and Q8 field recovery also pass with
the corrected primitive. The native controls are separate from D63's
111-test Python/Sage regression result.

The corrected genus-16/a=51 control also passes: 364.732 s per lift,
440.569 s overall, with exact-divisor and 2-torsion checks under the
unchanged limits. Its kernel sizes and ranks match the baseline.
This is recorded separately; no genus-64 control has been rerun with
the corrected library. The complete D66 collection exits 0, and no
jobs remain running.

The actual degree-51 section field is checked independently, including
four length-51 Frobenius cycles and an entry outside both maximal proper
subfields. The correctly reduced genus-16 Jacobian still occupies
120.425 MB at precision exponent 2. Component-wise extrapolation to
genus 64 and 663 evaluation points gives about 1.473 GB of principal
matrix object trees. This assumes comparable known-curve basis shapes
and entry representations; it is neither peak RSS nor a stack lower
bound. Caller-held reduced Jacobian, GWV and Schur data remain after
the full derivative matrix has been removed.

*Decision:* hold the genus-64/a=51 run and leave the cap unchanged.
Next instrument those retained allocations and group-operation stages
on the corrected genus-16/a=51 control, then choose a measured change.
Do not repeat kernel tuning without a cause. Target arithmetic section
construction and its p-adic lift remain the principal mathematical gap;
no target torsion or nonsolvable polynomial is obtained. CM scans remain
paused. See `lifttors-degree51.md` and `lifttors_degree51.json` for the
separate original/corrected logs and source provenance. No remote job,
external message, checkout edit, commit or cleanup.

**D67 (2026-09-17). Measure caller allocations and group-operation
cost before choosing another backend change.** The user asked to
continue D66's bounded allocation audit. A separate diagnostic build
retains every original arithmetic and reclamation statement. Removing
the hooks recovers all C tokens in the four generated source files.
Twenty tracing-off/on comparisons preserve exact matrix representatives
and random states and agree with saved torsion points. The genus-4/a=51
and genus-16/a=51 controls both pass under the same 2 GB cap and
900-second timeout. D63–D66 inputs and builds remain unchanged.

The genus-16 lift takes 368.023 s, whole control 444.494 s. Its 1,270
events form 294 complete calls. Group multiplication occupies 300.179 s
(about 82%); kernel and equation construction are disjoint leaf categories
totalling 303.401 s. These totals overlap by nesting, so they must not
be added together. Reduced-J copying takes 0.098 s but retains substantial
data. The generated-row kernel stages still occupy about 11% of the lift.

The caller occupies 273,164,736 stack bytes at lift entry. Forming a
34,458,640-byte GWV tree adds 136,524,504 stack bytes. The Schur mark
is set after that product workspace, so collecting the kernel leaves
it in memory throughout the following group operations. Source inspection
shows no further use of GWV after the kernel is obtained. `DivMul` also
returns its matrix without a local collection of intermediate products.
The largest observed checkpoint is 1,053,617,264 bytes inside the first
inflation's divisor-subtraction kernel, 780,452,528 above lift entry.
Growth to the 2 GB capacity occurs in that kernel's rank-selection
interval. Checkpoints and object-tree sizes are not peak RSS or proof
that the full capacity was used.

*Decision:* next test moving the Schur workspace mark before GWV and
collecting `DivMul` outputs, preserving comparison paths in a separate
build and rerunning the bounded controls. These cleanups are selected,
not yet implemented; no speedup or memory saving is claimed. Keep all
required Jacobian fields and D66's auxiliary-table correction. No
genus-64/a=51 attempt, cap increase or further kernel redesign follows
automatically. The actual target arithmetic section construction and
its compatible p-adic lift remain open; no target torsion or polynomial
is obtained. CM scans remain paused. See `lifttors-allocation.md` and
`lifttors_profile.json`. All jobs and collection pass; none remain
running. D63's 111 tests are still the latest full Python/Sage run.
DECISIONS, REFERENCES and handoff are current. No remote job, external
message, checkout edit, commit or cleanup.

**2026-09-18 — Strategic orientation after D67 (no new computation).**
The user says they have lost the thread and asks whether there is a
path to the field. The distinction to restore is between a supported
mathematical route and an executable field construction. D51 identifies
the intended residual systems in the specified Jacobian; marked descent
clarifies fields of definition with its stated qualifications. Neither
supplies arithmetic equations or section evaluations on the actual Y.
D62–D67 test and improve downstream arithmetic on known control curves.
Those results do not compute target torsion or remove the input gap.

*Recommendation:* pause the proposed memory cleanups and prioritize
an explicit target-arithmetic construction, with an independently
checkable exact section relation or evaluation table as its first
deliverable and a stated connection to a usable global model or lifted
Jacobian input. No such construction is currently implemented or newly
found in this review. This recommendation is recorded as such; it does
not claim a replacement algorithm has been selected or approved. Full
target-scale computation, arithmetic projection, recognition and final
certification remain ahead. D67's measurements and proposed cleanups
are preserved. No new benchmark or CM scan is launched.

**D68 (2026-09-18). Use the entire degree-17 CM divisor as a canonical
projective frame; verify the resulting equation candidate next.**
The user suggested M23/rigidity, Belyi code, the 17T7 paper (“7t17”),
and HMF code for curve construction. The focused review distinguishes
the general Belyi canonical-reconstruction method from the local
entry point's nonhyperelliptic genus limit, the 17T7 genus-four
period/invariant reconstruction from arbitrary-genus reconstruction,
and HMF Fourier products from the quaternionic canonical ring.
The van Bommel–Costa–Poonen–Srinivasan algorithm requires an arithmetic
differential basis as input. See `curve-construction-sources-2026-09-18.md`.

*New construction:* on a genus-g curve with a nonspecial closed divisor
D of degree g+1, Riemann–Roch gives a pencil L(D). Residues of h*omega,
for h in that pencil, identify H0(K) with the trace-zero residue
algebra, up to common scale. A numerical left kernel obtains the
necessary row multipliers without constructing h. For our seventeen
CM points, the known labelled degree-17 field therefore provides an
arithmetic projective frame. This is a local adaptation, not a result
attributed to the source papers. The general argument is exact; target
rank and inherited geometric/orbit hypotheses remain qualified.

Script 114 passes an exact Fermat-quartic control, then applies the
construction to the existing N=16384/12288 banks. The 91-dimensional
quadric spaces agree to relative 6.12e-15 in a fixed normalization.
No new differential solve is used. Script 115 first imposes exact
vanishing at the CM divisor, leaving a saturated integer lattice of
rank 119. One bounded lattice search finds 91 independent integer
quadrics with maximum coefficient 1,514. Their row lattice is also
saturated; all equations vanish exactly at the prescribed CM point.
Numerical residuals on both banks support the discovery but do not
certify relations on the Shimura curve.

Script 116 passes a nonsplit cubic-divisor control and exact Magma
checks: the candidate over Q has degree 30, arithmetic genus 16 and
a 105-element Gröbner basis. A monic basis integral at 31 supplies
a flat model whose special fiber is reduced and irreducible. The
specified point has residue degree 17. The candidate is exported as
`cm_frame_curve_candidate.{json,m}`. No exact P32 coordinate vector
is recovered. General smoothness hits the Jacobian-minor count limit;
a separate normalization/genus probe times out at 180 seconds. These
outcomes are retained and are not positive smoothness checks.

*Decision:* prioritize verification of this concrete curve candidate,
starting with a more suitable smoothness/normalization calculation
and an independent arithmetic comparison with the specified Shimura
datum. State a sufficient identification criterion; matching genus
and a CM point is not enough. Once identified, construct the actual
degree-three cover Y/C before target torsion. Backend cleanup and
the unchanged CM-function scans remain paused. This supersedes the
claim that no arithmetic equation candidate exists, but does not
claim the actual target input or field polynomial has been obtained.
The three main scripts complete successfully; the two smoothness
probes have the limited outcomes above. D63's 111 tests remain the
latest full regression suite. No jobs remain running. Work is local
and uncommitted; previous artifacts and external checkouts are
unchanged, with no remote job or external message.

**D69 (2026-09-18). Certify the candidate by a finite free projection;
separate the resulting smooth curve from its Shimura identification.**
The user asked to continue D68 verification. Instead of repeating the
failed large-minor and normalization calls, the Gröbner basis gives a
rank-30 free module over the last two coordinates, with basis degrees
`0,1^14,2^14,3`. On each chart of the resulting P1 projection, the
exact trace discriminant has degree 90 and is squarefree modulo 31.
An index-squared argument proves normality, hence smoothness; the
monic flat model transfers it to Q. The graded free basis and
Riemann–Roch prove geometric integrality and the canonical embedding.
Thus the unchanged equations now provably define a smooth canonical
genus-16 curve over Q, with good reduction at 31.

Magma script 117 checks a smooth conic, a singular cusp and a smooth
cubic with repeated branch discriminant, explicitly keeping the
criterion one-sided. Independent multiplication-matrix calculations
check the target trace pairing on four fibers. Script 118 counts
points on every degree-30 fiber over F31 and F31², exploiting base
Frobenius orbits in degree two. The counts are 50 and 1,400, exactly
the predictions from the four saved quartic T31 constituents of the
genus-16 quotient. These are two counts at one split prime, not a
full Euler factor or two distinct-prime checks.

Python runner `117_cm_frame_verification.py` runs the three jobs with
180 seconds and 2 GB per job, requires PASS markers and no errors,
and saves source/log hashes plus all fiber counts. All jobs pass.
See `cm-frame-verification.md` and `cm_frame_curve_verification.json`.
No D68 candidate, numerical bank or earlier backend artifact changes.

*Decision:* next obtain independently justified arithmetic local data
on the specified Shimura curve, or another sufficient identification
theorem. One explicit sufficient test is order-four vanishing of each
quadric at its degree-17 CM point: `4*17>deg(2K)=60`. vBCPS supplies
that vanishing bound, but exact Shimura-side jets in matching
arithmetic coordinates remain missing. Jets derived from the candidate
itself would not identify it. The successful point counts strengthen
evidence without discharging this proof obligation. Then construct
the actual degree-three Y/C before target torsion; the desired field
polynomial is still open. Backend cleanup and old CM-function scans
remain paused. D63's 111 tests remain the latest full regression run;
D69's exact certificates are separate. No jobs remain running, remote
job, external checkout edit, message, commit or cleanup.

**D70 (2026-09-18). Recover the marked branch candidates on the exact
curve; retain the separate Shimura-identification obligation.**
The requested continuation first reviews the availability of exact
Shimura-side jets. Voight–Willis's numerical method and CM algebraicity
do not supply them. Guillemot–Voight's certified Belyi monodromy
workflow needs an exact map and specified triple, which we do not have
for this identification. No new identification theorem is claimed.

The exact curve nevertheless permits concrete progress on the cover
input. Script 119 uses D68's arithmetic frame and the two unchanged
banks. One projective LLL run recovers an exact rational point of
primitive height 3310032844768591087; D68's 10^12 cap had excluded it.
All 91 quadrics vanish. Exact implicit jets modulo 31 have rank 16
and determinant 8, proving that the point is ordinary on the
candidate over F31 and Q. This is not an independent Shimura-side
jet calculation or a proof of the proposed order-32 CM label.

Order-two Cauchy coefficients at the nine order-three elliptic
points, checked on two radii and both banks, yield seven integer
linear forms of height at most 54. Their intersection with the
curve is exactly one reduced degree-nine closed point B3. Script
120 verifies its disjointness from P32 and D17, and monic flat
models with reduced disjoint specializations at 31. Elimination
gives a nonic residue polynomial. Its Galois group 9T15, order 72,
is proved with `GaloisProof`, including the normal (C3)^2 and cyclic
order-eight stabilizer. This is an auxiliary solvable field, not
the target field, and its CM class-field identification is open.
A default maximal-order probe times out at 90 s before printing
a discriminant; preserve the failure and do not repeat unchanged.

Set B2=D17+P32. The plausible simplifying relation B2~2B3 is
rigorously excluded: a residual-ideal computation in |2K| gives
h0(2B3-B2)=0 modulo 31, and the verified flat markings allow
semicontinuity to transfer that result to Q. This rules out that
particular quadratic-resolvent recipe, not the required cover.

*Decision:* use the explicit marked candidate as input to recovering
the cover's extension data with the saved full S3 monodromy. The
quadratic resolvent selected by the sign character is a concrete
intermediate target: recover its square class, equivalently the
degree-nine L with L^2=O(B2) and its branch section. L is not O(B3).
No square-class reconstruction algorithm is yet implemented; the
branch locations alone do not select the cover. Working over F is
allowed, without assuming Q descent. Keep independent base-curve
identification as a separate proof obligation. The actual genus-64
Y, target torsion and field polynomial remain unconstructed.

See `cm-frame-marks.md`, scripts 119–120 and their saved JSON/Magma
data. Script 119 finishes in about 20 s; the exact job passes in
46.070 s under 120 s/2 GB limits, with required PASS/error checks.
D68/D69 artifacts, earlier backends and external checkouts remain
unchanged. D63's 111 tests are still the latest full regression
suite; these targeted algebraic certificates are separate. Backend
optimization and old CM-function scans remain paused. Ledgers and
handoff are updated; no job remains running, external message,
remote job, commit or cleanup.

**D71 (2026-09-18). Construct and certify a finite-field quadratic
resolvent candidate before attempting a characteristic-zero lift.**
The requested continuation targets the sign double cover branched at
B2=D17+P32. The old cover differential bank is insufficient for direct
arithmetic recognition, so no unchanged numerical run is repeated.

The genus-16 Hecke polynomial suggests the odd Jacobian order
N=1640801490553691915934375. This is not proved for the candidate.
Use `[(N+1)/2](D17-17P32)` only as a proposed half class, then verify
the resulting relation directly. This separates a useful discovery
guess from the certificate required for the final cover.

Generic FunctionField(C) times out at 90 s. An explicit function field
from the rank-30 coordinate algebra, using its known integral bases
and trace-discriminant proof, recovers genus 16 in about 36 s and the
marked places in 44 s. Native Reduction nevertheless times out at
150 s. Preserve these probes and avoid repeating them unchanged.
Canonical quadrics and saturated colon ideals provide an effective
alternative: represent classes by E-deg(E)P32 with deg(E)<=16, then
reduce products by two complementary divisors in |2K|.

The 80-bit scalar computation succeeds in 466.760 s under 900 s/2 GB.
It gives E of degree 16 and explicit quadrics satisfying
div(q_num/q_den)=D17+15P32-2E. An independent script verifies this
identity without the Hecke guess, proving L=O(E-7P32) is a degree-nine
half of B2 over F31. The smooth projective model of z²=q_num/q_den
is geometrically connected of genus 40 with the required 18 branch
points. The two constant twists have 45 and 55 F31-points; 45 agrees
with the genus-40 norm-one Hecke prediction. This does not prove the
Jacobian order, absence of two-torsion, uniqueness of the half class,
or identification with the desired sign cover.

The independent certificate and complete rational-fiber enumeration
pass in 10.897 s under 120 s/2 GB. Exact implicit jets handle two
common zeros of the numerator and denominator. A separate negative
control changes the X1² numerator coefficient and is correctly
rejected in 2.026 s. Source/log hashes and explicit PASS/error checks
are retained. Read `cm-frame-resolvent.md`, scripts 121–122 and
`cm_frame_resolvent{,_check}.json`.

*Decision:* next implement a first lift of L²=O(B2) modulo 31²,
checking the doubled class. Doubling's invertible differential gives
the local Newton/Hensel route; no lifting implementation or arithmetic
recognition has been completed. Then seek recognition over F and
match the saved sign monodromy before the cyclic cubic extension and
genus-64 quotient. Do not interpret finite-field coefficients as a
characteristic-zero equation, and do not assume Q descent. Independent
base-curve identification, including the prior hyperellipticity
conflict, remains an unresolved proof obligation. Target torsion and
the desired nonsolvable field polynomial remain unconstructed.

DECISIONS, REFERENCES, handoff and entry-point READMEs are updated.
D68–D70 inputs, numerical banks, external checkouts and backend code
remain unchanged. D63's 111 tests are the latest full backend suite;
these exact certificates are separate. Backend optimization and old
CM-function scans stay paused. All jobs finished; work is local and
uncommitted, with no remote job, external message, commit or cleanup.

**D72 (2026-09-18). Lift the certified branch half, then measure the
normalization cost before requesting substantially more precision.**
The user asks why there are so many branch points and to continue
with the lift. The saved sign character is negative at the seventeen
order-two transpositions and the order-32 transposition, giving 18
geometric branch points. It is positive on the nine 3-cycles. This
is a double cover of genus-16 C; the three-branch-value property for
Belyi maps to P1 does not constrain it. D17 is one closed point
packaging seventeen geometric points.

Script 123 exports exact étale support algebras for D17, E and the
common residual divisor T, with factor degrees [17], [2,2,2,10] and
[1,1,3,23]. X15/X16 separates their points and is unramified there.
Thus a direct local Newton calculation avoids D71's expensive class
arithmetic. At each digit, script 124 corrects q_num using 32 value/jet
conditions, q_den using 44 value conditions, then the sixteen double
zeros using their unit second coefficients. All 91 curve equations
and all needed residuals are checked over the exact finite rings.

Compatible lifts through 31²,...,31⁸ succeed. The final modulus is
852891037441, and the independent Magma script 125 verifies
div(q_num/q_den)=D17+15P32-2E there. The proof uses flat étale divisors,
exact jets, unit leading coefficients, disjointness and exhaustive
degree-60 accounting for both quadric sections. A control changing
only the highest digit is rejected, despite agreeing modulo 31^7.
The seven Sage steps take 38.547 s including startup (35.363 s
internally). The independent checker takes about two seconds.
The lift has a 240 s timeout; Magma jobs have 120 s/2 GB limits.
Sage jobs do not impose the Magma memory cap.

Script 126 independently solves the numerator's rational linear
conditions over Q and matches all eight digits. It completes in
7.643 s including startup. This recovers only the numerator, not
the denominator, square class or number-field cover. The primitive
numerator height has 631 decimal digits (2,096 bits). Its known
affine coefficient bounds give n=845 as a sufficient uniform bound
31^n>2UV for unique bounded rational reconstruction. This is neither
a minimal precision threshold nor a height bound for the unknown
denominator. The rational numerator is already obtained exactly.

*Decision:* next seek a smaller integral normalization in the exact
13-dimensional numerator space. Transform numerator and denominator
together and check that the square class is preserved. No such
normalization reduction is implemented yet. Then use precision
doubling to obtain higher accuracy and seek arithmetic recognition
over F. Hundreds of successive digits in the current normalization
are not the default next run. The lift is established; the observed
coefficient height now gives a concrete reason to address normalization.

Read `cm-frame-resolvent-lift.md`, scripts 123–126 and the saved
`cm_frame_resolvent_lift{,_check}.json` and
`cm_frame_lift_numerator.json`. The runner supports reproduction,
independent checking, a highest-digit control and hash collection.
The full cover over a number field, Shimura identification (including
the prior hyperellipticity conflict), specified cyclic cubic extension,
genus-64 Y, target torsion and nonsolvable polynomial remain open.
Q descent of the cover is not assumed.

DECISIONS, REFERENCES, handoff and entry-point READMEs are updated.
D68–D71 artifacts, numerical banks, backend code and external checkouts
are unchanged. Backend optimization and old CM-function scans remain
paused. D63's 111 tests remain the latest full backend regression;
these targeted exact certificates are separate. All jobs finished;
work is local and uncommitted, with no remote job, external message,
commit or cleanup.

**D73 (2026-09-18). Reduce the integral section lattice, including known
curve relations, and certify a transfer preserving the radicand.**
The user approves the normalization plan and suggests revisiting M23.
Section 3's treatment of equations modulo known relations motivates
testing all 136 quadratic coefficients as well as the existing
45-monomial section chart. Our integer-kernel/LLL implementation is a
local adaptation, not the separate reduction algorithm in Zhang's note.

Script 127 forms the exact rank-32 constraint matrix for D17+15P32.
The integer kernel in the old chart has rank 13 and gives a primitive
numerator of 48 decimal digits, versus D72's 631. The full kernel has
rank 104, with 91 curve-relation directions; its best accepted section
has **39 digits / 127 bits**, height
119732280500973149122871877303430862720. Unit Smith invariants certify
both kernels are saturated. There are 322 distinct accepted candidates
from basis vectors and pairwise sums/differences. This is a measured
improvement, not a shortest-vector or optimal-height theorem.

Script 128 selects the first candidate and solves n*d'=n'*d over
Z/31^8 in the coordinate ring. The multiplication matrix has rank 45
in 105 quartic coordinates, with a unit square minor; all remaining
equations pass. Thus n'/d' equals the saved radicand at this precision,
preserving its twist, E and the half L=O(E-7P32). The new degree-28
common residual T' is reduced, has factor degrees [1,1,26], and has a
verified univariate presentation with unramified separating coordinate.

Independent script 129 verifies the exact numerator over Q by ideal
membership and a fresh rational implicit-jet calculation. It checks
the full-precision quartic identity and local orders, and independently
checks the residue divisor ideals and Jacobian ranks. Adding 31^7 to
one denominator coefficient leaves the seven lower digits unchanged
but fails the quartic identity as required. Search takes 53.058 s;
transfer 9.987 s; independent certificate 20.524 s; negative control
14.501 s. Sage has a 240 s timeout with no memory cap; Magma has
180 s/2 GB limits. The runner checks saved provenance transitively.

*Decision:* retain the 39-digit numerator in its full monomial form.
Next implement precision doubling and seek recognition over F. Track
scale explicitly: extending D72 and repeating the cross-product
transfer is a safe comparison path. A new arbitrary denominator scale
requires an explicit square-factor/isomorphism check before asserting
the same cover. T' is currently exported modulo 31 only; its simple
zeros can be lifted against the exact numerator. No higher normalized
support lift or precision-doubling implementation is claimed here.

The experiment establishes a substantial numerator reduction, but
does not bound the denominator's arithmetic height. The number-field
cover, Shimura identification, earlier hyperellipticity conflict,
specified cyclic cubic extension, genus-64 Y, target torsion and field
polynomial remain open. Read `cm-frame-normalization.md`, scripts
127–129, and `cm_frame_normalization_check.json`; runner 129 supports
default verification, `--collect-only`, and full `--rebuild`.

DECISIONS, REFERENCES, handoff and entry-point READMEs are updated.
D68–D72 arithmetic artifacts, numerical banks, backend code and external
checkouts are unchanged. Backend optimization and old CM scans remain
paused. D63's 111 tests remain the latest full backend regression;
these targeted exact certificates are separate. All jobs finished;
work is local and uncommitted, with no remote job, external message,
commit or cleanup.

**D74 (2026-09-18). Double the certified precision, test recognition on
unused digits, and construct a smaller exact denominator space.**
The user asks to continue. Script 130 implements Newton steps from
31^e to 31^(2e), reducing the already known rational numerator and
preserving D72's denominator scale. Unit-pivot elimination and scalar
Newton inverses handle finite étale algebras over the composite base
ring. A 4->8 control agrees in every saved coefficient, support point,
tangent and jet with the successive-digit implementation. All four
stages 8->16->32->64->128 pass in 52.198 s including startup/control,
under 900 s without a Sage memory cap.

Runner 131 uses hashed copies of Magma 125/128/129 with only data paths
changed. At every stage it independently certifies the divisor relation,
transfers to the 39-digit numerator by n*d'=n'*d, and verifies that
saved equality and local orders. All reductions are compatible. A
31^127 denominator perturbation is rejected. The scalar, branch half
and twist at the stated finite precision are preserved. Magma jobs
retain 240 s/2 GB bounds. No characteristic-zero cover is inferred
from these finite-ring certificates.

Script 132 tests Q and F coefficient recognition in affine coordinates
and projective ratios, at training/validation pairs 16/32, 32/64 and
64/128. All eight embeddings of F at 31 are tested. Every candidate
fails unused-digit validation; exact Q/F positive controls and
perturbed-unused-digit controls pass. This is not a nonmembership or
height-exclusion result. The known 39-digit numerator becomes 144 digits
in the 45-monomial chart, with affine bounds 144/104 digits. Script 133
therefore tests whole rational quadrics modulo the 91 known relations.
It recovers the exact numerator control, but none of 43 denominator
candidates survives. The smallest returned vector has 88 digits;
this is not a lower bound. Jobs 132/133 take 5.003/35.780 s.

*Further reduction:* the denominator vanishes on the rational common
residual T' of degree 28. Thus it lies in W=H0(2K-T'), dimension 17.
Script 134 selects another exact numerator r nonvanishing on T' and
computes the kernel of r*d=n'*s in H0(4K). The 90-by-105 matrix has
rank 73 and its projection to d is injective. This exact construction
takes 12.466 s under 180 s/2 GB. Its initial rational basis has up to
1,322-digit coefficients.

Script 135 computes the saturated rank-108 integer lattice, with 91
curve-relation directions. Unit Smith invariants certify saturation;
the seventeen section directions have heights
[39,43,43,47,51,55,59,63,65,69,72,77,80,84,88,93,96] digits. A generic
rational-nullspace attempt timed out at 300 s and is archived with
its exact source and limit. The successful implementation eliminates
an existing identity block, building the 28 constraints in 0.358 s
and finishing all reduction/recognition work in 59.463 s under the
same limit. Do not repeat the old probe unchanged.

Magma 136 independently verifies all seventeen exact paired identities,
independence modulo curve equations, and the expression of the same
128-digit denominator in this basis. It takes 6.116 s. A 31^127 error
in a basis coordinate is rejected in 5.619 s, under 180 s/2 GB. The
coordinates agree at 32/64/128 digits. Coefficientwise Q/F recognition
still yields no surviving affine/projective candidates in this space.

*Decision:* next try joint projective F reconstruction in W, representing
the seventeen coordinates by polynomials of degree at most seven in
the F generator and allowing a common F-valued scale. This can avoid
growth from independently dividing coordinates and using rational
integer denominators. It is not yet implemented or guaranteed to
succeed. Use the existing 64/128 validation split, recover the recorded
scalar, and require exact algebraic verification of a recognized
candidate. More lifting is not the next default action.

Read `cm-frame-precision-doubling.md`; runner 131 reproduces/checks the
lift and transfer, and runner 137 certifies/collects the reduced-space
and recognition work. The combined record is `cm_frame_arithmetic_check.json`.
Number-field reconstruction, independent Shimura/marking/sign-cover
identification, the prior hyperellipticity conflict, the specified cubic
extension, genus-64 Y, target torsion and the nonsolvable polynomial
remain open. No descent to Q or F is inferred from failed searches.

DECISIONS, REFERENCES, handoff and entry-point READMEs are current.
D68–D73 arithmetic artifacts, numerical banks, backend code and external
checkouts are unchanged. Backend optimization and old CM scans remain
paused; D63's 111 tests remain the latest full backend suite. These
targeted exact certificates are separate. All jobs finished; work is
local and uncommitted, without remote jobs, messages, commits or cleanup.

**D75 (2026-09-18). Complete joint F recognition, then change the auxiliary
divisor to obtain a height-583 numerator.** The user asks to continue.
Script 138 constructs the rank-136 congruence lattice for seventeen
degree-seven polynomials with a common F-valued scale. Sixteen identity
columns certify its index (31^64)^16; reduction and index are verified
exactly. Training uses 64 digits and validation 128. An exact F control
has eight surviving projective representatives although separate ratio
recognition finds none. None of 765 tested denominator rows survives,
at any of the eight embeddings; every failure occurs at the first unused
digit. Nonunit-anchor rows are skipped by this candidate search.

Script 139 gives a rigorous exclusion separately from LLL's unsuccessful
search. For each full lattice basis R, D=31^64*R^-1 is integral and
R*D=31^64*I. If S is the largest column l1 norm of D, an integer lattice
vector with coordinate bound H and H*S<31^64 is zero. The uniform
excluded bound is 8066216. This applies to all nonzero lattice vectors
in D74's fixed section and field power bases, not to arbitrary
normalizations and not to descent itself. Magma 140 checks every row,
the exact F control, all inverse certificates and unused-digit errors.
Runner 141 records the checks. Whole jobs 138/139 take 31.380/4.214 s;
independent verification and its corruption control take 6.752/0.879 s.

*Geometric normalization:* the old branch half is L=O(E-7P32), deg E=16.
Use the known degree-nine divisor B3 to represent L as O(E_new-B3),
deg E_new=18. This is distinct from the excluded claim L=O(B3).
Script 142 constructs H0(2K-B2-2B3), dimension 9, with B2=D17+P32.
The full integer kernel has rank 100 and unit Smith invariants. All
100 LLL rows have nonzero section images: the small section directions
mix with curve relations. Nine independent representatives have 3–4
digit heights. Among 172 basis/pairwise candidates, the first has
primitive coefficient height 583 and passes the geometric gate.
This replaces the 39-digit numerator and takes 21.872 s; no shortest
vector or denominator-height theorem is claimed.

Script 143 constructs g with divisor E+B3+G, deg G=35, then the
three-dimensional space of q vanishing on G+7P32. A selected q has
divisor E_new+G+7P32. The rational numerator has divisor B2+2B3+T,
deg T=24, and d_new has divisor 2E_new+T. The global identity
n_old*g^2*d_new=n_new*d_old*q^2 fixes the scalar and certifies
w_new=w_old*g/q over F31. The odd branch divisor is still B2,
degree 18, and the double cover still has genus 40. All three moving
q sections are saved. Transfer at higher precision is not yet performed.

A direct rational residual-ideal phase timed out after 180 s/2 GB,
after the finite-field identity had passed. Its exact source, log and
job are archived as `cm_frame_B3_rational_ideal_probe`; do not repeat
unchanged. The successful replacement proves rational numerator
membership by linear algebra integral at 31. D69/D70 good reduction
and the reduced disjoint special residual certify the rational residual
via relative Cartier divisors and reduced-fibre specialization. This
finishes the transfer job in 20.390 s under the unchanged bounds.
Magma 145 independently verifies the saved data in 16.051 s. Its
wrong-twist control negates d_new, preserves every divisor, and correctly
fails the global identity in 15.709 s. Runner 144 records both results.

*Decision:* use the existing 128-digit E/support data to transfer this
B3 normalization. Lift g with fixed free coordinates, its simple
residual G, and the full three-dimensional q-space. Solve the saved
global identity for d_new and independently certify the square map and
scalar at each precision. Retain all three sections so that their six
pairwise products can also be tested as a denominator space; its rank
and arithmetic height are not yet computed. Do not blindly impose
denominator coefficient constraints that could change the half or its
field. No new precision is the next default action.

Read `cm-frame-joint-field-and-B3-normalization.md`. Combined records
are `cm_frame_joint_field_check.json` and `cm_frame_B3_check.json`;
the new equation and square factor are `cm_frame_B3_normalization.json`.
No number-field denominator or cover, Shimura identification, specified
cubic extension, genus-64 Y, target torsion or nonsolvable polynomial is
obtained. The hyperellipticity conflict remains open. DECISIONS,
REFERENCES, handoff and entry-point READMEs are updated. D68–D74 arithmetic
artifacts, including the old 128-digit lift, are preserved. Backend work
and old CM scans stay paused; no full backend suite was needed for these
targeted exact certificates. All jobs finished; local uncommitted work,
without remote work, external messages, commits or cleanup.

**D76 (2026-09-18). Recognize the full product space and construct an exact
rational double cover.** The user asks to continue. The B3 normalization
now gives w^2=n/d over Q on the certified genus-16 candidate, with integral
coefficient heights 583 and 2935433. Its smooth normalization has genus
40 and odd branch divisor B2=D17+P32, degree 18. The equation is an exact
rational construction, independently certified, with an explicit square
map to the old lift modulo 31^128. Arithmetic identification of the
Shimura/sign cover and its global twist remains a separate open problem.

Scripts 146–149 reuse the old 64/128-digit supports. The 25 conditions
for E+B3 leave a 20-dimensional section space. Lift g with fixed free
coordinates and choose h in that space which is a unit along the
degree-35 residual G. Instead of lifting G, solve h*q=g*s and impose
seven P32 jets. The 90-by-112 matrix has rank 87 and gives the entire
three-dimensional q-space. Transfer its six products through
n_old*g^2*d_ij=n*d_old*q_i*q_j; their rank is 6. Reductions at 64/128
digits agree, independent checks pass, and a 31^127 perturbation is
rejected. This implements the intended geometric change with simpler
linear algebra than explicit residual-point lifting.

Script 150 recognizes the six-dimensional denominator span over Q.
Allowing the 91 curve relations gives a rank-136 congruence lattice
of exact index (31^64)^39. Six of 45 tested nonzero section images
survive validation at 128 digits, giving six independent quadrics of
six-digit height. A known rational six-space control passes and rejects
a changed unused digit. The old arbitrary selected denominator still
has no surviving rational projective ratios. The choice to recognize
the space before choosing its square section removes that obstruction.
This does not invalidate the correctly bounded unsuccessful old searches.

Magma 151 computes the 21 products over Q: rank 15, six exact relations.
Script 152 explicitly splits their Veronese surface. The unique cubic
whose derivatives lie in the relation space has a rank-three polar at
the known rational point. A tangent two-jet supplies a rational point
on the quotient conic; splitting it and solving two syzygies gives
F0,D0,E0,A0,B0,C0 and all six exact symmetric rank-one identities.
The transformation is invertible, with d=9*F0 primitive integral.
This is an exact algebraic verification following recognition.

Script 153 chooses the second small numerator r, nonvanishing on T
modulo 31, and saves exact witnesses r*v=n*s_v for all six forms,
integral at 31. Thus the forms vanish on rational T. The common zeros
of F0,A0 at 31 are exactly T; after removing T they have no common
zeros over Q, by properness. F0*A0=D0^2 therefore forces the remaining
zeros of F0 to be even. The finite residual half E_Q is reduced of
degree 18, disjoint from T and B2+2B3. Together with D75's flat residual
certificate, this proves div(d)=T+2E_Q over Q and gives the rational
branch half O(E_Q-B3). No repeat of the archived rational-ideal timeout
was needed. Riemann–Hurwitz gives genus 40 for the normalization.

Script 154 decomposes the product coordinates of d at 128 digits into
a unit scalar times a square. The scalar is already a square at 31;
the twist multiplier is 1. Its Hensel square root gives a saved q_Q
with n_old*g^2*d=n*d_old*q_Q^2 modulo 31^128. Magma 155 independently
checks the saved rational relations/witnesses, finite divisor ideals
and this identity. Negating d and its recorded scale preserves all
divisor checks but fails the square identity. Matching one completion
does not identify the global arithmetic quadratic twist.

Whole runtimes: 146 6.781 s; 147 at 64/128 digits 23.831/24.581 s;
independent lifted checks 21.940/22.684 s and highest-digit control
18.407 s; 150 26.510 s; 151 6.987 s; 152 3.365 s; 153 30.183 s;
154 3.901 s; independent rational check 30.035 s and wrong-twist
control 29.883 s. Magma retains 180 s/2 GB, Sage explicit 180 s
timeouts (300 s for 150) with no memory cap. All jobs pass and finish.

*Decision:* next compute the normalized unramified fibre over B3,
its degree-18 étale algebra and involution. Use the leading unit of
n/d after removing its order-two zero, not naive w=0 substitution.
These supply branch data for the cyclic cubic cover Z->X and the
genus-64 reflection quotient Y. The arithmetic S3 monodromy must select
the extension; branch data alone do not. No new precision or repeated
old coefficient search is the next default. Base/marking/sign-cover
identification, the hyperellipticity conflict, global twist, genus-64
Y, target torsion and the nonsolvable field polynomial remain open.

Read `cm-frame-rational-double-cover.md`. The rational equation and
witnesses are `cm_frame_B3_rational_model.{json,m}`; the combined records
are `cm_frame_B3_lift_check.json` and `cm_frame_B3_rational_check.json`.
Runner 148 checks/rebuilds the lift, runner 156 checks/reconstructs the
rational model, and both support recursive `--collect-only` validation.
DECISIONS, REFERENCES, handoff and entry-point READMEs are current.
D68–D75 arithmetic artifacts, backend code and external checkouts are
preserved. Backend optimization stays paused; these are targeted exact
certificates, not a new full backend run. Local uncommitted work only;
no remote jobs, external messages, commits or cleanup.

**D77 (2026-09-19). Normalize the B3 fibre and isolate the cubic class
problem.** Continue from the rational genus-40 equation. Its normalized
fibre above B3 is exactly K(sqrt(-3)), degree 18 over Q, with K the
previously certified nonic residue field. Over Q(sqrt(-3)) this gives
two degree-nine divisors D+ and D-, exchanged by the double-cover
involution and by constant conjugation. Their difference is nonprincipal.
No cyclic cubic or genus-64 quotient has yet been constructed.

Scripts 157–160 use the leading unit, rather than substituting w=0
into the singular equation. With t=X15/X16-a, a nonsingular 14-by-14
Jacobian minor supplies exact two-jets satisfying all 91 quadrics.
The expansions n=n2*t^2+O(t^3), d=d0+O(t) give alpha=n2/d0.
A small rational square-class search, screened by the norm, finds
alpha=-3*s^2 in K and saves s. The negative norm proves the quadratic
algebra is a field. No maximal-order computation is invoked.

The first B3 linear form ell supplies a rational local parameter.
For W=w/(ell/X16), the branches have W=+/-sqrt(-3)*r(a), with an
explicit r. At 31 choose sqrt(-3)=11: each degree-nine branch splits
as three degree-three points. All coordinates, jets, units, the
involution and splitting idempotents are independently checked by
161. Adding 1 to alpha's constant coefficient is rejected at
n2=d0*alpha while leaving the point and zero orders unchanged.
Runner 162 records the checks and their recursive source hashes.

A constant cyclic Galois cubic over F, totally ramified above B3,
requires the residue fields to contain mu3 by the tame inertia
character. For a scalar twist c*n/d the fibre over KF is
KF(sqrt(-3*c)). Since [KF:F]=9, the odd-degree norm argument makes
this condition equivalent to c being a square in F. Thus the D76
equation is the unique F-scalar twist class of this fixed branch
half satisfying this necessary condition. This does not identify
the geometric half, the marks or the base with the Shimura data.
The twist c=-3 is square at 31 but fails the cubic inertia condition;
the new restriction is stronger than the earlier local scalar test.

Script 163 verifies a rank-nine canonical evaluation at B3, with
a 9-by-9 minor of determinant 17 modulo 31. Riemann–Roch yields
h0_C(B3)=1. D70's h0(2B3-B2)=0 excludes L~B3, so the degree-zero
bundle O(B3-L) has no section. The double-cover pushforward gives
h0_X(pi^*B3)=1. A function with divisor D+-D- would contradict this.
The direct principal-divisor shortcut is therefore excluded.

*Decision:* next represent Delta=D+-D- over F31 and seek
3[A]=-[Delta], then div(h)=Delta+3A. Neither divisibility over the
finite field nor uniqueness is assumed. The involution, constant
descent and specified Fuchsian S3 monodromy must select and verify
the eventual extension v^3=h. Branch supports alone do not select it.
No additional 31-adic precision or repeated old coefficient search
is the next default.

Whole runtimes: 157 76.599 s; 159 0.678 s; 160 5.819 s;
independent 161 43.402 s; corrupted-unit control 26.301 s.
Magma jobs retain 180 s/2 GB; Sage has 180 s without a memory cap.
All finish. Read `cm-frame-B3-fiber.md`; the combined records are
`cm_frame_B3_fiber_check.json` and `cm_frame_B3_branch_class.json`.
The arithmetic identification, hyperellipticity conflict, cubic,
genus-64 curve, target torsion and final field remain open. Earlier
artifacts and hashes are preserved; backend optimization remains
paused. Local uncommitted work only, with no remote jobs, external
messages, commits or cleanup.

**D78 (2026-09-21). Construct genus-40 divisor arithmetic and verify the
required third modulo 31.** The user asks to continue. We now have an
explicit class A with 3[A]=-[D+-D-] in J_X(F31), fixed by Frobenius
and negated by the double-cover involution. A saved-relation check uses
neither the proposed order nor the scalar search; changing A to
A+Delta is rejected. No Kummer function or cyclic cubic is constructed.

*Decision:* use section evaluations on the existing cover rather than
repeat D71's native function-field reduction timeout. Choose
D0=2*pi^*div_C(X16), degree 120. Its larger degree makes the sections
explicit: 45 even quadrics and 36 odd sections w*q3/(ell*X16^2),
where q3 vanishes on E_Q+U and div(ell)=B3+U, deg U=21. Script 164
verifies those spaces and collects 2,048 usable points over F31^2.
This is an evaluation set, not a full point count.

Script 166 selects 640 points, stable under Frobenius and the
involution, and constructs complete section spaces of dimensions
81,201,321. Since 640>5*120, all group-operation products are evaluated
injectively. A disjoint Frobenius-stable auxiliary divisor B of degree
111 gives W+/-=L(2D0-B-D+/-), each of dimension 81. The 120 branch
and auxiliary conditions have rank 120. The regular fibre coordinate
from D77 supplies the degree-nine branch constraints.

Verifier 168 checks pole bounds, point equations, evaluations, product
indices, ranks, actions and both divisor spaces without a point search
or kernel solve. A changed odd-section evaluation is rejected. The
Magma matrix model is also exported to the pinned LiftTors interface.
Its GP probe 169 validates both branch representatives and their
inequality in 56.494 s, but times out at 180 s during class operations.
Retain that record; do not repeat it unchanged or resume backend
optimization for this task.

Script 170 implements the pinned negation/chord schedule with Magma
finite-field matrices. Product spaces must attain their proved
Riemann–Roch dimension; partial quotient constraints must reduce to
the proved dimension. Equality/zero tests verify every generator of
a surviving one-dimensional space. Random choices affect runtime,
not correctness. Script 171 verifies Delta!=0, 3*Delta!=0, its
Frobenius and deck actions, and inverse cancellation, in 2.744 s.

The suggested Prym order is N=751200095370944434080214902187185651
=9*m, m=83466677263438270453357211354131739. This is not a certified
order for the candidate. Scripts 172–173 propose
c=55644451508958846968904807569421159, with 3*c+1=2*m, compute
A=c*Delta in 154 checked negation/chord steps, and test 3*A+Delta
directly. It is zero. The search takes 47.897 s. Script 175 then
reconstructs Delta and verifies the saved third with a different seed,
without loading N or the chain. A+Delta fails because 3*Delta!=0.
No uniqueness or prescribed S3-monodromy match is asserted.

The matrices use F31^2. Frobenius fixes the class A, so it lies in
J_X(F31); the displayed effective representative E need not itself
descend. *Next:* recover h with div(h)=D+-D-+3E-3D0, accounting for
the representative and descent. A zero witness for a reduced
intermediate class is not yet this h. Then construct v^3=h, impose
the scalar/involution compatibility, and obtain the reflection
quotient before lifting and recognizing the arithmetic cubic.

Read `cm-frame-cover-class-arithmetic.md`. Section/point data are
`cm_frame_cover_sections.{json,m}`; evaluation matrices and branch
spaces are `cm_frame_cover_makdisi.{json,m,gp}`; the third is
`candidate_rows` in `cm_frame_cover_third.json`. Runner 174 checks,
rebuilds or collects `cm_frame_cover_check.json`. Routine rechecks
have separate filenames to preserve the discovery provenance.
Magma has 180 s/2 GB bounds; the GP probe has 180 s/2 GB stack.
Sections/points take 154.552 s, matrix construction 3.904 s, and
saved-data checks about three seconds. An initial matrix-constructor
API error is archived and corrected. All jobs finish or are reaped.

D68–D77 arithmetic artifacts and hashes are preserved. The arithmetic
Shimura/marking/half identification, hyperellipticity conflict, cubic,
genus-64 curve, target torsion and field polynomial remain open.
DECISIONS, REFERENCES and entry points are current. Local uncommitted
work only; no remote jobs, external edits/messages, commits or cleanup.

**D79 (2026-09-21). Recover the Kummer function, descend its representative
and construct the genus-64 cubic modulo 31.** The user asks to continue.
The finite-field equation is now Q4*T^3-3*A4*Q4*T-P10=0 over the
candidate C, with T of weight two. Its smooth projective normalization
has genus 64; its S3 closure has genus 136 and quadratic resolvent X.
The intended arithmetic monodromy and characteristic-zero model are
not yet identified.

*Decision:* extend D78's exact evaluation model to 1,024 points and
L(4D0), rather than return to the timed-out native function-field
reduction. Since 1024>8*120, evaluation certifies every identity through
L(8D0). Preserve the original 640 points, bases and verified third.

The old class A descends, but its effective representative E need not.
Choose q over F31 with div(q)=D-+Q-D0, nonvanishing on D+, and let
B=D++Q. A Frobenius-fixed section in L(4D0-E-sigma(E)-B) supplies
an effective E_R over F31 with [E_R-D0]=-2A-Delta=A. Saved row-reduced
coordinates lie in F31; exact rank checks give the needed disjointness,
and class equality with the original third is checked directly.

Script 176 obtains u with div(u)=3E_R+B-4D0 and f with
div(f)=E_R+tau(E_R)-2D0, tau(f)=f. It verifies
u*tau(u)=27*f^3*q*tau(q). Thus h=27*u/q and a=27*f satisfy
h*tau(h)=a^3. The extension v^3=h admits the involution v->a/v,
and y=v+a/v satisfies y^3-3*a*y-(h+tau(h))=0. Branch valuations
prove geometric connectedness and S3; tame inertia gives genus 64.
The three invariant coefficient arrays have lengths 105,105,285.
This equation specifies a function field; its raw denominator-cleared
special fibres are not automatically normalized.

Verifier 178 uses a different seed, reconstructs the saved spaces,
checks all generators of the final divisor inclusions, the norm and
the cubic coefficients. No third or function search is repeated.
Controls changing the norm scalar and one trace coefficient are both
rejected. The constructor takes 5.762 s, verifier 6.397 s and controls
4.554/6.321 s, under 180 s/2 GB. Corrected Magma dependent-comprehension
and heterogeneous-matrix sequence failures are archived with immutable
source snapshots. All jobs finish.

*Next decision:* compare the normalized cubic's first Frobenius
fingerprint with the predicted genus-16 old plus 48-dimensional new
Hecke factor before investing in a 31-adic lift. A mismatch would
require revisiting the choice of third/cover. Agreement alone would
not identify the prescribed Fuchsian S3 monodromy. A subsequent lift
must retain the marked cover, norm identity and normalization choices.

Data: `cm_frame_cubic.{json,m}`; combined certificate:
`cm_frame_cubic_check.json`; runner 179 checks/rebuilds/collects.
Read `cm-frame-cubic-cover.md`. DECISIONS, REFERENCES and entry points
are current. D68–D78 arithmetic artifacts and hashes remain unchanged.
The base/marking/half identification, hyperellipticity conflict,
characteristic-zero cubic, target torsion and final field remain open.
Backend optimization stays paused. Local uncommitted work only; no
remote jobs, external edits/messages, commits or cleanup.

**D80 (2026-09-22). Check two Frobenius traces of the explicit genus-64
cubic before lifting.** The user asks to continue. The normalized
cubic has 68 points over F31 and 2818 over F31^2, exactly matching
the saved genus-16 old plus 48-dimensional new Hecke prediction.
The measured power traces are -36,-1856; det(1-T*Frob) begins
1+36T+1576T^2. This is not a full Euler factor or arithmetic identification.

*Decision:* count the normalized curve through its cover, with local
series at exceptional fibres. Do not count roots of a denominator-cleared
equation where it is singular. Script 180 enumerates 50/1400 base
points through the degree-30 map, including infinity and using Frobenius
orbits over F31^2. At unit denominator and discriminant it counts simple
cubic roots. Elsewhere exact jets through degree 31 determine quadratic
splitting and the Kummer leading-unit cube class. The P32 transposition
fibre has two rational points; no other B2 or B3 points occur over
these fields. Six/twelve exceptional fibres are resolved.

Verifier 182 checks each saved fibre by quadratic/Kummer splitting
without using the cubic coefficients for the count. Distinctness,
membership and D69's exact base counts certify the point lists are
complete. Its local calculations choose different projective anchors,
quadric rows, parameters and precision, and check all curve equations.
All fibres agree. Changing one saved count by one modulo four fails.
The point-count distributions for 0/1/2/3 points are [9,27,1,13] and
[219,362,1,818]. The Hecke bank from script 58 is unchanged.

Both enumeration jobs fit 180 s/2 GB, taking 6.282/87.304 s. Independent
checks take 1.069/6.727 s and the corruption control 1.119 s. Corrected
Magma loop-variable scope and conditional-load syntax failures are
archived with immutable source snapshots. All jobs are finished.
Data: `cm_frame_cubic_point_counts.json`; combined certificate:
`cm_frame_cubic_point_check.json`; runner 183 checks/rebuilds/collects.
Read `cm-frame-cubic-frobenius.md`.

*Next decision:* the two successful comparisons support continuing with
this candidate. Start a bounded first lift modulo 31^2 of the marked
cubic class and function identities, fixing matrix pivots and section
normalizations before higher precision. Keep Frobenius descent, branch
orientation and norm compatibility explicit. The counts do not select
a unique third or match the prescribed Fuchsian monodromy. The base/
marking/half identification, hyperellipticity conflict, characteristic-zero
cubic, target torsion and final field remain open. D68–D79 arithmetic
artifacts and hashes are preserved; backend optimization stays paused.
DECISIONS, REFERENCES and entry points are current. Local uncommitted
work only; no remote jobs, external edits/messages, commits or cleanup.

*D80 lift preparation:* the verified annihilator N=3c+1 of Delta
gives a concrete first-lift scalar c2=31c+10=
1724977996777724256036049034652055939. On the good-reduction Jacobian
modulo 31^2, N*Delta2 lies in the reduction kernel, which is killed
by 31. Thus 3*c2*Delta2+Delta2=0, and c2-c=10N preserves the saved
reduction. This uses a verified annihilator of one class, not a class
number. The formula is proved in the D80 report; lifted matrices have
not yet been computed. Build actual lifted section spaces with unit
pivots before applying the 121-bit scalar and checking the relation.

**D81 (2026-09-22). Execute and verify the first genuine cubic lift
modulo 961, preserving its saved reduction.** The user accepts the
D80 plan. The genus-64 equation, branch-class third and function
witnesses now lift modulo 31^2. Every cubic coefficient reduces to
D79's value; the norm scalar is 58, reducing to 27. Independent checks
pass, and changes confined to the new digit are rejected.

*Decision:* lift actual support points and complete section spaces
before class arithmetic. Entrywise lifts of the old matrices would
not represent divisors. Script 184 lifts E_Q/U of degrees 18/21,
the 36 odd sections with fixed unit pivots, 1,024 evaluation points,
111 auxiliary entries and the B3 values. Use matrix pairs over Z/961
for the unramified quadratic coefficient ring, with native-ring
comparisons and explicit Frobenius b->-29-b. This is local arithmetic
for the cover construction; upstream backend optimization stays paused.

Scripts 189/190 execute c2=31*c+10 using 161 add-flip operations in
five bounded checkpoint jobs. The verified annihilator of Delta
justifies the scalar; direct checks establish 3A2=-Delta2 and both
symmetries. No Jacobian/Prym order is assumed. Script 191 lifts q
and chooses a moving section whose residual E_R reduces to D79's
representative, preserving all old function and equation coefficients
modulo 31. Full divisor inclusions and the identity
u*tau(u)=58*f^3*q*tau(q) certify the function and reflection equation.

Verifier 193 reconstructs the saved geometry and checks the third,
representative, functions and coefficients with a different seed,
without repeating their search. Adding 31 to the norm scalar or one
trace coefficient fails at the required identities. Every Magma job
fits 180 s/2 GB; the largest scalar chunk takes 56.343 s, function
construction 24.635 s, and independent verification 32.960 s. Four
corrected API/data failures have immutable archives. All jobs finish.

Data: `cm_frame_cubic_lift_sections.{json,m}`,
`cm_frame_cubic_lift_third.{json,m}`, `cm_frame_cubic_lift.{json,m}`.
Combined certificate: `cm_frame_cubic_lift_check.json`; runner 194
checks/rebuilds/collects. Read `cm-frame-cubic-lift.md`.

*Next decision:* before increasing precision, fix the effective
representative by persistent algebraic conditions. Matching its old
reduction leaves 80 projective linear-system parameters. The proposed
next implementation pins 80 row-reduced coefficient coordinates after
certifying a unit derivative minor. This prevents changing class-chain
representatives from changing the recognition gauge arbitrarily.
Then extend to 31^4/31^8 and validate any reconstruction at unused
precision. An intrinsic gauge is not yet implemented, and no
characteristic-zero cubic has been reconstructed.

The arithmetic identification, prescribed Fuchsian monodromy,
hyperellipticity conflict, target torsion and final field remain open.
D68–D80 arithmetic artifacts and hashes are preserved. DECISIONS,
REFERENCES and entry points are current. Local uncommitted work only;
no remote jobs, external edits/messages, commits or cleanup.

**D82 (2026-09-22). Complete the persistent normalization, lift through
31^32, and separate the class-coordinate choice from the final equation.**
The user asks to continue beyond individual checkpoints. The internal
class model now has compatible, independently checked 80P-normalized
cubics through 32 digits. The effective divisor E=80P+E40 is uniquely
selected by a rank-80 jet map on 81 sections. Its leading terms normalize
without extracting roots, giving ell*T^3-3*A4*ell*T-R7=0. Explicit
function identities identify its special fibre with D79, preserving
D80's counts 68/2818. Scripts 217–245 contain the constructions, saved-
data checks, highest-digit controls, exact route comparisons and audits.

*Algorithm decision:* lift an actual effective divisor via a rank-120
idempotent in its degree-240 section zero algebra (208–213). First test
correction of 3A'+Delta by a short scalar in the formal reduction kernel;
this agrees with the full annihilator route at 4/8 digits. Then replace
the scalar by linear interpolation in the unique pointed chart:
B=−2A'−Delta and C_new=(2*C(A')+C(B))/3. A precision doubling has a
square-zero error ideal, so this divides the class error by 3. Scripts
230/231 independently prove the averaged matrix is an actual divisor
and satisfies the class relation. At 8/16 digits it equals the saved
pointed divisor exactly. At 16 digits direct function recovery gives
the same entire coefficient arrays as the scalar route, in 118.179 s
instead of 176.869 s. The 32-digit direct constructor takes 129.098 s.
No Jacobian order is assumed. Every Magma job retains 180 s/2 GB limits.

*Rejected recognition gauge:* the initial 80-RREF-entry gauge has a
complete 31^4 certificate, but its 31^8 function job times out and local
étaleness alone does not preserve a global coefficient field. Preserve
this experiment and its diagnostics. The unique pointed chart resolves
that problem, but forcing 80 zeros at one point can inflate output
heights. Individual Q/F recognition of its coefficients, projective
ratios and local invariants gives no candidates at 8/16/32 digits.
A 128-digit lattice attempt to recover H0(4K-80P32), validated with
another 128 digits, also gives no surviving basis-row candidate. These
are bounded-search outcomes, not field or height exclusions.

*Output normalization decision:* retain 80P for class arithmetic, and
choose E=K_X+2P+E40 for the final equation. The fixed degree-80 divisor is
pi*div(X16)+R_ram+2P. Its vanishing space in L(2D0) has dimension 121;
a unique intersection with the complementary-divisor space selects E
by linear algebra. Now a and h have orders 6 and 9 at P. With the
existing branch constant r=sqrt(-3), lambda=r*a0/h0 makes their leading
coefficients 3 and 3r. This is compatible with orientation conjugation.
The final equation drops to **ell*T^3-3*A2*ell*T-R4=0, weight(T)=1**.
Scripts 249–253 construct compatible models through 31^32. Independent
checks and corruption controls pass at both the special fibre and
32 digits. Scripts 256/257 prove an explicit
isomorphism to the old pointed cover, so both matching counts remain.

*Recognition decision:* A2 lies in H0(2K-D17-3P32), dimension 25.
Scripts 254/255 construct this space exactly over Q, saturate and reduce
its integer lattice, verify its row space and a unit minor at 31. Its
largest basis coefficient is only 5430. Script 258 checks the full
coordinate conversion and leading term. Individual recognition still
finds no candidate at 8/16/32 digits. Script 259 therefore tests joint
projective F-recognition with a common F-valued scale, using 24 digits
and reserving eight. Known F-valued controls pass and corrupted unused
digits are rejected; all eight embeddings give no surviving target candidate, and the
per-embedding outcomes are saved separately.
An observed failure does not exclude definition over F or select a
higher-degree coefficient field. Any candidate still needs an exact
curve certificate.

The final equation package is `cm_frame_cubic_adjoint_package_32.json`;
the combined audit is `cm_frame_cubic_adjoint_audit_32.json`. Next test
64 digits with the same small output basis and joint recognition, using
new orchestration where existing hash-bound CLIs stop at 32. Any proposed
number-field equation must pass exact function/divisor checks.
See `dembele/certificates/cm-frame-cubic-precision.md` for formulas,
roots, timings and final outcomes. D68–D81 arithmetic inputs remain
unchanged. No characteristic-zero cubic, arithmetic identification,
target torsion or field polynomial has been certified. The prescribed
Fuchsian monodromy and hyperellipticity conflict remain open.

**D83 (2026-09-22). Test 64 digits in the smaller output normalization.**
The user asks to continue. Double the verified D82 lift, retaining the
linear class correction and K_X+2P output normalization. Use the exact
25-dimensional rational space for A2 and joint projective F recognition
with 48 training digits and 16 unused validation digits. Any apparent
candidate must still pass exact function/divisor identities.
Runner 261 extends orchestration through separate generated copies of
the precision-restricted wrappers; D82 sources and certificate hashes
remain unchanged. Each successful stage has a provenance receipt.
Keep the 180-second/2 GB Magma limits and split longer jobs if needed.
The combined class check and combined pointed function recovery both
hit that limit. Preserve both failed jobs. Script 264 separates the
tripling relation (160.456 s) from the symmetries (47.652 s); both pass.
Runner 265 binds this certificate by exact equality with the divisor
matrix, then checks the full geometry and function identities.
Runner 266 searches for u directly in WB4, rather than first finding a
larger quotient inside RG4, and separates u recovery from f and the norm.
The complete RG2 inclusion and independent WB4 membership check retain
the original divisor certificate. Coefficient fitting then preserves
every verified 32-digit coefficient. Runners 267–269 apply the same
bounded stages to the smaller output model. Its divisor move depends
only on the certified class, so it can run alongside verification of
the internal pointed equation. Both internal and smaller models now pass
independent verification and highest-digit norm/trace controls through
31^64. The compact package is `cm_frame_cubic_adjoint_package_64.json`;
the final audit verifies 1329 file hashes across 493 JSON records.

Both joint recognition runs, 48/16 and 60/4 training/validation digits,
are negative in all eight embeddings. The tested target rows fail at
the first unused digit; known F controls and corrupted-digit controls
pass. Script 271 gives a separate complete low-height exclusion using
K=31^60*B^-1 and B*K=31^60*I. Script 263 rechecks every integer product
and bound without Sage. Uniformly over embeddings, integral homogeneous
representatives of the A2 point in the specified 25-by-8 bases cannot
have height <=1,301,123. This does not exclude F or identify the chosen
third arithmetically.

The optional Gram-Schmidt diagnostic 270 exceeded its intended bound:
the old Sage runner killed its launcher but left the Python child alive.
The audit detected late log output. Preserve the late files separately,
restore the original empty timeout log to its recorded hash, and exclude
the late result. Scripts 272/273 implement and test process-group timeout
termination, including a real Sage child that tries to write later.
Use runner 274 for future Sage recognition and immutable result reuse.

Next test 128 digits with the same smaller model and exact A2 basis,
using 112 training digits and 16 unused validation digits. Add new
bounded orchestration; do not edit hash-bound 64-digit sources or
increase the 180-second Magma limit. Larger inverse computations may
need precision-aware arithmetic. Any number-field candidate still
requires exact curve identities before target torsion work.
See `dembele/certificates/cm-frame-cubic-64.md` for current outcomes.

**D84 (2026-09-22). Pause doubling to test the choice of cover and calibrate
recognition.** The user approves these two investigations after the
strategic stocktake. Preserve the existing 64-digit construction and test
whether the selected third is distinguished among concrete alternatives,
and how much synthetic recovery improves at higher precision.

Scripts 276/277 find two independent rational, tau-anti-invariant classes
of order three. The Hecke-suggested cofactor is only a search aid: direct
class operations check every order and symmetry. Verifier 278 independently
certifies their (Z/3)^2 subgroup, nine distinct thirds and the relation
3A=-Delta for all nine. Adding Delta to a torsion point is rejected. One
random-support search (seed 1) fails before class arithmetic because its
support does not reach degree 120; preserve that failed job and log.

Runner 279 specializes frozen D79/D80 scripts at the alternative inputs,
retaining source hashes and generated copies. It reuses the certified
complete base point lists, independently checks all nine genus-64 covers,
and counts every normalized fibre by two methods over both fields. The
current third alone gives the expected 68/2818. The other eight give
59/1495, 50/1540, 59/1543, 44/1504, 38/1474, 59/1525, 38/1456 and
53/1567. This distinguishes the current choice in the tested subgroup;
neither completeness of the subgroup nor the prescribed global monodromy
has been proved. The missing comparison is between divisor classes on
the explicit X and the cycle marking of the quaternionic presentation.

Script 275 tests 67 synthetic exact F-points with the same rank-200 joint
recognition lattice as 259. Three seeds at root 4 all recover height 10^7
and fail 10^8 with 48/16 digits; recover 10^9 and fail 10^10 with 60/4;
recover 10^18 and fail 10^19 with 112/16. Root-20 boundary checks agree
for the latter two splits. All survivors are checked against unused digits
and the exact known projective point; corrupted unused digits are rejected.
Script 280 independently verifies the 34 positive cases with plain Python
integer arithmetic. These empirical example heights do not bound the target
or give a uniform recovery guarantee. All 128-digit data here is synthetic.

*Recommendation after the checks:* retain the selected third and attempt
one bounded actual 128-digit reconstruction with the same K_X+2P model,
exact A2 basis and 112/16 split. The finite-field comparison now supports
this choice against eight actual alternatives, while calibration shows
substantial useful extra precision. If recognition is negative again,
revisit coefficient-field/descent and identification assumptions before
another doubling. No height upper bound promises success. Any recognized
equation still needs exact function/divisor identities before torsion.

The authorized structural/calibration checkpoint is complete; no actual
128-digit lift has run. Script 281 binds 1666 file hashes / 593 JSON
records in `cm_frame_structural_checkpoint.json`, including unchanged
D83/D78 certificates. All jobs finish within their limits; no active jobs,
remote work, external messages, commits or cleanup. Read
`dembele/certificates/cm-frame-structural-checkpoint.md`. The arithmetic
identification, hyperellipticity conflict and target field remain open.

**D85 (2026-09-22). Try 128 within the resource bounds, then complete the
coefficient-field/descent review.** The user explicitly authorizes this
sequence. Runner 282 extends the frozen workflow without changing earlier
sources. Sections/evaluation points and pointed local expansions pass
at 128 digits in 94.609/105.349 seconds. The actual-divisor constructor
hits 2 GB after 65.268 seconds. Precision-aware inverses in 283 already
pass native-ring controls and highest-digit inverse corruption checks.
Releasing unused model data and using pointwise scaling (285/286, runner
287) also reaches the memory cap, after 73.358 seconds. Corrected blocked
multiplication (293/294, runner 291) passes native controls 295 but the
divisor job times out at 180 seconds. Preserve all three failed attempts,
their executed source snapshots and logs. The initial block-control
289/292 failed at a heterogeneous matrix-sequence conversion; retain it
as a failed control, superseded by 295.

Stop this precision branch at the resource checkpoint and proceed with
the requested review. **No actual divisor or cubic at 128 was completed,
and no 112/16 recognition test ran. The verified cubic remains at 31^64.**
This is not a negative recognition result or evidence excluding F.
Do not increase the limits or start 256 digits. Successful sections/jets
remain reusable if a later divisor algorithm supplies a checked split.

The review derives the geometric ambiguity: J_X[3] has dimension 80,
its invariant part is the pullback of J_C[3] of dimension 32, and the
compatible third torsor therefore has 3^48 geometric members. This does
not give the degree of the selected coefficient field. D84's nine local
solutions and two point counts do not determine its global Galois orbit.
Script 296 checks that x^2−5 has a simple root lifted through 31^128
although it has no root in F, illustrating the missing local-to-global
implication. This is not a proposed larger coefficient field.

Retain K_X+2P normalization: its unique linear spaces and final scale
lambda=sqrt(-3)*a0/h0 do not add a new root choice. A sufficient missing
global condition is sigma(A)=epsilon_sigma*A, where
epsilon_sigma=sigma(sqrt(-3))/sqrt(-3), for sigma fixing F. The norm and
trace would then be fixed. Local Frobenius checks do not prove this.
The field-preserving argument supplies no coefficient-height bound.

For the S3 cubic, Aut_C(Y)=N_S3(C2)/C2=1; 296 checks the finite group
calculation. Thus, once conjugates are known to be isomorphic over the
fixed base, uniqueness supplies the descent cocycle. Sijsling–Voight's
marked descent theorem does not itself establish that field of moduli.
The local level's intrinsic kernel and conjugate reflections suggest
extending D58's canonical-conjugation argument, but level/component
compatibility and identification with the explicit candidate remain
unproved. No Q-descent of the cubic is asserted. The earlier published
hyperellipticity conflict remains part of the identification audit.

**Next deliverable:** a marked arithmetic comparison between the explicit
base/cover/class and the canonical quaternionic cover. First determine
what the saved analytic data can certify about the base and branch
marking and what additional certified comparison is required. A direct
proof of the class's global Galois action would be an alternative.
Do not substitute automatic precision growth, arbitrary larger-field
searches, or target torsion for this comparison.

Report: `dembele/certificates/cm-frame-cubic-128-review.md`. Root:
`cm_frame_cubic_128_attempt_review.json`; verifier 297 checks 1744 file
hashes / 612 linked JSON records, including unchanged D84/D83/D78 roots.
The computational attempt and requested review are complete; the full
128-digit lift, arithmetic identification and target field are not.
All jobs finished. Decisions/references/entry points are current.

**D86 (2026-09-22–23). Complete the 128-digit lift on Châtelet;
stop precision escalation after negative reconstruction.** The user
requests remote execution and explicitly authorizes the mathematical
inputs for this run. That resolves the earlier two automatic-review
upload rejections; the authorization persists across this run's stages.
The first twelve-file manifest totals 12,626,184 bytes. Credentials
and unrelated files are excluded. A resource probe reports 24 CPUs
and about 108 GB available RAM.

*Decision:* reuse the successful D85 sections/jets and original
precision-aware kernel 283, with isolated single-threaded 8 GB /
1800-second remote jobs. This changes the execution budget while
preserving the mathematical method and earlier failed attempts.
Scripts 298–300 implement hashed incremental transfers, durable
bounded workers, process-group timeout termination and fetched logs.
Script 302 schedules the unchanged independent checkers in two lanes.

*Outcome:* all 21 remote jobs complete in their intended roles. The
actual divisor, corrected class, tripling relation and symmetries
pass. Both the internal pointed cubic and smaller K_X+2P model are
independently verified through 31^128, with coefficientwise reduction
to 64 digits. All four highest-digit norm/trace corruptions are rejected
at their intended assertions. The longest job takes 299.709 seconds;
maximum RSS is 2,250,620,928 bytes. The remote run clears the earlier
local time/memory obstruction.

Transient socket/TLS failures and a connection reset interrupt some
input uploads. Completed mathematical jobs remain immutable. Adapters
304/305 add at most six attempts with bounded backoff for idempotent
transfer/status operations; they do not retry detached launches.
Interrupted transfers, retry events and successful resumption are
recorded. A fresh remote inspection verifies that all 21 jobs have
finished and their statuses match the saved local records.

The actual 128-digit coefficients undergo joint projective F recognition
with 112 training / 16 validation digits in all eight embeddings.
**No candidate survives.** Known-F points are recovered and first-unused-
digit errors rejected at every root. The coefficientwise 64/64 pilot
also has no surviving Q/F candidate in its stated scope. These local
Sage jobs use 274's process-group runner and finish within 180 seconds.

Scripts 301/303 give exact inverse-matrix height certificates. An
independent plain-integer check of B*K=31^112*I excludes integral
homogeneous coordinate height through **348,750,355,384,078**, uniformly
in the fixed 25-coordinate and degree-eight power bases, including
arbitrary common F-valued scaling. This is not a proof that F is the
wrong field, nor a coordinate-independent height bound.

*Next decision:* retain the K_X+2P normalization and pause precision
escalation. Pursue the D85 marked arithmetic comparison/global class
action, starting with what the saved analytic data certifies about the
base and branch marking. The class's global twist and the published
hyperellipticity conflict remain open. No automatic 256-digit run,
arbitrary larger-field search, or target torsion computation follows.
The exact number-field cubic and target field polynomial are unconstructed.

Report: `dembele/certificates/cm-frame-cubic-128-chatelet.md`. Package:
`cm_frame_cubic_adjoint_package_128.json`. Root:
`cm_frame_cubic_adjoint_audit_128.json`; 303 verifies **2009 file hashes /
769 JSON records**, including unchanged D85/D84/D83/D78 provenance.
D85's no-result assertions are historical; its bound files remain intact.
All remote and local jobs are finished. Decisions, references and entry
points are updated.

**D87 (2026-09-23). Compare the double-cover character before further
precision work; retain the geometric cover candidate.** The D86
reconstruction is negative, so continue the marked comparison with a
test that can distinguish covers sharing the same branch divisor.
For the genus-16 base, those geometric double-cover choices form a
torsor under `Jac(C)[2]`, of size `2^32`.

*Decision:* pull the exact rational function `n/d` back through the saved
CM frames and differential banks, continue its square root, and compare
the character with the exact signs of script 66's S3 images. No new
differential system or 31-adic precision increase is needed.

*Outcome:* all **277** saved side generators match in both banks and
along an alternative path family in the current bank. Maximum sign
errors are below 7.86e-14 / 2.00e-8 / 7.86e-14. Three campaigns retain
192,405 samples. Script 318 independently reconstructs the branches by
argument accumulation; winding controls pass and a reversed stored
branch is rejected. The trivial character disagrees on 133 generators.

The midpoint pilot met an elliptic fixed point where the differential
coordinates vanish; its full-polynomial comparison was rejected and
preserved. Perturbed side points pass direct-substitution checks in
both banks. Two apparent sign mismatches in a uniform 128-step pilot
disappear on refinement. Adaptive continuation uses local changes and
logarithmic derivatives, then repeats with half the tolerance. The
derivative estimates are not interval bounds. Finite-polynomial tail
skipping is ball-bounded; the infinite differential tail is not.

This supports the geometric double-cover choice without proving the
analytic or arithmetic identification. Retain it. Re-reading D77
also confirms that its exact B3 fibre/inertia argument already selects
the unique F-scalar twist within this fixed half; the -3 twist is
excluded there. A certified marked base/geometric comparison would let
that existing constraint settle the arithmetic double cover. Do not
restart an unrestricted scalar-twist search.

*Next:* focus on the marked arithmetic base identification and the
selected cubic class/global Galois action. The geometric third torsor
and published hyperellipticity conflict remain unresolved. Keep precision
paused; no automatic 256-digit run, arbitrary larger-field search or
target torsion follows. No exact number-field cubic or field polynomial
has been constructed.

Report: `dembele/certificates/cm-frame-double-cover-character.md`. Root:
`cm_frame_double_cover_character_d87.json`; 318 `--check` verifies
**2,187 file hashes / 875 JSON records**, including unchanged D86.
All 52 job records are preserved: 51 successful and one rejected
midpoint check, longest 118.136 seconds within a 180-second bound.
All jobs are finished. Audit 303 was rerun and passes. Decisions,
references and entry points are current; bound sources remain frozen.

**D88 (2026-09-23). Independently review the CM-expansion route and the
proposed cubic uniqueness shortcut.** The user requested one agent for
each question. Their reports are
`dembele/certificates/d88-cm-expansion-identification-review.md` and
`dembele/certificates/d88-cubic-identification-shortcut-review.md`.

*Base review:* the nonrational-point expansion paper supplies a precise
certificate once exact arithmetic expansions are available. In the
matching arithmetic canonical frame, order-four vanishing at the
degree-17 point kills every candidate quadratic section: 68 > 60.
An exact rank refinement reduces the target to three coefficients:
rank 45 of the 51-by-136 quadratic-product jet matrix forces its kernel
to be the true quadratic ideal and rules out hyperellipticity. The new
candidate-side diagnostic verifies ranks 17/34/45 modulo 31; good
specialization proves the third rank over Q. Its independent Python
replay reconstructs the matrix, checks all quadrics, preserves rank under
nonlinear reparametrization and rejects an altered highest coefficient.
The successful Magma job takes 0.347 seconds under 180-second / 2 GB
bounds; the failed first matrix-layout attempt is preserved. Recheck
with `python3 dembele/pari/d88_candidate_cm_jet_rank_check.py --check`.
The canonical map then has degree one onto the smooth degree-30
candidate, so nonhyperellipticity need not be assumed in this argument.
Projective ratios in a ratio-defined parameter remove the common period.
The saved CM frame provides values, not independent arithmetic jets;
neither this paper nor the other reviewed evaluation sources supplies a
ready exact restriction map for our quaternion algebra over F. Computing
more candidate jets would not establish that comparison. P32 and B3
markings remain separate obligations.

*Shortcut review:* retain it as a conditional theorem. Once the marked
arithmetic C and X are identified, the canonical Prym order has v3=2.
Anti-invariant rational 3-torsion equals Prym rational 3-torsion, so the
two independent D84 points make its nine choices exhaustive. The count
68 already singles out the current choice; 2818 is an additional check.
Global irreducibility of D+ and D- over F(sqrt(-3)) forces constant
inertia exponents on each and opposite signs, up to simultaneous inversion.
The norm identity removes constant Kummer twists. On the fixed smooth
marked model, reduction is injective on 3-torsion, hence a shared
reduction identifies the two algebraic thirds. This does not contradict
D85's counterexample to inferring a field of definition from a local
lift alone: the new argument uses an independently specified global
canonical cover. The saved Hecke place is beta=27 modulo 31.

*Decision:* concentrate the next research step on an independently
computable projective tangent at the labelled CM point, including an
explicit arithmetic evaluation theorem and model. Its feasibility is
not established; this review must not be represented as an implemented
exact-jet algorithm. Preserve the need to certify D87's geometric cover
comparison and resolve the published hyperellipticity conflict. Further
precision escalation remains paused. D86/D87 certificates are unchanged;
no exact number-field cubic or target field polynomial is obtained.

**D89 (2026-09-23). Test whether ordinary CM deformation and the saved
Hecke data make the independent tangent computable.** The user asked
to work on D88's next step. New exact local calculations are in
`dembele/pari/319_cm_tangent_local_arithmetic.py` and
`cm_tangent_local_arithmetic_d89.json`; the report is
`dembele/certificates/cm-tangent-local-arithmetic-d89.md`.

At b=27 modulo 31, beta^2=-2-b has roots 8 and 23. The tame
order-two quotient requires differential terms z,z^3 for a coarse
projective tangent and z,z^3,z^5 for the three-term comparison. In a
split Serre–Tate chart, z=(q-1)/(q+1) is odd and u=z^2 is the coarse
parameter, which vanishes on first-order upstairs deformations. Exact
formal identities and local-section controls pass. This does not
construct the arithmetic moduli test object or its section restrictions.

Enumerating P1(F31) gives two horizontal and thirty conductor-l Hecke
neighbors. The elliptic involution fixes the first two and pairs the
others. The fifteen paired coarse branches each have multiplicity two;
their differential trace extracts odd coefficients. In particular an
unknown cubic term at a descending point contributes to the desired
tangent. Therefore a Hecke equation restricted to the known seventeen
CM points omits necessary terms. This rules out that closed-system
proposal, not every possible Hecke-based evaluation method.

*Outcome:* no independent arithmetic tangent is computed. The missing
input is a global section evaluator. The source review did not find a
ready exact construction for this real-octic datum. Nelson's explicit
analytic formula would need a totally real adaptation; the investigated
CM and theta-correspondence results do not by themselves supply the
canonical section map. Retain the D88 criterion and conditional cubic
argument, but do not describe a formal parameter as an implemented jet
algorithm. Further precision remains paused. Script 319 `--check`
passes; no candidate curve input, remote job or new large solve is used.
Earlier bound sources and artifacts remain unchanged.

**D90 (2026-09-23). Implement the local pieces of Nelson's Shimizu
method for the real-octic datum.** The user approved pursuing the paper.
Instead of another source-only feasibility review, implement components
on the actual saved quaternion order. Report:
`dembele/certificates/nelson-totally-real-kernel-d90.md`; scripts 320--326.

*Normalization:* use the totally positive different generator
`delta=16/(2+b)`, of norm `2^31`. Scaling the global additive character
at finite and real places reduces the dual quotient from the absolute
index `2^126` to order 4. Its Fourier denominator is 2 and normalized
Gauss sum is -1, checked exactly. At infinity use one split polynomial
Gaussian and seven compact Gaussian factors. Derivative and disk
conversion checks cover orders through five. At an order-two CM point,
ordinary value anchoring vanishes; the useful pairs are `(1,1),(3,1),
(5,1)`.

*Enumeration:* the CM splitting has two rank-16 integral pieces with
direct-sum index `2^16`; preserve its 65,536 matching cosets. The first
majorant shell lies entirely in K, so extend the bounded pilot once to
see the mixed terms required by higher derivatives. This gives 9,910
vectors, of which 9,360 are mixed and outside the direct sum. An exact
rational majorant is proved within 1% of the natural majorant at every
real place. Dropping the cosets would already lose those finite terms.

*Analytic prototype:* implement the scalar Mellin integral with Gamma
product `Gamma(s)^8 Gamma(s+1)^7 Gamma(s+k)`. Its degree-one version
matches the independent Bessel identity beyond 40 digits; six degree-
eight shifts agree under a contour change. These are numerical checks,
not interval tail bounds or a proved global Hilbert formula.

*Outcome and next:* no Hecke-weighted quaternion sum, global lift or
Shimura tangent is computed. Finish the Hilbert cusp/unit unfolding,
norm-ideal coefficient indexing and global measure/argument factors;
then evaluate one form from the first quartic level-p2-new orbit, with
a truncation bound. This is the correct C-form module, distinct from
the level-one target representation. Exact arithmetic jets and D88's
identification criterion remain subsequent tasks.

Script 326 `--check` independently validates the finite and lattice
data, all 9,910 shell vectors, eight rational interval proofs and 27
hashes. All six jobs are complete: three passes and three preserved
development failures, maximum 9.645 seconds under 180-second bounds.
No remote work or precision escalation occurred; earlier bound
certificates remain unchanged. Decisions, references and entry points
are updated. The target field remains unconstructed.

**D91 (2026-09-23). Assemble the Hilbert cusp/unit sum and certify a
primitive-subset evaluation; expose the remaining enumeration cost.**
The user said “go for it” after D90. Report:
`dembele/certificates/nelson-hilbert-unfolding-d91.md`.

*Cusp and unit simplification:* prove `O#=beta^(-1)O` on the saved exact
basis. For the odd derivative pairs, the dual cusp is the same order
with A divided by 2 and unchanged phase. Remove central-unit duplicates:
130 small-norm signed-pair representatives become 34 classes, with 96
exact duplicate witnesses. Removing beta powers gives 29 primitive
classes. Sum every beta power by a geometric factor; retain every
auxiliary ideal through `zeta_F(2s)`.

*Do not invent Hecke inputs:* the primitive subset requires coefficients
at b=10/20/21 mod31, while the saved quartic T31 polynomials are at b=27.
Keep those three coefficients as variables. Script 60 records both a
conjugate-prime InternalNeighbors assertion and a 307.8-second T31 build;
do not present an unmodified rebuild as a bounded next action.

*Numerical result:* 42 Arb kernel enclosures yield the `(1,1),(3,1),(5,1)`
partial sums as four affine Hecke buckets. Both strip discretization
and vertical tails are bounded. Maximum scalar quadrature error is
6.55e-44; bucket component radii are below 1e-47. These are bounds on the
specified partial expression, not on a complete form or tangent. The
global nonzero Shimizu test-vector identification is still outstanding.

*Normalization review:* Masri's Hilbert Eisenstein constant term fixes
the residue and argument factors. Direct rational `(1,1)` differentiation
agrees with the implemented Gaussian/Mellin kernel beyond 40 digits.
It reveals an absolute-X scale discrepancy in the literal arXiv-v1
display (11). Preserve that finding; the published display was not
accessible, and no claim about it is made. The derivative implementation
is based on independently checked Gaussian identities.

*Enumeration decision:* an explicit missing norm-two mixed class proves
the old shell is not a global cutoff. Seven independent cyclotomic units
give a complete reduction bound; LLL reduces its constant from 648536
to 2126. Even A<=359 then needs Q<=333, with ellipsoid volume about
3.22e39 (not a point count). Do not launch that search or increase
precision. Next develop complete enumeration by norm ideal and
hyperbolic displacement, beginning with the norm-one control whose
coefficient is known. Coverage and an omitted-class tail are required.

*Outcome:* a certified partial analytic evaluation, not a complete
eigenform or independent CM tangent. Script 337 `--check` validates
44 hashes, independent rational quaternion/unit checks and interval
outputs. Nine bounded jobs completed, five passes and four retained
API/coercion failures, all below 6.3 seconds. Scripts 327--337 are frozen;
D90 recheck passes. No remote job or higher cubic precision was used.
Decisions, references and handoff are updated. The exact jets, marked
arithmetic identification, cubic coefficients and target field remain
open.

**D92 (2026-09-23). Fix the norm, certify coverage, and complete the
norm-one control with an infinite-family bound.** The user asked to
continue D91's proposed enumeration step. Report:
`dembele/certificates/nelson-norm-one-control-d92.md`.

*Enumeration choice:* eight independent unit signatures prove every
totally positive unit is a square. For the unit norm ideal, normalize
reduced norm exactly to 1 and quotient only by sign. Compact-place
norms are then fixed. An anisotropic rational majorant with split
weights +/-1/(2T) covers all A<=T in a small ellipsoid. This avoids
the all-norm central-unit covering constant responsible for D91's
infeasible first bound; no larger version of that search is launched.

*Coverage choice:* PARI's fast flag 0 rejects the large matrix entries.
Preserve that attempt and use flag 2 at 256 bits, but do not promote
its floating enumeration to a rigorous completeness assertion. A
separate Arb recursion, exact rational LDL identity and exact leaf
tests reproduce every vector. The complete class counts are
13/29/137/541 at A=400/1600/6400/25600. The first cutoff exposes four
norm-one classes missed by D91. The largest coverage replay finishes
in 81.44 seconds, without rebuilding the Fuchsian polygon.

*Tail choice:* apparent stability of partial sums is insufficient.
The complete small cutoff proves orbit separation. A crude packing
count bounds the infinite tail but is too wide. Positive angular
averages over disjoint hyperbolic disks improve it, using 129 exact
binomial terms and rigorous absolute Mellin integrals. At A=25600,
the `(1,1)` partial sum is 7317.7436102796 and its omitted norm-one
tail is <1124.696. Thus 6193<S11<8443 for the full norm-one family
of the D91 expression, including auxiliary ideals and beta powers.
Positivity of this subsum does not prove the full lift is nonzero.
Higher derivative bounds are still too wide for projective jets.

*Next gate:* retain this successful norm-one control. Extend the
fixed-norm search to the norm-31 prime b=27, where Hecke polynomials
already exist, and prove a coset decomposition or valid tail bound
for that family. This is preferable to another norm-one cutoff or
an unmodified costly T31 rebuild. Other matched Hecke coefficients,
an all-ideal tail and the global test-vector identification remain
necessary before a differential evaluation can be claimed.

*Outcome:* script 343 `--check` verifies 51 hashes, independent
rational majorants and every cutoff vector/classification, unit
signatures, LDL identities, nesting, inverse pairing, disk averages
and interval containment. Twelve computational jobs are complete:
eleven passes and one preserved PARI precision failure; the root
audit generation also passes. Scripts 338--343 are frozen. No remote
run, cubic precision increase or candidate-model change occurred.
D91 and earlier certificates remain unchanged. Decisions, references
and handoff are updated; the CM tangent and target field remain open.

**D93 (2026-09-23). Complete the saved norm-31 family, then assess
all-ideal accuracy before extending the search.** The user asked to
continue D92's norm-31 step. Report:
`dembele/certificates/nelson-prime31-and-global-tail-d93.md`.

*Use the available coefficient:* normalize reduced norm to the explicit
positive generator of `(31,b-27)`, using unit squares. The complete
counts are 8/60/170/586 at A=400/1600/6400/25600. The independent
interval replay checks 11,568 signed pairs and 4,334,720 nodes at the
last cutoff in <94.44 seconds. No new T31 computation is needed.

*Prove the orbit transfer:* the exact reduction `O/nO=M2(F31)`
classifies alpha*O by a line. All 32 lines are represented, and each
of the 586 classes has an exact integral norm-one right-factor witness.
Thus the infinite family has exactly 32 norm-one orbits. Apply disk
separation within each orbit and sum; do not assume disks from distinct
orbits are disjoint. This requires no ideal-class shortcut.

*Weighted control:* use the saved first quartic and U_p2=+1. For its
smallest root -7.3140105084, the unit-plus-prime `(1,1)` partial is
7640.7581837028 with total two-family error <9626.300. The enclosure
contains zero. Small changes in the unweighted prime partial sums
are not themselves a convergence certificate.

*Global cost check:* Blasius's Ramanujan theorem bounds coefficients
by d(a)*sqrt(Norm(a)). Local Hermite forms bound the number of norm-one
orbits by sigma_1(a). A whole-orbit disk moment and an exact Euler
identity give absolute convergence of the D91 expression and a bound
on all uncomputed norm ideals. The `(1,1)` bound <2.685e16 is far too
loose for a tangent. Hypothetical complete-A bounds remain huge at the
tested cutoffs; no such all-ideal enumeration was launched. These
are weak upper bounds, not a proof of large actual error or failure
of the method. Review the global kernel/summation and nonzero
Shimizu identification before enlarging the Hecke bank or cutoff.

*Repair the certificate export:* a failed rational endpoint comparison
led to a direct Sage conversion check. `QQ(MPFR_endpoint)` may round
inward, and one old point-bound record even has lower>upper. Preserve
all original sources and artifacts; script 351 replays five analytic
stages with `.exact_rational()` and corrected dependencies. The new
`*_exact_d93.json` files supersede those analytic endpoint exports.
Coverage uses direct MPFR ceil/floor and is unaffected. The reported
bounds, including D92's norm-one positivity, are re-established.
Use the final root `nelson_prime31_exact_d93.json` and script 354,
not the intermediate 350 result alone.

*Outcome:* eight original computational jobs and five endpoint replays
passed. Three failed audit attempts and the intermediate passing audit
are preserved; the final audit independently checks exact arithmetic,
rational moments, corrected endpoint outputs and provenance. Scripts
344--354 are frozen. No remote run, candidate-model change or cubic
precision increase occurred. Decisions, references and handoff are
current; independent arithmetic jets, marked identification, cubic
recognition and the target field remain open.

**D94 (2026-09-23). Review the contour and establish local
nonvanishing before expanding the global computation.** The user asked
to continue the D93 review. Report:
`dembele/certificates/nelson-test-vector-and-contour-d94.md`.

*Contour result:* test seven contours with rigorous fractional Gamma
bounds and exact-endpoint Arb output. At c=25/16 the unchanged-kernel
omitted-ideal `(1,1)` bound is <2.680e13, versus <2.685e16 before.
This is still over three billion times the partial sum about 7641.
The best tested contour is not a proof of global optimality, and the
upper bound is not a measurement of the actual error. Additional
quadrature digits or a small cutoff increase will not address this loss.

*Weight decision:* Nelson's residue identity permits polynomial H
with the required endpoint values. Test m=0/1/2/4 in
`W_m=(2s-1)*(1-s*(s-1)/(c*(c-1)))^m`, with all 28 choices rigorously
bounded. The best changed-weight bound is <2.257e13. Nonzero m
changes each finite-family contribution; no such partial sums were
computed and none may be mixed with D93's original partials. The
modest gain does not justify changing the kernel. Keep m=0 and seek
a bounded pilot that retains more cancellation before absolute values.

*Local nonvanishing:* pair the actual Schwartz functions with the
dual matrix coefficient on the norm-one group. Finite factors are 1
when vol(O_v^1)=1. The seven definite factors and the split radial
integral are exp(-2*pi/delta_v). Since Tr(delta^-1)=1, their product
is exp(-2*pi). The dual K type is essential: the wrong conjugate
gives a zero angular average. Exact order conjugation, field trace,
root positivity and Cartan identities are checked separately from
the analytic proof. This establishes the local functional, not the
global Petersson scalar or the CM first derivative.

*Next proof step:* use Disegni section 5.1 for the number-field
framework and Watson's forward norm-fibre/adjoint argument as a guide.
Explicitly match the fixed-character classical kernel to the
similitude kernel, including the extra variable, determinant and unit
integration, dual convention and newvector. Keep global identification
false until that comparison is written. Nonzero as an automorphic
form will not alone prove nonzero at the CM derivative anchor.

*Outcome:* two computations and the final audit pass, maximum
<7.21 seconds. Script 357 replays 168 tail polynomials, checks 505
dyadic intervals, local field/order facts and 127 source hashes, and
binds the corrected D93 root and new report. Scripts 355--357 and
bound artifacts/report are frozen. No Hecke rebuild, new displacement
enumeration, remote run, candidate change or cubic precision increase
occurred. Decisions, references and handoff are current. Independent
arithmetic jets, marked identification, cubic recognition and the
target field remain open.

**D95 (2026-09-23). Finish the global comparison, and make the
derivative conjugation explicit.** The user asked to continue D94's
comparison step. Proof:
`dembele/certificates/nelson-global-identification-d95.md`.

*Global construction:* extend the fixed-character Schwartz function
in the similitude variable using positive normalized real bumps and
finite unit support. Central averaging forces positive rational u
with even finite valuations. Certified class number one and full
unit signature rank make u a square. Unfolding these squares gives
exactly the classical half-lattice sum with the stated Haar measures,
without an additional unit regulator. Local level and component checks
make Disegni's general-field Shimizu theorem applicable to this kernel.

*Nonzero scalar:* the fixed types select one tensor line, but that
alone would permit zero. The forward norm-one Fourier coefficient is
norm(v)^2*exp(-2*pi), by D94's local integral and direct unfolding.
Adjointness gives the positive classical scalar norm(f)^2/norm(v)^2.
The full implemented Mellin series is therefore the intended derivative
pairing. Direct height-power accounting also matches D91's prefactor
and argument. Numerical Petersson norms are unnecessary for ratios
and were not computed.

*Orientation correction:* rendered Nelson equation (13) and an
independent Cayley-matrix calculation fix the bars. The code's first
index is anti-holomorphic and its second index holomorphic. The sums
are unchanged, but their coefficient interpretation must use
`c_a/c_1=conjugate(S_(a,1)/S11)/a!`, a=1/3/5, when S11!=0. No prior
certified ratio or arithmetic recognition needs to be undone. The
arXiv-v1 derivative-display caveat remains; direct Gaussian identities
are still the implementation's basis.

*Boundary:* the global identification gap is closed. Numerical
accuracy is not: the <2.680e13 omitted-ideal bound is unchanged and
the selected CM first derivative may vanish. Canonical base-point
freeness guarantees some anchor among the sixteen forms, without
choosing it from the current partial sums. Analytic disk ratios also
still need an arithmetic coordinate comparison before becoming exact
CM jets. Next test completed-kernel bounds on norm/displacement blocks
in a bounded pilot, retaining more cancellation before absolute values.
Do not repeat the global comparison or automatically enlarge the
enumeration, Hecke bank or cubic precision.

*Outcome:* script 358 passes in <5.49 seconds, with certified ordinary
and narrow class numbers, signature rank 8, 1,056 exact norm conditions
and symbolic matrix/Gaussian checks. The independent audit 359 passes
in <1.45 seconds and binds 134 files, including the proof and D94 root.
Sources 358--359 and bound artifacts/report are frozen. Older pending
flags remain historical; their numerical artifacts remain valid and
unchanged. Decisions, references and handoff are updated. No remote
run or candidate-model change occurred. Exact arithmetic jets, marked
identification, cubic recognition and the target field remain open.

**D96 (2026-09-23). Complete the scalar kernel and ideal majorant,
then keep the enumeration gate closed.** The user asked to continue
D95's bounded numerical pilot. Report:
`dembele/certificates/nelson-completed-majorant-d96.md`.

*Method:* evaluate the completed scalar Mellin integrals on dyadic
displacement blocks, retaining cancellation before absolute values.
Degree-31 Taylor enclosures and Bernstein certificates prove 0<K3<K4
and decreasing K4/A through A=2^72. Stieltjes integration against the
disjoint-disk count C_N(A)<=32*A/(7*N) gives an orbital majorant in
terms of K4 plus its radial integral. Sum its entire ideal-count
majorant through D_odd(s+1/2), cancelling the scalar zeta_F(2s)
factor. This avoids a new quaternion or ideal census.

*Result:* the original-kernel omitted-ideal S11 bound improves from
2.6795251840e13 to <6.754e12, a factor >3.967. The original D93
partial sum remains 7640.7582 with its unchanged two-family tail.
The complete positive scalar comparison is about 1.47735e12, enclosed
to width <1e-40; all far-tail/splice corrections total <1.4e-6.
The remaining factor of about 884 million relative to the partial
sum is not numerical integration uncertainty.

*Decision:* this improvement is not useful enough to justify a larger
Hecke bank or displacement enumeration. Do not rerun this comparison
at more digits or infer that the actual omitted sum is large. The
next method must materially improve the positive orbital/Hecke
estimates or retain signed and angular cancellation. Test a concrete
bound on saved data with an explicit remainder before expansion.
Saved finite-family cancellation factors, about 1.064799 and 3.652448,
do not demonstrate the required gain for uncomputed large norms.
This conclusion concerns the tested comparison, not every possible
Nelson-based evaluator. The full D95 identification remains proved.

*Verification:* the two computations pass in <11.95 seconds each.
Audit 362 independently replays 6,840 rational Bernstein coefficient
signs, the Gamma-tail polynomial, final directed error bounds and
finite-family diagnostics, and binds the new proof and D95 provenance.
Sources 360--362 and bound report/artifacts are frozen. Corrected
endpoints, the 180-second process-group cap and cubic precision pause
remain. No remote run, candidate change or new Hecke/quaternion data
occurred. Decisions, references and handoff are current; exact CM jets,
marked identification, cubic recognition and the target field remain open.

**D97 (2026-09-24). Test signed orbital cancellation, and expose the
missing infinite-count estimate.** The user asked to resume from the
D96 handoff. Report: `dembele/certificates/nelson-signed-orbit-d97.md`.

*Method:* pair every saved class with its reduced conjugate, group by
exact displacement, and calculate shell phase sums from reduced traces
over F. The 541 unit and 586 norm-31 classes yield 80 and 83 shells.
Discrete Abel summation accumulates signed phase counts before taking
absolute values. This requires no new quaternion or Hecke computation.

*Finite result:* the outer block's bound falls from about 5.52655 to
0.855935 for the unit family and from 5.38597 to 0.660035 for the
unweighted prime family. The respective gains exceed 6.45 and 8.16.
Whole-family phase counts satisfy explicit square-root and two-thirds
power comparisons only through A=25600. Conjugation and the CM
normalizer do not force global phase cancellation; odd scalar classes
have phase 1.

*Infinite interface:* derive the Stieltjes tail formula in terms of
P_N(A) and f_N'(A), and rigorously bound its transfer integrals using
D96 Taylor blocks plus a contour-4 infinite tail. For a proved bound
abs(P_N(A))<=M*(A/N)^(2/3) for all A>=25600, the unit and unweighted
prime remainders would be <0.124645+9.091228*M and
<0.116890+0.923191*M. The required premise is not proved. These
conditional constants therefore do not replace D96's actual error.

*Literature and decision:* identify the phase as the (2,2) Cartan
harmonic, involving both angles. Good's estimate as recorded by
Bourgain--Kontorovich--Sarnak motivates exponent 2/3, but exceptional
spectral terms and effective constants still need control. The
Gorodnik--Nevo framework points to the geometric/spectral inputs for
uniform translated counts. Do not substitute fitted finite constants
or a general spectral-gap slogan. Even a uniform orbital displacement
power saving retains the same norm-mass exponent after absolute Hecke
summation. Next prove and numerically instantiate a uniform harmonic
bound or a direct signed Hecke-block bound, then evaluate the complete
norm remainder before expansion.

*Verification:* script 363 and corrected transfer script 366 pass in
<6.20 seconds each. Two earlier type-conversion failures in 364/365 are
preserved with their logs. Audit 367 independently checks 163 exact
phase identities, all conjugation pairs, finite Abel/prefix bounds,
944 algebraic radicals, derivative and far-tail polynomial identities,
and 162 hashes / 2,049 dyadic intervals. Root generation passes in
<1.76 seconds. Sources 363--367 and bound report/artifacts are frozen.
The actual omitted-ideal bound stays <6.754e12, plus the unchanged
two-family tail <9626.300; the full interval still contains zero.
All jobs finished. No new Hecke/quaternion data, remote work, candidate
change or precision increase occurred. Keep corrected endpoints,
the 180-second process-group limit, D95's proved identification and
the cubic precision pause. Arithmetic CM jets, marked identification,
cubic recognition and the target polynomial remain open.

**D98 (2026-09-24). Bound the complete Hecke family spectrally.**
The user asked to continue D97's handoff. Report:
`dembele/certificates/nelson-spectral-ideal-d98.md`.

*Method:* identify each complete norm-ideal sum with the diagonal of
its unnormalized Hecke operator composed with the K-type-four radial
kernel. Transform the original S11 Mellin integrand before bounding it.
The two radial terms combine to a factor lambda+2: the lowest-weight-four
discrete series vanishes, while the weight-two derivative survives.
Vertical Gamma log-concavity uniformly controls the principal and
complementary series, including all exceptional parameters. The existing
CM packing bound limits a positive pretrace diagonal to 1795/1792.

*Arithmetic input:* use Blomer--Brumley's 7/64 exponent for the auxiliary
cuspidal Hecke spectrum and the stronger holomorphic Ramanujan bound for
the target eigenform. This removes the sigma_1(a) absolute orbit-count
factor and gives the mass sum d(a)^2*Norm(a)^(-(c-7/64)), convergent for
c>71/64. The norm-two Euler factor is removed, followed by the unit and
only the one saved prime above 31. No new ideal census is required.

*Result:* ten interval-certified contours give the best tested choice
c=5/4 and omitted-ideal bound <24,784,932,714, improving D96 by >272.48.
With the unchanged saved-family tails the full error is <24,784,942,340.
This is still about 3.244 million times the partial sum 7640.7582.
The proof does not assume an infinite signed-count law and does not
extrapolate D97's finite constants. The CM anchor remains uncertified.

*Decision:* keep enumeration and Hecke expansion paused. The next bounded
pilot should evaluate the completed spectral multiplier before absolute
values, with uniform control of the entire spectrum and the full norm
remainder. Do not repeat the contour scan at more precision. The
remaining loss is in absolute Mellin and independent Hecke comparisons;
the certified vertical tail is <1e-103.

*Verification:* script 368 passes in <5.38 seconds, root generation in
<0.41 seconds. Audit 369 checks 169 hashes, 20,480 rectangle endpoints,
107 dyadic intervals, transform and discrete-series identities, 64 Euler
coefficients, packing and tail arithmetic, algebraic powers and final
rational error assembly. The analytic spectral proof and Arb evaluations
are hash-bound. Sources 368--369 and bound report/artifacts are frozen.
Both jobs finished; no new quaternion/Hecke data, remote work, candidate
change or precision increase occurred. Preserve exact endpoints, the
180-second process-group limit, D95's positive scalar and conjugated
factorial ratio convention, and the cubic precision pause. Arithmetic
CM jets, marked identification, cubic recognition and the field remain
open. Entry documents, decisions and references are current.

**D99 (2026-09-24). Revisit hyperellipticity from the definitions and sources.**
The user requested a complete fresh review. Report:
`dembele/certificates/hyperellipticity-review-d99.md`.

*Conclusion:* retain geometric nonhyperellipticity of the intended
genus-16 C as an established project input. The proof can be shortened:
an involution with tree quotient on a graph with at least three vertices
would give an edge cut of size one or two. The fresh stable graph has
30 vertices, 45 edges and edge connectivity three. Every one of the
1,035 one/two-edge deletions stays connected. Baker specialization and
Chan's metric-graph theorem transfer this obstruction to C, independently
of all numerical differentials and candidate equations.

*Arithmetic and source review:* Magma 371 freshly recomputes the
58-class Brandt matrix with exact mass and unconditional class checks.
It uses the same HMF library, not a new Brandt implementation. New
standard-Python 372 reconstructs the full two-layer graph, quotient
and stable core, and separately finds 64 automorphisms/19 involutions
with quotient Betti histogram 8:5, 10:4, 12:6, 14:4. Positive and
negative controls pass. Kurihara's original Proposition 3-2/Lemma 3-3
was checked from the scan, along with Nekovar, Baker and Chan. The
integral quotient theorem includes torsion at 2; it removes reversed
oriented edge classes, not arbitrary loops. No faithful specialization
of curve automorphisms or tame fixed-point count is used.

*Published proof:* the Riemann--Roch implication is valid if its
vanishing premise holds, but an upstairs deck stabilizer acts trivially
on the coarse coordinate u=t^2. The local differential u du has a
simple zero downstairs and invariant pullback 2t^3 dt. Thus that action
does not establish the premise. This identifies a gap; the separate
graph proof supplies nonhyperellipticity. No claim about all CM points
being ordinary or other consequences in the paper is inferred.

*Scope and verification:* the actual saved-order audit and exact
candidate canonical-curve certificate were rerun successfully. The
candidate remains unidentified with C, even though both are now proved
nonhyperelliptic by separate arguments. Audit 374 verifies 479 hashes,
including D98's 169, and recomputes the graph. All jobs finished, with
successful runs at most 27.34 seconds. Failed 370 (unrecognized Magma
intrinsic) and corrected 371 are both preserved. Sources 370--374 and
bound reports/artifacts are frozen; old bound sources are unchanged.

*Next:* the requested review is complete. If construction resumes,
return to D98's completed spectral multiplier; no CM error bound or
candidate identification changed. Keep the process-group timeout and
enumeration/Hecke/cubic-precision pauses. Arithmetic CM jets, marked
identification, cubic recognition and the field polynomial remain open.
No external correspondence was sent; all entry documents are updated.

**D100 (2026-09-24). Revisit the complete construction methodology.**
The user requested a strategic step back. Report:
`dembele/certificates/construction-methodology-d100.md`.

*Assessment:* keep the curve/Jacobian route as the route with the most
concrete progress, while separating arithmetic candidate identification,
exact global cubic/section construction, and target-scale torsion. D51
proves the original kernels occur on canonical Y, not on the candidate.
The natural initial polynomial has degree 257 over F; taking its
appropriate normal closure gives the target over Q. Nonhyperellipticity
does not undermine this route or the independent existence theorem.

*Next research objective:* specify an executable independent arithmetic
comparison using D88's three-coefficient rank-45 or four-coefficient
divisor criterion. Include the arithmetic frame and a mechanism proving
exact equality. Numerical enclosures without a separation bound or an
independent exact verification do not prove the proposed coefficients.
D98's completed spectral multiplier remains an analytic option; the
review does not prescribe its automatic continuation. Its present error
enclosure still contains zero.

*Remaining dependencies:* marked double-cover identification is needed
before the nine-cover shortcut applies. The shortcut does not construct
exact cubic coefficients or bound their heights. D86's 31^128 lift and
negative bounded-height recognition remain current. Norm-97 full Euler
cofactor separation and genus-64/degree-51 target arithmetic remain open;
smaller controls do not prove the combined case. A separating invariant
on 257 lines still requires actual torsion and certified reconstruction.

*Alternatives:* direct certification of the original residual kernel
could bypass full marked-curve identification, but no effective criterion
has been instantiated here. A smaller abelian variety lacks an effective
model; equation-free or higher-level uniformization approaches still
need arithmetic section/component data. A reduction graph alone misses
the desired supercuspidal new part.

*Scope:* this is a methodology review, not a new mathematical certificate.
No arithmetic jobs, precision increases, external correspondence, or
changes to frozen sources/results occurred. Entry documents now make
D100 govern resumption. Keep the existing timeout and resource pauses.

*Execution-readiness follow-up (same date):* the user asked whether more
planning was needed and requested current decisions and references.
No additional broad strategy review is required. Section 7 of D100 now
specifies the first bounded task: establish an exactness mechanism for
an independent CM tangent, initially assessing the existing
Nelson/Shimizu route. Before another spectral-bound pilot, seek an
effective algebraic separation bound for the normalized unknown
coefficients or an independent exact verification identity. Specify
the arithmetic frame and CM label, field/basis, denominator and height
bounds if using recognition, and a finite error tolerance. None of
these missing inputs is supplied merely by candidate-derived jets.

*Acceptance and stopping conditions:* a usable mechanism justifies a
bounded evaluator pilot; a rigorously incompatible tangent rejects the
marked comparison. A missing indispensable input must be named and
prompts assessment of an arithmetic restriction map, not automatic
precision/enumeration growth. A tangent match alone does not complete
identification: extend to the rank-45 three-coefficient test or the
four-coefficient divisor criterion. The current S11 interval contains
zero and cannot be used as a certified denominator.

*Documentation:* REFERENCES now includes a D100 source-to-claim ledger,
the separate Mascot certification reference and its applicability limit,
and the distinction between a literature theorem and our adaptation.
The first task is ready to attempt as research; an effective exactness
mechanism and the complete construction are not claimed ready. No new
arithmetic computation was run for this follow-up.

**D101 (2026-09-24). Execute the bounded CM-tangent exactness task.**
The user said to proceed after D100's execution specification. Report:
`dembele/certificates/cm-tangent-exactness-d101.md`.

*Result:* the tangent is the ratio G_bj(D)/G_ba(D) of first-Gaussian
sections in H0(3K_C). The map has dimensions 120 -> 75. The order-two
pullback coefficient has factor 8*z^3, explaining why the upstairs
bracket vanishes while the coarse value may not. Exact controls check
coordinate covariance and the quotient factor.

*Exactness criterion:* a proved clearing integer M for the actual minus
candidate value and certified errors at all d embeddings give equality
when M^d*product(E_sigma)<1. A denominator ideal gives a sharper version.
Thus all-conjugate evaluation can avoid a separate height bound. Working
over F may require d=136, not the candidate's degree 17. Explicit
theta+2^(-n) controls show why field information and denominator-prime
support alone do not suffice. A separate projective-height inequality
identifies the clearing ideal, arithmetic frame/metric norms and
coarse-canonical CM height needed for a one-embedding certificate.

*Source applicability:* Zhao's maximal-compact CM-height formula
permits the actual common ramification at 2. Yuan's quoted CM-point
Theorem 1.2 forbids it; his different curve-height Theorem 1.1 remains
potentially useful. Both field polynomials are 2-Eisenstein, so this
is an exact hypothesis check. Intrinsic point or curve heights have
not been converted into bounds on our residue-framed sections. The
integral residue-map index and compatible archimedean norms are still
missing. An auxiliary PEL construction likewise still needs actual
CM test objects and global Gaussian-section restrictions.

*Computation:* Magma 375 determines the candidate tangent exactly.
Its clearing integer has 269 decimal digits in the saved integral
lattice and 285 in the power basis; these are neither unknown-target
bounds nor minimum precision requirements. Python 376 independently
replays the quadric linearizations, integral-basis conversion, mod-31
agreement and uniqueness, plus corruption and formal controls.
Magma passed in 8.81 seconds; a bounded independent recheck passed in
1.92 seconds. Initial collection failed on multiline sequence output;
the failed source/record are retained, and repaired collection reused
the successful arithmetic job. Audit 377 binds the report and source
ledger and repeats the arithmetic and elementary proof controls.

*Decision:* this first investigation is complete, but no independent
Shimura tangent or effective target tolerance was obtained. The exactness
gate for another spectral pilot remains unmet. Next establish the
actual residue-frame lattice/metric comparison, potentially using the
new height inputs, or construct the arithmetic Gaussian-section
restriction map. The candidate has neither been identified nor refuted.
Keep D98 accuracy, exact cubic construction and target-scale torsion
as separate gaps. Preserve the 180-second process-group cap, resource
pauses and all completed sources 375–377 and bound results. No previous
bound artifact was changed or external correspondence sent. Decisions,
references and entry documents are current.

**D102 (2026-09-24). Continue with the integral residue-frame comparison.**
The user authorized continuing the plan after the tangent explanation.
Report: `dembele/certificates/cm-residue-lattice-d102.md`.

*New mathematical result:* under explicit DVR model/divisor hypotheses,
the cokernel length of the primitive residue map equals
`length H1(O(D)) + v(Norm(a))`, with a the principal part of a generator
of `H0(O(D))/R`. The target is the trace-zero codifferent. The proof
uses the principal-parts sequence and relative duality; a short exact
sequence separates the two contributions. Globalization must retain
the pencil lattice. Fixed smooth genus-two and nonhyperelliptic
quartic controls show an unbounded index at a good prime even with
an etale split divisor and zero H1 term. These are not counterexamples
for the fixed CM closed point or to bounds using marked-point heights.

*Exact arithmetic:* script 378 reads the existing degree-17 field
polynomial and basis, without candidate equations, jets or numerical
banks. It checks irreducibility modulo 31, all 153 unordered basis
products, trace discriminant 2^79 and trace ideal Z. The trace-dual
lattice has clearing integer 32. The centered basis eta_i needs the
common factor 17 to enter that lattice; its trace-zero index then is
2^79*17^15. No maximality assertion or identification with the actual
horizontal order is made. These factors do not clear the unknown
Shimura tangent.

*Archimedean result:* the signed evaluation cofactors c_i satisfy
`det((diag(c)*E)_r)=(-1)^r*product(c_i)`. Cramer's rule gives an explicit
inverse bound once the entries and nonzero minors have certified
bounds in a compatible arithmetic normalization. Empirical condition
numbers do not instantiate it. Controls check covariance, both defect
terms and ranks 2 and 16. Audit 379 independently computes traces via
multiplication operators and determinants via Bareiss, checks the
nonhyperelliptic control and binds 12 sources. All 22 D101 source
hashes remain unchanged. Initial jobs passed in 0.56 and 0.63 seconds;
no failures, all within the 180-second process-group cap.

*Decision:* the field trace-lattice component is settled. Next bound or
compute the two geometric defects on the actual marked C_ar, including
the pencil/horizontal-order comparisons, and match the archimedean
norms; alternatively construct actual Gaussian-section restrictions.
No independent tangent, effective actual height bound or numerical
tolerance has been obtained. D101's Gaussian denominator and canonical
height inputs remain required. The spectral pilot gate stays unmet;
do not repeat the field-lattice calculation or enlarge precision and
enumeration as a replacement. Preserve sources 378--379 and bound
outputs, all earlier artifacts and existing resource pauses. Exact
cubic construction, norm-97 separation and target torsion remain
separate gaps. Decisions, references and entry documents are current.
No external correspondence was sent.

**D103 (2026-09-24). Bound tangent height with integral adjugates.**
The user authorized continuing after D102. Report:
`dembele/certificates/cm-adjugate-height-d103.md`.

*New result:* the residue-frame inverse need not be bounded directly
for a projective height estimate. Signed evaluation minors define an
integral map Phi into a common arithmetic line times the trace-zero
module. Its adjugate applied to the integral vectors 17*eta_j gives
canonical sections in a common line T. The determinant factor cancels
in Gaussian ratios; finite common zeros only improve the height bound.
The Gaussian map extends integrally through nodal fibres. This avoids
separately bounding D102's residue index or the nonzero evaluation
minors from below in this argument. It does not prove their nonvanishing
or remove conditioning requirements from a later numerical computation.

*Actual analytic upper bounds:* for each CM embedding beta^2=-pi,
the perpendicular projection of a norm-one quaternion has norm v with
4*v integral and compact conjugates between 0 and 4. The product
formula forces |v_split|>=2^-16 for a moving translate. Norm-one and
normalizer orbits agree at the CM point, so rho=2^-10 is a uniform
embedded disk modulo its stabilizer, including arithmetic conjugates.
This gives evaluation norm <=2^20 and Gaussian norm <=2^60 without
new enumeration. An exact root/basis estimate gives |17*eta_j|<2^35.

*Height theorem:* keeping the arithmetic lines and using Bost's lower
Faltings-height bound gives `h(v_j)<=513*H_CM,disk+8400`. Here H_CM,disk
is the actual stable coarse-canonical fibre height with ||d(z^2)||=1.
It remains numerically unbounded. The intended arithmetic CM labels,
all nonzero evaluation cofactors and a nonzero Gaussian denominator
are hypotheses. No candidate identification or independent tangent
was obtained. No upper bound on the genus-16 curve's Faltings height
is needed for this particular route.

*Checks:* main 380 passed in 0.24 seconds. Audit 381 passed in 0.40
seconds, independently checking dense rank-3/rank-16 frames, Horner
field bounds and rational constants. It binds 45 sources and verifies
all 12 D102 and 22 D101 source hashes unchanged. The first 0.04-second
run found a zero bracket in accidentally proportional toy jets. Its
source snapshot, log and receipt are preserved; correcting those
test jets changed no arithmetic input or theorem. Every job used a
180-second private process-group cap.

*Decision:* next prove the comparison of H_CM,disk with Zhao's
arithmetic Hodge height, including the norm-one/genus-16 quotient's
wild dyadic fibre, and bound the result. Do not infer an integral
comparison from u=z^2 alone or from compatibility in a level tower.
Do not resume a per-prime residue-index/minor-lower-bound search just
to instantiate D103. D102 remains a valid, frozen theorem. The new
bound does not yet justify a spectral pilot; retain D98's unresolved
full error and the existing resource pauses. Keep cubic construction,
norm-97 separation, target torsion and the field polynomial as separate
gaps. Sources 380--381 and bound artifacts are frozen. Decisions,
references and entry documents are current; no correspondence was sent.

**D104 (2026-09-24). Close the intrinsic CM height comparison.**
The user authorized continuing after D103. Report:
`dembele/certificates/cm-intrinsic-height-d104.md`.

*New geometric result:* Liu--Lorenzini's extension theorem supplies
a map between stable models. Pullback of dualizing differentials
extends integrally by a codimension-one check at nodes. Differentiating
this map at a simple ramification section gives W_C -> W_S^2, even
if the section meets a node. Its archimedean norm is 2. Auxiliary
sufficiently small levels, maximal at each chosen finite prime, and
Yuan--Zhang's structural Hodge theorems then give
`H_CM,disk<=2*h_L(Q)+log(2)`. No explicit bad-fibre equations or
division by 2 are needed. Toy nodal controls are not asserted to be
actual Shimura models.

*Numerical result:* Zhao 7.4 plus published nearby-type and averaged
Colmez identities give `h_L=-R/8+log(2)/16` in absolute normalization.
The CM degree-16 field is cyclotomic of conductor 64; eight primitive
odd characters give exact rational log-Gamma coefficients. Finite
products and an independent Taylor series both prove `h_L<17/10`.
Thus `H_CM,disk<41/10`, and D103 yields `h(v_j)<10504` under its
arithmetic labels and frame/chart hypotheses.

*Source audit:* Zhao's final proof display of 7.5 omits d_Sigma,
unlike earlier 7.4 and statements 1.1/7.5. Our derivation retains it;
no author confirmation is claimed. Yuan--Zhang's Shimura-point
normalization differs by [F:Q]=8. The CM-point theorems excluding
common ramification remain unused; the structural Hodge theorems
have no such restriction. The CM and curve Faltings metrics are
tracked separately.

*Exactness diagnostic:* the saved candidate has h(beta_j)<683.
Assuming the correctly labelled common field has degree at most 136,
sufficient absolute errors are 10^(-660791) at one embedding or
10^(-4859) at every embedding. These are conservative sufficient
thresholds, not minimum precision, existing errors or evaluator
cost estimates. Candidate data enters only this diagnostic, not
the target-height proof.

*Checks:* main 382 and audit 383 passed in 1.09 and 1.11 seconds,
both on their first computational attempts under 180-second private
process-group caps. The audit independently recomputes traces with
generator 3 and a conjugate-product inverse, uses a separate Gamma
series and log implementation, and verifies nodal second jets. It
binds 53 sources and checks all 45 D103 hashes unchanged, including
transitive D102/D101 sources. These computations do not machine-verify
the geometric proof or cited theorems.

*Decision:* the intrinsic height gap is closed. Next establish the
actual arithmetic CM labels and qualitative frame/chart nonvanishing,
then assess an independent evaluator against an exactness threshold.
Do not repeat the height comparison or per-prime residue-index search
solely to instantiate D103. No independent tangent or candidate
identification; D98 still contains zero and the spectral pilot gate
remains unmet. Retain enumeration/Hecke/cubic-precision pauses. Exact
global cubic/section data, norm-97 separation, target torsion and the
final field polynomial remain separate gaps. Sources 382--383 and
bound results are frozen. Decisions, references and entry documents
are current; no correspondence was sent.

**D105 (2026-09-24). Prove the actual CM frame; use an auxiliary-field tangent atlas.**
The user authorized continuing after D104. Report:
[cm-frame-arithmetic-d105.md](dembele/certificates/cm-frame-arithmetic-d105.md).
For the actual seventeen-point CM divisor D, H0(K_C-D)=0. CM
transitivity then proves all seventeen maximal cofactors nonzero.
This closes the projective-frame hypothesis independently of the
candidate or any numerical differential rank.

*Geometric proof:* the layer-swapping Atkin--Lehner action reverses
nine annuli and fixes no vertex. An annulus unit/slope argument proves
two simple generic fixed points per annulus in characteristic zero,
including residue characteristic 2. Kurihara's integral quotient
theorem and stabilization give twice the sum of nine marked midpoints
for the branch divisor. Test every possible location of P32 rather
than guessing it: all nine K-D classes are noneffective, with
q-reduced root coefficients -3,-2,...,-2. Baker's specialization and
canonical-class lemmas transfer this to the actual curve.

*Arithmetic alternative:* the degree-17 polynomial splitting field
equals the Hilbert class field H of the degree-16 CM field M. Use
D59's proved order-272 Galois group and class number 17, its bounded
degree-16 resolvent, and unramifiedness. The resolvent identity is
rechecked exactly; gamma generates M since its power-basis determinant
is 5 modulo 101. The verified order discriminant 2^79 excludes odd
ramification. The dyadic local units of M are pro-2 and have no
C17 quotient, excluding relative dyadic ramification. This avoids
numerical root orientation and the disputed hyperellipticity premise.
H is the solvable CM auxiliary field, not the nonsolvable target.

*Decision:* any fixed bijection of the actual CM points with polynomial
roots defines the frame over H, with [H:Q]=272. This bypasses the
saved D59 labelling for the height calculation but does not prove
F-equivariance or frame descent. Nonhyperellipticity and s1(P) nonzero
give a nonzero fifteen-coordinate projective Gaussian tangent.
D103--D104 bound its height by 10504 without assuming a specific
nonzero G12. Work with the finite atlas until a chart is certified.

*Exactness diagnostic:* the candidate projective height is below 677.
In a consistently labelled common valid chart over H, sufficient errors
are 10^(-1320873) at one embedding or 10^(-4857) at every embedding.
These are conservative sufficient thresholds, not minimum precision
or existing error certificates. The all-embedding condition includes
the conjugate frame and transported bijection. Higher jets at all
seventeen points are required for the H-version of D88, unless
equivariant labels/descent are independently proved.

*Checks:* probe 384, main 385 and audit 386 passed in 0.35, 0.95 and
0.71 seconds, each on its first computational attempt under the
180-second private process-group cap. The audit reconstructs marks
from Brandt entries, checks the witnesses without the discovery
solver, rejects altered potentials/orders/branch allocations, replays
integral-order arithmetic, and binds 543 sources. All 479 D99 and 53
D104 bound hashes are unchanged. The finite calculations do not
machine-verify the geometric proof or the cited theorems. The original
conditional probe, completed sources and outputs remain frozen.

*Next:* assess an actual independent tangent/jet evaluator with a
feasible equality mechanism. Certifying D59 labels remains useful for
smaller fields and Galois propagation, but it is no longer a prerequisite
for the qualitative frame or projective height theorem. A specific
numerical chart, higher-jet exactness and descent still need certificates.
No independent tangent or candidate identification has been obtained;
D98's existing full enclosure still contains zero. Keep the spectral
pilot gate and enumeration/Hecke/cubic-precision pauses. Global cubic
data, norm-97 separation, target-scale torsion and the final target
polynomial remain open. Decisions, references and entry documents are
updated; no correspondence was sent.

**D106 (2026-09-24). Rigidify the CM marking, descend the frame, and bound higher jets.**
The user authorized “continue” after D105. Report:
[cm-rational-frame-jets-d106.md](dembele/certificates/cm-rational-frame-jets-d106.md).
The actual marked curve satisfies Aut(C_Qbar,D)=1. This replaces
D58's conditional D56-based rigidity proof and makes its geometric
Q-descent compatible with the given F-model.

*Proof and source choice:* stable-model uniqueness and the finite
unramified automorphism scheme give faithful specialization, including
at residue characteristic 2. Every rational component has three
distinct attaching points, so the full geometric automorphism group
embeds in the graph group of order 64. Its D-preserving subgroup is
a 2-group acting on seventeen points, hence has a common fixed point.
Galois normalization and CM transitivity make every CM point fixed.
D105's projective frame and D99's canonical embedding force identity.
This uses neither tame specialization nor Dembélé's disputed stronger
admissibility/exponent argument. It does not determine unmarked Aut(C).

*Arithmetic consequence:* D58's canonical-conjugation input and marked
descent remain explicit literature inputs. Trivial marked automorphisms
make the comparison unique, hence F-defined, and satisfy the Weil
cocycle automatically. The degree-17 residue field embeds into the
D105 CM class field H. Affine point stabilizers are conjugate Sylow
2-subgroups and self-normalizing, so it is uniquely Q-isomorphic to
the saved root field L. Residues of h*omega, for poles(h)=D, give a
rational canonical basis from the trace-zero basis, up to one scalar.

*Scope of labeling:* the abstract field/frame identification is now
proved. The saved numerical CM-point/root matching and the change
from the old analytic basis to this rational frame are not certified.
A local embedding and a valid chart still belong in the evaluator
certificate. In particular, G12 need not be assumed nonzero.
No explicit descent matrices or actual section evaluations are claimed.

*Higher jets:* integral differential expressions have line powers
omega^9*T^6 and omega^15*T^10. The D103 disk bounds give actual
ratio Taylor heights below 10504,31518,52533 at orders 1,2,3, with
the factorials included. Magma 388 supplies exact candidate references,
whose heights are below 677,1947,3218. D88 already used the same
ratio parameter; an extra raw-X1 factor in its second coefficient
would be incorrect. Its direct mod-31 comparison passes.

*Equality mechanism:* 31 is inert of residue degree 17 in L, so a
nonzero difference has height at least v31(delta)*log(31). Sufficient
valuations are 3257,9746,16236. Common precision 9746 supports D88's
J3 rank test; precision 16236 supports J4's degree/vanishing test.
The thresholds are conservative sufficient bounds, not minima,
existing precision or a cost estimate. No global actual denominator
bound is required for this height argument.

*Checks:* main 387 enumerates the graph via twin collapse and color
refinement, checks the 272 affine maps, and verifies higher formulas
by independent series reversion and covariance controls. Review 389
checks 364 exact quadratic coefficients and ranks 17,34,45,45.
Main/Magma/probe/review passed in 0.15/42.91/1.11/1.42 seconds, with
180-second private process-group caps. The initial main syntax
failure is preserved with its source snapshot. The review binds
562 sources and checks all 543 D105 hashes unchanged. Finite arithmetic
does not machine-verify geometric/descent theorems.

*Decision and next step:* use the rational frame and degree-17 bounds
when the evaluator certifies that normalization. Retain D105's
arbitrary H-frame as a valid alternative. The next research task is
an executable independent arithmetic tangent/jet evaluator; exact
CM reciprocity orientation is a useful bounded prerequisite for
reusing the analytic route. No 31-adic Shimura evaluator is implemented.
Do not increase precision merely because a threshold is available.
D98's enclosure still contains zero; preserve its spectral pilot gate
and existing enumeration/Hecke/cubic-precision pauses.

No independent actual tangent, candidate identification or target
polynomial has been obtained. Even after (C,D) identification,
P32/degree-nine branch matching, exact cubic/section data, norm-97
separation and target-scale torsion remain separate requirements.
Sources 387--389 and bound artifacts are frozen. Decisions, references
and all entry documents are current; no correspondence was sent.


**D107 (2026-09-24--25). Certify the saved CM labels by rigidity, a resolvent norm and cycle separation.**
The user authorized continuing after D106. Report:
[cm-root-matching-d107.md](dembele/certificates/cm-root-matching-d107.md).
The saved D59 lookup is now proved. The abstract rational frame from
D106 can be used with this exact correspondence in the saved analytic
CM-point order, once true differential evaluations are available.

*Real structure and source choice:* conjugation by I preserves the
saved order, with negative split determinant. Its antiholomorphic
action preserves D, so D106 marked rigidity identifies it with
canonical complex conjugation. This avoids a separate adelic
comparison or applying a CM-reflex-field descent theorem. A positive
order unit U makes U^(-1)I anticommute with beta at point 8, proving
that point real. The c -> -c class action makes it the unique real
point. Exact Sturm and square bounds applied to the actual Rickards
matrix embedding select beta=-i*sqrt(2+b). Both off-diagonal signs
matter; a different matrix convention must not be substituted.

*Exact root action:* fixed 4096-bit Newton iteration proposes centers,
then independent integer Rouche inequalities certify radius-10^-1080
disks for seventeen roots and beta. They imply
|kappa_f-gamma|<10^-1000. An integral field norm with two small
conjugate embeddings and 275090^270<10^2000 makes the equality exact.
This alone would not prove the cycle Galois: a separate rank-271
certificate shows the only rational relation among the 272 ordered-pair
monomials is their all-ones sum. Distinct directed cycles then have
distinct sums. The order-17 stabilizer of gamma centralizes the
proposed cycle, forcing it to generate the actual Galois subgroup.

*Propagation:* independent Hensel lifts modulo 31^8 identify that
cycle as arithmetic Frobenius at (31,beta-19). Recomputing the prime
class gives 3 in D59's saved generator. Point 8 matches real root 2
under D106's unique residue-field isomorphism. Voight's explicit
arithmetic Artin convention propagates this pair and recovers exactly
the old seventeen-entry lookup. The old complex Galois root-order
comparison and approximate CM function values are not trusted.

*Checks and resources:* real-structure/rank/witness/probe/final-review
jobs passed in 4.30/1.06/3.97/1.60/1.90 seconds under 180-second
private process-group caps. Review 393 binds 588 sources and checks
all 562 D106 hashes unchanged. Two first attempts failed on Sage
API details; original logs, receipts and source snapshots are preserved.
The finite audit independently verifies quaternion and rational
inequalities, the rank and local lifts. Rigidity, reciprocity and
their geometric use remain mathematical proof inputs.

*Decision and next step:* use the certified labels for the rational
residue frame, without certifying the saved differential bank or its
approximate change matrices. Establish an executable independent
Shimura evaluator, a complete error bound and a nonzero Gaussian chart
before requesting more precision. For the complex route D98 still
requires a completed spectral multiplier bound over the entire
principal/complementary spectrum, the surviving discrete series and
the infinite norm remainder. An arithmetic alternative must actually
compute Shimura differential data; local root lifting does not do so.
The qualitative frame theorem and available equality thresholds do
not meet that evaluation gate.

No actual tangent/jet, particular G12 nonvanishing, candidate
identification or target polynomial has been obtained. Retain the
enumeration/Hecke/cubic-precision pauses. D107's bounded algebraic root
certificate did not restart those computations. Downstream marking,
global cubic/section data, norm-97 separation and target-scale torsion
remain separate tasks. Sources 390--393 and bound artifacts are frozen.
Decisions, references and all entry documents are updated; no
correspondence was sent.


**D108 (2026-09-25). Reject the unchanged absolute spectral comparison; specify a direct dyadic moment interface.**
The user authorized continuing after D107. Report:
[shimura-evaluator-d108.md](dembele/certificates/shimura-evaluator-d108.md).
This addresses evaluator feasibility after closing the CM-labeling gap.
No actual Shimura differential was evaluated.

*Necessary-condition test:* before constructing a full-spectrum
majorant, evaluate the completed multiplier at the required surviving
discrete series mu=1. Gamma recurrence gives H_N(1)=8*pi/N*K1(Z0*N).
Certified quadrature gives H_31(1)=462.99971524852148.... The global
maximum of h_p(1) is 4*pi*(5-2*sqrt(6)). With the unsigned geometric
diagonal bound and retained absolute Hecke envelopes, the seven
omitted norm-31 primes alone force the comparison above 460891.49,
over 60.32 times the partial. Positive mixtures cannot evade this
floor. Even finite-place exponent zero leaves more than 41 times
the partial. This rejects the method without needing an upper bound
on the rest of the spectrum or infinite tail.

*Scope and decision:* do not spend work on the full-spectrum version
of this same per-ideal absolute comparison. The floor is not the
actual error, and no impossibility claim for Nelson's method follows.
Joint Hecke cancellation, a more effective diagonal bound or changed
residue weights remain possible. A complex-route restart must say
which hypothesis of this obstruction changes. D98's old full
enclosure is unchanged; its saved-family error alone exceeds the
partial. Existing enumeration and Hecke-bank pauses remain in force.

*Direct alternative:* bounded scalar harmonic measures on the
arithmetic tree boundary give Poisson differentials. At the ramified
dyadic CM point beta, use the three charts pi*x, 1+pi*x, 1/(pi*x).
The actual Eisenstein polynomials give v(pi)=1, v(2)=8, v(beta)=1/2.
Moments through J of absolute precision P and bound v(mu(B))>=-d
give ordinary Taylor error min((J-k)/2-d,P-(k+1)/2). Passing to
w=(z-beta)/(z+beta) and u=w^2 gives the first three coarse differential
coefficients with error min((J+1)/2-d,P). The factor two is accounted
for exactly. These are conditional local bounds, not actual moments
or a cost prediction at identification precision.

*References and implementation choice:* Franc--Masdeu supplies the
Q_p moment framework; its updated harmonicity correction matters.
Do not assume its overconvergent control theorem or software ports
unchanged to ramified K. Masdeu--Torrents gives a general totally-real
tree-domain algorithm. Its public implementation is documented,
not pinned, inspected or tested here. Read-only inspection of the
existing HMF source identifies order and ideal-representative access.
The saved Brandt matrix lacks local matrices and edge transports.

*Checks:* main 394, corrected local 395, probe and review 396 passed
in 7.47/2.97/0.09/0.38 seconds under 180-second private-process-group
caps. Review 396 binds 606 sources and preserves all 588 D107 hashes.
It independently reconstructs conservative rational quadrature errors,
pi/radical bounds, the comparison floor and coordinate/valuation
identities. Arb centers and Sage field controls are hash-bound.
The four local controls use synthetic three-atom measures. An initial
sign-flip assertion failed because v(2)=8 hides that corruption at
low precision; the corrected test detects it at J=31. The original
source, failure and receipt are preserved. No output came from the
failed attempt.

*Next bounded task:* export the actual definite order, certify its
integral dyadic splitting and verify one vertex/edge transport
witness, reusing the 58-class arithmetic data. Do not start a full
new tree census yet. Subsequent work needs the actual arithmetic
group/quotient, invariant cocycles, dyadic CM and residue-frame
matching, certified moments and a valid Gaussian chart. D107's
complex labels do not provide a dyadic embedding matrix. D106's
inert-31 thresholds need a new local-degree conversion at 2.

No actual tangent/jet, candidate identification or target polynomial
has been obtained. Retain cubic-precision and all other resource
pauses. Downstream branch marking, global sections, norm-97 separation
and target-scale torsion remain separate. Freeze sources 394--396
and bound artifacts. Decisions, references and all entry documents
are updated; no correspondence was sent.


**D109 (2026-09-25). Complete the bounded definite-order, dyadic-splitting and edge-transport plan.**
The user explicitly authorized the plan with “proceed with this plan”.
Report: [definite-dyadic-d109.md](dembele/certificates/definite-dyadic-d109.md).
All three deliverables are complete; no full new census was needed.

*Actual order:* use the existing HMF QuaternionOrder(M) construction,
with D99's field, level and seed, to export the 32-dimensional integer
lattice in B=(-1,-1)_F. This definite algebra has finite discriminant
one. Exact checks establish 1, O_F-stability, all 1024 basis products,
and reduced-trace determinant 2^124. This proves maximality without
relying only on the software predicate. The export does not identify
an ideal-class ordering with D99's saved matrix.

*Exact local certificate:* use Magma pMatrixRing only to propose
matrices. A rational C,x0,y with f(t)=t^2+y^2+1 gives valuations
v(f(x0))=188 and v(f'(x0))=8. Hensel specifies an exact t in K with
v(t-x0)=180. Conjugating [0,-1;1,0] and [t,y;y,-t] by C gives exact
quaternion relations. Every order-basis image is integral and known
to error at least 176; residue rank four proves its image is all
M2(O_K). This works over the ramified degree-eight K, with v(2)=8.
No control theorem or software port from Q_p is assumed.

*Arithmetic edge witness:* u=(1-i-j-k)/2 is an actual norm-one unit
of the exported order. It reduces to [1,1;1,0] and permutes the three
neighboring lines by [2,0,1]. The exact transition from lattice L0
to L2 is integral with determinant one and error bound 175. The
witness fixes the base vertex. Do not describe it as a cross-vertex
side-pairing or as a computed fundamental domain.

*Execution and review:* the initial export failed an exact-equality
assertion on approximate matrices. Two attempts then timed out at
the direct map of all 32 order-basis elements. Their private process
groups were terminated at 180 seconds; sources, logs and receipts
are preserved and none wrote a result artifact. Export four algebra
matrices and verify the full order with exact arithmetic instead.
Successful export / certificate / probe / final review jobs took
0.63/6.15/0.78/1.04 seconds. Independent Python review 399 checks the
lattice, Hensel inequalities, integral splitting and edge transport;
wrong-root and wrong-target controls are rejected. It binds 629
sources and preserves all 606 D108 hashes. Freeze sources 397--399
and bound artifacts. Recheck with 399 --check.

*References:* Magma's local-splitting documentation allows ramification
of K/Q_2; it requires splitting of B at p. Masdeu--Torrents supplies
the norm-one arithmetic setting and column-lattice action. The local
HMF construction and access functions are inspected and hash-bound.
No external tree-domain implementation has been installed or run.

*Next bounded task:* make D99's already established arithmetic group
and Atkin--Lehner/normalizer quotient explicit in these matrix
coordinates, reconcile it with the saved 58-class Brandt data, and
certify one transport moving the base vertex. Preserve same-session
ideal ordering in any export. Continue with a bounded witness before
a full domain construction; no full new census is justified yet.
Actual harmonic cocycles, their measure bound, dyadic CM/residue-frame
matching, certified moments, cofactor error propagation and a valid
Gaussian chart remain necessary for an evaluator.

D108's moment formula remains conditional and its unchanged absolute
spectral comparison remains rejected. No actual tangent/jet, candidate
identification or target polynomial has been obtained. Retain the
enumeration/Hecke/cubic-precision pauses and the 180-second job cap.
Downstream marking, global sections, norm-97 separation and target-scale
torsion remain separate. Decisions, references and all entry documents
are current. No correspondence was sent and no jobs remain running.


**D110 (2026-09-25). Make the dyadic group and odd coset explicit; certify movement of the base vertex.**
The user authorized continuing. Report:
[dyadic-group-transport-d110.md](dembele/certificates/dyadic-group-transport-d110.md).
The bounded next step after D109 is complete.

*Group contract:* put R=O[1/b], A=O_F[1/b], G=R*/A* and let Gamma be
the projective image of R^1. D99's class and unit certificates show
Gamma=ker(v(Nrd) mod 2). They also identify N_B(R)/F* with G, using
local maximal-order normalizers away from p. Cerednik--Drinfeld gives
S=Gamma\Omega and C=G\Omega geometrically over the completed maximal
unramified extension. The odd coset represents w_p. Do not confuse
normalization of R with stabilization of the definite maximal order O
at p, or infer a CM-label or descent matrix from this group description.

*Recover the missing arithmetic witnesses:* D99 saved only the matrix
and stabilizers, so replay the same 58-class, norm-two calculation and
read the cached representatives and tps in that session. This is
reconstruction of the existing data, not an expanded class census or
new tree search. The new matrix and stabilizers agree entry for entry
with D99, and the entire order basis agrees with D109. Export the four
ideals and seven quaternions along the shortest odd closed walk
[0,1,3,4,4,3,1,0]. Exact sandwich inclusions have Z-index four on both
sides. Preserve same-session indexing; do not infer it from graph
shape alone.

*Explicit outcome:* if c=(b^7-7b^5+14b^3-7b)/2, then c^2=1-b^2/4.
The normalized odd element is W=(1+b/2)i+cj, with norm 2+b and
W^2=-(2+b). Thus G/Gamma=C2 has an explicit involutory representative.
W moves the base vertex seven edges in the fixed D109 splitting.
For u=(1-i-j-k)/2, the element g=WuW^(-1) belongs to R^1 and moves
the base vertex fourteen edges. It has projective order three.
The further product h=ug has trace 1-c of valuation -7, so is hyperbolic
with translation length fourteen. No additional search is needed.

*Certification:* Sage 401 and rational Python replay 402 check the
selected right ideals, 4096 module products, seven exact sandwiches,
normalization and localized-order membership. Replay also exports
the localized conjugation matrices. Exact lattice transitions for W
and g have unit determinants and error bounds 169 and 162. Norm parity
rejects treating W as norm-one projectively; exact valuations reject
pretending that g fixes the base vertex. The hyperbolic assertion
follows from its checked trace/norm and an elementary Hensel argument.

Export / certificate / probe / review passed on their first attempts
in 28.77/8.03/2.88/3.11 seconds under the 180-second private-process-group
cap. Review 402 binds 643 sources and preserves all 629 D109 hashes.
Freeze sources 400--402 and bound artifacts. Recheck with 402 --check.
Dembélé's uniformization and graph propositions, Masdeu--Torrents's
arithmetic setup, and the actual HMF interfaces are recorded in the
updated reference ledger. No external domain implementation was run.

*Next bounded task:* complete the adjacency transports and vertex
stabilizers for the existing 58-class data. Certify all three neighbors
at every vertex and turn these data into a finite edge-reduction
procedure. Then construct G-invariant scalar harmonic cocycles, checking
the expected dimension 16 and a bound for their measures. Reuse the
known quotient without expanding the level, prime bank or class census.
The current witnesses are not a full fundamental domain or generating
set. The abstract CM embedding W^2=-2-b is not yet matched to the saved
seventeen-point labels and rational residue frame.

Actual moment lifting, dyadic frame matching, cofactor error propagation
and a valid Gaussian chart remain separate gates. No actual tangent/jet,
candidate identification or target polynomial has been obtained.
Retain enumeration/Hecke/cubic-precision pauses and D108's rejection
of the unchanged absolute spectral comparison. Downstream marking,
global sections, norm-97 separation and target-scale torsion remain
separate. Decisions, references and all entry documents are current.
No correspondence was sent and no jobs remain running.


**D111 (2026-09-25). Complete arithmetic edge reduction and construct the sixteen invariant harmonic cocycles.**
The user authorized continuing with “keep going!”. Report:
[dyadic-harmonic-d111.md](dembele/certificates/dyadic-harmonic-d111.md).
The bounded next task after D110 is complete.

*Arithmetic scope:* reconstruct and export all data for the existing
58-class, norm-two calculation in one session. The matrix/stabilizers
match D99 entry for entry and the entire order basis matches D109.
This introduces no new class census, level or Hecke prime. All 174
neighbor entries and 164 projective stabilizer elements are available.

*Certification choice:* prove each global ideal's b-stability and
p-supported index in O, then certify a local matrix frame using
integrality and residue rank four. Nakayama and localization give the
global right-ideal property. For each transport, exact localized
membership and determinant-one-length local inclusions prove both
global sandwich indices are four. This avoids a redundant 58-fold
order-product check while retaining exact arithmetic proof. The full
class/stabilizer counts retain D99/Magma provenance; rational review
checks all exported units and their local actions independently.

*Complete stars and reducer:* verify all three lines of F2^2 at each
vertex, all stabilizer permutations and reversal witnesses. Implement
reduction by following the first direction toward the input lattice
and applying its quaternion transport; the distance drops by one at
each step. Return the exact quaternion word and all cocycle values.
Refine D109's same Hensel root when a residue decision needs more
precision. Do not assume its frozen 180-digit center suffices for
arbitrarily long words. A connected fundamental subtree and group
presentation are not additional deliverables.

*Harmonic outcome:* 376 integer relations on 174 outgoing slots have
rank 158 and a 16-dimensional kernel. Exact products and ranks modulo
101 independently certify a basis with integer coefficients of
absolute size at most four. There are 155 oriented edge orbits,
nine inverted orbits and 73 reversal pairs. Inverted edges have zero
scalar harmonic value, also at residue characteristic two. Stabilizer
invariance and the reducer extend the basis to actual G-invariant
cocycles on the whole tree. Boundary-ball masses are integral, so the
chosen measures have uniform denominator bound d=0. No saturated
integral cohomology basis is claimed.

*Validation and audit:* six complete sample stars through depth 32
check reversal and harmonicity; eight sample edges have nonzero values.
Nonzero values are invariant under u, W and h. A shortened root center
refines from error 28 to 48 and recovers the full-precision answer.
Altered cocycle and nonadjacent-input controls are rejected. Minimum
frame/stabilizer/neighbor errors are 166/162/160. All five bounded jobs
pass on first attempts in 29.86/9.19/6.59/15.01/15.22 seconds. Review
406 binds 661 sources and preserves all 643 D110 hashes. Freeze
sources 403--406 and bound artifacts; recheck with 406 --check through
runner 272 and the 180-second process-group cap.

*Next bounded task:* certify W's dyadic fixed points and a coordinate
change to beta^2=-(2+b). Match the embedding and its orientation to
the saved seventeen CM labels and rational residue frame using
arithmetic/reciprocity evidence. W's quadratic equation alone does not
match labels. Then use the resulting charts for a small actual moment
pilot with a proved error/contraction bound over the ramified K.
Direct exponential Riemann refinement is not the high-precision plan.
The bound d=0 now enters D108's conditional tails, but actual moments,
cofactor normalization, a Gaussian pivot and dyadic equality thresholds
remain separate gates. Qp control theorems are not imported unchanged.

No actual moment bank, dyadic CM/frame match, tangent/jet, candidate
identification or target polynomial has been obtained. D99's
nonhyperelliptic conclusion and D108's spectral rejection remain in
force. Retain all enumeration, Hecke-bank and cubic-precision pauses.
Downstream marking, global sections, norm-97 separation and target-scale
torsion remain separate. Decisions, references and all seven entry
documents are current. No correspondence was sent.


**D112 (2026-09-25). Certify dyadic CM coordinates, arithmetic labels and the residue frame; compute chart zeroth masses.**
The user authorized continuing with “keep going!”. Report:
[dyadic-cm-matching-d112.md](dembele/certificates/dyadic-cm-matching-d112.md).
The bounded CM matching task after D111 is complete.

*Reuse the existing arithmetic:* use W and both normalized signs of
the eight ordinary inverted edges 152,155,158,161,164,167,170,173.
No class census, new level or Hecke prime is added. Source 407 proves
that every embedding contains the full O_M in R, and supplies exact
matrices S satisfying A*S=S*[0,-(2+b);1,0]. The point S*(beta:1)
has CM eigenvalue beta. Lattice-error bounds are 173 at W and 166
otherwise, with exact splitting coefficients retained; these are
not affine-coordinate error bounds after arbitrary divisions.

*Identify the anchor geometrically:* k=ij belongs to O*, has norm
one and anticommutes with W. It exchanges W's eigenlines, making
their quotient point inertia-fixed. The principal prime (beta)
splits completely in H/M, so the local decomposition action equals
inertia; its order-two subgroup over K has one fixed point on D.
Equivalently, f_L has one Q2-root with v2=1 and sixteen roots of
v2=1/16, which cannot lie in K. W is the unique K-rational CM point.
The torus-unit argument gives exact stabilizer order two, so this
does not confuse the ordinary CM divisor with P32.

*Fix the branch and Artin convention explicitly:* choose the H-place
taking saved reference root 2 to the unique rational dyadic root,
and normalize the local M embedding by W's eigenvalue character.
Changing beta's local sign conjugates point and root labels together.
For u=1 at W and u=v+W otherwise, certify v*u=u*W and
iota_W(a)R=u^(-1)R. Arithmetic Artin(a) therefore sends P to uP.
The interpretation uses canonical CM reciprocity and prime-to-p
equivariance of the adelic uniformization, with its local character
specified. State these theory inputs and the localized derivation;
neither W's quadratic equation nor numeric root ordering establishes
the labels. No inert-Qp CM theorem is applied to the ramified extension.

*Export replayable class witnesses:* source 408 supplies exact
principal relations a=z*(31,beta+16)^c for all seventeen entries.
The norm products are 1 at W and 128 otherwise, proving the needed
localized right-ideal equalities together with inclusion. The
relative classes are
[0,15,2,7,10,1,16,5,12,8,9,11,6,13,4,3,14]. They cover C17 and
prove the resulting points are distinct. Another principal witness
shows that sigma(beta)=beta^3+3*beta acts on the class group by 10.

*Certify local root orientation independently:* Magma 409 only
proposes centers. Rational review 410 proves all seventeen Hensel
disks, error at least 688 beta-digits and separation at most 17.
Sigma has one fixed root and one 16-cycle. D105's affine Galois group
and the exponent-10 conjugation action determine the regular C17
subgroup up to generator. D107's exact cubic resolvent then selects
the unique arithmetic class orientation. An inverse-Artin control
and an altered-root control fail as required. This avoids treating
an arbitrary local permutation as a certified global Galois action.

*Frame and moment boundary:* evaluate exactly the saved sixteen
trace-centered basis polynomials at all matched roots, with rigorous
error at least 384 beta-digits = 192 pi-digits = 24 binary digits.
These are algebraic residue-frame entries, not actual harmonic
differential values or the change-of-basis matrix. At the rational
anchor eta1=theta-2/17 has v2=7, or v_beta=112. Use this cancellation
in subsequent division bounds. The 51 certified CM boundary charts
give actual zeroth moments A0=0 and B0+C0=0 for every measure;
some B0 values are nonzero. No positive-degree moment is obtained.

*Audit outcome:* sources 407/408/409 pass first attempts in
11.46/5.77/1.54 seconds. The first review probe failed after 24.51
seconds on an incorrect expected anchor valuation, with no result
artifact. Preserve its exact source snapshot, receipt and log.
The corrected independent probe passes in 29.90 seconds; final
review 410 binds 682 sources and preserves all 661 D111 hashes.
Freeze sources 407--410 and bound artifacts; recheck with 410 --check.
All computations use runner 272 and its 180-second process-group cap.
The report and ledger distinguish checked arithmetic from geometric
theory input, and attribute Voight's CM law and Dembélé's adelic
uniformization precisely. D99's nonhyperellipticity is unchanged.

*Next bounded task:* derive finite transport/recursion for
positive-degree moments in these actual CM charts and prove its
truncation/contraction bound over ramified K; then perform a small
actual moment pilot. D111's d=0 and the chart labels now enter
D108's conditional formulas. Direct exponential Riemann refinement
is not the high-precision plan. Do not transfer Qp control constants
or inert-31 equality thresholds unchanged. The actual change of
basis, cofactor normalization, a Gaussian pivot and dyadic equality
thresholds remain later gates.

No actual Shimura jet, candidate identification or target polynomial
has been obtained. Keep D108's spectral rejection and all census,
new-level, Hecke-bank and cubic-precision pauses. Downstream marking,
global sections, norm-97 separation and target-scale torsion remain
separate. Decisions, references and all seven entry documents are
current. No correspondence was sent.


**D113 (2026-09-25). Prove finite positive-moment contraction over ramified K and execute an actual bounded pilot.**
The user authorized continuing with “keep going!”. Report:
[dyadic-moments-d113.md](dembele/certificates/dyadic-moments-d113.md).
The next bounded moment task after D112 is complete.

*Finite recursion instead of growing tree partitions:* attach an
O_K coordinate H_e to each of the existing 174 edge slots. The
saved transport t_e brings its target vertex to a saved local frame.
Exactly two outgoing target slots f yield maps
H_e^(-1)*iota(t_e^(-1))*H_f covering the two residue balls. Retain
all slots, including stabilizer redundancy, rather than introduce
new orbit-representative conventions. Source 411 certifies all
348 maps in the exact D109 splitting algebra, with normalized
coefficient errors at least 159. All zeroth mass relations agree
with the sixteen actual harmonic cocycles.

*Ramified-field proof:* normalize each child map to
phi=b+delta*x/(1+c*x), with v_pi(delta)=1 and v_pi(c)>=1. Binomial
expansion gives v_pi([x^k]phi^n)>=k for every positive n and k.
The exact moments therefore satisfy m=b+T*m after fixing their
zeroth masses, and T gains one pi-digit. D111's d=0 bounds every
moment integrally and justifies termwise integration. Cutoff J,
N iterations and working precision P give error min(J+1,N,P).
The same contraction makes a zero residual modulo pi^P a uniqueness
certificate. This proves the needed scalar statement directly;
do not apply a Qp overconvergent control theorem outside its field
hypotheses. Attribute the moment-lifting framework to Franc--Masdeu,
section 6.1, and the general tree coordinates to Masdeu--Torrents.

*Actual bounded computation:* source 412 takes J=11 and N=P=12.
It produces 33,408 moments, with successive differences of valuations
0,...,11 and zero final residual. Exact bit-plane arithmetic uses
power coefficients modulo 4 for indices 0..3 and modulo 2 for 4..7,
and pi^8=-2 modulo pi^12. This retains v_pi(2)=8. The helper is
restricted to P<=16; extending it beyond that requires the full
Eisenstein polynomial, not the unchanged pi^8=-2 shortcut.

*CM transfer:* the existing reducer and D112 charts give 51 exact
ball isomorphisms, with normalized errors at least 165. Their
determinant valuation is zero and denominator slope lies in pi*O_K.
Thus the n-th power has coefficient bound max(0,k-n), giving
transferred error min(P,J+1-n). The first three positive CM moments
have errors 11,10,9. All zeroth masses recover D112. There are
2043 certified nonzero entries among the 2448 positive CM entries.
Every one of the 144 W-anchor entries is zero modulo its error
bound. Do not promote these enclosures to exact vanishing, an anchor
normalization, a differential value or a projective tangent.

*Independent audit:* source 413 reconstructs every exact matrix,
checks all quaternion words and partitions, and replays the complete
moment residual and CM transfer using ordinary integer polynomial
convolution and matrix multiplication. This is separate from the
pilot's bit-plane arithmetic. A unit perturbation of a positive
moment is rejected. Independently reduce 32 depth-three leaf balls
in W's three charts and CM index 1's B chart, and compare all 192
degree-1,2,3 scalar Riemann sums modulo pi^3. This fixed sample is
validation, not the high-precision algorithm.

Transport / pilot / probe / final review pass first attempts in
6.18/1.32/5.83/6.12 seconds under runner 272 and its 180-second
private-process-group cap. Review 413 binds 696 sources and preserves
all 682 D112 hashes. Freeze sources 411--413 and bound artifacts;
recheck with 413 --check using Python/NumPy, without Sage or Magma.
No floating-point solve or numerical tolerance enters this certificate.

*Next bounded pilot:* target T=16 pi-digits for D108's first coarse
Poisson coefficients. Sufficient parameters are CM moment cutoff 31,
state cutoff 46, precision P=16 and 16 contraction iterations.
This combines the transfer loss with the conditional coarse tail;
it is not a candidate-identification threshold. The coefficient
bound is uniform in the row degree, and columns k>=P vanish modulo
pi^P. Thus first solve moments 0..P-1, then obtain higher state
moments through 46 by one row evaluation against that solution.
Implement this in a new source, retaining the frozen pilot. Evaluate
actual coarse differential coefficients with all errors propagated,
and certify a nonzero value at W before any normalization. If this
precision is insufficient, report the resulting enclosure rather
than divide by an unresolved zero. Larger working precision requires
extended quotient arithmetic; beyond the saved splitting bounds,
refine the same exact Hensel branch with new certificates.

Actual harmonic-to-residue change of basis, cofactor error propagation,
a Gaussian pivot, final-scale runtime and dyadic equality thresholds
remain later gates. No actual differential value/jet, candidate
identification or target polynomial is obtained here. D99's
nonhyperellipticity and D108's spectral rejection stand. Keep all
expanded-census, new-level, Hecke-bank and cubic-precision pauses,
with no transfer of the inert-31 thresholds. Downstream marking,
global sections, norm-97 separation and target-scale torsion remain
separate. Decisions, references and all seven entry documents are
current. No correspondence was sent.


**D114 (2026-09-25). Evaluate actual coarse differential jets and prove the W-anchor precision gate.**
The user authorized continuing with “continue!”. Report:
[dyadic-coarse-d114.md](dembele/certificates/dyadic-coarse-d114.md).
The bounded Poisson pilot after D113 is complete. All sixteen
actual harmonic differentials have certified coarse coefficients
through order two at all seventeen matched CM points, in the
specified u=((z-beta)/(z+beta))^2 coordinate. This is an actual
harmonic-basis differential 2-jet. Rational-residue-frame ratio
jets and the basis change remain separate requirements.

*Recover high moments from the low fixed system:* at precision P,
child-map coefficients in columns k>=P vanish uniformly in the
row degree. Source 414 solves only degrees through P-1 and then
evaluates higher rows once. With P=16, low cutoff 15, iterations
16, state cutoff 46 and CM cutoff 31, it produces 130,848 state
entries and 26,112 CM entries with errors at least pi^16. All
frozen D113 state entries agree on overlap. This implements the
proved contraction without enlarging the fixed system or tree census.
The bit-plane quotient remains restricted to its proved P<=16 range.

*Combine coarse kernels before arithmetic:* source 415 substitutes
the CM chart expansions into D108's exact Taylor-to-coarse formula.
Its integral coefficients avoid division by an approximate beta;
the full CM polynomial supplies arithmetic modulo beta^80. Keeping
the binomial valuations improves the initial errors to 24,32,24
pi-digits. The three-chart artifact certifies 250 nonzero entries
per order and remains frozen with these original bounds.

*Use the actual CM symmetry to sharpen the certificate:* review
416 independently expands K_j(t)=(1-((beta+t)/(beta-t))^(2j+2))/2
in all three charts. Separate integer arithmetic modulo beta^96
pays for division by two, retaining beta^80 precision and checking
all 288 kernel coefficients. A changed infinity-kernel sign is
rejected. The embedded CM involution exchanges A=pi*O_K with its
complement and preserves both the kernel and actual measure.
Thus g_j=2*integral_A K_j dmu exactly. The constant coefficient
vanishes and the positive coefficients have factors 4,8,4 for
orders 0,1,2. The resulting errors are **32,40,32 pi-digits**.
All **256 non-anchor entries per order** are certified nonzero.
Use `certificates.Poisson.symmetry_refined_CM_values` in the final
review artifact, preserving the specified basis and local coordinate.
The refined and original three-chart enclosures agree.

*Raise precision rather than only degree at W:* the computed
A-chart moments of degrees 0..31 all vanish modulo pi^16 at W.
Since x^2-x is divisible by pi on O_K, Q(X)=(X^2-X)^16 is monic
of degree 32 and takes values in pi^16. Monic division of any
integral polynomial by Q, together with the measure bound d=0,
proves all polynomial moments divisible by pi^16 at every degree.
The twice-A expansion then proves anchor valuation lower bounds
**32.5,40.5,32.5 in v_pi**. These do not prove exact vanishing or
nonvanishing. More degrees at the same working precision cannot
produce a usable anchor. No normalization is performed.

*Independent audit and provenance:* review 416 checks every state
residual and CM transfer using separate binomial/convolution
arithmetic, then checks the kernels, coarse values and involution
comparison. Sources 414/415 pass first attempts in 4.59/0.40 seconds.
The first review probe fails in 1.64 seconds on an implementation
type mismatch: a NumPy integer lacks bit_length. Its exact source,
log and receipt are archived; it wrote no result artifact. Converting
to a Python integer fixes it without weakening any assertion.
Probe two/final review pass in 1.69/2.16 seconds. The review binds
**713 sources**, preserving all **696 D113 hashes**. Freeze sources
414--416 and bound artifacts. Use runner 272, private process
groups and the 180-second cap, including for 416 --check.

*Next bounded pilot:* raise moment precision to **24 pi-digits**,
initially evaluating W's A chart using the twice-A formula. Use
low cutoff 23, 24 iterations, state cutoff 70 and CM cutoff 47.
The coarse design errors are at least 40,48,40 pi-digits; this
does not guarantee anchor nonvanishing. Implement the full
Eisenstein quotient in a new source: pi^8=-2 omits the -20*pi^4
term of valuation 20 and is invalid at precision 24. Retain the
defining polynomial pi^8-8*pi^6+20*pi^4-16*pi^2+2 and all terms
relevant at the chosen precision. Use CM precision at least
beta^96, with extra digits for independent divisions. Reuse the
low-system/high-row optimization and existing normalized transport
centers (errors 159/165), checking overlap with the precision-16
bank. No new splitting branch or tree census is needed. Keep the
180-second cap and do not divide by an unresolved anchor.

After anchor nonvanishing, actual harmonic-to-residue frame change,
cofactor propagation and a Gaussian pivot remain separate. Dyadic
height/equality thresholds and final-scale performance are still
needed before identification; inert-31 thresholds cannot be copied.
The target polynomial remains unconstructed. D99's nonhyperellipticity
and D108's spectral rejection stand. Keep all expanded-census,
new-level, Hecke-bank and cubic-precision pauses. Downstream marking,
global sections, norm-97 separation and target-scale torsion remain
separate. Decisions, references and all seven entry documents are
current. No correspondence was sent.


**D115 (2026-09-25). Reassess the route, complete the actual two-order comparison, and make exact identification the next priority.**
The user requested a strategic reassessment and sustained execution
without repeated approval stops. Report:
[dyadic-comparison-and-strategy-d115.md](dembele/certificates/dyadic-comparison-and-strategy-d115.md).
The dyadic route is retained because it now independently reaches the
actual rational residue frame and two ratio orders. All 512 comparisons
at the sixteen non-anchor CM points agree with the candidate within
beta-error bounds **101/70**. This supports the proposed comparison;
it does not prove exact curve identification or construct the field.

*Work through the comparison, rather than stop at an anchor pilot:*
resolve W, compute the actual projective frame, certify the ratio
parameter, then compare candidate coefficients. Candidate data enter
only after the actual frame is constructed. A certified mismatch
would refute this branch; a match must be judged against an exactness
criterion. The computation proceeds through this chain without asking
for approval at each precision step.

*Full quotient arithmetic and bounded refinement:* sources 417--429
use the entire Eisenstein polynomial, solve only low moments, and
recover higher rows afterward. A previous bank seeds the calculation
after restoring exact zeroth masses. The first two failed probes
catch that initialization mistake; both are archived. Propagating
the homogeneous correction allows omission of columns k>=P-v(delta).
Batched operators, separate capped phases and reduced intermediate
storage reach working precision 200. All earlier overlaps pass.
The final bank has 1,667,616 state entries through degree 598 and
108,800 CM A-chart entries through degree 399.

*Refine the same arithmetic input:* after P=152 the old center bounds
159/165 are insufficient. One Newton step on the same D109 root gives
error 352 and normalized child/CM errors 331/337. Exact matrices,
transports, partitions and labels are preserved. Two archived probes
expose the finite v(0) sentinel when testing exactly unchanged matrices;
testing exact equality first resolves it. No bound or mathematical
assertion is weakened, and no new tree or class census is run.

*Resolve W and construct the actual rational frame:* the first W
leading coefficient has v_beta=296, first resolved at P=136. At P=200
all 816 harmonic coarse entries are certified nonzero, with beta-errors
432/448/432. Normalize leading rows to h_i, put D=h_nonanchor and
q=h_W*D^(-1), and take M=D^(-1)*diag(q_i^(-1))*E_nonanchor. All pivots
and q_i are certified nonzero. The trace-zero residue rows E_i give
h_i*M=E_i/q_i and h_W*M=-E_W. D106 identifies this projective basis
with the rational residue frame, up to one common scalar.

*Certify the ratio chart and compare two orders:* the chosen Gaussian
G12 has valuation 153 and error 254 at each non-anchor point. The
ratio parameter t=omega_2/omega_1-(omega_2/omega_1)(P) is therefore valid
there. Rationality and CM transitivity imply nonvanishing throughout
the CM divisor. W's Gaussian remains numerically unresolved at error
825, and no division by its local enclosure is performed. The first
and second ratio coefficients have candidate-difference valuations
at least 101 and 70 in v_beta, or 50.5 and 35 in v_pi. Source 430
checks the formulas by direct series division and parameter reversion.
The sixteen points belong to one degree-16 dyadic place; they are
not sixteen independent places for the product formula.

*Quantify the remaining equality gap:* source 423 derives dyadic
thresholds from D106's actual-minus-candidate heights using exact
rational bounds on log(2). At the degree-16 place, orders 1/2 require
sufficient beta-errors **274241/820774**, or integer pi-errors
**137121/410387**. Comparing both places with a common bound would
give smaller thresholds, but that W ratio precision is unavailable.
These are sufficient bounds, not lower bounds on every possible method.
The achieved comparison does not activate the exact J3 rank-45 test.

*Revised plan:* retain the route and candidate, but stop treating
another routine precision increase as the default next task. The
binding objective is an exact arithmetic identification certificate:
either an effective substantially sharper bound on the actual unknown
coefficients, or an exact identity/correspondence with proved uniqueness.
No replacement certificate is supplied here. Candidate-only height
bounds, extra matching primes and additional finite Taylor agreement
are insufficient. This is a mathematical gap, not a request for approval.

After exact base identification, certify the P32/B3 markings and
double-cover character, then apply the conditional nine-cover shortcut
and construct exact global genus-64 cubic/section data. Norm-97
isolation, combined torsion scaling, the specified F256 subspace and
a separating degree-257 invariant remain separate requirements. The
target field polynomial remains unconstructed.

Review 431 binds **814 sources**, preserving all **713 D114 hashes**.
Independent moment/kernel and formal-series reviews pass. Before the
final audit, 24 jobs pass and four implementation probes fail with
complete archives. No job times out; the longest takes 145.02 seconds.
Freeze sources 417--431 and bound artifacts. Recheck 431 --check through
runner 272 and its 180-second private-process-group cap. Keep D99's
nonhyperellipticity, D108's spectral rejection, and all census, new-level,
Hecke-bank and cubic-precision pauses. Decisions, references and all
seven entry documents are current. No correspondence was sent.


**D116 (2026-09-26). Prefer direct integral quadratic-section vanishing, complete its local inputs, and retain an explicit exactness gap.**

The user authorized continuing the reassessment without approval stops.
See [the proof and plan](dembele/certificates/cm-compound-height-d116.md)
and [the source ledger](dembele/data/computed/cm_compound_sources_d116.json).

*Remove avoidable determinant factors:* Jacobi's integral compound
identity reduces exterior products of adjugates. Together with the
Gaussian/Wronskian identity this sharpens actual ratio heights. The
stable-model residue argument, harmonic saturation and unimodular
weighted graph cycles identify the actual integral differential basis.
Canonical generation gives fibre exponents 296/33 and cofactor valuations
280/245, with Delta valuation 4200 and common section factor 3920.
The evaluation defect 245 is not the horizontal CM residue-map index.

*Account for finite common zeros:* the principal dyadic prime of M
splits completely in H/M. Equivariance averages the seventeen CM
valuations over those primes. Reduced Gaussian and second-ratio common
contents lower actual heights below 4723/19438 and sufficient ratio
beta-errors to 132444/524481, versus achieved 101/70. W's unresolved
Gaussian is never inverted.

*Change the primary exactness test:* for any candidate quadric through
all seventeen frame points, Q(s)/Delta is an integral quadratic section.
An adjacent-pair complementary-minor identity gives norm below 2^4855.
If preceding jets are exactly zero, the next divided jet is integral
even at a nodal specialization. With measured anchor bounds, successive
non-anchor beta-valuations 119806/120284/120758 suffice for exact zeros.
Then 4D has degree 68>60, and D88/D69 identify (C,D), without the separate
J3 rank-45 prerequisite. This proof supersedes source 441's earlier
147023 sufficient direct bound; its artifact remains frozen.

*Complete the required local orders:* source 442 computes the third
actual coarse coefficient from the existing P=200 moment bank. The
four errors are 432/448/432/448 beta-digits; all 1088 coefficients are
certified nonzero. Source 443 evaluates every quadric through order
three at all seventeen points. Achieved non-anchor lower bounds are
3794/3745/3728 and anchor lower bounds 3576/3248/2984. Every residual
contains zero; no positive-order exact vanishing follows. The higher
intrinsic-jet interpretation remains conditional on preceding exact
zeros, and these valuations are not ratio error digits.

*Keep the diagnostic claims separate:* actual J3 rank is at least 33.
Candidate-centered trials predict rank 45 after +96 beta-digits but
are not actual precision data. The rank result is not an independent
proof of nonhyperellipticity because the rational-frame descent already
uses D99. No small precision increase closes the remaining section
valuation gap of 116012--117030.

*Next research task:* sharpen the norm/content estimate for the actual
reduced quadric tensors using the explicit formula, or find an exact
arithmetic identity with a uniqueness proof. If a large precision run
becomes the selected alternative, first prove limb-safe arithmetic,
transport/Hensel accuracy and a bounded memory/time phase plan. The
current fixed-width implementation cannot simply be extrapolated.
Candidate-only heights and further finite matches do not replace
the exactness argument. Retain the ratio certificate as a fallback.

Review 445 binds 868 sources, preserves all 814 D115 hashes and checks
lattice witnesses, third coarse coefficients, 4641 positive quadratic coefficients and
the logarithm budgets independently. All thirteen input jobs and the
final calculation probe, final review and recheck pass within the
180-second cap. Freeze sources
432--445 and bound artifacts. Use 445 --check through runner 272;
435/440 are probe-only predecessors with superseded draft build counts.
No candidate identification or target field polynomial is proved.
P32/B3, the double-cover character, global genus-64 sections, norm-97
isolation, combined torsion and the degree-257 invariant remain separate.
Keep D99, D108's spectral rejection and every existing resource pause.
All seven entry documents and references are current; no correspondence
was sent. Earlier next steps are historical.


**D117 (2026-09-26). Certify uniform large CM disks, quantify their benefit, and move the exactness work to finite arithmetic corrections.**

The user authorized continued autonomous execution. See
[the proof and revised plan](dembele/certificates/cm-disk-and-exactness-d117.md)
and [the source ledger](dembele/data/computed/cm_disk_sources_d117.json).

*Strengthen the uniform disk without a group census:* for a norm-one unit
alpha, the commutator trace is integral in F and has seven conjugates in
[-2,2]. A complete 6167-vector weighted trace-lattice search excludes an
outlier in (2,8]. More strongly, alpha+beta*alpha*beta^(-1) is integral
in M, with seven squared absolute values at most four. A complete
376935-vector Hermitian trace-lattice search excludes an outlier in
(4,64]. This forces displacement >2*acosh(4), uniformly over the CM
points and conjugates, and certifies an open disk with radius squared
3/5 modulo the order-two stabilizer. No sufficiency claim for arbitrary
lattice elements as quaternion units is made.

*Recompute the actual section budget:* retain D104's exact rational
Hodge-height upper endpoint and the pi factors in D116's complementary-minor
norm. The new sufficient non-anchor beta-valuations are
**35947/36096/36237**, down from 119806/120284/120758. Actual lower bounds
remain **3794/3745/3728**, with anchor bounds 3576/3248/2984. These are
section valuations, not ratio errors or working precision. The higher
integral-jet hypotheses still require preceding exact zeros. No positive
jet is proved exactly zero, no curve is identified and no field polynomial
is constructed. The preliminary radius-9/19 bounds remain frozen; use
source 449's final budget.

*Close the radius-only branch of the reassessment:* even the optimistic
rho=1 substitution leaves sufficient thresholds 32928/33064/33193 when
the other inputs are fixed. This is a limitation of this bound, not a
universal precision lower bound. Further radius work alone cannot certify
the current data. The remaining actual valuation gap is 32153--32509.

*Select the next bounded arithmetic task:* D104 gives
H_CM=2*h_L(Q)+log(2)-2*c_L-c_ram, where c_L is the Hodge/stable fibre
height difference and c_ram is the finite zero degree of D_Q(df).
Recover proved dyadic contributions using the stable upstairs cover and
compatible Hodge lattices. Prove its nodal generators and stabilizer
thicknesses before assigning integral derivative content. Neither correction
has been computed; the evaluation defect 245 is not a substitute. Assess
the resulting gain and any required stronger h_Fal lower bound before
selecting more precision. An exact identity with proved uniqueness remains
an alternative; candidate-only heights and finite matches do not suffice.

*Retain the computational gate:* the present dense state alone has an
ideal packed storage count over 104 GB at P=10000, before operators and
temporaries. This example is not a prediction of required P or a lower
bound on other algorithms. Any large run needs a different costed design,
proved limb arithmetic and refined transport/Hensel inputs under the
existing 180-second cap. No moment precision is increased in D117.

Review 450 independently checks support-pattern enumerations, multiplication
traces, root sign changes, interval recurrences and a different logarithm
series. It binds **891 sources** and preserves all **868 D116 hashes**.
Four input jobs pass; one decimal-serialization failure is archived with
its source, log and receipt. Certified outward rounding fixes it without
weakening assertions. The independent probe and final review pass in
7.536/9.031 seconds, and the reproducibility recheck passes in 9.527 seconds.
Freeze sources 446--450 and bound artifacts; recheck
450 --check through runner 272. D99 nonhyperellipticity, D108 spectral
rejection and all census, level, Hecke and cubic pauses stand. Markings,
the double-cover character, genus-64 sections, norm-97 isolation, target
torsion and the degree-257 invariant remain downstream. All seven entry
documents and references are current. No correspondence was sent.


**D118 (2026-09-26). Complete the combined dyadic fibre correction, add the exact tropical Faltings term, and test a different integral frame next.**

The user authorized continuation. Read
[the proof and next task](dembele/certificates/cm-finite-height-d118.md)
and [the source ledger](dembele/data/computed/cm_finite_height_sources_d118.json).

*Compute the two finite corrections together:* on an auxiliary small-level
model maximal at 2, the arithmetic Hodge fibre is the relative dualizing
fibre. The chain rule identifies the composite derivative W_C -> L(Q)^2
with the original ramification derivative followed by the square of the
Hodge/stable comparison. In the actual CM coordinates, dz/z=2dw/(1-w^2)
and u=w^2, so an integral generator beta^m_i du gives derivative coefficient
beta^m_i/2 up to a unit. The exact contents are [280,17x16]. This includes
the anchor without assigning an unproved generator to its coarse quotient.
No auxiliary level computation is run; this is a geometric proof device.

*Apply the finite degree:* the seventeen dyadic primes and CM orbit give
(280+16*17)*log(2)/272=(69/34)*log(2). Therefore
H_CM<=2*h_L-(35/34)*log(2)<8/3. The combined dyadic correction is fully
computed, while its Hodge and ramification summands and the non-dyadic
corrections remain separate unknowns. Splitting the sum cannot add more
dyadic gain. The evaluation defect 245 is not one of these corrections
or the D102 residue-map index.

*Improve the Faltings lower bound from existing arithmetic:* the
de Jong--Shokrieh formula applies in the matching determinant L2 metric.
The known graph has length 76, tau=67889/27075 and tropical moment
223268/27075. Its normalized dyadic contribution is (55817/54150)*log(2),
giving h_Fal(C)>-23.146371 after dropping the other nonnegative terms.
No new graph, census, level or Hecke data is needed.

*Update the exactness certificate:* the sufficient section valuations are
**25330/25444/25551**, versus actual **3794/3745/3728** and anchor bounds
3576/3248/2984. Source 454 is current; source 452's fibre-only bounds
27633/27747/27854 remain frozen as an intermediate result. The higher
intrinsic jets require preceding exact zeros. No positive jet, exact
candidate identification or field polynomial is proved.

*Measure the remaining limitation:* the valuation gap is 21536--21823;
the fixed-input radius-one limits are 22310/22412/22506. If only h_Fal
were improved, a proved lower bound 37 would suffice for all three tests,
but that bound is not established. Known common vertical content already
included in the measured zero degree cannot be subtracted a second time
as a new height gain.

*Next bounded research task:* test a lower-degree integral CM frame using
D102's principal-parts sequence. First construct/check an actual model
where the CM divisor is finite flat Cartier, record its intersections,
and verify the principal-part norm and cohomology torsion terms. The
stable evaluation matrix alone does not supply these hypotheses or its
index. The goal is to see whether this changes the large CM-fibre power
in the bound; no improved replacement has been proved. Keep exact
arithmetic identities with uniqueness as an alternative, and retain
the current section criterion as a fallback. A larger precision run
still requires a costed, limb-safe design and transport refinement.

Review 455 revalues all 272 leading coefficients, verifies the grounded
graph inverse by multiplication, independently integrates resistance
derivatives at all thirty basepoints, and rechecks the bounds with a
separate logarithm series. It binds **911 sources**, preserving all
**891 D117 hashes**. All four input jobs pass first attempts; the probe
and final audit pass in 4.396/5.784 seconds; the reproducibility recheck
passes in 6.336 seconds. Freeze sources 451--455
and bound artifacts; recheck 455 --check through runner 272 and the
180-second process cap. The P=200 data, D99/D108, every existing
resource pause and all downstream cover/field requirements remain.
All seven entry documents and references are current. No correspondence
was sent; earlier next steps are historical.


**D119 (2026-09-26). Establish the actual Cartier CM divisor and its dyadic residue index before testing the intrinsic frame's height budget.**

The user authorized continuation. Read
[the proof and next task](dembele/certificates/cm-cartier-frame-d119.md)
and [the source ledger](dembele/data/computed/cm_cartier_frame_sources_d119.json).

*Model and divisor:* use the minimal regular semistable model obtained
by resolving D99's quotient nodes and contracting its rational tails.
The anchor ends on component 6; the eight ordinary pairs are on the
retained components 51--58 (one-based labels). At each ordinary edge
the endpoint stabilizer is trivial and the quotient parameter is t=x-y,
where xy=2+b and the involution is (x,y)->(-y,-x). The two sections have
t=+/-2*beta, hence intersection length 33. Different pairs and the anchor
are disjoint. Keep these intersections rather than assuming split
etale reduction. Their sum is finite flat Cartier with algebra
R x product_8 R[t]/(t^2+4*(2+b)), normalization index 264 and discriminant
valuation 528. This order is not the abstract degree-17 field order.

*Actual principal parts:* in the pair basis 1/F(t), (t+2*beta)/F(t), the
restriction rows are (h_plus+h_minus)/(16*beta^2), h_plus/(4*beta).
Use h_W/beta^296 at the anchor. Source 456 evaluates this matrix from
the frozen P=200 bank. Its Smith valuations [0x9,2x7] give H1 torsion
length 14, and its cofactors have valuations [16,14x16]. The primitive
principal part has value valuations [2,0x16], hence norm valuation 2.
D102 now gives the actual residue index valuation **16=14+2**. Direct
composition yields Smith values [0x8,2x8], so **beta^2 kills the cokernel**
and clears the local eta frame for a primitive pencil generator.

The normalized dyadic residue-index contribution is log(2), split into
(7/8)*log(2) from torsion and (1/8)*log(2) from the norm. Neither the
earlier evaluation defect 245 nor a field-order discriminant determines
this index. A separated-model control instead gives torsion/norm/index
740/68/808; these quantities cannot be transferred between models.

*Height assessment:* with the residue-coordinate metric on N and its
induced metric on Lambda, taking determinants gives
h(Lambda)=h(det N)+h_Fal+tau-average log vol(delta), and
h(det N)=-sum H_CM+I, where I is the unordered intersection sum.
The proved dyadic I+tau is (139/8)*log(2). D117's row bound then gives
a lower bound for Lambda, recorded in the report. This is not yet an
inverse-map or quadric height bound. No global scaling of h or non-dyadic
residue indices have been computed, and the existing exactness budget
does not change by replacing 245 with 16.

*Next bounded task:* derive the full quadratic-section bound in the
intrinsic residue frame, with the actual codifferent, beta^2 clearing,
pencil-line bound and consistent archimedean norms. Compare degree minus
measured zeros with D118 before adopting it. If there is no gain, reject
this replacement and return to the exact-identity alternative or a costed
precision design. Already counted vertical zeros cannot be subtracted
again. Keep D118's sufficient valuations **25330/25444/25551**, actual
**3794/3745/3728**, and all preceding exact-zero hypotheses.

*Verification:* 457 independently reconstructs 272 entries using integer
polynomial quotients, checks all 17 maximal minors and the primitive
kernel, and computes the residue map's Smith factors directly. The first
456 run failed on a wrong expected graph-pruning count; its source, log
and receipt are preserved. The corrected run passes in 3.882 seconds,
probe/final review in 2.642/4.159 seconds; the reproducibility recheck
passes in 4.622 seconds. The audit binds **922 sources**,
preserving all **911 D118 hashes**. Freeze sources 456--457 and bound files;
recheck through runner 272, one BLAS thread and the 180-second private
process-group cap.

No positive quadric jet, candidate identification or field polynomial
is proved. The P=200 data, D99 nonhyperellipticity, D108 spectral rejection,
all resource pauses and downstream marked-cover/field tasks remain.
Decisions, references and all seven entry documents are current.
No correspondence was sent.


## 2026-09-26 — D120: reject the inverse-frame estimate and execute a costed alternative

The user requested a reassessment, then authorized proceeding with the
best approach without further approval. Read
[the complete proof and plan](dembele/certificates/construction-reassessment-d120.md)
and [the source ledger](dembele/data/computed/construction_reassessment_sources_d120.json).

*Decision:* retain D118's direct integral quadratic-section certificate.
The complete D119 inverse-frame norm costs more: sufficient valuations
43459/43553/43642 versus measured 154/105/88 in that frame. Its small
local cokernel does not compensate for the inverse determinant. Odd-prime
indices cancel with Fitting-ideal clearing; no global scalar is guessed.
The normalization comparison removes the old scalar of valuation 3640
from measured zeros, avoiding double-counting. Close this estimate.

Known evaluation minors also give h_Fal<30.970856. Rescuing the current
D118 bound by changing that input alone would require >35.39--36.18,
so close that detour as well. This is a limitation of the current bound,
not nonexistence of the curve or the field. No new exact-identity theorem
was established; the inspected exact-expansion theorem requires exact
input and does not turn current p-adic balls into zeros.

*Executed alternative:* inverse entries are >=-35 in valuation, and
explicit propagation gives conditional sufficient moment P=10552, with
per-order targets 10416/10480/10552. The refined inputs and zero-containing
quadratic enclosures are still required. Dense operators would require
72.75 TB, so 459 replaces them by homogeneous polynomial transport with
arbitrary-integer arithmetic. Its actual P=200 checks cover one harmonic
column, every state and chart, and 332800 scalar coefficients. Synthetic
P=1600 cost exposes Python multiplication as a bottleneck. Source 463
uses installed GMP and integral binomial powers: that case falls from
51.126 to 1.146 seconds, and a synthetic P=10552 action passes in 50.408
seconds. This is a proved component and measured cost, not a full solve.

*Next bounded work:* implement r=1 low-moment elimination on P=200.
The Schur-complement proof improves correction gain to r+1 after exact
elimination. Check the 174-dimensional low-block solve, original full
residual and precision gains; price storage and iterations before a
larger r or actual refinement. The raw packed low-moment payload is
2.424 GB per harmonic column at the proposed P. A naive repetition of
full sweeps remains too expensive. No large actual run is ready.

*Downstream result:* frozen source-58 multiplicities, D51 occurrence and
old/new decomposition force norm-97 target multiplicities one in canonical
Y64 and zero in its old part. Thus both torsion factors are coprime to
their full Euler cofactors. Only the first has order 51, matching the
second T31 target; the other has order 257. One mistaken initial assertion
that both had order 51 was caught, corrected against the already frozen
source-64 output, and fully archived. No Hecke bank was expanded.
The genus-64 degree-51 backend and global F256 action are still open.

*Audit and scope:* seven input jobs pass; one failed expectation is
archived. Independent probe/final review passes in 5.261/6.791 seconds,
binding 961 sources and preserving all 922 D119 hashes. The reproducibility
recheck passes in 7.093 seconds. Freeze 458--463
and bound artifacts. Keep runner 272, one BLAS thread, the 180-second
private-process-group cap, P=200 and every resource pause. Current D118
section thresholds and actual values remain unchanged. No positive jet,
candidate identification or target polynomial is proved. All seven
entry documents, decisions and references are current. No correspondence
was sent; the user need not approve this next bounded implementation.


## 2026-09-27 — low-moment elimination reaches fresh arithmetic data

**D121. Keep the Schur solver, refine a complete column, then address the
remaining transport cost before a target-size run.** Read
[the proof and result](dembele/certificates/dyadic-schur-lift-d121.md) and
[the ledger](dembele/data/computed/dyadic_schur_sources_d121.json).
The integral low inverse exists because its matrix is I modulo pi;
eliminating r positive moments gives gain r+1. Actual low solves pass
on all sixteen columns through r=64, and a whole-column test gains
64 -> 129 -> 194 -> 200. Sparse block LU uses 2246 updates.

Arbitrary-precision FLINT multiplication passes independent controls.
All 399 transport parameters are refined on the certified Hensel branch
to P=10552. An actual r=32 factorization at P=400 passes, followed by
column 0's 200 -> 233 -> 266 -> 299 -> 332 -> 365 -> 398 -> 400 lift.
Every original state equation and old overlap passes. Its seventeen CM
charts and four coarse coefficients then pass, with beta-errors
[832,848,832,864]. This is new actual data, but the other fifteen columns
remain P=200, so the full residue-frame certificate has not improved.

Prepared synthetic target actions still take 26.825 seconds. A complete
target-size sweep is too expensive even with fewer iterations. Next
accelerate polynomial transport, complete all sixteen P=400 columns and
retest the quadrics before larger lifts. Retain D118's section method
and D120's conditional P=10552 target. Review 474 binds 1079 sources,
preserving all 961 D120 hashes. Twenty-one of 24 input attempts pass;
two sentinel-check errors and one premature dependent-stage launch are
fully archived. Freeze 464--475 and bound artifacts. All caps and pauses
stand. No exact positive quadric jet, curve identification or target
polynomial is claimed. Decisions and references are updated; continue
without an approval pause.


## 2026-09-27 — D122: complete the P=400 bank and checkpoint before the comparison

The user authorized continued execution, then requested updated handoff,
decisions and references. Read
[the progress checkpoint](dembele/certificates/dyadic-precision400-progress-d122.md)
and [the source ledger](dembele/data/computed/dyadic_precision400_sources_d122.json).

*Outcome:* all sixteen actual harmonic columns now reach P=400. Sources
476--477 control a compiled FLINT polynomial backend; 478--479 complete
columns 1--15 and all seventeen CM charts, preserving the audited D121
column 0. Final original residuals use the older GMP polynomial backend.
All 155 input jobs pass under separate 180-second process-group caps,
with one BLAS thread. The three batch workers have finished successfully;
no jobs or pause flag remain.

Source 482 consolidates all 1088 coarse values, with beta-errors
[832,848,832,864]. All states have low moments through 399; only nine
CM-target states were extended through 1198, and CM moments through 799.
Source 481 also refines the algebraic CM frame eta to beta-error 21168
on the original root branches. This does not increase harmonic moment
precision beyond P=400. The target-size synthetic action falls to
23.574 seconds plus 1.901 preparation; it remains only a component timing.

*Decision:* finish the actual P=400 comparison and independent review
before choosing another moment precision. Sources **483--484 are drafted
but unrun**, with no output files and no freeze. Run 483 for the actual
residue frame, then 484 for all 91 quadrics and revised anchor-dependent
height bounds, checking each receipt before launching its dependent job.
Record any certified mismatch; agreement has not been assumed. Draft 483
clamps eta error to its working precision, and 484 checks the coefficient
valuation condition used by the integer-scaling shortcut. Keep W's
unresolved Gaussian uninverted. Source 486 is the next unused number for
an independent mathematical review using alternate arithmetic paths.

*Checkpoint scope:* source 485 binds 1844 source hashes, preserving all
1079 D121 hashes and the 155 D122 input receipts. Checkpoint creation
passes in 9.137 seconds and hash replay in 2.195 seconds. These verify
provenance and completion status, not the pending independent mathematical
review. Freeze successful sources
476--482 and completed artifacts, plus the snapshot's bound report/ledger.
Use the persistent `run_dyadic_capped.py` wrapper and fresh receipt names
on resume; temporary runner scripts are no longer required. Exact commands
are at the top of [HANDOFF.md](HANDOFF.md).

No P=400 quadric bound or new exact zero is claimed. D118's accepted
section values 3794/3745/3728 and sufficient bounds 25330/25444/25551
remain current pending that comparison. Higher intrinsic jets require
preceding exact zeros; D99/D108, D120's conditional P=10552 design,
all resource pauses and downstream cover/field requirements stand.
No candidate identification or target polynomial is proved. This is
the user's requested resume checkpoint, not completion of the construction.
All seven entry documents are updated; no correspondence was sent.


## 2026-09-27 — D122 completion: accept the reviewed comparison and stage the next lift

The user asked to continue and raised recurring chat transport errors.
After rechecking the saved manifest, sources 483--484 complete the actual
residue frame and all 91 quadrics through four orders. Source 486 then
passes seven independent arithmetic phases. Read
[the completed report](dembele/certificates/dyadic-precision400-d122.md)
and [the final ledger](dembele/data/computed/dyadic_precision400_review_sources_d122.json).

*Accepted result:* all 6188 quadratic coefficients, including 4641 positive
coefficients, contain zero in their certified balls. There is no certified
mismatch. Section bounds are now 4194/4145/4128, with anchor bounds
3976/3648/3384. The unchanged D118 global budget gives updated sufficient
non-anchor bounds 25305/25419/25526. The 21111--21398 gap remains large;
finite agreement does not prove positive exact vanishing or identification.

W's Gaussian is independently certified nonzero with valuation 1024 and
absolute error 1225. Retire the unresolved-denominator restriction for
this specific ball, while retaining explicit error propagation for any
future division. No Gaussian inversion has been performed. This resolves
a local question without establishing a better global ratio-height bound;
keep the direct integral-section route.

*Independent evidence:* source 486 imports no production arithmetic. It
uses integer quotient Horner products, absolute-error balls, residual
certification of q and the change matrix, alternate CM kernels, and
gradient/polar-form quadratic coefficients. All 1088 coarse values and
6188 quadratic coefficients are checked, along with the roots, eta values,
low-state overlaps and selected original recurrences. Review 487 binds
1884 sources, preserving all 1079 D121 hashes and all 1844 interim hashes.
All 167 input jobs pass:
157 computation, seven independent arithmetic and three interim provenance.
Freeze 476--487 and completed artifacts; the earlier progress checkpoint
remains unchanged as history.

*Next decision:* the P=400 falsification test passed, so continue staged
precision work. Generalize the lift and checkpoint original-operator
sweeps by state chunks, then cost one P=800 column from P=400 with r=32,
including factor, seed, corrections, final residual and CM work. Do not
infer full P=10552 affordability from a synthetic action. Source 488 is
next unused; the generalized driver and P=800 run are not yet executed.
Retain all resource pauses, preceding exact-zero hypotheses, D99/D108,
D120's conditional target and all downstream cover/field requirements.

*Transport recovery:* the installed CLI supports `codex resume --last`.
A fresh chat in the same workspace can resume from HANDOFF.md. A stream
failure is not evidence that a local job failed: inspect receipts and
partial outputs before restarting a phase. No client configuration was
changed, and no automatic retry loop was installed. Once a turn has
failed, another request must come from the client or user to continue it.
All jobs completed, and the entry documents were updated.


## 2026-09-27 — D123: retain weighted Schur correction after an audited P=800 pilot

The user authorized continued work without approval pauses. Read
[the proof and measurements](dembele/certificates/dyadic-staged-pilot-d123.md)
and [the source ledger](dembele/data/computed/dyadic_staged_pilot_sources_d123.json).
Sources 488--491 complete one actual P=800 column, all seventeen CM charts
and an independent audit. The four coarse beta-errors are
[1632,1648,1632,1664]. All original residuals and old overlaps pass.
The complete sixteen-column bank remains P=400, so D122's quadric and
Gaussian results are unchanged. No exact curve or field identification.

*Method decision:* use moment-dependent precision rather than retaining
uniform precision throughout every correction. The positive input column
k is divisible by pi^k. Hence T kills the error lattice v_pi(e_k)>=P-k
modulo pi^P, and a weighted residual followed by one original application
certifies a uniformly correct column. After r=32 low elimination, only
k<P-u remain active at residual valuation u. Stop when u+33>=P and
reconstruct. Source 492 checks a compact input using 51.5625% of the
uniform bytes. Source 493 implements twelve shrinking corrections from
the frozen uniform seed and reproduces the verified column exactly.

The active counts fall from 400 to 33. All intermediate weighted states
and residuals agree with the original thirteen-step calculation.
Correction files total 103,751,328 bytes versus 940,992,000 in the original
loop; both sets remain frozen. The serial shrinking coordinator takes
513.967 seconds excluding construction of its imported seed. The earlier
parallel state pilot takes 538.595 seconds, including seed construction.
These different scopes do not establish an elapsed speedup.

*Review:* source 491 checks recurrences, high seed moments and all 68
coarse values; 494 separately checks the weighted representation,
14,476,800 state overlaps, 3,695,760 residual overlaps, all 348 divisibility
hypotheses and the final reconstruction. Neither imports production
arithmetic. All 148 input jobs pass. Review 495 binds 2532 source hashes,
preserving all 1884 D122 hashes. Creation and hash replay pass in 3.538
and 3.198 seconds. Freeze 488--495, both coordinators and bound artifacts.
All workers have completed; no file was deleted.

*Next bounded work:* combine weighted storage and shrinking correction
bands with resumable state chunks, then cost one P=1600 column from this
verified P=800 seed, including the factor, seed, original residual, CM
extension and peak memory. Source 496 is next unused; no P=1600 job or
combined driver exists yet. Complete these costs before another full bank
or the conditional P=10552 solve. Retain all caps, resource pauses,
D99/D108, exact-zero prerequisites and downstream cover/field tasks.
Decisions, references and resume instructions are updated. No correspondence.


## 2026-09-28 — D124: accept P=1600 pilot; prioritize the complete P=800 comparison

All 242 bounded input jobs pass. One actual column is certified P=1600
by weighted refinement, full GMP reconstruction and a second full original
residual check; CM errors are [3232,3248,3232,3264]. Four separate integer
quotient audits pass. The 228 state phases take 1713.775 coordinator
seconds, with 1,127,170,048 maximum single-process resident bytes. This
measures one column, not a full target-size solve.

Composing an integral CM map with the original contracting child maps
preserves c and determinant divisibility by pi, so weighted moments
suffice directly. Source 500 agrees with every independently calculated
CM moment at P=800 and 1600. Sources 502--503 validate compiled small
products; 172 independent controls and 33,320 actual scalar comparisons
pass. Synthetic target timings still do not establish full-solve cost.

Decision: use these controlled improvements to complete the full P=800
bank and redo the quadric falsification check before another isolated
higher-precision column. Reuse column 0 and lift columns 1..15 from
P=400. Adapt the older seed metadata explicitly. Keep full original GMP
residuals, independent audits, old overlaps, resumability, three workers
maximum and 180-second private-process-group caps. Source 505 is drafted;
new drivers are required and no P=800 full bank is claimed yet.

Review 504 binds 3535 sources, preserving all 2532 D123 hashes. Freeze
successful 496--504, the coordinator and the bound report/ledger. The
accepted full-bank section bounds and all downstream geometric/field
obligations remain unchanged. No positive exact quadric zero, candidate
identification or target polynomial has been proved. See
[report](dembele/certificates/dyadic-precision1600-d124.md) and
[ledger](dembele/data/computed/dyadic_precision1600_sources_d124.json).

## 2026-09-28 — D125: retain the candidate after full P=800 review; bound target storage next

The complete P=800 bank and independent comparison pass. All 6188
quadric coefficients, including 4641 positive coefficients, contain zero;
no mismatch is certified. Section bounds improve to 4994/4945/4928,
anchor bounds to 4776/4448/4184, and sufficient nonanchor thresholds to
25255/25369/25476. The remaining gaps are 20261/20424/20548. W Gaussian
remains nonzero, valuation 1024 and error 2025, uninverted. No positive
exact zero, candidate identification or target field polynomial is proved.

All fifteen new state runs and CM calculations pass; column 0 reuses
D123. Original residuals cover 17,817,600 scalars across the full bank.
Fifteen independent column audits and a separate global comparison
validate every coarse value, sampled recurrences, all weighted errors,
the frame and all quadric coefficients. All 1250 input jobs pass under
the unchanged caps; maximum job duration is 69.292 seconds and maximum
single-process peak memory is 811,401,216 bytes. The state runs take
5409.946 recorded coordinator seconds and retain 3,656,839,680 bytes.
Review 513 binds 8729 hashes, preserving all 3535 D124 hashes. Freeze
505--513, both coordinators and the bound report/ledger/artifacts.

Decision: retain the candidate and integral-section route. Before another
larger full bank, control selective state reads and a bounded checkpoint
protocol. A uniform target column already needs 2,423,583,360 packed
bytes; the current full-input decoding and cumulative checkpoint layout
are not a target-size resource certificate. Final correctness depends on
exact masses, the original residual and transport/truncation proof:
e=T_+e modulo pi^P, with T_+ pi-divisible, implies e=0 after P iterations.
Thus future intermediate data can be treated as rolling scratch while
retaining the final state/certificate and required receipts. This is a
prospective implementation change, not deletion of any existing frozen
artifact or replacement of full residual checks by hashes.

Next unused source 514 should control selective reading at certified
P=1600 against all weighted projections and selected full original GMP
rows, measuring peak memory. Then control the rolling protocol and
profile low-factor decoding/solves and map reuse before selecting a larger
refinement. The conditional P=10552 design, original kernels, all resource
pauses and downstream cover/torsion/action/invariant gates remain unchanged.
See [report](dembele/certificates/dyadic-precision800-d125.md) and
[ledger](dembele/data/computed/dyadic_precision800_sources_d125.json).

## 2026-09-28 — D126: accept selective/streamed controls; integrate before increasing precision

All 22 bounded input controls pass. Selective uniform and weighted GMP
sweeps each check all 2,227,200 P=1600 state scalars; every weighted
coordinate and exact mass agrees. Complete-sweep peaks are 221/229 MB.
The prospective rolling store replays all 25 checkpoints, recovers from
four deliberate process exits and a corrupt scratch copy, and stays
below 87,665,776 bytes. No old frozen artifact is changed or deleted.
The sealed control directory itself now freezes.

Streamed 200-bit factors match resident answers and satisfy every
original sparse equation. Two-RHS peak falls from 786,153,472 to
293,371,904 bytes; a sixteen-RHS control uses 353,501,184 bytes and checks
712,704 equations. Grouped map reuse and complete actual low solves pass
for two P=800 columns and the first P=1600 correction. The two-column
RHS takes 59.828 of 76.713 total seconds; transport arithmetic dominates.
Do not present memory reductions or one-run timings as a full target
runtime certificate. These controls do not raise harmonic precision.

Decision: integrate a complete rolling refinement for new column 1
from P=800 to P=1600 using verified existing factors, before increasing
precision or launching another full bank. New source 519 is next unused.
Require a phase inventory and hard 512 MiB cap covering all prospective
scratch work/chunks, final uniform reconstruction, a separate original
GMP residual, exact masses, old overlaps and direct CM. Retain final
artifacts and immutable receipts; distinguish retired scratch hashes
from available provenance sources. Freeze every existing artifact.

Review 518 binds 8816 sources and preserves all 8729 D125 hashes.
The full bank remains P=800, column 0 P=1600. D125's section bounds,
Gaussian, conditional target, original kernels, exact-zero prerequisites
and downstream cover/field gates remain unchanged. No positive exact
quadric zero, curve identification or field polynomial is proved.
See [report](dembele/certificates/dyadic-resource-controls-d126.md) and
[ledger](dembele/data/computed/dyadic_resource_controls_sources_d126.json).

## 2026-09-28 — D127: accept complete rolling refinement; reuse the low factor at higher precision

The full column-1 P=800-to-P=1600 refinement passes all 228 state phases,
2,227,200 original residual scalars, old overlaps, exact masses and direct
CM; four independent audits pass. The complete bank remains P=800 and
the D125 quadric/section/Gaussian conclusions are unchanged. Peak scratch
is 308,327,101 bytes under the proven 381,534,376-byte inventory and hard
512 MiB limit. Retiring prospective scratch reduces retained state payloads
to 140,237,736 bytes; no old frozen file is removed. The independent review
replays every allocation/retirement set. Serial full-array assembly still
peaks at 1,117,175,808 resident bytes and remains a scaling obstacle.

The low-system factor need not be rebuilt at every doubling: solve with
the existing factor modulo 2^m, form the original residual modulo 2^(2m),
divide its coefficients exactly by 2^m, and solve once more with the same
factor. Source 524 controls this at P=1600/3200, each with 89,088 complete
sparse equations; the smaller case also matches the full factor. This
raises low-system precision, not actual harmonic precision.

Decision: retain the integral-section route and complete rolling workflow.
Replace whole-bank serial decoding with selective assembly/preparation,
controlled against retained D124 data, then measure bounded P=3200
transport/RHS chunks and prove a complete phase resource inventory before
an actual larger column. Reuse the existing P=1600 factor through exact
residual lifting; do not pay for a new P=3200 factor. Source 525 is next
unused at this review. A larger full bank and complete P=10552 solve
remain uncosted, and all original-kernel/geometric/field gates remain.

All 235 input jobs pass under unchanged caps. Review 523 binds 9599 sources,
preserving all 8816 D126 hashes; creation and replay pass. Freeze 519--524,
all successful artifacts, sealed scratch, report and ledger. See
[report](dembele/certificates/dyadic-rolling-pilot-d127.md) and
[ledger](dembele/data/computed/dyadic_rolling_sources_d127.json).

## 2026-09-28 — D128: accept selective serial controls; integrate one P=3200 column

All thirteen input controls pass. Selective serial processing reproduces
305,582,280 bytes across fourteen retained D124 artifacts and all 133,632
original sparse low equations. Assembly peaks at 365,510,656 resident
bytes; preparation peaks are smaller. No new binary writer or complete
refinement is executed. Precision-3200 original-map samples compare every
scalar between adaptive and GMP backends, totaling 926,352 comparisons
and 230,400 actual old overlaps. Eighteen states per mode are sampled;
full/RHS inputs are synthetic. Maximum transport RSS is 420,642,816 bytes.

Decision: proceed to a single actual column-0 P=1600-to-P=3200 refinement
with a new integrated driver, source 528 onward. Use selective serial
processing, initially six-state chunks, separately chunked correction
RHS and existing-factor residual lifting. The proposed scratch inventory
is 1,510,359,376 bytes under a 2 GiB limit; enforce full output reservations,
row writes, receipt-bound retirement and final sealing in the new driver.
The inventory is not an existing cap, aggregate RAM bound or full runtime
certificate. Retain full original GMP reconstruction/verification, old
low/extended overlaps, masses, direct CM and independent audits. Split
CM by chart when needed. No new factorization is needed at P=3200.

A larger full bank and complete P=10552 solve remain uncosted. The complete
bank is still P=800, two columns P=1600. All quadric/section/Gaussian bounds
and downstream original-kernel/cover/field gates remain unchanged. No
positive exact vanishing, candidate identification or polynomial is proved.
Review 527 binds 9648 sources, preserving all 9599 D127 hashes. Freeze
525--527, passing outputs and the bound report/ledger; preserve every earlier
freeze. See [report](dembele/certificates/dyadic-selective-scaling-d128.md)
and [ledger](dembele/data/computed/dyadic_selective_scaling_sources_d128.json).

## 2026-09-28 — D129: accept actual P=3200 refinement; cost the target before scaling the bank

One actual column now reaches P=3200 with every original residual equation,
old overlap, exact mass, direct CM chart and all 22 independent audit jobs
passing. All 1934 input jobs and both reviews pass; review 532 binds 15600
sources and preserves all 9648 D128 hashes. The enforced 2 GiB scratch
limit holds, with peak 1,229,041,837 bytes; all 103 retirement barriers are
independently replayed. The four sealed payloads total 558,829,536 bytes.
Selective serial processing removes complete long-bank decoding; measured
single-process peak is 491,929,600 bytes, without an aggregate-RAM claim.
No earlier frozen artifact is removed. Retired hashes are history, and
the final original-residual proof is independent of iteration history.

Decision: retain the candidate and integral-section route, and use the
completed pilot to cost target-size operations before producing another
large bank. Source 533 is next unused. Control original full/RHS/extension
actions at P=10552 with suitably split child/backend jobs; compare both
polynomial backends and old actual overlaps, distinguishing samples and
synthetic data from a real lift. Control repeated exact residual solves
with the existing factor, in at most 200-bit increments: seven can reach
1319 bits without a new factorization. This target-size control is not yet
executed. Compare a staged ladder with a direct jump and account for
multiple-RHS reuse; a single large-action benchmark cannot choose the
complete precision schedule.

Prepare a complete phase and storage budget. The current four dense final
payloads per target-size column plus CM data would exceed available disk
for a full bank. Prospectively control lossless zero-residual encoding and
regenerated weighted projections from retained uniform moments. Preserve
all frozen data; this is a proposed format for future outputs. Do not infer
target runtime or aggregate memory from the P=3200 pilot. Keep the unchanged
three-worker and 180-second process-group limits, assertions and one BLAS
thread. The next bounded controls are authorized within those constraints.

The full bank remains P=800, the other higher-precision column P=1600.
All section/quadric/Gaussian bounds and exact-zero prerequisites are
unchanged. No candidate identity or field polynomial is proved. Freeze
528--532, both operational schedulers, passing artifacts, sealed scratch,
the report and ledger, preserving every prior freeze. See
[report](dembele/certificates/dyadic-precision3200-d129.md),
[ledger](dembele/data/computed/dyadic_precision3200_sources_d129.json) and
[review](dembele/data/computed/dyadic_precision3200_review_d129.json).

## 2026-09-28 — Strategic stocktake after D129: cost the geometric certificate and expose the downstream construction

The user requested a reassessment before further execution. D129 remains
the latest completed arithmetic checkpoint. No new computation or D130
milestone is claimed. See the
[stocktake](dembele/certificates/stocktake-2026-09-28.md).

Decision: retain the dyadic integral-section route, whose height argument
gives a conditional finite precision target for exact identification of C.
Treat exact genus-16 identification as the next major mathematical
milestone. D126--D129 are valuable evaluator/resource advances, but the
complete bank and section bounds remain D125's P=800 results. Neither
the high-precision single column nor the number of passing checks is
a measure of proximity to the field polynomial.

Broaden the source-533 work packet to a cost of the complete certificate:
target map/RHS/extension controls, repeated low-factor reuse, precision
schedule and column batching, CM/frame/quadric arithmetic, original
residuals, independent audits, review/I/O and retained storage. Control
compact future residual/projection retention, preserve frozen files, and
budget concurrent RAM separately from scratch. Proceed to another actual
refinement only with a defensible full schedule and storage reserve under
the current caps; any intermediate pilot must resolve a named uncertainty.

Alongside that cost report, specify the first downstream arithmetic
construction, with inputs, operations and exact acceptance criteria.
Base identification alone does not prove the P32/B3 markings or arithmetic
double-cover character/twist, recover exact global cubic coefficients,
supply Y64's section matrices, or make genus-64/degree-51 torsion practical.
D88's cubic shortcut remains conditional on the marked arithmetic X.
D120 already settles norm-97 cofactor separation; it does not implement
the global F256 action. Distinguish a costed intermediate theorem from
a costed path through the original-kernel polynomial.

Alternatives: do not automatically repeat single-column precision
doublings, revive the rejected spectral/inverse-frame/Faltings-only
estimates, or restart ordinary cubic recognition without a new mechanism.
No executable replacement carrier or direct original-kernel construction
has been established, so abandoning the current route is not justified
by this review. Conversely, resource or arithmetic-construction failures
must produce a specific redesign/research task, not another larger pilot.

Preserve all freezes, original kernels, successive exact-zero hypotheses
and resource pauses. At most three mathematical workers, unchanged
180-second process-group caps, assertions and one BLAS thread. No new
external theorem, remote launch, correspondence, commit or cleanup.
The handoff, references and entry documents now point to this plan.

## 2026-09-28 — D130: choose weighted representation redesign before the staged bank

The accepted stocktake work is complete: 137 passing inputs, one retained
and resolved budget-script failure, and two passing fixed reviews. Review
540 binds 16142 hashes and preserves all 15600 D129 hashes. See the
[feasibility report](dembele/certificates/dyadic-target-feasibility-d130.md),
[arithmetic construction specification](dembele/certificates/arithmetic-construction-d130.md)
and [ledger](dembele/data/computed/dyadic_target_feasibility_sources_d130.json).
Freeze sources 533--540, the coordinator, successful artifacts/reports and
failed-attempt history; preserve all earlier freezes. Actual precisions
remain P=800 full bank, P=3200 column 0, P=1600 column 1.

The measured controls cover target-size actions, seven existing-factor
stages to 1319 bits, coarse CM formulas, frame and quadric substitution.
Complete backend comparisons and independent samples pass. Staged refinement
is much cheaper in the empirical model: about 9--14 ideal three-worker days
versus 35--61 direct, before additional I/O/contention. Those are sample
scenarios, not runtime bounds. Batching low solves alone gives a modest
saving. The old scratch protocol requires 6.03 GB already at P=6400,
exceeding the unchanged 2 GiB cap. A target uniform payload alone exceeds
that cap. Compact final retention and isolated action timings cannot admit
another complete refinement.

Decision: implement a weighted-only certificate first, then a resumable
row-journal protocol, using source 541 onward. D121's column valuation
bound implies T Q=T; therefore Q T(w)=w certifies the uniform fixed point
T(w) without storing it. Review 540 independently checks divisibilities for
all 348 original and 34 composed CM maps. Replay every actual D129 retained
coordinate and CM output before using the new certificate. Keep the
original GMP action and independent arithmetic checks. Update one temporary
weighted state with durable row recovery; permit operator reads only at
committed generation barriers; retain correction input plus one new residual.
The target weighted state plus two largest residuals is 1,968,764,760 bytes,
but all other live slots and crash paths still need an enforced inventory.
Stream authentication once per generation and verify per-row hashes on
selective reads; the old hash helper's whole-file allocation is now explicit.

Do not automatically double precision, raise caps, delete frozen data, or
commit to the long bank. Prefer the staged ladder only after the new
protocol passes. Specialized zero-parameter maps and larger Schur blocks
are subsequent bounded performance comparisons, with no presumed speedup.

The arithmetic bridge is a separate research obligation. The exact unit
1+b has norm -1, is square at the chosen 31-adic place, and its quadratic
extension has no finite ramification away from 2. Local agreement and
ramification support therefore do not determine the arithmetic double
cover. This is not evidence that the candidate is wrong. Certify P32/B3,
geometric character and global twist before invoking D88 on the same
arithmetic X; exact Y sections and global F256 action still require effective
construction. D120's norm-97 separation remains settled. The field
polynomial and even exact base identification remain open.

Keep at most three mathematical workers, unchanged 180-second process-group
caps, assertions and one BLAS thread. No correspondence or remote launch.
The seven entry documents are updated with this next packet.

## 2026-09-28 — D131: retain the weighted certificate and integrate a complete resumable driver

The D130 implementation packet passes: 54 input jobs, no failed bounded
jobs, and two passing reviews. Review 546 binds 16567 hashes and preserves
all 16142 from D130. Freeze successful 541--546, `run_d131_batch.py`,
bound artifacts and all 24 sealed stores; keep every earlier freeze.
See the [report](dembele/certificates/dyadic-weighted-journal-d131.md),
[ledger](dembele/data/computed/dyadic_weighted_journal_sources_d131.json)
and [completion record](dembele/data/computed/dyadic_weighted_journal_completion_d131.json).
All four batch coordinators completed. No mathematical worker remains.

The complete weighted certificate checks all 4,454,400 uniform and
4,454,400 weighted coordinates, 174 exact masses and 870,400 CM scalars
against frozen D129. T Q=T and Q T(w)=w give a uniform fixed point without
retaining a uniform payload. D129 already evaluated CM from weighted
inputs; this new replay uses GMP and generation-bound streaming/row
authentication. Independent ordinary recurrence checks are sampled,
not a second complete independent operator.

The journal recovers nineteen distinct process-interruption boundaries,
rejects four corruption/stale-journal cases and passes actual saved and
synthetic target-width transitions. The 22 intentional child exits are
passing control events, not failed jobs. No power-loss/hardware guarantee
is claimed. Source 545 freshly recomputes D124's known first P=1600
correction through the journal: 348 low-RHS actions, the streamed 100-bit
factor, all 44,544 original low equations and 348 correction actions.
All 1,067,664 new residual scalars match the frozen reference. This
validates arithmetic integration without increasing mathematical precision.

Decision: proceed with the weighted staged route and complete its resumable
driver using source 547 onward. This resolves the next implementation
gap more directly than another isolated map timing or saved-byte replay.
Make low-RHS chunks and multi-digit factor stages separately capped and
resumable. Save authenticated low answers before mutating state rows;
resume computation as well as storage recovery. Use the old weighted
seed directly with the D121 error/column-valuation argument, restore
exact masses, check old overlaps and every final weighted equation.

Use one working store. Integrate all initialization, low-stage, journal,
sweep, CM publication and restart lifetimes, plus a separate concurrent
RAM budget. The target reservation is 2,035,873,922 bytes including a
64 MiB reserve and owner metadata, under 2 GiB; these are sparse logical
reservations, not a completed target run. Per-store enforcement does not
certify aggregate concurrent stores or RAM. Only then select the first
actual higher-precision column and re-cost the full staged schedule.
D130's 9--14 ideal three-worker days is a pre-redesign empirical baseline,
not an updated ETA. No automatic doubling or full-bank launch follows.

The complete bank stays P=800, column 0 P=3200 and column 1 P=1600.
The 6188 quadric balls contain zero with no positive exact vanishing;
section bounds, anchors, uninverted W Gaussian and successive-zero
hypotheses remain. Exact base identification and the original-kernel
polynomial are open. Marked P32/B3, double-cover character and arithmetic
twist, actual Y64 sections, combined g64/d51 torsion and global F256
action remain independent research obligations. D130's local/global
twist distinction and D120's settled norm-97 separation still apply.

At most three mathematical workers globally; unchanged runner 272
180-second private-process-group caps, assertions and one BLAS thread.
Inspect receipts and partials after disconnects; preserve completed work.
No new external theorem, remote launch, correspondence or frozen cleanup.
Decisions, references, handoff and all seven entry documents are updated.

## 2026-09-28 — D132: admit one actual P6400 column after complete driver controls

All 471 control inputs and both fixed reviews pass, with no failed bounded
jobs. Review 555 binds 18589 hashes and preserves all 16567 D131 hashes.
Freeze sources 547--555, successful artifacts, sealed P800/low1319 stores,
report, ledger and the admitted configuration. See the
[report](dembele/certificates/dyadic-staged-integration-d132.md) and
[completion record](dembele/data/computed/dyadic_staged_integration_completion_d132.json).

The new driver completes a known P800 column from P400: 432 phases,
twelve corrections, all weighted equations/masses, 217,600 CM coefficients
and 68 coarse values. A separate synthetic control executes the same
low phases through seven digits to 1319 bits, checking all 44,544 original
low equations per digit and matching every D130 answer byte. Seven
actual worker interruptions and one archival interruption recover. These
are process-interruption tests, not a hardware-durability theorem.

Decision: retain this staged driver and admit one actual P6400 column 0
from the frozen D129 P3200 seed. The named implementation gaps are now
controlled, so another isolated timing/replay would add less than an
actual complete stage. Use source 554 (arithmetic unchanged from 548,
configurable prior-review provenance), source 553's archiving schedule,
one-state operator jobs, three-state RHS jobs and one-chart CM jobs.
Pause the coordinator after initialization and resume from its receipts,
then continue all 96 corrections through full weighted/CM verification and
independent review. This actual execution is D133 and is now active.
No new P6400 precision is claimed before its final certificate and review.

The complete live-file model fits 973,167,872 bytes at P6400 and
2,046,552,040 at P10552 from 6400, including conservative metadata/crash
allowances and the 64 MiB reserve. A single working store and archival after
every completed sweep are required. Duplicate internal job records may
retire only after identical external metadata and passing receipt/log
bindings are checked. External records and all older frozen stores stay.
The actual long-stage retention/runtime must be re-costed before committing
the full bank. D130 timings remain a pre-redesign baseline.

RAM admission is separate: at most three workers, at most 2 GiB measured
peak per successful job and at most 6 GiB as their conservative sum. It is
not OS hard enforcement or a claim about physical free memory. Queries
for the process table and hardware memory are unavailable in the sandbox;
interrupted-child RSS was not separately recorded. Actual controls peak
at 122,978,304 bytes for a successful mathematical worker. A timeout,
excessive measured peak or reservation rejection stops further admission
and requires a smaller job. Keep unchanged 180-second process-group caps,
assertions, one BLAS thread and every prior freeze.

The certified full bank remains P800, column 0 P3200 and column 1 P1600.
No positive exact zero, candidate identity or field polynomial is proved.
D125 bounds/anchors and uninverted W, successive-zero hypotheses, D99/D108,
D120 norm97 separation and D130's marked-cover/twist/Y-section obligations
remain. No automatic full-bank launch, correspondence or remote execution.
All seven entry documents now record the reviewed controls and active D133.

## 2026-09-28 — D133 in progress: complete the admitted column and separate audit scopes

The planned initialization pause completed with 176 passing phases. Its
[record](dembele/data/computed/dyadic_staged_P6400_col00_pause_d133.json)
binds the receipts and historical checkpoint. The resumed coordinator
reused those receipts and passed the seed low solves at 200, 400, 600 and
800 bits, checking all 44,544 original low equations at each stage.
Continue the frozen 553/554 schedule to completion; no new admission or
full-bank launch is inferred from these intermediate checks.

Draft sources 556/557 and `run_d133_audits.py` define the final verification.
The actual schedule contains 24,456 arithmetic/storage phases and 97
archival jobs. After sealing, execute the 24 independent audit jobs, then
review creation/replay. Complete old weighted and CM overlaps, all masses
and all 68 coarse overlaps are distinct from sampled independent original
state/CM recurrences and six independently summed coarse values. The
review must authenticate the full phase list, every committed generation,
all retained payloads, archive bindings and all 176 reused pause receipts.
The drafts are not run or frozen yet. Sources 558/559 now hold the
separate, unrun D134 refinement below; source 560 is next unused.

Certification remains at full bank P800, column 0 P3200 and column 1 P1600
until the actual final equations and independent review pass. Preserve the
same time, worker, storage and measured-RAM limits and all prior freezes.

## 2026-09-29 — D134 draft: use the odd-order and B3 arithmetic cover criterion

Re-reading D71, D77, D87 and D88 found a stronger existing arithmetic
condition than the separate twist gate stated in D130. D77 proves the
exact normalized B3 fibre has squareclass -3 in its degree-nine residue
field. A constant Galois C3 cover totally ramified above B3 requires that
fibre to contain the cube roots of unity. The odd-degree norm argument
therefore selects exactly one F-scalar twist within the fixed half.
D130's nonsquare unit remains a counterexample to local-31 agreement plus
ramification support alone; it does not satisfy this extra inertia test.
Restore the existing D77 condition to the active plan.

There is a further conditional deduction. The canonical genus-16 Hecke
order P16(32)=1640801490553691915934375 is odd. Once the candidate base and
its branch markings are arithmetically identified, and the canonical
Hecke interpretation is applied, good reduction at31 gives Jac(C)(F)[2]=0.
Any two F-rational branch halves then agree. The remaining scalar is
fixed by D77. Thus the marked arithmetic double cover follows from the
marked base and these arithmetic inputs; a separate geometric-character
continuation proof is not required by this route. Two matching candidate
point counts do not supply its missing base identification or Euler factor.

The [D134 draft](dembele/certificates/arithmetic-twist-classification-d134.md)
states all hypotheses. It leaves P32/B3 marking, the exact (C,D17)
identification, canonical Hecke interpretation, cubic orientation/global
coefficients or Y sections, and the final target construction explicit.
Sources 558/559 now draft two rational-polynomial checks of the D77 witness
and independent computations of the odd Hecke order. Their first unit-class
prototype was unexecuted and replaced before any source was frozen.
The D77 certificate chain is separate from the dyadic catalogue and will
be merged by recursive hash verification. No earlier frozen record changes.

Stacks tags 09EE, 0BFH and 03RP were freshly checked on 2026-09-29 for
inertia and torsion facts. Their application to specialization, branch
halves and the fixed fibre is our deduction. The old residual-image
verdicts in f16_steinberg.out are not used. The revised drafts remain
unrun; global caps and the three-worker limit are unchanged. Source 560
is next unused. Continue D133 to completion and review before executing
the D134 fixed review, which is designed to preserve the full D133 root.

## 2026-09-29 — D133 continuation across long execution and disconnects

The production coordinator remains active; seed and corrections 1--6
have committed with no failed receipt observed. The final audit and
review stages are now queued through `run_d133_completion.py`, which
waits for production to release its lock and requires a completed sealed
store. It then runs the 24 independent jobs, prepares the measured report
and ledger, runs D133 fixed review/replay, and continues to the D134 finite
replay and review. Successful checkpoints update all seven entry documents.
This removes the dependency on another chat prompt at those transitions.

Six operational fixture controls pass without launching a mathematical
driver: real locks, incomplete/failed-input stops, receipt reuse and hash
checks, idempotent document updates with resolving links, and immutable
artifacts. The control record binds the continuation source; reviewer557
will preserve those bindings. Production is session37950 and the waiting
continuation is session32689. Inspect both before any restart; no parallel
manual mathematics may exceed the existing global three-worker limit.

A failure stops the chain and retains its receipt/log; neither failed
arithmetic nor a missing production summary triggers an automatic rerun.
There is no full-bank or next-precision launch. Certified precision and
the conditional cover criterion remain unchanged until their respective
fixed reviews pass. No frozen source or earlier artifact is modified.

For the subsequent re-costing, retain complete coordinator wall time in
addition to summed worker durations. Static inspection found repeated
computed-directory globs in source553's per-job attempt lookup and
source551's per-record archival lookup. Their scaling with the permanent
receipt population needs measurement; it is not yet a measured bottleneck.
Direct attempt paths or a checked index belong in a future coordinator,
along with bounded submission. The active frozen implementations remain
unchanged, and no larger Schur factor or full-bank schedule is admitted
from this inspection alone.

## 2026-09-29 — Session-close handoff for the active D133/D134 chain

At the user's request, persist the current execution and recovery procedure
before they close the session. The
[11:34:55 UTC snapshot](dembele/data/computed/dyadic_close_session_snapshot_d133_20260929.json)
records 2,493 production/archive receipts reporting pass, no failure, and
maximum duration 28.544548 seconds. Seed and corrections 1--8 are committed;
correction 9 is underway. The observed state is ready008, epoch18,
(u,count,bits)=(3464,2936,367). This observation does not certify P6400.

Leave production session37950 and continuation session32689 running.
Both coordinator locks are held at observation. Persistence after closing
the session is unverified; a new session must inspect durable completion
records, real lock ownership and in-flight receipts before restarting.
Session IDs alone are not durable process identifiers. A free coordinator
lock also does not prove that no orphan worker remains. Do not remove lock
files or launch a duplicate coordinator. Resume production first if needed;
the continuation requires its active lock or a completed sealed result.

The handoff specifies all completion filenames, command order, partial-job
diagnosis, receipt reuse and the post-review re-costing task. Handoff,
decisions, references and all four entry READMEs/instructions are updated.
No mathematical driver, successful source, receipt or frozen store is
changed by this documentation checkpoint. Full bank P800, column 0 P3200,
column 1 P1600 and the open field construction remain unchanged. Sources
556--559 await execution/review; source 560 is next unused.

## 2026-10-05 — Resume the admitted D133/D134 chain

The user requested resumption from the handoff on the original compatible
host. All 28,976 retained files and 289 external dependencies matched their
saved hashes, covering all 18,589 frozen D132 sources. Native libraries
loaded; all three locks were free and no mathematical workers remained.
See the [preflight record](dembele/checkpoints/d133-resume-2026-10-05-preflight.json).

Frozen production resumed at correction 10, reusing the passing receipts.
The unchanged continuation started only after production held its lock;
it waits to run D133's 24 audits, review/replay and D134. Both coordinators
use separate sessions and durable logs, recorded in the
[resumption record](dembele/checkpoints/d133-resume-2026-10-05.json).
The worker, timeout, storage and measured-RAM limits remain unchanged.
No new precision certificate or full-bank launch is claimed. Preserve the
historical transfer inventory as the pre-resumption baseline; re-cost the
complete stage only after D133/D134 review.

<!-- D133 reviewed continuation checkpoint -->

**Current reviewed checkpoint: D133.**

D133 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. All 24,577 D133 input jobs and both reviews pass. The fixed review binds 93,638 hashes. The completion coordinator next runs the D134 finite replay and review; inspect its live session and receipts before starting any other mathematical job. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](dembele/certificates/dyadic-precision6400-d133.md) and [completion record](dembele/data/computed/dyadic_precision6400_completion_d133.json).

<!-- D134 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D134.**

D134 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. The D134 replay and both reviews pass; its fixed review binds 93,912 hashes and preserves the D133 catalogue. The conditional route uses the odd canonical Jacobian order to fix the F-rational branch half, then D77 cubic inertia to fix its scalar. The marked-base and canonical Hecke hypotheses remain essential. The continuation coordinator has no further mathematical jobs after this checkpoint. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](dembele/certificates/arithmetic-twist-classification-d134.md) and [completion record](dembele/data/computed/arithmetic_cover_criterion_completion_d134.json).



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

D148 decision: adopt 15237 as the current proved relation-height upper
bound, keep 623 as the sufficient P1600 target, and stop refinement of
the trace-dual/root-size factor as a standalone route to that target.
Assess a relation-specific or primitive-pencil comparison next. The
11266 floor concerns only this majorant and does not justify a precision
increase or a claim that the candidate is wrong.


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

D147 decision: retain the actual relation-height route, with the combined
comparison term explicitly budgeted. Do not replace the ordinary
bicanonical determinant by the orbifold weight-four determinant, assume a
Mumford isometry, or infer subspace distortion from the full-frame
determinant. The finite multiplication cokernel helps an upper bound;
its dyadic length is zero and the other lengths may be discarded.


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

D146 scope decision (2026-10-08): close the Faltings-only repair of
the current P1600 jet estimate. Further refinement of the same
elliptic or spectral terms cannot establish its false height target.
Return to the independent relation-space criterion, beginning with
the canonical multiplication determinant and its precise metrics.
No additional precision computation follows from this decision.

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

D145 scope decision (2026-10-08): stop pursuing the now-refuted
spectral target. A spectrum calculation cannot establish it.
Continue the proof-gap investigation by testing whether the omitted
intersection terms can supply the required geometric improvement.
This does not reject the recognized candidate or the original-kernel
field route, and does not admit a new precision bank or search.

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

D144 scope decision (2026-10-08): “continue” authorizes the theoretical
adjunction and compact RR investigation and its bounded finite audits.
The source repairs are explicit derivations, with independent controls;
no author confirmation is claimed. The new spectral threshold is a
sufficient target, not a measured or proved value. Continue analytic
feasibility work within the existing pauses. No P3200, actual-curve
spectral work, new level, Hecke bank, cubic search or resource change is
admitted by this checkpoint.

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

D143 scope decision (2026-10-08): “keep going!” authorized continuing the
finite-model and cotangent investigation. It is completed with explicit
bounds and an exact model correction. Continue theoretical control of
the remaining RR terms; this does not admit P3200, a spectral calculation,
a new level, or a change of resource caps. No new user decision was needed.

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

D142 scope decision (2026-10-08): the user explicitly requested work
through both height bullets. Retain the new actual upper estimates and
the quantified RR comparison as the outcome of that investigation.
Neither sufficient hypothesis follows. Continue the theoretical model
comparison before considering a numerical spectral job; this checkpoint
does not admit P3200 or change any resource cap.

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

D141 scope decision (2026-10-08): the user's request to update the entry
documents and proceed with the proof-gap investigation authorizes this
bounded analysis. Continue toward an actual height comparison using the
existing bank. The conditional targets above establish no missing geometric
estimate and do not authorize a new precision bank or reopen paused searches.
Retain D120's P200 exclusion as historical evidence and use D141's thresholds
for current P1600 planning.

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

*Maintenance note: append an entry per significant fork — the decision, the
alternatives, the reason, and (when known) the outcome. Commit refs and script
numbers make entries checkable against the repository history.*


## Operational checkpoint — 2026-09-30: stop and transfer to dots

The user requested a stopping point, commit and push. Production and continuation
had stopped after the previous session. Advisory locks were free, and a process
inspection found no production/continuation/archive/audit or capped worker.
There were 2,648 passing receipts and three completed worker logs without wrapper
receipts, with correction 9 in progress. Frozen coordinator 553 was resumed with
`--stop-before low_begin_010`; it preserved those logs, wrote attempt-02 recovery
receipts, completed correction 9 and archived duplicate metadata, then exited zero.
The journal is `ready009`, epoch 20, with no pending transaction and 2,682 passing
production/archive receipts. No frozen arithmetic source was edited. D133/D134
remain incomplete and no certified precision changes.

All existing D132 source hashes and the pause payload/row/receipt bindings were
verified. Git LFS was selected for large computed artifacts so the complete
retained research state can be pushed to the existing origin without dropping
payloads or rewriting history. A separate relative-path transfer inventory and
verifier support retrieval. `.env`, external tools, ignored third-party checkouts
and build caches remain outside Git. CHECKPOINT.md records native and absolute-path
dependencies: moving the frozen production runner to another OS/root requires a
reviewed port with new provenance, not mutation of old evidence. The next mathematical
source remains 560. Further production, D133 audits and D134 reviews are deferred
to the next working session; no full-bank launch is authorized by this checkpoint.

## 2026-10-09 — D150 structural comparison

**D150. Complete the saved structural audit before proposing another evaluator.**
The user resumed D149's handoff. The inspected actual-curve and candidate
certificates do not supply an exact comparison of their multiplication
relations. Marked descent gives uniqueness of an existing isomorphism;
the Shimizu tensor and conditional cover criteria do not create the
missing candidate isomorphism.

The exact dyadic recursion offers a possible identity mechanism, but
its finite chart set does not close the ordinary moment equations at
any finite degree. Two bounded checks verify all 348 contractions,
275 nonaffine branches with distinct child targets, and reachable
cycles of lengths four and six. A companion pole-orbit argument rules
out finite-dimensional rational test spaces invariant under each
individual branch and containing a CM kernel. This is a limitation of
that closure proposal, not of every exact transfer identity.

The next theoretical task is a finite exact identity for a cleared
positive-order residual using the summed transfer operator, or an
equivalent multiplication-compatible comparison. D150 section 5 gives
the sufficient identity and tensor extension but constructs no candidate
witness and asserts no finite search bound. Existing precision and
arithmetic pauses persist. The actual relation-height upper bound is
still 15237; target 623, identification and the field polynomial remain
open. Sources 626--628 and the new completion packet preserve D149's
transitive provenance. See the D150 checkpoint at the top of this file.
