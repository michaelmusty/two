# Level raising at the prime above 2, conductor `𝔭^k` (k ≥ 2): the supercuspidal family

> **Scope correction, 2026-09-14 (D42):** the closure below applies to the
> existing Mumford/toric-period pipeline, not to all constructions using this
> carrier. `review-2026-09-14.md` develops a curve-first Jacobian route at an
> odd good prime, with a conditional genus-64 quotient. Finite T31/T97 matches
> alone are not a full residual-identity proof; script 63 investigates an
> all-Hecke sign-type comparison. The historical calculations below are retained.

**Date:** 2026-09-08. **Decision:** D39. **Script:** `dembele/magma/58_levelraise_p2k.m`.
**Output:** `dembele/data/computed/levelraise_p2k.out`. **Predecessor:** D36
(`57_levelraise_p2.m`, conductor `𝔭¹`, Steinberg: closed).

## 0. Verdict

The door is *open* as a congruence and *closed* as a route.

- **Level raising holds at `𝔭²`.** Dembélé's residual system occurs in the `𝔭²`-new part
  of the level-`𝔭²` Brandt module with multiplicity exactly **1** per residual system
  (`f1`, `f2`), on top of the old baseline **3** (three degeneracy copies of the level-1
  form). Verified at `T_31` on the whole raw module (basis-free characteristic-polynomial
  count; §2), confirmed at `T_97` on the saturated new lattice (§4).
- **`d_g = 48`.** The `𝔭²`-new characteristic polynomial of `T_31` is *irreducible of
  degree 48* over `Q`: the entire new space is one rational Hecke orbit. The abelian
  variety `A_g/F` carrying the congruence is 48-dimensional (not 16).
- **No toric structure.** The `𝔭²`-new forms are depth-zero supercuspidal at `𝔭`
  (`U_𝔭 = 0` on the new part, char 0). Hence `ρ_g|G_𝔭` is irreducible of tame inertial
  type, `A_g` has **potentially good (supersingular) reduction** at `𝔭`, and the Shimura
  curve carrying it is uniformized by a quotient of Drinfeld's first covering `Σ¹`, not
  by `Ω`. Nothing from the Cerednik–Drinfeld period arc (D28–D34, D38) applies, and D38's
  locality objection applies verbatim. **This is not a path to the field** (§3).

## 1. Setup and method

`F = Q(ζ₃₂)⁺`, `𝔭 | 2` the unique prime above 2 (`N𝔭 = 2`, `e = 8`), definite
discriminant-1 quaternion algebra, parallel weight 2, trivial character, levels `𝔭^k`.
Cuspidal dimensions (Magma): `57, 154, 299, 580, 1142, 2249` for `k = 0..5`; hence
`𝔭^k`-new dimensions `57, 40, 48, 136, 281, 545`.

Everything is done on the raw Brandt module (cuspidal + one Eisenstein line) with the
sparse Hecke intrinsic (`InternalHMFRawHeckeDefiniteSparse`, `dembele/patches/`). With
`cp_k = charpoly(T_31)` at level `𝔭^k` and `cp_new(0) = cp_0` (raw level 1, Eisenstein
factor `t − 32` once),

    cp_new(k) = cp_k / gcd(cp_k, ∏_{j<k} cp_new(j)^{k−j+1}),

and the degree of `cp_new(k)` is checked against the new dimension above (the gcd absorbs
the Eisenstein factor exactly once). The residual multiplicity of `f_i` (the two degree-8
factors of the level-1 invariant `g16bar(31)`) in `cp_new(k) mod 2` is the answer; the
total multiplicity in `cp_k mod 2` minus the old baseline `Σ_{j<k} (k−j+1)·m_new(j)` is
printed as a cross-check. This is a characteristic-polynomial statement in characteristic
zero, so it needs neither Ihara's lemma nor any basis compatibility (the D26b trap).

