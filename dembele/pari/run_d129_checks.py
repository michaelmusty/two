"""Run the D129 CM and independent checks after the state coordinator returns.

This scheduler performs no mathematical arithmetic. Every worker uses the
unchanged capped runner; dependencies and at most three workers are enforced.
Passing jobs may be authenticated and skipped after a transport disconnect.
An unresolved partial or failed job requires inspection, never blind retry.
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
DATA = ROOT / 'dembele/data/computed'
WRAPPER = 'dembele/pari/run_dyadic_capped.py'
STATE = DATA / 'dyadic_streamed_scratch_col00_d129'
SUMMARY = DATA / 'dyadic_precision3200_checks_d129.json'


def source(path):
    path = Path(path).resolve()
    sha = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            sha.update(raw)
    return {'path': str(path), 'sha256': sha.hexdigest()}


def main(await_state=False):
    assert not SUMMARY.exists(), 'completed check scheduler must not be rerun'
    pilotpath = DATA / 'dyadic_streamed_pilot_P3200_col00_d129.json'
    if await_state:
        print('D129_CHECKS_WAITING|state summary, seal and released coordinator lock', flush=True)
    while True:
        ready = pilotpath.exists() and (STATE / 'SEALED.json').exists()
        if ready:
            try:
                pilot = json.loads(pilotpath.read_text())
            except json.JSONDecodeError:
                # The producing coordinator may still be writing its summary.
                ready = False
        if ready:
            assert pilot['status'] == 'pass' and pilot['completed_phases'] == 1905
            # Reading and locking an existing empty lock does not modify it.
            lock = (STATE / '.coordinator.lock').open('rb')
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                lock.close()
                ready = False
        if ready:
            break
        assert await_state, 'state coordinator has not finished and released its lock'
        time.sleep(1)
    assert not SUMMARY.exists(), 'completed check scheduler must not be rerun'
    tasks = {}

    def task(key, number, filename, stem, marker, args, deps=()):
        assert key not in tasks
        tasks[key] = {'driver': f'dembele/pari/{number}_{filename}.py',
            'stem': stem, 'marker': f'PASS|{number}_{marker}',
            'args': args, 'deps': set(deps)}

    for block in range(8):
        for branch in (0, 1):
            task(f'seed{branch}_{block}', 531, 'dyadic_precision3200_independent',
                f'dyadic_P3200_audit_seed_b{branch}_k{block:02d}_d129',
                'DYADIC_PRECISION3200_INDEPENDENT',
                ['--phase', 'seed-block', '--branch', str(branch), '--block', str(block)],
                () if block == 0 else (f'seed{branch}_{block-1}',))
    chart_keys = []
    for first, last in ((0, 2), (3, 5), (6, 8), (9, 11), (12, 14), (15, 16)):
        key = f'cm{first}'
        chart_keys.append(key)
        task(key, 530, 'dyadic_chunked_CM_precision3200',
            f'dyadic_CM_P3200_col00_d129_c{first:02d}_{last:02d}',
            'DYADIC_CHUNKED_CM_PRECISION3200',
            ['--phase', 'charts', '--first', str(first), '--last', str(last)])
    task('cm_assemble', 530, 'dyadic_chunked_CM_precision3200',
        'dyadic_CM_P3200_col00_d129', 'DYADIC_CHUNKED_CM_PRECISION3200',
        ['--phase', 'assemble'], chart_keys)
    for phase in ('states', 'weighted', 'seed-final'):
        task(phase, 531, 'dyadic_precision3200_independent',
            'dyadic_P3200_audit_' + phase.replace('-', '_') + '_d129',
            'DYADIC_PRECISION3200_INDEPENDENT', ['--phase', phase],
            ('seed0_7', 'seed1_7') if phase == 'seed-final' else ())
    for first, last in ((0, 5), (6, 11), (12, 16)):
        task(f'coarse{first}', 531, 'dyadic_precision3200_independent',
            f'dyadic_P3200_audit_coarse_c{first:02d}_{last:02d}_d129',
            'DYADIC_PRECISION3200_INDEPENDENT',
            ['--phase', 'coarse', '--first', str(first), '--last', str(last)],
            ('cm_assemble',))
    assert len(tasks) == 29

    def run(key):
        row = tasks[key]
        stem = row['stem']
        receipt = DATA / (stem + '_attempt01.job.json')
        log = DATA / (stem + '_attempt01.log')
        output = DATA / (stem + '.json')
        resumed = receipt.exists()
        if not resumed:
            assert not log.exists() and not output.exists(), ('inspect partial', stem)
            cmd = ['python3', WRAPPER, row['driver'], stem + '_attempt01', row['marker']] + row['args']
            result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if result.returncode:
                print(result.stdout + result.stderr, flush=True)
                raise RuntimeError(stem)
        job = json.loads(receipt.read_text())
        assert job['status'] == 'pass' and job['exit_code'] == 0
        assert job['timeout_seconds'] == 180 and job['timeout_terminates_process_group']
        assert job['command'] == ['python3', str(ROOT / row['driver'])] + row['args']
        assert source(job['driver']['path']) == job['driver']
        assert source(log) == job['log']
        packet = json.loads(output.read_text())
        assert packet['status'] == 'pass'
        for file in packet['checkpoint_files']:
            assert source(file['path']) == file
        print('D129_CHECK|' + json.dumps({'key': key, 'seconds': job['wall_seconds'],
            'peak_rss_bytes': packet['peak_rss_bytes'], 'resumed': resumed}), flush=True)
        return {'receipt': source(receipt), 'output': source(output), 'resumed': resumed}

    pending, active, done = list(tasks), {}, {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        while pending or active:
            for key in list(pending):
                if len(active) == 3:
                    break
                if tasks[key]['deps'] <= done.keys():
                    active[pool.submit(run, key)] = key
                    pending.remove(key)
            assert active, 'dependency deadlock'
            finished, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in finished:
                key = active.pop(future)
                done[key] = future.result()
    result = {'status': 'pass', 'milestone': 'D129', 'maximum_workers': 3,
        'completed_check_jobs': len(done), 'prior_state_coordinator_lock_acquired': True,
        'phases_resumed_from_prior_invocations': sum(row['resumed'] for row in done.values()),
        'jobs': done, 'sources': [source(Path(__file__)), source(ROOT / WRAPPER), source(pilotpath)]}
    with SUMMARY.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D129_CHECKS_COMPLETE|29', flush=True)
    lock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--await-state', action='store_true')
    main(parser.parse_args().await_state)
