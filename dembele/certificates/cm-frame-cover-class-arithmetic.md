# A verified third of the cubic branch class

Date: 2026-09-21. Decision D78. Continues
[the normalized B3 fibre](cm-frame-B3-fiber.md).

**Result:** on the genus-40 candidate X modulo 31, we now have an
explicit divisor-class representation A satisfying

\[
3[A]=-[D_+-D_-]\quad\text{in }J_X(\mathbf F_{31}).
\]

The class is fixed by Frobenius and negated by the double-cover
involution. A verifier checks the saved relation without using the
suggested Jacobian order or repeating the scalar search. Adding the
nonzero branch difference to the proposed third is correctly rejected.
The difference Delta=D+-D- is nonzero and is not killed by three.

This removes the required class-division obstruction at 31 for this
candidate. It does **not** construct the Kummer function h, the cyclic
cubic, its genus-64 reflection quotient, or a characteristic-zero
third. The arithmetic Shimura identification remains open. In particular,
no uniqueness or match to the prescribed Fuchsian monodromy is claimed.

## 1. Exact arithmetic input on the cover

Write H=div_C(X16), a canonical divisor of degree 30, and choose

\[
D_0=2\pi^*H,\qquad \deg D_0=120>2g(X)+1.
\]

The choice is larger than the minimum degree 81 but makes its sections
accessible directly from the existing canonical equations. Put
div_C(ell)=B3+U, with deg U=21, and use D76's denominator half E_Q,
of degree 18. Script [164](../magma/164_cm_frame_cover_sections.m)
constructs the following basis of L(D0):

* 45 invariant sections q2/X16^2, where q2 ranges over the canonical
  quadratic coordinate space;
* 36 anti-invariant sections w*q3/(ell*X16^2), where q3 is a canonical
  cubic vanishing on E_Q+U.

The second formula equals W*(q3/X16^3), where W=w/(ell/X16) is D77's
regular coordinate at B3. The divisor of w on X is the ramification
divisor over B2 plus pi^*(B3-E_Q). Thus these vanishing conditions give
the claimed pole bound D0. The odd cubic space has dimension
90-39+1-16=36 by Riemann–Roch. The even and odd spaces are independent
under the involution and together have the full dimension 81.

The same script enumerates 2,048 distinct usable points over F31^2,
on the chart X16=1 away from ell*n*d=0. This is a set of evaluation
points, **not a count of every point on X**. Forty of the usable points
are rational over F31. The field is represented by

\[
\mathbf F_{31}[b]/(b^2+29b+3).
\]

All point coordinates, Frobenius and deck permutations, polynomial
bases and branch evaluations are retained in
[cm_frame_cover_sections.json](../data/computed/cm_frame_cover_sections.json),
with [Magma data](../data/computed/cm_frame_cover_sections.m).
Collector [165](../pari/165_cm_frame_cover_section_data.py) binds them
to the constructor and its log.

Script [166](../magma/166_cm_frame_cover_makdisi.m) selects 640 points,
closed under both actions. Since 640>5*120, evaluation is injective
on L(5D0), hence on every function space used below. Products of saved
sections give the full spaces:

| Space | Degree | Verified dimension |
|---|---:|---:|
| L(D0) | 120 | 81 |
| L(2D0) | 240 | 201 |
| L(3D0) | 360 | 321 |

Every product belongs to the stated space. Its computed rank equals
the Riemann–Roch dimension, proving completeness. Product indices are
saved, so checking does not repeat basis selection.

Choose a common effective divisor B of degree 111 from other points,
disjoint from the 640 evaluation points and stable under Frobenius.
The branch constraints, computed in the nonic algebra using W rather
than w, give 81-dimensional spaces

\[
W_\pm=L(2D_0-B-D_\pm).
\]

Each combines 111 conditions at B and nine at its oriented branch.
The constraint matrix has rank 120. These spaces represent the classes
[B+D+-D0] and [B+D--D0]; their difference is Delta. The branch points
have degree three and are disjoint from the chosen degree-one/two
auxiliary points.

