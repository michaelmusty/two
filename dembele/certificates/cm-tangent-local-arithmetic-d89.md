# D89: arithmetic local input for the CM tangent

Date: 2026-09-23. Continuation of the user's request to work on D88's
next step: compute the projective tangent independently of the candidate
curve equations.

**Result:** the local quotient and the relevant Hecke branches are now
explicit and checked with exact arithmetic. They expose two requirements
for a proposed evaluator: it must handle the order-two quotient, and it
must evaluate sections beyond the seventeen maximal-order CM points.
The known CM values and a Hecke matrix do not form a closed tangent
computation. **No independent arithmetic CM tangent has been obtained.**

The new calculation reads no candidate equations, candidate jets, or
numerical differential banks. It uses the CM field from D57 and the
Hecke place from the existing arithmetic bank. This is an input audit
and a local calculation, not a construction of the global section map.

## 1. Fix the local arithmetic before choosing a parameter

Write

    F=Q(b), b^8-8b^6+20b^4-16b^2+2=0,
    K=F(beta), beta^2=-2-b.

D57/D59 identify this K from the actual order-two elliptic elements;
it is not inferred from our reconstructed curve. At the saved Hecke
prime

    l=(1+2b-4b^3+b^5), b=27 mod31,

the CM polynomial becomes beta^2=2, with roots **8 and 23**. Both are
checked against the saved absolute degree-16 polynomial of K. The new
script also rechecks splitting at all eight places of F above 31.
Choosing 8 instead of 23 here only labels the two local eigenspaces;
it does not claim a new global CM-orientation certificate. In particular,
D59's beta=19 prime has b=9, not b=27, and must not silently be substituted
for the saved Hecke place.

The split integral CM algebra at l is R x R, where R=Z31. After choosing
its eigenlines, the projective elliptic element acts as diag(8,23),
hence as diag(1,-1). The fact that its square is scalar agrees with
the order-two stabilizer already known from the quaternionic group.

