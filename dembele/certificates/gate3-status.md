# Gate 3: blocked by the HMF package's dense implementation at dim 10^5

**Date:** 2026-08-22. `q0` = prime of F above 7, norm 2401 (D23).

## The space is fine; the implementation is not

`Dimension(M)` at level `q0` is **109240**, computed in **14 seconds**. The
mathematics is not the problem. The problem is that
`ModFrmHil/definite.m` is written for spaces of dimension in the hundreds, and
materialises dense `dim x dim` objects. Two separate places, both fatal at
`dim = 109240` (a dense `dim x dim` matrix is **45.5 GB**):

1. **`BasisMatrixDefinite`** (line ~944). `basis_matrix_big` is assembled
   **block-diagonally** from the 58 direct factors — then stored as one dense
   `109240 x 109240` matrix, and inverted *globally*:

       Binv := Transpose(Solution(Transpose(B), IdentityMatrix(BaseRing(B), Nrows(B))));

   For a block-diagonal matrix the inverse is the block-wise inverse: 58 blocks
   of ~`2402 x 2402` (23 MB each), trivially invertible. This is the allocation
   that actually kills us — it happens *before* any Hecke work, and is triggered
   merely because `HeckeOperatorDefiniteBig` reads `dim := Ncols(M`basis_matrix_big)`.

2. **Hecke assembly** (line ~1072), `Tp := MatrixRing(F, dim) ! 0`. Same 45.5 GB,
   for an operator with ~`Norm(p)+1` nonzeros per column. **Already patched**
   (`dembele/patches/hmf-sparse-hecke.patch`, verified identical to dense at
   level 1) — correct, but not the binding constraint.

## This work is not optional

Gate 4 needs the level-`q0` Brandt module too — it *is* the Bruhat–Tits tree
quotient, and the plan's own cost figure `58*(Nq0+1)` is exactly this space. So
a sparse/block-aware definite implementation at `dim ~ 10^5` is on the critical
path regardless of what we decide about gate 3.

## The fork

Gate 3 was specified as "**verify**, don't trust mod-2 level-raising theorems" —
written when verification looked cheap. It isn't: it needs the same package
surgery as gate 4.

**Option A — do the surgery now.** Patch `BasisMatrixDefinite` to keep the
block-diagonal structure (sparse storage, block-wise inversion), then gate 3 is
ordinary sparse linear algebra mod 2. Cost: a focused piece of work, but it is
gate 4's prerequisite anyway, so nothing is wasted.

**Option B — accept the theorem for gate 3, spend the effort on gate 4.**
Ribet-style level raising *guarantees* the form exists once the hypotheses hold,
and those are cheap to check: `rho-bar` irreducible (its image is `SL_2(F_256)`,
so yes), `q0` prime to the level (yes), and `abar_{q0} = 0` — which is precisely
what the scan measured, since `Nq0 = 2401` is odd so `±(Nq0+1) ≡ 0 mod lambda`.
The congruence would then be verified *inside* gate 4, where the level-`q0`
module gets built regardless.

**Recommendation: A, but framed as gate-4 groundwork rather than gate-3
verification.** The surgery is unavoidable; doing it now buys the gate-3
verification as a by-product, and the by-product is exactly the check the plan
wanted.
