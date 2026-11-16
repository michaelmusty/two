# Step 4 design notes (673-adic lift and evaluation)

Date: 2026-11-15. Working notes, not a certificate. Nothing here is
computed unless stated. Status of inputs: five points of V_b mod 673
(`results/torsion_points673_log.txt`); span check in progress (script 09).

## 1. The evaluation function must be global

The polynomial has coefficients in F only if the function evaluated on
V_b is defined over F. The cubic model of Y mod 673 (scripts 05, 07)
depends on choices made mod 673 (q, moving section, representative of the
third), so sections of the Y model are not global objects. Global objects
available exactly: C, X, the divisors D17, P32, B3, T, E on C, and
pullbacks to Y of functions on C. The two points of Y above P32 (one
ramified, one not) are canonical points of Y.

Proposed function. For x in V_b, take M on C of degree 21 defined over Q
and R2 the unramified point of Y above P32. deg(pi^*M + R2) = 64 = g(Y),
so generically there is one effective D_x in |x + pi^*M + R2|. Its
pushforward pi_*(D_x) is an effective divisor of degree 64 on C in the
class 3M + P32 (the norm of x is 0), i.e. a point of P(L_C(3M + P32)),
an exactly known projective space of dimension 48 over Q. Ratios of its
coordinates are Galois-equivariant functions of x that involve Y only
through the map pi. Not yet implemented, not yet tested mod 673.

## 2. The F_256-structure is not visible from Frobenius alone

The 257 roots are the lines of V_b for the Hecke field H = F_256. At 673
we only have Frob, with minimal polynomial g of degree 8, so V_b is a
2-dimensional space over F' = F_2[Frob], and every F'-line is
Frob-stable. H commutes with Frob, and Frob has eigenvalues lambda,
lambda^-1 = lambda^16 on two H-lines L1, L2. H acts as F' on L1 and as F'
twisted by the 4th power of the 2-Frobenius on L2. So H is determined by
the unordered pair {L1, L2} of F'-lines: 257*256/2 = 32896 candidates.
Hecke operators are self-adjoint for the Weil pairing, which forces L1,
L2 to be isotropic; if the count of isotropic F'-lines is 17 (unitary
form in dimension 2 over F_256/F_16; not double-checked) this leaves 136
candidates. The correct pair is the one for which the degree-257
polynomial has coefficients in F; this can only be decided after lifting
(recognition test on a coefficient that depends on the partition, e.g.
sum over lines of (sum of values on the line)^2). The Weil pairing on
V_b mod 673 is not implemented.

## 3. Coefficient field may be Q(sqrt 2)

V_b as an F_2-space is the kernel of a maximal ideal of the Z-Hecke
algebra, so it is stable under the subgroup C4 of Gal(F/Q) = C8 that
fixes the system b up to automorphisms of F_256 (assuming a and b are
exchanged by the other coset, unchecked, D160). If Y and the function of
section 1 are defined over Q(sqrt 2) (or Q), the 257 lines form a
G_Q(sqrt 2)-stable set and the polynomial has coefficients in Q(sqrt 2).
Recognition would then need precision 2*h instead of 8*h (h = coefficient
height). Unverified; depends on the field of definition of Y.

## 4. Cost model and the height risk

- Lift of the model: X is exact. The third A over Z/p^N is c*Delta with
  3c = -1 mod m*p^(N-1) (scalar of about 224 + 9.4N bits; arithmetic over
  Z/p^N on X, constants Z_673). Then ports of 05 and 07 over Z/p^N need
  linear algebra over Z/p^N (Hensel-lifted nullspaces).
- Lift of torsion points: over W_N(K), K = F_673^17. Multiplying an
  arbitrary lift by p^(N-1) costs about 14 N additions at full precision:
  too slow beyond small N. Mascot's linearized lifting is needed.
- All of V_b: 65535 nonzero points, 3855 Frobenius orbits; one addition
  and one evaluation each at full precision.
- Size: an element of W_N(K) has 160 N bits. A class matrix (66 x 400) at
  N = 1000 is about 530 MB; intermediate 324 x 400 matrices 2.6 GB.
- The precision N needed is (2 or 8) * h / log(673), and h is unknown.
  Mascot's computations over Q at genus about 50 used thousands of p-adic
  digits. If h is of that order, N at 673 would be in the thousands to
  tens of thousands, where a single addition costs hours to days. This is
  the main risk of step 4 and is not resolved.

## 5. Order of work

1. Span check of two points (running).
2. Implement the function of section 1 mod 673; check Frobenius
   equivariance and that it separates points.
3. Weil pairing on V_b mod 673; list the isotropic F'-lines.
4. Prototype arithmetic over W_N(K) at N = 2, 4, 8 to measure cost
   against N before committing to a lift.
