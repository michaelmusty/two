# D141: what would turn the P1600 recognition into a proof

The user authorized checking the handoff, decisions, references and other
entry documents, then investigating D140's proof gap. All seven entry
documents contained D140 and their 21 artifact links resolved before this
investigation began.

Two sufficient proof targets can now be stated precisely using the existing
data. Neither target is proved here:

1. A bound **h_ext(I_2) <= 623** for the actual quadratic relation space in
   the fixed rational residue coordinates would force equality with the
   recovered space. This uses a basis-independent height defined below.
2. A lower bound **h_Fal(C) >= 29**, in D118's absolutely normalized metric,
   would make all three existing exact-vanishing tests succeed at P1600.
   Unlike at P200, this is compatible with the known upper bound 30.970856.

The invariant-height criterion is a new consequence of the saved lattice.
The Faltings threshold is a reassessment of D118/D120 using the completed
bank. The latter is numerical feasibility of a sufficient criterion, not
evidence that the actual height is near 29. The published formulas examined
below do not supply either missing estimate directly. No exact positive
vanishing, curve identification or field polynomial is established.

## 1. A bound on the relation space without choosing small equations

Let K be the actual rational quadratic relation space, of dimension 91 in
Q^136. Its rationality follows from the residue-frame descent in
[D106](cm-rational-frame-jets-d106.md); its dimension uses the actual
nonhyperelliptic canonical curve in [D99](hyperellipticity-review-d99.md).
Put Lambda_K=K intersect Z^136, and choose any integer basis with row matrix A.
Define

    h_ext(K) = log ||wedge^91 A||_2 = (1/2) log det(A A^t).

The wedge has primitive integer Pluecker coordinates because Lambda_K is
saturated. Its sign is the only ambiguity under a change of integer basis.
The Euclidean norm uses the saved 136 lexicographically ordered monomials,
with their ordinary integer coefficients; it is not invariant under a
change of the ambient canonical coordinates. Natural logarithms are used.

By [D140](dyadic-P1600-recognition-d140.md), every vector in Lambda_K belongs
to the certified full congruence lattice L. Let b_1,...,b_136 be its saved
ordered basis, and V the rational span of b_1,...,b_91. Write

    d_i = ||b_i*||^2 = D_i/D_(i-1),

where D_i is the leading Gram determinant and D_0=1.

Suppose K differs from V. The integral expansion of wedge^91 A in the
wedges b_J has a nonzero coefficient for some J other than {1,...,91}.
Order the subsets colexicographically and take the last nonzero one.
The change to wedges of the Gram--Schmidt vectors is triangular with
diagonal one. Therefore that coefficient remains a nonzero integer in
the orthogonal wedge basis. Consequently

    exp(2 h_ext(K)) >= min_(|J|=91, J != {1,...,91}) product_(j in J) d_j.  (1)

