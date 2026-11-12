"""D156 fixed pilot admission, transitive replay and preparation completion.

Only one exact P6400/column-2 configuration is admitted. No schedule is
launched here. --check replays the frozen preparation; --finish checks docs.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import resource
import shutil
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P6400_col02_config_d156';BASE='dyadic_staged_P6400_col02_d156'
OUT=DATA/'dyadic_higher_pilot_preparation_review_d156.json'
LEDGER=DATA/'dyadic_higher_pilot_preparation_sources_d156.json'
COMPLETION=DATA/'dyadic_higher_pilot_preparation_completion_d156.json'
REPORT=ROOT/'dembele/certificates/dyadic-higher-pilot-preparation-d156.md'
HELPER=ROOT/'dembele/pari/644_proof_criterion_review.py'
PATHS={Path(__file__),HELPER};CACHE={}
DEPS=['646_dyadic_higher_pilot_independent.py','647_dyadic_higher_pilot_column_review.py',
      '648_dyadic_higher_pilot_setup.py','649_dyadic_higher_pilot_controls.py',
      'run_d139_indexed_production.py','run_d137_audits.py','run_dyadic_capped.py',
      '554_dyadic_resumable_staged_production.py','547_dyadic_staged_store.py',
      '576_dyadic_receipt_lookup.py','577_dyadic_indexed_metadata_archive.py']

def module(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

prior=module(HELPER,'d156_inherited_graph')

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

def graph():
    parent=read('proof_criterion_review_d155');checked(parent['sources'])
    assert parent['independent_finite_review_complete'] and len(parent['sources'])==35
    inherited=prior.graph()
    proof=prior.inputs()
    assert all(parent[k]==v for k,v in (inherited|proof).items())
    done=read('proof_criterion_completion_d155')
    assert done['fixed_review']==source(DATA/'proof_criterion_review_d155.json')
    assert done['successful_bounded_jobs_this_continuation']==5 and done['failed_bounded_jobs_this_continuation']==0
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        job('proof_criterion_review_d155',HELPER.name,args,'_'+suffix)
    job('proof_criterion_completion_d155',HELPER.name,['--finish'])
    return {**inherited,'D155_direct_bindings':35,
            'inherited_review':source(DATA/'proof_criterion_review_d155.json'),
            'D155_conditional_criterion_replayed':True}

def job(stem,driver,args=(),receipt_suffix='_attempt01'):
    packet=read(stem);row=read(stem+receipt_suffix+'.job')
    expected=source(ROOT/'dembele/pari'/driver)
    assert row['driver']==expected and row['command']==['python3',expected['path']]+list(args)
    assert row['status']=='pass' and row['exit_code']==0 and 0<row['wall_seconds']<180
    assert row['timeout_seconds']==180 and row['private_process_group']>0 and row['timeout_terminates_process_group']
    for ref in [row['driver'],row['log'],*row['sources']]:assert source(ref['path'])==ref
    lines=Path(row['log']['path']).read_text().splitlines()
    assert [json.loads(s.split('|',1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]==[source(DATA/(stem+'.json'))]
    assert any(s.startswith('PASS|'+driver[:3]+'_') for s in lines)
    checked(packet.get('sources',[]))
    peak=packet.get('peak_rss_bytes')
    if peak is None:
        assert list(args)==['--finish']
        measures=[json.loads(s.split('|',1)[1]) for s in lines if re.match(r'D\d+_REVIEW_RESOURCES\|',s)]
        assert len(measures)==1;peak=measures[0]['peak_rss_bytes']
    assert peak<=2*(1<<30)
    return {'receipt':source(DATA/(stem+receipt_suffix+'.job.json')),
            'metadata':source(DATA/(stem+'.json')),'wall_seconds':row['wall_seconds'],
            'peak_rss_bytes':peak}

def validate_inputs():
    receipts=[job('dyadic_storage_timing_plan_d156','645_dyadic_storage_timing_plan.py'),
              job('dyadic_higher_pilot_setup_d156','648_dyadic_higher_pilot_setup.py')]
    plan=read('dyadic_storage_timing_plan_d156');checked(plan['sources'])
    replay=module(ROOT/'dembele/pari/645_dyadic_storage_timing_plan.py','d156_cost_replay').calculate()
    assert all(plan[k]==v for k,v in replay.items())
    cfg=read(CONFIG);assert (cfg['precision_pi'],cfg['seed_precision_pi'],cfg['column'])==(6400,3200,2)
    assert cfg['working_store_bound_bytes']==plan['pilot']['working_store_bound_bytes']==973167872
    assert cfg['launch_free_space_gate_bytes']==plan['pilot']['rounded_free_gate_bytes']==12*(1<<30)
    assert plan['filesystem_observation']['free']<plan['rounded_full_bank_free_gate_bytes']
    assert cfg['namespace']=='dyadic_rowjournal_P6400_col02_d156_d132' and cfg['output_prefix']==BASE
    assert cfg['execution_milestone']=='D156' and cfg['milestone']=='D132'
    assert (cfg['digit_bits'],cfg['state_chunk'],cfg['rhs_chunk'],cfg['CM_chunk'])==(200,1,3,1)
    assert cfg['admission_review']==OUT.stem and cfg['admission_replay_receipt']==OUT.stem+'_recheck01.job'
    setup=read('dyadic_higher_pilot_setup_d156');assert setup['config']==source(DATA/(CONFIG+'.json'))
    bridge=read(cfg['prior_review']);checked(bridge['sources'])
    known={}
    for stem in ['dyadic_precision1600_review_d138','dyadic_pilot_col02_review_d153']:
        for ref in read(stem)['sources']:
            assert ref['path'] not in known or known[ref['path']]==ref['sha256']
            known[ref['path']]=ref['sha256']
    for ref in bridge['sources']:assert known[ref['path']]==ref['sha256']
    assert bridge['native_dependency_closure_complete'] and not bridge['production_schedule_admitted_by_this_bridge']
    assert setup['seed_bridge']==source(DATA/(cfg['prior_review']+'.json'))
    assert setup['audit_plan']==source(DATA/(cfg['audit_plan']+'.json'))
    seed,cm=read(cfg['seed']),read(cfg['CM_reference'])
    assert seed['weighted_input'] and seed['certificate']=={'original_weighted_fixed_point':True,'all_fixed_masses':True}
    assert seed['working_precision_pi']==cm['working_precision_pi']==3200
    assert seed['harmonic_basis_column']==cm['harmonic_basis_column']==2
    assert cm['coarse_error_beta']==[6432,6448,6432,6464]
    for name in DEPS:source(ROOT/'dembele/pari'/name)
    # Recompute the complete native closure from source 554, not merely a
    # convenient transitive root. INPUTS is immutable after create; mutable
    # pool files and their prospective payload hashes are never root sources.
    engine=module(ROOT/'dembele/pari/554_dyadic_resumable_staged_production.py','d156_input_engine')
    deps=engine.immutable_dependencies()|{DATA/(cfg['seed']+'.json'),DATA/(cfg['CM_reference']+'.json'),
        Path(seed['state_file']['path']),DATA/'dyadic_target_transports_d121.json',DATA/'dyadic_harmonic_certificate_d111.json',
        *(Path(ch['file']['path']) for ch in cm['moment_chunks'])}
    assert {str(p.resolve()) for p in deps}=={r['path'] for r in bridge['sources']}
    for ref in bridge['sources']:assert source(ref['path'])==ref
    inputs_path=DATA/cfg['namespace']/'INPUTS.json';inputs=json.loads(inputs_path.read_text())
    assert hashlib.sha256(json.dumps(inputs['value'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==inputs['sha256']
    source(inputs_path);inputs=inputs['value'];checked(inputs['sources'])
    assert inputs['seed']==engine.row_manifest(seed['state_file'],3200,400,True,174,known)
    assert inputs['CM_precision_pi']==3200 and inputs['CM_chunks']==cm['moment_chunks']
    for ch in cm['moment_chunks']:
        assert inputs['CM_'+str(ch['first_chart'])]==engine.row_manifest(ch['file'],6400,400,False,ch['last_chart']-ch['first_chart']+1,known)
    stem=BASE+'_create'
    receipts.append(job(stem,'554_dyadic_resumable_staged_production.py',
        ['--config',CONFIG,'--output',stem,'--phase','create','--key','create']))
    create=read(stem);assert create['certificates']=={'weighted_state_bytes':449407200,'old_seed_read_as_weighted_representative':True}
    assert create['maximum_observed_store_bytes']<=973167872
    cases=[('states',['--phase','states','--first','0','--last','28']),
           ('cm',['--phase','cm','--first','0','--last','2']),
           ('ordinary_state',['--phase','ordinary-state','--state','83']),
           ('ordinary_cm',['--phase','ordinary-cm','--chart','8']),
           ('horner',['--phase','coarse-horner','--chart','16','--order','3']),('review',['--control'])]
    for label,args in cases:
        stem='dyadic_higher_pilot_'+label+'_control_d156'
        driver='647_dyadic_higher_pilot_column_review.py' if label=='review' else '646_dyadic_higher_pilot_independent.py'
        receipts.append(job(stem,driver,args+['--config','dyadic_staged_P6400_col00_config_d133','--output',stem]))
    receipts.append(job('dyadic_higher_pilot_controls_d156','649_dyadic_higher_pilot_controls.py'))
    controls=read('dyadic_higher_pilot_controls_d156')
    replay=module(ROOT/'dembele/pari/649_dyadic_higher_pilot_controls.py','d156_control_replay').calculate()
    assert all(controls[k]==v for k,v in replay.items())
    assert controls['total_pilot_jobs']==24579 and controls['wrong_overlap_flag_digest_length_and_top_bits_rejected']==8
    assert setup['filesystem_observation']['free_bytes']>=setup['planning_scenario']['rounded_free_gate_bytes']
    return receipts

def prelaunch_state():
    cfg=read(CONFIG);store=DATA/cfg['namespace']
    assert not (store/'CURRENT.json').exists() and not (store/'SEALED.json').exists()
    pool=json.loads((store/'pool_initial.json').read_text())
    assert hashlib.sha256(json.dumps(pool['value'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==pool['sha256']
    assert not pool['value']['complete'] and pool['value']['row_sha256']==[None]*174
    assert (store/'state.bin').stat().st_size==449407200
    assert not (DATA/(BASE+'_completed.json')).exists()
    lookup=module(ROOT/'dembele/pari/576_dyadic_receipt_lookup.py','d156_receipt_inventory')
    inv=lookup.ReceiptInventory(DATA,BASE)
    assert inv.preflight(BASE+'_create')==[DATA/(BASE+'_create_attempt01.job.json')]
    # This exact create receipt will be reused by the admitted coordinator.
    receipts=list(DATA.glob(BASE+'*_attempt*.job.json'))
    assert receipts==[DATA/(BASE+'_create_attempt01.job.json')]
    return {'empty_initial_pool_only':True,'initialized_rows':0,'actual_new_moments_evaluated':False,
            'existing_create_receipt_will_be_reused':True,'logical_store_bytes_at_preparation':sum(p.stat().st_size for p in store.iterdir())}

def local_links(path,text,allowed_missing=()):
    results=[]
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if link.startswith(('https://','http://','#')):continue
        p=(path.parent/link.split('#',1)[0]).resolve()
        assert p.is_file() or p in allowed_missing,(path,link);results.append(p)
    return results

def space_gate(free_bytes, required_bytes):
    assert type(free_bytes) is int and type(required_bytes) is int
    assert required_bytes >= 10*(1<<30)
    assert free_bytes >= required_bytes, 'insufficient current free space for this pilot and reserve'

def launch_check():
    saved=read(OUT.stem);checked(saved['sources'])
    done=read(COMPLETION.stem)
    assert done['fixed_review']==source(OUT)
    cfg=read(CONFIG)
    assert saved['permitted_configs']==[source(DATA/(CONFIG+'.json'))]
    assert saved['indexed_receipt_coordinator_admitted'] and saved['single_column_timing_pilot_only']
    job(OUT.stem,Path(__file__).name,['--check'],'_recheck01')
    assert cfg['launch_free_space_gate_bytes']==saved['free_bytes_required_including_reserve']==12*(1<<30)
    for key in ['PYTHONDONTWRITEBYTECODE','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS',
                'MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:
        assert os.environ.get(key)=='1', key
    initial=prelaunch_state()
    for stem in [BASE,cfg['audit_plan']]:
        path=DATA/(stem+'.lock')
        if path.exists():
            with path.open('rb') as stream:
                fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
                fcntl.flock(stream,fcntl.LOCK_UN)
    free=shutil.disk_usage(ROOT).free
    space_gate(free,cfg['launch_free_space_gate_bytes'])
    print('D156_LAUNCH_SPACE_CHECK|'+json.dumps({'observed_at':datetime.now(timezone.utc).isoformat(),
        'free_bytes':free,'required_bytes':cfg['launch_free_space_gate_bytes'],
        'empty_initial_pool_only':initial['empty_initial_pool_only'],
        'not_a_reservation':True,'coordinator_started':False}),flush=True)

def build():
    inherited=graph();print('D156_TRANSITIVE_GRAPH_PASS',flush=True)
    previous=read('proof_criterion_completion_d155')
    receipts=validate_inputs();initial=prelaunch_state()
    links=local_links(REPORT,REPORT.read_text(),(OUT,LEDGER,COMPLETION))
    reports=sorted({p for p in links if p.suffix=='.md'})
    ledger={'status':'pass','milestone':'D156','scope':'Prepare one column-2 P3200-to-P6400 integrated timing pilot.',
            'external_sources':[],'inspected_reports':[source(p) for p in reports],
            'source_policy':'Reuse D154 certified P3200 seed, D138 native closure, frozen schedules and D139 interruption controls.',
            'independent_operator_checks_are_samples':True,'no_new_geometric_or_height_claim':True,
            'synthetic_control_data_are_not_actual_new_precision':True,'sources':[source(REPORT)]}
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER);setup=read('dyadic_higher_pilot_setup_d156')
    return {'status':'pass','milestone':'D156','independent_finite_review_complete':True,
            'catalogue_graph_is_transitive':True,**inherited,
            'indexed_receipt_coordinator_admitted':True,'permitted_configs':[source(DATA/(CONFIG+'.json'))],
            'single_column_timing_pilot_only':True,'production_schedule_launched':False,
            'full_bank_or_P10480_stage_admitted':False,'preparation_state':initial,
            'input_receipts':receipts,'completed_input_jobs':len(receipts),'preserved_failed_input_jobs':0,
            'production_jobs':24456,'archive_jobs':97,'audit_jobs':24,'column_review_jobs':2,'total_pilot_jobs':24579,
            'working_store_bound_bytes':973167872,'direct_seed_native_bindings':setup['direct_seed_native_bindings'],
            'independent_full_old_weighted_overlap_scalars':174*3200*8,'independent_full_old_CM_overlap_scalars':17*6400*8,
            'independent_original_equations_are_sampled':True,
            'storage_plan':source(DATA/'dyadic_storage_timing_plan_d156.json'),
            'full_bank_storage_capacity_resolved':False,
            'free_bytes_observed':setup['filesystem_observation']['free_bytes'],
            'free_bytes_required_including_reserve':setup['planning_scenario']['rounded_free_gate_bytes'],
            'modeled_pilot_active_hours':[s['total_active_hours'] for s in setup['planning_scenario']['timing_scenarios']],
            'runtime_is_empirical_not_a_bound':True,'resource_caps_changed':False,'actual_harmonic_precision_increased':False,
            'finite_rational_transfer_search_remains_parked':True,'candidate_identification_proved':False,
            'positive_exact_quadric_vanishing_proved':False,'field_polynomial_constructed':False,
            'full_bank_precision_pi':1600,'column0_precision_pi':6400,'column2_precision_pi':3200,
            'report_local_links_checked':len(links),'next_work':'After the separate launch decision and fresh launch-space check, run only the reviewed column-2 P6400 pilot, then all 24 audits and both column reviews; record integrated timing and reassess before any next column or stage.',
            'sources':[source(p) for p in sorted(PATHS)]}

def finish():
    saved=read(OUT.stem);checked(saved['sources']);refs=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        record=job(OUT.stem,Path(__file__).name,args,'_'+suffix);refs.append(record['receipt'])
        row=read(OUT.stem+'_'+suffix+'.job')
        marks=[json.loads(s.split('|',1)[1]) for s in Path(row['log']['path']).read_text().splitlines() if s.startswith('D156_REVIEW_RESOURCES|')]
        assert len(marks)==1 and marks[0]['peak_rss_bytes']<=2*(1<<30)
        resources.append({'receipt_wall_seconds':row['wall_seconds'],**marks[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md']
    links=[]
    for name in docs:
        p=ROOT/name
        block=p.read_text().split('<!-- D156 pilot preparation checkpoint -->',1)[1].split('<!-- End D156 pilot preparation checkpoint -->',1)[0]
        assert all(s in block for s in ['6400','3200','24579','source 651 is next unused'])
        links.extend(local_links(p,block,(COMPLETION,)))
    assert len(links)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update(completed_at=datetime.now(timezone.utc).isoformat(),fixed_review=source(OUT),
        report=source(REPORT),source_applicability_ledger=source(LEDGER),review_receipts=refs,review_resources=resources,
        successful_bounded_jobs=13,input_bounded_jobs=10,review_bounded_jobs=2,completion_bounded_jobs=1,failed_bounded_jobs=0,
        completion_job_receipt_path=str(DATA/'dyadic_higher_pilot_preparation_completion_d156_attempt01.job.json'),
        entry_documents_updated=docs,current_artifact_links_checked=len(links),direct_source_bindings=len(saved['sources']),
        next_unused_source=651,entry_document_hashes_intentionally_not_frozen=True,all_D156_preparation_jobs_sequential=True)
    with COMPLETION.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    assert all(p.is_file() for p in links)

if __name__=='__main__':
    assert __debug__;parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--check',action='store_true');modes.add_argument('--finish',action='store_true');modes.add_argument('--launch-check',action='store_true');args=parser.parse_args()
    tick=time.monotonic();out=OUT
    if args.launch_check:launch_check()
    elif args.finish:finish();out=COMPLETION
    elif args.check:
        saved=read(OUT.stem);checked(saved['sources']);inherited=graph()
        assert all(saved[k]==v for k,v in inherited.items())
        assert validate_inputs()==saved['input_receipts']
    else:
        assert not OUT.exists();saved=build()
        saved.update(wall_seconds=time.monotonic()-tick,
            peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
        assert saved['peak_rss_bytes']<=2*(1<<30)
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert peak<=2*(1<<30)
    print('D156_REVIEW_RESOURCES|'+json.dumps({'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(raw_source(out)),flush=True)
    print('PASS|650_DYADIC_HIGHER_PILOT_PREPARATION_REVIEW',flush=True)
