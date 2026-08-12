# Exact characteristic-zero \(C_8\)-equivariance

## Statement

Let \(W\) be the unique 16-dimensional rational newform constituent in
\(S_2(1)\) over

\[
F=\mathbf Q(\zeta_{32})^+,
\]

and let \(H\) be its degree-16 Hecke field. There is an injective homomorphism

\[
\rho:\operatorname{Gal}(F/\mathbf Q)\simeq C_8
\longrightarrow \operatorname{Aut}_{\mathbf Q}(H)\simeq C_8
\]

such that, for every prime ideal \(\mathfrak p\),

\[
a_{\sigma\mathfrak p}(f)=\rho(\sigma)(a_{\mathfrak p}(f))
\]

after choosing the corresponding representative \(f\) of the characteristic-zero Hecke
orbit.

This is an exact characteristic-zero statement; it is stronger than the already checked
mod-\(2\) trace identities.

## Proof from the certified data

The base-field Galois group acts on the Hecke algebra by

\[
T_{\mathfrak p}\longmapsto T_{\sigma\mathfrak p}.
\]

It therefore permutes the rational irreducible newform constituents while preserving
their dimensions. The certified characteristic-zero decomposition has dimensions

\[
[1,2,2,4,16,32].
\]

Because the 16-dimensional constituent is unique, it is stable under the full \(C_8\)
action. Its rational Hecke algebra is the field \(H\), so restriction of the action gives
a homomorphism

\[
\rho:C_8\to\operatorname{Aut}_{\mathbf Q}(H).
\]

The exact field computation gives

\[
\operatorname{Aut}_{\mathbf Q}(H)\simeq C_8.
\]

It remains only to show that \(\rho\) has order \(8\). The two primes
\(\lambda,\lambda'\mid2\) have residue degree \(8\). The verified residual identities show
that \(\sigma\) exchanges the two residual constituents, while \(\sigma^2\) stabilizes
each and acts on \(\mathbf F_{256}\) by

\[
x\longmapsto x^4.
\]

This residue-field automorphism has order \(4\). Hence \(\rho(\sigma)^2\) has order
divisible by \(4\), while \(\rho(\sigma)^8=1\). It follows that
\(\rho(\sigma)\) has order \(8\), proving injectivity and therefore identifying the two
cyclic groups.

The Hecke-eigenvalue relation follows directly from the definition of the induced action
on the stable Hecke field.

## Constructive significance

The isogeny class predicted by Eichler--Shimura is stable under
\(\operatorname{Gal}(F/\mathbf Q)\): coefficient conjugation merely permutes the factors
in

\[
L(A_f,s)=\prod_{\tau:H\hookrightarrow\mathbf R}L(\tau(f),s).
\]

This does **not** by itself prove that \(A_f\) descends to \(\mathbf Q\). Effective descent
requires compatible isogenies and vanishing of the resulting cocycle obstruction.
Nevertheless, descent is now the highest-value alternative to the infeasible
large-conductor twisted-\(L\)-value computation. A descended model, or even descent to
\(\mathbf Q(\sqrt2)\), could provide a lower-conductor route to periods.

Cunningham--Dembélé, arXiv:1705.03054v1, claims this descent for the same form, but its
proof omits the possible Schur-index-\(2\) crossed product when the cyclic degree is \(8\).
See `dembele/certificates/cunningham-dembele-audit.md`.

## Supporting exact artifacts

- `dembele/magma/20_char0_decomposition.m`
- `dembele/data/computed/lift_field_structure.json`
- `dembele/data/computed/constituents.json`
- `dembele/certificates/lift-report.md`
