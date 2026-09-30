# D97: signed orbital blocks and the missing infinite estimate

Date: 2026-09-24. Resumption of [D96](nelson-completed-majorant-d96.md).

**Result:** a concrete cancellation mechanism works on the saved data.
Exact displacement-shell grouping followed by discrete Abel summation
reduces the bound for the outer saved block by factors greater than
**6.45** for the unit family and **8.16** for the norm-31 family.
We also compute rigorous constants that turn a specified, uniform signed
counting estimate into an infinite remainder bound. That counting
estimate has **not** been proved. Consequently the actual global error
bound remains D96's **<6.754e12**, plus the unchanged two-family tail
<9626.300. The CM anchor remains uncertified, and enumeration expansion
is not justified.

This checkpoint uses all 541 unit classes and 586 classes at the saved
prime (31,b-27), without new quaternion enumeration or Hecke coefficients.
The original Mellin weight, D95 identification and derivative orientation
remain unchanged. The cancellation found here concerns finite blocks;
it is not evidence for a numerical bound on every uncomputed block.

## 1. Exact signed shells

For a fixed odd norm ideal, choose its positive generator n and write
N=Norm(n). In the CM chart let

    f_N(A) = [K3(Z0*A)-(1-N/A)*K4(Z0*A)]/A,
    Phi(alpha) = (X/|X|)^4,
    A = N*|X|^2/sigma_0(n).

Then the S11 summand, before its Hecke coefficient, is Phi(alpha)*f_N(A).
The real part of X is sigma_0(Trd(alpha))/2. Thus the phase's real part
is the split-place value of the exact field element

    tau = N*Trd(alpha)^2/(4*n*A),
    Re(Phi(alpha)) = 1-8*tau+8*tau^2.

Here A on the right is the saved element of F, evaluated at sigma_0
when used as a real displacement. Reduced conjugation alpha -> bar(alpha)
preserves the maximal order, reduced norm and A; it conjugates X and
therefore Phi. Every complete shell is closed under this operation.
Consequently its phase sum is real, including the self-paired cases
modulo sign. Script 363 checks the involution on all 1,127 classes.

There are 80 distinct A-values in the unit family and 83 in the prime
family. Their summed phases are exact elements of F. Audit 367 checks
them without algebraic-number software: after clearing denominators,
each group of m classes satisfies

    2*(n*A)^2*(phase_sum-m)
      = -4*N*(n*A)*sum Trd(alpha)^2 + N^2*sum Trd(alpha)^4.

An isolated root of the field polynomial supplies independent rational
enclosures. The resulting real shell terms agree with the corrected
D93 kernels and sums; the paired imaginary sums contain zero.

Conjugation does not force zero shell sums. Nor does the CM normalizer
beta supply a fourth-root cancellation: its left action multiplies X
by a purely imaginary scalar, whose fourth phase power is 1. More
generally, odd central scalars alpha=m have Phi=1 and A=N=m^16.
Thus a uniform pointwise phase contraction strictly below 1 is false.
This observation does not exclude cancellation among many different
classes or ideals.

## 2. Finite Abel summation

Within a block, order the distinct displacements A_1<...<A_m, let p_i
be their signed phase sums, and put P_i=sum_(j<=i) p_j. Then exactly

    sum_i p_i*f_N(A_i)
      = P_m*f_N(A_m) + sum_(i<m) P_i*(f_N(A_i)-f_N(A_(i+1))).

Taking absolute values only on the right retains cancellation in every
P_i. No assumption about monotonicity or an infinite counting law is
needed. We compare this bound with summing absolute values before and
after exact shell grouping. The following displayed upper bounds are
rounded up; the signed sums are approximate diagnostics.

| Family | A block | Signed sum | Individual absolute sum bound | Shell absolute sum bound | Abel bound |
|---|---:|---:|---:|---:|---:|
| Unit | (400,1600] | -9.279595 | 19.328632 | 9.279595 | 9.279595 |
| Unit | (1600,6400] | 6.188873 | 15.608639 | 12.124886 | 6.188874 |
| Unit | (6400,25600] | 0.843735 | 5.526555 | 3.352054 | 0.855935 |
| Prime 31, unweighted | (400,1600] | 0.298700 | 61.342494 | 40.430120 | 3.931733 |
| Prime 31, unweighted | (1600,6400] | -2.377581 | 16.566471 | 14.154530 | 3.546761 |
| Prime 31, unweighted | (6400,25600] | -0.092712 | 5.385974 | 3.665527 | 0.660035 |

