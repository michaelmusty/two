# Census of the coinvariant formula   dim H_1(X,F_2)_G = 2 + d(M(G)) - r
# (writeup/lemma-B-cyclic.md, Proposition) with r computed DIRECTLY:
#   r   = rank of the three puncture classes [x^{e0}], [y^{e1}], [(xy)^{-e_inf}]
#         in H_1(X°,F_2)_G  (X° = punctured surface, H_1(X°,F_2) = N^{ab} (x) F_2),
#   r_L = rank of their images in L/2L  (the G^{ab}-visible part; r_L <= r),
# for every Aut(G)-class of generating pairs (GQuotients) of every 2-generated
# 2-group of the given orders.  Also tests whether the module M = H_1(X,F_2) is
# determined by the conjugacy classes of the three cyclic subgroups <sigma_b>
# ("subgroup-determinacy"), via MeatAxe isomorphism testing inside each bin.
#
# usage:  sage lemmaB/census_top.sage 4 8 16 32 [64]   -> lemmaB/census_top_<orders>.csv + stdout summary
import sys, csv
# pull in the helpers of torsion_module.sage without triggering its CLI block
exec(preparse(open("torsion_module.sage").read().split('if __name__ == "__main__":')[0]))

def full_module(G, s0, s1):
    """As torsion_module.analyze, but also returns the coinvariant data of X°."""
    elts, idx = elt_index(G)
    d = len(elts)
    sinf = (s0*s1)**(-1)
    R0 = right_perm(elts, idx, s0); R1 = right_perm(elts, idx, s1)
    Rinf = right_perm(elts, idx, sinf); R1inv = right_perm(elts, idx, s1**(-1))
    V = VectorSpace(F2, 2*d)
    rows = []
    for g in range(d):
        r = [0]*d; r[g] += 1; r[R0[g]] += 1; rows.append(r)
    for g in range(d):
        r = [0]*d; r[g] += 1; r[R1[g]] += 1; rows.append(r)
    B = Matrix(F2, rows).transpose()
    Z = B.right_kernel(); assert Z.dimension() == d + 1
    Zs = V.subspace(Z.basis())
    # puncture classes: one orbit representative per branch point, and all of them
    punct = {0: [], 1: [], 2: []}
    for o in orbits_under(R0):
        v = [0]*(2*d)
        for g in o: v[g] += 1
        punct[0].append(V(v))
    for o in orbits_under(R1):
        v = [0]*(2*d)
        for g in o: v[d+g] += 1
        punct[1].append(V(v))
    for o in orbits_under(Rinf):
        g0 = o[0]; v = [0]*(2*d); j = g0
        for _ in range(len(o)):
            v[d + R1inv[j]] += 1; v[Rinf[j]] += 1; j = Rinf[j]
        punct[2].append(V(v))
    W = V.subspace(punct[0] + punct[1] + punct[2])
    assert W.is_subspace(Zs)
    # left G-action on C_1 and the subspace I*Z_1 = span (h-1) z
    gens = list(libgap.GeneratorsOfGroup(G))
    def left_on_C1(h, z):
        Lp = left_perm(elts, idx, h); y = [0]*(2*d)
        for g_ in range(d):
            if z[g_]:   y[Lp[g_]] += 1
            if z[d+g_]: y[d+Lp[g_]] += 1
        return V(y)
    IZ = V.subspace([left_on_C1(h, z) - z for h in gens for z in Zs.basis()])
    dimZG = Zs.dimension() - IZ.dimension()                       # = 2 + d(M(G)) by Hopf
    reps = [punct[0][0], punct[1][0], punct[2][0]]
    r = V.subspace(IZ.basis() + reps).dimension() - IZ.dimension()
    # sanity: all conjugates of a puncture class agree in coinvariants
    assert V.subspace(IZ.basis() + punct[0] + punct[1] + punct[2]).dimension() - IZ.dimension() == r
    dimMG = Zs.dimension() - V.subspace(IZ.basis() + W.basis()).dimension()
    twog = Zs.dimension() - W.dimension()
    # module matrices for MeatAxe (basis of Zs/W)
    Wb = list(W.basis()); span = V.subspace(Wb); basisH = []
    for zb in Zs.basis():
        t = V.subspace(list(span.basis()) + [zb])
        if t.dimension() > span.dimension(): basisH.append(zb); span = t
    Mb = Matrix(F2, [list(v) for v in basisH] + [list(v) for v in Wb])
    def proj(v): return vector(F2, list(Mb.solve_left(v))[:twog])
    Ms = [Matrix(F2, [proj(left_on_C1(h, zb)) for zb in basisH]).transpose() for h in gens]
    return twog, Ms, dimZG, r, dimMG

