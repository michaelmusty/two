# Lemma B for cyclic 2-groups: a proof, and a coinvariant formula in general

**Correction (2026-09-03, §4 below): Lemma B as stated ("`J[2]` indecomposable") is
FALSE — it fails for the generalized quaternion groups `Q_{2^m}`, `m ≥ 4`, where
`J[2] = A ⊕ B` with `A ≇ B`. The property the census scans actually verified, and the one
the arithmetic conclusion needs, is *multiplicity-freeness* (no two isomorphic summands);
see §4 for the corrected statement and the census tables.** The cyclic theorem below is
unaffected (it proves the stronger cyclic-module statement).

**Status (2026-09-01):** Lemma B (`writeup/lemma-B-open-problem.md`) is **proved for
every cyclic 2-group** `G = C_{2^k}` — step (a) of the attack plan. The proof is a
half-page coinvariant computation via Hopf's formula; it yields, for *every*
2-generated 2-group, an exact formula for `dim H_1(X,F_2)_G` in terms of the Schur
multiplier and three explicit lattice vectors, which explains why the socle/top
criterion fails beyond the cyclic case. Numerical confirmation:
`lemmaB/cyclic_check.sage` (930 positive-genus cyclic triples, `n ≤ 32`, all
`dim M_G = dim M^G = 1`) and `lemmaB/coinv_formula_check.sage` (all 2-generated groups of order `≤ 32`, output in
`lemmaB/coinv_formula_check.out`: the bounds `d(M(G)) − 1 ≤ dim M_G ≤ 2 + d(M(G))` and
`dim M_G = dim M^G` hold in every case; `Q_8 = [8,4]` and `Q_16 = [16,9]` give `dim M_G = 2`
exactly as §3 predicts; `dim M_G = 3` occurs at `[32,5]` and `[32,8]`).

Notation as in `lemma-B-open-problem.md` §1–2: `F = ⟨x,y⟩` free, `π: F ↠ G` with
kernel `N`, `σ_0 = π(x)`, `σ_1 = π(y)`, `σ_∞ = π((xy)^{-1})`, `e_b = ord σ_b`; `X → P¹`
the Galois Belyi cover, `X° = X ∖ φ^{-1}{0,1,∞}`. We work with homology
`M = H_1(X, F_2)`; `H¹(X,F_2) = M^*` and a module is indecomposable iff its dual is,
so nothing is lost.

## 1. Two general facts

**(F1) Cyclic ⟹ indecomposable, for any 2-group.** `F_2[G]` is a local ring with
radical the augmentation ideal `I` and residue field `F_2`. If `dim_{F_2} M/IM = 1`
(i.e. `dim M_G = 1`) then `M` is cyclic (Nakayama) and indecomposable: `M = A ⊕ B`
with `A, B ≠ 0` would give `M/IM = A/IA ⊕ B/IB` with both summands nonzero by
Nakayama. (This uses only locality, not the uniserial structure of `F_2[C_{2^k}]`.)

**(F2) Coinvariants of the relation module.** `H_1(X°, F_2) = N^{ab} ⊗ F_2` with `G`
acting through conjugation by `F`, so `(g−1)` acts by `n ↦ [f, n]`, and

    H_1(X°,F_2)_G = N / ([F,N]·N²) = (N/[F,N]) ⊗ F_2.

Hopf's formula gives the exact sequence

    0 → H_2(G,Z) → N/[F,N] → F^{ab} = Z² → G^{ab} → 0,

so `N/[F,N]` is an extension of the rank-2 lattice
`L := ker(Z² → G^{ab}) = {(u,v) : σ_0^u σ_1^v ∈ [G,G]}` by the Schur multiplier
`M(G) = H_2(G,Z)`. Since `L` is free, `− ⊗ F_2` stays exact on the left:

    0 → M(G)/2M(G) → H_1(X°,F_2)_G → L/2L → 0,       dim H_1(X°,F_2)_G = 2 + d(M(G)),

where `d(M(G))` is the 2-rank of `M(G)`. (Cross-check: the five-term sequence gives
`dim = dim H_2(G,F_2) + 2 − d(G) = (d(M(G)) + d(G)) + 2 − d(G)`.)

**Punctures.** `H_1(X,F_2) = H_1(X°,F_2)/P` where `P` is spanned by the classes of
the loops around the punctures. The puncture over `b` corresponding to the coset
`g⟨σ_b⟩` has loop `f·w_b^{e_b}·f^{-1} ∈ N` with `w_0 = x`, `w_1 = y`, `w_∞ = (xy)^{-1}`
and `π(f) = g`. All `G`-conjugates of a puncture loop have the same image in the
coinvariants, so `im(P_G → H_1(X°,F_2)_G)` is spanned by the **three** classes
`[x^{e_0}]`, `[y^{e_1}]`, `[(xy)^{-e_∞}]`, whose images in `L/2L` are

    p_0 = (e_0, 0),   p_1 = (0, e_1),   p_∞ = (e_∞, e_∞)   (mod 2L).

