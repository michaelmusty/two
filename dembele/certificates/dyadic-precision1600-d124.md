# D124: actual P=1600 pilot, direct weighted CM and transport controls

Started 2026-09-27; completed 2026-09-28. This continues
[D123](dyadic-staged-pilot-d123.md) toward Dembélé's original residual
kernels. The [source ledger](../data/computed/dyadic_precision1600_sources_d124.json)
records the arithmetic, controls, measurements and unchanged obligations.
The full sixteen-column bank remains P=400. No new full-bank quadric
bound, positive exact zero, candidate identification or target polynomial
is proved by this single-column pilot.

## Actual weighted lift

Source 496 factors the P=1600, r=32 low block in 88.330 recorded seconds.
Every coefficient overlaps the P=800 factor. All 174 diagonal inverse
products and 89,088 scalar equations for two unrelated right-hand sides
pass. The factor payload is 251,084,800 bytes; peak resident memory is
972,111,872 bytes. This is a measured actual factor, not a synthetic cost.

Source 497 and its coordinator implement D123's weighted method with
six chunks of 29 states per sweep and at most three concurrent state
workers. They also split construction of the seed's low right-hand side
into chunks, before a separate factor solve. This avoids extrapolating
the earlier monolithic seed cost beyond the per-job cap.

The seed comes from the certified P=800 column. Restore its exact masses
at the new modulus and apply the original T to reconstruct higher seed
moments before imposing low equations. The inherited input-column bound
v_pi(T_{n,k})>=k controls both omitted old moments and high seed moments.
After low elimination, the active residual starts at valuation 800.

Moments 0..32 retain full precision; higher moment k is stored modulo
pi^(1600-k), using coordinate-specific binary widths. A correction at
residual valuation u uses only k<1600-u. Eliminating the low block gives
gain 33 and the next active band. The twenty-four corrections are

    800 -> 833 -> 866 -> ... -> 1559 -> 1592.

At that point only the 33 low/mass rows remain active and their residual
is zero. The weighted residual criterion is sufficient because
T(I_P) is contained in pi^P for I_P={e:e_0=0, v_pi(e_k)>=P-k}. A full
GMP application reconstructs a uniform P=1600 vector. A second, explicit
GMP application checks every original equation. This older polynomial
backend is separate from the FLINT path used for the corrections.

The final uniform state contains 2,227,200 scalar coefficients and
occupies 55,680,000 bytes. All 1,113,600 old low coefficients and all
2,227,200 extended seed coefficients overlap at the old precision.
Exact harmonic masses are checked at all 174 states. Every sweep is
assembled only after disjoint complete coverage and its input hash have
been verified. Every mathematical phase retains the 180-second private
process-group cap, assertions and one BLAS thread.

All 228 state phases pass. The coordinator takes **1713.775 seconds
(28.563 minutes)**, with 3084.406 summed phase seconds. The latter includes
overlapping jobs and is not a CPU-time measurement. The largest state
phase takes 65.131 seconds. Maximum measured single-process peak resident
memory is **1,127,170,048 bytes**; this does not measure the aggregate of
concurrent workers. The state pilot retains 1,451,881,056 distinct binary
checkpoint bytes, excluding the factor and subsequent CM work. No prior
file was deleted, and no phase was resumed from an earlier invocation.

## CM values and a direct composition route

Source 498 uses the independently established extension route: only the
nine required target states are extended through degree 4798, then all
seventeen CM charts are computed through degree 3199. The four coarse
beta-errors are **[3232,3248,3232,3264]**. There are 435,200 new CM scalar
coefficients; all 217,600 old CM scalars and all 68 old coarse values
overlap the P=800 bank.

A further algebraic observation avoids that 3P state extension. Write a
CM map as g(x)=(A x+B)/(1+C x) and one original child map as
f(x)=(a x+b)/(1+c x). The actual CM maps have C in pi O. Set d=1+C b;
it is a unit. The composite has normalized parameters

    a'=(A a+B c)/d,  b'=(A b+B)/d,  c'=(c+C a)/d,

and determinant

    a'-b'c' = (A-BC)(a-bc)/d^2.

Thus c' and a'-b'c' belong to pi O. Its positive input column k is
divisible by pi^k, just as for an original child map. Since the actual
state at an edge is the sum of the transported child states, composing
the CM map with these children computes the same CM distribution.
Weighted input precision P-k therefore suffices directly for every CM
moment at uniform precision P. Only P input moments are required;
the omitted tail also vanishes modulo pi^P. This applies independently
of the harmonic basis column.

Source 500 implements the composition using integral Newton inversion
of d. Separate integer quotient arithmetic checks all three normalization
identities, the determinant identity, and the c'/determinant valuations
for all 34 composed maps. It compares every resulting CM moment with
the separately computed bank. The P=800 control passes in 11.669 seconds,
checking 217,600 scalars. The uniform state is read only to validate the
weighted input; it and the 3P extension are not used in the CM calculation.

