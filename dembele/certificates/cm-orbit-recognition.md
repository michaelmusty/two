# CM orbit labels and simultaneous field reconstruction (D59)

Date: 2026-09-16. This continues the descent work at the user's request.

**Result:** the seventeen saved CM embeddings now have exact ideal-class
labels. A Frobenius computation matches them to the seventeen complex
roots of Elkies's degree-17 polynomial, with the numerical orientation
choices recorded explicitly. This makes simultaneous reconstruction in
the known residue field operational. It does not yet recognize X or Y.
The bounded search below accepts no projective direction for either.

**D60 follow-up:** [cm-flag-height.md](cm-flag-height.md) tests the whole
evaluation plane and strengthens the line results with exact exclusions
for every rational subspace below recorded height bounds inside empirical
chart boxes. These still do not certify target membership in the boxes.

D58's descent argument and D56's ordinary-point/nonzero-moment hypotheses
remain as stated in [marked-descent.md](marked-descent.md). The ideal
calculations do not certify those geometric hypotheses or the accuracy
of the saved function values.

## 1. Exact class labels from the saved embeddings

Use the saved maximal order O in B=(b-b^2,-1) over

    F=Q(b),  b^8-8*b^6+20*b^4-16*b^2+2=0,
    K=F(beta),  beta^2=-2-b.

The absolute polynomial of beta is

    s^16+16*s^14+104*s^12+352*s^10+660*s^8
        +672*s^6+336*s^4+64*s^2+2.

Script [96_cm_orbit.py](../pari/96_cm_orbit.py) exports O and the first
seventeen elliptic generators q_i directly from the saved Rickards
domain. PARI checks that the lattice is an order. D57's square witness

    s0=-4*b^6+22*b^4-28*b^2+4*b+2

gives beta_i=2*q_i/s0 with beta_i^2=-2-b for every i. Embedding an entire
integral basis of O_K into O proves that these embeddings are optimal.
Sage/PARI, with `class_group(proof=True)`, now independently proves
Cl(K)=C17. In D57 this class number was only a published input.

Take point 8 as reference and write beta_0 here for its embedded
generator. This reference is selected by the real/conjugate pattern
in the saved evaluations, checked for both X and Y below. For each other
point choose a sign epsilon_i such that

    u_i=epsilon_i*beta_i+beta_0

has totally positive reduced norm. Set u_8=1. Exact arithmetic checks

    (epsilon_i*beta_i)*u_i=u_i*beta_0.

Consequently u_i carries the reference fixed point to point i. Define
the fractional ideal

    I_i={a in K : u_i*iota_0(a) in O}.

The computation is a saturated lattice intersection. If M contains an
integral basis of O and V contains u_i*iota_0 applied to an integral
basis of O_K, put W=M^-1*V. For a denominator d of W, let H be a basis
matrix for the integer row lattice of d*W. The columns of d*H^-1 give
the preimage of Z^32 under W. The script checks that taking the O_K-span
of this lattice does not enlarge it.

By construction, I_i*O is contained in u_i^-1*O. The relative covolumes
of these two O-lattices are respectively N_K/Q(I_i)^2 and
N_F/Q(nrd(u_i))^-2. Every entry satisfies the exact identity

    N_K/Q(I_i)*N_F/Q(nrd(u_i))=1.

Thus I_i*O=u_i^-1*O. This supplies the principal generator required by
reciprocity without a quaternion ideal-principalization search.

