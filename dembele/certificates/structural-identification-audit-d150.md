# D150: structural identification audit and exact transfer limits

Date: 2026-10-09. Resumption of D149's authorized structural audit.

**Result:** the inspected certificates do not yet identify the candidate
with the actual marked Shimura curve. The exact group, rational frame,
rank-45 actual jet map and candidate scheme are available. What remains
missing is an exact comparison of their multiplication relations. Neither
marked descent, the Shimizu tensor nor the conditional cover criteria
provide that comparison.

There is a new, narrower conclusion about the dyadic alternative. The
finite chart recursion is not an exact finite moment system. Moreover,
no family of finite-dimensional rational-function spaces closed under
**each individual child pullback** can contain the CM Poisson kernel.
An explicit reachable four-edge cycle certifies the hypotheses of the
pole-orbit proof below. This excludes that particular way of replacing
the moment bank by an exact finite solve. It does not exclude identities
using cancellations in the summed transfer operator.

Section 5 gives a precise sufficient identity using that summed operator.
No such identity for a candidate residual has been constructed. The best
proved actual relation-height upper bound remains 15237, versus the
sufficient target 623. Positive exact vanishing, marked identification
and the original-kernel field polynomial remain open.

## 1. Compare the actual inputs with the candidate certificates

The following inventory treats the old reports as statements with their
stated hypotheses, not as interchangeable certificates for one curve.
In particular D88/D106's historical statements that no independent
positive jets had been evaluated are superseded by D115/D138.

| Input | What is established | What it does not establish |
| --- | --- | --- |
| [D62](curve-identification-audit.md), [D99](hyperellipticity-review-d99.md) | The specified arithmetic group, quotient, actual stable graph and nonhyperellipticity | An isomorphism from the candidate, or its canonical ring |
| [D106](cm-rational-frame-jets-d106.md) | Compatible rational descent of the actual marked curve, its unique degree-17 residue-field identification, and canonical projective residue frame | Positive-order equality with candidate coefficients |
| [D110](dyadic-group-transport-d110.md), [D111](dyadic-harmonic-d111.md), [D112](dyadic-cm-matching-d112.md) | Exact arithmetic transports, complete stars and stabilizers, sixteen harmonic measures, and dyadic CM labeling | An exact algebraic presentation of the quotient in the candidate coordinates |
| [D113](dyadic-moments-d113.md), [D115](dyadic-comparison-and-strategy-d115.md), [D138](dyadic-precision1600-bank-d138.md) | A uniquely specified bounded moment solution, certified finite approximations, rational-frame change and valid ratio chart | Exact zero from a finite zero-containing enclosure |
| [D140](dyadic-P1600-recognition-d140.md), [D141](P1600-proof-gap-d141.md) | Actual jet rank 45, independent recovery of the candidate lattice, and a conditional height exclusion | Equality of the actual and candidate kernels without the missing height or identity hypothesis |
| [D69](cm-frame-verification.md), [D70](cm-frame-marks.md), [D88](d88-cm-expansion-identification-review.md) | A smooth geometrically integral canonical degree-30 candidate, exact candidate divisors, and candidate jet rank 45 | That its positive jets, P32 or B3 are the prescribed Shimura objects |
| [D95](nelson-global-identification-d95.md) | The complete analytic kernel is the nonzero Shimizu tensor with the stated derivative conventions | Arithmetic positive CM coefficients, or a candidate-to-actual multiplication map |
| [D51](target-realization.md) | Original residual systems occur in the specified canonical genus-64 Jacobian | That a candidate cover is that canonical curve |
| [D134](arithmetic-twist-classification-d134.md) | Conditional uniqueness of the arithmetic double cover after marked-base and canonical-Hecke identification | The marked-base identification that is one of its premises |

The graph and group are different kinds of input. The exact arithmetic
action, with the uniformization theorem, specifies the actual analytic
curve. Its finite abstract graph alone does not give the analytic
gluing or the canonical multiplication map. No comparison of a candidate
uniformization with that exact action is present in the inspected packet.

