load("belyi/combinatorial_tower.sage")
from sage.all import libgap
import sys
orders = [int(a) for a in sys.argv[1:]] or [16,32]
print("SCANNING orders", orders, "for span-FAIL on a POSITIVE-genus base")
Fr = libgap.FreeGroup(2)
hits=[]; ncases=0; fail_g0=0; fail_gpos=0; cases_with_fail=0
for order in orders:
    for gid in range(1, int(libgap.NrSmallGroups(order))+1):
        G = libgap.SmallGroup(order, gid)
        if bool(libgap.IsAbelian(G)): continue
        nq = int(libgap.Size(libgap.GQuotients(Fr, G)))
        for quo in range(nq):
            ncases += 1
            try:
                v = run_oracle(order, gid, quo, verbose=False)
            except Exception as e:
                print(f"  [{order},{gid}] quo{quo} ERR {str(e)[:40]}"); continue
            anyfail=False
            for (s, ram, gb, ok) in v:
                if not ok:
                    anyfail=True
                    if gb>0:
                        fail_gpos+=1
                        hits.append((order,gid,quo,str(libgap.StructureDescription(G)),s,ram,gb))
                    else:
                        fail_g0+=1
            if anyfail: cases_with_fail+=1
print(f"scanned {ncases} triples; {cases_with_fail} had >=1 span-fail")
print(f"span-fails: {fail_g0} on genus-0 base (RR/rational, NO torsion), {fail_gpos} on genus>0 base (GENUINE torsion)")
print("GENUINE-TORSION hits (span-fail, base genus>0):")
for h in hits: print("  ", h)
if not hits: print("  NONE -- span never fails on a positive-genus base in these orders")
