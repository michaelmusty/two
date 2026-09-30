# D95: identify the classical kernel with the Shimizu tensor

Date: 2026-09-23. Continuation of
[D94](nelson-test-vector-and-contour-d94.md), authorized by “continue”.

**Result:** the D90 classical theta integral is a **nonzero rank-one
Jacquet–Langlands tensor**, with positive scalar. The comparison below
handles the similitude variable, central averaging, the classical
component, local level and nonvanishing. Together with the D91 unfolding
and D93 convergence proof, it identifies the full implemented Mellin
series with the indicated derivative pairing.

There is an essential convention to record: the implemented pair
`(a,1)` differentiates the **conjugated first factor** a times. In the
fixed disk coordinate, recovering differential coefficient ratios
therefore requires complex conjugation and a factorial, as in section 6.
No previous numerical ratio was certified or used to construct a tangent.

This is an identification theorem, not a new numerical evaluation.
The D94 omitted-ideal bound remains <2.680e13 for `(1,1)`. The first
derivative of the chosen eigenform at the CM point is still not proved
nonzero. No arithmetic CM jet or target field polynomial is obtained.

## 1. Fix the classical conventions

Retain F, its different generator delta=16/(2+b), the order O and
the character psi_delta from D90. Write D=2^31 for the field
discriminant. Let sigma be one of the parallel-weight-two,
level-p2-new representations with U_p2=+1 in the saved module, and
pi its Jacquet–Langlands transfer to B. The different level-one
16-dimensional target module is not used.

Let f be the classical Hilbert eigenform with coefficient a_f((1))=1
and frequencies n/delta. Write F(g_z)=Norm(y)*f(z) for its unitary
realization. Let v be a nonzero quaternionic eigenform in pi, fixed by
O_v^times at finite places, trivial on the seven compact real norm-one
groups, and of right K type +2 at the split real place. On the latter,
v(g_z)=y*f_B(z). Petersson norms below use these unitary realizations.

Put G=PSL_2(R), Gamma_B=O^1/{+1,-1}, and give K mass 1 and G/K the
hyperbolic area measure. For the Hilbert quotient use product
hyperbolic area. A simultaneous change of adelic measure conventions
does not change the nonvanishing or derivative ratios proved here.

The fixed-character adelic theta kernel on SL_2 and norm-one
quaternionic arguments is

    Theta_phi(g;h1,h2) = (1/2) sum_(x in B(F))
        omega_psi_delta(g)[phi(h1^(-1)*x*h2)].

At finite places phi=1_O. At the split real place it is
`X^2/delta_0*exp(-2*pi*P/delta_0)`; at the other seven it is
`exp(-2*pi*Nrd/delta_v)`. At finite identity the rational x are exactly
the actual saved order O. The factor 1/2 identifies x and -x.

The classical integral is

    L_f(h1,h2) = integral_(Hilbert quotient) conjugate(F(g))*Theta_phi(g;h1,h2) dg.

