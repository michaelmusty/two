# D130: from an identified base to the original-kernel polynomial

Date: 2026-09-28. Companion to the
[target feasibility report](dyadic-target-feasibility-d130.md).

The next intermediate theorem is an arithmetic identification of (C,D17)
by the integral-section argument. This document specifies what that
theorem would and would not provide. It does not claim that all subsequent
steps have executable algorithms or a complete cost estimate.

## 1. Input theorem and the marked double cover

Inputs: the actual canonical differentials and independent CM frame;
successive exact vanishing at orders 1,2,3; the exact candidate quadrics.
Order 0 is already exact. The degree comparison 4*17=68>deg(2K_C)=60
then gives the [D88 base-identification criterion](d88-cm-expansion-identification-review.md).
The higher-order height bounds require the preceding exact zeros. A ball
containing zero below threshold is not a substitute.

Required next output: an F-isomorphism of the **marked arithmetic map**
X->C, preserving the involution, P32, D17 and B3. The exact candidate is
z^2=n/d, with branch divisor D17+P32. The D17 frame identifies no additional
marking automatically. D87's 277 matching signs are sampled numerical
evidence for the geometric character, not its rigorous certification.

Proposed operations and acceptance tests:

* Obtain arithmetic evaluations at the canonical P32 and B3 CM points
  through independently labelled embeddings/uniformization. Match the
  candidate coordinates by exact identities or certified height bounds;
  prove the closed-point degrees and branch multiplicities. No certified
  evaluator for these markings has yet been supplied by the D17 bank.
* Certify the geometric double-cover character on generators, either by
  rigorous analytic continuation with nonvanishing enclosures along entire
  paths, or by an exact arithmetic torsor construction. Endpoint/sample
  agreement alone does not certify continuation. This construction remains
  to be implemented or replaced by an exact method.
* Remove the constant arithmetic twist by canonical arithmetic descent
  data, or by a proven finite twist classification together with canonical
  fibre/Frobenius information that separates every remaining class. Neither
  the classification nor those separating arithmetic inputs have yet been
  constructed. Agreement at the saved 31-adic place is insufficient.

These are specified mathematical tasks, not completed algorithms. Increasing
the present D17 moment precision addresses only the input base theorem.

## 2. An explicit twist invisible at the saved 31-adic place

Write F=Q(b), with

    f(b)=b^8-8b^6+20b^4-16b^2+2=0,
    delta=1+b.

Source 538's [exact witness](../data/computed/dyadic_target_audit_bridge_d130.json)
checks f(-1)=-1. Hence Norm(delta)=-1, so delta is an integral unit and
is not a square in F: the norm of a square is a square in Q.

At D88's chosen norm-31 place, b=27 modulo 31. Here f(27)=0 and
f'(27)=12 modulo 31; delta=28=20^2 modulo 31, with derivative
2*20=9 nonzero. Hensel lifting makes delta a square in that completion.
The discriminant of z^2-delta is 4*delta, a unit at every finite prime
away from 2. Thus F(sqrt(delta))/F is nontrivial globally, locally split
at the chosen 31-adic place, and unramified at finite primes away from 2.

Twisting z^2=u by delta therefore preserves its geometric double cover
and its local isomorphism at that place while changing its arithmetic
cover over a geometrically integral F-base. This is a counterexample to
using those tests alone to select the global twist. It does not show that
the current candidate has the wrong twist, or determine the effect on
the target mod-2 representation.

