# Direct Hilbert-Eisenstein prototype

## Verdict

The proposed replacement for generic theta enumeration passes a genus-4 control test.
A directly evaluated normalized Hilbert Eisenstein series of parallel weight \(4\)
separates all \(17\) two-isogeny neighbors of the abelian fourfold used in the 17T7
construction.

This does not yet solve the genus-16 target, but it establishes that the alternative in
Section 3.5 of the Costa--Schiavone--Voight paper is computationally meaningful rather
than merely formal.

## Control setup

The RM field is

\[
K=\mathbf Q(a),\qquad
a^4-10a^3+20a^2+25a-25=0,
\]

with discriminant \(725\) and narrow class number \(1\). The pinned
EichlerShimuraHMF code recovered the Schottky-selected neighbor with Schottky value
approximately

\[
5.83\cdot10^{-73}.
\]

For this field,

\[
\zeta_K(-3)=\frac{541}{15},
\]

so the constant-term-one Eisenstein series was evaluated as

\[
E_4(z)
=1+\frac{240}{541}
\sum_{0\ll\nu\in\mathfrak d_K^{-1}}
\sigma_3((\nu)\mathfrak d_K)
\exp(2\pi i\operatorname{Tr}_{K/\mathbf Q}(\nu z)).
\]

Totally positive codifferent elements satisfying the exponential cutoff were enumerated
as lattice points in a rational polytope using Normaliz. Ideal divisor sums were computed
exactly.

## Numerical result

The fine run used bare-exponential cutoff \(10^{-22}\). It required:

- 5,007 terms at the base point;
- 80,286 terms for the common imaginary part of the 16 finite neighbors;
- 315 terms for the final doubled neighbor.

The resulting roots satisfy:

\[
\min_{i\ne j}|r_i-r_j|\simeq1.1513.
\]

Comparing cutoffs \(10^{-18}\) and \(10^{-22}\) gave an unordered root error of

\[
2.49\cdot10^{-3}.
\]

Thus the observed separation is more than 450 times the empirical truncation error.
The degree-17 polynomial's coefficients, whose absolute values reach \(6.0\cdot10^{42}\),
have maximum imaginary part only \(6.7\cdot10^{-19}\) after aligning Magma's and Sage's
real embeddings.

## What this proves and what it does not

The experiment shows:

1. restricted Siegel \(E_4\) and enumeration of all theta characteristics are not needed
   to obtain a separating invariant in the control case;
2. direct Hilbert \(q\)-expansion evaluation is practical in degree \(4\);
3. the automorphy factors and isogeny-neighbor formulas give the expected coefficient
   descent numerically.

It does not yet provide:

1. a rigorous tail bound;
2. exact rational reconstruction of the degree-17 coefficients;
3. a complexity estimate in degree \(16\);
4. treatment of nonprincipal \(\lambda\) or nontrivial narrow class group.

The last two points depend directly on the running ideal and narrow-class computation for
the degree-16 Hecke field.

## Reproduction

Recover the control point:

```text
ESHMF_ROOT=/path/to/EichlerShimuraHMF \
CHIMP_ROOT=/path/to/CHIMP \
magma -b dembele/magma/40_genus4_reference_point.m
```

The CHIMP checkout needs its `endomorphisms`, `Magma`, and `Theta.magma` submodules.

Run the direct evaluator:

```text
sage dembele/tests/hilbert_eisenstein_genus4.sage
```

Machine-readable output is stored in
`dembele/data/computed/eisenstein_genus4.json`.
