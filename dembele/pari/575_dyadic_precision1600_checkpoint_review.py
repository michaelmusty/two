"""D138 finite final review with an explicitly replayable provenance graph.

No production arithmetic is imported. The independent source-573 integer
quotient computation checks the complete frame/quadric comparison. Fifteen
capped catalogue replays authenticate the inherited and new column evidence.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_precision1600_review_d138.json'
PATHS={Path(__file__),ROOT/'dembele/certificates/dyadic-precision1600-bank-d138.md'};CACHE={}

def raw_source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while raw:=f.read(1<<20):h.update(raw)
    return {'path':str(path),'sha256':h.hexdigest()}

def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:CACHE[path]=raw_source(path)
    return CACHE[path]

def checked(rows):
    for row in rows:assert source(row['path'])==row,row['path']

def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);v=json.loads(path.read_text());assert v['status']=='pass',stem;return v

def receipt(ref,metadata,driver,args):
    checked([ref,metadata]);r=json.loads(Path(ref['path']).read_text())
    assert r['status']=='pass' and r['exit_code']==0 and r['timeout_seconds']==180 and r['timeout_terminates_process_group']
    assert r['command']==['python3',str(ROOT/driver)]+args and r['driver']==source(ROOT/driver)
    checked([r['log'],*r['sources']])
    marks=[json.loads(x.split('|',1)[1]) for x in Path(r['log']['path']).read_text().splitlines() if x.startswith('PHASE_METADATA|')]
    assert marks==[metadata]
    packet=json.loads(Path(metadata['path']).read_text());assert packet['status']=='pass';checked(packet.get('sources',[]))
    if 'peak_rss_bytes' in packet:assert packet['peak_rss_bytes']<=2*(1<<30)
    assert r['wall_seconds']<=180
    return r,packet

def build():
    tick=time.monotonic();prior=read('dyadic_checkpoint_admission_r2_d137')
    assert prior['P1600_checkpoint_admitted'] and prior['revision']==2 and not prior['P3200_and_higher_bank_admitted']
    parent=source(DATA/'dyadic_checkpoint_admission_r2_d137.json')
    admission_done=read('dyadic_checkpoint_admission_completion_r2_d137');assert admission_done['fixed_review']==parent
    for ref,args in zip(admission_done['review_receipts'],([],['--check'])):
        # Admission outputs bind the original catalogue. Its transitive
        # files are rehashed by shard 0, rather than flattened here.
        checked([ref]);r=json.loads(Path(ref['path']).read_text())
        assert r['status']=='pass' and r['exit_code']==0
        assert r['command']==['python3',str(ROOT/'dembele/pari/567_dyadic_checkpoint_admission_revision.py')]+args
        checked([r['driver'],r['log'],*r['sources']])
    assert admission_done['failed_initial_startup_preserved']['mathematical_work_started'] is False
    summary=read('dyadic_checkpoint_columns_completed_r2_d137')
    assert summary['prior_admission']==parent and summary['all_fourteen_new_columns_independently_reviewed']
    assert summary['working_precision_pi']==1600 and summary['maximum_mathematical_workers']==3
    assert summary['higher_precision_bank_not_launched'] and summary['bank_assembly_frame_comparison_and_final_review_pending']
    checked([summary['coordinator']]);assert summary['coordinator']==source(ROOT/'dembele/pari/run_d137_bank_r2.py')
    roots=[parent];counts=Counter();timings=[];archive_max=0;peak_rss=0;observed_store=0
    expected_input_receipts=set();past_end=None;next_seed_sources=[]
    assert len(summary['columns'])==14
    for col,ref in zip(range(2,16),summary['columns']):
        checked([ref]);done=read(Path(ref['path']).stem);assert done['column']==col and done['prior_admission']==parent
        checked([done['config'],done['production'],done['audits'],done['fixed_review']])
        cfg=read(Path(done['config']['path']).stem)
        assert cfg['column']==col and cfg['precision_pi']==1600 and cfg['seed_precision_pi']==800
        review=read(Path(done['fixed_review']['path']).stem);roots.append(done['fixed_review'])
        assert review['independent_finite_review_complete'] and review['incremental_provenance']
        assert review['prior_fixed_review']==parent and review['working_precision_pi']==1600 and review['harmonic_basis_column']==col
        assert review['passing_input_jobs']==6637 and review['failed_bounded_input_jobs']==0
        e=review['certificates']['execution'];a=review['certificates']['independent'];store=review['certificates']['store']
        assert e['actual_phases']==6588 and e['metadata_archive_jobs']==25 and e['corrections']==24
        assert e['full_original_weighted_equation_scalars']==174*1600*8 and e['all_fixed_masses']==174
        assert e['complete_CM_scalars']==17*3200*8 and e['coarse_values']==68
        assert e['coarse_errors_beta']==[3232,3248,3232,3264]
        assert e['maximum_recorded_phase_concurrency']<=3 and e['conservative_sum_of_concurrent_measured_peaks_bytes']<=6*(1<<30)
        assert e['maximum_measured_job_RSS_bytes']<=2*(1<<30)
        assert e['maximum_observed_working_store_bytes']<=e['proved_inventory_bound_bytes']==141761896
        assert a['audit_jobs']==24 and a['complete_old_weighted_overlap_scalars']==174*800*8
        assert a['exact_masses']==a['final_residual_zero_rows']==174
        assert a['old_CM_overlap_scalars']==17*1600*8 and a['coarse_old_overlaps']==68
        assert a['ordinary_state_scalars']==a['ordinary_CM_scalars']==72 and a['independent_Horner_beta_scalars']==96
        assert store['epoch']==50 and store['history_records']==50 and store['retirement_records']==25
        production=read(Path(done['production']['path']).stem)
        assert production['all_phases_complete'] and production['completed_jobs']==6588 and production['maximum_workers']==3
        intervals=[row['coordinator_interval'] for row in production['jobs']]
        begin=min(x[0] for x in intervals);end=max(x[1] for x in intervals)
        if past_end is not None:assert past_end<=begin,'different columns overlap'
        past_end=end
        for row in production['metadata_archives']:
            path=Path(row['receipt']['path']);raw=json.loads(path.read_text())
            assert raw['status']=='pass' and raw['wall_seconds']<=180
            archive_max=max(archive_max,raw['wall_seconds'])
        assert len(production['metadata_archives'])==25
        for ref,check in zip(done['review_receipts'],(False,True)):
            args=['--config',Path(done['config']['path']).stem,'--output',Path(done['fixed_review']['path']).stem]+(['--check'] if check else [])
            # The review's large sources list is authenticated by its own
            # root and a dedicated shard, not copied to this sources list.
            checked([ref]);r=json.loads(Path(ref['path']).read_text());assert r['status']=='pass' and r['exit_code']==0
            assert r['timeout_seconds']==180 and r['timeout_terminates_process_group']
            assert r['command']==['python3',str(ROOT/'dembele/pari/568_dyadic_checkpoint_column_review.py')]+args
            checked([r['driver'],r['log'],*r['sources']])
            marks=[json.loads(x.split('|',1)[1]) for x in Path(r['log']['path']).read_text().splitlines() if x.startswith('PHASE_METADATA|')]
            assert marks==[done['fixed_review']]
        assert len(done['review_receipts'])==2
        counts.update(production=6588,archive=25,audit=24,column_review=2)
        peak_rss=max(peak_rss,e['maximum_measured_job_RSS_bytes']);observed_store=max(observed_store,e['maximum_observed_working_store_bytes'])
        timings.append({'column':col,'production_coordinator_seconds':production['wall_seconds'],
                        'summed_production_worker_seconds':production['sum_recorded_job_seconds'],
                        'summed_archive_seconds':e['summed_archive_seconds']})
    assert counts==Counter(production=92232,archive=350,audit=336,column_review=28)
    manifest_summary=read('dyadic_precision1600_manifests_d138_completed')
    assert manifest_summary['workers']==2 and manifest_summary['completed_jobs']==15
    assert manifest_summary['coordinator']==source(ROOT/'dembele/pari/run_d138_manifest_rechecks.py')
    inherited={};replayed=0;events=[]
    for index,item in enumerate(manifest_summary['jobs']):
        stem=f'dyadic_precision1600_manifest{index:02d}_d138';assert item['index']==index
        r,m=receipt(item['receipt'],item['metadata'],'dembele/pari/574_dyadic_checkpoint_manifest_recheck.py',['--index',str(index),'--output',stem])
        expected_input_receipts.add(item['receipt']['path'])
        assert m['index']==index and m['all_catalogue_hashes_match'] and m['catalogue_root']==roots[index]
        assert m['prior_admission']==parent and m['full_source_list_bound_by_catalogue_root']
        catalogue=json.loads(Path(roots[index]['path']).read_text())
        assert m['catalogue_sources_rehashed']==len(catalogue['sources'])
        replayed+=len(catalogue['sources'])
        for row in catalogue['sources']:
            if row['path'] in inherited:assert inherited[row['path']]==row['sha256']
            inherited[row['path']]=row['sha256']
        b,e=item['coordinator_interval'];events.extend([(b,1,item['peak_rss_bytes']),(e,-1,-item['peak_rss_bytes'])])
    used=rss=0
    for _,n,size in sorted(events):
        used+=n;rss+=size;assert 0<=used<=2 and 0<=rss<=4*(1<<30)
    assert used==rss==0 and replayed==380188
    # Preserve the immutable dependency interface needed by a separately
    # admitted future stage, without flattening every old phase receipt.
    inp=DATA/'dyadic_rowjournal_P1600_col02_r2_d132'/'INPUTS.json'
    assert inherited[str(inp)]==source(inp)['sha256']
    wrapped=json.loads(inp.read_text());raw=json.dumps(wrapped['value'],sort_keys=True,separators=(',',':')).encode()
    assert hashlib.sha256(raw).hexdigest()==wrapped['sha256']
    checked(wrapped['value']['sources'])
    stages=[('dyadic_precision1600_bank_d138','569_dyadic_complete_precision1600_bank.py'),
            ('dyadic_precision1600_balls_d138','570_dyadic_precision1600_balls.py'),
            ('dyadic_residue_frame1600_d138','571_dyadic_precision1600_residue_frame.py'),
            ('dyadic_integral_quadrics1600_d138','572_dyadic_precision1600_quadrics.py'),
            ('dyadic_precision1600_audit_comparison_d138','573_dyadic_precision1600_comparison_audit.py')]
    packets={};new_jobs=[]
    for stem,driver in stages:
        rp=DATA/(stem+'_attempt01.job.json');mp=DATA/(stem+'.json')
        r,m=receipt(source(rp),source(mp),'dembele/pari/'+driver,[])
        assert m['milestone']=='D138';packets[stem]=m;expected_input_receipts.add(str(rp))
        new_jobs.append({'receipt':source(rp),'seconds':r['wall_seconds'],'peak_rss_bytes':m['peak_rss_bytes']})
    observed={str(p.resolve()) for p in DATA.glob('*d138*_attempt*.job.json') if not p.name.startswith(OUT.stem)}
    assert observed==expected_input_receipts,'unexpected, failed or unreviewed D138 attempt'
    bank,balls,frame,quads,audit=[packets[s] for s,_ in stages]
    assert bank['working_precision_pi']==1600 and bank['full_sixteen_column_bank_refined'] and bank['harmonic_basis_columns']==16
    assert bank['coarse_error_beta']==[3232,3248,3232,3264] and bank['old_coarse_values_checked']==1088
    assert bank['common_precision_original_equation_scalar_coverage']==35635200 and bank['CM_moment_scalar_coefficients']==6963200
    assert bank['column_review_roots']==roots[1:] and bank['prior_admission']==parent
    assert balls['ring_precision_beta']==4096 and balls['independent_ring_products_checked']==8
    assert balls['integral_scalings_compared_with_field_products']==20 and balls['unknown_ball_inverse_rejected']
    assert frame['working_precision_pi']==1600 and frame['P800_change_entries_compared']==256 and frame['P800_actual_jet_overlaps']==1088
    assert not frame['candidate_data_used'] and not frame['W_Gaussian_inverted']
    assert quads['all_coefficients_tested']==6188 and quads['positive_coefficients_tested']==4641
    assert audit['production_arithmetic_not_imported'];cert=audit['certificates']
    assert cert['all_bank_assembled_coarse_values_checked']==1088 and cert['all_actual_jet_values_checked']==1088
    assert cert['independent_quadric_coefficients_checked']==6188 and cert['positive_coefficients_checked']==4641
    assert cert['certified_mismatch_count']==len(quads['certified_mismatches'])
    assert bool(cert['certified_mismatch_count'])==quads['candidate_mismatch_certified']
    assert cert['degree16_section_lower_beta']==[row['degree16_achieved_lower_beta'] for row in quads['comparison_with_sufficient_bounds']]
    assert cert['anchor_section_lower_beta']==[row['anchor_achieved_lower_beta'] for row in quads['comparison_with_sufficient_bounds']]
    assert cert['sufficient_nonanchor_beta']==[row['sufficient_nonanchor_beta_with_new_anchor'] for row in quads['comparison_with_sufficient_bounds']]
    assert cert['W_Gaussian']['valuation_beta']==frame['Gaussian_G12'][0]['valuation_beta']
    assert not cert['positive_exact_vanishing_proved'] and not cert['W_Gaussian_inverted']
    assert not quads['candidate_identification_proved'] and not quads['target_field_polynomial_constructed']
    old=read('dyadic_precision800_audit_comparison_d125')['certificates']
    gain=[a-b for a,b in zip(cert['degree16_section_lower_beta'],old['degree16_section_lower_beta'])]
    anchor_gain=[a-b for a,b in zip(cert['anchor_section_lower_beta'],old['anchor_section_lower_beta'])]
    for path,ref in CACHE.items():
        if str(path) in inherited:assert inherited[str(path)]==ref['sha256']
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<=2*(1<<30)
    return {'status':'pass','milestone':'D138','independent_finite_review_complete':True,
            'review_scope':'Independent finite arithmetic and authenticated companion arguments; not a machine-formalized geometric proof.',
            'full_bank_precision_pi':1600,'column_precisions':{'0':6400,**{str(c):1600 for c in range(1,16)}},
            'sixteen_column_checkpoint_complete':True,'coarse_error_beta':bank['coarse_error_beta'],
            'comparison_certificates':cert,'P800_to_P1600_section_bound_gain_beta':gain,'P800_to_P1600_anchor_bound_gain_beta':anchor_gain,
            'D137_successful_column_job_categories':dict(counts),'D137_successful_column_jobs':sum(counts.values()),
            'D137_column_run_wall_seconds':summary['wall_seconds'],'D137_column_timings':timings,
            'D137_maximum_archive_seconds':archive_max,'D137_maximum_production_RSS_bytes':peak_rss,
            'D137_maximum_working_store_bytes':observed_store,'D137_initial_namespace_failure_preserved':True,
            'D138_bounded_input_jobs':20,'D138_stage_jobs':new_jobs,'failed_D138_input_jobs':0,
            'inherited_catalogues':roots,'catalogue_graph_is_transitive':True,'catalogue_hash_replays':replayed,
            'unique_inherited_file_hashes':len(inherited),'all_inherited_bindings_preserved':True,
            'prior_catalogues_not_duplicated_in_this_sources_list':True,
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
            'arithmetic_cover_identification_proved':False,'field_polynomial_constructed':False,
            'next_precision_bank_admitted':False,'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak,
            'sources':[source(p) for p in sorted(PATHS)]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();tick=time.monotonic()
    if a.check:
        saved=json.loads(OUT.read_text());assert saved['status']=='pass' and saved['sixteen_column_checkpoint_complete']
        checked(saved['sources'])
        # A full transitive replay, still bounded by the same wrapper. The
        # source catalogues are read one at a time to keep memory bounded.
        hashes=0
        for ref in saved['inherited_catalogues']:
            assert raw_source(ref['path'])==ref
            for item in json.loads(Path(ref['path']).read_text())['sources']:
                assert raw_source(item['path'])==item,item['path'];hashes+=1
        assert hashes==saved['catalogue_hash_replays']
        peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<=2*(1<<30)
        print('D138_TRANSITIVE_REPLAY|'+json.dumps({'catalogue_hashes':hashes,'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    else:
        assert not OUT.exists();saved=build()
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|575_DYADIC_PRECISION1600_CHECKPOINT_REVIEW',flush=True)

if __name__=='__main__':main()
