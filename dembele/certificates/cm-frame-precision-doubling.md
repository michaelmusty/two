# Precision doubling and arithmetic recognition of the denominator

Date: 2026-09-18. Decision D74. Continues
[D73's numerator normalization](cm-frame-normalization.md).

Follow-up: [D75](cm-frame-joint-field-and-B3-normalization.md) completes
joint F recognition in this space and constructs a different geometric
normalization with numerator height 583. Its transfer is certified at 31;
the 128-digit lift described here is preserved for the next step.

**Result:** compatible exact lifts now reach **31^128**, with independent
divisor and unchanged-radicand certificates at 31^16, 31^32, 31^64 and
31^128. The 39-digit numerator remains exact over Q. Coefficientwise
recognition over Q and F has not produced a candidate that passes the
unused higher digits. This is not a number-field cover.

The arithmetic experiment identifies a concrete representation cost:
the 39-digit numerator becomes a **144-digit primitive vector** in
the fixed 45-monomial section chart. An exact **17-dimensional rational
denominator space** is therefore constructed using the common residual
divisor, to replace that larger coordinate system.

## 1. Newton steps that double precision

Let m=31^e. We work directly modulo m^2, using the same finite étale
support algebras as D72. D72's original numerator is already known
exactly over Q; reducing its coefficients supplies it at any precision.
Its 631-digit height is not a reconstruction obstacle for this step.

At the D17 and old common residual supports, one Newton correction
solves the curve and simple-zero equations. At E we first lift on C,
holding the parameter X15/X16 fixed. The 44 denominator value conditions
are linear, so an exact solve corrects precisely D72's 44 active
coefficients and retains every fixed coefficient, including its scale.

To correct a double zero, compute full-precision tangent and second-jet
vectors v,w along C. With d the corrected denominator, put

\[
b=\nabla d(x)\cdot v,\qquad
c=\nabla d(x)\cdot w+d(v).
\]

Here b is divisible by m and 2c is a unit. The displacement
delta=-b/(2c) gives x'=x+delta*v. Terms quadratic in delta vanish
modulo m^2. All 91 curve equations, d(x')=0, and the derivative
condition at x' are checked, not merely the equations used for solving.

Script [`130_cm_frame_precision_doubling.py`](../pari/130_cm_frame_precision_doubling.py)
uses unit-pivot elimination in the finite algebras. Scalar inverses
are lifted by y <- y*(2-a*y). This avoids relying on polynomial xgcd
over a composite coefficient ring, which the installed Sage interface
does not implement. These are exact finite-ring operations.

The control step 31^4 -> 31^8 agrees with the earlier successive-digit
calculation in every numerator and denominator coefficient, every
support coordinate and tangent, all rational-point jets, and the
second jets modulo 31. Each later stage also reduces coefficientwise
to its predecessor.

| Stage | Internal wall time |
|---|---:|
| 8 -> 16 digits | 9.626 s |
| 16 -> 32 digits | 10.256 s |
| 32 -> 64 digits | 11.013 s |
| 64 -> 128 digits | 12.681 s |

The whole job, including the regression control and Sage startup, takes
**52.198 s**, within a 900 s timeout; no Sage memory cap is imposed.

## 2. Independent certificates and scalar preservation

Runner [`131_cm_frame_doubling_check.py`](../pari/131_cm_frame_doubling_check.py)
generates copies of the existing Magma scripts 125, 128 and 129 with
only their input data paths changed. Both templates and generated
sources are recorded by hash; the earlier files remain unchanged.
At each new precision it:

1. Independently certifies the old representation's complete divisor
   identity using supports, local jets and exhaustive degree counts.
2. Transfers to the exact 39-digit numerator n' by solving
   n*d'=n'*d in the coordinate ring, and checks every quartic coordinate.
3. Independently verifies that saved cross-product identity and all
   required local orders in the new representation.

The normalized coefficients are compatible at all saved precisions.
The identity is equality of rational functions over the finite base
ring, preserving the scalar and twist. E and the branch half remain
unchanged; the new common residual has the same degrees [1,1,26].

| Digits | Divisor check | Transfer | Normalized-pair check |
|---:|---:|---:|---:|
| 16 | 2.989 s | 9.015 s | 20.015 s |
| 32 | 2.544 s | 9.080 s | 20.425 s |
| 64 | 4.645 s | 9.077 s | 21.260 s |
| 128 | 8.011 s | 9.304 s | 23.085 s |

A 31^127 error in one denominator coefficient preserves all 127 lower
digits but fails the global identity. The expected assertion and
nonzero exit are checked, in 14.081 s. Each Magma job has 240 s and
2 GB limits.

## 3. Recognition with unused digits

Script [`132_cm_frame_denominator_recognition.py`](../pari/132_cm_frame_denominator_recognition.py)
tests 45 affine denominator coordinates and 44 projective ratios.
Projective rescaling here is only a diagnostic; it does not change
the saved radicand. Training and validation precisions are 16/32,
32/64 and 64/128 digits.

For Q it uses [Sage's bounded rational reconstruction](https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html#sage.arith.misc.rational_reconstruction).
For F=Q(zeta32)^+ it uses

\[
f(t)=t^8-8t^6+20t^4-16t^2+2.
\]

The polynomial is checked against the minimal polynomial of
zeta32+zeta32^-1. It has eight simple roots modulo 31; every embedding
is tested. A nine-dimensional congruence lattice searches for
a0+...+a7*theta^7-b*c=0 modulo the training power. Its LLL rows are
tested against the unused higher digits. The
[Sage integer-matrix reference](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
documents the lattice interface; this search and its validation gate
are local code.

**No tested coefficient candidate over Q or F survives**, in either
coordinate mode at any of the three precision pairs. Known rational
and F elements are recovered by positive controls. Perturbations in
their first unused digit are rejected. The job takes 5.003 s including
startup, under 240 s. This neither proves nonmembership in Q or F nor
excludes all coefficients below a claimed height: the F search uses
selected LLL rows, not exhaustive enumeration.

An exact calibration shows why the section representation matters:
the known 39-digit numerator becomes a 144-digit primitive chart
vector, with maximum affine numerator and denominator lengths 144
and 104 digits respectively.

Script [`133_cm_frame_projective_denominator.py`](../pari/133_cm_frame_projective_denominator.py)
therefore searches whole rational quadrics. Its rank-136 integer
congruence lattice imposes 44 projective conditions modulo 31^64
while allowing all 91 curve equations. Explicit identity pivot
columns prove the displayed triangular basis is the full congruence
kernel, of index (31^64)^44. Adding the known curve relations before
LLL preserves that lattice.

The exact numerator control is recovered at 39 digits and verified
as the same section over Q. For the denominator, none of 43 tested
nontrivial candidates passes the unused 64 digits. The smallest
returned denominator candidate has 88-digit coefficients; that is
not a lower bound on the unknown denominator's height. The whole
experiment takes 35.780 s under 300 s, with no Sage memory cap.

## 4. An exact smaller denominator space

Write div(n')=A+T', where A=D17+15P32 and deg(T')=28. All this data
is rational. The denominator necessarily lies in

\[
W=H^0(C,2K_C-T'),\qquad \dim W=32+1-16=17.
\]

The dimension follows from Riemann–Roch, since deg(2K-T')=32>30.
Script [`134_cm_frame_denominator_space.m`](../magma/134_cm_frame_denominator_space.m)
chooses a second exact numerator r in H0(2K-A), with r nonzero on T'.
This is checked on the entire reduced residue divisor by a polynomial
gcd, and transfers to Q. Consequently

\[
r d=n' s,\qquad d,s\in H^0(C,2K_C),
\]

holds for some s exactly when d vanishes on T'. An exact rational
90-by-105 multiplication matrix has rank 73 and a 17-dimensional
kernel; projection to its d coordinates is injective. This constructs
W in 12.466 s under 180 s/2 GB, without constructing a large defining
polynomial for the residual divisor. The first exported basis has
coefficients with up to 1,322 numerator/denominator digits, so a
reduced integral basis is needed before recognition.

Script [`135_cm_frame_denominator_space_reduction.py`](../pari/135_cm_frame_denominator_space_reduction.py)
constructs the saturated rank-108 integer lattice of representatives of
W, including the 91 curve-relation directions. All Smith invariants
are 1. LLL leaves seventeen independent nonzero section directions,
with coefficient-height digit lengths

```text
39, 43, 43, 47, 51, 55, 59, 63, 65, 69, 72, 77, 80, 84, 88, 93, 96.
```

The first attempt recomputed a generic rational nullspace from the
large spanning basis and timed out after 300 s. Its exact source,
empty log and limit are preserved in
[`cm_frame_denominator_space_nullspace_probe.json`](../data/computed/cm_frame_denominator_space_nullspace_probe.json).
The exported basis already has an identity block in its first seventeen
columns. Eliminating those coordinates directly constructs the same
28 constraints in 0.358 s. The complete corrected job, including
saturation, LLL and recognition tests, takes **59.463 s**, under the
same 300 s limit and without a Sage memory cap. The timeout is not
repeated with a larger limit.

Every reduced section retains an exact paired witness r*d_i=n'*s_i.
Script [`136_cm_frame_denominator_space_check.m`](../magma/136_cm_frame_denominator_space_check.m)
independently verifies all seventeen identities over Q and their
independence modulo the curve equations. It also checks that the saved
seventeen coordinates give exactly the same denominator modulo 31^128.
The certificate takes 6.116 s. A 31^127 error in a basis coordinate is
rejected in 5.619 s; both jobs have 180 s/2 GB limits.

The denominator coordinates in this basis agree at 32, 64 and 128
digits. At training/validation pairs 32/64 and 64/128, none of the
seventeen affine coordinates or sixteen projective ratios passes
coefficientwise Q/F recognition. All eight embeddings of F are tried
coherently and recorded separately. This again is a bounded search
result, not a proof that the denominator does not descend to F.

## 5. Reproduction and limits

```sh
# Recheck all saved doubling stages and their normalized transfers:
python3 dembele/pari/131_cm_frame_doubling_check.py
# Validate their saved provenance:
python3 dembele/pari/131_cm_frame_doubling_check.py --collect-only
# Recompute the Newton lift before checking:
python3 dembele/pari/131_cm_frame_doubling_check.py --lift --digits 128
# Check the reduced space and reject a changed basis coordinate:
python3 dembele/pari/137_cm_frame_arithmetic_check.py
# Validate the entire saved D74 record:
python3 dembele/pari/137_cm_frame_arithmetic_check.py --collect-only
# Repeat the bounded recognition searches and exact-space construction:
python3 dembele/pari/137_cm_frame_arithmetic_check.py --recognize
```

The main stage files are `cm_frame_doubling_{16,32,64,128}.json` and
`cm_frame_doubling_normalized_{16,32,64,128}.json`; their independent
certificate is
[`cm_frame_doubling_check.json`](../data/computed/cm_frame_doubling_check.json).
The bounded recognition results are
[`cm_frame_denominator_recognition.json`](../data/computed/cm_frame_denominator_recognition.json)
and [`cm_frame_projective_denominator.json`](../data/computed/cm_frame_projective_denominator.json).
Job records retain commands, limits, source hashes and logs.

The reduced section basis, witnesses and denominator coordinates are
[`cm_frame_denominator_space_reduced.json`](../data/computed/cm_frame_denominator_space_reduced.json).
The combined certificate is
[`cm_frame_arithmetic_check.json`](../data/computed/cm_frame_arithmetic_check.json).

**Next:** test joint projective reconstruction over F in this reduced
17-dimensional space. Represent a potential projective point by
seventeen degree-at-most-seven polynomials in the chosen generator of
F, allowing a common F-valued scale. This can avoid the coefficient
growth caused by independently dividing each coordinate and expressing
its denominator as a rational integer. It has not been implemented;
neither its success nor a smaller required precision is assumed.
Keep the existing 64/128 digit validation split and require exact
algebraic verification before accepting any resulting cover.
More precision is not the next default action.

The lift is certified at the stated finite precision. Recognition and
identification with the desired arithmetic sign cover are separate
obligations. No number-field denominator, Shimura identification,
specified cyclic cubic extension, genus-64 curve, target torsion or
nonsolvable field polynomial is claimed. Earlier D68–D73 arithmetic
artifacts, numerical banks and backend code are preserved.