Why this is the right object for `k ≥ 2`: the diamond operators at `𝔭^k` form a 2-group
(`(O/𝔭^k)^× ≅ (1+𝔭)/(1+𝔭^k)`, order `2^{k−1}`), so every mod-2 Hecke eigensystem at
`Γ₁(𝔭^k)` already occurs on the `Γ₀(𝔭^k)` (trivial-character) space — nothing is lost
by working with trivial character.

## 2. Results

| k | cusp dim | new dim | `cp_new` factor degrees over `Q` | `cp_new mod 2` | new mult `[f1,f2]` | old baseline |
|---|---|---|---|---|---|---|
| 1 | 154 | 40 | 4,4,4,4,24 | `(t⁴+t+1)⁵(t⁴+t³+t²+t+1)⁵` | **[0,0]** (D36) | [2,2] |
| 2 | 299 | 48 | **48** | `t³² · f1 · f2` | **[1,1]** | [3,3] |
| 3 | 580 | 136 | **64, 72** | (output) | **[2,2]** (one per orbit) | [6,6] |
| 4 | 1142 | 281 | 1, 1⁴, 2², 4, 4, 4, 4, **16**, 24, 32, **48**, **64**, **72** | `t¹³⁷ (t⁴+t+1)¹⁰ (t⁴+t³+t²+t+1)¹⁰ f1⁴ f2⁴` | **[4,4]** (one per bold orbit) | [12,12] |

Level-1 recomputation matches the D36 reference invariant exactly (`g16bar(31)`,
`f1 = t⁸+t⁴+t³+t+1`, `f2 = t⁸+t⁶+t⁵+t²+1`, each of multiplicity 1 in `cp_0 mod 2`).

`k = 2` details (all from the output file):
- `U_𝔭` on the char-0 new subspace `W_new` (dim 48): charpoly `t⁴⁸` — nilpotent, as
  forced for conductor `𝔭²` with trivial central character (`a_𝔭(g) = 0`).
- `U_𝔭` on the generalised `f_i`-eigenspace mod 2 (dim 32 = 4 × 8): charpoly
  `t²⁴ (t²+t+1)⁴`. Reading: of the three old copies, one has `U_𝔭 = ā_𝔭 = ω` and two have
  `U_𝔭 = 0` (the `K₀(𝔭²)`-fixed vectors of an unramified principal series carry
  `U_𝔭`-charpoly `X(X² − a_𝔭X + N𝔭) ≡ X²(X+ω)` mod 2), and the new copy has `U_𝔭 = 0`.
  Consistent.
- The 48-dimensional Hecke field `H_g` has (at least) two primes above 2 of residue
  degree 8 with `a_31` reducing to `f1`, `f2`, and `a_31 ≡ 0` modulo every other prime
  above 2 (the `t³²`).

`k = 3`: the 136-dimensional new part is two rational orbits (degrees 64 and 72), each
carrying one copy of each residual system; `U_𝔭` nilpotent on `W_new`. These are the
conductor-`𝔭³` (depth-`1/2`, ramified-dihedral) supercuspidals.

`k = 4`: the four new copies per residual system sit on orbits of degrees **16, 48, 64,
72** — the degrees of Dembélé's form and of the `𝔭²`- and `𝔭³`-new carriers. Explanation:
the quadratic character `χ` of `Q(ζ₃₂)/F` has conductor exactly `𝔭²` (relative
discriminant `𝔭²`, norm 4), so `f ⊗ χ` and the twists of the depth-0 and depth-1/2
supercuspidals all have conductor `𝔭⁴` (`a(π ⊗ χ) = 2a(χ) = 4` when `χ` is deeper than
`π`), while `ρ̄_{g⊗χ} = ρ̄_g` since `χ ≡ 1 mod 2`. Accounting: `1 + 1 + 2 = 4` ✓, and the
twists of the 40 Steinberg forms (`4,4,4,4,24`) are visible too. `χ(𝔭₃₁) = −1` (31 is
inert in `Q(ζ₃₂)/F`), so twisted factors are `h(−t)`. **Verified** by
`59_p2k_twist_check.m` (`dembele/data/computed/p2k_twist_check.out`, charpolys banked in
`levelraise_p2k_charpolys.m`): *every* irreducible factor of the `𝔭⁴`-new charpoly is
`h(−t)` for a factor `h` of a lower new charpoly — `57` (all level-1 cusp forms; the
Eisenstein line `t − 32` correctly does not reappear, since `χ∘Nrd` is not
level-`𝔭⁴`-invariant) `+ 40 + 48 + 136 = 281`, twist-minimal remainder **0**; and nothing
at `𝔭²` or `𝔭³` is a twist of a lower level. The level-1 repeated factors `(t+4)⁴`,
`(t²−8t+8)²` explain the `1⁴`, `2²` multiplicities. **So the family's twist-minimal
carriers of `ρ̄_f` are exactly the orbits of degree 48 (`𝔭²`) and 64, 72 (`𝔭³`); at
`𝔭⁴` there are no twist-minimal newforms at all, and the degree-16 orbit is `A_f`
itself, twisted by `Q(ζ₃₂)/F`** (same `λ`-torsion field, nothing new).

