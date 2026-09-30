# Short numerator representatives for the lifted double cover

Date: 2026-09-18. Decision D73. This continues
[D72's exact lift](cm-frame-resolvent-lift.md).

**Follow-up:** [D74](cm-frame-precision-doubling.md) extends the certified
lift and transfer to 31^128 and constructs a reduced 17-dimensional
denominator space. The details below record D73's normalization step.

**Result:** the primitive integer numerator height falls from **631 decimal
digits to 39**, and a transferred denominator gives **the same rational
function modulo 31^8**. The numerator is exact over Q. The denominator
remains finite-precision data, with no established number-field height bound.

An independent Magma certificate checks the exact numerator, the global
cross-product identity, and the local divisor orders. A denominator error
confined to the highest digit is rejected. The cover's branch divisor and
chosen twist at the saved precision are unchanged.

## 1. What we take from M23

At the user's suggestion, we reread [Huang–Jackson–Lee–Poonen–Pries–Zhang,
§3, p. 6](https://arxiv.org/pdf/2608.08538). They fix the cubic equation
modulo the linear multiples of an already known quadric by taking a
Hermitian orthogonal complement. This supplies a precise principle:
use known equations to remove redundant polynomial representatives.

Our implementation is an **integral lattice adaptation**. We allow all
91 known quadrics of C when shortening a numerator representative.
We do not implement their Hermitian normalization, and do not attribute
our LLL search to the paper. Zhang's
[companion account](https://www.shaowuzhang.com/files/how-we-found-m23.pdf)
also describes a separate cubic reduction, without giving its algorithm.
The earlier [D53 source audit](m23-coordinate-review.md) remains applicable.

## 2. The exact lattices and measured heights

Put A=D17+15P32, of degree 32. A numerator is a section of

\[
V=H^0(C,2K_C-A),\qquad \dim V=13.
\]

There are 136 quadratic monomials and 91 independent curve equations,
so H0(2K) has dimension 45. Exact evaluation at the degree-17 point and
the fifteen rational jets at P32 give a rank-32 rational matrix M.
All 91 curve equations lie in its kernel. Script
[`127_cm_frame_numerator_lattice.py`](../pari/127_cm_frame_numerator_lattice.py)
uses the exact field and implicit jets, with all curve equations checked.

Two searches are compared:

| Representation | Integer kernel rank | Best accepted primitive height | Bits |
|---|---:|---:|---:|
| D72's fixed thirteen free coordinates | One chosen section | 631 digits | 2096 |
| Integer coefficients in the fixed 45-monomial chart | 13 | 48 digits | 157 |
| All 136 monomials, allowing curve relations | 104, including 91 relations | 39 digits | 127 |

For each search we clear the constraint-row denominators, compute the
integer kernel with Sage/PARI, and use LLL. All Smith invariants of each
kernel basis are 1. Together with full rank and M*K^t=0, this certifies
the **full saturated integer kernel**, rather than just a sublattice
obtained by clearing a rational basis's denominators. The full basis
has exactly 91 rows that vanish identically on C and thirteen remaining
section directions. Both searches retain their bases and invariants.
See the [Sage integer-matrix reference](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html).

We test basis vectors and their pairwise sums and differences, make them
primitive, and reject candidates whose reduction at 31 has excess
vanishing at D17 or P32, or vanishes at E. There are 322 distinct accepted
candidates across the two searches. The smallest has height

```text
119732280500973149122871877303430862720
```

It is the first nonzero section row of the full reduced basis, up to
primitive sign. The comparison concerns the best sections found by two
different searches; it is not a shortest-vector proof or a fixed-section
comparison of two bases. In particular, no optimal-height claim is made.

## 3. Transfer and preservation of the radicand

Write D72's ratio as u=n/d, with

\[
\operatorname{div}(u)=A-2E,\qquad \deg E=16.
\]

For the new numerator n', div(n')=A+T' with deg(T')=28. Thus n'/u is a
regular section of 2K, with divisor 2E+T'. This justifies seeking its
quadratic representative d' from

\[
n d'=n'd\quad\text{in the homogeneous coordinate ring of C}.
\]

