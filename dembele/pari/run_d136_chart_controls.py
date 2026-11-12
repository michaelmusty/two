"""Run the finite 17-chart D136 control plan within the global three-worker limit.

Only nonmathematical orchestration runs here. Every child has its own existing
180-second process-group wrapper. Failed/partial attempts require diagnosis.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
DRIVER = 'dembele/pari/562_dyadic_target_chart_control.py'
BASE = 'dyadic_target_chart_controls_d136'


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path':str(path),'sha256':h.hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workers',type=int,default=3)
    args = ap.parse_args()
    assert 1 <= args.workers <= 3
    out = DATA/(BASE+'_completed.json')
    assert not out.exists(), 'Completed plan must not be rerun'
    tick = time.monotonic()
    driver = source(ROOT/DRIVER)
    with (DATA/(BASE+'.lock')).open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        def job(chart):
            stem = f'dyadic_target_chart_c{chart:02d}_d136'
            rp = DATA/(stem+'_attempt01.job.json')
            mp = DATA/(stem+'.json')
            command = ['python3',str(ROOT/DRIVER),'--chart',str(chart),'--output',stem]
            reused = rp.exists()
            if not reused:
                assert not mp.exists() and not (DATA/(stem+'.bin')).exists()
                assert not (DATA/(stem+'_attempt01.log')).exists()
                result = subprocess.run(['python3','dembele/pari/run_dyadic_capped.py',DRIVER,
                                         stem+'_attempt01','PASS|562_DYADIC_TARGET_CHART_CONTROL',
                                         '--chart',str(chart),'--output',stem],
                                        cwd=ROOT,capture_output=True,text=True)
                if result.returncode:
                    print(result.stdout+result.stderr,flush=True)
                    raise RuntimeError('Inspect bounded failure: '+stem)
            receipt = json.loads(rp.read_text())
            assert receipt['status']=='pass' and receipt['exit_code']==0
            assert receipt['command']==command and receipt['driver']==driver==source(ROOT/DRIVER)
            assert receipt['timeout_seconds']==180 and receipt['timeout_terminates_process_group']
            assert source(receipt['log']['path'])==receipt['log']
            metadata = json.loads(mp.read_text())
            assert metadata['status']=='pass' and metadata['chart']==chart
            assert metadata['peak_rss_bytes']<=2*(1<<30)
            assert metadata['actual_harmonic_precision_increased'] is False
            assert source(metadata['target_binary']['path'])==metadata['target_binary']
            markers = [json.loads(s.split('|',1)[1]) for s in Path(receipt['log']['path']).read_text().splitlines() if s.startswith('PHASE_METADATA|')]
            assert markers==[source(mp)]
            record = {'chart':chart,'metadata':source(mp),'receipt':source(rp),
                      'seconds':receipt['wall_seconds'],'peak_rss_bytes':metadata['peak_rss_bytes'],
                      'reused':reused}
            print('D136_CHART_PASS|'+json.dumps(record),flush=True)
            return record
        results = []
        charts = iter(range(17))
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            pending = {pool.submit(job,chart) for chart in [next(charts) for _ in range(args.workers)]}
            while pending:
                done,pending = wait(pending,return_when=FIRST_COMPLETED)
                # Inspect every finished result before submitting more work.
                batch = [future.result() for future in done]
                results.extend(batch)
                for _ in batch:
                    chart = next(charts,None)
                    if chart is not None:
                        pending.add(pool.submit(job,chart))
        assert len(results)==17
        rss_bound = sum(sorted((r['peak_rss_bytes'] for r in results),reverse=True)[:args.workers])
        assert rss_bound<=6*(1<<30)
        record = {'status':'pass','milestone':'D136','kind':'finite_synthetic_chart_controls',
                  'coordinator':source(Path(__file__)),'driver':driver,'workers':args.workers,
                  'jobs':sorted(results,key=lambda r:r['chart']),'completed_jobs':17,
                  'wall_seconds':time.monotonic()-tick,
                  'maximum_job_seconds':max(r['seconds'] for r in results),
                  'maximum_job_RSS_bytes':max(r['peak_rss_bytes'] for r in results),
                  'conservative_concurrent_RSS_sum_bytes':rss_bound,
                  'actual_harmonic_precision_increased':False,'full_bank_launch_admitted':False}
        with out.open('x') as f:
            f.write(json.dumps(record,indent=2)+'\n')
        print('D136_CONTROLS_COMPLETE|'+json.dumps(source(out)),flush=True)


if __name__=='__main__':
    main()
