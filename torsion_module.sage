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

    # matrix of the left action of an arbitrary group element g on H_1(X~,F_2)
    def matfn(g):
        Lp = left_perm(elts, idx, g)
        cols = []
        for zb in basisH:             # zb is a V-vector (a cycle in Zs)
            y = [0]*(2*d)
            for g_ in range(d):
                if zb[g_]:   y[Lp[g_]] += 1     # e0_g -> e0_{h g}
                if zb[d+g_]: y[d+Lp[g_]] += 1   # e1_g -> e1_{h g}
            cols.append(proj(V(y)))
        return Matrix(F2, cols).transpose()     # columns = images of basis

    gens = list(libgap.GeneratorsOfGroup(G))
    Ms = [matfn(h) for h in gens]
    return genus, twog, Ms, matfn

def restrict_to_invariants(matfn, twog, Hgens):
    """M^H = common fixed space of H on H^1(X~,F_2); return (basis matrix, dim)."""
    I = identity_matrix(F2, twog)
    stack = []
    for h in Hgens:
        stack.append(matfn(h) - I)
    if stack:
        Big = block_matrix(F2, [[m] for m in stack], subdivide=False)
        MH = Big.right_kernel()
    else:
        MH = (F2**twog)
    return MH

def analyze_nongalois(G, s0, s1, H):
    """Compute H^1(X,F_2)=H^1(X~)^H with the Aut(X)=N_G(H)/H action.
    Returns (genus_X, dim, action_matrices) for the solvability screen."""
    genus_t, twog, _Ms, matfn = analyze(G, s0, s1)
    Hgens = list(libgap.GeneratorsOfGroup(H))
    MH = restrict_to_invariants(matfn, twog, Hgens)
    B = MH.basis_matrix()                 # rows = basis of M^H, in H^1(X~) coords
    dimX = MH.dimension()
    # N/H action on M^H: for nu in gens(N_G(H)), restrict matfn(nu) to M^H.
    N = libgap.Normalizer(G, H)
    Ngens = list(libgap.GeneratorsOfGroup(N))
    A = []
    for nu in Ngens:
        Mnu = matfn(nu)
        # image of each basis row under Mnu (acts on column vectors): (Mnu * b^T)^T
        rows_img = [Mnu * B[r] for r in range(dimX)]
        # express in basis B: solve  X * B = img  for coordinates
        coords = [B.solve_left(v) for v in rows_img]
        A.append(Matrix(F2, coords))       # action on M^H in basis B (row convention)
    return dimX // 2, dimX, A

def gl_solvable(a, q):
    # GL_a(q) solvable iff a==1, or (a==2 and q in {2,3}). (q is a power of 2 here.)
    if a == 1: return True
    if a == 2: return q in (2, 3)
    return False

def commutant_basis(n, Ms):
    # F_2-basis of A = { X in M_n(F_2) : X P = P X for all generator matrices P }
    rows = []
    for P in Ms:
        for a in range(n):
            for b in range(n):
                row = [0]*(n*n)              # coeff of X[i,j] in (XP-PX)[a,b]
                for i in range(n):
                    if P[a][i]:
                        row[i*n + b] += 1    # -(P X)[a,b] term: sum_i P[a,i] X[i,b]
                for j in range(n):
                    if P[j][b]:
                        row[a*n + j] += 1    # (X P)[a,b] term: sum_j X[a,j] P[j,b]
                rows.append(row)
    C = Matrix(F2, rows) if rows else Matrix(F2, 0, n*n)
    K = C.right_kernel()
    return [Matrix(F2, n, n, list(v)) for v in K.basis()]

