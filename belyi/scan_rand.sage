load("belyi/combinatorial_tower.sage")
from sage.all import libgap
import sys
orders = [int(a) for a in sys.argv[1:-1]] or [16,32]
T = int(sys.argv[-1]) if len(sys.argv)>1 else 20
print(f"RANDOMIZED SCAN orders {orders}, {T} sibling-choice trials/case; flag POS-genus span-fail")
Fr = libgap.FreeGroup(2)
hits={}; ncases=0
for order in orders:
    for gid in range(1, int(libgap.NrSmallGroups(order))+1):
        G = libgap.SmallGroup(order, gid)
        if bool(libgap.IsAbelian(G)): continue
        nq = int(libgap.Size(libgap.GQuotients(Fr, G)))
        for quo in range(nq):
            ncases += 1
            for _ in range(T):
                try: v = run_oracle(order, gid, quo, verbose=False, randomize=True)
                except Exception: break
                for (s,ram,gb,ok) in v:
                    if (not ok) and gb>0:
                        key=(order,gid,str(libgap.StructureDescription(G)))
                        hits.setdefault(key,set()).add((s,gb))
print(f"scanned {ncases} triples x {T} trials")
print("groups where SOME sibling needs positive-genus RR (genuine-torsion possible):")
for k in sorted(hits): print("  ", k, "-> pos-genus fail rungs", sorted(hits[k]))
if not hits: print("  NONE in these orders")
