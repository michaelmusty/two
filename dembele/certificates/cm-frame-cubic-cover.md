# An explicit genus-64 cubic modulo 31

Date: 2026-09-21. Decision D79. This completes the finite-field function
construction left open by [D78](cm-frame-cover-class-arithmetic.md).

**Result:** over the saved genus-16 candidate C modulo 31, we have an
explicit cubic whose smooth projective normalization Y has genus 64.
Its Galois closure Z has group S3 and genus 136; its quadratic resolvent
is the saved genus-40 double cover X. The functions, divisor witnesses
and cubic coefficients pass a separate verification. Deliberately
changing the norm scalar or a cubic coefficient is rejected.

This is a finite-field construction on the candidate C. It does not
identify the cover with the prescribed arithmetic Fuchsian cover, lift
it to characteristic zero, or construct the desired number field.

## Equation and files

The equation on C is

\[
 Q_4T^3-3A_4Q_4T-P_{10}=0,\qquad \operatorname{weight}(T)=2.
\]

Here A4 and Q4 are quartics, and P10 is a form of degree ten in the
sixteen saved canonical coordinates. All coefficients are in F31.
The three coefficient arrays have lengths 105,105,285 in the saved
standard monomial bases. Each monomial is an explicit exponent vector
in X1,...,X16. The curve means the normalization of the generic cubic
function field: the raw weighted equation need not be smooth, and
clearing denominators is not a prescription for its special fibres.

- [Machine-readable coefficients and witnesses](../data/computed/cm_frame_cubic.json).
- [Magma coefficient and witness arrays](../data/computed/cm_frame_cubic.m).
- [Combined verification certificate](../data/computed/cm_frame_cubic_check.json).
- [Constructor 176](../magma/176_cm_frame_kummer_function.m),
  [collector 177](../pari/177_cm_frame_cubic_data.py),
  [verifier 178](../magma/178_cm_frame_cubic_check.m),
  [runner 179](../pari/179_cm_frame_cubic_check.py).

The collector's `independent_verification_completed=false` records its
construction-only role. The combined certificate records the completed
independent verification. D78's unchanged certificate remains the proof
of the input class relation.

## Exact evaluation model

Retain D0=2*pi^*div_C(X16), degree 120, on the genus-40 curve X.
The first 640 evaluation points and all bases from D78 are unchanged.
Add complete Frobenius/involution orbits from its saved point pool to
reach 1,024 distinct points on the same smooth chart. The resulting
spaces L(iD0), i=1,2,3,4, have dimensions 81,201,321,441. The last
basis consists of saved products of the first and third bases.

Every product used below belongs to L(8D0) or a smaller space.
Since 1024>8*120=960, evaluation is injective throughout. Point equations,
both actions, basis products and ranks are checked anew. The pole bounds
for the original 81 sections are already certified in D78. All basis
functions are defined over F31, although their point values use
F31[b]/(b^2+29b+3).

