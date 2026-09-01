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
Lean formalization (project 11dcaed0, `aristotle_fixing/`). **Outcome (2026-08-16):
all three theorems proved — 0 sorries, no new axioms — and Aristotle noted the
Suzuki evenness hypothesis is unnecessary, slightly strengthening the lemma.**

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
mysterious failure, verify the measurement instrument. Final resolution: the
"unkillable survivors" were other tenants' Magma jobs — the shared host exposes
other CoCalc projects' processes in ps, so every unfiltered count was polluted.
All fleet accounting now filters by uid (`ps -u $(id -u)`).

**D19. The fixing congruence is now machine-checked.** (Same event as the
outcome line appended to D14 by a concurrent session in `d50f0c4`; this entry
carries the detail.) The Aristotle project
`aristotle_fixing` (submitted 2026-08-13) returned proved: `FixingCongruence.lean`
contains three theorems — `fixing_congruence_gl` (`p | 2^{2^j}+1 ⟹ 2^{j+1} | p−1`),
`fixing_congruence_sz` (`p | q²+1 ⟹ p ≡ 1 mod 4`), and `twist_fixes`
(`x^{2^m} = 1` and `2^m | p−1 ⟹ x^p = x`) — with no `sorry` and no new axioms
beyond `propext`/`Classical.choice`/`Quot.sound`. All three route through one
helper: if `a^{2^n} = −1` in `ZMod p` then `ord(a) = 2^{n+1}`, so `2^{n+1} | p−1`
by Fermat. Note the reported slack: the Suzuki statement never uses evenness of
`q`; it holds for every natural `q`. Banked in `aristotle_fixing/` alongside its
toolchain pin (`leanprover/lean4:v4.28.0`) and cited in
`writeup/all-2-power-covers.md` §6. This is the second Lean-certified component
of the project after Lemma A. The *transfer* hypothesis ("fixing ⇒ deficient ⇒
ramified") remains empirical — formalization does not touch it.

**D20. Credential outage, and the duplicate-work bug it exposed.** The
chatelet account API key stopped authenticating (`/api/v1/ping`, which takes no
arguments, returned "No account found" under all four auth encodings, while
`/customize` served 200 — so: key revoked or expired, not an outage). The key
was rotated by hand; `remote_magma/set_key.py` now does that rewrite without
echoing the key, and `.env.bak` was added to `.gitignore`, which the bare
`.env` rule did not cover.

The reconnect survey (`remote_magma/reconnect.py`, read-only by design) found
all 8 lanes alive at 19.5 h uptime — the fleet had survived the whole outage —
but every lane had spent that time **recomputing a prime it had already
finished**: 1249, 1279, 1409, 1439, 1471, 1567, 1601, 1663, at 14–20 h each,
≈130 CPU-hours lost. Cause: a restarted lane always resumes at its first
non-`DONE` prime, and `DONE` is a static literal in the script, so results not
hand-harvested are replayed. HANDOFF said "harvest before any rescan edits";
`restore_scan.py` restarts lanes automatically and never harvests, so the
instruction could not hold in practice. **Lesson: a manual step in the recovery
path of an automated restart loop is a bug, not a procedure.**

Fix, in the script rather than the runbook: (a) *self-harvest* — `DONE` is
augmented at startup from every prime recorded in the lane logs, matched on the
full `q over NNN): trace` pattern so a half-written line from a killed process
cannot register a truncated prime; (b) *stable assignment* — lanes are assigned
by position in the FULL sorted prime list before done-filtering, since with the
filter applied first, two lanes restarting with different harvest sets can be
handed the same prime. (b) is backward-compatible: the 24 statically-DONE
primes are exactly the 24 smallest by norm and 24 ≡ 0 mod 8, so the historical
assignment is unchanged — verified by recomputing the ordering independently in
Python and matching all 8 observed lane-to-prime pairs. Results are now banked
in the repo (`dembele/scanjob/scan_results.csv`) instead of living only in
remote `*.out` files, and the lane script itself
(`dembele/scanjob/37_levelraise_lane.m`) is committed — it had existed only on
chatelet, so a project wipe would have made gate 1 unreproducible.

Scan state after harvest: 32 rationals scanned, `const2val = 0` throughout, 0
hits. Cost is 14–20 h per prime and rising with norm.

**D21. The genus-2 corner is precision-blocked, and the instrument says so
honestly.** The 24 h local run produced its dump; no absolute Igusa invariant
admits a certifiable relation of degree ≤ 24. The verdict is *precision*, not
mathematics: the numerical curve carries ~25 correct digits of the 285 it
formally reports. Established three ways — LLL heights growing linearly with
precision at every degree (noise, not a relation); a gauge probe showing the
Igusa formulas themselves preserve 257–274 digits; and the package's own two
outputs of the same curve (pre- and post-`TriangleRescaleCoefficients`, proved
identical up to a weighted gauge by the ratio pattern) agreeing to only 24–26
digits. The loss is upstream, in the power-series → `NumericalKernel` curve
solve; the Arnoldi eigenvector itself converged to 1e-273, and there is no
Newton refinement anywhere in the genus-2 path to recover it. Corollary: the
package's own `MakeK` search at `DegreeBound = 24` was running on the same
~25-digit data and could not have succeeded legitimately — a hit there would
have been spurious. Full argument in
`dembele/certificates/g2-corner-precision.md`.

**Lesson worth keeping:** a recogniser must be able to *fail*. The first
version of `32_g2_field.m` used a fixed height threshold, which neither
rejects a marginal noise fit nor accepts a genuine large-height one; the
precision-ladder test (does the fitted polynomial stop moving as precision
rises?) distinguishes them structurally, and it is what turned "no answer"
into the diagnosis above rather than a plausible wrong field. Also switched to
the low-weight ratios `I4/I2^2, I6/I2^3, I10/I2^5`: same field, but the
classical `I2^5/I10` triple is weight 30 and reaches height 1e22 at degree 12,
beyond certification at any precision this run could offer.

Options recorded, none taken unilaterally: rerun at ~500 digits (~a week,
since the ~260-digit conditioning loss is roughly constant in the working
precision); diagnose the kernel solve (cheaper if the ill-conditioning is a
construction detail); or leave it — this corner verifies an arc already closed
and written up negatively, and is not on the critical path.

**D22. Ops: the fixer caused the fault it was built to prevent.** After the
recycler retired four lanes at once, half the fleet sat idle waiting for the
watchdog's 10-minute sweep, so I ran `restore_scan.py` by hand to bring them
back sooner. The watchdog swept at the same moment; both censused, both saw the
same lanes missing, and both launched them. Lanes 3 and 4 ended up with two
processes each — quietly duplicating a 14-20 h prime, which is precisely the
waste D20's self-harvest was introduced to stop. Duplicates were identified by
the uid-filtered, environ-based census (D18) and the younger process of each
pair killed.

The bug was latent in `restore_scan.py` from the start: census and relaunch are
separate round trips, with no interlock. Impatience only exposed it. Fixed with
a local `flock` plus a re-check of each lane immediately before launching.
**Lesson: an idempotent-looking repair tool that is not actually idempotent is
a loaded gun, and the moment you reach for it manually is exactly when the
automation is also running.** Prefer waiting for the scheduled sweep, or make
the tool safe to run concurrently — we did the latter.

**D23. GATE 1 IS SATISFIED: q0 = the prime above 7 of norm 2401.** On
2026-08-22, after 53 rationals scanned, lane 0 returned
`Nq=2401 (q over 7): trace=0 const2val=8 <== LEVEL-RAISING PRIME` (128 700 s).
Since `v_2(Norm a_q) = 8 v_lambda + 8 v_lambda'`, a valuation of exactly **8**
forces `v_lambda + v_lambda' = 1`: precisely one of the two primes above 2
divides `a_q`, i.e. `abar_q = 0` for exactly one of Dembele's two residual
systems. That the valuation is exactly 8 — the residue degree — rather than
some arbitrary even number is itself a consistency check that a spurious or
buggy verdict would be unlikely to pass. Single occurrence, no conflicting
verdict for q = 7 anywhere in the logs.

**This is what the entire period route was dammed behind.** Every gate from 3
onward was scoped, costed and waiting on it.

**Two pieces of luck worth recording.** (i) The norm is 2401, comfortably inside
the affordable window: gate-4 cost goes as `Nq0^2`, and 2401 sits close to the
2111 used in the cost tables (a 1.29x multiplier — ~157 core-hours at M = 20),
far from the norm-5000 decision point where a hit would have become painful and
20000 where it would have been useless. (ii) It arrived at the 53rd rational
rather than deep in the tail; the cumulative-odds table put ~28% by norm 5000.

**Not yet trusted.** The plan of record deliberately makes gate 3 a
*verification* rather than an assumption: compute the level-`q0` Brandt module
and find the Steinberg eigensystem congruent to `f` mod `lambda`, instead of
relying on mod-2 level-raising theorems. That is now the immediate next action.
Note `q0` has residue degree 4 (`2401 = 7^4`), which is fine for the parity and
CD arguments — they need only *a* finite prime — but means the local field at
`q0` is the unramified quartic extension of `Q_7`.

The scan continues: a second hit at lower norm would be cheaper downstream, and
redundancy matters if gate 3 rejects this `q0`.

**D24. Gate 3: surgery on the pinned HMF package, and why we are verifying
rather than invoking Ribet.** Two forks resolved on 2026-08-22.

*(a) The package could not build the objects.* Level `q0` has dim **109240**
(14 s to compute — the mathematics was never the issue), but `definite.m`
materialises dense `dim x dim` matrices, 45.5 GB apiece here. Two sites, both
patched additively and recorded in `dembele/patches/`: the Hecke assembly, and —
the binding one, since it fires first — `BasisMatrixDefinite`. The finding there
is worth keeping: at parallel weight 2 every per-factor `basis_matrix` is the
**identity** (the package's own `TO DO` calls them removable), so
`basis_matrix_big` *is* the identity, built densely and inverted by a global
`Solution` call. 45.5 GB twice plus an O(n^3) solve, to construct and invert an
identity matrix. Downstream it is read only through `Ncols`/`Nrows`, and its
inverse never at all. Verified by comparing against the pristine package: level 1
for the Hecke hunk (`Matrix(sparse) eq dense`, V16's degree-16 factor unchanged),
and — since level 1 takes the "easy" branch and never reaches the basis-matrix
code — **level 31** for that one, matching on dimension, `Nrows`, trace, and the
sum and sum-of-squares of every entry of `T_97`. At level `q0` the operator now
builds in 963 s with 3 494 618 nonzeros, **31.99 per column** against the
predicted `Norm(p)+1 = 32`. This surgery was required for gate 4 regardless: the
level-`q0` module *is* the Bruhat–Tits tree quotient.

*(b) Verify, or invoke the theorem?* The plan said "verify, don't trust mod-2
level-raising theorems", and on inspection that instinct was right. Level raising
for Hilbert modular forms is general **for `ell > 2`**; `ell = 2` is a separate
and delicate case (there is a dedicated literature on it). Worse, Rajaei's
theorem carries a hypothesis for even `d = [F:Q]` requiring the automorphic
representation to be **special or supercuspidal at some finite prime** — and our
`f` has level 1, so it is unramified at every finite prime. Our configuration
(`ell = 2`, `d = 8` even, level 1) sits exactly in the corner the theorems avoid.
So: **direct verification**, not invocation. *(This reading is from secondary
sources; the primary text should be checked before either conclusion is
published.)* Running: `charpoly(T_31 mod 2)` at level `q0`, testing whether the
residual invariant `g16bar` divides it and with what multiplicity.

*Method lesson, twice earned.* Both of this session's serious mis-estimates were
unmeasured guesses about constants: the overconvergent inner loop (wrong by
1300x, because a distribution action is `O(M^2)` with Python overhead, not the
`O(M)` vector op I timed) and dense `GF(2)` multiplication (wrong by ~15x in the
*pessimistic* direction — Magma is bitsliced, so `n = 109240` costs ~22 min, not
the ~5 h I asserted; that error nearly discarded a viable approach). **Measure
the constant before letting it decide anything.**

**D25. Gate 3 has positive evidence; U_q0 is the first job the durability
chain did not cover; and a self-correction on gate 5.** Three things since D24.

*(a) The congruence shows up, twice.* With the package surgery done, the test is
whether the residual invariant of `rho-bar_f` appears at level `q0` beyond what
oldforms explain. It does, and only on one side. `g16bar` splits into two
*distinct* irreducible degree-8 factors — one per prime above 2 in `H`, i.e. one
per residual system — and against an oldform baseline of 2 each:

| `ell` | one factor | the other |
|---|---|---|
| 31 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |
| 97 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |

The `ell = 97` invariant is a different polynomial tested against a different
operator, so it is a second draw, not a restatement. And the side carrying the
excess is the side gate 1 predicted: `const2val = 8` means
`v_lambda + v_lambda' = 1`, so exactly one system has `abar_q0 = 0`. Three
computations sharing almost no machinery agree. **The baseline is not an
assumption either** — the non-raising system is its own control, sitting at
exactly 2 in both rows.

Not yet established: that the two excesses are the *same* subspace, and
Steinberg. One computation settles both — `dim ker(U_q0 - 1)` on the excess
subspace. Note the naive test is vacuous: oldforms satisfy
`x^2 - a_q0 x + Nq0`, which mod 2 is `(x+1)^2` precisely *because* `a_q0 = 0`
mod `lambda` — the very hit that makes `q0` interesting collapses the obvious
Steinberg check, and the separation has to come from `U - 1` being nilpotent
nonzero on the old part but zero on the new.

*(b) A 40–50 h job cannot run unprotected on this host.* `U_q0` was launched as
a bare `nohup` and chatelet restarted after ~18 h, destroying it. The scan's
chain (`project_init.sh` → supervisor → lanes) came back automatically with
exactly one process per lane and no duplicates — its first real test against a
project restart, passed — but `U_q0` was outside that chain. Observed uptimes
between restarts: ~3 days, ~5 days, then this one. A job needing two days is a
coin flip, and without checkpointing each failure costs everything. Response:
chunk it. `HeckeOperatorDefiniteBig` already takes `Columns`, so the operator
can be assembled in column blocks that are disjoint and simply add; each block
is banked, so a restart costs one block. **Lesson: durability is a property of
the *job*, not of the host — and "it survives session close" is not the same as
"it survives the host".**

*(c) I was wrong that gate 5 was under-specified.* I claimed reaching a global
polynomial from q0-adic periods had no stated mechanism and would need a model
of a 16-dimensional abelian variety. `csv-paper-adaptation.md` states the
mechanism: the **257 λ-isogeny neighbours are the 257 points of `P^1(F_256)`**,
Galois permutes them, and a separating invariant evaluated at each gives the
degree-257 polynomial. No model is needed — only separation. The narrower real
gap is that the Eisenstein prototype is archimedean while the route is q0-adic;
but for a Mumford-uniformized variety the periods are topologically nilpotent,
so the same q-expansion converges with `q^nu` replacing
`exp(2 pi i Tr(nu z))`, as on a Tate curve. Enumeration and divisor sums carry
over; only evaluation and cutoff change. What genuinely remains unverified:
whether the invariant separates 257 neighbours at genus 16 (17 at genus 4 is
all that is tested), and the q0-adic term count, which depends on period
valuations. Detail: `dembele/certificates/gate5-padic-eisenstein.md`.

**D26. Gate 3 is verified to the eigensystem level, and the audit that got it
there.** On request I re-audited the chain step by step
(`dembele/certificates/gate3-method-audit.md`) rather than trusting it, and two
of the seven links turned out to be load-bearing assumptions I had never checked.

*(a) The oldform baseline — the one that could have voided everything.* The
excess argument reads "multiplicity 4 at `q0`, baseline 2, excess 2". But the
baseline is `2*m1`, where `m1` is the multiplicity of the residual factor at
**level 1** — each level-1 form with that residual system contributes two
oldforms. I had assumed `m1 = 1` without checking, and at `m1 = 2` the baseline
would be 4, the excess zero, and the `ell = 97` "corroboration" would have been
the same error twice. **Verified:** against the *full* level-1 charpoly mod 2
(degree 58, not just `V16`), both degree-8 factors occur with multiplicity
exactly 1. Baseline 2 confirmed; the excess is real.

*(b) Banked operators from different sessions are incomparable.* The eigensystem
test failed with `Solution: No solution exists` — `T_97` did not preserve
`ker f1(T_31)`, impossible for commuting operators. Direct check: the banked
pair failed to commute on 5 of 5 random vectors. They had been built in separate
Magma sessions, and the package's internal ordering (ideal-class reps, unit
generators, `P^1` enumeration) is not reproducible across sessions. Crucially
this does **not** touch the multiplicity results — characteristic polynomials
are basis-independent — but it invalidates any *joint* analysis. The alternative
explanation, that the sparse patch was simply wrong at level `q0`, had to be
excluded rather than assumed: rebuilding both in one session gave
`COMMUTE = true` (0 failures of 8), which also became **the strongest validation
the patch has had at level `q0`**, where previously only the
nonzeros-per-column shape check applied. **Rule: never combine banked operators
from different sessions.**

*(c) The eigensystem evidence itself.* `W = ker f(T_31)` at level `q0` is
16-dimensional, and `charpoly(T_97|W)` is a *single* degree-8 irreducible
squared, matching a factor of the independently computed level-1 `a_97`
invariant — a two-prime eigensystem match on the actual subspace, which the
multiplicity method could not reach (audit step 7).

*(d) A third signature, unlooked for.* The kernel dimensions give the Jordan
structure over the residue field. `f1`: primary dimension 32, `dim ker = 16`,
so blocks of **size 2** — non-semisimple. `f2`: primary dimension 16,
`dim ker = 16` — semisimple. Congruence between an oldform and a newform
produces exactly that non-split gluing, and it appears **only** on the factor
carrying the excess. Three independent observations now agree: the gate-1
valuation, the multiplicity excess at two primes, and the Jordan structure.

Running at session close: a four-prime test (31, 97, 127, 191) in one session,
computing each kernel once and restricting every operator to it, and printing
*which* level-1 factor matches so the correspondence is checked rather than
assumed.

**D27. Three forks on 2026-08-26: the scan is wound down, the four-prime job
was vacuous and is replaced, and the Eisenstein back end has a computable
go/no-go.** Resumed from handoff; every item below is recorded before its
outcome is known.

*(a) Scan: `STOP_SUPERVISOR` set, fresh lane 0 retired.* The host had 0 GB
available (7 lanes at 14–17 GB each, plus a just-relaunched lane 0 about to
grow into the same 16 GB the gate-3 job needs). The handoff itself recommended
winding down to 2–3 lanes: `q0` is banked, the primes now cost ~2 days each
(norms ≈ 3000), and further hits are redundancy. Chosen: stop relaunches
(`touch two_scanjob2/STOP_SUPERVISOR`), kill only the 52-minute-old lane 0,
let the seven in-flight lanes finish their primes and exit. Not chosen: killing
in-flight lanes (43 h of work each), or editing `NLANES` while lanes with
`NLANES=8` are mid-prime (the position-mod-`NLANES` assignment would double-
assign their primes). **To resume at 3 lanes** once the fleet has drained: set
`NLANES=3` and the loop `for L in 0 1 2` in `two_scanjob2/supervise.sh`,
mirror it in `remote_magma/restore_scan.py`, remove the STOP file, relaunch the
supervisor with the command in its header. Doing that before the lanes drain
duplicates work.

*(b) `47_gate3_multiprime.m` retired; `48_gate3_genkernel.m` launched.* While
writing the closure argument I found that the eigenspace `W = ker f1(T_31)`
used for the step-7 "eigensystem match" is, under Ihara's lemma, exactly the
mod-2 old subspace: `O` (two copies of the level-1 `f1`-part, `T_31`
semisimple on it) sits inside `W`, and both are 16-dimensional. Restricting
`T_ell` to `W` then re-derives level-1 data by construction; the running
four-prime job could not have distinguished "new forms congruent to `f`" from
"not". Full argument in `gate3-method-audit.md` (2026-08-26 section). The
replacement restricts to the 32-dimensional generalised eigenspace
`G = ker f1(T_31)^2` and tests `charpoly(T_ell | G) = (f1^{(ell)})^4`, which is
equivalent to the **new quotient** carrying `f`'s system at `ell` because the
old contribution `(f1^{(ell)})^2` is forced by local theory (two Iwahori-fixed
vectors per unramified principal series). No degeneracy maps are built — the
second one needs `get_tps` at `q0`, the `U_q0` cost. Extra cost over 47: one
dense `GF(2)` multiply and one kernel. The banked, basis-independent level-`q0`
characteristic polynomial selects the excess factor so the non-raising side
(old forms only) is skipped. The script's level-1 phase was validated locally
at level 31 and its tail on a synthetic commuting pair with the expected
Jordan structure (`[4, 2]` multiplicities, quotient `= level-1^2`). Killing 47
cost 3.3 h of sunk compute; its four operator builds could not be reused (they
die with the session) and its output was uninterpretable.

*(c) Gate 5: term count quantified; gate-4 build blocked on one determinant.*
`gate5-genus16-term-count.md`. The Fourier-term count obeys
`sqrt(D)·C^n/(n!·N(y))`, validated on all three genus-4 counts to 0.3%. At
genus 16, with the integrality of the q0-adic valuation pairing, it is bounded
by `1.1·10^4 · M^16 / Δ'`, `Δ'` = determinant of the period-valuation pairing
relative to unimodular. Feasibility needs `Δ' ≳ 10^20–10^30`, i.e. period
valuations of tens, and large valuations raise the recognition precision `M`
which gate 4 pays for quadratically. `Δ'` is computable now from the level-`q0`
character group (monodromy pairing on the `g`-isotypic part) — the right next
computation and the one that can invalidate the gate-4 build. The handoff's
item 3 (an archimedean "separation test" at genus 16) is not the binding
question and is not being run. Side finding: `ζ_H(−3) ≈ 10^{87.7}` makes the
constant-term-1 `E_4` equal to `1 + O(10^{−13})` on the whole fundamental
domain — a scale artefact of the discriminant, removable by rescaling but
requiring `ζ_H(−3)` exactly; irrelevant q0-adically.

*Operational.* `Bash run_in_background` here kills its process after ~2 h; the
local smoke test died at the level-31 phase and was relaunched with
`nohup … & disown` (macOS has no `setsid`). The first chatelet launch of 48
through `cocalc.py exec` died silently after ~15 min: CoCalc applies the
`project_exec` timeout to the command tree as `RLIMIT_CPU` (default 120
CPU-seconds), and `setsid`/`nohup` do not shed an rlimit. Relaunched via
`rexec(..., timeout=86400*3, sock_timeout=60)` — the pattern `CHATELET.md`
and `restore_scan.py` already prescribe. Lesson re-learned: a detached launch
must go through `rexec` with an explicit CPU limit, never through a plain
`exec`. Attempt 2 then ran 11 h, built all four level-`q0` operators
(**commuting pairwise, 0 failures of 27 checks** — the sparse patch validated
at four primes in one session), evaluated `f1(T_31)` (3938 s) and squared it
(585 s), and died at its own 16 GB cap on the kernel: four dense `GF(2)`
operators at 1.5 GB each plus two dense polynomials plus the kernel workspace.
The cap was inherited from 47 without re-measuring — the D24 lesson again.
Attempt 3 (2026-08-27 03:xxZ) keeps the operators sparse (dense only for the
polynomial evaluation), prints memory at each checkpoint, runs under a 40 GB
cap (47 GB free after four lanes exited), and **banks the four integer sparse
operators** (`two_gate3/gk_s3_T{31,97,127,191}.m`, ~120 MB each) — a
commuting set in one basis, which the `Δ'` computation over `Z` will need.

**D28. GATE 3 IS CLOSED: the level-`q0` new quotient carries `f`'s residual
system at 31, 97, 127 and 191.** `48_gate3_genkernel.m`, attempt 3, finished
2026-08-27 10:26Z (`dembele/data/computed/gate3_genkernel_q0.out`,
`gate3-closure.md`). On the 32-dimensional generalised eigenspace
`G = ker f1(T_31)^2` every one of the four commuting operators has
characteristic polynomial `(f1^{(ell)})^4`; the old part accounts for
`(f1^{(ell)})^2` by local theory, so the new quotient has `f`'s system at all
four primes, with the pairing of the four polynomials fixed by the single
prime `lambda` on the `f` side. `T_31` has Jordan blocks of size 2 on `G`
(rank 16), semisimple on the old part — now a corollary of the congruence, not
a signature (D27b). Steinberg at `q0` follows from newness at prime level with
trivial character. Not proved and not needed: `rho-bar_g = rho-bar_f` itself
(no affordable Sturm bound; a Galois-conjugate system cuts out the same field;
the gate-5 certification is the backstop).

*Decision:* the Hecke side of the route is done; no more primes will be added
(each costs a full same-session rebuild, ~5 h, for evidence that cannot become
a proof this way). The four integer operators are banked from this session
(`two_gate3/gk_s3_T*.m`, commuting, one basis) as the input for the next
computation, `Delta'` (D27c), which is now the binding question of the whole
route. The scan stays stopped: `q0` is confirmed level-raising in the strongest
sense a finite computation gives, so redundancy has little value; resume at
three lanes only if a *second* `q0` is wanted for downstream reasons (e.g. a
smaller norm for gate 4).

*Method note.* Two of the three "independent signatures" of D26 turned out to
be one signature (the multiplicity excess) plus one vacuous test plus one
ambiguous one; the version that actually decides the question needed a
quotient, not a subspace, and it needed no new mathematics — only asking
what output the test would produce if the claim were false.

**D29. `Δ'` is computed as the mass-Gram of the `g`-sublattice, not a graph
kernel — the character group needs no boundary map.** With gate 3 closed, the
binding question is `Δ'` (`gate5-genus16-term-count.md`). The certificate
framed it as a monodromy pairing on `X = ker(∂: Z[edges] → Z[vertices])` and
flagged the integral kernel of `∂` on the 109240-dim space as the obstacle.
That obstacle is illusory: `g` is **new** at `q0`, so it lies in the kernel of
both degeneracy maps to level 1, i.e. `∂ = 0` on the whole `g`-part. Hence the
`g`-isotypic part of the raw Brandt lattice already *is* its character lattice,
and the monodromy pairing is the diagonal Brandt mass pairing
(`InnerProductMatrixBig`, verified diagonal at parallel weight 2,
`definite.m:748`) restricted to it. `Δ'` is therefore
`det(B W Bᵀ)/(N(𝓛)²·D_H)` for a saturated `Z`-basis `B` of the `g`-sublattice
and mass vector `W` — no graph, no `get_tps`, no boundary operator. Plan in
`gate5-delta-prime-plan.md`; the raw operators we banked (`gk_s3_T*.m`) and the
mass vector share a basis, so they compose directly.

*Package change (recorded as a patch, D-worthy because results depend on it):*
the mass pairing was not reachable from outside the package —
`InnerProductMatrixBig` is internal and the cuspidal `InnerProductMatrix`
errors "Not implemented" on these spaces. Added a two-line additive intrinsic
`InternalHMFRawInnerProductDefinite` (+ a `forward` declaration),
`dembele/patches/hmf-raw-innerproduct.patch`, applied locally, **not yet on
chatelet**. First fact it produced: at level 31 the masses are `{1,3}`, not all
equal — some ideal class has an order-3 unit stabiliser — so `W` is genuinely
non-scalar and the pairing cannot be replaced by the standard dot product.

*Status:* the pipeline prototype `49_delta_prime_proto.m` (validate over `Q` at
a small level: self-adjointness of `T` under `W`, new ⊥ old, saturation, the
sub/quotient Gram determinants) is **running at level 31** (`~/dp31_proto.out`),
not yet verified — the level-31 raw operator builds are ~1 h each, so it is
slow for a prototype. Once it passes, the `q0` computation is multimodular:
`det(Γ) mod p` for ~20–50 primes, CRT'd — parallel, ~1–2 core-days, no
host-scale job. Sub vs quotient determinant and the polarisation factor remain
the real ambiguity (`gate5-genus16-term-count.md` §; both reported).

**D30 (2026-08-31). The q0 `Δ'` run identifies `h_g` 2-adically and builds
`L_g` by Wiedemann projection — per-prime full charpolys are rejected; and
`d_g` (16 vs 32) is promoted to the first output.** The D29 plan's step 2 left
"take the `g`-factor `h_p`" unspecified. Costing the naive reading killed it:
a dense mod-`p` charpoly at `N = 109240` over an odd word-size prime is
47–95 GB (no bit-packing) and ~a day per prime — unaffordable for 20–50
primes. *Decision:* (a) recognize the global factor `h_g` from the 2-adic side,
where everything is mod-2 dense (bit-packed, cheap) or 32×32: Hensel-lift the
gate-3 block `ker f1(T_31)²` to `Z/2^192`, take the block charpoly, divide out
the exact level-1 old part `u1²`, and balanced-lift under the Deligne
coefficient bound (`|a_31| ≤ 2√31` ⇒ deg-16 coefficients `< 2^70 ≪ 2^192`);
(b) per word-size prime, get `μ mod p` by Wiedemann (sparse matvecs only),
verify `h_g | μ`, and span `L_g ⊗ F_p` by `(μ/h_g)(T_31)·v` projections —
valid because `W ≻ 0` and `W`-self-adjointness force `μ` squarefree; CRT the
canonical echelon bases, saturate, `Γ = B W Bᵀ` exact. *Alternative rejected:*
computing `charpoly(T_31) mod p` per prime and guessing the factor by degree —
memory-infeasible and the factor is not identifiable mod odd `p` anyway.
*Promoted question:* gate 3's residual multiplicity on the new part is 2
(vs 1 at level 1), so the char-0 orbit could be a single degree-32 orbit; then
`dim B_g = 32` and gate 4's term count is `M^32/Δ'` — a probable no-go. `d_g`
is therefore the run's first deliverable, before `Δ'`. Full mechanics in
`gate5-delta-prime-plan.md` (Addendum 2026-08-31); step-1 script
`dembele/magma/50_delta_prime_q0_W.m` (rebuild `W` + `T_31`, assert equality
with banked `gk_s3_T31` before trusting the pairing).

**D31 (2026-08-31). The monodromy pairing diagonal is the STABILIZER ORDERS
`e_i`, not the Eichler masses — D29's identification of `W` was off by a
reciprocal.** The q0 self-adjointness check (`50_delta_prime_q0_W.m`) failed:
with the Eichler-mass diagonal of `InternalHMFRawInnerProductDefinite`
(`m_i = (ulcm/g)/e_i`, the package's `InnerProductMatrixBig` weights),
`W_i T_ij = W_j T_ji` fails on 304/1197 support entries already at level 1.
Deriving the unique consistent diagonal directly from `T_31`'s entry ratios
along the support graph (connected; zero cycle inconsistencies) gives exactly
the reciprocal pattern: `W'_i · m_i = ulcm/g` for every `i` — i.e. `W' = e_i`,
the stabilizer orders, which is the classical Brandt relation
`e_j T_ij = e_i T_ji` and the Cerednik–Drinfeld monodromy edge lengths
(Gross/Ribet), as it should have been from the start. *Fixes:* new intrinsic
`InternalHMFRawStabOrdersDefinite` (returns `e_i`, `ulcm`, `g`; patch file
revised); since `m_i e_i = ulcm/g` is **basis-independent**, the banked q0
mass vector converts offline — `54_delta_prime_q0_wfix.m` read `C = 48` at q0
(`ulcm 96, g 2`; `e_i ∈ {1,2,3,4,8,16}`) and verified the converted diagonal
is self-adjoint for the banked `dp_T31` on **all 3 494 618** support entries;
`dp_Wtrue.m` banked in the `dp_T31` basis. The level-31 prototype was
relaunched (chatelet) with the corrected pairing. *Unaffected:* `h_g`/`d_g`
(51) and the `L_g` construction (52) are pairing-independent; only the Gram
step uses `W`. *Also learned:* the raw basis is confirmed session-dependent
(rebuilt `T_31` ≠ `gk_s3_T31`), so the authoritative Δ' inputs are the
same-session trio `dp_T31.m` + `dp_W.m` + `dp_Wtrue.m` on chatelet;
`gk_s3_T97/127/191` cannot be paired with them. And
`InternalHMFRawInnerProductDefinite` originally went through
`InnerProductMatrixBig`, whose `return Matrix(...)` densifies the diagonal —
95 GB at q0, which killed the first run of 50; the intrinsic now computes the
masses directly (patch revised; regression: level-31 masses unchanged).

**D32 (2026-09-01). GATE 5 ANSWERS NO-GO: `d_g > 16` at q0 — the residual
system has no rational 16-dimensional isotypic piece, so the gate-4 genus-16
construction is unavailable at this auxiliary prime.** The q0 run of
`51_delta_prime_q0_hg.m` (banked `dp_T31`, precision `2^192`) lifted both
residual blocks T-stably with every internal check exact: the `f1` block
(dim 32) has `cp_m = u1² · h'` with zero remainder and `deg h' = 16`; the
`f2` block (dim 16) is purely old (`cp_m = u2²`, new-part degree 0), exactly
as gate 1 predicted. Over `Z_2`, `h'` splits into TWO irreducible degree-8
pieces (matching residual multiplicity 2). The Deligne coefficient bound
(`|a_31| ≤ 2√31`; a degree-d global factor balanced-lifts under
`C(d,d/2)·12^d`) rejects **all** sub-products: `h'` itself and each degree-8
piece lift to coefficients ~`2^190` against bounds `2^71`/`2^35`
(`55_subproduct_f1block.m`, 0 of 3 pass). Hence every global Hecke orbit
meeting the `f1`-side new block has degree > 16 — its other 2-adic pieces lie
over residual factors other than `f1` and `f2` — so `dim B_g > 16` (compare:
already at level 31 the new orbits have degrees 656/684), the
`gate5-genus16-term-count` premise `genus = 16` fails, and the term count
`~M^{d_g}` is out of reach for any plausible `Δ'`. Moreover the `f1`-new
lattice is only `Z_2`-rational, so the `Δ'`-as-integer framing (D27c/D29/D30)
loses its object: scripts 52/53 are moot at this prime. *Evidence:*
`dembele/data/computed/dp_hg_q0.out`, `dp_hg_f1_block.m` (the lifted 32×32
block action). *What remains open:* `d_g` is a property of the CHOSEN q0; the
options are (a) resume the gate-1 scan for a different auxiliary prime and
re-run 51 there (the whole pipeline is now banked + validated; marginal cost
per candidate ≈ one 51 run, ~8 h), (b) rework gate 4 to use only the
16-dimensional 2-adic toric data rather than the global abelian variety —
a genuine research question, (c) the contingencies of
`levelraise-cd-plan.md`. The route is NOT killed; this q0 is.

---

*Maintenance note: append an entry per significant fork — the decision, the
alternatives, the reason, and (when known) the outcome. Commit refs and script
numbers make entries checkable against the repository history.*
