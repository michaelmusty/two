# D131: weighted certificate replay and recoverable arithmetic updates

Date: 2026-09-28. This executes the next packet in
[D130](dyadic-target-feasibility-d130.md).

**The weighted representation passes a complete actual P=3200 replay.
The row journal survives process interruptions and corruption controls,
and a freshly recomputed actual correction uses it successfully.** This
supplies the core mechanism for the next driver. It is not a complete
target refinement or a new precision milestone.

All 54 input jobs pass under the unchanged 180-second private-process-group
cap, assertions and one BLAS thread. At most three mathematical workers
run concurrently. Summed input durations are 1268.854 seconds; the longest
is 78.143 seconds. Maximum measured single-process RSS is 334,118,912
bytes. Different scopes/backends prevent interpreting these measurements
as a target speedup or a bound on aggregate RAM.

Sources 541--546 and `run_d131_batch.py` supply the implementation and
review. See the [ledger](../data/computed/dyadic_weighted_journal_sources_d131.json),
[fixed review](../data/computed/dyadic_weighted_journal_review_d131.json)
and [completion record](../data/computed/dyadic_weighted_journal_completion_d131.json).
All prior frozen artifacts remain unchanged.

**Actual status is unchanged:** full harmonic/CM bank P=800; column 0
P=3200; column 1 P=1600. The 6188 actual quadric enclosures contain zero,
with no positive exact zero. Section bounds, the uninverted W Gaussian,
successive-zero hypotheses, candidate identification and original-kernel
polynomial are unchanged. This work removes implementation obstacles;
it does not establish the next geometric theorem.

## 1. Complete weighted-only replay

Let Q retain low moments modulo pi^P and moment k>32 modulo pi^(P-k).
D121's original coefficient bound gives T Q=T modulo pi^P. If every
equation Q T(w)=w holds with the specified masses, mu=T(w) satisfies

    T(mu)=T Q(mu)=T(w)=mu modulo pi^P.

Fixed-mass contraction identifies the canonical harmonic solution. Q
selects representatives of a residue lattice; this is not a claim that
that choice is globally linear. D130 independently checked the required
c/delta divisibilities for all 348 original and 34 composed CM maps.
The same lattice argument permits direct CM evaluation from w.

Source 541 authenticates the frozen D129 weighted state, uniform reference
and six CM chunks once per payload, with hash blocks of at most 1 MiB.
The row-hash manifest is bound to the prior fixed review and committed
D129 generation. Arithmetic workers authenticate requested rows without
rehashing the complete payload; only boundedly many rows are decoded.

Twenty-nine GMP original-map jobs check all 174 states: 348 child actions,
4,454,400 uniform scalar comparisons, 4,454,400 weighted scalar comparisons,
and 174 exact masses. Thus both Q T(w)=w and equality with every retained
uniform coordinate are checked. Six GMP composed-map jobs cover all
seventeen CM charts and all 870,400 retained scalar coefficients.

**D129 CM already used weighted inputs.** The new replay changes the
authentication path and uses GMP against retained adaptive-backend
outputs; it is not the first successful weighted CM computation. No new
uniform or CM binary is retained.

A negative control adds three nonzero errors inside the weighted error
lattice and checks all 25,600 output scalars remain unchanged. A wrong
first low moment is detected, with the expected nonzero delta in output
degree one. Only private memory is changed.

Source 542 independently reconstructs ordinary fractional-linear powers
at degrees 1,2,3 in a separate integer quotient. It checks 72 state and
72 CM scalar equations at three states/charts, then audits complete
coverage and every output-row digest. The recurrence checks are samples,
not a second complete independent operator. Full comparisons use the
production GMP action and frozen reference computations.

## 2. Row-journal protocol

Source 543 implements storage in new owned namespaces. The caller must
certify the arithmetic of proposed rows. Working payloads are explicitly
transient until sealing; frozen previous inputs are never writable.

Each generation records shapes, full streaming digests and per-row hashes.
A preparation transaction blocks ordinary reads until all rows commit.
Before overwriting a state/residual pair, the store synchronizes old and
new row copies and commits a checksummed write-ahead record. It writes
the destination rows, commits progress, then removes the journal. Recovery
verifies durable copies before redoing interrupted updates. A partial row
write is recoverable without keeping a duplicate full state.

Operator workers read the same immutable prepared correction generation
and write disjoint rows of a reserved residual. Every read checks its
generation token and row hash. Duplicate writes must agree. A complete
new generation commits before retirement of the old correction payload;
a durable retirement record lets recovery finish interrupted deletion.
A shared file lock serializes reservations, metadata and row commits.

Every output reserves its complete logical length before writes. The hard
cap is 2 GiB **per owned working store**, including a 64 MiB reserve for
prospective integration work; actual metadata/journals are also counted.
Oversized reservations fail before creating a file. Reservations may be
sparse: they do not guarantee physical disk allocation or aggregate RAM.

All completed stores are sealed. The independent review checks current
file and row hashes, 46 historical generations and 23 retirement records
across 24 stores. Their retained payloads total 101,567,858 bytes.
Historical hashes for overwritten/retired data are not claims that those
payloads remain available. Correctness uses the current generation and
arithmetic certificate.

## 3. Interruption and corruption evidence

Source 544 uses child processes that exit immediately without Python
cleanup at nineteen distinct boundaries: initialization; preparation
intent; uncommitted/committed journal copies; partial/full writes of each
row; progress commit; journal removal; generation commit; operator intent
and partial/full/progress writes; and retirement boundaries. Children
inherit the wrapper's private process group and timeout. Every interrupted
case recovers and agrees byte-for-byte with its expected final result.

