# D98: a spectral bound for every omitted norm ideal

Date: 2026-09-24. Continuation of [D97](nelson-signed-orbit-d97.md).

**Result:** an unconditional spectral comparison reduces the omitted-ideal
S11 bound from D96's 6.753599953802e12 to **<24,784,932,714**, a factor
**>272.48**. It keeps cancellation within a complete Hecke family and
does not assume D97's unproved signed-counting law. The original kernel
and partial sum are unchanged. After the existing two-family tail, the
full error is **<24,784,942,340**. This still exceeds the partial sum
7640.7582 by about 3.244 million, so the CM anchor remains uncertified.

No new quaternion classes or Hecke coefficients are computed. The
finite run takes <5.38 seconds under the 180-second process-group limit.
The numerical result is a bound, not the size or sign of the omitted sum.

## 1. The complete ideal family is a Hecke kernel

Keep the norm-one quotient Gamma=O^1/{+1,-1}, the CM frame and split
embedding fixed in D91--D95. Normalize Haar measure so that K has mass
one and G/K has hyperbolic area measure. For a quaternion alpha of
totally positive norm n, put N=Norm(n) and

    D=A/N=|X|^2/sigma_0(n)=cosh^2(r/2),
    Phi(alpha)=(X/|X|)^4.

The normalized matrix g=alpha/sqrt(sigma_0(n)) belongs to PSL_2(R).
The kernel Phi(g)*F(D(g)) has left and right K character +4; convolution
acts on right K type -4. Conjugating every convention gives the same
real diagonal bounds. In polar coordinates the radial measure is
2*pi*sinh(r)*dr=4*pi*dD.

D95 certifies narrow class number one and that every totally positive
unit is a square. Strong approximation and the ideal-class description
used there imply that every locally principal right O-ideal is principal.
More explicitly, for norm ideal a=(n) with n totally positive, the
reduced-norm theorem supplies a global element of norm n. Local order
units have surjective norms, so local generators of any given ideal of
norm a can also be chosen with norm exactly n. Strong approximation for
B^1 at the split real place then adjusts the global element to generate
that ideal without changing its norm. The remaining choices are right
O^1, and the only scalar choices of norm one are the two signs. The
positive-unit square property identifies the resulting action with the
single classical component used in D95.

Consequently all integral alpha of norm n, modulo sign, form the full
Hecke correspondence, with all central contents included. At an odd
prime power p^e it has 1+q+...+q^e right cosets. Its unnormalized Hecke
operator T_a has eigenvalues b_pi(a)=sqrt(N)*lambda_pi(a), where the
local standard-L coefficients are

    lambda_pi(p^e)=sum_(j=0)^e alpha_p^j*beta_p^(e-j).

There is no division by the correspondence degree. Reduced conjugation
identifies the inverse normalized correspondence with this one, so
left/right and inverse conventions give the same diagonal sum. The
single classical component and the positive-unit squares are essential
here; passing to the normalizer quotient would change the problem.

## 2. Explicit weight-four transform

Write lambda=mu*(1-mu). The unitary representations having this K type
are the principal series mu=1/2+ir, the complementary series
1/2<mu<1, and the discrete series with lowest weights 2 and 4,
represented by mu=1 and mu=2. The trivial representation has no such
K type. The normalized radial matrix coefficient is

    phi_mu(D)=D^(-mu)*2F1(mu+2,mu-2;1;1-1/D).

