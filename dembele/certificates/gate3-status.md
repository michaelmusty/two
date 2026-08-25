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


---

## Update 2026-08-22 (evening): enablers DONE and verified; algorithm needs redesign

**Both patches verified and deployed.** At level `q0` the probe now runs:

    T_31 sparse: 109241 x 109241, 3,494,618 nonzeros, 31.99 per column [963 s]
    expected ~Norm(p)+1 = 32 per column
    dense would have been 44.46 GB

Exactly `Nell+1` neighbours per vertex — the Brandt matrix is what it should be,
built in 16 minutes and under a GB. The 45.5 GB blocker is gone.

**But the drafted verification (`38_gate3_congruence.m`) is infeasible as
written.** It calls `Kernel(Evaluate(g16bar, T2))` on a dense GF(2) matrix.
Dense GF(2) multiplication at `n = 109240` is ~`n^3/64 = 2e13` word ops, ~5 h
each; Horner on a degree-16 polynomial needs 16 of them, per prime — ~350 h.
The mistake was reasoning "GF(2) dense is only 1.49 GB, so it's cheap": the
*storage* is cheap, the *multiplication* is not.

**Measured alternative.** The operator is sparse, so:

| | cost |
|---|---|
| one sparse matvec | 3.5 ms |
| Wiedemann, ~`2n` matvecs | 765 s (13 min) |

so anything expressible in matvecs is ~1000x cheaper than the dense route.

**What still needs designing.** "Cut out the eigenspace" is not a kernel
computation at this size. A workable shape:

1. Wiedemann for the minimal polynomial of `T_ell mod 2`; check `g16bar` divides.
2. Build the projector onto the `g16bar`-primary part from that factorisation and
   apply it to random vectors — each application is `O(deg)` matvecs.
3. The projected vectors span the eigenspace; get its dimension by rank of a
   modest dense block (`k x n`, cheap for small `k`).
4. Restrict `U_q0` to it and check `+-1`.

Step 4 needs `U_q0` at the level prime, whose cost is not yet measured — at
level 1 the norm-2401 operator took 36 h, and the level-prime operator is a
different (and possibly cheaper) computation, but that is an assumption, not a
measurement.

**The fork from the top of this file is therefore still live**, and better
informed: the enabling surgery is done and was worth it regardless (gate 4 needs
it), but a *direct* gate-3 verification is a further algorithmic project. The
alternative remains to verify Ribet's hypotheses — `rho-bar` irreducible (image
`SL_2(F_256)`), `q0` prime to the level, `abar_q0 = 0` (measured) — and let the
congruence be confirmed inside gate 4, where the same module is built anyway.


---

## 2026-08-23: first positive evidence for the congruence at q0

`charpoly(T_31 mod 2)` at level `q0` (degree 109241, 3341 s) against the
residual invariant from level 1:

    g16bar = f1 * f2,  two DISTINCT irreducible factors of degree 8
    f1 : multiplicity 4 at level q0
    f2 : multiplicity 2 at level q0

**The factorisation is the expected shape.** `H` has degree 16 with two primes
`lambda, lambda'` above 2, each of residue degree 8 — Dembele's two residual
systems — so the degree-16 invariant splits into one degree-8 factor per system.

**The asymmetry is the signal.** Each level-1 newform yields *two* oldforms at
level `q0` (the two degeneracy maps), so the oldform baseline is multiplicity 2
for each factor. Observed: `f2` sits exactly at baseline (excess 0), while `f1`
is at 4 — an **excess of 2** unaccounted for by oldforms.

**And the asymmetry is the one gate 1 predicted.** The hit was
`const2val = 8`, i.e. `v_lambda + v_lambda' = 1`: exactly *one* of the two
residual systems has `abar_q0 = 0`, so exactly one should level-raise. Precisely
one factor shows excess. The two independent computations — a 36 h Hecke
eigenvalue valuation at level 1, and a mod-2 characteristic polynomial at level
`q0` — agree on *which side* the phenomenon sits.

### What this does and does not establish

Established: there are forms at level `q0`, beyond the oldforms, whose residual
Hecke system at 31 matches one of Dembele's two systems — and it is the system
gate 1 singled out.

Not yet established:

1. **Steinberg at `q0`.** The excess forms must have `U_q0 = ±1`. Until that is
   checked they are only "extra forms with the right residual system at 31".
2. **One prime is not an eigensystem.** Matching at `ell = 31` alone leaves room
   for coincidence; the same excess should appear at further `ell`, and the
   saved charpoly makes each additional prime cheap (the operator, not the
   charpoly, is the cost).
