# D140: independent equation recovery from the existing P1600 data

The saved P1600 data recover the complete 91-dimensional integer quadric
lattice of the existing candidate, without using its equations in discovery.
The recovered relations pass the withheld CM points, the unused third-order
jet, and higher digits. Exact changes of integer basis show that both
recognition runs recover the same saturated lattice as the old candidate.
No higher harmonic precision was computed.

This answers the immediate precision question: P1600 already suffices to
recognize the candidate equations. P3200 is not required for that task.
Exact identification with the intended Shimura curve remains open. This
checkpoint supplies a new bounded-height uniqueness certificate and makes
its missing hypothesis explicit; it does not construct the field polynomial.

## Discovery with withheld information

The input is D138's actual residue-frame jets, whose construction uses no
candidate quadrics. Source 583 generates the 136 degree-two monomials in
lexicographic order and evaluates orders 0, 1 and 2 at nonanchor CM chart 1.
Each coefficient is expanded in the sixteen-element beta power basis,
giving a 48-by-136 matrix over the 2-adic integers after a certified row
normalization. These matrices contain at least 180 usable binary digits.
P1600 is uniformizer precision, not 1600 binary digits.

Two probes use only 96 and 160 binary digits, respectively. Valued elimination
finds 45 certified independent constraints and spends 13 binary digits in
each case, leaving kernel graphs modulo 2^83 and 2^147. The trailing zero
blocks are finite-precision statements. Entrywise rational reconstruction
recovers no complete graph-basis vector in either run; its vacuous
`all_reconstructed_vectors_pass_higher_digits` flag is not a positive result.

Source 586 instead constructs the full 136-dimensional integer congruence
lattice from each kernel graph. Sage reduces it by LLL, retaining the entire
basis and its unimodular transformation. It proposes the first 91 shortest
rows, using the observed nullity rather than a candidate coefficient cutoff.
Neither the probes nor LLL reads the candidate equations or candidate pivots.

| Training binary digits | Unused higher digits | Congruence modulus | Recovered independent relations | Largest absolute coefficient |
| ---: | ---: | --- | ---: | ---: |
| 96 | 84 | 2^83 | 91 | 968 |
| 160 | 20 | 2^147 | 91 | 981 |

The two joint recognition jobs take about 12 and 14 seconds. The existing
candidate basis has maximum coefficient 1514; the smaller numbers above
describe different bases of the same lattice, not a different curve.

## Independent validation and exact comparison

All proposed vectors pass the unused higher digits of their training matrix.
Source 587 then uses a separate integer Horner quotient implementation and
absolute-error balls, without importing production ball arithmetic or reading
candidate equations. For each recognized basis it checks all 6,188 coefficients
at all seventeen CM points through orders 0–3. There are no certified
mismatches. Of these checks, 5,824 use the sixteen withheld CM charts and
91 use the withheld order 3 at the training chart: 5,915 structurally withheld
coefficients in total. A one-coefficient perturbation is rejected.

Only after discovery and the first holdout result does source 590 read the
old candidate. It supplies exact 91-by-91 integer matrices of determinant
plus or minus one taking the 96-digit recovered basis to the 160-digit basis
and to the existing candidate. It also verifies both full LLL transformations
and the full congruence-lattice determinants. Thus the equality is of the
saturated integer relation lattices, not merely of their reductions.

Source 591 independently replays all 6,528 entries of each training matrix
using Horner products. An exact rational inverse of a selected 45-by-45 minor
supplies a modular certificate N with

    N B = 2^13 I modulo 2^t,

where t is 96 or 160. Multiplying the full selected-row matrix by N and
dividing by 2^13 reproduces the saved kernel graph. This check does not replay
source 583's elimination algorithm. Since t>13, the identity proves that the
minor of the actual matrix is invertible: changing any input by its allowed
error changes the product by a multiple of 2^t, and I+2^(t-13)E is invertible.
Every exact integral relation on the actual jets therefore lies in the
certified congruence lattice.

## An exhaustive height gap

