"""D157 measured column-2 P6400 timing and limited remaining-route scenarios.

Run after production, all independent audits and column review/replay.
No other column or higher precision is admitted by this assessment.
"""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import fcntl
import json
from pathlib import Path
import resource
import re
import shutil
import statistics
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P6400_col02_config_d156';BASE='dyadic_staged_P6400_col02_d156'
REVIEW='dyadic_higher_pilot_col02_review_r2_d157'
PIPELINE='dyadic_higher_pilot_pipeline_d157_run01'
OUT=DATA/'dyadic_higher_pilot_timing_d157.json'
PATHS={Path(__file__)};CACHE={}

def source(path):
    p=Path(path).resolve();PATHS.add(p)
    if p not in CACHE:
        h=hashlib.sha256()
        with p.open('rb') as f:
            while raw:=f.read(1<<20):h.update(raw)
        CACHE[p]={'path':str(p),'sha256':h.hexdigest()}
    return CACHE[p]

def read(stem):
    p=DATA/(stem+'.json');source(p);v=json.loads(p.read_text());assert v['status']=='pass',stem;return v

def checked(ref):
    assert source(ref['path'])==ref;return json.loads(Path(ref['path']).read_text())

def calculate():
    cfg=read(CONFIG);review=read(REVIEW);prod=read(BASE+'_completed');audits=read(cfg['audit_plan']+'_completed')
    plan=read(cfg['audit_plan']);parent=read(cfg['admission_review'])
    assert parent['indexed_receipt_coordinator_admitted'] and parent['permitted_configs']==[source(DATA/(CONFIG+'.json'))]
    assert review['prior_fixed_review']==source(DATA/(cfg['admission_review']+'.json'))
    assert review['independent_finite_review_complete'] and review['incremental_provenance']
    assert review['execution_milestone']=='D156' and review['working_precision_pi']==6400 and review['harmonic_basis_column']==2
    assert (cfg['precision_pi'],cfg['seed_precision_pi'],cfg['column'])==(6400,3200,2)
    assert prod['coordinator']==source(ROOT/'dembele/pari/run_d139_indexed_production.py')
    assert prod['completed_jobs']==24456 and len(prod['metadata_archives'])==97
    assert prod['all_phases_complete'] and prod['maximum_workers']==3 and prod['receipt_inventory']['reconciled']
    assert audits['completed_jobs']==24 and audits['worker_limit']==3 and len(plan['jobs'])==24
    assert audits['coordinator']==source(ROOT/'dembele/pari/run_d137_audits.py')
    e,a,store=(review['certificates'][x] for x in ('execution','independent','store'))
    assert e['actual_phases']==24456 and e['metadata_archive_jobs']==97 and e['corrections']==96
    assert e['full_original_weighted_equation_scalars']==174*6400*8
    assert e['complete_CM_scalars']==17*12800*8 and e['coarse_errors_beta']==[12832,12848,12832,12864]
    assert a['audit_jobs']==24 and a['complete_old_weighted_overlap_scalars']==174*3200*8
    assert a['old_CM_overlap_scalars']==17*6400*8
    assert e['maximum_observed_working_store_bytes']<=e['proved_inventory_bound_bytes']==973167872
    assert e['maximum_recorded_phase_concurrency']<=3
    assert e['conservative_sum_of_concurrent_measured_peaks_bytes']<=6*(1<<30)
    assert e['maximum_measured_job_RSS_bytes']<=2*(1<<30)
    # Bind the already reviewed receipts, but leave their large immutable
    # catalogue transitive through the column review in the fixed review.
    phase_rows=defaultdict(list);owned=set();receipt_seconds=[];rss=[];archives=[]
    catalogue={x['path']:x['sha256'] for x in review['sources']}
    def receipt(item):
        ref=item['receipt'];assert catalogue[ref['path']]==ref['sha256']
        p=Path(ref['path']);raw=json.loads(p.read_text())
        assert raw['status']=='pass' and raw['exit_code']==0 and raw['timeout_seconds']==180
        assert raw['timeout_terminates_process_group'] and 0<raw['wall_seconds']<=180
        for rr in [ref,item['metadata'],raw['log']]:
            assert catalogue[rr['path']]==rr['sha256'];owned.add(Path(rr['path']))
        receipt_seconds.append(raw['wall_seconds']);return raw
    for item in prod['jobs']:
        raw=receipt(item);packet=json.loads(Path(item['metadata']['path']).read_text())
        assert item['seconds']==raw['wall_seconds'] and item['peak_rss_bytes']==packet['peak_rss_bytes']
        rss.append(item['peak_rss_bytes'])
        phase=packet['request']['phase'];begin,end=item['coordinator_interval']
        assert begin<=end
        phase_rows[phase].append({'seconds':raw['wall_seconds'],'elapsed':end-begin,
                                  'begin':begin,'end':end,'reused':item['reused_receipt']})
    reused=[x for x in prod['jobs'] if x['reused_receipt']]
    assert len(reused)==1 and reused[0]['key']=='create'
    for item in prod['metadata_archives']:archives.append(receipt(item)['wall_seconds'])
    for item in audits['jobs']:
        raw=receipt(item);assert item['seconds']==raw['wall_seconds'];rss.append(item['peak_rss_bytes'])
    review_rows=[]
    for suffix,extra in [('attempt01',[]),('recheck01',['--check'])]:
        stem=REVIEW+'_'+suffix+'.job';raw=read(stem)
        assert raw['command']==['python3',str(ROOT/'dembele/pari/651_dyadic_higher_pilot_column_review_revision.py'),
            '--config',CONFIG,'--output',REVIEW]+extra
        assert raw['status']=='pass' and raw['exit_code']==0 and raw['timeout_seconds']==180 and raw['timeout_terminates_process_group']
        assert source(raw['driver']['path'])==raw['driver'] and source(raw['log']['path'])==raw['log']
        marks=[json.loads(s.split('|',1)[1]) for s in Path(raw['log']['path']).read_text().splitlines() if s.startswith('PHASE_METADATA|')]
        assert marks==[source(DATA/(REVIEW+'.json'))]
        review_rows.append(raw['wall_seconds']);owned.update([DATA/(stem+'.json'),Path(raw['log']['path'])])
    assert sum(x['seconds'] for x in prod['jobs'])==e['summed_actual_job_seconds']==prod['sum_recorded_job_seconds']
    assert sum(archives)==e['summed_archive_seconds']
    phase_summary={}
    for phase,rows in sorted(phase_rows.items()):
        known=e['phase_timings'][phase]
        assert known['jobs']==len(rows) and known['summed_seconds']==sum(x['seconds'] for x in rows)
        phase_summary[phase]={'jobs':len(rows),'worker_seconds':sum(x['seconds'] for x in rows),
            'maximum_job_seconds':max(x['seconds'] for x in rows),
            'median_job_seconds':statistics.median(x['seconds'] for x in rows),
            'summed_callback_seconds':sum(x['elapsed'] for x in rows),
            'summed_nonnegative_callback_overhead_seconds':sum(max(0,x['elapsed']-x['seconds']) for x in rows if not x['reused'])}
    # Coordinator monotonic times include archive/discovery overhead. The
    # one earlier create phase is charged separately.
    active=prod['wall_seconds']+audits['wall_seconds']+sum(review_rows)+reused[0]['seconds']
    planning=read('dyadic_storage_timing_plan_d156')
    earlier=read('dyadic_pilot_timing_d154')
    full=read('precision_route_cost_d152')['schedules'][0]
    comparison=[];remaining=[]
    assert planning['pilot']['column_jobs']==24579
    for expected,bank in zip(planning['pilot']['timing_scenarios'],full['timing_scenarios']):
        assert expected['scenario']==bank['scenario']
        comparison.append({'scenario':expected['scenario'],
            'modeled_column_seconds':expected['column_cycle_seconds'],
            'modeled_total_hours_with_shared_allowances':expected['total_active_hours'],
            'observed_to_modeled_column_ratio':active/expected['column_cycle_seconds'],
            'retained_shared_allowance_seconds':expected['graph_review_seconds_allowance']+expected['common_comparison_seconds_allowance']})
        assert [(x['seed'],x['target'],x['columns']) for x in bank['stages']]==[(1600,3200,15),(3200,6400,15),(6400,10480,16)]
        first=14*earlier['measured_column_cycle_active_seconds']
        second=14*active
        last=16*bank['stages'][2]['active_seconds_per_column']
        tail=bank['retained_graph_review_seconds_allowance']+bank['retained_common_comparison_seconds_allowance']
        remaining.append({'scenario':bank['scenario'],'remaining_P3200_columns':14,
            'remaining_P6400_columns':14,'remaining_P10480_columns':16,
            'same_cost_remaining_P3200_hours':first/3600,
            'same_cost_remaining_P6400_hours':second/3600,
            'unchanged_unmeasured_P10480_hours':last/3600,
            'unchanged_graph_and_comparison_hours':tail/3600,
            'remaining_total_active_hours':(first+second+last+tail)/3600,
            'remaining_total_active_days':(first+second+last+tail)/86400})
    owned.update(DATA/(stem+'.json') for stem in [CONFIG,cfg['audit_plan'],BASE+'_completed',cfg['audit_plan']+'_completed',REVIEW,cfg['CM_output']])
    store_files=list((DATA/cfg['namespace']).iterdir())
    assert all(p.is_file() for p in store_files)
    storage={label:{'files':len(paths),'logical_bytes':sum(p.stat().st_size for p in paths),
                    'allocated_bytes':sum(p.stat().st_blocks*512 for p in paths)}
             for label,paths in [('sealed_store',store_files),('external_column_artifacts',sorted(owned))]}
    assert storage['sealed_store']['logical_bytes']==store['retained_store_bytes']
    assert all(p.is_file() for p in owned)
    retained_allowance=planning['pilot']['retained_allowance_bytes']
    remaining_free=planning['required_remaining_free_bytes']-retained_allowance
    assert retained_allowance==1254739040 and remaining_free==75002411056
    assert planning['largest_active_extra_bytes']==349629168 and planning['planning_reserve_bytes']==10*(1<<30)
    def raw_packet(stem):
        path=DATA/(stem+'.json');source(path);return json.loads(path.read_text())
    launch=raw_packet(PIPELINE+'_launch');status=raw_packet(PIPELINE+'_status')
    power=read(PIPELINE+'_power_assertion_finished')
    assert launch['status']=='started' and status['status']=='stopped_after_failure'
    assert not status['automatic_retry_attempted']
    assert launch['config']==source(DATA/(CONFIG+'.json'))
    assert launch['admission']==source(DATA/(cfg['admission_review']+'.json'))
    assert source(launch['supervisor']['path'])==launch['supervisor']
    assert launch['maximum_mathematical_workers']==3 and launch['mathematical_job_timeout_seconds']==180
    assert launch['no_other_column_or_stage_admitted'] and not power['permanent_power_settings_changed']
    launch_receipt=checked(launch['launch_check_receipt'])
    assert launch_receipt['status']=='pass' and launch_receipt['timeout_seconds']==180
    assert launch_receipt['timeout_terminates_process_group']
    for ref in [launch_receipt['driver'],launch_receipt['log'],*launch_receipt['sources']]:assert source(ref['path'])==ref
    source(DATA/(PIPELINE+'.log'))
    failed=raw_packet('dyadic_higher_pilot_col02_review_d156_attempt01.job')
    assert failed['status']=='failed' and failed['exit_code']==1 and 0<failed['wall_seconds']<180
    assert failed['timeout_seconds']==180 and failed['timeout_terminates_process_group']
    for ref in [failed['driver'],failed['log'],failed['failed_driver_snapshot'],*failed['sources']]:assert source(ref['path'])==ref
    assert failed['driver']['sha256']==failed['failed_driver_snapshot']['sha256']
    controls=read('dyadic_higher_pilot_review_controls_d157')
    control_receipt=read('dyadic_higher_pilot_review_controls_d157_attempt01.job')
    assert controls['complete_actual_D156_audits_accepted']==24
    assert len(controls['malformed_in_memory_fixtures_rejected'])==7
    assert controls['revised_reviewer']==source(ROOT/'dembele/pari/651_dyadic_higher_pilot_column_review_revision.py')
    assert controls['failed_attempt_and_snapshot_preserved'] and controls['production_and_audit_arithmetic_unchanged']
    assert [s['name'] for s in status['completed_stages']]==['production','audits','column_review']
    assert [s['exit_code'] for s in status['completed_stages']]==[0,0,1]
    clocks={}
    for i,stage in enumerate(status['completed_stages']):
        assert stage['command']==launch['stages'][i]['command']
        assert source(stage['log']['path'])==stage['log']
        if i<2:
            assert source(stage['output']['path'])==stage['output']
        span=(datetime.fromisoformat(stage['ended_utc'])-datetime.fromisoformat(stage['started_utc'])).total_seconds()
        clocks[stage['name']]={'started_utc':stage['started_utc'],'ended_utc':stage['ended_utc'],
            'supervisor_wall_span_seconds':span,'supervisor_monotonic_seconds':stage['monotonic_seconds'],
            'wall_span_minus_supervisor_monotonic_seconds':span-stage['monotonic_seconds']}
    clocks['production']['coordinator_monotonic_seconds']=prod['wall_seconds']
    clocks['audits']['coordinator_monotonic_seconds']=audits['wall_seconds']
    locks=[PIPELINE+'.lock',BASE+'.lock',cfg['audit_plan']+'.lock']
    for name in locks:
        with (DATA/name).open('r') as stream:
            fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
            fcntl.flock(stream,fcntl.LOCK_UN)
    # Retained allowances and current allocation are observations and
    # scenarios. They do not reserve space or predict APFS sharing.
    return {'status':'pass','milestone':'D157','column':2,'seed_precision_pi':3200,'precision_pi':6400,
        'config':source(DATA/(CONFIG+'.json')),'fixed_column_review':source(DATA/(REVIEW+'.json')),
        'production_jobs':24456,'archive_jobs':97,'audit_jobs':24,'column_review_jobs':2,'total_column_jobs':24579,
        'prior_preparation_create_jobs_reused':1,'new_passing_column_jobs_this_continuation':24578,
        'preserved_failed_column_review_attempts':1,'failed_column_review_seconds':failed['wall_seconds'],
        'review_regression_control_seconds':control_receipt['wall_seconds'],
        'production_coordinator_seconds':prod['wall_seconds'],'audit_coordinator_seconds':audits['wall_seconds'],
        'column_review_seconds':review_rows,'prior_create_seconds':reused[0]['seconds'],
        'measured_column_cycle_active_seconds':active,'measured_column_cycle_active_hours':active/3600,
        'observed_cycle_plus_failed_review_and_regression_seconds':active+failed['wall_seconds']+control_receipt['wall_seconds'],
        'measurement_excludes_preparation_other_than_create_and_final_timing_assessment':True,
        'successful_cycle_separates_preserved_failed_review_and_regression_overhead':True,
        'clock_observations':clocks,'wall_clock_gap_cause_not_established':True,
        'monotonic_computation_time_distinguished_from_supervisor_wall_span':True,
        'temporary_idle_sleep_assertion_cleanup_recorded':True,'permanent_power_settings_changed':False,
        'owned_coordinator_locks_observed_free':locks,
        'separate_prior_create_charge_included':True,'production_worker_seconds':prod['sum_recorded_job_seconds'],
        'archive_worker_seconds':sum(archives),'audit_worker_seconds':sum(x['seconds'] for x in audits['jobs']),
        'phase_timings':phase_summary,'archive_maximum_seconds':max(archives),'archive_median_seconds':statistics.median(archives),
        'maximum_passing_column_job_seconds':max(receipt_seconds+review_rows),'maximum_production_or_audit_RSS_bytes':max(rss),
        'maximum_observed_working_store_bytes':e['maximum_observed_working_store_bytes'],'proved_working_store_bound_bytes':973167872,
        'maximum_recorded_production_concurrency':e['maximum_recorded_phase_concurrency'],
        'conservative_production_concurrent_RSS_bytes':e['conservative_sum_of_concurrent_measured_peaks_bytes'],
        'storage_observation':storage,'D156_pilot_scenario_comparison':comparison,
        'remaining_full_route_job_count':planning['remaining_column_jobs']-24579,'conditional_remaining_scenarios':remaining,
        'remaining_scenarios_replace_only_P3200_and_P6400_column_costs':True,
        'P10480_integrated_cost_still_unmeasured':True,'one_column_does_not_bound_other_columns_or_higher_stages':True,
        'full_route_free_space_requirement_before_pilot_bytes':planning['required_remaining_free_bytes'],
        'completed_pilot_retained_allowance_debited_bytes':retained_allowance,
        'conditional_remaining_free_bytes_including_10GiB_reserve':remaining_free,
        'rounded_remaining_bank_free_gate_bytes':((remaining_free+(1<<30)-1)//(1<<30))*(1<<30),
        'remaining_storage_keeps_full_largest_active_extra_and_reserve':True,
        'completed_actual_column_2_precision_pi':6400,'full_sixteen_column_bank_precision_pi':1600,'column0_precision_pi':6400,
        'next_column_or_higher_stage_admitted':False,'candidate_identification_proved':False,
        'positive_exact_quadric_vanishing_proved':False,'field_polynomial_constructed':False,
        'resource_caps_changed':False,'finite_rational_transfer_search_remains_parked':True}

if __name__=='__main__':
    assert __debug__ and not OUT.exists();tick=time.monotonic();result=calculate()
    result.update(wall_seconds=time.monotonic()-tick,
        filesystem_observation={'observed_at':datetime.now(timezone.utc).isoformat(),'free_bytes':shutil.disk_usage(ROOT).free},
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        sources=[source(p) for p in sorted(PATHS)])
    result['remaining_space_shortfall_at_observation_bytes']=max(0,result['conditional_remaining_free_bytes_including_10GiB_reserve']-result['filesystem_observation']['free_bytes'])
    result['rounded_remaining_gate_shortfall_at_observation_bytes']=max(0,result['rounded_remaining_bank_free_gate_bytes']-result['filesystem_observation']['free_bytes'])
    assert result['peak_rss_bytes']<=2*(1<<30)
    with OUT.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|653_DYADIC_HIGHER_PILOT_TIMING',flush=True)
