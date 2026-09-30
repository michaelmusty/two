# Arithmetic normalization from a marked point (D52)

Date: 2026-09-15. The user asked to continue, giving priority to `belyi/`,
their thesis, and their two coauthored Belyi papers.

**Mathematical result:** a formal coordinate constructed from a distinguished
differential, followed by a weight-one rescaling, gives coefficients over
the marked curve's field of definition. This removes the need to identify
a CM period or to infer a field from real-looking coefficients. The
statement below is an elementary argument, rather than a claim that the
Belyi papers already prove this normalization for arbitrary Shimura curves.

**Application remains conditional:** the base jet matrix and selected cover
coefficient matrix must be invertible, and the two selected scale
coefficients must be nonzero. Our saved floating-point spaces do not
certify these hypotheses. The final method does not assume a vanishing
sequence for the 48 new differentials.
An exact algebraic model, exact new differential coefficients, and the
target field polynomial are still absent.

## Sources and actual reuse

The local thesis is
[`musty_thesis_final.pdf`](/Users/musty/michaelmusty.github.io/assets/musty_thesis_final.pdf).
The first paper is also local as
[`belyi.pdf`](/Users/musty/michaelmusty.github.io/assets/belyi.pdf).

- Klug–Musty–Schiavone–Voight,
  [*Numerical calculation of three-point branched covers of the projective line*](https://arxiv.org/abs/1311.2081),
  §5, explicitly describes reconstruction of general nonhyperelliptic
  canonical curves from differential products. This is the appropriate
  general-genus part of that paper to retain here.
- Musty–Schiavone–Sijsling–Voight,
  [*A database of Belyi maps*](https://arxiv.org/abs/1805.07751),
  §§4.2–4.4, uses a marked point for descent and weighted coefficients for
  normalization. Remark 4.4.1 describes the observed field of normalized
  series as a numerical observation. It is not a theorem identifying our
  previous CM gauge with F. The existing
  `/Users/musty/Belyi/Code/recognition.m:5` implements a weighted Bézout
  rescaling, and `theta.m` contains the recognition routines. Its present
  equation-construction entry points handle genus one and hyperelliptic
  curves; they cannot directly accept our genus-64 canonical model.
- Musty's [*2-Group Belyi Maps*](https://michaelmusty.github.io/assets/musty_thesis_final.pdf),
  Chapter 5, constructs quadratic extensions using divisors and Picard
  groups. Its characteristic-zero method has an explicit incompleteness
  caveat after Algorithm 5.5.1. The current degree-three cover of a
  positive-genus base is not input to that tower algorithm. The thesis's
  Q8 example is, however, a concrete exact control. The new
  [`belyi/pointed_series.py`](../../belyi/pointed_series.py) calls the
  existing [`validate_q8.sage`](../../belyi/validate_q8.sage), then performs
  the independent exact coordinate tests below.

No new Belyi map on Y or triangle-group presentation has been found. D51's
adapter continues to reuse the user's actual Cauchy operator. The external
Belyi checkout was not edited in D52.

The general equation-recovery theorem of van Bommel–Costa–Poonen–Srinivasan
also assumes an arithmetic basis and arithmetic local expansions as input;
it does not itself convert an arbitrary numerical complex basis into that
input. See [Theorem 3.1](https://arxiv.org/pdf/2506.14026). The following
construction addresses that normalization step in our rational-point case.

## The formal-coordinate argument

Let k be a characteristic-zero field embedded in C. Let X/k be a smooth
projective curve and P a k-rational point. Let L be a one-dimensional
k-subspace of H^0(X,Omega), with nonzero differential vanishing to order m
at P. For example, L is the highest nonzero step of the vanishing
filtration on a k-defined space of differentials. Since P is rational,
each graded piece has dimension at most one; the highest step is a line.

Choose a k-defined local parameter z, for the proof only. After division
by its leading coefficient, a generator of L has expansion

    omega = z^m (1 + c_1 z + c_2 z^2 + ...) dz,   c_i in k.

There is a unique formal parameter with leading coefficient one satisfying

    t^(m+1) = (m+1) integral_0^z omega,
    t = z + O(z^2).

Indeed, the right side is z^(m+1) times a unit with constant coefficient
one. Its formal (m+1)-st root lies in k[[z]] in characteristic zero. This
does not require adjoining a root of a nonunit leading constant. It gives
omega = t^m dt. The formal parameter need not be a global rational
function; local reconstruction only needs a parameter of the completed
local ring.

Now start instead from an arbitrary analytic parameter u and an arbitrary
complex generator of the same line. Normalize its leading u coefficient
to one, and apply the same integral construction, obtaining tau=u+O(u^2).
Both primitives come from the same one-dimensional differential line.
Consequently tau=s*t for some s in C^*. All nonlinear coordinate ambiguity
has disappeared; only this one scalar remains.

Let V be any k-defined space of regular differentials, with vanishing
sequence a_0<...<a_(r-1) at P. There is a unique basis whose coefficients at
these orders are the identity matrix. In parameter t, write its coefficients
as c_(n,i). They are in k, because taking these coefficients and solving
the invertible jet system are operations over k. In parameter tau the
same echelon normalization gives

    H_i(tau) = tau^a_i + sum_(n not a_j) A_(n,i) tau^n,
    A_(n,i) = c_(n,i) s^(a_i-n).

Thus the weight of A_(n,i) is w=n-a_i. Select nonzero coefficients and
integer exponents e_j with sum e_j*w_j=1, and put

    lambda = product A_j^e_j.

Then lambda=c/s with c in k^*, so v=lambda*tau=c*t belongs to k[[z]].
The rescaled, echelonized differential coefficients

    G_i(v) = lambda^a_i H_i(v/lambda)

all lie in k. More precisely G_i(v)dv are a k-basis of V: uniqueness of
the echelon basis in the k-defined parameter v proves this, including the
differential scaling factor. Multiplying lambda by a nonzero rational
number does not change the conclusion.

Once v is k-defined, the normalization of V can use **any fixed r
coefficient functionals** with invertible coefficient matrix. They do not
have to be the vanishing orders or the first r coefficients. Setting that
matrix to the identity defines a unique k-basis, by the same linear-algebra
argument. Choosing the integer indices numerically does not affect this
conclusion; hold those indices fixed during every subsequent comparison.

If the available nonzero weights have gcd d>1, extracting a d-th root
does not establish the same conclusion over k. One gets at most a
controlled extension from this procedure; the implementation refuses to
silently choose such a root. Additional coefficients or a different
marking may resolve the ambiguity. A finite list with gcd>1 alone does
not prove an obstruction to descent.

## Using the genus-16 base to normalize the cover

Use the canonical F-models and markings specified in
[`genus64-cover.md`](genus64-cover.md). The unique order-32 point P of C
and the unramified point P32 over it on Y are F-rational under that
canonical-model interpretation. The other point above P has ramification
index two, which distinguishes both points arithmetically.

Take the highest-vanishing differential line on C at P. The numerical
16-by-16 jet matrix supports orders 0,...,15, with condition number about
555. The corresponding integral parameter tau uses m=15. In the
re-echelonized base series, select

    A2 = [tau^16] H_14,       weight 2,
    A3 = [tau^16] H_13,       weight 3,
    lambda = 12*A3/A2.

The factor 12 is a fixed rational choice keeping |lambda| near one. The
two coefficients are numerically nonzero and stable. Conditional on the
rank and nonvanishing hypotheses, v=lambda*tau is an F-defined formal
parameter on C. Pulling it back along the unramified P32 branch gives an
F-defined parameter on Y without further root extraction.

The new space is ker(Tr: H^0(Y,Omega) -> H^0(C,Omega)), of dimension 48,
and is defined over F because the map Y -> C is. Echelonizing it in this
pulled-back parameter therefore gives an F-basis. The same parameter
also normalizes the 16 old directions. Once computed accurately, these
two bases can be combined into the full 64-dimensional canonical input
without solving a single 64-by-64 initial-jet normalization system.

At P32, the saved new component has differential proportional to
a(u)du with u=(w/R)^32; its common constant is irrelevant to echelon
normalization. The base uses this same u. The implementation checks that
their saved radii agree. An initial trial assumed new vanishing orders
0,...,47. Its first-48 coefficient matrix becomes severely ill-conditioned
as the source improves. This does not establish a different vanishing
sequence: very small genuine singular values remain possible. The final
method instead chooses 48 coefficient indices among a longer expansion,
and does not require knowing the new vanishing sequence.

## Exact control and numerical implementation

The thesis curve is y^2=16*x^5-x. At (1,sqrt(15)), use u=x-1. After
multiplication by sqrt(15), a basis of regular differentials has
coefficient series

    h(u) = ((16*(1+u)^5-(1+u))/15)^(-1/2),   u*h(u).

The exact integral normalization gives

    [tau^2] H_0 = 481/4320,
    [tau^3] H_0 = -4879/182250,
    lambda = -78064/324675.

The normalized coefficients agree exactly after a nonlinear parameter
change over Q(i) and a nontrivial basis change. Omitting the differential
Jacobian changes the result and is detected. At infinity, the vanishing
sequence is [0,2] and the first nonzero scale weights have gcd 8; the
root ambiguity is refused. Here the order-eight symmetry also explains
why the weights remain multiples of eight.

The exact reference explicitly reverses and substitutes formal series.
[`83_pointed_normalization.py`](../pari/83_pointed_normalization.py) instead
uses Lagrange inversion. If tau=u*phi(u), then

    [tau^n] H(tau) = [u^n] h(u)*phi(u)^(-(n+1)).

This accounts for the derivative automatically. The two implementations
agree on the exact Q8 control. Further tests check a three-dimensional
canonical space with nonconsecutive vanishing orders on a plane quartic,
and normalization by fixed coefficient indices that are not vanishing
orders. To obtain B output jets using a line
vanishing to order m requires B+m input jets of that line. The numerical
script uses 60-digit arithmetic on saved double inputs, which controls
added arithmetic error without increasing source accuracy.

An initial attempt to use the highest *new* differential as the coordinate
anchor was poorly conditioned. The current implementation uses the much
more accurate base data. This choice is justified by the same argument
and directly retains both F-defined summands.

Reproduce from the repository root:

```sh
DOT_SAGE=/tmp/dembele-pointed-sage sage -python belyi/pointed_series.py \
  --output dembele/data/computed/pointed_normalization_control.json
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/83_pointed_normalization.py \
  --output dembele/data/computed/pointed_evaluation_4096_60.json
```

The default comparison uses cover n=4096 versus 2048, the same n=10240
base anchor, and 60 output jets. `--length 96` reproduces the longer
`pointed_evaluation_4096.json` trial. The `pointed_evaluation_lengths.json`
table comes from the same comparison at lengths 56,60,64,72,80.
`--gauge initial --length 64` retains the initial first-48 normalization
for diagnostics. The earlier `pointed_normalization_2048.json` compares
cover 2048/1024 with base 10240/8192; `pointed_normalization_4096.json`
compares cover 4096/2048 with the common 10240 base.

## Outcome of the bounded cover experiment

The new n=4096 run reuses the Belyi engine and takes 234 seconds. Its
48th eigenvalue is 7.68e-7 from one, while the 49th is 0.391 away. The
native adapter agrees with the independent numerical implementation to
2.88e-16. These checks support the candidate space; they are not error
bounds on its arithmetic coefficients.

| Diagnostic | n=2048 | n=4096 |
|---|---:|---:|
| Finite operator defect | 5.88e-4 | 1.04e-6 |
| Changed quadrature defect | 6.42e-4 | 1.16e-6 |
| Worst sampled side defect | 9.08e-3 | 2.75e-5 |
| First-48 raw jet matrix condition number | 9.08e4 | 4.50e7 |

The base normalization factor changes by 1.30e-10 between the base's two
saved truncations; three independent base samples change by at most
4.49e-10 in the stated scaled norm. The new first-48 normalized samples,
however, still change by order one. This separates a stable coordinate
anchor from an unstable basis extraction.

Selecting later coefficient indices removes the new vanishing-sequence
assumption but has not solved the numerical conditioning problem:

| Output jets available | Selected matrix condition | Unselected-jet relative difference |
|---|---:|---:|
| 56 | 1.38e7 | 0.180 |
| 60 | 7.79e6 | 0.101 |
| 64 | 2.42e7 | 0.218 |
| 72 | 1.15e8 | 0.268 |
| 80 | 3.25e8 | 0.212 |
| 96 | 4.48e9 | 0.341 |

Each comparison uses the same selected indices in both cover banks. The
norm omits all identity rows imposed by normalization, so a successful
fit at those rows cannot make this check pass. Whitening gives small
selection condition numbers, but the original matrices remain poorly
conditioned; reporting only the whitened numbers would hide the problem.

**Next bounded task:** improve the conditioning of the arithmetic
coordinate/basis, for example by testing a few small rational changes of
the now justified F-parameter, with the Q8 and quartic controls and these
two cover banks held fixed. Measure sensitivity and coefficient stability
before choosing another larger truncation. A low residual in the finite
Cauchy system does not justify a recognition search. The current data do
not support even a first exact new coefficient, and no such coefficient
was claimed or passed to a broad search.

All 52 tests pass. The Q8 reference reports an exact PASS. No external
Belyi edits, remote jobs, messages, commit, algebraic Y, target torsion,
or field polynomial were produced.

**D53 follow-up:** [M23 review and relative reconstruction](m23-coordinate-review.md)
revises the next task to equation recovery in this arithmetic base gauge.
Complex trace data for Y/C are stable, while five simple line choices
using both marked points remain unstable. Those experiments do not
replace this document's arithmetic hypotheses with a numerical proof.
