# D152: the precision fallback still needs a multiweek bank

Date: 2026-10-09. Bounded cost review after D151; no precision run admitted.

**Result:** the existing rank-45 certificate reduces the direct section
route's conditional sufficient target from P10552 to **P10480**. This is
a small saving: the updated plan still requires about **20.6--29.2 active
days**, **1,059,939 bounded column jobs**, and **71.5 GiB free including
the existing 10 GiB planning reserve**. The observed free space is 51.5 GiB,
about 20.0 GiB short of that planning requirement.

The next useful preparation is a single-column P1600-to-P3200 timing
pilot with the indexed coordinator, estimated at **2.9--3.4 active hours**
and **0.46--0.59 GiB additional retained space**. Prepare its concrete
admission and independent checks before a launch decision. This report
does not launch that pilot or commit to the full bank. P3200 by itself
has no new exact-identification implication from these height bounds.

These are empirical planning scenarios, not runtime or storage bounds.
P10480 is a sufficient design only if new certified data meet the stated
error and zero-enclosure hypotheses. It is not a predicted successful
identification, a necessary precision, or a field-polynomial ETA.

## 1. Which proved height enters the precision design

The [D148 relation-space bound](P1600-forward-frame-bound-d148.md)
is h_ext(I_2)<15237, while the saved P1600 exterior-lattice test would
suffice at 623. These are heights of a rational relation space in the
fixed residue coordinates. They cannot be substituted for the arithmetic
line height in the direct section test. Nor is the observed change in
the lattice gap between 96 and 160 training bits a theorem about future
Gram--Schmidt lengths.

The already costed fallback is instead [D118](cm-finite-height-d118.md)'s
integral section q_Q=Q(s)/Delta and [D120, section 3](construction-reassessment-d120.md)'s
uniform error propagation. For coarse order n, its finite zero budget
F_n uses the proved CM-fibre upper and Faltings lower bounds. A future
calculation must supply:

- Correctly labeled actual moments and coarse coefficients, with common
  raw error E=2P+32 in beta valuation.
- Residue-coordinate eta values to at least E, beta-ring arithmetic to
  at least 2P+64, and the certified branches and fibre normalizations.
- Quadric enclosures containing zero through the propagated errors.

Under these hypotheses the integral-section bounds are

    N_n(P)=2P+3310-33n,        at the sixteen nonanchor points,
    A_n(P)=2P+2784-296n,       at the anchor.

The sufficient strict zero inequality is

    (16N_n(P)+A_n(P))*log(2)/272 > F_n,

or equivalently

    (P/8+(55744-824n)/272)*log(2) > F_n.               (1)

Source 632 recomputes the thresholds from the frozen rational intervals.
Source 633 uses a different logarithm implementation and reconstructs
the uncollected section norm, fibre degree and Faltings contribution.
For each order it verifies success at the listed multiple of eight and
failure at the preceding one, within this sufficient uniform design.

| Positive order | Frozen basis, L1 maximum 42550 | Recognized basis, L1 maximum 29299 |
| --- | ---: | ---: |
| 1 | P10416 | P10408 |
| 2 | P10480 | P10480 |
| 3 | P10552 | P10544 |

The shorter basis was already proved integrally equivalent in D140.
It does not improve the two-order target. P1600, P3200 and P6400 fail
all three uniform design inequalities; that is not a claim that their
actual residuals are nonzero or that no stronger certificate could work.

The P1600 measured valuations exceed this conservative propagation by
117/101/117 beta-digits at the nonanchor points and 688/656/688 at the
anchor. D138 also observed a linear improvement from P800 to P1600.
This report does not extrapolate those extra digits into a universal
error law. The certified D120 law suffices for the planning conclusion.

## 2. Why the rank-45 certificate removes the third positive order

By [D140](dyadic-P1600-recognition-d140.md), the actual restriction map
using orders 0, 1 and 2 at nonanchor CM chart 1 has rank 45 after
expansion in the local degree-16 field. It factors through actual
canonical multiplication, whose image has dimension 45. Hence it is
injective on that multiplication image, and its exact kernel is the
actual 91-dimensional quadratic relation space.

