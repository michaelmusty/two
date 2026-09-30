# D126: selective reads, bounded scratch, and streamed low solves

Completed 2026-09-28. All 22 bounded input jobs pass. These controls remove
specific memory and checkpoint-retention obstacles without changing the
certified harmonic precision. The full bank remains P=800; column 0 is
also certified at P=1600. No positive exact quadric zero, candidate
identification or target field polynomial is proved.

See the [source ledger](../data/computed/dyadic_resource_controls_sources_d126.json)
and [fixed review](../data/computed/dyadic_resource_controls_review_d126.json).
The mathematical comparison and all its hypotheses remain those of
[D125](dyadic-precision800-d125.md).

## Selective state reads

Source 514 hashes complete input files by streaming, then seeks to a
requested state and decodes only that row. It has no decoded bank cache
and does not scan the full bank to choose a common valuation. Taking a
zero common binary shift is valid for these integral inputs. Separate
fresh processes measure projection, uniform-input and weighted-input
controls without first decoding a complete reference bank.

Every one of the 2,227,200 weighted coordinates agrees with the frozen
uniform P=1600 state, and all 174 exact masses agree. Five selected
complete output rows first pass in both representations. Six disjoint
chunks of 29 states then cover every original output row, separately
from uniform inputs and weighted inputs. Both complete sweeps equal the
certified uniform state in all 2,227,200 scalars. The polynomial backend
is the older GMP implementation. The weighted sweep tests full
reconstruction; the uniform sweep tests the original residual.

| Complete sweep | Summed chunk seconds | Maximum single-process RSS |
|---|---:|---:|
| Selective uniform input | 308.531 | 220,938,240 bytes |
| Selective weighted input | 307.492 | 228,753,408 bytes |
| Frozen D124 uniform verification | 293.781 | 504,233,984 bytes |
| Frozen D124 weighted reconstruction | 293.830 | 440,483,840 bytes |

The earlier and new runs had different concurrent loads and plan-cache
policies. This is evidence of lower measured memory, not a measured
elapsed speedup. Sums include concurrent phases and are not CPU time or
coordinator elapsed time. The new code retains only one input row at a
time; the output, polynomial workspace and parameter data also use RAM.

## Rolling scratch and its certificate boundary

Source 515 creates a new, explicitly mutable and marked scratch directory.
It replays the 25 frozen P=1600 checkpoints by copying their payloads;
it does not recompute the refinement. Existing frozen files are only read.
Each generation contains a weighted state, scaled residual and metadata.
Before staging the next generation, the current one is verified and its
older predecessor is retired. An atomic head-file replacement commits
the new generation, retaining its predecessor until the following step.

The maximum generation payload is 43,308,600 bytes. A hard limit of
87,665,776 bytes allows two such payloads plus 1 MiB of metadata. Every
copy observes the cap. The maximum observed occupancy is 84,954,288
bytes. The sealed final directory retains 57,768,619 bytes, including
generations 23 and 24; all files remaining after this control are frozen.
This is a checkpoint-store bound, not a bound for a complete refinement's
additional work files, chunks or final artifacts.

Four child processes deliberately exit during a payload copy, after
generation installation, before head replacement and after head
replacement. Recovery selects the old generation in the first three
cases and the committed new one in the fourth. A deliberately corrupted
new scratch payload is detected and rolls back to its intact predecessor.
The final scratch state passes all 2,227,200 weighted projection checks.
These are successful expected-fault controls, not failed mathematical
jobs. Process interruption is tested; power-loss durability is not.

Permanent history records contain hashes of retired scratch payloads but
do not claim that those payloads remain available for replay. Final
mathematical correctness still requires the final state, exact masses,
original full residual and transport/truncation hypotheses. D125 proves
this boundary: with fixed masses the error satisfies e=T_+e modulo pi^P,
and the positive-column operator is pi-divisible. Iterating P times
forces e=0. Thus correctness does not depend on retaining the iteration
history. Hash records do not replace the original-equation verification.

## Factor and map costs

Source 516 controls a factor reader that decodes one 32-by-32 block at
a time. It groups the lower factors by elimination column and the upper
factors by row, preserving the frozen elimination order. Each of the
1226 blocks is read exactly once per solve, and a block serves every
right-hand-side column before being released. No new factorization is
performed. Every resulting solution is checked in the original sparse
low equations, rebuilt from the transport parameters.

| 200-bit factor control | Decode seconds | Solve including decode | Peak RSS |
|---|---:|---:|---:|
| Resident factors, 2 RHS | 3.948 | 9.209 s | 786,153,472 bytes |
| Streamed factors, 2 RHS | 3.742 | 8.988 s | 293,371,904 bytes |
| Streamed factors, 16 RHS | 3.753 | 18.181 s | 353,501,184 bytes |

