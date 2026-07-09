# Combinatorial (geometric, F_bar_p) tower + span oracle.
# Tracks the S-places of each tower level X_j as <sigma_b>-orbits on the quotient
# Q_j = G/H_j (chief series), with INTEGER valuations of {x, x-1, y_1..y_j} propagated
# by geometric ramification indices -- NO function-field arithmetic.  Reproduces the
# span PASS/FAIL verdict of the (slow) Hecke solver; validated below.
load("belyi/groups.sage")
from sage.all import libgap, GF, matrix, vector

BR = ['0', '1', 'oo']

def level_data(G, Hj, sbar_of):
    """For quotient Q_j=G/Hj: return (EQ list, proj hom, {b: [orbits]} places, {b:{q_pos:orbit_id}})."""
    proj = libgap.NaturalHomomorphismByNormalSubgroup(G, Hj)
    Q = libgap.ImagesSource(proj)
    EQ = list(libgap.Elements(Q))
    pos = {}                      # map Q-element -> index via identity string
    for i, q in enumerate(EQ):
        pos[str(q)] = i
    places = {}; place_of = {}
    for b in BR:
        gb = libgap.Image(proj, sbar_of[b])
        seen = [False]*len(EQ); orbs = []
        for i, q in enumerate(EQ):
            if seen[i]: continue
            orb = []; r = q
            while True:
                j = pos[str(r)]
                if seen[j]: break
                seen[j] = True; orb.append(j); r = r*gb
            orbs.append(frozenset(orb))
        places[b] = orbs
        place_of[b] = {}
        for oid, orb in enumerate(orbs):
            for j in orb: place_of[b][j] = oid
    return proj, EQ, places, place_of

