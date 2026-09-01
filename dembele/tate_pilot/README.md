# Tate pilot workspace

Plan: `../certificates/tate-pilot-plan.md`. Goal: compute the Tate parameter
of a rational new eigenform at level p31 over `F = Q(ζ32)⁺` from definite
Brandt data + an overconvergent lift (darmonpoints' integration layer), then
LLL-recognize `j_E ∈ F` and derive the curve's 2-division field.

## Architecture

```
Magma (57_tate_pilot_export.m, ONE session)          Sage/Python (this dir)
  quaternion algebra B/F (definite, unram. finite)     definite_group.py:
  Eichler order O of level p31                           DefiniteBigArithGroup
  right-ideal classes (rids, session order!)               — the ~14-method seam
  P¹(F_p31) BT edge reps (quaternions)                 wired into darmonpoints
  wp, unit generators, splitting B→M₂(Q₃₁)              cohomology_arithmetic +
  T_97/U_31 eigenvectors IN THE SAME session            integrals (unchanged)
        └── tate_export.json ──────────────────────────┘
```

**Same-session rule (D26b):** the eigenvector coordinates are indexed by the
session's `rids` order. Everything element-level — ideals, BT reps, vectors —
must be exported by ONE Magma session (script 57). `56_tate_pilot_lattice.m`
(already run) provides the basis-independent phase-1 numbers only:
`ord(q_E)`, `U_31` signs, `a_127`.

## The interface (from gate4-darmonpoints-assessment.md + source read
of sarithgroup.py, darmonpoints 8.3)

`BigArithGroup`-shaped object supplying:
- `small_group()` / `large_group()` — `Gpn` (level group ≅ O^×-data) and `Gn`
  (`O[1/p31]^×`); both need `gens()`, `B` (the algebra), `_is_in_order`,
  element arithmetic. Definite case: unit groups are FINITE mod center;
  `Gn` generators = units + BT edge elements (Ihara).
- `get_BT_reps()` — the 32 coset reps: quaternions mapping to the standard
  `P¹(F_31)` matrices under the splitting; `_hardcode_matrices` is the
  precedent for supplying them explicitly (sarithgroup.py:493).
- `get_BT_reps_twisted()`, `wp()` — the `p31`-normalizer element
  (norm generates p31, normalizes the Iwahori); twisted reps = `wp`-conjugates.
- `local_splitting(prec)` / `embed(q, prec)` — `B ⊗ F_{p31} ≅ M₂(Q_31)`
  to `31^prec` (norm-31 prime is degree 1, so the local field is `Q_31`).
- `reduce_in_amalgam(x)` — REUSED AS-IS (purely p-adic; sarithgroup.py:805).
- `get_covering(depth)`, `subdivide(...)` — tree combinatorics over BT reps
  (generic, reused).
- `prime()`, `base_field()`, `use_shapiro()`, `is_in_Gpn_order(x)`,
  `Gpn_Obasis()`, `coset_reps()`/`get_coset_ti(x)`.

## Files

- `definite_group.py` — the class (skeleton; phase 3).
- `tate_export.json` — phase-2 data (schema in `definite_group.py` docstring).
- `NOTES.md` — source-reading notes, decisions, measurements.

## Validation ladder (plan §3)

1. Internal: harmonic cocycles of the class reproduce the Brandt eigensystems.
2. Ground truth over Q if a supported configuration exists
   (`E.tate_curve(p).parameter()`).
3. Degree-8 run; success = recognized `j_E ∈ F` with
   `v_{p31}(j) = −ord(q_E)` (phase 1), integrality away from p31, and
   matching `a_97, a_127`.
