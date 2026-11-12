"""D153 single-column pilot configuration and direct seed/native input closure.

This prepares inputs only. It does not execute a production schedule.
"""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import shutil
import sys
import time

ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'dembele/data/computed'
CONFIG='dyadic_staged_P3200_col02_config_d153'
BASE='dyadic_staged_P3200_col02_d153'
BRIDGE='dyadic_pilot_seed_bridge_d153'
PLAN='dyadic_pilot_col02_audit_plan_d153'
ADMISSION='dyadic_pilot_preparation_review_d153'
OUT='dyadic_pilot_setup_d153'
PATHS={Path(__file__)}

def source(path):
    p=Path(path).resolve();PATHS.add(p);h=hashlib.sha256()
    with p.open('rb') as f:
        while raw:=f.read(1<<20):h.update(raw)
    return {'path':str(p),'sha256':h.hexdigest()}

def read(stem):
    p=DATA/(stem+'.json');source(p);v=json.loads(p.read_text());assert v['status']=='pass';return v

def module(name):
    p=ROOT/'dembele/pari'/name;source(p)
    s=importlib.util.spec_from_file_location('pilot_'+name[:3],p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def save(stem,value):
    p=DATA/(stem+'.json');text=json.dumps(value,indent=2)+'\n'
    if p.exists():assert p.read_text()==text
    else:
        with p.open('x') as f:f.write(text)
    return source(p)

def setup():
    parent=read('dyadic_precision1600_review_d138')
    known={r['path']:r['sha256'] for r in parent['sources']}
    seed_stem='dyadic_staged_P1600_col02_r2_d137_seal'
    cm_stem='dyadic_CM_P1600_col02_r2_d137'
    seed,cm=read(seed_stem),read(cm_stem)
    assert seed['working_precision_pi']==cm['working_precision_pi']==1600
    assert seed['harmonic_basis_column']==cm['harmonic_basis_column']==2
    assert seed['weighted_input'] and seed['certificate']['original_weighted_fixed_point']
    assert seed['certificate']['all_fixed_masses']
    assert cm['coarse_error_beta']==[3232,3248,3232,3264]
    engine=module('554_dyadic_resumable_staged_production.py')
    dependencies=engine.immutable_dependencies() | {
        DATA/(seed_stem+'.json'),DATA/(cm_stem+'.json'),Path(seed['state_file']['path']),
        DATA/'dyadic_target_transports_d121.json',DATA/'dyadic_harmonic_certificate_d111.json',
        *(Path(ch['file']['path']) for ch in cm['moment_chunks'])}
    refs=[source(p) for p in sorted(dependencies)]
    for ref in refs:
        # D138 explicitly carries this closure, including the frozen engine.
        assert known[ref['path']]==ref['sha256'],ref['path']
    inv=module('567_dyadic_checkpoint_admission_revision.py').inventory(3200,1600)
    assert inv['maximum_bound']['total_bytes']==304049792
    cfg={'status':'pass','milestone':'D132','execution_milestone':'D153',
         'namespace':'dyadic_rowjournal_P3200_col02_d153_d132','output_prefix':BASE,
         'precision_pi':3200,'seed_precision_pi':1600,'column':2,
         'seed':seed_stem,'CM_reference':cm_stem,'prior_review':BRIDGE,
         'admission_review':ADMISSION,'admission_replay_receipt':ADMISSION+'_recheck01.job',
         'digit_bits':200,'state_chunk':1,'rhs_chunk':3,'CM_chunk':1,
         'audit_plan':PLAN,'CM_output':'dyadic_CM_P3200_col02_d153',
         'column_review':'dyadic_pilot_col02_review_d153',
         'working_store_bound_bytes':304049792,
         'purpose':'One column-2 P1600-to-P3200 timing pilot only; no automatic next column or stage.'}
    assert not (DATA/cfg['namespace']).exists(), 'new preparation needs a fresh namespace'
    oldplan=read('dyadic_precision6400_audit_plan_d133');jobs=[]
    for previous in oldplan['jobs']:
        label=previous['stem'].removeprefix('dyadic_precision6400_').removesuffix('_d133')
        jobs.append({'driver':'dembele/pari/635_dyadic_pilot_independent.py',
                     'stem':'dyadic_pilot_col02_'+label+'_d153',
                     'marker':'PASS|635_DYADIC_PILOT_INDEPENDENT',
                     'args':previous['args']+['--config',CONFIG]})
    assert len(jobs)==24
    bridge={'status':'pass','milestone':'D153','kind':'direct_seed_native_dependency_bridge',
            'inherited_review':source(DATA/'dyadic_precision1600_review_d138.json'),
            'all_sources_directly_bound_by_inherited_review':True,
            'working_precision_pi':1600,'harmonic_basis_column':2,
            'weighted_seed':True,'native_dependency_closure_complete':True,
            'production_schedule_admitted_by_this_bridge':False,'sources':refs}
    save(BRIDGE,bridge);save(CONFIG,cfg)
    save(PLAN,{'status':'pass','milestone':'D137','execution_milestone':'D153',
               'legacy_harness_schema_retained':True,'kind':'bounded_job_plan','config':CONFIG,
               'requires_completed_and_sealed_actual_column':True,'maximum_workers':3,'jobs':jobs})
    cost=read('precision_route_cost_d152');pilot=cost['schedules'][1]
    free=shutil.disk_usage(ROOT).free
    assert free>=pilot['recommended_free_bytes_including_10GiB_reserve']
    return {'status':'pass','milestone':'D153','config':source(DATA/(CONFIG+'.json')),
            'seed_bridge':source(DATA/(BRIDGE+'.json')),'audit_plan':source(DATA/(PLAN+'.json')),
            'inventory':inv,'direct_seed_native_bindings':len(refs),
            'planning_scenario':pilot,
            'filesystem_observation':{'observed_at':datetime.now(timezone.utc).isoformat(),'free_bytes':free},
            'new_moments_evaluated':False,'production_schedule_launched':False,
            'candidate_identification_proved':False,'field_polynomial_constructed':False}

if __name__=='__main__':
    assert __debug__ and not (DATA/(OUT+'.json')).exists();tick=time.monotonic()
    result=setup();result.update(wall_seconds=time.monotonic()-tick,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        sources=[source(p) for p in sorted(PATHS)])
    assert result['peak_rss_bytes']<=2*(1<<30)
    ref=save(OUT,result);print('PHASE_METADATA|'+json.dumps(ref),flush=True)
    print('PASS|637_DYADIC_PILOT_SETUP',flush=True)
