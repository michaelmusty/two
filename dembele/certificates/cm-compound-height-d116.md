# D116: integral quadric jets and an arithmetic identification criterion

Date: 2026-09-26. The user authorized continuing the reassessment without
approval stops.

The preferred certificate now tests the candidate's **quadratic sections
directly**. It avoids Gaussian denominators and the separate rank-45
requirement. Integral complementary-minor identities give sufficient
successive vanishing bounds of **119806, 120284 and 120758** in normalized
beta-valuation. The existing computations give lower bounds
**3794, 3745 and 3728**. Thus no positive jet has been proved exactly zero,
the candidate is not yet identified, and the target field polynomial
remains unconstructed.

We have also computed the third actual coarse jet from the frozen
precision-200 moment bank, proved that the harmonic differentials form
an integral stable-model basis, and reduced the alternative two-order
ratio-equality thresholds to beta-errors **132444/524481**. These are
sufficient bounds, not minimum precision requirements. In particular,
the direct-section valuations and ratio-error digits are different quantities.

The local data now suffice for the preferred four-coefficient test.
Its remaining obstacle is exact vanishing at attainable cost. A small
precision increase is not the main next task. Section 10 gives the
revised continuation plan.

## 1. Fixed inputs and normalization

Keep the actual genus-16 quotient C, its compatible rational descent,
the transitive degree-17 CM divisor D, and the rational residue frame
from [D99](hyperellipticity-review-d99.md),
[D105](cm-frame-arithmetic-d105.md),
[D106](cm-rational-frame-jets-d106.md) and
[D112](dyadic-cm-matching-d112.md). None is inferred from the candidate
quadrics in this work. The nonhyperellipticity proof remains D99's
arithmetic reduction-graph obstruction.

Write F=Q(b), b^8-8b^6+20b^4-16b^2+2=0, and
M=F(beta), beta^2=-(2+b). Normalize v_beta(beta)=1, so
v_beta(2)=16 and v_beta(b)=2. The splitting field H of the CM residue
polynomial is the Hilbert class field of M, of degree 272 over Q,
with Gal(H/M)=C17. The degree-17 residue field is denoted L, not M.

Over a field splitting D and giving stable reduction, use the integral
lines and metrics of [D103](cm-adjugate-height-d103.md):

    E = H^0(omega),  rank E=g=16;       W_i = omega|P_i;
    S = (tensor_(i=0)^g W_i) (det E)^(-1);
    c_i = signed maximal evaluation minor omitting P_i;
    Phi = (c_i e_i)_i : E -> S tensor ker(sum);
    Delta = det(Phi with one row deleted) = +/- product_i c_i;
    T = S^(g-1) (det E)^(-1);
    V_ij = sigma_i(17 eta_j),             sum_i V_ij=0;
    s_j = adj(Phi) V_j in E tensor T.

Every c_i and Delta is generically nonzero. Changing the omitted row
changes all s_j by a common sign. This construction is equivariant
under the arithmetic CM labels. It does not license treating an
arbitrary projective scalar as an integral unit.

The already proved uniform inputs, with their original metrics, are

    H_CM = h(W_i) < 41/10,
    h_Fal(C) >= -16 log(2*pi) > -48 log 2,
    ||e_i|| <= B=2^20,       |V_ij| < V=2^35.

The CM-height comparison is [D104](cm-intrinsic-height-d104.md).
Its geometric, Hodge-height and metric inputs remain part of the proof;
finite matrix checks do not replace them.

## 2. Integral compound cancellation and ratio-height bounds

For a square matrix A and every k, Jacobi's complementary-minor identity is

    wedge^k adj(A) = det(A)^(k-1) * complementary_(g-k)_minors(A),

