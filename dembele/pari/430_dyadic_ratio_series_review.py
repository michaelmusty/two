"""D115: review the actual residue frame and ratio jets by formal series division."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('frame',ROOT/'dembele/pari/427_dyadic_second_order_comparison.py')
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)

def restore(row):return f.Ball(tuple(row['unit_beta']),row['beta_exponent'] or 0,row['error_beta'])

def calculations():
    path=DATA/'dyadic_comparison200_d115.json';p=json.loads(path.read_text())
    coarsepath=DATA/'dyadic_precision200_d115.json';data=json.loads(coarsepath.read_text())
    reviewpath=DATA/'dyadic_precision200_review_d115.json';review=json.loads(reviewpath.read_text())
    assert review['status']=='pass' and review['same_branch_and_all_refined_centers_verified']
    for packet in [p,data,review]:f.coarse.checked(packet['sources'])
    assert p['frame_computed'] and not p['candidate_identification_proved'] and not p['candidate_mismatch_certified']
    transform=[[restore(x) for x in row] for row in p['change_of_basis']]
    roots=json.loads((DATA/'dyadic_cm_matching_review_d112.json').read_text())['certificates']['roots_and_frame']
    eta=[[f.center(cs,roots['rational_residue_frame_error_beta']) for cs in row] for row in roots['rational_residue_frame_values']]
    counts=[0,0];minima=[10**9,10**9];pivots=[]
    for ci,row in enumerate(data['CM_values']):
        raw=[[f.center(cs,data['coarse_error_beta'][j]) for cs in row['coarse_coefficients_beta'][j]] for j in range(3)]
        jet=f.multiply(raw,transform)
        # Projective frame check without choosing a local scalar or dividing by W.
        assert all(not (jet[0][j]*eta[ci][0]-jet[0][0]*eta[ci][j]).known_nonzero() for j in range(16))
        comparison=p['comparisons'][ci]
        if not comparison['comparison_possible']:continue
        assert jet[0][0].known_nonzero()
        ratios=[]
        for j in range(16):
            r0=jet[0][j]/jet[0][0]
            r1=(jet[1][j]-r0*jet[1][0])/jet[0][0]
            r2=(jet[2][j]-r0*jet[2][0]-r1*jet[1][0])/jet[0][0]
            ratios.append([r0,r1,r2])
        t1,t2=ratios[1][1:];assert t1.known_nonzero();pivots.append(ci)
        # Independent reversion t=t1*u+t2*u^2, instead of Gaussian formulas.
        for j in range(16):
            a1=ratios[j][1]/t1
            a2=(ratios[j][2]-a1*t2)/(t1*t1)
            for n,actual in enumerate([a1,a2]):
                record=comparison['orders'][n]
                assert not (actual-restore(record['actual'][j])).known_nonzero()
                reference=restore(record['candidate'][j]);difference=restore(record['differences'][j])
                assert not (actual-reference).known_nonzero()
                assert not difference.known_nonzero()
                counts[n]+=1;minima[n]=min(minima[n],difference.error)
    assert pivots==list(range(1,17)) and counts==[256,256] and minima==[101,70]
    assert data['CM_values'][0]['certified_valuations_beta'][0][0]==296
    print(f'RATIO_SERIES_REVIEW|{counts} entries; saved error bounds {minima}; all direct series reversion checks pass',flush=True)
    return {'status':'pass','milestone':'D115','actual_ratio_orders':[1,2],
        'CM_indices_with_certified_G12_pivot':pivots,'comparison_entries_by_order':counts,
        'minimum_difference_error_beta':minima,'mismatch_count':0,
        'formal_series_division_and_reversion_checks':True,'projective_residue_frame_checks':17,
        'global_G12_nonvanishing_by_D106_and_CM_transitivity':True,
        'W_G12_numerically_resolved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,
        'sources':[f.coarse.source(x) for x in [Path(__file__),Path(f.__file__),path,coarsepath,reviewpath,
                    DATA/'dyadic_cm_matching_review_d112.json']]}

def main():
    result=calculations();out=DATA/'dyadic_ratio_series_review_d115.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|430_DYADIC_RATIO_SERIES_REVIEW',flush=True)

if __name__=='__main__':main()
