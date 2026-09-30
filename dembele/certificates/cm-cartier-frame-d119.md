# D119: the actual Cartier CM divisor and its dyadic residue index

Date: 2026-09-26. Continuation of D118's principal-parts task.

The local model hypotheses left open in D102 are now established at 2.
On the minimal regular semistable model, the sixteen non-anchor CM
sections meet in eight pairs, each of intersection multiplicity 33 in
v_beta. The anchor is disjoint from these pairs. Keeping these intersections
gives a finite flat Cartier divisor of degree 17 with algebra

    A = R x product_(j=1)^8 R[t_j]/(t_j^2+4*(2+b)).

In this actual algebra the principal-parts restriction map has nine unit
Smith factors and seven beta^2 factors. Thus

    length H1(O(D)) = 14,
    v_beta Norm(a) = 2,
    length coker(R_h) = 16.

The residue cokernel itself is (R/(beta^2))^8, so beta^2 is a sufficient
local clearing factor for the primitive pencil normalization. These
numbers refer to this model and its codifferent. The old stable evaluation
defect 245 is a different quantity.

This resolves a local normalization problem. It does **not** yet lower
D118's sufficient quadric valuations 25330/25444/25551, prove a positive
jet zero, identify the candidate, or construct the target polynomial.

## 1. Choose the model before its lattices

Work over the integers R of M_p after an unramified extension large enough
to split the uniformization model. Use v_beta(beta)=1, v_beta(2)=16 and
beta^2=-(2+b). The constructions and lengths may be checked after this
faithfully flat extension; no ramification normalization changes.

Begin with D99/D110's integral quotient model. Its noninverted graph has
58 vertices and 73 edges. Resolve the nodes, whose thicknesses are the
saved edge lengths, and contract the rational tails. This constructs the
minimal regular semistable model X. The remaining rational chains map to
the stable nodes; their resolution is crepant. In local charts this follows
by pulling back the same logarithmic generator dx/x along subdivisions of
xy=beta^n. Hence the canonical fibres on X are the pullbacks of the stable
canonical fibres, and H0(omega_X/R) is D116's integral harmonic lattice E.

