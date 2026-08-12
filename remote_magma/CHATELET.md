# Running Magma remotely on chatelet

This repository can run Magma jobs on `chatelet.mit.edu`, an on-prem CoCalc
instance, through its HTTP API. There is no SSH or interactive remote shell.
The local client is `remote_magma/cocalc.py`.

The setup is adapted from the
[IGP24 chatelet instructions](https://github.com/nt-lib/IGP24/blob/main/ideas/belyi/verify/CHATELET.md).

## Remote environment

- Magma: `/usr/local/bin/magma`, V2.29-8.
- Capacity: 24 cores and approximately 94 GB RAM.
- Eight parallel Magma lanes are reasonable for small jobs.
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

Chatelet omits a Let's Encrypt intermediate from its served certificate
chain. `remote_magma/ca_extra.pem` supplies the missing certificates and is
loaded in addition to the normal Python or `certifi` trust store.

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