Order-zero vanishing of each candidate quadric is already exact in
the residue frame. If the first application of (1) proves order one
zero, the intrinsic order-two section is defined; the second application
then proves order two zero. The CM conjugacy and integral-section
construction are the ones already used in D116--D120. In particular
these conclusions give exact zeros at the D140 restriction point.
Each quadric therefore lies in that map's exact kernel and is an
actual relation. The candidate's established rank and scheme certificate
then identify the marked base (C,D17).

Thus **P10480 is a conditional sufficient common design**. The older
order-four divisor-degree argument remains valid at P10552; it does
not require the rank refinement. A finite enclosure that merely contains
zero at lower precision supplies neither exact kernel inclusion nor
the induction hypothesis for the next intrinsic jet.

This argument retains all sixteen harmonic columns: the current evaluator
uses all leading evaluation rows in the cofactor frame and all columns
in the change of basis. The rank certificate reduces the highest positive
order needed for proof; it does not supply those missing high-precision
frame entries from the existing column 0 alone. The cost model retains
all four coarse coefficients and gives no additional saving for dropping
order three. Alternative evaluators are not ruled out.

## 3. Updated schedule and cost method

The starting bank is [D138](dyadic-precision1600-bank-d138.md): all sixteen
columns at P1600, with column 0 at P6400. All existing artifacts are
retained. The staged P10480 schedule is:

| Stage | Columns | Jobs per column, including archives/audits/reviews | Largest logical working store |
| --- | ---: | ---: | ---: |
| P1600 to P3200 | 15 | 12,570 | 304,049,792 bytes |
| P3200 to P6400 | 15 | 24,579 | 973,167,872 bytes |
| P6400 to P10480 | 16 | 31,419 | 2,005,700,320 bytes |

Each working store fits the unchanged 2 GiB logical cap. A direct
P1600-to-P10480 stage needs 4,711,815,952 bytes under the same inventory
and is rejected by that cap. No change to the storage protocol is assumed.

The empirical baseline is the reviewed [D139 model](dyadic-indexed-recost-d139.md),
which incorporates measured P1600 job floors and the indexed receipt and
archive work. Source 632 reproduces its P10552 job counts, storage totals
and timing scenarios before evaluating the smaller target. It retains
D139's per-phase mean job costs, adjusting only exact phase counts, and
retains its full bank-level review and final comparison allowances.
It takes no credit for smaller arithmetic operands, faster final checks,
more workers, batching columns, deletion, compression or remote compute.

This local sensitivity calculation is not a new production benchmark.
In particular the indexed coordinator has not yet supplied an integrated
new-column timing. D138's completed P1600 run took 22.05 active hours;
the older 15--18-hour forecast was optimistic because directory/archive
overhead grew. D139's replacement avoids the identified scans, but that
does not make its overall timing an observed production result.

| Scope | Column jobs | Active time scenarios | Additional retained space scenarios | Free space with 10 GiB reserve |
| --- | ---: | ---: | ---: | ---: |
| Full P10480 staged bank | 1,059,939 | 493.9--699.4 h, or 20.6--29.2 days | 51.0--61.5 GiB | 71.5 GiB |
| Full P10552 baseline | 1,068,035 | 498.7--706.4 h, or 20.8--29.4 days | 51.4--62.0 GiB | 72.0 GiB |
| One P1600-to-P3200 timing pilot | 12,570 | 2.9--3.4 h | 0.46--0.59 GiB | 10.6 GiB |

Column jobs include archives, audits and review allowances. Bank comparison
and provenance-shard jobs are additional, with time/storage allowances
already carried in the model. Active days mean 24 hours of execution;
sleep, pauses, contention and setup are not calendar-time guarantees.
The single-column pilot retains the entire P3200 bank's graph-review and
comparison allowances, rather than dividing every cost by fifteen.

