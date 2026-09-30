# D110: explicit dyadic arithmetic group and transports moving the base vertex

Date: 2026-09-25. Continuation authorized by “continue”.

The bounded next step is complete. The existing 58-class Brandt calculation
has been replayed and matched entry for entry, with the same order as D109.
Seven exact ideal correspondences give an element in the odd norm-parity
coset. Its normalization W is an explicit projective involution representing
the Atkin--Lehner action in the dyadic uniformization. A norm-one conjugate
of D109's unit moves the base vertex by **fourteen edges**. A further
explicit product is hyperbolic, with translation length fourteen.

These witnesses specify arithmetic action, not a complete fundamental
domain or generating set. No harmonic cocycle, moment bank, matched
dyadic CM frame, actual Shimura jet or candidate identification is supplied.

## 1. The group and the quotient

Keep D109's exact order O in `B=(-1,-1)_F`, its certified splitting iota,
`K=F_p`, `pi=b`, and the normalization `v(pi)=1`, `v(2)=8`. Set

    A = O_F[1/b],       R = O[1/b],
    G = iota(R^*) / A^*,
    Gamma = image of iota(R^1) in PGL2(K).

Scalars in the definition of G are embedded as scalar matrices. D99 proves
`h(F)=h+(F)=1` and that every totally positive unit is a square. Put
`lambda=2+b`; it is totally positive and generates p, with absolute norm 2.
For any q in R*, the reduced norm is totally positive and has the form
`epsilon*lambda^n`, where epsilon is a totally positive unit. Consequently

    Gamma = ker(G -> Z/2Z, [q] |-> v(Nrd(q)) mod 2).

Indeed, when n is even its reduced norm has a square root in A*, by the
unit fact, and dividing q by that scalar gives norm one. Conversely scalar
normalization changes the norm valuation by an even integer.

There is also no extra projective normalizer of R: at every prime away
from p, O is a maximal matrix order and its local normalizer is a scalar
times its unit group. Class number one lets these scalar valuations be
cleared by one element of F*. Thus `N_B(R)/F*=G`. This statement concerns
the localized order R. W need not stabilize the maximal order O at p.

