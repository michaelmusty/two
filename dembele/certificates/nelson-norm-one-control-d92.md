# D92: complete norm-one enumeration and an infinite-family bound

Date: 2026-09-23. Continuation of
[D91](nelson-hilbert-unfolding-d91.md), authorized by “continue”.

**Result:** fixing the reduced norm removes the large central-unit
covering cost. We enumerate every norm-one class modulo sign through
`A=25,600`: **541 classes**, with an independent exhaustive interval
replay. We then bound the entire omitted norm-one tail of the D91
expression, including its auxiliary ideals and beta powers. In that
normalization, without the common Petersson scalar,

    6193 < S_(1,1)^(norm-one family) < 8443.

This proves positivity of this one infinite subsum. **It does not prove
nonvanishing of the full lift or evaluate a CM tangent.** Other norm
ideals may contribute with either sign. Bounds for the higher derivative
pairs remain too wide for projective jets. The global nonzero Shimizu
test-vector comparison also remains open. No candidate curve equations,
candidate jets or differential banks enter these computations.

## 1. Fix the norm before enumerating

Use the field, maximal order O and CM element beta from D90. Eight
explicit units have linearly independent sign vectors over F2: -1 and
the seven cyclotomic units

    1 + C_1(b) + ... + C_j(b),  j=1,...,7,
    C_0=2, C_1=b, C_j=b*C_(j-1)-C_(j-2).

Their integrality, inverse integrality, norms and signs are checked
exactly. Dirichlet's unit theorem gives size `2^8` for units modulo
squares. The surjective signature map therefore has trivial kernel:
**every totally positive unit is a square**.

Consequently every integral quaternion with totally positive norm
generating the unit ideal can be multiplied by a central unit to give
reduced norm exactly 1. Two such representatives in the same central-unit
class differ only by sign. This is why the norm-one problem needs no
unit parallelepiped.

Write alpha=alpha_parallel+alpha_perpendicular using conjugation by
beta. Put u=Nrd(alpha_parallel), v=Nrd(alpha_perpendicular), so u+v=1.
At the seven compact real places u,v are nonnegative. At the split
place, u=A>=1 and v=1-A. In particular,

    A = cosh(distance(z0,alpha*z0)/2)^2.

For a chosen T, construct rational field elements gamma and eta whose
eight real values approximate

    compact places: gamma=eta=1,
    split place:   gamma=1/(2*T), eta=-1/(2*T)

within relative error epsilon=1/1000. Rational root intervals verify
these inequalities. The exact positive quadratic form

    Q_T(alpha)=Tr_F/Q(gamma*u + eta*v)

then contains every norm-one alpha with A<=T in the ellipsoid

    Q_T(alpha) <= (1+epsilon)*(8-1/(2*T)).

Indeed the seven compact contributions are at most 1+epsilon each;
the split contribution is at most
`(1+epsilon)*(2*A-1)/(2*T)`. Positivity follows from the signs of
gamma and eta and the definite/CM splitting at each place. This
majorant is specific to the fixed norm. It does not contradict D91's
much larger bound for simultaneously reducing all norms.

## 2. Exhaustiveness, not just a list of short vectors

Script 339 reduces the exact rational Gram matrix by a unimodular
change and runs PARI `qfminim` flag 2 at 256 bits. Every returned vector
is retained. The first attempt, frozen script 338, used flag 0 and
failed because its integral matrix entries exceeded that routine's
precision limits. Its source, log and job record remain unchanged.

