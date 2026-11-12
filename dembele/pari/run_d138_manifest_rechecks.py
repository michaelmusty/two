"""Nonmathematical two-worker coordinator for D138's fifteen catalogue replays."""
from concurrent.futures import FIRST_COMPLETED,ThreadPoolExecutor,wait
import fcntl,hashlib,json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
DRIVER='dembele/pari/574_dyadic_checkpoint_manifest_recheck.py'
BASE='dyadic_precision1600_manifests_d138'

def source(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def main():
    out=DATA/(BASE+'_completed.json');assert not out.exists()
    lock=(DATA/(BASE+'.lock')).open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    start=time.monotonic()
    def job(index):
        stem=f'dyadic_precision1600_manifest{index:02d}_d138';receipt=DATA/(stem+'_attempt01.job.json');meta=DATA/(stem+'.json')
        args=['--index',str(index),'--output',stem];begin=time.monotonic()
        if not receipt.exists():
            assert not meta.exists() and not (DATA/(stem+'_attempt01.log')).exists(),('inspect partial replay',stem)
            p=subprocess.run(['python3','dembele/pari/run_dyadic_capped.py',DRIVER,stem+'_attempt01','PASS|574_DYADIC_CHECKPOINT_MANIFEST_RECHECK']+args,cwd=ROOT,capture_output=True,text=True)
            if p.returncode:print(p.stdout+p.stderr,flush=True);raise RuntimeError(stem)
        r=json.loads(receipt.read_text());assert r['status']=='pass' and r['exit_code']==0
        assert r['timeout_seconds']==180 and r['timeout_terminates_process_group']
        assert r['command']==['python3',str(ROOT/DRIVER)]+args and r['driver']==source(ROOT/DRIVER)
        assert r['log']==source(r['log']['path'])
        marks=[json.loads(x.split('|',1)[1]) for x in Path(r['log']['path']).read_text().splitlines() if x.startswith('PHASE_METADATA|')]
        assert marks==[source(meta)]
        v=json.loads(meta.read_text());assert v['index']==index and v['all_catalogue_hashes_match'] and v['peak_rss_bytes']<=2*(1<<30)
        result={'index':index,'receipt':source(receipt),'metadata':source(meta),'seconds':r['wall_seconds'],
                'peak_rss_bytes':v['peak_rss_bytes'],'coordinator_interval':[begin,time.monotonic()]}
        print('D138_MANIFEST|'+json.dumps({'index':index,'hashes':v['catalogue_sources_rehashed'],'seconds':r['wall_seconds']}),flush=True)
        return result
    rows=[None]*15
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending={};cursor=0
        try:
            while cursor<15 or pending:
                while cursor<15 and len(pending)<2:pending[pool.submit(job,cursor)]=cursor;cursor+=1
                finished,_=wait(pending,return_when=FIRST_COMPLETED)
                for future in finished:rows[pending.pop(future)]=future.result()
        except BaseException:
            for future in pending:future.cancel()
            raise
    result={'status':'pass','milestone':'D138','workers':2,'completed_jobs':15,'jobs':rows,
            'coordinator':source(__file__),'driver':source(ROOT/DRIVER),'wall_seconds':time.monotonic()-start}
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n');f.flush();os.fsync(f.fileno())
    print('D138_MANIFESTS_COMPLETE|'+json.dumps(source(out)),flush=True)

if __name__=='__main__':main()
