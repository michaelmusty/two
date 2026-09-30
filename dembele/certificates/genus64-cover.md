# A computed Fuchsian realization of the genus-64 carrier

Date: 2026-09-15. Decision D43. This advances the proposal in
`review-2026-09-14.md` through the fundamental-domain and local-cover gates.

**Result:** the genus-16 normalizer quotient now has a saved, validated
Fuchsian domain and presentation. Its computed local monodromy is S3. The
inverse image of a reflection subgroup gives the proposed genus-64 curve;
an independent lifted-presentation calculation has first Betti number 128.
Algebraic equations and the integral target realization remain open.

## 1. The domain we actually computed

We use

    F = Q(b), b^8 - 8b^6 + 20b^4 - 16b^2 + 2 = 0,
    D = (b-b^2, -1)/F.

This small presentation is given in Dembélé's section 5.1. It avoids the
large Hilbert-symbol coefficients obtained by asking Magma to construct an
algebra from its ramification set. The published genus-40 curve X is the
norm-one quotient, and its positive-normalizer quotient C has signature
(16; 2^17,3^9,32).
[Dembélé, the explicit algebra and Theorem 5.1](https://arxiv.org/pdf/1906.06772).

Rickards's `afuchinit(A,,3,0)` selects the full positive normalizer. The
computed normalizer-norm list has one Atkin–Lehner generator, no extra unit
generators and no class-group generators. The first run gave:

| Quantity | Result |
|---|---:|
| Field discriminant | 2^31 |
| Finite ramification | The unique prime above 2 |
| Real ramification | Seven places; the fifth PARI real embedding is split |
| Polygon sides | 277 |
| Presentation generators / relations | 58 / 27 |
| Signature | (16; 2^17,3^9,32), no cusps |
| Area divided by 2 pi | 1455/32, numerically matching to the working precision |
| Domain CPU time | 250.785 seconds |
| Whole run wall time | 257.443 seconds |

`afuchcheck(X)` returns zero. It checks the signature/area comparison,
presentation sizes and relations, side-pairing relations, word reduction,
and elliptic elements. The arithmetic generators and relations are exact;
the polygon was computed at 57 decimal digits. This is a validated numerical
Fuchsian computation, not an interval-arithmetic proof of polygon coverage.
The genus-40 signature and discriminant 2 are independently reproduced in
Magma by `65_explicit_quaternion.m`.

The relevant upstream improvement and implementation are due to Rickards;
this project supplies the specific input, compatibility patch and checks.
[Rickards, Math. Comp. 91 (2022)](https://doi.org/10.1090/mcom/3777),
[maintained implementation](https://github.com/JamesRickards-Canada/Fundamental-domains-for-Shimura-curves).

## 2. An explicit local homomorphism

Let p be the prime above 2, and P_D the radical of the local maximal order.
The quotient

    D_p^* / (F_p^* (1+P_D)) = F4^* semidirect C2 = S3

has a concrete realization on the three nonzero elements of F4. The generator
i of the Hilbert-symbol presentation is a division uniformizer because its
reduced norm has p-valuation one. Its square is central. Conjugation by i
induces squaring on the residue field.

Script 66 constructs this residue field from the **actual order stored in
the saved domain**, rather than guessing the correspondence between bases.
The algebra O/2 has dimension 32 over F2. Its Jacobson radical has dimension
30, and the two-dimensional quotient is checked to be F4.

For a quaternion g, put v = valuation_p(nrd(g)) and normalize it to the local
unit u = g*i^(-v). Reducing u gives r in F4^*. The local permutation is

    x |-> r*x^(2^(v mod 2)),  x in F4^*.

The code checks nonzero residues, permutations, all 27 presentation
relations, and multiplicativity on products of each presentation generator
with the first five generators. The generated permutation group has exactly
six elements. These calculations use exact arithmetic over Q, F and F2.
The map is the intended division-level reduction: its formula and kernel
are intrinsic to the local division algebra, not an arbitrary S3 quotient
of the abstract surface group.

The use of the full local projective division group for C agrees with
Qiu's explicit adelic description. Replacing that component by the kernel
above or by the inverse image of a reflection subgroup specifies the levels
of Z and Y respectively; other components stay maximal.
[Qiu, section 7](https://arxiv.org/html/2509.06175v1#S7).

## 3. The cover and its two genus checks

The local image is surjective, so its kernel defines a connected degree-six
cover Z of C. The inverse image of the stabilizer of sheet 1 defines a
connected degree-three cover Y of C. The latter is not Galois; Z is its
S3 Galois closure as a cover. This S3 is a **level-cover group**, not the
Galois group of the desired nonsolvable number field.

The 17 order-two elliptic elements map to transpositions, the nine
order-three elements to 3-cycles, and the order-32 element to a transposition.
This proves the branching prediction in the previous review for the
computed arithmetic presentation. Lifting elliptic cycles gives

    signature(Y) = (64; 2^17,16,32),
    signature(Z) = (136; 16^3).

The co-area ratios to C are three and six. For example,

    3*(1455/32) = 2*64-2 + 17/2 + 15/16 + 31/32.

Independently, lift each presentation relation starting on each of the
three sheets. The resulting rational cellular complex has 174 one-cells,
three zero-cells and 81 two-cells. The code checks that consecutive
boundary maps compose to zero and computes

    rank(d1) = 2, rank(d2) = 44,
    dim H1(Y,Q) = 174 - 2 - 44 = 128.

Finite orbifold stabilizers do not affect rational first homology, so this
is a second calculation of genus 64. It is not merely the earlier
Riemann–Hurwitz arithmetic with an assumed genus as input.

Coset representatives are particularly small: the identity and side
generators 2 and 8. Their exact quaternion values and the local images of
all 277 side generators are exported. Every resulting Schreier generator
is checked to fix sheet 1. These data specify three translated parent
polygons with their sheet transitions; a new normalized Dirichlet polygon
for Y has not been computed.

## 4. What this establishes for the target

The proposed curve is now specified by an explicit arithmetic subgroup,
with its local monodromy, connectedness, branching and genus checked. The
standard Shimura canonical-model construction supplies the abstract
algebraic curve for this level. No explicit descent to Q is claimed or
needed at this stage: the intended polynomial construction can work over F.

There is also a useful marked-point deduction from this canonical-model
interpretation. The unique order-32 elliptic point of C is F-rational.
Its degree-three fiber has two geometric points, of distinct ramification
indices 1 and 2; each is therefore F-rational. Their upstairs elliptic
orders are 32 and 16. They supply candidates for a rational Jacobian
basepoint and a CM-centered expansion, although their algebraic coordinates
on an explicit model have not yet been computed.

The proposed Jacobian decomposition remains 16 old dimensions plus the
48-dimensional p²-new carrier. Its explanation is local: the permutation
representation on three sheets decomposes as the trivial representation
plus the standard two-dimensional S3 representation. On the depth-zero
division type, a reflection has a one-dimensional invariant subspace.
This retains one copy of the desired new factor. A precise Jacquet–Langlands
and integral-lattice comparison still needs to connect this geometric
realization to the sign-type congruence of script 63.

In particular, the exact local-cover calculation does not by itself prove
that an arbitrarily chosen lattice in H1(Y) has exactly the original
residual kernel. Nor does it supply algebraic evaluation maps, curve
equations, a torsion invariant or a polynomial for the field.

## 5. The next computational gate

The domain enables a specific automorphic-form computation. One can work
on the 277-sided parent polygon with three-component forms transforming
through the known sheet permutations. Equivalently, separate the trivial
component from the two-component standard representation. This can avoid
rebuilding a fundamental domain for Y before computing its differentials.
It still requires a working power-series or other analytic section algorithm.

The first geometric measurement warns against choosing a single global
Taylor truncation without investigation. In disk coordinates for the saved
domain, the maximum vertex radius is approximately 0.9997819873. Merely
forcing r^N below 10^-30 at that radius takes N = 316817. This is **only a
geometric damping measurement**: it omits coefficient growth, cancellation,
automorphy and tail estimates, so it is neither a precision certificate nor
a universal lower bound. Multiple expansion centers, analytic continuation,
or a CM-centered sparse expansion should be evaluated before allocating a
large dense system.

The next milestone is a numerically validated basis of holomorphic
differentials and multiplication/evaluation data that can be recognized
algebraically. Once such curve data exists, the odd-prime torsion route
of D42 becomes executable. The fundamental-domain obstruction has been
removed; the algebraic-model obstruction has not.

## 6. Reproduction and retained artifacts

See `../pari/README.md` for the pinned revision, build patch and bounded
runner. The exact scripts are `../pari/65_normalizer_domain.gp` and
`../pari/66_local_s3_cover.gp`; the independent Magma input is
`../magma/65_explicit_quaternion.m`. All have passing logs in
`../data/computed/`. The local cover replays in about two seconds from the
saved domain. Upstream software is stored in the ignored vendor checkout;
the revision, patch, input scripts and generated domain are retained.
