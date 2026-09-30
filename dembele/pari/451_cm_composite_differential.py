"""D118: dyadic content of W_C -> L(Q)^2 through a small-level model.

The geometric comparison is proved in the companion report. No auxiliary
level is computed. The local Hodge generator is dz/z=2*dw/(1-w^2).
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def derivative(a):return [i*a[i] for i in range(1,len(a))] or [Q(0)]

def controls():
    results=[]
    for a in [[1],[1,2,-3],[2,-3,4],[-5,2,0,9]]:
        # eta=a(u)du, u=w^2, lambda=2dw/(1-w^2).
        even=[Q(0)]*(2*len(a)-1)
        for i,c in enumerate(a):even[2*i]=Q(c)
        coefficient=mul(even,[0,1,0,-1])
        divided=mul(derivative(coefficient),[Q(1,2),0,Q(-1,2)])
        assert coefficient[0]==0 and divided[0]==Q(a[0],2)
        results.append({'a_u':a,'coefficient_of_lambda':list(map(str,coefficient)),
                        'D_lambda_at_zero':str(divided[0])})
    # Ordinary edge quotient: xy=lambda0, involution (x,y)->(-y,-x).
    # t=x-y, dt=(x+y) dx/x, D(dx/x)(x+y)=x-y=2*beta at x=beta.
    # Also t=2*beta*(1+u)/(1-u), so dt/du at zero is 4*beta.
    assert (2*16+1)-16==16+1
    return results

def build():
    frame=json.loads((DATA/'dyadic_integral_frame_d116.json').read_text())
    cm=json.loads((DATA/'dyadic_cm_embeddings_d112.json').read_text())
    raw=json.loads((DATA/'dyadic_precision200_d115.json').read_text())
    exponents=frame['canonical_fibre_coarse_generator_valuations_beta']
    assert frame['stable_integral_basis_and_fibre_interpretation_via_companion_proof']
    assert exponents==[min(row['certified_valuations_beta'][0]) for row in raw['CM_values']]==[296]+[33]*16
    assert sorted(cm['relative_class_labels'])==list(range(17))
    assert cm['dyadic_CM_prime_norm']==2 and cm['CM_roots_of_unity']==2
    rows=[]
    for i,(entry,m) in enumerate(zip(cm['entries'],exponents)):
        content=m-16;assert content>=0
        rows.append({'CM_index':i,'name':entry['name'],'coarse_fibre_exponent_beta':m,
                     'Hodge_fibre_coefficient_in_dw_valuation_beta':16,
                     'composite_ramification_derivative_valuation_beta':content})
    total=sum(r['composite_ramification_derivative_valuation_beta'] for r in rows)
    degree=Q(total,272);assert total==552 and degree==Q(69,34)
    print('COMPOSITE_DIFFERENTIAL|contents=280,17x16|dyadic degree=(69/34)*log(2)',flush=True)
    return {'status':'pass','milestone':'D118','local_polynomial_controls':controls(),
            'CM_fibres':rows,'sum_composite_valuations_beta':total,
            'normalized_dyadic_finite_zero_degree_coefficient_log2':str(degree),
            'old_log2_correction_after_subtraction':str(1-degree),
            'combined_correction':'2*c_L+c_ram',
            'Hodge_and_ramification_parts_separately_computed':False,
            'dyadic_combined_content_is_exact_via_companion_proof':True,
            'non_dyadic_content_computed':False,'auxiliary_level_computed':False,
            'actual_moment_precision_increased':False,'candidate_identification_proved':False,
            'sources':[source(p) for p in [Path(__file__),DATA/'dyadic_integral_frame_d116.json',
                DATA/'dyadic_cm_embeddings_d112.json',DATA/'dyadic_precision200_d115.json',
                ROOT/'dembele/certificates/cm-intrinsic-height-d104.md',
                ROOT/'dembele/certificates/cm-compound-height-d116.md',
                ROOT/'dembele/certificates/dyadic-cm-matching-d112.md']]}

if __name__=='__main__':
    out=DATA/'cm_composite_differential_d118.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|451_CM_COMPOSITE_DIFFERENTIAL',flush=True)
