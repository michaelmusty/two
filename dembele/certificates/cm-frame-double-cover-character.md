# D87: comparing the double cover with the Fuchsian sign character

Date: 2026-09-23. This continues the marked arithmetic comparison requested
after the negative D86 coefficient reconstruction. It does not increase
31-adic precision or solve another differential system.

## Result and scope

Both saved differential banks give the expected sign on **all 277 side
generators** of the saved Fuchsian group. An independent checker reconstructs
the square-root branches from the retained sampled values, by accumulating
arguments rather than choosing the nearest square root.

| Saved bank | Paths | Samples | Generators matched | Maximum distance from expected sign |
|---|---:|---:|---:|---:|
| 16,384 terms, radial paths | 550 | 56,232 | 277 | 7.84e-14 |
| 12,288 terms, radial paths | 550 | 56,232 | 277 | 2.00e-8 |
| 16,384 terms, bent paths | 550 | 79,941 | 277 | 7.86e-14 |

The bent paths use angular displacement `0.03*sin(pi*t)` from the radial
paths, with the same endpoints. Their endpoint roots agree with the radial
roots to relative error below `1.46e-14`; the two banks agree below `1.00e-8`.
All three campaigns are complete, with 192,405 retained samples in their
nonduplicated path sets.

This is **numerical evidence**, not a rigorous analytic or arithmetic
identification. Its significance is that matching the branch divisor alone
would leave a torsor under `Jac(C)[2]`, of size `2^32` over the complex
numbers. Comparing the character on a generating set tests this otherwise
hidden choice. The comparison supports retaining the present double cover.

The cover being tested is the exact genus-40 curve

\[
X:\quad z^2=n/d\quad\text{over the genus-16 candidate }C,
\]

with odd branch divisor `B2 = D17 + P32`, of degree 18. This is the sign
quotient of the proposed S3 closure. It is not the genus-64 cubic itself.
No exact number-field cubic or target field polynomial has been recovered.

## The comparison

Script 66 already computes the exact S3 images of the quaternionic side
generators. We take their permutation signs independently from
`genus64_cosets.gp`. The 277 images have 133 negative and 144 positive signs.
The order of these images agrees with the disk-action order: Rickards's
`afuchelts` and `afuchactions` retrieve parallel vectors of the same stored
boundary, assembled from the same element indices. Script 67 preserves
that order when recentering at the order-32 elliptic point.

Let `w` be this disk coordinate, `r = 0.99991`, and

\[
v=(w/r)^{32},\qquad P(v)=H(v)M.
\]

Here `H` is the saved 16-column differential bank and `M` is its saved CM
frame change. The common `w^31` factor in the pulled-back differentials
cancels from the ratio of quadrics. Thus the candidate function pulls back
numerically as

\[
U(v)=n(P(v))/d(P(v)),\qquad R(v)=U(v)/v.
\]

At the central branch point, `U` has a simple zero in the coarse parameter
`v`. The initial value for continuation is `R(0)=n_1/d_0`, obtained from
the first coefficients; we do not divide the small numerical constant
error by zero. The apparent numerator constant divided by its linear
coefficient has absolute value `2.95e-20` in the current bank and `4.50e-15`
in the earlier bank.

Conditionally on the marked analytic identification, the other zeros and
poles of `R` have even orders and its meromorphic square root is single
valued on the disk. A square root of the pulled-back cover function is

\[
s(w)=(w/r)^{16}\sqrt{R((w/r)^{32})}.
\]

For a side generator `g`, the character is therefore computed as

\[
\chi_X(g)=
(gw/w)^{16}\,
\frac{\sqrt{R((gw/r)^{32})}}{\sqrt{R((w/r)^{32})}}.
\]

We compare this with `sign(rho(g))`. There are 275 nonrotation generators
and two pure rotations. The former use 550 endpoint paths. For the latter,
the folded parameter is fixed and the factor `(gw/w)^16` gives the sign.

## Numerical checks and preserved corrections

The initial balanced-midpoint experiment is retained. Such a midpoint can
be an elliptic fixed point, where every pulled-back differential vanishes.
The resulting ratio can be sensitive to error even when its two endpoint
values agree. In particular the balanced point for side 272 is fixed to
the saved accuracy. A full-polynomial versus direct-substitution check
rejected that attempt. No character conclusion uses those midpoints.

The accepted samples use script 79's deterministic hyperbolic
perturbations, of radius at most `0.005` and seed `71420`, about the balanced
points. All endpoints stay within the saved expansion disk. The maximum
relative discrepancy between `U(gw)` and `U(w)` is `1.59e-13` for the current
bank and `3.99e-8` for the earlier bank.

For efficient repeated evaluation, script 307 forms the two **full**
polynomials `n(HM)` and `d(HM)`, including every product coefficient. Script
310 checks them against the independent route of first evaluating `H`,
then applying `M` and substituting into the quadrics, at all 550 accepted
endpoints in each bank. Relative errors are below `1.23e-49`.

Uniform path meshes are insufficient. In the first 25-generator pilot,
128 steps gave apparent mismatches at sides 5 and 8. Both disappeared on
refinement. These exploratory outputs remain intact. They are sampling
failures, not evidence for a different cover.

