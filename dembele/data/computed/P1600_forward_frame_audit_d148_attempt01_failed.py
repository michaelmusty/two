"""D148: independent Newton-trace, collected-height and exterior-norm audit."""
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
INPUTS=['cm_arithmetic_audit','cm_field_recognition','cm_intrinsic_height_review_d104',
        'P1600_forward_frame_bound_d148']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from itertools import combinations
    from sage.all import QQ,ZZ,matrix,identity_matrix,diagonal_matrix,gcd,prod,RealBallField
    R=RealBallField(224);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    packets={n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    first=packets['P1600_forward_frame_bound_d148']
    f=packets['cm_arithmetic_audit']['residue_algebra_input']['polynomial_coefficients_ascending']
    B=matrix(QQ,packets['cm_field_recognition']['field_basis']['integral_basis_power_coordinates'])
    traces=[QQ(17)]
    for k in range(1,33):
        if k<=17:traces.append(-sum(f[17-j]*traces[k-j] for j in range(1,k))-k*f[17-k])
        else:traces.append(-sum(f[17-j]*traces[k-j] for j in range(1,18)))
    P=matrix(QQ,17,17,lambda i,j:traces[i+j])
    # Solve the trace-duality equations in the power basis, without the basis Gram inverse.
    D=32*(B*P).inverse().transpose();assert B*P*D.transpose()==32*identity_matrix(QQ,17)
    assert all(x.denominator()==1 for x in (D*B.inverse()).list())
    bounds=[]
    for j in range(1,17):
        value=QQ(0)
        for c in reversed(list(D[j])):value=4*value+abs(c)
        bounds.append(value)
        saved=list(map(QQ,first['scaled_trace_dual_power_coordinates'][j-1]))
        assert list(D[j])==saved+[0]*(17-len(saved))
    D2=sum(t*t for t in bounds)
    assert bounds==list(map(QQ,first['dual_root_majorants'])) and D2==QQ(first['sum_squared_dual_root_majorants'])
    l2=R(2).log();lp=R.pi().log();lo=R(QQ(5)/3).log()
    hL=QQ(packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'][1])
    H=2*R(hL)-QQ(35)/34*l2;F=-16*lp+(-8+QQ(55817)/54150)*l2
    # Fully collected independently from the geometric line-by-line assembly in 620.
    upper=3225*H-199*F-1592*lp+3225*lo+1547*R(17).log()+91*R(D2).log()
    upper-=QQ(68719)/8*l2+QQ(91)/2*R(91).log()
    upper+=13*(R(3).sqrt()+1).log()
    floor=upper-91*R(D2).log();combined=upper+4*F+QQ(139)/2*l2
    def overlaps(x,pair):
        a,b=map(QQ,pair);return QQ(x.lower())<=b and a<=QQ(x.upper())
    assert overlaps(upper,first['true_relation_height_upper_interval'])
    assert overlaps(floor,first['field_size_removed_majorant_interval'])
    assert overlaps(combined,first['combined_R_minus_t_upper_interval'])
    assert 15236<upper<15237<83240 and 11266<floor<11267
    norm_checks=0
    for g in range(2,8):
        vals=[QQ(2*i+3,3) for i in range(g)]
        squares=sorted([vals[i]**2*vals[j]**2 for i in range(g) for j in range(i,g)],reverse=True)
        frob=sum(t*t for t in vals)
        assert sum(squares)==(frob**2+sum(t**4 for t in vals))/2
        assert sum(squares)<=frob**2
        for r in range(1,len(squares)+1):
            assert prod(squares[:r])<=(frob**2/r)**r;norm_checks+=1
    # Check finite content under Sym^2 before exterior saturation, using genuine minors.
    ps=[(i,j) for i in range(3) for j in range(i,3)]
    def sym(T):
        return matrix(ZZ,6,6,lambda k,l:T[ps[k][0],ps[l][0]]*T[ps[k][1],ps[l][1]]+
                      (T[ps[k][1],ps[l][0]]*T[ps[k][0],ps[l][1]] if ps[k][0]!=ps[k][1] else 0))
    T=matrix(ZZ,[[1,2,0],[0,1,1],[0,0,1]]);S=sym(T);assert S.det()==1
    basis=matrix(ZZ,[[1,0,1,0,0,0],[0,1,0,0,1,0],[0,0,0,1,0,1]])
    initial=basis*S.transpose()
    content=lambda A:gcd([A.matrix_from_columns(list(c)).det() for c in combinations(range(6),3)])
    assert content(initial)==1
    controls=[]
    for p,k in [(2,1),(2,3),(3,2),(5,4)]:
        A=basis*sym(p**k*T).transpose();value=content(A)
        assert A==p**(2*k)*initial and value==p**(6*k)
        controls.append({'prime':p,'frame_content':k,'kernel_rank':3,'image_index':str(value)})
    assert QQ(2*91*245)/16==QQ(22295)/8
    result={'status':'pass','milestone':'D148','independent_Newton_power_trace_dual_verified':True,
            'sum_squared_dual_root_majorants':str(D2),'true_relation_height_upper_interval':iv(upper),
            'safe_true_relation_height_upper':15237,'combined_R_minus_t_upper_interval':iv(combined),
            'field_size_removed_majorant_interval':iv(floor),'majorant_floor_is_not_an_actual_height_lower_bound':True,
            'exterior_norm_cases':norm_checks,'symmetric_and_exterior_content_controls':controls,
            'dyadic_frame_content_coefficient_log2':'22295/8','worst_filtration_ranks':[17,15,13],
            'target_proved':False,'target_disproved':False,'candidate_identification_proved':False,
            'new_precision_bank_admitted':False,'spectral_n2_determinant_used':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D148_FORWARD_AUDIT_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_forward_frame_audit_d148.json';child_path=DATA/'P1600_forward_frame_audit_d148_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D148_FORWARD_AUDIT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|621_P1600_FORWARD_FRAME_AUDIT',flush=True)
