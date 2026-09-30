"""D116: explicit complementary minors sharpen the direct quadric norm bound.

The adjacent-pair polynomial identity proves integral division and bounds the
quotient without a regularizing complex pencil. Existing anchor bounds are
included as finite zero contributions, with the higher-jet hypotheses retained.
"""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('quadric',ROOT/'dembele/pari/441_cm_integral_quadrics.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)

def product(xs):
    z=[1]
    for x in xs:z=p.mul(z,x)
    return z

def controls():
    records=[]
    for g in [3,4]:
        E=[[[((i+2)*(j+3)+i*j)%7-3,(-1 if i==0 else int(i-1==j))] for j in range(g)] for i in range(g+1)]
        M=E[1:];A=p.adj(M);D=p.det(M)
        c=[p.scale(p.det([row for j,row in enumerate(E) if j!=i]),(-1)**i) for i in range(1,g+1)]
        assert all(c[i]==p.scale(sum_polynomials(p.mul(E[0][k],A[k][i]) for k in range(g)),-1) for i in range(g))
        vectors=[[int(i==j) for i in range(g)] for j in range(g)]
        vectors += [[int(k in [i,j]) for k in range(g)] for i in range(g) for j in range(i+1,g)]
        count=0
        for x in vectors:
            w=[sum_polynomials(p.scale(A[k][i],x[k]) for k in range(g)) for i in range(g)]
            for i in range(g):
                for j in range(g):
                    for k in range(j+1,g):
                        if i in [j,k]:continue
                        cross=p.add(p.mul(c[k],w[j]),p.scale(p.mul(c[j],w[k]),-1))
                        J,remainder=p.divide(cross,D)
                        assert not any(remainder) and all(a.denominator==1 for a in J)
                        Tij=p.mul(product(c[a] for a in range(g) if a not in [i,j]),p.mul(w[i],w[j]))
                        Tik=p.mul(product(c[a] for a in range(g) if a not in [i,k]),p.mul(w[i],w[k]))
                        lhs=p.add(Tij,p.scale(Tik,-1))
                        rhs=p.mul(D,p.mul(product(c[a] for a in range(g) if a not in [i,j,k]),p.mul(w[i],J)))
                        assert lhs==rhs;count+=1
        records.append({'genus':g,'adjacent_pair_polynomial_identities':count,
                        'integral_complementary_minor_quotients':True})
    return records

def sum_polynomials(xs):
    z=[0]
    for x in xs:z=p.add(z,x)
    return z

def budgets():
    old=json.loads((DATA/'cm_integral_quadrics_d116.json').read_text())['direct_quadric_budgets']
    measured=json.loads((DATA/'dyadic_integral_quadric_jets_d116.json').read_text())['comparison_with_sufficient_bounds']
    g=16;L=old['maximum_quadric_coefficient_l1_norm'];d=(g-2)*(g+1)
    bound=2*g*(g-1)*L*2**(2*35+20*d);K=bound.bit_length()
    assert 2**(K-1)<=bound<2**K and K==4855
    lo=sum(Q(1,k*2**k) for k in range(1,257));hi=lo+Q(1,257*2**256)
    rows=[]
    for n,functional in [(1,60),(2,81),(3,102)]:
        alpha=Q((d+n+2)*41,10);beta=K+functional+720
        achieved=measured[n-1]['degree16_achieved_lower_beta'];anchor=measured[n-1]['anchor_achieved_lower_beta']
        targets=[]
        for correction in [Q(0),Q(anchor,272)]:
            lower=17*(beta-correction)+17*alpha/hi;upper=17*(beta-correction)+17*alpha/lo
            N=upper.numerator//upper.denominator+1
            assert N-1<lower<upper<N;targets.append(N)
        rows.append({'vanishing_jet_order':n,'requires_previous_jets_exactly_zero':list(range(n)),
            'line_coefficient_of_H_CM':d+n+2,'line_negative_coefficient_of_h_Fal':15,
            'jet_functional_binary_exponent':functional,'height_bound_alpha':str(alpha),
            'height_bound_beta_log2':beta,'degree16_sufficient_lower_beta_without_anchor':targets[0],
            'certified_anchor_lower_beta':anchor,'anchor_finite_contribution_coefficient_log2':str(Q(anchor,272)),
            'degree16_sufficient_lower_beta_with_anchor':targets[1],
            'degree16_achieved_lower_beta':achieved,'valuation_gap':targets[1]-achieved,
            'exact_vanishing_proved':False})
    return {'maximum_quadric_coefficient_l1_norm':L,
       'tensor_norm_bound_integer':str(bound),'reduced_quadric_tensor_norm_binary_exponent':K,
       'previous_pencil_bound_binary_exponent':old['reduced_quadric_tensor_norm_binary_exponent'],
       'reduced_quadric_tensor_degree_in_evaluations':d,'maximum_adjacent_pair_path_length':2,
       'thresholds':rows,'common_sufficient_lower_beta_with_anchor':max(x['degree16_sufficient_lower_beta_with_anchor'] for x in rows),
       'thresholds_are_integral_section_valuations_not_ratio_error_digits':True}

def build():
    result={'status':'pass','milestone':'D116','polynomial_controls':controls(),
       'direct_quadric_budgets':budgets(),'complementary_minor_norm_proof_in_companion_report':True,
       'third_actual_coarse_jet_computed':True,'positive_quadric_jet_exact_vanishing_proved':False,
       'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
       'sources':[p.source(x) for x in [Path(__file__),Path(p.__file__),
             DATA/'cm_integral_quadrics_d116.json',DATA/'dyadic_integral_quadric_jets_d116.json',
             ROOT/'dembele/pari/433_cm_compound_height.py']]}
    print('SHARP_DIRECT_QUADRIC_BUDGETS|'+json.dumps(result['direct_quadric_budgets']['thresholds']),flush=True)
    return result

if __name__=='__main__':
    result=build();out=DATA/'cm_quadric_compound_bound_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|444_CM_QUADRIC_COMPOUND_BOUND',flush=True)
