# Project: making Dembélé's field explicit

The current objective is to construct an explicit polynomial whose splitting field is
Dembélé's nonsolvable Galois extension of `Q`, ramified only at `2`. The base field is
`F = Q(zeta_32)^+`; the target group fits into
`1 → SL₂(F₂₅₆)² → Gal(K/Q) → C₈ → 1`.

Start new work in **`dembele/`**. The immediate milestone is to reproduce the
57-dimensional level-one, parallel-weight-two mod-2 Hilbert Hecke module, recover its two
8-dimensional nonzero constituents, and determine whether their maximal ideals lift through
the integral characteristic-zero Hecke algebra. The pinned local HMF package is
`/Users/musty/hilbertmodularforms`; heavy Magma jobs can run through `remote_magma/`.

## Legacy 2-group Belyi investigation

**Original goal:** find an *explicit* nonsolvable number field ramified only at 2 — the
thesis's "long-term application" (open questions Q1.2.5, Q6.2.1). Mechanism: a 2-group Belyi
map has good reduction outside 2 (Beckmann), so `Q(J[2^n])` is ramified only at 2; if the
Galois image in `Sp_{2g}(F₂)` were nonsolvable you'd get such a field explicitly.

**What we found (a strong conditional obstruction):** assuming Lemma B below, the 2-group
Belyi construction cannot produce one. Such a field exists (Dembélé 2009) but is not
explicit. Full argument in **`writeup/main-result.md`**. In brief:
- Frobenius acts `F₂[G]`-linearly on `J[2] = H¹(X,F₂)`, so the arithmetic image lies in
  `Aut_{F₂[G]}(J[2])` (the centralizer of the deck group).
- **Lemma A** (indecomposable module ⟹ solvable automorphism group) — **PROVED, formalized
  in Lean 4**: `aristotle_solvable/FiniteLocalSolvable.lean` (0 sorry/axiom).
- **Lemma B** (`J[2]` is always indecomposable) — **OPEN**, but verified for ALL genus-≥2
  triples with `|G| ≤ 128` (**2008/2008**, no exceptions). This is the one remaining gap.
- Non-Galois covers are controlled by their Galois closure (a Galois 2-group Belyi map), so
  they are conditionally blocked with the Galois route.

## Status ledger

| Component | Status |
|---|---|
| Frobenius ⟹ image in centralizer | standard (Beckmann + NOS) |
| Indecomposable ⟹ solvable (Lemma A) | **proved + Lean-formalized** |
| pro-2: `J[2]` controls `J[2^∞]` | standard |
| non-Galois ⟹ Galois-closure subquotient | rigorous (boundary term to tidy) |
| `J[2]` indecomposable (Lemma B) | **OPEN**; verified `\|G\| ≤ 128` |

## The one open problem (Lemma B)

Prove `H¹(X,F₂)` is an indecomposable `F₂[G]`-module for 2-group Belyi maps. Full attack
plan in **`writeup/lemma-B-open-problem.md`**: Gruenberg relation-module framework
`0 → H¹(X°,F₂) → F₂[G]² → I_G → 0` + puncture quotient; simple socle AND top already ruled
out (socle dim reaches 3; self-dual). **Start with cyclic `G`** (reduces to an `F₂[G]`-cyclic
check over the uniserial ring `F₂[t]/(t^{2^k})`). Highest-value experiment: find where
indecomposability *first fails* (non-2-generated? positive-genus base?) to pin the minimal
hypothesis.

## File map

- **`dembele/`** — CURRENT WORK: published data, exact Magma computations, tests,
  certificates, and eventual explicit polynomials.
- **`remote_magma/`** — tested CoCalc/chatelet client for Magma V2.29-8; operational
  details in `remote_magma/CHATELET.md`.
- **`writeup/`** — START HERE. `main-result.md`, `lemma-B-open-problem.md`,
  `all-2-power-covers.md` (the covers negative arc), `README.md`.
- **`DECISIONS.md`** — running decision log: every fork, the alternatives, the
  reason, the outcome. Append an entry whenever a significant choice is made.
- **`aristotle_solvable/FiniteLocalSolvable.lean`** — Lean proof of Lemma A (via Aristotle).
- **`torsion_module.sage`** — `analyze(G,s0,s1)` builds `H¹(X,F₂)` as `F₂[G]`-module + exact
  centralizer solvability (commutant/Wedderburn). CLI: `scan`, `ng`, `ngr`.
- **`torsion_fast.sage`, `torsion_shard.sage`** — MeatAxe multiplicity screen (80× faster
  indecomposability test). `torsion_shard.sage ORDER LO HI` or `... list i1,i2,...` →
  `/tmp/shard_*.csv`. This ran the order-16/32/64/128 scans.
- **`belyi/`** — equation toolkit: `verify.sage` (M1), `cyclic.sage` (M2), `towers.sage`,
  `groups.sage`, `reconstruct.sage`; **`combinatorial_tower.sage`** (fast group-theoretic
  span oracle), `export_steps.sage` (Sage→JSON for the Hecke solver), scan scripts.