The framework is Khuri-Makdisi's section multiplication and division
in an evaluation representation; see
[Representation B and sections 2–3](https://arxiv.org/pdf/math/0409209).
The concrete moving-divisor construction below is local work. Products
must reach their proved Riemann–Roch dimensions; partial quotient
constraints must cut down to their proved dimensions. Random choices
affect runtime, not acceptance.

## Descending the effective representative

Write Delta=D+-D-. D78 gives a Frobenius-fixed class A with 3A=-Delta
and tau(A)=-A, represented by W_E=L(2D0-E) over F31^2. E has degree
120, but E itself was not proved to descend. The new construction
replaces it by an effective divisor E_R defined over F31.

Choose q in L(D0-D-), over F31, nonvanishing on D+. Then

\[
 \operatorname{div}(q)=D_-+Q-D_0,\qquad \deg Q=111,
 \qquad B=D_++Q,\qquad [B-D_0]=\Delta.
\]

The branch constraint uses D77's regular W coordinate and nonic residue
algebra. In particular, nonvanishing on D+ is an exact unit test, not
a point sample. The quotient

\[
 \{s\in L(2D_0):sL(D_0-D_-)\subset qL(2D_0)\}
 =L(2D_0-Q)
\]

has dimension 90. Nine independent D+ conditions give W_B=L(2D0-B)
of dimension 81. A rank-321 sum of L(3D0-E) and L(3D0-B) proves that
E and B are disjoint; the same holds for sigma(E), since B descends.

The 81-dimensional space

\[
 M=L(4D_0-E-\sigma E-B)
\]

is Frobenius stable. Its row-reduced coordinates in the F31 basis of
L(4D0) lie in F31. Choose a nonzero F31 section m in M. Its remaining
zero divisor E_R satisfies

\[
 \operatorname{div}(m)=E+\sigma E+B+E_R-4D_0,
 \qquad [E_R-D_0]=-2A-\Delta=A.
\]

The quotient of m*L(2D0) by M recovers L(2D0-E_R). Its saved
row-reduced coordinates lie in F31, and a direct class comparison
with D78's saved third passes. The representative is chosen with
E_R disjoint from B, again certified by a rank-321 sum. No class-number
assumption or repetition of D78's scalar search enters this step.

## The Kummer function and norm

Products of W_R=L(2D0-E_R) give L(6D0-3E_R). Dividing by L(2D0)
inside L(4D0) gives L(4D0-3E_R). Its intersection with L(4D0-B)
is a line, generated by the saved F31 section u. Since E_R and B
are disjoint and 3*120+120=4*120,

\[
 \operatorname{div}(u)=3E_R+B-4D_0,
 \qquad \operatorname{div}(u/q)=D_+-D_-+3E_R-3D_0.
\]

For independent verification it suffices to check every generator of
u*L(2D0) lies in L(6D0-3E_R), and u lies in L(4D0-B). L(2D0) is
base-point-free, so these are the required divisor inclusions. Equality
follows from degrees. Verifier 178 checks all these generators.

Similarly, a saved f in L(2D0) satisfies

\[
 \operatorname{div}(f)=E_R+\tau E_R-2D_0,\qquad \tau(f)=f.
\]

The verifier checks every generator of f*L(2D0) lies in the product
W_R*tau(W_R), so this divisor equality also follows from degrees.
The final identity is

\[
 u\tau(u)=c f^3q\tau(q),\qquad c=27\in\mathbf F_{31}^{*}.
\]

Both sides lie in L(8D0), so equality at all 1,024 points certifies
equality of functions. Set

\[
 h=c\,u/q,\qquad a=c f.
\]

Then h*tau(h)=a^3 and tau(a)=a. This scalar adjustment uses the
displayed identity, without any assumed norm surjectivity.

## S3 closure, cubic quotient and genus

Since 5 is a primitive cube root of unity in F31, define

\[
 Z:\ v^3=h,\qquad \rho(v)=5v,\qquad \widetilde\tau(v)=a/v.
\]

The norm identity makes the involution well defined and of order two;
it conjugates rho to rho inverse. The valuations of h along D+ and
D- are respectively 1 and -1 modulo three, so h is not a cube even
after extending constants. Thus Z is geometrically connected and
Z/C has geometric Galois group S3. The only cubic branch points on X
are D+ and D-. Locally, a valuation divisible by three is removed by
a cube of a uniformizer, leaving an étale unit equation. This is the
Kummer construction with 3 invertible; see
[Stacks, section 59.28](https://stacks.math.columbia.edu/tag/03PK).

The fixed function y=v+a/v obeys

\[
 y^3-3ay-b=0,\qquad b=h+\tau(h).
\]

The verifier checks the universal trace and discriminant identities.
The difference h-tau(h) is nonzero. The discriminant is
-27*(h-tau(h))^2, and -27=2^2 in F31, which recovers the quadratic
resolvent X. The fixed field of the reflection has degree three over
k(C), so this polynomial is irreducible there.

In the canonical coordinates,

\[
 a=A_4/X_{16}^4,\quad q\tau(q)=Q_4/X_{16}^4,
 \quad b=P_{10}/(Q_4X_{16}^6).
\]

Putting T=X16^2*y yields the displayed weighted equation. Exact
evaluation verifies these identities in standard degree-four and
degree-ten bases. Their ranks are 105 and 285; equality is covered
by the same injectivity bound.

Above B2 (degree 18) the inertia is a transposition. Above B3 (degree
9) it is a 3-cycle. The covers are tame in characteristic 31. Hence

\[
 2g_Z-2=3(2\cdot40-2)+2\cdot18=270,
 \qquad
 2g_Y-2=3(2\cdot16-2)+18+2\cdot9=126.
\]

Thus gZ=136 and gY=64, by the
[tame Riemann–Hurwitz formula](https://stacks.math.columbia.edu/tag/0C1B).
These genera refer to smooth projective normalizations.

## Verification and remaining gate

All Magma jobs use 180-second / 2-GB bounds. The table records the first
successful runs; later rebuilt job records may have different timings.

| Job | Result | Wall time |
|---|---|---:|
| 176 function, representative descent and coefficients | pass | 5.762 s |
| 178 independent saved-data check, different seed | pass | 6.397 s |
| Norm scalar c changed to c+1 | rejected at norm identity | 4.554 s |
| First trace-numerator coefficient changed by 1 | rejected at trace identity | 6.321 s |

The constructor initially reached its arithmetic progress markers but
failed in a dependent monomial comprehension. The verifier initially
failed because a Magma sequence cannot contain matrices of different
sizes. Both failed source snapshots and logs are archived. Neither
failure is treated as a completed computation; final PASS markers and
exit statuses are checked. All jobs are finished.

Historical failure records retain their original input hashes. Current
certificates bind their immutable logs and source snapshots, while the
successful current inputs form the arithmetic proof chain. This allows
`--rebuild` to replace discovery records without treating historical
inputs as current proof dependencies.

```sh
python3 dembele/pari/179_cm_frame_cubic_check.py --collect-only
python3 dembele/pari/179_cm_frame_cubic_check.py
python3 dembele/pari/179_cm_frame_cubic_check.py --rebuild
```

**D80 follow-up:** [the Frobenius report](cm-frame-cubic-frobenius.md)
completes the first two counts, 68 and 2818 over F31 and F31^2. Both
match the Hecke prediction and pass independent fibre checks. The
D79 artifacts and certificates remain unchanged.

The immediate next comparison at the end of D79 was the Frobenius fingerprint of this
normalized genus-64 curve against the predicted genus-16 old plus
48-dimensional new Hecke factor. At minimum begin with the F31 count,
handling poles and singular fibres by normalization rather than counting
roots of a denominator-cleared equation blindly. A mismatch would direct
us back to the choice of third/cover. Agreement would be evidence, not
identification with the specified Fuchsian S3 monodromy.

After that comparison, lift the marked cubic and its function identities
31-adically and test arithmetic recognition. The base/marking/branch-half
identification, the recorded hyperellipticity conflict, the monodromy
match, characteristic-zero cubic, target torsion and field polynomial
remain open. No uniqueness of the third is proved. Earlier arithmetic
artifacts and their hashes are unchanged; backend optimization stays
paused.
