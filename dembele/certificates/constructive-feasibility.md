# Constructive feasibility after the lift audit

## Current verdict

The characteristic-zero lift exists, but the published 17T7 pipeline is not directly
scalable to it. Direct Hilbert-Eisenstein evaluation successfully replaces the theta back
end in a genus-4 control. The remaining obstruction is now the period front end: required
quadratic twists have conductor norm \(991\), making approximate-functional-equation
recovery infeasible. Exact computation also rules out the only plausible quadratic inner
twist or proper base change that could have reduced the expected abelian variety to
dimension \(8\).

The expected characteristic-zero object is therefore a \(16\)-dimensional abelian variety
over \(F=\mathbf Q(\zeta_{32})^+\), subject to the usual Eichler--Shimura existence issue
for this setting.

## Exact Hecke-field structure

For the degree-16 Hecke field \(H\):

- signature: \((16,0)\);
- \(\operatorname{Aut}_{\mathbf Q}(H)\simeq C_8\);
- \(H/\mathbf Q\) is not Galois;
- the fixed field of the full automorphism group is \(\mathbf Q(\sqrt5)\);
- \(\operatorname{disc}(H)=5^{14}89^7 661^4\);
- there is one embedded subfield in each degree \(2,4,8\);
- the unique octic subfield has discriminant \(5^6 89^3\), so it is not the base field
  \(F\) and \(F\cap H=\mathbf Q\).

The two primes above \(2\) remain unramified with residue degree \(8\). The cyclic
automorphism structure explains why one degree-16 characteristic-zero orbit reduces to
Dembélé's two degree-8 systems.

## Why there is no 8-dimensional building block

The only possible halving mechanism is a quadratic inner twist associated with the unique
octic subfield of \(H\). Such a twist would force the residual traces to be fixed by
\(x\mapsto x^{16}\), hence to lie in \(\mathbf F_{16}\).

Dembélé's first trace above \(31\), \(\alpha^{100}\), has multiplicative order \(51\),
which does not divide \(15\), and

\[
(\alpha^{100})^{16}\ne\alpha^{100}.
\]

Thus the quadratic inner twist does not exist. The same trace table shows that the form is
not fixed by \(\sigma^4\), excluding base change from any proper subfield of \(F\).
The nonsolvable residual image also excludes CM.

## Audit of the existing constructive code

Pinned revisions are recorded in `dembele/upstream.lock`.

`edgarcosta/EichlerShimuraHMF` provides a useful analytic front end:

1. exact Hecke-eigenvalue ingestion;
2. twisted \(L\)-series and functional-equation checks;
3. Oda-period extraction;
4. Cremona's lattice recognition;
5. polarized period matrices.

However, its tested path is specialized to a real-quadratic base, four sign periods, and a
quartic Hecke field. The Dembélé target has:

- base degree \(8\);
- a 256-dimensional sign-indexed cohomological eigenspace, but only nine sign classes
  sufficient for the split period spaces used by Oda's construction;
- 16 Hecke-field embeddings;
- 257 \(\lambda\)-isogeny neighbors.

Its theta back end is a hard blocker. Generic genus-16 evaluation enumerates
\(4^{16}=4,294,967,296\) characteristics for one invariant evaluation. Across a base point
and 257 neighbors this is about \(1.1\times10^{12}\) theta values. The existing Schottky
code is also explicitly genus 4.

The `SamSchiavone/17T7` repository contains the search/congruence input and downstream
tritangent checks, not a separate general period implementation. The local
`inverse-galois-hmf` repository is relevant to residual-image searches but contains no
period or theta pipeline.

## Revised constructive gates

1. Finish explicit generators and the polarization ideal for \(H\). The class-group gate
   itself now passes: under GRH bounds,
   \(\mathrm{Cl}(H)\simeq C_2\), \(\mathrm{Cl}^+(H)\simeq C_2^2\), both primes
   \(\lambda\mid2\) are narrowly principal, and the codifferent is narrowly principal.
2. Determine whether exact \(C_8\)-stability of the isogeny class is effective descent to
   \(\mathbf Q\) or \(\mathbf Q(\sqrt2)\), including the cocycle obstruction.
3. If descent is effective, identify a lower-conductor source for periods.
4. Otherwise investigate quaternionic cohomological periods or a \(2\)-adic construction
   of the projective torsion field.
5. Retain direct Hilbert-Eisenstein evaluation as the complex-analytic isogeny invariant
   once a period matrix is available.

The \(C_8\) symmetry is still useful: it organizes eigenvalues, periods, and the 257
projective points into smaller orbits. It does not, however, change the geometric dimension
from 16 to 8.

## Reproducible artifacts

- `dembele/magma/30_lift_field_structure.m`
- `dembele/data/computed/lift_field_structure.json`
- `dembele/certificates/lift-report.md`
- `dembele/upstream.lock`