Script 313 refines paths using sampled changes in argument, log modulus,
and endpoint logarithmic derivatives. It first uses tolerance `0.30`,
then `0.15`, and requires the endpoint branch choices to agree. It retains
every final sample, including its path parameter, `R` value and logarithmic
derivative. Independent value checks and centered finite differences
check the derivative evaluator. These derivative estimates guide
refinement; they are not bounds over entire path segments.

Scripts 315/316 accelerate interior evaluations by omitting only finite
polynomial tails with a checked absolute ball bound. If the coefficient
bound is `M = 10^8`, then both omitted value and derivative are bounded by

\[
\frac{Mn\,|v|^{L-1}}{1-|v|}.
\]

The coefficient bound is checked, the tail bound is checked in ball
arithmetic below `1e-65`, and the error is added to the computed balls.
Full-polynomial and accelerated continuations agree on the 26-path control.
This check bounds an omitted part of a **finite polynomial**. It supplies
no bound for the unsaved infinite differential tail.

Script 318 uses Python's standard library to reconstruct all sampled
windings independently. Known winding controls include odd and even
winding numbers; an incorrectly reversed stored square-root branch is
rejected. The trivial character disagrees with 133 exact S3 signs. Every
computational job has a 180-second process-group timeout. Earlier rejected
attempts, uniform-mesh outputs, sources and logs are preserved.

The 52 job records comprise 51 successful jobs and the rejected initial
midpoint cache check. The longest job took 118.136 seconds. No job remains
running. The earlier 128-digit audit was rerun successfully: all 2,009 file
hashes, 769 linked JSON records, eight integer height identities and 21
remote job records remain valid.

## Artifacts and recheck

Root: [cm_frame_double_cover_character_d87.json](../data/computed/cm_frame_double_cover_character_d87.json).
It verifies **2,187 file hashes / 875 linked JSON records**, including the
unchanged D86 root and all new sources, sampled paths, controls and logs.
The two `cm_frame_double_cover_polynomials_*_d87.json` files contain the
generator order, endpoint coordinates, exact expected signs and checked
polynomial-cache provenance. The `cm_frame_double_cover_tail_*_d87.json`
files retain the adaptive samples.

```sh
python3 dembele/pari/318_cm_frame_double_cover_character_audit.py --check
```

This recomputes the sampled phase choices and character comparisons using
Python's standard library. It does not launch numerical jobs or promote
the samples to an interval certificate. Scripts 306–317 and their bound
artifacts are frozen; use a new source and output name for any follow-up.

## What remains open

1. The canonical equations, rational point, closed branch divisors and
   rational double cover are exact objects. Their identification with the
   marked quaternionic curve still uses numerical analytic data. The saved
   geometry has no interval certificate of coverage, and the differential
   banks have no rigorous analytic truncation bound.
2. A constant arithmetic quadratic twist is invisible to this complex
   character test: every nonzero complex constant is a square. However,
   D77 already gives a separate exact constraint, described below. There
   is no reason to restart an unrestricted search for scalar twists.
3. Identifying the double cover does not identify the anti-invariant
   third-division class used for the cubic. D84's nine locally tested
   choices do not exhaust its `3^48` geometric torsor. Its required global
   Galois action remains unproved.
4. The published hyperellipticity discrepancy remains unresolved. No new
   claim about it follows from this character comparison.

The source audit is consistent with these limitations. Dembélé's
[Theorem 4.1 and Lemma 5.2](https://arxiv.org/pdf/1906.06772) describe
canonical arithmetic level maps and descent of the maximal-level curve
and quotient. They do not identify our reconstructed equations or select
our cubic class. D85 already explains why marked descent needs the field
of moduli to be established first.

## Combining this with the existing exact twist constraint

The [D77 fibre certificate](cm-frame-B3-fiber.md) proves that the normalized
fibre over B3 is `K(sqrt(-3))`, where `[K:Q]=9`. For this **fixed geometric
branch half**, it proves uniqueness of the F-scalar twist compatible with
a cyclic cubic cover totally ramified above B3. This is a previously
proved constraint, not a new result of the complex calculation.

Indeed, `K_F=KF` has odd degree nine over F. Replacing the cover function
by `c*n/d` changes the fibre square class from `-3` to `-3c`. The required
cube roots of unity are present precisely when `c` is a square in `K_F`.
For `s^2=c`, the norm identity gives

\[
c=(\operatorname{Norm}_{K_F/F}(s)/c^4)^2,
\]

so `c` was already a square in F. In particular, the apparently tempting
`-3` twist, invisible at 31, is already excluded by D77's fibre condition.

Consequently, a certified **arithmetic identification of the marked base**,
together with a certified geometric sign-cover comparison, would allow
this existing inertia argument to settle the remaining scalar twist.
The numerical result here addresses the geometric-half choice; it does
not by itself supply those certifications.

Retain the present double-cover candidate, use D77's constraint, and focus
the next comparison on the marked base and the selected cubic class.
This diagnostic supplies no reason for an automatic 256-digit lift or
an arbitrary larger coefficient-field search.
