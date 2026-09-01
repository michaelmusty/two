// Tate pilot, phase 1 (stocktake-2026-09-01.md; tate-pilot-plan.md): the
// lattice-level data for the five rational new eigenforms at level p31 —
// elliptic curves over F with multiplicative reduction at the norm-31 prime.
//
// For each rational T_97-eigenvalue a on the new part:
//   - the (rank-1) saturated character-lattice vector v in the banked Brandt
//     basis (kernel of T_97 - a, integrally saturated);
//   - ord_{p31}(q_E) = <v, v> under the stabilizer-order monodromy pairing
//     (D31) — the valuation of the Tate parameter, i.e. -v(j_E);
//   - the U_31 eigenvalue (+-1: split/non-split multiplicative reduction);
//   - the T_127 eigenvalue (identification data).
//
// Needs on chatelet: dp31_T97.m, dp31_T127.m, dp31_W.m (banked, one session,
// D31-validated), and a fresh U_31 build IN THE SAME BASIS -- impossible
// across sessions (D26b), so U_31 is instead applied via its action on the
// eigenVECTOR: U_31 commutes with T_97, preserves the 1-dim eigenspace, and
// the eigenvalue is read off from any nonzero coordinate of v*U.  A fresh
// U_31 build in THIS session's basis cannot be paired with the banked v...
// therefore U_31 must be built in the banked basis.  Since that basis is dead,
// we instead rebuild T_97 AND U_31 together in THIS session, re-derive the
// eigenvectors here, and verify the T_97 charpoly matches the banked one
// (basis-independent).  The banked dp31 operators are used only for the
// charpoly cross-check.
//
// Env: HMF_ROOT, G3_MEMCAP.
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
Zz<z> := PolynomialRing(Integers());
g31e := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31e>;
p97 := [ p[1] : p in Factorization(97*OF) | Norm(p[1]) eq 97 ][1];
p127 := [ p[1] : p in Factorization(127*OF) | Norm(p[1]) eq 127 ][1];

M := HilbertCuspForms(F, p31, [2 : i in [1..8]]);
stabs, ulcm, g := InternalHMFRawStabOrdersDefinite(M);
printf "TP|level norm 31: stab orders distinct %o, ulcm %o, g %o\n",
    Seqset(stabs), ulcm, g;
t0 := Cputime();
T97 := InternalHMFRawHeckeDefiniteSparse(M, p97);
printf "TP|T_97 built [%o s]\n", Cputime(t0);
t0 := Cputime();
T127 := InternalHMFRawHeckeDefiniteSparse(M, p127);
printf "TP|T_127 built [%o s]\n", Cputime(t0);
t0 := Cputime();
U31 := InternalHMFRawHeckeDefiniteSparse(M, p31);
printf "TP|U_31 built [%o s]\n", Cputime(t0);
N := Ncols(T97);

// cross-check against the banked session: charpoly is basis-independent
function loadBank(path)
    txt := Read(path);
    i0 := Index(txt, ":=");
    j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
    return eval txt[i0+2..j0-1];
end function;
T97d := ChangeRing(Matrix(T97), Rationals());
cpnew := Zz!CharacteristicPolynomial(T97d);
cpbanked := Zz!CharacteristicPolynomial(ChangeRing(Matrix(loadBank("dp31_T97.m")), Rationals()));
printf "TP|CHECK T_97 charpoly matches banked session: %o\n", cpnew eq cpbanked;

// self-adjointness of all three under the stab pairing (U_31 included: the
// Iwahori pairing makes U self-adjoint iff ... -- report, do not assume)
procedure sacheck(S, name, stabs)
    bad := 0;
    for t in Support(S) do
        i := t[1]; j := t[2];
        if stabs[i]*S[i,j] ne S[j,i]*stabs[j] then bad +:= 1; end if;
    end for;
    printf "TP|CHECK %o self-adjoint under stab pairing: %o bad of %o\n",
        name, bad, #Support(S);
end procedure;
sacheck(T97, "T_97", stabs);
sacheck(T127, "T_127", stabs);
sacheck(U31, "U_31", stabs);

U31d := ChangeRing(Matrix(U31), Rationals());
T127d := ChangeRing(Matrix(T127), Rationals());
VN := VectorSpace(Rationals(), N);
for a in [14, 6, 2, -6, -14] do
    Ka := Kernel(T97d - a);
    printf "TP|=== a_97 = %o: eigenspace dim %o\n", a, Dimension(Ka);
    error if Dimension(Ka) ne 1, "rational eigenvalue not multiplicity one";
    v0 := Basis(Ka)[1];
    den := LCM([ Denominator(e) : e in Eltseq(v0) ]);
    vz := Vector(Integers(), Eltseq(den*v0));
    gg := GCD(Eltseq(vz));
    vz := Vector(Integers(), [ e div gg : e in Eltseq(vz) ]);   // saturated generator
    v := VN!Vector(Eltseq(vz));
    // eigenvalues of U_31 and T_127 on v
    uv := v*U31d;
    i0 := Min(Support(v));
    ueig := uv[i0]/v[i0];
    printf "TP|  U_31 eigenvalue: %o (consistent: %o)\n", ueig, uv eq ueig*v;
    tv := v*T127d;
    teig := tv[i0]/v[i0];
    printf "TP|  T_127 eigenvalue: %o (consistent: %o)\n", teig, tv eq teig*v;
    // monodromy self-pairing = ord_{p31}(q_E)
    ordq := &+[ stabs[i]*(Integers()!v[i])^2 : i in [1..N] ];
    printf "TP|  ord(q_E) = <v,v>_stab = %o ; support size %o ; max |v_i| %o\n",
        ordq, #Support(v), Max([Abs(Integers()!e) : e in Eltseq(v)]);
    Write(Sprintf("tate_v_a%o.m", a),
          Sprintf("va%o := %m;\n", a, vz) : Overwrite := true);
end for;
// bank this session's operators: the pilot's later phases must act in THIS basis
Write("tate_T97.m", Sprintf("T97 := %m;", T97) : Overwrite := true);
Write("tate_U31.m", Sprintf("U31 := %m;", U31) : Overwrite := true);
Write("tate_stabs.m", Sprintf("stabs := %m;", [Integers()!e : e in stabs]) : Overwrite := true);
printf "TP|banked: tate_T97.m, tate_U31.m, tate_stabs.m, tate_v_a*.m (one basis)\n";
printf "TP|done\n";
quit;
