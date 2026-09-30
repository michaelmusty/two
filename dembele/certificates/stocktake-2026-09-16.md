# Stocktake after descent and CM reconstruction (D61)

Date: 2026-09-16. The user asked whether to keep going or take stock.
This is a strategic review of the saved work and its dependencies,
with the principal descent and Jacobian-input references rechecked.
It is not another reconstruction experiment or a new independent proof
of every earlier mathematical claim.

**Recommendation: take stock now and pause repetition of the current
CM recognition searches.** Retain the curve/Jacobian route as a credible,
well-developed candidate in this repository. Its practical completion
has not been demonstrated, and the present CM-coordinate branch has
not produced its first exact target function value.

## 1. What has changed since the previous strategic review

The [D50 review](route-review-2026-09-15.md) identified three priorities:
the representation comparison, arithmetic input for the target carrier,
and a credible torsion implementation. Subsequent work addressed the
first and made progress on parts of the second. The third remains open.

| Object or step | Current evidence | What it does not yet supply |
|---|---|---|
| Original residual systems | Exact Hecke data; D51's local/global transfer and integral projector argument for the specified genus-64 Y | Computed points or divisor arithmetic on Y |
| Analytic curves and sections | Quaternion domain, local S3 cover, numerical base and cover sections, independent numerical checks | An exact arithmetic section model of C or Y |
| Marked descent | D58's compatible marked-cover argument and cited descent theorem; Q-definition of X,Y under D56's hypotheses | Explicit equations or exact evaluations; a proof of those numerical hypotheses |
| CM residue algebra and labels | Degree-17 field, proved class number 17, D59's ideal classes and Frobenius matching with stated complex inputs | The images of the particular geometric sections in that field |
| Reconstruction feasibility | D60's exact exclusions within empirical boxes | Target membership in those boxes, a height upper bound, or an accepted exact candidate |
| Torsion method | Abstract target subspace and an exact Q8 hyperelliptic control | Generic Makdisi lifting or a representative genus-64 runtime measurement |

The descent and labelled orbit were substantive gains. They resolve
which rational algebra to use and how to put the numerical conjugates
in it. The recent exclusion work tells us which small-height solutions
are unavailable in the chosen neighborhood. It does not measure distance
to a successful reconstruction.

The 111 passing tests validate important pieces of code and exact
controls. They do not certify the target's analytic errors, its exact
model, or the feasibility of the full number-field computation.

## 2. Keep the auxiliary objects distinct from the final target

The known degree-17 CM field is an auxiliary, solvable residue field.
It is not the original nonsolvable extension we want to construct.
Similarly, the genus-16 base C is useful for building arithmetic
coordinates, but the target residual systems are carried by the
specified genus-64 cover Y in the [D51 argument](target-realization.md).

Even complete recognition of X|D and Y|D would give restrictions of two
functions to seventeen points. It would not automatically recover their
global relation, the degree-three cover, its Jacobian arithmetic, or the
target torsion. An explicit global section construction would still
have to connect those finite values to the needed arithmetic model.

The route therefore still has several substantial steps:

    usable arithmetic sections/model of the specified Y
      -> target 2-torsion and arithmetic evaluation
      -> degree-257 projective invariant over F
      -> recognition and certification of the required normal closure.

The genus-16 CM branch is one proposed way of supplying the first step,
through C and the cover. It is not known to be a necessary intermediate
step or the most economical one.

## 3. Why another ordinary recognition run is not the recommendation

The coefficient field, point labels and evaluation-matrix conditioning
have now been addressed. We still do not have an exact target value,
a reduction of the evaluation flag, an upper height bound, or certified
analytic errors. D60 makes the small-height failure more decisive
within its boxes; it does not fill any of those missing inputs.

There is no deduction from a large conditional lower bound to a useful
precision budget. There is also no deduction from rational descent to
small coefficients. Repeating LLL with slightly different scales or
increasing the truncation without a specified new hypothesis would
mostly repeat the same experiment.

