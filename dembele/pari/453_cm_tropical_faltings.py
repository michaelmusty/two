"""D118: exact tropical moment of the known reduction graph.

Uses de Jong--Shokrieh's tau/moment formula. The companion proof explains
the metric normalization and its contribution to the Faltings lower bound.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def inverse(matrix):
    n=len(matrix);a=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if a[i][k]);a[k],a[pivot]=a[pivot],a[k]
        c=a[k][k];a[k]=[x/c for x in a[k]]
        for i in range(n):
            if i==k or not a[i][k]:continue
            c=a[i][k];a[i]=[x-c*y for x,y in zip(a[i],a[k])]
    return [row[n:] for row in a]

def graph_data(vertices,edges):
    indices={v:i for i,v in enumerate(vertices)};n=len(vertices)
    L=[[Q(0)]*n for _ in vertices]
    for u,v,length in edges:
        i,j=indices[u],indices[v];c=1/Q(length)
        L[i][i]+=c;L[j][j]+=c;L[i][j]-=c;L[j][i]-=c
    reduced=[row[:-1] for row in L[:-1]];inv=inverse(reduced)
    G=[row+[Q(0)] for row in inv]+[[Q(0)]*n]
    R=[[G[i][i]+G[j][j]-2*G[i][j] for j in range(n)] for i in range(n)]
    assert all(R[i][j]>=0 and R[i][j]==R[j][i] for i in range(n) for j in range(n))
    assert sum(R[indices[u]][indices[v]]/Q(length) for u,v,length in edges)==n-1
    tau=[]
    for q in range(n):
        total=Q(0)
        for u,v,length in edges:
            i,j=indices[u],indices[v];ell=Q(length);F=1-R[i][j]/ell
            total+=ell*F*F/12+(R[i][q]-R[j][q])**2/(4*ell)
        tau.append(total)
    assert len(set(tau))==1
    length=sum(Q(e[2]) for e in edges);moment=length/8-tau[0]/2
    assert moment>=0
    return {'vertices':vertices,'edges':[[u,v,str(l)] for u,v,l in edges],
            'ground_vertex':vertices[-1],
            'grounded_laplacian':[[str(x) for x in row] for row in reduced],
            'grounded_laplacian_inverse':[[str(x) for x in row] for row in inv],
            'effective_resistances':[[str(x) for x in row] for row in R],
            'Foster_sum':n-1,'all_vertex_tau_values':list(map(str,tau)),
            'total_length':str(length),'tau':str(tau[0]),'tropical_moment':str(moment)}

def build():
    graph=json.loads((DATA/'hyperellipticity_graph_review_d99.json').read_text())
    current=graph_data(graph['stable_vertices'],[(u,v,Q(w)) for u,v,w in graph['stable_edges']])
    assert len(current['vertices'])==30 and len(current['edges'])==45
    controls=[]
    for name,vertices,edges,expected in [
        ('interval',[0,1],[(0,1,1)],Q(0)),
        ('circle subdivided into three edges',[0,1,2],[(0,1,1),(1,2,1),(2,0,1)],Q(1,4)),
        ('three-edge banana',[0,1],[(0,1,1)]*3,Q(5,18))]:
        answer=graph_data(vertices,edges);assert Q(answer['tropical_moment'])==expected
        controls.append({'name':name,'tau':answer['tau'],'moment':answer['tropical_moment']})
    normalized=Q(current['tropical_moment'])/8
    print('TROPICAL_FALTINGS|'+json.dumps({'length':current['total_length'],'tau':current['tau'],
          'moment':current['tropical_moment'],'normalized_coefficient_log2':str(normalized)}),flush=True)
    return {'status':'pass','milestone':'D118','graph':current,'controls':controls,
            'dyadic_tropical_Faltings_contribution_coefficient_log2':str(normalized),
            'Faltings_lower_bound_formula':'-16*log(pi)-8*log(2)+tropical_moment*log(2)/8',
            'curve_L2_and_Jacobian_Faltings_metrics_agree_via_companion_proof':True,
            'archimedean_theta_and_Neron_Tate_terms_discarded_by_nonnegativity':True,
            'other_finite_tropical_terms_discarded_by_nonnegativity':True,
            'candidate_curve_used':False,'new_reduction_graph_computed':False,
            'sources':[source(p) for p in [Path(__file__),DATA/'hyperellipticity_graph_review_d99.json',
                ROOT/'dembele/certificates/hyperellipticity-review-d99.md',
                ROOT/'dembele/certificates/cm-adjugate-height-d103.md']]}

if __name__=='__main__':
    out=DATA/'cm_tropical_faltings_d118.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|453_CM_TROPICAL_FALTINGS',flush=True)