Over the whole saved prime family the Abel bound is <46.572979,
versus individual absolute sum <161.306036. For the whole unit family
the identity term dominates, and Abel summation is worse than grouping
alone. We keep the smaller valid finite bound in each comparison.
These bounds do not change the already computed finite sums.

For the **whole ideal family**, define the real cumulative phase count

    P_N(A) = sum_(A_alpha<=A) Phi(alpha).

The finite data prove, for N<=A<=25600, the following inequalities:

| Family | Bound with exponent 1/2 | Bound with exponent 2/3 |
|---|---:|---:|
| Unit | |P_1(A)| <= sqrt(A) | |P_1(A)| <= A^(2/3) |
| Prime 31 | |P_31(A)| <= 2.030*(A/31)^(1/2) | |P_31(A)| <= 1.619*(A/31)^(2/3) |

The maximum is checked at every shell endpoint; between endpoints P_N
is constant and the comparison increases. These are not bounds for
individual right norm-one orbits, and they have no proved extension
beyond 25600. In particular, square-root behavior is not inferred
from a probabilistic independence assumption.

## 3. An explicit infinite-remainder interface

Let T=25600. Stieltjes integration by parts gives

    tail_N(T) = -P_N(T)*f_N(T) - integral_T^infinity P_N(A)*f_N'(A) dA.

The boundary at infinity vanishes, for example by the existing linear
packing bound and the contour-4 decay. The derivative is

    f_N'(A) = (2*K3-4*K4+K5)/A^2 + N*(2*K4-K5)/A^3,

where every K is evaluated at Z0*A. Thus **if** an additional proof gives

    |P_N(A)| <= M*(A/N)^theta for every A>=T,

then

    |tail_N(T)| <= |P_N(T)*f_N(T)| + M*J_(N,theta),
    J_(N,theta) = N^(-theta)*integral_T^infinity A^theta*|f_N'(A)| dA.

Script 366 certifies the following upper bounds for J. They are transfer
constants, not estimates of P_N and not actual signed remainder bounds.

| N | Boundary term, upper bound | J for theta=1/2 | J for theta=2/3 | J for theta=3/4 | J for theta=7/8 |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.124645 | 1.450731 | 9.091228 | 22.943440 | 93.132757 |
| 31 | 0.116890 | 0.261146 | 0.923191 | 1.749891 | 4.623547 |

For example, a proof extending the unit-family bound with theta=2/3
and M=1 would give tail <9.216, compared with the current <1124.696.
That extension is missing. Even a successful proof for these two
families would leave all other norm ideals to control.

### Certification of the transfer constants

