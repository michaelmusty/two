# Construction methodology review (D100)

Date: 2026-09-24. Requested strategic review. This records the proof
dependencies and a proposed order of work; it supplies no new arithmetic
computation or identification certificate. Earlier bound artifacts are
unchanged.

**Assessment:** retain the Shimura-curve/Jacobian route as the route with
the most concrete progress. It has a proved abstract carrier for the
right representations and substantial exact candidate geometry. It does
not yet have an identified global curve on which the required torsion
can be computed. Arithmetic identification, global cubic construction,
and target-scale torsion are separate unfinished tasks. Improving the
current analytic estimate would address only part of the first task.

## 1. Work backwards from the field

Let F=Q(zeta_32)^+. The target is the field K in
[Dembélé's original construction](https://arxiv.org/pdf/0811.4379),
with two residual representations

    rho_1, rho_2 : G_F -> SL_2(F_256),
    E_i = fixed field of ker(rho_i),
    K = E_1 E_2.

Its group over F is SL_2(F_256)^2 and its quotient over Q is C_8.
The normal closure over Q of either original E_i gives K. The objective
is to recover one of these kernels, not just a field with the same
group, ramification set, or several matching Frobenius traces.

A natural first output is a degree-257 polynomial over F, encoding the
action on P^1(F_256). This action is faithful because SL_2(F_256) has
trivial center. A separating, Galois-equivariant invariant of the 257
lines therefore has splitting field E_i over F. Then take the normal
closure over Q, keeping the base field explicit. A coefficient norm
produces a polynomial of degree 2056 over Q; when using it, also verify
that its splitting field contains F, or include F's defining polynomial.
No descent of the degree-257 polynomial to Q is required.

The existence theorem does not depend on hyperellipticity. The
[D99 review](hyperellipticity-review-d99.md) establishes that the
intended genus-16 quotient is geometrically nonhyperelliptic. This
settles the model type and excludes a hyperelliptic reconstruction
ansatz; it does not identify our candidate or remove a torsion carrier.

## 2. The proved arithmetic route and the candidate route

For the specified quaternionic levels, write C_ar for the genus-16
positive-normalizer quotient, X_ar for its genus-40 quadratic cover,
Z_ar for the genus-136 full local-level cover, and Y_ar for the genus-64
reflection quotient. The maps have degrees

    Z_ar --3--> X_ar --2--> C_ar
      |                       ^
      2                       3
      |                       |
      +--------> Y_ar --------+

The local quotient is S_3; X_ar is the quadratic resolvent of the
degree-three cover Y_ar -> C_ar. These levels specify the arithmetic
curves, not merely their genera and branching.

[D51](target-realization.md) identifies two actual Galois-stable
16-dimensional F_2 subspaces of J(Y_ar)[2], each two-dimensional over
F_256, with the original residual systems. Its integral congruence
commutes with every relevant Hecke operator, so the conclusion is about
the original kernels. The new characteristic-zero factor has dimension
48. The genus-16 base alone does not carry the desired constituents.

What we have constructed is a separate candidate route:

| Object | Established | Still required |
| --- | --- | --- |
| C_candidate | Exact smooth canonical genus-16 curve over Q, defined by 91 quadrics; independently nonhyperelliptic | An identification with C_ar over F, with the correct arithmetic frame and CM labels |
| X_candidate -> C_candidate | Exact genus-40 double cover, exact candidate markings and twist choice; extensive numerical character comparison | Identification of the marked arithmetic cover, including the branch labels and the double-cover character |
| Y_candidate -> C_candidate | Exact normalized special fibre at 31; compatible cubic data verified modulo 31^128 | Exact global coefficients and identification with Y_ar |
| Torsion backend | End-to-end small controls, genus-64 control at residue degree 2, and genus-16 control at degree 51 | Genus-64 arithmetic at the required extension degree and precision, with the actual target subspace and evaluation map |

The [D69 candidate certificate](cm-frame-verification.md),
[D87 character comparison](cm-frame-double-cover-character.md), and
[D86 cubic lift](cm-frame-cubic-128-chatelet.md) certify different
statements. They cannot be combined into a global arithmetic
identification without an additional argument. In particular,
agreement of branch support does not determine a double cover, and
agreement at a finite collection of primes does not identify arbitrary
global curves or representations.

## 3. First proof objective: an independent arithmetic comparison

The most concrete sufficient certificate remains the
[D88 CM-expansion criterion](d88-cm-expansion-identification-review.md).
In its current Q-formulation, assume the intended Q-descent, a correctly
labelled degree-17 CM point D, and the saved canonical coordinates
identified with a Q-basis up to a common nonzero scalar. Compute local
expansions independently on C_ar, not from the candidate equations.

For our field objective an identification over F already suffices.
The same divisor argument works over F once D is independently
identified as a degree-17 closed point over F and the frame as an
F-basis. Thus proving a Q-descent need not be a separate prerequisite
of a revised implementation. This is our base-field reformulation of
the criterion; it does not supply the missing frame or CM expansions.

Each candidate quadric is a section of 2K_C, of degree 60. If its
restriction to 4D is zero, its vanishing divisor has degree at least
68, so it is identically zero. Checking all 91 quadrics then identifies
the canonical image with the exact candidate and proves an isomorphism.
Thus four coarse local coefficients suffice. Three suffice if the
independent 51-by-136 quadratic restriction matrix has rank 45 and its
kernel is exactly our 91-dimensional space of quadrics. The candidate
passes this rank test, but that does not compute the arithmetic matrix.

This is an application of the homogeneous-relation bound in
[van Bommel–Costa–Poonen–Srinivasan](https://arxiv.org/pdf/2506.14026),
not an algorithm from that paper for finding Shimura-side expansions.
At the order-two CM point the coarse coordinate is locally u=z^2.
Three coarse differential coefficients involve upstairs powers z,
z^3, z^5; first-order upstairs data do not suffice. Ratios of
differentials remove a common period, but still require independently
evaluated global sections and the correct arithmetic frame. See the
[D89 local analysis](cm-tangent-local-arithmetic-d89.md).

Identifying (C_ar,D) does not automatically identify P32, B3, or the
genus-40 double cover. Those are further parts of this proof objective.
The numerical comparison of 277 side-generator signs is useful
evidence, but is not yet the required rigorous arithmetic comparison.

The present analytic branch has a more limited status:

- D95 identifies the implemented global kernel with the intended
  automorphic pairing, up to a positive common scalar. It does not
  identify the algebraic candidate curve.
- [D98](nelson-spectral-ideal-d98.md) gives a full S11 error bound
  below 24,784,942,340 against a partial sum about 7640.7582. The
  enclosure contains zero, so even the normalization anchor is open.
- A successful nonzero anchor would still need higher derivative
  ratios, all necessary canonical directions, and an exact comparison.
  Small error balls alone do not prove equality with proposed
  algebraic coefficients. One needs an effective separation/height
  bound or an independent exact identity or verification argument.

Consequently, another spectral estimate should be judged by a specified
output: a uniform full-remainder bound giving a nonzero anchor and a
credible extension to the required jets, together with a mechanism for
certifying the eventual algebraic equalities. A further multiplicative
improvement in an unusable error bound is not a curve-identification
certificate. The completed spectral multiplier is a possible next
analytic experiment, not an automatic next construction step.

## 4. Second proof objective: an exact arithmetic genus-64 input

Once the marked arithmetic double cover is identified, the
[D88 cubic shortcut](d88-cubic-identification-shortcut-review.md)
substantially reduces the remaining comparison. Under its hypotheses,
the nine saved rational anti-invariant thirds exhaust the relevant
finite-field family, and the Hecke point count selects the current
cover. Finite-etale lifting on the same fixed global X identifies its
lift with the canonical cover. The orientation and Kummer scalar
conditions matter. The argument is conditional on the marked X
identification and does not identify arbitrary covers by point counts.

That would establish the coefficient field F in the prescribed
normalization. It would not recover the exact coefficients. D86's
31^128 data have no recognized coefficient point in any of the eight
embeddings of F. Its certified exclusion through homogeneous height
348,750,355,384,078 applies to the specified bases. This is neither a
proof that the coefficients lie outside F nor a height bound above
which reconstruction is guaranteed to succeed.

Completion requires either exact equations with their arithmetic
identification, or an exact arithmetic section model sufficient for
Jacobian arithmetic. Recognition can be certified by an effective
bound, or by verifying exact defining identities and a uniqueness
argument; a numerical guess need not be the final proof. A larger
precision run should follow a justified recognition strategy, not
substitute for the missing field or identification argument.

An equation-free implementation has a concrete interface, described in
[D62](arithmetic-section-interface.md): for deg(D0)=129 on Y, section
dimensions are 66, 195, 324, 453, 582, with at least 646 suitable
evaluation points, compatible multiplication, Frobenius, and auxiliary
evaluation data. These entries must arise from the intended arithmetic
Y and lift compatibly. A Hecke module or a reduction graph alone does
not supply them. Equation-free modular-curve methods such as
[Hashimoto–Lido–Lombardo–Mascot–Parent](https://arxiv.org/pdf/2608.10919)
use arithmetic moduli evaluations; they are not an already implemented
source for these quaternionic data.

## 5. Third proof objective: target torsion and a separating invariant

Before a production run, demonstrate the missing combination of genus
64, the required residue extension, and useful precision. The existing
[genus-16/degree-51 control](lifttors-degree51.md) has a known rational
torsion point; it is not a target-representation computation. The
[allocation profile](lifttors-allocation.md) identifies substantial
work left in the backend. The smaller controls do not establish the
time or peak memory of the required combined case.

A prime of norm 97 is attractive because one original residual
Frobenius has order 51. Before using that choice, finish the separation
check against the entire genus-64 Euler cofactor and preserve the
identification of which original constituent is selected. That full
check is already available at norm 31, where the target orders 257
and 255 are more expensive. D51's geometric Hecke projectors prove
existence, but have not become operations on computed divisor classes.
Local Frobenius can implement extraction only with a justified
separation argument; it is not itself a global Hecke correspondence.

The useful benchmark should exercise projection, lifting, Frobenius,
and evaluation on the actual target subspace, eventually obtaining an
F_2 basis and its F_256 scalar structure. A generic Jacobian operation
or a rational branch-point control leaves these requirements open.
If target arithmetic input is not yet available, an honest synthetic
scaling test can still isolate backend cost, but must be labelled as
such. No new large run is prescribed by this review; retain the current
180-second process-group cap and existing resource pauses.

For V of dimension two over F_256, there are 65,535 nonzero vectors
but only 257 lines. A rational function on the Jacobian can be
symmetrized over the 255 nonzero points of each line, and the resulting
line values must be checked for collisions. Choosing a degree-257
output does not by itself reduce the computation to 257 torsion
evaluations. Frobenius orbits and the scalar action are computational
opportunities, not a replacement for separation and equivariance.

Finally recognize the polynomial over F and certify its relation to
the original representation. The p-adic algorithm in
[Mascot](https://arxiv.org/pdf/1808.03939) distinguishes approximation
and coefficient recognition from certification. His
[certification paper](https://www.maths.tcd.ie/~mascotn/research/Certification.pdf)
provides a precedent for a separate arithmetic proof, but its stated
classical, prime-residue-degree-one setting is not a ready certificate
for our Hilbert representation over F with coefficient field F_256.
If our torsion construction is exact and has the D51 identification,
the original ramification and kernel statements follow from that
identification. Otherwise group and ramification checks alone do not
establish that a guessed polynomial is the requested field.

## 6. Alternatives and the next decision

Full curve identification is a sufficient proof architecture, not a
logical necessity. One could instead construct an exact global
candidate Y or polynomial and independently prove that its residual
representation has an original kernel. That could bypass the complete
marked-curve comparison. No such effective arithmetic comparison
criterion has yet been instantiated here; finite trace agreement is
not one by itself.

Working directly with the smaller level-one abelian variety would be
attractive if an effective arithmetic model were available. We do not
currently have one. The higher genus route was chosen because it gives
a specified geometric carrier. Likewise, the desired depth-zero
supercuspidal new part at 2 is not the toric part encoded by the simple
reduction graph. A graph-only period-lattice construction would miss
it; a higher-level uniformization approach would need the additional
component geometry and effective arithmetic sections. These remain
research alternatives, not established replacements.

**Recommended order of work:**

1. Write an executable specification for the first independent
   arithmetic comparison: input, output, precision/error certificate,
   arithmetic frame, and the exact equality mechanism. Use the
   three-coefficient rank test or the four-coefficient divisor bound as
   the final acceptance criterion. If using the analytic route, address
   algebraic exactness as well as the nonzero-anchor estimate.
2. Keep the marked-cover checks explicit, then apply the conditional
   nine-cover shortcut. Produce the exact cubic or equivalent arithmetic
   section data with a verified recognition/construction method.
3. Separately close the Frobenius-isolation and combined scaling tests
   before committing to full target-torsion extraction. Reuse existing
   data before enlarging a Hecke bank or prime search.
4. Compute and certify the degree-257 invariant polynomial over F,
   then its required normal closure over Q.

This ordering identifies where each investment can change the status
of the construction. The immediate research decision is whether we
can supply an effective exact-identification method, analytically or
arithmetically. The review does not resolve that decision or prescribe
another large computation. Hyperellipticity is settled for present
purposes; candidate identification, cubic coefficients, target torsion,
and the defining polynomial remain open.

## 7. Execution readiness: first bounded task

Follow-up, 2026-09-24. The user asked whether more planning is needed
before execution. No further broad strategy review is needed. The
first task is a mathematical feasibility test of exact identification;
it is not yet a production computation of the curve or field.

**First task: establish an exactness mechanism for the independent CM
tangent.** Start with the existing Nelson/Shimizu route because its
independent evaluator is already implemented and identified. Before
another spectral-bound pilot, attempt to supply either an effective
algebraic separation bound for its normalized CM coefficients or an
independent exact identity that verifies the proposed coefficients.
The deliverable must distinguish proved hypotheses from missing ones;
algebraicity or a proposed rational reconstruction is insufficient.

The specification is:

| Item | Required content |
| --- | --- |
| Arithmetic input | The specified C_ar/F and labelled CM point D; a presentation of L=F(D) with [L:F]=17; the arithmetic origin and normalization of the sixteen sections |
| Initial output | The actual projective tangent at D, expressed by the sixteen ratios (d r_j/d r_a)(D) in L, with r_j=omega_j/omega_b and a proved nonzero d r_a(D) |
| Independence | Obtain the arithmetic restrictions from C_ar; use candidate equations and jets only for the subsequent comparison |
| Exactness | Either exact arithmetic operations on a specified model, an effective separation bound applying to the actual unknown coefficients, or an independent exact verification theorem with its hypotheses proved |
| Extension | Explain how the same method reaches three coarse coefficients for the rank-45 test, or four for the divisor-degree test |

For the separation-bound branch, state the coefficient field and basis,
denominator bounds, bounds at the relevant embeddings, the resulting
explicit separation constant, and a finite error tolerance that proves
equality with the proposed value. A bound only on the guessed candidate
does not bound the unknown arithmetic coefficient. Frame certification
and CM-label identification are part of the task, not assumed outputs
of the candidate calculation. An exact arithmetic construction can
avoid numerical recognition and need not supply such a height bound.

There are three distinct outcomes. A usable exactness mechanism and
finite numerical specification justify a bounded evaluator pilot.
An independently certified tangent that disagrees with the candidate
refutes the proposed marked comparison. If an indispensable bound,
arithmetic input, or identity remains unavailable, record the precise
missing statement and assess the arithmetic-restriction alternative;
do not respond by automatically increasing precision or enumeration.
Failure to instantiate one route does not prove that route impossible.

A matching tangent is only an intermediate result. Full base-curve
identification still needs the higher-coefficient test, and the marked
double cover has its own remaining obligations. If the analytic route
advances, certify a nonzero full S11 anchor before taking ratios, with
uniform error bounds for every omitted contribution; the present
enclosure cannot be used for that division.

Keep the existing 180-second per-job process-group cap and resource
pauses. The norm-97 cofactor check and backend scaling remain separate
follow-up tasks; neither substitutes for this arithmetic comparison.
This addendum fixes what execution should attempt and how to judge it.
It does not claim the missing exactness mechanism has been found.