with the appropriate transpose and signs. One proves it first for an
invertible matrix over the universal fraction field and then as a
polynomial identity over Z. It is therefore valid integrally at nonunit
determinants and on singular matrices. The classical determinant method
is discussed by [Aitken](https://doi.org/10.1017/S001309150000794X).

Consequently the reduced exterior products

    v_k = (s_j1 wedge ... wedge s_jk)/Delta^(k-1)

are integral in wedge^k E tensor S^(g-k) (det E)^(-1).
Cauchy--Binet, Hadamard, and ||V_j||<=sqrt(g)*V give strict binary
norm exponents 5139, 4838, 4536 for k=1,2,3. Source 433 checks the
bookkeeping and 1946 complementary-minor identities, including singular
and nonunit controls; an extra power of Delta is explicitly rejected.

The D103 disk of radius rho=2^-10 has coarse parameter u=z^2.
Its coefficient functional a_k has norm at most
sqrt(k+1)/(sqrt(pi)*rho^(2k+2)). Thus Gaussian evaluation has norm
below 2^60. The three-by-three Wronskian has norm below 2^120:
the product of the derivative bounds has constant 2*sqrt(6)/pi^(3/2)<1.
Their integral extensions at a node use D=x*d/dx-y*d/dy and the
dualizing generator dx/x. Exterior alternation cancels the derivatives
of changes of generator. No division by a bad-prime determinant occurs.

Let f,a,b be the local coefficients of s_1,s_2,s_j, and put
G=f*a'-a*f', H=f*b'-b*f'. Then

    G*H'-H*G' = f * Wr(f,a,b).
    gamma=G/Delta,  kappa=Wr(f,a,b)/Delta^2.
    a_(j,1)=H_reduced/gamma,
    a_(j,2)=f^3*kappa/(2*Delta*gamma^3).

The second numerator and denominator are integral in the same line
W^9 S^(4g-6) (det E)^(-4); their strict binary norm exponents are
20133 and 20135. Before finite common-zero subtraction, this gives

    h(a_1) <= 9881/10 + 5618 log 2 < 4883,
    h(a_2) <= 40795/10 + 23111 log 2 < 20099.

These are bounds for the actual unknown coefficients. The candidate
heights 677/1947 enter only in the final difference bound. Section 5
subtracts certified finite common contents.

## 3. The harmonic lattice is the stable integral differential lattice

An integral-valued harmonic basis need not be a saturated basis.
Source 436 separately replays Smith reduction on the D111 16-by-174
matrix. All sixteen Smith factors are one. Its saved 355 unimodular
operations certify index one in the integer kernel of the harmonic
relations. A control with primitive rows but index two prevents the
incorrect row-by-row primitivity inference.

Saturation in tree coordinates alone is still insufficient. For an
oriented noninverted quotient edge e, let d_e be its stabilizer order.
The ordinary graph flow attached to a tree cocycle is c_e/d_e.
Indeed there are |Gamma_v|/d_e lifts at a vertex, and division of the
tree conservation equation by |Gamma_v| gives graph conservation.
Source 437 reconstructs the 73 edges on 58 vertices from D111, computes
their d_e, and compares these weighted flows with the sixteen fundamental
integer cycles of a 57-edge spanning tree. The change matrix and its
inverse are integral; its determinant is -1.

Here is the geometric lattice comparison, rather than an assumption
that invariants commute with reduction. D99's Kurihara input gives a
proper nodal quotient with rational normalized components. Noninverted
nodes have local equation xy=uniformizer^d_e; inverted intervals are
removed. [Nekovar, section 1.5.3](https://doi.org/10.4153/CJM-2011-077-6)
states this integral quotient description and the stabilizer thicknesses.
The Kurihara scanned pages were verified in D99; this turn's attempted
refetch returned HTTP 429, and is not recorded as a new reading.

For a split nodal model all of whose normalized components are P1,
annular residues define an integral map

    H^0(omega_R) -> H_1(graph,R).

At xy=a, a regular dualizing differential is a regular function times
dx/x, with integral Laurent residue. On reduction, the map is the
usual residue map on each normalized component. A differential on P1
with at most simple poles is uniquely specified by its residues, whose
sum is zero. Opposite branches have opposite residues. This identifies
the reduced space with graph cycles. Proper duality and base change
make H^0(omega_R) free of rank g; Nakayama now proves that the integral
residue map is an isomorphism. The relevant dualizing line is invertible
and compatible with base change for nodal families
([Stacks, 0E6N](https://stacks.math.columbia.edu/tag/0E6N)).

For the finite quotient of a noninverted annulus, pullback multiplies
the residue by its degree d_e. This is a characteristic-zero residue
identity on the generic annulus, valid even when the residue
characteristic divides d_e. D108's Poisson differential has tree
residue c_e. Its downstairs residue is therefore c_e/d_e. The
unimodular weighted-cycle witness above proves that the sixteen
computed differentials are an integral basis of H^0(omega_R).
Contraction of rational tails and subdivision chains preserves global
differentials and graph cycles, so this is also the stable lattice.

This is a mathematical deduction from the integral uniformization model
and the finite witnesses. Source 437 explicitly does not claim machine
verification of the uniformization or duality theorem.

## 4. Integral canonical fibres and evaluation contents at 2

Source 438 verifies that deleting any one of the thirty vertices of
the stable cubic graph leaves it connected. Any residue triple of sum
zero on a component can consequently be completed to a graph cycle:
join the other endpoints by paths in the graph with that vertex removed.
Thus global differentials restrict to the full O(1) on each stable P1.
A cycle through a node gives a nonzero residue there, and subdivision
components carry generated O(0). Nakayama proves that evaluation
E -> W_i is surjective, including for sections specializing to nodes.

The minimum valuations in the actual leading harmonic rows are

    m_i = [296, 33, ..., 33].

Since these differentials are an integral basis and evaluation is
surjective, beta^m_i du is an integral generator of the corresponding
canonical fibre. The normalized D115 evaluation rows therefore are
integral rows in actual fibre bases, not arbitrary analytic scales.

The determinant of the sixteen non-anchor rows has valuation 280.
The coefficients q=h_W*D_matrix^(-1) all have valuation -35. It follows
that the seventeen evaluation cofactors have valuations

    [280, 245, ..., 245],
    v_beta(Delta)=4200.

The evaluation map's saturation defect has normalized valuation 245;
its primitive relation has valuations [35,0,...,0]. The D103 sections
and the D115 residue-framed sections differ by the common scalar
-17*Delta/c_W, of valuation 3920. These assertions are independently
checked in 440/445.

**This is not the index of D102's horizontal CM residue map.** The
horizontal order, point intersections, principal-parts lattice and
possible H^1 torsion have not been calculated. No conclusion about
that separate index is drawn from the number 245.

## 5. Finite common-zero subtraction for the ratio method

The reduced integral Gaussian vector has beta-valuation lower bounds

    [3577, 3694, ..., 3694].

They use the shift 2*3920-4200-3*m_i from raw coarse Gaussians.
The common lower bounds for the integral second-ratio numerator and
denominator are

    [14881, 15298, ..., 15298].

Source 439 uses the Wronskian expression. Review 440 instead uses
f^2*(G*H'-H*G') and checks all 255 numerator bounds independently.
W's Gaussian remains numerically unresolved; this computation only
uses lower bounds and never inverts it.

The full beta polynomial is Eisenstein with constant term 2, so
Norm_M/Q(beta)=2 and M's unique prime above 2 is principal. It splits
completely in the Hilbert class field H/M, by the principal-ideal
kernel of the Artin map
([Milne, Class Field Theory](https://www.jmilne.org/math/CourseNotes/CFT.pdf)).
There are seventeen primes of H over 2, each with e=16 and f=1.
The C17 action simultaneously permutes these primes and the CM points.
The natural cofactor construction is equivariant up to signs. Hence
the seventeen values at one completion enumerate the valuations at
all seventeen primes for one fixed CM point. Further stable-model
extension scales the numerator and field degree equally.

In D103's exact projective-height formula, the common finite zero
degree can therefore be decreased from the upper bound by

    (62681/272) log 2  for the first ratio,
    (259649/272) log 2 for the second ratio.

All other finite common zeros are discarded. This gives actual heights
below 4723 and 19438. With the D106 candidate heights and the
height-of-a-difference inequality, the sufficient degree-16-place
beta-errors are **132444/524481**, or sufficient integer pi-errors
66222/262241. Rational logarithm enclosures and an independent binary
logarithm series certify every rounding.

The local degree-16 place of L is one place, not sixteen independent
places. The seventeen primes of H just used belong to the separate
global averaging argument. The achieved ratio errors remain 101/70.

## 6. A sharper direct integral quadric identity

Let Q be any one of the 91 integer candidate quadrics. It vanishes on
every certified frame row V_i. Then

    q_Q = Q(s_1,...,s_g)/Delta

is an integral section of 2*omega tensor U, where

    U = T^2/Delta = S^(g-2) (det E)^(-1).

The following explicit identity proves both integrality and a useful
norm bound. Trivialize the input lines and omit row 0. Let M be the
g-by-g matrix of evaluation rows e_1,...,e_g, let A=adj(M), and
write A_i for its columns, v=e_0, and D_0=det M. Then

    c_0=D_0,       c_i=-v*A_i for i=1,...,g,
    Delta=D_0*product_(i=1)^g c_i,
    adj(Phi)_i=(product_(k!=i) c_k)*A_i.

The transformed quadratic form Q(sum_i X_i V_i) has no diagonal
terms, since Q(V_i)=0. Write its cross coefficients as q_ij.
They satisfy sum_(i<j) q_ij=0 because sum_(i=1)^g V_i=-V_0.
In Sym^2 E, put

    T_ij=(product_(a not in {i,j}) c_a)*A_i*A_j.

For distinct i,j,k one has the integral identity

    (T_ij-T_ik)/D_0
      = (product_(a not in {i,j,k}) c_a)*A_i*
          (c_k*A_j-c_j*A_k)/D_0.                    (1)

The last quotient is contraction with -v of
(A_j wedge A_k)/D_0, which is an integral complementary minor of M.
Fix any reference pair. Every other pair is connected to it by at
most two pairs sharing an index. Since sum q_ij=0, subtracting the
reference T in the sum expresses q_Q as a sum of the integral
differences (1). This proves the claimed division without inverting
an integral determinant. Covariance gives exactly the line U above.

Hadamard bounds |c_i|<=B^g and ||A_i||<=B^(g-1).
A fixed complementary two-column wedge has norm <=B^(g-2), so
its contraction with v has norm <=B^(g-1). Every expression (1)
has norm <=B^((g-2)(g+1))=B^238.

Let L_Q be the sum of the absolute integer coefficients of Q.
The transformed cross coefficients satisfy
sum|q_ij|<=g*(g-1)*L_Q*V^2. Thus

    ||q_Q as a tensor|| <= 2*g*(g-1)*L_Q*V^2*B^238 < 2^4855,  (2)

since max L_Q=42550. These are bounds in the induced quotient norm
on Sym^2 E. Sources 441 and 444 check polynomial pencils, integral
division, and the adjacent-pair identities, including rejection of a
quadric not through the full frame.

An earlier, valid Cauchy-pencil estimate in source 441 gave exponent
6389 and threshold 147023. Source 444's explicit identity supersedes
that bound. The earlier artifact remains frozen and is not the
current recommendation.

## 7. Successive integral vanishing jets, including nodal specializations

Q vanishes exactly on D, so q_Q(P_i)=0 is already known. Suppose its
coarse jets through order n-1 vanish exactly at a CM point. Its next
divided derivative defines a canonical integral element

    tau_n(Q,P_i) in W_i^(n+2) tensor U.                (3)

At a smooth point, ordinary divided derivatives are integral Taylor
coefficients. At a node xy=a, take lambda=dx/x=-dy/y and
D_lambda=x*d/dx-y*d/dy. For every integer m, including negative m,
binomial(m,n) is integral. Therefore binomial(D_lambda,n) preserves
the local integral ring. Its difference from D_lambda^n/n! is a
linear combination of lower derivatives. On evaluating at a section
where those derivatives vanish exactly, the divided derivative is
integral. This argument also applies to the completed nodal chart.

Changing the generator lambda or the local coefficient of q_Q changes
the n-th derivative by its expected leading factor plus lower jets.
Those lower jets are zero by hypothesis, proving that (3) is intrinsic.
In particular this proof does not divide an arbitrary dyadic derivative
by 2 or 6 and assert integrality. The hypotheses are sequential:
tau_2 needs tau_1=0 exactly; tau_3 needs both preceding positive jets
to vanish exactly. A finite zero-containing ball does not establish
either hypothesis.

For Taylor coefficients of products, the disk functionals from section 2
give strict binary bounds 2^60, 2^81, 2^102 for orders 1,2,3.
For example their constants are 2*sqrt(2)/pi,
(2*sqrt(3)+2)/pi and (4+2*sqrt(6))/pi, respectively; the last two
are safely bounded by 2 and 4. Combining (2)--(3), a nonzero tau_n
has normalized finite zero degree at most

    alpha_n + beta_n log 2,
    alpha_n=(240+n)*41/10,
    beta_n=4855+[60,81,102]_n+720.

The line degree is (240+n)*H_CM-15*h_Fal(C). At the seventeen
dyadic primes, if the sixteen non-anchor valuations are at least N
and the anchor valuation is at least A, the finite contribution is
at least (16*N+A)*log(2)/272. The Galois argument of section 5 applies
to these natural sections as well. Consequently the strict inequality

    (16*N+A)*log(2)/272 > alpha_n+beta_n*log(2)          (4)

proves tau_n=0. This is a section zero bound, not a ratio reconstruction
bound. With A=0, sufficient N are 120029,120487,120945. The actual
anchor lower bounds improve them as shown in section 8.

If (4) proves all three successive positive jets zero for every Q,
then Q(s) vanishes on 4D. Since deg(4D)=68>deg(2K_C)=60, it vanishes
identically. This is the degree argument of
[van Bommel--Costa--Poonen--Srinivasan, Lemma 4.1 and Corollary 4.2](https://arxiv.org/pdf/2506.14026),
applied in [D88](d88-cm-expansion-identification-review.md).
The candidate scheme certificate from D69 then identifies (C,D).
No rank-45 witness is needed for this four-coefficient route.
The P32/B3 markings and the upstairs double-cover character would
still require their separate certificates.

## 8. Actual third coarse coefficients and direct quadric evaluations

Source 442 uses only the frozen D115 precision-200 moments. For
n=2j+2 the twice-A kernel is

    2*K_j = 1-((1+X)/(1-X))^n,         X=(b/beta)*x.

Its degree-r coefficient, for r>0, is
-sum_(k=1)^min(n,r) 2^k*binomial(n,k)*binomial(r-1,k-1).
For j=0,1,2,3 these coefficients have uniform extra beta-valuations
32,48,32,64; the constant coefficient is zero. The 400 retained
degrees and moment error 400 give analytic errors 432,448,432,464.
Arithmetic modulo beta^448 safely caps the last at 448. Explicit
integer overflow bounds are checked before the NumPy products.

The new calculation reproduces all 816 earlier coarse coefficients
within their saved errors and computes all 272 third coefficients.
Review 445 uses a different binomial expansion and the independent
integer quotient implementation from 416 to verify every third value.
No moment precision, splitting branch or arithmetic label changed.

Source 443 transforms these four coefficients by the actual D115
matrix and evaluates every candidate quadric at all seventeen points.
For order n the conversion to the lower bound in (3) is

    v_beta([u^n] Q(actual residue-frame coefficients))
                + 2*3920-4200-(n+2)*m_i.

The unknown common scalar unit does not affect this valuation. For
n>=2 its intrinsic integral interpretation is conditional on the
preceding exact zeros, as section 7 requires. Review 445 recomputes
all 4641 positive coefficients using gradient and polar-form formulas.

| Successive order | Achieved lower bound at degree-16 place | Anchor lower bound | Sufficient bound using anchor | Remaining valuation gap |
|---|---:|---:|---:|---:|
| 1 | 3794 | 3576 | 119806 | 116012 |
| 2, if order 1 is exactly zero | 3745 | 3248 | 120284 | 116539 |
| 3, if orders 1 and 2 are exactly zero | 3728 | 2984 | 120758 | 117030 |

Every computed residual contains zero. No positive-order exact
vanishing and no certified mismatch are obtained. The offsets above
must not be confused with error digits in the ratio chart.

## 9. Rank diagnostic and audit scope

Sources 432/434 expand the actual degree-two monomial jets at one
non-anchor CM embedding in the sixteen-dimensional beta basis over Q2.
They certify rank at least 32, or 33 after adding W's exact constant
row. Review 435 inverts the selected rational center minors exactly
and proves every entry of A_0^(-1)*(A-A_0) has v2>=1. The Neumann
criterion proves the minor is nonzero independently of interval pivoting.

Candidate-centered trials with hypothetical extra beta-digits
0,32,64,96 give predicted ranks 33,34,41,45. These are conditioning
diagnostics, not actual precision certificates. Rank 45 remains
unproved. Nor is this an independent proof of nonhyperellipticity:
the rational-frame descent used here already relies on D99.

Sources 432--445 and the source ledger accompany this report.
Final review 445 preserves all 814 D115 source hashes and binds the
new sources, data, receipts, report and ledger. Before the final
audit, all thirteen input jobs passed; the longest took 57.894
seconds. The final audit's calculation probe passed in 143.899 seconds.
Sources 435 and 440 ran as probes, and their calculation
cores are incorporated in 445; their earlier draft final-build job
counts are not the current audit entry point. No failed probe or
timeout occurred in this milestone. All jobs retain runner 272's
180-second private-process-group cap.

Recheck the final certificate through runner 272 with Python/NumPy:

    python3 dembele/pari/445_cm_arithmetic_identification_review.py --check

The machine checks establish the finite identities, local enclosures,
integer lattices, bounds and provenance. The integral uniformization,
descent, metric comparison, nodal residue and vanishing-jet arguments
are the mathematical proofs and stated source inputs above.

## 10. Revised continuation plan

The direct integral section criterion is the primary exact-identification
route. It removes both ratio-chart divisions and the rank-45 prerequisite,
and its required coarse orders are now available. Keep the ratio bounds
and rank diagnostic as secondary evidence and controls.

The next bounded research task is to sharpen the norm/content bound
for the actual reduced tensors q_Q in (2), using their explicit
complementary-minor expression. In particular, compare a provably
larger embedded CM disk or tighter integral evaluation lattice with
the current B^238 estimate, and carry any gain through (4). This needs
an effective bound on the actual curve, or an exact arithmetic identity
with uniqueness. A small candidate height alone is insufficient.

If that cannot make the direct test practical, the alternative is a
costed algorithm for the explicit valuation targets above. Before
running it, certify a limb-safe ring implementation, transport/Hensel
accuracy, memory bounds and a phase schedule under the existing cap.
The current fixed-width matrix products cannot simply be used at the
forecast higher precision. An optimistic extrapolation from this
diagnostic is insufficient to justify a large precision run.

There is no need to rerun the class census, introduce another level,
restart a Hecke bank, or enlarge the old cubic precision job to address
this particular gap. All existing resource pauses remain. D108's
spectral rejection remains in force. After base identification, marked
cover comparison, global genus-64 cubic/section data, norm-97 isolation,
combined target-scale torsion and the degree-257 invariant remain
separate tasks. No correspondence was sent. This milestone supplies
a stronger certificate and its actual inputs, not the final field.
