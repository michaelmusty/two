# Explicit nonsolvable fields ramified only at 2 — status of the search

Goal: an explicit, verifiable nonsolvable number field ramified **only at 2**.

## Verified in Sage (this session)

| source | Galois group | ramified at | note |
|---|---|---|---|
| Bosman, `math/0701442` (deg 17) | SL2(F16) | **2, 137** | field disc 2^30·137^8 — NOT only at 2 |
| Voight et al `17T7` (1.1.4, deg 17) | PSL2(16)⋊C2 = 17T7 | **2, 3, 17** | field disc 2^44·3^6·17^8 — NOT only at 2 |

Both realize the nonsolvable GROUP over Q but pick up extra ramification. The
`17T7` paper also gives an explicit **genus-4 curve** (1.1.6) whose Jacobian's
2-torsion field is the splitting field of (1.1.4); Jac ~ abelian fourfold with RM
attached to Hilbert modular form 2.2.12.1-578.1-d over Q(sqrt 3).

Bosman polynomial:
  x^17 -5x^16 +12x^15 -28x^14 +72x^13 -132x^12 +116x^11 -74x^9 +90x^8 -28x^7
  -12x^6 +24x^5 -12x^4 -4x^3 -3x -1
17T7 (1.1.4):
  x^17 -2x^16 +12x^15 -28x^14 +60x^13 -160x^12 +200x^11 -500x^10 +705x^9 -886x^8
  +2024x^7 -604x^6 +2146x^5 +80x^4 -1376x^3 -496x^2 -1013x -490

## The genuine "ramified only at 2" example: Dembele (2009)
Exists and is PROVEN (nonsolvable Galois extension of Q unramified outside 2, image
SL2(F_2^8)^2 ⋊ Z/2). It is a mod-2 Galois representation of a Hilbert modular form
over Q(zeta_32)^+ (degree 8, disc a power of 2), level a power of 2 -- NOT a small
explicit polynomial.

## LMFDB HMF search (route 1) -- negative
For SL2(F16) ramified only at 2 need: base field totally real with 2-power disc AND
a form with 2 INERT in the Hecke field (residue F16). LMFDB has only two 2-power-disc
totally real fields: 2.2.8.1=Q(sqrt2) (only dim<=2 forms at 2-power level) and
4.4.2048.1=Q(zeta_16)^+ (dim-4 forms exist: 1024.1-r,-v, ramified only at 2, but
Hecke poly x^4-128x^2+2048 = x^4 mod 2, so 2 is RAMIFIED => residue F2 => image in
GL2(F2)=S3, SOLVABLE). Dembele's base field Q(zeta_32)^+ (degree 8) is NOT in LMFDB.
=> No explicit nonsolvable field ramified only at 2 is reachable via LMFDB.

## Conclusion
- The example exists (Dembele) but is not a writable small polynomial and is not in
  LMFDB.
- Making it explicit requires reproducing the Hilbert modular form computation over
  Q(zeta_32)^+ -- needs Magma's HMF package (the 17T7 authors, incl. Voight/Schiavone/
  Costa, have this machinery).
- WHY 2-group Belyi maps can't shortcut this: the successful route builds SL2(F16)
  from the 2-torsion of an abelian variety with REAL MULTIPLICATION (the RM supplies
  the irreducible F16-action). A 2-group deck group is nilpotent, so Aut(X)>=C2 and
  its automorphisms can never supply that F16-action (nilpotency obstruction). The
  HMF/RM route succeeds precisely where the 2-group Belyi route is structurally blocked.
