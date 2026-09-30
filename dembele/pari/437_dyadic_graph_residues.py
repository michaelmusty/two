"""D116: compare invariant integer cocycles with stabilizer-weighted graph flows.

The arithmetic stable-model residue interpretation is a separate theorem;
this source certifies the finite graph, edge weights and integral change matrix.
"""
from collections import deque
from fractions import Fraction as Q
import importlib.util
import json
from math import lcm,prod
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('saturation',ROOT/'dembele/pari/436_dyadic_harmonic_saturation.py')
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)

def determinant(a):
    a=[list(map(Q,row)) for row in a];result=Q(1);n=len(a)
    for k in range(n):
        i=next(i for i in range(k,n) if a[i][k])
        if i!=k:a[k],a[i]=a[i],a[k];result=-result
        pivot=a[k][k];result*=pivot
        for i in range(k+1,n):
            ratio=a[i][k]/pivot
            for j in range(k+1,n):a[i][j]-=ratio*a[k][j]
    return result

def build():
    path=DATA/'dyadic_harmonic_certificate_d111.json';p=json.loads(path.read_text())
    orbits=p['oriented_edge_orbits'];which={e:i for i,orb in enumerate(orbits) for e in orb}
    rev=[which[p['edges'][orb[0]]['reverse_edge']] for orb in orbits]
    edges=[]
    for i,orb in enumerate(orbits):
        if i>=rev[i]:continue
        e=orb[0];row=p['edges'][e];v=row['source_class'];w=row['target_class'];line=row['line']
        stabilizers=p['ideal_checks'][v]['stabilizer_permutations']
        weight=sum(perm[line]==line for perm in stabilizers)
        other=p['edges'][orbits[rev[i]][0]];perms=p['ideal_checks'][w]['stabilizer_permutations']
        assert weight==sum(perm[other['line']]==other['line'] for perm in perms)
        assert len(stabilizers)==weight*len(orb)
        edges.append({'source':v,'target':w,'representative_slot':e,'edge_stabilizer_order':weight})
    assert len(edges)==73
    B=p['harmonic_basis'];flows=[[Q(row[e['representative_slot']],e['edge_stabilizer_order']) for e in edges] for row in B]
    assert all(sum((int(e['source']==v)-int(e['target']==v))*x for e,x in zip(edges,row))==0
               for row in flows for v in range(58))
    parent=list(range(58));tree=[];chords=[];adj=[[] for _ in range(58)]
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    for k,e in enumerate(edges):
        u,v=e['source'],e['target'];a,b=find(u),find(v)
        if a==b:chords.append(k)
        else:parent[a]=b;tree.append(k);adj[u].append((v,k,1));adj[v].append((u,k,-1))
    assert len(tree)==57 and len(chords)==16 and len({find(i) for i in range(58)})==1
    cycles=[]
    for chord in chords:
        e=edges[chord];start,end=e['target'],e['source'];previous={start:None};queue=deque([start])
        while end not in previous:
            u=queue.popleft()
            for v,k,sign in adj[u]:
                if v not in previous:previous[v]=(u,k,sign);queue.append(v)
        cycle=[0]*73;cycle[chord]=1;v=end
        while previous[v] is not None:
            u,k,sign=previous[v];cycle[k]=sign;v=u
        cycles.append(cycle)
    coordinates=[[row[j] for j in chords] for row in flows]
    assert all(sum(coordinates[i][k]*cycles[k][j] for k in range(16))==flows[i][j]
               for i in range(16) for j in range(73))
    denominator=lcm(*(x.denominator for row in coordinates for x in row))
    integer=[[int(x*denominator) for x in row] for row in coordinates]
    diagonal,_,_,operations=h.smith(integer);det=determinant(coordinates)
    assert abs(det)==Q(prod(diagonal),denominator**16)
    equal=denominator==1 and diagonal==[1]*16
    print('WEIGHTED_GRAPH_RESIDUES|denominator='+str(denominator)+'|det='+str(det)+'|equal_lattices='+str(equal),flush=True)
    return {'status':'pass','milestone':'D116','quotient_vertices':58,'quotient_edges':edges,
       'spanning_tree_edges':tree,'chord_edges':chords,'fundamental_integer_cycles':cycles,
       'harmonic_to_cycle_coordinates':[[str(x) for x in row] for row in coordinates],
       'coordinate_denominator':denominator,'coordinate_determinant':str(det),
       'integer_coordinate_Smith_factors':diagonal,'integer_coordinate_Smith_operations':operations,
       'weighted_harmonic_lattice_equals_integer_cycle_lattice':equal,
       'stable_dualizing_interpretation_machine_verified':False,
       'residue_frame_index_computed':False,'candidate_identification_proved':False,
       'sources':[h.source(x) for x in [Path(__file__),Path(h.__file__),path,
         ROOT/'dembele/certificates/hyperellipticity-review-d99.md']]}

if __name__=='__main__':
    result=build();out=DATA/'dyadic_graph_residues_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|437_DYADIC_GRAPH_RESIDUES',flush=True)
