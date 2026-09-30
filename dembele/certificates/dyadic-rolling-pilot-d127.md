# D127: complete rolling refinement and reuse of low factors

Completed 2026-09-28. All 235 bounded input jobs pass, with no failures.
This work advances column 1 from P=800 to P=1600 using the controlled
methods of [D126](dyadic-resource-controls-d126.md). The full bank remains
P=800. Exact curve identification and the target field polynomial are
still open.

See the [source ledger](../data/computed/dyadic_rolling_sources_d127.json)
and [fixed review](../data/computed/dyadic_rolling_review_d127.json).

## Arithmetic workflow and storage boundary

Source 519 retains the weighted proof, r=32 Schur correction and full
original GMP verification of source 505. It substitutes D126's selective
child-state reader for whole-bank input decoding in operator sweeps,
streams the 1226 existing low-factor blocks, and prepares maps one at a
time when constructing correction RHS. The low solve uses the previously
certified P=400, 800 or 1600 factors according to the remaining precision.
No new factorization is required for this P=1600 pilot.

The seed extends the old actual P=800 column with the original operator,
restores exact masses at the new modulus and solves the low block. After
its residual is checked, 24 corrections raise the weighted residual
bound from 800 to 1592 in increments of 33, leaving 33 active moments.
Moments 0..32 keep full precision; moment k>32 keeps precision P-k.
A full GMP application reconstructs uniform moments through degree 1599.
A second full GMP application checks every original equation. These two
sweeps are separate from the adaptive polynomial backend used in the
refinement. Old low and extended-seed overlaps and exact masses remain
required. The coordinator schedules six chunks of 29 states per sweep,
at most three simultaneously, and 228 mathematical phases in total.

The new namespace `dyadic_rolling_scratch_col01_d127` is explicitly
temporary until its final seal. No earlier frozen file is deleted or
changed. Every mathematical phase writes permanent metadata, a log and
a capped receipt. The metadata is hashed into its log before the pass
marker, so resumption can authenticate it even after temporary payloads
have been retired. The coordinator only skips an already passing phase
when its command and driver/log/metadata hashes agree. It refuses an
unresolved partial phase. A process lock prevents duplicate coordinators.
This pilot completes without an interrupted or resumed phase. D126's
deliberate interruption tests concern its separate checkpoint store;
no crash is injected into this complete arithmetic coordinator.

At each serial barrier, source 520 writes an immutable retirement record
before deleting any obsolete payload. That record is anchored to the
passing receipt and identifies both the files retained and those retired.
After interruption, deletion authorized by the latest record can finish
without rerunning mathematical work. The previous complete checkpoint is
retained through preparation and until its successor passes. Initial
input and extended-seed chunks are kept until the final checks, allowing
all extended old-precision overlaps to be compared directly. The final
uniform state, full original zero residual, weighted state and its last
scaled residual are retained and the directory is sealed.

Permanent records of retired hashes are history, not available payloads.
The new manifest deliberately excludes retired binaries. Final moment
correctness uses the iteration-independent certificate from D125: exact
masses, every original residual equation and the transport/truncation
proof. If e is the difference from the actual moments, e=T_+e modulo
pi^P and T_+ is pi-divisible, so P iterations force e=0. No history hash
is being substituted for an original-equation check.

## Preflight storage bound

The hard scratch limit is **536,870,912 bytes (512 MiB)**. Each write
holds a shared advisory lock, checks current occupancy plus its entire
new payload against the limit, writes and synchronizes the payload, and
checks occupancy again. Thus concurrent workers cannot individually
reserve the same free space. The static phase inventory deliberately
overcounts mutually exclusive work slots:

| Slot | Maximum bytes |
|---|---:|
| Old seed input | 27,840,000 |
| Extended-seed chunks | 55,680,000 |
| Two complete checkpoints | 86,617,200 |
| Newly prepared weighted state | 28,831,800 |
| Prepared correction | 14,476,800 |
| One active operator sweep | 55,680,000 |
| Assembled uniform state | 55,680,000 |
| Final full residual | 55,680,000 |
| Scratch metadata allowance | 1,048,576 |
| **Conservative total** | **381,534,376** |

Cleanup leaves at most two complete checkpoints and, during preparation,
one new weighted state/correction. A serial barrier consumes one complete
sweep before another starts. Seed and final assembly fit the larger
uniform slots. All these sizes use the exact binary codecs, including
ceilings for partial bytes. Permanent receipts and phase metadata are
outside the scratch namespace. Source 523 independently replays allocation
and retirement sets, recomputes each binary size, and compares every
barrier byte count with the recorded execution.

Selective sweeps and streamed factors do not yet make every phase use
only a few state rows. Serial assembly and correction preparation still
decode their required complete arrays. This pilot measures their memory;
it does not certify target-size RAM or complete P=10552 cost.

## Direct CM and independent audit

Source 521 computes all 17 CM charts from the final weighted state using
the controlled composed maps. It checks every weighted projection against
the retained uniform state using selective reads, all 34 composition and
divisibility identities with separate integer quotient arithmetic, old
CM overlaps, exact zeroth moments and all 68 old coarse values. The new
CM cutoff is degree 3199 and the certified beta-errors are
[3232,3248,3232,3264]. No 3P state extension is used.

