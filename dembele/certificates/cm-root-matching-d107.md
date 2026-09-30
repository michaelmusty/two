# D107: certify the saved CM point-to-root matching

Dates: 2026-09-24--25. Continuation authorized by “continue”.

**Result.** The saved D59 lookup between the seventeen actual CM
points and the seventeen roots of the degree-17 polynomial is now
certified. It is the lookup for D106's rational residue frame:

    [13,10,15,3,4,16,9,14,2,1,8,5,11,12,6,7,0].

All indices in this report are zero-based. Point 8 is the unique
real CM point, root 2 is the unique real polynomial root, and the
oriented CM generator at point 8 has negative imaginary part.
The arithmetic Frobenius at (31,beta-19) acts by the saved root
cycle, and that prime has class 3 in the saved class generator.

The proof uses an exact negative normalizer, a point-fixing unit
witness, rational root disks, an integral field-norm argument and
a rank-271 finite-field certificate. It does not trust the old
complex/p-adic root-order comparison or any differential values.

**No independent Shimura tangent or higher jet has been evaluated.**
This closes the labeling gap. The saved numerical frame matrices,
the chosen actual G12 pivot and the analytic truncation errors still
need certificates. The candidate and target field polynomial remain
unidentified and unconstructed, respectively.

## 1. Inputs and distinctions

Retain the fields

    F=Q(b),   b^8-8*b^6+20*b^4-16*b^2+2=0,
    M=F(beta),   beta^2=-2-b,
    L=Q(theta),   [L:Q]=17.

The split real place has 0<b<1. The quaternion algebra is
B=(b-b^2,-1), with generators I,J and K=IJ. The saved maximal
order and seventeen elliptic generators are those exported in D59.

[D105](cm-frame-arithmetic-d105.md) identifies the polynomial
splitting field with the CM Hilbert class field H, of degree 272.
Its Galois group on the roots is the full affine group AGL1(F17).
It also proves that the saved element gamma(beta) generates M
and has the saved degree-16 resolvent as its minimal polynomial.
These results did not require the numerical root matching.

[D106](cm-rational-frame-jets-d106.md) proves Aut(C_Qbar,D)=1
and compatible Q-descent. The isomorphism of the residue field of
D with L is unique. The present task is to identify its embeddings
in the saved analytic point order. The exact CM ideal classes
from [D59](cm-orbit-recognition.md) are reused; their numerical
orientation and root matching are replaced by the proofs below.

## 2. A negative normalizer identifies the real CM point

Conjugation by I fixes the 1,I coordinates and negates the J,K
coordinates. [Script 390](../pari/390_cm_real_structure.py) verifies
that this carries the full saved order lattice onto itself:
its matrix on the integral basis is integral and squares to the
identity. The reduced norm is b^2-b, negative at the split place
and positive at all seven other real places.

Therefore

    rho_I(z)=I*conjugate(z)

is an antiholomorphic involution of the upper half-plane quotient C.
It normalizes the positive normalizer group and preserves the
order-two elliptic divisor D. The Q-model from D106 has its own
complex conjugation, also preserving D. Composing these two
antiholomorphic maps gives a holomorphic D-marked automorphism.
By D106 rigidity it is the identity. Thus rho_I is the actual
complex conjugation on this marked Q-model.

