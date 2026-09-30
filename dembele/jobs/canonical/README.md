# Canonical computations on Châtelet

This packages D46's numerical solver and audits for an isolated remote run.
It does **not** implement arbitrary-precision FFT or linear algebra. The
default N=12288 run extends the local N=10240 basis and checks stability;
increasing N cannot eliminate the double-precision accuracy limit.

From the repository root:

```sh
python3 dembele/jobs/canonical/chatelet.py deploy
python3 dembele/jobs/canonical/chatelet.py status
python3 dembele/jobs/canonical/chatelet.py fetch --output /private/tmp/canonical-results.tgz
```

The default directory is `two_canonical_d46_20260915` in the existing
CoCalc project. For another run, use a new `--remote two_canonical_NAME`
on every command. Deployment refuses an existing directory. `--n` defaults
to 12288 and accepts 10240 through 16384. Four BLAS threads are used.
To inspect the upload without connecting:

```sh
python3 dembele/jobs/canonical/chatelet.py bundle --output /private/tmp/canonical-inputs.tgz
```

Only eleven explicitly listed scripts/data files are uploaded. Credentials
remain local, managed by `remote_magma/cocalc.py`. Both the archive and
individual inputs are SHA-256 checked before launch. Sage's Python supplies
NumPy, SciPy, mpmath and NetworkX; no packages are installed or upgraded.

The detached runner receives a three-day inherited CPU limit, with a
60-second API socket timeout. A lost launch response requires a status
check before any retry. A lock prevents concurrent runners in one directory.
Logs, start/finish timestamps, PID, and exit status stay in that directory.
Detachment survives client disconnection, but does not guarantee survival
of a server/project restart. A killed job may have no completion marker;
inspect its PID and logs. There is no automatic relaunch or partial-matrix
checkpointing.

Stages: exact graph-minor witness, refined differential basis, independent
275-side/product/cubic audit, fixed CM normalization, bounded recognition
pilot. The runner finishes with `CANONICAL_JOB_OK` only when the differential
audit meets the recorded rank and residual thresholds. This is numerical
validation, not certification of algebraic equations. Fetch requires the
runner's completion marker and verifies the downloaded archive checksum.
Extract into a new local directory to preserve previous artifacts.

Preflight on 2026-09-15: Sage Python provides NumPy 1.26.3, SciPy 1.11.4,
mpmath 1.3.0, NetworkX 3.2.1. Host memory was 125 GiB total, about 110 GiB
available; cgroup v2 reported no project memory cap. Plain system Python
lacked NetworkX, so the runner consistently uses `sage -python`.
