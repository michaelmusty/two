# D148: a joint bound from the CM filtration and forward residue map

Continuation of the authorized proof-gap investigation.

**Result:** the actual relation space in the fixed rational residue
coordinates satisfies

    h_ext(I_2) < 15237.

This improves D142's 83240 by more than a factor of five. It still
does not reach the sufficient P1600 target 623. The unrounded upper
expression is 15236.599070671391... . No candidate coefficient height
or unproved positive vanishing is an input.

The calculation handles the frame and multiplication quotient together.
It avoids a new spectral determinant and does not identify the rank-45
ordinary bicanonical space with the rank-72 orbifold space. In D147's
notation it also gives an upper bound below 15193 for R-t_mu, not for
R alone. Neither the target height nor candidate identification is proved.

There is a useful limitation: deleting the entire positive field-basis
size term from this particular majorant still leaves
11266.237580094368... . Thus sharpening only that size estimate cannot
make this bound reach 623. This is a floor for the displayed estimate,
**not a lower bound on the actual relation-space height**, and supplies
no reason by itself to increase P1600.

## 1. The actual multiplication image with its quotient metric

Use the actual rational marked curve and its stable differential lattice
from D99/D106/D116, after a number-field extension giving stable reduction
and splitting the CM divisor D=P_0+...+P_16. Normalized degrees count all
complex embeddings. Let

    E=H^0(omega), A=Sym^2 E, J=ker(mu), M=im(mu),
    mu:A -> H^0(omega^2),       ranks (E,A,J,M)=(16,136,91,45).

E has the established L2 metric, A its quotient symmetric metric, J
the subspace metric, and M the quotient metric. Thus the exact sequence
of lattices gives

    deg(J)=17F+60log(2)-deg(M).                               (1)

This uses the image lattice M. It neither assumes global integral
surjectivity nor drops an odd-prime multiplication index with the wrong
sign. D147 proved surjectivity at 2, but (1) is valid without that extra
fact. Finite multiplication cokernels are absorbed by using M.

Filter the actual image, without reference to the candidate, by

    M_n=M intersect H^0(2K_C-nD), n=0,1,2,3.

