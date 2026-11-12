# D151: a finite rational summed-transfer certificate is obstructed

Date: 2026-10-09. Bounded feasibility investigation authorized after D150.

**Result:** park the finite rational summed-transfer witness search proposed
in [D150, section 5](structural-identification-audit-d150.md). For a concrete
first positive coefficient of the first saved candidate quadric, no identity
of that form can exist. The obstruction allows summed cancellation and
arbitrary rational witnesses; it is not a finite search cutoff.

The reason is algebraic. Transfer-invariant linear functionals on rational
test functions need not be continuous. We construct such functionals that
kill every polynomial moment but distinguish the CM kernels independently.
A finite rational identity would have to hold for these functionals too.
The selected residual varies under them, whereas its proposed known-mass
right side does not.

This does **not** refute the candidate, produce different bounded measures,
or contradict the unique bounded moment solution. It isolates continuity
as information that this certificate form loses. Exact positive vanishing,
actual/candidate identification and the original-kernel field polynomial
remain open. The actual relation-height upper bound stays 15237; the
sufficient P1600 target stays 623. The precision banks are unchanged.

## 1. Scope and inherited exact inputs

Work over a common coefficient field contained in C_p and extend scalars
to C_p when considering linear functionals. Let K be the dyadic completion
of F, with uniformizer pi=b and residue field F2. Write G for the actual
projective arithmetic group of [D112](dyadic-cm-matching-d112.md).
Its seventeen chosen CM lifts are p_i=S_i(beta), where S_i is K-rational,
beta^2=-(2+pi), and v_pi(beta)=1/2. They lie in seventeen distinct G-orbits.
The exact point stabilizer is C2. In the coordinate

    t=S_i^(-1)z,       w_i=(t-beta)/(t+beta),

its nonidentity element sends t to beta^2/t and w_i to -w_i.
These are actual uniformization inputs, independent of the candidate.

Retain [D113](dyadic-moments-d113.md)'s 174 charts H_e, boundary balls
B_e=H_e(O_K), and 348 child maps. For each parent e, the balls
t_e^(-1) B_j of its two children partition B_e, and

    phi_(e,j)=H_e^(-1) t_e^(-1) H_j,       t_e in G.

Let V be the direct sum of rational functions in the chart variables
having no poles on their integration domains O_K. Define

    (A f)_j = sum_(e -> j) f_e composed with phi_(e,j).

For each harmonic basis index a, actual bounded integration Lambda_a
satisfies Lambda_a A=Lambda_a. D150 proposed finding a finite identity

    F = B + (1-A^tensor_d) H,                              (1)

where F represents a cleared residual, H is a finite tensor of rational
test functions, and B is a tensor of statewise constants with known
mass evaluation. Finite sums over the harmonic labels and tensor degrees
are allowed. No restriction on the pole set of H is imposed here.

## 2. Elementary boundary weights centered at a CM point

The retraction of p_i to the tree is the midpoint m_i of an edge. In its
t-coordinate the two central half-trees are A=pi O_K and its complement.
Assign each mass 1/2. At every step away from m_i, split a half-tree into
its two children of equal mass. Thus an outward cylinder at depth n has
weight 2^(-n-1), and its complement has weight 1-2^(-n-1).

This defines a rational-valued finitely additive weight rho_i on all
boundary balls. One can compute any ball's weight by its unique path
from m_i. Both outward and inward partitions obey additivity: for n>=1,

    2^(-n-1) = 2 * 2^(-n-2),
    1-2^(-n-1) = (1-2^(-n)) + 2^(-n-1).

At the central edge each reverse half-tree splits into two quarters.
The construction is invariant under every tree automorphism fixing m_i,
including G_(p_i). This is a combinatorial weight, viewed in C_p;
it is not a bounded p-adic measure. Its weights grow in p-adic absolute
value at increasing depths. Only finite sums of these weights are used.

## 3. Invariant principal-part functionals

For f in V put R_e(z)=f_e(H_e^(-1)z). Fix a CM label i and an integer r>=1.
For every pole q of R_e in G p_i, choose g_q in G with g_q p_i=q. Set

    L_(i,r)(f) = sum_e sum_(q in poles(R_e) intersect G p_i)
                   rho_i(g_q^(-1) B_e)
                   [w_i^(-2r)] (R_e composed with g_q).    (2)

This is a finite sum: every component has finitely many poles. The
coefficient is taken in the Laurent expansion at p_i in w_i. Replacing
g_q by g_q h with h in G_(p_i) changes neither factor: rho_i is invariant
under h, and an even Laurent coefficient is unchanged by w_i -> -w_i.
Thus (2) is well-defined. It is linear, including when poles cancel;
equivalently sum over the finite union of the pole sets, allowing zero
principal coefficients.

