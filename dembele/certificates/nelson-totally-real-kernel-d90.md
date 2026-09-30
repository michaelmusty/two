# D90: local components of a totally real Shimizu evaluator

Date: 2026-09-23. The user asked to proceed with Paul D. Nelson's
[*Evaluating modular forms on Shimura curves*](https://arxiv.org/pdf/1210.1243).

**Result:** the local arithmetic and derivative components now have a
working implementation tied to our actual quaternion order. We also
implemented and calibrated a scalar Mellin kernel for the proposed
degree-eight unfolding. This is progress toward an independent evaluator;
**no global theta lift, Shimura differential coefficient, or arithmetic
CM tangent has yet been evaluated.**

The new programs read the exact quaternion export in `cm_orbit.json`.
They read no candidate curve equations, candidate jets, or numerical
differential banks. All six bounded jobs have finished. The three failed
development runs, their sources and their logs are retained.

## 1. Fix the representation and the Fourier character

The algebra is the indefinite

    D=(b-b^2,-1) over F=Q(b),
    b^8-8b^6+20b^4-16b^2+2=0.

It splits at the real place with b approximately 0.39018 and is definite
at the other seven places. Use the saved maximal order O in D. The
forms on the genus-16 normalizer quotient come from the four quartic
orbits in the level-p2-new Hecke module, with U_p2=+1 in the package's
convention. Their saved T31 polynomials are

    t^4 - 8t^3 - 36t^2 + 433t - 899,
    t^4 + 2t^3 - 56t^2 + 133t - 19,
    t^4 + 7t^3 - 51t^2 - 407t - 359,
    t^4 + 17t^3 + 69t^2 - 87t - 649.

This identification is the historical exact calculation in
`f16_steinberg.out`, now bound by the D90 audit. The level-one
16-dimensional target representation is a different Hecke module.

For a Fourier transform over F, the field different must be included.
The new calculation proves exactly that

    pi=2+b is totally positive, Norm(pi)=2,
    delta=16/(2+b) is totally positive,
    (delta)=Different(F/Q)=(pi)^31, Norm(delta)=2^31.

Let O# denote the dual for the F-valued reduced-trace pairing. For the
standard trace character, the annihilator of O is delta^(-1) O#.
For the global character psi_delta(x)=psi(x/delta), the finite character
at p2 has conductor O_F and the annihilator is O#. The real character
changes at the same time: its v-component is exp(2*pi*i*x/delta_v).
Changing the finite character without this real scaling would be wrong.

The program constructs both absolute Gram matrices, on the actual
32-element Z-basis:

    G[i,j]  = Tr_F/Q Trd(e_i*conjugate(e_j)),
    G0[i,j] = Tr_F/Q (Trd(e_i*conjugate(e_j))/delta).

Their absolute determinants are respectively 2^126 and 4. The Smith
invariants of G0 are thirty 1s and two 2s. The equality between the two
dual lattices after multiplication by delta is checked by an integral
change of determinant one. The program also checks O# has reduced norms
in pi^(-1) O_F, including all bilinear cross terms.

Consequently the self-dual additive volume of O is 2^(-63) for the
standard character and 1/2 for the normalized character. Neither is an
arbitrary choice of Haar measure after the character is fixed.

There is an additional exact finite check. On O#/O the quadratic form

    q(x)=Tr_F/Q(Nrd(x)/delta) modulo Z

takes values 0,1/2,1/2,1/2. Its Fourier matrix is a four-by-four sign
matrix divided by 2, its square is the identity, and its normalized
Gauss sum is **-1**. These supply the finite Fourier normalization and
sign for the division-place test lattice. Assembling them with the
Hilbert newvector and global measures remains a separate step.

## 2. The real-place derivative kernel

At the split place, write

    X([a b;c d])=(a+d+i*(b-c))/2,
    Y([a b;c d])=(a-d+i*(b+c))/2,
    Nrd=|X|^2-|Y|^2, P=|X|^2+|Y|^2.

The weight-two split test function is proportional to
`X^2/delta_0 * exp(-2*pi*P/delta_0)`. At each definite real place,
parallel weight two corresponds to the trivial quaternionic compact
representation; its test function is the Gaussian
`exp(-2*pi*Nrd/delta_v)`. Thus there is one polynomial Gaussian factor
and seven ordinary Gaussian factors. Eight copies of the split formula
would give the wrong real-place kernel.

For the split derivatives, let p_(a,b)(y,ybar) start at p_(0,0)=1, with

    p_(a+1,b) = ybar*p_(a,b) - d/dy p_(a,b),
    p_(a,b+1) = d/dybar p_(a,b) - y*p_(a,b).

The implementation checks all 36 pairs 0<=a,b<=5 against both the
Laguerre expression and direct differentiation of the polynomial
Gaussian. If h=4*pi*t, where t is the scaled split height, the derivative
polynomial multiplying the Gaussian is

    X^(2+a+b) sum C_(e1,e2) h^((a+b+e1+e2)/2) Y^e1 Ybar^e2.

The three pairs needed with a first-derivative anchor are particularly
small:

    p_(1,1) = 1 - y*ybar,
    p_(3,1) = 3*ybar^2 - y*ybar^3,
    p_(5,1) = 5*ybar^4 - y*ybar^5.

The lower-degree terms must be retained. For example, dropping the 1
from p_(1,1) is rejected by the exact check.

For the centered disk coordinate w=(z-z0)/(z-conjugate(z0)), a
weight-two differential has coefficient of w^j dw equal to

    2*i*y0^(j+1) * delta^j(f)(z0)/j!.

This conversion is checked on all Taylor monomials through degree five,
using the varying-height term in the successive raising operators.
On C, invariance under w -> -w forces f(z0)=0 in the upstairs chart.
Therefore a value anchor at this order-two CM point would annihilate
the desired pairing. Use a nonzero first derivative, or a non-CM anchor.
The derivative orders 1,3,5 then supply D89's three coarse coefficients;
the global lift has not yet supplied their values.

## 3. Actual CM lattices and a bounded enumeration

Use the saved reference CM point, index 8, with beta^2=-2-b. Conjugation
by beta preserves O. Its +1 and -1 eigenspaces are K and K-perpendicular,
each of Q-dimension 16. The program computes the two integral
intersections and proves

    [O : (O intersect K) + (O intersect K-perpendicular)] = 2^16.

The quotient has sixteen nontrivial Smith invariants, all equal to 2.
Hence the CM specialization is a sum over **65,536 matching cosets** of
products of rank-16 lattice sums. Replacing it by a single product of
the two intersection-lattice theta series loses terms. This is the
concrete version of the translated-lattice decomposition suggested in
Nelson's section 3.5; it is not a claim that all those sums should be
enumerated separately.

The natural positive CM majorant, with the character scaling, is

    M(x) = P_0(x)/delta_0 + sum_(v != 0) Nrd_v(x)/delta_v.

We construct an exact rational positive quadratic form Q on O satisfying

    (99/100)*M <= Q <= (101/100)*M.

To do this, project x to its commuting and anticommuting parts. A field
element c is chosen whose value is within 1/100 of -1 at the split
place and +1 at the other seven places. Then

    Q(x)=Tr_F/Q((Nrd(x_parallel)+c*Nrd(x_perpendicular))/delta).

All eight coefficient inequalities are independently proved by rational
interval arithmetic, using disjoint sign-changing intervals that exhaust
the eight roots of the field polynomial. The Gram matrix of Q is
rational and positive definite. Both
enumerations use this exact rational matrix, with denominators cleared,
and retain the integral reduction matrix and every returned vector.

| Bound on Q | Vectors, counting both signs | Pure K | Pure K-perpendicular | Mixed |
|---|---:|---:|---:|---:|
| 1.01 | 30 | 30 | 0 | 0 |
| 2.02 | 9,910 | 452 | 98 | 9,360 |

Every mixed vector in the second shell lies outside the direct sum of
the two intersection lattices. Thus this small calculation already
detects the terms lost by discarding the cosets. The first shell alone
cannot test the higher derivative kernels: its Y coordinate is zero.
These are finite lattice shells, **not truncation bounds for the full
theta lift**. The second shell took 3.334 seconds including Sage startup.

## 4. A scalar Mellin integral is implemented, but the global sum is pending

For a norm-positive term, integration of the split-height factor gives
Gamma(s+2+r), where r is the polynomial's height degree. The other seven
Gaussian height integrals give Gamma(s+1)^7. Combining formally with
the Gamma factors in the completed Dedekind zeta factor suggests the
scalar building block

    J_(d,k)(Z) = (1/(2*pi*i)) integral_(c)
        (2s-1) Gamma(s)^d Gamma(s+1)^(d-1) Gamma(s+k) Z^(-s) ds.

The implemented numerical prototype evaluates this function. For d=1,
it is independently compared with the closed Bessel expression

    2*Z^(k/2) * (2*sqrt(Z)*K_(k-1)(2*sqrt(Z))-K_k(2*sqrt(Z))).

The three calibration cases agree with relative/absolute scaled errors
at most 8.02e-44. For d=8, the six shifts k=3,...,8 needed by the
three derivative pairs are evaluated at Z=1 on contours Re(s)=1.25 and
1.75; they agree to the working precision. The calculation uses 50
decimal digits and an imaginary cutoff of 40. These are numerical
checks, not interval bounds on quadrature or tails.

**This does not establish a totally real analogue of Nelson's Theorem
3.9.** In particular, we have not fixed the full cusp coefficients,
unit quotient, scalar argument Z, or all global measure factors. The
scalar function is available for that assembly; it is not itself the
derivative of a Shimura form. No Hecke-weighted quaternion sum was
evaluated in D90.

## 5. Next calculation and verification

The next bounded target is to finish the Hilbert unfolding for this
specific test vector: specify the two cusp contributions at p2, the
quotient by central units, the Fourier coefficient indexed by each norm
ideal, and the measure/argument factors. Then evaluate one eigenform
from the first quartic orbit at one CM point, using derivative pairs
(1,1) and (3,1), with an explicit truncation estimate. This would be the
first independent differential calculation in this route. The existing
CM frame can subsequently absorb separate eigenform scales; its saved
numerical values cannot be substituted for the new derivatives.

Nelson's explicit theorem is for Q; Remark 5.1 leaves the totally real
application for further work. D90 executes local pieces and a formal
scalar-integral prototype. It does not silently import the missing
global theorem or turn numerical recognition into an exact certificate.
The later passage to arithmetic jets and D88's exact rank/kernel test
also remains open.

Recheck the new certificates with standard Python:

```sh
python3 dembele/pari/326_nelson_kernel_audit.py --check
```

This independently checks the dual Gram inverse/determinant, finite
quadratic and Fourier forms, derivative polynomials, CM splitting/index,
and every one of the 9,910 stored shell vectors and its classification.
Enumeration completeness uses PARI's `qfminim`; the replay validates the
saved vectors without pretending to implement a second enumerator.
It rejects a Fourier-sign corruption and an omitted derivative term,
and verifies 27 file hashes. It also proves the eight real-place
majorant inequalities using rational intervals. The numerical Mellin result remains a
hash-bound numerical calibration.

Root `nelson_kernel_d90.json` includes the earlier `nelson_d90.json`
manifest and binds all six jobs: three passes and three
retained failures (a Sage cache path, a Sage rounding interface, and
incorrect rational `%1` in an initial Fourier check, replaced by
subtracting the floor). Each had a 180-second process-group timeout;
the longest took 9.645 seconds. No remote run, new differential solve,
or precision escalation was launched. D86--D89 artifacts remain unchanged.
