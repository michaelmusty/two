# An exact branched double cover modulo 31

Date: 2026-09-18. Decision D71. This continues
[D70's marked-divisor computation](cm-frame-marks.md).

**Result:** on the verified genus-16 candidate over F31, explicit
quadrics q_num and q_den give a rational function u=q_num/q_den with

\[
\operatorname{div}(u)=D_{17}+15P_{32}-2E,\qquad \deg E=16.
\]

Consequently the smooth projective model of `z^2=u` is a geometrically
connected genus-40 double cover, branched exactly at `B2=D17+P32`.
It has **45 points over F31**, agreeing with the genus-40 norm-one
Hecke prediction; its constant twist `z^2=3u` has 55 points.
The equation is given by a function-field extension: the naive graph
equation at zeros and poles is not being claimed to be a smooth model.

This is an unconditional construction on the candidate **over F31**.
It is not a construction over Q or F, an identification with the saved
sign cover, or a proof of the base curve's Shimura identification.
The actual genus-64 cover, target torsion and nonsolvable field
polynomial remain unconstructed.

## 1. Explicit data and independent certificate

The human-readable equation is in
[`cm_frame_resolvent_equation.txt`](../data/computed/cm_frame_resolvent_equation.txt).
Machine-readable coefficients, monomial ordering and 29 quadrics
cutting out E are in
[`cm_frame_resolvent.json`](../data/computed/cm_frame_resolvent.json)
and [`cm_frame_resolvent.m`](../data/computed/cm_frame_resolvent.m).
The coefficient arrays use one-based coordinate pairs and ordinary
mixed monomials, with no factor of two.

The independent verifier
[`122_cm_frame_resolvent_check.m`](../magma/122_cm_frame_resolvent_check.m)
does not use the guessed Jacobian order or replay the class arithmetic.
It checks:

- The saved 16-term jets satisfy all 91 curve quadrics, have the
  correct constant point, and use a unit 14-by-14 implicit Jacobian.
  Their vanishing conditions cut out the length-15 divisor 15P32.
- The supplied ideal cuts out E of degree 16, disjoint from P32.
  Squaring its ideal on the smooth curve gives 2E of degree 32.
- A saturated colon ideal gives a residual divisor T of degree 28.
  Exact saturated-ideal equalities prove
  `div(q_num)=D17+15P32+T` and `div(q_den)=2E+T`.
  The supports needed for the intersections are checked disjoint.

The reduced branch markings and smoothness of the base are D69–D70
certificates, whose input files and results are included in the hash
chain. The ratio identity proves the claimed square class without any
cardinality assumption. Its odd valuations are precisely at B2.
They remain odd after extending the constant field, so u is not a
geometric square. Tame Riemann–Hurwitz gives

\[
2g(S)-2=2(2\cdot16-2)+18=78,\qquad g(S)=40.
\]

The corresponding degree-nine half of B2 is

\[
L=\mathcal O(E-7P_{32}),\qquad L^{\otimes2}\simeq\mathcal O(B_2).
\]

This replaces the excluded D70 choice L=O(B3). No uniqueness of L is
proved; geometric two-torsion can change a square root of a line bundle.

## 2. Discovery by divisor arithmetic in the canonical embedding

Let `D0=D17-17P32`. The saved genus-16 Hecke trace polynomial P16 suggests

\[
N=P_{16}(32)=1640801490553691915934375.
\]

N is odd, but it is **not a proved Jacobian order for the candidate**.
We use it only to propose the half class
`[(N+1)/2]D0`, with scalar `820400745276845957967188`.
The 80-bit double-and-add computation produces E-16P32. The final
independent identity verifies `2(E-16P32) ~ D0`. Thus the guess
succeeded for this class; it does not certify N, a full Euler factor,
or absence of rational two-torsion.

The arithmetic avoids expensive general function-field reduction.
Represent a degree-zero class by an effective divisor A of degree
r<=16, disjoint from P32, as A-rP32. Divisor addition uses intersections
for disjoint supports and squared ideals for doubling. To reduce a
divisor D of degree d between 17 and 32, choose a canonical quadric
q0 vanishing at D but nonzero at P32. Write

\[
\operatorname{div}(q_0)=D+T,\qquad \deg T=60-d.
\]

Set m=d-16. A quadric q1 vanishing at T+mP32 exists by Riemann–Roch,
since `deg(2K-T-mP32)=16`. Its complementary divisor A has degree 16,
and `D-dP32 ~ A-16P32`. Remove any P32 component from A and adjust
the reference degree. Every actual step checks the degrees and
disjointness needed by this construction. Homogeneous degree-two
normal forms give the complete space of canonical quadrics.

This is a direct implementation of complementary-divisor arithmetic,
using `ColonIdeal` and `Saturation` as described by the
[Magma divisor/sheaf handbook](https://docs.magma-maths.org/AlgebraicGeometry/Sheaves/div_maps.html).
The source is
[`121_cm_frame_resolvent.m`](../magma/121_cm_frame_resolvent.m).
The initial run used a scratch copy with identical bytes; its command,
source hashes and **466.760 s** wall time are recorded in the discovery
JSON. Its limit was 900 s and 2 GB. The full log includes every scalar
step and the final one-dimensional Riemann–Roch space.

## 3. Point counts and the constant twist

The verifier enumerates all 50 points of C(F31) through the same
degree-30 projection used in D69, including the fiber at infinity.
The single rational branch point contributes one point on each cover.
Every other point contributes two or zero according to the square
class of the local unit of u. At two common zeros of q_num and q_den,
formal implicit coordinates through degree seven recover that unit;
all 91 equations are checked on these jets as well.

The individual fiber records sum to 45 for u and 55 for 3u. Their
sum is 100=2#C(F31), as required. The coefficient of degree 39 in the
saved degree-40 T31 polynomial is 13, so the norm-one Hecke prediction
is `31+1-(-13)=45`. This singles out u among **these two constant
twists for this comparison**, not among all possible branched covers.
It does not certify the global monodromy or identify the curve.

## 4. Reproduction, controls and unsuccessful alternatives

```sh
# Independent certificate and point counts, about 11 seconds:
python3 dembele/pari/122_cm_frame_resolvent_check.py
# Validate saved hashes and recompute totals from the saved fiber records:
python3 dembele/pari/122_cm_frame_resolvent_check.py --collect-only
# Optional full discovery, about eight minutes, then the certificate:
python3 dembele/pari/122_cm_frame_resolvent_check.py --discover
```

The checker passes in **10.897 s** with a 120 s/2 GB cap. Its runner
requires a successful exit, explicit PASS marker, and no Magma error
markers; hashes bind the scripts, input data and output log.
The result is
[`cm_frame_resolvent_check.json`](../data/computed/cm_frame_resolvent_check.json).
Discovery loads a task-owned scratch input at
`/private/tmp/dembele_d71_half_input.m`; the runner restores it from
the archived `cm_frame_resolvent_input.m` before `--discover`.

A separate negative control changes the numerator's X1^2 coefficient
by one. The verifier rejects it at membership in the D17+15P32 ideal,
before declaring a cover. Its source, log and **2.026 s** result are
`cm_frame_resolvent_negative_control.{m,out,json}`. This confirms that
the certificate detects a corrupted radicand.

Two bounded alternatives are retained in
[`cm_frame_resolvent_probe_limits.json`](../data/computed/cm_frame_resolvent_probe_limits.json).
Generic `FunctionField(C_candidate)` did not finish within 90 s.
Using the known rank-30 coordinate algebra instead gives an explicit
function field and genus 16 in about 36 s. The integral bases come
from the two free projective charts, with maximality justified by
squarefree trace discriminants, before calling `SetOrderMaximal`.
Prime-ideal-to-place conversion supplies P32 and D17 in about 44 s,
but the first native `Reduction` still fails to finish by 150 s.
Do not repeat these unchanged probes. The
[function-field creation/order](https://docs.magma-maths.org/GlobalFields/AlgebraicFunctionFields/creation.html)
and [divisor](https://docs.magma-maths.org/GlobalFields/AlgebraicFunctionFields/divisors.html)
handbooks explain the interfaces; the setter is not itself a
maximality proof. Intermediate matrix-inversion and coefficient-
conversion bottlenecks were bypassed before the retained probe.

## 5. Next construction gate

The concrete next experiment is a **first 31-adic lift of the half
line bundle, modulo 31^2**, with the doubled class checked against B2.
Doubling has invertible differential in characteristic 31, as in
[Stacks Project, Lemma 39.9.9](https://stacks.math.columbia.edu/tag/0BFH).
This motivates a Newton/Hensel approach on the relative Picard variety;
an explicit lifting implementation and arithmetic reconstruction are
still needed. Finite-field coefficients cannot simply be interpreted
as characteristic-zero coefficients.

After a verified lift, seek arithmetic recognition over F and match
the saved sign monodromy. Then construct the specified cyclic cubic
extension over S, its S3 closure, and the genus-64 quotient Y. Branch
supports alone still do not determine those data. Q descent is not
assumed. The independent Shimura-side identification problem, including
the previously recorded hyperellipticity conflict, remains open.
No claimed field polynomial follows from these finite-field results.

D68–D70 artifacts, numerical banks, external checkouts and backend code
are unchanged. D63's 111 tests remain the latest full backend regression;
D71's exact certificates and negative control are separate. No remote
job, message, commit or cleanup was performed; all computations finished.
Final maintenance checks validate 60 source/artifact hashes across 20
JSON documents, 106 local Markdown links, the readable equation against
the coefficient arrays, Python syntax, and whitespace. Collection of
the saved exact certificate also passes.
