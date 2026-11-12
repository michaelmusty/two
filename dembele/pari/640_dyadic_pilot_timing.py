"""D154 measured one-column timing and explicitly limited repeat scenarios.

Run after production, all independent audits and column review/replay.
No other column or higher precision is admitted by this assessment.
"""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import re
import shutil
import statistics
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P3200_col02_config_d153';BASE='dyadic_staged_P3200_col02_d153'
OUT=DATA/'dyadic_pilot_timing_d154.json'
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
    cfg=read(CONFIG);review=read(cfg['column_review']);prod=read(BASE+'_completed');audits=read(cfg['audit_plan']+'_completed')
    plan=read(cfg['audit_plan']);parent=read(cfg['admission_review'])
    assert parent['indexed_receipt_coordinator_admitted'] and parent['permitted_configs']==[source(DATA/(CONFIG+'.json'))]
    assert review['prior_fixed_review']==source(DATA/(cfg['admission_review']+'.json'))
    assert review['independent_finite_review_complete'] and review['incremental_provenance']
    assert review['execution_milestone']=='D153' and review['working_precision_pi']==3200 and review['harmonic_basis_column']==2
    assert (cfg['precision_pi'],cfg['seed_precision_pi'],cfg['column'])==(3200,1600,2)
    assert prod['coordinator']==source(ROOT/'dembele/pari/run_d139_indexed_production.py')
    assert prod['completed_jobs']==12495 and len(prod['metadata_archives'])==49
    assert prod['all_phases_complete'] and prod['maximum_workers']==3 and prod['receipt_inventory']['reconciled']
    assert audits['completed_jobs']==24 and audits['worker_limit']==3 and len(plan['jobs'])==24
    assert audits['coordinator']==source(ROOT/'dembele/pari/run_d137_audits.py')
    e,a,store=(review['certificates'][x] for x in ('execution','independent','store'))
    assert e['actual_phases']==12495 and e['metadata_archive_jobs']==49 and e['corrections']==48
    assert e['full_original_weighted_equation_scalars']==174*3200*8
    assert e['complete_CM_scalars']==17*6400*8 and e['coarse_errors_beta']==[6432,6448,6432,6464]
    assert a['audit_jobs']==24 and a['complete_old_weighted_overlap_scalars']==174*1600*8
    assert a['old_CM_overlap_scalars']==17*3200*8
    assert e['maximum_observed_working_store_bytes']<=e['proved_inventory_bound_bytes']==304049792
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
        stem=cfg['column_review']+'_'+suffix+'.job';raw=read(stem)
        assert raw['command']==['python3',str(ROOT/'dembele/pari/636_dyadic_pilot_column_review.py'),
            '--config',CONFIG,'--output',cfg['column_review']]+extra
        assert raw['status']=='pass' and raw['exit_code']==0 and raw['timeout_seconds']==180 and raw['timeout_terminates_process_group']
        assert source(raw['driver']['path'])==raw['driver'] and source(raw['log']['path'])==raw['log']
        marks=[json.loads(s.split('|',1)[1]) for s in Path(raw['log']['path']).read_text().splitlines() if s.startswith('PHASE_METADATA|')]
        assert marks==[source(DATA/(cfg['column_review']+'.json'))]
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
    cost=read('precision_route_cost_d152');pilot=cost['schedules'][1];full=cost['schedules'][0]
    comparison=[];remaining=[]
    for expected,bank in zip(pilot['timing_scenarios'],full['timing_scenarios']):
        modeled_column=expected['stages'][0]['active_seconds_per_column']
        assert expected['stages'][0]['columns']==1 and expected['stages'][0]['target']==3200
        comparison.append({'scenario':expected['scenario'],'modeled_column_seconds':modeled_column,
            'modeled_total_hours_with_bank_allowances':expected['active_hours'],
            'observed_to_modeled_column_ratio':active/modeled_column,
            'retained_model_graph_and_comparison_seconds':expected['retained_graph_review_seconds_allowance']+expected['retained_common_comparison_seconds_allowance']})
        assert [(x['seed'],x['target'],x['columns']) for x in bank['stages']]==[(1600,3200,15),(3200,6400,15),(6400,10480,16)]
        later=sum(x['columns']*x['active_seconds_per_column'] for x in bank['stages'][1:])
        tail=bank['retained_graph_review_seconds_allowance']+bank['retained_common_comparison_seconds_allowance']
        remaining.append({'scenario':bank['scenario'],'remaining_P3200_columns':14,
            'same_cost_remaining_P3200_hours':14*active/3600,
            'unchanged_unmeasured_higher_stage_hours':later/3600,
            'unchanged_graph_and_comparison_hours':tail/3600,
            'remaining_total_active_hours':(14*active+later+tail)/3600,
            'remaining_total_active_days':(14*active+later+tail)/86400})
    owned.update(DATA/(stem+'.json') for stem in [CONFIG,cfg['audit_plan'],BASE+'_completed',cfg['audit_plan']+'_completed',cfg['column_review'],cfg['CM_output']])
    store_files=list((DATA/cfg['namespace']).iterdir())
    assert all(p.is_file() for p in store_files)
    storage={label:{'files':len(paths),'logical_bytes':sum(p.stat().st_size for p in paths),
                    'allocated_bytes':sum(p.stat().st_blocks*512 for p in paths)}
             for label,paths in [('sealed_store',store_files),('external_column_artifacts',sorted(owned))]}
    assert storage['sealed_store']['logical_bytes']==store['retained_store_bytes']
    assert all(p.is_file() for p in owned)
    components=pilot['storage_components']
    retained_allowance=(components['payload_bytes']+components['metadata_logical_bytes']+
                        components['incremental_catalogue_allowance_bytes']+12570*20480)
    remaining_free=full['recommended_free_bytes_including_10GiB_reserve']-retained_allowance
    clocks={}
    for label,filename,elapsed in [('production','dyadic_pilot_production_d154_run01.log',prod['wall_seconds']),
                                   ('audits','dyadic_pilot_audits_d154_run01.log',audits['wall_seconds'])]:
        log=DATA/filename;source(log);st=log.stat()
        assert hasattr(st,'st_birthtime') and st.st_mtime>=st.st_birthtime
        clocks[label]={'log_birth_epoch_seconds':st.st_birthtime,'log_last_write_epoch_seconds':st.st_mtime,
            'log_birth_utc':datetime.fromtimestamp(st.st_birthtime,timezone.utc).isoformat(),
            'log_last_write_utc':datetime.fromtimestamp(st.st_mtime,timezone.utc).isoformat(),
            'filesystem_wall_span_seconds':st.st_mtime-st.st_birthtime,
            'coordinator_monotonic_seconds':elapsed,
            'wall_span_minus_coordinator_seconds':st.st_mtime-st.st_birthtime-elapsed}
    sleep_log=DATA/'dyadic_pilot_sleep_events_final_d154.log';source(sleep_log)
    sleep_rows=[]
    for line in sleep_log.read_text().splitlines():
        match=re.match(r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d [+-]\d{4}).*Entering Sleep state.*?\s(\d+) secs\s*$',line)
        assert match,line
        epoch=datetime.strptime(match[1],'%Y-%m-%d %H:%M:%S %z').timestamp()
        if clocks['production']['log_birth_epoch_seconds']<=epoch<=clocks['production']['log_last_write_epoch_seconds']:
            sleep_rows.append({'entered_epoch_seconds':epoch,'recorded_duration_seconds':int(match[2]),'record':line})
    # This read-only allocation observation is not a guarantee about clones,
    # future free space, or the unmeasured higher-precision stages.
    return {'status':'pass','milestone':'D154','column':2,'seed_precision_pi':1600,'precision_pi':3200,
        'config':source(DATA/(CONFIG+'.json')),'fixed_column_review':source(DATA/(cfg['column_review']+'.json')),
        'production_jobs':12495,'archive_jobs':49,'audit_jobs':24,'column_review_jobs':2,'total_column_jobs':12570,
        'prior_preparation_create_jobs_reused':1,'new_column_jobs_this_continuation':12569,
        'production_coordinator_seconds':prod['wall_seconds'],'audit_coordinator_seconds':audits['wall_seconds'],
        'column_review_seconds':review_rows,'prior_create_seconds':reused[0]['seconds'],
        'measured_column_cycle_active_seconds':active,'measured_column_cycle_active_hours':active/3600,
        'measurement_excludes_other_D153_preparation_and_D154_final_assessment':True,
        'clock_observations':clocks,'host_sleep_events_during_production':sleep_rows,
        'recorded_host_sleep_seconds':sum(x['recorded_duration_seconds'] for x in sleep_rows),
        'monotonic_computation_time_distinguished_from_filesystem_wall_span':True,
        'filesystem_wall_span_is_an_observation_not_an_exact_launch_timer':True,
        'temporary_idle_sleep_prevention_used_after_host_sleep_observed':True,
        'separate_prior_create_charge_included':True,'production_worker_seconds':prod['sum_recorded_job_seconds'],
        'archive_worker_seconds':sum(archives),'audit_worker_seconds':sum(x['seconds'] for x in audits['jobs']),
        'phase_timings':phase_summary,'archive_maximum_seconds':max(archives),'archive_median_seconds':statistics.median(archives),
        'maximum_input_job_seconds':max(receipt_seconds+review_rows),'maximum_production_or_audit_RSS_bytes':max(rss),
        'maximum_observed_working_store_bytes':e['maximum_observed_working_store_bytes'],'proved_working_store_bound_bytes':304049792,
        'maximum_recorded_production_concurrency':e['maximum_recorded_phase_concurrency'],
        'conservative_production_concurrent_RSS_bytes':e['conservative_sum_of_concurrent_measured_peaks_bytes'],
        'storage_observation':storage,'D152_pilot_scenario_comparison':comparison,
        'remaining_full_route_job_count':1059939-12570,'conditional_remaining_scenarios':remaining,
        'remaining_scenarios_only_replace_P3200_column_cost':True,
        'one_column_does_not_bound_other_columns_or_higher_stages':True,
        'full_route_free_space_requirement_before_pilot_bytes':full['recommended_free_bytes_including_10GiB_reserve'],
        'completed_pilot_retained_allowance_debited_bytes':retained_allowance,
        'conditional_remaining_free_bytes_including_10GiB_reserve':remaining_free,
        'remaining_storage_keeps_full_largest_active_extra_and_reserve':True,
        'old_bank_timing_is_still_an_unmeasured_scenario':True,
        'completed_actual_column_2_precision_pi':3200,'full_sixteen_column_bank_precision_pi':1600,'column0_precision_pi':6400,
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
    assert result['peak_rss_bytes']<=2*(1<<30)
    with OUT.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|640_DYADIC_PILOT_TIMING',flush=True)
