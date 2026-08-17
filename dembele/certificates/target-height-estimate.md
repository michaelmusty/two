# The height of the target polynomial: the last binding unknown

**Date:** 2026-08-16. Follows `gate4-dim2-calibration.md`, which reduced the
whole precision question to one number: `H`, the height of the coefficients of
a degree-257 defining polynomial of `L/Q(sqrt 2)` (equivalently `L/F`), since

    M ~ 0.7 * log10(H)        (measured recognition law, recognition degree 2)

and the gate-4 kernel cost goes as `M^3`.

## Ramification structure at 2, and a byproduct

Wild inertia at 2 lies in the 2-Sylow of `SL_2(F_256)`, the unipotent subgroup
`U = {[[1,b],[0,1]]}` of order 256. On `P^1(F_256)` — the 257 points — `U`
fixes `infinity` and acts on the affine line by translation `x -> x + b`, hence
**simply transitively** on the other 256. So `L` has, above 2, one unramified
prime and one prime with `e = 256`, `f = 1`.

With the wild different bound `d <= e - 1 + v_2(e) e = 255 + 8*256 = 2303`, and
`disc(F) = 2^31`, the tower formula gives

    v_2(disc L/Q) <= 2303 + 31*257 = 10270,   [L:Q] = 2056
    rd(L) <= 2^(10270/2056) = 31.9

**Byproduct worth recording independently: `L` cannot be totally real.**
Odlyzko's asymptotic lower bound for totally real fields is `rd >= 60.8`, and
`31.9 < 60.8`. So `E` has complex places — complex conjugation acts
nontrivially, necessarily as a unipotent involution. (Consistent with the
totally imaginary bound `22.3 < 31.9`.) This is a genuine structural constraint
on Dembélé's field obtained from ramification alone, and it is checkable against
any explicit polynomial we eventually produce.

## Why the height is not determined by the degree

Tempting but wrong: "a degree-257 polynomial has a middle coefficient summing
`C(257,128) ~ 1e76` products, so `log10 H >= 76`". Cancellation defeats this —
`Phi_257(x)` has degree 256 and every coefficient equal to 1. Degree alone
gives **no** lower bound on the height. The height is a property of how
*structured* the field is:

- abelian/cyclotomic-like: heights of order 1;
- generic of this degree and root discriminant: astronomically large.

`L` is nonsolvable with `rd <= 32` — small — but nothing forces the cyclotomic
kind of structure. So the height must be estimated empirically against the
right comparison class, not derived.

## The right comparison class, and what it suggests

The closest published analogue is **Bosman's explicit mod-`ell` Galois
representations for level-one forms** (Edixhoven–Couveignes et al.): degree
`ell+1` fields ramified only at `ell`, cut out by a nonsolvable modular mod-`ell`
representation. That is our situation with `(ell+1, ell)` in place of
`(257, 2)`: same provenance (modular), same shape (one ramified prime,
nonsolvable, projective degree `ell+1`).

Those polynomials are notoriously large — the computations were celebrated
precisely because the heights made them hard, and they run to degree 24 only.
Our target is degree **257**.

Consequences under a range of assumptions, using `M ~ 0.7 log10(H)` and the
optimised-kernel figure of 85–2000 core-hours at `M = 20`:

| `log10 H` | `M` | kernel cost, 16 classes |
|---|---|---|
| 30 | ~21 | 100–2 000 core-h — days |
| 75 | ~53 | 1 500–35 000 core-h — weeks |
| 140 | ~100 | 10 000–250 000 core-h — marginal |
| 280 | ~200 | 85 000–2e6 core-h — out of reach |

So the route survives if `log10 H` is in the tens, is painful in the low
hundreds, and dies above that.

## What to do about it

This is now **the** question for the project, ahead of the scan and ahead of
the kernel rewrite, because it decides whether either is worth doing. It is
also cheap to attack, in increasing order of effort:

1. **Read off Bosman's actual heights** for `ell = 13, 17, 19, 23` and fit the
   growth in degree. Published data; no computation needed. This gives an
   empirical `log10 H` vs degree curve for exactly the right family.
