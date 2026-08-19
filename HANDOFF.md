# Session handoff

## SESSION CLOSE 2026-08-17/18 — read this first

Full narrative: `DECISIONS.md` (D1–D22). Attributions: `REFERENCES.md`.
Plan of record: `dembele/certificates/levelraise-cd-plan.md`, now materially
revised by this session's measurements — read
`dembele/certificates/roadmap-reevaluation.md` **before** deciding what to do next.

### The scan now survives session close (2026-08-18)

A **remote supervisor runs on chatelet** and keeps the 8 lanes alive without any
local session: `dembele/scanjob/supervise.sh`, deployed to
`two_scanjob2/supervise.sh`, running under `flock` so a second launch is a no-op.

```sh
# stop it
python3 remote_magma/cocalc.py exec "touch two_scanjob2/STOP_SUPERVISOR"
# start it (safe to repeat; flock makes a duplicate launch a no-op)
python3 remote_magma/cocalc.py exec "rm -f two_scanjob2/STOP_SUPERVISOR; \
  setsid nohup flock -n \$HOME/two_scanjob2/.sup.lock \
  sh \$HOME/two_scanjob2/supervise.sh \
  >> \$HOME/two_remote_magma/supervisor.log 2>&1 < /dev/null & echo ok"
```

**Why this was needed, and the regression it fixes.** One-prime-per-process
(D20) bounded memory but made the fleet *depend* on something relaunching it.
That something was a watchdog living in the local Claude session — and monitors
die when the session closes, so the fleet would have drained to zero within one
prime-time (14–20 h) of the session ending. The earlier version of this handoff
said "re-arm the watchdog first" without noticing that the scan could not
survive a closed session at all. It can now.

**Project restarts are covered too (2026-08-19).** CoCalc runs `~/project_init.sh`
at project start; ours (`dembele/scanjob/project_init.sh`) relaunches the
supervisor, honours the STOP sentinel, and exits 0 (CoCalc's Supervisor
re-runs the script on any exit code other than 0 or 2). So the chain is now:

| failure | covered by |
|---|---|
| a lane finishes its prime and exits | remote supervisor |
| the Claude session closes | remote supervisor |
| the project/host restarts | `~/project_init.sh` |
| the supervisor itself dies | local watchdog, when a session is open |

All three launchers take the same `flock`, so running any of them alongside the
others is a no-op rather than a double-launch. Arming the local watchdog while a
session is open is still worthwhile as the last layer:

```sh
cd /Users/musty/two
while true; do out=$(python3 remote_magma/restore_scan.py 2>&1); \
  [ -n "$out" ] && echo "[watchdog] $(date -u +%H:%MZ) $out"; sleep 600; done
```

`restore_scan.py` takes a `flock` and re-checks each lane before launching (D22),
so it is safe to run alongside the remote supervisor — but prefer letting them
work rather than hand-running either.

### State of the tracks

1. **Covers/rigidity arc: CLOSED and written up.** Unchanged, except the last
   open corner is now *closed as unanswerable at this precision*: the genus-2
   run finished, and its numerical curve carries only ~25 correct digits of the
   285 it reports (three independent confirmations, D21,
   `dembele/certificates/g2-corner-precision.md`). The package's own `MakeK`
   also failed rather than inventing a field. Deciding it needs a ~500-digit
   rerun (~a week); it verifies an already-negative arc and is **not** on the
   critical path. `32_g2_field.m` is a validated instrument waiting for a
   better dump.
2. **Period route: still the sole live path, and now fully costed.** Gate 1
   scanning (below). Gates 3–5 were scoped end-to-end this session; see
   "What changed" below — the headline is that the route is **feasible** but
   needs an inner-loop rewrite.
3. **Aristotle fixing congruence: DONE.** Proved, banked in `aristotle_fixing/`,
   cited in `writeup/all-2-power-covers.md` §6, logged D19. Second
   Lean-certified component after Lemma A.
4. **Sz(8) hypothesis test: PARKED** (D17), unchanged.

### Running computation and its care

**Eight chatelet lanes** (`dembele/scanjob/37_levelraise_lane.m`, now committed
— it previously existed only on chatelet). Three properties added this session,
all load-bearing:

