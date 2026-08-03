# Making Dembélé's field explicit

This repository is a computational research project whose main goal is to construct an
explicit defining polynomial for the nonsolvable Galois extension of
\(\mathbf Q\), ramified only at \(2\), whose existence was proved by
[Lassina Dembélé](https://arxiv.org/abs/0811.4379).

The earlier work in this repository investigated whether the same goal could be reached
through 2-group Belyi maps arising from Musty's thesis. That investigation produced useful
code, computations, and a nearly complete obstruction argument, but it did not construct
Dembélé's field. The project now turns to Dembélé's Hilbert-modular construction itself.

## The target

Let

\[
F=\mathbf Q(\zeta_{32})^+
  =\mathbf Q(\beta),\qquad
\beta^8-8\beta^6+20\beta^4-16\beta^2+2=0.
\]

Dembélé computed two eight-dimensional irreducible constituents of the space
\(S_2(1,\mathbf F_2)\) of mod-\(2\) Hilbert cusp forms over \(F\). Their Hecke eigensystems
give surjective representations

\[
\bar\rho_f,\bar\rho_{f'}:
\operatorname{Gal}(\overline F/F)\longrightarrow
\operatorname{SL}_2(\mathbf F_{2^8}).
\]

If \(E\) and \(E'\) are the fixed fields of their kernels, then \(E\) and \(E'\) are
linearly disjoint over \(F\), and

\[
K=EE'
\]

is Galois over \(\mathbf Q\), ramified only at \(2\), and fits into

\[
1\longrightarrow
\operatorname{SL}_2(\mathbf F_{256})^2
\longrightarrow \operatorname{Gal}(K/\mathbf Q)
\longrightarrow C_8
\longrightarrow 1.
\]

In particular,

\[
[K:\mathbf Q]
=2^{19}(3\cdot5\cdot17\cdot257)^2
=2\,251\,731\,094\,732\,800.
\]

The desired output is not a power basis for this enormous Galois field. It is a manageable
polynomial over \(\mathbf Q\) whose splitting field is \(K\), together with reproducible
certificates of its Galois group and ramification. A natural first target is a degree-\(257\)
polynomial over \(F\): the projective-line action of
\(\operatorname{SL}_2(\mathbf F_{256})\) has degree \(257\), so such a polynomial can have
splitting field \(E/F\). Its Galois conjugates can then be combined and descended to
\(\mathbf Q\).

## Research program

### 1. Reproduce Dembélé's computation

- Construct \(F\), its ring of integers, and the action of
  \(\operatorname{Gal}(F/\mathbf Q)\).
- Recompute \(S_2(1,\mathbf F_2)\) and its Hecke algebra.
- Recover the two eight-dimensional eigensystems \(f,f'\).
- Match Dembélé's traces and Frobenius orders at the primes above \(31\) and \(97\).
- Record exact, machine-readable Hecke data rather than only the published table.

This phase will most likely require Magma's Hilbert modular forms machinery, or an
equivalent computation using quaternionic modular forms.

### 2. Determine which constructive route is available

The method of
[van Bommel–Costa–Elkies–Keller–Schiavone–Voight](https://arxiv.org/abs/2411.07857)
turns a characteristic-zero Hilbert newform into a period matrix and then an explicit
isogeny polynomial. It is the main model for this project, but it does not automatically
apply here: Dembélé's eigensystems are mod-\(2\) forms.

The first mathematical decision is therefore to determine whether the maximal ideals
corresponding to \(f\) and \(f'\) lift to suitable characteristic-zero parallel-weight-\(2\)
Hilbert newforms.

- **If suitable lifts exist:** reconstruct the attached abelian variety from twisted
  \(L\)-values and periods, then compute its \(2\)-isogeny polynomial. In this setting the
  relevant projective action should produce \(257\) roots.
- **If the eigensystems are genuinely torsion:** period reconstruction is unavailable
  as stated. The project must instead compute the residual representation directly from
  quaternionic or Shimura-curve cohomology, adapting constructive torsion-representation
  methods to the Hilbert setting.

This lift-versus-torsion check is the first major milestone after reproducing the Hecke
calculation.

### 3. Construct and descend the field

- Construct a polynomial over \(F\) whose splitting field is \(E\).
- Apply the \(C_8=\operatorname{Gal}(F/\mathbf Q)\) action explicitly.
- Recover \(E'\) as the appropriate conjugate and form \(K=EE'\).
- Descend to a polynomial over \(\mathbf Q\), initially without optimizing its degree or
  coefficient size.
- Search afterward for smaller subfields, better invariants, and reduced polynomials.

### 4. Certify the result

An explicit candidate is complete only after exact verification:

- its splitting field is unramified away from \(2\);
- its residual Frobenius traces agree with the two published eigensystems;
- each geometric image is \(\operatorname{SL}_2(\mathbf F_{256})\);
- the two fields are linearly disjoint over \(F\);
- the normal closure over \(\mathbf Q\) has the required extension by \(C_8\).

Numerical period calculations may be used to discover the polynomial, but the final
identification must use exact arithmetic.

## Current repository

- `nonsolvable_at_2_examples.md` — preliminary comparison with other explicit
  nonsolvable fields.
- `writeup/` — results and remaining gap from the 2-group Belyi-map investigation.
- `belyi/`, `belyi_jl/` — Sage and Julia/Hecke experiments for constructing Belyi curves.
- `torsion_module.sage`, `torsion_fast.sage`, `torsion_shard.sage` — mod-\(2\) Jacobian
  module and centralizer computations.
- `aristotle_solvable/` — Lean formalization of the algebraic solvability lemma.
- `NOTES.md` and `CLAUDE.md` — detailed history, environment notes, and legacy results.

New Hilbert-modular computations should be added in a separate top-level directory so
that the original Belyi-map investigation remains reproducible.

## References

1. L. Dembélé,
   [*A non-solvable Galois extension of \(\mathbf Q\) ramified at 2 only*](https://arxiv.org/abs/0811.4379),
   C. R. Math. Acad. Sci. Paris **347** (2009), 111–116.
2. J.-P. Serre,
   [*Un complément à la Note de Lassina Dembélé*](https://doi.org/10.1016/j.crma.2008.12.006),
   C. R. Math. Acad. Sci. Paris **347** (2009), 117–118.
3. R. van Bommel, E. Costa, N. D. Elkies, T. Keller, S. Schiavone, and J. Voight,
   [*The constructive inverse Galois problem via Hilbert modular forms: realizing the
   transitive group 17T7*](https://arxiv.org/abs/2411.07857).
4. M. Musty, *2-Group Belyi Maps*, Ph.D. thesis, Dartmouth College, 2019.

## Secrets

API keys and other credentials belong in the gitignored `.env` file at the repository
root and must never be committed. For Aristotle, the expected variable is
`ARISTOTLE_API_KEY`.
