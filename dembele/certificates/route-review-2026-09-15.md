# Strategic review: from the current computations to Dembélé's field

Date: 2026-09-15. Decision D50. This review responds to the request to step
back and validate the approach. It supersedes D49's automatic next step of
increasing the genus-16 truncation; it does not invalidate that computation.

**Assessment:** retain the curve/Jacobian route as the strongest concrete
candidate identified in this project, but change the next milestones. We
have made the analytic machinery work and identified a specific geometric
carrier. We have not demonstrated an end-to-end practical construction of
the field. Further solver precision alone does not resolve the largest
remaining uncertainties.

No exact curve equations, arithmetic evaluation model, target torsion
points, or field polynomial were produced in this review. No new large or
remote job was launched. The alternative-route assessment below is bounded
by the project audits and the primary literature checked here, not an
exhaustive impossibility theorem or a proof of optimality.

## 1. What the route actually requires

The objective remains the original residual kernel over
`F = Q(zeta_32)^+`, followed by its normal closure over Q. Matching the group,
ramification set, or a handful of Frobenius traces would not establish this
identity. The relevant chain is:

    original mod-2 Hecke system
      -> rank-48 sign-type automorphic lattice
      -> the 48-dimensional new abelian factor of J(Y), g(Y)=64
      -> an actual Galois-stable 16-dimensional F2 space in J(Y)[2]
      -> a faithful degree-257 projective polynomial over F
      -> the required normal closure over Q.

The sign-type lattice has rank 48 as a space of automorphic forms. The new
abelian factor has dimension 48 and hence 96-dimensional geometric
2-torsion. The desired constituent has dimension 16 over F2, or two over
F256. These are different dimensions of different objects.

| Required step | Present evidence | Remaining issue |
|---|---|---|
| Original system occurs at the new level | Script 63's exact rank-48 supported lattice, all-Hecke reduction argument, and coprime quotient test | Finish the local-type and geometric identification with precise conventions |
| A suitable geometric carrier exists | Explicit local S3 map; degree-three cover Y of C; genus 64 checked by signature and lifted homology | The exact arithmetic subgroup is specified; equations and arithmetic section data are absent |
| Effective analytic sections | Sixteen differentials on C, numerical canonical relations, working compiled residual refinement | These are sections on the genus-16 base, not the 48 new directions on Y |
| Arithmetic input for Jacobian calculations | CM normalization removes a basis choice and common scale | Its coefficient field, exact recognition and a model of Y remain unestablished |
| Extract the target torsion | General algorithms exist; conditional Euler-factor isolation check passes at norm 31 | No implementation or measured torsion calculation on Y; norm-97 cofactor test remains open |
| Obtain and certify a polynomial | A degree-257 projective invariant would retain the kernel | No evaluated invariant, coefficient-height measurement, recognition or certification |

The local evidence is in [the D42 review](review-2026-09-14.md),
[the cover calculation](genus64-cover.md), and
[the D49 solver report](compiled-precision-refinement.md).

## 2. Why the latest numerical success is a limited milestone

At N=8192 the compiled solver reaches a finite-system residual of about
`1.54e-41`, but the independent side residual is about `1.42e-9` and the
changed/larger quadrature defect is about `5.86e-12`. These are empirical
diagnostics. They are not rigorous bounds on the differential coefficients.
The geometry itself was originally computed at roughly 57 decimal digits.

Thus D49 successfully separates roundoff from discretization. It does not
give forty correct digits of the curve, establish an arithmetic coordinate
system, or make the target cover algebraic. The N=12288 native run is a
reasonable bounded convergence experiment when tied to a concrete
recognition test. It should cease to be the default project milestone.

