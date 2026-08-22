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

**Verified.** At level 1, `Matrix(sparse) eq dense` is `true`, and the degree-16
factor of `charpoly(T_31)` that defines `V16` is unchanged. Note the apparent
speedup in that test (995 s dense vs 0.000 s sparse) is a caching artifact —
`get_tps` was already computed. **The patch buys memory, not time.**

Apply with:

    cd /Users/musty/hilbertmodularforms && git apply /path/to/hmf-sparse-hecke.patch
