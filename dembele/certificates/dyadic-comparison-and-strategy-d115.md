# D115: the actual rational-frame comparison and a revised construction plan

Date: 2026-09-25. The user requested a reassessment followed by sustained
execution, without repeated approval stops.

The dyadic route has now reached its first actual arithmetic comparison
with the candidate. We resolved the previously invisible W value,
constructed the harmonic-to-rational-residue frame, certified the chosen
ratio parameter at the CM divisor, and compared the first two ratio
coefficients at its sixteen non-anchor dyadic embeddings. Every comparison
is compatible with the candidate, with difference valuations at least
**101 and 70 in v_beta**, respectively.

This supports retaining the route and candidate. It does **not** identify
the curve exactly. The present height-based equality bounds require
**274241 and 820774 beta-digits** at the degree-16 dyadic place. This is
the main remaining gap in this comparison, not an unresolved differential
value or an unimplemented frame change. No target field polynomial has
been constructed.

## 1. Reassess the route against its intended output

The target remains the original residual kernels in Dembélé's construction,
with normal closure group SL2(F256)^2 by C8. A polynomial with a similar
group or several matching Frobenius traces is not sufficient. D100's
three major dependencies still apply:

1. Identify the marked arithmetic genus-16 base and its genus-40 cover.
2. Obtain exact global genus-64 cubic or equivalent arithmetic section data.
3. Extract the specified residual constituent and a separating degree-257
   invariant, with a proof that it has the original kernel.

D51 supplies the abstract arithmetic carrier. D99's nonhyperellipticity
changes the curve model, without invalidating field existence. The dyadic
Poisson construction remains a useful independent evaluator for the first
dependency; the candidate is not used to construct its measures or moments.
The independent comparison is a necessary test of this branch before
investing in its downstream cubic and torsion calculations.

The immediate plan was therefore changed from another isolated W pilot to
an end-to-end diagnostic: resolve W, change frames, establish the ratio
chart, and compare two positive orders. A certified mismatch would refute
the proposed marked comparison. A match must still be assessed against an
explicit exactness criterion. The run pursued this chain without approval
stops and without increasing a process timeout.

