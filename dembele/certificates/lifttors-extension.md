# Residue-degree-51 calibration and row generation (D64)

Date: 2026-09-16. This executes D63's next bounded experiment. The
compiled backend and its pinned upstream sources are unchanged.

**Subsequent D65 work:** the checked formula now has a separate native
implementation; see [lifttors-rows.md](lifttors-rows.md). D64's saved
source files, build and results remain unchanged. Follow the D65 report
for the current tests and next step.

**Result:** the known genus-4 2-torsion lift passes at residue degree 51,
with one lift taking 8.356 seconds under the same 2 GB PARI stack cap
and 900-second timeout. The degree-two comparison takes 0.264 seconds.
Measured equation-entry sizes project to roughly 9.1 GB for the existing
genus-64 lifting matrix alone, conditional on comparable representations.
A new row-generation identity agrees with every original equation in
four small systems and gives the same kernels. It is a GP prototype;
the production C routine still stores the full matrix.

The report and hashes are in
[`lifttors_extension.json`](../data/computed/lifttors_extension.json).
The earlier [`lifttors_controls.json`](../data/computed/lifttors_controls.json)
and all D63 source digests remain unchanged.

## Measured controls

Both runs use y^2=x^9-x, p=97, e=4, d0=9, section dimensions 6/15/24,
one worker and seed 20260916. Script 101 checks the nonzero point
[(0,0)-(1,0)], independently doubles the exact divisor, lifts its
reduction from precision 97 to 97^4, compares the lift with that exact
divisor, and checks that doubling the result gives zero. Its equation
and symbolic bases are removed after initialization, as in D63.

| Measurement | a=2 | a=51 |
|---|---:|---:|
| Evaluation points | 46 | 51 |
| Jacobian object, bytes | 489,240 | 8,566,200 |
| Initialization, seconds | 0.015 | 0.214 |
| Doubling and zero check, seconds | 0.019 | 0.547 |
| One torsion lift, seconds | 0.264 | 8.356 |
| Final lift checks, seconds | 0.025 | 0.712 |
| Whole process, seconds | 0.405 | 10.116 |
| Result | PASS | PASS |

These are single local measurements. The lift-time ratio is 31.65,
and the Jacobian object-size ratio is 17.51. Evaluation-point counts
also differ, so neither ratio isolates field-degree cost. They do not
forecast genus-64 runtime or the eventual precision budget.

The torsion point is rational. This tests arithmetic over the extension,
not a representation whose torsion has Frobenius order 51. To check that
the arithmetic really uses that field, script 106 verifies the defining
polynomial's degree and irreducibility, the evaluation-point Frobenius
cycles (23 cycles of length 2 versus one of length 51), and an entry of
each degree-51 equation matrix outside both F_(97^3) and F_(97^17).
These contain every proper subfield of F_(97^51). The degree-two systems
similarly have an entry outside F_97.

## Storage evidence and budget decision

Script 106 reconstructs derivative systems at initial precisions 97
and 97^2 on the same known divisor. These use separate deflations of
the exact point, not a second timing of the full torsion lift.

| Quantity, at derivative precision 97^2 | a=2 | a=51 |
|---|---:|---:|
| Full system dimensions | 132 by 19 | 162 by 19 |
| Rank / kernel dimension | 9 / 10 | 9 / 10 |
| Full matrix object, bytes | 221,016 | 5,097,368 |
| Largest generated row block, bytes | 37,096 | 849,832 |
| Selected independent rows, bytes | 15,360 | 283,472 |
| Formula caches S,H,Cbar,rho, bytes | 140,552 | 3,027,696 |

