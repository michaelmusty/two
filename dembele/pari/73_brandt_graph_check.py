"""Reconstruct the weighted stable graph independently from the Brandt matrix.

Run with Sage Python for NetworkX, without importing sage.all.
The matrix columns enumerate the three neighbors of a vertex.
"""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import networkx as nx

DATA=Path(__file__).resolve().parents[1]/'data/computed'


def main():
    raw=json.loads((DATA/'stable_graph_brandt.json').read_text())
    matrix,stabs=raw['matrix'],raw['stabilizers']
    assert raw['class_group_proof']=='Minkowski'
    assert len(matrix)==len(stabs)==58
    assert all(sum(matrix[i][j] for i in range(58))==3 for j in range(58))
    assert sum(Fraction(1,e) for e in stabs)==Fraction(1455,32)
    graph=nx.Graph()
    graph.add_nodes_from(range(1,59))
    for i in range(58):
        # A unique diagonal neighbor gives an inverted edge of the
        # Atkin-Lehner quotient, hence only a removable pendant interval.
        assert matrix[i][i] in [0,1]
        for j in range(i+1,58):
            assert (matrix[i][j]>0)==(matrix[j][i]>0)
            if not matrix[i][j]:
                continue
            # At one endpoint there is only one neighbor: consequently
            # there is exactly one edge orbit between these two classes.
            assert min(matrix[i][j],matrix[j][i])==1
            weight=Fraction(stabs[j],matrix[i][j])
            assert weight==Fraction(stabs[i],matrix[j][i])
            assert weight.denominator==1
            graph.add_edge(i+1,j+1,weight=int(weight))
    assert nx.is_connected(graph) and graph.number_of_edges()==73
    initial_edges=[(u,v,d['weight']) for u,v,d in graph.edges(data=True)]
    operations=[]
    while True:
        v=next((v for v in sorted(graph) if graph.degree(v)<3),None)
        if v is None:
            break
        neighbors=list(graph.neighbors(v))
        weights=[graph[v][u]['weight'] for u in neighbors]
        assert len(neighbors) in [1,2]
        graph.remove_node(v)
        operations.append({'vertex':v,'neighbors':neighbors,'weights':weights})
        if len(neighbors)==2:
            assert not graph.has_edge(*neighbors)
            graph.add_edge(*neighbors,weight=sum(weights))
    assert len(graph)==30 and graph.number_of_edges()==45
    assert set(dict(graph.degree()).values())=={3}
    reference=json.loads((DATA/'stable_graph_audit.json').read_text())
    printed=nx.Graph()
    printed.add_weighted_edges_from(reference['edges'])
    matcher=nx.algorithms.isomorphism.GraphMatcher(
        graph,printed,edge_match=nx.algorithms.isomorphism.numerical_edge_match('weight',1))
    assert matcher.is_isomorphic()
    report={'status':'PASS: arithmetic reconstruction is weight-preserving isomorphic to published Figure 2',
            'class_group_proof':raw['class_group_proof'],
            'stabilizer_histogram':dict(Counter(stabs)),
            'diagonal_inverted_edges':sum(matrix[i][i] for i in range(58)),
            'initial_vertices':58,'initial_edges_count':73,
            'initial_edges':initial_edges,'stabilization_operations':operations,
            'stable_vertices':30,'stable_edges_count':45,
            'stable_edges':[(u,v,d['weight']) for u,v,d in graph.edges(data=True)],
            'isomorphism_to_published_labels':matcher.mapping,
            'tree_quotient_involutions':reference['tree_quotient_involutions']}
    (DATA/'brandt_graph_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in
                     ['initial_edges','stabilization_operations','stable_edges']},indent=2))


if __name__=='__main__':
    main()
