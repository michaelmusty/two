# Scorecard: constructions of the projective λ-torsion field

## Goal

Produce an explicit degree-\(257\) polynomial over \(\mathbf Q(\sqrt2)\) (then a degree-\(514\)
norm to \(\mathbf Q\)) whose splitting field realises Dembélé's projective residual image
associated to the unique degree-\(16\) characteristic-zero Hecke orbit over
\(F=\mathbf Q(\zeta_{32})^+\), reduced at a prime \(\lambda\mid2\) with
\(\mathrm{Nm}(\lambda)=256\).

Two broad pipelines:

```text
Hecke data --> period matrix --> Eisenstein invariant --> deg-257 polynomial
Hecke data --> Frobenius / 2-adic field data ----------> deg-257 polynomial
```

The Eisenstein back end is ready in principle
([eisenstein-prototype.md](eisenstein-prototype.md)). This scorecard ranks ways to
supply the missing front end.

## Summary table

| Route | Output | Software | Fit to \((F,1,g=16)\) | Hard blocker | Verdict |
|---|---|---|---|---|---|
| 1. Twisted-\(L\) Oda periods | complex periods | Magma `LSeries` / EichlerShimuraHMF | poor (base deg 8) | conductor norm \(991\), \(\sim10^{10}\) coeffs/digit | **dead** |
| 2. Greenberg–Voight Shimura \(H_1\) | Hecke only (API) | Magma Algorithm II | **unavailable at level 1** | parity of ramification; no period export | **dead** for periods |
| 3. Definite Brandt / HMF package | Hecke eigenvalues | `hilbertmodularforms` | exact fit (in use) | no path to periods or torsion coords | **Hecke-only** |
| 4. Frobenius → deg-257 polynomial | field polynomial | PARI/`nflist`, Hunter, ad hoc | data already in hand | degree \(257\) Hunter box \(\log_{10}\mathrm{vol}\approx24084\) | **dead** (see `frob-disc-gate.md`) |
| 5. Singular-weight GSpin / orthogonal | Hecke modules | Magma orthogonal forms | descent-adjacent only | does not output \(\lambda\)-torsion | **parallel math** |
| 6. Overconvergent / \(2\)-adic symbols | \(p\)-adic periods / points | research code | no deg-8 HMF package | no implementation | **long-shot** |

## Route 1. Twisted-\(L\) Oda periods

Already settled in [period-feasibility.md](period-feasibility.md). The nine required sign
classes force quadratic characters of conductor norm at least \(991\). One decimal digit
of one such twisted \(L\)-value requests on the order of \(1.35\cdot10^{10}\) Dirichlet
coefficients. **Verdict: dead.**

## Route 2. Greenberg–Voight indefinite quaternionic homology (deep dive)

### What the literature computes

Greenberg–Voight (Math. Comp. 2011; Magma Algorithm II) locate parallel-weight-two Hecke
systems in

\[
H^1(\Gamma,V)^+,
\]

the plus eigenspace for complex conjugation on the cohomology of a Fuchsian group attached
to an indefinite quaternion order. Internally they:

1. compute a fundamental domain and presentation for \(\Gamma\) (Voight);
2. solve the word problem to evaluate Hecke correspondences on crossed homomorphisms;
3. output systems of Hecke eigenvalues.

The Eichler–Shimura map in their §3 integrates cusp forms against paths to produce
cohomology classes, but the published algorithm and Magma package use that isomorphism
only in the direction “cohomology \(\Rightarrow\) Hecke eigenvalues”.

### What Magma exposes

The `ModFrmHil` handbook surface is Hecke-centric:
`HeckeOperator`, `NewformDecomposition`, `HeckeEigenvalue`, `QuaternionOrder`,
`IsDefinite`. There is no documented intrinsic that returns period matrices, path
integrals, or an integral homology lattice suitable for Cremona–Style lattice recognition.

So even when Algorithm II runs, it does **not** supply the polarized Oda period matrix
required by Costa–Schiavone–Voight §§3.3–3.5
([csv-paper-adaptation.md](csv-paper-adaptation.md)).

### Structural fit to level one over \(F\)

GV Theorem 3.10 requires a factorization \(N=DM\) with \(D\) squarefree, coprime to \(M\),
and

\[
\omega(D)\equiv n-1\pmod{2}.
\]

Here \(n=[F:\mathbf Q]=8\), so \(n-1=7\) is odd and \(\omega(D)\) must be odd. At level
\(N=(1)\) one is forced to take \(D=(1)\), hence \(\omega(D)=0\), which violates the
parity condition. Equivalently: the Jacquet–Langlands partner of a level-one form over an
even-degree totally real field is a form on a **totally definite** quaternion algebra
(Algorithm I), not on a Shimura curve.

Local Magma probe (V2.29-8), without computing the expensive dimension:

```text
F = Q(zeta_32)^+ (absolute, degree 8), N = (1)
HilbertCuspForms(F, N)
IsDefinite(M) = true
```

Magma therefore selects the definite algorithm for our exact input. Algorithm II is not
available for this space.

### Even if periods of a Shimura Jacobian were obtained

A JL abelian variety attached to an indefinite transfer realises the same Hecke system,
but the CSV pipeline needs the **Hilbert-modular** RM torus with the nine Oda sign
spaces over the eight real embeddings of \(F\). Passing from Shimura-curve periods to
that polarized period matrix is an additional, currently undocumented, comparison of
motives / period conjectures. It is not a drop-in replacement.

### Verdict

**Dead as a period source for this project.** Useful only as background on how Magma
computes Hecke data we already possess via the definite package.

## Route 3. Definite Brandt modules / integral Hecke cohomology

