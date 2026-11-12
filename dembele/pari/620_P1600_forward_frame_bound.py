"""D148: evaluate the joint filtered multiplication / forward-frame height bound.

Use run_dyadic_capped.py. The geometric filtration and integral comparison
are proved in the companion report, not by these finite calculations.
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
INPUTS=['cm_arithmetic_audit','cm_field_recognition','cm_residue_lattice_d102',
        'cm_intrinsic_height_review_d104','P1600_multiplication_determinant_d147','P1600_multiplication_review_d147']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ,ZZ,PolynomialRing,NumberField,matrix,identity_matrix,RealBallField,lcm,ceil
    R=RealBallField(192);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    packets={n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    field=packets['cm_arithmetic_audit']['residue_algebra_input']
    saved=packets['cm_field_recognition']['field_basis']
    old=packets['cm_residue_lattice_d102']['field_lattice']
    f=field['polynomial_coefficients_ascending'];assert len(f)==18 and f[-1]==1
    P=PolynomialRing(QQ,'x');L=NumberField(P(f),'a');a=L.gen()
    b=[L(P(list(map(QQ,row)))) for row in saved['integral_basis_power_coordinates']]
    assert len(b)==17 and b[0]==1
    T=matrix(QQ,17,17,lambda i,j:(b[i]*b[j]).trace())
    assert T==matrix(QQ,old['trace_gram']) and T.det()==2**79
    inv=T.inverse();assert lcm([z.denominator() for z in inv.list()])==32
    assert all((32*z).denominator()==1 for z in inv.list())
    dual=[sum(inv[j,k]*b[k] for k in range(17)) for j in range(17)]
    eta=[b[j]-b[j].trace()/17 for j in range(1,17)]
    assert matrix(QQ,16,16,lambda i,j:(dual[i+1]*eta[j]).trace())==identity_matrix(QQ,16)
    assert all(dual[j].trace()==0 for j in range(1,17))
    left=sum(abs(ZZ(c))*4**k for k,c in enumerate(f[:-1]));assert left<4**17
    bounds=[];polys=[]
    for j in range(1,17):
        coeff=list((32*dual[j]).polynomial())
        z=sum(abs(c)*4**k for k,c in enumerate(coeff));assert z>0
        bounds.append(z);polys.append([str(c) for c in coeff])
    D2=sum(z*z for z in bounds);assert D2>1
    l2=R(2).log();lp=R.pi().log();logB=R(QQ(5)/3).log()-lp/2
    hL=QQ(packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'][1])
    H=2*R(hL)-QQ(35)/34*l2
    F=-16*lp+(-8+QQ(55817)/54150)*l2
    # Norms of coefficients of products of L2-normalized holomorphic differentials.
    beta=[R(1)/(R.pi()*R(QQ(3)/5)**2),
          2*R(2).sqrt()/(R.pi()*R(QQ(3)/5)**3),
          (2*R(3).sqrt()+2)/(R.pi()*R(QQ(3)/5)**4)]
    costs=[(n+2)*H+beta[n].log() for n in range(3)]
    assert costs[0]<costs[1]<costs[2]
    choices=[]
    for k1 in [15,16,17]:
        counts=[17,k1,28-k1]
        value=sum(k*c for k,c in zip(counts,costs))
        choices.append({'ranks':counts,'image_degree_upper_interval':iv(value)})
    dM=17*costs[0]+15*costs[1]+13*costs[2]
    # ||Phi||_HS <= (17/16)^8 B^17, ||W||_op <= sqrt(17*sum D_j^2).
    logN=R(17).log()/2+R(D2).log()/2+8*R(QQ(17)/16).log()+17*logB
    r=91
    # Sym^2 Frobenius estimate, rank-r exterior AM-GM, then ordinary coefficient norm.
    exterior=2*r*logN-QQ(r)/2*R(r).log()+QQ(r)/2*l2
    dyadic=QQ(2*r*245)/16*l2
    S=17*H-F
    upper=2*r*S+dM-17*F-60*l2+exterior-dyadic
    combined=upper+4*F+QQ(139)/2*l2
    safe=int(ceil(upper.upper()))
    assert 623<safe<83240
    # Favorable removal of the nonnegative trace-dual polynomial-size term.
    # This is a floor of THIS numerical majorant, not a lower bound on h_ext.
    floor=upper-r*R(D2).log()
    assert floor>10000
    result={'status':'pass','milestone':'D148','trace_gram_determinant':str(T.det()),
            'trace_dual_clearing_integer':32,'trace_dual_pairing_with_eta_is_identity':True,
            'root_radius':4,'Rouche_left':str(left),'Rouche_right':str(4**17),
            'scaled_trace_dual_power_coordinates':polys,'dual_root_majorants':[str(z) for z in bounds],
            'sum_squared_dual_root_majorants':str(D2),
            'H_upper_interval':iv(H),'F_lower_interval':iv(F),'log_B_interval':iv(logB),
            'jet_operator_norm_intervals':[iv(z) for z in beta],'filtration_rank_cases':choices,
            'worst_filtration_ranks':[17,15,13],'image_quotient_degree_upper_interval':iv(dM),
            'forward_frame_log_HS_upper_interval':iv(logN),'rank91_exterior_log_upper_interval':iv(exterior),
            'dyadic_frame_content_coefficient_log2':str(QQ(2*r*245)/16),
            'true_relation_height_upper_interval':iv(upper),'safe_true_relation_height_upper':safe,
            'display_true_relation_height_upper':float(upper.center()),
            'combined_R_minus_t_upper_interval':iv(combined),
            'field_size_removed_majorant_interval':iv(floor),'display_field_size_removed_majorant':float(floor.center()),
            'majorant_floor_is_not_an_actual_height_lower_bound':True,
            'previous_upper':83240,'target_upper':623,'target_proved':False,'target_disproved':False,
            'candidate_identification_proved':False,'new_precision_bank_admitted':False,
            'spectral_n2_determinant_used':False,'candidate_height_used_as_actual_bound':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D148_FORWARD_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_forward_frame_bound_d148.json';child_path=DATA/'P1600_forward_frame_bound_d148_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D148_FORWARD_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|620_P1600_FORWARD_FRAME_BOUND',flush=True)
