# Does `λ`-torsion localize in the Cerednik–Drinfeld uniformization? (paper-math hole 1)

**Date:** 2026-09-04. **Question** (stocktake-2026-09-01 §2(b), q.1; D32 option (b)): in
the q₀-adic uniformization `B_g = T_g/Λ_g` of the Steinberg lift `g` at the auxiliary
prime `q₀`, does `B_g[λ]` depend only on the `λ`-isotypic block of `(X_g, Λ_g)` — so that
`d_g = dim B_g > 16` (D32) stops mattering and gate 4 can run on the banked rank-16 2-adic
block plus a few q₀-adic periods?

**Answer.** *Yes as a Galois module — and that is exactly why it does not help.* The
localization is an elementary Kummer-theory statement about the **local** module at
`q₀`; the route's global step (algebraic recognition) goes through algebraic functions on
`B_g`, whose complexity is governed by `dim B_g = d_g`, and the `λ`-block is not the
2-torsion of any lower-dimensional variety. Hole (1) is closed; it collapses into hole (2).

## 1. Setup

`X/F` the Shimura curve of discriminant `q₀` (indefinite algebra, 7 real places + `q₀`),
`J = Jac X`, `T` its Hecke algebra; `g` a newform of level `q₀`, Steinberg at `q₀`, with
`ρ̄_{g,λ} ≅ ρ̄_f` for a prime `λ | 2` of `O = O_{K_g}`, `O/λ = F₂₅₆`, `d_g = [K_g : Q]`.
`B_g` the `g`-isotypic quotient of `J`, `dim B_g = d_g`, with `O`-action.

Cerednik–Drinfeld: over `K := F_{q₀}`, `J` has totally degenerate reduction, so
`J ≅ T/Λ` rigid-analytically with `T = Hom(X, G_m)`, `X = H₁(Γ\𝒯, Z)` the character
group (`Γ\𝒯` the quotient of the Bruhat–Tits tree by the units of Dembélé's definite
order localized at `q₀`; its edges are the level-`q₀` Brandt module, its vertices two
copies of the level-1 module), and `Λ ⊂ T(K)` the image of `X' = X` under the period
pairing `u : X × X → K^×`, `v_{q₀} ∘ u` = the monodromy pairing (D31: stabilizer orders on
the diagonal). `T` acts on `X`, `Λ`, `u` compatibly. Passing to the `g`-part:
`B_g = T_g/Λ_g`, `T_g = Hom(X_g, G_m)`, `X_g ⊗ Q ≅ K_g` (rank-1 over `K_g`), `Λ_g ≅ X_g`
as `O`-modules via `u`.

## 2. The localization statement (true, elementary)

For any `t ∈ B_g[2]` write `t = √l` for `l ∈ Λ_g`, i.e. `t ∈ Hom(X_g, K̄^×)` with
`t(x)² = u(l, x)`. Then

    0 → Hom(X_g/λX_g, μ₂) → B_g[λ] → Λ_g/λΛ_g → 0,

both ends 1-dimensional over `F₂₅₆` (8 over `F₂`), both with **trivial** `G_K`-action
(`μ₂ ⊂ K`, `Λ_g ⊂ T_g(K)`), and the extension class is the Kummer image of the
`λ`-block of the period pairing:

    u_λ : (X_g/2X_g)_λ × (X_g/2X_g)_λ → K^×/(K^×)²  ≅ (Z/2)² = ⟨π_{q₀}, ε⟩,

an `8 × 8` matrix over `F₂` with entries in a 2-dimensional `F₂`-space. Concretely, with
`ẽ_λ ∈ O` lifting the idempotent `e_λ ∈ O/2O = ∏_{λ'|2} F₂₅₆` (2 is unramified in `K_g`
at the primes over `f1`; D32):

    K(B_g[λ]) = K( √u(ẽ_λ l, x) : l ∈ Λ_g, x ∈ X_g ),

and `u(ẽ_λ l, x) mod (K^×)²` depends only on `l, x` modulo `2` and through the
`λ`-block, because `u` is `O`-balanced (`u(al, x) = u(l, ax)`) and `u(2Λ_g, X_g) ⊂` squares.
So: **`B_g[λ]` as a `G_K`-module, together with its points as elements of
`Hom(X_g, K̄^×)` modulo the `K`-rational part, is determined by (i) the `λ`-block of
`X ⊗ Z₂` (banked: `dp_hg_f1.m`, D32) and (ii) 64 period values modulo squares** — only
their valuations mod 2 and unit parts mod squares. That is far less than the "16 columns
of periods at ~110 core-h" the stocktake budgeted.

