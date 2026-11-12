"""D149 independent collected-budget and polynomial-substitution audit."""
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
INPUTS=['cm_intrinsic_height_review_d104','cm_cartier_frame_review_d119',
        'P1600_forward_frame_bound_d148','P1600_primitive_frame_limits_d149']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ,ZZ,GF,PolynomialRing,matrix,binomial,prod,RealBallField
    R=RealBallField(224);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    packets={n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    first=packets['P1600_primitive_frame_limits_d149'];old=packets['P1600_forward_frame_bound_d148']
    hmin,hmax=map(QQ,packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'])
    l2=R(2).log();l3=R(3).log();lp=R.pi().log();lo=R(QQ(5)/3).log()
    Hp=2*R(hmax)-QQ(35)/34*l2;Hm=2*R(hmin)-QQ(36)/17*l3-QQ(35)/34*l2
    F=-16*lp+(-8+QQ(55817)/54150)*l2;D2=QQ(old['sum_squared_dual_root_majorants'])
    pencil_low=-17*Hp+F+QQ(139)/8*l2-8*R(QQ(17)/16).log()-16*(lo-lp/2)
    pencil_high=-Hm+QQ(263)/136*l2-R(17).log()/2
    fixed=131*Hp-17*F-136*lp+313*lo+91*R(17).log()+91*R(D2).log()
    fixed+=QQ(3171)/8*l2+13*(R(3).sqrt()+1).log()-QQ(91)/2*R(91).log()
    required=(fixed-623)/182
    upper=3225*Hp-199*F-1592*lp+3225*lo+1547*R(17).log()+91*R(D2).log()
    upper-=QQ(68719)/8*l2+QQ(91)/2*R(91).log();upper+=13*(R(3).sqrt()+1).log()
    # Collected after replacing Lambda by its favorable UPPER endpoint.
    floor=131*Hp+182*Hm-17*F-136*lp+313*lo+182*R(17).log()
    floor+=QQ(6041)/136*l2+13*(R(3).sqrt()+1).log()-QQ(91)/2*R(91).log()
    optimistic=floor+91*R(D2).log()
    values={'H_lower_interval':Hm,'H_upper_interval':Hp,
            'pencil_degree_lower_interval':pencil_low,'pencil_degree_upper_interval':pencil_high,
            'pencil_degree_required_for_623_interval':required,
            'primitive_true_relation_height_upper_interval':upper,
            'optimistic_pencil_majorant_interval':optimistic,
            'field_term_removed_optimistic_majorant_interval':floor}
    for key,z in values.items():
        a,b=map(QQ,first[key]);assert QQ(z.lower())<=b and a<=QQ(z.upper()),key
    assert Hm>0 and pencil_high<0 and required>24 and floor>623
    # Identity for an arbitrary rank, twist and scalar, before inequalities.
    A=PolynomialRing(QQ,names=['S','af','aa','k','r','j','v','ix'])
    S,af,aa,k,r,j,v,ix=A.gens();lam=af-aa-S
    old_height=2*r*S-j+v-ix
    new_height=-2*r*lam-j+v+2*r*(k-aa)-(ix+2*r*(k-af))
    assert old_height==new_height
    # D146's row bound implies B_23 <= 27 log(3), with exact nonnegative slack.
    B=PolynomialRing(QQ,names=['a','b']);a,b=B.gens()
    assert 27-b==2*(QQ(27)/2-(QQ(4)/3*a+b/2))+QQ(8)/3*a
    local=packets['cm_cartier_frame_review_d119']['certificate']
    index=8*local['model']['intersection_length_each_ordinary_pair_beta']
    tau=sum(local['restriction_Smith_valuations_beta']);norm=sum(local['primitive_principal_part_values_beta'])
    assert (index,tau,norm)==(264,14,2)
    # The simple-pole valuation vector differs from the cofactor vector by 278.
    simple=[2]+[-33]*16;cofactors=[280]+[245]*16
    assert [c-s for c,s in zip(cofactors,simple)]==[index+tau]*17
    assert min(simple)+48==15
    assert sum(simple)+2*index==norm
    assert -182*QQ(index+tau)/16+182*3+QQ(2*91*245)/16-QQ(2*91*15)/16==0
    amgm=[]
    for weights in [[1]*17,list(range(1,18)),[2**i for i in range(17)],[1]+[100]*16]:
        total=sum(weights);squares=[QQ(x)/total for x in weights]
        assert sum(squares)==1 and prod(squares)<=QQ(1)/17**17
        amgm.append([str(x) for x in squares])
    # Direct polynomial substitution, independent of 623's Sym^2 matrix formula.
    pairs=[(i,j) for i in range(16) for j in range(i,16)]
    lookup={p:k for k,p in enumerate(pairs)};groups={};relations=[];rows=[]
    for i in range(15):
        for j2 in range(i,15):
            if i+j2 in groups:
                a,b=groups[i+j2];relations.append((i,j2,a,b))
                row=[0]*136;row[lookup[(i,j2)]]=1;row[lookup[(a,b)]]=-1;rows.append(row)
            else:groups[i+j2]=(i,j2)
    J=matrix(QQ,rows);ell_products=[]
    for i in range(16):
        row=[0]*136;row[lookup[tuple(sorted((i,15)))]]+=1;row[lookup[(0,i)]]-=1
        ell_products.append(row)
    assert J.rank()==91 and J.stack(matrix(QQ,ell_products)).rank()==107
    K=GF(61);P=PolynomialRing(K,names=['y'+str(i) for i in range(16)]);ys=P.gens()
    c=[0]+[(-1)**(a-1)*binomial(15,a-1) for a in range(1,17)]
    T=matrix(K,16,16,lambda a,b:0 if a==0 else c[a]*(a**b if b<15 else 1))
    forms=[sum(T[a,b]*ys[a] for a in range(16)) for b in range(16)]
    image_polys=[forms[i]*forms[j2]-forms[a]*forms[b] for i,j2,a,b in relations]
    image=matrix(K,[[f.monomial_coefficient(ys[i]*ys[j2]) for i,j2 in pairs] for f in image_polys])
    pivots=list(image.pivots());minor=image.matrix_from_columns(pivots).det()
    assert T.rank()==15 and image.rank()==91 and minor!=0
    result={'status':'pass','milestone':'D149','independent_collected_budget_verified':True,
            'arbitrary_scalar_and_twist_height_invariance_verified':True,
            'odd_intersection_slack_identity_verified':True,
            'principal_part_norm_zero_beta':norm,'primitive_scalar_valuation_beta':index+tau,
            'primitive_forward_content_beta':15,'budget_difference_coefficient_log2':'0',
            'primitive_forward_bound_equals_D148':True,
            **{key:iv(z) for key,z in values.items()},
            'display_values':{key.removesuffix('_interval'):float(z.center()) for key,z in values.items()},
            'pencil_product_AMGM_controls':amgm,
            'direct_polynomial_substitution_control':{'field_characteristic':61,
              'forward_rank':15,'quadric_dimension':91,'quadratic_image_rank':91,
              'image_pivot_columns':pivots,'image_pivot_minor':int(minor),
              'relation_plus_linear_factor_space_rank':107,'cofactor_product_zero':True},
            'diagnostic_floors_are_not_actual_height_lower_bounds':True,
            'pencil_degree_and_field_norm_refinements_alone_sufficient':False,
            'universal_cofactor_product_cancellation_disproved':True,
            'actual_CM_specific_cancellation_disproved':False,
            'best_current_proved_relation_height_upper':15237,
            'target_proved':False,'target_disproved':False,'candidate_identification_proved':False,
            'new_precision_bank_admitted':False,'actual_harmonic_precision_increased':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D149_PRIMITIVE_AUDIT_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_primitive_frame_audit_d149.json';child_path=DATA/'P1600_primitive_frame_audit_d149_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D149_PRIMITIVE_AUDIT_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|624_P1600_PRIMITIVE_FRAME_AUDIT',flush=True)
