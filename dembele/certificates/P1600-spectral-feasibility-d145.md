# D145: the proposed spectral target is impossible

Date: 2026-10-08. Continuation authorized by “continue”.

For every complex embedding of the actual normalizer curve,

    log Z'_sigma(1) > -41.

Consequently D144's sufficient target
`average(log Zprime(1)) <= -96.820` is false. This is an analytic
bound, not a numerical computation of the spectrum. It closes the
proposal to reach the height target using that spectral inequality
and the current joint upper bound alone. It does not disprove
`h_Fal(C)>=29`, the recognized equations, or the field construction.

The proof combines an exhaustive scalar trace calculation with the
congruence spectral gap and positivity in the heat trace. It does
not use D144's reconstructed RR constants. Those constants are used
only in the following interpretation: under the complete D144 identity,

    h_Fal(C)>=29  ==>  Psi+I < -249.                            (1)

Thus the present bound `Psi+I<85.172` is far too weak for this route.
The next investigation should assess the omitted geometric intersections
against (1), or obtain an exact structural identification. A numerical
spectrum or a higher precision bank cannot repair this particular gap.
Neither height target, exact positive vanishing, identification nor the
field polynomial is established here. Existing pauses and caps persist.

## 1. A trace calculation bounds all closed-geodesic lengths

Retain the actual maximal quaternion order O over

    F=Q(b),  b^8-8b^6+20b^4-16b^2+2=0.

The finite discriminant is the unique prime p=(b) above 2. Its norm
is 2. The split real place is the fifth root in increasing order,
`0<b_0<1`. The other seven quaternion algebras are definite. The
normalizer and its conjugates are the ones in
[D58](marked-descent.md); class number one and the fact that every
totally positive unit is a square are certified in
[D92](nelson-norm-one-control-d92.md) and D95.

Every positive projective normalizer element has an integral
representative of reduced norm either 1 or n=2+b. To see this, at a
split finite place the normalizer of a maximal order is the product
of the center with its unit group. Its norm valuation is even.
At p the quaternion algebra is division and its maximal order is
unique. Choose a central scalar to remove half the norm valuation
at each place, leaving valuation 0 or 1 at p. Class number one makes
this simultaneous choice global. The resulting element is integral.
Its norm divided by 1 or n is a totally positive unit, whose square
root can be removed by a further central scalar.

Let tau be the reduced trace. In the norm-one case tau belongs to O_F.
In the norm-n case tau belongs to p: the division valuation of the
element and its conjugate is 1/2, so their sum has valuation at least
1/2; since the trace lies in F its valuation is at least 1.
Put u=tau^2/n, with n=1 in the first case. Then

    0 <= u_j <= 4  at the seven definite places,
    u_0 = 4 cosh(length/2)^2 = 2+2 cosh(length).

In particular, length <= acosh(25) implies Tr(u)<=80. It suffices
to enumerate the two positive definite trace lattices through 80.
These are necessary trace conditions; no embedding of a trace as
an actual quaternion or closed geodesic is assumed.

Set C_0=2, C_1=b, C_j=b C_(j-1)-C_(j-2). We have C_8=0 and
O_F=Z[b], as verified by the field and polynomial discriminants 2^31.
The following are integral bases and exact Gram matrices:

| Norm | Trace lattice basis | Gram matrix for Tr(tau^2/n) |
|---|---|---|
| 1 | 1,C_1,...,C_7 | diag(8,16,16,16,16,16,16,16) |
| 2+b | C_0+C_1,...,C_7+C_8 | 16 times the identity |

The second basis lies in p and has index 2 in O_F, so it is all of p.
The Gram identities are checked over F. They also follow from the
orthogonality of cyclotomic cosines: if c^2=2+b in Q(zeta_64)^+,
then `(C_j(b)+C_(j+1)(b))/c=C_(2j+1)(c)`.

| Norm | Sign pairs through 40 | Sign pairs through 80 | Admissible hyperbolic traces through 80 |
|---|---:|---:|---:|
| 1 | 149 | 2,229 | 0 |
| 2+b | 64 | 1,864 | 0 |

The central trace pair +/-2 in the norm-one list is excluded exactly.
Source 609 first uses exact LDL decomposition and outward interval
branch bounds through 40. Source 610 constructs the orthogonal bases,
replays those lists, and enumerates through 80 by integer recursion.
Source 612 independently enumerates supports, magnitudes and signs
through 80. It isolates all eight roots with rational sign-changing
intervals and checks every trace inequality with rational interval
arithmetic. It reproduces both full sets and rejects an omitted vector.

