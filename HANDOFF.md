# Session handoff

## STATE 2026-09-01 (session close) — read this first

Narrative through **D33** in `DECISIONS.md`.

**THE TATE PILOT ANSWERED AT PHASE 1 (D33): `M_rec ~ 10⁴` — recognition
wall.** Phase 1 completed before session close: the five level-31 curves have
`ord(q_E) ∈ {7960, 8120, 10344, 12888, 62872}` (already the /2-corrected
values; full table with U_31 signs and a_127 in
`dembele/data/computed/tate_lattice.out`). Heights ⇒ recognition precision
~10⁴–10⁵ digits ⇒ the overconvergent chain is out of reach at any
implementation quality. **Option (b) is dead as designed; the
level-raising/CD arc is closed by two measured, independent obstructions
(D32 + D33). Pilot phases 2–4 were NOT built.** The 08-31/09-01 sections
below describe the arc; treat them as history. What stands: the validated
monodromy layer (`v(q) = ⟨v,v⟩_stab/2`, six ground-truth classes over Q),
the orbit-degree certification method (51/55), the D31 pairing intrinsics,
all chatelet banks (`dp_*`, `tate_*`, `l1_*`, `l31_*`).

**Open directions after this arc** (stocktake + D32/D33/D34): the fast-lift
escape was found and priced (D34: one-pass filtration solve — makes the
STANDALONE level-31 curve computation feasible, but transfers to no usable
q0) and the **user chose to stay on the original goal**. So the state of the
goal is: **every door in `idea-exhaustion.md` plus the level-raising/CD door
is now closed and priced**. The next session's task is the hard one the
2026-08-04 hard stop already named: a genuinely new mathematical front end
for realizing the λ-torsion — no candidate is currently on the table. The
priced-out routes and their exact obstructions (orbit sizes D32, intrinsic
heights D33) are the constraints any new idea must clear; read
`stocktake-2026-09-01.md` §1–2 before proposing one. Lemma B
(`writeup/lemma-B-open-problem.md`) remains the clean, self-contained open
problem elsewhere in the project — a legitimate place to spend effort while
the Dembélé front end has no live candidate.

**Historical below this line.**

Former current work: the **Tate pilot** —
`dembele/certificates/tate-pilot-plan.md` (outcome banner at top), workspace
`dembele/tate_pilot/` (README, NOTES, class skeleton, over-Q scripts).

**Pilot state at close:**
- **Monodromy layer ground-truthed over Q**: `v(q_CD-optimal) = ⟨v,v⟩_stab/2`
  on six curve classes, (D,p) = (2,13),(2,7),(3,5),(5,11)
  (`tate_pilot/overq_monodromy2.sage`). Read all `ord(q)` outputs with the
  /2 rule. Derivation of the uniform /2 still owed.
- **Phase 1 RUNNING on chatelet at close** (survives session close by
  construction — RLIMIT_CPU 86400, detached): `56_tate_pilot_lattice.m`,
  output `two_gate3/tate_lattice.out`. FIRST ACTION NEXT SESSION: read that
  file; expect per curve (a_97 ∈ {14,6,2,-6,-14}): saturated vector bank
  `tate_v_a*.m`, ⟨v,v⟩ (halve it!), U_31 sign, a_127; plus banks
  `tate_T97/U31/stabs.m` in ONE session basis. The session's monitors die
  with the session — poll the file, don't wait for notifications.
- **Next implementation step** (the core): definite S-arithmetic group class
  over Q first — (2,13) fully instrumented in `tate_pilot/overq_data.sage`
  (Hurwitz order, 3 classes, stabs (3,2,3), wp of norm 13, 13-adic splitting
  to 13^40). Wire into darmonpoints (8.3, installed in Sage 10.6; interface
  notes in `tate_pilot/README.md` + NOTES); decisive test = computed q vs
  `EllipticCurve('26a1').tate_curve(13).parameter()`. darmonpoints REJECTS
  definite discs even over Q (tested) — the class is unavoidable; build it
  over Q, then retarget via the Magma element export (script 57, NOT yet
  written; must be same-session-complete, see tate_pilot/README).
- Remote job launcher: `remote_magma/launch_remote.py` (upload + detached
  nohup + RLIMIT pattern).

