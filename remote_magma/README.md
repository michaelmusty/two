# Remote Magma on chatelet

`cocalc.py` runs Magma V2.29-8 through the CoCalc `project_exec` API at
`chatelet.mit.edu`. It reads these values from the repository-root `.env`:

```text
COCALC_ACCOUNT_API_KEY=...
COCALC_PROJECT_ID=...
COCALC_BASE=https://chatelet.mit.edu
```

The API key is used as the HTTP Basic username and is never printed.

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
