# D93: the norm-31 family and the remaining global accuracy problem

Date: 2026-09-23. Continuation of
[D92](nelson-norm-one-control-d92.md), authorized by “continue”.

**Result:** the fixed-norm method works for the prime `(31,b-27)`.
There are **586 classes modulo sign through A=25,600**, with an
independent exhaustive coverage proof. An exact finite-ring calculation
proves that the entire norm-31 family consists of **32 right norm-one
orbits**. This gives a rigorous infinite-family bound, and the saved
quartic Hecke polynomial supplies its coefficient without a new Hecke
computation.

We also prove absolute convergence and an explicit bound for all other
norm ideals in the D91 expression. That bound is **less than 2.685e16**,
against a current two-family partial sum of about **7640.758**. It gives
no useful CM accuracy. Even the completed two-family enclosure contains
zero. The global nonzero Shimizu test-vector identification remains open;
these are bounds for the specified formal expression, not an identified
differential or CM tangent.

The final audit also found and corrected an interval-export error:
`QQ(MPFR_endpoint)` need not preserve the directed endpoint. Five new
analytic replays use exact dyadic endpoints and preserve the reported
numerical conclusions. Use the corrected artifacts and final audit
listed below. Original sources, outputs and failed checks are retained.

## 1. Normalize the prime norm and prove coverage

The saved Hecke input is at **b=27 mod31**. Its generator is

    g = 1 + 2*b - 4*b^3 + b^5.

Among the eight roots of the field polynomial modulo 31, only 27
annihilates g. A unit correction, checked exactly, gives the totally
positive generator

    n = b^6 + b^5 - 6*b^4 - 6*b^3 + 8*b^2 + 9*b + 3,
    Norm(n) = 31.

D92's full unit-signature rank proves that every totally positive unit
is a square. Thus every central-unit class with norm ideal `(n)` has a
representative of reduced norm exactly n, unique modulo sign. Choosing
the displayed positive generator uses a finite search among square-unit
adjustments; optimal balancing is not required for coverage.

For the CM splitting alpha=alpha_parallel+alpha_perpendicular, put
u=Nrd(alpha_parallel), v=Nrd(alpha_perpendicular). Then u+v=n and

    A = 31*sigma_0(u/n) = 31*cosh(distance(z0,alpha*z0)/2)^2.

Construct rational weights gamma, eta such that n*gamma and n*eta
approximate 1 at all seven compact places and `+/-31/(2*T)` at the
split place, within relative error 1/1000. Every class with A<=T lies
in the positive rational ellipsoid

    Tr(gamma*u + eta*v) <= (1.001)*(8 - 31/(2*T)).

Script 344 enumerates that ellipsoid using PARI flag 2. Script 345
independently repeats the full search by D92's outward Arb recursion,
exact rational LDL decomposition and exact leaf tests. Its integer
branch endpoints use MPFR ceil/floor directly, so the analytic-export
issue below does not affect coverage.

| T | Ellipsoid representatives modulo sign | Norm-31 classes | Interval recursion nodes |
|---:|---:|---:|---:|
| 6,400 | 890 | 170 | 675,068 |
| 25,600 | 11,568 | 586 | 4,334,720 |

The larger exhaustive replay took 94.44 seconds rounded up, within the
180-second process-group limit. The class counts at A=400 and 1600,
obtained by filtering the complete lists, are 8 and 60.

## 2. Exactly 32 norm-one orbits

Script 346 constructs an explicit surjective ring map

    rho: O -> M_2(F_31),  kernel = n*O,

using b=27, hence b-b^2=11, in the quaternion presentation. The images
of i and j satisfy i^2=11, j^2=-1 and ij=-ji. The computation checks
all 1,024 products of the saved 32 integral basis elements. The image
has dimension 4 and `[O:nO]=31^4`, which proves the kernel assertion.

