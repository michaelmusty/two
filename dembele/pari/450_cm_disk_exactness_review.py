"""D117 independent lattice, norm-budget and frozen-provenance review."""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'cm_disk_exactness_review_d117.json'
FP=[2,0,-16,0,20,0,-8,0,1]
MP=[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]

def source(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def checked(rows):
    result=[]
    for row in rows:
        p=Path(row['path']);assert source(p)==row;result.append(p)
    return result

def read(name):return json.loads((DATA/(name+'.json')).read_text())
def value(p,x):return sum(c*x**i for i,c in enumerate(p))

def ring_product(a,b,p):
    n=len(p)-1;out=[0]*(2*n-1)
    for i,c in enumerate(a):
        for j,d in enumerate(b):out[i+j]+=c*d
    for k in range(2*n-2,n-1,-1):
        for j in range(n):out[k-n+j]-=out[k]*p[j]
    return out[:n]

def basis_review(packet,p,basis_key,gram_key,hermitian):
    n=len(p)-1;basis=packet[basis_key]
    assert len(basis)==n and all(len(a)==i+1 and a[-1]==1 for i,a in enumerate(basis))
    powers=[[int(i==j) for i in range(n)] for j in range(n)]
    # Trace by diagonal entries of multiplication, independent of Newton sums.
    traces=[sum(ring_product(a,e,p)[j] for j,e in enumerate(powers)) for a in powers]
    gram=[]
    for a in basis:
        row=[]
        for b in basis:
            conjugate=[x*((-1)**j if hermitian else 1) for j,x in enumerate(b)]
            row.append(sum(x*y for x,y in zip(ring_product(a,conjugate,p),traces)))
        gram.append(row)
    assert gram==packet[gram_key]==[[(n if i==0 else 2*n)*int(i==j) for j in range(n)] for i in range(n)]
    assert n*(2*n)**(n-1)==2**(79 if hermitian else 31)

def support_vectors(n):
    # The tail square budget is at most five. Thus its entries are 0,+/-1,
    # with at most one +/-2. Enumerate support patterns, not a recursive ball.
    indices=tuple(range(1,n))
    for a0 in range(-3,4):
        budget=(11-a0*a0)//2
        for ntwo in (0,1):
            if 4*ntwo>budget:continue
            for two in combinations(indices,ntwo):
                rest=tuple(i for i in indices if i not in two)
                for none in range(budget-4*ntwo+1):
                    for ones in combinations(rest,none):
                        support=two+ones
                        for signs in product((-1,1),repeat=len(support)):
                            a=[a0]+[0]*(n-1)
                            for i,sign in zip(support,signs):a[i]=sign*(2 if i in two else 1)
                            assert a0*a0+2*sum(c*c for c in a[1:])<=11
                            yield a

UNIT=2**100
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def multiply(a,b):
    v=[x*y for x in a for y in b]
    return min(v)//UNIT,-(-max(v)//UNIT)
def square(a):
    lo=0 if a[0]<=0<=a[1] else min(x*x for x in a)
    return lo//UNIT,-(-max(x*x for x in a)//UNIT)
def linear(a,entries):
    lo=hi=0
    for c,(x,y) in zip(a,entries):
        lo+=c*(x if c>=0 else y);hi+=c*(y if c>=0 else x)
    return lo,hi

def lattice_review():
    real=read('cm_arithmetic_trace_gap_d117');cm=read('cm_projection_norm_gap_d117')
    basis_review(real,FP,'trace_basis_polynomials','trace_Gram_matrix',False)
    basis_review(cm,MP,'CM_trace_basis_polynomials','Hermitian_trace_Gram_matrix',True)
    assert cm['real_root_intervals']==real['real_root_intervals']
    roots=[tuple(map(Q,r)) for r in real['real_root_intervals']]
    assert len(roots)==8 and all(a<b and value(FP,a)*value(FP,b)<0 for a,b in roots)
    assert all(roots[i][1]<roots[i+1][0] for i in range(7))
    # Eight disjoint sign changes exhaust a degree-eight polynomial.
    real_rows=[];cm_rows=[]
    for a,b in roots:
        x=((a*UNIT).__floor__(),(b*UNIT).__ceil__());two=(2*UNIT,)*2
        T=[two,x]
        for k in range(2,8):T.append(add(multiply(x,T[-1]),neg(T[-2])))
        real_rows.append([(UNIT,UNIT)]+T[1:])
        # Write P_even=r(b), P_odd=beta*s(b), and evaluate by recurrence.
        bp2=add(x,two);parts=[two,(UNIT,UNIT)]
        for k in range(2,16):
            first=parts[-1] if k%2 else neg(multiply(bp2,parts[-1]))
            parts.append(add(first,parts[-2]))
        cm_rows.append(([(UNIT,UNIT)]+parts[1:],bp2))
    found=[];count=0
    for a in support_vectors(8):
        count+=1
        if not any(a[1:]):continue
        values=[linear(a,row) for row in real_rows]
        assert all(not lo<=2*UNIT<=hi and not lo<=-2*UNIT<=hi for lo,hi in values)
        out=[i for i,(lo,hi) in enumerate(values) if lo>2*UNIT or hi< -2*UNIT]
        if len(out)==1 and values[out[0]][0]>2*UNIT:
            assert values[out[0]][0]>8*UNIT;found.append((tuple(a),out[0]))
    assert count==real['vectors_enumerated']==6167
    assert set(found)=={(tuple(r['coefficients_in_trace_basis']),r['outlier_embedding_index']) for r in real['eligible_single_positive_outlier_elements']}
    found_cm=[];boundary=[];cmcount=0
    for a in support_vectors(16):
        cmcount+=1;active=[(i,c) for i,c in enumerate(a) if c];out=[]
        for i,(row,bp2) in enumerate(cm_rows):
            rlo=rhi=slo=shi=0
            for j,c in active:
                x,y=row[j]
                if c<0:x,y=y,x
                if j%2:slo+=c*x;shi+=c*y
                else:rlo+=c*x;rhi+=c*y
            lo,hi=add(square((rlo,rhi)),multiply(bp2,square((slo,shi))))
            if lo<=4*UNIT<=hi:
                assert a in ([-2]+[0]*15,[2]+[0]*15);boundary.append(a);break
            if lo>4*UNIT:out.append((i,lo))
            if len(out)>1:break
        else:
            if len(out)==1:
                i,lo=out[0];assert lo>64*UNIT;found_cm.append((tuple(a),i))
    assert cmcount==cm['vectors_enumerated']==376935
    assert set(found_cm)=={(tuple(r['coefficients_in_CM_trace_basis']),r['outlier_embedding_index']) for r in cm['eligible_single_outlier_elements']}
    assert sorted(boundary)==sorted(cm['constant_norm_four_vectors'])
    assert len(found)==8 and len(found_cm)==16
    return {'root_check':'eight disjoint rational sign changes, no Sturm reuse',
            'Gram_check':'multiplication-matrix traces, no Newton-sum reuse',
            'enumeration':'support patterns with at most one tail coefficient of absolute value two',
            'basis_value_check':'fixed-point interval recurrences, no polynomial Horner reuse',
            'real_vectors_checked':count,'CM_vectors_checked':cmcount,
            'single_outlier_real_elements':len(found),'single_outlier_CM_elements':len(found_cm),
            'no_real_trace_outlier_in_2_to_8':True,'no_CM_squared_norm_outlier_in_4_to_64':True}

def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def inverse(a):return [[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]]

def geometric_controls():
    J=[[0,-1],[1,0]];count=0
    for s,t,k in product((Q(-2),Q(0),Q(3,2)),(Q(-1),Q(0),Q(2)),(Q(1,2),Q(1),Q(2))):
        a=mm([[1,s],[0,1]],mm([[1,0],[t,1]],[[k,0],[0,1/k]]));assert det(a)==1
        conjugate=mm(J,mm(a,inverse(J)))
        x=[[a[i][j]+conjugate[i][j] for j in range(2)] for i in range(2)]
        q=[[(a[i][j]-conjugate[i][j])/2 for j in range(2)] for i in range(2)]
        gamma=mm(a,mm(J,mm(inverse(a),inverse(J))))
        coshd=sum(v*v for row in a for v in row)/2
        assert gamma[0][0]+gamma[1][1]==2-4*det(q)==2*coshd
        assert det(x)==2*coshd+2
        count+=1
    r2=Q(3,5);assert 4*(1+r2)**2/(1-r2)**2==64
    return {'rational_SL2_projection_controls':count,'final_disk_radius_squared':'3/5',
            'uniform_geometry_requires_companion_proof':True}

def plus(*xs):return sum(x[0] for x in xs),sum(x[1] for x in xs)
def scale(x,c):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])
def rounded(x):
    u=2**180;return Q((u*x[0]).__floor__(),u),Q((u*x[1]).__ceil__(),u)
