# D121: low-moment elimination and the first actual precision lift

Date: 2026-09-27. Continue the original-kernel field construction under
the [D120 decision](construction-reassessment-d120.md). The low-moment
solver now works, all transport parameters have the conditional target
precision, and one actual harmonic column has been refined from P=200
to P=400, including all seventeen CM charts and four coarse coefficients.
The complete sixteen-column bank remains at P=200. No positive quadric
jet is proved exactly zero, no candidate identification is proved, and
no target field polynomial is constructed.

Sources and attribution are in
[the ledger](../data/computed/dyadic_schur_sources_d121.json).
Review 474 independently checks normalization, interpolation, selected
original moment equations and all 68 new coarse values, and binds every
inherited D120 source hash. These are exact finite computations and
mathematical arguments, not machine-formalized geometric proofs.

## 1. Why eliminating low moments accelerates the iteration

Work over O_F with pi=b, v_pi(2)=8. For a child map

    phi(x)=(a*x+b0)/(1+c*x),    delta=a-b0*c,

both c and delta lie in (pi), and

    phi(x)^n = sum_j binom(n,j)*b0^(n-j)*delta^j*x^j/(1+c*x)^j.

For k>0 every term of the x^k coefficient has valuation at least
j+(k-j)=k. Fix the exact zeroth masses. Split the positive moments
into L={1,...,r} and U={r+1,...,P-1}. The low matrix M=I-T_LL
reduces to the identity modulo pi, hence has an integral inverse.
The Schur operator on U is

    S=T_UU+T_UL*M^(-1)*T_LU.

Each column of T_LU and T_UU has valuation at least r+1, so S is
divisible by pi^(r+1). If the current low equations hold exactly,
take delta_U to be the current upper residual and
delta_L=M^(-1)*T_LU*delta_U. After adding this correction, the next
upper residual is S*delta_U. This proves a gain of at least r+1.

All graph pivots are allowed: successive diagonal Schur blocks remain
I modulo pi. The saved directed minimum-fill order on 174 states needs
2246 block updates, with 174 diagonal inverses, 506 lower and 546 upper
blocks. The directed graph has one component of size 169 and five singletons.

Source 464 checks the full r=1 inverse in the original sparse equations
and all sixteen actual first-moment columns. Source 465 recovers a full
P=200 column from P=184 in eight gains of two, then checks its full
original residual. Source 467 factors larger low blocks and checks all
sixteen actual low columns, plus two unrelated right-hand sides in the
original equations. The two right-hand sides are not a full-rank basis
of the global system; the corresponding source comment is imprecise.

| r | Low dimension | Factor time | Sixteen-column solve time | Stored in-memory coefficient payload |
|---|---:|---:|---:|---:|
| 8 | 1392 | 0.279 s | 0.078 s | 5,021,696 bytes |
| 32 | 5568 | 4.722 s | 1.127 s | 80,347,136 bytes |
| 64 | 11136 | 41.053 s | 5.117 s | 321,388,544 bytes |

These are P=200 measurements. Source 468 recovers one entire column
from P=64 by 64 -> 129 -> 194 -> 200, and independently reapplies
the original full operator. This whole-column test does not cover
all sixteen columns. When a correction has common valuation v, exact
coefficientwise division by 2^floor(v/8) permits smaller arithmetic
and input cutoff 8*(bits-floor(v/8)); omitted columns are certified zero.

## 2. Multiprecision arithmetic and transport parameters

Source 466 caches map-dependent powers and uses masks for power-of-two
reductions. Its synthetic P=10552 action takes 1.905 s to prepare and
27.706 s to apply, or 26.825 s with a reused plan. This is a benchmark,
not an actual target-precision moment calculation. Its original power
routine assumes enough output rows for the untruncated intermediate
powers. Source 473 supplies the truncated-power variant needed by low-row
actions and independently checks output lengths 1, 3 and 9 with 39 inputs.

Sources 469--470 implement exact field-valued block multiplication using
the installed FLINT 3.6.0 and GMP 6.3.0. A product of two degree-seven
entry polynomials has degree at most fourteen. Evaluate at 0,...,14,
multiply the ordinary modular matrices, and use Newton interpolation:

    P(b)=sum_(j=0)^14 (Delta^j P(0)/j!)*(b)_j.

The quotient by the two-part of j! is exact in the integers. Invert
only its odd part. Eleven extra binary digits suffice because
max v_2(j!)=v_2(14!)=11. Reduce the falling factorials modulo f(b)
over the integers. Choosing arbitrary input lifts is harmless: changing
a lift by 2^bits changes the result by a multiple of that modulus.
No even local-ring element is inverted.

The C build keeps assertions enabled. Tests include rectangular products
at 3,25,200,1319,1536 bits, all 64 field-basis products, and independent
full dot products in dense benchmarks. At 1319 bits the n=32 product
takes 0.07775 s and n=64 takes 0.44359 s, including binary conversion.
Review 474 also checks all fifteen integer monomial interpolation
identities and the guard-bit bound independently.