**Transfer invariance.** Consider one component R_e and a child j. Its
global child function is R_e composed with t_e^(-1). The pole q moves to
t_e q, and choose g_(t_e q)=t_e g_q. The Laurent coefficient in (2) is
then exactly the same as for R_e. Its weight is

    rho_i(g_q^(-1) t_e^(-1) B_j).

The two pulled-back child balls partition g_q^(-1) B_e. Their weights
add to its weight. Summing over poles and parents proves

    L_(i,r) A = L_(i,r).                                 (3)

If different parents contribute poles to the same child component,
linearity handles their cancellation. This proof applies to the summed
operator, without assuming separate branch closure or separate poles.

**Annihilation of polynomial moments.** A polynomial in a chart variable
has global poles only at H_e(infinity), a K-rational point. No point of
G p_i is K-rational. Consequently L_(i,r) vanishes on every chart
polynomial, including every statewise constant. This holds for all
degrees, not just the stored moment cutoff.

## 4. The CM kernels remain independent in this algebraic quotient

By [D114, section 4](dyadic-coarse-d114.md), the actual coarse coefficient
g_(i,n),a equals integration over the A-half-tree of the twice-A kernel

    2 K_n(t) = 1-((beta+t)/(beta-t))^(2n+2)
             = 1-w_i^(-2n-2).                           (4)

Transport it to the saved state by the exact D113 CM A-chart transport;
denote the resulting single-component vector by k_(i,n) in V. Its only
global pole is a G-translate of p_i. The pole coefficient in (4) is -1
and the pulled-back A-ball has rho_i-weight 1/2. Distinct CM orbits give

    L_(i,r)(k_(j,n)) = -(1/2) delta_(i,j) delta_(r,n+1).   (5)

The factor 1/2 is a boundary weight, not a numerical integration
approximation. The kernel includes the exact factor two of D114.

For any finite collection of these kernels, define separately for each
harmonic basis index a

    Lambda'_a = Lambda_a + sum_(i,n) c_(i,n),a L_(i,n+1).

Each Lambda'_a is transfer invariant and agrees with Lambda_a on all
chart polynomials. Equation (5) lets us assign its values on that finite
collection arbitrarily, by taking c=-2*(desired-original).
There is no assertion that Lambda'_a is continuous or an actual measure.
Indeed it cannot be a continuous extension when it changes a CM kernel
that has a uniformly convergent polynomial expansion in its A chart.

It follows that a nonconstant formal polynomial in these CM integrals
cannot have an identity of form (1) with a fixed known-mass right side.
Apply the tensor products of the Lambda'_a: the coboundary evaluates
to zero and B stays fixed, while the polynomial can vary arbitrarily
over its input values. The same argument also excludes finite sums of
legwise coboundaries. Allowing polynomial-moment tensors on the right,
with their exact values fixed, does not help: all such values are
preserved too. This conclusion concerns polynomial representations in
the indicated kernels; it makes no assertion about analytic completions.

## 5. A genuine first positive candidate residual

Select quadric index 0 in the frozen
[candidate file](../data/computed/cm_frame_curve_candidate.json), at
CM index 0 and coarse order 1. Use [D116, sections 6--7](cm-compound-height-d116.md)'s
integral cleared section q_Q=Q(s)/Delta, whose order-zero value is
already exactly zero. Its first coefficient has no unproved lower
positive-jet hypothesis.

Here is a small arithmetic circuit for that coefficient; it does not
expand an enormous tensor. Let z=e_0 be the leading harmonic evaluation
row, w its first coarse coefficient, and M the sixteen remaining
leading rows e_1,...,e_16. Put A=adj(M), D_0=det(M), and let A_i be its
columns. With V_i=(sigma_i(17 eta_j)) the exact residue frame, set

    c_0=D_0,     c_i=-z A_i,
    Phi=diag(c_1,...,c_16) M,
    Delta=D_0 product_i c_i,
    Q(sum_(i=1)^16 X_i V_i)=sum_(i<j) q_ij X_i X_j,
    s_i=sum_(j != i) q_ij.

There are no diagonal terms and sum q_ij=0, since Q vanishes on each
V_i and V_0=-sum_(i=1)^16 V_i. Differentiating D116's identity gives

    tau_Q = [u] Q((z+u w) adj(Phi) V_nonanchor) / Delta
          = -(1/D_0) sum_i s_i (w A_i) product_(a != i) c_a. (6)