If Nrd(alpha)=n, the right ideal alpha*O contains n*O and has index
31^2. Its image consists of the matrices whose columns lie in the
one-dimensional image of rho(alpha). There are 32 such lines. Two
elements alpha and alpha_i with the same line therefore generate the
same right ideal; gamma=alpha_i^(-1)*alpha lies in O and has reduced
norm 1. Its conjugate is its inverse, so gamma is a norm-one unit.
Conversely right multiplication by a norm-one unit preserves the ideal.

All 32 lines already occur at A<=6400. For each representative the
certificate stores the integral left-multiplication matrices for
alpha_i and its conjugate, their product n*I, determinant 31^2 and
finite ideal image. Every one of the 586 classes has an exact witness
`alpha=alpha_i*gamma`, with integral gamma of norm 1. This proves the
classification of the whole infinite family, not just the finite list.

Each orbit alpha_i*(O^1/{+1,-1})*z0 is an isometric image of the D92
norm-one orbit. Its disks of radius acosh(8) have disjoint interiors.
Disks from different orbits can overlap: we apply the bound separately
and sum 32 bounds. No principal-ideal or class-number shortcut is used.

## 3. Evaluate and bound the weighted prime family

Retain the D91 Gaussian normalization, with no common Petersson scalar:

    Z0 = (4*pi^2)^8/2^62,
    rho = 1-31/A,
    V_a(alpha) = Phi_a/A * [a*K_(a+2)(Z0*A) - rho*K_(a+3)(Z0*A)],
    a = 1,3,5,   |Phi_a| <= 1.

The kernels still include every auxiliary ideal via zeta_F(2s), and
every beta power and both cusps via `(1+2^s)/(1-2^(-s-1))`.
There are 83 distinct A-values and 498 scalar kernel evaluations.
The finite quadrature uses 320-bit Arb balls, step 1/32 and height 16,
with the D91 strip and vertical-tail proofs.

Let M_p(t) be D92's positive disk-average moment bound, now allowing
the rational cutoff t=T/31>9/2. Explicitly,

    A_-(t) = [8*(2*t-1) - 2*sqrt(63*t*(t-1)) + 1]/2,
    S_p(t) = sum_(j=0)^128 ((p+1)_j/j!)^2*(1-1/t)^j*(7/9)^(j+1)/(j+1),
    L_p = 1 (p<=1), or (2/9)^(p-1) (p>1),
    M_p(t) = A_-(t)^(-p)/(p*L_p*S_p(t)).

The 32-orbit decomposition proves

    sum_(A>T) A^(-p-1) <= 32*31^(-p-1)*M_p(T/31).

Writing the derivative factor as
`a-rho*(s+a+2)=-(s+2)+(31/A)*(s+a+2)` gives the family tail bound

    E_a(c,T) = 32*31^(-c-1)*Z0^(-c)
                  *[B_(c,a,2)*M_c(T/31) + B_(c,a,a+2)*M_(c+1)(T/31)].

The B constants are the absolute Mellin integrals defined and bounded
in D92. Take the smallest valid bound for c=3/4,7/8,1. Quaternion
conjugation pairs the `(1,1)` terms with their complex conjugates, so
that sum is real.

| T | Classes | Unweighted partial S_(1,1) | Absolute tail, rounded up |
|---:|---:|---:|---:|
| 400 | 8 | -41.9922179439 | 29,560 |
| 1,600 | 60 | -41.6935180130 | 9,991 |
| 6,400 | 170 | -44.0710986751 | 3,489 |
| 25,600 | 586 | -44.1638104089 | 1,163 |

The final unrounded prime-family error is below 1162.373. Higher-pair
partial sums are approximately `580.268-394.582*i` and
`-1433.231+3625.718*i`; their errors are below 22,084 and 861,438.
Digits shown describe the finite sums, not the completed families.

The first saved quartic Hecke orbit has polynomial

    x^4 - 8*x^3 - 36*x^2 + 433*x - 899,

and U_p2=+1. Its four real roots are approximately
`-7.3140105084, 3.9471584106, 4.6058065759, 6.7610455219`.
All four weightings are stored. Selecting the smallest root, the
combined norm-one and prime-family `(1,1)` partial sum is
**7640.7581837028**, with total omitted-family error **less than
9626.300**. This enclosure contains zero. The earlier positive
norm-one subsum remains valid, but does not prove positivity after
other norm ideals are included.

