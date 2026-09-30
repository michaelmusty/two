# The genus-64 cubic passes two Frobenius comparisons

Date: 2026-09-22. Decision D80. This tests the explicit finite-field
cubic constructed in [D79](cm-frame-cubic-cover.md).

**Result:** the smooth projective normalization Y has

\[
 \#Y(\mathbf F_{31})=68,\qquad
 \#Y(\mathbf F_{31^2})=2818.
\]

Both counts match the existing genus-16 old plus 48-dimensional new
Hecke prediction. A separate calculation checks every fibre using the
quadratic resolvent and Kummer function, without factoring the cubic.
A deliberately changed fibre count is rejected.

These are two power traces at one prime. They support the candidate
cover but do not prove its full Euler factor, prescribed Fuchsian
monodromy, arithmetic identification, or characteristic-zero descent.

## Counting the normalized fibres

[Script 180](../magma/180_cm_frame_cubic_point_count.m) enumerates the
base points via the degree-30 map (X15:X16), including its infinity
fibre. Frobenius orbits reduce the work over F31^2. All points satisfy
all 91 original curve quadrics. There are respectively 50 and 1,400
distinct projective points, in agreement with D69's independently
certified base counts.

At a point where Q4 is a unit and the cubic discriminant is nonzero,
the equation T^3-3*A4*T-P10/Q4 is finite étale over the local ring.
Its distinct rational roots therefore count the normalized fibre.
At other points the denominator-cleared equation alone is insufficient.

The rational point P32 lies in B2 and has transposition inertia. The
normalizer of this inertia subgroup in S3 is itself, so the decomposition
group equals inertia. The two inertia orbits on the three sheets are
both rational: this fibre contributes two points. Direct evaluation
excludes all other points of B2 and all of B3 over both fields.

For each remaining exceptional fibre, a unit 14-by-14 Jacobian minor
on C gives a local parameter t. Exact coordinate series through t^31
satisfy all 91 quadrics. The valuation of n/d is even. Its leading
unit determines whether the normalized quadratic fibre splits.

- A nonsplit quadratic fibre gives a transposition Frobenius in S3,
  hence one point on Y.
- At a split quadratic fibre, expand one branch w^2=n/d and evaluate
  the saved function h=27*u/q. Its valuation is divisible by three.
  Dividing by t to that valuation leaves a unit whose residue is a
  cube precisely when the cubic fibre splits completely. Since both
  fields contain mu3, the contribution is three or zero.

