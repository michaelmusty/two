"""D147: canonical multiplication at the stable fibre and determinant controls.

Run only through run_dyadic_capped.py. Matrix controls do not prove the
companion geometric argument or bound the unknown global metric remainder.
"""
import argparse
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
INPUTS=['hyperellipticity_graph_review_d99','P1600_intersection_review_d146']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from itertools import combinations
    from sage.all import QQ,ZZ,GF,matrix,diagonal_matrix,identity_matrix,gcd,RealBallField
    R=RealBallField(192);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    saved=json.loads((DATA/(INPUTS[0]+'.json')).read_text())
    vertices=saved['stable_vertices'];edges=[(u,v) for u,v,_ in saved['stable_edges']]
    assert len(vertices)==30 and len(edges)==45
    assert all(sum(v in e for e in edges)==3 for v in vertices)
    incidence=matrix(GF(2),[[int(v in e) for e in edges] for v in vertices])
    cycles=incidence.right_kernel().basis_matrix();assert cycles.nrows()==16
    pairs=list(combinations(range(16),2));pairs=sorted([(i,i) for i in range(16)]+pairs)
    products=matrix(GF(2),45,136,lambda e,k:cycles[pairs[k][0],e]*cycles[pairs[k][1],e])
    rank=products.rank();pivots=list(products.pivots())
    def connected(removed):
        seen={vertices[0]};front=list(seen)
        while front:
            v=front.pop()
            for e,(a,b) in enumerate(edges):
                if e in removed:continue
                w=b if a==v else a if b==v else None
                if w is not None and w not in seen:seen.add(w);front.append(w)
        return len(seen)==len(vertices)
    cuts1=[list(c) for c in combinations(range(45),1) if not connected(set(c))]
    cuts2=[list(c) for c in combinations(range(45),2) if not connected(set(c))]
    graph={'vertices':vertices,'edges':[list(e) for e in edges],
           'cycle_basis_mod2':[[int(x) for x in row] for row in cycles],
           'monomial_pairs':[list(p) for p in pairs],'multiplication_rank_mod2':rank,
           'pivot_columns':pivots,'one_edge_cuts':cuts1,'two_edge_cuts':cuts2,
           'deletion_subsets_checked':45+990}
    if rank==45:
        assert products.matrix_from_columns(pivots).det()==1
        graph['surjective_pivot_minor_mod2']=1
    # Quotient symmetric metric: ordinary off-diagonal monomials have norm 1/sqrt(2).
    symcontrols=[]
    for g in range(2,7):
        A=matrix(QQ,g,g,lambda i,j:((i+2)*(j+3)+i*i)%7-3)
        G=A.transpose()*A+identity_matrix(QQ,g)
        ps=[(i,j) for i in range(g) for j in range(i,g)]
        S=matrix(QQ,[[(G[i,k]*G[j,l]+G[i,l]*G[j,k])/2 for k,l in ps] for i,j in ps])
        exponent=g*(g-1)//2
        assert S.det()==G.det()**(g+1)/ZZ(2)**exponent
        assert S.det()!=G.det()**(g+1)
        symcontrols.append({'rank_E':g,'off_diagonal_count':exponent,'determinant_formula_verified':True})
    # Integral cokernel, archimedean quotient volume and kernel covolume together.
    exact=[]
    for seed in range(1,31):
        n=5;m=2
        M=matrix(ZZ,m,n,lambda i,j:((seed+3*i+7*j)**2+11*i*j)%17-8)
        if M.rank()!=m:continue
        M=diagonal_matrix(ZZ,[2,3])*M
        A=matrix(QQ,n,n,lambda i,j:((seed+2*i+3*j)**2)%11-5)
        S=A.transpose()*A+identity_matrix(QQ,n)
        H=matrix(QQ,[[seed+2,1],[1,seed+3]])
        K=M.right_kernel().basis_matrix()
        index=gcd([M.matrix_from_columns(list(c)).det() for c in combinations(range(n),m)])
        volume2=H.det()*(M*S.inverse()*M.transpose()).det()
        lhs=(K*S*K.transpose()).det()
        rhs=S.det()*volume2/(H.det()*index**2)
        assert lhs==rhs and index>=6
        assert lhs!=S.det()*volume2/(H.det()*index**(-2))
        assert lhs!=S.det()*volume2/H.det()
        scale=QQ(7)/3
        Hnew=scale**2*H;vnew=Hnew.det()*(M*S.inverse()*M.transpose()).det()
        assert vnew/Hnew.det()==volume2/H.det()
        exact.append({'seed':seed,'cokernel_index':int(index),'identity_verified':True})
    assert len(exact)>=25
    shears=[]
    for N in [1,2,10,10**3,10**6]:
        T=identity_matrix(QQ,4);T[1,0]=N;assert T.det()==1
        G=T.transpose()*T;ps=[(i,j) for i in range(4) for j in range(i,4)]
        S=matrix(QQ,[[(G[i,k]*G[j,l]+G[i,l]*G[j,k])/2 for k,l in ps] for i,j in ps])
        q=matrix(QQ,1,len(ps),[1 if p==(0,3) else -N if p==(1,3) else -1 if p==(1,2) else 0 for p in ps])
        assert (q*S*q.transpose())[0,0]==1
        assert (q*q.transpose())[0,0]==N*N+2 and gcd(list(q[0]))==1
        shears.append({'N':N,'frame_determinant':1,'intrinsic_quadric_norm_squared':1,
                       'coefficient_covolume_squared':N*N+2})
    Fminus=-16*R.pi().log()+(-8+QQ(55817)/54150)*R(2).log()
    delta=QQ(19)/2*R(2).log();symmetric_correction=60*R(2).log()
    base=-4*Fminus-delta-symmetric_correction;headroom=623-base
    assert 44<base<QQ(89)/2 and QQ(1157)/2<headroom<579
    assert base+578<623
    orbifold_corrections={m:2-(2+m-1)//m for m in [2,3,32]}
    assert orbifold_corrections=={2:1,3:1,32:1}
    orbifold_rank=45+17+9+1;assert orbifold_rank==72
    result={'status':'pass','milestone':'D147','graph':graph,
            'symmetric_metric_controls':symcontrols,'cokernel_and_volume_controls':exact,
            'wrong_cokernel_sign_and_omission_rejected':True,
            'target_metric_rescaling_cancels':True,'determinant_one_shear_controls':shears,
            'symmetric_metric_degree_correction_log2':'60',
            'Faltings_lower_interval':iv(Fminus),'known_height_constant_interval':iv(base),
            'residual_headroom_for_623_interval':iv(headroom),
            'display_known_height_constant':float(base.center()),
            'display_residual_headroom':float(headroom.center()),
            'safe_sufficient_metric_residual_upper':'578',
            'ordinary_quadratic_differential_rank':45,'orbifold_weight4_rank':orbifold_rank,
            'elliptic_principal_parts_rank':27,'orbifold_n2_direct_substitution_valid':False,
            'metric_residual_at_most_578_proved':False,'relation_height_at_most_623_proved':False,
            'candidate_identification_proved':False,'new_precision_bank_admitted':False,
            'mathematical_claims_require_companion_derivations':True,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as fp:fp.write(json.dumps(result,indent=2)+'\n')
    print('D147_MULTIPLICATION_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_multiplication_determinant_d147.json';child_path=DATA/'P1600_multiplication_determinant_d147_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D147_MULTIPLICATION_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|617_P1600_MULTIPLICATION_DETERMINANT',flush=True)
