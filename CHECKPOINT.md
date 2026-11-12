# Transfer checkpoint — 2026-09-30

**Resumed on 2026-10-05:** the user requested continuation on the original
compatible host. Transfer integrity and all external dependency hashes
passed before production resumed from correction 10. Production and its
waiting continuation are recorded in the [resumption record](dembele/checkpoints/d133-resume-2026-10-05.json)
with durable logs; see [HANDOFF.md](HANDOFF.md) for current operational
instructions. Inspect live locks and receipts before any restart.

The checkpoint below is historical. Its inventory remains the exact
September 30 transfer baseline; resumed working-store files can now differ
or have been retired by the reviewed journal protocol. Do not overwrite
that inventory or treat it as a verifier for the advancing mutable store.
Frozen source and certificate hashes must still match.

D133 is deliberately paused after correction 9 and its receipt-verified
metadata archive, before `low_begin_010`. The working journal is
`ready009`, epoch 20, with `(u, count, bits) = (3497, 2903, 363)`.
There is no pending transaction and neither coordinator is running.
This is a resumable operational checkpoint, not a completed P6400 certificate.

The [pause record](dembele/checkpoints/d133-stop-before-010-2026-09-30.json)
authenticates the current full payloads and every row, the final sweep/archive,
and the [coordinator log](dembele/checkpoints/d133-stop-before-010-2026-09-30.log).
All 2,682 production/archive receipts pass; their driver, log and metadata
hashes were checked. Three interrupted attempt-01 logs remain intact, with
passing attempt-02 recovery receipts. The longest recorded job is 28.545 s.
All 18,589 source hashes in the frozen D132 review still match.

The existing suite passes all 111 tests under SageMath 10.6 with one BLAS
thread; see the [test log](dembele/checkpoints/tests-2026-09-30.log).
All 479 executable Python sources parse. Archived failed-source snapshots
are preserved as historical evidence, including their original syntax errors.
The transfer verifier's controls reject altered bytes, missing files,
unfetched LFS pointers and paths escaping the checkout.

Certified precision remains P800 for the complete bank, P3200 for column 0,
and P1600 for column 1. D133's remaining corrections, final verification,
24 independent audits and fixed review/replay remain pending. D134 sources
558/559 are also unrun. Exact arithmetic curve identification and the field
polynomial remain open. Source 560 is still next unused.

## Get the complete checkout

Install Git LFS before cloning, or install it in an existing checkout and
fetch the payloads:

```sh
git lfs install
git clone git@github.com:michaelmusty/two.git
cd two
git lfs pull
python3 scripts/verify_transfer.py
```

For an existing clean checkout, use `git pull --ff-only` in place of cloning,
then run the last two commands. Git LFS carries computed binary arrays,
native libraries, ACB data and the seven large JSON artifacts listed in
[.gitattributes](.gitattributes). Smaller evidence, source and prose remain
ordinary Git files. Line-ending conversion is disabled to preserve hashes.
See [GitHub's Git LFS documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).

The [transfer inventory](dembele/checkpoints/d133-transfer-2026-09-30.json)
uses relative paths and records SHA-256 and size for every retained computed
file, plus the repository sources and certificates bound by D132. The verifier
runs with Python 3.10+ and no mathematical dependencies. It verifies transferred
bytes, not mathematical validity or the ability to execute native libraries.
Run it before new work changes the mutable D133 journal.

Credentials, virtual environments, ignored build caches and third-party
checkouts stay outside Git. Recreate credentials through the destination's
secret configuration. Dependency revisions and build instructions are in
[dembele/upstream.lock](dembele/upstream.lock),
[the PARI README](dembele/pari/README.md#software-and-build) and
[CLAUDE.md](CLAUDE.md#cross-machine-setup-nothing-here-travels-with-git).
The inventory also lists the 289 external/ignored dependencies bound by
D132; these are an installation inventory, not included payloads.

## Continue with dots

Start by reading this file and the top of [HANDOFF.md](HANDOFF.md).
The historical statements that production and continuation are active are
superseded by this pause. No automatic computation should start on checkout.

The frozen receipts use absolute paths rooted at `/Users/musty/two`, and the
current arithmetic imports macOS ARM64 `.dylib` files and Homebrew GMP/FLINT.
Their sources also hardcode `/opt/homebrew` paths. These are actual execution
dependencies; a Linux checkout is ready for research and development but
cannot directly run the frozen production command. Keep all historical
sources, binaries and receipts unchanged. A different OS or checkout root
needs a separately reviewed portability adapter/new driver with new receipt
names, explicit old-to-new path mapping, preserved historical hashes and
equivalence/resource controls. Do not regenerate frozen libraries in place
or edit absolute paths inside existing certificates. The current native
versions include GMP 6.3.0, FLINT 3.6.0 and SageMath 10.6.

On the original compatible host, after verifying that the production,
continuation and store locks are free and no orphan workers remain, resume:

```sh
python3 dembele/pari/553_dyadic_staged_archiving_coordinator.py \
  --config dyadic_staged_P6400_col00_config_d133 --workers 3
```

The coordinator reuses passing receipts and starts at correction 10. Keep
the unchanged 180-second private-process-group cap, one BLAS thread, at most
three mathematical workers globally, 2 GiB per owned store and the existing
measured RAM admission rules. After production holds its lock, the existing
continuation can wait for completion in a second terminal:

```sh
python3 dembele/pari/run_d133_completion.py
```

Do not start the continuation alone while production is incomplete and
inactive. It requires the completed summary and sealed store before auditing.
Do not rerun completed phases or launch a full bank. After D133/D134 review,
re-cost the complete measured stage before choosing further computation.
