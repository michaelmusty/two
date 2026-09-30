"""D133 resume an explicit finite job list, preserving all completed receipts.

This coordinator performs no mathematical arithmetic. The caller must keep
the sum of worker limits of simultaneous coordinators/manual jobs at most 3.
"""
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'


def source(path):
    path = Path(path).resolve()
    sha = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            sha.update(raw)
    return {'path': str(path), 'sha256': sha.hexdigest()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan', required=True)
    p.add_argument('--workers', type=int, required=True)
    args = p.parse_args()
    assert 1 <= args.workers <= 3
    path = DATA / (args.plan + '.json')
    plan = json.loads(path.read_text())
    out = DATA / (args.plan + '_completed.json')
    assert not out.exists(), 'completed batch must not be rerun'
    lock = (DATA / (args.plan + '.lock')).open('a+b')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert plan['milestone'] == 'D133' and plan['kind'] == 'bounded_job_plan'
    assert plan['requires_completed_and_sealed_actual_column']
    actual = json.loads((DATA / 'dyadic_staged_P6400_col00_d133_completed.json').read_text())
    assert actual['status'] == 'pass' and actual['all_phases_complete']
    assert (DATA / 'dyadic_rowjournal_P6400_col00_d132' / 'SEALED.json').is_file()
    assert len({job['stem'] for job in plan['jobs']}) == len(plan['jobs'])
    start = time.monotonic()

    def job(spec):
        driver, stem, marker, extra = spec['driver'], spec['stem'], spec['marker'], spec['args']
        receipt = DATA / (stem + '_attempt01.job.json')
        log = DATA / (stem + '_attempt01.log')
        metadata = DATA / (stem + '.json')
        command = ['python3', str(ROOT / driver)] + extra + ['--output', stem]
        resumed = receipt.exists()
        if not resumed:
            assert not log.exists() and not metadata.exists(), ('inspect partial job', stem)
            cmd = ['python3', 'dembele/pari/run_dyadic_capped.py', driver,
                   stem + '_attempt01', marker] + extra + ['--output', stem]
            done = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if done.returncode:
                print(done.stdout + done.stderr, flush=True)
                raise RuntimeError(stem)
        row = json.loads(receipt.read_text())
        assert row['status'] == 'pass' and row['exit_code'] == 0
        assert row['timeout_seconds'] == 180 and row['timeout_terminates_process_group']
        assert row['command'] == command
        assert source(row['driver']['path']) == row['driver'] and source(row['log']['path']) == row['log']
        bindings = [json.loads(line.split('|', 1)[1]) for line in log.read_text().splitlines()
                    if line.startswith('PHASE_METADATA|')]
        assert bindings == [source(metadata)]
        packet = json.loads(metadata.read_text())
        assert packet['status'] == 'pass' and packet['milestone'] == 'D133'
        assert packet['peak_rss_bytes'] <= 2 * (1 << 30)
        result = {'stem': stem, 'receipt': source(receipt), 'metadata': source(metadata),
                  'seconds': row['wall_seconds'], 'peak_rss_bytes': packet.get('peak_rss_bytes'), 'resumed': resumed}
        print('D133_JOB|' + json.dumps(result), flush=True)
        return result

    # Submit only the running window. A failure drains at most the other
    # already-running capped jobs, without admitting the rest of the plan.
    rows = [None] * len(plan['jobs'])
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {}
        cursor = 0
        try:
            while cursor < len(plan['jobs']) or pending:
                while cursor < len(plan['jobs']) and len(pending) < args.workers:
                    pending[pool.submit(job, plan['jobs'][cursor])] = cursor
                    cursor += 1
                finished, _ = wait(pending, return_when=FIRST_COMPLETED)
                # Check every completion before submitting replacements.
                for future in finished:
                    rows[pending.pop(future)] = future.result()
        except BaseException:
            for future in pending:
                future.cancel()
            raise
    result = {'status': 'pass', 'milestone': 'D133', 'plan': source(path),
        'coordinator': source(Path(__file__)), 'worker_limit': args.workers,
        'completed_jobs': len(rows), 'jobs': rows, 'wall_seconds': time.monotonic() - start}
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())
    print('D133_BATCH_COMPLETE|' + json.dumps(source(out)), flush=True)


if __name__ == '__main__':
    main()