3. **Why the excess is 2 rather than 1** — consistent with a new form whose
   Hecke field contributes `2 x 8`, or with two new forms, but not yet pinned
   down.

The charpoly is now banked (`gate3_charpoly_q0.m`), so none of this needs
recomputing.


---

## 2026-08-23: the excess reproduces at a second prime

`charpoly(T_97 mod 2)` at level `q0` (degree 109241, 5275 s), against the
`ell`-specific invariant `charpoly(T_97|V16) mod 2` from level 1:

| `ell` | one degree-8 factor | the other |
|---|---|---|
| 31 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |
| 97 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |

**A genuine second draw, not the same measurement twice.** The invariant is
`ell`-specific: for `ell = 97` it is the degree-16 charpoly of `T_97` restricted
to `V16` — a different polynomial — tested against a different operator at level
`q0`. The two computations share only `V16` itself.

**Three independent things now agree.** (i) The gate-1 valuation
`const2val = 8` says `v_lambda + v_lambda' = 1`: exactly one residual system has
`abar_q0 = 0`. (ii) At `ell = 31` exactly one degree-8 factor carries excess.
(iii) At `ell = 97` the same. Coincidence is a strain.

**Two more confirmations that the patched assembly is correct:** the operators
have 31.99 and 97.94 nonzeros per column against the predicted `Norm(p)+1` of
32 and 98.

### Still not established

1. **Same subspace.** Multiplicities cannot see whether the `ell = 31` and
   `ell = 97` excesses come from the *same* forms — that is a claim about a
   common eigenspace.
2. **Steinberg.** The excess forms must satisfy `U_q0 = ±1`.

One computation settles both: restrict to the excess subspace and compute
`U_q0` there. That is strictly better than adding a third prime, and is the next
step. Cost still unmeasured — the operator is at the level prime, norm 2401,
and the level-1 operator at that norm took 36 h.

### Cost note

The `ell = 97` charpoly took 5275 s against 3341 s for `ell = 31` at the *same*
dimension over the same field: Magma's `GF(2)` charpoly cost is data-dependent,
not a function of dimension alone. Relatedly, a 6 GB memory cap set from the
`ell = 31` job's 4.6 GB peak was too small for `ell = 97`'s ~7.5 GB. Bank
intermediates; do not extrapolate a constant from one observation.


---

## 2026-08-25: chunking is useless, and U_q0 is unnecessary

**The chunking plan failed its own test — informatively.** Column-chunked
assembly is *correct*: at level 31, four disjoint column blocks summed to
139052 nonzeros against the full operator's 139052, `IDENTICAL=true`. But the
timings kill the idea:

    full operator   3149.79 s
    chunk 0..3      0.43 / 0.40 / 0.41 / 0.36 s

Essentially the entire cost is `get_tps`, the quaternion-element enumeration,
which is **per-prime, not per-column**, and was cached in-process. Across
*separate* processes — which is what checkpointing means — every chunk repeats
the enumeration, so ten chunks cost ten full builds: 400+ h instead of 40.
**Column chunking checkpoints nothing.**

**But U_q0 is not needed at all.** A newform of level exactly `q0` with trivial
character is Steinberg at `q0`, so *newness* is sufficient — and newness is a
statement about the degeneracy maps, not about `U_q0`. The two maps from level 1
span the old subspace; if the excess subspace is not contained in that span, the
excess is new, hence Steinberg.

And the degeneracy maps are cheap: `DegUp1Big` / `DegDown1Big` / `DegUppBig`
call `get_tps` **zero** times (against 2 in `HeckeOperatorDefiniteBig`) — they
are built from the `P^1`/fundamental-domain combinatorics alone, with no
element enumeration at norm 2401. That is the entire 40–50 h cost avoided.

### Revised plan for finishing gate 3

1. Build the two degeneracy maps level 1 → level `q0` (cheap, no `get_tps`).
2. Isolate the `f1`-primary subspace at level `q0` mod 2 (dimension `<= 32`,
   from the already-banked `T_31`/`T_97`).
3. Compare with the old subspace: `dim(f1-primary and old)` against
   `dim(f1-primary)`. The oldform prediction is 16 of 32; a strictly larger
   `f1`-primary space means new forms are present.
4. New + level exactly `q0` + trivial character ⇒ Steinberg. Gate 3 closed.

This also settles the "same subspace" question, since it is performed on the
subspace the excess actually occupies.