This is the exterior-lattice argument of [D60](cm-flag-height.md), now
applied to certified dyadic congruences and to exclusion outside a known
space. It does not assume that LLL found shortest vectors. The general
Gram--Schmidt lattice setup is in
[Lenstra--Lenstra--Lovasz, section 1](https://ir.cwi.nl/pub/9304/9304D.pdf);
the particular conditional identification criterion (1) is our deduction.

In both saved bases, every d_j with j>91 exceeds every d_i with i<=91.
Thus the minimum on the right is

    B_ext = D_91 * min_(j>91) d_j / max_(i<=91) d_i.                    (2)

Source 594 evaluates (2) exactly. Source 596 independently checks all 45
possibilities for the number of outside indices. It also recomputes the
first 91 leading Gram determinants by rational LDL decomposition; D140's
independent native certificates already check determinants 91 through 136.

| Training digits | h_ext(V) | Strict upper threshold for h_ext(K) that forces K=V |
| ---: | ---: | ---: |
| 96 | 547.226455339254 | 579.377760669288 |
| 160 | 547.226455339254 | 623.347163078801 |

The displayed decimals are explanatory; the saved rational intervals
certify the inequalities. In particular h_ext(K)<=623 suffices. The
known value of h_ext(V) does not give an upper bound for h_ext(K).

For readers using maximum primitive Pluecker coordinate instead of the
Euclidean norm, there are binomial(136,91) coordinates, so the sufficient
integer bound H_P satisfies

    binomial(136,91) H_P^2 < B_ext.

Both exact integer thresholds are in the diagnostic artifact. This
conversion loses a binomial factor. At 96 digits its sufficient bound
does not even include the simple covolume-based upper bound for the
candidate's maximum coordinate; the stronger covolume test still includes
the candidate. This is a limitation of that conversion, not a mismatch.

The new condition concerns one geometric subspace height. It is an
alternative to D140's hypothesis of 91 independent integral equations
of bounded coefficient height; these two sufficient hypotheses should
not be identified with each other.

## 2. Reassess the Faltings route at the actual P1600 precision

Retain D118's arithmetic line, metrics, radius and CM-height estimate.
Let F_n denote its upper bound for the finite zero degree after substituting
the existing Faltings lower endpoint F_minus=-23.146370000760... . If a new
lower bound F_new is proved, the section budget becomes

    F_n - 15*(F_new-F_minus).

For D138's achieved nonanchor/anchor bounds N_n,A_n, the measured zero
degree is Z_n=(16*N_n+A_n)*log(2)/272. Therefore a sufficient strict target is

    h_Fal(C) > T_n = F_minus + (F_n-Z_n)/15.                          (3)

| Order | N_n | A_n | Critical value T_n | Sufficient integer lower bound |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 6594 | 6376 | 27.304628397558 | 28 |
| 2 | 6545 | 6048 | 27.749242337224 | 28 |
| 3 | 6528 | 5784 | 28.084617400198 | 29 |

As always, higher intrinsic jets require the preceding jets to vanish
exactly. A bound of 29 would permit this induction from the already
exact order-zero vanishing, and then the degree comparison
deg(4D)=68>deg(2K)=60 proves the quadrics vanish on the actual curve.
The existing canonical-embedding and candidate-scheme certificates would
then identify (C,D17). P32/B3 markings and the later cover/torsion work
would still be separate obligations.

D120 proved h_Fal(C)<30.970856 from nonzero evaluation minors. Its
rejection of a Faltings-only improvement was correct for the P200 data:
the old critical values exceeded 35. Those values cannot be carried
unchanged into a P1600 decision. Equation (3) reopens a numerical window
between approximately 28.084618 and 30.970856; it supplies no lower estimate
inside that window.

Source 596 checks (3) with an independent logarithm series and with the
uncollected expression before substituting F_minus. All arithmetic
decisions use rational outward enclosures.

## 3. What the height formulas actually provide

[de Jong--Shokrieh, Theorem A and equation (1.11)](https://arxiv.org/pdf/1810.02637)
express the stable Faltings height using the normalized theta-divisor
height, finite tropical moments and archimedean terms. In our existing
normalization this gives

    h_Fal(C) = F_minus_exact + 32*h'_Theta(Theta)
               + 2*I_infinity_average + other_finite_terms,

where F_minus_exact is D118's constant and known dyadic contribution,
and the remaining terms are nonnegative. The last order in (3) requires
more than 51.230987400958... of additional contribution. For example,
h'_Theta(Theta)>=13/8 or I_infinity_average>=26 would suffice. Neither
inequality is established. Discarded nonnegative terms cannot be assigned
a positive numerical value without further evidence.

[Yuan, *Modular Heights of Quaternionic Shimura Curves*, v3, section 1.1
and Theorem 1.1](https://arxiv.org/pdf/2205.13995v3) computes a normalized
arithmetic self-intersection of the automorphic Hodge line. This is a
different invariant from the determinant-of-cohomology Faltings height
in (3). The distinction is visible in the definitions, before any numerical
calculation. Applying that formula to obtain (3) would require a proved
comparison of metrics, integral models and the normalizer quotient,
with all correction terms. The theorem is not used here as a Faltings
height formula.

[Freixas i Montplet--von Pippich, sections 1 and 10](https://arxiv.org/pdf/1604.00284v2)
provide a possible type of comparison through orbifold Riemann--Roch,
Quillen metrics, elliptic cotangent lines and Selberg zeta. It introduces
new analytic and finite-model terms that are not in the current certificate.
There is also a specific source issue to resolve before using its constants:
[Kalvin, Introduction, Corollary 1.2 and Remark 3.2](https://arxiv.org/pdf/2011.05407v1)
gives a different model-cone determinant and explicitly identifies a
discrepancy with that paper's Theorem 2.5/section 7. This is a recorded
source reconciliation requirement, not our proof that every related
Riemann--Roch statement is invalid. No disputed constant is used in D141.

These inspected sources do not establish the required Faltings lower bound
or an upper bound for h_ext(K) in the fixed residue coordinates. A numerical
height of the candidate alone would not establish either statement about
the unknown actual curve.

## 4. Shorter equations do not close the old section budget

The largest coefficient L1 sums in the recovered bases are 30460 and 29299,
versus 42550 in the old basis. Their integral unimodular equivalence means
the old uniform local lower bounds remain valid for the recovered bases.
Replacing only the global L1 constant by 29299 lowers each sufficient
threshold by nine beta-valuation units:

| Order | Old sufficient N | Recovered-basis sufficient N | Achieved N |
| ---: | ---: | ---: | ---: |
| 1 | 25155 | 25146 | 6594 |
| 2 | 25269 | 25260 | 6545 |
| 3 | 25376 | 25367 | 6528 |

Even setting the coefficient L1 cost to its optimistic lower limit 1
and formally replacing the certified disk by radius 1 leaves thresholds
21874,21976,22070. That radius is not certified; this is a limitation of
the particular bound with its other inputs fixed. It rules out more
basis shortening or this radius adjustment as a sufficient repair.
It is not a lower bound on every possible identification method.

## 5. Continuation and audit scope

The next proof work is to obtain an actual geometric height estimate in
one of the two normalizations above. A focused feasibility task is to
derive the corrected arithmetic Riemann--Roch comparison for the actual
normalizer curve, explicitly accounting for its signature
(16;2^17,3^9,32), the finite model, metric constants and analytic term.
Determine whether that expression can yield a bound above 28.084618
before admitting any numerical spectral work. The current spectral,
new-level, Hecke-bank and cubic-search pauses remain in effect.
The intrinsic relation-space height remains an alternative if a bound
in the specified rational frame becomes available. No P3200 bank follows
from these conditional criteria.

The source-594 diagnostic and source-596 independent audit pass. The audit
checks 6,561 small exterior controls (6,192 outside wedges), the strict
boundary, both sets of 91 early Gram minors, all 45 outside-count cases
per lattice, and the new height targets. These finite checks do not
machine-prove the geometric argument or the cited theorems.

Two failed attempts are retained. Source 593 included an overly strong
assertion that the conservative maximum-Pluecker bound must contain the
candidate covolume upper bound at 96 digits; source 594 records the two
tests separately. Source 595 exposed an integer-division-to-float error
at the first LDL pivot; source 596 uses rational pivots throughout and
adds a non-diagonal exact Gram control. Both failures stopped before
creating a result. Neither changes D140 or supplies a numerical mismatch.

Source 597's fixed provenance review and replay, followed by the completion
record, are the final checkpoint authority. Preserve sources 593–597,
this report, the source ledger, all receipts/logs and both failed source
snapshots after that review. All work retains the 180-second process-group
cap, the 2 GiB per-worker/store limit and the 6 GiB conservative aggregate
RSS limit. No harmonic precision, sealed store or prior certificate changed.