def rL(G, s0, s1):
    """rank in L/2L of p_0=(e0,0), p_1=(0,e1), p_inf=(e_inf,e_inf), L = ker(Z^2 -> G^ab)."""
    e0, e1 = int(libgap.Order(s0)), int(libgap.Order(s1)); einf = int(libgap.Order((s0*s1)**-1))
    D = libgap.DerivedSubgroup(G)
    vecs = [vector(ZZ, [e0, 0]), vector(ZZ, [0, e1])]
    p0 = [s0**u for u in range(e0)]
    for u in range(e0):
        for v in range(e1):
            if bool((p0[u] * s1**v) in D): vecs.append(vector(ZZ, [u, v]))
    L = (ZZ**2).span(vecs)
    assert L.index_in(ZZ**2) == int(libgap.Index(G, D))
    Lb = L.basis_matrix()
    ps = [vector(ZZ, [e0, 0]), vector(ZZ, [0, e1]), vector(ZZ, [einf, einf])]
    coords = [Lb.solve_left(p) for p in ps]
    return Matrix(F2, [[c % 2 for c in v] for v in coords]).rank()

def gap_module(Ms):
    return libgap.GModuleByMats(libgap([libgap(M) for M in Ms]), libgap.GF(2))
_Indec = libgap.eval("MTX.Indecomposition")
_Iso = libgap.eval("MTX.IsomorphismModules")
_EndB = libgap.eval("MTX.BasisModuleEndomorphisms")
_fail = libgap.eval("fail")

orders = [int(a) for a in sys.argv[1:]] or [4, 8, 16, 32]
Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
tag = "_".join(str(o) for o in orders)
out = open(f"lemmaB/census_top_{tag}.csv", "w"); wr = csv.writer(out)
wr.writerow(["order", "id", "struct", "dM", "e0", "e1", "einf", "genus", "dimZG", "dimMG", "r", "rL", "indec", "dimEnd", "EndModRad", "subgp_bin"])
agg = {}      # (dM, r) -> count of triples
maxdimMG = {}
det_bins = 0; det_fail = []
for order in orders:
    for i in range(1, int(libgap.NrSmallGroups(order)) + 1):
        G = libgap.SmallGroup(order, i)
        if int(libgap.RankPGroup(G)) > 2: continue
        dM = len(list(libgap.AbelianInvariantsMultiplier(G)))
        struct = str(libgap.StructureDescription(G))
        ccs = libgap.ConjugacyClassesSubgroups(G)
        def sub_class(s):
            H = libgap.Group(s)
            for k in range(int(libgap.Length(ccs))):
                if bool(H in ccs[k]): return k
        bins = {}
        rows = []
        for h in libgap.GQuotients(Fr, G):
            s0 = libgap.Image(h, fg[0]); s1 = libgap.Image(h, fg[1]); sinf = (s0*s1)**-1
            twog, Ms, dimZG, r, dimMG = full_module(G, s0, s1)
            if twog == 0: continue
            assert dimZG == 2 + dM, (order, i, dimZG, dM)
            assert dimMG == 2 + dM - r
            rl = rL(G, s0, s1); assert rl <= r
            Mg = gap_module(Ms)
            parts = _Indec(Mg); indec = int(libgap.Length(parts)) == 1
            dimEnd = int(libgap.Length(_EndB(Mg)))
            _, blocks, _ = centralizer_solvable(twog, Ms)          # Wedderburn blocks of End/rad
            blocks = "+".join(f"M{a}(F{q})" for a, q in sorted(blocks))
            key = tuple(sorted([sub_class(s0), sub_class(s1), sub_class(sinf)]))
            bins.setdefault(key, []).append(Mg)
            e = (int(libgap.Order(s0)), int(libgap.Order(s1)), int(libgap.Order(sinf)))
            rows.append([order, i, struct, dM, *e, twog // 2, dimZG, dimMG, r, rl, indec, dimEnd, blocks, str(key)])
            agg[(dM, r)] = agg.get((dM, r), 0) + 1
            maxdimMG[(order, i)] = max(maxdimMG.get((order, i), 0), dimMG)
        for row in rows: wr.writerow(row)
        out.flush()
        # subgroup-determinacy: within each bin, are all modules isomorphic?
        for key, mods in bins.items():
            if len(mods) < 2: continue
            det_bins += 1
            for Mg in mods[1:]:
                iso = _Iso(mods[0], Mg)
                if iso == _fail:
                    det_fail.append((order, i, key, len(mods))); break
        if rows:
            vals = sorted(set(rw[9] for rw in rows)); rs = sorted(set(rw[10] for rw in rows))
            ends = sorted(set(rw[14] for rw in rows))
            print(f"[{order},{i}] {struct}: d(M(G))={dM} triples={len(rows)} dimM_G in {vals} r in {rs} "
                  f"all_indec={all(rw[12] for rw in rows)} End/rad in {ends}", flush=True)
out.close()
print("\n=== r vs d(M(G)) (count of Aut-classes of positive-genus triples) ===")
for dM in sorted(set(k[0] for k in agg)):
    print(f"d(M(G))={dM}: " + ", ".join(f"r={r}:{agg[(dM,r)]}" for r in range(4) if (dM, r) in agg))
print("\n=== subgroup-determinacy: bins with >=2 Aut-classes of triples sharing the three subgroup classes ===")
print(f"bins tested: {det_bins}; bins where M is NOT determined by the subgroup classes: {len(det_fail)}")
for f in det_fail: print("   ", f)
