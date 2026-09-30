# Stocktake after D129: proof progress and the next commitments

Date: 2026-09-28. Requested by the user before further execution.
This is a planning review of the saved results, not a new arithmetic
certificate, a D130 milestone, or a fresh independent proof of the
theorems cited in earlier reports. D129 remains the latest completed
computation. No arithmetic worker was launched for this stocktake.

**Decision: retain the dyadic integral-section route, but organize the
next work around an exact geometric conclusion and the remaining path
to the field.** The next bounded computation should price the complete
genus-16 identification certificate. Another isolated precision doubling
is not the default next milestone. The cover construction and target
torsion remain separate research and implementation risks.

## 1. The actual objective

The objective is an explicit polynomial recovering Dembélé's original
residual kernel over F = Q(zeta_32)^+, followed by the required normal
closure over Q. Existence of the nonsolvable extension ramified only
at 2 is already known. Its existence does not depend on our candidate
curve being hyperelliptic.

The intended first field output is a degree-257 polynomial over F,
obtained from a separating, Galois-equivariant invariant of the 257
projective lines in an original two-dimensional F256 representation.
The normal-closure step and its relation to the requested field must
then be certified. Matching a group, ramification set, or a finite list
of Frobenius traces is not a substitute for the original-kernel proof.
See [D100](construction-methodology-d100.md) and
[D51](target-realization.md).

## 2. What is established, and what remains open

| Part of the construction | Current position | Remaining obligation |
| --- | --- | --- |
| Original representations and carrier | D51 identifies both original residual systems in the geometric 2-torsion of the specified canonical genus-64 Y, using the integral all-Hecke argument | Construct arithmetic data for that Y and compute the identified subspace |
| Hyperellipticity | D99 establishes geometric nonhyperellipticity of the intended genus-16 C; the exact candidate is separately nonhyperelliptic | Identify the candidate with the intended C |
| Candidate geometry | An exact smooth canonical genus-16 candidate and exact genus-40 double-cover candidate exist | Identify the marked arithmetic maps, including the additional CM branch labels and the double-cover character/twist |
| Independent CM comparison | The full 16-column harmonic/CM bank is certified at P=800; all 6188 quadric enclosures contain zero | Prove positive-order vanishing exactly using the section-height criterion |
| Scalable evaluator | Column 0 reaches P=3200 and column 1 P=1600, with original-equation verification, CM checks, audits and capped scratch | Cost and execute the full comparison at sufficient precision |
| Cubic cover | Exact special-fibre data and compatible cubic coefficients modulo 31^128 are available; D88 supplies a conditional identification shortcut | Prove its marked-double-cover hypothesis and construct exact global coefficients or an equivalent arithmetic section model |
| Target isolation | D120 settles the norm-97 Euler-cofactor separation and identifies the target available over residue degree 51 | Compute target points, implement the global F256 scalar action, and evaluate a separating invariant |
| Torsion implementation | Separate genus-64/degree-2 and genus-16/degree-51 controls exist | Demonstrate the combined genus-64/degree-51 case at useful precision with the actual arithmetic interface |
| Final polynomial | No target invariant polynomial has been produced | Recognition and exact certification over F, then the required normal closure and original-kernel/ramification conclusion |

The genus-16 curve is an arithmetic coordinate construction for the
route. Its Jacobian alone is not the carrier of the desired residual
constituents. Exact identification of C would be a substantial result,
but would not finish the field construction.

## 3. What the latest computations changed

[D125](dyadic-precision800-d125.md) is the latest improvement to the
complete geometric comparison. Its bounds are:

| Successive positive order | Nonanchor lower bound | Anchor lower bound | Sufficient nonanchor bound with that anchor |
| --- | ---: | ---: | ---: |
| 1 | 4994 | 4776 | 25255 |
| 2 | 4945 | 4448 | 25369 |
| 3 | 4928 | 4184 | 25476 |

All 4641 positive-order enclosures contain zero, but no positive order
is proved exactly zero. Orders two and three require preceding exact
zeros before their intrinsic section-height argument applies. The
Gaussian at W is certified nonzero and remains uninverted; the preferred
direct-section certificate does not require taking that quotient.

