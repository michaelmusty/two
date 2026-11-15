// D158 step 2c: Kummer function and genus-64 cubic mod p (port of script 176).
// Files in the current directory: state_in.m (from script 03), third_in.m
// (from script 04, or an alternative third), the exact data files, the libs.
// Env: OUT (result file). The cubic is Q4*T^3 - 3*A4*Q4*T - P10 = 0 over C.
SetQuitOnError(true); SetColumns(0); SetSeed(79);
started := Cputime();
load "state_in.m";
load "state_lib.m";
load "makdisi_lib.m";
load "third_in.m";
Third := Dec(st_third);
assert NEV eq 1024;
Fp := GF(p);
function IsRat(c) return c^q eq c; end function;
function TauVec(v) return Vector(k4, [v[i] : i in etau]); end function;
function IndependentIndices(M)
    e := EchelonForm(Transpose(M)); out := [];
    for v in Rows(e) do
        if v ne 0 then Append(~out, Min([j : j in [1..Ncols(e)] | v[j] ne 0])); end if;
    end for;
    return out;
end function;
G1 := V1; G2 := V2; G3 := V3;
G4 := ZeroMatrix(k4, 0, NEV); pairs4 := [];
for i in [1..81] do
    np := [[i,j] : j in [1..321]];
    cand := ScaleRows(G3, G1[i]); both := VerticalJoin(G4, cand); pp := pairs4 cat np;
    ii := IndependentIndices(both); G4 := Matrix([both[j] : j in ii]); pairs4 := [pp[j] : j in ii];
    assert #pairs4 le 441;
    if #pairs4 eq 441 then break; end if;
end for;
assert Rank(G4) eq 441;
printf "S05|sections of 4*D0: rank 441 [%o s]\n", Cputime(started);

WE := Third; Wsigma := FrobeniusClass(WE);
WE3 := ProductSpace(WE, G1, 201);
UA<a> := PolynomialRing(k4);
A<aa> := quo<UA | UA![Fp!c : c in fiber_nonic_coefficients]>;
plus1 := [A!UA![DecE(c) : c in row] : row in st_branch_plus];
plus2 := [plus1[pr[1]]*plus1[pr[2]] : pr in st_pairs2];
bp2 := Matrix(k4, [[Coefficient(UA!v, j) : j in [0..8]] : v in plus2]);
bm1 := Matrix(k4, [[DecE(c) : c in row] : row in st_branch_minus]);
qker := Matrix(Basis(Nullspace(bm1))); assert Nrows(qker) eq 72;
assert &and[IsRat(c) : c in Eltseq(qker)];
Sminus := qker*G1;
qfound := false;
for trial in [1..16] do
    qcoeff := Vector(k4, [k4!Random(Fp) : i in [1..72]])*qker;
    qplus := &+[qcoeff[i]*plus1[i] : i in [1..81]];
    if not IsUnit(qplus) then continue; end if;
    qv := qcoeff*G1;
    WQ := QuotientSpace(Sminus, ScaleRows(G2, qv), G2, 90);
    Qcoeff := Solution(G2, WQ); assert Qcoeff*G2 eq WQ;
    bker := Matrix(Basis(Nullspace(Qcoeff*bp2))); assert Nrows(bker) eq 81;
    WB := bker*WQ;
    WB3 := ProductSpace(WB, G1, 201);
    if Rank(VerticalJoin(WE3, WB3)) ne 321 then continue; end if;
    qfound := true; break;
end for;
assert qfound;
assert RowSpace(FrobeniusClass(WB)) eq RowSpace(WB);
WB4 := ProductSpace(WB, G2, 321);
traceSpace := ProductSpace(WE, Wsigma, 201);
moving := Matrix(Basis(RowSpace(traceSpace) meet RowSpace(WB4)));
assert Nrows(moving) eq 81;
movingcoeff := Matrix(Basis(RowSpace(Solution(G4, moving))));
assert &and[IsRat(c) : c in Eltseq(movingcoeff)];
moving := movingcoeff*G4;
efound := false;
for trial in [1..16] do
    move_coeff := Vector(k4, [k4!Random(Fp) : i in [1..81]])*movingcoeff;
    move := move_coeff*G4;
    if move eq 0 then continue; end if;
    WR := QuotientSpace(moving, ScaleRows(G2, move), G2, 81);
    WR3 := ProductSpace(WR, G1, 201);
    if Rank(VerticalJoin(WR3, WB3)) ne 321 then continue; end if;
    efound := true; break;
end for;
assert efound;
assert RowSpace(FrobeniusClass(WR)) eq RowSpace(WR);
assert EqualClass(WR, Third);
WRcoords := Matrix(Basis(RowSpace(Solution(G2, WR))));
assert &and[IsRat(c) : c in Eltseq(WRcoords)];
WR := WRcoords*G2;
printf "S05|rational effective representative of the third [%o s]\n", Cputime(started);

