# Computing `Δ'`: the plan, and a simplification that removes the graph

**Date:** 2026-08-27. Prerequisite reading: `gate5-genus16-term-count.md`
(why `Δ'` is the gate-4 go/no-go) and `gate3-closure.md` (the `g`-isotypic
newform space at level `q0` is established). Package facts verified against
`/Users/musty/hilbertmodularforms/ModFrmHil/definite.m` at the lines cited.

## The simplification

The certificate's §3/§5 framed `Δ'` as the determinant of a monodromy pairing
on the `g`-part of the level-`q0` **character group** `X = ker(∂ : Z[edges] →
Z[vertices])`, and flagged the integral kernel of `∂` on a 109240-dimensional
space as the obstacle. That kernel is not needed.

**Claim.** On the `g`-isotypic part the boundary map `∂` is identically zero,
so `X_g` is simply the saturated `g`-isotypic sublattice of the raw Brandt
lattice `Z[edges]`, and the monodromy pairing is the diagonal Brandt mass
pairing restricted to it.

*Why `∂ = 0` on the `g`-part.* `∂` is built from the two degeneracy maps
`M_{q0} → M_1` (down-`p` and down-`1`); `g` is **new** at `q0` (gate 3,
Steinberg), and a newform is by definition in the kernel of both degeneracy
maps to level 1. So the whole 16-dimensional `g`-isotypic space lies in
`ker ∂ ⊗ Q = X ⊗ Q`. Equivalently: the toric part of `B_g`'s reduction at `q0`
is the full 16-dimensional torus (total multiplicative reduction, the
Mumford/CD case), and its character lattice is the `g`-part of the edge lattice.

*Why the pairing is the mass matrix.* `InnerProductMatrixBig(M)` at parallel
weight 2 (`definite.m:748`) is the **diagonal** matrix of masses
`m_i = ulcm/#Stab_i` (unit/stabiliser orders, cleared by their gcd). This is
the Brandt height pairing, which for a Mumford curve *is* the monodromy/length
pairing on the character lattice of the toric reduction (each edge contributes
its length = its mass weight; the graph is the tree quotient and the edge
lengths are the stabiliser masses). So

    monodromy pairing on X_g  =  (diagonal mass matrix) restricted to L_g,

no graph, no boundary operator, no `get_tps`.

This also means the raw operators we already banked are exactly the right
objects: `InternalHMFRawHeckeDefiniteSparse` returns `T_p` on the **raw**
(“Big”) space (`definite.m:141`), the same basis as `InnerProductMatrixBig`,
so `gk_s3_T{31,97,127,191}.m` and the mass vector are directly compatible.

## The quantity

Let `L_g ⊂ Z[edges] = Z^N` (`N` = raw level-`q0` dimension) be the saturated
`g`-isotypic sublattice, rank 16. Let `W = diag(m_1,…,m_N)` be the mass
pairing, and `B` a `Z`-basis of `L_g` (rows). Then the Gram matrix is
`Γ = B W Bᵀ` and

    Δ' = det(Γ) / (N(𝓛)² · D_H)                                          (∗)

where `𝓛` is `L_g` viewed as a rank-1 `O_H`-module (norm of its content) and
`D_H` the Hecke-field discriminant (`gate5-genus16-term-count.md` §3). The
normalisation `N(𝓛)²·D_H` is what makes `Δ' = 1` for a unimodular pairing; the
raw `det(Γ)` is basis-dependent only up to `±1` once `L_g` is saturated.

**Two determinants, as the certificate warned.** `B_g` can be taken as an
abelian subvariety of `Jac` or as a quotient; the character lattices are dual
up to the polarisation, and `det` differs by the square of the polarisation
degree (the congruence number of `g`). Both are computed: `L_g` itself (sub)
and its `W`-orthogonal-projection image / `W`-dual inside the `g`-part
(quotient). The gate-4 feasibility uses the **larger** valuation, i.e. the
determinant that makes the periods most `q0`-divisible.

## Computation

Everything is in hand except one integral linear-algebra step.

1. **Raw space + masses (cheap).** Rebuild the raw ambient `M_{q0}` (weight 2)
   and read `W = Diagonal(InnerProductMatrixBig(M))` — a length-`N` integer
   vector, seconds. Rebuild is needed only for `W`; the operators are banked.
   (Same-session caveat: `W` must be read in the **same session** that built the
   banked operators, or rebuilt together with them, since the basis ordering is
   session-dependent — D26b. The banked `gk_s3_*` were built in one session; to
   pair them with `W` we either re-read `W` in a fresh rebuild of that exact
   space **and check an operator against a banked one**, or rebuild operators
   and `W` together. The plan rebuilds `T_31` alongside `W` and asserts it
   equals `gk_s3_T31` before trusting the pairing.)

