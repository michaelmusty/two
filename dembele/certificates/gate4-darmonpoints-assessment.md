# Gate 4 de-risking: what `darmonpoints` gives us and what it does not

**Date:** 2026-08-16. Follows the plan of record
(`levelraise-cd-plan.md`, gate 4: "de-risk by first running `darmonpoints` on a
small totally real case to map the machinery, then assess the degree-8 stress
points").

## Status: installed, working

`sage -pip install darmonpoints` builds cleanly against **SageMath 10.6**
(darmonpoints 8.3, Cython extension compiled, wheel cached). All the modules we
care about import: `findcurve`, `padicperiods`, `cohomology_arithmetic`,
`arithgroup`, `sarithgroup`.

Smoke test — the canonical classical Stark–Heegner point, `darmon_point(7,
EllipticCurve('35a1'), 41, 20)` — returns in **9.1 s** with the point
recognized algebraically over `Q(sqrt 41)`:

```
(9681/16400 : -5602879/13448000*alpha - 1/2 : 1)
```

So the toolchain is live and the p-adic integration → algebraic recognition
loop works end to end on a small case.

## Structural conditions: two of three match our setting

The package's curve-finding requires:

1. **`F` of narrow class number 1.** For `F = Q(zeta_32)^+` this **holds**:
   computed directly (GRH class-group bounds), `h = 1` and `h+ = 1`, with
   `disc(F) = 2^31`. Every totally positive unit is a square. ✓
2. **A quaternion algebra over `F` split at exactly one infinite place.** This
   is precisely the indefinite algebra our route produces: the parity count
   `7 infinite places + q0 = 8` is even, so the algebra ramified at 7 of the 8
   infinite places and at `q0` exists, and it is split at exactly one. ✓
3. **Dimension.** `padicperiods` is written for **two-dimensional** components:
   its core is `Thetas(p1,p2,p3,q1,q2,q3)` — three half-periods, i.e. a genus-2
   Jacobian — and recognition runs through Igusa–Clebsch invariants
   (`igusa_clebsch_from_half_periods`, `absolute_igusa_padic_from_xvec`). Our
   `g`-isotypic piece is **16-dimensional**. ✗

## Consequence: we want the integration, not the front end

(3) is not fatal, because our route never wanted their recognition step. The
plan takes the λ-torsion field from **square roots of lattice data** with the
Eisenstein back end (`eisenstein-prototype.md`), not from theta functions and
Igusa invariants — which is fortunate, since genus-16 theta enumeration is
hopeless and the genus-2 Igusa route does not generalise. What we would reuse
is the layer *below*: `cohomology_arithmetic` (overconvergent coefficients),
`integrals`, `homology`, and the S-arithmetic group in `sarithgroup`.

## The pivotal open question for gate 4

There are two quite different group-theoretic settings, and which one the
implementation needs decides whether gate 4 is cheap or impossible:

- **Indefinite / Fuchsian (what `darmonpoints` is built around).** The algebra
  split at one infinite place gives a group acting on `H x tree`, and the code
  obtains a presentation via a fundamental-domain computation (Magma, with
  Page's bundled `KleinianGroups`). Cost scales with the covolume, which grows
  like `disc(F)^{3/2}`. For `disc(F) = 2^31 ~ 2.1e9` that is `~1e14` — on the
  face of it far out of reach.
- **Definite / tree-only (what Cerednik–Drinfeld actually gives us).** CD
  uniformizes `X` q0-adically through the **definite** algebra ramified at all
  8 infinite places — Dembélé's own algebra. Its unit groups are finite modulo
  centre, the S-arithmetic group with `q0` inverted is a tree lattice, and its
  presentation comes from the Brandt/tree quotient **which this directory
  already computes**.

If the period integration can be driven from the definite side, the expensive
Fuchsian presentation never appears and the group data is already in hand. That
is what the plan asserts ("the tree quotient and Hecke action are already in
our hands, and only the overconvergent lifting is new code"), and it is the
single most valuable thing to confirm next — before any implementation effort.

## Next actions

1. Determine whether `sarithgroup.BigArithGroup` can be driven in the
   definite/tree-only regime, or whether every path through the package assumes
   the split-at-one-infinite-place Fuchsian construction. Read
   `sarithgroup.py`'s branch structure; do not benchmark before knowing this.
2. If definite-only is supported: benchmark the S-arithmetic group construction
   for `F` of degree 2, 3, 4 to map growth, then attempt degree 8.
3. If it is not: the fallback the plan already names — a bespoke overconvergent
   lift against our own Brandt data — becomes the plan rather than the
   contingency, and should be scoped early.
