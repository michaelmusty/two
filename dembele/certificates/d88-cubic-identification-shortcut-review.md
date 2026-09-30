# D88: review of the proposed cubic-identification shortcut

Date: 2026-09-23. Independent review requested by the user. This report
does not change any earlier arithmetic certificate or claim that the
marked Shimura identification has been proved.

**Verdict: the shortcut is sound as a conditional argument.** Once the
marked arithmetic double cover `X -> C` is identified, the Hecke order,
the nine saved thirds, and their point counts can identify the selected
cubic. A direct comparison of its full Fuchsian monodromy is then
unnecessary. The short version needs two repairs: prove that the
canonical cover belongs to the *particular oriented* third-division
family, and remove the possible Kummer scalar ambiguity. Both repairs
are available here. Unique lifting must take place on the same fixed
characteristic-zero `X` with the same branch divisors.

The conclusion is conditional on an **arithmetic identification of the
marked double-cover map**, not merely an identification of the underlying
complex curve or a numerical sign match. D87 has not yet supplied that
hypothesis.

## 1. A precise conditional proposition

Put `F = Q(b)`, where

\[
b^8-8b^6+20b^4-16b^2+2=0,
\qquad E=F(r),\quad r^2=-3.
\]

Use the prime

\[
\mathfrak l=(1+2b-4b^3+b^5),\qquad b\equiv27\pmod {31},
\]

and the place of `E` with `r ≡ 11 mod 31`. Its completion is `Q31`.
This is the prime used by the saved Hecke bank, as specified in
[script 58](../magma/58_levelraise_p2k.m). It is not the root 4 used in
some reconstruction calibration examples. D86 tested all eight roots,
including 27.

Assume the following inputs.

1. There is an `F`-isomorphism from the candidate double-cover map
   `X -> C`, with its involution, `P32`, `D17`, and `B3`, to the specified
   canonical arithmetic double cover. In particular its `B3` is the
   cubic branch locus of the canonical reflection cover. Use the
   candidate's fixed smooth proper model at 31, with the certified
   disjoint, reduced branch markings.
2. The canonical Hecke interpretation used in D51/D80 applies at
   `mathfrak l`. It gives the genus-40 and genus-16 Euler factors and
   the genus-64 counts 68 and 2818. In particular the Prym order is
   the integer in section 2 below.
3. Accept the independently checked finite-field class and cover
   certificates from D78/D79/D84: two independent rational
   anti-invariant 3-torsion points, the nine resulting thirds, and
   their normalized-cover point counts.

Then the special fibre of the canonical reflection cover is the
current `(0,0)` cover in D84. Its oriented class is the reduction of
the same unique characteristic-zero third that the saved computation
lifts. Consequently the associated characteristic-zero cubic over
the fixed base is the canonical reflection cover.

With D85's field-preserving normalization and its certified
one-dimensional section spaces, the exact normalized coefficient point
is defined over `F`. The saved coefficients modulo `31^128` are its
truncation. This conclusion does **not** recover its exact coefficients
or bound their heights, and does not assert descent to `Q`.

The following sections prove the implications and separate them from
the still-open first hypothesis.

## 2. The Prym bound really does exhaust the rational ambiguity

Let `k=F31`, `J=Jac(X_k)`, and

\[
P=\operatorname{im}(1-\tau:J\longrightarrow J).
\]

This is the connected Prym abelian variety of dimension `40-16=24`.
For 3-torsion there is no component-group ambiguity. If `3T=0` and
`tau(T)=-T`, then

\[
T=(1-\tau)(2T),
\]

so `T` belongs to `P[3]`. Conversely `tau` acts as `-1` on `P`.
The equality is defined over `k`, hence

\[
\{T\in J(k)[3]:\tau T=-T\}=P(k)[3].
\]

The isogeny `Jac(C) x P -> Jac(X)` gives the quotient of their Weil
polynomials, and therefore the quotient of their finite-field orders.
Evaluating the saved Hecke trace polynomials at `31+1=32` independently
reproduces

```text
#Jac(X)(F31) = 1232570236188721150202046839205630133464681300793863257653125
#Jac(C)(F31) = 1640801490553691915934375
#P(F31)      = 751200095370944434080214902187185651
             = 9 * 83466677263438270453357211354131739.
```

