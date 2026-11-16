// D166 step 4.4: the cube (rank-one cubic tensor) system for the third, mod p.
// On X: the third is the class of E_R - D0, with 3(E_R - D0) = Dminus - Dplus
// and u in L(4*D0) of divisor 3*E_R + B - 4*D0 (B = Dplus + Q, script 05).
// For S = 79 auxiliary points, L(E_R - S) is 2-dimensional (beta1, beta2), and
// c_ijk = beta_i*beta_j*beta_k*u lie in U = L(4*D0 - 3*S - B) (84-dim) and
// satisfy the twisted-cubic relations. Unknowns 4*84 = 336, gauge GL_2 (4).
// Rank 332 of the linearized relations means the third is an isolated
// solution and can be Hensel-lifted by a small system on X.
// Files: state_in.m, cubic_in.m, state_lib.m, makdisi_lib.m, exact data.
SetQuitOnError(true); SetColumns(0); SetSeed(113);
started := Cputime();
load "state_in.m";
load "state_lib.m";
load "makdisi_lib.m";
load "cubic_in.m";
Fp := GF(p); k := Fp;
load "cm_frame_curve_candidate.m";
load "cm_frame_marks.m";
load "cm_frame_B3_rational_model.m";
load "cm_frame_B3_fiber.m";
G1 := V1; G2 := V2; G3 := V3;
G4 := Matrix(k4, [[G1[pr[1],r]*G3[pr[2],r] : r in [1..NEV]] : pr in cub_pairs4]);
assert Rank(G4) eq 441;
qv := Vector(k4, cub_q_coefficients)*G1;
u := Vector(k4, cub_u_coefficients)*G4;
WRc := Matrix(k4, cub_WR_coordinates); WR := WRc*G2;
// L(2*D0 - B) as in script 05
UA<a> := PolynomialRing(k4);
A<aa> := quo<UA | UA![Fp!c : c in fiber_nonic_coefficients]>;
plus1 := [A!UA![DecE(c) : c in row] : row in st_branch_plus];
plus2 := [plus1[pr[1]]*plus1[pr[2]] : pr in st_pairs2];
bp2 := Matrix(k4, [[Coefficient(UA!v, j) : j in [0..8]] : v in plus2]);
bm1 := Matrix(k4, [[DecE(c) : c in row] : row in st_branch_minus]);
qker := Matrix(Basis(Nullspace(bm1)));
Sminus := qker*G1;
WQ := QuotientSpace(Sminus, ScaleRows(G2, qv), G2, 90);
Qcoeff := Solution(G2, WQ);
bker := Matrix(Basis(Nullspace(Qcoeff*bp2))); assert Nrows(bker) eq 81;
WB := bker*WQ;
WB4 := ProductSpace(WB, G2, 321);
printf "S13|L(4*D0 - B): 321 [%o s]\n", Cputime(started);
// auxiliary points S: 79 points outside the evaluation set
unused := [i : i in [1..nn] | not i in evals];
r0 := 0; rc := 0;
repeat
    lam := Vector(k4, [k4!Random(Fp) : i in [1..81]]);
    rc := lam*WRc;
    Ssel := [];
    for i in unused do
        if (rc, V2all[i]) ne 0 then Append(~Ssel, i); end if;
        if #Ssel eq 79 then break; end if;
    end for;
until #Ssel eq 79;
rvec := rc*G2;
assert &and[c ne 0 : c in Eltseq(rvec)];
VS := Matrix(k4, [Eltseq(V2all[i]) : i in Ssel]);       // 79 x 201: L(2*D0) at S
T0 := QuotientSpace(WR, ScaleRows(G2, rvec), G2, 81);   // L(2*D0 - R')
Tc0 := Solution(G2, T0);
bc := Matrix(Basis(Nullspace(Tc0*Transpose(VS))))*Tc0;
printf "S13|L(E_R - S): dimension %o (expected 2)\n", Nrows(bc);
assert Nrows(bc) eq 2;
beta := [Vector(k4, [(bc[i]*G2)[r]/rvec[r] : r in [1..NEV]]) : i in [1..2]];
L2S := Matrix(Basis(Nullspace(Transpose(VS))))*G2;      // L(2*D0 - S)
assert Nrows(L2S) eq 201 - 79;
L4S := ProductSpace(L2S, L2S, 283);
L6S := ProductSpace(L4S, L2S, 444);
printf "S13|L(6*D0 - 3*S): 444 [%o s]\n", Cputime(started);
U1 := QuotientSpace(G2, L6S, G4, 204);                   // L(4*D0 - 3*S)
U := Matrix(Basis(RowSpace(U1) meet RowSpace(WB4)));
printf "S13|U = L(4*D0 - 3*S - B): dimension %o (expected 84) [%o s]\n", Nrows(U), Cputime(started);
assert Nrows(U) eq 84;
idx := [[1,1,1],[1,1,2],[1,2,2],[2,2,2]];
c := [Vector(k4, [beta[t[1]][r]*beta[t[2]][r]*beta[t[3]][r]*u[r] : r in [1..NEV]]) : t in idx];
inU := &and[IsConsistent(U, v) : v in c];
printf "S13|the four c_ijk lie in U: %o\n", inU;
assert inU;
minors := [[1,3,2,2],[2,4,3,3],[1,4,2,3]];
assert &and[IsZero(Vector(k4, [c[m[1]][r]*c[m[2]][r] - c[m[3]][r]*c[m[4]][r] : r in [1..NEV]])) : m in minors];
rows := [];
for a in [1..4] do
    for e in [1..84] do
        row := [];
        for m in minors do
            co := Vector(k4, NEV, [0 : r in [1..NEV]]);
            if m[1] eq a then co +:= Vector(k4, [U[e,r]*c[m[2]][r] : r in [1..NEV]]); end if;
            if m[2] eq a then co +:= Vector(k4, [U[e,r]*c[m[1]][r] : r in [1..NEV]]); end if;
            if m[3] eq a then co -:= Vector(k4, [U[e,r]*c[m[4]][r] : r in [1..NEV]]); end if;
            if m[4] eq a then co -:= Vector(k4, [U[e,r]*c[m[3]][r] : r in [1..NEV]]); end if;
            row cat:= Eltseq(co);
        end for;
        Append(~rows, row);
    end for;
end for;
Jm := Matrix(k4, rows); rk := Rank(Jm);
printf "S13|linearized cube relations: %o unknowns, rank %o, kernel %o (gauge 4) [%o s]\n", Nrows(Jm), rk, Nrows(Jm) - rk, Cputime(started);
print "DONE|13_CUBE_SYSTEM";
quit;
