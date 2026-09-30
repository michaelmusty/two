# D117: uniform CM disks and the remaining arithmetic exactness gap

Date: 2026-09-26. This continues the authorized D115--D116 reassessment.

The uniform disk estimate can be improved substantially. An exact search
in the CM integer lattice proves that every moving normalizer translate
of every order-two CM point has displacement greater than 2*acosh(4).
Consequently the centered open disk with **rho^2=3/5** embeds modulo
the order-two stabilizer, at all seventeen points and all conjugates.
This replaces D103's rho=2^-10 without another group or class census.

Combined with D116's integral complementary-minor formula, the sufficient
successive non-anchor beta-valuations become **35947, 36096, 36237**.
The actual lower bounds remain **3794, 3745, 3728**. No positive-order
jet is proved exactly zero, the candidate is not identified, and the
target field polynomial remains unconstructed.

Even formally setting rho=1, with all other inputs to this bound fixed,
leaves sufficient thresholds **32928, 33064, 33193**. This resolves the
radius-refinement branch of the plan: further improvement of that input
alone cannot certify the present data. It is not a lower bound on the
precision required by every possible proof.

## 1. Fixed arithmetic and geometric inputs

Use the actual arithmetic curve, CM divisor, integral differential
lattice and rational frame from D99 and D103--D116. In particular,

    F=Q(b),   b^8-8*b^6+20*b^4-16*b^2+2=0,
    M=F(beta),   beta^2=-(2+b),
    disc(F)=2^31,   disc(M)=2^79.

The quaternion algebra is split at one real place and definite at seven.
Each relevant maximal order O contains its CM beta. Conjugation by beta
normalizes O: beta is a unit away from the dyadic place, and the maximal
order in the dyadic division algebra is unique. The norm-one group
Gamma^1 has index two in Gamma^+, represented by beta. Since beta fixes
the CM point p, Gamma^1*p=Gamma^+*p. D103, section 4, supplies these facts
uniformly, including their transport under canonical conjugation. The
split place is transported with the algebra.

The full integer rings used below follow from the discriminants already
certified in D104--D105. The monic triangular bases have determinants
equal to those discriminants. An integral element in the embedded M
therefore belongs to the enumerated lattice. No converse assertion that
every enumerated lattice element arises from a quaternion unit is used.

## 2. A first displacement bound from the real trace lattice

For alpha in O^1, decompose

    p_alpha=(alpha+beta*alpha*beta^(-1))/2,
    q_alpha=(alpha-beta*alpha*beta^(-1))/2,
    v=Nrd(q_alpha).

The two summands are orthogonal for the reduced norm, with
Nrd(p_alpha)+v=1. At the seven definite places 0<=v<=1. At the
distinguished split place, when alpha moves p,

    v=-sinh(d(p,alpha*p)/2)^2.

The element gamma=alpha*beta*alpha^(-1)*beta^(-1) is an integral
norm-one unit. Its trace is

    t=Trd(gamma)=2-4*v.

Thus seven conjugates of t belong to [-2,2], and the remaining one is
2*cosh(d)>2. These are necessary conditions on a moving unit.

Set T_0=2, T_1=b and T_k=b*T_(k-1)-T_(k-2). The integral basis
1,T_1,...,T_7 has trace Gram matrix diag(8,16,...,16). If the outlying
conjugate of t were at most 8, then

    Tr(t^2)<=8^2+7*2^2=92,
    a_0^2+2*sum_(k=1)^7 a_k^2<=11.

Source 446 enumerates all 6167 vectors in this weighted ball. Root
isolation by rational Sturm intervals and outward interval evaluation
show that all eight eligible single-positive-outlier elements have
outlier strictly greater than 8. Therefore t>8 for a moving unit.
This already certifies rho=9/19 and gives preliminary thresholds
41761/41934/42099 in source 447. Those artifacts remain frozen.

## 3. The stronger integral CM projection

Consider instead

    x=alpha+beta*alpha*beta^(-1)=2*p_alpha.

This lies in O, commutes with beta, and hence is an algebraic integer
in M. At each of the seven definite CM places its squared absolute
value is at most 4. At the distinguished place it is

    |x|^2=4*cosh(d(p,alpha*p)/2)^2>4.

