# D144: joint adjunction and the compact Riemann--Roch normalization

Date: 2026-10-08. Continuation authorized by “continue”.

The remaining geometric terms can be bounded together on the actual
normalizer curve, without finding every elliptic intersection:

    Psi + I < 85.172.

Reconstructing the compact analytic comparison gives

    log C_* = 15 log(pi) + (5081/192) log(2) + log(3) - 485/64
            = 29.03456487028975... .

In D118's Faltings normalization, these yield the proved implication

    h_Fal(C) > -19.410 - (1/2) average_sigma log Z'_sigma(1),
    average_sigma log Z'_sigma(1) <= -96.820  ==>  h_Fal(C) >= 29.  (1)

The average is over the eight embeddings of F. The spectral inequality
in (1) is NOT proved or numerically tested. Combining the first inequality
with D142's actual Faltings upper bound gives the useful consistency bound

    average_sigma log Z'_sigma(1) > -98.900.                       (2)

The compact normalization below is our derivation from smooth
Riemann--Roch, metric adjunction, surgery and the scalar determinant.
Its repairs to the source's collected constants are not author-confirmed
corrections. The finite audits check arithmetic and symbolic identities;
they do not mechanically verify the geometric or analytic arguments.
No claim about the cusped case is made.

Exact positive quadric vanishing, identification and the field polynomial
remain open. The sufficient relation-space bound 623 also remains open.
P1600, column 0/P6400, all existing pauses and all resource caps persist.

## 1. Eliminate the cotangents by adjunction

Use D143's uncontracted quotient Q, its smooth marked sections P_i,
orders m_i, alpha_i=1-1/m_i and beta_i=1-1/m_i^2. Put
gamma_i=m_i-1/m_i=m_i beta_i. On Q the Petersson Hodge line is

    L = omega_Q(sum alpha_i P_i) + V.

Write l_i=h_L(P_i), q_i=height(V|P_i), H_i^Q for the Wolpert
cotangent height, and J_ij^Q for the absolute finite intersection of
two distinct sections. These are normalized absolute degrees, so local
v_b lengths at 2 are multiplied by log(2)/8. Use unordered J_ij, while
I_Q=sum_(i != j) alpha_i alpha_j J_ij is an ordered sum.

Restrict the line identity to P_i and use
O(P_i)|P_i=(omega_Q|P_i)^(-1). The archimedean factor matters:
in centered coordinates u=z^m, the Petersson norm of du/u^(1-1/m)
at the origin is m, while the Wolpert norm of du is one. Give the
other section divisors their canonical trivial norms near P_i. Thus

    l_i = H_i^Q/m_i - log(m_i)
            + sum_(j != i) alpha_j J_ij^Q + q_i.

Substituting for H_i^Q gives the exact identity

    S_Q := Psi_Q + I_Q
       = sum_i gamma_i (l_i + log(m_i) - q_i)
           - sum_(i < j) alpha_i alpha_j (m_i+m_j) J_ij^Q.       (3)

Every pairwise intersection has a nonpositive coefficient in (3).
Retaining known intersections and dropping the others gives an UPPER
bound. No disjointness claim at the odd primes is needed.

For a rational-tail contraction of length ell carrying total mark
weight r, each carried cotangent decreases by ell and each unordered
carried pair gains intersection ell. Therefore, in v_b units,

    S_after-S_before = ell(r^2-2r).

D143's nine contractions have sum ell=48 and
sum ell(1-r)^2=16955/768. Consequently

    S_X-S_Q = -(19909/6144) log(2),                             (4)

where X is the minimal regular model used by D119. This also checks
model invariance in RR: W^2 gains sum ell(1-r)^2, the nodal term loses
sum ell, and S gains their difference. Resolving the remaining nodes
is crepant and none of these sections passes through a remaining node.

## 2. Known local intersections give a substantially better bound

The D143 coefficients of V on the marked components give

    sum gamma_i q_i = (27799/256) log(2).

The eight ordinary order-two pairs have J_ij^Q=(33/16)log(2),
by D119. Their combined subtraction in (3) is (33/2)log(2).

There is also an order-two/order-32 collision at the anchor. It can
be recovered from the already certified D118 jet, rather than from
new point coordinates. In a local chart u=a z^m+..., the leading
integral derivative is m! a, whereas the m-th-power adjunction map
has coefficient m^m a. Their ratio is m!/m^m. If d_i is the finite
content of the derivative on X, and t_i the cotangent loss from Q
to X, the line identity gives

    d_i = m_i v_i + m_i sum_(j != i) alpha_j J_ij^Q
              + v_b(m_i!) - m_i v_b(m_i) + t_i.                (5)

All quantities in (5) are local valuations. At the anchor, D118 gives
d_0=280/2=140, D143 gives v_0=25, and the contracted path
5 -> 4 -> 2 -> 3 -> 6 has t_0=16+8+8+4=36. The only other
marked section on component 5 is P_32. Thus

    140 = 2*25 + 2*(31/32)*J_(2,32)^Q - 8 + 36,
    J_(2,32)^Q = 32,
    J_(2,32)^X = 68.                                           (6)

