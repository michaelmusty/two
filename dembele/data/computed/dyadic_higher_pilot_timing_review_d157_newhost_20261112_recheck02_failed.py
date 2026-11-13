"""D157 fixed higher-pilot review, transitive replay and completion.

The existing column review supplies independent arithmetic checks. This
review authenticates that new catalogue and recomputes the timing totals
and limited repeat scenarios without importing the timing calculator.
"""
import argparse
from collections import defaultdict
import fcntl
import statistics
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P6400_col02_config_d156';BASE='dyadic_staged_P6400_col02_d156'
COLUMN_REVIEW='dyadic_higher_pilot_col02_review_r2_d157'
PIPELINE='dyadic_higher_pilot_pipeline_d157_run01'
OUT=DATA/'dyadic_higher_pilot_timing_review_d157.json'
COMPLETION=DATA/'dyadic_higher_pilot_timing_completion_d157.json'
LEDGER=DATA/'dyadic_higher_pilot_timing_sources_d157.json'
REPORT=ROOT/'dembele/certificates/dyadic-higher-pilot-timing-d157.md'
HELPER=ROOT/'dembele/pari/650_dyadic_higher_pilot_preparation_review.py'
PATHS={Path(__file__),HELPER};CACHE={}

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m);return m

prior=module(HELPER,'d157_inherited_preparation')

def raw_source(path):
    p=Path(path).resolve()
    if p not in CACHE:
        h=hashlib.sha256()
        with p.open('rb') as f:
            while raw:=f.read(1<<20):h.update(raw)
        CACHE[p]={'path':str(p),'sha256':h.hexdigest()}
    return CACHE[p]

def source(path):
    p=Path(path).resolve();PATHS.add(p);return raw_source(p)

def checked(refs):
    for ref in refs:assert raw_source(ref['path'])==ref,ref['path']

def read(stem):
    p=DATA/(stem+'.json');source(p);v=json.loads(p.read_text());assert v['status']=='pass',stem;return v

