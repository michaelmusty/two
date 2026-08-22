# References and attributions

A running ledger of the papers, people, and software this project pulls from,
with *how each is used* — maintained alongside `DECISIONS.md` so that any
eventual writeup can cite accurately and generously. Conventions: role tags are
**[target]** (defines the problem), **[method]** (we execute or adapt their
technique), **[theory]** (results we invoke), **[tool]** (software we run),
**[context]** (orientation/verification). Repo pointers say where the use
happens.

## The problem and its history

- **L. Dembélé**, *A non-solvable Galois extension of Q ramified at 2 only*
  (arXiv:0811.4379). **[target]** The field we are trying to make explicit; his
  level-one mod-2 Hilbert Hecke computation over Q(ζ₃₂)⁺ is reproduced exactly
  in `dembele/` (checkpoints 1–5), and his published eigenvalue/Frobenius
  tables are our ground truth (`dembele/data/published/dembele_2009.json`).
- **J-P. Serre**, supplement to Dembélé's result (C. R. Acad. Sci.,
  doi:10.1016/j.crma.2008.12.006). **[context]** Image/ramification analysis of
  the residual representations.
- **C. Cunningham & L. Dembélé**, descent of the 16-dimensional abelian
  variety (arXiv:1705.03054). **[context]** Audited in
  `dembele/certificates/cunningham-dembele-audit.md`; we identified a gap in
  the cyclic-degree-8 case (Schur-index-2 alternative).
- **M. Musty**, *2-Group Belyi Maps* (Dartmouth thesis, 2019; advisor
  J. Voight). **[target]** Source of the open questions Q1.2.5/Q6.2.1; the
  legacy negative arc (`writeup/main-result.md`) and the present covers arc
  (`writeup/all-2-power-covers.md`) are its sequels.

## The M23 cluster (the trigger and the method template)

- **X. Huang, B. Jackson, K.-H. Lee, B. Poonen, R. Pries, S. Zhang**, *The
  Mathieu group M₂₃ is a Galois group over Q* (arXiv:2608.08538). **[method]**
  The template for the whole rigidity arc: non-rigid triples with
  𝔊-equivariant branch data, numerics-then-certify, tame mod-p monodromy
  certification (their Prop 3.5 pattern is our `GaloisGroup`-certification
  step), and the polred/specialization endgame. `dembele/rigidity/README.md`.
- **S. Zhang**, *How AI entered our collaboration on M₂₃* (personal note,
  shaowuzhang.com; copy at `dembele/rigidity/refs_how-we-found-m23.pdf`).
  **[method]** The coordinates-not-precision lesson (DECISIONS D3) and the
  4-tuple → triple discovery narrative; directly caused our equivariant-gauge
  pivot, which every subsequent recognition uses.
- **F. Häfner**, braid orbits and M₂₃ (arXiv:2202.08222; also Diplomarbeit,
  Karlsruhe 1987). **[method]** The 4-point-orbit → boundary-triple
  correspondence (their Thm 5.1) is the conceptual basis of our boundary/cusp
  maps (scripts `24`, `29`), which became our cheap oracle for component
  arithmetic.
- **M. Klug, M. Musty, S. Schiavone, J. Sijsling, J. Voight**, *Numerical
  calculation of three-point branched covers* (LMS J. Comput. Math. 17, 2014),
  and **M. Musty, S. Schiavone, J. Sijsling, J. Voight**, *A database of Belyi
  maps* (ANTS XIII, 2019). **[tool/method]** The `~/Belyi` package is our main
  computational engine for all cover computations; we made four local patches
  during this work (TrialDivision guard, genus-1 and hyperelliptic dump hooks,
  genus-scaled column count) that should be offered upstream.
- **R. van Bommel, E. Costa, B. Poonen, P. Srinivasan**, *Curve equations from
  expansions of 1-forms at a nonrational point* (LuCaNT, 2026). **[method,
  planned]** The general-genus equation-recognition method (used by the M23
  paper for their genus-4 curve); our named tool for the parked Sz(8) and any
  future k=8 curve computation.

## Rigidity, Hurwitz spaces, reduction of covers

- **M. Fried & H. Völklein** (Math. Ann. 290, 1991). **[theory]** Hurwitz
  spaces, Nielsen classes, the rigidity framework; the braid action we compute
  in scripts `20`, `22`, `29`.
