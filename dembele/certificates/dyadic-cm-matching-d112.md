# D112: dyadic CM coordinates, arithmetic labels and the rational residue frame

Date: 2026-09-25. Continuation authorized by “keep going!”.

The seventeen CM points now have explicit dyadic coordinates, certified
relative ideal classes, and a matching to the saved complex point and
polynomial-root labels. The saved rational residue basis is evaluated
at these roots with error at least **384 beta-digits**, or **192
pi-digits**. The sixteen actual harmonic measures also have certified
zeroth masses on all **51 CM boundary charts**. Positive-degree moments,
the harmonic-to-residue change of basis, an actual Shimura tangent/jet,
candidate identification and the target field polynomial remain open.

The arithmetic checks are independently replayable in rational Python.
The geometric interpretation uses canonical CM reciprocity and the
prime-to-p equivariance of Cerednik--Drinfeld uniformization, with the
local CM character specified below. Those theorems are mathematical
inputs, not consequences of numerical root matching or machine-verified
geometric proofs. The source roles are recorded in
[the D112 ledger](../data/computed/dyadic_cm_matching_sources_d112.json).

## 1. Fixed arithmetic and exact coordinates

Retain the notation of D109--D111:

    F=Q(b),   b^8-8*b^6+20*b^4-16*b^2+2=0,
    K=F_p,   pi=b,   v_pi(pi)=1,   v_pi(2)=8,
    lambda=2+b,   M=F(beta),   beta^2=-lambda,
    B=(-1,-1)_F,   k=ij,   R=O[1/b],
    G=R*/O_F[1/b]*,   Gamma=image(R^1).

The unique prime p_M of M above 2 is (beta), with norm 2, and
(2)=p_M^16. In M_p, use v_beta(beta)=1, so v_beta=2*v_pi and
v_beta(2)=16. In particular M_p/K is ramified quadratic and beta
does not belong to K. The minimal polynomial of beta is

    X^16+16*X^14+104*X^12+352*X^10+660*X^8
        +672*X^6+336*X^4+64*X^2+2.

[Source 407](../pari/407_dyadic_cm_embeddings.py) reuses D110's

    c=(b^7-7*b^5+14*b^3-7*b)/2,
    W=(1+b/2)*i+c*j,       W^2=-lambda.

The other sixteen embedded generators are both signs of the normalized
transports at D111's eight ordinary inverted edges, indexed
152,155,158,161,164,167,170,173. Their endpoint stabilizers are trivial.
The inverted edge 14, at the vertex with stabilizer order 32, is not
used for these sixteen entries; W supplies the remaining CM point.
Normalization is by an exact F-square root of Nrd(t)/lambda. Every
resulting generator v satisfies v^2=-lambda, and the full integer
ring O_M embeds in R under beta -> v. Its intersection with R is
therefore O_M[1/beta], by maximality away from p.

The splitting coefficients are represented exactly in
E=F[t]/(t^2+y^2+1), evaluated at the same local Hensel root t in K
as D109. If A is the matrix image of v, put

    S = [1, A00; 0, A10],       T=[0,-lambda;1,0].

Exact arithmetic proves det(S) is nonzero and A*S=S*T. Thus the
two fixed points are

    S*(beta:1) and S*(-beta:1),
    z=(beta+A00)/A10 on the first eigenline.

The eigenvalue on S*(beta:1) is beta. Both points lie in Omega_K
because beta is not in K. The packet saves the exact E coefficients,
their F-valued centers at D109's x0, and the t-slopes. The relative
lattice error lower bound is 173 at W and 166 at every other entry.
These bounds certify the associated tree lattices; they are not
assertions of 166 affine-coordinate digits after arbitrary divisions.

## 2. Why these are the ordinary CM points, and why W is the anchor

A G-element fixing a non-K eigenline also fixes its M_p/K conjugate,
since its matrix entries lie in K. It consequently lies in the
embedded torus M*. A representative q of its projective stabilizer
belongs to O_M[1/beta]*. At every finite prime q/bar(q) is a unit:
away from p this follows from localized membership, and at p it
follows because conjugation fixes the unique prime. At every complex
place its absolute value is one. Hence q/bar(q) is a root of unity.

