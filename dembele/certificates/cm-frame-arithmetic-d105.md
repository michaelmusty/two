# D105: the actual CM frame and a tangent atlas over the CM class field

Date: 2026-09-24. Continuation of D104, authorized by “continue”.

**Result:** for the actual genus-16 Shimura quotient C and its divisor
D of seventeen order-two CM points,

    H^0(C,K_C-D)=0.

The evaluation matrix has rank 16, and CM Galois transitivity makes
all seventeen maximal cofactors nonzero. Thus these points really
form a projective frame. This proof uses the arithmetic reduction
graph, not candidate equations, numerical differentials or a guessed
location of the distinguished eighteenth branch point.

There is also a way to use the D103--D104 height bound before certifying
the old numerical point-to-root matching. Over the CM Hilbert class
field H, of degree 272 over Q, choose any fixed bijection between the
actual CM points and the seventeen polynomial roots. The resulting
frame is algebraic over H. Nonhyperellipticity guarantees a nonzero
projective tangent in fifteen Gaussian coordinates, with

    h([G_12(P):...:G_1,16(P)]) < 10504.

This does not certify the saved orientation, a specific nonzero G_12,
or descent of that frame to F. No independent tangent has yet been
evaluated, and the candidate remains unidentified.

## 1. Locate the branch divisor without choosing its labels

Keep the notation of [D99](hyperellipticity-review-d99.md): S has
genus 40, C=S/<w_p> has genus 16, and both have totally degenerate
dyadic reduction. The actual signatures are (40;3^18,16) and
(16;2^17,3^9,32). The double cover has reduced characteristic-zero
branch divisor

    B=P_32+D,       deg(B)=18.

These signature and branching statements do not use the disputed
hyperellipticity argument or the ordinary-point/moment hypotheses
from the earlier plane-model route.

In the D99 semistable model of S, w_p interchanges the two vertex
layers. It fixes no vertex and reverses precisely nine edges, at
diagonal Brandt classes 5,51,...,58. Their lengths are 32,1,...,1.
Every fixed geometric point retracts to a fixed point of the skeleton,
so it lies in one of the corresponding nine open annuli.

**Annulus lemma.** Over an algebraically closed complete nonarchimedean
field of characteristic zero, an involution of an open annulus which
interchanges its ends has exactly two fixed points, both simple.

To prove this, its action on the skeleton has slope -1. On a closed
subannulus straddling the fixed midpoint, choose a coordinate t and
write

    w(t)=a*t^(-1)*(1+g(t)),       ||g||_sup<1.

The fixed-point equation is t^2-a*(1+g(t))=0. On an inner circle of
radius less than sqrt(|a|), its constant term dominates; on an outer
circle of larger radius, t^2 dominates. The slope change counts
exactly two zeros with multiplicity. All fixed points retract to
the midpoint, so none are omitted. A nontrivial involution at a smooth
fixed point in characteristic zero has derivative -1: derivative +1
would make the first nonidentity term of its formal square twice
that term. Hence both zeros are simple.

