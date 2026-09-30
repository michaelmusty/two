# Lifting memory audit and streamed products (D63)

Date: 2026-09-16. This follows D62's observed failure and the user's
instruction to address it before a major arithmetic frontend effort.
The control curve is known explicitly and is not the target Y.

**Subsequent D64 result:** the planned genus-4/degree-51 calibration
now passes; see [lifttors-extension.md](lifttors-extension.md). It
measures equation storage and verifies a row-generation prototype.
The D63 backend and results below remain unchanged. Its historical
next-step statements are superseded by that report.
The later [D65 native path](lifttors-rows.md) implements generated
equation blocks in a separate build, preserving this D63 baseline.

**Result:** the genus-64 control now passes under the unchanged 2 GB
PARI stack cap. One lift to 97^4 takes 613.521 seconds; the whole
control, including setup and independent checks, takes 784.161 seconds.
This clears D62's measured small-extension failure. It does not establish
feasibility at the target's residue degree 51 or supply target sections.

## Cause and change

The pinned [LiftTors source](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/lift.c)
precomputes a vector `V0` of `d0` product matrices before its first
lifting iteration. At genus 64, d0=129, each is a 646-by-195 matrix.
The loop retains both its outputs and intermediate arithmetic
allocations on the PARI stack. In a diagnostic run of that original
algorithm, allocation relative to entry into `PicLiftTors` grows to
570,789,312 bytes after 16 products, 1,140,582,520 after 32, and
1,710,353,704 after 48. It overflows the unchanged 2,000,011,264-byte
stack limit before completing the 129 products. Initialization and the
independent doubling check have already succeeded.

The local adaptation removes that vector. A worker receives the small
coordinate column U0[j], constructs `DivMul(V*U0[j],V)` when needed,
calls the original derivative worker, and retains only its resulting
column of the lifting system. The product and its temporary allocations
are reclaimed using PARI's documented stack discipline. This trades
repeated product computation for lower peak memory. The full derivative
matrix remains; this is not a claim of bounded memory independently of
genus or extension degree.

At a precision step e1 -> e2, the derivative is required modulo
p^(e2-e1). The original code forms products modulo p^floor(efin/2);
the new worker forms them directly at the required precision. Since
e2-e1 <= floor(efin/2), the resulting derivative columns are congruent
at the modulus used by the kernel routine. No equation,
precision step, torsion test or chart condition is discarded. Both
the multiplication and chart branches of the original lift are retained.

The products-only version reaches the first full 21,252-by-259 lifting
system, using 673,338,832 stack bytes relative to the lift's entry, but
the original tall-matrix kernel solve then overflows the same 2 GB
limit. This separate failure is saved in
`data/computed/lifttors_g64_streamed_probe.out`; `--products-only`
reproduces that intermediate algorithm. Its final `/usr/bin/time -l`
resource query was unavailable in the sandbox, so it supplies no peak
resident-memory measurement. The GP stack error itself is unambiguous.

The second adaptation selects an independent row basis modulo p in
batches of 256 rows, retaining each selected row's original coefficients.
Only that small matrix goes to the original p-adic kernel routine.
Every row batch is examined unless a unit full-rank minor has already
proved that the kernel is zero. At higher precision a nonzero kernel
is additionally checked against every original equation modulo p^e.
A failure of the good-reduction premise raises an explicit error.

Why this gives the full kernel: the selected rows R are actual rows of
K and have a unit pivot minor, so ker(R) is free with a normalized
basis L of the expected rank. The batch scan proves the row rank
modulo p. At e=1, this already proves equality of kernels. At e>1,
the complete check K*L=0 proves ker(R) is contained in ker(K); the
reverse containment follows because R consists of rows of K. Hence
the returned kernel is exactly ker(K). The algorithm makes no random
selection or omitted-equation acceptance. Full-rank systems have zero
kernel directly from their unit pivot minor.

The adaptation is limited to generated build files. The pinned checkout
stays unmodified. `pari/lifttors_lift.py` checks each source replacement;
`pari/lifttors_streamed.c` contains the worker. `PicLiftTors_original`
remains callable in the default build for comparisons. `--validator-only`
reproduces D62's algorithms, while `--upstream` omits all local
adaptations. Build manifests record source and adapter hashes.

## Verification

