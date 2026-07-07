import Mathlib

open scoped BigOperators
open scoped Pointwise

set_option maxHeartbeats 8000000

/-!
# Generating-pair counts for `ZMod 4` and the Klein four-group

We call an ordered pair `(a, b)` a *generating pair* of an additive group `G`
if `AddSubgroup.closure {a, b} = ⊤`.
-/

/-
Characterisation of generating pairs of `ZMod 4`: a pair `(a, b)` generates
`ZMod 4` iff at least one of `a`, `b` is a unit, i.e. equal to `1` or `3`.
-/
lemma zmod4_gen_iff (a b : ZMod 4) :
    AddSubgroup.closure ({a, b} : Set (ZMod 4)) = ⊤ ↔
      (a = 1 ∨ a = 3 ∨ b = 1 ∨ b = 3) := by
  constructor;
  · revert a b;
    intro a b h
    by_contra h_contra;
    -- Since $a$ and $b$ are not $1$ or $3$, they must be $0$ or $2$.
    have h_cases : a = 0 ∨ a = 2 := by
      fin_cases a <;> simp_all +decide
    have h_cases' : b = 0 ∨ b = 2 := by
      fin_cases b <;> simp_all +decide;
    rcases h_cases with ( rfl | rfl ) <;> rcases h_cases' with ( rfl | rfl ) <;> simp_all +decide [ AddSubgroup.eq_top_iff' ];
    · simp_all +decide [ AddSubgroup.mem_closure_singleton ];
    · simp_all +decide [ AddSubgroup.mem_closure_singleton ];
      obtain ⟨ n, hn ⟩ := h 1; replace hn := congr_arg ( fun x : ZMod 4 => x.val ) hn; norm_num at hn; have := congr_arg ( · % 2 ) hn; norm_num at this;
      erw [ ZMod.val_mul ] at this ; norm_num at this; have := ZMod.val_lt ( n : ZMod 4 ) ; interval_cases ( n : ZMod 4 ).val <;> contradiction;
    · simp_all +decide [ AddSubgroup.mem_closure_pair ];
      obtain ⟨ m, hm ⟩ := h 1; replace hm := congr_arg ( fun x : ZMod 4 => x.val ) hm; norm_num at hm; have := congr_arg ( · % 2 ) hm; norm_num at this;
      erw [ ZMod.val_mul ] at this ; norm_num at this; have := ZMod.val_lt ( m : ZMod 4 ) ; interval_cases ( m : ZMod 4 ).val <;> trivial;
    · simp_all +decide [ AddSubgroup.mem_closure_singleton ];
      obtain ⟨ n, hn ⟩ := h 1; replace hn := congr_arg ( fun x : ZMod 4 => x.val ) hn; norm_num at hn; have := congr_arg ( · % 2 ) hn; norm_num at this;
      erw [ ZMod.val_mul ] at this ; norm_num at this; have := ZMod.val_lt ( n : ZMod 4 ) ; interval_cases ( n : ZMod 4 ).val <;> contradiction;
  · intro h
    have h_closure : ∀ x : ZMod 4, x ∈ AddSubgroup.closure {a, b} := by
      rcases h with ( rfl | rfl | rfl | rfl ) <;> simp_all +decide [ AddSubgroup.mem_closure_pair ];
      · exact fun x => ⟨ x.val, 0, by fin_cases x <;> fin_cases b <;> trivial ⟩;
      · intro x; use x.val * 3; use 0; fin_cases x <;> simp +decide ;
      · exact fun x => ⟨ 0, x.val, by fin_cases x <;> simp +decide ⟩;
      · intro x; use 0; use x.val * 3; fin_cases x <;> fin_cases a <;> trivial;
    exact SetLike.ext fun x => by simpa using h_closure x;