Coinvariants are right exact, hence:

> **Proposition (coinvariant formula).** For every 2-generated 2-group Belyi map,
>
>     dim H_1(X,F_2)_G = 2 + d(M(G)) − r,      r = rank_{F_2} ⟨[x^{e_0}], [y^{e_1}], [(xy)^{-e_∞}]⟩ ⊆ (N/[F,N]) ⊗ F_2,
>
> and `r ≤ 3`. In particular `dim H_1(X,F_2)_G ≥ d(M(G)) − 1`, so the cyclic/socle
> criterion (F1) can only apply when `d(M(G)) ≤ 2`.

By self-duality of `H_1(X,F_2)` (Weil pairing) the same number is `dim H_1(X,F_2)^G`;
this is the quantity that reaches 3 in the census (`[32,5]`, genus 9), which the
proposition now explains structurally rather than as an accident.

## 2. The cyclic case

> **Theorem.** Let `G = C_n`, `n = 2^k`, and let `X → P¹` be any Galois Belyi map with
> deck group `G` and `g(X) ≥ 1`. Then `H_1(X,F_2)` (equivalently `H¹(X,F_2) = J[2]`) is
> a cyclic `F_2[G]`-module; in particular it is indecomposable, i.e. Lemma B holds.

*Proof.* Write `σ_0 = σ^a`, `σ_1 = σ^b` for a generator `σ`; 2-generation means
`gcd(a,b,n) = 1`, so (swapping the roles of `0` and `1` if necessary) `a` is odd, hence
`e_0 = n`. For cyclic `G`, `M(G) = 0` and `G^{ab} = G`, so by (F2)

    H_1(X°,F_2)_G = L/2L ≅ F_2²,    L = {(u,v) : au + bv ≡ 0 (mod n)}.

The puncture class `p_0 = (n, 0)` lies in `2L` iff `(n/2, 0) ∈ L` iff `a·n/2 ≡ 0
(mod n)` iff `a` is even. So `p_0 ≠ 0` in `L/2L`, i.e. `r ≥ 1`, and the proposition
gives `dim H_1(X,F_2)_G ≤ 1`. Since `g ≥ 1`, `H_1(X,F_2) ≠ 0`, and a nonzero module
over the local ring `F_2[G]` has nonzero coinvariants; hence `dim H_1(X,F_2)_G = 1`,
and (F1) finishes. ∎

*Remarks.* (i) Over `F_2[C_{2^k}] = F_2[t]/(t^{2^k})` a cyclic module is uniserial,
so the theorem says `J[2] ≅ F_2[t]/(t^{2g})` exactly — the 2-torsion of the
superelliptic curve `y^{2^k} = x^a(x−1)^b` is a single Jordan block for `σ`.
(ii) The proof never uses the explicit equation; the input is only Hopf's formula
and the vanishing of the Schur multiplier. (iii) For the non-Galois covers with
cyclic Galois closure this feeds directly into the subquotient argument of
`main-result.md`.

## 3. What the formula says about the general case

(F1) applies iff `r = 1 + d(M(G))`. The `L/2L`-component of `p_b` is computable in the
group: `p_b ∈ 2L` iff `(e_b/2)·w_b ∈ L` iff `σ_b^{e_b/2} ∈ [G,G]`, i.e. iff the
involution in `⟨σ_b⟩` lies in the derived subgroup. Consequences:

- **Generalized quaternion `Q_{2^m}`**: `M(G) = 0`, and the unique involution is
  central and lies in `[G,G] = ⟨σ²⟩`, so all three `p_b` vanish, `r = 0`, and
  `dim M_G = 2` for *every* quaternion triple (cf. the `Q_8` demo: `dim J[2] = 4`,
  `dim End = 6`). So already at `d(M(G)) = 0` the socle/top criterion fails and
  indecomposability is a genuine gluing phenomenon.
- **Semidihedral `SD_{2^m}`** (`M(G) = 0`): `p_b ≠ 0` iff `σ_b` is a non-central
  involution; triples with all `σ_b` of order `≥ 4` again have `r = 0`.
- `d(M(G)) ≥ 1` (dihedral, `C_{2^a} × C_2`, ...): the `M(G)/2`-component of the
  puncture classes (their lift to `N/[F,N]` beyond `L`) enters and is not visible
  in `G^{ab}` alone.

