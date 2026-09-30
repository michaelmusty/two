# D111: arithmetic edge reduction and sixteen invariant harmonic cocycles

Date: 2026-09-25. Continuation authorized by “keep going!”.

The next bounded task after D110 is complete. All three neighbors at each
of the existing **58 ideal classes** now have certified arithmetic
transports. The **164 projective stabilizer elements** and their local
actions are checked. These data give a terminating edge reducer and an
explicit basis of **16 G-invariant scalar harmonic cocycles** on the
whole Bruhat--Tits tree. The associated boundary measures have uniform
denominator bound **d=0**.

The computation retains the group and geometric uniformization of D110:
`K=F_p`, `pi=b`, `v(pi)=1`, `v(2)=8`, `R=O[1/b]`, and
`G=R*/O_F[1/b]*`. The splitting is the exact Hensel splitting of D109.
There is no new class census, level or Hecke prime. No actual moment bank,
dyadic CM/frame matching, Shimura tangent/jet, candidate identification
or target polynomial is obtained here.

## 1. Arithmetic data and global right ideals

[Export 403](../magma/403_dyadic_quotient_export.m) replays the existing
seed-990370, norm-two, level-one calculation, then serializes all its
right ideals, cached `get_tps` correspondences and norm-one unit groups.
Its Brandt matrix and stabilizer sequence agree entry for entry with
D99; its entire order basis agrees with D109. Indexing is taken from
this same Magma session. There are 174 outgoing neighbor entries,
three for each class, and 164 unit representatives modulo scalars.

For every exported rank-32 Z-lattice I_j, both the Sage certificate and
the independent rational review verify

    I_j subset O,       [O:I_j] = 2^(2*n_j),       b*I_j subset I_j.

Since `O_F=Z[b]`, this makes I_j an O_F-lattice. Since p is the only
prime above 2, its localization away from p equals O. In particular
`I_j[1/b]=R`. The local frame computation below proves the right
O-module property at p; away from p it already follows from equality
with O. This local-to-global argument certifies all 58 right ideals
without repeating 58 times all 1024 order-basis products.

For each I_j the certificate supplies an exact `L_j in GL2(F)` with

    iota(I_j tensor O_K) = L_j M2(O_K),       v(det L_j)=n_j.

To prove the equality, it checks that every transformed basis image is
integral and that their reductions span all four dimensions of M2(F2).
Nakayama's lemma applies to this finite O_K-module. Error lower bounds
for these transformed images are at least **166**; thus their reductions
are exact. The base frame is `L_0=1` and the base ideal is exactly O.

## 2. Complete stars, stabilizers and reversal

An exported entry from class j to class i is a quaternion t satisfying

    pi I_i subset t I_j subset I_i.

The following two local matrices are integral with determinant valuation
one, and have rigorously determined rank-one reductions modulo pi:

    pi L_j^(-1) iota(t^(-1)) L_i,
       L_i^(-1) iota(t)      L_j.                         (1)

Each entry has certified error at least **160** in these coordinates.
Also, t and t^(-1) have dyadic denominators in the fixed O-basis, so
both belong to R. Away from p they are mutually inverse units. Thus
the local inclusions in (1) prove the asserted global sandwiches;
each inclusion has Z-index four. Determinants in the rational review
use exact reduced norms, not approximate matrix determinants.

The first matrix in (1) describes the neighbor `[iota(t^(-1))L_i]` of
`[L_j]`. The three reductions at every j give exactly the three lines

    (1,0), (0,1), (1,1) in F2^2.

Hence every local star is covered with no missing or duplicated direction.
The second matrix gives the reverse direction after applying t. The
number of entries for each pair of classes recovers D99's full matrix.

Every exported stabilizer representative u has reduced norm one,
belongs with its inverse to R, and satisfies

    L_j^(-1) iota(u) L_j in SL2(O_K).