Splitting makes an ordinary CM deformation route plausible, but does
not itself construct a moduli test object, its polarization and level,
or a restriction map for the sixteen sections. The distinction in
[Mori, Proposition 3.3 and Theorem 3.6](https://arxiv.org/pdf/math/0406388)
is relevant: a deformation coordinate and a formula relating coefficients
to derivatives presuppose the modular form being evaluated. Moreover,
that paper's quaternionic moduli setup is over Q, so an application to
this real-octic datum needs its own construction.

## 2. The coarse tangent requires higher-order data upstairs

Let z be an odd local coordinate for the order-two stabilizer, so that
the stabilizer sends z to -z. The coarse coordinate is u=z^2. At this
tame prime the formal invariant ring is R[[z^2]]. For the formal
neighborhood of the degree-17 point, extend R to the unramified
degree-17 coefficient ring; all the displayed identities commute with
that extension. This elementary
quotient is intrinsic to the order-two point; no hyperellipticity
assumption is involved.

In the standard split ordinary Serre–Tate chart, the CM ratio -1 acts
by q -> q^(-1). If x=q-1, then

    x -> -x/(1+x),
    z=x/(2+x),
    u=z^2=x^2/(2+x)^2.

The script verifies the involution and these identities with rational
coefficients through degree nine. In particular u is zero on the
dual-number deformation x^2=0. Thus a first-order deformation of the
upstairs moduli object does not yet probe a nonzero tangent on C.
This calculation describes what a compatible Serre–Tate construction
must do; it does not certify that an arithmetic test object for our
curve has been built.

A coarse differential pulls back as

    (A_j+B_j*u+C_j*u^2+...) du
       = 2*(A_j*z+B_j*z^3+C_j*z^5+...) dz.

Consequently the projective tangent needs the coefficients in degrees
one and three upstairs. D88's three-coefficient comparison needs degrees
one, three and five. It would be incorrect to feed three consecutive
upstairs coefficients into the coarse jet test.

Here is the exact normalization interface. Suppose the independently
evaluated differentials have expansions

    omega_j=(a_j*z+b_j*z^3+c_j*z^5+...) dz,

and choose a denominator coordinate indexed by 0 with a_0 nonzero.
For r_j=omega_j/omega_0, write r_j=A_j+B_j*u+C_j*u^2. Then

    A_j = a_j/a_0,
    B_j = (b_j*a_0-a_j*b_0)/a_0^2,
    C_j = c_j/a_0-b_j*b_0/a_0^2
          + a_j*b_0^2/a_0^3-a_j*c_0/a_0^2.

Choose a parameter coordinate indexed by 1 with B_1 nonzero, and set
t=r_1-A_1. The desired coefficients are

    r_j = A_j + v_j*t + w_j*t^2,
    v_j = B_j/B_1,
    w_j = (C_j-v_j*C_1)/B_1^2.

The common differential scale and the local parameter choice disappear.
The unknowns are now explicit: independent section evaluations supplying
the vectors a,b (and then c), in a matched arithmetic canonical frame.
These formulas do not determine those vectors. The saved D68 frame
only fixes the projective a-vector, subject to its existing hypotheses.

An exact local control illustrates the distinction: du and
(1+2u+3u^2)du have the same value at u=0 as du and
(1+7u+3u^2)du, but the second coordinate has a different tangent.
Both pairs respect the same order-two quotient. These are local
sections, not counterexamples claiming to be global Shimura bases.

## 3. The Hecke correspondence leaves the known CM orbit

One possible repair was to recover derivatives from the known CM
values by applying the exact T_l action. The local lattice calculation
shows the missing terms in that proposal.

The degree-31 neighbors of a maximal local lattice are indexed by
P1(F31), with 32 elements. In a CM eigenbasis, let a neighbor correspond
to a line L in F31^2. Its CM multiplier order is determined by which
diagonal endomorphisms preserve L:

- For either coordinate axis, every diag(a,b) preserves L. These are
  the two horizontal neighbors, still at maximal CM conductor.
- For a line having two nonzero coordinates, diag(a,b) preserves L
  exactly when a=b modulo 31. Its integral multiplier order is
  `{(a,b) in R x R : a=b mod31}`, of conductor l. There are 30 such
  neighbors.

The script checks every diagonal endomorphism over F31 for every line.
The dimensions of the residue algebras are two and one respectively.
Thus the other branches cannot be treated as values at the saved
seventeen maximal-order CM points.

The elliptic involution fixes the two horizontal lines and pairs the
other thirty lines. On the coarse correspondence the fiber therefore
has two local branches of multiplicity one and fifteen of multiplicity
two. These are local branches with multiplicity; this is **not** a
claim that all their images on C are distinct, or a global count of
CM points of conductor l. The multiplicities total 32.

The familiar horizontal/descending description is discussed for
rational quaternion algebras in
[Saia, sections 3–4](https://arxiv.org/pdf/2212.12635).
Here the required statement is proved directly using R-lattices, so
it does not rely on transferring that paper's global rational-field
classification to F.

This failure of closure is not particular to 31. At an odd prime
unramified in K/F, the same local argument gives two horizontal
branches when split and none when inert. The remaining branches
have increased conductor. At the finite ramified prime above 2, the
Atkin–Lehner map has already been quotiented out in C. These observations
rule out a closed system using a single prime Hecke operator and only
the known maximal-order CM neighborhoods. They do not prove that every
possible use of Hecke operators is incapable of determining the tangent.

## 4. The omitted branches contribute derivatives, not just values

At one of the fifteen paired branches the source projection has local
form t=s^2. For a differential g(s)ds, its trace is

    Tr(g(s)ds) = (g_1+g_3*t+g_5*t^2+...) dt.

Indeed dividing by dt=2s ds and summing at s and -s gives
(g(s)-g(-s))/(2s). Even a value at the original CM point therefore
involves a first derivative at the descending point. A tangent involves
its third derivative.

This local trace is surjective: for any f(t), take g(s)=s*f(s^2).
Exact controls verify the first three coefficients over F31. In
particular g(s)=s^3 contributes t dt, so dropping the descending terms
can change the tangent while leaving the constant term unchanged.

Thus the available T_l matrix supplies a sum relation with unknown
neighbor jets. It cannot simply be substituted for the missing section
restriction map. Global relations might constrain those jets, but no
such evaluated global section data have been provided by this method.

## 5. Source review and the remaining construction

The expanded source search did not locate an implemented exact evaluator
for this datum. This is a finding about the sources inspected, not a
claim that no method exists.

- Mori supplies the deformation/derivative framework, subject to its
  moduli hypotheses. It does not turn our Hecke matrices into section
  evaluations.
- [Nelson, section 3.4 and Remark 5.1](https://arxiv.org/pdf/1210.1243)
  gives an independent analytic derivative-evaluation method, but its
  explicit computational formula is for rational quaternion algebras.
  It explicitly leaves the totally real application for further work.
  Using it here requires the appropriate archimedean kernels, local
  test functions, and a justified evaluation/truncation procedure.
- [Hida, sections 4–5](https://www.emis.de/ft/9824) gives CM-value and
  integral theta-correspondence results over totally real fields.
  Those statements concern specified theta lifts and their arithmetic
  normalization. They do not identify our canonical multiplication or
  its CM tangent from an abstract Hecke module. No new evaluation
  routine is imported from that source.

The next missing mathematical construction is a **global section
evaluator**, not merely a local deformation parameter. A possible
research continuation is a concrete totally real Shimizu derivative
formula with inputs tied to the saved Hecke module. That would first
provide an independent analytic calculation; exact arithmetic output
would still require an identity or an effective recognition bound.
It should not be advertised as a ready exact algorithm.

D88's tangent and three-coefficient certificates remain valid targets.
This continuation closes the specific idea that Serre–Tate coordinates
plus the existing seventeen-point Hecke data already make the target
computable. It does not justify another precision increase. The marked
base, P32/B3, and geometric double-cover identification remain open,
as does the published hyperellipticity conflict.

## 6. Artifacts and verification

New script:
[319_cm_tangent_local_arithmetic.py](../pari/319_cm_tangent_local_arithmetic.py).
New record:
[cm_tangent_local_arithmetic_d89.json](../data/computed/cm_tangent_local_arithmetic_d89.json).

```sh
python3 dembele/pari/319_cm_tangent_local_arithmetic.py --check
```

This replays the exact formal identities, place/splitting calculations,
all 32 neighbor multiplier tests, and the local trace controls. It also
checks its source/input hashes. The record explicitly sets
`Shimura_tangent_computed=false` and
`arithmetic_ST_test_object_constructed=false`.

No large numerical solve, remote job, coefficient lift, target torsion
calculation, or edit of the earlier bound sources/artifacts was made.
