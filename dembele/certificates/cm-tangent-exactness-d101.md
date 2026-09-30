# D101: exactness of the first CM tangent

Date: 2026-09-24. Execution of the first bounded task in D100 section 7.

**Outcome:** the tangent has a useful algebraic reformulation, and there
is now an explicit conditional height/separation certificate. Its
arithmetic hypotheses have not been instantiated on the Shimura curve.
In particular, there is still no proved numerical tolerance at which
our analytic output would certify the proposed tangent. Another
spectral-bound pilot is not yet justified by this exactness review.

The new exact computation constructs the tangent of the saved candidate
over its degree-17 point field. It supplies a comparison value and checks
the verification machinery; it is not an independent Shimura tangent.

## 1. Replace tangent derivatives by algebraic tricanonical sections

Let C/F be a smooth curve, and let omega_1,...,omega_16 be the intended
arithmetic canonical frame. Choose b with omega_b(D) nonzero and set
r_j=omega_j/omega_b. In a local coordinate u, write omega_j=f_j(u)du.
The first Gaussian map is

    gamma : wedge^2 H0(C,K_C) -> H0(C,3K_C),
    G_ij = gamma(omega_i wedge omega_j)
         = (f_i f'_j - f_j f'_i) (du)^3.

This standard algebraic map is described, for example, in
[Aprodu et al., Gaussian maps](https://link.springer.com/article/10.1007/s00029-023-00912-4).
Our application is the following identity:

    G_bj = omega_b^2 d(r_j),
    v_j = (d r_j / d r_a)(D) = G_bj(D)/G_ba(D).

It requires G_ba(D) nonzero. Both numerator and denominator lie in the
same one-dimensional fibre, so their ratio does not require a chosen
CM period. Their arithmetic origin and common normalization still
have to be proved.

The formula glues: under u=h(z), differential coefficients become
f_j(h(z))h'(z); their bracket becomes h'(z)^3 times the old bracket.
The terms involving h'' cancel. Multiplication of all local differential
coefficients by a common function g multiplies every bracket by g^2,
which also cancels in the ratios. These are polynomial identities,
not numerical approximations.

At the order-two point u=z^2, the upstairs coefficient is

    G_up(z) = 8*z^3 * G_coarse(z^2).

Thus the vanishing upstairs is compatible with a nonzero coarse
tricanonical value. One must extract the leading coefficient or evaluate
on the coarse curve; substituting z=0 into G_up would lose the tangent.
This recovers D89's need for the z and z^3 differential coefficients.

For genus 16 the Gaussian map has source dimension 120 and target
dimension 75; deg(3K_C)=90. An arithmetic alternative to analytic
derivatives is consequently to evaluate the fifteen sections G_bj at
D in a common fibre and divide by a verified nonzero G_ba. Specifying
this map does not compute its entries. Hecke eigensystems by themselves
do not supply the Gaussian map or its evaluations.

## 2. The precise norm certificate

Let L be a proved field containing an actual tangent coefficient alpha
and the proposed coefficient beta. Write d=[L:Q]. Suppose a positive
integer M is independently proved to satisfy

    M*(alpha-beta) in O_L.

If every complex embedding sigma has a certified upper bound
E_sigma >= |sigma(alpha-beta)|, then

    M^d * product_sigma E_sigma < 1

proves alpha=beta. Otherwise the norm of the nonzero algebraic integer
M*(alpha-beta) would be a nonzero rational integer of absolute value
less than one. Count all d embeddings; a complex conjugate pair
contributes twice. Equality at the threshold is insufficient.

More generally, if an integral ideal a satisfies
alpha-beta in a^(-1), replace M^d by Norm(a). The product bound follows
from the nonzero integral ideal (alpha-beta)*a. A common integer is
convenient but can be much less efficient than a denominator ideal.

**Useful refinement of D100:** with enclosures at every embedding and
a proved denominator bound, a separate archimedean height bound is
unnecessary. Uniform E_sigma<1/M is sufficient. With only one evaluated
embedding and bounds |sigma(alpha-beta)|<=B_sigma at the others, the
sufficient tolerance is instead

    E_sigma0 < 1 / (M^d * product_(sigma != sigma0) B_sigma).

The saved candidate coefficient field has degree 17 over Q. Working
only over F does not justify assuming that degree for the unknown
coefficient. If the proposed identification F(D)=F*L0 is established,
where L0 is the degree-17 candidate field, its absolute degree is 136:
the degrees 8 and 17 are coprime. All-embedding evaluation would then
have to cover those 136 embeddings, or separately justify a descent.
The current calculation at one real place of F does not supply them.

Neither algebraicity, a fixed field, nor control of the allowed
denominator primes supplies the missing bound. For example, if theta
generates the known degree-17 field, then

    alpha_n = theta + 2^(-n)

generates that same field and is integral outside 2. Its conjugates are
bounded independently of n, and all are arbitrarily close to the
corresponding conjugates of theta. Yet alpha_n is never theta. This
is a counterexample to an inference from those inputs alone, not a
claim that these numbers are possible tangents of our fixed curve.

## 3. A conditional height bound, with the missing constant exposed

Here is an alternative when one cannot evaluate every embedding. Fix
an integral arithmetic model, a metrized extension of K_C, and an
actual arithmetic representative of the CM frame. Suppose an integral
ideal a of O_F clears its sections, so that every omega_j lies in
a^(-1)H0(K_C), and that the Gaussian map is integral on the chosen
extensions. Any corrections needed at bad fibres must be included in
these hypotheses. Then G_ba and G_bj are integral sections of

    3K_C tensor a^(-2).

For an L-valued point D where G_ba is nonzero, the elementary
projective-height inequality gives

    h(v_j) <= 3*h_K(D) + (2/[F:Q])*log Norm_F(a)
               + (1/d)*sum_sigma log U_(j,sigma),

where U_(j,sigma) bounds
max(||G_ba(D)||_sigma, ||G_bj(D)||_sigma) for that same arithmetic
normalization. To prove it, trivialize the one-dimensional fibre over
L. The common finite zero divisor of two integral sections has
nonnegative degree; subtracting it from the fibre's Arakelov degree
and adding the archimedean log maxima gives h([G_ba:G_bj]). Dropping
the common zero divisor gives the displayed upper bound.

If the right side is bounded by B and h(beta)<=B0, then

    |sigma0(alpha-beta)| < exp(-d*(B+B0+log(2)))

also forces equality. Indeed h(alpha-beta)<=B+B0+log(2), and the
product formula gives |sigma0(delta)|>=exp(-d*h(delta)) for nonzero
delta in L. These bounds are sufficient, not optimal.

**The missing input is now specific:** we do not have the ideal a and
compatible arithmetic-normalization/metric bounds U for the actual
CM-framed sections, or the complete comparison of h_K(D) with an
available arithmetic CM-height formula. Replacing them by the values
on our candidate would assume the identification being tested.

The residue construction makes the finite-place issue particularly
visible. Conditional on H0(K_C-D)=0 and the correct arithmetic CM label,
the frame over F uses the isomorphism

    (H0(O_C(D))/F) tensor H0(K_C) -> ker Tr_(L/F),
    h tensor omega |-> Res_D(h*omega).

Its integral counterpart involves the lattice in H0(O_C(D))/F, the
appropriate residue/dualizing lattice of the horizontal divisor, and
the cokernel of the restriction map. A generic-fibre isomorphism does
not bound that cokernel. Even at good primes, marked sections can
collide or a restriction map can lose rank. Knowing the discriminant
of the abstract point field is not a proof that these defects vanish.
No global bound on this framing index has been supplied by the saved
numerical frame or by the Hecke-module calculations.

## 4. What the newly reviewed height sources actually provide

[Roy Zhao, Theorem 1.1](https://arxiv.org/pdf/2309.08886) expresses the
intrinsic arithmetic Hodge height of a CM point at maximal compact
level in terms of CM Faltings heights and discriminants. Its hypothesis
requires the CM extension to ramify wherever the quaternion algebra
ramifies finitely. That ramification pattern matches our data at 2.
This is a relevant potential input to the preceding inequality, not
a bound already expressed in our canonical frame. The level, metrics,
normalizer quotient and coarse canonical bundle still need comparison.

[Xinyi Yuan, Theorem 1.1 and section 1.1](https://arxiv.org/pdf/2205.13995)
give the modular height of the quaternionic Shimura curve, again with
specified arithmetic Hodge-bundle normalization. This may help an
arithmetic Riemann–Roch or lattice comparison. **The CM-point formula
quoted as Theorem 1.2 has a different restriction:** it excludes a
finite place ramified in both the CM extension and the quaternion
algebra, so that formula cannot be applied directly here.

The common ramification is exact, not a numerical guess. The polynomial
of F is 2-Eisenstein. Substituting b=-beta^2-2 gives

    beta^16+16 beta^14+104 beta^12+352 beta^10+660 beta^8
      +672 beta^6+336 beta^4+64 beta^2+2,

also 2-Eisenstein. Thus the local degrees over Q_2 are eight and
sixteen, respectively, and the quadratic CM extension is ramified
over F at its unique dyadic place. The quaternion algebra is ramified
there by construction. Audit 377 replays the substitution and both
Eisenstein checks.

These papers supply intrinsic height identities, not the missing
integral canonical-section lattice in our coordinates. This review
does not show that such a comparison cannot be derived. It identifies
the additional arithmetic argument needed before the formulas yield
a usable recognition bound.

## 5. The arithmetic-restriction alternative

Zhao's sections 3–7 construct the related PEL setting, the relevant
deformations and the Kodaira–Spencer comparison. The CM test point is
related to a product of CM abelian varieties. These structures give a
possible setting for an arithmetic evaluation of omega_j and G_bj.
They do not turn our saved Brandt eigenvectors into values of those
global sections.

[Guo, sections 2.2–2.3](https://arxiv.org/pdf/2606.18579) also carefully
distinguishes the PEL RSZ integral model used for computations from
the original non-PEL Shimura variety and its normalized heights. We
cannot treat the existence of an auxiliary moduli space as an already
specified integral equation or evaluator for our quotient C.

For an exact restriction approach the remaining concrete inputs are:
the arithmetic CM test object with its polarization and level, descent
to the required quotient, and the restrictions of the sixteen actual
canonical sections together with their Gaussian brackets. Constructing
only a deformation parameter or only a Hecke module does not provide
them. Once available, the ratios in section 1 give an exact tangent
without a height-recognition step. No such map was constructed in this
bounded investigation.

## 6. Exact candidate calculation and controls

New Magma [375](../magma/375_cm_tangent_candidate_height.m) uses the
saved rational quadrics and exact degree-17 point. The projective
Jacobian has rank 14. Adding the conditions v_1=0 and v_2=1 determines
the unique tangent in the chart X1=1 with parameter
t=X2/X1-(X2/X1)(D). Its output is exact in Q(theta).

The least common denominator of its coordinates in the saved integral
lattice has **269 decimal digits**; the power-basis denominator has
285. Magma checks integrality of the lattice generators using their
minimal polynomials and checks their trace discriminant. Maximality of
the lattice is not needed for the stated clearing integer. All sixteen
tangent coefficients are saved in the
[D101 artifact](../data/computed/cm_tangent_exactness_d101.json).

The checker also proves |theta|<4 at every embedding and stores a
rational conjugate bound B_j^cand from each coefficient polynomial.
With the clearing integer M_cand this gives the usable candidate-only
bound h(beta_j)<=log(M_cand)+log(max(1,B_j^cand)). The corresponding
bound for the unknown arithmetic coefficient remains missing.

This demonstrates that low-degree equations and a first-order tangent
need not give small rational coordinates in the chosen normalization.
It is not a height bound for the actual Shimura tangent, a minimum
precision requirement, or an exclusion of better parameter choices
or denominator-ideal certificates.

The independent standard-Python checker
[376](../pari/376_cm_tangent_exactness.py) replays all 91 quadric
identities and linearizations using integer polynomial arithmetic.
It verifies the integral-basis conversion, the clearing integers,
agreement with D88 modulo 31, and uniqueness by a fresh finite-field
rank calculation. A corrupted tangent coefficient is rejected. Exact
polynomial controls check the Gaussian covariance, the 8*z^3 quotient
factor, and the strictness/integrality requirements in norm separation.

The Magma job passed in 8.81 seconds under the 180-second process-group
limit and 2 GB Magma cap. Initial collection failed because a parser
expected single-line sequences; the failed source and failure record
are preserved. Collection was repaired and used the same successful
arithmetic log. The bounded independent recheck passed in 1.92 seconds.
No cubic precision, Hecke bank or quaternion enumeration was increased.

Recheck the candidate and formal controls with:

```sh
python3 dembele/pari/376_cm_tangent_exactness.py --check
```

The review audit additionally binds the report and source ledger:

```sh
python3 dembele/pari/377_cm_tangent_exactness_review.py --check
```

The audits verify computations and provenance, not the cited theorems
or the unproved arithmetic hypotheses. Completed sources 375–377 and
their bound results are frozen after the review audit is generated.

## 7. Decision after this first execution

The first bounded investigation is complete. It did not establish the
exactness mechanism's arithmetic inputs, so it does not pass the gate
for resuming numerical tangent extraction. No independent tangent has
been computed or compared, and the candidate has neither been
identified nor refuted.

The next mathematical task is an explicit comparison of the residue
frame with an integral canonical-section lattice, including a bound
on its finite index and compatible archimedean norms. The height
formulas above are potential inputs; applying their intrinsic bounds
directly to tangent coordinates would skip this task. The alternative
is to construct the Gaussian-section restriction map from actual
arithmetic moduli data. The all-embedding norm certificate offers a
way to avoid a separate height bound if a global denominator bound
can be obtained first.

Keep D98's analytic accuracy, the global cubic, and target-scale
torsion as separate open tasks. More precision does not settle this
newly specified arithmetic comparison.
