# Decision log

A running record of the choices made in the hunt for an explicit polynomial for
Dembélé's nonsolvable field ramified only at 2 — what was considered, what was
chosen, why, and how it turned out. Maintained so that if this project succeeds
(or closes), the path is reconstructible. Results live in `writeup/` and
`dembele/certificates/`; this file records the *forks*.

For the pre-2026-08-11 history (the 2-group Belyi arc → Lemma A/B; the Brandt/HMF
reproduction of Dembélé's computation; the killed constructive routes), see
`writeup/main-result.md`, `HANDOFF.md`, and `dembele/certificates/idea-exhaustion.md`.

---

## 2026-08-11

**D1. Take the M23 paper seriously as a signpost.** Trigger: arXiv:2608.08538
(engine = the KMSV/BelyiDB machinery). Options: dismiss (rigidity controls groups,
not ramification) or investigate whether the method's shape transfers. Chose to
run the M23 "step 1" (Nielsen census) on the Dembélé group's almost-simple
quotient PΓL₂(256). Rationale: cheap (character theory), and the HMF route was at
a hard stop. Outcome: found the all-2-power triple phenomenon — the single
structural discovery the whole arc grew from.

**D2. Pilot at k=4 before attempting k=8.** Options: attack PΓL₂(256) directly
(genus 28+, unknown feasibility) or calibrate on PΓL₂(16) (genus 0, M23-easier).
Chose k=4, explicitly as a *negative control*: the k=4 target field doesn't exist
(LMFDB/HMF sweep), so the pilot's guaranteed failure would reveal the obstruction
mechanism. This framing ("where does the guaranteed failure materialize?") drove
everything after.

## 2026-08-11/12 — the pilot

**D3. Precision vs coordinates.** The Belyi package's recognition failed at every
precision (115 → 500 digits; certified relation finder confirmed "insufficient").
First response (wrong): raise precision — the same reflex Zhang's note records the
AI systems having in the M23 project. The user supplied Zhang's account; pivoted
to Galois-equivariant coordinates (canonical points → 0, 1, ∞) and recognition of
Newton *factors* instead of expanded polynomials. Outcome: instant success at
existing precision. Lesson institutionalized: gauge first, digits second; detect
spurious LLL fits by noise-floor height + precision-instability.

**D4. Trust but verify the numerics: certificates over faith.** Every exact cover
was required to pass (i) the exact passport identity over its field and (ii) a
rigorous `GaloisGroup` monodromy certificate. Cost: hours. Benefit: the k=4
conclusions are unconditional, which mattered later when the whole negative arc
leaned on them.

**D5. Compute the local mechanism rather than accept "bad primes = {2,5,17}".**
Options: record the disc and move on, or do place-by-place reduction analysis.
Chose the latter; found the mixed ordinary/supersingular structure and that ≥ 2
conjugate covers are good at every odd prime — relocating the obstruction from
geometry to the moduli field. This reframing produced the decisive question for
everything downstream ("is the k=8 moduli field only-2-ramified?").

## 2026-08-12 — probing the family

**D6. The twist probe instead of a k=8 computation.** To predict k=8 without the
genus-28 computation: sought a group-theoretic marker separating the ramified
primes {5,17} from the unramified {3} at k=4. Rejected en route: char-p Gröbner
counting of covers (the profile doesn't isolate the monodromy group at degree
≥ 17 — recorded as a dead end). Found: the Frobenius-twist fixing criterion,
with the (later proved) congruence that +1-torus primes always fix. Honestly
labeled the inductive step ("fixing ⇒ deficiency ⇒ ramification") a *transfer
hypothesis*, n=1-group calibration.

**D7. Search breadth before depth.** With rigidity "predicted dead," options were
(a) accept and pivot entirely, or (b) run cheap breadth searches for escape
hatches before closing. User chose (b): braid-orbit census (r=4), Suzuki census.
Outcome: Suzuki closed by the same congruence (now proved for q²+1); the braid
census found genuinely short orbits — the escape hatch candidates.

**D8. Boundary maps as the cheap oracle.** To determine the short components'
fields, options: compute a family explicitly (heavy) or exploit degeneration to
already-computed triples (cheap, convention-risk). Chose boundary maps; the
(4,4,8,8) components landed bijectively on the golden triples (inheriting K), and
the (8@φ)⁴ components on the *uncomputed* genus-1 passport — concentrating
everything in one new computation instead of many.

**D9. Genus-1 verdict via j-invariant, not package recognition.** The package's
genus-1 recognition crashed (bug found, patched: TrialDivision guard + dump
hooks). Rather than debug the full pipeline, recognized the gauge-invariant j
from dumped Newton data. Outcome: degree-8 minpoly, field ≅ K — the k=4 closure.
Same philosophy as D3: choose the invariant, not the coordinates.

## 2026-08-13 — the pivot and the period route

**D10. Declare the covers arc closed and write it up.** With k=4 closed and the
family conditionally closed, options: push k=8 numerics anyway, or bank the
result and pivot. User asked for the step-back; chose to write
`writeup/all-2-power-covers.md` (the sequel to the thesis's negative result) and
pivot to the period route. k=8 left as a *falsification target*, not a project.

**D11. Reopen the audit's one unkilled door: level-raising + CD.** Re-read
`idea-exhaustion.md`; the entry "Level-raising + CD at an auxiliary prime —
speculative" was the only non-dead constructive route. Computed the archimedean
feasibility first: ζ_F(−1) = 5820 ⇒ Shimura-curve genus ≥ 91(Nq₀−1)/2 — dead.
Recognized that Cerednik–Drinfeld (the "CD" in the audit's own label) converts
the problem to q₀-adic periods computed from Dembélé's *definite* algebra — the
Greenberg–Voight method, previously killed only because level 1 has no finite
disc prime. Level-raising manufactures the prime. Plan of record:
`dembele/certificates/levelraise-cd-plan.md`.

**D12. Gate the route; scan first.** Ordered the gates by cost: (1) find q₀ with
ā_{q₀} = 0 (scan), (3) verify the congruence at level q₀ directly (don't trust
mod-2 level-raising theorems), (4) CD/GV implementation (de-risk via
`darmonpoints` on a small case). Launched the scan on chatelet after measuring
local cost (950 s/prime — never scan locally).

**D13. The conjugate-grouping correction.** User challenged the Chebotarev
heuristics ("asymptotic — could take a while"). Re-examination found worse: V16
is Gal(F/Q)-stable, so the 8 primes above a rational prime share one parity
verdict — the sample size was 8× overstated (and the v1 scan wasted 8× compute).
Deployed scan v2 (one prime per rational prime, norm ≤ 20000, ~280 independent
samples, ~2/3 heuristic odds; honestly noted that effective Chebotarev is vacuous
at this conductor). Lesson: user-side skepticism of statistical claims pays.

## 2026-08-13/14 — adversarial audit and parallel probes

**D14. Adversarial self-audit of the covers arc.** On user request, ranked the
weak links: transfer hypothesis > boundary-map convention > weight overclaims >
genus-1 "=" vs "⊇" > completeness. Fixed the writeup (weights → certified
bounds; ⊇; k=2 rung). Two items resolved by *argument*: completeness/transitivity
certified by the degree-8 coefficient; the boundary convention forced by the
generating-vs-subgroup dichotomy (exactly one merge ordering gives generating
triples, and it is bijective). Submitted the fixing congruence to Aristotle for
Lean formalization (project 11dcaed0, `aristotle_fixing/`).

**D15. Probe everything cheap in parallel while the scan runs.** User chose
breadth: Sz(8) covers (independent-family hypothesis test), the k=4 genus-2
corner (universality test; also decides the twelve [10,10,11,11] components via
their cusps — found cusp-bijective by capped-BFS sampling after the full-closure
approach was killed by a 1.5M-element orbit), exact k=8 Nielsen counts
(Ni_gen = 32 for (2,8,16), 200 for (2,8,8); forced layers Q(ζ₈) and Q(√2)).
Operational lessons accumulated: chatelet detached-nohup for everything heavy;
memory pressure kills the biggest local jobs; the recognition/optimization layer
(not numerics) is always the failure point — genus-2 stalled in Polredbestabs on
degree-24 junk-gauge fields (response: hyperelliptic dump hook + offline Igusa
plan), Sz(8) needed a precision sweet spot (40 too low for the hyperelliptic
rank test, 115 too high for memory; trying 70).

**D16. Diagnose "try higher precision" as a bug, not a precision problem.** The
Sz(8) hyperelliptic test failed identically at 40 and 70 digits ("multiple
relations"). Precision-independence of a numerical failure ⇒ structural cause:
found the relation-matrix column count hard-coded (`+15` hack, flagged TODO in
the package source) — sufficient at genus ≤ 4, under-determined at genus 8, so
the kernel keeps noise vectors at any precision. Patched to scale with genus
(fourth upstream-worthy `~/Belyi` patch: TrialDivision guard, two dump hooks,
column count). Meta-lesson, same family as D3: when raising precision doesn't
change the failure, the failure is not about precision.

**D17. Park the Sz(8) probe.** The widened matrix (D16) did not fix the
hyperelliptic test: the kernel is genuinely multi-dimensional — the package's
automatic coordinate choice (ratios of the first basis forms) degenerates on
this curve, independent of precision. Fixing coordinate selection is a rabbit
hole; the right tool for a genus-8 (likely non-hyperelliptic) curve is the
vBCPS26 canonical-embedding method — a proper mini-project. Parked with blocker
documented; the independent-family hypothesis test is deferred, not abandoned.
The genus-2 corner (imminent) carries the audit's validation weight meanwhile.

**D18. Ops incident: fleet deaths, real and imagined.** The chatelet project
restarted (twice), killing all detached jobs — real. The subsequent "instant
deaths" of relaunched jobs were **not** real: the verification pattern
`pgrep -f "magma -b"` never matched the actual process (`magma.exe -b` after
the wrapper exec), so healthy fleets read as dead, triggering an escalating
false diagnosis (session reaping? memory kills? — sentinel and memory-hog
probes both came back clean, which was the tell). Resolutions: (a) scan
progress is checkpointed via the DONE skip-set, so restarts lose little;
(b) staggered relaunches (30 s gaps) — the one bulk 11-job relaunch died,
plausibly a startup stampede; (c) liveness monitoring on *verified* process
patterns, since a dead fleet writes nothing and looks identical to a quiet
one. Meta-lesson, the operational cousin of D16: before theorizing about a
mysterious failure, verify the measurement instrument.

---

*Maintenance note: append an entry per significant fork — the decision, the
alternatives, the reason, and (when known) the outcome. Commit refs and script
numbers make entries checkable against the repository history.*
