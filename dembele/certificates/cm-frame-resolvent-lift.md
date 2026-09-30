# Exact 31-adic lifting of the branch square class

Date: 2026-09-18. Decision D72. This continues
[D71's double cover over F31](cm-frame-resolvent.md).

**Follow-up:** [D73's normalization experiment](cm-frame-normalization.md)
reduces the numerator height to 39 digits and certifies a denominator
transfer preserving the same ratio modulo 31^8. The details below
record the original D72 normalization and its height calibration.

**Result:** the equation and its divisor certificate now lift compatibly
through every modulus 31²,...,31⁸. The final modulus is
**852891037441**. An independent Magma calculation verifies

\[
\operatorname{div}(q_{\rm num}/q_{\rm den})
=D_{17}+15P_{32}-2E,
\qquad \deg E=16,
\]

on the smooth model over Z/31⁸. Thus `L=O(E-7P32)` remains a degree-nine
half of `B2=D17+P32`. This is an exact calculation in finite rings,
not a floating-point approximation. It does not yet reconstruct the
denominator, the square class, or the cover over a number field.

The chosen numerator is separately recovered **exactly over Q** and
agrees with all eight lifted digits. Its primitive integer coefficient
height has **631 decimal digits**. This measures a serious cost of the
current normalization and motivates reducing that normalization before
requesting much greater precision. It is not a height estimate for the
unknown denominator or for the target nonsolvable field polynomial.

## 1. Why there are eighteen branch points

The saved local S3 homomorphism specifies a cover of the genus-16 base C.
Taking its sign character produces the double cover. Its local data are:

| Marked points on C | Number of geometric points | Image in S3 | Image under sign | Branch in the double cover |
|---|---:|---|---|---|
| Order-two elliptic points | 17 | Transposition | -1 | Yes |
| Order-32 elliptic point | 1 | Transposition | -1 | Yes |
| Order-three elliptic points | 9 | 3-cycle | +1 | No |

Hence there are 17+1=18 geometric branch points. D17 packages seventeen
of them as a single degree-17 closed point. The restriction to three
branch values belongs to Belyi maps to the projective line; this
auxiliary double cover has a genus-16 base. Its Riemann–Hurwitz check is
`2g(S)-2=2(2*16-2)+18`, giving genus 40.
See [the saved cover specification](genus64-cover.md), §2–3. These local
monodromy data are exact for that specified arithmetic group. Matching
the algebraic candidate and its markings with the Shimura objects
remains a separate identification problem.

## 2. Finite étale supports and integral local coordinates

Script [`123_cm_frame_lift_supports.m`](../magma/123_cm_frame_lift_supports.m)
rechecks D71's divisor identity and exports exact support algebras for
D17, E, and the common residual divisor T of q_num and q_den.
The code calls this last divisor `F`; it is unrelated to the base
number field F. All three supports avoid X16=0, are reduced, and have
X15/X16 as a separating coordinate. Lexicographic ideal equalities
certify their univariate presentations, rather than only testing a
polynomial at sampled points. Their residue-field factor degrees are:

- D17: `[17]`;
- E: `[2,2,2,10]`;
- T: `[1,1,3,23]`.

For each irreducible factor f, lift its coefficients to 0,...,30 and
work in `A_n=(Z/31^n)[a]/f(a)`. The monic polynomial and its unit
derivative make A_n finite étale and free of the recorded degree.
The point coordinates, tangent vectors and supporting jets are stored
as coefficient lists in these algebras.

The projection X15/X16 is unramified at every support point: the
Jacobian with respect to X1,...,X14 on X16=1 has rank 14 in each
residue field. Fixed unit minors let us lift the curve coordinates
and use X15 as a local parameter. All 91 original quadrics are
checked after each solve, not just the fourteen selected equations.
Sage provides the exact
[polynomial quotient-ring arithmetic](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_quotient_ring.html);
the Newton steps and their residual checks are implemented locally.

## 3. The lift as three linear corrections

There are 45 independent canonical quadric sections modulo the 91
curve equations. A unit minor chooses a fixed integral section chart.
For a step from modulus m=31^(n-1) to 31m, all corrections are m times
residue-field coefficients, and quadratic correction terms vanish.

First lift D17 using its exact rational ideal and lift the order-16
formal coordinates at the exact rational point P32. Correct q_num to
vanish on D17 and to order 15 at P32. These impose **32 independent
conditions on 45 coefficients**. The thirteen remaining coordinates
are held fixed. The simple residual zeros T of the corrected numerator
then lift by the implicit-function calculation.

Next temporarily lift E along C while holding its local parameter
fixed. Correct q_den to vanish on both T and this temporary lift of E.
These impose **44 independent conditions on 45 coefficients**; the
remaining coordinate fixes scale. Because q_den has a double zero
at each point of E modulo 31, moving E has no first-order effect on
this value condition.

Finally enforce double vanishing. Write locally at a temporary point
of E

\[
q_{\rm den}=0+b\,t+c\,t^2+\cdots,
\qquad b\equiv0\pmod m,\quad c\not\equiv0\pmod{31}.
\]

Moving the parameter by `m*delta`, with
`delta=-(b/m)/(2c)` in the residue field, kills the derivative modulo
31m. The value remains zero. The factor 2c is a unit at every support
point. This gives the corrected E and the required half relation.
The invertibility of two is consistent with
[étaleness of doubling on the Jacobian](https://stacks.math.columbia.edu/tag/0BFH),
but the actual computation uses the displayed local equations rather
than a general Jacobian or function-field reduction routine.

Script [`124_cm_frame_resolvent_lift.py`](../pari/124_cm_frame_resolvent_lift.py)
implements these steps for each digit. It verifies all curve equations,
branch and residual value conditions, double-zero derivatives, and
the unit leading coefficients. All stages retain ranks 32 and 44.
The runner checks reduction compatibility of the quadrics, support
coordinates, tangents and P32 jets between successive digits.
No guessed Jacobian order is used in the lift.

## 4. Independent certificate over the finite base ring

Script [`125_cm_frame_resolvent_lift_check.m`](../magma/125_cm_frame_resolvent_lift_check.m)
reads only the original curve/marking data and the exported lifted
equations, coordinates and jets. It does not repeat Sage's solves.
It verifies irreducibility and separability of each residue polynomial,
the local Jacobian ranks, all 91 equations, and the following orders:

| Support | q_num | q_den | Degree |
|---|---:|---:|---:|
| D17 | 1 | 0 | 17 |
| P32 | 15 | 0 | 1 |
| T | 1 | 1 | 28 |
| E | 0 | 2 | 16 |

At E, values and first derivatives vanish over Z/31⁸, and the
second-order coefficient is nonzero modulo 31. At P32 all coefficients
below degree 15 vanish over Z/31⁸ and the degree-15 coefficient is a
unit. All indicated order-zero values and order-one derivatives are
units. The support reductions are disjoint.

These local checks prove a global divisor equality over the finite
base ring. The étale support coordinates give finite flat Cartier
divisors; the jet with parameter derivative one gives the corresponding
double divisor at E. Their specializations agree with the already
certified D71 supports. The quadric sections are regular and nonzero
on the integral special fiber, so their zero divisors are finite flat
of degree 60. The inclusions checked above exhaust these degrees:
`17+15+28=60` and `2*16+28=60`. A closed inclusion between the resulting
finite free schemes of equal rank is an equality. Thus there is no
unchecked extra zero divisor elsewhere on C.

The verifier passes at 31⁸ in **2.351 s**. A negative control adds
31⁷ to the numerator's X1² coefficient. This preserves all seven
lower digits, but the verifier rejects its D17 value in **0.351 s**.
Checking only reduction modulo 31 would miss that error.

## 5. An exact numerator and a measured normalization problem

The numerator's branch conditions and its thirteen fixed coordinates
are rational. Script
[`126_cm_frame_lift_numerator.py`](../pari/126_cm_frame_lift_numerator.py)
therefore constructs the 32-by-32 system over Q directly. Evaluation
at D17 uses the existing degree-17 number field and exact projective
coordinates; the fifteen P32 conditions use exact rational implicit
jets. All 91 quadrics vanish in both calculations.

Solving this system over Q recovers q_num, independently of the
31-adic corrections, and verifies agreement modulo 31⁸. This takes
**4.622 s** inside Sage, **7.643 s** including startup. The rational
coefficients and a primitive integral representative are saved in
[`cm_frame_lift_numerator.json`](../data/computed/cm_frame_lift_numerator.json).
The largest primitive integer coefficient has 631 decimal digits
(2,096 bits). The affine coefficient bounds have 631 numerator digits
and 629 denominator digits.

For these known affine coefficients, the uniform uniqueness condition
`31^n > 2*U*V`, with U and V the actual maximum numerator and denominator,
holds at **n=845**. Indeed two bounded fractions with the same residue
have a cross-difference divisible by 31^n and of absolute value at most
2UV, so must coincide. This is a sufficient bound with known bounds,
not a minimal precision claim and not a prediction for the unknown
denominator. The exact numerator has already been recovered without
requiring 845 digits.

**Next:** use the exact 13-dimensional numerator space to seek a
smaller integral normalization, then transform numerator and denominator
together while checking that the square class is preserved. This
normalization experiment has not yet been implemented. After it, use
precision doubling for higher accuracy and seek arithmetic recognition
of the remaining extension data over F. Increasing precision blindly
in the current fixed-coordinate normalization is not the next default.

## 6. Files, reproduction and limits

The final data are
[`cm_frame_resolvent_lift.json`](../data/computed/cm_frame_resolvent_lift.json)
and [`cm_frame_resolvent_lift.m`](../data/computed/cm_frame_resolvent_lift.m).
The seven stage files `cm_frame_resolvent_lift_2.json` through
`cm_frame_resolvent_lift_8.json` retain every compatible intermediate
result. The certificate is
[`cm_frame_resolvent_lift_check.json`](../data/computed/cm_frame_resolvent_lift_check.json).
The support and solver job records are `cm_frame_resolvent_lift_jobs.json`;
the rational calibration has its own `cm_frame_lift_numerator_job.json`.

```sh
# Independent verification of the saved lift plus the corruption control:
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py --collect-only
# Reproduce support extraction and all seven lifting steps before verification:
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py --lift --digits 8
# Independent rational numerator calibration, with refreshed job hashes:
python3 dembele/pari/125_cm_frame_resolvent_lift_check.py --calibrate
```

Support extraction passes in **5.664 s** under 120 s/2 GB. The seven
lifting steps take **35.363 s** internally, **38.547 s** including Sage
startup, under a 240 s timeout. The Sage jobs did not impose a 2 GB
memory cap; that cap applies to the Magma jobs. Each positive job
requires a successful exit, the correct PASS marker and no error markers.
The negative control instead requires failure at the intended assertion.
Source and log hashes bind the computations and their inputs.

Eight digits and a rational numerator do not identify an arithmetic
denominator or a characteristic-zero double cover. The base curve's
Shimura identification, the prior hyperellipticity conflict, the saved
global sign monodromy, and the actual genus-64 cubic construction remain
open. Q descent of the cover is not assumed. No target torsion or
nonsolvable defining polynomial has been obtained.

D68–D71 inputs, numerical banks, backend code and external checkouts
are unchanged. D63's 111 tests remain the latest full backend suite;
the current exact lifting certificates are separate. All jobs finished.
Work is local and uncommitted, with no remote job, message or cleanup.
Final maintenance checks validate 78 source/artifact hashes across 30
JSON documents, 112 local Markdown links, syntax of all three new Python
scripts, and whitespace. Separate standard-library rational arithmetic
checks the primitive numerator, its 845-digit sufficient uniqueness bound,
and agreement with the lift modulo 31^8. Saved-certificate collection passes.
