# D96: completed scalar and ideal majorant

Date: 2026-09-23. This is the bounded numerical pilot requested after
[D95](nelson-global-identification-d95.md). The original kernel and all
corrected D93 partial sums are unchanged.

The rigorous bound for all uncomputed norm ideals in S11 improves from
2.6795251840e13 to **less than 6.754e12**, a factor greater than 3.967.
It remains about 884 million times the selected partial sum 7640.7582.
The CM anchor is still uncertified. This pilot does **not** justify a
larger quaternion enumeration or Hecke bank.

The improvement retains cancellation in the scalar Mellin integral
and sums the entire positive ideal majorant through its Euler series.
Its value is measured accurately; uncertainty in the quadrature and
far tail is negligible. The remaining difficulty is the replacement
of the signed, complex arithmetic sum by positive orbital and Hecke
majorants. This result does not measure the actual omitted sum, and
does not rule out other ways to exploit its cancellation.

## 1. Completed scalar blocks

Use D91's K_k, Z0=(4*pi^2)^8/2^62 and D95's orientation. For the
(1,1) pair a class of norm N and displacement A>=N contributes

    phase/A * (K3(Z0*A) - (1-N/A)*K4(Z0*A)),  |phase|=1.

Script 360 encloses the completed functions on 96 dyadic A blocks,
from 1 to 2^96. On [2^j,2^(j+1)] put

    A_c=2^(j+1/2), x=log(A/A_c), h=log(2)/2,
    H(x)=K3(Z0*A_c*exp(x))-K4(Z0*A_c*exp(x)),
    Q(x)=exp(-x)*K4(Z0*A_c*exp(x)).

The D91 trapezoidal rule uses s=2+it, mesh 1/32 and height 16.
Before taking absolute values, expand each node through degree 31
in x and sum its coefficients in 320-bit Arb arithmetic. The H
multiplier is `-(s+2)*(s)_3`, and the Q multiplier is `(s)_4` with
exponent `-(s+1)*x`. The finite-node remainders are bounded by

    |factor|*exp(c*h)*(|s+shift|*h)^32/32!,

with (shift,c)=(0,2) or (1,3). This follows from the integral
remainder for the complex exponential, since x is real. Sum these
positive bounds over the nodes and include Z_c^-2. Add D91's
analytic infinite-trapezoid and vertical-tail errors, evaluated at
the smallest Z in the block. For Q multiply that analytic error by
sqrt(2). This encloses every point of each block, not just its centre.
The A=1 values overlap the corrected D93 K3 and K4 enclosures.

Script 361 proves, on the smaller full range 1<=A<=T=2^72, that

    K3(Z0*A)>0,
    K4(Z0*A)-K3(Z0*A)>0,
    d(K4(Z0*A)/A)/dA < 0.

For K3 recover the polynomial H+exp(x)*Q by convolution of Taylor
coefficients. Its remainder is at most one fourth of the H remainder,
because |s+2|>=4 on the contour; its analytic error is the K3 error.
For the decreasing condition use -Q', whose finite remainder is
32/h times Q's remainder. Since

    Q'=exp(-x)*(3*K4-K5),

its analytic error is at most sqrt(2)*(3*error_K4+error_K5).
Each polynomial is converted to Bernstein form on [-3/8,3/8], which
contains [-h,h]. Every Bernstein coefficient exceeds the corresponding
remainder and analytic error. This certifies all 72 blocks without a
sign assumption about the untested infinite tail. Audit 362 independently
replays the 6,840 coefficient inequalities with rational intervals.

Thus, for N<=A<=T,

    |K3-(1-N/A)*K4|/A <= K4/A.

No higher derivative-pair bound is improved in this checkpoint.

## 2. Sum over every point of an orbit

D92 proves that disks of radius r=acosh(8) around points in any
one right norm-one orbit are disjoint. For a norm-N orbit let
C_N(A) count its points with invariant at most A. Distances satisfy
D=A/N=cosh(distance/2)^2. Comparing the disjoint disks with the
disk of radius distance+r gives

    C_N(A) <= [8*(2*D-1)+2*sqrt(63*D*(D-1))-1]/7
            <= (32/7)*A/N.

The count applies separately to each orbit; disks from different
orbits are not asserted disjoint. Put kappa=32/7. Stieltjes integration
of the positive decreasing function g(A)=K4(Z0*A)/A proves

    sum_(A_gamma<=T) g(A_gamma)
       <= kappa/N * [K4(Z0*N)+integral_N^T K4(Z0*A)*dA/A]

for N<=T. In particular this does not charge a fresh packing bound
independently for every narrow displacement block.

For an odd ideal a, write w(a)=d(a)*sigma_1(a). D93 bounds the
number of right orbits by sigma_1(a), and Ramanujan bounds the Hecke
coefficient by d(a)*sqrt(N(a)). Define the completed scalar

    F(N)=K4(Z0*N)+integral_N^infinity K4(Z0*A)*dA/A.

The positive ideal majorant can now be summed without enumerating
the ideals. Its Mellin multiplier is (1+1/s), and D93's Euler identity
gives the particularly useful cancellation

    zeta_F(2*s)*D_odd(s+1/2)
      =zeta_F(s+1/2)^2*zeta_F(s-1/2)^2/F2(2^(-s-1/2)),
    F2(x)=(1-2*x^2)/((1-x)^2*(1-2*x)^2).

