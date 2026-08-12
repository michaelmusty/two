# Frobenius discriminant / Hunter-volume gate

## Verdict

Pure Frobenius–Hunter reconstruction of the degree-\(257\) field is **dead**.

Even under absurdly optimistic conjugate bounds \(|\alpha|\le 2\) and allowing two
full Chebotolev filters of size \(|\mathrm{PSL}_2(\mathbf F_{256})|\), the monic
degree-\(257\) coefficient box still has

\[
\log_{10}(\text{filtered volume})\approx 24084\gg 12.
\]

The middle coefficient alone already contributes more than \(10^{114}\) choices.
No \(2^{O(1)}\) discriminant upper bound is needed to reach this conclusion: the
binomial coefficient \(\binom{257}{128}\) dominates.

Machine-readable output: `dembele/data/computed/frob_disc_gate.json`.

## What was computed

From the certified residual traces in `constituents.json` (Dembélé's \(f\)-component),
each Frobenius class was realised as the companion matrix

\[
\begin{pmatrix}0&1\\1&t\end{pmatrix}\in\mathrm{SL}_2(\mathbf F_{256})
\]

used by the Magma residual encoding (characteristic polynomial \(X^2+tX+1\) in
characteristic \(2\)). Its permutation action on \(\mathbf P^1(\mathbf F_{256})\) was
enumerated. In characteristic \(2\) one has \(\mathrm{SL}_2=\mathrm{PSL}_2\).

Observed factorization types for primes in the abstract degree-\(257\) extension:

| Frobenius order | \(\mathrm{SL}_2\) class | Factorization type on \(\mathbf P^1\) |
|---|---|---|
| \(257\) | nonsplit Singer | \(257^1\) (inert) |
| \(255\) | split maximal torus | \(1^2\cdot 255^1\) |
| \(51\) | split torus | \(1^2\cdot 51^5\) |

Every computed cycle type matches the group-theoretic partition for that order.
At the published orbits this gives, for the \(f\)-component:

- above \(31\): alternating Singer / split-maximal types along the \(C_8\)-orbit;
- above \(97\): alternating Singer / order-\(51\) split types.

These splitting constraints are recorded for any future non-Hunter approach; they do
not bring a coefficient search under the kill threshold.

## Hunter estimate

For a monic integral primitive element with all archimedean conjugates bounded by
\(M\), the coefficient \(a_k\) satisfies \(|a_k|\le\binom{n}{k}M^k\). Taking \(n=257\)
and \(M=2\):

- \(\log_{10}\) of the full coefficient box \(\approx 24098\);
- after subtracting \(2\log_{10}|G|\) as an upper bound on savings from the primes
  \(31\) and \(97\), one still has \(\approx 24084\);
- the single middle coefficient (\(k=128\)) has \(\log_{10}\#\mathrm{choices}\approx 115\).

The same binomial explosion applies to a relative Hunter search over
\(\mathbf Z[\sqrt2]\). An even more extreme bound \(M=1\) remains far above
\(10^{12}\).

## Discriminant status

The target field \(L/\mathbf Q(\sqrt2)\) is ramified only above \(2\), so
\(\operatorname{disc}(L/\mathbf Q(\sqrt2))\) is a power of the prime above \(2\).
No explicit small Artin-conductor exponent for the projective residual representation
was derived from the present Hecke data. The gate does not need one: volume already
kills targeted Hunter search.

## Consequence

Route 4 of `torsion-construction-scorecard.md` is closed for ordinary / targeted
Hunter reconstruction. Remaining constructive options are geometric or \(2\)-adic
(period matrix, explicit torsion, or a genuinely new sparse-polynomial method not
controlled by this gate). Descent / GSpin remain parallel theory only.

## Reproduction

```sh
python3 dembele/tests/frob_disc_gate.py
python3 -m unittest dembele.tests.test_frob_disc_gate
```
