# D85: bounded 128-digit attempt and descent review

Date: 2026-09-22. The user authorized trying 128 digits, then proceeding
with the review if the attempt failed.

**Outcome:** the section spaces and local expansions were extended to
31^128, but construction of the actual lifted divisor failed within the
existing resource limits. Two implementations reached the 2 GB memory
cap; a version using smaller multiplication blocks timed out at 180
seconds. The verified cubic therefore remains at **31^64**. No 128-digit
cubic coefficients were produced and no 112/16 recognition test ran.
This is a resource failure, not a negative coefficient-field test.

The requested review was then completed. It separates three issues:
the normalization does not require a new root choice; descent over a
fixed base has no automorphism obstruction for this S3 cubic once its
field of moduli is established; the missing information is the global
Galois action on the selected third and its identification with the
prescribed arithmetic cover. No move to 256 digits is proposed.

## 1. The actual attempt

Runner 282 adapts the frozen 64-digit workflow to 128 without modifying
the earlier arithmetic sources. Executed driver snapshots, generated
adapters, inputs, outputs and job receipts are retained. Each Magma job
uses process-group runner 272, with 180 seconds and 2,000,000,000 bytes.

| Stage | Result | Wall seconds |
| --- | --- | ---: |
| Section spaces and evaluation points at 128 digits | Pass | 94.609 |
| Pointed local expansions at 128 digits | Pass | 105.349 |
| Actual divisor, precision-aware inverses | Memory limit | 65.268 |
| Actual divisor, released temporaries and pointwise scaling | Memory limit | 73.358 |
| Actual divisor, multiplication in blocks of at most 96 rows | Timeout | 180.0 |

Script 283 performs Newton matrix inversion at successively doubled
precisions and checks each returned inverse at the full precision.
Native Galois-ring controls in 284 compare inverses in sizes 1,4,9,16,32
and reject a change by 31^127. Scripts 285/286 release unused model
temporaries and replace dense diagonal row scaling by pointwise products;
288 checks these products against native arithmetic. Scripts 293/294
also bound multiplication workspaces by row blocks. Control 295 checks
native products across block boundaries as well as scaling and inverses.
These controls pass. They do not certify a divisor that was never output.

An initial block-product control (289/292) failed because Magma could
not put differently sized matrix blocks in one homogeneous sequence.
That failed source, log and receipt are retained; the corrected version
uses successive vertical joins. It passed control 295 before the final
divisor attempt. No failed record is overwritten or treated as accepted.

The construction was stopped at this bounded checkpoint. Retained
sections and jets can support a future algorithmic split, but there is
no new third, normalized cubic, highest-digit cubic check or recognition
result at precision 128. The existing 64-digit norm/trace corruption
controls and coefficient-height exclusion remain the relevant results.

## 2. The geometric ambiguity is much larger than nine