The P=1600 direct control also passes, checking all 435,200 CM scalars in
35.561 recorded seconds. The separate extension, two chart batches and
coarse assembly take 23.149, 27.863, 24.765 and 10.059 seconds respectively.
These phase durations may overlap and are not an elapsed total.

All four source 499 audits pass without importing production arithmetic.
The state audit checks exact masses, 348 child-column divisibility
conditions, complete coverage of 29 sweeps, all saved residuals and old
low overlaps, plus 160 independent recurrence scalars. The seed audit
checks all 2,227,200 extended overlaps and 24 high-seed recurrence scalars
at degrees 800,1199,1599. The coarse audit independently reconstructs all
68 values with an alternate binomial/Horner formula and checks all
217,600 old CM overlaps. The weighted audit checks all 25 checkpoints:
55,680,000 state scalars and 14,094,000 scaled residual scalars, all
correction gains and the final weighted overlap.

Recorded audit times (state, seed, coarse, weighted) are 33.420, 64.132,
12.238 and 52.003 seconds. Their peak resident memory is 418,054,144;
356,646,912; 102,203,392; and 587,694,080 bytes respectively. Full original
residuals use the older GMP backend; the independent recurrence audit
is sampled. These finite arithmetic checks do not machine-formalize the
geometric arguments or prove an exact positive quadric zero.

## Small-product acceleration and its limits

Source 501 profiles five actual low-row equations from the first P=1600
correction and checks them with the older GMP backend. Repeated small
polynomial products contribute substantial overhead. Its profile also
includes repeated whole-input scans for the separate sampled states;
those scan timings must not be extrapolated to one full state chunk.

Sources 502--503 move the already proved carry-free small-product packing,
GMP multiplication and degree-eight field reduction into C. Products
with at least 24 outputs retain frozen source 476's FLINT implementation.
The packing has fifteen slots per moment coefficient and enough guard
bits for every convolution sum, followed by exact reduction by f(b).
The existing D120 carry bound and D122 large-product proof apply; this
introduces no new external theorem or division by an even integer.

All 172 independent product controls pass at binary precisions
1,3,25,50,100,200,1319,1536. They include maximal coefficients, zero
products, truncation and both sides of the dispatch boundary. Full actual
P=800 equations and P=1600 correction low equations additionally check
33,320 scalars against both older backends.

On the same five-state samples, without profiling, full P=800 transport
takes 2.715 seconds with the previous mixed backend and 1.861 seconds
with the new path. The low-row sample falls from 1.726 to 0.957 seconds.
These are component timings, not complete-solver speedups. The running
P=1600 production driver remained unchanged throughout this experiment.

A synthetic P=10552 action takes 1.586 seconds preparation plus 24.653
seconds application with the new path. All 84,416 output scalars agree
with a complete older-GMP computation, which takes 1.949 plus 29.426
seconds in the same job. This does not establish an improvement over the
historical FLINT-only target timing under different load, and it does
not cost a full solve. The remaining large-action expense is real.

## Reassessment and continuation

The actual P=1600 pilot establishes that weighted refinement, seed
construction, final residuals and CM evaluation can be completed inside
the per-phase time and measured memory limits. The direct CM composition
and compiled small products provide useful improvements for subsequent
runs. They do not close the global precision gap by themselves.

The next priority is a complete P=800 bank and a new quadric falsification
check, rather than another isolated higher-precision column. Incorporate
the controlled small-product path and direct weighted CM calculation into
a new resumable driver; refine columns 1..15 from their frozen P=400
states and reuse column 0's already certified P=800 data. Verify each
original full residual and every old overlap. Consolidate all 1088 coarse
values, then recompute the residue frame, quadrics and anchor-dependent
section bounds and audit them independently. Do not infer new global
bounds from this single P=1600 column. Record cost and memory before
choosing the next full-bank precision or the conditional P=10552 target.

## Provenance and resume rule

All **242 input jobs pass**, with no failed mathematical attempt. This
includes one factor, 228 state phases, four CM phases, four independent
audits, two composed-CM controls, one profile and two native-kernel
controls. The longest job takes 88.330 seconds; summed job durations
are 3551.715 seconds, not an elapsed or measured CPU total. All workers
and the pilot coordinator have returned.

Final review 504 checks these receipts, payloads, source hashes and all
2532 inherited D123 hashes. Run its creation and then its fixed-manifest
`--check` replay through the persistent capped wrapper, with fresh
receipt names. Successful sources 496--503 and the weighted coordinator
are frozen. After that review passes, freeze 504, this report, the ledger
and the resulting fixed manifest too. Future work uses new sources;
505 is next. Resume after a transport interruption by inspecting receipts
and partial outputs before starting anything again.

Retain all prior freezes and resource pauses, D99 nonhyperellipticity,
D108 spectral rejection and the original residual kernels. D122's
accepted section bounds remain 4194/4145/4128 against sufficient
25305/25419/25526. W's Gaussian remains certified nonzero, valuation
1024 with error 1225, and has not been inverted. Higher intrinsic jets
still require the preceding exact zeros. The marked X40/Y64 covers,
genus-64 section and degree-51 torsion backend, global F256 action and
final invariant remain downstream requirements. No correspondence.
