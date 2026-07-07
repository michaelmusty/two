# Census of Galois 2-group Belyi maps oriented toward the nonsolvability question.
#
# Each isomorphism class = an epimorphism  phi: F_2 ->> G  (G a 2-group of order d),
# up to Aut(G), given by GQuotients. From phi we read the monodromy triple
#   s0 = phi(x), s1 = phi(y), sinf = (s0 s1)^{-1}
# with local ramification orders e0,e1,einf = orders of s0,s1,sinf in the regular rep.
# Genus (Riemann-Hurwitz, Galois cover X -> X/G = P^1 branched at {0,1,inf}):
#   g = 1 + (|G|/2)*(1 - 1/e0 - 1/e1 - 1/einf).
#
# For J[2] = H^1(X,F_2) to have a NONSOLVABLE Galois image we need g>=2
# (Sp_2(F_2)=S_3 solvable; Sp_4(F_2)=S_6 nonsolvable) AND, since the Galois
# image centralizes rho(G) in Sp_{2g}(F_2), the group G must be nonabelian and
# act on J[2] with a large centralizer.  Here we tabulate g and abelianness so we
# know where the candidates live.  (The centralizer test itself is Stage 2.)
import sys
from collections import Counter

F = libgap.FreeGroup(2)
gens = libgap.GeneratorsOfGroup(F)

degrees = [int(x) for x in sys.argv[1:]] or [2,4,8,16,32]
for d in degrees:
    n = int(libgap.NrSmallGroups(d))
    total = 0
    genus_counter = Counter()          # genus -> #triples
    genus_nonab = Counter()            # genus -> #triples with G nonabelian
    candidates = []                    # (genus, G id, structure, e0,e1,einf, abelian?)
    for i in range(1, n+1):
        G = libgap.SmallGroup(d, i)
        ab = bool(libgap.IsAbelian(G))
        gid = f"[{d},{i}]"
        try:
            struct = str(libgap.StructureDescription(G))
        except Exception:
            struct = "?"
        q = libgap.GQuotients(F, G)
        for h in q:
            total += 1
            s0 = libgap.Image(h, gens[0])
            s1 = libgap.Image(h, gens[1])
            sinf = (s0*s1)**(-1)
            e0 = int(libgap.Order(s0)); e1 = int(libgap.Order(s1)); ei = int(libgap.Order(sinf))
            g = 1 + (d/2)*(1 - 1/e0 - 1/e1 - 1/ei)
            g = int(g)
            genus_counter[g] += 1
            if not ab:
                genus_nonab[g] += 1
            if g >= 2 and not ab:
                candidates.append((g, gid, struct, (e0,e1,ei)))
    print(f"===== degree d = {d}  ({total} triples) =====")
    print("  genus:  " + "  ".join(f"g{g}:{genus_counter[g]}" for g in sorted(genus_counter)))
    print("  of which G nonabelian: " +
          "  ".join(f"g{g}:{genus_nonab[g]}" for g in sorted(genus_nonab) if genus_nonab[g]))
    # show the lightest candidates (smallest |G| already fixed = d; sort by genus then structure)
    cand_by = {}
    for g, gid, struct, ram in candidates:
        cand_by.setdefault((struct,), []).append((g, ram))
    print(f"  nonabelian G with genus>=2: {len(candidates)} triples, "
          f"{len(set(c[1] for c in candidates))} distinct groups")
    seen = set()
    for g, gid, struct, ram in sorted(candidates):
        key = (struct, g)
        if key in seen: continue
        seen.add(key)
        print(f"    g={g}  G={gid} {struct:20s} ram(e0,e1,inf)={ram}")
    print(flush=True)