2. **`g`-isotypic sublattice over `Z` (the one hard step).** Over `Q`, `L_g⊗Q`
   is the `g`-eigenspace — the kernel of the `g`-part of the factored
   characteristic polynomial of `T_31` on the **new** subspace, 16-dimensional.
   We have this mod 2 (`ker f1(T_31)^2` intersected with new). For `Δ'` we need
   an **integral** basis of the saturated lattice, or — cheaper — only
   `det(Γ) mod p` for enough primes `p`, CRT’d to the integer, since `det(Γ)`
   is what (∗) needs and it is an integer of bounded height. Route:

   - For each of several primes `p` (avoiding 2 and primes dividing masses or
     the congruence number), reduce the banked integer `T_31` mod `p`, factor
     its char poly on the new part, take the `g`-factor `h_p`, and set
     `L_g/p = ker h_p(T_31 mod p)` (rank 16 over `F_p`).
   - `Γ_p = B_p W B_pᵀ mod p` for a row-reduced basis `B_p` of `L_g/p`; but the
     basis choice changes `det(Γ_p)` by a square unit, so instead compute the
     **basis-independent** invariant: `det(Γ)` up to squares is fixed, and its
     exact value needs a consistent integral basis. The clean way: compute
     `L_g` over `Q` by CRT + rational reconstruction of a *projection* (e.g. the
     16 coordinates of an echelon basis onto 16 pivot columns), saturate, then
     `Γ = B W Bᵀ` exactly. The multimodular cost is dominated by one
     `ker h_p(T_31 mod p)` per prime — a sparse nullspace on `N ≈ 1.1·10^5`,
     the same size gate 3 handled mod 2 (~minutes each).

3. **Normalisation.** `N(𝓛)` from the `O_H`-module structure of `L_g` (the
   `H`-action is `T_31` restricted to `L_g⊗Q`, identified with `H` via its
   minimal polynomial); `D_H` is known (`5^14·89^7·661^4`). Compute both the
   sub and quotient determinants (§ above) and report `Δ'` for each.

## Cost estimate (to be replaced by measurement)

- Rebuild raw `M_{q0}` + one `T_31` for the `W`-consistency check: ~1 h
  (matches gate 3).
- Per prime `p`: reduce banked `T_31` mod `p` (dense-ish `GF(p)` from the
  sparse integer matrix; sizes as gate 3) + factor char poly on new part
  (already have the factor shape) + one rank-16 nullspace ≈ 10–30 min.
- Number of primes: `det(Γ)` has height ≤ `16·log₂(max mass) + log₂(N!)/…` —
  bounded by a few thousand bits pessimistically; 20–50 primes of ~60 bits.
  Total ≈ 1–2 core-days, fully parallel across primes, **no host-scale job**.

The prototype (`../magma/49_delta_prime_proto.m`) validates steps 1–3 on level
31 over `Q` exactly (small `N`), where the whole `Δ'` can be computed in one
session without the multimodular machinery, checking: `InnerProductMatrixBig`
alignment with the raw operators, `∂ = 0` on the new part (newforms orthogonal
to old under `W` is the check), saturation, and the sub/quotient determinant
pair. Only after it passes is the `q0` multimodular run worth launching.

## Correction 2026-08-31 (D31): the pairing diagonal is the stabilizer orders

The claim above that the pairing is "the diagonal **Brandt mass** pairing
(`InnerProductMatrixBig`)" is off by a reciprocal. Empirically (level 1 and
level q0): with the Eichler-mass diagonal `m_i = (ulcm/g)/e_i` the
self-adjointness `W_i T_ij = W_j T_ji` FAILS; the unique consistent diagonal,
derived from `T`'s entry ratios along the (connected) support graph, is
`W_i = e_i`, the **stabilizer orders** — the classical Brandt relation
`e_j T_ij = e_i T_ji`, and the Cerednik–Drinfeld monodromy pairing's edge
lengths (Gross, Ribet). The relation `m_i e_i = ulcm/g` (basis-independent;
`= 48` at q0, `e_i ∈ {1,2,3,4,8,16}`) converts the banked mass vector without
any rebuild; `dp_Wtrue.m` on chatelet is the converted vector in the
`dp_T31.m` basis, and self-adjointness holds on all 3 494 618 support entries
(`54_delta_prime_q0_wfix.m`). Everywhere `W` appears below, read the
stabilizer-order diagonal. The exposed intrinsics are
`InternalHMFRawStabOrdersDefinite` (the pairing) and
`InternalHMFRawInnerProductDefinite` (the package's dual mass normalization,
kept for cross-checks).

## Addendum 2026-08-31: the q0 implementation route (revises step 2)

Step 2 above said "take the `g`-factor `h_p`" per prime without saying how the
`g`-factor is known. Working out the costs shows the naive reading — a full
`charpoly(T_31 mod p)` per odd prime — is **infeasible**: dense linear algebra
at `N = 109240` over a word-size odd prime is 47–95 GB (no bit-packing, unlike
mod 2) and ~`N³ ≈ 1.3·10^15` field ops ≈ day(s) per prime. The route below
avoids every dense-mod-`p` object of size `N²`.

