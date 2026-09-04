# Direct check of the quaternion decomposition from the Belyi model (torsion_module.analyze):
# MeatAxe decomposition + commutant/Wedderburn blocks + per-summand invariants. usage: sage lemmaB/quaternion_check.sage
import sys
_argv=sys.argv[:]; sys.argv=[sys.argv[0]]; load("torsion_module.sage"); sys.argv=_argv
_Indec = libgap.eval("MTX.Indecomposition"); _Iso = libgap.eval("MTX.IsomorphismModules"); _fail = libgap.eval("fail")
Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
for (n, m) in [(16, None), (32, None), (64, None), (8, None)]:
    Q = libgap.QuaternionGroup(n); ident = libgap.IdGroup(Q)
    G = libgap.SmallGroup(ident[0], ident[1])
    print(f"Q_{n} = SmallGroup{ident}")
    for h in libgap.GQuotients(Fr, G):
        s0 = libgap.Image(h, fg[0]); s1 = libgap.Image(h, fg[1])
        genus, dim, Ms, _ = analyze(G, s0, s1, verbose=False)
        if genus == 0: continue
        gm = libgap.GModuleByMats(libgap([libgap(M) for M in Ms]), libgap.GF(2))
        parts = _Indec(gm)
        dims = [int(parts[i][1]["dimension"]) for i in range(len(parts))]
        iso = (len(parts) == 2 and _Iso(parts[0][1], parts[1][1]) != _fail)
        solvC, blocks, dimA = centralizer_solvable(dim, Ms)
        # invariants/coinvariants of each summand
        sub = []
        for i in range(len(parts)):
            sm = parts[i][1]; gens = sm["generators"]
            d = int(sm["dimension"]); I = identity_matrix(F2, d)
            mats = [Matrix(F2, g) for g in gens]
            inv = d - block_matrix([[ (A - I) for A in mats ]], subdivide=False).rank()
            coinv = d - block_matrix([[ (A - I).transpose() for A in mats ]], subdivide=False).rank()
            sub.append((d, inv, coinv))
        e = (int(libgap.Order(s0)), int(libgap.Order(s1)), int(libgap.Order((s0*s1)**-1)))
        print(f"  orders {e} genus {genus} dim {dim}: #summands {len(parts)} dims {dims} iso_summands={iso} "
              f"End/rad blocks {blocks} dimEnd {dimA}; summand (dim, dim inv, dim coinv) = {sub}")
