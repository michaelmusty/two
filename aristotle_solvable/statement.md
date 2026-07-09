# Finite local ring ⟹ solvable unit group (the algebraic engine)

This is **Lemma A** of the "2-group Belyi maps have solvable `Q(J[2])`" program: the
purely algebraic core that converts *indecomposability* of the mod-2 torsion module into
*solvability* of the arithmetic Galois image. The geometric input (that `H¹(X, F₂)` is an
indecomposable `F₂[G]`-module) stays a hypothesis; this file proves the engine that runs
on it.

Formalize in Lean 4 (with Mathlib) and prove:

**Theorem A (core).** Let `E` be a finite local ring. Then its group of units `Eˣ` is
solvable.

Proof outline (all steps standard):
1. A finite local ring has residue field `E/J` (`J` = maximal ideal = Jacobson radical),
   which is a finite **division ring**, hence a finite **field** by Wedderburn's little
   theorem. Its unit group `(E/J)ˣ` is cyclic, hence solvable.
2. `J` is nilpotent (finite ⟹ Artinian), and the map `x ↦ 1 + x` is a bijection
   `J → (1 + J)` onto a subgroup of `Eˣ`; so `|1 + J| = |J|`. A finite local ring has
   prime-power order, so `1 + J` is a `p`-group, hence nilpotent, hence solvable.
3. The reduction map `Eˣ → (E/J)ˣ` is a surjective group homomorphism with kernel exactly
   `1 + J`. Thus `Eˣ` is an extension of the solvable group `(E/J)ˣ` by the solvable group
   `1 + J`, hence solvable.

**Theorem B (application to modules).** Let `A` be a ring and `M` a finite `A`-module
(finite as a set) whose endomorphism ring `Module.End A M` is a **local** ring (this holds,
by Fitting's lemma, whenever `M` is indecomposable of finite length). Then the automorphism
group `(Module.End A M)ˣ` — equivalently the group `M ≃ₗ[A] M` of `A`-linear
automorphisms — is solvable.

(Context: for a 2-group Belyi map, `J[2] = H¹(X, F₂)` is a finite `F₂[G]`-module, and the
arithmetic Frobenius acts `F₂[G]`-linearly, so the Galois image lands in
`Aut_{F₂[G]}(J[2]) = (Module.End (MonoidAlgebra (ZMod 2) G) J[2])ˣ`. Empirically `J[2]` is
indecomposable, so Theorem B forces this centralizer — hence the Galois image, hence
`Gal(Q(J[2])/Q)` — to be solvable. This is why no 2-group Belyi map yields a nonsolvable
number field ramified only at 2.)
