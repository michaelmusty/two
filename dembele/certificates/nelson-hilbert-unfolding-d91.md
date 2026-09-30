# D91: Hilbert unfolding and a certified partial sum

Date: 2026-09-23. Continuation of
[D90](nelson-totally-real-kernel-d90.md), authorized by “go for it”.

**Result:** the two cusp lattices are now identified exactly, central-unit
duplicates are removed, and all powers at p2 and all auxiliary ideals are
summed for a finite set of 29 primitive quaternion classes. The resulting
three derivative-kernel sums have rigorous numerical enclosures. They
are affine expressions in three missing Hecke coefficients.

**This is not an evaluation of a complete eigenform or a CM tangent.**
The omitted primitive classes have no tail bound. The specialization of
the global Shimizu correspondence to our exact test vector, including
its nonzero normalization, also remains to be established. No candidate
curve equations, candidate jets or differential banks were read.

The first complete central-unit reduction bound is much too large for
a direct 32-dimensional shell enumeration. This is now a concrete
algorithmic issue, rather than an unspecified need for more precision.

## 1. Exact cusp and unit arithmetic

Retain F, O, pi=2+b, delta=16/pi and the CM element beta from D90.
We prove on the actual 32-element Z-basis that

    beta^2=-pi, Nrd(beta)=pi,
    O#=beta^(-1) O, [O : beta O]=4.

The basis change between beta^(-1)O and the saved relative dual is
integral with determinant ±1. The equality is independently replayed
using rational polynomial and quaternion arithmetic in script 334.

For an element alpha with totally positive n=Nrd(alpha), put

    alpha_parallel=(alpha+beta*alpha*beta^(-1))/2,
    u=Nrd(alpha_parallel),
    A=Norm(n)*sigma_0(u/n).

Here sigma_0 is the split real place. In the CM-centered matrix chart,

    A=|X|^2 * product_(v != 0) n_v,
    rho=|Y/X|^2=1-Norm(n)/A.

Both A and rho are invariant under multiplication by a central unit.
For the pairs (a,1), a=1,3,5, the remaining phase is

    Phi_a=(X/|X|)^(a+3)*(conjugate(Y)/|X|)^(a-1).

Multiplication by beta divides or multiplies A by 2 and preserves this
phase. This follows from beta being purely imaginary in the CM chart;
the general sign is (-1)^(a+1). Exact lattice membership, norm identities
and the field element defining A are checked independently. The
archimedean quantities used in the final sum are recomputed as Arb balls
from exact algebraic inputs, not from D90's decimal coordinates.

Of the 4,955 signed-pair representatives in D90's second shell, 130 have
positive norm-ideal norm at most 64. They represent 34 central-unit
classes; 96 duplicate witnesses are retained and checked exactly.
There are 28 mixed classes and six pure CM classes.

Remove the largest possible left power of beta from each representative.
This gives 29 distinct primitive classes:

| Norm ideal | Prime label | Classes | Coefficient required |
|---|---|---:|---|
| 1 | — | 9 | 1 |
| 31 | b=10 modulo 31 | 12 | a_f(p_10) |
| 31 | b=20 modulo 31 | 4 | a_f(p_20) |
| 31 | b=21 modulo 31 | 4 | a_f(p_21) |

The nine norm-one classes comprise the identity class and eight mixed
classes. These are finite subsets, not complete norm-ideal enumerations.
The saved T31 characteristic polynomials concern **b=27**, a different
prime. They do not specify the three coefficients in this table on a
matched eigenline.

There is a simple exact counterexample to using the old shell as a
global cutoff. Multiplying a mixed norm-one representative by beta gives
an integral mixed class of norm-ideal norm 2. The old pilot contains only
a pure CM class at norm 2. Script 330 retains the missing element.

## 2. The unfolding, with its scope stated

Use Fourier frequencies n/delta and ideal coefficients a_f((n)). For
parallel weight two, a normalized form has a_f((1))=1. The relevant
sixteen C-forms have U_p2=+1; the level-one target representation must
not be substituted for them.

For the full Hilbert modular group, define

    Lambda_F(s)=D^(s/2)*pi^(-8*s/2)*Gamma(s/2)^8*zeta_F(s), D=2^31,
    E*(z,s)=Lambda_F(2*s)*E(z,s).

The completion satisfies s ↔ 1-s and has residue 64*R_F at s=1.
Thus E*/(64*R_F) is the residue-one completion used in Nelson's contour
argument. These normalizations follow from the constant term and
completion in [Masri, section 2](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806604636373020674-1806604636373020674-6e788fc744157b0b48d40b90be793f0e.pdf).

