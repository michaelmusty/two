# D106: a rational CM frame and finite higher-jet comparison bounds

Date: 2026-09-24. Continuation authorized by “continue”.

**Result.** The actual marked curve satisfies
`Aut(C_Qbar,D)=1`. Consequently the geometric marked descent from
D58 is compatible with the given F-model, without the unproved D56
ordinary-point or moment hypotheses. Its residue construction gives
a canonical rational CM frame, up to a common scalar, and ratio
Taylor coefficients in the degree-17 field L=Q(theta).

The first three positive-order coefficients have absolute logarithmic
height strictly below 10504, 31518 and 52533. Exact candidate reference
coefficients are now available through order three. At the inert prime
31, sufficient comparison precisions are respectively 3257, 9746 and
16236 digits. The three-coefficient rank test from D88 needs only
orders zero through two, so a common precision 9746 suffices for that
test, subject to the evaluator conditions below.

**No independent Shimura tangent or higher jet has been evaluated.**
These are sufficient separation bounds, not achieved accuracy,
minimum precision requirements, or a candidate-identification proof.
The saved numerical point/root matching remains uncertified.

## 1. Specialization bounds the geometric automorphism group

Use the actual stable reduction established in
[D99](hyperellipticity-review-d99.md). Over an algebraically closed
dyadic residue field it has thirty rational components and forty-five
nodes. Its graph G is simple and cubic. Every normalized component
therefore has three distinct points over nodes.