/-
Characterisation of generating pairs of the Klein four-group
`ZMod 2 × ZMod 2`: a pair `(a, b)` generates iff `a`, `b` are nonzero and
distinct.
-/
lemma klein_gen_iff (a b : ZMod 2 × ZMod 2) :
    AddSubgroup.closure ({a, b} : Set (ZMod 2 × ZMod 2)) = ⊤ ↔
      (a ≠ 0 ∧ b ≠ 0 ∧ a ≠ b) := by
  refine' ⟨ _, fun h => _ ⟩;
  · intro h;
    refine' ⟨ _, _, _ ⟩ <;> contrapose! h;
    · simp_all +decide [ AddSubgroup.eq_top_iff', AddSubgroup.mem_closure_singleton ];
      fin_cases b <;> simp_all +decide [ Prod.ext_iff ];
      · exact ⟨ 1, 0, by simp +decide ⟩;
      · exact ⟨ 0, 1, by simp +decide ⟩;
      · exact ⟨ 0, 1, by simp +decide ⟩;
    · simp +decide [ h, AddSubgroup.eq_top_iff' ];
      fin_cases a <;> simp +decide [ AddSubgroup.mem_closure_pair ];
      · simp +decide [ AddSubgroup.mem_closure_singleton ];
      · exact ⟨ 1, 1, by simp +decide ⟩;
      · exact ⟨ 0, 1, by simp +decide ⟩;
      · exists 0, 1;
        lia;
    · fin_cases a <;> simp +decide [ *, SetLike.ext_iff ];
      · refine' ⟨ 1, 0, _ ⟩ ; simp +decide [ h.symm ];
        simp +decide [ AddSubgroup.mem_closure_singleton ];
      · refine' ⟨ 1, 0, _ ⟩ ; simp +decide [ ← h ];
        simp +decide [ AddSubgroup.mem_closure_singleton ];
      · refine' ⟨ 0, 1, _ ⟩ ; simp +decide [ AddSubgroup.mem_closure_pair ];
        intro x y; subst h; simp +decide [ Prod.ext_iff ] ;
      · refine' ⟨ 1, 0, _ ⟩ ; simp +decide [ AddSubgroup.mem_closure_pair ];
        intro x y; subst h; simp +decide [ Prod.ext_iff ] ;
        grind;
  · refine' eq_top_iff.mpr fun x hx => _;
    fin_cases x <;> simp_all +decide [ AddSubgroup.mem_closure_pair ];
    · exact ⟨ 0, 0, by simp +decide ⟩;
    · fin_cases a <;> fin_cases b <;> simp_all +decide;
      exacts [ ⟨ 1, 0, by simp +decide ⟩, ⟨ 1, 0, by simp +decide ⟩, ⟨ 0, 1, by simp +decide ⟩, ⟨ 1, -1, by simp +decide ⟩, ⟨ 0, 1, by simp +decide ⟩, ⟨ 1, -1, by simp +decide ⟩ ];
    · fin_cases a <;> fin_cases b <;> simp_all +decide;
      all_goals by_contra! h;
      all_goals have h₁ := h 0 1; have h₂ := h 1 0; have h₃ := h 1 1; simp_all +decide ;
    · fin_cases a <;> fin_cases b <;> simp_all +decide;
      exacts [ ⟨ 1, 1, rfl ⟩, ⟨ 0, 1, rfl ⟩, ⟨ 1, 1, rfl ⟩, ⟨ 0, 1, rfl ⟩, ⟨ 1, 0, rfl ⟩, ⟨ 1, 0, rfl ⟩ ]

/-- **Theorem 1.** The cyclic group `ZMod 4` has exactly `12` generating pairs. -/
theorem zmod4_gen_count :
    {p : ZMod 4 × ZMod 4 | AddSubgroup.closure ({p.1, p.2} : Set (ZMod 4)) = ⊤}.ncard = 12 := by
  have h : {p : ZMod 4 × ZMod 4 | AddSubgroup.closure ({p.1, p.2} : Set (ZMod 4)) = ⊤}
      = ↑((Finset.univ : Finset (ZMod 4 × ZMod 4)).filter
          (fun p => p.1 = 1 ∨ p.1 = 3 ∨ p.2 = 1 ∨ p.2 = 3)) := by
    ext p
    simp only [Set.mem_setOf_eq, Finset.coe_filter, Finset.mem_univ, true_and,
      Set.mem_setOf_eq]
    exact zmod4_gen_iff p.1 p.2
  rw [h, Set.ncard_coe_finset]
  decide

/-- **Theorem 2.** The Klein four-group `ZMod 2 × ZMod 2` has exactly `6`
generating pairs. -/
theorem klein_gen_count :
    {p : (ZMod 2 × ZMod 2) × (ZMod 2 × ZMod 2) |
        AddSubgroup.closure ({p.1, p.2} : Set (ZMod 2 × ZMod 2)) = ⊤}.ncard = 6 := by
  have h : {p : (ZMod 2 × ZMod 2) × (ZMod 2 × ZMod 2) |
        AddSubgroup.closure ({p.1, p.2} : Set (ZMod 2 × ZMod 2)) = ⊤}
      = ↑((Finset.univ : Finset ((ZMod 2 × ZMod 2) × (ZMod 2 × ZMod 2))).filter
          (fun p => p.1 ≠ 0 ∧ p.2 ≠ 0 ∧ p.1 ≠ p.2)) := by
    ext p
    simp only [Set.mem_setOf_eq, Finset.coe_filter, Finset.mem_univ, true_and,
      Set.mem_setOf_eq]
    exact klein_gen_iff p.1 p.2
  rw [h, Set.ncard_coe_finset]
  decide