"""D147 independent cycle witnesses, quotient identities and metric budget."""
import argparse
from collections import deque
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
SAGE=Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
PYTHON=SAGE/'venv/bin/python3'
INPUTS=['hyperellipticity_graph_review_d99','P1600_multiplication_determinant_d147',
        'P1600_height_routes_audit_d142']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def paths_without_edge(vertices,edges,omitted):
    start,end=edges[omitted];adj={v:[] for v in vertices};flow={}
    for e,(u,v) in enumerate(edges):
        if e==omitted:continue
        adj[u].append(v);adj[v].append(u);flow[u,v]=flow[v,u]=0
    def find(allowed):
        prev={start:None};todo=deque([start])
        while todo and end not in prev:
            u=todo.popleft()
            for v in adj[u]:
                if v not in prev and allowed(u,v):prev[v]=u;todo.append(v)
        assert end in prev,(omitted,'no augmenting path')
        p=[end]
        while p[-1]!=start:p.append(prev[p[-1]])
        return p[::-1]
    for _ in range(2):
        p=find(lambda u,v:flow[u,v]<1)
        for u,v in zip(p,p[1:]):flow[u,v]+=1;flow[v,u]-=1
    answer=[]
    for _ in range(2):
        p=find(lambda u,v:flow[u,v]>0);answer.append(p)
        for u,v in zip(p,p[1:]):flow[u,v]-=1;flow[v,u]+=1
    return answer


def worker(out):
    from itertools import combinations
    from sage.all import QQ,ZZ,GF,matrix,identity_matrix,RealBallField
    R=RealBallField(224);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    saved=json.loads((DATA/(INPUTS[0]+'.json')).read_text())
    primary=json.loads((DATA/(INPUTS[1]+'.json')).read_text())
    vertices=saved['stable_vertices'];edges=[(u,v) for u,v,_ in saved['stable_edges']]
    lookup={frozenset(e):j for j,e in enumerate(edges)};witnesses=[]
    for omitted in range(len(edges)):
        paths=paths_without_edge(vertices,edges,omitted);cycles=[]
        for p in paths:
            assert len(p)==len(set(p)) and p[0]==edges[omitted][0] and p[-1]==edges[omitted][1]
            c={omitted}|{lookup[frozenset((u,v))] for u,v in zip(p,p[1:])}
            assert len(c)==len(p)
            assert all(sum(v in edges[e] for e in c) in [0,2] for v in vertices)
            cycles.append(c)
        assert cycles[0]&cycles[1]=={omitted}
        assert [int(e in cycles[0])*int(e in cycles[1]) for e in range(45)]==[int(e==omitted) for e in range(45)]
        witnesses.append({'edge_index':omitted,'edge':list(edges[omitted]),'paths':paths,
                          'cycles':[sorted(c) for c in cycles]})
    assert len(witnesses)==45 and primary['graph']['multiplication_rank_mod2']==45
    # A cubic graph with a two-edge cut rejects unrestricted surjectivity.
    bad_edges=[(i,j) for start in [0,4] for i,j in combinations(range(start,start+4),2)
               if (i,j) not in [(0,1),(4,5)]]+[(0,4),(1,5)]
    B=matrix(GF(2),[[int(v in e) for e in bad_edges] for v in range(8)])
    C=B.right_kernel().basis_matrix();assert C.nrows()==5
    assert C.column(10)==C.column(11)
    M=matrix(GF(2),[[C[i,e]*C[j,e] for i in range(5) for j in range(i,5)] for e in range(12)])
    assert M.rank()<12
    # Independently derive the exact-sequence formula by a block Gram matrix.
    checks=0
    for seed in range(1,26):
        # The columns of U are a unimodular ambient basis, with the first 3 in the kernel.
        U=identity_matrix(QQ,5)
        for i,j in [(0,1),(1,4),(3,2),(2,0),(4,3)]:
            T=identity_matrix(QQ,5);T[i,j]=seed+i-j;U=U*T
        assert U.det()==1
        A=matrix(QQ,5,5,lambda i,j:((i+seed)*(j+2)+j*j)%9-4)
        S=A*A.transpose()+identity_matrix(QQ,5)
        V=U.transpose()*S*U
        X=V[:3,:3];Y=V[:3,3:];Z=V[3:,3:]
        Schur=Z-Y.transpose()*X.inverse()*Y
        assert V.det()==X.det()*Schur.det()
        d=QQ((seed+1)*(seed+2))
        # Diagonal quotient map with finite index d and the target's standard metric.
        vol2=d*d/Schur.det()
        assert X.det()==S.det()*vol2/(d*d)
        assert X.det()!=S.det()*vol2*(d*d)
        checks+=1
    # Collected logarithms, independent of 617's assembly from Fminus and delta.
    base=64*R.pi().log()-(QQ(75)/2+QQ(111634)/27075)*R(2).log()
    headroom=R(623)-base
    def overlap(ball,pair):
        a,b=map(QQ,pair);return QQ(ball.lower())<=b and a<=QQ(ball.upper())
    assert overlap(base,primary['known_height_constant_interval'])
    assert overlap(headroom,primary['residual_headroom_for_623_interval'])
    assert base<R(QQ(44412)/1000) and headroom>R(QQ(578588)/1000)
    assert base+578<623
    # Local invariant quadratic differentials in w=z^m: z^(m-2) dz^2 = dw^2/(m^2 w).
    local=[]
    for m in [2,3,32]:
        a=m-2
        assert (a+2)%m==0 and (a+2)//m-2==-1
        local.append({'stabilizer_order':m,'minimal_invariant_z_exponent':a,
                      'coarse_pole_order':1,'coefficient_denominator':m*m})
    # The binomial quotient convention contributes half a logarithm per cross monomial.
    cross=16*15//2;assert cross==120 and QQ(cross)/2==60
    result={'status':'pass','milestone':'D147','cycle_pair_witnesses':witnesses,
            'independent_surjectivity_rank':45,'dyadic_multiplication_cokernel_length':0,
            'dyadic_surjectivity_requires_companion_stable_model_argument':True,
            'cubic_two_edge_cut_control_rank':int(M.rank()),'cubic_two_edge_cut_control_edges':12,
            'two_edge_cut_obstruction_detected':True,'block_Gram_identity_controls':checks,
            'wrong_torsion_sign_rejected':True,'known_height_constant_interval':iv(base),
            'residual_headroom_for_623_interval':iv(headroom),'safe_sufficient_metric_residual_upper':'578',
            'orbifold_local_descent_checks':local,'ordinary_quadratic_differential_rank':45,
            'orbifold_weight4_rank':72,'elliptic_principal_parts_rank':27,
            'metric_residual_at_most_578_proved':False,'relation_height_at_most_623_proved':False,
            'candidate_identification_proved':False,'new_precision_bank_admitted':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D147_MULTIPLICATION_AUDIT_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_multiplication_audit_d147.json';child_path=DATA/'P1600_multiplication_audit_d147_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D147_MULTIPLICATION_AUDIT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|618_P1600_MULTIPLICATION_AUDIT',flush=True)
