# D120: close the frame comparison and price the precision route

Date: 2026-09-26. Continue the original-kernel field construction. This
reassessment rejects the D119 inverse-frame estimate, retains D118's
integral quadratic-section certificate, and starts a different transport
implementation. It also settles the norm-97 cofactor-separation question
using existing Hecke input. **No positive quadric jet is proved exactly
zero, no candidate identification is proved, and no field polynomial is
constructed.**

Inputs and attribution are in [the source ledger](../data/computed/construction_reassessment_sources_d120.json).
The previous [D119 report](cm-cartier-frame-d119.md) remains frozen.
Scripts 458--461 and 463 produce the new calculations; 462 independently
reviews the numerical bounds, inverse norm, error propagation and finite
polynomials, and preserves all 922 D119 source hashes. The geometric and
metric arguments below are mathematical proofs, not formalized theorems.

## 1. The full cost of the Cartier inverse frame

Use D119's notation, with g=16 and d=17. Write H for the common normalized
CM fibre height, F for the determinant L2/Faltings height, I for the total
finite intersection degree and tau for the total cohomology torsion degree.
The principal-parts line Lambda has its induced metric. Put

    B=1/(sqrt(pi)*rho^2),  rho^2=3/5,
    L=42550,  V=2^35,
    C_1=2*sqrt(2), C_2=2*sqrt(3)+2, C_3=4+2*sqrt(6).

At infinity identify A^vee with C^17 using its value coordinates and
the standard direct-sum metric, and give Z=ker(ell -> ell(1)) the
induced metric. The normalization inclusion has finite index I, and
the sum map has norm sqrt(17). Consequently

    h(det Z)=I-(1/2)*log(17).                              (1)

The residue map R:Lambda tensor E -> Z is generically an isomorphism.
Let j be its normalized finite determinant index. Choose a clearing
ideal J using its determinant/Fitting ideal away from 2 and the
annihilator beta^2 at 2. If d_J denotes the positive degree of J, D119
gives

    d_J-j <= -(7/8)*log(2).                              (2)

This avoids assuming that uncomputed odd-prime indices vanish. The
integral vectors v_k=17*eta_k belong to Z; their archimedean norms are
at most sqrt(17)*V. Their inverse images are integral sections of
E tensor Lambda tensor J^(-1). Locally, multiplying their coefficients
by a generator of J expresses them in an integral frame of this line.

For a unit vector h of Lambda, let r_i be its simple-pole coefficients
in unit tangent frames. Then sum |r_i|^2=1 and
R(h tensor omega)_i=r_i*omega(P_i). Thus ||R||_HS <= B. The product of
its largest fifteen singular values is at most (B^2/15)^(15/2), by
arithmetic-geometric mean. The determinant identity is

    average log |det R| = j-h(det Z)+16*h(Lambda)+F.       (3)

The quadratic product/jet estimate of D116--D117, applied to the inverse
images, therefore gives the following upper bound for arithmetic degree
plus logarithmic archimedean norm of the order-n section:

    (n+2)*H -30*h(Lambda)-2*F+2*I+2*(d_J-j)
      +32*log(B)-15*log(15)+log(L)+2*log(V)
      +log(C_n)+n*log(5/3).                              (4)

In particular the inverse determinant is not free. The factor log(17)
from the target vectors cancels against the metric term in (1).

We can slightly strengthen D119's pencil estimate: the restriction map
has Hilbert--Schmidt norm squared at most 17*B^2, so its volume is at most
(17/16)^8*B^16. Hence

    h(Lambda) >= -17*H+F+I+tau-8*log(17/16)-16*log(B).   (5)

Substitute (5) in (4), then use I >= (33/2)*log(2),
tau >= (7/8)*log(2), (2), and D118's bounds

    H <= Hplus=2*hLplus-(35/34)*log(2),
    F >= -16*log(pi)-8*log(2)+theta*log(2),
    theta=55817/54150.

