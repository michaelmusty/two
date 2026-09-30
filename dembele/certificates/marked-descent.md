# Marked descent and a rational CM-polynomial pilot (D58)

Date: 2026-09-16. This follows the user's request to work on descent of the
marked curve before attempting rational reconstruction.

**Result:** the canonical-model argument gives a descent of `(C,P,D)` to
Q, independently of hyperellipticity. With D56's ordinary-point and
nonzero-moment hypotheses, this marked curve is rigid, its given F-model
is the base change of that descent, and the normalized functions X,Y
are Q-defined. Their CM value polynomial is consequently in Q[T].
The bounded reconstruction below recovers no complete polynomial.

**D59 follow-up:** [cm-orbit-recognition.md](cm-orbit-recognition.md)
constructs the labelled CM ideal-class/root matching and runs simultaneous
recognition in the known residue field. It supplies the previously
missing labels, with complex-orientation inputs recorded, but no exact
target value is recovered at the tested bounds.

This is a geometric argument using the cited canonical-model and marked
descent theorems, supported by exact arithmetic checks. It is not an
explicit computation of descent isomorphisms. The D56 hypotheses remain
numerically supported rather than certified on the target curve.

## 1. An earlier descent result, independent of hyperellipticity

Write S for the genus-40 norm-one Shimura curve, w_p for its Atkin--Lehner
involution, and pi:S -> C=S/<w_p> for the degree-two quotient. This avoids
confusing the upstairs curve with D56's function X.

