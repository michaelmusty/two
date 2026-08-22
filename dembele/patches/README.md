# Local patches to pinned upstream packages

The HMF package is pinned in `dembele/upstream.lock`. Anything here modifies it,
so results depend on the patch being applied — apply before reproducing.

## `hmf-sparse-hecke.patch` (2026-08-22, gate 3)

`ModFrmHil/definite.m`. Adds sparse assembly for the definite Hecke operator.

**Why.** `HeckeOperatorDefiniteBig` allocates a dense `dim x dim` matrix. At
level `q0` (norm 2401), `dim = 109240`, so that single allocation is **45.5 GB**
— while the operator carries only ~`Norm(p)+1` nonzeros per column (~42 MB).
The package already *stores* the result as a `SparseMatrix`; only the assembly
was dense. Gate 3 needs several operators at once to cut out a common
eigenspace, so this is a hard blocker, not an inefficiency.

**What.** Additive and behaviour-preserving:

- `HeckeOperatorDefiniteBig(..., Sparse:=false)` — new optional parameter.
- In the parallel-weight-2 branch, `Sparse` writes each `+:= 1` straight into a
  `SparseMatrix` instead of extracting, updating and re-inserting a dense block.
- Sparse mode returns early and **does not touch the cache**, so the dense path
  is untouched.
- New intrinsic `InternalHMFRawHeckeDefiniteSparse(M, p)`.

### Second hunk: `BasisMatrixDefinite` — the binding blocker

At parallel weight 2 every direct factor's `basis_matrix` is set to the
**identity** in `HilbertModularSpaceDirectFactors` (which even carries a
`TO DO: get rid of this, and the basis_matrices`). So the block-diagonal
`basis_matrix_big` *is* the identity matrix — and the generic code builds it as
a dense `dim x dim` matrix and obtains its inverse by a **global linear solve**.
At `dim = 109240` that is 45.5 GB twice plus an O(n^3) solve, to construct and
invert an identity. It fires *before* any Hecke work, triggered merely by
`dim := Ncols(M`basis_matrix_big)`, so it — not the Hecke assembly — is what
actually blocks gate 3.

Downstream, `basis_matrix_big` is only ever read through `Ncols`/`Nrows` (four
sites) and `basis_matrix_big_inv` is **never read at all**, so a sparse identity
is faithful. Guarded by `assert &and [IsOne(HMDF[m]`basis_matrix) : ...]` so a
weight/level combination violating the assumption fails loudly instead of
silently returning a wrong basis. Gated on `weight2 and EisensteinAllowed`,
leaving `RemoveEisenstein` and the higher-weight paths untouched.

**Verified.** At level 1, `Matrix(sparse) eq dense` is `true`, and the degree-16
factor of `charpoly(T_31)` that defines `V16` is unchanged. Note the apparent
speedup in that test (995 s dense vs 0.000 s sparse) is a caching artifact —
`get_tps` was already computed. **The patch buys memory, not time.**

For the basis-matrix hunk, level 1 is **not** a valid test — it takes the "easy"
branch and never reaches this code. Tested instead at level 31 (non-easy),
comparing pristine against patched on dimension, Nrows, trace, and the sum and
sum-of-squares of every entry of `T_97`:

    DIM=1460  NROWS=1461  TRACE=4  SUM=143178  SUMSQ=152110

identical on all fields (3502 s vs 3455 s — again memory, not speed).

Apply with:

    cd /Users/musty/hilbertmodularforms && git apply /path/to/hmf-sparse-hecke.patch
