# D86: verified Châtelet 128-digit lift and negative reconstruction

Dates: 2026-09-22–23. **Complete.** Both cubic models are independently
verified modulo **31^128**, including highest-digit norm/trace corruption
controls and coefficientwise reduction to the [64-digit models](cm-frame-cubic-64.md).
The original precision-aware arithmetic succeeds with Châtelet's larger
resource allowance. All 21 remote jobs have finished successfully in
their intended roles; the four negative controls fail at the intended
assertions.

Joint projective recognition over `F = Q(zeta_32)^+`, with **112 training
and 16 validation digits**, produces **no surviving candidate in any of
the eight embeddings**. All known-F and unused-digit error controls pass.
Independent integer certificates exclude integral homogeneous coefficient
height through **348,750,355,384,078** in the specified bases. This is not
a coefficient-field exclusion. Exact number-field coefficients, arithmetic
identification, and the target field polynomial remain unconstructed.

The user explicitly authorized uploading the mathematical inputs for
this run to `chatelet.mit.edu`. The first twelve files and their hashes
are recorded in
`cm_frame_cubic_pointed_128_formal_divisor_chatelet_d86_planned_transfer.json`.
Credentials remain local. Later transfers contain only required Magma
sources, coefficient artifacts, and the standalone bounded worker.

## Computation and provenance

Scripts 298–300 execute the existing D85 precision adapters and kernel
283 in `two_remote_magma/dembele_d86_128_20260922`. They reuse the
successful 128-digit sections and jets. Every remote job is single
threaded, with 8,000,000,000 bytes of Magma memory and 1800-second CPU
and wall limits. Timeouts terminate the process group. The detached
launcher has a sufficiently high API CPU ceiling; its worker imposes
the actual per-job bounds.

Remote input hashes are verified before execution. Local receipts retain
the specifications, status records, full fetched logs, output hashes,
resource use, and original/generated source hashes. Earlier failures and
the [D85 descent review](cm-frame-cubic-128-review.md) remain immutable.
The D85 audit's assertions that no 128-digit result exists describe that
earlier checkpoint and must not be reused as current-state assertions.

| Stage | Wall seconds | Peak RSS bytes | Outcome |
| --- | ---: | ---: | --- |
| Initial actual divisor lift | 188.036 | 2,246,602,752 | Pass |
| Class correction | 256.172 | 1,264,381,952 | Pass |
| Normalize lifted divisor | 158.186 | 1,766,006,784 | Pass |
| Normalize correcting class | 152.653 | 1,767,043,072 | Pass |
| Corrected actual divisor | 187.408 | 2,250,620,928 | Pass |
| Independent tripling relation | 299.709 | 1,289,744,384 | Pass |
| Independent class symmetries | 89.384 | 1,184,993,280 | Pass |
| Adjoint representative move | 248.889 | 2,184,327,168 | Pass |
| Pointed u recovery | 199.817 | 2,146,426,880 | Pass |
| Adjoint u recovery | 197.915 | 2,147,655,680 | Pass |
| Pointed f and norm recovery | 154.870 | 1,852,178,432 | Pass |
| Pointed coefficient fitting | 54.301 | 1,023,193,088 | Pass |
| Adjoint f and coefficient recovery | 160.008 | 1,865,781,248 | Pass |
| Independent pointed geometry | 66.571 | 878,985,216 | Pass |
| Independent pointed functions | 206.970 | 2,133,131,264 | Pass |
| Pointed highest-digit norm control | 202.267 | 2,142,334,976 | Intended error rejected |
| Pointed highest-digit trace control | 214.636 | 2,141,642,752 | Intended error rejected |
| Independent adjoint representative | 287.441 | 2,185,023,488 | Pass |
| Independent adjoint functions | 202.359 | 2,178,949,120 | Pass |
| Adjoint highest-digit norm control | 128.452 | 2,088,701,952 | Intended error rejected |
| Adjoint highest-digit trace control | 202.658 | 2,178,322,432 | Intended error rejected |

The longest remote job takes 299.709 seconds; the maximum observed RSS
is 2,250,620,928 bytes. The successful run therefore exceeds both bounds
that constrained the earlier local attempt, while remaining well within
the remote 1800-second / 8 GB limits. Independent checks use at most two
remote jobs concurrently. Script 302 reuses the original generated
checkers and assembles their unchanged reports from the job receipts.

Two local orchestrators encountered socket timeouts while uploading the
next function-stage inputs. Remote inspection confirmed that neither
next job had a specification, launcher, start, or completion record.
`cm_frame_cubic128_upload_interruption_d86.json` records the interruption.
The successful u computations are retained; resumption reuses those
receipts and verified upload chunks.

One sequential resumption also encountered a TLS handshake timeout
during upload. Adapter 304 adds at most six attempts, with bounded
backoff, for idempotent transfer/status operations. It records each
transient error and binds those event files into subsequent receipts.
The detached job launch retains its original durable-state guard and
is never retried by this adapter. Sources 298–300 remain unchanged.
After a later connection reset, adapter 305 also handles connection
closures, incomplete HTTP responses and transient HTTP status errors.
It preserves 304 and the same bounded, idempotent retry policy.