M has exactly two roots of unity, as checked by 407. This also follows
from D105: M/Q is cyclic of degree 16 and ramified only at 2, and
complex conjugation is the eighth power of a generator. Its unique
quadratic subfield is real, so i is absent; a root of unity in M
must have 2-power order, hence can only be +1 or -1. Therefore q is
projectively 1 or v. Conversely v is a unit of the localized order.
Each fixed point has exact projective stabilizer order two, and
belongs to the known seventeen-point divisor D. None is the special
order-32 point P32.

At the anchor an especially simple witness is

    k in O*,   Nrd(k)=1,   kW=-Wk.

Both k and k^(-1) have integral order coordinates. Thus k exchanges
W's two eigenlines while belonging to Gamma, and these eigenlines
have the same image on C=G\Omega. This is not a claim that the two
fixed points of every other signed embedding have the same G-orbit.

D110's uniformization is over the completed maximal unramified
extension of K. Inertia therefore acts coefficientwise on this
presentation. The nontrivial automorphism of M_p/K exchanges W's
eigenlines and fixes the splitting coefficients in K. The image of
W is consequently fixed by K-inertia.

To pass from inertia to K-rationality, use the actual field of D.
By D105 it has splitting field H, the Hilbert class field of M,
with Gal(H/Q)=AGL1(F17). Since p_M=(beta) is principal, it splits
completely in H/M. Each completion H_P equals M_p and is totally
ramified of degree 16 over Q2. Thus decomposition and inertia have
the same action on D. Over K the remaining order-two action sends
class labels c to -c after choosing its fixed point as zero. It has
exactly one fixed point. W is that unique K-rational point of D.

There is also an independent polynomial check. Let

    f_L(X)=X^17-2*X^16+8*X^13+16*X^12-16*X^11
           +64*X^9-32*X^8-80*X^7+32*X^6+40*X^5
           +80*X^4+16*X^3-128*X^2-2*X+68.

Then g(X)=f_L(2X)/4 is integral and g(X)=1-X modulo 2.
Hensel gives one Q2-root theta0 of f_L with v2(theta0)=1.
The Newton polygon puts the other sixteen roots at v2=1/16.
Since K has value group (1/8)Z, theta0 is the unique root in K.
D106's unique residue-algebra identification sends W's image to
this root.

## 3. Local branch and Artin direction

D107's saved reference is complex point 8, whose polynomial root is
root 2, the unique real root. Its CM eigenvalue has negative complex
imaginary part. To compare with the dyadic realization, choose the
place of H above 2 at which this reference root becomes theta0.
It is unique: the local decomposition group, of order 16, is the
stabilizer of one of the seventeen roots.

Normalize the local embedding of M by the CM eigenvalue character
at the W anchor: beta is the eigenvalue on S*(beta:1). This states
which local CM branch is used; a complex imaginary sign is not a
2-adic sign convention. The two embeddings of M_p over K exchange
beta and -beta, and conjugate both the signed point list and the
root labels. They must not be applied to only one of those lists.
The chosen embedding of M together with theta0 determines the
embedding of H, since H=M L and the degrees 16 and 17 are coprime.

For an ideal a of M and an embedded torus iota, the arithmetic Artin
convention is

    iota(a)R=xi R  =>  Artin(a): P -> xi^(-1)P.          (1)

