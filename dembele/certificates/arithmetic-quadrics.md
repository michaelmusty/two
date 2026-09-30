# Arithmetic canonical quadrics (D54)

Date: 2026-09-15. The user explicitly asked to continue beyond the D53
review milestone. This work implements reconstruction, compares independent
truncations, and attempts bounded recognition. It preserves the user's
preference for the Belyi normalization methods and existing analytic engine.

**Status:** 91 numerical canonical quadrics have been reconstructed in the
conditional F-basis of D52. A fixed, short change of differential basis
avoids the unstable long formal-coordinate substitution. No exact curve
or Dembélé field polynomial has been obtained.

## Why long coordinate substitution is unnecessary

Let `f(u) du` be the row vector of the sixteen source differentials.
D52 constructs the intrinsic parameter tau from the highest-vanishing
differential and then `v=lambda*tau`, with

    lambda = 12 * [tau^16]H_13 / [tau^16]H_14.

Write `T` for the matrix of coefficients at orders 0,...,15 of the
*raw differentials*, including the differential Jacobian, after pullback
to tau. Then the intrinsic echelon basis is `f*T^-1`. In the original
analytic coordinate a basis of the F-defined projective canonical space is

    S(u) = f(u) M,       M = T^-1 diag(1, lambda, ..., lambda^15).

The actual F-normalized differentials have one additional common factor
lambda. Dropping that scalar leaves their homogeneous ideal unchanged.
Likewise the coordinate Jacobian is common to all canonical coordinates,
so any homogeneous relation can be recovered using the original u-series
`S(u)`, without substituting hundreds of terms into v.

Only 32 source jets determine T and lambda: 17 output jets plus the
highest vanishing order 15. Script 85 separately checks that this fixed
matrix change gives the same short normalized series as script 83's full
formal pullback. The base change has numerical condition about 849.
The argument retains D52's hypotheses: the exact canonical differential
space and F-rational marking, the indicated jet rank, and nonzero scale
witness must be established. Numerical conditioning alone proves none of
these arithmetic assertions.

## Recovering and checking the equations

[`85_arithmetic_quadrics.py`](../pari/85_arithmetic_quadrics.py) forms all
136 products and recovers the 91-dimensional kernel. The product rank is
45. A fixed choice of 45 pivot monomials normalizes each of 91 equations
by giving its corresponding free monomial coefficient one and its other
free monomial coefficients zero. Those same indices are used in every
comparison. Only the 4,095 nontrivial pivot coefficients enter the reported
coefficient differences; identity rows cannot inflate apparent agreement.

The initial double solves use 256 training and 512 unused jets. Their
scaled pivot matrix condition is about 92,697, explaining why equation
coefficient accuracy can be much worse than a small product residual.

| Double source banks compared | Equation relative difference | Maximum absolute difference |
|---|---:|---:|
| 10240 / 8192 | 2.411e-9 | about 3.2e-7 |
| 12288 / 10240 | 8.994e-11 | 1.189e-8 |

The n=12288 double bank is the already completed D47/D48 Châtelet job.
Its JSON and NPZ were retrieved and checked against remote SHA256 values;
this was read-only retrieval, not a new remote computation.

[`86_precise_quadrics.py`](../pari/86_precise_quadrics.py) repeats the
calculation with FLINT complex-ball polynomials and matrix arithmetic.
It uses 512 source jets and 45 interpolation rows selected from the first
256. The remaining 211 training rows and all later 256 rows are unused
checks. The same interpolation rows are held fixed across banks. Output
coefficients are decimal string pairs, not rounded to binary64.

These balls enclose arithmetic on the supplied values. They do **not**
enclose errors in the geometric input or the omitted infinite-series tail.
The short change of basis uses additional mpmath guard digits, not an
interval proof. In particular a tiny polynomial residual is not a bound
on distance to the true arithmetic curve.

| Source for precise solve | Relative imaginary part | Scaled residual on later 256 jets |
|---|---:|---:|
| native 8192 | 1.483e-11 | 5.041e-17 |
| double 12288 | 7.602e-13 | 1.057e-19 |
| native 12288 | 4.313e-15 | 1.451e-22 |
| native 16384 | 7.117e-21 | 9.525e-28 |

