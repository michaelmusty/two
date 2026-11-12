"""D154 fixed actual-pilot review, transitive replay and completion.

The existing column review supplies independent arithmetic checks. This
review authenticates that new catalogue and recomputes the timing totals
and limited repeat scenarios without importing the timing calculator.
"""
import argparse
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
CONFIG='dyadic_staged_P3200_col02_config_d153';BASE='dyadic_staged_P3200_col02_d153'
OUT=DATA/'dyadic_pilot_timing_review_d154.json'
COMPLETION=DATA/'dyadic_pilot_timing_completion_d154.json'
LEDGER=DATA/'dyadic_pilot_timing_sources_d154.json'
REPORT=ROOT/'dembele/certificates/dyadic-pilot-timing-d154.md'
HELPER=ROOT/'dembele/pari/639_dyadic_pilot_preparation_review.py'
PATHS={Path(__file__),HELPER};CACHE={}

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m);return m

prior=module(HELPER,'d154_inherited_preparation')

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
    parent=read('dyadic_pilot_preparation_review_d153');checked(parent['sources'])
    assert len(parent['sources'])==89 and parent['independent_finite_review_complete']
    assert parent['indexed_receipt_coordinator_admitted'] and parent['single_column_timing_pilot_only']
    inherited=prior.graph()
    cfg=read(CONFIG);column=read(cfg['column_review']);checked(column['sources'])
    assert column['prior_fixed_review']==source(DATA/'dyadic_pilot_preparation_review_d153.json')
    assert column['independent_finite_review_complete'] and column['incremental_provenance']
    return {'D153_direct_bindings':89,**inherited,
            'new_column_catalogue_root':source(DATA/(cfg['column_review']+'.json')),
            'new_column_catalogue_bindings':len(column['sources']),
            'new_column_catalogue_rehashed':True}

def close(a,b):
    assert abs(a-b)<=1e-8*max(1,abs(a),abs(b)),(a,b)

def transcript_objects(text,marker):
    # Concurrent print calls can place two complete JSON payloads on the
    # same line. Decode each marker's JSON value without requiring its LF.
    decoder=json.JSONDecoder()
    return [decoder.raw_decode(text,m.end())[0] for m in re.finditer(re.escape(marker),text)]