Thus we evaluate

    S = sum_(a odd, a not 1 or p31) w(a)*N(a)^(-1/2)*F(N(a))

by one completed Mellin integral, subtracting the unit contribution
and `64/sqrt(31)*F(31)`. Only the saved prime (31,b-27) is removed;
the other seven ideals of norm 31 remain in this sum. The coefficient
64 is 2*(31+1), not a Hecke eigenvalue.

## 3. Quadrature and the finite-range splice

Use Re(s)=5/2, mesh 1/64, height 16 and strip half-width 1/2. The
integrand is holomorphic on the strip 2<=Re(s)<=3. The pole at 3/2
of the new zeta factors lies outside it. The fine rule and an
independently enclosed mesh-1/32 rule overlap for the full ideal sum,
unit term and removed prime term.

At the integer boundary contours use D91's Gamma polynomials and
the absolute zeta bounds zeta_F(c+1/2)^2*zeta_F(c-1/2)^2. For the
reciprocal local factor, with x=2^(-c-1/2), use

    |1/F2(2^(-s-1/2))| <= (1+x)^2*(1+2*x)^2/(1-2*x^2).

The strip error is bounded by (boundary_2+boundary_3)/(6*(exp(3*n)-1))
at denominator n. The Binet bound used in D94, now at c=5/2, gives

    |Gamma(5/2+it)|^16 <= 8^8*exp(8/15)*(3+t)^32*exp(-24*t).

After multiplying the remaining factors, the tail polynomial is

    (3+t)^39*(4+2*t)*product_(j=0..3)(3+j+t),

of degree 44. Beyond t=16 its product with exp(-24*t) decreases;
the exact factorial tail integral bounds the omitted quadrature
nodes. Audit 362 replays that polynomial and integral. The resulting
enclosure of S is centred at

    1477349989894.07203507307804001951679133318669734369...

with width less than 1e-40. This is a positive majorant's scalar sum,
**not** an evaluation of the target eigenform.

We do not assume the sign or monotonicity statements beyond T.
Use the corrected D93 contour-c=4 constants B_H and B_K for
|K3-K4| and |K4|, respectively. Put u=25/16 and

    D=D_odd(u+1/2), C_u=1/(1-(2/9)^u),
    L=Z0^(-4)*T^(u-4)*D.

Every omitted quaternion with A>T has total contribution at most

    E_A = L*(B_H+B_K)*C_u < 3.096e-7.

Replacing integral_N^T by integral_N^infinity for N<=T costs at
most kappa*L*B_K/4. Extending the completed ideal sum to N>T costs
at most kappa*L*B_K*(1+1/4). Both follow from the contour-4 bound
and the same positive divisor mass, with no ideal census. Therefore

    E_splice = kappa*L*B_K*(1+2/4) < 1.034e-6,
    E_uncomputed <= kappa*S + E_A + E_splice
                 = 6753599953801.472161677187411481... < 6.754e12.

Add the unchanged two-family tail, less than 9626.300, when combining
this bound with the partial sum 7640.7581837028. The full enclosure
still contains zero. D95's full-series nonnegativity can intersect it
with [0,infinity), but cannot prove a nonzero CM derivative.

## 4. Cost decision and reproducibility

This experiment measures the completed positive comparison accurately.
Finer quadrature, tighter Taylor blocks or moving the far splice
cannot remove its remaining factor of about 884 million relative to
the current partial sum. A substantially different treatment of the
orbital/Hecke majorants, or a method that retains signed and angular
cancellation, is needed before a larger enumeration is justified.
This is a conclusion about the tested comparison, not an impossibility
claim for Nelson's method or a lower bound on the actual error.

The saved finite families do not yet demonstrate an enormous
cancellation effect. Rational square-root bounds in audit 362 give
sum(|term|)/|sum(term)| about 1.064799 for the 541 unit classes and
3.652448 for the 586 prime-31 classes. Their absolute sums are about
7791.925701 and 161.306035. These are finite diagnostics only; the
unit family is dominated by its identity term. They cannot predict
the behavior of the uncomputed large-norm families.

**Next:** review a concrete way to bound signed Hecke blocks or
quaternion orbit sums before replacing them by counts. Its first
test should use the existing unit/prime-31 data and give an explicit
estimate for what remains uncomputed. A small cutoff increase,
another precision increase or another evaluation of this same
positive majorant is not the next step. The already proved D95
global identification does not need to be repeated. Exact CM jets,
marked curve identification, cubic recognition and the field
polynomial remain open.

Script 360 passed in 9.16 seconds and script 361 in 11.95 seconds,
rounded up. Both used the 180-second process-group limit and fresh
DOT_SAGE directory. Exact dyadic endpoints are exported with
`.exact_rational()`. Sources 360--362 and the bound report/artifacts
are frozen after the audit. No Hecke rebuild, new quaternion census,
remote run, candidate change or higher cubic precision occurred.

Recheck with:

```sh
python3 dembele/pari/362_nelson_completed_majorant_audit.py --check
```

Root: `dembele/data/computed/nelson_completed_majorant_d96.json`.
It binds the D95 root and its existing provenance, the new sources,
two bounded runs and this analytic proof. It replays rational signs,
tail-polynomial arithmetic, directed final error assembly and saved
finite-family diagnostics. Transcendental Arb node evaluations are
bound to their runs rather than independently re-executed by the audit.