Timings (local Magma 2.29-8, sparse `T_31` builds): level 1 1085 s; `𝔭` 310 s; `𝔭²` 333 s;
`𝔭³` 339 s; `𝔭⁴` 328 s — essentially flat in the level; `U_𝔭` 15 s per level. The
archived `p2k_twist_check.out` is the replay (`BANK_IN=1`) of the accounting from the
banked charpolys; the build run that produced the bank had the same T_31 timings.

## 3. What the congruence means geometrically, and why it is not a route

**Local type.** A newform of conductor exactly `𝔭²` with trivial central character is
depth-zero supercuspidal at `𝔭`: `π_𝔭 = c-Ind` of the inflation of the cuspidal
representation of `GL₂(F₂) ≅ S₃` (the sign character, attached to the order-3 characters
of `F₄^×`). Its Weil–Deligne type is `Ind_{E/F_𝔭} χ` with `E` the unramified quadratic
extension and `χ` tame of order 3 on `F₄^×`. Consequences for `A_g` (the 48-dimensional
abelian variety over `F` attached to the orbit):
- `ρ_g|G_𝔭` is irreducible, of tame inertial type; `A_g` acquires good reduction over the
  tamely ramified cubic extension `F_𝔭(ϖ^{1/3})`. No toric part at `𝔭`.
- The Frobenius eigenvalues on the crystalline module over that extension are `±√(2u)`,
  both of slope `1/2`: the reduction is **supersingular**, isogenous to `E₀⁴⁸` with
  `E₀ : y² + y = x³` the `j = 0` curve over `F₂`.

**Which Shimura curve.** By Jacquet–Langlands, `g` transfers to the quaternion algebra
`B'` ramified at `𝔭` and seven real places, where `π_𝔭` becomes the 2-dimensional
representation of `D_𝔭^×` trivial on `1 + 𝔭_D` (restriction to `O_D^×/(1+𝔭_D) = F₄^×`:
`χ ⊕ χ²`). So `A_g` (twice) sits in the Jacobian of the Shimura curve `X` of level
`1 + 𝔭_D` at `𝔭`, a cyclic cover of degree `|F₄^×/F₂^×| = 3` of the level-1 discriminant-`𝔭`
curve `X_𝔭` of genus 40 (the 40 Steinberg forms of D36). Genus count:
`g(X) = 40·1 + 48·2 = 136`; Riemann–Hurwitz then requires 18 points of ramification index
3 (elliptic points of order 3 on `X_𝔭`), which is the expected shape.

**Uniformization.** Drinfeld's theorem uniformizes `X` by `Γ \ Σ¹`, where `Σ¹ → Ω` is the
first Drinfeld covering (Galois group `F₄^×`) and `Γ` is the same definite level-1 group
as in the CD arc. The reduction of `Σ¹` has components that are Deligne–Lusztig curves
`x y (x + y) = 1` of genus `q(q−1)/2 = 1` (for `q = 2`), sitting over the vertices of the
tree, with the covering totally ramified over the three `F₂`-points where edges attach.
So the dual graph is unchanged (toric rank of `Jac X` = toric rank of `Jac X_𝔭`, all of it
`F₄^×`-invariant, i.e. old), and the `χ`-part — where `A_g` lives — has purely abelian
reduction `E₀^{96}` (up to isogeny), matching the local-type analysis above. `X` is not a
Mumford curve; there is no period lattice, no monodromy pairing, no Schottky
parametrisation for `A_g`. Teitelbaum-style CD period computations do not exist here.

