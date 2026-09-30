# Exact marked divisors on the canonical genus-16 candidate

Date: 2026-09-18. Decision D70. This continues
[D69's curve verification](cm-frame-verification.md).

**Result:** the verified curve now has an explicit ordinary rational point
and disjoint closed points of degrees 17 and 9. The degree-nine residue
field has proved Galois group `9T15`, of order 72. These are algebraic
candidates for all the branch locations of the required degree-three
cover. Their CM labels, the Shimura identification of the curve, and the
cover itself remain unproved or unconstructed.

The curve equations and the two numerical differential banks are unchanged.
No target torsion or defining polynomial for Dembélé's nonsolvable field
has been computed. The degree-nine and degree-17 fields here are auxiliary
solvable fields.

## 1. What is exact, and what is a numerical identification

Write `C_candidate` for the smooth canonical genus-16 curve proved in
D69. The markings are saved in
[`cm_frame_marks.m`](../data/computed/cm_frame_marks.m), to be loaded after
[`cm_frame_curve_candidate.m`](../data/computed/cm_frame_curve_candidate.m).

| Mark on the candidate | Exact result | Proposed analytic label |
|---|---|---|
| `P32_candidate` | Rational point; ordinary over Q and modulo 31 | The unique order-32 CM point |
| `D17_candidate` | Reduced closed point of degree 17, with D68's residue field | The seventeen order-two CM points |
| `B3_candidate` | Reduced closed point of degree 9, cut out by seven linear forms on the curve | The nine order-three CM points |

All three supports are pairwise disjoint. Their monic Gröbner models
are flat at 31 and have reduced, disjoint special fibers. The numerical
labels in the last column are not consequences of these scheme checks.

Set `B2 = D17 + P32`, of degree 18. The recorded arithmetic local
monodromy calls for ramification index 2 above B2 and index 3 above B3.
If a connected degree-three cover with precisely this ramification is
constructed, Riemann–Hurwitz gives

\[
2g(Y)-2=3(2\cdot16-2)+18+2\cdot9=126,
\qquad g(Y)=64.
\]

This only checks the predicted genus. Branch supports and local indices
do not choose the global cover. The existing homomorphism from all the
Fuchsian presentation generators to S3 must still be matched; see
[the cover specification](genus64-cover.md).

## 2. Rational point and ordinarity

One projective LLL run, at scale `10^20` and coordinate height cap
`10^20`, recovers a primitive integer vector of height
`3310032844768591087`. The earlier cap of `10^12` excluded this vector.
All 91 integer quadrics vanish exactly at the recovered point. Its
coordinates and the complete recognition record are in
[`cm_frame_marks.json`](../data/computed/cm_frame_marks.json).

The maximum absolute error in normalized coordinate ratios is
`3.725e-21` for the N=16384 bank and `2.887e-16` for N=12288. These are
comparisons with computed values, not rigorous analytic error bounds.

Ordinarity has a separate exact proof. Reduce the point modulo 31,
normalize X1 to 1, and use the variation of X16 as parameter t. The
affine Jacobian has rank 14. An invertible 14-by-14 minor gives formal
coordinates through degree 15 by the implicit-function recursion.
The script checks all 91 quadrics modulo t^16. The 16-by-16 matrix of
canonical coordinate coefficients has determinant **8 modulo 31**.
Consequently the canonical vanishing sequence is `0,1,...,15`; the
Weierstrass gaps are `1,2,...,16`.

The same Jacobian minor is a unit in the smooth model over Z_(31).
The formal recursion therefore lifts, and the nonzero determinant
proves ordinarity over Q as well. This proof uses jets of the candidate
curve. It is a legitimate ordinarity certificate for that curve, but
does not supply the independent Shimura-side jets sought in D69.
It does not by itself complete the marked descent identification.

## 3. The degree-nine divisor and its residue field

For each of the nine analytic order-three elliptic points, the
pulled-back canonical differentials have a common zero of order two.
Their leading coefficients give the coarse canonical point, up to a
common row scalar. Script 119 extracts that coefficient on two circles
using 24 Cauchy samples, for each of the existing N=16384 and N=12288
banks, and then applies D68's saved change of basis.

The nine rows have numerical rank nine. A single 16-by-34 integer
lattice at scale `10^12` finds seven independent integer linear forms,
with maximum coefficient 54 and saturated row lattice. The maximum
normalized residual is `8.486e-20` on the current bank and `1.963e-14`
on the previous bank, across the two extraction radii. All four
evaluation matrices are retained. This is numerical discovery.

Exact Magma computation then proves that the intersection of these
seven hyperplanes with `C_candidate` is reduced, irreducible, and of
degree nine. It has no point on X16=0, and elimination gives an
irreducible degree-nine polynomial for X15/X16. Its full rational
coefficients are retained in
[`cm_frame_nonic_polynomial.txt`](../data/computed/cm_frame_nonic_polynomial.txt)
and the verification JSON; they are large in this coordinate.

The polynomial has Galois group `9T15`. The script explicitly checks
an elementary abelian normal subgroup of order 9, a cyclic point
stabilizer of order 8, and generation of the group of order 72.
Thus the group is `(C3)^2 semidirect C8 = AGL(1,9)`. The subsequent
`GaloisProof` call succeeds; the handbook distinguishes this proof
step from the preliminary group calculation.
[Magma Galois group documentation](https://docs.magma-maths.org/GlobalFields/GaloisGroupsAndAutomorphisms/galois.html).

This is consistent with the CM setting, but the group alone does not
identify a particular class field. Dembélé gives class number 9 for
`F(sqrt(-3))` and nine order-three elliptic points in §5.1. No exact
identification of our residue field with that CM construction is
claimed. [Dembélé, §5.1](https://arxiv.org/pdf/1906.06772).

A separate default maximal-order computation on the large-coordinate
nonic polynomial timed out after 90 seconds under a 2 GB cap, before
printing a discriminant. Its script, empty log and failure record are
saved as `cm_frame_nonic_order_probe.{m,out,json}`. The subsequent
optimized-representation call was not reached. No ramification bound
was assumed, and neither a maximal order nor a small defining
polynomial was obtained. Do not repeat this unchanged call.

## 4. A useful failed branch-function ansatz

The equality of degrees might suggest `B2 ~ 2 B3`, permitting a
quadratic resolvent of the form `z^2 = u` with
`div(u) = B2 - 2 B3`. **This relation is false on the candidate.**

Here is an exact finite-field test, followed by specialization to Q.
On the smooth curve over F31, choose the first recovered linear form
ell, which vanishes at B3 and nowhere on B2. Its square has divisor

\[
\operatorname{div}(\ell^2)=2B_3+E,\qquad \deg(E)=42.
\]

The squared ideal of B3 has projective length 18. A saturated colon
ideal gives E; its intersection with the B2 ideal gives the disjoint
sum E+B2 of degree 60. This is the residual-divisor construction
described in the [Magma sheaf documentation](https://docs.magma-maths.org/AlgebraicGeometry/Sheaves/div_maps.html).

Multiplication by ell^2 identifies

\[
H^0(C,\mathcal O(2B_3-B_2))
\simeq H^0(C,\mathcal O(2K-E-B_2)).
\]

Every section of 2K is represented by a quadric: the homogeneous
coordinate ring has dimension 45 in degree two, equal to
`h0(2K)=60+1-16=45`. The saturated ideal of E+B2 also has quotient
Hilbert function 45 in degree two. Thus it imposes all 45 independent
conditions on H0(2K), and the space displayed above is zero.

The flat, reduced markings are relative Cartier divisors in D69's
proper smooth model over Z_(31). Upper semicontinuity gives
`h0_Q(2B3-B2) <= h0_F31(2B3-B2) = 0`.
[Stacks Project, Lemma 36.32.1](https://stacks.math.columbia.edu/tag/0BDN).
In particular B2 and 2B3 are not linearly equivalent, even after
extending the ground field. This excludes this specific square-root
recipe; it does not obstruct other quadratic resolvents or the
required cubic cover.

## 5. Remaining construction and identification

The immediate cover input is now explicit: C, P32, D17 and B3.
The next construction task is to recover the cover's algebraic
extension data while matching the saved S3 monodromy. A concrete
intermediate object is its quadratic resolvent, corresponding to the
sign character. It requires a square class with odd valuations exactly
at B2, or equivalently the appropriate degree-nine line bundle L with
`L^2 = O(B2)`, together with its branch section. The effective choice
`L = O(B3)` has just been excluded. The marked supports alone neither
select L nor construct the cyclic cubic extension above this resolvent.
Working over F remains allowed; Q descent of this cover is not assumed.
No algorithm for recovering the required square class has yet been
implemented.

Identification with the specified Shimura curve is a separate proof
obligation. The review did not uncover the independent exact CM jets
needed for D69's order-four vanishing criterion. Voight–Willis's
method is numerical, and §3 distinguishes its checks from rigorous
verification. CM algebraicity alone does not compute exact coefficients.
[Voight–Willis](https://jvoight.github.io/articles/ModFormPaper-090317.pdf).
Guillemot–Voight's certified path tracking verifies the monodromy of
a specified Belyi map candidate against a given permutation triple;
we do not have such a Belyi map/passport identifying this Shimura
curve. That method was reviewed, not executed here.
[Guillemot–Voight](https://arxiv.org/pdf/2604.15562).

The path to the original field remains: identify the base curve and
construct the specified genus-64 Y; obtain the target part of J(Y)[2];
recover and certify its projective field polynomials. The present
result advances the branch data needed in the first step.

## 6. Reproduction and verification

From the repository root:

```sh
DOT_SAGE=/private/tmp/dembele-d70-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/119_cm_frame_marks.py
python3 dembele/pari/120_cm_frame_marks_check.py
python3 dembele/pari/120_cm_frame_marks_check.py --collect-only
```

Script 119 takes about 20 seconds on the recorded run. Script 120's
Magma job passes in 46.070 seconds with a 120-second timeout and 2 GB
memory cap. It requires an explicit final PASS marker and rejects
Magma error messages. The runner stores source and log SHA-256 hashes
in [`cm_frame_marks_check.json`](../data/computed/cm_frame_marks_check.json).
The ordinary-point jet matrix, the four numerical divisor matrices,
and recognition provenance are in script 119's JSON.

Collection mode passes. A separate standard-library calculation checks
the primitive point against all quadrics, every saved jet equation
modulo t^16, and determinant 8. The provenance audit checks nine
D68–D70 reports and 52 distinct source/log hashes; Python syntax,
119 local Markdown links and the tracked whitespace check pass.

These are targeted algebraic certificates, not a rerun of D63's
111-test backend suite. No D68/D69 equation or verification artifact,
earlier backend code, or external checkout is changed. All jobs are
finished; the work remains local and uncommitted.