## 4. Bound every remaining norm ideal

For ideals a coprime to p2, the arithmetic Hecke normalization satisfies

    |a_f(a)| <= d(a)*sqrt(Norm(a)).

This follows from the finite-place Ramanujan theorem and the Hecke
recurrences. Parallel weight two satisfies the hypotheses of
[Blasius, Theorem 1 and section 2.2](https://arxiv.org/pdf/math/0511007).
We use this theorem only for coefficient bounds; it does not identify
our Schwartz function or its Shimizu lift.

At an unramified prime of residue size q, right ideals in M_2(O_v)
correspond to rank-two sublattices. Hermite normal forms count
`1+q+...+q^e` at norm q^e. Taking the product of local counts bounds
the number of right norm-one orbits at norm ideal a by sigma_1(a).
Only principal represented ideals contribute, so counting all right
ideals is an upper bound regardless of their ideal classes. A
represented family supplies a positive norm generator, and D92's
positive-unit square argument supplies its normalization. Powers of p2
have already been included in the beta factor.

The same disjoint disks give a useful uniform whole-orbit inequality.
For any isometric image of the norm-one orbit, and u>0,

    sum_gamma D_gamma^(-u-1) <= C_u := 1/(1-(2/9)^u),
    D_gamma = cosh(distance(z0,gamma*z0)/2)^2.

Indeed the disk angular average has constant term 1 and all remaining
terms nonnegative. Its radial integral is at least
`4*pi/u * (1-(2/9)^u)` times the value at the center. The integral
over the whole hyperbolic plane is `4*pi/u`. Disjointness proves the
inequality, independently of the orbit's position relative to z0.

The divisor majorant can be summed by Euler products. For s>2 put

    D_odd(s) = sum_((a,p2)=1) d(a)*sigma_1(a)*Norm(a)^(-s)
             = zeta_F(s)^2*zeta_F(s-1)^2/zeta_F(2*s-1) / F_2(2^(-s)),
    F_q(x) = (1-q*x^2)/((1-x)^2*(1-q*x)^2).

The local identity is obtained by differentiating
`x/((1-x)*(1-q*x))`. With A=Norm(a)*D and Norm(a)/A<=1, the
absolute sum for derivative pair `(a,1)` is bounded on c>3/2 by

    Z0^(-c)*(B_(c,a,2)+B_(c,a,a+2))*C_c*D_odd(c+1/2).

This proves absolute convergence of the D91 formal expression.
Removing the norm-one ideal and the single computed norm-31 prime
replaces the final factor by

    D_odd(c+1/2) - 1 - 64*31^(-c-1/2).

Here 64=2*32 is the divisor/orbit majorant for one prime, not all eight
primes above 31. Script 348 bounds the B constants on c=2,3,4 using
Arb interval rectangles and the integer-contour Gamma recurrence tail.
For `(1,1)` the best resulting omitted-ideal bound is approximately
**2.684968450243612e16**. Higher derivative bounds are larger.

For a hypothetical enumeration of **every** class with A<=T, any
3/2<u<c also gives the global A-tail bound

    Z0^(-c)*(B_(c,a,2)+B_(c,a,a+2))
       * T^(u-c)*C_u*D_odd(u+1/2).

| Hypothetical complete cutoff T | `(1,1)` global A-tail bound, rounded up |
|---:|---:|
| 25,600 | 2.237e16 |
| 10^6 | 8.945e15 |
| 10^8 | 2.829e15 |
| 10^10 | 8.945e14 |
| 10^12 | 2.829e14 |
| 10^14 | 7.097e12 |

**None of these is a completed all-ideal enumeration.** Only the
norm-one and one norm-31 family were evaluated. These are weak upper
bounds, not lower bounds on the actual error or evidence that the
method is impossible. They explain why extending the current cutoff
or coefficient bank alone is not yet justified as a route to accuracy.

## 5. Correct the endpoint exports and preserve provenance

The first standard-Python audit, frozen script 349, rejected an
endpoint-product comparison at about 1e-94. Script 350 refined the
algebraic Hecke root intervals and passed. A subsequent direct API
check exposed a broader problem in the original serializer:
`QQ(value.lower())` and `QQ(value.upper())` choose simple rationals
that can lie inward of the directed MPFR endpoints. A passing 350
audit alone therefore does not certify those serialized enclosures.

[Sage's MPFR documentation](https://doc.sagemath.org/html/en/reference/rings_numerical/sage/rings/real_mpfr.html#sage.rings.real_mpfr.RealNumber.exact_rational)
specifies exact rational extraction separately. Script 351 replays
333, 341, 342, 347 and 348 with
`value.lower().exact_rational()` / `value.upper().exact_rational()`.
Each stage consumes corrected dependencies. Import checks prove that
reconstructed Arb balls contain their saved rational intervals. A pi
regression control explicitly demonstrates the original inward movement.

The new files append `_exact_d93` before `.json`. They supersede the
analytic endpoints in `nelson_interval_sum_d91.json`,
`nelson_norm_one_sum_d92_T25600.json`,
`nelson_norm_one_packing_tail_d92.json`, `nelson_prime31_sum_d93.json`
and `nelson_all_ideal_bounds_d93.json`. Original files remain unchanged.
Script 352 exposed the malformed old zero-radius record; 353 exposed
a too-strict comparison of broad error enclosures. Those attempts are
preserved. Arb rounds radii separately from its high-precision midpoints,
so revised exact inputs can move a broad enclosure by a radius ulp.
The final audit compares those diagnostics at their radius scale and
certifies the corrected bounds independently. The new values agree
with the old ones more closely than the precision reported here; exact
endpoint fidelity is nevertheless required for an enclosure certificate. Algebraic root isolation,
exact arithmetic and the exhaustive enumeration remain valid.

The governing audit is:

```sh
python3 dembele/pari/354_nelson_prime31_certified_audit.py --check
```

Its root is `dembele/data/computed/nelson_prime31_exact_d93.json`,
with 115 file hashes and 11,046 corrected interval records. It replays
the exact prime classification, 32 ideal representatives,
586 norm-one witnesses, rational moment inequalities and corrected
analytic-output checks. It also verifies every corrected endpoint is
dyadic and reconstructs the final selected-family component enclosures
by exact fraction arithmetic. Arb quadrature nodes and exhaustive
recursion are bound to their successful runs; the standard-Python
checker does not rerun them. The analytic proofs are given above.

Eight original computational jobs and five exact-endpoint replays
passed. Three failed audit attempts, the intermediate passing 350 audit
and the final passing 354 audit are preserved separately. The largest
computation took less than 94.44 seconds. Scripts 344--354 and their bound artifacts are frozen.
No candidate curve equations or candidate differential banks enter
the evaluator. No remote run, new Hecke computation or higher cubic
precision was used.

## 6. Next step toward the curve and field

The arithmetic enumeration and norm-orbit decomposition now work.
The unresolved numerical task is a sharp **global** sum, especially
for derivative ratios. Before a larger enumeration or Hecke rebuild,
review the Mellin test function and global summation strategy to find
a demonstrably useful omitted-term bound. Separately establish that
the exact finite and infinite Schwartz factors give a nonzero Shimizu
lift in the chosen level-p2-new eigenline, with the asserted derivative
normalization. A finite sum with small quadrature error does not settle
either requirement.

The D91 arXiv-v1 derivative-scale caveat remains: independently
differentiated Gaussian identities govern the implementation, and the
published display was not checked. A future continuation must use
exact endpoint exports rather than the old default QQ conversions.

Once an identified evaluator gives independent arithmetic CM jets,
D88's criterion can certify the base and markings, after which its
conditional cubic argument becomes applicable. Those jets, marked
identification, cubic coefficient recognition and the explicit target
field polynomial remain open. The present bound does not justify a
further cubic precision increase.