So the cyclic case is special because `M(G) = 0` *and* the derived subgroup is
trivial. Beyond it, the proposition is a bookkeeping tool, not a proof: it computes
`dim M_G = dim M^G` exactly and separates the census into cases explained by (F1)
(`dim M_G = 1`) and cases where indecomposability is carried by the gluing of a
multi-dimensional top (`dim M_G ≥ 2`), which is where the attack plan's §4(b)–(c)
must operate.

**Next steps (as of 09-01; see §4 for what happened).** (1) Tabulate `dim M_G`
(= `2 + d(M(G)) − r`) across the census and list the groups/triples with `dim M_G ≥ 2`.
(2) The proposition is Lean-formalizable (Hopf formula + Nakayama) once
`H_1(X°,F_2) = N^{ab} ⊗ F_2` is taken as the definition of the module, matching
`torsion_module.sage`.

## 4. The census tabulation (2026-09-03): Lemma B is false as stated; the corrected statement

Script: `lemmaB/census_top.sage`; outputs `lemmaB/census_top_{4_8_16_32,64}.{csv,out}`.
For every Aut(`G`)-class of generating pairs (`GQuotients`) of every 2-generated 2-group of
order `≤ 64` with positive genus — **707 triples** — it computes, from the module itself:
`dim H_1(X°,F_2)_G`, `r` (rank of the three puncture classes in those coinvariants), the
`L/2L`-part `r_L`, `dim M_G`, the MeatAxe indecomposable decomposition, and the Wedderburn
blocks of `End(M)/rad`. Plus a subgroup-determinacy test (below).

### 4.1 Consistency checks (all pass, 707/707)

- `dim H_1(X°,F_2)_G = 2 + d(M(G))` (Hopf), `dim M_G = 2 + d(M(G)) − r`, `r_L ≤ r`.
- `r_L = r` in 568 cases; `r_L < r` in 139 — the Schur-multiplier component of the puncture
  classes is genuinely present (it is invisible in `G^{ab}`).

**Cohomological form of `r`.** `V := N/([F,N]N²) = H_1(X°,F_2)_G` is the kernel of the
universal 2-generated central `F_2`-extension `F/[F,N]N² → G`, and `H²(G,F_2) = V^*`
(dimension `2 + d(M(G))` on both sides). A class `λ ∈ V^*` restricts nontrivially to the
cyclic subgroup `⟨σ_b⟩` iff the lift of `σ_b` has order `2e_b` iff `λ([w_b^{e_b}]) ≠ 0`.
Hence

    r = rank( res : H²(G,F_2) → ⊕_b H²(⟨σ_b⟩,F_2) ),     dim M_G = dim ker(res).

(Equivalently, via the Cartan–Leray sequence of `X → X/G` as an orbifold, `M^G ≅ ker
(H²(G,F_2) → H²(Δ,F_2))`, `Δ` the triangle group; the two descriptions agree because a
class inflates to zero on `Δ` iff it dies on the three cyclic subgroups.) For `Q_{2^m}`,
`H²` is spanned by products of degree-1 classes, whose restrictions to cyclic subgroups of
order `≥ 4` vanish (`u² = 0` in `H^*(C_{2^k},F_2)`, `k ≥ 2`): so `r = 0`, `dim M_G = 2`.

### 4.2 `r` versus `d(M(G))` (counts of triples, `|G| ≤ 64`)

| `d(M(G))` | `r=0` | `r=1` | `r=2` | `r=3` | `dim M_G` values |
|---|---|---|---|---|---|
| 0 | 73 | 222 | — | — | 1, 2 |
| 1 | 51 | 144 | 83 | — | 1, 2, 3 |
| 2 | 4 | 30 | 48 | 42 | 1, 2, 3, 4 |
| 3 | — | — | 3 | 7 | 2, 3 |

`dim M_G = 4` first occurs at `[64,19]` and `[64,22]` (`r = 0`). The cyclic criterion (F1)
covers exactly the `dim M_G = 1` column; everything else is glued.

### 4.3 The decomposition: `Q_{2^m}` (`m ≥ 4`) is a counterexample to Lemma B as stated

| group | `M` | `End(M)/rad` |
|---|---|---|
| `Q_8 = [8,4]` (`g = 2`) | indecomposable | **`F_4`** (not absolutely indecomposable) |
| `Q_16 = [16,9]` (`g = 4`) | **`A ⊕ B`, `A ≇ B`, `dim 4 + 4`** | `F_2 × F_2` |
| `Q_32 = [32,20]` (`g = 8`) | **`A ⊕ B`, `A ≇ B`, `dim 8 + 8`** | `F_2 × F_2` |
| `Q_64 = [64,54]` (`g = 16`) | **`A ⊕ B`, `A ≇ B`, `dim 16 + 16`** | `F_2 × F_2` |
| every other group, `\|G\| ≤ 64` (703 triples) | indecomposable | `F_2` |

