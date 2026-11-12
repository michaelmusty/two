# D147: the canonical multiplication determinant in the residue frame

Continuation of the authorized proof-gap investigation.

**New geometric result:** canonical multiplication is surjective over the
stable dyadic model. Its reduction has rank 45, independently witnessed
by 45 pairs of graph cycles. The dyadic part of its cokernel length is
therefore zero.

The determinant calculation gives the exact identity

    h_ext(I_2) = -4F - delta - 60 log(2) + R - t_mu,             (1)

where F is the actual Faltings height, delta=(19/2)log(2), t_mu is the
nonnegative global multiplication-cokernel degree, and R is the combined
Mumford-metric, multiplication-volume and residue-frame comparison term
defined below. The previously proved lower bound on F gives

    h_ext(I_2) <= 44.411750955 + R.

Thus **R<=578 is sufficient** for the P1600 target h_ext(I_2)<=623.
This is an unevaluated sufficient condition, not a new numerical bound
on R or on the actual relation space. D142's bound 83240 remains the
best proved numerical upper bound in this investigation.

Two shortcuts fail. The determinant of the frame does not control its
action on the relation subspace. Also, the orbifold weight-four space
has dimension 72, not 45: it contains 27 additional elliptic principal
parts. Substituting its spectral determinant for the ordinary
bicanonical determinant would omit a nontrivial comparison.

No exact positive vanishing, candidate identification or field polynomial
follows. The recognized candidate's height is not used in this argument.

## 1. Integral multiplication and its metrics

Take a number field K over which the actual curve has a stable model
f:X->Spec(O_K). All arithmetic degrees are divided by [K:Q], and all
complex embeddings are counted. Set

    E=f_*omega,             rank 16,
    G=f_*(omega^2),         rank 45,
    A=Sym^2 E,              rank 136,
    mu:A->G,               J=ker(mu), rank 91.

E has the established (i/2) integral metric, so deg(E)=F. Stable
duality and base change make E and G locally free: on each stable
geometric fibre H^1(omega^2)=H^0(omega^(-1))^dual=0. The actual generic
multiplication rank is 45, already implied by the frozen rank-45 jet
constraint calculation. Section 3 below proves it again by reduction.
Consequently G/im(mu) is finite torsion and J is saturated in A.

Give A the quotient metric from E tensor E, and J its subspace metric.
For an orthonormal basis e_i of E, the ordinary symmetric monomials have

    ||e_i^2||=1,            ||e_i e_j||=1/sqrt(2), i<j.

There are 120 cross monomials. The algebraic determinant formula
det(Sym^2 E)=(det E)^17 therefore gives the metrized formula

    deg(A)=17F+60log(2).                                      (2)

The coefficient norm in D141 is instead the Euclidean norm in which
all 136 ordinary monomials have norm one. Section 4 retains that
difference. Source 617 checks the symmetric Gram determinant in ranks
2 through 6 using

    <e_i e_j,e_k e_l>=(G_ik G_jl+G_il G_jk)/2,
    det Gram(Sym^2 E)=2^(-g(g-1)/2)*(det Gram(E))^(g+1).

Choose any fixed Hermitian metric on G. For example, restrict the
orbifold Petersson metric to ordinary holomorphic quadratic
differentials. Write

    t_mu = degree of the finite module G/im(mu) >= 0,
    U_mu = average_sigma log(product of nonzero singular values of mu).

The singular values compare A/J with its quotient metric to G with
the chosen metric. Taking determinants of A/J ~= im(mu) gives

    deg(J)=17F+60log(2)-deg(G)+t_mu-U_mu.                       (3)

In particular, t_mu has a positive sign in deg(J) and a negative sign
in the eventual coefficient-height upper bound. Unknown odd-prime
lengths may safely be dropped for that upper bound. They must not be
replaced by the unrelated CM residue-map indices.

One direct check of (3) is useful. Let an integral rank-m matrix M
map an ambient lattice with Gram matrix S to a target with Gram
matrix H. Let B be a saturated integer kernel basis and let c be the
gcd of M's maximal minors. Then

    vol(mu)^2=det(H)*det(M S^(-1) M^t),
    det(B S B^t)=det(S)*vol(mu)^2/(det(H)*c^2).                (4)

Source 617 checks thirty nonsurjective integral examples with c>=6;
source 618 checks the determinant identity independently by Schur
complements in unimodular adapted bases. Omitting c or reversing its
sign fails these controls.

## 2. What the Mumford isomorphism does and does not provide

For the **unpointed stable coarse curve**, the algebraic Mumford
isomorphism is

    det(G) ~= (det E)^13 tensor O(-Delta).                    (5)