- **self-harvesting DONE set** — a restarted lane reads the lane logs and skips
  every prime already recorded, so a restart costs only in-flight work (D20);
- **restart-stable lane assignment** — lanes are assigned by position in the
  full prime list before done-filtering, so assignments do not shift as the
  harvest grows;
- **one prime per process** — each lane exits after one prime and the watchdog
  relaunches it fresh, bounding memory (D20 note). Overhead ~12 min startup
  against a 14–20 h prime.

This was exercised for real on 2026-08-17: the project restarted and killed all
8 lanes; the watchdog restored them; every lane harvested all 37 completed
primes and lost nothing but in-flight work. Before this session the same event
would have silently replayed ~200 CPU-hours.

Scan state: **37 rationals scanned, `const2val = 0` throughout, 0 hits.**
Results banked in `dembele/scanjob/scan_results.csv` (they previously lived
only in remote `*.out` files). Cost 14–20 h per prime and rising with norm.

### What changed in the plan (read before resuming)

- **Gate-4 cost goes as `Nq0^2 * M^3`**, so a hit's usefulness decays
  quadratically in its norm. The headline "≈2/3 odds" counts hits we may not be
  able to exploit; treat **norm ~5000 as a decision point** rather than grinding
  to 20000 (`roadmap-reevaluation.md`).
- **The degree-16 Hecke field is a non-issue.** The isotypic component is
  `Q`-rational and the lift is `Q_q0`-linear, so it never meets `H`; `U_q0 = ±1`
  is a scalar on the whole component (verified three ways, including on the
  exact GM example). `H (x) Q_q0` enters only at period assembly.
  (`gate4-lift-scoping.md`.)
- **`darmonpoints` cannot serve as a reference implementation.** Its period path
  has bit-rotted under Sage 10.6 — four version-drift bugs, each deeper;
  abandoned deliberately rather than risk silently wrong periods. The
  overconvergent *lift* does work and is timed. (`gate4-dim2-calibration.md`.)
- **Gate 4 is feasible but is a rewrite.** The existing Python stack is ~1.6e5
  core-hours (infeasible); an optimised kernel measures **229 core-h at M=20**,
  and the real run at `M ~ 70–140` is **13 days to 6 months on 24 cores**. The
  inner loop is a fixed sparse block operator — precompute the table once, then
  it is pure linear algebra. (`gate4-kernel-rewrite-scope.md`.)
- **Precision is bounded.** Recognition obeys `M ~ 1.1–1.3 d log_q0(H)`
  (measured); our recognition degree is 2, so `M ~ 0.7 log10(H)`, and Bosman's
  published heights for the same family put `log10 H ~ 100–200`, likely lower
  since our weight is 2. (`target-height-estimate.md`.)
- **Byproduct: `L` cannot be totally real.** `rd(L) <= 31.9 < 60.8` (Odlyzko),
  so complex conjugation acts as a unipotent involution — a structural fact
  about Dembélé's field from ramification alone, checkable against any
  polynomial we produce.

### Next actions, in order

1. **Re-arm the watchdog** (above). Nothing else keeps the scan alive.
2. **Let gate 1 run.** It needs no attention. Re-assess at norm ~5000 rather
   than on autopilot to 20000.
