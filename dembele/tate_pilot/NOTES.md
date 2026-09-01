# Tate pilot — working notes

## 2026-09-01 (pilot start)

- darmonpoints 8.3 installed in SageMath 10.6
  (`~/Library/SageMath-10-6/lib/python3.12/site-packages/darmonpoints`),
  imports fine; the 35a1 smoke test ran on 08-16.
- Source read (sarithgroup.py): `get_BT_reps` at :493 with the
  `_hardcode_matrices` explicit-reps branch; `reduce_in_amalgam` at :805
  (purely p-adic, reusable); `local_splitting` calls
  `Gpn._compute_padic_splitting` — our class supplies the splitting from the
  Magma export instead. `edge_from_quaternion` uses `embed` at prec 20.
- Cost sanity at level 31 (dim-2 calibration constant `c = 1.77e-5 s`,
  cost ~ positions x cosets x M^3): positions 1461, cosets 32, M = 20 →
  ~1.8 core-h in Python. M = 60 → ~50 core-h. Both fine.
- **Same-session trap identified before it bit:** 56's banked eigenvectors
  are in 56's session basis; the element export (57) must re-derive
  eigenvectors in its own session alongside the rids export. 56's
  basis-independent outputs (ord(q_E), U signs, a_127) stand.
- Phase-1 job (56) launched on chatelet (`tate_lattice.out`): stab orders at
  level 31 = {1,3}, ulcm 96, g 32 — note `ulcm/g = 3` matches D31's level-31
  reciprocal constant.

## Open items (ordered)

1. 56 results: five (ord q_E, U-sign, a_127) triples.  [running]
2. Write 57 (same-session element export; JSON schema in definite_group.py).
   Magma intrinsics to use: `QuaternionAlgebra(SetOfPlaces)`, `Order(...)`
   Eichler of level p31 (or extract the HMF package's own via
   `QuaternionOrder(M)` — PREFERRED for consistency), `RightIdealClasses`,
   unit groups, `pMatrixRing(O, p31 : Precision := M)` for the splitting.
   BT reps: the p31-Iwahori structure — the package's `HilbertModularSpace
   DirectFactors` P^1-line data (PLD) may already hold the P^1(F_31)
   parametrization; investigate before hand-rolling.
3. Phase 3: fill definite_group.py; internal validation = reproduce the
   Brandt eigensystem from the class's own cocycle space.
4. Ground-truth-over-Q question: ANSWERED 2026-09-01 — NO.
   `BigArithGroup(13, 2, 1)` fails (Magma errors inside
   Algebra/AlgQuat/ramified.m: the definite algebra has no Fuchsian group,
   same root cause as over F). Consequence: the definite class is needed even
   over Q — which sets the development order: build it over Q FIRST (Sage has
   native quaternion ideals/Brandt over Q; ground truth from
   E.tate_curve(p).parameter() on a conductor-2p curve, e.g. 26a/26b at
   disc 2, p = 13), then swap the data layer to the Magma export for F.
