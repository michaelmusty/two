# D83: 64-digit cubic lift and reconstruction experiment

Date: 2026-09-22. The lift and independent checks through 31^64 are
complete. Both recognition experiments are negative; exact coefficients
over a number field remain unreconstructed. The frozen input is the
[D82 cubic modulo 31^32](cm-frame-cubic-precision.md).

## Objective

The verified pointed class correction gives the smaller equation

\[
\ell T^3-3A_2\ell T-R_4=0,\qquad \operatorname{wt}(T)=1,
\]

with 45 quadratic and 105 quartic coefficients modulo 31^64. Both the
internal 80P model and the K_X+2P output model pass independent saved-data
checks and highest-digit error controls. Every core coefficient reduces
to the verified 32-digit model. The earlier explicit isomorphisms retain
the genus-64 special fibre and point counts 68/2818.

Joint projective recognition over F uses the exact 25-dimensional rational
space containing A2. The searches with 48 training / 16 validation digits
and 60 training / 4 validation digits find no surviving candidate in any
of the eight embeddings. Exact inverse-matrix certificates also exclude
integral homogeneous coefficient height at most **1,301,123** in the
specified bases, uniformly over those embeddings. This is not a field
exclusion or an arithmetic identification.

## Reproducibility and bounds

Runner `261_cm_frame_cubic_precision64.py` extends the existing
orchestration without changing D82 sources. Its generated
`d83_64_*.py` runners change only the accepted precision, milestone and
provenance header. Each completed stage has a receipt binding the
original runner, generated copy and output certificate. Existing receipts
are verified before reuse. The geometry and class arithmetic remain
unchanged. Every substantive Magma job retains its 180-second wall limit
and 2 GB memory limit; a timeout is an unsuccessful computation.

The completed route uses 261 for sections, jets, the initial divisor,
class charts and the corrected actual divisor. Script 264 checks the class
in separate jobs; 266 recovers the pointed functions; 262 fits their
coefficients; 265 checks the internal equation. Script 261 publishes the
verified third and internal cubic under the standard precision filenames.
Scripts 269/267 construct the smaller model and 268 verifies it. The
details below explain the two unsuccessful monolithic attempts.

For future Sage jobs use **274_cm_frame_bounded_recognition.py**. Its
272 runner enforces timeouts on the entire process group and verifies
existing successful records without overwriting them. The older frozen
recognition CLIs have the timeout defect documented below. All successful
recognition and inverse-matrix jobs here finish within 15 seconds.

## Outcomes

| Stage | Wall seconds | Result |
| --- | ---: | --- |
| Sections and evaluation points | 45.078 | Pass; compatible with 32 digits |
| Local expansions | 61.655 | Pass; compatible with 32 digits |
| Initial actual divisor lift | 155.402 | Pass; idempotent and reduction verified |
| Form the class correction | 145.287 | Pass |
| Normalize the lifted divisor | 88.442 | Pass |
| Normalize the correcting class | 86.462 | Pass |
| Actual divisor from corrected coordinates | 158.709 | Pass |
| Independent tripling relation | 160.456 | Pass |
| Independent class symmetries | 47.652 | Pass |
| Pointed u recovery in its required subspace | 135.268 | Pass |
| Pointed f recovery and norm identity | 95.878 | Pass |
| Pointed coefficient fitting | 46.214 | Pass; all coefficients reduce to 32 digits |
| Independent pointed geometry / functions | 57.423 / 137.359 | Pass |
| Pointed highest-digit norm / trace controls | 130.186 / 136.734 | Rejected at intended identities |
| Adjoint divisor move | 158.853 | Pass |
| Adjoint u recovery | 139.298 | Pass |
| Adjoint f, norm and coefficient recovery | 105.385 | Pass; all coefficients reduce to 32 digits |
| Independent adjoint move / functions | 158.908 / 124.486 | Pass |
| Adjoint highest-digit norm / trace controls | 81.198 / 130.821 | Rejected at intended identities |

The combined direct class check (script 231) timed out at 180 seconds.
Its log and job record remain archived under
`cm_frame_cubic_pointed_64_newton_check`. This is not a completed class
check. Script 264 separates the tripling relation and the two symmetries
into bounded jobs; both now pass. Runner 265 reuses
their certificate after verifying exact equality with the divisor
matrix used by the cubic. It retains the full independent geometry,
function and coefficient checks and both highest-digit error controls.

Runner 262 first split pointed function search from coefficient fitting.
The combined u/f search still timed out at 180 seconds; its failed
`cm_frame_cubic_pointed_64_function_checkpoint_job.json` remains
unchanged. Runner 266 now separates u from f and searches for u directly
inside WB4. Previously the constructor found an 81-dimensional quotient
inside RG4, then intersected it with WB4. The final space is the same
degree-zero line. RDegreeZero checks its full RG2 inclusion; the later
independent checker also verifies membership in WB4 and every function
divisor condition. These two jobs and subsequent fitting pass. The
successful checkpoint JSON binds the new u/f jobs, not the failed job
with the earlier basename.