The reciprocity convention is arithmetic Frobenius. In
[Voight, Theorem 5.1 and Algorithm 5.2](https://jvoight.github.io/articles/shimcm-fixed-errata.pdf),
an ideal c with iota(c)*O=xi*O acts on CM values by z -> xi^-1*z.
Here xi=u_i^-1, so [I_i] acts by z_0 -> u_i*z_0. We use the underlying
CM reciprocity law on the canonical curve and its normalizer quotient;
the paper's triangle-group parametrization is not required.
[Voight, section 4.3](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf)
also states the Hilbert-class-field and reciprocity description for
general totally real F.

The class labels, modulo 17 and in saved point order, are

    [10,12,16,14,3,1,5,7,0,4,11,15,8,9,2,6,13].

The generator ideal and all seventeen fractional ideal bases are saved
in [cm_orbit.json](../data/computed/cm_orbit.json). Labels depend on that
generator choice; the resulting point-to-root matching does not.

## 2. Match arithmetic Frobenius to the complex roots

Let H be Elkies's polynomial from D57 and L=Q(theta)=Q[t]/H. Its splitting
field has group C17 semidirect C16. Script
[96_cm_root_action.m](../magma/96_cm_root_action.m) computes the group
using complex roots and using 31-adic roots. It runs `GaloisProof` on
the latter, obtaining a proved group of order 272, and compares the
two root orderings with `GaloisGroupConjugation`.

The [Magma handbook](https://docs.magma-maths.org/GlobalFields/GaloisGroupsAndAutomorphisms/galois.html)
distinguishes the conditional group computation from `GaloisProof`
and documents the root comparison. The installed implementation does
not implement `GaloisProof` for the complex calculation. We retain its
complex/p-adic comparison as a software input; this report does not
supply an independent certified enclosure of every labelled root.

Since H is irreducible modulo 31, raising residues to the 31st power
gives a 17-cycle f. To identify which prime of K gives this Frobenius,
form the C17-invariant

    kappa=sum_j r_j^2*r_f(j).

Its sixteen conjugates replace f by f^a for 1<=a<=16. Their product
polynomial is reconstructed exactly from 31-adic arithmetic. The
Rouche inequality `sum_(j<17) |H_j|*4^j < 4^17` bounds all roots by 4,
so |kappa|<1088 and every resolvent coefficient has absolute value at
most 1089^16. The lift modulus 31^70 exceeds twice that bound. The
resulting degree-16 polynomial is irreducible and splits completely
over K; its coefficients are saved in the Magma log and orbit report.

The disk action at reference point 8 selects

    beta_complex=-i*sqrt(2+2*cos(7*pi/16)).

This sign is read from the eigenvalue on the saved fixed line. The
normalized eigenvalue differs from +i by 2.43e-53. This is a numerical
orientation check on saved geometric data, not a new error certificate.

For that complex embedding the resolvent generator is

    gamma=-beta^13-5*beta^12-12*beta^11-59*beta^10-55*beta^9
          -264*beta^8-119*beta^7-558*beta^6-114*beta^5
          -559*beta^4-15*beta^3-218*beta^2+28*beta-10.

Its minimal polynomial is checked exactly against the resolvent. Its
complex value matches kappa to 1.11e-87; the next possible match is
0.33124 away. Evaluating gamma at all sixteen 31-adic roots of the
polynomial of K selects exactly one root modulo 31^60. It gives

    q=(31,beta-19),  N(q)=31,  [q]=3 in Cl(K)=Z/17Z.

Starting the complex Frobenius cycle at the unique real root gives
the following **zero-based** root indices:

    [2,4,7,12,10,5,16,1,14,13,0,15,6,9,11,8,3].

A point of class c therefore corresponds to entry 6*c mod 17 in this
cycle, since 3^-1=6 modulo 17. The resulting lookup is:

| Saved point index | Ideal class | Complex root index |
|---:|---:|---:|
| 0 | 10 | 13 |
| 1 | 12 | 10 |
| 2 | 16 | 15 |
| 3 | 14 | 3 |
| 4 | 3 | 4 |
| 5 | 1 | 16 |
| 6 | 5 | 9 |
| 7 | 7 | 14 |
| 8 | 0 | 2 |
| 9 | 4 | 1 |
| 10 | 11 | 8 |
| 11 | 15 | 5 |
| 12 | 8 | 11 |
| 13 | 9 | 12 |
| 14 | 2 | 6 |
| 15 | 6 | 7 |
| 16 | 13 | 0 |

Complex conjugation is c -> -c. The saved X and Y values obey these
pairs to 3.75e-18 and 8.86e-18 respectively. The closest incorrect
pairings differ by 0.00781 and 0.21768. The root lookup respects the
same involution. These checks support the reference-point choice;
they do not supply analytic error bounds for the functions.

## 3. A stable field basis and a bounded joint search

Script [97_cm_field_recognition.py](../pari/97_cm_field_recognition.py)
uses the current, previous, alternate-fit and larger-probe evaluations
already saved by D56. It creates no new analytic bank.

A reduced integral basis of L is computed with 256-bit reduction
precision, and its discriminant is checked to be 2^79. Its first
element is 1. Replace each remaining basis element b_j by

    eta_j=b_j-Tr(b_j)/17.

Together with 1 these form a rational basis adapted to trace zero.
The complex evaluation matrix has infinity-norm condition number
40.9175 and computed inverse residual 3.10e-88. A default-precision
basis reduction had produced a badly conditioned basis in the pilot;
the script now checks both the discriminant and the actual matrix.
Small arithmetic residuals here do not increase the analytic accuracy
of the supplied CM values.

For each function, invert this matrix on all seventeen matched values.
Its constant coefficient is forced to zero by trace normalization.
Divide the sixteen remaining coefficients by the one of largest
magnitude, keeping this pivot fixed across the four banks. This gives
fifteen independent ratios specifying a rational projective direction.
The pivots are basis index 4 for X and index 1 for Y.

Each empirical interval has radius ten times the largest complex L1
change to another bank or imaginary part across all banks. Radii range
from 3.82e-13 to 3.05e-12 for X and 3.08e-13 to 5.15e-12 for Y.
Exact rational-interval tests on these saved decimals give:

| Denominator cap | X hits / unique hits | Y hits / unique hits |
|---:|---:|---:|
| 100 | 0 / 0 | 0 / 0 |
| 1,000 | 0 / 0 | 0 / 0 |
| 10,000 | 0 / 0 | 0 / 0 |
| 100,000 | 0 / 0 | 1 / 1 |
| 1,000,000 | 10 / 7 | 10 / 5 |

There are fifteen independent intervals in each column. Neither has
a full rational vector at these bounds. These are bounds on individual
projective ratios in this basis, not on monic polynomial coefficients.

A separate LLL search seeks one primitive integer vector satisfying
all fifteen projective intervals, using scales 10^10,10^11,10^12,10^13
and a maximum absolute coordinate of 10^9. It examines 58 distinct
directions for X and 59 for Y. **None is accepted.** This is a bounded
LLL search, not exhaustive enumeration up to the stated height cap.

Without that cap, the best numerical fits have heights 1041339150298
and 613595839686. They fit the intervals but are rejected as exact
recognitions: generic rational approximation at such large heights
does not identify an algebraic value. They do not determine a lower
bound for the true height. Failure at the chosen bounds neither
contradicts descent nor establishes that further precision will suffice.

As an independent positive control, the same basis, matching and
joint algorithm recover the exact normalized element
(17*theta-2)/30 from seventeen evaluations perturbed by at most 1e-15,
with a projective height cap of 1000. Candidate validation evaluates
the exact element at all seventeen roots and checks every supplied
bank. A separate control corrupts an unused bank and is rejected.

## 4. Reproduction and remaining work

Run from the repository root, in this order:

```sh
/Applications/Magma/magma -b dembele/magma/96_cm_root_action.m \
  > dembele/data/computed/cm_root_action.out
DOT_SAGE=/tmp/dembele-d59-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/96_cm_orbit.py
DOT_SAGE=/tmp/dembele-d59-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/97_cm_field_recognition.py
DOT_SAGE=/tmp/dembele-d59-sage OPENBLAS_NUM_THREADS=1 \
  sage -python -m unittest discover -s dembele/tests -v \
  > dembele/data/computed/cm_orbit_tests_20260916.out 2>&1
```

Outputs are `cm_root_action.out` and the identical JSON/OUT pairs
`cm_orbit.*`, `cm_field_recognition.*`. Reports record hashes of their
scripts and inputs, the ideal bases, root action, field basis, all four
coordinate vectors, interval decisions and search bounds. Seven new
controls bring the full suite to **103 passing tests**.

The labelled residue-field identification requested in D58 is now
usable, subject to the stated complex-orientation/software inputs.
The missing target is an exact rational line ev_D L(17P)/<1> and then
the compatible plane ev_D L(18P)/<1> in the trace-zero field. A next
arithmetic construction must determine these spaces, or justify a
specific height and accuracy budget for recovering them. Repeating
the same bounded scan or merely increasing precision has no such
justification yet.

Exact target CM values, a curve equation, the genus-64 cover, its
required torsion and the nonsolvable field polynomial remain open.
All work is local and uncommitted; no computation remains running.