5. Decide feasibility with measured costs; the fallback prime 7 (D164)
   has field degree 12 for system b.

## 6. Results of 2026-11-16 and revised lifting route (D166)

Computed mod 673 (logs `results/eval_function673_log.txt`,
`results/tangency673_log.txt`; scripts 10, 11):

- The function of section 1 is implemented with N = 22*P32 and without the
  points above P32: S_x = H^0(x (x) pi^*O(22 P32)) is 3-dimensional; the
  trace forms b(s,s') = Tr_{Y/C}(s s'/(phi Q^2)) lie in L_C(44 P32)
  (29-dim, checked by solving); the leading coefficient at P32 gives a
  form of rank 2 on S_x whose radical is the section vanishing at both
  points above P32; f_x = b(s_x, s_x). On pt11 and pt13: two
  representatives of the class give the same f_x; f(Frob y) = Frob f(y);
  f separates y from Frob y and pt11 from pt13. 4 s per evaluation over K.
- G44 = H^0(Y, pi^*O(44 P32)) has dimension 69; the six functions
  g_ij = s_i s_j / phi lie in G44 and satisfy the 2x2 minor equations;
  the linearized minor map on the 414 coefficients has rank 405, kernel 9
  = the GL_3 gauge. So each 2-torsion class is an isolated solution of a
  quadratic system in G44.

Revised route. Do not lift Jacobian arithmetic on Y. Lift, for each
point of V_b, the six functions g_ij in G44 by Newton/Hensel on the minor
equations (414 unknowns over W_N(K)), starting from the mod-673 values
computed with scripts 08-11. f_x is read off from the g_ij (trace to C
and the leading coefficient at P32). Needed first: G44 and G88 with
their multiplication to precision N, i.e. the 673-adic model of Y over C
(the functions a, h of the cubic, or equivalently the third A), over
Z_673 only (constants of degree 1). The third can be lifted by the same
device on X (cubes instead of squares). Cost estimates are in D166 and
are not measured.

## 7. The third as a cube system on X (script 13, passed mod 673)

With S = 79 auxiliary points of X, L(E_R - S) is 2-dimensional; the four
functions c_ijk = beta_i beta_j beta_k u lie in U = L(4 D0 - 3S - B)
(84-dim) and satisfy the twisted-cubic relations; the linearized
relations have rank 332 of 336, kernel 4 = the GL_2 gauge (log
`results/cube_system673_log.txt`, 6 s). So the cubic cover is also an
isolated solution of a small quadratic system, over Z_673 (constants of
degree 1). For the lift, S must be replaced by an exactly defined divisor
(or by points lifted to Z_673; the class of the solution does not depend
on S, only the functions do).

Work packages for the lift (none started):
1. X-level section spaces over Z/673^N as value vectors at lifted points
   (port of script 03; the odd cubics lifted by linear algebra).
2. Branch data Dplus, Dminus over Z/673^N (nonic algebra).
3. Newton lift of the c_ijk; recover E_R, u, q, f at precision N.
4. G44, G88, multiplication, trace to C, leading coefficient at P32.
5. Newton lift of the g_ij for each Frobenius orbit of V_b, over W_N(K).
6. An exact Q-basis of L_C(44 P32).
7. F_256-structure and recognition of the coefficients.

## 8. Smaller per-point system and a staged precision plan (D167)

Measured (Chatelet, Magma): one product in W_N(F_673^17) takes 2 ms at
N = 1000 (9.4 kbit) and 16 ms at N = 5000 (47 kbit), schoolbook over the 17
coefficients. A 405-dimensional linear solve per point at 170 kbit would
cost days, so the 414-unknown system of section 6 is too large.

Smaller system (script 14, passed mod 673 on pt11 and pt13): take two
complete rational fibres of Y -> C; s_A, s_B in S_x vanish at two points of
the first, resp. second fibre; g = s_A^2/phi, g' = s_B^2/phi,
h = s_A s_B/phi lie in G44 with those simple zeros imposed (dimensions
67, 67, 65) and satisfy g g' = h^2. Linearization: 199 unknowns, rank 197,
kernel 2 = the two scalings. The fibres need not be global; f_x is then
obtained from g by a second, linear step (S_x from s_A: not yet written).

Staged plan. Build the pipeline with the precision as a parameter; run all
3855 orbits first at low precision (about 2 kbit); try to recognize
e_1 = sum of r(x) over all nonzero x in V_b, which does not depend on the
F_256-structure and has the height of a single value. That measures the
height and decides the coefficient field (Q(sqrt 2) or F) before any
high-precision run. Per-point cost at 170 kbit is estimated at 2-3 hours
with a frozen low-precision inverse and linear iteration (not measured).
