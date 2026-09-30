# D102: the integral defect of the CM residue frame

Date: 2026-09-24. Continuation of the D101 arithmetic-normalization task.

**Result:** the previously unspecified residue-frame index has an exact
local formula. It is the sum of a principal-part norm valuation and a
cohomology-torsion length. The two terms are independent requirements.
An explicit fixed smooth curve shows that the index can grow at a good
prime even when the marked divisor is etale and the cohomology term is
zero. A separate exact calculation settles the trace-lattice conversion
for our saved degree-17 field order: its trace-dual lattice is cleared by
32, and the saved trace-centered basis needs the common factor 17 to
enter that lattice.

These are new formulas, controls and field arithmetic. They are **not a
bound for the actual Shimura frame**, an independently evaluated tangent,
or a curve identification. No candidate equations or jets are inputs to
the new calculation. D101's analytic-exactness gate remains unmet.

## 1. A local integral formulation

Work over a DVR R with fraction field K. Let f:X->Spec(R) be a proper
flat Gorenstein family of geometrically connected curves of genus g.
Assume H0(O_X)=R, H1(O_X) is free of rank g, and use its relative-duality
identification with the dual of E=H0(omega_X/R). Let D be a finite flat
relative effective Cartier divisor of degree g+1, with generically
reduced fibre, such that

    H1(X_K,O(D_K)) = H0(X_K,omega(-D_K))^dual = 0.

Write A=H0(O_D), N=H0(O_D(D)), and T=H1(X,O_X(D)). The module N is an
invertible A-module; A is semilocal, so we may trivialize N over A.
The module T is finite torsion. The principal-parts exact sequence gives

    0 -> Lambda -> N --delta--> E^dual -> T -> 0,
    Lambda = H0(O_X(D))/R.

Here Lambda is a free rank-one R-module. Choose its primitive generator
h modulo constants, and let a be its image in N. Since N/Ra is the
image of delta in a free module, a is primitive as an R-vector. Also
assume a is a unit in N over the generic algebra A_K. For a single
closed generic point D_K, this last assertion follows because the
nonconstant h has polar divisor exactly D_K. For a split divisor it
must be checked separately.

The correct residue lattice is

    Omega_A = Hom_R(A,R),
    Z = {lambda in Omega_A : lambda(1)=0}.

Under the generic trace pairing, Omega_A is the codifferent of the
order A and Z is its trace-zero part. It is generally not the
trace-zero part of A. Adjunction identifies
omega_X/R|D with Hom_R(N,R). Under this identification, delta^dual
is differential restriction to D. Multiplication by the principal part
a gives the integral residue map

    R_h : E -> Z,  omega |-> Res_D(h*omega).

