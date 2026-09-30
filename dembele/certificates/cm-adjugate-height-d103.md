# D103: an integral adjugate bound for the CM tangent

Date: 2026-09-24. Continuation of D102, authorized by “continue”.

**Result:** one can avoid separately bounding the residue-frame index
in D102 when bounding the *height of a tangent ratio*. Keep the frame
inverse in adjugate form. Its determinant is common to all canonical
sections and cancels from every Gaussian ratio. This also avoids a
quantitative lower bound for the evaluation minors in this height
argument. An arithmetic displacement estimate supplies uniform local
analytic bounds at the seventeen CM points. Together they give

    h(v_j) <= 513*H_CM,disk + 8400.                         (1)

Here H_CM,disk is the normalized arithmetic degree of the **stable
coarse-canonical fibre at the actual CM point**, with the disk metric
specified below. Formula (1) is conditional on the arithmetic field
labels, the projective-frame condition and a nonzero chosen Gaussian
denominator. It is **not yet a numerical height bound**: H_CM,disk has
not been bounded. No independently evaluated tangent or identification
of the candidate is claimed. D102's index theorem remains valid.

## 1. Arithmetic lines, without inverting an integral frame

Let g=16. After a finite extension K/F, split the actual CM divisor as
D=P_0+...+P_g and take the stable model f:C->Spec(O_K). Write

    E=f_*omega_C/O_K,             W_i=P_i^*omega_C/O_K.

The module E is locally free of rank g; the W_i are invertible modules.
All evaluation maps e_i:E->W_i are integral. The sections P_i may meet
at bad primes. No etaleness of their union or identification of its
horizontal order is required here. Stable base change gives the same
normalized fibre degrees after further extension. Equivalently, one
can use the minimal regular semistable model: contraction of its
unstable chains is crepant for the relative dualizing sheaf.

Equip E with the inner product (i/2) integral omega wedge conjugate(eta).
The normalized arithmetic degree of det(E) is then h_Fal(C). Our
convention agrees with Javanpeykar's sections 2.1--2.3, including the
induced determinant metric. All complex embeddings are counted, so a
nonreal conjugate pair contributes twice.

Put

    c_i=(-1)^i det(e_k)_(k != i),
    S=(tensor_i W_i) tensor (det E)^(-1).

Each c_i is a section of (tensor_(k != i) W_k) tensor (det E)^(-1).
The cofactor identity sum_i c_i e_i=0 gives an integral map

    Phi:E -> S tensor U,    U=ker(O_K^(g+1) --sum--> O_K).

Assume every c_i is nonzero on the generic fibre. This is the
projective-frame hypothesis; rank(Evaluation)=g alone is weaker.
Deleting row r identifies U with O_K^g, and gives

    Delta_r=det(Phi_r)=(-1)^r product_i c_i.

The line on each side is S^g tensor (det E)^(-1), after fixing the
standard determinant of the deleted-row coordinates on U.

Let eta_j be the sixteen saved trace-centered field-basis elements.
Under the intended *arithmetic* identification and labelling of the
CM residue algebra, set

    V_ij=sigma_i(17*eta_j),       sum_i V_ij=0.

D102 proves 17*eta_j integral in the saved degree-17 field order.
Thus these vectors are integral over O_K. This uses the arithmetic
CM-field identification as a hypothesis, not merely the numerical
matching of seventeen complex points.

Define

    T=S^(g-1) tensor (det E)^(-1),
    s_j=adj(Phi_r) V_(j,r) in E tensor T.                  (2)

The adjugate is polynomial in the entries of Phi_r, so (2) is integral
at every finite place. Generically, s_j=Delta_r Phi_r^(-1)V_(j,r).
The latter inverse differs from the intended residue-framed canonical
basis only by a common scalar: both weight evaluation by the unique
relation between the g+1 evaluation rows. The factor 17 is also
common. Gaussian ratios of the s_j therefore equal the intended
tangent ratios. Changing the deleted row changes every s_j by the
same sign.

This does not prove Delta_r nonzero. Once nonvanishing holds, however,
neither a lower bound for |Delta_r| nor its finite valuations are
needed in the height calculation. They can still matter for a separate
numerical inversion or nonvanishing certificate.

## 2. The Gaussian map is integral on the stable model

For an invertible sheaf L, local sections f*l and g*l give the first
Gaussian expression (f*dg-g*df)*l^2 in Omega^1 tensor L^2. The expression
glues: the derivative of a change of local generator cancels. On a
nodal family there is an integral map Omega^1_C/O_K -> omega_C/O_K.
In an etale nodal chart xy=a its formula, using xi=dx/x=-dy/y, is

    dx |-> x*xi,             dy |-> -y*xi.

