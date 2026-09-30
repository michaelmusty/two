"""D116: evaluate all 91 reduced integral quadrics through the third CM jet.

Only the first jet is already an intrinsic integral section. The second and
third acquire that interpretation if their preceding jets vanish exactly.
Finite enclosures are never promoted to exact zeros by this calculation.
"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('series',ROOT/'dembele/pari/430_dyadic_ratio_series_review.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r);f=r.f

def calculations():
    coarse=json.loads((DATA/'dyadic_third_coarse_jet_d116.json').read_text())
    comparison=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    integral=json.loads((DATA/'dyadic_integral_frame_d116.json').read_text())
    candidate=json.loads((DATA/'cm_frame_curve_candidate.json').read_text())
    budget=json.loads((DATA/'cm_integral_quadrics_d116.json').read_text())['direct_quadric_budgets']
    change=[[r.restore(x) for x in row] for row in comparison['change_of_basis']]
    scalar=integral['D103_sections_over_D115_frame_scalar_valuation_beta']
    delta=integral['frame_determinant_valuation_beta'];assert [scalar,delta]==[3920,4200]
    pairs=candidate['monomial_pairs'];quadrics=candidate['quadrics'];assert len(quadrics)==91
    scalars={c:f.rational(c) for row in quadrics for c in row if c}
    points=[]
    for ci,row in enumerate(coarse['CM_values']):
        jet=f.multiply([[f.center(cs,coarse['coarse_error_beta'][n]) for cs in row['coarse_coefficients_beta'][n]] for n in range(4)],change)
        monomials=[]
        for i,j in pairs:
            entries=[]
            for n in range(4):
                z=f.Ball()
                for k in range(n+1):z=z+jet[k][i]*jet[n-k][j]
                entries.append(z)
            monomials.append(entries)
        m=integral['canonical_fibre_coarse_generator_valuations_beta'][ci]
        rows=[]
        for Q in quadrics:
            values=[]
            for n in range(4):
                z=f.Ball()
                for c,monomial in zip(Q,monomials):
                    if c:z=z+scalars[c]*monomial[n]
                assert not z.known_nonzero(),(ci,n,z.summary())
                values.append({'coarse_coefficient':z.saved(),
                   'conditional_intrinsic_jet_lower_beta':z.lower()+2*scalar-delta-(n+2)*m,
                   'intrinsic_interpretation_requires_exact_zero_orders':list(range(n)),
                   'required_exact_vanishing_already_proved':n<=1})
            rows.append(values)
        lows=[min(q[n]['conditional_intrinsic_jet_lower_beta'] for q in rows) for n in range(4)]
        points.append({'CM_index':ci,'fibre_generator_valuation_beta':m,
                       'all_91_quadric_coefficients':rows,'minimum_lower_beta_by_order':lows})
    summaries=[]
    for n in [1,2,3]:
        target=budget['thresholds'][n-1]['degree16_sufficient_integral_jet_valuation_beta']
        achieved=min(p['minimum_lower_beta_by_order'][n] for p in points[1:])
        summaries.append({'order':n,'degree16_achieved_lower_beta':achieved,
            'anchor_achieved_lower_beta':points[0]['minimum_lower_beta_by_order'][n],
            'degree16_sufficient_lower_beta':target,'valuation_gap':target-achieved,
            'intrinsic_integral_interpretation_conditional_on_previous_orders':n>1,
            'exact_vanishing_proved':False})
        assert achieved<target
    print('INTEGRAL_QUADRIC_JETS|'+json.dumps(summaries),flush=True)
    return {'status':'pass','milestone':'D116','quadric_count':91,'CM_point_count':17,
       'coarse_orders':[0,1,2,3],'CM_values':points,'comparison_with_sufficient_bounds':summaries,
       'order_zero_exact_vanishing_via_certified_CM_frame':True,
       'positive_quadric_jet_exact_vanishing_proved':False,'candidate_mismatch_certified':False,
       'third_actual_coarse_jet_computed':True,'candidate_identification_proved':False,
       'target_field_polynomial_constructed':False,
       'sources':[f.coarse.source(x) for x in [Path(__file__),Path(r.__file__),Path(f.__file__),
           DATA/'dyadic_third_coarse_jet_d116.json',DATA/'dyadic_comparison200_d115.json',
           DATA/'dyadic_integral_frame_d116.json',DATA/'cm_frame_curve_candidate.json',
           DATA/'cm_integral_quadrics_d116.json']]}

if __name__=='__main__':
    result=calculations();out=DATA/'dyadic_integral_quadric_jets_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('PASS|443_DYADIC_INTEGRAL_QUADRIC_JETS',flush=True)
