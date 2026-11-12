# D149: primitive normalization and the limits of cofactor cancellation

Date: 2026-10-09. Continuation of the authorized proof-gap investigation.

The primitive forward residue construction reproduces D148's upper
expression **15236.599070671391...**, hence the best proved actual
relation-height bound remains **15237**. Its small local residue index
does not supply a new global height saving.

Two further limitations are now explicit. With all other terms of this
estimate fixed, even the most favorable permitted pencil degree leaves
the majorant above 5132. Removing the entire positive field-vector term
as well still leaves it above **1162**, above the target 623. These are
lower bounds on this particular majorant, not on the actual relation
height. Also, vanishing on the marked points does not force a positive
power of the cofactor product to divide the forward rank-91 exterior map.

Neither limitation refutes the candidate or rules out a comparison using
additional information about the actual CM curve. Exact positive
vanishing, marked identification and the field polynomial remain open.
No harmonic precision, spectral calculation, level, Hecke or cubic search
is admitted here.

## 1. Retain the actual horizontal order and pencil line

Use D119's minimal regular model, finite flat Cartier divisor D, actual
horizontal order A, principal-parts module N, and pencil line Lambda.
Write lambda=deg(Lambda), H for the common absolute CM cotangent height,
F for the determinant L2 height, I for the unordered intersection degree,
and tau for the cohomology torsion degree. The metrics are those of
D119/D120: at infinity N is the direct sum of the seventeen tangent
fibres, and Lambda has its induced subline metric. The established
sequence and degree identity are

    0 -> Lambda -> N -> E^dual -> T -> 0,
    lambda = -17H+F+I+tau-average log vol(delta).              (1)

