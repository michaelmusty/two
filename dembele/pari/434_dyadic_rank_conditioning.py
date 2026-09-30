"""D116: add the exact CM constant information and diagnose J3 conditioning.

Candidate-centered higher-precision trials are explicitly predictions, never
actual Shimura evaluations. The actual packet is kept separate throughout.
"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('rank',ROOT/'dembele/pari/432_dyadic_jet_rank.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
f=r.f

def setup():
    packet=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    roots=json.loads((DATA/'dyadic_cm_matching_review_d112.json').read_text())['certificates']['roots_and_frame']
    constants=[]
    for ci in [0,1]:
        eta=[f.center(cs,roots['rational_residue_frame_error_beta']) for cs in roots['rational_residue_frame_values'][ci]]
        constants.append([x/eta[0] for x in eta])
    return packet['comparisons'][1]['orders'],constants

def matrix(orders,constants,gain=None):
    positive=[]
    for order in orders:
        if gain is None:positive.append([r.series.restore(x) for x in order['actual']])
        else:
            row=[]
            for actual,reference in zip(order['actual'],order['candidate']):
                x=r.series.restore(reference);error=actual['error_beta']+gain
                assert error<=x.error
                row.append(f.Ball(x.u,x.v if x.u!=f.Z else 0,error))
            positive.append(row)
    r0=constants[1];r1,r2=positive;pairs=[(i,j) for i in range(16) for j in range(i,16)]
    rows=[[] for _ in range(49)];monomial_jets=[]
    for i,j in pairs:
        anchor=r.coefficients(constants[0][i]*constants[0][j])
        assert all(x.v>=x.e for x in anchor[1:])
        rows[0].append(anchor[0])
        jets=[r0[i]*r0[j],r0[i]*r1[j]+r1[i]*r0[j],r0[i]*r2[j]+r1[i]*r1[j]+r2[i]*r0[j]]
        monomial_jets.append(jets)
        for n,jet in enumerate(jets):
            for k,x in enumerate(r.coefficients(jet)):rows[1+16*n+k].append(x)
    return rows,pairs,monomial_jets

def residuals(pairs,jets):
    packet=json.loads((DATA/'cm_frame_curve_candidate.json').read_text())
    assert [tuple(x) for x in packet['monomial_pairs']]==pairs
    result=[]
    for row in packet['quadrics']:
        values=[]
        for order in [1,2]:
            value=f.Ball()
            for c,monomial in zip(row,jets):
                if c:
                    x=monomial[order]
                    # Multiplication by an exact integer retains its extra 2-adic valuation.
                    v=(abs(c)&-abs(c)).bit_length()-1
                    term=f.Ball(f.R.scale(x.u,c),x.v if x.u!=f.Z else 0,x.error+16*v)
                    value=value+term
            assert not value.known_nonzero();values.append(value.saved())
        result.append(values)
    return result

def build():
    orders,constants=setup();actual,pairs,jets=matrix(orders,constants)
    actual_certificate=r.rank_certificate(actual)
    direct=residuals(pairs,jets)
    print('ACTUAL_AUGMENTED_RANK|'+str(actual_certificate['rank_lower_bound']),flush=True)
    trials=[]
    for gain in [0,32,64,96,128,160,192]:
        predicted,_,_=matrix(orders,constants,gain)
        certificate=r.rank_certificate(predicted)
        row={'hypothetical_additional_beta_digits':gain,'predicted_rank_lower_bound':certificate['rank_lower_bound'],
             'is_actual_precision_certificate':False,'pivots':certificate['pivots']}
        trials.append(row);print('CANDIDATE_ONLY_CONDITIONING|'+str(gain)+'|'+str(certificate['rank_lower_bound']),flush=True)
        if certificate['rank_lower_bound']==45:break
    return {'status':'pass','milestone':'D116','matrix_shape':[49,136],
       'matrix_rows':'W constant coefficient, then three degree-16-place blocks',
       'actual_matrix_Q2_balls':[[x.saved() for x in row] for row in actual],
       'actual_rank_certificate':actual_certificate,
       'direct_actual_quadric_residuals_orders_1_2':direct,
       'minimum_quadric_residual_error_beta':[min(x[n]['error_beta'] for x in direct) for n in range(2)],
       'candidate_only_conditioning_trials':trials,
       'actual_J3_rank_45_certified':actual_certificate['rank_lower_bound']==45,
       'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
       'sources':[f.coarse.source(p) for p in [Path(__file__),Path(r.__file__),
          DATA/'dyadic_comparison200_d115.json',DATA/'dyadic_cm_matching_review_d112.json',
          DATA/'cm_frame_curve_candidate.json']]}

if __name__=='__main__':
    result=build();out=DATA/'dyadic_rank_conditioning_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|434_DYADIC_RANK_CONDITIONING',flush=True)
