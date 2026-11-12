"""Run the authorized P1600 checkpoint columns with at most three math workers.

Nonmathematical coordinator. Every arithmetic, audit and review subprocess
uses the frozen 180-second wrapper. Columns run sequentially; within each
column the reviewed coordinator uses three workers. All attempt files are
retained. A failure or partial job stops the run for inspection.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
ADMISSION='dyadic_checkpoint_admission_r2_d137'
WRAPPER='dembele/pari/run_dyadic_capped.py'
REVIEW='dembele/pari/568_dyadic_checkpoint_column_review.py'

def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while raw:=f.read(1<<20):h.update(raw)
    return {'path':str(path),'sha256':h.hexdigest()}

def read(path):
    value=json.loads(path.read_text());assert value['status']=='pass',path.name;return value

def save(path,value):
    with path.open('x') as f:f.write(json.dumps(value,indent=2)+'\n');f.flush();os.fsync(f.fileno())

def now():return datetime.now(timezone.utc).isoformat()

def verify_receipt(path,metadata,driver,args):
    row=read(path);assert row['exit_code']==0 and row['timeout_seconds']==180 and row['timeout_terminates_process_group']
    assert row['command']==['python3',str(ROOT/driver)]+args
    assert row['driver']==source(ROOT/driver) and row['log']==source(row['log']['path'])
    for ref in row['sources']:assert source(ref['path'])==ref
    marks=[json.loads(s.split('|',1)[1]) for s in Path(row['log']['path']).read_text().splitlines() if s.startswith('PHASE_METADATA|')]
    assert marks==[source(metadata)]
    return row

def review_job(config,stem,check):
    label='_recheck01' if check else '_attempt01'
    receipt=DATA/(stem+label+'.job.json');log=DATA/(stem+label+'.log');meta=DATA/(stem+'.json')
    args=['--config',config,'--output',stem]+(['--check'] if check else [])
    if not receipt.exists():
        assert not log.exists() and (check or not meta.exists()),('inspect partial review',stem,label)
        proc=subprocess.run(['python3',WRAPPER,REVIEW,stem+label,'PASS|568_DYADIC_CHECKPOINT_COLUMN_REVIEW']+args,cwd=ROOT,capture_output=True,text=True)
        if proc.returncode:print(proc.stdout+proc.stderr,flush=True);raise RuntimeError(stem+label)
    row=verify_receipt(receipt,meta,REVIEW,args)
    assert read(meta)['peak_rss_bytes']<=2*(1<<30)
    print('D137_COLUMN_REVIEW|'+json.dumps({'column_config':config,'check':check,'seconds':row['wall_seconds']}),flush=True)
    return source(receipt)

def coordinator(driver,args,out):
    if not out.exists():
        proc=subprocess.run(['python3',driver]+args,cwd=ROOT)
        assert proc.returncode==0,driver
    packet=read(out);assert packet['coordinator']==source(ROOT/driver)
    return packet

def main():
    assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
        assert os.environ.get(key)=='1',key
    out=DATA/'dyadic_checkpoint_columns_completed_r2_d137.json';assert not out.exists(),'completed bank must not be rerun'
    lock=(DATA/'dyadic_checkpoint_bank_r2_d137.lock').open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    root=DATA/(ADMISSION+'.json');admission=read(root);known={r['path']:r['sha256'] for r in admission['sources']}
    assert admission['P1600_checkpoint_admitted'] and not admission['P3200_and_higher_bank_admitted']
    for path in (Path(__file__).resolve(),ROOT/WRAPPER,ROOT/REVIEW,ROOT/'dembele/pari/run_d137_audits.py'):
        assert known[str(path)]==source(path)['sha256']
    for label,args in (('_attempt01',[]),('_recheck01',['--check'])):
        verify_receipt(DATA/(ADMISSION+label+'.job.json'),root,'dembele/pari/567_dyadic_checkpoint_admission_revision.py',args)
    start=time.monotonic();columns=[]
    for ref in admission['production_configs']:
        assert source(ref['path'])==ref;cp=Path(ref['path']);cfg=read(cp);col=cfg['column']
        assert cfg['precision_pi']==1600 and cfg['seed_precision_pi']==800 and col in range(2,16)
        completed=DATA/f'dyadic_checkpoint_col{col:02d}_completed_r2_d137.json'
        if completed.exists():
            row=read(completed);assert row['config']==ref
            for key in ('production','audits','fixed_review'):
                assert source(row[key]['path'])==row[key]
            for receipt in row['review_receipts']:assert source(receipt['path'])==receipt
            columns.append(source(completed));print('D137_REUSED_COMPLETE_COLUMN|'+str(col),flush=True);continue
        assert shutil.disk_usage(ROOT).free>=admission['free_disk_floor_bytes'],'disk reserve reached; inspect before continuing'
        print('D137_COLUMN_BEGIN|'+json.dumps({'column':col,'at':now(),'free_bytes':shutil.disk_usage(ROOT).free}),flush=True)
        actual=DATA/(cfg['output_prefix']+'_completed.json')
        production=coordinator('dembele/pari/run_d137_production_r2.py',['--config',cp.stem,'--workers','3'],actual)
        assert production['all_phases_complete'] and production['maximum_workers']==3
        audit=DATA/(cfg['audit_plan']+'_completed.json')
        audited=coordinator('dembele/pari/run_d137_audits.py',['--plan',cfg['audit_plan'],'--workers','3'],audit)
        assert audited['completed_jobs']==24 and audited['worker_limit']==3
        receipts=[review_job(cp.stem,cfg['column_review'],False),review_job(cp.stem,cfg['column_review'],True)]
        fixed=DATA/(cfg['column_review']+'.json');packet=read(fixed)
        assert packet['independent_finite_review_complete'] and packet['working_precision_pi']==1600 and packet['harmonic_basis_column']==col
        save(completed,{'status':'pass','milestone':'D137','column':col,'config':ref,
                        'production':source(actual),'audits':source(audit),'fixed_review':source(fixed),
                        'review_receipts':receipts,'completed_at':now(),'prior_admission':source(root)})
        columns.append(source(completed));print('D137_COLUMN_COMPLETE|'+json.dumps(columns[-1]),flush=True)
    assert len(columns)==14
    save(out,{'status':'pass','milestone':'D137','coordinator':source(__file__),'prior_admission':source(root),
              'all_fourteen_new_columns_independently_reviewed':True,'working_precision_pi':1600,
              'reused_columns':{'0':6400,'1':1600},'columns':columns,'maximum_mathematical_workers':3,
              'wall_seconds':time.monotonic()-start,'completed_at':now(),
              'bank_assembly_frame_comparison_and_final_review_pending':True,
              'higher_precision_bank_not_launched':True})
    print('D137_COLUMNS_COMPLETE|'+json.dumps(source(out)),flush=True)

if __name__=='__main__':main()
