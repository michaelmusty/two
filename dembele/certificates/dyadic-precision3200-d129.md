# D129: streamed refinement of one actual column to P=3200

Completed input arithmetic and independent checks, 2026-09-28. All
1934 bounded input jobs pass, with no failed receipt. Column 0 now
reaches P=3200; column 1 reaches P=1600. The full sixteen-column bank
remains at P=800. Exact positive
quadric vanishing, candidate identification and the target field
polynomial are still open.

The [source ledger](../data/computed/dyadic_precision3200_sources_d129.json)
records completed receipts and the
[fixed review](../data/computed/dyadic_precision3200_review_d129.json)
checks preservation of all 9648 source hashes from
[D128](dyadic-selective-scaling-d128.md).

## Arithmetic certificate

Source 528 integrates D128's selective serial arithmetic and original-map
controls into an actual P=1600-to-P=3200 refinement of harmonic column 0.
Every long input is read one state at a time. Serial phases retain the
fixed 174-by-32 low system and a constant number of long rows, rather
than decoding a complete long state bank. Existing adaptive polynomial
arithmetic is used for refinement; the final reconstruction and separate
full original residual use the GMP backend.

The old actual P=1600 moments are extended by the original operator and
their exact masses restored. The seed low solve uses the already frozen
P=1600 factor twice: first solve modulo 2^200, divide the original
400-bit residual coefficientwise by 2^200, solve that quotient with the
same factor, and add the shifted correction. Exact divisibility and all
44,544 original sparse scalar equations are checked. This decodes 2452
existing factor blocks and builds no new factorization.

The r=32 weighted correction increases the residual lower bound by 33
pi-digits per step. Starting at 1600, 48 corrections reach 3184 and leave
33 active moments. Moments 0 through 32 retain full precision; moment
k>32 retains pi-precision P-k. Low right-hand sides are computed in six
chunks of 29 states before each serial solve and state update. Full
operator sweeps use 29 chunks of six states. Source 529 permits at most
three concurrent mathematical workers. The complete state schedule
has 101 sweeps, 1802 sweep jobs, 102 serial arithmetic jobs and one
writer control: 1905 capped jobs in total.

Uniform reconstruction must agree with every weighted projection and
with both the old low moments and the original extended-seed values at
old precision. A second full application must give zero in all 4,454,400
original scalar residuals, with all 174 masses exact. The final proof
does not depend on retaining iteration history: the difference e from
the actual moments has zero masses and satisfies e=T_+e modulo pi^P.
Every positive input column of T_+ is pi-divisible, so P iterations
force e=0. The original transport and tail hypotheses are inherited
from D125 and its predecessors. This is a mathematical argument with
finite arithmetic checks, not a machine-formalized geometric theorem.

## Streamed writes and file lifetimes

The new directory `dyadic_streamed_scratch_col00_d129` is explicitly
temporary until final sealing. No earlier frozen file may be changed
or deleted. Each new binary reserves its complete final length under
a shared advisory lock, after checking total logical occupancy against
the hard cap. The file is then filled one row at a time without holding
the lock. Every append checks its exact length, coordinate bounds and
required binary shift; completion checks the final position and file
length, synchronizes the file and records its hash. Reservations count
against the cap before any concurrent row write can consume them.

This controls logical file lengths, not physical filesystem allocation
or aggregate resident memory. A partially written reserved file remains
visible and cannot be mistaken for a passing checkpoint. The initial
writer control interleaves two reserved outputs, compares all 11,376
bytes, and rejects a wrong-length row and an oversized reservation. It
does not inject a process crash or test power-loss durability.

The hard scratch cap is **2,147,483,648 bytes (2 GiB)**. The conservative
inventory deliberately overcounts mutually exclusive slots:

| Slot | Maximum bytes |
|---|---:|
| Old seed input | 111,360,000 |
| Extended-seed chunks | 222,720,000 |
| Two complete checkpoints | 338,047,200 |
| Newly prepared weighted state | 113,343,600 |
| Prepared correction | 55,680,000 |
| One active operator sweep | 222,720,000 |
| Assembled uniform state | 222,720,000 |
| Final full residual | 222,720,000 |
| Scratch metadata allowance | 1,048,576 |
| **Conservative total** | **1,510,359,376** |

The largest serialized state row is 1,280,000 bytes. Permanent phase
metadata, logs and capped receipts live outside this scratch budget.
Every phase hashes its metadata into its log before the pass marker.
Resumption requires matching command, driver, log and metadata hashes;
an unresolved partial phase is refused. A coordinator lock prevents a
second coordinator from sharing the namespace.

At each serial barrier an immutable journal identifies the passing
receipt, all live payloads and the subset to retire, before deletion
starts. Only payloads in this new temporary namespace are eligible.
Two complete checkpoints are kept through correction preparation; the
old input and extension chunks survive until all final overlaps pass.
The final seal retains four payloads: uniform moments and their full
zero residual, the final weighted state and its last scaled residual.
Their declared total is 558,829,536 bytes. The 103 scheduled barriers
allocate 1954 distinct payloads and retire 1950.

Review 532 independently recomputes each declared payload size from its
codec, replays every allocation and retirement set, checks every barrier
occupancy and verifies the retained files and seal. Retired hashes are
historical records, not retained sources or a replay of their contents.

## Direct CM and separate integer arithmetic

Source 530 computes all 17 CM charts using the controlled composition
with original child maps. Separate integer quotient arithmetic checks
all 34 composition and divisibility identities. Each chart checks its
exact mass and every old CM overlap. The cutoff is degree 6399; the
four coarse beta-errors are [6432,6448,6432,6464]. The CM output contains
870,400 scalar coefficients, with 435,200 old scalar overlaps and 68
old coarse values. Six bounded chart jobs retain 43,520,000 bytes; a
seventh job assembles their metadata and coarse values without writing
a duplicate binary. These permanent CM outputs lie outside scratch.

