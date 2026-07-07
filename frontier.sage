# Frontier search: genus-g non-Galois 2-group Belyi maps with TRIVIAL Aut(X).
#
# For the mod-2 image to be PSL_2(16) (the only known nonsolvable group realizable
# ramified only at 2), it must act irreducibly on F_2^8 = F_16^2; its centralizer in
# Sp_8(F_2) is F_16^* = C_15, which contains NO nontrivial 2-group.  The Galois image
# centralizes Aut(X)=N_G(H)/H (a 2-group), so a genus-4 PSL_2(16) image forces
# Aut(X)=1.  Hence the structural frontier = genus-4 non-Galois 2-group Belyi maps
# X=X~/H with N_G(H)=H (self-normalizing, core-free).  We enumerate them (group
# theory only: genus via the coset action, Aut(X)=|N_G(H)/H|).
import sys
from collections import Counter

F = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(F)

def ncycles(perm, d):
    return int(libgap.Length(libgap.Cycles(perm, libgap.eval(f"[1..{d}]"))))

def scan(order, target_genus=4):
    n = int(libgap.NrSmallGroups(order))
    frontier = []; census = Counter()
    n2gen = 0
    for i in range(1, n + 1):
        G = libgap.SmallGroup(order, i)
        if bool(libgap.IsAbelian(G)):
            continue
        quos = libgap.GQuotients(F, G)          # generating triples (2-generated only)
        if int(libgap.Length(quos)) == 0:
            continue
        n2gen += 1
        struct = str(libgap.StructureDescription(G))
        ccs = libgap.ConjugacyClassesSubgroups(G)
        for k in range(int(libgap.Length(ccs))):
            H = libgap.Representative(ccs[k]); oH = int(libgap.Order(H))
            if oH == 1 or oH == order:
                continue
            if int(libgap.Order(libgap.Core(G, H))) != 1:
                continue                        # faithful monodromy = G
            d = order // oH
            autX = int(libgap.Order(libgap.Normalizer(G, H))) // oH
            act = libgap.FactorCosetAction(G, H)
            for h in quos:
                s0 = libgap.Image(act, libgap.Image(h, fg[0]))
                s1 = libgap.Image(act, libgap.Image(h, fg[1]))
                sinf = (s0 * s1)**(-1)
                c = ncycles(s0, d) + ncycles(s1, d) + ncycles(sinf, d)
                g = 1 + (-2*d + 3*d - c) // 2
                if g == target_genus:
                    census[autX] += 1
                    if autX == 1:
                        frontier.append((order, i, struct, d))
                        print(f"  FRONTIER g{target_genus} triv-Aut: G=[{order},{i}]{struct} "
                              f"deg={d} |Aut(X)|=1", flush=True)
    print(f"\norder {order}: {n2gen} 2-generated nonabelian groups; "
          f"genus-{target_genus} non-Galois records by |Aut(X)|: {dict(census)}")
    print(f"  => {len(frontier)} FRONTIER candidates (trivial Aut(X)) at order {order}")
    return frontier

if __name__ == "__main__":
    argv = [int(x) for x in sys.argv[1:]]
    order = argv[0] if argv else 64
    tg = argv[1] if len(argv) > 1 else 4
    scan(order, tg)