Consistency prediction (cheap, unperformed): `ρ̄_f` is unramified at `q₀` (level 1), so
the class must be unramified — the monodromy pairing restricted to the `f1`-new block must
have **even** valuations mod 2 on the block, and the class lives in the `ε`-component. If a
future run at some `q₀` produced odd valuations there, something upstream would be wrong.
(Also: `Frob_{q₀}` has `ā_{q₀} = 0`, `det ≡ 1`, so characteristic polynomial `(t+1)²` —
unipotent, as level raising requires.)

## 3. Why this does not reopen the route

The point of the CD uniformization was never the *Galois module* `B_g[λ]` — that module
is `ρ̄_f`, known since Dembélé 2009 — but a **construction of the global field**
`F(B_g[λ]) = K_Dembélé` from computable data. Local data at `q₀` cannot do that:

1. **The uniformization coordinates are transcendental.** `t(x) = √u(l, x) ∈ K̄` is the
   analogue of `q^{1/2}` for a Tate curve; the algebraic point `t ∈ B_g(F̄)` has algebraic
   coordinates only after applying algebraic functions on `B_g` (theta functions /
   Tate–Mumford series), just as `j(q)`, not `q`, is algebraic. So stocktake question 2
   ("`λ`-division + LLL") recognizes nothing on its own: LLL on `√u(l,x)` has no algebraic
   target.
2. **The algebraic functions live on `B_g`, not on the block.** Theta functions on
   `T_g/Λ_g` are sums over `Λ_g` (rank `d_g`), evaluated with the full `d_g × d_g` period
   matrix — the `M^{d_g}` term count of `gate5-genus16-term-count.md`. The `λ`-block is an
   `O/2`-summand of `B_g[2]`, not a sub-abelian-variety: there is no torus quotient of
   dimension 16 (or 8) whose 2-torsion is `B_g[λ]`. Such a variety would be an abelian
   variety with a degree-16 Hecke orbit carrying `ρ̄_f` — precisely what D32 excludes at
   `q₀` and the stocktake's size/structure argument makes an unstructured accident anywhere
   (`P ≲ 1%` per candidate prime).
3. **Local information at one prime never determines a global field.** The `G_{F_{q₀}}`-
   module `B_g[λ]` is unipotent with a 2-element-valued Kummer class; it is the same for
   every lift `g` at every `q₀` up to the two bits `(π, ε)`. Even the union over all
   auxiliary primes reduces to Frobenius data already known from `a_p(f) mod λ`
   (Chebotarev); it is the *shape* of `K_Dembélé`, not a polynomial.

Hence: `d_g` remains the operative parameter of any recognition that goes through `B_g`,
and hole (1) — answered positively — is not a lever. The only ways `d_g` can stop
mattering are (a) an abelian variety of dimension 16 carrying `ρ̄_f` with a computable
model (a small rational Hecke orbit at some auxiliary prime: the lottery; or the
level-1 `A_f` itself, which has good reduction everywhere, hence no multiplicative
uniformization anywhere — only the killed archimedean routes), or (b) hole (2): an
algebraic invariant of `K_Dembélé` computable *without* passing through the points of a
`d_g`-dimensional variety. No candidate for (b) is known; note it is the original
front-end problem restated.

## 4. Status of the CD arc after this note

| obstruction | measured/argued | scope |
|---|---|---|
| `d_g > 16` at `q₀` | D32 (Deligne-bound certificate) | this `q₀`; heuristically all |
| `M_rec ~ 10⁴` | D33 (level-31 Tate parameters) | any q₀-adic period recognition |
| `λ`-torsion localizes but only locally | this note | the "toric rework" (b) of D32 |

The `λ`-torsion localization was the last conceptual escape listed against `d_g`. With it
closed, the CD arc has no open door except the auxiliary-prime lottery (`~10⁻³` path
probability in the affordable window) and the untested conductor-`𝔭^k` family at the
prime above 2 (D36: Steinberg at `𝔭` is closed; supercuspidal untouched, larger and
murkier — and it too produces a `d_g` question).

## 5. What is *not* claimed

- Nothing here is a theorem about `K_Dembélé`; §2 is standard rigid-analytic Kummer
  theory for totally degenerate abelian varieties (Raynaud/Mumford uniformization,
  Grothendieck's monodromy pairing), applied to the `O`-module structure.
- The unramifiedness prediction in §2 is a *consistency check* on future runs, not a new
  invariant: it is forced by `ρ̄_f` having level 1.
- §3(2) assumes recognition proceeds through algebraic functions on some abelian variety
  or curve. A recognition scheme that bypasses varieties altogether would be new
  mathematics (hole 2), and is not excluded here — only unidentified.
