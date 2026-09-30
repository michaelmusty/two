# Hyperelliptic versus nonhyperelliptic: fresh review (D99)

Date: 2026-09-24. Requested scope: reconsider the entire argument from
its definitions and primary sources, without accepting the earlier verdict.

**Conclusion: the intended genus-16 quotient C is geometrically
nonhyperelliptic.** A fresh arithmetic computation and a simpler graph
obstruction support this as a mathematical conclusion, not a numerical
preference. The exact candidate curve is also nonhyperelliptic, but its
identification with C remains open. These are separate statements.

The decisive implication is

    C hyperelliptic
      => its reduction metric graph has a degree-two rank-one divisor
      => its canonical graph admits an involution with tree quotient
      => deleting at most two edges disconnects that graph.

The last condition is false: all 1,035 deletions of one or two edges
leave the freshly computed graph connected. This proof does not need
the numerical differentials or an injection of curve automorphisms into
graph automorphisms.

## 1. Fix the object before testing it

Here F=Q(b), with b^8-8b^6+20b^4-16b^2+2=0, and
D=(b-b^2,-1)/F. The algebra is ramified at the unique prime p above 2
and seven real places. Let S be the maximal-level norm-one Shimura
curve and let C=S/<w_p>. Their genera are 40 and 16, respectively.
This is the quotient in [Dembélé, §5.1 and §5.4](https://arxiv.org/pdf/1906.06772).
Write C_candidate for the curve defined by our 91 integer quadrics;
that notation deliberately does not assert an isomorphism with C.

The new arithmetic run proves h(F)=h+(F)=1. A separate rerun on the
actual saved order verifies closure of its 32-dimensional integral
lattice, absolute reduced-trace determinant 2^126, finite algebra
discriminant of norm 2, and the unique split embedding b in (0,1).
The determinant equals disc(F)^4 Norm(disc(D))^2, proving maximality.
Eight independent unit signatures imply that positive units are squares.
Thus the norm-one and positive-unit projective groups agree, and the
positive normalizer adds the one Atkin--Lehner class. Narrow class
number one removes a connected-component or maximal-order-class
ambiguity. This checks the saved group's datum; it does not certify
the floating-point polygon or identify C_candidate.

## 2. Rebuild the reduction graph from arithmetic

Switch the ramification at p and the split real place. The resulting
algebra B is totally definite and unramified at all finite primes.
[Script 371](../magma/371_hyperellipticity_fresh_brandt.m) recomputes its
maximal-level norm-2 Brandt matrix, using a new seed and the dense entry
point. It reads no old matrix, graph, candidate or differential output.
This is a fresh run of the same underlying Hilbert modular forms
library, not an independent implementation of Brandt arithmetic.

There are 58 ideal classes. With stabilizer orders e_i, the checks give

    sum_i 1/e_i = 1455/32 = zeta_F(-1)/128,  zeta_F(-1)=5820;
    sum_i T_ij = 3,  e_i*T_ij = e_j*T_ji.

For each nonzero off-diagonal pair, min(T_ij,T_ji)=1. One endpoint
therefore has just one neighbor in the other class, so there is exactly
one edge orbit, of length e_j/T_ij=e_i/T_ji. Diagonal entries are zero
or one. The pairing orientation is checked on the data; a misleading
reversed identity in the library's helper documentation is not used.

The geometric correspondence between the double-coset graph and the
reduction follows from Cerednik--Drinfeld uniformization. In particular,
[Nekovář, §1.5.3--1.5.5](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2A11114CBB9FC75C2DBF56F766BFE7BF/S0008414X00009196a.pdf/level-raising-and-anticyclotomic-selmer-groups-for-hilbert-modular-forms-of-weight-two.pdf)
gives the rational components, nodal local equations, two vertex layers
and stabilizer lengths. No sufficiently-small-level assumption is
needed for those statements; that extra assumption in part (3) makes
the lengths one. Nodes of greater thickness can instead be resolved,
subdividing the corresponding edges.

The action of w_p exchanges the two layers: its local reduced norm
changes the valuation coordinate by one. The following counts are
reconstructed before stabilizing:

| Graph | Vertices | Edges | First Betti number |
|---|---:|---:|---:|
| Upstairs S | 116 | 155 | 40 |
| Topological quotient, including fixed midpoints | 67 | 82 | 16 |
| Algebraic quotient graph, removing inverted intervals | 58 | 73 | 16 |
| Stable graph G | 30 | 45 | 16 |

There are nine reversed edges, no fixed vertices and 73 pairs of other
edges. A reversed edge becomes a pendant interval in the topological
quotient. This interval is not a node of the algebraic quotient.

The original [Kurihara, §3, pp. 284--288, Proposition 3-2 and Lemma
3-3](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf)
was inspected directly from the scanned pages. Its setup permits a
discrete cocompact subgroup of PGL2 of a p-adic field with torsion,
without an odd-p or prime-to-p restriction. It establishes the integral
quotient's rational components and nodes. Its star operation removes
oriented edge classes equal to their own reversal. Lemma 3-3 treats
the case where the two branches are interchanged by making that local
quotient smooth. An ordinary loop with distinct oriented classes is
not removed. Thus residue characteristic 2 does not invalidate the
construction. We do not assume invariants commute with reduction.

The new graph program starts with the full quotient including midpoints
and records every contraction. Its stable result is simple and cubic,
and is weight-preserving isomorphic to the paper's Figure 2, whose
transcription was checked against the PDF image. The obstruction is
computed on the arithmetic graph, independently of that comparison.

## 3. A shorter obstruction than enumerating involutions

**Lemma.** A connected loopless graph with at least three vertices
which remains connected after deletion of any one or two edges cannot
have an involution whose quotient, with edges inside a vertex orbit
contracted, is a tree.

**Proof.** An involution has at least two vertex orbits. A tree quotient
therefore has an edge a. Its preimage is one edge or a pair of edges.
Removing a partitions the quotient vertices into two nonempty sets.
Their preimages partition the original vertices into two nonempty sets,
and every edge between them must lie over a. Deleting those at most
two edges disconnects the original graph, a contradiction.

The canonical loopless model here is exactly G: every vertex has
valence three and there are no loops. In particular, a metric isometry
must preserve this vertex set. By [Chan, Theorem 1.3 / 3.13](https://arxiv.org/pdf/1110.0273),
a hyperelliptic metric graph with no leaves has an involution of this
model with tree quotient. Chan contracts edges whose endpoints belong
to the same orbit. For a simple graph and an involution those are
inverted edges; keeping their midpoint pendants instead does not change
the quotient's first Betti number.

The new [standard-Python checker 372](../pari/372_hyperellipticity_graph_review.py)
uses breadth-first connectivity searches for all
45 + binomial(45,2) = **1,035** edge deletions. Every result is connected.
It also supplies a three-edge cut, so the edge connectivity is exactly
three. The lemma rules out hyperellipticity for **every assignment of
positive edge lengths** to this graph.

As a separate check, a new exhaustive search over bijections preserving
graph distances finds 64 automorphisms and 19 involutions. Their
quotient Betti numbers have histogram

    8: 5,   10: 4,   12: 6,   14: 4;   zero: 0.

This implementation does not call Sage's automorphism routines or
NetworkX. Both quotient conventions are constructed and compared for
each involution. Controls include a genus-two dumbbell with a tree
quotient, K4 without one, and a two-vertex three-edge banana. The banana
is hyperelliptic despite edge connectivity three: the lemma's
at-least-three-vertices condition is essential.

## 4. Transfer the obstruction to C

Assume C is geometrically hyperelliptic. After a finite field extension
its degree-two rank-one divisor is defined. Resolve the nodes of a
semistable model, and if necessary pass to a further extension.
[Baker, Lemma 2.8, Corollary 2.10 and §3.1](https://arxiv.org/pdf/math/0701075)
specialize this divisor to a degree-two divisor of rank at least one
on the reduction metric graph. These statements impose no restriction
excluding residue characteristic 2. The graph has genus 16, so this
is a hyperelliptic metric graph. Base change and resolution subdivide
edges and change the length normalization, not its canonical model G.
Section 3 gives a contradiction. Hence C is geometrically
nonhyperelliptic, and in particular is not hyperelliptic over F.

This avoids specializing an involution and then asserting it remains
faithful on the graph. It also avoids the admissibility claim in
Dembélé's Proposition 4.7(2) and any tame fixed-point count at 2.

## 5. Audit the argument for hyperellipticity

[Dembélé's Theorem 5.9](https://arxiv.org/pdf/1906.06772) starts with an
elliptic order-two element of the uniformizing group and asserts a
vanishing-order restriction on differentials on C. The subsequent
Riemann--Roch implication, *if* l(K-2P)=l(K-P), is valid: it would give
l(2P)=2 and a degree-two map. The problem is the premise.

An element of the uniformizing group is a deck identification, not a
nontrivial automorphism of the coarse quotient. Over characteristic
zero take an upstairs coordinate t with gamma(t)=-t. The coarse
coordinate is u=t^2, on which gamma acts trivially. A local downstairs
differential h(u)du pulls back to

    2t h(t^2) dt.

It is invariant for every h. In particular u du has downstairs order
one, and pulls back to 2t^3 dt, which is invariant. Thus invariance
does not rule out a simple zero downstairs. More generally order m
downstairs becomes order 2m+1 upstairs. There is no even-order
restriction on the coarse curve.

This local example refutes the claimed inference, not the existence
of particular global differentials by itself. The independent graph
argument supplies the nonhyperellipticity conclusion. The later CM
point count cannot repair the missing premise. We do not infer that
all CM points are ordinary or decide other claims about them here.

## 6. Evidence ledger and remaining uncertainty

| Statement | Status after this review |
|---|---|
| Intended C is geometrically nonhyperelliptic | Exact arithmetic graph plus the source-checked theorem chain above |
| Published local argument proves hyperellipticity | No: upstairs/coarse-ring confusion invalidates its premise |
| Our explicit C_candidate is nonhyperelliptic | Independently established for its exact equations |
| C_candidate is the intended C, with the required marks | Still unproved |
| Numerical differential product rank 45 proves the result | No; it remains supportive, uncertified numerical evidence |

For C_candidate, the D69 checker was rerun from the equations. It
again proves a smooth geometrically integral degree-30 genus-16 curve
over Q with h0(O(1))=16. Riemann--Roch makes O(1) canonical; a canonical
closed embedding implies nonhyperellipticity. The proof uses the monic
Groebner model and squarefree trace discriminants on both projection
charts modulo 31. See [D69](cm-frame-verification.md) for the argument.
This is a rerun of that algorithm, not a new identification theorem.

The numerical product-space dimensions are consistent: a genus-16
hyperelliptic canonical system has quadratic-product image dimension
31, whereas the nonhyperelliptic value is 45. However, uncertified
series truncation and a numerical rank decision cannot carry the proof.
The graph proof above reads neither these series nor the candidate.

My confidence is high enough to use nonhyperellipticity as an
established project input. The remaining review risk lies in the
arithmetic uniformization identification or a software error, rather
than a numerical rank threshold. Primary-source checks, exact mass and
genus checks, a fresh matrix, two distinct graph obstructions and the
saved-order rerun substantially constrain those possibilities. This is
not a proof-assistant certificate or an externally acknowledged
correction of the published theorem. An independent expert's review
would be useful for publication. No external correspondence was sent.

## 7. Reproduction, provenance and scope

Run the read-only root audit:

```sh
python3 dembele/pari/374_hyperellipticity_review_audit.py --check
```

It verifies the bound source/result/log hashes, recomputes the entire
graph check, and verifies the new job outcomes. The mathematical
uniformization, specialization, graph lemma and candidate smoothness
arguments are bound in this report or their cited report; Python does
not prove those theorems. The D98 provenance is also verified without
changing its analytic result. Downloaded primary-source PDF hashes and
the inspected sections are recorded in
`hyperellipticity_sources_d99.json`; the PDFs are not runtime inputs
to the arithmetic checker.

All calculations used the 180-second process-group limit. The first
Brandt attempt failed because `IsTotallyDefinite` is not a Magma
intrinsic; its source and failure log are preserved as 370/attempt01.
The corrected 371/attempt02 passed in 27.34 seconds. Graph review
372 passed in 0.14 seconds, candidate rerun in 4.47 seconds, and
saved-order rerun 373 in 6.47 seconds. No old bound source or output
was overwritten. The new successful sources and results are frozen.

This review changes no CM error enclosure, candidate equation,
arithmetic identification or target-field status. The latest analytic
bound remains D98: full S11 error <24,784,942,340, too large for a
certified CM anchor. General canonical equations remain the appropriate
model format. The candidate identification, arithmetic CM jets, cubic
recognition and target field polynomial remain open.