// qv has divisor D- + Q - D0; B = D+ + Q. Recover u with divisor 3E + B - 4D0.
cubeSpace := ProductSpace(ProductSpace(WR, WR, 201), WR, 321);
tripleVanishing := QuotientSpace(G2, cubeSpace, G4, 81);
uline := Matrix(Basis(RowSpace(tripleVanishing) meet RowSpace(WB4)));
assert Nrows(uline) eq 1;
ucoeff := Solution(G4, uline[1]);
pivot := Min([j : j in [1..441] | ucoeff[j] ne 0]); ucoeff /:= ucoeff[pivot];
assert &and[IsRat(c) : c in Eltseq(ucoeff)];
u := ucoeff*G4;
normSpace := ProductSpace(WR, DeckClass(WR), 201);
ok, f := DegreeZeroQuotient(G2, normSpace, G2); assert ok;
fcoeff := Solution(G2, f);
pivot := Min([j : j in [1..201] | fcoeff[j] ne 0]); fcoeff /:= fcoeff[pivot];
assert &and[IsRat(c) : c in Eltseq(fcoeff)];
f := fcoeff*G2;
assert TauVec(f) eq f;
ut := TauVec(u); qt := TauVec(qv);
good := Min([j : j in [1..NEV] | f[j]*qv[j]*qt[j] ne 0]);
c := u[good]*ut[good]/(f[good]^3*qv[good]*qt[good]);
assert c ne 0 and IsRat(c);
assert &and[u[j]*ut[j] eq c*f[j]^3*qv[j]*qt[j] : j in [1..NEV]];
assert &or[u[j]*qt[j] - ut[j]*qv[j] ne 0 : j in [1..NEV]];
printf "S05|Kummer divisor and norm identity pass; norm scalar %o [%o s]\n", Fp!c, Cputime(started);

// Reflection quotient: y^3 - 3*a*y - btrace = 0, a = c*f, h = c*u/q.
k := Fp;
load "cm_frame_curve_candidate.m";
IC := Ideal(C_candidate); GC := GroebnerBasis(IC); LM := [LeadingMonomial(z) : z in GC];
FB := [R!1]; layer := [R!1]; depth := 0;
repeat
    depth +:= 1; assert depth le 40;
    layer := Setseq({m*R.i : m in layer, i in [1..14] | not &or[IsDivisibleBy(m*R.i, l) : l in LM]});
    FB cat:= layer;
until #layer eq 0;
Sort(~FB); assert #FB eq 30;
function CanonMons(deg, FB, R)
    return &cat[[m*R.15^j*R.16^(deg-TotalDegree(m)-j) : j in [0..deg-TotalDegree(m)]] : m in FB | TotalDegree(m) le deg];
end function;
base4 := CanonMons(4, FB, R); base10 := CanonMons(10, FB, R);
assert #base4 eq 105 and #base10 eq 285;
xs := [plist[i][1..16] : i in evals];
function MonRow(m)
    e := Exponents(m);
    return [&*[x[t]^e[t] : t in [1..16]] : x in xs];
end function;
C4 := Matrix(k4, [MonRow(m) : m in base4]);
C10 := Matrix(k4, [MonRow(m) : m in base10]);
assert Rank(C4) eq 105 and Rank(C10) eq 285;
avec := c*f;
denvec := Vector(k4, [qv[j]*qt[j] : j in [1..NEV]]);
numvec := Vector(k4, [c*(u[j]*qt[j] + ut[j]*qv[j]) : j in [1..NEV]]);
arow := Solution(C4, avec); denrow := Solution(C4, denvec); numrow := Solution(C10, numvec);
assert arow*C4 eq avec and denrow*C4 eq denvec and numrow*C10 eq numvec;
assert &and[IsRat(z) : z in Eltseq(arow) cat Eltseq(denrow) cat Eltseq(numrow)];
function FpSeq(v) return [Integers()!(Fp!z) : z in Eltseq(v)]; end function;
OUT := GetEnv("OUT");
PrintFile(OUT, Sprintf("cub_p := %o;\ncub_norm_scalar := %o;", p, Integers()!(Fp!c)) : Overwrite := true);
PrintFile(OUT, Sprintf("cub_quartic_monomials := %o;\ncub_decic_monomials := %o;", [Exponents(m) : m in base4], [Exponents(m) : m in base10]));
PrintFile(OUT, Sprintf("cub_A := %o;\ncub_den := %o;\ncub_num := %o;", FpSeq(arow), FpSeq(denrow), FpSeq(numrow)));
PrintFile(OUT, Sprintf("cub_pairs4 := %o;\ncub_q_coefficients := %o;\ncub_move_coefficients := %o;", pairs4, FpSeq(qcoeff), FpSeq(move_coeff)));
PrintFile(OUT, Sprintf("cub_u_coefficients := %o;\ncub_f_coefficients := %o;\ncub_WR_coordinates := %o;", FpSeq(ucoeff), FpSeq(fcoeff), [FpSeq(r) : r in Rows(WRcoords)]));
printf "S05|cubic coefficients written [%o s]\n", Cputime(started);
print "PASS|05_KUMMER";
quit;
