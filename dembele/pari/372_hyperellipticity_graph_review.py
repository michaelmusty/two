"""D99: rebuild the graph from fresh Brandt data, using only standard Python.

The main obstruction checks every deletion of at most two edges. A separate
exhaustive distance-preserving search enumerates automorphisms, without Sage,
NetworkX, or the previous graph output. See the D99 report for the theorem.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
INPUT = DATA / "hyperellipticity_fresh_brandt_d99.json"
OUTPUT = DATA / "hyperellipticity_graph_review_d99.json"

# Figure 2, arXiv:1906.06772v2, p.19. Rechecked against the PDF image.
# This is a comparison only: the obstruction below runs on the Brandt graph.
FIGURE = [
    (1,2,12),(1,3,3),(1,5,3),(2,4,3),(2,14,3),
    (3,6,1),(3,10,2),(4,7,1),(4,11,2),(5,8,1),(5,12,2),
    (6,15,1),(6,19,1),(7,16,1),(7,20,1),(8,17,1),(8,21,1),
    (9,14,1),(9,18,1),(9,22,1),(10,26,2),(10,30,2),
    (11,23,2),(11,27,2),(12,24,2),(12,28,2),
    (13,14,2),(13,25,2),(13,29,2),(15,23,1),(15,27,1),
    (16,24,1),(16,28,1),(17,25,1),(17,29,1),
    (18,26,1),(18,30,1),(19,24,1),(19,28,1),
    (20,25,1),(20,29,1),(21,26,1),(21,30,1),
    (22,23,1),(22,27,1),
]


def source(path):
    return {"path": str(Path(path).resolve()),
            "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}


def components(vertices, edges, removed=()):
    adj = {v: [] for v in vertices}
    removed = set(removed)
    for i, (u, v, *_) in enumerate(edges):
        if i not in removed:
            adj[u].append(v)
            adj[v].append(u)
    todo = set(vertices)
    out = []
    while todo:
        start = min(todo)
        todo.remove(start)
        found, queue = [start], [start]
        while queue:
            for v in adj[queue.pop()]:
                if v in todo:
                    todo.remove(v)
                    found.append(v)
                    queue.append(v)
        out.append(sorted(found))
    return out


def summary(vertices, edges):
    cc = components(vertices, edges)
    assert len(cc) == 1
    return {"vertices": len(vertices), "edges": len(edges),
            "betti": len(edges)-len(vertices)+1}


def stabilize(vertices, edges):
    vertices = set(vertices)
    live = {i: (u,v,Fraction(w),[i]) for i,(u,v,w) in enumerate(edges)}
    next_id = len(live)
    operations = []
    while True:
        stars = {v: [] for v in vertices}
        for i,(u,v,w,path) in live.items():
            assert u != v
            stars[u].append(i)
            stars[v].append(i)
        small = [v for v in sorted(vertices) if len(stars[v]) < 3]
        if not small:
            break
        v = small[0]
        ids = stars[v]
        assert len(ids) in (1,2)
        old = [live.pop(i) for i in ids]
        neighbors = [b if a == v else a for a,b,_,_ in old]
        op = {"vertex":v,"removed_edges":ids,"neighbors":neighbors,
              "weights":[str(e[2]) for e in old]}
        vertices.remove(v)
        if len(ids) == 2:
            assert neighbors[0] != neighbors[1]
            assert all(set(e[:2]) != set(neighbors) for e in live.values())
            path = old[0][3]+old[1][3]
            live[next_id] = (*neighbors,old[0][2]+old[1][2],path)
            op["added_edge"] = next_id
            next_id += 1
        operations.append(op)
    ordered = sorted((min(u,v),max(u,v),w,sorted(path))
                     for u,v,w,path in live.values())
    return sorted(vertices), [(u,v,w) for u,v,w,_ in ordered], operations, [
        {"edge":[u,v],"weight":str(w),"original_edge_ids":path}
        for u,v,w,path in ordered]


def distances(vertices, edges):
    adj = {v: {} for v in vertices}
    for u,v,w in edges:
        assert u != v and v not in adj[u]
        adj[u][v] = adj[v][u] = w
    dist = {}
    for v in vertices:
        d, queue = {v:0}, deque([v])
        while queue:
            u = queue.popleft()
            for z in adj[u]:
                if z not in d:
                    d[z] = d[u]+1
                    queue.append(z)
        assert len(d) == len(vertices)
        dist[v] = d
    return adj, dist


def isomorphisms(v1,e1,v2,e2,weighted=False):
    """Exhaustive bijection search; all pruning conditions are necessary."""
    a,d = distances(v1,e1)
    b,f = distances(v2,e2)
    def signature(v, adj, dist):
        ans = (tuple(sorted(dist[v].values())),)
        if weighted:
            ans += (tuple(sorted(adj[v].values())),)
        return ans
    domains = {v:[w for w in v2 if signature(v,a,d)==signature(w,b,f)] for v in v1}
    mapping, used = {}, set()
    def search():
        if len(mapping) == len(v1):
            assert all((z in a[v]) == (mapping[z] in b[mapping[v]]) for v in v1 for z in v1)
            yield dict(mapping)
            return
        choices = []
        for v in v1:
            if v in mapping:
                continue
            candidates = [w for w in domains[v] if w not in used and all(
                d[v][x] == f[w][y] and
                (not weighted or x not in a[v] or a[v][x] == b[w][y])
                for x,y in mapping.items())]
            if not candidates:
                return
            choices.append((len(candidates),v,candidates))
        _,v,candidates = min(choices)
        for w in candidates:
            mapping[v] = w
            used.add(w)
            yield from search()
            used.remove(w)
            del mapping[v]
    yield from search()


def quotient(vertices, edges, perm):
    """Compare Chan's contracted quotient with the topological quotient.

    Input is simple. Parallel quotient edges are retained separately.
    """
    assert all(perm[perm[v]] == v for v in vertices)
    orbit = {v:min(v,perm[v]) for v in vertices}
    qv = set(orbit.values())
    qt = set(qv)
    qe, te = [], []
    seen = set()
    fixed_v = sum(perm[v] == v for v in vertices)
    fixed_e = inverted = 0
    midpoint = max(vertices)+1
    for u,v,w in edges:
        e = tuple(sorted((u,v)))
        mate = tuple(sorted((perm[u],perm[v])))
        if e in seen:
            continue
        seen.update((e,mate))
        if orbit[u] == orbit[v]:
            assert perm[u] == v and perm[v] == u
            inverted += 1
            qt.add(midpoint)
            te.append((orbit[u],midpoint,1))
            midpoint += 1
        else:
            if e == mate:
                assert perm[u] == u and perm[v] == v
                fixed_e += 1
            qe.append((orbit[u],orbit[v],1))
            te.append((orbit[u],orbit[v],1))
    qs,ts = summary(qv,qe),summary(qt,te)
    numerator = len(edges)+fixed_e-inverted-len(vertices)-fixed_v
    assert numerator % 2 == 0
    assert qs["betti"] == ts["betti"] == numerator//2+1
    return {"permutation":[perm[v] for v in vertices],"fixed_vertices":fixed_v,
            "fixed_edges":fixed_e,"inverted_edges":inverted,
            "chan_quotient":qs,"topological_quotient":ts}


def cut_check(vertices, edges):
    histogram = Counter()
    checks = []
    for size in (1,2):
        for ids in combinations(range(len(edges)),size):
            count = len(components(vertices,edges,ids))
            histogram[count] += 1
            checks.append([list(ids),count])
    return {"deletions_tested":len(checks),
            "component_count_histogram":dict(sorted(histogram.items())),
            "checks":checks}


def review():
    raw = json.loads(INPUT.read_text())
    T,e = raw["matrix"],raw["stabilizers"]
    n = len(e)
    assert n == 58 and len(T)==n and all(len(row)==n for row in T)
    assert raw["class_group_proof"] == "Minkowski"
    assert (raw["class_number"],raw["narrow_class_number"],raw["residue_norm"]) == (1,1,2)
    assert all(type(x) is int and x>=0 for row in T for x in row)
    assert all(sum(T[i][j] for i in range(n))==3 for j in range(n))
    assert all(e[i]*T[i][j]==e[j]*T[j][i] for i in range(n) for j in range(n))
    assert sum(Fraction(1,x) for x in e)==Fraction(1455,32)==Fraction(raw["zeta_minus_one"],128)
    upstairs, ordinary, diagonal = [], [], []
    for i in range(n):
        assert T[i][i] in (0,1)
        if T[i][i]:
            diagonal.append(i+1)
            upstairs.append((i+1,i+1+n,Fraction(e[i])))
        for j in range(i+1,n):
            if T[i][j]:
                assert min(T[i][j],T[j][i])==1
                w = Fraction(e[j],T[i][j])
                assert w == Fraction(e[i],T[j][i]) and w.denominator==1
                ordinary.append((i+1,j+1,w))
                upstairs.extend(((i+1,j+1+n,w),(j+1,i+1+n,w)))
    uv = list(range(1,2*n+1))
    flip = {v:v+n if v<=n else v-n for v in uv}
    ud = {tuple(sorted((u,v))):w for u,v,w in upstairs}
    assert all(ud[tuple(sorted((flip[u],flip[v])))]==w for u,v,w in upstairs)
    upstairs_quotient = quotient(uv,upstairs,flip)
    assert summary(uv,upstairs)=={"vertices":116,"edges":155,"betti":40}
    assert len(diagonal)==9
    assert upstairs_quotient["chan_quotient"]=={"vertices":58,"edges":73,"betti":16}
    assert upstairs_quotient["topological_quotient"]=={"vertices":67,"edges":82,"betti":16}
    # Keep the fixed midpoint of each inverted edge until stabilization.
    topological = ordinary+[(v,n+1+i,Fraction(e[v-1],2)) for i,v in enumerate(diagonal)]
    tv = list(range(1,n+len(diagonal)+1))
    sv,se,operations,paths = stabilize(tv,topological)
    assert summary(sv,se)=={"vertices":30,"edges":45,"betti":16}
    adj,dist = distances(sv,se)
    assert all(len(adj[v])==3 for v in sv)
    cuts = cut_check(sv,se)
    assert cuts["deletions_tested"]==1035 and cuts["component_count_histogram"]=={1:1035}
    witness_v = sv[0]
    witness = [i for i,(u,v,w) in enumerate(se) if witness_v in (u,v)]
    witness_cc = components(sv,se,witness)
    assert len(witness)==3 and len(witness_cc)==2 and [witness_v] in witness_cc
    autos = list(isomorphisms(sv,se,sv,se))
    assert len(autos)==64
    assert len({tuple(p[v] for v in sv) for p in autos})==64
    assert all(all(adj[u][v]==adj[p[u]][p[v]] for u,v,w in se) for p in autos)
    involutions = [quotient(sv,se,p) for p in autos
                   if any(p[v]!=v for v in sv) and all(p[p[v]]==v for v in sv)]
    hist = Counter(q["chan_quotient"]["betti"] for q in involutions)
    assert len(involutions)==19 and hist=={8:5,10:4,12:6,14:4}
    figiso = next(isomorphisms(sv,se,list(range(1,31)),FIGURE,weighted=True))
    assert len(figiso)==30
    # A positive control with inverted edges and a pointwise fixed bridge.
    dumbbell = [(0,1,1),(1,2,1),(2,0,1),(0,3,1),(3,4,1),(4,5,1),(5,3,1)]
    dp = {0:0,1:2,2:1,3:3,4:5,5:4}
    dq = quotient(list(range(6)),dumbbell,dp)
    assert dq["chan_quotient"]["betti"]==0 and dq["inverted_edges"]==2 and dq["fixed_edges"]==1
    assert len(components(range(6),dumbbell,[3]))==2
    k4 = [(u,v,1) for u,v in combinations(range(4),2)]
    ka = list(isomorphisms(range(4),k4,range(4),k4))
    kq = [quotient(range(4),k4,p) for p in ka if any(p[v]!=v for v in range(4))
          and all(p[p[v]]==v for v in range(4))]
    assert len(ka)==24 and len(kq)==9 and all(q["chan_quotient"]["betti"]>0 for q in kq)
    assert cut_check(range(4),k4)["component_count_histogram"]=={1:21}
    # The >=3 vertices hypothesis is essential: a three-edge banana has a
    # tree quotient under swapping its two vertices and reversing each edge.
    banana = [(0,1,1)]*3
    assert cut_check(range(2),banana)["component_count_histogram"]=={1:6}
    banana_topological = summary(range(4),[(0,1,1),(0,2,1),(0,3,1)])
    assert banana_topological["betti"]==0
    return {"status":"PASS","sources":[source(__file__),source(INPUT)],
            "algorithm":"standard-Python exhaustive one/two-edge cuts and distance-constrained bijections",
            "mass":str(sum(Fraction(1,x) for x in e)),
            "stabilizer_histogram":dict(sorted(Counter(e).items())),
            "upstairs":summary(uv,upstairs),"upstairs_quotient":upstairs_quotient,
            "diagonal_classes":diagonal,
            "quotient_edges":[[u,v,str(w)] for u,v,w in topological],
            "stabilization":operations,"stable_paths":paths,
            "stable_vertices":sv,"stable_edges":[[u,v,str(w)] for u,v,w in se],
            "stable_summary":summary(sv,se),"cut_check":cuts,
            "edge_connectivity":3,"three_edge_cut_witness":witness,
            "three_edge_cut_components":witness_cc,
            "automorphisms":[[p[v] for v in sv] for p in autos],
            "involutions":involutions,"quotient_betti_histogram":dict(sorted(hist.items())),
            "weighted_isomorphism_to_figure":figiso,
            "controls":{"dumbbell":dq,"K4_automorphisms":24,"K4_involutions":9,
                        "K4_quotient_betti_histogram":dict(sorted(Counter(q["chan_quotient"]["betti"] for q in kq).items())),
                        "two_vertex_banana_tree_quotient":banana_topological},
            "conclusion":"No positive edge lengths make this stable graph hyperelliptic.",
            "scope":"The identification with C and the specialization/metric-graph theorems are mathematical inputs; candidate equations are not read."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args = parser.parse_args()
    result = review()
    serialized = json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.check:
        assert json.loads(serialized)==json.loads(OUTPUT.read_text())
    else:
        with OUTPUT.open("x") as f:
            f.write(serialized)
    print("PASS|372_HYPERELLIPTICITY_GRAPH_REVIEW|1035 cuts|64 automorphisms|19 involutions|no tree quotient")


if __name__ == "__main__":
    main()