The [PARI documentation](https://pari.math.u-bordeaux.fr/dochtml/html-stable/Vectors__matrices__linear_algebra_and_sets.html#qfminim)
does not give flag 2 rigorous roundoff tracking. We therefore do not
use it alone as an exhaustiveness certificate. Script 340 performs
a separate Fincke--Pohst recursion:

1. Decompose the reduced Gram matrix as `U^t diag(d_i) U` over Q.
2. Check that every d_i is positive and the matrix identity is exact.
3. At each coordinate, use outward Arb intervals to bound the center,
   remaining radius and entire possible integer range.
4. Test leaves by exact rational arithmetic and retain one sign.

The resulting sets agree exactly with PARI's lists. Removing a saved
vector makes the comparison fail. Interval overestimation can only
add branches; it cannot remove a valid vector.

| T | Ellipsoid representatives modulo sign | Norm-one classes with A<=T | Interval recursion nodes |
|---:|---:|---:|---:|
| 400 | 21 | 13 | 36,305 |
| 1,600 | 112 | 29 | 157,827 |
| 6,400 | 949 | 137 | 783,089 |
| 25,600 | 11,620 | 541 | 3,743,707 |

The largest interval replay took 81.44 seconds including startup,
under the local 180-second limit. No polygon reconstruction or remote
run was necessary. The saved normalizer polygon was inspected, but
none of its numerical completeness assumptions are needed here.

The T=400 classes are the identity and four each at

    A = 77.875966849741966...,
        197.742567566289454...,
        346.638897100603235....

The last four were missing from D91's nine-class norm-one subset.
All four cutoff sets are nested, and are closed under inversion.
The only stabilizer of z0 in O^1 modulo sign is the identity. The
complete T=400 enumeration proves every other orbit point has A>64.

## 3. Finite sums and the first tail bound

Script 341 reuses D91's independently differentiated Gaussian kernel:

    V_a(alpha)=Phi_a/A * [a*K_(a+2)(Z) - rho*K_(a+3)(Z)],
    rho=1-1/A,  Z=Z0*A,  Z0=(4*pi^2)^8/2^62,
    a=1,3,5.

The kernels include `zeta_F(2s)` and
`(1+2^s)/(1-2^(-s-1))`, hence every auxiliary ideal and beta power
in this family. The norm-one Hecke coefficient is 1. We evaluate
480 kernels at 80 distinct exact A-values using the D91 Arb quadrature
and its strip and vertical-tail bounds.

For the infinite quaternion tail, first combine the two shifts:

    a-(1-1/A)*(s+a+2) = -(s+2)+(s+a+2)/A.

On `Re(s)=c`, let B_(c,a,j) bound

    zeta_F(2c) * (1+2^c)/(1-2^(-c-1)) / pi
      * integral_0^infinity
        |(2s-1)*Gamma(s)^16*s^7*(s)_(a+2)*(s+j)| dt.

We use c=3/4, 7/8, 1 and j=2,a+2. The finite integrals are bounded
by interval rectangles of width 1/128 through height 16. For their
remaining tails, [Binet's formula, DLMF 5.9.10_2](https://dlmf.nist.gov/5.9.E10_2)
gives the elementary bound

    |Gamma(c+it)| <= sqrt(2*pi)*exp(1/(12*c))
                     *(c^2+t^2)^((c-1/2)/2)*exp(-pi*t/2).

For completeness, the Binet remainder is bounded by 1/(12*c), using
`0 < 1/(exp(x)-1)-1/x+1/2 < x/12`. The latter follows from the
partial-fraction expansion of coth. Also
`t*atan(t/c) >= pi*t/2-c`. For 1/2<c<=1 the resulting Gamma product
is bounded by `8^8*exp(4/(3*c))*P(t)*exp(-24*t)` for an explicit
polynomial with nonnegative coefficients. Integrating its monomials
is exact apart from enclosed real exponentials. These vertical tails
are below 1e-100 before the other factors.

The elementary disk-packing count `N(T)<=(32/7)*T` gives an initial
tail bound. At T=25,600 it is still greater than 9,144 for `(1,1)`.
The small changes between successive partial sums alone do not
establish convergence to the displayed digits.

## 4. A sharper bound from positive disk averages

Here is the improvement implemented by script 342. The minimum
displacement result makes hyperbolic disks of radius `r=acosh(8)`
about the norm-one orbit points disjoint. In disk coordinates their
squared radius is u=7/9. Put

    f_p(w)=(1-|w|^2)^(p+1)=A(w)^(-p-1),  p>0.

Moving a disk centered at an orbit point w to the origin expresses
its angular average as the positive series

    sum_(n>=0) [((p+1)_n/n!)^2 * |w|^(2*n) * |v|^(2*n)].

This follows by multiplying the convergent binomial series for
`(1+conjugate(w)*v)^(-p-1)` and its conjugate and integrating the
angle; only equal powers survive. Hyperbolic area in the variable
`x=|v|^2` is `4*pi*dx/(1-x)^2` after angular integration.

For an orbit point with A>T, we have `|w|^2>=1-1/T`. Integrating only
the first 129 positive terms and using

    (1-x)^(p-1) >= L_p,
    L_p=1 if p<=1, otherwise (2/9)^(p-1),

gives a lower bound `4*pi*f_p(w)*L_p*S_p(T)` for its disk integral,
where the following sum is rational for the p used here:

    S_p(T)=sum_(n=0)^128
      ((p+1)_n/n!)^2 * (1-1/T)^n * (7/9)^(n+1)/(n+1).

Every such disk lies outside the radius `R(T)-r`, whose A-value is

    A_-(T)=[8*(2*T-1)-2*sqrt(63*T*(T-1))+1]/2.

Their interiors are disjoint. Integrating f_p over this outer region
therefore proves

    sum_(A>T) A^(-p-1)
      <= M_p(T) := A_-(T)^(-p)/(p*L_p*S_p(T)).

All quantities are positive, so truncating the angular series in this
direction is safe. This proof and the fixed-norm majorant are local
derivations; they are not claimed as results quoted from Nelson.

The derivative tail is consequently at most

    Z0^(-c) * [B_(c,a,2)*M_c(T)
                 + B_(c,a,a+2)*M_(c+1)(T)].

Take the smallest of the three independently valid contour bounds.
The rational audit checks each angular sum and the algebraic-power
inequalities in M_p by exact integer powers. No numerical asymptotic
orbit-density estimate is used.

## 5. What the control establishes

| T | Partial S_(1,1) | Rigorous absolute omitted-family bound, rounded up |
|---:|---:|---:|
| 400 | 7319.9905962970 | 26,979 |
| 1,600 | 7310.7110017574 | 9,523 |
| 6,400 | 7316.8998750533 | 3,366 |
| 25,600 | 7317.7436102796 | 1,125 |

The unrounded final bound is below 1124.696. Including numerical
rounding gives a real enclosure contained in `[6193,8443]`. The sum
is real because inversion conjugates its `(1,1)` terms. The proof
applies to the full infinite norm-one family, not only the 541 terms.

For comparison, the final `(3,1)` partial sum is approximately
`-68.046 + 46.271*i`, with absolute tail below 21,356. The `(5,1)`
partial sum is approximately `44640.738 - 112930.007*i`, with tail
below 832,412. These bounds do **not** give useful derivative ratios.
The many digits in the finite kernel enclosures are not digits of
the completed sums.

The immediate next computation should extend the fixed-norm search
to the prime of norm 31 with **b=27 mod31**. Its quartic Hecke
polynomials are already saved, so this is a first nontrivial weighted
control without rebuilding T31. Choose a totally positive generator
n; at compact places replace the target weights by 1/n_v, and at
the split place by `+/- Norm(n)/(2*T*n_0)`. The same argument gives
cutoff `(1+epsilon)*(8-Norm(n)/(2*T))` for
`A=Norm(n)*sigma_0(u/n)<=T`.

Before treating the resulting family as completed, establish its
norm-one coset decomposition or another valid orbit-tail argument.
The b=10/20/21 Hecke coefficients needed by the old subset remain
missing, as do coefficients and a tail estimate covering all other
norm ideals. A larger norm-one cutoff alone does not resolve these
issues. Finish the global nonzero test-vector identification before
calling the assembled expression a differential value. D88's exact
jet criterion, the marked curve identification, the cubic coefficient
recognition and the target field polynomial remain later tasks.

## 6. Reproduction and provenance

```sh
python3 dembele/pari/343_nelson_norm_one_audit.py --check
```

Root: `dembele/data/computed/nelson_norm_one_d92.json`, with 51 hashes.
The standard-Python audit independently replays exact field/quaternion
arithmetic, all four majorants, all 12,702 ellipsoid representatives
and their classifications, unit signatures, LDL identities, nesting,
inverse pairing, rational disk-average sums and interval containment.
The exhaustive Arb recursion and analytic Gamma/zeta integrals are
hash-bound to their successful runs; this checker does not rerun them.

Scripts 338--343 and their bound artifacts are frozen. The manifest
records twelve bounded computational jobs: eleven passes and the
preserved flag-0 failure. The longest is 81.44 seconds. The separate
root-audit generation job also passed in 4.81 seconds. Every job uses
the process-group timeout runner. No remote computation, upload,
larger cubic precision, or candidate-model change occurred.

The key new artifacts are `nelson_norm_one_d92_T*.json`,
`nelson_norm_one_coverage_d92_T*.json`,
`nelson_norm_one_sum_d92_T25600.json`, and
`nelson_norm_one_packing_tail_d92.json`. D90/D91 bound sources and
results remain unchanged. Decisions, references and entry documents
are updated at this checkpoint.
