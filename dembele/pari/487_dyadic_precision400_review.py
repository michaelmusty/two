"""D122 final review: bind independent arithmetic phases and all provenance.

Source 486 supplies the independent mathematical calculations. This driver
checks their complete coverage and freezes the final manifest. --check
replays that manifest, without overwriting or rerunning completed jobs.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_precision400_review_d122.json'


def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    return {'path':str(path),'sha256':h.hexdigest()}


def checked(rows):
    result=[]
    for row in rows:
        assert source(row['path'])==row,row['path'];result.append(Path(row['path']))
    return result


def build():
    priorpath=DATA/'dyadic_precision400_checkpoint_d122.json'
    prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==1844
    assert not prior['independent_mathematical_review_complete']
    paths=checked(prior['sources'])+[priorpath,Path(__file__),
        ROOT/'dembele/certificates/dyadic-precision400-d122.md',
        DATA/'dyadic_precision400_review_sources_d122.json']
    olderpath=DATA/'dyadic_schur_review_d121.json';older=json.loads(olderpath.read_text())
    assert len(older['sources'])==1079
    paths+=checked(older['sources'])+[olderpath]
    certificates={}
    names=['roots','moments','comparison']+[f'coarse_{first:02d}_{first+3:02d}' for first in (0,4,8,12)]
    for name in names:
        path=DATA/f'dyadic_precision400_audit_{name}_d122.json';packet=json.loads(path.read_text())
        assert packet['status']=='pass' and packet['phase']==name
        paths+=[path]+checked(packet['sources']);certificates[name]=packet['certificates']
    roots=certificates['roots'];moments=certificates['moments'];comparison=certificates['comparison']
    assert roots['eta_values_cross_multiplied']==272 and roots['eta_error_beta']==21168
    assert moments['actual_columns']==16 and moments['precision_pi']==400
    assert moments['all_old_low_state_scalar_overlaps_checked']==8908800
    assert moments['independent_original_recurrence_scalar_checks']==2560
    columns=[];coarse=0
    for name in names[3:]:
        row=certificates[name];columns+=list(range(row['first_column'],row['last_column']+1))
        coarse+=row['coarse_values_checked'];assert row['coarse_error_beta']==[832,848,832,864]
    assert columns==list(range(16)) and coarse==1088
    assert comparison['independent_quadric_coefficients_checked']==6188
    assert comparison['positive_coefficients_checked']==4641 and comparison['certified_mismatch_count']==0
    assert comparison['degree16_section_lower_beta']==[4194,4145,4128]
    assert comparison['anchor_section_lower_beta']==[3976,3648,3384]
    assert comparison['sufficient_nonanchor_beta']==[25305,25419,25526]
    assert comparison['W_Gaussian']=={'valuation_beta':1024,'error_beta':1225}
    assert not comparison['W_Gaussian_inverted'] and not comparison['positive_exact_vanishing_proved']
    jobs=[];categories={'computation':0,'independent_arithmetic':0,'interim_provenance':0}
    for path in sorted(DATA.glob('*d122*')):
        if path.name.startswith('dyadic_precision400_review_d122'):continue
        paths.append(path)
        if path.suffix!='.json':continue
        packet=json.loads(path.read_text())
        paths+=checked([x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        paths+=checked(packet.get('checkpoint_files',[]))
        if path.name.endswith('.job.json'):
            assert packet['status']=='pass' and packet['exit_code']==0
            assert packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
            paths+=checked([packet['driver'],packet['log']])
            if path.name.startswith('dyadic_precision400_checkpoint_d122'):kind='interim_provenance'
            elif path.name.startswith('dyadic_precision400_audit_'):kind='independent_arithmetic'
            else:kind='computation'
            categories[kind]+=1
            jobs.append({'receipt':path.name,'kind':kind,'wall_seconds':packet['wall_seconds'],'status':'pass'})
    assert categories=={'computation':157,'independent_arithmetic':7,'interim_provenance':3},categories
    return {'status':'pass','milestone':'D122','independent_mathematical_review_complete':True,
        'review_scope':'Independent finite arithmetic checks and the companion mathematical arguments; not a formalized geometric proof.',
        'D121_source_hashes_checked_unchanged':1079,'interim_checkpoint_source_hashes_preserved':1844,
        'certificates':certificates,'bounded_input_jobs':jobs,'input_job_categories':categories,
        'actual_harmonic_columns':16,'working_precision_pi':400,'coarse_error_beta':[832,848,832,864],
        'all_coarse_values_independently_checked':1088,'all_quadric_coefficients_independently_checked':6188,
        'degree16_section_lower_beta':[4194,4145,4128],'anchor_section_lower_beta':[3976,3648,3384],
        'sufficient_nonanchor_beta':[25305,25419,25526],'W_Gaussian_valuation_beta':1024,
        'W_Gaussian_error_beta':1225,'W_Gaussian_inverted':False,
        'positive_quadric_jet_exact_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'full_target_precision_solve_ready':False,
        'sources':[source(p) for p in sorted(set(p.resolve() for p in paths))]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        result=json.loads(OUT.read_text());checked(result['sources'])
        assert result['status']=='pass' and result['independent_mathematical_review_complete']
    else:
        assert not OUT.exists();result=build();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs']),
        'independent_mathematical_review_complete':True,'W_Gaussian_valuation_beta':1024}),flush=True)
    print('PASS|487_DYADIC_PRECISION400_REVIEW',flush=True)