D126--D129 chiefly made the evaluator more practical: selective reading,
streamed low-factor reuse, prospective scratch retirement, streamed row
writes, and a complete larger-column validation. In
[D129](dyadic-precision3200-d129.md), the original full residual has
4,454,400 zero scalar coefficients; all 17 CM charts and the separate
audits pass. There are 1934 passing input jobs and two passing reviews.
The ordinary recurrence checks in the additional independent audits are
samples; they are not a second independent implementation of every
original equation.

The P=3200 state coordinator took about 71 minutes, with peak scratch
about 1.23 GB under a 2 GiB cap and maximum single-process input RSS
about 492 MB. These are measured local results, not an aggregate-RAM
bound or a runtime forecast for the complete target. A faster or larger
single column does not improve the full-frame quadric bounds on its own.

Thus the recent work is useful infrastructure progress, with strong
finite arithmetic checks, but it has not closed another geometric
identification step. Passing-job and manifest counts are not measures
of how close we are to the field polynomial.

## 4. Why retain this route

The present route has a specific exactness mechanism. D116 constructs
integral quadratic sections; D117--D118 bound their archimedean norms
and arithmetic heights. D120 propagates the local errors and gives
**P=10552 as a conditional sufficient common precision**. The conditions
include the same certified frame and CM branches, adequate algebraic
CM precision, and future quadric balls that continue to contain zero.
This is neither a proved minimum nor a prediction that the candidate
will pass at that precision.

Once positive orders one, two and three vanish exactly, each quadric
vanishes on 4D. Here deg(D)=17 and deg(2K_C)=60, so the zero divisor
would have degree at least 68. This forces the quadric to vanish
identically. The exact smooth candidate geometry then gives the
isomorphism, as in the [D88 criterion](d88-cm-expansion-identification-review.md).
The order-zero relation is already exact in the arithmetic residue frame.

This supplies a finite mathematical destination for the expensive
computation. The older spectral comparison is ruled out in its tested
form by [D108](shimura-evaluator-d108.md); D120 rejects the current
inverse-frame estimate and a Faltings-only rescue of the existing
bounds. None should be reopened without a new quantitative or
mathematical reason. A direct smaller carrier or a different polynomial
construction could be better, but no executable replacement identifying
the original kernel is currently available.

Confidence should be separated by claim. The saved arithmetic checks
and the D99 nonhyperellipticity argument support strong confidence within
their stated scope. Repeated independent agreement supports retaining
the candidate, but is not an equality certificate or a calibrated
probability. Completion cost and the unresolved cover/torsion steps
remain substantially less certain. This review does not assign a
percentage of completion or a final-field ETA.

## 5. Next work packet: price a complete identification certificate

Source 533 remains unused. Preserve D129 and all earlier frozen files.
The next execution should produce a bounded feasibility report with
these outputs before another actual harmonic refinement:

1. **Target-size operation controls.** Measure original full-map,
   low-RHS and seed-extension actions at P=10552, split by child/backend
   as necessary. Compare the adaptive and GMP paths and available old
   actual overlaps; distinguish synthetic inputs and sampled maps from
   an actual target lift. Control repeated exact residual solves with
   the existing 200-bit factor, including the proposed seven stages
   for a 1319-bit low modulus. No new factorization is justified yet.
2. **A complete schedule comparison.** Compare a staged precision ladder
   and a direct jump, accounting for shrinking correction bands,
   different existing seeds, and D126's measured multiple-RHS reuse.
   Include all sixteen columns, all 17 CM charts, high-precision frame
   and quadric arithmetic, final original residuals, independent audits,
   receipt/review overhead and I/O. Report assumptions and ranges for
   unmeasured components; a single map timing cannot price this stage.
3. **A storage and memory plan.** Inventory temporary and permanent
   payloads, CM data, audit witnesses and metadata. D120 already requires
   38,777,333,760 bytes for sixteen target uniform states alone. The
   present four-dense-payload retention policy exceeds the last recorded
   roughly 80 GiB of free space for the full target bank. Control a
   prospective lossless zero-residual representation and regeneration
   of weighted projections from uniform moments, including full byte
   comparisons and verifier inputs. Existing frozen files are preserved.
   Budget concurrent resident memory separately from scratch disk and
   single-process RSS; recheck free disk before a production commitment.
