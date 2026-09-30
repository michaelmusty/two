# D122 handoff: complete P=400 bank, comparison still pending

Date: 2026-09-27. This is a progress checkpoint requested by the user,
not the final independent D122 mathematical review. The previous
[D121 report](dyadic-schur-lift-d121.md) and its 1079 bound source hashes
remain unchanged. All batch workers have finished. No jobs remain running.

## Completed work

The actual sixteen-column harmonic bank now has P=400 low state moments
and all seventeen CM A charts. The combined artifact is
`dyadic_precision400_d122.json`; it points to packed per-column state
files and includes all 1088 coarse values, in the usual point/order/basis
ordering. Four coarse coefficients have beta-errors [832,848,832,864].
There are 8,908,800 checked original low-state scalar coefficients and
1,740,800 stored CM scalar coefficients. Only the nine state charts needed
by the CM maps were extended through moment 1198; all other state files
contain moments 0 through 399. CM moments run through 799.

Source 476 implements polynomial multiplication by fifteen evaluations
and integer Newton interpolation over FLINT. Source 477 checks small and
truncated products through 1536 bits, compares larger products against
GMP, checks full synthetic transforms and five actual P=400 state
equations. A synthetic P=10552 action takes 23.574 seconds, plus 1.901
seconds preparation. This is a modest improvement over D121's 26.825-second
reused action and does not solve the full target-size cost problem.

Source 478 reuses the frozen Schur lift, using the compiled backend for
seed/correction phases and the separate older GMP polynomial backend
for each final full residual. Columns 1--15 are complete, including all
old P=200 overlaps. Column 0 is the audited D121 result. Source 479
finishes each column's CM moments and four coarse coefficients. Three
orchestration workers ran disjoint columns; each mathematical phase had
its own 180-second private-process-group cap and one BLAS thread. The
workers all returned successfully and no restart or pause flag remains.

Source 480 supplies arbitrary-integer beta arithmetic and valuation balls
at beta-precision 1024. Controls compare the old ring, integral scaling,
inverse residuals and rejection of an unknown inverse. The next frame
script explicitly clamps imported center errors to this working precision.
The integer-scaling shortcut is used only when the coefficient valuation
is smaller than the ring precision; draft 484 checks that condition.

Source 481 refines all seventeen algebraic CM roots on their original
certified Hensel branches and evaluates the fixed rational residue basis.
The exported eta precision is 21168 beta-digits, the work ring has 22224,
and the minimum pre-export frame bound is 22128. All prior frame values
overlap through 384 digits, labels are unchanged and trace sums vanish
to the exported precision. The job takes 7.912 seconds. These are algebraic
CM values, not newly computed harmonic moments at the target precision.

Source 482 consolidates the complete P=400 bank. All **155 D122 input
jobs pass**; their total recorded durations are 3586.909 seconds, with
maximum individual duration 62.703 seconds. This sum is not elapsed
wall time because three workers operated concurrently. D122 files occupy
about 1.068 GB at this checkpoint. Successful sources 476--482 and their
completed outputs are frozen.

## Precisely what remains

Sources **483 and 484 are drafted but have not been run**. They are not
frozen and their output JSON files do not yet exist. No P=400 residue-frame
change, P=400 quadric verdict or improved integral-section lower bound
has been claimed. The last accepted section data remain D118's full-bank
values 3794/3745/3728, with anchor bounds 3576/3248/2984 and sufficient
non-anchor bounds 25330/25444/25551. No positive exact quadric zero,
candidate identification or target field polynomial is proved.

Run the next two jobs sequentially, checking the first receipt before
starting the second:

```sh
python3 dembele/pari/run_dyadic_capped.py dembele/pari/483_dyadic_precision400_residue_frame.py dyadic_residue_frame400_d122_attempt01 'PASS|483_DYADIC_PRECISION400_RESIDUE_FRAME'
python3 dembele/pari/run_dyadic_capped.py dembele/pari/484_dyadic_precision400_quadrics.py dyadic_integral_quadrics400_d122_attempt01 'PASS|484_DYADIC_PRECISION400_QUADRICS'
```

483 uses only actual jets and algebraic CM values, checks all leading
frame rows and the old basis change, and reports the Gaussian without
inverting W's unresolved value. 484 tests all 91 quadrics through four
orders at all 17 points. It records any certified mismatch rather than
assuming agreement. It also recomputes D118's sufficient non-anchor
bound using the new anchor lower bound. Higher intrinsic jets still
require preceding exact zeros.

Then implement an independent D122 review in a new source (486 is the
next unused number). It should cross-multiply refined eta values,
check the root residuals/branch overlap, reproduce the four coarse
coefficients with the alternate kernel/Horner method, and check the
quadric enclosures with an independent direct quotient-ring evaluation.
Preserve all D121 hashes and the completed D122 receipts. Source 485
is only a provenance/completion snapshot; it is not that mathematical
review. Decide further precision work only after the actual quadric
verdict and audit. A full P=10552 run remains uncosted as a complete solve.

## Resuming safely

The persistent wrapper `dembele/pari/run_dyadic_capped.py` replaces reliance
on `/private/tmp/d115_run.py` for new jobs. It uses frozen runner 272,
refuses existing log/receipt names and archives failed Python sources.
Completed-column files must not be overwritten or recomputed casually.
The temporary worker driver `/private/tmp/d122_columns.py` is no longer
needed; all its columns have finished.

Recheck this checkpoint's recorded source hashes with source 485 `--check`
through the same wrapper and a fresh receipt stem. Its replay covers
this fixed snapshot even if later D122 artifacts are added. The
[source ledger](../data/computed/dyadic_precision400_sources_d122.json)
records the exact distinction between successful internal checks,
provenance checks and the pending independent mathematical review.

Keep D99 nonhyperellipticity, D108's spectral rejection, D120's conditional
P=10552 target, all census/new-level/Hecke/cubic pauses and every downstream
marked-cover, genus-64 section, degree-51 torsion, F256-action and final
field requirement. No correspondence was sent.