- **M. Fried**, branch cycle lemma. **[theory]** The ε-cyclotomy constraints
  on class multisets — our "forced 2-cyclotomic layer" computations.
- **K. Coombes & D. Harbater** (Duke 1985); **P. Dèbes & J-C. Douai** (Ann.
  ENS 1997). **[theory]** Field of moduli = field of definition for
  center-trivial covers; invoked for every moduli-field statement.
- **S. Beckmann** (J. Algebra 1989). **[theory]** Good reduction of covers
  away from |G|; the gate-2 analysis in `writeup/all-2-power-covers.md` §1, §4.
- **M. Raynaud** (Invent. Math. 1999); **S. Wewers** (J. AMS 2003);
  **I. Bouw & S. Wewers** (Crelle 2004 and related). **[theory]** Bad
  reduction of three-point covers at p ∥ |G|: the mixed ordinary/supersingular
  picture our local-mechanism data exemplifies (`local-mechanism.md`), the mild
  moduli ramification we observe, and the deformation-data machinery that is
  the named route to replacing our transfer hypothesis with a theorem.
- **A. Grothendieck** (SGA 1), with **F. Orgogozo & I. Vidal** for the tame
  specialization refinements. **[theory]** Tame specialization isomorphism —
  underlies both the good-reduction lifting arguments and the M23-style mod-p
  certification.
- **Conway–Parker** (unpublished; via Fried–Völklein). **[context]** The
  braid-transitivity expectation against which our short orbits are the
  interesting exception.
- **L. E. Dickson**. **[theory]** Subgroup classification of PSL₂(q) — the
  generation filters in every census.
- **R. Lang** — Lang's theorem. **[theory]** The outer-coset class
  correspondence (classes over φʲ ↔ classes of SL₂(2^gcd)) used throughout the
  censuses.
- **M. Suzuki** (1962). **[theory]** The Sz(q) family and its 2-Sylow
  structure — the independent-family test (script `21`).
- **J-P. Serre**, *Topics in Galois Theory*; **G. Malle & B. H. Matzat**,
  *Inverse Galois Theory*. **[context]** Rigidity background and the
  realization landscape.

## The period route (Hilbert modular / quaternionic side)

- **M. Eichler; G. Shimura**. **[theory]** Brandt matrices; Eichler–Shimura
  theory relating weight-2 forms to abelian varieties — the reason λ-torsion of
  B_g gives the field.
- **H. Jacquet & R. Langlands**. **[theory]** The correspondence moving
  Dembélé's form between definite and indefinite quaternion algebras; the
  parity constraint that forces the auxiliary prime.
- **K. Ribet**; **A. Rajaei** (*On the levels of mod ell Hilbert modular
  forms*, J. reine angew. Math. 2001); **R. Taylor**; **F. Jarvis**.
  **[theory]** Level raising and lowering. The congruence condition
  `a_q = +-(Nq+1) mod lambda` is what the gate-1 scan searches for. We
  deliberately **do not invoke** these theorems for gate 3: they are general for
  `ell > 2`, whereas `ell = 2` is a separate delicate case (cf. *Level raising
  mod 2 and arbitrary 2-Selmer ranks*, arXiv:1501.01344), and Rajaei's
  even-degree hypothesis asks for a special or supercuspidal place, which our
  level-one form does not have. Hence the direct computation (D24,
  `dembele/certificates/gate3-status.md`).
- **I. Cerednik; V. Drinfeld**. **[theory]** p-adic uniformization of Shimura
  curves with a finite disc prime — the pivot that eliminates the genus wall
  (`levelraise-cd-plan.md`).
- **J. Teitelbaum**. **[method]** First explicit p-adic periods of Shimura
  curves; the lineage of our planned computation.
- **M. Greenberg** (2006–09). **[method]** Numerical p-adic integration on the
  Bruhat–Tits tree; with **J. Voight** (Math. Comp.), the definite
  Hecke-eigenvalue algorithms behind `hilbertmodularforms`.