The quotient's formal local description is
[Kurihara, Proposition 3-2 and Lemma 3-3, pp. 286--288](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf).
His quotient at an inverted edge is smooth even in this residue
characteristic. The cached primary scan was inspected again; the new
network request failed. For the later contractions,
[Stacks, 0CDF](https://stacks.math.columbia.edu/tag/0CDF) shows that a
contracted exceptional tail meets a smooth point of the resulting family.
The minimal regular model and its contraction property are
[0C9Y](https://stacks.math.columbia.edu/tag/0C9Y); stabilization preserves
H0(O) and H1(O) by [0E7B](https://stacks.math.columbia.edu/tag/0E7B).

Here are the actual marked components, using D99's one-based labels.
The anchor is on the inverted-edge disk at component 5. Tail contraction
moves this point through 5,4,2,3 to a smooth point of component 6. That
component lies inside the stable edge [9,10] of length 12 in v_b units.
The eight other pairs are on components 51,...,58, respectively. Each
of those components has two noninverted incident edges of length one,
and lies inside a different stable edge of length two. They survive on
the regular resolution. Thus different pairs and the anchor have no
intersections on X.

Source 456 checks these labels against the actual D111 Brandt matrix and
edge transports, and records all nine tail contractions (49 vertices and
64 edges remain before resolving thicknesses). Review 457 instead checks
the eight pairs against D99's recorded stable paths and the anchor's
attachment. Graph data locate the sections; the quotient and contraction
theorems supply their geometric interpretation.

## 2. Exact local equations of the intersections

At each ordinary inverted edge, D112 proves that the endpoint stabilizer
is trivial. Its full setwise stabilizer is therefore the involution that
reverses it. In the exact S coordinate its annulus is

    xy=2+b,       x=z,       y=(2+b)/z,
    involution: (x,y) |-> (-y,-x).

Put t=x-y. The completed quotient is R[[t]]. This also has a direct
integral proof: the original ring is free of rank two over R[[t]], with
basis 1,x and relation x^2-t*x-(2+b)=0. The involution sends x to t-x.
Invariance of A(t)+x*B(t) forces 2*B(t)=0, hence B=0 over R. This argument
does not assume that taking invariants commutes with reduction.

The two CM sections are x=beta and x=-beta, so

    t_plus=2*beta,       t_minus=-2*beta,
    t_plus-t_minus=4*beta,       v_beta(4*beta)=33.

Consequently their intersection length is 33 and their sum has local
equation F(t)=t^2+4*(2+b). At the signed CM coordinates
u=((z-beta)/(z+beta))^2, with the sign incorporated in D112's S matrix,

    (dt/du)_plus=4*beta,       (dt/du)_minus=-4*beta.       (1)

The matrices for the two signs satisfy S_minus(z)=S_plus(-z) projectively,
which fixes the signs in (1). This is the same ordinary quotient used as
a control in D118. It is not applied to the anchor's larger stabilizer.
The anchor is a single section at a smooth point of X; D112's witness k
already identifies its two eigenlines on the coarse curve.

Let D be the sum of these seventeen horizontal sections on X. It is
Cartier in the smooth locus, finite flat of degree 17, even though eight
pairs meet. Locally this is explicit from the monic equations F(t),
and at the anchor from a parameter. Equivalently use
[Stacks, 0B9D](https://stacks.math.columbia.edu/tag/0B9D).
This proves the algebra A displayed above. Its normalization is R^17;
each pair contributes index 33 and discriminant valuation 66. Therefore

    length(R^17/A)=264,       v_beta disc(A)=528.          (2)

It is essential to use this horizontal order. For example, the abstract
degree-17 generator theta is not in A: D112 certifies that every difference
of distinct theta roots has valuation at most 17, whereas membership in A
requires the values in each of these pairs to differ by a multiple of
4*beta. Neither the abstract order B nor its base change may be substituted
for A.

## 3. Compute the principal-parts map, including its torsion

Put N=H0(O_D(D)) and Lambda=H0(O_X(D))/R. The family is proper, flat and
Gorenstein, with H0(O_X)=R and H1(O_X) free of rank 16. Relative duality is
[Stacks, 0E6N](https://stacks.math.columbia.edu/tag/0E6N).
Generic nonspeciality follows, for example, from the nonzero rank-16
evaluation minor already certified in D115. All cofactors are nonzero,
so the generic generator has a pole at every point. D102's exact sequence
now applies to this actual model:

    0 -> Lambda -> N --delta--> E^dual -> T -> 0,
    T=H1(O_X(D)).                                           (3)

At a pair choose the A-module generator 1/F(t) of the normal module N.
An R-basis is 1/F(t), (t+2*beta)/F(t). Write h_plus and h_minus for the
actual leading harmonic coefficients in the two u coordinates. By (1),
the differential values relative to dt are

    e_plus=h_plus/(4*beta),       e_minus=-h_minus/(4*beta).

Adjunction and residues give the two rows of delta^dual:E->N^dual:

    (e_plus-e_minus)/(4*beta),       e_plus,

or, directly from the frozen harmonic bank,

    (h_plus+h_minus)/(16*beta^2),       h_plus/(4*beta).      (4)

At the anchor choose a parameter whose differential at the section is
the integral generator beta^296*du supplied by D116. This is possible
because the section is in the smooth locus of X. Its row is h_W/beta^296.
Changing this parameter by a unit cannot change any result below.

Source 456 builds the actual 17-by-16 integral matrix (4) from the frozen
P=200 bank. It uses certified ball arithmetic, not candidate equations.
Its Smith valuations and maximal-minor valuations are

    Smith:       [0 x 9, 2 x 7],
    cofactors:   [16, 14 x 16].                            (5)

Thus T is (R/(beta^2))^7 and has length 14. Divide the signed-cofactor
kernel vector by its common beta^14 factor. This gives the primitive
principal part a in N, up to an R-unit. Its coefficient at the anchor
has valuation 2; its two coefficients in each pair basis are units.
More decisively, evaluating a in the generic split algebra gives

    [v_beta(a(P_i))] = [2, 0 x 16],
    v_beta Norm_(A_K/K)(a) = 2.                           (6)

If a=A0+A1*(t+2*beta), these evaluations are A0+4*beta*A1 and A0.
Every value is certified nonzero. Applying D102's index formula to (3)
and (6) gives

    length coker(R_h:E->Z_A)=14+2=16,
    Z_A={ell in Hom_R(A,R):ell(1)=0}.                     (7)

There is a stronger direct check. In the pair basis {1,s=t+2*beta},
s^2=4*beta*s. Multiplication by a has matrix

    [ A0          0         ]
    [ A1   A0+4*beta*A1    ].

Review 457 composes its transpose with the restriction matrix, verifies
the trace-zero condition, and computes the resulting residue-map Smith
valuations [0 x 8, 2 x 8]. Hence its cokernel is exactly (R/(beta^2))^8.
This proves the local clearing assertion, rather than inferring it only
from the determinant length.

The trace-centered eta values are integral at 2: they come from an
integral field order and 17 is a unit here. Since A is a suborder of
R^17, every integral value vector defines an element of A's codifferent
under the generic trace pairing. Their zero sums put them in Z_A.
Thus beta^2*eta lies in the actual residue image, for the primitive
choice of h. This does not fix h's global scale or its archimedean norms.

## 4. Why this is different from the number 245

The stable evaluation matrix uses separate fibres at all seventeen
points. D102's map instead uses the dual of the normal module on D.
Passing to (4) takes eight divided differences, whose denominators each
have valuation 33. The anchor-deleted determinant therefore changes
from 280 to 280-8*33=16. The full minimum changes from 245 to 14, as
verified using every maximal minor. Neither of those minima alone is
the residue index: the principal-part norm must still be added.

The index also depends on the chosen integral model. As a control,
separate each ordinary pair by 33 successive smooth-point blowups.
In each chart dt=beta*dt_new, so each of the sixteen ordinary fibre
evaluation rows acquires 33 extra powers of beta. Starting from D116's
separate-fibre cofactor valuations v=[280,245 x 16], put k=[0,33 x 16].
The new valuations are v_i+sum(k)-k_i. They give

    length T_separated=740,
    principal-part norm valuation=68,
    residue index=808.

These are valid for the separated model's different normal module and
codifferent. They do not contradict (7), and they cannot replace it in
a bound with the original lattices. Review 457 verifies this control.

## 5. What the local result contributes to a global height argument

The marked divisor and minimal regular model are intrinsic under the
CM Galois action. The same local lengths occur at all seventeen primes
of H above 2. Since [H:Q]=272, their normalized contributions are

    dyadic cohomology torsion:       (7/8)*log(2),
    dyadic principal-part norm:      (1/8)*log(2),
    dyadic residue index:                  log(2).        (8)

Non-dyadic indices have not been computed. Neither (8) nor beta^2 is a
global denominator bound for an arbitrarily scaled h.

There is now a precise determinant identity with which to assess the
alternative frame. After a finite global extension, take regular
semistable models and the sum of the CM sections. At infinity identify
N with the direct sum of tangent lines by simple-pole coefficients,
and give it the direct-sum dual canonical-fibre metric. Give Lambda
the induced subline metric. Let I be the normalized finite intersection
sum over unordered pairs of CM sections and let tau be the normalized
length of T at all finite places. Then

    h(det N) = -sum_i H_CM(P_i)+I,
    h(Lambda) = h(det N)+h_Fal(C)+tau
                 -average_sigma log vol(delta_sigma).  (9)

For the first identity, the lattice of independent simple principal
parts is N0=direct_sum W_i^(-1), with N0 contained in N. At a pair its
index is 33, not 66. In a larger smooth cluster the determinant of the
simple-fraction change matrix is the product of pair differences;
the same identity follows. The metrics agree under this inclusion.
The second identity follows by taking determinants of (3), with the
quotient metric on N/Lambda; the torsion term has the displayed positive
sign. The archimedean volume is the product of the sixteen nonzero
singular values of delta. It cannot be discarded as an integral unit.

D117's row bound B=1/(sqrt(pi)*rho^2), rho^2=3/5, and Cauchy--Binet give
vol(delta_sigma)<=sqrt(17)*B^16. D118's H^+ and Faltings lower endpoint
h_Fal^- therefore give the explicit lower estimate

    h(Lambda) >= -17*H^+ + h_Fal^- + (139/8)*log(2)
                    -(1/2)*log(17)-16*log(B).            (10)

Here the proved dyadic contributions are I=(33/2)*log(2) and
tau=(7/8)*log(2); all other intersections and torsion lengths are
nonnegative. Equation (10) is a bound for the pencil line in the stated
metric. It is not a bound for the inverse residue map or for the
quadratic sections. Those further steps must keep their determinant,
codifferent, local clearing and operator norms in the same normalization.

In particular, replacing the old evaluation defect by 16 in D118's
formula has no justification. Dividing out vertical factors already
counted among the actual local zeros also leaves the exact-zero test
unchanged. D118's sufficient thresholds and actual bounds remain
25330/25444/25551 and 3794/3745/3728, respectively.

The next bounded task is to derive an explicit quadratic-section bound
for the intrinsic residue frame using (9)--(10), its codifferent and the
actual beta^2 clearing map. Compare its entire degree-minus-zero budget
with D118 before choosing it. If it gives no improvement, reject this
frame replacement and return to the exact-identity alternative or a
costed precision design. No new moment run is authorized by the local
index calculation alone; the existing census, new-level, Hecke-bank,
cubic-precision and 180-second job limits remain in force.

## 6. Independent verification and scope

See [the source ledger](../data/computed/cm_cartier_frame_sources_d119.json).
Source 456 uses the frozen ball implementation. Review 457 instead uses
416's integer polynomial quotients at 64 beta-digits, with common-factor
extraction and unit Schur complements. It reconstructs all 272 matrix
entries directly from the raw harmonic values, checks every one of the
17 maximal minors, the primitive kernel, and the full residue map.
All required source errors exceed that precision. The geometric arguments
above are mathematical proofs, not machine-verified theorems.

The first 456 run failed on an incorrect expected count after graph
pruning (50 instead of 49); its source, log and receipt are archived.
The corrected calculation passes in 3.883 seconds and the independent
review probe in 2.642 seconds. All jobs use runner 272, one BLAS thread
and a 180-second private-process-group cap. The final review preserves
all 911 D118 source hashes. Freeze successful sources and bound artifacts;
run the audit and its reproducibility check through the same runner:

    python3 dembele/pari/457_cm_cartier_frame_review.py --check

No moment precision, candidate equation, CM label or earlier proof is
changed. D99 nonhyperellipticity and D108's spectral rejection stand.
Exact curve identification and all downstream cover and field requirements
remain open. No correspondence was sent.
