# Fast nonsolvable-centralizer screen for Galois 2-group Belyi maps.
# MeatAxe indecomposable multiplicities are the primary filter (mult 1 => solvable,
# skip); mult>=2 falls back to the exact commutant/Wedderburn centralizer_solvable.
# Prize signal: NONSOLVABLE centralizer => candidate nonsolvable Q(J[2]) ramified only at 2.
import sys, time
_real_argv = sys.argv[:]
sys.argv = [sys.argv[0]]                 # shield torsion_module's __main__ (runs Q8 demo)
load("torsion_module.sage")
sys.argv = _real_argv
from sage.all import libgap

_Indec = libgap.eval("MTX.Indecomposition")
_Iso   = libgap.eval("MTX.IsomorphismModules")
_fail  = libgap.eval("fail")

def max_multiplicity(dim, Ms):
    gm = libgap.GModuleByMats(Ms, libgap.GF(2))
    parts = _Indec(gm)
    mods = [parts[i][1] for i in range(len(parts))]
    reps = []          # (rep_module, mult)
    for m in mods:
        for k,(r,c) in enumerate(reps):
            if _Iso(r, m) != _fail:
                reps[k] = (r, c+1); break
        else:
            reps.append((m, 1))
    return max(c for _,c in reps), len(mods)

def fast_scan(degrees, validate=False):
    F = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(F)
    prizes=[]; nchk=0; nskip=0; mismatches=0; ndecomp=0
    for d in degrees:
        t0=time.time()
        for i in range(1, int(libgap.NrSmallGroups(d))+1):
            G = libgap.SmallGroup(d, i)
            if bool(libgap.IsAbelian(G)): continue
            if i % 25 == 0: print(f"  ..progress d={d} group {i}/{int(libgap.NrSmallGroups(d))}  (checked {nchk}, decomp {ndecomp})", flush=True)
            struct = str(libgap.StructureDescription(G))
            for h in libgap.GQuotients(F, G):
                s0=libgap.Image(h,fg[0]); s1=libgap.Image(h,fg[1])
                genus,dim,Ms,_ = analyze(G,s0,s1,verbose=False)
                if genus < 2: continue
                mm, nind = max_multiplicity(dim, Ms)
                if mm >= 3:                          # GL_{>=3} always nonsolvable -> PRIZE
                    print(f"  *** NONSOLVABLE (mult>=3) *** d={d} G=[{d},{i}]{struct} genus={genus} dim={dim} maxmult={mm}", flush=True)
                    prizes.append((d,i,struct,genus,mm)); continue
                if mm >= 2:
                    ndecomp += 1
                    print(f"  DECOMP J[2] d={d} G=[{d},{i}]{struct} genus={genus} dim={dim} maxmult={mm}", flush=True)
                if mm == 1 and not validate:
                    nskip += 1; continue             # GL_1 blocks only => solvable
                nchk += 1                            # mm==2 (or validate): exact field check
                solvC,_,_ = centralizer_solvable(dim, Ms)
                if validate and (mm==1) and (not solvC):
                    print(f"  MISMATCH d={d}[{i}] mm={mm} solv={solvC}"); mismatches+=1
                if not solvC:
                    print(f"  *** NONSOLVABLE CENTRALIZER *** d={d} G=[{d},{i}]{struct} genus={genus} dim={dim} maxmult={mm}", flush=True)
                    prizes.append((d,i,struct,genus,mm))
        print(f"--- degree {d}: checked {nchk}, skipped(mult1) {nskip}, time {time.time()-t0:.0f}s ---", flush=True)
    print("\n==== NONSOLVABLE-CENTRALIZER (prize candidates) ====")
    print("  NONE" if not prizes else "")
    for p in prizes: print("  ", p)
    if validate: print(f"validation mismatches: {mismatches}")
    return prizes

if __name__ == "__main__":
    argv = sys.argv[1:]
    validate = ('validate' in argv)
    degs = [int(x) for x in argv if x.isdigit()]
    fast_scan(degs or [16,32], validate=validate)
