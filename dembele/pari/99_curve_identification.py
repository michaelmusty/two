"""D62: audit the quaternion/order and the full Cerednik--Drinfeld graph.

The geometric theorem is explained separately in curve-identification-audit.md.
This script does not infer that theorem from graph counts or rerun the graph
automorphism enumeration. Run with Sage Python.
"""
import importlib.util
import json
from pathlib import Path

import networkx as nx
from sage.all import AA, GF, NumberField, PolynomialRing, QQ, QuaternionAlgebra, matrix


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("cm_orbit", Path(__file__).with_name("96_cm_orbit.py"))
orbit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orbit)


def upstairs_graph(brandt, stabilizers):
    """One edge for each nonzero oriented class pair, not each neighbor.

    min(T_ij,T_ji)=1 certifies uniqueness of the edge orbit. A diagonal
    entry 1 is ONE edge between opposite layers, reversed by w_p.
    """
    n = len(brandt)
    assert len(stabilizers) == n and all(len(row) == n for row in brandt)
    assert all(sum(brandt[i][j] for i in range(n)) == 3 for j in range(n))
    graph = nx.Graph()
    graph.add_nodes_from(range(2*n))
    for i in range(n):
        for j in range(n):
            assert brandt[i][j] >= 0
            assert stabilizers[i]*brandt[i][j] == stabilizers[j]*brandt[j][i]
            if not brandt[i][j]:
                continue
            assert min(brandt[i][j], brandt[j][i]) == 1
            weight = QQ(stabilizers[j])/brandt[i][j]
            assert weight.denominator() == 1
            graph.add_edge(i, n+j, weight=int(weight))
    return graph


def atkin_lehner_quotient(graph):
    """Keep reversed edges as pendant intervals until stabilization.

    This acts on the actual bipartite graph; it never deletes arbitrary
    self-loops in an arbitrary quotient graph.
    """
    n = len(graph)//2
    flip = lambda v: (v+n) % (2*n)
    quotient = nx.Graph()
    quotient.add_nodes_from(range(n))
    reversed_edges = []
    for u, v, d in graph.edges(data=True):
        assert graph.has_edge(flip(u), flip(v))
        assert graph[flip(u)][flip(v)]["weight"] == d["weight"]
        if {u,v} == {flip(u),flip(v)}:
            midpoint = n+len(reversed_edges)
            quotient.add_edge(u % n, midpoint, weight=QQ(d["weight"])/2)
            reversed_edges.append([u,v,d["weight"]])
        elif not quotient.has_edge(u % n, v % n):
            quotient.add_edge(u % n, v % n, weight=QQ(d["weight"]))
    return quotient, reversed_edges


def stabilize(graph):
    graph = graph.copy()
    steps = []
    while True:
        v = next((v for v in sorted(graph) if graph.degree(v) < 3), None)
        if v is None:
            break
        neighbors = list(graph[v])
        assert len(neighbors) in (1,2)
        weights = [graph[v][w]["weight"] for w in neighbors]
        graph.remove_node(v)
        steps.append({"vertex":v,"neighbors":neighbors,"lengths":[str(w) for w in weights]})
        if len(neighbors) == 2:
            assert not graph.has_edge(*neighbors)
            graph.add_edge(*neighbors, weight=sum(weights))
    return graph, steps