A theorem giving an upper height bound is not mandatory for every
numerical discovery attempt: exact verification can establish a
candidate after heuristic recognition. But after this sequence of
failures, another attempt needs a concrete reason to expect new
information, such as a different function with controlled divisor data,
an independent reduction, or a measured accuracy target attached to a
specific candidate. None has yet been supplied here.

## 4. The arithmetic interface that would actually advance the route

[Mascot's torsion method](https://arxiv.org/abs/1808.03939) starts from
arithmetic curve/Jacobian input and the relevant Galois subspace.
An equation is not essential if adequate section-evaluation data are
available. In the [later paper, Definition 2.1.1 and Remark 2.1.6](https://arxiv.org/pdf/2004.14683),
the input consists of a sufficiently positive line bundle, sufficiently
many points with Frobenius action, local trivializations, a matrix of
section values preserving rank on reduction, and a local Euler factor.
Its modular construction obtains these values from elliptic moduli.

Thus an equationless approach can bypass writing down a plane equation,
but still needs an arithmetic mechanism for evaluating the sections.
No such replacement mechanism has been implemented for our quaternionic
curve. Naming Makdisi arithmetic or a known residue field does not
supply that input matrix.

Two possible outputs would justify renewed construction work:

* An exact arithmetic function or section relation on the actual C,
  together with a specified method for extending it to a usable global
  model and the cover Y. One recognized CM value is a useful initial
  checkpoint, not completion of this output.
* A finite-field or p-adic section-evaluation construction for the actual
  Y that supplies the required Jacobian input without first reconstructing
  the chosen X,Y. It must explain how the entries are obtained from
  available arithmetic data, without assuming the missing model.

These are research targets, not existing callable algorithms in the
workspace. D57 already audited the available input; another generic
inventory would not count as progress. Continuing requires a new
construction or a changed, testable reconstruction hypothesis.

## 5. Checks to prioritize before a major computation

The mathematical dependencies deserve review alongside algorithm design.
The repository's nonhyperellipticity argument conflicts with
[Dembélé's Theorem 5.9](https://arxiv.org/pdf/1906.06772). D45 gives exact
graph calculations and an arithmetic graph identification; repeating
the finite automorphism enumeration alone would not independently
resolve that geometric conflict. The correspondence between the saved
quaternion datum, the stable model and the canonical curve is the
relevant check. This review does not overturn D45 or claim to have
settled that conflict afresh.

D58's descent argument uses the earlier Lemma 5.2 and
[Sijsling--Voight's marked-map theorem](https://jvoight.github.io/articles/birch-descent-021420.pdf),
independently of the disputed hyperellipticity statement. Its function
consequences retain the ordinary-point and moment assumptions. D59's
complex orientation and root comparison are additional stated inputs.
A focused audit should check these dependencies rather than treating
the number of passing tests as their substitute.

Separately, the intended torsion backend needs an end-to-end control
using its actual divisor representation, group operations, lifting and
evaluation. The existing Q8 calculation uses hyperelliptic Jacobian
arithmetic and does not yet exercise that backend. A representative
cost measurement should precede a large investment in the genus-64
front end; no runtime is inferred here from a small control.

## 6. Recommendation and stopping rule

Retain the descent, orbit labels, exact Hecke data and the curve/Jacobian
strategy. Put further scans in the same CM coordinates on hold while
choosing an arithmetic construction that can feed the global model or
Jacobian interface. The next experiment should state its required
inputs, exact output, independent check, and the downstream operation
that becomes possible if it succeeds.

If no such construction can be specified, report that gap and redirect
effort to the missing mathematics or compare a materially different
carrier/function. More digits and more negative certificates are not
a replacement for that choice. This is a recommendation to change the
next unit of work, not a proof that the broader route cannot succeed.

This stocktake is complete. It starts no new numerical search, does not
claim a replacement arithmetic algorithm has been found, and does not
select a production torsion prime. The previous 111-test result remains
the latest implementation check; tests were not rerun for this review.
The decisions, references and handoff are updated. All work remains
local and uncommitted, with no computation running.
