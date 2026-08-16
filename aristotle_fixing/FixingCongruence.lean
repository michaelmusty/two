/-
The fixing congruence: the combinatorial core of the moduli-field
obstruction for all-2-power branched covers (writeup/all-2-power-covers.md).

Theorem 1: if k = 2^j and a prime p divides 2^k + 1, then p ≡ 1 mod 2^(j+1).
Theorem 2: if q is even and a prime p divides q^2 + 1, then p ≡ 1 mod 4.
Theorem 3 (the fixing consequence): if x is a group element with
x^(2^m) = 1 and p ≡ 1 mod 2^m, then x^p = x.
-/
import Mathlib

open Nat

/-- Key order computation: if `a ^ (2 ^ n) = -1` in `ZMod p` for an odd prime `p`,
then `a` has multiplicative order exactly `2 ^ (n + 1)`, hence `2 ^ (n + 1) ∣ p - 1`. -/
theorem pow_two_pow_eq_neg_one_dvd_sub_one (p : ℕ) (hp : p.Prime) (hp2 : p ≠ 2)
    (a : ZMod p) (n : ℕ) (ha : a ^ (2 ^ n) = -1) : 2 ^ (n + 1) ∣ p - 1 := by
  haveI : Fact p.Prime := ⟨hp⟩
  haveI : Fact (2 < p) := ⟨lt_of_le_of_ne hp.two_le (Ne.symm hp2)⟩
  have hne : (-1 : ZMod p) ≠ 1 := ZMod.neg_one_ne_one
  have h2 : a ^ (2 ^ (n + 1)) = 1 := by
    rw [pow_succ, pow_mul, ha]; ring
  have hord : orderOf a ∣ 2 ^ (n + 1) := orderOf_dvd_of_pow_eq_one h2
  obtain ⟨i, hi, hieq⟩ := (Nat.dvd_prime_pow Nat.prime_two).1 hord
  have hin : i = n + 1 := by
    rcases Nat.lt_or_ge i (n + 1) with h | h
    · exfalso
      have h1 : a ^ (2 ^ n) = 1 := by
        apply orderOf_dvd_iff_pow_eq_one.1
        rw [hieq]
        exact pow_dvd_pow 2 (by omega)
      rw [ha] at h1
      exact hne h1
    · omega
  have ha0 : a ≠ 0 := by
    intro h
    rw [h, zero_pow (by positivity : (2 : ℕ) ^ n ≠ 0)] at ha
    exact hne (by linear_combination (-2 : ZMod p) * ha)
  have hd : orderOf a ∣ p - 1 :=
    orderOf_dvd_of_pow_eq_one (ZMod.pow_card_sub_one_eq_one ha0)
  rw [hieq, hin] at hd
  exact hd

/-- If `k = 2^j` and an odd prime `p` divides `2^k + 1`,
then `2^(j+1)` divides `p - 1`. -/
theorem fixing_congruence_gl (j : ℕ) (p : ℕ) (hp : p.Prime) (hp2 : p ≠ 2)
    (hdvd : p ∣ 2 ^ (2 ^ j) + 1) : 2 ^ (j + 1) ∣ p - 1 := by
  apply pow_two_pow_eq_neg_one_dvd_sub_one p hp hp2 (2 : ZMod p) j
  have h : ((2 ^ (2 ^ j) + 1 : ℕ) : ZMod p) = 0 := (ZMod.natCast_eq_zero_iff _ _).2 hdvd
  push_cast at h
  linear_combination h

/-- Every odd prime divisor of `q² + 1` with `q` even is `≡ 1 mod 4`.
(The evenness hypothesis `hq` is retained as stated, although the proof
does not need it: the conclusion holds for every natural number `q`.) -/
theorem fixing_congruence_sz (q : ℕ) (hq : 2 ∣ q) (p : ℕ) (hp : p.Prime)
    (hp2 : p ≠ 2) (hdvd : p ∣ q ^ 2 + 1) : 4 ∣ p - 1 := by
  have key : 2 ^ (1 + 1) ∣ p - 1 := by
    apply pow_two_pow_eq_neg_one_dvd_sub_one p hp hp2 ((q : ZMod p)) 1
    have h : ((q ^ 2 + 1 : ℕ) : ZMod p) = 0 := (ZMod.natCast_eq_zero_iff _ _).2 hdvd
    push_cast at h
    rw [pow_one]
    linear_combination h
  norm_num at key
  exact key

/-- If `x` has order dividing `2^m` in a group and `p ≡ 1 mod 2^m`,
then `x^p = x`: such `p` fix every class of 2-power order `≤ 2^m`. -/
theorem twist_fixes {G : Type*} [Group G] (x : G) (m p : ℕ)
    (hx : x ^ (2 ^ m) = 1) (hp : 2 ^ m ∣ p - 1) (hp1 : 1 ≤ p) : x ^ p = x := by
  obtain ⟨t, ht⟩ := hp
  have hpe : p = 2 ^ m * t + 1 := by omega
  rw [hpe, pow_succ, pow_mul, hx, one_pow, one_mul]