def exact_order_check(raw):
    ring = PolynomialRing(QQ, "s")
    s = ring.gen()
    field = NumberField(s**8-8*s**6+20*s**4-16*s**2+2, "b")
    b = field.gen()
    algebra = QuaternionAlgebra(field,b-b*b,-1)
    basis = [algebra([field([QQ(c) for c in v[8*j:8*(j+1)]])
                      for j in range(4)]) for v in raw["order_basis"]]
    coords = lambda q: sum([list(c.vector()) for c in q.coefficient_tuple()], [])
    lattice = matrix(QQ,[coords(q) for q in basis]).transpose()
    inverse = lattice.inverse()
    assert all(c in QQ and c.denominator() == 1
               for x in basis for y in basis for c in (inverse*matrix(QQ,32,1,coords(x*y))).list())
    trace_gram = matrix(QQ,[[(x*y).reduced_trace().trace() for y in basis] for x in basis])
    determinant = abs(trace_gram.det())
    discr = algebra.discriminant()
    assert discr.norm() == 2 and determinant == field.discriminant()**4*discr.norm()**2
    places = field.embeddings(AA)
    split = [i for i,v in enumerate(places) if v(b-b*b)>0]
    assert len(split)==1 and 0 < places[split[0]](b) < 1
    # Full unit signatures imply every totally positive unit is a square.
    units = field.unit_group(proof=True).gens_values()
    signatures = matrix(GF(2),[[int(v(u)<0) for v in places] for u in units])
    assert signatures.rank()==8
    assert field.class_number(proof=True)==1
    return {
        "field_discriminant":int(field.discriminant()),
        "algebra_finite_discriminant_norm":int(discr.norm()),
        "real_split_index_ascending":split[0],
        "real_split_b":str(places[split[0]](b)),
        "saved_order_closed_under_products":True,
        "absolute_reduced_trace_gram_determinant":str(determinant),
        "maximal_order_discriminant_formula_matches":True,
        "class_number_proved":1,"unit_signature_rank":8,
        "unit_generators":[str(u) for u in units],
        "unit_signature_rows":[[int(c) for c in row] for row in signatures.rows()],
    }


def main():
    raw = orbit.export_quaternions(orbit.arithmetic.GP)
    order = exact_order_check(raw)
    source = json.loads((DATA/"stable_graph_brandt.json").read_text())
    assert source["class_group_proof"]=="Minkowski"
    graph = upstairs_graph(source["matrix"], source["stabilizers"])
    assert nx.is_connected(graph) and len(graph)==116 and graph.number_of_edges()==155
    genus = graph.number_of_edges()-len(graph)+1
    assert genus==40
    quotient, reversed_edges = atkin_lehner_quotient(graph)
    assert len(reversed_edges)==9 and len(quotient)==67 and quotient.number_of_edges()==82
    assert nx.is_connected(quotient) and quotient.number_of_edges()-len(quotient)+1==16
    stable, steps = stabilize(quotient)
    previous = json.loads((DATA/"brandt_graph_check.json").read_text())
    expected = nx.Graph()
    expected.add_weighted_edges_from(previous["stable_edges"])
    assert nx.is_isomorphic(stable,expected,edge_match=lambda a,b:a["weight"]==b["weight"])
    assert len(stable)==30 and stable.number_of_edges()==45
    trace = 1-len(reversed_edges)  # trace C0=0, trace C1=-9, trace H0=1.
    assert trace==-8 and (genus+trace)//2==16 and (genus-trace)//2==24
    paths = [Path(__file__), Path(__file__).with_name("96_cm_orbit.py"),
             DATA/"normalizer_domain.bin", DATA/"stable_graph_brandt.json",
             DATA/"brandt_graph_check.json", DATA/"stable_graph_audit.json"]
    report = {
        "status":"PASS: exact datum and full-graph audit; geometric argument in companion report",
        "order":order,
        "upstairs":{"vertices":116,"edges":155,"genus":40},
        "atkin_lehner":{"fixed_vertices":0,"reversed_edges":reversed_edges,
                         "homology_trace":trace,"plus_dimension":16,"minus_dimension":24},
        "quotient_with_midpoints":{"vertices":67,"edges":82,"genus":16},
        "stable":{"vertices":30,"edges":45,"genus":16,
                  "agrees_with_D45_weighted_graph":True},
        "stabilization_steps":steps,
        "sources":[orbit.arithmetic.source(p) for p in paths],
    }
    text = json.dumps(report,indent=2)+"\n"
    (DATA/"curve_identification.json").write_text(text)
    (DATA/"curve_identification.out").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
