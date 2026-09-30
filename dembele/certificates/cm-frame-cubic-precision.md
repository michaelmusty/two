# D82: pointed normalization and higher precision

Date: 2026-09-22. The normalization and lift through 32 digits are complete
and verified; coefficient-field reconstruction remains open. Every
substantive Magma job has a 180-second wall limit and a 2 GB memory limit.
A timeout is an unsuccessful computation.

## Result and scope

The final output equation is

\[
\ell T^3-3A_2\ell T-R_4=0,\qquad \operatorname{wt}(T)=1,
\]

with 45 quadratic and 105 quartic coefficients. It has compatible models
modulo 31, 31², 31⁴, 31⁸, 31¹⁶ and 31³². The 32-digit independent
check and both coefficient-error controls pass. The smaller normalization,
its exact 25-dimensional rational space for A2, and the bounded recognition
searches are described below. No exact number-field equation is recovered.

For class arithmetic, the construction first uses an internal pointed model:

\[
\ell T^3-3A_4\ell T-R_7=0,\qquad \operatorname{wt}(T)=2.
\]

Here ell is the fixed rational linear form from D77, A4 is a canonical
quartic, and R7 is a canonical septic. Their arrays have 105 and 195
entries. This replaces D79's movable quartic denominator. The special
fibre is explicitly isomorphic to D79 and retains D80's verified counts
68 over F31 and 2818 over F961. These computations do not reconstruct a
characteristic-zero equation, identify the curve arithmetically, or
construct the target field.

Construction data: `cm_frame_cubic_pointed_{1,2,4,8,16,32}.{json,m}`.
Runner 221 constructs the earlier models; 240/241 recover the functions
directly from the certified pointed class, and 244 publishes the verified
32-digit result. Runners 223/236/243 independently check the saved
witnesses and deliberate coefficient errors in bounded stages. Only an existing
`cm_frame_cubic_pointed_n_check.json` records completed independent
verification at precision n. Construction success alone is not that check.

## Why change the first persistent gauge?

Scripts 195/202 prove that 80 selected RREF entries give local coordinates
on the 80-dimensional complete linear system. The selected derivative
minor is 8 modulo 31. An actual equivalent-divisor perturbation normalizes
back to the D81 representative, and the entire construction and independent
controls succeed modulo 31⁴. The eight-digit function job using this gauge
times out at 180 seconds, after two Newton corrections. Its failed log is
`cm_frame_cubic_precision_8_formal_cubic.out`.

More importantly, local uniqueness of a finite étale coordinate choice
does not imply that it preserves the coefficient field. A linear choice
in the complete linear system provides a stronger normalization for
reconstruction. The old gauge and its successful four-digit certificate
are retained without alteration.

## Unique divisor containing 80P

Let P be the rational ramification point of X above P32. D0 has degree
120, X has genus 40, and an effective representative E of A has degree
120. Thus L(E) has dimension 81. At P, X16, ell and d are units and n
vanishes simply on C, so w is a uniformizer on X, with w²=n/d.

Choose g in W_E=L(2D0-E), nonzero at P. Its complementary divisor E'
satisfies div(g)=E+E'-2D0. Compute N=L(2D0-E'), an 81-dimensional space.
The conditions that r in N vanish to order at least 80 at P have rank 80
modulo 31. Consequently they have a unique projective solution over
every lifted ring. The divisor E_point=div(r)-E'+2D0 lies in the class
of E and contains 80P. Recover its section space by an actual quotient
operation, not by altering arbitrary matrix entries. The residual
divisor has degree 40.

Scripts 217–219 compute and verify the local jets; 220 applies this
normalization and 222 checks its saved g/r witnesses, rank and vanishing.
The construction is rational in the class because it uses a unique kernel
line of a linear map with a unit maximal minor. No additional algebraic
coordinate choices are introduced.

## Fixed denominator and scalar

Retain the certified construction h=c*u/q, a=c*f, with h*tau(h)=a³,
tau(a)=a and b=h+tau(h). The divisor of h is
D+−D−+3E_point−3D0. Hence b has poles only along B3+6K_C, and
R7=ell*b is a canonical septic. Script 220 recovers it from evaluations
and verifies the cleared identity at all 1024 points. Its pole degree on
X is at most 660, strictly below the evaluation length.

