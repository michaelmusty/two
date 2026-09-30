# Reusing the user's Belyi code for the target cover

Date: 2026-09-15. D51. The user approved D50's plan and requested that Belyi
maps and their own code receive preference where useful, without making
them mandatory. This preference persists for subsequent work.

**Results:** an adapter now uses the existing Cauchy operator and Arnoldi
implementation in `/Users/musty/Belyi/Cext/powser_arnoldi.c` for the
genus-64 level cover. A numerical pilot finds the expected 48 new
directions with a clear spectral separation and improving independent
errors. The separate [target-realization argument](target-realization.md)
identifies the original residual systems in the canonical Jacobian.
An exact torsion control uses the Q8 Belyi curve from the user's thesis.
There is still no arithmetic model or target field polynomial.

## 1. What is reused

The Belyi package separates geometric reduction from a numerical operator
given by polynomial evaluations, point weights, a permutation of samples,
and Fourier transforms. Its input permits different coefficient counts
at different centers. The type-specific Magma frontend requires a
triangle-group presentation; the C operator and generic Arnoldi callback
do not. The adapter supplies the latter with the known arithmetic polygon
and sheet monodromy.

The C source is included at compile time, without copying or editing it.
Only the interface and the projection onto the new part are implemented
here. Builds are stored in ignored `dembele/pari/.build/`, with a key
depending on both sources and the compiler/link flags. `--belyi-root` or
`BELYI_ROOT` selects the package. Source provenance in the saved reports:

- Package HEAD inspected: `d5ddfc31cca495c7c0288e9e80e29982f1710ff0`.
- Operator source SHA256:
  `f304ff6a2e93f7c1ea31f69082623167ccdc70b9f8564eed1588932ec63d5a5b`.
- The package's pre-existing modified files were preserved.

This is actual reuse of its numerical implementation, not just a citation
to a similar method. The analytic input remains different: Y -> C has
positive-genus base and 27 branch points (18 transposition points and
nine three-cycle points). We have not supplied a three-point map from
Y to P1, nor a permutation triple that the triangle-group frontend could
use directly. Such a Belyi presentation remains an optional possibility.

## 2. Two CM orbit blocks and the new part

Script 80's geometry export replays the exact division-level reduction.
It checks that all 277 numerical side actions are aligned with their
exact quaternion elements before exporting their S3 images. The squared
comparison error is zero at the stored arithmetic precision. The
order-32 elliptic generator has transposition image.

Label its fixed sheet 0 and its swapped sheets 1 and 2. With
`zeta=exp(2 pi i/32)`, the sheet functions satisfy

    f0(w) = (w/R)^31 H0((w/R)^32),
    f1(w) = (w/R)^15 H1((w/R)^16),
    f2(w) = zeta f1(zeta w).

This is the ramification-offset mechanism already used in the Belyi
power-series implementation. A truncation n in H0 and 2n in H1 keeps
the same maximum upstairs power. There are 3n orbit coefficients. The
new part is expressed using 2n coefficients a,b:

    H0(u) = -2 a(u),
    H1(t) = b(t^2) + t a(t^2).

The sum of the three sheet differentials vanishes. The inverse projection
is `a=(H1_odd-H0)/3`, `b=H1_even`. These are complex differential
coordinates. Diagonalizing a transposition in characteristic zero is not
an integral mod-two comparison; the representation proof uses the Hecke
projectors on the Tate lattice instead.

Reduction records each side element and rotation. Their exact permutations
are composed in that same order. If the final sheet is the partner of
sheet 1, the node is rotated by zeta and its derivative multiplied by
zeta. These reduced nodes, weights and sorting permutation are passed to
the unmodified Belyi C operator. Both DFT strides are one after replacing
the disk coordinate by the appropriate CM power.

## 3. Checks and numerical results

The tests compare native operator values with direct NumPy polynomial
evaluation and Fourier transforms, check serial/threaded equality, and
recover the independently implemented scalar operator on the old part.
They also check the two elliptic exponent sectors, old/new decomposition,
optimized matrix assembly on a shifted grid, and rejection of zero
vectors as differential candidates.

| n | Largest target eigenvalue distance from 1 | 49th distance | Finite-operator defect | Changed-quadrature defect | Worst sampled side defect |
|---:|---:|---:|---:|---:|---:|
| 256 | 0.671 | 0.678 | 0.472 | 0.638 | about 1.2 |
| 1024 | 0.0354 | 0.403 | 0.0458 | 0.0473 | 0.115 |
| 2048 | 0.000469 | 0.398 | 0.000588 | 0.000642 | 0.00908 |

