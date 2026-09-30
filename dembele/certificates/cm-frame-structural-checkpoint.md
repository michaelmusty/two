# D84: cover ambiguity and recognition calibration

Date: 2026-09-22. The user paused the automatic precision doubling to
investigate (1) the choice of third and (2) the useful precision of the
recognition algorithm. Both investigations are complete for this checkpoint.

**Results:** there are at least nine compatible thirds on the candidate
genus-40 curve over F31. All nine give independently checked genus-64
covers. The current third is the only one in this subgroup whose first
two point counts agree with the Hecke prediction. Separately, 67 synthetic
recognition tests show a consistent increase in the recoverable example
height from 10^9 at 64 digits to 10^18 at 128 digits. These are empirical
examples, not uniform recovery guarantees or bounds on the target's height.

The actual curve remains verified through **31^64**. No 128-digit curve
lift, exact number-field cubic, arithmetic identification or target field
has been constructed in D84.

## 1. An actual subgroup of compatible thirds

Let A be the D78 class, Delta=D+−D−, and tau the double-cover involution.
If T is fixed by F31-Frobenius, satisfies 3T=0 and tau(T)=−T, then

\[
3(A+T)=-\Delta,\qquad \tau(A+T)=-(A+T).
\]

Conversely, the difference of two compatible thirds satisfies these
conditions. Thus the ambiguity is the rational anti-invariant 3-torsion.
This is an elementary group calculation. The associated Kummer-cover
interpretation is supported by
[Stacks, Kummer theory](https://stacks.math.columbia.edu/tag/03PK).

Scripts 276/277 form actual Frobenius-stable degree-120 divisors from the
saved evaluation points. A class B−tau(B) is anti-invariant. Multiplication
by the same prime-to-three cofactor suggested in D78 supplies trial torsion
points. The cofactor is only a search aid: every accepted point is checked
directly for nonzeroness, order three, Frobenius invariance and its tau
action. No Jacobian or Prym order is assumed.

Seeds 0 and 2 give two independent points T1,T2. Script 278, using a
different arithmetic seed, independently verifies their orders and
symmetries, checks the distinctness of all nine combinations, and verifies
the class relation and symmetries for every A+i*T1+j*T2. Replacing a
proposed torsion point by T+Delta is rejected at the tripling relation.
The witnesses are in
[cm_frame_third_ambiguity_0_2.json](../data/computed/cm_frame_third_ambiguity_0_2.json).

This proves a subgroup isomorphic to (Z/3)^2 and **at least nine**
compatible thirds. It is not an exhaustive determination of the rational
3-torsion. The predicted Prym order has 3-adic valuation two, so if that
order were independently established these nine would exhaust the
compatible thirds. This conditional observation is not used in acceptance.

One unsuccessful search, seed 1, stopped when its randomly selected
Frobenius-stable support failed to reach degree 120. Its failed log and
job record are retained. It produced no accepted class. Successful
searches take 51.4 and 53.6 seconds; the independent nine-third check
takes 30.0 seconds and its corruption control 3.3 seconds.

## 2. Constructing and distinguishing the nine covers

Runner 279 specializes the frozen D79/D80 constructors and independent
verifiers at the new third and cubic input filenames. It preserves the
original sources and saves their hashes and generated copies. An immutable
snapshot records the executed orchestration source. Each cover has the
full function/divisor/norm and coefficient verification, not only a fitted
polynomial with the right branching degrees.

Point counting reuses D80's complete, independently certified lists of
50 base points over F31 and 1,400 over F31^2. Every point is rechecked on
the base curve. The constructor counts normalized cubic fibres, and the
independent verifier uses quadratic splitting and Kummer units with
different local parameters. Reusing the base lists avoids repeating
enumeration; it does not assume any upstairs count.

| Third A+i*T1+j*T2 | Points over F31 | Points over F31^2 | Both Hecke predictions |
| --- | ---: | ---: | --- |
| (0,0), current third | **68** | **2818** | **Match** |
| (1,0) | 59 | 1495 | Fail |
| (2,0) | 50 | 1540 | Fail |
| (0,1) | 59 | 1543 | Fail |
| (1,1) | 44 | 1504 | Fail |
| (2,1) | 38 | 1474 | Fail |
| (0,2) | 59 | 1525 | Fail |
| (1,2) | 38 | 1456 | Fail |
| (2,2) | 53 | 1567 | Fail |

The current class is reconstructed in this comparison as a control and
recovers D80's counts. Every alternative fails each comparison separately.
All nine constructions, nine independent cover checks, eighteen point
counts and eighteen independent fibre checks pass. Each of these jobs
takes less than eight seconds with the cached base point lists.

This strengthens the case for the selected third within the tested
subgroup. It neither proves that the subgroup is complete nor identifies
the characteristic-zero curve with the canonical Shimura curve.

### What remains of the monodromy comparison

The saved arithmetic map in script 66 and `genus64_cosets.gp` specifies
the intended S3 permutations on the quaternionic presentation generators.
All nine covers have the same branch inertia types. An unramified
3-torsion modification on X preserves the branch valuations modulo three;
branch multiplicities therefore cannot distinguish these choices.

We do not yet have a comparison taking the arithmetic divisor classes on
the explicit X to the cycle marking in that quaternionic presentation.
Consequently D84 does not claim a direct generator-by-generator Fuchsian
monodromy match. The new comparison uses the Hecke predictions instead.
The base/marking identification and earlier hyperellipticity discrepancy
also remain open.

Multiplication by three is
[étale in characteristic 31](https://stacks.math.columbia.edu/tag/0BFH),
and [étale sections lift uniquely across nilpotent thickenings](https://stacks.math.columbia.edu/tag/06NE).
This explains why an alternative third can also lift successfully.
Increasing precision does not resolve the initial choice by itself.

## 3. Empirical recognition thresholds

Script 275 uses the same rank-200 lattice and 24 congruence conditions
as frozen script 259: 25 homogeneous coordinates in the degree-eight
power basis of F, one common F-valued projective scale, and LLL basis-row
search. Synthetic integral F-coordinates have prescribed maximum height
H, coefficients drawn in [−H,H], and integer content one. An arbitrary
common 31-adic unit scales their evaluated coordinates before recognition.

Inputs come from exact known F-points; increasing their synthetic
precision is cheap and **does not lift the candidate curve**. The
reconstruction receives only the training digits. Every survivor must
match all unused digits and the exact known projective F-point. Changing
the first unused digit in one coordinate is rejected. Source, input,
output and timeout receipts are retained for each campaign.

| Synthetic precision | Training / validation | Example height recovered in all three seeds | Next tested height failing in all three seeds |
| --- | --- | ---: | ---: |
| 31^64 | 48 / 16 | 10^7 | 10^8 |
| 31^64 | 60 / 4 | 10^9 | 10^10 |
| 31^128 | 112 / 16 | 10^18 | 10^19 |

These three-seed comparisons use the root 4 modulo 31. Additional boundary
tests at root 20 give the same outcomes for 60/4 and 112/16. The full
campaign includes 67 cases in twelve bounded jobs: 34 recover the known
point exactly and 33 return no surviving basis row. Larger failure cases
up to height 10^22 and smaller positive cases are retained. The longest
job takes 111.3 seconds, below the 180-second limit.

Script 280 checks the saved positive recoveries again using plain Python
integer multiplication modulo the defining polynomial of F. It verifies
the exact projective identities, all held-out digits, the input heights,
common scales and rejection of the changed digit, independently of Sage's
number-field implementation.

These observations do not prove a universal threshold, determine the
target's coefficient height, or exclude a smaller target vector missed
by the basis-row search. The coordinates are in the fixed bases, not
intrinsic Weil heights. D83's separate rigorous low-height exclusion
through 1,301,123 remains unchanged; it is not replaced by these empirical
figures.

## 4. Decision and next experiment

These checks give a better reason to try 128 digits than repeated lifting
alone: the selected cover is distinguished among nine actual alternatives,
and the tested reconstruction method gains about nine orders of magnitude
in recoverable example height at 112 training digits.

**Recommendation:** one bounded actual 128-digit experiment in the same
K_X+2P normalization and exact A2 basis, reserving sixteen validation
digits. Any recovered equation must pass exact function/divisor identities
over its proposed field. If reconstruction remains negative, revisit the
coefficient-field, descent and identification assumptions before another
precision doubling. No height bound guarantees that 128 will suffice.

The user authorized this structural/calibration checkpoint; the actual
128-digit lift has not been run. The existing 64-digit arithmetic inputs,
normalization and all D68–D83 certificates remain unchanged.

## 5. Artifacts and reproduction

The combined root is
[cm_frame_structural_checkpoint.json](../data/computed/cm_frame_structural_checkpoint.json).
Script 281 verifies **1,666 distinct file hashes and 593 linked JSON
records**, including the frozen D83 root and D78 hash. All jobs have
finished. No remote jobs, external edits/messages, commits or cleanup.

```sh
# Read-only verification of the complete checkpoint and prior provenance:
python3 dembele/pari/281_cm_frame_structural_checkpoint.py --check
# Existing immutable results are verified without overwriting them:
python3 dembele/pari/278_cm_frame_third_ambiguity.py --seeds 0 2
python3 dembele/pari/279_cm_frame_alternative_covers.py --case 1
python3 dembele/pari/275_cm_frame_recognition_calibration.py --digits 64 --train 60 --seed 0
```

Fresh calibration campaigns use the process-group timeout runner 272.
The actual lift remains packaged in `cm_frame_cubic_adjoint_package_64.json`.
