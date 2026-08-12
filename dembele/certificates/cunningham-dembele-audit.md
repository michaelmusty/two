# Audit of the claimed descent in Cunningham--Dembélé

## Verdict

Cunningham--Dembélé, arXiv:1705.03054v1, studies this exact degree-16 Hilbert
constituent and claims, conditional on Eichler--Shimura, that its abelian variety descends
to a 16-dimensional variety over \(\mathbf Q\).

The printed proof does not establish that claim when the cyclic degree is \(8\). It omits
the possible Schur-index-\(2\) obstruction. Consequently, descent to a 16-fold over
\(\mathbf Q\) remains plausible but unproved by that argument.

## The missing case

Write

\[
H=L_f,\qquad K=H^{C_8}=\mathbf Q(\sqrt5).
\]

The exact Hecke equivariance defines a cyclic crossed-product class

\[
[C]\in H^2(C_8,H^\times)
\simeq K^\times/N_{H/K}(H^\times).
\]

Theorem 4.2 considers only:

1. \(C\simeq M_8(K)\), giving descent; or
2. a division algebra of degree \(8\) over \(K\).

For a composite cyclic degree, those are not the only possibilities. A degree-8 cyclic
algebra can have

\[
C\simeq M_8(K),\quad M_4(D_2),\quad M_2(D_4),\quad\text{or }D_8,
\]

where the subscript is the Schur index. A splitting field of degree \(8\) implies only
that the Schur index divides \(8\).

Polarization makes the Brauer class \(2\)-torsion. By
Albert--Brauer--Hasse--Noether, exponent equals index over a number field, so the genuine
alternatives reduce to

\[
C\simeq M_8(K)
\quad\text{or}\quad
C\simeq M_4(D),
\]

with \(D/K\) a quaternion division algebra.

## Why total reality does not remove it

The proof excludes a *totally definite* division algebra split by the totally real field
\(H\). That exclusion is valid at real places, but it does not address a totally
indefinite quaternion algebra.

Such an algebra can be split by \(H\). For example, choose two finite primes of \(K\)
having even local degree in \(H/K\), and let \(D\) ramify exactly there. Then \(D\) is:

- division over \(K\);
- split at every real place;
- split by \(H\), because each invariant \(1/2\) is killed by the even local degree.

Albert type II permits such totally indefinite quaternion endomorphism algebras for
abelian varieties. No argument in Theorem 4.2 rules this case out.

Geometrically, the unresolved alternative is a 32-dimensional \(B'/\mathbf Q\) with

\[
\operatorname{End}_{\mathbf Q}^0(B')=D,\qquad
B'_F\sim A_f^2,
\]

rather than a 16-dimensional \(B\) with \(B_F\sim A_f\).

This is a gap in the proof, not a counterexample to the descent statement itself.

## Conductor correction

For a genuine descended 16-fold \(B/\mathbf Q\), one \(K\)-adic constituent is

\[
\operatorname{Ind}_{G_F}^{G_{\mathbf Q}}\rho_f,
\]

where \(\rho_f\) is two-dimensional and unramified at finite places of \(F\). The Artin
conductor induction formula gives

\[
\operatorname{cond}
\left(\operatorname{Ind}_{F/\mathbf Q}\rho_f\right)
=\operatorname{disc}(F)^2
=2^{62}.
\]

There are two embeddings of \(K=\mathbf Q(\sqrt5)\), so the full rational Tate module has

\[
\boxed{\operatorname{cond}(B)=2^{124}}.
\]

The preprint instead prints \(2^{248}\). That exponent is twice the expected value for a
16-fold and is the exponent naturally associated with the doubled 32-dimensional
quaternionic alternative.

## What would settle descent

Choose a semilinear isogeny

\[
\mu_\sigma:{}^\sigma A_f\to A_f.
\]

The eightfold composition gives

\[
u=\mu_\sigma\,{}^\sigma\mu_\sigma\cdots
{}^{\sigma^7}\mu_\sigma\in K^\times.
\]

The 16-fold descends if and only if

\[
u\in N_{H/K}(H^\times).
\]

By the cyclic Hasse norm theorem, this can be checked locally once \(u\) is known. The
current Hecke traces determine the semilinear action but not \(u\). Useful sources for it
would be:

1. an explicit isogeny \({}^\sigma A_f\to A_f\);
2. an \(\ell\)-adic intertwining matrix, reconstructed globally from several completions;
3. the exact crossed-product endomorphism algebra of
   \(\operatorname{Res}_{F/\mathbf Q}A_f\).

Ideal, unit-norm, and polarization computations constrain the possible class but do not
determine it by themselves.

## Computed local splitting data

The local degrees of \(H/K\) at the most relevant rational primes are now exact:

\[
\begin{array}{c|c}
\text{prime of }K&\text{decomposition in }H/K\\
\hline
\mathfrak p_2,\ N=4&g=2,\ e=1,\ f=4\\
\mathfrak p_5,\ N=5&g=1,\ e=4,\ f=2\\
\mathfrak p_{89}^{(1)}&g=1,\ e=8,\ f=1\\
\mathfrak p_{89}^{(2)}&g=1,\ e=1,\ f=8\\
\mathfrak p_{661}^{(1)}&g=8,\ e=1,\ f=1\\
\mathfrak p_{661}^{(2)}&g=1,\ e=2,\ f=4
\end{array}
\]

A quaternion invariant \(1/2\) is killed after extension to \(H\) exactly when the local
degree is even. Consequently, every listed prime except the split prime
\(\mathfrak p_{661}^{(1)}\) can support the unresolved quaternion obstruction. The split
prime cannot.

This narrows a future Hasse norm calculation but still does not determine its ramification
set. The exact data are in `dembele/data/computed/brauer_local_data.json`.

## Why Whittaker rationality does not yet repair the proof

A tempting repair is to use the rational Whittaker model of the automorphic induction
\(\operatorname{AI}_{F/E}(\pi)\) on \(\mathrm{GL}_{16}\). For a **regular algebraic
cohomological** cuspidal representation of \(\mathrm{GL}_n\), Clozel's rationality theorem
does give the finite part a model over its field of rationality; see Clozel, Théorème 3.13,
or Raghuram--Shahidi, Theorem 3.1.

The regularity hypothesis fails here. Parallel weight \(2\) over the eight real embeddings
of \(F\) gives the automorphic induction Hodge weights

\[
0^{\times 8},\qquad 1^{\times 8},
\]

so the \(\mathrm{GL}_{16}\) representation is algebraic but singular, not regular
algebraic. The optimal rational-structure theorem therefore cannot simply be invoked to
produce the missing \(K_\lambda\)-model of the induced Galois representation. This is also
consistent with Cunningham--Dembélé's use of singular-weight GSpin machinery.

Even an automorphic \(K\)-model would have to be connected carefully to a
\(K_\lambda\)-linear Galois realization before it could replace the faulty step in
Theorem 4.2. Thus Whittaker uniqueness is a useful lead, but it does not currently settle
the quaternionic alternative.

## Constructive consequence

Even if the obstruction vanishes, the descended 16-fold has

\[
\operatorname{End}_{\mathbf Q}^0(B)=\mathbf Q(\sqrt5),
\]

so it is not of \(\mathrm{GL}_2\)-type. Its expected automorphic realization is on
\(\operatorname{GSpin}_{17}\), not a classical modular curve. Descent therefore does not
automatically supply a practical period algorithm.

The direct Hilbert-Eisenstein invariant remains useful once periods are available, but
the project should investigate the Brauer obstruction and non-analytic torsion or
cohomological constructions in parallel.