The result is

    Fnew_n=(512+n)*Hplus+(-164-32*theta)*log(2)
      +256*log(pi)+log(L)+log(C_n)
      +240*log(17/16)-15*log(15)+(512+n)*log(5/3).        (6)

All omitted odd-prime terms have the correct sign after this substitution.
No global scalar generator of Lambda is required.

The local zero comparison must also change normalization. In D119's
primitive normalization the anchor principal part is beta^2, and
R_h(psi)=-beta^2*eta. The locally cleared inverse frame is -17*psi.
D116's old quadratic section is

    q_old=17^2*(Delta/c_W^2)*Q(psi),
    v_beta(Delta/c_W^2)=4200-2*280=3640.

The new section's non-anchor bounds are therefore the old bounds minus
3640. At the anchor use its integrality to retain the lower bound zero.
Higher orders still require preceding exact zeros.

| Order | New sufficient non-anchor valuation | New measured lower bound | Gap |
|---|---:|---:|---:|
| 1 | 43459 | 154 | 43305 |
| 2 | 43553 | 105 | 43448 |
| 3 | 43642 | 88 | 43554 |

The full degree-minus-measured-zero margins are worse than D118 in
every order. **Reject this inverse-frame estimate.** This conclusion
concerns the proved estimates and current data, not every possible
principal-parts argument. D118's sufficient section valuations remain
25330/25444/25551 for its existing anchor bounds; actual values remain
3794/3745/3728. Known vertical content is not a second height gain.

## 2. Improving only the Faltings lower bound cannot rescue D118

Each nonzero evaluation cofactor c_i is an integral section of
(product_(j != i) W_j) tensor (det E)^(-1), of degree 16*H-F.
Its archimedean norm is at most B^16 by Hadamard's inequality. Galois
averaging of the known local values [280,245 x 16] gives finite zero
degree at least

    ((280+16*245)/272)*log(2)=(525/34)*log(2).

The product formula therefore also supplies an upper bound:

    F <= 16*Hplus+16*log(B)-(525/34)*log(2)
      < 30.970856.                                      (7)

With all other D118 inputs and measured zeros fixed, a Faltings-only
rescue would need lower bounds exceeding approximately
35.3913455/35.8359594/36.1713345. Equation (7) rules this out.
This eliminates a proposed single-input improvement; it is not an
obstruction to the curve or target field.

## 3. Translate the section certificate into a working-precision design

Source 461 computes the non-anchor normalized evaluation Smith factors
[0 x 8,35 x 8]. Review 462 independently checks its inverse using
valuation-ball Gauss--Jordan arithmetic. Thus all inverse entries have
valuation at least -35. The sixteen frame-relation entries q_i have
valuation exactly -35, as already certified in D115.

Suppose a future actual calculation supplies all four raw coarse
coefficients with error E=2*P+32 beta-digits, refines the eta values to
at least E, and retains the certified branches and fibre scalings.
Use beta-ring arithmetic of precision at least 2*P+64. The kernel-tail
argument of 442 with CM cutoff 2*P-1 supplies this common raw error from
P pi-digits of certified chart moments. The error propagation is:

| Quantity | Absolute beta-error lower bound |
|---|---:|
| normalized non-anchor leading matrix | E-33 |
| its inverse | E-103 |
| normalized anchor leading row | E-296 |
| relation q | E-331 |
| reciprocal 1/q | E-261 |
| change into the residue frame | E-296 |
| coarse quadratic coefficient | E-296 |

For example, the relation error is min(E-296-35,E-103)=E-331.
The inverse has entry bound -35 and the eta/q matrix has entry bound
35, so their product has integral entries. Raw jets and the resulting
residue-frame jets are also integral. This explains the last two rows
without assuming any positive quadric coefficient vanishes.

**If the future quadratic enclosures contain zero through these errors**,
the integral-section lower bounds are

    N_n(P)=2*P+3310-33*n,        non-anchor,
    A_n(P)=2*P+2784-296*n,       anchor.