This distinction is the scalar trivialization in the Kummer description
of covers. [Stacks, Kummer theory, tag 03PK](https://stacks.math.columbia.edu/tag/03PK)
was checked for its invertible-n exact sequence and description by a line
bundle with a trivialized nth power. The particular unit, norm, residue
calculation and application here are our elementary deduction, not a
claim quoted from that reference. Infinite-place conditions, if added to
a future twist classification, must be checked separately.

## 3. From the same marked arithmetic X to Y64

Inputs: the preceding F-isomorphism of marked double covers, the canonical
Hecke interpretation, the D78/D79/D84 finite-field third census, and its
orientation and branch divisors.

Operation: apply the [D88 cubic identification proposition](d88-cubic-identification-shortcut-review.md).
The Prym order has 3-part nine. The nine saved thirds exhaust the rational
ambiguity, and the prescribed counts select the (0,0) special-fibre cover.
Unique lifting occurs on the **same fixed arithmetic X**, with the same
oriented branch data; it cannot identify lifts on different global twists.

Acceptance: prove every hypothesis of that proposition, including global
branch irreducibility/orientation and the arithmetic double-cover
identification. The proposition then identifies the canonical cubic lift.
It does not recover its normalized coefficients over F or bound their
heights. D86's failed recognition modulo 31^128 is a lower exclusion in
chosen bases, not an upper reconstruction bound. A further ordinary LLL
scan has no new justification.

Required arithmetic output: either exact global cubic coefficients and
their identity with that lift, or a compatible arithmetic section model.
Possible approaches are exact third-division/line-bundle computation on
the now-identified X, or reconstruction with a proved upper height bound
and exact verification. Neither effective target construction is currently
implemented. Local congruences alone do not provide it.

## 4. The section interface and combined torsion backend

Given the actual degree-three map pi:Y->C and arithmetic P32, put
D0=pi^*(43P32), of degree 129. The [D62 interface](arithmetic-section-interface.md)
requires at least 646 suitable Frobenius-stable evaluation points disjoint
from D0, compatible trivializations, and the following section dimensions:

| Space | Dimension |
|---|---:|
| L(D0) | 66 |
| L(2D0) | 195 |
| L(3D0) | 324 |
| L(4D0) | 453 |
| L(5D0) | 582 |

Operation: construct the initial evaluations from the actual arithmetic
curve/cover or an independently proved arithmetic section mechanism;
build product spaces and lift the same data to increasing prime powers.
Acceptance: correct ranks and multiplication, full rank on reduction,
Frobenius compatibility, arithmetic origin on the specified Y, and
compatible auxiliary evaluations. Two degree-65 auxiliary divisors need
130-dimensional L(2D0-E_i) spaces, or a verified separating alternative.
A graph, Hecke module or dimension count supplies none of these entries.

The [D66 genus-16/degree-51 control](lifttors-degree51.md) and
[D67 allocation audit](lifttors-allocation.md) are scaling evidence on
known curves. The combined genus-64/degree-51 backend has not run. Its
historical monolithic controls used a different timeout; they cannot be
copied into the present 180-second protocol. Split preparation, lifting,
group arithmetic and verification into independently resumable stages,
then run a clearly labelled combined control within the current limits
before target torsion. Such a control still would not supply actual Y.

## 5. Original target, scalars and the polynomial

[D120](construction-reassessment-d120.md) already settles the norm-97
Euler-cofactor separation and the selected rank-16 F2 target over residue
degree 51; this supersedes D100's older open isolation question. D51
places the original residual systems in the canonical Y Jacobian.

Once arithmetic sections exist, construct and lift a basis of this actual
target torsion. Verify 2-torsion, independence, Frobenius action and the
canonical target projector. Then implement the **global F256 scalar
action** on divisor classes, for example through the identified Hecke
endomorphism, and verify its action and defining polynomial on the target.
The present abstract Hecke action and one local Frobenius matrix are not
an implemented geometric scalar operation. An equivalent verified
arithmetic construction would also suffice; none is currently supplied.

Form the 257 F256 lines in a two-dimensional target space. Choose an
arithmetic invariant constant on each line and separating these lines;
verify both properties on the actual target, then form the orbit
polynomial. Its coefficients must be proved to lie in F and recovered
with a justified recognition bound or exact arithmetic construction.
Matching a few reductions or a desired Galois group does not certify
these coefficients or identify Dembélé's original kernel.

Finally establish the polynomial's action/kernel using the faithful
projective action of SL2(F256) in characteristic two and the identification
with the original residual representation. Relate the required conjugates
and normal closure over Q to the original two residual systems; verify
the resulting field and ramification claim. This last identification,
not a group-name coincidence, is the project's acceptance criterion.

The executable next packet remains the weighted representation control
in D130's feasibility report. The first missing *mathematical* bridge is
the marked arithmetic cover and its twist, followed by the actual Y
section mechanism. Neither is routine processing after exact C.
