# D123: one actual P=800 column and shrinking corrections

Date: 2026-09-27. This continues the original-kernel construction after
[D122](dyadic-precision400-d122.md). One actual harmonic column now has
P=800 pi-digits, including all seventeen CM charts and four coarse
coefficients. The full sixteen-column bank remains P=400. The previously
accepted quadric bounds, W Gaussian, global height budget and geometric
obligations therefore remain unchanged. No positive exact quadric zero,
candidate identification or target field polynomial is proved.

The [source ledger](../data/computed/dyadic_staged_pilot_sources_d123.json)
separates the actual refinement, independent arithmetic, weighted-input
control and shrinking correction experiment. Sources 491 and 494 import
only source 486's independent integer quotient arithmetic, without the
production multiplication or transport implementations. Source 495 binds
their coverage and provenance; it is not another arithmetic implementation.

## Actual refinement and CM values

Source 488 constructs the P=800, r=32 sparse low-block factor in 64.745
recorded seconds. All factor coefficients overlap the frozen P=400 factor.
All 174 diagonal inverse products and 89,088 scalar equations from two
unrelated right-hand sides pass. Its packed factor has 130,564,096 bytes.

Source 489 generalizes the lift and splits each original-operator sweep
into six immutable chunks of 29 states. The coordinator runs at most
three chunks concurrently, verifies complete disjoint coverage and input
hashes, and resumes only from successful receipts. The initial seed first
applies the original operator to the old P=400 moments to reconstruct
the higher seed moments. Those moments cannot simply be set to zero
and declared correct to precision 400. Exact harmonic masses are restored
before seed extension, and the low residual is eliminated afterward.

The actual correction precisions are

    400 -> 433 -> 466 -> 499 -> 532 -> 565 -> 598 -> 631 -> 664 ->
    697 -> 730 -> 763 -> 796 -> 800.

All 126 state phases pass, with 538.595 seconds coordinator elapsed time
and 895.733 summed phase seconds. The latter includes overlapping jobs;
it is neither elapsed time nor a measured CPU-time total. The largest
state phase takes 63.167 seconds. Every mathematical phase retains the
180-second private-process-group cap and one BLAS thread.

The final original residual uses the older GMP polynomial backend,
separate from FLINT multiplication used for the lift. All 1,113,600
scalar coefficients of the state equations pass. All 556,800 old low
coefficients and 1,113,600 old-precision extended coefficients overlap.
The state and zero residual each occupy 14,476,800 bytes. These are actual
precision-800 moments by fixed-mass contraction, not merely a formal
increase of the arithmetic modulus.

Source 490 extends only the nine required target states through degree
2398 and computes all seventeen CM charts through degree 1599. The four
coarse beta-errors are **[1632,1648,1632,1664]**. All 108,800 old CM-moment
scalar coefficients and all 68 old coarse values overlap. The new CM bank
contains 217,600 scalar coefficients. Its four phases take 7.374, 8.914,
7.919 and 4.722 recorded seconds, with the two chart phases concurrent.

Source 491 independently checks 160 original recurrence coefficients at
five states and degrees 1,2,33,64; an additional 24 coefficients at seed
degrees 400,599,799; all 68 coarse values through the alternate binomial
kernel and Horner evaluation; all old low overlaps; all thirteen gains;
and complete coverage of all sixteen state sweeps. It passes in 33.996
seconds. The sampled recurrence checks supplement the full production
residual, rather than replacing it.

## Why precision can depend on the moment index

Let T be the original linear moment operator, with zeroth masses fixed.
For each child write phi(x)=(a x+b)/(1+c x), delta=a-bc. The certified
parameters have c,delta in pi O. For positive input index k, expanding
phi(x)^n through powers of delta x/(1+c x) shows that its coefficient
has valuation at least k: each summand contains delta^j c^(k-j).
This holds uniformly in output degree n. Indices beyond a cutoff P
therefore contribute zero modulo pi^P for integral moments.

Define the additive error lattice

    I_P = { e : e_0=0 and v_pi(e_k)>=max(0,P-k) for k>0 }.

Then **T(I_P) is contained in pi^P** in every output coordinate. If a
stored center z has Tz-z in I_P, put y=Tz. Linearity gives

    Ty-y = T(Tz-z) = 0 modulo pi^P.

Its masses are exact, so the inherited contraction theorem certifies y
as the actual full-precision moment vector. Thus a weighted residual
suffices, followed by one original application. Merely having a weighted
state without checking this residual would not suffice.

In the degree-eight Eisenstein basis, the coefficient of pi^i in moment
k needs max(0,ceil((P-k-i)/8)) binary digits. Distinct coefficient valuations
modulo eight make these coordinate masks exactly the ideal pi^(P-k).
A common binary precision for every field coordinate can retain needless
digits near the boundary; the control uses the coordinate-specific masks.

Source 492 selects higher moments from the earliest frozen uniform
checkpoint whose error u satisfies u+k>=P. For low indices 0..32, a zero
low residual and the integral low inverse strengthen the state error to
u+33. At the twelfth checkpoint u=796, that lower bound is 829, exceeding
800. All selected coordinates are compared with the verified full column.
The compact input has **7,464,600 bytes, 51.5625% of the uniform payload**.
One full GMP application reconstructs all 1,113,600 verified coefficients
exactly and checks the weighted residual. The control passes in 116.922
seconds, including 100.265 seconds for the serial original application.
It validates this lattice and reconstruction; it is not a target-size
benchmark or an independent new harmonic column.