Insert these into D118's inequality (16*N+A)*log(2)/272 > Fold_n.
The sufficient precisions rounded upward to multiples of eight are
10416/10480/10552. Thus **P=10552** is a sufficient common design under
the stated hypotheses. This is not a prediction of equality or an
assertion that 10552 is the minimum attainable precision by any method.
It differs from merely interpreting section valuations as moment digits.

At P=10552 the modulus uses 1319 bits per base-field coefficient. Even
with packed storage, low moments require 2,423,583,360 bytes per harmonic
column, or 38,777,333,760 bytes for sixteen columns, before work buffers.
The former dense child-operator layout would require 72,750,331,368,000
bytes. Extending source 429's int64 implementation is not an option.

## 4. A different transport implementation, with measured costs

For a child map phi(x)=(a*x+b)/(c*x+1), write moments m_k and
K(S)=sum_(k>=0) m_(k+1)*S^k. Set A=a*T-c, D=1-b*T and Delta=a-b*c.
Summing the geometric series inside the moment functional gives

    sum_(n>=0) mu(phi(x)^n)*T^n
      =m_0/D+Delta*T*K(A/D)/D^2.                         (8)

For a finite input of length P, homogenize K to degree P-2; the second
term has denominator D^P. Divide-and-conquer homogenization and
polynomial multiplication replace the stored quadratic-size operator.
There is no division by c, Delta or any other nonunit. For child maps,
v_pi(c)>=1 and v_pi(Delta)>=1 imply the coefficient of x^k in phi(x)^n
is divisible by pi^k. Hence omitting input moments k>=P is valid modulo
pi^P. CM-chart truncations use their separate existing tail certificate.

Script 459 implements (8) with arbitrary Python integers. Bivariate
Kronecker packing uses b-exponent stride 15 and a digit width whose base
exceeds 8*min(lengths)*(2^bits-1)^2. Thus no coefficient carries into
another slot. Reduction by b^8-8*b^6+20*b^4-16*b^2+2 occurs afterwards.
Controls cover up to 1536-bit coefficients, beyond the proposed 1319.

On the actual frozen P=200 bank, this implementation checks one harmonic
column in all 174 state equations, all 348 child actions (165 distinct
maps), and all 17 CM charts: 332800 scalar coefficients. No moments are
refined. Synthetic compatible tests at P=200/400/800/1600 expose poor
Python integer multiplication costs: approximately
0.153/0.779/6.001/51.126 seconds per action.

Script 463 uses the installed GMP 6.3.0 library for large packed products
and integral binomial formulas for linear-form powers and D^(-P).
Binomial divisions are exact in Z before ring reduction, so they do not
invert even integers in the local ring. Its import/export controls agree
with Python integers; every actual-bank check above passes again.
The same synthetic action ladder takes about
0.067/0.150/0.396/1.146 seconds. A separate **synthetic** P=10552 action
passes in 50.408 seconds, with maximum packed product 105,082,980 bytes;
its P=200 reduction agrees with the first implementation. The two input
jobs, including controls and loading, take 28.396 and 50.790 seconds.

This establishes feasible individual operations and removes the dense
operator table. It does not price or implement a complete solve. At the
last synthetic action's rate, 348*16 actions alone would take about
3.25 days. That multiplication is an illustration, not a forecast for
actual maps or for a production implementation. Repeating full-precision
sweeps thousands of times is not an acceptable next step.

The concrete next algorithmic test is low-moment elimination. Once
masses are fixed, the transport matrix T has its degree-k input column
divisible by pi^k. Split the first r positive moments L from the rest U.
Since T_LL is divisible by pi, I-T_LL is integrally invertible, and the
reduced iteration matrix is

    S=T_UU+T_UL*(I-T_LL)^(-1)*T_LU.