def inputs():
    cfg=read(CONFIG);parent=read(cfg['admission_review']);column=read(cfg['column_review'])
    done=read('dyadic_pilot_preparation_completion_d153')
    assert done['fixed_review']==source(DATA/(cfg['admission_review']+'.json'))
    assert done['successful_bounded_jobs']==12 and done['failed_bounded_jobs']==0
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        receipt(cfg['admission_review'],HELPER.name,args,'_'+suffix)
    receipt('dyadic_pilot_preparation_completion_d153',HELPER.name,['--finish'])
    assert parent['permitted_configs']==[source(DATA/(CONFIG+'.json'))]
    assert (cfg['precision_pi'],cfg['seed_precision_pi'],cfg['column'])==(3200,1600,2)
    assert column['working_precision_pi']==3200 and column['harmonic_basis_column']==2
    assert column['passing_input_jobs']==12568 and column['failed_bounded_input_jobs']==0
    e,a,store=(column['certificates'][k] for k in ('execution','independent','store'))
    assert e['actual_phases']==12495 and e['metadata_archive_jobs']==49 and e['corrections']==48
    assert e['full_original_weighted_equation_scalars']==4454400 and e['all_fixed_masses']==174
    assert e['complete_CM_scalars']==870400 and e['coarse_values']==68
    assert e['coarse_errors_beta']==[6432,6448,6432,6464]
    assert a['audit_jobs']==24 and a['complete_old_weighted_overlap_scalars']==2227200
    assert a['old_CM_overlap_scalars']==435200 and a['coarse_old_overlaps']==68
    assert a['ordinary_state_scalars']==a['ordinary_CM_scalars']==72 and a['independent_Horner_beta_scalars']==96
    assert a['sampled_not_complete_independent_operators']
    assert store['epoch']==98 and store['history_records']==98 and store['retirement_records']==49
    assert e['maximum_observed_working_store_bytes']<=e['proved_inventory_bound_bytes']==304049792
    assert e['maximum_recorded_phase_concurrency']<=3 and e['maximum_measured_job_RSS_bytes']<=2*(1<<30)
    assert e['conservative_sum_of_concurrent_measured_peaks_bytes']<=6*(1<<30)
    cm=read(cfg['CM_output']);assert column['CM_adapter']==source(DATA/(cfg['CM_output']+'.json'))
    assert cm['working_precision_pi']==3200 and cm['harmonic_basis_column']==2 and cm['coarse_error_beta']==[6432,6448,6432,6464]
    seal=read(BASE+'_seal');assert seal['certificate']=={'original_weighted_fixed_point':True,'all_fixed_masses':True}
    assert seal['weighted_input'] and seal['working_precision_pi']==3200
    refs=[];review_seconds=[]
    for suffix,extra in [('attempt01',[]),('recheck01',['--check'])]:
        row,ref=receipt(cfg['column_review'],'636_dyadic_pilot_column_review.py',
            ['--config',CONFIG,'--output',cfg['column_review']]+extra,'_'+suffix)
        refs.append(ref);review_seconds.append(row['wall_seconds'])
    timing=read('dyadic_pilot_timing_d154');checked(timing['sources'])
    row,timing_receipt=receipt('dyadic_pilot_timing_d154','640_dyadic_pilot_timing.py')
    prod=read(BASE+'_completed');audit=read(cfg['audit_plan']+'_completed')
    assert prod['all_phases_complete'] and prod['completed_jobs']==12495 and prod['maximum_workers']==3
    assert audit['completed_jobs']==24 and audit['worker_limit']==3
    reused=[x for x in prod['jobs'] if x['reused_receipt']];assert len(reused)==1 and reused[0]['key']=='create'
    seconds=prod['wall_seconds']+audit['wall_seconds']+sum(review_seconds)+reused[0]['seconds']
    close(seconds,timing['measured_column_cycle_active_seconds'])
    close(seconds/3600,timing['measured_column_cycle_active_hours'])
    for label,summary in [('production',prod),('audits',audit)]:
        c=timing['clock_observations'][label]
        close(c['coordinator_monotonic_seconds'],summary['wall_seconds'])
        close(c['filesystem_wall_span_seconds'],c['log_last_write_epoch_seconds']-c['log_birth_epoch_seconds'])
        close(c['wall_span_minus_coordinator_seconds'],c['filesystem_wall_span_seconds']-summary['wall_seconds'])
    assert timing['recorded_host_sleep_seconds']==sum(x['recorded_duration_seconds'] for x in timing['host_sleep_events_during_production'])
    assert timing['monotonic_computation_time_distinguished_from_filesystem_wall_span']
    close(sum(x['seconds'] for x in prod['jobs']),timing['production_worker_seconds'])
    close(sum(x['seconds'] for x in audit['jobs']),timing['audit_worker_seconds'])
    archive_seconds=[]
    for item in prod['metadata_archives']:
        ref=item['receipt'];checked([ref]);r=json.loads(Path(ref['path']).read_text())
        assert r['status']=='pass' and r['timeout_seconds']==180
        archive_seconds.append(r['wall_seconds'])
    close(sum(archive_seconds),timing['archive_worker_seconds'])
    close(max(archive_seconds),timing['archive_maximum_seconds'])
    close(max(x['peak_rss_bytes'] for x in prod['jobs']+audit['jobs']),timing['maximum_production_or_audit_RSS_bytes'])
    model=read('precision_route_cost_d152');full,pilot=model['schedules']
    assert timing['remaining_full_route_job_count']==1047369
    for b,p,c,r in zip(full['timing_scenarios'],pilot['timing_scenarios'],timing['D152_pilot_scenario_comparison'],timing['conditional_remaining_scenarios']):
        close(c['observed_to_modeled_column_ratio'],seconds/p['stages'][0]['active_seconds_per_column'])
        later=sum(s['active_seconds_per_column']*s['columns'] for s in b['stages'][1:])
        tail=b['retained_graph_review_seconds_allowance']+b['retained_common_comparison_seconds_allowance']
        close(r['remaining_total_active_hours'],(14*seconds+later+tail)/3600)
        close(r['remaining_total_active_days'],r['remaining_total_active_hours']/24)
        assert r['remaining_P3200_columns']==14
    pc=pilot['storage_components']
    debit=sum(pc[k] for k in ('payload_bytes','metadata_logical_bytes','incremental_catalogue_allowance_bytes'))+12570*20480
    assert timing['completed_pilot_retained_allowance_debited_bytes']==debit
    remaining_free=full['recommended_free_bytes_including_10GiB_reserve']-debit
    assert timing['conditional_remaining_free_bytes_including_10GiB_reserve']==remaining_free
    assert timing['remaining_space_shortfall_at_observation_bytes']==max(0,remaining_free-timing['filesystem_observation']['free_bytes'])
    # Authenticate the durable coordinator transcripts against every summary
    # row; output order may differ inside a concurrent window.
    log=ROOT/'dembele/data/computed/dyadic_pilot_production_d154_run01.log';source(log)
    transcript=log.read_text()
    jobs=transcript_objects(transcript,'D132_JOB|')
    assert len(jobs)==12495 and len({x['key'] for x in jobs})==12495
    expected={x['key']:{'key':x['key'],'seconds':x['seconds'],'reused':x['reused_receipt'],'peak_rss_bytes':x['peak_rss_bytes']} for x in prod['jobs']}
    assert all(expected[x['key']]==x for x in jobs)
    assert transcript_objects(transcript,'D132_COMPLETE|')==[source(DATA/(BASE+'_completed.json'))]
    log=ROOT/'dembele/data/computed/dyadic_pilot_audits_d154_run01.log';source(log)
    transcript=log.read_text();rows=transcript_objects(transcript,'D137_JOB|')
    assert len(rows)==24 and {x['stem']:x for x in rows}=={x['stem']:x for x in audit['jobs']}
    assert transcript_objects(transcript,'D137_BATCH_COMPLETE|')==[source(DATA/(cfg['audit_plan']+'_completed.json'))]
    assert not timing['next_column_or_higher_stage_admitted'] and not timing['candidate_identification_proved']
    assert timing['remaining_scenarios_only_replace_P3200_column_cost'] and timing['one_column_does_not_bound_other_columns_or_higher_stages']
    assert not timing['field_polynomial_constructed'] and not timing['resource_caps_changed']
    return {'column_review_receipts':refs,'timing_receipt':timing_receipt,'measured_column_cycle_active_seconds':seconds,
            'remaining_active_days_scenarios':[x['remaining_total_active_days'] for x in timing['conditional_remaining_scenarios']],
            'remaining_free_bytes_including_reserve':remaining_free,
            'remaining_space_shortfall_at_observation_bytes':timing['remaining_space_shortfall_at_observation_bytes']}

