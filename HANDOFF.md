# Session handoff

## STATE 2026-08-26 — read this first

Narrative: `DECISIONS.md` (D1–D27). Attributions: `REFERENCES.md`. Plan of
record: `dembele/certificates/levelraise-cd-plan.md`, revised by
`roadmap-reevaluation.md`, `gate5-padic-eisenstein.md`, and — new today —
**`gate5-genus16-term-count.md`**, which blocks the gate-4 build on one
computable number. Read that and the 2026-08-26 section of
`gate3-method-audit.md` before deciding anything.

### GATE 1 IS DONE: q0 = the prime above 7 of norm 2401

Found 2026-08-22 (`const2val = 8`: exactly one of the two residual systems has
`abar_q0 = 0`). D23. Banked in `dembele/scanjob/scan_results.csv`. 61 rationals
scanned by 2026-08-25; primes now cost ~2 days each.

### GATE 3: multiplicity evidence intact; eigensystem evidence REOPENED

What stands (basis-independent, D25/D26):

| `ell` | one factor | the other |
|---|---|---|
| 31 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |
| 97 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |

with the oldform baseline `2·m1 = 2` verified against the full level-1
charpoly, and the sparse assembly validated by same-session commutation.

What fell (2026-08-26, D27b): the "eigensystem match on the subspace" used
`W = ker f1(T_31)`, 16-dimensional — but the mod-2 old subspace is 16-dimensional
and `T_31`-semisimple, so `O ⊆ W`, and under Ihara's lemma `W = O`. Restricting
`T_ell` to `W` only re-derives level-1 data. The four-prime job built on `W`
was retired. Non-semisimplicity is likewise not proof of old/new gluing.

**Running now (the decisive test):** `two_gate3/48_gate3_genkernel.m`
(attempt 2, launched 15:55Z 2026-08-26 with a 3-day CPU limit; output
`two_gate3/genkernel.out`; ~12–14 h). In one session it builds `T_31, T_97,
T_127, T_191` at level `q0`, checks commutation, takes the **generalised**
eigenspace `G = ker f1(T_31)^2` (32-dim) on the excess side only (selected via
the banked level-`q0` charpoly), and prints for each `ell` whether
`charpoly(T_ell | G) = (level-1 charpoly of T_ell on the f1-part)^4`. Because
the old contribution `(f1^{(ell)})^2` is forced by local theory, that equality
is exactly "the new quotient has `f`'s residual system at `ell`". Look for the
lines `T_ell on NEW quotient G/O: ... equals level-1 charpoly^2: true`.

If all four are `true`: gate 3 is verified at the eigensystem level on four
primes; write `gate3-closure.md` (excess + baseline ⇒ new forms; new + prime
level + trivial character ⇒ Steinberg; residual system matches `f` at
31/97/127/191; the full congruence `rho-bar_g = rho-bar_f` is still not
*proved* — no Sturm bound is affordable — but it is what the final
Galois-group certification of the polynomial would catch). If any is `false`:
the new forms carrying the `T_31` excess do not carry `f`'s system at that
prime; the level-raising picture at `q0` is wrong and the scan must resume.

A local smoke test of the same script at level 31 (`G3_LEVEL=31`) runs in
`scratchpad/gk/smoke31.out`; its tail was unit-tested on a synthetic commuting
pair. Attempt 1 on chatelet died at CoCalc's default 120 CPU-second rlimit —
**launch detached jobs only through `rexec(..., timeout=86400*3,
sock_timeout=60)`**, never plain `exec`.

### GATE 5: the back end has a go/no-go number, and gate 4 waits for it

`gate5-genus16-term-count.md` (D27c). The Fourier-term count law
`sqrt(D)·C^n/(n!·N(y))` is validated on the genus-4 control to 0.3%. At genus
16 the q0-adic count is bounded by `1.1·10^4 · M^16 / Δ'`, with `Δ'` the
determinant of the period-valuation pairing relative to unimodular. Feasible
only if `Δ' ≳ 10^20–10^30` (period valuations of tens), and larger valuations
raise the recognition precision `M`, which gate 4 pays for as `M^2`. `Δ'` is
computable from the level-`q0` character group (monodromy pairing on the
`g`-isotypic part, §5 of the certificate) with gate-3 machinery plus an
integral sparse kernel. **Compute `Δ'` before building gate 4.** The
handoff's old item 3 (an archimedean separation run at genus 16) is not the
binding question and was not run.