Its split K types are (-2,+2). Accordingly the tensor orientation is
`conjugate(v(h1))*v(h2)`. The bars in
[Nelson's equation (13)](https://arxiv.org/pdf/1210.1243), printed page 18,
were checked in the rendered PDF: extracted text alone loses them.

## 2. Remove the similitude variable by central averaging

We use the general-number-field Shimizu correspondence in
[Disegni, sections 3.1 and 5.1](https://arxiv.org/pdf/1510.02114).
Its Schwartz space has variables (x,u), and its central GL_2 action,
for the four-dimensional quaternion norm space, is

    r(c*I)Phi(x,u) = Phi(c*x,c^(-2)*u).

This is distinct from merely setting u=1 inside the global integral.

Choose smooth nonnegative functions h_v on R_(>0), of compact support,
with `integral h_v(u) du/u=1`. Define

    Phi_v(x,u) = 1_(O_v)(x)*1_(O_F,v^times)(u),            v finite,
    Phi_v(x,u) = h_v(u)*phi_v(sqrt(u)*x),                  v real, u>0,
    Phi_v(x,u) = 0,                                      v real, u<0.

These are Schwartz functions. For positive real u, scaling x by
sqrt(u) intertwines the SL_2 Weil actions for q and u*q. This follows
on the unipotent, diagonal and Fourier generators; the Fourier
measure scales by u^2 in dimension four and cancels the Jacobian.
The analogous identity for u=t^2 holds at every place with x scaled
by t. The norm-space quadratic character is trivial.

The arithmetic hypotheses needed here are now checked together by
script 358: h(F)=h^+(F)=1, with PARI `bnfcertify=1`, and eight
independent unit signatures. Thus a totally positive unit is a
square. More generally,

    u totally positive, ord_p(u) even at every finite p  =>  u in F^(times 2).

To prove this, write (u)=a^2, use h(F)=1 to choose a=(t), and apply
the positive-unit square statement to u/t^2. This also explains why
the class-number hypothesis cannot be omitted from the argument.

Let theta_Phi be the similitude theta series without a factor 1/2,
summed over u in F^times and x in B(F). For g at finite identity and
real determinant one, average theta_Phi(c*g;h1,h2) over
F^times\A^times in the central variable c. The support at finite
places forces ord_p(u)=2*ord_p(c); real support forces u>0 everywhere.
Every surviving rational u is therefore t^2. Reindex x by t*x and
unfold the sum over t in F^times/{+1,-1}. The resulting integral is

    integral_({+1,-1}\A^times) sum_x r(g,h)Phi(c*x,c^(-2)) d^times c.

Now c is a unit at every finite place. Its finite action leaves O
unchanged. At a real place, phi_v is even, so

    Phi_v(c*x,c^(-2)) = h_v(c^(-2))*phi_v(x).

Normalize the finite unit groups to have volume 1, take dc/|c| on
both components of R^times, and give the finite group {+1,-1}
counting measure. At each real place

    integral_(R^times) h_v(c^(-2)) dc/|c|
        = integral_(R_(>0)) h_v(u) du/u = 1.

The quotient by the single global sign contributes 1/2. Hence the
central average is **exactly Theta_phi** in these conventions. There
is no extra unit regulator: the entire rational square sum was
unfolded, rather than replaced by a sum over a chosen list of units.
Changing to another Haar convention multiplies both sides by a
specified positive measure constant.

This computation holds after the SL_2 and norm-one actions: the
central action commutes with them, and scaling by the rational t
intertwines the corresponding Weil actions before reindexing.
Compact support in the logarithms of u, Gaussian decay and the
compact quaternionic quotient justify the central unfolding and the
subsequent cuspidal pairings.

## 3. Check level, components and the one-dimensional tensor line

At every unramified finite place the order lattice is self-dual and
its norm is integral, so Phi_v is fixed by GL_2(O_F,v). At p2 the
Fourier transform is supported on O# and
`Nrd(O#) subset pi^(-1)*O_F`. Upper unipotents with integral parameter
fix Phi_v; after Fourier transformation, lower unipotents with
parameter in pi*O_F do too. Diagonal units preserve both supports.
These generators give K_0(p2) invariance. Multiplying the character
by a unit u leaves this support argument unchanged. Script 358
checks all diagonal and bilinear norm terms on the actual O and O#
bases, rather than inferring norm integrality from diagonal terms alone.

Independently, Phi is fixed by O_v^times in each quaternionic factor.
At the compact real places its type is trivial, and at the split
place its two types are (-2,+2). The corresponding local fixed lines
in pi and pi-dual have dimension one. At the division place an
unramified character chi composed with Nrd transfers to an unramified
twist of Steinberg. Its norm-pi^r shell contributes
`q^(-r)*chi(pi)^r` in unitary Whittaker normalization; the arithmetic
U_p2 coefficient is chi(pi). Thus U_p2=+1 selects the required
normalizer-invariant line, without replacing U_p2 by the opposite
Atkin–Lehner sign.

The class-number calculation also deals with classical components.
Strong approximation identifies the finite-level components through
the relevant norm class groups. They are trivial here since the
narrow class group is trivial. For the quaternion order this is
[Voight, Corollaries 28.5.12 and 28.5.17](https://link.springer.com/chapter/10.1007/978-3-030-56694-4_28).
For the Hilbert group it is the split matrix-algebra case, with
det(K_0(p2))=the finite units. A positive determinant unit is a square,
so dividing by its scalar square root identifies the classical
positive-determinant group modulo its center with the determinant-one
group. No unexamined sum over additional components is left.

The global Shimizu theorem puts the lift in pi-dual tensor pi (with
our ordering). The fixed lines above make its classical restriction
a scalar multiple of `conjugate(v(h1))*v(h2)`. The central comparison
proves that this assertion applies to L_f, the kernel used in D91.
It remains to prove its scalar is nonzero; uniqueness alone would
not prove this.

## 4. Prove nonvanishing by the forward norm-one coefficient

Consider the forward classical transform

    T_v(g) = integral_(Gamma_B\G)^2 Theta_phi(g;h1,h2)
                 *v(h1)*conjugate(v(h2)) dh1 dh2.

The forward Shimizu correspondence and the local fixed types put
T_v in the Hilbert newvector line of sigma, so T_v=c*f in classical
notation. This uses the general-field correspondence, not a claim
that Watson's theorem over Q is stated over F. The norm-fibre
unfolding below is our specialization of the forward/adjoint method
in [Watson, sections 2.2.1--2.3](https://arxiv.org/pdf/0810.0425).
The forward transform is cuspidal: B(F) has no nonzero isotropic
element, and the nontrivial split quaternionic K type kills the zero
term at every cusp.

Extract the Fourier frequency 1/delta at real heights y_v=1. The
rational quaternions are now precisely O^1. The sign factor turns
this into a sum over Gamma_B. The seven definite Gaussian factors
are constant on that norm fibre. Unfolding one of the two compact
quotient integrals gives

    [frequency 1/delta of T_v at y=1]
       = norm(v)^2 * product_(v real) I_v
       = norm(v)^2 * exp(-2*pi).

Here I_v are exactly D94's local contractions: the split matrix
coefficient is X(g)^(-2), so it cancels X(g)^2; the radial integral
with density 2*pi*sinh(r) gives exp(-2*pi/delta_0). The compact
places give exp(-2*pi/delta_v), and Tr(delta^(-1))=1. At general
heights the unitary coefficient is
`norm(v)^2*Norm(y)*exp(-2*pi*sum_v y_v/delta_v)`, consistent with
the same classical Fourier normalization.

Since a_f((1))=1, this proves c=norm(v)^2 in the stated classical
measures. Adjointness now gives

    L_f(h1,h2) = [norm(f)^2/norm(v)^2]
                    *conjugate(v(h1))*v(h2).

Indeed pairing both sides with v(h1)*conjugate(v(h2)) gives
`c*norm(f)^2` on the left and `lambda*norm(v)^4` on the right.
The scalar lambda is **strictly positive**. Choosing v with
norm(v)=norm(f) makes it 1. Computing either norm is unnecessary
for derivative ratios; no numerical norm is claimed here.

## 5. Match the Mellin normalization already implemented

The D91 prefactor can also be checked directly from the now identified
kernel. In unitary notation the split height contributes
`y_0^2*X^2/delta_0`, the seven compact heights contribute y_v, and
F contributes Norm(y). After the invariant measure and Eisenstein
factor, the split integral of a derivative term with height degree r
is Gamma(s+2+r); the others are Gamma(s+1).

The r powers of 4*pi/delta_0 from differentiation cancel the extra
r powers from the split Gamma integration. Each delta_v is left
with exponent s+1. The total power of 4*pi is -(8*s+9).
Translation covolume sqrt(D) and the completion Lambda_F(2*s) give
the remaining D and pi powers. Dividing by the residue 64*R_F gives

    P_F = D^(3/2)/(64*R_F*(4*pi)^9) > 0,
    Z   = (4*pi^2)^8*A/D^2.

These are D91's prefactor and argument. Its exact cusp identity,
U_p2 coefficient and beta strings remain unchanged. D93 proves the
absolute convergence required for the full primitive-ideal sum at
c>3/2. Therefore, with D1,D2 the Lie derivatives used by the code,

    P_F*S_(a,1) = D1^a D2 L_f
                = lambda*conjugate(J_a)*J_1,   a=1,3,5,

where J_j is the j-th pure holomorphic disk derivative of the unitary
quaternionic form at the CM point. This identifies the **complete**
series; it does not turn its finite partial sums into completed values.
In particular the full S_(1,1) is nonnegative, but may be zero for
the selected eigenform at this particular point.

## 6. Resolve the derivative orientation and coefficient ratios

For a real matrix g, the correct complex matrix is

    M(g) = [[X,conjugate(Y)],[Y,conjugate(X)]].

Script 358 verifies it by a Cayley change of basis. The centered disk
section has complex matrix
`[[1,w],[conjugate(w),1]]/sqrt(1-|w|^2)`. For pure derivatives in
the first anti-holomorphic variable u and second holomorphic variable v,

    M' = (I-u*E21)*M*(I+v*E12).

It preserves the norm. If h=4*pi*y_0/delta_0 and
P=X*Xbar+Y*Ybar, its change in the Gaussian exponent is

    -h*(P'-P)/2 = h*(u*X*Ybar-v*X*Y+u*v*X^2).

Consequently the `(a,1)` derivative of the polynomial Gaussian is

    X^(a+3) * [a*h^a*Ybar^(a-1)-h^(a+1)*Y*Ybar^a],

exactly the polynomial implemented in D90--D93. This independent
matrix-path derivation fixes which factor was differentiated; it
requires no change to the stored numerical sums.

Write the upstairs differential in the fixed disk coordinate as

    omega = sum_j c_j*w^j dw.

The unitary disk derivatives satisfy J_j=j!*c_j/(2*i). At the
order-two quotient, only odd j occur, and t=w^2 gives coarse
coefficients c_(2m+1)/2. Provided S_(1,1) is nonzero,

    c_a/c_1 = conjugate(S_(a,1)/S_(1,1))/a!,   a=1,3,5.

Thus the degree-three and degree-five ratios require factors 1/6 and
1/120, respectively, after conjugation. These are analytic coordinate
ratios, not automatically arithmetic CM jets. Their recognition and
the arithmetic coordinate scale remain separate steps. D91's recorded
arXiv-v1 derivative-display discrepancy remains; this proof uses the
checked Gaussian derivations.

At least one of the sixteen eigenforms has a nonzero first derivative
at this quotient point: the canonical system on the smooth genus-16
curve has no base point, and the coarse constant coefficient is half
the upstairs first coefficient. This existence statement does not
select an eigenform or certify any of the currently computed partial
sums as its nonzero value.

## 7. Evidence, boundaries and next computation

Script 358 passed in less than 5.49 seconds. It re-proves the ordinary
and narrow class numbers with certification, checks unit signatures,
checks 1,056 diagonal/cross norm-integrality conditions, and verifies
the Cayley matrix, Gaussian paths and Mellin powers symbolically.
The class-number proof is supplied by the certified PARI run; the
standard-Python audit independently replays the exact unit, order
and Gaussian coefficient arithmetic and binds the analytic proof here.
The mathematical correspondence theorem is a cited input, not a
theorem proved by the audit program.

```sh
python3 dembele/pari/359_nelson_global_identification_audit.py --check
```

Use `nelson_global_identification_d95.json` as the new root. The
D94 root and all earlier numerical artifacts remain frozen, including
their historically correct pending-identification flags. The D95
result supersedes that pending global comparison; it does not
supersede their numerical error estimates.

**Next:** address accuracy with a bounded pilot that evaluates the
completed scalar kernel before applying an absolute bound on
norm/displacement blocks. Require a demonstrable improvement over
the present global estimate before adding more Hecke data or larger
enumerations. Identify a nonzero CM anchor numerically with a valid
full error bound before forming the ratios above. No remote run,
candidate-model change or cubic precision increase occurred. Exact
arithmetic jets, marked identification, cubic recognition and the
target field polynomial remain open.