def links(path,text,missing=()):
    result=[]
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if link.startswith(('http://','https://','#')):continue
        p=(path.parent/link.split('#',1)[0]).resolve();assert p.is_file() or p in missing,(path,link);result.append(p)
    return result

def build():
    inherited=graph();print('D154_TRANSITIVE_GRAPH_PASS',flush=True);values=inputs()
    report_links=links(REPORT,REPORT.read_text(),(OUT,LEDGER,COMPLETION))
    ledger={'status':'pass','milestone':'D154','external_sources':[],
            'scope':'One actual column-2 P3200 pilot and measured timing; no next-stage admission.',
            'source_policy':'Frozen D153 admission and arithmetic interfaces, completed column catalogue, actual bounded receipts and D152 planning scenarios.',
            'inspected_reports':[source(p) for p in sorted(set(report_links)) if p.suffix=='.md'],
            'independent_equation_checks_are_sampled':True,'higher_stage_costs_still_unmeasured':True,'sources':[source(REPORT)]}
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER)
    return {'status':'pass','milestone':'D154','independent_finite_review_complete':True,
            'catalogue_graph_is_transitive':True,'inherited_review':source(DATA/'dyadic_pilot_preparation_review_d153.json'),
            **inherited,**values,'complete_column_jobs':12570,'inherited_preparation_create_jobs':1,
            'new_column_jobs_this_continuation':12569,'failed_bounded_input_jobs':0,
            'actual_column2_precision_pi':3200,'full_sixteen_column_bank_precision_pi':1600,'column0_precision_pi':6400,
            'working_store_bound_bytes':304049792,'all_caps_retained':True,
            'actual_complete_original_weighted_equations_certified':True,
            'complete_new_operator_independently_recomputed':False,
            'timing_totals_and_conditional_repeat_scenarios_independently_checked':True,
            'one_column_does_not_bound_higher_stages':True,'next_column_or_stage_admitted':False,
            'candidate_identification_proved':False,'positive_exact_quadric_vanishing_proved':False,'field_polynomial_constructed':False,
            'finite_rational_transfer_search_remains_parked':True,'report_local_links_checked':len(report_links),
            'sources':[source(p) for p in sorted(PATHS)]}

def finish():
    saved=read(OUT.stem);checked(saved['sources']);refs=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        row,ref=receipt(OUT.stem,Path(__file__).name,args,'_'+suffix);refs.append(ref)
        measures=[json.loads(s.split('|',1)[1]) for s in Path(row['log']['path']).read_text().splitlines() if s.startswith('D154_REVIEW_RESOURCES|')]
        assert len(measures)==1 and measures[0]['peak_rss_bytes']<=2*(1<<30)
        resources.append({'receipt_wall_seconds':row['wall_seconds'],**measures[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md'];targets=[]
    for name in docs:
        p=ROOT/name;block=p.read_text().split('<!-- D154 pilot timing checkpoint -->',1)[1].split('<!-- End D154 pilot timing checkpoint -->',1)[0]
        assert all(s in block for s in ['3200','1600','12570','source 642 is next unused'])
        targets.extend(links(p,block,(COMPLETION,)))
    assert len(targets)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update(completed_at=datetime.now(timezone.utc).isoformat(),fixed_review=source(OUT),report=source(REPORT),
        source_applicability_ledger=source(LEDGER),review_receipts=refs,review_resources=resources,
        successful_bounded_jobs_this_continuation=12573,reused_preparation_create_jobs=1,
        total_column_jobs_including_reused_create=12570,additional_timing_and_fixed_review_jobs=4,
        failed_bounded_jobs_this_continuation=0,completion_job_receipt_path=str(DATA/'dyadic_pilot_timing_completion_d154_attempt01.job.json'),
        entry_documents_updated=docs,current_artifact_links_checked=len(targets),direct_source_bindings=len(saved['sources']),
        next_unused_source=642,entry_document_hashes_intentionally_not_frozen=True)
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
    print('D154_REVIEW_RESOURCES|'+json.dumps({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(raw_source(out)),flush=True)
    print('PASS|641_DYADIC_PILOT_TIMING_REVIEW',flush=True)
