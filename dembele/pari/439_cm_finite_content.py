"""D116: subtract certified dyadic common-zero content from the jet height bounds.

The Galois averaging over the 17 split dyadic primes of H/M is justified in
the companion report. The finite contents are computed in stable fibre bases.
"""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('integral',ROOT/'dembele/pari/438_dyadic_integral_frame.py')
i=importlib.util.module_from_spec(s);s.loader.exec_module(i);f=i.f;r=i.r

def determinant3(rows):
    a,b,c=rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def build():
    integral=json.loads((DATA/'dyadic_integral_frame_d116.json').read_text())
    coarse=json.loads((DATA/'dyadic_precision200_d115.json').read_text())
    comparison=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    height=json.loads((DATA/'cm_compound_height_d116.json').read_text())
    matrix=[[r.restore(x) for x in row] for row in comparison['change_of_basis']]
    factor=integral['D103_sections_over_D115_frame_scalar_valuation_beta'];delta=integral['frame_determinant_valuation_beta']
    content1=[x['reduced_integral_Gaussian_vector_lower_beta'] for x in integral['reduced_Gaussian_content']]
    content2=[];details=[]
    for ci,raw in enumerate(coarse['CM_values']):
        jet=f.multiply([[f.center(cs,coarse['coarse_error_beta'][n]) for cs in raw['coarse_coefficients_beta'][n]] for n in range(3)],matrix)
        m=integral['canonical_fibre_coarse_generator_valuations_beta'][ci]
        assert jet[0][0].known_nonzero()
        fvalue=factor+jet[0][0].v-m
        G=jet[0][0]*jet[1][1]-jet[0][1]*jet[1][0]
        gamma=2*factor-delta+G.lower()-3*m
        denominator=16+delta+3*gamma
        nums=[]
        for j in range(1,16):
            wr=determinant3([[row[k] for k in [0,1,j]] for row in [jet[0],jet[1],[f.TWO*x for x in jet[2]]]])
            kappa=3*factor-2*delta+wr.lower()-6*m
            nums.append(3*fvalue+kappa)
        common=min([denominator]+nums)
        content2.append(common);details.append({'CM_index':ci,'s1_value_beta':fvalue,
            'denominator_lower_beta':denominator,'numerator_lower_beta':nums,'common_lower_beta':common})
    lo,hi=map(Q,[height['height_budgets']['log2_lower'],height['height_budgets']['log2_upper']])
    contents=[content1,content2];rows=[]
    for base,content in zip(height['height_budgets']['thresholds'],contents):
        correction=Q(sum(content),272)
        alpha=Q(base['actual_height_bound_alpha']);beta=Q(base['actual_height_bound_beta_log2'])-correction
        ceiling=(alpha+beta*hi).numerator//(alpha+beta*hi).denominator+1
        assert ceiling-1<alpha+beta*lo<alpha+beta*hi<ceiling
        A=alpha+base['candidate_height_upper'];B=beta+1
        low=17*B+17*A/hi;high=17*B+17*A/lo
        threshold=high.numerator//high.denominator+1
        assert threshold-1<low<high<threshold
        rows.append({'order':base['order'],'common_content_beta_at_17_CM_points':content,
            'subtracted_coefficient_of_log2':str(correction),
            'actual_height_bound_alpha':str(alpha),'actual_height_bound_beta_log2':str(beta),
            'actual_height_strict_integer_upper':ceiling,'candidate_height_upper':base['candidate_height_upper'],
            'difference_height_bound_alpha':str(A),'difference_height_bound_beta_log2':str(B),
            'degree16_sufficient_beta_error':threshold,'degree16_sufficient_integer_pi_error':(threshold+1)//2})
    print('FINITE_CONTENT_BUDGETS|'+json.dumps(rows),flush=True)
    return {'status':'pass','milestone':'D116','CM_splitting_field_degree':272,
       'dyadic_primes_in_H':17,'dyadic_ramification_index':16,'dyadic_residue_degree':1,
       'second_ratio_content_details':details,'thresholds':rows,
       'integral_lattice_and_Galois_averaging_via_companion_proof':True,
       'odd_prime_common_zeros_discarded':True,'CM_horizontal_residue_index_computed':False,
       'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
       'sources':[f.coarse.source(x) for x in [Path(__file__),Path(i.__file__),
          DATA/'dyadic_integral_frame_d116.json',DATA/'dyadic_precision200_d115.json',
          DATA/'dyadic_comparison200_d115.json',DATA/'cm_compound_height_d116.json',
          ROOT/'dembele/certificates/cm-frame-arithmetic-d105.md',
          ROOT/'dembele/certificates/cm-rational-frame-jets-d106.md']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_finite_content_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|439_CM_FINITE_CONTENT',flush=True)
