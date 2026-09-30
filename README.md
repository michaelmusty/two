# Making Dembélé's field explicit

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
- `remote_magma/` — tested client and operational documentation for running Magma V2.29-8
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
