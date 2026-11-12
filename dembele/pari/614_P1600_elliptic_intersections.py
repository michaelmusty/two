"""D146: finite controls and height consequences of the local intersection proof.

Use the frozen capped wrapper. The companion report, not these finite
checks, proves the assertions about all residue characteristics.
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
INPUTS=['cm_intrinsic_height_review_d104','P1600_elliptic_heights_d143',
        'P1600_dyadic_model_diagnostic_d143','P1600_dyadic_model_audit_d143',
        'P1600_joint_adjunction_d144','P1600_spectral_review_d145']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ,GF,NumberField,PolynomialRing,RealBallField
    R=RealBallField(192);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    def ball(v):
        a,b=map(QQ,v);return R((a+b)/2,(b-a)/2)
    packets={n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    assert all(p['status']=='pass' for p in packets.values())
    P=PolynomialRing(QQ,'x');x=P.gen();f=x**8-8*x**6+20*x**4-16*x**2+2
    F=NumberField(f,'b');b=F.gen();n=2+b
    assert F.discriminant()==2**31 and f.change_ring(GF(3)).is_irreducible()
    assert n.norm()==2 and not F(3).is_square() and not (3*n).is_square()
    E=NumberField(x*x-x+1,'a');a=E.gen()
    K=P.fraction_field();t=K(x);h=1/(1-t);r=1-t
    compose=lambda u,v:u.subs({x:v})
    assert compose(h,compose(h,h))==t and compose(r,r)==t
    assert compose(r,compose(h,r))==compose(h,h)
    u=t+1/(1-t)+(t-1)/t
    assert compose(u,h)==u
    fixed=t*t-t+1
    assert u.derivative()==fixed**2/(t*t*(t-1)**2)
    invariant=(2*u-3)**2
    assert compose(invariant,h)==invariant and compose(invariant,r)==invariant
    def at(v,z):return v.numerator()(z)/v.denominator()(z)
    assert at(u,a)==3*a and at(u,1-a)==3*(1-a)
    assert (at(u,a)-at(u,1-a))**2==-27
    assert at(invariant,a)==-27 and at(invariant,QQ(1)/2)==0
    assert ((1/(1-a)**2)-1)*((1/a**2)-1)==3
    model=packets['P1600_dyadic_model_diagnostic_d143']
    marks=[]
    for c in model['components']:
        for m in [2,3,32]:marks += [(m,c['class_one_based'])]*c['order'+str(m)+'_points']
    assert len(marks)==27
    for j in [35,36,37,38]:
        c=model['components'][j-1]
        assert c['class_one_based']==j and c['stabilizer_order']==3 and c['order3_points']==2
    shared=[]
    for i,(m,c) in enumerate(marks):
        for k,(s,d) in enumerate(marks[i+1:],i+1):
            if c==d:shared.append((m,s,c))
    assert len(shared)==13
    assert sum(c in range(35,39) and m==s==3 for m,s,c in shared)==4
    alpha={m:1-QQ(1)/m for m in [2,3,32]}
    weights=[]
    for m,s in [(3,3),(2,3)]:
        pair=alpha[m]*alpha[s]*(m+s)
        rows=(alpha[s] if m==3 else 0)+(alpha[m] if s==3 else 0)
        ratio=pair/rows;assert 2<=ratio<=QQ(10)/3
        weights.append({'orders':[m,s],'pair_coefficient':str(pair),'sum_order3_row_coefficient':str(rows),'ratio':str(ratio)})
    assert weights[0]['ratio']=='2' and weights[1]['ratio']=='10/3'
    cost_low=2*9;cost_high=QQ(10)/3*9*QQ(3)/2
    assert cost_low==18 and cost_high==45
    heights={2:ball(packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'])}
    heights.update({row['elliptic_order']:ball(row['absolute_Hodge_height_interval'])
                    for row in packets['P1600_elliptic_heights_d143']['CM_heights']})
    signature={2:17,3:9,32:1};l2=R(2).log();l3=R(3).log()
    dyadic_coefficient=QQ(packets['P1600_joint_adjunction_d144']['weighted_vertical_coefficient_log2'])
    dyadic_coefficient+=QQ(packets['P1600_joint_adjunction_d144']['known_dyadic_pair_cost_coefficient_log2'])
    dyadic_coefficient-=QQ(packets['P1600_joint_adjunction_d144']['tail_joint_correction_coefficient_log2'])
    assert dyadic_coefficient==QQ(1193197)/6144
    base=sum(count*(QQ(m)-QQ(1)/m)*(heights[m]+R(m).log()) for m,count in signature.items())-dyadic_coefficient*l2
    lower=base-cost_high*l3;upper=base-cost_low*l3
    assert lower>48 and upper<79
    main=ball(packets['P1600_dyadic_model_audit_d143']['RR_main_term_after_model_interval'])
    logC=ball(packets['P1600_joint_adjunction_d144']['signature_log_C_interval'])
    assert packets['P1600_spectral_review_d145']['uniform_strict_log_Zprime_lower']=='-41'
    Fupper=(main-lower-6*logC+246)/12
    assert Fupper<QQ(21)/5<29
    result={'status':'pass','milestone':'D146','arb_precision_bits':192,
            'field_discriminant':str(F.discriminant()),'prime3_inert_degree':8,
            'order6_normalizer_square_conditions_both_rejected':True,
            'cyclic3_and_symmetric3_rational_controls':True,
            'cyclic3_branch_difference_square':'-27','symmetric3_branch_difference':'-27',
            'controls_are_examples_not_a_claim_all_actions_have_these_coordinates':True,
            'dyadic_same_component_pairs':len(shared),'dyadic_order3_pairs_separated_by_tame_reduction':4,
            'pair_to_row_weights':weights,'order3_row_sum_bounds_in_v3':['1','3/2'],
            'odd_pair_cost_bounds_log3':['18','45'],
            'joint_base_before_odd_cost_interval':iv(base),
            'joint_Psi_plus_I_lower_interval':iv(lower),'joint_Psi_plus_I_upper_interval':iv(upper),
            'display_joint_lower':float(lower.center()),'display_joint_upper':float(upper.center()),
            'safe_joint_strict_lower':'48','safe_joint_strict_upper':'79',
            'Faltings_upper_interval':iv(Fupper),'display_Faltings_upper':float(Fupper.center()),
            'safe_Faltings_strict_upper':'4.2','Faltings_lower_29_disproved':True,
            'height_route_using_Faltings_lower_29_closed':True,
            'relation_height_at_most_623_proved':False,'candidate_identification_proved':False,
            'actual_curve_eigenvalue_computation_started':False,'new_precision_bank_admitted':False,
            'mathematical_claims_require_companion_derivations':True,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as fp:fp.write(json.dumps(result,indent=2)+'\n')
    print('D146_INTERSECTION_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_elliptic_intersections_d146.json';child_path=DATA/'P1600_elliptic_intersections_d146_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D146_INTERSECTION_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|614_P1600_ELLIPTIC_INTERSECTIONS',flush=True)
