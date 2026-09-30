# The original residual systems in the specified genus-64 Jacobian

Date: 2026-09-15. D51. This supplies the representation argument requested
in D50, together with exact projector polynomials. It uses the standard
local/global Jacquet–Langlands and Shimura-curve cohomology theorems, and
the exact Hecke computations recorded in scripts 58, 63 and 80. It does
not assert that the numerical polygon is interval-certified or that an
algebraic model has been computed.

**Proposition.** Let Y/F be the connected canonical Shimura curve with the
division level specified below. Its Jacobian has two Galois-stable
subspaces of geometric 2-torsion, each of dimension 16 over F2 and two over
F256, affording the two original residual systems in Dembélé's level-one
construction, up to automorphisms of F256. In particular this identifies
their kernels, rather than merely their groups or finitely many traces.

This is a mathematical argument supported by exact input calculations,
not a formalized proof or a computation of geometric torsion points. The
standard theorems and the integral passage used in it are spelled out
below so the arithmetic identification can be reviewed independently.

## 1. Local levels and the characteristic-zero factor

Write p for the unique prime over 2 in F, so the residue field is F2. Let
B be the totally definite quaternion algebra split at every finite place;
let D be the quaternion algebra ramified at p and at seven real places.
The common central character is trivial. At finite places other than p,
all levels are maximal. The parallel weight is two.

On the B side, put K=GL2(O_Fp) and inflate the sign character of
`GL2(F2)=S3` to K. Extend it trivially on central scalars. This is the
unique cuspidal representation of GL2(F2): its restriction to the
nontrivial upper unipotent subgroup is nontrivial, whereas its value on
the order-three elliptic torus is one. The corresponding local
representation of GL2(Fp) is the depth-zero supercuspidal representation
of conductor p² with trivial central character.

On the D side, with P_D the radical of the maximal order, the quotient is

    D_p^* / (F_p^* (1+P_D)) = F4^* semidirect C2 = S3.

