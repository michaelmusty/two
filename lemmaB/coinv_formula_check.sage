# Check the structural formula
#   dim H_1(X,F_2)_G = 2 + d(M(G)) - rank_{F_2}( image of the 3 puncture classes in Rel_G )
# where Rel_G = (N/[F,N]) (x) F_2 and M(G) = H_2(G,Z) (Schur multiplier), d = 2-rank.
# We only test the consequence that is directly computable from the module:
#   dim M_G  >=  d(M(G)) - 1,   and   dim M_G <= 2 + d(M(G)).
# and record dim M_G, dim M^G for every 2-generated Belyi triple with |G| <= 32.
load("torsion_module.sage")
def coinv_dim(twog, Ms):
    I = identity_matrix(F2, twog)
    S = block_matrix([[ (M - I) for M in Ms ]], subdivide=False)
    return twog - S.rank()
def inv_dim(twog, Ms):
    I = identity_matrix(F2, twog)
    S = block_matrix([[ (M - I).transpose() for M in Ms ]], subdivide=False)
    return twog - S.rank()
import itertools
for order in [2,4,8,16,32]:
    for i in range(1, libgap.NrSmallGroups(order)+1):
        G = libgap.SmallGroup(order, i)
        if int(libgap.Size(libgap.GeneratorsOfGroup(G))) > 2 and int(libgap.RankPGroup(G)) > 2: continue
        if int(libgap.RankPGroup(G)) > 2: continue
        mult = [int(m) for m in libgap.AbelianInvariantsMultiplier(G)]
        dM = len(mult)
        elts = list(libgap.Elements(G))
        seen = set(); results = {}
        for s0 in elts:
            for s1 in elts:
                if libgap.Size(libgap.Group(s0, s1)) != order: continue
                # dedupe up to Aut(G)-images crudely: use orders signature + module dims
                genus, twog, Ms, matfn = analyze(G, s0, s1, verbose=False)
                if genus == 0: continue
                key = (int(libgap.Order(s0)), int(libgap.Order(s1)), int(libgap.Order((s0*s1)**-1)), genus)
                if key in seen: continue
                seen.add(key)
                ci = coinv_dim(twog, Ms); iv = inv_dim(twog, Ms)
                ok = (dM - 1 <= ci <= 2 + dM) and ci == iv
                results[key] = (ci, iv, ok)
        if results:
            summ = sorted(set(v[0] for v in results.values()))
            allok = all(v[2] for v in results.values())
            print(f"[{order},{i}] d(M(G))={dM} ({mult}); dim M_G values {summ}; bounds+selfdual ok={allok}")
