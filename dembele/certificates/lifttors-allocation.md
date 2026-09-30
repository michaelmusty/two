# Allocation and timing audit of the corrected backend (D67)

Date: 2026-09-17. This follows D66's bounded genus-16/degree-51
calibration. The diagnostic build preserves the D66 arithmetic,
precision sequence, random calls and reclamation points. No genus-64
job, larger stack cap or production precision is introduced.

**Result:** all three D67 jobs pass. The instrumented genus-16,
degree-51 control completes in 444.494 seconds, including a
368.023-second lift, with the exact-divisor and 2-torsion checks.
Group multiplication occupies about 82% of the lift. The audit finds
an obsolete product workspace retained through those operations and
uncollected product temporaries. It selects a concrete cleanup
experiment; no memory optimization has yet been applied.

Results and source hashes are collected in
[`lifttors_profile.json`](../data/computed/lifttors_profile.json).
The raw traces are `lifttors_profile_genus4_a51.out` and
`lifttors_profile_genus16_a51.out`. Each process has the existing
2 GB PARI stack cap and 900-second wall limit.

## What is measured

`build_lifttors_profile.py` creates `.build/lifttors_profile` from the
verified D66 build, preserving all earlier sources, libraries and logs.
The hooks record entry/exit and selected stage boundaries in twelve
functions: reduction, lifting, inflation/deflation, group multiplication,
chords and negation, divisor addition/subtraction and its validator,
and p-adic kernel/equation construction.

Each event records the function and parent call, precision, cumulative
wall time, absolute PARI stack use, use since function entry, current
stack capacity and, where applicable, object-tree size. Nested call
identifiers allow inclusive and exclusive timing totals without adding
overlapping parent/child times. Stack-growth warnings are associated
with the innermost active call and its preceding checkpoint.

These are **checkpoints**, not peak memory measurements. Absolute
stack use includes the caller's live data; a local difference includes
unreclaimed temporaries as well as reachable objects. `sizebyte` counts
object trees and can count shared data more than once. No peak RSS is
measured, and a checkpoint after a library call can miss its temporary
maximum. Timings include tracing overhead and are single local runs.

## Controls on the instrumentation

The collector removes the inserted hooks and compares the remaining
C tokens, including literals and operators, with all four preserved
source files. No original arithmetic or reclamation statement changes.
The hooks allocate no PARI objects and do not use the random generator.
The cumulative timer uses PARI's `walltimer_get`; a local check confirms
that `walltimer_delay` resets the timer and would be unsuitable here.

Script 113 compares tracing disabled/enabled for the origin and four
saved Q8 torsion points, at final/initial precisions (2,1), (5,1),
(7,2), and (64,1). All twenty cases produce identical matrix
representatives and random states, agree with the independently saved
points and remain killed by 2. These include both lifting branches,
odd precision and nontrivial starting precision, with one worker.

The genus-4/degree-51 control also passes in 10.319 seconds overall,
including an 8.539-second lift. Its 1,054 events form 251 complete,
properly nested calls. This curve takes the chart branch; genus 16
takes the multiplication branch at the same p=97 and exponent 4.
The genus-16 trace contains 1,270 events in 294 complete, properly
nested calls. Initialization takes 6.399 s, initial doubling/zero
checking 20.723 s, the lift 368.023 s and the final lift checks
25.275 s; total process time is 444.494 s. The independently supplied
branch divisor and its annihilation by 2 are checked. D66's uninstrumented
control takes 440.569 s overall and 364.732 s per lift. This single
comparison does not isolate instrumentation overhead from machine
variation. All jobs and the collector exit successfully; none remain running.

Within the instrumented lift, the function-level timer records
368.021 s, differing from GP's surrounding measurement by 2 ms.

| Work inside the lift | Calls | Inclusive seconds |
|---|---:|---:|
| Group multiplication (`PicMul`) | 2 | 300.179 |
| Inflation (`PicInflate_U`) | 2 | 17.649 |
| Divisor subtraction (`DivSub`) | 56 | 309.222 |
| Kernel construction (`matkerpadic`) | 61 | 243.680 |
| Equation construction (`mateqnpadic`) | 56 | 59.721 |
| Precision reduction (`PicRed`) | 2 | 0.098 |

These rows overlap by nesting and must not be summed. The two
calls with scalar arguments 97 and 97^2 take 101.760 and 198.419 s.
They contain 26 chord operations and two negations. Kernel and equation
construction are disjoint leaf categories and together account for
303.401 s, about 82% of total lift time. By contrast, copying reduced
Jacobian data has negligible measured runtime, though its retained
memory is material. The two generated-row kernel stages take 40.808 s,
about 11% of the lift, consistent with D66.

## A measured workspace lifetime