The two nontrivial characters of F4^* are Frobenius conjugate. Inducing
either from the order-three subgroup gives Std, the two-dimensional
standard representation of S3. Local Jacquet–Langlands matches this with
the GL2 depth-zero cuspidal type above. Trivial central character removes
any ambiguity from central extensions; the unramified quadratic twist
does not change Std. The level-zero construction and compatibility are
given in Weinstein, §2.2 and Theorems 6.1.1–6.2.1.
[Weinstein, local Jacquet–Langlands](https://www.numdam.org/item/10.5802/jtnb.728.pdf).

Let H be the inverse image of a reflection subgroup in this local S3.
Then `dim Std^H=1`. The trivial representation also has one invariant;
the sign representation has none. Thus the holomorphic differential
space at this division level consists of the 16 old dimensions on C,
plus one copy of the 48-dimensional sign-type automorphic space. This
identifies the characteristic-zero new factor, not only its genus.

Here Y is the canonical level curve, not an arbitrary degree-three cover
having the same branch multiplicities. The local map in script 66 was
computed from the actual quaternion order and has precisely the kernel
in the displayed quotient. Its reflection subgroup gives the degree-three
map Y -> C. Norms of 1+P_D contain all units of Fp (the residue field is
F2), and a reflection lift has norm of odd valuation, so this level has
full reduced-norm image at p. Together with narrow class number one this
gives the connected canonical component over F used here.

Global Jacquet–Langlands preserves the Hecke operators away from p.
The Shimura-curve cohomology construction realizes the transferred
weight-two representations in the Jacobian, with rank two over their
Hecke fields. In this case the finite discrete-series place required in
even degree is p, and the local representation is depth zero. See
Carayol, Theorem B, §0.10 and §2.2. We use covariant Tate modules; dual
or cyclotomic-twist conventions do not change the residual representation
here, where the determinant is one.
[Carayol, Hilbert modular Galois representations](https://numdam.org/item/10.24033/asens.1512.pdf).

## 2. The integral all-Hecke congruence

Let L_sign be the Z2 lattice of sign-valued functions on B's 58 ideal
classes. At a class whose unit stabilizer contains an odd permutation,
an integral value must equal its negative and hence vanish. At the other
classes it is an arbitrary Z2 value. Script 63 computes 48 admissible
classes and ten forbidden ones in the same ideal-class basis as T31.

Reduction gives an injection

    L_sign / 2 L_sign -> L_trivial / 2 L_trivial.

It is injective because the free coordinates on admissible classes are
unchanged. It commutes with every Hecke operator away from p: each
transporter's sign becomes one modulo two. This assertion follows from
the definition of the double-coset action; it does not extrapolate from
the computed T31 matrix. Constants in the trivial module cause no issue:
their T31 eigenvalue is 32 and reduces to zero.

On the ten-dimensional quotient the T31 polynomial is t^10. The original
systems have trace polynomials

    h1 = t^8+t^4+t^3+t+1,
    h2 = t^8+t^6+t^5+t^2+1.

Both are coprime to t^10. Therefore their entire generalized eigenspaces
in the level-one module lie in the image of L_sign/2. Since this is an
all-Hecke injection, their full residual systems agree with the original
ones. The characteristic-zero sign-type space is exactly the p²-new
space: no unramified principal series or Steinberg type contains the
finite cuspidal sign representation, and deeper types have no such
principal-congruence invariants.

The exact degree-48 polynomial P48 of T31 is irreducible over Q, and

    P48 mod 2 = t^32 h1 h2.

Thus each of the two systems occurs once in the differential space. The
degree-16 old polynomial P16 is coprime modulo two to both h_i. These
are exact input checks repeated by script 80 from the saved polynomial
bank; the basis-sensitive stabilizer and quotient computations are in
script 63. The source logs and the earlier all-Hecke explanation are
linked from [the D42 review](review-2026-09-14.md).

## 3. Actual torsion subspaces, not just semisimplifications

Put `P=P16 P48`, of degree 64. T31 on the characteristic-zero Tate module
has characteristic polynomial P² and is annihilated by P. Indeed the
Hecke eigenvalues in the differential space are distinct, and each has
rank two in the Tate module. Since the Tate lattice is Z2-free, this
integral polynomial identity persists on J(Y)[2].

Write pbar for P modulo two and `q_i=pbar/h_i`. Because h_i is simple in
pbar, choose a_i with `a_i q_i = 1 mod h_i` and set

    e_i(t) = a_i(t) q_i(t) mod pbar(t).

Then `e_i^2=e_i`, `e_1 e_2=0`, and `h_i e_i=0` modulo pbar. Hence

    V_i = e_i(T31) J(Y)[2]

is a genuine Galois-stable subspace: the geometric Hecke correspondence
T31 is defined over F and commutes with Galois. Stability does not come
from treating one local Frobenius as a global endomorphism.

The corresponding simple factor of the Hecke algebra at 2 is unramified
of degree eight, by Hensel's lemma and the simplicity of h_i. Its integer
ring is generated by T31 locally. The projected Tate lattice is torsion
free over this discrete valuation ring and has rank two; reduction
therefore gives `dim_F2 V_i=16`, with an F256 scalar action and dimension
two over F256. This also explains why a separate full integral comparison
of the two homology lattices is unnecessary.

Every other integral Hecke operator acts through that local integer ring:
in characteristic zero it is in the Hecke field, and its eigenvalue is
integral. Its residue is the scalar eigenvalue identified in §2. Thus at
every prime l away from 2 the residual characteristic polynomial on V_i is

    X^2 - a_l(original system i) X + 1.

The original representation is absolutely irreducible over F256. The
cohomological compatibility theorem, Chebotarev and Brauer–Nesbitt identify
the semisimplification of V_i with it. As both have dimension two over
F256 and the latter is irreducible, V_i itself is irreducible and
isomorphic to it. A residue-field automorphism changes the chosen trace
root but does not change the kernel. This proves the proposition.

## 4. Exact certificate and its limits

Run:

```sh
/Applications/Magma/magma -b dembele/magma/80_target_projectors.m
```

The script checks irreducibility of P48, squarefreeness of P over Q,
the stated mod-two factorization, separation from the old part, and the
two CRT identities. It writes all coefficients of pbar, h_i and e_i to
`../data/computed/target_projectors.json`. The log has the readable
projector polynomials. A companion-module check gives rank eight for
each projector on F2[t]/pbar, consistent with rank sixteen on the Tate
module. The companion matrix is explicitly not a computed H1 matrix.

This closes the abstract representation-occurrence argument for the
specified canonical level, subject to the stated standard theorems and
the recorded exact Hecke input. It does not implement Hecke
correspondences on divisor coordinates, construct the algebraic curve,
compute torsion, or certify a polynomial. A future recognized curve must
still be identified with this canonical Y before this proposition applies
to its Jacobian. The numerical-domain identification and coefficient
recognition remain separate checks.
