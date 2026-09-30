# CM-normalized global functions on the genus-16 curve (D56)

Date: 2026-09-16. User instruction: pursue a concrete arithmetic description
of a useful map or function on this particular curve, with preference for
their Belyi code and thesis where applicable.

**Result:** there is now an intrinsic prescription for two global
functions X and Y, using the distinguished CM point and the seventeen
order-two CM points. Subject to the ordinary-point and nonvanishing
hypotheses below, they are F-defined, have sole poles 17P and 18P, and
generate F(C). Scripts 91–92 construct numerical representatives and
check their invariance under a change of differential basis. This is
more specific than the previous local coordinate or pencil invariant.

**Limit:** no exact coefficients have been recognized. Script 93's
attempts to recover a plane equation all fail their unweighted validation
rows. A favorable singular-value gap alone gives a false impression here.
The saved failed coefficients are not equations or height estimates.

## Arithmetic input and hypotheses

Continue with F=Q(zeta_32)^+, the genus-16 normalizer quotient C, and its
unique order-32 elliptic CM point P. The canonical-model interpretation
and F-rationality of P are the same as in
[pointed-normalization.md](pointed-normalization.md).

Let D be the reduced sum of the seventeen order-two elliptic CM points.
It is an F-rational divisor. One way to see this is to use the canonical
degree-two map from the genus-40 norm-one curve to C: its branch divisor
is D+P. The stabilizer indices are two at these eighteen points and one
at the order-three points. Subtracting the F-rational point P gives D.
The ramification count also satisfies 2*40-2=2*(2*16-2)+18.
The relevant signatures are computed in Dembélé's
[Theorem 5.1](https://arxiv.org/pdf/1906.06772), independently of the
later hyperellipticity claim contradicted by our D45 audit.

The construction assumes that P is ordinary, so the canonical vanishing
sequence is 0,...,15. It then has

    L(16P) = <1>,  dim L(17P)=2,  dim L(18P)=3.

Choose any x in L(17P) outside the constants, and y in L(18P) outside
L(17P). The trace moments used below must be nonzero. These are exact
hypotheses; the present numerical calculations support them without
certifying them. The functions' definition does not depend on D52's
formal-coordinate scale or on choosing an F-basis numerically.

## Recover the functions by section multiplication

Take holomorphic differentials a and b of orders 15 and 14 at P. For
m=16,17,18, look for pairs

    A in H^0(2K-(30-m)P),  B in H^0(2K-(28-m)P)
    satisfying A*b^2 = B*a^2.

If a and b have no common zero away from P, their common quotient

    f=A/a^2=B/b^2

has poles only at P, of order at most m. Conversely, every f in L(mP)
gives such a pair. Thus a multiplication-kernel computation recovers
the required Riemann–Roch space without locating the differential zeros.
The known constant pair is (a^2,b^2); setting its first A coefficient to
zero removes the constants from the numerical kernel.

There is also a dimension check on the possible extra common divisor.
If gcd(div(a),div(b))=14P+E with E disjoint from P, the kernel for m=17
identifies with L(17P+2E). Riemann–Roch gives dimension at least
2+2*deg(E). Therefore dimension two for the full kernel implies E=0.
This implication is exact; the measured dimension is still numerical.

The relation is a section of 4K, of degree 120. Consequently 121 exact
vanishing jets would prove it. The main fit uses 256 jets, an alternative
fit uses 121, and both are checked through 512 jets. The native
n=16384 and n=12288 checkpoints supply separate truncation comparisons.

| m | Dimension of A-space | Dimension of B-space | Columns after removing constants | Measured rank | Dimension including constants |
|---|---:|---:|---:|---:|---:|
| 16 | 31 | 33 | 63 | 63 | 1 |
| 17 | 32 | 34 | 65 | 64 | 2 |
| 18 | 33 | 35 | 67 | 65 | 3 |

Script 91 selects independent quadratic products from the appropriate
vanishing flag. It checks their ranks against Riemann–Roch dimensions;
it does not assume that products of individually high-order forms always
span the desired space. An exact genus-four negative control demonstrates
why this check is necessary.

The arithmetic-basis m=17 solve has last nonzero relative singular value
2.03e-8 and first null value 2.93e-17. Its unscaled interpolation matrix
has condition about 2.62e10. Map-coefficient differences between the two
checkpoints are about 1.1e-13 to 3.4e-13; changes of interpolation rows
on a single checkpoint are about 1e-18 to 4e-18. The much smaller
reported backward residuals do not bound coefficient accuracy.

## Fix the arithmetic normalization by CM traces

For a function regular along D, write

    E(f) = (1/17) * sum_{Q in D} f(Q).

This is the algebraic trace on the degree-17 divisor, not a Hermitian
average: there is no complex conjugation. Define

    mu = E(x),  M2 = E((x-mu)^2),  M3 = E((x-mu)^3),
    X = (M2/M3)*(x-mu).

Next define

    nu = E(y),  beta = E((y-nu)*X)/E(X^2),
    z = y-nu-beta*X,
    N2 = E(z^2),  N3 = E(z^3),
    Y = (N2/N3)*z.

Require M2, M3, N2, N3 to be nonzero. The defining conditions become

    E(X)=E(Y)=E(XY)=0,
    E(X^2)=E(X^3),  E(Y^2)=E(Y^3).

Replacing x by a*x+b multiplies its centered moments by a^2 and a^3,
so X stays unchanged. Replacing y by c*y+d*x+e changes z to c*z and
leaves Y unchanged. These exhaust the changes of generators of the
two Riemann–Roch spaces. No root choice remains.

To prove descent, choose x and y over F initially. All the traces and
the displayed rational operations are then over F because P and D are
F-rational. Invariance shows that starting with an arbitrary complex
basis gives the same X and Y. Thus the numerical basis need not itself
be F-defined. The nonvanishing assumptions are essential; a test with
a zero third moment explicitly refuses normalization.

The poles are exactly 17P and 18P. Therefore

    [F(C):F(X)] = 17,  [F(C):F(Y)] = 18.

The degree [F(C):F(X,Y)] divides both, so **F(C)=F(X,Y)**. Moreover
t=X/Y has a simple zero at P and is an F-defined global rational
uniformizer there. This does not assert that its Taylor coefficients in
the original complex disk coordinate belong to F.

The polynomial product_{Q in D}(T-X(Q)) is another specific arithmetic
object: a monic degree-17 polynomial over F. Script 92 saves its numerical
coefficients. It has not been recognized in F.

These are maps of curves, not asserted Belyi maps. A degree-17 Belyi map
cannot have genus 16: Riemann–Hurwitz for three branch values gives
d>=2g+1=33. The useful borrowing from the Belyi work is divisor-based
construction, arithmetic normalization, and exact control examples.

## Actual CM evaluations and comparisons

Script 92 obtains the CM points from the seventeen saved elliptic
generators in `expansion_geometry.json`. It evaluates the full native
differential checkpoint near each point. Because the pulled-back
differentials vanish at an elliptic fixed point, it uses eight-point
circular averages at radii delta and delta/2, with delta at most 1e-5,
and compares both denominator charts. These are empirical checks,
not certified removable-singularity or tail estimates.

An initial proposed shortcut was div(x-c)=D-17P. It would force all
seventeen x-values to agree. In the arithmetic basis their spread is
22.8075, versus largest measured discrepancy 6.87e-12. Thus that
particular fiber proposal is incompatible with the numerical data.
The trace normalization still uses D successfully.

| Comparison | Maximum change in normalized X-values | Maximum change in normalized Y-values |
|---|---:|---:|
| Arithmetic basis versus complex flag basis, same checkpoint | 1.94e-17 | 5.34e-17 |
| n=16384 versus n=12288, flag basis | 1.25e-12 | 1.86e-12 |
| 256-jet versus 121-jet fit, flag basis | 1.12e-17 | 1.98e-17 |
| delta versus delta/2, flag basis | 4.38e-23 | 9.84e-23 |

The first row tests independence from D52's normalization. It is not an
independent analytic approximation: both bases use the same checkpoint.
The CM value polynomial changes by 2.16e-11 across checkpoints.
Uniformizer coefficients grow to about 5.45e30 through order 31, so
absolute differences alone are misleading; the basis-change comparison
there is 1.27e-16 in relative Euclidean norm.

## Conditioning and the rejected plane equations

Script 93 first scans rational parameters 2^e*X/(Y+c*X), with seven
nearby integer c values and -5<=e<=5. The coefficient of u in u/t is
approximately -3.01942015941633. The best trial is c=3, e=0:

| Parameter | Condition of first-16 canonical jet matrix, double estimate |
|---|---:|
| X/Y | 7.27e20 |
| X/(Y+3X) | 1.72e10 |

This is a substantial improvement within this family, but the previous
D52 normalization has condition about 849. The new parameter should
not automatically replace that better-conditioned local calculation.

For a direct plane model, the coprime pole degrees give a relation
supported on the 172 monomials X^i*Y^j with 17i+18j<=306. Its leading
terms include X^18 and Y^17. Script 93 clears the common denominator
before multiplying, to avoid long division of Laurent series:

    X=Nx/D0, Y=Ny/D0, D0=a^2,
    ord_P(Nx)=13, ord_P(Ny)=12, ord_P(D0)=30.

Put U=Nx/u^13, V=Ny/u^12 and W=D0/u^30. After removing a common
factor u^234, the columns are

    u^(306-17i-18j) * U^i * V^j * W^(18-i-j).

The relation is unique up to scale when the functions really have the
stated poles. All monomials other than one of the leading pair have
distinct pole orders, so fitting those leading rows is triangular.
There are 171 interpolation rows, 136 unused rows through order 306,
and 205 further checked rows. The shifted triangular fit has maximum
scaled residuals 0.823 on unused rows and 1.0 on later rows: it fails.

Two balanced fits also fail. They weight row n by rho^n, normalize
columns, select interpolation rows and columns with QR, solve using
80-digit ball arithmetic, undo column scaling, and validate in the
original unweighted rows. The fitting window is 384 jets and the full
window is 512.

| Y-coordinate | Row radius | Measured rank at 1e-12 | Last singular gap | Maximum unused / held-out scaled residual |
|---|---:|---:|---:|---|
| Y | 0.25 | 163 instead of 171 | — | No balanced fit attempted |
| Y+3X | 0.25 | 171 | 9.14e12 | about 1 / 1 |
| Y+3X | 0.50 | 171 | 8.65e5 | 0.99962 / 0.99854 |

Residuals divide each unweighted coefficient error by the sum of
absolute monomial contributions in that row. Very small residuals in
the weighted matrix coexist with these failures. The fitted coefficient
vectors also differ by about 1.17e5 in relative norm across checkpoints.
They cannot be accepted or used to estimate arithmetic heights. The
code labels each failed fit explicitly as rejected.

The older unshifted and shifted diagnostic reports are retained as
exploratory records. `pointed_map_model_balanced3_16384.json` is the final
report with the rejection screens. No arithmetic recognition was run
on rejected equation coefficients.

## Reuse, controls, and provenance

The user's [thesis](https://michaelmusty.github.io/assets/musty_thesis_final.pdf),
Chapter 5, motivates constructing functions from divisors. Its tower
algorithms require an already known function field, Picard arithmetic,
and branch data; they do not directly provide the missing model of C.
The section-multiplication viewpoint is also related to Khuri-Makdisi's
[linear algebra for divisors](https://arxiv.org/abs/math/0105182), section 3.
The trace prescription above is derived here; it is not attributed to
either source as an existing algorithm for this curve.

The six new tests in `dembele/tests/test_pointed_map.py` include:

- A smooth genus-six trigonal control y^3=x^7-x+1. The recovered
  degree-seven function is checked against an independent exact
  pole-cancellation construction over Q(zeta_3), agreeing through
  fourteen Laurent coefficients up to its allowed affine freedom.
- A rank-deficient genus-four example which must be refused.
- The actual thesis Q8 curve y^2=16*x^5-x, loaded from
  `belyi/validate_q8.sage`. At (1,sqrt(15)), the functions
  (y+T2)/(x-1)^3 and (y+T3)/(x-1)^4 give an exact one-pole control;
  Tj is the order-j Taylor polynomial of the positive local branch.
  Their normalization over the five finite branch points is exact.
- Exact invariance under complex triangular generator changes, and
  refusal of a zero third moment.
- An exact weighted plane relation on the Q8 curve, checked on unused
  jets. The balanced numerical solver agrees with it; perturbing only
  a held-out coefficient makes the validation reject it.

The controls reuse `belyi/pointed_series.py` and the thesis model.
The external `/Users/musty/Belyi` checkout was inspected, not edited.
All 84 tests pass. The eight saved JSON/out pairs agree byte-for-byte,
and all eight distinct referenced source hashes have been checked.
The complete test output is preserved in
[`pointed_maps_tests_20260916.out`](../data/computed/pointed_maps_tests_20260916.out).

From the repository root, using temporary output stems:

```sh
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/91_pointed_map.py --basis-gauge flag \
  --output /private/tmp/pointed_map_flag.json
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/92_cm_fibers.py \
  --map /private/tmp/pointed_map_flag.json \
  --output /private/tmp/cm_pointed_maps_flag.json
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/93_pointed_map_model.py \
  --cm-report /private/tmp/cm_pointed_maps_flag.json --y-shift 3 \
  --output /private/tmp/pointed_map_model_balanced3.json
DOT_SAGE=/tmp/dembele-d56-sage OPENBLAS_NUM_THREADS=1 \
  sage -python -m unittest discover -s dembele/tests -v
```

For the arithmetic-basis comparison, run script 91 with
`--basis-gauge arithmetic`, then script 92 on that report. Script 93
accepts `--y-shift 0` to reproduce the unshifted equation experiment.
The saved reports include source hashes and identical `.out` copies:

- `pointed_map_{flag_,}16384.{json,out}`;
- `cm_pointed_maps_{flag_,}16384.{json,out}`;
- `cm_pointed_maps_comparison_16384.{json,out}`;
- `pointed_map_model_16384.{json,out}`;
- `pointed_map_model_shift3_16384.{json,out}`;
- `pointed_map_model_balanced3_16384.{json,out}`.

## What this resolves and what remains

The functions now have a precise arithmetic identity: their pole
divisors and CM trace conditions determine them. Coordinate freedom is
no longer an unspecified obstacle for these objects. Their low-degree
section-ratio representation is numerically much more stable than the
attempted degree-18 plane relation.

Exact reconstruction remains open. A useful next experiment should
work with the section-ratio representation and the CM divisor, seeking
corresponding exact reductions, conjugates, or independently justified
height/precision information for those specific objects. Repeating the
same plane fit, treating a weighted singular gap as a certificate, or
recognizing its rejected coefficients would not advance the task.

This is progress on C. It does not yet give the genus-64 cover, the
target Jacobian torsion, or a polynomial for the original Dembélé field.
