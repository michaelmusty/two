"""D127 resumable column-1 pilot with capped jobs and bounded scratch retirement.

Every successful phase metadata/log/receipt is immutable. Payloads in the
new marked directory are prospectively temporary until the final seal.
Retirement records commit before unlinking and can finish after interruption.
"""
from concurrent.futures import ThreadPoolExecutor
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
SCRATCH = DATA / 'dyadic_rolling_scratch_col01_d127'
DRIVER = 'dembele/pari/519_dyadic_rolling_precision_chunks.py'
WRAPPER = 'dembele/pari/run_dyadic_capped.py'
CAP = 512 * (1 << 20)
BASE = 'dyadic_rolling_P1600_col01'
SUMMARY = DATA / 'dyadic_rolling_pilot_P1600_col01_d127.json'


def source(path):
    path = Path(path).resolve()
    sha = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(1 << 20):
            sha.update(block)
    return {'path': str(path), 'sha256': sha.hexdigest()}


def save(path, packet):
    with path.open('x') as f:
        f.write(json.dumps(packet, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())


def occupied():
    assert SCRATCH.is_dir() and not SCRATCH.is_symlink()
    paths = list(SCRATCH.iterdir())
    assert all(p.is_file() and not p.is_symlink() for p in paths)
    total = sum(p.stat().st_size for p in paths)
    assert total <= CAP
    return total


def inventory():
    P, old = 1600, 800
    uniform = 174 * P * 8 * 25
    weighted = 174 * sum(((P // 8 if k <= 32 else max(0, (P - k - i + 7) // 8)) + 7) // 8
                        for k in range(P) for i in range(8))
    residual = 174 * (P - old) * 8 * 13
    # Deliberately overcount mutually exclusive slots. At most two complete
    # checkpoints, one newly prepared state, and one active sweep are live.
    slots = {'old_seed_input': uniform // 2, 'seed_extension_chunks': uniform,
        'two_complete_checkpoints': 2 * (weighted + residual),
        'new_prepared_weighted_state': weighted, 'prepared_correction': residual,
        'one_active_operator_sweep': uniform, 'assembled_uniform_state': uniform,
        'final_full_residual': uniform, 'scratch_metadata_allowance': 1 << 20}
    assert sum(slots.values()) < CAP
    return {'status': 'pass', 'milestone': 'D127', 'working_precision_pi': P,
        'seed_precision_pi': old, 'harmonic_basis_column': 1,
        'scratch_limit_bytes': CAP, 'conservative_simultaneous_slots': slots,
        'conservative_total_bytes': sum(slots.values()),
        'writes_serialized_by_advisory_lock_and_hard_byte_check': True,
        'permanent_phase_metadata_and_receipts_outside_scratch': True,
        'maximum_workers': 3, 'phase_timeout_seconds': 180,
        'full_bank_or_target_size_cost_certificate': False,
        'sources': [source(Path(__file__)), source(ROOT / DRIVER)]}


def apply_retirement(event):
    assert event['coordinator'] == source(Path(__file__))
    anchor = event['anchor_receipt']
    assert source(anchor['path']) == anchor
    assert json.loads(Path(anchor['path']).read_text())['status'] == 'pass'
    for row in event['retire']:
        record = row['source']
        path = Path(record['path'])
        assert path.parent == SCRATCH and path.suffix == '.bin' and not path.is_symlink()
        if path.exists():
            assert source(path) == record and path.stat().st_size == row['bytes']
            path.unlink()


def main():
    start = time.monotonic()
    assert not SUMMARY.exists(), 'completed coordinator must not be rerun'
    owner = {'namespace': 'D127-column1', 'driver': source(ROOT / DRIVER),
        'coordinator': source(Path(__file__)), 'scratch_limit_bytes': CAP,
        'payloads_prospectively_transient_until_final_seal': True}
    if not SCRATCH.exists():
        SCRATCH.mkdir()
        save(SCRATCH / 'OWNER.json', owner)
    assert json.loads((SCRATCH / 'OWNER.json').read_text()) == owner
    lock = (SCRATCH / '.coordinator.lock').open('a+b')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    invpath = DATA / 'dyadic_rolling_inventory_d127.json'
    inv = inventory()
    if invpath.exists():
        assert json.loads(invpath.read_text()) == inv
    else:
        save(invpath, inv)
    print('ROLLING_INVENTORY|' + json.dumps(inv['conservative_simultaneous_slots']) +
        '; total=' + str(inv['conservative_total_bytes']), flush=True)
    prior_events = sorted(DATA.glob('dyadic_rolling_retirement_d127_*.json'))
    if prior_events and not (SCRATCH / 'SEALED.json').exists():
        apply_retirement(json.loads(prior_events[-1].read_text()))
    jobs, bootstrap, events = [], [], []
    barrier = 0

    def job(phase, stem, extra):
        receipt = DATA / (stem + '_attempt01.job.json')
        log, out = DATA / (stem + '_attempt01.log'), DATA / (stem + '.json')
        cmd = ['python3', WRAPPER, DRIVER, stem + '_attempt01',
            'PASS|519_DYADIC_ROLLING_PRECISION_CHUNKS', '--phase', phase, '--output', stem] + extra
        resumed = receipt.exists()
        if not resumed:
            assert not log.exists() and not out.exists(), ('inspect partial phase before resuming', stem)
            completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if completed.returncode:
                print(completed.stdout + completed.stderr, flush=True)
                raise RuntimeError(stem)
        row = json.loads(receipt.read_text())
        assert row['status'] == 'pass' and row['exit_code'] == 0
        assert row['timeout_seconds'] == 180 and row['timeout_terminates_process_group']
        assert row['command'] == ['python3', str(ROOT / DRIVER)] + cmd[5:]
        assert source(row['driver']['path']) == row['driver'] and source(row['log']['path']) == row['log']
        bindings = [json.loads(line.split('|', 1)[1]) for line in log.read_text().splitlines()
                    if line.startswith('PHASE_METADATA|')]
        assert bindings == [source(out)]
        packet = json.loads(out.read_text())
        assert packet['status'] == 'pass' and packet['phase'] == phase
        assert packet['checkpoint_payloads_prospectively_transient']
        print('ROLLING_PHASE|' + json.dumps({'stem': stem, 'seconds': row['wall_seconds'],
            'peak_rss_bytes': packet['peak_rss_bytes'], 'scratch_bytes': packet['scratch_bytes_after'],
            'lower_pi': packet.get('weighted_residual_lower_bound_pi'), 'resumed': resumed}), flush=True)
        return packet, receipt, out, resumed

    def one(phase, stem, extra):
        value = job(phase, stem, extra)
        jobs.append(value)
        return value[0]

    def sweep(previous, prefix, purpose):
        def worker(first):
            return job('sweep', f'{prefix}_e{first:03d}_{first + 28:03d}',
                ['--previous', previous, '--purpose', purpose, '--first', str(first), '--last', str(first + 28)])
        with ThreadPoolExecutor(max_workers=3) as pool:
            values = list(pool.map(worker, range(0, 174, 29)))
        jobs.extend(values)
        return [value[0] for value in values]

    def cleanup(packets, final=False):
        nonlocal barrier
        barrier += 1
        path = DATA / f'dyadic_rolling_retirement_d127_{barrier:03d}.json'
        expected = {row['path']: row for packet in packets + ([] if final else bootstrap)
                    for row in packet['checkpoint_files']}
        if path.exists():
            event = json.loads(path.read_text())
            assert {row['source']['path']: row['source'] for row in event['keep']} == expected
        else:
            assert not (SCRATCH / 'SEALED.json').exists()
            for record in expected.values():
                assert source(record['path']) == record
            keep = [{'source': expected[p], 'bytes': Path(p).stat().st_size} for p in sorted(expected)]
            retire = [{'source': source(p), 'bytes': p.stat().st_size} for p in sorted(SCRATCH.glob('*.bin'))
                      if str(p) not in expected]
            event = {'status': 'pass', 'barrier': barrier, 'coordinator': source(Path(__file__)),
                'anchor_receipt': source(jobs[-1][1]), 'keep': keep, 'retire': retire,
                'before_scratch_bytes': occupied(), 'final_retirement': final,
                'retired_payload_hashes_are_history_not_retained_sources': True}
            save(path, event)
            apply_retirement(event)
            assert occupied() <= CAP
        events.append((path, event))

    initial = BASE + '_input_d127'
    packet = one('init', initial, ['--precision', '1600', '--seed', 'dyadic_weighted_P800_col01_verified_d125'])
    bootstrap.append(packet)
    cleanup([packet])
    extension = BASE + '_extend_d127'
    bootstrap.extend(sweep(initial, extension, 'extend'))
    seed = BASE + '_seed_assembled_d127'
    packet = one('seed-assemble', seed, ['--previous', initial, '--chunks', extension])
    cleanup([packet])
    rhs = BASE + '_seed_rhs_d127'
    sweep(seed, rhs, 'seed-low-rhs')
    low = BASE + '_seed_low_d127'
    packet = one('seed-low-finish', low, ['--previous', seed, '--chunks', rhs])
    cleanup([packet])
    prefix = BASE + '_seed_operator_d127'
    sweep(low, prefix, 'seed-residual')
    previous = BASE + '_seed_d127'
    checkpoint = one('finish-seed', previous, ['--previous', low, '--chunks', prefix])
    predecessor = None
    cleanup([checkpoint])
    step = 0
    while checkpoint['active_moment_count'] > 33:
        step += 1
        assert step <= 24
        prepared = BASE + f'_step{step:02d}_prepared_d127'
        packet = one('prepare-step', prepared, ['--previous', previous])
        cleanup([packet, checkpoint] + ([predecessor] if predecessor else []))
        prefix = BASE + f'_step{step:02d}_operator_d127'
        sweep(prepared, prefix, 'correction')
        previous = BASE + f'_step{step:02d}_d127'
        predecessor = checkpoint
        checkpoint = one('finish-step', previous, ['--previous', prepared, '--chunks', prefix])
        cleanup([checkpoint, predecessor])
    prefix = BASE + '_reconstruct_operator_d127'
    sweep(previous, prefix, 'reconstruct')
    reconstructed = BASE + '_reconstructed_d127'
    packet = one('finish-reconstruct', reconstructed, ['--previous', previous, '--chunks', prefix])
    cleanup([packet, checkpoint, predecessor])
    prefix = BASE + '_verify_operator_d127'
    sweep(reconstructed, prefix, 'verify')
    verified = BASE + '_verified_d127'
    packet = one('finish-verify', verified, ['--previous', reconstructed, '--chunks', prefix])
    assert packet['certificate']['original_full_residual_zero'] and step == 24 and len(jobs) == 228
    cleanup([packet, checkpoint], final=True)
    sealpath = SCRATCH / 'SEALED.json'
    seal = {'status': 'pass', 'namespace': 'D127-column1', 'all_remaining_files_now_frozen': True,
        'verified_checkpoint': source(DATA / (verified + '.json')),
        'weighted_checkpoint': source(DATA / (previous + '.json')),
        'final_retirement': source(events[-1][0])}
    if sealpath.exists():
        assert json.loads(sealpath.read_text()) == seal
    else:
        save(sealpath, seal)
    receipts = [json.loads(receipt.read_text()) for _, receipt, _, _ in jobs]
    outputs = [packet for packet, _, _, _ in jobs]
    retired = {row['source']['path']: row for _, event in events for row in event['retire']}
    retained = sorted(p for p in SCRATCH.iterdir() if p.is_file())
    peak = max([occupied()] + [p['scratch_bytes_after'] for p in outputs] +
               [event['before_scratch_bytes'] for _, event in events])
    result = {'status': 'pass', 'milestone': 'D127', 'working_precision_pi': 1600, 'harmonic_basis_column': 1,
        'completed_phases': 228, 'correction_steps': step, 'correction_history': packet['correction_history'],
        'verified_checkpoint': seal['verified_checkpoint'], 'weighted_checkpoint': seal['weighted_checkpoint'],
        'maximum_workers': 3, 'chunk_size': 29, 'scratch_limit_bytes': CAP,
        'conservative_scratch_bound_bytes': inv['conservative_total_bytes'], 'maximum_observed_scratch_bytes': peak,
        'sealed_scratch_bytes': occupied(), 'sealed_payload_bytes': sum(p.stat().st_size for p in retained if p.suffix == '.bin'),
        'retired_payload_count': len(retired), 'retired_payload_bytes': sum(row['bytes'] for row in retired.values()),
        'retirement_events': len(events), 'retired_payloads_are_not_retained_sources': True,
        'sum_recorded_phase_seconds': sum(r['wall_seconds'] for r in receipts),
        'maximum_phase_seconds': max(r['wall_seconds'] for r in receipts),
        'maximum_single_phase_peak_rss_bytes': max(p['peak_rss_bytes'] for p in outputs),
        'coordinator_current_invocation_wall_seconds': time.monotonic() - start,
        'phases_resumed_from_prior_invocations': sum(resumed for _, _, _, resumed in jobs),
        'full_sixteen_column_bank_precision_pi': 800, 'complete_target_size_solve_costed': False,
        'sources': [source(path) for path in [Path(__file__), ROOT / DRIVER, ROOT / WRAPPER, invpath,
            *retained, *[r for _, r, _, _ in jobs], *[o for _, _, o, _ in jobs], *[e for e, _ in events]]]}
    save(SUMMARY, result)
    print('ROLLING_PILOT_COMPLETE|' + json.dumps({k: v for k, v in result.items() if k != 'sources'}), flush=True)
    lock.close()


if __name__ == '__main__':
    main()
