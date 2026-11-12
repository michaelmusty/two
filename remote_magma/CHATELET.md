# Running Magma remotely on chatelet

This repository can run Magma jobs on `chatelet.mit.edu`, an on-prem CoCalc
instance, through its HTTP API. There is no SSH or interactive remote shell.
The local client is `remote_magma/cocalc.py`.

The setup is adapted from the
[IGP24 chatelet instructions](https://github.com/nt-lib/IGP24/blob/main/ideas/belyi/verify/CHATELET.md).

## Remote environment

- Magma: `/usr/local/bin/magma`, V2.29-10 (verified 2026-10-05).
- Capacity: 24 cores and approximately 94 GB RAM.
- Current project policy allows at most three mathematical workers globally,
  including the active local D133 workers. Reserve capacity before starting
  a remote job.
- `/tmp` is shared by all CoCalc projects on the host. Use the project-local
  `two_remote_magma` directory instead.

## Credentials and TLS

The gitignored repository-root `.env` must contain:

```text
COCALC_ACCOUNT_API_KEY=sk_...
COCALC_PROJECT_ID=<uuid>
COCALC_BASE=https://chatelet.mit.edu
```

The key must be account-level; CoCalc project keys cannot execute commands.
The client sends it only as the HTTP Basic username and never prints it.

Chatelet omits the intermediate certificates from its served certificate
chain. `remote_magma/ca_extra.pem` supplies YR1, YR2 and cross-signed Root YR,
loaded in addition to the normal Python or `certifi` trust store. Certificate
validation and hostname checks remain enabled.

On 2026-10-05 the server presented a certificate issued by YR1, valid from
2026-09-29 through 2026-12-28. The previous bundle contained YR2, so Python
failed with `unable to get local issuer certificate`. YR1 was downloaded
over verified HTTPS from the official [Let's Encrypt certificate catalogue](https://letsencrypt.org/certificates/)
at [int-yr1.pem](https://letsencrypt.org/certs/gen-y/int-yr1.pem), then checked
as an untrusted intermediate against the existing trusted roots before
being added. Its DER SHA-256 fingerprint is:

```text
13:94:96:34:D9:9C:D6:FD:6A:A8:0B:C0:34:FE:FA:CC:EB:19:69:FE:EF:98:65:86:71:3E:CD:BB:05:75:8D:3F
```

If issuance changes again, obtain the needed intermediate from that
catalogue and verify its chain. Keep TLS and hostname verification enabled.

### Verified access and credential replacement

The user installed a fresh account key on 2026-10-05. Authentication and
the Magma V2.29-10 version check pass. The checked-in smoke test passes
through file upload/execution/cleanup; inline checks of the degree-eight
base field, its defining equation and GF(256) also pass. See the
[remote test record](../dembele/checkpoints/magma-access-2026-10-05-remote-restored.json).
The two tests took 2.480 and 0.486 seconds. D133's coordinator was held
while existing workers drained, then resumed after 4.897 seconds, preserving
the global worker limit.

The earlier configured key and explicitly authorized backup-key test both
returned HTTP 400 with `No account found. Is your API key wrong?`; the
[backup-key check](../dembele/checkpoints/magma-backup-key-check-2026-10-05.json)
records that resolved authentication outage. If this error recurs, create
a fresh account key on `chatelet.mit.edu` in Account settings, under API Keys
and Add API key; see the [CoCalc account-key instructions](https://doc.cocalc.com/apikeys.html#account-api-keys).
Run the helper below in your own interactive Terminal, enter the key at
the hidden prompt, then rerun the smoke test:

```sh
python3 remote_magma/set_key.py
```

Do not paste credentials into logs or documentation. Existing project
settings are preserved by the helper.

## Running jobs

Run short inline Magma:

```sh
python3 remote_magma/cocalc.py eval 'print 6*7;'
```

Upload, verify, execute, and remove one Magma source file:

```sh
python3 remote_magma/cocalc.py --timeout 3600 run path/to/job.m
```

Use repeatable `--remote-env KEY=VALUE` options for package paths and parallel lane
parameters:

```sh
python3 remote_magma/cocalc.py --timeout 3600 \
  --remote-env HMF_ROOT=two_hilbertmodularforms \
  --remote-env ORBIT_INDEX=1 run path/to/job.m
```

Run a diagnostic shell command:

```sh
python3 remote_magma/cocalc.py exec 'command -v /usr/local/bin/magma'
```

The file runner base64-encodes the source, uploads it in chunks of at most
64 KB, verifies the remote byte count, and cleans up its uniquely named
temporary files. Magma reads the uploaded source from closed stdin so the
batch process exits reliably.

The reusable Python API is:

```python
from remote_magma.cocalc import env, rexec, run_magma_file, run_magma_text
```

`rexec(conf, command, ...)` returns a dictionary containing `stdout`,
`stderr`, and `exit_code`.

## Critical timeout behavior

CoCalc's `project_exec` `timeout` is also applied to the command and all its
children as `RLIMIT_CPU`. A detached process inherits this limit. Jobs that
need more than the default 120 CPU-seconds must receive a larger value.

For a long detached job, use a one-day CPU limit and a separate short socket
timeout:

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

The launcher shell exits immediately, but its HTTP response can occasionally
be lost. A socket timeout on a detached launch is therefore not proof that
the job failed. Write results to a remote file and poll that file or a
completion marker with separate `rexec` calls.

## Operational guidance

- Start a fresh Magma process for each slice of a large computation. Long
  processes making many `GaloisGroup` calls can accumulate memory.
- Wrap independent Magma inputs in `try ... catch` so one failure does not
  discard the rest of a slice.
- Treat synchronous API output as reliable for short jobs only. Long jobs
  should write remote output and be polled.
- Avoid shared `/tmp`; namespace all remote files under
  `two_remote_magma`.
- Increase `--timeout` according to CPU time, not merely expected wall time.

## Smoke test

The checked-in smoke test should print `REMOTE_MAGMA_OK` and `42`:

```sh
python3 remote_magma/cocalc.py --timeout 30 run \
  remote_magma/smoke_test.m
```