Although (6) displays a denominator, D116's complementary-minor proof
shows that it is a polynomial in the evaluation and first-jet inputs.
It is homogeneous of total degree 240: each w A_i has degree 16, the
fifteen c-factors have degree 240, and D_0 has degree 16. There are
288 scalar inputs, from eighteen CM kernels paired with sixteen
harmonic basis functionals. No new evaluated jet is required.

**Nonconstancy with all frame denominators nonzero.** Specialize

    M=I_16,       z=(-1,...,-1),       w V_nonanchor=e_0.

Then every c_i, D_0 and Delta equals 1, Phi=I_16, and the argument of Q
is V_0+u e_0. Hence tau_Q=partial_(X0) Q(V_0). With w=0 it is zero.
V_nonanchor is invertible: the sixteen trace-centered coordinates form
a basis of the trace-zero subspace, so their seventeen conjugate rows
have the unique row relation sum V_i=0 and any sixteen are independent.

Source 629 evaluates Q(V_0)=0 exactly and finds partial_(X0) Q(V_0)!=0
in the degree-17 residue field. Its constant power-basis coefficient is

    -1319914447538691206632 / 11563101439788991.

The full seventeen-entry vector is saved, not a floating-point test.
Source 630 independently recovers this derivative as
(Q(V_0+e_0)-Q(V_0-e_0))/2 using the frozen D106 field multiplier.
It also checks the trace-zero basis rank and (6) against direct adjugate
evaluation in genera 3, 4 and 5, including its scaling degree g(g-1).

The specialization assigns formal integral values; it is not claimed
to be another Shimura curve or another bounded measure. Section 4 makes
both assignments available to invariant algebraic functionals with
exactly the same polynomial moments as the actual ones. Therefore the
nonconstant tau_Q cannot have a certificate (1). In particular a search
over larger finite rational pole sets cannot repair this route.

## 6. Why this does not contradict analytic determination

D113 determines the bounded moment solution uniquely and bounded
integration determines the CM coefficients from convergent expansions.
The functionals (2) vanish on those polynomial approximations but not
on their rational limit. They deliberately fail continuity. No new
bounded solution, numerical discrepancy or exact nonzero actual
residual has been constructed.

[Franc--Masdeu, section 4.2](https://arxiv.org/pdf/1201.0356) distinguishes
integration on locally constant functions from its extension to
continuous or locally analytic functions using boundedness and
convergent series. The present ramified setting uses D113's direct
boundedness argument. The principal-part construction and obstruction
above are companion derivations, not a theorem attributed to that paper.

The excluded class uses exact finite rational transfer identities and
fixed moment data. It does not include infinite convergent witnesses,
nonrational analytic witnesses, an effective tail-plus-height zero
argument, additional geometric relations not implied by transfer, or
a multiplication-compatible comparison of the actual and candidate
curves. Such an extension would need to state and use its additional
input; merely increasing the finite search depth is insufficient.

## 7. Verification and continuation decision

[Source 629](../pari/629_summed_transfer_obstruction.py) and
[source 630](../pari/630_summed_transfer_controls.py) supply exact
arithmetic witnesses, even-principal-part controls, rational boundary
partitions, and independent finite matrix checks. An explicit binary
leaf model checks the weight partitions and center swap. Odd Laurent
coefficients fail the stabilizer test, as required. These finite checks
do not mechanically prove the construction on every rational function
or the geometric hypotheses inherited from D112--D116.

The [fixed review](../data/computed/summed_transfer_review_d151.json),
[source ledger](../data/computed/summed_transfer_sources_d151.json) and
[completion record](../data/computed/summed_transfer_completion_d151.json)
bind this report, both finite jobs, their replays, and D150's transitive
provenance. Sources 629--631 and passing artifacts are frozen after
completion. The next unused source is 632. Every mathematical and review
job uses the 180-second private-process-group wrapper, at most three
workers, 2 GiB per worker/store and 6 GiB aggregate; this packet is
sequential. Ordinary entry-document edits need no mathematical rerun.

**Decision:** end the bounded finite rational witness investigation with
this obstruction. Do not start an unbounded witness search. A further
identification attempt must name additional analytic or geometric input,
or reassess the cost of the established sufficient precision/height
route. Such reassessment is not admission to compute a larger bank.
Retain the rank-45 or order-four implication as the identification target.
No P3200/higher bank, spectral or geodesic census, new level, Hecke
calculation or cubic search is admitted by this checkpoint. P32/B3,
the cover and canonical Hecke identification, torsion realization and
the field polynomial remain separate open obligations.
