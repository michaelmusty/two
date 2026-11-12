# D142: work through both P1600 height targets

The user asked to work through both bullets in D141. Neither target is
proved. This investigation establishes a bound for the actual relation
space, improves the Faltings upper bound, and derives the remaining
Riemann--Roch comparison with its metric factors and correction signs.

| Target | Result of this investigation |
| --- | --- |
| Actual relation-space height at most 623 | Proved upper bound less than 83,240; too weak to apply D141 |
| Actual Faltings height at least 29 | Not proved; upper bound improved to less than 30.039246 |

The first row is a limitation of the estimate, not a lower bound for the
true relation-space height. The second does not assert that the true
Faltings height is close to 29. No exact positive vanishing, candidate
identification or field polynomial follows. No precision bank, spectral
calculation on C, new level, or Hecke computation was launched.

## 1. Sharpen the heights of the actual ratio jets

Use the actual curve and rational residue frame from D99/D105/D106.
[D115](dyadic-comparison-and-strategy-d115.md), section 6, proves that
the chart t=r_2-r_2(P) is valid at every point of D: nonvanishing at one
point and transitivity prove it even at the numerically unresolved anchor.
Thus this argument does not assume a candidate tangent is the actual one.

Write H for the coarse CM fibre height and F for h_Fal(C), with the
existing metrics. Set B=1/(sqrt(pi)*rho^2), rho^2=3/5, V=2^35. Retain
D118's bounds H<=Hplus and F>=Fminus. For the reduced exterior sections
in [D116](cm-compound-height-d116.md), valid norm bounds are

    N_k = sqrt(binomial(16,k)*16^k) V^k B^(17(16-k)),  k=1,2,3.

They follow by Cauchy--Binet and complementary minors. The larger D117
disk changes their norms, not their arithmetic lines or integrality.
We use the conservative Gaussian norm Gamma=2*sqrt(2)/(pi*rho^6),
and the Wronskian norm Omega=2*sqrt(6)/(pi^(3/2)*rho^12).

In the notation of D116, the relevant values and line degrees are

    |f| <= N_1 B,         degree(f) = 256H-16F,
    |gamma| <= N_2 Gamma, degree(gamma) = 241H-15F,
    |kappa| <= N_3 Omega, degree(kappa) = 227H-14F,
    |Delta| <= B^272,     degree(Delta) = 272H-17F.

The first ratio vector has common denominator gamma. The second has
numerators f^3*kappa_j and common denominator 2*Delta*gamma^3; all are
integral sections of degree 995H-62F. Include that denominator when
taking the projective height, so these are joint *affine* bounds
h([1,a_n,1,...,a_n,16]), not just separate coordinate bounds.

Subtract the common finite zero degrees already proved in D116:
62681*log(2)/272 and 259649*log(2)/272. These contents apply to the
fixed chart r_2. No new common content is inferred. Consequently

    B_1 = 241Hplus-15Fminus + log(N_2 Gamma)
            -(62681/272)log(2) < 871,

    B_2 = 995Hplus-62Fminus
            +max(log((N_1 B)^3 N_3 Omega),
                 log(2 B^272 (N_2 Gamma)^3))
            -(259649/272)log(2) < 3532.

These improve D116's 4723 and 19438 using proved subsequent inputs.
They concern the unknown actual curve. Source 598 evaluates them with
rational outward logarithms; source 599 independently recomputes their
collected expressions with Arb balls. Finite contents are subtracted
once, in the height calculation.

## 2. An upper bound for the actual quadratic relation space

Let J_n be the row of 136 coefficients obtained by evaluating all
quadratic monomials in r_1,...,r_16 at Taylor order n. All seventeen
conjugate rows are considered. Put B_0=35*log(2), since the integral
vector (17*eta_j)_j has all conjugates bounded by V. At a place v put
M_n,v=max(1,|a_n,j|_v). The convolution of the Taylor coefficients gives
the following valid projective row-height bounds:

    C_0=2B_0,
    C_1=B_0+B_1+log(2),
    C_2=B_0+2B_1+B_2+log(3).

For example, the two types of terms in J_2 are a_0,j*a_2,k and
a_1,j*a_1,k. Their local maximum is bounded by M_0 M_1^2 M_2;
the sum costs at most log(3) at infinity and nothing at finite places.

The three-order jet map has rank 45. This follows from D140's certified
45 independent dyadic constraints: changing the local parameter and
dividing by omega_1^2 are invertible triangular changes on truncated
jets, and restriction to the degree-16 completion cannot increase the
rank of the full rational map. The actual space I_2 has dimension 91,
so its kernel is precisely the true quadratic relation space. This uses
the constraint rank, not the candidate's coefficients or its height.

