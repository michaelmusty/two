# D109: an exact integral dyadic splitting and one arithmetic edge transport

Date: 2026-09-25. The user authorized the bounded plan with
“proceed with this plan”.

The three requested deliverables are complete. We exported the definite
order selected by the existing HMF arithmetic, certified an isomorphism
`O tensor O_K -> M2(O_K)`, and verified an actual norm-one unit carrying
one adjacent edge to another. An independent Python replay checks the
integer lattice, the Hensel certificate and the transport using rational
arithmetic. This supplies local arithmetic input for a dyadic evaluator;
it does not yet supply a harmonic cocycle or a Shimura differential.

The transport fixes the base vertex and cyclically permutes its three
neighbors. It is a nontrivial edge transport, not a side-pairing between
distant parts of a computed fundamental domain. No new ideal-class or
tree census, Hecke bank or high-precision cubic calculation was run.

## The actual definite order

Use the unchanged field and dyadic prime

    F = Q(b),  b^8 - 8b^6 + 20b^4 - 16b^2 + 2 = 0,
    p = (b),  K = F_p,  pi = b,  v(pi)=1,  v(2)=8.

The polynomial is Eisenstein at 2. Its power basis therefore gives

    v(sum_(r=0..7) c_r*b^r) = min_r(8*v_2(c_r)+r).

Distinct nonzero summands have valuations distinct modulo 8, so this
formula is exact, including for rational coefficients with denominators.
The residue field is F2. The already certified ring of integers is
`O_F=Z[b]`, of discriminant `2^31`.

[Export 397](../magma/397_definite_dyadic_export.m) uses the same HMF
`QuaternionOrder(HilbertCuspForms(F,1,[2,...,2]))` construction as D99,
with seed 990370. Inspection of `hackobj.m` shows that this case selects

    B = (-1,-1)_F = F + F*i + F*j + F*k,
    i^2=j^2=-1,  ij=k=-ji.

This is the totally definite algebra of finite discriminant one, distinct
from the indefinite algebra used in the complex uniformization.
The export records all 32 Z-basis vectors of its maximal order O as
four lists of eight rational power-basis coefficients. No ideal-class
ordering is inferred from the export: D99 saved the 58-class Brandt
matrix and stabilizer orders, not these local coordinates.

Both [certificate 398](../pari/398_definite_dyadic_certificate.py) and
[independent replay 399](../pari/399_definite_dyadic_review.py) verify:

- the lattice contains 1 and is stable under multiplication by b;
- all 1024 products of its Z-basis elements lie in the lattice;
- its absolute reduced-trace pairing has determinant `2^124=(2^31)^4`.

The discriminant comparison makes the relative reduced-trace
discriminant the unit ideal. Together with the order property, this
proves maximality at every finite prime. The definite presentation and
the exact trace calculation do not depend on accepting Magma's
`IsMaximal` predicate alone.

## From approximate matrices to an exact splitting