The subtraction from (3) is (527/8)log(2). As a separate control,
the ordinary order-two formula is 17/2=33/2-8, exactly the D118
content. Source 607 reconstructs all seventeen saved contents from
the marks, V, known collisions and tail paths.

At primes over 3, V and the tail correction vanish. The order-three
derivative remains integral, so (5) implies

    sum_(j != i) alpha_j J_ij >= (2/3) v(3),       m_i=3.

For each pair, its coefficient alpha_i alpha_j(m_i+m_j) in (3)
is at least twice its contribution to the sum of these nine row
inequalities. This includes pairs with just one order-three endpoint.
After absolute normalization, the total subtraction above 3 is at
least 12 log(3). It concerns different places from (6), so it may
be added to the dyadic contribution.

Using D104/D143's absolute CM Hodge heights, (3)--(6) now give

    S_X <= (51/2)(h_L(E_2)+log(2)) + 24(h_L(E_3)+log(3))
             + (1023/32)(h_L(E_32)+log(32))
             - (1193197/6144)log(2) - 12log(3)
         < 85.172.                                             (7)

The evaluated upper-bound expression is approximately 85.1719940318.
Use the D104 upper endpoint for h_L(E_2), not a conjectural exact
height. The two other CM heights retain D143's different applicable
theorems and its explicit Zhao normalization caveat. Formula (7)
bounds Psi+I jointly; it does not furnish a separate upper bound on I.

## 3. Reconstruct the compact analytic constant from uncollected factors

