# A genuine first lift of the genus-64 cubic

Date: 2026-09-22. Decision D81. This continues the
[two Frobenius comparisons](cm-frame-cubic-frobenius.md).

**Result:** the marked cubic, its divisor class, and its function witnesses
are now computed and independently verified modulo 31^2=961. Its equation
is still

\[
 Q_4T^3-3A_4Q_4T-P_{10}=0,\qquad \operatorname{weight}(T)=2.
\]

The three coefficient arrays have lengths 105,105,285, and reduce
coefficient by coefficient to [D79's equation](cm-frame-cubic-cover.md).
They are stored in [the lift data](../data/computed/cm_frame_cubic_lift.json)
and [Magma input](../data/computed/cm_frame_cubic_lift.m).
The lifted norm scalar is **58**, reducing to 27 modulo 31:

\[
 u\tau(u)=58f^3q\tau(q),\qquad
 h=58u/q,\quad a=58f,\quad h\tau(h)=a^3.
\]

This is a finite-precision lift on the candidate base. A cubic over a
number field, arithmetic identification, and the final field polynomial
remain unconstructed. D80's two matching traces are retained unchanged.

## Actual points and complete section spaces

[184](../magma/184_cm_frame_cubic_lift_sections.m) first lifts the geometry.
It uses the rational genus-40 double cover w^2=n/d and the same divisor
D0=2*pi^*div(X16), of degree 120. The section dimensions remain
81,201,321,441 for L(D0),...,L(4D0).

The 45 even sections are canonical quadrics. The 36 odd sections have
the form w*q3/(ell*X16^2), where q3 vanishes at E_Q+U, of degree 18+21.
The supports are reduced and disjoint modulo 31. On E_Q, the rational
Veronese section D vanishes simply while A is a unit; F*A=D^2 and d=9F
give the required double zeros of d. On U, ell vanishes simply away
from B3. Each support component is lifted using a unit 15-by-15
Jacobian minor, and all curve and cut equations are checked afterward.

Evaluating the 75 cubic monomials at these lifted supports gives 39
independent conditions. Keeping the old 36 pivot columns equal to the
identity gives a unique lifted basis. Its full support matrix product
is zero modulo 961, and its reduction is the saved odd basis.

The 1,024 evaluation points and 111 auxiliary entries are lifted using
unit curve Jacobian minors and the equation w^2*d=n. The first 640
evaluation points retain the D78 order. Frobenius and the involution
are transported explicitly. The coefficient ring is

\[
 R'=(\mathbf Z/961)[b]/(b^2+29b+3),\qquad \sigma(b)=-29-b.
\]

The old field operation x->x^31 must not be used for Frobenius on this
ring. Branch evaluations come from the exact nonic coordinates and
the lift sqrt(-3)=879 of the old root 11. They use the regular value
W=w/(ell/X16), so no division by the vanishing ell occurs at B3.

[185](../pari/185_cm_frame_cubic_lift_section_data.py) collects these
[point, support and section data](../data/computed/cm_frame_cubic_lift_sections.json).
Reduction ranks certify complete free section spaces. Evaluation is
injective through L(8D0): the 1,024 distinct special-fibre points exceed
degree 960. A section vanishing on their lifts first vanishes modulo
31, and its remaining multiple of 31 vanishes by the same argument.

## Ring arithmetic and the third

[186](../magma/186_cm_frame_cubic_lift_arithmetic.m) represents each matrix
as M0+b*M1, using native matrices over Z/961. Three base-ring products
compute a product over R'. A unit inverse is lifted from the residue
field by J=J0*(2I-M*J0), and its identity is checked. Pilot
[188](../magma/188_cm_frame_cubic_lift_pilot.m) also compares multiplication
and inversion directly with native Galois-ring matrices.

This implements the section multiplication, quotient and complementary
divisor operations of
[Khuri-Makdisi's evaluation method](https://arxiv.org/pdf/math/0409209).
At intermediate quotient steps a maximal unit minor may omit constraints
divisible by 31. The known free Riemann–Roch target lies in this larger
space. Once both ranks agree, their reductions agree and Nakayama gives
equality; the accumulated constraints are then checked over the whole
ring. Every surviving degree-zero witness is checked against **all**
generators. These rank and inclusion checks are essential over a ring
with nilpotents.

The verified annihilator from D78 is

\[
 N=166933354526876540906714422708263478=3c+1.
\]

The square-zero reduction kernel is killed by 31. Thus, for the actual
lifted branch class Delta2, the scalar

\[
 c_2=31c+10=1724977996777724256036049034652055939
\]

gives A2=c2*Delta2 with 3A2=-Delta2. This deduction uses an annihilator
of one class, not a Jacobian or Prym order.
[189](../pari/189_cm_frame_cubic_lift_third.py) and
[190](../magma/190_cm_frame_cubic_lift_third.m) execute 161 add-flip
operations in five bounded jobs, keeping only the checkpoint classes
needed later. Direct checks verify 3A2=-Delta2, sigma(A2)=A2 and
tau(A2)=-A2. The
[saved third](../data/computed/cm_frame_cubic_lift_third.json) includes
its section coordinates and every checkpoint's provenance.

Multiplication by three has invertible differential at 31, as in
[Stacks, Lemma 39.9.9](https://stacks.math.columbia.edu/tag/0BFH).
The same relative Jacobian argument, together with
[étale lifting across nilpotent thickenings](https://stacks.math.columbia.edu/tag/06NE),
gives uniqueness of the class lift **with this chosen reduction**.
It does not select a unique third in characteristic 31.

## Preserving the saved coefficient reduction

[191](../magma/191_cm_frame_cubic_lift_function.m) lifts q in
L(D0-D-) with its old free coordinates, keeping q nonzero on D+.
Write div(q)=D-+Q-D0 and B=D++Q. For an effective representative E
of A2, the space L(4D0-E-sigma(E)-B) has rank 81. Its row-reduced
coefficient basis is fixed by sigma, hence lies over Z/961.

To preserve D79's effective representative E_R on reduction, intersect
the reduction of that moving space with L(4D0-E_R). This intersection
has dimension one. Lift its section inside the actual moving module.
The residual divisor then defines a lift of E_R with class
-2A2-Delta2=A2. Exact inclusion and disjointness checks verify this
construction. Its row-reduced section module reduces to the saved one.

The lifted functions satisfy

\[
 \operatorname{div}(u)=3E_R+B-4D_0,\qquad
 \operatorname{div}(f)=E_R+\tau(E_R)-2D_0,\qquad \tau(f)=f.
\]

Normalize the first unit coefficient of u and f to one. Their coefficient
vectors, q, and the norm scalar reduce to their D79 values. Recover A4,
Q4 and P10 in the same saved canonical monomial bases. The complete
evaluation equalities verify the cubic and its coefficientwise reduction.
The identity for h and a gives the same involution v->a/v on v^3=h,
and the reflection coordinate y=v+a/v. The tame cover construction
extends the saved genus-64 special fibre over Z/961; the raw cleared
equation still requires its cover interpretation at exceptional fibres.

This fixes the reduction of the representative, but it does not yet
specify an intrinsic representative gauge at every higher precision.
The moving space still has 80 projective parameters. Before recognition,
those choices must be fixed by persistent algebraic conditions, rather
than by changing scalar-chain representatives between precision levels.

## Independent verification and controls

[193](../magma/193_cm_frame_cubic_lift_check.m) reads the saved data with a
different seed. It verifies all lifted point equations, support cuts and
unit Jacobians; the odd-section constraints; branch evaluations;
the third relation and symmetries; the reduction of E_R; every generator
of the final function-divisor inclusions; the norm identity; and all
three invariant coefficient arrays. It does not replay the scalar search
or search for the functions.

Two controls add **31**, respectively to the norm scalar and one P10
coefficient. Both therefore pass unchanged modulo 31, but fail their
specified identity modulo 961. This tests the new digit explicitly.
The [combined certificate](../data/computed/cm_frame_cubic_lift_check.json)
binds the successful inputs and the expected failures recursively.

| Stage | First successful wall time |
|---|---:|
| Points, supports, sections | 8.368 s |
| Arithmetic pilot | 10.711 s |
| Five scalar chunks | 54.870 / 55.947 / 56.343 / 55.696 / 11.773 s |
| Function and cubic construction | 24.635 s |
| Independent verifier | 32.960 s |
| Highest-digit norm / trace controls | 29.437 / 33.071 s |

Every Magma job retains a 180-second, 2-GB limit. Four corrected
implementation failures are archived: degree-one Galois-ring creation,
the linear residue-field root convention, Galois-ring division syntax,
and a heterogeneous Magma data sequence. Immutable logs and source
snapshots are historical records, separate from current proof inputs.

[Magma's Galois-ring documentation](https://magma.maths.usyd.edu.au/magma/handbook/text/606)
specifies the finite quotient rings used for point arithmetic. The
matrix-pair implementation, unit-minor checks, checkpoint schedule,
representative choice and the computed coefficients are local work.

The final recursive audit verifies 435 distinct file hashes across
132 linked JSON records. D78's root certificate retains its original
hash. The 183 local Markdown links checked across the entry points
and D79–D81 reports, new Python syntax, and whitespace checks pass.
All computation jobs have finished.

```sh
python3 dembele/pari/194_cm_frame_cubic_lift_check.py --collect-only
python3 dembele/pari/194_cm_frame_cubic_lift_check.py
python3 dembele/pari/194_cm_frame_cubic_lift_check.py --rebuild
```

The first command audits saved hashes; the second reruns the independent
verifier and both controls; the third also rebuilds all D81 stages.

**Next:** fix a representative normalization that persists at higher
precision, then extend the checked lift to 31^4 and 31^8. One concrete
option is to pin 80 independent row-reduced coefficient coordinates of
L(2D0-E_R), after verifying that their derivatives give a unit minor on
the 80-dimensional linear system. This remains to be implemented.
Coefficient reconstruction should follow compatible lifts and an unused
precision check. The prescribed Fuchsian monodromy, base/marking/half
identification, hyperellipticity conflict, target torsion and final field
remain separate outstanding steps. Older arithmetic artifacts are unchanged.