The last cofactor is prime to three. These remain *predicted* orders
for the candidate until hypothesis 1 makes the canonical Hecke factor
applicable to it. The arithmetic calculation itself uses
[the polynomial bank](../data/computed/levelraise_p2k_charpolys.m) and
[the saved genus-16 polynomial](../data/computed/cm_frame_curve_verification.json),
the same inputs as [script 172](../pari/172_cm_frame_cover_third.py).

D84's two independent points generate a subgroup of order nine.
Under the order bound it must be all of `P(k)[3]`. The nonempty set

\[
S(k)=\{A\in J(k):3A=-\Delta,\ \tau A=-A\},
\qquad \Delta=[D_+-D_-],
\]

is a torsor under this group: subtract two solutions, or add a torsion
point to one solution. Thus the nine saved classes exhaust `S(k)`.

The geometric torsor still has `3^48` members. This causes no problem:
the canonical cover at the chosen place gives a *rational* class in
`S(k)`. No enumeration of the other geometric members is needed.

## 3. Why the canonical cover belongs to this oriented family

First use the arithmetic cover, rather than only its reduction. Its
geometrically connected `S3` closure is defined over `F`; the order-three
deck group is a constant group over `F`. This follows directly from
an `F`-defined cubic with geometric group `S3`: its arithmetic splitting
group is a subgroup of `S3` containing the geometric `S3`, so there is
no larger constant-field extension in the splitting field.

