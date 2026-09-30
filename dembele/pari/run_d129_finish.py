"""Finalize D129 records and run the capped fixed review after all checks pass.

This operational scheduler never reruns a mathematical phase. It waits for
the check scheduler's summary and released lock, fills the draft report and
ledger from completed receipts, then creates and replays the fixed manifest.
Entry-point documentation is updated separately after inspecting the result.
"""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
REPORT = ROOT / 'dembele/certificates/dyadic-precision3200-d129.md'
LEDGER = DATA / 'dyadic_precision3200_sources_d129.json'
REVIEW = DATA / 'dyadic_precision3200_review_d129.json'
COMPLETION = DATA / 'dyadic_precision3200_completion_d129.json'


def read(stem):
    return json.loads((DATA / (stem + '.json')).read_text())


def source(path):
    path = Path(path).resolve()
    sha = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            sha.update(raw)
    return {'path': str(path), 'sha256': sha.hexdigest()}


def main(await_checks):
    assert not REVIEW.exists() and not COMPLETION.exists(), 'inspect completed or partial review; do not rerun'
    summary = DATA / 'dyadic_precision3200_checks_d129.json'
    if await_checks:
        print('D129_FINISH_WAITING|completed checks and released scheduler lock', flush=True)
    while True:
        ready = summary.exists()
        if ready:
            try:
                checks = json.loads(summary.read_text())
            except json.JSONDecodeError:
                ready = False
        if ready:
            assert checks['status'] == 'pass' and checks['completed_check_jobs'] == 29
            lock = (DATA / 'dyadic_streamed_scratch_col00_d129/.coordinator.lock').open('rb')
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                lock.close()
                ready = False
        if ready:
            break
        assert await_checks, 'downstream checks have not finished'
        time.sleep(1)
    assert not REVIEW.exists() and not COMPLETION.exists()
    pilot = read('dyadic_streamed_pilot_P3200_col00_d129')
    state = read('dyadic_streamed_P3200_col00_verified_d129')
    cm = read('dyadic_CM_P3200_col00_d129')
    assert pilot['status'] == state['status'] == cm['status'] == 'pass'
    assert state['certificate']['original_full_residual_zero']
    jobs = []
    peaks = []
    for path in sorted(DATA.glob('*d129*')):
        if not path.is_file() or path.suffix != '.json':
            continue
        packet = json.loads(path.read_text())
        if 'peak_rss_bytes' in packet:
            peaks.append(packet['peak_rss_bytes'])
        if path.name.endswith('.job.json'):
            assert packet['status'] == 'pass' and packet['exit_code'] == 0
            assert packet['timeout_seconds'] == 180 and packet['timeout_terminates_process_group']
            jobs.append(packet)
    assert len(jobs) == 1934
    statistics = {'passed': len(jobs), 'failed': 0,
        'sum_wall_seconds': sum(row['wall_seconds'] for row in jobs),
        'maximum_wall_seconds': max(row['wall_seconds'] for row in jobs),
        'maximum_single_process_peak_rss_bytes': max(peaks),
        'maximum_workers': 3, 'BLAS_threads': 1, 'timeout_seconds': 180,
        'timeout_scope': 'private process group'}
    ledger = json.loads(LEDGER.read_text())
    assert ledger['execution_status'] == 'in_progress'
    ledger['execution_status'] = 'complete'
    ledger['bounded_input_jobs'] = statistics
    ledger['state_arithmetic_certificate'] = state['certificate']
    ledger['storage_certificate'] = {key: pilot[key] for key in (
        'scratch_limit_bytes', 'conservative_scratch_bound_bytes', 'maximum_observed_scratch_bytes',
        'sealed_scratch_bytes', 'sealed_payload_bytes', 'retired_payload_count',
        'retired_payload_bytes', 'retirement_events')}
    ledger['state_timing_certificate'] = {key: pilot[key] for key in (
        'completed_phases', 'state_arithmetic_phases', 'writer_control_phases',
        'sum_recorded_phase_seconds', 'maximum_phase_seconds',
        'maximum_single_phase_peak_rss_bytes', 'coordinator_current_invocation_wall_seconds',
        'phases_resumed_from_prior_invocations')}
    ledger['CM_certificate'] = {key: cm[key] for key in (
        'CM_charts_checked', 'composed_child_maps_checked', 'CM_moment_scalar_coefficients',
        'old_CM_moment_scalar_coefficients_checked', 'old_coarse_values_checked',
        'coarse_error_beta', 'chunked_moment_payload_bytes', 'duplicate_assembled_binary_written')}
    ledger['independent_audits'] = {path.stem: json.loads(path.read_text())['certificates']
        for path in sorted(DATA.glob('dyadic_P3200_audit_*_d129.json'))}
    assert len(ledger['independent_audits']) == 22
    ledger['preserved_global_status']['actual_columns_at_precision_1600'] = [1]
    ledger['preserved_global_status']['actual_columns_at_precision_3200'] = [0]
    ledger['finalization_scheduler'] = source(Path(__file__))
    report = REPORT.read_text()
    old = ('Draft while execution is in progress, 2026-09-28. This report will be\n'
        'finalized and frozen only after all arithmetic and independent checks\n'
        'pass. The full sixteen-column bank remains at P=800. Exact positive\n')
    new = ('Completed input arithmetic and independent checks, 2026-09-28. All\n'
        '1934 bounded input jobs pass, with no failed receipt. Column 0 now\n'
        'reaches P=3200; column 1 reaches P=1600. The full sixteen-column bank\n'
        'remains at P=800. Exact positive\n')
    assert report.count(old) == 1
    report = report.replace(old, new)
    report = report.replace('will record completed receipts and the\n', 'records completed receipts and the\n')
    report = report.replace('will preserve all 9648 source hashes from\n', 'checks preservation of all 9648 source hashes from\n')
    old = ('Execution is in progress. Final timings, observed storage and resident\n'
        'peaks, receipt totals, failures if any, and the next costed execution\n'
        'will be recorded here before the first passing fixed review.\n')
    new = f'''All 1905 state jobs pass, including 48 corrections and the separate
full original residual. All seven CM jobs and all 22 independent audits
also pass. Every mathematical job uses the unchanged 180-second private
process-group cap, assertions and one BLAS thread. Both schedulers enforce
at most three workers; the check scheduler waits for the state summary,
seal and released coordinator lock before launching any worker.

The state coordinator takes {pilot['coordinator_current_invocation_wall_seconds']:.3f} seconds. Summed state phase
durations are {pilot['sum_recorded_phase_seconds']:.3f} seconds; summed input durations are
{statistics['sum_wall_seconds']:.3f} seconds. These are sums of elapsed job times, including
concurrent jobs, not CPU-time measurements. The longest state/input jobs
take {pilot['maximum_phase_seconds']:.3f}/{statistics['maximum_wall_seconds']:.3f} seconds. The highest measured single-process
input resident peak is {statistics['maximum_single_process_peak_rss_bytes']:,} bytes. Selective serial processing
removes the prior complete-bank decoding, but no aggregate RAM bound or
target-size runtime follows from this measurement.

Maximum observed scratch occupancy is {pilot['maximum_observed_scratch_bytes']:,} bytes, below both the
1,510,359,376-byte conservative inventory and the enforced 2 GiB cap.
All 103 retirement barriers complete. They retire 1950 temporary payloads
totalling {pilot['retired_payload_bytes']:,} bytes; four retained payloads total
558,829,536 bytes. The sealed directory occupies {pilot['sealed_scratch_bytes']:,} bytes.
Every earlier frozen artifact is preserved. The state/check schedulers
resume {pilot['phases_resumed_from_prior_invocations']}/{checks['phases_resumed_from_prior_invocations']} prior phases; no injected crash is claimed.

Sources 528--532, both operational schedulers, successful artifacts,
permanent phase/retirement records and sealed scratch freeze on their
first pass. This report and ledger freeze at the first passing fixed
review. Review creation and fixed-manifest replay have separate capped
receipts; their measured outcomes are recorded in the entry-point docs.
Do not rerun completed jobs or coordinators.
'''
    assert report.count(old) == 1
    report = report.replace(old, new)
    assert 'Draft while execution' not in report and 'Execution is in progress' not in report
    LEDGER.write_text(json.dumps(ledger, indent=2) + '\n')
    REPORT.write_text(report)
    results = []
    for suffix, extra in (('attempt01', []), ('recheck01', ['--check'])):
        stem = 'dyadic_precision3200_review_d129_' + suffix
        assert not (DATA / (stem + '.job.json')).exists() and not (DATA / (stem + '.log')).exists()
        cmd = ['python3', 'dembele/pari/run_dyadic_capped.py',
            'dembele/pari/532_dyadic_precision3200_review.py', stem,
            'PASS|532_DYADIC_PRECISION3200_REVIEW'] + extra
        completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if completed.returncode:
            print(completed.stdout + completed.stderr, flush=True)
            raise RuntimeError(stem)
        job = read(stem + '.job')
        assert job['status'] == 'pass' and job['exit_code'] == 0
        results.append({'receipt': source(DATA / (stem + '.job.json')), 'wall_seconds': job['wall_seconds']})
        print('D129_REVIEW|' + json.dumps({'stem': stem, 'seconds': job['wall_seconds']}), flush=True)
    fixed = json.loads(REVIEW.read_text())
    result = {'status': 'pass', 'milestone': 'D129', 'input_jobs_passed': 1934,
        'total_bounded_receipts_passed': 1936, 'fixed_manifest_sources': len(fixed['sources']),
        'reviews': results, 'entrypoint_documentation_update_pending': True,
        'sources': [source(Path(__file__)), source(REVIEW), source(REPORT), source(LEDGER)]}
    with COMPLETION.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D129_REVIEW_COMPLETE|' + json.dumps(result), flush=True)
    lock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--await-checks', action='store_true')
    main(parser.parse_args().await_checks)