**GATE 5 ANSWERED: NO-GO AT THIS q0 (D32).** The `d_g` determination ran to
completion with every internal check exact. `d_g > 16`: the degree-16
`f1`-side new charpoly splits 2-adically into two degree-8 irreducibles and
no sub-product passes the Deligne bound — every rational Hecke orbit meeting
the block has degree > 16, so the genus-16 gate-4 construction is unavailable
at this auxiliary prime and 52/53 are moot here. The `f2` side is purely old
(as gate 1 predicted). Evidence in `dembele/data/computed/dp_hg_q0.out` and
`dp_hg_f1_block.m`; analysis script `dembele/magma/55_subproduct_f1block.m`.

**Paths forward (D32):** (a) a SECOND auxiliary prime from the scan (resume
at 3 lanes per the 08-27 instructions); the 51 pipeline is validated and
banked, so each new candidate costs one ~8 h run — but note a new q0 needs
its own gate-3-style closure AND its own `dp_T31`-equivalent (a fresh
same-session build at that level, ~30 min); (b) rework gate 4 to use only
the rank-16 2-adic toric data (research question); (c) the contingencies in
`levelraise-cd-plan.md`.

**Banked on chatelet (`two_gate3/`), all validated:** `dp_T31.m` + `dp_W.m` +
`dp_Wtrue.m` (q0, one basis; self-adjoint, D31); `l1_T31.m`, `l1_T97.m`
(level-1 operators); `l31_T97.m`, `dp31_T97/T127/W.m` (level 31);
`dp_hg_f1.m`/`dp_hg_f2.m` (the lifted q0 block actions, 32×32 and 16×16
integer matrices mod 2^192 — `f1`'s is also in the repo).

## STATE 2026-08-31 (superseded by 09-01 above)

Session work in progress; narrative through **D31** in `DECISIONS.md`.

**MAJOR CORRECTION (D31): the monodromy pairing diagonal is the stabilizer
orders `e_i`, NOT the Eichler masses.** The q0 self-adjointness check caught
D29's reciprocal error. `m_i e_i = ulcm/g = 48` at q0 (basis-independent)
converts the banked mass vector offline. Verified: the banked `dp_T31` is
self-adjoint under the converted diagonal on ALL 3 494 618 support entries.
**Authoritative Δ' inputs (chatelet `two_gate3/`): `dp_T31.m` + `dp_W.m`
(masses) + `dp_Wtrue.m` (stab orders), one session, one basis.** The gate-3
banked `gk_s3_T*` are a DIFFERENT session's basis (rebuild ≠ banked,
confirmed) and must not be paired with them. Two package intrinsics now:
`InternalHMFRawStabOrdersDefinite` (the pairing) and
`InternalHMFRawInnerProductDefinite` (dual masses; rewritten to avoid a
95 GB densification that killed the first run of 50). Patch file revised;
chatelet re-uploaded (md5 `c5d39f28...`).

- **The 08-27 level-31 prototype died** ~2 h in (only 2 output lines; the
  detachment lesson struck again). Relaunched locally, then superseded: the
  corrected-pairing version (49 now uses stab orders + banks its operators,
  `DP_BANK=dp31`) **runs on chatelet**, output `two_gate3/dp31_proto.out`.
  Local runs sat at ~40% duty — the launching shell's nice put them on
  E-cores; chatelet is ~2× faster for these builds.
- **CoCalc job pattern (the real semantics):** `timeout` = RLIMIT_CPU
  inherited by detached children; launch with
  `nohup magma -b X.m > out 2>&1 < /dev/null & echo PID=$!`, a LARGE
  `timeout`, `sock_timeout≈60`, then POLL the output file. The socket timing
  out does NOT kill the job. Reusable launcher in the session scratchpad
  (`launch_remote.py`); a client retry once duplicated a job — check
  `ps aux | grep <script>` after launching.
- **`hmf-raw-innerproduct.patch` is now applied on chatelet**: local
  `definite.m` (md5 `a761f109...`) uploaded over the remote copy (backup at
  `two_hilbertmodularforms/ModFrmHil/definite.m.pre-innerproduct.bak`);
  spec compiles remotely, intrinsic visible. Note the remote copy previously
  had an OLDER sparse-hecke revision (no `Columns` option); the upload also
  brought that up to the local revision. Basis compatibility with the banked
  `gk_s3_T*.m` is NOT assumed — it is asserted by `50_delta_prime_q0_W.m`.
- **Scan fleet fully drained** on chatelet; ~100 GB free. The 15 magma
  processes visible there are another user's (`bsd_magma_v7`, Magma 2.29-9).