**(0) `d_g` is a first-class unknown, and gate 4 depends on it.** Gate 3 gives
the new `f1`-primary part dimension 16 = `deg(f1)²`, i.e. residual multiplicity
**2**, versus multiplicity 1 at level 1. Possible char-0 orbit structures: one
degree-16 orbit whose two primes over 2 both reduce to `f1`-systems; two
degree-16 orbits splitting `(8,8)` like `H` (one the `C8`-mirror carrying the
`f2` side); or **one degree-32 orbit** with `(16,16)` over the two mod-2
systems. In the last case `dim B_g = 32` and the gate-4 term count is
`~M^32/Δ'` — almost certainly a no-go. So the first output of the q0 run is
`d_g`, not `Δ'`.

**(a) Identify `h_g` 2-adically (cheap: everything is mod 2 or 32×32).**
The mod-2 `f1`-primary block `G = ker f1(T_31)² ` (dim 32, gate 3) is the
reduction of the 2-adic `m`-primary lattice block. Hensel-lift a basis of it
to `Z/2^k`, `k = 192`, by the standard step: solve `P^e·C ≡ rhs (mod 2)` where
`P = f1(T_31) mod 2` and `P^e` is computed by ~`log e` dense **mod-2**
(bit-packed, 1.5 GB) matrix squarings. Restrict `T_31` to the lifted block:
`cp_m32 mod 2^k` (32×32 charpoly, trivial). Divide by `u1²` where `u1` is the
degree-8 Hensel factor of the **exact** level-1 degree-16 factor `g16 ≡ f1`
(a 16-degree polynomial factorization over `Z_2`, trivial): the quotient
`h' (deg 16, mod 2^k)` is the charpoly of `T_31` on the **new** `f1`-block.
Repeat on the `f2` side for `h''`. Deligne bounds the true coefficients:
roots `|a| ≤ 2√31`, so a degree-16 factor has coefficients `< 2^70` and a
degree-32 factor `< 2^140`; with `k = 192` the balanced lift of whichever of
`h'`, `h''`, `h'·h''` is a global factor is exact and the coefficient bound
rejects the others (a non-global product has ~`2^k`-size lifted coefficients).
This decides `d_g` and produces `h_g ∈ Z[z]`.

**(b) Verify `h_g` and build `L_g` mod word-size primes (sparse only).**
`W` is positive definite and `T_31` is `W`-self-adjoint, so `T_31` is
diagonalizable over `R` and the global minimal polynomial `μ` is squarefree.
Per word-size prime `p`: compute `μ mod p` by Wiedemann (Berlekamp–Massey on
`u·T_31^i·v`, `~2N` sparse matvecs at ~3.5·10^6 nnz ⇒ tens of minutes);
**check `h_g | μ mod p`** — this is the per-prime verification of (a). Then
project random vectors: `v_g = (μ/h_g)(T_31)·v` (Horner, `~N` matvecs,
~10 min) lies in `L_g ⊗ F_p` with generically nonzero `g`-component since `μ`
is squarefree; ~20 vectors span. Reduced echelon form w.r.t. a fixed pivot
set is canonical, so the per-prime bases are CRT-compatible: CRT + rational
reconstruction gives `B ⊗ Q`, clear denominators, saturate, then
`Γ = B W Bᵀ` and `det Γ` **exactly over Z** (16×16 or 32×32 — tiny). Add
primes until the reconstruction stabilizes and `B·h_g(T_31) = 0` holds over
`Z` (a posteriori exact certificate). Primes where the projection drops rank
(dividing a resultant) are skipped.

**Cost.** (a): one-off, dominated by ~7–8 dense mod-2 squarings ≈ minutes each
+ the lift solves; well under a day, ~4 GB. (b): ~1–3 h per prime, fully
parallel across chatelet lanes; expected 10–40 primes. No step allocates a
dense `N×N` matrix over an odd-prime field. This keeps the plan's 1–2
core-day estimate honest.

**Prerequisite** (step 1, unchanged): `50_delta_prime_q0_W.m` reads `W` and
asserts a rebuilt `T_31` equals the banked `gk_s3_T31`, tying `W`'s basis to
the banked operators. If that assert fails, all four operators must be rebuilt
with `W` in one session before (b).

## Honest caveats

- The identification “Brandt mass pairing = CD monodromy pairing” is standard
  for Mumford curves (Ribet; Cerednik–Drinfeld) but is asserted here at the
  level of the certificate, not proved for this base field. The prototype tests
  its two checkable consequences (`∂=0` on new; the pairing is positive
  definite on `L_g`); a wrong identification would most likely show as a
  non-integral or non-definite `Γ`.
- Sub vs quotient and the polarisation factor are exactly the ambiguity §above
  and `gate5-genus16-term-count.md` flag; both determinants are reported and the
  feasibility read from the more favourable one, with the gap noted.
- `Δ'` fixes the term count but not the recognition precision `M_rec`
  independently; the two together decide gate 4, and `M_rec` still needs the
  dimension-2 calibration `roadmap-reevaluation.md` recommended. `Δ'` is the
  half that is computable now with what gate 3 produced.
