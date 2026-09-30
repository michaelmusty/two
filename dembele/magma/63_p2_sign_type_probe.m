// Probe the integral sign type of GL2(F2)=S3 on the level-one class set.
// The rank-one sign lattice reduces to the trivial type mod 2. Its global
// lattice injects into level-one functions after reduction, but only on
// classes whose unit stabilizer has even image in S3. This tests that image
// and its inclusion of the original two residual constituents, in one basis.
SetColumns(0);
SetQuitOnError(true);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F); p2 := Factorization(2*OF)[1][1];
k, red := ResidueClassField(p2); assert #k eq 2;
M := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
t0 := Cputime();
raw := InternalHMFRawDataDefinite(M : Verbose:=false);
rids := raw`RightIdealClassReps;
printf "R63|level-one ideal classes %o [%o s]\n", #rids, Cputime(t0);
allowed := []; forbidden := [];
for i in [1..#rids] do
    LO := LeftOrder(rids[i]);
    mats, split := ResidueMatrixRing(LO, p2);
    U, mU := UnitGroup(LO);
    even := true;
    for u in Generators(U) do
        A := Matrix(k, 2, [ red(OF!v) : v in Eltseq(split(mU(u))) ]);
        assert Determinant(A) eq 1;
        // The only odd permutations in GL2(F2) are nonidentity involutions.
        if A ne IdentityMatrix(k,2) and A^2 eq IdentityMatrix(k,2) then
            even := false; break;
        end if;
    end for;
    if even then Append(~allowed, i); else Append(~forbidden, i); end if;
end for;
printf "R63|sign-admissible classes %o; forbidden %o; forbidden indices %o [%o s]\n", #allowed, #forbidden, forbidden, Cputime(t0);
g31 := F![1,2,0,-4,0,1,0,0]; p31 := ideal<OF | OF!g31>;
// The package acts on ROW functions: see definite.m, assembly T[i,j]
// from the neighbors of class j, and its invariant pairing T*IP=IP*T^t.
// Only the forbidden columns are needed to test stability and compute the
// quotient. A coprime quotient polynomial forces each target constituent
// into the supported submodule; no full T31 rebuild is necessary.
T := Matrix(InternalHMFRawHeckeDefiniteSparse(M, p31 : Columns:=forbidden));
Tb := ChangeRing(T,k);
P<t> := PolynomialRing(k);
f1 := t^8+t^4+t^3+t+1;
f2 := t^8+t^6+t^5+t^2+1;
rowstable := &and[ Tb[i,j] eq 0 : i in allowed, j in forbidden ];
printf "R63|supported row subspace stable under T31: %o\n", rowstable;
assert rowstable;
Tquot := Matrix(k,#forbidden,#forbidden,[Tb[i,j] : i,j in forbidden]);
qcp := CharacteristicPolynomial(Tquot);
printf "R63|T31 on the 10-dimensional quotient: %o\n", qcp;
for f in [f1,f2] do
    coprime := GCD(qcp,f) eq 1;
    printf "R63|factor %o: coprime to quotient %o; hence its generalized eigenspace is supported\n", f,coprime;
    assert coprime;
end for;
Zz<z> := PolynomialRing(Integers());
bank := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
assert #allowed eq 48;
// bank[1] is the raw level-one polynomial, including its Eisenstein factor.
supportedcp := ExactQuotient(P!bank[1], qcp);
assert supportedcp eq P!bank[3];
printf "R63|supported T31 charpoly (raw level-one bank divided by quotient) equals degree-48 p2-new charpoly mod 2: true [%o s]\n", Cputime(t0);
print "PASS|63_p2_sign_type_probe";
quit;
