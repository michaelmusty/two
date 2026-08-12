# Explicit Dembélé field

This directory contains the new computation aimed at constructing an explicit polynomial
whose splitting field is Dembélé's nonsolvable extension of \(\mathbf Q\), ramified only at
\(2\).

The immediate milestone is narrower and fully checkable: reproduce the level-one,
parallel-weight-two mod-\(2\) Hilbert Hecke module over

\[
F=\mathbf Q(\zeta_{32})^+
 =\mathbf Q(\beta),\qquad
\beta^8-8\beta^6+20\beta^4-16\beta^2+2=0,
\]

recover its two nonzero eight-dimensional constituents, and determine exactly how they
arise from the integral characteristic-zero Hecke algebra.

## Layout

- `upstream.lock` — exact software and source revisions used by the computation.
- `data/published/` — machine-readable transcription of published checkpoints.
- `data/computed/` — generated exact data; large outputs should be reproducible and
  checksummed rather than committed blindly.
- `magma/` — exact Magma computations, ordered by milestone.
- `tests/` — lightweight validation of source data and generated artifacts.
- `jobs/` — resumable local and chatelet job manifests.
- `certificates/` — human-readable explanations backed by exact outputs.
- `polynomials/` — eventual defining polynomials and their certificates.

## First checkpoints

1. Certify the field \(F\), its \(C_8\)-action, and the ordered prime orbits above
   \(2,31,97\).
2. Using the pinned
   [`hilbertmodularforms`](https://github.com/edgarcosta/hilbertmodularforms) revision,
   reproduce the 58-dimensional raw Brandt module and 57-dimensional cuspidal module.
3. Extract a saturated integral Hecke-stable lattice before reducing modulo \(2\).
4. Match Dembélé's characteristic polynomials, eigenvalue tables, and Frobenius orders.
5. Localize the integral Hecke algebra at the two residue-degree-eight maximal ideals and
   issue a definitive characteristic-zero lift report.

The finite-field constructors in `hilbertmodularforms` deliberately reject parallel
weight \(2\). Therefore the mod-\(2\) calculation must be derived from, and checked
against, the integral raw Brandt module; reducing an arbitrary rational cusp basis is not
a valid substitute.

## Current result

The first five checkpoints are complete. The characteristic-zero space decomposes with
dimensions `[1, 2, 2, 4, 16, 32]`, and Dembélé's two mod-\(2\) systems are the reductions
of the unique 16-dimensional component at the two unramified residue-degree-8 primes above
\(2\) in its Hecke field. The exact argument and defining polynomial are recorded in
`certificates/lift-report.md`.

The Eisenstein back end for the Costa–Schiavone–Voight isogeny polynomial has passed a
genus-4 control, and the characteristic-zero lift / residual match / \(C_8\)-equivariance
/ (GRH) polarization gates are complete. An exhaustive audit of remaining constructive
ideas — twisted-\(L\) periods, Shimura-curve periods, dense and sparse Frobenius–Hunter
search, \(\Omega^+\)+RM sign recovery, classical mod-\(2\) forms, HMF/RieSrf hacks, and
CSV without a new front end — is recorded in `certificates/idea-exhaustion.md`. All are
blocked. The explicit polynomial is stalled pending a genuinely new period or
\(\lambda\)-torsion construction outside the present toolkit.

Supporting certificates: `eisenstein-prototype.md`, `period-feasibility.md`,
`frob-disc-gate.md`, `torsion-construction-scorecard.md`, `char0-equivariance.md`,
`cunningham-dembele-audit.md`. Polarization data:
`data/computed/lift_field_ideals.json`, `data/computed/brauer_local_data.json`.

## Running computations

Run the source-data checks:

```sh
python3 dembele/tests/test_published_data.py
```

Run the base-field certificate locally:

```sh
python3 dembele/tests/run_magma_certificate.py \
  dembele/magma/00_field.m PASS\|dembele_field_certificate
```

The wrapper requires an explicit `PASS` marker because Magma may report process status
zero even after a source-level runtime error.

Long Magma jobs can be sent to chatelet using the checked-in client:

```sh
python3 remote_magma/cocalc.py --timeout 3600 run dembele/magma/job.m
```

See `remote_magma/CHATELET.md` before launching detached work. In particular, CoCalc's
API timeout is also the remote process's CPU limit.

## Reproducibility policy

- Exact inputs, source revisions, and Magma versions are part of every result.
- Expensive precomputation must have a manifest and checksum.
- Numerical period calculations may discover a polynomial but cannot certify it.
- The notation
  \(\operatorname{SL}_2(\mathbf F_{256})^2\mathbin{\cdot}8\) in Dembélé's paper is not,
  without further work, a certificate that the group extension splits.