[Dembélé, Theorem 5.1 and Lemma 5.2](https://arxiv.org/pdf/1906.06772)
give the signatures and descent of S together with w_p. The lemma's
proof uses the invariant finite prime, a trivial ray class group, and
the unique CM point for Q(zeta_32)/F. It precedes, and does not use, the
disputed hyperellipticity assertion in Theorem 5.9. D57's source audit
overlooked this lemma when discussing descent; that omission is corrected
here. The signatures are

    S: (40; 3^18,16),        C: (16; 2^17,3^9,32).

Let Q_* be the unique order-16 elliptic point upstairs and P=pi(Q_*) the
order-32 point downstairs. Let D be the sum of the seventeen order-two
points downstairs. The local stabilizer inclusions give ramification
index two at Q_* and above every point of D; the order-three points are
unramified. Hence

    Branch(pi)=P+D,        deg Branch(pi)=18.

This also agrees with Riemann--Hurwitz: 78-2*30=18. The branching here is
that of S -> C, not a hypothetical map from C to a genus-zero curve.

## 2. Carry the marking through the same descent

It is essential to establish the field of moduli of the *marked cover*.
An F-rational point on a curve of field of moduli Q does not by itself
establish this. Nor would separately chosen Q-models of S and C supply
a compatible Q-model of their map.

Here is the compatibility argument applied to the arithmetic data in
Lemma 5.2. It uses canonical conjugation of the Shimura datum, including
its level, maps, and CM embeddings.

For an automorphism tau of Qbar, put sigma=tau|F. The canonical conjugate
of S is uniformized by a maximal order in the conjugate quaternion
datum: the split real place moves with sigma, while the finite
ramification set is still {p}. Applying sigma to the coefficients of
the original quaternion algebra gives an algebra with precisely these
ramification places, because sigma(p)=p. Quaternion classification
identifies the two algebras, and narrow class number one identifies the
maximal orders up to conjugacy. Comparing at the corresponding split
real places gives the uniformizing isomorphisms; the full unit signatures
(class and narrow class numbers both one) allow the orientation to be
matched in this comparison.

Make that comparison simultaneously for the norm-one subgroup and the
positive normalizer. Reduced norm, positivity at all real places, and
the inclusion of these groups are preserved. The resulting conjugacy
therefore identifies the covers, carrying the p-labelled Atkin--Lehner
operator with them. This is the level-compatible use of the
canonical-conjugation argument, not a deduction from equal signatures
alone. In particular, applying sigma to a quaternion generator while
keeping the old split embedding fixed would be an incorrect comparison.

The comparison also transports optimal CM embeddings. The field
Q(zeta_32) and its maximal order are Galois stable. Its unique CM point
upstairs must therefore be taken to Q_*. Consequently, for every tau
there is a marked isomorphism

    tau(S --pi--> C; Q_*)  ~=  (S --pi--> C; Q_*).

Thus this marked map has field of moduli Q. The point Q_* is smooth on
the coarse curve: a nontrivial elliptic stabilizer is not a singularity
of that curve.

[Sijsling--Voight, Theorem 1.3.2](https://jvoight.github.io/articles/birch-descent-021420.pdf)
in the 2020 author version (Theorem 1.8 in the published numbering)
then descends the map together with its smooth source marking. We get
pi_0:S_0 -> C_0 and Q_{*,0} over Q. Its image P_0 is Q-rational, and

    D_0=Branch(pi_0)-P_0

is a Q-defined divisor. This proves the geometric marked descent.
No ordering or individual rationality of the seventeen points is required.

The canonical-model comparison is the substantive literature input in
this step. Script 95 checks its arithmetic prerequisites; it does not
reprove that comparison theorem from numerical curves. The general
canonical-model formulation in
[Clark--Voight, Example 10.3](https://jvoight.github.io/articles/triangle-031622.pdf)
is useful context. Its separate triangle-congruence argument is not
being applied to this genus-16 curve.

## 3. Rigidity removes the possible F-twist ambiguity

Assume D56's hypotheses: P is ordinary and the second and third moments
used there are nonzero. Then

    dim L(16P)=1,    dim L(17P)=2,    dim L(18P)=3.

Choose x in L(17P) outside the constants and y in L(18P) outside L(17P).
Any geometric automorphism preserving P and D acts by

    x -> a*x+b,       y -> c*y+d*x+e,       a*c != 0.

Let E=Tr_D/17. D56's normalization is invariant under exactly these
changes:

    xc=x-E(x),             X=E(xc^2)/E(xc^3)*xc,
    z=y-E(y)-E((y-E(y))*X)/E(X^2)*X,
    Y=E(z^2)/E(z^3)*z.

The automorphism therefore fixes X and Y. Their pole degrees are 17
and 18. The degree of Qbar(C)/Qbar(X,Y) divides both, so it is one.
Thus the automorphism is the identity:

    Aut(C_Qbar,P,D)=1.

This proves more than the existence of a geometric Q-form. The unique
marked isomorphism from the given F-model to (C_0,P_0,D_0)_F is fixed
by Gal(Qbar/F), hence is defined over F. There is no remaining F-twist
for this marked object under the stated hypotheses.

Likewise, the unique marked comparison maps phi_sigma satisfy

    phi_(sigma*tau)=phi_sigma * sigma(phi_tau)

automatically: both sides are marked isomorphisms with the same source
and target. This is the Weil cocycle criterion, as formulated in
[Sijsling--Voight, Theorem 2.1.1 and section 2.2](https://jvoight.github.io/articles/birch-descent-021420.pdf).
It supplies an intrinsic descent datum, although we have not calculated
its matrices in the numerical canonical basis.

All operations in the formulas commute with this descent. Consequently
X,Y belong to Q(C_0), generate Q(C_0), and X/Y is a Q-defined local
parameter at P_0. No choice of tangent vector is required for this claim.

## 4. The rational reconstruction target

Put A_0=H^0(D_0,O_D0). Then

    H_X(T)=Norm_(A_0/Q)(T-X|D_0) in Q[T],     deg H_X=17.

D57 gives a transitive degree-17 divisor over F. Hence D_0 is also a
single closed point of degree 17. Its residue field has no intermediate
field over Q. Since E(X)=0 and E(X^2)!=0, the restriction X|D_0 is not
constant and therefore generates A_0. Thus H_X is irreducible.

One can also descend D57's abstract residue-algebra identification.
After the F-identification, A_0 embeds into the Harbater field H_K:
A_0 tensor F is the degree-17 extension of F already embedded there.
The image of A_0 has degree 17 over Q. In C17 semidirect C16 all
subgroups of order 16 are conjugate complements. It follows that

    A_0 ~= Q[theta],       H_Elkies(theta)=0.

This still supplies no labelled embedding of the numerical CM points
and no coordinates of X in the theta power basis. The unknown flag
from D57 is now a Q-flag in this algebra, rather than merely an F-flag.
Knowing H_X would give the CM restriction of X up to an algebra
isomorphism, not the whole curve or the desired nonsolvable field.

For H_X=sum c_i*T^i, Newton identities and the normalization give

    c17=1,        c16=0,        2*c15=3*c14.

Indeed, sum X=0, sum X^2=-2*c15, and sum X^3=-3*c14. We use the
15 independent indices 0,...,13,15 in the pilot.

## 5. Exact supporting computations

Script [95_marked_descent.py](../pari/95_marked_descent.py) checks:

* F/Q has the order-eight automorphism sigma(b)=b^3-3*b. This is a
  generator choice different from the one in the original Magma script.
* p=(2+b), Norm(p)=2, (2)=p^8, and
  `2+sigma(b)=(2+b)*(b-1)^2`. In particular p is invariant.
* The class and narrow class numbers of F, and the class number of
  Q(zeta_32), are one, with Sage/PARI proof enabled. Since O_F/p=F_2,
  narrow class number one implies the required ray class group is
  trivial for p times any subset of the real places.
* The CM lift acts by beta -> (1-b)*beta on beta^2=-2-b, and the product
  of its eight successive factors is -1. This is consistent with
  D57's order-16 lift, not an order-eight lift on K.
* The branch degree computed from the two genera is 18.

The test suite independently compares the field identity with the
cyclotomic action and verifies that trace normalization removes a
nonrational semilinear change of generators in an exact algebra.
Neither test purports to certify the target's ordinarity or moments.

## 6. Bounded numerical pilot

The pilot reads the four saved polynomial banks in
`cm_pointed_maps_flag_16384.json`: current, previous, alternate_fit,
and larger_probe. It creates no new analytic bank.

For each coefficient, the interval is centered at the real part of the
current value. Its radius is ten times the largest of the three complex
L1 discrepancies from the other banks and the four imaginary parts.
All interval arithmetic uses exact fractions parsed from the saved
decimal strings. The factor ten is a stated empirical choice, not an
analytic error estimate.

`Fraction.limit_denominator(B)` supplies a nearest rational with
denominator at most B. Exact Farey neighbors determine whether a hit
is unique in the closed interval. Thus a `none` result is exhaustive
for the *chosen interval and bound*. It is not a lower bound for the
denominator of the unknown exact coefficient.

| Denominator bound B | Independent intervals with a hit | With exactly one rational |
|---:|---:|---:|
| 1,000 | 0/15 | 0/15 |
| 10,000 | 0/15 | 0/15 |
| 100,000 | 5/15 | 4/15 |
| 1,000,000 | 10/15 | 0/15 |

At 10^6, indices 0,1,2,3,10 have no hit. The reported hits are individual
interval tests, not a jointly consistent polynomial; in particular the
dependent c14 must also obey the Newton identity in any future candidate.
No complete candidate is available at any tested bound. Small imaginary
parts or satisfaction of the normalization identities do not supply
independent accuracy evidence.

An exact control makes the height limitation concrete. For D57's
simple generator X1=(17*theta-2)/30, its monic polynomial is

    (17/30)^17 * H_Elkies((30*T+2)/17).

Its largest coefficient denominator is
215233605000000000000000, about 2.15e23. Therefore a cap on each monic
coefficient denominator can reject even a very simple field element.
The code recovers this entire control polynomial uniquely from
80-place truncated decimals with a known truncation bound; those
80 certified control digits are not attributed to the target data.

## 7. Artifacts, reproduction, and next step

From the repository root:

```sh
DOT_SAGE=/tmp/dembele-d58-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/95_marked_descent.py
DOT_SAGE=/tmp/dembele-d58-sage OPENBLAS_NUM_THREADS=1 \
  sage -python -m unittest discover -s dembele/tests -v \
  > dembele/data/computed/marked_descent_tests_20260916.out 2>&1
```

The identical [JSON](../data/computed/marked_descent.json) and
[out file](../data/computed/marked_descent.out) contain source hashes,
exact field checks, all interval decisions and the height control.
All **96 tests pass**, including six new controls; see the
[test log](../data/computed/marked_descent_tests_20260916.out).

The descent question has been resolved at the theorem level, with the
function conclusions subject to D56's existing hypotheses. The useful
next arithmetic task is now to construct a labelled identification
between the CM class-group orbit and the embeddings of Q(theta), then
test simultaneous recognition of X|D in that algebra. That would use
all seventeen conjugate values and account for normalization, rather
than independently guessing monic coefficients. Whether the current
data suffice for that identification is still to be checked. The
exact evaluation flag remains an alternative target. Increasing these
denominator caps alone already creates ambiguous intervals and does
not solve the missing-information problem.

No exact target CM polynomial, curve model, torsion point, or
nonsolvable field polynomial has been recovered. No remote job,
external Belyi edit, message, commit, or cleanup was performed.
