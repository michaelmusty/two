# D114: actual coarse differential coefficients and the anchor precision gate

Date: 2026-09-25. Continuation authorized by “continue!”.

The first three coarse coefficients of all sixteen actual harmonic
differentials are now evaluated at all seventeen matched CM points.
In the specified local parameter u, write

    omega_a=(g_(a,0)+g_(a,1)*u+g_(a,2)*u^2+...)*du.

The final certified error valuations are **32, 40 and 32 in v_pi**.
At each of the sixteen non-anchor CM points, every one of these
48 entries is certified nonzero. At W, the respective valuations
are bounded below by **32.5, 40.5 and 32.5**. These are lower bounds,
not exact vanishing statements or an anchor nonvanishing certificate.

This is an actual coarse differential 2-jet in the harmonic basis
of the fixed geometric uniformization. It is not yet a ratio jet
in D106's rational residue frame. No basis change, normalization,
Gaussian pivot, candidate identification or target field polynomial
is obtained. The local parameter and basis must remain attached to
the saved values.

The independent review also identifies a concrete precision gate:
every polynomial moment on W's A chart is zero modulo pi^16.
Adding higher degrees at that same working precision cannot reveal
the anchor. The next bounded run must increase moment precision.

## 1. Extend the actual moment bank without a larger fixed system

Retain K=F_p, pi=b, v_pi(2)=8, beta^2=-(2+b), and
v_beta=2*v_pi. D113 has 174 canonical edge charts, 348 child maps,
51 matched CM chart maps and sixteen actual bounded measures with
denominator bound d=0. All arithmetic and geometric labels are
unchanged.

For a child map phi, D113 proves

    v_pi([x^k]phi(x)^n)>=k,       n>=1, k>=1.

At working precision P, every column k>=P therefore vanishes,
independently of the row degree n. Solve only the fixed system
through degree P-1. Once that solution is known modulo pi^P,
any higher row is obtained by one evaluation against the same
low-degree moments; its omitted-column error is still at least P.

[Source 414](../pari/414_dyadic_moment_extension.py) takes

    P=16,   low cutoff=15,   iterations=16,
    full state cutoff=46,   CM moment cutoff=31.

It produces **130,848 state entries** and **26,112 CM moment entries**.
All CM moments have error at least pi^16, since D113's transfer
bound gives min(16,47-n)>=16 for n<=31. Projection to the frozen
D113 state bank agrees everywhere. There are 20,336 positive CM
moments certified nonzero, but none at the W anchor at this precision.

The two-bit-plane arithmetic is used only at its certified upper
limit P=16. Here O_K/(pi^16) has all eight power coefficients modulo
4, and pi^8=-2. The exact normalized transport errors, at least
159 for child maps and 165 for CM maps, are far larger than P.
The full integer-ring coefficient representation and these bounds
justify every reduction. No new tree census, level or Hecke prime
is needed.

## 2. What differential is being evaluated

For each actual scalar harmonic measure mu, the Poisson differential
in the uniformizing coordinate is

    omega=f(z)dz,       f(z)=integral dmu(t)/(z-t).

D108 proves convergence, the transformation law from G-invariance
and total mass zero, and the local residue recovery of mu. Thus the
sixteen independent cocycles give sixteen independent holomorphic
differentials in the geometric Shimura uniformization. This uses the
same uniformization over the completed maximal unramified extension
as D110; no new rational basis or explicit descent matrix is asserted.
The matched D112 coordinate changes pull back these differentials
and their measures compatibly. Their coefficient errors have already
been absorbed in the CM moment transfer.