Every column of S is divisible by pi^(r+1). Thus exact elimination of
these low moments improves the uniform correction gain to at least
r+1. First implement and time r=1 on the existing P=200 bank, checking
the original residual and all input/output precision losses. Its block
has dimension 174. Require a costed low-block solve and streaming storage
before increasing r or refining actual moments. The theorem about the
gain alone does not make the low-block inverse cheap.

## 5. Norm 97: the existing bank already isolates the targets

The canonical Y64 realization and integral all-Hecke occurrence are
proved in [D51](target-realization.md). Its differentials consist of the
old sixteen-dimensional part of the level-p-new space and the
48-dimensional level-p^2-new/sign-type space.

The frozen source-58 log supplies the trace polynomials

    h_a=t^8+t^4+t^3+t^2+1,
    h_b=t^8+t^6+t^5+t+1,

each with multiplicity 1 at level one and 4 in the full level-p^2 module.
The target occurs in the p^2-new space by D51 (and the saved joint
31/97 calculations). Old/new multiplicities therefore satisfy, for
each target,

    4=3*1+2*m_(p-new)+m_(p^2-new),
    m_(p-new)>=0,  m_(p^2-new)>=1.

The unique possibility is (0,1). Constants in the raw Brandt modules
have eigenvalue 98=0 modulo 2 and cannot contribute these factors.
Independently, the source-60 log records the whole level-p-new
T97 polynomial as t^40 modulo 2. The Y64 old part consequently contains
neither factor, and each target is simple in the Y64 differential
polynomial. The all-Hecke injection also bounds its multiplicity in the
sign part by the level-one multiplicity, giving the same conclusion.

Under f(t) -> x^deg(f)*f(x+x^(-1)), coprime trace factors with nonzero
constant term remain separated. Sources 460/462 verify the resulting
degree-16 torsion polynomials. The first splits as two irreducible
degree-eight factors with root order 51. The second is irreducible of
degree sixteen with root order 257. Both are squarefree and coprime to
their full Y64 Euler cofactors, without needing the remaining Euler
coefficients. Thus ker(psi_a(Frob_97)) on J(Y)[2] is exactly the desired
sixteen-dimensional target, rational over residue extension degree 51.
The saved joint calculation matches it to **the second T31 target**.

There are 65535 nonzero vectors and 1285 Frobenius orbits in that target.
Its 257 projective F256 lines remain the desired invariant input.
One local Frobenius does not supply the global Hecke scalar action or
identify an arbitrary candidate with canonical Y64. The combined genus-64,
degree-51 torsion backend, global cover realization, scalar selection
and field certification all remain required. No new Hecke computation
was run, and the saved matrices themselves are not regenerated here.

The first 460 attempt incorrectly expected order 51 for both targets.
Its factorization assertion rejected that expectation. The frozen source-64
output already recorded order 257 for the second; the corrected script
and independent review preserve that distinction. The failed source,
log and receipt are archived.

## 6. Decision and remaining construction gates

Continue the direct integral-section route with the stated conditional
precision target. Close the inverse-frame and Faltings-only detours for
the current estimates. Develop and test low-moment elimination before
any large actual refinement. Preserve the P=200 bank, all resource
pauses, and runner 272's single-threaded 180-second private-process-group
cap. The individual-operation benchmark does not authorize bypassing
the complete solver's cost, storage or independent-residual checks.

An exact geometric identity would still be valuable, but none has been
established. Theorem 3.1 of
[van Bommel--Costa--Poonen--Srinivasan](https://arxiv.org/pdf/2506.14026)
uses exact expansion data over a computable field; it does not turn the
present approximate coefficients into exact zeros. No replacement
identification theorem is claimed from that reference.

After exact marked-base identification, the marked double and cubic
cover realization and the genus-64 section interface remain necessary.
The norm-97 cofactor question is now settled, but genus-64 torsion over
degree 51, the correct F256 action, the degree-257 invariant and the final
original-kernel/ramification checks remain open. Nonhyperellipticity
does not invalidate the known field's existence.
