# Stage 2: compute J[2] = H_1(X, F_2) as an F_2[G]-module for a Galois 2-group
# Belyi cover X -> P^1 given by a monodromy triple (s0,s1,sinf) in G (regular rep).
#
# Model: Y = X minus ramification pts = G-cover of the figure-eight (pi_1 = F_2).
#   Sheets = elements of G. Monodromy = RIGHT mult; deck G-action = LEFT mult (commute).
#   C_1(Y) = <e0_g, e1_g>_{g in G}  (edges over the two loops gamma_0, gamma_1)
#   C_0(Y) = <v_g>                  d1(e0_g)=v_g+v_{g s0},  d1(e1_g)=v_g+v_{g s1}
#   Z_1 = ker d1  (dim d+1).  Compactify by killing the puncture loops:
#     over 0:  L0 = sum_orbit e0     (right-<s0> orbits = left cosets)
#     over 1:  L1 = sum_orbit e1
#     over inf: Linf = sum_k ( e1_{g sinf^k s1^{-1}} + e0_{g sinf^{k+1}} )   [word (s0 s1)^-1]
#   H_1(X,F_2) = Z_1 / span(L0,L1,Linf).  Left mult by G descends -> F_2[G]-module.
# Then rho(G) <= GL(2g,2); C = Centralizer in GL(2g,2). If C solvable, the field
# Q(J[2]) is solvable for THIS triple (Galois image centralizes rho(G)) -> hopeless.
import sys

F2 = GF(2)

def elt_index(G):
    elts = list(libgap.Elements(G))
    idx = {str(e): i for i, e in enumerate(elts)}
    return elts, idx

def right_perm(elts, idx, s):
    # permutation i -> idx(elts[i]*s)
    return [idx[str(e*s)] for e in elts]

def left_perm(elts, idx, h):
    return [idx[str(h*e)] for e in elts]

def orbits_under(perm):
    d = len(perm); seen = [False]*d; orbs = []
    for i in range(d):
        if seen[i]: continue
        o = []; j = i
        while not seen[j]:
            seen[j] = True; o.append(j); j = perm[j]
        orbs.append(o)
    return orbs

def analyze(G, s0, s1, verbose=True):
    elts, idx = elt_index(G)
    d = len(elts)
    sinf = (s0*s1)**(-1)
    R0 = right_perm(elts, idx, s0)
    R1 = right_perm(elts, idx, s1)
    Rinf = right_perm(elts, idx, sinf)
    s1inv = s1**(-1)
    R1inv = right_perm(elts, idx, s1inv)

    V = VectorSpace(F2, 2*d)          # e0_g -> g ,  e1_g -> d+g
    C0 = VectorSpace(F2, d)
    # boundary d1 as 2d x d (rows = edges); build kernel of the map C_1 -> C_0
    rows = []
    for g in range(d):                # e0_g
        r = [0]*d; r[g] += 1; r[R0[g]] += 1; rows.append(r)
    for g in range(d):                # e1_g
        r = [0]*d; r[g] += 1; r[R1[g]] += 1; rows.append(r)
    D = Matrix(F2, rows)              # (2d) x d ; edge -> vertices
    B = D.transpose()                 # d x 2d : boundary map C_1 -> C_0 on columns
    Z = B.right_kernel()              # cycles: x in C_1=GF(2)^{2d} with B x = 0
    assert Z.dimension() == d + 1, (Z.dimension(), d+1)

    # relations
    rels = []
    for o in orbits_under(R0):        # L0
        v = [0]*(2*d)
        for g in o: v[g] += 1
        rels.append(v)
    for o in orbits_under(R1):        # L1
        v = [0]*(2*d)
        for g in o: v[d+g] += 1
        rels.append(v)
    for o in orbits_under(Rinf):      # Linf : sum_k e1_{g sinf^k s1^-1} + e0_{g sinf^{k+1}}
        g0 = o[0]; v = [0]*(2*d); j = g0
        for _ in range(len(o)):
            v[d + R1inv[j]] += 1      # e1_{ j * s1^{-1} }
            v[Rinf[j]] += 1           # e0_{ j * sinf }
            j = Rinf[j]
        rels.append(v)
    W = V.subspace([V(r) for r in rels])
    Zs = V.subspace(Z.basis())
    assert W.is_subspace(Zs), "relations not closed (bug in Linf)"

    # Choose an explicit basis of H_1 = Zs / W:  greedily extend W to a basis of Zs.
    Wb = list(W.basis())
    span = V.subspace(Wb) if Wb else V.subspace([])
    basisH = []                       # representatives of a basis of Zs/W
    for zb in Zs.basis():
        test = V.subspace(list(span.basis()) + [zb])
        if test.dimension() > span.dimension():
            basisH.append(zb); span = test
    twog = len(basisH)
    assert twog % 2 == 0, twog
    genus = twog // 2
    # coordinate change: rows = [basisH ... , Wb ...] form a basis of Zs
    Mbasis = Matrix(F2, [list(v) for v in basisH] + [list(v) for v in Wb])
    def proj(v):                      # v in Zs (length 2d) -> H_1 coords (length 2g)
        x = Mbasis.solve_left(V(v))
        return vector(F2, list(x)[:twog])

    # left G-action matrices on H_1
    gens = list(libgap.GeneratorsOfGroup(G))
    Ms = []
    for h in list(gens):
        Lp = left_perm(elts, idx, h)
        cols = []
        for zb in basisH:             # zb is a V-vector (a cycle in Zs)
            y = [0]*(2*d)
            for g_ in range(d):
                if zb[g_]:   y[Lp[g_]] += 1     # e0_g -> e0_{h g}
                if zb[d+g_]: y[d+Lp[g_]] += 1   # e1_g -> e1_{h g}
            cols.append(proj(V(y)))
        M = Matrix(F2, cols).transpose()        # columns = images of basis
        Ms.append(M)
    return genus, twog, Ms

