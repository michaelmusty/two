# The genus-16 quotient is not hyperelliptic (D45)

Date: 2026-09-15.

D62 independently revisits the arithmetic/geometric identification in
[curve-identification-audit.md](curve-identification-audit.md), including
the actual saved order, the full genus-40 graph and Kurihara's integral
quotient theorem at residue characteristic 2. It supports the identification
used here and clarifies that reversed edge classes, not arbitrary loops,
are removed.

**Conclusion:** the genus-16 curve C under investigation is geometrically
nonhyperelliptic. This is an exact computational argument from its stable
reduction graph, independent of D44's numerical differential calculations.
It uses standard specialization and metric-graph theorems, exact Brandt
arithmetic, and exhaustive graph computations. It is not a formal proof
checked by a proof assistant.

## The argument

Let G be the loopless stable dual graph of C at the prime over 2. We
reconstruct G independently from the norm-2 Brandt operator and find:

    |V(G)|=30, |E(G)|=45, b1(G)=16.

Every vertex has degree three, and G is simple and 3-edge-connected. In
particular, it is the canonical loopless model of its metric realization.
The full unweighted automorphism group has order 64. It has exactly 19
elements of order two, with the following quotient genera:

| Quotient genus | Number of involutions |
|---|---:|
| 8 | 5 |
| 10 | 4 |
| 12 | 6 |
| 14 | 4 |
| 0 | **0** |

