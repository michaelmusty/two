"""D137 lossless P800 interfaces, bounded inventory and P1600-only admission.

Rehash the inherited catalogue once; column reviews subsequently retain
separate deltas bound to this immutable root. No precision is gained here.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil
import sys
import threading
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_checkpoint_admission_d137.json'
PATHS={Path(__file__),ROOT/'dembele/certificates/dyadic-checkpoint-admission-d137.md'};CACHE={}

def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:
        h=hashlib.sha256()
        with path.open('rb') as f:
            while raw:=f.read(1<<20):h.update(raw)
        CACHE[path]={'path':str(path),'sha256':h.hexdigest()}
    return CACHE[path]

def checked(rows):
    for row in rows:assert source(row['path'])==row,row['path']

def read(stem):
    p=DATA/(stem+'.json');PATHS.add(p);v=json.loads(p.read_text());assert v['status']=='pass',stem;return v

def save(path,value):
    text=json.dumps(value,indent=2)+'\n'
    if path.exists():assert path.read_text()==text,path.name
    else:
        with path.open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
    return source(path)

def module(name,path):
    path=ROOT/'dembele/pari'/path;source(path)
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def inventory(P,S):
    assert P%8==S%8==0 and 400<=S<P<=10552
    N,R,K=174,32,P//8;reserve=64*(1<<20);cap=2*(1<<30)
    Wrow=sum(((K if k<=32 else max(0,(P-k-i+7)//8))+7)//8 for k in range(P) for i in range(8));W=N*Wrow
    def residual(u):return N*max(33,P-u)*8*((K-u//8+7)//8)
    def low(bits):return N*R*8*((bits+7)//8)
    metadata=8*(1<<20);records=[];permanent=0
    def add(phase,step,payload,meta):
        records.append({'phase':phase,'step':step,'payload_and_reserve_bytes':payload+reserve,
                        'metadata_bound_bytes':meta,'total_bytes':payload+reserve+meta})
    add('initial_row_pool',0,W+N,metadata+N*8192);step=0
    while True:
        seed=step==0;u=0 if seed else S+33*(step-1);bits=K-u//8;oldR=N if seed else residual(u)
        digits=list(range(min(bits,200),bits,200))+[bits]
        jobs=2*N+6+5+3*len(digits)+(N if seed else 0)
        transient_records=(jobs+8)*8192;pool_history=(2*len(digits)+1)*16384
        context_history=6*65536;archive_intent=512*(1<<10)
        live_meta=metadata+transient_records+pool_history+context_history+archive_intent;oldbits=0
        for new in digits:
            add('low_residual_solve_verify',step,W+oldR+low(bits)+low(oldbits)+low(new-oldbits)+low(new),live_meta);oldbits=new
        add('journal_prepare',step,W+oldR+low(bits)*2+2*Wrow+2*(oldR//N),live_meta)
        after=S if seed else min(P,u+33);newR=residual(after)
        add('operator_sweep',step,W+oldR+newR,live_meta)
        metadata+=pool_history+context_history+archive_intent;permanent+=jobs*(16384+4096)
        if max(33,P-after)==33:break
        step+=1
    cm=17*2*P*8*((K+7)//8);final_meta=metadata+(N+17+68+10)*8192+2*65536
    add('weighted_verification_CM_publication',step,W+residual(after)+cm+N*32,final_meta)
    largest=max(records,key=lambda x:x['total_bytes']);assert largest['total_bytes']<cap
    return {'precision_pi':P,'seed_precision_pi':S,'correction_steps':step,'single_working_store':True,
            'scratch_cap_bytes':cap,'weighted_bytes':W,'CM_bytes':cm,'phase_inventory':records,
            'maximum_bound':largest,'margin_bytes':cap-largest['total_bytes'],
            'external_phase_record_allowance_bytes':permanent,
            'requires_duplicate_job_record_archival_after_each_sweep':True,
            'metadata_ceiling_violations_must_stop_before_next_phase':True,
            'concurrent_RAM_budget_bytes':6*(1<<30),'per_job_measured_RSS_admission_bytes':2*(1<<30),
            'RAM_budget_is_admission_from_measured_peaks_not_OS_hard_limit':True}

def controls():
    pairs=[('states','dyadic_precision6400_states_e000_028_d133'),('cm','dyadic_precision6400_cm_c00_02_d133'),
           ('horner','dyadic_precision6400_horner_c16_o3_d133'),
           ('ordinary_state','dyadic_precision6400_ordinary_state_e083_d133'),
           ('ordinary_cm','dyadic_precision6400_ordinary_cm_c08_d133')]
    for key,previous in pairs:
        stem='dyadic_checkpoint_'+key+'_control_d137';meta=read(stem);old=read(previous)
        assert meta['certificates']==old['certificates'] and meta['production_arithmetic_not_imported']
        verify_receipt(stem)
    meta=read('dyadic_checkpoint_review_control_d137')
    assert meta['known_D133_complete_schedule_and_store_match'] and meta['passing_production_and_archive_receipts']==24553
    verify_receipt('dyadic_checkpoint_review_control_d137')
    # Same finite inventory formula at all three frozen known-answer stages.
    old=read('dyadic_staged_lifetime_inventory_d132')['certificates']['schedules']
    for row in old:assert inventory(row['precision_pi'],row['seed_precision_pi'])==row
    prod=module('checkpoint_schedule','run_d137_production.py')
    visited=[]
    def fail(i):visited.append(i);raise RuntimeError('expected fixture failure')
    try:prod.run_window(list(range(9)),fail,1)
    except RuntimeError as exc:assert str(exc)=='expected fixture failure'
    else:raise AssertionError('failure was swallowed')
    assert visited==[0]
    barrier=threading.Barrier(3);active=peak=0;lock=threading.Lock()
    def success(i):
        nonlocal active,peak
        with lock:active+=1;peak=max(peak,active)
        barrier.wait(timeout=5)
        with lock:active-=1
        return i*i
    assert prod.run_window(list(range(6)),success,3)==[i*i for i in range(6)] and peak==3 and active==0
    return {'known_answer_audit_jobs':5,'complete_D133_production_review_control':True,
            'inventory_known_answer_stages':3,'failure_stops_submission':True,'ordered_three_worker_window':True}

# Wrapper receipts use .job.json, unlike the mathematical metadata.
def verify_receipt(stem):
    path=DATA/(stem+'_attempt01.job.json');source(path);r=json.loads(path.read_text())
    assert r['status']=='pass' and r['exit_code']==0 and r['timeout_seconds']==180 and r['timeout_terminates_process_group']
    checked([r['driver'],r['log'],*r['sources']]);meta=source(DATA/(stem+'.json'))
    marks=[json.loads(x.split('|',1)[1]) for x in Path(r['log']['path']).read_text().splitlines() if x.startswith('PHASE_METADATA|')]
    assert marks==[meta]
    assert read(stem)['peak_rss_bytes']<=2*(1<<30)
    return r

def setup(known,inv):
    bank=read('dyadic_precision800_d125');assert bank['full_sixteen_column_bank_refined']
    previous_plan=read('dyadic_precision6400_audit_plan_d133');configs=[]
    for col in range(2,16):
        rec=bank['state_columns'][col];assert rec['harmonic_basis_column']==col
        checked([rec['verified_state_metadata'],rec['CM_metadata'],rec['state_binary']])
        for ref in (rec['verified_state_metadata'],rec['CM_metadata'],rec['state_binary']):assert known[ref['path']]==ref['sha256']
        seed=read(Path(rec['verified_state_metadata']['path']).stem)
        assert seed['certificate']['original_full_residual_zero'] and seed['working_precision_pi']==800 and not seed.get('weighted_input',False)
        old=read(Path(rec['CM_metadata']['path']).stem);assert old['working_precision_pi']==800 and old['harmonic_basis_column']==col
        assert old['coarse_error_beta']==[1632,1648,1632,1664] and len(old['checkpoint_files'])==1
        binary=old['checkpoint_files'][0];checked([binary]);assert known[binary['path']]==binary['sha256']
        assert Path(binary['path']).stat().st_size==17*1600*8*13
        adapter_stem=f'dyadic_CM_P800_col{col:02d}_d137'
        adapter=old|{'moment_chunks':[{'first_chart':0,'last_chart':16,'file':binary}],
                     'metadata_adapter':{'milestone':'D137','original_metadata':rec['CM_metadata'],'lossless':True,'binary_copied':False}}
        save(DATA/(adapter_stem+'.json'),adapter)
        config=f'dyadic_staged_P1600_col{col:02d}_config_d137';base=f'dyadic_staged_P1600_col{col:02d}_d137'
        plan=f'dyadic_checkpoint_col{col:02d}_audit_plan_d137'
        cfg={'status':'pass','milestone':'D132','execution_milestone':'D137',
             'namespace':f'dyadic_rowjournal_P1600_col{col:02d}_d137','output_prefix':base,
             'precision_pi':1600,'seed_precision_pi':800,'column':col,
             'seed':Path(rec['verified_state_metadata']['path']).stem,'CM_reference':adapter_stem,
             'prior_review':OUT.stem,'admission_review':OUT.stem,
             'digit_bits':200,'state_chunk':1,'rhs_chunk':3,'CM_chunk':1,
             'audit_plan':plan,'CM_output':f'dyadic_CM_P1600_col{col:02d}_d137',
             'column_review':f'dyadic_checkpoint_col{col:02d}_review_d137',
             'working_store_bound_bytes':inv['maximum_bound']['total_bytes'],
             'purpose':'User-authorized P1600 full-bank checkpoint; do not continue to P3200 or P10552.'}
        save(DATA/(config+'.json'),cfg);configs.append(source(DATA/(config+'.json')))
        jobs=[]
        for previous in previous_plan['jobs']:
            label=previous['stem'].removeprefix('dyadic_precision6400_').removesuffix('_d133')
            jobs.append({'driver':'dembele/pari/564_dyadic_checkpoint_independent.py',
                         'stem':f'dyadic_checkpoint_col{col:02d}_{label}_d137',
                         'marker':'PASS|564_DYADIC_CHECKPOINT_INDEPENDENT','args':previous['args']+['--config',config]})
        save(DATA/(plan+'.json'),{'status':'pass','milestone':'D137','kind':'bounded_job_plan','config':config,
                                'requires_completed_and_sealed_actual_column':True,'maximum_workers':3,'jobs':jobs})
        prod=module('schedule_'+str(col),'run_d137_production.py')
        rev=module('review_'+str(col),'565_dyadic_checkpoint_column_review.py');rev.configure(config)
        actual=list(prod.schedule(cfg));assert actual==list(rev.expected_groups())
        assert sum(map(len,actual))==6588 and len(jobs)==24
    return configs

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args();tick=time.monotonic()
    assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
    prior=read('dyadic_target_chart_review_d136');checked(prior['sources'])
    known={r['path']:r['sha256'] for r in prior['sources']};assert len(known)==94006
    completion=read('dyadic_target_chart_completion_d136');checked(completion['review_receipts'])
    for ref in completion['review_receipts']:
        row=json.loads(Path(ref['path']).read_text());assert row['status']=='pass' and row['exit_code']==0
        checked([row['driver'],row['log'],*row['sources']])
    tests=controls();inv=inventory(1600,800);configs=setup(known,inv)
    for name in ('564_dyadic_checkpoint_independent.py','565_dyadic_checkpoint_column_review.py',
                 'run_d137_production.py','run_d137_audits.py','run_d137_bank.py'):
        source(ROOT/'dembele/pari'/name)
    # Assembly/comparison may be finalized separately; the staged bank ends
    # after its reviewed columns. This admission cannot launch another tier.
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<=2*(1<<30)
    result={'status':'pass','milestone':'D137','independent_finite_review_complete':True,
            'prior_fixed_review':source(DATA/'dyadic_target_chart_review_d136.json'),
            'all_inherited_hashes_preserved':True,'prior_hash_count':len(known),
            'P1600_checkpoint_admitted':True,'P3200_and_higher_bank_admitted':False,
            'columns_to_lift':list(range(2,16)),'already_certified_columns':{'0':6400,'1':1600},
            'production_configs':configs,'resource_inventory':inv,'controls':tests,
            'production_jobs_per_column':6588,'archive_jobs_per_column':25,'audit_jobs_per_column':24,
            'column_review_jobs_per_column':2,'total_scheduled_bounded_column_jobs':92946,
            'global_mathematical_worker_limit':3,'per_job_timeout_seconds':180,
            'per_worker_measured_RSS_limit_bytes':2*(1<<30),'conservative_concurrent_RSS_limit_bytes':6*(1<<30),
            'free_disk_floor_bytes':10*(1<<30),'incremental_column_reviews_bound_to_this_root':True,
            'actual_harmonic_precision_increased':False,'full_bank_certified_precision_pi':800,
            'bank_assembly_frame_comparison_and_final_review_required_after_columns':True,
            'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak,'sources':[source(p) for p in sorted(PATHS)]}
    now={r['path']:r['sha256'] for r in result['sources']};assert all(now[p]==v for p,v in known.items())
    if args.check:
        saved=json.loads(OUT.read_text())
        for key in result:
            if key not in ('wall_seconds','peak_rss_bytes'):assert result[key]==saved[key],key
    else:
        assert not OUT.exists();save(OUT,result)
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|566_DYADIC_CHECKPOINT_ADMISSION',flush=True)

if __name__=='__main__':main()