The native 12288 / native 8192 coefficient difference is 2.373e-9.
It is dominated by the older bank and does not establish the accuracy
of the newer coefficients.

A separate fit using only the first 61 jets (with 67 later jets checked)
has interpolation condition 1.10e6, versus 1.90e6 for the original fit.
On the same native n=12288 source the two equation coefficient matrices
differ by 9.70e-16 in relative norm. This checks sensitivity to interpolation
choice, rather than providing another independent differential bank.
At n=16384 the early-jet and later-jet fits differ by 7.31e-21 in relative
norm (maximum absolute difference 9.48e-19). Across native n=16384/12288,
the original fitted coefficient matrices differ by 1.397e-14 in relative
norm (maximum absolute difference 1.852e-12). The independent bank
comparison is dominated by n=12288; the new imaginary parts and variation
between interpolation choices are additional empirical diagnostics,
not a certification of twenty correct digits.

## Native refinement and memory

The local n=12288, 16-column, 50-working-digit run takes 572 seconds.
Its stabilized finite-system residual is below 9.27e-42, but its actual
finite Cauchy defect is 2.15e-17, changed-quadrature defect 2.09e-17,
and independent 275-side infinity-norm defect 1.12e-14. These must not
be described as 42 correct digits of differential coefficients.

A further n=16384 run completed in 1064 seconds. Its stabilized residual
is below 1.36e-41; the actual finite defect is 1.32e-22, independent
49152-node quadrature defect 1.31e-22, and 275-side infinity-norm defect
3.86e-20. Before launching it, scripts 68
and 79 were changed to assemble the dense matrix in Fortran order and
allow LAPACK to overwrite it. A test checks exact agreement of both
assembly layouts, shared matrix/LU storage, and the solved residual.
One n=16384 complex matrix occupies 4 GiB, less than the two 2.25 GiB
matrices used by the earlier n=12288 implementation. The report records
that the overwrite actually occurred; this is an allocation improvement,
not a claim that 4 GiB bounds the entire process's memory.

## Bounded arithmetic searches

[`87_quadric_recognition.py`](../pari/87_quadric_recognition.py) tests
empirical PSLQ candidates. It omits entries within 1e-7 of an integer,
then selects 128 nontrivial coefficients by independent-bank stability.
This prevents the near-minus-one coefficients forced by the osculating
normalization from being reported as new arithmetic information.

The initial search uses Q at height 1000, Q(sqrt(2)) at height 100,
the quartic subfield at height 8, and F at height 4, with absolute
tolerance 1e-13. It finds **zero candidates among 128 entries** in the
native n=12288 equations. This is only a bounded search, not a proof
that these values fail to belong to F.

Two coordinate variants are implemented and also find zero candidates
in the initial n=12288 tests:

1. Replace the power basis by
   `[1, 2*cos(theta), ..., 2*cos(7*theta)]`, `theta=7*pi/16`.
   The recurrence `p_(j+1)=b*p_j-p_(j-1)` is monic and integral, so the
   change from the power basis is unimodular. Exact Sage arithmetic checks
   trace Gram matrix `diag(8,16,...,16)` and discriminant `2^31`.
   Galois acts by signed permutations on the seven nonconstant entries;
   this height bound is thus independent of the chosen embedding.
2. If a normalized equation entry c belongs to pivot monomial p and
   free monomial f, its weight is `h=weight(f)-weight(p)`, where
   `weight(X_i X_j)=i+j`. Under rescaling the parameter by mu it becomes
   `mu^h*c`. Ratios of entries with the same weight cancel this scalar.
   Script 87 fixes an anchor's indices in both banks, and leaves weight-zero
   entries unchanged. The ratio search excludes near-integer results.
   This removes scaling ambiguity but does not guarantee small height.

The two tolerance tests on a single candidate are discovery diagnostics.
Even a numerically persistent relation needs an independent higher-quality
input and exact curve validation. The original Belyi `theta.m` and
`Cext/makek_relfinder.c` were inspected: their denominator chaining and
integral-basis search are useful once adequate input accuracy exists.
Declaring the present inputs to have 50 correct digits merely because
they were serialized at that precision would misuse that recognizer.