At P the orders of a and b are respectively 160 and 240. Write their
leading coefficients as a0 and b0. The norm identity and tau(w)=−w
give b0²=4a0³; both coefficients are units. Set lambda=2a0/b0 and
replace a,b by lambda²*a,lambda³*b. Their leading coefficients are now
1 and 2. This normalization uses only unit division, without extracting
a root. It removes the scalar choices in q,u,f. Exact 244-term curve
jets independently check all lower vanishing coefficients and these two
leading coefficients. The q free coordinates on odd sections are
scaled by sqrt(−3)/11, respecting the algebraic branch orientation.

## Identification with the old special fibre

Script 224 uses all 2048 saved points, with maximum pole degree 1200,
to prove identities of rational functions, including evaluations where
denominators vanish after clearing them. With s=r/g, it proves

\[
h_{\rm point}=13^3s^3h_{\rm D79},\qquad
a_{\rm point}=13^2s\tau(s)a_{\rm D79}
\]

over F31. Therefore v_point=13*s*v_D79 identifies the Kummer fields and
commutes with their involutions. It identifies the smooth projective
reflection quotients, including exceptional fibres. The certificate
`cm_frame_cubic_pointed_isomorphism.json` binds both the independent
pointed checker and D80's point-count certificate. The job takes 5.014 s.

## Shorter class lift

A coefficient lift of the old divisor matrix does not generally define
a divisor. Scripts 208–213 instead choose one genuine global section g,
construct its degree-240 zero algebra using quotient spaces in section
degrees 3,4,6, and lift the rank-120 summand belonging to E. Its defining
idempotent is lifted with the polynomial 3e²−2e³, which squares the
idempotency error. This is the explicit argument of
[Stacks, Lemma 10.32.6](https://stacks.math.columbia.edu/tag/00J9).
The full multiplication matrix verifies idempotency, rank and the kernel
representing the actual lifted effective divisor. E may be nonreduced;
only its complement in div(g) must be disjoint.

For precision doubling k to 2k, let A' be this actual class lift and
R=3A'+Delta. R reduces to zero modulo 31^k. The formal reduction kernel
is killed by 31^k: in formal coordinates multiplication by 31^k kills
the linear term, while all quadratic terms vanish modulo 31^(2k).
Thus A=A'−inv3*R, where inv3=(2*31^k+1)/3. The corrected class is
checked directly for 3A=−Delta, Frobenius invariance and tau(A)=−A.
This takes 12/26 add-flip operations at four/eight digits, compared with
172/196 for the full annihilator scalar. Independent saved-data checks
prove the two routes give the same class at both precisions. At four
digits they also give identical coefficients in the old 80-entry gauge.
No Jacobian order is assumed.

`cm_frame_cubic_precision_{4,8}_formal_comparison.json` records the
comparison. Script 226 adapts the same bounded jobs to the pointed
previous representative for 16 and 32 digits. The sixteen-digit scalar correction and independent idempotent/class
check have completed. At 32 digits the direct linear correction below
replaces the scalar chain.

## Linear correction in the pointed coordinates

Scripts 227–231 provide a faster correction, verified first at eight
digits against the completed model. Normalize the actual class lift A'
and B=−2A'−Delta in the unique pointed chart. Their matrices C0 and C1
agree modulo 31^k. Since (31^k)^2=0 modulo 31^(2k), set
C_new=(2*C0+C1)/3. On this infinitesimal neighbourhood the Abel map and
its pointed inverse are affine on the deformation spaces. Thus this
interpolation corresponds to A'−(3A'+Delta)/3.

More explicitly, the pointed condition gives h0(E40)=1, so the
Sym^40(X) to Pic^40(X) map is étale at the residual divisor. The section
matrix is a regular coordinate map on this neighbourhood. For any
polynomial equation of its image, Taylor terms of order two in
C1−C0 vanish over the square-zero ideal. Consequently the interpolation
stays on the divisor parameter space. The same linearity applies to the
class error, with 3 invertible.

This argument is backed by an actual-divisor certificate: script 230
chooses a section from the interpolated matrix, reconstructs its zero
algebra and rank-120 idempotent, and verifies that the resulting genuine
divisor matrix is exactly C_new. Script 231 then checks 3A=−Delta and
both symmetries. At eight digits it agrees with the full scalar class
and equals the entire saved pointed matrix, entry for entry.

The eight-digit jobs take 44.433 s for B, 27.357/27.192 s for its two
pointed charts, 40.122 s for the actual-divisor certificate, and 52.719 s
for the direct class check. The certificate root is
`cm_frame_cubic_pointed_8_newton_third.json`. At sixteen digits the complete pointed matrix and all core function
coefficients agree exactly with the 51-operation scalar route. The
32-digit linear correction is verified directly, including its actual
divisor and class relation; it does not repeat the long scalar chain.
This infinitesimal interpolation and its checks are local deductions,
not an attribution to the M23 paper.