Script 103 compares the original and streamed lifts on the origin and
four independent Q8 torsion generators, using final/initial precision
pairs (2,1), (3,1), (5,1), (7,2), (16,3), (64,1), with one and two
worker threads. Each case checks equality with the original, equality
with the saved lift, membership, 2-torsion and reduction
to its input. All 60 comparisons pass. This includes odd final
precision, a nontrivial starting precision, and both lifting branches.

Script 104 tests twelve 787-by-17 systems with prescribed ranks 0, 1,
9 and 17 at precisions p, p^2 and p^5. Their first 512 rows vanish,
forcing the scan to use later batches. It verifies nullity, every
equation, a free kernel basis and agreement with the original routine
on nonzero-rank cases. Six perturbed systems must raise the specific
good-reduction error. All pass. The test uses polynomial representatives
for every entry, including constants, as required by the upstream
p-adic C routines.

The final genus-64 control uses y^2=x^129-x over the unramified quadratic
extension of Q97, d0=129, precision 97^4, and 646 evaluation points.
Its section dimensions are 66,195,324 and the initialized equationless
Jacobian object occupies 90,719,008 bytes. Both lifting systems have
21,252 rows, 259 columns, rank 129 and kernel dimension 130. The lifted
point equals the independent exact divisor [(0,0)-(1,0)] modulo 97^4,
and doubling it gives zero. The full PASS marker is present.

| Control | Final result |
|---|---|
| Q8 end-to-end | PASS; full 2-torsion, four lifts, evaluation, known Q(i) field |
| Original/batched divisor validator | 70 comparisons pass |
| Original/adapted lifting | 60 comparisons pass |
| Batched kernels | 12 prescribed kernels pass; 6 rank-drop cases rejected |
| Genus 16, a=2, e=4 | PASS; one lift 10.076 s |
| Genus 64, a=2, e=4 | PASS; one lift 613.521 s; full control 784.161 s |
| Existing Python/Sage suite | 111 tests pass in 6.263 s |

For genus 64, initialization takes 7.537 s, doubling plus its zero check
30.507 s, and the final lift checks 39.461 s. The total additionally
includes constructing the supplied point and checking that it is nonzero.
The reported stage times are therefore not a complete runtime profile.
These are single local runs, not production forecasts or a general
performance claim. The stack grows to its 2 GB cap but does not overflow;
no peak resident-memory value is available.

## Scope and reproduction

The full lifting matrix still contains 5,504,268 field entries in this
control. Streaming the products and batching the solve do not make
that storage independent of residue degree. The candidate norm-97
target uses residue degree 51; this control uses degree two and precision
97^4. No run at degree 51, production precision, or on 65,535 target
vectors is included. No target section, torsion point or polynomial is
constructed. The input gap in [the section interface](arithmetic-section-interface.md)
remains separate from backend validation.

The next bounded backend experiment is a smaller known curve at residue
degree 51: script 101 with g=4, a=51, e=4, retaining the same stack cap
and timeout. This would measure the larger coefficient-field cost before
a full genus-64 attempt. It has not been launched. An arithmetic method
for producing the specified target section evaluations remains required;
the successful known-curve control does not construct one.

Build and execute from the repository root:

```sh
python3 dembele/pari/build_lifttors.py
python3 dembele/pari/run_lifttors_controls.py
```

The runner uses a fresh GP process for each control, an initial 512 MB
PARI stack, the unchanged 2 GB stack cap, and a 900-second per-process
wall limit including verification. A timeout kills the whole local
process group. A successful result requires a PASS marker, exactly one
JSON data record and no GP error; GP's exit code alone is insufficient.
`--collect` rebuilds the report from the saved logs without rerunning
the arithmetic. `lifttors_controls.json` includes source hashes, build
provenance, scope flags and the two earlier allocation failures.
Stack checkpoints in the trace are relative to entry into the lift;
they are not peak process-memory measurements.

The earlier D62 report/logs are retained with `_d62` suffixes. The
original allocation trace is `lifttors_g64_eager_d63.out`. To reproduce
that diagnostic with the default build, run script 101 from
`vendor/LiftTors` with GP variable `bench_original=1` and environment
variable `LIFTTORS_TRACE=1`. The products-only build has its own saved
manifest and failed log. Neither failed intermediate is a passing test.

## References

The algorithm is Mascot's, as attributed in
[the D62 control report](lifttors-control.md). The product scheduling
change and diagnostic comparisons are local adaptations.
[PARI's library manual, stack handling](https://pari.math.u-bordeaux.fr/dochtml/html-stable/usersch5.html)
specifies the `avma`/`gerepilecopy` memory discipline used by the worker.
