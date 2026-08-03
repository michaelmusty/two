# Session handoff

## Current objective

Construct an explicit polynomial whose splitting field is the nonsolvable extension
\(K/\mathbf Q\), ramified only at \(2\), proved to exist by Dembélé in 2009.

Start with `README.md`, which defines the target, success criteria, and proposed research
program.

## Important correction to the legacy notes

Dembélé's field is not the degree-\(17\), \(\operatorname{SL}_2(\mathbf F_{16})\)-type
example mentioned in parts of the earlier investigation. His construction uses two
surjective representations

\[
\bar\rho_f,\bar\rho_{f'}:
\operatorname{Gal}(\overline F/F)\to
\operatorname{SL}_2(\mathbf F_{256}),
\qquad F=\mathbf Q(\zeta_{32})^+.
\]

Their fixed fields \(E,E'\) are linearly disjoint over \(F\), and \(K=EE'\) satisfies

\[
1\to\operatorname{SL}_2(\mathbf F_{256})^2
\to\operatorname{Gal}(K/\mathbf Q)\to C_8\to1.
\]

The degree-\(17\) 17T7 construction in arXiv:2411.07857 is relevant as a method, not as
the field being sought.

## Work completed in this session

- Added a root `README.md` giving the repository its new purpose.
- Reviewed Dembélé's paper and the constructive 17T7 paper.
- Identified the first major mathematical fork: determine whether Dembélé's mod-\(2\)
  eigensystems lift to suitable characteristic-zero Hilbert newforms.
- Configured Aristotle through the gitignored `.env`.
- Verified Aristotle authentication with `aristotle list`.

No Aristotle task has yet been submitted for the new project.

## Recommended next steps

1. Reproduce Dembélé's Hilbert modular forms computation over
   \(F=\mathbf Q(\zeta_{32})^+\):
   - construct the level-one, parallel-weight-two mod-\(2\) space;
   - recover its two eight-dimensional irreducible Hecke constituents;
   - match the published traces and Frobenius orders above \(31\) and \(97\).
2. Determine whether the corresponding maximal ideals of the mod-\(2\) Hecke algebra
   occur in the reduction of the characteristic-zero Hecke algebra.
3. If they lift, investigate the period-matrix and isogeny-polynomial method of
   arXiv:2411.07857. The natural projective action suggests first constructing a
   degree-\(257\) polynomial over \(F\) with splitting field \(E\).
4. If they do not lift, investigate a direct residual-representation computation from
   quaternionic or Shimura-curve cohomology.
5. Preserve all exact Hecke data and verification scripts in a new top-level directory;
   do not mix them into the legacy `belyi/` code.

## Environment

- Repository: `/Users/musty/two`
- Branch: `main`
- Remote: `git@github.com:michaelmusty/two.git`
- Aristotle virtual environment: `.venv`
- Aristotle credential: `ARISTOTLE_API_KEY` in `.env`

Never print or commit `.env`. To use Aristotle:

```sh
set -a
source .env
set +a
source .venv/bin/activate
aristotle list
```

## Relevant sources

- Dembélé: <https://arxiv.org/abs/0811.4379>
- Serre's supplement: <https://doi.org/10.1016/j.crma.2008.12.006>
- Constructive 17T7 method: <https://arxiv.org/abs/2411.07857>
- Legacy investigation summary: `CLAUDE.md`, `NOTES.md`, and `writeup/`
