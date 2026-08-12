# Characteristic-zero lift report

## Verdict

Dembélé's two nonzero mod-\(2\) eigensystems both lift to characteristic zero. They arise
from the unique 16-dimensional component of the level-one, parallel-weight-two
characteristic-zero Hecke module, reduced at the two primes above \(2\) in its Hecke field.

This resolves the project's lift-versus-genuine-torsion decision in favor of the
characteristic-zero construction route.

## Exact computation

The pinned `hilbertmodularforms` package decomposes the 57-dimensional characteristic-zero
space as

\[
57=1+2+2+4+16+32.
\]

Let \(H=\mathbf Q(\theta)\) be the Hecke field of the unique 16-dimensional component. The
computed defining polynomial is

\[
\begin{aligned}
h(x)={}&x^{16}-12x^{15}-255x^{14}+3655x^{13}+18005x^{12}
-393541x^{11}\\
&+119362x^{10}+17669515x^9-50861545x^8-286668975x^7\\
&+1402550907x^6+756001636x^5-11972369685x^4+12087897420x^3\\
&+26153849155x^2-54404306283x+26601321401.
\end{aligned}
\]

The equation order \(\mathbf Z[\theta]\) is already maximal at \(2\): its index in the
\(2\)-maximal order is \(1\). The full factorization modulo \(2\) is

\[
h(x)\bmod 2=
(x^8+x^4+x^3+x+1)
(x^8+x^6+x^5+x^2+1),
\]

with two distinct irreducible factors. Consequently

\[
2\mathcal O_H=\lambda\,\lambda',
\qquad
e(\lambda/2)=e(\lambda'/2)=1,
\qquad
f(\lambda/2)=f(\lambda'/2)=8.
\]

Both prime ideals have norm \(256\).

## Why this certifies lifts in the actual Hecke order

The element \(\theta\) is an integral Hecke-algebra generator, so
\(\mathbf Z[\theta]\) is a suborder of the integral Hecke order \(\mathbb T_H\), which is
itself a suborder of \(\mathcal O_H\). After tensoring with \(\mathbf Z_2\),

\[
\mathbf Z_2[\theta]\subseteq
\mathbb T_H\otimes\mathbf Z_2\subseteq
\mathcal O_H\otimes\mathbf Z_2.
\]

The \(2\)-maximal index computation says the first and last rings are equal. Therefore all
three rings are equal at \(2\), and the two degree-8 factors above are genuinely the two
maximal ideals of the integral Hecke order above \(2\).

The same two irreducible factors were independently obtained from the integral raw Brandt
matrix for \(T(\mathfrak p_{31}^1)\). Restricting all Hecke operators above \(31\) and \(97\)
to those factors reproduced every trace exponent and Frobenius order in Dembélé's Table 1,
with a unique common \(\mathbf F_{256}\) normalization. Thus the reductions at
\(\lambda\) and \(\lambda'\) are precisely Dembélé's \(f\) and \(f'\), not merely two
residue-degree-eight systems with the same dimensions.

## Reproducible artifacts

- `dembele/magma/20_char0_decomposition.m`
- `dembele/magma/21_target_lift_field.m`
- `dembele/data/computed/jobs/char0_decomposition/job.out`
- `dembele/data/computed/jobs/target_lift_field/job.out`
- `dembele/data/computed/target_lift_field.json`
- `dembele/data/computed/constituents.json`

All exact calculations used Magma V2.29-8 and
`edgarcosta/hilbertmodularforms` at commit
`f5ce65826697ee1ba7ed6e77a3fda0ef779f633b`.

## Next gate

The remaining question is constructive suitability, not existence of a lift. The next
phase must:

1. compute enough exact Hecke eigenvalues of this degree-16 orbit for twisted
   \(L\)-series;
2. determine the field automorphisms and the action of
   \(\operatorname{Gal}(F/\mathbf Q)\) on the lift and on \(\lambda,\lambda'\);
3. determine polarization and ideal-class data needed for the \(257\)
   \(\lambda\)-isogenies;
4. prototype period recovery and theta evaluation at modest precision before launching a
   full reconstruction.