The order-zero rows have rank 17: Riemann--Roch gives
h0(2K-D)=28. Through order one the rank is

    45-h0(2K-2D)=34-h0(2D-K) >= 32.

Here 2D-K has degree four, and strict Clifford for the already proved
nonhyperelliptic curve gives h0(2D-K)<=2. The equality case used is
stated and proved in [Bertram, Special Divisors, pages 3--4](https://www.math.utah.edu/~bertram/6180/Special.pdf).
Thus one can choose a row basis with 17 order-zero rows, at least 15
order-one rows, and at most 13 order-two rows. Since C_0<C_1<C_2,
the worst permitted counts are 17,15,13.

Exterior Hadamard, followed by height duality between a rational space
and its orthogonal kernel, now gives

    h_ext(I_2) <= 17C_0+15C_1+13C_2+(45/2)log(136)
               < 83240.                                      (1)

The last term converts the archimedean maximum norm of each row to its
Euclidean norm. This can be proved after extending to a splitting field:
the row wedge spans a rational line, and its absolute height is unchanged
by field extension. Hodge duality identifies its primitive Pluecker
coordinates with those of the saturated kernel, up to signs.

The rational interval underlying (1) is approximately 83239.40720608109.
Without the Clifford refinement the same argument gives less than
149277. Both are bounds for the actual space, but neither is remotely
small enough for D141's strict threshold 623.347163. We do not infer
that the actual space has a large height. This route needs a substantially
stronger global estimate, not merely a shorter basis or more decimal digits.

## 3. Tighten the Faltings upper bound before seeking a lower bound

D120 used each of the seventeen nonzero evaluation cofactors separately.
Their full squared norm is the Gram determinant of the 17-by-16
evaluation matrix. Its Hilbert--Schmidt norm squared is at most 17B^2,
so Cauchy--Binet and arithmetic-geometric mean give

    sum_i |c_i|^2 <= (17/16)^16 B^32,
    (1/17)sum_i log|c_i|
        <= 16log(B)+8log(17/16)-(1/2)log(17).

Galois averaging makes the arithmetic degrees and normalized finite
zero contributions comparable across all seventeen cofactors. Use
D116's dyadic contribution (525/34)log(2). The result is

    F <= 16Hplus+16log(B)-(525/34)log(2)
           +8log(17/16)-(1/2)log(17)
       < 30.039246.                                         (2)

This saves about 0.931610 from D120. It still permits 29; it proves no
lower bound. The exact arithmetic audit also checks fifty small kernel
height, Cauchy--Binet and cofactor arithmetic-geometric-mean controls.

## 4. Riemann--Roch: retain the metric conversion and the signs

Let d=2g-2+sum(1-1/m_i)=1455/32 for signature (16;2^17,3^9,32).
On a regular semistable model after splitting the marked points, put
W_hyp=omega(sum_i(1-1/m_i)P_i) with the orbifold hyperbolic metric.
All degrees below are divided by the field degree. Write

    Psi=sum_i (1-1/m_i^2) h_Wolpert(omega|P_i),
    I=sum_(i!=j) (1-1/m_i)(1-1/m_j)(P_i.P_j)_finite,
    delta=the nodal discriminant degree.

The template is [Freixas i Montplet--von Pippich, Theorem 10.1](https://arxiv.org/pdf/1604.00284v2).
Its section 4.2 uses (i/(2*pi))*integral for differentials, and the
constant function has squared norm d. Our Faltings metric uses
(i/2)*integral. Therefore the determinant-of-cohomology L2 degree is
F+8log(pi)-(1/2)log(d). With the corrected spectral factor C_*Z'(1),
the comparison required for this problem has the form

    12F = W_hyp^2+delta-Psi-I
             -96log(pi)+6log(d)-6 average log(C_*Z'(1)).       (3)

Equation (3) records the necessary normalization and signs; the global
corrected constant and the integral-model comparison are not certified
by this investigation. To obtain a lower bound for F, the terms Psi,
I and log(C_*Z') need upper bounds. Their mere existence or positivity
does not permit dropping the negative terms.

Some terms are already concrete. The dyadic graph length gives
delta_2=(19/2)log(2), counting nodal thicknesses, not just the toric
rank of H1. The elliptic cotangent sum is

    Psi=(51/4)H_2+8H_3+(1023/1024)H_32,

where each H_m is the average fibre height within that order. H_2 is
the existing H, so its contribution is less than 34. The other two
heights have not been bounded here. D119's eight CM intersection pairs
give exactly (33/4)log(2) of the *ordered, weighted* dyadic I. This is
only part of I; a lower bound for I is not the upper bound needed in (3).

## 5. Reconcile the known local cone correction

Put zeta1=zeta_R'(-1), gamma0=Euler's constant, and
G_m=sum_(j=1)^(m-1) j*log Gamma(j/m). Subtracting the old constant in
F-vP Theorem 2.5 from [Kalvin, equation (1.5)](https://arxiv.org/pdf/2011.05407v1)
gives the following local difference; the log-radius term cancels:

    Delta_m = m*(1/6-2*zeta1-(1/2)log(2*pi))
                +(-2*zeta1+2*G_m+gamma0/6+log(m)/6)/m-1/4.

Source 599 checks this subtraction in both forms with Arb at 192 bits:

| m | New minus old constant |
| ---: | ---: |
| 1 | -0.244384680919280 |
| 2 | -0.249209501193934 |
| 3 | -0.249758957153045 |
| 32 | -0.249999796249765 |

For the actual signature their sum is -6.734391930924049. The cone
determinants occur in the denominator of F-vP (9.2). Thus replacing
just that input changes log(C) by minus this sum; it would change the
Faltings value inferred from (3) by half the sum, about -3.367195965462024,
if all other ingredients hold. This is a local substitution calculation,
not a claim that we have certified the complete corrected global theorem.
In particular it is not a newly computed height of C.

## 6. Size of the modular main term and the remaining obligation

[Yuan, Theorem 1.1](https://arxiv.org/pdf/2205.13995v3) gives a relative
modular height Y for the maximal-level Hodge line. Its absolute
normalization here is Y/8. The Petersson differential norm is sqrt(2)
times the hyperbolic norm in (3). Consequently the expected contribution
to W_hyp^2, with the finite-model difference retained as E_model, is

    W_hyp^2 = 2d*(Y/8)+d*log(2)+E_model.                      (4)

The existence of the generic normalizer quotient does not prove
E_model=0. Formula (4) defines the required comparison remainder;
no sign or size is assumed for it.

We evaluated the modular main term rigorously, without computing a
Selberg eigenvalue or geodesic. For F=Q(zeta_32)^+, disc(F)=2^31,
the functional equation gives

    Y=(97/4)log(2)-8log(pi)-8*gamma0+4+zeta_F'(2)/zeta_F(2).

For odd p the residue degree f_p is the order of p modulo sign in
(Z/32Z)^*. Its logarithmic-derivative term is
-8*log(p)/(p^(2f_p)-1); the dyadic term is -log(2)/3. Summing p<=10000
and bounding the remaining absolute sum by

    8*(log(10000)+1)/(10000*(1-1/10001^2))

gives 0.8440203211 < Y/8 < 0.8450413553. The tail follows by replacing
primes by all integers and integrating log(x)/x^2. These are coarse
but certified bounds; rounding cannot explain the remaining problem.

Insert only the main term of (4) and the known delta_2 into (3). Their
contribution to 12F, including -96log(pi)+6log(d), is in
(27.86261465,27.95546495). Therefore the remaining combination

    R = E_model+delta_other-Psi-I-6 average log(C_*Z'(1))

must contribute about 320.05--320.14 for F>=29. A proved R>=320.138
would suffice with the saved outward bounds. No such estimate is supplied
by the current certificates. Assigning any uncomputed term zero would
not be justified. This is a quantified comparison problem, not a spectral
certificate or an obstruction theorem.

## 7. Audit, conclusion and continuation

Sources 598 and 599 pass in 0.20 and 5.19 seconds. The latter checks the
new elementary bounds independently with Arb, fifty exact lattice
controls, the local special-function difference, field discriminant and
Euler-factor tail bookkeeping. These finite checks do not machine-prove
the geometric height argument, Clifford's theorem, the cited papers or
the missing normalizer comparison.

The final source-600 fixed review and replay, and their completion record,
are the checkpoint authority. Preserve sources 598--600, the report, source
ledger and all passing artifacts after review. No D142 input job failed.
Retain the three-worker, 180-second, 2 GiB per-worker/store and 6 GiB
aggregate limits, all earlier failures and the complete inherited graph.

Both bullets have now been developed into explicit estimates. The current
jet-height machinery does not reach 623. The Faltings route still lacks a
corrected global comparison, control of its normalizer model, and bounds
on the remaining terms. The next focused theoretical task is the finite
Hodge-line comparison E_model and the order-3/order-32 cotangent terms;
then assess whether a certified analytic estimate has a plausible target.
This does not admit a numerical spectral job or a larger precision bank.
An exact structural identification remains an alternative to both height
routes. P1600 and column 0/P6400 are unchanged; the field remains open.