## Completed timings and resumption

| Precision digits | Pointed constructor, seconds | Independent check/controls |
| --- | ---: | --- |
| 1 | 26.992 | 36.395 / 28.712 / 34.209 |
| 2 | 30.200 | 40.382 / 35.841 / 38.813 |
| 4 | 31.997 | 44.017 / 36.500 / 42.108 |
| 8 | 114.545 | 152.996 / 133.557 / 149.475 |
| 16 | 176.869; direct 118.179 | Stages 39.425 / 91.025 / 121.810; controls 109.535 / 117.474 |
| 32 | Direct 129.098 | Stages 40.064 / 102.107 / 75.014; controls 62.829 / 73.793 |

The independent checker reconstructs all saved supports and evaluation
points, checks the class and descent, verifies the actual pointed move,
all final function inclusions, the norm, both equation representations,
local jets, and reduction to every preceding coefficient array. Its two
controls add 31^(n−1) to the norm scalar and a septic coefficient and must
fail at the intended identities. It uses a different random seed and
does not repeat the function search.

Completed internal-chart certificate: `cm_frame_cubic_pointed_32_check.json`.
The 16-digit provenance audit checks 894 file hashes across 297 linked
JSON records. Runner 245 also audits the 32-digit roots and exact route
comparisons; its output is a separate immutable certificate.

Do not rerun an active job or overwrite a failed diagnostic. The next
recognition experiment must reserve unused digits and separate evidence
of a small coefficient field from an exact equation certificate. The
pointed choice preserves fields of definition; it does not bound heights
or prove that the selected class is defined over the expected field.
The monomial basis and high prescribed vanishing can inflate coefficient
heights, so basis conditioning matters before a large recognition run.

## Smaller output normalization: K_X+2P

The high multiplicity 80P is convenient for the local class coordinates,
but it makes coefficient recognition difficult. A separate output choice
uses H=K_X+2P, also of degree 80. Choose the canonical divisor
K_X=pi*div_C(X16)+R_ram, where R_ram lies over B2. The new effective
representative E=H+E40 is again selected by a unique linear intersection.
This change retains the useful 80P chart for class lifting.

To construct L(2D0-H), first form L(3*pi*K_C-R_ram). Its even part is
H0(3K_C-B2), dimension 57; its odd part has dimension 66. The even part
comes from the exact 27-dimensional quadratic space vanishing on B2,
and the odd part from the 36 old odd sections multiplied by canonical
linear sections. At P, two further jet conditions remove the terms of
orders one and two. This gives a 121-dimensional subspace of L(2D0).
Intersecting it with the complementary-divisor space of dimension 81
gives a single line. The saved g/r move is checked as an actual divisor
move in the same class.

Now a has poles of order at most 2K_C and b=h+tau(h) has poles bounded by
3K_C+B3. The equation therefore becomes

\[
\ell T^3-3A_2\ell T-R_4=0,\qquad \operatorname{wt}(T)=1.
\]

Only 45 quadratic and 105 quartic coefficients are needed. E has
multiplicity three at P, so h starts at w^9 and a at w^6. Their leading
coefficients satisfy -h0²=a0³. With the already fixed r=sqrt(-3), set
lambda=r*a0/h0. Then a starts with 3w^6 and h with 3r*w^9. This uses the
existing branch orientation, with no new root choice. If orientation
conjugation exchanges h and tau(h), it also negates r; these leading
conditions are compatible with that exchange.

Scripts 249/253 construct compatible models at 1,2,4,8,16,32 digits in
`cm_frame_cubic_adjoint_n.{json,m}`. Construction times are respectively
23.388, 24.216, 26.369, 80.405, 120.714 and 162.229 seconds. Script 251
checks the saved fixed space, unique intersection, move, function
divisors, norm, scaling and both coefficient arrays. Runner 252 includes
highest-digit norm and trace controls. The special fibre passes all
three jobs (19.292 / 16.730 / 18.319 s); the 32-digit independent check and both controls also pass
(113.222 / 93.785 / 114.508 s). The completed root is
`cm_frame_cubic_adjoint_32_check.json`.

