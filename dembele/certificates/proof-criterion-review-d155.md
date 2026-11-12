# D155: rigorous review of the conditional P10480 proof criterion

Date: 2026-10-10. Scope: review the base-curve identification criterion;
no new precision column, higher-stage pilot or bank.

**Conclusion.** The conditional implication survives this review. If the
specified actual Shimura data satisfy the certified error bounds and the
91 quadratic residuals contain zero to those bounds at P10480, the candidate
is the actual genus-16 curve in its rational residue coordinates. Reaching
P10480 alone does not establish those hypotheses. The implication identifies
the base curve and its degree-17 CM divisor; it does not construct the
upstairs cover or Dembélé field polynomial.

The review supplies a direct proof of the rank step, reconstructs the
integral-section and height argument, resolves an additional normalization
inconsistency in a cited proof, and independently replays the relevant
finite arithmetic. It finds no correction to P10480. The second-order
margin is only **0.1693677259** in normalized natural-log degree, however:
an unaccounted uniform loss of four beta-digits would exhaust it.

New artifacts are the [rational bounds](../data/computed/proof_criterion_bounds_d155.json),
[independent controls](../data/computed/proof_criterion_controls_d155.json),
[fixed review](../data/computed/proof_criterion_review_d155.json),
[source ledger](../data/computed/proof_criterion_sources_d155.json) and
[completion record](../data/computed/proof_criterion_completion_d155.json).
The geometric deductions below are mathematical arguments, not claims of
formal verification by the finite scripts.

## 1. Precise conditional statement and the inherited inputs

Let C0/Q be the compatible descent of the specified Shimura quotient,
of genus 16, and let D0 be its closed degree-17 CM point. Write
V=H0(C0,K), dim_Q(V)=16. Use the rational residue basis of
[D106](cm-rational-frame-jets-d106.md), up to its one common nonzero
scalar, and the 91 frozen integer quadrics of
[D69](cm-frame-verification.md). Their coefficient L1 norms are at most
42550. The following dependencies are substantive:

| Input | Justification and scope |
| --- | --- |
| Actual curve, integral reduction and genus | [D99](hyperellipticity-review-d99.md)'s arithmetic reduction; independent of candidate equations. |
| All seventeen CM evaluation cofactors nonzero | [D105](cm-frame-arithmetic-d105.md)'s graph-divisor obstruction and CM transitivity. |
| Compatible Q-descent and rational residue basis | [D58](marked-descent.md)'s canonical conjugation, with the twist ambiguity removed by D106's marked rigidity. This is essential for the Q2 rank argument. |
| Correct actual CM labels and analytic branches | [D112](dyadic-cm-matching-d112.md)'s arithmetic matching; a numerical permutation of roots is insufficient. |
| Integral harmonic lattice and canonical fibre generators | D116's weighted residue lattice, saturation and global generation proof. |
| Integral section, uniform archimedean norm and height bounds | [D103](cm-adjugate-height-d103.md), [D104](cm-intrinsic-height-d104.md) and [D118](cm-finite-height-d118.md), with D116–D117, reviewed below. |
| Actual rank-45 jet restriction | D138 actual frame and D140 inverse certificates; replayed here without candidate equations. |
| Candidate is a smooth geometrically integral degree-30 curve | D69's exact algebraic certificate; identification does not use its matching point counts. |

For a future working precision P, require certified actual harmonic
solutions, transports, coarse coordinates and eta values on those same
branches. The common raw coarse error must be at least E=2P+32 in
v_beta, eta error at least E, and beta-ring precision at least 2P+64.
Transport errors must meet their P requirement. All sixteen harmonic
columns feed the present frame evaluator. The positive-order residual
balls for every quadric at all seventeen points must contain zero through
the propagated bounds. At P10480 these hypotheses suffice using orders
zero, one and two. The existing implementation also computes order three;
exact vanishing at that order is not needed for this implication.

These are statements about the actual curve, not jets generated from the
candidate. Neither the candidate's smoothness nor blind recognition of
small relations supplies a missing hypothesis in this table.

## 2. Why rank 45 suffices, with the coefficient field explicit

Consider multiplication

    mu : Sym^2_Q V -> H0(C0,2K).

Riemann–Roch gives dim H0(2K)=60+1-16=45. After tensoring with Q2,
take orders 0,1,2 at the certified nonanchor CM chart. Its residue field
has local degree 16, so expanding its coefficients gives a Q2-linear map

    J : Q2^136 -> Q2^48.

