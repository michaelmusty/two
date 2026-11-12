# Magma locally and on chatelet

## Local Magma

The local installation is `/Applications/Magma/magma`, available as `magma`
on `PATH`. On Apple Silicon it requires Rosetta because the installed binary
is Intel x86-64. Install Rosetta with Apple's installer if the launcher
reports `Bad CPU type in executable`:

```sh
softwareupdate --install-rosetta
```

Check the version and run the shared smoke test:

```sh
magma --version
magma -b < remote_magma/smoke_test.m
```

On 2026-10-05, installing Rosetta restored local V2.29-8. The smoke test and
small number-field/finite-field checks passed; see the
[local test record](../dembele/checkpoints/magma-access-2026-10-05-local.json).
Magma's [platform list](https://magma.maths.usyd.edu.au/magma/download/) and
[Apple's Rosetta instructions](https://support.apple.com/en-us/102527)
describe the Intel-on-Apple-Silicon setup.

## Chatelet connection

`cocalc.py` runs Magma through the CoCalc `project_exec` API at
`chatelet.mit.edu`. It reads these values from the repository-root `.env`:

```text
COCALC_ACCOUNT_API_KEY=...
COCALC_PROJECT_ID=...
COCALC_BASE=https://chatelet.mit.edu
```

The API key is used as the HTTP Basic username and is never printed.

**Verified on 2026-10-05:** Chatelet runs Magma V2.29-10. The user's new
account key passes authentication, the checked-in file smoke test passes
through upload/execution/cleanup, and inline number-field/finite-field
checks pass. See the [remote test record](../dembele/checkpoints/magma-access-2026-10-05-remote-restored.json).
Local Magma remains V2.29-8.

The client loads `ca_extra.pem` to supply intermediates omitted by the
server. The bundle includes YR1, YR2 and cross-signed Root YR. On 2026-10-05,
adding the verified YR1 certificate repaired TLS after the server's issuer
changed. The old configured key and backup were both rejected before the
user installed a fresh key; the earlier [backup-key check](../dembele/checkpoints/magma-backup-key-check-2026-10-05.json)
is historical. For future replacement, create an account API key on
`chatelet.mit.edu` under Account settings and API Keys, following the
[CoCalc account-key instructions](https://doc.cocalc.com/apikeys.html#account-api-keys).
Run the helper in your own interactive Terminal and enter the key at its
hidden prompt:

```sh
python3 remote_magma/set_key.py
```

See [CHATELET.md](CHATELET.md) for certificate provenance and authentication
troubleshooting. Keep the current global limit of three mathematical
workers, including the active D133 production workers, when testing or
launching Magma jobs.

## Short jobs

Run inline Magma:

```sh
python3 remote_magma/cocalc.py eval 'print 6*7;'
```

Upload and run one Magma file:

```sh
python3 remote_magma/cocalc.py --timeout 3600 run path/to/job.m
```

Forward repeatable environment settings when a job depends on remote paths or lane
parameters:

```sh
python3 remote_magma/cocalc.py --timeout 3600 \
  --remote-env HMF_ROOT=two_hilbertmodularforms \
  --remote-env ORBIT_INDEX=1 run path/to/job.m
```

Run a diagnostic shell command:

```sh
python3 remote_magma/cocalc.py exec '/usr/local/bin/magma --version'
```

The file runner uploads base64 in chunks no larger than 64 KB, verifies the
byte count, and cleans up its uniquely named remote files.

## Long or detached jobs

The API's `timeout` is also the remote process's `RLIMIT_CPU`. For a detached
job, import `env` and `rexec`, launch with `timeout=86400`, and set a short
socket timeout:

```python
from remote_magma.cocalc import env, rexec

result = rexec(
    env(),
    "cd two_remote_magma && "
    "nohup /usr/local/bin/magma -b < slow.m > slow.out 2> slow.err "
    "< /dev/null & echo PID=$!",
    timeout=86400,
    sock_timeout=60,
)
```

A socket timeout during a detached launch is not proof that launch failed.
Poll a completion marker or output file through a separate `rexec` call.
Avoid shared `/tmp`; use the project-local `two_remote_magma` directory.

This setup follows
[`CHATELET.md`](https://github.com/nt-lib/IGP24/blob/main/ideas/belyi/verify/CHATELET.md).
