# Exact height exclusions for empirical CM evaluation spaces (D60)

Date: 2026-09-16. The user asked to continue the descended CM-field
approach and to keep the decisions and references ledgers current.

**Result:** the two-dimensional evaluation space does not supply a
small-height reconstruction in the current numerical neighborhood.
Script [98_cm_flag_height.py](../pari/98_cm_flag_height.py) produces
exact lattice certificates excluding **all** rational spaces below
the bounds in the table, within explicitly declared empirical boxes.
This strengthens D59's nonexhaustive unsuccessful searches.

| Space in the fixed trace-zero field basis | Height excluded, inclusive | Lattice scale |
|---|---:|---:|
| Q X | 19,927,223,139 | 10^13 |
| Q Y | 13,481,861,693 | 10^12 |
| Q X + Q Y | 43,166,965,625,539,309,014 | 10^13 |

For a line, height means the largest absolute coordinate of a primitive
integer vector. For a plane, it means the largest absolute primitive
integer Pluecker coordinate. These heights are independent of a choice
of generators for the space, but depend on the fixed D59 ambient basis.

**The boxes are not certified analytic error enclosures.** Accordingly,
the table is not an unconditional lower bound for the actual functions
or evaluation flag. It says exactly: no rational subspace of such height
lies inside the specified box. The geometric target has the resulting
height lower bound only if it lies in that box. D56's hypotheses and
D59's complex-orientation inputs remain in force.

## 1. Remove the choice of generators for the evaluation plane

Under D56 and D58's hypotheses, trace centering identifies

    ev_D L(17P)/<1> with Q X,
    ev_D L(18P)/<1> with Q X + Q Y

inside the trace-zero part of L=Q(theta), the known degree-17 residue
field. D59 supplies coordinates in a fixed basis eta_1,...,eta_16 and
the labelled complex embeddings used to compute them.

Recovering the plane can be easier than recovering a chosen basis:
large coefficients introduced by mixing two generators do not change
the plane. This does not eliminate the distinguished line Q X from
the eventual reconstruction problem. Different lines in the same
plane can define different flags and different normalized X,Y.

Arrange the coordinates of X and Y as a 2-by-16 matrix U. Choose a
pair of columns P for which the absolute determinant is largest, and
form

    C=U_P^-1 U.

The P columns of C are the identity; the remaining 28 entries describe
the plane in an affine Grassmannian chart. For every invertible
2-by-2 matrix G, even a complex one, `(G U)_P^-1 G U=C`. Thus the
chart removes all generator choices within the plane.

The selected field-basis indices are 1 and 7. The line charts use
indices 4 for X and 1 for Y, agreeing with D59. Maximal-minor selection
keeps the current chart entries bounded in absolute value by one.

## 2. Exactly specified empirical boxes

The only numerical input is
[cm_field_recognition.json](../data/computed/cm_field_recognition.json).
For each of the four banks, the saved decimal real and imaginary parts
are interpreted as exact rational numbers. All subsequent row reduction,
comparison, rounding and certification is performed in Q or Q(i).
No additional floating-point rounding enters the certificate.

For each free chart entry, the center is its current real part and
the radius is ten times the largest of:

* the complex L1 change from current to each other bank;
* the absolute imaginary part in each of the four banks.

This is the same empirical rule used in D59, now applied to the whole
plane as well as its two named directions. The plane's radii range
from 3.18e-14 to 2.99e-12. Its largest imaginary part across all banks
is 3.03e-14. The line radii agree with D59.

Individual rational-interval tests on the 28 free plane entries give
0 hits at denominator caps 10^3,10^4,10^5; 10 hits at 10^6; and 27 hits
at 10^7. None gives a complete chart. The certificate below imposes
the shared integer structure of a rational plane and yields a much
stronger statement than these individual tests.

## 3. A verifiable exclusion for the entire box

Here is the precise argument implemented by script 98. It applies
to dimension r=1 or 2 in ambient dimension n=16. Permute the chosen
pivot columns first and write the candidate chart as `[I_r | T]`.
Let A be the rational matrix of interval centers and E the nonnegative
matrix of radii, so `|T_ij-A_ij| <= E_ij` entrywise.

For a positive integer S, let R be A*S rounded entrywise to nearest
integers. Form the integral lattice with row basis

    M = [ I_r    R  ]
        [  0    S I ].

For an integer ambient vector v=(a,p), its image

    F_S(v)=(a, a*R-S*p)

belongs to this lattice. Indeed it is the combination of rows of M
with coefficients (a,-p). This map is injective.

LLL supplies a new row basis B=V*M. The saved certificate includes
the integer matrix V, and the verifier checks `det(V)=+1 or -1` and
the equality exactly. It computes the squared Gram--Schmidt lengths

    d_i=||b_i^*||^2

over Q directly from B*B^transpose. It also checks that their product
equals the Gram determinant. Validity of the argument does not depend
on trusting floating-point LLL metadata or even on B being reduced;
reduction improves the bound.

Write

    L_r = product of the r smallest d_i,
    k_ij = |R_ij-S*A_ij| + S*E_ij,
    C_r = product_i (1 + sum_j k_ij^2).