The translation lattice has covolume sqrt(D). Its constant term pairs
equal norm frequencies. Grouping alpha modulo central units unfolds the
seven unit directions in the height integral. The factor 1/2 in the
theta kernel cancels the two signs of alpha. There is no second regulator
factor from this grouping. The cusp stabilizer and its height quotient
are also described in [Hida, section 3.1](https://www.emis.de/ft/9824).

Integrating the one split polynomial Gaussian and seven definite
Gaussians gives

    Gamma(s)^8 * Gamma(s+1)^7 * Gamma(s+k),
    Z=(4*pi^2)^8*A/D^2.

For (a,1), the two shifts are k=a+2 and k=a+3, with coefficients a and
-rho. The conditional common Petersson prefactor, with the theta kernel
chosen in D90, is

    D^(3/2)/(64*R_F*(4*pi)^9).

This accounts for the chosen additive character, translations, Gamma
integrals and Eisenstein residue. It does **not** by itself establish
the identification of the theta integral with a compatibly normalized
rank-one tensor of quaternionic eigenforms. Hida's section 5.3 and its
reference to Shimura's matrix-coefficient theorem provide general
context, not a checked specialization of that theorem to these test
functions. That remaining identification is explicit in the JSON flags.

At p2, the newvector Fourier change contributes -1/2, the theta Fourier
change contributes -1/2, and the cusp has width 2. Hence the dual lattice
has coefficient 1/2. Replacing its elements by beta^(-1)alpha changes
A to A/2. The inverse-A factor cancels the 1/2, and the odd-pair phase
is unchanged. The two cusp kernels therefore combine as J(Z)+J(Z/2).

Finally, every beta^r multiple of a primitive class has coefficient
a_f((n)), since U_p2=+1. Its inverse majorant is 2^(-r)/A. The entire
string supplies the geometric factor 1/(1-2^(-s-1)). Define

    K_k(Z) = integral_(c) (2s-1) Gamma(s)^8 Gamma(s+1)^7 Gamma(s+k)
             * zeta_F(2s) * Z^(-s)
             * (1+2^s)/(1-2^(-s-1)) ds/(2*pi*i).

The implemented primitive-class summand is

    a_f((n)) * Phi_a/A * (a*K_(a+2)(Z)-rho*K_(a+3)(Z)).

The finite primitive-subset expression is well defined independently of
the unfinished global identification. The zeta factor sums every
auxiliary ideal; it is not truncated to the unit ideal. Over Q, the
undifferentiated argument, scalar and sign grouping reduce to Nelson's
Bessel formula.

## 3. Rigorous numerical enclosure

Script 333 evaluates 42 scalar kernels: seven distinct A values and six
Gamma shifts. It uses 320-bit Arb balls, Re(s)=2, step 1/32, and
|Im(s)|<=16. The Dedekind zeta is evaluated as the Riemann zeta times
the seven nontrivial even Dirichlet L-functions modulo 32. Hurwitz-zeta
evaluations include their complete series. Three independent finite
Euler products, with explicit omitted-factor bounds, check the
character product and the ramified Euler factor.

The quadrature bound is analytic, rather than inferred from agreement
between two grids. For c=1,2,3, write the Gamma product using Gamma(1+it)
and integer linear factors. The inequalities

    |Gamma(1+it)|^2 = pi*t/sinh(pi*t)
                    <= (1+2*pi*t)*exp(-pi*t)

and 3<pi<4 give a positive-coefficient polynomial P_(c,k)(t), of degree
16*c+k, times exp(-24*t). Its integral is an exact finite sum of
factorials and powers of 24. Bounds for zeta_F(2c), the two cusp factors
and the beta string are included.

The two strip boundaries c=1 and c=3 bound the infinite trapezoidal-rule
error. This uses the contour identity in
[Trefethen–Weideman, section 5, equation (5.15)](https://people.maths.ox.ac.uk/trefethen/publication/PDF/2014_149.pdf).
The same polynomial majorant bounds the omitted vertical grid tail;
it decreases beyond height 16. Roundoff and the algebraic input
uncertainty are included in the node balls.

The largest scalar quadrature error bound is **6.55e-44**. After the
actual phases and inverse-A factors, every real and imaginary component
of the four accumulated Hecke buckets has radius **less than 1e-47**.
These bounds apply only to the specified primitive subsets.

For example, omitting the common Petersson scalar, the (1,1) expression
is approximately

    7338.803962224303
    -19.66178305689814 * a_f(p_10)
    +14.41114472387155 * a_f(p_20)
    + 6.77251007757757 * a_f(p_21).

The JSON also contains the complex (3,1) and (5,1) expressions and
every individual primitive-class contribution. No value is assigned to
the three unknown coefficients, and no ratio is presented as a tangent.

## 4. Derivative calibration and a source discrepancy

Script 335 adds a check beyond D90's undifferentiated Bessel calibration.
At Y=0, with A=|X|^2, direct application of the displayed Lie derivations
to phase_2*W_2 gives

    delta_1 delta_2 = W_2 - A*dW_2/dA
                    = 4*pi*sqrt(A)*W_3.

The differentiated Gaussian/Mellin implementation agrees with this
direct derivative at |X|=0.7,1.3,2, with relative discrepancies below
1.5e-60. This diagnostic is numerical; the separate Gaussian polynomial
identities are exact, and the degree-eight sums have the interval bounds
above.

There is a scale discrepancy with a literal reading of equation (11)
in [arXiv v1, page 12](https://arxiv.org/pdf/1210.1243v1): for this test
its displayed summand gives 4*pi*W_3, without |X|. We retain the direct
Gaussian derivation and record the discrepancy rather than silently
changing the implementation to match the display. The published 2015
formula was not inspected: the publisher PDF returned HTTP 403. No
claim about an error in the published version is made.

## 5. A complete unit cutoff, and why not to enumerate it directly

Script 336 constructs seven independent cyclotomic units. Independence
is checked by a nonzero interval determinant of their logarithms. Full
unit-group generation is unnecessary: any rank-seven subgroup provides
a fundamental parallelepiped covering the logarithmic hyperplane.

Let

    v=(P_0/delta_0, n_1/delta_1, ..., n_7/delta_7).

Its product is (1+rho)*A/D <= 2*A/D. Multiplication of alpha by a central
unit adds twice the unit logarithm to log(v). Center the resulting vector
in the unit parallelepiped. Convexity bounds the sum of its exponential
coordinates by the largest value at one of the 128 vertices. Combining
this with D90's Q<=1.01*M proves

    A(alpha)<=T => some central-unit representative alpha' satisfies
    Q(alpha') <= 1.01*C*(2*T/2^31)^(1/8).

The raw cyclotomic basis gives C=648536. An LLL change reduces the
proved integer constant to **2126**. Even so, covering A<=359 would
require enumerating through **Q<=333**, compared with the saved shell
Q<=2.02. The volume of that 32-dimensional ellipsoid is about 3.22e39.
Volume is a diagnostic, not a lattice-point count or a runtime estimate.
No such enumeration was launched.

This bound establishes finite coverage, but is computationally much
too conservative. It also does not bound the contribution of A>T.

A useful next formulation avoids one large unit-cover ellipsoid:

    A/Norm(n)=cosh(distance(z0,alpha*z0)/2)^2.

Thus fixing the norm ideal turns the remaining cutoff into a hyperbolic
displacement cutoff. A norm-ideal/Hecke-coset enumeration using the
arithmetic Fuchsian group is a concrete alternative to investigate.
The nine norm-one classes provide a small control with known coefficient
1. Completeness still needs a proof; a stable partial sum is insufficient.

## 6. Reproducibility and next work

```sh
python3 dembele/pari/337_nelson_hilbert_audit.py --check
python3 dembele/pari/326_nelson_kernel_audit.py --check
```

Root `nelson_hilbert_d91.json` incorporates the earlier D91 manifest.
The standard-Python replay checks the exact dual identity, all 96 unit
witnesses, primitive decompositions, ideal labels, norm/majorant
identities, interval widths and bucket accumulation. A corrupted dual
change is rejected. Arb nodes, logarithm/vertex balls and numerical
calibration are hash-bound to their recorded runs; the standard-Python
checker does not recompute those analytic functions.

Nine bounded jobs completed: five passes and four retained development
failures, all below 6.3 seconds. The failures were Sage API/coercion
issues, not failed mathematical assertions. Scripts 327--337 and their
bound artifacts are frozen. The earlier certificates remain intact.
Decisions, references and the entry-point documents are updated.

**Next:** make a complete, economical norm-ideal enumeration and an
omitted-class tail bound, beginning with the norm-one control. Build a
matched coefficient bank for the first quartic level-p2-new eigenline;
the current subset already requires p_10,p_20,p_21. The old script 60
records an InternalNeighbors assertion for conjugate primes and a
307.8-second T31 build, so an unmodified rerun is not a bounded solution.
Finish the nonzero global test-vector identification before interpreting
the resulting complete sum as a CM derivative. The independent exact
jets and D88's marked-curve identification remain subsequent work.

No remote job, larger cubic precision, exact cubic recognition or target
field construction was performed in D91.
