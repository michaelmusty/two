# Lemma B for cyclic 2-groups: a proof, and a coinvariant formula in general

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

**Next steps.** (1) Tabulate `dim M_G` (= `2 + d(M(G)) − r`) across the census and
list the groups/triples with `dim M_G ≥ 2` — the quaternion family is the smallest
such and the natural first target for a gluing argument (`F_2[Q_8]` has tame
representation type, so its indecomposables are classified). (2) The proposition is
Lean-formalizable (Hopf formula + Nakayama) once `H_1(X°,F_2) = N^{ab} ⊗ F_2` is
taken as the definition of the module, matching `torsion_module.sage`.
