# D104: the intrinsic CM height and a numerical tangent-height bound

Date: 2026-09-24. Continuation of D103, authorized by “keep going!”.

The missing stable coarse-canonical/Hodge comparison in D103 can be
proved without calculating the individual wild quotient charts. For
the actual degree-two map from the genus-40 norm-one curve S to the
genus-16 normalizer curve C, at a ramification CM point Q above P,

    H_CM,disk <= 2*h_L(Q)+log(2) < 41/10.                 (1)

Here h_L is the **absolutely normalized** canonical arithmetic Hodge
height, and H_CM,disk has exactly D103's stable coarse-fibre and
centered-disk metric. Combining (1) with D103 gives

    h(v_j) < 105033/10 < 10504.                          (2)

Formula (2) retains D103's hypotheses: the intended arithmetic CM
field labels, all nonzero evaluation cofactors, and the chosen nonzero
Gaussian denominator. No independent Shimura tangent has been
evaluated, and no candidate identification follows yet. The target
height computation uses no candidate curve equations or tangent values.

## 1. Integral differential on semistable models

Let R be a DVR of mixed characteristic, and let f:X->Y be a morphism
of proper nodal R-curves with smooth generic fibres. Assume the
generic map is finite and separable. Both total spaces are normal.
There is an integral extension

    df:f^*omega_Y/R -> omega_X/R.                        (3)

Here is a local proof, including the case of contracted components.
On the smooth locus of Y, use ordinary differentials followed by
Omega_X/R -> omega_X/R. At a node of Y use an etale chart uv=a and
the dualizing generator du/u=-dv/v. At a vertical codimension-one
point of X, the source is smooth over R and its local ring is a DVR
whose uniformizer is the base uniformizer pi. Write f^*u=pi^m*epsilon
with epsilon a unit. Since d(pi)=0 relative to R,

    d(f^*u)/f^*u = d(epsilon)/epsilon

is regular there. The generic differential is regular at every
horizontal codimension-one point. Normality extends this rational
section of the invertible Hom line across the remaining points.
Etale descent gives (3). In nodal coordinates on X, the integral map
used here is dx->x*xi, dy->-y*xi for xi=dx/x=-dy/y.

