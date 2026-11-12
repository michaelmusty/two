"""D149: normalized primitive-frame budget and a corank-one cancellation control.

Run only through run_dyadic_capped.py. Geometric applications are in the
companion report; these finite calculations do not formalize those proofs.
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
INPUTS=['cm_cartier_frame_review_d119','cm_intrinsic_height_review_d104',
        'P1600_intersection_review_d146','P1600_forward_frame_bound_d148']


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import QQ,ZZ,GF,PolynomialRing,matrix,vector,diagonal_matrix,binomial,factorial,prod,RealBallField
    R=RealBallField(192);iv=lambda t:[str(QQ(t.lower())),str(QQ(t.upper()))]
    packets={n:json.loads((DATA/(n+'.json')).read_text()) for n in INPUTS}
    local=packets['cm_cartier_frame_review_d119']['certificate']
    old=packets['P1600_forward_frame_bound_d148']
    assert local['model']['normalization_index_beta']==264
    assert local['cohomology_torsion_length_beta']==14 and local['principal_part_norm_beta']==2
    assert packets['P1600_intersection_review_d146']['odd_pair_cost_bounds_log3']==['18','45']
    hmin,hmax=map(QQ,packets['cm_intrinsic_height_review_d104']['independent_analytic']['Hodge_height_interval'])
    l2=R(2).log();l3=R(3).log();lp=R.pi().log();logB=R(QQ(5)/3).log()-lp/2
    Hplus=2*R(hmax)-QQ(35)/34*l2
    Hminus=2*R(hmin)-QQ(35)/34*l2-QQ(36)/17*l3
    Fminus=-16*lp+(-8+QQ(55817)/54150)*l2
    I=QQ(33)/2*l2;tau=QQ(7)/8*l2
    logvol=8*R(QQ(17)/16).log()+16*logB
    pencil_lower=-17*Hplus+Fminus+I+tau-logvol
    # Product of all seventeen simple-pole coefficients: known norm zero 2/16.
    pencil_upper=-Hminus+(2*I-QQ(1)/8*l2)/17-R(17).log()/2
    D2=QQ(old['sum_squared_dual_root_majorants']);r=91
    logNp=R(8).log()+(R(17).log()+R(D2).log())/2+logB
    ext=2*r*logNp-QQ(r)/2*R(r).log()+QQ(r)/2*l2
    alpha=264+14;clearing=3*16;content=245-alpha+clearing
    assert alpha==278 and content==15 and clearing>=33
    assert 2*16<33  # A value-vector bound alone does not allow clearing by 4.
    dyadic=QQ(2*r*content)/16*l2
    beta=[R(1)/(R.pi()*R(QQ(3)/5)**2),
          2*R(2).sqrt()/(R.pi()*R(QQ(3)/5)**3),
          (2*R(3).sqrt()+2)/(R.pi()*R(QQ(3)/5)**4)]
    dM=sum(k*((n+2)*Hplus+beta[n].log()) for n,k in enumerate([17,15,13]))
    fixed=dM-17*Fminus-60*l2+ext-dyadic
    upper=-182*pencil_lower+fixed
    a,b=map(QQ,old['true_relation_height_upper_interval'])
    assert QQ(upper.lower())<=b and a<=QQ(upper.upper())
    # Exact coefficient cancellation, before any interval evaluation.
    difference=-182*QQ(139)/8+182*3+QQ(22295)/8-QQ(1365)/8
    assert difference==0
    required=(fixed-623)/182
    optimistic=-182*pencil_upper+fixed
    favorable_floor=optimistic-91*R(D2).log()
    assert Hminus>0 and pencil_upper<0 and required>24
    assert favorable_floor>623 and 15236<upper<15237
    # An integral nondegenerate curve with dimensions 16,136,45,91.
    P=PolynomialRing(QQ,'t');t=P.gen()
    q=1-(t**14+1)*prod(t-a for a in range(1,17))/factorial(16)
    fs=[t**i for i in range(15)]+[q]
    pairs=[(i,j) for i in range(16) for j in range(i,16)]
    lookup={p:k for k,p in enumerate(pairs)}
    multiplication=matrix(QQ,61,136,lambda k,l:(fs[pairs[l][0]]*fs[pairs[l][1]])[k])
    groups={};relations=[]
    for i in range(15):
        for j in range(i,15):
            if i+j not in groups:groups[i+j]=(i,j)
            else:
                row=[0]*136;row[lookup[(i,j)]]=1;row[lookup[groups[i+j]]]=-1;relations.append(row)
    J=matrix(ZZ,relations)
    assert multiplication.rank()==45 and J.rank()==91 and multiplication*J.transpose()==0
    evaluation=matrix(QQ,17,16,lambda i,j:fs[j](i))
    c=vector(ZZ,[0]+[(-1)**(a-1)*binomial(15,a-1) for a in range(1,17)])
    assert evaluation.rank()==16 and evaluation.transpose()*c==0
    assert evaluation.matrix_from_rows(list(range(1,17))).det()==0
    assert evaluation.matrix_from_rows([0]+list(range(2,17))).det()!=0
    forward=diagonal_matrix(QQ,list(c))*evaluation
    T=forward.matrix_from_rows(list(range(16))).change_ring(ZZ)
    ell=vector(ZZ,[-1]+[0]*14+[1])
    assert T.rank()==15 and T*ell==0 and all(c[a]!=0 for a in range(1,17))
    K=GF(31);A=T.change_ring(K)
    S=matrix(K,136,136,lambda k,l:A[pairs[k][0],pairs[l][0]]*A[pairs[k][1],pairs[l][1]]+
             (A[pairs[k][1],pairs[l][0]]*A[pairs[k][0],pairs[l][1]] if pairs[k][0]!=pairs[k][1] else 0))
    image=J.change_ring(K)*S.transpose();pivots=list(image.pivots())
    assert image.rank()==91
    minor=image.matrix_from_columns(pivots).det();assert minor!=0
    assert q(0)==0 and all(q(a)==1 for a in range(1,17)) and q.derivative()(16)!=0
    result={'status':'pass','milestone':'D149',
            'primitive_scalar_valuation_beta':alpha,'clearing_multiplier':8,
            'trace_dual_integer_multiplier':256,'primitive_forward_content_beta':content,
            'dyadic_primitive_exterior_content_coefficient_log2':'1365/8',
            'budget_difference_coefficient_log2':str(difference),
            'primitive_forward_bound_equals_D148':True,
            'H_lower_interval':iv(Hminus),'H_upper_interval':iv(Hplus),
            'pencil_degree_lower_interval':iv(pencil_lower),'pencil_degree_upper_interval':iv(pencil_upper),
            'pencil_degree_required_for_623_interval':iv(required),
            'primitive_true_relation_height_upper_interval':iv(upper),
            'optimistic_pencil_majorant_interval':iv(optimistic),
            'field_term_removed_optimistic_majorant_interval':iv(favorable_floor),
            'diagnostic_floors_are_not_actual_height_lower_bounds':True,
            'pencil_degree_and_field_norm_refinements_alone_sufficient':False,
            'corank_one_control':{'field_characteristic':31,'section_dimension':16,
              'multiplication_rank':45,'quadric_dimension':91,'evaluation_rank':16,
              'forward_rank':15,'quadratic_image_rank':91,'cofactor_product_zero':True,
              'image_pivot_columns':pivots,'image_pivot_minor':int(minor),
              'curve_q_coefficients':[str(z) for z in q.list()],
              'cofactor_vector_up_to_nonzero_scalar':list(map(int,c)),
              'smooth_canonical_CM_curve_claimed':False},
            'universal_cofactor_product_cancellation_disproved':True,
            'actual_CM_specific_cancellation_disproved':False,
            'best_current_proved_relation_height_upper':15237,
            'target_proved':False,'target_disproved':False,'candidate_identification_proved':False,
            'new_precision_bank_admitted':False,'actual_harmonic_precision_increased':False,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)}
    assert result['peak_rss_bytes']<2*(1<<30)
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('D149_PRIMITIVE_WORKER_PASS',flush=True)


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker',type=Path);args=ap.parse_args()
    if args.worker:worker(args.worker);sys.exit(0)
    tick=time.monotonic();output=DATA/'P1600_primitive_frame_limits_d149.json';child_path=DATA/'P1600_primitive_frame_limits_d149_worker.json'
    assert not output.exists() and not child_path.exists()
    env=dict(os.environ,DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH']=str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH','')
    child=subprocess.run([str(PYTHON),str(Path(__file__).resolve()),'--worker',str(child_path)],cwd=ROOT,env=env,capture_output=True,text=True)
    assert child.returncode==0 and 'D149_PRIMITIVE_WORKER_PASS' in child.stdout,(child.returncode,child.stdout,child.stderr)
    result=json.loads(child_path.read_text());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    crss=max(result['peak_rss_bytes'],resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024));assert rss+crss<2*(1<<30)
    result.update({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':rss,'child_peak_rss_bytes':crss,
                   'conservative_peak_rss_bytes':rss+crss,
                   'sources':[source(p) for p in [Path(__file__),PYTHON,child_path]+[DATA/(n+'.json') for n in INPUTS]]})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|623_P1600_PRIMITIVE_FRAME_LIMITS',flush=True)
