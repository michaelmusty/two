"""D116: integral quadric reduction and direct vanishing-jet budgets.

The universal divisibility, analytic norm estimate and nodal jet theorem are
proved in the report. Exact polynomial controls and rational budgets live here.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import factorial
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([c*x for x in a])
def mul(a,b):
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return trim(z)
def det(a):
    n=len(a);z=[0]
    for perm in permutations(range(n)):
        term=[(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))]
        for i,j in enumerate(perm):term=mul(term,a[i][j])
        z=add(z,term)
    return z
def adj(a):
    n=len(a)
    return [[scale(det([[a[u][v] for v in range(n) if v!=i] for u in range(n) if u!=j]),(-1)**(i+j))
             for j in range(n)] for i in range(n)]
def divide(a,b):
    a=list(map(Q,a));b=list(map(Q,b));out=[Q(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        k=len(a)-len(b);q=a[-1]/b[-1];out[k]=q
        for j,c in enumerate(b):a[k+j]-=q*c
        a=trim(a)
    return trim(out),a

def controls():
    checks=[]
    for g in [3,4]:
        # V_0=-1, V_i=e_i; Q=X_1 X_2-X_1 X_3 vanishes on every V_i.
        E=[[[((i+2)*(j+3)+i*j)%7-3,(-1 if i==0 else int(i-1==j))] for j in range(g)] for i in range(g+1)]
        cofactors=[scale(det([row for j,row in enumerate(E) if j!=i]),(-1)**i) for i in range(g+1)]
        Phi=[[mul(cofactors[i],x) for x in E[i]] for i in range(1,g+1)]
        Delta=det(Phi);S=adj(Phi);degrees=[];negative=False
        vectors=[[int(i==j) for i in range(g)] for j in range(g)]
        vectors += [[int(k in [i,j]) for k in range(g)] for i in range(g) for j in range(i+1,g)]
        for v in vectors:
            coordinates=[]
            for j in range(g):
                z=[0]
                for i in range(g):z=add(z,scale(S[i][j],v[i]))
                coordinates.append(z)
            numerator=mul(coordinates[0],add(coordinates[1],scale(coordinates[2],-1)))
            quotient,remainder=divide(numerator,Delta)
            assert not any(remainder) and all(x.denominator==1 for x in quotient)
            degrees.append(len(quotient)-1)
            _,bad=divide(mul(coordinates[0],coordinates[0]),Delta)
            negative|=any(bad)
        assert max(degrees)==(g-2)*(g+1) and negative
        checks.append({'genus':g,'quadratic_coefficients_controlled':len(vectors),
                       'maximum_reduced_degree':max(degrees),'quadric_not_through_frame_rejected':True})
    # The nodal Euler derivation acts on x^m by m, including the negative y branch.
    for m in range(-30,31):
        for n in [1,2,3]:
            falling=1
            for j in range(n):falling*=m-j
            assert falling%factorial(n)==0
    return {'polynomial_pencil_controls':checks,'nodal_integral_binomial_controls':183}

def budgets():
    candidate=json.loads((DATA/'cm_frame_curve_candidate.json').read_text())
    row_bounds=[sum(abs(x) for x in row) for row in candidate['quadrics']];L=max(row_bounds)
    g=16;d=(g-2)*(g+1)
    # Square the bound to eliminate sqrt(17); no floating logarithms are used.
    numerator=L**2*g**4*2**(4*35+2*20*d)*17**17*39**(4*(g*g-1))
    denominator=21**(2*g*(g+1))
    K=max(0,(numerator.bit_length()-denominator.bit_length())//2)
    while 2**(2*K)*denominator<=numerator:K+=1
    while K and 2**(2*(K-1))*denominator>numerator:K-=1
    assert 2**(2*(K-1))*denominator<=numerator<2**(2*K)*denominator
    assert 16*17<17**2 and 38-17==21 and 38+1==39
    x=Q(1,3);lo=2*sum(x**(2*k+1)/Q(2*k+1) for k in range(64))
    hi=lo+2*x**129/(Q(129)*(1-x*x))
    rows=[]
    for order,functional in [(1,60),(2,81),(3,102)]:
        alpha=Q((d+order+2)*41,10);beta=K+functional+48*(g-1)
        lower=17*beta+17*alpha/hi;upper=17*beta+17*alpha/lo
        threshold=upper.numerator//upper.denominator+1
        assert threshold-1<lower<upper<threshold
        rows.append({'vanishing_jet_order':order,'requires_previous_jets_exactly_zero':list(range(order)),
          'line_coefficient_of_H_CM':d+order+2,'line_negative_coefficient_of_h_Fal':g-1,
          'jet_functional_binary_exponent':functional,'height_bound_alpha':str(alpha),
          'height_bound_beta_log2':beta,'degree16_sufficient_integral_jet_valuation_beta':threshold})
    return {'maximum_quadric_coefficient_l1_norm':L,'quadric_l1_norms':row_bounds,
      'reduced_quadric_tensor_degree_in_evaluations':d,
      'reduced_quadric_tensor_norm_binary_exponent':K,
      'regularizing_radius_in_units_of_B':38,'minor_lower_radius_in_units_of_B':21,
      'row_upper_radius_in_units_of_B':39,'thresholds':rows,
      'thresholds_are_integral_section_valuations_not_ratio_error_digits':True,
      'common_threshold_for_J4':max(row['degree16_sufficient_integral_jet_valuation_beta'] for row in rows)}

def build():
    return {'status':'pass','milestone':'D116','controls':controls(),'direct_quadric_budgets':budgets(),
       'universal_integral_quadric_division_via_companion_proof':True,
       'direct_J4_zero_certificate_via_companion_proof':True,
       'positive_quadric_jet_exact_vanishing_proved':False,
       'third_actual_coarse_jet_computed':False,'candidate_identification_proved':False,
       'target_field_polynomial_constructed':False,'sources':[source(x) for x in [Path(__file__),
         DATA/'cm_frame_curve_candidate.json',DATA/'cm_ratio_jet_review_d106.json',
         ROOT/'dembele/certificates/cm-adjugate-height-d103.md',
         ROOT/'dembele/certificates/cm-intrinsic-height-d104.md',
         DATA/'dyadic_integral_frame_d116.json']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_integral_quadrics_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('DIRECT_QUADRIC_BUDGETS|'+json.dumps(result['direct_quadric_budgets']),flush=True)
    print('PASS|441_CM_INTEGRAL_QUADRICS',flush=True)