The evaluations, product indices, kernels and actions are in
[cm_frame_cover_makdisi.json](../data/computed/cm_frame_cover_makdisi.json),
with [Magma](../data/computed/cm_frame_cover_makdisi.m) and
[GP](../data/computed/cm_frame_cover_makdisi.gp) exports. Collector
[167](../pari/167_cm_frame_cover_makdisi_data.py) constructs these exports.
Field elements are encoded in JSON/Magma arrays as c0+31*c1; GP uses
the polynomial c0+c1*t required by the pinned C interface.

## 2. Verification and divisor operations

Verifier [168](../magma/168_cm_frame_cover_makdisi_check.m) independently
checks the pole conditions, the selected points against all 91 curve
quadrics and the cover equation, all evaluations, products, ranks,
permutations and both branch kernels. It performs no point search or
kernel solve. Changing one odd-section evaluation is rejected.

The divisor arithmetic uses Khuri-Makdisi's evaluation representation
and section multiplication/division. See
[Khuri-Makdisi, Representation B and §§2–3](https://arxiv.org/pdf/math/0409209).
The operation schedule follows the pinned
[LiftTors pic.c](../vendor/LiftTors/pic.c): represent an effective
degree-120 divisor E by W_E=L(2D0-E), take complementary divisors for
negation, and use the chord operation for the negative of a sum.
Our local [Magma implementation](../magma/170_cm_frame_cover_class_arithmetic.m)
uses finite-field matrices; it does not change the upstream backend.

For clarity, the correctness checks are stronger than a random sample
of equations. Each product is a subspace of a known space of dimension
201 and must attain that rank. Each quotient contains the desired
space of dimension 81 and is intersected with constraints until its
dimension is exactly 81. Riemann–Roch supplies these dimensions, and
the relevant degree-120 line bundles are base-point free. Thus random
choices affect runtime, not acceptance of an incorrect space.
Each search has a fixed limit of sixteen trials.

For example the chord on W_E,W_F first constructs L(4D0-E-F), then
divides by L(D0) inside L(3D0) to get L(3D0-E-F). A nonzero section s
has divisor E+F+G-3D0. Dividing s*L(2D0) by that intermediate space
inside L(2D0) gives W_G. Hence [G-D0]=-[E-D0]-[F-D0]. All products
have pole bound at most 5D0, where evaluation is injective.

Equality and zero tests concern degree-zero line bundles, with section
dimension at most one. If a candidate one-dimensional kernel remains,
the code checks its inclusion against **every** section generator.
No probable equality is accepted.

Pilot [171](../magma/171_cm_frame_cover_class_check.m) constructs Delta,
checks that it is nonzero, fixed by Frobenius and negated by the deck
involution, and verifies Delta+(-Delta)=0. It also proves 3*Delta is
nonzero. The saved class is an actual Jacobian representation on this
cover, not an abstract group label.

## 3. Finding a third and checking it without an order assumption

The saved Hecke polynomials suggest a Prym order

```text
N = 751200095370944434080214902187185651 = 9*m,
m = 83466677263438270453357211354131739.
```

This is only a search aid: it is not a certified order of this
candidate's Prym. The full predicted genus-40 Jacobian order has
3-adic valuation six, while the quotient by the genus-16 prediction
has valuation two. We therefore do not invert three modulo either
predicted order.

Runner [172](../pari/172_cm_frame_cover_third.py) instead proposes

```text
c = 55644451508958846968904807569421159,    3*c+1 = 2*m.
```

Script [173](../magma/173_cm_frame_cover_third.m) computes A=c*Delta
using 154 checked negation/chord steps, then tests the actual class
3*A+Delta. **It is zero.** The proposed order is not used as a
zero-test or an annihilation assumption. The resulting third is also
checked to be fixed by Frobenius and negated by the involution.
Together with the checked scalar chain, the relation certifies
(2*m)*Delta=0 for this particular class. It does not certify a
Jacobian or Prym order.
Its 81-by-640 section matrix is `candidate_rows` in
[cm_frame_cover_third.json](../data/computed/cm_frame_cover_third.json).

Verifier [175](../magma/175_cm_frame_cover_third_check.m) uses another
random seed, reconstructs Delta from W+ and W-, and verifies
3*A=-Delta from the saved candidate. It does not load the proposed
order or addition chain. The zero relation includes a nonzero section
witness with its entire 81-dimensional product space contained in the
computed residual space. Replacing A by A+Delta fails the relation;
the earlier check 3*Delta!=0 explains why this is a genuine wrong class.

The matrices are over F31^2. Frobenius fixes the **class**, so it is a
point of J_X(F31); the particular effective divisor used to represent
it need not itself be Frobenius fixed. Recovering a function over F31
must address this representative/descent issue. There is no uniqueness
claim: other thirds can differ by rational three-torsion.

## 4. Resource bounds and reproduction

| Job | Whole wall time | Bound |
|---|---:|---|
| Sections and 2,048 points, 164 | 154.552 s | 180 s / 2 GB |
| Evaluation model, 166 | 3.904 s | 180 s / 2 GB |
| Original independent model check, 168 | 2.988 s | 180 s / 2 GB |
| Corrupted evaluation | 2.088 s | 180 s / 2 GB |
| Actual class pilot, 171 | 2.744 s | 180 s / 2 GB |
| Scalar search and relation, 173 | 47.897 s | 180 s / 2 GB |
| Final saved-third check, 175 | 2.825 s | 180 s / 2 GB |
| Final wrong-class control | 2.514 s | 180 s / 2 GB |

Two unsuccessful jobs are retained. The first section constructor
reached a Magma matrix-constructor API error after 73.546 s; correcting
the vector-row call gives the successful job above. The initial pinned
LiftTors probe [169](../pari/169_cm_frame_cover_class.gp) validates both
branch representatives and their inequality in 56.494 s, then hits its
180 s bound before finishing the class checks. Its PARI stack cap is
2 GB. The finite-field Magma implementation replaces that bottleneck;
the timeout is not repeated with a larger limit.

```sh
# Check all linked sources and artifacts:
python3 dembele/pari/174_cm_frame_cover_check.py --collect-only
# Repeat model and saved-third checks, with both corruption controls:
python3 dembele/pari/174_cm_frame_cover_check.py
# Rebuild sections, matrices and scalar search before checking:
python3 dembele/pari/174_cm_frame_cover_check.py --rebuild
```

Runner [174](../pari/174_cm_frame_cover_check.py) collects the result in
[cm_frame_cover_check.json](../data/computed/cm_frame_cover_check.json).
Routine section rechecks use separate filenames to preserve the
discovery chain's hashes. No full backend regression, remote job,
external edit, message, commit or cleanup was performed.

Final maintenance checks validate 323 distinct source/artifact hashes
across 104 linked JSON documents, 213 local Markdown links, Python
syntax and whitespace. D76 and D77 collection checks still pass.

## 5. Next step toward the cubic equation

**D79 follow-up:** [the cubic-cover report](cm-frame-cubic-cover.md)
completes the following finite-field function, representative descent
and reflection quotient. Its normalization has genus 64. The D78
artifacts and certificates remain unchanged.

Write the saved class as A=[E-D0]. Recover a function with

\[
\operatorname{div}(h)=D_+-D_-+3E-3D_0.
\]

This requires an actual principal-divisor witness and a representative
over F31, or an explicit constant-field descent. A zero-class witness
for an intermediate reduced divisor is not by itself this h: the
complementary-divisor transformations must be accounted for.

Then form v^3=h, enforce the involution and scalar compatibility, and
construct the reflection quotient. Those steps must precede a lift
and arithmetic recognition of the cubic cover. The saved Fuchsian S3
monodromy must still select the intended arithmetic extension; a
branch support and a third in one reduction do not identify it.
The genus-64 carrier, its target two-torsion and the final nonsolvable
field polynomial remain unconstructed.
