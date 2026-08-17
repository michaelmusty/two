# The GM example is p=5, level 33 -> the abelian surface is a 2-dimensional new
# component of level 165 = 5*33, Steinberg at 5 (so a_5 = +-1).
N = 165
M = ModularSymbols(N, 2, sign=1).cuspidal_subspace().new_subspace()
print("new subspace of level %d has dimension %d" % (N, M.dimension()))
for D in M.decomposition():
    if D.dimension() != 2:
        continue
    U5 = D.hecke_matrix(5)
    scalar = U5 == U5[0,0]*identity_matrix(2)
    print("  dim-2 component: U_5 = %s (scalar: %s), T_2 charpoly = %s" % (
        U5[0,0] if scalar else U5.list(), scalar, D.hecke_matrix(2).charpoly().factor()))
    print("     -> Hecke field degree %d, Steinberg at 5: %s" % (
        D.hecke_matrix(2).charpoly().degree(), scalar))