These are saturated sublattices of M. D140's rank-45 actual jet map gives
M_3=0 on the generic fibre, hence M_3=0. Riemann--Roch gives rank(M_1)=28
and rank(M_2)=11+h^0(2D-K_C). Since 2D-K_C has degree four, strict
Clifford for the already proved nonhyperelliptic curve gives h^0<=2.
The equality criterion is stated in
[Bertram, Special Divisors, pages 3--4](https://www.math.utah.edu/~bertram/6180/Special.pdf).
Consequently the quotient ranks are

    (k_0,k_1,k_2)=(17,k_1,28-k_1),   15<=k_1<=17.             (2)

For each n, the leading divided jet of a section of M_n is an integral
element of W_i^(n+2), where W_i=P_i^*omega. This is the intrinsic
successive-jet construction from D116, with no extra twisting line.
At a smooth section it is its usual Taylor coefficient. At a nodal
specialization D116's integral binomial-derivation argument applies
because all lower jets are zero by the definition of M_n. We do not
assert that an unrestricted higher derivative divided by n! is integral.

The leading-jet map kills M_(n+1), and is generically injective on the
quotient M_n/M_(n+1) after using all seventeen points. Choose k_n
coordinates giving a nonzero determinant. Their target determinant
line has degree k_n(n+2)H, since the seventeen W_i have the same
normalized arithmetic degree H. It is not necessary to divide by any
evaluation determinant. Intersections of CM sections can increase
finite contents, and discarding such additional contents is safe here.

## 2. Norms of these leading jets

D117 supplies an embedded orbifold disk of radius rho at every CM point
and every complex embedding, with rho^2=3/5. In its coarse coordinate
u=z^2, and with ||du||=1, the coefficient functional a_n on E has norm
at most sqrt(n+1)/(sqrt(pi)*rho^(2n+2)). The coefficient of a product
is the sum of tensor products of these functionals. Therefore, as
functionals on A, the first three product coefficients have bounds

    beta_0=1/(pi*rho^4),
    beta_1=2sqrt(2)/(pi*rho^6),
    beta_2=(2sqrt(3)+2)/(pi*rho^8).                            (3)

If q is in M_n, choose a lift in A of minimal norm. Its product is
q, so the same bound beta_n holds for its leading jet in the quotient
metric on M_n/M_(n+1). The lower-jet conditions introduce no denominator
in this argument.

For an injective integral determinant map V->L, the arithmetic degree
identity is deg(V)=deg(L)-finite_content+average log(norm of map).
Hadamard and (3) consequently give

    deg(M_n/M_(n+1)) <= k_n((n+2)H+log(beta_n)).

Add these exact filtered determinant degrees, substitute H<=Hplus,
and maximize over (2). The worst ranks are 17,15,13, giving

    deg(M) <= D_M
      :=131Hplus+17log(beta_0)+15log(beta_1)+13log(beta_2).     (4)

This controls the ordinary multiplication quotient directly. It uses
neither a Mumford isometry nor a choice of orbifold n=2 zero modes.

## 3. An integral forward map into the rational coordinates

Retain D103/D116's cofactor construction

    S=(tensor_i W_i)(det E)^(-1),       deg(S)=17H-F,
    Phi:E -> S tensor ker(sum:O^17->O),
    Phi(omega)_i=c_i e_i(omega),

where e_i is canonical evaluation and c_i the signed complementary
maximal minor. All these maps are integral. Unlike an inverse matrix,
Phi requires no division by a possibly small determinant.

Let b_0=1,b_1,...,b_16 be the saved integral order basis in the actual
degree-17 residue field L, eta_j=b_j-Tr(b_j)/17, and b_j^vee its trace
dual. D102 proves 32 b_j^vee is integral. For j>=1 it also has trace
zero, and

    Tr(b_j^vee eta_k)=delta_jk.

Define a map T:E->S tensor O^16 by

    T_j(omega)=sum_(i=0)^16 sigma_i(32 b_j^vee)c_i e_i(omega),
    j=1,...,16.                                              (5)

The coefficients sigma_i(32 b_j^vee) are algebraic integers, so (5)
is integral over the splitting field. This uses value vectors over
the base integers; it does not identify the actual horizontal order
with the abstract field order, which D119 shows would be wrong at 2.

The cofactor-weighted residue vector of the j-th rational canonical
section is a common scalar times (sigma_i(eta_j))_i. Trace duality
therefore says T is the coefficient map in the fixed rational residue
frame, multiplied by one common scalar. Its symmetric square sends
the actual J into the fixed coefficient relation space I_2 tensor S^2.
This establishes the coordinate comparison without assuming any of the
candidate equations is an actual relation.

## 4. Archimedean and finite exterior bounds for the forward map

Set B=1/(sqrt(pi)*rho^2). Every evaluation row has norm at most B.
Cauchy--Binet and the arithmetic-geometric mean inequality give

    sum_i |c_i|^2=det(Evaluation^* Evaluation)
       <= (17/16)^16 B^32.

Hence ||Phi||_HS<=(17/16)^8 B^17, since its squared Hilbert--Schmidt
norm is sum_i |c_i|^2 ||e_i||^2. For each j let D_j be an upper bound
for all |sigma(32 b_j^vee)|, and put D2=sum_(j=1)^16 D_j^2. The
coefficient matrix in (5) has Hilbert--Schmidt norm at most sqrt(17 D2),
so

    ||T||_HS <= N := sqrt(17 D2)(17/16)^8 B^17.               (6)

Here the bounds D_j are explicit rationals, not fitted condition
numbers. Rouché's inequality for the saved degree-17 polynomial puts
every root theta inside |theta|<4. If 32 b_j^vee=sum_k d_jk theta^k,
we may take D_j=sum_k |d_jk|4^k. Source 620 computes trace duals by
number-field traces. Source 621 independently constructs the power
trace matrix by Newton sums and solves the duality equations in that
basis. The common result is

    D2 = 1187318416985061838983337259276954121067476988424880
         / 133705314906850236656538604798081.

For singular values s_i of T, the squared Hilbert--Schmidt norm of
Sym^2 T in quotient symmetric metrics is

    sum_(i<=j) s_i^2 s_j^2
      =((sum_i s_i^2)^2+sum_i s_i^4)/2 <= N^4.

With r=91, the product of its largest r singular values is at most
(N^4/r)^(r/2). Changing the target from quotient symmetric norm to
the ordinary coefficient Euclidean norm costs at most sqrt(2) in each
direction. Therefore the log-volume on the actual J is at most

    L_ext=182log(N)-(91/2)log(91)+(91/2)log(2).                (7)

At the dyadic place, D116 proves that the evaluation cofactors, in the
actual integral E and W_i lattices, have valuations [280,245,...,245]
with v_beta(2)=16. Every row of Phi, and hence every row of T, is
divisible by beta^245. Sym^2 T is divisible by beta^490. Its image of
J lies in beta^490 times the saturated coefficient-relation lattice:
intersecting a rational subspace with the ambient integral lattice
commutes with multiplication by a scalar. Its rank-91 image index
therefore contributes at least

    J_2=(490*91/16)log(2)=(22295/8)log(2).                    (8)

The construction is equivariant in the CM labels, up to common signs,
so the same bound applies at every dyadic prime after Galois extension.
The factor 16 in (8) is essential. This content is the index of the
**forward frame on J**, not D147's multiplication cokernel, which is
zero at 2. Additional finite contents are not assumed.

## 5. Combine before taking upper endpoints

Let t_T be the finite index of (Sym^2 T)(J) in the saturated coefficient
relation lattice tensor S^2. With its ordinary Euclidean coefficient
metric that target has degree 182deg(S)-h_ext(I_2). The determinant
comparison therefore gives

    h_ext(I_2)=182deg(S)-deg(J)+average log vol(T^2|J)-t_T.

Insert (1), (4), (7), (8), H<=Hplus and F>=Fminus. The coefficients
of H and F have the required signs, giving the rigorous bound

    U=182(17Hplus-Fminus)+D_M-17Fminus-60log(2)+L_ext-J_2.
                                                                  (9)

The saved inputs are

    Hplus=2h_L^+-(35/34)log(2),
    h_L^+=31172134711534863111/18446744073709551616,
    Fminus=-16log(pi)+(-8+55817/54150)log(2).

As an independent arithmetic check, collect (9) as

    U=3225Hplus-199Fminus-1592log(pi)+3225log(5/3)
      +1547log(17)+91log(D2)-(68719/8)log(2)
      +13log(sqrt(3)+1)-(91/2)log(91).                        (10)

Sources 620 and 621 use separate 192-bit and 224-bit Arb evaluations
of (9) and (10). Their outward intervals overlap and lie strictly
between 15236 and 15237. This proves the reported upper bound.

Combining with D147, the same calculation bounds the joint quantity
R-t_mu by U+4Fminus+(139/2)log(2)<15193. This collects the F coefficient
before substituting its lower bound. It does not separately evaluate
the Mumford norm, the frame distortion, or the unknown odd-prime index.

## 6. What the estimate rules out, and the next task

The only appearance of the root-based field-vector majorants in (10)
is the positive term 91log(D2). Deleting it gives

    U-91log(D2)=11266.237580094368... >11266.                  (11)

Moreover the actual total squared norm of the matrix of the conjugates
of the sixteen nonzero algebraic integers 32 b_j^vee is at least 16*17:
the norm of each such integer is a nonzero integer, and AM-GM applies
to its seventeen squared absolute values. Thus field-vector norm
refinement cannot supply an arbitrarily negative substitute for the
term removed in (11). Treating that term as zero is already favorable
for diagnosing the limitation of this method.

This closes the proposal to reach 623 by merely refining the polynomial
root radius or the trace-dual vector norms inside this majorant. It does
not close all determinant methods, disprove the target, identify the
candidate, or establish a need for higher moment precision.

The large loss is the full rank-91 exterior comparison of the forward
cofactor frame. The next theoretical task is to assess a relation-specific
exterior estimate, or a direct arithmetic comparison using the primitive
principal-parts pencil, that avoids paying this full ambient frame bound.
Any proposed cancellation must hold for the unknown actual relation
space and retain the horizontal order and global normalization from
D119. A determinant-only claim or a candidate-only estimate is
insufficient. Exact structural identification remains an alternative.

P1600 and column 0/P6400 remain unchanged. The spectral, new-level,
Hecke and cubic pauses persist. No new arithmetic bank or search is
admitted. The later markings, cover character, cubic/section data and
field polynomial remain open. No new decision is needed for this
continuing theoretical assessment.

## 7. Reproducibility

Sources 620 and 621 contain the primary and independent arithmetic
calculations. The latter also checks 83 exterior-norm cases and four
integer minor-content controls. Its first attempt stopped on a Sage
two-argument rational-constructor call in a control; the source, log
and receipt are archived. Replacing it by exact rational division
fixes that API error. The dual-field and collected-height checks had
already passed, and the successful audit repeats them unchanged.

Source 622 provides the fixed review, transitive replay, source ledger
and completion record. Five bounded jobs pass, with that one archived
audit failure. The seven entry documents point to D148. Sources
620--622 and passing artifacts are frozen; source 623 is next unused.
All jobs use the existing 180-second private-process-group wrapper,
maximum three mathematical workers, 2 GiB per worker/store and 6 GiB
aggregate. Finite controls do not mechanically verify the geometric
filtration, duality or Arakelov arguments supplied above.
