import Mathlib

set_option maxHeartbeats 4000000

/-!
# Finite local ring ⟹ solvable unit group

**Theorem A (core):** the unit group of a finite local ring is solvable.
**Theorem B (application):** the automorphism group of a finite module with local
endomorphism ring (e.g. a finite indecomposable module, by Fitting's lemma) is solvable.

This is the algebraic engine behind "2-group Belyi maps have solvable `Q(J[2])`":
`J[2] = H¹(X, F₂)` indecomposable ⟹ `End` local ⟹ `Aut_{F₂[G]}(J[2])` solvable ⟹ the
arithmetic Galois image (which lands in that centralizer) is solvable.

We work with a *possibly noncommutative* finite local ring `E`, since the intended
application uses `E = Module.End A M`, which is noncommutative in general. We therefore use
the Jacobson radical `Ring.jacobson E` (a two-sided ideal) in place of the commutative
`IsLocalRing.maximalIdeal`, and construct the residue *division* ring `E ⧸ Ring.jacobson E`
by hand (it becomes a field by Wedderburn's little theorem).
-/

namespace BelyiSolvable

variable (E : Type*) [Ring E] [Finite E] [IsLocalRing E]

/-! ### The residue division ring `E ⧸ J` -/

/-- In a finite ring, a left inverse gives a unit. -/
theorem isUnit_of_mul_eq_one_finite {R : Type*} [Ring R] [Finite R] (a b : R)
    (h : a * b = 1) : IsUnit a :=
  IsUnit.of_mul_eq_one b h

/-- In a finite ring, a right inverse gives a unit. -/
theorem isUnit_of_mul_eq_one_finite' {R : Type*} [Ring R] [Finite R] (a b : R)
    (h : a * b = 1) : IsUnit b :=
  IsUnit.of_mul_eq_one_right a h

/-- The Jacobson radical of a finite local ring is proper. -/
theorem jacobson_ne_top : Ring.jacobson E ≠ (⊤ : Ideal E) := by
  have h := IsArtinianRing.isNilpotent_jacobson_bot (R := E)
  rw [Ideal.jacobson_bot] at h
  intro htop
  rw [htop] at h
  obtain ⟨n, hn⟩ := h
  rw [Ideal.top_pow] at hn
  exact bot_lt_top.ne' hn

/-- **Key characterization.** In a finite local ring, an element lies in the Jacobson
radical iff it is *not* a unit. -/
theorem mem_jacobson_iff_not_isUnit (x : E) :
    x ∈ Ring.jacobson E ↔ ¬ IsUnit x := by
  rw [← Ideal.jacobson_bot]
  constructor
  · intro hx hu
    have : (Ideal.jacobson (⊥ : Ideal E)) = ⊤ := Ideal.eq_top_of_isUnit_mem _ hx hu
    rw [Ideal.jacobson_bot] at this
    exact jacobson_ne_top E this
  · intro hx
    rw [Ideal.mem_jacobson_iff]
    intro y
    have hyx : ¬ IsUnit (y * x) := by
      intro hu
      obtain ⟨v, hv⟩ := isUnit_iff_exists_inv'.mp hu
      exact hx (isUnit_of_mul_eq_one_finite' (v * y) x (by rw [mul_assoc]; exact hv))
    have h1 : IsUnit (1 + y * x) := by
      rcases IsLocalRing.isUnit_or_isUnit_of_add_one (a := 1 + y * x) (b := -(y * x))
          (by abel) with h | h
      · exact h
      · exact absurd (by simpa using h.neg) hyx
    obtain ⟨z, hz⟩ := isUnit_iff_exists_inv'.mp h1
    refine ⟨z, ?_⟩
    rw [Ideal.mem_bot, mul_add, mul_one, mul_assoc] at *
    rw [add_comm] at hz
    rw [hz, sub_self]

/-- If `j` is in the Jacobson radical then `1 + j` is a unit. -/
theorem isUnit_one_add_of_mem_jacobson {j : E} (hj : j ∈ Ring.jacobson E) :
    IsUnit (1 + j) := by
  have hj' : ¬ IsUnit j := (mem_jacobson_iff_not_isUnit E j).mp hj
  rcases IsLocalRing.isUnit_or_isUnit_of_add_one (a := 1 + j) (b := -j) (by abel) with h | h
  · exact h
  · exact absurd (by simpa using h.neg) hj'

instance instFiniteResidue : Finite (E ⧸ Ring.jacobson E) := Quotient.finite _

instance instNontrivialResidue : Nontrivial (E ⧸ Ring.jacobson E) :=
  Ideal.Quotient.nontrivial_iff.mpr (jacobson_ne_top E)

/-- Every element of the residue ring is either a unit or zero. -/
theorem isUnit_or_eq_zero_residue (a : E ⧸ Ring.jacobson E) : IsUnit a ∨ a = 0 := by
  obtain ⟨x, rfl⟩ := Ideal.Quotient.mk_surjective a
  by_cases hx : x ∈ Ring.jacobson E
  · right
    rwa [Ideal.Quotient.eq_zero_iff_mem]
  · left
    have : IsUnit x := not_not.mp (fun h => hx ((mem_jacobson_iff_not_isUnit E x).mpr h))
    exact this.map (Ideal.Quotient.mk (Ring.jacobson E))

/-- The residue ring `E ⧸ J` is a division ring; by Wedderburn it is in fact a (finite)
field, so `littleWedderburn` upgrades this to `Field` automatically. -/
noncomputable instance instDivisionRingResidue : DivisionRing (E ⧸ Ring.jacobson E) :=
  DivisionRing.ofIsUnitOrEqZero (isUnit_or_eq_zero_residue E)

/-- The unit group of the residue field is solvable (it is cyclic). -/
theorem isSolvable_units_residue : IsSolvable (E ⧸ Ring.jacobson E)ˣ := by
  letI := IsCyclic.commGroup (α := (E ⧸ Ring.jacobson E)ˣ)
  exact CommGroup.isSolvable

/-! ### The reduction homomorphism on units and its kernel `1 + J` -/

/-- The reduction homomorphism `Eˣ → (E ⧸ J)ˣ`. -/
noncomputable def residueUnits : Eˣ →* (E ⧸ Ring.jacobson E)ˣ :=
  Units.map (Ideal.Quotient.mk (Ring.jacobson E)).toMonoidHom

/-- The kernel `1 + J` of the reduction map has the same cardinality as the additive group
of the Jacobson radical (via the bijection `u ↦ (u : E) - 1`). -/
theorem card_ker_eq_card_jacobson :
    Nat.card (MonoidHom.ker (residueUnits E)) = Nat.card (Ring.jacobson E) := by
  have key : ∀ u : Eˣ, u ∈ MonoidHom.ker (residueUnits E) ↔ (u:E) - 1 ∈ Ring.jacobson E := by
    intro u
    rw [MonoidHom.mem_ker, ← Ideal.Quotient.eq_zero_iff_mem]
    constructor
    · intro hu
      have h1 : Ideal.Quotient.mk (Ring.jacobson E) (u:E) = 1 := by
        simpa [residueUnits, Units.coe_map] using congrArg Units.val hu
      simp [h1]
    · intro hu
      have h1 : Ideal.Quotient.mk (Ring.jacobson E) (u:E) = 1 := by
        rw [map_sub, map_one, sub_eq_zero] at hu; exact hu
      ext; simp [residueUnits, Units.coe_map, h1]
  apply Nat.card_congr
  exact {
    toFun := fun u => ⟨(u.1:E) - 1, (key u.1).mp u.2⟩
    invFun := fun j => ⟨(isUnit_one_add_of_mem_jacobson E j.2).unit,
      (key _).mpr (by simp)⟩
    left_inv := fun u => by
      apply Subtype.ext; apply Units.ext; simp
    right_inv := fun j => by
      apply Subtype.ext; simp }

/-! ### Cardinality: a finite local ring has prime-power order -/

/-- A finite local ring has prime-power cardinality; moreover the additive group is a
`p`-group for that prime `p` (the characteristic of the residue field). -/
theorem exists_prime_pow_card :
    ∃ (p n : ℕ), p.Prime ∧ Nat.card E = p ^ n := by
  set F := E ⧸ Ring.jacobson E with hF
  have hp : (ringChar F).Prime := CharP.prime_ringChar F
  set c := ringChar F with hc
  haveI : Fact c.Prime := ⟨hp⟩
  -- `(c : E)` reduces to zero in the residue field, hence lies in the Jacobson radical.
  have hcmem : (c : E) ∈ Ring.jacobson E := by
    rw [← Ideal.Quotient.eq_zero_iff_mem]
    show (Ideal.Quotient.mk (Ring.jacobson E)) (c : E) = 0
    rw [map_natCast]
    exact_mod_cast (ringChar.spec F c).mpr dvd_rfl
  -- The Jacobson radical is nilpotent, so some power of `(c : E)` is zero.
  obtain ⟨K, hK⟩ := IsArtinianRing.isNilpotent_jacobson_bot (R := E)
  rw [Ideal.jacobson_bot] at hK
  have hcK : ((c ^ K : ℕ) : E) = 0 := by
    rw [Nat.cast_pow]
    have : (c : E) ^ K ∈ (Ring.jacobson E) ^ K := Ideal.pow_mem_pow hcmem K
    rw [hK] at this
    exact Ideal.mem_bot.mp this
  -- Therefore the additive group of `E`, viewed multiplicatively, is a `c`-group.
  have hpg : IsPGroup c (Multiplicative E) := by
    intro g
    refine ⟨K, ?_⟩
    apply Multiplicative.toAdd.injective
    have hsmul : (c ^ K) • (Multiplicative.toAdd g) = 0 := by
      rw [nsmul_eq_mul, hcK, zero_mul]
    simpa using hsmul
  obtain ⟨n, hn⟩ := (IsPGroup.iff_card (p := c) (G := Multiplicative E)).mp hpg
  exact ⟨c, n, hp, by simpa using hn⟩

/-- The kernel `1 + J` of the reduction map is a `p`-group. -/
theorem isPGroup_ker :
    ∃ p : ℕ, p.Prime ∧ IsPGroup p (MonoidHom.ker (residueUnits E)) := by
  obtain ⟨p, n, hp, hcard⟩ := exists_prime_pow_card E
  refine ⟨p, hp, ?_⟩
  haveI : Fact p.Prime := ⟨hp⟩
  rw [IsPGroup.iff_card, card_ker_eq_card_jacobson]
  have hdvd : Nat.card (Ring.jacobson E) ∣ Nat.card E :=
    AddSubgroup.card_addSubgroup_dvd_card (Ring.jacobson E).toAddSubgroup
  rw [hcard] at hdvd
  obtain ⟨m, _, hm⟩ := (Nat.dvd_prime_pow hp).mp hdvd
  exact ⟨m, hm⟩

/-! ### Theorem A -/

/-- **Theorem A.** The unit group of a finite local ring is solvable.

`Eˣ → (E/J)ˣ` has kernel `1 + J`. The kernel is a `p`-group (hence solvable) and the
codomain `(E/J)ˣ` is cyclic (hence solvable), so `Eˣ` is solvable as an extension. -/
theorem isSolvable_units_of_finite_local : IsSolvable Eˣ := by
  obtain ⟨p, hp, hpg⟩ := isPGroup_ker E
  haveI : Fact p.Prime := ⟨hp⟩
  haveI hnil : Group.IsNilpotent (MonoidHom.ker (residueUnits E)) := hpg.isNilpotent
  haveI hker : IsSolvable (MonoidHom.ker (residueUnits E)) := IsNilpotent.to_isSolvable
  haveI : IsSolvable (E ⧸ Ring.jacobson E)ˣ := isSolvable_units_residue E
  exact solvable_of_ker_le_range
    (f := (MonoidHom.ker (residueUnits E)).subtype) (g := residueUnits E)
    (by rw [Subgroup.subtype_range])

end BelyiSolvable

namespace BelyiSolvable

/-- In a finite monoid, some positive power of any element is idempotent. -/
theorem exists_pow_isIdempotent {M : Type*} [Monoid M] [Finite M] (a : M) :
    ∃ n, 0 < n ∧ IsIdempotentElem (a ^ n) := by
  obtain ⟨i, j, hij, hfij⟩ := Finite.exists_ne_map_eq_of_infinite (fun n : ℕ => a ^ (n + 1))
  wlog hlt : i < j generalizing i j
  · exact this j i hij.symm hfij.symm (by omega)
  set s := i + 1 with hs
  set t := j - i with ht
  have hts : 0 < t := by omega
  have hbase : a ^ s = a ^ (s + t) := by
    have hj : j + 1 = s + t := by omega
    rw [hfij, hj]
  have step : ∀ x, s ≤ x → a ^ x = a ^ (x + t) := by
    intro x hx
    obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hx
    calc a ^ (s + d) = a ^ s * a ^ d := by rw [pow_add]
      _ = a ^ (s + t) * a ^ d := by rw [hbase]
      _ = a ^ (s + t + d) := by rw [← pow_add]
      _ = a ^ (s + d + t) := by rw [show s + t + d = s + d + t from by omega]
  set N := s * t with hN
  have hNs : s ≤ N := Nat.le_mul_of_pos_right s hts
  have hmul : ∀ k, a ^ (N + t * k) = a ^ N := by
    intro k
    induction k with
    | zero => simp
    | succ m ih =>
      have hrw : N + t * (m + 1) = (N + t * m) + t := by ring
      rw [hrw, ← step (N + t * m) (by omega), ih]
  refine ⟨N, Nat.mul_pos (by omega) hts, ?_⟩
  have hfin : a ^ (N + N) = a ^ N := by
    have hs2 := hmul s
    have heq : t * s = N := by rw [hN]; ring
    rw [heq] at hs2; exact hs2
  show a ^ N * a ^ N = a ^ N
  rw [← pow_add]; exact hfin

/-- A finite nontrivial ring whose only idempotents are `0` and `1` is local: for any `a`,
some power `a ^ n` is idempotent, hence `0` (making `a` nilpotent, so `1 - a` a unit) or `1`
(making `a` a unit). -/
theorem isLocalRing_of_finite_of_isIdempotentElem {R : Type*} [Ring R] [Finite R] [Nontrivial R]
    (h : ∀ e : R, IsIdempotentElem e → e = 0 ∨ e = 1) : IsLocalRing R := by
  apply IsLocalRing.of_isUnit_or_isUnit_one_sub_self
  intro a
  obtain ⟨n, hn, hidem⟩ := exists_pow_isIdempotent a
  rcases h _ hidem with h0 | h1
  · right
    exact IsNilpotent.isUnit_one_sub ⟨n, h0⟩
  · left
    refine isUnit_of_mul_eq_one_finite a (a ^ (n - 1)) ?_
    rw [← pow_succ', show n - 1 + 1 = n from by omega]
    exact h1

/-- The endomorphism ring of a finite module is finite. -/
instance finite_moduleEnd {A M : Type*} [Ring A] [AddCommGroup M] [Module A M] [Finite M] :
    Finite (Module.End A M) := by
  have : Function.Injective (fun (f : Module.End A M) => (f : M → M)) := by
    intro f g h
    ext m
    exact congrFun h m
  exact Finite.of_injective _ this

/-- **Theorem B.** If a finite `A`-module `M` has local endomorphism ring (e.g. `M`
indecomposable of finite length, by Fitting), then its automorphism group is solvable. -/
theorem isSolvable_moduleAut_of_localEnd
    {A M : Type*} [Ring A] [AddCommGroup M] [Module A M] [Finite M]
    [IsLocalRing (Module.End A M)] :
    IsSolvable (Module.End A M)ˣ :=
  isSolvable_units_of_finite_local (Module.End A M)

/-- Fitting's lemma (the geometry-to-algebra bridge): a finite indecomposable module has
local endomorphism ring. -/
theorem isLocalRing_end_of_indecomposable
    {A M : Type*} [Ring A] [AddCommGroup M] [Module A M] [Finite M]
    (hM : ∀ e : Module.End A M, IsIdempotentElem e → e = 0 ∨ e = 1) (hM0 : Nontrivial M) :
    IsLocalRing (Module.End A M) :=
  isLocalRing_of_finite_of_isIdempotentElem hM

end BelyiSolvable
