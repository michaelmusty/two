# D122: complete P=400 comparison and independent review

Date: 2026-09-27. This completes the comparison and audit left pending in
the frozen [interim handoff](dyadic-precision400-progress-d122.md).
All sixteen actual harmonic columns, all seventeen CM charts, all 1088
coarse values and all 6188 quadratic coefficients have now been checked.
No certified mismatch is found. No positive quadric jet is proved exactly
zero, no candidate identification is proved, and no target field polynomial
is constructed. The original-kernel construction remains the objective.

The [final source ledger](../data/computed/dyadic_precision400_review_sources_d122.json)
distinguishes production, independent arithmetic and provenance checks.
Source 486 imports no production arithmetic. Source 487 checks its seven
completed phases and binds the final sources; source 485 remains only
the earlier provenance snapshot. These are finite computations with the
mathematical arguments below, not machine-formalized geometric proofs.

## Actual data and comparison

The completed bank has P=400 pi-digits, low state moments through 399,
CM moments through 799, and four coarse beta-errors [832,848,832,864].
Only the nine CM-target states were extended through 1198. Source 482
combines the audited D121 column 0 with columns 1--15 from sources
478--479. All full original residuals and old overlaps pass. Source 481
separately supplies algebraic CM values eta at beta-error 21168 on the
original seventeen root branches; this is not harmonic precision 21168.

Source 483 reconstructs the residue frame in 2.687 seconds. Its matrix
is integral; column error bounds are

    [537,536,537,536,536,540,536,539,537,537,538,536,539,536,536,536].

All leading rows and 256 old change-of-basis entries agree. Source 484
then evaluates all 91 quadrics at all 17 points through four orders in
68.753 seconds. All 6188 coefficients contain zero in their certified
balls, including 4641 positive-order coefficients. This remains a finite
congruence, not exact vanishing.

The revised integral-section data are:

| Order | Non-anchor lower bound | Anchor lower bound | Sufficient non-anchor bound with this anchor | Gap |
|---|---:|---:|---:|---:|
| 1 | 4194 | 3976 | 25305 | 21111 |
| 2 | 4145 | 3648 | 25419 | 21274 |
| 3 | 4128 | 3384 | 25526 | 21398 |

Measured section bounds increase by 400 beta-digits from D118. The
sufficient non-anchor thresholds decrease by 25 because the anchor also
improves by 400 and carries weight 1/16 in that inequality. The global
height budget is unchanged. Orders two and three still require the
preceding exact zeros before interpreting them as intrinsic higher jets.

**W's Gaussian is now certified nonzero:** its raw coarse beta-valuation
is 1024, with absolute error 1225, hence relative precision 201. Source
486 confirms this independently. It has not been inverted. The earlier
instruction forbidding inversion of an *unresolved* value is superseded
for this specific ball; any later division must propagate its error.
This closes a local denominator question without proving curve equality
or improving the global ratio-height budget. Retain the direct section
method rather than reopening the rejected height estimates on this basis.

## Independent arithmetic and frame-error proof

Source 486 derives the degree-16 CM polynomial from f(-2-beta^2) and
multiplies by Horner steps in the integer polynomial quotient. Its
comparison phase uses a 2048-beta-digit ring and integral balls carrying
absolute errors, without production unit normalization or field inversion.
The Eisenstein power basis has distinct coefficient valuations modulo
16, so the minimum coefficient valuation gives the element valuation
up to the recorded modulus.

Write H for the sixteen normalized non-anchor leading rows and h_W for
the anchor row. Their raw leading errors become 799 and 536, respectively.
The new H overlaps the audited D120 matrix through 399 digits. The latter
has inverse entries of valuation at least -35; multiplying the perturbation
by that inverse has valuation at least 364. The integral Neumann series
therefore preserves the inverse bound -35 for the new matrix.

Let q=h_W H^(-1), and Q=beta^35 q. The saved Q centers are units. The
audit directly checks Q_center H-beta^35 h_W through valuation 571.
Right multiplication by H^(-1), followed by division by beta^35,
certifies q's saved error 571-35-35=501 without reproducing its inversion.

For the saved change matrix B, independently evaluate each column of

    diag(Q) H B - beta^35 eta_nonanchor.

The inverse of diag(Q)H has entry valuations at least -35, since Q's
entries are units. Subtracting 35 from the minimum residual bound in
each column yields exactly the column-error list above. Evaluate H B
before multiplying by Q to retain the measured cancellation. The audit
then reconstructs all 1088 actual residue-frame jet values and all leading
frame relations using these certified errors.

For quadrics the audit uses gradients and polar forms instead of the
production monomial convolution. With jets x,v,w,t, the positive
coefficients are grad Q(x).v, grad Q(x).w+Q(v), and
grad Q(x).t+grad Q(v).w. These enclosures validate every stored coefficient
and section shift. An independent rational atanh series for log(2)
checks all three strict threshold inequalities and their insufficiency.

The remaining audit phases check all seventeen root residuals and Hensel
branch overlaps, cross-multiply all 272 eta values after clearing rational
denominators, and verify the sixteen trace sums. All 8,908,800 low-state
scalar overlaps and saved zero residual coefficients are checked. Direct
original recurrences additionally check 2560 scalar coefficients across
all sixteen columns, at five states and degrees 1,2,33,64; this sampling
is distinct from the production full-residual check. Four phases reproduce
all 1088 coarse values by an alternate binomial-series kernel and Horner
evaluation of the CM moments.

## Execution and continuing plan

All 167 input receipts pass: 157 computation jobs, seven independent
arithmetic phases and three interim provenance checks. The independent
phases total 85.929 recorded seconds; parallel durations must not be
read as elapsed wall time. Every phase uses one BLAS thread and runner
272's 180-second private-process-group cap. There are no rejected D122
attempts. All workers have returned successfully.

Review 487 preserves every one of the 1079 D121 hashes and all 1844 hashes
in the interim snapshot, while binding the completed comparison and
independent review. Freeze successful sources 476--487, their artifacts,
this report and its ledger. The interim report/ledger remain unchanged.
Replay 487 with `--check` through `run_dyadic_capped.py` and a fresh receipt
stem; do not rerun completed output-producing phases.

The P=400 falsification check passed, so staged refinement remains the
best current route. A complete P=10552 solve is still uncosted: the
compiled synthetic action takes 23.574 seconds plus 1.901 preparation,
and neither the audit nor the nonzero Gaussian removes the full-sweep
cost. The next bounded implementation should generalize the P=400 lift
and persist original-operator sweeps in state chunks, then measure one
actual P=800 column from its P=400 checkpoint with r=32. Include factor,
seed, corrections, full original residual and CM costs before deciding
on another sixteen-column bank or a target-size lift. Source 488 is next
unused. No P=800 job or new generalized driver has been run or written.

Keep D99 nonhyperellipticity, D108's spectral rejection, D120's conditional
precision target, all census/new-level/Hecke/cubic pauses and the remaining
marked-cover, genus-64 section, degree-51 torsion, global F256 action and
final field requirements. No correspondence was sent.

After a disconnected chat stream, inspect completed receipts and outputs
before retrying commands. An interrupted response does not by itself say
whether a local job finished. Completed artifacts survive a new chat in
the same workspace; the live top of HANDOFF.md records the next task.
