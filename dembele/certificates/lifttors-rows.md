# Native generation of lifting equations (D65)

Date: 2026-09-17. This implements D64's checked row formula and keeps
the D63/D64 source files, builds, machine-readable reports and saved
control logs unchanged.

Subsequent work: [D66](lifttors-degree51.md) completes the optional
genus-16/degree-51 control and fixes an independent auxiliary-table
reduction bug in a separate build. The measurements below remain
specific to the preserved D65 library.

**Result:** all nine D65 jobs pass. The genus-64 known-answer control
at a=2, p=97, e=4 completes under the same 2 GB PARI stack cap and
900-second timeout. One lift takes 514.585 seconds; the complete
control takes 690.829 seconds and verifies equality with the exact
branch divisor and annihilation by 2. Its equation buffer has 1/66
as many entries as the full matrix. Genus-64/a=51 feasibility and
the target arithmetic inputs remain unproved.

The machine-readable result, traces and source hashes are in
[`lifttors_rows.json`](../data/computed/lifttors_rows.json). Individual
logs use the `lifttors_rows_*.out` prefix; the successful collection
summary is [`lifttors_d65_collect.out`](../data/computed/lifttors_d65_collect.out).

## Implementation and correctness

The separate build in `.build/lifttors_rows` exposes three lifting
paths: `PicLiftTors` uses generated rows, `PicLiftTors_D63` retains the
full matrix with the batched kernel, and `PicLiftTors_original` retains
the pinned upstream algorithm. The existing `.build/lifttors` is
untouched. Both builds use the same exact batched divisor validator.

`lifttors_rows.py` checks the pinned source before replacing the
product bank and the column-worker assembly/solve. The rest of the
lifting algorithm, including its precision sequence, multiplication
branch, chart branch and chart workers, is retained. The native path
does not allocate the full derivative matrix K.

