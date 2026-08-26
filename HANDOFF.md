# Session handoff

## STATE 2026-08-25 — read this first

Narrative: `DECISIONS.md` (D1–D25). Attributions: `REFERENCES.md`. Plan of
record: `dembele/certificates/levelraise-cd-plan.md`, revised by measurement —
read `roadmap-reevaluation.md` and `gate5-padic-eisenstein.md` before deciding
anything.

### GATE 1 IS DONE: q0 = the prime above 7 of norm 2401

Found 2026-08-22 after 53 rationals (`const2val = 8`, i.e.
`v_lambda + v_lambda' = 1`: exactly one of Dembele's two residual systems has
`abar_q0 = 0`). D23. Banked in `dembele/scanjob/scan_results.csv`. The norm is
comfortably inside the affordable window — gate-4 cost goes as `Nq0^2`, and 2401
sits beside the 2111 used in the cost tables.

The scan continues for redundancy only (61 rationals as of 2026-08-25). Its
marginal value is now low, and it occupies the whole host; **consider winding it
down to 2–3 lanes** — it is what created the memory contention that has twice
interfered with gate-3 jobs.

### GATE 3: verified to the eigensystem level

The residual invariant splits into two distinct degree-8 factors (one per prime
above 2 in `H`). At level `q0`, against an oldform baseline of 2:

| `ell` | one factor | the other |
|---|---|---|
| 31 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |
| 97 | multiplicity 4, **excess +2** | multiplicity 2, excess 0 |

**Three independent signatures now agree**, and the excess is always on the side
gate 1 predicted (`const2val = 8` ⇒ exactly one system has `abar_q0 = 0`):

1. **Multiplicity excess** at two primes, on `ell`-specific invariants.
2. **Eigensystem match on the subspace.** `W = ker f(T_31)` is 16-dimensional and
   `charpoly(T_97|W)` is a *single* degree-8 irreducible squared, matching a
   factor of the independently computed level-1 `a_97` invariant. This is the
   step-7 evidence the multiplicity method could not reach.
3. **Non-semisimplicity, exactly where predicted.** Over the residue field the
   block count is `dim ker / 8`. `f1`: primary dimension 32, `dim ker` 16 ⇒
   blocks of size 2, **non-semisimple**. `f2`: primary dimension 16, `dim ker`
   16 ⇒ **semisimple**. Old/new congruence produces precisely that non-split
   gluing, and it appears only on the factor carrying the excess.

**Verified assumptions** (each could have voided the above; see
`gate3-method-audit.md` for the step-by-step grading):

- *Oldform baseline = 2*: against the **full** level-1 charpoly mod 2 (degree 58,
  not just `V16`) both degree-8 factors have multiplicity exactly 1, so no other
  level-1 component shares either residual system.
- *The sparse assembly is correct at level `q0`*: rebuilt in one session, `T_31`
  and `T_97` **commute** (0 failures of 8) — a far tighter constraint than the
  nonzeros-per-column shape check that was previously all we had at that level.

**Still open:** more primes (two is not a Sturm bound; running), and which
level-1 factor each `W` matches — the script printed degrees, not polynomials.
Newness itself follows from the excess plus the verified baseline; Steinberg then
follows from level exactly `q0` with trivial character.

### TRAP: never combine banked operators from different sessions

The package's internal basis (ideal-class reps, unit generators, `P^1`
enumeration) is **not reproducible across Magma sessions**. Banked operators from
different runs do not commute and any joint analysis — eigenspaces, common
kernels, restrictions — is invalid. Characteristic polynomials are
basis-independent, so multiplicity results are safe. Anything joint must be
computed in **one session**.

### The package is patched, and results depend on it

`dembele/patches/hmf-sparse-hecke.patch` against the pinned HMF package. Two
dense `dim x dim` allocations (45.5 GB each at `dim = 109240`) removed: the
Hecke assembly, and `BasisMatrixDefinite` — which at parallel weight 2 was
building *and inverting an identity matrix*. **Apply the patch before
reproducing anything in gate 3.** Verified sparse-first on both branch types and
against the pristine package at level 31.

### Running computation and its care