This argument avoids having to choose a new adelic real-structure
comparison. For context, the general canonical-model formulation is
[Blasius--Guerberoff, section 2.2, especially the discussion after
Lemma 2.2.4](https://msp.org/ant/2017/11-10/ant-v11-n10-p02-s.pdf).
Their later theorem about descent from a CM reflex field is not
needed: here the real structure is identified by uniqueness.

Let beta0 be the oriented quaternion at saved point 8, with
beta0^2=-2-b. Put

    beta'=-I*beta0*I^(-1),      u=beta'+beta0.

The exact intertwining identity is beta'*u=u*beta0, and nrd(u)
is totally positive. The saturated intersection ideal

    a={x in M : u*iota0(x) in O}

has class zero. Script 390 verifies the lattice intersection and
the norm identity N(a)*N(nrd(u))=1, which proves
iota0(a)*O=u^(-1)*O as in D59.

[Script 392](../pari/392_cm_matching_witness.py) supplies a stronger,
directly replayable witness: a principal generator t of a, giving

    U=u*iota0(t) in O^*,       nrd(U) totally positive,
    U*beta0*U^(-1)=-I*beta0*I^(-1).

The artifact contains the power coordinates of t and U, as well
as integral order coordinates of both U and U^(-1).
[Review 393](../pari/393_cm_root_matching_review.py) verifies these
quaternion identities with independent rational arithmetic.

Set W=U^(-1)*I. Then W normalizes O, has negative split determinant,
and anticommutes with beta0. Its exact reduced norm is

    -54+33*b+415*b^2-268*b^3-358*b^4+215*b^5+79*b^6-45*b^7.

The map z -> W*conjugate(z) fixes the upper-half-plane eigenline
of beta0: conjugation changes its imaginary eigenvalue's sign,
and anticommutation changes it back. Because U belongs to the
positive group, rho_W and rho_I induce the same map on C.
Hence saved point 8 is fixed by actual complex conjugation.

Complex conjugation in AGL1(F17) lies over the order-two element
of Gal(M/Q)=C16, so it acts on the C17 subgroup by inversion.
Since point 8 is fixed and has ideal class label zero, its action
on the labels is c -> -c. Exactly one label is fixed. In particular,
point 8 is the unique real CM point. This conclusion uses neither
the saved X,Y values nor their numerical conjugate-pair residuals.

## 3. Fix the complex embedding of the CM field

It is necessary to use the same matrix embedding as the saved
domain software. In
[Rickards's fdom.c, afuch_make_m2rmats](../vendor/rickards-fdom/fdom.c),
when a=b-b^2>0, the embedding is

    q0+q1*I+q2*J+q3*K  |->
      [q0+q1*sqrt(a), -(q2+q3*sqrt(a));
       q2-q3*sqrt(a),  q0-q1*sqrt(a)].

The alternative convention with both off-diagonal signs reversed
changes the archimedean orientation and must not be substituted
silently.

For a real matrix [A,B;C,D] fixing z in the upper half-plane,
the eigenvalue on the line (z,1) is C*z+D; its imaginary part has
the sign of C. At beta0, the lower-left entry is

    beta0_J(b)-beta0_K(b)*sqrt(b-b^2) < 0.

Review 393 proves this inequality by rational interval arithmetic.
An exact Sturm calculation isolates the unique root b in (0,1);
rational square bounds enclose sqrt(b-b^2). The result is

    beta_complex=-i*sqrt(2+b).                                (1)

This agrees with D59's numerical sign, but no numerical disk action
is used to prove it. The same Sturm calculation places all eight
roots of the F polynomial in (-2,2), so every conjugate of beta
has absolute value below 2.

## 4. Certify the polynomial roots and the resolvent identity

Write r_0,...,r_16 for the roots in the saved D59 complex order.
Script 392 uses 4096-bit Newton iteration only to propose centers.
The saved centers have rational real and imaginary parts with
common denominator 10^1100.

For each center c, review 393 proves that the disk

    |z-c| < 10^(-1080)

contains exactly one root. It uses the linear part f'(c)*(z-c)
and bounds the remaining Taylor terms by

    |f(c)| + M*radius^2,
    M=sum_(j>=2) |f_j|*2^j*8^(j-2).

Here |c|<8 and radius<8. Clearing denominators gives an integer
inequality in which the linear term exceeds twice the remainder.
[Rouche's theorem, for example Tao's Theorem 37](https://terrytao.wordpress.com/2016/10/11/math-246a-notes-4-singularities-of-holomorphic-functions/)
then counts one root in the disk. The seventeen disks are disjoint,
so they exhaust the roots. Each lies within 10^(-70) of its old
saved center. The disk at index 2 is invariant under conjugation;
all others avoid the real line. Thus r_2 is the unique real root.

The same check certifies one disk for beta in (1), with purely
imaginary center. Symmetry under z -> -conjugate(z) proves the root
is purely imaginary; beta^2=-2-b and the isolated b interval fix
which root it is. No ball-arithmetic library is trusted for these
disk certificates.

Let f be the proposed saved 17-cycle, and define

    kappa_f=sum_i r_i^2*r_(f(i)).

At this stage f is only a permutation proposal. Define the exact
CM element

    gamma=-beta^13-5*beta^12-12*beta^11-59*beta^10-55*beta^9
          -264*beta^8-119*beta^7-558*beta^6-114*beta^5
          -559*beta^4-15*beta^3-218*beta^2+28*beta-10.

The root disks and a polynomial Lipschitz bound give

    |kappa_f-gamma| < 10^(-1000).                             (2)

This is checked after clearing all denominators. To make (2) an
exact identity, set delta=kappa_f-gamma. All r_i and beta are
algebraic integers in H. That beta belongs to this concrete copy
of H follows from D105's field identification and M/Q being Galois.
Therefore delta is an algebraic integer in a field of degree 272.

Every conjugate of kappa_f has absolute value below 17*4^3=1088,
even before f is known to be a Galois permutation. Every conjugate
of gamma is bounded directly using |beta|<2. Consequently

    |sigma(delta)| < 1088+sum_j |gamma_j|*2^j = 275090.

Since H is totally imaginary, (2) also holds at the distinct
conjugate embedding. If delta were nonzero, its integer norm would
satisfy

    1 <= |N_(H/Q)(delta)|
       < 10^(-2000)*275090^270 < 1,

a contradiction. Hence

    kappa_f=gamma                                             (3)

exactly. The audit additionally checks the alternative one-embedding
bound 10^(-1000)*2176^271<1, using D105's sharper resolvent-root
bound; the two-embedding proof above does not need that sharper
bound. Flipping beta's sign or replacing f by f^(-1) fails the
matching controls by more than 10^(-3) at the centers, far beyond
the certified uncertainties.

## 5. Prove that the proposed cycle is a Galois action

An equality of one resolvent value alone would not automatically
certify a proposed root permutation. The following finite rank
certificate supplies the missing implication.

Consider the 272 ordered-pair monomials

    m_ij=r_i^2*r_j,       i != j.

The polynomial's first three power sums are 2,4,8. Thus

    sum_(i!=j) m_ij = (sum_i r_i^2)*(sum_j r_j)-sum_i r_i^3
                   = 4*2-8 = 0.                              (4)

[Magma 391](../magma/391_cm_root_pair_rank.m) and independent
Python arithmetic in review 393 prove that (4) is their only
rational linear relation.

Here is why the finite matrix proves that statement. At 31 the
polynomial is irreducible and separable. Its residue roots can be
written s_i=alpha^(31^i), indexed by i in F17. The normal C17 in
the proved Galois group is generated by Frobenius. Its normalizer
in S17 has order 272, so the full Galois group is exactly that
normalizer, with actions i -> a*i+b.

For each a=1,...,16, evaluate all s_(a*i)^2*s_(a*j) in
F_(31^17), and expand in the power basis of alpha. Stacking these
sixteen blocks gives a 272-by-272 matrix over F31. Its rank is
**271**, with kernel spanned by the all-ones vector.

These blocks are reductions of actual Galois conjugates under
representatives for the sixteen Frobenius cosets. A nonzero
271-minor remains nonzero over Q31, so the rational relation space
has dimension at most one. Relation (4) proves it has exactly
dimension one. This argument concerns the complete set of
ordered-pair monomials and does not assume any complex/p-adic
root-index comparison.

It follows that distinct directed 17-cycles have distinct kappa
values. Indeed, the difference of two cycle incidence vectors
would be a rational relation with coordinate sum zero. A multiple
of the all-ones relation can have sum zero only if it is zero.

By D105, gamma generates M. Equation (3) therefore makes the
stabilizer of kappa_f equal to Gal(H/M), of order 17. For any
sigma in this subgroup,

    kappa_(sigma*f*sigma^(-1)) = sigma(kappa_f) = kappa_f.

The cycle-separation result forces sigma to commute with f. The
centralizer of a 17-cycle in S17 is its cyclic group. Hence

    Gal(H/M)=<f>.

In particular, f really is a Galois automorphism, without trusting
Magma's old complex Galois calculation or GaloisGroupConjugation.

## 6. Identify the prime and propagate the reference point

The review independently Hensel-lifts all seventeen roots to

    (Z/31^8)[alpha]/(f_L(alpha)).

Their reductions are alpha^(31^i), so arithmetic Frobenius carries
the i-th lifted root to the (i+1)-st. Summing its cubic expression
gives the scalar

    kappa_31 = 235040037749 mod 31^8.

This agrees with the old saved 31-adic result, but is recomputed
without its root numbering. The sixteen simple residue roots of
the M polynomial are also independently lifted. Evaluating gamma
on them gives sixteen distinct values modulo 31^8. Exactly one
matches kappa_31:

    beta = 79944587169 mod 31^8,       beta = 19 mod 31.

The exact degree-16 resolvent from D105 is both the polynomial of
these gamma values and the polynomial of the Frobenius-cycle sums.
Thus distinct local neighborhoods identify the algebraic root
exactly, not merely by a congruence of unrelated elements. By
cycle separation, the arithmetic Frobenius at

    q=(31,beta-19)

is precisely f. Script 390 recomputes [q]=3 in the saved class
generator, accounting for any different generator returned by
the class-group software.

We retain the D59 reciprocity convention: if
iota(a)*O=xi*O, arithmetic Artin action sends the CM point z to
xi^(-1)*z. The explicit convention is in
[Voight, Theorem 5.1 and Algorithm 5.2](https://jvoight.github.io/articles/shimcm-fixed-errata.pdf);
the general totally real canonical-curve setting is described in
[Voight, section 4.3](https://jvoight.github.io/articles/shimura-clay-proceedings-071707.pdf).
Only the underlying CM reciprocity is used, not the triangle-group
parametrization or the separate descent assertions in the former paper.

Point 8 and r_2 are the unique real points in their respective
degree-17 orbits. D106's unique Q-algebra isomorphism must identify
them. The f-cycle beginning at r_2 is

    [2,4,7,12,10,5,16,1,14,13,0,15,6,9,11,8,3].

A saved point with class label c corresponds to entry 6*c mod 17
in this cycle, since 6 is the inverse of 3 modulo 17. This produces
exactly the lookup stated at the start of the report. Its conjugation
pairs agree with c -> -c.

## 7. Consequence for the construction

The old lookup can now be used as the arithmetic labeling for
D106's rational residue frame. Applying the cofactor/residue
normalization to the **true** differential evaluations in this
point order gives that Q-frame up to a common scalar. The degree-17
jet-height bounds and Galois propagation now have certified labels
for the saved complex CM points.

This does not validate the old approximate differential evaluations
or their approximate change matrices. It does not establish a
nonzero actual G12, supply a tangent, identify the candidate,
or prove the downstream P32 and degree-nine branch markings.

The next bounded task is to make an independent tangent evaluator
produce a certified enclosure in this now-identified frame, with
a certified chart. Compare the existing complex spectral approach
with an executable arithmetic alternative before increasing
precision or enumeration. D98's interval still contains zero;
its spectral pilot gate and the resource pauses remain unchanged.
The 31-adic equality test from D106 remains available, but this
root-matching computation is not a 31-adic Shimura evaluator.

The 4096-bit root calculation was a fixed, small-degree algebraic
certificate with an explicit norm threshold. It did not expand the
spectral census, refine a differential bank, or resume the paused
cubic coefficient search.

## 8. Audit and reproduction

The successful real-structure job took 4.30 seconds; the root-pair
rank job 1.06 seconds; the witness job 3.97 seconds; the independent
rational probe 1.60 seconds. Every job used the existing 180-second
private-process-group cap. Two implementation failures are preserved:
Sage's quaternion truth-value conversion, and an unavailable
ComplexField.real_field method. Neither produced a result artifact.

Review 393 preserves every one of the 562 D106 source hashes and
binds the new witnesses, sources, job receipts, this report and the
[source ledger](../data/computed/cm_root_matching_sources_d107.json).
Completed sources 390--393 and bound artifacts are frozen.
Recheck from the repository root:

```sh
python3 dembele/pari/393_cm_root_matching_review.py --check
```

The independent review certifies integer/rational inequalities,
quaternion identities, the finite rank and local lifting calculations.
Its geometric use of marked rigidity and CM reciprocity is the
mathematical proof above, not a machine-verified theorem.