The structural inputs are relative duality for Gorenstein curves
([Stacks, 0E6N](https://stacks.math.columbia.edu/tag/0E6N)),
Cartier-divisor adjunction and its principal-parts sequence
([0B4A](https://stacks.math.columbia.edu/tag/0B4A)), and the finite
dualizing module Hom_R(A,R)
([0BUK](https://stacks.math.columbia.edu/tag/0BUK)). The index formula
below is our deduction from these sequences. Application at the actual
bad fibre requires checking these model and divisor hypotheses; the
generic Shimura curve alone does not establish them.

## 2. Exact index formula

Let T^D=Ext1_R(T,R), which has the same length as T. Then there is an
exact sequence

    0 -> T^D -> coker(R_h) -> coker(a^*:N^dual -> A^dual) -> 0.

Consequently, after any A-trivialization of N,

    length_R coker(R_h)
      = length_R T + v_R(det_R(m_a))
      = length_R H1(X,O_X(D)) + v_R(Norm_(A_K/K)(a)).       (1)

The determinant is unchanged up to a unit by changing the trivialization.
The norm here is of the principal part in that trivialization, not a
norm of a CM-field generator. Formula (1) also works for a product
generic algebra.

Proof: put I=im(delta). Dualizing 0->I->E^dual->T->0 gives

    0 -> E -> I^dual -> T^D -> 0.

Dualizing 0->Ra->N->I->0 identifies I^dual with
Ann(a)={lambda in N^dual:lambda(a)=0}. The diagram

    0 -> Ann(a) -> N^dual --evaluation at a--> R -> 0
           |          |                         |
           v          a^*                       identity
    0 -> Z      -> A^dual --evaluation at 1--> R -> 0

has exact rows: both a and 1 are primitive R-vectors. Its snake lemma
identifies coker(Ann(a)->Z) with coker(a^*). The map a^* is generically
invertible, and hence injective over R. Factoring R_h through Ann(a)
proves the claimed short exact sequence. The elementary-divisor
formula for a square matrix over a DVR gives (1).

In particular, the residue frame is integral and unimodular if and only
if both T=0 and a generates N over A. Generic nonspeciality gives
neither conclusion on every special fibre. For an unramified local
field algebra A/R, R-primitivity makes a a unit; it still does not
remove the possible T term. For split A, a may be primitive while
vanishing modulo the uniformizer in one component.

If the resulting index ideal is J, it annihilates the local cokernel,
so J*Z is contained in R_h(E). This supplies a sufficient clearing
ideal once J is bounded. To globalize, retain the pencil lattice
Lambda: the intrinsic map is Lambda tensor E -> Z. A chosen global
representative h introduces its own local scaling factors unless it
generates that lattice. Neither those factors nor J are known for the
actual arithmetic curve.

## 3. A geometric control at a good prime

Over R=Z_5, keep the single smooth genus-two curve

    y^2 = x^5-x+1.

Its finite branch polynomial has derivative -1 modulo 5; its usual
odd-degree model has one smooth point at infinity. For any n>=1 put
q=5^n and choose the Hensel root y_n=-1 mod5 satisfying
y_n^2=q^5-q+1. Mark

    P1=(0,1), P2=(q,y_n), P3=(1,1), D=P1+P2+P3.

The three reductions are distinct, so D is split etale and its residue
algebra R^3 has discriminant a unit. Since deg(D)=3>2g-2=2,
H1(O(D)) vanishes on every fibre and T=0. In the integral differential
basis dx/y, x*dx/y and parameters x-x(P_i), the restriction matrix is

    E_D = [ 1       0    ]
          [ 1/y_n   q/y_n]
          [ 1       1    ].

A primitive generator of the principal-parts kernel is

    a = (q-1, y_n, -q).

Thus, in the basis (1,0,-1),(0,1,-1) of the trace-zero lattice, R_h has
matrix

    [ q-1  0 ]
    [ 1    q ].

Its determinant has valuation exactly n. This proves an unbounded
residue index on a fixed smooth curve with a fixed split etale residue
algebra, despite T=0. The marked divisor varies. These are local split
divisors, not the degree-17 CM closed point; this is not a counterexample
to a CM-specific height theorem or to a bound using heights of the
marked points. It rules out a deduction from good reduction, etaleness
and generic nonspeciality alone.

Script 378 verifies the Hensel roots, restriction and residue matrices
at n=1,2,4,8,16 with eight additional 5-adic digits. The formula above
is exact for every n; the finite computations are controls of it.
Additional abstract integral matrices exercise nonzero T independently
and reject the index formula with that term omitted. Those matrices
are not asserted to all arise from curves.

The phenomenon also occurs on a fixed nonhyperelliptic curve. Over Z_17
take the smooth plane quartic x^4+y^4=1 and put q=17^n. There is a
unique Hensel root r=4 mod17 of r^4=1-q^4. At

    (1,0), (-1,0), (r,q), (0,1),

choose unit local trivializations so that the canonical restriction
matrix has rows (1,x,y). Its signed cofactors are

    (r+1-q, 1-r-q, -2, 2q).

The first three are units and the fourth has valuation n. One maximal
minor is the unit -2, so T=0, while (1) gives residue index valuation n.
The points have distinct reductions. The plane quartic remains smooth
and nonhyperelliptic, and the residue algebra remains R^4. Script 379
checks this additional family at n=1,2,4,8,16. Thus nonhyperellipticity
does not supply a missing integrality implication either. These remain
split local divisors, not CM counterexamples.

## 4. The degree-17 field contribution is now explicit

The saved arithmetic audit supplies Elkies's degree-17 polynomial;
the saved field-recognition record supplies the basis b_0=1,b_1=theta,
...,b_16. Script 378 independently checks irreducibility modulo 31,
all 153 unordered basis products, and the trace Gram matrix. Thus
the lattice B spanned by this basis is an integral order. We do not
need, or newly claim, maximality.

Its exact trace data are

    disc(B) = 2^79,
    Tr(b_0)=17, Tr(b_1)=2, Tr(B)=Z.

Let B^vee be its trace dual, B_0=ker(Tr:B->Z), and
Z_B=ker(Tr:B^vee->Z). The inverse Gram matrix has common denominator
exactly 32. In particular 32*B^vee is contained in B.

The saved frame basis is eta_i=b_i-Tr(b_i)/17. It satisfies

    17*span_Z(eta_i) subset B_0 subset Z_B,
    [Z_B:B_0] = 2^79,
    [B_0:17*span_Z(eta_i)] = 17^15,
    [Z_B:17*span_Z(eta_i)] = 2^79 * 17^15.

These indices are checked by exact determinants. To verify saturation
of B_0, use the trace-one element b_0-8b_1 and the trace-zero vectors
-2b_0+17b_1, b_i-Tr(b_i)*(b_0-8b_1) for i>=2. This change of integral
basis is unimodular. Pairing those vectors with b_1,...,b_16 gives
their coordinates in Z_B. For the scaled eta_i the coordinate matrix
is 17*G_ij-Tr(b_i)*Tr(b_j), with i,j>=1.

The common factor 17 is minimal for placing all the unscaled eta_i
in B^vee: pairing eta_1 with b_1 has denominator 17. Common scaling
does not change the projective canonical frame, so this factor is a
normalization that can be fixed explicitly.

This removes an abstract-field ambiguity; it does not compute (1).
Even after identifying F(D) with F*Frac(B), the actual horizontal
order, normal module N, principal part a and cohomology T require
arithmetic geometric input. At the dyadic place, tensoring the known
order with O_F must not be silently identified with the integral
closure or the horizontal divisor's order. The integer 32 is **not**
a clearing bound for the unknown Shimura tangent.

## 5. The archimedean comparison has a concrete determinant

Let E_sigma be the (g+1)-by-g matrix of canonical differential values
at the conjugates of D, with compatible local trivializations. Define
its signed maximal minors

    c_i = (-1)^i det(E_sigma with row i deleted),  i=0,...,g.

Assume all c_i are nonzero. The cofactor identity gives c^t E_sigma=0.
Put H=diag(c_i)*E_sigma and delete row r to obtain the square H_r.
Then

    det(H_r) = (-1)^r product_(i=0)^g c_i.                (2)

If V is the matrix of conjugate values of the desired trace-zero
field basis, the residue-frame change is M=H_r^(-1)*V_r; the omitted
row follows because both column sums are zero. This uses a generator
c of the principal-parts line, so it determines the required frame
up to a common scalar.

For B=max_ij |(H_r)_ij|, Cramer's rule gives the explicit sufficient
bound

    ||M||_infinity <= g! * B^(g-1) * ||V_r||_infinity
                       / product_i |c_i|.               (3)

Every cofactor of H_r has at most (g-1)! terms, which proves (3).
Certified lower bounds for all |c_i| and upper bounds for the entries
therefore suffice for an archimedean change-of-frame bound. A nearly
singular frame cannot be controlled by entry upper bounds alone.
Formula (3) must be tied to the same arithmetic representative and
metrics as the finite-place calculation before being used in D101's
height inequality. Arbitrarily scaled numerical differential banks do
not supply that comparison.

Row rescaling by s_i and differential-basis change by U send
c_i to det(U)*(product s_j)/s_i*c_i. Hence H changes to
det(U)*(product s_j)*H*U, and the resulting differential frame changes
only by a common scalar. Script 378 checks this covariance, (2), the
Cauchy--Binet identity det(E^t E)=sum c_i^2 on rational controls,
and (3) in ranks 2 and 16. The Cauchy--Binet control uses real matrices;
the complex Hermitian version would use absolute squares.

Over a split DVR, the gcd of the maximal minors is a generator kappa
of Fitt_0(T), and c=kappa*a up to a unit after primitive normalization.
Thus (2) and (1) describe the same restriction matrix but different
normalizations. Dropping the common divisor kappa without tracking
the integral lattice would lose the T contribution.

## 6. What is still needed on the actual Shimura curve

The task is now more specific than applying an intrinsic CM-height
formula directly to a coordinate:

1. On an actual integral marked model, bound the principal-part norm
   and the Fitting ideal of H1(O(D)), including the pencil lattice and
   comparison with the chosen horizontal order. These determine the
   finite residue-frame defect by (1).
2. Certify the archimedean evaluation minors in a compatible arithmetic
   normalization, or derive an arithmetic-intersection bound controlling
   the same quantities. Equations (2)--(3) expose the necessary lower
   bounds; the old empirical condition numbers do not supply them.
3. Combine those inputs with D101's canonical-height and Gaussian-norm
   comparisons. Clearing the frame alone does not bound a tangent
   ratio's denominator: its chosen Gaussian denominator also needs
   control, or the projective-height certificate must be instantiated.

Zhao's CM height and Yuan's curve height remain possible inputs to
such an intersection estimate. No theorem reviewed so far directly
bounds these two marked-frame defects in our normalization. The
arithmetic Gaussian-restriction alternative remains available, but
still requires actual global section restrictions on a CM test object.
Neither route has been instantiated by this calculation.

The next continuation should attempt a bound or exact arithmetic
calculation for these defects on C_ar, beginning with the geometric
principal-parts/cohomology map, rather than recomputing the now-settled
field trace lattice. The independence, CM-label and nonspeciality
hypotheses remain explicit. Another spectral pilot, coefficient lift,
or larger Hecke bank is not justified by this result alone.

## 7. Reproduction and scope

Recheck the exact arithmetic and controls:

```sh
python3 dembele/pari/378_cm_residue_lattice.py --check
python3 dembele/pari/379_cm_residue_lattice_review.py --check
```

The initial calculation took 0.56 seconds under a 180-second private
process-group timeout. The review uses a second trace computation and
fraction-free determinant checks, binds this report and the source
ledger, and checks that the earlier D101 inputs remain unchanged.
Its exact computation is not a formal verification of relative duality
or of this geometric proof. All new target-status flags remain false.
Completed sources 378--379 and bound artifacts are frozen after the
review. Earlier bound outputs, enumeration limits, cubic precision,
and target-torsion status are unchanged. No correspondence was sent.
