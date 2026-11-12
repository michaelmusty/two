# D137: approved full-bank P1600 checkpoint admission

The user selected the recommended P1600 checkpoint with “proceed” on
2026-10-06. This authorizes lifting columns 2–15 from P800 to P1600 and
subsequently assembling and comparing the full bank at common precision
P1600. Column 0 is already certified at P6400 (D133); column 1 is already
certified at P1600 (D127). It does not authorize a P3200/P6400/P10552 full
bank or the multiweek target run.

This is an admission certificate, not a completed arithmetic checkpoint.
The fixed admission artifact and its capped creation/replay receipts
record whether every condition below passed. Running progress and later
column completion records are separate from this frozen report.

## Inputs and bounded execution

Source 566 rehashes the entire 94,006-entry D136 catalogue, authenticates
its later review receipts, and supplies fourteen lossless CM metadata
adapters. Each adapter references the existing P800 moment binary without
copying it or assigning it new precision. The actual P800 uniform state
seeds and original full-residual certificates remain frozen.

The arithmetic engine remains source 554, with the source-547 transaction
store and source-551 duplicate-metadata archive. Each configured column
has 6,588 production phases, 25 archives, 24 independent audit jobs and
two column-review jobs: 6,639 capped jobs per column, 92,946 for all
fourteen. Every job uses the existing 180-second private-process-group
wrapper, assertions, and one numerical-library thread.

The global limit remains three mathematical workers. Each successful
worker must report at most 2 GiB measured RSS; summing three measured peaks
must remain at most 6 GiB. This is measured admission, not an OS hard
memory cap. The private working store remains bounded by 2 GiB. Source
566 independently reconstructs its lifetime inventory and compares the
same formula with all three frozen D132 inventories before admitting
P800→P1600. The bank checks a 10 GiB free-disk floor before each column.
D135 estimates 15.2–17.7 active hours and roughly 3–4 GiB extra retention;
these are forecasts, not bounds or calendar completion promises.

The new production coordinator retains the frozen phase schedule, uses
a running submission window, and stops admitting jobs after an observed
failure. Passing receipts may be reused only with matching commands,
drivers, logs and metadata. Partial or failed attempts require inspection;
they are preserved, not automatically retried or erased. Columns run
sequentially; their production, audits and reviews never overlap with
another column's mathematical work.

## Independent validation and incremental provenance

Source 564 generalizes the pure integer-quotient checker from source 556.
It checks every old weighted state overlap and exact mass, every old CM
moment overlap, all 68 old coarse overlaps, three sampled original-state
recurrences, three sampled composed-CM recurrences, and six independent
Horner evaluations per new column. The full new weighted original
equations are checked by the authenticated production engine; the
independent original-equation checks are samples and are labeled so.

Source 565 independently specifies every phase, checks every production
and archive receipt, verifies the sealed store and all current full/row
hashes, checks the complete epoch history and retired manifests, and
accounts for all 24 independent audit jobs. Its generalization is tested
against the entire completed D133 production history and store. The five
independent audit types are also tested against frozen D133 answers.
Submission-window success/failure fixtures and exact schedule equality
are checked before admission.

Each column review keeps its own source catalogue and binds the immutable
admission root. It does not copy or rehash all inherited 94,006 entries
again. Touched inherited files must retain their inherited hashes. A
second capped review invocation rehashes that column's complete catalogue.
A final full-bank review must bind the admission root, all fourteen column
review roots and their receipts, and the bank/frame/quadric calculations.
This avoids cumulative catalogue duplication without discarding evidence.

## Completion boundary and mathematical limits

`run_d137_bank.py` durably runs all fourteen columns, their independent
audits and fixed reviews. Its final artifact is
`dyadic_checkpoint_columns_completed_d137.json`. That artifact explicitly
leaves bank assembly, common-P1600 residue-frame/quadric comparison and
final provenance review pending; those follow within the approved
checkpoint scope. Until those finish, the certified full-bank comparison
remains P800. The coordinator never launches another precision tier.

No positive-order exact quadric zero, candidate curve identification,
arithmetic double-cover identification, global torsion action or defining
field polynomial is claimed by this admission or by a single new column.
The conditional P10552 sufficient target and the outstanding marked-base
and Hecke hypotheses of D134 are unchanged.