def centralizer_solvable(dim, Ms):
    """Is the centralizer of <Ms> in GL(dim,2) solvable?  = unit group of the
    commutant algebra A.  A^* solvable iff every Wedderburn block M_{a}(F_q) of
    A/rad has GL_a(q) solvable.  Returns (solvable?, blocks[(a,q)], dim End)."""
    n = dim
    basis = commutant_basis(n, Ms)
    dimA = len(basis)
    gb = libgap([libgap(b) for b in basis])
    A = libgap.AlgebraWithOne(libgap.GF(2), gb)
    R = libgap.RadicalOfAlgebra(A)
    hom = libgap.NaturalHomomorphismByIdeal(A, R)
    S = libgap.ImagesSource(hom)                    # semisimple A/rad
    D = libgap.DirectSumDecomposition(S)            # simple two-sided ideals
    blocks = []
    solvC = True
    for k in range(int(libgap.Length(D))):
        I = D[k]
        dI = int(libgap.Dimension(I))
        kz = int(libgap.Dimension(libgap.Center(I)))   # M_a(F_{2^k}): center dim = k
        q = 2**kz
        a = isqrt(dI // kz)                              # dI = a^2 * k
        blocks.append((a, q))
        if not gl_solvable(a, q):
            solvC = False
    return solvC, blocks, dimA

def solvable_report(genus, dim, Ms, label):
    solvC, blocks, dimA = centralizer_solvable(dim, Ms)
    ordH = int(libgap.Order(libgap.Group(libgap([libgap(M) for M in Ms]))))
    shape = " x ".join(f"M_{a}(F_{q})" for a, q in sorted(blocks))
    flag = "" if solvC else "   <<< NONSOLVABLE CENTRALIZER"
    print(f"{label}: genus={genus} dimJ2={dim} |rho(G)|={ordH} dimEnd={dimA} "
          f"A/rad={shape} solvable={solvC}{flag}", flush=True)
    return solvC, blocks

def nongalois_scan(degrees):
    """Screen non-Galois 2-group Belyi maps: for core-free H<G and each triple,
    test whether the centralizer of Aut(X)=N_G(H)/H on H^1(X,F_2)=H^1(X~)^H is
    solvable.  Solvable => Q(J[2]) provably solvable; nonsolvable => candidate."""
    Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
    cands = []; nscanned = 0
    for order in degrees:
        n = int(libgap.NrSmallGroups(order))
        for i in range(1, n + 1):
            G = libgap.SmallGroup(order, i)
            if bool(libgap.IsAbelian(G)):
                continue
            struct = str(libgap.StructureDescription(G))
            ccs = libgap.ConjugacyClassesSubgroups(G)
            Hreps = []
            for k in range(int(libgap.Length(ccs))):
                H = libgap.Representative(ccs[k]); oH = int(libgap.Order(H))
                if oH == 1 or oH == order: continue
                if int(libgap.Order(libgap.Core(G, H))) != 1: continue
                Hreps.append(H)
            if not Hreps: continue
            quos = libgap.GQuotients(Fr, G)
            for H in Hreps:
                d = order // int(libgap.Order(H))
                autX = int(libgap.Order(libgap.Normalizer(G, H))) // int(libgap.Order(H))
                for h in quos:
                    s0 = libgap.Image(h, fg[0]); s1 = libgap.Image(h, fg[1])
                    gX, dim, Amats = analyze_nongalois(G, s0, s1, H)
                    if gX < 2: continue
                    nscanned += 1
                    solvC, blocks, _ = centralizer_solvable(dim, Amats)
                    if not solvC:
                        shape = " x ".join(f"M_{a}(F_{q})" for a, q in sorted(blocks))
                        print(f"  CANDIDATE d={d} G=[{order},{i}]{struct} gX={gX} "
                              f"|Aut(X)|={autX} A/rad={shape}", flush=True)
                        cands.append((order, i, gX, d, autX))
    print(f"\n--- non-Galois scan: {nscanned} (curve,triple) with genus>=2 ---")
    print(f"==== {len(cands)} NONSOLVABLE-centralizer candidates ====" if cands
          else "==== NONE: every non-Galois genus>=2 map here has solvable Q(J[2]) ====")
    return cands

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
                genus, dim, Ms, _ = analyze(G, s0, s1)
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
    argv = sys.argv[1:]
    if argv and argv[0] == "ng":
        nongalois_scan([int(x) for x in argv[1:]] or [16, 32])
        sys.exit(0)
    args = [int(x) for x in argv]
    if args:
        scan(args)
    else:
        G = libgap.SmallGroup(8,4)
        gens = libgap.GeneratorsOfGroup(G)
        genus, dim, Ms, _ = analyze(G, gens[0], gens[1])
        solvable_report(genus, dim, Ms, "Q8 (8,4) demo")