Similarly, D106's `Aut(C_bar,D)=1` says that **if** a D-marked
isomorphism between two given curves exists, it is unique. The set of
such isomorphisms may be empty. Its use to descend an already supplied
geometric marked isomorphism does not create one for the candidate.
This is the distinction between uniqueness of a comparison and its
existence; no new automorphism computation is needed.

The two candidate point counts at 31 are exact candidate facts. They
are not the full Hecke interpretation. An identification of linear
Hecke modules likewise supplies no multiplicative compatibility with
the canonical ring. None of these implications is supplied by the
saved correspondence reports, so D51/D134 cannot be used backwards
to identify the base.

## 2. The exact comparison that would suffice is already small

Write E for the actual sixteen-dimensional rational residue frame and
K_act for its quadratic relation space. The established dimensions are

    dim Sym^2(E)=136,   dim H^0(2K_C)=45,   dim K_act=91.

D140's invertible minor proves that the actual three-coefficient
restriction has rank 45. Therefore its exact kernel is K_act.
To finish this route, the saved 91-dimensional candidate space V must
be shown to lie in that exact kernel. Its inclusion only modulo the
saved error ideals is the current result. Rank equality alone cannot
replace inclusion.

There is also the order-four criterion: a candidate quadric vanishing
to order four at the rationally defined degree-17 CM divisor has at
least 68 zeros as a section of 2K_C, whose degree is 60. Thus it is
zero. Either criterion, combined with D69's already certified scheme,
identifies (C,D17); P32/B3 remain separate.
The degree argument is the application of
[van Bommel--Costa--Poonen--Srinivasan, Lemma 4.1 and Corollary 4.2](https://arxiv.org/pdf/2506.14026).
Those statements take arithmetic expansions as input and do not
construct the missing comparison here. The rank refinement is D88's
linear-algebra argument, not a further assertion quoted from the paper.

A control makes the rank issue explicit. Put

    R0=[I_45 | 0],   RN=R0+2^N E_(0,45).

Both maps have rank 45 and agree modulo 2^N, but e_45 lies in ker R0
and not in ker RN. The latter instead contains e_45-2^N e_0. Sources
626/627 check this at N=83,147. These are linear maps, not asserted
counterexamples satisfying the actual curve's arithmetic conditions.
They isolate the invalid inference from rank and congruence alone.

## 3. The finite chart set does not give finitely many exact moments

Retain D113's 174 states, 348 child maps, bounded measures nu_e and
exact degree-zero masses. The moment equations are

    m_(e,n) = sum_(e -> f) sum_(k>=0) [X^k] phi_(e,f)(X)^n m_(f,k),
    phi(X)=(aX+b)/(cX+1)=b+delta X/(1+cX),
    a in pi O_K, b in O_K, c in pi O_K, v_pi(delta)=1.

For fixed masses these equations have a unique bounded solution, by
D113's contraction. A residual zero modulo pi^P certifies the solution
only modulo that ideal. It does not assert that the omitted terms
are exactly zero. This agrees with
[Franc--Masdeu, Introduction and section 6.2](https://arxiv.org/pdf/1201.0356),
which distinguishes recognized equations from proved equations. The
ramified-field contraction used here is D113's own argument.

Source 626 checks all 348 branch shapes from the saved centers and
their certified errors. Of these, **275** have both a slope certified
nonzero and a target distinct from the other child in that row. This
count is of those two properties together, not of all nonaffine maps.
One witness is state 0, child 0, target 5:

    v_pi(c)=2,   c error >=176,   v_pi(delta)=1.

For this branch, for every k>=1,

    [X^k]phi(X)=delta*(-c)^(k-1),   v_pi([X^k]phi)=2k-1.

It is never zero. Because the other child has a different target,
there is no second term in that same operator matrix entry. Thus any
ordinary polynomial degree cutoff omits genuine coefficients from the
degree-one equation on the full moment space. Additional constraints
on the actual measures could produce cancellations; this calculation
does not deny that possibility.

The independent source 627 uses the frozen field backend, rather than
626's rational polynomial convolution. It reconstructs the first twelve
Taylor coefficients by `(1+cX)phi=b+aX` and checks the same valuations.
The assertion for every k follows from the displayed exact formula.
The scalar control x=1+2x has exact dyadic solution -1; its N-term
iterate 2^N-1 has residual -2^N. It provides a simple nonzero residual
at arbitrarily high finite precision, without any curve claim.

## 4. A pole-orbit obstruction to finite branchwise rational closure

One might replace polynomial moments by finitely many rational test
functions that are exactly closed under each child pullback. The
following argument excludes that proposal when it must include a
CM evaluation kernel.

Suppose finite-dimensional spaces W_e of rational functions over a
common coefficient field extending K satisfy

    f in W_e => f composed with phi_(e,fchild) in W_fchild

for every individual branch. Assume one W_e contains a rational
function with a pole outside P1(K). This includes the CM Poisson
kernel: beta^2=-(2+pi) has odd K-valuation, so beta is not in K.
The kernel `2K_j(t)=1-((beta+t)/(beta-t))^(2j+2)` has a pole at beta.
The saved K-rational CM chart changes preserve the property of a pole
being outside P1(K).

Follow any directed path from that state until a state repeats.
A non-K pole remains non-K under all the Mobius changes. A cycle
of length l composes to

    psi(X)=(AX+B)/(CX+1),
    A,C in pi O_K, B in O_K, v_pi(A-BC)=l>0.                (1)

Indeed under composition the new denominator constant is 1+cB, a
unit, and determinant valuations add. The other integrality claims
follow directly by multiplying the normalized matrices.

The characteristic polynomial of this cycle matrix has unit trace
1+A and determinant of valuation l. Modulo pi it is X(X-1), with
two simple roots, including in residue characteristic two. Hensel
lifting gives eigenvalues in K of valuations 0 and l. They are
distinct, and their ratio is not a root of unity. Consequently psi
is conjugate over K to a nontrivial dilation with multiplier of
nonzero valuation. Its only periodic geometric points are its two
K-rational fixed points.

Let p be a non-K pole of the transported function at this cycle.
The repeated pullbacks have poles at psi^(-n)(p), all distinct.
But every finite-dimensional space of rational functions has a
finite common pole set: take the union of the poles of a basis.
This is a contradiction. It proves the stated branchwise obstruction.

The saved W-anchor A chart starts at state 14. Source 626 exhibits
the reachable path and cycle

    14 -> 12 -> 9 -> 3,       3 -> 1 -> 5 -> 10 -> 3.

Each arrow is the saved child 0; the cycle has determinant valuation
four. Source 627 verifies every arrow and independently follows the
other-child graph to another cycle. It also checks the control
phi(x)=2x and k(x)=1/(x^2-2): the squared poles of the nth pullback
are 2/4^n, all distinct and of odd valuation. Without contraction,
phi(x)=-x preserves k, showing why the strict hypothesis matters.

This proof concerns closure under **individual** branches. It does
not rule out cancellation after summing branches, finite descriptions
by functional equations, nonrational function classes, quotients of
test-function spaces, or a separate geometric correspondence. It
does not prove that exact identification is impossible.

## 5. A sufficient exact identity that allows summed cancellation

Here is a concrete alternative interface. It is a derived sufficient
criterion, not an identity already supplied by the certificates.

Let V be the direct sum over the 174 charts of rational functions
with no poles on their integration domains O_K. They are continuous
and bounded there. Define the summed pullback operator by

    (A f)_j(X) = sum_(e -> j) f_e(phi_(e,j)(X)).

For any of the sixteen harmonic measures define

    Lambda_a(f)=sum_e integral f_e dnu_e^a.

The exact partition/invariance equations imply
`Lambda_a(Af)=Lambda_a(f)`. Finite sums and bounded integration justify
the equality. Hence a **finite exact rational-function identity**

    F = B + H - A H,                                        (2)

where each B_e is constant, proves

    Lambda_a(F)=sum_e B_e m_(e,0)^a.

Every quantity on the right is exact harmonic data. In particular a
zero right side proves the integral is zero, without increasing a
moment cutoff. This uses a finite witness H, not a claim that V or
the orbit of H is finite-dimensional and invariant.

Products have a corresponding sufficient test. On d-fold tensors
use the product measure functional Lambda_(a1,...,ad), and replace
A by A tensor ... tensor A. Then an identity

    F = B + (1-A^tensor_d)H                                 (3)

evaluates F as the finite sum of the constants B times products of
the known zeroth masses. Bounded product integration proves (3) in
the same way. No division by a candidate-derived integral occurs.

Actual finite CM jets are Poisson integrals of rational kernels.
The actual residue-frame conversion is a rational expression in
their order-zero evaluations and the exact residue coordinates.
After clearing its already proved nonzero denominators, a candidate
quadric residual through any fixed jet order is therefore a polynomial
in finitely many such integrals. Its homogeneous pieces can be
represented by tensor test functions of the type above.

To make this into identification, one must explicitly build that
cleared residual in the **actual** frame, supply the finite identities
and zero mass evaluations for a spanning set of candidate quadrics,
and retain the rank-45 or order-four argument of section 2. Neither
the tensor degree nor the size of a useful H is claimed small.
No witness H for a candidate residual is present or constructed in
D150. No existence or effective finite-search theorem for such H
is proved. A numerical residual of (2) or (3) is insufficient.

## 6. Decision and next work

The requested structural inventory is complete for the named saved
packets. There is no overlooked candidate identification in them.
The missing comparison is now isolated from the already completed
candidate geometry, arithmetic frame, actual rank, and abstract
automorphic correspondence.

Do not rerun candidate smoothness, point counts or ordinary moment
truncations as an exactness repair. Do not infer rigidity from a
trivial marked automorphism group. The new pole argument closes the
specified branchwise rational-closure proposal only.

The next bounded theoretical task is to test whether the **summed**
transfer relations and actual quaternionic symmetries supply an exact
identity of the type (2)/(3) for a cleared positive-order residual,
or an equivalent multiplication-compatible geometric comparison.
Begin with a concrete residual and a finite exact witness; do not
label an unbounded search as an executable certificate. A height
alternative still needs new actual-curve input beyond D149's closed
scalar repairs. No user decision is pending for this bounded work.

P1600 and column 0/P6400 are unchanged. No new spectrum, geodesic
census, level, Hecke calculation, cubic search or precision bank is
admitted. D134's later markings and canonical-Hecke hypotheses, the
global cubic/section construction and original-kernel torsion tasks
remain separate.

## 7. Reproducibility and limits of the finite checks

Sources 626 and 627 pass in approximately 0.35 and 0.29 seconds.
Both use standard Python; neither invokes Sage, Magma, a production
coordinator or a moment worker. Source 628 binds this report, the
source applicability ledger, the finite controls, the inherited
D149 completion and its full transitive provenance. Its review,
replay and completion receipts record the final timings and counts.

The [fixed review](../data/computed/structural_identification_review_d150.json),
[source ledger](../data/computed/structural_identification_sources_d150.json)
and [completion record](../data/computed/structural_identification_completion_d150.json)
separate finite verification from the companion pole-orbit and
functional-identity proofs. The review does not mechanically prove
those arguments or the inherited geometric theorems.

Every job uses `run_dyadic_capped.py`, its 180-second private-process-group
cap and the unchanged maximum three mathematical workers, 2 GiB per
worker/store and 6 GiB aggregate. D150 runs its jobs sequentially.
All owned jobs have bounded receipts. A system-wide process listing
was unavailable in the workspace sandbox, so no global absence of
unrelated processes is claimed. Preserve frozen sources 626--628
and all passing artifacts after completion; source 629 is next unused.