Script [`88_pointed_invariant.py`](../pari/88_pointed_invariant.py) also
tests the simplest scale-free pointed jet invariant

    J = A3^2/A2^3 = G3^2/G2^3 = 1/(144*G2).

This depends on the pointed curve and the intrinsic differential line,
not on the remaining scalar in its parameter. It is conditionally in F,
but is not a complete invariant of C. It provides a small diagnostic
separate from the 4,095 equation entries. At n=12288,
`J=-0.00446378840016233395889... - 2.54e-18*i`.
The height-32/64 search at tolerance 1e-15 returns the same single fragile
candidate, with error 3.48e-16. It already fails a ten-times-tighter
tolerance; this is not an accepted recognition.
At n=16384, `J=-0.004463788400162326581798895520... + 3.43e-24*i`;
the change from n=12288 is 7.80e-18. No candidate remains at tolerance
1e-20 for the tested degree-eight height bounds 4,8,16,32,64. In
particular the earlier near-match does not improve with the data.

The broader n=16384 equation searches, at tolerance 1e-18 and degree-eight
height 16, finish with **zero candidates**: all 3,003 eligible nontrivial
entries in the power basis, the same 3,003 in the cosine basis, and 2,933
eligible scale-invariant ratios. These are bounded PSLQ searches with
recorded stopping parameters, not exhaustive arithmetic exclusion proofs.
The Q, quadratic and quartic bounds remain 1000,100,8 respectively.

## Direct equation-space lattice pilot

Script [`89_quadric_lattice.py`](../pari/89_quadric_lattice.py) searches for
small equations directly, avoiding the requirement that each normalized
matrix entry itself have a short rational expression over F. For the
fixed pivot products, let D have the identity in pivot columns and the
negative normalized equation coefficients in free columns. Then an
equation coefficient vector c satisfies `D*c=0`.

Expand c in the cosine integral basis and form the integer lattice
`[I | round(10^17 * D_normalized)]`, scaling each constraint row of D to
Euclidean norm one. There are 136 rows over Q or 1088 rows over F and
45 additional constraint columns. The LLL subprocess has a 180-second
limit. Candidate coefficients are checked at full working precision in
both the early-jet and later-jet reconstructions from n=16384. These
are distinct fits to the same source, not independent geometric banks.

The error metric is `norm(D*c)/(norm(D)*norm(c))` in the given field
embedding. Using the embedded coefficient norm prevents a very small
algebraic unit times an arbitrary monomial from looking like an equation.
The candidate threshold is 1e-20 and integer height is bounded by 64;
the threshold remains empirical, not a geometric enclosure. Exact
controls recover the genus-four quadric, check the field-basis convention,
and reject the small-unit trap.

Both full-space pilots finish without candidates. LLL takes 12.4 seconds
over Q and 176.7 seconds over F. Their best numerical residuals are
1.23e-18 and 4.79e-18; the corresponding integer heights are 23,598 and
129, respectively. Neither meets the two candidate requirements.

The optional `--min-weight m` restricts to monomials `X_i X_j` with
`i+j>=m`. These lie in `H0(2K-mP)`, of dimension `45-m` for the tested
range by Riemann--Roch. The implementation checks this rank numerically
and selects that many constraint rows for the lattice, but validates all
45 original constraints afterward. This gives small arithmetic subspaces
for subsequent coordinate experiments:

| Minimum weight | Monomials | Product rank | Quadric dimension | F lattice rows | LLL seconds | Candidates |
|---|---:|---:|---:|---:|---:|---:|
| 20 | 36 | 25 | 11 | 288 | 7.62 | 0 |
| 22 | 25 | 23 | 2 | 200 | 2.03 | 0 |

The last nonzero/first negligible scaled singular values at weight 22
are about 0.0419/2.23e-16. This is a well-separated numerical pencil,
not an exactly recognized pencil. Its best lattice residual is 5.45e-18
at height 96; at weight 20 the corresponding figures are 4.46e-18 and
106. These bounded negative results do not prove lower height bounds:
LLL is not an exhaustive search for all small vectors.

## What this resolves, and what remains

The D53 next computation is complete: the base quadrics now use the
D52 arithmetic normalization, their coefficients have been compared
across banks, and recognition has actually been attempted. The new
fixed-matrix formulation removes long formal substitution from this
step. Extra working digits are no longer being mistaken for accurate
analytic input. The latest diagnostics improve substantially with n,
and the interpolation choice is checked independently on each bank.

