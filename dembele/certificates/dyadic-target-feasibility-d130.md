# D130: target feasibility, retention, and the arithmetic bridge

Date: 2026-09-28. This executes the accepted
[stocktake plan](stocktake-2026-09-28.md).

**Decision: keep the integral-section route, but redesign the working
representation before another actual refinement.** Target-size operations
and seven-stage low solves pass bounded controls. The existing schedule is
expensive and its storage protocol fails the unchanged 2 GiB scratch cap.
The next concrete task is a weighted-only certificate and a resumable
single-state-file update protocol, first replayed against D129. The
[downstream construction specification](arithmetic-construction-d130.md)
also exposes an arithmetic cover ambiguity that higher precision on C
does not resolve.

There are 137 passing input jobs and one retained failed budget-script
attempt. The failure was a string-to-integer conversion in a finite map
census, before any output was committed; attempt 02 passes. Sources
533--539 and `run_d130_batch.py` supply the controls/model; source 540
supplies a fixed finite review. See the
[ledger](../data/computed/dyadic_target_feasibility_sources_d130.json),
[review](../data/computed/dyadic_target_feasibility_review_d130.json) and
[completion record](../data/computed/dyadic_target_feasibility_completion_d130.json).
All earlier frozen artifacts remain unchanged.

**No actual harmonic or differential precision increases.** The complete
bank remains P=800, column 0 P=3200, column 1 P=1600. All 6188 actual
quadric enclosures still contain zero. No positive exact vanishing,
candidate identification or field polynomial is proved. P=10552 remains
a conditional sufficient design, not a minimal precision or a prediction
that the candidate will pass.

## 1. What the bounded controls establish

Every mathematical job uses the unchanged 180-second private-process-group
cap, assertions and one BLAS thread. At most three mathematical workers
run concurrently. All seven explicit batch plans completed. No completed
phase or coordinator was rerun. The maximum passing input duration is
35.824 seconds; summed passing input durations are 1290.623 seconds.
Maximum measured single-process input RSS is 1,781,727,232 bytes, for a
GMP CM action. This is not a concurrent-memory bound.

Source 533 executes 74 individual child-map controls at P up to 10552.
Full, low-RHS, correction and CM inputs are dense synthetic vectors;
extension inputs are actual old column-0 rows with exact zeroth masses.
The target controls include states 0, 83 and 173, selected branches, four
CM children, and correction shapes across the active-length schedule.
They do not cover every target map or compute a new harmonic column.

Source 538 checks 26 complete adaptive/GMP output pairs, totalling
1,698,208 scalar comparisons; 22 additional actions are single-backend
cost controls. The sum of both extension children at state 0 agrees with
all 25,600 old scalar coordinates. Six separate ordinary-recurrence
audits use independent integer quotient arithmetic at full modulus;
their degrees 1, 2 and 3 are samples, not a complete independent operator.
Every source-533 action also checks its low 25-bit truncation.

Representative per-child preparation-plus-application times at target:

| Operation | Adaptive | GMP |
|---|---:|---:|
| Full, state 0 branch 0 | 25.70 s | 31.31 s |
| Full, state 83 branch 0 | 12.44 s | 18.17 s |
| Low RHS, state 0 branch 0 | 8.84 s | 10.71 s |
| Extend actual P=3200, state 0 branch 0 | 8.08 s | 8.45 s |
| CM chart 0 branch 1 | 28.96 s | 35.36 s |

Source 534 reaches 1319 binary digits using the frozen 200-bit r=32
factor in increments 200,200,200,200,200,200,119. All seven solves and
their separate original-equation verifications pass; each checks 44,544
original scalar equations. Six intermediate residual divisions are exact.
Source 538 independently checks 5376 sampled original equations and all
267,264 successive solution-prefix coordinates. No new factor is built.

At 1319 bits, three disjoint profiles cover all 165 distinct original
low maps for one and sixteen unrelated RHS columns. Their shared first
columns agree. Total measured operator time is about 22.05 seconds for
one RHS and 35.00 seconds for sixteen; coefficient construction is shared.
Together with D126's 8.988/18.181-second two/sixteen-RHS factor solves,
this supports batching as a limited optimization. It does not measure a
complete target multiple-column refinement.