3. **On a hit:** gate 3 — level-`q0` Brandt module on chatelet, find the
   congruent Steinberg eigensystem (verify, don't trust mod-2 level raising).
   Then the kernel rewrite becomes worth building, and only then.
4. **Optional, cheap, and not blocked by anything:** verify the sharper
   discriminant claim in `target-height-estimate.md` (Bosman's Cor. 2 analogue
   giving `rd(L) ~ 16`), which if correct would put `rd` below the
   totally-imaginary bound too — a sharp claim currently resting on an unverified
   analogy from `F_ell` to `F_256`.
5. Maintain `DECISIONS.md` and `REFERENCES.md` at every fork and new source.

### Gotchas added this session

- `.env.bak` is now gitignored; `remote_magma/set_key.py` rotates the CoCalc key
  without echoing it (the key died once already — see D22's neighbours).
- Never run a repair tool by hand while its automation is armed unless it is
  genuinely idempotent. `restore_scan.py` was not, and double-launched two lanes
  (D22).
- A second Claude session has committed to this repo (`d50f0c4`). Concurrent
  sessions on one working tree can collide.


## Objective and exact target

Construct an explicit polynomial whose splitting field is Dembélé's nonsolvable
extension of \(\mathbf Q\), ramified only at \(2\).

Let

\[
F=\mathbf Q(\zeta_{32})^+,\qquad
S=\operatorname{SL}_2(\mathbf F_{256}).
\]

Dembélé's two residual representations cut out linearly disjoint fields \(E,E'/F\).
Their compositum \(K=EE'\) is Galois over \(\mathbf Q\), with

\[
\operatorname{Gal}(K/\mathbf Q)\simeq S^2\rtimes C_8.
\]

The practical first target is a degree-\(257\) polynomial over
\(\mathbf Q(\sqrt2)\) for the projective \(S\)-action. Combining it with its conjugate
would give a degree-\(514\) polynomial over \(\mathbf Q\) with splitting field \(K\).

Important: geometric descent of the characteristic-zero abelian variety is **not**
needed to define \(K/\mathbf Q\) or prove this Galois group. It is only a possible
constructive shortcut.

## Results completed

### Exact reproduction of Dembélé's computation

- Certified \(F\), its \(C_8\)-action, relevant prime orbits, and class data.
- Reproduced the 58-dimensional raw Brandt module and 57-dimensional cuspidal module.
- Reproduced Dembélé's mod-\(2\) characteristic polynomials.
- Matched every published trace and Frobenius order above \(31\) and \(97\) on both
  eight-dimensional constituents.
- Verified the residual Galois indexing and \(\mathbf F_{256}\) normalization.

### Positive characteristic-zero lift result

The characteristic-zero cusp space decomposes into dimensions

```text
[1, 2, 2, 4, 16, 32].
```

The unique 16-dimensional component has Hecke field \(H\). The two primes of \(H\)
above \(2\) are unramified of residue degree \(8\), and reduction at them gives exactly
Dembélé's two residual systems. This settles the original lift-versus-torsion fork
positively. See:

- `dembele/certificates/lift-report.md`
- `dembele/data/computed/target_lift_field.json`
- `dembele/data/computed/lift_field_structure.json`

There is no quadratic inner twist, CM, or proper base change that reduces the expected
abelian dimension from \(16\) to \(8\).

### Constructive period and invariant audit

- The Costa--Schiavone--Voight isogeny-polynomial framework applies abstractly with
  257 two-isogeny neighbors.
- Only nine Oda sign classes are sufficient, not all 256 signs.
- A direct parallel-weight-4 Hilbert Eisenstein invariant successfully replaced the
  \(4^g\) theta enumeration in the genus-4 17T7 control. It stably separated all
  17 neighbors.
- The Oda-period front end is nevertheless infeasible by the published twisted
  \(L\)-value method. Required single-negative characters first occur at conductor norm
  \(991\), and one decimal digit already requests roughly \(1.35\cdot10^{10}\) Hecke
  coefficients.

See:

- `dembele/certificates/eisenstein-prototype.md`
- `dembele/certificates/period-feasibility.md`
- `dembele/certificates/constructive-feasibility.md`
- `dembele/certificates/csv-paper-adaptation.md`

### Hecke-field ideals and polarization gate

Under GRH class-group bounds:

\[
\mathrm{Cl}(H)\simeq C_2,\qquad
\mathrm{Cl}^+(H)\simeq C_2^2.
\]

Both primes above \(2\) and the codifferent are narrowly principal. Exact data:

- `dembele/data/computed/lift_field_ideals.json`
- `dembele/magma/31_lift_field_ideals.m`

### Descent audit

Cunningham--Dembélé's claimed descent of the 16-fold to \(\mathbf Q\) has a genuine gap
for cyclic degree \(8\): their proof omits the Schur-index-\(2\), totally indefinite
quaternion alternative. The correct conductor of a genuinely descended 16-fold would
be \(2^{124}\), not \(2^{248}\).

Local decomposition of \(H/\mathbf Q(\sqrt5)\) at \(2,5,89,661\) is now exact and
narrows where a quaternion obstruction could ramify. A Whittaker-rationality repair does
not immediately apply because the automorphic induction has singular Hodge weights
\(0^8,1^8\), not regular algebraic weights.

See:

- `dembele/certificates/cunningham-dembele-audit.md`
- `dembele/data/computed/brauer_local_data.json`
- `dembele/magma/33_brauer_local_data.m`

This descent issue is mathematically interesting but is not currently the main blocker
to an explicit polynomial.

## Running computation (historical)

*Superseded — see "Running computation and its care" at the top of this file for
what is actually running. The job recorded here, `lift_field_generators`
(`dembele/magma/34_lift_field_generators.m`, de-GRHing principality of the two
primes above 2 and the codifferent), belongs to an earlier session and does not
unblock the polynomial either way.*

## Current bottleneck and recommended next work

**Update 2026-08-17.** The level-raising route below remains the plan of record, but its costs and risks were measured this session and the conclusions changed — read `dembele/certificates/roadmap-reevaluation.md` first.

**Update 2026-08-13.** The hard stop below is superseded: the one unexplored
door in the exhaustion audit ("Level-raising + CD at an auxiliary prime") is
now the plan of record — see **`dembele/certificates/levelraise-cd-plan.md`**
(gates, prior art, contingencies; gate-1 scan running on chatelet). The
M23-inspired covers investigation is complete and negative — one universal
moduli field (disc 2^18 5^2 17) blocks every all-2-power cover at k=4, with a
proved fixing congruence + calibrated transfer hypothesis closing the family —
written up in **`writeup/all-2-power-covers.md`** with full provenance in
`dembele/rigidity/`. Chatelet is operational for heavy compute
(`remote_magma/upload_dir.py`, detached-nohup pattern; Belyi package deployed).

**Hard stop (historical, 2026-08-04).** An exhaustive audit of constructive ideas is recorded in:

- `dembele/certificates/idea-exhaustion.md`
- `dembele/data/computed/idea_exhaustion.json`
- `dembele/certificates/torsion-construction-scorecard.md`
- `dembele/certificates/frob-disc-gate.md`

Killed in particular: twisted-\(L\) Oda periods; Greenberg–Voight periods at level 1;
dense and sparse Frobenius–Hunter search; \(\Omega^+\)+RM sign recovery; classical
mod-\(2\) level \(2^k\) realization; CSV without a new front end; HMF/RieSrf hacks.

The missing object remains a period matrix or another explicit realization of
\(\lambda\)-torsion. The Eisenstein back end is ready once that exists. Do **not**
restart Hecke/lift audits or re-run variants of the killed routes. The next advance
must be a new mathematical front end outside the present toolkit.

## Verification

Run all lightweight certificates:

```sh
python3 -m unittest discover -s dembele/tests
```

Current result: 34 tests pass.

Magma scripts print explicit `PASS|...` markers because Magma can return process status
zero after a source-level runtime error.

## Repository and environment

- Repository: `/Users/musty/two`
- Branch: `main`
- Remote: `git@github.com:michaelmusty/two.git`
- Local Magma: V2.29-8
- Local HMF package: `/Users/musty/hilbertmodularforms`
- Pinned HMF revision: `f5ce65826697ee1ba7ed6e77a3fda0ef779f633b`
- Remote Magma: `remote_magma/cocalc.py`
- Remote credentials: gitignored CoCalc configuration
- Aristotle virtual environment: `.venv`
- Aristotle credential: `ARISTOTLE_API_KEY` in gitignored `.env`

The current research changes are uncommitted. Review `git status` before beginning new
work. Never print or commit `.env`.

## Primary references

- Dembélé: <https://arxiv.org/abs/0811.4379>
- Cunningham--Dembélé: <https://arxiv.org/abs/1705.03054>
- Costa--Schiavone--Voight: <https://arxiv.org/abs/2411.07857>
- Serre's supplement: <https://doi.org/10.1016/j.crma.2008.12.006>
