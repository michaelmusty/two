# A rational double cover from the B3 normalization

Date: 2026-09-18. Decision D76. Continues
[D75's auxiliary-divisor change](cm-frame-joint-field-and-B3-normalization.md).

**Follow-up:** [D77](cm-frame-B3-fiber.md) computes the normalized B3
fibre as K(sqrt(-3)), supplies the oriented cubic branch divisors, and
uses the cubic inertia condition to constrain scalar twists. The
status statements below describe the D76 checkpoint.

**Result:** on the certified genus-16 candidate C, we now have an exact
equation over Q

\[
X_{\mathbf Q}:\quad w^2=n/d,
\qquad H(n)=583,\quad H(d)=2935433.
\]

Here n and d are integral quadrics in the existing sixteen canonical
coordinates, and H is their maximum absolute coefficient. The smooth
normalization is geometrically connected of genus 40. Its odd branch
divisor is exactly B2=D17+P32, of degree 18. An independently checked
square-factor identity matches this equation to the old lift modulo
31^128, including its scalar. Negating d preserves the exact divisor
data but is rejected by that identity.

The coefficient arrays and monomial ordering are in
[cm_frame_B3_rational_model.json](../data/computed/cm_frame_B3_rational_model.json);
[the Magma data](../data/computed/cm_frame_B3_rational_model.m) can be
loaded with [the canonical curve](../data/computed/cm_frame_curve_candidate.m).
The combined independent certificate is
[cm_frame_B3_rational_check.json](../data/computed/cm_frame_B3_rational_check.json).

This constructs a rational cover of our candidate curve. Independent
identification with the arithmetic Shimura curve and its sign cover,
including the correct global quadratic twist, remains open. The earlier
hyperellipticity conflict is not resolved. Neither the specified
genus-64 curve Y nor the target nonsolvable field is constructed here.

## 1. Lift the moving section space by multiplication

Write P=P32. The old half is L=O(E-7P), with deg E=16. D75 replaces
this by L=O(E_new-B3), with deg B3=9 and deg E_new=18. Its exact
numerator has

\[
\operatorname{div}(n)=B2+2B3+T,\qquad \deg T=24.
\]

Scripts [146](../pari/146_cm_frame_B3_moving_sections.py) and
[147](../magma/147_cm_frame_B3_product_space.m) reuse the saved old
supports at 64 and 128 digits. The 25 independent conditions for
E+B3 leave twenty sections in H0(2K-E-B3). Fixed free coordinates
lift D75's g, whose divisor is E+B3+G, deg G=35.

We avoid lifting the thirty-five points of G. Choose a second section
h in the same space which is nonzero at every point of G modulo 31.
The first saved basis section works. Then

\[
h q=g s,\qquad q,s\in H^0(2K),\qquad \operatorname{ord}_P(q)\ge7
\]

describes H0(2K-G-7P). Indeed, at G the section h is a unit, so the
identity forces q to vanish there; the converse follows by dividing
hq by g. The common E+B3 factors account for the other zeros of g.
The unit property persists over the finite local base.

The matrix has 90 unknowns and 112 conditions: 105 quartic coordinates
and seven jets. Its rank is 87, giving three sections q1,q2,q3.
Unit minors give exact solutions over Z/31^e. We then solve for all
six products using

\[
n_{\rm old}g^2d_{ij}=n d_{\rm old}q_iq_j\quad(1\le i\le j\le3).
\]

Multiplication on the left has rank 45 in 225 degree-eight coordinates.
The six denominator sections have rank **6**, even modulo 31. The
selected q also reproduces D75's selected equation modulo 31.
Every saved quantity at 128 digits reduces to its 64-digit counterpart.

Independent script [149](../magma/149_cm_frame_B3_lift_check.m) checks
all identities, the E/B3 conditions, the seven jets and the finite-field
unit condition. A denominator change by 31^127 fails the global identity.
Runner [148](../pari/148_cm_frame_B3_lift_check.py) records the results in
[cm_frame_B3_lift_check.json](../data/computed/cm_frame_B3_lift_check.json).

## 2. Recognize the space before choosing a point

Script [150](../pari/150_cm_frame_B3_space_recognition.py) recognizes
the whole six-dimensional span. In the 45-dimensional quadratic
coordinate ring, a six-column unit minor gives 39 membership conditions.
Allowing all 136 monomials and the 91 exact curve relations produces
a rank-136 lattice of index (31^64)^39. The index and every membership
congruence are checked exactly after reduction. Sage supplies the
[integer-matrix and LLL interface](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html);
the lattice construction is local to this project.

Only 64 digits are used to fit. Six independent rational quadrics,
each with six-digit coefficient height, survive all 128 digits.
There are 45 nonzero section images among the tested reduced rows;
six survive. A known rational six-space control also returns six
independent exact members and rejects a changed unused digit.

The arbitrary selected denominator still has **zero** surviving
rational reconstructions among its 44 projective coordinate ratios.
The successful step is therefore recognition of the space and a new
choice of square section within it. No failed earlier search is
reinterpreted as evidence against descent.

## 3. Recover the exact Veronese structure

Let y1,...,y6 denote the recognized rational sections. Magma script
[151](../magma/151_cm_frame_B3_exact_product_relations.m) computes all
21 products in H0(4K). They have rank 15 over Q, yielding six exact
quadratic relations with small coefficients. The point P maps to
(0:0:0:1:0:1) in these coordinates.

Script [152](../pari/152_cm_frame_B3_veronese.py) constructs an explicit
invertible rational change of the six coordinates. It finds the unique
cubic whose six first derivatives belong to the relation space, takes
its rank-three polar at this rational point, and obtains a rational
point on the quotient conic from a tangent two-jet. Splitting that
conic and solving two linear syzygies gives six forms F0,D0,E0,A0,B0,C0.
The following identities hold exactly on C:

\[
F0 A0=D0^2,\quad F0 B0=D0 E0,\quad F0 C0=E0^2,
\]
\[
D0 B0=E0 A0,\quad D0 C0=E0 B0,\quad A0 C0=B0^2.
\]

Their coefficient rows span the entire six-dimensional relation space,
and the coordinate transformation has rank six. These are the standard
equations of the second Veronese embedding; see the
[Magma linear-systems example](https://docs.magma-maths.org/AlgebraicGeometry/Schemes/introduction.html#linear-systems).
The cubic-polar/two-jet splitting above is our explicit local algorithm;
we do not invoke a general surface-parametrization routine or infer
exactness from the 31-adic fit.

The primitive integral representative of F0 is **d=9 F0**. Its maximum
absolute coefficient is 2935433. The full change of coordinates and
six rational forms are in
[cm_frame_B3_veronese.json](../data/computed/cm_frame_B3_veronese.json).

## 4. Why the divisor statement holds over Q

Scripts [153](../magma/153_cm_frame_B3_rational_cover.m) and
[155](../magma/155_cm_frame_B3_rational_check.m) turn the exact identities
into a divisor certificate, without the rational residual-ideal
calculation that timed out in D75.

Take the second small numerator r from D75's candidate list. It is
nonzero everywhere on T modulo 31. For each of the six rational forms
v above, an exact quadratic witness s_v satisfies

\[
r v=n s_v\quad\text{on }C.
\]

All coefficients are integral at 31. Thus every v vanishes on the
rational residual T. The prior good model and marked divisors give
a flat relative Cartier divisor T; its reduced special fibre and
disjointness certify these properties over Q as well. The underlying
facts are [relative Cartier divisors and subtraction](https://stacks.math.columbia.edu/tag/056P)
and [reduced special fibre over a DVR, Lemma 37.26.6](https://stacks.math.columbia.edu/tag/0574).
The actual membership and disjointness assertions are checked here.

At 31, the saturated common zero scheme of F0 and A0 is exactly T.
After removing T, their common zero locus is empty. Properness then
rules out a common generic-fibre zero: any such zero would specialize
to the closed fibre. The equality F0 A0=D0^2 therefore forces the
remaining zeros of F0 to have even multiplicity. Locally, wherever
F0/T vanishes, A0/T is a unit and their product is (D0/T)^2.

The saved special-fibre divisor E_Q is obtained from the common zeros
of F0,D0 after removing T. It is reduced of degree 18, disjoint from
T and B2+2B3. Its doubled ideal has degree 36, and the verifier checks
the full zero-scheme equality for d. Consequently

\[
\operatorname{div}(d)=T+2E_{\mathbf Q},\qquad
\operatorname{div}(n/d)=B2+2B3-2E_{\mathbf Q}
\]

over Q. In particular O(E_Q-B3) is a rational branch half on C.
The odd divisor B2 is nonempty, so n/d is not a geometric square.
The normalized double cover is connected and Riemann–Hurwitz gives

\[
2g(X)-2=2(2\cdot16-2)+18=78,\qquad g(X)=40.
\]

This is an equation for the function-field extension and its smooth
normalization; the displayed equation at its common zeros is not
asserted to be an already smooth projective embedding of X.

## 5. Preserve the recorded local twist

Script [154](../pari/154_cm_frame_B3_rational_model.py) expresses d in
the six saved product sections at 128 digits. The corresponding
symmetric three-by-three matrix is exactly rank one over Z/31^128:
S=lambda*v*v^t, with a unit diagonal anchor. Its scalar lambda is a
square modulo 31. No extra nonsquare multiplier is needed; the
recorded twist multiplier is **1**. Hensel lifting the scalar square
root supplies a section q_Q for which

\[
n_{\rm old}g^2d=n d_{\rm old}q_{\mathbf Q}^2
\quad\pmod{31^{128}}.
\]

Thus w_Q=w_old*g/q_Q gives the saved square-factor isomorphism at the
stated precision. Script 155 checks this degree-eight identity
independently after checking the exact rational relations and witnesses.
Its negative control changes d to -d and the recorded Veronese scale
to -9. All divisor and rational relation checks still pass; the local
square identity fails. This tests the scalar, not just the zeros.

Agreement at one completion does not choose the required global
arithmetic quadratic twist: rational factors which are squares at 31
can still produce different global twists. The arithmetic cover has
not been identified by this certificate.

## 6. Reproduction, bounds and next step

| Job | Whole wall time | Limit |
|---|---:|---|
| Moving section lifts, 146 | 6.781 s | 180 s, no Sage memory cap |
| Product transfer at 64 / 128 digits, 147 | 23.831 / 24.581 s | 180 s / 2 GB each |
| Independent lifted checks, 149 | 21.940 / 22.684 s | 180 s / 2 GB each |
| Highest-digit error control | 18.407 s | 180 s / 2 GB |
| Rational six-space recognition, 150 | 26.510 s | 300 s, no Sage memory cap |
| Exact product relations, 151 | 6.987 s | 180 s / 2 GB |
| Rational Veronese splitting, 152 | 3.365 s | 180 s, no Sage memory cap |
| Rational divisor construction, 153 | 30.183 s | 180 s / 2 GB |
| Equation and scalar export, 154 | 3.901 s | 180 s, no Sage memory cap |
| Independent rational certificate, 155 | 30.035 s | 180 s / 2 GB |
| Wrong-twist control | 29.883 s | 180 s / 2 GB |

```sh
python3 dembele/pari/148_cm_frame_B3_lift_check.py --collect-only
python3 dembele/pari/148_cm_frame_B3_lift_check.py
python3 dembele/pari/148_cm_frame_B3_lift_check.py --rebuild
python3 dembele/pari/156_cm_frame_B3_rational_check.py --collect-only
python3 dembele/pari/156_cm_frame_B3_rational_check.py
python3 dembele/pari/156_cm_frame_B3_rational_check.py --reconstruct
```

Runner 156's reconstruction mode repeats 150–154 against the saved
lift, then checks independently. Rebuilding the lift first uses 148.
The source/log hashes and explicit limits are retained throughout.
Earlier arithmetic data, including the unsuccessful searches and
archived timeout probes, remain unchanged.

Final collection checks revalidated 257 transitively hashed files in
the rational-cover certificate, plus the saved D74/D75 collectors.
The six new Python scripts parse, all 178 local Markdown links in the
updated documents resolve, and `git diff --check` passes. These targeted
certificates do not rerun the unrelated backend suite.

**Next:** compute the normalized unramified fibre of X_Q above B3,
including its degree-18 étale algebra and the double-cover involution.
Since n/d has order two at B3, ordinary substitution w=0 would give
the singular equation's fibre; divide by a local parameter squared
and use its leading unit instead. This supplies the branch data for
the next cyclic cubic extension of X_Q. The intended S3 closure Z
has genus 136 and its reflection quotient Y has genus 64, as specified
by [the arithmetic local-monodromy computation](genus64-cover.md).

That branch data will not by itself select the required cubic cover.
The arithmetic monodromy and global twist must be matched, alongside
the outstanding identification of C and its marked divisors. No extra
31-adic precision or return to the old coefficient searches is needed
as the default next action. Backend optimization remains paused.
