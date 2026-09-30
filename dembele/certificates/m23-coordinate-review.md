# M23, earlier normalization work, and relative reconstruction (D53)

Date: 2026-09-15. User suggestions: revisit the Poonen/coauthors M23 paper,
the earlier agent sessions in this repository, and Zhang's companion note.

**Result:** retain the curve/Jacobian route for the original Dembélé field,
but prioritize staged equation reconstruction over normalizing every new
differential coefficient. The saved Belyi computations already contain
usable complex trace data. A bounded attempt to choose an arithmetic line
using the two marked points remains unstable. No exact coefficient, curve,
target torsion point, or field polynomial was recovered.

## 1. What the sources actually supply

Zhang's linked note is now titled
[*Where to Point the Telescope: AI, Mathematical Judgment, and M23*](https://www.shaowuzhang.com/files/how-we-found-m23.pdf).
The local [August 11 preliminary copy](../rigidity/refs_how-we-found-m23.pdf)
has the older title *How AI Entered Our Collaboration on M23 and How We
Found the Case*. Its mathematical account agrees with the current link.
It reports failed recognition at 40, 60 and 90 digits in triangle
coordinates. Map-defined coordinates allowed recovery of the quadric from
40 digits, with heights below 1000. A separate reduction recovered the
cubic from those same data. It does not claim failure at every possible
precision or describe that separate algorithm in implementable detail.

In [the M23 paper, §3](https://arxiv.org/pdf/2608.08538), the authors
normalize the quadric, then the cubic modulo the linear multiples of that
quadric, using a Hermitian orthogonal complement. They recognize equations
over Q(sqrt(-23)). Algebraic Riemann–Roch computations then recover the
map and a function that descends to Q; modular linear algebra and CRT
recover the final polynomial. Numerical discovery is explicitly
uncertified; the final assertions receive exact verification.

The [published repository](https://github.com/shaowuz/m23isgalois), inspected
on this date, contains final polynomials and verification code. It does
not provide the separate coordinate/cubic reduction routine from the
personal account. The explicit quotient by known quadric multiples is
reusable; equating it with the entire undocumented reduction algorithm
would go beyond the sources.

## 2. Reusable work from previous sessions

| Earlier work | Actual implementation and evidence | Transfer |
|---|---|---|
| D3, degree-17 genus-zero covers | [Script 12](../rigidity/12_recognize_248_factors.m) sends the unique simple zero, double point over 1, and simple pole to 0,1,infinity. It uses dumped Newton factors for zeros/poles. Recognition logs record 17/17 coefficients, and [script 14's output](../rigidity/out/exact_map_248_rep1.txt) records an exact passport identity and order-16320 Galois group. | Choose functions using intrinsically distinguished fibers; retain factor structure. The third fiber in script 12 still uses clustered roots of an expanded polynomial, so the code does not eliminate all repeated-root extraction. |
| D9, genus-one corner | [Script 26](../rigidity/26_g1_field.m) extracts the invariant j from Newton data; its obstruction field is the degree-eight field already encountered. | Recover an invariant that answers the arithmetic question before the entire model. |
| D21, genus-two corner | [Precision audit](g2-corner-precision.md), [script 32](../rigidity/32_g2_field.m), and low-weight Igusa ratios. The two internally produced models agree only to about 25 digits in their invariants despite 285-digit working precision. | Check accuracy after equation construction. A small eigensolver residual does not measure downstream coordinate accuracy. |
| D52, current cover | [Marked-point normalization](pointed-normalization.md), [exact thesis controls](../../belyi/pointed_series.py), and [script 83](../pari/83_pointed_normalization.py). | Supplies a conditional F-defined formal parameter. It does not solve numerical conditioning: the best recorded 48-coordinate selection still changes by 10% across banks. |

The earlier rigidity results are historical computations on other covers.
They do not identify the original Dembélé field. The present task still
uses the canonical Y and the [target-realization argument](target-realization.md).

## 3. A relative cubic for the current cover

The following is our adaptation, not a claimed algorithm from the M23 paper.
Let pi:Y -> C be our connected degree-three cover over F, and choose
nonzero F-defined differentials

    omega in ker(Tr: H^0(Y,K_Y) -> H^0(C,K_C)),
    eta in H^0(C,K_C).

The function z=omega/pi^*eta has trace zero. It is nonzero and cannot lie
in F(C), since its trace there would be 3z. A degree-three field extension
has no proper intermediate field, so z is a primitive generator. Newton's
identities give its minimal polynomial

    T^3 - A*T - B,
    A = Tr(z^2)/2,  B = Tr(z^3)/3,  A,B in F(C).

This can recover Y as the normalization of a cubic over an explicit C.
It does not directly construct the nonsolvable number field.

The known branch data matter. Let B2 be the reduced divisor of the 18
transposition branch points, and B3 the divisor of the nine three-cycle
branch points. In particular, the latter nine cannot be omitted. Locally
t=s^e, so a holomorphic differential divided by dt has poles of order at
most e-1 in s. Summing kth powers over the branches retains powers of s
divisible by e; the resulting pole order in t is at most floor(k(e-1)/e).
Consequently

    Tr(omega^2)/2 in H^0(C, 2K_C + B2 + B3),
    Tr(omega^3)/3 in H^0(C, 3K_C + B2 + 2B3).

Here trace means summing the meromorphic tensor powers on the local
sheets; it is not the tensor power of the linear trace. Since g(C)=16,
these spaces have dimensions 72 and 111 by Riemann–Roch. Once C, its
branch divisors, and omega are arithmetic, this supplies finite spaces
for the two unknown coefficient sections. Those inputs are not yet
available as exact computational data.

In script 81's local notation u=(w/R)^32 and r^2=u, the three sheet values
of z are

    -2*a/c,   (a+b/r)/c,   (a-b/r)/c.

Thus

    A = (3*a^2 + b^2/u)/c^2,
    B = 2*a*(b^2/u-a^2)/c^3.

The polynomial can be evaluated without dividing by c or taking a square
root, using its three homogeneous coefficients

    [u*c^3, -(3*u*a^2+b^2)*c, -2*a*(b^2-u*a^2)]

for the terms T^3,T,1. On the disk these acquire a common factor
(w/R)^61. Side transformations multiply them by the cube of the
differential multiplier. This is the numerical descent check below.

**Arithmetic qualification:** a complex choice of omega gives functions
on the complex base, without proving they lie in F(C). Trace symmetry
removes sheet labels, not arbitrary scalar or basis choices. The tests
include the rational cubic Belyi map t=3*x^2-2*x^3: scaling its centered
generator by sqrt(2) gives a cubic coefficient outside Q(t), while the
trace identities remain valid.

## 4. Bounded experiments on the existing banks

[Script 84](../pari/84_relative_cubic.py) reuses script 81's geometry and
the saved banks computed with the user's Belyi kernel. It does not solve
another Cauchy system. The report includes input hashes, alignment
weights, disjoint validation coefficients, denominator diagnostics, and
independent side tests:

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/84_relative_cubic.py \
  --marked-scan --output dembele/data/computed/relative_cubic_4096.json
```

First choose the current cover bank's first complex direction and align
the older bank to it using 128 coefficients of each a,b sector. The two
feature matrix conditions are 2.90713 and 2.90693; disagreement on the
next, unused 128 coefficients per sector is 1.5720e-4. The base
differential is aligned independently between the 10240/8192 banks.

| Coarse u radius, 48 samples each | Relative difference in u*A | Relative difference in u*B |
|---|---:|---:|
| 0.25 | 0.001965 | 0.002192 |
| 0.60 | 0.000993 | 0.001602 |
| 0.85 | 0.000371 | 0.000908 |

The common pole at u=0 has been removed in these comparisons. Global
side tests use homogeneous coefficients: direct division by eta near
its zeros gave misleading, order-one errors in an exploratory test at
exact side midpoints. The stored test uses perturbed side points and
does not divide by eta.

At 381 sampled pairs on 273 distinct sides, the current homogeneous
cubic transformation error is 2.9728e-6 in relative L2, with worst
pointwise relative error 5.0790e-5. The aligned older bank gives 0.005500
in relative L2. These are empirical samples, not uniform error bounds.
The coefficient comparison above and D52's 10% comparison concern
different objects; the former is not a demonstrated improvement of the
arithmetic basis.

Second, test a simple arithmetic line choice at both F-rational marked
points. If v is D52's arithmetic base parameter, the ramified branch has
coordinate s with s^2=v, up to a constant quadratic extension. Each
individual coefficient-vanishing condition is F-defined: relative to an
F-local coordinate, the possible square-root constant only scales that
functional. A one-dimensional common kernel can then be normalized at
the unramified point without adjoining this constant.

The b-sector pullback is a half-density. Writing psi=u/tau and v=lambda*tau,

    [v^n] a_new = lambda^(-n-1) [u^n] a(u)*psi(u)^(n+1),
    [v^n] b_new = lambda^(-n-1/2) [u^n] b(u)*psi(u)^(n+1/2).

The square-root choice only rescales b rows and does not change their
common kernel. We impose a[0..m-1]=b[0..q-1]=0 and a[m]=1, where
m+q=47. Both banks use the same current base parameter, to isolate the
cover's sensitivity. The five trials give:

| m | q | Current raw matrix condition | Relative difference of normalized directions |
|---:|---:|---:|---:|
| 16 | 31 | 8.85e5 | 1.180 |
| 20 | 27 | 4.28e5 | 0.764 |
| 24 | 23 | 5.73e5 | 0.673 |
| 28 | 19 | 4.21e6 | 1.343 |
| 32 | 15 | 2.00e7 | 1.028 |

Thus these simple two-point choices do not fix the arithmetic conditioning.
Rank and D52's arithmetic hypotheses remain uncertified. In particular,
the good complex trace test cannot be substituted for this failed gate.

Artifacts: [JSON](../data/computed/relative_cubic_4096.json) and
[transcript](../data/computed/relative_cubic_4096.out). Six new tests cover
exact elimination and traces for a cubic Belyi control, disk/coarse
offsets, the arithmetic descent counterexample, an independent exact
half-density substitution, zero/nonfinite rejection, and failure of
arbitrary local series at global side checks.

All 58 tests pass (`/tmp/dembele-d53-tests.out`).

## 5. Next work

1. Adapt script 74's quadratic-relation recovery to the **D52 arithmetic
   base normalization**, retaining fixed monomial choices across the two
   saved C banks. Recover and compare the equations themselves and their
   unused-jet residuals. D46's older period normalization is not a substitute
   for D52's field argument. Stable low-height equations may be recognizable
   even when demanding recognition of an entire differential series is wasteful.
2. With exact base relations, reduce subsequent unknowns in its coordinate
   ring/Riemann–Roch spaces before attempting recognition of a relative
   cubic. An F-defined generator with usable conditioning is still needed;
   the five failed line choices are not a solution. Exact known relations
   should be used in that choice and in any refinement.
3. Increase precision only for a specified reconstruction residual after
   these coordinate/representation choices. Exact identification with the
   canonical Y and the original target representation remains necessary;
   matching a branch profile or a Galois group alone is insufficient.

This is a change in the order and representation of the reconstruction
problem, not proof that the end-to-end field construction is now feasible.
No new large solve, external package edit, remote work, message, or commit.
