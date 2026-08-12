# Feasibility of Oda-period recovery from twisted \(L\)-values

## Verdict

The direct Hilbert-Eisenstein back end is viable, but the published twisted-\(L\)-value
front end is not directly scalable to Dembélé's base field.

The obstruction is quantitative and decisive: the required quadratic twists have large
analytic conductor before any useful numerical precision is requested.

## Required signs and conductors

Oda's split period spaces use the all-positive sign and the eight single-negative signs.
An exhaustive primitive quadratic-character scan through conductor norm \(1000\) found:

\[
\begin{array}{c|ccccccccc}
\text{sign}&+&s_1&s_2&s_3&s_4&s_5&s_6&s_7&s_8\\
\hline
\min\operatorname{Nm}(\mathfrak c)&1&991&991&991&991&991&991&991&991.
\end{array}
\]

No required single-negative character has conductor norm below \(991\).

The base field itself has

\[
\operatorname{disc}(F)=2^{31}=2147483648.
\]

For a level-one weight-two form, the completed twisted \(L\)-series therefore has
conductor

\[
\operatorname{disc}(F)^2\operatorname{Nm}(\mathfrak c)^2.
\]

For a required single-negative twist this is

\[
2^{62}\cdot991^2
=4529049216663187540148224.
\]

## Magma coefficient requirements

Magma's `LCfRequired` gives the following rational Dirichlet-coefficient bounds:

\[
\begin{array}{c|rr}
\text{decimal digits}&\operatorname{Nm}(\mathfrak c)=1&
\operatorname{Nm}(\mathfrak c)=991\\
\hline
1&4\,246\,733&13\,529\,146\,983\\
2&13\,290\,701&38\,171\,521\,844\\
5&95\,631\,975&210\,790\,200\,116\\
10&1\,056\,532\,017&1\,902\,989\,662\,695\\
20&29\,589\,598\,005&43\,635\,994\,803\,076\\
40&1\,869\,269\,484\,654&2\,351\,241\,006\,596\,040\\
80&212\,410\,318\,900\,588&240\,341\,865\,945\,550\,376
\end{array}
\]

Thus even a one-digit experiment for one required sign asks for coefficients through
approximately \(1.35\cdot10^{10}\). Computing the Hecke data needed by the 17T7
`EichlerShimuraHMF` pipeline is not realistic.

## Consequence for the constructive route

The direct Eisenstein invariant remains the preferred replacement for the theta back end,
but it first needs a period matrix obtained by another method. The next theoretical gates
are:

1. test exact characteristic-zero equivariance
   \(a_{\sigma\mathfrak p}=\rho(a_{\mathfrak p})\), which may permit descent of the
   isogeny class and a lower-conductor realization;
2. investigate a cohomological or modular-symbol period computation on a quaternionic
   transfer;
3. investigate a \(2\)-adic construction of the projective torsion field that bypasses
   complex periods entirely.

The first test is computationally accessible and is the immediate next step.

## Reproduction

```text
HMF_ROOT=/path/to/hilbertmodularforms \
magma -b dembele/magma/41_period_feasibility.m
```

The machine-readable bounds are in
`dembele/data/computed/period_feasibility.json`.