If C were hyperelliptic, its degree-two rank-one divisor would specialize
to a degree-two divisor of rank at least one on the reduction metric
graph. This is the specialization obstruction of
[Baker, Specialization of linear systems from curves to graphs, §2 and §3.2](https://arxiv.org/pdf/math/0701075).
By [Chan, Tropical hyperelliptic curves, Theorem 1.3](https://arxiv.org/pdf/1110.0273),
that metric graph would admit an involution with tree quotient. No such
involution exists. Therefore C is not hyperelliptic.

This checks **all** graph automorphisms, including any that might fail to
preserve the metric. An isometry necessarily permutes the 30 trivalent
vertices and the edges between them. Since the graph is simple and has
no loops, there are no additional automorphisms supported only on edges.
Thus no choice of positive edge lengths can remove the obstruction.

The specialization theorem imposes no assumption that the residue
characteristic is different from two. Passing to a field where the
degree-two map and a regular semistable model exist only subdivides edges
and rescales their lengths; the argument applies to the same canonical
metric graph. We do not use a tame-ramification fixed-point count.

## Independent reconstruction from arithmetic

Script `magma/72_stable_graph_brandt.m` works over

    F = Q[b]/(b^8-8b^6+20b^4-16b^2+2).

It computes the norm-2 Brandt matrix T on the 58 ideal classes of the
maximal totally definite quaternion order of level one. The curve C is
the positive-normalizer quotient for the algebra ramified at the norm-2
prime and seven real places. Switching the ramification at that prime
and the split real place gives the definite algebra used for the Brandt
graph. This is the Cerednik–Drinfeld/Atkin–Lehner graph construction; see
[Dembélé, Propositions 4.4 and 4.7 and §5.5](https://arxiv.org/pdf/1906.06772).

This run uses a Minkowski proof bound for class groups, with a smaller
initial search bound. Both the ordinary and narrow class numbers of F
are checked to be one. The list of stabilizer orders has distribution

    32, 24, 16, 8^2, 4^3, 3^4, 2^6, 1^40.

It satisfies the exact mass check

    sum_i 1/e_i = 1455/32 = zeta_F(-1)/128,
    zeta_F(-1) = 5820.

The computation took about 27 CPU seconds after the initial class-number
checks. No GRH assumption is used as the final class-group proof bound.

Columns of T count the three neighbors of a class. The exported matrix
satisfies

    sum_i T_ij = 3,
    e_i T_ij = e_j T_ji.

For every nonzero off-diagonal pair, min(T_ij,T_ji)=1. Thus at one endpoint
there is a single neighbor in the other class, which forces exactly one
edge orbit between those two classes. Its weight is

    e_j/T_ij = e_i/T_ji,

an integer. This determines the edges and weights without guessing
multiplicities from a support matrix. Diagonal entries are zero or one;
the nine diagonal neighbors correspond to inverted edges in the
Atkin–Lehner quotient. Their quotient intervals are pendant and do not
affect the stable core.

Script `pari/73_brandt_graph_check.py` constructs the resulting graph:
58 vertices and 73 non-pendant edges. It removes leaves and suppresses
degree-two vertices, adding edge weights along the suppressed paths.
The output has 30 vertices and 45 edges. It is **weight-preserving
isomorphic** to the independently transcribed Figure 2 of the paper.
The isomorphism and every stabilization operation are saved. Consequently
the obstruction does not depend merely on reading a published diagram.

One audit correction: the package's stabilizer helper documentation
states the reverse pairing identity. The raw norm-2 matrix satisfies the
identity displayed above and fails that reversed identity. The graph
script checks the correct identity directly. This is recorded without
silently changing any older pairing-dependent calculations; their scope
should be reviewed separately if reused.

## Exact finite graph checks

Script `pari/71_stable_graph.sage.py` enumerates graph automorphisms with
Sage and independently with NetworkX's VF2 algorithm. The two complete
sets of 64 permutations agree. All also preserve the printed weights.
The supports of the 19 involutions have sizes

    2^4, 4^6, 6^4, 8^1, 28^4.

For each involution s, let f_V count fixed vertices, f_E pointwise-fixed
edges, and r_E inverted edges. The quotient Betti number is

    b1(G/s) = (45+f_E-r_E)/2 - (30+f_V)/2 + 1.

Each quotient is also constructed explicitly as a multigraph. An
inverted edge becomes an interval ending at its fixed midpoint; that
midpoint is retained as a new pendant vertex. Connectedness and Euler
characteristic of each constructed quotient verify the formula.

Equivalently, the trace on H1(G,Q) is 1-f_V+f_E-r_E. The traces of these
involutions are 0, 4, 8, or 12; none is -16. The quotient calculation is
tested on a genus-two positive control with both inverted edges and a
fixed bridge, and on the nonhyperelliptic K4 negative control.

## Relation to the numerical and published claims

D44 found product rank 45, 91 canonical quadrics, and canonical degree-3
dimension 75. Those remain numerical computations. The present exact
reduction argument independently supports their nonhyperelliptic
interpretation and supersedes D44's unresolved verdict on hyperellipticity.

This contradicts the hyperellipticity statement in Dembélé's Theorem 5.9.
D44 identified the local problem in the opening step: the stabilizer
acts on an upstairs parameter, but acts trivially on the coarse quotient
local ring. In local coordinates u=t², an invariant differential upstairs
is t h(t²)dt=h(u)du/2. Its downstairs vanishing order is unrestricted;
for example u du has order one. That stabilizer action cannot imply
l(K-2P)=l(K-P). The graph argument establishes nonhyperellipticity without
depending on an interpretation of that proof step.

This conclusion concerns C. It does not invalidate the original
nonsolvable F256 target or D43's exact S3 cover data. It also does not,
by itself, decide every other assertion in the cited paper: the F16
systems have a separate published induced-character argument. We have
not inferred an automorphism of C merely because its graph has one.
No external messages have been sent concerning these findings.

## Reproduce

From the repository root:

```sh
sage -python dembele/pari/71_stable_graph.sage.py
HMF_ROOT=/Users/musty/hilbertmodularforms /Applications/Magma/magma -b dembele/magma/72_stable_graph_brandt.m
sage -python dembele/pari/73_brandt_graph_check.py
```

Exact outputs and passing logs are `stable_graph_audit.*`,
`stable_graph_brandt.*`, and `brandt_graph_check.*` under `data/computed/`.
The first JSON includes all involutions; the third includes the graph
isomorphism and stabilization history. The next curve-model work should
use general canonical equations, not a hyperelliptic equation.