[Dembélé, Theorem 4.3 and Proposition 4.4](https://arxiv.org/pdf/1906.06772)
provide the geometric Cerednik--Drinfeld uniformization, its two-layer
Brandt graph, and the Atkin--Lehner interchange of the layers. In our
class-number-one setting, the adelic description reduces to
`R* \ (Omega_K x Z)`, with q shifting the integer coordinate by
`v(Nrd(q))`. The element W below makes this norm map surjective. Fixing
the integer coordinate then gives Gamma projectively. Hence over the
completed maximal unramified extension of K,

    S = Gamma \ Omega_K,       C = G \ Omega_K,
    G/Gamma = C2,              w_p acts by [W].

The last assertion follows by representing w_p as an integer-coordinate
shift by one, and bringing the coordinate back with W^(-1). Here [W] is
an involution, so [W^(-1)]=[W]. This is the geometric uniformization of
the already identified arithmetic curve and quotient. It supplies no
new descent matrix or labeling of the seventeen CM points.

The norm-one arithmetic setting and column-lattice tree action agree
with [Masdeu--Torrents, sections 2.1--2.2](https://arxiv.org/pdf/2510.09356).
Their full domain algorithm is not run in this milestone.

## 2. Reconcile the arithmetic witnesses with the saved graph

[Export 400](../magma/400_dyadic_brandt_transport_export.m) replays the
same level-one, norm-two, seed-990370 computation as D99, then accesses
the cached `get_rids` and `get_tps` data in that same Magma session.
It introduces no new level or Hecke prime. This reconstructs the
existing 58 classes because D99 did not serialize their representatives;
it is not an expansion of the class census or a new tree enumeration.

The new matrix and stabilizer sequence agree **entry for entry** with
D99, and the order's complete Z-basis agrees with D109. Class 0 is the
unit ideal O. The selected walk, in zero-based class indices, is

    0 -> 1 -> 3 -> 4 -> 4 -> 3 -> 1 -> 0.

A breadth-first calculation in the saved graph's parity double cover
proves that seven is the minimum length of an odd closed walk at class 0.
The four exported right ideals have reduced-ideal absolute norms
`1,2,4,8`, respectively. Both the Sage certificate and rational replay
check their right O-module property and all 4096 basis products.

For each step j -> i, the exported first cached quaternion t_ji satisfies

    pi*I_i subset t_ji*I_j subset I_i.

Both inclusions have Z-index 4, as required for residue norm two.
The certificates contain the two integral 32-by-32 inclusion matrices
for every step. This checks the direction of the Hecke correspondence
and its arithmetic meaning, rather than inferring a transport from
an unweighted adjacency entry.

Multiplying the seven quaternions in the order of their left action gives
`w=t_7*...*t_1`. It belongs to O and has reduced norm n with

    v(n)=7,       Norm_(F/Q)(n)=128,       Trd(w)=0.

The norm has no support away from p. The inverse of w and every other
element used below has only powers of two in its O-basis denominators.
This proves actual membership in R*, with no assumption that an arbitrary
local matrix comes from the global arithmetic group.

An exact scalar a of valuation 3 satisfies `a^2=n/lambda`. Define `W=w/a`.
The full coordinates of w and a are recorded in
[the arithmetic packet](../data/computed/dyadic_group_transport_d110.json).
The normalized answer has a short formula. Let

    c = (b^7-7*b^5+14*b^3-7*b)/2,
    c^2 = 1-b^2/4.

Then

    W = (1+b/2)*i + c*j,
    Nrd(W)=lambda=2+b,       W^2=-lambda.

In particular [W] has order two and odd norm parity. It represents the
nontrivial coset of G/Gamma, and `G=Gamma semidirect <[W]>`. The rational
replay also exports the conjugation matrices on the 32-dimensional
localized order for W and the norm-one witness below; both directions
have dyadic denominators, and the W conjugation matrix squares to one.

The relation `W^2=-2-b` gives an explicit embedding of the abstract CM
quadratic field into B. Matching this embedding and its fixed points
to the saved CM classes and rational residue frame is still required.

## 3. Certified movement in the tree

Let `u=(1-i-j-k)/2`, the unit certified in D109. Set

    g = W*u*W^(-1)
      = 1/2 + (-c/2-b/4)*i + (-c/2+b/4)*j + k/2.

Then `g in R^1` and `g^3=-1`. The projective element has order three;
although it moves the base vertex, it is not a hyperbolic element.

All images use D109's same exact Hensel root t with `v(t-x0)=180`.
The finite matrices are centers of expressions linear in t, with explicit
error bounds. For a two-by-two matrix M over K, write `m=min v(M_ab)`.
The elementary divisors over O_K give

    distance(v0,M*v0) = v(det M)-2*m.

The certified entry errors exceed m, so the center gives this minimum
exactly; determinants are computed as exact quaternion reduced norms.

| Element | Norm valuation | Minimum entry valuation | Base-vertex displacement |
|---|---:|---:|---:|
| w | 7 | 0 | 7 |
| W | 1 | -3 | 7 |
| g | 0 | -7 | 14 |

We also give explicit target lattices. Define

    r_W = pi^2+pi^3+pi^4+pi^6,
    r_g = r_W+pi^7+pi^8+pi^10+pi^13,
    L_W = [r_W pi^7; 1 0],
    L_g = [r_g pi^14; 1 0].

The exact transitions

    L_W^(-1)*pi^3*iota(W),    L_g^(-1)*pi^7*iota(g)

are integral and have determinants `-lambda/pi` and `-1`, respectively.
Their entry-error lower bounds are 169 and 162. Thus they lie in
GL2(O_K), proving the transported lattice equalities up to the displayed
homotheties. This establishes actual movement of the base vertex.

The independent replay also forms the product

    h = u*g = (1-c)/2 -(1+c)*i/2 + b*j/4 - b*k/4.

It verifies `h in R^1`, `Trd(h)=1-c`, and `v(Trd(h))=-7`. For
`X^2-Trd(h)*X+1`, Hensel's inequality at X=Trd(h) is `0>2*(-7)`.
Equivalently, substituting `X=Trd(h)*Y` gives the integral polynomial
`Y^2-Y+Trd(h)^(-2)`, which has a simple root congruent to 1 modulo pi.
There is an eigenvalue in K of valuation -7 and a second of valuation 7.
Diagonalizing therefore shows that h is hyperbolic with **translation
length 14**. Its displacement at v0 is also 14, checked using the same
certified splitting. This supplies an explicit infinite-order element
without a further search. It is not a complete group generating set.

Two negative controls reject putting W into the projective norm-one
group (its norm valuation is odd) and pretending that g fixes v0
(its determinant is a unit but an entry has valuation -7).

## 4. Verification, provenance and next task

[Certificate 401](../pari/401_dyadic_group_transport.py) uses exact Sage
number-field arithmetic. [Replay 402](../pari/402_dyadic_group_transport_review.py)
uses rational Python arithmetic independently for the selected ideal
inclusions, scalar normalization, localized conjugation, matrix bounds
and transported lattices. It additionally verifies the explicit
hyperbolic product. The class-number and unit-sign facts are preserved
from D99, and the unit signature matrix's rank is checked again.
The geometric uniformization argument is a mathematical proof using
the cited results; it is not a proof-assistant verification.

Export / certificate / independent probe took 28.77/8.03/2.88 seconds.
All passed on their first attempts, under 180-second private-process-group
caps; Magma had a 2 GB memory cap. Review 402 binds the new sources,
artifacts, receipts, report and source ledger, preserving all 629 D109
hashes. Completed sources and bound artifacts are frozen. Recheck:

    python3 dembele/pari/402_dyadic_group_transport_review.py --check

The source ledger is
[dyadic_group_transport_sources_d110.json](../data/computed/dyadic_group_transport_sources_d110.json).

Next export and certify the remaining adjacency transports and vertex
stabilizers for the **existing** 58-class data. Turn them into a finite
edge-reduction procedure, checking that the three neighbors at every
vertex are accounted for. Then construct the G-invariant scalar harmonic
cocycles, checking the expected dimension 16 and an explicit bound for
their measures. This reuses the known quotient; it does not call for a
new class census or a search at higher level.

Actual moment lifting, dyadic CM/frame matching, cofactor error propagation
and a valid Gaussian chart remain separate gates. No actual tangent/jet,
candidate identification or target polynomial has been obtained. Keep
the enumeration, Hecke-bank and cubic-precision pauses. D108's rejection
of the unchanged absolute spectral comparison remains in force.