Voight–Willis support the power-series route for compact arithmetic
Fuchsian groups and motivate CM period normalization. Their general
algebraicity statements do not, by themselves, identify our normalized
coordinates with F; their numerical reconstruction method also leaves
rigorous numerical error control open. In particular, the hypotheses and
normalization must be adapted to our elliptic CM center, where the upstairs
differentials vanish. Reality of the computed ratios is insufficient.
[Voight–Willis, §2–3](https://arxiv.org/pdf/1205.0045).

The failed small-height searches tested six coefficients within tiny
specified bounds. They establish neither a prohibitive height nor failure
of the method. Before broadening them substantially, determine the CM
field and Galois action on the normalized jets, or exhibit a different
arithmetic normalization with a justified field of definition. A model
over a controlled extension with explicit descent would also be useful.

## 3. Two useful structural deductions

### The degree-three map splits old and new 2-torsion

Let `pi: Y -> C` be the proposed map over F. Norm and pullback on Jacobians
satisfy `Nm_pi pi^* = [3]`. Consequently, on geometric 2-torsion,

    e_old = pi^* Nm_pi,
    e_old^2 = e_old,
    e_new = 1 - e_old,
    J(Y)[2] = pi^* J(C)[2] direct-sum ker(Nm_pi | J(Y)[2]).

This follows since multiplication by three is the identity on 2-torsion.
Both summands are Galois-stable when the map is defined over F. Their F2
dimensions are 32 and 96. This is a deduction from the odd-degree map;
it does not identify the target inside the second summand or supply
efficient arithmetic on a stand-alone 48-dimensional abelian variety.

In particular, the genus-16 base is useful for calibration and arithmetic
coordinates, but its own torsion is not the original target. Computing it
alone cannot complete this route.

### The existing domain can address Y directly

The three-sheet permutation representation is `1 + Std`, with Std the
two-dimensional standard representation of S3. Over Q, the projectors are
`P_old = (1/3) J_3` and `P_new = I_3 - P_old`, where J_3 is the all-ones
matrix. They also make sense integrally at 2. The standard component
accounts for `64 - 16 = 48` holomorphic differential directions on Y.

At the order-32 elliptic center the local image is a transposition. In an
eigenbasis of Std, a differential `f(w) dw` satisfies

    f(zeta_32 w) zeta_32 = s f(w),

so its two components have powers `w^(31+32n)` and `w^(15+32n)` respectively.
The second sparse sector is essential. This is a concrete way to extend
the current parent-domain calculation to the new part, without first
finishing all 91 exact quadrics of C or constructing a new Dirichlet domain.
It was already suggested in D43; the current scalar pipeline has not
implemented it.

Exact small-matrix checks in this review verified both projectors, their
commutation with all six permutations, their mod-2 idempotence and the two
CM exponent residues. These checks validate the representation arithmetic,
not a vector-valued analytic solver. A doubled coefficient space may still
be expensive with the current dense LU. A bounded pilot must measure this.

## 4. Make the representation comparison precise before major expansion

The sign-type congruence is stronger than matching several eigenvalues.
Reduction of sign-valued integral functions on the 48 admissible ideal
classes gives an all-Hecke map into the original level-one module. The
ten-dimensional quotient has T31 polynomial `t^10`, excluding either
original degree-eight constituent. This is substantial evidence in favor
of the route.

The next proof should specify the central character and level, identify
the depth-zero GL2 type with the standard division-algebra type under
Jacquet–Langlands, and identify the corresponding characteristic-zero
factor of J(Y). Then use the residual Hecke ideals and the known original
system to identify its residual representation.

One possible economical proof uses characteristic-zero transfer,
lattice-independence of residual semisimplification, and an integral
Hecke projector isolating a single 16-dimensional F2 constituent. This
must include the projector's dimension and the target's irreducibility;
a constituent of a semisimplification is not automatically the actual
Galois-stable subspace required by the torsion algorithm. A coprime
polynomial in one local Frobenius does not by itself prove global Galois
stability. Algebraic Hecke correspondences can supply the needed global
stability once their factor is identified.

This is a proof outline, not a completed integral comparison. It may avoid
an unnecessary full integral homology computation. It also explains why
establishing original-field identity should be an early gate rather than
a check deferred until after coefficient recognition.

## 5. Test the torsion end of the route sooner

Mascot's method starts with arithmetic curve/divisor data and an identified
Galois subspace, with a suitable Frobenius polynomial separating it. It
extends to number fields and finite coefficient fields. Evaluation and
coefficient recognition still need a globally defined function and final
certification. Its full lifting algorithm is not merely cubic in the
genus, even though individual Jacobian operations use linear algebra of
size proportional to the genus.
[Mascot, Hensel lifting, §1 and §2–6](https://arxiv.org/pdf/1808.03939).

The later modular implementation reports an example of genus 22 over an
unramified extension of degree four, taking just under eleven hours on
84 cores at precision `191^2048`. This is relevant evidence that the
backend works beyond small genus; it is not a timing prediction for our
genus-64, characteristic-two representation. The same paper gives explicit
Makdisi input requirements and examples where the evaluation function
substantially changes the necessary precision.
[Mascot, moduli-friendly Eisenstein series, §2.1 and §8.1](https://arxiv.org/pdf/2004.14683).

For us, a recorded prime above 97 has target Frobenius order 51. There are
65,535 nonzero vectors, 257 projective lines and 1,285 vector Frobenius
orbits. Its projective orbit lengths are
`1, 1, 51, 51, 51, 51, 51`: the matrix is split with eigenvalues of order
51, so it fixes its two eigenlines and acts with order 51 on the other
255. The cycle count was checked exactly in this review. Seven line
orbits do not mean seven cheap Jacobian evaluations; the proposed line
invariant sums over 255 vectors, and an efficient shortcut is not known here.

Norm 97 is a candidate, not a selected production prime. Its full Euler
cofactor test is unfinished; the corresponding conditional test at norm
31 passes. A bounded prime search should balance extension degree,
isolation and actual arithmetic cost. Recovering F256 scalars from
`Frob + Frob^(-1)` helps after isolation, but does not replace a globally
defined evaluation function.

The appropriate early benchmark is an actual Makdisi arithmetic and
torsion-lifting control on an explicit curve, followed by a representative
genus/extension-degree test. A dense finite-field matrix benchmark alone
does not validate this pipeline. Before full torsion enumeration, measure
one lift, several evaluations, collision behavior and observed invariant
heights. Avoid importing the old period invariant's height estimate as a
bound for every possible generator of the target field.

## 6. Alternatives and the published geometric conflict

| Alternative | Present assessment |
|---|---|
| Genus-16/level-p F16 branch | Its residual field is the solvable Harbater field. It is a control or geometric base, not a substitute for the original target. |
| Return to the tested auxiliary-prime toric period pipeline | Its measured carrier and invariant-height problems remain. They do not exclude other primes, models or invariants, but no concrete improvement was identified here. |
| Direct use of the level-one abelian variety, or descent to Q | Smaller characteristic-zero dimension is attractive, but we have no effective model or Jacobian realization. The audited descent argument also has an unresolved Schur-index alternative. |
| Equationless Jacobian arithmetic | Potentially valuable if arithmetic section evaluation becomes available for this quaternionic curve. The recent modular results rely on additional moduli input that we have not supplied. |
| Direct polynomial search or a different inverse-Galois construction | No bounded search space or specific construction identifying the original residual kernel has emerged in this review. |

The August 2026 equationless quadratic Chabauty paper explicitly uses
elliptic curves with Cartan level structures. It does not supply an
immediate replacement for our quaternionic arithmetic input. That last
statement is a scope comparison, not a theorem ruling out adaptation.
[Hashimoto–Lido–Lombardo–Mascot–Parent](https://arxiv.org/abs/2608.10919).

The hyperellipticity discrepancy remains significant. The local D45/D46
graph calculations give an exact obstruction for the identified reduction
graph, reinforced by independent numerical differential calculations.
Nevertheless the latest Qiu version inspected here still invokes
Dembélé's hyperellipticity theorem; it supplies a citation to that theorem,
not a new independent proof.
[Qiu v2, §8, Theorem 8.1](https://arxiv.org/html/2509.06175v2#S8).

Preserve the distinction between verifying a finite graph and verifying
that it is the correct stable reduction of the specified canonical curve.
A targeted independent audit of that arithmetic identification remains
worthwhile. Repeating graph-automorphism enumeration alone will not resolve
the published conflict. General section reconstruction can proceed without
assuming hyperellipticity. The separate Harbater-field identification is
not reopened by the geometric discrepancy; see the discussion of
Dembélé's separate residual argument in the D42 review.
[Dembélé, 2020, §5–6](https://msp.org/ant/2020/14-10/ant-v14-n10-p05-p.pdf).

## 7. Revised next milestones and stopping criteria

1. **Close the arithmetic target comparison.** Write the local-type/JL
   argument and isolate an actual irreducible residual subspace using
   integral Hecke action. Success means a precise proposition connecting
   the specified Y to the original residual kernel, with every remaining
   hypothesis explicit. A few more matching traces do not pass this gate.
2. **Run a bounded pilot on Y and settle arithmetic normalization.** Use
   the standard S3 component on the existing domain. Check the predicted
   48 directions, both CM sectors, independent side transformations and
   cross-truncation behavior. In the accompanying mathematical work,
   justify a coefficient field and recognition procedure. C remains a
   useful calibration; an unrecognized numerical model of C is not the
   final objective of this gate. A single recognized coefficient would
   validate one recognition step, not certify a whole curve or cover.
3. **Establish a credible torsion implementation and cost.** Inventory the
   required Makdisi input, run an explicit-curve control, complete the
   candidate-prime isolation checks, and benchmark representative
   arithmetic. This preliminary work need not wait for exact equations of
   Y; actual target torsion necessarily does.

Do not keep increasing N when the unresolved question is the coefficient
field or the algebraic cover. If the vector-valued pilot fails to converge,
measure whether multiple centers or structured linear algebra addresses
that failure before allocating larger dense systems. If torsion costs or
invariant heights are prohibitive, revisit the model, prime or invariant
before committing to full enumeration. If the target comparison fails,
stop work on this carrier as a route to the original field.

The next meaningful success is a proved representation bridge and usable
arithmetic data for the target carrier, with a measured torsion plan. More
digits on C are supporting work toward those goals.
