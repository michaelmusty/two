# Theoretical adaptation of the Costa--Schiavone--Voight construction

This note records what the general results in
van Bommel--Costa--Elkies--Keller--Schiavone--Voight,
*The constructive inverse Galois problem via Hilbert modular forms: realizing the
transitive group 17T7* (arXiv:2411.07857), imply for Dembélé's degree-16 lift.

## 1. What applies directly

Let

\[
F=\mathbf Q(\zeta_{32})^+,\qquad [F:\mathbf Q]=8,
\]

and let \(f\) be the unique degree-16 characteristic-zero Hecke orbit found in this
project, with Hecke field \(H\). Let \(\lambda,\lambda'\mid2\) be the two primes of \(H\),
both with residue field \(\mathbf F_{256}\).

The paper's general constructions in Sections 3.3--3.5 allow arbitrary totally real base
degree \(n\) and arbitrary totally real Hecke-field degree \(g\). Thus their definitions of
the Oda period lattice, the polarized RM torus, and the \(\lambda\)-isogeny polynomial make
sense formally with

\[
n=8,\qquad g=16,\qquad \operatorname{Nm}(\lambda)=256.
\]

The projective line has

\[
\#\mathbf P^1(\mathbf F_{256})=257
\]

points, so a separating modular invariant gives a degree-257 polynomial whose splitting
field over \(F\) is the projective residual field.

The major theorem that does *not* apply is Theorem 3.2.2: our base degree is even and the
level is \(1\), so there is no prime exactly dividing the level. Existence of the abelian
16-fold remains an instance of the Eichler--Shimura conjecture (Conjecture 3.2.1), rather
than the Shimura-curve case proved in that theorem.

## 2. Nine sign classes suffice for the split period spaces

The full cohomological Hecke eigenspace has \(H\)-dimension \(2^n=256\), indexed by

\[
W_\infty=\{\pm1\}^8.
\]

This does **not** mean that constructing the split period lattice requires all 256 sign
periods. In equation (3.3.11), for the real embedding \(\sigma_i:F\hookrightarrow\mathbf R\),
the relevant two-dimensional \(H\)-space is

\[
V_{f,s_i}
=H\,\Omega^{s_i}\oplus H\,\Omega^+,
\]

where \(+\) is the all-positive sign and \(s_i\) has a single negative entry in position
\(i\). Oda's split conjecture then identifies a lattice in this space with the complex
abelian variety under \(\sigma_i\).

Consequently, a sufficient sign dataset for all eight split period spaces consists of

\[
\Omega^+,\Omega^{s_1},\ldots,\Omega^{s_8}.
\]

Across the 16 embeddings of \(H\), this is \(9\cdot16=144\) complex period entries, not
\(256\cdot16=4096\). Additional sign classes may provide relations and numerical
stabilization, as the fourth sign did in the quadratic 17T7 calculation. The paper does
not prove that the nine-label dataset is information-theoretically minimal, and it does
not by itself determine the fractional ideals, integral lattice, or polarization.

Theorem 3.4.6 relates each required sign vector to quadratic twists:

\[
\tau_j(\alpha_\chi)\Omega_j^s
=-4\pi^2\sqrt{\operatorname{disc}(F)}
  G(\overline\chi)L(\tau_j(f),1,\chi).
\]

The factors \(\alpha_\chi\in H\) are unknown, so recovery still requires several twists
and Cremona-style lattice recognition for each sign. A lean analytic prototype therefore
needs several quadratic characters in each of nine sign classes, not all 256.

## 3. Generic theta enumeration is not fundamental

Section 3.5 begins with an arbitrary level-one Hilbert modular form \(e\) over the RM field
\(H\), of parallel weight \(k\), with rational Fourier coefficients. It defines

\[
T_\lambda(X)
=\prod_\gamma
\left(
X-j(\gamma,z)^{-1}\frac{e(\gamma z)}{e(z)}
\right),
\]

where the 257 matrices \(\gamma\) represent the \(\lambda\)-isogeny neighbors.

The authors choose the restriction of Siegel \(E_4\) and evaluate it as a sum of eighth
powers of theta constants because this is convenient in genus 4. That is a computational
choice, not a requirement of the isogeny-polynomial construction.

A possible genus-16 replacement is a directly evaluated Hilbert Eisenstein series over
\(H\). A suitably normalized parallel-even-weight Eisenstein series is a candidate with
rational constant term and explicit divisor-sum Fourier coefficients. Its value could in
principle be evaluated by a truncated Hilbert \(q\)-expansion

\[
E_k(z)=c_0+
\sum_{0\ll\nu\in\mathfrak d_H^{-1}}
c(\nu)\exp(2\pi i\operatorname{Tr}_{H/\mathbf Q}(\nu z)).
\]

This would replace the paper's all-theta-characteristics implementation by a lattice-point
enumeration controlled by the imaginary parts of the reduced RM moduli point. To make it
rigorous, one must handle every relevant Hilbert-modular component and cusp, prove
rationality of the normalization, verify \(e(z)\ne0\), and supply reduction and truncation
bounds. No computational advantage has yet been demonstrated.

The immediate theoretical/computational questions are:

1. choose a low-weight level-one Hilbert Eisenstein series over \(H\);
2. handle the case of nonprincipal \(\lambda\) adelically if the running ideal computation
   shows this is necessary;
3. prove or verify that its ratios separate the 257 neighbors at our point;
4. derive rigorous truncation bounds after Hilbert modular reduction;
5. use several weights or a vector of invariants if one ratio has collisions.

## 4. Exact descent and group structure

For one prime \(\lambda\), the full \(C_8=\operatorname{Gal}(F/\mathbf Q)\) does not
stabilize \(\lambda\): a generator exchanges \(\lambda\) and \(\lambda'\). The subgroup

\[
\operatorname{Gal}(F/\mathbf Q(\sqrt2))
=\langle\sigma^2\rangle\simeq C_4
\]

does stabilize \(\lambda\), acting on its residue field by \(x\mapsto x^4\). Dembélé's
all-prime residual identities, together with the paper's Theorem 2.3.6 (equivalently
Corollary 2.3.17) over \(F_0=\mathbf Q(\sqrt2)\), give

\[
\operatorname{Gal}(E/F_0)
\simeq \operatorname{SL}_2(\mathbf F_{256})\rtimes C_4.
\]

The splitting follows because the image is \(\operatorname{SL}_2\) in characteristic 2,
the \(C_4\)-action lifts entrywise as \(x\mapsto x^4\), and the center is trivial. This
argument uses the residual result directly. Applying Theorem 2.4.4 through the
characteristic-zero field \(H\) will additionally require certification of the
decomposition-group action at \(\lambda\) and of the all-prime Hecke congruence in that
model.

For \(K=EE'\), the kernel over \(F\) is

\[
\operatorname{SL}_2(\mathbf F_{256})^2,
\]

again centerless. The \(C_8\)-action lifts explicitly: up to orientation, if
\(\varphi:x\mapsto x^4\), a generator may act by

\[
s(g,h)=(h,\varphi(g)),
\qquad
s^2(g,h)=(\varphi(g),\varphi(h)).
\]

This explicitly lifts the outer action. Since the kernel has trivial center, Proposition
2.3.8 then shows that the global extension also splits:

\[
\operatorname{Gal}(K/\mathbf Q)
\simeq
\operatorname{SL}_2(\mathbf F_{256})^2\rtimes C_8.
\]

This sharpens Dembélé's dot notation, subject to recording the exact orientation of the
computed coefficient-field automorphism.

If \(B\) is a point stabilizer in the action on
\(\mathbf P^1(\mathbf F_{256})\), then \(B\rtimes C_4\) has index 257 in the split group.
Its fixed field is therefore an abstract degree-257 field over \(\mathbf Q(\sqrt2)\) with
normal closure \(E\).

Given an irreducible polynomial
\(p\in\mathbf Q(\sqrt2)[x]\) for this field with splitting field \(E\), the product
\[
\operatorname{Nm}_{\mathbf Q(\sqrt2)/\mathbf Q}(p)=p\,p^\iota
\]
is an irreducible degree-514 polynomial over \(\mathbf Q\) with splitting field \(EE'\);
the global group is transitive on its two 257-element blocks. This is presently an
abstract consequence. Section 3.5 initially produces a polynomial over \(F\), so an
additional descent or simultaneous reconstruction step is required to produce \(p\) over
\(\mathbf Q(\sqrt2)\).

## 5. Revised theoretical work program

1. Finish the exact principality and polarization-ideal computation for \(H\).
2. Determine whether the now-certified exact \(C_8\)-stability of the isogeny class gives
   effective descent to \(\mathbf Q\) or \(\mathbf Q(\sqrt2)\).
3. Obtain periods from a descended lower-conductor realization, quaternionic cohomology,
   or a \(2\)-adic replacement; the direct nine-sign twisted-\(L\)-value route is
   quantitatively infeasible.
4. Scale the genus-4 direct Hilbert-Eisenstein prototype to \(H\) once a period matrix is
   available.
5. Prove that the selected invariant separates \(\mathbf P^1(\mathbf F_{256})\), using
   multiple invariants if necessary.
6. Construct first over \(\mathbf Q(\sqrt2)\), then descend the pair to degree 514 over
   \(\mathbf Q\).
