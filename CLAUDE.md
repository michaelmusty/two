# Project: making Dembélé's field explicit

**Current stopping point (2026-09-30): D133 paused for transfer to dots.**
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

**Current checkpoint: D132 reviewed; D133 P=6400 column active (2026-09-29).**

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
- **`remote_magma/`** — tested CoCalc/chatelet client for Magma V2.29-8; operational
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
| **Magma** | 2.29-8 | Current `dembele/` Hilbert modular forms and exact number-field computations; installed locally and available remotely on chatelet. | licensed Magma install; remote setup in `remote_magma/CHATELET.md` |
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