Therefore every hyperbolic element satisfies

    length > acosh(25) = 3.9116227652... > 39/10.               (2)

This bounds primitive lengths and all their repetitions. It is not
a displacement bound at a chosen CM point. For any conjugate curve,
transport by Gal(F/Q) moves the split place and preserves p. The
ratio sigma(2+b)/(2+b) is a totally positive unit and hence a square,
so the same two normalized trace problems apply. Thus (2) is uniform
over the eight embeddings, without assuming their spectra are equal.

## 2. The spectral gap is a theorem for this group

[Blomer--Brumley, Definition 1 and Theorem 1](https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p18-p.pdf)
give exponent 7/64 at every place for cuspidal GL2 representations
over F. At the split real place this gives the scalar bound

    lambda_1 >= 1/4-(7/64)^2 = 975/4096 > 3/16.                (3)

Here is the applicability argument. Functions on the normalizer
quotient pull back to the norm-one maximal-order quotient. This is
the congruence quaternionic automorphic quotient in D95. Its
noncharacter constituents transfer by Jacquet--Langlands to cuspidal
GL2 representations. A real spherical complementary-series exponent
r has scalar eigenvalue 1/4-r^2. Automorphic characters restrict to
constants on the connected classical component; they do not give
extra positive eigenvalues below (3). Passing to the normalizer
selects a subspace and cannot introduce a smaller eigenvalue.
The same argument applies at every conjugate split place. D98 used
the cited theorem at finite places; this application uses its real
place assertion. No eigenvalue of C has been estimated numerically.

## 3. Positive heat terms bound each other

