"""D144 independent audit: marked blowdowns, adjunction and compact RR factors."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
SAGE = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
PYTHON = SAGE/'venv/bin/python3'
INPUTS = ['P1600_joint_adjunction_d144','P1600_elliptic_height_audit_d143',
          'P1600_dyadic_model_audit_d143','P1600_height_routes_audit_d142',
          'cm_intrinsic_height_review_d104','cm_finite_height_review_d118']


def source(path):
    p = Path(path).resolve()
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ, RealBallField, PolynomialRing, vector
    R = RealBallField(224)
    iv = lambda x: [str(QQ(x.lower())),str(QQ(x.upper()))]
    def ball(pair):
        a,b = map(QQ,pair)
        return R((a+b)/2,(b-a)/2)
    def overlaps(a,b):
        return QQ(a[0]) <= QQ(b[1]) and QQ(b[0]) <= QQ(a[1])
    packets = {n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    assert all(x['status']=='pass' for x in packets.values())
    primary = packets['P1600_joint_adjunction_d144']
    model = packets['P1600_dyadic_model_audit_d143']
    # Replay the independent contraction order, carrying individual marks.
    marks = [(2,5)]+[(2,v) for v in range(51,59) for _ in range(2)]
    marks += [(3,v+1) for v,n in enumerate(model['order3_points_by_component']) for _ in range(n)]
    marks += [(32,5)]
    assert len(marks)==27
    orders = [m for m,v in marks]
    al = [1-QQ(1)/m for m in orders]
    be = [1-QQ(1)/m**2 for m in orders]
    ga = [m-QQ(1)/m for m in orders]
    carrier = {v:[i for i,(_,w) in enumerate(marks) if w==v] for v in range(1,59)}
    drops = [QQ(0)]*27
    pair_increase = {(i,j):QQ(0) for i in range(27) for j in range(i+1,27)}
    total_W = total_delta_loss = QQ(0)
    for v,w,length,weight,energy in model['independent_tail_contractions']:
        length,weight,energy = map(QQ,(length,weight,energy))
        ids = carrier[v]
        assert sum(al[i] for i in ids)==weight
        assert length*(weight-1)**2==energy
        for i in ids:
            drops[i] += length
        for i in ids:
            for j in ids:
                if i<j:
                    pair_increase[i,j] += length
        total_W += energy
        total_delta_loss += length
        carrier[w] += ids
        del carrier[v]
    deltaS = -sum(be[i]*drops[i] for i in range(27))+sum(2*al[i]*al[j]*v for (i,j),v in pair_increase.items())
    assert deltaS == total_W-total_delta_loss == -QQ(19909)/768
    assert drops[0]==36 and drops[26]==36 and drops[17]==28
    # Construct just the known intersections on Q and verify every m=2 jet.
    J = {(i,j):QQ(0) for i in range(27) for j in range(i+1,27)}
    J[0,26]=32
    for i in range(1,17,2):
        J[i,i+1]=QQ(33)/2
    vcoeff = list(map(QQ,model['independent_grounded_Laplacian_solution']))
    q = [vcoeff[v-1] for m,v in marks]
    djets=[]
    for i in range(17):
        cross = sum(al[j]*J[min(i,j),max(i,j)] for j in range(27) if j!=i)
        djets.append(2*q[i]+2*cross-8+drops[i])
    contents = packets['cm_finite_height_review_d118']['certificates']['composite_fibre']['combined_dyadic_contents_beta']
    assert [str(2*d) for d in djets] == list(map(str,contents))
    assert sum(djets)/(17*8) == QQ(69)/34
    qcost = sum(ga[i]*q[i] for i in range(27))/8
    jcost = sum(al[i]*al[j]*(orders[i]+orders[j])*v for (i,j),v in J.items())/8
    assert qcost==QQ(27799)/256 and jcost==QQ(659)/8
    h2 = R(QQ(packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'][1]))
    heights={2:h2}
    heights.update({r['elliptic_order']:ball(r['Hodge_height_interval']) for r in packets['P1600_elliptic_height_audit_d143']['CM_fields']})
    l2,lp,l3 = R(2).log(),R.pi().log(),R(3).log()
    joint = sum(ga[i]*(heights[m]+R(m).log()) for i,(m,v) in enumerate(marks))-(qcost+jcost-deltaS/8)*l2-12*l3
    assert overlaps(iv(joint),primary['joint_Psi_plus_I_upper_interval'])
    assert joint < QQ(21293)/250 # 85.172
    # Universal formal controls, independent of numerical Gamma values.
    F = PolynomialRing(QQ,'m').fraction_field(); m=F.gen()
    a,b=1-1/m,1-1/m**2
    assert b/6-QQ(1)/3+(m+1/m)/(6*m)==0
    # Boundary anomaly from radial Dirichlet energy, curvature and normal term.
    anomaly_loga = a*a/6+a*(1-a)/3
    assert anomaly_loga==b/6
    assert -a/6 != anomaly_loga # printed constant fails variable-cut control
    # Pairing W^2 / (omega_epsilon^2 tensor psi) has these log factors.
    pairing_ratio = vector(F,[-a,2*a,2*a*a-a*a])
    assert pairing_ratio==vector(F,[-a,2*a,a*a])
    # Hence the topological factor contains -2*a*log(m), not +2*a*log(m).
    topological_logm = -pairing_ratio[1]
    assert topological_logm==-2*a
    # After Gamma multiplication, assemble coefficients [zeta',log2,logpi,logm,1].
    K = vector(F,[2,QQ(1)/2,QQ(1)/2,0,-QQ(1)/4])
    disk = vector(F,[-2,-QQ(1)/6,-QQ(1)/2,0,-QQ(5)/12])
    # A - 2G/m = -(m+1)/m * sum log Gamma(j/m).
    gamma_reduced=vector(F,[0,-(m*m-1)/(2*m),-(m*m-1)/(2*m),(m+1)/(2*m),0])
    minus_cone_without_G=vector(F,[2/m,m/3-1/(6*m),m/2,-QQ(1)/2-m/6-1/(3*m),QQ(5)/(12*m)])
    # Choose general cut ratio t; its log coefficient already checked zero.
    other=vector(F,[0,(m+1/m)/6-QQ(1)/3+a/6,0,QQ(1)/3-a/3+(m-1/m)/6,a/2])
    assembled=a*K+disk+gamma_reduced+minus_cone_without_G+other
    assert assembled==vector(F,[0,a/6,0,1/(3*m),-a/6])
    # Teo (6.6), n=1: independent spectral constant, Gamma arguments shifted.
    z=R(-1).zetaderiv(1)
    spectral_rows=[]
    for mi in [1,2,3,4,5,8,16,32,64]:
        m=QQ(mi)
        direct=R(0)
        if mi>1:
            direct += (m-1)/(2*m)*R(m).log()
            direct += sum(QQ(2*((r-1)%mi)+1-mi)/(2*m)*R(QQ(r)/m).log_gamma() for r in range(1,mi))
            direct += sum(QQ(2*((r+1)%mi)+1-mi)/(2*m)*R((QQ(2)+r)/m).log_gamma() for r in range(mi))
            direct += ((m*m-1)/(6*m)-(m-1)/m)*R(m).log()
        A=sum(QQ(2*r-1-mi)/m*R(QQ(r)/m).log_gamma() for r in range(1,mi))
        expected=A+(m-1/m)/6*R(m).log()
        assert (direct-expected).contains_zero()
        # Gamma multiplication independently checks the cancellation step.
        gamma_sum=sum((R(QQ(r)/m).log_gamma() for r in range(1,mi)),R(0))
        assert (gamma_sum-(m-1)/2*(l2+lp)+R(m).log()/2).contains_zero()
        spectral_rows.append({'order':mi,'Teo_elliptic_constant_interval':iv(direct),'overlaps_final_FvP_8_1':True})
    logC=15*(l2+lp-QQ(1)/3)+6*l2+sum((1-QQ(1)/m)*(l2-1)/6+R(m).log()/(3*m) for m,v in marks)
    assert overlaps(iv(logC),primary['signature_log_C_interval'])
    main=ball(model['RR_main_term_after_model_interval'])
    baseline=(main-joint-6*logC)/12
    target=2*(baseline-29)
    assert overlaps(iv(target),primary['sufficient_average_log_Zprime_for_Faltings29_interval'])
    assert baseline > -QQ(1941)/100 and target > -QQ(4841)/50
    upperF=ball(packets['P1600_height_routes_audit_d142']['independent_Faltings_upper_interval'])
    implied_Z_lower=2*(baseline-upperF)
    assert implied_Z_lower > -QQ(989)/10
    result={'status':'pass','milestone':'D144','arb_precision_bits':224,
            'individual_mark_tail_replay':True,'marked_points':27,'unordered_pair_slots':351,
            'independent_tail_joint_correction_coefficient_log2':str(deltaS/8),
            'all_17_D118_dyadic_contents_reconstructed':True,'dyadic_contents_beta':list(map(str,contents)),
            'independent_joint_upper_interval':iv(joint),'joint_strict_upper':'85.172',
            'universal_variable_cut_cancellation':True,'boundary_anomaly_derived_from_radial_terms':True,
            'Deligne_pairing_topological_sign_checked':True,'universal_Gamma_cancellation_checked':True,
            'Teo_n1_spectral_controls':spectral_rows,
            'independent_log_C_interval':iv(logC),'independent_affine_Faltings_baseline_interval':iv(baseline),
            'safe_affine_Faltings_baseline':'-19.410','independent_sufficient_log_Zprime_target_interval':iv(target),
            'safe_sufficient_average_log_Zprime_target':'-96.820',
            'implied_average_log_Zprime_lower_interval':iv(implied_Z_lower),
            'safe_implied_average_log_Zprime_lower':'-98.900',
            'source_corrections_are_our_derivations_not_author_confirmed':True,
            'geometric_and_analytic_claims_require_companion_proof':True,
            'actual_curve_spectral_calculation_started':False,'Faltings_lower_29_proved':False,
            'candidate_identification_proved':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print('D144_ADJUNCTION_AUDIT_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path)
    args=ap.parse_args()
    if args.worker:
        worker(args.worker);sys.exit(0)
    tick=time.monotonic()
    output=DATA/'P1600_adjunction_RR_audit_d144.json'
    child_path=DATA/'P1600_adjunction_RR_audit_d144_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D144_ADJUNCTION_AUDIT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text())
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
    assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|607_P1600_ADJUNCTION_RR_AUDIT',flush=True)