- **New scripts** (both untested at q0 until the prototype passes):
  - `dembele/magma/50_delta_prime_q0_W.m` — step 1: rebuild raw `M_q0`, read
    `W`, rebuild `T_31`, **assert equality with banked `gk_s3_T31`**, bank `W`.
  - `dembele/magma/51_delta_prime_q0_hg.m` — step (a) of the plan Addendum:
    2-adic block lifting to determine `d_g` and `h_g`. Level-1 self-test ran
    this session; a full self-test at a small prime level should run on
    chatelet before q0. At q0 use `G3_MULT=4,2 G3_TBANK=gk_s3_T31.m`.
- **51's level-31 self-test PASSED** (2026-08-31, `two_gate3/hg_l31_test.out`):
  both blocks T-stable mod 2^192, block charpolys EXACTLY match the Hensel
  factors of the true charpoly, old-part `u²`-division clean with new-part
  degree 0 (correct: nothing raises at 31). Banked: `l1_T97.m`, `l31_T97.m`.
  **The q0 run is launched**: `dp_hg_q0.out`, env `G3_TBANK=dp_T31.m
  G3_MULT=4,2 G3_PREC=192 HG_BANK=dp_hg` — its first deliverable is `d_g`.
- **Plan revision (D30)**: `gate5-delta-prime-plan.md` Addendum 2026-08-31.
  Naive per-prime full charpolys at q0 are memory/time-infeasible; the route
  is 2-adic `h_g` recognition (Deligne bound certifies the balanced lift) +
  per-prime Wiedemann/minimal-polynomial projections for `L_g` (script 52,
  not yet written). **`d_g` (16 vs >16) is the first deliverable** — gate 3's
  new-part residual multiplicity is 2, so a single degree-32 orbit is
  possible, which would make gate 4's term count `M^32/Δ'` — a probable no-go.
  Gate-3 out confirms multiplicities `[4, 2]` and block min-poly `f1²`.

## STATE 2026-08-27 — read this first

Narrative: `DECISIONS.md` (D1–D29). Attributions: `REFERENCES.md`. Plan of
record: `dembele/certificates/levelraise-cd-plan.md`, revised by
`roadmap-reevaluation.md`, `gate5-padic-eisenstein.md`, and — new today —
**`gate5-genus16-term-count.md`**, which blocks the gate-4 build on one
computable number. Read that and the 2026-08-26 section of
`gate3-method-audit.md` before deciding anything.

### GATE 1 IS DONE: q0 = the prime above 7 of norm 2401

Found 2026-08-22 (`const2val = 8`: exactly one of the two residual systems has
`abar_q0 = 0`). D23. Banked in `dembele/scanjob/scan_results.csv`. 61 rationals
scanned by 2026-08-25; primes now cost ~2 days each.

### GATE 3 IS CLOSED (2026-08-27, D28)

`48_gate3_genkernel.m` (attempt 3) verified, in one Magma session at level
`q0`, that on the 32-dimensional generalised eigenspace `G = ker f1(T_31)^2`
each of the four commuting operators `T_31, T_97, T_127, T_191` has
characteristic polynomial `(f1^{(ell)})^4`. The old subspace accounts for
`(f1^{(ell)})^2` (two Iwahori-fixed vectors per level-1 form), so the **new
quotient carries `f`'s residual system at all four primes**; Steinberg at `q0`
follows from newness at prime level with trivial character. Full argument and
the honest limits (no Sturm bound; Galois-conjugate systems give the same
field) in **`dembele/certificates/gate3-closure.md`**; output in
`dembele/data/computed/gate3_genkernel_q0.out`.

What was wrong before (D27b): the earlier "eigensystem match" used the
eigenspace `W = ker f1(T_31)`, which under Ihara's lemma *is* the old
subspace, so that test was vacuous; the generalised eigenspace and the
quotient argument fix it without building degeneracy maps.

**Banked from that session (chatelet `two_gate3/`):** `gk_s3_T{31,97,127,191}.m`,
integer sparse operators, commuting, one basis (39/118/154/231 MB). Use them
*together*; never with operators from any other session.

### GATE 5: computing `Δ'`, the gate-4 go/no-go (IN PROGRESS)

`gate5-genus16-term-count.md` (D27c): the Fourier-term count at genus 16 is
`≤ 1.1·10^4 · M^16 / Δ'`, feasible only if `Δ' ≳ 10^20–10^30`. `Δ'` is the
determinant of the period-valuation pairing.

