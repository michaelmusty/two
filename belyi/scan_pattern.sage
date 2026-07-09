# In one Sage process: find steps FROM positive genus whose ramifying set escapes the
# pullback span (heuristic: |ramify|==3, i.e. all of {0,1,oo}) -> RR solver likely needed
# on a positive-genus base => candidate for genuine Pic^0[2] torsion.
load("belyi/groups.sage")
from sage.all import libgap
def gfp(d, pp):
    S = sum((d - d//e) for e in pp); return 1 + (S - 2*d)//2
Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
hits=[]
for order in [16,32]:
    for gid in range(1, int(libgap.NrSmallGroups(order))+1):
        G = libgap.SmallGroup(order, gid)
        if bool(libgap.IsAbelian(G)): continue
        chain = chief_series_indices(G)
        for quo,h in enumerate(libgap.GQuotients(Fr, G)):
            s0=libgap.Image(h,fg[0]); s1=libgap.Image(h,fg[1]); sinf=(s0*s1)**(-1)
            genera=[gfp(int(libgap.Index(G,chain[j])), level_passport(G,s0,s1,chain[j])) for j in range(len(chain))]
            for i in range(len(chain)-1):
                if genera[i]>0:
                    rb=step_ramified_branch_points(G,chain[i],chain[i+1],s0,s1,sinf)
                    if len(rb)==3:
                        hits.append((order,gid,quo,str(libgap.StructureDescription(G)),genera,i,int(genera[i]))); break
print("PATTERNHITS")
seen=set()
for h in hits:
    k=(h[0],h[1],h[2])
    if k in seen: continue
    seen.add(k)
    print(f"[{h[0]},{h[1]}] quo{h[2]} {h[3]} genera{h[4]} step{h[5]} from genus {h[6]} ramifies all-3")
if not hits: print("NONE in order 16,32")
