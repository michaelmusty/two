"""D105 bounded graph probe; the proposed CM specialization is a hypothesis.

Place one chip at the midpoint of stable edge (9,10), and two at each
midpoint coming from diagonal classes 51,...,58. Test K-D on the unit
subdivision. This calculation does NOT identify the actual CM retraction.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
INPUT = DATA / "hyperellipticity_graph_review_d99.json"
OUT = DATA / "cm_frame_specialization_probe_d105.json"


def source(path):
    p = Path(path).resolve()
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def solve(a, rhs):
    n = len(a)
    a = [[Q(x) for x in row]+[Q(rhs[i])] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        value = a[k][k]
        a[k] = [x/value for x in a[k]]
        for i in range(k+1, n):
            value = a[i][k]
            if value:
                a[i] = [x-value*y for x, y in zip(a[i], a[k])]
    result = [Q(0)]*n
    for i in reversed(range(n)):
        result[i] = a[i][-1]-sum(a[i][j]*result[j] for j in range(i+1, n))
    return result


def laplacian(adj, value):
    return [len(neighbors)*value[i]-sum(value[j] for j in neighbors)
            for i, neighbors in enumerate(adj)]


def burn(adj, divisor, root):
    burned, order = {root}, [root]
    while True:
        added = [i for i in range(len(adj)) if i not in burned and
                 divisor[i] < sum(j in burned for j in adj[i])]
        if not added:
            return burned, order
        burned.update(added)
        order.extend(added)


def reduced(adj, divisor, root):
    n = len(adj)
    ids = [i for i in range(n) if i != root]
    matrix = [[len(adj[i]) if i == j else -int(j in adj[i]) for j in ids] for i in ids]
    rhs = [len(adj[i])-divisor[i] for i in ids]
    rational = solve(matrix, rhs)
    potential = [0]*n
    for i, value in zip(ids, rational):
        potential[i] = value.__floor__()
    delta = laplacian(adj, potential)
    current = [d+v for d, v in zip(divisor, delta)]
    assert all(current[i] >= 0 for i in ids)
    operations = 0
    while True:
        burned, order = burn(adj, current, root)
        if len(burned) == n:
            break
        unburned = set(range(n))-burned
        for i in unburned:
            potential[i] -= 1
        indicator = [int(i in unburned) for i in range(n)]
        step = laplacian(adj, indicator)
        current = [d-v for d, v in zip(current, step)]
        assert all(current[i] >= 0 for i in ids)
        operations += 1
        assert operations < 100000, "Bound the discovery loop."
    assert current == [d+v for d, v in zip(divisor, laplacian(adj, potential))]
    return {"q_reduced": current, "root_coefficient": current[root],
            "integer_potential": potential, "burn_order": order,
            "firing_steps": operations,
            "effective_representative_exists": current[root] >= 0}


def build():
    graph = json.loads(INPUT.read_text())
    originals = graph["stable_vertices"]
    vertices = [f"v{v}" for v in originals]
    index = {v: i for i, v in enumerate(originals)}
    edges, midpoints = [], {}
    marked_pairs = {(39,45), (40,46), (41,47), (42,48),
                    (39,49), (40,50), (41,43), (42,44)}
    for u, v, weight in graph["stable_edges"]:
        length = Q(weight)
        assert length.denominator == 1
        length = int(length)
        chain = [index[u]]
        for k in range(1, length):
            chain.append(len(vertices))
            vertices.append(f"e{u}_{v}_{k}")
        chain.append(index[v])
        edges += list(zip(chain, chain[1:]))
        if (u, v) in marked_pairs or (u, v) == (9, 10):
            assert length % 2 == 0
            midpoints[(u, v)] = chain[length//2]
    assert len(midpoints) == 9
    adj = [[] for _ in vertices]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    assert len(edges)-len(vertices)+1 == 16
    root = midpoints[(9, 10)]
    marked = [0]*len(vertices)
    marked[root] = 1
    for pair in marked_pairs:
        marked[midpoints[pair]] = 2
    canonical = [len(neighbors)-2 for neighbors in adj]
    divisor = [k-d for k, d in zip(canonical, marked)]
    assert sum(marked) == 17 and sum(canonical) == 30 and sum(divisor) == 13
    result = reduced(adj, divisor, root)
    # Controls: a degree-negative divisor cannot be effective; zero can.
    negative = [0]*len(vertices)
    negative[root] = -1
    negative_check = reduced(adj, negative, root)
    zero_check = reduced(adj, [0]*len(vertices), root)
    assert not negative_check["effective_representative_exists"]
    assert zero_check["effective_representative_exists"]
    return {"status": "pass", "milestone": "D105", "scope": "Conditional tropical probe only",
            "vertices": vertices, "unit_edges": edges, "root_index": root,
            "hypothetical_marked_divisor": marked, "canonical_minus_marked": divisor,
            "reduction": result, "controls": {"negative_degree_rejected": True, "zero_accepted": True},
            "actual_CM_specialization_proved": False,
            "actual_CM_frame_nonspeciality_proved": False,
            "sources": [source(Path(__file__)), source(INPUT)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        for item in old["sources"]:
            assert source(item["path"]) == item
    result = build()
    # JSON normalizes tuple edge pairs to lists.
    result = json.loads(json.dumps(result))
    if args.check:
        assert result == old
    else:
        assert not OUT.exists()
        OUT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "pass", "root_coefficient": result["reduction"]["root_coefficient"],
                      "effective_representative_exists": result["reduction"]["effective_representative_exists"],
                      "firing_steps": result["reduction"]["firing_steps"],
                      "actual_CM_specialization_proved": False}), flush=True)
    print("PASS|D105_SPECIALIZATION_PROBE", flush=True)


if __name__ == "__main__":
    main()
