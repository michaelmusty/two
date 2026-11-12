# D136: integrated target CM charts and the P6400 metadata interface

Date: 2026-10-06. The seventeen finite controls are complete. Acceptance,
independent review and replay are recorded in the D136 completion record.
This work uses synthetic compatible high digits and increases no arithmetic
precision. It follows the execution gates identified in the
[D135 cost report](dyadic-bank-recost-d135.md).

## Integrated target chart controls

Source 562 runs each complete CM chart at P10552, with both composed children
in one process and the same plan/input lifetime as production source 554.
The first child's output remains live while the second child is computed.
The input is a deterministic synthetic completion of authenticated P6400
weighted rows, preserving every old coordinate modulo its weighted modulus.
Zeroth masses are restored exactly. Arbitrary high digits have no arithmetic
meaning and are not used as a target harmonic column.

All seventeen charts pass under the existing 180-second private-process-group
cap and 2 GiB measured per-job RSS admission. The largest measured peak is
1,914,568,704 bytes (1.783 GiB),
in chart 16. The longest bounded job takes 69.749
seconds. The sum of the three largest measured peaks is
5,087,657,984 bytes
(4.738 GiB), below the 6 GiB
three-worker admission rule. This remains measured admission, not an OS
hard limit or a bound for all future data.

The coordinator uses a submission window of at most three jobs and checks
completed results before admitting replacements. It reuses the separately
completed chart-0 receipt and completes the rest in 337.526
seconds. All seventeen receipts, logs, metadata and synthetic binaries are
retained. No failed input job occurred.

Every complete chart agrees with its certified P6400 CM row in all 102,400
old scalar coefficients and has the prescribed zeroth mass. Source 563
checks all 1,740,800 old scalar overlaps again using direct little-endian
byte comparisons, independently of production decoding. It checks every
target coefficient's unused top bit, binary lengths, hashes and receipts.
The retained synthetic outputs total 473,573,760 bytes and contain
2,870,144 target-size scalar coefficients; these are resource controls,
not new certified CM values.

These results replace the D135 quadratic-memory warning with actual full
chart measurements for all seventeen saved maps and this deterministic
compatible input family. Future production still checks each job's measured
RSS and time. No resource limit is raised.

## Lossless CM metadata adapter

The reviewed D133 seal already supplies the weighted state seed expected
by source 554. Its CM binary lacked a top-level reference object in the
format consumed by that driver's initialization and coarse-overlap phases.

Source 563 publishes
[dyadic_CM_P6400_col00_d136.json](../data/computed/dyadic_CM_P6400_col00_d136.json)
by referencing the existing authenticated CM binary as one seventeen-row
chunk. It copies the 68 reviewed coarse values, retaining beta-error bounds
[12832,12848,12832,12864]. No payload is duplicated, modified or recomputed.
An exact replay must reproduce the adapter byte for byte. Its precision
claim is inherited from the completed D133 certificate.

Review and replay preserve all 93,928 D135 bindings and add the control
sources, coordinator, outputs, adapter and this report. The review does
not import production arithmetic. Sources 562/563 and the coordinator are
frozen when both review receipts pass.

## Next work and user decision

Certified precision remains P800 for the full bank, P6400 for column 0,
and P1600 for column 1. Exact curve identification, arithmetic genus-64
construction and the original-kernel polynomial remain open.

The full bank's bounded incremental provenance review and the lower-column
seed/CM interfaces still need implementation and admission. D135 estimates
15--18 active hours for a full-bank P1600 checkpoint, or 22--31 active days
for the full conditional target bank. The latter needs additional working
volume capacity; the current recommendation is at least 80 GiB free with
incremental review. These are empirical planning scenarios, not ETAs.

A scope/storage preference is pending from the user. The smaller full-bank
checkpoint is the recommended next commitment after its interfaces and
review plan pass. Source 564 is next unused. No actual bank has launched,
no frozen file was removed, and no correspondence or remote job was sent.