def run_oracle(order, gid, quo, verbose=True, randomize=False):
    Fr = libgap.FreeGroup(2); fg = libgap.GeneratorsOfGroup(Fr)
    G = libgap.SmallGroup(order, gid)
    h = libgap.GQuotients(Fr, G)[quo]
    sb = {'0': libgap.Image(h, fg[0]), '1': libgap.Image(h, fg[1])}
    sb['oo'] = (sb['0']*sb['1'])**(-1)
    chain = chief_series_indices(G)                 # H_0=G ⊃ ... ⊃ H_L=1
    L = len(chain)
    # ---- level 0: P^1, one place per branch, e=1 ----
    # state: places[b] = list of dicts {'val': {func:int}}, indexed; plus a projection cache
    # We recompute quotient data per level and relate via representative lifts.
    # valuations keyed per level by (b, orbit_id).
    projs = [None]*L; EQs=[None]*L; places=[None]*L; place_of=[None]*L
    for j in range(L):
        projs[j], EQs[j], places[j], place_of[j] = level_data(G, chain[j], sb)
        # fill _posD_cache for this projection
    # valuation store: val[j][b][orbit_id][func] = int
    val = [ {b: [dict() for _ in places[j][b]] for b in BR} for j in range(L) ]
    funcs = ['x','x-1']
    # level 0 base valuations
    for b in BR:
        for oid,orb in enumerate(places[0][b]):
            v = val[0][b][oid]
            v['x']   = 1 if b=='0' else (-1 if b=='oo' else 0)
            v['x-1'] = 1 if b=='1' else (-1 if b=='oo' else 0)
    # level-0 radicand rad_0 = x^[0 in ram0] (x-1)^[1 in ram0]  (step 0 is never span-tested)
    ram0 = set(str(x) for x in step_ramified_branch_points(G, chain[0], chain[1], sb['0'], sb['1'], sb['oo']))
    a0 = 1 if '0' in ram0 else 0; b0 = 1 if '1' in ram0 else 0
    for b in BR:
        rv0 = a0 if b=='0' else (b0 if b=='1' else -(a0+b0))
        for oid in range(len(places[0][b])):
            val[0][b][oid]['radval'] = rv0
    verdicts = []
    # ---- climb levels; at level j build valuations from level j-1, then test step j ----
    for j in range(1, L):
        # ramification e(P'/P): orbit size ratio; parent via representative lift
        for b in BR:
            for oidU, orbU in enumerate(places[j][b]):
                qU = EQs[j][min(orbU)]
                g  = libgap.PreImagesRepresentative(projs[j], qU)
                qD = libgap.Image(projs[j-1], g)
                # locate parent orbit id at level j-1
                # find position of qD in EQs[j-1]
                pd = None
                for i,q in enumerate(EQs[j-1]):
                    if str(q)==str(qD): pd = place_of[j-1][b][i]; break
                eU = len(orbU); eD = len(places[j-1][b][pd])
                e_rel = eU // eD                       # 1 (split) or 2 (ramified)
                vU = val[j][b][oidU]
                # inherit old functions
                for f in funcs:
                    vU[f] = e_rel * val[j-1][b][pd][f]
                # new generator y_j = sqrt(rad_{j-1}); rad chosen at level j-1 (see below)
                if 'radval' in val[j-1][b][pd]:
                    rv = val[j-1][b][pd]['radval']       # val_P(rad_{j-1})
                    if e_rel==2:  vU[f'y{j}'] = rv
                    else:         vU[f'y{j}'] = rv//2
        funcs = ['x','x-1'] + [f'y{k}' for k in range(1, j+1)]
        # ---- span test at step j (X_j -> X_{j+1}), i.e. tower step index j ----
        ram = step_ramified_branch_points(G, chain[j], chain[min(j+1,L-1)], sb['0'], sb['1'], sb['oo']) if j < L-1 else None
        # build S-place list + target + parity rows
        Sp = [(b,oid) for b in BR for oid in range(len(places[j][b]))]
        def parity_vec(f):
            return vector(GF(2), [ val[j][b][oid].get(f,0) % 2 for (b,oid) in Sp ])
        if ram is not None:
            ramset = set(str(x) for x in ram)
            target = vector(GF(2), [ 1 if b in ramset else 0 for (b,oid) in Sp ])
            M = matrix(GF(2), [ list(parity_vec(f)) for f in funcs ])
            try:
                M.solve_left(target); ok=True
            except ValueError:
                ok=False
            gb = int(genus_of_level(G, chain[j], sb))
            verdicts.append((j, [str(x) for x in ram], gb, ok))
            if verbose:
                print(f"  step {j}: ramify {[str(x) for x in ram]}  base-genus {gb}  span={'PASS' if ok else 'FAIL'}")
            # choose radicand for propagation (span combo if PASS) -> set radval at level j
            if ok:
                sol = M.solve_left(target)
                if randomize:
                    K = M.left_kernel().basis()           # radicand-choice freedom
                    for kv in K:
                        if randint(0,1): sol = sol + kv
                combo = [funcs[t] for t in range(len(funcs)) if sol[t]==1]
            else:
                combo = None
            for b in BR:
                for oid in range(len(places[j][b])):
                    if combo is None:
                        # span failed: radicand = the reduced ramification target itself
                        val[j][b][oid]['radval'] = 1 if b in ramset else 0
                    else:
                        val[j][b][oid]['radval'] = sum(val[j][b][oid].get(f,0) for f in combo)
    return verdicts

def genus_of_level(G, Hj, sb):
    from sage.all import prod
    d = int(libgap.Index(G, Hj))
    pp = level_passport(G, sb['0'], sb['1'], Hj)
    S = sum((d - d//e) for e in pp); return 1 + (S - 2*d)//2

if __name__ == "__main__":
    import sys
    GT = {(8,4,0): "FAIL@2", (16,6,0): "all PASS", (16,6,1): "all PASS"}
    for (o,g,q),exp in GT.items():
        print(f"### [{o},{g}] quo{q}   (Hecke ground truth: {exp}) ###")
        v = run_oracle(o,g,q)
        print("   oracle verdicts:", [(s,'PASS' if ok else 'FAIL') for (s,r,gb,ok) in v])
