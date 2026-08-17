# Roadmap reevaluation, 2026-08-16

Prompted by: are we spending effort in the right place? Written after a day of
gate-4 scoping that moved several numbers, in both directions.

## Bottom line

The route is still right and I would not change it. But the **binding
uncertainty has moved**, and effort should move with it. It is no longer the
scan, nor the group theory, nor the degree-16 Hecke field. It is the
**precision required at the recognition step** — which is calibratable *now*,
at small scale, independently of gate 1, and which determines how much of the
scan window is even usable.

## What today retired

The plan's "scale frontier vs our demand" listed three gaps. Two are now much
smaller than they looked:

| gap | plan's statement | now |
|---|---|---|
| Hecke field degree | "≤ 2 vs **16**" | **retired.** The 16-dimensional isotypic component is `Q`-rational (a sum of Galois conjugates) and the overconvergent lift is `Q_q0`-linear, so it runs on a basis and never meets `H`. `U_q0 = ±1` is a scalar on the whole component (verified), so the lift's one eigenvalue normalisation survives untouched and the slope is 0, making the lift unique. |
| uniformizing prime | "small vs `Nq0` possibly in the hundreds" | **partly retired.** Measured: ~110 core-hours for all 16 classes at `Nq0 ~ 2000`, `M = 20`. But see the new risk below. |
| base field degree | "≤ 3–4 vs **8**" | **unchanged in kind, but the CD side is confirmed clear.** The archimedean route is dead as the plan said (I recomputed the Shimura curve: area 1.2e6, genus ~96 000 at `Nq0 ~ 2111`, growing linearly in `Nq0`). CD avoids it, and `reduce_in_amalgam` turns out to be purely p-adic, so the tree word problem needs no fundamental domain. |

## What today revealed

**Gate-4 cost scales as `Nq0^2 · M^2`.** Positions `~58(Nq0+1)` times cosets
`(Nq0+1)` times `~M` iterations times a moment cost linear in `M`. Calibrated
on the measured 5.3 us inner operation, for **all 16 classes**:

| `Nq0` | `M = 20` | `M = 60` | `M = 100` |
|---|---|---|---|
| 257 | 2 core-h | 16 core-h | 45 core-h |
| 2111 | 122 core-h | 1 100 core-h | 3 050 core-h |
| 5003 | 685 core-h | 6 160 core-h | 17 100 core-h |
| 20011 | 10 900 core-h | 98 000 core-h | 273 000 core-h |

The classes are independent, so wall-clock divides by the cores available. Even
so the bottom-right corner is 31 core-years: **there is a practical ceiling on
`Nq0`, and where it falls depends entirely on the precision `M` we need.**

## The consequence nobody had priced

The scan's value is **front-loaded**, and more sharply than "big primes cost
more to scan". A hit's usefulness decays quadratically in its norm:

| window | primes | cumulative hit odds | gate-4 cost of a hit there |
|---|---|---|---|
| norm ≤ 3000 | 56 | 19.7% | cheap |
| norm ≤ 5000 | 83 | 27.7% | affordable |
| norm ≤ 8000 | 124 | 38.5% | painful |
| norm ≤ 20000 | 288 | 67.6% | fatal at high `M` |

The plan's headline "≈ 2/3 odds" counts hits we may not be able to exploit. If
recognition needs `M ~ 100`, the usable window is roughly `norm ≤ 5000` and the
effective odds are **~28%**. If `M ~ 20` suffices, most of the window is usable
and it really is ~68%. That factor-of-two in the project's success probability
is decided by a single unmeasured quantity.

## The one link never tested

`period lattice -> 2-torsion -> algebraic recognition`. We have never run it, at
any dimension. It is published for elliptic curves (Guitart–Masdeu–Şengün) and
abelian surfaces (Guitart–Masdeu), which is real support, but the plan's
argument that our case is *easier* —

> we need 2-torsion, not equations — for a multiplicatively uniformized variety
> that is square roots of period-lattice generators, far below theta-level
> difficulty

— is plausible and unverified. It is also precisely the claim that sets `M`.
Note the precision side is affordable in isolation: `M = 100` at `Nq0 = 2111`
gives `q0`-adic precision `~10^330`, enough to recognize coefficients of height
`~10^165` in `Q(sqrt 2)`. The question is not whether we can reach high
precision; it is how much we need.

## Honest odds

- gate 1, a hit **we can use**: 0.28–0.68 depending on the above
- gate 3, congruence verifies: ~0.95 (expected theory, cheap to check)
- gate 4, implementation works at degree 8: ~0.6 (scoped today; group side
  reusable, three new pieces, no unknown mathematics)
- gate 5, recognition inside affordable precision: ~0.5 (untested)

Product: **roughly 8–19%**. That is not discouraging for a problem of this
kind, but it does say the effort should go where the uncertainty is largest per
unit cost — and that is gate 5, not gate 1.

## Recommendation

1. **Do the dimension-2 end-to-end calibration next.** Take a published
   Guitart–Masdeu abelian surface, compute its `p`-adic period lattice with the
   existing (unmodified, dimension-2-supported) `darmonpoints` stack, take
   square roots, recognize the 2-torsion field, and record **the precision
   actually consumed**. This single experiment (a) validates the chain we have
   never run, (b) measures `M`, (c) therefore tells us how much of the scan
   window is worth anything, and (d) exercises the exact code we would extend.
2. **Keep the scan running** — it costs no attention now that it is
   self-healing — but treat **norm ~5000 as a decision point** rather than
   grinding to 20000 on autopilot.
3. **Defer** building the definite S-arithmetic group class until (1) says the
   endgame closes. It is the largest build item and it is worthless if gate 5
   does not.
4. **Stop** spending on: the genus-2 corner (parked, and it verifies a closed
   negative arc), and gate-1 micro-optimisation (the cost is `get_tps`, which
   we cannot improve).

## What would kill the route

If the dimension-2 calibration needs precision beyond roughly `M = 40` *at
small scale*, then degree 8 with `Nq0 ~ 2000` will need more than we can afford,
and the honest conclusion is that this front end does not reach. In that case
the right response is not to build gates 3–5 anyway, but to go back to the
front-end question — the same conclusion the 2026-08-04 exhaustion audit
reached, with one more door now closed behind us.