- **`belyi_jl/`** — Julia/Hecke: `tower_solver.jl` + `radicand.jl` (span-first + Riemann-Roch
  radicand solver, validated to genus 5). Run: `julia --project=belyi_jl belyi_jl/tower_solver.jl <steps.json>`.
- **`aristotle_deg4/`** — earlier Aristotle proof (Thm 1.2.2 d=4 counts).
- `NOTES.md` — tool inventory (Sage 10.6, Hecke, PARI, Aristotle, lmfdb-lite).

## Key facts / gotchas

- Only **2-generated** 2-groups occur (monodromy = quotient of `F₂ = π₁(P¹∖{0,1,∞})`). At
  order 128 that's 159 of 2313 nonabelian groups — makes scans feasible.
- MeatAxe `max_multiplicity == 1` ⟺ indecomposable ⟺ (Lemma A) solvable centralizer. A
  decomposable `J[2]` with a repeated summand would be a prize candidate — none found.
- Sage's `class_group()` is the AFFINE class group, not `Pic⁰`; `is_square`/relative-tower
  places are unimplemented → the Hecke pivot exists for exactly these gaps.
- Hecke has no packaged function-field class group; it does have `is_principal` (true
  `Pic⁰`), `riemann_roch_space`. Genus-3+ non-metacyclic tower builds are slow (>15 min).
- **Aristotle CLI**: `. .venv/bin/activate`; key in `.env` (`ARISTOTLE_API_KEY`);
  `aristotle submit "<short, <255 bytes>" --project-dir DIR`; `aristotle list` for status
  (`show`/`tasks` hang — they stream); `aristotle download <id> --destination FILE.zip` (a
  FILE path, gzip-tar; a directory path errors). Prompt >255 bytes crashes the CLI.
- `.env` (API keys) is gitignored — do not commit it.

## Cross-machine setup (nothing here travels with `git`)

The repo is code + prose only; every tool below is an external install and must be
provisioned on a new machine. Verified versions on the original host (macOS):

| Tool | Version | Provides / used for | Install |
|---|---|---|---|
| **Magma** | 2.29-8 | Current `dembele/` Hilbert modular forms and exact number-field computations; installed locally and available remotely on chatelet. | licensed Magma install; remote setup in `remote_magma/CHATELET.md` |
| `hilbertmodularforms` | commit `f5ce6582…` | Definite quaternionic Hilbert Hecke/Brandt machinery; pin recorded in `dembele/upstream.lock`. | clone `edgarcosta/hilbertmodularforms` outside this repo |
| **SageMath** | 10.6 | `sage`, `libgap`; bundles **GAP 4.14.0** + SmallGroups library + MeatAxe. Core of `torsion_module/fast/shard.sage`, `belyi/`. | conda `sage`, or sagemath.org binaries |
| **Julia** | 1.12.6 | `belyi_jl/` Hecke tower + radicand solver | julialang.org |
| Julia pkgs | Hecke, Combinatorics, JSON | pinned in `belyi_jl/{Project,Manifest}.toml` | `julia --project=belyi_jl -e 'using Pkg; Pkg.instantiate()'` |
| **Python** | 3.10 | Aristotle CLI (`aristotlelib`) in `.venv/` | `python3 -m venv .venv && . .venv/bin/activate && pip install aristotlelib` |
| PARI/GP | 2.17.x | `nflist` number-field enumeration (earlier route) — **optional** | pari.math.u-bordeaux.fr |
| lmfdb-lite | — | `lmf` package for LMFDB Postgres queries (genus-2 verdict) — **optional**, external | see `[[lmfdb-lite]]` / user's setup |

**Secrets (gitignored — recreate by hand):** `.env` at repo root contains the Aristotle
key and the `COCALC_ACCOUNT_API_KEY`, `COCALC_PROJECT_ID`, and `COCALC_BASE` settings used
by remote Magma. See `remote_magma/CHATELET.md`. `.env` must never be committed.

**Minimum to reproduce the headline result** (the 2008/2008 indecomposability scans): just
**SageMath 10.6** — no Julia, Python-venv, PARI, or LMFDB needed. Julia/Hecke is only for the
equation/tower solver; the Aristotle venv is only for re-running/continuing the Lean proof
(the proof itself, `aristotle_solvable/FiniteLocalSolvable.lean`, is a static artifact and
needs only a Lean 4 + Mathlib toolchain — `leanprover/lean4:v4.28.0` — to recompile).

**Project memory:** rich session history lives in the user's `~/.claude/…/memory/` (keyed to
this directory path), not in the repo — it auto-loads for a session opened *here on this
machine* but does not travel. This `CLAUDE.md` + `writeup/` are the portable substitute.

## Reproduce the headline scan

```
sage torsion_shard.sage 64 1 68        # → /tmp/shard_64_1_68.csv ; all maxmult=1
awk '$1!="#"{print $5}' /tmp/shard_64_*.csv | sort | uniq -c   # → all "1" (indecomposable)
```