Source 522 imports no production arithmetic. Its four bounded phases
check the retained full residual, all old low overlaps and exact masses,
348 divisibility hypotheses, sampled original and high-seed recurrences,
all 68 coarse values through an alternate Horner formula, sampled CM
recurrences, and every coordinate of the final weighted state. It checks
all 29 sweep coverages and 25 checkpoint metadata records. It explicitly
does not claim to replay retired intermediate states or extended-seed
payloads. Those omissions do not weaken the final original-residual
certificate; the geometric argument itself is not machine-formalized.

## Higher precision without a new low factor

Let A be the original low matrix at binary precision 2m, and suppose an
existing verified factor solves A modulo 2^m. For an arbitrary RHS b,
first compute x0 from that factor. Then r=b-A*x0 is coefficientwise
divisible by 2^m. Solve A*d=r/2^m modulo 2^m using the same factor and put
x=x0+2^m*d. Direct substitution gives A*x=b modulo 2^(2m). Division is
exact division of known integer coefficients; no nonunit is inverted in
the coefficient ring. The final residual is checked at the higher
precision, using original transport coefficients.

Source 524 controls this construction at P=1600 and P=3200 on two
unrelated RHS. The P=1600 case also compares against the existing full
P=1600 factor. The P=3200 case requires only the existing P=1600 factor.
These are low-system controls, not actual P=3200 harmonic moments.

For a future P=1600-to-3200 refinement, this can handle the full-precision
seed low solve, while all correction solves already require at most the
existing P=1600 factor. The cost of building a new P=3200 factor can
therefore be avoided. Both controls pass all 89,088 higher-precision
original sparse scalar equations and all 89,088 exact divisibility
checks. At P=1600 every solution coordinate also matches the existing
full-precision factor. The P=1600/P=3200 jobs take 40.612/40.359 seconds
with peak resident sizes 346,849,280/316,194,816 bytes. These direct
low-system residual checks use the production matrix kernel; they are
separate from source 522's independent arithmetic audit of actual moments.
Remaining gates are the
P=3200 original-transport timings, bounded RHS phases and the complete
memory/disk inventory. None is inferred from the factor control alone.

## Results, decision and provenance

All 228 state phases pass, including all 2,227,200 original residual
scalars, 1,113,600 old low overlaps, 2,227,200 old extended overlaps and
174 exact masses. The 24 corrections take the weighted residual bound
from 800 to 1592. All 435,200 new CM scalar coefficients, 217,600 old CM
overlaps and 68 old coarse values pass. The four independent audit phases
pass with the scopes described above.

The state coordinator takes 1276.888 seconds. Summed state phase durations
are 2405.241 seconds, including concurrent jobs; this is not CPU time.
The longest state phase is 57.986 seconds. Final uniform assembly reaches
1,117,175,808 peak resident bytes, the highest single-process measurement.
Thus the scratch integration succeeds, while whole-array serial assembly
remains a memory obstacle for larger precision. No aggregate RAM bound
or target-size runtime is inferred from these numbers.

All 235 input jobs use the unchanged 180-second private-process-group
cap, assertions and one BLAS thread, with at most three workers. Summed
input job durations are 2642.670 seconds; the longest job is the
65.949-second independent high-seed audit. No successful job is rerun.

Maximum observed scratch is **308,327,101 bytes**, below the conservative
381,534,376-byte inventory and hard 512 MiB cap. Fifty-four retirement
barriers remove 248 prospectively temporary payloads totaling
1,311,643,320 bytes. Four final payloads occupy **140,237,736 bytes**;
the complete sealed directory occupies 140,238,953 bytes. The direct CM
binary adds 10,880,000 retained bytes outside that namespace. The old
frozen artifacts remain intact. Source 523 independently recomputes all
252 distinct payload sizes and replays every live set and barrier count;
it never treats a retired hash as an available payload.

Decision: retain the integral-section route and use the complete rolling
workflow for future refinements. Before a P=3200 column, replace serial
whole-bank assembly/preparation with selective row processing, control
those phases against retained actual P=1600 data, and measure bounded
P=3200 original-transport and RHS chunks. Use the existing P=1600 factor
through the exact residual lift above instead of building a P=3200
factor. A new phase inventory must cover all scratch, final state and
CM files; the 512 MiB P=1600 cap is not automatically a P=3200 cap.
Source 525 is next unused at this review. A larger full bank and the
complete conditional P=10552 solve remain uncosted.

The full sixteen-column bank remains P=800; columns 0 and 1 are now
certified at P=1600. The D125 section bounds remain 4994/4945/4928,
anchors 4776/4448/4184 and sufficient nonanchor thresholds
25255/25369/25476. All 6188 quadric balls contain zero. W Gaussian remains
nonzero at valuation 1024, error 2025 and relative precision 1001, and is
uninverted. Higher isolated columns do not improve these full-bank bounds.

Source 523 binds the prior 8816 D126 hashes, every new passing input
receipt, the retained final artifacts, this report and the ledger. Its
creation and fixed-manifest replay have separate fresh capped receipts.
Successful sources 519--524, final artifacts, permanent phase metadata,
retirement records and the sealed scratch directory freeze. The finite
review does not machine-formalize the geometric proofs. All caps, earlier freezes,
original kernels, D99/D108 decisions and exact-zero prerequisites remain.
The marked covers, genus-64 section/degree-51 torsion backend, global
F256 action, final invariant and original-kernel/ramification checks
remain downstream. No correspondence.
