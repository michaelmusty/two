# The normalized B3 fibre and the cubic-cover input

Date: 2026-09-19. Decision D77. Continues
[the rational double-cover construction](cm-frame-rational-double-cover.md).

**Follow-up:** [D78](cm-frame-cover-class-arithmetic.md) constructs
the genus-40 section model and verifies a Frobenius-fixed,
anti-invariant third of the branch difference modulo 31. The
Kummer function remains to be recovered. The statements below
describe the D77 checkpoint.

**Result:** the normalized fibre of the rational genus-40 cover X over
the degree-nine point B3 is the field

\[
H=K(\sqrt{-3}),\qquad [K:\mathbf Q]=9,\quad [H:\mathbf Q]=18.
\]

Here K is exactly D70's nonic residue field. An explicit witness proves
that the leading unit of the double-cover equation is **-3 times a
square in K**. The involution fixes K and negates sqrt(-3). Over
Q(sqrt(-3)) the fibre splits into two disjoint degree-nine divisors
D+ and D-, exchanged both by the cover involution and by conjugation
of the constant quadratic field.

The exact fibre and its rational local parameter pass an independent
verifier and a corrupted-unit control. The fibre contains the cube
roots of unity required by total ramification in the intended cyclic
cubic cover. This necessary condition selects the scalar twist within
the fixed branch-half class over F. It does not identify that half or
the candidate curve with the arithmetic Shimura data.

We also prove **D+-D- is not principal**. The next construction must
therefore solve a nontrivial 3-division problem in the divisor class
group; no cyclic cubic extension or genus-64 Y is obtained here.

## 1. Exact normalized local algebra

Let a=X15/X16 on B3. Script
[157](../magma/157_cm_frame_B3_fiber.m) computes an affine lexicographic
shape presentation of B3 and verifies it against the original ideal.
Its degree-nine polynomial f agrees exactly with D70's polynomial.
Every projective coordinate, with X16=1, is exported as a polynomial
in a of degree at most eight.

The coordinate t=X15/X16-a is a local parameter after extending the
residue field to K=Q[a]/f. A nonsingular 14-by-14 Jacobian minor gives
two exact coefficients for all sixteen coordinates:

\[
x_i(t)=p_i+v_i t+v_i^{(2)}t^2+O(t^3).
\]

All 91 curve quadrics vanish modulo t^3. For D76's fixed equation
w^2=n/d, the computed expansions satisfy

\[
n(t)=n_2t^2+O(t^3),\qquad d(t)=d_0+O(t),\qquad n_2d_0\ne0.
\]

Consequently z=w/t is the regular unit coordinate on the normalized
cover and its residue satisfies

\[
z^2=\alpha,\qquad \alpha=n_2/d_0\in K^*.
\]

Thus the normalized fibre is K[z]/(z^2-alpha). Since alpha is nonzero
and the characteristic is zero, this is an étale K-algebra of rank
two. In contrast, substituting w=0 into the original singular equation
would give a doubled fibre and lose the two branches.

The coordinates, both jets, the Jacobian minor and all local units are
in [cm_frame_B3_fiber.json](../data/computed/cm_frame_B3_fiber.json) and
[its Magma companion](../data/computed/cm_frame_B3_fiber.m). Collector
[158](../pari/158_cm_frame_B3_fiber_data.py) checks the match to the
saved nonic field and records the degree-18 algebra.

## 2. The square class is exactly -3

Script [159](../magma/159_cm_frame_B3_fiber_squareclass.m) first uses
Norm(K/Q)(alpha) to screen the eight rational square classes represented
by +/-1, +/-2, +/-3 and +/-6. For a candidate c, alpha/c being a square
would force Norm(alpha)/c to be a rational square, because [K:Q]=9.
Only **c=-3** passes this necessary test.

Magma's number-field square-root routine then returns s in K with

\[
\alpha=-3s^2.
\]