def log_unit(q):
    assert 1<=q<=2;t=1-1/q;n=256
    lo=sum(t**k/k for k in range(1,n+1))
    return rounded((lo,lo+t**(n+1)/((n+1)*(1-t))))
L2=log_unit(Q(2))
def log(q):
    q=Q(q);k=0
    while q>=2:q/=2;k+=1
    while q<1:q*=2;k-=1
    return plus(log_unit(q),scale(L2,k))
def atan(q):
    n=96;lo=sum((-1)**k*q**(2*k+1)/Q(2*k+1) for k in range(n))
    return lo,lo+q**(2*n+1)/Q(2*n+1)
def sqrt(n):
    u=2**160;k=isqrt(n*u*u);assert k*k<n*u*u<(k+1)*(k+1)
    return Q(k,u),Q(k+1,u)

def budget_review():
    pi=rounded(plus(scale(atan(Q(1,5)),16),scale(atan(Q(1,239)),-4)))
    logpi=(log(pi[0])[0],log(pi[1])[1])
    hodge=Q(read('cm_intrinsic_height_review_d104')['independent_analytic']['Hodge_height_interval'][1])
    H=plus((2*hodge,2*hodge),L2)
    C=[scale(sqrt(2),2),plus(scale(sqrt(3),2),(Q(2),)*2),plus(scale(sqrt(6),2),(Q(4),)*2)]
    candidate=read('cm_frame_curve_candidate');L=max(sum(abs(c) for c in q) for q in candidate['quadrics'])
    assert L==42550
    results=[]
    for name,r2 in [('cm_disk_vanishing_budget_d117',Q(9,19)**2),('cm_uniform_disk_budget_d117',Q(3,5))]:
        packet=read(name);rows=packet['budgets']['thresholds'];targets=[]
        for n,row in enumerate(rows,1):
            logC=(log(C[n-1][0])[0],log(C[n-1][1])[1])
            pieces={'CM_fibre_degree':scale(H,240+n),'frame_vector_and_Faltings_log2':scale(L2,310),
                    'net_pi_factor':scale(logpi,120),'quadric_and_path_constant':log(480*L),
                    'jet_constant':logC,'disk_radius':scale(log(1/r2),240+n)}
            for key,iv in pieces.items():
                saved=tuple(map(Q,row['upper_bound_pieces'][key]))
                assert max(iv[0],saved[0])<=min(iv[1],saved[1])
            total=plus(*pieces.values());optimistic=plus(*(v for k,v in pieces.items() if k!='disk_radius'))
            anchor=row['certified_anchor_lower_beta'];achieved=row['achieved_degree16_lower_beta']
            for interval,key in [(total,'degree16_sufficient_integral_jet_lower_beta'),
                                 (optimistic,'optimistic_radius_one_same_bound_threshold_beta')]:
                lo=17*interval[0]/L2[1]-Q(anchor,16);hi=17*interval[1]/L2[0]-Q(anchor,16)
                N=row[key];assert N-1<lo<hi<N
            assert row['previous_exact_zero_orders_required']==list(range(n))
            assert row['valuation_gap']==row['degree16_sufficient_integral_jet_lower_beta']-achieved
            assert anchor==[3576,3248,2984][n-1] and achieved==[3794,3745,3728][n-1]
            targets.append(row['degree16_sufficient_integral_jet_lower_beta'])
        results.append({'packet':name,'sufficient_beta_valuations':targets})
    assert results[-1]['sufficient_beta_valuations']==[35947,36096,36237]
    for row in packet['dense_state_storage_examples']:
        P=row['working_pi_precision'];elements=174*(3*P-1)*16
        assert elements==row['state_field_elements']
        assert (elements*P+7)//8==row['packed_state_bytes_at_P_bits_per_element']
    return {'independent_log_series':'256-term -log(1-t), with rational remainder',
            'independent_pi_and_radical_enclosures':True,'budgets':results,
            'radius_one_fixed_input_limits_beta':[32928,33064,33193],
            'actual_integral_quadric_jet_lower_beta':[3794,3745,3728],
            'dense_state_storage_counts_checked':True,'exact_vanishing_proved':False}

