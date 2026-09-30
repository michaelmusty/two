"""D115 final provenance audit and replay of the ratio-series certificate."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_strategy_review_d115.json'
REPORT=ROOT/'dembele/certificates/dyadic-comparison-and-strategy-d115.md'
s=importlib.util.spec_from_file_location('series',ROOT/'dembele/pari/430_dyadic_ratio_series_review.py')
series=importlib.util.module_from_spec(s);s.loader.exec_module(series)
source,checked=series.f.coarse.source,series.f.coarse.checked

def build():
    prior_path=DATA/'dyadic_coarse_review_d114.json';prior=json.loads(prior_path.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==713
    paths=checked(prior['sources'])+[prior_path,Path(__file__),REPORT,DATA/'dyadic_comparison_sources_d115.json']
    result=series.calculations();saved=json.loads((DATA/'dyadic_ratio_series_review_d115.json').read_text())
    assert result==saved
    budget=json.loads((DATA/'dyadic_exactness_budget_d115.json').read_text());checked(budget['sources'])
    lo,hi=map(Q,[budget['log2_lower'],budget['log2_upper']]);N=64;x=Q(1,3)
    assert lo==2*sum(x**(2*k+1)/Q(2*k+1) for k in range(N))
    assert hi==lo+2*x**(2*N+1)/(Q(2*N+1)*(1-x*x))
    for row in budget['thresholds']:
        B=Q(row['difference_height_upper'])
        for name,m in [('rational_anchor_only',272),('degree16_place_only',17),('both_places_uniform_beta_error',16)]:
            threshold=row[name]['sufficient_beta_error']
            assert threshold*lo>m*B and (threshold-1)*hi<m*B
    jobs=[]
    for p in sorted(DATA.glob('*d115*')):
        if p.name.startswith('dyadic_strategy_review_d115'):continue
        assert p.is_file();paths.append(p)
        if p.name.endswith('.job.json'):
            job=json.loads(p.read_text());assert job['timeout_seconds']==180 and job['timeout_terminates_process_group']
            paths+=checked(job['sources']+[job['log']])
            if job['status']=='pass':
                assert job['wall_seconds']<180;paths+=checked([job['driver']])
            else:
                assert job['status']=='failed'
                snapshot=p.with_name(p.name.replace('.job.json','_failed.py'))
                assert source(snapshot)['sha256']==job['driver']['sha256'];paths.append(snapshot)
            jobs.append({'receipt':p.name,'status':job['status'],'wall_seconds':job['wall_seconds']})
        elif p.suffix=='.json':
            record=json.loads(p.read_text())
            hashes=[v for v in record.get('sources',[]) if isinstance(v,dict) and 'sha256' in v]
            paths+=checked(hashes)
    for number in range(417,431):
        matches=list((ROOT/'dembele/pari').glob(f'{number}_*.py'));assert len(matches)==1;paths+=matches
    assert sum(j['status']=='pass' for j in jobs)==24 and sum(j['status']=='failed' for j in jobs)==4
    return {'status':'pass','milestone':'D115','D114_source_hashes_checked_unchanged':713,
      'certificates':{'ratio_series':result,'exactness_budgets':budget},
      'actual_harmonic_to_rational_residue_frame_computed':True,
      'actual_rational_frame_ratio_orders_computed':[1,2],
      'CM_indices_with_numerically_certified_G12':list(range(1,17)),
      'common_G12_chart_on_CM_divisor_via_rationality_and_transitivity':True,
      'actual_candidate_difference_error_beta':[101,70],
      'candidate_mismatch_certified':False,'candidate_identification_proved':False,
      'target_field_polynomial_constructed':False,
      'next_requirement':'An exact arithmetic identification certificate, not another default precision pilot.',
      'bounded_jobs':jobs,'sources':[source(p) for p in sorted(set(x.resolve() for x in paths))]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.check:previous=json.loads(OUT.read_text());checked(previous['sources'])
    result=build()
    if a.check:assert result==previous
    else:assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','sources':len(result['sources']),'D114_preserved':713,
                     'ratio_difference_bounds_beta':[101,70],'candidate_identification':False}),flush=True)
    print('PASS|431_DYADIC_STRATEGY_REVIEW',flush=True)

if __name__=='__main__':main()
