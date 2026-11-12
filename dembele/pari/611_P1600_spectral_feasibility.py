"""D145: rigorous scalar heat bounds from the trace systole and congruence gap.

No eigenvalues, geodesics, or new quaternion classes are computed.
The companion report proves the analytic inequalities used here.
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


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ,RealBallField,factorial
    R=RealBallField(192);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    def ball(v):
        a,b=map(QQ,v);return R((a+b)/2,(b-a)/2)
    trace=json.loads((DATA/'P1600_trace_systole_audit_d145.json').read_text())
    assert trace['status']=='pass' and all(not f['all_admissible_candidates'] for f in trace['families'])
    delta=QQ(39)/10;gap=QQ(3)/16;d=QQ(1455)/32
    assert QQ(trace['normalizer_systole_lower_rational'])>delta
    ramanujan_gap=QQ(1)/4-(QQ(7)/64)**2
    assert ramanujan_gap==QQ(975)/4096>gap
    cE=sum(QQ(count)*(QQ(m)-QQ(1)/m)/12 for m,count in [(2,17),(3,9),(32,1)])
    assert cE==QQ(869)/128
    D=(R(d)/2+cE)*R(-QQ(1)/4).exp()
    a=2*R(QQ(3)/4-3*delta**2/16).exp()
    q=R(-3*gap).exp()
    assert D<23 and a<QQ(1)/4 and q<QQ(4)/7
    M=a*(1+q*(D-1))/(1-a*q)
    assert M<QQ(95)/24
    K=4/(delta**2-1)
    gamma=R.euler_constant()
    x=R(gap)
    # Alternating E1 expansion; after 48 terms the next positive term
    # bounds the remainder since 0 < x < 1.
    series=-gamma-x.log()-sum((-x)**k/(k*factorial(k)) for k in range(1,49))
    remainder=x**49/(49*factorial(49))
    E1=R(series.center(),series.rad()+remainder.upper())
    refined=gamma-M*K-(D+M-1)*x.exp()*E1
    # Separate deliberately rounded proof, suitable for rational audit.
    assert gamma>QQ(577)/1000
    tail=x.exp()*(-QQ(577)/1000-x.log()+x)
    assert tail<QQ(31)/20
    simple=QQ(577)/1000-QQ(95)/24*K-QQ(623)/24*QQ(31)/20
    assert simple> -41 and refined>simple
    rr=json.loads((DATA/'P1600_dyadic_model_audit_d143.json').read_text())
    joint=json.loads((DATA/'P1600_joint_adjunction_d144.json').read_text())
    main=ball(rr['RR_main_term_after_model_interval'])
    logC=ball(joint['signature_log_C_interval'])
    # F >= 29 and average(log Z') > -41 require this STRICT upper
    # bound on the actual S=Psi+I, using the complete D144 identity.
    required_S=main-6*logC+6*41-12*29
    assert required_S< -249
    result={'status':'pass','milestone':'D145','arb_precision_bits':192,
            'systole_used':str(delta),'available_systole_lower':trace['normalizer_systole_lower_rational'],
            'Blomer_Brumley_gap':str(ramanujan_gap),'spectral_gap_used':str(gap),
            'elliptic_heat_zero_bound':str(cE),'times':['1','4'],
            'D1_upper_interval':iv(D),'hyperbolic_time_ratio_interval':iv(a),
            'spectral_time_ratio_interval':iv(q),'H1_upper_interval':iv(M),
            'small_time_integral_multiplier_upper':str(K),
            'E1_gap_interval':iv(E1),'refined_log_Zprime_lower_interval':iv(refined),
            'display_refined_lower':float(refined.center()),
            'rounded_tail_multiplier_upper':'31/20','rounded_H1_upper':'95/24',
            'rounded_nonconstant_heat1_upper':'623/24',
            'elementary_log_Zprime_lower':str(simple),'uniform_strict_log_Zprime_lower':'-41',
            'D144_sufficient_spectral_target':'-96.820','D144_sufficient_spectral_target_ruled_out':True,
            'necessary_joint_S_upper_for_Faltings29_interval':iv(required_S),
            'display_necessary_joint_S_upper':float(required_S.center()),
            'safe_necessary_joint_S_upper_for_Faltings29':'-249',
            'Faltings_lower_29_proved':False,'Faltings_lower_29_disproved':False,
            'candidate_identification_proved':False,
            'actual_curve_eigenvalue_computation_started':False,'geodesic_census_started':False,
            'mathematical_claims_require_companion_derivations':True,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D145_SPECTRAL_FEASIBILITY_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_spectral_feasibility_d145.json';child_path=DATA/'P1600_spectral_feasibility_d145_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D145_SPECTRAL_FEASIBILITY_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,'sources':[source(p) for p in [Path(__file__),PYTHON,child_path,
                    DATA/'P1600_trace_systole_audit_d145.json',DATA/'P1600_dyadic_model_audit_d143.json',
                    DATA/'P1600_joint_adjunction_d144.json']]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|611_P1600_SPECTRAL_FEASIBILITY',flush=True)