Magma's documented
[`pMatrixRing(O,p : Precision:=96)`](https://magma.maths.usyd.edu.au/magma/handbook/text/1074)
provides proposed local matrices. Its hypothesis is that p is unramified
in the quaternion algebra; it does not require `K/Q_2` to be unramified.
The level-one HMF `SplittingMap` is not used.

The exported matrices are converted into exact rational elements of F.
Their role is to propose a conjugating matrix C and numbers x0,y. The
following independent calculation establishes an exact map, regardless
of the precision guarantees of that proposal. All full coordinates are
in [the certificate packet](../data/computed/definite_dyadic_certificate_d109.json).

Let

    I0 = [0 -1; 1 0],
    J0(t) = [t y; y -t],
    f(t) = t^2+y^2+1.

The saved C is invertible over F, with `v(det C)=4`. Exact arithmetic gives

    v(x0)=0,  v(y)=4,
    v(f(x0))=188,  v(f'(x0))=v(2*x0)=8.

Since `188>2*8`, Hensel's lemma supplies a unique root t in K satisfying
`v(t-x0)>8`, and in fact `v(t-x0)=180`. This is an exact algebraic
description of t and its chosen dyadic embedding. It is not an assertion
that a finite-precision residual is exactly zero. Newton's iteration
converges in this specified ball; the second root lies outside it.

Define

    iota(i) = C*I0*C^(-1),
    iota(j) = C*J0(t)*C^(-1),
    iota(k) = iota(i)*iota(j).

The identities `I0^2=-1`, `I0*J0=-J0*I0` and `J0(t)^2=-1` hold exactly.
They define a nonzero algebra homomorphism from the central simple
four-dimensional algebra `B tensor K` to `M2(K)`, hence an isomorphism.

Each order-basis image has the form `A_q+t*D_q`. The rational matrix
`A_q+x0*D_q` is integral, and the true image differs from it by valuation
at least 176 in every entry. Four of these images, at zero-based Z-basis
indices `[0,12,20,24]`, span `M2(F2)` after reduction. Thus the image of
`O tensor O_K` lies in `M2(O_K)` and is surjective modulo pi. Nakayama's
lemma gives the exact integral isomorphism

    iota(O tensor O_K) = M2(O_K).

The 176-digit bound uses the uniformizer pi: it corresponds to 22 binary
digits. It is sufficient for this feasibility certificate. It is not
identification precision for a Shimura jet.

## A norm-one unit transporting an edge

The explicit unit is

    u = (1-i-j-k)/2.

In the exported Z-basis it is `q_0-q_24`. Exact arithmetic proves both
u and its inverse belong to O, and `Nrd(u)=1`. Also `u^2-u+1=0`, so its
projective order is three. Therefore it belongs to the norm-one
S-arithmetic group `O[1/pi]^1`, and its local matrix lies in `SL2(O_K)`.
Its reduction in this particular certified splitting is

    iota(u) mod pi = [1 1; 1 0].

Let the three neighboring lattices have column matrices

    L0 = [1 0; 0 pi],
    L1 = [pi 0; 0 1],
    L2 = [1 0; 1 pi].

Their reductions correspond to the lines `(1,0)`, `(0,1)`, `(1,1)`.
The unit induces the permutation `[2,0,1]`, fixing the central vertex.
In particular, it sends the oriented edge `(O_K^2,L0)` to `(O_K^2,L2)`.

The replay checks this using the actual lattice equation:
`L2^(-1)*iota(u)*L0` is integral, with a certified entry-error bound
of 175, and its exact determinant is

    Nrd(u)*det(L0)/det(L2) = 1.

It is therefore in `GL2(O_K)`, which proves equality of the transported
lattices, not merely a match of approximate residue labels. Deliberately
using L0 as the target instead produces a negative-valuation entry and
is rejected. Replacing the proposed Hensel root x0 by x0+1 also fails
the Hensel inequality. Both negative controls pass.

These are the integral splitting and arithmetic equivalence inputs of
[Masdeu--Torrents, sections 2.1--2.2 and 3](https://arxiv.org/pdf/2510.09356).
We use the column-lattice definition of the tree action directly. Their
full domain algorithm and public implementation have not been run here.

## Provenance, failures and scope

The successful export, exact certificate and independent replay probe
took 0.63, 6.15 and 0.78 seconds. Every job used the 180-second private
process-group runner; Magma had a 2 GB memory cap. The initial export
failed an overly strong equality assertion on approximate matrices.
Two later attempts reached the direct mapping of all 32 order-basis
elements and hit the 180-second cap. Their full process groups were
terminated. All three original sources, receipts and logs are archived.
None produced a result artifact. The successful implementation exports
four algebra matrices and performs order integrality checks exactly.

Review 399 binds the completed sources, artifacts, report, source ledger,
successful receipts and failed-attempt snapshots. All 606 D108 source
hashes are preserved. The report supplies the mathematical implications
of Hensel lifting, trace discriminants and Nakayama; this is not a
formal proof-assistant verification. Recheck without Sage or Magma:

    python3 dembele/pari/399_definite_dyadic_review.py --check

The source ledger is
[definite_dyadic_sources_d109.json](../data/computed/definite_dyadic_sources_d109.json).
Sources 397--399 and all bound artifacts are frozen after successful review.

The next bounded task is to specify the exact arithmetic group and
normalizer quotient for our curve, reconcile its action with the saved
58-class Brandt data, and verify one transport that moves the base
vertex. Preserve the same-session ideal ordering when exporting such
data. A stabilizer permutation alone does not establish a fundamental
domain or its side-pairings. Do not start a full new tree census yet.

An evaluator still needs invariant harmonic cocycles and their measure
bound, dyadic CM/residue-frame matching, certified moments, propagation
through the cofactor frame, and a valid Gaussian chart. D107's complex
labels remain proved but supply no dyadic CM embedding. D108's local
jet formula remains conditional. No actual tangent/jet, candidate
identification or target polynomial has been obtained. Keep the
enumeration, Hecke-bank and cubic-precision pauses; D108's rejection
of the unchanged absolute spectral comparison remains in force.