This agrees with [Bourgain--Kontorovich--Sarnak, equation (2.14)](https://www.math.ias.edu/files/avi/Bourgain_Kontrovich_Sarnak.pdf)
at n=k=2 and their disk radius squared 1-1/D.
One can verify the formula directly: it is the solution regular at
D=1, with value one, of the radial Casimir equation

    D*(D-1)*phi''+(2*D-1)*phi'+(lambda+4/D)*phi=0.

Substituting u=1-1/D gives the hypergeometric equation. In particular,
mu=1 gives -2/D+3/D^2 and mu=2 gives D^(-2); audit 369 checks both
normalizations in the radial equation.

For Re(p)>2 the transform of Phi(g)*D(g)^(-p) is

    h_p(mu)=4*pi*Gamma(p-mu)*Gamma(p+mu-1)
                   /[Gamma(p+2)*Gamma(p-2)].

Indeed substitute u in its radial integral, integrate the hypergeometric
series against (1-u)^(p+mu-2), and apply
[Gauss's evaluation, DLMF 15.4.20](https://dlmf.nist.gov/15.4.E20).
The resulting integral is Gamma(p+mu-1)*Gamma(p-mu) divided by the
displayed denominator. Absolute convergence holds in the stated domain.
The two discrete-series transforms divided by 4*pi are respectively
(p-2)/(p*(p+1)) and 1/(p+1), also obtainable by elementary integration.
For real p>2 every h_p on this unitary spectrum is strictly positive.

For the original S11 radial function, define

    f_N(A)=[K3(Z0*A)-(1-N/A)*K4(Z0*A)]/A,
    Z0=(4*pi^2)^8/2^62,
    C(s)=zeta_F(2*s)*(1+2^s)/(1-2^(-s-1)).

The Mellin integrand for f_N(ND), after extracting
N^(-1)*(Z0*N)^(-s)*(2*s-1)*Gamma(s)^16*s^7, is

    C(s)*(s)_3*[-(s+2)*D^(-s-1)+(s+3)*D^(-s-2)].

Apply the transform before taking absolute values. Gamma recurrence gives

    (s)_3*[-(s+2)*h_(s+1)+(s+3)*h_(s+2)]
      =4*pi*(lambda+2)*Gamma(s+1-mu)*Gamma(s+mu)/Gamma(s)^2.

The elementary identity behind this cancellation is
-(s+2)*(s-1)+(s+1-mu)*(s+mu)=lambda+2. Thus the transformed complete
radial kernel is

    H_N(mu)=(4*pi/N)*integral_(c)
      (2*s-1)*Gamma(s)^14*s^7*C(s)*(lambda+2)
      *Gamma(s+1-mu)*Gamma(s+mu)*(Z0*N)^(-s) ds/(2*pi*i).

The lowest-weight-four discrete series vanishes identically. The
lowest-weight-two series, which contains the derivative of the target
form, survives. This is a normalization control, not a vanishing claim
about the desired derivative.

## 3. Uniform control of the entire remaining spectrum

For c>=1, s=c+it, use the positive comparison transform h_(c+2).
The key estimate is

    |(lambda+2)*Gamma(s+1-mu)*Gamma(s+mu)|
       <= Gamma(c+2-mu)*Gamma(c+1+mu).

The right side is positive real on this spectrum. For real mu in
[1/2,1], the integral for Gamma gives |Gamma(x+it)|<=Gamma(x).
Gamma recurrence then makes the ratio at most

    (lambda+2)/(c*(c+1)+lambda) <= 1.

For principal mu=1/2+ir set x=c+1/2. The function
L_x(v)=log|Gamma(x+iv)| is concave for x>=1/2. To prove this, the
[trigamma reflection and asymptotic formulas, DLMF 5.15.6 and 5.15.8](https://dlmf.nist.gov/5.15)
give Re(psi'(1/2+iv))=pi^2/(2*cosh(pi*v)^2)>0 and uniform decay
psi'(z)=O(1/|z|) in the closed right half-plane. The minimum principle
on larger and larger half-disks gives Re(psi'(x+iv))>=0 for x>=1/2.
Therefore L_x''=-Re(psi')<=0. Since L_x is even, midpoint concavity
yields

    |Gamma(x+i*(t-r))*Gamma(x+i*(t+r))| <= |Gamma(x+ir)|^2.

After Gamma recurrence, the required ratio is at most
(r^2+9/4)/(r^2+(c+1/2)^2)<=1. The mu=1 case is covered by the real
argument; the mu=2 multiplier is zero. No spectral-gap constant,
exceptional eigenfunction value or translated injectivity estimate is
needed.

It follows, for c>1, that

    |H_N(mu)| <= B(c)*Z0^(-c)*N^(-c-1)*h_(c+2)(mu),

    B(c)=Gamma(c+4)*Gamma(c)*zeta_F(2*c)
         *(1+2^c)/(1-2^(-c-1))/pi
         *integral_0^infinity |(2*s-1)*Gamma(s)^14*s^7| dt.

The 4*pi factors cancel in this comparison. The 1/pi accounts for
both halves of the Mellin contour.

## 4. Positive pretrace comparison and the ideal sum

Let {v_j} be an orthonormal simultaneous Casimir/Hecke basis in the
chosen K type, evaluated at the fixed CM frame. The positive comparison
kernel gives

    C_p=sum_gamma Phi(gamma)*D(gamma)^(-p)
       =sum_j h_p(mu_j)*|v_j(z0)|^2 >= 0.

For p>=3, D92's identity-only range D<=64 and count C(D)<=32*D/7 imply

    C_p <= sum_gamma D(gamma)^(-3)
        <= 1+(32/7)*integral_64^infinity 3*D^(-3) dD
         =1795/1792.

This slightly overcounts the nonidentity tail. Absolute convergence of
the geometric sum and the positive transform justify the pretrace
identity and its diagonal limit. The multiplier comparison dominates
the spectral series by this finite positive sum. In particular it also
justifies evaluating the composed Hecke kernel at z0.

All noncharacter automorphic representations here transfer by
Jacquet--Langlands to cuspidal GL2 representations. Automorphic
characters have K type zero and contribute nothing. At odd finite
places, [Blomer--Brumley, *On the Ramanujan conjecture over number
fields*, Definition 1 and Theorem 1](https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p18-p.pdf)
give the Satake exponent delta=7/64 over this number field. Hence

    |b_pi(a)| <= d(a)*N^(1/2+delta).

The target holomorphic eigenform retains the stronger D93 bound
|a_f(a)|<=d(a)*sqrt(N). Apply the spectral comparison to the **whole**
norm-a diagonal kernel R_a, before replacing Hecke eigenvalues by bounds:

    |a_f(a)*R_a|
      <= (1795/1792)*B(c)*Z0^(-c)*d(a)^2*N^(-(c-delta)).

This removes the earlier factor sigma_1(a) from the absolute orbit
count. The squared-divisor mass, for w=c-delta>1, is

    E_odd(w)=sum_(a odd) d(a)^2*Norm(a)^(-w)
            =zeta_F(w)^4/zeta_F(2*w)*(1-2^(-w))^3/(1+2^(-w)).

Its local series is sum_(e>=0)(e+1)^2*x^e=(1+x)/(1-x)^3.
There is one dyadic prime of norm two. Remove the unit ideal and only
the saved prime (31,b-27), giving the proved bound

    E(c)=(1795/1792)*B(c)*Z0^(-c)*[E_odd(c-delta)-1-4*31^(-(c-delta))].

The other seven primes above 31 remain in the remainder. The convergence
threshold is now c>71/64 instead of the earlier c>3/2. No infinite
signed-count estimate or empirical phase constant enters this result.

## 5. Bounded computation and independent replay

Script 368 evaluates ten rational contours from 73/64 through 2.
At each contour, 2,048 Arb interval rectangles cover 0<=t<=16 with
width 1/128. Their exact upper dyadic endpoints are saved. On the
remaining half-line, the Binet estimate used in D94 gives, for 1<c<=2,

    |Gamma(c+it)|^14
       <=8^7*exp(7/(6*c))*(2+t)^21*exp(-21*t).

Thus the remaining integrand is bounded by the same prefactor times
(2+t)^28*(3+2*t)*exp(-21*t). Its integral from 16 to infinity is an
exact rational factorial sum times exp(-336). Every vertical-tail
bound is <1e-103. Zeta_F is evaluated by the existing eight even
Dirichlet characters of conductor dividing 32.

The best tested contour is c=5/4; no claim of global optimization is
made. It gives B(c)<102.082 and omitted squared-divisor mass <10.430061.

| Contour c | Omitted-ideal bound, rounded up |
|---|---:|
| 73/64 | 499,803,092,779 |
| 75/64 | 76,479,933,770 |
| 5/4 | 24,784,932,714 |
| 21/16 | 27,776,754,075 |
| 11/8 | 43,668,517,814 |
| 3/2 | 219,488,756,572 |
| 2 | 4,679,743,738,092,225 |

The unchanged D93 partial is 7640.7581837028, with two-family error
<9626.300. Audit 369 assembles the full interval from rational endpoints;
it still contains zero. D95's nonnegative rank-one pairing remains
identified up to a positive scalar, but nonnegativity alone supplies
no positive lower bound at this CM point.

Run the independent replay with:

```sh
python3 dembele/pari/369_nelson_spectral_ideal_audit.py --check
```

It verifies all 162 prior source hashes and the new provenance, all
20,480 rectangle endpoints and their sums, the transform cancellation,
two discrete-series radial equations, 64 local Euler coefficients,
the packing constant, the degree-29 tail polynomial and its exact
integral, algebraic powers and final directed error bounds. Gamma/zeta
evaluations on the rectangles and the analytic spectral arguments are
bound to the successful run and this proof; they are not re-proved by
the rational checker. Sources 368--369, this report and bound artifacts
are immutable once the root certificate has been generated.

## 6. Next step

This closes the specific D97 request for an explicit estimate retaining
Hecke-family cancellation, including all exceptional spectrum. It does
not make a larger enumeration useful yet. The new loss is visible in
the absolute Mellin integral and the independent absolute Hecke bounds.
Next test a completed spectral multiplier H_N(mu), retaining its Mellin
cancellation before majorizing the spectrum and the full norm sum.
Such a pilot must control all spectral parameters and the infinite
norm remainder; point samples or a finite set of eigenvalues do not
suffice. Do not repeat this contour scan at higher precision or infer
that a 272-fold gain makes the remaining 3.244-million factor small.

Keep the original partial sums, D95's conjugated factorial ratio rule,
exact interval endpoints, the process-group timeout and cubic precision
pause. Arithmetic CM jets, marked identification, cubic recognition
and the target field polynomial remain open.