The primary sources are the [final author version of Freixas--von Pippich](https://perso.pages.math.cnrs.fr/users/gerard.freixas/articles/freixas-pippich-JEMS.pdf),
[Kalvin's cone determinant](https://arxiv.org/pdf/2011.05407v1), and
[Teo's scalar spectral normalization](https://www.imath.kiev.ua/~sigma/2021/083/sigma21-083.pdf).
We use the smooth RR and surgery framework, derive the elementary
metric factors directly, replace the cone determinant, and independently
check the spectral factor. The old arXiv v2 spectral expression differs
from the final author version and is not used here.

Let zeta'=zeta_R'(-1), alpha=1-1/m and beta=1-1/m^2.
The scalar spectral determinant, with curvature -1, is

    log det' Delta = log Z'(1) + d(2zeta'-1/4+log(2pi)/2)
         + sum_m [A_m+(m-1/m)log(m)/6],
    d=2g-2+sum alpha,
    A_m=sum_(j=1)^(m-1) (2j-1-m)/m * log Gamma(j/m).             (8)

This is final-version Proposition 8.1, also obtained independently
from Teo (6.6) with n=1. The nonzero spectra for functions and
one-differentials agree by differentiation on the compact orbifold.
Applying Gamma(x+1)=x Gamma(x) to Teo's shifted arguments gives (8).
In particular the denominator of A_m is m, not m^2.

For the surgery, freeze the metric at rs radius epsilon and cut
at radius t epsilon, with any fixed 0<t<1. Put

    sigma(r)=log(2/m)-alpha log(r)-log(1-r^(2/m)),
    phi(r)=sigma(epsilon)-sigma(r),   t epsilon <= r <= epsilon.

The Riemannian metric is exp(2 sigma)|du|^2. The Polyakov--Alvarez
formula with the exterior normal gives the following limits:

    integral |grad phi|^2       -> 2pi alpha^2 log(1/t),
    integral K phi             -> 0,
    integral_boundary k_g phi  -> 2pi alpha/m log(1/t),
    integral_boundary d_n phi  -> -2pi alpha.

The signed geodesic curvature of the inner boundary satisfies
k_g ds=-(1/m+o(1))dtheta. Combining the four terms yields

    log det Delta_(M,epsilon) - log det Delta_(M,hyp)
          -> alpha/2 + beta log(t)/6.                          (9)

For t=1/2 this is alpha/2-beta log(2)/6. It differs from the
collected constant in Proposition 5.3(ii). The derivation uses its
standard anomaly formula (5.1), not that collected evaluation.

Write

    F_disk=-2zeta'-log(2pi)/2+log(2)/3-5/12.

The frozen disk has Euclidean radius
2t epsilon^(1/m)/m * (1+o(1)), so its determinant contributes

    F_disk-log(epsilon)/(3m)+log(m)/3-log(2t)/3.

The cone has geodesic radius 2(t epsilon)^(1/m)*(1+o(1)).
Kalvin's expansion is

    log det Delta_cone=-(m+1/m)log(eta)/6+c_m+o(1),
    c_m=-m(log(2)/3+log(pi)/2)
         -(2zeta'-2sum j log Gamma(j/m)+5/12-log(2)/6)/m
         +log(m)/2+m log(m)/6+log(m)/(3m).                      (10)

The coefficient of log(t) in disk + anomaly - cone is exactly

    beta/6 - 1/3 + (m+1/m)/(6m) = 0.                           (11)

Thus surgery is independent of the arbitrary cut. The printed
boundary constant does not pass this test. The coefficient of
log(epsilon) is beta/6, as required by the RR truncation limit.
The volume ratio tends to one. Smooth scalar-to-Dolbeault scaling
contributes (g+2)log(2)/3.

There is a second metric factor to keep distinct from the surgery.
At a marked point, the truncated norm of du is
m epsilon^alpha/sqrt(2)*(1+o(1)). The self-pairing of O(P) corresponds
to the inverse cotangent norm epsilon^(-1). Bilinearity therefore
gives

    <omega(D)_epsilon,omega(D)_epsilon>
       = <omega_epsilon,omega_epsilon> tensor psi_W tensor O(R_epsilon),
    log R_epsilon=sum[-alpha log(2)+2alpha log(m)+alpha^2 log(epsilon)]
                     +o(1).                                  (12)

Consequently smooth RR puts the factor C(g)/R_epsilon on its right,
not C(g) R_epsilon. With

    log C(g)=(2g-2)(-12zeta'+1/2),

the finite topological factor has logarithm

    log C_top=log C(g)+sum[alpha log(2)-2alpha log(m)].           (13)

The sign of the log(m) term in (13) also follows immediately by
solving (12) for the untwisted pairing. This differs from the
positive exponent in final-version (4.6). Moving this factor into
the determinant normalization adds log C_top/6 to log C_*.

Insert (8)--(13). Gamma multiplication gives

    A_m-(2/m)sum j log Gamma(j/m)
       = -(m+1)/m * [(m-1)log(2pi)/2-log(m)/2].

All zeta' and Gamma terms cancel. The result, for compact orbifolds, is

    log C_*=(g-1)(log(2pi)-1/3)+(g+2)log(2)/3
               +sum_m [(1-1/m)(log(2)-1)/6+log(m)/(3m)].        (14)

An artificial order-one mark contributes zero. The empty-mark case
recovers the smooth normalization. The audit proves cutoff cancellation
and the algebraic reduction as identities with formal m; it separately
checks Teo's shifted Gamma factors at orders 1,2,3,4,5,8,16,32,64.
For the actual signature (16;2^17,3^9,32), (14) is the constant
stated at the start of this report.

For comparison with the final author's printed (1.2), the per-point
change is

    -Delta_m + [1/(3m)-(alpha+beta)/6]log(2)
                    -(2/3)alpha log(m),                       (15)

where Delta_m is D142's Kalvin-minus-old cone constant. This separates
the cone replacement, the collection/boundary factors, and the metric
adjunction sign. Replacing only the cone constant is insufficient.
No author confirmation or extension of these repairs to cusps is claimed.

## 4. What now remains of the height route

The arithmetic comparison in the established metric conventions is

    12 h_Fal(C) = W_hyp^2 + delta - (Psi+I) -96log(pi)
                         +6log(d)-6log(C_*)-6 average log Z'(1).

Here W_hyp^2=2d(Y/8)+d log(2)+E_model, delta=(19/2)log(2),
E_model=-(12421/6144)log(2), and d=1455/32. There is no nodal
contribution away from 2. Combining D143's interval for the main term
with (7) and (14) yields (1). Rational interval endpoints, rather than
the displayed decimal approximations, determine all strict bounds.

This resolves the full-intersection obstruction through a joint bound
and reconstructs the compact analytic normalization. The outstanding
quantity is now the actual archimedean average log Z'(1). Inequality
(2) is a consistency bound obtained from the already proved height
upper bound, not an independent spectral calculation and not evidence
that the sufficient upper bound in (1) holds.

The next task is to derive a certified analytic route to that upper
bound and assess its feasibility before admitting any actual-curve
numerical spectral work. Exact structural identification remains an
alternative. No larger harmonic bank, new level, geodesic census,
eigenvalue computation, Hecke bank or cubic search is authorized by
this checkpoint.

## 5. Finite audit and provenance

- Source 606 evaluates the constants with Arb192 and reconstructs the
  compact comparison from its separate factors.
- Source 607 uses Arb224, the independent D143 inputs, individual marks
  carried through the reverse-order blowdown replay, all seventeen D118
  local contents, formal variable-cut identities and Teo's formula.
- The first 607 attempt failed a hard-coded control that incorrectly
  said the order-three path had length 28. Its edges have length
  8+8+4=20. The failed driver snapshot, log and receipt are preserved;
  the corrected second attempt passes. The aggregate bound and analytic
  formulas did not change.
- Source 608 binds this report and its source ledger, checks both
  successful jobs and the preserved failed attempt, and rechecks D143's
  complete inherited provenance graph. Its replay checks frozen hashes.

All mathematical jobs use the frozen 180-second wrapper, one Sage child
when needed, and the inherited memory and worker caps. The fixed review,
completion packet and seven entry documents record the exact artifacts
and the continuing proof gaps.