The general moment/Poisson framework is described by
[Franc--Masdeu, section 6.1](https://arxiv.org/pdf/1201.0356).
Their paper also distinguishes numerically recognized curve equations
from a proof of those equations. We use D108/D113's direct ramified-field
arguments, rather than their Qp control theorem or precision constants.

## 2. Full quotient arithmetic and efficient refinement

The completed runs use the full polynomial

    pi^8 - 8*pi^6 + 20*pi^4 - 16*pi^2 + 2.

At P divisible by 8, coefficient reduction modulo 2^(P/8) represents
O_K/(pi^P). In particular, the pi^8=-2 shortcut is not used above P=16.
Source 417 initially implements exact packed scalar/vector products with
guard bits and full polynomial reduction. Ordinary signed convolution
checks multiplication, including the previously omitted pi^4 term.

Only the positive degrees below P are iterated. Columns k>=P vanish
modulo pi^P, and higher state rows are recovered afterward. A previous
bank at precision P0 provides a seed. Its zeroth entries must first be
replaced by the **exact** masses; they are not unknowns of the contraction.
The first two new probes caught this initializer mistake and were archived.
Restoring exact masses retained the original contraction assertion and
produced successive correction valuations P0,...,P-1.

Source 420 updates only the correction delta: delta_next=T*delta. If
v(delta)>=s, columns k>=P-s can be omitted. Sources 422/426 batch the
coefficient construction across all 165 distinct child maps. Source 429
also avoids materializing the entire transformed high-degree moment bank:
CM transfers transform one target state at a time. All arrays contain
bounded integers; explicit bounds keep their products inside signed int64.
The higher-precision coarse sums reduce after each term to prevent overflow.

The sequence of completed working precisions was

    16 -> 24 -> 40 -> 56 -> 72 -> 104 -> 136 -> 152 -> 200.

All state overlaps pass. The final bank contains **1,667,616 state entries**
(174 charts, degrees 0..598, sixteen measures) and **108,800 CM A-chart
entries** (17 charts, degrees 0..399, sixteen measures), with errors at
least pi^200. Only chart A is required because D114 proved the exact
identity g_j=2*integral_A K_j dmu.

## 3. Refine the same splitting branch when the old centers run out

The old normalized child and CM centers had errors at least 159 and 165.
They suffice through P=152, but cannot simply be reused at P=200.
Source 425 performs one Newton refinement of D109's specified root of
x^2+y^2+1. Its residual valuation is 360, derivative valuation is 8,
and root error is 352. The new and old centers agree to the old error 180,
so this is the same Hensel branch.

Every saved exact matrix C+S*x is retained. Re-normalizing its center gives
child and CM errors at least **331 and 337**, respectively. All old centers
agree to their previous bounds; quaternion transports, partitions, local
frames and CM labels are unchanged. Two failed probes arose from comparing
the finite sentinel for v(0) against a larger bound on an exactly constant
matrix. Checking exact equality first resolves that implementation issue.
Both failed sources, logs and receipts are archived.

Review 428 independently verifies the Hensel inequalities, exact matrix
identities N*V_22=V, all new error bounds, and preservation of the exact
transport matrices. No new splitting choice, class census or tree search
is involved.

## 4. Resolve W and preserve the actual coarse-coordinate conventions

The coefficients remain those of

    omega_a=(g_(a,0)+g_(a,1)*u+g_(a,2)*u^2+...)*du,
    u=((z-beta)/(z+beta))^2,      beta^2=-(2+pi).

At moment precision P, the twice-A formula has beta-error bounds
2P+32, 2P+48, 2P+32. At P=200 these are **432,448,432**, or
**216,224,216 pi-digits**. All 816 computed harmonic-basis entries
at the seventeen points are certified nonzero.

At W the leading valuations, in harmonic basis order, are

    [296,308,308,314,314,314,314,318,
     326,326,326,326,322,322,322,322].

The first entry was resolved already at P=136, with valuation 296 below
error 304. The final errors leave 136 beta-digits relative to that value.
Its valuation is 148 in v_pi, or 18.5 in v2; the earlier zero enclosures
were therefore insufficient. No earlier lower bound is contradicted.

Source 419 also checks that W's A chart reaches nonzero harmonic support:
the first such state is five child steps away, with mass -4 in one basis
direction. Its support is not empty. This check does not by itself bound
the cancellation in polynomial moments or differential coefficients.

Reviews 421, 424 and 428 verify the retained state equations and CM
transfers with separate ordinary integer arithmetic. The later reviews
certify every coefficient table by the exact polynomial identity

    (1+cX)*phi(X)^(n+1)=(b+aX)*phi(X)^n.

Together with the constant row this uniquely determines all retained
coefficients. Independent expansion of

    2*K_j(t)=1-((beta+t)/(beta-t))^(2j+2)

checks the coarse kernels and all resulting values. The final review
also verifies all 713 D114 source hashes unchanged.

## 5. Construct the rational residue frame before consulting the candidate

Let H_i be the row of actual leading harmonic coefficients at CM point i.
Normalize each row by a certified beta power s_i so h_i=H_i/s_i has at
least one unit entry. Let D contain the sixteen non-anchor rows and put

    q=h_W*D^(-1),       E_i=(sigma_i(eta_1),...,sigma_i(eta_16)).

D112 supplies the arithmetic E_i, independently of the candidate, and
sum_i E_i=0. All sixteen pivots of D and all q_i are certified nonzero.
Define

    M=D^(-1)*diag(q_i^(-1))*E_nonanchor.

Then h_i*M=E_i/q_i for non-anchor i, and h_W*M=-E_W. By D105--D106's
projective-frame and residue argument, M is the actual rational residue
basis change up to one common nonzero scalar. The row normalizations
do not change this projective identification.

Sources 418 and 427 propagate local balls through every field operation
and matrix division. If x and y have errors e_x,e_y and known valuations
v_x,v_y, multiplication has error at least
min(e_x+v_y,e_y+v_x); division by certified nonzero y has error at least
min(e_x-v_y,e_y+v_x-2v_y). Unknown balls use their valuation lower bounds.
No unresolved center is inverted. At P=136 the frame succeeds but the
chosen Gaussian pivot is still unresolved; P=152 first resolves the
non-anchor tangent comparison.

The source-427 field arithmetic retains 448 beta-digits and explicitly
accounts for losses when removing powers of beta or inverting units.
All seventeen transformed constant rows enclose the required projective
residue values. Candidate coefficients enter only after M is constructed.

## 6. Actual ratio coefficients and the independent series check

In the rational frame let f,a,b be the local coefficients of omega_1,
omega_2,omega_j. Put t=omega_2/omega_1-(omega_2/omega_1)(P). With f_k,a_k,b_k
the coarse coefficients, set

    G=f_0*a_1-a_0*f_1,             H=f_0*b_1-b_0*f_1,
    A2=f_0*a_2-a_0*f_2,           B2=f_0*b_2-b_0*f_2.

The first two ratio Taylor coefficients are

    a_(1,j)=H/G,
    a_(2,j)=f_0^2*(G*B2-H*A2)/G^3.

The second formula is D106's derivative formula after cancelling its
factor 2 against the conversion from second Taylor coefficients to
second derivatives. No dyadic division is silently dropped.

At every non-anchor point the saved G has valuation 153 and error 254,
so the parameter is certified. Source 430 checks the calculation by a
different route: divide the differential series to obtain ratios in u,
then invert t=t1*u+t2*u^2. It checks

    a1=r1/t1,       a2=(r2-a1*t2)/t1^2.

It also checks the seventeen projective constant rows without choosing
their local scalars. All **256 entries per positive order** agree with
the exact D106 candidate packet within the following certified bounds:

| Ratio order | Difference valuation at least v_beta | In v_pi |
|---:|---:|---:|
| 1 | 101 | 50.5 |
| 2 | 70 | 35 |

There are 512 comparisons, including the fixed normalization coordinates.
These sixteen points are conjugates at the same degree-16 dyadic place;
they must not be counted as sixteen independent places in a height bound.
Since v_beta(2)=16, the displayed valuation precisions correspond to
101/16 and 70/16 in v2.

The Gaussian at W remains numerically unresolved at its bound 825. It is
nevertheless nonzero qualitatively: D106's rational frame makes the
vanishing locus on D Galois stable, and one nonzero value on the transitive
degree-17 divisor rules out vanishing at any of its points. This establishes
the common ratio chart on D, not an everywhere nonvanishing Gaussian on C.
No numerical division by W's unresolved Gaussian is performed.

## 7. Exactness is now the binding requirement

D106 bounds the absolute logarithmic heights of the actual-minus-candidate
ratio differences by B1=111817/10 and B2=334657/10. The degree-17 field
has dyadic local degrees 1 and 16. A nonzero difference delta satisfies

    h(delta) >= (log(2)/17)*(max(0,v2(delta_W))
                              +16*max(0,v2(delta_nonanchor))).

Source 423 uses exact rational bounds on log(2), from the atanh series,
to obtain sufficient equality thresholds:

| Available place(s) | First order, beta-digits | Second order, beta-digits |
|---|---:|---:|
| Degree-16 place only | 274241 | 820774 |
| Both places with a common beta bound | 258109 | 772493 |
| Rational W place only | 4387846 | 13132378 |

For the actual comparison available here, the first line applies. Its
integer pi-digit thresholds are **137121 and 410387**. The more favorable
both-place thresholds are 129055 and 386247, but a W ratio error of that
size has not been computed. All are sufficient bounds, not necessary
precision claims or lower bounds on the difficulty of a different proof.

Thus the computed congruences do not activate D88/D106's exact J3 rank-45
criterion. Three exact coefficients would suffice for that geometric
criterion; knowing three coefficient enclosures is a different statement.
See [van Bommel--Costa--Poonen--Srinivasan](https://arxiv.org/abs/2506.14026)
for the reconstruction framework. It does not turn these finite
congruences into exact algebraic equalities without an additional input.

## 8. Decision and remaining plan

Retain the Shimura/Jacobian route and its candidate: the independent
comparison has found no contradiction, and the formerly missing frame
and CM ratio chart are now available. This is evidence for the proposed
identification, not a completed proof or a quantified probability.

Do not make another routine precision increase the default next step.
The existing height bound is executable as a mathematical specification,
but production at its scale is not supported by the present moment
algorithm. The next research objective is an **exact arithmetic
identification certificate**. A proposed replacement must supply either
an effective substantially sharper bound on the actual unknown ratios
or an exact identity/correspondence with a proved uniqueness argument.
A bound on candidate coefficients alone, extra matching primes, or
another finite Taylor agreement does not supply this.

No such replacement is proved in this run. This is a remaining mathematical
gap, not a request for approval. The local computational plan has been
carried through to a reviewed two-order comparison; the global field
construction remains unfinished at the exact-identification step.

Once that step is closed, the marked P32/B3 and double-cover character
checks remain explicit obligations. Only then apply the conditional
nine-cover shortcut and construct exact global genus-64 cubic/section
data. Frobenius isolation at norm 97, combined genus-64 torsion scaling,
the correct F256 subspace and a separating degree-257 invariant remain
later requirements. Keep the existing census, new-level, Hecke-bank and
cubic-precision pauses and the 180-second process-group cap.

## 9. Artifacts and reproducibility

The final data are

- `dyadic_precision200_d115.json`: actual moment bank and harmonic coarse jets;
- `dyadic_moment_transports_refined_d115.json`: same-branch refined centers;
- `dyadic_comparison200_d115.json`: actual frame, pivots, ratio coefficients,
  candidate references, and differences with individual error bounds;
- `dyadic_precision200_review_d115.json`: independent operator/moment/kernel review;
- `dyadic_ratio_series_review_d115.json`: formal-series comparison review;
- `dyadic_exactness_budget_d115.json`: rational product-formula budgets;
- `dyadic_strategy_review_d115.json`: final source-preservation audit.

The source ledger is
[dyadic_comparison_sources_d115.json](../data/computed/dyadic_comparison_sources_d115.json).
Sources 417--430 and successful bound artifacts are frozen. Before the
final audit, 24 jobs passed and four implementation probes failed, with
all failures archived. The longest run took 145.02 seconds. The final
precision-200 solve/review took 114.97/39.29 seconds; the two-order
comparison and formal-series review took 9.81/7.53 seconds. No timeout
was increased, and no job timed out.

Recheck the final audit through runner 272:

    python3 dembele/pari/431_dyadic_strategy_review.py --check

The audit binds finite witnesses and executable arithmetic, including
all 713 prior source hashes. It does not machine-verify the cited
uniformization, CM reciprocity or geometric descent theorems. All seven
entry documents record the new status. No correspondence was sent.