These matrices induce the recorded permutations of the three lines;
their error lower bounds are at least **162**. Exact quaternion checks
prove distinctness modulo scalars, identity and closure. Their sizes
equal D99's full stabilizer counts. Completeness retains the certified
Magma unit-group/class provenance: it is not a second exhaustive unit
enumeration in rational Python. D99's positive-unit-square fact and
D110's norm-parity argument identify these with the full projective
G-stabilizers of the representative vertices. Indeed, a vertex-fixing
element has even norm valuation, so can be normalized to norm one;
it then preserves I_j locally at p and at all other primes.

If t' is the transport selected for the reverse direction, the exact
quaternion `t'*t/pi` is projectively one of the recorded stabilizers at j.
This checks the compatibility of reversal. Reversal of the 174 slots
need not itself be an involution: stabilizers can identify slots. After
quotienting by their actions there are **155 oriented edge orbits**;
reversal is an involution on those orbits. It has **9 fixed orbits**
and **73 pairs**. The fixed orbits are edges inverted by G.

## 3. Exact harmonic space and measure bound

Use one variable for each of the 174 outgoing slots. Impose:

1. the sum of the three outgoing values at every vertex is zero;
2. every stabilizer permutation preserves the values;
3. a value plus its transported reverse value is zero.

These give **376 nonzero integer relations**. Sage computes their kernel
over Q and clears each basis vector's denominators. Rational review
checks every equation exactly and independently finds relation rank
158 and basis rank 16 modulo 101. Exact annihilation and these two
lower bounds prove the ranks over Q, and hence over K. No dimension
formula is used to replace the rank certificate.

The resulting 16-by-174 integer matrix is stored in
[the harmonic packet](../data/computed/dyadic_harmonic_certificate_d111.json).
Its entries have absolute value at most four. All nine inverted edge
orbits receive zero: antisymmetry gives `x=-x`, hence x=0 in
characteristic zero, including over this dyadic field. The basis spans
the full K-valued invariant harmonic space. No claim of a saturated
integral cohomology basis is needed or made.

For an oriented tree edge e, let B_e be the boundary ball consisting
of ends on its terminal side. Set `mu_a(B_e)=c_a(e)`. Reversal makes
the complementary ball's mass negative; harmonicity makes the two
forward subballs add to the parent's mass. These identities give a
well-defined finitely additive measure of total mass zero on compact
open subsets of P1(K). Section 4 below extends each c_a to the whole
tree. Every value is an integer from the finite basis table, so

    v(mu_a(B_e)) >= 0,       d=0.                         (2)

Finite additivity and the nonarchimedean inequality give the same bound
for every compact open set. Thus these are bounded K-valued measures,
which can integrate continuous functions. General K-linear combinations
have the corresponding bound from their coefficients; (2) refers to
the chosen basis. A coordinate change in PGL2(K) preserves this bound,
since it permutes boundary balls.

