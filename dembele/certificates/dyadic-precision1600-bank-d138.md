# D138: complete P1600 bank and independent comparison

The approved P1600 checkpoint combines all sixteen harmonic columns at
common precision P1600. Column 0 retains its stronger P6400 certificate;
column 1 reuses its P1600 certificate. D137 lifted and independently reviewed
columns 2–15. The new common-bank assembly, residue frame, candidate-quadric
comparison and independent integer-quotient audit all pass.

The candidate remains compatible with the computed data: all 91 quadrics
were tested at 17 CM points through coarse orders 0–3, and the independent
audit checked all 6,188 coefficients, including 4,641 positive-order
coefficients. There are no certified mismatches. No positive-order exact
quadric vanishing, candidate-curve identification, arithmetic double-cover
identification or defining field polynomial follows at this precision.

## Completed computation and resource limits

The D137 revision-2 column run finished at 2026-10-07 18:36:36 UTC
(2:36 p.m. Eastern), after 79,367.504 seconds, approximately 22.05 hours.
It passed 92,946 bounded jobs: 92,232 production phases, 350 archives,
336 independent audit jobs, and 28 column review/replay jobs. The earlier
namespace startup failure is preserved separately with its receipt, log
and driver snapshot; it occurred before a working store or arithmetic was
created. There were no failed revision-2 arithmetic or review jobs.

The engine, store and archive sources remain frozen. The three-worker,
180-second private-process-group, 2 GiB logical working-store, 2 GiB
measured per-worker RSS and 6 GiB conservative concurrent RSS limits were
unchanged. D137's proved working-store inventory bound is 141,761,896 bytes.
RSS limits are measured admission, not OS hard memory limits.

The original 15–18-hour forecast was optimistic. Production worker time
stayed approximately 83 minutes per column, while coordinator and archive
overhead grew with the number of result files. The first column took about
57 minutes and the last about 144 minutes. Archive time grew from about
9 minutes to 42 minutes per column; the longest last-column archive took
157.681 seconds, within the unchanged 180-second bound. The next execution
plan should remove repeated directory-wide receipt searches and be costed
again before a larger precision bank is admitted.

## Common precision and the frame

Source 569 authenticates all sixteen state/CM metadata pairs and their
retained binaries against the D137 admission and fourteen reviewed column
catalogues. Column zero's higher-precision coarse centers are explicitly
reduced modulo the coefficient modulus for beta precision 3264. The bank
uses common coarse errors `[3232, 3248, 3232, 3264]`; it never assigns
higher precision to discarded digits. All 1,088 coarse values overlap the
previous P800 bank. No new uniform state binary or CM binary is created.

The common original-equation scalar coverage is 35,635,200 and the common
CM-moment scalar coverage is 6,963,200. These counts do not change the
certificate scope: columns 0 and 2–15 use authenticated full original
weighted equations; column 1 inherits a uniform full residual certificate.
Independent original-operator checks are explicitly sampled. Every new
column also has complete old weighted-state overlaps, masses, residual-zero
rows, old CM overlaps, and old coarse overlaps checked independently.

Source 570 lifts the existing explicit valuation-ball arithmetic to beta
precision 4096. Product, scaling, inverse and unresolved-division controls
pass. Source 571 reconstructs the residue frame from actual jets without
using candidate quadrics. All 256 change-of-basis entries and 1,088 actual
jets overlap P800. The minimum change-entry error is beta 2936. The anchor
Gaussian has valuation 1024 and error 3625; it is never inverted.

## Candidate comparison and remaining gap

Source 572 evaluates the quadrics with explicit errors. Source 573 imports
no production arithmetic: it independently uses Horner multiplication in
the integer polynomial quotient, absolute-error balls, frame residual
bounds, gradients and polar forms. It checks the assembled bank, all actual
jets and all quadric coefficients. Exact rational logarithm intervals
verify the sufficient-height comparisons.

| Positive order | Degree-16 lower bound | Anchor lower bound | Sufficient nonanchor bound with this anchor | Remaining gap |
| --- | ---: | ---: | ---: | ---: |
| 1 | 6594 | 6376 | 25155 | 18561 |
| 2 | 6545 | 6048 | 25269 | 18724 |
| 3 | 6528 | 5784 | 25376 | 18848 |

All values are beta-adic valuations. The intrinsic interpretation of orders
2 and 3 remains conditional on exact vanishing of previous positive orders.
Relative to P800, both the degree-16 and anchor lower bounds improve by
1600 at each order, and the displayed gaps shrink by 1700. The sufficient
inequalities still fail. Zero-containing finite balls are not exact zeros.
The conditional P10552 sufficient target is neither certified nor asserted
necessary, and the marked-base and canonical-Hecke hypotheses of D134
remain unresolved.

## Incremental provenance and completion

Source 574 replays fifteen frozen catalogues: the 94,126-entry D137
admission catalogue and fourteen 20,433-entry column catalogues. All 380,188
listed hash occurrences match. Their catalogue roots bind the complete
lists, so the lists need not be duplicated in every new result. Source 575
checks the column completion records and reviews, every new bounded receipt,
all comparison outputs, resource assertions, and the consistent catalogue
graph. Its replay rehashes the complete transitive graph again, within the
same job cap. The final review also retains direct current seed/CM and
immutable engine-dependency bindings for a separately admitted future stage.

The fixed review is `dyadic_precision1600_review_d138.json`; its creation
and replay receipts and `dyadic_precision1600_completion_d138.json` are the
completion authority. Sources 569–575, the manifest coordinator, this report,
and every bound artifact are frozen after that review. The full-bank
comparison checkpoint is P1600 once those final receipts pass. No P3200 or
higher bank is admitted by this checkpoint.
