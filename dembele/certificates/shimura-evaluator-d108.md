# D108: reject an insufficient spectral comparison and specify a dyadic jet evaluator

Date: 2026-09-25. Continuation authorized by “continue”.

**Result.** Completing the Mellin integral cannot make D98's current
per-ideal absolute spectral comparison certify the CM anchor. The
seven omitted primes of norm 31 alone force that comparison above
**460891.49**, more than **60.32** times the saved partial sum.
This statement allows the best power kernel, or any positive mixture
of them, while retaining the absolute Hecke envelopes and unsigned
geometric diagonal bound specified below. It is a lower bound on
this comparison method, not on the actual omitted sum.

For a direct dyadic alternative, we prove an explicit conditional
moment-to-jet formula at the ramified CM point. Moments through
index J with absolute precision P and measure bound v(mu(B))>=-d
give the first three **coarse differential coefficients** with error

    v(error) >= min((J+1)/2-d, P),       v(pi)=1, v(2)=8.

Exact synthetic controls in the actual degree-16 CM field pass.
**No actual harmonic cocycle, moment bank, Shimura tangent or jet
was computed.** The local formula becomes an evaluator only after
the arithmetic group, CM embedding and actual moments are supplied.
Candidate identification and the target polynomial remain open.

## 1. A necessary condition for the completed spectral comparison

Use the unchanged kernel and conventions of
[D98](nelson-spectral-ideal-d98.md). With lambda=mu*(1-mu), its
completed multiplier is

    H_N(mu)=(4*pi/N)*integral_(2)
      (2*s-1)*Gamma(s)^14*s^7*C(s)*(lambda+2)
      *Gamma(s+1-mu)*Gamma(s+mu)*(Z0*N)^(-s) ds/(2*pi*i),

    Z0=(4*pi^2)^8/2^62,
    C(s)=zeta_F(2*s)*(1+2^s)/(1-2^(-s-1)).

