"""D122 test every candidate quadric on the actual P=400 differential jets.

Certified nonzero coefficients are recorded as mismatches, not assertion
failures. Finite zero-containing balls are never promoted to exact zeros.
"""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,filename):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/filename)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
f=module('balls','480_dyadic_multiprecision_balls.py')
provenance=module('provenance','482_dyadic_complete_precision400_bank.py')
logs=module('rigorous_logs','450_cm_disk_exactness_review.py')


def build():
    begin=time.monotonic()
    framepath=DATA/'dyadic_residue_frame400_d122.json';frame=json.loads(framepath.read_text())
    candidatepath=DATA/'cm_frame_curve_candidate.json';candidate=json.loads(candidatepath.read_text())
    integralpath=DATA/'dyadic_integral_frame_d116.json';integral=json.loads(integralpath.read_text())
    budgetpath=DATA/'cm_arithmetic_height_budget_d118.json';budgets=json.loads(budgetpath.read_text())['budgets']
    pairs=candidate['monomial_pairs'];quadrics=candidate['quadrics']
    assert len(pairs)==136 and len(quadrics)==91
    assert all(isinstance(c,int) for row in quadrics for c in row)
    assert all(16*((abs(c)&-abs(c)).bit_length()-1)<f.PRECISION for row in quadrics for c in row if c)
    scalar=integral['D103_sections_over_D115_frame_scalar_valuation_beta'];det=integral['frame_determinant_valuation_beta']
    assert [scalar,det]==[3920,4200]
    points=[];mismatches=[]
    for ci,row in enumerate(frame['CM_values']):
        jet=[[f.restore(x) for x in row] for row in row['actual_residue_frame_coarse_jets']]
        monomials=[]
        for i,j in pairs:
            coefficients=[]
            for n in range(4):
                value=f.Ball()
                for k in range(n+1):value=value+jet[k][i]*jet[n-k][j]
                coefficients.append(value)
            monomials.append(coefficients)
        m=frame['canonical_fibre_valuations_beta'][ci];rows=[]
        assert m==integral['canonical_fibre_coarse_generator_valuations_beta'][ci]
        for qi,quadric in enumerate(quadrics):
            values=[]
            for n in range(4):
                z=f.Ball()
                for c,monomial in zip(quadric,monomials):
                    if c:z=z+monomial[n].scale_integer(c)
                if z.known_nonzero():mismatches.append({'CM_index':ci,'quadric_index':qi,'order':n,**z.summary()})
                values.append({'coarse_coefficient':z.saved(),'coarse_known_nonzero':z.known_nonzero(),
                    'conditional_intrinsic_jet_lower_beta':z.lower()+2*scalar-det-(n+2)*m,
                    'intrinsic_interpretation_requires_exact_zero_orders':list(range(n)),
                    'required_exact_vanishing_already_proved':n<=1})
            rows.append(values)
        lows=[min(row[n]['conditional_intrinsic_jet_lower_beta'] for row in rows) for n in range(4)]
        points.append({'CM_index':ci,'fibre_generator_valuation_beta':m,'all_91_quadric_coefficients':rows,
            'minimum_lower_beta_by_order':lows})
        if ci%4==0:print(f'P400_QUADRICS|CM={ci}; minima={lows}; mismatches={len(mismatches)}; seconds={time.monotonic()-begin:.3f}',flush=True)
    comparison=[]
    for n in (1,2,3):
        old=budgets['thresholds'][n-1];F=list(map(Q,old['upper_bound_expression_interval']))
        achieved=min(row['minimum_lower_beta_by_order'][n] for row in points[1:])
        anchor=points[0]['minimum_lower_beta_by_order'][n]
        low=(272*F[0]/logs.L2[1]-anchor)/16
        high=(272*F[1]/logs.L2[0]-anchor)/16
        target=high.__floor__()+1;assert target-1<low<high<target
        sufficient=(16*achieved+anchor)*logs.L2[0]/272>F[1]
        comparison.append({'order':n,'degree16_achieved_lower_beta':achieved,'anchor_achieved_lower_beta':anchor,
            'sufficient_nonanchor_beta_with_new_anchor':target,'gap':target-achieved,
            'inequality_is_sufficient':sufficient,'intrinsic_interpretation_conditional_on_previous_orders':n>1,
            'exact_vanishing_proved':False})
    assert all(not row['inequality_is_sufficient'] for row in comparison)
    result={'status':'pass','milestone':'D122','working_precision_pi':400,'quadric_count':91,
        'CM_point_count':17,'coarse_orders':[0,1,2,3],'CM_values':points,
        'positive_coefficients_tested':91*17*3,'all_coefficients_tested':91*17*4,
        'candidate_mismatch_certified':bool(mismatches),'certified_mismatches':mismatches,
        'comparison_with_sufficient_bounds':comparison,'order_zero_exact_vanishing_via_certified_CM_frame':True,
        'positive_quadric_jet_exact_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'wall_seconds':time.monotonic()-begin,
        'sources':[provenance.source(x) for x in [Path(__file__),Path(f.__file__),Path(provenance.__file__),
            Path(logs.__file__),framepath,candidatepath,integralpath,budgetpath]]}
    print('P400_QUADRIC_RESULT|'+json.dumps({'mismatches':len(mismatches),'bounds':comparison,
        'wall_seconds':result['wall_seconds']}),flush=True)
    return result


if __name__=='__main__':
    out=DATA/'dyadic_integral_quadrics400_d122.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|484_DYADIC_PRECISION400_QUADRICS',flush=True)