The actual generic double cover extends between stable models after
a finite field extension: use Liu--Lorenzini,
[*Models of curves and finite covers*, Proposition 4.4(a)](https://www.math.u-bordeaux.fr/~qliu/articles/modcove.pdf),
page 80; Corollary 4.7, page 82, also applies. The extension need not
be finite on the special fibres. We use stable models, not an
unjustified functoriality assertion for minimal regular models.

## 2. Differentiate the ramification map at its zero

Take the stable extension f:S->C and the extended sections Q and P.
Write W_S=Q^*omega_S and W_C=P^*omega_C. The restriction of (3) at Q
is zero: it vanishes on the generic fibre, and the fibre Hom module
over R is torsion-free. Locally, for generators eta of f^*omega_C
and xi of omega_S, write df(eta)=a*xi. Then a(Q)=0, and

    eta |-> (da)(Q) tensor xi(Q)

defines an integral map

    D_Q(df): W_C -> W_S^2.                              (4)

The derivative uses Omega_S/R -> omega_S/R. If eta is multiplied by
a unit f and xi by a unit g, the new coefficient of (4) is multiplied
by f(Q)/g(Q)^2: every extra derivative term contains a(Q). This proves
independence of generators. It also shows why Q need not be a Cartier
divisor or lie in the smooth locus of the special fibre. No division
by 2 occurs over R.

Generically the ramification order is exactly two, so (4) is nonzero.
At infinity take a centered uniformizing disk z upstairs and u=z^2
downstairs, with ||dz||=||du||=1. The map is

    du |-> 2*(dz)^2,

and its operator norm is 2. For the normalized arithmetic degrees,

    2*h(W_S)-h(W_C) = finite_zero_degree - log(2).

The zero degree is nonnegative, proving

    H_CM,disk <= 2*h(W_S)+log(2).                        (5)

This accounts for the dyadic fibre even if Q meets a node. The
constant log(2) is a safe upper correction; no optimality is claimed.

## 3. Compare W_S with the canonical arithmetic Hodge line

Use the canonical Hodge system in Yuan--Zhang,
[*On the averaged Colmez conjecture*, Theorems 4.5 and 4.7](https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n2-p04-p.pdf),
pages 564 and 567. It is compatible with level pullback. At a
sufficiently small level which is maximal at a specified finite prime,
its local model is semistable and its Hodge line is the dualizing line.
These structural statements have no exclusion of common CM/quaternion
ramification.

Fix any finite prime. Choose an auxiliary sufficiently small level
away from that prime and the quaternion discriminant, preserving
maximal level there. After a finite local extension, lift Q to a
point Q' on the corresponding semistable curve S'. The map S'->S is
generically unramified at Q': Q is an ordinary point on the norm-one
curve. In the saved signature (40;3^18,16), these seventeen CM points
have no norm-one elliptic stabilizer. Their order-two stabilizer is
introduced by the normalizer quotient.

Stabilize S' and apply Liu--Lorenzini to extend the generic level map
to the stable model of S; composing with stabilization gives a map
from the original semistable S'. Apply (3) and restrict at Q'. By
level compatibility, its target fibre is the pullback of L(Q).
Consequently the canonical generic identification W_S=L(Q) gives
an inclusion of lattices at this prime, after clearing Q-line powers.
Checking this after finite extension is sufficient because valuations
scale by the positive ramification index. The auxiliary level may
be chosen separately at each finite prime.

At infinity the comparison is an isometry: ||d(tau)||=2*Im(tau)
becomes ||dz||=1 in a centered uniformizing disk. The metric on W_S
is the one from the Shimura orbifold uniformization; we are not using
the complete hyperbolic metric of the coarse curve. Thus

    h(W_S) <= h_L(Q),

which with (5) proves the first inequality in (1). This argument
compares the stable and Hodge models through small levels; it does
not identify arbitrary coarse canonical bundles with Hodge bundles.
Zhao's one-dimensional Hodge system has this same dualizing, level
compatibility and metric normalization.

## 4. The CM height formula, with normalizations checked

Write M for the degree-16 CM field, to distinguish it from the
degree-17 CM residue field in the frame. Here [F:Q]=n=8 and

    d_F=2^31,  Norm(d_M/F)=2^17,  d_M=2^79,  d_B=2.

The saved embedding beta^2=-(2+b) contains the full ring of integers
of M. Indeed M is the fixed field of {1,31} in Q(zeta_64), with
generator zeta_64-zeta_64^(-1), for a conjugate choice of b. Its saved
polynomial is Eisenstein at 2 with discriminant 2^79. Locally at 2,
an Eisenstein uniformizer generates the full integer ring, and no
other prime divides the possible global index. Script 382 checks
the polynomial identity, orbit, discriminants and character conductors.
No class-number computation enters the height bound.

Let R=L_f'(0,chi_M/F)/L_f(0,chi_M/F), using the finite L-function.
The averaged CM Faltings height and nearby-pair identity give

    h_average = -R/2 - log(d_F*Norm(d_M/F))/4,
    h_average = (n/2)*h_nearby - log(d_F)/4.             (6)

Here h_nearby=h(Phi_1,tau_1)+h(Phi_2,tau_2) is twice the
nearby-pair height in Yuan--Zhang. There are n*2^(n-1) unordered
edges among the 2^n CM types, explaining the factor n/2. The cited
inputs are their Theorem 1.1, Corollary 2.6 and Theorem 2.7.

Zhao's [Theorem 7.4](https://arxiv.org/pdf/2309.08886), specialized
to a singleton partial CM type, gives

    h_L(Q)=h_nearby+log(d_B*Norm(d_M/F))/(2*n).

Its ramification hypothesis allows our common dyadic ramification.
Combining this with (6) yields the formula used in the computation:

    h_L(Q) = -R/8 + log(2)/16.                          (7)

Two normalization checks are essential. First, Zhao uses arithmetic
degree divided by [K:Q], as we do; Yuan--Zhang's *Shimura-point*
height on page 537 divides by [K:F] and is eight times the absolute
height. Their CM Faltings heights in (6) are already absolute.
Second, their CM Faltings metric has squared norm
(2*pi)^(-8)*abs(integral alpha wedge conjugate(alpha)). In this
convention (6) has no additional log(2*pi) term. D103's curve
Faltings metric is different and remains separately accounted for
in its already established constant 8400.

There is a concrete discrepancy in Zhao v1 (16 September 2023):
the last display in the proof of Theorem 7.5, page 27, drops the
d_Sigma factor from log(d_B*d_Sigma), whereas the statements of
Theorems 1.1 and 7.5 and the earlier Theorem 7.4 retain it. Here
d_Sigma=2^17; dropping it would change (7) by (17/16)*log(2).
Our derivation uses Theorem 7.4 and the published identities (6),
and agrees with the stated main theorem. The discarded display is
not used. This is our source reconciliation, not an author-confirmed
correction or an audit of every argument in the preprint.

Yuan--Zhang's CM-point Theorems 1.6 and 1.7, and Yuan's 2024
CM-point Theorem 1.2, exclude common ramification and remain unused.
That exclusion does not affect the structural Hodge results in section 3.

## 5. Rational enclosures for the L-value

The odd characters of Gal(M/Q) are eight conjugate primitive
characters of conductor 64. Put w=zeta_16 and

    psi((-1)^epsilon*5^m)=(-1)^epsilon*w^m,
    A=L(0,psi)=1+w+w^2-w^3-w^4-w^5+w^6-w^7,
    c_a=Trace_Q(w)/Q(psi(a)/A).

The exact norm of A is 2176. For a=1,3,...,63 the numerators of c_a
over 17 are

    12,8,-4,24,28,16,32,20,20,32,16,28,24,-4,8,12,
    -12,-8,4,-24,-28,-16,-32,-20,-20,-32,-16,-28,-24,4,-8,-12.

In particular sum(c_a)=0 and sum(c_a*a/64)=-8. The Dirichlet/Hurwitz
identities [DLMF 25.15.3](https://dlmf.nist.gov/25.15.E3),
[25.11.13](https://dlmf.nist.gov/25.11.E13) and
[25.11.18](https://dlmf.nist.gov/25.11.E18) then give

    R=-8*log(64)+sum_a c_a*log(Gamma(a/64)).              (8)

The main enclosure uses log convexity of Gamma, which follows from
its positive integral and Holder's inequality. For 0<x<1 and N=64,

    F_N(x)=log(N!)+x*log(N)-sum_(k=0)^N log(x+k),
    F_N(x) <= log(Gamma(x)) <= F_N(x)+x*log(1+1/N).

For completeness, convexity gives
Gamma(N+1+x)<=Gamma(N+1)*(N+1)^x. Applying convexity to N+1 between
N+x and N+1+x gives the lower bound
Gamma(N+1+x)>=Gamma(N+1)*(N+x)^x>=Gamma(N+1)*N^x.
Recurrence proves the displayed enclosure. In (8) this leaves

    R_N=-8*log(64*N)-sum_a c_a*sum_(k=0)^N log(a+64*k),
    R_N-(212/17)*log(65/64) <= R
          <= R_N+(76/17)*log(65/64).

Every logarithm is enclosed by rational range reduction and the
atanh series, with 32 terms, an explicit geometric tail, and outward
rounding to 80 binary places. Substitution in (7) proves
h_L(Q)<17/10 and 2*h_L(Q)+log(2)<41/10. All certification uses
rational arithmetic, not floating-point values.

Audit 383 uses a different character generator (3), inverts A by
multiplying its seven other conjugates, and recomputes every trace.
It independently bounds (8) by the convergent expansion

    log(Gamma(x))-log(Gamma(1-x))
      =-log(x)-2*gamma*x-2*sum_(m>=3 odd) zeta(m)*x^m/m,

for x=a/64<1/2. This follows from
[DLMF 5.7.3--4](https://dlmf.nist.gov/5.7).
Use H_512-log(512)-1/512<gamma<H_512-log(512), integral bounds
for the tail of sum_(k=1)^64 k^(-m), odd powers through 25, and
remainder magnitude at most 4*x^27/(27*(1-x^2)). These inequalities
follow from integral comparison and zeta(m)<2. The audit uses its
own 40-term logarithm implementation and outward 64-bit rounding.
It independently proves the same two height bounds.

## 6. Conditional recognition tolerances

Only this diagnostic uses the exact candidate tangent from D101.
For beta_j=sum a_jk*theta^k/q_j with integral coefficients and the
proved root bound |theta|<4, integrality gives

    h(beta_j) <= log max(q_j, sum_k |a_jk|*4^k).

The largest integer in this bound is less than 2^975. Since
log(2)<7/10, all candidate tangent heights are less than 683.
For delta_j=v_j-beta_j, (2) implies

    h(delta_j) < 10504+683+7/10 = 111877/10.

Assume, in addition to the frame and chart hypotheses, that actual
and candidate coordinates belong to the correctly labelled common
field of degree at most 136 envisaged in D101. A nonzero delta has
|sigma(delta)|>=exp(-136*h(delta)) at any fixed embedding. Thus an
absolute error at most **10^(-660791)** at one correctly matched
embedding is a sufficient equality certificate for each coordinate.

Alternatively, the product formula gives
product_sigma |sigma(delta)|>=exp(-d*h(delta)). If **every** complex
embedding has error at most **10^(-4859)**, this contradicts the
inequality for nonzero delta. Conjugate complex embeddings count
separately. Audit 383 proves the strict logarithmic thresholds with
rational enclosures; it does not assume a degree-17 descent for v_j.

These are sufficient conservative tolerances, not minimal precision
requirements, error estimates for an existing evaluator, or evidence
that a computation at this scale is feasible. Sharper denominator
ideals, heights, local certificates or a better chart could change the
practical requirements. No actual error bound presently meets them.

## 7. Checks, remaining work and next decision

Script 382 passed under the 180-second private process-group cap.
Its exact local controls include smooth simple ramification, a
branch-swapping node, and a wild branch-preserving involution on xy=4.
Audit 383 rechecks the latter using second-order exponential jets,
and rejects corrupted character data. These examples verify formulas;
they are not asserted to be equations of the actual bad fibre.

The audit binds this proof, the source ledger, completed job and source
hashes, and checks all 45 D103 bound sources unchanged, including
the transitive D102/D101 sources. It replays the main calculation and
performs the independent character and analytic checks above. These
are computational audits; they do not machine-verify the geometric
proof or the cited theorems. Recheck with:

    python3 dembele/pari/383_cm_intrinsic_height_review.py --check

The intrinsic height gap in D103 is now closed using the cited
theorems and the comparison proved here. Next establish the actual
arithmetic CM labelling and qualitative frame/chart nonvanishing,
and then assess an independent evaluator against a rigorous exactness
threshold. D98's full enclosure still contains zero, so this result
does not pass the gate for another spectral pilot. Keep the existing
enumeration, Hecke-bank and cubic-precision pauses and the 180-second
job cap. Do not repeat the residue-index search solely for this bound.

Candidate identification, exact global cubic/section data, norm-97
separation, target-scale torsion and the final field polynomial remain
separate gaps. Completed sources 382--383 and their bound artifacts
are frozen after the audit. Decisions, references and entry documents
record this checkpoint. No external correspondence was sent.