The analytic inputs are the annulus unit description and skeleton
slope/zero formula in [Baker--Payne--Rabinoff, Propositions 2.2, 2.5,
2.10 and Corollary 2.6](https://arxiv.org/pdf/1404.0279).
Their Proposition 4.3 identifies a node's tube with an open annulus.
The fixed-point lemma above is our deduction from these inputs; it
is not a tame reduction count. In particular, it allows residue
characteristic 2. It does not apply to arbitrary branch-preserving
annulus involutions.

Each reversed node has smooth image in the integral quotient, by
[Kurihara, Proposition 3-2 and Lemma 3-3, pp. 284--288](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf),
as checked in D99. Thus the images of its two fixed points specialize
to that smooth point of the quotient component. This uses the
integral quotient theorem, without assuming that invariants commute
with reduction at 2. Stabilization retracts that component to a point
q_i of the stable graph Gamma. Consequently

    tau(B)=2*(q_0+...+q_8),
    tau(D)=2*(q_0+...+q_8)-q_k       for some k in {0,...,8}.    (1)

The sixteen or thirty-two stabilizer orders change node thickness;
they do not multiply the number of fixed points on the coarse annulus.

## 2. Reconstruct the nine marked positions

The stable weighted graph is the actual graph from D99, with 30
vertices and 45 edges. Unlike D99's topological hyperellipticity
obstruction, the present divisor calculation uses these lengths.

| Original diagonal class | Stable edge containing q_i | Distance from either endpoint |
| --- | --- | --- |
| 5 | (9,10) | 6 |
| 51 | (39,45) | 1 |
| 52 | (40,46) | 1 |
| 53 | (41,47) | 1 |
| 54 | (42,48) | 1 |
| 55 | (39,49) | 1 |
| 56 | (40,50) | 1 |
| 57 | (41,43) | 1 |
| 58 | (42,44) | 1 |

For class 5, pruning the quotient's rational tail moves the mark to
vertex 6; the paths 6--7--9 and 6--8--10 each have length 6. The other
eight marks are the bivalent vertices of length-1 plus length-1 paths.
The independent audit reconstructs the 73 algebraic quotient edges
directly from the fresh Brandt entries and stabilizers, prunes tails
while carrying the marks, and contracts the remaining bivalent paths.
It does not assume the midpoint list chosen by the preliminary probe.

Subdivide the weighted edges into unit intervals. The resulting model
has 61 vertices and 76 edges. Its root is q=q_0, named e9_10_6 in the
artifact. All nine marks lie in this vertex set. A finite base
extension merely subdivides edges and changes the common length
normalization; neither operation changes the divisor conclusion.

## 3. Nine explicit certificates of noneffectivity

For each possible k in (1), set

    E_k=K_Gamma-2*sum_i q_i+q_k,       deg(E_k)=13.

[Script 385](../pari/385_cm_frame_specialization.py) stores an integer
potential f_k and a divisor E'_k=E_k+L*f_k. Here
(L*f)(v)=valence(v)*f(v)-sum_(u adjacent v) f(u). Thus L*f is the
principal divisor of the negative of the piecewise linear interpolation
of f on the unit graph, with the outgoing-slope convention.

Every E'_k is nonnegative away from q and has negative coefficient
at q: -3 for k=0 and -2 for each of the eight other cases. A saved
ordering starts at q and burns every vertex; each subsequent v has

    E'_k(v) < number of edges from v to earlier vertices.       (2)

For example, the first certificate has
E'_0=2*(v27+...+v34)-3*q. The artifact contains all potentials,
divisors and orders, rather than only a solver's boolean answer.

For clarity, this certifies noneffectivity on the metric graph,
including corrections with additional breakpoints. Suppose
E'_k+div(h) were effective. Its maximum locus cannot contain q,
since every outgoing slope there is nonpositive. A boundary point
of this locus inside an open unit edge would have E'_k=0 and strictly
negative outgoing slope sum, also impossible. Therefore the maximum
locus has a boundary only at model vertices. Choose its first vertex
v in the burning order. Every edge to an earlier vertex must leave
the maximum immediately; otherwise it would have an interior boundary
point. Its integral outgoing slope is at most -1. All other outgoing
slopes are nonpositive. Inequality (2) makes the corrected coefficient
at v negative, a contradiction. Hence E_k has no effective representative.

[Baker, Corollary 2.10 and Lemma 4.19](https://arxiv.org/pdf/math/0701075)
apply after semistable resolution: specialization preserves linear
equivalence, cannot lower rank, and sends the canonical class of a
totally degenerate curve to K_Gamma. If K_C-D had a nonzero section,
its effective zero divisor would specialize to an effective divisor
in the class of one of the E_k. The certificates exclude all nine.
This proves H^0(C,K_C-D)=0.

The evaluation map from the 16-dimensional canonical space at D
therefore has rank 16. At least one of its seventeen maximal minors
is nonzero. By CM reciprocity the seventeen points form one orbit
under Gal(H/M)=C17; D59's exact ideal classes exhaust this group.
Galois transport preserves whether the minor omitting a given point
vanishes. Therefore all seventeen minors are nonzero. In particular,
this proves the full projective-frame condition, not only full rank.
Riemann--Roch also gives h^0(C,O(D))=2.

## 4. Identify a common field without a numerical orientation

Let M be the degree-16 CM field from D104, and let N be the splitting
field of the saved degree-17 polynomial. The following argument
identifies N with H, the Hilbert class field of M. It uses no
hyperellipticity claim, Jacobian identification, or numerical root
matching from D59.

The proved 31-adic Galois calculation in D59 gives a transitive
permutation group of order 272 with normal subgroup C17. Its quotient
has order 16. D59 also constructs the C17-invariant resolvent
kappa=sum_j r_j^2*r_f(j), where f is a 17-cycle. Its sixteen conjugates
have the saved monic polynomial R. The root bound |r_j|<4 and lift
modulus 31^70>2*1089^16 certify its integer coefficients.

The audit evaluates R(gamma) exactly in M, where gamma is the saved
polynomial in beta, and proves that 1,gamma,...,gamma^15 are linearly
independent by a nonzero determinant modulo a prime. Thus R is
irreducible and Q(gamma)=M is isomorphic to N^C17. D104 realizes M
as a Galois subfield of Q(zeta_64), so any isomorphic embedded copy
in a fixed algebraic closure is M itself. It follows that M is
contained in N and N/M is cyclic of degree 17.

D102 supplies an integral order of discriminant 2^79 in the
degree-17 root field. The audit replays its ring-closure and trace
calculation. Its discriminant suffices to prove that this field,
all its conjugates, and their compositum N are unramified at every
odd prime. This is the discriminant of the verified order, not the
larger discriminant of the polynomial's power order; maximality
of the verified order is unnecessary here.

The polynomial of beta is Eisenstein at 2. Hence M has one dyadic
prime with residue field F2. Its local unit group is pro-2 and has
no quotient of order 17. Local reciprocity therefore makes every
cyclic degree-17 extension of this local field unramified. Thus N/M
is unramified at 2 as well. Since M is totally imaginary and its
proved class number is 17, N is its Hilbert class field H, with
[H:Q]=272. The local and global class-field inputs are
[Milne, Class Field Theory, I.1.8--1.11 and V.3.9](https://www.jmilne.org/math/CourseNotes/CFT.pdf).

Maximal-order CM points on the canonical Shimura curve are H-rational;
see [Voight, Shimura curve computations, §4.3](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf).
Their images in the F-defined normalizer quotient are also H-rational.
Therefore H contains both all seventeen actual points and all
seventeen polynomial roots. Reusing D59's proved group and class-number
computations is explicit; they have not been independently rerun here.

Choose any one fixed bijection between these two sets. The D103
vectors V_ij=sigma_i(17*eta_j) are integral and sum to zero, and its
adjugate construction defines a canonical frame over H up to a common
scalar. The height argument only needs these integrality and size
properties, so it works for every such bijection. This bypasses the
old orientation issue for a construction over H; it does not prove
that a chosen bijection is Galois equivariant over F or that its frame
descends to F.

## 5. A finite atlas removes the chosen-denominator hypothesis

Write s_1,...,s_16 for the framed canonical sections. Their values at
P_i are a_i*eta_j(theta_i), with a_i nonzero. Since eta_1 is a nonzero
element of the degree-17 field, s_1(P_i) is nonzero at every marked
point. The canonical map of a nonhyperelliptic curve is an immersion
(for example [Vakil, Class 46, Exercise 1.A](https://math.stanford.edu/~vakil/0708-216/216class46.pdf)).
Equivalently, Riemann--Roch and l(2P)=1 show that it separates the
tangent direction at P. Thus the derivatives of s_j/s_1 cannot all
vanish, and

    Lambda(P)=[G_12(P):...:G_1,16(P)] in P^14(H)

is defined and nonzero. At least one of the fifteen charts with pivot
G_1a, a=2,...,16, is valid. This does not identify that pivot or give
a numerical lower bound for it.

The D103 projective-height inequality applies to all fifteen integral
sections of the common line W_P^3*T^2 at once. Its pointwise norm bound
already bounds every pair uniformly, so taking the maximum over all
coordinates adds no constant. D104 and the full frame just proved give

    h(Lambda(P)) <= 513*H_CM,disk+8400 < 10504.

Every coordinate ratio in any valid chart has height at most this
projective height. This statement applies to the H-frame for the
chosen bijection and all its conjugates. It is not a certification of
the particular G_12 chart used by the old approximate computation.

## 6. Sufficient equality thresholds, and their limits

Only this diagnostic reads the exact candidate tangent from D101.
Its fifteen coordinates have no zero entry. Clearing all denominators
by one integer q and applying |theta|<4 gives

    h(Lambda_candidate) <= log max(q, max_j sum_k |q*a_jk|*4^k).

The integer inside the logarithm is less than 2^976. Rational log
enclosures prove 976*log(2)<677, so every candidate chart ratio has
height less than 677. For a consistently labelled comparison in a
common valid chart, the difference delta of actual and candidate
ratios satisfies

    h(delta)<10504+677+7/10=111817/10.

Since delta is in H, a nonzero delta obeys
|sigma(delta)|>=exp(-272*h(delta)) at each embedding. An absolute
error at most **10^(-1320873)** at one matched embedding is therefore
a sufficient equality certificate. If errors are certified at every
embedding of H, the product formula gives the sufficient bound
**10^(-4857)** at each embedding. These are conservative sufficient
thresholds, not minimum precision, existing accuracy or evaluator cost.
The all-embedding alternative includes the transported bijection and
conjugate frame at each embedding; seventeen approximate evaluations
at one complex place do not supply that certificate by themselves.

This is only a first-tangent bound. D88's curve-identification
criterion requires higher jets: vanishing through order three at all
seventeen points forces a quadratic relation of degree 60 to vanish,
because 4*17>60. Over H with arbitrary labels, these jets must be
checked at all seventeen points, unless equivariant labels and
descent have independently been proved. Exact equality of the first
tangent alone does not identify the curve, double cover or cubic cover.

## 7. Audit, preservation and next task

The preliminary [probe 384](../pari/384_cm_frame_specialization_probe.py)
assumed the first possible P_32 location and remains frozen with
that conditional status. Script 385 handles all nine locations.
[Audit 386](../pari/386_cm_frame_arithmetic_review.py) reconstructs the
marks from the Brandt matrix, verifies each integer potential by
edgewise flux, and checks each burning inequality without invoking
the discovery solver. It rejects altered potentials, burning orders,
and distinguished-point allocations. It also checks the field
resolvent, replays the verified integral-order arithmetic, calculates
the projective candidate bound, and checks all 479 D99 and 53 D104
bound source hashes unchanged.

The finite computations do not machine-verify the geometric lemmas
or the cited theorems. The [source ledger](../data/computed/cm_frame_arithmetic_sources_d105.json)
distinguishes those inputs from the new deductions. Jobs use the
180-second private process-group cap. Recheck the completed audit with:

    python3 dembele/pari/386_cm_frame_arithmetic_review.py --check

Next address an actual independent tangent/jet evaluator with a
feasible equality mechanism, keeping the H-frame and its chosen
bijection explicit. Certifying the D59 labels may reduce the field
degree and restore Galois propagation, but is no longer a prerequisite
for the qualitative frame or this height theorem. A specific chart
still needs certification before dividing numerical enclosures.
Higher-jet exactness and arithmetic descent remain separate inputs.
Do not launch a spectral run merely because qualitative nonvanishing
is known: D98's existing full enclosure still contains zero, and the
spectral pilot gate has not passed. Retain the enumeration, Hecke-bank
and cubic-precision pauses. Global cubic construction, norm-97
separation, target-scale torsion and the final field polynomial remain
open. No correspondence was sent.