This identity is checked exactly, and later checked again without a
square-root search. The software interface is documented under
[number-field element operations](https://magma.maths.usyd.edu.au/magma/handbook/text/386).
No maximal-order or class-group computation is invoked. The old large
nonic maximal-order timeout remains archived and is not repeated.

Norm(alpha) is negative. Hence alpha cannot be a square in K, since
the norm of a square would be a rational square. Equivalently, the
odd-degree field K cannot contain Q(sqrt(-3)). This proves that the
rank-two algebra is a field, of degree eighteen over Q. Set b=z/s;
then b^2=-3 and the primitive cube root is zeta3=(-1+b)/2.

## 3. A rational local parameter and the two branches

Script [160](../pari/160_cm_frame_B3_fiber_structure.py) uses the first
of the seven rational linear forms cutting out B3:

```text
ell = [-24,28,-8,15,-10,22,40,-2,12,-5,16,38,-8,32,12,1] * [X1,...,X16].
```

Write ell/X16=lambda*t+mu*t^2+O(t^3), with lambda nonzero. The code
exports lambda and mu and the coordinate jets after replacing t by
the rational parameter ell/X16. The regular fibre coordinate

\[
W=w/(\ell/X16)
\]

has values

\[
W=\pm b\,r(a),\qquad r=s/\lambda,\qquad
W^2=\beta=-3r^2.
\]

This presents D+ and D- on the normalized local chart by the original
B3 coordinates and W=+b*r(a) or W=-b*r(a). Over Q(b), each has degree
nine: the coprime field degrees 9 and 2 ensure that f remains
irreducible after extending constants. The sign labels are a choice
of orientation, not a match to the prescribed global branch cycles.

The exact witness, parameter change and branch ratio are in
[cm_frame_B3_fiber_structure.json](../data/computed/cm_frame_B3_fiber_structure.json)
and [its Magma data](../data/computed/cm_frame_B3_fiber_structure.m).
The involution fixes a and sends b to -b. After splitting the fibre,
the idempotents (1 +/- W/(b*r))/2 are checked to be complementary,
and the involution exchanges them.

There is also a usable specialization at 31. With b=11, since
11^2=-3 modulo 31, B3 factors as **[3,3,3]**. Each oriented divisor
has the same three cubic factors. In the power basis 1,a,...,a^8,
the values of W are

```text
D+ : [22,22, 8,21, 8,26,21,30,11]
D- : [ 9, 9,23,10,23, 5,10, 1,20].
```

Their difference is a unit in the nonic étale algebra. The total
fibre has six degree-three closed points modulo 31. These explicit
divisors can be used in the next finite-field class calculation.

## 4. What this says about the scalar twist

This is a necessary condition for the intended cubic step, not a
construction of it. Suppose Z->X is a **Galois cyclic cover of degree
three over F**, totally ramified at every point above B3. At each such
point its ramification index is 3, so the residue extension has degree
one. Tame inertia acts faithfully on the one-dimensional cotangent
space, forcing the residue field to contain a primitive cube root.
This is the characteristic-zero case of the inertia character in
[Stacks Project, Lemma 15.114.5](https://stacks.math.columbia.edu/tag/09EE).

For our cover, the residue field is K(sqrt(-3)), so this condition is
satisfied. It has a sharper consequence for scalar twists. Write
K_F=KF; its degree over F is nine because [K:Q]=9 and [F:Q]=8.
The totally real field F does not contain sqrt(-3), and neither does
its odd-degree extension K_F. A twist w^2=c*n/d, c in F*, has fibre

\[
K_F[z]/(z^2+3c).
\]

It contains the required quadratic field K_F(sqrt(-3)) exactly when
c is a square in K_F. By the odd-degree norm argument, this is
equivalent to c being a square in F: if s^2=c in K_F, then
c=(Norm(s)/c^4)^2 in F. Thus our cover is the **unique F-scalar twist
class of this fixed branch half** that passes this necessary inertia
condition.

For example c=-3 is invisible to a test at Q31, because -3 has a
square root modulo 31 and hence in Q31. But it changes the B3 fibre
to a split algebra, since (-3)*alpha=(3s)^2, and fails the cubic
inertia requirement. This is information beyond D76's local scalar
check. It does not rule out a different geometric branch half, prove
existence of the cubic extension, or identify the Shimura curve.

## 5. The oriented difference is not principal

Script [163](../pari/163_cm_frame_B3_branch_class.py) checks a new
small rank certificate. The sixteen coordinate values at B3 have
rank nine; a saved nine-by-nine minor has determinant **17 modulo
31**. Therefore h0_C(K_C-B3)=7, and Riemann–Roch gives

\[
h^0_C(B3)=9+1-16+7=1.
\]

Let L=O(E_Q-B3) be D76's branch half, of degree nine. D70's exact
certificate h0_C(2B3-B2)=0 excludes L~B3. Thus the degree-zero
bundle O(B3) tensor L^(-1) has no section. The double-cover
eigenspace decomposition and projection formula give

\[
\pi_*O_X=O_C\oplus L^{-1},\qquad
h^0_X(\pi^*B3)=h^0_C(B3)+h^0_C(B3-L)=1.
\]

The general eigensheaf description is recalled in
[Alexeev–Pardini, §1.1, equation (1.1)](https://arxiv.org/pdf/1102.4184).
In this degree-two case the projectors (1+tau)/2 and (1-tau)/2 are
defined over Q, so the decomposition applies over our ground field
as well. The numerical ranks and vanishing inputs are our exact
certificates, not an inference from that reference.

After extending constants, pi^*B3=D++D- and the two divisors are
disjoint. A function with divisor D+-D- would be nonconstant and
belong to H0_X(pi^*B3), contradicting its dimension one. Hence

\[
[D_+-D_-]\ne0\quad\text{in }\operatorname{Pic}^0(X_{\mathbf Q(\sqrt{-3})}).
\]

The rank minor and deductions are retained in
[cm_frame_B3_branch_class.json](../data/computed/cm_frame_B3_branch_class.json).

## 6. Independent verification and next computation

Magma [161](../magma/161_cm_frame_B3_fiber_check.m) checks saved
coordinates and jets against every curve equation, verifies the
Jacobian minor, recomputes the leading unit, and checks alpha=-3s^2.
It repeats the jet check in the rational ell parameter, verifies the
involution and splitting idempotents, and checks the specialization
at 31. It performs no linear solve or square-root search.

The negative control adds 1 to the constant coefficient of alpha.
The original point and zero orders remain unchanged, but the equality
n2=d0*alpha fails. The combined certificate is
[cm_frame_B3_fiber_check.json](../data/computed/cm_frame_B3_fiber_check.json).

| Job | Whole wall time | Limit |
|---|---:|---|
| Exact fibre and two jets, 157 | 76.599 s | 180 s / 2 GB |
| Square-class search, 159 | 0.678 s | 180 s / 2 GB |
| Rational parameter and branches, 160 | 5.819 s | 180 s, no Sage memory cap |
| Independent fibre certificate, 161 | 43.402 s | 180 s / 2 GB |
| Corrupted-unit control | 26.301 s | 180 s / 2 GB |

```sh
python3 dembele/pari/162_cm_frame_B3_fiber_check.py --collect-only
python3 dembele/pari/162_cm_frame_B3_fiber_check.py
python3 dembele/pari/162_cm_frame_B3_fiber_check.py --rebuild
python3 dembele/pari/163_cm_frame_B3_branch_class.py
```

Runner 162's default repeats independent checking and the control;
`--rebuild` also repeats 157–160. The source/log hashes and resource
bounds are retained. Earlier curve, cover, marks and lift artifacts
are unchanged; no full backend regression or remote job was run.

**Next:** over Q(sqrt(-3)), or F(sqrt(-3)) if necessary, put
Delta=D+-D-. Seek a degree-zero divisor A and function h with

\[
\operatorname{div}(h)=\Delta+3A,\qquad 3[A]=-[\Delta].
\]

Then v^3=h has the required local exponents 1 and -1. Start by
representing the saved oriented divisors on X modulo 31 and testing
the corresponding class division there. Do not assume the class is
divisible over the finite base field or that its third is unique.
The [Kummer sequence](https://stacks.math.columbia.edu/tag/03PK)
explains why the divisor-class choice and a scalar remain part of
the extension data. The involution, constant-field descent, and the
specified Fuchsian S3 monodromy must select and verify the desired
extension. Branch supports alone do not select it.

The intended cover would have genus(Z)=136, with reflection quotient
Y of genus 64; see [the existing monodromy specification](genus64-cover.md).
Those curves, the arithmetic identification and the final nonsolvable
field polynomial remain open. No further 31-adic precision is the
default next step.