4. **An exact acceptance specification.** The production deliverable is
   the full independently constructed frame and the 91 relations at
   all 17 CM points through coarse order three, with successive exact
   vanishing certified in the correct order. Verify that the existing
   high-precision algebraic CM data meet the target error requirement.
   A certified nonzero coefficient is a meaningful rejection of the
   candidate and must be retained as such. An enclosure containing zero
   below the height threshold is an explicitly incomplete result.

Keep at most three mathematical workers, runner 272's unchanged
180-second private-process-group cap, assertions and one BLAS thread.
Any new temporary namespace must be declared before use. After a
disconnect, inspect receipts and partial outputs before retrying;
never rerun a completed phase merely because the chat disconnected.

**Decision gate.** If all phases have a capped implementation, the
retained outputs and prospective scratch fit a stated disk reserve,
and the full schedule has defensible measured cost, choose the schedule
and work toward the complete certificate. An intermediate pilot is
justified only by a named remaining uncertainty in that schedule.
If these conditions fail, record the dominant obstruction and make a
specific algorithm, retention or proof-bound change before scaling.
Repeated isolated precision doublings do not satisfy this gate.

## 6. Keep the downstream bridge on the critical path

Before committing to a long full-bank run, accompany the cost report
with a short construction specification for what follows exact C
identification. This is not another generic inventory: each missing
output must name its arithmetic inputs, proposed operation and exact
verification criterion, or explicitly state that no effective method
has yet been supplied.

* **Marked X and Y.** D88's base certificate identifies (C,D17); P32,
  B3 and the arithmetic double-cover character/twist need separate
  proofs. [D87](cm-frame-double-cover-character.md) gives strong sampled
  numerical character evidence, not that proof. The
  [D88 cubic shortcut](d88-cubic-identification-shortcut-review.md)
  applies only after identification of the marked arithmetic double
  cover on the same global X. It identifies a compatible cubic lift
  conditionally, not its exact coefficients. The
  [D86 recognition failure](cm-frame-cubic-128-chatelet.md) is a lower
  height exclusion in specified bases, not an upper reconstruction
  bound. Another ordinary recognition scan needs a new reason to
  succeed or an exact verification/construction mechanism.
* **Arithmetic sections.** Supply exact global Y coefficients or a
  compatible arithmetic section model. The
  [D62 interface](arithmetic-section-interface.md) requires, for a
  divisor of degree 129, at least 646 suitable evaluation points,
  an initial 66-dimensional section space, product spaces, Frobenius
  and auxiliary evaluation data. A Hecke module, a reduction graph,
  or local cubic congruences alone do not supply those entries.
* **Combined torsion cost.** Reuse the
  [D66 degree-51 control](lifttors-degree51.md) and
  [D67 allocation audit](lifttors-allocation.md) to design a bounded
  combined genus-64/degree-51 test before production torsion. Their
  historical monolithic jobs used different limits and are not
  authorized by this plan to bypass the current cap. Until actual Y
  input exists, a scaling control must remain labelled as a control,
  not target torsion. The proposed workspace cleanups are not measured
  improvements until implemented and checked.
* **Scalars and invariant.** D120 already settles local Frobenius
  separation, superseding D100's older instruction to finish it.
  It does not implement the global F256 action on divisor classes.
  That action or an equivalent verified construction, a separating
  invariant, and coefficient certification over F are still required.
  One local Frobenius cannot simply be called the global scalar action.

Solving all downstream problems is not a prerequisite for a valuable
exact genus-16 result. However, a plan to spend substantial resources
on that result must say whether it is delivering that intermediate
theorem or an executable path all the way to the field. At present
only the former has a quantitative exactness target. If the downstream
specification exposes a missing construction, keep that research task
explicit instead of representing it as routine final processing.

## 7. Resumption and provenance

This stocktake supersedes the ordering and scope of the next-task
paragraphs in the D129 entry documents; it does not change D129's
accepted mathematics or freeze. The three immediate outputs are a
complete certificate cost, a verifiable retention scheme, and the
specific downstream construction obligations. The next major
mathematical milestone is exact identification of C, followed by the
marked cover and arithmetic Y interface, target torsion, and the
original-kernel polynomial.

Only local reports and saved specifications were reviewed. No new
external theorem or fresh primary-source verification is claimed.
The handoff, decisions, references and entry documents are updated;
no arithmetic computation, external correspondence, remote launch,
commit, or cleanup was performed for this planning review.