Here Delta is the nodal discriminant divisor, whose normalized degree
is delta=(19/2)log(2). In
[Freixas i Montplet, Theorem 4.5 and Lemma 4.6, n=0](https://arxiv.org/pdf/0803.2366v1),
the k=0 relation is lambda_1^12 ~= kappa tensor O(Delta), and
lambda_2 ~= lambda_1 tensor kappa. Combining them gives (5).
The algebraic trivialization of R^1 f_*omega is from Serre duality.
We give det(E) the existing Faltings metric, rather than silently
adopting a different determinant-of-cohomology metric.

Define its metric discrepancy in our conventions by

    A_2=deg(G)-13F+delta.                                    (6)

Equivalently A_2 is minus the averaged logarithm of the norm of (5),
oriented from its right side to its left, with the canonical section
of the discriminant line assigned norm one. Equation (5) alone says
nothing about the sign or size of A_2. In particular, setting A_2=0
would assert an isometry which has not been established.

Combining (3) and (6), our deduction is

    deg(J)=4F+delta+60log(2)-A_2+t_mu-U_mu.                   (7)

The combination A_2+U_mu is independent of the auxiliary metric on G.
For example, multiplying every norm on G by a>0 changes A_2 by
-45log(a) and U_mu by +45log(a). More generally the determinant of
any change of target metric cancels in the same way. One can choose
the multiplication quotient metric on G, in which U_mu=0, but then
A_2 is measured in that quotient metric. This does not make A_2 known.

## 3. Surjectivity at 2 from the actual stable graph

Use D99's actual geometric stable special fibre: thirty copies of P1
with forty-five nodes and a simple cubic dual graph. The graph and
its applicability to this curve are inherited geometric inputs.
The new calculation does not infer the special fibre from the candidate.

For canonical differentials, the three residues on each component sum
to zero, and residues on opposite branches are negatives. Thus
H^0(omega) is the graph cycle space, as in D116's integral lattice
argument. In characteristic two the incidence matrix has rank 29 and
its kernel has dimension 16.

There is an especially simple description of H^0(omega^2). On a
component, omega^2 restricts to O(2). Evaluation at its three distinct
attaching points is an isomorphism to three node fibres. The two
branches of a node have the same squared logarithmic differential:
(dx/x)^2=(-dy/y)^2. Hence a global quadratic differential is determined
by one arbitrary value at each edge. This identifies H^0(omega^2)
with k^45. Under these descriptions, multiplication is the
edge-by-edge product of two cycle residue vectors.

Source 617 computes the 45-by-136 product matrix from a basis of the
binary cycle space. A saved 45-column minor has determinant one.
It also checks every one-edge and two-edge deletion; none disconnects
the graph.

Source 618 gives a separate constructive certificate. For **each of the
45 edges e**, it finds two edge-disjoint paths between the endpoints
in the graph with e removed. Adjoining e gives simple cycles C_e and
D_e whose intersection is exactly {e}. Their residue-vector product
is the standard basis vector at e. Every path and every intersection
is checked and saved; this audit does not use the primary cycle basis
or its pivot minor. This proves surjectivity directly. With oriented
cycles it also works over arbitrary residue fields for this split
trivalent graph, although only characteristic two is needed here.

A separate cubic graph with a two-edge cut has two identical edge
functionals on its cycle space, and its product matrix is not
surjective. This rejects the inference that trivalence alone suffices.

Relative base change identifies the computed multiplication with the
reduction of mu over a stable dyadic DVR. Since E and G are free,
Nakayama's lemma proves

    mu is surjective over that DVR,     t_mu,2=0.             (8)

This persists under stable base change. D106's compatible rational
descent makes the dyadic primes conjugate after a Galois extension,
so (8) vanishes at every prime contributing to t_mu,2.

Nodal thicknesses do not change this reduction argument. The degree
245 evaluation defect, the local residue index from D119 and the
contents of individual candidate jets are different quantities;
none is a multiplication-cokernel length. Surjectivity here supplies
no new vanishing of a candidate quadric in characteristic zero.

## 4. Keep the rational residue-frame comparison

Let b=(omega_1,...,omega_16) be a representative of D106's rational
residue frame. It determines an isomorphism

    phi:Q^136 -> Sym^2 H^0(C,omega),
    ordinary monomial e_ij |-> omega_i omega_j as a tensor.

The actual coefficient relation space K_0=I_2 in D141 is phi^(-1)(J_Q).
Let w be the primitive integral Pluecker vector of K_0, and let
j=(wedge^91 phi)(w), a rational nonzero element of det(J). At a finite
prime p of the stable-model field let ord_p(j) be its order in the
determinant lattice det(J)_p; it may be negative. Put

    ell(j) = (1/[K:Q]) sum_p ord_p(j) log Norm(p),

    Theta_frame = ell(j)
        - average_sigma log(||j_sigma|| / ||w||_Euclidean).  (9)

Since deg(J)=ell(j)-average log||j_sigma|| and
h_ext(K_0)=log||w||_Euclidean, this gives exactly

    h_ext(I_2)=-deg(J)+Theta_frame.                          (10)

The finite orders and archimedean norms belong to the same rational
representative. Multiplying all omega_i by a common nonzero rational
scalar multiplies j by its 182nd power; the two resulting changes in
(9) cancel by the product formula. It is therefore legitimate to use
the projective residue frame, but illegitimate to declare its local
scalars units or drop its finite indices.

Nor can Theta_frame be recovered from the determinant of the full
16-dimensional frame alone. A simple control already occurs with
four basis vectors. Keep the intrinsic tensor

    q=e_0 e_3-e_1 e_2,

and change the frame to b_0=e_0+N e_1, b_i=e_i otherwise. The frame
determinant and its integral index are one, while

    q=b_0 b_3-N b_1 b_3-b_1 b_2,
    squared primitive coefficient norm=N^2+2.

Its intrinsic quotient-symmetric norm remains one. Thus coefficient
height is unbounded under determinant-one frame changes. Source 617
checks five values of N with the full transformed Gram matrix. This
is a linear-algebra control, not a counterexample to a CM-specific
height theorem or a claim that the actual residue frame varies freely.
It identifies the extra estimate such a theorem would have to supply.

## 5. The numerical budget and the orbifold mismatch

Set

    R=A_2+U_mu+Theta_frame.

Combining (7) and (10) proves (1). The nonnegative term t_mu can be
dropped when seeking an upper bound. D118's saved lower bound is

    F >= -16log(pi)+(-8+55817/54150)log(2).

It yields the certified known part

    -4F-delta-60log(2)
      <= 64log(pi)-(75/2+111634/27075)log(2)
       = 44.41175095412529... .                              (11)

Sources 617 and 618 enclose (11) independently with Arb at 192 and
224 bits. The remaining headroom to 623 is
578.5882490458747..., so R<=578 is a convenient sufficient condition.
Neither source claims that condition holds. The exact threshold
623.347163 from D141 could marginally enlarge the budget, but does
not resolve the missing comparison.

The tempting n=2 substitution into
[Teo's determinant formula, sections 5--6](https://www.imath.kiev.ua/~sigma/2021/083/sigma21-083.pdf)
does not compute A_2 here. Locally at an elliptic point of order m,
put w=z^m. The minimal invariant holomorphic quadratic differential
upstairs is

    z^(m-2) dz^2 = (1/m^2) dw^2/w.

It allows a simple pole on the coarse curve. Thus the orbifold
weight-four space is

    H^0(C,2K_C+B_ell),

where B_ell is the reduced divisor of all 27 elliptic points.
Riemann--Roch gives dimension 45+27=72. The desired G has dimension
45. The exact sequence of complex vector spaces is

    0 -> H^0(2K_C) -> H^0(2K_C+B_ell)
        -> H^0((2K_C+B_ell)|B_ell) -> 0.                     (12)

The last term has dimension 27. Its quotient metric, the determinant
of the inclusion and the corresponding integral lattices have not
been bounded. Equation (12) does not identify analytic torsions of
the two spaces; restricting the zero modes of an orbifold Laplacian
is not by itself a determinant formula for a different line bundle.
The earlier scalar spectral bound concerns n=0/1 and supplies none
of these missing n=2 comparisons.

## 6. Outcome and continuation

The generic determinant sequence is now normalized, including its
60log(2) symmetric-metric correction, finite-cokernel sign and rational
frame term. Its multiplication map is integrally surjective at 2.
The remaining task is quantitative: **bound the actual combined
comparison R by 578**, or give a different bound that implies the
existing coefficient-height target. The determinant identity alone
does not do so, and no new lower bound for F is being assumed.

The next bounded theoretical task is to estimate Theta_frame from
the actual CM evaluation/residue construction and A_2+U_mu in the
ordinary bicanonical multiplication quotient metric, retaining any
cancellations between them. D102/D103/D116/D119 supply integral
comparison data, but not a certified estimate meeting this budget.
Before using a spectral n=2 route, its 27 extra principal parts and
metric/lattice comparisons must be resolved. Exact structural
identification remains an alternative.

P1600 and column 0/P6400 are unchanged. The spectral-computation,
new-level, Hecke and cubic pauses persist. No new bank, eigenvalue
calculation or geodesic census is admitted. The later markings,
cover character, global cubic data and field polynomial remain
separate obligations after base identification. No new user decision
is needed for the continuing theoretical work.

## 7. Reproducibility

Sources 617 and 618 each pass a bounded job with one Sage child.
Their packets include all cycle witnesses, exact controls, outward
intervals, resource use and source hashes. Source 619 supplies the
fixed review, transitive replay, source-applicability ledger and
completion record. The seven project entry documents point to this
checkpoint. Sources 617--619 and passing artifacts are frozen;
source 620 is next unused.

The first final-review attempt stopped at a legacy status-format check:
D99 records `PASS`, while the review expected `pass`. Its receipt, log
and failed source snapshot are preserved. The corrected review checks
that older status explicitly. The primary and independent mathematical
calculations passed unchanged; this was not a failed rank or height
identity. Completion comprises five passing bounded jobs and that one
archived review failure.

The 180-second private-process-group cap, maximum three mathematical
workers, 2 GiB per worker/store and 6 GiB aggregate remain in force.
The graph checks and matrix controls do not mechanically prove the
stable-model, duality or Mumford theorems. Their application, the
height identity and the local orbifold calculation are the companion
mathematical arguments above.
