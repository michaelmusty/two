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
