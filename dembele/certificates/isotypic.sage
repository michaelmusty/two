# The class we lift is an arbitrary element of the isotypic component, not an
# eigenvector over Q.  So what matters is how U_q and T_ell act on the WHOLE
# component: U_q must be a scalar (then ZZ(f/f0) works for any class), while
# T_ell need not be.
for N, deg in [(97, 4), (109, 4), (61, 3)]:
    M = ModularSymbols(N, 2, sign=1).cuspidal_subspace().new_subspace()
    for D in M.decomposition():
        if D.dimension() != deg:
            continue
        print("=== level %d, isotypic component of dimension %d" % (N, D.dimension()))
        Uq = D.hecke_matrix(N)
        is_scalar = Uq == Uq[0,0] * identity_matrix(D.dimension())
        print("    U_%d on the component = %s  -> scalar? %s" % (
            N, Uq.list() if D.dimension() <= 2 else "(%dx%d)" % (deg, deg), is_scalar))
        print("    U_%d eigenvalue = %s, charpoly = %s" % (N, Uq[0,0], Uq.charpoly().factor()))
        for ell in [2, 3]:
            if N % ell == 0: continue
            Tl = D.hecke_matrix(ell)
            sc = Tl == Tl[0,0] * identity_matrix(D.dimension())
            print("    T_%d scalar? %s   charpoly = %s" % (ell, sc, Tl.charpoly().factor()))
            # the fix: T_ell - ell - 1 as an OPERATOR is invertible on the component
            E = Tl - (ell + 1) * identity_matrix(D.dimension())
            print("       (T_%d - %d - 1) invertible on component? %s  det = %s" % (
                ell, ell, E.is_invertible(), E.det()))
        break