def calculations():
    answer={'lattices':lattice_review(),'geometry_controls':geometric_controls(),'budgets':budget_review()}
    print('DISK_EXACTNESS_REVIEW|independent lattices, displacement controls and budgets pass',flush=True)
    return answer

def build(certificates):
    prior_path=DATA/'cm_arithmetic_identification_review_d116.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==868
    paths=checked(prior['sources'])+[prior_path,Path(__file__),
        ROOT/'dembele/certificates/cm-disk-and-exactness-d117.md',DATA/'cm_disk_sources_d117.json']
    for number in range(446,450):
        matches=list((ROOT/'dembele/pari').glob(f'{number}_*.py'));assert len(matches)==1;paths+=matches
    jobs=[]
    for path in sorted(DATA.glob('*d117*')):
        if path.name.startswith('cm_disk_exactness_review_d117'):continue
        paths.append(path)
        if path.suffix!='.json':continue
        packet=json.loads(path.read_text())
        paths+=checked([x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        if not path.name.endswith('.job.json'):continue
        assert packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
        paths+=checked([packet['log']])
        if packet['status']=='pass':paths+=checked([packet['driver']])
        else:
            assert packet['status']=='failed' and path.name=='cm_disk_vanishing_budget_d117_attempt01.job.json'
            paths+=checked([packet['failed_driver_snapshot']])
            assert packet['driver']['sha256']==packet['failed_driver_snapshot']['sha256']
        jobs.append({'receipt':path.name,'status':packet['status'],'wall_seconds':packet['wall_seconds']})
    assert len(jobs)==5 and sum(j['status']=='pass' for j in jobs)==4
    return {'status':'pass','milestone':'D117','D116_source_hashes_checked_unchanged':868,
            'certificates':certificates,'bounded_jobs':jobs,'uniform_disk_radius_squared':'3/5',
            'sufficient_degree16_integral_quadric_jet_valuations_beta':[35947,36096,36237],
            'actual_integral_quadric_jet_lower_beta':[3794,3745,3728],
            'actual_moment_precision_increased':False,'positive_quadric_jet_exact_vanishing_proved':False,
            'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
            'sources':[source(p) for p in sorted(set(p.resolve() for p in paths))]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--probe',action='store_true');parser.add_argument('--check',action='store_true');a=parser.parse_args()
    result=calculations()
    if not a.probe:
        result=build(result)
        if a.check:
            prior=json.loads(OUT.read_text());checked(prior['sources']);assert result==prior
        else:
            assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'status':'pass','sources':len(result['sources']),'D116_preserved':868}),flush=True)
    print('PASS|450_CM_DISK_EXACTNESS_REVIEW',flush=True)
