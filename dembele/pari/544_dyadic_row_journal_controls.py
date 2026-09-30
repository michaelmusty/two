"""D131 process-interruption, corruption, actual-transition and capacity controls.

All mutations are confined to new prospectively temporary owned stores.
Small/target synthetic byte controls test storage, not harmonic arithmetic.
Actual mode replays one frozen D124 transition and does not recompute its
low solve or original operator. Completed stores are sealed and retained.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('journal',ROOT/'dembele/pari/543_dyadic_row_journal.py')
j=importlib.util.module_from_spec(s);s.loader.exec_module(j)
PATHS={Path(__file__),Path(j.__file__)};CACHE={}


def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:
        sha=hashlib.sha256()
        with path.open('rb') as f:
            while raw:=f.read(1<<20):sha.update(raw)
        CACHE[path]={'path':str(path),'sha256':sha.hexdigest()}
    return CACHE[path]


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);p=json.loads(path.read_text());assert p['status']=='pass';return p


def raw(c,kind,e):
    width=c['state_width'] if kind in ('state','new_state') else c['next_width'] if kind=='next_aux' else c['aux_width']
    if c['kind']=='actual':
        rec=c['files'][kind]
        with Path(rec['path']).open('rb') as f:f.seek(e*width);value=f.read(width)
        assert len(value)==width
        return value
    return hashlib.shake_256(f"D131-storage-{kind}-{e}".encode()).digest(width)


def initialize(store,c):
    store.initialize(c['rows'],c['state_width'],c['aux_width'],
                     (raw(c,'state',e) for e in range(c['rows'])),
                     (raw(c,'aux',e) for e in range(c['rows'])),{'control':c['kind']})


def child(store,task,fault,row=0):
    cmd=['python3',str(Path(__file__).resolve()),'--worker',task,'--namespace',store.path.name,'--fault',fault,'--row',str(row)]
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==73,(cmd,r.returncode,r.stdout,r.stderr)
    # No new process group: the wrapper's 180-second group cap also covers
    # this deliberately interrupted child. Parent waits for it to exit.
    return {'task':task,'fault':fault,'row':row,'exit_code':r.returncode,
            'child_inherits_capped_process_group':True}


def worker(args):
    store=j.Store(DATA/args.namespace,fault=args.fault);c=store._get('CONTROL.json')
    if args.worker=='initialize':initialize(store,c)
    elif args.worker=='begin_prepare':store.begin_prepare('prepared',{'control':c['kind']})
    elif args.worker=='prepare_row':store.prepare_row(args.row,raw(c,'new_state',args.row),raw(c,'new_aux',args.row))
    elif args.worker=='finish_prepare':store.finish_prepare()
    elif args.worker=='begin_sweep':store.begin_sweep('finished',c['next_width'],{'control':c['kind']})
    elif args.worker=='sweep_row':store.sweep_row(args.row,raw(c,'next_aux',args.row))
    elif args.worker=='finish_sweep':store.finish_sweep()
    else:raise AssertionError(args.worker)
    raise AssertionError('requested interruption was not reached')


def must_reject(fn):
    try:fn()
    except (AssertionError,FileNotFoundError):return 1
    raise AssertionError('invalid operation accepted')


def check_finished(store,c):
    v=store.current();assert v['tag']=='finished' and v['phase']=='ready'
    checks=0
    for e in range(c['rows']):
        assert store.read_row('state',e,'finished')==raw(c,'new_state',e)
        assert store.read_row('aux',e,'finished')==raw(c,'next_aux',e)
        checks+=c['state_width']+c['next_width']
    assert not store._file('aux_initial.bin').exists()
    return checks


def replay(name,c,interruption=None,actual_math=False):
    store=j.Store(DATA/name,create=True);store._put('CONTROL.json',c)
    events=[];blocked=0
    def inject(task):
        nonlocal blocked
        if interruption and interruption[0]==task:
            events.append(child(store,task,interruption[1],interruption[2] if len(interruption)>2 else 0))
            if store._file('TXN.json').exists():blocked+=must_reject(store.current)
            store.recover();return True
        return False
    if not inject('initialize'):initialize(store,c)
    elif not store._file('CURRENT.json').exists():initialize(store,c)
    if not inject('begin_prepare'):store.begin_prepare('prepared',{'control':c['kind']})
    blocked+=must_reject(lambda:store.read_row('state',0,'initial'))
    scalar_checks=0
    for e in range(c['rows']):
        if actual_math:
            old=raw(c,'state',e);new=raw(c,'new_state',e);delta=raw(c,'new_aux',e)
            assert delta[:8*13]==bytes(8*13)
            assert delta[33*8*13:]==raw(c,'aux',e)[33*8*13:]
            pos=0;rebuilt=bytearray()
            for k in range(1600):
                for i in range(8):
                    bits=200 if k<=32 else max(0,(1600-k-i+7)//8);width=(bits+7)//8
                    v=int.from_bytes(old[pos:pos+width],'little');pos+=width
                    if k<800:
                        offset=(k*8+i)*13;dv=int.from_bytes(delta[offset:offset+13],'little');assert dv<1<<100;v+=dv<<100
                    rebuilt.extend((v % (1<<bits)).to_bytes(width,'little'));scalar_checks+=1
            assert bytes(rebuilt)==new and pos==len(old)
        if interruption and interruption[0]=='prepare_row' and e==(interruption[2] if len(interruption)>2 else 0):inject('prepare_row')
        t=store._get('TXN.json')
        if t['next_row']==e:store.prepare_row(e,raw(c,'new_state',e),raw(c,'new_aux',e))
        else:assert t['next_row']==e+1
    if not inject('finish_prepare'):store.finish_prepare()
    if store._file('TXN.json').exists():store.finish_prepare()
    assert store.current()['phase']=='prepared'
    blocked+=must_reject(lambda:store.read_row('state',0,'initial'))
    if not inject('begin_sweep'):store.begin_sweep('finished',c['next_width'],{'control':c['kind']})
    assert store.read_row('aux',0,'prepared',operator=True)==raw(c,'new_aux',0)
    for e in range(c['rows']):
        if interruption and interruption[0]=='sweep_row' and e==(interruption[2] if len(interruption)>2 else 0):inject('sweep_row')
        store.sweep_row(e,raw(c,'next_aux',e))
    store.sweep_row(0,raw(c,'next_aux',0)) # Identical retry is accepted.
    bad=bytearray(raw(c,'next_aux',0));bad[0]^=1
    blocked+=must_reject(lambda:store.sweep_row(0,bytes(bad)))
    if not inject('finish_sweep'):store.finish_sweep()
    if store._file('TXN.json').exists():store.finish_sweep()
    checks=check_finished(store,c)
    peak=store.peak;store.seal()
    blocked+=must_reject(lambda:store.begin_prepare('forbidden',{}))
    PATHS.update(store.path.iterdir())
    return {'namespace':name,'kind':c['kind'],'rows':c['rows'],'interruptions':events,
            'rejected_mixed_stale_wrong_retry_or_sealed_operations':blocked,
            'final_direct_byte_comparisons':checks,'actual_weighted_addition_scalar_checks':scalar_checks,
            'maximum_observed_logical_bytes_in_parent':peak,'sealed':True}


def corruptions():
    name='dyadic_rowjournal_corruption_d131';c={'kind':'synthetic','rows':3,'state_width':41,'aux_width':17,'next_width':13}
    store=j.Store(DATA/name,create=True);store._put('CONTROL.json',c);initialize(store,c)
    old=store.read_row('state',0,'initial');bad=bytearray(old);bad[0]^=1
    store._writeat('state.bin',0,bad)
    rejections=must_reject(lambda:store.read_row('state',0,'initial'))
    store._writeat('state.bin',0,old);store.begin_prepare('prepared',{})
    event=child(store,'prepare_row','wal_committed')
    before=store._file('state.bin').read_bytes()+store._file('aux_initial.bin').read_bytes()
    wal=store._get('WAL.json');blob=store._file('wal_after_state.bin');good=blob.read_bytes();bad=bytearray(good);bad[-1]^=1
    store._writeat(blob.name,0,bad);rejections+=must_reject(store.recover)
    assert store._file('state.bin').read_bytes()+store._file('aux_initial.bin').read_bytes()==before
    store._writeat(blob.name,0,good)
    txn=store._file('TXN.json');original=txn.read_bytes();altered=json.loads(original);altered['value']['next_row']=2
    txn.write_bytes(j.canonical(altered));rejections+=must_reject(store.recover);txn.write_bytes(original)
    store._put('WAL.json',{**wal,'target':'stale_epoch'});rejections+=must_reject(store.recover);store._put('WAL.json',wal)
    store.recover();store.recover();assert store._get('TXN.json')['next_row']==1
    for e in (1,2):store.prepare_row(e,raw(c,'new_state',e),raw(c,'new_aux',e))
    store.finish_prepare();store.begin_sweep('finished',13,{})
    for e in range(3):store.sweep_row(e,raw(c,'next_aux',e))
    store.finish_sweep();checks=check_finished(store,c);store.seal();PATHS.update(store.path.iterdir())
    return {'namespace':name,'corruption_or_stale_WAL_rejections':rejections,'bad_WAL_rejected_before_payload_write':True,
            'repeated_recovery_idempotent':True,'final_direct_byte_comparisons':checks,'interruption':event}


def small():
    c={'kind':'synthetic','rows':3,'state_width':41,'aux_width':17,'next_width':13}
    cases=[('initialize','initial_state_written'),('begin_prepare','prepare_intent')]
    cases += [('prepare_row',x) for x in ('wal_blobs_uncommitted','wal_committed','state_half','state_written','aux_half','aux_written','progress_committed','wal_unlinked')]
    cases += [('finish_prepare','prepare_generation_committed'),('begin_sweep','sweep_intent')]
    cases += [('sweep_row',x) for x in ('sweep_half','sweep_row_written','sweep_progress_committed')]
    cases += [('finish_sweep',x) for x in ('retirement_intent','sweep_generation_committed','sweep_intent_removed','retired_file_unlinked')]
    return {'controls':[replay(f'dyadic_rowjournal_small_{i:02d}_d131',c,case) for i,case in enumerate(cases)],
            'corruptions':corruptions(),'power_loss_or_hardware_fault_testing_claimed':False}


def actual():
    prior=read('dyadic_target_feasibility_review_d130');known={x['path']:x['sha256'] for x in prior['sources']}
    packets=[read('dyadic_weighted_P1600_col00_'+x+'_d124') for x in ('seed','step01_prepared','step01')]
    old,prep,new=packets
    files={'state':old['state_file'],'aux':old['residual_file'],'new_state':prep['state_file'],
           'new_aux':prep['operator_input_file'],'next_aux':new['residual_file']}
    for rec in files.values():assert known[rec['path']]==rec['sha256'] and source(rec['path'])==rec
    sw=Path(files['state']['path']).stat().st_size//174
    c={'kind':'actual','rows':174,'state_width':sw,'aux_width':800*8*13,'next_width':767*8*12,'files':files}
    # 200-floor(833/8)=96 bits, hence 12 bytes in the new residual.
    assert Path(files['next_aux']['path']).stat().st_size==174*c['next_width']
    result=replay('dyadic_rowjournal_actual_d131',c,('prepare_row','state_half',83),actual_math=True)
    result['original_low_solve_and_operator_recomputed']=False
    result['all_original_reference_payloads_preserved']=True
    return result


def target():
    c={'kind':'synthetic_target_width','rows':2,'state_width':6996660,'aux_width':2159040,'next_width':2141880}
    result=replay('dyadic_rowjournal_target_d131',c,('prepare_row','aux_half',1))
    result['full_target_bank_or_arithmetic_computed']=False
    return result


def inventory():
    rows=174;P=10552;seed=6400
    weighted=sum((max(0,(P-k-i+7)//8) if k>32 else P//8)+7>>3 for k in range(P) for i in range(8))
    residual=(P-seed)*8*((P//8-seed//8+7)//8)
    assert weighted==6996660 and residual==2159040
    stages={'prepare':rows*(weighted+residual)+2*(weighted+residual)+j.RESERVE,
            'sweep':rows*(weighted+2*residual)+j.RESERVE,
            'initialize':rows*(weighted+residual)+j.RESERVE,
            'final_weighted_plus_CM':rows*weighted+17*2*P*8*165+j.RESERVE}
    assert stages['sweep']==2035873624<j.CAP
    store=j.Store(DATA/'dyadic_rowjournal_capacity_d131',create=True)
    with store.guard():
        for name,size in [('capacity_state.bin',rows*weighted),('capacity_input.bin',rows*residual),('capacity_output.bin',rows*residual)]:store._reserve(name,size)
        occupied=store.occupied();rejected=must_reject(lambda:store._reserve('rejected.bin',j.CAP-occupied+1))
        assert not store._file('rejected.bin').exists()
        for name in ('capacity_state.bin','capacity_input.bin','capacity_output.bin'):store._remove(name)
    c={'kind':'synthetic','rows':1,'state_width':1,'aux_width':1,'next_width':1};initialize(store,c);store.seal();PATHS.update(store.path.iterdir())
    return {'staged_target_from_P6400':True,'capacity_bytes':j.CAP,'reserved_workspace_bytes':j.RESERVE,
            'prospective_layout_bytes_excluding_metadata':stages,'largest_reserved_occupancy_with_metadata':occupied,
            'oversized_reservation_rejections':rejected,'rejected_file_not_created':True,
            'large_capacity_files_logically_reserved_but_not_filled_with_target_data':True,
            'low_factor_integration_and_all_stage_lifetimes_verified':False,
            'full_target_refinement_or_concurrent_RAM_certificate':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase',choices=('small','actual','target','inventory'))
    ap.add_argument('--output');ap.add_argument('--worker');ap.add_argument('--namespace');ap.add_argument('--fault');ap.add_argument('--row',type=int,default=0)
    args=ap.parse_args()
    if args.worker:worker(args);raise SystemExit
    out=DATA/(args.output+'.json');assert not out.exists();tick=time.monotonic()
    cert={'small':small,'actual':actual,'target':target,'inventory':inventory}[args.phase]()
    packet={'status':'pass','milestone':'D131','phase':args.phase,'certificates':cert,
            'actual_harmonic_precision_increased':False,'wall_seconds':time.monotonic()-tick,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            'maximum_child_process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            'sources':[source(x) for x in sorted(PATHS)]}
    out.write_text(json.dumps(packet,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print(json.dumps({'phase':args.phase,'wall_seconds':packet['wall_seconds']}),flush=True)
    print('PASS|544_DYADIC_ROW_JOURNAL_CONTROLS',flush=True)