**The computation is simpler than the certificate first said (D29).** Because
`g` is new at `q0`, `∂ = 0` on the `g`-part, so the character lattice IS the
`g`-isotypic sublattice of the raw Brandt lattice, and the monodromy pairing is
the diagonal **Brandt mass** pairing. No graph, no boundary kernel. Plan:
`gate5-delta-prime-plan.md`. Then

    Δ' = det(B W Bᵀ) / (N(𝓛)² · D_H),

`B` a saturated `Z`-basis of the `g`-sublattice, `W` the mass vector — which
shares a basis with the banked operators `gk_s3_T*.m`.

**Package change:** the mass vector needed a new exported intrinsic
`InternalHMFRawInnerProductDefinite` — `dembele/patches/hmf-raw-innerproduct.patch`,
**applied locally, NOT on chatelet yet** (apply before the `q0` run). First
finding: level-31 masses are `{1,3}`, so `W` is non-scalar (matters).

**In flight at session close:** the pipeline prototype
`49_delta_prime_proto.m` runs over `Q` at level 31 (`~/dp31_proto.out`,
detached, survives session close) to validate self-adjointness, new⊥old,
saturation and the sub/quotient Gram determinants. **Unverified** — check its
output first thing. Caveat: level-31 raw operator builds are ~1 h each, so the
prototype is slow; if it is still churning or wrong, the mechanics are cheap to
re-derive from the plan. Do NOT scale to `q0` until the prototype's checks pass
(especially: `Γ` integral and positive definite, new⊥old = true).

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
- **No gate-3 job is running**; `48` finished 2026-08-27 10:26Z. Relaunch
  recipe if ever needed: `cd two_gate3 && G3_CPBANK=gate3_charpoly_q0.m
  G3_MEMCAP=40 G3_BANK=<tag> HMF_ROOT=../two_hilbertmodularforms nohup
  /usr/local/bin/magma -b 48_gate3_genkernel.m > genkernel.out`, launched via
  `rexec(..., timeout=86400*3, sock_timeout=60)`. Peak memory 10.4 GB with
  sparse operators.
- Memory: 67/125 GB used at 10:30Z 2026-08-27 with three scan lanes still
  finishing; each exiting lane frees 14–17 GB.

### Banked gate-3 artifacts (on chatelet, `two_gate3/`)

| file | what | cost to redo |
|---|---|---|
| `gate3_T31_sparse.m`, `gate3_T97_sparse.m` | level-`q0` operators, separate sessions | 963 s / 3628 s |
| `gate3_T31_same.m`, `gate3_T97_same.m` | the same pair from ONE session (they commute) | 1254 s / 4269 s |
| `gk_s3_T{31,97,127,191}.m` (being written by attempt 3) | integer sparse operators, ONE session, all commute | 1418 / 4329 / 4195 / 6720 s |
| `gate3_charpoly_q0.m` (`cp`) | `charpoly(T_31 mod 2)` at `q0` | 3341 s |
| `gate3_charpoly97_q0.m` (`cp97`) | `charpoly(T_97 mod 2)` at `q0` | 5275 s |
| `gate3_inv97.m` | the `ell=97` level-1 invariant | ~45 min |

The `_same` pair is usable for a two-prime `G` analysis without rebuilding.

### Next actions, in order

1. **Read `~/dp31_proto.out`** (the level-31 `Δ'` prototype). Confirm: `T`
   self-adjoint under `W`; new ⊥ old = true; `L_g` saturates; `Γ` integral and
   positive definite; a sensible `det Γ`. If it errors or is still running,
   fix/finish it — the plan (`gate5-delta-prime-plan.md`) has the mechanics.
2. **Apply `hmf-raw-innerproduct.patch` on chatelet**, then run `Δ'` at `q0`
   multimodularly: `det(Γ) mod p` for ~20–50 split primes, CRT'd; reuse the
   banked `gk_s3_T*.m` (one basis) for the `g`-sublattice, pair against the
   mass vector. ~1–2 core-days, parallel, no host-scale job. Report BOTH the
   sub and quotient determinants (the polarisation ambiguity, D29 / term-count
   §). This is the gate-4 go/no-go.
3. Gate-4 build only if 2 gives `Δ' ≳ 10^20–10^30` with an affordable
   recognition precision `M`.
4. Scan: stays stopped. Resume at 3 lanes (instructions above) only if a
   second `q0` is wanted (e.g. a smaller norm for gate 4).
5. Maintain `DECISIONS.md` and `REFERENCES.md` at every fork.

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