- **Scan**: 8 lanes, self-harvesting, one prime per process. Durability chain:
  `~/project_init.sh` (project restart) → remote supervisor (session close, lane
  exit) → local watchdog (supervisor death, only while a session is open). All
  three take the same `flock`. **Verified against a real project restart on
  2026-08-24**: everything returned automatically with exactly one process per
  lane. The local watchdog dies with the session; re-arm it if you want the
  third layer:

  ```sh
  cd /Users/musty/two
  while true; do out=$(python3 remote_magma/restore_scan.py 2>&1); \
    [ -n "$out" ] && echo "[watchdog] $(date -u +%H:%MZ) $out"; sleep 600; done
  ```

- **Nothing else is running.** `U_q0` was destroyed by that restart after ~18 h
  and is **not** being rebuilt — see below, it is no longer needed.

### Banked gate-3 artifacts (on chatelet, `two_gate3/`)

Do not recompute these; each is hours of work.

| file | what | cost to redo |
|---|---|---|
| `gate3_T31_sparse.m` | `T_31` at level `q0`, sparse | 963 s |
| `gate3_T97_sparse.m` | `T_97` at level `q0`, sparse | 3628 s |
| `gate3_charpoly_q0.m` | `charpoly(T_31 mod 2)` | 3341 s |
| `gate3_charpoly97_q0.m` | `charpoly(T_97 mod 2)` | 5275 s |
| `gate3_inv97.m` | the `ell=97` level-1 invariant | ~45 min |

### Next actions, in order

1. **Read the four-prime result** (`two_gate3/multiprime.out`, launched
   2026-08-26, ~8 h): primes 31/97/127/191 in one session, each kernel computed
   once and every operator restricted to it, printing *which* level-1 factor
   matches. Extends the eigensystem evidence and closes the labelling gap.
2. **Close gate 3 formally**, writing the argument down: excess + verified
   baseline ⇒ new forms; new + level exactly `q0` + trivial character ⇒
   Steinberg. Optionally verify the degeneracy maps' injectivity/trivial
   intersection, the last soft spot in audit step 4 — `DegUp1Big` /
   `DegDown1Big` / `DegUppBig` call `get_tps` **zero** times, so this is cheap.
3. **Test whether the Eisenstein invariant separates at genus 16.** The
   highest-value open question in the project: only 17 neighbours at genus 4 has
   been tested, 257 at genus 16 is assumed, and if it fails the degree-257
   polynomial degenerates. Cheap relative to gate 4, and it can invalidate that
   build — so do it *before*, not after.
4. **Estimate the q0-adic term count** for the Eisenstein evaluation (depends on
   period valuations; never estimated). `gate5-padic-eisenstein.md`.
5. **Consider winding the scan down to 2–3 lanes.** We have `q0`; further hits
   are redundancy, and the fleet occupies the whole host — it has repeatedly
   squeezed gate-3 jobs (117/125 GB at the last check).
6. **Only then** the gate-4 build: definite S-arithmetic group class + optimised
   kernel (~229 core-h at M=20; 13 days–6 months at M = 70–140).
7. Maintain `DECISIONS.md` and `REFERENCES.md` at every fork.

### Hard-won operational lessons (all cost real time)

- Durability is a property of the **job**, not the host. "Survives session
  close" is not "survives the host" (D25).
- A regression against a reference implementation must call the **new** path
  first — a shared cache can make both paths return the same object, so the test
  passes while proving nothing (`dembele/patches/README.md`).
- **Measure constants; never extrapolate one observation.** Three separate
  mis-estimates this week: the overconvergent inner loop (1300x), dense `GF(2)`
  multiplication (15x, nearly discarded a viable route), and a memory cap set
  from a single peak.
- A monitor whose failure filter is broader than its subject retires itself on
  the first network hiccup — and silence looks exactly like "still running".
- Never hand-run a repair tool while its automation is armed unless it is
  genuinely idempotent (D22).
- **Audit assumptions before building on them.** Two of the seven links in the
  gate-3 chain were unchecked assumptions; one (the oldform baseline) would have
  voided the whole argument, and its failure mode was to make a second
  "independent" confirmation into the same error twice.
- When a computation fails in a way that *should be impossible* (operators that
  must commute, not commuting), enumerate the benign and the fatal explanation
  and design a test that separates them — do not assume the benign one.

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