Write P_0=2, P_1=beta, P_k=beta*P_(k-1)+P_(k-2). Then

    P_16=beta^16+16*beta^14+104*beta^12+352*beta^10
         +660*beta^8+672*beta^6+336*beta^4+64*beta^2+2=0.

The monic triangular basis 1,P_1,...,P_15 has Hermitian trace Gram
matrix diag(16,32,...,32), of determinant 2^79. If the exceptional
squared absolute value were at most 64, we would have

    Tr_M/Q(x*conjugate(x))<=2*(64+7*4)=184,
    a_0^2+2*sum_(k=1)^15 a_k^2<=11.

Source 448 enumerates all **376935** vectors. Write each x as r(b)+beta*s(b)
and evaluate r(b)^2+(2+b)*s(b)^2 at the eight isolated real roots. All
operations and comparisons use exact integers and rational intervals.
Sixteen elements have exactly one squared absolute value greater than
4 and all others at most 4. Every one of these outliers is strictly
greater than 64. The only unresolved interval boundaries at 4 are
x=+/-2, whose norm is identically 4 and which cause no displacement.
There is no element satisfying an outlier in (4,64]. It follows that

    d(p,alpha*p)>2*acosh(4)

for every moving unit. The proof is uniform in the CM embedding and
the distinguished real place; the enumeration allows any of the eight
places to be the outlier.

The hyperbolic radius R of |z|<rho is 2*atanh(rho). For rho^2=3/5,

    cosh(R)=(1+rho^2)/(1-rho^2)=4.

Thus 2R is strictly below every nonzero displacement. The open disk
embeds in the normalizer quotient modulo z->-z. This argument does
not claim that disks about different CM points are mutually disjoint.
It gives the individual embedded disks needed for the coefficient norms.

Review 450 independently enumerates both balls by support patterns,
checks the Gram matrices using multiplication-matrix traces instead of
Newton sums, verifies eight disjoint root sign changes instead of using
Sturm, and evaluates the basis by recurrences instead of polynomial
Horner evaluation. It finds the same eight and sixteen eligible vectors.
Twenty-seven rational SL2 controls check the projection/displacement
identities; their general geometric justification is the argument above
and D103's split and definite quaternion decompositions.

## 4. Combine the norm and height estimates before rounding

The centered coordinate z, coarse coordinate u=z^2, and metric ||du||=1
are unchanged. Increasing the embedded radius does not rescale the
arithmetic fibre line. The coefficient functional a_k has norm at most

    sqrt(k+1)/(sqrt(pi)*rho^(2*k+2)).

Let B=1/(sqrt(pi)*rho^2), V=2^35, and L=max_Q sum|Q_coefficients|=42550.
D116's integral identity gives

    ||Q(s)/Delta|| <= 480*L*V^2*B^238.

The product-coefficient functional at orders n=1,2,3 has norm at most
C_n/(pi*rho^(2*n+4)), where

    C_1=2*sqrt(2),   C_2=2*sqrt(3)+2,   C_3=4+2*sqrt(6).

The line of a successive intrinsic jet has arithmetic degree
(240+n)*H_CM-15*h_Fal(C). Retain the actual saved D104 Hodge-height
upper endpoint h_L^+=31172134711534863111/18446744073709551616 and put

    H^+=2*h_L^++log(2) < 41/10.

