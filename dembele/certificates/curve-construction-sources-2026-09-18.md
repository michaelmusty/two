# Curve-construction sources and a CM projective frame (D68)

Date: 2026-09-18. The user suggested M23/rigidity, Belyi code, the
17T7 paper (interpreting “7t17”), and Hilbert modular forms code.

**Result:** these sources prompted a different arithmetic coordinate
construction on the genus-16 base. It uses all seventeen order-two CM
points as a projective frame. The resulting numerical canonical ideal
admits **91 independent integer quadrics**, with coefficients bounded
in absolute value by **1,514**. They define a candidate over Q of
degree 30 and arithmetic genus 16, and contain the prescribed degree-17
CM point exactly. There is a flat Gröbner model at 31 whose special
fiber is reduced and irreducible.

**Not yet established:** smoothness, identification of this candidate
with the specified Shimura curve C, the genus-64 cover Y, or target
torsion. Arithmetic genus 16 alone is not a smooth genus-16 certificate.
No Dembélé field polynomial has been obtained. The earlier statement
that there are no candidate arithmetic curve equations is now outdated;
the stronger statement that the actual target input is unproved remains.

## 1. What the sources contribute

| Source | Construction step to reuse | Boundary of that use |
|---|---|---|
| [M23, §3](https://arxiv.org/pdf/2608.08538) | Numerical differentials, geometrically chosen coordinates, equation recognition, then exact algebraic verification. Relations in higher degrees are reduced modulo earlier ones. | Its rigidity computation starts with a specified cover of P1. We have not supplied a Belyi passport for C or Y. A cover with the right abstract group would not identify Dembélé's original field. |
| [Klug–Musty–Schiavone–Voight, §5, general case](https://arxiv.org/pdf/1311.2081), and [Musty–Schiavone–Sijsling–Voight](https://arxiv.org/pdf/1805.07751) | Reconstruct a canonical ideal from products of differential expansions; retain the existing Belyi numerical engine and marked arithmetic data. | The local `BelyiMap` entry point stops on nonhyperelliptic genus greater than two. The general method in the paper is broader than that entry point. Our saved target banks already provide the numerical front end. |
| [17T7, §§3–4.3](https://arxiv.org/html/2411.07857v4) | Periods to isogeny invariants and a field polynomial; in genus four, period matrix to complex curve, rational Bouchet invariants, then reconstruction. | Its curve reconstruction is specific to genus four. Remark 4.3.9 establishes isogenous Jacobians, not an isomorphism between the exhibited curve and the Shimura curve. Remark 4.3.10 points to Voight–Willis for arbitrary-genus equation computation. The earlier target period-cost objections remain. |
| Local [`hilbertmodularforms`](https://github.com/edgarcosta/hilbertmodularforms) | `Syzygies`, coefficient-matrix kernels, and quotienting by known relations are useful implementation patterns. Exact Hecke computations remain essential for identification. | Its Fourier-expansion products are on the Hilbert modular variety. For our base field that variety has dimension eight. Jacquet–Langlands matching of eigensystems does not supply an identification of its multiplication ring with the quaternionic curve's canonical ring. |
| [van Bommel–Costa–Poonen–Srinivasan](https://arxiv.org/pdf/2506.14026), Theorem 3.1 and Corollary 4.2 | Recover equations by exact linear algebra on differential expansions at a nonrational point. | The input already includes a basis defined over the ground field and arithmetic expansions. The theorem does not turn an arbitrary complex basis into such input. This distinction motivates the construction below. |

The M23 [public repository](https://github.com/shaowuz/m23isgalois)
still supplies final polynomials and verification, not the separate
coordinate-reduction routine discussed in Zhang's account. The
[17T7 README](https://github.com/SamSchiavone/17T7) directs period
computation to [EichlerShimuraHMF](https://github.com/edgarcosta/EichlerShimuraHMF).
We do not claim a fresh source audit of that package's entire implementation.
D53's M23 audit and the earlier period-feasibility calculations remain relevant.

Read-only local inspection reached `Belyi/Code/belyi_main.m:210`,
`Code/recognition.m:643`, and the HMF functions `Syzygies`,
`LinearDependence`, `HilbertModularVariety`, and `RestrictionToDiagonal`.
The HMF ring code is not universally restricted to quadratic fields;
the important obstacle is the different geometric object, not a blanket
degree check. The diagonal restriction constructs classical modular
forms, not our quaternionic restriction. Exact source hashes and
working-tree qualifications are in
[the source record](../data/computed/curve_construction_sources_20260918.json).
Neither external checkout was changed.

## 2. A basis from the degree-(g+1) divisor

The following argument is our adaptation, not an algorithm attributed
to any of the papers above.

Let C/k be a smooth projective geometrically integral curve of genus g
in characteristic zero. Let D be a reduced closed point of degree g+1,
with known residue algebra A=k(D). Suppose

    H^0(C,K_C-D)=0.

Riemann–Roch gives `dim L(D)=2`. Choose `h in L(D) \ k` over k.
Since D is a single closed point, the polar divisor of h is exactly D.
For a holomorphic differential omega, define

    R_h(omega) = Res_D(h*omega) in A.

The global residue theorem puts this value in `ker Tr_(A/k)`. The map
is injective: zero residue at every geometric point of D forces omega
to vanish along D, and the assumed space of such differentials is zero.
Both spaces have dimension g. Consequently

    R_h : H^0(C,K_C) -> ker Tr_(A/k)

is an isomorphism over k. Replacing h by `a*h+b`, with `a in k*`,
only rescales this isomorphism. An explicit trace-zero basis of A
therefore determines a projective arithmetic basis of differentials.
**We need not construct h first.**

Indeed, let E be the `(g+1)-by-g` matrix of numerical differential
values at the geometric points of D, in any local trivializations.
When E has rank g, its left kernel is one-dimensional. A nonzero
vector a in that kernel is proportional to the simple-pole coefficients
of h in those trivializations. All its entries are nonzero. If V is
the matrix of conjugate values of a fixed trace-zero basis of A, solve

    diag(a) * E * M = V.

The resulting differentials are a common complex scalar times a
k-basis. That common scalar has no effect on homogeneous equations.
Changing the initial differential basis or rescaling any individual
row of E changes M in precisely the compensating way.

Equivalently, the g+1 canonical points are a projective frame in
P^(g-1). Their Galois-equivariant identification with the rows of V
determines a unique projective coordinate change. This is why the
whole CM divisor can fix the arithmetic coordinates, although knowing
its abstract residue field did not determine the earlier function
evaluation line or plane.

For this application `g=16`, `deg D=17`, and D58–D59 supply the marked
descent and labelled residue-field identification. We use the existing
trace-centered reduced integral basis of Elkies's degree-17 field.
The new formula itself uses neither the high-order flag at P32 nor
D56's moment normalization. Its application still inherits the stated
qualifications of the curve/descent/orbit identification; this note
does not silently discharge those earlier arithmetic hypotheses.
The rank and nonzero-dependence tests on the target remain numerical.

At each order-two elliptic point the upstairs differential has a simple
zero. Taking its first derivative gives its coarse canonical value up
to a common scalar at that point. Such row scalars cancel in the frame
construction. No arithmetic choice of local tangent is needed here.

## 3. Exact controls and the target pilot

[Script 114](../pari/114_cm_projective_frame.py) first tests the residue
construction on the Fermat quartic `x^4+y^4=1`, at
`(+/-1,0),(0,+/-1)`. The function `(x^2+y^2+1)/(x*y)` has exactly
these four simple poles. Its principal parts independently verify the
left-kernel formula. Exact checks cover a nonrational basis change,
independent row scalings, simultaneous relabelling, and two invalid
frames. The transformed quartic has rational coefficients.

[Script 116](../pari/116_cm_frame_curve_check.py) adds a nonsplit
control: on `y^2=x^5-x^2-x`, the divisor `(x^3-x-1,y-1)` has degree
three and `(y+1)/(x^3-x-1)` has poles exactly there. Over the splitting
field, the residues and trace-zero coordinates produce a projective
change defined over Q. This checks a genuinely nonrational divisor;
it is a basis test, not an assertion that quadrics recover a genus-two curve.

The target pilot reads the existing native banks at N=16384 and
N=12288. Sixteen-point circular Cauchy sums compute derivatives at
the seventeen CM points, with radius at most 1/32 of the distance
to the boundary. A half-radius repetition checks sampling sensitivity.
It solves no new differential system. The initial double probe used
column-scaled banks and had condition about 25; the final native
row-scaled evaluation matrix has condition 17.936. These are different
normalizations of the same rank check.

| Diagnostic | Result |
|---|---:|
| Evaluation rank | 16, numerically |
| Minimum normalized left-kernel weight | 0.01484 |
| Differential basis-change condition | 664.41 |
| Quadratic product rank / relation dimension | 45 / 91 |
| Two banks: relative difference of transformed series | 4.04e-16 |
| Two banks: relative difference of quadric coefficients | 6.12e-15 |
| Two banks: maximum coefficient difference | 3.67e-14 |
| Two radii, same bank: relative coefficient difference | 4.25e-24 |

These are empirical comparisons, not certified error bounds. The
128 held-out jets and 83 unused fitting-window jets are distinct
from the 45 interpolation rows. Source hashes and full coefficient
matrices are in [the frame report](../data/computed/cm_projective_frame.json).

## 4. Integer equations and algebraic checks

Evaluating the 136 quadratic monomials at the exact CM coordinates
has rank 17 over Q. Thus the lattice of quadrics vanishing at D has
rank 119. Script 115 checks its integral saturation and searches
inside it. This imposes exact arithmetic constraints before numerical
recognition, instead of recognizing 4,095 row-reduced coefficients
independently.

The one bounded run uses scale 10^18 and a coefficient cap of 10,000.
Its 119-by-226 lattice includes all 45 complex quotient constraints.
The timed final LLL stage takes 3.92 seconds; the whole script,
including exact kernel setup and validation, takes 86.61 seconds.
The timeout in script 115 applies to the final LLL subprocess, not
the initial exact lattice setup. No larger search was launched.

It finds 91 independent primitive integer quadrics; their individual
heights range from 655 to 1,514. Their integer row lattice is saturated.
All vanish exactly at D. The largest normalized quotient residual is
2.50e-21 in the current bank and 3.80e-16 in the older bank.
Those checks discover candidates; they do not certify vanishing on
the analytic Shimura curve.

The exact candidate is saved as
[JSON coefficients](../data/computed/cm_frame_curve_candidate.json)
and a [self-contained Magma model](../data/computed/cm_frame_curve_candidate.m).
Magma variables X1,...,X16 correspond to JSON X0,...,X15; the monomial
order is explicitly saved, with no factors of two on mixed terms.

Script 116 then verifies:

* Over Q the ideal has a 105-element Gröbner basis, affine-cone
  dimension two, and Hilbert polynomial `30*t-15`.
* Its monic Gröbner basis has denominators coprime to 31. Its reduction
  has the same leading monomials and defines the same ideal as reducing
  the original quadrics. This gives a flat Gröbner model over Z_(31).
* The special fiber at 31 is reduced and irreducible, of degree 30
  and arithmetic genus 16.
* The specified CM coordinates give an exact point over the degree-17
  field, and one coordinate ratio has minimal polynomial of degree 17.

These are assertions about the candidate. They do not identify it with C.
A small additional search for the P32 coordinate vector recovers no
exact rational point; no approximate rational point is promoted.

Two smoothness attempts are retained as limitations. General
`IsNonsingular` rejects the number of Jacobian minors in codimension
14. A separate normalization/genus computation at 31 reaches its
180-second timeout after confirming integrality. Neither proves
smoothness or geometric genus. The exact distinction between
arithmetic genus and the genus of the normalization is documented in
[Magma's curve handbook](https://magma.maths.usyd.edu.au/magma/handbook/text/1467).
The scripts, logs and limits are saved in
[the probe record](../data/computed/cm_frame_curve_probe_limits.json).

## 5. Next work and the path to the field

The next task is **verification of this concrete candidate**. Start
with an efficient smoothness/normalization check at 31; the flat
model can then support characteristic-zero conclusions. Check an
independent arithmetic fingerprint from the specified Shimura datum,
and state a sufficient identification criterion. Matching genus,
one CM divisor or a few traces alone is not that criterion.

Once the base is identified, construct the actual degree-three cover
Y/C, using its branch data and the relative cubic prescription in
[D53](m23-coordinate-review.md), or another explicit arithmetic
construction. Only then does the intended Jacobian/torsion route
receive target input. The base curve alone does not carry the required
new torsion constituent.

Backend cleanup stays paused. Repeating the old CM-function scans is
not the next step. This coordinate construction changes the arithmetic
input to recognition and has produced a concrete candidate to assess.
It supplies no runtime estimate for the complete field construction.

Reproduction, from the repository root:

```sh
DOT_SAGE=/tmp/dembele-d68-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/114_cm_projective_frame.py
DOT_SAGE=/tmp/dembele-d68-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/115_cm_frame_quadric_search.py
DOT_SAGE=/tmp/dembele-d68-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/116_cm_frame_curve_check.py
```

The main three scripts complete successfully. The two smoothness probes
have the limited outcomes just stated. D63's 111-test run remains the
latest full regression suite; D68's controls and algebraic assertions
are separate. All work is local and uncommitted. D63–D67 artifacts and
external checkouts are preserved, with no remote job or message.
