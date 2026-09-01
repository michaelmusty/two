# Stock-take, 2026-09-01 — after the gate-5 no-go (D32)

Written the morning after the q0 `d_g` determination. Prior state:
`levelraise-cd-plan.md` (the route), `roadmap-reevaluation.md` (its costs),
`gate5-genus16-term-count.md` (the feasibility gate), D23–D32.

## 1. What is now known

**The level-raising route's unpriced assumption is false at q0, and heuristically
false everywhere.** The route needed the congruent newform `g` at the auxiliary
prime to span a *small* rational Hecke orbit — the gate-4 term count is
`1.1·10^4 · M^{d_g}/Δ'`, feasible only for `d_g ≈ 16` (or smaller) with `Δ'`
large. D32 proved `d_g > 16` at q0: the two 2-adic pieces carrying the residual
system each sit inside rational orbits of degree > 16 (Deligne-bound
certification, 0 of 3 sub-products pass, margins `2^190` vs `2^71`).

This is not bad luck specific to q0:

- **Size bias.** The residual block lands in orbits weighted by dimension. The
  new space at a usable auxiliary prime has dimension `≈ 57·(Nq0+1)` (109 240
  at q0), and empirically its decomposition is dominated by giant orbits
  (level 31: degrees {1×5, 656, 684} — small orbits hold 5/1460 ≈ 0.3% of the
  dimension). Heuristic `P(d_g ≤ 16)` per candidate: **≲ 1%**.
- **Structure is forbidden.** The known mechanisms that force small orbits —
  CM, base change, inner twists — all impose structure on the residual
  representation. Ours is Dembélé's, with nonsolvable image `SL₂(F₂₅₆)`:
  CM would make the residual dihedral; base-change/twist structure would
  descend to the residual system, contradicting its `C₈`-orbit shape. A small
  `d_g` at some future prime would therefore be an *unstructured accident*
  (a sporadic rational eigenform), not something any selection principle can
  target.

Additionally, the `f1`-new lattice is only `Z₂`-rational, so the `Δ'`-as-
integer object (D27c/D29/D30) does not exist at this prime independently of
the term count.

## 2. The options, priced

**(a) More auxiliary primes — a lottery, not a plan.** The scan bank holds 54
scanned rationals, 1 hit (q0). The usable window (`norm ≤ 5000`, set by the
gate-4 `Nq0²M²` ceiling) has ~29 rationals left: expected additional gate-1
hits ≈ 0.1, times `P(d_g small) ≲ 1%` ⇒ path success probability **~10⁻³**.
The full window adds hits that gate 4 cannot afford anyway. Marginal cost is
low (3 background lanes + one validated ~8 h `51` run per hit), so it can run
as a *background lottery*, but it cannot be the plan.

**(b) 2-adic/toric rework of gate 4 — the live mathematical direction.** The
needed object is not `B_g` (dimension `d_g`, huge) but its `λ`-torsion, `λ|2`
in `O_{K_g}` with residual `f1`. In the Cerednik–Drinfeld uniformization
`B_g = T/Λ` over `Q_{q0}`, torsion plausibly *localizes at `λ`*: `B_g[λ]`
should involve only `X/λX` and `λ`-divided periods, i.e. exactly the rank-16
2-adic block we have banked (`dp_hg_f1.m`) plus 16 columns of q0-adic periods
— whose cost was already measured (~110 core-h at `Nq0 ~ 2000`, `M = 20`,
roadmap-reevaluation) — NOT the `M^16` theta enumeration, which came from the
recognition strategy, not the periods. Two open questions, in order:
  1. *(paper math)* Does `B_g[λ]` in the CD uniformization depend only on the
     `λ`-isotypic block of `(X, Λ)`? (Ribet/component-group calculations
     suggest torsion questions localize; needs a real argument.)
  2. *(computational)* Can `λ`-division + LLL recognition replace the theta
     front end at affordable precision `M_rec`?

**The decisive pilot exists and is cheap:** level 31 has five *rational* new
eigenforms — elliptic curves over `F` with multiplicative reduction at the
norm-31 prime, i.e. rank-1 character lattices inside the banked 1461-dim
Brandt lattice (`dp31_*` banks, eigenvalues {14, 6, 2, −6, −14}). Computing
one Tate parameter q0-adically from Brandt data + an overconvergent lift, then
recognizing the 2-torsion field of the (identifiable) curve, tests the entire
(b) machinery end-to-end at dimension 1 — and simultaneously delivers the
`M_rec` calibration that `roadmap-reevaluation.md` already demanded. If the
pilot fails, (b) dies cheaply; if it works, scale questions come next.

**(c) The plan's contingencies** address gate-1/3/4 failures, not `d_g`; they
fold into (a)/(b).

**Elsewhere in the project** (if the Dembélé arm pauses): Lemma B remains the
clean self-contained open problem with a written attack plan
(`writeup/lemma-B-open-problem.md`); the Cunningham–Dembélé descent gap
remains interesting but non-blocking.

## 3. Assets banked by this arc

- The **orbit-degree certification method**: deciding the rational-orbit
  degree over a residual block *without decomposing the newspace* (sparse
  integer + dense mod-2 work only; Deligne-bound balanced-lift certificate).
  Validated at level 31 against exact factorizations; ran at dimension 109 241.
- The **pairing correction** (D31): the Brandt monodromy diagonal is the
  stabilizer orders, not the Eichler masses; two exported intrinsics
  (`InternalHMFRawStabOrdersDefinite`, the mass reader) worth upstreaming.
- Banked, mutually consistent operator/pairing data at level 1, 31, and q0
  (see HANDOFF), plus the validated remote-job pattern.
- Scripts 49b–55; the multimodular `L_g` machinery (52/53) is written and
  API-tested, usable as-is should a future prime pass the `d_g` test.

## 4. Recommendation

Run the **level-31 Tate-parameter pilot** (option (b), question 2 at dimension
1) as the next unit of work; put the scan on as a background lottery only if
chatelet is otherwise idle; treat question 1 as the parallel paper-math task.
Do not build anything further on `d_g = 16` at any prime until a `51` run
certifies it there.
