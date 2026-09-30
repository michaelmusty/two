"""D132 target low-solve integration and full staged live-file accounting.

The 1319-bit RHS is synthetic and matches D130's frozen complete reference.
These controls do not create a higher-precision harmonic column.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module('driver','548_dyadic_resumable_staged_driver.py');j=m.j;b=m.b
CONFIG='dyadic_staged_low1319_config_d132'
def source(path):return m.source(path)
def setup():
    eng=m.Engine(CONFIG);st=j.Store(eng.path,create=True);eng.store=st
    st._put('CONFIG.json',{'config':source(eng.config_path),'driver':source(Path(m.__file__))})
    prior=m.read('dyadic_weighted_journal_review_d131');known={x['path']:x['sha256'] for x in prior['sources']}
    transport=source(DATA/'dyadic_target_transports_d121.json');assert known[transport['path']]==transport['sha256']
    st._put('INPUTS.json',{'transport':transport,'synthetic_low_control_only':True})
    st.initialize(174,1,1,[b'\0']*174,[b'\0']*174,{'synthetic_low_control_only':True})
    bits=1319;digits=[200,400,600,800,1000,1200,1319]
    st._put('low_000.json',{'step':0,'seed':True,'base':st.current(),'u':0,'shift':0,'bits':bits,'count':10552,'digits':digits})
    rhs=[b.k.data(32,1,bits,f'D130-low-rhs-state{e}') for e in range(174)]
    info=eng.write_low('rhs000',rhs,bits,{'synthetic_matches_D130':True})
    return {'synthetic_RHS_bits':bits,'digits':digits,'RHS_sha256':info['sha256'],'actual_precision_increased':False}
def finish():
    eng=m.Engine(CONFIG);st=eng.open();valid=st._get('valid000_06.json');assert valid['bits']==1319
    info=st.pool('answer000_06',True)
    prior=m.read('dyadic_target_low_c01_bits1319_d130_solve')['certificates']['answer']
    assert source(prior['path'])==prior and info['sha256']==prior['sha256']
    assert info['bytes']==174*32*8*165
    # The complete answer is retained; all obsolete quotient/answer slots were retired.
    assert {p.name for p in st.path.glob('*.bin')}=={'state.bin','aux_initial.bin','WORKSPACE.bin','rhs000.bin','answer000_06.bin'}
    st.seal()
    return {'complete_original_low_equation_scalars':44544,'final_bits':1319,'all_answer_bytes_match_D130':info['bytes'],
            'answer_sha256':info['sha256'],'new_factor_constructed':False,'actual_precision_increased':False,
            'sealed_namespace':str(st.path)}
def archive_fault():
    stem='dyadic_staged_low1319_d132_archive_low_verify_000_00'
    driver=ROOT/'dembele/pari/551_dyadic_staged_metadata_archive.py'
    child=subprocess.run(['python3',str(driver),'--config',CONFIG,'--label','low_verify_000_00',
                          '--output',stem,'--fault','archive_record_removed'],cwd=ROOT,capture_output=True,text=True)
    assert child.returncode==73,(child.returncode,child.stdout,child.stderr)
    assert not (DATA/(stem+'.json')).exists()
    store=DATA/'dyadic_rowjournal_low1319_d132'
    intent=json.loads((store/'archive_low_verify_000_00.json').read_text())['value']
    assert len(intent['items'])==3
    assert sum((store/x['name']).exists() for x in intent['items'])==2
    for item in intent['items']:assert source(item['external_metadata']['path'])==item['external_metadata']
    return {'intentional_child_exit':73,'archived_records':3,'records_removed_before_interruption':1,
            'all_external_copies_unchanged':True,'child_inherits_capped_process_group':True}
def inventory(P,S):
    assert P%8==S%8==0 and 400<=S<P<=10552
    N,R,K=174,32,P//8;reserve=64*(1<<20);cap=2*(1<<30)
    Wrow=sum((n+7)//8 for bs in m.v.layout(P,K,True) for n in bs);W=N*Wrow
    def residual(u):return N*max(33,P-u)*8*((K-u//8+7)//8)
    def low(bits):return N*R*8*((bits+7)//8)
    # Exact payload lengths; conservative metadata ceilings include atomic
    # replacements, archive intents and retained historical manifests.
    metadata=8*(1<<20);records=[];permanent=0
    def add(phase,step,payload,meta):
        records.append({'phase':phase,'step':step,'payload_and_reserve_bytes':payload+reserve,
                        'metadata_bound_bytes':meta,'total_bytes':payload+reserve+meta})
    add('initial_row_pool',0,W+N,metadata+N*8192)
    step=0
    while True:
        seed=step==0;u=0 if seed else S+33*(step-1);bits=K-u//8;oldR=N if seed else residual(u)
        digits=list(range(min(bits,200),bits,200))+[bits]
        # A worst-case one-state task schedule. Completed duplicate job records
        # are archived after each sweep; external metadata/receipts remain retained.
        jobs=2*N+6+5+3*len(digits)+(N if seed else 0)
        transient_records=(jobs+8)*8192
        pool_history=(2*len(digits)+1)*16384
        context_history=6*65536
        archive_intent=512*(1<<10)
        live_meta=metadata+transient_records+pool_history+context_history+archive_intent
        oldbits=0
        for new in digits:
            add('low_residual_solve_verify',step,W+oldR+low(bits)+low(oldbits)+low(new-oldbits)+low(new),live_meta)
            oldbits=new
        add('journal_prepare',step,W+oldR+low(bits)*2+2*Wrow+2*(oldR//N),live_meta)
        after=S if seed else min(P,u+33);newR=residual(after)
        add('operator_sweep',step,W+oldR+newR,live_meta)
        # A completed barrier preserves compact archive receipts and the full
        # low/history manifests, while retiring only duplicate done records.
        metadata+=pool_history+context_history+archive_intent
        permanent+=jobs*(16384+4096) # External JSON and receipt/log allowance; not scratch.
        if max(33,P-after)==33:break
        step+=1
    cm=17*2*P*8*((K+7)//8)
    final_meta=metadata+(N+17+68+10)*8192+2*65536
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
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--phase',choices=('setup','finish','inventory','archive-fault'),required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args();out=DATA/(a.output+'.json');assert not out.exists();tick=time.monotonic()
    cert=setup() if a.phase=='setup' else finish() if a.phase=='finish' else archive_fault() if a.phase=='archive-fault' else {'schedules':[inventory(800,400),inventory(6400,3200),inventory(10552,6400)]}
    packet={'status':'pass','milestone':'D132','phase':a.phase,'certificates':cert,'wall_seconds':time.monotonic()-tick,
            'actual_harmonic_precision_increased':False,'sources':[source(Path(__file__)),source(Path(m.__file__)),source(Path(j.__file__)),source(DATA/(CONFIG+'.json'))]}
    out.write_text(json.dumps(packet,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|552_DYADIC_STAGED_TARGET_CONTROLS',flush=True)