## Equation and reconstruction test

The output equation retains the verified normalization

\[
\ell T^3-3A_2\ell T-R_4=0,\qquad \operatorname{wt}(T)=1.
\]

Here `A2` has 45 quadratic coefficients in the fixed exact
25-dimensional rational subspace, and `R4` has 105 quartic coefficients.
The fixed divisor is `K_X+2P`; the normalization scale is
`sqrt(-3)*a0/h0`. No new root is chosen by this normalization. Internal
class arithmetic still uses the `80P` chart. Precision means modulo
`31^128`, with coefficientwise compatibility modulo `31^64`.

The joint reconstruction uses the power basis of
`F = Q(theta)`, where
`theta^8 - 8*theta^6 + 20*theta^4 - 16*theta^2 + 2 = 0`,
and the same 25 coordinates for `A2` as D83/D84. Each rank-200 lattice
imposes 24 projective congruences modulo `31^112`. Candidate rows must
also match all sixteen unused digits. Known exact `F` points and errors
in the first unused digit control the test at every embedding. A
surviving finite-precision candidate would still require exact equation
and arithmetic-identification checks.

The coefficientwise pilot uses 64 training / 64 validation digits. It
finds no rational survivor among all tested coefficients or separate
projective coordinates, and no F survivor in its fixed samples, across
the quadratic, quartic and reduced-coordinate groups. This pilot is
distinct from the joint test of all 25 reduced coordinates.

The joint results and exact height exclusions are:

| Root of theta modulo 31 | Known-F survivors | Target survivors | Maximum matching digits | Excluded height through |
| ---: | ---: | ---: | ---: | ---: |
| 4 | 8 | 0 | 112 | 416,963,134,869,138 |
| 9 | 6 | 0 | 112 | 472,851,805,904,364 |
| 10 | 8 | 0 | 112 | 348,750,355,384,078 |
| 11 | 8 | 0 | 112 | 545,931,952,569,702 |
| 20 | 8 | 0 | 112 | 624,747,224,516,487 |
| 21 | 8 | 0 | 112 | 723,950,521,948,168 |
| 22 | 7 | 0 | 112 | 806,752,711,089,091 |
| 27 | 8 | 0 | 112 | 381,720,305,027,558 |

Recognition and height computations run locally in Sage through the
process-group timeout runner 272, using 274 and the 128-digit adapter
301. The coefficient pilot takes 12.150 seconds, joint jobs take
25.721–29.272 seconds, and height jobs take 6.155–7.676 seconds. All
finish inside their 180-second bounds. No exact number-field cubic is
inferred from finite-precision recognition.

Script 301 certifies an additional, rigorous height exclusion. If `B`
is the integral lattice basis, `D=31^112`, and `K=D*B^-1` is integral,
put `S=max_j sum_i |K_ij|`. A lattice vector `v=z*B` whose coefficients
have absolute value at most `H` satisfies `D*|z_j| <= H*S`. Thus
`H=floor((D-1)/S)` excludes every nonzero such vector. Script 303 checks
`B*K=D*I` again using plain integer arithmetic. The height refers only to
these specified bases and integral homogeneous coordinates, allowing
arbitrary common `F`-valued scaling; it is not an intrinsic height or a
field exclusion.

## Package and audit

The portable finite-precision equation, base curve and monomial orderings
are in `cm_frame_cubic_adjoint_package_128.json`. The independent checks
are `cm_frame_cubic_pointed_128_check.json` and
`cm_frame_cubic_adjoint_128_check.json`. The final root is
`cm_frame_cubic_adjoint_audit_128.json`; verifier 303 checks **2009 file
hashes / 769 JSON records**, including the unchanged D85/D84/D83/D78
provenance. It independently checks every integer identity `B*K=D*I`,
the bounds, reduction to 64 digits, and the remote logs against their
success markers or deliberate-error assertions.

`cm_frame_cubic128_remote_completion_d86.json` records a fresh remote
inspection: all 21 jobs are complete, and every remote status agrees
with its saved local record. All local recognition jobs are complete too.

```sh
python3 dembele/pari/303_cm_frame_cubic128_audit.py --check
```

Successful stages can be checked/reused through 305 with `--stage NAME`
or `--family pointed`/`adjoint`; they need no new execution. All bound
sources and failure receipts are immutable. Do not rerun 297's historical
absence assertions as a test of this new checkpoint.

## Consequence and next step

The remote attempt resolves the computational resource obstacle and
substantially increases the certified coordinate-height exclusion. It
does not resolve the coefficient-field question or identify the local
cover with the canonical arithmetic cover. The D85 review remains the
next mathematical guide: prepare a marked comparison of the explicit
base, branch marking and selected third with the quaternionic cover,
or prove the required global Galois action on that third. The global
twist and published hyperellipticity discrepancy remain in scope.
Pause precision escalation; no automatic 256-digit lift, arbitrary
larger-field search, or target torsion computation follows this result.