### TRAP: never combine banked operators from different sessions

Unchanged (D26b). Characteristic polynomials are safe; joint analysis is not.

### The package is patched, and results depend on it

`dembele/patches/hmf-sparse-hecke.patch`. Unchanged; apply before reproducing.

### Running computation and its care

- **Scan: winding down.** `two_scanjob2/STOP_SUPERVISOR` exists (set 13:48Z
  2026-08-26); the supervisor has exited; lane 0 was retired fresh; lanes 1–7
  finish their current primes (norms ≈ 2700–3300, started ~43 h earlier) and
  exit without relaunch. `project_init.sh` honours the STOP file, so a host
  restart does not resurrect the fleet. The local watchdog is not armed and
  must not be (it would relaunch 8 lanes). **To resume at 3 lanes** after the
  fleet drains: `NLANES=3`, `for L in 0 1 2` in `supervise.sh`, mirror in
  `restore_scan.py`, remove the STOP file, relaunch the supervisor (command in
  its header). Do not do this while lanes with `NLANES=8` are still running.
- **`48_gate3_genkernel.m`**: plain detached job, no durability layer; if
  chatelet restarts, relaunch by hand with the `rexec` pattern above
  (`cd two_gate3 && G3_CPBANK=gate3_charpoly_q0.m G3_MEMCAP=16
  HMF_ROOT=../two_hilbertmodularforms nohup /usr/local/bin/magma -b
  48_gate3_genkernel.m > genkernel.out`).
- Memory: 116/125 GB used at launch; each exiting lane frees 14–17 GB.

### Banked gate-3 artifacts (on chatelet, `two_gate3/`)

| file | what | cost to redo |
|---|---|---|
| `gate3_T31_sparse.m`, `gate3_T97_sparse.m` | level-`q0` operators, separate sessions | 963 s / 3628 s |
| `gate3_T31_same.m`, `gate3_T97_same.m` | the same pair from ONE session (they commute) | 1254 s / 4269 s |
| `gate3_charpoly_q0.m` (`cp`) | `charpoly(T_31 mod 2)` at `q0` | 3341 s |
| `gate3_charpoly97_q0.m` (`cp97`) | `charpoly(T_97 mod 2)` at `q0` | 5275 s |
| `gate3_inv97.m` | the `ell=97` level-1 invariant | ~45 min |

The `_same` pair is usable for a two-prime `G` analysis without rebuilding.

### Next actions, in order

1. **Read `genkernel.out`** and act on it as above.
2. **Compute `Δ'`** (`gate5-genus16-term-count.md` §5): the monodromy pairing
   on the `g`-part of the character group at level `q0`. This is the gate-4
   go/no-go and the highest-value open computation in the project.
3. Write `gate3-closure.md` once 1 is in.
4. Resume the scan at 3 lanes only after the fleet drains, if redundancy is
   still wanted.
5. Gate-4 build only after 2 says the window exists.
6. Maintain `DECISIONS.md` and `REFERENCES.md` at every fork.

### Hard-won operational lessons (all cost real time)

- Durability is a property of the **job**, not the host (D25).
- A regression test must call the **new** path first (`patches/README.md`).
- **Measure constants; never extrapolate one observation** (D24).
- A monitor whose failure filter is broader than its subject retires itself on
  the first hiccup — and silence looks like "still running".
- Never hand-run a repair tool while its automation is armed (D22).
- **Audit assumptions before building on them** — twice now: the oldform
  baseline (D26) and the eigenspace-equals-old-subspace trap (D27).
- **Check what a test could *fail* to see.** A test whose output is the same
  whether or not the claim holds is not a test (D27b).
- CoCalc `exec` kills detached children at 120 CPU-seconds; `Bash
  run_in_background` here kills at ~2 h. Detach properly and verify.

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
