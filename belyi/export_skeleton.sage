# Export the tower skeleton of a 2-group Belyi map to JSON for the Hecke.jl solver.
# Keeps the group theory in Sage/GAP (works) and hands Hecke exactly what it needs:
# per level the genus (=> whether an S-unit or Pic^0[2] radicand is needed), and per
# step which of {0,1,oo} ramify (the radicand support).
load("belyi/groups.sage")
import json, sys

def genus_from_passport(d, pp):
    S = sum((d - d // e) for e in pp)          # sum_b (deg - #cycles), #cyc = d/e
    return 1 + (S - 2 * d) // 2

def skeleton(order, gid, quotient_index=0):
    G = libgap.SmallGroup(order, gid)
    struct = str(libgap.StructureDescription(G))
    quos = libgap.GQuotients(libgap.FreeGroup(2), G)
    h = quos[quotient_index]
    fg = libgap.GeneratorsOfGroup(libgap.FreeGroup(2))
    # NB: use generators consistent with the quotient
    F = libgap.FreeGroup(2); fgg = libgap.GeneratorsOfGroup(F)
    quos = libgap.GQuotients(F, G); h = quos[quotient_index]
    s0 = libgap.Image(h, fgg[0]); s1 = libgap.Image(h, fgg[1]); sinf = (s0 * s1)**(-1)
    chain = chief_series_indices(G)
    levels, steps = [], []
    for i in range(len(chain)):
        Hi = chain[i]; d = int(libgap.Index(G, Hi))
        pp = level_passport(G, s0, s1, Hi)
        levels.append({"i": i, "order_Hi": int(libgap.Order(Hi)), "index": int(d),
                       "passport": [int(e) for e in pp],
                       "genus": int(genus_from_passport(d, pp))})
    for i in range(len(chain) - 1):
        rb = step_ramified_branch_points(G, chain[i], chain[i + 1], s0, s1, sinf)
        steps.append({"from": i, "to": i + 1, "ramified_branch_points": rb})
    return {"group": f"[{order},{gid}] {struct}", "degree": order,
            "top_genus": levels[-1]["genus"], "levels": levels, "steps": steps}

if __name__ == "__main__":
    args = sys.argv[1:]
    order = int(args[0]) if args else 8
    gid = int(args[1]) if len(args) > 1 else 4
    sk = skeleton(order, gid)
    out = f"skeletons/{order}_{gid}.json"
    import os; os.makedirs("skeletons", exist_ok=True)
    with open(out, "w") as f:
        json.dump(sk, f, indent=2, default=int)
    print(json.dumps(sk, indent=2, default=int))
    print(f"\nwrote {out}")
