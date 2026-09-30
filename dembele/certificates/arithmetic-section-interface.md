# A concrete section interface for Y (D62)

This records the arithmetic input to construct after the D62 backend
scaling gate. It is a specified interface and a line-bundle choice,
**not an implemented method for obtaining its entries**. The existing
analytic CM restrictions do not supply this matrix.

Let pi:Y->C be the established degree-three cover, with genera 64 and
16. Let P be C's distinguished F-rational order-32 CM point. Choose

    D0 = pi^*(43P),   deg(D0) = 129 = 2*g(Y)+1.

This divisor is defined over F independently of D56's ordinary-point
or moment assumptions. Riemann--Roch applies uniformly since its degree
exceeds 2*g(Y)-2. We need arithmetic section evaluations with dimensions

| Space | Dimension |
|---|---:|
| H0(Y,O(D0)) | 66 |
| H0(Y,O(2D0)) | 195 |
| H0(Y,O(3D0)) | 324 |
| H0(Y,O(4D0)) | 453 |
| H0(Y,O(5D0)) | 582 |

At a suitable good prime and chosen embedding F into its completion,
evaluate at at least 646 distinct reduction points, disjoint from D0,
whose set is Frobenius-stable. Use compatible local trivializations.
The initial matrix has at least 646 rows and 66 columns; it must preserve
rank on reduction. Products produce the higher spaces with the displayed
dimensions. This is the concrete size demanded by
[Mascot, Definition 2.1.1 and Remark 2.1.6](https://arxiv.org/pdf/2004.14683).
Script 100 now tests this kind of interface after removing the equation
from an initialized control object.
The upstream p-adic C routines use polynomial representatives in the
unramified field generator, including for constant matrix entries.

The cover gives a useful exact decomposition. Write

    pi_*O_Y = O_C + V,  V = ker(Tr),  rank(V)=2.

From Euler characteristics, deg(V)=-18. Thus the first section space
splits into a 28-dimensional pullback of L(43P) and a 38-dimensional
trace-zero space H0(C,V(43P)). Its higher powers have dimensions
71+124=195 and 114+210=324. Their H1 vanishes because it is a direct
summand of H1(Y,O(nD0))=0. This specifies how a construction through
the base and cubic algebra would connect to the backend; merely knowing
the dimensions or the vector bundle's degree does not construct it.

The required additional inputs are:

* The entries of these evaluations, with Frobenius permutation and the
  arithmetic origin of the section spaces on the specified Y. A genus
  count or a generic curve of the same genus is insufficient.
* Two suitable auxiliary divisors of degree d0-g=65, with spaces
  H0(2D0-E_i) of dimension 130, or another verified arithmetic evaluation
  map that separates the target torsion. The Q8 branch-point failure
  shows that genericity must be checked on the actual torsion.
* A local Euler factor and a verified projection onto the intended
  residual subspace, or a computed geometric Hecke action when Frobenius
  alone does not separate it. D51's abstract Hecke projector is not yet
  an operation on these divisor matrices.
* A coefficient-recognition and certification step over F. The stock
  high-level LiftTors example recognizes rational coefficients; the
  target degree-257 polynomial over F needs the corresponding arithmetic
  recognition step, unless a further descent has been constructed.

An acceptable next arithmetic experiment would construct the first
matrix modulo a specified odd prime, prove that its sections and
multiplication belong to the actual cover, and verify ranks and
Frobenius compatibility. A subsequent p-adic lift needs an arithmetic
mechanism to produce the same data modulo increasing prime powers.
Neither that finite-field construction nor that lifting mechanism has
been implemented for Y. D53's cubic trace expressions still require
the missing arithmetic base sections and cover coefficients.

No production prime or precision is selected here. D63's
[memory adaptations](lifttors-memory.md) make the genus-64 control pass
at residue degree two and precision four under the same 2 GB stack cap.
D64's [extension calibration](lifttors-extension.md) passes at degree
51 on a known genus-4 curve. D65 now supplies a separate
[native implementation](lifttors-rows.md) that generates equation blocks
and verifies the complete kernel without storing the full matrix.
Genus-64/degree-51 cost and production precision remain untested. The
small control point is rational and does not realize the target
residual representation. D66's
[genus-16/degree-51 control](lifttors-degree51.md) now passes under
the same cap and timeout. Its independent reduction audit also finds
and locally fixes the auxiliary embedding-table structure in `PicRed`;
the arithmetic interface must preserve a vector of matrices, one per
embedding, for each auxiliary divisor. Correct reduction/evaluation
controls do not construct these spaces on the actual Y.
The arithmetic construction of the actual matrices remains open.
Further scans in the same CM coordinates remain paused.