## Shrinking Schur corrections

Split positive indices into L={1,...,r} and H={r+1,...}, r=32.
A=I-T_LL has an integral inverse. Maintain exact low residuals modulo
pi^P and store higher moment k modulo pi^(P-k). If the active high
residual has valuation u, choose its projected representative d_H,
supported on k<P-u, and set

    d_L = A^(-1) T_LH d_H.

Discarded high coordinates lie in I_P and have no effect under T
modulo pi^P. Updating by d preserves the exact low equations. The next
high residual, in the weighted quotient, is the high part of T d.
Since the columns of T_LH and T_HH have valuation at least r+1 and
the inverse is integral, this new residual has valuation at least u+r+1.
Only output indices k<P-u-r-1 need to remain active. Low rows are still
computed to check d_L=(Td)_L in the original operator.

When u+r+1>=P, every high index is already sufficient in the weighted
quotient and the low residual is zero. This is the valid stopping test;
it does not assert that the stored weighted centers themselves have
uniform precision P. Reconstruction by T supplies that uniform result.

Source 493 implements this correction stage from the saved uniform
P=800 seed. It retains full precision for indices 0..32 and weighted
precision above them, storing residuals after removing a common power
of two. Its active input counts are

    400, 367, 334, 301, 268, 235, 202, 169, 136, 103, 70, 37, 33.

Each computed state and residual is checked against the corresponding
frozen uniform checkpoint only after the new calculation. Twelve
corrections replace thirteen, followed by a full GMP reconstruction and
the weighted residual check. The uniform seed remains an explicit input;
this experiment does not replace or reprice its construction, factor or
CM extension.

All fourteen shrinking phases pass: seed import, twelve corrections and
final reconstruction. The corrections total 409.052 recorded seconds;
the final reconstruction takes 101.385 seconds. The complete serial
coordinator takes 513.967 seconds, excluding the already saved uniform
seed construction. Its largest phase is the final reconstruction.
The new correction files total 103,751,328 bytes, versus 940,992,000
bytes for the original correction files. This reduction includes fewer
checkpoints and narrower residuals, in addition to the smaller state
layout. The complete shrinking experiment retains 129,596,592 checkpoint
bytes. Both experiments' existing files remain frozen; nothing was deleted.

Source 494 passes in 30.120 seconds. Independent quotient arithmetic
checks c,delta divisibility for all 348 child maps, decodes the variable
width files, and checks 14,476,800 state scalar overlaps and 3,695,760
active residual scalar overlaps across all thirteen checkpoints.
All 174 harmonic masses, every reconstructed scalar and the final weighted
residual pass. Ordinary coefficient recurrence from the weighted input
additionally checks 96 scalars at three states and degrees 1,2,33,64.
These checks do not import production arithmetic.

## Decision, provenance and continuation

Retain the weighted Schur method. It proves a smaller necessary state
representation and a shrinking active band, while preserving the full
original equations. Do not extrapolate a complete P=10552 cost from
this P=800 experiment or from one synthetic action. The serial shrinking
control and the earlier three-worker coordinator have different timing
scopes. Their summed job durations cannot establish an elapsed speedup.

The next bounded implementation should combine the weighted layout and
shrinking bands with resumable state chunks, then measure one actual
P=1600 column from this verified P=800 seed, recording peak memory as
well as phase times. Check the larger factor against P=800, cost each
phase before expanding its scope, retain an independent full original
residual and CM verification, and carry the original seed-extension
proof forward. A failed or oversized phase must be inspected and split,
not blindly retried under a larger cap. Complete those costs before a
new sixteen-column bank or the conditional target-size solve. No P=1600
factor, state lift or CM run is included in this checkpoint.

Source 495 preserves all 1884 hashes in the completed D122 review and
binds all new successful sources, checkpoint files and receipts. Freeze
successful 488--495, both coordinators, their outputs, this report and
its ledger after the final review passes. Its --check replays that fixed
manifest. Keep all existing frozen files; this experiment introduces no
deletion or mutable-checkpoint policy. An interrupted chat response does
not establish whether a local phase completed: inspect its receipt and
partial output before restarting a coordinator.

All 148 input jobs pass: one factor, 126 uniform state phases, four CM
phases, two independent arithmetic audits, one weighted reconstruction
control and fourteen shrinking phases. There are no rejected D123
attempts. Both coordinators and all their workers have returned.
Source 496 is next unused after this review. No worker is left running.

Keep D99 nonhyperellipticity, D108 spectral rejection, D120's conditional
precision target and all census/new-level/Hecke/cubic pauses. The D122
section lower bounds remain 4194/4145/4128 against sufficient non-anchor
bounds 25305/25419/25526; W's Gaussian remains certified nonzero with
valuation 1024 and error 1225, uninverted. Higher intrinsic jets require
preceding exact zeros. The marked X40/Y64 covers, genus-64 section and
degree-51 torsion backend, global F256 action and final invariant remain
downstream requirements. No correspondence was sent.