[Franc--Masdeu, sections 4.1--4.2](https://arxiv.org/pdf/1201.0356)
describe harmonic cocycles and their boundary distributions over Q_p.
The preceding ball-partition argument establishes the needed scalar
case directly over our K. We do not import their overconvergent
control theorem or its precision constants to the ramified field.

## 4. Terminating arithmetic reduction on the whole tree

[Reducer 405](../pari/405_dyadic_edge_reducer.py) accepts adjacent vertices
given by column lattices U,V in GL2(F). Every tree edge over K admits
such representatives, by finite uniformizer expansion; see
[Masdeu--Torrents, section 2.1 and Lemma 2.2](https://arxiv.org/pdf/2510.09356).
F-matrix input avoids assigning meaning to uncertified approximate
local-field entries.

Start at class j=0 with q=1. For `M=L_j^(-1)iota(q)U`, compute

    distance = v(Nrd(q)*det(U)/det(L_j)) - 2*min v(M_ab).

If positive, the primitive reduction of M gives the unique first
direction toward `[iota(q)U]`. Select its certified transport t from
the star, replace `(j,q)` by `(i,t*q)`, and repeat. Because t carries
that neighbor to `[L_i]`, the new distance drops by exactly one.
The code asserts this at every step. Thus termination occurs after
the initial distance from the base vertex to U, subject to the
caller's explicit step cap.

At distance zero q sends U to `[L_j]`. The primitive reduction for
qV picks the final outgoing slot. The reducer returns its 16 values,
the exact quaternion product q in R*, its transport word, decreasing
distance trace and residue-error margin. Independence of the chosen
transport follows from invariance under the full vertex stabilizer.
Reversal and all harmonicity identities therefore hold everywhere,
not just on the finite quotient table. This also proves G-invariance.

The fixed splitting has images of the form

    center(x) + (t-x)*slope,       t^2+y^2+1=0.

Residue decisions require the root-error bound plus the slope valuation
to exceed the smallest center-entry valuation. When that fails,
the reducer performs exact Newton refinement in F and truncates in
the integral power basis with a proved error. It rechecks the strict
Hensel inequality and `v(x-x_D109)>8`, ensuring the same root branch.
The certified root error increases, so each fixed nonzero matrix
eventually has sufficient precision. The initial 180-digit packet
is never assumed sufficient for arbitrarily long words.

This is finite quotient data with an arithmetic reduction algorithm.
It does not additionally construct a connected fundamental subtree,
a presentation or a separate complete generating set.

## 5. Validation and audit

The saved runtime packet tests all three edges at six source vertices,
including the infinity sector and depth 32. It verifies reversal and
the harmonic sum for every one of the 16 cocycles; eight of the 18
tested edges have nonzero values. On a nonzero vector of values,
arithmetic invariance under u, W and the hyperbolic element h of D110
is checked after certifying the transformed lattices.

A deliberately shortened Hensel center starts with root error 28;
one refinement increases it to 48 and reproduces the full-precision
depth-32 reduction. A nonadjacent input is rejected. The independent
review also rejects an altered cocycle coefficient.

Export, Sage certificate, runtime validation and independent probe
passed on their first attempts in **29.86, 9.19, 6.59 and 15.01 seconds**,
respectively. Every job has a 180-second private-process-group cap.
The final review binds their sources, artifacts, logs and receipts,
this report and the source ledger, preserving **all 643 D110 hashes**.
The final review and recheck receipts record their own run times.

Sources 403--406 and bound artifacts are frozen. Recheck without Sage
or Magma, using runner 272 with the same 180-second cap:

    python3 dembele/pari/406_dyadic_harmonic_review.py --check

The script itself does not impose that wall-clock cap; the saved job
receipts show the runner invocation. Its exact field helpers are shared
with earlier rational reviews; its arithmetic and rank calculations
are independent of the Sage certificate.

## 6. Updated next step and scope

The actual cocycles and measure bound required by D108 are now available.
Next certify the dyadic fixed points of W and an explicit coordinate
change to the quadratic CM model `beta^2=-(2+b)`. Match the embedding
and its orientation to the saved seventeen CM labels and rational
residue frame using explicit arithmetic/reciprocity evidence. The
equation for W alone does not provide that matching.

The moment stage must use the resulting charts and prove its error or
contraction bound over K before a precision run. A small bounded pilot
is appropriate; exponentially growing Riemann refinement is not the
high-precision plan. Cofactor normalization, a certified Gaussian pivot
and the dyadic equality threshold remain later gates. The bound d=0
can enter D108's conditional tail formula but supplies no moment values
or frame-change matrix by itself.

D99's nonhyperelliptic conclusion and D108's rejection of the unchanged
absolute spectral comparison remain in force. Preserve all enumeration,
Hecke-bank and cubic-precision pauses and the 180-second job cap.
Downstream branch marking, global sections, norm-97 separation and
target-scale torsion remain separate tasks.
