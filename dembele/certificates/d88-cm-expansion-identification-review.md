# CM expansions as an identification certificate (D88 review)

Date: 2026-09-23. Research review requested by the user, with one small
exact diagnostic on the existing candidate. No Shimura-side jet
certificate, new curve, numerical solve, or remote job is claimed.

**Assessment:** the van Bommel–Costa–Poonen–Srinivasan paper gives a
correct and unusually short verification target for this example. It
does not provide the missing arithmetic expansions. Our CM frame removes
much of the normalization problem, but the saved data do not yet supply
an independent exact first derivative of the canonical map, let alone
the higher coefficients needed for identification. The useful research
target is an independently computed **projective tangent at the degree-17
CM point**, followed by
its higher extensions. The reviewed sources do not currently make even
that first step executable for this datum. More recognition digits alone
would not close this gap.

## 1. What the paper assumes

[Van Bommel–Costa–Poonen–Srinivasan, Theorem 3.1, Lemma 4.1 and
Corollary 4.2](https://arxiv.org/pdf/2506.14026) take exact expansions
of a ground-field basis of regular differentials at a point with a
specified number-field residue field. The local parameter belongs to
the completed local ring over that field. The general reconstruction
bound is 19g+48; the homogeneous-relation bound is instead
B > d(2g−2)/[L:Q] in degree d. The algorithm does not construct its
arithmetic differential basis or expansions from a Fuchsian group.
The distinction matters here: B=352 is unnecessary for verifying our
already supplied quadrics; B=4 suffices. A fresh nonhyperelliptic
reconstruction using degrees two, three and four would use B=4,6,8,
respectively. Their main new algorithmic work addresses the hyperelliptic
case, rather than exact evaluation on compact Shimura curves.

The following application and proposed interface are our deductions,
not an implemented algorithm asserted by that paper.

## 2. The precise sufficient certificate

Let C_sh denote the specified smooth genus-16 Shimura quotient, with
the intended Q-descent. Let D be its closed degree-17 order-two CM
point, L=Q(D), and let Q_1,...,Q_91 be our saved rational quadrics.
Use K_C for the canonical bundle, to avoid confusing it with the
quadratic CM field.

The required hypotheses are:

1. The Q-model and the labelled identification of D with the chosen
   degree-17 field are the intended arithmetic ones.
2. The sixteen canonical coordinates on C_sh are a common nonzero
   scalar times a Q-basis of H^0(C_sh,K_C), in the saved CM frame.
3. Independently on C_sh, every Q_i vanishes to order at least four
   at D in these coordinates.
4. The common zero locus of the Q_i is the smooth geometrically
   integral degree-30 candidate verified in D69.

Then each Q_i defines a global section of 2K_C of degree 60.
Its zero divisor contains 4D of degree 68, so it is identically zero.
The canonical morphism of C_sh has image contained in the candidate.
The image is an irreducible curve and hence is that candidate. Its
pullback of O(1) is K_C, and both have degree 30, so the morphism has
degree one. A degree-one morphism between smooth proper curves is an
isomorphism. **This argument need not assume nonhyperellipticity in
advance.** If its hypotheses hold, it proves it and confronts the
published hyperellipticity claim directly.

The labelled D is preserved because the input specifies its arithmetic
coordinates and residue-field correspondence. **P32 and the degree-nine
B3 marking do not follow automatically.** Their current numerical CM
labels still require independent certification for the downstream cover
comparison. This certificate identifies (C_sh,D), not every D70 marking.

A convenient exact representation of hypothesis 3 is a map

    J_4: Sym^2(Q^16) -> L[t]/(t^4).

After a fixed rational basis of L is chosen, this is a 68-by-136
rational matrix. It must arise from actual Shimura-side jets, not an
arbitrarily supplied matrix with the right kernel. The existing exact
CM coordinates determine only its first seventeen rows: that block
has rank 17 and kernel dimension 119. The missing three coefficients
encode tangent and higher local geometry.

Since deg(2K_C−4D)=−8, restriction of H^0(2K_C) to 4D is injective.
For a nonhyperelliptic genus-16 curve the full product map therefore
has rank 45 and kernel dimension 91. In the hyperelliptic case its
rank is 31 and kernel dimension 105. Once independent arithmetic jets
exist, these are useful exact diagnostics in addition to checking the
91 proposed relations.

A sharper rank certificate can sometimes stop at three coarse
coefficients. Suppose the independent map

    J_3: Sym^2(Q^16) -> L[t]/(t^3)

has rank 45. A hyperelliptic source has product rank 31, so this excludes
that case. The true quadratic ideal and ker(J_3) then both have dimension
91, with the former contained in the latter; hence they coincide. If
that kernel is our saved space of quadrics, the preceding isomorphism
argument applies. Two coefficients cannot give rank 45 because their
target has dimension 34. This rank argument trades the uniform order-four
bound for an exact matrix-rank check; it is not a height assumption.

**New exact diagnostic on the candidate.** The three-term refinement is
attainable for the actual saved candidate. The new
[Magma driver](../magma/d88_candidate_cm_jet_rank_v2.m) works over
F_(31^17), using the irreducible reduction of the known degree-17
polynomial and the exact reduction of the saved point. In the chart
X1=1 it uses t=X2/X1−(X2/X1)(P). The affine tangent has dimension one;
the parameter derivative is nonzero. It solves for the coefficients
of t and t^2 and evaluates all 136 quadratic monomials. The resulting
ranks are exactly

    one coefficient: 17; two coefficients: 34; three coefficients: 45.

All 91 quadrics annihilate that 51-by-136 matrix and remain independent
modulo 31. D69/D70 already give the smooth candidate and its flat reduced
CM divisor at 31. The chart and parameter remain valid in that model,
so the nonzero special-fiber minor proves rank at least 45 over Q;
h^0(2K)=45 gives equality. Equivalently, on the candidate,
H^0(2K−3D)=0. **This establishes the size of a sufficient comparison
packet; it does not identify any of its coefficients as Shimura values.**

The [independent Python checker](../pari/d88_candidate_cm_jet_rank_check.py)
uses finite-field polynomial arithmetic to reconstruct the matrix from
the saved jets, checks all quadric identities, and recomputes the ranks.
The nonlinear reparametrization t_old=t_new+t_new^2 preserves the kernel;
changing one highest jet coefficient preserves the first two blocks
but is rejected by the equations. Its
[JSON artifact](../data/computed/d88_candidate_cm_jet_rank.json) records
the exact jets, full matrix, input hashes, and both job receipts. The
successful job took 0.347 seconds within the 180-second / 2 GB bounds
using runner 272. The original 1.324-second failure used the wrong
matrix layout for a multi-index Magma comprehension; that source,
failed log and receipt are retained. The successful driver builds rows
explicitly. Neither attempt edits a previous computation.

Recheck this diagnostic from the repository root:

```sh
python3 dembele/pari/d88_candidate_cm_jet_rank_check.py --check
```

This check passed after artifact creation. It validates the new data
and the hashes of the prior candidate/verification records it uses;
it does not rerun the full D87 provenance audit or prove a new
Shimura-side statement.

## 3. What the frame gives, and how to remove period normalization

[D68](curve-construction-sources-2026-09-18.md) gives a valid conditional
arithmetic coordinate construction. If H^0(K_C−D)=0, choose a function
h with simple polar divisor D. Residues identify H^0(K_C) with the
trace-zero subspace of L. Numerically, the left kernel of the seventeen
canonical value rows obtains the same projective frame without first
constructing h. Local row scales cancel.

However, the target frame's full rank and nonzero kernel weights are
still numerical, and the label comparison retains D59's numerical
orientation/root-matching inputs. Exact membership of D in the
candidate does not certify these statements on C_sh. More crucially,
the residue field and frame determine point coordinates, not tangent
lines or infinitesimal neighborhoods. Knowing the abstract completed
local ring L[[t]] is not an evaluation algorithm for global sections.

There is a useful simplification for a future arithmetic implementation.
Choose a coordinate b nonzero at P in D and put

    r_j = omega_j/omega_b.

These are Q-rational functions; the common differential scalar cancels.
Choose a with d(r_a)(P) nonzero and set

    t = r_a − r_a(P).

This is a uniformizer over L. Then r_b=1, r_a=r_a(P)+t, and all
coefficients of r_j modulo t^4 lie in L. Each homogeneous relation is
checked as Q_i(r_1,...,r_16)=0 modulo t^4. We do not need a numerical
value of a CM period, an absolute normalization of the omega_j, or a
comparison between that period and the disk coordinate. The nonzero
derivative must itself be justified. This parametrization is a
conditional simplification, not a proof that the current numerical
ratios are exact L-series.

At an order-two elliptic point, use a centered disk coordinate z with
stabilizer z -> −z. A coarse coordinate is u=z^2, and

    omega_j = f_j(u) du
            = 2z(f_j0 + f_j1*z^2 + f_j2*z^4 + f_j3*z^6 + ... ) dz.

Thus the four coarse differential coefficients require the upstairs
terms of degrees 1,3,5,7. A re-expansion must include the differential
Jacobian; taking ratios avoids that common factor. The raw disk square
need not be an arithmetic parameter over L. Reverting the ratio-defined
parameter t handles a general analytic reparametrization, not merely
a scalar period adjustment.

## 4. What the current files actually contain

Read-only inspection covered the D57/D59/D68/D69/D70 reports,
`pari/114_cm_projective_frame.py`, and their saved JSON interfaces.

| Saved input | Usable information | Missing for J_4 |
|---|---|---|
| Exact quaternion embeddings and CM ideals | CM field, optimal embeddings, ideal-class labels | Evaluation of global differentials or their derivatives |
| `cm_orbit.json` | Labels and the recorded complex-root correspondence | Independent interval certification of its analytic comparisons |
| `cm_projective_frame.json` | Numerical change matrices, bank comparisons, exact abstract trace-zero basis | Exact Shimura-side derivatives |
| `cm_frame_curve_candidate.json` | Exact quadrics and exact projective coordinates over L | Identification of their formal neighborhood with C_sh |
| Saved native differential banks | Numerical expansions and strong empirical consistency | Bounds for the true solution and infinite tail |
| Candidate implicit jets and 31-adic lifts | Exact or finite-precision identities on the candidate | Independent Shimura input |

In particular, script 114's CM sampling computes first derivatives of
the upstairs forms to obtain **coarse values**. It does not provide
three further arithmetic coarse derivatives. Its later products use
numerical series at the order-32 center. Current/previous banks give
scaled 45th singular values about 2.88456e−5 and 46th values about
1.4e−16 / 1.7e−16; these are empirical diagnostics, not certified ranks.
No new analytic evaluation was run in this review; the exact
candidate diagnostic is described separately above.

## 5. Possible sources of the missing map

**Analytic CM expansions.**
[Voight–Willis, Theorem 2.5, equations (5)–(7), and section 3](https://jvoight.github.io/articles/ModFormPaper-090317.pdf)
provide period-graded CM algebraicity and a numerical expansion method.
They explicitly leave rigorous approximation as further work. Algebraicity
is valuable for discovery, but supplies neither our exact coefficients
nor an effective height/denominator bound for recognizing them. The
ratio normalization above improves the interface; it does not upgrade
recognition to proof. A certified error ball still cannot prove an
unknown algebraic number equals a proposed one without a separation
bound or an independent identity.

**Ordinary CM deformation.**
[Mori, sections 3.1–3.2, especially Proposition 3.3 and Theorems 3.6/3.8](https://arxiv.org/pdf/math/0406388)
connects Serre–Tate expansions and normalized CM derivatives. The setup
uses modular curves and quaternionic false elliptic curves over Q; it
is not a ready implementation for our quaternion algebra over the
real octic field. It presupposes arithmetic modular forms and CM test
objects. A formal parameter alone does not compute their restrictions.
For our example, D57's exact splitting calculation makes 31 a plausible
prime for investigating such a method. Before a computation, one must
specify the relevant integral moduli model, CM object and quotient
marking, prove the required ordinary local description, and construct
an arithmetic restriction map for the sixteen sections. A finite
31-adic approximation without a global recognition bound would again
be evidence rather than the proposed characteristic-zero certificate.

**Hecke eigenvalues and theta evaluation.**
[Nelson, section 3.4 and Remark 5.1](https://arxiv.org/pdf/1210.1243)
gives derivative evaluation through an explicit convergent formula in
the rational-quaternion setting; the general method extends further,
but that paper defers the detailed totally real application. It offers
a possible independent analytic evaluator. The paper does not give us
an exact, ready restriction map over this degree-eight field. Likewise,
Jacquet–Langlands identification of Hecke eigensystems does not by
itself identify the multiplication of Hilbert modular forms with our
curve's canonical ring. This source needs a separate adaptation before
it can replace the saved numerical engine.

## 6. Recommended bounded next deliverable

First settle an implementation question: identify an exact arithmetic
restriction map for this quaternionic datum. A Serre–Tate parameter,
CM algebraicity theorem, or candidate-derived tangent is insufficient.
No inspected source currently supplies that map in an executable form.
Calling it “compute the CM jets” would conceal the unsolved task.

The smallest useful success condition for an arithmetic construction
is a **Shimura-side projective tangent**, not a full 352-term
reconstruction:

- Fix the known field L and CM label, a nonzero coordinate b, and a
  candidate parameter coordinate a using the saved data.
- Obtain the first-order restriction of the actual sixteen arithmetic
  canonical sections at that labelled CM point, independently of the
  candidate equations. Output the normalized tangent vector
  `(d r_j / d r_a)(P)` in L, or an exact formula that computes it.
- State the theorem or arithmetic model making the computation an
  evaluation on C_sh. Then compare with the candidate tangent and
  numerical banks as independent checks. Failure of this first-order
  comparison is already decisive against the proposed identification.
- If successful, extend through t^2 and check rank 45 and the saved
  quadratic kernel. Once the arithmetic inputs are certified, a different
  rank or kernel refutes this marked comparison. The four-coefficient
  degree criterion remains an alternative proof method, not a way to
  override such a mismatch. Retain independent Shimura-side provenance.

The candidate tangent and truncated jets have now been calculated
modulo 31, and the rank certificate gives a concrete comparison target.
This alone does not satisfy the independent-evaluation milestone. The
crucial human/research input is a way to evaluate the arithmetic canonical
sections on the CM deformation for this particular
quaternionic datum. The reviewed paper establishes what to do **after**
that input is available. The practical next research decision is which
source can construct this restriction map; the present source audit
does not justify scheduling an exact Shimura-jet computation yet.

If no such arithmetic evaluator is accessible, a different bounded
verification project is to certify at least 32 independent products of
actual analytic differentials. That would independently rule out
hyperellipticity without recognizing any zero relation. It still needs
true-solution and tail bounds, and it would not identify the candidate.
It is a fallback aimed at the published conflict, not a substitute for
J_4 or authorization for another large numerical solve.

No arithmetic identification or target field construction is completed
by this review. Frozen scripts, computed artifacts, root audits and
remote state were not modified.
