# Export per-step ramification data for a 2-group tower, for the Hecke solver.
# For group (order,gid) and quotient index quo: emit JSON with, per chief-series step,
# the subset of branch points {0,1,oo} that ramify, and the predicted step-genus.
load("belyi/groups.sage")
import json
from sage.all import libgap

def gfp(d, pp):
    S = sum((d - d//e) for e in pp); return 1 + (S - 2*d)//2

def export(order, gid, quo=0):
    Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
    G = libgap.SmallGroup(order, gid)
    h = libgap.GQuotients(Fr, G)[quo]
    s0 = libgap.Image(h, fg[0]); s1 = libgap.Image(h, fg[1]); sinf = (s0*s1)**(-1)
    chain = chief_series_indices(G)
    genera = [gfp(int(libgap.Index(G, chain[j])), level_passport(G, s0, s1, chain[j]))
              for j in range(len(chain))]
    steps = []
    for i in range(len(chain) - 1):
        rb = step_ramified_branch_points(G, chain[i], chain[i+1], s0, s1, sinf)
        steps.append({"ramify": [str(b) for b in rb],
                      "genus_before": int(genera[i]), "genus_after": int(genera[i+1])})
    return {"order": int(order), "gid": int(gid), "quo": int(quo),
            "struct": str(libgap.StructureDescription(G)),
            "genera": [int(g) for g in genera], "steps": steps}

if __name__ == "__main__":
    import sys
    order = int(sys.argv[1]); gid = int(sys.argv[2]); quo = int(sys.argv[3]) if len(sys.argv)>3 else 0
    outpath = sys.argv[4] if len(sys.argv)>4 else "/tmp/tower_steps.json"
    d = export(order, gid, quo)
    with open(outpath,"w") as fh: json.dump(d, fh)
    print("WROTE", outpath)
