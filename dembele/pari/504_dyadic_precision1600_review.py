"""D124 freeze completed P=1600 arithmetic, controls, and prior provenance."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_precision1600_review_d124.json';CACHE={}


def source(path):
    path=Path(path).resolve()
    if path not in CACHE:
        sha=hashlib.sha256()
        with path.open('rb') as file:
            while block:=file.read(1<<20):sha.update(block)
        CACHE[path]={'path':str(path),'sha256':sha.hexdigest()}
    return CACHE[path]


def checked(rows):
    paths=[]
    for row in rows:assert source(row['path'])==row,row['path'];paths.append(Path(row['path']))
    return paths


def build():
    priorpath=DATA/'dyadic_staged_review_d123.json';prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and prior['independent_mathematical_review_complete'] and len(prior['sources'])==2532
    paths=checked(prior['sources'])+[priorpath,Path(__file__),
        ROOT/'dembele/certificates/dyadic-precision1600-d124.md',DATA/'dyadic_precision1600_sources_d124.json']
    replay=DATA/'dyadic_staged_review_d123_recheck02.job.json';row=json.loads(replay.read_text())
    assert row['status']=='pass';paths+=[replay]+checked(row['sources']+[row['driver'],row['log']])
    def read(stem):
        path=DATA/(stem+'.json');paths.append(path);packet=json.loads(path.read_text());assert packet['status']=='pass';return packet
    factor=read('dyadic_low_factor_P1600_r32_d124')
    assert factor['all_P800_factor_coefficients_agree'] and factor['original_sparse_residual_checked']
    assert factor['original_scalar_equations_checked']==89088 and factor['binary_payload_bytes']==251084800
    pilot=read('dyadic_weighted_pilot_P1600_col00_d124')
    assert pilot['completed_phases']==228 and pilot['correction_steps']==24 and pilot['working_precision_pi']==1600
    state=read('dyadic_weighted_P1600_col00_verified_d124');cert=state['certificate']
    assert cert['original_full_residual_zero'] and cert['actual_new_precision_pi']==1600
    assert cert['weighted_residual_condition_checked'] and cert['scalar_coefficients_checked']==2227200
    assert cert['old_low_scalar_overlaps_checked']==1113600 and cert['old_extended_scalar_overlaps_checked']==2227200
    assert cert['full_residual_uses_different_polynomial_backend_from_lift']
    cm=read('dyadic_CM_P1600_col00_d124')
    assert cm['CM_charts_checked']==17 and cm['coarse_error_beta']==[3232,3248,3232,3264]
    assert cm['CM_moment_scalar_coefficients']==435200 and cm['old_CM_moment_scalar_coefficients_checked']==217600
    audits={name:read(f'dyadic_precision1600_audit_{name}_d124') for name in ['states','seed','coarse','weighted']}
    assert all(row['production_arithmetic_not_imported'] for row in audits.values())
    a={name:row['certificates'] for name,row in audits.items()}
    assert a['states']['independent_original_recurrence_scalar_checks']==160 and a['states']['child_column_divisibility_checks']==348
    assert a['states']['complete_disjoint_sweeps_checked']==29
    assert a['seed']['independent_high_seed_scalar_checks']==24 and a['seed']['all_old_precision_extended_seed_scalar_overlaps']==2227200
    assert a['coarse']['independent_coarse_values_checked']==68 and a['coarse']['old_CM_scalar_overlaps']==217600
    assert a['weighted']['all_weighted_state_scalar_checks']==55680000
    assert a['weighted']['all_scaled_residual_scalar_checks']==14094000 and a['weighted']['weighted_checkpoints_checked']==25
    composed={P:read(f'dyadic_composed_CM_P{P}_d124') for P in (800,1600)}
    for P,row in composed.items():
        assert row['weighted_input_used'] and row['all_scalar_moment_comparisons']==17*2*P*8
        assert row['composed_child_maps_checked']==34 and row['uniform_reconstruction_and_3P_state_extension_not_used_for_calculation']
        for mapping in row['independent_composition_normalization_and_determinant_checks']:
            assert mapping['denominator_valuation_pi']==0 and mapping['c_valuation_pi']>=1 and mapping['delta_valuation_pi']>=1
    profile=read('dyadic_transport_profile_d124');assert profile['original_low_equation_scalar_checks']==1320
    adaptive=read('dyadic_adaptive_kernel_control_d124');assert adaptive['certificates']['independent_small_products_checked']==172
    assert adaptive['certificates']['actual_original_equation_scalar_checks']==33320
    target=read('dyadic_adaptive_target_d124');assert target['certificates']['complete_scalar_comparisons']==84416
    assert not target['certificates']['actual_harmonic_precision_increased']
    kinds={'496_dyadic_factor1600.py':'factor','497_dyadic_weighted_chunks.py':'state',
        '498_dyadic_CM1600.py':'CM','499_dyadic_precision1600_independent.py':'independent_arithmetic',
        '500_dyadic_composed_CM_control.py':'composed_CM','501_dyadic_transport_profile.py':'profile',
        '503_dyadic_adaptive_kernel_control.py':'adaptive_kernel'}
    counts={kind:0 for kind in kinds.values()};jobs=[];peaks=[]
    for path in sorted(DATA.glob('*d124*')):
        if path.name.startswith('dyadic_precision1600_review_d124'):continue
        assert path.is_file();paths.append(path)
        if path.suffix!='.json':continue
        row=json.loads(path.read_text())
        paths+=checked([x for x in row.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        paths+=checked(row.get('checkpoint_files',[]))
        if 'peak_rss_bytes' in row:assert row['peak_rss_bytes']>0;peaks.append(row['peak_rss_bytes'])
        if not path.name.endswith('.job.json'):continue
        assert row['status']=='pass' and row['exit_code']==0,path.name
        assert row['timeout_seconds']==180 and row['timeout_terminates_process_group']
        paths+=checked([row['driver'],row['log']]);kind=kinds[Path(row['driver']['path']).name];counts[kind]+=1
        jobs.append({'receipt':path.name,'category':kind,'status':'pass','wall_seconds':row['wall_seconds']})
    assert counts=={'factor':1,'state':228,'CM':4,'independent_arithmetic':4,'composed_CM':2,'profile':1,'adaptive_kernel':2},counts
    manifests=[source(path) for path in sorted({path.resolve() for path in paths})]
    assert {(x['path'],x['sha256']) for x in prior['sources']}<={(x['path'],x['sha256']) for x in manifests}
    return {'status':'pass','milestone':'D124','independent_mathematical_review_complete':True,
        'inherited_D123_hashes_preserved':2532,'actual_P1600_harmonic_columns':1,'full_sixteen_column_bank_precision_pi':400,
        'coarse_error_beta':[3232,3248,3232,3264],'certificates':a,
        'composed_CM_scalar_checks_by_precision':{str(P):row['all_scalar_moment_comparisons'] for P,row in composed.items()},
        'adaptive_kernel_independent_product_controls':172,'maximum_recorded_single_process_peak_rss_bytes':max(peaks),
        'pilot_measurements':{key:pilot[key] for key in ['sum_recorded_phase_seconds','maximum_phase_seconds',
            'maximum_single_phase_peak_rss_bytes','coordinator_current_invocation_wall_seconds','distinct_checkpoint_payload_bytes']},
        'input_job_categories':counts,'bounded_input_jobs':jobs,
        'quadric_bounds_changed':False,'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'complete_target_size_solve_costed':False,'sources':manifests}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        result=json.loads(OUT.read_text());checked(result['sources']);assert result['status']=='pass' and result['independent_mathematical_review_complete']
    else:
        assert not OUT.exists();result=build();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs']),
        'actual_P1600_columns':1,'full_bank_precision_pi':400}),flush=True)
    print('PASS|504_DYADIC_PRECISION1600_REVIEW',flush=True)