Every nonzero element of the exterior lattice wedge^r(Lambda_M) has
squared Euclidean length at least L_r. To see this, write it in the
integral basis consisting of wedges of rows of B. Gram--Schmidt changes
that basis by a triangular matrix with diagonal one. The last nonzero
integer coefficient therefore remains nonzero in the corresponding
orthogonal wedge basis. Its squared contribution is at least a product
of r distinct d_i, hence at least L_r. For r=1 this is the usual last
nonzero coefficient argument for a shortest-vector bound.

Now suppose W is a rational r-plane in the chart box, and choose a
Z-basis of the saturated lattice W intersect Z^n. Its exterior product
has the primitive integer Pluecker coordinates of W: saturation removes
the common factor in the minors. Let h_P be the minor on the selected
pivot columns. It is a nonzero integer of absolute value at most H(W).

Applying F_S to this basis transforms its exterior product into h_P
times the wedge of the rows

    [I_r | R-S*T].

Each tail entry has absolute value at most k_ij. Hadamard's inequality
bounds this wedge's squared norm by C_r. The transformed exterior
product is a nonzero element of the integral exterior lattice, so

    L_r <= |h_P|^2 C_r <= H(W)^2 C_r.

It follows that **no rational space in the box can have height H with
H^2 C_r < L_r**. All terms in this inequality are exact rational
numbers. The reported bound is the largest integer H satisfying the
strict inequality; equality is handled explicitly.

The lattice reduction and Gram--Schmidt background is in
[Lenstra--Lenstra--Lovasz, section 1](https://ir.cwi.nl/pub/9304/9304D.pdf).
The exterior-power adaptation and the displayed box bound are derived
here, not quoted as an output of that paper. The
[Sage integer-matrix documentation](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html)
documents the returned unimodular transformation and saturation.
Our verification recomputes the required identities exactly.

## 4. Results and independent controls

The tested scales are 10^8,10^10,10^11,10^12,10^13,10^14,10^16. The
largest exclusions are in the opening table. Raising S indefinitely
does not improve the result: the interval uncertainty is multiplied
by S too. For example, the plane bound drops from 4.32e19 at S=10^13
to 6.67e18 at S=10^16. This is an arithmetic scale experiment on the
same saved data, not a change in analytic precision.

The result rules out a small-height plane inside this neighborhood,
even after arbitrary changes of its two generators. It strengthens
D59's line search as well: there is no missed line of height at most
10^9 inside its stated intervals. D59's best unrestricted numerical
fits had heights about 10^12 and are consistent with these exclusions;
they remain rejected as exact identifications.

A positive control uses the known exact field plane

    span(theta-Tr(theta)/17, theta^2-Tr(theta^2)/17).

It has primitive Pluecker height 1 in the same ambient basis. After
an invertible nonrational complex change of generators and small known
rational perturbations, it lies in the constructed empirical box.
The certificate excludes height zero only, and rational reconstruction
with the known height recovers the exact plane. This verifies that a
small rational plane is preserved through the coordinate machinery.

Eight new tests check:

* invariance of the plane chart under complex generator changes;
* primitive Pluecker coordinates under rational changes and saturation,
  while distinguishing different lines in the same plane;
* the exterior Gram--Schmidt product formula via an independent compound
  matrix calculation;
* the exclusion against exhaustive small-height plane enumeration in Q^3;
* rejection of altered heights, transformations and Gram--Schmidt data;
* strict boundary handling and invalid input refusal;
* recovery of the known perturbed field plane;
* verification of all three saved certificates without running LLL.

All **111 tests pass**. The saved reports contain exact boxes, the best
certificate for each space, results at every scale and source hashes.

## 5. Consequence for the next step

The work now separates two unresolved arithmetic questions. First,
does the exact target lie in the empirical boxes? Second, what upper
height bound or independent exact evaluation data can select it?
The new certificates answer neither. In particular, they do not prove
that a larger numerical bank will recover the target or that the
descended functions have small denominators.

The direct plane experiment excludes the proposed shortcut of obtaining
a small rational basis merely by mixing X and Y, up to the stated
height limits within these boxes.
The next productive input should be an arithmetic construction of the
evaluation flag, or justified error and height bounds for this fixed
field-basis target. An analytic error enclosure would turn the present
conditional exclusions into genuine target lower bounds, but would
still not give an upper bound or the flag itself.

No exact target function value, curve equation, genus-64 cover, required
torsion or nonsolvable field polynomial is produced. D58's marked
descent and D59's labelled orbit remain useful inputs.

## Reproduction

Run from the repository root:

```sh
DOT_SAGE=/tmp/dembele-d60-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/98_cm_flag_height.py
DOT_SAGE=/tmp/dembele-d60-sage OPENBLAS_NUM_THREADS=1 \
  sage -python dembele/pari/98_cm_flag_height.py \
  --verify dembele/data/computed/cm_flag_height.json
DOT_SAGE=/tmp/dembele-d60-sage OPENBLAS_NUM_THREADS=1 \
  sage -python -m unittest discover -s dembele/tests -v \
  > dembele/data/computed/cm_flag_height_tests_20260916.out 2>&1
```

Reports are the identical pair
[cm_flag_height.json](../data/computed/cm_flag_height.json) and
[cm_flag_height.out](../data/computed/cm_flag_height.out); the full
[test log](../data/computed/cm_flag_height_tests_20260916.out) is saved.
The `--verify` mode checks the supplied boxes and certificate arithmetic
without performing any new lattice reduction. It does not certify the
analytic origin of those boxes.

All work is local and uncommitted. No new analytic bank or remote
computation was launched; all local computations have finished.
