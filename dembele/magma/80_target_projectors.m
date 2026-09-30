// Exact Hecke projector algebra for the specified genus-64 carrier.
// This computes polynomials in the geometric T31 correspondence, not a
// matrix of that correspondence on a computed Jacobian. See the certificate.
SetColumns(0);
SetQuitOnError(true);
Z<z> := PolynomialRing(Integers());
P<t> := PolynomialRing(GF(2));
bank := eval Read("dembele/data/computed/levelraise_p2k_charpolys.m");
cp40 := Z!bank[2]; cp48 := Z!bank[3];
assert Degree(cp48) eq 48 and IsIrreducible(cp48);
quartics := [a[1] : a in Factorization(cp40) | Degree(a[1]) eq 4];
assert #quartics eq 4;
cp16 := &*quartics;
cp64 := cp16*cp48;
assert Degree(cp64) eq 64 and GCD(cp64,Derivative(cp64)) eq 1;
h := [t^8+t^4+t^3+t+1, t^8+t^6+t^5+t^2+1];
p := P!cp64;
assert P!cp48 eq t^32*h[1]*h[2];
assert GCD(P!cp16,h[1]*h[2]) eq 1;
e := [];
for i in [1..2] do
    assert IsIrreducible(h[i]);
    q := ExactQuotient(p,h[i]);
    d,a,b := XGCD(q,h[i]);
    assert d eq 1;
    ei := (a*q) mod p;
    assert (ei^2-ei) mod p eq 0;
    assert ei mod h[i] eq 1 and ei mod q eq 0;
    assert (h[i]*ei) mod p eq 0;
    Append(~e,ei);
end for;
assert (e[1]*e[2]) mod p eq 0;
// A companion-model check illustrates the rank forced by the predicted
// characteristic polynomial cp64^2 and its squarefree target factors.
// This is explicitly NOT the actual geometric H1 matrix.
C := CompanionMatrix(p);
E := [Evaluate(ei,C) : ei in e];
assert [Rank(Ei) : Ei in E] eq [8,8];
assert &and[ Ei^2 eq Ei : Ei in E ];
assert E[1]*E[2] eq 0;
assert Rank(E[1]+E[2]) eq 16;
out := "dembele/data/computed/target_projectors.json";
txt := Sprintf("{\n  \"schema\": 1,\n  \"hecke_prime_norm\": 31,\n  \"cp64_mod2\": %o,\n  \"target_factors\": %o,\n  \"projectors\": %o,\n  \"companion_model_ranks\": [8,8],\n  \"predicted_geometric_torsion_ranks\": [16,16],\n  \"geometric_matrix_computed\": false\n}\n",
    [Integers()!Coefficient(p,j) : j in [0..64]],
    [[Integers()!Coefficient(hi,j) : j in [0..8]] : hi in h],
    [[Integers()!Coefficient(ei,j) : j in [0..63]] : ei in e]);
Write(out,txt : Overwrite:=true);
printf "R80|cp48 mod 2 = t^32*h1*h2; both factors simple and disjoint from old part\n";
for i in [1..2] do
    printf "R80|projector %o = %o\n",i,e[i];
end for;
print "R80|CRT identities pass; companion-model ranks 8+8; geometric Tate ranks predicted 16+16";
print "PASS|80_target_projectors";
quit;