The target reduction saves **8,096 jobs**, **4.8--7.0 active hours**, and
**573,307,248 bytes** in the retained-space allowance. It does not change
the overall commitment. The main modeled costs remain repeated operator
sweeps, right-hand-side construction and row preparation. Omitting a
coarse jet or improving receipt lookup alone does not remove that work.

## 4. Current storage and the already resolved memory question

The saved filesystem observation at 2026-10-09 16:59:45 UTC is
**51.4984 GiB free**. It is an observation, not a reservation. Compared
with the P10480 plan's 71.4703 GiB requirement, the shortfall is
**19.9719 GiB**. Plan for at least **72 GiB free** before a complete
bank commitment, preserving every frozen file. The pilot fits within
the present observed space with the same planning reserve.

[D136](dyadic-target-charts-d136.md) already tested all seventeen
complete two-child CM charts at the larger P10552 using compatible
synthetic inputs. The largest measured RSS was 1,914,568,704 bytes;
the sum of the three largest was 5,087,657,984 bytes. The longest
job took 69.749 seconds. These passed the 2 GiB per-worker, 6 GiB
aggregate and 180-second limits. D135's earlier memory extrapolation
warning is therefore historical, not an unresolved missing control.

These measurements do not establish bounds for all future production
data. Each actual job must still meet the existing admission checks.
The 2 GiB working-store inventory is a different limit from process RSS.
Target-scale synthetic control outputs are not certified harmonic values.

## 5. Concrete continuation decision

Prepare one P1600-to-P3200 pilot for **column 2**, whose seed and CM data
already have the D137/D138 review chain. This avoids making the missing
column-1 CM adapter a dependency of the first timing measurement.
Use a fresh namespace and the frozen D139 indexed coordinator as a
candidate; it still requires stage-specific admission and replay.

The preparation must bind the source-554 direct seed/native dependencies,
publish the stage-specific independent audit and bounded provenance plan,
and retain the global three-worker window and every resource limit. The
later transitive review graph does not replace those direct bindings.
A future pilot must validate the weighted equations, old state/CM/coarse
overlaps, all receipts, measured RSS and timeout compliance, then compare
its integrated timing with this model before any wider-bank decision.
It cannot by itself identify the curve.

No further finite rational transfer search is recommended: [D151](summed-transfer-obstruction-d151.md)
excludes that certificate for the selected residual. New geometric or
analytic information remains an alternative to the multiweek computation,
but no cheaper exact comparison is supplied by the inspected packets.
The pilot is a measurement proposal, not a promise that computation will
complete the original-kernel construction. P32/B3 markings, the cover,
canonical Hecke interpretation and target torsion remain separate after
base identification; there is still no field-polynomial ETA.

## 6. Verification and checkpoint

[Source 632](../pari/632_precision_route_cost.py) gives the exact thresholds,
inventory and model adaptation. [Source 633](../pari/633_precision_route_controls.py)
independently reconstructs the uncollected height formula, rejects the
preceding precision multiples, checks job counts and weighted byte widths,
reconstructs the reported peak live-file inventories, and recomputes the
phase-cost sums with rational arithmetic. It also checks the saved storage
shortfall and D136 resource observations. A rank-deficient restriction
control illustrates why the actual rank-45 premise is essential.

The [fixed review](../data/computed/precision_route_review_d152.json),
[source ledger](../data/computed/precision_route_sources_d152.json) and
[completion record](../data/computed/precision_route_completion_d152.json)
bind this report, the finite checks and D151's transitive provenance.
The finite checks do not mechanically verify the geometric rank argument
or the inherited height theorems, and they do not turn empirical timing
scenarios into bounds. Sources 632--634 and passing artifacts are frozen
after completion; source 635 is next unused.

All five D152 jobs use the capped wrapper sequentially. No higher precision
bank, coordinator, new spectrum/census, level, Hecke calculation or cubic
search is launched. The full bank stays P1600 and column 0 stays P6400.
Exact positive vanishing, candidate identification and the field polynomial
remain unproved. The proved relation-height upper 15237 and the P1600
sufficient target 623 remain unchanged.