Let L be the integer congruence lattice, with full basis b_1,...,b_136,
and let V be the rational span of the first 91 recovered rows. This notation
uses the saved order after sorting the reduced rows by squared length.
Write b_i* for their Gram–Schmidt orthogonalizations.

For any v in L outside V, write v=sum a_i b_i with integer a_i and take the
largest index j with a_j nonzero. Then j>91. Its projection onto b_j* is
a_j b_j*, hence

    ||v||^2 >= min_{j>91} ||b_j*||^2.

This argument requires a full lattice basis, not an assumption that LLL has
found a shortest vector. Source 589 computes the Gram leading determinants
D_k by exact fraction-free arithmetic. Their ratios D_k/D_(k-1) are precisely
the squared orthogonal lengths. Source 591 separately computes all 46 leading
determinants needed for the last 45 ratios using Sage's exact matrix backend.
Both methods agree. The final review independently checks the modular inverse
identities, transformation products and strict norm inequalities.

Because ||v||^2 <= 136 H^2 when all coefficients have absolute value at most H,
the strict inequality 136 H^2 < min_{j>91} ||b_j*||^2 gives the following
exhaustive bounds:

| Training digits | Every compatible integer quadric of coefficient height at most H lies in V |
| ---: | ---: |
| 96 | 18,234,668,645,049,602 |
| 160 | 223,818,092,532,287,707,686,732,450,725,941,069 |

The second bound is approximately 2.24×10^35. It applies to all integer vectors
in the congruence lattice, not only the LLL output. It is relative to the saved
rational residue coordinates and lexicographic monomial basis; it is not an
absolute invariant height of an arbitrary curve model.

## What this does and does not prove

The recognition bottleneck is resolved for these quadrics. A sufficient new
route to exact identification would be to prove that the actual canonical
ideal in these residue coordinates has 91 independent integral quadrics with
maximum absolute coefficients at most the second H. They would all lie in V,
and dimension 91 would force equality of the quadratic relation spaces.
Together with the existing candidate scheme and canonical-embedding facts,
that would identify the base curve in this frame.

That height hypothesis is **not proved here**. The small coefficients of the
recognized candidate do not bound the unknown true ideal. Finite congruence
conditions always permit sufficiently large additional vectors, so neither
successful reconstruction nor the large height gap establishes exact vanishing
without such an arithmetic bound or another exact identification argument.

D138's existing integral-section criterion still has gaps 18,561, 18,724 and
18,848 in beta valuation. This coefficient-height certificate is a different
conditional criterion, not a claim that those inequalities now hold. The
P10552 target remains conditional and sufficient, not necessary. Marked P32/B3,
the canonical Hecke interpretation and the remaining cover/torsion/original-
kernel construction stay separate obligations.

The next research task is to assess whether the actual ideal admits a useful
coefficient-height bound in this fixed frame, or whether the recovered model
can be identified structurally. The D139 P3200 cost model remains valid as a
planning scenario; its recommendation to make P3200 the default next action
is superseded by this reassessment. No new bank is admitted or launched.

## Preserved attempts and completion

Two LLL startup attempts stopped before arithmetic: the old `/usr/local/bin/sage`
launcher could not restore its application link, and the direct interpreter
then lacked Singular on PATH. Source 586 supplies the installed application's
executable paths within the child environment; no application installation,
global launcher, key or environment file was changed. The failed receipts,
logs, source snapshots and lattice inputs remain retained.

The first exact-comparison wrapper stopped on the legacy candidate's descriptive
status string rather than `pass`. Source 590 handles that exact status and
authenticates the candidate against D138. Its original source-588 attempt is
also preserved. These three interface failures are not numerical mismatches.

All work uses the unchanged 180-second private-process-group cap, at most three
mathematical workers, and the existing 2 GiB per-job/store and 6 GiB conservative
RSS limits. The Sage parent-plus-child peak is checked conservatively. No sealed
arithmetic store is modified and no higher precision bank runs. Source 592's
fixed review and replay, followed by the D140 completion record, are the final
completion authority. Freeze sources 583–592, this report and bound artifacts
after that review. Earlier milestones and all failures remain immutable.
