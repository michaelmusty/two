"""D116 independent rank witness, logarithm budgets, residual checks and provenance."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('conditioning',ROOT/'dembele/pari/434_dyadic_rank_conditioning.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
r=c.r;f=c.f
OUT=DATA/'cm_compound_review_d116.json'

def exact_inverse(a):
    n=len(a);m=[list(map(Q,row))+[Q(i==j) for j in range(n)] for i,row in enumerate(a)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if m[i][k]);m[k],m[pivot]=m[pivot],m[k]
        factor=m[k][k];m[k]=[x/factor for x in m[k]]
        for i in range(n):
            if i!=k:
                factor=m[i][k];m[i]=[x-factor*y for x,y in zip(m[i],m[k])]
    assert all(m[i][j]==(i==j) for i in range(n) for j in range(n))
    inv=[row[n:] for row in m]
    assert all(sum(inv[i][k]*a[k][j] for k in range(n))==(i==j) for i in range(n) for j in range(n))
    return inv

def witness(packet,matrix_key,certificate_key):
    pivots=packet[certificate_key]['pivots'];rows=[p['row'] for p in pivots];cols=[p['column'] for p in pivots]
    n=len(pivots);full=packet[matrix_key]
    centers=[[Q(full[i][j][0]) for j in cols] for i in rows]
    errors=[[full[i][j][1] for j in cols] for i in rows]
    inv=exact_inverse(centers)
    bounds=[[min(r.val(inv[i][k])+errors[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    minimum=min(map(min,bounds));assert minimum>=1
    return {'rank_lower_bound':n,'rows':rows,'columns':cols,
            'method':'Exact rational center inverse; every entry of A0^-1*(A-A0) has v2 at least one.',
            'minimum_Neumann_error_valuation_v2':minimum,
            'inverse_centers':[[str(x) for x in row] for row in inv]}

def log_review(packet):
    n=256;lo=sum(Q(1,k*2**k) for k in range(1,n+1));hi=lo+Q(1,(n+1)*2**n)
    ans=[]
    for row in packet['height_budgets']['thresholds']:
        order=row['order'];alpha=Q(row['actual_height_bound_alpha']);beta=row['actual_height_bound_beta_log2']
        ceiling=row['actual_height_strict_integer_upper']
        assert ceiling-1<alpha+beta*lo<alpha+beta*hi<ceiling
        A=Q(row['difference_height_bound_alpha']);B=row['difference_height_bound_beta_log2']
        for name,m in [('rational_anchor_only',272),('degree16_place_only',17),('both_places_uniform_beta_error',16)]:
            N=row[name]['sufficient_beta_error']
            assert (N-m*B)*lo>m*A and (N-1-m*B)*hi<m*A
        ans.append({'order':order,'actual_height_strict_integer_upper':ceiling,
                    'degree16_sufficient_beta_error':row['degree16_place_only']['sufficient_beta_error']})
    # Independent line bookkeeping from T=S^(g-1)*(det E)^-1 and Delta=S^g*(det E)^-1.
    g=16
    for k in [1,2,3]:assert [k*(g-1)-(k-1)*g,-k+(k-1)]==[g-k,-1]
    assert [3+(g-2)*(g+1),g-1]==[241,15]
    assert [9+(4*g-6)*(g+1),4*g-2]==[995,62]
    return {'independent_binary_log_series_terms':n,'budgets':ans,'line_exponent_checks':True}

def residual_review(packet):
    orders,constants=c.setup();actual=[[r.series.restore(x) for x in order['actual']] for order in orders]
    x=constants[1];v,w=actual
    quadrics=json.loads((DATA/'cm_frame_curve_candidate.json').read_text())
    pairs=quadrics['monomial_pairs'];vv=[v[i]*v[j] for i,j in pairs]
    def scale(a,n):
        if not n:return f.Ball()
        extra=16*((abs(n)&-abs(n)).bit_length()-1)
        return f.Ball(f.R.scale(a.u,n),a.v if a.u!=f.Z else 0,a.error+extra)
    count=0;minima=[10**9,10**9]
    for q,saved in zip(quadrics['quadrics'],packet['direct_actual_quadric_residuals_orders_1_2']):
        gradient=[f.Ball() for _ in range(16)]
        quadratic=f.Ball()
        for coefficient,(i,j),product in zip(q,pairs,vv):
            gradient[i]=gradient[i]+scale(x[j],coefficient)
            gradient[j]=gradient[j]+scale(x[i],coefficient)
            quadratic=quadratic+scale(product,coefficient)
        first=f.dot(gradient,v);second=f.dot(gradient,w)+quadratic
        for k,value in enumerate([first,second]):
            reference=r.series.restore(saved[k])
            assert not value.known_nonzero() and not (value-reference).known_nonzero()
            minima[k]=min(minima[k],value.error);count+=1
    assert minima==packet['minimum_quadric_residual_error_beta']==[100,69]
    return {'independent_gradient_and_Hessian_residuals_checked':count,
            'minimum_error_beta':minima,'exact_vanishing_claimed':False}

def calculations():
    rank=json.loads((DATA/'dyadic_jet_rank_d116.json').read_text())
    conditioning=json.loads((DATA/'dyadic_rank_conditioning_d116.json').read_text())
    height=json.loads((DATA/'cm_compound_height_d116.json').read_text())
    first=witness(rank,'matrix_Q2_balls','certificate')
    second=witness(conditioning,'actual_matrix_Q2_balls','actual_rank_certificate')
    assert [first['rank_lower_bound'],second['rank_lower_bound']]==[32,33]
    orders,constants=c.setup();matrix,_,_=c.matrix(orders,constants)
    assert [[x.saved() for x in row] for row in matrix]==conditioning['actual_matrix_Q2_balls']
    assert [[x.saved() for x in row] for row in matrix[1:]]==rank['matrix_Q2_balls']
    logarithms=log_review(height);residuals=residual_review(conditioning)
    trials=conditioning['candidate_only_conditioning_trials']
    assert [(x['hypothetical_additional_beta_digits'],x['predicted_rank_lower_bound']) for x in trials]==[(0,33),(32,34),(64,41),(96,45)]
    assert all(not x['is_actual_precision_certificate'] for x in trials)
    print('INDEPENDENT_REVIEW|ranks 32/33 by exact inverse and Neumann; residuals 100/69; revised budgets pass',flush=True)
    return {'rank_witnesses':[first,second],'height_budget_review':logarithms,
            'quadric_residual_review':residuals,'candidate_conditioning_is_not_actual_precision':True}

def build(result):
    prior_path=DATA/'dyadic_strategy_review_d115.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==814
    paths=f.coarse.checked(prior['sources'])+[prior_path,Path(__file__),
        ROOT/'dembele/certificates/cm-compound-height-d116.md',DATA/'cm_compound_sources_d116.json']
    for number in [432,433,434]:paths+=list((ROOT/'dembele/pari').glob(f'{number}_*.py'))
    jobs=[]
    for p in sorted(DATA.glob('*d116*')):
        if p.name.startswith('cm_compound_review_d116'):continue
        paths.append(p)
        if p.suffix=='.json':
            record=json.loads(p.read_text())
            hashes=[x for x in record.get('sources',[]) if isinstance(x,dict) and 'sha256' in x]
            paths+=f.coarse.checked(hashes)
            if p.name.endswith('.job.json'):
                assert record['status']=='pass' and record['timeout_seconds']==180 and record['timeout_terminates_process_group']
                paths+=f.coarse.checked([record['driver'],record['log']])
                jobs.append({'receipt':p.name,'status':record['status'],'wall_seconds':record['wall_seconds']})
    assert len(jobs)==3
    return {'status':'pass','milestone':'D116','D115_source_hashes_checked_unchanged':814,
            'certificates':result,'bounded_jobs':jobs,
            'actual_J3_rank_lower_bound':33,'actual_J3_rank_45_certified':False,
            'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
            'sources':[f.coarse.source(p) for p in sorted(set(x.resolve() for x in paths))]}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--probe',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    result=calculations()
    if not a.probe:
        result=build(result)
        if a.check:
            previous=json.loads(OUT.read_text());f.coarse.checked(previous['sources']);assert result==previous
        else:assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'status':'pass','sources':len(result['sources']),'D115_preserved':814}),flush=True)
    print('PASS|435_CM_COMPOUND_REVIEW',flush=True)