Confirmed three ways: MeatAxe `MTX.Indecomposition`; the commutant/Wedderburn computation
of `torsion_module.centralizer_solvable` (`End/rad = F_2 × F_2`); and an explicit model.
The model: for `Q_{2^m}` the unique triple type is `(4, 4, 2^{m-1})`, the central involution
`z` fixes every ramification point, Riemann–Hurwitz gives `g(X/z) = 0`, so `X` is the
hyperelliptic curve `y² = x(x^{2g}−1)`, `g = 2^{m-2}`, with `G/z = D_{2g}` acting on the
`2g+2` Weierstrass points in orbits of sizes `g, g, 2` (fibres over `0, 1, ∞`), and
`J[2] = (even subsets)/⟨all⟩`. Decomposing that permutation-module quotient
(`lemmaB/quaternion_hyperelliptic.sage`; the Belyi-model check is
`lemmaB/quaternion_check.sage`) gives the same `A ⊕ B`, with
`soc A = ⟨[fibre over 0]⟩`, `soc B = ⟨[fibre over 1]⟩`. Each summand has 1-dimensional socle
and top, identical fixed-point dimensions under `σ_0, σ_1, σ_∞`, and restricts to
`⟨σ_∞⟩` as a single Jordan block of size `g`. The summands are **not** the permutation
modules `F_2[G/⟨σ_b⟩]`, and for `g = 8` neither is generated by an even subset of size
`≤ 4`; a closed-form description is open.

**Why the earlier claim was wrong.** `torsion_fast/shard.sage` computed
`max_multiplicity` = the largest multiplicity of an indecomposable summand, and
`max_multiplicity == 1` was reported as "indecomposable". It means **multiplicity-free**.
The 2008/2008 tally for `|G| ≤ 128` is therefore a tally of multiplicity-freeness — which
is exactly what the arithmetic argument uses, since `End(M)/rad` is then a product of finite
fields and `Aut(M)` is solvable (Lemma A's proof verbatim, with "finite field" replaced by
"product of finite fields"; the Lean file covers the local case only — the product case is a
one-line extension not yet formalized).

### 4.4 Corrected statements

> **Lemma B′ (conjecture; what the scans verified for `|G| ≤ 128`).** `H_1(X,F_2)` is
> multiplicity-free: no indecomposable `F_2[G]`-summand occurs twice. Equivalently
> `End_{F_2[G]}(H_1(X,F_2))/rad` is commutative.

> **Lemma B″ (refined conjecture; verified for `|G| ≤ 64`).** `H_1(X,F_2)` is
> indecomposable unless `G ≅ Q_{2^m}`, `m ≥ 4`, in which case it is `A ⊕ B` with `A ≇ B`
> and `dim A = dim B = g`. `End/rad = F_2` for every indecomposable summand except when
> `G = Q_8` (`F_4`).

Lemma A + B′ give the conditional theorem of `main-result.md` unchanged.

### 4.5 Subgroup-determinacy (new observation)

Binning triples of a fixed `G` by the multiset of conjugacy classes of the three cyclic
subgroups `⟨σ_b⟩`: in 151 of 155 bins with `≥ 2` Aut-classes the modules are isomorphic;
the 4 failures are `[64,4]`, `[64,15]`, `[64,35]`, `[64,36]` (3 Aut-classes each). So `M`
is *nearly*, but not exactly, determined by the three subgroups — consistent with the
stable-category description `M ≅ cone(⊕_b F_2[G/⟨σ_b⟩]/F_2 → Ω²F_2)`, where the three
stable maps are canonical (each lies in `Ĥ^{-2}(⟨σ_b⟩,F_2) = F_2`) but the lift through
the quotient by `F_2` carries an `Ĥ³(G,F_2)`-ambiguity.

### 4.6 Where this leaves Lemma B′

Open. The quaternion family shows the mechanism is not "one indecomposable" but "pairwise
non-isomorphic summands". A proof must explain why two summands can never be isomorphic,
e.g. via the socle: `soc M = M^G`, and the summands' socles are spanned by the fibre classes
`[φ^{-1}(b)]` — in the quaternion case the two summands are told apart by *which* fibre
spans their socle. Whether that persists (summand socles ↔ distinct fibre classes) is the
natural next experiment; it is a statement about the `G`-module, cheap to test on the
census, and would turn B′ into a statement about the three fibre classes in `M^G`.
