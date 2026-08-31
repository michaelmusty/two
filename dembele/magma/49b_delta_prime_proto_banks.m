// Delta' prototype, mechanics-only rerun from the banked level-31 operators
// (dp31_T97.m, dp31_T127.m, dp31_W.m — one session, one basis, D31 pairing).
//
// The 49 run validated the pairing (self-adjointness with the stab-order W)
// but stalled evaluating a degree-684 rational kernel for its surrogate g.
// New\perp old follows FORMALLY from self-adjointness + distinct eigenvalues,
// so what remains to validate is the lattice/Gram mechanics that 53 uses:
// saturation, Gamma = B W B^t integral and positive definite, det,
// elementary divisors, and the quotient-lattice index.  A rank-5 synthetic
// L — the saturated joint span of the five RATIONAL new eigenforms — tests
// exactly that in minutes.
//
// Env: G3_MEMCAP; banks are read from the working directory.
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
Zz<z> := PolynomialRing(Integers());

function loadBank(path)
    txt := Read(path);
    i0 := Index(txt, ":=");
    j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
    return eval txt[i0+2..j0-1];
end function;

S97 := loadBank("dp31_T97.m");
S127 := loadBank("dp31_T127.m");
W := loadBank("dp31_W.m");
N := Ncols(S97);
printf "PB|banks loaded: N = %o, W distinct %o\n", N, Seqset(W);

T := ChangeRing(Matrix(S97), Rationals());
T127 := ChangeRing(Matrix(S127), Rationals());
Wd := DiagonalMatrix(Rationals(), W);
printf "PB|CHECK T_97 self-adjoint: %o ; T_127 self-adjoint: %o ; commute: %o\n",
    (Wd*T) eq (Transpose(T)*Wd), (Wd*T127) eq (Transpose(T127)*Wd),
    T*T127 eq T127*T;

// cuspidal charpoly and the rational new eigenvalues
cp := Zz!CharacteristicPolynomial(T);
mult := 0; cc := cp;
while true do qq, r := Quotrem(cc, z-98); if r ne 0 then break; end if; mult +:= 1; cc := qq; end while;
printf "PB|Eisenstein mult %o; cuspidal degree %o\n", mult, Degree(cc);
cp1 := Zz!CharacteristicPolynomial(ChangeRing(Matrix(loadBank("l1_T97.m")), Rationals()));
facs := Factorization(cc);
newlin := [ t[1] : t in facs | Degree(t[1]) eq 1 and not IsDivisibleBy(cp1, t[1]) ];
printf "PB|rational new eigenvalues: %o\n", [ -Coefficient(h,0) : h in newlin ];

// L = saturated joint span of their eigenvectors (synthetic rank-#newlin lattice)
VN := VectorSpace(Rationals(), N);
rows := [ VN | ];
for h in newlin do
    Kh := Kernel(Evaluate(h, T));
    error if Dimension(Kh) ne 1, "rational new eigenvalue with multiplicity != 1";
    v := Basis(Kh)[1];
    den := LCM([ Denominator(e) : e in Eltseq(v) ]);
    Append(~rows, VN!Vector(Eltseq(den*v)));
end for;
B := Matrix(rows);
Bsat := Saturation(Matrix(Integers(), B));
printf "PB|L rank %o, saturated\n", Nrows(Bsat);
BQ := ChangeRing(Bsat, Rationals());
Gsub := BQ * Wd * Transpose(BQ);
Gz := Matrix(Integers(), Gsub);
printf "PB|CHECK Gamma integral %o, symmetric %o, positive definite %o\n",
    Gsub eq ChangeRing(Gz, Rationals()), IsSymmetric(Gz), IsPositiveDefinite(Gz);
dsub := Determinant(Gz);
printf "PB|det Gamma_sub = %o = %o\n", dsub, Factorization(dsub);
printf "PB|elementary divisors: %o\n", ElementaryDivisors(Gz);

// quotient lattice: rows of Wd * B^t * Gamma^{-1} over Z^N, in B-coordinates
Mq := Wd * Transpose(BQ) * Gsub^-1;      // N x r
lq := LCM([ Denominator(e) : e in Eltseq(Mq) ] cat [1]);
MqZ := Matrix(Integers(), lq*Mq);
H := HermiteForm(MqZ);
r := Nrows(Bsat);
detH := &*[ H[i,i] : i in [1..r] ];
idx := lq^r / detH;
printf "PB|quotient/sub index = %o ; det Gamma_quot = %o\n", idx, dsub/idx^2;
printf "PB|done\n";
quit;
