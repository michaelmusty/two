# Sharded nonsolvable-centralizer scan for Galois 2-group Belyi maps + B-insight data.
# Args: ORDER LO HI  (scan SmallGroup(ORDER, i) for i in [LO,HI)).
# Per genus>=2 triple, records to a CSV-ish log:
#   gid, quo, genus, dim, maxmult, n_indec, summary(dim^mult ...)
# maxmult>=3 => instant PRIZE; maxmult==2 => exact field check (nonsolvable if F4+ endo).
import sys
_a = sys.argv[:]; sys.argv = [sys.argv[0]]
load("torsion_module.sage"); sys.argv = _a
from sage.all import libgap
import time

ORDER = int(_a[1])
# two arg modes: "ORDER LO HI" (range) or "ORDER list <i1,i2,...>" (explicit indices)
if len(_a) > 2 and _a[2] == "list":
    IDXS = [int(x) for x in _a[3].split(",")]; LO, HI = IDXS[0], IDXS[-1]+1
else:
    LO = int(_a[2]); HI = int(_a[3]); IDXS = list(range(LO, HI))
_Indec = libgap.eval("MTX.Indecomposition")
_Iso   = libgap.eval("MTX.IsomorphismModules")
_Dim   = libgap.eval("MTX.Dimension")
_fail  = libgap.eval("fail")

def decomp(dim, Ms):
    gm = libgap.GModuleByMats(Ms, libgap.GF(2))
    parts = _Indec(gm); mods = [parts[i][1] for i in range(len(parts))]
    reps = []                                  # [(rep, mult, dim)]
    for m in mods:
        md = int(_Dim(m)); placed=False
        for k,(r,c,rd) in enumerate(reps):
            if rd==md and _Iso(r, m) != _fail:
                reps[k]=(r,c+1,rd); placed=True; break
        if not placed: reps.append((m,1,md))
    reps.sort(key=lambda t:(-t[1],-t[2]))
    mm = max(c for _,c,_ in reps)
    summ = " ".join(f"{rd}^{c}" for _,c,rd in reps)
    return mm, len(mods), summ

F = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(F)
out = open(f"/tmp/shard_{ORDER}_{LO}_{HI}.csv", "w"); print("# gid quo genus dim maxmult nindec summary", file=out, flush=True)
t0=time.time()
for i in IDXS:
    G = libgap.SmallGroup(ORDER, i)
    if bool(libgap.IsAbelian(G)): continue
    struct = str(libgap.StructureDescription(G))
    for qi,h in enumerate(libgap.GQuotients(F, G)):
        s0=libgap.Image(h,fg[0]); s1=libgap.Image(h,fg[1])
        genus,dim,Ms,_ = analyze(G,s0,s1,verbose=False)
        if genus < 2: continue
        mm, nind, summ = decomp(dim, Ms)
        tag=""
        if mm >= 3:
            tag=" PRIZE_mult>=3"
        elif mm == 2:
            solvC,_,_ = centralizer_solvable(dim, Ms)
            tag = "" if solvC else " PRIZE_mult2_F4"
        print(f"{i} {qi} {genus} {dim} {mm} {nind} {summ}{tag}", file=out, flush=True)
        if tag:
            print(f"*** {tag.strip()} *** [{ORDER},{i}]{struct} quo{qi} genus={genus} dim={dim} [{summ}]", flush=True)
    if i % 20 == 0:
        print(f"  shard[{LO},{HI}) at gid {i}  ({time.time()-t0:.0f}s)", flush=True)
print(f"SHARD_DONE [{LO},{HI}) in {time.time()-t0:.0f}s", flush=True)
out.close()
