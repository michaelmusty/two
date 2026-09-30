"""D123 final provenance and coverage review; arithmetic is in 491/494.

Build once after all pilot jobs complete. --check replays the fixed
manifest, allowing later work without changing this certificate.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_staged_review_d123.json';CACHE={}


def source(path):
    path=Path(path).resolve()
    if path not in CACHE:
        sha=hashlib.sha256()
        with path.open('rb') as file:
            while data:=file.read(1<<20):sha.update(data)
        CACHE[path]={'path':str(path),'sha256':sha.hexdigest()}
    return CACHE[path]


def checked(rows):
    paths=[]
    for row in rows:
        assert source(row['path'])==row,row['path'];paths.append(Path(row['path']))
    return paths


def build():
    priorpath=DATA/'dyadic_precision400_review_d122.json';prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and prior['independent_mathematical_review_complete']
    assert len(prior['sources'])==1884
    paths=checked(prior['sources'])+[priorpath,Path(__file__),
        ROOT/'dembele/certificates/dyadic-staged-pilot-d123.md',
        DATA/'dyadic_staged_pilot_sources_d123.json']
    resume=DATA/'dyadic_precision400_review_d122_recheck02.job.json'
    check=json.loads(resume.read_text());assert check['status']=='pass' and check['exit_code']==0
    paths+=[resume]+checked(check['sources']+[check['driver'],check['log']])
    def read(stem):
        path=DATA/(stem+'.json');paths.append(path);packet=json.loads(path.read_text())
        assert packet['status']=='pass';return packet
    factor=read('dyadic_low_factor_P800_r32_d123')
    assert factor['working_precision_pi']==800 and factor['eliminated_positive_moments']==32
    assert factor['all_P400_factor_coefficients_agree'] and factor['original_sparse_residual_checked']
    assert factor['original_scalar_equations_checked']==89088
    baseline=read('dyadic_staged_pilot_P800_col00_d123')
    assert baseline['completed_phases']==126 and baseline['correction_steps']==13
    state=read('dyadic_staged_P800_col00_verified_d123');certificate=state['certificate']
    assert certificate['original_full_residual_zero'] and certificate['actual_new_precision_pi']==800
    assert certificate['scalar_coefficients_checked']==1113600
    assert certificate['frozen_old_low_scalar_overlaps_checked']==556800
    assert certificate['old_precision_extended_scalar_overlaps_checked']==1113600
    assert certificate['full_residual_uses_different_polynomial_backend_from_lift']
    cm=read('dyadic_staged_CM_P800_col00_d123')
    assert cm['coarse_error_beta']==[1632,1648,1632,1664] and cm['CM_charts_checked']==17
    assert cm['CM_moment_scalar_coefficients']==217600 and cm['old_coarse_values_checked']==68
    audit=read('dyadic_staged_pilot_independent_d123')
    assert audit['independent_original_recurrence_scalar_checks']==160
    assert audit['independent_high_seed_scalar_checks']==24 and audit['independent_coarse_values_checked']==68
    assert audit['complete_disjoint_sweeps_checked']==16
    weighted=read('dyadic_weighted_precision_control_d123')
    assert weighted['original_operator_reconstruction_equals_verified_column']
    assert weighted['weighted_residual_condition_checked']
    assert weighted['compact_input_bytes']==7464600 and weighted['uniform_input_bytes']==14476800
    shrink=read('dyadic_shrinking_pilot_d123')
    assert shrink['completed_phases']==14 and shrink['correction_steps']==12
    assert shrink['correction_stage_uses_existing_uniform_seed']
    assert shrink['full_original_reconstruction_equals_verified_P800_column']
    audit2=read('dyadic_weighted_independent_d123')
    assert audit2['production_arithmetic_not_imported'] and audit2['shrinking_correction_stage_passes']
    assert audit2['child_maps_with_integral_column_divisibility_checked']==348
    assert audit2['all_thirteen_shrinking_state_scalar_checks']==13*1113600
    assert audit2['active_moment_counts']==[400,367,334,301,268,235,202,169,136,103,70,37,33]
    assert audit2['independent_original_recurrence_from_weighted_input_scalar_checks']==96
    assert audit2['full_uniform_reconstruction_scalar_checks']==1113600
    jobs=[];categories={'factor':0,'uniform_state':0,'CM':0,'independent_arithmetic':0,
        'weighted_reconstruction':0,'shrinking_state':0}
    for path in sorted(DATA.glob('*d123*')):
        if path.name.startswith('dyadic_staged_review_d123'):continue
        assert path.is_file();paths.append(path)
        if path.suffix!='.json':continue
        packet=json.loads(path.read_text())
        paths+=checked([x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        paths+=checked(packet.get('checkpoint_files',[]))
        if not path.name.endswith('.job.json'):continue
        assert packet['status']=='pass' and packet['exit_code']==0,path.name
        assert packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
        paths+=checked([packet['driver'],packet['log']])
        name=Path(packet['driver']['path']).name
        category={'488_dyadic_staged_low_factor.py':'factor','489_dyadic_staged_lift.py':'uniform_state',
            '490_dyadic_staged_CM.py':'CM','491_dyadic_staged_pilot_independent.py':'independent_arithmetic',
            '492_dyadic_weighted_precision_control.py':'weighted_reconstruction',
            '493_dyadic_shrinking_schur.py':'shrinking_state',
            '494_dyadic_weighted_independent.py':'independent_arithmetic'}[name]
        categories[category]+=1
        jobs.append({'receipt':path.name,'category':category,'wall_seconds':packet['wall_seconds'],'status':'pass'})
    assert categories=={'factor':1,'uniform_state':126,'CM':4,'independent_arithmetic':2,
        'weighted_reconstruction':1,'shrinking_state':14},categories
    manifests=[source(path) for path in sorted(set(path.resolve() for path in paths))]
    assert {(x['path'],x['sha256']) for x in prior['sources']}<={(x['path'],x['sha256']) for x in manifests}
    return {'status':'pass','milestone':'D123','independent_mathematical_review_complete':True,
        'inherited_D122_source_hashes_preserved':1884,'actual_P800_harmonic_columns':1,
        'full_sixteen_column_bank_precision_pi':400,'coarse_error_beta_for_refined_column':[1632,1648,1632,1664],
        'full_original_residual_scalar_checks':1113600,'independent_coarse_values_checked':68,
        'independent_original_recurrence_scalar_checks':160,'independent_high_seed_scalar_checks':24,
        'weighted_reconstruction_input_bytes':7464600,'weighted_input_ratio':0.515625,
        'shrinking_correction_steps':12,'shrinking_stage_uses_existing_P800_seed':True,
        'shrinking_pilot':{k:shrink[k] for k in ['sum_recorded_phase_seconds','maximum_phase_seconds',
            'coordinator_wall_seconds','checkpoint_payload_bytes']},
        'uniform_pilot':{k:baseline[k] for k in ['sum_recorded_phase_seconds','maximum_phase_seconds','coordinator_wall_seconds']},
        'independent_weighted_state_scalar_checks':audit2['all_thirteen_shrinking_state_scalar_checks'],
        'independent_weighted_residual_scalar_checks':audit2['all_thirteen_active_residual_scalar_checks'],
        'input_job_categories':categories,'bounded_input_jobs':jobs,
        'quadric_bounds_changed':False,'positive_exact_quadric_vanishing_proved':False,
        'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
        'complete_target_size_solve_costed':False,'sources':manifests}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        result=json.loads(OUT.read_text());checked(result['sources'])
        assert result['status']=='pass' and result['independent_mathematical_review_complete']
    else:
        assert not OUT.exists();result=build();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs']),
        'actual_P800_columns':1,'full_bank_precision_pi':400,'shrinking_corrections':12}),flush=True)
    print('PASS|495_DYADIC_STAGED_REVIEW',flush=True)
