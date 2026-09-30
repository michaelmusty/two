# Joint field recognition and normalization using B3

Date: 2026-09-18. Decision D75. Continues
[D74's precision and denominator-space work](cm-frame-precision-doubling.md).

**Follow-up:** [D76](cm-frame-rational-double-cover.md) transfers this
normalization through 31^128 and constructs an exact rational cover,
using its six-dimensional product space and exact Veronese relations.
The limitations and next steps below record the D75 checkpoint.

**Main result:** changing the auxiliary divisor from 7P32 to B3 gives
an exact rational numerator of coefficient height **583**, replacing
the earlier 39-digit numerator. An explicit square-factor identity
certifies the same double cover **modulo 31**. An independent verifier
passes and rejects a wrong quadratic twist. This new representation
has not yet been transferred to 31^128 or recognized over a number field.
The old certified 128-digit lift is preserved.

The planned joint F recognition was completed first. It recovers an
exact control that separate coefficient recognition misses, but none
of 765 tested denominator candidates survives unused-digit validation.
There is also a rigorous coefficient-box exclusion in the old basis.

## 1. Joint projective recognition

Use D74's seventeen rational section classes d_i and
F=Q(theta), where theta satisfies

\[
f(t)=t^8-8t^6+20t^4-16t^2+2.
\]

Represent a possible projective denominator by
sum_i A_i(theta)d_i, with each A_i an integer polynomial of degree
at most seven. This permits a common F-valued scale; there is no
separate rational denominator for each coordinate.

Script [138](../pari/138_cm_frame_joint_field_recognition.py) uses only
the residues modulo m=31^64 to construct a rank-136 integer lattice.
For an anchor a whose target coordinate is a unit, its sixteen
conditions are

\[
A_i(r)c_a-A_a(r)c_i\equiv0\pmod m\quad(i\ne a).
\]

The constant coefficients in the sixteen non-anchor blocks give an
identity minor after dividing by c_a. An explicit triangular lattice
basis therefore has index m^16. After LLL, both membership and the
index are checked exactly. The
[Sage matrix documentation](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
supplies the software interface; the lattice and validation argument
are local constructions.

All eight roots of f modulo 31 are lifted to 31^128. Only rows whose
anchor evaluation is a unit are tested as full-precision projective
candidates. Every tested row is checked against the unused 64 digits.
This is a bounded row search, not an exhaustive search through the lattice.

The control uses seventeen degree-seven polynomials with coefficients
of absolute value at most 997845. It divides all coordinates by one
nonconstant F element. Joint recognition recovers eight lattice rows
representing the exact same point over F; separate recognition of its
sixteen ratios recovers none. Adding 31^64 to one non-anchor target
coordinate leaves the fitted lattice unchanged and rejects all rows.

| Root modulo 31 | Tested denominator rows | Survivors |
|---:|---:|---:|
| 4 | 98 | 0 |
| 9 | 91 | 0 |
| 10 | 94 | 0 |
| 11 | 95 | 0 |
| 20 | 98 | 0 |
| 21 | 98 | 0 |
| 22 | 95 | 0 |
| 27 | 96 | 0 |

Every tested denominator row fails already at the first unused digit.
The smallest returned candidate at every embedding has 12-digit
coefficients. That observed size is not a lower bound.

## 2. An exact bound in the old coordinates

Script [139](../pari/139_cm_frame_joint_height_bounds.py) supplies a
separate, rigorous bound. Let R be the row-basis matrix of a full
congruence lattice and put D=m R^-1. D is integral, and R D=m I is
checked exactly. Let S be the largest column sum of absolute values
in D. For a lattice vector v=zR,

\[
z=vD/m\in\mathbf Z^{136}.
\]

If every coordinate of v has absolute value at most H and H S<m,
every coordinate of z has absolute value less than one. Thus z=0
and v=0. The certified excluded box is H=floor((m-1)/S).

| Root modulo 31 | Excluded coefficient bound H |
|---:|---:|
| 4 | 10847276 |
| 9 | 27531661 |
| 10 | 8066216 |
| 11 | 15844923 |
| 20 | 14089839 |
| 21 | 17084941 |
| 22 | 20133228 |
| 27 | 14309890 |

Consequently no nonzero common-scale representation in these section
and power bases has all 136 coefficients bounded by **8066216**.
This bound applies to the entire lattice, including rows skipped by
the recognition filter. It is basis dependent and does not prove
non-descent to F. It does not apply to the new B3 normalization below.

Independent Magma script [140](../magma/140_cm_frame_joint_field_check.m)
checks the determinants, every congruence and validation result, the
exact control identities over F, and every inverse-norm bound. Runner
[141](../pari/141_cm_frame_joint_field_check.py) also tests corrupted
unused digits. The combined record is
[cm_frame_joint_field_check.json](../data/computed/cm_frame_joint_field_check.json).

## 3. Move the auxiliary divisor

Write P=P32, B2=D17+P, and retain D71's certified identity

\[
\operatorname{div}(u)=B2+14P-2E,\qquad \deg E=16.
\]

The associated branch half is L=O(E-7P). The known rational divisor
B3 has degree nine and short linear equations. Instead of representing
L by E-7P, seek an effective E_new of degree eighteen with
L=O(E_new-B3). This is a change of representative of the same line bundle;
it does not assert the previously excluded relation L=O(B3).

The new rational numerator should vanish on B2+2B3. Script
[142](../pari/142_cm_frame_B3_numerator.py) computes the exact space

\[
H^0(C,2K-B2-2B3),\qquad \dim=9.
\]

Products of the seven equations of B3, together with the 91 curve
equations, span a rank-118 space of quadrics. Imposing D17 and P gives
36 independent linear conditions on all 136 quadratic monomials.
The saturated integer kernel has rank 100 and all Smith invariants
equal to one. The quotient section space has rank nine modulo 31.

The chosen nine independent section representatives have coefficient
heights of three or four digits. There are 172 tested basis/pairwise
combination candidates. The first candidate has height **583** and
passes the divisor checks. No shortest-vector assertion is made.
In this lattice all 100 LLL rows have nonzero section classes: short
sections and curve relations are mixed, so they cannot be separated
by simply counting nonzero images.

## 4. Explicit square-factor transfer

Script [143](../magma/143_cm_frame_B3_transfer.m) works at 31. It chooses
a quadric g with

\[
\operatorname{div}(g)=E+B3+G,\qquad\deg G=35.
\]

The space H0(2K-E-B3) has dimension twenty. The space of quadrics q
vanishing on G+7P has dimension three. A saved q gives

\[
\operatorname{div}(q)=E_{\rm new}+G+7P,\qquad\deg E_{\rm new}=18.
\]

The relevant residuals are reduced and disjoint; all multiplicities
are certified by ideal identities and degree counts. For the exact
height-583 numerator n_new, its common residual T has degree 24.
A unique denominator up to scalar vanishes on 2E_new+T. Its scalar
is fixed by checking the global identity on C

\[
n_{\rm old}g^2d_{\rm new}
=n_{\rm new}d_{\rm old}q^2.
\]

Thus

\[
u_{\rm new}=\frac{n_{\rm new}}{d_{\rm new}}
=u\left(\frac gq\right)^2,
\qquad w_{\rm new}=w_{\rm old}\frac gq,
\]

and div(u_new)=B2+2B3-2E_new. The odd branch divisor is still B2,
of degree eighteen; the double cover still has genus forty. B3 has
even multiplicity and contributes no new ramification.

The numerator is exact over Q. Its membership in the ideal of 2B3
is verified by a rational linear combination whose denominators are
prime to 31. Its D17 and P vanishings are checked separately, using
D70's flat marked models. Subtracting B2+2B3 from its relative zero
divisor produces a proper flat degree-24 residual. Its reduced special
fibre therefore proves that its generic fibre is reduced; disjointness
also follows by properness. This uses the Stacks Project's results on
[relative Cartier divisors, including differences](https://stacks.math.columbia.edu/tag/056P)
and [reduced fibres over a DVR, Lemma 37.26.6](https://stacks.math.columbia.edu/tag/0574).

A direct rational residual-ideal computation timed out after 180 s.
Its exact source, log and limits are archived in
[cm_frame_B3_rational_ideal_probe.json](../data/computed/cm_frame_B3_rational_ideal_probe.json).
The successful calculation uses the linear membership certificate and
good reduction, under the same 180 s/2 GB limits. Do not repeat the
archived ideal computation unchanged.

Independent script [145](../magma/145_cm_frame_B3_check.m) verifies the
saved data without selecting sections. Negating d_new preserves every
divisor but introduces the nonsquare twist -1 over F31; the global
identity correctly rejects it. Runner
[144](../pari/144_cm_frame_B3_check.py) records both outcomes in
[cm_frame_B3_check.json](../data/computed/cm_frame_B3_check.json).
The equation, square factor, E_new quadrics and all three moving
sections are in
[cm_frame_B3_normalization.json](../data/computed/cm_frame_B3_normalization.json).

## 5. Reproduction and next step

| Job | Whole wall time | Limit |
|---|---:|---|
| Joint F recognition, 138 | 31.380 s | 300 s, no Sage memory cap |
| Exact box bounds, 139 | 4.214 s | 180 s, no Sage memory cap |
| Independent joint check, 140 | 6.752 s | 180 s / 2 GB |
| Joint unused-digit control | 0.879 s | 180 s / 2 GB |
| B3 numerator lattice, 142 | 21.872 s | 240 s, no Sage memory cap |
| B3 transfer, 143 | 20.390 s | 180 s / 2 GB |
| Independent B3 check, 145 | 16.051 s | 180 s / 2 GB |
| Wrong-twist control | 15.709 s | 180 s / 2 GB |

```sh
python3 dembele/pari/141_cm_frame_joint_field_check.py --collect-only
python3 dembele/pari/141_cm_frame_joint_field_check.py
python3 dembele/pari/141_cm_frame_joint_field_check.py --search
python3 dembele/pari/144_cm_frame_B3_check.py --collect-only
python3 dembele/pari/144_cm_frame_B3_check.py
python3 dembele/pari/144_cm_frame_B3_check.py --rebuild
```

**Next:** transfer this normalization using the old saved 128-digit
supports. Lift g in H0(2K-E-B3) by linear conditions with fixed free
coordinates, lift its simple residual G, then lift the entire
three-dimensional space H0(2K-G-7P). Solve the displayed global
identity for d_new and verify the square-factor map at each precision.
Keep the same recorded scalar. This reuses existing precision;
no higher-precision B3 transfer is claimed yet.

Retain all three q sections: their six pairwise products offer a
possible way to recognize a small denominator space before choosing
one point in it. Their rank and arithmetic height have not been
computed. Do not assume that independently fixing denominator
coefficients selects the same branch half or preserves its field.

Neither the denominator nor the full cover has been reconstructed
over a number field. Independent Shimura/marking identification,
including the earlier hyperellipticity conflict, remains open. The
specified cubic cover, genus-64 Y, target torsion and nonsolvable
field polynomial remain unconstructed. D68–D74 arithmetic artifacts
and the certified 128-digit lift are unchanged.