There is also an explicit canonical-level construction. Start with the
maximal-order level giving `X`, and replace its local unit group at the
prime above 2 by `1+P_D`. Its quotient is `F4*`, of order three. The
reduced norms of `1+P_D` contain all local units: use the unramified
quadratic subfield to obtain a unit of prescribed norm, and divide by
its order-three Teichmuller residue lift, whose norm is one. With narrow
class number one, this level has one geometric component over `F`.
The division uniformizer normalizes it, acts on `F4*` by inversion,
and gives the reflection involution. Its square is a central idele;
narrow class number one and the inclusion of all central units make
that central action trivial. Thus the level cover and the reflection
quotient are defined over `F`, without a new `Q`-descent claim. The
canonical-model functoriality and component description used here are
[Dembélé, Theorem 4.1](https://arxiv.org/pdf/1906.06772); the particular
local quotient is [D43's exact construction](genus64-cover.md).

Over `E`, write the cyclic cover as `v^3=h`. By D77, the fibre above
`B3` is `D+ + D-`. Each divisor is a **single degree-nine closed point
over E**: the nonic residue field has degree 9 over `Q`, whereas
`[E:Q]=16`, and these coprime degrees give linear disjointness.
Consequently the valuation of `h` modulo three is constant on all
geometric points of each `D+` or `D-`.

Choose a generator `rho` with `rho(v)=zeta3*v`. A reflection must act as

\[
\widetilde\tau(v)=a/v,
\qquad a\in E(C)^*,\qquad h\tau(h)=a^3.
\]

Indeed conjugation inverts `rho`, and squaring the reflection forces
`tau(a)=a`. The two branch exponents are therefore opposite. Invert
the Kummer generator if necessary to choose them as `+1,-1`. Then

\[
\operatorname{div}(h)=D_+-D_-+3D_A,
\qquad A=[D_A]\in\operatorname{Jac}(X)(E),
\]

with `3A=-Delta` and `tau(A)=-A`. The latter equality follows from
the actual norm identity, not just from tripling the classes.
The basic correspondence between Kummer functions and line bundles
with a trivialized third power is
[Stacks, Kummer theory](https://stacks.math.columbia.edu/tag/03PK).

At the selected place of `E`, both the class and the oriented divisors
specialize over `F31`. Thus the canonical class enters exactly `S(k)`.
Reversing the global orientation replaces `(Delta,A)` by
`(-Delta,-A)` and gives the same unlabelled reflection cover.

**Why a purely special-fibre argument would be insufficient.** Modulo
31, `B3` has three cubic factors. Choosing the sign separately on
those factors is not justified. A small counterexample illustrates
the issue: over `F31`, let `X=P1_x`, `C=P1_t`, `t=x^2`, and for
`e_i in {1,-1}` put

\[
h_{\boldsymbol e}(x)=
\prod_{i=1}^{3}\left(\frac{x-i}{x+i}\right)^{e_i}.
\]

The covers `v^3=h_e`, with reflection `(x,v)->(-x,1/v)`, have the same
quadratic resolvent and branch supports. Exponent vectors differing
by more than simultaneous inversion give different covers, even
though `Jac(X)=0`. Thus a third census for one `Delta` does not cover
arbitrary branch orientations. Here the global irreducibility over
`E` is precisely what rules those alternatives out.

## 4. There are no additional scalar twists in this S3 family

Work over `k=F31`, which contains `mu3`. For a fixed oriented divisor
and a fixed class `A`, two Kummer functions have the form

\[
h'=d\,g^3h,\qquad d\in k^*,\quad g\in k(X)^*.
\]

Suppose both extend to `S3` covers with the given quadratic resolvent.
Their norm identities give

\[
d^2=\left(\frac{a'}{a\,g\tau(g)}\right)^3.
\]

The expression in parentheses belongs to `k(C)` and is algebraic over
`k`, so it belongs to `k` because `C` is geometrically integral.
Thus `d^2` is a cube in `k`. Squaring is invertible on `k*/k*3`, so
`d` is a cube as well. Explicitly, if `d^2=c^3`, then
`d=(c^2/d)^3`.

Hence `h` and `h'` give the same cyclic extension. The three reflection
subgroups are conjugate by the rational order-three deck group, so
their cubic quotients are isomorphic over `k(C)`. There is no extra
factor of three from `F31*/F31*3` to add to D84's census.

This is a statement about `S3` covers with the **fixed quadratic
resolvent**. Arbitrary cyclic cubic covers without that involution
compatibility do retain a scalar ambiguity. The same argument works
over `Q31` and over `E`.

## 5. Good reduction follows in this fixed family

The required good reduction need not be inferred from a general
statement about all Shimura covers. Let `R=Z31` and use the smooth
proper marked model of `X` in hypothesis 1. Its special fibre is
geometrically integral, and `D+` and `D-` extend to disjoint finite
étale divisors. The canonical generic cover has the norm identity
above over `Q31`.

At the generic point of the special fibre, `tau` preserves the
valuation. If `m=v31(h)`, the norm identity gives

\[
2m=3v_{31}(a).
\]

Thus `3` divides `m`; remove this vertical factor by a cube of 31.
On the regular surface `X_R`, the resulting function has divisor
`D+ - D- + 3D` for an integral Cartier divisor `D`, with no vertical
term. Locally removing a cube representing `3D` leaves a unit off
`D+ union D-`. The cover is therefore étale there. At either branch
divisor, using `v` or `1/v` gives a chart `s^3=u*t`, where `u` is a
unit and `t` is a relative local parameter. These are smooth tame
charts over `R`.

The normalization is consequently a smooth proper model of `Z`.
Its `S3` action extends by normalization. The reflection quotient
also has smooth fibres: invariants commute with reduction since 2 is
invertible, and the quotient of a smooth curve over a perfect field
by this finite group is a smooth curve. Thus the canonical reflection
cover has the required good reduction, with the same oriented branch
data. The norm condition is essential; it excludes a ramified
constant Kummer twist that could otherwise obstruct this argument.

## 6. Point counts select the reduction; étaleness identifies its lift

By sections 2–5, the canonical special fibre is one of the nine actual
normalized covers in
[D84](cm-frame-structural-checkpoint.md). Their counts are:

| Class | F31 | F31 squared |
|---|---:|---:|
| `(0,0)` | **68** | **2818** |
| `(1,0)` | 59 | 1495 |
| `(2,0)` | 50 | 1540 |
| `(0,1)` | 59 | 1543 |
| `(1,1)` | 44 | 1504 |
| `(2,1)` | 38 | 1474 |
| `(0,2)` | 59 | 1525 |
| `(1,2)` | 38 | 1456 |
| `(2,2)` | 53 | 1567 |

Only `(0,0)` has the canonical predicted counts. In fact the first
count already singles it out. The second count is independent
confirmation; no claim is made that two counts identify arbitrary
curves. They identify a member of this *proved exhaustive finite
family* containing the canonical cover.

Now fix the same characteristic-zero `X`, `Delta`, and embedding at
the specified prime. Its Jacobian extends to an abelian scheme over
`R`; multiplication by three is finite étale. The scheme of thirds
of `-Delta` is a finite étale `R`-scheme. Henselian lifting gives a
unique section above each rational special-fibre solution. See
[Stacks, multiplication by an invertible integer](https://stacks.math.columbia.edu/tag/0BFH)
and [finite étale algebras over a henselian local ring](https://stacks.math.columbia.edu/tag/04GK).

Equivalently, if the canonical third and the computed third have the
same reduction, their difference is a 3-torsion point reducing to
zero. Prime-to-31 torsion has injective specialization, so the
difference is zero. This also compares geometric algebraic thirds
after choosing the embedding in an algebraic closure of `Q31`.

This last implication is stronger than “the root can be lifted.” The
canonical algebraic third is already known to exist on the **same
fixed global curve** and is now known to reduce to the chosen root.
The `x^2-5` example in D85 correctly refutes an inference of global
field membership from a local root alone; it does not refute this
comparison with an independently specified global root.

Finally, the constant `S3` action over `F` gives

\[
\sigma(A)=\frac{\sigma(r)}{r}\,A\qquad(\sigma\in\operatorname{Gal}(\overline F/F)).
\]

To see this, use the eigenfunction for the rational deck generator
`rho`. Galois elements fixing `zeta3` preserve its eigenline; those
inverting `zeta3` take it to the inverse eigenline. Their Kummer
classes are respectively `[h]` and `-[h]`. This is exactly the global
condition left open in
[D85](cm-frame-cubic-128-review.md). D85's unique representative,
one-dimensional function spaces, and scaling
`lambda=r*a0/h0` then preserve the field of the cubic coefficients.
The scalar introduces no further root extraction.

## 7. What this review changes

| Required input or implication | Status after this review |
|---|---|
| Arithmetic identification of `C` and its `P32`, `D17`, `B3` markings | **Open.** Exact candidate objects and numerical matching exist. |
| Identification of the geometric double-cover choice `X -> C` | **Open.** D87 compares all 277 signs numerically; it is not a certified comparison. |
| Scalar quadratic twist once that geometric choice is fixed | D77's exact degree-nine fibre condition selects the compatible `F`-twist. |
| Hecke order and counts for the canonical objects at `b ≡ 27` | Existing canonical Hecke argument and exact bank; applicability to the candidate is conditional on the identification above. |
| Nine distinct rational thirds and their point counts | Existing exact certificates, unchanged. |
| Exhaustion, global branch orientation, and Kummer scalar uniqueness | Proved conditionally above; no new class enumeration is required. |
| Identification of the characteristic-zero third from its reduction | Valid on the same fixed smooth marked `X`; not a general local-to-global field test. |
| Exact normalized cubic coefficients over `F` | Still unconstructed; conditional `F`-definition gives no height bound. |

The cubic choice need not remain a separate full monodromy problem
after the marked arithmetic double cover has been identified. The
saved Hecke data and nine-cover comparison can finish that part.
The first hypothesis remains the substantive gap: D87 supplies
excellent numerical sign evidence but neither a certified marked
analytic identification nor the required arithmetic identification.
The published hyperellipticity conflict remains part of that gap.

It would be incorrect to promote the predicted Prym order to a
theorem about the current candidate merely because two low point
counts agree. One may instead prove the candidate Prym order
independently, but that alone still would not identify the canonical
double cover or its branch marking. The proposition above uses the
marked arithmetic identification to make the existing Hecke order
applicable.

No new large computation is needed to repair the shortcut. The
review adds the orientation argument, the scalar-uniqueness
argument, the local good-reduction argument, and the precise
fixed-curve lifting comparison. It independently rechecked the
Hecke prime label, the order quotient and its 3-adic valuation.
Earlier source files and artifacts were read only; no remote job,
precision escalation, exact number-field reconstruction, or target
torsion computation was performed.