The measurements use PARI's
[`sizebyte`](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Conversions_and_similar_elementary_functions_or_commands.html#sizebyte),
which counts the object tree. These are not peak stack or resident-memory
measurements. Shared objects, surrounding Jacobian data and arithmetic
temporaries matter separately. The prototype keeps the full reference
matrix for comparison, so its process memory is not a measurement of a
production streaming implementation.

No measured degree-51 entry vanishes modulo 97; about 99% have the full
polynomial degree 50. Mean entry payloads at the two precisions are
1,644.66 and 1,647.96 bytes. Applying these means to D63's
5,504,268-entry genus-64 matrix, adding its measured eight-byte pointer
and header representation, gives 9.10–9.11 GB for that object alone.
If initialization instead produced thirteen full length-51 orbits,
nZ=663 would give 5,794,866 entries and 9.58–9.60 GB. That point count
is a scenario, not an observed genus-64 initialization.

These are conditional storage projections, not rigorous lower bounds
for the target or measured peak memory. They provide no support for
trying the unchanged full-matrix method under the 2 GB cap. No
genus-64/a=51 job was launched and the cap was not increased.

## Exact row-generation identity

The pinned
[`PicLift_worker`](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/lift.c)
implements the derivative of the Schur complement. With pivot rows I,
complementary rows Ic, pivot columns P and complementary columns Pc,
write the current product matrix as

    M = [ A B ; C D ],       Cbar = C*A^-1,
    rho = (D - Cbar*B) / p^e1.

All derivative arithmetic is modulo q=p^(e2-e1). Scatter the matrix
[-A^-1*B; identity] back to the original column order to form N, and
split N into its two input blocks N_1,N_2. If V is the evaluated
section basis and U0 the normalization-preserving deformation basis, set

    S = V*U0,       H_i = V*N_i.

For a complementary column k, the equations for all deformation
coordinates in input block i are

    B_i,k = diag(H_i[Ic,k])*S[Ic,:]
            - Cbar*diag(H_i[I,k])*S[I,:].

The corresponding row block of the homogeneous lifting system is
[B_1,k, B_2,k, rho[:,k]]. Indeed a deformation in coordinate j changes
input block i by diag(S[:,j])*V. Multiplication by N and elimination of
the pivot rows gives exactly the displayed formula, equivalent to

    d - c*A^-1*B - Cbar*b + Cbar*a*A^-1*B.

Upstream `mat2col` visits rows first, then columns: with b=#Pc, the j-th
row of this block is row (j-1)*b+k of the original full system. This
indexing is checked explicitly; successive generated blocks need not
be contiguous in the original ordering.

For a production kernel computation, feed these blocks into D63's
independent-row selection, solve the selected system and regenerate
every block to verify the kernel at the full derivative precision.
The selected rows come from the original equations. Their unit pivot
minor gives a free kernel; the complete residual check proves equality
with the full system, as in the [D63 argument](lifttors-memory.md).
No full K is needed for that algorithm.

Script 106 compares every entry against the existing derivative worker:
2,508 entries at each of two precisions for a=2, and 3,078 at each for
a=51, totaling **11,172 exact comparisons**. All four selected systems
have nine rows and ten kernel generators. Their kernels agree with the
full-system kernels and satisfy every regenerated equation modulo 97
or 97^2, respectively. Both coefficient fields have a full-field entry
witness. All checks pass.

At g=64, each block has (nZ-324) by 259 entries; the full matrix has
66 such blocks. This divides the equation-buffer entry count by 66,
not total process memory. The caches, selected rows, Jacobian data and
temporary allocations remain to be budgeted. No claim that the final
implementation fits 2 GB follows yet.

## Next step and reproduction

Integrate this checked row-generation formula into a separately
selectable native lifting path, retain the original and D63 comparison
paths, and repeat their meaningful controls. Include the complete
equation verification and good-reduction rejection. Reassess memory
and time on the existing bounded controls before a genus-64/a=51 job.
The GP prototype alone is not an integrated streaming torsion lift.

The target arithmetic section entries and a mechanism for lifting
them remain missing; see the
[section interface](arithmetic-section-interface.md). No target
torsion, target polynomial or new exact CM value is obtained. D62's
geometry and D58–D60's descent scope are unchanged; repeated CM scans
remain paused.

With the D63 build already present, run from the repository root:

```sh
python3 dembele/pari/105_lifttors_extension.py
```

Use `--collect` to rebuild the JSON from the four saved logs without
rerunning arithmetic. The runner checks the D63 library, adapter,
upstream and previously recorded source digests, and requires explicit
PASS markers, one data record and no GP error. It shares D63's process
group timeout handling. Build initially with
`python3 dembele/pari/build_lifttors.py` if needed; the manifest must
match the saved D63 comparison. D64 changes no C backend source.
Collection was also checked against five invalid-log fixtures: missing
PASS, duplicate DATA, a GP error, a timeout marker and a wrong field
degree. Each is rejected. Source digests and local report links verify;
`git diff --check` passes. The unchanged D63 result remains the latest
111-test Python/Sage regression run; D64's GP checks are separate.

The row formula, its prototype, projection and decision are local work;
the divisor and lifting algorithms are Mascot's. PARI documents the
object-size function used for these measurements. No target-scale
performance or arithmetic frontend is attributed to either source.