Source 531 imports only the separate integer audit arithmetic, not the
production solver. It selectively reads retained rows and checks:

- The full zero residual, all 2,227,200 old low overlaps, all exact
  masses, 348 original-map divisibility hypotheses, 96 sampled original
  recurrence scalars and the complete disjoint coverage of 101 sweeps.
- Every one of the 4,454,400 final weighted projection coordinates,
  all 45,936 final scaled residual coordinates, 49 checkpoint metadata
  records and the 48 recorded correction gains.
- Ordinary formal power recurrences for the two children of state 0,
  in sixteen blocks of at most 400 degrees. At degrees 1600, 2399 and
  3199 their sums must agree with the new uniform moments reduced to
  old precision, giving 24 independent scalar checks. The sixteen
  retained power checkpoints total 5,120,000 bytes outside scratch.
- All 68 coarse values through an alternate Horner formula, all old
  CM overlaps and 72 sampled CM recurrence scalars in three chart jobs.

These are 22 independent audit jobs. The all-coordinate original
residual is computed by the production GMP path; the independent
ordinary recurrence checks are samples, not a second full recomputation.
The audit explicitly does not replay retired intermediate production
states or seed chunks. Source 532 authenticates the finite certificate
chain and preserved D128 hashes without importing production arithmetic.

## Execution results and next decision

All 1905 state jobs pass, including 48 corrections and the separate
full original residual. All seven CM jobs and all 22 independent audits
also pass. Every mathematical job uses the unchanged 180-second private
process-group cap, assertions and one BLAS thread. Both schedulers enforce
at most three workers; the check scheduler waits for the state summary,
seal and released coordinator lock before launching any worker.

The state coordinator takes 4245.664 seconds. Summed state phase
durations are 10562.838 seconds; summed input durations are
11115.625 seconds. These are sums of elapsed job times, including
concurrent jobs, not CPU-time measurements. The longest state/input jobs
take 52.191/94.767 seconds. The highest measured single-process
input resident peak is 491,929,600 bytes. Selective serial processing
removes the prior complete-bank decoding, but no aggregate RAM bound or
target-size runtime follows from this measurement.

Maximum observed scratch occupancy is 1,229,041,837 bytes, below both the
1,510,359,376-byte conservative inventory and the enforced 2 GiB cap.
All 103 retirement barriers complete. They retire 1950 temporary payloads
totalling 9,302,747,376 bytes; four retained payloads total
558,829,536 bytes. The sealed directory occupies 558,830,756 bytes.
Every earlier frozen artifact is preserved. The state/check schedulers
resume 0/0 prior phases; no injected crash is claimed.

Sources 528--532, both operational schedulers, successful artifacts,
permanent phase/retirement records and sealed scratch freeze on their
first pass. This report and ledger freeze at the first passing fixed
review. Review creation and fixed-manifest replay have separate capped
receipts; their measured outcomes are recorded in the entry-point docs.
Do not rerun completed jobs or coordinators.

The next question is target-size feasibility, rather than automatically
producing every intermediate-precision column. Before another complete
refinement, control individual original-map actions at P=10552, including
full, low-RHS and seed-extension shapes. Split by child and backend where
needed to preserve the 180-second cap. Actual old moments can control
extension overlaps; dense synthetic vectors can compare full/RHS
backends but cannot certify a new harmonic column. Sample timings must
remain labelled as samples and feed a complete phase and storage budget.
Compare a staged precision ladder with a direct jump when budgeting the
remaining residual work: their correction precisions differ, so a single
target-size timing cannot choose the cheaper schedule. D126's measured
multiple-RHS factor reuse is another input to that comparison, not a
certificate that a complete batch of large columns fits current resources.

No target-size low factor is forced by the higher modulus. If
A*x=b modulo 2^s and d<=200, set c=(b-A*x)/2^s modulo 2^d, solve
A*z=c modulo 2^d using an existing factor, and replace x by x+2^s*z.
Direct substitution gives the next s+d bits. Exact coefficient divisions
and original residuals must be checked at each stage. Thus seven blocks
of at most 200 bits could reach the target's 1319 bits without a new
factorization. This generalization is a proposed control, not an executed
target-size solve; its phases must be split and timed before integration.

The eventual retention policy also needs a fresh prospective inventory.
A P=10552 uniform column alone occupies 2,423,583,360 bytes, and its
weighted state occupies 1,217,418,840 bytes. Retaining the current four
dense state payloads for every target-size column, plus all CM data,
would exceed the approximately 80 GiB available at this checkpoint.
Future verified zero residuals may use a lossless compact encoding, and
weighted projections may be regenerated from retained uniform moments;
both changes need their own byte-for-byte controls and review. Nothing
in that prospective design authorizes changing any existing frozen file.
The complete sixteen-column P=10552 calculation remains uncosted.

The global P=800 section lower bounds remain 4994/4945/4928, anchor bounds
4776/4448/4184, sufficient non-anchor bounds 25255/25369/25476 and gaps
20261/20424/20548. All 6188 quadric balls contain zero; this is not exact
positive vanishing. W Gaussian remains nonzero with valuation 1024,
error 2025 and relative precision 1001, and remains uninverted. A single
higher-precision column cannot raise the complete-bank section bounds.

Preserve D99's nonhyperellipticity, D108's spectral rejection, the
original residual kernels, every preceding exact-zero prerequisite and
all resource pauses. Marked X40/Y64 realization, the genus-64 section
and degree-51 torsion computation, global F256 action, the degree-257
invariant and original-kernel/ramification checks remain downstream.
No correspondence is sent.