`lifttors_rows.c` computes S=V*U0 and H_i=V*N_i once per precision
step. For each complementary Schur column, it generates the block in
[D64's identity](lifttors-extension.md). A shared streaming solver
selects independent original rows modulo p and applies the existing
`matkerpadic` to that small system. Each discarded block is regenerated
to verify the resulting kernel at the full derivative precision,
including when that precision is p. Polynomial representatives are
used for constant entries as required by the upstream p-adic routines.

The selected rows are equations from K and have a unit pivot minor.
Their kernel therefore has a free, normalized basis. The complete
residual check proves that this kernel is contained in ker(K); the
reverse inclusion follows from row selection. A full-rank unit minor
already proves the kernel is zero and requires no replay. A nonfree
kernel caused by rank dropping on reduction raises the same explicit
good-reduction error as D63. This argument uses every equation and does
not rely on a sample of residuals.

Only a row block, the selected rows, their kernel and the caches are
retained during this solve. PARI temporaries are reclaimed after each
block or row-basis update. The other Jacobian operations and Schur
setup are unchanged and may still dominate time or memory. The block
formula does not reduce every allocation in a torsion lift.

## Verification

The runner generates checked copies of existing controls with only
their loader and explicitly listed comparison additions changed. The
templates themselves remain unchanged; generated-file and build hashes
make those transformations inspectable.

* The native block generator agrees with the independent GP formula
  and all 11,172 original derivative entries from D64's four systems
  (a=2/51, derivative precision 97/97^2). Its kernels satisfy every
  original equation and have the same free span.
* Sixty three-way torsion comparisons agree between upstream, D63
  and native row generation. These include the origin and four Q8
  generators, final/initial precisions (2,1), (3,1), (5,1), (7,2),
  (16,3), (64,1), and one/two worker threads. Membership, torsion,
  reduction and the independently saved exact lift are checked.
* The same solver passes twelve prescribed-kernel cases at precisions
  p, p^2 and p^5, with ranks 0,1,9,17. The first two 256-row blocks
  vanish, forcing later blocks to matter. Six rank-drop perturbations
  raise the required good-reduction error. These fixtures use stored
  blocks; production uses the same solver with generated blocks.
* The full Q8 control completes torsion lifting, Frobenius, evaluation
  and recovery of a degree-15 polynomial with splitting field Q(i).
  Its output binary has a separate D65 filename.

The GP PASS marker is accepted only with one data record and no error.
Five invalid-log fixtures are rejected; ordinary PARI stack-growth
warnings are permitted. Checked source generation also rejects either
of two changed assembly boundaries. The existing Python/Sage arithmetic
sources are unchanged; their latest full regression result remains
D63's 111 passing tests.

| Known-curve control | Lift, seconds | Whole process, seconds | Result |
|---|---:|---:|---|
| Genus 4, a=2, e=4 | 0.261 | 0.365 | PASS |
| Genus 4, a=51, e=4 | 8.263 | 9.957 | PASS |
| Genus 16, a=2, e=4 | 10.070 | 12.401 | PASS |
| Genus 64, a=2, e=4 | 514.585 | 690.829 | PASS |

The genus-64 point is the same independently known [(0,0)-(1,0)] on
y^2=x^129-x, with d0=129, 646 evaluation points and section dimensions
66/195/324. Initialization takes 7.525 s, the initial doubling and zero
check 32.765 s, and the final lift checks 40.936 s. Whole-process time
also includes constructing the point and checking that it is nonzero.

D63's saved one-lift time is 613.521 s; this run is about 16% shorter.
These are single local runs, not a general speedup claim or a production
forecast. The two native kernel solves account for 77.306 s of the
514.585-second lift. Most time remains outside that stage, including
Schur setup, caches and group operations. Degree-51 performance is only
measured here at genus 4; the control point itself is rational.

The initial collector incorrectly treated a normal stack-growth warning
as a failure after the genus-64 GP control had passed. The collector
was corrected and tested, and `--collect` produced the passing report
from the completed logs without rerunning the arithmetic. The original
aggregate run log retains that parser failure; it is not a failed
genus-64 computation.

## Genus-64 kernel storage

At g=64, a=2, p=97, e=4, both derivative systems have 21,252 rows,
259 columns, rank 129 and kernel dimension 130. Each is processed as
66 blocks of 322 rows. Both passes scan and replay all 66 blocks.

| Object or checkpoint | First precision step | Second precision step |
|---|---:|---:|
| S,H cache object, bytes | 14,195,944 | 14,279,480 |
| Largest equation block, bytes | 7,311,136 | 7,343,000 |
| Selected-row object, bytes | 2,930,776 | 2,944,200 |
| Kernel object, bytes | 1,350,408 | 1,887,560 |
| Largest internal kernel stack checkpoint, bytes | 30,298,840 | 30,972,760 |
| Kernel computation including replay, seconds | 38.390 | 38.916 |

The cache column counts only the newly formed S and H; C*A^-1 and rho
are already owned by the caller. The stack checkpoint excludes those
caller objects and the S,H cache. Neither is total peak process memory.
The equation buffer holds 83,398 field entries instead of the full
5,504,268, exactly a factor of 66 in entry count. Other group operations
still grow the PARI stack to the unchanged 2 GB cap during the lift.

## Scope and reproduction

Run from the repository root:

```sh
python3 dembele/pari/build_lifttors_rows.py
python3 dembele/pari/107_lifttors_rows.py
```

The runner checks the new library and generated-source digests, then
D64's strict checks of the untouched D63 build and recorded inputs.
`--collect` reuses saved logs; `--only` selects named controls without
writing a report that would imply completion of the full suite. Each
job uses a 512 MB initial PARI stack, a 2 GB maximum and a 900-second
wall timeout. A timeout kills the whole local process group.

The next bounded cost check is genus 16 at degree 51 and precision
97^4, using the existing native control and unchanged limits:

```sh
python3 dembele/pari/107_lifttors_rows.py --only genus16_a51
```

This optional job is excluded from the default suite and has not been
launched. It tests how the remaining group operations and live Jacobian
data scale after eliminating the full equation matrix. Keep a larger
genus-64/a=51 attempt dependent on those measurements; no higher cap
or production-precision run is implied. Further kernel tuning without
a measured bottleneck is not the next task.

The stored `sizebyte` values count object trees. Stack traces are
checkpoints relative to entry into the cache or kernel routine, and
exclude live objects allocated by its caller. They are not peak stack
or RSS measurements. Successful completion under the cap remains a
separate measured fact from these diagnostics.

No genus-64/a=51 job or production precision is included. The known
control torsion point is rational even when the coefficient field has
degree 51. Actual target arithmetic sections and a mechanism to lift
them remain missing; see the
[section interface](arithmetic-section-interface.md). No target torsion
or nonsolvable polynomial has been constructed. Repeated CM scans stay
paused, with the earlier geometry and descent qualifications unchanged.

## Attribution

Mascot's pinned
[lifting implementation](https://github.com/nmascot/LiftTors/blob/fd6403caf7147b21b67dcb17dbedccea762d6262/lift.c)
supplies the Jacobian and lifting algorithms. The row identity, native
storage adaptation and comparisons are local work. D64 records the
derivation against that exact source. PARI's
[library manual](https://pari.math.u-bordeaux.fr/dochtml/html-stable/usersch5.html)
documents the stack discipline used here; its
[object-size documentation](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Conversions_and_similar_elementary_functions_or_commands.html#sizebyte)
specifies the diagnostic's meaning. No target-scale feasibility or
arithmetic frontend is attributed to these sources.
