# D146: control the omitted intersections and close the Faltings-only route

Date: 2026-10-08. Continuation authorized by “continue”.

The omitted intersection terms cannot supply the improvement required
by D145. On the actual normalizer curve, in the existing normalization,

    48 < S := Psi+I < 79.                                      (1)

Combining (1) with D144's corrected compact Riemann--Roch identity
and D145's spectral lower bound gives

    h_Fal(C) < 4.2.                                           (2)

Thus the D141 sufficient lower target 29 is false. All three of
D141's critical height thresholds are excluded, not just the rounded
integer 29. This closes the proposal to repair those existing P1600
jet inequalities by improving only the Faltings lower bound.

The actual relation-space target `h_ext(I_2)<=623` remains open.
Neither the recognized candidate nor the original-kernel field route
is refuted by this result. Positive exact vanishing, identification,
the later marking/Hecke/cover obligations and the field polynomial
remain unproved. No new precision bank or numerical spectrum is used.

The new geometric proof is given below. Its numerical consequences
retain D104/D143's CM-height source reconciliation and D144's
reconstructed RR normalization. Those repairs are our derivations,
not author-confirmed errata. The bound on S does not use a spectral
calculation. Finite audits check the algebra and numerical enclosures;
they do not mechanically verify the geometric arguments or theorems.

## 1. What remains after the dyadic calculation

Use the uncontracted model Q and notation of
[D144](P1600-joint-adjunction-RR-d144.md). The orders are seventeen 2,
nine 3, and one 32. Put alpha_m=1-1/m and gamma_m=m-1/m. Its exact
adjunction formula and the already computed tail corrections give

    S = sum_i gamma_(m_i) (h_L(P_i)+log(m_i))
          -(1193197/6144)log(2) - C_odd,                        (3)

provided the known dyadic pairs are the complete dyadic intersections.
Here C_odd is the weighted unordered pair cost at odd primes, with
coefficient alpha_m alpha_n(m+n) for a pair of orders m,n.

The required dyadic completeness follows from the marked components
in D143. Distinct components have disjoint smooth sections. Component
5 has just the order-two anchor and P_32, whose intersection was
recovered in D144. Components 51,...,58 carry the eight ordinary
order-two pairs already computed in D119. The only remaining
same-component pairs are the two order-three points on each of
35,...,38. Each of these four vertex groups has order three. Its
reduction acts faithfully on P1(F_2), and the two fixed directions
in P1(F_4) are distinct. Since this action is tame, their quotient
images stay distinct: each direction is its own orbit. Their
intersection on Q is zero. Component 1 carries only one mark.

Consequently there is no further dyadic cost on Q. The intersections
created by contracting marked tails are already included in the
coefficient in (3). They must not be counted again. Source 615
reconstructs the coefficient from the individual 27 marks, pair
lengths and tail paths, rather than copying the collected coefficient.

## 2. The integral quotient at an odd prime