The Cartier and relative-duality hypotheses are the ones checked in
D119; see [Stacks, 0B9D](https://stacks.math.columbia.edu/tag/0B9D) and
[0E6N](https://stacks.math.columbia.edu/tag/0E6N). The new comparisons
below are our derivations, not statements quoted from those sources.

D146 proves that distinct order-two marks have no intersections at odd
primes: tame disks have a single elliptic section, and a wild S3 disk
at 3 has at most one coarse order-two section. Thus for D itself,

    I=(33/2)log(2),       tau >= (7/8)log(2).                  (2)

In particular A equals its split normalization away from 2. At 2 its
eight pair factors still impose differences divisible by beta^33;
v_beta(2)=16. This order is not the abstract degree-17 field order.

Let f_j=32 b_j^vee be D148's sixteen integral trace-dual field elements.
Their value vectors need not belong to A. However 8 f_j does: at 2
each value is divisible by beta^48, hence so is each pair difference;
away from 2 the order is already split. This provides an integral map

    P:E -> Lambda^(-1) tensor O^16,
    P_j(omega)=<256 b_j^vee, R_h(omega)>                       (3)

in a local generator h of Lambda. The expression is independent of h
as a map with the indicated line twist. Trace duality identifies it,
up to one common scalar, with the same fixed rational coefficient frame
as D148. It applies to the actual relation lattice J, without reading
candidate equations.

For a unit vector h at infinity, write r_i for its simple-pole coefficients.
Then sum |r_i|^2=1 and R_h(omega)_i=r_i e_i(omega). D117's bound
B=1/(sqrt(pi)*rho^2), rho^2=3/5, gives ||R_h||_HS<=B. If D2 is D148's
saved sum of squared trace-dual majorants, then

    ||P||_HS <= N_p=8 sqrt(17 D2) B.                          (4)

## 2. The normalization costs cancel exactly

In the dyadic generators, the primitive simple-pole coefficients have
valuations [2,-33,...,-33]. The ordinary entries are the unit values
of the primitive numerator a divided by the pair derivative 4 beta.
D116's cofactor coefficients have valuations [280,245,...,245]. Their
common difference is

    278=264+14,                                               (5)

the normalization index plus the principal-parts cohomology length.
Consequently P is 8 beta^(-278) times the old map in these line
generators, up to a unit. Its integral entries have content at least

    245-278+48=15.

On Sym^2 P restricted to rank 91 this gives finite index at least

    (2*91*15/16)log(2)=(1365/8)log(2).                        (6)

As in D148, this is a forward-frame index, not the multiplication
cokernel. D147's dyadic multiplication surjectivity persists.

The determinant-volume estimate already used in D120 is

    log vol(delta) <= 8log(17/16)+16log(B).

With D148's Hplus and Fminus it gives

    lambda >= lambda_min
      := -17Hplus+Fminus+(139/8)log(2)
           -8log(17/16)-16log(B).                            (7)

Retain D148's multiplication-image bound D_M and its quotient symmetric
metrics. The primitive forward bound is

    U_p=-182 lambda_min+D_M-17Fminus-60log(2)
          +182log(N_p)-(91/2)log(91)+(91/2)log(2)
          -(1365/8)log(2).                                  (8)

Subtract D148's expression. Every term cancels except the following
coefficient of log(2), which also vanishes:

    -182*(139/8)+182*3+22295/8-1365/8=0.                     (9)

Thus U_p=U_D148 exactly, before numerical evaluation. Replacing 245 by
the primitive index 16 while leaving the old line and norm unchanged
would not be a valid comparison. D120 had rejected the inverse-pencil
estimate; (9) now treats the forward map.

More generally let the old and new maps differ by k/alpha, with alpha
a section of Lambda tensor S. If a_f is its finite zero degree and
a_infty its mean logarithmic norm, then
lambda+deg(S)=a_f-a_infty. On a rank-r quadratic relation space the
volume changes by 2r(log|k|-a_infty), the index by
2r(log|k|-a_f), and the target twist by -2r(lambda+deg(S)).
Their sum is zero. Source 624 checks this identity symbolically for
arbitrary r. A change of normalization does not create a height gain.

## 3. A favorable pencil degree still cannot make this estimate suffice

There is a useful new lower bound on H from D146's odd intersections.
Let A_33 and B_23 be the total intersections at 3 of the order-three
pairs and the order-two/order-three pairs. D146 gives

    T_3=(4/3)A_33+(1/2)B_23 <= (27/2)log(3),

so B_23<=27log(3). D144's exact order-two adjunction, with D118's
complete dyadic correction, gives after averaging the seventeen marks

    H=2h_L-(35/34)log(2)-(4/51)B_23.

Hence, using both certified endpoints of D104's Hodge-height interval,

    Hminus := 2h_L^- -(35/34)log(2)-(36/17)log(3)
             =0.335546364783548... <= H <= Hplus.             (10)

No new odd-prime disjointness of order-two and order-three marks is
assumed; their entire allowed intersection is retained in (10).

For a primitive local pencil generator, take the product of all its
simple-pole coefficients. It defines a nonzero map from Lambda^17 to
the product tangent line, allowing poles of total degree 2I. At 2 the
finite zero degree after clearing those poles is D119's principal-part
norm, (1/8)log(2); the other finite zeros are nonnegative. At infinity
sum |r_i|^2=1 implies

    product |r_i| <= 17^(-17/2).

The product formula therefore yields

    lambda <= -H+(2I-(1/8)log(2))/17-(1/2)log(17)
            <= lambda_max
             := -Hminus+(263/136)log(2)-(1/2)log(17)
              = -0.411728709699408... .                      (11)

This is an upper bound on the actual pencil degree. It must not be
substituted for a lower bound in (8) to claim a better actual-height
upper bound. It instead diagnoses the best this formula could do if
only its pencil-degree estimate were improved.

Let K_0 denote all the fixed terms of (8) except -182 lambda_min.
To make -182lambda+K_0<=623 would require

    lambda >= (K_0-623)/182=24.366546943643208... ,            (12)

incompatible with (11). Even at the favorable endpoint lambda_max,

    -182lambda_max+K_0=5132.646168908356... .                 (13)

Deleting the entire positive field-size term 91log(D2) leaves

    1162.284678331332... >1162>623.                           (14)

The nonnegative nature of a replacement field term is justified by
D148: the sixteen nonzero algebraic integers 32 b_j^vee each have sum
of squared conjugate norms at least 17. Their trace-zero matrix has
operator norm squared at least 17. In a bound of the form sqrt(17 D2),
one cannot take D2 below 1. Removing its logarithm is already favorable.

Equations (13)--(14) are floors of this frozen majorant, retaining its
Hplus, Fminus, multiplication-jet constants and exterior norm estimate.
They are not lower bounds on h_ext(I_2), and do not exclude simultaneous
improvements to those other terms or a different comparison.

## 4. Vanishing on D does not force a forward cofactor-product factor

Let C be any integral nondegenerate curve in P(E^dual), and J its
quadratic ideal. If a linear map T on E has one-dimensional kernel
k ell, then

    ker(Sym^2 T)=ell E,       J intersect ell E=0.             (15)

For the second equality, a nonzero product ell*m vanishing on an
integral curve forces one of its factors to vanish on C. That would
place C in a hyperplane, contrary to nondegeneracy. Thus Sym^2 T is
injective on J even when T has corank one. This argument applies to
the actual nonhyperelliptic canonical curve as a linear-algebra fact.

An explicit characteristic-zero control also realizes this with a
cofactor map and the same dimensions 16,136,45,91. Put

    q(t)=1-(t^14+1) product_(a=1)^16(t-a)/16!,
    E_0=span(1,t,...,t^14,q(t)).

The projective closure of this parametrized curve is integral and
nondegenerate. Its products span 45 dimensions: powers through 28,
the fifteen q(t)t^i with distinct leading degrees 30,...,44, and q(t)^2
of degree 60. Its quadratic ideal therefore has dimension 91. These
quadrics are precisely the equal-power differences among the first
fifteen coordinates. No assertion that this control is the smooth
canonical CM curve is made.

Evaluate at t=0,1,...,16. Since q(0)=0 and q(a)=1 for 1<=a<=16,
the evaluation matrix has rank 16, with signed cofactor kernel,
up to a nonzero scalar,

    c_0=0,       c_a=(-1)^(a-1) binomial(15,a-1).

All sixteen other cofactors are nonzero. The cofactor-weighted map
has rank 15 and kernel q-1. By (15) its rank-91 quadratic exterior
map remains nonzero, although Delta=product c_i is zero. Varying the
last point near 16 makes the anchor cofactor nonzero: q'(16)!=0 and
the other fifteen evaluation rows give a Vandermonde minor. Thus this
is a specialization of actual projective frames on the same curve,
not a permanently degenerate configuration.

Source 623 verifies the rational polynomial and multiplication ranks,
then exhibits a nonzero rank-91 image minor modulo 31. Source 624 uses
direct multivariate polynomial substitution modulo 61 and independently
checks J intersect ell E=0 over Q. These controls support the proof;
they are not data about an actual CM degeneration.

Consequently no universal positive power of Delta divides this forward
exterior map merely because the quadrics vanish on the curve or on the
seventeen points. D116's inverse-frame identity Q(s)/Delta remains
valid; it concerns a different map. An actual CM-specific cancellation
would require an additional argument.

## 5. Price a dyadic-index refinement before admitting more computation

One further local bound can be obtained from existing exact indices.
At 2 put Z_0=ker(sum:R^17->R). D119 gives length(Z_A/Z_0)=264.
The columns eta_j generate a sublattice of Z_0 of index 632: the
embedding determinant of (1,b_1,...,b_16) has valuation
16*79/2=632 from the saved discriminant 2^79; centering the columns
and removing the constant column only introduces the unit 17.

Thus the determinant valuation of the coefficient pairing by 256 b_j^vee
on Z_0 is 16*128-632=1416, and on Z_A it is 1416-264=1152.
Composing with the primitive residue map of determinant index 16 gives

    v_beta det(P)=1168.                                     (16)

Every Smith exponent of P is at least 15 by section 2. The 136 Smith
exponents of Sym^2 P have total 17*1168=19856 and are each at least
30. For any saturated rank-91 source sublattice, its image index in
its saturated image is at most the sum of the largest 91 exponents:
a primitive exterior vector has a unit coordinate in Smith bases.
Consequently the actual relation-image index satisfies

    2730 <= t_(P,J),beta <= 19856-45*30=18506.                (17)

The extra dyadic saving beyond (6) is therefore at most

    (18506-2730)log(2)/16=986log(2)<684.                      (18)

Source 625 checks the determinant accounting, the equivalent old-frame
accounting, and a rational-series enclosure of log(2). This is an upper
bound on the possible saving, not a proved extra saving. It does not
bound uncomputed indices at odd primes. Computing more dyadic digits
solely to refine this index cannot by itself bridge D148's gap exceeding
14613. No such computation is launched.

## 6. Decision, next task and reproducibility

Close three isolated repairs of the current majorant: changing primitive
normalization, improving only the pencil degree and field-vector norm,
or improving only the dyadic frame index. The proposed universal forward
Delta cancellation is also invalid. These conclusions concern the
specified methods; the target h_ext(I_2)<=623 remains undecided.

The next theoretical task is an exact structural comparison: inspect the
saved candidate-scheme, canonical-model and correspondence certificates
for an automorphic identity or correspondence with a proved uniqueness
statement that can identify the actual marked curve. Reuse the existing
candidate-scheme checks. Candidate invariants, finite jet agreement and
candidate height alone cannot supply the missing implication. A new
height approach should first name the additional actual-curve input and
show where it enters, rather than reprice the closed scalar adjustments.

Sources 623 and 624 pass in 5.69 and 4.14 seconds. Their independent
192/224-bit ball evaluations agree; both rank-91 controls pass. Source
625 provides the fixed review, transitive replay, local index pricing,
source ledger and completion record. Five bounded jobs pass, with no
new failed attempts. The geometric applications remain companion proofs,
not machine-verified theorems.

The [source ledger](../data/computed/P1600_primitive_frame_sources_d149.json),
[fixed review](../data/computed/P1600_primitive_frame_review_d149.json) and
[completion record](../data/computed/P1600_primitive_frame_completion_d149.json)
bind D149 and its inherited provenance. Freeze sources 623--625 and
passing artifacts; source 626 is next unused. Seven entry documents are
updated. P1600, column 0/P6400, all resource caps and existing pauses
persist. No user decision is needed for the structural certificate audit.
