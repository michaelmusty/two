# Gate 3 closed: the level-`q0` new quotient carries `f`'s residual system

**Date:** 2026-08-27. Output: `../data/computed/gate3_genkernel_q0.out`
(script `../magma/48_gate3_genkernel.m`, attempt 3 on chatelet, one Magma
session, 40 GB cap, 10.4 GB peak). Audit trail: `gate3-method-audit.md`
(including the 2026-08-26 correction), D24–D28.

## Statement

Let `F = Q(ζ_32)^+`, `q0` the prime of `F` above 7 of norm 2401, `f` the
level-1 parallel-weight-2 eigenform with 16-dimensional Hecke orbit and Hecke
field `H`, and `λ` the prime of `H` above 2 with `a_{q0}(f) ≡ 0 mod λ` (gate 1,
D23). Let `f1` be the minimal polynomial over `F_2` of `a_31(f) mod λ` and, for
`ℓ ∈ {31, 97, 127, 191}`, let `f1^{(ℓ)}` be the characteristic polynomial of
`T_ℓ` on the `f1`-primary part of the level-1 module mod 2 (equivalently, the
minimal polynomial of `a_ℓ(f) mod λ`; each is irreducible of degree 8).

**Verified.** In the level-`q0` Brandt module mod 2 (dimension 109240), with
`G = ker f1(T_31)^2`:

| | |
|---|---|
| `dim G` | 32 (so `f1` has multiplicity 4 in `charpoly(T_31 mod 2)`) |
| `rank f1(T_31)|_G` | 16 (`T_31` has Jordan blocks of size exactly 2 on `G`) |
| `charpoly(T_ℓ|_G)` for `ℓ = 31, 97, 127, 191` | `(f1^{(ℓ)})^4` in every case |
| `charpoly(T_ℓ|_{G/O})`, `O` = old subspace | `(f1^{(ℓ)})^2` in every case |

and the four operators commute pairwise (0 failures of 27 random-vector
checks), so `G` is stable under each and the restrictions are well defined.

## The argument

1. **Old contribution is exactly two copies of level 1.** The old subspace at
   level `q0` is, per level-1 eigenform, the 2-dimensional space of
   Iwahori-fixed vectors in an unramified principal series of `GL_2(F_{q0})`;
   `T_ℓ` (`ℓ ≠ q0`) commutes with both degeneracy maps. Hence
   `charpoly(T_ℓ | Old) = charpoly(T_ℓ | level 1)^2`, over `Z`, and therefore
   mod 2. On the `f1`-primary part this is `(f1^{(ℓ)})^2`, because `f1` occurs
   with multiplicity exactly 1 in the full level-1 characteristic polynomial
   mod 2 (`44_gate3_baseline.m`, D26a). No injectivity of degeneracy maps is
   used: the count is a local statement in characteristic zero and the
   reduction of a characteristic polynomial is basis-independent.

2. **The excess is new.** `charpoly(T_31 | M_q0) = charpoly(T_31 | Old) ·
   charpoly(T_31 | New)` over `Z` (the new subspace is the Hecke-stable
   complement). Multiplicity 4 of `f1` at level `q0` against 2 from `Old`
   forces multiplicity 2 in `charpoly(T_31 | New) mod 2`: there are
   characteristic-zero newforms `g` of level `q0` whose `a_31` reduces, at some
   prime of their Hecke field above 2, to a root of `f1`.

3. **Their residual system is `f`'s at four primes.** `G` contains the
   `f1`-primary part of `Old mod 2` (16-dimensional) and
   `charpoly(T_ℓ | G) = charpoly(T_ℓ | G ∩ Old) · charpoly(T_ℓ | G/(G ∩ Old))`.
   With step 1, `charpoly(T_ℓ | G) = (f1^{(ℓ)})^4` gives
   `charpoly(T_ℓ | new quotient) = (f1^{(ℓ)})^2` for each of
   `ℓ = 31, 97, 127, 191`. So the newforms of step 2 satisfy
   `a_ℓ(g) ≡ (a root of f1^{(ℓ)}) mod λ_g` at all four primes: the residual
   Hecke eigenvalues of `g` and `f` share minimal polynomials at 31, 97, 127
   and 191, with the pairing between the four polynomials fixed by the single
   prime `λ` on the `f` side (they were all computed on the level-1
   `f1`-primary part, not matched by index).

4. **Steinberg at `q0`.** `g` is new of prime level `q0` with trivial
   character; the local component at `q0` has conductor exponent 1 and
   trivial central character, hence is special: Steinberg up to an unramified
   quadratic twist, `a_{q0}(g) = ±1`. This is what the Cerednik–Drinfeld side
   needs (`levelraise-cd-plan.md`): `g` is discrete series at `q0` and at the
   eight real places, so by Jacquet–Langlands it transfers to the indefinite
   quaternion algebra ramified at `q0` and seven real places.

5. **Non-semisimplicity, correctly read.** `T_31` has Jordan blocks of size 2
   on `G` while it is semisimple on `G ∩ Old`. Given step 3 this is consistent
   with old/new gluing by the congruence, but — as `gate3-method-audit.md`
   (2026-08-26) records — it is not itself evidence: a newform whose order at
   2 is non-maximal produces the same Jordan data with a split module. It is
   now a corollary, not a signature.

## What is and is not established

- **Established (finite computation):** newforms `g` of level exactly `q0`,
  Steinberg at `q0`, exist with `a_ℓ(g) mod λ_g` and `a_ℓ(f) mod λ` conjugate
  over `F_2` for `ℓ = 31, 97, 127, 191`. This is the level-raising conclusion
  at the level a Brauer–Nesbitt-type comparison on four primes can reach.
- **Not proved:** `ρ̄_g ≅ ρ̄_f`. Two gaps, both known and both accepted for the
  route: (i) four primes are not a Sturm bound, and no affordable bound exists
  at this level (D13); (ii) "same minimal polynomial" allows a Galois
  conjugate system, which cuts out the *same field* `E` and is therefore
  harmless for the objective but is a weaker statement. Neither is closed by
  more primes at present cost, and neither needs to be: the final
  Galois-group certification of the explicit polynomial (gate 5) is the check
  that catches a wrong `g`.
- **Deliberately not invoked:** level-raising theorems at `ℓ = 2` for even
  `[F:Q]` and level 1 (D24b). The computation replaces them.

## Provenance and reproducibility

- Same-session discipline (D26b): all four operators were built in one Magma
  session and are banked from that session as integer sparse matrices,
  `two_gate3/gk_s3_T{31,97,127,191}.m` (39 / 118 / 154 / 231 MB) — a
  commuting set in one basis, reusable together (but not with any other bank).
- The sparse-Hecke patch (`../patches/`) must be applied to the pinned package.
- Costs (attempt 3, host lightly loaded): level-1 phase ~1 h; `T_31, T_97,
  T_127, T_191` at `q0`: 856 / 2647 / 2898 / 5163 s; `f1(T_31)` 3101 s;
  square 595 s; kernel 276 s; restrictions negligible. Peak memory 10.4 GB.
- Attempt 1 died at CoCalc's 120 CPU-second default rlimit; attempt 2 at a
  16 GB cap (dense operators). Both recorded in D27.

## Consequence for the plan

Gate 3 is closed. The route's next binding question is not on the Hecke side
at all: it is `Δ'`, the determinant of the period-valuation pairing, which
decides whether the Fourier-expansion back end can reach recognition precision
at genus 16 (`gate5-genus16-term-count.md`, §5). The banked four-operator set
is the input for the `g`-isotypic sublattice that computation needs.
