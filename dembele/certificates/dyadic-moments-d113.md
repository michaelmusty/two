# D113: finite moment recursion over the ramified dyadic field

Date: 2026-09-25. Continuation authorized by “keep going!”.

We now have **actual positive-degree moments** of all sixteen harmonic
measures. A finite system of 174 boundary charts and 348 contracting
maps computes moments through degree 11 with error at least pi^12.
Transfer to the 51 matched CM charts gives degrees 1, 2 and 3 with
error valuations at least **11, 10 and 9**, respectively. Among these
2448 positive-degree CM entries, **2043 are certified nonzero**.

The computation is a low-precision pilot, with v_pi(2)=8. At the W
anchor every computed positive-degree CM entry is zero modulo its
stated error ideal. This is a precision limitation, not a proof of
exact vanishing, and does not certify a normalization or Gaussian
pivot. No actual Shimura differential value or jet, harmonic-to-residue
change of basis, candidate identification or target polynomial is
claimed here.

The recursion and error proof below use the bounded scalar measures
already established in D111. They apply directly over our ramified K.
[Franc--Masdeu, section 6.1, especially Theorems 6.2--6.3](https://arxiv.org/pdf/1201.0356)
provides the related moment-lifting and evaluation framework over Qp.
We adapt the finite-chart idea and prove the scalar contraction needed
here; their Qp control theorem and constants are not imported.
The reference roles are recorded in
[the D113 ledger](../data/computed/dyadic_moment_sources_d113.json).

## 1. Boundary charts and exact finite transports

Retain K=F_p, pi=b, v_pi(pi)=1 and v_pi(2)=8. The residue field is
F2. Use D111's local frames L_j for the 58 existing ideal classes,
the same 174 oriented edge slots, their exact arithmetic transports
t_e, and the sixteen integral harmonic cocycles. No new class census,
level or Hecke prime is introduced.

In the D111 direction order infinity, zero, one, put

    H_inf=[0,1;pi,0],   H_zero=[pi,0;0,1],
    H_one=[pi,1;0,1].

If slot e at vertex j has direction d, its chart is H_e=L_j*H_d.
It sends O_K to the corresponding boundary ball B_e. Its target
vertex is [H_e], and its source is [H_e*diag(1,pi)]=[L_j]. This
records which side of the oriented edge supplies the measure mass.
Column-lattice coordinates over general local completions are also
described in
[Masdeu--Torrents, section 2.2 and Lemma 2.2](https://arxiv.org/pdf/2510.09356).

The saved transport t_e sends the target vertex of e to its saved
class i. Among the three outgoing slots f at i, exactly two yield
the maps

    phi_(e,f)=H_e^(-1)*iota(t_e^(-1))*H_f                 (1)

whose images partition O_K into its two residue balls. Matrix
identities are projective; the implementation uses
adj(H_e)*iota(bar(t_e))*H_f, omitting a common scalar.

[Source 411](../pari/411_dyadic_moment_transports.py) computes every
map exactly in the D109 splitting algebra F[t]/(t^2+y^2+1). After
normalizing its bottom-right entry, (1) has the form

    phi(x)=(a*x+b)/(c*x+1)
          =b+delta*x/(1+c*x),       delta=a-b*c,
    a,b in O_K,   c in pi*O_K,   v_pi(delta)=1.           (2)

The two values b mod pi are 0 and 1, respectively. The map
x -> x/(1+c*x) is an analytic bijection of O_K, with analytic
inverse x -> x/(1-c*x). Thus (2) maps O_K bijectively onto its
residue ball and contracts distances by exactly |pi|. These tests
certify the whole partition, not merely two sampled image points.

There are **348 maps**. Their normalized matrix-center errors have
valuation at least **159**. Exact reduced norms independently check
the determinant valuations. The sixteen masses satisfy

    mu(B_e)=sum_(two children f) mu(B_f).

This identity agrees with D111's harmonic table for every slot.
Retaining all 174 slots avoids imposing a new choice of representatives
for stabilizer orbits; redundant slots do not affect the argument.

## 2. The moment equations and their contraction

Let nu_e be the pullback of mu restricted to B_e by H_e, and put

    m_(e,n)=integral_(O_K) x^n dnu_e(x),       n>=0.

D111 gives v_pi(mu(B))>=0 for every compact open B, so these moments
exist and are integral. Arithmetic G-invariance and the partition in
(1) give the exact equations

    m_(e,n)=sum_(children f) integral phi_(e,f)(x)^n dnu_f(x)
           =sum_(children f) sum_(k>=0) C_(e,f;n,k)*m_(f,k),
    C_(e,f;n,k)=[x^k] phi_(e,f)(x)^n.                    (3)

There is no Jacobian or weight factor for these scalar measures.
The zeroth moments are exactly the saved harmonic values.

For every n>=1, expansion of (2) gives

    phi(x)^n=sum_(l=0)^n binom(n,l)*b^(n-l)
                          *delta^l*x^l*(1+c*x)^(-l).

All binomial coefficients are integral. A contribution to x^k,
k>=1, has l>=1 and valuation at least
l+(k-l)=k. Consequently

    v_pi(C_(e,f;n,k))>=k for k>=1,                     (4)

uniformly in n. This also proves uniform convergence, so summation
and integration in (3) are justified by the bounded-measure estimate.

Fix the known degree-zero moments and regard the positive moments
as the unknown vector. Its equation is m=b+T*m. By (4), T raises
the minimum error valuation by at least one. The actual integral
moments supply a bounded solution, and this contraction proves
uniqueness. It is enough to work with each finite truncation below;
no higher-weight or general overconvergent control theorem is needed.

Truncate at moment index J. The omitted terms all have valuation
at least J+1, since every m_(f,k) is integral. Therefore working
modulo pi^P is valid whenever J+1>=P. On the retained positive
moments, the operator is still divisible by pi. Starting with zero
positive moments and iterating m <- b+T*m N times gives

    v_pi(error)>=min(N,J+1,P),                           (5)

provided the coefficient centers are known modulo pi^P. Integral
coefficients and the contraction prevent amplification of rounding
errors. Equivalently, a retained vector with zero residual modulo
pi^P is the unique solution there. This is why the independent
residual check certifies the result without trusting the iteration.

This method has a fixed finite chart set. Increasing precision
increases the moment degree and the number of iterations, rather
than creating exponentially many tree balls. High-precision runtime
has not yet been measured; the theorem is not a performance claim
at the final field-identification precision.

## 3. Exact arithmetic and the executed pilot

[Source 412](../pari/412_dyadic_moment_pilot.py) takes

    J=11,   P=12,   N=12.

The ring O_K/(pi^12) has the unique power-basis representation

    sum_(i=0)^7 a_i*pi^i,
    a_0,...,a_3 modulo 4;  a_4,...,a_7 modulo 2.

In this quotient pi^8=-2. Indeed the full Eisenstein polynomial is

    pi^8-8*pi^6+20*pi^4-16*pi^2+2=0,

and the discarded terms have valuations at least 20. In particular
2 has valuation 8, not 1. Two bit planes implement the coefficient
arithmetic, processing the sixteen measures together. This optimized
implementation is restricted to working precision at most 16; it
must not silently be used beyond that range. The contraction proof
itself is not so restricted.

There are **174*12*16=33,408 saved moment entries**, including
degree zero. The successive differences of the positive moment
vectors have minimum valuations

    0,1,2,3,4,5,6,7,8,9,10,11.

The final residual is zero modulo pi^12. A unit perturbation of a
positive moment is rejected: it changes that moment modulo pi,
whereas every right-hand-side dependence on positive moments is
divisible by pi. Exact power-basis multiplication checks also verify
the quotient arithmetic and the ramification convention.

## 4. Transfer to the matched CM charts

For a D112 coordinate S and one of its boundary charts H_d, set
H_CM=S*H_d. The certified reducer provides q in G sending its
oriented edge to a canonical slot f. The coordinate map from the
canonical slot to this CM chart is

    psi=H_CM^(-1)*iota(q^(-1))*H_f.

Source 411 saves the exact splitting-algebra matrix, the quaternion
word for q, and its normalized coefficient center. For all 51 maps,

    psi(x)=(a*x+b)/(c*x+1),
    a,b in O_K,   c in pi*O_K,   v_pi(a-b*c)=0.           (6)

Hence each is an analytic bijection of O_K. The normalized error
is at least **165**. A stored center valuation for c is used only
up to this error bound; a zero center is not a claim that the exact
denominator slope vanishes.

Using (6), the same binomial expansion proves

    v_pi([x^k]psi(x)^n)>=max(0,k-n).

Transferring a degree-n moment from a bank through J therefore gives

    v_pi(error)>=min(P,J+1-n).                           (7)

Coefficient errors are also harmless here since their certified
precision is larger than P. Applied to J=11 and P=12, (7) gives

| CM moment degree | Certified error valuation v_pi |
|---:|---:|
| 1 | 11 |
| 2 | 10 |
| 3 | 9 |

All sixteen measures are transferred to all 51 CM charts. The zeroth
moments recover D112's exact values, including A0=0 and B0+C0=0.
There are 2043 nonzero positive-degree entries whose valuations are
strictly below their error bounds. All 144 positive-degree entries
at the W anchor are congruent to zero at their respective bounds.
They may become nonzero at greater precision. Neither the moment
zeros nor the nonzero values elsewhere are a differential evaluation
or an identification of a projective tangent.

## 5. Independent checks and bounded execution

[Review 413](../pari/413_dyadic_moment_review.py) does not import
source 412's bit-plane arithmetic. It independently reconstructs
all 348 transport matrices and all 51 CM maps using rational
arithmetic in the exact splitting algebra. It checks the quaternion
words, residue-ball partitions, coefficient-error bounds, determinant
valuations and mass identities.

It then uses ordinary integer coefficient convolution and integer
matrix multiplication in the quotient ring to reconstruct the
moment operators, verify every saved fixed-point equation, and
recompute every CM moment transfer. NumPy performs only exact
integer operations of bounded size; no floating-point linear solve
is involved. The residual and the contraction proof certify the
whole bank, including all unsampled moments.

As a separate integration check, the review partitions four actual
CM charts into depth-three balls: W's A, B and C, and CM index 1's
B. It reduces the **32 leaf edges** independently using source 405,
checks their exact masses and certified lattice precision, and
forms direct degree-1,2,3 Riemann sums. On a ball of radius pi^3,
x^n differs from its representative's n-th power by an element of
pi^3*O_K; d=0 therefore bounds the integration error by pi^3. All
192 scalar moment comparisons pass. This fixed small sample is a
validation, not the high-precision integration algorithm.

The transport, pilot and independent probe passed on their first
attempts in **6.18, 1.32 and 5.83 seconds**. All are runner-272 jobs
with private process groups and 180-second termination caps. There
were no failed D113 attempts before the final review. The final
[review artifact](../data/computed/dyadic_moment_review_d113.json)
binds the report, ledger, sources, artifacts and probe receipts, and
checks all **682 D112 hashes unchanged**. Its final and recheck
execution receipts remain separate to avoid circular hashes.

Freeze sources 411--413 and their bound files after successful review.
Recheck with Python and NumPy, without Sage or Magma, through runner 272:

    python3 dembele/pari/413_dyadic_moment_review.py --check

## 6. Next bounded task

The finite positive-moment method and the first actual pilot are now
complete. Next choose a modest precision and enough moment degrees
to feed D108's coarse Poisson coefficients, using (5) and (7) to
budget the transfer losses. For example, to make the common error
in D108's first three coarse coefficients at least T, the conservative
sufficient choices are

    CM moment cutoff R>=max(5,2*T-1),
    state precision P>=T,   state cutoff J>=max(P-1,T+R-1),
    iteration count N>=P.

These conditions combine D108's min((R+1)/2,P_CM) bound with
P_CM>=min(P,J+1-R). They do not establish a Gaussian pivot. Begin
with the actual coarse differential values and a certified nonzero
normalization at the anchor; do not divide by the currently unresolved
anchor moments. If working beyond precision 16, extend the quotient
arithmetic using the full Eisenstein polynomial. Beyond the saved
matrix bounds, refine the same exact Hensel branch and regenerate
new coefficient certificates without modifying the frozen ones.

A harmonic-to-residue change of basis, cofactor error propagation,
Gaussian chart and dyadic equality thresholds remain subsequent
gates. Inert-31 thresholds are not unchanged dyadic thresholds.
D99's nonhyperellipticity and D108's spectral rejection stand. Keep
the expanded-census, new-level, Hecke-bank and cubic-precision pauses,
and retain the 180-second job cap. Downstream marking, global sections,
norm-97 separation and target-scale torsion remain separate. No
correspondence was sent.
