"""D132 phase schedule with duplicate-metadata retirement at arithmetic barriers.

Up to three wrapper jobs run at once. Completed receipts are immutable;
failed attempts and logs are preserved and a new numbered attempt resumes
the same durable phase. Unexpected failures stop admission of new work.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
DRIVER='dembele/pari/554_dyadic_resumable_staged_production.py'
WRAPPER='dembele/pari/run_dyadic_capped.py'
def source(path):
    p=Path(path).resolve();h=hashlib.sha256()
    with p.open('rb') as f:
        while raw:=f.read(1<<20):h.update(raw)
    return {'path':str(p),'sha256':h.hexdigest()}
def save(path,value):
    with path.open('x') as f:f.write(json.dumps(value,indent=2)+'\n');f.flush();os.fsync(f.fileno())
def schedule(cfg):
    P,S=cfg['precision_pi'],cfg['seed_precision_pi']
    if cfg.get('low_only_control'):
        bits=P//8
        digits=list(range(min(bits,cfg['digit_bits']),bits,cfg['digit_bits']))+[bits]
        for digit,_ in enumerate(digits):
            for phase in ('low-residual','low-solve','low-verify'):
                yield [{'phase':phase,'key':f"{phase.replace('-','_')}_000_{digit:02d}",'step':0,'digit':digit}]
        return
    chunk=cfg['state_chunk'];rhs_chunk=cfg['rhs_chunk']
    assert 1<=chunk<=29 and 1<=rhs_chunk<=29
    def one(phase,key,**kw):return [{'phase':phase,'key':key}|kw]
    def rows(phase,prefix,count=174,size=chunk,**kw):
        return [{'phase':phase,'key':f'{prefix}_e{i:03d}_{min(count-1,i+size-1):03d}',
                 'first':i,'last':min(count-1,i+size-1)}|kw for i in range(0,count,size)]
    yield one('create','create');yield rows('extend','extend');yield one('init-finish','init_finish')
    u=S;steps=0
    while True:
        step=steps;bits=P//8 if step==0 else P//8-(S+33*(step-1))//8
        yield one('low-begin',f'low_begin_{step:03d}',step=step)
        yield rows('rhs',f'rhs{step:03d}',size=rhs_chunk,step=step)
        digits=list(range(min(bits,cfg['digit_bits']),bits,cfg['digit_bits']))+[bits]
        for digit,_ in enumerate(digits):
            for phase in ('low-residual','low-solve','low-verify'):
                yield one(phase,f"{phase.replace('-','_')}_{step:03d}_{digit:02d}",step=step,digit=digit)
        yield one('prepare-begin',f'prepare_begin_{step:03d}',step=step)
        # The in-place preparation journal has a monotone row cursor.
        for item in rows('prepare-rows',f'prepare{step:03d}',size=29,step=step):yield [item]
        yield one('prepare-finish',f'prepare_finish_{step:03d}',step=step)
        yield one('sweep-begin',f'sweep_begin_{step:03d}',step=step)
        yield rows('operator',f'operator{step:03d}',step=step)
        yield one('sweep-finish',f'sweep_finish_{step:03d}',step=step)
        u=S+33*step
        if max(33,P-u)==33:break
        steps+=1
    yield one('verify-begin','verify_begin');yield rows('verify','verify')
    yield one('cm-begin','cm_begin');yield rows('cm','cm',count=17,size=cfg['CM_chunk'])
    yield [{'phase':'coarse','key':f'coarse_c{ci:02d}_o{order}','chart':ci,'order':order} for ci in range(17) for order in range(4)]
    yield one('seal','seal')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--config',required=True)
    ap.add_argument('--workers',type=int,default=3);ap.add_argument('--stop-before');ap.add_argument('--fault-controls',action='store_true')
    a=ap.parse_args();assert 1<=a.workers<=3
    assert not a.fault_controls,'fault controls are the reviewed source-549 path'
    global DRIVER
    archives=[]
    cp=DATA/(a.config+'.json');cfg=json.loads(cp.read_text());base=cfg['output_prefix']
    if cfg.get('low_only_control'):DRIVER='dembele/pari/548_dyadic_resumable_staged_driver.py'
    out=DATA/(base+'_completed.json');assert not out.exists(),'completed coordinator must not be rerun'
    with (DATA/(base+'.lock')).open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        started=time.monotonic();results=[];faults=[]
        planned={
          'extend_e000_028':'pool_progress_committed',
          'rhs000_e000_028':'job_committed',
          'low_solve_000_00':'pool_row_written',
          'prepare001_e000_028':'state_written',
          'operator001_e000_028':'sweep_row_written',
          'coarse_c00_o0':'job_committed',
          'seal':'job_committed'} if a.fault_controls else {}
        def checked(receipt,output,command,driver):
            d=json.loads(receipt.read_text());assert d['status']=='pass' and d['exit_code']==0
            assert d['command']==command and d['timeout_seconds']==180 and d['timeout_terminates_process_group']
            assert source(d['driver']['path'])==d['driver'] and d['driver']['path']==str(ROOT/driver)
            assert source(d['log']['path'])==d['log']
            lines=Path(d['log']['path']).read_text().splitlines()
            assert [json.loads(x.split('|',1)[1]) for x in lines if x.startswith('PHASE_METADATA|')]==[source(output)]
            return d
        def job(spec):
            key=spec['key'];stem=base+'_'+key;output=DATA/(stem+'.json')
            extra=['--config',a.config,'--output',stem]
            for k,val in spec.items():extra+=['--'+k.replace('_','-'),str(val)]
            passed=[];prior=[]
            for receipt in sorted(DATA.glob(stem+'_attempt[0-9][0-9].job.json')):
                d=json.loads(receipt.read_text());prior.append(receipt)
                if d['status']=='pass':passed.append(receipt)
            assert len(passed)<=1
            if key in planned:
                fs=stem+'_interrupt';fr=DATA/(fs+'_attempt01.job.json');fo=DATA/(fs+'.json')
                fdriver='dembele/pari/550_dyadic_staged_interrupt_control.py'
                fextra=['--config',a.config,'--spec',json.dumps(spec,separators=(',',':')),'--fault',planned[key],'--output',fs]
                if not fr.exists():
                    assert not passed and not fo.exists()
                    done=subprocess.run(['python3',WRAPPER,fdriver,fs+'_attempt01','PASS|550_DYADIC_STAGED_INTERRUPT_CONTROL']+fextra,cwd=ROOT,capture_output=True,text=True)
                    if done.returncode:print(done.stdout+done.stderr,flush=True);raise RuntimeError(fs)
                checked(fr,fo,['python3',str(ROOT/fdriver)]+fextra,fdriver);faults.append(source(fr))
            begin=time.monotonic()
            if passed:receipt=passed[0]
            else:
                # Logs without receipts are retained as interrupted attempts.
                index=1
                while (DATA/(stem+f'_attempt{index:02d}.job.json')).exists() or (DATA/(stem+f'_attempt{index:02d}.log')).exists():index+=1
                assert index<100;attempt=stem+f'_attempt{index:02d}';receipt=DATA/(attempt+'.job.json')
                done=subprocess.run(['python3',WRAPPER,DRIVER,attempt,('PASS|548_DYADIC_RESUMABLE_STAGED_DRIVER' if cfg.get('low_only_control') else 'PASS|554_DYADIC_RESUMABLE_STAGED_PRODUCTION')]+extra,cwd=ROOT,capture_output=True,text=True)
                if done.returncode:print(done.stdout+done.stderr,flush=True);raise RuntimeError(stem)
            d=checked(receipt,output,['python3',str(ROOT/DRIVER)]+extra,DRIVER)
            packet=json.loads(output.read_text());assert packet['request']['key']==key and packet['status']=='pass'
            rss=packet['peak_rss_bytes'];assert rss<=2*(1<<30)
            result={'key':key,'receipt':source(receipt),'metadata':source(output),'seconds':d['wall_seconds'],
                    'peak_rss_bytes':rss,'reused_receipt':bool(passed),'coordinator_interval':[begin,time.monotonic()]}
            print('D132_JOB|'+json.dumps({'key':key,'seconds':d['wall_seconds'],'reused':bool(passed),'peak_rss_bytes':rss}),flush=True)
            return result
        for group in schedule(cfg):
            if a.stop_before and any(x['key']==a.stop_before for x in group):
                print('D132_PLANNED_PAUSE|'+a.stop_before,flush=True);return
            with ThreadPoolExecutor(max_workers=min(a.workers,len(group))) as pool:rows=list(pool.map(job,group))
            results.extend(rows)
            if len(group)==1 and group[0]['phase'] in ('sweep-finish','low-verify') and (group[0]['phase']=='sweep-finish' or cfg.get('low_only_control')):
                label=group[0]['key'];stem=base+'_archive_'+label
                receipt=DATA/(stem+'_attempt01.job.json');meta=DATA/(stem+'.json')
                archive_driver='dembele/pari/551_dyadic_staged_metadata_archive.py'
                args=['--config',a.config,'--label',label,'--output',stem]
                if not receipt.exists():
                    if cfg.get('low_only_control') and label=='low_verify_000_00':
                        fault_stem='dyadic_staged_archive_interruption_d132'
                        fault_driver='dembele/pari/552_dyadic_staged_target_controls.py'
                        fault_args=['--phase','archive-fault','--output',fault_stem]
                        fault_receipt=DATA/(fault_stem+'_attempt01.job.json')
                        if not fault_receipt.exists():
                            test=subprocess.run(['python3',WRAPPER,fault_driver,fault_stem+'_attempt01','PASS|552_DYADIC_STAGED_TARGET_CONTROLS']+fault_args,cwd=ROOT,capture_output=True,text=True)
                            if test.returncode:print(test.stdout+test.stderr,flush=True);raise RuntimeError(fault_stem)
                        checked(fault_receipt,DATA/(fault_stem+'.json'),['python3',str(ROOT/fault_driver)]+fault_args,fault_driver)
                    done=subprocess.run(['python3',WRAPPER,archive_driver,stem+'_attempt01','PASS|551_DYADIC_STAGED_METADATA_ARCHIVE']+args,cwd=ROOT,capture_output=True,text=True)
                    if done.returncode:print(done.stdout+done.stderr,flush=True);raise RuntimeError(stem)
                checked(receipt,meta,['python3',str(ROOT/archive_driver)]+args,archive_driver)
                archives.append({'receipt':source(receipt),'metadata':source(meta)})
            # Sum individual measured peaks, conservatively ignoring their exact overlap.
            bound=sum(sorted((r['peak_rss_bytes'] for r in rows),reverse=True)[:a.workers])
            assert bound<=6*(1<<30)
        result={'status':'pass','milestone':'D132','config':source(cp),'coordinator':source(Path(__file__)),
                'jobs':results,'completed_jobs':len(results),'metadata_archives':archives,'interruption_controls':faults,'maximum_workers':a.workers,
                'wall_seconds':time.monotonic()-started,'all_phases_complete':True,
                'RAM_admission':{'per_job_measured_peak_bytes':2*(1<<30),'three_worker_sum_bytes':6*(1<<30),
                                 'OS_hard_RAM_limit_claimed':False,'process_table_monitoring_available':False},
                'sum_recorded_job_seconds':sum(x['seconds'] for x in results),
                'max_single_job_seconds':max(x['seconds'] for x in results),'max_single_job_peak_rss_bytes':max(x['peak_rss_bytes'] for x in results)}
        save(out,result);print('D132_COMPLETE|'+json.dumps(source(out)),flush=True)

if __name__=='__main__':main()
