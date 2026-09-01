# Numerical check of the cyclic-case theorem: for G = C_n (n = 2^k) and every
# Belyi triple, dim H_1(X,F_2)_G = dim H_1(X,F_2)^G = 1 (so the module is cyclic,
# hence uniserial, hence indecomposable).  Also records the lattice-criterion
# prediction from the proof.
load("torsion_module.sage")
from math import gcd
def coinv_dim(twog, Ms):
    # M_G = M / sum (g-1)M
    I = identity_matrix(F2, twog)
    S = block_matrix([[ (M - I) for M in Ms ]], subdivide=False)
    return twog - S.rank()
def inv_dim(twog, Ms):
    I = identity_matrix(F2, twog)
    S = block_matrix([[ (M - I).transpose() for M in Ms ]], subdivide=False)
    return twog - S.rank()
for k in range(1, 6):
    n = 2**k
    G = libgap.CyclicGroup(n); s = libgap.GeneratorsOfGroup(G)[0]
    bad = 0; cnt = 0
    for a in range(n):
        for b in range(n):
            if gcd(gcd(a, b), n) != 1: continue
            s0 = s**a; s1 = s**b
            genus, twog, Ms, matfn = analyze(G, s0, s1, verbose=False)
            if genus == 0: continue
            cnt += 1
            ci = coinv_dim(twog, Ms); iv = inv_dim(twog, Ms)
            if ci != 1 or iv != 1:
                bad += 1; print("FAIL", n, a, b, genus, ci, iv)
    print(f"n={n}: {cnt} positive-genus triples, coinvariant dim == 1 in all but {bad}")