Source 535 controls all four coarse CM orders at chart 0 by both direct
and independent Horner formulas. Their full values agree and preserve the
old actual overlaps. Arbitrary high digits are synthetic. A complete
16-by-16 frame control, using the existing algebraic eta precision 21168,
passes 1088 old jet overlaps and 272 leading identities. Its minimum
change error is 20840, as in D120's design; eta needs no further lift.
Full quadric substitutions at charts 0, 8 and 16 are independently
recomputed in 1092 coefficients. Their synthetic nonzero positive-order
values are expected and say nothing about the actual candidate.

## 2. Complete phase inventory and empirical schedule comparison

The [source-539 model](../data/computed/dyadic_target_schedule_budget_d130.json)
includes seed extension, seed RHS, repeated low-factor solves and every
original low check, initial residual, correction RHS/actions, serial state
updates, full GMP reconstruction and verification, all final CM maps,
direct and Horner coarse values, frame, all quadrics, independent audits,
old overlaps, serialization, proposed jobs, receipts and final review.
It separately displays logical I/O volumes and sensitivity to assumed
25/100/500 MB/s rates. These bandwidths are not sustained measurements.

The initial columns have seeds 3200,1600,800,...,800. The staged plan is
800->1600 for fourteen columns, 1600->3200 for fifteen, and
3200->6400->10552 for all sixteen. At r=32 each correction gains 33
digits; the staged plan has 4592 column-corrections and the direct plan
4623. Their costs differ sharply because the staged corrections work at
smaller moduli and lengths.

The two map scenarios assign either sampled state 83 or sampled state 0
to every child action. They illustrate map-cost sensitivity; **they are
not rigorous lower and upper bounds**. Corrections use piecewise linear
interpolation in active length. Smaller full actions use quadratic size
scaling. Factor batching and serial work have explicit interpolation and
pass-count assumptions. Map preparations are not shared across columns
in these estimates.

| Schedule | Factor batching | Modeled process hours | Ideal days at three workers |
|---|---:|---:|---:|
| Direct to target | 1 | 2681--4361 | 37.2--60.6 |
| Direct to target | up to 16 | 2536--4216 | 35.2--58.6 |
| Staged | 1 | 683--1007 | 9.5--14.0 |
| Staged | up to 16 | 634--958 | 8.8--13.3 |

The last column is division of process time by three. It excludes extra
I/O, dependencies, load variation and contention, and is **not an ETA**.
The large-batch scenarios have no resource-admitted implementation.
Proposed job counts range from about 117,000 to 256,000; startup and
review allowances at that scale remain unvalidated. Logical checkpoint
and final-data traffic in the stated pass model is about 22.2 TB staged
versus 52.9 TB direct. Some I/O is already included in measured row/factor
times; separately adding all sensitivity costs can double-count cached I/O.

For the slower staged single-column-factor scenario, correction actions
and RHS account for about 588 process hours, full final reconstruction
and verification for 143, and low solves/checks for 54.5. CM/frame/quadric
processing is a comparatively small cost. Another isolated doubling or
factor batching alone does not resolve the dominant expense.

Thus this is a complete **phase inventory with an empirical cost model**,
not an unconditional runtime certificate or a costed path through the
field polynomial. The model explicitly lists the unresolved admission,
concurrency, sustained-I/O and downstream-construction gates.

## 3. Exact byte controls and the failed storage gate

Source 536 reads every byte of both retained D129 zero residuals and
controls a lossless zero descriptor with length, layout and SHA-256.
Malformed descriptors and nonzero contents are rejected. The target-size
zero stream is synthetic, not a computed residual. Six projection jobs
regenerate every D129 weighted row from uniform moments and match all
113,343,600 bytes / 4,454,400 coordinates. A synthetic target row passes
serialization, fsync, readback and independent projection checks.

| P, old seed | Uniform state | Weighted state | Inherited conservative scratch |
|---|---:|---:|---:|
| 3200,1600 | 222,720,000 | 113,343,600 | 1,510,359,376 |
| 6400,3200 | 890,880,000 | 449,407,200 | 6,026,390,176 |
| 10552,6400 | 2,423,583,360 | 1,217,418,840 | 15,944,609,416 |

All numbers are bytes. The inherited scratch protocol fails at P=6400.
One uniform target column itself exceeds 2 GiB. Keeping only uniform
moments plus CM outputs reduces sixteen-column final payloads from
104,611,284,096 to 46,354,513,920 bytes, but does not fix working storage.
Existing frozen files are never candidates for deletion. The measured
available disk at review preparation was about 80 GiB; it is an observation,
not a reservation or a budget for all future stages/audits.