**Why it is not a route.**
1. *No period machinery.* The whole CD arc (gates 3–5, Δ′, the Tate pilot, D38) rests
   on the toric uniformization. Supercuspidal at `𝔭` is precisely the case in which it is
   absent. The archimedean alternative is the period matrix of a genus-136 Shimura curve
   over a degree-8 field, or of a 48-dimensional abelian variety — none of the killed
   routes (`idea-exhaustion.md`) becomes cheaper at dimension 48.
2. *Locality (D38).* Even a full description of `A_g[λ₁^∞]` over `O_{F_𝔭}` (a point in an
   8-dimensional Lubin–Tate-type deformation space of `E₀[2^∞] ⊗ O_{H,λ₁}`) is local
   data at `𝔭`; the global field `F(A_g[λ₁]) = K_Dembélé` is reached only through
   algebraic functions on the 48-dimensional `A_g`. The "shape of `K`" from local data
   is already known from `a_p mod λ`.
3. *`d_g = 48 > 16`.* Even if a toric structure existed, the gate-4 term count
   `M^{d_g}/Δ′` (D27c, D32) is worse here than at `q₀`.

**What it does give.** The first *explicit* geometric carrier of `ρ̄_f` at the prime
above 2 with a clean local description: a 48-dimensional factor of a genus-136 Shimura
curve, supersingular `j = 0` reduction over a tame cubic extension of `F_𝔭`. This is a
structural fact about `K_Dembélé` (its local shape at 2 is "supersingular after tame
cubic base change, in a `2`-divisible `O_{H,λ₁}`-module of `O`-height 2"), not a handle.

## 4. Confirmation at a second prime

Done (end of `levelraise_p2k.out`, `T_97` at level `𝔭²` built in 9107 s, level 1 in 3581 s).
- The level-1 residual invariant at 97 (`g16bar(97)`) matches D36's; its two degree-8
  factors are the residual systems at 97.
- Multiplicity of each residual(97) factor in `cp(T_97)` at level `𝔭²`: **4 = 3 old + 1
  new**, the same count as at 31.
- On the saturated integral new lattice `W_new` (rank 48) reduced mod 2, the generalised
  `f1(31)`-eigenspace has dimension 8 and coincides with the generalised eigenspace of one
  residual(97) factor (joint dimension 8, the other 0); `f2(31)` pairs with the other
  factor the same way. So the `𝔭²`-new copy carries *one* eigensystem matching `ρ̄_f`
  (resp. its conjugate) at both 31 and 97, not two accidental coincidences.

## 5. Honest limits

- Multiplicity counts are `T_31`-characteristic-polynomial counts on the raw module; the
  identification of the new copy with `ρ̄_f` rests on the residual invariant at 31 (and
  97 once §4 lands), the project's standard (`gate3-closure.md` §limits): Galois-conjugate
  systems give the same field, and no Sturm bound is invoked.
- §3's geometric statements are standard local theory (depth-zero types, Jacquet–Langlands,
  Drinfeld's uniformization, Teitelbaum's reduction of `Σ¹`) applied to this case; the
  genus-136 count and the 18 elliptic points are derived, not computed. Nothing in §3 is
  needed for the verdict of §0 beyond "supercuspidal ⇒ no toric part".
- The prediction that the door opens at `k = 2` with multiplicity 1 is what a
  Breuil–Mézard-type count gives (residue field `F₂` has only two Serre weights and
  `ρ̄_f` carries both; the depth-zero type reduces to the trivial weight, as does the
  level-1 type, so the multiplicities agree). None of that is a theorem at `p = 2`,
  `e = 8`; the computation is the evidence.
