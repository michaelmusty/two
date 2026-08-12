# Session handoff

## Objective and exact target

Construct an explicit polynomial whose splitting field is Dembélé's nonsolvable
extension of \(\mathbf Q\), ramified only at \(2\).

Let

\[
F=\mathbf Q(\zeta_{32})^+,\qquad
S=\operatorname{SL}_2(\mathbf F_{256}).
\]

Dembélé's two residual representations cut out linearly disjoint fields \(E,E'/F\).
Their compositum \(K=EE'\) is Galois over \(\mathbf Q\), with

\[
\operatorname{Gal}(K/\mathbf Q)\simeq S^2\rtimes C_8.
\]

The practical first target is a degree-\(257\) polynomial over
\(\mathbf Q(\sqrt2)\) for the projective \(S\)-action. Combining it with its conjugate
would give a degree-\(514\) polynomial over \(\mathbf Q\) with splitting field \(K\).

Important: geometric descent of the characteristic-zero abelian variety is **not**
needed to define \(K/\mathbf Q\) or prove this Galois group. It is only a possible
constructive shortcut.

## Results completed

### Exact reproduction of Dembélé's computation

- Certified \(F\), its \(C_8\)-action, relevant prime orbits, and class data.
- Reproduced the 58-dimensional raw Brandt module and 57-dimensional cuspidal module.
- Reproduced Dembélé's mod-\(2\) characteristic polynomials.
- Matched every published trace and Frobenius order above \(31\) and \(97\) on both
  eight-dimensional constituents.
- Verified the residual Galois indexing and \(\mathbf F_{256}\) normalization.

### Positive characteristic-zero lift result

The characteristic-zero cusp space decomposes into dimensions

```text
[1, 2, 2, 4, 16, 32].
```

The unique 16-dimensional component has Hecke field \(H\). The two primes of \(H\)
above \(2\) are unramified of residue degree \(8\), and reduction at them gives exactly
Dembélé's two residual systems. This settles the original lift-versus-torsion fork
positively. See:

- `dembele/certificates/lift-report.md`
- `dembele/data/computed/target_lift_field.json`
- `dembele/data/computed/lift_field_structure.json`

There is no quadratic inner twist, CM, or proper base change that reduces the expected
abelian dimension from \(16\) to \(8\).

### Constructive period and invariant audit

- The Costa--Schiavone--Voight isogeny-polynomial framework applies abstractly with
  257 two-isogeny neighbors.
- Only nine Oda sign classes are sufficient, not all 256 signs.
- A direct parallel-weight-4 Hilbert Eisenstein invariant successfully replaced the
  \(4^g\) theta enumeration in the genus-4 17T7 control. It stably separated all
  17 neighbors.
- The Oda-period front end is nevertheless infeasible by the published twisted
  \(L\)-value method. Required single-negative characters first occur at conductor norm
  \(991\), and one decimal digit already requests roughly \(1.35\cdot10^{10}\) Hecke
  coefficients.

See:

- `dembele/certificates/eisenstein-prototype.md`
- `dembele/certificates/period-feasibility.md`
- `dembele/certificates/constructive-feasibility.md`
- `dembele/certificates/csv-paper-adaptation.md`

### Hecke-field ideals and polarization gate

Under GRH class-group bounds:

\[
\mathrm{Cl}(H)\simeq C_2,\qquad
\mathrm{Cl}^+(H)\simeq C_2^2.
\]

Both primes above \(2\) and the codifferent are narrowly principal. Exact data:

- `dembele/data/computed/lift_field_ideals.json`
- `dembele/magma/31_lift_field_ideals.m`

### Descent audit

Cunningham--Dembélé's claimed descent of the 16-fold to \(\mathbf Q\) has a genuine gap
for cyclic degree \(8\): their proof omits the Schur-index-\(2\), totally indefinite
quaternion alternative. The correct conductor of a genuinely descended 16-fold would
be \(2^{124}\), not \(2^{248}\).

Local decomposition of \(H/\mathbf Q(\sqrt5)\) at \(2,5,89,661\) is now exact and
narrows where a quaternion obstruction could ramify. A Whittaker-rationality repair does
not immediately apply because the automorphic induction has singular Hodge weights
\(0^8,1^8\), not regular algebraic weights.

See:

- `dembele/certificates/cunningham-dembele-audit.md`
- `dembele/data/computed/brauer_local_data.json`
- `dembele/magma/33_brauer_local_data.m`

This descent issue is mathematically interesting but is not currently the main blocker
to an explicit polynomial.

## Running computation

One remote Magma job may still be active:

```text
job: lift_field_generators
script: dembele/magma/34_lift_field_generators.m
purpose: explicit totally positive generators for both primes above 2 and the codifferent
```

Check and fetch it with:

```sh
python3 dembele/jobs/chatelet_job.py status \
  lift_field_generators --marker 'PASS|dembele_lift_field_generators'
python3 dembele/jobs/chatelet_job.py fetch lift_field_generators
```

Allow it to finish if still running. It only de-GRHs principality; it does not unblock
the polynomial. Nothing else should be launched from the killed-route list below.

## Current bottleneck and recommended next work

**Hard stop.** An exhaustive audit of constructive ideas is recorded in:

- `dembele/certificates/idea-exhaustion.md`
- `dembele/data/computed/idea_exhaustion.json`
- `dembele/certificates/torsion-construction-scorecard.md`
- `dembele/certificates/frob-disc-gate.md`

Killed in particular: twisted-\(L\) Oda periods; Greenberg–Voight periods at level 1;
dense and sparse Frobenius–Hunter search; \(\Omega^+\)+RM sign recovery; classical
mod-\(2\) level \(2^k\) realization; CSV without a new front end; HMF/RieSrf hacks.

The missing object remains a period matrix or another explicit realization of
\(\lambda\)-torsion. The Eisenstein back end is ready once that exists. Do **not**
restart Hecke/lift audits or re-run variants of the killed routes. The next advance
must be a new mathematical front end outside the present toolkit.

## Verification

Run all lightweight certificates:

```sh
python3 -m unittest discover -s dembele/tests
```

Current result: 34 tests pass.

Magma scripts print explicit `PASS|...` markers because Magma can return process status
zero after a source-level runtime error.

## Repository and environment

- Repository: `/Users/musty/two`
- Branch: `main`
- Remote: `git@github.com:michaelmusty/two.git`
- Local Magma: V2.29-8
- Local HMF package: `/Users/musty/hilbertmodularforms`
- Pinned HMF revision: `f5ce65826697ee1ba7ed6e77a3fda0ef779f633b`
- Remote Magma: `remote_magma/cocalc.py`
- Remote credentials: gitignored CoCalc configuration
- Aristotle virtual environment: `.venv`
- Aristotle credential: `ARISTOTLE_API_KEY` in gitignored `.env`

The current research changes are uncommitted. Review `git status` before beginning new
work. Never print or commit `.env`.

## Primary references

- Dembélé: <https://arxiv.org/abs/0811.4379>
- Cunningham--Dembélé: <https://arxiv.org/abs/1705.03054>
- Costa--Schiavone--Voight: <https://arxiv.org/abs/2411.07857>
- Serre's supplement: <https://doi.org/10.1016/j.crma.2008.12.006>