Script [`128_cm_frame_normalization_transfer.m`](../magma/128_cm_frame_normalization_transfer.m)
forms the degree-four products using the rational Gröbner basis. Their
coefficient denominators are units at 31, so the normal forms reduce
over Z/31^8 using D69's verified flat model. Multiplication by n gives
a rank-45 matrix in 105 quartic coordinates. A unit 45-by-45 minor solves
for d' in the existing section chart. The entire equation, including all
unused quartic coordinates, is then checked.

The first candidate passes all support conditions. Its common residual
divisor T' is reduced, avoids D17, P32 and E, and has residue-factor
degrees **[1,1,26]**. Its exact univariate presentation is checked by an
ideal equality. The projection X15/X16 separates its points and is
unramified there. D72's D17 and E supports remain unchanged.

The cross-product identity proves equality of rational functions over
the finite base ring: both denominators are regular, nonzero sections
on the integral special fiber. Consequently it also preserves the
square class and the selected twist at this precision. This is stronger
than checking only a branch profile or a point count.

## 4. Independent verification

Script [`129_cm_frame_normalization_check.m`](../magma/129_cm_frame_normalization_check.m)
reads the saved pair and does not repeat the transfer solve. It verifies:

- Over Q, n' belongs to the exact D17 ideal; independently computed
  rational implicit jets give order exactly 15 at P32.
- The quartic n*d'-n'*d is zero on C modulo 31^8. Every coefficient of
  its rational normal form has denominator prime to 31 and numerator
  divisible by 31^8.
- At the unchanged D17 and E supports, the numerator and denominator
  have the required orders at full precision, including double-zero
  derivatives at E and unit leading coefficients modulo 31.
- The new degree-28 residual divisor has the asserted exact ideal,
  squarefree residue polynomial and unit local Jacobian minors.
  Saturated ideal equalities modulo 31 give div(n')=A+T' and
  div(d')=2E+T'.

Together with the already verified D72 divisor identity and the global
ratio equality, this certifies the same full-precision relation

\[
\operatorname{div}(n'/d')=D17+15P32-2E.
\]

The negative control adds 31^7 to the denominator's X1^2 coefficient.
It preserves every digit modulo 31^7 and the exact numerator conditions,
but the quartic identity fails. The expected assertion and nonzero exit
are checked explicitly.

| Job | Wall time including startup | Limits |
|---|---:|---|
| Exact lattices and candidate search | 53.058 s | 240 s; no Sage memory cap |
| Denominator transfer and support selection | 9.987 s | 180 s / 2 GB |
| Independent certificate | 20.524 s | 180 s / 2 GB |
| Highest-digit corruption control | 14.501 s | 180 s / 2 GB |

These are targeted exact certificates. Earlier numerical banks and
backend code are unchanged; no full backend test rerun is needed.

## 5. Reproduction and next step

The main data are
[`cm_frame_numerator_lattice.json`](../data/computed/cm_frame_numerator_lattice.json),
[`cm_frame_normalized_resolvent.json`](../data/computed/cm_frame_normalized_resolvent.json)
and [`cm_frame_normalization_check.json`](../data/computed/cm_frame_normalization_check.json).
Magma data files, logs, job limits and transitive source hashes are saved
alongside them. Run from the repository root:

```sh
# Independently check the saved pair and reject a newest-digit error:
python3 dembele/pari/129_cm_frame_normalization_check.py
# Verify the complete saved provenance without rerunning arithmetic:
python3 dembele/pari/129_cm_frame_normalization_check.py --collect-only
# Recompute both lattices, transfer the denominator, then certify:
python3 dembele/pari/129_cm_frame_normalization_check.py --rebuild
```

**Next:** extend the lift with precision doubling, retain the exact
39-digit numerator in its full 136-monomial representation, and seek
recognition of the remaining data over F. T' is currently exported
modulo 31; its simple support can be lifted against the exact numerator
when a new support representation is needed. Its higher-precision
coordinates have not yet been computed.

Keep scalar changes explicit. One safe comparison path is to extend
the original D72 lift and repeat the cross-product transfer at each
new precision. Merely fixing a different denominator coefficient to 1
would change u, and would require an explicit square-factor/isomorphism
check before claiming preservation of the same cover. The 39-digit
numerator does not supply a denominator height bound, guarantee small
coefficients over F, or establish descent.

The denominator and cover over a number field, the independent Shimura
identification (including the earlier hyperellipticity conflict), the
specified cubic extension, genus-64 Y, target torsion and the nonsolvable
polynomial remain open. All D68–D72 arithmetic artifacts are preserved.
