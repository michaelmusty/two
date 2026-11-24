# Session handoff

<!-- D173, 2026-11-24 -->

**Resume here (2026-11-24, 18:00 UTC): literature review done (D173); nothing running.**
Plan in DECISIONS D173, sources in REFERENCES D173. Next action:
step 1, joint reconstruction with a shared denominator on the stored
`prec_852/fx_*.txt` records (extend script 18: all r(x) values,
e_1..e_k, one lattice with a common denominator; also the other
Laurent ratios). Then step 2, the map evaluated at rational points of
J(Y) on `prec_3408/ly_in.m`.

<!-- D172, 2026-11-21 -->

**Resume here (2026-11-23, 00:10 UTC): model-only test (D172); N = 1704 negative, N = 3408 in progress.**
N = 1704 finished on 22 November at 02:51 UTC: control recognized
(1966 bits), J_Y not recognized in any of the six fields
(`dembele/pivot/results/model_invariants_1704_log.txt`). N = 3408 is
in script 15 (cube system solved at 109020 s CPU); expected
MODEL_DONE around 17:00 UTC on 23 November. Earlier text of this
block follows.
**Update 2026-11-24, 16:00 UTC:** N = 3408 finished (23 November,
12:49 UTC). Two ratios of Tr(g0^2) are 424 and 208 bits below random
size in Q (15584 and 15800 of 16008 bits); J_Y is not. This points to
rational cover invariants of height about 15600 bits; see the D172
outcome in DECISIONS. A rerun of script 20 that prints these vectors
is in `prec_3408/s20b.out` (about 40 minutes; last line
DONE|20_MODEL_INVARIANTS). Next: read the NEAR lines, check the two
vectors against each other and against the control denominators, and
record the result.
**Update 2026-11-24, 16:45 UTC:** confirmed. The two ratios are
rational with about 15585 and 15800 bits; their denominators share a
15577-bit factor and the small primes of the control
(`dembele/pivot/results/model_invariants_3408_near_vectors.txt`).
The cover model is over Q; heights are 7.9 times the control's.
Nothing is running on Chatelet. Next decision: how to bound or lower
the height of the torsion power sums before any further torsion run.
`dembele/pivot/20_model_invariants.m` (env PREC, optional LIST =
script-17 outputs) computes invariants of the cover Y -> C from
`ly_in.m` alone and tries to recognize them. At N = 852: the rational
control on C is recognized (1966 bits); the cover invariant J_Y and
the t-independent torsion sum are not
(`dembele/pivot/results/model_invariants_852_log.txt`; remote
`prec_852/s20.out`). Running since 17:05 UTC in
`two_remote_magma/pivot_lift/`: `./chain_model.sh 1704` and
`./chain_model.sh 3408` (scripts 15, 16, 20 in `prec_<N>/`; logs
`s15.out`, `s16.out`, `s20.out`, last line MODEL_DONE; estimates 8 h
and 28 h). They are not restartable: after a host reboot rerun the
same commands from an exec with `--timeout 864000`. Read in
`s20.out`: lines `J_Y` and the following `in <field>` lines
(RECOGNIZED flag). If J_Y is recognized: record field and height,
then decide the precision of a torsion run. If not at 3408: the cover
is not over F(sqrt -3) or its height exceeds about 3550 bits per
coefficient; reconsider the choice of the third (D84, D88).
`prec_5/fx.txt` is in an old format (do not pass it as LIST).

<!-- D171, 2026-11-21 -->

**Resume here (2026-11-21, 13:00 UTC): N = 852 complete, recognition negative (D171); nothing running.**
All 3855 records are in `two_remote_magma/pivot_lift/prec_852/`
(`fx_<k>_<a>.txt`, 1.3 GB with logs; `*.orig` and `*.out.partial` are
the pieces cut by the reboots, superseded). `s18.out` (copy:
`dembele/pivot/results/power_sums_852_log.txt`): p_1..p_3 at the
random size in Q, Q(sqrt 2) and F. No job of this work is running on
Chatelet (a process `magma.exe -b u246st200.m` seen there earlier is
not ours). The next step is not chosen: see D171 (height-independent
test of the lifted values, a lower-height quantity, or N = 3408).
Launch rule for long jobs is unchanged (exec `--timeout 864000`).

<!-- D170, 2026-11-17 -->

**Update (2026-11-19, 14:55 UTC): two host reboots; continuation `full4.sh` running.**
Chatelet rebooted about 07:50 UTC on 18 Nov and about 23:17 UTC on
18 Nov; each time all jobs died and nothing restarts by itself. The
first restart (`full3.sh`, 18 Nov 12:27) lost the interrupted chunks.
Now running: `./full4.sh 852 128 20` (same log). It keeps the 40
finished chunks and the complete records of the 20 interrupted ones
(1868 records; originals in `fx_*.txt.orig`, logs `*.out.partial`)
and runs the missing 1987 records in 504 chunks of at most 4
(`prec_852/chunks4.txt`), then script 18. After a reboot: rerun the
same command from an exec with `--timeout 864000`; a chunk cut short
is simply rerun (at most 4 records lost per job). Rate under load:
about 57 records per hour. Before trusting `s18.out`: the count of
`^]>,$` lines over `fx_*_*.txt` must be 3855.

**Resume here (2026-11-17, 06:20 UTC): full run at N = 852 in progress (D170).**
The trial `chain.sh 852 1 2` passed (scripts 15, 16: 7878 s, 1161 s;
old script 17: about 3070 s per record). Script 17 was revised (env
`M0` = Newton block, default 16; corrections computed mod p^M0): 757 s
per record at M0 = 128 (931 s at 64, 1472 s at 32, 1070 s at 256), a
job holds about 3.5 GB; `19_compare_r.m` gives agreement mod 673^852
with the trial output `prec_852/fx.txt` on record (1,0).
Running since 06:17 UTC in `two_remote_magma/pivot_lift/`:
`./full3.sh 852 128 20` (log `full3_852.log`; 121 chunks of 32 records
listed in `prec_852/chunks.txt`, 20 processes at a time, outputs
`prec_852/fx_<k>_<a>.txt`, logs `s17_<k>_<a>.out`). Estimate: about
40 hours. It then runs script 18 (`prec_852/s18.out`, last line
FULL_DONE). It is restartable: rerun the same command (from an exec
with `--timeout 864000`); chunks whose log has a DONE line are
skipped. Before trusting `s18.out`, count the `S17|record` lines over
`s17_*_*.out` (must be 3855) and look for `Killed`/errors in
`full3_852.log`. The old script is `17_old_lift_points_padic.m.bak`
on Chatelet (and in git history). Test files `fxb_*.txt`,
`s17b_*.out` in `prec_852/` are from the timing runs.
Recognition thresholds at N = 852: about 890 bits per coefficient in
F, 2670 in Q(sqrt 2), 4000 in Q.

<!-- D169, 2026-11-17 -->

**Resume here (2026-11-17, 00:40 UTC): N = 213 complete, recognition negative (D169); N = 852 trial started.**
All 3855 records are in `two_remote_magma/pivot_lift/prec_213/`
(`fx_<k>_<a>.txt`; records 1..128 of `vb_0` are in `fx_0r_<a>.txt`,
a = 1, 9, ..., 121; `fx_0_1.txt` is an empty leftover of the dead job
and must be left out of LIST). `s18b.out` is the valid script-18
output; `s18.out` is not (3727 records). Nothing recognized in Q,
Q(sqrt 2), F. Control `./chain_alt.sh 5 1 3` (directory `prec_5alt`)
and `PREC=5 FA=prec_5alt/fx.txt FB=prec_213/fx_0r_1.txt magma -b
19_compare_r.m`: r(x) agrees mod 673^5 on three records.
Running: `./chain.sh 852 1 2` (started 00:58 UTC; log `chain_852.log`,
outputs in `prec_852/`). When it ends (`CHAIN_DONE` in
`prec_852/s17.out`, with `ly_in.m` present): read the per-record times
in `s17.out` and the memory, choose the number of simultaneous jobs
(at N = 213 a job held 1 GB, 2 GB while loading), adapt `full2.sh`
(it starts 31 jobs; `fx.txt` of the trial is not in its LIST pattern)
and launch the full run; script 18 runs at the end.
**Launch rule (cause of all silent job deaths so far):** the CoCalc
exec call sets `ulimit -t` (CPU seconds per process, hard limit) to its
`--timeout`, and detached children inherit it. A job launched from
`cocalc.py --timeout 30 exec ...` is killed after 30 CPU seconds
(message `Killed` in the runner log, nothing in the Magma output).
Launch long jobs only from an exec with a large timeout, e.g.
`python3 remote_magma/cocalc.py --timeout 864000 exec '... (nohup ./x.sh > log 2>&1 &)'`,
and check `grep "cpu time" /proc/<pid>/limits`.

<!-- D168, 2026-11-16 -->

**Resume here (2026-11-16, 07:00 UTC): the 673-adic lift passes at N = 1, 2, 5, 32 (D168).**
Chain on Chatelet, directory `two_remote_magma/pivot_lift/`:
`./chain.sh N [FIRST LAST]` runs scripts 15, 16, 17 in `prec_N/`
(inputs linked from the parent; records FIRST..LAST of
`../pivot_tors/vb_0.txt`). Logs `prec_N/s15.out`, `s16.out`, `s17.out`;
outputs `lx_in.m`, `ly_in.m`, `fx.txt`. Script 16 spends 80 s in the
mod-673 header. Per point: about 6 s at N = 2, 40 s at N = 32.
Launch only detached (`nohup ./chain.sh N &` inside a subshell); a job
started inside a remote command without `nohup` dies with the command.
Update 08:00 UTC: `chain.sh 213` passed (cube system, G44, two points:
all residuals zero mod 673^213; 122 s per point alone). Running since
08:00 UTC: `./full.sh 213` (31 jobs of script 17 over all 3855 records,
outputs `prec_213/fx_<k>_<first>.txt`, then script 18 into
`prec_213/s18.out`, last line `FULL_DONE`); estimate 6-8 hours.
Correction 07:30 UTC: the 31 jobs of `full.sh 213` were killed while
loading (project memory peaked at 64 GB; no kernel OOM record). Relaunched
as `./full2.sh 213` (starts 20 s apart, about 1 GB per job); markers
`prec_213/running_<k>_<first>`; log `full2_213.log`. Job 0_1 was started
by hand and is not a child of `full2.sh`. Next: (1) time one point at
N = 213; (2) run all 3855 records (31 jobs over `vb_<k>.txt`);
(3) script 18: r(x) = ratio of the Laurent coefficients t^-42 / t^-43
of f_x, e_1 = sum of traces over all records, recognition in Q,
Q(sqrt 2), F by LLL at each of the 8 embeddings.

<!-- D167, 2026-11-16 -->

**Resume here (2026-11-16, 04:00 UTC): lifting route fixed in outline (D167).**
Running on Chatelet in `two_remote_magma/pivot_tors/`: 15 jobs of
`12_enumerate_Vb_modp.m` (`en<k>.out`, results `vb_<k>.txt`, k = 0..14;
`vb_15.txt` is done), about 256 points each. Tests passed mod 673:
scripts 10, 11, 13 (in `pivot_cover17/`), 14. Next: the work packages in
`dembele/pivot/step4_design_notes.md` section 7, with the per-point
system of section 8, first at N = 2.

Update 2026-11-16 06:00 UTC: the enumeration finished. All 16 jobs end
with `control ... true`; 3855 records, 3855 distinct labels, 3855
distinct f_x, one G44 basis checksum (15772820). Files
`two_remote_magma/pivot_tors/vb_<k>.txt` (82 MB, on Chatelet only;
sha256 in `dembele/pivot/results/enumeration673_log.txt`). No Chatelet
job is running.

<!-- D166, 2026-11-16 -->

**Resume here (2026-11-16): evaluation function and tangency system pass mod 673 (D166).**
Scripts `dembele/pivot/10_eval_function_modp.m` and
`11_tangency_system_modp.m` (run in `two_remote_magma/pivot_tors/`, env
`TAGS=pt11,pt13`, about 90 s each). No Chatelet job is running. Next:
(1) design and prototype the 673-adic model of Y over C (G44, G88 and
multiplication over Z/673^N, N = 2 first), then one Newton step of the
tangency system for pt11; (2) enumerate V_b mod 673 (3855 Frobenius
orbits, about 13 s each) and compute all g_ij mod 673; (3) Weil pairing
or another way to cut the 32896 candidate F_256-structures.

<!-- D165, 2026-11-15 -->

**Resume here (2026-11-15, 22:15 UTC): V_b mod 673 is in hand (D165).**
Points: `two_remote_magma/pivot_tors/pt{11,13,14,15,16}.pt` (sha256 in
`dembele/pivot/results/torsion_points673_log.txt`); pt11 and any other
span V_b with Frobenius conjugates (`results/span_check673_log.txt`,
script `dembele/pivot/09_span_check_modp.m`). No Chatelet job is running.
Next, in order (see `dembele/pivot/step4_design_notes.md`): (1) implement
the global evaluation function mod 673 and test Frobenius equivariance;
(2) Weil pairing on V_b, isotropic F_2[Frob]-lines; (3) prototype
arithmetic over W_N(F_673^17) for N = 2, 4, 8 and measure cost; (4)
decide feasibility of the lift. Nothing of step 4 is computed yet.

<!-- D164, 2026-11-15 -->

**Update (2026-11-15, 17:00 UTC): scans done; route unchanged (D164).**
47 gives order 17/17 (field F_47^34); 7 gives orders 2 (a) and 3 (b) but
the model has a T/B3 collision mod 7 and isolation is unverified; see
DECISIONS D164 and `dembele/pivot/results/frobenius_order_scan.md`. The
five torsion runs in `two_remote_magma/pivot_tors/` (seeds 11, 13-16) run
at about 15 s per addition (five in parallel), about 15.5 CPU-hours per
point, expected end about 20:20 UTC; the D163 block below is otherwise
current.

<!-- D163, 2026-11-15 -->

**Resume here (2026-11-15, 04:50 UTC): step 3 measured; five torsion-point runs in progress (D163).**
`dembele/pivot/07_Y_model_modp.m` builds the evaluation model of Y mod 673
(66 sections of pi^*(2H-G) at 679 rational points; ranks 195 and 324 as
Riemann-Roch predicts; the predicted #J(Y)(F_673) kills two random
classes, order+2 does not; log `results/ymodel673_log.txt`; model file
remote only: `two_remote_magma/pivot_cover17/ymodel673.m`).
`dembele/pivot/08_torsion_point_modp.m` computes one point of V_b over
K = F_673^17: timing run in `results/torsion_timing673.txt` (one addition
about 8-9 s; multiplier has 601-bit coefficients, about 3,800 additions,
so about 9 h per point). Running in `two_remote_magma/pivot_tors/`:
seeds 11, 13, 14, 15, 16 (`pt<seed>.out`, checkpoints `pt<seed>.ck` every
30 min, results `pt<seed>.pt`); seed 12 stopped at start (too few
K-points in its pool). To resume a run, relaunch with the same SEED and
TAG. Expected end about 14:00 UTC. Each run prints whether y is zero,
whether 2y = 0, and g(Frob)y = 0 for the two degree-8 factors.
Next: check the outputs; two or three nonzero points and their Frobenius
conjugates should span V_b (verify rank 16 over F_2); then the 673-adic
lift (model and points) and evaluation, step 4.

<!-- D162, 2026-11-15 -->

**Resume here (2026-11-15, later): step-3 design and isolation check (D162).**
See DECISIONS D162. Target isolation at 673 holds from Hecke data
(`dembele/pivot/results/isolation673.txt`): the Frobenius polynomial of Y
mod 2 is (t+1)^96 * g_a1 * g_a2 * g^2 with g = t^8+t^7+t^6+t^4+t^2+t+1
dividing t^17-1, so V_b = ker g(Frob) in J(Y)[2] and
J(K)[2^inf] = J(F_673)[2^inf] + V_b for K = F_673^17 (2-valuations 40 and
56). Linear-algebra benchmark over K: `results/bench17_linear_algebra.txt`.
Next to write: `dembele/pivot/07_*` building the evaluation model of Y
mod 673 with D0_Y = pi^*(2H - G), deg 129 (design in D162), checked by
[#J(Y)(F_673)] * random class = 0; then one torsion point over K.

<!-- D161, 2026-11-15 -->

**Resume here (2026-11-15): Y is built mod 673 and matches Hecke (D161).**
Step 2 of the D158 plan is done modulo 673 except for the 673-adic lift.
Hecke charpolys at norm 673 are in `dembele/pivot/results/hecke673_raw.txt`
(each level took about 14 h). Predicted Prym order 3^2*m; m*Delta = 0
confirmed; third A = c*Delta with 3c = -1 mod m (script 04). Script 05
builds the Kummer function and the cubic Q4*T^3 - 3*A4*Q4*T - P10 = 0;
coefficients in `dembele/pivot/results/cubic673.m`. Script 06 counts
#C(F_673) = 670 and #Y(F_673) = 692, both equal to the Hecke predictions
(674 - 4 and 674 + 18). Logs: `dembele/pivot/results/cover673_logs.txt`.
Remote-only files in `two_remote_magma/pivot_cover17/`: `state673.m`,
`third673.m` (sha256 2bfdaea4..., 16ec9377...). Not done: count over
F_673^2; the eight alternative thirds were not constructed (the first
one matched). Next: 673-adic lift of the cover data, then step 3 (cost
of one torsion point over F_673^17). Scans at 7 and 47 still running
(`pivot_scan/p7.run2.out`, `p47.run2.out`), no longer on the route.

<!-- D160, 2026-11-14 -->

**Resume here (2026-11-14, later): prime changed from 17 to 673 (D160).**
The exact model is degenerate mod 17 (see DECISIONS D160), so step 2 runs
at the prime of norm 673 generated by [1,-8,-3,14,1,-7,0,1] (order 17 for
system b). Running on Chatelet: (i) `two_remote_magma/pivot_hecke673/`,
script `dembele/pivot/02_hecke_charpolys_at_prime.m`, charpolys of T_P on
the p2-new 16+24 and p2^2-new 48 spaces (log `hecke673.out`, expect many
hours); (ii) `two_remote_magma/pivot_cover17/` (name is historical),
script `dembele/pivot/03_cover_class_modp.m` with `PRIME=673`, the
genus-40 cover, section spaces and branch class Delta mod 673 (log
`s03_673.out`, state `state673.m`). Next: use the p24 charpoly to get the
Prym order, find a third of -Delta (port of script 173), build the Kummer
function and cubic (port of 176), count points against the Hecke
prediction to select the third (ports of 180, 279), then lift 673-adically.

<!-- D159 scan result, 2026-11-14 -->

**Resume here (2026-11-14): Frobenius-order scan done except p=7, 47.**
[Results](dembele/pivot/results/frobenius_order_scan.md). Validation at
norm 97 passes (257, 51). The prime above 17 of norm 289 has order 17 for
both systems (D159: provisional choice). Jobs for 7 and 47 still run on
Chatelet in `two_remote_magma/pivot_scan/` (`p7.out`, `p47.out`, and
backups `p7.run2.out`, `p47.run2.out`); an order 3 or 5 there would beat
17. Launch detached Chatelet jobs through `rexec(env(), cmd,
timeout=<cpu seconds>, sock_timeout=60)`: the CLI `--timeout` is also the
CPU limit of any child. Never use `pkill -n` there. Next: D158 step 2,
rebuild the p-adic model of Y at the chosen prime (residue field F_289),
then cost one torsion point over its degree-17 extension.

<!-- D158 methodology pivot, 2026-11-13 -->

**Current direction: D158 — methodology pivot (2026-11-13).** The user
adopted the [D158 review](dembele/certificates/methodology-pivot-d158.md):
stop proving that the genus-16 candidate is the Shimura quotient; assume
it, compute the degree-257 polynomial by p-adic torsion at a prime chosen
for small Frobenius order, and verify the final polynomial directly. The
P10480 bank is off the route. New-track work lives in `dembele/pivot/`
and runs on Chatelet without the 180-second/2 GiB/three-worker limits or
the frozen-replay requirement; logs are kept, and DECISIONS, HANDOFF and
REFERENCES are updated as work proceeds. All earlier frozen artifacts stay
untouched. Blocks below this one are historical.

**Resume here.** Host `otto` setup notes are in the next entry (Magma is
not licensed locally; Chatelet works: `.env` complete, smoke test passes,
24 cores, 125 GB, 1.1 TB free). Step 1 of the plan is in progress: the
Frobenius-order scan. Validate at 97 against Dembélé's table (expect 51
and 257), then launch one detached Magma per rational prime under
`two_remote_magma/pivot_scan/` and collect `RESULT|` lines. Record results
in `dembele/pivot/` and update this entry.

<!-- Fresh-session entry: 2026-11-12, new-host setup on otto (incomplete) -->

**Setup on `otto.local` is partly done; the source-654 replay has not yet
passed here.** See the [setup record](dembele/checkpoints/newhost-setup-2026-11-12.json).
Done: Homebrew git-lfs/GMP 6.3.0/FLINT 3.6.0 (`libflint.24.0.dylib`
present)/MPFR, NumPy 2.2.6 on Python 3.11.2, `git lfs pull` (2482 objects,
`fsck` OK, clean status), and all three native libraries load.

The first replay attempt, stem `..._newhost_20261112_recheck01`, failed in
0.62 s: the catalogues hash-bind the SageMath 10.6 interpreter at
`/Applications/SageMath-10-6.app/...`, which is not installed. Its receipt,
log and snapshot are preserved; this is environmental, not a mismatch.
The interpreter inside `SageMath-10.6_arm64.dmg` (3-manifolds/Sage_macOS
v2.6.0) has the bound SHA-256.

**Update 2026-11-13.** Sage 10.6 is installed and its hash matches.
`~/hilbertmodularforms` is now at pinned `f5ce6582` with
`hmf-sparse-hecke.patch` applied. Attempts `recheck02`/`recheck03` failed
(preserved): the old host's `ModFrmHil/definite.m` also carried the
prose-only `hmf-raw-innerproduct.patch`, which could not be reproduced
byte-for-byte. A scan of 288 out-of-repository bindings finds 280 matching;
the other eight need byte-identical copies from the original host:
`definite.m`, four files in `~/Belyi`, and Homebrew's `libflint.24.0.dylib`,
`libgmp.10.dylib` and `gmp.h` (same versions, different bottle bytes on
macOS 27). Do not rebuild or substitute them. **Next:** obtain those files,
then replay with stem `..._newhost_20261112_recheck04` and write the
step 5.3 readiness check. Chatelet TLS verifies with the repository
bundle; `.env` holds only `COCALC_BASE`, so the account key and project id
are still needed before the smoke test.

**Update 2026-11-13 (later).** Chatelet is authenticated and the smoke
test passes (24 cores, 125 GB RAM, 1.1 TB free, idle). The bound
`ModFrmHil/definite.m` (sha256 dcdb6b76…) was fetched from Chatelet's
`two_hilbertmodularforms` and installed locally, so seven external files
remain (four in `~/Belyi`, Homebrew `libflint`, `libgmp`, `gmp.h`). The
replay was not re-attempted; `..._recheck04` is still the next stem.

**Capacity:** the LFS store plus working copies use about 23 GiB (not
2.4 GB). Free space is **12.3 GiB** after Sage, below the 13 GiB
single-column P10480 gate and about 58 GiB below the 70 GiB bank gate.
Nothing is admitted or running. The mathematical checkpoint is still
D157; source 655 is still unused.

<!-- End new-host setup on otto -->

<!-- Fresh-session entry: 2026-11-12, new-machine setup after the D157 push -->

**Moving to another machine: set up the items Git does not carry.**
Commit `22395c95` on `origin/main` holds everything through D157, including
2.4 GB of Git LFS payloads. No computation was running when it was made and
none should start on checkout. This entry is operational only; the latest
mathematical checkpoint is still D157 and the "Next" in the 2026-10-16
entry below is unchanged. Source 655 is still next unused.

### 1. Checkout

```sh
git lfs install
git clone git@github.com:michaelmusty/two.git /Users/musty/two
cd /Users/musty/two
git lfs pull
git lfs fsck          # every LFS object present and uncorrupted
git status --short    # expect no output
```

Use the path `/Users/musty/two` on an Apple-silicon Mac if you intend to
run or replay the dyadic jobs: frozen receipts bind absolute paths under
that root, and the three production `.dylib` files in
`dembele/data/computed/` are macOS ARM64 builds linked against
`/opt/homebrew/opt/{flint,gmp}`. Those libraries travel in LFS and must not
be rebuilt in place. Any other OS or checkout root is fine for reading and
new development but needs the separately reviewed portability adapter
described in [CHECKPOINT.md](CHECKPOINT.md#continue-with-dots).

### 2. External tools

| Item | Version on the original host | Setup |
|---|---|---|
| Homebrew GMP, FLINT, MPFR, pkgconf | 6.3.0, 3.6.0, 4.2.2, 3.0.7 | `brew install gmp flint mpfr pkgconf` |
| Python | 3.10.12, with NumPy 2.2.6 | `python3 -m pip install numpy` |
| SageMath | 10.6 (bundles PARI 2.17.1, GAP) | sagemath.org binaries; `sage` on `PATH` |
| Magma | V2.29-8 local (Intel binary) | licensed install, then `softwareupdate --install-rosetta` |
| Julia | 1.12.6 (legacy `belyi_jl/` only) | `julia --project=belyi_jl -e 'using Pkg; Pkg.instantiate()'` |

Homebrew may install a newer FLINT. The production libraries load
`libflint.24.0.dylib`; if that soname is absent, stop and record it rather
than relinking or rebuilding a frozen library.

### 3. Secrets (`.env`, gitignored)

Create `.env` at the repository root with these names. Never commit it or
paste values into logs.

```text
ARISTOTLE_API_KEY=...
AXIOMATIC_API_KEY=...
COCALC_ACCOUNT_API_KEY=sk_...
COCALC_PROJECT_ID=<uuid>
COCALC_BASE=https://chatelet.mit.edu
```

Copy the file from the old machine over a private channel, or regenerate:
for Chatelet, create an account-level key (Account settings, API Keys) and
run `python3 remote_magma/set_key.py` in your own Terminal; it prompts
without echo and preserves the other settings. Details and the smoke test
are in [remote_magma/CHATELET.md](remote_magma/CHATELET.md). The Aristotle
key is needed only for the legacy Lean work.

### 4. Ignored directories

None of these is needed by the current dyadic route (D109 onward); they
serve earlier routes and the 111-test suite.

- **`.venv/`** (Aristotle CLI only):
  `python3 -m venv .venv && . .venv/bin/activate && pip install aristotlelib`
- **`dembele/vendor/LiftTors`**:
  ```sh
  git clone https://github.com/nmascot/LiftTors.git dembele/vendor/LiftTors
  git -C dembele/vendor/LiftTors checkout fd6403caf7147b21b67dcb17dbedccea762d6262
  ```
- **`dembele/vendor/rickards-fdom`**:
  ```sh
  git clone --branch klein https://github.com/JamesRickards-Canada/Fundamental-domains-for-Shimura-curves.git dembele/vendor/rickards-fdom
  git -C dembele/vendor/rickards-fdom checkout 79a12d3f108edce3e78d30c4a59dfc0fb01012d8
  ```
- **`dembele/pari/.build/`** is a build cache. After the vendor checkouts:
  ```sh
  python3 dembele/pari/build_rickards.py
  python3 dembele/pari/build_lifttors.py
  python3 dembele/pari/build_lifttors_rows.py
  python3 dembele/pari/build_lifttors_reduction.py
  python3 dembele/pari/build_lifttors_profile.py
  ```
  The `cm_acb`, `cover` and `belyi_bridge` entries are compiled on first
  use by their Python modules and need `pkg-config flint` to resolve.
  See [the PARI README](dembele/pari/README.md#software-and-build).
- **Checkouts outside the repository** (revisions in
  [dembele/upstream.lock](dembele/upstream.lock)):
  ```sh
  git clone https://github.com/edgarcosta/hilbertmodularforms ~/hilbertmodularforms
  git -C ~/hilbertmodularforms checkout f5ce65826697ee1ba7ed6e77a3fda0ef779f633b
  git clone https://github.com/michaelmusty/inverse-galois-hmf ~/inverse-galois-hmf
  git -C ~/inverse-galois-hmf checkout 4d60ea1943376636a7dca2c0ab805fb8f403aa0b
  ```
  The optional Belyi material (`~/Belyi` at `c8721709…`, and the papers
  under `~/michaelmusty.github.io/assets/`) is the user's own; copy it if
  the Belyi route is revisited.

### 5. Verify the transfer

`scripts/verify_transfer.py` defaults to the 2026-09-30 inventory. That
inventory predates D133–D157 and the D133 journal has since advanced, so
it is not a verifier for this checkpoint and must not be overwritten.
Use instead, in order:

1. `git lfs fsck` and a clean `git status` (step 1): transferred bytes.
2. The source-654 transitive replay, which rechecks the D157 catalogue and
   every inherited hash. Use a fresh receipt stem; never reuse one.
   ```sh
   export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
     MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
   python3 dembele/pari/run_dyadic_capped.py \
     dembele/pari/654_dyadic_higher_pilot_timing_review.py \
     dyadic_higher_pilot_timing_review_d157_newhost_YYYYMMDD_recheck01 \
     'PASS|654_DYADIC_HIGHER_PILOT_TIMING_REVIEW' --check
   ```
   It took 85–100 seconds on the original host, under the 180-second cap.
3. For runtime readiness (engine import, dependency closure, the three
   native libraries, coordinator locks, free space), write a new dated
   check modelled on
   [d157_cleanup_check_20261016.py](dembele/checkpoints/d157_cleanup_check_20261016.py).
   Do not rerun that script: it refuses to overwrite its own record.
4. Optional, needs Sage: `OPENBLAS_NUM_THREADS=1 sage -python -m unittest
   discover -s dembele/tests -v` (111 tests) and the Magma smoke tests in
   `remote_magma/CHATELET.md`.

Record the new host's results in a dated file under `dembele/checkpoints/`
and refresh the free-space observation against the 70 GiB gate before any
launch. All caps, pauses and freezes in the entries below still apply.

<!-- End new-machine setup -->

<!-- Fresh-session entry: 2026-10-16, post-cleanup integrity and capacity -->

**The required D157 checkpoint is intact after the user's disk cleanup.**
The fresh source-654 transitive [replay receipt](dembele/data/computed/dyadic_higher_pilot_timing_review_d157_cleanup_20261016_recheck01.job.json)
passes in 99.729 seconds with no missing or changed required sources.
The bounded [operational check](dembele/data/computed/dyadic_cleanup_check_d157_20261016_attempt01.job.json)
also passes: the production engine imports, its dependency closure
matches the frozen input bridge, and all three native libraries load.
The original completion, previous resume record, 28 current artifact
links and three free coordinator locks are checked.

Git lists only the same two absent scratch files seen before cleanup:
`dyadic_rowjournal_P6400_col00_d132/WORKSPACE.bin` and `aux_ready009.bin`.
The store's seal removes the former; `retired_0022.json` records the
latter's retirement. Neither requires restoration. No frozen file was
restored, modified or deleted by this check.

The dated [cleanup record](dembele/checkpoints/d157-cleanup-check-2026-10-16.json)
records current capacity and runtime checks. The workspace now has about
**117.5 GiB free**, exceeding the unchanged **70 GiB** remaining-bank
gate by about **47.5 GiB**. The storage shortfall in the October 15 entry
below is resolved at this observation; no alternate destination is
needed under the existing model. Space is not reserved and must be
checked again before a future launch.

**Next:** prepare and separately review the P10480 timing experiment
using the existing workspace. This integrity check grants no new
production admission. The full bank, other columns and P10480 launches
remain paused; all mathematical and resource constraints remain in force.
Actual data remain a complete P1600 bank with P6400 columns 0 and 2.
Both new bounded checks have exited, and no production was launched.
The latest mathematical checkpoint remains D157; numbered source 655
is still unused. Preserve these new receipts and the dated check script.

<!-- End D157 post-cleanup integrity and capacity -->

<!-- Fresh-session entry: 2026-10-15, D157 replay and storage refresh -->

**Resumed and verified D157.** Its completed P3200-to-P6400 column-2
pilot remains the latest mathematical checkpoint. The fresh source-654
`--check` [receipt](dembele/data/computed/dyadic_higher_pilot_timing_review_d157_resume_20261015_recheck01.job.json)
passes in 87.402 seconds. The bounded operational
[resume check](dembele/data/computed/dyadic_resume_preflight_d157_20261015_attempt01.job.json)
also passes, verifying the original completion receipt, all 28 current
entry-document links and all three owned coordinator locks. Both new
jobs have exited. No production coordinator was launched.

The [resume record](dembele/checkpoints/d157-resume-2026-10-15.json)
is an operational observation, not a new mathematical certificate.
At **2026-10-15 16:16:39 UTC**, the workspace had **13.69 GiB free**,
leaving **56.31 GiB to the unchanged 70 GiB remaining-bank gate**.
This supersedes the October 13 free-space observation for planning;
the cause of the 30.17 GiB decrease was not investigated. `/Volumes`
still exposes only the same-device Macintosh HD alias. No alternate
destination has been selected, and no frozen file was moved or removed.
A larger storage path was requested from the user; none has yet been
provided. Free space must be refreshed before any future launch.

The inherited P6400-to-P10480 single-column budget is **31419 jobs**,
**18.98–28.85 active hours** excluding shared review allowances, and
**13548388784 bytes** including the 10 GiB reserve, rounded to a
**13 GiB** gate. Only **0.69 GiB** lay above that rounded gate at the
observation. These are existing planning scenarios, not measured
P10480 timings or a launch admission. No P10480 configuration, audit
adaptation, review admission or initial store has been prepared.

**Next:** resolve the storage destination/capacity and separately prepare
and review any P10480 timing experiment before a launch. The full bank,
other columns and P10480 production remain paused under D157. Actual
data remain a complete P1600 bank and P6400 columns 0 and 2; positive
exact vanishing, candidate identification and the field polynomial are
still open. All earlier mathematical pauses and resource caps persist.

Sources 651–654 and all prior bound artifacts remain frozen. The dated
resume script and its successful outputs must not be overwritten;
use a fresh receipt stem for any later source-654 replay. Numbered
source **655** is still unused. The D157 block below remains the
completed checkpoint; earlier fresh-session and preparation blocks
are historical.

<!-- End D157 resume and storage refresh -->

<!-- D157 higher pilot timing checkpoint -->

**Current checkpoint: D157 — the approved column-2 P3200-to-P6400 pilot
is complete.** The [D157 report](dembele/certificates/dyadic-higher-pilot-timing-d157.md),
[fixed review](dembele/data/computed/dyadic_higher_pilot_timing_review_d157.json),
[completion record](dembele/data/computed/dyadic_higher_pilot_timing_completion_d157.json) and
[source ledger](dembele/data/computed/dyadic_higher_pilot_timing_sources_d157.json)
record its results, bounded reviewer repair and timing reassessment.

All 24456 production phases, 97 archives and 24 independent audits passed.
The corrected column review and replay also passed: **24579 successful
column jobs**, including the inherited create. No production or audit job
failed or was rerun. Source 647's final review failed on its obsolete
D153 audit-label assertion. That receipt, log and source snapshot remain
frozen. Source 651 corrects the execution-label assertion and the indexed
receipt-inventory branch; source 652 accepts the actual audits and rejects
seven malformed fixtures. Arithmetic sources are unchanged.

Use `dyadic_higher_pilot_col02_review_r2_d157` as the completed column review
for the unchanged `dyadic_staged_P6400_col02_config_d156` configuration.
The original config's `dyadic_higher_pilot_col02_review_d156` output remains
absent. The CM interface `dyadic_CM_P6400_col02_d156` is now published.
The supervisor's original stopped-after-failure status is preserved;
the separate D157 completion records its successful review recovery.
Do not restart the supervisor, production/audit coordinators, setup or
create, and do not reuse completed output stems. The owned coordinator
locks are free and the temporary power assertion ended.

The successful column cycle measured **9.397 active hours**, or 9.405
including the failed review and regression controls. Production itself
used 9.378 active hours and spanned 12.385 wall-clock hours; this checkpoint
does not establish the cause of the clock gap. It separately accounts for
active time and wall time. Updated remaining scenarios are **19.7–26.5
active days** for 1022790 column jobs. P10480 is still unmeasured, and
one column does not bound other columns or later stages.

The full-bank capacity gap persists. Remaining planned free space is
69.85 GiB including the full largest active-store extra and 10 GiB reserve;
the rounded gate is **70 GiB**. On October 13 at 12:56:44 UTC, 43.87 GiB
was free, leaving **26.13 GiB to the rounded gate**. Preserve all frozen
files; no deletion, relocation or alternate destination is authorized.
The full bank, other columns and P10480 launches remain paused.

**Actual data:** the complete bank remains P1600; columns 0 and 2 are
P6400. Full new equations and complete old overlaps are authenticated;
independent new-equation checks remain samples. D155's conditional proof
criterion still requires actual future errors and exact successive
vanishing. Exact positive vanishing, candidate identification and the
field polynomial remain open. D151 stays parked; spectral/census,
new-level, Hecke and cubic pauses persist.

Keep every mathematical/control/audit/review job under the 180-second
private-process-group cap, at most three workers, 2 GiB per worker/store
and 6 GiB aggregate. Set PYTHONDONTWRITEBYTECODE=1 and the OPENBLAS, OMP,
MKL, VECLIB and NUMEXPR thread counts to one. Sources 651–654 and bound
artifacts are frozen; source 655 is next unused. Source 654 `--check`
with a fresh capped receipt performs the transitive replay. Entry-document
hashes stay editable; earlier D156 blocks are historical.

D157 completion is finished: **24584 new passing bounded jobs and one
preserved failed review attempt**. Fixed provenance review and replay
passed in 86.12/85.10 seconds; completion checked 28 current links across
seven entry documents and records 55 direct source bindings. All jobs
owned by this continuation have exited. No next computation is running.

<!-- End D157 higher pilot timing checkpoint -->

<!-- Fresh-session entry: 2026-10-12, after D156 higher-stage preparation -->

**Start here.** D156 prepares the single column-2 P3200-to-P6400 integrated
timing measurement proposed after D155. The current report and four
checkpoint links are immediately below. Production has not been launched;
no new harmonic moments have been evaluated. The source-554 create
preflight is already complete, with all 174 initial row commitments empty.
Reuse its receipt; never rerun setup or create.

The prepared config is `dyadic_staged_P6400_col02_config_d156`. The column
has 24579 planned jobs including the completed create; 24578 remain.
Model 10.79–13.79 active hours including shared allowances, not a deadline.
The report supplies the exact launch-space, production, audit and review
commands. The next substantive action, after a separate launch decision,
is this one pilot followed by all 24 audits and both reviews, then a
measured reassessment. No second column, P10480 stage or bank is admitted.

The fresh launch-space gate is 12 GiB, including the unchanged 10 GiB
reserve. Source 650 `--launch-check` verifies the initial state, fixed
replay, thread environment and free space without launching a coordinator.
Its receipt must use a fresh name. The current volume was observed at
44.63 GiB free; the rounded remaining-bank gate is 72 GiB, a 27.37 GiB
capacity gap. Only the same-device Macintosh HD alias is visible under
/Volumes. No separate destination, frozen-file deletion or relocation is
authorized. The full-bank capacity problem remains unresolved.

All mathematical, control, audit and review jobs keep the 180-second
private-process-group cap, maximum three workers, 2 GiB per worker/store
and 6 GiB aggregate. Set PYTHONDONTWRITEBYTECODE=1 and the OPENBLAS, OMP,
MKL, VECLIB and NUMEXPR thread counts to one. D156 preparation is sequential.
Use scoped Git text checks; leave credentials and unrelated work untouched.

The actual bank stays P1600, column 0 P6400 and column 2 P3200. D155's
conditional proof criterion remains in force; exact positive vanishing,
candidate identification and the field polynomial are open. Preserve
D151's parked transfer search and every spectral/census, new-level, Hecke
and cubic pause. Earlier checkpoint and fresh-session blocks are history.
Sources 645–650 and the successful bound artifacts are frozen; source 651
is next unused. Source 650 `--check` is the transitive replay, with a fresh
capped receipt stem. Do not recreate its fixed review, recheck01 or
completion outputs. Entry documents remain editable.

All 13 D156 bounded jobs passed; no attempt failed. Fixed admission,
replay and completion are finished, with 28 entry links checked. All
session-owned jobs have exited. The initial pool remains empty.

<!-- End D156 fresh-session entry -->

<!-- D156 pilot preparation checkpoint -->

**Current preparation: D156 — storage plan and one column-2 P3200-to-P6400 timing pilot.**
The [D156 report](dembele/certificates/dyadic-higher-pilot-preparation-d156.md),
[fixed admission](dembele/data/computed/dyadic_higher_pilot_preparation_review_d156.json),
[completion record](dembele/data/computed/dyadic_higher_pilot_preparation_completion_d156.json) and
[source ledger](dembele/data/computed/dyadic_higher_pilot_preparation_sources_d156.json)
bind the exact configuration, inputs, controls, storage and launch sequence.

The single pilot is `dyadic_staged_P6400_col02_config_d156`, using the
completed D154 P3200 seed. There are **24579 column jobs**: 24456 production,
97 archives, 24 independent audits and two column reviews. The empty-store
create preflight is complete and must be reused; all 174 row commitments
remain empty. No new harmonic moments or production coordinator have run.

The column-cycle model is 9.55–11.98 active hours, or **10.79–13.79 hours**
with conservative shared allowances. These are scenarios, not measured
runtimes. The working-store bound is 973167872 bytes. A fresh **12 GiB**
free-space gate includes the 10 GiB reserve. Source 650 `--launch-check`
checks the initial state, fixed replay and current space before a launch.
The report contains the exact sequence. After a separate launch decision,
run only this column, all audits and both reviews, then reassess.

**Full-bank storage remains unresolved.** The October 12 observation is
44.63 GiB free, against 71.02 GiB modeled; the rounded **72 GiB** full-bank
gate needs 27.37 GiB more. No separate volume is selected. Retain all
frozen data; no deletion or relocation is authorized. The pilot fits the
observed space, but no other column, P10480 stage or bank is admitted.

The full bank remains P1600, column 0 P6400 and column 2 P3200. D155's
P10480 sufficient criterion remains conditional on actual certified errors
and exact successive vanishing. Candidate identification and the field
polynomial are open. D151 stays parked; spectral/census, new-level, Hecke
and cubic pauses persist. P10480 timing remains unmeasured.

Keep the 180-second private-process-group cap, at most three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate. Preparation jobs are
sequential. Sources 645–650 and their successful bound artifacts freeze
after admission; source 651 is next unused. Use source 650 `--check` with
a fresh capped receipt for transitive replay. Do not recreate setup,
create, fixed review, recheck01 or completion outputs. Earlier blocks
remain historical, and entry-document hashes remain editable.

D156 completion: all 13 bounded preparation jobs pass with no failures.
Fixed admission and replay took 89.07/84.67 seconds, below the unchanged
180-second limit. Completion checks 28 current artifact links across seven
entry documents and records 93 direct bindings. All jobs owned by this
preparation have finished; no production or audit coordinator was launched.

<!-- End D156 pilot preparation checkpoint -->

<!-- Fresh-session entry: 2026-10-12, session closed after D155 proof review -->

**Start here.** D155 is the current completed checkpoint. The latest
substantive task was the user's request to review the proof criterion
more rigorously; the final request was to update this handoff and close
the session. This closing update changes documentation only. All five
D155 bounded jobs passed, including fixed review, replay and completion;
no attempt failed. All mathematical jobs launched by this session have
finished. There is no unfinished session-owned computation to resume.

Read the [D155 proof review](dembele/certificates/proof-criterion-review-d155.md)
and its [completion record](dembele/data/computed/proof_criterion_completion_d155.json).
The review found no fatal gap in the conditional base-curve implication
under the recorded geometric inputs. P10480 remains sufficient only if
future actual data meet the complete error and zero-containment tests.
The actual rank-45 certificates were replayed at 96 and 160 bits; with
the rational descent and Riemann–Roch dimension 45, exact orders zero
through two suffice. Order one must be proved exactly before order two.

The strict P10480 margins are 6.104656 and 0.169368. A uniform additional
loss of four beta-digits exhausts the second margin. Zhao's factor-of-two
proof discrepancy was reconciled from the integral line-bundle identity,
retaining the height bound; this is our mathematical reconciliation,
not an author-confirmed correction. The finite scripts do not formally
verify the inherited geometry. No calibrated probability of success for
the long computation was established.

**Current data:** the complete bank remains P1600, column 0 is P6400,
and column 2 is P3200. D154's single-column pilot is complete. Do not
restart its coordinators, setup or create jobs, or reuse completed output
names. D155 computed no new harmonic data. Exact positive vanishing and
candidate identification remain open, as do P32/B3, the explicit upstairs
cover, subsequent torsion work and the final field polynomial.

**Next preparation, if continuing this route:** make a concrete storage
plan and separately review a bounded higher-stage timing measurement.
D154's conditional remaining estimate is 20.2–28.5 active days; the
higher stages still dominate the cost and lack integrated measurements.
The saved October 9 storage observation was 48.07 GiB free against a
71.02 GiB plan, a 22.95 GiB shortfall. Refresh that observation before
planning; it is not current free space. Moving or deleting frozen data
is not authorized. The bank remains paused, with no next column, pilot,
higher stage or full bank admitted by this proof review or closing update.

Sources 642–644 and the D155 report/artifacts are frozen; source 645 is
next unused. Source 644 --check, run through run_dyadic_capped.py with a
fresh receipt stem, is the optional transitive replay. Do not recreate
the completed attempt01, recheck01 or completion outputs. Entry documents
remain editable; earlier checkpoint blocks below are historical.

Every mathematical, control, audit and review job retains the 180-second
private-process-group cap, at most three mathematical workers, 2 GiB per
worker/store and 6 GiB aggregate. Set PYTHONDONTWRITEBYTECODE=1 and
OPENBLAS/OMP/MKL/VECLIB/NUMEXPR thread counts to one. Preserve D151's
parked finite transfer search and the spectral/census, new-level, Hecke
and cubic pauses. Use scoped Git checks and leave credentials untouched.

<!-- End D155 fresh-session entry -->

<!-- D155 proof criterion checkpoint -->

**Current reviewed checkpoint: D155 — P10480 remains a valid conditional
base-curve identification criterion after rigorous review.**
The [D155 report](dembele/certificates/proof-criterion-review-d155.md),
[fixed review](dembele/data/computed/proof_criterion_review_d155.json),
[completion record](dembele/data/computed/proof_criterion_completion_d155.json) and
[source ledger](dembele/data/computed/proof_criterion_sources_d155.json)
record the proof, exact finite checks and inherited provenance.

The actual rank-45 minor plus the Riemann–Roch dimension 45 proves that
orders zero through two suffice; the argument explicitly needs D106's
rational descent. All 6528 actual matrix entries were replayed at both
96 and 160 bits. Exact CM-frame vanishing of all 91 quadrics and the
height thresholds were independently checked.

The P10480 strict margins are 6.104656 for order one and 0.169368 for
order two. P10472 fails the second test. An additional uniform loss of
four beta-digits would exhaust the latter margin. Future data must pass
the complete error ledger, zero-containment tests and successive exact
vanishing argument. Reaching a precision label is insufficient.

The review reconciles a factor-of-two discrepancy in Zhao's proof from
the integral line-bundle identity, retaining the existing height bound.
This is a mathematical source reconciliation, not an author-confirmed
correction or formal verification of the inherited geometry.

**Decision:** retain the conditional criterion and keep the larger bank
paused. The base curve, positive exact vanishing and final field polynomial
are still unproved. P32/B3 and the upstairs cover remain separate.
Full-bank precision stays P1600; column 0 stays P6400 and column 2 P3200.
D154's timing and storage limitations and D151's parked search persist.
No new column, higher stage or bank is admitted.

Keep the 180-second private-process-group cap, at most three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate. D155 jobs are
sequential. Sources 642–644 and their bound reports/artifacts are frozen;
source 645 is next unused. Source 644 --check is the transitive replay,
using a fresh receipt stem. Preserve earlier checkpoints as history.

D155 completion: all five bounded jobs pass, with no failed attempts.
Fixed review and replay took 68.18/66.96 seconds, with peak RSS below
280 MB. Completion checks 28 artifact links across seven entry documents
and records 35 direct bindings. All owned mathematical jobs have finished.

<!-- End D155 proof criterion checkpoint -->

<!-- Fresh-session entry: 2026-10-09, after D154 pilot execution -->

**Start here.** D154 records the completed single column-2 P1600-to-P3200
pilot, all 24 independent audits, both column reviews and the measured
reassessment. The fixed timing review, replay and completion all passed.
All 12573 new bounded jobs pass, with no failed attempts; the one prior
create receipt is retained separately. The completion record checks all
28 current artifact links across the seven entry documents.

The production and audit coordinators have exited. Their durable logs
are dyadic_pilot_production_d154_run01.log and
dyadic_pilot_audits_d154_run01.log in dembele/data/computed.
The completed config is dyadic_staged_P3200_col02_config_d153. Do not
re-run its coordinators, setup, create, or any completed output name.
Source 641 --check is the bounded transitive replay with a fresh stem.
All mathematical jobs owned by this continuation have finished. Both
coordinator locks are free. The temporary caffeinate assertion was stopped
and its removal verified; no persistent power setting was changed.

The useful next preparation is a concrete storage plan and a separately
reviewed higher-stage timing measurement. Do not infer admission for a
new column, higher stage or the multiweek bank. Preserve frozen data;
reclaiming or relocating it is not authorized by this checkpoint.
All mathematical, control, audit and review jobs use run_dyadic_capped.py
with the unchanged 180-second process-group timeout, maximum three workers,
2 GiB per worker/store and 6 GiB aggregate. Set PYTHONDONTWRITEBYTECODE=1
and BLAS/OMP/MKL/VECLIB/NUMEXPR thread counts to one. No remote job or
correspondence is part of this continuation. Use scoped Git checks and
leave private credentials untouched. Source 642 is next unused.

<!-- End D154 fresh-session entry -->

<!-- D154 pilot timing checkpoint -->

**Current reviewed checkpoint: D154 — the column-2 P1600-to-P3200 pilot is complete.**
The [D154 report](dembele/certificates/dyadic-pilot-timing-d154.md),
[fixed review](dembele/data/computed/dyadic_pilot_timing_review_d154.json),
[completion record](dembele/data/computed/dyadic_pilot_timing_completion_d154.json) and
[source ledger](dembele/data/computed/dyadic_pilot_timing_sources_d154.json)
record the actual column, measured timing and limited remaining-route scenarios.

All 12570 column jobs pass: 12495 production phases, 49 archives,
24 independent audits and both column reviews. One empty-store create
receipt was inherited from D153; 12569 column jobs are new. The original
coordinator survived the server restart and completed without replaying
jobs. The P3200 store is sealed and its lossless CM interface is published.
Full new equations use authenticated production checks; independent
original-equation samples retain their narrower scope. No attempt failed.

The measured column cycle is 2.126 active hours, versus modeled per-column
costs 2.56--3.02 hours (2.9--3.4 with shared planning allowances).
Production spans 3.624 wall-clock hours; the power log records 5450 seconds
of host sleep. Monotonic computation time and filesystem observations
remain separate. Temporary idle-sleep prevention changed no permanent setting.

**Decision:** keep the larger bank paused. Replacing only the remaining
14 P3200 column costs gives conditional remaining scenarios of 20.2--28.5
active days; higher-stage costs remain unmeasured. The remaining storage
plan calls for 71.02 GiB free including reserve, versus 48.07 GiB observed,
a 22.95 GiB shortfall. Resolve the storage plan and separately review a
bounded higher-stage timing measurement before another launch. No next
column, higher stage or full bank is admitted by D154.

The full bank remains P1600; column 0 remains P6400 and column 2 is now
P3200. P10480 remains a conditional sufficient target, not attained data.
The relation-height upper remains 15237 versus the P1600 target 623.
Exact positive vanishing, candidate identification and the field polynomial
remain open. D151 stays parked; spectral/census, new-level, Hecke and
cubic pauses persist.

Retain the 180-second private-process-group cap, at most three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate. The observed working
store maximum was 291519605 bytes, below its 304049792-byte bound.
Sources 640--641 and their bound artifacts are frozen; source 642 is next unused.
Use source 641 --check through run_dyadic_capped.py with a fresh receipt
stem for transitive replay. It retains 380188 inherited hash occurrences
and checks the new 38446-binding column catalogue. Preserve all frozen
sources, stores and receipts. Entry documents remain editable; earlier
checkpoint blocks are historical.

D154 completion: all 12573 new bounded jobs pass, with no failed attempts;
one prior create receipt is reused. The fixed review and replay took
65.76/64.84 seconds. Completion checks 28 artifact links across the seven
entry documents and records 36 direct bindings. All owned mathematical
jobs have finished, both coordinator locks are free, and the temporary
idle-sleep assertion has been removed.

<!-- End D154 pilot timing checkpoint -->

<!-- Fresh-session entry: 2026-10-09, after D153 pilot preparation -->

**Start here.** D153 is the active checkpoint. The latest “continue”
authorized preparation of the column-2 P1600-to-P3200 integrated timing
pilot proposed in D152. The preparation has a stage-specific fixed
admission, weighted-seed-compatible independent audit, indexed-archive
reviewer and exact launch instructions in the D153 report below.
No production schedule was launched and no new moments were evaluated.

The source-554 create preflight is complete. Reuse its receipt; do not
re-run create or setup. All initial row commitments are empty. The exact
configuration is dyadic_staged_P3200_col02_config_d153. The next substantive
step is this one pilot, estimated at 2.9--3.4 active hours, followed by all
24 audits and review/replay, then an integrated timing reassessment.
Do not infer admission for another column, a higher stage or the full bank.

The report contains runnable production, audit and review commands. D139's
coordinator admits only the hash-bound configuration and requires source
639's passing fixed --check receipt. Keep only one coordinator active;
manual mathematical jobs count toward the same maximum of three workers.
All arithmetic/control/audit/review scripts use run_dyadic_capped.py,
180 seconds per private process group, 2 GiB per worker/store, 6 GiB
aggregate. Set PYTHONDONTWRITEBYTECODE=1 and all BLAS/OMP/MKL/VECLIB/NUMEXPR
thread counts to one. No cap has changed; no remote job was launched.

Sources 635--639 and successful preparation artifacts are frozen.
Source 640 is next unused. Source 639 offers creation, --check and --finish;
only --check may replay completed results, using a fresh receipt stem.
Do not overwrite the fixed admission replay receipt. Its immutable INPUTS
manifest remains bound; prospective pool files are not frozen. Preserve
all old stores and failed snapshots. Entry documents remain editable;
use scoped Git checks and leave private credentials untouched.

D151's finite rational transfer search remains parked. The actual bank
is still P1600 with column 0 at P6400. P10480 remains only a conditional
sufficient target; actual/candidate identification, exact positive
vanishing and the original-kernel field polynomial are unproved.
All previous spectrum/census, new-level, Hecke and cubic pauses remain.

The 12 preparation jobs all pass with no failures. Fixed admission and
replay took 77.87/76.54 seconds and retain the 380188 inherited hash
occurrences covering 379923 unique inherited files. Completion checked
28 artifact links across the seven entry documents. All jobs owned by
this continuation have completed; no production coordinator is running.

<!-- End D153 fresh-session entry -->

<!-- D153 pilot preparation checkpoint -->

**Current reviewed checkpoint: D153 — the single column-2 P1600-to-P3200 timing pilot is prepared.**
The [D153 report](dembele/certificates/dyadic-pilot-preparation-d153.md),
[fixed admission](dembele/data/computed/dyadic_pilot_preparation_review_d153.json),
[preparation completion](dembele/data/computed/dyadic_pilot_preparation_completion_d153.json) and
[source ledger](dembele/data/computed/dyadic_pilot_preparation_sources_d153.json)
bind the exact configuration, input closure, controls and launch sequence.

The admission permits only column 2 at P3200 from its existing P1600 seed,
using the frozen D139 indexed coordinator. No production schedule has
been launched. Source-554 create passed with all 174 row commitments empty;
no new moments were evaluated. Its passing receipt will be reused.
The seed bridge directly binds all 30 seed/CM/native dependencies in D138.

The plan has 12570 jobs (12495 production, 49 archives, 24 audits, two
reviews), including the completed empty-store create. The working-store
bound is 304049792 bytes. Modeled active time remains 2.9--3.4 hours;
10.59 GiB free is recommended including reserve, versus the saved 51.50 GiB
observation. These are planning scenarios, not runtime or allocation bounds.

Source 635 supports the weighted old seed and reproduces five known
P6400 audit phases. Source 636 reproduces the completed P6400 review,
accepts the indexed archive format and retains bounded provenance checks.
Source 638 tests packed overlaps, malformed inputs and all job specifications.
Independent full old overlaps and sampled original-equation checks retain
separate scopes. Complete new equations use authenticated production jobs.

**Next:** run the one prepared pilot through production, all audits and
both reviews, then record integrated timing and reassess before another
column or stage. The full bank is not admitted. P3200 alone does not
identify the candidate. The full bank remains P1600, column 0 remains
P6400, and D152's conditional sufficient target remains P10480 (old P10552).
The relation-height upper remains 15237 versus the P1600 target 623.
Exact positive vanishing and the field polynomial remain open. D151 stays
parked; spectral/census, new-level, Hecke and cubic pauses persist.

Keep the 180-second process-group cap, at most three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate. Preparation jobs are sequential.
Source 639 --check replays the transitive preparation with a fresh receipt
stem. Preserve frozen sources, stores, passing artifacts and failed snapshots;
source 640 is next unused. Earlier checkpoint blocks are historical.

D153 preparation completion: all 12 bounded jobs pass, with no failed
bounded attempts. Admission/replay took 77.87/76.54 seconds; completion
checked 28 artifact links across seven entry documents. All jobs owned
by this preparation have completed. The production pilot is not running.

<!-- End D153 pilot preparation checkpoint -->

<!-- Fresh-session entry: 2026-10-09, after D152 cost assessment -->

**Start here.** D152 is the active checkpoint. The latest “continue”
authorized the proposed bounded cost assessment after D151. Read the D152
report linked below. It derives a conditional P10480 target using the
already certified actual rank-45 map and prices the remaining staged bank.
It neither computes higher precision nor admits a pilot or full-bank run.

The full plan remains roughly three to four active weeks and needs about
20 GiB more free space than the recorded observation. The useful next
preparation is a single column-2 P1600-to-P3200 integrated timing pilot,
estimated at 2.9--3.4 hours. Build its concrete stage-specific admission,
independent audit and bounded review before a launch decision. Its seed
and CM data already have D137/D138 provenance; no column-1 metadata adapter
is needed for this first measurement. D139's indexed coordinator is a
frozen candidate, not an already admitted next-stage coordinator.

Keep source-554 direct seed/native dependency closure, all frozen stores,
failed snapshots and old sources. Every mathematical, control, audit and
review script runs through `dembele/pari/run_dyadic_capped.py`, with the
unchanged 180-second process group, three-worker, 2 GiB per-worker/store
and 6 GiB aggregate limits. Set `PYTHONDONTWRITEBYTECODE=1` and all relevant
BLAS/OMP/MKL/VECLIB/NUMEXPR thread counts to one. Source 634 has creation,
--check and --finish modes; only --check may replay completed results,
using a fresh receipt stem. Source 635 is next unused.

No exact positive zero or candidate identification has been proved. D151's
finite rational transfer obstruction remains in force. P10480 is sufficient
only if future certified enclosures and their error hypotheses pass; it
is not a promise that the candidate will pass. The original-kernel field
polynomial and later marking/cover/Hecke/torsion obligations remain open.
Use scoped Git text checks, preserve unrelated changes, and leave private
credentials untouched. No remote job or correspondence was launched.

The two finite jobs took 0.18/1.70 seconds; review/replay took
63.29/62.45 seconds; completion took 0.08 seconds. All five pass. The
transitive graph retains 380188 hash occurrences covering 379923 distinct
inherited files. No coordinator or remote job remains from this work.

<!-- End D152 fresh-session entry -->

<!-- D152 precision cost checkpoint -->

**Current reviewed checkpoint: D152 — rank 45 lowers the conditional precision target to P10480; the bank still costs about three to four active weeks.**
The [D152 report](dembele/certificates/precision-route-cost-d152.md),
[fixed review](dembele/data/computed/precision_route_review_d152.json),
[completion record](dembele/data/computed/precision_route_completion_d152.json) and
[source applicability ledger](dembele/data/computed/precision_route_sources_d152.json)
record the sufficient-precision argument, cost scenarios and provenance.

The existing actual rank-45 restriction makes exact vanishing through
coarse order two sufficient. Combining it with the proved uniform section
error law gives conditional P10480, versus P10552 for the order-four
argument. Future actual zero enclosures and all arithmetic error hypotheses
are still required. All sixteen columns remain inputs to the current frame
evaluator. The observed extra P1600 digits are not extrapolated.

The staged P10480 plan has 1,059,939 bounded column jobs and modeled active
time 20.6--29.2 days. It needs about 71.5 GiB free including the 10 GiB
planning reserve; the saved observation is 51.5 GiB, about 20.0 GiB short.
These are empirical scenarios, not runtime or allocation bounds. Direct
P1600-to-P10480 refinement violates the unchanged working-store cap.
D136 already supplies complete synthetic target CM memory controls.

**Next preparation:** a separately reviewed column-2 P1600-to-P3200 timing
pilot using its existing seed/CM data and the D139 indexed coordinator.
The estimate is 2.9--3.4 active hours and 0.46--0.59 GiB additional retained
space. Preserve source-554 direct seed/native dependency admission,
stage-specific independent audits and bounded provenance. No pilot or bank
launch follows from this cost checkpoint; P3200 alone does not identify C.

D151's finite rational transfer search stays parked. The proved actual
relation-height upper remains 15237; the P1600 sufficient target remains
623. Positive exact vanishing, identification, P32/B3, downstream
cover/Hecke/torsion obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged, as are all spectral/census,
new-level, Hecke and cubic pauses. Sources 632--634 are frozen;
source 635 is next unused. Earlier checkpoint blocks are historical.

The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate persist. D152 jobs are
sequential. Use source 634 with --check and a fresh receipt stem for a
transitive replay; do not recreate completed outputs. Finite checks do
not mechanically verify the companion rank argument or inherited geometry.

D152 completion: all five bounded jobs pass, with no failed bounded
attempts. The completion record checks 28 checkpoint links across the
seven entry documents. All jobs owned by this continuation are complete.

<!-- End D152 precision cost checkpoint -->

<!-- Fresh-session entry: 2026-10-09, after D151 investigation -->

**Start here.** D151 is the active checkpoint. The user's instruction
“ok let's pursue that” authorized the bounded summed-transfer feasibility
investigation. That investigation reaches a negative conclusion for the
proposed finite rational certificate form, with a concrete positive-order
residual and a companion obstruction proof. Read the D151 report in the
block below, especially sections 3--6, before proposing another witness
search. D150 and earlier entries are preserved history.

The new obstruction is stronger than D150's individual-branch result:
it allows cancellation in the summed operator. Its algebraic functionals
are discontinuous and are not alternative actual harmonic measures.
No positive actual residual has been proved nonzero. The candidate
remains plausible but unidentified; its height is not an actual-curve
height bound. The field polynomial remains unconstructed.

No new bank, spectral/census expansion, level, Hecke computation or cubic
search was launched. Reuse the completed P1600 bank and column 0/P6400.
Further work must add analytic/geometric information outside the excluded
certificate class, or assess the established sufficient precision route's
cost without starting it. The next source is 632. Keep all old sources,
passing artifacts and failed snapshots unchanged.

Every mathematical, control, audit or review job must use
`dembele/pari/run_dyadic_capped.py` with the unchanged 180-second private
process group and memory/worker caps. Set `PYTHONDONTWRITEBYTECODE=1`
and the BLAS/OMP/MKL/VECLIB/NUMEXPR thread counts to one. Source 631 has
separate creation, --check and --finish modes; only --check may replay
against completed result names, using a fresh receipt stem. Entry documents
are intentionally not hash-frozen. Use scoped Git text checks and preserve
unrelated workspace changes. Credentials remain private; no remote job
or correspondence is needed for this checkpoint.

D151 completed all five bounded jobs successfully, with no failed bounded
attempts. The two finite jobs took 0.31/0.62 seconds, review/replay took
60.30/57.84 seconds, and completion took 0.08 seconds. The review traverses
380188 inherited hash occurrences covering 379923 distinct files. The
completion record checks 28 checkpoint links across the seven entry
documents. All jobs owned by this continuation have completed; no
coordinator or remote job was launched.

<!-- End D151 fresh-session entry -->

<!-- D151 summed transfer checkpoint -->

**Current reviewed checkpoint: D151 — the finite rational summed-transfer witness search is parked.**
The [D151 report](dembele/certificates/summed-transfer-obstruction-d151.md),
[fixed review](dembele/data/computed/summed_transfer_review_d151.json),
[completion record](dembele/data/computed/summed_transfer_completion_d151.json) and
[source applicability ledger](dembele/data/computed/summed_transfer_sources_d151.json)
record the companion proof, exact finite witnesses and inherited provenance.

The first positive CM coefficient of saved candidate quadric 0 is a
nonconstant cleared polynomial of degree 240 in 288 scalar integral
inputs. Invariant principal-part functionals preserve every polynomial
moment while assigning those CM inputs freely. They therefore exclude
D150's finite rational tensor transfer certificate for this residual,
including summed cancellations and arbitrary rational witness poles.
These functionals are discontinuous: the proof neither changes the
actual bounded measure nor refutes the candidate.

**Decision:** do not expand this finite witness search. Any continuation
must name additional analytic or geometric input, or reassess the cost
of the established sufficient precision/height route. A cost assessment
does not admit a larger bank. Retain the rank-45 or order-four implication
as the exact identification target. The proved actual relation-height
upper bound remains 15237; the sufficient target remains 623.

Exact positive vanishing, candidate identification, P32/B3 markings,
the subsequent cover/Hecke/torsion obligations and the field polynomial
remain open. P1600 and column 0/P6400 are unchanged. All existing
spectral, census, new-level, Hecke and cubic pauses persist.
Sources 629--631 and passing artifacts are frozen;
source 632 is next unused. Earlier checkpoint blocks are historical.

D151 completion: five bounded jobs pass, with no failed bounded attempts.
The two finite arithmetic jobs use independent quadric derivative
checks and matrix controls. Finite checks do not mechanically verify the
infinite-dimensional functional construction or inherited geometric proofs.
The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate persist. All D151 jobs
are sequential. Use source 631 with --check and a fresh receipt stem
for a transitive replay; do not recreate completed output names.

<!-- End D151 summed transfer checkpoint -->

<!-- Fresh-session entry: 2026-10-09, after D150 completion -->

**Start here.** D150 is the active checkpoint. The older D149 fresh-session
entry below is preserved history. The authorized structural inventory is
now complete for the named packets; no D151 work or source 629 has started.

Read the D150 report, especially sections 1--2 for the actual/candidate
comparison and sections 4--6 for the new closure obstruction and the
remaining exact-identity task. The finite chart count does not make the
moment system finite-dimensional. Only closure under individual branches
is excluded; cancellation in the summed transfer operator remains open.

The next concrete target is an exact finite witness for a cleared
positive-order candidate residual using the actual summed transfer
relations, or an equivalent multiplication-compatible comparison.
Section 5 states a sufficient identity and its tensor extension.
It proves neither existence of a witness nor a practical search bound.
Retain the rank-45 or order-four implication when assessing any proposal.
No new user decision is needed for bounded theoretical investigation.

D149's best height bound 15237 and D141's sufficient target 623 persist.
There is no new positive exact zero or base-curve identification. Preserve
all frozen sources, artifacts and failed snapshots; use fresh numbered
sources and receipt stems. No P3200/higher bank, spectral/census expansion,
new level, Hecke calculation or cubic search is admitted.

D150 completed all five bounded jobs sequentially through
`dembele/pari/run_dyadic_capped.py`. Use source 628 with `--check`
and a fresh receipt stem only if a transitive replay is needed; do not
rerun creation or `--finish` against completed output names. The replay
checks the inherited 380188 hash occurrences / 379923 distinct files.
Ordinary document edits require no mathematical rerun. The unchanged
resource caps and source-554 seed/native admission rules continue.

The two finite jobs took 0.35/0.29 seconds, review/replay took
65.81/68.41 seconds, and completion took 0.13 seconds. All five pass;
there are no new failed bounded attempts. The completion record checks
28 checkpoint links across the seven entry documents.

All jobs owned by this continuation have completed with receipts. No coordinator
or remote job was launched. A system-wide `ps` listing was sandbox-denied,
so D150 does not claim that unrelated system processes were inspected.
Credentials remain private; no key work or remote Magma job is needed.

<!-- End D150 fresh-session entry -->

<!-- D150 structural identification checkpoint -->

**Current reviewed checkpoint: D150 — the structural audit isolates the exact comparison and excludes finite branchwise rational closure.**
The [D150 report](dembele/certificates/structural-identification-audit-d150.md),
[fixed review](dembele/data/computed/structural_identification_review_d150.json),
[completion record](dembele/data/computed/structural_identification_completion_d150.json) and
[source applicability ledger](dembele/data/computed/structural_identification_sources_d150.json)
record the scope, finite witnesses and inherited provenance.

The actual rational frame and rank-45 jet map, and the candidate's
smooth canonical scheme, are established separately. The inspected
descent, Shimizu and cover certificates do not supply the missing
exact multiplication comparison. The best proved actual relation-height
upper bound remains 15237; the sufficient target remains 623.

All 348 child contractions are checked. Among them, 275 have a certified
nonzero denominator slope and a target distinct from the other child.
An explicit reachable cycle supports the proof that finite-dimensional
rational-function spaces closed under every individual child pullback
cannot contain the CM Poisson kernel. This excludes that particular
finite exact-solve proposal. It does not exclude summed cancellations.

**Next proof task:** test a finite exact identity using the summed
transfer operator for one cleared positive-order candidate residual,
or a multiplication-compatible geometric comparison. The report gives
a sufficient tensor identity; a candidate witness is not constructed.
Do not substitute finite congruence, marked automorphism rigidity or
matching invariants for the missing comparison. A height alternative
still needs new actual-curve input.

Exact positive vanishing, candidate identification, P32/B3 markings,
the subsequent cover/Hecke/torsion obligations and the field polynomial
remain open. P1600 and column 0/P6400 are unchanged. All existing
spectral, census, new-level, Hecke and cubic pauses persist.
Sources 626--628 and passing artifacts are frozen;
source 629 is next unused. Earlier checkpoint blocks are historical.
No user decision is pending for this bounded theoretical work.

The two finite jobs pass in about 0.35/0.29 seconds. The review and
completion packet retain the 180-second private-process-group cap,
maximum three mathematical workers, 2 GiB per worker/store and
6 GiB aggregate. Finite checks do not mechanically verify the
companion pole-orbit, functional-identity or geometric proofs.

<!-- End D150 structural identification checkpoint -->


<!-- Fresh-session entry: 2026-10-09, after D149 completion -->

**Start here in a new session.** The active checkpoint is D149. Read this
entry and the D149 block immediately below; subsequent checkpoint blocks
are preserved history, including their superseded next steps and source
numbers. The latest user request was to prepare this handoff for a fresh
session. No D150 mathematical work or source 626 has been started.

The main goal remains an explicit construction of Dembélé's nonsolvable
field ramified only at 2 by the original-kernel route. The immediate gap
is exact identification of the recognized genus-16 candidate with the
actual marked Shimura curve. P1600 independently recovers all 91 candidate
quadrics, but agreement to finite precision is not exact vanishing.
The sufficient actual relation-height target is 623; the best proved
upper bound is 15237. The candidate's height about 547 is not a bound
on the unknown actual relation space. The field polynomial and subsequent
marking, cover, Hecke and torsion obligations remain open.

**Resume with the structural certificate audit.** Existing authorization
covers this bounded proof investigation; no user decision is pending.
The next concrete deliverable is a precise comparison of the already
proved actual-curve inputs with the candidate-only facts, followed by
an exact automorphic identity or correspondence with a proved uniqueness
implication if the available inputs support one. Do not repeat candidate
smoothness checks or treat matching invariants as an identification theorem.

Read these sources in order, following their references only as needed:

1. [D149](dembele/certificates/P1600-primitive-frame-limits-d149.md),
   especially sections 3--6, for the repairs just closed and their limits.
   [D148](dembele/certificates/P1600-forward-frame-bound-d148.md) contains
   the best current actual-height proof.
2. [D140](dembele/certificates/dyadic-P1600-recognition-d140.md) and
   [D141](dembele/certificates/P1600-proof-gap-d141.md) for independent
   recognition, the actual rank-45 certificate, and the exact height-gap
   implication. Higher precision is not needed for equation recognition.
3. [D88's exact comparison criterion](dembele/certificates/d88-cm-expansion-identification-review.md)
   and [D106's arithmetic frame](dembele/certificates/cm-rational-frame-jets-d106.md).
   D69's smooth degree-30 candidate is already certified. Exact actual
   three-coefficient data of rank 45, with the candidate kernel, would
   identify the curve; those coefficient equalities remain unproved.
4. [D62](dembele/certificates/curve-identification-audit.md) identifies
   the arithmetic group and stable graph.
   [D95](dembele/certificates/nelson-global-identification-d95.md) identifies
   a nonzero Shimizu tensor but supplies no arithmetic positive CM jet.
   Neither already identifies the candidate. Consult
   [D51](dembele/certificates/target-realization.md) for the downstream
   canonical Hecke realization and its separate hypotheses.

The initial inventory above was read, but the structural audit is not
complete. A new height argument remains possible if it names additional
actual-curve input. D149 closes only the stated normalization, isolated
pencil/basis and isolated dyadic-index repairs; it does not disprove the
target 623 or all CM-specific cancellations.

**Completed state and execution rules.** D149's completion packet below
is authoritative: five successful bounded jobs, no new failures, 38 direct
source bindings, and 28 checked checkpoint links. The two mathematical
jobs took 5.69/4.14 seconds; review/replay took 59.85/58.78 seconds; finish
took 0.13 seconds. The final process check found no mathematical workers.
There are no live coordinators, pending remote jobs or tool sessions to
resume from this session. Source 626 is next unused.

- Workspace: `/Users/musty/two`, macOS ARM64, zsh. Preserve frozen
  sources 623--625, reports, passing packets and all earlier failed
  snapshots. Entry documents, including this handoff, are deliberately
  not hash-frozen. Use new numbered sources and fresh artifact names.
- Every mathematical, control, audit or review script runs through
  `dembele/pari/run_dyadic_capped.py`: 180-second private-process-group
  cap, at most three mathematical workers, 2 GiB per worker/store and
  6 GiB aggregate. Ordinary document edits need no mathematical rerun.
- Use the installed Sage child interpreter at
  `/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/python3`.
  Sources 623/624 show the required `PATH`, `DOT_SAGE` and parent/child
  resource accounting. Set `PYTHONDONTWRITEBYTECODE=1` and the BLAS,
  OMP, MKL, VECLIB and NUMEXPR thread counts to 1. In Sage use
  `QQ(n)/d`, not the unsupported two-argument `QQ(n,d)` call.
- Reuse completed packets; do not rerun sources 623/624, default review,
  or `--finish` against their existing output names. A transitive replay,
  if needed, uses source 625 with `--check` through the capped wrapper
  and a fresh receipt stem. It traverses 380188 inherited hash occurrences
  covering 379923 distinct files; allow about one minute.
- Keep the full P1600 bank and column 0/P6400 unchanged. No P3200 or
  higher bank, new numerical spectrum/geodesic census, new level, Hecke
  calculation or cubic search is admitted. Do not restart completed
  production coordinators. A separately admitted future source-554 stage
  must retain D138's direct seed/native dependency closure; the later
  transitive review graph does not replace it.
- Use scoped Git text checks; broad status/diff can hit the sandboxed
  LFS path. Preserve unrelated workspace changes. Credentials in `.env`
  and `.env.bak` are private; no key work or remote Magma job is needed
  for this next theoretical audit.

<!-- End fresh-session entry -->

<!-- D149 primitive frame checkpoint -->

**Current reviewed checkpoint: D149 — the primitive-frame comparison closes several isolated repairs; the actual height target 623 remains open.**
The [D149 report](dembele/certificates/P1600-primitive-frame-limits-d149.md),
[fixed review](dembele/data/computed/P1600_primitive_frame_review_d149.json),
[completion record](dembele/data/computed/P1600_primitive_frame_completion_d149.json) and
[source applicability ledger](dembele/data/computed/P1600_primitive_frame_sources_d149.json)
record the proofs, independent controls and inherited provenance.

- The correctly normalized primitive forward pencil map reproduces
  D148's bound exactly. The best proved actual relation-height upper
  bound remains 15237.
- The actual pencil degree is at most -0.4117287, while improving only
  that degree in the frozen estimate would require at least 24.3665.
  Even the favorable pencil endpoint with the field-size term removed
  leaves this majorant above 1162. This is not an actual-height lower
  bound and does not refute the candidate.
- A rank-91 control on an integral nondegenerate curve disproves a
  universal forward cofactor-product cancellation. It does not exclude
  an additional identity specific to the actual CM curve.
- Existing determinant data bound any additional dyadic frame-index
  saving by 986 log(2), less than 684. Refining this index alone cannot
  close the current gap; no additional precision work is admitted.

**Next proof task:** inspect the saved candidate-scheme, canonical-model
and correspondence certificates for an exact automorphic identity or
correspondence with a proved uniqueness implication identifying the
actual marked curve. Reuse established candidate checks. Finite jet
agreement and candidate height do not supply that implication. A new
height comparison must identify an additional actual-curve input.

Exact positive vanishing, candidate identification, the later markings,
cover/Hecke obligations and the field polynomial remain open. P1600 and
column 0/P6400 are unchanged. Existing spectral, new-level, Hecke and
cubic pauses persist. Sources 623--625 and passing artifacts are frozen;
source 626 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the structural certificate audit.

D149 completion: five bounded jobs pass with no new failed attempts.
The two mathematical jobs use independent 192/224-bit ball evaluations
and different rank-91 controls. Finite checks do not mechanically verify
the companion geometric proofs. The 180-second private-process-group
cap, maximum three mathematical workers, 2 GiB per worker/store and
6 GiB aggregate persist.

Operational continuation: sources 623 and 624 take about 5.69 and
4.14 seconds, each with one Sage child. Source 625 uses the standard
attempt01/recheck01/finish sequence and also prices the dyadic index
from the existing discriminant and residue-index data. Follow inherited
reviews through D149 -> D148 -> D147 -> D146 -> D145 -> D144 -> D143 ->
D142 -> D141 -> D140 -> D139 -> D138 and the fifteen catalogues.
D148 source 621's successful input receipt is attempt02; older archived
failures remain frozen. Source-554 seed/native admission requirements,
scoped Git checks and all frozen artifact rules persist.

The new CM cotangent lower endpoint is 0.335546364783548. The pencil
upper endpoint follows from the product of all seventeen principal
parts, including the dyadic norm zero and the archimedean AM-GM factor.
Do not substitute this upper endpoint into a negative-coefficient
formula to claim a new actual-height upper bound: it is used only to
bound the possible improvement of that majorant. The primitive forward
determinant valuation is 1168; its unknown rank-91 relation-image index
lies between 2730 and 18506 in beta valuation. Those endpoints price
a possible saving and do not prove any additional saving.

Initial structural inventory, read after D149's mathematical checks:
D69's smooth degree-30 candidate certificate is already available, as
recalled in d88-cm-expansion-identification-review.md; do not rerun it
as if it were missing. That review gives an exact three-coefficient,
rank-45 sufficient identification criterion. D140 proves the actual
rank, but has not identified those coefficients exactly. D62's
curve-identification-audit.md identifies the arithmetic group and its
stable graph. D95's nelson-global-identification-d95.md identifies a
nonzero Shimizu tensor, but supplies no arithmetic positive CM jet.
Neither report already identifies the candidate curve. These are
starting points for the next audit, not new identification results.


<!-- D148 forward frame checkpoint -->

**Current reviewed checkpoint: D148 — the actual relation-height upper bound improves to 15237; the target 623 remains open.**
The [D148 report](dembele/certificates/P1600-forward-frame-bound-d148.md),
[fixed review](dembele/data/computed/P1600_forward_frame_review_d148.json),
[completion record](dembele/data/computed/P1600_forward_frame_completion_d148.json) and
[source applicability ledger](dembele/data/computed/P1600_forward_frame_sources_d148.json)
record the proof and independent arithmetic checks.

- The actual fixed-coordinate relation space satisfies
  `h_ext(I_2)<15237`, improving D142's 83240 by more than a factor
  of five. The unrounded upper expression is 15236.599070671391.
  This is still too weak for the sufficient P1600 target 623.
- The proof combines the multiplication-image filtration, with worst
  ranks 17/15/13, and an integral trace-dual forward residue map.
  Symmetric metrics and dyadic frame content are retained. It also
  bounds `R-t_mu<15193`; it does not bound R alone or prove R<=578.
- Removing the entire positive field-vector size term leaves this
  majorant above 11266. Sharpening only that term cannot reach 623.
  This is a limitation of the estimate, not a lower bound on the actual
  height or evidence against the candidate.

**Next proof task:** assess a comparison specific to the actual relation
space, or one using the primitive principal-parts pencil, that avoids
the full rank-91 ambient cofactor-frame estimate. Any cancellation must
retain D119's horizontal order and global normalization. Exact structural
identification remains an alternative.

D147's dyadic multiplication surjectivity and D146's `h_Fal(C)<4.2`
persist. Exact positive vanishing, candidate identification, the later
marking/Hecke/cover obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged. Existing spectral, new-level,
Hecke and cubic pauses persist; no new bank or arithmetic search is
admitted. Sources 620--622 and passing artifacts are frozen;
source 623 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the bounded theoretical work.

D148 completion: five bounded jobs pass. One archived audit attempt
failed on a Sage rational-constructor API call in a control; the fix
and full rerun pass. The mathematical height formulas were unchanged.
Finite checks do not mechanically verify the companion geometric
proofs. The 180-second private-process-group cap, maximum three
mathematical workers, 2 GiB per worker/store and 6 GiB aggregate persist.

Operational continuation: source 620 takes about 5 seconds and source
621 about 4 seconds, each with one Sage child. Source 621's successful
receipt is attempt02; attempt01's source snapshot and failure receipt
are frozen. Source 622 uses the ordinary attempt01/recheck01/finish
sequence. Follow inherited reviews through D148 -> D147 -> D146 ->
D145 -> D144 -> D143 -> D142 -> D141 -> D140 -> D139 -> D138 and
the fifteen catalogues. Source-554 seed/native admission requirements,
scoped Git checks, and frozen passing/failed artifacts persist.

The new bound comes from degree(M)<=131Hplus+sum(k_n log beta_n),
S=17H-F, a trace-dual forward frame T, its rank-91 exterior norm,
and the certified (22295/8)log(2) dyadic frame content. Its final H/F
coefficients are 3225/-199. The remaining comparison must improve that
ambient frame loss; it must not use the candidate height as an actual
bound or treat D119's primitive pencil as globally normalized for free.


<!-- D147 multiplication determinant checkpoint -->

**Current reviewed checkpoint: D147 — dyadic multiplication is surjective; the determinant height comparison remains open.**
The [D147 report](dembele/certificates/P1600-multiplication-determinant-d147.md),
[fixed review](dembele/data/computed/P1600_multiplication_review_d147.json),
[completion record](dembele/data/computed/P1600_multiplication_completion_d147.json) and
[source applicability ledger](dembele/data/computed/P1600_multiplication_sources_d147.json)
record the proof and independent finite checks.

- Actual canonical multiplication has rank 45 on the stable dyadic
  fibre. A pivot-minor calculation and 45 independent cycle-pair
  witnesses prove surjectivity; its dyadic cokernel length is zero.
- The normalized identity is
  `h_ext(I_2)=-4F-delta-60log(2)+R-t_mu`, with `t_mu>=0`.
  Here R retains the Mumford metric, multiplication volume and rational
  residue-frame comparison. Existing bounds make `R<=578` sufficient
  for `h_ext(I_2)<=623`; **R has not been bounded by 578**.
  D142's 83240 remains the best proved numerical height upper bound.
- Orbifold weight-four differentials have dimension 72, with 27 extra
  elliptic principal parts beyond the desired rank 45. Their spectral
  determinant cannot be substituted directly. A determinant-one frame
  control also shows why full-frame volume alone is insufficient.

**Next proof task:** bound the actual combined comparison R using the
CM residue construction and the ordinary bicanonical multiplication
quotient metric, retaining cancellations. An orbifold n=2 approach
first needs its extra principal parts and metric/lattice comparisons.
Exact structural identification remains an alternative.

D146's `h_Fal(C)<4.2` and the closure of the Faltings-only P1600 repair
persist. Exact positive vanishing, candidate identification, the later
marking/Hecke/cover obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged; existing spectral, new-level,
Hecke and cubic pauses persist. No new bank or arithmetic search is
admitted. Sources 617--619 and passing artifacts are frozen;
source 620 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the bounded theoretical work.

D147 completion: five bounded jobs pass. One archived final-review
attempt failed on D99's legacy uppercase status format and was fixed;
both mathematical jobs passed unchanged. Finite checks do not
mechanically verify the companion geometric proofs. The 180-second
private-process-group cap, maximum three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate caps persist.

Operational continuation: sources 617/618 each use one Sage child and
complete in about 5/4 seconds. The independent audit saves 45 explicit
pairs of cycles intersecting in one edge. Source 619 also replays their
paths and the primary pivot minor with integer bit arithmetic. Its first
review attempt failed only on D99's uppercase `PASS` status; the source
snapshot and receipt are frozen. The successful review uses attempt02.
Follow the inherited review through D147 -> D146 -> D145 -> D144 ->
D143 -> D142 -> D141 -> D140 -> D139 -> D138 and the fifteen catalogues.
Source-554 seed/native admission requirements and scoped Git checks persist.


<!-- D146 elliptic intersection checkpoint -->

**Current reviewed checkpoint: D146 — the Faltings-only P1600 repair is ruled out.**
The [D146 report](dembele/certificates/P1600-elliptic-intersections-d146.md),
[fixed review](dembele/data/computed/P1600_intersection_review_d146.json),
[completion record](dembele/data/computed/P1600_intersection_completion_d146.json) and
[source applicability ledger](dembele/data/computed/P1600_intersection_sources_d146.json)
record the proof and independent finite checks.

- The actual combined elliptic term satisfies `48 < Psi+I < 79`.
  All dyadic intersections on Q are accounted for. Distinct elliptic
  points stay disjoint away from 2 and 3; at 3 the local groups C3
  and S3 give total pair cost between `18log(3)` and `45log(3)`.
- Together with D144's corrected RR identity and D145's spectral
  bound, this proves `h_Fal(C)<4.2`. The target `h_Fal(C)>=29`
  is false, and all three D141 critical height thresholds are excluded.
  Improving only that lower bound cannot repair the existing P1600
  jet criterion. The prior CM/RR source reconciliations remain part
  of the proof; they are not author-confirmed errata.
- The actual relation-space height target `h_ext(I_2)<=623` is
  still open. This result does not refute the recognized candidate.
  Exact positive vanishing, identification, the later marking/Hecke/
  cover obligations and the field polynomial remain unproved.

**Next proof task:** investigate the determinant of the canonical
multiplication sequence in the fixed rational residue frame as a
route to the actual relation-space height bound. Retain integral
indices and archimedean quotient metrics; no bound from this proposal
is yet claimed. D142's jet-row bound 83240 remains too weak. Exact
structural identification remains an alternative.

P1600 and column 0/P6400 are unchanged. Existing spectral, new-level,
Hecke and cubic pauses persist. No new bank or arithmetic search is
admitted. Sources 614--616 and passing artifacts are frozen;
source 617 is next unused. Earlier checkpoint blocks are historical.
No new user decision is needed for the continuing bounded theoretical
investigation.

D146 completion: five bounded jobs pass (primary calculation,
independent audit, fixed review, replay and completion audit);
no D146 job failed. Finite checks do not mechanically verify the
companion geometric proofs or published theorems. The 180-second
private-process-group cap, maximum three mathematical workers,
2 GiB per worker/store and 6 GiB aggregate caps persist.

Operational continuation: sources 614/615 each use one Sage child
and take about 5/4 seconds. Follow `inherited_review` through
D146 -> D145 -> D144 -> D143 -> D142 -> D141 -> D140 -> D139
-> D138 and the fifteen inherited catalogues (380,188 inherited
hash occurrences, 379,923 distinct files). Preserve all frozen
sources and earlier failed attempts. Source-554 seed/native admission
requirements persist. Use scoped Git checks. No D146 mathematical
worker remains active.

The new local argument uses the faithful special-fibre action,
the fixed-section derivative `nu(zeta3-1)=nu(3)/2`, and the different
product. Its C3/S3 rational-function examples are controls, not a
claim that all actual actions have those coordinates. D118's saved
dyadic content and the marked-tail corrections are used exactly once.
The next determinant argument must concern the unknown actual kernel;
the recognized candidate's height 547.226455 is not such a bound.

<!-- D145 spectral feasibility checkpoint -->

**Current reviewed checkpoint: D145 — the proposed spectral target is ruled out.**
The [D145 report](dembele/certificates/P1600-spectral-feasibility-d145.md),
[fixed review](dembele/data/computed/P1600_spectral_review_d145.json),
[completion record](dembele/data/computed/P1600_spectral_completion_d145.json) and
[source applicability ledger](dembele/data/computed/P1600_spectral_sources_d145.json)
record the proof and independent finite checks.

- Every complex embedding satisfies `log Zprime(1) > -41`, hence
  `average(log Zprime(1)) > -41`. D144's proposed sufficient upper
  target `-96.820` is false. The spectral lower bound is independent
  of D144's reconstructed Riemann--Roch constants.
- Exhaustive scalar trace checks give systole `>acosh(25)>3.9`.
  Two independent enumerations through bound 80 check all 4,093 sign
  pairs. The congruence spectral-gap theorem and a positive heat-trace
  argument then prove the bound; no numerical eigenvalues or closed
  geodesic census are used.
- Under the D144 RR identity, `h_Fal(C)>=29` now requires
  `Psi+I < -249`. This is a necessary condition, not a proved or
  sufficient bound. The current joint upper bound is 85.172.
  The desired height itself has neither been proved nor disproved.

**Next proof task:** assess the omitted geometric intersections using
saved derivative contents and local constraints against this necessary
threshold. Exact structural identification remains an alternative.
Do not pursue the false D144 spectral target or increase precision
to address it. No new user decision is needed for this bounded
theoretical investigation.

Exact positive vanishing, identification, marking/Hecke/cover
obligations and the field polynomial remain open. The sufficient
relation-space height bound 623 remains open. P1600 and column
0/P6400 are unchanged. Existing spectral, new-level, Hecke and cubic
pauses persist. Sources 609--613 and passing artifacts are frozen;
source 614 is next unused. Earlier checkpoint blocks are historical.

D145 completion: seven bounded jobs pass (four inputs, fixed review,
replay and completion audit); no D145 job failed. Finite checks do
not mechanically verify the companion proofs or published theorems.
The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate caps persist.

Operational continuation: sources 609--611 each use one Sage child
and take about 4--6 seconds; source 612 uses exact Python rational
arithmetic and takes under a second. The review follows
`inherited_review` through D145 -> D144 -> D143 -> D142 -> D141
-> D140 -> D139 -> D138 and the fifteen inherited catalogues
(380,188 inherited hash occurrences, 379,923 distinct files).
Preserve every frozen source and earlier failed attempt. The
source-554 seed/native admission requirements remain unchanged.
Use scoped Git checks. No D145 mathematical worker remains active.

Starting point for the next investigation: D118 determines the dyadic
part of the combined derivative content 2*c_L+c_ram, not its full
finite degree and not separate values of the two terms. Its formula
does not supply the missing odd-prime intersections. D119 supplies
the ordinary dyadic pairs already used by D144. Do not count these
known corrections twice; inspect what additional local geometry can
actually certify before scheduling any new arithmetic search.

<!-- D144 joint adjunction and compact RR checkpoint -->

**Current reviewed checkpoint: D144 — joint elliptic bound and compact RR normalization reconstructed.**
The [D144 report](dembele/certificates/P1600-joint-adjunction-RR-d144.md),
[fixed review](dembele/data/computed/P1600_joint_RR_review_d144.json),
[completion record](dembele/data/computed/P1600_joint_RR_completion_d144.json) and
[source applicability ledger](dembele/data/computed/P1600_joint_RR_sources_d144.json)
record the derivations and independent finite checks.

- Adjunction bounds the actual combined term `Psi+I < 85.172`.
  Unknown intersections have a favorable sign. The bound uses the
  recovered anchor order-2/order-32 intersection, the saved ordinary
  pairs, marked tail corrections, and derivative integrality at 3.
- The compact comparison has
  `log(C_*)=15log(pi)+(5081/192)log(2)+log(3)-485/64`.
  Its derivation corrects the cone, boundary and metric-adjunction
  factors, with cutoff-independence and a separate Teo spectral check.
  These are our documented source corrections, not author-confirmed
  errata or a claim about cusps. Finite audits do not mechanically
  verify the companion mathematical proofs.
- The remaining sufficient target is
  `average(log Zprime(1)) <= -96.820`, which would prove
  `h_Fal(C)>=29`. This inequality is unproved and untested on C.
  The existing upper height bound also implies the consistency bound
  `average(log Zprime(1)) > -98.900`.

**Next proof task:** derive a certified analytic route to the remaining
spectral upper bound and assess its feasibility before admitting an
actual-curve numerical computation. Exact structural identification
remains an alternative. No new user decision is needed for that
continuing theoretical investigation.

The sufficient targets `h_ext(I_2)<=623` and `h_Fal(C)>=29` remain
unproved. Exact positive vanishing, identification, marking/Hecke/cover
obligations and the field polynomial remain open. P1600 and column
0/P6400 are unchanged. The spectral, new-level, Hecke and cubic pauses
persist; no higher bank is admitted. Sources 606--608 and the passing
bound artifacts are frozen; source 609 is next unused. The failed first
607 attempt is preserved (a path-length control used 28 instead of 20);
its corrected replay passes. Earlier checkpoint blocks are historical.

Operational continuation: retain the 180-second private-process-group
wrapper, maximum three mathematical workers, 2 GiB per worker/store and
6 GiB aggregate caps. Sources 606/607 each use one Sage child and took
about 5/4 seconds. The fixed review has 40 direct bindings. Follow
`inherited_review` through D144 -> D143 -> D142 -> D141 -> D140 -> D139
-> D138 and the fifteen inherited catalogues (380,188 hash occurrences,
379,923 distinct files). Preserve every failed attempt and frozen source.
The source-554 seed/native admission requirements persist. Use scoped
Git checks. The next task requires an analytic proof strategy, not an
unapproved spectrum, geodesic census or precision-bank launch.

D144 completion: four bounded jobs pass (primary calculation, independent
audit, fixed review and replay); one failed control attempt is preserved.
The final review/replay took 59.86/59.77 seconds. All scoped whitespace
checks pass. No D144 mathematical worker remains active.

<!-- D143 finite model and elliptic cotangent checkpoint -->

**Current reviewed checkpoint: D143 — finite-model comparison and both missing cotangent bounds established.**
The [D143 report](dembele/certificates/P1600-finite-model-cotangents-d143.md),
[fixed review](dembele/data/computed/P1600_finite_model_review_d143.json),
[completion record](dembele/data/computed/P1600_finite_model_completion_d143.json) and
[source applicability ledger](dembele/data/computed/P1600_finite_model_sources_d143.json)
record the proofs and independent finite checks.

- The actual normalizer model correction is
  `E_model=-(12421/6144)*log(2)`, approximately `-1.401299012`.
  All 58 component-degree identities hold; independent stabilizer and
  graph calculations agree, including the marked rational-tail correction.
  C has good reduction away from 2, so `delta_other=0`.
- The order-3 and order-32 cotangent heights satisfy
  `H_3<3.948`, `H_32<99.372`; the full elliptic cotangent sum is
  `Psi<164.846`. The two CM fields use different applicable height
  theorems, with independent character and field-discriminant checks.
- Under the complete corrected Riemann--Roch comparison, a sufficient
  remaining target is `I+6 average(log(C_* Zprime(1))) <= -486.385`.
  The full intersection bound and corrected global analytic comparison
  remain open. This target is not a proved inequality.

**Next proof task:** control the remaining intersection contribution and
reconcile the complete corrected global RR constant, then assess the
required analytic inequality. An adjunction bound for `Psi+I` together
is worth investigating before computing every intersection separately.
Exact structural identification remains an alternative.

The sufficient targets `h_ext(I_2)<=623` and `h_Fal(C)>=29` remain
unproved. D142's actual upper bounds 83240 and 30.039246 stand, as does
D140's independent recognition. Exact positive vanishing, identification,
marking/Hecke/cover obligations and the field polynomial remain open.
P1600 and column 0/P6400 are unchanged; no higher bank or numerical
spectral work on C is admitted. All six bounded D143 jobs pass,
including two independent input audits and fixed review/replay; no D143
job failed. Sources 601--605 and all bound artifacts are frozen;
source 606 is next unused. Existing pauses and resource caps persist.
Earlier checkpoint blocks and next-task statements below are historical.

Final review/replay took 60.06/56.46 seconds.
The fixed D143 review has 46 direct bindings.

Operational continuation: sources 601--604 each run in about 4--6 seconds
with one Sage child and combined memory below 2 GiB. Retain the global
three-worker limit, 180-second private-process-group cap, 2 GiB per
worker/store and 6 GiB aggregate limit. The source-554 seed/native
admission requirements remain unchanged. No mathematical worker remains
active after this checkpoint. Follow `inherited_review` through D143 ->
D142 -> D141 -> D140 -> D139 -> D138 and the fifteen inherited catalogues
(380,188 inherited hash occurrences, 379,923 distinct files). Preserve
every earlier failure and use new numbered sources and scoped Git checks.

Potential next simplification, not a certified formula: use arithmetic
adjunction on the uncontracted orbifold model to express the cotangent
and intersection terms together in CM Hodge heights. First justify the
Wolpert metric factor and track the marked tail contractions. Good
reduction of C away from 2 does not prove that the elliptic sections
are disjoint there. D143's separate cotangent bound and conditional
analytic target remain the reviewed authority until this is proved.

<!-- D142 both P1600 height routes investigated -->

**Current reviewed checkpoint: D142 — both D141 height targets investigated; neither proved.**
The [D142 report](dembele/certificates/P1600-two-height-routes-d142.md),
[fixed review](dembele/data/computed/P1600_two_height_review_d142.json),
[completion record](dembele/data/computed/P1600_two_height_completion_d142.json) and
[source applicability ledger](dembele/data/computed/P1600_two_height_sources_d142.json)
contain the derivations and independent finite audit.

- The existing geometry now gives a proved upper bound
  `h_ext(I_2) < 83240` for the actual relation space, in the fixed
  coordinates. Joint ratio-jet bounds improve to 871 and 3532.
  This estimate does not reach the sufficient target 623; it does
  not prove that the actual height exceeds 623.
- Cauchy--Binet improves the actual Faltings upper bound to
  `h_Fal(C) < 30.039246`. The sufficient lower bound 29 remains
  unproved. The Riemann--Roch comparison now retains the metric
  conversion, finite-model difference, cotangent heights, intersections
  and analytic term with their required signs. The local cone correction
  is checked; the complete corrected global constant is not certified.

**Next proof task:** establish the finite Hodge-line comparison for the
actual normalizer and the order-3/order-32 cotangent terms, then assess
the analytic estimate required by the comparison. The report quantifies
that remaining combination; none of its unknown terms is assigned zero.
The current jet-height estimate alone cannot certify the relation-space
target. Exact structural identification remains an alternative.

D140's independent recognition stands. Exact positive vanishing, curve
identification, the later marking/Hecke/cover obligations and the field
polynomial remain open. P1600 and column 0/P6400 are unchanged. No higher
bank or numerical spectral work on C is admitted; existing search pauses
persist. All four bounded D142 jobs pass, including independent audit and
final review/replay; no D142 job failed. Sources 598--600 and the bound
artifacts are frozen; source 601 is next unused. Resource limits are
unchanged. Earlier next-task statements below are historical and
superseded by this checkpoint.

Operational continuation: no D142 mathematical worker remains active.
Final review/replay took 59.45/56.78 seconds. The new review has 38 direct
bindings; follow `inherited_review` through D142 -> D141 -> D140 -> D139 ->
D138 and its fifteen catalogues (380,188 inherited hash occurrences,
379,923 distinct files). Preserve every earlier failed attempt.
The source-554 seed/native admission requirements remain unchanged.
Use new numbered sources and scoped text Git checks. Retain the global
three-worker, 180-second private-process-group, 2 GiB per-worker/store and
6 GiB conservative aggregate limits. Source 599's Sage child shares its
capped group; its combined parent/child peak RSS was about 298 MiB.
The source ledger distinguishes the checked local cone correction from
the still-unproved global RR comparison. Neither target is a completed
identification certificate.

<!-- D141 P1600 proof-gap investigation checkpoint -->

**Current reviewed checkpoint: D141 — two precise sufficient proof targets at P1600.**
The [D141 report](dembele/certificates/P1600-proof-gap-d141.md),
[fixed review](dembele/data/computed/P1600_proof_gap_review_d141.json),
[completion record](dembele/data/computed/P1600_proof_gap_completion_d141.json) and
[source applicability ledger](dembele/data/computed/P1600_proof_gap_sources_d141.json)
record the completed investigation and independent finite audit.
D140's independent recognition of all 91 quadrics remains valid.

- A bound `h_ext(I_2) <= 623` for the true relation space would identify it
  with the recovered space. Here `h_ext` is half the natural logarithm of
  the Gram determinant of a saturated integer basis, in the fixed 136
  monomial coordinates. The certified strict threshold is about 623.347163.
  It is independent of the lattice basis, not of the ambient coordinates.
  The candidate's height 547.226455 does not bound the true space's height.
- A proved `h_Fal(C) >= 29`, in D118's normalization, would make all three
  exact-vanishing tests succeed at the existing P1600 precision. Their
  critical values are approximately 27.304628, 27.749242 and 28.084617.
  This is compatible with the known upper bound 30.970856; the proved
  lower endpoint remains about -23.146370. D120's negative conclusion
  at P200 does not carry over unchanged to the completed bank.

**Neither missing height bound is proved.** Exact positive vanishing,
candidate identification and the field polynomial remain open, as do
the later marking, canonical Hecke and cover/torsion obligations.
Shorter recovered equations improve the old sufficient section thresholds
by only nine valuation units and cannot close that gap by themselves.

**Next proof task:** derive a corrected arithmetic Riemann--Roch comparison
for the actual normalizer curve, retaining finite-model, elliptic-fibre,
metric and analytic terms. Assess whether it can prove the Faltings height
above 28.084618 before admitting numerical spectral work. A true
relation-space height bound at most 623 remains an alternative.
Existing spectral, new-level, Hecke-bank and cubic-search pauses persist.
No higher bank is admitted; P1600 and column 0/P6400 remain unchanged.

Four bounded jobs pass, including independent audit and final review/replay;
two diagnosed failed attempts remain preserved. The review binds 48 direct
sources and traverses D140, D139, D138 and fifteen inherited catalogues
(380,188 hash occurrences, 379,923 distinct files). Sources 593--597,
the report and bound artifacts are frozen; source 598 is next unused.
The three-worker, 180-second, 2 GiB per-worker/store and 6 GiB summed-RSS
limits remain unchanged. Earlier next-task statements below are historical
and superseded by this checkpoint.

Operational continuation: D141 is complete and no D141 mathematical job
remains active. Final review and replay passed in 59.24 and 58.28 seconds.
Follow `inherited_review` through D141 -> D140 -> D139 -> D138, then all
fifteen catalogues; the new 48 direct bindings do not replace that graph.
A future source-554 seed admission still needs D138's direct seed/native
closure. Preserve the source-593 conservative-Pluecker comparison failure
and source-595 rational-LDL pivot failure, including both source snapshots.
Use new numbered sources for further implementation and scoped text Git
checks because broad status/diff triggers sandboxed LFS. The source ledger
records the literature versions and the unresolved cone-constant correction;
do not substitute a modular self-intersection for a Faltings height.
The next task is the comparison derivation, with no new bank or spectral
calculation authorized by this checkpoint.

<!-- D140 independent P1600 recognition checkpoint -->

**Current reviewed checkpoint: D140 — P1600 independently recovers all 91 candidate quadrics.**
The [D140 report](dembele/certificates/dyadic-P1600-recognition-d140.md),
[fixed review](dembele/data/computed/dyadic_P1600_recognition_review_d140.json) and
[completion record](dembele/data/computed/dyadic_P1600_recognition_completion_d140.json)
record successful discovery without reading the old candidate equations.
One nonanchor CM chart, orders 0–2, and only 96 of 180 usable binary digits
recover 91 independent integer quadrics; an independent 160-digit run agrees.
Their largest coefficients are 968 and 981. Exact unimodular changes of
basis identify both recovered lattices with the old saturated candidate
lattice. Each basis passes all 6,188 independent coefficient checks,
including 5,915 structurally withheld coefficients, with zero mismatches.

There is also an exhaustive coefficient-height certificate: every integer
relation in the 160-digit congruence lattice with maximum absolute
coefficient at most 223,818,092,532,287,707,686,732,450,725,941,069 lies in
the recovered 91-dimensional rational space. This follows from exact Gram
determinants and the full lattice basis; it is stronger than testing the
LLL output. The actual canonical ideal has not been proved to admit
91 integral quadrics below this bound in the fixed residue coordinates.

**Next research task: justify that true-ideal height hypothesis, or identify
the recovered curve by an exact structural argument.** P1600 suffices for
equation recognition. D139's recommendation to make P3200 the default next
action is superseded; its costs remain planning scenarios. No higher bank
is admitted or launched. Exact positive vanishing, marked-base/canonical
Hecke identification, the later cover/torsion construction and the field
polynomial remain open. D138's section-bound gaps and the conditional
P10552 target are unchanged.

Eleven input jobs and both final review/replay jobs pass. Three diagnosed
interface failures are preserved with their logs and source snapshots.
The review binds 80 direct sources and transitively replays D139, D138 and
380,188 inherited hash occurrences (379,923 distinct files). Sources 583–592,
the D140 report and bound artifacts are frozen; source 593 is next unused.
The three-worker, 180-second, 2 GiB per-worker/store and 6 GiB summed-RSS
limits remain unchanged. Earlier next-task statements below are historical
and superseded by this checkpoint.

Operational continuation: no D140 mathematical job remains active. The
review and replay passed in 64.21 and 59.39 seconds. Traverse D140's
`inherited_review` to D139, then D138 and its fifteen catalogues; the
80 direct bindings are not a replacement for that graph. A future
source-554 seed admission still needs D138's direct seed/native closure.
P1600 remains the full bank and column 0 retains P6400.

Sage works for these bounded local matrix jobs through the installed
application's `Current/venv/bin/python3`, with `Current/local/bin` and
`Current/venv/bin` prepended to the child's PATH and DOT_SAGE set to
`/private/tmp/dembele_P1600_recognition_sage`. Source 586 records the full
paths; the old global launcher and application installation were not
modified. The waiting parent and Sage child share the capped process group,
and their conservative combined RSS is checked. Keep all three failed
attempts and use new numbered sources for any further implementation.
The next mathematical step needs a height or identification mechanism;
another precision bank is not automatically warranted by recognition.
Use scoped text Git checks because broad status/diff triggers sandboxed LFS.

<!-- D139 indexed receipt and cost checkpoint -->

**Current reviewed checkpoint: D139 — bookkeeping controls, revised costs and final replay pass.**
The [D139 report](dembele/certificates/dyadic-indexed-recost-d139.md), [fixed review](dembele/data/computed/dyadic_indexed_recost_review_r2_d139.json) and [revised cost model](dembele/data/computed/dyadic_indexed_bank_recost_r2_d139.json) record the bookkeeping work following D138. The [completion record](dembele/data/computed/dyadic_indexed_recost_completion_d139.json) confirms six passing bounded jobs; the one diagnosed review-parser failure is preserved.
The new lookup matches all 13,176 checked production receipts. A copied
422-record archive completes in 0.6803 seconds versus the original recorded
157.6806 seconds; both archive interruption/recovery controls pass. The new
coordinator preserves the mathematical schedule and requires a separate,
hash-bound bank admission. Completed arithmetic stores remain frozen.

The recommended next scope is the full P3200 checkpoint: lift columns 1–15,
reuse column 0/P6400, and validate integrated timing after the first column.
Planning scenarios are 38.7–45.7 active hours and 5.0–6.9 GiB additional
retention, with 16.9 GiB free including a 10 GiB reserve. Observed free space
is 54.55 GiB. The remaining staged conditional P10552 bank is 20.8–29.4
active days and 51.4–62.0 GiB additional retention, needing about 72 GiB free.
These are empirical scenarios, not runtime bounds or calendar ETAs. No
P3200-or-higher bank is admitted; a new scope decision and stage-specific
admission/replay are required. Existing three-worker/180-second/2 GiB limits
remain unchanged, and no frozen artifacts are deleted.

The mathematical checkpoint remains D138: full bank P1600, column 0/P6400,
91 quadrics compatible at 17 CM points, zero certified mismatches. Exact
positive-order vanishing, candidate/cover identification and the field
polynomial remain unproved; the conditional target and D134 hypotheses stay
conditional. Source 580 supersedes source 579's first cost calculation.
The failed source-581 review was a phase-name parser error, preserved with
its log and source snapshot; corrected source 582's independent review and full replay pass.
Sources 576–582, the candidate coordinator, report, models and controls must
remain unchanged. Source 583 is next unused. Earlier next-task instructions
below are historical and superseded by this status.

Operational continuation: D139 is complete; review and replay took 70.40
and 69.55 seconds, respectively. No D139 worker remains active. The review graph follows
`inherited_review` to D138, then its fifteen `inherited_catalogues`; do not
replay only D139's 1,298 direct source bindings. Preserve the source-581 failed
review receipt and the source-579 superseded model. The new coordinator is
`run_d139_indexed_production.py`; no current admission allows it to launch.
A future source-554 seed admission must preserve D138's direct seed/native
closure, since D139's review is a transitive bookkeeping graph rather than a
replacement flat seed catalogue. Next preparation after a scope decision:
column-1 CM adapter, new stage-specific audit/review, bounded graph-replay
shards, and the first-column timing gate. Broad Git status/diff still hits the
sandboxed LFS path; use scoped text checks.

<!-- D138 completed P1600 comparison checkpoint -->

**Current reviewed checkpoint: D138 — the full P1600 bank and comparison are complete.**
The [D138 report](dembele/certificates/dyadic-precision1600-bank-d138.md), [fixed review](dembele/data/computed/dyadic_precision1600_review_d138.json) and [completion record](dembele/data/computed/dyadic_precision1600_completion_d138.json) supersede the running/ETA notes below.
All sixteen columns are certified at least to P1600; column 0 retains P6400.
The fourteen-column D137 run finished 2026-10-07 at 2:36 p.m. Eastern after
22.05 hours, passing 92,946 bounded production/archive/audit/review jobs.
D138's 22 bounded assembly/control/comparison/provenance/review jobs also pass.
The earlier namespace startup failure remains preserved; no revision-2
arithmetic or D138 job failed. The completed coordinators must not be rerun.

All 91 candidate quadrics remain compatible at 17 CM points through orders
0–3. Independent integer-quotient arithmetic checks all 6,188 coefficients
and reports zero certified mismatches. Degree-16 lower bounds are
`[6594, 6545, 6528]`, anchor bounds `[6376, 6048, 5784]`; the remaining
sufficient-bound gaps are `[18561, 18724, 18848]`. Both sets of lower bounds
improved by 1600 from P800. Positive exact vanishing, candidate/cover
identification and a field polynomial remain unproved. Orders 2 and 3 retain
their previous-order exactness conditions; D134's hypotheses remain open.

The final replay checks 380,188 inherited hash occurrences (379,923 distinct
files) through fifteen immutable catalogue roots; the new flat source list
has 315 direct bindings. Sources 569–575, `run_d138_manifest_rechecks.py`,
the report, all passing artifacts and the review are frozen. Source 576 is
next unused. Keep the three-worker/180-second/2 GiB limits. No higher bank
is admitted. Next remove the growing directory-wide receipt-lookup overhead
with bounded controls, then re-cost the next precision stage before a new
scope decision. Do not use the old 15–18-hour forecast as an actual runtime.

Operational continuation: no D137/D138 mathematical job remains after the
completion record above. The new `sources` list is intentionally incremental;
full replay must also traverse `inherited_catalogues`. The flat list retains
current state/CM seeds and the frozen source-554 engine's immutable dependency
bindings for a separately admitted next stage. Do not mutate any sealed store
or frozen source to optimize lookup; use new numbered sources and controls.
The D138 comparison uses beta precision 4096 for production balls and 8192
for the independent absolute-error checker. Common coarse centers use beta
precision 3264, with explicit reduction of the higher column-0 input.
Broad Git status/diff still triggers the sandboxed LFS path; use scoped text
checks. Source 551's repeated directory glob and the production coordinator's
per-phase attempt glob are the first performance targets.


<!-- D137 approved P1600 checkpoint running -->

**Current action: the approved full-bank P1600 checkpoint is running (D137, revision 2).**
<!-- D137 progress 2026-10-07 late morning -->
[Progress observed 2026-10-07 10:26 EDT](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_observation03.json): twelve of the fourteen new columns
(2–13) have passed their 24 independent audits and fixed review/replay;
column 14 is running and column 15 remains. Including existing columns 0
and 1, fourteen of sixteen columns now have reviewed precision at least
P1600. There have been no new worker failures since the revision-2 launch.
The revised estimate of approximately 2–3 p.m. Eastern today for the column
run still looks reasonable; common-bank comparison and final review follow.
This is an advisory forecast, not a completion claim. No additional user
decision is needed now. Earlier morning progress is retained in
`dyadic_checkpoint_bank_r2_d137_observation02.json`.

The user's 2026-10-06 “proceed” selected the recommended P1600 checkpoint;
no further scope/storage approval is needed for it. The multiweek P10552
full bank remains unapproved. The [D137 revision-2 admission](dembele/certificates/dyadic-checkpoint-revision-d137.md), [fixed review](dembele/data/computed/dyadic_checkpoint_admission_r2_d137.json) and [admission completion](dembele/data/computed/dyadic_checkpoint_admission_completion_r2_d137.json)
record passing bounded admission and replay over 94,126 hashes.
The first launch exposed the frozen store's required `_d132` suffix before
any store or arithmetic was created. Its failed receipt/log/snapshot and
original configurations are preserved; revision 2 fixes only the interfaces.
The actual revised column-2 storage-creation preflight passed before relaunch.

[launch record](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_launch01.json); [live coordinator log](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_run01.log). Started 2026-10-06T20:33:48.236162+00:00 under a detached coordinator,
with idle sleep inhibited only while it runs. Columns 2–15 are lifted
sequentially from P800 to P1600; existing columns 0/P6400 and 1/P1600 are
reused. Every column gets 24 independent audits and fixed review/replay.
At most three mathematical jobs run globally, with the unchanged 180-second
wrapper, 2 GiB per store/worker measured-RSS admission and 6 GiB summed-RSS
limit. Do not start competing mathematical jobs while this coordinator runs.
D135 forecasts 15–18 active hours and about 3–4 GiB additional retention.
The fixed lifetime working-store bound is 141,761,896 bytes.

The bank coordinator stops after reviewed columns in
`dyadic_checkpoint_columns_completed_r2_d137.json`. Common-P1600 bank assembly,
residue-frame/quadric comparison and final review remain required within this
approved checkpoint scope. Until then the completed full-bank comparison
remains P800. No new exact quadric vanishing, curve identification or field
polynomial is claimed. Earlier “scope decision pending/no run started” notes
below are historical and superseded by this authorization and launch.

Latest startup observation: [first solve/check/archive cycle passed](dembele/data/computed/dyadic_checkpoint_bank_r2_d137_observation01.json); the column is continuing beyond `ready000`. This is a running snapshot, not a completed P1600 column certificate. Concurrent worker progress messages may share a log line; parse marker-delimited JSON or use individual receipt files rather than assuming one JSON event per line.

Operational continuation: the frozen current coordinators are
`run_d137_bank_r2.py`, `run_d137_production_r2.py`, and `run_d137_audits.py`;
independent arithmetic is source 564, column review is source 568, and revised
admission is source 567. Sources/reports/configs bound by either D137 admission
must not be edited. Source 569 is next unused. Current config names end
`_config_r2_d137`; store namespaces end `_r2_d132`; output stems end `_r2_d137`.
Preserve all failed/partial attempts. A failure stops admission; inspect before
resuming. The single old failed `create` attempt is explicitly classified as a
namespace startup failure, not a failed arithmetic equation. Do not rerun a
completed coordinator or launch a second instance. Read the log and check the
bank lock/process tree first. Broad Git status/diff still hits the sandboxed
LFS path; use scoped text checks.


<!-- D136 reviewed target-chart checkpoint -->

**Current reviewed checkpoint: D136.**

All 17 integrated P10552 CM chart controls and independent review/replay pass. The largest observed job peak is 1,914,568,704 bytes (1.783 GiB), and the longest job takes 69.749 seconds. The controls use synthetic compatible high digits; they certify no new harmonic precision. Independent byte checks cover all 1,740,800 old CM scalar overlaps. The lossless P6400 CM metadata adapter now supplies the reference interface for the existing weighted seed. Review binds 94,006 hashes, preserving all 93,928 D135 bindings. Freeze sources 562/563, run_d136_chart_controls.py, the passing controls, adapter and reviews. No mathematical worker from this work remains active, and no actual bank has launched. Certified precisions remain P800 for the full bank, P6400 for column 0 and P1600 for column 1. Next prepare lower-column CM adapters and bounded bank provenance review. The D135 scope/storage question is still pending: recommended P1600 checkpoint 15--18 active hours and 3--4 GiB, versus the full target bank at 22--31 active days with at least 80 GiB free after incremental-review design. Source 564 is next unused. Keep all frozen artifacts and the existing three-worker/180-second/2 GiB limits.

See the [target-chart report](dembele/certificates/dyadic-target-charts-d136.md), [cost report](dembele/certificates/dyadic-bank-recost-d135.md) and [completion record](dembele/data/computed/dyadic_target_chart_completion_d136.json).

<!-- D135 reviewed bank-cost checkpoint -->

**Previous reviewed checkpoint: D135.**

D135 cost analysis and independent review/replay pass, preserving all 93,912 D134 hashes. The staged target bank is estimated at 22.0--30.5 active days with at most three workers; these are empirical scenarios, not an ETA or admission. Incremental reviews would put additional retention at about 53--65 GiB; plan for at least 80 GiB free, versus roughly 51 GiB observed. A full-bank P1600 checkpoint is estimated at 15--18 hours and 3--4 GiB. Direct P800/P1600-to-target stores violate the unchanged 2 GiB cap. Next resolve target CM peak memory, seed/CM metadata interfaces and bounded incremental review; a scope/storage preference has been requested from the user. No new harmonic stage or bank has launched. Certified precisions remain P800 for the full bank, P6400 for column 0 and P1600 for column 1. Sources 560/561 and reviewed artifacts are frozen. D136 source 562 is running the finite 17-chart synthetic target-memory controls; source 563 is its drafted review/CM adapter. Source 564 is next unused. Inspect the D136 receipts and control lock before any other mathematical job. Preserve every earlier freeze and the three-worker/180-second limits.

See the [cost report](dembele/certificates/dyadic-bank-recost-d135.md) and [completion record](dembele/data/computed/dyadic_bank_recost_completion_d135.json).

<!-- D134 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D134.**

D134 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. The D134 replay and both reviews pass; its fixed review binds 93,912 hashes and preserves the D133 catalogue. The conditional route uses the odd canonical Jacobian order to fix the F-rational branch half, then D77 cubic inertia to fix its scalar. The marked-base and canonical Hecke hypotheses remain essential. The continuation coordinator has no further mathematical jobs after this checkpoint. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](dembele/certificates/arithmetic-twist-classification-d134.md) and [completion record](dembele/data/computed/arithmetic_cover_criterion_completion_d134.json).

<!-- D133 reviewed continuation checkpoint -->

**Previous reviewed checkpoint: D133.**

D133 is reviewed. The full bank remains P800; column 0 is now certified at P6400 and column 1 at P1600. No positive exact zero, base identification or field polynomial is proved. All 24,577 D133 input jobs and both reviews pass. The fixed review binds 93,638 hashes. The completion coordinator next runs the D134 finite replay and review; inspect its live session and receipts before starting any other mathematical job. Re-cost the complete measured stage before selecting a full-bank schedule; no new bank is automatically admitted. Source 560 is next unused. All earlier next-task statements below are historical; retain every frozen artifact.

See the [report](dembele/certificates/dyadic-precision6400-d133.md) and [completion record](dembele/data/computed/dyadic_precision6400_completion_d133.json).

## Resumed execution — 2026-10-05

At the user's request, D133 resumed from `low_begin_010` on the original
macOS ARM64 host. Before launch, all 28,976 retained files (12,170,078,912
bytes) and all 289 external dependencies matched their saved hashes;
together these cover all 18,589 frozen D132 sources. Native libraries
loaded, all three locks were free, and an unsandboxed process check found
no mathematical workers. See the [preflight record](dembele/checkpoints/d133-resume-2026-10-05-preflight.json).

The [resumption record](dembele/checkpoints/d133-resume-2026-10-05.json)
records production PID 59189 and continuation PID 59190, started in separate
sessions with durable [production](dembele/checkpoints/d133-resume-2026-10-05-production.log)
and [continuation](dembele/checkpoints/d133-resume-2026-10-05-continuation.log)
logs. Both locks were held after the launching command exited. Production
reused the 2,682 saved production/archive receipts. The [startup observation](dembele/checkpoints/d133-resume-2026-10-05-startup-observation.json)
authenticates the first 68 new passing correction-10 receipts and their
driver/log/metadata bindings, for 2,750 passing receipts at 16:22:39 UTC.
PIDs and this statement are observations,
not proof that processes remain alive: inspect locks, logs, receipts and
orphan workers before any restart. Do not start duplicate coordinators.

The unchanged continuation waits for sealed production, runs the 24 D133
audits and fixed review/replay, then executes and reviews D134. Keep at most
three mathematical workers, 180-second private-process-group caps, one BLAS
thread, the 2 GiB per-store cap and existing measured-RAM admission rules.
All frozen sources and historical evidence remain unchanged. No full-bank
launch follows. Re-cost the completed stage after D133/D134 review.

Certified precision remains full bank P800, column 0 P3200 and column 1
P1600 until the new review passes. Source 560 remains next unused. The
September 30 transfer inventory describes the pre-resumption mutable store;
its old journal/payload entries cease to describe the live store as work
advances. Preserve that inventory and all old checkpoint evidence.

Magma works locally and on Chatelet as checked on 2026-10-05. Installing
Rosetta restored local V2.29-8. Adding the missing YR1 intermediate and the
user's fresh account key restored Chatelet access, now V2.29-10. Local smoke
and field checks pass; remote file upload/execution/cleanup and inline field
checks pass. See the [local test](dembele/checkpoints/magma-access-2026-10-05-local.json),
[remote test](dembele/checkpoints/magma-access-2026-10-05-remote-restored.json)
and [setup notes](remote_magma/README.md). Earlier access/backup-key records
describe the resolved authentication outage. Both keys were rejected before
the user supplied the replacement in their own Terminal. D133's coordinator
was held while existing workers drained for each test and resumed afterward;
the recorded local and remote holds were 3.719 and 4.897 seconds.

## Historical stopping point — 2026-09-30, transfer to dots

D133 is deliberately **paused before `low_begin_010`**, after correction 9
and its verified metadata archive. The journal is `ready009`, epoch 20,
`(u,count,bits)=(3497,2903,363)`, with no pending transaction. Production
and continuation are stopped; older claims below that they are active
are historical. All 2,682 saved production/archive receipts pass. Three
interrupted attempt-01 logs are preserved with passing attempt-02 recovery
receipts. All current state/residual full and row hashes, receipt/log/metadata
bindings, and all 18,589 frozen D132 source hashes were checked.

Read [CHECKPOINT.md](CHECKPOINT.md) for Git LFS retrieval, transfer-integrity
verification, native dependencies, and the exact resumption procedure.
The [pause record](dembele/checkpoints/d133-stop-before-010-2026-09-30.json)
is operational evidence, not a P6400 certificate. D133 final verification,
24 audits and review/replay, plus D134 sources 558/559, remain pending.
Certified precision stays full bank P800, column 0 P3200, column 1 P1600.
Source 560 remains next unused. No further computation or full-bank launch
is part of this transfer checkpoint.

The frozen execution currently requires the original absolute paths and
macOS ARM64 GMP/FLINT libraries. On a different host, preserve frozen bytes
and create a reviewed portability adapter/new driver before executing it;
do not rewrite old receipt paths or rebuild frozen libraries in place.
The user requested this stopping point, commit and push to continue with dots.

## Session-close snapshot — 2026-09-29, 11:34:55 UTC

The user requested a durable handoff before closing this session. The
[saved observation](dembele/data/computed/dyadic_close_session_snapshot_d133_20260929.json)
records 2,493 production/archive receipts reporting pass, no failed receipt,
and maximum job duration 28.544548 seconds. The seed and corrections 1--8
are committed; correction 9 is underway. The observed checkpoint is
`ready008`, epoch18, with `(u,count,bits)=(3464,2936,367)`.
This is an intermediate snapshot, not a new mathematical certificate.

Both coordinator locks were held and both tool sessions responded:
production `37950`, continuation `32689`. They have been left running.
Their survival after closing this session has not been verified, and these
tool-session IDs may not be usable in a new session. Durable files and
current locks, not these historical IDs, determine how to resume. Later
completion records and the continuation's newer documentation take precedence
over this snapshot. No frozen source, receipt or earlier store was changed.

### Resume procedure

1. Read this handoff and inspect the current records under
   `dembele/data/computed/`, especially
   `dyadic_staged_P6400_col00_d133_completed.json`,
   `dyadic_precision6400_audit_plan_d133_completed.json`,
   `dyadic_precision6400_completion_d133.json`, and
   `arithmetic_cover_criterion_completion_d134.json`.
   At this snapshot none of these completion stages had finished.
2. Inspect the production lock `dyadic_staged_P6400_col00_d133.lock` and
   continuation lock `dyadic_precision6400_completion_d133.lock`. File
   existence does not mean a lock is held; use a nonblocking advisory-lock
   probe. Never remove a lock file to bypass another coordinator. If an
   owner remains active, follow its receipts instead of starting a duplicate.
3. If production is incomplete and has stopped, first establish that its
   in-flight workers have finished or stopped; a free coordinator lock alone
   does not exclude orphan workers. Inspect retained logs, receipts and the
   working journal. Then resume the production command below, preserving
   passing receipts and every interrupted/failed attempt. Start the
   continuation only after production holds its lock. Do not start the
   continuation alone against an incomplete, inactive production run: it
   intentionally refuses that state.
4. If production is complete and sealed, never rerun it. Let an active
   continuation finish; if none is active and there is no in-flight work,
   resume `python3 dembele/pari/run_d133_completion.py`. It reuses passing
   audit/review receipts and identical generated artifacts. A failed receipt,
   partial output without a passing receipt, or mismatched artifact needs
   diagnosis; the chain does not blindly retry it.
5. After D133 and D134 both have passing review and replay receipts, re-cost
   the complete measured stage before selecting a bank schedule. The
   conditional cover criterion still requires the marked base and canonical
   Hecke interpretation. No full-bank launch or field construction follows
   automatically. Source 560 remains next unused.

At closure, certified precision is still full bank P800, column 0 P3200,
column 1 P1600; sources 556--559 have not run their arithmetic/reviews.
The six continuation fixture controls have passed, and their bound source
must remain unchanged. Keep at most three mathematical workers globally,
the unchanged 180-second private-process-group cap, one BLAS thread,
the existing storage/RAM admission rules, and all prior freezes.

## Historical D133 execution checkpoint — one actual P=6400 column, 2026-09-29

D132 is fully reviewed below. Continue the admitted P=3200-to-P=6400
column-0 execution using frozen source 554 and coordinator 553. Its
[configuration](dembele/data/computed/dyadic_staged_P6400_col00_config_d133.json)
is frozen in the D132 review. The engine/storage version remains D132;
D133 names the new actual execution. Only the new
`dyadic_rowjournal_P6400_col00_d132` namespace is transient. All earlier
frozen stores, sources and certificates remain read-only.

The initialization coordinator completed its planned pause at
`--stop-before low_begin_000`: all 176 phases passed, including all 174
extension rows. The [pause record](dembele/data/computed/dyadic_staged_P6400_col00_pause_d133.json)
binds those receipts and the historical initialization state. The full
coordinator is now running in session `37950`, reusing those receipts;
the seed low system passed at 200, 400, 600 and 800 bits, with all 44,544
original equations checked at each stage. Its seed sweep and corrections
1--8 committed successfully; correction 9 is in progress at this update.
The session-close receipt census has 2,493 passing receipts and no failure;
maximum recorded job duration is 28.544548 seconds. This is an intermediate
observation, not the final D133 precision certificate.
Inspect the live session, lock and
saved receipts before any restart. Its command is:

```sh
python3 dembele/pari/553_dyadic_staged_archiving_coordinator.py --config dyadic_staged_P6400_col00_config_d133 --workers 3
```

Resume existing passing receipts and durable rows; preserve failed or
interrupted attempts. Never run a second coordinator concurrently for this
configuration or rerun a completed coordinator. Continue through all 96
corrections, every original weighted equation and mass, old overlaps,
seventeen CM charts and all 68 coarse values. Then independently review
D133 before claiming P=6400. Sources 556 (independent arithmetic) and 557
(final provenance/phase review) are drafted, with the 24-job
[audit plan](dembele/data/computed/dyadic_precision6400_audit_plan_d133.json)
and `run_d133_audits.py`. These drafts are syntax checked, not executed or
frozen; do not run the audits until the actual store is sealed and its
coordinator is complete. The expected actual
schedule has 24,456 phases and 97 archive jobs, followed by 24 audits and
fixed review/replay. A hard job failure, excessive measured RSS or rejected
reservation requires diagnosis before any later group is admitted.
Frozen coordinator 553 may drain the already queued current group;
the draft audit coordinator uses a bounded submission window instead.
Reduce a failing job without changing frozen sources or raising caps.

While D133 runs, the [D134 draft](dembele/certificates/arithmetic-twist-classification-d134.md)
now restores D77's existing exact B3 fibre/inertia criterion: it selects
one F-scalar twist after the half and B3 are identified. D130's local
counterexample remains valid, but its separate twist gate was too broad.
There is a further conditional algebraic route: the canonical Hecke order
P16(32)=1640801490553691915934375 is odd. Once the marked base is identified,
good reduction at31 gives Jac(C)(F)[2]=0, so the F-rational branch half is
unique. D77 then fixes the scalar. This can replace a separate geometric
character-continuation proof, provided the arithmetic base/marks and
canonical Hecke interpretation are established. No such identification
has yet been proved. The field/Y-section obligations remain open.

Sources 558/559 now draft the B3 witness and odd-order replay/review:
`558_arithmetic_cover_criterion.py` and
`559_arithmetic_cover_criterion_review.py`. They are unrun. The earlier
unit-classification prototype was replaced before execution. Sources 556/557
remain the pending P6400 audits/review. Source 560 is next unused. Keep
the global worker limit; D134 must not interrupt the active computation.
The draft audit coordinator submits at most three jobs at once and stops
new submissions after a failure; frozen553 queues the whole current
sweep, a limitation to address before future runs.

An unattended continuation is now active in session `32689`:

```sh
python3 dembele/pari/run_d133_completion.py
```

It waits for production's lock to release, then requires the completed
summary and sealed store. It runs the 24 audits, prepares the measured
D133 report/ledger, runs fixed review and replay, updates all seven entry
documents and writes completion. It then runs source558 and D134's fixed
review/replay, again updating documentation and completion. It never
starts production or a bank, retries a failed job, or raises caps. Keep
all manual mathematical jobs out of this chain until it completes.
Inspect both sessions/locks/receipts before any restart; a production
failure stops the continuation instead of being treated as completion.

The [six operational fixture controls](dembele/data/computed/dyadic_continuation_controls_d133.json)
pass: real-lock ordering, refusal after incomplete/failed inputs, reuse
and log authentication, idempotent linked documentation, and preservation
of fixed artifacts. These are bookkeeping controls, with no mathematical
driver launched and no P6400 or D134 precision/identity claim. Their
source hashes are to be preserved by reviewer557. The continuation's
source is already bound by this control record; do not edit it in place.

At most three mathematical workers globally, unchanged runner 272
180-second private-process-group caps, assertions and one BLAS thread.
The one-store bound is 973,167,872 bytes below the 2 GiB cap. RAM admission
is at most 2 GiB measured per successful job and at most 6 GiB for three
workers; it is not an OS hard limit or proof of free physical memory.
No automatic sixteen-column bank follows. Re-cost from the complete
actual stage before choosing the next bank schedule.

In that re-costing, compare full coordinator wall time as well as capped
job durations. Static inspection found a full computed-directory glob for
each attempt lookup in frozen553 and again per archive item in frozen551.
This is an unmeasured scaling concern as permanent receipts accumulate,
not an established runtime bottleneck. A future coordinator should use
direct attempt paths/indexing together with the bounded submission window;
do not alter either frozen source during this run.

Until final D133 certification, the certified full bank stays P=800,
column 0 P=3200 and column 1 P=1600. No positive exact zero, candidate
identity or field polynomial has been established. Keep D130's arithmetic
cover/Y-section obligations explicit. Continue autonomously; no approval
is needed for the admitted one-column execution.

## Completed checkpoint — D132 staged driver reviewed, 2026-09-28

Read the [report](dembele/certificates/dyadic-staged-integration-d132.md),
[ledger](dembele/data/computed/dyadic_staged_integration_sources_d132.json),
[fixed review](dembele/data/computed/dyadic_staged_integration_review_d132.json)
and [completion record](dembele/data/computed/dyadic_staged_integration_completion_d132.json).
All 471 input jobs and both reviews pass; no bounded failure. Review 555
binds 18589 hashes, preserving all 16567 D131 hashes. Creation/replay take
18.707/10.910 seconds. Both control coordinators completed. Freeze 547--555,
all bound artifacts/reports, the P800 and low1319 sealed stores and the
P6400 configuration, preserving every earlier freeze. D133 working files
are not part of the sealed control stores.

The complete known P=800 replay has 432 phases and twelve corrections.
All 1,113,600 uniform/weighted coordinates, 174 masses, 217,600 CM scalars
and 68 coarse values match frozen references. Initialization uses weighted
representatives directly with exact masses; no uniform output is retained.
The actual seed uses two 50-bit low digits. The seven-stage target control
reaches 1319 bits with the same resumable phases, checking all 44,544
original low equations per stage and matching all 7,349,760 D130 answer
bytes. No larger factor is built. These controls do not raise precision.

Seven actual workers are intentionally interrupted at initialization,
low-RHS completion, low-answer writing, state preparation, residual writing,
coarse publication and final sealing. All recover. An eighth interruption
tests verified metadata archival. Completed internal job records retire
only after identical external records, passing receipts and log bindings
are checked. All external records remain frozen. No power-loss/hardware
claim is made. Independent ordinary audits check 72 state, 72 CM and
48 target low scalars; full comparisons are distinct from these samples.

The live-file inventory includes initialization, digit solves, journals,
residual slots, CM, replacement metadata, history, archival and crash
states. With one working store and a 64 MiB reserve, bounds are
100,749,888 bytes at P800, 973,167,872 at P6400 from3200, and
2,046,552,040 at P10552 from6400. The target margin is 100,931,608 bytes.
Archival after each complete sweep is required. Existing frozen input/
factor files and permanent logs/receipts are accounted separately.
Measured RAM admission is separate; process-table/hardware-memory queries
are unavailable and interrupted-child RSS was not separately recorded.

The P800 coordinator takes 705.765 seconds; target low takes 288.818.
Summed input durations are 1628.259; longest input 24.607. Maximum measured
successful arithmetic-worker RSS is 122,978,304 bytes. These controls do
not recost the full target bank. D130's 9--14 ideal-worker-day model remains
a pre-redesign empirical baseline, not an updated ETA.

Source 554 differs from validated 548 only by configurable prior-review
provenance and its identity; review 555 checks that exact source relation.
Source 553 adds receipt-verified metadata archival to the full schedule.
D132 admits the one P6400 column now active above, not a full-bank launch.
All seven entry documents and references are updated. Earlier next-task
ordering below is historical.

## Previous completed checkpoint — D131 weighted certificate and row journal reviewed, 2026-09-28

Read the [D131 report](dembele/certificates/dyadic-weighted-journal-d131.md),
[ledger](dembele/data/computed/dyadic_weighted_journal_sources_d131.json),
[fixed review](dembele/data/computed/dyadic_weighted_journal_review_d131.json)
and [completion record](dembele/data/computed/dyadic_weighted_journal_completion_d131.json).
All 54 input jobs and both reviews pass; there are no failed bounded jobs.
Review 546 binds 16567 source hashes, preserving all 16142 from D130.
Creation/replay take 15.339/10.543 seconds. All four batch coordinators
completed and no mathematical worker remains. Freeze successful 541--546,
`run_d131_batch.py`, bound artifacts, plans/summaries, 24 sealed stores,
report, ledger and review, preserving every earlier freeze. Never rerun
completed phases or review creation. Source 547 is next unused.

**Complete weighted replay.** Source 541 checks all 174 states against
frozen D129: 4,454,400 uniform and 4,454,400 weighted scalar comparisons,
174 masses, and all 870,400 CM scalars. The certificate uses T Q=T and
Q T(w)=w to certify the uniform fixed point T(w) without retaining it.
Generation-bound manifests use streaming full hashes and selective row
hashes. No new uniform/CM binary is retained. D129 source 530 already
computed CM directly from weighted inputs; D131 adds authenticated GMP
replay. Sources 542/546 supply separate ordinary-arithmetic samples,
not a second complete independent operator.

**Recoverable updates and actual arithmetic.** Source 543 uses durable
row undo/redo records, read barriers and generation commit before retiring
correction input. Source 544 recovers 19 distinct abrupt-exit boundaries
and rejects four corruption/stale-journal cases. Its saved actual P=1600
transition and synthetic target-width rows agree byte-for-byte after
interruption. The 22 intentional child exits are passing control events,
not failed jobs; power-loss/hardware durability is not claimed.

Source 545 freshly recomputes D124's first P=1600 correction u=800 to 833:
348 original low-RHS actions, the streamed 100-bit factor, all 44,544
original low equations, and 348 new GMP correction actions. All 1,067,664
new residual coordinates and prepared state/correction coordinates match
the frozen reference. This is actual arithmetic integration at an already
certified stage, with no precision increase. All sealed control payloads
total 101,567,858 bytes. Historical overwritten/retired hashes are history,
not claims that those payloads remain retained.

**Resource scope.** Largest target logical reservation is 2,035,873,922
bytes including a 64 MiB workspace reserve and owner metadata, below the
2 GiB cap; oversized reservation is rejected before file creation. The
capacity files are sparse reservations, not filled target arithmetic.
The cap is per owned store; no aggregate concurrent-store or RAM
certificate is claimed. Source 545 peaks at 123,374,413 logical bytes.
Maximum input single-process RSS is 334,118,912 bytes. Full initialization,
multi-digit low solves, CM publication and every restart lifetime still
need integrated accounting. D130's 9--14 ideal three-worker days is a
pre-redesign empirical baseline, not a current ETA or bound.

**Next execution: complete the resumable staged driver, source 547 onward.**
Use one working store, weighted input/output, authenticated rows and the
journal. Split low-RHS actions and multi-digit low stages into separately
capped, resumable jobs. Persist authenticated low answers before updating
state rows. D130 controls seven factor stages to 1319 bits; source 545
integrates only the 100-bit solve and does not yet resume every arithmetic
phase. A complete driver must resume computation as well as recover storage.

Initialize directly from a certified weighted seed of precision S:
moment-k error pi^(S-k) times column valuation pi^k gives uniform accuracy
pi^S; account for the omitted k>=S tail and restore exact masses. Verify
old overlaps and every final Q T(w)=w equation. Supply the complete
live-file inventory and a separate concurrent-RAM budget. Select the
first actual higher-precision column only after these gates pass; do not
automatically launch another doubling or the full bank. Re-cost the full
schedule when the complete new stage supplies measurements.

**Mathematical status unchanged.** Full bank P=800, column 0 P=3200,
column 1 P=1600. All 6188 quadric balls contain zero, with no positive exact
zero; D125 bounds/anchors, uninverted W Gaussian and successive-zero
hypotheses remain. P=10552 is only a conditional sufficient design.
Exact base identification and the original-kernel polynomial are open.
Keep D130's [arithmetic construction specification](dembele/certificates/arithmetic-construction-d130.md)
on the research path: marked P32/B3, geometric double-cover character and
arithmetic twist, actual Y64 sections, combined g64/d51 torsion, global
F256 scalar action and coefficient/kernel certification remain missing.
D130's globally nonsquare, locally square unit still prevents choosing
the arithmetic twist from that local comparison and ramification support.
D120 norm-97 separation is settled; D99 nonhyperellipticity is compatible
with field existence. Preserve D108's rejection and all resource pauses.

Continue autonomously within the recorded bounds: at most three mathematical
workers globally, unchanged runner 272 180-second private-process-group
cap, assertions and one BLAS thread. Inspect receipts and partials after
disconnects before retrying. No correspondence or frozen-file cleanup.
All seven entry documents are updated. Earlier next-task ordering is historical.

## Previous completed checkpoint — D130 feasibility and arithmetic bridge reviewed, 2026-09-28

The accepted stocktake plan is executed. Read the
[feasibility report](dembele/certificates/dyadic-target-feasibility-d130.md),
[arithmetic construction specification](dembele/certificates/arithmetic-construction-d130.md),
[ledger](dembele/data/computed/dyadic_target_feasibility_sources_d130.json),
[fixed review](dembele/data/computed/dyadic_target_feasibility_review_d130.json)
and [completion record](dembele/data/computed/dyadic_target_feasibility_completion_d130.json).
All 137 input jobs and both reviews pass. One failed source-539 census
attempt is retained and resolved by attempt 02. Review 540 binds 16142
hashes, including all 15600 D129 hashes. All seven batch coordinators
returned. No worker remains. Freeze 533--540, `run_d130_batch.py`, their
successful outputs, plans/summaries, reports, ledger/review and the failed
539 snapshot/log/receipt, preserving every earlier freeze.

The full harmonic/CM bank remains P=800, column 0 P=3200, column 1 P=1600.
D125's 6188 actual quadric balls still contain zero, with no positive exact
zero. Section bounds/anchors, the uninverted W Gaussian and all successive
exact-zero hypotheses are unchanged. No candidate identity or field
polynomial is proved. P=10552 is a conditional sufficient design only.

**What D130 adds.** Seventy-four map controls yield 26 complete backend
pairs / 1,698,208 scalars, plus 22 single-backend cost controls. Seven
existing-factor digit solves reach 1319 bits, with complete original low
equations after each stage; independent ordinary audits are sampled.
Synthetic coarse CM, frame and quadric controls pass; existing eta
precision 21168 suffices. Compact zero descriptors and complete D129
weighted projections pass. A new streaming hash/row-manifest control
removes the prospective whole-file authentication allocation; the old
selective reader's inherited source helper actually calls read_bytes().
Old arithmetic is unaffected; the new reader is not yet integrated.

**Decision.** Prefer staged refinement only after redesign. The empirical
model gives about 9--14 days at ideal three-worker utilization, versus
35--61 direct; these are sample/interpolation scenarios, not bounds or
ETAs. The inherited scratch protocol needs 6.03 GB at P=6400 and 15.94 GB
at P=10552 from P=6400. The unchanged cap is 2 GiB; a target uniform state
alone is 2.424 GB. Compact uniform+CM final retention is 46.35 GB versus
104.61 GB in the old format, without fixing scratch. No further actual
refinement or bank launch is admitted by D130.

**Next executable packet: source 541 is unused.** Implement the weighted-only
certificate and replay against actual D129. D121's column-k valuation
bound gives T Q=T modulo pi^P. Thus all equations Q T(w)=w plus exact
masses certify mu=T(w), since T(mu)=T Q(mu)=T(w). Review 540 independently
checks c/delta divisibilities for all 348 original and 34 composed CM
maps. Check every retained D129 uniform/weighted coordinate and all direct
CM output against this alternative; preserve full original GMP actions
and separate ordinary arithmetic samples. This is a new certificate
implementation, not permission to modify D129 or infer a new precision.

Then implement a new prospectively transient row-journal namespace:
one weighted state; exact-low-solve correction preparation converts the
old residual into the correction input and updates state rows using durable
undo/redo records; an epoch barrier forbids mixed-generation operator reads.
The correction sweep reads that immutable input and writes one new residual,
then atomically commits a complete authenticated generation before retirement.
Bind streaming whole-file hashes once and row hashes on selective reads.
At target from P=6400, weighted state plus two largest residuals is
1,968,764,760 bytes, leaving 178,718,888 below 2 GiB. This is only a proposed
layout: inventory low solves, initialization, output buffers, WAL, failures,
CM and sealing. Inject interruptions/corruption and compare completed
old data before any actual lift. Weighted+CM final retention would be
27,055,881,600 bytes for sixteen target columns, excluding other stages.

**Keep the mathematical bridge explicit.** Exact (C,D17) does not identify
P32/B3 or the arithmetic X twist. The unit delta=1+b has norm -1, is a
square at b=27 mod31, and gives a quadratic extension unramified at finite
primes away from 2. Therefore even exact agreement at that completion
and ramification support cannot choose the global twist. D87 signs remain
numerical; D88's cubic shortcut requires the same marked arithmetic X.
Exact Y coefficients or D62 arithmetic section entries, combined g64/d51
torsion, global F256 scalar action and coefficient/kernel certification
remain missing. D120 norm-97 isolation is settled; do not reopen D100's
superseded question or resume ordinary cubic LLL without a new mechanism.

No further approval is needed for the recorded bounded work. At most three
mathematical workers globally, runner 272's unchanged 180-second private
process-group cap, assertions and one BLAS thread. Preserve frozen files,
resource pauses and original kernels. Inspect receipts and partials after
disconnects; never rerun completed coordinators/phases. No correspondence.
All earlier next-task ordering below is historical.

## Previous planning checkpoint — strategic stocktake after D129, 2026-09-28

The user requested a step back to assess progress and plan next steps.
Read the [current stocktake](dembele/certificates/stocktake-2026-09-28.md).
This is a planning update, not a new arithmetic milestone. D129 remains
the latest completed computation; no worker was launched for this review.

**Retain the dyadic integral-section route. The next major mathematical
milestone is exact identification of the genus-16 base.** D126--D129
improve the evaluator and its resource controls; they do not improve
D125's complete geometric comparison. The full bank remains P=800,
column 0 P=3200 and column 1 P=1600. All 6188 quadric balls contain zero;
no positive exact vanishing or candidate identity is proved. P=10552
is a conditional sufficient design, not a minimum or a guarantee.

Source 533 remains unused. The next bounded execution should cost the
**complete identification certificate**, including target full/RHS/extension
maps, repeated existing-factor solves, all sixteen columns, CM/frame/
quadric arithmetic, verification, review, I/O and retained outputs.
Compare staged and direct precision schedules and multiple-RHS reuse.
Control compact future retention and budget concurrent RAM separately
from scratch disk. No automatic next precision doubling or large bank:
choose the actual schedule only after the full phase/storage budget is
defensible under the unchanged caps. Preserve all frozen artifacts.

Accompany that feasibility report with the specific downstream arithmetic
construction: marked P32/B3 and double-cover character/twist; the D88
cubic shortcut's hypotheses; exact global Y64 coefficients or D62's
arithmetic section interface; the combined genus-64/degree-51 torsion
backend and global F256 action. D120 already settles norm-97 target
isolation, superseding D100 on that point. Higher precision on C does
not settle those remaining gates. Identify any missing effective
construction explicitly before describing the route as costed through
the field polynomial.

The full acceptance test is successive exact vanishing through coarse
order three, followed by the degree-60 versus degree-68 divisor argument.
A certified mismatch is a result; a zero-containing ball below threshold
is incomplete. D99 nonhyperellipticity and field existence are compatible.
Keep D108's rejected spectral comparison and D120's rejected bound detours
closed unless new mathematics or measurements justify reopening them.

No further approval is needed for the recorded bounded work. Keep at most
three mathematical workers, runner 272's 180-second private-process-group
cap, assertions and one BLAS thread. Inspect receipts/partials after
disconnects before retrying; never rerun completed phases. No correspondence.
The stocktake supersedes next-task ordering below, not accepted results.

## Previous completed arithmetic checkpoint — D129 actual P=3200 column reviewed, 2026-09-28

Continue autonomously toward Dembélé's original-kernel field polynomial.
Read the [D129 report](dembele/certificates/dyadic-precision3200-d129.md),
[ledger](dembele/data/computed/dyadic_precision3200_sources_d129.json),
[fixed review](dembele/data/computed/dyadic_precision3200_review_d129.json)
and [completion record](dembele/data/computed/dyadic_precision3200_completion_d129.json).
**All 1934 input jobs and both reviews pass. Review 532 binds 15600 hashes,
preserving all 9648 D128 hashes. Column 0 reaches P=3200, column 1 P=1600;
the complete bank remains P=800. Exact positive vanishing, candidate
identification and the target field polynomial remain open.** All state,
check and finalization schedulers have returned; the seven entry-point
documents are updated. The completion record's pending flag records the
state at its creation, before these documentation updates.

Sources 528--529 perform 1905 capped jobs: one writer control and 1904
arithmetic phases, including 48 corrections and 101 sweeps. The residual
bound rises from 1600 to 3184. Full GMP reconstruction and the separate
original residual check all 4,454,400 scalars, 2,227,200 old low overlaps,
4,454,400 extended old overlaps and 174 exact masses. The actual 400-bit
seed low solve reuses the old 200-bit factor through exact residual
division; no new factorization is built. Source 530 supplies all 870,400
CM scalar coefficients and beta-errors [6432,6448,6432,6464]. Its six
chunks total 43,520,000 bytes and are not duplicated at assembly.

Source 531's 22 audit jobs independently check retained zero residuals,
all weighted coordinates, old state/CM overlaps, all 68 coarse values,
sampled ordinary state/CM recurrences, 101 sweep coverages and 49 checkpoint
records. Sixteen high-seed recurrence blocks retain 5,120,000 bytes.
Retired intermediate payloads are explicitly not replayed. Final correctness
uses the original fixed-mass contraction certificate, not historical hashes.

The enforced 2 GiB scratch cap covers a conservative 1,510,359,376-byte
inventory. Observed peak is 1,229,041,837; 103 barriers retire 1950 files
totalling 9,302,747,376 bytes. Four retained payloads total
558,829,536 bytes; sealed occupancy is 558,830,756. Review 532
replays all live sets and exact sizes. Row writes reserve complete lengths
under the shared lock; maximum serialized row is 1,280,000 bytes. No earlier
frozen file changes. No injected-crash or aggregate-RAM certificate is claimed.

Coordinator time is 4245.664 s; summed input durations
11115.625 s; longest input 94.767 s. Maximum single-process
input peak is 491,929,600 bytes. Review creation/replay pass in
13.333/9.531 s. Freeze 528--532, `run_d129_checks.py`,
`run_d129_finish.py`, all successful artifacts and permanent records,
sealed scratch, report and ledger, plus all earlier freezes. Never rerun
completed phases, coordinators or review creation. After a disconnect,
inspect saved receipts and partials before choosing any retry.

**Next execution: source 533 is unused.** Cost P=10552 original child-map
actions in full, low-RHS and seed-extension shapes, splitting by child and
backend where required. Compare adaptive/GMP outputs and available old
actual overlaps; label synthetic and sampled results precisely. Control
multi-digit exact residual lifting with the existing factor: at most
200 bits per solve, seven stages for the target's 1319-bit low modulus.
Compare staged refinement with a direct jump, including D126's measured
multiple-RHS reuse. Then provide the complete phase, scratch, permanent
storage and retained-output budget before another actual refinement.

Current four-payload retention at target size would exceed available disk
for sixteen columns. Future lossless zero-residual encoding and regeneration
of weighted projections from uniform moments need byte controls and review;
they never authorize deleting existing frozen artifacts. Keep at most three
mathematical workers, every job within runner 272's unchanged 180-second
private-process-group cap, assertions and one BLAS thread. The full target
solve and a larger full bank remain uncosted. No additional approval is
needed for the recorded bounded controls within these constraints.

D125 section bounds stay 4994/4945/4928, anchors 4776/4448/4184,
sufficient 25255/25369/25476 and gaps 20261/20424/20548. All 6188 quadric
balls contain zero; no positive exact vanishing follows. W Gaussian remains
nonzero at valuation 1024, error 2025, relative precision 1001, uninverted.
Preserve original kernels, preceding exact-zero hypotheses, D99/D108 and
all resource pauses. Marked X40/Y64, the genus-64 section and degree-51
torsion backend, global F256 action, the final invariant and original-kernel/
ramification checks remain downstream. No correspondence. Earlier next
steps below are historical.

## Previous completed checkpoint — D128 selective controls reviewed, 2026-09-28

Continue autonomously toward Dembélé's original-kernel field polynomial.
Read [the D128 report](dembele/certificates/dyadic-selective-scaling-d128.md),
[ledger](dembele/data/computed/dyadic_selective_scaling_sources_d128.json)
and [fixed review](dembele/data/computed/dyadic_selective_scaling_review_d128.json).
**All 13 input controls pass. Review 527 binds 9648 sources and preserves
all 9599 D127 hashes. The full bank remains P=800, columns 0 and 1 P=1600.
No actual P=3200 column, positive exact quadric zero, candidate identity
or field polynomial is proved.** All input and review workers have returned.

Source 525 processes serial phases one state at a time, retaining only
the fixed low system and a constant number of long rows. Eight assembly
outputs and preparations 1/12/24 match all 305,582,280 bytes of fourteen
retained D124 payloads directly. All 133,632 original sparse low equations
also pass. Assembly checks all final weighted projections, original
residual scalars, old overlaps and masses using the saved verified chunks.
It does not rerun those full original maps, write new binary payloads or
execute a complete refinement. Streaming serialization is controlled;
the future streamed file writer is not yet implemented.

The combined assembly control peaks at 365,510,656 resident bytes;
preparation controls peak at 246,841,344/184,729,600/148,029,440. These are
below the earlier approximately 1.1 GB full-array reconstruction peaks,
with different work scopes and scheduling; no elapsed-speedup claim.
Source 526 compares adaptive and GMP original-map actions at P=3200
for states 0--5, 83--88 and 168--173, in extension/full/low-RHS modes.
All 926,352 backend scalar comparisons and 230,400 old actual low overlaps
pass. Extension inputs are actual P=1600 data with exact masses; full/RHS
inputs are dense synthetic data. Eighteen states are not full coverage.
Maximum transport peak is 420,642,816 bytes. Longest input job 64.210 s;
summed input durations 450.414 s. Review creation and fixed-manifest
replay pass in 9.092/9.287 s. All 15 D128 receipts (13 inputs plus the
two reviews) pass; all logs are paired with receipts.
Freeze 525--527, their successful outputs, report and ledger, plus all
prior freezes. Never rerun successful phases or completed coordinators.

**Next execution: source 528 is unused.** Implement one actual column-0
P=1600-to-P=3200 rolling refinement. Integrate selective serial processing
and streamed row writes, initially six-state operator chunks, and the
existing P=1600 factor using D127's exact residual lift. Split correction
RHS construction into capped chunks before the low solve/state update.
The fixed low solve itself already passes at P=3200; no new factorization
is needed. Keep at most three workers and every job under the unchanged
180-second private-process-group cap, with one BLAS thread and assertions.

The prospective P=3200 scratch inventory is 1,510,359,376 bytes under a
proposed 2 GiB limit. Uniform/weighted/largest scaled payloads are
222,720,000/113,343,600/55,680,000 bytes. Reserve full output capacity under
the shared lock, stream rows, check lengths and synchronize before commit.
Retain journal-before-retirement and final sealing. The new namespace
must be explicitly temporary before launch; no earlier file may be deleted.
The future four final state payloads total 558,829,536 bytes and direct CM
adds 43,520,000; split CM by charts if needed for the cap. This is a byte
inventory, not an enforced P=3200 cap, aggregate RAM bound or full runtime
certificate. The integrated driver must supply that enforcement. Preserve
full GMP reconstruction plus separate original residual, old overlaps,
exact masses, direct CM, independent audits and a new fixed review.

D127's actual rolling P=1600 column is complete, sealed and frozen; do not
rerun its 228 phases or touch its sealed scratch. A larger full bank and
the complete conditional P=10552 solve remain uncosted. D125 bounds stay
4994/4945/4928, anchors 4776/4448/4184, sufficient 25255/25369/25476 and
gaps 20261/20424/20548. All 6188 quadric balls contain zero. W Gaussian
is nonzero at valuation 1024, error 2025, relative precision 1001, uninverted.
Keep all resource pauses, original kernels, exact-zero prerequisites,
D99/D108 and downstream marked X40/Y64, genus-64 section/degree-51 torsion,
global F256 action, final invariant and ramification checks. No correspondence.
Inspect saved receipts/partials after a disconnect. Earlier next steps
below are historical.

## Previous completed checkpoint — D127 complete rolling column and factor reuse reviewed, 2026-09-28

Continue autonomously toward Dembélé's original-kernel field polynomial.
Read [the D127 report](dembele/certificates/dyadic-rolling-pilot-d127.md),
[ledger](dembele/data/computed/dyadic_rolling_sources_d127.json) and
[fixed review](dembele/data/computed/dyadic_rolling_review_d127.json).
**All 235 input jobs pass. Review 523 binds 9599 sources, preserving all
8816 D126 hashes. Columns 0 and 1 now reach P=1600; the complete bank
remains P=800. No positive exact quadric zero, candidate identification
or field polynomial is proved.** All D127 workers have returned.

Sources 519--520 complete column 1 from P=800 with 24 corrections and
228 phases. The separate full original GMP residual checks 2,227,200
scalars; all old low/extended overlaps and exact masses pass. Source 521
certifies all 17 CM charts, 435,200 scalars and errors
[3232,3248,3232,3264]. Four source 522 independent audit phases pass.
Retired intermediate payloads are explicitly not replayed. Final masses,
original residual and the contraction/truncation proof certify moments
independently of iteration history; hashes do not substitute for this.

The scratch inventory bounds 381,534,376 bytes under the enforced
512 MiB cap; peak observed is 308,327,101. Fifty-four retirement barriers
retire 248 prospectively temporary files, totaling 1,311,643,320 bytes.
Four retained payloads total 140,237,736 bytes; the sealed directory
occupies 140,238,953. All earlier frozen files remain preserved. Review
523 independently replays every allocation/live set and barrier byte
count. The complete pilot had no interrupted/resumed phase; D126's
crash controls concerned a separate store.

State coordinator time is 1276.888 seconds; summed state phase durations
2405.241 seconds. Final assembly still peaks at 1,117,175,808 resident
bytes, so the storage improvement is not a complete RAM certificate.
Longest input job is 65.949 seconds, summed input durations 2642.670.
Creation/replay of the fixed review pass in 9.258/8.703 seconds. Freeze
519--524, all successful artifacts, permanent phase/retirement records,
the sealed scratch directory, report and ledger, plus all earlier freezes.
Do not rerun completed phases/coordinators or alter sealed scratch.

Source 524 controls exact residual lifting with an existing half-precision
factor at P=1600 and P=3200. Each checks 89,088 higher-precision sparse
equations and exact coefficient divisions; P=1600 also agrees with every
full-factor answer. The P=3200 control uses only the old P=1600 factor.
This raises low-system solve precision, not actual harmonic precision.
It removes the need to build a P=3200 low factor for the next doubling.

**Next execution: source 525 is unused.** Control selective serial
assembly and correction preparation against retained D124 P=1600 data;
then measure bounded P=3200 original-transport/RHS chunks. Prove a new
complete per-phase scratch/RAM inventory before an actual P=3200 column.
Use the existing factor through exact residual lifting. Do not infer
larger-bank or complete P=10552 cost from the current controls.

D125 section bounds remain 4994/4945/4928, anchors 4776/4448/4184,
sufficient 25255/25369/25476 and gaps 20261/20424/20548. All 6188 quadric
balls contain zero. W Gaussian remains nonzero at valuation 1024,
error 2025, relative precision 1001, uninverted. Preserve all resource
pauses, original kernels, preceding exact-zero hypotheses, D99/D108,
marked X40/Y64 covers, genus-64 section/degree-51 torsion, global F256
action, final invariant and ramification gates. No correspondence.
Keep assertions, one BLAS thread, at most three workers and 180-second
private-group caps. Inspect receipts/partials after any disconnect.
Older next steps below are historical.

## Previous completed checkpoint — D126 resource controls reviewed, 2026-09-28

Continue autonomously toward Dembélé's original-kernel field polynomial.
Read [the D126 report](dembele/certificates/dyadic-resource-controls-d126.md),
[ledger](dembele/data/computed/dyadic_resource_controls_sources_d126.json)
and [fixed review](dembele/data/computed/dyadic_resource_controls_review_d126.json).
**All 22 input jobs pass. Review 518 binds 8816 sources and preserves all
8729 D125 hashes. The full bank remains P=800 and column 0 remains
P=1600. No positive exact quadric zero, candidate identification or field
polynomial is proved.** All input workers have returned.

Source 514 selectively reads one state at a time and checks both complete
P=1600 original GMP sweeps (2,227,200 scalars each), all weighted
coordinates and exact masses. Full-sweep peak RSS is 220,938,240 uniform
and 228,753,408 weighted bytes. These are memory controls, not measured
elapsed speedups over the differently scheduled D124 jobs.
Source 515 replays 25 actual checkpoints into a new prospective store,
testing four deliberate process exits and corrupted-copy rollback.
Peak scratch is 84,954,288 bytes under 87,665,776; the final 57,768,619-byte
directory is sealed and frozen. No old frozen file was changed/deleted.
This controls storage/recovery, not a complete new arithmetic refinement.

Source 516 streams 1226 factor blocks once per solve and matches resident
two-RHS answers; sixteen RHS also pass every original sparse equation.
Peak falls from 786,153,472 to 293,371,904 bytes for two RHS. Map reuse
matches actual data. Source 517 combines selective reads, sequential
map reuse and streamed factors on all low moments for two actual P=800
columns plus the saved first P=1600 correction. Checks total 133,632 known
low scalars plus the same number of original sparse equations. All pass.
Transport arithmetic dominates: 59.828 seconds for the two-column RHS,
7.892 for the solve, out of 76.713 seconds total. Longest input job is
77.022 seconds; summed input job durations 853.240 seconds.

Freeze 514--518, all successful outputs, the sealed scratch directory,
report and ledger, plus all earlier freezes. Review creation passed in
10.579 seconds; fixed-manifest replay passed in 8.939 seconds.
No successful phase may be rerun. Scratch-history hashes are explicitly
not retained payloads and do not replace final original-equation checks.

**Next execution: source 519 is unused.** Integrate the controlled pieces
into a complete rolling P=800-to-P=1600 refinement for column 1, using
existing verified factors. Before launch, inventory every phase and
prove/enforce a 512 MiB total scratch cap including work files and chunks.
Retain final uniform state, exact masses, separate full original GMP
residual, old overlaps, direct CM and immutable receipts. Validate the
new complete arithmetic workflow before a larger precision or full bank.
No complete rolling arithmetic driver exists yet. Preserve all old files.

D125 section bounds remain 4994/4945/4928, anchors 4776/4448/4184,
sufficient 25255/25369/25476; gaps 20261/20424/20548. All 6188 quadric balls
contain zero. W Gaussian is nonzero at valuation 1024, error 2025,
relative precision 1001, and remains uninverted. The conditional P=10552
design remains uncosted as a complete solve; its uniform column alone
is 2,423,583,360 packed bytes. Geometric proofs are not machine-formalized.
Keep the 180-second private-group cap, one BLAS thread, assertions and
at most three workers. Inspect receipts/partials after any disconnect.
Keep all resource pauses, original kernels, exact-zero hypotheses,
D99/D108 and downstream X40/Y64, genus-64 section/degree-51 torsion,
global F256 action, final invariant and ramification gates. No correspondence.
Older next steps below are historical.

## Previous completed checkpoint — D125 P=800 full bank and comparison reviewed, 2026-09-28

Continue autonomously toward Dembélé's original-kernel field polynomial.
Read [the D125 report](dembele/certificates/dyadic-precision800-d125.md),
[ledger](dembele/data/computed/dyadic_precision800_sources_d125.json) and
[fixed review](dembele/data/computed/dyadic_precision800_review_d125.json).
**All sixteen actual harmonic columns reach P=800, with full original
residuals, CM values and independent audits passing. All 6188 quadric
coefficients (4641 positive) contain zero; no mismatch is certified.
No positive exact quadric zero, candidate identification or field
polynomial is yet proved.** One column also remains certified at P=1600
from D124. All completed arithmetic and coordinators have returned.

The accepted section lower bounds are **4994/4945/4928**, anchors
**4776/4448/4184**, sufficient nonanchor **25255/25369/25476**, and gaps
**20261/20424/20548**. Bounds rise by 800 from D122, while the improved
anchor lowers sufficient thresholds by 50. The global height budget is
unchanged. W Gaussian remains nonzero with valuation **1024**, improved
error **2025**, relative precision **1001**, and has not been inverted.
The candidate survives another full-bank precision doubling; finite
zero-containing balls are not exact identities.

Columns 1..15 use source 505's weighted solver, 12 corrections and 81
phases each, then source 506's direct weighted CM. Column 0 reuses D123.
The bank checks 17,817,600 original state scalars and 3,481,600 CM scalars;
coarse errors are [1632,1648,1632,1664]. Independent source 511 audits all
15 new columns: 217,152,000 weighted state scalars, 55,436,400 residual
scalars, sampled original/high-seed/CM recurrences and every coarse value.
Source 512 independently audits all 1088 assembled values, the frame,
6188 quadric coefficients, Gaussian and thresholds. Geometric proofs
remain mathematical arguments, not machine-formalized theorems.

All **1250 input jobs pass**, no failures, under the unchanged 180-second
private-process-group cap and one BLAS thread. State coordinators total
5409.946 seconds; CM phases total 196.843 seconds. The longest input job
is 69.292 seconds. Maximum single-process resident memory is 811,401,216
bytes, not an aggregate measure. Retained state checkpoints occupy
3,656,839,680 bytes. Review 513 binds **8729 sources**, preserving all
**3535 D124 hashes**. Creation and fixed-manifest
replay pass in 10.890 and 8.148 seconds. No owned job remains running. Freeze 505--513, both P=800 coordinators,
their artifacts and the bound report/ledger, plus every earlier freeze.
Do not rerun successful jobs or completed coordinators.

**Reassessment and next execution:** retain the candidate and integral-
section route, but address target I/O and storage before another larger
full-bank run. A uniform P=10552 column alone needs 2,423,583,360 packed
bytes. Current chunks decode all 174 states and keep every intermediate
checkpoint; target-size full-solve cost remains unestablished.

**514 is next unused; no D126 driver exists.** Implement a selective-read
control at the already certified P=1600, checking every weighted projection
against the frozen uniform state and selected full original GMP rows,
with isolated peak-memory measurement. Then implement and control a
bounded rolling scratch protocol, and profile factor decoding/solves
and map reuse before selecting a larger refinement. The new report proves
that exact masses plus the original residual and truncation certificate
already certify the final moments independently of iteration history:
e=T_+e mod pi^P and T_+ is pi-divisible, so iterate P times. This permits
prospective bounded scratch storage; metadata hashes do not replace final
residual verification. No existing frozen file may be deleted or changed.
No rolling scratch protocol has yet been implemented.

Keep assertions, fresh receipt names, at most three workers and the caps.
Inspect receipts/partial files after a disconnect before resuming. Keep
all resource pauses, preceding exact-zero hypotheses, D99 nonhyperellipticity,
D108 spectral rejection and the original kernels. The marked X40/Y64
covers, genus-64 section and degree-51 torsion backend, global F256 action,
final invariant and original-kernel/ramification checks remain downstream.
No correspondence. Older next tasks below are historical.


## Previous completed checkpoint — D124, 2026-09-28

Continue autonomously toward Dembélé's original-kernel field construction.
The [D124 report](dembele/certificates/dyadic-precision1600-d124.md) and
[source ledger](dembele/data/computed/dyadic_precision1600_sources_d124.json)
are complete and frozen. One actual column is certified at P=1600,
including all 17 CM charts and beta-errors [3232,3248,3232,3264]. All
242 input jobs pass; no failed attempt. Review 504 binds **3535 sources**,
preserving all **2532 D123 hashes**. Creation passed in 5.050 seconds;
fixed-manifest replay passed in 4.545 seconds. All mathematical workers and
the P=1600 coordinator have returned; do not rerun successful phases.

The 228 state phases use 24 weighted corrections and a separate GMP
reconstruction followed by every original residual equation: 2,227,200
scalar checks. All old low and extended overlaps and exact masses pass.
Coordinator elapsed time is 1713.775 seconds; peak single-process RSS
is 1,127,170,048 bytes. The factor takes 88.330 seconds, the longest job.
Four source 499 audits independently check sampled recurrences, all
coarse values, 25 weighted checkpoints and recorded overlaps. This does
not machine-formalize the geometric arguments.

New validated method: composing each CM map with the original child maps
preserves pi-divisibility of c and determinant. CM moments therefore come
directly from weighted state data without extending states through 3P.
Source 500 matches all 217,600 P=800 and 435,200 P=1600 CM scalars. Sources
502--503 control a compiled small-product path with 172 independent
products and 33,320 actual equation scalars. Production source 497 was
not modified. A synthetic P=10552 action still does not cost a full solve.

**Next execution (D125):** complete the full P=800 bank, then retest the
quadrics before another isolated higher-precision pilot. Reuse column 0's
D123 P=800 data; refine columns 1..15 from D122 P=400. Source 505 is a new
mutable draft combining the validated adaptive backend with source 497's
weighted chunks and full GMP residual. It explicitly supports older
metadata with `checkpoint_files` but no `state_file`. Its initial phase has now passed; see the active D125 block above.
Prepare a resumable coordinator and direct-CM driver; retain at most three
workers and 180-second private-process-group caps, one BLAS thread and
assertions. Freeze each source at its first successful phase. Inspect
receipts and partial outputs before resuming after a transport failure.

Accepted full-bank bounds remain D122/P=400: section lower
4194/4145/4128, anchor 3976/3648/3384, sufficient nonanchor
25305/25419/25526. No positive exact quadric zero, candidate identification
or field polynomial is proved. W Gaussian remains nonzero, valuation
1024/error1225, uninverted. Retain all freezes through 504, resource
pauses, preceding exact-zero hypotheses, D99 nonhyperellipticity and
D108 spectral rejection. No correspondence. Older next tasks are historical.


## Previous completed checkpoint — D123 P=800 pilot and weighted solver reviewed, 2026-09-27

Continue autonomously toward the original-kernel field construction. Read
[the D123 proof and measurements](dembele/certificates/dyadic-staged-pilot-d123.md)
and [the ledger](dembele/data/computed/dyadic_staged_pilot_sources_d123.json).
**One actual harmonic column now reaches P=800, including all 17 CM
charts, with coarse beta-errors [1632,1648,1632,1664]. A smaller weighted
representation and shrinking Schur correction stage reproduce it exactly.
Both independent audits pass. The full sixteen-column bank remains P=400;
no new quadric bound, positive exact zero, curve identification or field
polynomial is proved.** Both coordinators and all workers have finished.

Source 488's r=32 factor passes in 64.745 seconds, preserving every old
factor coefficient. Source 489's uniform pilot uses thirteen corrections
400 -> 433 -> ... -> 796 -> 800. All 126 state phases pass in 538.595
coordinator seconds (895.733 summed phase seconds). The full original
GMP residual checks 1,113,600 scalar coefficients; all old overlaps pass.
Source 490 extends only nine CM-target states through 2398 and all CM
moments through 1599. Source 491 independently checks the recurrences,
new seed tail and all 68 coarse values in 33.996 seconds.

**New method:** for fixed masses, T sends errors satisfying
v_pi(e_k)>=P-k to zero modulo pi^P. Thus a weighted residual suffices:
if Tz-z has these bounds, y=Tz has full original residual zero. Source
492 stores 7,464,600 input bytes, 51.5625% of the uniform payload, and
reconstructs every verified coefficient. Source 493 keeps low moments
0..32 at full precision and shrinks active high indices to k<P-u after
residual precision u. Twelve corrections suffice, followed by a full
GMP reconstruction. All intermediate weighted states and residuals match
the uniform baseline. Correction files total 103,751,328 bytes versus
940,992,000 for the original loop; no existing file was deleted.

The shrinking experiment imports the saved uniform seed. Its serial
coordinator takes 513.967 seconds, excluding construction of that seed;
this is not an elapsed-speedup comparison with the earlier parallel run.
Source 494 independently checks all 348 column-divisibility hypotheses,
14,476,800 state scalar overlaps, 3,695,760 residual scalar overlaps,
the exact masses and sampled recurrences from the weighted input. It
passes in 30.120 seconds. All 148 input jobs pass under the unchanged
180-second private-process-group cap and one BLAS thread.

Final review 495 binds **2532 sources**, preserving all **1884 D122 hashes**,
in [the fixed review](dembele/data/computed/dyadic_staged_review_d123.json).
Creation and hash replay pass in 3.538 and 3.198 seconds. Freeze successful
488--495, both new coordinators, their artifacts and the bound D123
report/ledger, along with all earlier freezes. No successful job or
completed coordinator needs rerunning. Keep assertions enabled and use
fresh receipt names.

**Next bounded work:** combine weighted storage and shrinking bands with
the existing resumable state-chunk protocol, then measure one actual
P=1600 column from verified P=800 with r=32. Record peak memory as well
as factor, seed, corrections, full original residual and CM times.
Check the new factor against P=800. Split oversized phases within the
existing cap; do not extrapolate affordability from one synthetic action.
**496 is next unused. No P=1600 job has run and its combined driver is
not written.** Complete these costs before another full bank or P=10552.

**Resume verification:** replay the fixed manifest through the persistent
wrapper, using this next fresh stem (attempt01 and recheck01 belong to
this completed checkpoint):

```sh
python3 dembele/pari/run_dyadic_capped.py dembele/pari/495_dyadic_staged_review.py dyadic_staged_review_d123_recheck02 'PASS|495_DYADIC_STAGED_REVIEW' --check
```

Use a later stem if it already exists. After a chat transport error,
inspect receipts and partial files before restarting: the error does not
establish whether a local command completed. The original recovery notes
below remain applicable. D122's current section/Gaussian bounds remain
unchanged, as do D99/D108, D120's conditional target, all resource pauses,
preceding exact-zero hypotheses and downstream marked-cover/field tasks.
All earlier next tasks below are historical. No correspondence was sent.


## Previous completed checkpoint — D122 comparison and independent audit complete, 2026-09-27

Continue the original-kernel field construction autonomously. Read
[the completed D122 report](dembele/certificates/dyadic-precision400-d122.md)
and [the final ledger](dembele/data/computed/dyadic_precision400_review_sources_d122.json).
**The complete sixteen-column P=400 bank, residue frame and quadric
comparison now pass independent review. All 6188 quadratic coefficients
contain zero in their certified balls; no mismatch is found. No positive
exact quadric zero, candidate identification or field polynomial is proved.**
All jobs have completed; no worker remains running.

**Accepted current arithmetic:** four raw coarse beta-errors
[832,848,832,864]; actual section lower bounds **4194/4145/4128**;
anchor bounds **3976/3648/3384**; sufficient non-anchor bounds with the
new anchor **25305/25419/25526**. These supersede D118's measured values
and anchor-dependent thresholds, using the same global height budget.
Higher intrinsic jets still require preceding exact zeros.

**W's Gaussian is now certified nonzero:** raw coarse valuation **1024**,
absolute error **1225**, relative precision **201**. Independent integer
quotient arithmetic confirms it. It has not been inverted. The historical
unresolved-denominator prohibition no longer applies to this certified
ball; any later inversion must propagate its finite error. This local
result does not improve the global ratio-height budget or identify the curve.

Sources 483--484 are now successful and frozen. Source 486 completes seven
independent phases: seventeen root residuals/branches, 272 eta cross-products,
all 8,908,800 low-state overlaps, 2560 sampled direct recurrence coefficients,
all 1088 coarse values, all residue-frame values and all 6188 quadratic
coefficients. It certifies the frame change by residual equations rather
than repeating the production inverse. Source 487 binds **1884 source
hashes** in [the final review](dembele/data/computed/dyadic_precision400_review_d122.json),
preserving all 1079 D121 hashes and all 1844 interim-checkpoint hashes.
Final review creation passes in 12.149 seconds and its hash replay in
2.230 seconds.
Its 167 input receipts all pass: 157 computations, seven independent
arithmetic phases and three interim provenance checks. Source 485 remains
the frozen historical provenance snapshot, not the completed math review.

**Next bounded work:** generalize the lift to configurable precision and
persist original-operator sweeps in state chunks. Then measure one actual
P=800 column from its P=400 checkpoint with r=32, including factorization,
seed, corrections, full residual and CM costs. Use those measurements
before another sixteen-column bank or a P=10552 solve. **488 is the next
unused source number; this generalized driver has not been written and
no P=800 job has run.** The target transports and algebraic eta are already
sufficiently refined; actual harmonic moments remain P=400. The synthetic
23.574-second target action does not cost a complete solve.

**Resume verification:** run the final manifest replay from the repository
root with the next fresh stem (attempt01 and recheck01 belong to this
completed checkpoint):

```sh
python3 dembele/pari/run_dyadic_capped.py dembele/pari/487_dyadic_precision400_review.py dyadic_precision400_review_d122_recheck02 'PASS|487_DYADIC_PRECISION400_REVIEW' --check
```

Use a fresh stem if that one already exists. Keep successful sources
476--487, their outputs and both checkpoint reports/ledgers frozen.
The persistent wrapper enforces runner 272's 180-second private-process-group
cap and one BLAS thread; keep assertions enabled. Do not relaunch 483/484
or recompute completed columns. Every census/new-level/Hecke/cubic pause,
D99 nonhyperellipticity, D108 spectral rejection and D120's conditional
precision target remain. The marked X40/Y64 covers, genus-64 section and
degree-51 torsion backend, global F256 action and final invariant remain
downstream requirements. No correspondence was sent.

**Recovery after a chat transport error:** retry the failed turn by sending
"continue", or open a new chat in `/Users/musty/two` and request
"resume from HANDOFF.md". In the CLI, `codex resume --last` resumes the
saved session. First inspect output artifacts and `.job.json` receipts:
a disconnected model response does not establish whether a local command
finished. A missing receipt or partial output needs inspection before a
replacement job is launched. Completed files remain the resume source;
never blindly rerun commands or overwrite their receipts. Restarting a
chat is a recovery attempt, not a diagnosed fix for a network failure.
All earlier next tasks below are historical.


## Previous interim checkpoint — D122 complete bank; comparison and audit pending, 2026-09-27

The user requested this handoff checkpoint. Resume the authorized plan
autonomously; no further approval is needed for the bounded tasks below.
Read [the progress report](dembele/certificates/dyadic-precision400-progress-d122.md)
and [the source ledger](dembele/data/computed/dyadic_precision400_sources_d122.json).
**All sixteen actual harmonic columns now reach P=400, including all
17 CM charts and four coarse coefficients. All 155 D122 computation jobs
pass. All batch workers have finished; no jobs remain running. The
residue-frame and quadric comparisons have NOT been run, and the
independent D122 mathematical review is still pending.** No positive
exact quadric zero, candidate identification or target field polynomial
is proved.

**Completed data:** [the consolidated bank](dembele/data/computed/dyadic_precision400_d122.json)
contains all 1088 coarse values, with beta-errors **[832,848,832,864]**,
and points to each packed state column. Original residual checks cover
8,908,800 scalar coefficients; stored CM moments contain 1,740,800.
All 174 states have moments 0--399. Only the nine states required by the
CM maps were extended through 1198; CM moments run through 799.
Column 0 remains the audited D121 result. Sources 478--479 complete
columns 1--15, preserving every old P=200 overlap. Their final original
residuals use the older GMP polynomial backend, separate from the compiled
polynomial multiplication used for the lifts.

Sources 476--477 implement and control FLINT polynomial multiplication.
A synthetic P=10552 action takes 23.574 seconds plus 1.901 preparation;
this modest improvement does not establish the cost of a complete
target-size solve. Source 480 provides controlled arbitrary-integer beta
balls. Source 481 refines the algebraic CM frame eta to **21168 beta-digits**
on the original seventeen root branches. These algebraic values do not
raise the actual harmonic moment bank beyond P=400. D121 already supplies
all 399 actual transport parameters at P=10552.

**Resume in this order, from the repository root:**

1. Recheck the fixed provenance snapshot through the persistent wrapper.
   Use a fresh receipt stem; the recorded checkpoint uses attempt01 and
   recheck01. The following recheck02 is reserved here for the next session:

   ```sh
   python3 dembele/pari/run_dyadic_capped.py dembele/pari/485_dyadic_precision400_checkpoint.py dyadic_precision400_checkpoint_d122_recheck02 'PASS|485_DYADIC_PRECISION400_CHECKPOINT' --check
   ```

2. Run drafted source 483, then inspect its successful receipt and output
   before proceeding. It constructs the residue frame from actual jets,
   checks leading rows and the old change of basis, and reports the
   Gaussian without inverting W. Imported eta error is clamped to the
   working beta precision 1024.

   ```sh
   python3 dembele/pari/run_dyadic_capped.py dembele/pari/483_dyadic_precision400_residue_frame.py dyadic_residue_frame400_d122_attempt01 'PASS|483_DYADIC_PRECISION400_RESIDUE_FRAME'
   ```

3. Run drafted source 484. It evaluates all 91 quadrics at all 17 points
   through four orders, records certified mismatches, and recomputes
   D118's sufficient non-anchor thresholds using the new anchor bounds.
   It checks the valuation condition required by its integer-scaling
   shortcut. Do not assume agreement before reading the result.

   ```sh
   python3 dembele/pari/run_dyadic_capped.py dembele/pari/484_dyadic_precision400_quadrics.py dyadic_integral_quadrics400_d122_attempt01 'PASS|484_DYADIC_PRECISION400_QUADRICS'
   ```

4. Implement an independent D122 mathematical review in a new source;
   **486 is the next unused number**. Cross-multiply refined eta values,
   check root residuals and branch overlaps, reproduce the four coarse
   coefficients with the alternate kernel/Horner method, and check the
   quadric enclosures with independent direct quotient-ring arithmetic.
   Preserve all D121 hashes and completed D122 receipts. Reassess further
   precision only after the actual quadric verdict and this review.

**Provenance and execution:** source 485 binds **1844 source hashes** in
[the fixed snapshot](dembele/data/computed/dyadic_precision400_checkpoint_d122.json),
preserving all **1079 inherited D121 hashes** and checking all **155
completed D122 input receipts**. Creation passes in 9.137 seconds and
the replay of the saved hashes passes in 2.195 seconds
(`dyadic_precision400_checkpoint_d122_attempt01.job.json` and
`dyadic_precision400_checkpoint_d122_recheck01.job.json`). These are
provenance/completion checks, **not the pending
independent mathematical audit**. Its `--check` replays the saved manifest
even after later D122 artifacts are added. Freeze successful sources
476--482, completed outputs, and the checkpoint's bound report/ledger.
Sources **483--484 are unrun drafts, intentionally not frozen**; their
output JSON files do not exist at this checkpoint. Retain all older freezes.

Use [run_dyadic_capped.py](dembele/pari/run_dyadic_capped.py) for new jobs:
it uses frozen runner 272, one BLAS thread and a 180-second private
process-group cap, rejects existing log/receipt names, and archives a
failed driver. Keep assertions enabled. No temporary-file runner is
required; `/private/tmp/d122_columns.py` is no longer needed, and no
pause flag remains. Do not overwrite or relaunch completed columns.

**Mathematical boundary:** the last accepted section bounds remain D118's
3794/3745/3728, anchor 3576/3248/2984, and sufficient non-anchor
25330/25444/25551. No P=400 quadric improvement is claimed yet. Higher
intrinsic jets require preceding exact zeros. Keep D99 nonhyperellipticity,
D108's spectral rejection, W's unresolved Gaussian, D120's conditional
P=10552 target, and all census/new-level/Hecke-bank/cubic-precision pauses.
The base genus-16 curve is not the torsion carrier: the marked double
X40/cubic Y64, section interface, genus-64 degree-51 torsion backend,
global F256 action and degree-257 field invariant still require work.
Decisions, references and all seven entry documents are current.
No correspondence was sent. Earlier next steps below are historical.


## Previous checkpoint — D121 Schur solver and first actual precision lift, 2026-09-27

Continue autonomously. Read [the proof and next task](dembele/certificates/dyadic-schur-lift-d121.md)
and [the ledger](dembele/data/computed/dyadic_schur_sources_d121.json).
**One actual harmonic column is now certified at P=400, including all
17 CM charts and four coarse coefficients. The full sixteen-column bank
remains at P=200. No positive exact quadric zero, candidate identification
or target field polynomial is proved.**

Low-moment elimination works. All sixteen low columns are checked at
r=1,8,32,64 on P=200. A complete r=64 iteration recovers one column by
64 -> 129 -> 194 -> 200. The 174-state minimum-fill ordering uses 2246
block updates, 174 diagonal inverses, 506 lower and 546 upper blocks.
The extra test right-hand sides in 467 number two, not a full-rank basis.

The arbitrary-precision FLINT block kernel uses degree-fourteen Newton
interpolation with eleven binary guard digits, dividing powers of two
exactly in the integers and inverting only odd factorial parts. At target
1319-bit arithmetic, n=32/64 products take 0.078/0.444 seconds.
Keep assertions enabled. All 399 actual transport maps now have certified
P=10552 precision on the original Hensel branch (root error 10816).

Source 472 factors the actual r=32, P=400 low matrix in a 39.370-second
job; packed factors occupy 70,303,744 bytes. Source 473 lifts column 0 by
200 -> 233 -> 266 -> 299 -> 332 -> 365 -> 398 -> 400. Its final original
residual checks 556800 scalar coefficients and all old overlaps.
Source 475 extends only nine required states, computes all seventeen
CM A charts and four actual coarse coefficients, with beta-errors
[832,848,832,864]. The state jobs total about 248 seconds; CM takes 13.873.
Artifacts are `dyadic_actual_P400_col0_verified_d121*` and
`dyadic_actual_CM_P400_col0_d121*`. These cannot yet improve the full
residue-frame or quadric certificate because fifteen columns are missing.

**Next work:** accelerate polynomial transport in compiled arbitrary
precision arithmetic, validate against old and new actual data, then
complete the sixteen-column P=400 bank and recompute the quadrics before
committing to P=10552. Prepared synthetic target action is 26.825 seconds;
348 actions already extrapolate to 2.6 hours for a single full column
sweep. A complete target-size run is still not ready. Source 473 fixes
466's short-output power truncation and supplies checkpointed phases.

Audit 474 binds **1079 sources**, preserving all **961 D120 hashes**.
Twenty-one of 24 input attempts pass. Two sentinel-comparison failures
and one premature dependent-stage launch are fully archived. Independent
checks cross-multiply all transports, test interpolation identities,
use a direct recurrence for selected original equations and re-evaluate
all 68 new coarse values by an alternate kernel and Horner evaluation.
Freeze successful sources 464--475 and bound artifacts. Recheck 474
`--check` through runner 272, one BLAS thread and its 180-second private
process-group cap. All resource pauses, W's unresolved Gaussian, D99,
D108 and downstream cover/field requirements remain. Decisions and
references are current. Earlier next steps below are historical.


## Previous checkpoint — D120 reassessment, precision design and norm-97 isolation, 2026-09-26

Continue the user's authorized construction autonomously, without another
approval pause. Read [the decision and proofs](dembele/certificates/construction-reassessment-d120.md)
and [the source ledger](dembele/data/computed/construction_reassessment_sources_d120.json).
**No positive quadric jet is proved exactly zero, no candidate identification
is proved, and no target polynomial is constructed.**

**Decision:** retain D118's direct integral quadratic-section certificate.
The complete D119 inverse-frame estimate is worse: new-frame thresholds
43459/43553/43642 versus measured 154/105/88. Those local measurements
remove the old scalar of valuation 3640; comparing unadjusted values would
be wrong. Odd residue indices cancel using Fitting-ideal clearing, so no
unproved odd-prime vanishing is assumed. Known minors also give
h_Fal <30.970856, excluding a Faltings-only rescue of the current bound,
which would need >35.39--36.18. Close these two particular detours.

**Concrete conditional precision target:** P=10552 pi-digits suffices for
all three successive section tests IF the refined quadratic enclosures
contain zero and all input/error hypotheses in report section 3 hold.
The per-order targets are 10416/10480/10552. The normalized non-anchor
matrix has Smith factors [0x8,35x8], inverse entries >=-35 and q_i=-35
in valuation. With raw four-jet error E=2P+32, the quadratic coarse error
is at least E-296. The local section bounds are
N_n=2P+3310-33n and A_n=2P+2784-296n. Refine transports to >=P pi-digits,
eta to >=E beta-digits and beta arithmetic to >=2P+64. Actual certified
data remain P=200; these formulas do not prove candidate equality.

**New implementation:** 459 replaces dense Möbius operators by a moment
generating-function transform and carry-free arbitrary-integer products.
463 accelerates it with the installed GMP 6.3.0 and integral binomial
formulas. Both reproduce one harmonic column in all 174 state equations
and all 17 CM charts, checking 332800 scalar coefficients. The first
Python synthetic P=1600 action took 51.126 seconds; GMP takes 1.146.
A separate synthetic P=10552 action passes in 50.408 seconds. It is NOT
an actual moment refinement or a complete solver. Payload at this P is
2.424 GB per low-moment harmonic column, 38.778 GB for sixteen, before
buffers. The discarded dense operator design would need 72.75 TB.

**Next bounded task:** implement and time r=1 low-moment elimination on
the existing P=200 bank. Once masses are fixed, the degree-k transport
column is divisible by pi^k. Eliminating the first r positive moments
gives Schur matrix T_UU+T_UL*(I-T_LL)^(-1)*T_LU divisible by pi^(r+1).
For r=1 the low block has dimension 174. Certify its solve, precision
gains and the original full residual; cost storage and iteration before
increasing r or refining actual moments. The single-operation benchmark
does not make thousands of full sweeps affordable. No large run is ready.

**Downstream gate now closed:** norm-97 target cofactor separation follows
from the frozen source-58 multiplicities and D51: 4=3+2*m1+m2 with m2>=1
forces (m1,m2)=(0,1). Source 60 independently gives t^40 at level p-new.
The first norm-97 target has order 51 and matches the SECOND T31 target;
the other has order 257. The first is isolated in J(Y64)[2] and rational
over residue degree 51. This does not construct Y64, implement its
torsion backend, or supply the global F256 action. No new Hecke data.

**Audit:** 462 binds **961 sources**, preserving all **922 D119 hashes**.
Seven input jobs pass; one incorrect expectation that BOTH norm-97
targets had order 51 was caught and is fully archived. Probe/final
independent reviews pass in 5.261/6.791 seconds; the reproducibility recheck
passes in 7.093 seconds. Freeze successful sources
458--463 and all bound files. Recheck via runner 272, one BLAS thread and
the 180-second private-process-group cap:

    python3 dembele/pari/462_construction_reassessment_review.py --check

D118's current section thresholds 25330/25444/25551 and actual values
3794/3745/3728 remain unchanged. Higher jets require preceding exact
zeros; W's Gaussian is unresolved and must not be inverted. D99/D108,
all census/new-level/Hecke-bank/cubic-precision pauses and every remaining
marked-cover, section, torsion and final-field requirement stand. Decisions,
references and all seven entry documents are current. No correspondence
was sent. Earlier next steps below are historical.


## Previous checkpoint — D119 actual Cartier CM divisor and dyadic residue index, 2026-09-26

Continue the user's authorized work autonomously. Read
[the D119 proof and next task](dembele/certificates/cm-cartier-frame-d119.md)
and [the source ledger](dembele/data/computed/cm_cartier_frame_sources_d119.json).
The actual local-model and divisor hypotheses from D102 are now proved
at 2. **No positive quadric jet is proved exactly zero, no candidate
identification is proved, and the target polynomial remains unconstructed.**

**The actual dyadic residue index is now computed.** On the minimal regular
semistable model, eight pairs of ordinary CM sections meet with intersection
length 33 each. The anchor is disjoint from them. Keep the intersections:

    A=R x product_(j=1)^8 R[t_j]/(t_j^2+4*(2+b)).

This is the degree-17 finite flat Cartier divisor's algebra; its
normalization index is 264 and discriminant valuation is 528 in v_beta.
It is not D102's abstract field order. The ordinary quotient parameter
is t=x-y, with t(P_plus/minus)=+/-2*beta and dt/du=+/-4*beta.
The anchor lies on component 6 after tail contraction; ordinary pairs
lie on the retained chain components 51--58 (D99 one-based labels).

**Principal-parts matrix:** at each pair use rows
(h_plus+h_minus)/(16*beta^2), h_plus/(4*beta); at W use h_W/beta^296.
The Smith valuations are [0x9,2x7], so length H1(O(D))=14.
The primitive principal part has value valuations [2,0x16], hence
norm valuation 2. The residue map has Smith valuations [0x8,2x8],
index valuation **16**, and cokernel **(R/(beta^2))^8**.
Thus beta^2 clears the local residue frame for a primitive pencil generator.
The normalized dyadic index contribution is log(2), split 7/8 and 1/8
between torsion and principal-part norm. The evaluation defect 245 is
a different lattice quantity. Separating the sections instead changes
the model-dependent index to 808; do not transfer it between models.

**Height assessment and next bounded task:** D119 section 5 derives
a lower bound for the intrinsic pencil line Lambda with its induced
principal-parts metric. The determinant identity includes both the
intersection term and the archimedean volume. It does NOT yet give a
bound for the inverse residue map or an improved quadric certificate.
Next derive that full quadratic-section bound with consistent metrics,
the actual codifferent and the beta^2 clearing map. Compare degree minus
measured zeros with D118 before adopting it. If it does not improve the
bound, reject this replacement and return to an exact identity or a
costed precision design. Non-dyadic indices and global h normalization
are still uncomputed. Previously counted vertical zeros cannot be
subtracted again as a height gain.

**Current sufficient section valuations remain 25330/25444/25551**,
versus actual 3794/3745/3728 and anchor 3576/3248/2984. Use D118's
cm_arithmetic_height_budget_d118.json. These are section valuations,
not ratio errors or moment precision. Higher intrinsic jets require
preceding EXACT zeros. D116's 68>60 criterion and D117's disk stand.

**Audit:** review 457 binds **922 sources**, preserving all **911 D118
hashes**. Independent integer quotient arithmetic reconstructs all 272
restriction entries, all 17 maximal minors, the primitive kernel and
the full residue map. The first 456 run failed only on the expected
graph-pruning count; its source, log and receipt are archived. The
corrected calculation passes in 3.882 seconds, and the independent
probe/final review in 2.642/4.159 seconds; the reproducibility recheck
passes in 4.622 seconds. Freeze sources 456--457 and
bound artifacts. Recheck through runner 272, OPENBLAS_NUM_THREADS=1,
and its 180-second private-process-group cap:

    python3 dembele/pari/457_cm_cartier_frame_review.py --check

Keep the P=200 data. W's Gaussian remains numerically unresolved; never
invert it. Actual J3 rank is at least 33, not 45, and uses D99 for descent.
All census, new-level, Hecke-bank and cubic-precision pauses stand.
A large precision proposal still needs a costed, limb-safe implementation
and transport refinement. D99 nonhyperellipticity, D108's spectral
rejection and all downstream marked-cover/field requirements remain.
Decisions, references and all seven entry documents are current.
No correspondence was sent. Earlier next steps below are historical.


## Previous checkpoint — D118 finite CM height and tropical Faltings correction, 2026-09-26

Continue the user's authorized work autonomously. Read
[the D118 proof and next task](dembele/certificates/cm-finite-height-d118.md)
and [the source ledger](dembele/data/computed/cm_finite_height_sources_d118.json).
The omitted dyadic fibre correction and a stronger graph-based Faltings
lower bound are now included. **No positive quadric jet is proved exactly
zero, no candidate identification is proved, and the field polynomial
remains unconstructed.**

**Current sufficient non-anchor beta-valuations:** **25330/25444/25551**
for orders 1/2/3. Actual lower bounds remain **3794/3745/3728**, with
anchor bounds **3576/3248/2984**. Use `cm_arithmetic_height_budget_d118.json`.
The intermediate fibre-only bounds 27633/27747/27854 in source 452 are
superseded by source 454. These are section valuations, not ratio errors
or moment precision. Higher intrinsic jets require preceding EXACT zeros.
D116's 68>60 identification criterion and D117's disk rho^2=3/5 stand.

**Dyadic fibre correction is complete as a sum:** pull W_C -> W_S^2
to a sufficiently small level, where the canonical arithmetic Hodge line
is the dualizing line. In the existing CM coordinate,
lambda=dz/z=2*dw/(1-w^2), u=w^2. The composite derivative sends an
integral fibre generator beta^m_i du to a unit times beta^m_i/2 times
lambda^2. Thus its contents are **[280,17x16]**, since m=[296,33x16].
Galois averaging gives (69/34)*log(2), and
H_CM <= 2*h_L-(35/34)*log(2) < 8/3. This computes the dyadic part of
2*c_L+c_ram exactly; their individual values and non-dyadic contributions
are not computed. No auxiliary level calculation was run. Splitting the
two terms cannot produce additional dyadic gain. The evaluation defect
245 is not either correction or the D102 residue index.

**Faltings improvement:** the existing length-76 reduction graph has
tau=67889/27075 and tropical moment 223268/27075. The de Jong--Shokrieh
formula, in the matching L2 normalization, gives
h_Fal(C) >= -16*log(pi)-8*log(2)+(55817/54150)*log(2) > -23.146371.
The other theta-height/local terms are discarded by nonnegativity.
No new graph, census, level, Hecke data or moments were computed.

**Remaining gap and next bounded task:** the actual valuation gap is
21536--21823. Even rho=1 with all other inputs fixed leaves thresholds
22310/22412/22506. Improving only the h_Fal lower bound would need a
bound above about 36.172 for all orders; 37 suffices but is NOT proved.
Known vertical content already counted in the local jet valuations
cannot also be subtracted as a new height gain.

Test an integral frame construction with lower dependence on CM fibre
height through D102's principal-parts sequence. First construct/check an
actual model where the horizontal CM divisor is finite flat Cartier,
record CM intersections, and verify the principal-part norm and H1-torsion
terms. The current stable evaluation matrix alone does not establish
these hypotheses or determine the index. No improved replacement bound
from this route is proved yet. Keep exact identities with uniqueness as
an alternative and the current section certificate as a fallback.

**Audit:** final review 455 binds **911 sources**, preserving all **891
D117 hashes**. It revalues all 272 leading coefficients, checks the
graph inverse by multiplication, independently integrates the resistance
derivatives at all thirty vertices, and recomputes the budgets with a
separate logarithm series. All four input jobs pass first attempts. The
probe/final review pass in 4.396/5.784 seconds; the reproducibility
recheck passes in 6.336 seconds. Freeze sources 451--455
and bound files. Recheck through runner 272, OPENBLAS_NUM_THREADS=1,
and the 180-second private-process-group cap:

    python3 dembele/pari/455_cm_finite_height_review.py --check

Retain the actual D115/D116 P=200 bank, rational frame and four coarse
coefficients. W's Gaussian remains unresolved numerically; never invert
it. Actual J3 rank is at least 33, not 45, and its descent uses D99.
Any large precision proposal still needs a costed, limb-safe implementation,
transport refinement and capped phases. D99, D108 and all census,
new-level, Hecke-bank and cubic pauses stand. Marked-cover, genus-64
section, norm-97, torsion and degree-257 invariant work remains downstream.
Decisions, references and all seven entry documents are current.
No correspondence was sent; earlier next steps below are historical.


## Previous checkpoint — D117 uniform CM disks and arithmetic exactness, 2026-09-26

Continue the user's authorized reassessment autonomously. Read
[the D117 proof and revised plan](dembele/certificates/cm-disk-and-exactness-d117.md)
and [the source ledger](dembele/data/computed/cm_disk_sources_d117.json).
The direct integral quadratic-section route remains primary. The new
uniform CM disk sharply improves its sufficient bounds, but **no positive
quadric jet is proved exactly zero, no candidate identification is proved,
and the target field polynomial remains unconstructed**.

**Current sufficient beta-valuations:** **35947/36096/36237** for successive
orders 1/2/3, including the measured anchor contributions. Actual lower
bounds remain **3794/3745/3728**, with anchor bounds **3576/3248/2984**.
Use `cm_uniform_disk_budget_d117.json`. These are section valuations,
not ratio error digits or working moment precision. The higher integral
jets require preceding jets to vanish EXACTLY. The D116 four-term test
still gives exact identification via 68>60 without a rank-45 prerequisite.

**Uniform geometry is now certified:** the integral commutator trace
gives a 6167-vector real-lattice test. The stronger projection
x=alpha+beta*alpha*beta^(-1) lies in O_M and has squared absolute values
at most four at seven compact places. An exhaustive 376935-vector CM
lattice test excludes a remaining value in (4,64]. Thus every moving
translate has displacement >2*acosh(4), uniformly for all CM points and
conjugates. Open disks of radius squared **3/5** embed modulo the order-two
stabilizer. No group/class census or moment refinement was needed.
The trace-only radius 9/19 and thresholds 41761/41934/42099 in source 447
are preliminary; source 449 is current. Freeze all successful sources.

**Radius-only refinement is insufficient:** with the other inputs fixed,
even the optimistic rho=1 substitution leaves thresholds
**32928/33064/33193**. This is a limitation of this bound, not a universal
precision lower bound. The actual valuation gap is still 32153--32509.

**Next bounded arithmetic task:** compute the finite corrections omitted
from D104. If c_L=h_L(Q)-h(W_S) and c_ram is the finite zero degree of
D_Q(df), then H_CM=2*h_L(Q)+log(2)-2*c_L-c_ram. Obtain proved dyadic
contributions from the stable upstairs cover and compatible Hodge/stable
lattices, then assess their effect on the bound. Neither correction has
been computed. Prove the upstairs nodal generator and stabilizer thickness
before interpreting derivative coefficients as integral content. The
evaluation defect 245 is not either correction or the D102 residue index.
A stronger h_Fal lower bound or an exact identity may also be needed.

Do not launch another small precision pilot as the default. The present
dense state alone would need over 104 GB in an ideal packed representation
at P=10000; this is an algorithm-specific example, not a forecast of the
required P. A large run first needs a different costed implementation,
proved limb arithmetic, refined transport inputs and capped phases.
Keep the actual D115/D116 P=200 bank, frame and four coarse coefficients.
W's Gaussian remains unresolved numerically; never invert it. Actual J3
rank is at least 33, not 45, and its descent already uses D99.

**Audit:** review 450 binds **891 sources**, preserving all **868 D116 hashes**.
It independently checks both lattice enumerations, Gram matrices, root
intervals, displacement controls and rational logarithm budgets. Four
input jobs pass; one serialization-only failure is archived with its
source, log and receipt. The independent probe and final review pass
in 7.536 and 9.031 seconds; the reproducibility recheck passes in 9.527
seconds. Freeze sources 446--450 and all bound files.
Use runner 272 with OPENBLAS_NUM_THREADS=1 and its 180-second private
process-group cap for the reproducibility check:

    python3 dembele/pari/450_cm_disk_exactness_review.py --check

D99 nonhyperellipticity, D108 spectral rejection and all census, new-level,
Hecke-bank and cubic-precision pauses stand. Markings, the double-cover
character, global genus-64 sections, norm-97 isolation, target torsion
and the degree-257 invariant remain downstream. Decisions, references
and all seven entry documents are current. No correspondence was sent.
Earlier next steps below are historical.


## Previous checkpoint — D116 integral quadric identification criterion, 2026-09-26

Continue the user's authorized reassessment autonomously. Read
[the D116 proof and revised plan](dembele/certificates/cm-compound-height-d116.md)
and [the source ledger](dembele/data/computed/cm_compound_sources_d116.json).
The primary route now tests the candidate's **quadratic sections directly**.
It avoids Gaussian denominators and the separate rank-45 prerequisite.
**No positive quadric jet is proved exactly zero, no candidate identification
is proved, and the target field polynomial remains unconstructed.**

**Current sufficient certificate:** Q(s)/Delta is integral for every one
of the 91 quadrics through the full CM frame. An explicit adjacent-pair
complementary-minor identity bounds its tensor norm by 2^4855. Conditional
successive divided jets are integral even at nodal specializations.
With the certified anchor bounds, sufficient non-anchor beta-valuations
are **119806,120284,120758** for orders 1,2,3. Actual lower bounds are
**3794,3745,3728**; anchor lower bounds are **3576,3248,2984**.
These are integral-section valuations, not ratio error digits.
Orders 2/3 acquire their intrinsic integral interpretation only after
the preceding jets vanish EXACTLY. Zero-containing balls do not suffice.
Exact vanishing through order three would give 4D of degree 68 as zeros
of a section of 2K of degree 60, identifying (C,D) by D88/D69.

**Actual local data are complete through the required order:** source
442 computes all 272 third coarse coefficients from the frozen P=200
moment bank, without raising moment precision. The four coarse errors
are **432,448,432,448 beta-digits** and all 1088 entries are certified
nonzero. Use `dyadic_third_coarse_jet_d116.json` together with D115's
`dyadic_comparison200_d115.json` frame. Source 443 evaluates all 91
quadric residuals at all 17 CM points through order three; every enclosure
contains zero. Review 445 independently checks all third coefficients
and all 4641 positive quadratic coefficients.

**Integral lattice:** all sixteen Smith factors of the harmonic basis
are one. The weighted flows c_e/|Gamma_e| have an integral change matrix
of determinant -1 to fundamental graph cycles. The companion nodal-model
residue proof identifies this with the stable integral differential
lattice; it is not an assertion that invariants commute with reduction.
Vertex-deletion connectivity proves canonical global generation.
Integral fibre exponents are [296,33x16], cofactor valuations [280,245x16],
v_beta(Delta)=4200, and the D103/D115 common section factor has valuation
3920. The evaluation saturation defect 245 is NOT the D102 horizontal
CM residue-map index, which remains uncomputed.

**Alternative ratio route:** integral exterior-power cancellation and
dyadic common-zero subtraction reduce actual coefficient heights below
4723/19438 and sufficient degree-16-place ratio beta-errors to
**132444/524481** (integer pi-errors 66222/262241). Achieved errors remain
101/70. W's Gaussian remains numerically unresolved; never invert it.
The actual J3 matrix has certified rank at least **33**, not 45.
Candidate-centered +96-beta conditioning predicts rank 45 but is not
an actual computation. This diagnostic is not an independent proof of
nonhyperellipticity because the rational descent already uses D99.

**Next bounded research task:** sharpen the actual reduced-quadric
norm/content bound using the explicit complementary-minor formula,
or establish an exact arithmetic identity with a uniqueness argument.
The current 116012--117030 valuation gap does not justify another small
precision pilot as the main plan. A larger run first needs a limb-safe
arithmetic design, transport/Hensel accuracy, memory and time estimates,
and phases respecting the 180-second cap. No such large precision run
has been made. The current fixed-width products cannot simply be reused
above their proved range. Candidate-only heights or extra finite matches
do not supply an exactness proof.

**Audit:** final review 445 binds **868 sources**, preserves all 814 D115
source hashes, and includes the new artifacts, report and ledger. All
thirteen input jobs pass, with no failures or timeouts. The final audit
and reproducibility recheck pass in 151.117 and 147.619 seconds; the
calculation probe also passes within the cap. Freeze sources 432--445
and bound files.
Sources 435/440 are preliminary probe-only reviews; use their cores via
445, not their obsolete draft final-build job counts. Source 441's
147023 direct bound is superseded by 444's 120758 bound. Recheck through
runner 272 with Python/NumPy:

    python3 dembele/pari/445_cm_arithmetic_identification_review.py --check

D99 nonhyperellipticity and D108 spectral rejection stand. Retain all
census, new-level, Hecke-bank and cubic-precision pauses. After exact
base identification, P32/B3 markings, double-cover character, global
genus-64 cubic/section data, norm-97 isolation, combined torsion and the
degree-257 invariant remain separate requirements. Decisions, references
and all seven entry documents are current. No correspondence was sent.
Earlier next steps below are historical.


## Previous checkpoint — D115 actual rational-frame comparison and revised strategy, 2026-09-25

The user asked for a reassessment and sustained execution without approval
stops. The local plan has been carried through: W is resolved, the actual
harmonic-to-rational-residue frame is computed, and the first two ratio
coefficients agree with the candidate within **101 and 70 beta-digits**
at all sixteen non-anchor CM points. Read
[the D115 report and revised plan](dembele/certificates/dyadic-comparison-and-strategy-d115.md)
and [the source ledger](dembele/data/computed/dyadic_comparison_sources_d115.json).
No certified mismatch is found. **Exact curve identification and the
target field polynomial remain unproved.** Do not turn this agreement
into the exact D88/D106 J3 certificate.

**Actual computation:** full Eisenstein arithmetic replaces the old
precision-at-most-16 shortcut. Working precisions 24,40,56,72,104,136,152,200
all pass overlap checks. Batched operators, correction-only iteration
and separate capped phases make the final run practical. At P=200 there
are 1,667,616 state entries through degree 598 and 108,800 entries in
the seventeen CM A charts through degree 399. The twice-A formula gives
coarse beta-errors 432,448,432. All 816 harmonic-basis coarse entries
are now certified nonzero.

**W and the splitting:** the first W leading value has v_beta=296
(v_pi=148), first resolved at P=136. The leading values in basis order
have valuations 296,308,308,314,314,314,314,318,326,326,326,326,322,322,322,322.
Source 425 refines the same D109 Hensel root from error 180 to 352.
All exact C+S*x transport matrices are unchanged; normalized child and
CM center errors are now at least 331/337. No new splitting branch,
class census, tree domain or CM labeling is used.

**Actual rational frame:** normalize the seventeen leading harmonic
rows to h_i. With D the sixteen non-anchor rows, q=h_W*D^(-1), and
E_i the certified D112 residue rows, use
M=D^(-1)*diag(q_i^(-1))*E_nonanchor. Then h_i*M=E_i/q_i and
h_W*M=-E_W. All pivots and q_i are certified nonzero. D106 identifies
this with the rational residue basis up to a common scalar. Candidate
jets enter only after constructing M. Sources 418/427 track absolute
local errors through every multiplication and division.

**Ratio comparison:** the parameter t=omega_2/omega_1-(omega_2/omega_1)(P)
is certified at each non-anchor point: its saved Gaussian has valuation
153 and error 254. In this frame, the first and second ratio coefficients
have candidate-difference errors **101 and 70 in v_beta**, or 50.5 and 35
in v_pi. The 512 comparisons include normalization coordinates. The
sixteen embeddings form one degree-16 dyadic place, not sixteen places.
W's Gaussian remains numerically unresolved at error 825; do not divide
by that enclosure. Rationality and CM transitivity nevertheless prove
qualitative nonvanishing of this chart throughout the CM divisor.

Use `dyadic_comparison200_d115.json` for the actual frame and ratio
coefficients, `dyadic_precision200_d115.json` for harmonic coarse values,
and `dyadic_moment_transports_refined_d115.json` for refined centers.
Review 428 independently certifies all operator identities, moments,
CM transfers and coarse kernels. Review 430 checks the ratio formulas
by direct series division and parameter reversion.

**Exactness and the next research objective:** the current D106 height
bound requires beta-errors **274241/820774** at the degree-16 place for
orders 1/2, equivalently sufficient integer pi-errors **137121/410387**.
Source 423 proves these thresholds using rational logarithm enclosures.
The smaller both-place thresholds require a separate W ratio error,
which is not available. These are sufficient bounds, not claims about
the minimum precision of every possible proof.

Retain the route and candidate as supported by the independent comparison,
but do not make another routine precision increase the default next step.
The next objective is an exact arithmetic identification certificate:
either a substantially sharper effective bound on the actual unknown
coefficients or an exact identity/correspondence with proved uniqueness.
No such replacement is proved here. Candidate-only heights, extra matching
primes and additional finite Taylor agreement do not close this gap.
This is a mathematical requirement, not a request for user approval.

**Provenance:** final review 431 binds **814 sources** and preserves all
**713 D114 hashes**. Before the final audit, 24 jobs passed and four
implementation probes failed; all failures are archived. The fixes restore
exact zeroth masses before refinement and distinguish exact equality from
the finite v(0) sentinel. No mathematical assertion was weakened. All jobs
use runner 272 and the 180-second private-process-group cap; the longest
took 145.02 seconds, with no timeouts. Freeze sources 417--431 and bound
artifacts. Recheck through 272 with Python/NumPy:

    python3 dembele/pari/431_dyadic_strategy_review.py --check

After exact base identification, the P32/B3 markings and double-cover
character still need certification. Exact global genus-64 cubic/section
data, norm-97 isolation, combined torsion scaling and the target degree-257
invariant remain separate gaps. Keep all census, new-level, Hecke-bank
and cubic-precision pauses. D99's nonhyperellipticity and D108's spectral
rejection stand. All seven entry documents, decisions and references
are current. No correspondence was sent. Earlier next steps are historical.


## Previous checkpoint — D114 actual coarse differential jets and anchor precision gate, 2026-09-25

The user authorized continuing with “continue!”. The bounded actual
Poisson evaluation is complete. Read
[the D114 proof](dembele/certificates/dyadic-coarse-d114.md) and
[the source ledger](dembele/data/computed/dyadic_coarse_sources_d114.json).
We now have the first three coarse coefficients of all sixteen
actual harmonic differentials at all seventeen matched CM points:

    omega_a=(g_(a,0)+g_(a,1)*u+g_(a,2)*u^2+...)*du,
    u=((z-beta)/(z+beta))^2,     beta^2=-(2+pi).

The final error valuations are **32, 40, 32 in v_pi**. All 256
non-anchor entries at each order are certified nonzero. At W,
the respective valuations are bounded below by **32.5, 40.5, 32.5**.
These lower bounds do not prove exact vanishing or nonvanishing.
This is an actual harmonic-basis coarse differential 2-jet; the
rational-residue-frame ratio jet, actual frame change, Gaussian
pivot, candidate identification and target polynomial remain open.

**Extended moment bank:** source 414 uses working precision 16,
low cutoff 15 and 16 iterations, then recovers state degrees
through 46 by row evaluation. Child-map columns k>=P vanish
modulo pi^P uniformly in the row degree, so a larger fixed system
is unnecessary. The resulting 130,848 state entries and 26,112
CM entries (51 charts, degrees 0..31, sixteen measures) have errors
at least pi^16. All frozen D113 state values agree on overlap.
The two-bit-plane quotient is used only at its P<=16 limit.

**Coarse kernels and precision:** source 415 combines D108's exact
Taylor-to-coarse formula with the three CM moment expansions.
Integral kernel coefficients avoid approximate division by beta.
The full degree-16 CM polynomial gives arithmetic modulo beta^80.
Keeping the binomial valuations proves initial errors 24,32,24
pi-digits and certifies 250 nonzero entries per order. Those
source-415 values remain frozen with their original error bounds.

Review 416 independently expands

    K_j(t)=(1-((beta+t)/(beta-t))^(2j+2))/2.

It uses separate integer polynomial arithmetic modulo beta^96,
pays the 16-beta-digit division loss, and checks all 288 kernel
coefficients. The actual CM involution T(t)=beta^2/t exchanges
A=pi*O_K with its complement and preserves both measure and kernel.
Consequently g_j=2*integral_A K_j dmu. The constant A coefficient
vanishes, and its positive coefficients gain factors 4,8,4 for
j=0,1,2. This proves the stronger errors **32,40,32 pi-digits**.
The refined values are in `dyadic_coarse_review_d114.json` at
`certificates.Poisson.symmetry_refined_CM_values`; use these with
their specified harmonic basis and local parameter. The full
three-chart and twice-A enclosures agree.

**Anchor precision gate:** at W, all A-chart moments of degrees
0..31 vanish modulo pi^16. Since the residue field is F2,
Q(X)=(X^2-X)^16 is monic of degree 32 and takes values in pi^16.
Monic division and d=0 prove that every integral polynomial moment
on this chart is divisible by pi^16, at every degree. Applying
that bound to the twice-A kernel gives the stated anchor lower
bounds. Increasing only the degree cutoff at precision 16 cannot
resolve W. No normalization has been performed.

**Independent audit:** review 416 checks every moment residual and
CM transfer using separate binomial/convolution arithmetic, every
coarse coefficient, and the involution identity. A wrong infinity-
kernel sign is rejected. The moment/evaluator jobs pass in 4.59/0.40
seconds. One failed review probe is archived: a NumPy integer needed
conversion to a Python integer before bit_length. The corrected
probe and final review pass in 1.69/2.16 seconds. No mathematical
assertion was weakened. The review binds **713 sources**, preserving
all **696 D113 hashes**. Freeze sources 414--416 and bound artifacts.
All jobs use runner 272 and its 180-second private-process-group cap.
Recheck with Python and NumPy through 272:

    python3 dembele/pari/416_dyadic_coarse_review.py --check

**Next bounded task:** raise moment working precision to **24
pi-digits**, initially evaluating W's A chart with the twice-A
formula. Conservative parameters are low cutoff 23, 24 iterations,
state cutoff 70 and CM cutoff 47, giving coarse error bounds at
least 40,48,40 pi-digits. These are design bounds; nonvanishing at
this precision is not guaranteed. Use a new full Eisenstein
quotient implementation: pi^8=-2 is invalid at precision 24 because
the -20*pi^4 term has valuation 20 and contributes. The defining
polynomial is pi^8-8*pi^6+20*pi^4-16*pi^2+2. Retain all its relevant
terms and certify overlap with the precision-16 bank. CM arithmetic
needs at least beta^96, with extra precision for independent divisions.
Existing normalized transport errors 159/165 suffice; keep the
same splitting branch and finite charts. Preserve the low-degree
solve/high-row recovery and the 180-second cap. Do not divide by
an unresolved anchor.

After anchor nonvanishing, actual harmonic-to-residue frame change,
cofactor errors and a Gaussian pivot remain separate requirements
before ratio jets. Final-scale performance and dyadic equality
thresholds remain open; do not copy inert-31 thresholds. D99's
nonhyperellipticity and D108's spectral rejection stand. Keep all
census, new-level, Hecke-bank and cubic-precision pauses. Downstream
marking, global sections, norm-97 separation and target-scale torsion
remain separate. Decisions, references and all seven entry documents
are current. No correspondence was sent. Earlier next steps are historical.


## Previous checkpoint — D113 actual positive moments by finite contraction, 2026-09-25

The user authorized continuing with “keep going!”. The finite moment
recursion and bounded actual pilot are complete. Read
[the D113 proof](dembele/certificates/dyadic-moments-d113.md) and
[the source ledger](dembele/data/computed/dyadic_moment_sources_d113.json).
There are now **33,408 certified state moments** (174 charts, degrees
0..11, sixteen measures), with error at least pi^12. The first three
positive moments in all 51 matched CM charts have error valuations
**11, 10, 9**. Of the 2448 CM entries, **2043 are certified nonzero**.
No actual differential value/jet, harmonic-to-residue change of basis,
candidate identification or target polynomial is obtained yet.

**Finite arithmetic maps:** source 411 uses the existing D111 edges
and local frames. For each slot e, H_e=L_j*H_d maps O_K to its
oriented boundary ball. In direction order infinity/zero/one,
H_d is [0,1;pi,0], [pi,0;0,1], [pi,1;0,1]. The saved transport t_e
gives exactly two child maps H_e^(-1)*iota(t_e^(-1))*H_f, with images
the two residue balls. Their normalized form is

    phi(x)=(a*x+b)/(c*x+1)=b+delta*x/(1+c*x),
    c in pi*O_K, v_pi(delta)=1, b mod pi in {0,1}.

All 348 maps are exact in D109's splitting algebra. Normalized center
errors are at least 159. The 51 CM-to-state maps have the same form
with v_pi(delta)=0 and error at least 165. Quaternion words, full
partitions and all zeroth mass identities are certified. No new
class census, level or Hecke prime is used.

**Contraction and precision:** put m_(e,n)=integral x^n dnu_e. The
coefficient of x^k in phi(x)^n has valuation at least k, uniformly
in n>=1. The known zeroth masses therefore give m=b+T*m on positive
moments, with T divisible by pi. D111's d=0 makes all moments integral.
Cutoff J, N iterations and working precision P give error at least
min(J+1,N,P). This is proved directly over ramified K; no Qp control
theorem or constants are transferred. A zero residual modulo pi^P
uniquely certifies the entire retained moment bank.

**Executed pilot:** source 412 uses J=11, P=N=12. The twelve
successive differences have valuations 0,...,11, and the final
residual vanishes modulo pi^12. Two bit planes encode O_K/(pi^12):
power coefficients 0..3 are modulo 4, 4..7 modulo 2, and pi^8=-2.
The helper is restricted to P<=16. Beyond that use the full
Eisenstein polynomial; do not extend its shortcut silently.

**CM transfer and anchor limitation:** coefficients of x^k in the
n-th power of a CM ball isomorphism have valuation at least max(0,k-n).
Thus transferred degree n has error min(P,J+1-n). Zeroth values
recover D112 exactly. Every one of the 144 positive-moment entries
at W is congruent to zero at its stated error bound. This does not
prove exact vanishing and supplies no anchor normalization or pivot.
The nonzero entries elsewhere also are moments, not differential
values or an identified projective tangent.

**Independent audit:** source 413 reconstructs all exact transports
and uses ordinary polynomial convolution/integer matrix arithmetic,
separate from 412's bit-plane implementation, to check every moment
residual and CM transfer. It also independently reduces 32 leaf
balls in four CM charts (depth 3) and checks 192 direct positive-
moment sums modulo pi^3. A unit perturbation of a positive moment
is rejected. The transport / pilot / probe pass first attempts in
6.18/1.32/5.83 seconds. Review 413 binds **696 sources**, preserving
all **682 D112 hashes**. Freeze sources 411--413 and bound artifacts.
All jobs use runner 272 and the 180-second process-group cap.
Recheck with Python and NumPy, without Sage or Magma, through 272:

    python3 dembele/pari/413_dyadic_moment_review.py --check

**Next bounded task:** feed actual moments into D108's first coarse
Poisson coefficients. A modest next target is T=16 pi-digits, using
CM moments through 31, state moments through 46, and working precision
and iteration count 16. These are sufficient from the proved tail
and transfer bounds, not candidate-identification thresholds. Since
coefficients of state moment index k>=P vanish modulo pi^P, solve
only the low-degree fixed system and recover higher state moments
by one row evaluation afterward. Use a new source; keep the pilot
frozen. Certify all arithmetic/coordinate losses and establish an
actual nonzero coarse value at W before normalizing. A Gaussian
pivot, harmonic-to-residue change and cofactor error propagation
remain separate. If the modest pilot cannot resolve the anchor,
record the enclosure and its precision requirement explicitly.

The contraction proof works beyond precision 16, but the implemented
quotient arithmetic and coefficient bounds must be extended or
refined before use there. Final-scale performance and dyadic equality
thresholds remain open; do not copy inert-31 thresholds. D99's
nonhyperellipticity, D106's rational frame, D107/D112's CM labels and
D108's spectral rejection stand. Keep all census, new-level, Hecke-bank
and cubic-precision pauses. Downstream marking, global sections,
norm-97 separation and target-scale torsion remain separate. All
seven entry documents, decisions and references are updated. No
correspondence was sent. Earlier next steps are historical.


## Previous checkpoint — D112 dyadic CM coordinates and arithmetic frame matching, 2026-09-25

The user authorized continuing with “keep going!”. The bounded CM
matching task after D111 is complete. Read
[the D112 proof](dembele/certificates/dyadic-cm-matching-d112.md) and
[the source ledger](dembele/data/computed/dyadic_cm_matching_sources_d112.json).
All seventeen CM points have exact dyadic coordinates and certified
arithmetic class/root labels. The existing rational residue basis is
evaluated at the matched roots to at least 384 beta-digits = 192
pi-digits = 24 binary digits. All 51 CM boundary charts also have
actual zeroth-moment vectors for the sixteen harmonic measures.
Positive-degree moments, the actual harmonic-to-residue change of
basis, a Shimura tangent/jet, candidate identification and the target
polynomial remain open.

**Arithmetic coordinates:** source 407 uses W and both normalized
signs at the eight ordinary inverted edges 152,155,158,161,164,167,170,173.
The full O_M embeds in R for every generator v. In D109's exact
splitting A=iota(v), S=[1,A00;0,A10] satisfies
A*S=S*[0,-(2+b);1,0]. The point is S*(beta:1), with eigenvalue beta.
All S coefficients are saved exactly in the quadratic splitting
algebra; their lattice-error bounds are 173 at W and 166 otherwise.
Do not interpret these as affine-coordinate precision after divisions.

**Geometric anchor and convention:** k=ij lies in O*, has norm one
and anticommutes with W. It exchanges W's two eigenlines, so their
G-orbit is fixed by inertia. The principal prime (beta) splits in
H/M, and the local decomposition action is entirely inertia. W is
the unique K-rational point of D; f_L has one Q2-root of v2=1 and
sixteen other roots of v2=1/16, impossible in K. The torus-unit proof
gives exact stabilizer order two, excluding P32. Use the place of H
taking saved complex reference root 2 to this rational root, and
normalize the local M embedding by W's CM eigenvalue character.
Changing beta's local sign conjugates both point and root labels.

**Exact class and Artin witnesses:** for u=1 at W, u=v+W otherwise,
v*u=u*W. The ideal packet proves iota_W(a)R=u^(-1)R by localized
inclusion and norm product 1 or 128. Source 408 exports all seventeen
principal relations a=z*(31,beta+16)^c. Arithmetic Artin(a) sends
P to uP. This uses canonical CM reciprocity and prime-to-p adelic
equivariance of uniformization with the specified CM character;
the report states the theory input explicitly. It is not inferred
from root numerics or a theorem restricted to an inert Qp extension.
Relative classes in D112 order are

    [0,15,2,7,10,1,16,5,12,8,9,11,6,13,4,3,14].

**Independent root orientation:** sigma(beta)=beta^3+3*beta has
order 16 and acts on the class generator by exponent 10, with an
exact principal witness. Its root permutation is one fixed point
and one 16-cycle. D105's affine group and this action recover the
regular C17 subgroup; D107's exact cubic resolvent selects its
unique arithmetic class orientation. Rational review certifies all
17 Hensel disks, root error at least 688 beta-digits, separation at
most 17, and rejection of the inverse Artin cycle and an altered root.
The complete saved-complex/dyadic lookup is in the proof and review.

**Frame and chart masses:** use exactly the saved trace-centered
basis polynomials, not a substituted power basis. Their 17-by-16
algebraic value matrix is the target residue frame, not actual
harmonic differential evaluations. At the anchor eta1=theta-2/17
has v2=7, hence v_pi=56 and v_beta=112; at the other points v_beta=1.
For A:z=pi*x, B:z=1+pi*x, C:z=1/(pi*x), all zeroth masses satisfy
A0=0 and B0+C0=0; some B0 are nonzero. D111's d=0 remains valid.

Sources 407/408/409 passed first attempts in 11.46/5.77/1.54 seconds.
Probe one failed an incorrect expected valuation for eta1; its
source, receipt and log are archived, with no result artifact.
The corrected independent probe passed in 29.90 seconds. Review
410 binds **682 sources**, preserving all **661 D111 hashes**.
All jobs use runner 272 with the 180-second private-process-group cap.
Freeze sources 407--410 and bound artifacts. Recheck without Sage
or Magma, through runner 272:

    python3 dembele/pari/410_dyadic_cm_matching_review.py --check

**Next bounded task:** derive a finite transport/recursion for
positive-degree moments in these actual CM charts, with a proved
truncation/contraction bound over ramified K; then run a small actual
moment pilot. Direct exponential Riemann refinement is not the
high-precision plan. Do not import Qp control constants or inert-31
equality thresholds unchanged. Actual change of basis, cofactor
normalization, a Gaussian pivot and dyadic equality thresholds remain
later gates.

D99's nonhyperellipticity, D106's rational frame and D107's complex
labels stand. Keep D108's spectral rejection and all class-census,
new-level, Hecke-bank and cubic-precision pauses. Downstream marking,
global sections, norm-97 separation and target-scale torsion remain
separate. All seven entry documents, decisions and references are
updated. No correspondence was sent. Earlier next steps are historical.


## Previous checkpoint — D111 arithmetic edge reduction and harmonic cocycles, 2026-09-25

The user authorized continuing with “keep going!”. The bounded next
task after D110 is complete. Read
[the D111 proof](dembele/certificates/dyadic-harmonic-d111.md).
There are now **16 actual G-invariant scalar harmonic cocycles** and
a terminating arithmetic edge reducer. Their boundary measures have
uniform denominator bound **d=0**. No actual moment bank, dyadic CM/frame
matching, Shimura tangent/jet, candidate identification or target
polynomial has been obtained.

**Complete finite arithmetic:** export 403 reconstructs the same
58-class, norm-two, seed-990370 calculation. The matrix and stabilizers
match D99 entry for entry and the order basis matches D109. It exports
all 58 ideal bases, 174 neighbor transports and 164 projective stabilizer
elements. Exact p-supported lattice indices and b-stability, together
with residue-spanning local frames, prove all global right-ideal
assertions. All three lines in F2^2 occur once at every vertex.
Localized membership and local elementary divisors prove every global
ideal sandwich, both inclusions of Z-index four. No expanded class
census, new level or new Hecke prime was used.

**Harmonic certificate:** stabilizer invariance, reversal and the
three-term vertex sums give 376 integer relations on 174 slots.
Their rank is 158, certified independently modulo 101 and by exact
annihilation of 16 independent integer vectors. There are 155 oriented
edge orbits, nine inverted orbits and 73 reversal pairs. The inverted
orbits have value zero in characteristic zero. The basis entries have
absolute value at most four, so all boundary-ball masses are integral.
No saturated integral cohomology basis is claimed.

**Executable reduction:** import Reducer from source 405 and call
reduce(U,V) on adjacent column lattices in GL2(F), encoded as four
row-major entries, each eight rational coefficients. The result gives
all 16 cocycle values, the exact quaternion transport and its word,
and a distance trace dropping by one at each step. Every tree edge has
such F-matrix representatives. Precision is refined on D109's same
exact Hensel root when necessary; the original 180 digits are not
assumed sufficient for arbitrary word length. There is no separately
constructed connected fundamental subtree or group presentation.

Tests cover six full stars through depth 32, edge reversal, eight
nonzero sample edges and invariance under u, W and h. A shortened
root center refines from error 28 to 48 and reproduces the full-precision
answer. Altered cocycle and nonadjacent-input controls are rejected.
Frame/stabilizer/neighbor errors are at least 166/162/160.

Export / certificate / reducer / probe / final review passed on first
attempts in 29.86/9.19/6.59/15.01/15.22 seconds under 180-second
private-process-group caps. Review 406 binds **661 sources**, preserving
all **643 D110 hashes**. Freeze sources 403--406 and bound artifacts.
Recheck without Sage or Magma, through bounded runner 272:

    python3 dembele/pari/406_dyadic_harmonic_review.py --check

**Next bounded task:** certify the dyadic fixed points of W and an
explicit coordinate change to beta^2=-(2+b). Match that embedding and
its orientation to the saved seventeen CM labels and rational residue
frame using explicit arithmetic/reciprocity witnesses. W's quadratic
equation alone is not a label match. Then use the resulting charts
for a small actual moment pilot with a proved error/contraction bound
over K. Direct exponential Riemann refinement is not the high-precision
plan. The new d=0 bound enters D108's conditional tails but does not
supply moments, cofactor normalization or a Gaussian pivot.

D99's nonhyperelliptic result, D107's complex labels and D106's rational
frame remain proved. Keep D108's spectral rejection and all enumeration,
Hecke-bank and cubic-precision pauses, with the 180-second job cap.
Dyadic equality thresholds, downstream marking, global sections,
norm-97 separation and target-scale torsion remain separate gates.
All seven entry documents, decisions and references are updated.
No correspondence was sent. Earlier next steps are historical.


## Previous checkpoint — D110 explicit dyadic group and moving-vertex transports, 2026-09-25

The user authorized continuing. The bounded group/normalizer and
moving-vertex task is complete. Read
[the D110 proof](dembele/certificates/dyadic-group-transport-d110.md).
No actual Shimura tangent/jet, candidate identification or target
polynomial has been obtained.

**Arithmetic group:** with A=O_F[1/b], R=O[1/b], let G=R*/A* in
PGL2(K) and Gamma=image(R^1). D99's class-number-one and positive-unit
square facts give Gamma=ker(v(Nrd) mod 2). The localized normalizer
N_B(R)/F* equals G. Over the completed maximal unramified extension,
Cerednik--Drinfeld gives S=Gamma\Omega and C=G\Omega. The odd coset
acts as w_p. This is geometric uniformization, not new CM labeling
or a descent matrix. R, not the definite maximal order O at p, is
the order normalized by the new witness.

**Exact same-session arithmetic:** export 400 reconstructs the existing
58-class calculation, because D99 did not serialize representatives.
Its Brandt matrix and stabilizers match D99 entry for entry, and its
order basis matches D109. The walk [0,1,3,4,4,3,1,0] is a shortest odd
closed walk at class 0. Four right ideals of norms 1,2,4,8 and seven
quaternions are exported. Exact 32-by-32 inclusions prove
pi*I_i subset t_ji*I_j subset I_i, both Z-indices four.

**Explicit Atkin--Lehner coset and transport:** set

    c=(b^7-7*b^5+14*b^3-7*b)/2,       c^2=1-b^2/4,
    W=(1+b/2)*i+c*j,                 W^2=-(2+b),
    u=(1-i-j-k)/2,                   g=W*u*W^(-1).

W belongs to R*, has reduced norm 2+b, and projective order two.
It supplies the odd coset and G=Gamma semidirect <[W]>. It moves the
base vertex seven edges. The element g belongs to R^1 and moves the
base vertex fourteen edges; it has projective order three. The fixed
D109 splitting certifies explicit target lattices and integral
transitions, with error lower bounds 169 and 162. All membership and
inverse checks use exact dyadic order coordinates.

The derived element h=u*g=(1-c)/2-(1+c)*i/2+b*j/4-b*k/4 is hyperbolic:
its norm is one and its trace 1-c has valuation -7. It has translation
length fourteen and displaces the base vertex fourteen edges. Thus
there is now an explicit infinite-order arithmetic action, as well
as finite-order transports. These elements are not a complete
generating set or a full fundamental domain.

Export / certificate / independent probe / final review passed on
their first attempts in 28.77/8.03/2.88/3.11 seconds, under 180-second
private-process-group caps. Review 402 binds **643 sources**, preserving
all **629 D109 hashes**. It checks 4096 right-order products, seven
ideal sandwiches, normalization, localized conjugation matrices,
entry valuations and lattice equalities. Odd-parity and false
base-stabilization controls are rejected. Freeze sources 400--402
and bound artifacts. Recheck without Sage or Magma:

    python3 dembele/pari/402_dyadic_group_transport_review.py --check

**Next bounded task:** export and certify the remaining adjacency
transports and vertex stabilizers from the existing 58-class data.
Construct a finite edge-reduction procedure, checking all three
neighbors at every vertex. Then compute G-invariant scalar harmonic
cocycles, with expected dimension 16 and a certified measure bound.
Preserve same-session ideal ordering. This reuses the known quotient;
do not expand the class census, level or Hecke-prime bank.

W^2=-2-b gives an explicit abstract CM embedding, but its fixed points
are not yet matched to the seventeen saved CM labels and rational
frame. Actual moment lifting, cofactor error propagation and a valid
Gaussian chart remain separate gates. D108's evaluator is conditional
and its absolute spectral comparison remains rejected. Keep the
enumeration/Hecke/cubic-precision pauses and 180-second job cap.
Downstream branch marking, global sections, norm-97 separation and
target-scale torsion remain separate. All entry documents, decisions
and references are updated. No correspondence was sent and no jobs
remain running. Earlier next-step instructions are historical.


## Previous checkpoint — D109 integral dyadic splitting and edge transport, 2026-09-25

The user authorized the bounded plan with “proceed with this plan”.
All three deliverables are complete. Read
[the D109 proof](dembele/certificates/definite-dyadic-d109.md).
No actual Shimura tangent/jet, candidate identification or target
polynomial has been obtained.

**Actual definite order:** export 397 obtains the HMF maximal order in
B=(-1,-1)_F, finite discriminant one, with all 32 Z-basis vectors.
Independent checks prove it contains 1, is O_F-stable, is closed under
all 1024 basis products, and has reduced-trace determinant 2^124.
This is the definite algebra, distinct from the complex indefinite one.
No new ideal-class or tree census was run; no class ordering is inferred
from this order export alone.

**Exact integral splitting:** the Magma matrices are proposals only.
Exact rational field arithmetic constructs C,x0,y. For f(t)=t^2+y^2+1,
v(f(x0))=188 and v(f'(x0))=8. Hensel gives an exact root t in K with
v(t-x0)=180. Conjugating [0,-1;1,0] and [t,y;y,-t] by C gives exact
quaternion relations. All order images are integral, with center-error
valuation at least 176, and span M2(F2) modulo pi. Hence
O tensor O_K maps isomorphically onto M2(O_K). Here v(pi)=1, v(2)=8;
176 uniformizer digits correspond to 22 binary digits.

**One actual arithmetic transport:** u=(1-i-j-k)/2 is a norm-one unit
in O, equal to q_0-q_24 in the exported Z-basis. Its matrix reduces to
[1,1;1,0], cycling the three neighboring lines by [2,0,1]. It fixes
the base vertex and carries the edge to L0=[1,0;0,pi] to the edge
to L2=[1,0;1,pi]. The exact transition L2^(-1)*iota(u)*L0 is integral
with determinant one; its error lower bound is 175. This is a
stabilizer edge transport, not a side-pairing of a full domain.

Sources 397--399 and bound artifacts are frozen. Export / certificate /
independent probe / final review passed in 0.63/6.15/0.78/1.04 seconds,
under 180-second private-process-group caps. Review 399 binds **629
sources**, preserving all **606 D108 hashes**. Wrong-root and
wrong-target controls are rejected. One approximate-equality failure
and two timeouts at the direct 32-basis mapping check are archived
with original sources and receipts. None produced a result artifact;
the successful export uses four algebra matrices and exact checks.
Recheck without Sage or Magma:

    python3 dembele/pari/399_definite_dyadic_review.py --check

**Next bounded task:** instantiate D99's arithmetic group and
Atkin--Lehner/normalizer quotient in these matrix coordinates, reconcile
it with the saved 58-class Brandt data, and certify one transport that
moves the base vertex. Preserve same-session ideal ordering when
exporting representatives. Use the existing HMF get_rids/get_tps
interface; no full new tree census is justified yet. D99 already
establishes the abstract group and geometric graph correspondence;
the missing work is explicit arithmetic action and side-pairing data.

The evaluator still needs invariant harmonic cocycles and their measure
bound, dyadic CM/residue-frame matching, certified moments, cofactor
error propagation and a valid Gaussian chart. D107's complex labels
and D106's rational frame remain proved. D108's moment formula remains
conditional; inert-31 precision thresholds cannot transfer numerically
to 2. Its rejection of the unchanged absolute spectral comparison
remains in force. Retain enumeration/Hecke/cubic-precision pauses.
Downstream branch marking, global sections, norm-97 separation and
target-scale torsion remain separate. Decisions, references and all
entry documents are updated. No correspondence was sent and no jobs
remain running. Earlier next-step instructions are historical.


## Previous checkpoint — D108 evaluator feasibility and dyadic jet interface, 2026-09-25

The user authorized continuing after D107. Read
[the D108 proof and evaluator contract](dembele/certificates/shimura-evaluator-d108.md).
D107's CM labels and D106's rational frame remain proved. No actual
Shimura tangent/jet, candidate identification or target polynomial
has been obtained.

**The proposed spectral refinement fails a necessary condition.**
At the required lowest-weight-two discrete series, mu=1,

    H_N(1)=8*pi/N*K1(Z0*N),
    H_31(1)=462.99971524852148... .

This is the completed Mellin integral, with cancellation retained.
The comparison transform has global maximum
4*pi*(5-2*sqrt(6))=1.269461224... over every p>2. The seven omitted
norm-31 primes therefore force a comparison floor above **460891.49**,
or **60.32 times** the saved partial. Even finite-place exponent zero
leaves a floor above 316578.20. This applies to the retained absolute
Hecke envelopes and unsigned geometric diagonal bound, including
positive mixtures of the power kernels. It is not a lower bound
on the actual omitted sum or an impossibility theorem for Nelson's
method. A single required parameter suffices for rejection; it does
not validate a full-spectrum upper bound.

Do not build the full-spectrum version of that same comparison or
repeat its contour scan. A complex-route restart needs additional
joint Hecke cancellation, a different diagonal estimate, or another
change to the stated hypotheses. D98's old full enclosure is unchanged
and still contains zero; its saved-family error alone exceeds the
partial. No new quaternion classes or Hecke coefficients were computed.

**A conditional dyadic local evaluator is now explicit.** For
K=F_p, pi=b and beta^2=-2-b, the Eisenstein polynomials give
v(pi)=1, v(2)=8 and v(beta)=1/2. The three boundary charts
t=pi*x, t=1+pi*x and t=1/(pi*x) cover P1(K), x in O_K.
A bounded harmonic measure, with v(mu(B))>=-d, gives the Poisson
differential f(z)dz. Its moments through index J known to absolute
precision P give ordinary Taylor order k with error at least

    min((J-k)/2-d, P-(k+1)/2).

For w=(z-beta)/(z+beta), u=w^2, the first three coarse coefficients
are g_j=beta*sum_(k<=2j+1) (2*beta)^k*binom(2j+2,k+1)*f_k.
Their error is at least **min((J+1)/2-d,P)** for J>=5. This accounts
for the dyadic factor two in du; N uniformizer digits are only N/8
binary digits. Coordinate/field-arithmetic errors must also be enclosed.

Four exact controls in the CM field use synthetic three-atom measures,
not Shimura data. A first negative control failed because a sign flip
introduces a factor 2 of valuation eight and is invisible at low
precision. The corrected run detects it at J=31 and rejects omission
of the infinity chart at all four tested precisions. The failed source,
receipt and log are archived; no result artifact came from that run.

Main 394 / corrected 395 / probe / final 396 passed in
7.47/2.97/0.09/0.38 seconds under 180-second private-process-group
caps. Review 396 binds **606 sources**, preserving all **588 D107
hashes**. It independently reconstructs conservative rational
quadrature errors, pi/radical bounds, the comparison floor and
formal valuation/coordinate identities. Arb centers and Sage field
controls are bound, not independently recomputed. Sources 394--396
and bound artifacts are frozen. Recheck:

    python3 dembele/pari/396_shimura_evaluator_review.py --check

**Next bounded task:** export the actual definite quaternion order,
construct and certify its integral dyadic splitting into M2(O_K),
and verify one dyadic vertex/edge transport witness. Inspect the
existing HMF `InternalHMFRawDataDefinite`/`RightIdealClassReps`
interface; do not assume its level-one `SplittingMap` is the required
local splitting. Reuse the existing 58-class data. D99 exported a
Brandt matrix and stabilizer orders, not boundary matrices/transports.
No full new tree or quaternion census is justified yet.

Masdeu--Torrents (arXiv:2510.09356) provides a general totally-real
tree-domain algorithm. Its public implementation is documented but
has not been pinned, inspected or run here. Franc--Masdeu's Q_p
moment/control machinery is a framework, not an already justified
port to our ramified degree-eight K. The updated arXiv harmonicity
correction matters. These references and their limited uses are
recorded in the source ledger.

An actual evaluator still needs the correct arithmetic group and
normalizer quotient, invariant harmonic cocycles and their bound d,
dyadic CM/frame matching, certified moment lifting, error propagation
through cofactors, and a valid Gaussian pivot. D107's complex matching
does not provide a dyadic embedding matrix. D106's inert-31 valuation
thresholds must not be reused at 2 without the local-degree conversion.
Retain enumeration/Hecke/cubic-precision pauses. Downstream branch
marking, global cubic/section data, norm-97 separation and target-scale
torsion remain separate requirements. Decisions, references and all
entry documents are current. No correspondence was sent; no jobs
remain running. Earlier next-step instructions are historical.


## Previous checkpoint — D107 certified CM point/root matching, 2026-09-25

The user authorized continuing after D106. Read
[the D107 proof](dembele/certificates/cm-root-matching-d107.md).
The saved D59 correspondence between the seventeen actual CM points
and the polynomial roots is now certified. In zero-based point order:

    [13,10,15,3,4,16,9,14,2,1,8,5,11,12,6,7,0].

- Conjugation by the quaternion I preserves the exact order and has
  negative determinant at the split real place. Its antiholomorphic
  action preserves D, so D106 marked rigidity identifies it with
  canonical complex conjugation.
- An explicit positive order unit U makes W=U^(-1)I anticommute
  with the reference CM generator. This proves saved point 8 is real.
  Conjugation acts by c -> -c on the seventeen class labels, so it
  is the unique real point and must match the unique real root 2.
- The actual Rickards matrix embedding has lower-left entry
  q_J-q_K*sqrt(b-b^2). Rational Sturm/square intervals prove its
  sign negative for the reference beta: beta=-i*sqrt(2+b).
  Reversing both off-diagonal signs would reverse this orientation.
- Integer Rouche inequalities certify seventeen root disks and a
  CM-beta disk, each of radius 10^-1080. They give
  |kappa_f-gamma|<10^-1000 for the proposed root cycle. Integrality
  and 275090^270<10^2000 prove exact equality by the field norm,
  using the two conjugate complex embeddings.
- Magma and independent Python arithmetic give rank 271 for the
  272 ordered-pair monomials r_i^2*r_j. Their only rational relation
  is the all-ones sum. Distinct directed cycles therefore have
  distinct resolvent values; the stabilizer of gamma proves the
  proposed cycle is an actual Galois automorphism.
- Independent Hensel lifts modulo 31^8 identify it as arithmetic
  Frobenius at (31,beta-19). That prime has class 3 in the saved
  generator. Reciprocity propagates the real reference point to
  recover exactly the old lookup, without the old complex/p-adic
  root-order comparison.

The labels now identify D106's rational residue frame in the saved
complex point order. Applying its cofactor recipe to **true**
differential evaluations gives that frame up to a common scalar.
The old approximate differential bank and change matrices are still
uncertified; no actual frame matrix, tangent, higher jet or particular
nonzero G12 was obtained. Some one of the fifteen Gaussian charts
is valid, by D105.

Real-structure/rank/witness/probe/final-review jobs passed in
4.30/1.06/3.97/1.60/1.90 seconds, under the 180-second private
process-group cap. Review 393 binds **588 sources**, preserving
all **562 D106 hashes**. Two initial implementation failures, their
source snapshots and receipts are archived. Sources 390--393 and
bound artifacts are frozen. The audit checks finite witnesses;
the geometric uses of rigidity and reciprocity are proved in the
report, not machine-verified. Recheck:

    python3 dembele/pari/393_cm_root_matching_review.py --check

**Next task:** establish an executable independent Shimura
tangent/jet evaluator in this identified rational frame. First
specify the evaluation mechanism, its complete error bound and a
certifiable Gaussian chart; then run a bounded pilot. The existing
complex route still needs D98's completed spectral multiplier pilot,
covering all principal/complementary parameters, the surviving
discrete series and the infinite norm remainder. Point sampling
or another contour scan does not meet that gate. An arithmetic
alternative must produce actual Shimura differential data; root
Hensel lifting alone supplies no such evaluator.

D106's degree-17 height bounds remain available: sufficient inert-31
valuations are 3257,9746,16236 for positive orders 1,2,3, so common
precision 9746 suffices for D88's J3 test in a matched valid chart.
These are sufficient bounds, not achieved errors, minimum precision
or a reason to request thousands of digits before a method exists.

No candidate identification or target field polynomial has been
obtained. D98's full enclosure still contains zero. Retain the
enumeration/Hecke/cubic-precision pauses; D107's small-degree root
certificate did not restart those jobs. Even after (C,D)
identification, P32/degree-nine branch matching, exact global
cubic/section data, norm-97 separation and target-scale torsion
remain separate tasks. Decisions, references and entry documents
are updated. No correspondence was sent and no jobs remain running.
Earlier next-step instructions are historical.


## Previous checkpoint — D106 rational CM frame and higher jets, 2026-09-24

The user authorized “continue” after D105. Read
[the D106 proof](dembele/certificates/cm-rational-frame-jets-d106.md).
The actual marked curve now has **Aut(C_Qbar,D)=1**, giving a
compatible Q-descent of the given F-model without D56's unproved
ordinary-point and moment hypotheses.

- Stable automorphisms specialize faithfully, including at residue
  characteristic 2. The special components are P1 with three distinct
  nodes, so Aut(C_Qbar) injects into the graph group of order 64.
  This does not use Dembélé's admissibility/exponent refinement.
- The D-preserving subgroup is a 2-group acting on seventeen points,
  so has a common fixed point. Its common fixed set is stable under
  the transitive CM Galois action, hence is all of D. D105's projective
  frame and D99's canonical embedding force the subgroup to be trivial.
- D58 already supplies geometric marked Q-descent by canonical
  conjugation and marked descent. The unique D-marked comparison
  is F-defined. This closes the F-twist ambiguity; no explicit descent
  matrices or candidate identification were computed.
- The residue field of D is uniquely Q-isomorphic to the saved
  degree-17 field L=Q(theta): the order-16 point stabilizers in
  AGL1(F17) are conjugate and self-normalizing, so Aut_Q(L)=1.
  Residues of h*omega, with poles(h)=D, identify the canonical space
  with ker Tr_(L/Q). The saved trace-centered basis defines a rational
  CM frame, unique up to one common scalar.
- This abstract identification does **not** certify the old numerical
  CM-point/root correspondence or prove that the old analytic frame
  is this rational frame. A computational embedding still needs matching.
  The degree-272 auxiliary field H is unchanged and remains solvable.

The first three positive-order Taylor coefficients in a valid ratio
parameter have height below **10504, 31518, 52533**. The higher formulas
are integral sections before division by 2!/3!, with line powers
omega^9*T^6 and omega^15*T^10. Formal series reversion, nonlinear
coordinate changes and common-factor controls pass.

Magma 388 computed exact **candidate-only** ratio jets through t^3.
Review 389 independently checks all 91*4=364 quadratic coefficient
identities, the D101 first derivative and D88 mod-31 coefficients.
D88 already normalized X1=1 and used t=X2/X1-r2(P): compare its
second coefficient directly, with no extra raw-X1 factor.
The mod-31 product ranks are **17,34,45,45**.
Candidate heights are below **677,1947,3218**.

Since 31 is inert of residue degree 17 in L, sufficient valuations
of the actual-minus-candidate differences are **3257,9746,16236**,
respectively. Thus common precision 31^9746 suffices for D88's J3
rank certificate, and 31^16236 for J4. These are conservative
sufficient bounds, not minimum precision or achieved accuracy.
The rational frame, matched local embedding and valid common chart
are necessary. G12 is still not certified on the actual curve;
some one of the fifteen ratio pivots is nonzero.

Main 387, Magma 388, candidate probe and final review passed in
0.15,42.91,1.11,1.42 seconds under the 180-second private process-group
cap. Review 389 binds **562 sources**, checking all **543 D105 hashes**
unchanged. The initial 387 syntax failure, source snapshot and receipt
are preserved. Completed sources 387--389 and bound artifacts are
frozen. The finite audit does not machine-verify the geometric proof
or cited theorems. Recheck:

    python3 dembele/pari/389_cm_ratio_jet_review.py --check

**Next task:** obtain an independent arithmetic Shimura tangent/jet
evaluator, starting with a certified rational-frame tangent and chart.
A useful bounded prerequisite for reusing the analytic route is an
exact reciprocity proof of the saved CM-point/root orientation.
Do not infer that orientation from the abstract uniqueness above.
The inert-31 equality test is available, but no 31-adic Shimura
evaluator has been implemented. Do not request thousands of precision
digits before establishing the actual evaluation mechanism.

No actual Shimura tangent or higher jet, candidate identification,
or target field polynomial has been obtained. D98's full enclosure
still contains zero; retain its spectral pilot gate and the existing
enumeration/Hecke/cubic-precision pauses. Even after (C,D)
identification, the candidate P32 and degree-nine branch marking,
exact global cubic/section data, norm-97 separation and target-scale
torsion remain separate tasks. Decisions, references and all entry
documents are updated; no correspondence was sent and no jobs remain
running. Earlier next-step instructions are historical.


## Previous checkpoint — D105 actual CM frame and tangent atlas, 2026-09-24

The user authorized continuing after D104. Read
[the D105 proof](dembele/certificates/cm-frame-arithmetic-d105.md).
For the actual genus-16 quotient and its seventeen-point CM divisor,
**H0(K_C-D)=0**, and all seventeen maximal evaluation cofactors are
nonzero. The projective-frame hypothesis is now proved.

- The nine inverted dyadic annuli each contain two simple generic
  fixed points. The proof uses an annulus unit and zero-counting
  argument in characteristic zero; it permits residue characteristic 2.
  Kurihara's integral quotient theorem gives their specialization.
- After stabilization, the branch divisor is twice the sum of nine
  specified midpoints. Subtracting P32 gives nine possible marked
  divisors. All nine have noneffective K-D: exact integer potentials
  and burning orders give root coefficients -3,-2,...,-2. This avoids
  guessing which midpoint receives P32. CM transitivity upgrades full
  rank to all nonzero cofactors.
- An auxiliary class-field argument identifies the splitting field of
  the degree-17 polynomial with the Hilbert class field H of the
  degree-16 CM field M; [H:Q]=272. It uses the proved D59 group and
  class number, an exact degree-16 resolvent identity, and unramifiedness.
  No numerical orientation or disputed hyperellipticity claim enters.
  H is the solvable CM auxiliary field, not the nonsolvable target.
- Any fixed bijection of CM points and roots defines a frame over H.
  D103--D104 give projective tangent height **h(Lambda)<10504** for it.
  Nonhyperellipticity guarantees at least one of fifteen Gaussian
  charts works. This does not certify the saved D59 root orientation,
  the particular G12 pivot, or descent of the frame to F.
- Candidate projective height is below 677. In a consistently labelled
  common valid chart over H, sufficient absolute errors are
  **10^(-1320873)** at one embedding, or **10^(-4857)** at every
  embedding of H. These are sufficient conservative thresholds, not
  minimum precision, existing errors or evaluator cost. The latter
  condition includes the transported frame, not merely seventeen
  numerical values at one complex place.

Probe 384 and main 385 passed in 0.35 and 0.95 seconds. Audit 386 passed
on its first computational attempt in 0.71 seconds, under the
180-second private process-group cap. It reconstructs the marked graph
from Brandt entries, verifies witnesses without the reduction solver,
rejects three corruptions, evaluates the resolvent exactly, and replays
the integral-order calculation. It binds **543 sources**, verifying
all 479 D99 and 53 D104 hashes unchanged. The gamma power-basis
determinant is 5 modulo 101. Computations do not machine-verify the
geometric lemmas or cited theorems. Recheck:

    python3 dembele/pari/386_cm_frame_arithmetic_review.py --check

**Next task:** assess and implement an independent tangent/jet
evaluator with a feasible exact-equality mechanism, keeping the
H-frame and chosen bijection explicit. A numerical chart must be
certified before division. Higher jets need their own exactness bounds
or identities. For D88 over H with arbitrary labels, check the required
jets at all seventeen points; do not infer them from one point without
equivariance/descent. Certifying D59 labels remains useful for smaller
fields and Galois propagation, but is no longer a prerequisite for
the qualitative frame or the projective height theorem.

No independent tangent, candidate identification or F descent has been
obtained. D98's full enclosure still contains zero; the spectral pilot
gate remains unmet. Do not restart it on qualitative nonvanishing alone.
Retain enumeration/Hecke/cubic-precision pauses. Global cubic/section
data, norm-97 separation, target-scale torsion and the final field
polynomial remain open. Sources 384--386, their reports and completed
artifacts are frozen; the original conditional probe is preserved as
such. Decisions, references and entry documents are current. No
correspondence was sent. Earlier next-step instructions are historical.

## Previous checkpoint — D104 intrinsic CM height, 2026-09-24

The user authorized “keep going!” after D103. Read
[the D104 proof](dembele/certificates/cm-intrinsic-height-d104.md).
The stable coarse-canonical CM fibre now has the numerical upper bound

    H_CM,disk <= 2*h_L(Q)+log(2) < 41/10.

Together with D103 this gives **h(v_j)<10504**, still conditional on
the intended arithmetic CM field labels, all nonzero evaluation
cofactors, and the chosen nonzero Gaussian denominator. No independent
Shimura tangent or candidate identification has been obtained.

- A generic finite map extends between stable models by
  Liu--Lorenzini Proposition 4.4(a). Its differential extends integrally
  between dualizing sheaves: at a target node use d(u)/u and check
  vertical codimension-one points. Differentiate this map at the
  ramification section to obtain W_C -> W_S^2. It is integral even
  at 2 and at nodal sections; its archimedean norm is 2.
- Auxiliary sufficiently small levels, maximal at each prime under
  consideration, compare the stable upstairs fibre with the canonical
  Hodge line. Yuan--Zhang Theorems 4.5/4.7 provide semistable models,
  dualizing normalization and level compatibility. These structural
  results do not exclude common CM/quaternion ramification.
- Zhao Theorem 7.4 plus the published nearby-type and averaged Colmez
  identities give h_L=-R/8+log(2)/16, where R=L_f'/L_f(0,chi_M/F).
  The CM field M has degree 16, discriminant 2^79 and relative
  discriminant norm 2^17. Do not confuse it with the degree-17
  residue field. Absolute height divides by [K:Q]; Yuan--Zhang's
  Shimura-point height instead divides by [K:F].
- Zhao v1's last display in the proof of 7.5 omits d_Sigma from
  log(d_B*d_Sigma). The earlier 7.4 and statements 1.1/7.5 retain it.
  D104 derives its formula from 7.4, retaining the factor. This is
  our reconciliation, with no author confirmation. The older
  CM-point formulas excluding common ramification remain unused.
- Eight primitive odd characters of conductor 64 reduce R to an exact
  rational combination of log-Gamma values. The main finite-product
  enclosure and independent Taylor-series enclosure both prove
  h_L<17/10. Candidate data is not used for the target-height bound.

Audit 383 also bounds the exact candidate tangent heights by 683.
Assuming the correctly labelled common field has degree at most 136,
sufficient absolute errors are 10^(-660791) at one embedding, or
10^(-4859) at every embedding. These are conservative sufficient
thresholds, not minimum precision or evaluator cost estimates. No
actual tangent enclosure presently meets them.

Recheck:

    python3 dembele/pari/383_cm_intrinsic_height_review.py --check

The main and audit jobs passed in 1.09 and 1.11 seconds under the
180-second private process-group cap. Audit 383 binds 53 sources,
recomputes character traces using generator 3 and a conjugate-product
inverse, and checks all 45 D103 hashes unchanged, including transitive
D102/D101 sources. Both computational jobs passed on their first
attempts. Sources 382--383 and bound artifacts are frozen. No external
correspondence was sent.

**Next mathematical task:** establish the actual arithmetic CM
labelling and qualitative frame/chart nonvanishing, then assess an
independent evaluator against a rigorous equality threshold. The
intrinsic height comparison is now available; do not repeat it or
the per-prime residue-index search just to instantiate D103. D98's
full enclosure still contains zero and the spectral pilot gate remains
unmet. Keep the enumeration/Hecke/cubic-precision pauses. Candidate
identification, exact global cubic/section data, norm-97 separation,
target torsion and the final polynomial remain separate gaps.
Decisions, references and entry documents are current. Earlier
next-step instructions below are historical.

## Previous checkpoint — D103 adjugate tangent-height bound, 2026-09-24

The user authorized continuing after D102. Read
[the D103 proof](dembele/certificates/cm-adjugate-height-d103.md).
The height argument now avoids separately bounding the residue index
or the inverses of the evaluation minors. It gives the conditional
inequality

    h(v_j) <= 513*H_CM,disk + 8400.

H_CM,disk is the normalized degree of the actual stable coarse-canonical
CM fibre, with ||d(z^2)||=1 in a centered uniformizing disk. **It is not
yet numerically bounded.** The arithmetic field labels, all nonzero
evaluation cofactors, and the chosen nonzero Gaussian denominator
remain hypotheses. No independent tangent or candidate identification.

- Use s_j=adj(Phi_r)*V_j with V_ij=sigma_i(17*eta_j), retaining its
  arithmetic line T=(tensor W_i)^15 tensor (det E)^(-16).
  These sections are integral and differ from the intended canonical
  frame by one common factor. Gaussian ratios cancel that factor.
  Their fibre line has height 513*H_CM,disk-32*h_Fal(C). The integral
  nodal Gaussian map requires no division by 2.
- Every CM embedding beta^2=-pi yields a uniform displacement bound:
  the perpendicular part q of alpha in O^1 has 4*Nrd(q) integral,
  compact conjugates between 0 and 4, and split norm at most -2^-16
  when alpha moves the CM point. The normalizer and norm-one orbits
  agree there. Thus rho=1/1024 is an embedded disk modulo its order-two
  stabilizer, uniformly over all points and conjugates.
- Disk integration gives evaluation norm <=2^20 and Gaussian
  evaluation norm <=2^60. The saved field basis gives |17*eta_j|<2^35
  at every embedding. Bost's universal lower Faltings-height bound
  eliminates the Hodge determinant term. No upper curve-height bound
  is needed for this route.
- These are a proved conditional height theorem and exact controls,
  not actual computed Shimura sections. D102's index formula remains
  valid; its geometric defects simply need not be bounded separately
  to use this new inequality. Quantitative conditioning may still be
  needed for a later numerical inversion.

Recheck with:

```sh
python3 dembele/pari/381_cm_adjugate_height_review.py --check
```

Script 380 passed in 0.24 seconds. Audit 381 passed in 0.40 seconds,
with independent dense frames in ranks 3 and 16, Horner field bounds
and rational integration/constants. It binds 45 sources and verifies
all 12 D102 and 22 D101 hashes unchanged. The initial 0.04-second
failure was a deliberately required nonzero bracket failing for
accidentally proportional toy jets; the original source snapshot,
log and receipt are preserved. All jobs used 180-second private
process-group caps. Completed sources 380--381 and bound artifacts
are frozen. No correspondence was sent.

**Next mathematical task:** compare H_CM,disk with the arithmetic
Hodge height in Zhao's theorem, including the genus-40 norm-one to
genus-16 normalizer quotient and its wild dyadic fibre, then bound
the result. The generic relation u=z^2 does not prove an integral
fibre comparison on the stable/Hodge models. In particular, do not
assert H_CM,disk<=2*h_Hodge without that proof. Zhao permits the
common ramification; Yuan's excluded CM-point formula remains excluded.
Do not return to per-prime residue-index bounds just to instantiate
D103. No new spectral pilot is justified yet; D98 still contains zero.
Keep the enumeration/Hecke/cubic-precision pauses. Exact global cubic
coefficients, norm-97 separation, target torsion and the final polynomial
remain separate gaps. Decisions, references and entry documents are
current. Earlier next-step instructions below are historical.

## Previous checkpoint — D102 integral residue frame, 2026-09-24

The user authorized continuing the plan after the tangent explanation.
Read [the D102 result](dembele/certificates/cm-residue-lattice-d102.md).
This continues D101's arithmetic-normalization task. It supplies an
exact local index formula and new field arithmetic, but no effective
bound on the actual Shimura frame or independent tangent.

- Over a DVR, under the stated model/divisor hypotheses, the residue
  index length is length H1(O(D)) + v(Norm(a)), where a is the primitive
  principal part of the generator of H0(O(D))/R. The target lattice is
  the trace-zero codifferent. Both defect terms must be controlled;
  globalizing also retains the rank-one pencil lattice.
- Fixed smooth genus-two and nonhyperelliptic plane-quartic examples
  have unbounded residue indices at good primes, with etale split
  marked divisors and H1(O(D))=0. They are local varying-divisor
  controls, not CM or degree-17 closed-point counterexamples.
- Script 378 independently checks the saved degree-17 field order:
  irreducibility modulo 31, all 153 unordered basis products, trace
  discriminant 2^79, trace ideal Z, and trace-dual clearing integer 32.
  The saved centered basis eta_i needs the common factor 17 to enter
  the trace-dual lattice; its scaled trace-zero index is 2^79*17^15.
  These are abstract-field lattice facts, not tangent denominators or
  an identification of the actual horizontal order at 2.
- The cofactor product det((diag(c)*E)_r)=(-1)^r*product(c_i) supplies
  an explicit archimedean inverse bound. It requires certified lower
  bounds for the evaluation minors and compatible arithmetic norms.
  The old empirical condition numbers do not supply them.

Recheck with:

```sh
python3 dembele/pari/379_cm_residue_lattice_review.py --check
```

The review independently computes traces from multiplication operators
and determinants by Bareiss, checks the plane-quartic control, and
binds 12 sources. All 22 D101 bound source hashes remain unchanged.
The initial arithmetic and review jobs passed in 0.56 and 0.63 seconds,
under the 180-second private process-group cap. Sources 378--379 and
bound artifacts are frozen. No failed jobs or correspondence.

**Next mathematical task:** bound or compute the principal-parts norm
and the cohomology Fitting ideal on the actual marked C_ar, with its
pencil and horizontal-order comparisons, then the compatible
archimedean minors/norms. Alternatively construct the arithmetic
Gaussian-section restriction map. The known field trace lattice no
longer needs investigation. D101's height comparison and Gaussian
denominator still need their actual arithmetic inputs. No further
spectral pilot is justified yet; D98's enclosure still contains zero.
Keep all enumeration/Hecke/cubic-precision pauses. Global cubic
coefficients, norm-97 separation, target torsion and the polynomial
remain separate gaps. Decisions, references and entry documents are
current. Earlier next-step instructions below are historical.

## Previous checkpoint — D101 CM-tangent exactness, 2026-09-24

The user authorized execution of D100's first bounded task. Read
[the D101 result](dembele/certificates/cm-tangent-exactness-d101.md).
The investigation is complete, but it did not establish an effective
recognition bound or obtain an independent Shimura tangent. Earlier
next-step instructions below are historical; this section governs
resumption.

- The first Gaussian map expresses the tangent as ratios of algebraic
  sections of 3K_C. Its dimensions are 120 -> 75. At the order-two
  point, pullback multiplies the local bracket by 8*z^3; evaluating the
  upstairs bracket at zero would lose the needed coarse value.
- A conditional norm certificate is explicit: if M*(actual-candidate)
  is integral and all conjugate errors are bounded by E_sigma, then
  M^d*product(E_sigma)<1 proves equality. All-conjugate enclosures plus
  a denominator bound can replace a separate height bound. The unknown
  coefficient may require absolute degree 136 over F, not the
  candidate's degree 17. Field/descent hypotheses remain essential.
- A conditional Arakelov inequality exposes the missing inputs: the
  integral clearing ideal and compatible norms of the actual CM-framed
  sections, plus the coarse-canonical/CM-height comparison. The
  residue-frame lattice index has not been bounded. Intrinsic height
  formulas do not supply that coordinate comparison automatically.
- Zhao's maximal-level CM-height theorem permits our common
  ramification at 2. Yuan's quoted CM-point Theorem 1.2 excludes it;
  do not apply that latter formula. Yuan's separate curve-height
  theorem remains relevant. The PEL restriction alternative still
  needs actual global sections and CM test objects.
- Magma 375 computes the exact *candidate* tangent. Its clearing
  integer has 269 digits in the saved integral lattice, 285 in the
  power basis. This is neither an unknown-target bound nor a minimum
  required precision. Python 376 independently verifies all 91
  linearizations, basis conversion, uniqueness and agreement with D88
  modulo 31. The candidate is neither identified nor refuted.

Recheck with:

```sh
python3 dembele/pari/377_cm_tangent_exactness_review.py --check
```

The review audit binds the new proof, source ledger and candidate
arithmetic, and replays the Gaussian/norm controls and the exact
2-Eisenstein ramification test. Magma passed in 8.81 seconds; the
bounded independent recheck took 1.92 seconds. An initial multiline
output parser failure is preserved and was fixed by collecting the
same successful arithmetic job. No old bound outputs were changed.

**Next mathematical task:** bound the actual residue-frame lattice
index and compatible archimedean norms, using the newly reviewed
height formulas where their hypotheses hold, or construct the
arithmetic Gaussian-section restriction map. No further spectral
pilot is yet justified by this exactness task. D98's enclosure still
contains zero. Keep the 180-second process-group cap and the existing
enumeration/Hecke/cubic-precision pauses. Global cubic coefficients,
norm-97 separation and target-scale torsion remain separate gaps.
Completed sources 375–377 and bound results are frozen. Decisions,
references and entry documents are current; no correspondence was sent.

## Previous checkpoint — D100 construction methodology review, 2026-09-24

The user asked to step back and revisit the construction methodology.
Read [the D100 review](dembele/certificates/construction-methodology-d100.md).
This is a strategic review, not a new arithmetic certificate or a request
to resume heavy computations. This section supersedes earlier next-step
instructions; all bound sources and results remain unchanged.

**Execution-readiness follow-up:** no further broad planning is needed.
Use [D100 section 7](dembele/certificates/construction-methodology-d100.md#7-execution-readiness-first-bounded-task)
as the first bounded research task. Establish an exactness mechanism
for the independent CM tangent: first assess an effective separation
bound or exact verification identity for the existing Nelson/Shimizu
route, including the arithmetic frame and CM labels. A missing bound
or model must be recorded explicitly before considering an arithmetic
restriction-map alternative; do not automatically resume the spectral
pilot. A usable mechanism leads to the tangent computation and then
the three/four-coefficient criterion. DECISIONS and REFERENCES include
this follow-up. No new arithmetic result or ready exact evaluator is
claimed.

Retain the Shimura/Jacobian route as the most developed concrete route,
with three distinct gaps: identifying the marked arithmetic candidate,
constructing exact global cubic/section data, and demonstrating actual
target torsion at genus 64 and the required residue extension. D51 proves
the original kernels occur on the canonical Y; it does not identify our
candidate with that Y. The first natural polynomial has degree 257 over
F, followed by normal closure over Q. No hyperelliptic model is needed.

The next research objective is an executable independent arithmetic
identification certificate. D88 supplies a finite acceptance criterion:
four coarse CM coefficients, or three with rank 45 and the correct
quadratic kernel. It still needs the arithmetic frame, independent
expansions, and an exact equality mechanism. A useful analytic anchor
alone would not supply those. D98's completed spectral multiplier is
one possible experiment, no longer an automatic construction next step.
The full error bound remains <24,784,942,340 and contains zero.

After marked X -> C identification, D88's nine-cover shortcut applies,
but exact cubic coefficients still need construction. D86's verified
31^128 lift and negative bounded-height recognition remain current.
Genus-64/degree-51 target arithmetic is untested; the norm-97 full Euler
cofactor separation also remains to be completed. Keep these separate
from the existing smaller backend controls.

No new arithmetic computation was performed for D100. Existing audits
remain the evidence for their respective checkpoints. Preserve the
180-second process-group cap and enumeration/Hecke/cubic-precision
pauses. Do not repeat D99 without new contrary evidence. An alternative
direct certification of the original residual kernel could bypass full
curve identification, but no such effective certificate is implemented.

## Previous checkpoint — D99 hyperellipticity review, 2026-09-24

The user asked to revisit the entire hyperelliptic/nonhyperelliptic
argument from scratch. That review is complete. Read
[the D99 proof and evidence ledger](dembele/certificates/hyperellipticity-review-d99.md).
**The intended genus-16 quotient C is geometrically nonhyperelliptic.**
This is an exact reduction-graph argument; candidate identification
remains a separate open problem. The D100 section above governs resumption.

- Fresh Magma computation 371 rebuilds the norm-2 Brandt matrix on
  58 classes without old graph or candidate inputs, with unconditional
  class-number and exact mass checks. It uses the same HMF library,
  not an independently implemented Brandt algorithm.
- New standard-Python script 372 reconstructs the upstairs graph,
  Atkin--Lehner quotient and stable core: 30 vertices, 45 edges, genus
  16, simple and cubic. All 1,035 deletions of one or two edges leave
  it connected. A tree quotient by an involution would force such a
  cut. Baker specialization and Chan's metric-graph theorem therefore
  prove nonhyperellipticity, for every positive choice of edge lengths.
- A separate new exhaustive automorphism search recovers 64 elements,
  19 involutions and quotient Betti histogram 8:5, 10:4, 12:6, 14:4.
  Both quotient conventions and positive/negative controls pass.
- Kurihara's original scanned Proposition 3-2 / Lemma 3-3, Nekovar's
  reduction description, Baker and Chan were reread. Torsion at 2 is
  permitted; only self-reversing oriented edge classes disappear.
  No tame fixed-point count or faithful specialization of curve
  automorphisms is needed.
- The published Theorem 5.9 confuses upstairs t with coarse u=t^2.
  The differential u du has order one downstairs and invariant pullback
  2t^3 dt. Its asserted vanishing-order premise does not follow.
- Script 373 reruns the saved-order arithmetic audit (trace determinant
  2^126, maximality, unit signature rank eight). The D69 candidate
  canonical-curve checker also passes again from the exact equations.
  Neither result identifies the candidate with C.

Recheck with:

```sh
python3 dembele/pari/374_hyperellipticity_review_audit.py --check
```

Root `hyperellipticity_review_d99.json` verifies 479 hashes, including
D98's 169, and recomputes the graph and both obstructions. It binds the
mathematical proof and new logs; it does not formally prove the cited
theorems. Successful new jobs took at most 27.34 seconds. The failed
370 attempt (`IsTotallyDefinite` is not a Magma intrinsic) is preserved;
371 corrected it. All jobs finished. Sources 370--374 and bound reports
and artifacts are frozen; old bound files were preserved. Entry docs,
decisions and references are current. No external correspondence sent.

**Next construction task:** D98's completed spectral multiplier remains
the next analytic investigation if construction resumes. D99 changes
no CM enclosure: full S11 error is still <24,784,942,340 and the anchor
is uncertified. Keep the 180-second process-group cap and enumeration,
Hecke-bank and cubic-precision pauses. Do not repeat the hyperellipticity
review without new contrary evidence. Arithmetic CM jets, marked
candidate identification, cubic recognition and the field polynomial
remain open. Use general canonical equations, not a hyperelliptic ansatz.

## Previous checkpoint — D98 spectral ideal bound, 2026-09-24

Read [the D98 proof and pilot](dembele/certificates/nelson-spectral-ideal-d98.md).
An explicit spectral comparison now bounds every omitted norm ideal
while retaining cancellation within its complete Hecke correspondence.
The actual omitted-ideal S11 bound improves by **>272.48** over D96 to
**<24,784,932,714**. Including the unchanged saved-family tails gives
full error **<24,784,942,340**, still about 3.244 million times the
partial sum 7640.7582. The CM anchor remains uncertified. This section
governs resumption; earlier next steps below are historical.

- D95's single component, narrow class number one and positive-unit
  squares identify each complete norm-a family with the unnormalized
  Hecke kernel, including central contents at prime powers.
- For K type four, the radial transform of `Phi*D^(-p)` is
  `h_p(mu)=4*pi*Gamma(p-mu)*Gamma(p+mu-1)/(Gamma(p+2)*Gamma(p-2))`,
  with `lambda=mu*(1-mu)`. Transforming the original S11 integrand
  first produces a factor `lambda+2`; the lowest-weight-four discrete
  series vanishes and the lowest-weight-two series survives.
- A proved vertical Gamma log-concavity inequality controls every
  principal/complementary parameter and both discrete series by the
  positive kernel `h_(c+2)`. No empirical spectral gap or unproved
  infinite signed-count estimate is used. The comparison diagonal is
  at most `1795/1792`, from the existing CM-point packing bound.
- Blomer--Brumley's finite-place exponent `delta=7/64`, together with
  the target form's Ramanujan bound, changes the complete ideal mass to
  `sum d(a)^2*Norm(a)^(-(c-delta))`. Its exact Euler expression converges
  for `c>71/64`, removing the previous absolute orbit-count factor.
  Remove only the unit ideal and the one saved prime (31,b-27).
- Script 368 tests ten contours with 320-bit Arb rectangles and an
  explicit Binet tail. The best tested contour is 5/4; `B(c)<102.082`.
  All vertical tails are <1e-103. More quadrature precision will not
  remove the remaining absolute Mellin/Hecke comparison loss.

**Next:** test the completed spectral multiplier `H_N(mu)` from section
2 of the D98 proof, retaining Mellin cancellation before taking a
uniform spectral majorant and summing the full norm remainder. The
pilot must cover all principal/complementary parameters, the surviving
discrete series and the infinite norm tail. Point samples do not
suffice. Do not repeat D98's contour scan, D97's finite diagnostics,
D96's positive majorant or D95's completed identification. This bound
still does not justify a larger quaternion census or Hecke bank.

Recheck with `python3 dembele/pari/369_nelson_spectral_ideal_audit.py --check`.
Root `nelson_spectral_ideal_d98.json` verifies 169 hashes, all 20,480
rectangle upper endpoints and 107 dyadic interval records. It replays
the transform cancellation, two discrete-series radial equations,
64 Euler coefficients, packing constant, degree-29 tail polynomial,
algebraic powers and the final rational error enclosure. The analytic
spectral proof and Arb evaluations are bound, not re-proved by Python.

Both jobs passed and finished: numerical run <5.38 seconds, root
generation <0.41 seconds. Sources 368--369 and bound report/artifacts
are frozen. No new quaternion/Hecke data, remote work, candidate change
or precision increase occurred. Preserve corrected endpoints, the
180-second process-group limit and cubic precision pause. D95's positive
scalar and conjugated factorial ratio rule remain valid. Arithmetic CM
jets, marked identification, cubic recognition and the field polynomial
remain open. All entry documents, including `dembele/pari/README.md`,
are current.

## Previous checkpoint — D97 signed orbital blocks, 2026-09-24

Read [the D97 report](dembele/certificates/nelson-signed-orbit-d97.md).
The requested signed-cancellation review and bounded pilot are complete.
Exact shell grouping and Abel summation improve the outer saved block
bounds by factors >6.45 (unit) and >8.16 (prime 31). **There is no proved
signed counting bound beyond the saved cutoff.** The actual omitted-
ideal error remains <6.754e12, the CM anchor remains uncertified, and
enumeration expansion is not justified. This section governs resumption;
older next steps are historical.

- Script 363 uses the existing 541 unit and 586 norm-31 classes. Reduced
  conjugation pairs them within 80 and 83 exact displacement shells.
  Their real phase sums are exact field elements, checked from traces:
  `Re(Phi)=1-8*tau+8*tau^2`, `tau=N*Trd(alpha)^2/(4*n*A)`.
  Abel summation retains cumulative phase cancellation before absolute
  values. All finite sums agree with corrected D93 data.
- For the whole ideal families and only N<=A<=25600, the data prove
  `abs(P_1(A))<=A^(2/3)` and
  `abs(P_31(A))<=1.619*(A/31)^(2/3)`. These are neither individual-orbit
  bounds nor infinite estimates. Do not extrapolate them.
- Script 366 certifies an explicit conditional remainder interface.
  If `abs(P_N(A))<=M*(A/N)^theta` holds for every A>=25600, then the
  tail is at most `abs(P_N(T)*f_N(T))+M*J_(N,theta)`. For theta=2/3,
  valid bounds are `0.124645+9.091228*M` for N=1 and
  `0.116890+0.923191*M` for the unweighted prime family. The missing
  premise is not certified by these small transfer constants.
- The phase is the (2,2) Cartan harmonic, depending on both angles.
  Good's finite-volume estimate, recorded by Bourgain--Kontorovich--
  Sarnak, has a 2/3 displacement exponent but also exceptional spectral
  terms and unspecified constants. Gorodnik--Nevo supplies a uniform
  translated-count framework, requiring explicit geometric/spectral
  inputs. Neither has been instantiated as a numerical bound here.
  Even a uniform orbital power saving leaves the same norm-mass
  exponent after absolute Hecke/orbit summation.

**Next:** prove an effective bound for this Cartan harmonic with explicit
constants, exceptional-spectrum control, starting cutoff and uniformity
over the required translates, or prove a direct signed Hecke-block
estimate. Apply it to the remainder interface and complete norm sum
before extending enumeration. Do not repeat the finite diagnostic,
D96's positive-majorant pilot or D95's completed identification. More
quadrature or cubic precision does not supply the missing estimate.

Recheck with `python3 dembele/pari/367_nelson_signed_orbit_audit.py --check`.
Root `nelson_signed_orbit_d97.json` verifies 162 hashes and 2,049 dyadic
interval records, including all D96 provenance. It independently replays
163 exact phase identities, conjugation, finite Abel bounds, finite-prefix
inequalities, 944 algebraic radical bounds, the derivative identity and
far-tail polynomials. The actual global enclosure is rebuilt and contains
zero. Arb analytic errors are bound to the runs.

All four computational jobs finished: two passes, plus two preserved
Sage/Python type-conversion failures in 364/365. Successful computations
took <6.20 seconds each; root generation <1.76 seconds. Sources 363--367
and bound report/artifacts are frozen. No new Hecke/quaternion data,
remote run or candidate change occurred. Preserve exact endpoints, the
180-second process-group limit and cubic precision pause. D95's positive
scalar and conjugated factorial ratio rule remain valid. Arithmetic CM
jets, marked identification, cubic recognition and the field polynomial
remain open. Decisions, references and entry documents are current.

## Previous checkpoint — D96 completed majorant pilot, 2026-09-23

Read [the D96 report](dembele/certificates/nelson-completed-majorant-d96.md).
The bounded summation pilot is complete. Evaluating the completed scalar
kernel and summing the positive ideal majorant reduces the omitted-ideal
S11 bound from 2.6796e13 to **<6.754e12**, an improvement greater than
3.967. This is still about 884 million times the partial sum 7640.7582.
**The CM anchor remains uncertified, and the pilot does not justify a
larger enumeration or Hecke bank.** This section governs resumption;
older next steps are historical.

- Script 360 encloses K3-K4 and the rescaled K4 with degree-31 Taylor
  polynomials on 96 dyadic displacement blocks, 1<=A<=2^96. It retains
  Mellin cancellation before taking absolute values. On 1<=A<=2^72,
  script 361 proves 0<K3<K4 and decreasing K4/A using Bernstein signs
  with rigorous exponential and quadrature remainders.
- D92's disjoint disks imply C_N(A)<=32*A/(7*N) in each right orbit.
  Stieltjes integration gives an orbital majorant in terms of
  F(N)=K4(Z0*N)+integral_N^infinity K4(Z0*A)*dA/A. The complete ideal
  sum uses D_odd(s+1/2); its denominator zeta_F(2s) cancels the scalar
  kernel's zeta factor. This sums all ideal counts without a census.
  Remove the unit and only the saved prime (31,b-27).
- The resulting completed positive scalar sum is about 1.47735e12,
  accurately enclosed. The finite-range splice and all A>2^72
  together cost <1.4e-6. Consequently the large remaining bound is
  not integration error. The original weight and D93 partial sums
  are unchanged. Higher derivative-pair bounds are unchanged.
- The saved unit/prime-31 finite families have cancellation factors
  about 1.064799 and 3.652448. These are local diagnostics, not evidence
  for enormous cancellation among the uncomputed large-norm classes.
  The unit family is dominated by the identity term.

**Next:** review a concrete bound for signed Hecke blocks or quaternion
orbit sums before replacing them by positive counts. Test that mechanism
on existing data and require an explicit remainder estimate before
expanding the computation. Do not repeat this positive-majorant pilot,
the completed D95 global comparison, or increase quadrature/cubic
precision as a substitute. The result is a feasibility failure for
this comparison, not a lower bound on the true omitted sum or a proof
that all Nelson-based methods fail.

Recheck with `python3 dembele/pari/362_nelson_completed_majorant_audit.py --check`.
Root `nelson_completed_majorant_d96.json` verifies 145 source hashes
and 7,505 dyadic interval records, binding the D95 root and new proof
and jobs. The independent rational audit replays 6,840 Bernstein
coefficient signs, exact tail polynomials, directed final bounds and
the saved finite-family diagnostics. Arb evaluations are bound to the
runs. The two computations passed in <11.95 seconds each and the
audit in <4.12 seconds. Sources
360--362 and bound report/artifacts are frozen. All jobs are finished.

D95's global identification up to a positive scalar remains valid.
Conditional on S11!=0, use `c_a/c_1=conjugate(S_(a,1)/S11)/a!`.
Full eigenform evaluation, an arithmetic CM jet, marked identification,
cubic recognition and the field polynomial remain open. Preserve the
corrected D93 endpoints, 180-second process-group limit and cubic
precision pause. Decisions, references and entry documents are current.

## Previous checkpoint — D95 global kernel identification, 2026-09-23

Read [the D95 proof](dembele/certificates/nelson-global-identification-d95.md).
The D90 classical theta integral, and hence the complete D91 Mellin
series, are now identified with the required **nonzero rank-one
Jacquet–Langlands tensor up to a positive scalar**. The remaining
obstacle to a CM tangent is numerical accuracy and a certified nonzero
anchor. This section governs resumption; older pending-identification
flags describe historical checkpoints.

- Re-proved h(F)=h^+(F)=1 with `bnfcertify=1` and checked signature
  rank 8. Thus every totally positive element with even finite
  valuations is a square. This is the hypothesis that removes the
  extra rational similitude variable in the central average.
- Extend phi by `Phi_v(x,u)=h_v(u)*phi_v(sqrt(u)*x)` at real places,
  with normalized positive compact bumps, and by unit support in u
  at finite places. Unfold the central average over rational squares.
  The single global sign quotient gives exactly the classical 1/2
  lattice factor, with the stated measures; no extra regulator occurs.
  Local level, fixed types and the single classical component are
  checked, using Disegni's general-field Shimizu framework and strong
  approximation. The D94 norm-one integral gives a nonzero forward
  Fourier coefficient. Adjointness yields scalar norm(f)^2/norm(v)^2>0
  in the report's classical conventions.
- **Derivative orientation:** the actual complex matrix is
  `[[X,conjugate(Y)],[Y,conjugate(X)]]`. The implemented `(a,1)` pair
  differentiates the first anti-holomorphic variable a times and the
  second holomorphic variable once. The numerical sums do not change.
  If S11!=0, upstairs coefficients in omega=sum c_j*w^j dw satisfy
  `c_a/c_1=conjugate(S_(a,1)/S11)/a!`, a=1/3/5. The same ratios apply
  to the three coarse coefficients in t=w^2. No earlier ratio was
  certified or used for arithmetic recognition.
- The D91 Mellin prefactor and argument agree with direct height-power
  accounting. The full S11 is nonnegative, but the selected CM first
  derivative may vanish. Canonical base-point freeness guarantees an
  anchor among the sixteen eigenforms without selecting it numerically.
  These analytic ratios are not yet arithmetic CM jets.

**Next:** a bounded numerical pilot that evaluates the completed
scalar kernel before bounding norm/displacement blocks. Require a
useful rigorous global error estimate before extending the Hecke bank
or displacement cutoff. D94's <2.680e13 omitted-ideal bound is unchanged;
the partial sum about 7641 does not certify a nonzero anchor. The
global identification proof is no longer the next task. Exact arithmetic
jets, marked curve identification, cubic recognition and the field
polynomial remain open.

Recheck with `python3 dembele/pari/359_nelson_global_identification_audit.py --check`.
Root `nelson_global_identification_d95.json` binds 134 files, including
the D94 root and new analytic proof. The rational audit replays units,
1,056 diagonal/cross norm conditions, Gaussian coefficients and the
ratio conventions. PARI certification and Sage symbolic calculations
are bound to the <5.49-second run; the audit passed in <1.45 seconds.
The correspondence theorem is a cited mathematical input, not proved
by the audit. Sources 358--359 and bound artifacts/report are frozen.
Earlier numerical artifacts, corrected endpoints, D91's derivative
display caveat, the 180-second limit and cubic precision pause remain.
Decisions, references and entry documents are current through D95.

## Previous checkpoint — D94 contour review and local nonvanishing, 2026-09-23

Read [the D94 report](dembele/certificates/nelson-test-vector-and-contour-d94.md).
The requested global review gives a smaller rigorous bound and a new
local test-vector proof. **There is still no full eigenform evaluation,
CM tangent or target field.** This section governs resumption; older
checkpoints and their next steps are historical.

- Script 355 tests seven contours and four polynomial residue weights.
  Moving the original contour to c=25/16 reduces the uncomputed-ideal
  `(1,1)` bound from about 2.685e16 to **<2.680e13**. This unchanged-
  kernel bound can use the corrected D93 partial sums; it is still
  over three billion times the partial sum about 7641. It is an upper
  bound, not evidence that the actual error is large.
- The tested weights `W_m=(2s-1)*(1-s*(s-1)/(c*(c-1)))^m`, m=0/1/2/4,
  satisfy the residue identity. The best changed-weight bound is
  <2.257e13. Nonzero m changes every finite-family contribution, so
  **do not combine its bounds with D93 partial sums**. No changed-
  weight partial sums were computed. Keep m=0 for now.
- A direct local calculation with the D90 Schwartz functions gives
  nonzero norm-one contractions: finite factors 1 with vol(O_v^1)=1,
  definite real factors exp(-2*pi/delta_v), and the same factor at
  the split place after pairing X^2 with the dual coefficient X^-2.
  Hyperbolic radial integration and Tr(delta^-1)=1 give real product
  **exp(-2*pi)**. These measures are explicitly stated, not asserted
  to give D91's global Petersson scalar. A wrong dual K type gives
  a zero angular average. Script 356 and the audit check the exact
  field/order inputs; the analytic proof is in the report.
- Disegni section 5.1 supplies the general-number-field Shimizu
  framework. Watson sections 2.2--2.3 supply the forward norm-fibre
  and adjoint proof pattern over Q. Neither is silently substituted
  for a checked comparison with our fixed-character classical kernel.

**Next:** finish that explicit comparison: extend the Schwartz
function in the similitude variable, account for the determinant and
central-unit integration, match the dual/newvector/psi_delta conventions,
then apply the forward local nonzero calculation and adjointness.
The report gives a candidate real extension as a starting point.
Nonzero as an automorphic form will still not prove that the chosen
CM first derivative is nonzero. For numerical accuracy, a bounded
pilot must retain more cancellation before absolute bounds; more
quadrature digits or a small cutoff increase does not resolve the
current error. No Hecke rebuild or new enumeration is queued.

Recheck with `python3 dembele/pari/357_nelson_kernel_review_audit.py --check`.
Root `nelson_kernel_review_d94.json` verifies 127 hashes, 505 dyadic
intervals, 168 exact tail polynomials, and local field/order arithmetic.
It binds the corrected D93 root and the D94 proof report; it does not
repeat D93's exhaustive enumeration or the Arb nodes. The two new
computations passed in <7.21 seconds each, and the audit in <1.22 seconds.
Sources 355--357 and bound artifacts/report are frozen. D93's exact-
endpoint correction, D91's derivative caveat, the 180-second process-
group limit and the cubic precision pause remain. Decisions, references
and entry documents are current through D94.

## Previous checkpoint — D93 norm-31 family and global accuracy review, 2026-09-23

Read [the D93 report](dembele/certificates/nelson-prime31-and-global-tail-d93.md).
The requested norm-31 step is complete: **586 classes through A=25600,
32 exact right norm-one orbits, and a Hecke-weighted infinite-family
bound**. We also bound all other norm ideals, but that bound is too
loose for a CM tangent. This section governs resumption; earlier
checkpoints and their proposed next steps are historical.

- At the saved Hecke prime `(31,b-27)`, a positive generator is
  `n=b^6+b^5-6*b^4-6*b^3+8*b^2+9*b+3`, of norm 31. D92's positive-unit
  square proof permits reduced norm exactly n, modulo sign. Complete
  counts at A=400/1600/6400/25600 are 8/60/170/586. Separate interval
  coverage checks 11,568 signed pairs and 4,334,720 recursion nodes
  at the last cutoff in 94.44 seconds rounded up.
- The exact reduction `O/nO=M2(F31)` classifies alpha*O by its image
  line. All 32 lines occur, and all 586 classes have integral norm-one
  right-factor witnesses. Apply D92's disk bound within each orbit;
  disks from different orbits need not be disjoint.
- The first quartic Hecke polynomial is
  `x^4-8*x^3-36*x^2+433*x-899`, with U_p2=+1. For its smallest root
  -7.3140105084, the unit-plus-prime `(1,1)` partial sum is
  7640.7581837028 with two-family tail <9626.300. This includes zero.
  All four quartic-root weightings are stored; no Hecke rebuild occurred.
- Ramanujan coefficient bounds and at most sigma_1(a) norm-one orbits
  at ideal a give an absolutely convergent majorant for the full D91
  expression. The uncomputed-ideal `(1,1)` bound is <2.685e16. This is
  a weak upper bound, not the actual error. Hypothetical complete-A
  cutoffs are tabulated, but none was enumerated across all ideals.
  There is still no useful full-form accuracy or identified CM tangent.

**Important correction:** `QQ(MPFR_endpoint)` can move a directed
endpoint inward. Script 351 replays the D91 kernels, D92 sum/tail,
D93 prime sum and global bounds using `.exact_rational()` and corrected
input dependencies. Use the five `*_exact_d93.json` analytic artifacts
and the final root **`nelson_prime31_exact_d93.json`**. Original files
remain frozen; their default-QQ endpoint exports are superseded. One
old zero-radius error-bound record even had lower>upper. Coverage is
unaffected: its branch bounds use MPFR ceil/floor directly, and exact
root-isolation/arithmetic checks remain valid. D92's 6193<S11<8443
norm-one result is re-established with corrected endpoints.

**Next:** review the global Mellin kernel/summation strategy and the
nonzero Shimizu test-vector identification before extending the Hecke
bank or displacement cutoff. Seek a demonstrably useful global error
bound; more finite terms with the current bound do not establish
accuracy. Preserve D91's arXiv-v1 derivative-scale caveat. The b=10/20/21
coefficients are still missing, and script 60 still has its conjugate-
prime assertion and costly T31 build. No unmodified rebuild is the
next action. Exact arithmetic jets, marked identification, cubic
recognition and the target field polynomial remain open.

Recheck with `python3 dembele/pari/354_nelson_prime31_certified_audit.py --check`.
Its root binds 115 files and checks 11,046 corrected interval records,
exact prime classes/orbits, rational moments and all provenance. Arb
nodes and exhaustive recursion are bound to their runs. Eight original computational jobs
and five endpoint replays passed, all below 94.44 seconds. Three failed
audit attempts and the intervening 350 checkpoint are preserved.
Scripts 344--354 and bound artifacts are frozen. No remote run, higher
cubic precision or candidate-model change occurred. Decisions,
references and entry documents are current through D93.

## Previous checkpoint — D92 complete norm-one control, 2026-09-23

Read [the D92 report](dembele/certificates/nelson-norm-one-control-d92.md).
The user asked to continue the norm-one enumeration step. We now have
**complete displacement cutoffs and a bound on the entire infinite
norm-one family** of the D91 expression. This section governs resumption;
earlier checkpoints below are historical. There is still no complete
eigenform evaluation or independent CM tangent.

- Full unit signature rank 8 proves every totally positive unit is a
  square. Fix reduced norm exactly 1, leaving only the sign quotient.
  A new rational positive form uses weights +/-1/(2T) at the split
  place and 1 at the seven compact places. Every A<=T class lies in
  Q<=(1.001)*(8-1/(2T)); the large D91 unit-cover ellipsoid is avoided.
- Complete class counts at T=400/1600/6400/25600 are 13/29/137/541.
  PARI flag 2 finds the lists; a separate exhaustive Arb recursion
  with exact rational LDL and leaf tests proves coverage. At T=25600
  it checks 11,620 signed pairs in 81.44 seconds including startup.
  The T=400 list contains four A=346.6388971 classes missed by D91.
- Only the identity has A=1, and every nonidentity has A>64. Disjoint
  hyperbolic disks of radius acosh(8) give an infinite tail bound.
  Positive angular averages improve the first crude count estimate.
- At T=25600, the norm-one `(1,1)` partial sum is 7317.7436102796;
  its omitted-family tail is <1124.696. Including all auxiliary
  ideals and beta powers, **6193<S11<8443**, without the common
  Petersson scalar. This proves positivity of one infinite subsum,
  not nonvanishing of the full Shimizu lift. Higher-pair tails are
  still too wide: <21356 for `(3,1)`, <832412 for `(5,1)`.

**Next:** extend the fixed-norm algorithm to the norm-31 prime
**b=27 mod31**, whose quartic Hecke polynomials are already saved.
Use a totally positive norm generator and the report's rescaled
weights. Establish its norm-one coset decomposition or another tail
argument; do not transfer the norm-one bound without proof. This
gives a first nontrivial weighted control without rebuilding T31.
The other primes, matched coefficient bank, an all-ideal tail and
the global nonzero test-vector identification remain necessary.
The old b=10/20/21 coefficients are still missing. Script 60 still
has its conjugate-prime InternalNeighbors assertion and 307.8-second
T31 build; do not launch it unmodified under a 180-second budget.
Further norm-one cutoffs or cubic precision are not the next action.

Recheck with `python3 dembele/pari/343_nelson_norm_one_audit.py --check`.
Root `nelson_norm_one_d92.json` has 51 hashes. It independently replays
the exact majorants, all 12,702 cutoff representatives/classifications,
unit signatures, LDL identities, nesting, inverse pairing and rational
disk averages. The interval recursion and Gamma/zeta nodes are bound
to their runs, not repeated by this standard-Python audit.
Twelve computational jobs finished: eleven passes and one retained
PARI flag-0 precision failure; maximum 81.44 seconds. The separate
audit generation passed too. Scripts 338--343 and bound outputs are
frozen. No remote run or candidate-model change occurred. D91's
derivative normalization caveat remains. Exact arithmetic jets,
marked identification, cubic recognition and the target field remain open.

## RESUME HERE — D91 Hilbert unfolding and partial evaluation, 2026-09-23

Read [the D91 report](dembele/certificates/nelson-hilbert-unfolding-d91.md).
The user approved the next Nelson-method step. We now have exact cusp
and unit identities and interval-enclosed sums for **29 primitive
quaternion classes**, including every auxiliary ideal and every beta
power. **No complete eigenform, global theta lift, or CM tangent has
been evaluated.** This section governs resumption.

- Exactly `O#=beta^(-1)O`, with integral unimodular comparison to the
  saved dual. For odd pairs `(1,1),(3,1),(5,1)`, the two cusps combine as
  `J(Z)+J(Z/2)`. Central-unit duplicates must be removed.
- The norm<=64 subset of the old shell has 130 signed-pair representatives,
  34 unit classes and 96 checked duplicate witnesses. Removing powers
  of beta leaves 29 primitive classes: nine norm-one classes, and
  12/4/4 classes at the primes `b=10/20/21 mod31`. Their coefficients on
  a matched eigenline are missing. The saved T31 polynomials are at
  **b=27**, and cannot be substituted.
- Use `A=Norm(n)*sigma_0(Nrd(alpha_parallel)/n)`,
  `Z=(4*pi^2)^8*A/2^62`. The Mellin integrand includes `zeta_F(2s)`
  and the cusp/beta factor `(1+2^s)/(1-2^(-s-1))`. Forty-two Arb kernel
  enclosures give four affine Hecke buckets for each derivative pair.
  Scalar quadrature error <=6.55e-44; bucket component radii <1e-47.
  These bounds do **not** include missing primitive classes.
- A proved complete unit-reduction bound is available, but too large
  for a direct shell search: LLL gives C=2126 and covering A<=359
  requires Q<=333, versus the old Q<=2.02. The ellipsoid volume is
  about 3.22e39, a diagnostic rather than a point count. Do not launch
  that enumeration. The old shell is explicitly proved incomplete.
- Direct rational `(1,1)` derivative calibration passes. A literal
  reading of arXiv-v1 (11) misses an absolute-X factor in this local
  test; the implementation follows independently differentiated
  Gaussians. The published 2015 display was not accessible. See report
  section 4; do not silently switch formulas.

**Next:** develop economical complete enumeration by norm ideal and
hyperbolic displacement, beginning with the norm-one control:
`A/Norm(n)=cosh(distance(z0,alpha*z0)/2)^2`. Prove coverage and a tail
bound. Build a matched Hecke coefficient bank for the first quartic
level-p2-new eigenline; the unmodified old script 60 has a conjugate-
prime InternalNeighbors assertion and a 307.8-second T31 build.
Also finish the nonzero global Shimizu test-vector identification before
calling any complete sum a differential value. Higher precision does
not address these missing inputs.

Recheck with `python3 dembele/pari/337_nelson_hilbert_audit.py --check`.
Root `nelson_hilbert_d91.json` has 44 hashes. It independently replays
exact quaternion/unit arithmetic and audits the saved interval outputs;
Arb nodes and unit logarithms are hash-bound, not recomputed by this
standard-Python checker. Nine bounded jobs finished: five passes, four
preserved API/coercion failures, maximum 6.23 seconds. Scripts 327--337
and bound artifacts are frozen. D90 recheck also passes. No remote run
or cubic precision increase occurred. Exact jets, marked identification,
exact cubic coefficients and the target field remain open.

## RESUME HERE — D90 Nelson kernel components, 2026-09-23

Read [the implementation report](dembele/certificates/nelson-totally-real-kernel-d90.md).
The user approved pursuing Nelson's paper. We implemented local pieces
of a totally real Shimizu evaluator, including a calibrated scalar
Mellin kernel. **No global theta lift or independent Shimura tangent
has yet been evaluated.** This section governs resumption.

The new exact computations use the actual saved quaternion order and
CM embedding, with no candidate equations or differential-bank inputs:

- `pi=2+b`, `delta=16/(2+b)` are totally positive; `(delta)` is the
  different, of norm `2^31`. Normalize the additive character by delta
  at both finite and real places. The normalized dual quotient has
  order 4, Fourier denominator 2 and Gauss sum -1; the unnormalized
  absolute dual index is `2^126`.
- The real test function has one split polynomial Gaussian and seven
  definite Gaussians. All 36 derivative pairs through order five and
  the disk-coefficient conversion are checked. At the order-two point,
  a value anchor vanishes: use derivative pairs `(1,1),(3,1),(5,1)`.
- The integral CM pieces have ranks 16+16 and direct-sum index
  `2^16`. Preserve the 65,536 matching cosets. A rational positive
  majorant is proved within 1% of the natural one. Its second shell
  has 9,910 vectors, including 9,360 mixed vectors outside the direct
  sum. The first 30-vector shell lies entirely in K.
- A scalar Mellin prototype with factors
  `Gamma(s)^8 Gamma(s+1)^7 Gamma(s+k)` is evaluated for k=3,...,8.
  Degree-one calibration agrees with the independent Bessel formula
  beyond 40 digits. This is numerical calibration, not an interval
  certificate or an established global Hilbert formula.

**Next:** finish the specific Hilbert cusp/unit unfolding: two cusp
contributions at p2, central-unit quotient, norm-ideal Hecke indexing,
and global measure/argument factors. Then evaluate one form from the
first of the four quartic level-p2-new orbits, first with `(1,1)` and
`(3,1)`, with a truncation bound. These sixteen C-forms have U_p2=+1;
do not substitute the level-one target representation. No Hecke-weighted
quaternion sum was evaluated in D90. Do not treat the finite shells
as tails for that sum, or the prototype as an arithmetic tangent.

Recheck:

```sh
python3 dembele/pari/326_nelson_kernel_audit.py --check
```

Root `nelson_kernel_d90.json`: 27 hashes, independent finite-matrix and
CM-lattice checks, every stored shell vector/classification, rational
interval proofs at all eight real places, and corruption controls.
Six bounded jobs are complete: three passes, three preserved development
failures; maximum 9.645 seconds under 180-second process-group timeouts.
Scripts 320--326 and their bound artifacts are frozen. No remote run or
precision escalation occurred. D86--D89 remain unchanged; marked
identification, exact cubic coefficients and the target field remain open.

## RESUME HERE — D89 CM tangent input audit, 2026-09-23

Read [the arithmetic local-input report](dembele/certificates/cm-tangent-local-arithmetic-d89.md).
The user asked to work on the independent CM tangent. **No independent
arithmetic tangent has been obtained.** We now have exact local quotient
and Hecke-branch calculations showing why a Serre–Tate coordinate and
the saved seventeen-point data do not yet form an evaluator.

At the saved Hecke place b=27 modulo 31, the CM roots are beta=8,23.
The order-two quotient has coarse parameter u=z^2. Its projective
tangent needs differential coefficients z and z^3 upstairs; the D88
three-term certificate needs z, z^3, z^5. A first-order upstairs
deformation alone has zero coarse parameter. The report gives the
period-free ratio formulas for converting the required coefficients.

Of the 32 local degree-31 Hecke branches, exactly two preserve maximal
CM conductor; thirty have conductor l. The elliptic involution pairs
the latter, giving fifteen coarse branches of multiplicity two.
Their differential traces involve unknown neighbor derivatives, so
dropping these terms is invalid. These are local branch counts, not a
global census of distinct CM images.

The missing construction is a **global section evaluation map** for
this quaternionic datum. The expanded source review found no ready
exact implementation. A totally real Shimizu derivative formula is a
possible further research direction, not a completed method; even an
independent analytic evaluation would still need exact certification.
Do not schedule an exact tangent solve merely from the formal parameter
or Hecke matrix. D88's conditional identification route remains intact.

Recheck the new exact local calculation:

```sh
python3 dembele/pari/319_cm_tangent_local_arithmetic.py --check
```

Root `cm_tangent_local_arithmetic_d89.json` records formal identities,
all neighbor multiplier tests, trace controls and input hashes. It reads
no candidate equations, candidate jets, or differential banks. Checks
pass. No remote job or large solve was launched. D86/D87/D88 bound
sources and artifacts remain unchanged, and further precision is paused.
Marked arithmetic identification, the hyperellipticity conflict, exact
cubic coefficients and the target field remain open. This section
governs resumption; earlier checkpoints below are historical.

## RESUME HERE — D88 identification reviews, 2026-09-23

The user requested two independent reviews. Read
[the CM-expansion review](dembele/certificates/d88-cm-expansion-identification-review.md)
and [the cubic-shortcut review](dembele/certificates/d88-cubic-identification-shortcut-review.md).
The main dependency is now clearer: **identify the marked arithmetic
base and double cover; then the existing local cubic data can select the
canonical cubic by a conditional uniqueness argument.** Neither arithmetic
identification has been completed.

**Base:** an independent exact projective expansion through t^2 at the
degree-17 CM point can suffice. Its 51-by-136 quadratic-product matrix
must have rank 45 and kernel the saved 91 quadrics. That rank excludes
hyperellipticity and identifies the quadratic ideal. A new bounded
candidate-side calculation verifies ranks **17, 34, 45** for one, two,
and three coefficients, with an independent replay and corruption control.
The simpler four-coefficient fallback uses the paper's degree bound
4*17 > deg(2K)=60. In either case the smooth degree-30 candidate forces
the canonical map to be an isomorphism.

Ratios of canonical sections and a ratio-defined parameter remove the
common CM period. The saved frame gives point values, not independent
arithmetic derivatives. The paper supplies the verification criterion,
not the missing Shimura-side evaluator. Candidate-derived jets are not
that input. Full identification must also certify P32 and B3; the jet
criterion preserves the specified D17 marking only.

**Cubic:** after identifying that marked arithmetic X/C, the saved
Hecke data give a Prym order with 3-adic valuation two. D84's two
independent rational anti-invariant 3-torsion points would therefore make
its nine thirds exhaustive. Only the current one has 68 points over
F31 (and 2818 over F31^2). Global degree-nine branch irreducibility over
F(sqrt(-3)) forces a uniform orientation; mixed orientations on the
three cubic factors modulo 31 cannot arise from that canonical cover.
The S3 norm condition removes constant Kummer twists. On the fixed
smooth marked model, injectivity of reduction on 3-torsion then identifies
the algebraic third from its reduction. This is a conditional comparison
with an independently specified canonical cover, not a general inference
of global definition from a local lift. Use the saved Hecke place
beta=27 modulo 31; the D86 search included all eight places.

**Next research target:** find a concrete independent arithmetic
evaluation of the projective tangent at the labelled CM point, with its
theorem and input model specified, before extending to higher jets.
No such evaluator was found in the reviewed sources. D87's geometric
double-cover comparison still needs certification. The published
hyperellipticity conflict remains open. Keep precision escalation paused.

D86's verified 31^128 cubic, negative recognition and height exclusion,
and D87's numerical character comparison remain unchanged. The exact
number-field cubic and target field polynomial remain unconstructed.
The new candidate diagnostic is rechecked with:

```sh
python3 dembele/pari/d88_candidate_cm_jet_rank_check.py --check
```

Root `d88_candidate_cm_jet_rank.json` retains both the successful
0.347-second Magma job and the rejected matrix-layout attempt, each
bounded by 180 seconds / 2 GB. No Shimura-side jets were computed.
Earlier sections are historical; this section governs resumption.

## RESUME HERE — D87 sign-character comparison complete, 2026-09-23

Read [the double-cover character report](dembele/certificates/cm-frame-double-cover-character.md).
The requested marked comparison now has a concrete result: the exact
rational genus-40 candidate `X: z^2=n/d` has the expected **numerical sign
character on all 277 saved Fuchsian side generators**. Both differential
banks (16,384 and 12,288 terms), and a second path family in the current
bank, agree. Maximum sign errors are below 7.86e-14 / 2.00e-8 / 7.86e-14.
There are 1,650 endpoint paths and 192,405 retained samples across the
three campaigns. No new differential solve or 31-adic lift was needed.

This supports the geometric double-cover choice, which matching the
branch divisor alone would leave ambiguous by `Jac(C)[2]` (size `2^32`).
It is **not a certified analytic or arithmetic identification**. The
geometry and infinite-series tail remain uncertified; endpoint derivative
estimates guide refinement but do not bound entire path segments.

**Do not restart scalar-twist searches.** D77 already proves that the
fixed branch half has a unique F-scalar twist compatible with cyclic
cubic inertia above the degree-nine B3 point: its normalized fibre is
`K(sqrt(-3))`, and the odd-degree norm argument excludes every nonsquare
F-scalar twist. In particular the `-3` twist is already excluded. The
new complex comparison cannot detect constants, but a certified marked
base/geometric comparison would allow that existing D77 constraint to
settle the arithmetic double cover.

**Next:** retain the double-cover candidate and concentrate on the marked
arithmetic base identification and the selected cubic class. Its global
condition `sigma(A)=(sigma(sqrt(-3))/sqrt(-3))*A` remains unproved. D84's
nine local thirds do not exhaust the geometric torsor. The published
hyperellipticity conflict remains open. No automatic 256-digit lift,
arbitrary larger-field search or target torsion computation follows.

**Recheck:**

```sh
python3 dembele/pari/318_cm_frame_double_cover_character_audit.py --check
```

Root `cm_frame_double_cover_character_d87.json` verifies **2,187 file
hashes / 875 JSON records**, including unchanged D86 provenance. It
independently reconstructs the branches from sampled arguments, checks
known windings and rejects a reversed stored root. All 52 job records
are preserved: 51 successful and one rejected midpoint-cache check;
the longest job took 118.136 seconds within its 180-second bound.

The first balanced-midpoint test encountered an elliptic fixed point;
perturbed side samples resolve that issue. Uniform 128-step paths also
gave two false mismatches, removed by adaptive refinement. These earlier
outputs remain archived and must not be interpreted as different-cover
evidence. Scripts 306–318 and bound inputs/outputs are frozen. All jobs
have finished; decisions, references and entry points are updated.

D86 remains valid: both cubics are verified through 31^128, F recognition
is negative in all eight embeddings, and the fixed-basis height exclusion
is 348,750,355,384,078. Audit 303 was rerun successfully. No exact
number-field cubic or target polynomial has been constructed. The sections
below are historical; this section governs resumption.

## RESUME HERE — D86 verified at 128 digits; recognition negative, 2026-09-23

Read [the Châtelet run and reconstruction report](dembele/certificates/cm-frame-cubic-128-chatelet.md).
The requested remote 128-digit attempt is complete. Both the pointed
and smaller `K_X+2P` cubic are independently verified modulo **31^128**,
including geometry/class/function identities, all four highest-digit
corruption controls, and coefficientwise reduction to 64 digits.
All 21 remote jobs and all local recognition/height jobs have finished.

**Recognition:** joint projective F recognition with 112 training / 16
validation digits gives no surviving candidate in any of the eight
embeddings. Known-F points are recovered and unused-digit errors rejected
at every root. Exact integer matrix certificates independently exclude
integral homogeneous coordinate height through **348,750,355,384,078**
in the fixed 25-coordinate / degree-eight power bases, uniformly over
all embeddings and allowing arbitrary common F-valued scaling. This is
not a field exclusion or an arithmetic identification. The coefficientwise
64/64 pilot also has no surviving Q/F candidates in its stated scope.

**Next:** pause precision escalation. Pursue the D85 marked arithmetic
comparison: determine what the saved analytic data can certify about the
explicit base and branch marking, then compare the selected third with
the canonical quaternionic cover. Proving its required global Galois
action is an alternative. Keep the global twist and hyperellipticity
conflict in scope. No automatic 256-digit run, arbitrary larger-field
search, or target torsion computation is the next step. No exact
number-field cubic or target field polynomial has been constructed.

**Artifacts:** `cm_frame_cubic_adjoint_package_128.json` contains the
finite-precision equation/base/monomial ordering. Root
`cm_frame_cubic_adjoint_audit_128.json` verifies **2009 file hashes /
769 JSON records**, including all unchanged D85/D84/D83/D78 provenance.
Recheck locally with:

```sh
python3 dembele/pari/303_cm_frame_cubic128_audit.py --check
```

Scripts 298–300 reuse the original precision-aware kernel 283 with
single-threaded 8 GB / 1800-second remote bounds. The maximum observed
RSS is 2,250,620,928 bytes; the longest job takes 299.709 seconds. Script
302 schedules unchanged independent checkers in two remote lanes; 274
runs local Sage recognition with process-group timeouts; 301/303 certify
the height bounds. Transient transfer errors are recorded. Adapters
304/305 add bounded retries only to idempotent transfer/status operations;
completed calculations and guarded launches are preserved. Use 305 for
any necessary reuse of this campaign's stages, and do not alter bound
sources or overwrite earlier failures.

**Authorization persists:** the user explicitly authorized this run's
mathematical inputs to `chatelet.mit.edu`, beginning with the twelve-file
12,626,184-byte manifest. Credentials and unrelated files were excluded.
The earlier automatic-review rejections were resolved; do not ask again
for this run's upload permission. Remote artifacts remain in
`two_remote_magma/dembele_d86_128_20260922`. The completion receipt confirms
all 21 remote statuses match the saved local records.

D85's no-128-result assertions describe its historical checkpoint. Its
source hashes remain verified, but do not rerun 297's absence assertions
as a current-state test. Decisions, references and entry points are
updated. The sections below are historical; this section governs resumption.

## RESUME HERE — D85 bounded 128-digit attempt failed; descent review complete, 2026-09-22

Read [the attempt and review](dembele/certificates/cm-frame-cubic-128-review.md).
The user authorized trying 128 and proceeding with the review if it failed.
Both parts have been handled: an actual lift was attempted within the
existing limits, and the mathematical review was completed afterward.

**Precision outcome:** sections/evaluation points and pointed jets pass
at 31^128 (94.609/105.349 seconds). The actual-divisor stage fails twice
at 2 GB and then times out at 180 seconds with blocked multiplication.
No 128-digit divisor or cubic exists; **the verified cubic remains at
31^64, and no 128-digit recognition test ran**. Do not describe this as
negative 112/16 reconstruction or evidence against F.

Runners 282, 287 and 291 preserve each attempt and executed driver snapshot.
Kernel 283 makes Newton inversion precision-aware; 285/286 reduce scaling
and model memory; corrected 293/294 use multiplication blocks. Native
controls 284/288/295 pass, including highest-digit inverse corruption.
The initial block-control 289/292 had a matrix-sequence construction error;
retain its failed source/log/receipt too. None of these controls certifies
an actual divisor that was not output. Do not rerun failed jobs in place
or edit their bound sources. If this branch is later resumed, reuse the
sections/jets and introduce a new, checked split of the divisor stage.
Keep process-group runner 272 and 180 s / 2 GB limits.

**Review result:** the third-division torsor has 3^48 geometric members
(anti-invariant 3-torsion dimension 2*(40−16)=48). D84's nine solutions
are local Frobenius-fixed choices, not a global Galois-orbit determination.
Script 296 checks an illustrative root of x^2−5 through 31^128 while
5 is nonsquare in F, and verifies N_S3(C2)=C2. Hence local coefficients
in Q_31 do not prove definition over F, and the S3 cubic has no automorphisms
over its fixed base. Once its field of moduli over that base is proved,
unique comparison maps give the descent cocycle automatically.

The present K_X+2P normalization adds no new root choice: its final scale
is lambda=sqrt(-3)*a0/h0. A sufficient missing global condition is
sigma(A)=(sigma(sqrt(-3))/sqrt(-3))*A for sigma fixing F. This has not
been checked. Marked descent does not supply the field of moduli, and
two Hecke traces do not identify the cover. The base/marking/global-twist
identification and published hyperellipticity conflict remain open.

**Next:** pause precision escalation. Prepare a marked arithmetic
comparison between the explicit X/class and the canonical quaternionic
cover, beginning with what the saved analytic data can certify about
the base and branch marking. A direct proof of the global class action
would be an alternative. No automatic 256-digit lift, arbitrary larger
field search, or target torsion computation is the next step.

Root: `cm_frame_cubic_128_attempt_review.json`; verifier 297 `--check`
checks **1744 file hashes / 612 JSON records**, including unchanged D84,
D83 and D78 roots. Small review checks: `cm_frame_descent_review.json`.
All jobs have finished. Decisions, references and entry points are current.
No exact number-field cubic or target field is constructed. The sections
below are historical; this top section governs resumption.

## RESUME HERE — D84 structural checks complete; current cover distinguished, 2026-09-22

Read [the structural checkpoint](dembele/certificates/cm-frame-structural-checkpoint.md).
The user paused automatic doubling to investigate the choice of third
and calibrate recognition. Both investigations are complete.

**Cover choice:** scripts 276/277 find two independent rational,
tau-anti-invariant 3-torsion points. Independent verifier 278 proves
their orders/symmetries, nine distinct combinations and nine actual
thirds A+i*T1+j*T2. A wrong torsion point is rejected. No Jacobian order
is assumed. Runner 279 constructs and independently verifies all nine
genus-64 covers, then counts normalized fibres over F31 and F31^2 by
two methods. The current class alone matches 68/2818. The eight alternatives
give 59/1495, 50/1540, 59/1543, 44/1504, 38/1474, 59/1525, 38/1456,
53/1567. This is a subgroup of compatible thirds, not a proved exhaustive
census or a direct Fuchsian monodromy identification.

**Recognition calibration:** 275 runs 67 synthetic exact F-point cases
using the same rank-200 joint lattice as 259. At root 4, three independent
seeds all recover height 10^7 and fail 10^8 with 48/16 digits; recover
10^9 and fail 10^10 with 60/4; recover 10^18 and fail 10^19 with 112/16.
Boundary checks at root 20 agree for the latter two splits. Script 280
independently verifies exact projective identities with integer arithmetic.
These are empirical example heights, not guarantees or target height
bounds. The synthetic 128-digit tests did not lift the actual curve.

**Roots:** `cm_frame_third_ambiguity_0_2.json`,
`cm_frame_alternative_cover_0_2_0.json` through `_8.json`,
`cm_frame_recognition_calibration_check.json`, and
`cm_frame_structural_checkpoint.json`. Runner 281 `--check` verifies
1666 hashes / 593 JSON records, including unchanged D83/D78 roots.
Search seed 1 failed to form its random degree-120 support; retain its
failed job/log. All accepted computations have independent checks.

**Recommended next experiment:** one actual 128-digit lift in the same
K_X+2P normalization and exact A2 basis, with 112 training / 16 validation
digits. The checks strengthen the case for this experiment, but do not
guarantee success. If negative, revisit coefficient-field/descent and
identification assumptions before another doubling. Exact number-field
identities remain required before torsion. Do not edit frozen 64-digit
sources. Use process-group timeout runner 272 (274 for existing recognition
workers); preserve the 180 s / 2 GB Magma bounds.

The current authorized checkpoint is complete. **The actual curve remains
at 64 digits; no 128-digit lift has run.** Arithmetic identification,
completeness of the 3-torsion subgroup, the cycle-marking/monodromy comparison,
hyperellipticity conflict, target torsion and the field polynomial remain
open. All jobs have finished. Decisions/references/entry points are current.
The sections below are historical; this top section governs resumption.

## RESUME HERE — D83 cubic verified through 31^64; reconstruction open, 2026-09-22

Read [the D83 report](dembele/certificates/cm-frame-cubic-64.md).
Both the internal 80P cubic and the smaller K_X+2P equation
**ell*T^3-3*A2*ell*T-R4=0, weight(T)=1**, are independently verified
modulo 31^64, including highest-digit norm/trace error controls. All
core coefficients reduce to the frozen 32-digit models. The special
fibre retains genus 64 and counts 68/2818.

**Roots:** `cm_frame_cubic_pointed_64_check.json`,
`cm_frame_cubic_adjoint_64_check.json`,
`cm_frame_cubic_adjoint_package_64.json`, and
`cm_frame_cubic_adjoint_audit_64.json` (runner 263: 1329 file hashes,
493 linked JSON records).

**Bounded construction:** 261 extends the earlier wrappers without
changing D82 sources. The combined class check and first combined
function search timed out; retain both failed jobs. Script 264 splits
the relation and symmetry checks. Script 266 searches for u directly
in WB4, then recovers f separately; 262 fits coefficients. Script 265
checks the internal model and binds the class by exact matrix equality.
Scripts 269/267 construct the smaller model; 268 independently checks
its move and functions in separate jobs. All successful Magma jobs fit
180 s/2 GB. Do not rerun successful bound records in place.

**Recognition:** the individual coefficient pilot is negative. Joint
F recognition is negative in all eight embeddings at both 48/16 and
60/4 training/validation splits. Known controls and unused-digit error
controls pass. Script 271 gives exact inverse-matrix height exclusions;
263 independently verifies them with integer arithmetic. Uniformly
across embeddings, no nonzero integral homogeneous representative can
have all 200 coefficients at most **1,301,123** in absolute value in
the specified 25-by-8 bases. This does not exclude definition over F.

**Runner fix:** the optional Gram-Schmidt diagnostic 270 timed out but
its Sage child later wrote output. The late files are preserved in
`cm_frame_cubic_adjoint_height_64_48_0_late.{out,json}` and excluded from
the certificates. The original timeout log is restored to its recorded
empty hash; the archive manifest records the event. Runner **272**
kills the whole process group; real Sage descendant/positive controls
pass in **273**. Use **274_cm_frame_bounded_recognition.py** for future
Sage recognition jobs, not the older CLIs' timeout wrapper.

**Next:** 128 digits in the same smaller model and exact A2 basis,
with 112 training / 16 validation digits. Add orchestration without
editing the hash-bound 64-digit sources. Split expensive stages or
make inverse arithmetic precision-aware to retain the 180-second cap.
An exact candidate still needs function/divisor identities over its
proposed field before torsion. No characteristic-zero equation or
target field is certified. Selection among thirds, arithmetic
identification, Fuchsian monodromy and the hyperellipticity conflict
remain open. D68–D82 arithmetic inputs are unchanged. No jobs are active.

## RESUME HERE — D82 smaller cubic verified through 31^32, 2026-09-22

**Continue the current work; do not stop at an intermediate checkpoint.**
Read [the D82 report](dembele/certificates/cm-frame-cubic-precision.md).
The final output equation is **ell*T^3-3*A2*ell*T-R4=0, weight(T)=1**,
with 45 quadratic and 105 quartic coefficients. It uses the unique
representative E=K_X+2P+E40, where P is the rational ramification point
above P32. The leading terms are a=3w^6+... and h=3*sqrt(-3)*w^9+...;
normalization uses the existing branch orientation and unit division.
Compatible models exist at 1,2,4,8,16,32 digits in
`cm_frame_cubic_adjoint_n.{json,m}`. The earlier 80P normalization is
retained for efficient class arithmetic, not as the final output model.

**Completed verification:** `cm_frame_cubic_adjoint_32_check.json`
records the independent saved-data check and highest-digit norm/trace
error controls. Scripts 224/225 and 256/257 prove explicit special-fibre
isomorphisms to D79 on 2048 points, above the pole bound 1200. The
normalized cover retains genus 64 and counts 68/2818. The compact
`cm_frame_cubic_adjoint_package_32.json` contains the base quadrics,
ell, coefficient and exponent arrays, and modulus. It specifies the
component dominating C on ell != 0; clearing ell can introduce vertical
components. JSON uses X0,...,X15; Magma uses X1,...,X16 in the same order.

**Efficient class lift:** 208 reconstructs an actual lifted divisor
using an idempotent in a rank-240 zero algebra. Scripts 227–231 normalize
A' and B=-2A'-Delta in the 80P chart and interpolate
C_new=(2*C_A'+C_B)/3 for a k->2k precision doubling. Independent
idempotent reconstruction verifies the interpolated matrix is an actual
divisor; direct checks prove 3A=-Delta and both symmetries. At 8/16
digits it agrees with the scalar route, including the entire pointed
matrix. It is directly verified at 32 digits. Scripts 240–244 recover,
check and publish the pointed functions; 249/253 make the smaller model.

**Recognition:** 254/255 construct an exact rational basis of the
25-dimensional space H0(2K_C-D17-3P32) containing A2. Its integer
coefficients have absolute value at most 5430. Individual recognition
at 8/16/32 digits finds no surviving Q/F candidates. Script 259 tests
joint projective F recognition in this basis, using 24 digits and
reserving eight. All eight embeddings of F are tested; positive controls
and unused-digit error controls pass, but no actual candidate survives.
This bounded search does not exclude definition over F.

**Next:** lift to 64 digits with the verified linear class correction,
apply the K_X+2P output normalization, and repeat joint recognition in
the exact small basis with unused validation digits. Existing CLI
wrappers mostly stop at 32: add orchestration without editing hash-bound
sources. Keep each Magma job within 180 s/2 GB and split longer stages.
An apparent number-field candidate must pass exact function/divisor
identities before torsion work. No computation is currently running.

**Audit:** runner 260 verifies 1099 file hashes across 387 linked JSON
records in `cm_frame_cubic_adjoint_audit_32.json`. D68–D81 inputs and the
D78 root hash are unchanged. The old 80-RREF-entry gauge, its successful
four-digit model and failed eight-digit job remain archived. DECISIONS,
REFERENCES and the report are current through this completed D82 cycle.
No characteristic-zero cubic or target field is certified. Arithmetic
identification, prescribed Fuchsian monodromy, the hyperellipticity
conflict and target torsion remain open. No commits, cleanup, remote
jobs or external messages.

The sections below are historical; this top section governs resumption.

## RESUME HERE — D81 genus-64 cubic lifted modulo 961, 2026-09-22

**The first genuine cubic lift is complete and independently verified.**
Read [the D81 report](dembele/certificates/cm-frame-cubic-lift.md).
The equation remains Q4*T^3-3*A4*Q4*T-P10=0, weight(T)=2. Every
coefficient reduces to D79; the norm scalar lifts from 27 to 58:
u*tau(u)=58*f^3*q*tau(q), h=58*u/q, a=58*f. The saved special fibre
retains D80's two matching counts 68/2818. This is modulo 31^2, not
a number-field reconstruction or arithmetic identification.

**Geometry:** 184 lifts reduced E_Q/U supports of degrees 18/21,
the 36 odd sections, all 1,024 evaluation points and 111 auxiliary
entries, and the oriented B3 values. All defining equations pass.
185 writes `cm_frame_cubic_lift_sections.{json,m}`. The coefficient
ring is (Z/961)[b]/(b^2+29b+3); sigma(b)=-29-b. Sections have ranks
81,201,321,441. Evaluation is injective through degree 960.

**Class arithmetic:** 186 uses pairs of native Z/961 matrices, unit
pivots and residue-field Newton inverses. 187 reconstructs the model.
188 tests native-ring agreement and the lifted Delta. 189/190 execute
c2=1724977996777724256036049034652055939 via 161 add-flip operations,
split into five checkpoints (ends 41,81,121,161,162). No class number
is assumed. Direct checks prove 3A2=-Delta2, sigma(A2)=A2 and
tau(A2)=-A2. Saved coordinates use c0+961*c1, not D78's c0+31*c1.
Data: `cm_frame_cubic_lift_third.{json,m}`.

**Functions:** 191 lifts the old q and chooses a Frobenius-fixed moving
section whose residual divisor reduces to D79's E_R. The descended
81-by-201 coordinates lie over Z/961. It recovers u/f, checks all final
divisor inclusions, and solves for the same 105/105/285 canonical
coefficient arrays. 192 writes `cm_frame_cubic_lift.{json,m}`.
All function and equation coefficients reduce exactly to the old data.

**Verification:** 193 rechecks saved supports/Jacobians, point equations,
branch values, third relation, representative reduction, full function
inclusions, norm and invariant coefficients, with a different seed.
It does not repeat the scalar or function search. Adding 31 to the norm
scalar and to one trace coefficient fails at the intended identities.
The combined certificate is `cm_frame_cubic_lift_check.json`; runner
194 supports default saved-data checks, `--collect-only`, `--rebuild`.

**Bounds:** 180 s/2 GB per Magma job. Sections 8.368 s; pilot 10.711 s;
scalar chunks 54.870/55.947/56.343/55.696/11.773 s; functions 24.635 s;
independent check 32.960 s; controls 29.437/33.071 s. All jobs finished.
Four corrected ring API/data syntax failures are archived separately
from current proof dependencies. Older arithmetic artifacts are unchanged.
The final audit checks 435 file hashes across 132 linked JSON records;
D78's root hash is unchanged. Documentation links, syntax and whitespace pass.

**Next:** fix a persistent effective-divisor normalization before
precision doubling to 31^4 and 31^8. D81 fixes E_R's reduction, but
the moving linear system has 80 projective parameters. Pin 80
independent row-reduced coefficient entries of L(2D0-E_R), after
checking their derivative minor is a unit. This proposed intrinsic
gauge is not yet implemented. Changing scalar-chain representatives
between precisions without fixing those choices is unsuitable for
coefficient recognition. Then lift with compatible gauges and reserve
unused precision to validate reconstruction.

The class lift with the chosen reduction is unique since 3 is invertible;
uniqueness among special-fibre thirds is not proved. The prescribed
Fuchsian monodromy, base/marking/half identification, hyperellipticity
conflict, characteristic-zero cubic, target torsion and final field
remain open. Backend optimization stays paused. DECISIONS and
REFERENCES are current through D81. Local uncommitted work only;
no remote jobs, external edits/messages, commits or cleanup.

## RESUME HERE — D80 two matching genus-64 Frobenius traces, 2026-09-22

**D79's explicit genus-64 cubic has 68 points over F31 and 2,818 over
F31^2. Both exactly match the predicted old-plus-new Hecke factor.**
Every fibre passes an independent quadratic/Kummer calculation; a
changed fibre count is rejected. Read
[the D80 report](dembele/certificates/cm-frame-cubic-frobenius.md), then
[the D79 equation and proof](dembele/certificates/cm-frame-cubic-cover.md).
These are two power traces at one prime, not a full Euler factor or
an arithmetic identification theorem.

**Construction retained:** Q4*T^3-3*A4*Q4*T-P10=0, weight(T)=2,
over the candidate C modulo 31. D79's descended E_R and functions
h=27*u/q, a=27*f give v^3=h, tau(v)=a/v and y=v+a/v. The S3
closure has genus 136, quadratic resolvent X has genus 40, and the
reflection quotient has genus 64 after smooth projective normalization.
All D68–D79 arithmetic data and hashes remain unchanged.

**Point counts:** 180 enumerates C by its degree-30 projection,
including infinity, obtaining 50/1400 points. It counts simple cubic
roots where the model is étale and resolves 6/12 exceptional fibres
by exact local series. The rational P32 branch fibre contributes two;
there are no other B2 or B3 points over these fields. Fibre distributions
for 0/1/2/3 points are [9,27,1,13] and [219,362,1,818].

**Independent verification:** 182 takes the complete saved base-point
lists and counts all fibres by splitting in X followed by a cube test
of the local unit of h. It uses different projective anchors, parameters,
quadric minors and series precision where expansions are needed.
All fibre counts agree. Its split/nonsplit/branch distributions on X
are [22,27,1] and [1037,362,1]. The resulting Frobenius power traces
are -36,-1856; det(1-T*Frob) begins 1+36T+1576T^2. The remaining
coefficients have not been measured geometrically.

**Files and reruns:** `cm_frame_cubic_point_counts.json` contains
both point lists, all fibres and the Hecke comparison. The two
`cm_frame_cubic_point_count_F31*_input.m` files feed verifier 182.
Combined certificate: `cm_frame_cubic_point_check.json`; runner 183
supports default saved-data checks, `--collect-only`, and `--rebuild`.
The Hecke input remains script 58's `levelraise_p2k_charpolys.m`, with
the same four old quartics and degree-48 new factor used in 64/80.

**Bounds:** all Magma jobs retain 180 s/2 GB. Counts take 6.282/87.304 s;
independent checks 1.069/6.727 s; wrong-count control 1.119 s.
Corrected loop-variable scope and conditional-load syntax failures
are archived with immutable source snapshots. All jobs finished.

**Next:** start a bounded lift modulo 31^2 of the marked cubic class
and function identities, fixing matrix pivots and section normalizations
before increasing precision. Preserve the branch orientation, Frobenius
descent and norm compatibility. The two fingerprints support continuing
with this candidate. They do not prove uniqueness of its third or match
the prescribed Fuchsian S3 monodromy. Base/marking/half identification,
the hyperellipticity conflict, characteristic-zero cubic, target torsion
and the final field remain open. Backend optimization stays paused.

**Concrete class-lift scalar (derived, not yet executed):** D78 proves
N*Delta=0 for N=3c+1=166933354526876540906714422708263478. The
reduction kernel modulo 31^2 is killed by 31. Thus for the actual lifted
branch class Delta2, use c2=31c+10=
1724977996777724256036049034652055939 (121 bits): 3*c2+1=31*N,
and c2-c=10*N ensures reduction to the saved A. No full class number
is assumed. See the final section of the D80 report for the proof.
First lift genuine points and complete section spaces with unit pivots;
entrywise lifting the old matrices is not a valid divisor construction.

DECISIONS and REFERENCES are current through D80. Local uncommitted
work only; no remote jobs, external edits/messages, commits or cleanup.

## RESUME HERE — D79 explicit genus-64 cubic modulo 31, 2026-09-21

**There is now an explicit cubic over the candidate C modulo 31 whose
smooth projective normalization has genus 64.** Its S3 closure has genus
136 and quadratic resolvent the saved genus-40 X. The equation is
`Q4*T^3-3*A4*Q4*T-P10=0`, with T of weight two; all coefficients are
in F31. Read [the D79 report](dembele/certificates/cm-frame-cubic-cover.md).
This is not yet an identification with the intended arithmetic cover.

**Construction:** script 176 expands D78's evaluation set from 640 to
1,024 points, preserving the original order, and adds L(4D0), dimension
441. Evaluation is injective through L(8D0), since 1024>960. It replaces
the old effective representative E over F31^2 by E_R over F31, with
[E_R-D0]=A. Choose div(q)=D-+Q-D0 and B=D++Q; an F31 section of
L(4D0-E-sigma(E)-B) gives E_R with class -2A-Delta=A. Both required
disjointness checks are exact rank tests. The old third is unchanged.

**Functions:** div(u)=3E_R+B-4D0 and
div(f)=E_R+tau(E_R)-2D0, tau(f)=f. The exact identity is
`u*tau(u)=27*f^3*q*tau(q)`. Set h=27*u/q and a=27*f. Then
div(h)=D+-D-+3E_R-3D0 and h*tau(h)=a^3. Thus v^3=h has the
involution v->a/v and cubic quotient y=v+a/v. Its branch valuations
prove geometric connectedness and S3; tame branching gives genus 64.
The weighted equation uses a=A4/X16^4 and
h+tau(h)=P10/(Q4*X16^6), T=X16^2*y. Interpret its function-field
normalization, not the raw denominator-cleared special fibres.

**Saved data:** `cm_frame_cubic.{json,m}` contains the quartic/decic
monomial exponents and coefficient arrays (105,105,285), evaluation
indices, product pairs, representative coordinates and q,u,f witnesses.
Matrix entries use D78's F31^2 encoding c0+31*c1; the descended divisor
coordinates and function coefficients are all in F31. The discovery
record's independent-verification flag is false by design; the combined
certificate `cm_frame_cubic_check.json` records the completed check.

**Verification:** 178 reconstructs the saved spaces with a different
seed, verifies the representative, all generators of the final divisor
inclusions, norm identity and cubic coefficients. No third or function
search is repeated. Changing c or one P10 coefficient is rejected.
Runner 179 supports default saved-data checks, `--collect-only`, and
`--rebuild`. Constructor 5.762 s; verifier 6.397 s; controls 4.554/6.321 s.
Magma limits remain 180 s/2 GB. Two corrected Magma syntax/API failures
are archived with immutable source snapshots. All jobs finished.

**Next:** compute the normalized cubic's F31 point count and compare
with the genus-16 old plus 48-dimensional new Hecke prediction. Account
for poles and singular fibres using local normalization. A mismatch
would require revisiting the choice of third/cover before lifting;
agreement is only a first arithmetic fingerprint. Then build a bounded
31-adic lift of the marked cubic and function identities. The prescribed
Fuchsian S3 monodromy, base/marking/half identification, hyperellipticity
conflict, characteristic-zero cubic, target torsion and field polynomial
remain open. No uniqueness of the third is proved.

DECISIONS and REFERENCES are current through D79. D68–D78 arithmetic
artifacts and hashes are preserved; backend optimization remains paused.
Local uncommitted work only; no remote jobs, external edits/messages,
commits or cleanup.

## RESUME HERE — D78 verified cubic branch-class division, 2026-09-21

**We now have an explicit class A on the genus-40 candidate modulo 31
with 3[A]=-[D+-D-].** The class is fixed by Frobenius and negated by
the cover involution. The saved relation passes verification without
the proposed class number or scalar search; a deliberately wrong
class is rejected. Read
[the D78 report](dembele/certificates/cm-frame-cover-class-arithmetic.md).
The Kummer function and cyclic cubic have not yet been constructed.

**Arithmetic model:** D0=2*pi^*div_C(X16), degree 120. Script 164
constructs 45 even quadrics and 36 odd sections w*q3/(ell*X16^2).
The cubics q3 vanish on E_Q+U, where div(ell)=B3+U, deg U=21.
It collects 2,048 usable points over F31[b]/(b^2+29b+3), with
Frobenius and involution permutations. This is an evaluation set,
not the full point count. Script 166 selects 640 points, closed under
both actions, and constructs complete L(D0), L(2D0), L(3D0) of
dimensions 81,201,321. Since 640>5*120, all group-operation products
are evaluated injectively.

**Branch representatives:** a common Frobenius-stable auxiliary
divisor B of degree 111 gives W+/-=L(2D0-B-D+/-), each dimension 81.
The 111 auxiliary constraints plus nine branch conditions have rank
120. Their difference represents Delta. Modulo 31 use sqrt(-3)=11
in D77's regular W coordinate. The saved nonic branch data, rather
than naive w=0 values, supply these constraints.

**Class arithmetic:** 170 implements the pinned LiftTors negation/
chord schedule using Magma finite-field matrices. Every product and
quotient must reach its exact Riemann–Roch dimension; zero/equality
tests verify all generators of a surviving one-dimensional space.
171 proves Delta!=0, 3*Delta!=0, Frobenius(Delta)=Delta and
tau(Delta)=-Delta. This takes 2.744 s. No upstream backend is edited.

**Third:** the heuristic Prym order is
751200095370944434080214902187185651=9*m, with
m=83466677263438270453357211354131739. This is NOT a certified order.
172 proposes c=55644451508958846968904807569421159, with 3*c+1=2*m.
173 computes A=c*Delta in 154 negation/chord steps, then verifies
3*A+Delta=0 directly, in 47.897 s. A is Frobenius fixed and
anti-invariant. 175 reconstructs Delta from the branch spaces and
checks the saved third without loading the order or chain. Replacing
A by A+Delta fails; a separate control corrupting one evaluation also
fails. No uniqueness or arithmetic monodromy match is claimed.

**Representation caveat:** matrices are over F31^2. The class A is
proved to lie in J_X(F31), but its particular effective representative
E need not be defined over F31. The saved matrix is L(2D0-E), so
A=[E-D0]. Do not confuse this E on X with E_Q on C or the common
auxiliary divisor B.

**Next:** recover h with div(h)=D+-D-+3E-3D0, accounting for the
actual representative and constant-field descent. The zero witness
for a reduced intermediate class is not itself this Kummer function;
either track the complementary-divisor functions or solve the final
principal-divisor problem. Then construct v^3=h, enforce the scalar/
involution compatibility, and obtain the reflection quotient. A
31-adic lift and recognition follow that finite-field construction.
The specified Fuchsian S3 monodromy must still select the arithmetic
cover; these branch/class data do not identify it by themselves.

**Files:** `cm_frame_cover_sections.{json,m}` contains section bases,
points and actions. `cm_frame_cover_makdisi.{json,m,gp}` has the three
evaluation spaces and W+/-; GF31^2 entries are encoded c0+31*c1.
`cm_frame_cover_third.json` has the third in `candidate_rows`, an
81-by-640 matrix of section values. `cm_frame_cover_third_input.m`
also has Delta and the scalar chain. Combined certificate:
`cm_frame_cover_check.json`. Runner 174 defaults to both saved-data
checks and controls, supports `--collect-only` and `--rebuild`.
Routine section rechecks have separate filenames to preserve hashes.

**Bounds/failures:** Magma jobs use 180 s/2 GB. Sections/points take
154.552 s, matrix construction 3.904 s, section checking about 3 s.
The first section job's matrix API error is archived and corrected.
GP 169, with 2 GB stack, validates the branch representatives but
times out at 180 s during class operations. Do not repeat it unchanged;
170–175 are the successful finite-field replacement. All jobs finished.

DECISIONS and REFERENCES are current through D78. D68–D77 arithmetic
artifacts and hashes are preserved. The Shimura/marking/half
identification, hyperellipticity conflict, cyclic cubic, genus-64 Y,
target torsion and final polynomial remain open. Backend optimization
stays paused. Local uncommitted work; no remote jobs, external edits,
messages, commits or cleanup.

## RESUME HERE — D77 normalized B3 fibre and cubic branch classes, 2026-09-19

The user asked to continue. **The normalized fibre above B3 is exactly
K(sqrt(-3)), degree 18 over Q, where K is D70's nonic residue field.**
The double-cover involution fixes K and negates sqrt(-3). Over
Q(sqrt(-3)) it gives two disjoint degree-nine divisors D+ and D-.
Their difference is now proved nonprincipal. Read
[the D77 report](dembele/certificates/cm-frame-B3-fiber.md).
The genus-40 rational equation remains D76's unchanged w^2=n/d,
with coefficient heights 583 and 2935433.

**Local normalization:** script 157 exports all B3 coordinates in
K=Q(a), a=X15/X16, with exactly the old nonic polynomial. A nonsingular
14-by-14 minor gives jets through t^2 for t=X15/X16-a. All 91 curve
quadrics vanish modulo t^3. The numerator is n2*t^2+O(t^3), and
d0 is nonzero. Thus z=w/t has fibre equation z^2=alpha=n2/d0.
The job takes 76.599 s under 180 s/2 GB. No maximal order is computed.

**Exact square class:** script 159 screens +/-1, +/-2, +/-3, +/-6
using Norm(alpha), then finds and verifies alpha=-3*s^2 in K.
Only -3 passes the norm screen. The negative norm also proves the
fibre is a field. The square-class job takes 0.678 s. The explicit
witness is saved; independent checking does not repeat its search.

**Rational parameter and orientation:** script 160 uses the first
B3 linear form ell. If ell/X16=lambda*t+mu*t^2+..., then
W=w/(ell/X16) has values +/-sqrt(-3)*r(a), r=s/lambda. All data and
the jets after this parameter change are saved. Cover involution and
conjugation of Q(sqrt(-3)) each exchange D+ and D-. Choosing a sign
here is not a match to the prescribed global branch cycles.
Modulo 31 choose sqrt(-3)=11; each oriented divisor has factor
degrees [3,3,3]. The saved W values in 1,a,...,a^8 are
plus=[22,22,8,21,8,26,21,30,11] and its negative for minus.

**Independent certificate:** Magma 161 verifies every curve jet,
the Jacobian minor, n2=d0*alpha, the exact square witness, the rational
parameter change, involution, splitting idempotents and reduction at
31. It takes 43.402 s. Adding 1 to alpha's constant coefficient leaves
the point and vanishing orders unchanged but fails n2=d0*alpha,
in 26.301 s. Runner 162 records both checks and recursive provenance.

**Scalar-twist consequence:** a constant cyclic Galois cover Z->X
of degree three, totally ramified above B3 over F, forces these
residue fields to contain mu3 by the tame inertia character. Our
fibre passes. For a twist c*n/d, the fibre over K_F=KF is
K_F[sqrt(-3*c)]. Since [K_F:F]=9, c is a square in K_F iff it is
a square in F. Thus this necessary condition selects the unique
F-scalar twist class of this fixed branch half. It does not identify
the half or base curve with the arithmetic ones, or construct Z.
The twist c=-3 illustrates the extra information: it is a square in
Q31 but splits the B3 fibre and fails the cubic inertia condition.

**Nonprincipal difference:** script 163 verifies rank nine for the
sixteen canonical coordinate values at B3; a 9-by-9 minor is 17
modulo 31. Riemann–Roch gives h0_C(B3)=1. D70 excludes L~B3 by
h0(2B3-B2)=0. Consequently pi_*O_X=O_C+L^-1 gives
h0_X(pi^*B3)=1. Since pi^*B3=D++D- and the two are disjoint,
D+-D- cannot be principal. This excludes the simple direct-function
shortcut; no 3-division class has been computed.

**Next:** form Delta=D+-D- in the divisor class group of X modulo 31
using the saved two degree-nine divisors. Seek 3[A]=-[Delta] and
then h with div(h)=Delta+3A, giving v^3=h after adjoining mu3.
Do not assume finite-field divisibility or uniqueness of a third.
Recover the involution and constant-field descent, and match the
specified Fuchsian S3 monodromy before accepting a cubic extension.
The branch data alone do not choose one. More 31-adic precision and
the old coefficient searches are not the next default actions.

**Files:** `cm_frame_B3_fiber.{json,m}` has coordinates, jets and
alpha. `cm_frame_B3_fiber_structure.{json,m}` has the square witness,
rational parameter and oriented branches. Combined certificate
`cm_frame_B3_fiber_check.json`; nonprincipal-class certificate
`cm_frame_B3_branch_class.json`. Runner 162 defaults to independent
checking plus a corruption control; `--rebuild` repeats 157–160;
`--collect-only` validates provenance. Run script 163 for the small
rank/divisor-class audit. Magma has 180 s/2 GB; Sage 160 has 180 s
and no memory cap. The old nonic maximal-order timeout is not repeated.

DECISIONS and REFERENCES are current through D77. No cyclic cubic,
genus-64 Y, target torsion or nonsolvable field polynomial is obtained.
The Shimura/marking/half identification and hyperellipticity conflict
remain open. D68–D76 arithmetic artifacts and their hashes are
preserved. Backend work stays paused. All jobs finished; local,
uncommitted work only, with no remote jobs, messages, commits or cleanup.

## RESUME HERE — D76 exact rational genus-40 double cover, 2026-09-18

The user asked to continue. **We now have an exact rational equation
w^2=n/d on the certified genus-16 candidate C, with coefficient heights
583 and 2935433.** Its smooth normalization has genus 40 and branch
divisor B2=D17+P32 of degree 18. An independent verifier checks the
exact rational divisor certificate and a square-factor map to the old
cover modulo 31^128. A wrong quadratic twist is rejected. Read
[the D76 report](dembele/certificates/cm-frame-rational-double-cover.md).
This is a rational cover on C; identification with the arithmetic
Shimura/sign cover and its global twist remains open.

**Lift without lifting G:** scripts 146–149 transfer D75's B3
normalization at 64 and 128 digits. H0(2K-E-B3) has dimension 20.
Lift g with its fixed free coordinates, and choose h in that space
nonvanishing on the degree-35 residual G. Then h*q=g*s, together
with seven P32 jet conditions, gives the full three-dimensional
H0(2K-G-7P32). The 90-by-112 matrix has rank 87. No coordinates of
G need lifting. Solve n_old*g^2*d_ij=n*d_old*q_i*q_j for all six
products; they have rank 6. Independent checks and a 31^127 error
control pass. Data at 128 digits reduce exactly to those at 64.

**Successful space recognition:** script 150 fits the six-space at
64 digits, validates at 128, and finds six independent rational
quadrics of six-digit height. Its rank-136 lattice has index
(31^64)^39, exactly checked. Six of 45 nonzero tested section images
survive. A known rational six-space control passes and rejects a
changed unused digit. The old arbitrary selected denominator still
has zero surviving rational projective ratios. Recognizing the space
and selecting a new square section is the successful approach.

**Exact algebraic reconstruction:** script 151 finds product rank 15
and six exact quadratic relations over Q. Script 152 splits the
resulting Veronese surface explicitly: a unique singular cubic, its
rank-three polar at the known rational point, a tangent two-jet and
a split conic give an invertible rational transformation to
F0,D0,E0,A0,B0,C0 with all six symmetric rank-one identities. In
particular F0*A0=D0^2. The selected integral denominator is d=9*F0.
Do not confuse the section F0 with the base number field F.

**Rational divisor proof:** the second small numerator r is a unit
on the reduced residual T modulo 31. Script 153 saves exact witnesses
r*v=n*s_v for all six forms v, integral at 31. This proves vanishing
on the rational T. Modulo 31, gcd(F0,A0)=T; after removing T they
have no common zeros over Q by properness. F0*A0=D0^2 forces the
remaining zeros of F0 to be even. The residual half E_Q has degree
18 and is reduced and disjoint from T and B2+2B3. Thus
div(n)=B2+2B3+T and div(d)=2E_Q+T over Q. This avoids D75's archived
rational residual-ideal timeout. O(E_Q-B3) is a rational branch half.

**Scalar and independent certificate:** script 154 decomposes the
128-digit product coordinates of d as a unit scalar times a square.
The scalar is already a square modulo 31: twist multiplier 1.
The saved g/q_Q satisfies n_old*g^2*d=n*d_old*q_Q^2 modulo 31^128.
Magma 155 repeats no search or solves: it checks saved rational
identities/witnesses, divisor ideals at 31 and the global finite-ring
square identity. It takes 30.035 s. Negating d and its recorded scale
passes all divisor checks but fails that identity in 29.883 s.
Matching this one completion does not identify a global arithmetic
twist; rational scalars square at 31 can change the global cover.

**Files/reproduction:** `cm_frame_B3_rational_model.{json,m}` contains
the rational equation, monomial order, exact witnesses and finite-ring
square map. `cm_frame_B3_veronese.{json,m}` gives the coordinate change.
Combined records are `cm_frame_B3_lift_check.json` and
`cm_frame_B3_rational_check.json`. Runner 148 defaults to independent
lift checks, `--rebuild` repeats 146–147. Runner 156 defaults to the
independent rational check/control, `--reconstruct` repeats 150–154
against the saved lift. Both accept `--collect-only` for recursive
provenance checking. Magma jobs retain 180 s/2 GB; Sage jobs have
explicit 180 s limits (300 s for 150) and no memory cap.

**Next:** compute the normalized unramified fibre above B3, its
degree-18 étale algebra, and the double-cover involution. Since n/d
has order two there, use the leading unit after dividing by a local
parameter squared; naive w=0 substitution is the singular model's
fibre. These are the branch data for the cyclic cubic cover Z->X,
with genus(Z)=136 and reflection quotient Y of
genus 64. The specified arithmetic S3 monodromy must still select
the cubic extension; the branch divisor alone will not do so.
Keep the base/marking/sign-cover identification and hyperellipticity
conflict explicit. More lifting and old coefficient searches are not
the default next action.

DECISIONS and REFERENCES are current through D76. No genus-64 Y,
target torsion or nonsolvable field polynomial is obtained. D68–D75
arithmetic data and their hashes, old lifts and numerical banks are
preserved. Backend work stays paused; D63's 111 tests remain the
latest full backend suite. These are targeted exact certificates.
All jobs finished. Work is local and uncommitted; no remote jobs,
external messages, commits or cleanup.

## RESUME HERE — D75 height-583 numerator and square transfer at 31, 2026-09-18

The user asked to continue. **A geometric normalization now gives an
exact rational numerator of height 583, replacing the 39-digit one.**
The same double cover is independently certified modulo 31 by an
explicit square-factor identity; a wrong quadratic twist is rejected.
The new representation has not yet been transferred to higher precision.
The old certified 31^128 lift is preserved. Read
[the D75 report](dembele/certificates/cm-frame-joint-field-and-B3-normalization.md).

**Planned recognition completed:** script 138 fits seventeen degree-seven
polynomials over F with a common F-valued scale, at the 64/128 split.
The rank-136 lattice has index (31^64)^16, independently checked.
A known F projective point gives eight exact surviving rows, while
separate recognition of its sixteen ratios gives none. Every one of
765 tested denominator rows fails at the first unused digit, across
all eight embeddings. Script 139 gives exact coefficient-box exclusions
using D=31^64*R^-1 and column l1 norms: uniformly no nonzero lattice
vector has all 136 coefficients bounded by 8066216. This is in D74's
specific section/power bases, not non-descent to F, and does not apply
to the new B3 coordinates. Magma 140 and runner 141 certify the rows,
control, inverse bounds and a changed unused digit. Jobs 138/139 take
31.380/4.214 s; independent/control checks take 6.752/0.879 s.

**Geometric change:** write P=P32, B2=D17+P and L=O(E-7P), deg E=16.
Use E_new of degree 18 with L=O(E_new-B3), where B3 is the known
rational degree-nine marked divisor. This does not assert L=O(B3).
Script 142 constructs H0(2K-B2-2B3), dimension 9. Its saturated integer
representative lattice has rank 100 and unit Smith invariants. All
100 LLL rows have nonzero section images; do not assume 91 pure
curve-relation rows appear separately. Nine independent section
representatives have 3–4 digit heights. Of 172 candidates, the first
has primitive height 583 and passes the geometry. The job takes 21.872 s.

**Square transfer:** script 143 chooses g with div(g)=E+B3+G, deg G=35.
The space H0(2K-G-7P) has dimension 3; q in it has
div(q)=E_new+G+7P. For the new rational numerator n_new,
div(n_new)=B2+2B3+T, deg T=24. The denominator has div(d_new)=2E_new+T.
The identity n_old*g^2*d_new=n_new*d_old*q^2 fixes the scalar, hence
w_new=w_old*g/q gives the same cover over F31. Odd branch degree stays
18 and genus stays 40. The transfer takes 20.390 s.

**Rational certificate / timeout:** direct rational residual-ideal work
after the finite-field transfer timed out at 180 s/2 GB. Exact source,
log and limits are archived in `cm_frame_B3_rational_ideal_probe.json`.
Do not repeat unchanged. The successful replacement certifies numerator
membership over Q with coefficients integral at 31, and uses D69/D70
good reduction plus the reduced disjoint residual at 31 to prove the
rational residual properties. No cap increase. Magma 145 independently
checks the saved data in 16.051 s. Negating the denominator leaves its
divisor unchanged but fails the square-factor identity, in 15.709 s.

**Next:** reuse D74's 128-digit old E/support data to lift this change
of variables. Lift g in H0(2K-E-B3) by linear conditions with fixed free
coordinates, its simple residual G, and the entire three-dimensional
space H0(2K-G-7P). Solve for d_new using the displayed global identity
and independently verify the scalar and square map at each precision.
No new lifting beyond 128 digits is needed for this experiment. Keep
all three q sections: their six pairwise products may give a useful
denominator space to recognize before selecting one point. Their rank
and arithmetic height have not been computed. Do not assume arbitrary
denominator coefficient constraints preserve the half or its field.

**Files:** scripts 138–145; combined certificates
`cm_frame_joint_field_check.json` and `cm_frame_B3_check.json`.
`cm_frame_B3_normalization.json` saves the exact numerator, finite-field
denominator, g/q, E_new quadrics and all three moving sections.
Runner 141 defaults to independent checks, `--search` repeats 138–139;
runner 144 defaults to independent checks, `--rebuild` repeats 142–143.
Both accept `--collect-only` for recursive provenance validation.
Sage jobs have explicit timeouts and no memory cap; Magma has 180 s/2 GB.

DECISIONS and REFERENCES are current through D75. No number-field
denominator, arithmetic sign cover, genus-64 Y, target torsion or field
polynomial is obtained. Independent Shimura/marking identification and
the hyperellipticity conflict remain open. Earlier arithmetic artifacts,
the old 128-digit lift, banks and external checkouts are unchanged.
Backend optimization and old CM scans stay paused; D63's 111 tests are
the latest full backend suite. All jobs finished. Work is local and
uncommitted; no remote work, messages, commit or cleanup.

## RESUME HERE — D74 lift to 31^128 and reduced denominator space, 2026-09-18

The user asked to continue. **Precision doubling now reaches 31^128,
and the 39-digit numerator's transferred denominator has independently
verified divisor and unchanged-radicand certificates at every new
stage.** Arithmetic recognition remains open. Read
[the new report](dembele/certificates/cm-frame-precision-doubling.md).

**Lift:** script 130 reduces the known exact old numerator over Q and
doubles the support/denominator precision while retaining D72's scale.
Its 4->8 control agrees with every saved coefficient, coordinate,
tangent and jet. Stages 8->16->32->64->128 take 52.198 s including
startup/control, under 900 s with no Sage memory cap. Unit-pivot
elimination and scalar Newton inverses avoid unsupported polynomial
xgcd over composite rings. Every curve equation and double-zero
condition is checked. D68–D73 artifacts are not overwritten.

**Independent checks:** runner 131 generates data-path-only copies of
Magma 125/128/129 and certifies each stage and its transfer n*d'=n'*d.
All old/normalized data are compatible. A 31^127 denominator error
is rejected. The final modulus has 191 decimal digits / 635 bits.
No scalar change, number-field denominator, or descent is claimed.

**Recognition findings:** script 132 tests Q and F=Q(zeta32)^+ using
all eight roots of t^8-8t^6+20t^4-16t^2+2 modulo 31. Training/validation
pairs 16/32, 32/64 and 64/128 reject every tested affine/projective
coefficient candidate. Known Q/F controls and changed-unused-digit
controls pass. This is not a proof of nonmembership or a height bound.
The exact 39-digit numerator becomes a 144-digit primitive vector
in the fixed 45-monomial chart (affine numerator/denominator maxima
144/104 digits). Whole-quadric Q reconstruction, script 133, recovers
the known numerator exactly but rejects all 43 tested denominator
candidates; its smallest returned vector has 88 digits, not a lower
bound. Jobs 132/133 took 5.003/35.780 s.

**New exact space:** let A=D17+15P32 and div(n')=A+T', deg(T')=28.
The denominator lies in W=H0(2K-T'), dimension 17. Script 134 selects
a second numerator r nonvanishing on all T' and solves r*d=n'*s in
degree four: a rank-73, 90-by-105 matrix has a 17-dimensional kernel.
This takes 12.466 s. The first rational basis has up to 1,322-digit
coefficients. Script 135 computes a saturated rank-108 integer lattice,
including 91 curve relations, and reduces to seventeen sections with
height lengths [39,43,43,47,51,55,59,63,65,69,72,77,80,84,88,93,96].
All Smith invariants are 1, and the section classes have rank 17 at 31.
Each retains an exact witness r*d_i=n'*s_i. Coordinates of the saved
denominator agree at 32/64/128 digits. Coefficientwise Q/F recognition
still yields no surviving candidates in this basis.

**Avoid a repeated timeout:** generic nullspace recomputation on the
large rational spanning basis timed out after 300 s. Its source/log
and limit are archived in `cm_frame_denominator_space_nullspace_probe.json`.
The exported basis already has an identity block. Direct elimination
builds its 28 constraints in 0.358 s; the full corrected script 135
takes 59.463 s under the unchanged 300 s limit. Do not repeat the
archived generic-nullspace probe unchanged.

**Next:** try joint projective reconstruction over F in W. Use seventeen
degree-at-most-seven polynomials in the F generator, with a common
F-valued scale, rather than recognizing separately normalized ratios
with rational integer denominators. That common scale may avoid
coefficient growth from inversion in F. This algorithm is not yet
implemented; no success or precision bound is assumed. Start with
the existing 64/128 digit validation split. Preserve or explicitly
recover the recorded scalar, and require exact algebraic verification
before accepting a number-field cover. More lifting is not the next
default. The separate base/marking/sign-cover identification remains
unproved, including the earlier hyperellipticity conflict.

**Files/reproduction:** `131_cm_frame_doubling_check.py` verifies all
stages; `--lift --digits 128` reproduces the lift first; `--collect-only`
checks saved provenance. Main data are `cm_frame_doubling_{16,32,64,128}.json`
and `cm_frame_doubling_normalized_{16,32,64,128}.json`. Script 137 checks
the reduced space independently using Magma 136 and rejects a changed
basis coordinate. Its `--recognize` repeats scripts 132–135, and
`--collect-only` checks the whole D74 record. The reduced basis/witnesses
and denominator coordinates are `cm_frame_denominator_space_reduced.json`;
combined certificate `cm_frame_arithmetic_check.json`. The independent
space certificate takes 6.116 s; its highest-digit control 5.619 s,
both under 180 s/2 GB. Main lift verifiers have 240 s/2 GB bounds.

DECISIONS and REFERENCES are current through D74. The number-field
cover, specified cubic extension, genus-64 Y, target torsion and field
polynomial remain unconstructed. Backend optimization and old CM scans
stay paused; earlier arithmetic artifacts, banks and external checkouts
are unchanged. D63's 111 tests remain the latest full backend suite;
these are targeted exact certificates. All jobs finished. Work is local
and uncommitted; no remote work, external message, commit or cleanup.

## RESUME HERE — D73 numerator reduced to 39 digits, 2026-09-18

The user approved the normalization plan and suggested checking M23.
**The primitive exact rational numerator height is now 39 digits,
down from 631. The transferred denominator gives the same radicand
modulo 31^8, independently certified.** Read
[the normalization report](dembele/certificates/cm-frame-normalization.md).
The denominator is still finite-precision data; its number-field height
is unknown. No number-field cover or target field polynomial is obtained.

**M23 transfer:** §3 fixes a cubic modulo multiples of the known quadric
using a Hermitian complement. Our integral-lattice adaptation allows
the 91 curve equations while shortening a numerator. We do not claim
to implement the separate reduction algorithm in Zhang's account.

**Exact search:** script 127 computes the 32 rational constraints for
D17+15P32. The saturated kernel in the fixed 45-monomial chart has
rank 13 and gives 48-digit primitive height. The full 136-column
integer kernel has rank 104; LLL produces 91 curve-relation rows and
13 section rows. Allowing these representatives gives 39 digits /
127 bits, height 119732280500973149122871877303430862720. Unit Smith
invariants certify saturation. There are 322 accepted basis/pairwise
combination candidates; the first candidate passes the geometric gate.
No shortest-vector proof is claimed.

**Transfer/check:** script 128 solves the rank-45 multiplication system
in 105 quartic coordinates over Z/31^8 for n*d'=n'*d on C. Thus the
ratio and twist at this precision are unchanged, as are E, the half
L=O(E-7P32), and the 18 branch points. New common residual T' has
degree 28 and factor degrees [1,1,26]; its exact residue ideal is
reduced and X15/X16 separates it and is unramified there. Script 129
independently verifies the exact Q numerator using D17 ideal membership
and rational implicit jets, the global ratio identity, the full-precision
local orders, and the new residual ideal. A 31^7 denominator error,
invisible modulo 31^7, fails the quartic identity as expected.

**Next:** extend precision by doubling and seek recognition over F,
keeping the exact 39-digit numerator in its full 136-monomial form.
T' coordinates are currently saved modulo 31 only; lift its simple
zeros against the exact numerator when needed. Track the scalar:
one safe comparison is to extend D72 and transfer by n*d'=n'*d at
each higher precision. Changing a denominator's scale without a
documented square-factor/isomorphism check does not preserve the
claimed radicand. Numerator reduction alone does not bound denominator
height or settle descent. A precision-doubling implementation is still
needed; do not default to hundreds of one-digit steps.

**Reproduction:** `python3 dembele/pari/129_cm_frame_normalization_check.py`
verifies the saved pair and runs the corruption control; `--collect-only`
checks saved provenance, and `--rebuild` also repeats the lattice search
and transfer. Main data are `cm_frame_numerator_lattice.json`,
`cm_frame_normalized_resolvent.{json,m}`, and
`cm_frame_normalization_check.json`. Full bases, candidate provenance,
support presentation, logs, job limits and hashes are retained.
The lattice job took 53.058 s; transfer 9.987 s; independent checking
20.524 s; negative control 14.501 s. Sage timeout 240 s with no memory
cap; Magma jobs 180 s/2 GB.

DECISIONS and REFERENCES are current through D73. D68–D72 arithmetic
artifacts, numerical banks, backend code and external checkouts remain
unchanged. Shimura identification, the earlier hyperellipticity conflict,
the specified cyclic cubic extension, genus-64 Y, target torsion and
the nonsolvable field remain open. Backend optimization and old CM
scans stay paused; D63's 111 tests remain the latest full backend suite.
All jobs finished. Work is local and uncommitted; no remote job,
external message, commit or cleanup.

## RESUME HERE — D72 compatible lifts through 31^8, 2026-09-18

The user asked why there are so many branch points and to continue
with the lift. **The branch square class now lifts exactly through
31²,...,31⁸**, with an independent divisor certificate at
31⁸=852891037441. Read
[the lifting report](dembele/certificates/cm-frame-resolvent-lift.md).
This is a finite-precision equation, not a number-field cover.

**Branch count:** the saved sign character is negative on the
transpositions at 17 order-two points and at the unique order-32
point, giving 18 geometric branch points. The nine 3-cycles have
positive sign and do not branch in this double cover. D17 packages
seventeen geometric points into one degree-17 closed point. The
three-branch-value property concerns Belyi maps to P1, whereas this
auxiliary cover has genus-16 base C.

**Lift:** q_num/q_den still has divisor D17+15P32-2E, deg(E)=16;
L=O(E-7P32) remains a half of B2. The support fields have degrees
D17:[17], E:[2,2,2,10], residual T:[1,1,3,23]. Code calls T `F`,
unrelated to the base number field. All supports are étale and use
X15/X16 as a separating, unramified coordinate. At each digit, solve
32 numerator conditions, 44 denominator conditions, then correct
the 16 double-zero positions using the unit second coefficient.
All 91 equations and reduction compatibility of successive data are
checked. No guessed Jacobian order enters the lift.

**Important calibration:** script 126 independently recovers the
same numerator exactly over Q from D17 and rational order-15 jets
at P32. It agrees with all eight digits. Its primitive coefficient
height has **631 decimal digits / 2,096 bits** in the present fixed
coordinate normalization. The uniform sufficient bound 31^n>2UV
for its known affine coefficients gives n=845. This is not a minimal
threshold or a bound for the unknown denominator. The exact numerator
has already been obtained without such a precision run; the cover
has not been reconstructed over Q or F.

**Next:** use the exact 13-dimensional numerator space to seek a
smaller integral normalization. Transform numerator and denominator
together and verify preservation of the square class. This reduction
has not been implemented. Then use precision doubling for higher
accuracy and seek arithmetic recognition over F. Do not default to
hundreds of successive digits in the current normalization.
The independent Shimura-identification obligation, including the
earlier hyperellipticity conflict, remains. The specified cyclic cubic
extension, genus-64 Y, target torsion and nonsolvable polynomial are
still unconstructed. Q descent of the cover is not assumed.

**Files/reproduction:** Magma script 123 exports support algebras;
Sage script 124 lifts; Magma script 125 independently checks; Sage
script 126 recovers the rational numerator. Standard-library runner
`125_cm_frame_resolvent_lift_check.py` checks saved data by default,
uses `--collect-only` to validate hashes, and `--lift --digits 8`
to reproduce all stages. Main data are `cm_frame_resolvent_lift.{json,m}`
and `cm_frame_resolvent_lift_2.json` through `_8.json`. Main certificate
is `cm_frame_resolvent_lift_check.json`; rational coefficients and
height calibration are `cm_frame_lift_numerator.json`.

Support extraction took 5.664 s; all seven lift steps 38.547 s including
Sage startup (35.363 s internally). Independent verification took
2.351 s. A changed highest digit, invisible modulo 31^7, is correctly
rejected in 0.351 s. The rational numerator job took 7.643 s including
startup. Magma jobs have 120 s/2 GB limits; the lift has a 240 s timeout
and the rational calibration 120 s, without a Sage memory cap.

DECISIONS and REFERENCES are current through D72. D68–D71 artifacts,
numerical banks, backend code and external checkouts are unchanged.
Backend optimization and old CM-function scans remain paused. D63's
111 tests remain the latest full backend regression; these targeted
exact certificates are separate. All jobs finished. Work is local and
uncommitted; no remote job, external message, commit or cleanup.

## RESUME HERE — D71 exact double cover over F31, 2026-09-18

The requested continuation constructs an **explicit genus-40 double cover
of the candidate modulo 31**, branched precisely at B2=D17+P32. Read
[the resolvent report](dembele/certificates/cm-frame-resolvent.md).
This is a finite-field construction; no characteristic-zero cover or
Shimura identification is claimed.

**Exact result:** saved quadrics give u=q_num/q_den with
`div(u)=D17+15P32-2E`, where E has degree 16. Thus
`L=O(E-7P32)` has degree nine and L²=O(B2). The smooth projective
model of z²=u is geometrically connected of genus 40. Direct point
counts are 45 for u and 55 for its constant twist 3u. The first matches
the norm-one genus-40 Hecke prediction. This comparison does not prove
uniqueness of the half class or identify the specified sign cover.

**How it was found:** P16(32) gives the unproved Jacobian-order guess
N=1640801490553691915934375. Geometric divisor arithmetic computes
`[(N+1)/2](D17-17P32)`, with an 80-bit scalar. The final divisor identity
is independently certified, so the cover does not depend on assuming
that N is the actual order. N, absence of rational two-torsion, the
full Euler factor, and the base's Shimura identification remain unproved.

**Files:** `dembele/magma/121_cm_frame_resolvent.m` is the exact
discovery source, initially executed from an identical scratch copy.
`122_cm_frame_resolvent_check.m` independently proves the divisor
identity and counts all rational fibers, including two 0/0 evaluations
resolved by exact local jets. Data are `cm_frame_resolvent.{json,m}`;
the short equation is `cm_frame_resolvent_equation.txt`. The runner is
`dembele/pari/122_cm_frame_resolvent_check.py`: default checks the saved
equation, `--collect-only` validates hashes/log totals, and `--discover`
repeats the scalar calculation before checking. Discovery took
466.760 s under 900 s/2 GB; verification took 10.897 s under 120 s/2 GB.
A changed numerator coefficient is rejected by the saved negative
control in 2.026 s. All jobs finished.

**Next:** implement one 31-adic lift of L²=O(B2), initially modulo
31², and verify the doubled class. Doubling's invertible differential
provides the local Newton/Hensel route, but the implementation has
not been written. Then pursue arithmetic recognition over F and
identification with the saved sign monodromy, before the cyclic cubic
extension and genus-64 Y. Do not interpret the finite-field coefficients
as a characteristic-zero equation. Q descent is not assumed.
The independent base-curve identification, including the earlier
hyperellipticity conflict, is still a separate unresolved obligation.

**Avoid repeated dead ends:** generic FunctionField(C) timed out at
90 s. An explicit rank-30 function field and maximal orders recover
genus 16 in about 36 s, and the marked places in 44 s, but native
Reduction still times out at 150 s. Sources/logs and bounds are in
`cm_frame_resolvent_probe_limits.json`. Use the successful canonical
quadric/colon-ideal arithmetic instead. Old cover differential banks
remain too inaccurate for direct recognition; no new bank was computed.

DECISIONS and REFERENCES are current through D71. D68–D70 data and
earlier backend files are unchanged. Backend optimization and old
CM-function scans remain paused; D63's 111 tests remain the latest
full backend regression. These are targeted mathematical certificates.
Work is local and uncommitted; no remote job, external checkout edit,
message, commit or cleanup.

## RESUME HERE — D70 exact marked branch candidates, 2026-09-18

The user asked to continue. **The verified genus-16 candidate now has
an exact ordinary rational point and exact disjoint closed points of
degrees 17 and 9, accounting for candidates for all required branch
locations.** The nonic residue field has proved Galois group 9T15,
order 72. Read [the marked-divisor report](dembele/certificates/cm-frame-marks.md).

**Exact results:** the recovered rational point has primitive height
`3310032844768591087`; all 91 quadrics vanish. Its canonical jet matrix
modulo 31 has rank 16 and determinant 8, proving ordinarity there and
over Q. Seven linear forms of height at most 54 cut out one reduced
degree-nine closed point B3. D17 is cut out by 28 additional quadrics.
All three marks are disjoint, with flat reduced specialization at 31.
Magma proves the nonic Galois group, including `GaloisProof`.
The CM labels and identification with the actual Shimura curve are
still numerical, not certified by these algebraic assertions.

**Cover input:** B2=D17+P32 has degree 18; B3 has degree 9. The
prescribed local S3 monodromy requires transpositions over B2 and
3-cycles over B3. The convenient relation `B2 ~ 2 B3` is **false**:
an exact residual-ideal calculation gives `h0(2B3-B2)=0` modulo 31,
and the flat markings transfer this exclusion to Q. This only rules
out that square-root recipe, not the intended cover.

**Next:** recover the cover's algebraic extension data using the
saved full S3 monodromy. A concrete intermediate target is the
quadratic resolvent selected by its sign character: find the correct
square class branched at B2, equivalently a degree-nine line bundle
L with `L^2=O(B2)` and its branch section. L cannot be O(B3).
Branch locations alone do not select this class or the subsequent
cyclic cubic cover. No square-class reconstruction algorithm is yet
implemented. Work over F is allowed; Q descent is not assumed.
The independent Shimura-identification obligation remains: D69's
exact order-four CM jets have not been obtained. Candidate-derived
jets prove ordinarity, not that identification. Keep that distinction.

**Files and checks:** Sage script `119_cm_frame_marks.py` reads the
two existing banks and finishes in about 20 s. It writes
`cm_frame_marks.{json,m}`. Standard-library runner
`120_cm_frame_marks_check.py` runs `dembele/magma/120_cm_frame_marks.m`
with 120 s/2 GB limits; it passes in 46.070 s. Use `--collect-only`
to validate saved source/log hashes. The nonic polynomial and exact
log are `cm_frame_nonic_polynomial.txt` and `cm_frame_marks_check.out`;
the main result is `cm_frame_marks_check.json`.
A default nonic maximal-order probe timed out at 90 s, before a
discriminant or reduced polynomial; its reproduction script/log and
failure record are `cm_frame_nonic_order_probe.{m,out,json}`. Do not
repeat unchanged. The nonic CM class-field identification is also open.

DECISIONS and REFERENCES are current through D70. D68/D69 artifacts,
old banks, earlier backend files and external checkouts are unchanged.
Backend optimization and old CM-function scans remain paused. D63's
111 tests remain the latest full regression suite; D70 has targeted
algebraic certificates. No jobs remain running. Work is local and
uncommitted; no external message, remote job, commit or cleanup.

## RESUME HERE — D69 smooth curve and arithmetic fingerprint, 2026-09-18

The user asked to continue verification of D68's candidate. **The 91
unchanged integer quadrics now provably define a smooth, geometrically
integral, canonically embedded genus-16 curve over Q, with good reduction
at 31.** Direct counts are 50 over F31 and 1,400 over F31², agreeing
with the corresponding predictions from the saved genus-16 Hecke data.
Read [the proof and verification report](dembele/certificates/cm-frame-verification.md).

**Method:** the Gröbner basis exhibits the coordinate ring as free of
rank 30 over Q[X15,X16] and F31[X15,X16], with basis degrees
`0,1^14,2^14,3`. Both affine charts of the resulting projection to P1
have squarefree trace discriminants of degree 90. The index-squared
formula then proves normality and smoothness; the monic flat model
at 31 transfers smoothness to Q. The graded basis and Riemann–Roch
prove geometric integrality and the canonical embedding. No large
Jacobian-minor computation or normalization call is needed.

**Files:** equations remain `cm_frame_curve_candidate.{json,m}`.
New Magma scripts are `117_cm_frame_smoothness.m` and
`118_cm_frame_point_counts.m`; the standard-library Python runner is
`dembele/pari/117_cm_frame_verification.py`. It runs three bounded
jobs (180 s and 2 GB each), or verifies saved records with
`--collect-only`. All three pass, including exact small-curve controls,
independent trace-matrix checks, and fiber-by-fiber point counts.
The report is `dembele/data/computed/cm_frame_curve_verification.json`;
logs are `cm_frame_smoothness.out` and `cm_frame_points31_degree{1,2}.out`.
The degree-two count uses 497 base Frobenius orbits, including infinity.

**Next:** identify this curve with the specified Shimura curve C.
Two counts at one prime are evidence, not a full Euler factor or an
identification proof. A sufficient criterion is exact order-four
vanishing of the quadrics at the degree-17 CM point on the actual
Shimura curve: `4*17>deg(2K)=60`. This needs independently obtained
arithmetic Shimura-side jets in matching coordinates; deriving them
from the candidate would be circular. The report makes this proof
obligation explicit. Prioritize that local arithmetic input or another
sufficient identification theorem, then construct the actual Y/C.
The genus-64 cover, target torsion and field polynomial remain open.

D68's candidate and numerical artifacts, D63–D67 backend artifacts,
and external checkouts are unchanged. Backend optimization and old
CM-function scans remain paused. D63's 111 tests remain the latest
full regression suite; these exact certificates are separate checks.
No jobs remain running. Work is local and uncommitted, with no remote
job, external message, checkout edit, commit or cleanup.

## RESUME HERE — D68 candidate curve equations, 2026-09-18

The user named M23/rigidity, Belyi code, the 17T7 paper (“7t17”),
and Hilbert modular forms code as curve-construction references.
The review led to a new arithmetic coordinate prescription and **91
independent integer quadrics for a candidate genus-16 base curve**.
Read [the source review and construction](dembele/certificates/curve-construction-sources-2026-09-18.md).

**Construction:** the seventeen order-two CM points form a projective
frame numerically. Their labelled degree-17 residue field supplies a
trace-zero basis. A left-kernel/residue calculation identifies that
basis with the canonical differential space, up to a common scalar.
This avoids the previous high-order single-point normalization. The
general lemma is exact; the target frame rank and its inherited
curve/descent/orbit inputs retain their stated qualifications.

**Results:** script 114 passes an exact Fermat-quartic control and
reconstructs numerical quadrics from the existing N=16384/12288 banks.
Their relative coefficient difference is 6.12e-15. Script 115 searches
inside the saturated rank-119 lattice of quadrics vanishing exactly
at the CM divisor. One bounded run finds 91 independent equations,
with maximum coefficient 1,514. Script 116 passes a nonsplit-divisor
control and exact Magma checks: degree 30, arithmetic genus 16 over Q;
a flat Gröbner model at 31; reduced, irreducible special fiber; and
the prescribed exact closed point of degree 17. No exact P32 coordinate
vector was recovered. The three main scripts finish successfully.

**Candidate files:** `dembele/data/computed/cm_frame_curve_candidate.json`
and `.m`. The Magma file is self-contained and defines `C_candidate`
over Q unless `k` is supplied. JSON monomial pairs use zero-based
indices. Reports are `cm_projective_frame.json`,
`cm_frame_quadric_search.json`, and `cm_frame_curve_check.json`.
Source provenance is `curve_construction_sources_20260918.json`.

**Next:** verify this candidate efficiently, starting with smoothness
at 31 and an independent arithmetic comparison with the specified
Shimura datum. General `IsNonsingular` hit Magma's Jacobian-minor limit;
a normalization/genus probe timed out at 180 seconds. Both are retained
in `cm_frame_curve_probe_limits.json`, with scripts/logs. Do not repeat
those unchanged calls as the next experiment. Arithmetic genus does
not certify smoothness, and these equations are not yet proved to
define the intended C. After identification, construct the actual
degree-three Y/C before computing target torsion. The original field
polynomial remains open.

Backend cleanup and the old CM-function scans stay paused. D63–D67
artifacts and external checkouts are unchanged. D63's 111 tests remain
the latest full regression run; D68's exact controls, numerical checks
and algebraic assertions are separate. No jobs remain running. All
work is local and uncommitted; no remote job, message, commit or cleanup.

## Strategic orientation requested — 2026-09-18

The user has lost the thread and asks whether there is a path to the
field. Answer at the level of the field construction before resuming
D67's optional cleanup work. The objective is a polynomial whose
splitting field is Dembélé's original nonsolvable extension of Q,
ramified only at 2.

The candidate route is: arithmetic equations or equivalent section
evaluations for the specified genus-64 Shimura curve Y; compute the
appropriate part of J(Y)[2]; recover projective polynomials over
F=Q(zeta_32)^+; certify the required normal closure over Q. The
representation-identification argument and marked-descent work support
this route. They do not construct the arithmetic input.

The first step remains an unresolved research task for us. We have no
usable arithmetic model/evaluation construction for the actual Y or
compatible mechanism to lift its section data. Target torsion,
arithmetic projection, coefficient recognition and full-scale cost
also remain unexecuted. The recent controls use known curves, and the
auxiliary degree-17 CM field is not the sought nonsolvable field.

Current recommendation: pause backend optimization and make an explicit
target-arithmetic construction the next research priority, with a first
independently verifiable section relation or evaluation table as its
deliverable. This is a recommendation from the review, not a newly
found construction or an approved replacement algorithm. Do not treat
another benchmark or an unchanged CM recognition scan as filling this
gap. No new computation was launched for this orientation. Read the
[stocktake](dembele/certificates/stocktake-2026-09-16.md) and
[arithmetic interface](dembele/certificates/arithmetic-section-interface.md)
alongside D67's backend results below.

## RESUME HERE — D67 allocation audit complete, 2026-09-17

The user asked to continue the bounded allocation audit. Read
[lifttors-allocation.md](dembele/certificates/lifttors-allocation.md).
All three D67 jobs and the collector pass. No jobs remain running.
All work is local and uncommitted; preserve the dirty worktree.

**Result:** the instrumented genus-16/a=51/p=97/e=4 control passes
under the same 2 GB PARI stack cap and 900-second timeout: 368.023 s
per lift, 444.494 s overall. Exact-divisor and 2-torsion checks pass.
Group multiplication takes 300.179 s, about 82% of lift time. Its two
calls contain 26 chords and two negations. Across the lift, 61 kernel
and 56 equation constructions take 303.401 s combined (leaf timings;
do not add overlapping inclusive categories). Generated-row kernel
stages take 40.808 s, about 11%. Reduced-J copying takes only 0.098 s.

**Measured allocation:** the caller occupies 273,164,736 stack bytes
at lift entry. The first reduced J2 has a 120,425,152-byte tree. Forming
the 34,458,640-byte GWV matrix adds 136,524,504 stack bytes. The
`avrho` mark is placed after GWV, so subsequent Schur cleanup retains
that obsolete workspace throughout inflation and multiplication. The
second precision step exhibits the same effect while J2 aliases J.
The largest observed checkpoint is 1,053,617,264 bytes, in the first
inflation's divisor-subtraction kernel, 780,452,528 above lift entry.
Growth to the 2 GB capacity occurs inside that kernel's rank-selection
interval. These are checkpoints, not peak stack or RSS measurements.

**Diagnostic build:** `build_lifttors_profile.py` generates copies of
four D66 C inputs in `.build/lifttors_profile`; `lifttors_profile.{h,c,py}`
provide hooks and checked insertion. Removing hooks recovers all original
C tokens, including strings/operators. Script 113 checks twenty tracing
off/on lifts for exact matrix equality, identical random states, saved
point equality and torsion. The smaller genus-4/a=51 control also passes
(10.319 s overall). That tests the chart branch; genus 16 tests the
multiplication branch. All scale tracing is single-threaded. The
genus-16 log contains 1,270 events in 294 complete nested calls.

**Next bounded change:** in a separate build, test two explicit cleanup
changes: (1) move the Schur-workspace mark to after J2/pe2 but before
forming GWV, so collecting KM also discards the no-longer-used product
workspace; (2) give `DivMul` a local stack mark and return its collected
matrix to discard intermediate field products. Neither change has
been implemented or measured. Preserve the old paths, check exact
points and both lifting branches/precision boundaries, then rerun the
same genus-16/a=51 profile under the same cap/timeout. This targets
measured lifetimes, not another lifting-kernel redesign. Keep all
required Jacobian fields, including D66's corrected auxiliary tables.
No automatic genus-64/a=51 job or cap increase.

**Reproduction:** build with `python3 dembele/pari/build_lifttors_profile.py`,
then run `python3 dembele/pari/112_lifttors_profile.py`. `--collect`
verifies saved logs, provenance, original C tokens and trace nesting;
`--only` selects jobs without writing a full report. Results are
`lifttors_profile.json`, `lifttors_profile_*.out`, and
`lifttors_d67_collect.out`. D63–D66 recorded inputs and builds are
unchanged. D63's 111 tests remain the latest full Python/Sage suite;
D67's diagnostic/native checks are separate. No target arithmetic
sections, compatible p-adic section lift, torsion or polynomial has
been obtained. CM scans remain paused. Ledgers, READMEs, CLAUDE and
upstream.lock are current through D67. No remote job, external message,
upstream checkout edit, commit or cleanup.

## RESUME HERE — D66 degree-51 control and reduction fix pass, 2026-09-17

The user asked to continue the agreed bounded calibration. Read
[lifttors-degree51.md](dembele/certificates/lifttors-degree51.md).
All work is local and uncommitted; preserve the dirty worktree.
No jobs are running. The D66 collector exits 0 with all expected outcomes.

**Result:** genus 16, p=97, a=51, e=4 passes under the unchanged
2 GB PARI stack cap and 900-second timeout, before and after the
auxiliary-table correction. The unchanged D65 library takes 364.194 s
per lift / 439.776 s overall; the corrected library takes 364.732 s /
440.569 s. Both compare with the independently known branch divisor
and check annihilation by 2. Each kernel scans and replays all 18
blocks: 2,160 equations, 67 columns, rank 33, nullity 34. Kernel time
is about 11% of lift time; other operations still grow the stack to
its cap. Timings are single local observations, not production forecasts.

**Correctness finding:** pinned `PicRed` calls matrix-only `FpXM_red`
on J[13][1:2], which are vectors of embedding matrices. Script 110
reproduces ten bad auxiliary reductions at five precisions. Its PASS
marker means the audit completed, not that the old backend is correct.
Main section/equation reduction is correct; lifting does not consume
these auxiliary fields, and prior Q8 evaluation uses unreduced J.
Earlier controls therefore retain their stated scope.

**Correction:** `build_lifttors_reduction.py` verifies D65 and creates
`.build/lifttors_reduction`, reducing each embedding matrix separately.
It retains `PicRed_original` for diagnosis and all three lifting paths.
Script 111 checks 25 independent matrix reductions, 80 projective
vectors from 20 point evaluations, 15 nested reductions, idempotence
and two malformed-shape rejections. Sixty lift comparisons and full
Q8 recovery of Q(i) also pass with the corrected build. No genus-64
control has been rerun with this library. D63–D65 sources, builds,
logs and report hashes remain unchanged. D63's 111 tests are still
the latest full Python/Sage suite; D66's native GP checks are separate.

**Storage:** script 109 verifies the degree-51 residue field, four
length-51 Frobenius cycles and a section entry outside both maximal
proper subfields. Correctly reduced J occupies 120,425,152 bytes at
exponent 2, almost its full exponent-4 size. A component model projects
1,472,765,199 bytes for principal genus-64 matrices with 663 points,
assuming comparable known-curve bases and entry sizes. This is an
object-tree projection, not peak RSS or a stack lower bound. It ignores
shared storage. The known torsion point itself is rational.

**Next bounded work:** instrument retained allocations in the corrected
genus-16/a=51 control: reduced Jacobian, GWV/Schur setup, and surrounding
group operations. Use a separate build to preserve this calibration,
the same 2 GB cap and 900-second limit, and measure before choosing an
adaptation. No automatic genus-64/a=51 run or cap increase. Further
kernel tuning has little support from the measured time split.
The actual Y still lacks arithmetic section entries and their p-adic
lifting mechanism; the section interface remains a specification.
No target torsion or nonsolvable polynomial is obtained. CM scans stay paused.

**Reproduction:** `python3 dembele/pari/build_lifttors_reduction.py`,
then `python3 dembele/pari/108_lifttors_degree51.py`. The earlier D65
baseline is script 107's optional `--only genus16_a51`. Script 108's
`--collect` checks saved logs and provenance; `--only` runs selected
jobs without issuing a full report. Results are `lifttors_degree51.json`,
`lifttors_d66_collect.out`, separate `lifttors_rows_genus16_a51.out`
and `lifttors_reduction_genus16_a51.out`, and the audit/validation/
storage logs. Corrected Q8 output has its own binary filename.
DECISIONS, REFERENCES, CLAUDE, READMEs and upstream.lock are current
through D66. No remote job, external message, checkout edit, commit or cleanup.

## RESUME HERE — D65 native row generation passes, 2026-09-17

The user asked to continue D64's native integration. Read
[lifttors-rows.md](dembele/certificates/lifttors-rows.md).
All work is local and uncommitted; preserve the dirty worktree.
No jobs are running. All nine D65 jobs pass.

**Result:** the genus-64 known-answer lift at p=97, a=2, e=4 takes
514.585 s; its full control takes 690.829 s under the unchanged 2 GB
PARI stack cap and 900-second timeout. The lift equals the independently
known [(0,0)-(1,0)] divisor modulo 97^4 and doubles to zero. Each kernel
has 21,252 equations, 259 columns, rank 129 and nullity 130. All 66
blocks are scanned and replayed. The largest block is 7,343,000 bytes:
83,398 field entries instead of the full 5,504,268. S,H caches occupy
about 14.3 MB. The kernel's largest internal stack checkpoint is about
31 MB, excluding callers and caches; this is not peak memory. Other
group operations still grow the stack to the 2 GB cap.

**Implementation:** `pari/lifttors_rows.c` implements D64's formula,
independent-row selection and complete residual replay at every
derivative precision. It raises the same good-reduction error for
rank drop. `pari/lifttors_rows.py` makes checked source replacements
without changing the precision sequence, multiplication branch or
chart branch. `build_lifttors_rows.py` produces a separate
`.build/lifttors_rows` library: `PicLiftTors` is the new native path,
`PicLiftTors_D63` and `PicLiftTors_original` retain comparisons.
The old build, source files 100–106, adapters and recorded D63/D64
computational outputs remain unchanged and are verified by digest.

**Checks:** 11,172 native/GP/original equation comparisons; 60 three-way
lift cases including origin, both branches, odd precision, nontrivial
starting precision and one/two threads; 12 prescribed kernels and
6 rank-drop rejections; Q8 end-to-end recovery of Q(i). Native scale
controls pass at g=4,a=2 (0.261 s per lift), g=4,a=51 (8.263 s),
g=16,a=2 (10.070 s), and g=64,a=2. These are single local timings.
The two genus-64 kernel stages total 77.306 s; most lift time remains
outside them. D63's 111 tests remain the latest full Python/Sage run;
the D65 native checks are a separate count.

**Next bounded experiment:**
`python3 dembele/pari/107_lifttors_rows.py --only genus16_a51`.
This optional job uses p=97,e=4 and the same cap/timeout. It has not
been launched. It measures how the remaining operations and live
Jacobian data scale at degree 51. It is excluded from the default
nine-job suite and writes its own log. No automatic genus-64/a=51
job, cap increase or further kernel tuning without a measured cause.
Arithmetic target sections and their lifting mechanism still need
construction; the section interface remains a specification. No target
torsion or nonsolvable polynomial is obtained; CM scans stay paused.

**Reproduction:** build with `python3 dembele/pari/build_lifttors_rows.py`,
then run `python3 dembele/pari/107_lifttors_rows.py`. `--collect` checks
the saved logs and hashes without rerunning. Checked copies of existing
GP controls are generated under `.build/lifttors_rows/controls`.
Results are `data/computed/lifttors_rows.json`, individual
`lifttors_rows_*.out` logs and `lifttors_d65_collect.out`. The initial
aggregate run log retains a collector failure on a normal stack-growth
warning after GP passed; the parser is fixed and five invalid-log cases
plus a valid warning case are checked. Current collection exits 0.
DECISIONS, REFERENCES, CLAUDE, READMEs and upstream.lock are current
through D65. No remote job, external message, checkout edit, commit or cleanup.

## RESUME HERE — D64 degree-51 calibration and checked row formula, 2026-09-16

The user asked to continue D63's next bounded experiment. Read
[lifttors-extension.md](dembele/certificates/lifttors-extension.md).
All work is local and uncommitted; preserve the dirty worktree. No jobs are running.

**Result:** the known genus-4 curve y^2=x^9-x at p=97, e=4, d0=9
passes at a=2 and a=51 under the same 2 GB stack cap and 900-second
timeout. One lift takes 0.264 s versus 8.356 s; full controls take
0.405 s versus 10.116 s. The exact branch divisor is checked before
and after lifting. Evaluation counts differ (46/51), so the ratio is
not a pure field-degree multiplier or genus-64 forecast. The point is
rational. A separate field/cycle/entry check proves the arithmetic
uses the full degree-51 field, not the target Frobenius representation.

**Memory:** at a=51 the 162-by-19 equation matrix occupies about
5.1 MB. Mean entry sizes project to 9.10–9.11 GB for D63's
21,252-by-259 matrix. This is a conditional object-tree projection,
not measured peak memory or a target lower bound. No genus-64/a=51
job was launched. The existing full-matrix path is not supported by
that budget evidence at the unchanged cap.

**Concrete next step:** integrate script 106's checked row-generation
formula into a separately selectable native lifting path. With
Cbar=CA^-1 and N the scattered right annihilator [-A^-1B;Id], set
S=V*U0, H_i=V*N_i. For each Schur column k, generate
diag(H_i[Ic,k])*S[Ic,:]-Cbar*diag(H_i[I,k])*S[I,:] for both input
blocks, and append rho[:,k]. Feed blocks to independent-row selection,
solve the selected system and regenerate every block for full-precision
verification. Upstream mat2col is row-major: block row j corresponds
to full-system row (j-1)*b+k. Retain original and D63 paths and their
meaningful comparisons, including good-reduction rejection. At g=64,
the equation buffer has 1/66 as many entries; total memory and runtime
must still be measured. No automatic large job or larger cap.

**Checks and files:** `pari/106_lifttors_row_system.gp` checks all
11,172 equation entries in four systems (a=2/51, derivative precision
97/97^2), kernel equality and every equation. All pass. It retains the
full matrix only as a comparison reference. It is a GP prototype,
not production C integration or a full torsion lift using that formula.
`pari/105_lifttors_extension.py` runs/collects the two full small-curve
lifts and two diagnostic jobs, checks D63 source/build digests, and
writes `data/computed/lifttors_extension.json`. Raw logs are
`lifttors_g4_a{2,51}_{scale,rows}.out`. Reproduce with
`python3 dembele/pari/105_lifttors_extension.py`; `--collect` reuses
the four logs. The D63 build must already be present.

The compiled D63 library, adapters and `lifttors_controls.json` are
unchanged. Its 111 passing tests remain the latest full regression run;
D64's GP checks are a separate count. The actual target arithmetic
sections, construction/lift mechanism, torsion and polynomial remain
missing. Repeated CM scans stay paused. Geometry and descent scope are
unchanged. DECISIONS, REFERENCES, CLAUDE, READMEs and upstream.lock are
current through D64. No remote job, external message, checkout edit,
commit or cleanup.

## RESUME HERE — D63 genus-64 lifting control passes, 2026-09-16

The user approved addressing D62's lifting memory failure. The result is
in [lifttors-memory.md](dembele/certificates/lifttors-memory.md).
All work is local and uncommitted; preserve the dirty worktree. No jobs run.

**Result:** the same known genus-64 curve y^2=x^129-x, p=97, a=2,
e=4, d0=129 now passes under the unchanged 2 GB PARI stack cap.
There are 646 evaluation points and section dimensions 66/195/324.
The lift takes 613.521 s; the full control takes 784.161 s, including
setup, a nonzero check, doubling and final verification. The lifted
point equals the exact [(0,0)-(1,0)] divisor modulo 97^4 and is killed
by 2. This is not the target Y and does not benchmark residue degree 51.

**Two allocations were addressed:** the original eager V0 products use
1.71 GB after only 48 of 129 products and then overflow. Computing
products inside each derivative worker removes that allocation, but
the original kernel solve then overflows on a 21,252-by-259 system.
The final adaptation selects independent original rows modulo p in
batches of 256, solves that small system, and checks every equation at
full precision. Both precision steps have rank 129 and nullity 130.
The full 5,504,268-entry system is still stored, so larger residue-degree
memory and time are unresolved. Stack checkpoints are not peak RSS.

**Files:** `pari/lifttors_lift.py` generates a checked adaptation of
the pinned source; `pari/lifttors_streamed.c` supplies the worker and
batched kernel. The vendor checkout remains unmodified. The default
build retains `PicLiftTors_original` for comparison. `--products-only`
reproduces the intermediate kernel overflow; `--validator-only`
reproduces D62's algorithms; `--upstream` omits local adaptations.
Earlier logs and manifests are retained; do not reclassify their
failures as passes. `lifttors_controls.json` now reports the passing
final control and separately records both earlier failures.

**Checks:** the full Q8 field-recovery control and genus-16 control pass.
Script 102: 70 validator comparisons. Script 103: 60 original/adapted
lifts, including origin, odd precision, nontrivial starting precision,
both lifting branches, and one/two worker threads. Script 104: 12 tall
systems with known kernels, including initially zero row batches, and
6 specific good-reduction rejections. All pass. The 111 existing
Python/Sage tests pass separately in `d63_tests_20260916.out`.

**Next scoped backend experiment:** use script 101 with `bench_genus=4`,
`bench_a=51`, `bench_e=4` under the same cap and timeout to measure the
larger coefficient-field cost on a small known curve. This has not been
launched. Do not infer genus-64/a=51 feasibility from the a=2 pass or
automatically launch that larger job. The actual target arithmetic
section entries, a construction/lift mechanism for them, and the field
polynomial remain missing; the interface in
[arithmetic-section-interface.md](dembele/certificates/arithmetic-section-interface.md)
is a specification, not such a construction. Repeated CM scans remain
paused. D62's geometry/descent status is unchanged.

**Reproduce:** `python3 dembele/pari/build_lifttors.py`, then
`python3 dembele/pari/run_lifttors_controls.py`. The runner uses a
900-second per-process wall limit, including verification, and kills
the whole local process group on timeout. It requires explicit PASS
markers and rejects GP errors even when GP exits zero. It now exits 0;
`--collect` rebuilds the JSON from saved logs. Source hashes are saved.
DECISIONS, REFERENCES, CLAUDE, READMEs and upstream.lock are updated
through D63. No remote job, external message, commit or cleanup.

## RESUME HERE — D62 geometry audit and actual torsion backend, 2026-09-16

The user approved D61's recommendation. The two concrete checks are now
recorded in [curve-identification-audit.md](dembele/certificates/curve-identification-audit.md)
and [lifttors-control.md](dembele/certificates/lifttors-control.md).
All work is local and uncommitted; preserve the dirty worktree. No jobs run.

**Geometry:** script 99 checks the actual saved order's product closure,
Gram determinant 2^126, maximality, finite ramification, split real place,
proved class number one and full unit signatures. The full two-layer
Brandt graph has 116 vertices, 155 edges, genus 40. The Atkin--Lehner
involution reverses nine edges and fixes no vertices; H1 eigenspaces have
dimensions 16 and 24. Its quotient stabilizes to the D45 weighted graph.
Kurihara's original Proposition 3-2/Lemma 3-3 explicitly handle torsion
and reversed edges without an odd-residue-characteristic restriction.
Only reversed edge classes, not arbitrary loops, disappear. This supports
D45's geometric identification and nonhyperellipticity conclusion. The
published conflict has not been resolved externally. Numerical polygon,
ordinary-point/moment and complex-orientation hypotheses are not newly
certified by this audit.

**Backend:** LiftTors is downloaded under ignored `dembele/vendor/LiftTors`,
pinned in `dembele/upstream.lock`. `pari/build_lifttors.py` links a single
library against local PARI 2.17.1. The untouched upstream checkout is
compiled with an explicit batched validator adaptation in the default
build; `--upstream` gives the original. Script 100 performs actual Makdisi
arithmetic, lifts and evaluations on y^2=16*x^5-x. It finds all 16 torsion
points, lifts to 7^64, verifies Frobenius/reduction/[2], and recovers a
degree-15 polynomial with splitting field exactly Q(i). The initial
branch-point auxiliary evaluation failed; nonbranch auxiliary points work.
The equation and symbolic section bases are removed after initialization,
so subsequent arithmetic tests the evaluation-matrix interface.

**Measured limit:** script 101 passes for genus 16 at p=97, a=2, e=4;
one lift takes about 10.2 s. The genus-64 known-answer control completes
initialization and doubling but `PicLiftTors` overflows a 2 GB PARI stack.
No completed genus-64 lift or production runtime is claimed. Before that,
the upstream validator also exceeded the limit; `lifttors_bounded.c`
replaces its giant stacked matrix by an exact batched criterion. Script
102 compares both validators in 70 cases including tampering; all agree.
Generic membership checking remains expensive and is not included in the
larger operation timings; the supplied point has an exact RR certificate.

**Next step:** inspect and address the allocation inside `PicLiftTors`,
then rerun the same genus-64 known-answer control. Do not automatically
increase the stack, field degree, precision or CM bank. Target a=51 and
production precision remain unbenchmarked. A concrete eventual frontend
is specified in [arithmetic-section-interface.md](dembele/certificates/arithmetic-section-interface.md):
D0=pi^*(43P) has degree 129, with a 66-column initial evaluation matrix
and at least 646 Frobenius-stable points. Its trace split is 28+38.
No arithmetic construction of those entries on the actual Y is supplied.
The degree-17 CM field remains auxiliary; no target torsion or field
polynomial has been computed.

**Reproduce:** build with `python3 dembele/pari/build_lifttors.py`, then
`python3 dembele/pari/run_lifttors_controls.py`. `--collect` reuses logs.
The runner writes `lifttors_controls.json` and deliberately exits 1 for
the recorded genus-64 failure; GP's exit code zero is not a PASS.
The Q8 binary reader handles appended GP records. Source hashes and
individual logs are saved. All 111 existing regression tests pass,
plus the separately counted 70 GP comparisons. DECISIONS/REFERENCES and
READMEs are updated through D62. No external message, remote job, commit
or cleanup. Public software/paper downloads were the only network writes
to local files; no external checkout was edited.

## RESUME HERE — D61 strategic stocktake, 2026-09-16

The user asked whether we are on the right path or should take stock.
The review is saved in
[stocktake-2026-09-16.md](dembele/certificates/stocktake-2026-09-16.md).
No new reconstruction or large computation was launched. The worktree
remains local and uncommitted; preserve it. No jobs run.

**Assessment:** the curve/Jacobian strategy remains a credible candidate,
but practical completion is unproved. D51 supplied the abstract target
representation comparison. D58's marked descent and D59's labelled CM
orbit removed important arithmetic ambiguities. D60 gives exhaustive
exclusions inside empirical boxes. We still have no exact target function
value, arithmetic model of C or Y, target torsion, or field polynomial.
The last steps primarily clarified the recognition obstruction.

**Keep the destination visible:** the known degree-17 CM field is an
auxiliary solvable residue field. The original target is carried by the
specified genus-64 Y, not merely by its genus-16 base C. Recognizing
X|D,Y|D would still require global section/model reconstruction and the
cover before this route supplies torsion arithmetic. Current exact
controls do not test a generic Makdisi torsion-lifting implementation.

**Recommendation:** pause repetition of scans in the same CM coordinates.
Choose a new arithmetic construction or a changed reconstruction
hypothesis with specified inputs, output, independent check and a
downstream operation it enables. Useful outputs are a target section
relation connected to a global model, or finite/p-adic section-evaluation
data for Y. These are research targets, not presently available routines.
D57 already audited the existing input; do not repeat a generic inventory.
A formal upper-height theorem is not required for every discovery
experiment, but another numerical attempt needs a concrete new reason
to expect information, followed by exact validation of any candidate.

**Review priorities:** check the arithmetic identification underlying the
published hyperellipticity conflict, the marked-descent hypotheses and
CM orientation inputs before major investment. Separately establish an
actual generic divisor/torsion-lifting control and representative cost.
The stocktake does not itself redo those proofs or build that backend.
It recommends changing the next unit of work, not abandoning the route;
no replacement construction or production prime has been selected.

**Sources/checks:** Mascot's model definition still requires arithmetic
section values even when no curve equation is written. Dembélé Lemma
5.2 and the marked-map theorem were rechecked independently of the
disputed hyperellipticity assertion. DECISIONS.md and REFERENCES.md
are updated through D61. This was a documentation/research review;
the latest implementation suite remains **111 tests passing** from D60.
No new analytic bank, remote job, external edit, message, commit or cleanup.

## RESUME HERE — D60 exact exclusions for CM flag boxes, 2026-09-16

The requested continuation of the descended CM-field approach is saved.
Read [cm-flag-height.md](dembele/certificates/cm-flag-height.md).
The worktree remains local and uncommitted; preserve all existing work.
No computation remains running. Older sections are historical.

**New result:** script 98 treats the rational plane span(X,Y), removing
all choices of its two generators. Its Grassmannian chart has pivots
at field-basis indices 1,7 and 28 free entries. The four D59 coordinate
banks give empirical radii 3.18e-14 through 2.99e-12. There is no complete
individual rational chart at denominator cap 10^7 (27/28 entries have
hits, all ambiguous). No small-plane shortcut was found in these boxes.

**Exhaustive certificate within each box:** exact rational lattice and
exterior-power bounds exclude every rational subspace up to these
primitive integer Pluecker heights in the fixed D59 trace-centered basis:

    Q X:          19,927,223,139
    Q Y:          13,481,861,693
    Q X + Q Y:    43,166,965,625,539,309,014.

For a line this is ordinary projective integer-coordinate height. For
a plane it is the maximum primitive integer minor, independent of the
plane's generators. It still depends on the ambient field basis.
These strengthen D59's nonexhaustive unsuccessful searches: no small
candidate inside those boxes was merely missed by LLL.

**Critical scope:** the boxes are exactly defined from saved decimals,
but are empirical. No analytic theorem places the actual target in
them. Thus the certificates are NOT unconditional target-height lower
bounds. They give neither an upper height bound nor exact evaluations.
D56/D58's hypotheses and D59's numerical orientation inputs persist.

**Certificate:** write the chart as [I_r|T], center A, radius E. At
integer scale S put R=round(S*A), M=[I_r R; 0 S*I]. Save B=V*M and
verify V is unimodular. Recompute exact Gram--Schmidt squared lengths
d_i. If L_r is the product of the r smallest d_i and

    C_r=product_i (1+sum_j (abs(R_ij-S*A_ij)+S*E_ij)^2),

then every rational space of height H in the box satisfies H^2*C_r>=L_r.
The report proves the exterior-lattice lower bound and the Hadamard
upper bound. `--verify` checks saved certificates without new LLL.
All chart operations use exact Q(i) arithmetic on the saved decimals.

**Checks/artifacts:** `dembele/pari/98_cm_flag_height.py`,
`dembele/tests/test_cm_flag_height.py`, identical
`cm_flag_height.{json,out}` with source hashes, and full log
`cm_flag_height_tests_20260916.out`. Eight new controls bring the suite
to **111 passing tests**. These include a compound-matrix check of the
exterior formula, exhaustive small-plane enumeration, tamper rejection,
and recovery of a known exact field plane after complex mixing/noise.
Both DECISIONS.md and REFERENCES.md are updated through D60.

**Next:** obtain new arithmetic information about the evaluation flag,
or justified error and upper-height bounds in this fixed field basis.
An analytic error certificate alone would make these lower bounds
apply to the target, but still would not determine it. A concrete
finite-prime evaluation of the line/plane would be new input; the
abstract residue algebra and Frobenius permutations alone are not such
an evaluation. Do not repeat the same small-height scans, orbit
construction, or automatically launch another analytic bank.

No new analytic bank, remote job, external Belyi edit, message, commit
or cleanup. Exact target evaluations, C/Y, required torsion and the
nonsolvable field polynomial remain open.

## RESUME HERE — D59 labelled CM orbit and joint reconstruction, 2026-09-16

The requested continuation of descent is complete. Read
[cm-orbit-recognition.md](dembele/certificates/cm-orbit-recognition.md).
All research work remains local and uncommitted; preserve the existing
worktree. No computation remains running. Older sections are historical.

**New exact arithmetic:** script 96 exports the saved quaternion order
and all seventeen CM embeddings, checks optimality by embedding O_K,
and independently proves Cl(K)=C17 with Sage/PARI proof enabled. Relative
to point 8, totally positive intertwiners u_i give fractional ideals
I_i={a in K : u_i*iota_0(a) in O}. Saturated intersections and the exact
norm identity N(I_i)*N(nrd(u_i))=1 prove I_i*O=u_i^-1*O, supplying the
Shimura-reciprocity action. Class labels in saved point order are

    [10,12,16,14,3,1,5,7,0,4,11,15,8,9,2,6,13].

**Root matching:** Magma proves the order-272 Galois group in its
31-adic calculation and compares the complex root numbering. The
C17-invariant sum r_j^2*r_Frob(j) gives an exact degree-16 resolvent;
its coefficient lift has an explicit root/coefficient bound. Matching
that generator in K selects q=(31,beta-19), with ideal class 3. The
resulting zero-based point-to-root lookup is

    [13,10,15,3,4,16,9,14,2,1,8,5,11,12,6,7,0].

**Scope of matching:** its CM orientation is selected from the saved
disk action, and its reference point from the real/conjugate pattern
of both X and Y. Complex conjugation is class negation; discrepancies
are below 9e-18, well separated from incorrect pairs. Complex root
numbering uses Magma's complex/p-adic comparison; complex GaloisProof
is not implemented. These are explicit numerical/software inputs,
not a new analytic error certificate. D58 descent and D56's existing
ordinary-point/nonzero-moment hypotheses remain unchanged.

**Simultaneous reconstruction:** script 97 uses a 256-bit reduced
integral basis, discriminant 2^79, then centers its sixteen nonconstant
elements by trace. The actual evaluation matrix has infinity-norm
condition 40.9175. Default-precision basis reduction was inadequate;
do not use it without checking the resulting matrix. All four saved
CM banks give coordinate vectors. Projectivizing leaves fifteen ratios.
At denominator cap 10^6, X and Y each have hits in 10/15 intervals
(7 and 5 unique), so neither gives a complete vector. A joint LLL
search with scales 10^10 through 10^13 and projective height cap 10^9
accepts no direction. Best fits without the cap have heights about
1.04e12 and 6.14e11 and are rejected as recognitions. The intervals are
empirical; LLL does not exhaust the height cap. No true-height lower
bound or failure of descent follows.

**Next:** the labelled field identification is now available. The
missing exact data remain the line ev_D L(17P)/<1> and compatible plane
ev_D L(18P)/<1> inside the trace-zero residue field. Seek an arithmetic
construction of those spaces or a justified height/accuracy budget
for their reconstruction. Do not redo the orbit construction, repeat
the same interval scans, or launch another analytic bank automatically.
Recognizing these restrictions would still not give a whole curve model.

**Artifacts/checks:** `dembele/magma/96_cm_root_action.m`,
`dembele/pari/96_cm_orbit.py`, `97_cm_field_recognition.py`,
`cm_root_action.out`, and identical report pairs `cm_orbit.{json,out}`,
`cm_field_recognition.{json,out}` with source hashes. Seven new controls
include exact ideal classes, Frobenius/conjugation compatibility,
stable inversion, noisy recovery of a known exact element, a height
cap, and rejection of a corrupted validation bank. All **103 tests
pass**; log `cm_orbit_tests_20260916.out`. No new analytic bank, remote
job, external Belyi edit, message, commit or cleanup. Exact target
CM values, C/Y, torsion and nonsolvable field polynomial remain open.

## RESUME HERE — D58 marked descent and rational pilot, 2026-09-16

The user's requested descent investigation is complete. Read
[marked-descent.md](dembele/certificates/marked-descent.md).
All work remains saved locally and uncommitted; preserve the existing
worktree. No job remains running.

**Descent:** Dembélé's Lemma 5.2, overlooked in D57, descends the
genus-40 curve and its Atkin--Lehner involution independently of the
disputed hyperellipticity claim. Carry canonical conjugation through
the norm-one/normalizer cover and its unique Q(zeta_32) CM point.
The marked cover has field of moduli Q. Sijsling--Voight's marked-map
theorem descends it, so P and D=Branch(pi)-P descend together.
This uses canonical-model theory, not merely equal signatures or the
existence of an F-rational point. No explicit descent matrices computed.

**Function consequence, conditional on D56's existing hypotheses:**
any automorphism preserving P,D fixes the normalized X,Y. Their
coprime pole degrees 17,18 imply that they generate the function field,
so the marked curve is rigid. This removes the F-twist ambiguity and
makes its unique comparison maps satisfy the Weil cocycle automatically.
Thus X,Y and H_X(T)=Norm_D(T-X) are defined over Q. Ordinarity and
nonzero moments on the target remain numerically supported, not certified.
H_X is irreducible of degree 17, and the abstract CM residue algebra
over Q is Q(theta) for Elkies's known polynomial. The target element
and the labelled identification with numerical CM points are still unknown.

**Exact checks:** script 95 proves class/narrow class number one for F,
class number one for Q(zeta_32), invariance of p=(2+b) under
sigma(b)=b^3-3*b via `2+sigma(b)=(2+b)*(b-1)^2`, and the branch count 18.
The order-16 lift on K has eighth-power multiplier -1, as in D57.
These support the literature argument; they are not descent maps.

**Bounded rational pilot:** reused all four saved CM polynomial banks.
The empirical interval radius is ten times the largest checkpoint/fit/
probe complex L1 change or imaginary part. Exact fraction and Farey
calculations find 0,0,5,10 hits among 15 independent coefficients at
denominator caps 10^3,10^4,10^5,10^6. At 10^6 every hit is ambiguous;
indices 0,1,2,3,10 have none. No complete polynomial is recovered.
The identities c17=1, c16=0, 2*c15=3*c14 reduce the independent count.
These are exhaustive interval tests, not certified coefficient bounds.
A simple exact control X1=(17*theta-2)/30 has monic coefficient
denominators as large as 2.15e23; failure of this pilot is not an
intrinsic-height lower bound.

**Next:** construct a labelled CM class-group orbit identification with
the embeddings of Q(theta), then assess simultaneous recognition of
X|D in that algebra using all seventeen values. Its availability and
the adequacy of current accuracy still need checking. The exact
evaluation flag from D57 remains an alternative target. Do not repeat
the independent-coefficient scan or increase precision automatically.
Descent supplies a rational target, not its exact evaluations.

**Artifacts/checks:** `dembele/pari/95_marked_descent.py`, six new tests,
identical `dembele/data/computed/marked_descent.{json,out}` with source
hashes, and `marked_descent_tests_20260916.out`. All **96 tests pass**.
No new analytic bank, remote work, external Belyi edit, message, commit
or cleanup. Exact C/Y, target torsion and nonsolvable field polynomial
remain open. Earlier handoff sections below are historical.

## RESUME HERE — D57 exact CM-input audit, 2026-09-16

The D56 resume task is complete. Read
[cm-arithmetic-input-audit.md](dembele/certificates/cm-arithmetic-input-audit.md).
The existing uncommitted worktree is preserved. All local jobs finished.

**Exact input recovered:** script 94 reloads the saved domain and checks
all seventeen order-two elliptic generators. Their discriminants are
(-2-b)*s^2, with an explicit common square witness, so they embed the
expected K=F(sqrt(-2-b)). It independently verifies K/Q cyclic of degree
16, with generator beta -> beta^3+3*beta and eighth power conjugation.
The published h(K)=17 is retained as a source input, not recomputed.
CM reciprocity and the Harbater class-field identification give an
abstract presentation A_D=H^0(D,O_D) isomorphic to F[t]/H(t), using
Elkies's known degree-17 polynomial. This is NOT the target field
polynomial or the polynomial of D56's X-values. No labelled field-to-CM
embedding or exact section evaluation has been constructed.

**Finite data:** H is irreducible modulo 31 (which splits in F), proving
irreducibility over F. Its reductions have types 17 at 31 and 1,2^8 at
97,127,191. Q(theta) has discriminant 2^79; the power-order index is
23126202879577982, so not every odd prime is safe for this presentation.
These are exact reductions of the residue algebra, not of X or Y.

**Why that input is insufficient:** two explicit pairs in this same
algebra satisfy all five D56 trace-normalization conditions, but have
E(X^2)=16/225 and -32/5041. Their spectra differ even after permutation;
both differ from the saved target value about 0.39041414756552571896.
They are counterexamples to field-only reconstruction, not functions
asserted to have the required poles on C.

**Concrete reconstruction target:** the nested subspaces
`<1> subset ev_D L(17P) subset ev_D L(18P) subset A_D`. Under D56's
ordinary-point and nonzero-moment hypotheses, these have dimensions
1,2,3, and restriction is injective. Given this flag, exact trace
operations determine X|D,Y|D. Abstract flags form a 29-dimensional
family; the field alone does not select the curve's flag. Recognizing
the flag would still not supply a whole curve model.

**Availability verdict:** the inspected Hecke, Brandt, graph, CM,
Belyi and section-ratio data supply no independent exact target value,
reduction, or height bound. Seventeen CM conjugates at one embedding of
F are not eight embeddings of their F-valued traces. The Borcherds/
Whittaker CM-norm literature does cover totally real fields, but needs
a constructed input form and divisor; no such representation of these
functions is available. No universal impossibility is claimed.

**Next:** do not repeat the field-only audit, plane fits, or automatic
precision increases. A new arithmetic evaluation construction must
supply the flag above, or section multiplication/evaluation tensors
that determine it. An alternative is to construct a specific
special-divisor function to which a CM-value formula applies; knowing
K or H alone is not that construction. The report lists the missing
inputs for each route. A compatible descent of the marked objects to Q
has not been established here and must not be silently assumed.

**Artifacts/checks:** `dembele/pari/94_cm_arithmetic.py`, six controls in
`dembele/tests/test_cm_arithmetic.py`, and identical
`dembele/data/computed/cm_arithmetic_audit.{json,out}` with source hashes.
All **90 tests pass**; full log `cm_arithmetic_tests_20260916.out`.
No new analytic bank, remote job, external Belyi edit, message, commit or
cleanup. Exact C/Y, target torsion, and the nonsolvable field polynomial
remain open.

## RESUME HERE — D56 CM-normalized global functions, 2026-09-16

**Session closed at the user's request, 2026-09-16.** Resume from this
section and [the D56 construction report](dembele/certificates/cm-pointed-maps.md).
Older "next step" and running-job notes below are historical. All work
is saved locally on branch `main`, based on commit
`37b4793beea8ebe8844c17cf4e974d28025b957c`; the research changes remain
uncommitted, including new scripts and data. Preserve the current
worktree. No computation from this session is still running.

**First task on resumption:** audit whether the specific CM traces or
section ratios below can be obtained from independent exact arithmetic
data (conjugates or reductions). Knowing the CM residue field alone
does not provide the values of X and Y. Identify an actual available
input and reconstruction target before another large precision run.
This audit has not yet been carried out.

**User steering:** pursue a concrete arithmetic description of a useful
map/function on this specific curve, with preference for their Belyi
code and thesis. This bounded construction and conditioning experiment
is complete. Read `dembele/certificates/cm-pointed-maps.md` first.

**New arithmetic description:** let P be the distinguished order-32 CM
point and D the sum of the seventeen order-two CM points. D is F-rational:
D+P is the branch divisor of the canonical genus-40 double cover of C.
Conditional on P being ordinary, L(16P), L(17P), L(18P) have dimensions
1,2,3. Choose x with sole pole 17P and y with sole pole 18P. Write
E(f)=sum_{Q in D} f(Q)/17, with no complex conjugation. Set

    X = E((x-E(x))^2)/E((x-E(x))^3) * (x-E(x)),
    z = y-E(y)-E((y-E(y))*X)/E(X^2)*X,
    Y = E(z^2)/E(z^3)*z.

Under nonzero second/third moments, X,Y are invariant under every change
x -> a*x+b, y -> c*y+d*x+e. Hence they descend to F, without an arithmetic
input basis or D52 scale. Their pole degrees 17 and 18 are coprime, so
F(C)=F(X,Y). The global function X/Y is a uniformizer at P. These are
conditional arithmetic characterizations plus numerical representatives;
no exact coefficients have been recognized. They are not Belyi maps.

**Implemented:** script 91 solves A*b^2=B*a^2 for highest canonical
forms a,b of orders 15,14. The quotients A/a^2 recover L(mP). It checks
the product-span and multiplication ranks, removes the constant pair,
and compares native 16384/12288 checkpoints plus 256/121-jet fits.
Dimension two at m=17 also rules out any extra common zero of a,b,
provided that dimension is established exactly. All current rank
assertions remain numerical. Script 92 evaluates these functions at
the actual saved CM points with two denominator charts and circular
averages, then applies the trace normalization.

**Checks/results:** arithmetic and raw complex flag bases give normalized
CM values differing by at most 1.94e-17 for X and 5.34e-17 for Y. Across
checkpoints the differences are about 1.25e-12 and 1.86e-12; same-checkpoint
agreement is not an independent error bound. The initial proposal that
D-17P is principal fails decisively at empirical accuracy: raw x-values
spread 22.8 versus discrepancy 6.87e-12. The CM value polynomial is saved
numerically but not recognized. Large uniformizer coefficients are not
height estimates.

**Conditioning outcome:** script 93 finds X/(Y+3X) far better than X/Y
(first-16 jet condition 1.72e10 versus 7.27e20), still worse than the
old D52 condition about 849. The 172-monomial plane relation with
17i+18j<=306 is NOT recovered. A triangular fit fails; balanced row
radii .25 and .5 show rank 171 and impressive singular gaps but fail
unweighted unused/held-out rows with residuals near one. Coefficient
vectors also disagree by relative 1.17e5 across checkpoints. The final
`pointed_map_model_balanced3_16384.*` explicitly rejects every fit.
Do not treat the weighted residuals, old generic statuses, or failed
coefficients as curve equations, precision evidence, or height bounds.

**Artifacts:** `pointed_map_{flag_,}16384.*`,
`cm_pointed_maps_{flag_,}16384.*`, `cm_pointed_maps_comparison_16384.*`,
and `pointed_map_model_{,shift3_,balanced3_}16384.*` under
`dembele/data/computed/`. Eight JSON/out pairs and eight distinct source
hashes checked. Scripts 91–93 and six new exact/numerical controls are
in the workspace. All 84 tests pass. Exact controls genuinely reuse
`belyi/pointed_series.py` and the thesis Q8 model.
The full test log is saved at
[`dembele/data/computed/pointed_maps_tests_20260916.out`](dembele/data/computed/pointed_maps_tests_20260916.out).
The reproduction commands are in the D56 report and `dembele/pari/README.md`;
temporary files under `/private/tmp` are not required for resumption.

**Next:** work from the section-ratio representation and these specific
CM-normalized arithmetic objects to identify useful exact reductions,
conjugates, or justified height/precision information. A degree-18 plane
equation is currently much less stable than the section ratios. Do not
repeat the same plane fits or recognize their rejected coefficients.
The construction specifies the arithmetic target; it does not establish
that the current precision suffices to recover it. Exact C/Y and target
torsion remain open. No field polynomial, new analytic bank, remote job,
external Belyi edit, message, commit or cleanup. No job remains running.

## RESUME HERE — D55 marked-pencil scan and direct reconstruction, 2026-09-15

**User steering:** "please proceed" authorized the proposed 60
normalizations, cross-bank comparison and recognition of D54's
weight-22 pencil. This experiment is complete. Read
`dembele/certificates/marked-pencil.md` for the proof, results and commands.

**Implemented:** `dembele/pari/90_marked_pencil.py` evaluates all 60
choices of three of the five leading coefficient-zero points for
(0,infinity,1). Their 120 displayed coordinates give 30 distinct
cross-ratio expressions, rationally related rather than independent
evidence. The ranking uses chordal fit error divided by minimum point
separation. All methods select labels (0,4,3), corresponding to
(X7*X15, X11^2, X10*X12). The remaining coordinates are approximately
0.45242536589442931543 and 0.04150354539788466512.

**Better reconstruction:** the default `--method direct` fits the pencil
from its 25 native differential products, avoiding the full 91-quadric
interpolation. Current fits use 256/61 training and 512/128 checked jets.
Their discrepancies in the two selected coordinates are 1.73e-22 and
3.97e-21, improvements of 162 and 60 times over the quotient approach.
The n=12288/16384 changes are still 1.17e-16 and 1.88e-16. Exploratory
tolerances of 1e-20/1e-19 use an unproved geometric-tail estimate from
three truncations; do not call these certified digits or error bounds.

**Simpler field argument:** conditional on the true differential space,
F-rational P, ordinary vanishing flag, rank 23, and five distinct nonzero
coefficient functionals, the marked points of the pencil are F-rational.
Their cross-ratios are invariant under every flag-preserving triangular
basis change. This removes D52's formal-coordinate and scale assumptions
for these invariants. `--basis-gauge flag` inverts just the first 16 raw
jets and balances columns; its coefficients are not asserted F-defined.
It reproduces the two invariants within 2.43e-22 and 1.89e-21. All 30
expressions agree within both empirical tolerances. The points are on
the pencil parameter line, not known Belyi branch points.

**Recognition:** the initial quotient scan had two height-32 trials
representing one exact F candidate in equivalent charts. Both direct
reconstructions reject it in all six charts, by about 5.8--10.8 times
their empirical tolerances. Status: incompatible with current empirical
accuracy, not an exact non-equality theorem. No candidates in the direct
scan of all 30 expressions at degree-eight limits 4,8,16,32, or the two
best coordinates through 64. Degrees 1,2,4 use limits 1000,100,8.
PSLQ failure does not prove a height lower bound.

**Artifacts:** `marked_pencil_{scan_,direct_,direct_audit_,flag_,comparison_}16384.*`
and `marked_pencil_16384.*` under `dembele/data/computed/`. The latter is
the original rejected-candidate report, SHA256
`fd4b37e082637170af2a8c5856fad5864b9ae10bd3f8a31e6a0e27db17d060fd`;
do not overwrite it. The direct and flag audit reports refer to that hash.
The comparison report records the three source hashes and all 30 checks.

**Next arithmetic decision:** audit availability of corresponding
Galois-conjugate or finite-field data for this pointed Shimura curve, or
a justified height/precision budget for these invariants. The current
single-embedding bank provides neither. The flag-preserving coordinate
freedom has already been eliminated from these invariants; do not repeat
these 60 charts or automatically increase n without a concrete arithmetic
reconstruction plan. This bounded failure does not rule out the curve
route. Exact C/Y, the 48-direction cover conditioning and target torsion
remain open.

All 78 tests pass, including exact transformations on the user's thesis
Q8 branch-point configuration and an exact triangular-change control.
No local job remains running. No new analytic bank, remote computation,
external Belyi edits, message, commit or cleanup. No target field polynomial.

## RESUME HERE — D54 arithmetic quadrics and completed recognition pilots, 2026-09-15

**User steering:** continue the actual next steps; stopping at D53's
review milestone was premature. No further permission was needed. Read
`dembele/certificates/arithmetic-quadrics.md` for the results and commands.

**Implemented:** scripts 85–86 recover all 91 base quadrics in D52's
conditional F-normalization. Only 32 jets are needed to compute the fixed
basis matrix `M=T^-1 diag(lambda^i)`. Homogeneous relations are then fitted
in the original analytic parameter, avoiding long formal substitution.
The matrix condition is about 849. Script 86 uses native ball polynomial
and matrix arithmetic and preserves decimal coefficient strings; the
balls do not bound geometric or truncation errors. Fixed monomial and
interpolation indices make comparisons meaningful.

**Latest native base bank:** `acb_refinement_16384.{acb,json,out}` and
`acb_refinement_16384_run.log`. The local run took 1064 seconds. Its
finite-system residual is 1.36e-41, actual finite Cauchy defect 1.32e-22,
changed-quadrature defect 1.31e-22, and independent 275-side defect
3.86e-20. Do not claim 40 correct digits. Script 79 now factors its
Fortran-order matrix in place: the one n=16384 matrix is 4 GiB, versus
two 2.25 GiB matrices in the older n=12288 implementation. This is tested
and the actual overwrite is confirmed in the report. No job is running.

**Equation accuracy:** `precise_quadrics_16384.json` versus native 12288
differs by 1.397e-14 in relative norm. The new coefficient imaginary norm
is 7.117e-21. A separate first-61-jet fit,
`precise_quadrics_16384_shortfit.json`, agrees with the later-jet fit to
7.31e-21. Those two fits use the same source; they are not independent
geometric banks or a proof of twenty correct digits. The corresponding
native 8192/12288, double 12288 and double script-85 comparisons are saved.
The old Châtelet 12288 double bank was fetched and hash-verified; no new
remote computation was launched.

**Recognition completed:** script 87 finds zero candidates among all
3,003 eligible nontrivial entries, in either power or cosine basis, and
2,933 scale-invariant ratios. Bounds are 1000,100,8,16 for field degrees
1,2,4,8, with empirical tolerance 1e-18. The near-integer normalization
entries are excluded. Script 88 tests `J=A3^2/A2^3=1/(144*G2)`; an older
height-32 near-match fails with the new data. No candidate at tolerance
1e-20 through tested height 64. No accepted algebraic coefficient.

**Direct equation search:** script 89 runs bounded LLL on the full
136-monomial equation space over Q and F; neither gives a candidate.
Its `--min-weight 20` and `--min-weight 22` restrictions yield numerical
quadric spaces of dimensions 11 and 2, with well-separated product ranks
25 and 23. The smaller F lattices finish in 7.62 and 2.03 seconds, again
without candidates. The threshold is empirical relative residual 1e-20
and integer height <=64. LLL failure does not prove height lower bounds.
Reports are `quadric_lattice_{rational,field,weight20,weight22}_16384.*`.

**Next focused coordinate work:** use the weight-22 pencil and its five
leading coefficient-zero points to try a map-defined normalization before
another large n increase. A first unconditioned cross-ratio probe loses
several digits; see the certificate. Arithmetic reconstruction remains
the barrier to supplying exact relations for the relative cubic. The
cover's new 48-direction conditioning problem is still open. Do not
restart the broad searches above or present numerical quadrics as exact.

All 71 tests pass, including exact genus-four reconstruction, the user's
Q8 controls, field-basis/recognition controls, lattice recovery of a known
quadric and rejection of tiny embedded units. External Belyi files were
preserved. No exact C/Y, target torsion or field polynomial; no commit,
cleanup, external message or new remote launch. All local jobs finished.

## RESUME HERE — D53 M23 review and relative cubic, 2026-09-15

**User steering:** revisit the recent M23 paper, previous agent work in
this repository, and https://www.shaowuzhang.com/files/how-we-found-m23.pdf.
The linked note now has a revised title; its mathematical account agrees
with our saved preliminary copy. Read
`dembele/certificates/m23-coordinate-review.md` first.

**Recovered prior work:** D3's actual map-defined normalization and Newton
factor recognition (`rigidity/12`, exact result in `14`); D9's j-invariant
approach; D21's low-weight Igusa/precision diagnostic. Do not rediscover
these or claim the M23 lesson is new here. Corrected the rigidity README's
overstatement that triangle-coordinate recognition failed at any precision:
Zhang reports attempts at 40,60,90 digits. The separate cubic reduction
algorithm mentioned in his note is not in the published verification repo.

**New formulation:** for an F-defined trace-zero differential omega on Y
and F-defined eta on C, z=omega/pi^*eta is a primitive generator of the
degree-three extension and satisfies T^3-Tr(z^2)*T/2-Tr(z^3)/3=0.
There are 18 transposition AND nine three-cycle branch points. The two
trace sections lie in spaces of dimensions 72 and 111 on C. An exact C,
its branch divisors and an arithmetic generator remain missing.

**Bounded experiment:** script `84_relative_cubic.py --marked-scan` reuses
the existing Belyi cover banks, with no new large solve. Complex alignment
using both a,b sectors has condition 2.91 and unused-jet discrepancy 1.57e-4.
Sampled pole-cleared trace coefficients differ by 0.00037–0.00220 across
banks. Homogeneous cubic side error is 2.97e-6 (381 samples,273 sides;
worst pointwise 5.08e-5). These use an arbitrary complex line: they do not
prove F-descent. Five attempts to normalize a line using both marked
points instead give discrepancies 0.673–1.343 and are unsuccessful.
Report: `relative_cubic_4096.{json,out}`, with hashes and exact reproduction
command in the certificate. Six new controls bring the suite to 58 PASS.

**Next:** adapt script 74's base-quadric recovery to script 83's D52
arithmetic normalization. Compare equation coefficients and unused jets
across the two saved C banks before recognition. Use exact known relations
to reduce the subsequent relative cubic/Riemann–Roch problem. Do not
require recognizing all 48 differential series first, and do not equate
the successful complex trace check with an arithmetic coordinate solution.

No exact C/Y model, target torsion or field polynomial. All jobs finished;
no external package edits, remote work, messages, cleanup or commit.

## RESUME HERE — D52 marked-point normalization, 2026-09-15

**User clarification:** prioritize `belyi/`, their thesis, and their two
coauthored Belyi papers. Local thesis and first paper are in
`/Users/musty/michaelmusty.github.io/assets/{musty_thesis_final,belyi}.pdf`.
The external `/Users/musty/Belyi` implementation remains in use and was
not edited. The 2014 paper has four authors: Klug, Musty, Schiavone, Voight.

Read `dembele/certificates/pointed-normalization.md` first. It proves a
conditional arithmetic-normalization construction: normalize the highest
base differential by a formal integral, then cancel its remaining scalar
with a weight-one coefficient ratio. On C use
`lambda=12*[tau^16]H13/[tau^16]H14`; pull the resulting F-parameter back
through the F-rational, unramified P32 branch of Y/C. Rank/nonvanishing
hypotheses remain numerically supported, not certified. This is a new
argument; MSSV Remark 4.4.1 itself only reports numerical field behavior.

`belyi/pointed_series.py` is the exact reference and reuses
`belyi/validate_q8.sage`. It checks nonlinear parameter/basis invariance
on the thesis Q8 curve and refuses an eighth-root ambiguity at infinity.
The numerical script `dembele/pari/83_pointed_normalization.py` uses
independent Lagrange inversion. Extra tests cover a nonordinary quartic
point and fixed coefficient functionals. All 52 tests pass.

**Latest cover bank:** `belyi_cover_pilot_4096.{json,npz,out}`. The run
took 234 seconds locally; finite defect 1.04e-6, changed quadrature
1.16e-6, worst sampled side defect 2.75e-5. The 48th/49th eigenvalue
distances from one are 7.68e-7/0.391. Native adapter agreement 2.88e-16.
This is still a numerical candidate space, not an exact or certified basis.

**Main finding:** initial first-48 new-jet normalization is unstable:
its matrix condition rises from 9.08e4 at n=2048 to 4.50e7 at n=4096,
and normalized coefficients change by order one. This does not prove a
different vanishing sequence. Once the parameter is F-defined, any
invertible selection of 48 coefficient functionals gives an F-basis;
the final method thus avoids assuming the new vanishing orders.
Selection among 60 coefficients is the best of the small trials, but its
original matrix condition is still 7.79e6 and the unselected coefficients
change by 0.101 in relative norm. Whitening alone hides this conditioning.

Artifacts: `pointed_normalization_control.{json,out}`;
`pointed_normalization_{2048,4096}.{json,out}` for the initial gauge;
`pointed_evaluation_4096.{json,out}` for 96 coefficients;
`pointed_evaluation_4096_60.{json,out}` for the current 60-coefficient
selection; `pointed_evaluation_lengths.json` for the bounded length scan.
Script 83 defaults to the last comparison, with a common base n=10240
anchor. Its reports include fixed selected indices and input hashes.

**Next:** improve arithmetic parameter/basis conditioning on these saved
banks, e.g. a bounded trial of small rational parameter changes. Check
independent coefficient stability before another larger solve or LLL
recognition. The field argument and exact controls are established, but
no exact new coefficient, algebraic Y, target torsion, or field polynomial
has been obtained. No jobs remain active; no remote work or commit.

## RESUME HERE — D51 target proof and Belyi-code adapter, 2026-09-15

**Persistent user preference:** prioritize Belyi maps and the user's code
where useful; this is preferred, not mandatory. The relevant package is
`/Users/musty/Belyi`. Its files were preserved. The adapter compiles its
C source into ignored builds inside this workspace.

Read `dembele/certificates/target-realization.md` and
`dembele/certificates/belyi-cover-pilot.md` first.

**Representation gate:** the first document gives the local-type/JL and
integral Hecke argument realizing both original residual systems as actual
Galois-stable subspaces of canonical J(Y)[2], each of F2 dimension 16.
Script 80 checks their exact CRT projectors in T31. This uses the recorded
Hecke input and standard cohomology theorems; it does not compute the
actual H1 matrix. A recognized model must still be identified with Y.

**Direct cover pilot:** `dembele/pari/81_belyi_cover.py` reuses the user's
`Belyi/Cext/powser_arnoldi.c` through `belyi_cauchy_bridge.c`. All 277
side images were aligned with the exact quaternion elements. The n=2048
pilot has 48 eigenvalues within 0.000470 of 1, with the 49th ~0.398 away.
Finite-operator defect is 0.000588, changed-quadrature defect 0.000642,
and worst sampled side defect 0.00908. This is a converging numerical
candidate space, not an accurate or certified basis for recognition.

Saved banks: `belyi_cover_adapter_64.*` and
`belyi_cover_pilot_{256,1024,2048}.*` in `dembele/data/computed/`.
The largest run took 43.6 seconds after optimizing dense assembly; the
older n=1024 timing used a slower version. Pilot nodes are double
precision. Native operator checks agree to 2.8e-16, but its arithmetic
balls are too wide to give useful bounds. A small n=256 Arnoldi run
failed; its zero return is explicitly marked invalid.

**Belyi torsion control:** script 82 uses the user's Q8 example
`y^2=16*x^5-x`, with degree-eight Belyi map `(4*x^2+1)^2/(16*x^2)`.
It constructs all 16 two-torsion points over F49 and their Frobenius
action; #J(F49)=4096. This is exact hyperelliptic arithmetic, not yet
a generic Makdisi or p-adic lifting benchmark.

**Next:** justify the arithmetic normalization/field of sections on Y,
then choose multiplication/evaluation data for reconstruction. Inspect
the user's Belyi reconstruction routines first where their inputs fit.
Use the Q8 example to test a generic torsion backend. The norm-97 cofactor
check and genus-64 lifting cost remain open. Increasing n should serve
a specified arithmetic test.

All 47 tests and the exact script PASS checks pass. No remote launch,
external message, commit or cleanup. No exact Y, target torsion points
or Dembélé field polynomial. Existing work remains intact.

## Previous strategic handoff — D50 review, 2026-09-15

**User asked whether this is still the best path to the field.** Read
`dembele/certificates/route-review-2026-09-15.md`. Retain the curve/Jacobian
route as the strongest concrete candidate identified, but replace the
automatic next genus-16 precision run with checks of the missing links.
An end-to-end practical construction is not yet demonstrated.

**Revised next work:**

1. Finish the sign-type/local Jacquet–Langlands comparison with the
   specified genus-64 curve. Establish an actual Galois-stable target in
   its 2-torsion, not just a constituent of a semisimplification. An
   integral Hecke projector plus irreducibility may avoid computing a
   complete integral homology comparison.
2. Pilot the 48 new differential directions on Y using the standard S3
   representation on the existing domain. The order-32 CM center has
   sparse sectors w^(31+32n) and w^(15+32n). Justify the arithmetic field
   of the CM normalization before broad recognition searches. A complete
   genus-16 model is not a prerequisite for this analytic pilot.
3. Assess the torsion backend with actual explicit-curve controls and
   representative genus/extension arithmetic. The full Euler cofactor
   check at norm 97 is still open. Do not regard that prime or any
   coefficient height as settled.

**Useful deduction:** the degree-three map Y -> C splits old and new
2-torsion via pullback and norm, since [3]=1 on 2-torsion. This gives a
96-dimensional F2 new summand, not yet the 16-dimensional target.

The published hyperellipticity claim still conflicts with the local graph
audit; Qiu v2 §8 cites the original theorem rather than independently
proving it. A targeted audit of the graph's arithmetic identification is
more useful than repeating the finite automorphism enumeration.

No new large or remote computation was launched in D50. No exact curve,
arithmetic evaluation model, target torsion, or field polynomial exists.
D49's solver/checkpoints and all previous work remain available below.
Its N=12288 command is an optional bounded convergence experiment, not
the automatic next milestone. This review changed documentation only.

## Previous implementation handoff — D49 completed, 2026-09-15

**The D48 immediate implementation objective is complete.** Compiled FLINT
Cauchy actions and arbitrary-precision residual/iterate arithmetic work at
N=8192 for all sixteen columns, with one reusable double LU. Read
`dembele/certificates/compiled-precision-refinement.md`, then
`dembele/pari/79_acb_refinement.py` and `dembele/pari/cm_acb.{py,c}`.

**Do not confuse finite-system precision with differential accuracy.**
All sixteen columns at N=4096 and 8192 converge below 4e-41 after two
corrections. At N=8192, however, the independent 275-side residual is
1.42e-9 and the changed/larger quadrature defect is 5.86e-12. These are
empirical infinity-norm diagnostics, not certified error bounds. The
normalized jets change by 5.13e-4 between these truncations. There is still
no exact algebraic curve model, Jacobian torsion, or Dembélé field polynomial.

**Saved local work:**

- `dembele/data/computed/acb_refinement_{64,4096,8192}.{json,out,acb}`.
  The N=8192 job finished successfully in 246 seconds on four native column
  workers. Nothing from these runs remains active. Each report records
  input hashes, convergence, independent audits, and timings.
- `acb_gauge_comparison.json` checks native checkpoint serialization and
  compares normalized jets against older double banks: relative differences
  6.72e-12 at N=8192 and 4.85e-10 against N=10240. These are empirical
  comparisons, not coefficient error bounds.
- `.acb` saves the numerical iterates using FLINT's exact serialization,
  preserving their arbitrary precision. It is not a double NPZ. Load with
  `Backend(50).read(path, 8192, 16)` from `cm_acb`, with mpmath set to 70
  digits before converting to mpmath. The report already includes normalized
  first-64 jets when all sixteen columns were solved.
- Native builds live in ignored `dembele/pari/.build/`; the wrapper builds
  using a C compiler plus `pkg-config flint`. Local Sage selects FLINT 3.1.0,
  despite a separate Homebrew 3.6.0 install. Eight new backend tests and the
  existing 34 pass; Python compilation and diff whitespace checks pass.
- The existing local N=10240 and remote N=12288 double banks are preserved.
  The new N=8192 native checkpoint is not automatically the best analytic
  approximation just because it uses arbitrary precision.

**Next concrete work:** run N=12288 using script 79, compare normalized jets
against N=8192 and the completed Châtelet double result, and continue
independent truncation/quadrature and side checks before recognition. For
example, choose a new output stem and run locally:

```sh
OPENBLAS_NUM_THREADS=4 sage -python dembele/pari/79_acb_refinement.py \
  --n 12288 --columns 16 --threads 4 \
  --comparison dembele/data/computed/acb_refinement_8192.json \
  --output dembele/data/computed/acb_refinement_12288.json
```

Each native worker owns its own FFT plan and scratch storage. The current
method still uses O(mN) polynomial evaluation and dense O(N^3) double LU.
There are 40 guard bits beyond the requested 50 decimal digits; replay at
70 digits does not improve the roughly 57-digit source geometry. Rigorous
geometric/truncation bounds, multiple centers, and faster structured methods
remain open; no validated coefficient recognition was attempted.

**Remote state is unchanged:** Châtelet's D47 N=12288 double job completed
earlier in `two_canonical_d46_20260915`. Its full artifacts have not been
fetched locally. No new remote run was launched or deployed in D49.
Use the status/fetch commands and isolation rules in the historical D48
handoff below. The working tree preserves the prior intentional D41–D48
changes plus D49; no commit, push, reset, or cleanup was made.

## Previous resumption instructions — D48 session close, 2026-09-15

**User's latest clarification:** "Châtelet completed successfully" means
only that the N=12288 **double-precision numerical job** finished and passed
its audits. It did not compute exact curve equations, a high-precision
full-size basis, Jacobian torsion, or Dembélé's field. The N=64 arbitrary-
precision refinement experiment ran **locally**, separately. Keep these
results distinct when reporting progress.

**Immediate objective:** implement and validate scalable arbitrary-precision
residual evaluation for the genus-16 differential problem, using the
existing double LU as an approximate correction solver. The genus-64 cover
and target field remain downstream. There is no exact algebraic curve model.

Read in order:

1. `dembele/certificates/newton-and-hyperelliptic-ansatz.md` — current
   experiments, limits, and evidence against the hyperelliptic ansatz.
2. `dembele/pari/78_mixed_precision_refinement.py` — working small reference
   implementation; `cauchy_apply` retains arbitrary precision throughout.
3. `dembele/pari/68_cm_differentials.py` — current full-size double solver
   and high-precision geometry replay (`as_numpy=False` preserves precision).
4. `dembele/certificates/canonical-gauge.md` — normalization and exact
   quadratic-generation result; `hyperellipticity-audit.md` for the exact
   graph obstruction and the conflict with the published theorem.

Concrete next work:

- Implement a compiled high-precision operator action (Horner/FFT or a
  justified alternative), checking it against script 78 at small sizes.
  Local FLINT headers/libraries are under `/opt/homebrew/include/flint`
  and `/opt/homebrew/lib`; remote availability has not been checked.
- Retain/reuse LU factors, evaluate residuals and accumulate corrections
  at arbitrary precision; test convergence and cost before full-size runs.
- Independently increase truncation/quadrature and test unused side
  transformations. A small linear residual alone is not a basis error bound.
  Geometry currently has about 57 decimal digits. Multiple centers remain
  an option if single-center truncation becomes too expensive.
- Only then attempt validated coefficient/field recognition. Neither
  reality of coefficients nor numerical relations establish equations over F.

Artifact locations and remote state:

- Latest **local full-size** basis: `dembele/data/computed/cm_differentials_10240_refined.npz`.
- Latest **remote full-size** basis:
  `two_canonical_d46_20260915/dembele/data/computed/cm_differentials_12288_chatelet.npz`.
  Remote runner finished 2026-09-15 15:35:40 UTC, exit 0. That job is no
  longer running. Its full results have **not been downloaded locally**.
- Local script 77/78 outputs: `hyperelliptic_reconstruction.{json,out}` and
  `mixed_precision_refinement.{json,out}` under `dembele/data/computed/`.
- Remote scripts are a hash-verified D47 snapshot, preceding the local
  script 68 precision-return change and scripts 77–78. They do not update
  automatically when local sources change. Deploy new work into a new
  isolated directory; preserve the completed run and older remote banks.

```sh
python3 dembele/jobs/canonical/chatelet.py status
python3 dembele/jobs/canonical/chatelet.py fetch --output /private/tmp/canonical-results.tgz
```

Fetch requires a new output filename. Extract into a new directory so that
remote `canonical_gauge.*` does not overwrite local comparison data. Read
`dembele/jobs/canonical/README.md` and `remote_magma/CHATELET.md` before any
new launch (API timeout is inherited as a CPU limit). Credentials stay in
the ignored `.env`; do not print, upload, or commit them.

Last verification: 34 repository tests passed, Python compilation and
`git diff --check` passed, script 77's two positive controls and script 78's
refinement/matrix-action controls passed, and script 68's default double
node/operator path passed after its interface change. This closing update
changes documentation only. No background computation was started here.

Working tree contains intentional, uncommitted D41–D48 changes and many
new scripts/data files. They are saved on disk for the next local session;
no commit or push was made. Do not reset/clean the worktree or discard
failed-pilot artifacts, which document why earlier numerical methods failed.

## STATE 2026-09-15 — D48: refinement prototype; hyperelliptic ansatz fails

Read `dembele/certificates/newton-and-hyperelliptic-ansatz.md`. Script 78
tests mixed-precision refinement on the actual N=64 Cauchy operator:
high-precision matrix-free residuals plus double LU corrections give
2e-14 -> 5e-28 -> 1e-41 -> 1e-49. This validates the linear mechanism,
NOT a differential basis at N=64. Next: compiled full-size residual
evaluation, reusable LU, high-precision accumulation and truncation checks.
Script 68 optionally returns unrounded nodes with `as_numpy=False`.

Script 77 tries x=H15/H14, h=H14/x^14 in the ordinary jet basis. Target
fails coefficient 16 by ~745.59 at N=8192 and 10240; known hyperelliptic
controls including changed chart/basis pass. No model or hyperelliptic
assumption adopted. Graph obstruction remains supported.

Châtelet D47's double-precision numerical job finished and passed its audits:
275-side residual 4.01e-14, quadric
coefficient relative change 5.60e-12 against N=10240. Full artifacts remain
in `two_canonical_d46_20260915`; use the existing fetch client.

## Remote setup 2026-09-15 — Châtelet canonical job

User requested deployment to Châtelet. Runner and deployment/status/fetch
client are in `dembele/jobs/canonical/`; read its README. Launched in
`two_canonical_d46_20260915`, N=12288 seeded from local N=10240, four BLAS
threads, followed by all D46 audits and normalization. This is the existing
double-precision solver; arbitrary-precision linear algebra remains
unimplemented. Archive and all eleven input hashes verified before launch.
Other remote jobs/data are preserved. Check status for the current outcome.

## STATE 2026-09-15 — D46: quadrics suffice; fixed real CM normalization

**Read `dembele/certificates/canonical-gauge.md`.** Continued the general
canonical route, with two useful advances:

- **Exact:** script 76 gives connected, disjoint branch sets for a
  seven-vertex minor with minimum degree four. Hence treewidth and metric
  gonality are at least four; Baker specialization excludes trigonality.
  Petri now proves the canonical ideal is generated by 91 quadrics.
  Sections of 2K have degree 60, so local coefficients 0 through 60 suffice
  to determine the quadratic relations when known exactly.
- **Numerical:** script 74 jet-normalizes the basis (first 16 coefficients
  are I), then sets alpha=3*a_(16,15), v=alpha*u,
  G_i(v)=alpha^i H_i(v/alpha). This cancels arbitrary basis choices and
  common coordinate/CM period scale. A separate invariance control passes.
  The resulting coefficients are real to relative 1.86e-11. This does not
  prove that their field is F or make floating-point values exact.

Best differential basis is now `cm_differentials_10240_refined.npz`.
Script 68 accepts shorter initial bases by zero padding. N=10240/20480
samples with 50-digit geometry replay took ~87 seconds; linear algebra
and FFT are still double precision. Compared to N=8192, normalized jets
agree to relative 4.87e-10; quadric coefficients to 1.15e-10 (largest
absolute difference 1.95e-8). The pivot matrix has condition ~7.17e4.
Equation residuals can be much smaller than coefficient errors.
Independent script 70 audit (`differential_audit_10240.*`): all 275 side
actions checked, maximum relative residual 7.18e-13; product rank 45,
linear-times-quadric rank 741, degree-three quotient dimension 75.
All 34 repository tests, Python compilation, and diff whitespace checks pass.

`canonical_gauge.npz` stores the real 136-by-91 quadric array and its
explicit monomial/pivot/free index lists. Coefficients have magnitude at
most ~152. Both first-61 and first-256 product tests give rank 45.
Six small-height recognition trials (script 75) found no candidates:
rational denominator<=1000, or F-basis relation height<=4. This is only
a bounded pilot. No exact coefficient/model was accepted.

New scripts `pari/74_canonical_gauge.py`, `75_gauge_recognition.py`,
`76_quadric_generation.py`; outputs `canonical_gauge.*`,
`gauge_recognition.*`, `quadric_generation.*` under data/computed.
**Next:** substantially higher-precision jets, likely a structured or
multi-center arbitrary-precision solver, then validated arithmetic
recognition. The 61-jet bound limits recognition data, not the length of
the global expansion needed to compute those jets accurately. No model,
torsion, field polynomial, external messages, or commits. Ledgers updated.

## STATE 2026-09-15 — D45: exact nonhyperellipticity obstruction

**Read `dembele/certificates/hyperellipticity-audit.md`.** User asked to
determine whether the genus-16 curve is hyperelliptic. We now have an
exact computational argument that it is **not**; D44's numerical
discrepancy is resolved in favor of nonhyperellipticity.

1. Transcribed Figure 2 and enumerated all graph automorphisms independently
   with Sage and NetworkX VF2: same 64 permutations, exactly 19 involutions.
   Their quotient genera are 8 (5),10 (4),12 (6),14 (4). None is a tree.
2. Recomputed the 58-class norm-2 Brandt matrix from HMF. Final run uses
   unconditional Minkowski class-group proof bounds; ordinary/narrow h=1;
   exact mass 1455/32=zeta_F(-1)/128 with zeta_F(-1)=5820. ~27 CPU seconds.
3. Every nonzero off-diagonal pair has min(Tij,Tji)=1, determining one edge
   orbit and weight e_j/Tij=e_i/Tji. Nine diagonal entries are 1 and give
   folded pendant intervals. The 58-vertex/73-edge core stabilizes to
   30 vertices/45 edges, with an explicit weight-preserving isomorphism to
   Figure 2. Thus the result does not rely merely on a drawing.
4. Baker specialization and Chan's metric-graph criterion imply a
   hyperelliptic curve would give a tree-quotient involution. This works
   in residue characteristic 2; every metric involution is among the
   enumerated graph automorphisms. Exact obstruction, no numerical tail
   estimates or GRH needed. Not proof-assistant formalized.

Scripts: `pari/71_stable_graph.sage.py`, `magma/72_stable_graph_brandt.m`,
`pari/73_brandt_graph_check.py` under `dembele/`. JSON and passing logs:
`stable_graph_audit.*`, `stable_graph_brandt.*`, `brandt_graph_check.*`.
The first includes all involutions; the last includes graph stabilization
history and the isomorphism. Source PDF downloaded only to
`/private/tmp/dembele-genus16.pdf`; reproduction needs the transcribed
edge list already in script 71, not that temporary PDF.

**Mathematical consequence:** pursue general canonical equations. D44's
16 differentials/91 numerical quadrics remain useful. Theorem 5.9 of the
paper conflicts with this graph obstruction; the upstairs/coarse-coordinate
issue is described precisely in the certificate. Do not automatically
discard separate F16 induced-character claims or infer an actual curve
automorphism from a graph symmetry. No external messages or commits.

**Additional audit finding:** the raw norm-2 matrix obeys
e_i*Tij=e_j*Tji, contradicting the reverse identity stated in the helper
documentation. First script 72 attempt failed on the documented identity;
the corrected direct check and export pass. No older pairing-dependent
certificate was silently rewritten; audit those separately before reuse.

DECISIONS, REFERENCES and CLAUDE updated. The previous D44 section below
is historical; its "unresolved" verdict is superseded by this entry.

## STATE 2026-09-15 — D44: numerical differentials and canonical quadrics

**Read `dembele/certificates/genus16-differentials.md` first.** We followed
the user's request to tackle the genus-16 base before equations for Y64.
There is substantial numerical progress and an unexpected structural
discrepancy that must not be hidden.

- CM-centered expansion: omega=w^31 H(w^32)dw. The reconstructed sector
  reaches radius 0.9999083389704847; use R=0.99991. Smaller R=0.9998 gave
  spurious kernel directions because it did not cover the quotient.
- N=4096 isolates exactly 16 small singular values, with gap 0.13305 vs
  6.629e-7. N=8192 gives the best basis after 50-digit geometry replay
  and stabilized linear refinement. Independent 275-side checks give
  maximum relative residual 3.168e-10; operator defect 4.509e-12.
- Products have numerical rank **45** (singular gap 0.47078 vs 3.601e-12),
  yielding **91 quadrics**. Unused product coefficients verify them to
  relative 1.438e-12. Their linear multiples have rank 741, leaving the
  expected canonical degree-3 dimension 75. These are complex numerical
  relations, not equations over F and not reducible modulo 97 yet.
- A hyperelliptic genus 16 curve would give product rank 31. The opening
  step of Dembélé's Theorem 5.9 appears to confuse upstairs t with quotient
  u=t²: invariant t h(t²)dt descends to h(u)du/2, which can vanish to odd
  order. See certificate for careful scope. Do not claim a certified
  counterexample; independently audit the identification and numerics.
  Proposition 6.5/second proof of Theorem 6.4 is a separate induced-character
  argument, so this does not automatically reopen the F16 detour.

Scripts: `dembele/pari/67_expansion_geometry.gp`, `68_cm_differentials.py`,
`69_cm_sector.py`, `70_differential_audit.py`. Reproduce via pari/README.md.
Best artifacts: `cm_differentials_8192_refined.{json,npz,out}` and
`differential_audit.{json,npz,out}` in `dembele/data/computed/`.
The `8192_mp` single-vector eigensolver missed repeated eigendirections;
`8192_block` power iteration diverged because A has eigenvalues outside
the unit circle. Both are failed pilots, not valid bases. No active jobs
are needed to continue from these artifacts.

**Next:** audit the hyperellipticity discrepancy independently, then raise
precision and normalize the general canonical relations arithmetically
(Hecke eigenforms/CM periods are a possible route). Do not force a
hyperelliptic reconstruction. The Y64 integral comparison and torsion
steps remain open. No target polynomial, algebraic model, external
messages, or commits. DECISIONS and REFERENCES updated; 34 unit tests pass.

## STATE 2026-09-15 — D43: domain and genus-64 local cover computed

**Read `dembele/certificates/genus64-cover.md`.** The next D42 geometric
gate passed. Rickards's current PARI code computes the **genus-16 normalizer
quotient directly**, using D=(b-b²,-1)/F from Dembélé's paper. The 277-sided
domain has the expected signature (16;2^17,3^9,32), passes `afuchcheck`,
and took 257.443 wall seconds. Saved as
`dembele/data/computed/normalizer_domain.bin` (PARI 2.17.1).

**The proposed genus-64 cover now has explicit local monodromy.** Script 66
reduces the actual quaternion order: O/2 has radical dimension 30 and residue
field F4. Normalize g by i^(-valuation_p(nrd(g))) to obtain its S3 permutation.
All 27 presentation relations and product checks pass; image is all S3.
The reflection inverse-image subgroup has signature (64;2^17,16,32).
Lifted rational homology independently gives **b1=128**, with boundary ranks
2 and 44. The degree-six kernel cover has genus 136. Coset representatives
for Y are identity and side generators **2 and 8**, exported with all side
images in `genus64_cosets.gp`.

Run `python3 dembele/pari/run_fdom.py cover` to replay in ~2 seconds.
Build details, pinned upstream SHA, PARI compatibility patch and bounded
runner: `dembele/pari/README.md`. Upstream is in ignored `dembele/vendor/`.
Magma independently confirms discriminant 2 and X's genus-40 signature via
`dembele/magma/65_explicit_quaternion.m`. Numeric polygon checks are not an
interval proof; the residue, relation and homology calculations are exact.

**Next gate:** compute and algebraically recognize differentials and section
multiplication/evaluation data on Y (or the genus-16 base and exact cover).
The known three-sheet representation allows vector-valued forms on the parent
domain. Its maximum disk vertex radius is 0.9997819873: a single global
Taylor series has slow geometric decay (r^N<10^-30 at N=316817). This is not
a truncation bound or a universal impossibility claim. Investigate multiple
centers or a sparse CM-centered expansion. The unique order-32 base point
has two F-rational points above it, distinguished by ramification indices.
No algebraic equations, torsion points or field polynomial yet. The precise
local-type/JL and integral target comparison still needs formalization.

## STATE 2026-09-14 — D42 review supersedes the route verdicts below

**Read `dembele/certificates/review-2026-09-14.md`.** Dembélé's 2020 genus-16
Shimura-curve paper, Theorem 6.4, proves the D40 branch is the **solvable
Harbater field**. No further T127 image test is needed. The old SL2(F16)
claims below and in script 60's preserved output are invalid.

**New route to the original F256 target:** construct the p²-level curve,
then use divisor/Jacobian arithmetic and odd-prime torsion lifting. This
bypasses the specific toric/theta pipeline closed by D39. A proposed
Atkin–Lehner quotient has genus **64 = 16 + 48**, down from 136; its canonical
model, cover monodromy and integral target constituent still need verification.
There is no curve equation or target polynomial yet.

Script `64_curve_first_frobenius.m` **passes**: genus/branching consistency,
target Euler factors coprime to cofactors in the proposed genus-64 T31
polynomial, and Frobenius orders 257/255 at 31, **51/257 at 97**. The order-51
choice suggests computing torsion over F_(97^51), then 257 projective lines.
The full Euler cofactor check at 97 is not yet banked.

Script `63_p2_sign_type_probe.m` **passes** a new all-Hecke comparison's
finite calculation (64.630 CPU s): the
GL2(F2) sign lattice reduces into the trivial level-one module on **48** of
its 58 classes. The ten-dimensional quotient has T31 polynomial **t^10**,
so both target constituents lie in the supported submodule; its polynomial
matches the p²-new bank mod 2. The package uses row functions; the failed
column attempt is preserved separately. The local-type/JL and geometric
quotient-lattice arguments must still be written precisely.

Next geometric gate: verify the lifted involution/level cover; benchmark
Rickards's maintained PARI fundamental-domain code on X40, then obtain
algebraic curve or Makdisi data. Baït–Page (ANTS 2026) accelerates cohomology
*after* a polygon is available. No external messages were sent. The review
also withdraws unsupported ramification/height estimates in
`target-height-estimate.md`. Historical entries below are retained for audit.

## STATE 2026-09-14 — D41 correction, read this first

**D40's nonsolvability verdict is withdrawn.** The detached script 60 completed,
but its anti-dihedral fallback checked factors 3 and 5 instead of **17**.
Independent `dembele/magma/62_f16_dihedral_audit.m` passes and computes the sole
quadratic survivor M/F: degree 16 over Q, discriminant 2^79, signature (0,8),
class group **C17 (GRH)**. Dihedrality remains possible. Full details and the
completed T97 block: `dembele/certificates/f16-dihedral-audit.md`.

T97 gives trace zero for both tested classes, with one survivor each. The
old two VERDICT lines are invalid; original output preserved. Script 60's
fallback is repaired; use script 62 to replay the independent check quickly.
**Next:** T127 on the quartic carriers can falsify the dihedral candidate
(any nonzero residual trace does); zero would be inconclusive. Candidate
cycle types at 31/97/127/191 are 17 / 1 2^8 / 1 2^8 / 1 2^8. Do not start
the period pipeline assuming a nonsolvable target. Full eigensystem counts
and C8 action are also unproved; no polynomial was constructed this session.


## STATE 2026-09-08 (evening) — NEW TARGET, read this first

**D40 / `dembele/certificates/review-2026-09-08.md`.** The comprehensive review found
the object every closed route was missing, sitting in D36's own output: the **level-`𝔭`
Steinberg newforms over `F` have residue field `F₁₆`**, and each such mod-2 system is an
**`SL₂(F₁₆)`-representation of `G_F` unramified outside `𝔭`** — a second nonsolvable
extension of `Q` ramified only at 2 (expected group `SL₂(16)² ⋊ C₈`), carried by
**4-dimensional** abelian varieties with **split multiplicative reduction at the norm-2
prime** (`a_𝔭 = +1`, Hecke fields `Q(ζ₁₅)⁺` and the conductor-95 cyclic quartic, 2
inert). Period valuations `20–458` (vs `10⁴` at level 31), 174 tree positions, 17
neighbours (the validated genus-4 back end), Fuchsian signature `⟨40; 3¹⁸, 16⟩`.
Nothing lower in the tower (`Q(ζ₁₆)⁺` to `𝔭¹⁰`, `Q(√2)` to `𝔭¹⁴`: all traces in `F₂`).
**FIRST ACTION NEXT SESSION:** read the tail of `dembele/data/computed/f16_steinberg.out`
(job left running detached at close, PID 87628; expected to finish within the hour) and
copy the `T_97` block — `dihedral survivors` per class and the two `VERDICT` lines — into
`review-2026-09-08.md` §2.5 and D40; if a survivor remains, the class-number fallback
line decides it. Then: Phase 1 = write the field up + Frobenius cycle-type table (31: 17-cycle; add
97, 127, 191 — each `T_ℓ` at level `𝔭` is a same-session build, 5 min–4 h); Phase 2 = the
CD-at-`𝔭` pipeline at dimension 4 (review §4). Scripts: `60_f16_steinberg.m` (replayable;
its T_97 tail is the anti-dihedral certificate), `61_fuchsian_p2_probe.m`. Magma gotcha:
`InternalNeighbors` asserts (`ideals.m:237`) on the *conjugate* primes `τ^i(𝔭₃₁)` at
level `𝔭` — use `𝔭₃₁`, `𝔭₉₇`, … themselves, and Galois-conjugation arguments for the rest.

## STATE 2026-09-08 — read this first

**D39: the supercuspidal `𝔭^k` family is computed and closed as a route
(`dembele/certificates/levelraise-p2k.md`).** Level raising at the prime above
2 DOES happen for k ≥ 2: new multiplicity per residual system 0, 1, 2, 4 at
`𝔭¹..𝔭⁴`, carried by rational Hecke orbits of degree **48** (`𝔭²`, the whole
new space, depth-zero supercuspidal), **64, 72** (`𝔭³`), and at `𝔭⁴` only
`Q(ζ₃₂)/F`-twists of level 1 and of those (twist-minimal remainder 0,
verified). Why it is not a path: supercuspidal at `𝔭` ⇒ `A_g` has potentially
good *supersingular* reduction at `𝔭` (no toric part), the carrying Shimura
curve (level `1+𝔭_D`, genus 136) is a Drinfeld-`Σ¹` quotient with genus-1
reduction components — no Mumford curve, no CD periods — and D38's locality
objection stands; `d_g = 48` besides. Scripts `58_levelraise_p2k.m` (sweep;
`T_97` confirmation at k = 2 done, certificate §4) and
`59_p2k_twist_check.m` (replayable from the banked charpolys
`levelraise_p2k_charpolys.m` with `BANK_IN=1`). Sparse `T_31` builds are
~330 s at every level `𝔭^k` (flat), `T_97` ~25× that.

**What remains for the goal (unchanged in kind):** (i) the auxiliary-prime
lottery on chatelet (`~10⁻³`; 08-27 instructions), (iii) hole (2) — an
algebraic invariant of `K_Dembélé` computable without a `d_g`-dimensional
variety; no candidate. Item (ii) of the 09-04 list is done. Belyi side still
parked (next experiment there: `lemma-B-cyclic.md` §4.6).

## STATE 2026-09-04 — read this first

**Lemma B corrected (D37).** "`J[2]` indecomposable" is **false**: `Q_{2^m}`, `m ≥ 4`,
gives `J[2] = A ⊕ B`, `A ≇ B` (`Q_16, Q_32, Q_64` verified three ways). The property the
2008/2008 scans tested is **multiplicity-free** (`max_multiplicity == 1`), which is what
the solvability argument needs; all writeups + CLAUDE.md now say so. Census `|G| ≤ 64`
(`lemmaB/census_top.sage`, 707 triples): formula `dim M_G = 2 + d(M(G)) − r` exact
everywhere, `r = rank(res: H²(G,F_2) → ⊕_b H²(⟨σ_b⟩,F_2))`; decomposable only for
quaternion; `End/rad = F_2` except `Q_8` (`F_4`). Details: `writeup/lemma-B-cyclic.md` §4.
Belyi side is **parked** here by user decision; if resumed, the next experiment is
whether summand socles are always spanned by distinct fibre classes (§4.6).

**Dembélé goal — hole (1) answered (D38, `lambda-torsion-localization.md`):** `λ`-torsion
DOES localize in the CD uniformization — as a *local* Galois module at `q₀`, determined by
the banked 2-adic block plus 64 period values mod squares — but this is local data and the
torsion points' uniformization coordinates are transcendental; reaching the global field
needs algebraic functions on the full `d_g`-dimensional `B_g`. So D32 option (b) is closed
and hole (1) collapses into hole (2). **The CD arc now has no conceptual door left.** What
remains for the goal: (i) the auxiliary-prime lottery (resume 3 lanes on chatelet; path
probability `~10⁻³`; instructions in the 08-27 section), (ii) the untested supercuspidal
conductor-`𝔭^k` family at the prime above 2 (D36) — a real computation and it inherits a
`d_g` question, (iii) hole (2): an algebraic invariant of `K_Dembélé` computable without a
`d_g`-dimensional variety — no candidate; this is the 2026-08-04 front-end problem
restated. Free consistency check for any future `q₀` run: the Kummer class must be
unramified (even monodromy-pairing valuations on the `f1`-new block).

## STATE 2026-09-01 (second session)

**Lemma B is proved for cyclic 2-groups** (`writeup/lemma-B-cyclic.md`, D35).
Method: coinvariants of the relation module via Hopf's formula; general formula
`dim H_1(X,F_2)_G = 2 + d(M(G)) − r` with `r ≤ 3` the rank of the three puncture
classes. Checks in `lemmaB/`. Dembélé front end unchanged (no candidate; see
below). **Next:** (1) `d(M(G)) = 0` groups (`Q_{2^m}`, `SD_{2^m}`) — show `r ≥ 1`;
(2) tabulate `r` vs `d(M(G))` across the census to isolate the genuinely glued
cases; (3) optional Lean formalization of the proposition (Hopf + Nakayama).

**Dembélé front end — the norm-2 door is now CLOSED (D36, 2026-09-02).** Level
raising at the prime `𝔭 | 2` (conductor `𝔭¹`, Steinberg) was tested directly
(`57_levelraise_p2.m`, `dembele/data/computed/levelraise_p2.out`): on the
level-`𝔭` space (cuspidal dim **154**, raw 155) the residual invariant has
multiplicity **2 = oldform baseline** at BOTH 31 and 97 (excess 0), so the
`𝔭`-new part (dim 40) carries no copy of `f`'s residual system; that new part is
residue-field **F₁₆** (`cp mod 2 = (t⁴+t+1)⁵(t⁴+t³+t²+t+1)⁵`), not F₂₅₆. Reason:
Steinberg raising at `𝔭` needs `ā_𝔭 = 1`, but `ā_𝔭 = ω` (cube root of 1). NB the
script's confirmatory joint-lattice tail hit a matrix-coercion bug (fixed 09-02,
`MA!` coercion) AFTER both verdict lines printed; the answer rests on the two
multiplicity lines, not that block — no rerun needed. Only conductor `𝔭^k`, k≥2
(supercuspidal) remains untested on this door — larger, murkier, not an
afternoon. The two paper-math holes that survive the whole arc (independent of
the auxiliary prime): **(1)** does `λ`-torsion localize in the CD uniformization
(→ `d_g > 16` stops mattering, D32 option b); **(2)** recognize a smaller-height
invariant than the deg-257 polynomial (→ attacks `M_rec ~ 10⁴`, D33). Original
note below, superseded.

**[SUPERSEDED] level raising at the prime `𝔭` above 2 itself.**
The gate-1 scan started at norm 31 (its congruence assumed odd norm) and never
considered `𝔭`. Facts: the algebra ramified at `𝔭` + 7 real places is admissible,
so a Gal(F/Q)-stable Shimura curve `X_𝔭` of discriminant `𝔭`, level 1 exists;
its 𝔭-adic CD uniformization uses our definite disc-1 order on the 3-regular
tree (residue field F₂); positions ~174, lattice ~58-dim, so every q0-route
cost drops by 3–6 orders of magnitude and the D34 one-pass lift applies as is.
Obstacle: Ribet's criterion at `𝔭` would need `ā_𝔭 = 1`, but
`11_hecke_fingerprints.m` gives charpoly `(t²+t+1)^8` for `T_𝔭` mod 2 on the
16-block, i.e. `ā_𝔭 = ω`; the criterion is not a theorem at `𝔭 | 2` with
`e = 8`, so the question is a Serre-weight/multiplicity one at `𝔭`. **Decisive
cheap test:** level-`𝔭` Brandt module (~174-dim), `T_31` on it, check whether
the two degree-8 mod-2 factors divide the charpoly of the `𝔭`-new part. Hours
locally. If it fails at level `𝔭`, conductor `𝔭^k` (supercuspidal at `𝔭`) is
the same family with level structure. Second-tier: extend the 2-power-level
scan over `Q(ζ₁₆)⁺` past LMFDB's range for a residue-field-F₁₆ hit (check
Moon–Taguchi-type nonexistence first).

## STATE 2026-09-01 (first session close)

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