Four additional checks reject an altered committed row, altered journal
blob, damaged metadata and a journal from a stale generation. The bad
journal is rejected before destination payloads change. Recovery is
idempotent. Mixed-generation reads, stale tokens, conflicting retries
and writes to sealed stores are rejected.

A saved actual P=1600 transition tests all 174 rows, interrupting state
row 83 halfway through. Its explicit weighted addition passes 2,227,200
coordinate checks; the final state/residual matches all 41,643,768
reference bytes. This storage control uses saved correction/residual
outputs, without recomputing their arithmetic.

A separate two-row synthetic control uses target widths: 6,996,660
weighted bytes and 2,159,040 scaled-residual bytes per input row. It
interrupts the second auxiliary row halfway through and recovers all
18,277,080 final bytes. These arbitrary bytes test storage widths, not
target harmonic arithmetic.

There are 22 intentional interrupted child processes including the
corruption setup and these two additional cases. They are passing-test
events, not failed bounded jobs. **Power loss, filesystem failure and
hardware faults are not tested.** The fsync/atomic-replacement calls do
not turn process-interruption tests into universal durability guarantees.

## 4. Fresh arithmetic through the journal

Source 545 starts from the frozen first P=1600 column-0 checkpoint with
residual lower bound u=800 and recomputes the entire r=32 correction to
u=833. This goes beyond replaying saved output bytes.

Preparation performs all 348 original low-RHS actions, streams the
existing 100-bit factor through 1226 blocks and rebuilds every original
sparse low equation. All 44,544 scalar equations pass. The new process
replaces the factor's hash callback with the streaming helper; frozen
source files are unchanged. Prepared state/correction outputs match all
2,227,200 and 1,113,600 reference coordinates respectively. The journal
performs the in-place preparation.

Six separate GMP jobs then calculate all 348 correction child actions
and write newly calculated residual rows directly into the reserved
store. They check low equations, weighted projection and exact divisions
for u=833. All 1,067,664 new residual coordinates match the reference.
The committed state has 28,831,800 bytes; its residual has 12,811,968.
The integrated store's largest observed logical occupancy is 123,374,413
bytes, including its 64 MiB reserve and metadata.

Preparation takes 78.143 seconds including receipt overhead: 62.281 for
RHS actions, 7.488 for the factor solve, 4.899 for original sparse checks.
The six operator jobs finish in about 40.6 seconds with three workers.
These are P=1600 measurements, not target forecasts.

Review 546 independently constructs ordinary powers through degree 33
on six child maps. It checks degrees 1,2,33 at states 0,83,173, including
the first upper residual and its weighted/scaled encoding: 72 additional
scalar equations, not a complete independent operator. It also checks
coverage, final hashes, receipts, current journal payloads and every
inherited D130 hash.

## 5. Target capacity and remaining limits

For P=10552 from P=6400, the prospective payloads are:

| Phase | Payloads plus 64 MiB reserve, before metadata |
|---|---:|
| Initialization: weighted plus largest residual | 1,660,200,664 bytes |
| Preparation: weighted, residual and four journal rows | 1,678,512,064 bytes |
| Sweep: weighted plus two largest residuals | 2,035,873,624 bytes |
| Final weighted plus all CM outputs | 1,758,101,464 bytes |

The capacity control reserves complete logical target lengths. Its
occupancy is 2,035,873,922 bytes with owner metadata, below 2,147,483,648.
An allocation one byte beyond remaining capacity is rejected without
creating a file. These large files are not filled with target data and
are retired before sealing the control. Other independent controls use
separate stores; no aggregate concurrent-store cap certificate is claimed.

The largest proposed payload/reserve set leaves 111,610,024 bytes for
metadata. Dynamic enforcement prevents internal over-allocation, but
this is **not yet a complete target lifetime proof**. Multi-digit low
files, interrupted initialization, CM publication and every scheduler
restart state still need integration and explicit accounting.

## 6. Next execution and mathematical scope

Source 547 is next unused. Implement the complete staged driver with
weighted input/output, generation-bound reads and this journal. Make
low-RHS chunks and multi-digit low stages independently capped and
resumable; save authenticated low answers before state updates. D130's
seven-stage control is available, while source 545 integrates only the
100-bit solve. A complete driver must resume arithmetic phases as well
as recover the underlying storage.

Initialization can use previously certified weighted moments directly:
the old error in moment k is at least pi^(S-k), and the new original
operator contributes pi^k, giving uniform seed accuracy modulo pi^S.
Restore exact masses and account for the omitted k>=S tail by the same
bound. This is D121's coefficient argument at old precision S. Verify
old overlaps and all final weighted equations in the complete driver.

Supply the full live-file inventory, an explicit single-working-store
schedule and a separate concurrent-RAM budget. Then select the first
actual higher-precision column after those gates pass. D130's 9--14
ideal-worker-day estimate is the **pre-redesign baseline**; D131 does
not recost the full target schedule. No automatic doubling or full-bank
launch follows from these controls.

Keep the [arithmetic construction specification](arithmetic-construction-d130.md)
on the research path. Marked P32/B3, the double-cover character and
arithmetic twist, actual Y64 sections, combined genus64/degree51 torsion,
global F256 action and original-kernel coefficient certification remain
open. D120's norm-97 separation stays settled. D130's twist witness still
rules out identification from the chosen local comparison and ramification
support alone. Storage progress does not close these mathematical gaps.

Freeze successful 541--546, the coordinator, successful artifacts,
sealed stores, this report, ledger and review, preserving all prior
freezes. No earlier payload is removed; there is no correspondence,
remote launch, cap increase or target-polynomial claim.

