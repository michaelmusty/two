"""Durable, nonmathematical supervisor for the user-approved D156 pilot.

Run exactly one production coordinator, then its audits and both column
reviews. Every mathematical child uses the unchanged capped wrapper.
Failure stops the sequence; this supervisor never retries or overwrites a
completed run. The final timing reassessment is a separate bounded review.
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
import traceback

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
CONFIG = 'dyadic_staged_P6400_col02_config_d156'
BASE = 'dyadic_staged_P6400_col02_d156'
PLAN = 'dyadic_higher_pilot_col02_audit_plan_d156'
REVIEW = 'dyadic_higher_pilot_col02_review_d156'
RUN = 'dyadic_higher_pilot_pipeline_d157_run01'
WRAPPER = 'dembele/pari/run_dyadic_capped.py'
DRIVER = 'dembele/pari/647_dyadic_higher_pilot_column_review.py'
MARKER = 'PASS|647_DYADIC_HIGHER_PILOT_COLUMN_REVIEW'


def now():
    return datetime.now(timezone.utc).isoformat()


def source(path):
    path = Path(path).resolve()
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return {'path': str(path), 'sha256': digest.hexdigest()}


def read(stem):
    return json.loads((DATA / (stem + '.json')).read_text())


def create(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def status(value):
    value = {'updated_utc': now(), 'supervisor_pid': os.getpid(), **value}
    path = DATA / (RUN + '_status.json')
    temporary = DATA / (RUN + '_status.tmp')
    with temporary.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    print('D157_PIPELINE_STATUS|' + json.dumps(value), flush=True)


def main():
    assert __debug__
    for key in ['PYTHONDONTWRITEBYTECODE', 'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS',
                'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        assert os.environ.get(key) == '1', key
    lock = (DATA / (RUN + '.lock')).open('a+b')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    launch_path = DATA / (RUN + '_launch.json')
    completed = DATA / (RUN + '_completed.json')
    assert not launch_path.exists() and not completed.exists(), 'inspect the existing supervisor run; never start it twice'
    cfg = read(CONFIG)
    admission_path = DATA / (cfg['admission_review'] + '.json')
    admission = read(cfg['admission_review'])
    assert admission['status'] == 'pass' and admission['indexed_receipt_coordinator_admitted']
    assert admission['permitted_configs'] == [source(DATA / (CONFIG + '.json'))]
    launch_check = read('dyadic_higher_pilot_launchcheck_d156_attempt01.job')
    assert launch_check['status'] == 'pass' and launch_check['exit_code'] == 0
    assert launch_check['command'] == ['python3', str(ROOT / 'dembele/pari/650_dyadic_higher_pilot_preparation_review.py'), '--launch-check']
    assert launch_check['timeout_seconds'] == 180 and launch_check['timeout_terminates_process_group']
    assert source(launch_check['driver']['path']) == launch_check['driver']
    assert source(launch_check['log']['path']) == launch_check['log']
    marks = [json.loads(line.split('|', 1)[1]) for line in Path(launch_check['log']['path']).read_text().splitlines()
             if line.startswith('PHASE_METADATA|')]
    assert marks == [source(admission_path)]
    assert shutil.disk_usage(ROOT).free >= cfg['launch_free_space_gate_bytes']
    assert not (DATA / cfg['namespace'] / 'CURRENT.json').exists()
    assert not (DATA / (BASE + '_completed.json')).exists()
    stages = [
        ('production', ['python3', 'dembele/pari/run_d139_indexed_production.py', '--config', CONFIG, '--workers', '3'],
         'dyadic_higher_pilot_production_d157_run01.log', BASE + '_completed'),
        ('audits', ['python3', 'dembele/pari/run_d137_audits.py', '--plan', PLAN, '--workers', '3'],
         'dyadic_higher_pilot_audits_d157_run01.log', PLAN + '_completed'),
        ('column_review', ['python3', WRAPPER, DRIVER, REVIEW + '_attempt01', MARKER, '--config', CONFIG, '--output', REVIEW],
         'dyadic_higher_pilot_column_review_d157_run01.log', REVIEW + '_attempt01.job'),
        ('column_replay', ['python3', WRAPPER, DRIVER, REVIEW + '_recheck01', MARKER, '--config', CONFIG, '--output', REVIEW, '--check'],
         'dyadic_higher_pilot_column_replay_d157_run01.log', REVIEW + '_recheck01.job')]
    for _, _, log_name, output in stages:
        assert not (DATA / log_name).exists() and not (DATA / (output + '.json')).exists()
    launch = {'status': 'started', 'milestone': 'D157', 'started_utc': now(),
              'supervisor_pid': os.getpid(), 'config': source(DATA / (CONFIG + '.json')),
              'supervisor': source(Path(__file__)), 'admission': source(admission_path),
              'launch_check_receipt': source(DATA / 'dyadic_higher_pilot_launchcheck_d156_attempt01.job.json'),
              'maximum_mathematical_workers': 3, 'mathematical_job_timeout_seconds': 180,
              'no_other_column_or_stage_admitted': True,
              'stages': [{'name': name, 'command': command, 'log': str(DATA / log_name), 'output': str(DATA / (output + '.json'))}
                         for name, command, log_name, output in stages]}
    create(launch_path, launch)
    caffeine = None
    rows = []
    tick = time.monotonic()
    try:
        executable = shutil.which('caffeinate')
        if executable:
            caffeine = subprocess.Popen([executable, '-i', '-w', str(os.getpid())],
                                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for name, command, log_name, output in stages:
            started_utc, started = now(), time.monotonic()
            with (DATA / log_name).open('xb') as log:
                child = subprocess.Popen(command, cwd=ROOT, env=dict(os.environ), stdin=subprocess.DEVNULL,
                                         stdout=log, stderr=subprocess.STDOUT)
                status({'status': 'running', 'stage': name, 'child_pid': child.pid,
                        'stage_started_utc': started_utc, 'log': str(DATA / log_name),
                        'completed_stages': rows, 'temporary_idle_sleep_prevention_pid': caffeine.pid if caffeine else None})
                code = child.wait()
            row = {'name': name, 'command': command, 'started_utc': started_utc, 'ended_utc': now(),
                   'monotonic_seconds': time.monotonic() - started, 'exit_code': code, 'log': source(DATA / log_name)}
            rows.append(row)
            assert code == 0, f'{name} failed; inspect its log and preserve all partial data'
            value = read(output)
            assert value['status'] == 'pass', name
            row['output'] = source(DATA / (output + '.json'))
        result = {'status': 'pass', 'milestone': 'D157', 'launch': source(launch_path), 'completed_utc': now(),
                  'supervisor_monotonic_seconds': time.monotonic() - tick, 'stages': rows,
                  'production_audits_and_both_column_reviews_finished': True,
                  'timing_reassessment_pending': True, 'next_column_or_stage_launched': False}
        create(completed, result)
        status({'status': 'pass', 'stage': 'column_complete_timing_reassessment_pending',
                'completed_stages': rows, 'completion': source(completed)})
    except BaseException:
        status({'status': 'stopped_after_failure', 'completed_stages': rows,
                'error': traceback.format_exc(), 'automatic_retry_attempted': False})
        raise
    finally:
        if caffeine is not None:
            caffeine.terminate()
            caffeine.wait(timeout=10)
            create(DATA / (RUN + '_power_assertion_finished.json'),
                   {'status': 'pass', 'finished_utc': now(), 'owned_caffeinate_pid': caffeine.pid,
                    'return_code': caffeine.returncode, 'permanent_power_settings_changed': False})


if __name__ == '__main__':
    main()
