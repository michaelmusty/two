# Quaternion Belyi curves are hyperelliptic: y^2 = x(x^{2g}-1), g = 2^{m-2}, G/z = D_{2g} on the 2g+2
# Weierstrass points (orbits g, g, 2 = fibres over 0, 1, oo). J[2] = even subsets / <all>.
# Decomposes it with MeatAxe and prints the socle of each summand.  usage: sage lemmaB/quaternion_hyperelliptic.sage
_Indec = libgap.eval("MTX.Indecomposition"); _Iso = libgap.eval("MTX.IsomorphismModules"); _fail = libgap.eval("fail")
F2 = GF(2)
def model(g):
    n = 2*g + 2
    def rho(i):
        if i < g: return (i + 1) % g
        if i < 2*g: return g + (i - g + 1) % g
        return i
    def tau(i):
        if i < g: return (-i) % g
        if i < 2*g: return g + (-(i - g) - 1) % g
        return 2*g if i == 2*g + 1 else 2*g + 1
    V = VectorSpace(F2, n)
    one = V([1]*n)
    # basis of M = E/<1>: e_i + e_{i+1} for i = 0..n-3  (n-2 = 2g vectors; e_0+e_1,...,e_{n-3}+e_{n-2} are independent mod <1>)
    basis = [V([1 if j in (i, i+1) else 0 for j in range(n)]) for i in range(n-2)]
    Bm = Matrix(F2, basis + [one])          # basis of E
    def coords(v):                          # v in E -> coords in M basis (drop the <1> coordinate)
        return vector(F2, list(Bm.solve_left(v))[:n-2])
    mats = []
    for p in (rho, tau):
        P = Matrix(F2, n, n)
        for i in range(n): P[i, p(i)] = 1
        mats.append(Matrix(F2, [coords(b * P) for b in basis]))   # row convention
    def tosubset(c):
        v = sum((c[k] * basis[k] for k in range(n-2)), V(0))
        return v
    lab = lambda j: ("a%d" % j if j < g else "b%d" % (j-g) if j < 2*g else ("0" if j == 2*g else "oo"))
    return mats, tosubset, lab, n
for g in [2, 4, 8]:
    mats, tosubset, lab, n = model(g)
    gm = libgap.GModuleByMats(libgap([libgap(M) for M in mats]), libgap.GF(2))
    parts = _Indec(gm)
    print(f"g={g}: dim M={2*g}, #summands={len(parts)}, dims={[int(parts[i][1]['dimension']) for i in range(len(parts))]}")
    for i in range(len(parts)):
        B = Matrix(F2, parts[i][0])
        # socle (invariants) of the summand, as subsets
        d = B.nrows(); I = identity_matrix(F2, d)
        sub = []
        for M in mats:
            img = B * M
            sub.append(Matrix(F2, [B.solve_left(img[r]) for r in range(d)]) - I)
        K = block_matrix([[A for A in sub]], subdivide=False).left_kernel()
        socs = [" ".join(lab(j) for j in range(n) if tosubset(vector(F2, list(k)) * B)[j]) for k in K.basis()]
        names = [" ".join(lab(j) for j in range(n) if tosubset(B[r])[j]) for r in range(d)]
        print(f"   summand {i} (dim {d}): socle = {{ {' ; '.join(socs)} }} (mod complement)")
        print(f"      basis: " + " | ".join(names))