def receipt(stem,driver,args=(),suffix='_attempt01'):
    obj=read(stem);row=read(stem+suffix+'.job');expected=source(ROOT/'dembele/pari'/driver)
    assert row['driver']==expected and row['command']==['python3',expected['path']]+list(args)
    assert row['status']=='pass' and row['exit_code']==0 and 0<row['wall_seconds']<=180
    assert row['timeout_seconds']==180 and row['timeout_terminates_process_group'] and row['private_process_group']>0
    for ref in [row['driver'],row['log'],*row['sources']]:assert source(ref['path'])==ref
    lines=Path(row['log']['path']).read_text().splitlines()
    assert [json.loads(s.split('|',1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]==[source(DATA/(stem+'.json'))]
    assert any(s.startswith('PASS|'+driver[:3]+'_') for s in lines)
    if 'peak_rss_bytes' in obj:assert obj['peak_rss_bytes']<=2*(1<<30)
    return row,source(DATA/(stem+suffix+'.job.json'))

def graph():
    parent=read('dyadic_higher_pilot_preparation_review_d156');checked(parent['sources'])
    assert len(parent['sources'])==93 and parent['independent_finite_review_complete']
    assert parent['indexed_receipt_coordinator_admitted'] and parent['single_column_timing_pilot_only']
    inherited=prior.graph()
    assert all(parent[k]==v for k,v in inherited.items())
    column=read(COLUMN_REVIEW);checked(column['sources'])
    assert column['prior_fixed_review']==source(DATA/'dyadic_higher_pilot_preparation_review_d156.json')
    assert column['independent_finite_review_complete'] and column['incremental_provenance']
    # Keep the inherited P3200 catalogue's existing field names intact.
    return {**inherited,'D156_direct_bindings':93,
        'inherited_review':source(DATA/'dyadic_higher_pilot_preparation_review_d156.json'),
        'new_P6400_column_catalogue_root':source(DATA/(COLUMN_REVIEW+'.json')),
        'new_P6400_column_catalogue_bindings':len(column['sources']),
        'new_P6400_column_catalogue_rehashed':True}

def close(a,b):
    assert abs(a-b)<=1e-8*max(1,abs(a),abs(b)),(a,b)

def transcript_objects(text,marker):
    decoder=json.JSONDecoder()
    return [decoder.raw_decode(text,m.end())[0] for m in re.finditer(re.escape(marker),text)]

def raw_packet(stem):
    path=DATA/(stem+'.json');source(path);return json.loads(path.read_text())

def recovery():
    controls=read('dyadic_higher_pilot_review_controls_d157');checked(controls['sources'])
    control_row,control_ref=receipt('dyadic_higher_pilot_review_controls_d157','652_dyadic_higher_pilot_review_controls.py')
    assert controls['config']==source(DATA/(CONFIG+'.json'))
    assert controls['revised_reviewer']==source(ROOT/'dembele/pari/651_dyadic_higher_pilot_column_review_revision.py')
    assert controls['previous_reviewer']==source(ROOT/'dembele/pari/647_dyadic_higher_pilot_column_review.py')
    assert controls['only_two_guard_changes_plus_docstring_and_pass_markers']
    assert controls['production_and_audit_arithmetic_unchanged'] and controls['no_production_or_audit_jobs_rerun']
    assert controls['complete_actual_D156_audits_accepted']==24
    assert controls['malformed_in_memory_fixtures_rejected']==[
        'previous_execution_label','unknown_execution_label','missing_execution_label','unsupported_weighted_seed',
        'wrong_indexed_summary_milestone','unreconciled_receipt_inventory','wrong_receipt_lookup_source']
    failed_stem='dyadic_higher_pilot_col02_review_d156_attempt01.job'
    failed=raw_packet(failed_stem)
    assert failed['status']=='failed' and failed['exit_code']==1 and 0<failed['wall_seconds']<180
    assert failed['timeout_seconds']==180 and failed['timeout_terminates_process_group'] and failed['private_process_group']>0
    assert failed['command']==['python3',controls['previous_reviewer']['path'],'--config',CONFIG,
        '--output','dyadic_higher_pilot_col02_review_d156']
    for ref in [failed['driver'],failed['log'],failed['failed_driver_snapshot'],*failed['sources']]:
        assert source(ref['path'])==ref
    assert failed['driver']==controls['previous_reviewer']
    assert failed['driver']['sha256']==failed['failed_driver_snapshot']['sha256']
    assert "assert packet['execution_milestone'] == 'D153' and packet['weighted_seed_supported']" in Path(failed['log']['path']).read_text()
    assert controls['failed_review_receipt']==source(DATA/(failed_stem+'.json'))
    assert not (DATA/'dyadic_higher_pilot_col02_review_d156.json').exists()
    assert not (DATA/'dyadic_higher_pilot_col02_review_d156_recheck01.job.json').exists()
    launch=raw_packet(PIPELINE+'_launch');stopped=raw_packet(PIPELINE+'_status')
    power=read(PIPELINE+'_power_assertion_finished')
    assert launch['status']=='started' and stopped['status']=='stopped_after_failure'
    assert not stopped['automatic_retry_attempted'] and not power['permanent_power_settings_changed']
    assert launch['supervisor']==source(ROOT/'dembele/pari/run_d157_higher_pilot.py')
    assert launch['config']==source(DATA/(CONFIG+'.json'))
    assert launch['admission']==source(DATA/'dyadic_higher_pilot_preparation_review_d156.json')
    assert launch['maximum_mathematical_workers']==3 and launch['mathematical_job_timeout_seconds']==180
    assert launch['no_other_column_or_stage_admitted']
    source(DATA/(PIPELINE+'.log'))
    assert not (DATA/(PIPELINE+'_completed.json')).exists()
    assert [s['name'] for s in stopped['completed_stages']]==['production','audits','column_review']
    assert [s['exit_code'] for s in stopped['completed_stages']]==[0,0,1]
    for i,stage in enumerate(stopped['completed_stages']):
        assert stage['command']==launch['stages'][i]['command']
        assert source(stage['log']['path'])==stage['log']
        if i<2:assert source(stage['output']['path'])==stage['output']
    launch_ref=launch['launch_check_receipt'];assert source(launch_ref['path'])==launch_ref
    launch_row=json.loads(Path(launch_ref['path']).read_text())
    assert launch_row['driver']==source(HELPER)
    assert launch_row['command']==['python3',str(HELPER),'--launch-check']
    assert launch_row['status']=='pass' and launch_row['exit_code']==0
    assert 0<launch_row['wall_seconds']<launch_row['timeout_seconds']==180
    assert launch_row['timeout_terminates_process_group'] and launch_row['private_process_group']>0
    for ref in [launch_row['driver'],launch_row['log'],*launch_row['sources']]:assert source(ref['path'])==ref
    log=Path(launch_row['log']['path']).read_text()
    assert transcript_objects(log,'PHASE_METADATA|')==[launch['admission']]
    gates=transcript_objects(log,'D156_LAUNCH_SPACE_CHECK|');assert len(gates)==1
    assert gates[0]['free_bytes']>=gates[0]['required_bytes']==12*(1<<30)
    assert gates[0]['empty_initial_pool_only'] and not gates[0]['coordinator_started']
    assert 'PASS|650_DYADIC_HIGHER_PILOT_PREPARATION_REVIEW' in log
    return controls,failed,stopped,control_row,control_ref,launch_ref

def inputs():
    cfg=read(CONFIG);parent=read(cfg['admission_review']);column=read(COLUMN_REVIEW)
    done=read('dyadic_higher_pilot_preparation_completion_d156')
    assert done['fixed_review']==source(DATA/(cfg['admission_review']+'.json'))
    assert done['successful_bounded_jobs']==13 and done['failed_bounded_jobs']==0
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        receipt(cfg['admission_review'],HELPER.name,args,'_'+suffix)
    receipt('dyadic_higher_pilot_preparation_completion_d156',HELPER.name,['--finish'])
    assert parent['permitted_configs']==[source(DATA/(CONFIG+'.json'))]
    assert (cfg['precision_pi'],cfg['seed_precision_pi'],cfg['column'])==(6400,3200,2)
    assert cfg['column_review']=='dyadic_higher_pilot_col02_review_d156'
    assert column['working_precision_pi']==6400 and column['harmonic_basis_column']==2
    assert column['execution_milestone']=='D156'
    assert column['passing_input_jobs']==24577 and column['failed_bounded_input_jobs']==0
    e,a,store=(column['certificates'][k] for k in ('execution','independent','store'))
    assert e['actual_phases']==24456 and e['metadata_archive_jobs']==97 and e['corrections']==96
    assert e['full_original_weighted_equation_scalars']==8908800 and e['all_fixed_masses']==174
    assert e['complete_CM_scalars']==1740800 and e['coarse_values']==68
    assert e['coarse_errors_beta']==[12832,12848,12832,12864]
    assert a['audit_jobs']==24 and a['complete_old_weighted_overlap_scalars']==4454400
    assert a['old_CM_overlap_scalars']==870400 and a['coarse_old_overlaps']==68
    assert a['ordinary_state_scalars']==a['ordinary_CM_scalars']==72 and a['independent_Horner_beta_scalars']==96
    assert a['sampled_not_complete_independent_operators']
    assert store['epoch']==194 and store['history_records']==194 and store['retirement_records']==97
    assert e['maximum_observed_working_store_bytes']<=e['proved_inventory_bound_bytes']==973167872
    assert e['maximum_recorded_phase_concurrency']<=3 and e['maximum_measured_job_RSS_bytes']<=2*(1<<30)
    assert e['conservative_sum_of_concurrent_measured_peaks_bytes']<=6*(1<<30)
    cm=read(cfg['CM_output']);assert column['CM_adapter']==source(DATA/(cfg['CM_output']+'.json'))
    assert cm['working_precision_pi']==6400 and cm['harmonic_basis_column']==2
    assert cm['coarse_error_beta']==[12832,12848,12832,12864]
    seal=read(BASE+'_seal');assert seal['certificate']=={'original_weighted_fixed_point':True,'all_fixed_masses':True}
    assert seal['weighted_input'] and seal['working_precision_pi']==6400
    controls,failed,stopped,control_row,control_ref,launch_ref=recovery()
    assert controls['actual_audit_certificate']==a
    refs=[];review_seconds=[]
    for suffix,extra in [('attempt01',[]),('recheck01',['--check'])]:
        row,ref=receipt(COLUMN_REVIEW,'651_dyadic_higher_pilot_column_review_revision.py',
            ['--config',CONFIG,'--output',COLUMN_REVIEW]+extra,'_'+suffix)
        refs.append(ref);review_seconds.append(row['wall_seconds'])
    timing=read('dyadic_higher_pilot_timing_d157');checked(timing['sources'])
    _,timing_ref=receipt('dyadic_higher_pilot_timing_d157','653_dyadic_higher_pilot_timing.py')
    prod=read(BASE+'_completed');audit=read(cfg['audit_plan']+'_completed')
    assert prod['all_phases_complete'] and prod['completed_jobs']==24456 and prod['maximum_workers']==3
    assert prod['receipt_inventory']['reconciled'] and prod['receipt_inventory']['source']==source(ROOT/'dembele/pari/576_dyadic_receipt_lookup.py')
    assert audit['completed_jobs']==24 and audit['worker_limit']==3
    reused=[x for x in prod['jobs'] if x['reused_receipt']];assert len(reused)==1 and reused[0]['key']=='create'
    seconds=prod['wall_seconds']+audit['wall_seconds']+sum(review_seconds)+reused[0]['seconds']
    close(seconds,timing['measured_column_cycle_active_seconds']);close(seconds/3600,timing['measured_column_cycle_active_hours'])
    close(timing['failed_column_review_seconds'],failed['wall_seconds'])
    close(timing['observed_cycle_plus_failed_review_and_regression_seconds'],seconds+failed['wall_seconds']+control_row['wall_seconds'])
    assert timing['preserved_failed_column_review_attempts']==1
    assert timing['total_column_jobs']==24579 and timing['new_passing_column_jobs_this_continuation']==24578
    assert timing['successful_cycle_separates_preserved_failed_review_and_regression_overhead']
    for stage in stopped['completed_stages']:
        c=timing['clock_observations'][stage['name']]
        assert (c['started_utc'],c['ended_utc'])==(stage['started_utc'],stage['ended_utc'])
        span=(datetime.fromisoformat(stage['ended_utc'])-datetime.fromisoformat(stage['started_utc'])).total_seconds()
        close(c['supervisor_wall_span_seconds'],span)
        close(c['supervisor_monotonic_seconds'],stage['monotonic_seconds'])
        close(c['wall_span_minus_supervisor_monotonic_seconds'],span-stage['monotonic_seconds'])
    for label,summary in [('production',prod),('audits',audit)]:
        close(timing['clock_observations'][label]['coordinator_monotonic_seconds'],summary['wall_seconds'])
    assert timing['wall_clock_gap_cause_not_established'] and timing['monotonic_computation_time_distinguished_from_supervisor_wall_span']
    assert timing['temporary_idle_sleep_assertion_cleanup_recorded'] and not timing['permanent_power_settings_changed']
    close(sum(x['seconds'] for x in prod['jobs']),timing['production_worker_seconds'])
    close(sum(x['seconds'] for x in audit['jobs']),timing['audit_worker_seconds'])
    archive_seconds=[]
    for item in prod['metadata_archives']:
        ref=item['receipt'];checked([ref]);r=json.loads(Path(ref['path']).read_text())
        assert r['status']=='pass' and r['timeout_seconds']==180
        archive_seconds.append(r['wall_seconds'])
    assert len(archive_seconds)==97
    close(sum(archive_seconds),timing['archive_worker_seconds']);close(max(archive_seconds),timing['archive_maximum_seconds'])
    close(statistics.median(archive_seconds),timing['archive_median_seconds'])
    close(max(x['peak_rss_bytes'] for x in prod['jobs']+audit['jobs']),timing['maximum_production_or_audit_RSS_bytes'])
    close(max([x['seconds'] for x in prod['jobs']+audit['jobs']]+archive_seconds+review_seconds),timing['maximum_passing_column_job_seconds'])
    byphase=defaultdict(list)
    for row in prod['jobs']:
        packet=json.loads(Path(row['metadata']['path']).read_text());byphase[packet['request']['phase']].append(row)
    assert set(byphase)==set(timing['phase_timings'])
    for name,rows in byphase.items():
        t=timing['phase_timings'][name];assert t['jobs']==len(rows)
        close(t['worker_seconds'],sum(r['seconds'] for r in rows))
        close(t['maximum_job_seconds'],max(r['seconds'] for r in rows))
        close(t['median_job_seconds'],statistics.median(r['seconds'] for r in rows))
        close(t['summed_callback_seconds'],sum(r['coordinator_interval'][1]-r['coordinator_interval'][0] for r in rows))
        close(t['summed_nonnegative_callback_overhead_seconds'],sum(max(0,r['coordinator_interval'][1]-r['coordinator_interval'][0]-r['seconds']) for r in rows if not r['reused_receipt']))
    full=read('precision_route_cost_d152')['schedules'][0]
    planning=read('dyadic_storage_timing_plan_d156');earlier=read('dyadic_pilot_timing_d154')
    assert timing['remaining_full_route_job_count']==planning['remaining_column_jobs']-24579==1022790
    assert len(timing['conditional_remaining_scenarios'])==len(timing['D156_pilot_scenario_comparison'])==2
    for b,p,c,r in zip(full['timing_scenarios'],planning['pilot']['timing_scenarios'],timing['D156_pilot_scenario_comparison'],timing['conditional_remaining_scenarios']):
        assert b['scenario']==p['scenario']==c['scenario']==r['scenario']
        close(c['observed_to_modeled_column_ratio'],seconds/p['column_cycle_seconds'])
        close(c['modeled_column_seconds'],p['column_cycle_seconds'])
        close(c['modeled_total_hours_with_shared_allowances'],p['total_active_hours'])
        first=14*earlier['measured_column_cycle_active_seconds'];second=14*seconds
        last=16*b['stages'][2]['active_seconds_per_column']
        tail=b['retained_graph_review_seconds_allowance']+b['retained_common_comparison_seconds_allowance']
        assert (r['remaining_P3200_columns'],r['remaining_P6400_columns'],r['remaining_P10480_columns'])==(14,14,16)
        for key,value in [('same_cost_remaining_P3200_hours',first/3600),('same_cost_remaining_P6400_hours',second/3600),
            ('unchanged_unmeasured_P10480_hours',last/3600),('unchanged_graph_and_comparison_hours',tail/3600),
            ('remaining_total_active_hours',(first+second+last+tail)/3600),('remaining_total_active_days',(first+second+last+tail)/86400)]:close(r[key],value)
    debit=planning['stages'][1]['retained_allowance_per_column_bytes']
    remaining_free=sum(n*s['retained_allowance_per_column_bytes'] for n,s in zip((14,14,16),planning['stages']))+planning['largest_active_extra_bytes']+10*(1<<30)
    assert timing['completed_pilot_retained_allowance_debited_bytes']==debit==1254739040
    assert remaining_free==planning['required_remaining_free_bytes']-debit==75002411056
    assert timing['conditional_remaining_free_bytes_including_10GiB_reserve']==remaining_free
    rounded=((remaining_free+(1<<30)-1)//(1<<30))*(1<<30)
    assert timing['rounded_remaining_bank_free_gate_bytes']==rounded==70*(1<<30)
    free=timing['filesystem_observation']['free_bytes']
    assert timing['remaining_space_shortfall_at_observation_bytes']==max(0,remaining_free-free)
    assert timing['rounded_remaining_gate_shortfall_at_observation_bytes']==max(0,rounded-free)
    assert timing['remaining_storage_keeps_full_largest_active_extra_and_reserve']
    log=DATA/'dyadic_higher_pilot_production_d157_run01.log';source(log);text=log.read_text()
    rows=transcript_objects(text,'D132_JOB|')
    assert len(rows)==24456 and len({x['key'] for x in rows})==24456
    expected={x['key']:{'key':x['key'],'seconds':x['seconds'],'reused':x['reused_receipt'],'peak_rss_bytes':x['peak_rss_bytes']} for x in prod['jobs']}
    assert all(expected[x['key']]==x for x in rows)
    assert transcript_objects(text,'D132_COMPLETE|')==[source(DATA/(BASE+'_completed.json'))]
    log=DATA/'dyadic_higher_pilot_audits_d157_run01.log';source(log);text=log.read_text()
    rows=transcript_objects(text,'D137_JOB|')
    assert len(rows)==24 and {x['stem']:x for x in rows}=={x['stem']:x for x in audit['jobs']}
    assert transcript_objects(text,'D137_BATCH_COMPLETE|')==[source(DATA/(cfg['audit_plan']+'_completed.json'))]
    assert not timing['next_column_or_higher_stage_admitted'] and not timing['candidate_identification_proved']
    assert timing['remaining_scenarios_replace_only_P3200_and_P6400_column_costs'] and timing['P10480_integrated_cost_still_unmeasured']
    assert timing['one_column_does_not_bound_other_columns_or_higher_stages']
    assert not timing['field_polynomial_constructed'] and not timing['resource_caps_changed']
    return {'column_review_receipts':refs,'timing_receipt':timing_ref,'review_regression_receipt':control_ref,
        'launch_check_receipt':launch_ref,'preserved_failed_review_receipt':controls['failed_review_receipt'],
        'revised_reviewer_admitted_for_completed_D156_column':controls['revised_reviewer'],
        'original_config_and_failed_artifacts_preserved':True,'production_and_audit_arithmetic_unchanged':True,
        'measured_column_cycle_active_seconds':seconds,
        'remaining_active_days_scenarios':[x['remaining_total_active_days'] for x in timing['conditional_remaining_scenarios']],
        'remaining_free_bytes_including_reserve':remaining_free,'rounded_remaining_bank_free_gate_bytes':rounded,
        'remaining_space_shortfall_at_observation_bytes':timing['remaining_space_shortfall_at_observation_bytes'],
        'rounded_remaining_gate_shortfall_at_observation_bytes':timing['rounded_remaining_gate_shortfall_at_observation_bytes']}

def links(path,text,missing=()):
    result=[]
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if link.startswith(('http://','https://','#')):continue
        p=(path.parent/link.split('#',1)[0]).resolve();assert p.is_file() or p in missing,(path,link);result.append(p)
    return result

def build():
    inherited=graph();print('D157_TRANSITIVE_GRAPH_PASS',flush=True);values=inputs()
    report_links=links(REPORT,REPORT.read_text(),(OUT,LEDGER,COMPLETION))
    ledger={'status':'pass','milestone':'D157','external_sources':[],
        'scope':'Completed column-2 P6400 pilot, preserved review failure, corrected guards and measured timing.',
        'source_policy':'Frozen D156 admission, unchanged production/auditor arithmetic, source-651 revised column review, source-652 regression controls and inherited D152/D154 scenarios.',
        'inspected_reports':[source(p) for p in sorted(set(report_links)) if p.suffix=='.md'],
        'independent_equation_checks_are_sampled':True,'P10480_integrated_cost_still_unmeasured':True,'sources':[source(REPORT)]}
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER)
    return {'status':'pass','milestone':'D157','independent_finite_review_complete':True,
        'catalogue_graph_is_transitive':True,**inherited,**values,
        'complete_passing_column_jobs':24579,'inherited_preparation_create_jobs':1,
        'new_passing_column_jobs_this_continuation':24578,'preserved_failed_bounded_input_jobs':1,
        'actual_column2_precision_pi':6400,'full_sixteen_column_bank_precision_pi':1600,'column0_precision_pi':6400,
        'working_store_bound_bytes':973167872,'all_caps_retained':True,
        'actual_complete_original_weighted_equations_certified':True,'complete_new_operator_independently_recomputed':False,
        'timing_totals_and_conditional_repeat_scenarios_independently_checked':True,
        'P10480_integrated_cost_still_unmeasured':True,'next_column_or_stage_admitted':False,
        'full_bank_storage_capacity_resolved':False,'candidate_identification_proved':False,
        'positive_exact_quadric_vanishing_proved':False,'field_polynomial_constructed':False,
        'finite_rational_transfer_search_remains_parked':True,'report_local_links_checked':len(report_links),
        'sources':[source(p) for p in sorted(PATHS)]}

def finish():
    saved=read(OUT.stem);checked(saved['sources']);refs=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        row,ref=receipt(OUT.stem,Path(__file__).name,args,'_'+suffix);refs.append(ref)
        measures=transcript_objects(Path(row['log']['path']).read_text(),'D157_REVIEW_RESOURCES|')
        assert len(measures)==1 and measures[0]['peak_rss_bytes']<=2*(1<<30)
        resources.append({'receipt_wall_seconds':row['wall_seconds'],**measures[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md'];targets=[]
    for name in docs:
        p=ROOT/name;block=p.read_text().split('<!-- D157 higher pilot timing checkpoint -->',1)[1].split('<!-- End D157 higher pilot timing checkpoint -->',1)[0]
        assert all(s in block for s in ['6400','1600','24579','source 655 is next unused'])
        targets.extend(links(p,block,(COMPLETION,)))
    assert len(targets)==28
    cfg=read(CONFIG);locks=[PIPELINE+'.lock',BASE+'.lock',cfg['audit_plan']+'.lock']
    for name in locks:
        with (DATA/name).open('r') as f:
            fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(f,fcntl.LOCK_UN)
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update(completed_at=datetime.now(timezone.utc).isoformat(),fixed_review=source(OUT),report=source(REPORT),
        source_applicability_ledger=source(LEDGER),review_receipts=refs,review_resources=resources,
        successful_bounded_jobs_this_continuation=24584,reused_preparation_create_jobs=1,
        total_passing_column_jobs_including_reused_create=24579,
        additional_passing_bounded_jobs_outside_column=6,
        additional_jobs_breakdown={'launch_check':1,'review_regression':1,'timing':1,'fixed_review_and_replay':2,'completion':1},
        failed_bounded_jobs_this_continuation=1,failed_production_or_audit_jobs=0,
        supervisor_failure_preserved_and_separate_review_recovery_complete=True,
        completion_job_receipt_path=str(DATA/'dyadic_higher_pilot_timing_completion_d157_attempt01.job.json'),
        entry_documents_updated=docs,current_artifact_links_checked=len(targets),direct_source_bindings=len(saved['sources']),
        next_unused_source=655,entry_document_hashes_intentionally_not_frozen=True,
        owned_coordinator_locks_observed_free=locks,no_new_coordinator_launched_during_recovery=True)
    with COMPLETION.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    assert all(p.is_file() for p in targets)

if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__);modes=ap.add_mutually_exclusive_group()
    modes.add_argument('--check',action='store_true');modes.add_argument('--finish',action='store_true');args=ap.parse_args()
    tick=time.monotonic();out=OUT
    if args.finish:finish();out=COMPLETION
    elif args.check:
        saved=read(OUT.stem);checked(saved['sources']);inherited=graph();values=inputs()
        assert all(saved[k]==v for k,v in (inherited|values).items())
    else:
        assert not OUT.exists();saved=build()
        saved.update(wall_seconds=time.monotonic()-tick,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
        assert saved['peak_rss_bytes']<=2*(1<<30)
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<=2*(1<<30)
    print('D157_REVIEW_RESOURCES|'+json.dumps({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(raw_source(out)),flush=True)
    print('PASS|654_DYADIC_HIGHER_PILOT_TIMING_REVIEW',flush=True)