At entry into the genus-16 lift, the caller already occupies
273,164,736 bytes of PARI stack. In the first precision step:

| Checkpoint | Absolute stack bytes | Since lift entry | Object-tree bytes |
|---|---:|---:|---:|
| Reduced J2, exponent 2 | 394,667,016 | 121,502,280 | 120,425,152 |
| Product matrix GWV formed | 531,191,520 | 258,026,784 | 34,458,640 |
| Row kernel returned | 596,514,032 | 323,349,296 | 974,528 |
| Schur temporaries collected | 532,161,584 | 258,996,848 | 974,528 |
| Inflated point collected | 537,714,136 | 264,549,400 | 5,552,800 |
| Multiplication returned | 542,767,288 | 269,602,552 | 5,053,392 |

Forming GWV adds **136,524,504 bytes** to the stack while its
representing tree has 34,458,640 bytes. This difference identifies
temporary storage worth reclaiming; it is not itself a measured peak
or an exact count of unreachable bytes.

The source sets `avrho` **after** forming GWV. The later
`gerepileupto(avrho,KM)` releases Schur and kernel temporaries but
retains that preceding product workspace throughout inflation and
group multiplication. Source inspection shows no further use of GWV,
its Schur partition, inverse or residual after the kernel is obtained.
J2, U, U0 and the precision data must remain available.

At exponent 4, J2 aliases the original full-precision J rather than
creating another reduced copy. The product checkpoint nevertheless
adds 136,532,240 bytes for a 34,459,648-byte matrix. After Schur cleanup,
139,608,256 bytes remain above lift entry; most of that increment is
the product workspace. This second step independently exhibits the
same lifetime issue without a newly reduced Jacobian.

The first expansion from roughly 1 GB to the 2 GB cap occurs in
`matkerpadic` called by `DivSub` inside the first inflation. Immediately
before that kernel, stack use is 946,983,360 bytes and the constraint
matrix has a 65,191,936-byte tree. The warning precedes the rank-selection
checkpoint. It locates an allocation inside that interval; it does not
measure its maximum. Earlier growth from 512 MB occurs in the bounded
dimension validator during the known point's nonzero check.

The largest observed checkpoint is **1,053,617,264 bytes**, after
the inverse in that first inflation kernel. This is 780,452,528 bytes
above entry to the lift, including its retained objects and temporary
allocations. The kernel's own increment is 106,633,904 bytes, while
the returned inverse has a 36,350,104-byte tree. Internal field-arithmetic
temporaries between checkpoints remain unmeasured. The fact that the
stack grew to 2 GB does not mean that 2 GB was observed in use.

## Next bounded change

The audit supports a specific reclamation experiment, preserving the
current diagnostic build and the same caps:

1. Mark the reclaimable Schur workspace after retaining J2 and its
   precision data, **before** constructing GWV. Once KM has been
   obtained, collect KM to that earlier mark. Both lifting branches
   should then start without the obsolete product workspace.
2. Give `DivMul` a local PARI stack mark and return a collected product
   matrix, so intermediate field products do not remain with its caller.
   The original function currently returns the matrix directly.

These are proposed changes, not implemented speedups or demonstrated
memory savings. They require comparisons against the preserved path,
including the chart and multiplication branches, precision boundaries,
known exact points and full degree-51 controls. Do not remove required
Jacobian fields to save memory; D66's auxiliary-table correction remains
part of the arithmetic interface.

Neither change reduces the size of the necessary field-valued matrices
or supplies the missing arithmetic data for Y. D66's conditional
genus-64 object-size projection remains conditional. A genus-64/a=51
run and any larger cap remain outside this gate. Repeated CM scans stay
paused; no target sections, target torsion or nonsolvable polynomial
have been obtained.

## Reproduction and sources

```sh
python3 dembele/pari/build_lifttors_profile.py
python3 dembele/pari/112_lifttors_profile.py
```

The runner verifies the preserved D63–D66 chain, the diagnostic build
hashes, source equivalence, native control results and trace nesting.
`--collect` uses saved logs; `--only` selects jobs without writing a
full report. It rejects incomplete traces, malformed nesting, invalid
stack ranges and inconsistent cumulative timing. Ordinary stack-growth
warnings are permitted and recorded.

The inspected primary sources are Mascot's pinned
[lifting code](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/lift.c),
[divisor arithmetic](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/pic.c),
and [linear algebra](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/linalg.c),
together with the preserved local adaptations. PARI's
[library manual](https://pari.math.u-bordeaux.fr/dochtml/html-stable/usersch5.html)
provides the stack API, and its
[object-size definition](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Conversions_and_similar_elementary_functions_or_commands.html#sizebyte)
governs the tree measurements. Instrumentation, controls and lifetime
analysis are local work; no new geometric or descent theorem is invoked.
