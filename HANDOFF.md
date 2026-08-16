# Session handoff

## SESSION CLOSE 2026-08-15 — read this first

Full narrative: `DECISIONS.md` (D1–D18) and `writeup/all-2-power-covers.md`.
Attributions: `REFERENCES.md`. Plan of record: `dembele/certificates/levelraise-cd-plan.md`.

### State of the tracks

1. **Covers/rigidity arc: CLOSED and written up** (unconditional at k=4 — one
   universal degree-8 moduli field, disc 2¹⁸·5²·17, catches every computed
   all-2-power object; family-wide closure conditional on the twice-calibrated
   transfer hypothesis; the +1-torus fixing congruence is proved). Sixteen
   exact certified covers + exact k=8 data (Ni_gen = 32 / 200, forced layers
   Q(ζ₈) / Q(√2), predicted ram(K₈) ⊆ {2,17,257}).
2. **Period route (level-raising + Cerednik–Drinfeld/Greenberg–Voight): the
   sole live path.** Gate 1 (find q₀ of F with ā_{q₀} = 0, i.e. even constant
   coefficient of charpoly(T_q|V16)) is scanning on chatelet: 8 lanes, one
   prime per rational prime (conjugates share the verdict — see D13), norm ≤
   20000, ~280 independent samples, ~2/3 heuristic odds. 32 rationals done
   (all DONE-listed in `two_scanjob2/37_levelraise_lane.m` + 8 more at norms
   1249–1663), 0 hits — on script.
3. **k=4 genus-2 corner (last open verification, decides the twelve
   [10,10,11,11] braid components via cusp bijection): computing LOCALLY**
   (`dembele/rigidity/31_g2_local.m`, mid-numerics at session close). On dump
   (`out/g2_rep1_cfs.m`): recognize Igusa invariants offline (gauge-invariant;
   pattern of scripts 12/26 with noise-floor + two-precision discipline);
   verdict = whether its moduli field also contains K.
4. **Sz(8) hypothesis test: PARKED** (D17 — package coordinate-degeneracy at
   genus 8; needs the vBCPS26 canonical-embedding method).
5. **Aristotle**: project `11dcaed0` (aristotle_fixing, the fixing congruence
   in Lean) shows IDLE — download and check next session
   (`aristotle download 11dcaed0-... --destination out.zip`; source `.env`
   first: `set -a; . ./.env; set +a; . .venv/bin/activate`).

### Running computations and their care

- **Chatelet scan lanes (8–9 processes)**: the project restarts on an
  hours-scale and kills detached jobs (three times so far). A local persistent
  watchdog runs `python3 remote_magma/restore_scan.py` every 10 min
  (environ-census, relaunches missing lanes, append mode) — RE-ARM THIS
  WATCHDOG in the new session (monitors die with the session). Manual check:
  the census inside `restore_scan.py`; per-lane identity via
  `/proc/PID/environ` (LANE=), never via timestamps or launch order (D18).
  Harvest completed rationals into the script's DONE set before any rescan
  edits. Cost ≈ linear in Nq (~hours/prime at current norms).
- **Local genus-2** (`31_g2_local.m` + `out/g2_local.txt`): if dead without
  `out/g2_rep1_cfs.m`, just relaunch (env: BELYI_DUMP_CFS, BELYI_SKIP_POLRED,
  POWSER_ARNOLDI_BIN). ~4 h.
- **~/Belyi carries SIX uncommitted patches** (TrialDivision guard; dump hooks
  in newton.m, newton_hyperelliptic{,-new}.m, recognition.m genus-2 block;
  genus-scaled columns in hyperelliptic.m; polred escape in theta.m). The
  ACTIVE spec loads `newton_hyperelliptic-new.m` and `recognition.m` — the
  genus-2 flow is recognition.m's `Genus eq 2` block. Chatelet's `two_belyi`
  mirrors these. Consider upstreaming.

### Next actions, in order

1. On genus-2 dump: offline Igusa recognition → close/crack the last k=4
   corner; append the verdict to `writeup/all-2-power-covers.md` §3 and
   DECISIONS.md.
2. On scan hit: gate 3 — level-q₀ Brandt module on chatelet, find the
   congruent Steinberg eigensystem (verify, don't trust mod-2 level raising).
3. Check the Aristotle result; if proved, record alongside Lemma A.
4. Then the real project: CD/GV q₀-adic periods (de-risk via `darmonpoints`
   on a small totally real case first). The endgame (2-torsion = square roots
   of the period lattice; p-adic LLL with equivariant gauges; the ready
   Eisenstein back end) is specified in the plan of record.
5. Maintain `DECISIONS.md` and `REFERENCES.md` at every fork and new source.


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

## Running computation

One remote Magma job may still be active:

```text
job: lift_field_generators
script: dembele/magma/34_lift_field_generators.m
purpose: explicit totally positive generators for both primes above 2 and the codifferent
```

Check and fetch it with:

```sh
python3 dembele/jobs/chatelet_job.py status \
  lift_field_generators --marker 'PASS|dembele_lift_field_generators'
python3 dembele/jobs/chatelet_job.py fetch lift_field_generators
```

Allow it to finish if still running. It only de-GRHs principality; it does not unblock
the polynomial. Nothing else should be launched from the killed-route list below.

## Current bottleneck and recommended next work

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