A separate authentication issue also matters. Source 514 reads selected
rows, but its inherited `source` helper ultimately calls source 459's
`Path.read_bytes()` for hashing. Its authentication therefore allocates
the full file, despite the selective reader. Old arithmetic is unaffected.
Source 537 controls a new 1 MiB streaming hash and a generation manifest
with per-row hashes. It authenticates all actual D129 rows in reverse
order, rejects altered row data and malformed manifests, and hashes a
logical 2.42 GB target stream without creating that file. The largest
hash read is 1 MiB. This is not yet integrated into a production driver
and is not a sustained-disk benchmark.

## 4. The chosen redesign: retain weighted moments and certify their lift

There is a useful algebraic simplification, directly from D121's column
valuation proof. Let Q retain low moments modulo pi^P and moment k>32
modulo pi^(P-k); take moments k>=P to be zero. Let T be the original
child-sum moment operator with fixed zeroth masses.

For phi(x)=(a*x+b0)/(1+c*x), put delta=a-b0*c. Since c and delta lie in
(pi), expanding

    phi(x)^n = sum_j binom(n,j) b0^(n-j) delta^j x^j/(1+c*x)^j

shows that column k has valuation at least k. Consequently

    T Q = T modulo pi^P.

If a retained weighted vector w passes **all** equations Q T(w)=w,
define the uniform lift mu=T(w). Then Q(mu)=w and

    T(mu)=T Q(mu)=T(w)=mu modulo pi^P.

Together with exact masses and the inherited fixed-mass uniqueness
argument, this certifies the harmonic moments without retaining a dense
uniform file or materializing a second full residual. Q is a choice of
residue representatives; the equality means that T annihilates its error
lattice, not that this choice is globally linear. The same error-lattice
argument applies to a composed CM action after verifying its c/delta
divisibilities. The existing uniform moments remain useful as a complete
reference for the first implementation control.

This is a mathematical deduction from the existing operator bounds.
**A weighted-only production certificate has not yet been implemented.**
Next replay the new certificate and direct CM evaluation against every
retained actual D129 coordinate; use new sources, separate ordinary
arithmetic samples and the full original GMP action. Do not alter D129.

Then implement a prospectively temporary row-journal protocol. Prepare
the correction by updating one weighted state file and converting the old
residual to the correction input, with durable row undo/redo records and
a barrier forbidding reads of mixed generations. During the operator
sweep retain that correction input and one new residual. Commit a complete
authenticated generation before retiring the previous correction. Include
interruption recovery and corruption controls before an actual lift.

For P=10552 from P=6400, the weighted state plus two largest scaled
residuals is 1,968,764,760 bytes. That leaves 178,718,888 bytes below
2 GiB for journals, bounded output rows, manifests and other scratch.
This is a promising layout, **not a proven simultaneous live-set bound**:
initialization, low solves, CM output, failures and final sealing all need
explicit inventories and implementation. Retaining weighted plus CM
would use 27,055,881,600 bytes for sixteen target columns, before other
stages/audits. No new cap or allocation is authorized by these calculations.

The map census also finds 165 distinct maps among 348 children, with
95 b0=0 and 73 c=0 at the working modulus. These are opportunities to
check specialized kernels, not proofs of global zero parameters or
measured speedups. A larger Schur block is another bounded comparison
after the representation gate: D121's r=64 gain of 65 is proved, but its
old small-modulus factor timing does not supply target cost.

## 5. Arithmetic scope and next execution

The [construction specification](arithmetic-construction-d130.md) names
inputs, operations and acceptance tests from (C,D17) through marked X40,
Y64 sections, target torsion, global F256 scalars and the original-kernel
polynomial. Several effective arithmetic constructions remain missing.
In particular, source 538 gives a global nonsquare unit 1+b which is a
square at the selected norm-31 place and whose quadratic extension is
unramified at finite primes away from 2. Agreement there and ramification
support do not identify the arithmetic double cover.

Freeze successful sources 533--540, their passing artifacts, the failed
539 snapshot/log/receipt, all plans/summaries, this report, its companion,
ledger and fixed review, preserving every prior freeze. Source 541 is
next unused. Begin with the weighted-only proof/replay and row-journal
controls above; keep the arithmetic twist/section construction explicit
on the research path. The staged schedule is preferred only after those
gates pass. No full-bank or automatic next-doubling run is admitted.
