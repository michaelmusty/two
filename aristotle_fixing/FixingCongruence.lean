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

/-- If `k = 2^j` and an odd prime `p` divides `2^k + 1`,
then `2^(j+1)` divides `p - 1`. -/
theorem fixing_congruence_gl (j : ℕ) (p : ℕ) (hp : p.Prime) (hp2 : p ≠ 2)
    (hdvd : p ∣ 2 ^ (2 ^ j) + 1) : 2 ^ (j + 1) ∣ p - 1 := by
  sorry

/-- Every odd prime divisor of `q² + 1` with `q` even is `≡ 1 mod 4`. -/
theorem fixing_congruence_sz (q : ℕ) (hq : 2 ∣ q) (p : ℕ) (hp : p.Prime)
    (hp2 : p ≠ 2) (hdvd : p ∣ q ^ 2 + 1) : 4 ∣ p - 1 := by
  sorry

/-- If `x` has order dividing `2^m` in a group and `p ≡ 1 mod 2^m`,
then `x^p = x`: such `p` fix every class of 2-power order `≤ 2^m`. -/
theorem twist_fixes {G : Type*} [Group G] (x : G) (m p : ℕ)
    (hx : x ^ (2 ^ m) = 1) (hp : 2 ^ m ∣ p - 1) (hp1 : 1 ≤ p) : x ^ p = x := by
  sorry
