# The curve behind the reduction graph (D62)

Date: 2026-09-16. This implements the geometric audit requested in D61.
The new computation is `pari/99_curve_identification.py`; its identical
JSON and text reports are `data/computed/curve_identification.{json,out}`.

**Result:** the arithmetic datum and the full Cerednik--Drinfeld graph
support D45's identification of the genus-16 stable graph with C.
The audit finds no change of curve, level, connected component or
Atkin--Lehner quotient that would remove the hyperellipticity conflict.
It checks the geometric bridge using Kurihara's original quotient
theorem, rather than rerunning the graph automorphism enumeration.
This remains a mathematical argument using published theorems and exact
computer arithmetic, not a proof-assistant certificate or an external
resolution with the author.

## 1. The saved arithmetic group

The saved domain uses the field and quaternion algebra

    F = Q(b), b^8-8b^6+20b^4-16b^2+2 = 0,
    D = (b-b^2,-1)/F.

Script 99 reads the actual 32-dimensional order lattice from the saved
Rickards object. It checks closure under all products of basis elements
and computes the absolute reduced-trace Gram determinant. Its absolute
value is

    2^126 = disc(F)^4 * Norm(disc(D))^2,
    disc(F) = 2^31, Norm(disc(D)) = 2.

This is the maximal-order discriminant formula: an order properly
contained in a maximal order would have the larger Gram determinant
multiplied by the square of its index. Thus this is a maximal order in
the specified algebra, not an unnoticed Eichler-level lattice.
The seven ramified real places and the unique split place are checked;
the latter has b in (0,1), approximately 0.390180644.

The ordinary class number is proved to be one. Eight unit generators,
including -1, have a signature matrix of rank eight. Consequently the
narrow class number is also one, and every totally positive unit is a
square. The positive-unit and norm-one groups therefore have the same
projective image. The positive normalizer adds the single Atkin--Lehner
class at the only finite ramified prime. This agrees with the saved
`afuchinit(A,,3,0)` call and its normalizer-norm output: one Atkin--Lehner
generator, no extra unit or class-group generators.

These are the algebra and groups in Dembélé's §5.1 and Theorem 5.1.
The adelic maximal level has full unit reduced norm, so narrow class
number one gives a single geometric component. Its canonical curve is
the genus-40 S, and its normalizer quotient is C=S/<w_p>.
See [Dembélé, §§4.1--4.4 and §5.1](https://arxiv.org/pdf/1906.06772).
The choice of maximal order introduces no extra level: strong
approximation for the indefinite algebra and the narrow class number
identify the maximal-order components.

Switching ramification at p and the split real place gives the totally
definite algebra B, unramified at every finite prime. This is the algebra
used by script 72. The package's `quaternion_algebra` constructor in
`ModFrmHil/hackobj.m` explicitly asserts these ramification conditions;
in this field it can use (-1,-1), since the local degree at 2 is even.
The norm-2 Brandt matrix is on maximal level, with 58 ideal classes.
Its exact mass and unconditional class-group proof are recorded in D45.

## 2. Check the upstairs graph before quotienting

The full graph has vertices (i,epsilon), with 58 ideal classes and
epsilon in {0,1}. The Brandt operator counts neighbors with stabilizer
multiplicities; it is not directly the adjacency matrix of a simple
unweighted graph. For every nonzero class pair in these data,
min(T_ij,T_ji)=1, proving there is exactly one edge orbit. Its length is
e_j/T_ij=e_i/T_ji. Diagonal entries are zero or one.

Script 99 retains both layers and all nine diagonal edges. It constructs
w_p by interchanging the layers and checks that it preserves incidence
and edge lengths. This realizes the standard uniformization description
in [Nekovář, §1.5, especially Proposition 1.5.5](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2A11114CBB9FC75C2DBF56F766BFE7BF/S0008414X00009196a.pdf/level-raising-and-anticyclotomic-selmer-groups-for-hilbert-modular-forms-of-weight-two.pdf).
The base-change twist in the uniformization affects descent of the
special fibre, not this geometric graph.

| Object | Vertices | Edges | First Betti number |
|---|---:|---:|---:|
| Graph of S | 116 | 155 | 40 |
| Topological quotient, retaining fixed midpoints | 67 | 82 | 16 |
| Quotient after deleting the nine pendant intervals | 58 | 73 | 16 |
| Stable core | 30 | 45 | 16 |

There are no fixed vertices upstairs. Exactly nine edges are reversed,
and the other 146 edges occur in 73 pairs. On graph chains the traces
are tr(C0)=0, tr(C1)=-9 and tr(H0)=1. Hence tr(w_p|H1)=-8, with eigenspace
dimensions 16 and 24. This independently checks the quotient genus
against the genus-40 curve and its Atkin--Lehner decomposition.

## 3. Why the reversed edges disappear, including at 2

The decisive source is
[Kurihara, *On some examples of equations defining Shimura curves and the Mumford uniformization*, §3, pp. 284--288](https://repository.dl.itc.u-tokyo.ac.jp/records/39680).
The scanned original was inspected, including Proposition 3-2 and its
proof through Lemma 3-3. The setup allows a p-adic number field and a
discrete cocompact subgroup with torsion; there is no odd-p or
prime-to-p stabilizer hypothesis. The quotient has rational components
and nodal special fibre. The graph operation `*` removes oriented edge
classes equal to their own reversal. Lemma 3-3 treats interchange of
the two components by making that local quotient smooth.

This is more precise than “delete all loops” as a general rule.
An ordinary loop, with two distinct oriented edge classes, must be
retained. Here each of the nine diagonal Brandt entries gives a unique
edge between (i,0) and (i,1). The layer swap fixes that edge and reverses
its ends. It is therefore one of Kurihara's removed edge classes.
No ordinary loop is being discarded on the strength of its endpoints
alone. The script first retains each quotient interval with its fixed
midpoint; stabilization removes that pendant interval.

This directly addresses the wild-residue-characteristic concern.
We invoke the integral quotient theorem, rather than assuming that
forming invariants commutes with reduction or applying tame
Riemann--Hurwitz on the special fibre. The resulting arithmetic quotient
has generic fibre C by the canonical action. Stabilization contracts
rational tails and chains; the resulting weighted graph is isomorphic
to the D45 graph. All contractions and the nine reversed edges are saved.

## 4. What follows, and what does not

D45's exact finite-graph obstruction applies to this stable core:
none of its graph involutions has a tree quotient. Its specialization
argument therefore still gives geometric nonhyperellipticity of C.
This is incompatible with the published Theorem 5.9. The present audit
supports the identification needed for that conclusion; it does not
claim the published conflict has been acknowledged or settled externally.

The arithmetic order check also does not turn the saved floating-point
domain into an interval-certified polygon. It does not certify D56's
ordinary-point/moment hypotheses, D59's numerical orientation comparisons,
or identify exact analytic section values. D58's marked descent uses
the earlier descent lemma independently of the disputed hyperellipticity
claim. Those scope distinctions remain in force.

Reproduce from the repository root:

```sh
DOT_SAGE=/tmp/dembele-d62-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/99_curve_identification.py
```

No graph automorphism enumeration, analytic solve or recognition scan is
required for this new audit. The saved domain, Rickards installation and
D45 Brandt data are inputs; their hashes are in the output.
