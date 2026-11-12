"""D146 independent reconstruction of the local controls and global height bound."""
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
INPUTS=['P1600_elliptic_intersections_d146','P1600_dyadic_model_audit_d143',
        'P1600_elliptic_height_audit_d143','cm_intrinsic_height_review_d104',
        'P1600_proof_gap_review_d141','P1600_spectral_feasibility_audit_d145']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ,PolynomialRing,RealBallField,prod
    R=RealBallField(224);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    def ball(v):
        a,b=map(QQ,v);return R((a+b)/2,(b-a)/2)
    packets={n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    assert all(r['status']=='pass' for r in packets.values())
    primary=packets['P1600_elliptic_intersections_d146'];model=packets['P1600_dyadic_model_audit_d143']
    P=PolynomialRing(QQ,'t');t=P.fraction_field().gen()
    h=1/(1-t);h2=(t-1)/t
    elements=[t,h,h2,1-t,1/t,t/(t-1)]
    orbit_product=prod(t-g for g in elements[1:])
    u=(t**3-3*t+1)/(t*(t-1));v=(2*u-3)**2
    assert u.derivative()/((t-h)*(t-h2))==1/(t*(t-1))
    assert v.derivative()/orbit_product==4/(t*t*(t-1)**2)
    assert (2*u-3)==(2*t-1)*(t+1)*(t-2)/(t*(t-1))
    L=PolynomialRing(QQ,names=['A','B','nu','w']);A,B,nu,w=L.gens()
    cost=QQ(8)/3*A+QQ(5)/3*B;rows=QQ(4)/3*A+QQ(1)/2*B
    assert cost-2*rows==QQ(2)/3*B
    assert QQ(10)/3*rows-cost==QQ(16)/9*A
    d3=nu+3*w
    assert (d3+2*nu)/3==nu+w
    assert (d3+nu)/3!=nu+w  # Losing a factorial valuation fails.
    # Reconstruct all dyadic pair and tail terms from the independent model.
    marks=[(2,5)]+[(2,j) for j in range(51,59) for _ in range(2)]
    marks += [(3,j+1) for j,count in enumerate(model['order3_points_by_component']) for _ in range(count)]
    marks += [(32,5)];assert len(marks)==27
    alpha=[1-QQ(1)/m for m,c in marks];beta=[1-QQ(1)/m**2 for m,c in marks]
    gamma=[QQ(m)-QQ(1)/m for m,c in marks]
    carrier={c:[i for i,(m,j) in enumerate(marks) if c==j] for c in range(1,59)}
    drops=[QQ(0)]*27;pair_add={(i,j):QQ(0) for i in range(27) for j in range(i+1,27)}
    for c,target,length,weight,energy in model['independent_tail_contractions']:
        length=QQ(length);ids=carrier[c];assert sum(alpha[i] for i in ids)==QQ(weight)
        for i in ids:drops[i]+=length
        for i in ids:
            for j in ids:
                if i<j:pair_add[i,j]+=length
        carrier[target]+=ids;del carrier[c]
    tail=-sum(beta[i]*drops[i] for i in range(27))+sum(2*alpha[i]*alpha[j]*x for (i,j),x in pair_add.items())
    J={pair:QQ(0) for pair in pair_add};J[0,26]=32
    for i in range(1,17,2):J[i,i+1]=QQ(33)/2
    different=list(map(QQ,model['independent_grounded_Laplacian_solution']))
    vertical=sum(gamma[i]*different[c-1] for i,(m,c) in enumerate(marks))
    pair_cost=sum(alpha[i]*alpha[j]*(marks[i][0]+marks[j][0])*val for (i,j),val in J.items())
    coefficient=(vertical+pair_cost-tail)/8
    assert coefficient==QQ(1193197)/6144 and tail==-QQ(19909)/768
    heights={2:ball(packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'])}
    heights.update({r['elliptic_order']:ball(r['Hodge_height_interval']) for r in packets['P1600_elliptic_height_audit_d143']['CM_fields']})
    base=sum(gamma[i]*(heights[m]+R(m).log()) for i,(m,c) in enumerate(marks))-coefficient*R(2).log()
    lower=base-45*R(3).log();upper=base-18*R(3).log()
    main=ball(model['RR_main_term_after_model_interval'])
    logC=15*R.pi().log()+QQ(5081)/192*R(2).log()+R(3).log()-QQ(485)/64
    Fupper=(main-lower-6*logC+246)/12
    assert lower>48 and upper<79 and Fupper<QQ(21)/5
    independent={'joint_Psi_plus_I_lower_interval':iv(lower),'joint_Psi_plus_I_upper_interval':iv(upper),'Faltings_upper_interval':iv(Fupper)}
    for key,a in independent.items():
        b=primary[key];assert QQ(a[0])<=QQ(b[1]) and QQ(b[0])<=QQ(a[1])
    critical=packets['P1600_proof_gap_review_d141']['Faltings_critical_intervals']
    assert len(critical)==3 and all(QQ(row[0])>QQ(21)/5 for row in critical)
    assert packets['P1600_spectral_feasibility_audit_d145']['uniform_strict_log_Zprime_lower']=='-41'
    result={'status':'pass','milestone':'D146','arb_precision_bits':224,
            'different_product_controls_independent':True,'factorial_valuation_negative_control_rejected':True,
            'pair_cost_two_sided_linear_identities_verified':True,
            'individual_dyadic_marks_and_tails_replayed':True,'dyadic_combined_log2_coefficient':str(coefficient),
            **independent,'all_three_D141_Faltings_only_critical_targets_excluded':True,
            'safe_joint_strict_bounds':['48','79'],'safe_Faltings_strict_upper':'4.2',
            'Faltings_lower_29_disproved':True,'candidate_identification_proved':False,
            'relation_height_at_most_623_proved':False,'new_precision_bank_admitted':False,
            'mathematical_claims_require_companion_derivations':True,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D146_INTERSECTION_AUDIT_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_intersection_audit_d146.json';child_path=DATA/'P1600_intersection_audit_d146_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D146_INTERSECTION_AUDIT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|615_P1600_INTERSECTION_AUDIT',flush=True)
