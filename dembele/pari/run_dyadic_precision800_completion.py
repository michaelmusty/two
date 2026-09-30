"""D125 wait for the bank, then finish capped arithmetic and independent audits.

This coordinator survives a chat transport interruption. It never changes
successful sources or artifacts. Report finalization and fixed provenance
review remain explicit subsequent steps after inspecting the results.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import threading
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
WRAPPER='dembele/pari/run_dyadic_capped.py'
STOP=threading.Event()


def source(path):
    path=Path(path).resolve();sha=hashlib.sha256()
    with path.open('rb') as file:
        while block:=file.read(1<<20):sha.update(block)
    return {'path':str(path),'sha256':sha.hexdigest()}


def job(number,name,stem,success,args=()):
    if STOP.is_set():raise RuntimeError('another completion phase failed')
    driver=f'dembele/pari/{number}_{name}.py'
    receipt=DATA/(stem+'_attempt01.job.json');log=DATA/(stem+'_attempt01.log')
    out=DATA/(stem+'.json')
    cmd=['python3',WRAPPER,driver,stem+'_attempt01',success,*args]
    resumed=receipt.exists()
    if not resumed:
        assert not log.exists() and not out.exists(),('inspect partial output',stem)
        completed=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        if completed.returncode:
            STOP.set();print(completed.stdout+completed.stderr,flush=True);raise RuntimeError(stem)
    row=json.loads(receipt.read_text())
    assert row['status']=='pass' and row['exit_code']==0
    assert row['timeout_seconds']==180 and row['timeout_terminates_process_group']
    assert row['command']==['python3',str(ROOT/driver)]+list(args)
    assert source(row['driver']['path'])==row['driver'] and source(row['log']['path'])==row['log']
    packet=json.loads(out.read_text());assert packet['status']=='pass'
    for file in packet.get('checkpoint_files',[]):assert source(file['path'])==file
    print('P800_COMPLETION_PHASE|'+json.dumps({'stem':stem,'seconds':row['wall_seconds'],'resumed':resumed}),flush=True)
    return receipt


def main():
    start=time.monotonic();own=source(__file__)
    summary=DATA/'dyadic_precision800_completion_d125.json';assert not summary.exists()
    # The last CM receipt is written after the last mathematical worker exits.
    # Inspect failures while waiting; never race the active bank coordinator.
    while True:
        for path in DATA.glob('*d125*.job.json'):
            row=json.loads(path.read_text())
            assert row['status']=='pass',('existing failed receipt',path.name)
        ready=True
        for col in range(1,16):
            paths=[DATA/f'dyadic_weighted_column_P800_col{col:02d}_d125.json',
                   DATA/f'dyadic_direct_CM_P800_col{col:02d}_d125_attempt01.job.json']
            ready=ready and all(path.exists() for path in paths)
        if ready:break
        time.sleep(5)
    jobs=[]
    jobs.append(job(507,'dyadic_complete_precision800_bank','dyadic_precision800_d125','PASS|507_DYADIC_COMPLETE_PRECISION800_BANK'))
    jobs.append(job(509,'dyadic_precision800_residue_frame','dyadic_residue_frame800_d125','PASS|509_DYADIC_PRECISION800_RESIDUE_FRAME'))
    jobs.append(job(510,'dyadic_precision800_quadrics','dyadic_integral_quadrics800_d125','PASS|510_DYADIC_PRECISION800_QUADRICS'))
    tasks=[(511,'dyadic_precision800_column_audit',f'dyadic_precision800_audit_col{col:02d}_d125',
            'PASS|511_DYADIC_PRECISION800_COLUMN_AUDIT',('--column',str(col))) for col in range(1,16)]
    tasks.append((512,'dyadic_precision800_comparison_audit','dyadic_precision800_audit_comparison_d125',
                  'PASS|512_DYADIC_PRECISION800_COMPARISON_AUDIT',()))
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(job,*task) for task in tasks]
        try:
            for future in as_completed(futures):jobs.append(future.result())
        except BaseException:
            STOP.set()
            for future in futures:future.cancel()
            raise
    audit=DATA/'dyadic_precision800_audit_comparison_d125.json'
    result=json.loads(audit.read_text());assert source(__file__)==own
    summary.write_text(json.dumps({'status':'pass','milestone':'D125','arithmetic_and_audits_complete':True,
        'final_report_and_fixed_provenance_review_pending':True,'new_completion_jobs':len(jobs),
        'coordinator_wall_seconds_including_wait_for_bank':time.monotonic()-start,
        'comparison_certificates':result['certificates'],
        'sources':[source(p) for p in [Path(__file__),ROOT/WRAPPER,audit,*jobs]]},indent=2)+'\n')
    print('P800_COMPARISON_ARITHMETIC_COMPLETE|'+json.dumps(result['certificates']),flush=True)


if __name__=='__main__':main()