The two-RHS answers match in every coordinate. The sixteen-RHS solve
matches those first two columns and passes all 712,704 original sparse
scalar equations. The two smaller solves each check 89,088 equations.
These RHS are unrelated deterministic control vectors, not a new
sixteen-column harmonic refinement. Separate processes provide isolated
peak measurements; the timings are individual bounded observations.

A map-reuse control uses two actual P=800 harmonic columns, five states
and 33 output moments. Both cold and reused paths match all 2640 scalars.
Grouping identical maps uses eight preparations instead of twenty while
retaining one prepared map. Totals are 1.985 and 1.764 seconds in one
fixed-order experiment; this does not establish a target-size speedup.

Source 517 combines selective reads, one prepared map at a time and
streamed factors. It reconstructs all positive low moments 1..32 for
actual P=800 columns 0 and 1, matching 89,088 known scalars and all 348
masses. A separate phase reconstructs the first actual P=1600 correction
after its known binary scaling, matching 44,544 scalars and 174 zero
masses. Both also satisfy every rebuilt original sparse low equation.
They retain 165 prepared maps sequentially, never simultaneously.

The two-column harmonic control takes 76.713 seconds and 184,532,992
peak resident bytes. Its RHS construction takes 59.828 seconds, including
2.430 seconds of preparation and 56.232 seconds of map applications;
the streamed solve takes 7.892 seconds. The correction control takes
47.961 seconds and 216,694,784 peak bytes. Transport arithmetic remains
the main measured cost. Factor streaming primarily controls memory;
factor and map reuse alone do not remove the target runtime uncertainty.

## Reassessment and next execution

Retain the candidate and integral-section route. These controls meet the
D125 request to cost selective reads, checkpoint retention, factor
decoding and map reuse before choosing the next actual refinement.
Integrate the controlled pieces in a new driver and first complete
column 1 from P=800 to P=1600, using the existing verified factors. This
advances a new column while testing the complete rolling workflow at an
already costed precision. Include old overlaps, exact masses, weighted
reconstruction, a separate full original GMP residual and direct CM.

Use an explicit prospective scratch namespace and a hard 512 MiB total
scratch ceiling for that P=1600 pilot, including chunks and work files.
The phase inventory must prove this ceiling before launch. Keep final
state/CM/certificates, sources and receipts permanently. Distinguish
retired scratch hash records from retained provenance sources. No old
frozen artifact may be deleted. Source 519 is next unused at this review;
no complete rolling arithmetic driver has yet been executed.

Do not launch a larger full bank or infer complete P=10552 cost from
these controls. A uniform target column still needs 2,423,583,360 packed
bytes, and its weighted state needs 1,217,418,840 bytes. Higher-precision
factor construction, full transport runtime, CM storage and the complete
per-phase disk inventory still require costing. An eventual P=3200
checkpoint seeded from P=1600 would contain at most 169,023,600 payload
bytes, before work files and final uniform outputs. This is an exact
layout calculation, not a run or affordability certificate.

The D125 bounds remain 4994/4945/4928 against sufficient
25255/25369/25476. All 6188 quadric balls contain zero, without positive
exact vanishing. W Gaussian remains valuation 1024, error 2025 and
uninverted. Preserve the original kernels, all preceding exact-zero
hypotheses, D99 nonhyperellipticity, D108 spectral rejection and resource
pauses. The marked X40/Y64 covers, genus-64 section and degree-51 torsion
backend, global F256 action, invariant and ramification checks remain
downstream. No correspondence.

## Review and resume

All 22 input jobs pass under 180-second private-process-group caps,
assertions and one BLAS thread, with at most three workers. The longest
job is 77.022 seconds; summed job durations are 853.240 seconds. All owned
workers have returned. The four deliberate child exits are internal
protocol controls and each enclosing job passes.

Source 518 imports no production arithmetic. It independently decodes
all weighted coordinates and masses, checks every output-row digest
against the frozen uniform bytes, reviews complete disjoint sweep
coverage, validates the copied checkpoint history and retained scratch,
compares factor-answer digests, and checks every bounded receipt. It
preserves all 8729 D125 source hashes in a fixed manifest, along with this
report and ledger. Creation and `--check` replay use fresh capped receipts.
This preserves the prior mathematical audit; it does not machine-formalize
the geometric arguments or claim new harmonic precision.

Freeze successful 514--518, their control outputs, the sealed scratch,
this report and ledger. After interruption, inspect existing receipts
and partial files before continuing. Never rerun passing phases or edit
their sources. The top of HANDOFF, DECISIONS and REFERENCES records the
current execution state after this fixed report.