Runner 269 constructs the adjoint move using only the independently
certified class matrix, so it can run alongside pointed function
verification. Runner 267 uses the same smaller u search and separates
it from f recovery and coefficient fitting. Runner 268 splits the
independent adjoint checker into the divisor move and function identities;
its coefficient-error controls exercise the latter. Both checks and both
controls pass. The completed roots are
`cm_frame_cubic_pointed_64_check.json` and
`cm_frame_cubic_adjoint_64_check.json`.

## Recognition and an exact height exclusion

Script 258 tests individual Q/F coefficients and projective ratios,
including the coordinates in the exact small A2 basis. It finds no
survivors. Its pilot ran before the final adjoint checker finished; its
metadata records that fact, and the final audit binds both computations
to the same unchanged model.

Script 259 tests joint projective recognition in the degree-eight power
basis of F, allowing one common F-valued scale. The lattice has rank 200
and 24 congruence conditions. All eight roots 4,9,10,11,20,21,22,27 modulo
31 are tested at both 48/16 and 60/4 training/validation splits. Known
F-valued controls are recognized and first-unused-digit corruptions are
rejected. For the actual point, no tested candidate row matches even the
first unused digit. This LLL basis-row search alone is not exhaustive.

Script 271 supplies a separate exact statement. Let B be the integral
row basis of the 60-digit congruence lattice, D=31^60, and K=D*B^-1.
The matrix K is integral; the saved witness verifies B*K=D*I. Put
S=max_j sum_i |K_ij| and H=floor((D-1)/S). For any lattice vector v=z*B
with integral z, the relation v*K=D*z implies

\[
 D|z_j|\leq \|v\|_\infty S.
\]

If ||v||_infinity <= H, every integral z_j has absolute value less than
one, so v=0. Thus **all** nonzero lattice vectors of height at most H
are excluded, independently of which vectors LLL returned. Script 263
checks every saved integer product and column sum again using plain
Python, without Sage, inversion or floating-point arithmetic.

| Root modulo 31 | Integral coefficient height excluded through |
| --- | ---: |
| 4 | 2,160,583 |
| 9 | 2,159,127 |
| 10 | 3,165,549 |
| 11 | 1,301,123 |
| 20 | 4,384,493 |
| 21 | 1,778,583 |
| 22 | 2,998,618 |
| 27 | 1,406,747 |

Here height is the maximum absolute integer coefficient of a nonzero
homogeneous representative in the **25 fixed A2 basis coordinates and
the eight power-basis coordinates of F**. Any common F-valued scale is
allowed before clearing rational denominators. A matching exact
F-projective point would yield a vector in this congruence lattice, so
the bound applies to every such integral representative. It is not a
bound in arbitrary coordinate systems, a Weil-height statement, or an
exclusion of definition over F.

## Timeout handling and the archived diagnostic

An optional exact Gram-Schmidt calculation (270) timed out after 180
seconds. The old runner killed the Sage launcher but left its Python
child running; the child later produced output. The final provenance
audit detected the changed log hash. This late result is **excluded**
from the bounded mathematical certificates.

The late log and worker JSON are retained as
`cm_frame_cubic_adjoint_height_64_48_0_late.{out,json}`. The original
empty timeout log was restored exactly to its recorded SHA256. The
archive manifest `cm_frame_cubic_adjoint_height_late_archive.json`
records both versions; the original worker-result filename is now an
explicit `not_certified_timeout` pointer to that archive.

Runner 272 starts each job in its own process group and kills the whole
group on timeout. Regression 273 runs a real Sage job that spawns a
delayed writer: both processes are terminated, the late file never
appears, and the captured log hash remains unchanged after the child's
write deadline. A successful Sage control also passes. The root is
`cm_frame_bounded_sage_timeout_control.json`; 274 exposes the corrected
runner for existing recognition workers with immutable reuse.

The reviewed [Sage Gram-Schmidt interface](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.gram_schmidt)
belongs to the archived attempt. The successful height certificate uses
an exact rational inverse followed by integer identities; its inequality
above is a local deduction.

## Artifacts and next step

The compact equation is `cm_frame_cubic_adjoint_package_64.json`, and
the combined certificate is `cm_frame_cubic_adjoint_audit_64.json`.
The final audit passes 1329 file hashes and 493 linked JSON records.
The package retains D82's base quadrics, ell and monomial conventions.
On the special fibre it specifies the smooth projective normalization
of the component dominating C on ell != 0; clearing ell can add vertical
components. The audit binds the model checks, both recognition splits,
all eight independently checked height certificates, the unsuccessful
diagnostics and the timeout regression. Earlier arithmetic inputs,
including D78's frozen root, remain unchanged.

The next bounded reconstruction experiment is 128 digits in the same
K_X+2P normalization and exact A2 basis, using 112 training digits and
16 unused validation digits. The current lift wrappers are specialized
to 64 digits and hash-bound. Add new orchestration and split any stage
that would exceed 180 seconds; the largest inverse/class calculations
may need precision-aware arithmetic. Use runner 274 for future Sage
jobs. Any apparent number-field equation must pass exact function and
divisor identities before torsion work. Do not infer a larger field
or reject the selected third from the negative bounded searches.

All earlier arithmetic certificates remain frozen. Arithmetic
identification, prescribed Fuchsian monodromy, the hyperellipticity
conflict and construction of the target field remain open.
