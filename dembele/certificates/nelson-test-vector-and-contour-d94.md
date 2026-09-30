# D94: contour limits and a nonzero local test-vector calculation

Date: 2026-09-23. Continuation of
[D93](nelson-prime31-and-global-tail-d93.md), authorized by “continue”.

**Result:** moving the contour reduces the bound for all uncomputed
norm ideals from approximately 2.685e16 to **less than 2.680e13**.
This remains over three billion times the current `(1,1)` partial sum
of about 7641. Small polynomial changes of the residue weight offer
little further improvement in the tested family. More quadrature
precision or another small displacement cutoff is not justified by
these bounds.

Separately, the actual local Schwartz functions have a **nonzero
norm-one matrix-coefficient contraction at every place**. With the
measures specified below, the finite factors are 1 and the product
of the eight real factors is exactly **exp(-2*pi)**. This removes a
local nonvanishing question. It does not yet identify the D91 classical
integral with the global similitude lift, verify its Petersson scalar,
or prove that the first derivative at the chosen CM point is nonzero.

## 1. Test the contour before extending the enumeration

Keep the corrected D93 inputs, including

    Z0 = (4*pi^2)^8/2^62,
    D_odd(s) = zeta_F(s)^2*zeta_F(s-1)^2/zeta_F(2*s-1) / F_2(2^(-s)),
    F_q(x) = (1-q*x^2)/((1-x)^2*(1-q*x)^2).

For c>3/2, define C_c=1/(1-(2/9)^c). The D93 bound for all ideals
other than the unit ideal and the saved prime `(31,b-27)` is

    E_a(c) = Z0^(-c)*(B_(c,a,2)+B_(c,a,a+2))*C_c
             *[D_odd(c+1/2)-1-64*31^(-c-1/2)].

Here a=1,3,5 denotes the pair `(a,1)`. The 64 is
`d(p)*sigma_1(p)=2*32`. No new Hecke coefficient is required to
compute this majorant.