This is the convention already used for D59/D107. The canonical CM
reciprocity law is described for totally real base fields in
[Voight, section 4.3](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf);
the inverse-principalizer formula appears explicitly in
[Voight, Theorem 5.1 and Algorithm 5.2](https://jvoight.github.io/articles/shimcm-fixed-errata.pdf).
We use that CM law, not the triangle-group analytic algorithms or
the separate descent discussion in the latter article.

For the localized formula, take a representative prime to p and
apply the same torus action on the prime-to-p adelic coordinate.
The Cerednik--Drinfeld presentation retains this coordinate and its
action; replacing iota(a)R by xi R moves the local eigenline by
xi^(-1) after the diagonal B* action. This proves (1) in the dyadic
presentation with the normalized CM character. The adelic setup and
uniformization used here are
[Dembélé, section 4.1, Theorem 4.3 and Proposition 4.4](https://arxiv.org/pdf/1906.06772).
Because p_M is principal, localization loses no ideal class. The
ramification of M_p/K does not change this prime-to-p calculation.
No theorem restricted to an inert quadratic extension of Qp is
substituted for it. No new explicit unramified-descent matrix is needed.

For each embedded generator v, let u=1 at W and u=v+W otherwise.
Exact arithmetic gives v*u=u*W. Source 407 computes the lattice
intersection {x in M : u*iota_W(x) in O}, then its O_M ideal span a.
The two lattices agree away from 2. The certificates prove localized
inclusion and

    N_M/Q(a)*N_F/Q(Nrd(u)) = 1 at W, 128 otherwise.

The norm identity and inclusion imply equality of the right ideals
at every prime away from p. Therefore

    iota_W(a)R=u^(-1)R.

In (1), xi=u^(-1), so the point with embedded generator v=uWu^(-1)
is Artin([a]) of the anchor. This geometric step is an application
of reciprocity, not a guess from equal quadratic polynomials.

[Source 408](../pari/408_dyadic_cm_class_witnesses.py) supplies a
direct exact witness a=z*G0^c for every entry, where the saved class
generator is G0=(31,beta+16). Review 410 verifies every relation by
unimodular comparison of rational lattices. The classes cover all
of C17, proving that the seventeen resulting points are distinct.

## 4. Dyadic roots and an independently fixed class orientation

[Magma 409](../magma/409_dyadic_cm_root_proposals.m) proposes rational
power-basis centers for all seventeen roots in M_p. These centers
are not trusted as root or labeling certificates. For each center a,
[review 410](../pari/410_dyadic_cm_matching_review.py) independently
checks v_beta(f_L(a))>2*v_beta(f_L'(a)). The root-error lower bound
is at least 688; the largest valuation of a difference between two
centers is 17. Their Hensel disks are disjoint and account for all
roots. Root index 0 matches the independent rational theta0 center.

The exact automorphism sigma(beta)=beta^3+3*beta has order 16 and
sigma^8(beta)=-beta. Source 408 supplies a principal-ideal witness
for sigma(G0) being in class G0^10. Rational review checks the
witness and that 10 generates F17*. Applying sigma to the root
centers gives one fixed root and one cycle of length 16.

The known affine Galois action now determines its regular normal
C17 subgroup: choose a nonzero class for one point in the 16-cycle;
successive points must have labels multiplied by 10. The sixteen
initial choices rescale these labels, and give the sixteen nonidentity
translations as prospective class-one generators. This uses D105's
actual AGL1 group and the certified ideal action, not a fit to an
arbitrary permutation.

Let f be the arithmetic Frobenius of the prime (31,beta-19), of
class 3. D107 proves the exact identity

    sum_j r_j^2*r_f(j) = gamma(beta),

where gamma has ascending power coefficients

    [-10,28,-218,-15,-559,-114,-558,-119,
     -264,-55,-59,-12,-5,-1,0,0].

It also proves that the sixteen nonidentity translations give the
sixteen distinct conjugates of this resolvent value. Review 410
compares all sixteen class-label choices with gamma, using certified
root errors and exact separation of gamma's conjugates. Exactly one
choice matches. The cubic expression has error at least 688 because
the roots are integral. The inverse Artin cycle fails the separation
test. An altered root also fails its Hensel test.

The resulting table is below; every index is zero-based. “Edge +/-”
refers to 407's exact chosen normalization, not a real sign of its
dyadic value.

| CM index | Embedded generator | Ideal class | Saved complex point | Saved complex root | Dyadic root |
|---:|:---|---:|---:|---:|---:|
| 0 | W | 0 | 8 | 2 | 0 |
| 1 | edge 152 + | 15 | 11 | 5 | 8 |
| 2 | edge 152 - | 2 | 14 | 6 | 7 |
| 3 | edge 155 + | 7 | 7 | 14 | 9 |
| 4 | edge 155 - | 10 | 0 | 13 | 10 |
| 5 | edge 158 + | 1 | 5 | 16 | 2 |
| 6 | edge 158 - | 16 | 2 | 15 | 1 |
| 7 | edge 161 + | 5 | 6 | 9 | 15 |
| 8 | edge 161 - | 12 | 1 | 10 | 16 |
| 9 | edge 164 + | 8 | 12 | 11 | 6 |
| 10 | edge 164 - | 9 | 13 | 12 | 5 |
| 11 | edge 167 + | 11 | 10 | 8 | 11 |
| 12 | edge 167 - | 6 | 15 | 7 | 12 |
| 13 | edge 170 + | 13 | 16 | 0 | 4 |
| 14 | edge 170 - | 4 | 9 | 1 | 3 |
| 15 | edge 173 + | 3 | 4 | 4 | 13 |
| 16 | edge 173 - | 14 | 3 | 3 | 14 |

## 5. Residue-frame values and actual chart masses

Use exactly the sixteen trace-centered basis polynomials stored at
`field_basis.trace_centered_basis_power_coordinates[1:]` in
[cm_field_recognition.json](../data/computed/cm_field_recognition.json).
They are not replaced by an assumed pure-power basis. D106 identifies
their embedding values with the projective residue frame, up to the
common scalar permitted there. Review 410 evaluates all 17*16 entries
at the matched dyadic roots with rigorous error at least

    384 beta-digits = 192 pi-digits = 24 binary digits.

The coefficients' minimum v2 is -1; the available root-error bound
688 absorbs this denominator loss. Rational truncated arithmetic
certifies each truncation and all trace-zero column sums. These are
algebraic residue-frame values, not evaluations of the actual
harmonic differentials or their change-of-basis matrix.

For eta1=theta-2/17 the anchor has

    v2(eta1(theta0))=7,   v_pi=56,   v_beta=112.

At the other sixteen points its v_beta is 1. The anchor's extra
cancellation must be retained in subsequent error bounds for divisions.

In each exact S coordinate, use D108's boundary charts

    A: z=pi*x,       B: z=1+pi*x,       C: z=1/(pi*x),
    x in O_K.

Review 410 checks that the F-valued centers of the chart lattices
have the same exact lattice classes as S and its three neighbors.
It invokes D111's certified reducer to obtain all sixteen measures'
zeroth moments on these 51 balls. For every point and basis measure,

    A0=0,       B0+C0=0.

The result includes nonzero B0 values. The involution z -> -lambda/z
exchanges the A ball with its complement; invariance and total mass
zero explain A0=0, also at residue characteristic two since the
coefficient field has characteristic zero. These zeroth masses are
actual arithmetic measure data. No positive-degree moment is computed.

## 6. Audit, failure record and next bounded task

Sources 407/408/409 passed on their first attempts in
11.46/5.77/1.54 seconds. The first independent-review probe failed
after 24.51 seconds: an extra expected-valuation assertion incorrectly
treated eta1 at the anchor as having v_beta=16. The actual additional
cancellation gives v_beta=112. The failing source snapshot, log and
receipt are retained; it produced no result artifact. The corrected
review derives the valuation from the independent rational root center.
The second probe passed in 29.90 seconds and also certified the
zeroth chart masses. These were all runner-272 jobs with private
process groups and a 180-second termination cap.

The final
[D112 review artifact](../data/computed/dyadic_cm_matching_review_d112.json)
binds this report, the reference ledger, all new sources, artifacts,
successful probe evidence and the archived failed attempt. It checks
all **661 D111 source hashes unchanged**. Its execution receipt records
the final runtime; the receipt is kept separately to avoid a circular
hash. Freeze sources 407--410 and bound files after successful review.
Recheck without Sage or Magma, through bounded runner 272:

    python3 dembele/pari/410_dyadic_cm_matching_review.py --check

The next task is a finite transport/recursion for positive-degree
moments in these actual CM charts, with a proved truncation and
contraction bound over ramified K, followed by a small bounded pilot.
D111's d=0 and the matched coordinates are now available for D108's
conditional tail formulas. Direct exponential Riemann refinement is
not the high-precision plan. A Qp overconvergent control theorem or
the inert-31 comparison thresholds cannot be transferred unchanged.

The actual harmonic-to-residue change of basis, cofactor normalization,
Gaussian pivot and dyadic equality thresholds remain subsequent gates.
D99's nonhyperellipticity result and D108's rejection of the unchanged
absolute spectral comparison stand. Keep the class-census, new-level,
Hecke-bank and cubic-precision pauses. Downstream marking, global
sections, norm-97 separation and target-scale torsion remain separate.
No correspondence was sent.