Scripts 256/257 prove the explicit isomorphism
v_adjoint=22*(r_move/g_move)*v_pointed over F31. Both the Kummer function
and involution identities hold on 2048 points, above the 1200 pole bound.
Thus the smaller model retains the proved counts 68/2818. The certificate
is `cm_frame_cubic_adjoint_isomorphism.json`; the job takes 5.089 seconds.

## Recognition and an exact small rational basis

Scripts 232/238/239 test individual Q/F candidates, global projective
ratios and normalized local coefficients for the 80P model at 8,16,32
digits. Every search reserves half the digits. No candidate survives.
Positive rational/F controls pass and corruption of the first unused
digit is rejected. This is a bounded search, not a field exclusion.

Scripts 246–248 separately investigate the rational space
H0(4K_C-80P32). The constraints are computed to 128 and 256 digits without
lifting a cubic class. A rank-105 congruence lattice with 80 conditions
is reduced using only 128 digits. None of its basis-row candidates
survives the other 128 digits. This does not rule out a rational basis;
it shows that this particular recognition attempt is ineffective.

For the smaller model, A2 lies in H0(2K_C-D17-3P32), dimension 25.
Script 254 constructs this space **exactly over Q** using only three
local vanishing conditions on the known 28-dimensional D17 quadratic
space. It verifies all curve equations, the local parameter, quotient
coordinates modulo the canonical ideal, and the dimension. Script 255
saturates the integer lattice, reduces its basis, verifies the same
rational row space, and finds a unit coordinate minor at 31. The reduced
basis has integer coefficients of at most four decimal digits. This is
an exact rational basis, not a reconstruction from finite precision.

The certificate is `cm_frame_cubic_adjoint_quadratic_space.json`.
Script 258 expresses each lifted A2 in that basis and verifies all 45
coefficients and the prescribed leading coefficient 3. Separate Q/F
recognition still gives no surviving candidates at 8,16,32 digits.
Script 259 therefore tests **joint projective recognition over F**, with
one common F-valued scale, using 24 of the 32 digits and reserving eight.
The lattice has rank 200 and 24 congruence conditions. Known F-valued
projective controls and unused-digit errors test the procedure. All eight embeddings (roots 4,9,10,11,20,21,22,27 modulo 31) are tested.
Each known control is recognized and each first-unused-digit corruption
is rejected; the actual A2 has no surviving candidate. This is a bounded
LLL basis-row search, not an exclusion of definition over F. No exact
number-field equation has been recovered.

Corrected implementation diagnostics are kept outside the successful
proof roots: the earlier all-evaluations-unit assumption, the old-gauge
180-second timeout, Sage's default cache permission failure (fixed with a
dedicated DOT_SAGE under /private/tmp), and an undefined monomial API
name (fixed using Magma's documented
[Exponents](https://magma.maths.usyd.edu.au/magma/handbook/text/246)).

## Current artifacts and next step

The compact equation package is
`dembele/data/computed/cm_frame_cubic_adjoint_package_32.json`. It includes
the rational base quadrics, ell, the exponent arrays, both coefficient
arrays and the modulus. It uses the original JSON coordinate names
X0,...,X15; Magma uses X1,...,X16 in the same array order. The equation
specifies the component dominating C on ell != 0. On the special fibre,
take its smooth projective normalization; clearing ell can introduce
vertical components. The verified genus and point counts refer to that
normalized cover.

The combined audit is `cm_frame_cubic_adjoint_audit_32.json` (runner 260).
It verifies 1099 file hashes across 387 linked JSON records and binds
all earlier class and function checks, both model isomorphisms,
the exact rational basis and recognition diagnostics. Earlier D68–D81
arithmetic artifacts remain frozen, including the recorded D78 root.
The independent 32-digit adjoint check finished after the initial
recognition pilot; the combined audit binds both to the same unchanged
equation data.

The next bounded reconstruction experiment is a 64-digit class lift
using the verified linear correction, followed by this K_X+2P output
normalization and joint recognition in the exact small A2 basis. The
current command-line lift wrappers mostly stop at 32 digits, so extend
the orchestration without modifying hash-bound sources. Preserve the
180-second/2 GB Magma limit and split longer stages if needed. Reserve
unused digits. If a candidate appears, verify it in the function/divisor
identities over its proposed number field before using it for torsion.
Failure of the present searches is not a reason to assert a larger
coefficient field or discard the selected third.

All D68–D81 arithmetic inputs are preserved. The prescribed Fuchsian
monodromy, arithmetic identification, hyperellipticity conflict,
characteristic-zero cubic, target torsion and final field remain open.