Arithmetic recognition remains unresolved. None of these experiments
supplies exact relations to reduce D53's relative cubic, and the cover's
48 new directions retain their earlier conditioning problem. This does
not justify treating further n-growth as the automatic next task.

A focused next coordinate experiment is the weight-22 quadric pencil.
Its five coefficient functionals on `X7*X15, X8*X14, X9*X13, X10*X12,
X11^2` give marked points on the pencil's parameter line, when nonzero
and distinct. This offers map-defined normalizations and cross-ratios
before another broad precision or height search. A preliminary probe
using the first three coefficient-zero points as 0,infinity,1 gives
cross-ratios about -18.08134 and -9.900885, but these change by about
1.2e-16 and 6.4e-17 between interpolation choices, losing several digits
relative to the full equation space. These are exploratory values, not
recognized invariants. Condition the pencil and its marked points before
attempting to interpret such near-matches arithmetically.

## Reproduction and controls

Run from the repository root, preserving existing output artifacts:

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/85_arithmetic_quadrics.py \
  --output /private/tmp/arithmetic_quadrics_10240.json

DOT_SAGE=/tmp/dembele-d54-sage OPENBLAS_NUM_THREADS=4 \
  sage -python dembele/pari/86_precise_quadrics.py \
  --basis dembele/data/computed/acb_refinement_12288.acb \
  --rows-from dembele/data/computed/precise_quadrics_8192.json \
  --comparison dembele/data/computed/precise_quadrics_8192.json \
  --output /private/tmp/precise_quadrics_12288.json

OPENBLAS_NUM_THREADS=1 sage -python dembele/pari/87_quadric_recognition.py \
  --basis dembele/data/computed/precise_quadrics_16384.json \
  --comparison dembele/data/computed/precise_quadrics_12288.json \
  --samples 4095 --tolerance 1e-18 --field-height 16 \
  --field-basis cosine --scale-invariant \
  --output /private/tmp/quadric_recognition_invariants_16384.json

DOT_SAGE=/tmp/dembele-d54-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/88_pointed_invariant.py \
  --basis dembele/data/computed/acb_refinement_16384.acb \
  --comparison dembele/data/computed/acb_refinement_12288.acb \
  --tolerance 1e-20 --output /private/tmp/pointed_invariant_16384.json

DOT_SAGE=/tmp/dembele-d54-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/89_quadric_lattice.py \
  --basis dembele/data/computed/precise_quadrics_16384.json \
  --comparison dembele/data/computed/precise_quadrics_16384_shortfit.json \
  --min-weight 22 --output /private/tmp/quadric_lattice_weight22_16384.json

DOT_SAGE=/tmp/dembele-d54-sage OPENBLAS_NUM_THREADS=4 \
  sage -python -m unittest discover -s dembele/tests -v
```

The nonhyperelliptic exact control is the smooth genus-four curve
`y^3=x^5-x+1`, at `(0,1)`, with canonical coordinates `[1,x,x^2,y]`
and independently known quadric `X0*X2-X1^2`. It checks reconstruction
after the short change of basis and comparison against the exact
`belyi.pointed_series` formal method. Another test solves an interpolation
system whose distinction at 1e-35 disappears in binary64. Recognition
controls include a known F element, a bounded negative example, refusal
of a nonzero imaginary error, exact field-basis arithmetic and invariance
under complex parameter scaling. All 71 tests pass.

The native n=16384 run was:

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/79_acb_refinement.py \
  --n 16384 --columns 16 --threads 4 --digits 50 \
  --initial dembele/data/computed/cm_differentials_12288_chatelet.npz \
  --comparison dembele/data/computed/acb_refinement_12288.json \
  --output dembele/data/computed/acb_refinement_16384.json
```

Script 79 refuses existing output paths. Its checkpoints and reports,
the precise fits, recognition reports and lattice reports remain in
`dembele/data/computed/`. Detailed reports contain input hashes and
the fixed coefficient/monomial indices. All computations have finished.

The external Belyi checkout and thesis sources have not been edited.
No exact C/Y model, target torsion computation or field polynomial exists.
