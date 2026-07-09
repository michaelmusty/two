# Summary of changes for run 1cb59aba-ac9d-4c9f-9b37-91411eaaf6ea
Completed all sorries in `FiniteLocalSolvable.lean`; the file builds cleanly with no `sorry`/`admit`/`axiom`, and the main results depend only on the standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

What was proved (in namespace `BelyiSolvable`):

**Theorem A (priority):** `isSolvable_units_of_finite_local` — for any finite local ring `E` (`[Ring E] [Finite E] [IsLocalRing E]`), the unit group `Eˣ` is solvable. The statement is kept fully general (possibly noncommutative), because the intended application (Theorem B) needs it for `Module.End A M`, which is noncommutative.

**Theorem B:** `isSolvable_moduleAut_of_localEnd` — for a finite `A`-module `M` whose endomorphism ring is local, `(Module.End A M)ˣ` is solvable (a direct application of Theorem A). Its hypothesis is supplied by the newly-proved Fitting-style lemma `isLocalRing_end_of_indecomposable`: a finite nontrivial module all of whose endomorphism idempotents are `0` or `1` has a local endomorphism ring.

Design note: the original skeleton used `IsLocalRing.ResidueField`/`IsLocalRing.residue`, which in Mathlib only exist for commutative rings, so the file could not compile as given and would only have covered the commutative case (leaving Theorem B unprovable). I reformulated the residue construction noncommutatively using the Jacobson radical `Ring.jacobson E` (a two-sided ideal) and built the residue division ring `E ⧸ Ring.jacobson E` by hand (`DivisionRing.ofIsUnitOrEqZero`); `littleWedderburn` then upgrades it to a finite field with cyclic (hence solvable) unit group.

Supporting lemmas proved along the way, following the outline in `statement.md`:
- `mem_jacobson_iff_not_isUnit`: in a finite local ring, membership in the Jacobson radical is exactly non-invertibility;
- `isUnit_one_add_of_mem_jacobson`, `isUnit_or_eq_zero_residue`, `isSolvable_units_residue`;
- `card_ker_eq_card_jacobson`: the reduction map `Eˣ → (E/J)ˣ` has kernel `1 + J` in bijection with `J`;
- `exists_prime_pow_card`: a finite local ring has prime-power order (its additive group is a `p`-group for `p` the residue characteristic);
- `isPGroup_ker`: the kernel `1 + J` is a `p`-group, hence nilpotent and solvable;
- and general utilities `isUnit_of_mul_eq_one_finite(')`, `exists_pow_isIdempotent` (a positive power of any element of a finite monoid is idempotent), `isLocalRing_of_finite_of_isIdempotentElem`, and the `Finite (Module.End A M)` instance.

Theorem A itself is assembled via `solvable_of_ker_le_range`, exhibiting `Eˣ` as an extension of the (cyclic) residue-field unit group by the (`p`-group) kernel `1 + J`.