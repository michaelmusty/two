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

## Both follow-up checks, done

### 1. The word problem is NOT Fuchsian — this is the good news

`reduce_in_amalgam` and its workers `_reduce_fast` / `_reduce_in_amalgam`
(sarithgroup.py 805–928) are **purely p-adic**: they embed with
`self.embed(x, prec)`, test membership with `is_in_Gamma0loc`, and descend on
`dval = -min valuation of the entries` against the Bruhat–Tits representatives.
No fundamental domain, no side pairings, no archimedean data appears anywhere
in the reduction. It is already the tree algorithm.

Tracing the rest of the S-arithmetic layer the same way, it touches the
underlying group only through:

- `gens()` — a generating set, as quaternions (`enumerate_elements` merely
  multiplies out words in it)
- `is_in_Gpn_order()` — order membership, algebraic
- `embed()` — the local embedding `B -> M_2(F_q0)`
- arithmetic in `B`

The fundamental domain is only *how the Fuchsian class obtains* `gens()`. In
the definite setting those come for free: `O^x` modulo centre is **finite**
(that is why Brandt class numbers are finite), and by Ihara the S-arithmetic
group `O[1/q0]^x` acts on the tree with finite stabilisers and finite quotient
— the Brandt graph — so generators come from a spanning tree plus edge
elements, all derivable from data we already compute. `B` is split at `q0`
(the definite algebra is ramified only at the 8 infinite places), so
`B ⊗ F_q0 = M_2(F_q0)` and `embed` exists.

One member needs overriding rather than inheriting: `get_BT_reps` finds the
`Nq0+1` coset representatives by *searching* through `Gn.enumerate_elements()`
until local conditions are met — fine for `p = 5`, hopeless as a search at
`Nq0 ~ 2000`. But these are exactly the `P^1(F_q0)` neighbours the Brandt
machinery constructs directly, and the class already has a precedent for
supplying them explicitly (the `_hardcode_matrices` branch).

### 2. The dimension-2 assumption DOES leak into the cohomology layer

Not only into `padicperiods`. In `cohomology_arithmetic`:

- The component search accepts **only** 2-dimensional irreducible pieces:
  `if U0.dimension() == 1: continue`; `if U0.dimension() == 2 and is_irred:
  good_components.append(...)`; `else: # U0.dimension() > 2 or not is_irred`
  re-queues the component to be split further by more Hecke operators. A
  16-dimensional irreducible component is never accepted — it is split at until
  `num_hecke_operators >= bound` and then abandoned. Another driver asserts
  outright: `if U0.dimension() != 2: raise ValueError("Hecke data does not
  suffice to cut out space")`.
- More fundamentally, the lift's normalisation assumes a **rational** `U_p`
  eigenvalue: `scale = ZZ(self.Tq_eigenvalue(p)) ** -1`, where `Tq_eigenvalue`
  is `ans = ZZ(f / f0)` on the class itself. For our component the eigenvalues
  generate a degree-16 field, so `f` is not a scalar multiple of `f0` at all;
  this fails structurally, not merely by coercion.

The first is a driver-level restriction we would bypass, supplying our own
component from the level-`q0` Brandt module. The second is real work: the
overconvergent lift must be normalised over `H ⊗ Q_q0` rather than `ZZ`,
i.e. carried out on the isotypic subspace with eigenvalues in the Hecke field.

## Where that leaves gate 4

The seam is not where the plan guessed. The *group* side is in better shape
than feared — the word problem is already tree-based, and the definite group's
generators are within reach of the Brandt data. The *coefficient* side is worse
— the dimension-2 assumption is not confined to `padicperiods` but reaches into
the eigenclass normalisation of the overconvergent lift, which is the one piece
the plan expected to reuse wholesale ("only the overconvergent lifting is new
code" — in fact the lifting is precisely what needs rewriting for eigenvalues
in a degree-16 field).

## Next actions

1. Scope the overconvergent lift over `H ⊗ Q_q0`: the moment normalisation and
   the `U_p`-eigenvalue scaling, generalised from `ZZ` to the Hecke field. This
   is the true new-code core of gate 4.
2. Build the definite S-arithmetic group class against the four-method
   interface above, overriding `get_BT_reps` from the `P^1(F_q0)` neighbours.
3. Validate the pair on a case where the answer is known — a real quadratic
   field with a 2-dimensional component, reproducing a published
   Guitart–Masdeu abelian surface — before pointing it at degree 8.