After a finite extension of the local field, all geometric
automorphisms of C are defined. Each extends uniquely to the stable
model, by [Stacks, Lemma 109.24.2](https://stacks.math.columbia.edu/tag/0E97).
Specialization on automorphisms is injective: the stable-curve
automorphism scheme is finite and unramified, since the stable moduli
stack is proper and Deligne--Mumford
([Stacks, Theorem 109.25.3](https://stacks.math.columbia.edu/tag/0E9C)).
Two sections of a separated unramified morphism over a connected base
which agree at one point agree everywhere
([Stacks, Theorem 41.6.2](https://stacks.math.columbia.edu/tag/024U)).

An automorphism of the special curve acting trivially on G fixes every
component and each of its three attaching points. A projectivity of
P1 fixing three distinct points is the identity. Thus

    Aut(C_Qbar) injects into Aut(G),       |Aut(C_Qbar)| divides 64.   (1)

This argument allows automorphisms of 2-power order in residue
characteristic 2. It uses neither a tame-order assumption nor the
stronger admissibility/exponent assertion of Dembélé's Lemma 5.7.
It gives an upper bound, not a computation of the unmarked Aut(C).

[Script 387](../pari/387_cm_rational_frame.py) independently enumerates
the full unweighted graph group. It first collapses the four pairs
with identical open neighborhoods:

    {43,47}, {44,48}, {45,49}, {46,50}.

The resulting graph, with block sizes recorded, has twenty-six
vertices and four automorphisms. Lifting all independent swaps in
the four pairs gives 4*2^4=64 automorphisms, exactly the D99 list.
Color refinement followed by exhaustive adjacency-preserving
bijections proves completeness. Group closure and preservation of
all edge lengths are checked afterward. A K4 control has order 24,
so the argument does not infer a 2-group merely from trivalence.

## 2. The odd CM orbit rigidifies the curve

Let A=Aut(C_Qbar,D), preserving D as an unordered divisor. By (1),
A is a 2-group. Its action on the seventeen geometric points of D
has at least one singleton orbit: all other orbit sizes are even.
Thus some point of D is fixed by every element of A.

The pair (C,D) is defined over F, hence over the degree-16 CM field M.
Its absolute Galois group normalizes A. The subset of D fixed by
all of A is therefore Galois stable. CM reciprocity and the exact
D59 class-group computation make D a single orbit over M. The
nonempty fixed subset must be all of D.

[D105](cm-frame-arithmetic-d105.md) proves that these seventeen points
are a projective frame in the canonical P15. A projectivity fixing
a projective frame pointwise is the identity: after sixteen points
become coordinate vertices, the seventeenth forces all diagonal
entries to coincide. D99 proves nonhyperellipticity, so the canonical
map is an embedding. We conclude

    Aut(C_Qbar,D)=1.                                             (2)

The Galois-normalization step matters. A transposition acting on a
seventeen-point set has fixed points but does not fix the entire set;
script 387 checks that a transitive 17-cycle does not normalize that
example. No order-two CM point is being treated as a Weierstrass
point, and P32 is not used in this rigidity argument.

## 3. Compatible descent and the degree-17 residue field

[D58, sections 1--2](marked-descent.md) carries canonical conjugation
through the Shimura level, the Atkin--Lehner map, and its distinguished
smooth source CM point. This gives geometric Q-descent of (C,P32,D).
The literature input is
[Dembélé, Lemma 5.2](https://arxiv.org/pdf/1906.06772), together with
[Sijsling--Voight, Theorem 1.3.2](https://jvoight.github.io/articles/birch-descent-021420.pdf)
in the 2020 author version. D58 checks the invariant dyadic prime,
trivial relevant ray class group and unique cyclotomic CM point.
This canonical-conjugation statement remains a mathematical input;
the present graph computation does not reprove it.

Let (C0,P0,D0) be such a Q-descent. A geometric D-marked isomorphism
from C to (C0)_F is unique by (2). Its F-Galois conjugates are also
D-marked isomorphisms, so it is defined over F. Equivalently, the
unique marked comparison maps automatically satisfy the Weil
cocycle condition. See
[Sijsling--Voight, Theorem 2.1.1 and section 2.2, especially
Corollary 2.2.3](https://jvoight.github.io/articles/birch-descent-021420.pdf).
This replaces the conditional rigidity argument in D58 section 3.

Thus the given F-model is compatibly the base change of a unique
Q-form as a D-marked curve. It also carries the D58 P32 marking.
We have not computed descent matrices in the old analytic basis
or proved compatibility of an explicit model of the upstairs cover.

D0 is a closed point of degree 17, since it is already transitive
over M. Write A0=H^0(D0,O_D0). D105 proves that the splitting field
of the saved polynomial is the CM Hilbert class field H, with
Gal(H/Q)=AGL1(F17) of order 272, and that all actual CM points are
H-rational. The F-defined comparison above transports this
rationality to C0. Hence A0 embeds into H with degree 17.

Its stabilizer has order 16 and is a Sylow 2-subgroup. All such
subgroups are conjugate; the saved root field L=Q(theta) is fixed
by one of them. Therefore A0 is Q-isomorphic to L. In AGL1(F17) a
point stabilizer fixes exactly one point, so its normalizer equals
itself. The Galois correspondence gives Aut_Q(L)=1. The isomorphism

    A0 ~= L                                                   (3)

is consequently unique as a Q-algebra isomorphism. Script 387
checks the seventeen stabilizers, their conjugacy, self-normalizers
and trivial common core by enumerating all 272 affine maps.

This is an abstract arithmetic identification. It does not identify
a saved complex CM point with a saved numerical root. At a 31-adic
implementation the embedding of L into the completed field must
also be matched; local Frobenius choices cannot be ignored.

## 4. A canonical rational residue frame

D105 gives h0(K_C0-D0)=0 and h0(O(D0))=2. Choose a nonconstant
h in H^0(C0,O(D0)) over Q. Its polar divisor is a nonempty
Q-defined sub-divisor of the transitive reduced divisor D0, so it
is exactly D0, with simple poles.

The residue map

    H^0(C0,K_C0) -> ker(Tr_(A0/Q)),
    omega |-> Res_D0(h*omega)                                  (4)

is Q-linear. The residue theorem puts its image in the trace-zero
subspace. Zero residues imply that omega vanishes at every point
of D0, since h has a simple pole at each; D105 makes the kernel
zero. Both spaces have dimension sixteen, so (4) is an isomorphism.

Pull back the saved trace-centered basis eta_1,...,eta_16 through
(3)--(4). Another choice h'=a*h+b has a in Q nonzero and b in Q,
and rescales the resulting basis by the common factor a^(-1).
Hence the canonical projective coordinates are rational and unique
in this normalization. At a geometric CM point their values are

    [sigma(eta_1):...:sigma(eta_16)].

This is the same projective residue construction bounded by D103,
using the now-established equivariant arithmetic labeling. The
D103 integral adjugate sections differ by only a common scalar.

The first coordinate does not vanish on D0: eta_1=theta-2/17 is
nonzero in L. Put r_j=omega_j/omega_1. For any a with d(r_a)(D0)
nonzero, let

    t=r_a-r_a(D0),       r_j=sum_(n>=0) a_(n,j)*t^n.             (5)

Every a_(n,j) belongs to L. Canonical immersion supplies at least
one a among 2,...,16; its nonvanishing then holds at all seventeen
conjugate points. The particular choice a=2 is still unproved on
the actual curve. The candidate computations below use that choice.

## 5. Integral expressions for the higher coefficients

Use the D103 sections s_j in omega tensor T on a stable model.
On a smooth coarse chart write their coefficients as f,a,b for
s_1,s_a,s_j, and differentiate with respect to the coarse coordinate u.
Set

    G=f*a'-a*f',       H_j=f*b'-b*f',
    B_j=G*H_j'-H_j*G',
    N2_j=f^2*B_j,
    N3_j=f^2*(G*N2_j'-3*N2_j*G')
         =2*f^3*f'*B_j*G+f^4*G*B_j'-3*f^4*B_j*G'.             (6)

Since dt/du=G/f^2, direct differentiation gives

    a_(1,j)=H_j/G,
    a_(2,j)=N2_j/(2*G^3),
    a_(3,j)=N3_j/(6*G^5).                                     (7)

These are Taylor coefficients; the factorials in (7) are required.

The expressions before division extend integrally across nodes.
Use the map Omega^1 -> omega from D103 and a local dualizing
generator lambda, so dg=(D_lambda g)*lambda. Then G,H have line
omega^3*T^2, B has line omega^7*T^4, N2 has line omega^9*T^6, and
N3 has line omega^15*T^10. In the expression G*N2'-3*N2*G',
the changes of generator cancel because 9=3*3. At a node xy=c,
D_lambda(x)=x and D_lambda(y)=-y. No division by the residue
characteristic enters these sections. T is pulled back from the
base, so its transition factors have zero relative derivative.
This is our higher-order extension of the D103 Gaussian argument.

Script 387 independently checks (7) by inverting formal series,
and verifies covariance under a nonlinear change of u and a
common nonconstant rescaling of all three coefficients. Omitting
the first term of N3 in (6) fails the controls.

For the norm bounds, D103 gives ||s_j|| < 2^5141, where
5141=6+35+255*20. The embedded disk of radius rho=2^(-10) gives

    |f_j^(k)(0)| <= k!*sqrt(k+1)/sqrt(pi)
                   *2^(20*(k+1))*||s_j||.

For k=0,1,2,3 use the larger powers 2^20,2^41,2^63,2^85.
After removing the common section-norm factors, valid binary
exponents for G,G',G'',B,B',N2,N3 are

    62, 84, 107, 147, 170, 187, 315.

Retain D103's sharper exponent 60 for the original Gaussian
operator, and write

    Lambda=3*h(W)+2*h(T)+(2*5141+60)*log(2) < 10504.

Here W is the coarse canonical fiber with its disk metric.
D103--D105 prove the displayed upper bound. The integral-section
height inequality, followed by division by 2! or 3!, gives

    h(a_(2,j)) <= 3*Lambda+8*log(2) < 31518,
    h(a_(3,j)) <= 5*Lambda+15*log(2)+log(6) < 52533.             (8)

The line powers and the common finite zero ideals are handled
exactly as in D103; dropping the latter only increases the bound.
These bounds hold in any valid ratio chart (5). They use actual
Shimura geometry and no candidate coefficients.

## 6. Exact candidate references and normalization

[Magma driver 388](../magma/388_cm_candidate_ratio_jets.m) uses the
saved rational quadrics and CM point, sets X1=1, and recursively
solves their coefficients through t^3 with

    t=X2/X1-(X2/X1)(P).

The Jacobian has rank 14; fixing X1 and the parameter adds two
independent constraints. Thus each successive coefficient is
uniquely determined. The run passed in 42.91 seconds.

[Independent review 389](../pari/389_cm_ratio_jet_review.py) parses
the exact fractions and checks all 91*4=364 coefficient identities
using integer polynomial arithmetic modulo the degree-17 polynomial.
It verifies the normalized constant point, exact agreement of a1
with D101, and direct agreement of a0,a1,a2 with D88 modulo 31.

In particular, D88 already used X1=1 and the ratio parameter above.
No extra factor of the raw point's first coordinate belongs in that
comparison; a control rejects such a factor. D101 solved the
homogeneous tangent at the raw point, but its conditions v1=0,v2=1
give the same first ratio derivative. General raw-coordinate higher
jets would require a scaling, which is why this distinction matters.

The new mod-31 quadratic jet matrices have ranks 17,34,45,45 for
one through four coefficients. The candidate height bound uses
|sigma(theta)|<4 and one common clearing integer at each order:

| Taylor order | Clearing integer digits | Binary bound exponent | Candidate height upper |
| --- | ---: | ---: | ---: |
| 1 | 285 | 976 | 677 |
| 2 | 837 | 2808 | 1947 |
| 3 | 1389 | 4642 | 3218 |

The 285-digit integer is in the power basis; D101's smaller
269-digit integer was in its integral lattice. They are consistent.
All these denominators are prime to 31. These are candidate data
only, stored in the [review artifact](../data/computed/cm_ratio_jet_review_d106.json).

## 7. Finite equality tests

For delta=a_(n,j)-a_(n,j)^candidate, the absolute logarithmic height
satisfies h(delta)<B_n, with

    (B1,B2,B3)=(111817/10,334657/10,557517/10).

This uses h(x-y)<=h(x)+h(y)+log(2) and log(2)<7/10.
For a nonzero delta in L, the product formula and h(delta)=h(1/delta)
bound its possible smallness at any place.

The review independently proves that the defining polynomial is
irreducible modulo 31, by the prime-degree irreducibility criterion.
Thus 31 is unramified and inert, with residue degree 17. Normalize
v31(31)=1. Its contribution alone gives

    h(delta) >= v31(delta)*log(31).

The local degree 17 cancels [L:Q]=17. Consequently v31(delta)>=N
forces delta=0 whenever N*log(31)>B_n. Exact rational logarithm
enclosures give the following sufficient thresholds.

| Order | Actual height upper | Candidate height upper | Sufficient v31 difference |
| --- | ---: | ---: | ---: |
| 1 | 10504 | 677 | 3257 |
| 2 | 31518 | 1947 | 9746 |
| 3 | 52533 | 3218 | 16236 |

No global denominator bound on the actual coefficient is needed
for this height argument. A certified congruence also has to use
the same local embedding and the actual rational frame.

For an archimedean comparison, errors at most 10^(-N) suffice with:

| Order | One real embedding | One nonreal embedding and its conjugate | Every embedding |
| --- | ---: | ---: | ---: |
| 1 | 82555 | 41278 | 4857 |
| 2 | 247078 | 123539 | 14534 |
| 3 | 411616 | 205808 | 24213 |

An exact Sturm calculation gives signature (1,8). The middle column
uses the automatic equality of conjugate absolute errors for
algebraic numbers in the same identified field; it does not assume
independent approximations at both embeddings. All bounds are
conservative sufficient thresholds, not precision optima. D105's
degree-272 bounds remain valid for its arbitrary H-frame.

The evaluator must still certify a valid common chart, produce the
actual ratios in the rational residue frame (or prove its change
to that frame), match the local/complex field embedding, and
certify the comparison errors. Merely evaluating the candidate at
higher precision does none of these things.

## 8. What would finish marked curve identification

There are now two concrete comparison packets:

* **J3:** match the constant, first and second coefficients, using
  for example a common 31-adic precision of 9746. The constant
  coordinates follow from the rational residue frame. The candidate
  J3 matrix has rank 45, so equality identifies its 91-dimensional
  kernel with the actual quadratic ideal, as in D88.
* **J4:** include the third coefficients, with common precision
  16236. Each candidate quadric then vanishes on 4D0. Its degree
  is 60, while deg(4D0)=68, so it vanishes identically. The verified
  smooth degree-30 candidate is the canonical image.

The exactness criteria are the D88 application of
[van Bommel--Costa--Poonen--Srinivasan, Lemma 4.1 and Corollary 4.2](https://arxiv.org/pdf/2506.14026).
Together with D99 and the saved candidate geometry, either packet
identifies (C,D). Neither by itself certifies the candidate P32
and degree-nine branch markings or constructs the downstream
cubic sections and target torsion field.

The next task is an executable independent arithmetic evaluator,
beginning with one certified rational-frame tangent and valid chart.
A 31-adic implementation has an explicit advantageous separation
bound, but no such implementation has been established. The existing
complex Shimizu/Nelson route must likewise certify its frame and
orientation before using the degree-17 bounds. Keep D98's spectral
pilot gate and the existing enumeration/precision pauses; these new
bounds do not make the old error interval exclude zero.

## 9. Audit and reproducibility

Script 387's successful run took 0.15 seconds. Its initial syntax
error is preserved with the original source snapshot, log and
receipt; it produced no mathematical result. The independent
candidate probe passed in 1.11 seconds. All jobs use runner 272's
180-second private-process-group cap. Magma's receipt records its
existing memory-limit setting.

Review 389 replays the graph/group/formal checks and exact candidate
arithmetic. It checks all 543 D105 source hashes unchanged and binds
the D58 descent inputs, this report, the
[source ledger](../data/computed/cm_rational_frame_sources_d106.json),
and the new drivers, logs and receipts. Completed sources and bound
artifacts are frozen. Recheck from the repository root:

```sh
python3 dembele/pari/389_cm_ratio_jet_review.py --check
```

The audit verifies finite witnesses and source preservation. Stable
reduction, CM reciprocity, canonical conjugation and the mathematical
proofs above are not machine-verified.