Use h_Fal(C)>=-16*log(2*pi), with D103's L2 normalization. The primary
reference is [Javanpeykar, Lemma 2.4.4](https://msp.org/ant/2014/8-1/ant-v8-n1-p04-s.pdf).
Keeping the pi factors and logarithms together, the upper bound for the
normalized finite zero degree of a nonzero successive jet is

    F_n(rho)=(240+n)*H^+ + 310*log(2) + 120*log(pi)
             +log(480*L)+log(C_n)+(480+2*n)*log(1/rho).       (1)

This replaces several separate binary ceilings in D116. It concerns
the actual unknown section, not only the candidate curve's height.

If the sixteen non-anchor values are at least N and the anchor at
least A, the finite degree contribution is at least
(16*N+A)*log(2)/272. D116's Galois averaging applies unchanged. Therefore

    N>17*F_n(rho)/log(2)-A/16                              (2)

suffices. These are section valuations with v_beta(2)=16, not ratio
error digits or working moment precisions.

| Successive order | D116 sufficient N | D117 sufficient N | Actual N | Anchor A |
| --- | ---: | ---: | ---: | ---: |
| 1 | 119806 | 35947 | 3794 | 3576 |
| 2 | 120284 | 36096 | 3745 | 3248 |
| 3 | 120758 | 36237 | 3728 | 2984 |

Sources 447/449 use rational logarithm, arctangent and radical enclosures,
with outward dyadic rounding. Review 450 uses a different logarithm
series, -log(1-t), and fresh pi/radical enclosures to prove the same
strict integer thresholds. The valuation gaps remain 32153/32351/32509.

## 5. What this settles, and the next arithmetic calculation

Order zero vanishes exactly on the CM divisor. Orders two and three
acquire the integral intrinsic-jet interpretation only after all their
preceding jets vanish exactly, as proved in D116. Zero-containing balls
do not establish those hypotheses. If all three successive tests pass,
the exact quadratic relations follow from 68=deg(4D)>deg(2K)=60, and
D88/D69 identify (C,D), without a separate rank-45 test.

The most optimistic radius-only substitution, rho=1, deletes the last
term of (1). With the other inputs fixed, (2) still requires
32928/33064/33193. The radius-one disk is not certified; this is a
monotonicity diagnostic for this bound. It proves that another disk
improvement alone cannot make the present data an exact certificate.

The next bounded arithmetic task is to recover the finite corrections
dropped in D104 and measure their effect on (1). With its notation, set

    c_L=h_L(Q)-h(W_S)>=0,
    c_ram=finite_zero_degree(D_Q(df))>=0.

D104 gives the exact relation

    H_CM=2*h_L(Q)+log(2)-2*c_L-c_ram.

Compute certified dyadic contributions to c_ram from the stable local
cover and to c_L from the compatible Hodge/stable lattice comparison.
The nodal differential generator and its stabilizer thickness must be
proved for the upstairs curve before interpreting any derivative
coefficient as integral content. No value of either correction has been
proved here. In particular, the evaluation saturation defect 245 is
not a substitute for either quantity or for the D102 residue-map index.
Insert only proved contributions into (1), and assess whether a stronger
lower bound on h_Fal(C) or a different integral tensor construction is
also required. Retain exact arithmetic identities with a uniqueness
argument as an alternative; candidate-only heights cannot replace this.

Do not start another routine moment-precision increase from the new
thresholds. At working precision P the present dense state has
174*(3P-1)*16 local-field entries, each carrying P bits in a theoretical
packed representation. This alone occupies 104396520000 bytes at
P=10000 and 417593040000 bytes at P=20000, before operators, temporaries
or overhead. These examples do not predict the required P and do not
bound streaming or other algorithms. A large run would need a different,
costed implementation, proved limb arithmetic, refined transport/Hensel
inputs and phases respecting the existing 180-second cap.

D99 nonhyperellipticity, D108 spectral rejection and all census,
new-level, Hecke-bank and cubic-precision pauses remain in force.
After exact base identification, P32/B3 markings, the double-cover
character, global genus-64 cubic/section data, norm-97 isolation,
combined torsion and the degree-257 invariant remain separate tasks.

## 6. Reproducibility and attribution

The [source ledger](../data/computed/cm_disk_sources_d117.json) distinguishes
inherited results from this milestone's lattice and budget deductions.
Sources 446--449 have four passing jobs and one archived implementation
failure. The first 447 run reached Python's decimal integer-string limit
when serializing enormous rational endpoints. Certified outward dyadic
rounding fixes serialization without weakening any assertion. The failed
source snapshot, log and receipt are preserved and explicitly audited.
No job timed out and no moment precision was increased.

The independent calculation probe for source 450 passes in 7.536 seconds.
Its final review preserves all 868 D116 source hashes and binds the new
sources, results, input receipts, failed snapshot, this report and ledger.
Run its final reproducibility check through runner 272 with its
180-second private-process-group cap and OPENBLAS_NUM_THREADS=1:

    python3 dembele/pari/450_cm_disk_exactness_review.py --check

The finite checks do not machine-verify the uniformization, arithmetic
models or Arakelov comparison theorems. Their hypotheses and applications
are supplied by this proof and the cited frozen predecessors. No
correspondence was sent and no target polynomial is claimed.
