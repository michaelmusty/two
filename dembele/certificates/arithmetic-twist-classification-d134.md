# D134: an algebraic route from the marked base to its double cover

This note states a conditional mathematical criterion. Execution and
review status are recorded separately in the D134 receipts, fixed review
and completion record; the proposition alone claims no candidate
identification or new harmonic precision.

There are two useful conditional deductions. The existing D77 fibre
certificate already selects the scalar twist after the geometric branch
half and the B3 marking are fixed. Moreover, after identifying the base
and its branch markings, the odd canonical Jacobian order at the saved
norm-31 prime can select the branch half itself. Together these give an
algebraic route to the marked arithmetic double cover, with precise
remaining hypotheses.

## 1. Inputs that remain essential

Let C_sh be the specified genus-16 Shimura quotient over
F=Q(b), with b^8-8b^6+20b^4-16b^2+2=0. The proposition below requires:

1. An arithmetic isomorphism from the exact candidate C to C_sh that
   identifies D17, P32 and B3 with the canonical marked divisors. The
   D88/D116 section argument supplies (C,D17) only after its exact zeros
   are proved; P32 and B3 remain separate marking tasks.
2. The canonical Hecke interpretation at the norm-31 prime b=27. Its
   genus-16 trace polynomial is the saved P16, with Euler polynomial
   t^16 P16(t+31/t). This is an input about the canonical Shimura curve,
   not an inference from the candidate's two matching point counts.
3. The exact candidate double-cover and normalized B3-fibre certificates
   from D76/D77. The canonical S3 level cover has its stated total cubic
   ramification above B3.

The candidate has the certified good model at this prime. Once input 1
is proved, it transfers that good reduction to the identified curve.
Its branch divisor is B2=D17+P32, and both double covers are defined over F.

## 2. Odd Jacobian order selects the F-rational branch half

The recorded Hecke polynomial gives

    P16(32)=1640801490553691915934375,

an odd integer. This was already used as a discovery hint in
[D71](cm-frame-resolvent.md). D71 correctly did not claim it was the
candidate's Jacobian order. With inputs 1 and 2 it becomes the order of
the candidate's Jacobian over the residue field F31, because evaluating
the Euler polynomial at t=1 gives P16(32).

Good reduction and 2 invertible at this prime give an injection

    Jac(C)(F)[2] -> Jac(C)(F31)[2].

For completeness, properness extends a point to the local abelian scheme.
Multiplication by 2 is étale there, so its kernel is finite étale; over
the henselian local ring, two sections with the same reduction agree.
The odd finite group order therefore implies Jac(C)(F)[2]=0.
The fibrewise étaleness statement is
[Stacks, Lemma 39.9.9](https://stacks.math.columbia.edu/tag/0BFH), and the
finite torsion statement is
[Proposition 39.9.11](https://stacks.math.columbia.edu/tag/03RP).
The specialization argument just given is our application to the good
Jacobian model, not a separate candidate point-count theorem.

Write the pushforward of the structure sheaf of each double cover as
O_C direct-sum L^(-1), where L^(-1) is its anti-invariant summand. Let
L_can and L_cand denote the two degree-nine dual line bundles. Each is
defined over F and has square
O_C(B2). Their quotient is an F-rational degree-zero line bundle killed
by 2. Thus L_can is isomorphic to L_cand over F. This argument concerns
the two arithmetic line bundles; it makes no claim that geometric
2-torsion vanishes. With the common line bundle fixed, the two sections
defining the same branch divisor differ by a scalar c in F*. The only
remaining cover ambiguity is a constant quadratic twist.

## 3. D77 already selects that scalar

The [D77 certificate](cm-frame-B3-fiber.md) constructs the exact nonic
residue field K and normalized local unit alpha for the candidate cover,
with an explicit nonzero s satisfying

    alpha=-3 s^2 in K,        [K:Q]=9.

The rational-parameter version is beta=-3 r^2. Consequently the fibre
over K_F=KF is K_F(sqrt(-3)); the coprime degrees 9 and 8 give
[K_F:F]=9. Since F is totally real, this odd-degree extension cannot
already contain sqrt(-3).

For a constant twist c the fibre becomes K_F(sqrt(-3c)), or the split
quadratic algebra when -3c is a square. In the canonical S3 Galois
closure, Z->X is a cyclic Galois cover of degree three defined over F
and totally ramified above B3. At those characteristic-zero points the
residue extension is trivial, and the faithful tame inertia character
forces the residue field to contain a primitive cube root of unity.
This is the characteristic-zero application of
[Stacks, Lemma 15.114.5](https://stacks.math.columbia.edu/tag/09EE), freshly
checked on 2026-09-29. The base-change and odd-degree arguments are D77's
application, not additional assertions quoted from that lemma.

Thus the twisted quadratic fibre must contain K_F(sqrt(-3)). This is
equivalent to c being a square in K_F, and hence in F. Explicitly, if
a^2=c in K_F, then

    c=(Norm_(K_F/F)(a)/c^4)^2.

The scalar is therefore unique modulo F*2. This uses the exact B3 fibre
and the canonical cubic inertia, without a new classification of all
quadratic extensions unramified away from 2 or independent real signs.

## 4. Correction to the active construction plan

D87 and D88 already recorded D77's conditional scalar uniqueness. The
[D130 specification](arithmetic-construction-d130.md) subsequently
reintroduced a separate unresolved scalar-twist gate too broadly. Its
unit witness 1+b is a valid counterexample to local-31 agreement plus
ramification support alone. It does not preserve the D77 cubic-inertia
condition at the odd-degree B3 point. That condition must remain in the
active argument.

Under the three inputs above, the odd Jacobian order fixes the arithmetic
branch half and D77 fixes the scalar, identifying X->C as a cover over F
with the involution and marked divisors. Rigorous continuation of all
277 sampled generator signs remains possible supporting work; it is
not required by this conditional algebraic route. None of this proves
the currently missing marked-base isomorphism.

The next mathematical gates are therefore exact identification of
(C,D17), certified P32/B3 markings, and the canonical Hecke interpretation
needed to transfer the odd order. The subsequent D88 cubic criterion
still requires its orientation and arithmetic hypotheses. Exact global
cubic coefficients or actual Y sections, the combined torsion backend,
global F256 scalar action and original-kernel polynomial remain open.

## 5. Finite replay specification and reference roles

Sources 558/559 specify checks of the exact normalized fibre identities
by two rational-polynomial methods and independently reconstruct P16(32)
from the four saved quartic Hecke factors. The complete earlier curve,
divisor and local-jet certifications are inherited and hash bound.
The historical residual-image verdicts in `f16_steinberg.out` are not
used; their correction in D42 remains in force.

The preliminary D134 unit-squareclass draft was not executed. Its
classification would only supply an optional fallback requiring further
sign and ramification inputs. The present route uses the stronger
arithmetic condition already certified in D77.

All three Stacks references above were checked on 2026-09-29. They
supply general torsion/inertia facts. The odd-order specialization,
line-bundle comparison and resulting construction plan are deductions
for this datum, conditional on the stated canonical identifications.