Reuse D96's completed Taylor blocks, with x=log(A/A_c),
H=K3-K4 and Q=exp(-x)*K4. Then

    f_N'(A) = [H'-H+(N/A_c)*(Q'-Q)]/A^2.

On each block, form the coefficients of p'-p before taking absolute
values. The polynomial bound uses |x|<=3/8. For h=log(2)/2, the error
in differentiating a degree-31 exponential Taylor polynomial is at
most (32/h) times its original exponential remainder. Add the original
remainder for the subtraction of p. If e_k is D91's analytic quadrature
error for K_k at the smallest A in the block, valid conservative
analytic errors are

    H'-H: 4*e3+6*e4+e5,
    Q'-Q: sqrt(2)*(4*e4+e5).

Integrate the resulting bound times A^(theta-2) exactly by algebraic
powers. There are 58 intersecting blocks from T through U=2^72.
Their fractional-power integrals are independently enclosed by integer
root arithmetic in audit 367.

For A>U use Re(s)=4. Let P_4,3(t) be D91's integer-contour polynomial
majorant for the Gamma factors. Multiplying it by (t+5)(t+6) and
(t+6)(t+7) bounds the two derivative multipliers. Exact factorial
integration against exp(-24*t), together with
zeta_F(8)<=(8/7)^8, the cusp bound 544/31 and 1/pi<1/3, gives rational
constants B_H and B_Q. The remaining part of J is at most

    Z0^(-4)*N^(-theta)*[
      B_H*U^(theta-5)/(5-theta) + N*B_Q*U^(theta-6)/(6-theta)].

No infinite-tail sign assumption enters this calculation. The rational
audit replays both degree-69 polynomials, their integrals and all
fractional powers. The completed scalar Taylor coefficients and their
analytic errors remain bound to the D96 and new runs.

## 4. Which signed counting theorem is needed?

In our CM-centered Cartan chart, X/|X|=exp(i*(theta_1+theta_2)), so
Phi=exp(4i*(theta_1+theta_2)). This is a harmonic in **both** Cartan
angles, with n=k=2 in the convention of Bourgain--Kontorovich--Sarnak.
The position angle alone does not determine it. Their
[*Sector estimates for hyperbolic isometries*, Theorem 1.1](https://www.math.ias.edu/files/avi/Bourgain_Kontrovich_Sarnak.pdf)
records Good's finite-volume result: a vanishing constant contribution
for these nonzero K types, possible exceptional spectral terms, and
an O(R^(4/3)) remainder in their matrix norm. Since R^2=4*A/N-2,
the remainder exponent becomes 2/3 in A/N. Neither its unspecified
constant nor the exceptional terms can be replaced by the observed
finite-prefix constants. The paper's new second-kind results do not
directly apply to this cocompact lattice.

For uniformity in translated right orbits,
[Gorodnik--Nevo, *Counting lattice points*, Theorem 1.9, Corollary 1.11 and Remark 1.12](https://arxiv.org/pdf/0903.1515)
provide a framework using quantitative ergodic estimates, geometric
regularity and injectivity parameters. Adapting it to this weighted
harmonic still requires explicit numerical inputs and a threshold.
The existing separation proof at one CM point does not supply that
entire package. Neither source is used as an instantiated numerical
bound in this certificate.

There is also a norm-summation issue. Suppose, conditionally, that
every individual right orbit has phase count at most C*(A/N)^theta,
uniformly for A>=N. A contour-c derivative bound gives its full
contribution at most

    C*Z0^(-c)*N^(-c-1)*[
      B_H(c)/(c+1-theta) + B_Q(c)/(c+2-theta)].

After summing at most sigma_1(a) orbits and applying
|a_f(a)|<=d(a)*sqrt(N), the norm mass is still D_odd(c+1/2), requiring
c>3/2. A displacement exponent improvement alone does not automatically
improve this norm exponent. It may improve constants; a useful global
bound must actually evaluate that gain or preserve cancellation across
orbits/Hecke ideals as well.

**Next:** instantiate an effective bound for this (2,2) Cartan harmonic,
including exceptional spectrum, explicit constants, a valid starting
cutoff and uniformity over the necessary translates, or prove a direct
signed Hecke-block estimate. Feed that proved envelope into the displayed
remainder formula and the complete norm sum before enlarging enumeration.
Do not replace the missing proof by a larger finite sample, the observed
square-root fit, another positive-majorant run, or higher cubic precision.

## 5. Reproduction and scope

```sh
python3 dembele/pari/367_nelson_signed_orbit_audit.py --check
```

Root: `dembele/data/computed/nelson_signed_orbit_d97.json`.
The audit binds the D96 provenance, new code, report and bounded runs.
It independently checks all conjugation pairs, 163 exact phase identities,
finite Abel sums, rational finite-prefix inequalities, the derivative
identity and conditional integral bounds. The actual full enclosure is
assembled again and still contains zero. No fitted hypothesis is promoted
to a proved premise.

The successful jobs for 363 and 366 took less than 6.20 seconds each,
including startup, with the 180-second process-group runner and fresh
DOT_SAGE directories. Two earlier transfer attempts failed on Sage/Python
type conversions before producing an artifact; their sources 364/365,
logs and job records are preserved. All computational jobs are finished.
Sources 363--367 and the bound report/artifacts are frozen after the audit.
The corrected D93 endpoints, D95 identification, precision pause and
earlier mathematical certificates remain in force. Exact arithmetic
CM jets, marked curve identification, cubic recognition and the target
field polynomial remain open.