This is the live computational engine
([upstream.lock](../upstream.lock), pinned `hilbertmodularforms`). It has already
delivered the \(57\)-dimensional cuspidal module, the degree-\(16\) Hecke field \(H\),
and the residual systems at \(\lambda,\lambda'\mid2\).

The definite Shimura “variety” is zero-dimensional. Its cohomology is a space of
functions on ideal classes (Brandt modules). That yields Hecke eigenvalues and residual
Galois representations as conjugacy-class data, not complex periods and not explicit
torsion coordinates on an abelian variety.

Čerednik–Drinfeld \(p\)-adic uniformization relates definite orders to Shimura curves
over \(\mathbf C_p\), and is sometimes mentioned as a bridge (GV introduction). There is
no packaged algorithm that turns our Brandt module into a \(2\)-adic period matrix or an
explicit model of \(A[\lambda]\).

**Verdict: Hecke-only infrastructure.** Keep using it; do not expect periods from it.

## Route 4. Frobenius reconstruction of the degree-\(257\) field

### What we already have

Certified residual data for both constituents, including characteristic-polynomial masks
and Frobenius orders in \(\mathrm{SL}_2(\mathbf F_{256})\) at the published prime orbits
([constituents.json](../data/computed/constituents.json),
[csv-paper-adaptation.md](csv-paper-adaptation.md) §4). Abstractly, a point stabilizer in
the projective action gives a degree-\(257\) extension of \(\mathbf Q(\sqrt2)\) with
normal closure the projective residual field.

### Method

1. Promote each residual Hecke conjugacy class to a class in
   \(\mathrm{PSL}_2(\mathbf F_{256})\) (or the appropriate projective image).
2. Read the permutation character on \(\mathbf P^1(\mathbf F_{256})\) to obtain the
   factorization type of the corresponding rational prime in a degree-\(257\) field
   \(L/\mathbf Q(\sqrt2)\).
3. Use ramification (only above \(2\)) and Artin-conductor formulae to bound
   \(\operatorname{disc}(L/\mathbf Q(\sqrt2))\).
4. Feed the bound into a targeted Hunter / Martinet search (Jones–Roberts style), using
   the factorization types as congruence and splitting filters.

### Hard blocker

The degree \(257\) is prime, so \(L/\mathbf Q(\sqrt2)\) is automatically primitive, but
Hunter coefficient boxes grow severely with degree. Published targeted searches that
produce \(\mathrm{PSL}_2(\mathbf F_q)\) fields from modular data have succeeded for
small \(q+1\) (e.g. Roberts, arXiv:1109.6879), not for \(q+1=257\). Without an extremely
strong discriminant bound (power of \(2\) with small exponent) the search is impossible.

### Verdict

**Dead** for targeted Hunter reconstruction. The gate
([frob-disc-gate.md](frob-disc-gate.md)) gives
\(\log_{10}(\text{filtered volume})\approx24084\gg12\) even with conjugate bound
\(M=2\). Cycle types on \(\mathbf P^1\) are recorded; they do not rescue a coefficient
search.

## Route 5. Singular-weight GSpin / orthogonal modular forms

Relevant to the Cunningham–Dembélé descent picture
([cunningham-dembele-audit.md](cunningham-dembele-audit.md)): a genuinely descended
\(16\)-fold over \(\mathbf Q\) would have
\(\operatorname{End}^0=\mathbf Q(\sqrt5)\) and an expected automorphic realization on
\(\operatorname{GSpin}_{17}\), with singular Hodge weights \(0^8,1^8\).

Existing Magma orthogonal-modular-form packages compute Hecke operators via
\(p\)-neighbours on lattices. They do not produce \(\lambda\)-torsion coordinates or a
Hilbert-modular period matrix. Whittaker-rationality repairs do not apply at these
weights.

**Verdict: parallel mathematics.** Do not block the constructive polynomial on this
route.

## Route 6. Overconvergent / \(2\)-adic modular symbols

Classical overconvergent symbols (Stevens, Pollack–Stevens, …) give \(p\)-adic
\(L\)-functions and sometimes \(p\)-adic points for \(\mathrm{GL}_2/\mathbf Q\).
Greenberg–Voight explicitly flag a quaternionic generalisation as future work (Stark–
Heegner program). There is no available implementation for parallel weight \(2\) over a
degree-\(8\) field at level \(1\).

**Verdict: long-shot.** Revisit only if a concrete algorithm paper + code appears for
HMF or definite-quaternion overconvergent cohomology at this scale.

---

## Recommended next experiment

### Completed: `frob_disc_gate`

Executed in [frob-disc-gate.md](frob-disc-gate.md) /
`dembele/data/computed/frob_disc_gate.json`. **Result: killed by Hunter volume.**

### What remains after this kill

See the full exhaustion pass in [idea-exhaustion.md](idea-exhaustion.md): sparse
trinomials, \(\Omega^+\)+RM, classical mod-\(2\), Čerednik–Drinfeld, modular CRT, and
CSV-without-front-end are also dead or non-actionable. The bottleneck is again a period
matrix or another explicit \(\lambda\)-torsion realization outside the present toolkit.

## References (primary)

- Dembélé, arXiv:0811.4379
- Cunningham–Dembélé, arXiv:1705.03054
- Costa–Schiavone–Voight, arXiv:2411.07857
- Greenberg–Voight, Math. Comp. 2011 (Shimura-curve Hecke algorithm)
- Magma handbook, `ModFrmHil` Algorithms I–II
- Roberts, arXiv:1109.6879 (modular forms → small-degree \(\mathrm{PSL}_2\) fields)
- Local certificates: `period-feasibility.md`, `csv-paper-adaptation.md`,
  `constructive-feasibility.md`, `cunningham-dembele-audit.md`,
  `char0-equivariance.md`