The lowest-weight-four discrete series mu=2 is killed. The surviving
lowest-weight-two series mu=1 has lambda=0. Gamma recurrence
([DLMF 5.5.1](https://dlmf.nist.gov/5.5.E1)) therefore gives exactly

    H_N(1)=8*pi/N*K1(Z0*N),
    K1(z)=integral_(2) (2*s-1)*Gamma(s)^16*s^8*C(s)*z^(-s) ds/(2*pi*i).

This is D91's same K_k family at k=1. It retains all scalar Mellin
cancellation, before taking an absolute value.

[Script 394](../pari/394_nelson_discrete_multiplier.py) uses 320-bit
Arb arithmetic, mesh 1/32, height 16 and a strip of half-width one.
The Gamma-polynomial, zeta and trapezoid bounds of D91 apply also
at k=1. A separately enclosed mesh-1/16 rule overlaps. The values are

| N | K1(Z0*N), approximately | H_N(1), approximately |
|---:|---:|---:|
| 1 | 2372.85367844864739 | 59636.31747406230512 |
| 31 | 571.08737332255191 | 462.99971524852148 |

The saved intervals have width below 10^-25. The rational audit
reconstructs a more conservative width below 10^-40 from the finite
quadrature centers. It bounds exponentials using e>8/3 and verifies
pi independently by Machin's identity and alternating arctangent
series. The transcendental centers themselves remain bound to the
Arb run; Python does not independently re-evaluate all Gamma/zeta nodes.

## 2. Why optimizing the comparison kernel cannot remove this floor

D98 compares against the positive transform of Phi*D^(-p), p>2.
On the surviving discrete series,

    h_p(1)=4*pi*(p-2)/(p*(p+1)).

Its global maximum over p>2 is

    h_max=4*pi*(5-2*sqrt(6))=1.26946122402638818...,
    attained at p=2+sqrt(6).

For an exact algebraic proof, set t=5-2*sqrt(6), a=2+sqrt(6).
Then t>0 and

    t*p*(p+1)-(p-2)=t*(p-a)^2 >= 0.

Suppose a proposed uniform bound satisfies

    |H_N(mu)| <= A_N*h_p(mu)

on the whole required spectrum. Necessarily

    A_N >= |H_N(1)|/h_p(1) >= |H_N(1)|/h_max.                 (1)

The **unsigned geometric diagonal bound** used in D98 is an upper
bound for C_p obtained by summing |Phi(gamma)|*D(gamma)^(-p).
It includes the identity contribution one, hence is at least one.
This is a property of that upper bound. We do not claim C_p itself
is at least one, or that no more effective diagonal estimate exists.

The same argument applies to any positive mixture of these kernels:
its unsigned diagonal bound is at least the sum of its coefficients,
while its value at mu=1 is at most h_max times that sum. Scaling the
comparison kernel therefore does not evade (1).

The F polynomial splits into eight distinct linear factors modulo 31.
Only one of those primes appears in D93's saved families. At each of
the other seven, the retained absolute Hecke envelopes give the weight

    (2*sqrt(31))*(2*31^(1/2+delta))=4*31^(1+delta),
    delta=7/64.

Consequently the proposed comparison for all omitted ideals is at least

    7*4*31^(1+delta)*|H_31(1)|/h_max
       =460891.49560063327898... > 60.32*7640.7581837028... .  (2)

Even replacing delta by zero leaves a floor above 316578.20, more
than 41 times the partial. No infinite-tail computation can reduce
a sum of these nonnegative majorants below its seven-prime subsum.
The unchanged saved-family error also exceeds the partial: it is
9626.29908949.... Thus (2) fails even the more favorable test in
which that saved-family tail has been computed exactly.

This is a rigorous **rejection test**, not a full-spectrum upper-bound
pilot. One required spectral parameter suffices to reject a proposed
uniform majorant; point samples would not suffice to validate one.
It is not an impossibility theorem for Nelson's method. Joint Hecke
cancellation across ideals, a different comparison with a sharper
diagonal estimate, or changed residue weights are outside this result.
No new full error enclosure replaces D98's old one.

**Decision:** do not build the expensive full-spectrum version of this
particular per-ideal absolute comparison, or repeat its contour scan.
A complex-route restart must identify the additional cancellation or
diagonal information that changes the hypotheses of (2).

## 3. Direct dyadic evaluation: the arithmetic input it would need

A weight-two harmonic cocycle on an actual finite arithmetic tree
quotient determines a bounded measure mu on P1(K), with total mass
zero, where K=F_p at the unique dyadic prime. Its Poisson differential is

    omega=f(z) dz,       f(z)=integral_(P1(K)) dmu(t)/(z-t).    (3)

The residue on an oriented boundary annulus recovers the mass of its
boundary ball. This can be seen by expanding 1/(z-t) in that annulus:
the coefficient of z^(-1) from the inside ball is mu(B), while the
outside contribution has no residue. The orientation convention must
be recorded in the implementation.

In weight two, the transformation law is elementary. For gamma with
bottom row (c,d), invariance of mu and total mass zero give

    gamma'(z)/(gamma(z)-gamma(t))
       =1/(z-t)-c/(c*z+d),
    f(gamma(z))*gamma'(z)=f(z).

Boundedness and the convergent local series below justify integration
and differentiation. This calculation is valid over the ramified K;
it does not assume K=Q2 or an unramified CM point.

For the computational framework, see
[Franc--Masdeu, section 6.1](https://arxiv.org/pdf/1201.0356).
Their overconvergent implementation is over Q_p. The updated arXiv
version also corrects the identification with the full automorphic
space: harmonicity imposes the appropriate U_p eigencondition.
We do not apply its control theorem or software unchanged to our
ramified degree-eight field.

[Masdeu--Torrents, section 3](https://arxiv.org/pdf/2510.09356)
provides a tree-domain algorithm over general totally real fields.
It requires a definite order, an integral local splitting and
certified vertex/edge equivalence witnesses. Its
[implementation repository](https://github.com/Eloitor/btquotients)
advertises general number-field input and testing with Sage 10.9.
We inspected the paper and public documentation, not a pinned source
checkout or a running implementation. No compatibility or performance
claim for this degree-eight dyadic case is made.

The existing local HMF source supplies a useful entry point:
`InternalHMFRawDataDefinite` exposes `RightIdealClassReps`, while
`QuaternionOrder(M)` obtains the order. Its level-one `SplittingMap`
field must not be assumed to be the required dyadic integral splitting.
The saved D99 exports contain the Brandt matrix and stabilizer orders,
not actual boundary matrices and edge transports. The graph alone
cannot evaluate (3).

## 4. Three charts at the ramified CM point

Both polynomials

    P_F(x)=x^8-8*x^6+20*x^4-16*x^2+2,
    P_M(x)=P_F(-x^2-2)

are Eisenstein at 2. Set pi=b=-beta^2-2 in the corresponding local
fields. The normalized valuation is

    v(pi)=1,       v(2)=8,       v(beta)=1/2.

In particular K has residue field F2 and K(beta)/K is ramified
quadratic. Any identified quadratic CM embedding can be put in
coordinates with fixed point z=beta; that coordinate change and
the identification with the actual marked point still need witnesses.
D107's complex matching does not provide a dyadic embedding matrix.

The three compact-open boundary charts are, for x in O_K,

    A: t=pi*x,
    B: t=1+pi*x,
    C: t=1/(pi*x),     x=0 denotes infinity.

They partition P1(K). Write A_r,B_r,C_r for the moments of the
three pullback measures against x^r. Suppose v(mu(B))>=-d for every
compact-open ball, with d>=0. Then all chart moments have valuation
at least -d. A finite, equivariant weight-two cocycle can supply
such a bound, once the actual orbit representatives are known.

Write f(beta+delta)=sum_(k>=0) f_k*delta^k. The exact expansions of
(3) give

    f_k = (-1)^k*beta^(-k-1)
            *sum_(r>=0) binom(k+r,r)*(pi/beta)^r*A_r
        + (-1)^k*(beta-1)^(-k-1)
            *sum_(r>=0) binom(k+r,r)*(pi/(beta-1))^r*B_r
        - pi^(k+1)
            *sum_(r>=0) binom(k+r,r)*(beta*pi)^r*C_(k+r+1).  (4)

The third sign is negative for every k. The three series ratios have
valuations 1/2, 1 and 3/2, respectively. All binomial coefficients
are integral. Thus (4) converges uniformly, including at p=2.

Suppose moments through index J>=k are known to absolute precision
P: the error in each supplied moment has valuation at least P.
Truncate the first two sums at r=J and the third at r=J-k-1,
interpreting an empty sum as zero. The omitted terms have valuations
at least

    (J-k)/2-d,       J+1-d,       (3*J-k)/2+1-d.

The first is the smallest. Error in the supplied moments has
valuation at least P-(k+1)/2. Therefore

    v(error in f_k) >= min((J-k)/2-d, P-(k+1)/2).             (5)

This assumes exact coefficients in (4), or validated local-field
arithmetic that separately encloses their rounding errors. An
approximate CM coordinate with no error bound is not sufficient.

## 5. Coarse coefficients without an unaccounted dyadic division

At an order-two fixed point use

    w=(z-beta)/(z+beta),     z=beta*(1+w)/(1-w),     u=w^2.

The order-two action z -> beta^2/z sends w to -w. A descended
differential has odd pullback coefficient phi(w): omega=phi(w)dw.
If omega=sum_(j>=0) g_j*u^j du, then

    g_j=phi_(2*j+1)/2
       =beta*sum_(k=0)^(2*j+1)
             (2*beta)^k*binom(2*j+2,k+1)*f_k.               (6)

The initial factor two in dz/dw has canceled the division by two.
The coefficient multiplying f_k in (6) has valuation at least
(1+17*k)/2. Combining this with (5), for j=0,1,2 and J>=5,

    v(error in g_j) >= min((J+1)/2-d, P).                    (7)

Thus it is sufficient to take J>=max(5,2*(N+d)-1) and P>=N to
obtain these three coarse coefficients modulo valuation N. The units
are uniformizer digits: N=16 corresponds to just two binary digits,
not sixteen. This is a local input/output bound, not a feasibility
estimate for producing actual moments at identification precision.

[Script 395](../pari/395_dyadic_poisson_jet_interface.py) checks (4)--(7)
on a synthetic measure with masses 1,-2,1 at pi,1+pi,1/pi, scaled
in one control to test denominator loss. It compares with direct
rational functions in M and independently expands z(w). Taking the
odd part gives an invariant differential for this synthetic control;
it is not a Shimura differential. Four controls use J=7,15,15,31,
including deliberately perturbed moments.

The first run required a sign corruption to be visible at every
precision. That assertion failed correctly: changing a sign introduces
a factor 2, of valuation eight. The corrected controls detect the
sign error at J=31, where it is visible, and reject omission of the
infinity chart in all four cases. The original failure, source and
receipt are preserved. No result artifact was produced by that failure.

## 6. Execution decision and next bounded task

Prioritize a direct dyadic moment evaluator. The next concrete
prerequisite is to export the actual definite order and construct
a certified integral splitting into M2(O_K), then produce and verify
one dyadic vertex/edge transport witness. Reuse the existing 58-class
arithmetic data where possible. This is a bounded order/local-algebra
task, not authorization to launch a full new tree or quaternion census.

Before an actual jet is claimed, the implementation must also:

1. identify the arithmetic tree group and normalizer quotient with
   the intended curve, including stabilizers and level structure;
2. construct its actual invariant harmonic cocycles and a bound d;
3. match the seventeen dyadic CM embeddings with the rational residue
   frame, using explicit CM and reciprocity witnesses;
4. produce moments with a proved error/contraction bound over this
   ramified field, then apply (4)--(7) with certified field arithmetic;
5. propagate errors through the cofactor normalization and certify
   a Gaussian pivot before forming ratio jets.

The elementary tails proved here do not prove convergence of a
ported overconvergent lift. Nor does a Brandt eigenvector by itself
supply the boundary transport maps. Direct Riemann refinement has
exponential growth and is unsuitable as the high-precision plan.

D106's inert-31 equality thresholds cannot be reused numerically as
dyadic thresholds. Once an actual dyadic frame and evaluator exist,
the height argument must use the chosen dyadic local degree and
valuation normalization. No identification-precision run is justified
yet. Preserve the existing enumeration, Hecke-bank and cubic-precision
pauses. The complex route remains possible if the comparison method
is changed as specified after (2).

## 7. Audit and reproduction

The completed discrete-series calculation passed in 7.47 seconds.
The corrected dyadic controls and independent rational probe passed
in 2.97 and 0.09 seconds under the existing 180-second
private-process-group cap.
[Review 396](../pari/396_shimura_evaluator_review.py) checks every one
of D107's 588 source hashes unchanged, binds the new sources and
receipts, and replays the rational bounds and formal transformations.
It also binds this report and the
[source ledger](../data/computed/shimura_evaluator_sources_d108.json).

```sh
python3 dembele/pari/396_shimura_evaluator_review.py --check
```

The analytic proofs are mathematical arguments, not machine-verified
theorems. No new arithmetic harmonic measure or actual differential
value is hidden in the synthetic controls. Completed sources 394--396
and bound artifacts are frozen after the final review.
