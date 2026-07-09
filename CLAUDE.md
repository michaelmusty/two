# Project: nonsolvable number field ramified only at 2, via 2-group Belyi maps

Research repo building on **Michael Musty's 2019 Dartmouth thesis "2-Group Belyi Maps"**
(advisor J. Voight). The user (michaelmusty@gmail.com) is the thesis author.

## Goal & current answer

**Original goal:** find an *explicit* nonsolvable number field ramified only at 2 — the
thesis's "long-term application" (open questions Q1.2.5, Q6.2.1). Mechanism: a 2-group Belyi
map has good reduction outside 2 (Beckmann), so `Q(J[2^n])` is ramified only at 2; if the
Galois image in `Sp_{2g}(F₂)` were nonsolvable you'd get such a field explicitly.

**What we found (a NEGATIVE resolution):** the 2-group Belyi construction **cannot** produce
one. Such a field *does* exist (Dembélé 2009) but is not small/explicit; this construction
provably can't reach it. Full argument in **`writeup/main-result.md`**. In brief:
- Frobenius acts `F₂[G]`-linearly on `J[2] = H¹(X,F₂)`, so the arithmetic image lies in
  `Aut_{F₂[G]}(J[2])` (the centralizer of the deck group).
- **Lemma A** (indecomposable module ⟹ solvable automorphism group) — **PROVED, formalized
  in Lean 4**: `aristotle_solvable/FiniteLocalSolvable.lean` (0 sorry/axiom).
- **Lemma B** (`J[2]` is always indecomposable) — **OPEN**, but verified for ALL genus-≥2
  triples with `|G| ≤ 128` (**2008/2008**, no exceptions). This is the one remaining gap.
- Non-Galois covers are controlled by their Galois closure (a Galois 2-group Belyi map), so
  they die with the Galois route. Both routes blocked.

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

- **`writeup/`** — START HERE. `main-result.md`, `lemma-B-open-problem.md`, `README.md`.
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

## Reproduce the headline scan

```
sage torsion_shard.sage 64 1 68        # → /tmp/shard_64_1_68.csv ; all maxmult=1
awk '$1!="#"{print $5}' /tmp/shard_64_*.csv | sort | uniq -c   # → all "1" (indecomposable)
```