The n=2048 side audit samples 273 distinct side actions. It is not an
all-sides certificate. The changed quadrature uses 3n*2 samples per orbit
and phase offset 0.19 instead of the construction grid. All these errors
are empirical. The 48 directions are predicted by the representation
argument; simply requesting 48 eigenvectors would not establish their
dimension. Their spectral separation and independent convergence are
the numerical evidence.

Native/direct operator agreement at n=2048 is `2.78e-16` relative; the
old component agrees with the scalar implementation to `8.72e-14`.
These test the adapter on its supplied data. The reduction nodes are
double precision in this pilot, despite the native operator's 40-digit
arithmetic. The source geometry has roughly 57 digits. Neither fact
gives a certified error bound for the sections.

Dense pilot assembly was changed to evaluate each monomial once in blocks,
avoiding Horner evaluation of many mostly-zero basis vectors. The n=2048
pilot took 43.6 seconds after this change. The older n=1024 run took
114.5 seconds with the slower assembly; these timings should not be used
as a scaling comparison. The pilot still uses dense double linear algebra
to select/refine the 48-dimensional candidate space.

### Two failed/limited checks are retained

The first n=256 native output appeared to be zero because the upstream
ball formatter could print zero for a wide ball with nonzero midpoint.
The wrapper now explicitly serializes numerical midpoints and separately
reports arithmetic radii. At n=256 those radii can exceed `1e27`; at
n=2048 their conversion to a double overflows. They give no useful
accuracy certificate. This is distinct from the very close agreement
of the computed midpoints with the independent implementation.

A bounded n=256 call to the package's Arnoldi solver did not converge at
the requested `1e-5` threshold. Its zero return vector is marked invalid;
its reported differential errors are null, not zero. The result does not
establish that Arnoldi fails at adequate truncation. The larger pilots
reuse the native operator for validation, with a dense stabilized solve
for the candidate space. A production native solver remains to be chosen
after the arithmetic normalization question is addressed.

## 4. An actual Belyi curve as a torsion control

The model already recorded in `belyi/validate_q8.sage`, from the user's
Q8 thesis example, is

    y^2 = 16 x^5 - x.

On this model take `beta=(4x^2+1)^2/(16x^2)`. Then
`beta-1=(4x^2-1)^2/(16x^2)`. The six hyperelliptic branch points form three
pairs over 0,1,infinity. Each has ramification index four for beta, giving
degree eight and passport `(4,4),(4,4),(4,4)`. This supplies an explicit
Belyi map on the control, independently of numerical reconstruction.

Script 82 constructs all 16 geometric 2-torsion divisor classes over F49
from these branch points, checks their distinctness and group law, and
computes the action of Frob7. It has order two, fixes eight torsion points,
and has `rank(Frob7-1)=1`. The Jacobian has 4096 points over F49. This
agrees with the known torsion field Q(i) and gives a reproducible exact
answer for testing a future lifting backend.

The control uses Magma's hyperelliptic Jacobian arithmetic. It is not yet
a test of generic Makdisi arithmetic or p-adic lifting and gives no
runtime estimate for genus 64. No LiftTors installation was found at the
local locations checked. Its installation/adaptation and a representative
genus/extension benchmark remain future work.

## 5. Reproduction and next work

```sh
python3 dembele/pari/run_fdom.py cover-geometry
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/81_belyi_cover.py \
  --n 2048 --pilot --output dembele/data/computed/belyi_cover_pilot_2048.json
/Applications/Magma/magma -b dembele/magma/80_target_projectors.m
/Applications/Magma/magma -b dembele/magma/82_belyi_torsion_control.m
OPENBLAS_NUM_THREADS=4 sage -python -m unittest discover -s dembele/tests
```

All 47 tests pass. The exact Magma scripts and aligned-geometry export
reach their PASS markers. Saved numerical banks are
`belyi_cover_adapter_64.*` and `belyi_cover_pilot_{256,1024,2048}.*` under
`../data/computed/`; n=2048 is the current cover pilot, not an exact model.

The next arithmetic task is to justify a field/normalization for sections
on this specified Y and choose reconstructible multiplication or
evaluation data. Inspect the user's Belyi reconstruction/recognition
routines first where their input requirements fit. More numerical
precision should serve that specific arithmetic target. The Q8 curve
is the preferred small control for setting up generic torsion lifting;
the norm-97 cofactor check and actual genus-64 cost remain open.