- **X. Guitart, M. Masdeu, M. H. Şengün** (JLMS 2014; J. Algebra 2016; PLMS).
  **[method]** Overconvergent quaternionic Darmon points; *p-adic periods →
  algebraically recognized equations* — the published proof-of-concept for our
  endgame pattern. **M. Masdeu**'s `darmonpoints` (Sage/Magma) is the closest
  existing implementation and the designated de-risking vehicle for gate 4.
  **Assessed 2026-08-16** (`gate4-*.md`): the overconvergent *lift* works and is
  timed (dimension-2 case reproduced, matching an independent modular-symbols
  ground truth), but the *period* path has bit-rotted under Sage 10.6 — four
  version-drift failures, abandoned rather than risk silently wrong periods — and
  `padicperiods` is genus-2 specific (three half-periods, Igusa recognition),
  while the group layer only offers the Fuchsian construction for totally real
  base fields. So it is a source of algorithms and a partial reference, not a
  drop-in engine.
- **H. Shimizu**. **[theory]** The volume formula behind the archimedean
  infeasibility computation (ζ_F(−1) = 5820 ⇒ genus ≥ ~91(Nq₀−1)/2).
- **M. Kirschmer & J. Voight**. **[tool/theory]** Quaternion ideal-class
  algorithms (inside Magma) — the Brandt infrastructure and, prospectively, the
  CD dual graph.
- **J. Voight**, *Quaternion Algebras* (book) and the Magma Fuchsian/arithmetic
  machinery. **[theory/tool]** Reference frame for the whole quaternionic side.
- **E. Costa, S. Schiavone, J. Voight et al.** (the 17T7 project,
  arXiv:2411.07857 and companions; `edgarcosta/hilbertmodularforms`,
  `SamSchiavone/17T7`). **[method/tool]** The pinned HMF package our Brandt
  computations run on; the isogeny-polynomial/Eisenstein framework adapted in
  `dembele/certificates/eisenstein-prototype.md`; and (with van Bommel, Elkies,
  Keller) the descent-congruence certification method behind the
  `inverse-galois-hmf` sweep that supplies our k=4 nonexistence control.
- **J. Bosman**, *On the computation of Galois representations associated to
  level one modular forms* (arXiv:0710.1237), with **B. Edixhoven,
  J-M. Couveignes** et al. **[context/method]** Explicit polynomials for
  projectivised mod-`ell` level-one representations — degree `ell+1`, ramified
  only at `ell`, Galois group `PGL_2(F_ell)`: the same *shape* as our degree-257
  target one scale down. Table 1 supplies the only empirical anchor we have for
  the **height** of the polynomial we are trying to produce, and hence for the
  precision `M` the endgame needs (`dembele/certificates/target-height-estimate.md`).
- **A. Odlyzko**. **[theory]** Discriminant lower bounds. Used twice: to note
  that effective Chebotarev is vacuous at our conductor, and — with the
  ramification analysis at 2 — to prove `L` **cannot be totally real**
  (`rd(L) <= 31.9 < 60.8`), so complex conjugation acts as a unipotent
  involution.
- **J. Igusa**. **[theory]** Genus-2 invariants — the gauge-invariant
  recognition planned for the genus-2 corner verdict.
- **Kronecker–Weber**; **J. Lagarias & A. Odlyzko**. **[theory/context]** The
  C₈-subfield forcing into Q(ζ₂^∞); the (vacuous-at-our-conductor) effective
  Chebotarev bounds, cited to justify treating equidistribution as heuristic.

## Software and infrastructure

- **Magma** (Bosma–Cannon–Playoust), V2.29-8/9 — every exact computation.
- **The Belyi package** (Musty–Schiavone–Sijsling–Voight) with our four local
  patches — all cover numerics.
- **`hilbertmodularforms`** (Costa et al., pinned commit in
  `dembele/upstream.lock`) — Brandt/Hecke computations.
- **chatelet.mit.edu** (MIT-hosted CoCalc; Magma license courtesy of the host
  institution) — all heavy compute; client in `remote_magma/`.
- **Aristotle** (Harmonic) + **Lean 4 / Mathlib** — formalization of Lemma A
  (legacy) and the fixing congruence (in progress, `aristotle_fixing/`).
- **SageMath / GAP, PARI/GP, LMFDB** — the legacy scans, polred endgame
  (planned), and the modular-forms data environment.

## People (beyond the papers)

The M23 team's decision to publish not only their result but *how they found
it* (Zhang's note) materially changed this project's trajectory — twice (D3,
D16-meta). If any of this reaches publication, that intellectual debt — and
the KMSV/MSSV/17T7/HMF software lineage from the Voight school that both
projects run on — should be acknowledged prominently.

---

*Maintenance: add an entry when a new source enters the work; state the role
tag and where in the repo the use lives. Prefer over-attribution to under.*