def solvable_report(genus, dim, Ms, label):
    # push matrices into GAP, build subgroup of GL(dim,2), centralizer, solvability
    gapMs = [libgap(M) for M in Ms]
    GL = libgap.GL(dim, 2)
    H = libgap.Group(gapMs)
    ordH = int(libgap.Order(H))
    C = libgap.Centralizer(GL, H)
    ordC = int(libgap.Order(C))
    solvC = bool(libgap.IsSolvable(C))
    factors = ""
    if not solvC:
        cf = libgap.CompositionFactors(C)
        names = [str(libgap.StructureDescription(f)) for f in cf if int(libgap.Order(f)) > 1]
        factors = "  factors=" + ",".join(names)
    print(f"{label}: genus={genus} dimJ2={dim} |rho(G)|={ordH} "
          f"|C_GL|={ordC} solvable={solvC}{factors}", flush=True)
    return solvC, ordC

def scan(degrees):
    F = libgap.FreeGroup(2); fgens = libgap.GeneratorsOfGroup(F)
    nonsolv = []
    for d in degrees:
        n = int(libgap.NrSmallGroups(d))
        ntri = 0
        for i in range(1, n+1):
            G = libgap.SmallGroup(d, i)
            if bool(libgap.IsAbelian(G)):
                continue                       # abelian G -> abelian image, solvable
            struct = str(libgap.StructureDescription(G))
            for h in libgap.GQuotients(F, G):
                s0 = libgap.Image(h, fgens[0]); s1 = libgap.Image(h, fgens[1])
                genus, dim, Ms = analyze(G, s0, s1)
                if genus < 2:
                    continue
                ntri += 1
                label = f"d={d} G=[{d},{i}]{struct}"
                solvC, ordC = solvable_report(genus, dim, Ms, label)
                if not solvC:
                    nonsolv.append((d, i, struct, genus))
        print(f"--- degree {d}: scanned {ntri} nonabelian genus>=2 triples ---", flush=True)
    print("\n==== NONSOLVABLE-CENTRALIZER TRIPLES (candidates for nonsolvable Q(J[2])) ====")
    if not nonsolv:
        print("  NONE — every nonabelian genus>=2 triple in this range has solvable centralizer.")
    for x in nonsolv:
        print("  ", x)
    return nonsolv

if __name__ == "__main__":
    import sys
    args = [int(x) for x in sys.argv[1:]]
    if args:
        scan(args)
    else:
        G = libgap.SmallGroup(8,4)
        gens = libgap.GeneratorsOfGroup(G)
        genus, dim, Ms = analyze(G, gens[0], gens[1])
        solvable_report(genus, dim, Ms, "Q8 (8,4) demo")