It respects y*dx+x*dy=0 and agrees with the usual map on the smooth
locus. Invertibility and base change of omega follow from the
Gorenstein duality statement in
[Stacks, 0E6N](https://stacks.math.columbia.edu/tag/0E6N).
This local description proves the needed integral extension; no
division by 2 or the residue characteristic occurs.

Taking L=omega gives an integral Gaussian map to omega^3. Applying it
to the sections in (2), then restricting at P=P_k, gives

    G_bj(P), G_ba(P) in W_k^3 tensor T^2.

For G_ba(P) nonzero, v_j=G_bj(P)/G_ba(P). The projective-height formula
for two integral sections of this common arithmetic line gives

    h(v_j) <= 3*h(W_k)+2*h(T)
              + average_sigma log max(||G_ba(P)||,||G_bj(P)||).  (3)

The exact formula subtracts the degree of their common finite zero
ideal. Dropping that nonnegative term proves (3), even if the sections
have many common zeros at bad primes. This is the reason a separate
residue index or Gaussian denominator bound is unnecessary here.
The Gaussian sections themselves have not been computed.

## 3. Upper norms suffice

Suppose ||e_i||<=B_i in the stated metrics, and put Bcal=product_i B_i.
Hadamard gives ||c_i||<=product_(k != i) B_k. Every row of Phi_r has
norm at most Bcal. In orthonormal coordinates every adjugate entry has
absolute value at most Bcal^(g-1). If |V_ij|<=V, then

    ||s_j|| <= g^(3/2)*V*Bcal^(g-1).

If the Gaussian evaluation operator wedge^2(E)->W_k^3 has norm at
most Gamma, its value on any pair of these sections is at most

    Gamma*g^3*V^2*Bcal^(2*(g-1)).                         (4)

The points P_i form one arithmetic Galois orbit. With compatible
metrics they all have the same normalized degree H=h(W_i). Since

    T=(tensor_i W_i)^(g-1) tensor (det E)^(-g),
    h(T)=(g^2-1)*H-g*h_Fal(C),

(3)--(4), with a uniform B, imply

    h(v_j) <= (2*g^2+1)*H - 2*g*h_Fal(C)
              +3*log(g)+2*log(V)+2*(g^2-1)*log(B)+log(Gamma). (5)

All the frame determinants have been retained in arithmetic lines;
none has been treated as an archimedean unit or discarded from a
finite-place denominator calculation.

## 4. A uniform embedded disk at every order-two CM point

The arithmetic inputs are those of D57--D58 and D90--D92: F has degree
8; B is split at one real place and definite at seven; O is maximal;
pi=2+b is totally positive of norm 2; and the order-two CM points come
from embeddings beta in O with beta^2=-pi. The positive normalizer
group Gamma^+ contains Gamma^1=O^1/{+1,-1} with index two. The CM
element beta represents the nontrivial coset and fixes its CM point p.

The normalizer assertion for beta follows locally: away from the
dyadic place it is a unit of the maximal order, and at that division
place the maximal order is unique. D92's full unit signatures remove
the ambiguity from totally positive units. These properties hold for
each CM embedding, not just the enumerated reference point. D58's
canonical-conjugation argument transports them to the other complex
embeddings of the arithmetic curve; the split real place is transported
too. We do not keep the old split place while conjugating B.

For alpha in O^1 put

    q=(alpha-beta*alpha*beta^(-1))/2,      v=Nrd(q).

Then q belongs to (1/2)O, so 4*v is in O_F. At each compact place the
orthogonal CM decomposition gives 0<=v_tau<=1. At the split place,
if alpha moves p, the disk/SU(1,1) calculation gives

    v_split=-sinh(distance(p,alpha*p)/2)^2 < 0.

Thus 4*v is a nonzero algebraic integer and

    1 <= |Norm_F/Q(4*v)| <= 4^8*|v_split|,
    distance(p,alpha*p) >= 2*asinh(2^(-8)).                (6)

Since beta fixes p and generates Gamma^+/Gamma^1, their orbits of p
are the same. Therefore (6) holds for every normalizer translate that
moves p. Take the unit-disk coordinate z centered at p and rho=2^(-10).
Its hyperbolic radius is r=2*atanh(rho), and

    sinh(r)=2*rho/(1-rho^2)=2048/1048575 < 1/256.

Consequently 2*r is strictly smaller than every nonzero displacement
in (6). The disk |z|<rho is embedded in the quotient modulo the
order-two stabilizer z->-z. This is a uniform proof for all seventeen
CM points and their conjugates. It uses neither a polygon certificate
nor a new norm-one enumeration, and is deliberately weaker than the
large reference-point disk available from D92.

## 5. The metric and the numerical constants

At a CM point set u=z^2, a coarse coordinate, and define ||du||=1 on
the canonical fibre. A centered uniformizing disk coordinate is unique
up to phase, so this metric is intrinsic to the given orbifold
uniformization. At finite places use the stable **coarse** dualizing
lattice W=P^*omega. Its normalized degree is H_CM,disk. This is not
being identified with an orbifold or arithmetic Hodge height.

For omega=(sum_(m>=0) a_m*u^m)du, its pullback is
2*z*sum a_m*z^(2*m) dz. The coarse disk has half the upstairs integral,
and angular orthogonality gives

    ||omega||_L2^2 >= pi*sum_(m>=0) |a_m|^2*rho^(4*m+4)/(m+1).

Thus the coefficient functionals a_0,a_1 have norms at most
1/(sqrt(pi)*rho^2), sqrt(2)/(sqrt(pi)*rho^4). Their exterior product
is Gaussian evaluation in the metric ||(du)^3||=1. We may take

    B=2^20,             Gamma=2^60.                      (7)

These are actual operator upper bounds from the arithmetic disk, not
empirical condition numbers. No unknown periods enter them.

For the saved degree-17 polynomial h, the exact inequality
sum_(i<17) |h_i|*4^i < 4^17 puts every root inside |theta|<4.
Applying this to each saved eta_j gives

    |sigma(17*eta_j)| <= 17*sum_k |eta_(j,k)|*4^k < 2^35.

The ceiling of the largest rational upper bound is 18,666,352,210.
Script 380 stores all sixteen exact bounds and checks the relation
17*eta_j=17*b_j-Tr(b_j), using the already verified D102 field order.
Consequently V=2^35 is valid under the arithmetic labelling hypothesis.

Substituting g=16 and (7) into (5) yields

    h(v_j) <= 513*H_CM,disk - 32*h_Fal(C) + 10342*log(2).

Use the universal lower bound h_Fal(C)>=-16*log(2*pi), in the matching
L2 normalization: Bost's bound as stated in Javanpeykar,
[*Polynomial bounds for Arakelov invariants of Belyi curves*,
Lemma 2.4.4](https://msp.org/ant/2014/8-1/ant-v8-n1-p04-s.pdf).
No Belyi-degree upper bound is used. Since pi<4 and log(2)<7/10,

    10342*log(2)+512*log(2*pi)
      < 11878*log(2) < 8314.6 < 8400.

A positive rational Taylor sum for exp(7/10) certifies the logarithm
inequality. This proves (1), with no floating-point rounding dependency.
An upper bound for the Faltings height of the genus-16 curve is no
longer a required input to this route.

## 6. What is still needed

The numerical input still missing from (1) is an upper bound for
H_CM,disk on the actual stable coarse curve. Zhao's
[Theorem 1.1 and section 6](https://arxiv.org/pdf/2309.08886)
give an arithmetic Hodge height at quaternionic level; the common
dyadic ramification is allowed. Our normalizer quotient has genus 16,
whereas the norm-one curve has genus 40. A comparison must track the
integral models, the ramification at the CM section, and the metric.

Generically the double cover has u=z^2 at this point. If an integral
leading-coefficient map W_C(P)->W_S(Q)^2 existed on the chosen models,
it would give a useful height inequality in compatible disk metrics.
The generic coordinate identity does **not** establish that integral
map at the bad fibre. In particular, a stable section can meet a node,
and the wild dyadic quotient must be compared with the Hodge model.
We have not proved H_CM,disk<=2*h_Hodge(Q), or any corrected numerical
version of it. Zhao's compatibility in the level tower alone does not
resolve this normalizer/coarse-model comparison.

The arithmetic field labels, all nonzero evaluation minors, and the
chosen nonzero Gaussian denominator remain explicit hypotheses.
Their qualitative nonvanishing has not been upgraded by the toy
matrix checks. No new spectral pilot is justified by (1) alone; D98's
full enclosure still contains zero. The candidate curve remains
unidentified, and exact cubic construction, norm-97 separation,
target-scale torsion and the final field polynomial remain separate.

**Next task:** establish the intrinsic coarse-canonical/Hodge CM-height
comparison, especially at 2, and evaluate its upper bound. Keep the
180-second private process-group cap and the existing resource pauses.
Do not resume the per-prime residue-index or minor-lower-bound search
merely to instantiate (1); this argument has removed that requirement.

## 7. Checks and preservation

Script 380 checks adjugates, deleted-row compatibility, common-factor
Gaussian cancellation, basis/fibre covariance, and a rank-only negative
control in ranks 2, 3 and 16. A growing-index family keeps integral
adjugates while inverse denominators tend to infinity. Integral nodal
identities include a nonzero characteristic-two control. Exact field,
radius and constant calculations use rational arithmetic throughout.
These controls support the proof; they are not actual Shimura matrices.

The first 0.04-second job rejected the artificial genus-two jet because
its value and derivative rows were accidentally proportional. Its
source snapshot, log and receipt are preserved. Replacing those toy
jets with a pair having nonzero bracket made the 0.24-second rerun
pass; it changed no theorem or input arithmetic. No old bound source
or artifact was modified.

Audit 381 independently uses Bareiss determinants and rational linear
solves on a dense Vandermonde frame, a Horner field bound and an
independent integration/constant calculation. It binds this report,
the source ledger, the successful run and the failed-source snapshot,
and checks that D102's twelve and D101's twenty-two bound source hashes
are unchanged. Recheck with:

```sh
python3 dembele/pari/381_cm_adjugate_height_review.py --check
```

The completed sources and bound artifacts are frozen. Decisions,
references and entry documents are updated. No external correspondence
was sent.
