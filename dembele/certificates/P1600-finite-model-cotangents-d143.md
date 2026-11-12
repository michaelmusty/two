# D143: finite Hodge-model comparison and elliptic cotangent bounds

Date: 2026-10-08. Continuation authorized by “keep going!”.

The two tasks left by D142 now have concrete answers on the actual
normalizer curve C. In the normalization of that report,

    E_model = -(12421/6144)*log(2) = -1.401299012001152...,
    H_3 < 3.948,    H_32 < 99.372,    Psi < 164.846.

Here H_m is the average Wolpert cotangent height of the order-m points,
and Psi=(51/4)H_2+8H_3+(1023/1024)H_32. The model equality refers to
the minimal regular semistable model used in D119, including its
intersecting horizontal sections. C has good reduction away from 2,
so the nodal term outside 2 is zero. These statements use no candidate
equations, new harmonic bank, auxiliary-level computation, eigenvalues,
geodesics or Hecke data.

With these bounds, a sufficient remaining target in D142's correctly
normalized Riemann--Roch comparison is

    I + 6 average log(C_* Z'(1)) <= -486.385.                 (1)

This implication still requires the complete corrected global comparison.
Neither (1), an upper bound for the full I, nor that corrected global
constant is certified here. In particular h_Fal(C)>=29, positive exact
quadric vanishing, curve identification and the field polynomial remain
open. D142's actual bounds h_ext(I_2)<83240 and h_Fal(C)<30.039246 stand.

## 1. An integral derivative bound for any elliptic order

Let f:X->Y be a map of proper nodal curves over a mixed-characteristic
DVR R, with smooth generic fibres and a generically finite separable
map. D104 proves that the generic differential extends integrally as
f^*omega_Y -> omega_X, even if components are contracted. That proof
uses the logarithmic node generator and normality, not smoothness at
the marked section.

Suppose a section Q above P has generic ramification index m. Choose
local generators eta of f^*omega_Y and xi of omega_X, write
df(eta)=a*xi, and define the relative derivation D_xi by db=D_xi(b)*xi.
Then

    a(Q)=D_xi(a)(Q)=...=D_xi^(m-2)(a)(Q)=0.

These vanish on the generic fibre and hence over R, because the fibre
modules are torsion-free. The next derivative defines an integral map

    omega_Y|P -> (omega_X|Q)^m,
    eta |-> D_xi^(m-1)(a)(Q) * xi^m.                         (2)

Indeed, under eta'=f*eta and xi'=g*xi, its leading coefficient changes
by f(Q)/g(Q)^m. Every other Leibniz term contains a lower derivative
already zero. This also proves compatibility with extension of R and
with changes of charts. No factorial is divided out over R.

At infinity use centered uniformizing coordinates u=z^m and the
Wolpert norm ||du||=1, Petersson disk norm ||dz||=1. Map (2) is
du |-> m!*(dz)^m, of norm m!. Consequently its nonnegative finite
zero degree gives

    H_m <= m*h_L(Q)+log(m!).                                (3)

To apply this to C, choose a torsion-free auxiliary level away from a
specified finite prime, keeping maximal level at that prime. Its
canonical Hodge line is the relative dualizing line and pulls back
the maximal-level Hodge line. Extend the generic map to the stable
model of C and compose with stabilization upstairs. The structural
inputs are [Yuan--Zhang, Theorems 4.5 and 4.7](https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n2-p04-p.pdf)
and [Liu--Lorenzini, Proposition 4.4(a)](https://www.math.u-bordeaux.fr/~qliu/articles/modcove.pdf).
The level can be chosen separately at each prime; clearing Q-line
powers and finite base extension preserve the inequality. Resolution
of the stable nodes is crepant, as in D119, so the canonical fibre
used here is also the one on the minimal regular model.

The total generic ramification indices to C are 3 and 32, respectively.
The latter includes the norm-one order-16 stabilizer and the normalizer
double quotient. Formula (3) is deliberately a bound: it does not
assert that the finite zero degree vanishes. Source 601 checks the
node-derivation constants; source 602 changes both local frames before
differentiating and independently checks the leading coefficients.

## 2. The two CM fields require different height theorems

Keep F=Q(zeta_32)^+, [F:Q]=8, disc(F)=2^31 and d_B=2. The fields are

| Elliptic order on C | CM field | Absolute discriminant | Norm of relative discriminant |
| ---: | --- | ---: | ---: |
| 3 | E_3=F(sqrt(-3)) | 2^62*3^8 | 3^8 |
| 32 | E_32=Q(zeta_32)=F(i) | 2^64 | 4 |

An order-three stabilizer contains zeta_3 (or its conjugate). Because
the discriminants of F and Q(sqrt(-3)) are coprime, O_F[zeta_3] is
the full integer ring of E_3. An order-16 norm-one stabilizer contains
zeta_32, which generates O_E32. Thus the height formulas for maximal
CM orders apply; no unaccounted conductor correction is inserted.
The normalizer element 1+zeta_32 has relative norm 2+b and induces
projective order 32, compatibly with the saved signatures.

Let R_m=L_f'(0,chi_Em/F)/L_f(0,chi_Em/F), with the finite L-function.
E_3/F is unramified quadratic at 2. It therefore satisfies the
no-common-ramification hypothesis of [Yuan, Theorem 1.2](https://arxiv.org/pdf/2205.13995v3),
equivalently the published Yuan--Zhang Theorem 1.7. Divide its
relative Shimura-point height by eight to obtain

    h_L(E_3) = -R_3/8 + log(2)/16 - log(3)/2.               (4)

E_32/F is ramified at 2. For this field use
[Zhao, Theorem 7.4](https://arxiv.org/pdf/2309.08886v1), with
the singleton partial type and D104's normalization reconciliation.
The averaged Colmez and nearby-pair identities give

    h_average = -R_32/2 - log(d_F*4)/4,
    h_nearby = (h_average+log(d_F)/4)/4,
    h_L(E_32) = h_nearby + log(2*4)/16
              = -R_32/8 + log(2)/16.                       (5)

The common-ramification theorem is not substituted into (4). D104's
warning about the dropped discriminant factor in the final proof
display of Zhao's Theorem 7.5 remains applicable: we use Theorem 7.4
and the stated identities, not that inconsistent display. This is the
same source reconciliation as D104, not an author-confirmed correction.

For an exact finite evaluation, write an odd character as chi modulo q,
A_chi=L(0,chi)=-q^(-1)sum a*chi(a). Then

    L'(0,chi)/L(0,chi)
      = -log(q)+sum_a chi(a)/A_chi * log Gamma(a/q).

Source 601 constructs all eight characters by the signed powers of 5
modulo 32. For E_3 it multiplies the eight even characters of F by
chi_-3 and uses common modulus 96. Inflation removes the Euler factor
at 2 only for the conductor-3 character, so the common-modulus sum
needs the correction +(1/2)log(2). The primitive conductors are

    E_3:  3,24,48,48,96,96,96,96;
    E_32: 4,8,16,16,32,32,32,32.

Source 602 instead selects characters from independent Dirichlet
groups, takes primitive characters, uses their Bernoulli numbers, and
sums complex Arb balls. It also calculates both number-field
discriminants independently. Every interval overlaps the first
calculation, including the inflation correction. The certified bounds
and approximate values are

| Quantity | Approximate value of height or upper-bound expression | Safe strict upper bound |
| --- | ---: | ---: |
| h_L(E_3) | 0.718506627159660 | -- |
| h_L(E_32) | 0.556661186792734 | -- |
| 3h_L(E_3)+log(3!) | 3.947279350707035 | 3.948 |
| 32h_L(E_32)+log(32!) | 99.37111743348252 | 99.372 |
| (51/4)H_2^+ + 8H_3^+ +(1023/1024)H_32^+ | 164.845... | 164.846 |

The last row uses D118's H_2^+=2h_L(E_2)^+-(35/34)log(2),
not the coarser 8/3. Rational interval endpoints are in the packets.

## 3. Locate the finite-model difference

Let Q be D99/D110's integral normalizer quotient before contracting
its rational tails. Write L for the arithmetic Hodge Q-line descended
to Q, with its Petersson metric. The normalizer involution preserves
the maximal-level Hodge system: it normalizes the level and acts on
the small-level dualizing system. Equivalently take half the norm
of that line along the double quotient. Its pullback is the original
Hodge line. Norm/pullback compatibility is exactly the construction
in Yuan--Zhang 4.7 and Yuan section 4.1. Therefore

    L^2 = 2d*(Y/8),       d=1455/32,                        (6)

with Y as in D142. This defines the integral normalizer Hodge line;
it does not identify it with an arbitrary coarse dualizing extension.

At primes away from 2, [Yuan, Proposition 4.1](https://arxiv.org/pdf/2205.13995v3)
identifies the maximal-level Hodge line with the coarse orbifold line
and proves smoothness. The additional involution has order invertible
in the residue field. It extends on the smooth stable model, and its
tame quotient is smooth. Relative Riemann--Hurwitz therefore gives the
same orbifold-line equality on C there. In particular C has good
reduction away from 2 and the comparison divisor is dyadic.

At 2, work after an unramified splitting extension, and further split
the horizontal sections when necessary. Normalize v_b(b)=1 and
v_b(2)=8. The quotient has the 58 rational components and 73
noninverted edges of D111. Its nodes have the saved thicknesses.
The local quotient and resolution are those of D119, based on
[Kurihara, Proposition 3-2 and Lemma 3-3](https://repository.dl.itc.u-tokyo.ac.jp/record/39680/files/jfs250303.pdf).

Put alpha_i=1-1/m_i and W_Q=omega_Q(sum alpha_i P_i). All these
sections meet the smooth locus of Q. The order-two sections and the
order-32 section come from inverted-edge disks. D112 locates the
seventeen order-two sections; the remaining branch point P_32 is on
component 5. The order-three fixed points belong to the unramified
quadratic torus at 2. They retract to a vertex and reduce to the two
nonrational fixed directions in P1(F_4), away from the three nodal
directions in P1(F_2). The quotient images remain smooth.

Use the Petersson metric on W_Q for now, so L and W_Q agree
isometrically on the generic fibre. Their difference is a vertical
Q-divisor V. Its coefficients can be determined without knowing any
uncomputed elliptic-point coordinates.

## 4. Reconstruct V from multidegrees and a local normalization

Let e_j be the saved projective vertex-stabilizer order, n_j the
number of noninverted incident edges, and r_j the sum of alpha_i for
the marked sections on component j. A torsion-free small-level
component has three branches and dualizing degree one. Its map to
component j has degree e_j, including any inseparable residue degree.
Thus

    deg_j L=1/e_j,       deg_j W_Q=n_j-2+r_j.               (7)

The degree assertion includes wild stabilizers. At the generic
component DVR the base uniformizer still has valuation one downstairs;
the finite quotient's component degree is its stabilizer order. No
replacement by the order of its reduction in PGL2(F_2) is allowed.

For a noninverted edge jk of thickness ell_jk, set
N_jk=1/ell_jk and N_jj=-sum_(k!=j)N_jk. These are the intersection
numbers after crepant node resolution and elimination of the inserted
chains. The vertical coefficients v_j satisfy

    N*v = (1/e_j - n_j + 2 - r_j)_j.                       (8)

The graph is connected, so they are determined up to a common constant.
Component 58 has trivial stabilizer. Near its generic point the
small-level quotient is an isomorphism, the dualizing comparison is
the identity, and every horizontal divisor is a unit there. Hence
v_58=0. This fixes the constant; it is not an arbitrary gauge choice
for arithmetic self-intersection.

Here is the complete marking used in (8):

- order 2: one point on component 5 and two on each of 51,...,58;
- order 32: one point on component 5;
- order 3: one point on component 1 and two on each of 35,36,37,38.

For the last assertion count order-three elements in each saved vertex
group. Each cyclic subgroup has two fixed points, whose stabilizer
order is three by the actual signature. Orbit-stabilizer gives
3*(number of order-three elements)/e_j. Source 603 computes projective
orders; source 604 independently tests trace(q)^2=1 for norm-one q.
Both obtain these nine points.

The unique solution of (8), in the saved one-based order, is

    v=(12,15,8,18,25,5,2,2,1,1,0,...,0),                    (9)

with 48 final zero entries. Source 603 obtains the same coefficients
by summing the local displacement valuations of every nonidentity
vertex stabilizer. For A=(a b;c d) in GL2(O), each such valuation is
min(v_b(b),v_b(c),v_b(a-d)); all are strictly below their certified
splitting errors. This is the generic-component different calculation.
The monogenic derivative formula is [Stacks, 0BWB](https://stacks.math.columbia.edu/tag/0BWB).
Source 604 does not reuse that calculation: it solves the 57-by-57
grounded rational system (8). All 58 component identities hold, and
the two coefficient vectors agree exactly.

Consequently, in units of log(2)/8,

    (W_Q^2-L^2) = V^2-2L.V
      = -sum_edges (v_j-v_k)^2/ell_jk - 2sum_j v_j/e_j
      = -339/16 - 273/16 = -153/4.                         (10)

## 5. Contract the marked rational tails

Resolving a node is crepant and the marked sections avoid its
singularity, so it does not change W_Q^2. Tail contraction does change
it. For a blowup at a smooth point carrying total marked weight r,

    W_before = pullback(W_after)+(1-r)E,
    W_after^2-W_before^2 = (1-r)^2,

because E^2=-1 and the pullback has zero intersection with E. A leaf
attached by a node of thickness ell requires ell such contractions;
all its marked sections move with it. Its contribution is therefore
ell*(1-r)^2, even when the sections collide after contraction.

| Contracted component | Attachment | Thickness | Weight carried |
| ---: | ---: | ---: | ---: |
| 1 | 2 | 8 | 2/3 |
| 5 | 4 | 16 | 47/32 |
| 4 | 2 | 8 | 47/32 |
| 2 | 3 | 8 | 205/96 |
| 3 | 6 | 4 | 205/96 |
| 35,36,37,38 | 23,24,25,26 respectively | 1 each | 4/3 each |

Their total is 16955/768. Source 604 contracts in descending label
order, independently of source 603's ascending order, and obtains
the same sum and the same 49 remaining vertices and 64 edges before
resolving thicknesses. Combining this with (10) proves

    E_model = (-153/4+16955/768)*log(2)/8
            = -(12421/6144)*log(2).                        (11)

The finite normalization log(2)/8 comes from the unique dyadic prime
of F, whose norm is 2. Splitting extensions scale intersection numbers
and field degrees compatibly. Formula (11) is the comparison on the
minimal regular model, not on the uncontracted quotient. Omitting the
marked-tail correction would give a different answer.

Finally rescale the Petersson norm by 1/sqrt(2), as in D142. Both
lines have generic degree d, so the finite difference is unchanged
and the hyperbolic self-intersection is now established as

    W_hyp^2=2d*(Y/8)+d*log(2)-(12421/6144)*log(2).           (12)

## 6. Remaining proof target and audit boundary

Use D142's rigorous interval for Y/8, its delta_2=(19/2)log(2),
delta_other=0, equation (12), and the cotangent upper bound. The
outward-rounded calculation gives the sufficient condition (1),
equivalently

    average log(C_*Z'(1)) + I/6 <= -97277/1200.

This is a sufficient target using a coarse cotangent bound, not a
necessary condition or an estimate of the actual analytic expression.
D119's (33/4)log(2) remains only a known part of I. Intersections of
the other elliptic sections, including those caused by the marked
tail contractions, cannot be omitted. The next proof task is to
bound the full intersection term and reconcile the complete corrected
global RR constant, then assess an analytic inequality against this
explicit target. Numerical spectral work and a higher bank remain
unadmitted. Exact structural identification is still an alternative.

The four input jobs 601--604 pass in about 4--6 seconds each under
the unchanged private-process-group cap. All use at most one Sage
child, and combined parent/child memory stays well below 2 GiB.
Sources 601/602 independently check CM characters, fields, ball
constants and derivative controls. Sources 603/604 independently
check the vertical coefficients, marking counts, graph energies and
contractions. These finite checks support, but do not machine-prove,
the geometric arguments above or the cited theorems.

The fixed source-605 review/replay and completion record bind this
report, the source-applicability ledger and all four input jobs to
the full D142 inherited graph. Preserve all passing files and every
earlier failed attempt. P1600 and column 0/P6400 remain unchanged.
No secret, external message, publication, new level or search-pause
decision is needed for this completed checkpoint.