It factors as J=R o mu_Q2. Therefore rank(J)<=rank(mu_Q2)<=45.
The actual minor certificate gives rank(J)>=45. Equality follows
throughout, and R is injective on im(mu_Q2). Consequently

    ker(J) = ker(mu_Q2),       dim ker(J)=136-45=91.

This proves the needed implication without a separate application of
Max Noether's surjectivity theorem. A rational quadratic form whose
three actual coefficients vanish lies in ker(mu_Q2), hence in ker(mu)
by faithful scalar extension. It is a global canonical relation.

The rationality in this argument cannot be omitted. A one-dimensional
vector space over a degree-16 extension can have Q2-dimension 16;
one cannot use a dimension bound over that extension to bound the
expanded matrix rank over Q2. D106 supplies precisely the missing bridge.
The common scalar in the analytic frame multiplies the target by an
invertible Q2-linear map. Likewise, the saved nonzero block scalings and
an invertible change of local parameter preserve the kernel.

The [new rank replay](../pari/643_proof_criterion_controls.py) reconstructs
all 6528 entries of the actual 48-by-136 matrix twice, using convolution
in the Eisenstein quotient instead of the previous Horner implementation.
For each saved 45-by-45 minor B and integral matrix N it checks

    N*B = 2^13*I mod 2^t,          t=96 and t=160.

The coefficient errors cover these moduli. For the unknown exact matrix
B_true, N*B_true/2^13 is I plus a matrix divisible by 2^(t-13).
It is invertible because t-13>0, proving B_true invertible. This is a
certificate about the exact actual data, not the rank of a rounded
rational matrix. The remaining exponents are 83 and 147. A control shows
why t=13 would not suffice: B=0 and N=1 would pass the scalar congruence.

## 3. The section to which the height argument applies

Work over the CM Hilbert class field H and, where necessary, a stable
reduction extension. Here [H:Q]=272; the CM field M has degree 16 and
Gal(H/M)=C17. These fields differ from the degree-17 residue field L.
Let E be the integral stable differential lattice and W_i its canonical
fibre at CM point P_i. Put

    S = (tensor_i W_i)*(det E)^(-1),
    Phi = (c_i*e_i)_i : E -> S*ker(sum),
    Delta = det(Phi with one row deleted) = +/- product_i c_i,
    s_j = adj(Phi)*(sigma_i(17*eta_j))_i.

All c_i and Delta are nonzero on the generic fibre. The construction is
natural under the arithmetic CM permutation, up to a common sign.
For each candidate Q, exact vanishing on the CM frame gives the section

    q_Q = Q(s)/Delta  in H0(2*omega) tensor U,
    U = S^14*(det E)^(-1).

**Division by Delta is integral.** It is not justified by treating
Delta as a unit. To recall the algebra of
[D116, section 6](cm-compound-height-d116.md), write M0 for the sixteen
evaluation rows after deleting row zero, A=adj(M0), d=det(M0), v=e_0,
and c_i=-v*A_i. The cross terms of Q(sum X_i V_i) have coefficients q_ij
with no diagonal terms and sum q_ij=0, including the omitted frame point.
The numerator divided by the other cofactors is a sum of

    q_ij*T_ij,    T_ij=(product_{a not in {i,j}} c_a)*A_i*A_j.

For adjacent pairs, (T_ij-T_ik)/d is integral because its remaining
quotient is a contraction of (A_j wedge A_k)/d, an integral complementary
minor. Every two pairs can be joined in at most two steps. Subtracting
one reference T using sum q_ij=0 proves integral division universally.
The identity, rather than numerical divisibility in one completion,
allows all uncounted finite places to contribute nonnegatively.

This construction yields

    ||q_Q|| <= 480*42550*2^70*B^238,
    B=1/(sqrt(pi)*rho^2),       rho^2=3/5.

The exponent 238 is (16-2)(16+1), not an adjustable normalization.
The fresh check evaluates all 91 quadrics exactly in Q[theta]/(f),
rechecks their L1 maximum, and reproduces the bound |17*eta_j|<2^35
from the inherited root bound |theta|<4. Integrality of the saved field
basis and the embedded disk remain the prior algebraic/geometric inputs.

Suppose the lower coefficients through order n-1 vanish **exactly**.
The next divided derivative is an intrinsic integral element

    tau_n(q_Q,P_i) in W_i^(n+2) tensor U.

This remains valid when the section meets a node. For xy=a, use
lambda=dx/x=-dy/y and D_lambda=x*d/dx-y*d/dy. The operator
binomial(D_lambda,n) preserves the integral completed ring since its
eigenvalues on Laurent monomials are integral binomial coefficients.
It differs from D_lambda^n/n! only by lower derivatives, which vanish
on evaluation under the stated hypothesis. Changes of parameter or
generator also contribute only lower jets. Thus one must prove order
one zero before interpreting order two this way. A zero-containing
ball for order one is insufficient. Source 643 checks this distinction
using a nonlinear change of parameter and nodal divided derivatives.