The leading coefficient is only used after the computed Laurent
series has sufficient precision to determine its valuation. All square
identities and implicit curve equations are checked. Changing the local
parameter multiplies the leading unit by a cube, so it cannot change
the split/non-split result. The involution exchanges the two branches;
h*tau(h)=a^3 makes their cube tests equivalent. This uses the same
[Kummer unit-root construction](https://stacks.math.columbia.edu/tag/03PK)
as D79.

| Field | Base points | Fibres with 0 / 1 / 2 / 3 rational points | Local exceptions | Total |
|---|---:|---|---:|---:|
| F31 | 50 | 9 / 27 / 1 / 13 | 6 | 68 |
| F31^2 | 1400 | 219 / 362 / 1 / 818 | 12 | 2818 |

The local-exception column excludes the separately treated P32 fibre.
All six exceptions over F31 contribute three points; over F31^2 eight
contribute three and four contribute one.

## Independent check and comparison

[Verifier 182](../magma/182_cm_frame_cubic_point_check.m) takes the saved
base points. Their distinctness, curve membership and the previously
certified cardinalities prove completeness without a second point search.
It counts every fibre by quadratic splitting and the Kummer cube test,
without using Q4, A4, P10 or cubic factorization for the count.

Most function values are evaluated directly. Where necessary, it uses
different local coordinates: the last nonzero projective anchor,
reversed variable/quadric choices, and series precision 24 instead of
32. All original curve equations and square identities still pass.
It needs 5 and 14 local expansions, respectively. Its quadratic fibre
distributions (split, nonsplit, branch) are (22,27,1) and (1037,362,1).
Every individual Y fibre agrees with the constructor, including all
exceptional fibres. Changing the first saved fibre count by one modulo
four fails this check.

The Hecke input is the existing
[T31 characteristic-polynomial bank](../data/computed/levelraise_p2k_charpolys.m)
from script 58, already used in scripts 64/80 and D69. No new Hecke
module computation is performed. Extract the four quartic factors
forming p16 from the genus-40 bank, and multiply by the degree-48 new
factor p48. For p64=p16*p48, the predicted Frobenius characteristic
polynomial is x^64*p64(x+31/x). Its first two power traces agree with
the independently counted values:

\[
 \operatorname{Tr}(\mathrm{Frob}_{31})=32-68=-36,\qquad
 \operatorname{Tr}(\mathrm{Frob}_{31}^2)=962-2818=-1856.
\]

Thus the beginning of det(1-T*Frob) is

\[
 1+36T+1576T^2+\cdots.
\]

Only these coefficients have been measured geometrically. The saved
full Hecke polynomial remains a prediction for the candidate Y.

## Artifacts and bounds

- [Point lists and fibre counts](../data/computed/cm_frame_cubic_point_counts.json),
  collected by [181](../pari/181_cm_frame_cubic_point_data.py).
- [Combined comparison certificate](../data/computed/cm_frame_cubic_point_check.json),
  maintained by [183](../pari/183_cm_frame_cubic_point_check.py).
- The two `cm_frame_cubic_point_count_F31*_input.m` files contain the
  verifier inputs. F31^2 elements use c0+31*c1 in the fixed field
  F31[b]/(b^2+29b+3).

All Magma jobs have 180-second / 2-GB bounds. The first successful
enumeration/counting runs take 6.282 s over F31 and 87.304 s over F31^2.
The independent checks take 1.069/6.727 s, and the wrong-count control
1.119 s. Later rebuilt records may have different timings. The initial
local-parameter scope error and the verifier's conditional-load syntax
error are archived with their sources; neither had a final PASS. All
jobs are finished.

Historical job records retain the inputs used at the time. Current
certificates bind the immutable historical logs/source snapshots, and
bind current successful inputs separately, so rebuilding does not
invalidate the proof through an obsolete diagnostic dependency.

Final rebuilds of 179 and 183 both pass, including all three corruption
controls. The recursive certificate check validates 375 distinct hashes
across 117 linked JSON documents; D78's root certificate is unchanged.
All 210 checked local Markdown links, Python syntax and whitespace checks
pass. No jobs remain running.

```sh
python3 dembele/pari/183_cm_frame_cubic_point_check.py --collect-only
python3 dembele/pari/183_cm_frame_cubic_point_check.py
python3 dembele/pari/183_cm_frame_cubic_point_check.py --rebuild
```

The next bounded construction is a first 31-adic lift of the marked
cubic class and function identities, beginning modulo 31^2 with fixed
matrix pivots and explicit section normalizations. Higher precision
should follow a checked first step. The two point counts justify
continuing with this candidate; they do not remove the base/marking/
branch-half identification or hyperellipticity questions, select a unique
third, or replace the prescribed Fuchsian monodromy comparison. Target
torsion and the final field polynomial remain unconstructed.

## A concrete scalar for the first class lift

There is a useful way to specify the next class calculation without
assuming the proposed Jacobian/Prym order. D78 computed A=c*Delta and
verified 3A+Delta=0, where

\[
 c=55644451508958846968904807569421159,\qquad
 N=3c+1=166933354526876540906714422708263478.
\]

Thus N annihilates this particular Delta modulo 31. It is not asserted
to be a group order. On the good-reduction Jacobian over Z/31^2, the
kernel of reduction is an additive tangent group killed by 31: the
formal group law is linear on the square-zero ideal (31). If Delta2
is the lifted marked branch class, then N*Delta2 belongs to that kernel.
Consequently

\[
 c_2=31c+10=1724977996777724256036049034652055939,
 \qquad A_2=c_2\Delta_2
\]

satisfies 3A2+Delta2=31*N*Delta2=0. Since c2-c=10N, A2 reduces to
the saved A. The 121-bit scalar is concrete input for a bounded lift.
The same argument gives c_n=(31^(n-1)*N-1)/3 modulo 31^n; reduction
kernel filtrations are killed one step at a time by 31.

Multiplication by three has invertible differential at 31, as in
[Stacks, Lemma 39.9.9](https://stacks.math.columbia.edu/tag/0BFH).
Together with [unique lifting for étale morphisms across nilpotent
thickenings](https://stacks.math.columbia.edu/tag/06NE), this explains
uniqueness of the class lift *with the chosen reduction*. It does not
prove uniqueness among the different thirds in the special fibre.
The scalar formula itself is the preceding local deduction.

No class matrix modulo 31^2 has yet been computed. First lift the
actual evaluation points and complete section spaces of X, and use
unit-pivot matrix operations. Entrywise lifts of finite-field section
matrices do not automatically represent sections or divisors. The
lifted class relation, branch conditions and function/norm identities
must then be checked explicitly.