2. **Compute a small analogue ourselves end to end**: a mod-`lambda`
   representation of a Hilbert modular form over a small totally real field with
   projective degree ~10–30, ramified at one prime, and measure the height of
   its reduced defining polynomial. More work, but on our own machinery.
3. If both say the heights are in the tens: proceed to the kernel rewrite. If
   they say hundreds: the recognition front end must change — recognise
   something other than a defining polynomial (e.g. an invariant of smaller
   height, or the field via its ray-class/relative structure), or the route
   ends here and the front-end question reopens.

Note that (3) is not obviously hopeless even in the bad case: what we need is
*the field*, and a defining polynomial is only one presentation of it. A
presentation adapted to the tower `L/F` with its `e = 256` local structure could
be far smaller than a generic degree-257 polynomial over `Q(sqrt 2)`.

---

## Answered with published data: Bosman's Table 1

`arXiv:0710.1237`, Table 1 — polynomials for projectivised mod-`ell` level-one
representations, degree `ell+1`, Galois group `PGL_2(F_ell)`, ramified only at
`ell`. Exactly our family one scale down. Largest coefficient by (weight,
`ell`):

| deg | `log10 H` (by weight `k`) |
|---|---|
| 12 | 2.5 (k=12) |
| 14 | 3.4 (k=12) |
| 18 | 5.3 (12), 6.1 (16), 8.3 (18) |
| 20 | 4.7 (12), 6.8 (16), 9.3 (18), 8.8 (20) |
| 24 | 8.6 (16), 11.4 (18), 12.1 (20), **15.4 (22)** |

Two extrapolations to degree 257:

- linear fit `log10 H = 0.809 n - 8.0` → **`log10 H ~ 200`**
- structural model `log10 H = n log10(2) + (n/2) log10|alpha|`, whose implied
  `|alpha| ~ 1.47` is impressively stable across the table → **`log10 H ~ 99`**

So `log10 H` in the range **100–200**, giving `M ~ 70–140` and a kernel cost
multiplier of **43–318x** over the `M = 20` baseline. Against the optimised
kernel's 85–2000 core-hours at `M = 20`, that is 3 700–630 000 core-hours:
about a week on 24 cores at the optimistic end, three years at the pessimistic.

### One strong effect in our favour

The table shows height rising sharply with **weight**: at degree 24, `log10 H`
goes 8.6 → 11.4 → 12.1 → 15.4 as `k` goes 16 → 18 → 20 → 22, a slope of ~1.1
per unit weight. **Our form has parallel weight 2** — below every entry in
Bosman's table, which starts at 12. Naive extrapolation of that slope down to
`k = 2` runs negative, so it clearly saturates, but the direction is
unambiguous: minimal weight is the small-height end of this family. The 100–200
estimate, fitted on weights 12–22, is therefore likely an **over**estimate.

### Byproduct: a much sharper discriminant

Bosman's Corollary 2 gives, for exactly this configuration,
`v_ell(Disc(K/Q)) = k + ell - 2`. The analogue here (`k = 2`, `q = 256`) is
`v_2(disc(L/F)) = 256`, far below the worst-case wild bound of 2303 used above.
That gives `rd(L) = 2^((256 + 31*257)/2056) ~ 16.0`, and correspondingly
**strengthens the "not totally real" conclusion**: 16.0 is far below Odlyzko's
60.8, and now also below the totally-imaginary bound 22.3 — which would force
`L` to have both real and complex places rather than being totally imaginary.
Worth checking carefully, since it is a sharp structural claim resting on an
analogy across `F_ell` to `F_256` that has not been verified.

## Verdict

**The height does not kill the route.** The honest position: `M` is probably in
the 70–140 band and plausibly lower given weight 2, which makes gate 4 range
from a week to a few years of compute depending on the kernel constant — and
that constant (85 vs 2000 core-hours at `M = 20`, a 24x spread) is now the
dominant uncertainty, ahead of the height. Narrowing it means prototyping the
kernel's inner loop, which is a day's work rather than the full month.
