# Computing equations for 2-group Belyi maps — design & plan

Goal: a robust, tested toolkit that computes explicit equations for 2-group Belyi
maps by climbing the tower **one square root per level** (degree 2^a -> 2^(a+1)),
first over F_q (exact, testable) and then in characteristic zero / number fields.
Ultimate application: compute the 2-power torsion / moduli fields and search for a
**nonsolvable number field ramified only at 2**, or verify none exists up to a
degree bound.

## The mathematical skeleton (thesis Chapter 5)

A 2-group G has a chief series with C_2 factors
    1 = G_0 ◁ G_1 ◁ ... ◁ G_n = G,   G_{i+1}/G_i ≅ C_2  (central).
Dually the Belyi map factors as a tower of **quadratic** covers
    P^1 = X_0 <- X_1 <- ... <- X_n = X,   each X_{i+1} -> X_i of degree 2.
In char ≠ 2 a degree-2 cover is a square root:  k(X_{i+1}) = k(X_i)(sqrt(f_i)),
f_i in k(X_i)^* /(squares).  So the entire curve is encoded by the sequence
(f_0, f_1, ..., f_{n-1}) of "radicands", each living in the previous function field.

The radicand f_i is pinned down (mod squares) by WHERE the quadratic step is
ramified, which the group extension + monodromy dictate: X_{i+1}->X_i ramifies
exactly at the places where the corresponding involution (the nontrivial coset of
G_i in G_{i+1}) acts with a fixed point. Concretely:
  div(f_i)  ≡  (ramification divisor of the step)   mod 2·Div(X_i).
Finding f_i = "find a function with prescribed divisor class mod squares" =
Riemann-Roch / principal-divisor test. THAT is the one nontrivial primitive per
level; everything else is bookkeeping.

Because the ramification orders are 2-powers and we work over F_q with p = char ≠ 2,
**all ramification is tame** — differents are e-1, Riemann-Hurwitz is exact. This
is what makes verification clean and the whole scheme numerically safe over F_q.

## Why "one square root per level" is the magic
- Each level is a *single* quadratic extension: no high-degree resultant/Groebner
  blowup, no solving large nonlinear systems. Cost is dominated by Riemann-Roch in
  the current function field.
- The tower is reusable: a subgroup / quotient reuses lower levels verbatim
  (matches the thesis's "iterative structure" and explains passport splitting).
- Lifting F_q -> char 0 is also square-root-by-square-root (Hensel / CRT on the
  radicands), degree 2 at a time.

## Toolkit architecture
    belyi/
      verify.sage    # ramification, passport, genus, "Belyi?" checks   [Milestone 1]
      towers.sage    # tower-of-quadratics function field container      [M2]
      cyclic.sage    # superelliptic/cyclic builder y^(2^n)=prod         [M2]
      quadstep.sage  # THE primitive: solve for f_i via Riemann-Roch     [M3]
      groups.sage    # chief series + per-level ramification from a triple[M4]
      build.sage     # driver: triple -> tower -> equation               [M4]
      lift.sage      # F_q -> Q(bar) lift, field of definition           [M5]
      arithmetic.sage# J[2], torsion fields, Frobenius fingerprint       [M6]
    tests/           # pytest-style asserts run under sage; thesis + LMFDB oracles

## Verification strategy (the "tests, etc." backbone) — build FIRST
Oracle examples with known answers (from the thesis, exact):
  - y^16 = 1 - x                      deg16 genus0  passport {1,16,16}   (f16T1-1,16,16-g0)
  - y^16 + (4x-2)y^8 + 1              deg16 genus0  passport {2,2,8}     (f16T13-2,2,8-g0)
  - y^16 = -x^2 (x-1)^7               deg16 genus7  passport {8,16,16}   (f16T1-8,16,16-g7)
  - y^8  + 2x^6+2x^5+2x^4+x^3+x^2+x   deg8  genus3  over F_3             (8T1-8,8,4-g3)
Checks each builder output must pass:
  (V1) degree = 2^n.
  (V2) ramified only over {0,1,∞}   [genus_from_(0,1,∞)-ramification == L.genus()].
  (V3) passport (multiset of ramification orders over each of 0,1,∞) matches target.
  (V4) genus matches Riemann-Hurwitz from the triple.
  (V5) [later] monodromy group == G, and refined passport / field of definition.

## Milestones
  M1  verify.sage + tests on the four oracles.  [DONE: 5/5 tests pass]
  M2  cyclic/superelliptic tower (trivial square roots).  [DONE: 4/4 tests pass]
  M3  quadstep primitive (Riemann-Roch radicand); test: Q8 genus-2 tower over F_3.
  M4  group driver: permutation triple -> chief series -> tower -> equation;
      regenerate deg<=16 database over F_3; cross-check counts (census.sage) & genera.
  M5  characteristic-zero lift + field of definition; match thesis Q(bar) equations.
  M6  arithmetic: compute Q(J[2]) / torsion & moduli fields from equations;
      Frobenius fingerprint for NON-Galois covers; run the nonsolvability search
      up to a degree bound, feeding the module-obstruction results from
      torsion_module.sage (Galois case already shown solvable through deg 32).

## Interfaces to work already done
  - count_triples.sage / census.sage : enumeration + genus/structure of triples.
  - torsion_module.sage : Galois-case J[2] centralizer test (solvable => no field).
    Equations are needed precisely where that test is inconclusive (non-Galois) or
    to exhibit the explicit polynomial.

## M3 scoping (path A over F_p) -- de-risked 2026-07-07
KEY SAGE LIMITATION (confirmed): FunctionField.class_group() is the AFFINE class
group (finite maximal order), NOT Pic^0. E.g. z^4=x(x-1)/F_7: class_group order 1
but |Pic^0(F_7)| = L_polynomial(1) = 8. So Cl[2]/representative divisors for the
general radicand solver are NOT available in Sage. => positive-genus intermediate
curves are the Path-C (Hecke.jl) trigger.

BUT genus-0 intermediates need NO class group (Pic^0 trivial): radicand = explicit
S-unit = product of linear factors. Many towers (incl. Q8) pass through genus-0
curves until a final hyperelliptic step. Q8 chief series Q8 > <i> > <-1> > 1 gives
Fix(<i>) g0, Fix(<-1>) g0 (V4-quotient, ram (2,2,2)), X g2 = double cover of a P^1.

CONFIRMED WORKING Sage capabilities for the genus-0 tower solver:
- genus-0 parametrization: RR of a degree-1 place (P.divisor().basis_function_space())
  yields a degree-1 generator t; e.g. y^2=x -> t=y, x=t^2.
- locate S-places in t: t.evaluate(Q) gives the t-value of a place Q over x=0,1,oo.
- L.places_above(base_place), P.divisor(), .basis_function_space() (Riemann-Roch).
- compose_sqrt (M3.1) assembles the absolute model; verify.sage (M1) checks each level.

Method (genus-0 intermediates): parametrize X_i=F_p(t); write x=c*prod(t-t_j)^{e_j}
from div(x); group data (I_Q = H_i cap g<sigma_b>g^{-1} not-subset H_{i+1}) -> which
S-places ramify -> radicand = prod(t-t_j) over them; adjoin sqrt; verify.

## Status
  M1 DONE (2026-07-07): verify.sage passes 4 thesis oracles + negative control.
  M2 DONE (2026-07-07): cyclic.sage builds C_{2^n} Kummer covers; passport formula
       cross-checked against the verifier. 4/4 tests.
  M3 next: quadstep primitive (Riemann-Roch radicand) + general absolute-model tower.
