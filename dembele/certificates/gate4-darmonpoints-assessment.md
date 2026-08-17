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

## ANSWERED: definite-only is not supported, and the Fuchsian route is out

**Read of `sarithgroup.py`.** The dispatcher `ArithGroup(base, ...)` has, for a
number-field base, exactly three branches: totally real → `ArithGroup_nf_fuchsian`;
some complex place → `ArithGroup_nf_kleinian`; split algebra `(a,b) == (1,1)` →
`MatrixArithGroup`. `F = Q(zeta_32)^+` has signature `(8,0)`, so **every** path
lands in `ArithGroup_nf_fuchsian`. There is no definite branch.

`ArithGroup_nf_fuchsian._init_geometric_data` is built entirely on the
hyperbolic fundamental domain:

```python
Gm = self.magma.FuchsianGroup(self._O_magma.name())
FDom_magma = Gm.FundamentalDomain()
Uside_magma = Gm.get_magma_attribute("ShimGroupSidepairs")
self.magma.WordProblem(Gm(1))
```

Generators, side pairings, the word problem, `reduce_in_amalgam` — all are
fundamental-domain artifacts. Magma's `FuchsianGroup` moreover *requires* an
order in an algebra split at exactly one real place: a definite algebra is not
merely unsupported here, it has no Fuchsian group at all.

**And the Fuchsian domain is out of reach for our `F`.** Computed (script in
`scratchpad`, formula `vol = 8*pi*d_F^{3/2}*zeta_F(2)*prod_{p|D}(Np-1)/(4*pi^2)^n`):
`zeta_F(2) = 1.3479`, prefactor `571.4`, so for `X` with `D = q0 * (7 infinite)`

| `Nq0` | area | genus ~ area/4pi |
|---|---|---|
| 1663 | 9.5e5 | 75 600 |
| 2111 | 1.2e6 | 95 900 |
| 5003 | 2.9e6 | 227 000 |
| 20011 | 1.14e7 | 910 000 |

A fundamental domain with ~10^5 side pairings at high precision, growing
*linearly in `Nq0`*, against published Voight-algorithm computations that
handle areas of order 10–10^3. This is three or more orders of magnitude out,
and a larger `q0` makes it worse.

*(Correction to the first version of this note: I previously wrote that the
covolume "grows like `disc(F)^{3/2} ~ 1e14`". That omitted the `(4*pi^2)^n`
normalisation; the true area is ~1.2e6. The conclusion is unchanged but the
figure was wrong by eight orders of magnitude.)*

None of this contradicts the mathematics: Cerednik–Drinfeld genuinely
uniformizes `X` q0-adically through the **definite** algebra (ramified at all 8
infinite places, split at every finite prime — including `q0`, so `B ⊗ F_q0 =
M_2(F_q0)` and the S-arithmetic group `Γ[1/q0]` acts on the Bruhat–Tits tree
with finite stabilisers). The tree quotient is the Brandt graph this directory
already computes. It is the *implementation* that offers only the Fuchsian door.

## So the fallback is the plan — and it is well scoped

The plan's contingency ("a bespoke implementation against the Brandt data...
only the overconvergent lifting is new code") is now the route. The encouraging
part is how narrow the seam is: the integration layer is generic over the group
object, requiring only

- `small_group()`, `large_group()`, `gens()`
- `embed()`, `embeddings()` — local embeddings `B -> M_2(F_q0)`
- `prime()`, `base_field()`, `use_shapiro()`
- `wp()` — the uniformizer/Atkin–Lehner element at `q0`
- `reduce_in_amalgam()`, `coset_reps()`, `get_coset_ti()` — the word problem
- `get_hecke_reps()`, `get_covering()`, `subdivide()` — tree structure

That is roughly fourteen methods. Supplying a definite S-arithmetic group class
that implements them against our Brandt data would let `cohomology_arithmetic`
and `integrals` — the overconvergent machinery we actually want — run unchanged.

## Next actions

1. Scope the definite S-arithmetic group class against that interface. The hard
   member is `reduce_in_amalgam` (the word problem): in the Fuchsian case it
   comes from side pairings, and in the definite case it must come from the
   tree quotient / Brandt graph. Everything else is routine.
2. Check how `cohomology_arithmetic` handles the dimension of the Hecke
   eigencomponent — the genus-2 assumption lives in `padicperiods`, but confirm
   it does not leak into the cohomology layer, where we need dimension 16.
3. Only then write code.