Source 471 refines the same Hensel branch of x^2+y^2+1=0. The root-error
lower bounds are 352,696,1384,2760,5512,10816 pi-digits in a ring with
10824 digits. Its derivative has valuation 8. For each exact transport
C+S*x, clear the common dyadic denominator, divide out the denominator's
pi-valuation and invert the remaining unit. All 348 child maps and 51
CM maps are exported to 10552 pi-digits. Review 474 verifies these
normalizations by cross multiplication, without using the production
pi-division or inverse routine, and checks overlap with the old centers.

The first two attempts were rejected because a comparison treated the
old v(0)=10^9 sentinel as an attainable finite-modulus precision. Exact
root-independent maps now compare at min(old_error,exported_precision).
Both failed sources and logs remain archived. This was a checking error;
no inconsistent transport branch was accepted.

## 3. Actual P=400 state and CM data

Source 472 factors the actual r=32 low system at P=400 with arbitrary
integers. The coefficient matrix is constructed by the exact factorization

    H[n,j]=binom(n,j)*b0^(n-j)*delta^j,
    B[j,k]=binom(k-1,j-1)*(-c)^(k-j),    C=H*B.

All factors reduce to the frozen P=200 factors. Every diagonal inverse
is checked by multiplication, and two unrelated right-hand sides pass
the original sparse equations. The job takes 39.370 s; packed factors
occupy 70,303,744 bytes. Newton matrix inversion lifts the known inverse
without inverting any nonunit.

Source 473 refines harmonic column 0 from the P=200 bank, restoring
zeroth masses from the exact harmonic basis rather than interpreting
old negative residues as new exact integers. The residual gains are

    200 -> 233 -> 266 -> 299 -> 332 -> 365 -> 398 -> 400.

Each stage has its own immutable binary state, residual, metadata, log
and capped receipt. The last job reapplies the original full operator
and checks all 556800 scalar coefficients. It also checks all available
P=200 overlaps. Since the original positive-moment operator is divisible
by pi, the finite fixed point is unique; the integral actual moments
satisfy the same truncated equations. Thus this is an actual certified
precision increase for the entire selected column, not just a test
against previously known high digits. The nine successful state jobs
take about 248 seconds in total. One premature dependent-job launch
was rejected for a missing predecessor file; it is archived and rerun
after that predecessor completed, without changing the mathematical code.

Source 475 extends only the nine state charts needed by the seventeen
CM A charts, through moment 1198. It computes the CM moments through
799. For a CM map, the degree-k coefficient in phi^n has valuation
at least k-n; the first omitted input has k=1199 and n<=799, so the
tail has valuation at least 400. Child-state extensions use the stronger
degree-k bound from section 1. All existing state and CM overlaps pass.

The four actual coarse coefficients are computed in the beta ring at
864 digits, with error bounds [832,848,832,864]. All 68 old coarse
values overlap. This job takes 13.873 s. Review 474 recomputes all 68
using the alternate binomial kernel and Horner evaluation, and separately
checks selected original state equations of degrees 1,2,33,64 by direct
coefficient recurrence. No higher residue-frame or quadric precision
follows from one column: the other fifteen columns remain necessary.

## 4. Reassessment and continuing execution

The Schur method is correct and the actual lift succeeds. Keep it.
The full P=10552 computation is still too expensive with the present
polynomial transport backend: 348 times the synthetic 26.825-second
reused action is already about 2.6 hours for a single full column sweep,
before repeated corrections or all sixteen columns. This extrapolation
is a warning about the current implementation, not a measured complete
run. Increasing r alone does not remove the initial and final sweeps.

Next reduce the cost of polynomial transport in compiled arbitrary
precision arithmetic, validating it against both the frozen and newly
refined data. Then complete the sixteen-column P=400 bank and recompute
the residue-frame quadrics. This provides a chance to falsify the candidate
before paying for the sufficient P=10552 certificate. If the enclosures
continue to contain zero, stage larger lifts with measured time and
streamed storage. The target transport parameters are already available.

D118's full-bank section bounds and D120's conditional precision target
are unchanged. Higher intrinsic jets require preceding exact zeros.
Do not invert W's unresolved Gaussian. D99 nonhyperellipticity and D108's
spectral rejection stand. Canonical Y64, the marked cover, section
interface, degree-51 torsion backend, global F256 action and final
degree-257 invariant still require construction or verification as
recorded in D120. No new census, level, Hecke bank, cubic precision or
correspondence was used.

## 5. Reproducibility

All 24 input attempts use runner 272, one BLAS thread and a 180-second
private-process-group cap. Twenty-one pass; the three rejected attempts
described above have full archived sources, logs and receipts. Review 474
preserves all 961 D120 source hashes and binds the new sources and outputs.
Its full replay is:

    python3 dembele/pari/474_dyadic_schur_review.py --check

Run it through the same capped wrapper. Successful sources 464--475 and
their bound outputs are frozen; later improvements must use new files.
