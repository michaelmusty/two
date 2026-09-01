# The Tate pilot: q0-adic periods → algebraic recognition, at dimension 1

**Date:** 2026-09-01. Follows `stocktake-2026-09-01.md` (option (b)) and the
gate-4 scoping trio (`gate4-darmonpoints-assessment.md`,
`gate4-dim2-calibration.md`, `gate4-kernel-rewrite-scope.md`).

## Object and goal

Level p31 (the norm-31 prime of `F = Q(ζ32)⁺`) carries five **rational** new
eigenforms (`a_97 ∈ {14, 6, 2, −6, −14}`, from `dp31` banks / 49b) — elliptic
curves over `F` of conductor p31, Steinberg at p31, hence Tate curves over
`F_{p31} = Q_31`. The pilot computes, for (at least) one of them, the Tate
parameter `q_E ∈ Q_31^×` from **definite Brandt data plus an overconvergent
lift**, then recognizes `j_E = 1/q + 744 + 196884q + …` as a global algebraic
number in `F` by LLL, reconstructs the curve, and derives its 2-division
field. It is the entire option-(b) chain — q0-adic periods in place of the
dead archimedean/theta front ends — at dimension 1, where ground truth is
checkable.

Why this is the right experiment (stock-take §2): it decides the
computational half of option (b) cheaply, and it delivers the recognition
precision `M_rec` that `roadmap-reevaluation.md` flagged as the project's
binding uncertainty.

## Why the pilot avoids the two known blockers

- The gate-4 **coefficient blocker** (overconvergent normalization over a
  degree-16 Hecke field) vanishes: the eigenform is rational, `U_31 = ±1` is
  a scalar, slope 0 — exactly the situation `darmonpoints`' lift already
  handles (dim-2 calibration, Result 1).
- The gate-4 **cost blocker** vanishes: cost ~ positions × cosets × `M³` with
  positions ≈ 1461, cosets = 32; at `M = 20` the Python-constant estimate is
  ~2 core-h, at `M = 60` ~2 days — fine either way.
- The remaining blocker is the known one: `darmonpoints` has **no definite
  branch** for a totally real base (every path lands in the Fuchsian
  fundamental domain, hopeless at genus ~1400 even at level 31). The pilot's
  new code is therefore the **definite S-arithmetic group class** — the
  ~14-method seam the assessment already traced (`reduce_in_amalgam` is
  already purely p-adic; generators from the finite unit groups + Brandt
  gluing elements; `get_BT_reps` overridden with the explicit `P¹(F_q0)`
  neighbours; `embed` via the splitting `B ⊗ F_{p31} ≅ M₂(Q_31)`).

## Phases

1. **Lattice data** (`56_tate_pilot_lattice.m`, chatelet — RUNNING):
   rebuild `T_97, T_127, U_31` in one session; per curve: the saturated rank-1
   character-lattice vector `v`, `ord(q_E) = ⟨v,v⟩` under the stab-order
   monodromy pairing (D31), the `U_31` sign (split/non-split), `a_127`.
   Banks `tate_*.m` pin the working basis for all later phases.
   *Checks:* `T_97` charpoly matches the dp31 bank; self-adjointness of all
   three operators (whether `U_31` is self-adjoint for the Iwahori pairing is
   *reported*, not assumed); eigen-consistency of `U_31`, `T_127` on `v`.
2. **Element-level Brandt data** (Magma → JSON): the group-class inputs that
   counts do not provide — ideal-class representatives, the p31-Iwahori
   `P¹(F_{p31})` neighbour elements (tree edges with their actual quaternion
   representatives), unit-group generators of the stabilizers, a splitting
   `B → M₂(Q_31)` to precision `31^M`. All standard Magma quaternion
   intrinsics; new script `57`.
3. **The group class** (Python, `dembele/tate_pilot/`): implement the
   ~14-method interface against phase-2 data; wire into
   `cohomology_arithmetic`/`integrals`. Validation ladder:
   (a) internal — the class's harmonic-cocycle space must reproduce the
   Brandt eigensystems (`a_97`, `a_127`, `U`-signs) from phase 1;
   (b) if a definite-over-Q or split configuration permits, reproduce a known
   `E/Q` Tate parameter against `E.tate_curve(p).parameter()` (ground truth
   with zero ambiguity);
   (c) the degree-8 run.
4. **Integration and recognition**: overconvergent lift of the eigencocycle
   (slope 0, rational normalization), the multiplicative double integral for
   `q_E`, then `j_E` and LLL recognition in `F` (degree ≤ 8, `v_{p31}(j) =
   −ord(q_E)` known from phase 1 — a sharp prior AND a check; `j` integral
   away from p31). Reconstruct `E` up to quadratic twist, pin the twist by
   conductor + traces, verify `a_97, a_127`, then compute the 2-division
   field. Record `M_rec` = the precision LLL actually needed.

## Success / failure criteria

- **Success**: a recognized `j_E ∈ F` passing the valuation/integrality/trace
  checks, and the measured `M_rec`. Then option (b)'s scaling question (the
  `λ`-locality of `B_g[λ]` and the degree-16-block analog of this chain) is
  worth real investment.
- **Failure modes that are still informative**: recognition needs `M` beyond
  reach (kills option (b) on precision grounds — the same number would have
  killed gate 4 anyway); the group class stalls on degree-8 arithmetic
  (localizes the true implementation frontier).

## Costs

Phase 1: one chatelet session (~2–3 h). Phase 2: ~a day of Magma scripting,
minutes of compute. Phase 3: the real work — days of implementation. Phase 4:
hours of compute at `M ≤ 60`, plus LLL at height ~`M·log 31`.
