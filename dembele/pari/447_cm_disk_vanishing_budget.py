"""D117: larger CM disks, unrounded norm constants and a radius-only limit.

The optimistic radius-one calculation is a limitation of this particular
bound with its other inputs fixed, not a lower bound on every possible proof.
"""
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def plus(*xs):return sum(x[0] for x in xs),sum(x[1] for x in xs)
def scale(x,c):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])

def rounded(x):
    unit=2**192
    return Q((x[0]*unit).__floor__(),unit),Q((x[1]*unit).__ceil__(),unit)

def atanh_log(q,terms=80):
    assert 1<=q<=2
    x=(q-1)/(q+1)
    lo=2*sum(x**(2*k+1)/Q(2*k+1) for k in range(terms))
    hi=lo+2*x**(2*terms+1)/(Q(2*terms+1)*(1-x*x))
    return rounded((lo,hi))

LOG2=atanh_log(Q(2))

def log(q):
    q=Q(q);assert q>0;k=0
    while q>=2:q/=2;k+=1
    while q<1:q*=2;k-=1
    return plus(atanh_log(q),scale(LOG2,k))

def atan(x,terms=80):
    a=sum((-1)**k*x**(2*k+1)/Q(2*k+1) for k in range(terms))
    b=a+(-1)**terms*x**(2*terms+1)/Q(2*terms+1)
    return min(a,b),max(a,b)

def pi_interval():return rounded(plus(scale(atan(Q(1,5)),16),scale(atan(Q(1,239)),-4)))

def sqrt_interval(n):
    shift=2**128;k=isqrt(n*shift*shift)
    assert k*k<n*shift*shift<(k+1)*(k+1)
    return Q(k,shift),Q(k+1,shift)

def bounds():
    trace=json.loads((DATA/'cm_arithmetic_trace_gap_d117.json').read_text())
    old=json.loads((DATA/'cm_quadric_compound_bound_d116.json').read_text())['direct_quadric_budgets']
    intrinsic=json.loads((DATA/'cm_intrinsic_height_review_d104.json').read_text())
    hodge=Q(intrinsic['independent_analytic']['Hodge_height_interval'][1])
    rho=Q(9,19);required=2*(1+6*rho*rho+rho**4)/(1-rho*rho)**2
    assert required<Q(trace['uniform_hyperbolic_trace_lower'])
    pi=pi_interval();assert Q(314159,100000)<pi[0]<pi[1]<Q(314160,100000)
    logpi=(log(pi[0])[0],log(pi[1])[1]);logrho=log(1/rho)
    H=plus((2*hodge,2*hodge),LOG2);assert H[1]<Q(41,10)
    C={1:scale(sqrt_interval(2),2),2:plus(scale(sqrt_interval(3),2),(Q(2),Q(2))),
       3:plus(scale(sqrt_interval(6),2),(Q(4),Q(4)))}
    L=old['maximum_quadric_coefficient_l1_norm'];assert L==42550
    constant=log(2*16*15*L)
    rows=[]
    for n in [1,2,3]:
        logC=(log(C[n][0])[0],log(C[n][1])[1])
        # Combine B=(sqrt(pi)*rho^2)^-1 and the product-coefficient norm
        # C_n/(pi*rho^(2n+4)) with -15*h_Fal <=240*log(2*pi).
        pieces={'CM_fibre_degree':scale(H,240+n),
          'frame_vector_and_Faltings_log2':scale(LOG2,310),
          'net_pi_factor':scale(logpi,120),'quadric_and_path_constant':constant,
          'jet_constant':logC,'disk_radius':scale(logrho,480+2*n)}
        total=plus(*pieces.values());optimistic=plus(*(v for k,v in pieces.items() if k!='disk_radius'))
        base=old['thresholds'][n-1];anchor=base['certified_anchor_lower_beta'];achieved=base['degree16_achieved_lower_beta']
        targets=[]
        for expression in [total,optimistic]:
            lo=17*expression[0]/LOG2[1]-Q(anchor,16)
            hi=17*expression[1]/LOG2[0]-Q(anchor,16)
            N=hi.numerator//hi.denominator+1
            assert N-1<lo<hi<N;targets.append(N)
        rows.append({'order':n,'previous_exact_zero_orders_required':list(range(n)),
          'upper_bound_expression_interval':list(map(str,total)),
          'upper_bound_pieces':{k:list(map(str,v)) for k,v in pieces.items()},
          'degree16_sufficient_integral_jet_lower_beta':targets[0],
          'optimistic_radius_one_same_bound_threshold_beta':targets[1],
          'achieved_degree16_lower_beta':achieved,'certified_anchor_lower_beta':anchor,
          'valuation_gap':targets[0]-achieved,
          'optimistic_radius_one_still_insufficient':targets[1]>achieved,
          'exact_vanishing_proved':False})
    return {'disk_radius':str(rho),'required_trace_for_disk':str(required),'outward_rounding_bits':192,
       'pi_interval':list(map(str,pi)),'log2_interval':list(map(str,LOG2)),
       'coarse_CM_fibre_height_upper_interval':list(map(str,H)),
       'saved_Hodge_height_upper':str(hodge),'maximum_quadric_coefficient_l1_norm':L,
       'total_upper_bound_formula':'(240+n)*H + 310*log(2) + 120*log(pi) + log(480*L) + log(C_n) + (480+2*n)*log(1/rho)',
       'thresholds':rows,'radius_one_is_not_a_certified_embedded_disk':True,
       'radius_only_limit_keeps_all_other_bound_inputs_fixed':True,
       'bounds_are_sufficient_not_universal_necessary_precision':True}

def build():
    b=bounds();print('DISK_VANISHING_BUDGETS|'+json.dumps([{k:v for k,v in x.items() if k not in ['upper_bound_expression_interval','upper_bound_pieces']} for x in b['thresholds']]),flush=True)
    return {'status':'pass','milestone':'D117','budgets':b,
       'actual_precision_increased':False,'positive_quadric_jet_exact_vanishing_proved':False,
       'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
       'sources':[source(p) for p in [Path(__file__),DATA/'cm_arithmetic_trace_gap_d117.json',
           DATA/'cm_quadric_compound_bound_d116.json',DATA/'cm_intrinsic_height_review_d104.json',
           ROOT/'dembele/certificates/cm-compound-height-d116.md',
           ROOT/'dembele/certificates/cm-intrinsic-height-d104.md']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_disk_vanishing_budget_d117.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|447_CM_DISK_VANISHING_BUDGET',flush=True)