Script 355 uses 320-bit Arb interval rectangles of width 1/128 on
0<=t<=16 to bound the absolute Mellin constants. For 3/2<c<=2,
[Binet's remainder formula](https://dlmf.nist.gov/5.9.E10_2) gives

    |Gamma(c+it)| <= sqrt(2*pi)*|c+it|^(c-1/2)
                     *exp(1/(12*c))*exp(-pi*t/2).

Indeed the remainder has modulus at most 1/(12*c), while
`-c-t*arg(c+it)<=-pi*t/2`. Consequently

    |Gamma(c+it)|^16
       <= 8^8*exp(4/(3*c))*(2+t)^24*exp(-24*t).

The other factors are bounded by a polynomial with positive rational
coefficients. Its tail integral from 16 to infinity is an exact finite
factorial sum times exp(-384). The audit replays this polynomial and
factorial sum. Gamma, zeta and exponential balls are bound to the
successful Arb run. All exported endpoints use `.exact_rational()`.

| Contour c | `(1,1)` omitted-ideal bound, rounded up |
|---|---:|
| 193/128 | 3.679e14 |
| 97/64 | 1.157e14 |
| 49/32 | 4.522e13 |
| 25/16 | **2.680e13** |
| 13/8 | 3.477e13 |
| 7/4 | 2.030e14 |
| 2 | 2.685e16 |

The best tested unchanged-kernel bound before rounding is about
2.6795251840316894e13. This is a bound, not the actual error. Moving
this contour changes no finite summand: the kernel is holomorphic
between these lines, and its vertical decay justifies the shift.
It can therefore be used with the corrected D93 partial sums.
The full enclosure still contains zero by a very large margin.

Near c=3/2 the divisor mass grows; farther right the inverse power of
the small Z0 and the Gamma constants grow. The tested balance occurs
at c=25/16 for all three pairs. This is a finite search, not a proof
of the optimal contour or a lower bound on every possible method.

## 2. Polynomial residue weights do not resolve this bound

[Nelson, section 5.6, equation (18) and Theorem 5.6](https://arxiv.org/pdf/1210.1243)
allow a holomorphic weight H with H(0)=0, H(1)=1 and polynomial
growth on vertical strips. The integrand multiplier is H(s)-H(1-s).
We adapt the residue argument using D91's completed Hilbert Eisenstein
series; Nelson's Remark 5.1 does not supply an explicit degree-eight
formula.

For r=c(c-1), script 355 tests

    W_m(s) = (2*s-1)*(1-s*(s-1)/r)^m,
    H_m(s) = (1+W_m(s))/2,  m=0,1,2,4.

Exact polynomial arithmetic checks W_m(1-s)=-W_m(s) and the two
endpoint conditions. The tail proof adds the positive polynomial
bound `|1-s(s-1)/r|<=1+(2+t)*(1+t)/r`. There are 28 contour/weight
choices, each covering all three derivative pairs.

| Weight power m | Best tested c for `(1,1)` | Bound, rounded up |
|---|---|---:|
| 0 | 25/16 | 2.680e13 |
| 1 | 25/16 | 2.257e13 |
| 2 | 25/16 | 2.710e13 |
| 4 | 13/8 | 6.649e13 |

For m>0, the identity preserves the underlying full integral, but
**changes the contribution of each finite family**. These new bounds
must not be attached to D93's unchanged partial sums. No revised
partial sums were computed, and none are claimed. The tested gain
does not warrant adopting a new weight or rebuilding the coefficient
bank. Other weight families have not been excluded.

## 3. Calculate a local norm-one contraction directly

Write G_v=B_v^1, and let m_v be the matrix coefficient dual to the
chosen quaternionic fixed vector, normalized at the identity. We
calculate the following explicitly defined local functional:

    I_v = integral_(G_v) phi_v(g)*m_v(g) dg.

The inverse/conjugation convention matters. This formula pairs the
weight +2 polynomial with the coefficient of weight -2. In a forward
theta formula written with phi(g^(-1)), the corresponding matrix
coefficient must be inverted as well.

At every finite place phi_v=1_(O_v). Conjugation preserves the actual
order, and a norm-one element has inverse equal to its conjugate.
Thus `O_v intersect G_v=O_v^1`. The selected vector is fixed by
O_v^times, so m_v=1 on this support. Normalize vol(O_v^1)=1 to obtain
**I_v=1**. This argument also applies at the division place; it does
not need a choice of uniformizer eigenvalue on the norm-one subgroup.
Script 356 computes the integral 32-by-32 conjugation matrix and its
square on the saved order, and the identity's integral coordinates.

At a definite real place the parallel-weight-two quaternionic type
is trivial on G_v. With probability Haar measure on this compact
group, Nrd(g)=1 gives

    I_v = exp(-2*pi/delta_v) > 0.

At the split real place use D90's X,Y,P and

    phi_0(g)=X(g)^2/delta_0 * exp(-2*pi*P(g)/delta_0),
    m_0(g)=X(g)^(-2).

The matrix coefficient can be obtained from the weight-two Bergman
model on the disk: evaluation at the origin is pairing with the
constant lowest vector, and the automorphy factor supplies the inverse
square. We choose the dual action for which m_0(k_theta)=exp(-2*i*theta).
This fixes the convention independently of a choice of right versus
left action in a theta formula.

In Cartan coordinates g=k_1*a_r*k_2, put t=exp(r/2). Up to the compact
phases, X=(t+t^(-1))/2 and Y=(t-t^(-1))/2. Then

    |X|^2-|Y|^2=1,  P=cosh(r),
    phi_0(g)*m_0(g)=delta_0^(-1)*exp(-2*pi*cosh(r)/delta_0).

Give K mass 1 and G_0/K the standard hyperbolic area measure. Radial
integration has density 2*pi*sinh(r), hence, with u=cosh(r),

    I_0 = (2*pi/delta_0)*integral_1^infinity exp(-2*pi*u/delta_0) du
        = exp(-2*pi/delta_0) > 0.

This also shows why merely asserting “the Gaussian is positive” would
not suffice. If the dual coefficient is replaced by its complex
conjugate, a weight-four angular factor remains and its K average is
zero. The artifact records that negative control.

Finally delta^(-1)=(2+b)/16 and Tr(b)=0, so

    Tr_F/Q(delta^(-1))=1,
    product_(v real) I_v=exp(-2*pi),
    product_(all v) I_v=exp(-2*pi)

with the local measure choices just stated. Script 356 checks the
field trace, norm of delta, positivity at all eight isolated roots,
the split norm identity and the Cartan identities exactly. The
standard-Python audit independently replays the field and order
arithmetic. The analytic integral follows from the displayed change
of variable; this is not a numerical estimate of a CM value or the
Tamagawa-normalized global Petersson scalar.

## 4. What the sources establish, and the precise remaining comparison

[Disegni, section 5.1](https://arxiv.org/pdf/1510.02114), treats Shimizu
lifting over a number field, with the local one-dimensional intertwining
space, global target pi tensor pi-dual, and local factorization. Its
Schwartz space is S(B_A times A^times), with a similitude variable u.
Equations (5.1.1)--(5.1.3) give explicit normalization conventions.
Footnote 31 warns about a normalization assertion in the cited earlier
Yuan--Zhang--Zhang formulation; no constant is imported from it here.

[Watson, sections 2.2.1--2.3](https://arxiv.org/pdf/0810.0425), unfolds
the forward lift by norm fibres and identifies its adjoint using
multiplicity one. That work is over Q. Its proof structure motivates
the local calculation above; its global theorem is not being quoted
as a theorem for our F.

The new calculation supplies the nonzero local norm-one functional
needed for a forward-lift argument. To conclude that the **implemented
D91 expression** is a nonzero rank-one eigenform tensor, still write
the comparison between its fixed-character/isometry kernel and the
similitude formulation. In particular:

1. Specify the extension in u and its restriction to the chosen
   classical component, including the central-unit quotient.
2. Match the dual/conjugation convention, finite newvector and the
   character psi_delta on both sides. Use the local calculation above
   in the forward norm-one coefficient, then apply adjointness.
3. Check that the finite fixed lines and the one split real lowest
   type select the required tensor. Track the scalar separately if
   absolute Petersson normalization is needed.

A useful starting point for step 1 is a real extension
`Phi_v(x,u)=h_v(u)*phi_v(sqrt(u)*x)` for u>0 and finite support on
u in O_v^times. The SL2 actions intertwine after this real scaling;
positive-unit squares from D92 allow reindexing the rational theta
sum. The determinant integration and its measure have **not** been
completed, so this observation is a construction to check, not an
identification theorem.

Even after that comparison, nonzero as an automorphic form does not
imply a nonzero first derivative at this CM point. The latter remains
a separate requirement for derivative ratios and arithmetic jets.

## 5. Reproducibility and next work

New artifacts:

- `nelson_contour_weight_bounds_d94.json`: 28 rigorous majorant probes;
  no changed-weight partial sums.
- `nelson_norm_one_test_vector_d94.json`: exact arithmetic supporting
  the local nonvanishing proof, with the global boundary flags false.
- `nelson_kernel_review_d94.json`: final arithmetic/provenance audit.

Recheck with:

```sh
python3 dembele/pari/357_nelson_kernel_review_audit.py --check
```

The two computational jobs passed in 7.21 and 3.30 seconds rounded up.
The final audit checks source hashes, exact polynomial weights and
tail integrals, dyadic interval endpoints and rounded global bounds,
and the local field/order identities. It binds the corrected D93 root;
it does not repeat the exhaustive D93 enumeration or the Arb nodes.
The analytic local proof and the global comparison boundary are in
this report. Sources 355--357 and their bound artifacts are frozen
after the audit. No candidate model, remote computation, Hecke bank
or cubic precision was changed.

**Next:** finish the explicit kernel comparison above. For the accuracy
problem, test a method that keeps more cancellation before taking
absolute values, such as evaluating the completed scalar kernel on
norm/displacement blocks and then bounding those blocks. First require
a small bounded pilot with a useful rigorous error estimate. The
present contour/weight family does not justify another large enumeration.
Independent arithmetic CM jets, marked curve identification, cubic
recognition and the target field polynomial remain open.