Write Theta(t)=sum_j exp(-lambda_j t), including the single constant
mode. The compact scalar heat trace in
[Garbin--Jorgenson, Remark 2.7, equations (2.7)--(2.8)](https://www.jstage.jst.go.jp/article/kodaimath/43/1/43_84/_pdf)
decomposes as Theta=D+H, with nonnegative identity, elliptic and
hyperbolic terms. In our notation D=I+E and

    I(t) = area/(4pi) integral_R r tanh(pi r) exp[-t(r^2+1/4)] dr,
    H(t) = exp(-t/4)/sqrt(4pi t)
           * sum_(primitive p) sum_(k>=1)
             length_p/(2sinh(k length_p/2)) exp[-(k length_p)^2/(4t)].

For an elliptic point of order m, the positive integral for its kth
power is bounded by its value at t=0, times exp(-t/4). That value is
`1/(4m sin(pi k/m)^2)`. Summing gives `(m-1/m)/12`.
Using area=2pi d, d=1455/32, the signature (16;2^17,3^9,32) gives

    0 <= D(t) <= (d/(2t)+c_E) exp(-t/4),  c_E=869/128,
    D(1) < 23.                                                (4)

The remainder of this section is our derivation from these positive
terms, not a bound quoted from the sources.

Take delta=39/10 and g_0=3/16. For 0<s<T, (2) and (3) imply

    H(s) <= sqrt(T/s) exp[(T-s)/4-delta^2(1/s-1/T)/4] H(T),
    Theta(T)-1 <= exp[-g_0(T-s)] (Theta(s)-1).

At s=1,T=4 put

    a=2 exp[3/4-3delta^2/16] < 1/4,
    q=exp(-9/16) < 4/7.

Since H(4)<=Theta(4), equations (4) and Theta(1)=D(1)+H(1) yield

    H(1) <= a[1+q(D(1)+H(1)-1)]
          < (1/4)[1+(4/7)(22+H(1))].

Solving this inequality gives two useful strict bounds:

    H(1) < 95/24,       Theta(1)-1 < 623/24.                   (5)

For the small-time integral use the same geometric comparison with
T=1 and substitute v=1/t. Since v>=1 implies
v^(-1/2)<=1 and 1-1/v<=v-1, we obtain

    integral_0^1 H(t)/t dt
      <= H(1) integral_1^infinity v^(-1/2)
               exp[(1-1/v)/4-delta^2(v-1)/4] dv
      <= H(1) * 4/(delta^2-1)
      < (95/24)*(400/1421).                                   (6)

The nonconstant spectral tail satisfies

    integral_1^infinity (Theta(t)-1)/t dt
      <= (Theta(1)-1) exp(g_0) E_1(g_0)
      < (623/24)*(31/20).                                     (7)

For completeness the last elementary estimate follows from
`E_1(x)<=-gamma-log(x)+x` for 0<x<1 and gamma>577/1000.
The latter follows from the increasing sequence
`H_N-log(N)-1/(2N)`, below its limit gamma, at N=32. Its increase
is the trapezoidal inequality for the convex function 1/x.
Source 612 bounds the logarithms and exponentials using rational
power series with explicit remainders; it proves
`exp(3/16)*(-577/1000-log(3/16)+3/16)<31/20` independently of Arb.

## 4. Pass from the heat trace to Z'(1)

We use the usual Selberg Euler product, with the same primitive
hyperbolic classes as in H. For real s>1 and lambda=s(s-1), the
elementary Gaussian Laplace integral gives

    log Z(s) = - integral_0^infinity exp(-lambda t) H(t)/t dt.

Indeed a primitive length ell and repetition k contribute
`-exp(-s k ell)/(k(1-exp(-k ell)))`, the logarithm of that Euler
factor. All relevant sums and integrals have the same sign, which
justifies this interchange in the convergence half-plane.

Subtract 1-exp(-t) inside the integral. Its integral is
`log((lambda+1)/lambda)`. By (2)--(4), the remaining integral is
convergent at both endpoints and has a limit at s=1. This proves
the simple positive leading coefficient and gives, for any T>0,

    log Z'(1) = gamma+log(T) - integral_0^T H(t)/t dt
                 + integral_T^infinity D(t)/t dt
                 - integral_T^infinity (Theta(t)-1)/t dt.      (8)

This also fixes the normalization and the sign of the constant term;
no determinant/RR comparison is used in deriving (8). Apply (5)--(7)
at T=1, and drop the nonnegative D integral. Then

    log Z'(1)
      > 577/1000 - (95/24)*(400/1421) - (623/24)*(31/20)
      = -695255321/17052000
      > -41.                                                  (9)

The bound holds at each embedding, so it also holds for the average.
Source 611 additionally evaluates the unrounded version, obtaining a
lower-bound expression approximately -40.26445; (9) is the simpler
independently audited result used for the decision.

## 5. Consequence for the proof gap

D144 gives the exact comparison, with bounded numerical inputs,

    12 h_Fal = R - S - 6 log C_* - 6 average(log Z'),
    S=Psi+I,
    R in D143's RR_main_term_after_model_interval,
    log C_* = 15log(pi)+(5081/192)log(2)+log(3)-485/64.

Thus h_Fal>=29 and (9) force

    S < R - 6 log C_* + 246 - 348 < -249.

The numerical threshold interval is centered near -249.69965. This
is a NECESSARY condition for that height, not a sufficient one and
not a bound we have proved on S. Merely proving S<-249 would still
leave the spectral upper side to handle. The point is that the
currently omitted geometric terms must first supply a much larger
improvement before spectral computation would be useful for this
height argument. The height statement itself remains undecided.

The next bounded task is to inspect the saved derivative contents
and local intersection constraints, determine which omitted terms
can actually be certified, and compare their possible contribution
with this necessary threshold. Do not launch a spectrum, a geodesic
census or another harmonic precision bank to pursue the false D144
target. Exact structural identification remains a separate option.

## 6. Audit and provenance

Sources 609--612 and their passing artifacts are frozen. All four
input jobs pass: 609 in 5.64 seconds, 610 in 4.35 seconds, 611 in
3.99 seconds and 612 in 0.83 seconds. The first three each use one
Sage child; 612 uses only Python rational arithmetic. No D145 input
job failed. The global 180-second private-process-group, three-worker,
2 GiB per worker/store and 6 GiB aggregate caps remain in effect.

The [source applicability ledger](../data/computed/P1600_spectral_sources_d145.json)
records the published inputs and the scope of our derivations. The
[fixed review](../data/computed/P1600_spectral_review_d145.json) and
[completion record](../data/computed/P1600_spectral_completion_d145.json)
bind the finite work, independent replay, source fingerprints, and
the inherited D144 provenance graph. Finite checks do not mechanically
verify the mathematical arguments in this report or the cited theorems.
