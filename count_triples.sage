# Replicate Thm 1.2.2 of Musty's thesis: number of isomorphism classes of
# (Galois) 2-group Belyi maps of degree d = # normal subgroups of index d in F_2
#   = sum over 2-groups G of order d of #{ Aut(G)-orbits of generating pairs }
#   = sum_i  |GQuotients(F_2, SmallGroup(d,i))|
import sys, time

F = libgap.FreeGroup(2)
expected = {1:1, 2:3, 4:7, 8:19, 16:55, 32:151, 64:503, 128:1799, 256:7175}

degrees = [int(x) for x in sys.argv[1:]] or [1,2,4,8,16,32]
for d in degrees:
    t0 = time.time()
    n = int(libgap.NrSmallGroups(d))
    total = 0
    two_gen = 0
    for i in range(1, n+1):
        G = libgap.SmallGroup(d, i)
        q = libgap.GQuotients(F, G)
        c = int(libgap.Length(q))
        if c > 0:
            two_gen += 1
        total += c
    exp = expected.get(d, "?")
    ok = "OK" if exp == total else "MISMATCH"
    print(f"d={d:4d}  groups={n:6d}  2-generated={two_gen:4d}  "
          f"triples={total:6d}  expected={exp:>5}  [{ok}]  {time.time()-t0:6.1f}s",
          flush=True)