We use the smooth small-level models and level compatibility from
D104/D143. [Yuan, Proposition 4.1 and its proof, pp. 54--56](https://arxiv.org/pdf/2205.13995v3)
give the maximal-level quotient, compatibility with the special
fibre, absence of vertical generic inertia, and the integral
orbifold/Hodge-line identity away from the quaternion discriminant.
The proof also describes supersingular stabilizers in the nearby
definite quaternion algebra and the faithful local deformation action
modulo the center. These are the structural inputs used here.

For the normalizer choose the small level normal under the dyadic
Atkin--Lehner element as well. The extra quotient has order two,
invertible at the chosen odd prime. The same smooth quotient and
orbifold-line conclusions therefore apply. The kernel of a finite
group action on a special component is a residue-characteristic
group: any tame element trivial on that component can be linearized
and must be trivial. Since the extra normalizer quotient has order
two, any possible odd-primary kernel lies in the maximal-level
group, where Yuan's result excludes it. Thus the local action below
is faithful on the special formal disk.

After an unramified extension, followed by a finite extension splitting
the relevant sections, let R be the complete DVR. At a special point
upstairs the local source is R[[t]], with a finite stabilizer G, and
the coarse quotient is R[[u]]. All maps are finite and flat locally.
Normalize the valuation nu by nu(3)=1 when working over 3; arbitrary
ramified base extensions simply scale the unnormalized formulas.

The rest of the local argument is our derivation, including its
application to the normalizer; it is not a quotation of an
intersection formula from Yuan.

## 3. Only characteristic three can contribute at odd primes

For a faithful finite action on the special disk k[[t]], the tangent
map G->k^* has cyclic image of order prime to the characteristic.
Its kernel is a characteristic-primary group: successive quotients
of the filtration by the first nonzero coefficient of g(t)-t are
subgroups of the additive group of k. The filtration terminates for
a finite faithful group. In particular every wild stabilizer has
an element of order equal to the residue characteristic.

At an ordinary point the local endomorphism algebra splits as
F_v direct sum F_v. A projective finite-order element has its
eigenvalue ratio in F_v. For an odd residue prime, F_v/Q_p is
unramified, so F_v contains no primitive pth root of unity. Thus
ordinary stabilizers are tame.

At a supersingular point the projective stabilizer embeds in the
nearby definite quaternion algebra B(v)^*/F^*. If a projective
element has odd prime order p, its invariant reduced trace satisfies

    Trd(g)^2/Nrd(g) = 2+zeta_p^a+zeta_p^(-a),  (a,p)=1.

This would put Q(zeta_p)^+ inside F=Q(zeta_32)^+. For p>=5 this is
impossible: the former is ramified at p, whereas F is ramified only
at 2. The exception p=3 has real subfield Q. Hence all stabilizers
at odd primes other than 3 are tame.

A tame stabilizer of a smooth disk is cyclic and can be linearized
over R. For a generator with nontrivial tangent multiplier lambda,
lambda-1 is a unit, so its fixed section is unique in that disk.
Its nontrivial subgroups have the same fixed section. Therefore two
distinct generic elliptic points cannot meet in a tame disk. We have
proved

    C_odd = C_3.                                             (4)

## 4. At three the only wild local groups are C3 and S3

Let P be the kernel of the tangent action at a wild special point
over 3. It is a nontrivial finite 3-group. The nearby quaternion
algebra is definite at every real place, so its projective group
embeds in SO(3,R). Any finite odd-primary subgroup of SO(3) is
cyclic: a central element of odd prime order is a rotation with a
unique axis, and its centralizer is the circle of rotations about
that axis. Thus P is cyclic.

There is no projective element of order 9, since its invariant trace
would contain the cubic field Q(zeta_9)^+, which cannot embed in
the degree-eight field F. Consequently P=C3.

The centralizer of P in the projective quaternion group is the
torus E_3^*/F^*, E_3=F(sqrt(-3)). Its finite subgroup in G has no
element of order two. Such an element would be represented by a
trace-zero element c*sqrt(-3), with norm 3c^2, of odd valuation at
the prime over 3. A special-point stabilizer at maximal level at 3
has even norm valuation modulo the center, hence has an integral
norm-unit representative there. This is incompatible with 3c^2.

There are no other odd prime factors by section 3 and no order 9.
Thus the finite centralizer is exactly P. Conjugation embeds G/P
in Aut(P)=C2. The two possibilities are

    G=C3  or  G=C3 semidirect C2=S3.                          (5)

This uses the same norm-parity normalization as D145. Globally one
may normalize reduced norms to 1 or 2+b; neither has valuation at 3.
Source 614 checks that 3 is inert of degree eight and the related
order-six square conditions 3 and 3(2+b) fail in F. These are finite
controls on the argument, not substitutes for its all-prime proof.

No order-32 section can enter a wild disk in (5). There can be at
most one coarse order-two section in an S3 disk: each reflection
is tame and has a unique fixed section, and the three reflections
are conjugate. Thus the only possible intersecting pair types at 3
are (3,3) and (2,3).

## 5. Derivatives bound the entire order-three intersection row

Choose a lift a in the formal disk of a generic order-three point,
and let h generate its stabilizer C3. Its tangent multiplier is a
primitive cube root of unity. Since h acts nontrivially on the
special disk, h(t)-t has no vertical factor. Weierstrass preparation
after splitting its roots writes it as a unit times the product of
its distinct generic fixed sections. Differentiating at a gives

    sum_(b != a, h(b)=b) nu(a-b)
      = nu(h'(a)-1) = nu(3)/2.                               (6)

This bounds all such collisions together. It requires neither an
explicit CM coordinate nor a claim that there are exactly two roots.

Write the quotient map as u=f(t). The different can be calculated
either from f' or from the orbit polynomial with roots g(t).
The monogenic and smooth-curve formulas agree; see
[Stacks, Examples/Lemmas 49.12.5--49.12.6](https://stacks.math.columbia.edu/tag/0BWB).
In the present formal coordinates this gives

    f'(t) = unit * product_(g in G, g != 1) (t-g(t)).          (7)

The unit is an R[[t]] unit. One can also prove (7) directly by
Weierstrass preparation of f(t)-u: its monic degree-|G| polynomial
is the orbit polynomial, and differentiating at t gives the formula.

Write f(t)=f(a)+A(t-a)^3+... . The two factors for h and h^2
in (7) vanish to first order at a; their derivative multipliers
have product of valuation nu(3). Therefore

    nu(3A) = nu(3) + sum_(g outside C3) nu(a-g(a)).            (8)

The integral third derivative has coefficient 6A, so its content
d_3 is also the right side of (8). On the smooth model at 3 the
vertical and tail terms vanish. The local line identity, or D144
equation (5), says

    d_3 = 3 r_i - 2 nu(3),
    r_i = sum_(j != i) (1-1/m_j) J_ij.

It follows that

    r_i = nu(3) + (1/3) sum_(g outside C3) nu(a-g(a)).         (9)

For G=C3 the second term is zero. For G=S3, the three reflections
send a to the same other h-fixed point b. Equation (6) bounds
nu(a-b) by nu(3)/2. Thus, uniformly for every one of the nine
order-three points,

    nu(3) <= r_i <= (3/2)nu(3).                              (10)

The factorial valuations matter: d_3 is the valuation of 6A, and
the adjunction comparison uses 3^3 A. Dropping one factor of 3
would give a different, incorrect row bound. Source 615 includes
that failed-identity control.

As explicit controls, take h(t)=1/(1-t), r(t)=1-t, and

    u=(t^3-3t+1)/(t(t-1)),    v=(2u-3)^2.

The first is invariant under C3; the second under S3. The h-fixed
points satisfy t^2-t+1=0. Their u-values have difference squared
-27. In the S3 quotient the order-three value is -27 and the
order-two value is 0. The two different-unit factors in (7) are
1/(t(t-1)) and 4/(t^2(t-1)^2), respectively, which are units at
the relevant residue point over 3. Sources 614/615 verify these
identities in separate forms. These examples check constants; we
do not assume that every actual action has these coordinates.

## 6. Global cost and the resulting height bound

Let A be the sum of all order-three/order-three intersections at 3,
and B the sum of all order-two/order-three intersections there,
with absolute finite-degree normalization. By section 4 there are
no other intersecting types. Their cost and total row weight are

    C_3 = (8/3)A+(5/3)B,
    T = sum_(m_i=3) r_i = (4/3)A+(1/2)B.

The exact nonnegative identities

    C_3-2T = (2/3)B,
    (10/3)T-C_3 = (16/9)A

combined with (10), summed over all nine points and all places
above 3, give

    18 log(3) <= C_3 <= 45 log(3).                            (11)

The absolute normalization of the sum of nu(3) is log(3), even
after extending to split the sections. This is why no factor of
eight or a residue-field norm is inserted in (11).

Substitute (11) in (3), using both endpoints of the certified CM
Hodge-height intervals. The lower expression is centered at
48.89142 and the upper expression at 78.55395. Their outward
intervals prove (1). In particular the D145 necessary condition
S<-249 is impossible.

For an explicit consequence, D144 gives

    12 h_Fal = R-S-6 log C_*-6 average(log Z'),

with R in D143's model-corrected interval and
`log C_*=15log(pi)+(5081/192)log(2)+log(3)-485/64`.
D145 proves average(log Z')>-41. Hence

    h_Fal < (R_upper-S_lower-6(log C_*)_lower+246)/12 < 4.2.

The unrounded upper-expression interval is centered at 4.11741.
Both independent calculations enclose it strictly below 4.2.
Source 615 also compares 4.2 with all three saved D141 critical
intervals, so rounding 29 down does not rescue the Faltings-only
proposal for the existing P1600 jet criterion.

## 7. Next proof task and audit status

Return to the actual quadratic relation space I_2 and D141's
sufficient exterior-height target 623. D142's row-by-row jet
estimate gives only 83240. A concrete next theoretical test is to
bound the determinant of the canonical multiplication sequence

    0 -> I_2 -> Sym^2 H0(omega) -> H0(omega^2) -> 0

in the fixed rational residue frame, retaining integral indices
and the archimedean quotient metric. This would address the whole
kernel instead of summing separate jet-height majorants. No bound
from that proposal is claimed here. Exact structural identification
remains an alternative. Neither proposal admits a new precision
bank, a new level computation, Hecke work or a cubic search.

Sources 614 and 615 pass in 5.32 and 4.04 seconds, each with one
Sage child. The independent audit reconstructs the marked-tail and
pair contributions, uses the independent D143 CM-height intervals,
checks the two different formulas and the factorial control, and
compares against the original D141 thresholds. No input job failed.

The [source applicability ledger](../data/computed/P1600_intersection_sources_d146.json),
[fixed review](../data/computed/P1600_intersection_review_d146.json), and
[completion record](../data/computed/P1600_intersection_completion_d146.json)
bind the result and inherited D145 provenance. All sources and passing
artifacts remain frozen. The 180-second private-process-group,
three-worker, 2 GiB per worker/store and 6 GiB aggregate caps persist.