For the computational framework, see
[Franc--Masdeu, section 6.1](https://arxiv.org/pdf/1201.0356).
The required ramified-field convergence and tail estimates are the
direct arguments in [D108](shimura-evaluator-d108.md) and
[D113](dyadic-moments-d113.md), not an unchanged import of a Qp
overconvergent control theorem or precision proposition.

At each CM point use the exact D112 coordinate z with point beta,
and set

    w=(z-beta)/(z+beta),       u=w^2,
    z=beta*(1+w)/(1-w).

The stabilizer sends z to beta^2/z, hence w to -w. The invariant
differential has an odd coefficient in w, and its u-coefficients
are the actual coarse coefficients. This is not the odd-part
projection of a synthetic measure used in the old D108 controls.

## 3. Integral kernels and the initial certified enclosures

D108 gives

    g_j=beta*sum_(k=0)^(2j+1)
             (2*beta)^k*binom(2j+2,k+1)*f_k,
    f(beta+delta)=sum_(k>=0) f_k*delta^k.                 (1)

The factor two in dz/dw cancels the coarse division by two. It is
preferable to combine (1) with the moment expansions before doing
any field arithmetic. Put n=2j+2 and

    qA=pi/beta,   qB=pi/(beta-1),   qC=beta*pi,
    s=-2*beta/(beta-1).

For moments of degree r in charts A, B and C, the combined coefficients
used by [source 415](../pari/415_dyadic_coarse_poisson.py) are

    KA_(j,r)=qA^r*sum_(k=0)^(n-1)
                     (-2)^k*binom(n,k+1)*binom(k+r,r),

    KB_(j,r)=beta/(beta-1)*qB^r*sum_(k=0)^(n-1)
                     s^k*binom(n,k+1)*binom(k+r,r),

    KC_(j,0)=0,
    KC_(j,r)=-qC^r*sum_(k=0)^min(n-1,r-1)
                      2^k*binom(n,k+1)*binom(r-1,k),  r>=1.

All these coefficients are integral. In particular qA is computed
by an integral polynomial identity from the minimal polynomial of
beta, with beta*qA=pi. No approximate value is divided by beta.
The inverse of beta-1 is a certified finite geometric series in
the local quotient ring. All arithmetic uses the full degree-16
CM polynomial modulo beta^80.

The original D108 bound would give 16 pi-digits here. Keeping the
binomial valuations in (1) is stronger. With cutoff 31 and moment
precision 16, the error in f_k has v_beta at least 31-k, while its
coefficient in (1) has valuation

    1+17*k+16*v2(binom(2j+2,k+1)).

Hence the error in g_j is at least

    32+16*min_k(k+v2(binom(2j+2,k+1)))
       =48,64,48 beta-digits, or 24,32,24 pi-digits.       (2)

Source 415 evaluates all 816 entries with these bounds. At each
coarse order, 250 of the 272 entries are certified nonzero; the
anchor remains unresolved. These original enclosures are retained
unchanged in the source-415 artifact.

## 4. Independent kernel expansion and the involution improvement

For a boundary variable t, direct expansion of the pulled-back
Poisson kernel gives

    K_j(t)=(1-((beta+t)/(beta-t))^(2j+2))/2,
    g_j=integral K_j(t) dmu(t).                            (3)

Indeed omega's w-coefficient is
2*beta/((1-w)*((beta-t)+(beta+t)*w)); summing the geometric series
through the odd coefficient 2j+1 gives (3). This supplies a formula
independent of the finite f_k combination.

[Review 416](../pari/416_dyadic_coarse_review.py) expands (3) directly
in each of the three charts. It uses separate integer polynomial
arithmetic at precision beta^96, checks numerator divisibility by
2, and divides only then, retaining beta^80 precision. All 288
kernel coefficients agree with source 415. Thus the dyadic division
loss is explicitly accounted for. A changed infinity-kernel sign
is detected at the kernel precision.

There is an additional exact simplification. The actual embedded CM
involution T:t -> beta^2/t exchanges A=pi*O_K with its complement.
The measure is T-invariant. In (3) the ratio changes sign under T;
its exponent is even, so K_j(Tt)=K_j(t). Therefore

    g_j=2*integral_A K_j(t) dmu(t).                        (4)

This uses the actual G-invariance and the D112 exact CM embedding;
it is not a symmetry assumed of arbitrary input moments. It also
gives an independent consistency test against the three-chart sum.

The r=0 A-kernel coefficient is zero. For every r, the integer
coefficient 2*sum_k (-2)^k*binom(2j+2,k+1)*binom(k+r,r)
is divisible by 4, 8 and 4 for j=0,1,2. The factor qA^r has
v_beta=r. The omitted terms r>=32 in (4) consequently have valuations
at least 64,80,64. Errors in supplied positive moments have even
larger lower bounds, 65,81,65. The beta^80 field arithmetic suffices.

The review therefore supplies the stronger enclosure:

| Coarse order | Initial v_pi error | Involution-refined v_pi error |
|---:|---:|---:|
| 0 | 24 | 32 |
| 1 | 32 | 40 |
| 2 | 24 | 32 |

At each order there are now **256 certified nonzero entries**:
all sixteen basis entries at each of the sixteen non-anchor points.
Every refined enclosure agrees with the initial three-chart one
at its stated precision. Use the refined values in the final review
artifact for subsequent work, keeping their basis and local u attached.

## 5. Why a larger degree cutoff cannot resolve W at precision 16

At W, the A-chart moments of degrees 0 through 31 are all zero
modulo pi^16. This implies the same statement at every degree.
Since the residue field is F2, x^2-x belongs to pi*O_K for every
x in O_K. Thus

    Q(X)=(X^2-X)^16

is a monic integral polynomial of degree 32 whose values lie in
pi^16*O_K. Divide any integral polynomial by this monic Q. Its
remainder has degree at most 31, and the other term is pointwise
divisible by pi^16. The measure bound d=0 shows that its integral
is also divisible by pi^16. The remainder's integral is zero
modulo pi^16 by the computed moments. This proves

    v_pi(integral_A p(x)dnu(x))>=16 for every p in O_K[X].

Using this stronger bound on every term of (4), starting at r=1,
gives the rigorous anchor bounds

    v_beta(g_0)>=65,   v_beta(g_1)>=81,   v_beta(g_2)>=65,

for all sixteen differentials. Equivalently, their v_pi bounds
are 32.5,40.5,32.5. These do not prove exact vanishing. The degree-31
moment bank already detects the full polynomial-moment obstruction
at precision 16, so further degrees at that same precision cannot
produce a certified anchor value.

## 6. Audit and artifact contract

Review 416 recomputes all optimized moment equations, including
the vanishing of column 16, and all CM transfers using binomial
numerator/denominator expansions with ordinary integer convolution.
This is separate from source 414's bit-plane iteration. It checks
all 130,848 state entries, all 26,112 CM entries and the D113 overlap.
The independent kernel formula, accounted division by two, complete
coarse replay and involution comparison then certify the evaluation.
NumPy is used only for bounded integer operations, not floating-point
linear algebra.

Sources 414 and 415 passed first attempts in **4.59 and 0.40 seconds**.
The first review probe failed after **1.64 seconds** on an implementation
type mismatch: NumPy integers do not provide Python's bit_length
method. Its exact source, log and receipt are archived, and it wrote
no result artifact. Converting that value to a Python integer fixed
the issue; probe two passed in **1.69 seconds**. No arithmetic claim
was weakened to address the failure.

All jobs use runner 272, private process groups and a 180-second cap.
The final [D114 review](../data/computed/dyadic_coarse_review_d114.json)
binds the sources, artifacts, archived failure, successful probe,
this report and the [reference ledger](../data/computed/dyadic_coarse_sources_d114.json).
It checks all **696 D113 source hashes unchanged**. The final and
recheck receipts remain separate to avoid circular hashes.

The three result layers are deliberately explicit:

- `dyadic_moment_extension_d114.json`: the extended actual moment bank;
- `dyadic_coarse_poisson_d114.json`: original three-chart coarse values;
- `dyadic_coarse_review_d114.json`, at
  `certificates.Poisson.symmetry_refined_CM_values`: the stronger
  coarse values, with separate anchor lower bounds.

Freeze sources 414--416 and bound files after successful review.
Recheck with Python and NumPy, without Sage or Magma, through 272:

    python3 dembele/pari/416_dyadic_coarse_review.py --check

## 7. Next bounded task

Increase the working moment precision to **24 pi-digits**, initially
focusing on the W anchor and the A-chart formula (4). A conservative
pilot uses low state cutoff 23, 24 iterations, CM cutoff 47 and
state cutoff 70. Its expected coarse error bounds are at least
40,48,40 pi-digits. These are certified design bounds, not a promise
that this precision resolves a nonzero anchor value.

Use a new implementation of the full Eisenstein quotient. The old
pi^8=-2 shortcut is invalid at precision 24: the term -20*pi^4 has
valuation 20 and contributes. The existing transport centers remain
sufficient at this precision, so there is no need to change the
splitting branch or rebuild the tree data. Reuse the optimized
low-moment solve and recover higher state rows afterward. Keep the
180-second cap and certify overlap with the completed precision-16
bank. Do not divide by an unresolved anchor value.

After anchor nonvanishing, the rational-frame basis change, cofactor
error propagation and a Gaussian pivot remain separate requirements
before ratio jets. Final-scale runtime and dyadic equality thresholds
are not supplied here; inert-31 thresholds cannot be copied unchanged.
D99's nonhyperellipticity and D108's spectral rejection stand. Keep
the expanded-census, new-level, Hecke-bank and cubic-precision pauses.
Downstream marking, global sections, norm-97 separation and target-scale
torsion remain separate. No correspondence was sent.