Write pi:X -> C for the exact candidate double cover, with genera 40
and 16 and involution tau. On geometric 3-torsion, pi_* pi^*=[2] and
pi^* pi_*=1+tau. Since two is invertible modulo three, pi^* embeds
J_C[3], and its image is exactly the +1 eigenspace of tau on J_X[3].
Thus the +1 eigenspace has dimension 32 over F3 and the -1 eigenspace
has dimension 80-32=48. Equivalently, the Prym has dimension 24.
The torsion sizes used here follow from
[Stacks, Proposition 39.9.11](https://stacks.math.columbia.edu/tag/0BF9).

For Delta=D+−D−, the nonempty set

    S = { A : 3A=-Delta, tau(A)=-A }

is a torsor under this anti-invariant 3-torsion. Indeed differences
of two solutions satisfy both homogeneous equations, and adding any
such torsion point preserves both equations. Therefore the geometric
set S has

    3^48 = 79,766,443,076,872,509,863,361

members. This is a theoretical geometric count, not an enumeration,
the degree of the chosen coefficient field, or a count of rational
solutions over F31. D84 proved at least nine Frobenius-fixed solutions
and distinguished the current one by two point counts. That remains
useful local evidence; it does not determine the global orbit in S.

Multiplication by three is finite étale at 31. Each selected special
fibre solution has a unique formal lift. Thus successful lifting alone
cannot select the arithmetic solution, nor can it prove its field of
definition. The branch-class division is an algebraic finite problem;
the concern is the degree and height of its particular solution, not
that arbitrary transcendental coefficients have been introduced.

Script 296 supplies a small exact counterexample to the incorrect
local-to-global inference: x^2−5 has a simple root 6 modulo 31, which
it lifts and checks through 31^128, while 5 is not a square in
F=Q(zeta_32)^+. The latter is checked in the exact number field; also
Q(sqrt(5)) ramifies at 5 whereas the cyclotomic field ramifies only
at 2. Arbitrarily accurate coefficients in Q_31 can therefore lie
outside F. This is an illustrative counterexample, not a proposed
coefficient field for our cubic.

## 3. What the present normalization guarantees

The normalization uses a unique effective representative with fixed
part H=K_X+2P, followed by one-dimensional function spaces. The fixed
divisors and ambient section bases are rational. Unit-minor linear
algebra selects the same lines under extension of the coefficient
field. Random search sections only provide a way to compute that
unique result; they do not supply an additional algebraic parameter.

For the final scalar, let r^2=-3 and let a0,h0 be the leading
coefficients at the rational uniformizer w. The verified identities are

    -h0^2=a0^3,    lambda=r*a0/h0,
    lambda^2*a0=3, lambda^3*h0=3r.

Consequently no square-root or cube-root extraction is introduced by
this last scaling. The root r already encodes the orientation of D+
and D−. The equations and one-dimensional spaces in scripts 249/251
make this a field-preservation statement **relative to the selected
oriented class**. They provide no upper bound for its coefficient height.

A concrete sufficient global condition is now visible. Put
epsilon_sigma=sigma(r)/r. Since sigma(Delta)=epsilon_sigma*Delta,
Galois acts on S by A -> epsilon_sigma*sigma(A). To make the
normalized cubic F-defined it is sufficient to establish, for every
sigma fixing F,

    sigma(A)=epsilon_sigma*A.

If epsilon=+1, the unique representative and normalized functions are
preserved. If epsilon=-1, tau(A)=-A exchanges the representative with
its tau-image. The leading h coefficient changes sign under tau,
and r changes sign too, so the same normalization carries h to tau(h).
The norm coefficient a and the trace h+tau(h), hence A2 and R4, are
then fixed. This deduction is conditional: **that global Galois condition
has not been checked for the candidate**. At 31 the oriented branch
splits and the saved Frobenius condition tests only the local action.

We found no reason to replace the K_X+2P normalization on field grounds.
A poor height remains possible. The small coefficients of the ambient
25-dimensional A2 basis are not a height bound on the selected point.

## 4. Descent obstruction versus field of moduli

[Sijsling–Voight, Theorem 1.3.2 and Theorem 3.2.4](https://jvoight.github.io/articles/birch-descent-021420.pdf)
descend a map marked by a smooth source point to its field of moduli.
They do not identify that field with F or Q. In particular, having a
smooth marked point over Q_31 supplies no missing global comparison.

For this cover there is an additional simplification. Let Z -> C be
its geometric S3 closure and Y=Z/H, with H a reflection subgroup.
The automorphisms of Y over the fixed base C are N_S3(H)/H: in the
function-field closure an automorphism of the intermediate extension
is exactly an element normalizing H, modulo H. Here N_S3(H)=H, so

    Aut_C(Y)=1.

Script 296 independently checks the normalizer and the three conjugate
reflection subgroups in S3. If each conjugate of Y -> C is isomorphic
to it over the given F-model of C, these isomorphisms are unique.
Their composites therefore satisfy the Weil cocycle automatically,
giving descent over F. There is no further automorphism cocycle to
solve **once that field-of-moduli assertion over the fixed base is
proved**. The statement does not concern all automorphisms of Y as
an unmarked curve.

The canonical arithmetic reflection cover is a useful comparison
object. Its local division-level kernel is intrinsic, and all S3
reflection subgroups are conjugate. This gives a possible extension
of D58's conjugation argument from the maximal-level cover to the
reflection cover. Completing that extension requires compatible
canonical conjugation of the level and component, followed by an
identification with our explicit base and class. The elementary
S3 check proves neither requirement. A Q-descent of the cubic is
therefore not being asserted here.

## 5. Arithmetic identification remains the deciding gate

The exact candidate C, rational double cover X, selected special-fibre
third, and finite-precision cubic each have explicit certificates.
The canonical genus-64 Shimura curve has a separately specified
quaternionic S3 monodromy map. What is missing is a comparison tying
these objects together, including the base marking and global twist.

D84's two point counts distinguish the current cover among the tested
nine. They are two traces at one prime, not the full Euler factor,
an exhaustive third census, or a generator-by-generator comparison
with script 66's monodromy.

The earlier discrepancy also remains material:
[Dembélé, Theorem 5.9](https://arxiv.org/pdf/1906.06772) asserts
hyperellipticity of the arithmetic genus-16 quotient, whereas the exact
candidate and D45/D62's independently computed stable-graph obstruction
give nonhyperellipticity. D62 found no level or component mismatch that
resolves this. Lemma 5.2, used for D58's earlier descent, precedes that
claim and does not rely on it. The new review does not settle this
published conflict or promote an analytic match to an exact identification.

## 6. Decision and next deliverable

Pause precision escalation and retain the 64-digit model and the
selected third. The next substantive deliverable is a **marked arithmetic
comparison**: specify the conjugation/level compatibility on the canonical
cover and a verifiable map between its cycle marking and the divisor
class on the explicit X. An alternate route is direct evidence for the
global condition sigma(A)=epsilon_sigma*A, with its field of definition
proved. Merely retrying the same reconstruction, or searching an arbitrary
larger coefficient field, does not supply either comparison.

A practical first step is to extract exactly what the saved Fuchsian
and analytic data can certify about the base/branch marking and where
an additional certified continuation or period comparison is required.
Keep D62's hyperellipticity conflict in that audit. Do not begin target
torsion computations from a cover whose arithmetic identity is unproved.

If precision work is resumed for a stated reason, the retained 128-digit
sections and jets need not be recomputed. The actual-divisor stage must
be split at a mathematically checkable checkpoint or replaced by a less
expensive solve; simply extending the timeout or increasing memory is
outside the retained resource policy. This is a possible later engineering
task, not a completed 128-digit lift or the default next step.

The path to the field remains: identify the arithmetic cover, obtain
its exact equation, compute the specified residual 2-torsion carrier,
then recover and certify the degree-257 polynomial over F and its normal
closure over Q. This review advances the identification requirements;
it does not construct the target field.

## 7. Artifacts and verification

The combined root is
[cm_frame_cubic_128_attempt_review.json](../data/computed/cm_frame_cubic_128_attempt_review.json).
The exact small review checks are
[cm_frame_descent_review.json](../data/computed/cm_frame_descent_review.json).
All failed construction and control attempts are included in the audit
with their status; the D84/D83/D78 roots remain unchanged.

```sh
python3 dembele/pari/297_cm_frame_cubic_128_review_audit.py --check
python3 dembele/pari/296_cm_frame_descent_review.py
```

These commands verify retained records and hashes without repeating
the failed construction. Decisions, references and entry points are
updated for this outcome. No job remains active.