## 4. Height, metric and finite-place normalizations

Write Hplus for the uniform CM-fibre height upper bound and Fminus
for the stable curve Faltings lower bound. The arithmetic line of tau_n
has degree at most

    (240+n)*Hplus - 15*Fminus.

Indeed h(S)<=17*Hplus-h(det E) and h(U)<=238*Hplus-15*h(det E).
The cofactor coefficients and the value of tau_n use these same lines;
there is no independent choice of a convenient projective scale.

The uniformization metric and small-level integral comparison are those
of [Yuan–Zhang, Theorem 4.7](https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n2-p04-p.pdf).
The CM formula uses their averaged height and nearby-pair identities,
whose named nearby height is half D104's sum of the two partial heights.
Their CM-point theorems excluding common finite ramification are not used.
The stable cover extension needed for the derivative comparison is
[Liu–Lorenzini, Proposition 4.4](https://www.math.u-bordeaux.fr/~qliu/articles/modcove.pdf);
it applies to our genera 40 and 16. It is a statement about stable models,
not arbitrary minimal regular models.

An additional source inconsistency occurs on page 25 of
[Zhao v1, Theorems 6.1, 7.3 and 7.4](https://arxiv.org/pdf/2309.08886).
The first proof display for 7.4 uses 1/(2g) before halving a squared-line
identity; its statement uses that coefficient after halving. Reading
the integral Kodaira–Spencer inclusion directly resolves the factor:
its index has absolute norm D=d_B*d_Sigma, so the normalized finite
degree is log(D)/g. Therefore

    2*h_L = 2*h_nearby + log(D)/g,
    h_L = h_nearby + log(D)/(2g) = -R/8 + log(2)/16,

where g=[F:Q]=8, D=2^18 and R=L_f'(0,chi)/L_f(0,chi).
The divisor notation in 6.1 corresponds to the integral inclusion into
L^2; reversing the ideal convention would give an incorrect sign.
This agrees with the theorem statement and D104's chosen bound.
It is our reconciliation, not an author-confirmed correction. D104 had
already identified a different dropped discriminant in the final proof
display of 7.5.

The inherited certified Hodge upper bound is

    hLplus = 31172134711534863111/18446744073709551616.

The local ramification derivative has integral content m_i-16, with
m_i=296 at the anchor and 33 at the other sixteen points. Consequently
its normalized finite content is (280+16*17)/272*log(2)=69/34*log(2).
Its archimedean norm is 2. Dropping only other nonnegative finite
contents yields exactly

    Hplus = 2*hLplus - (35/34)*log(2).

The tropical term and metric are checked against
[de Jong–Shokrieh, formula (1.11) and section 12](https://arxiv.org/pdf/1810.02637).
The curve determinant L2 metric agrees with their top-form metric;
the differently normalized CM Faltings metric is kept separate.
Nonnegative theta height, archimedean Jensen terms and remaining finite
terms can be discarded. With the actual graph length 76 and tau
67889/27075 in v_b units, conversion by v_b(2)=8 gives

    theta = (76/8 - (67889/27075)/2)/8 = 55817/54150,
    Fminus = -16*log(pi) - 8*log(2) + theta*log(2).

Combining the line degree with the section norm and product-jet Cauchy
constants C1=2*sqrt(2), C2=2*sqrt(3)+2 gives the nonzero finite-zero bound

    F_n = (240+n)*Hplus + (190-15*theta)*log(2)
          +120*log(pi)+log(480*42550)+log(C_n)
          +(240+n)*log(5/3).

Source 642 recomputes this collected expression with fresh rational
intervals; source 643 independently reconstructs the uncollected line
degree, tensor norm and jet functional using a different logarithm series.

The beta prime of M is principal of norm 2 and splits into seventeen
primes of H, each of residue degree 1 and ramification index 16.
The natural C17 action turns the seventeen values at one completion
into the valuations of one intrinsic value at those seventeen primes.
Thus lower bounds N at the sixteen nonanchor points and A at the anchor
contribute

    (16*N+A)*log(2)/272.

There is no additional ramification factor 16. The local degree-16
factor of L and the seventeen primes of H play different roles. Stable
base extension scales numerator and field degree equally. If this
finite contribution is strictly greater than F_n, the intrinsic value
cannot be nonzero by the arithmetic degree formula.

## 5. Error propagation, strict thresholds and sensitivity

The normalized nonanchor evaluation matrix has inverse entries of
valuation at least -35. Its input error is E-33, so inverse error is
at least E-103. The normalized anchor row has error E-296; the frame
relation entries have valuation -35 and error E-331. Their reciprocals
have error E-261. Combining with integral eta gives an integral frame
change with error at least E-296. These estimates use a strict Neumann
condition, comfortably met here, and sufficient precision of every
input. They do not assume future residuals will remain zero-containing.

The integral section conversion contributes
2*3920-4200-(n+2)*m_i. Hence

    N_n(P)=2P+3310-33n,
    A_n(P)=2P+2784-296n.

The exact test for a nonzero intrinsic jet is therefore contradicted by

    (P/8+(55744-824*n)/272)*log(2) > F_n.             (1)

At P10480 the required lower bounds are (N1,A1)=(24237,23448) and
(N2,A2)=(24204,23152). The table reports left side minus right side
of (1); decimal values are display approximations of rational enclosures.

| P | Order-one margin | Order-two margin | Both tests pass? |
| ---: | ---: | ---: | :--- |
| 1600 | -763.288714 | -769.224003 | No |
| 3200 | -624.659278 | -630.594567 | No |
| 6400 | -347.400406 | -353.335694 | No |
| 10472 | 5.411509 | -0.523779 | No |
| 10480 | 6.104656 | 0.169368 | Yes |
| 10552 | 12.342981 | 6.407692 | Yes |

The first sufficient multiples of eight are P10416 and P10480.
The older order-three test first succeeds at P10552. The shorter
recognized quadratic basis still needs P10480 for the two-order test.
These are minima for this uniform bound, not necessary precisions for
every possible proof. In particular, failure of (1) does not certify a
nonzero actual residual.

Each extra block of eight P units adds log(2) to the margin. A uniform
loss of d beta-digits from all seventeen final bounds subtracts
d*log(2)/16. At the second-order P10480 margin, d=3 still passes and
d=4 fails. The actual final error ledger must therefore be checked;
rounding to a nominal P label is insufficient.

The inherited height improvements are also material. With only the
finite-fibre content improvement removed, the common two-order target
would be P14408. With only the tropical Faltings gain removed, it would
be P10608. These diagnostics explain which geometric inputs support
the present target; they are not newly proposed computation schedules.

## 6. Finish the implication and define the future acceptance test

Order zero vanishes exactly by the rational CM-frame construction and
the exact field evaluations. Apply the strict height inequality first
to order one. Its vanishing, and Galois compatibility, supply the exact
lower-jet hypothesis for order two. Apply the inequality again. Every
one of the 91 quadrics now has zero actual coefficients in orders
0,1,2, so section 2 proves all are global canonical relations.

The canonical image lies on their common zero scheme. D69 proves that
scheme is a smooth geometrically integral curve X of degree 30, so the
nonconstant canonical image is X. The pullback of O_X(1) is K_C0.
Its degree is 30, hence

    30=deg(K_C0)=deg(C0 -> X)*deg(O_X(1))=deg(C0 -> X)*30.

The map has degree one. A finite degree-one map between smooth projective
curves is an isomorphism. The equality of the specified CM frame also
identifies D0. This last argument does not require an additional
nonhyperellipticity assumption, although D99 is used in the inherited
rational-descent proof. P32/B3 labels, the explicit upstairs cover and
the eventual torsion field remain separate tasks.

A successful future run must leave a reviewable certificate containing:

1. Certified actual input solutions, matching, eta values, fibre scales
   and a complete error ledger for the frame and quadratic evaluation.
2. Zero-containing residuals for each of the 91 quadrics at all seventeen
   CM points in the two positive orders, with certified lower bounds.
3. Strict rational finite-degree inequalities, followed in order by
   exact order-one and order-two vanishing.
4. The authenticated actual rank minor and candidate scheme certificate,
   with the field-of-definition and geometric deductions above.

An excluded-zero residual would refute that candidate in those certified
coordinates. An insufficient error bound or failed inequality would leave
the test inconclusive. Neither outcome should be recorded as successful
identification merely because the precision computation finished.

Sources 642–643 are new finite checks; source 644 authenticates their
receipts and replays the inherited D154 provenance graph with a fresh
fixed review. The completion record records resources, passing job count
and entry-document links. Existing passed reports, sources and precision
stores remain frozen. Full-bank precision is still P1600, column 0 is
P6400 and column 2 is P3200. D154's timing and storage limitations remain;
this proof review authorizes no larger computation.
