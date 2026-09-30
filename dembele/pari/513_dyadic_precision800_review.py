"""D125 final fixed provenance review of the complete P=800 comparison."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_precision800_review_d125.json';CACHE={}


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
    priorpath=DATA/'dyadic_precision1600_review_d124.json';prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and prior['independent_mathematical_review_complete'] and len(prior['sources'])==3535
    paths=checked(prior['sources'])+[priorpath,Path(__file__),
        ROOT/'dembele/certificates/dyadic-precision800-d125.md',DATA/'dyadic_precision800_sources_d125.json']
    for stem in ('dyadic_precision1600_review_d124_attempt01','dyadic_precision1600_review_d124_recheck01'):
        path=DATA/(stem+'.job.json');row=json.loads(path.read_text());assert row['status']=='pass'
        paths+=[path]+checked(row['sources']+[row['driver'],row['log']])
    def read(stem):
        path=DATA/(stem+'.json');paths.append(path);packet=json.loads(path.read_text());assert packet['status']=='pass';return packet
    bank=read('dyadic_precision800_d125')
    assert bank['harmonic_basis_columns']==16 and bank['working_precision_pi']==800
    assert bank['full_sixteen_column_bank_refined'] and bank['complete_original_residual_scalar_checks']==17817600
    assert bank['CM_moment_scalar_coefficients']==3481600 and bank['coarse_error_beta']==[1632,1648,1632,1664]
    counts=[];summaries=[]
    for col in range(1,16):
        summary=read(f'dyadic_weighted_column_P800_col{col:02d}_d125');summaries.append(summary)
        assert summary['completed_phases']==81 and summary['correction_steps']==12
        assert summary['harmonic_basis_column']==col
        packet=read(f'dyadic_precision800_audit_col{col:02d}_d125');assert packet['production_arithmetic_not_imported']
        cert=packet['certificates'];counts.append(cert)
        assert cert['states']['production_full_original_residual_scalar_checks']==1113600
        assert cert['states']['old_P400_low_scalar_overlaps']==556800
        assert cert['states']['independent_original_recurrence_scalar_checks']==160
        assert cert['states']['complete_disjoint_sweeps_checked']==17
        assert cert['seed']['all_old_precision_extended_seed_scalar_overlaps']==1113600
        assert cert['seed']['independent_high_seed_scalar_checks']==24
        assert cert['coarse']['independent_coarse_values_checked']==68 and cert['coarse']['old_CM_scalar_overlaps']==108800
        assert cert['coarse']['independent_CM_recurrence_scalar_checks']==72
        assert cert['weighted']['weighted_checkpoints_checked']==13
        assert cert['weighted']['all_weighted_state_scalar_checks']==14476800
        assert cert['weighted']['all_scaled_residual_scalar_checks']==3695760
        cm=read(f'dyadic_direct_CM_P800_col{col:02d}_d125')
        assert cm['weighted_input_used'] and cm['state_extension_3P_not_used'] and cm['composed_child_maps_checked']==34
        for row in cm['independent_composition_checks']:
            assert row['denominator_valuation_pi']==0 and row['c_valuation_pi']>=1 and row['delta_valuation_pi']>=1
    # Column zero's stronger, separately computed route and its audits are inherited.
    inherited=read('dyadic_staged_pilot_independent_d123')
    assert inherited['independent_coarse_values_checked']==68 and inherited['working_precision_pi']==800
    frame=read('dyadic_residue_frame800_d125');quads=read('dyadic_integral_quadrics800_d125')
    audit=read('dyadic_precision800_audit_comparison_d125');assert audit['production_arithmetic_not_imported']
    cert=audit['certificates'];assert cert['all_bank_assembled_coarse_values_checked']==1088
    assert cert['independent_quadric_coefficients_checked']==6188 and cert['positive_coefficients_checked']==4641
    assert cert['certified_mismatch_count']==len(quads['certified_mismatches'])
    assert not cert['W_Gaussian_inverted'] and not cert['positive_exact_vanishing_proved']
    assert cert['certified_mismatch_count']==0 and cert['degree16_section_lower_beta']==[4994,4945,4928]
    assert cert['anchor_section_lower_beta']==[4776,4448,4184] and cert['sufficient_nonanchor_beta']==[25255,25369,25476]
    assert cert['W_Gaussian']=={'valuation_beta':1024,'error_beta':2025}
    assert frame['P400_change_entries_compared']==256 and frame['P400_actual_jet_overlaps']==1088
    kinds={'505_dyadic_weighted_bank_chunks.py':'state','506_dyadic_direct_CM_bank.py':'CM',
        '507_dyadic_complete_precision800_bank.py':'bank','508_dyadic_precision800_balls.py':'ball_controls',
        '509_dyadic_precision800_residue_frame.py':'frame','510_dyadic_precision800_quadrics.py':'quadrics',
        '511_dyadic_precision800_column_audit.py':'column_audits','512_dyadic_precision800_comparison_audit.py':'comparison_audit'}
    categories={kind:0 for kind in kinds.values()};jobs=[];peaks=[]
    for path in sorted(DATA.glob('*d125*')):
        if path.name.startswith('dyadic_precision800_review_d125'):continue
        assert path.is_file();paths.append(path)
        if path.suffix!='.json':continue
        row=json.loads(path.read_text())
        paths+=checked([x for x in row.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        paths+=checked(row.get('checkpoint_files',[]))
        if 'peak_rss_bytes' in row:assert row['peak_rss_bytes']>0;peaks.append(row['peak_rss_bytes'])
        if not path.name.endswith('.job.json'):continue
        assert row['status']=='pass' and row['exit_code']==0,path.name
        assert row['timeout_seconds']==180 and row['timeout_terminates_process_group']
        paths+=checked([row['driver'],row['log']]);kind=kinds[Path(row['driver']['path']).name];categories[kind]+=1
        jobs.append({'receipt':path.name,'category':kind,'status':'pass','wall_seconds':row['wall_seconds']})
    assert categories=={'state':1215,'CM':15,'bank':1,'ball_controls':1,'frame':1,'quadrics':1,'column_audits':15,'comparison_audit':1},categories
    manifests=[source(path) for path in sorted({p.resolve() for p in paths})]
    assert {(x['path'],x['sha256']) for x in prior['sources']}<={(x['path'],x['sha256']) for x in manifests}
    return {'status':'pass','milestone':'D125','independent_mathematical_review_complete':True,
        'review_scope':'Independent finite arithmetic and companion mathematical arguments; not a machine-formalized geometric proof.',
        'inherited_D124_hashes_preserved':3535,'actual_harmonic_columns':16,'working_precision_pi':800,
        'coarse_error_beta':[1632,1648,1632,1664],'complete_original_residual_scalar_checks':17817600,
        'CM_moment_scalar_coefficients':3481600,'all_coarse_values_independently_checked_including_inherited_column_zero':1088,
        'new_column_audits':15,'new_sampled_original_recurrence_scalar_checks':2400,
        'new_sampled_CM_recurrence_scalar_checks':1080,'new_weighted_state_scalar_checks':217152000,
        'comparison_certificates':cert,'bounded_input_jobs':jobs,'input_job_categories':categories,
        'maximum_recorded_single_process_peak_rss_bytes':max(peaks),
        'state_column_coordinator_seconds':[row['coordinator_current_invocation_wall_seconds'] for row in summaries],
        'state_checkpoint_payload_bytes':sum(row['distinct_checkpoint_payload_bytes'] for row in summaries),
        'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'complete_target_size_solve_costed':False,'sources':manifests}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        result=json.loads(OUT.read_text());checked(result['sources']);assert result['status']=='pass' and result['independent_mathematical_review_complete']
    else:
        assert not OUT.exists();result=build();out=OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs']),
        'actual_columns':16,'precision_pi':800}),flush=True)
    print('PASS|513_DYADIC_PRECISION800_REVIEW',flush=True)
