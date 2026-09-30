"""D133 finite provenance and complete phase review of one actual P=6400 column.

No production arithmetic is imported. Source 556 supplies independently
computed samples and complete old overlaps. Original full equations are
certified by the authenticated production jobs, with their scope explicit.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
BASE = 'dyadic_staged_P6400_col00_d133'
CONFIG = 'dyadic_staged_P6400_col00_config_d133'
STORE = DATA / 'dyadic_rowjournal_P6400_col00_d132'
OUT = DATA / 'dyadic_precision6400_review_d133.json'
DRIVER = ROOT / 'dembele/pari/554_dyadic_resumable_staged_production.py'
P, S, N = 6400, 3200, 174
CAP, RSS_CAP = 2 * (1 << 30), 2 * (1 << 30)
PATHS, CACHE = {Path(__file__)}, {}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        h = hashlib.sha256()
        with path.open('rb') as stream:
            while raw := stream.read(1 << 20):
                h.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': h.hexdigest()}
    return CACHE[path]


def checked(records):
    for record in records:
        assert source(record['path']) == record, record['path']


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    value = json.loads(path.read_text())
    assert value['status'] == 'pass', stem
    return value


def envelope(name):
    path = STORE / name
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert set(packet) == {'value', 'sha256'}
    assert hashlib.sha256(canonical(packet['value'])).hexdigest() == packet['sha256']
    return packet['value']


def expected_groups():
    """Separate explicit specification, without importing the scheduler."""
    def one(phase, key, **kw):
        return [dict(phase=phase, key=key, **kw)]
    def rows(phase, prefix, size=1, count=N, **kw):
        return [dict(phase=phase, key=f'{prefix}_e{e:03d}_{min(e+size-1,count-1):03d}',
                     first=e, last=min(e+size-1,count-1), **kw)
                for e in range(0, count, size)]
    yield one('create', 'create')
    yield rows('extend', 'extend')
    yield one('init-finish', 'init_finish')
    for step in range(97):
        bits = 800 if step == 0 else 800 - (S + 33 * (step - 1)) // 8
        digits = list(range(200, bits, 200)) + [bits]
        yield one('low-begin', f'low_begin_{step:03d}', step=step)
        yield rows('rhs', f'rhs{step:03d}', size=3, step=step)
        for digit in range(len(digits)):
            for phase in ('low-residual', 'low-solve', 'low-verify'):
                yield one(phase, f"{phase.replace('-', '_')}_{step:03d}_{digit:02d}",
                          step=step, digit=digit)
        yield one('prepare-begin', f'prepare_begin_{step:03d}', step=step)
        for row in rows('prepare-rows', f'prepare{step:03d}', size=29, step=step):
            yield [row]
        yield one('prepare-finish', f'prepare_finish_{step:03d}', step=step)
        yield one('sweep-begin', f'sweep_begin_{step:03d}', step=step)
        yield rows('operator', f'operator{step:03d}', step=step)
        yield one('sweep-finish', f'sweep_finish_{step:03d}', step=step)
    yield one('verify-begin', 'verify_begin')
    yield rows('verify', 'verify')
    yield one('cm-begin', 'cm_begin')
    yield rows('cm', 'cm', count=17)
    yield [dict(phase='coarse', key=f'coarse_c{ci:02d}_o{order}', chart=ci, order=order)
           for ci in range(17) for order in range(4)]
    yield one('seal', 'seal')


def receipt(record, metadata, driver, args):
    checked([record, metadata])
    row = json.loads(Path(record['path']).read_text())
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert row['timeout_seconds'] == 180 and row['timeout_terminates_process_group']
    assert row['command'] == ['python3', str(driver)] + args
    assert row['driver'] == source(driver)
    checked([row['log']] + row['sources'])
    log = Path(row['log']['path']).read_text().splitlines()
    bindings = [json.loads(line.split('|', 1)[1]) for line in log if line.startswith('PHASE_METADATA|')]
    assert bindings == [metadata]
    packet = json.loads(Path(metadata['path']).read_text())
    assert packet['status'] == 'pass'
    checked(packet.get('sources', []))
    return row, packet


def phase_certificate(spec, cert, history):
    phase, step = spec['phase'], spec.get('step')
    if phase in ('rhs', 'prepare-rows', 'operator', 'extend', 'verify', 'cm'):
        first, last = spec['first'], spec['last']
        assert (cert['first'], cert['last']) == (first, last)
        width = last - first + 1
    if phase == 'create':
        assert cert['weighted_state_bytes'] == 449407200
    elif phase == 'extend':
        assert cert['old_uniform_scalar_overlaps'] == width * S * 8
        assert cert['original_child_actions'] == 2 * width
    elif phase == 'init-finish':
        assert cert['generation'] == 'initial'
        assert cert['state_sha256'] == history[0]['state']['sha256']
    elif phase in ('low-begin', 'rhs', 'low-residual', 'low-solve', 'low-verify'):
        bits = 800 if step == 0 else 800 - (S + 33 * (step - 1)) // 8
        digits = list(range(200, bits, 200)) + [bits]
        if phase == 'low-begin':
            assert cert == {'bits': bits, 'digits': digits,
                            'base_tag': 'initial' if step == 0 else f'ready{step-1:03d}'}
        elif phase == 'rhs':
            assert cert['original_child_actions'] == 2 * width and cert['bits'] == bits
        else:
            digit = spec['digit']
            new, old = digits[digit], digits[digit - 1] if digit else 0
            answer = envelope(f'pool_answer{step:03d}_{digit:02d}.json')
            assert answer['complete'] and answer['retired']
            if phase == 'low-residual':
                quotient = envelope(f'pool_quotient{step:03d}_{digit:02d}.json')
                assert quotient['complete'] and quotient['retired']
                assert cert['old_bits'] == old and cert['new_bits'] == new
                assert cert['exact_divisions'] == (44544 if old else 0)
                assert cert['quotient_sha256'] == quotient['sha256']
            elif phase == 'low-solve':
                assert cert['bits'] == new and cert['factor_bits'] == new - old <= 200
                assert cert['factor_blocks'] == 1226 and cert['answer_sha256'] == answer['sha256']
            else:
                assert cert == envelope(f'valid{step:03d}_{digit:02d}.json')
                assert cert['bits'] == new and cert['all_original_low_equations'] == 44544
                assert cert['answer_sha256'] == answer['sha256']
    elif phase == 'prepare-begin':
        assert cert == {'step': step, 'low_answer_verified': True}
    elif phase == 'prepare-rows':
        assert cert['prepared_rows'] == width
    elif phase == 'prepare-finish':
        cur = history[2 * step + 1]
        assert cert == {'tag': f'prepared{step:03d}', 'state_sha256': cur['state']['sha256'],
                        'correction_sha256': cur['aux']['sha256']}
    elif phase in ('sweep-begin', 'operator', 'sweep-finish'):
        after = S + 33 * step
        count, bits = max(33, P - after), 800 - after // 8
        cur = history[2 * step + 2]
        assert cur['authority'] == {'u': after, 'count': count, 'bits': bits}
        if phase == 'sweep-begin':
            assert cert == {'after_pi': after, 'count': count, 'bits': bits}
        elif phase == 'operator':
            assert cert['after_pi'] == after and cert['count'] == count
            assert cert['row_sha256'] == cur['aux']['row_sha256'][first:last + 1]
        else:
            assert cert == {'tag': f'ready{step:03d}', 'u': after, 'count': count,
                            'residual_sha256': cur['aux']['sha256']}
    elif phase == 'verify-begin':
        assert cert == {'weighted_residual_is_zero': True, 'tag': 'ready096'}
    elif phase == 'verify':
        assert cert['weighted_equation_scalars'] == width * P * 8 and cert['masses'] == width
    elif phase == 'cm-begin':
        assert cert == {'all_weighted_equations_checked': N * P * 8, 'CM_payload_bytes': 174080000}
    elif phase == 'cm':
        assert cert['CM_scalars'] == width * 2 * P * 8 and cert['old_overlap_precision_pi'] == S
    elif phase == 'coarse':
        assert cert['chart'] == spec['chart'] and cert['order'] == spec['order']
        assert cert['error_beta'] == 2 * P + (32, 48, 32, 64)[spec['order']]
        assert len(cert['coarse_value_beta']) == 16 and cert['old_overlap_checked']
    elif phase == 'seal':
        assert cert['precision_pi'] == P and cert['new_mathematical_precision']
        assert cert['weighted_state'] == history[-1]['state'] and cert['residual'] == history[-1]['aux']
        assert cert['CM'] == envelope('pool_CM.json')
    else:
        raise AssertionError(phase)


def full_file(info):
    path = STORE / info['name']
    assert path.stat().st_size == info['bytes'] == info['rows'] * info['row_bytes']
    assert source(path)['sha256'] == info['sha256']
    assert len(info['row_sha256']) == info['rows']
    with path.open('rb') as stream:
        for sha in info['row_sha256']:
            raw = stream.read(info['row_bytes'])
            assert len(raw) == info['row_bytes'] and hashlib.sha256(raw).hexdigest() == sha
        assert not stream.read(1)


def inspect_store():
    owner, cur, seal = [envelope(name + '.json') for name in ('OWNER', 'CURRENT', 'SEALED')]
    assert owner['storage_source_sha256'] == source(ROOT / 'dembele/pari/547_dyadic_staged_store.py')['sha256']
    assert owner['cap_bytes'] == CAP and seal['all_remaining_files_frozen']
    assert seal['current_sha256'] == hashlib.sha256(canonical(cur)).hexdigest()
    assert cur['epoch'] == 194 and cur['tag'] == 'ready096' and cur['phase'] == 'ready'
    assert cur['authority'] == {'u': 6368, 'count': 33, 'bits': 4}
    assert cur['state']['bytes'] == 449407200 and cur['aux']['bytes'] == N * 33 * 8
    for name in ('TXN.json', 'WAL.json', 'RETIRE.json', 'WORKSPACE.bin'):
        assert not (STORE / name).exists()
    assert not list(STORE.glob('*.tmp')) and not list(STORE.glob('wal_*.bin'))
    live = {cur[kind]['name'] for kind in ('state', 'aux')}
    for kind in ('state', 'aux'):
        full_file(cur[kind])
    assert not any((STORE / cur['aux']['name']).read_bytes())
    for path in sorted(STORE.glob('pool_*.json')):
        pool = envelope(path.name)
        if pool.get('retired'):
            assert not (STORE / pool['name']).exists()
        elif pool.get('historical_after_state_update'):
            assert path.name == 'pool_initial.json' and pool['name'] == cur['state']['name']
        else:
            assert pool['complete']
            full_file(pool)
            live.add(pool['name'])
    assert {path.name for path in STORE.glob('*.bin')} == live
    assert live == {'state.bin', 'aux_ready096.bin', 'CM.bin', 'verification.bin'}
    assert envelope('pool_CM.json')['bytes'] == 174080000
    assert envelope('pool_verification.json')['bytes'] == N * 32
    verified = envelope('VERIFIED.json')
    assert verified['state'] == cur['state'] and verified['tag'] == cur['tag']
    assert verified['verification'] == envelope('pool_verification.json')
    assert verified['all_QT_w_equals_w'] and verified['masses'] == N
    history = [envelope(path.name) for path in sorted(STORE.glob('history_*.json'))]
    assert [row['epoch'] for row in history] == list(range(194))
    history.append(cur)
    assert history[0]['tag'] == 'initial' and history[0]['phase'] == 'ready'
    for step in range(97):
        base, prepared, ready = history[2*step:2*step+3]
        context = envelope(f'low_{step:03d}.json')
        assert context['base'] == base
        assert prepared['tag'] == f'prepared{step:03d}' and prepared['phase'] == 'prepared'
        assert ready['tag'] == f'ready{step:03d}' and ready['phase'] == 'ready'
        assert prepared['state'] == ready['state']
        retired = envelope(f'retired_{2*step+2:04d}.json')
        assert retired == {'after_tag': ready['tag'], 'name': prepared['aux']['name'], 'old_info': prepared['aux']}
        assert not (STORE / retired['name']).exists()
    assert len(list(STORE.glob('retired_*.json'))) == 97
    assert envelope('pool_initial.json')['sha256'] == history[0]['state']['sha256']
    archived = set()
    for path in sorted(STORE.glob('archive_*.json')):
        archive = envelope(path.name)
        assert archive['external_records_remain_frozen'] and not archive['arithmetic_payloads_removed']
        assert archive['source'] == source(ROOT / 'dembele/pari/551_dyadic_staged_metadata_archive.py')
        assert len(canonical(archive)) <= 512 * (1 << 10)
        for item in archive['items']:
            assert item['name'] not in archived and not item['name'].startswith('done_coarse_')
            archived.add(item['name'])
            checked([item['external_metadata'], item['passing_receipt']])
            external = json.loads(Path(item['external_metadata']['path']).read_text())
            original = canonical({'value': external, 'sha256': hashlib.sha256(canonical(external)).hexdigest()})
            assert len(original) == item['bytes'] and hashlib.sha256(original).hexdigest() == item['internal_sha256']
            assert not (STORE / item['name']).exists()
    assert len(list(STORE.glob('archive_*.json'))) == 97
    PATHS.update(STORE.iterdir())
    return history, archived, {
        'namespace': STORE.name, 'epoch': 194, 'history_records': 194, 'retirement_records': 97,
        'archived_duplicate_records': len(archived), 'all_current_full_and_row_hashes_checked': True,
        'retained_payload_bytes': sum((STORE / name).stat().st_size for name in live),
        'retained_store_bytes': sum(path.stat().st_size for path in STORE.iterdir()),
        'historical_payload_hashes_are_not_retained_source_claims': True}


def execution_review(history, archived):
    cfg = read(CONFIG)
    assert cfg['execution_milestone'] == 'D133' and cfg['milestone'] == 'D132'
    assert (cfg['precision_pi'], cfg['seed_precision_pi'], cfg['column']) == (P, S, 0)
    assert (cfg['digit_bits'], cfg['state_chunk'], cfg['rhs_chunk'], cfg['CM_chunk']) == (200, 1, 3, 1)
    summary = read(BASE + '_completed')
    assert summary['all_phases_complete'] and summary['maximum_workers'] == 3
    assert summary['config'] == source(DATA / (CONFIG + '.json'))
    assert summary['coordinator'] == source(ROOT / 'dembele/pari/553_dyadic_staged_archiving_coordinator.py')
    assert summary['interruption_controls'] == []
    groups = list(expected_groups())
    specs = [spec for group in groups for spec in group]
    assert [row['key'] for row in summary['jobs']] == [spec['key'] for spec in specs]
    assert summary['completed_jobs'] == len(specs)
    packets, byphase, events, receipt_paths = {}, defaultdict(list), [], set()
    peak_store = 0
    for spec, item in zip(specs, summary['jobs']):
        stem = BASE + '_' + spec['key']
        args = ['--config', CONFIG, '--output', stem]
        for key, value in spec.items():
            args += ['--' + key, str(value)]
        row, packet = receipt(item['receipt'], item['metadata'], DRIVER, args)
        receipt_paths.add(item['receipt']['path'])
        assert item['metadata'] == source(DATA / (stem + '.json'))
        expected = dict(config=CONFIG, phase=None, key=None, step=None, digit=None,
                        first=None, last=None, chart=None, order=None)
        expected.update(spec)
        assert packet['request'] == expected and packet['driver'] == source(DRIVER)
        assert packet['config'] == summary['config'] and packet['milestone'] == 'D132'
        assert packet['working_precision_pi'] == P and packet['harmonic_basis_column'] == 0
        assert packet['historical_payload_hashes_are_not_retained_source_claims']
        phase_certificate(spec, packet['certificates'], history)
        assert item['seconds'] == row['wall_seconds'] <= 180
        assert item['peak_rss_bytes'] == packet['peak_rss_bytes'] <= RSS_CAP
        peak_store = max(peak_store, packet['maximum_observed_store_bytes'])
        begin, end = item['coordinator_interval']
        assert 0 <= begin <= end
        events += [(begin, 1, packet['peak_rss_bytes']), (end, -1, -packet['peak_rss_bytes'])]
        byphase[spec['phase']].append(row['wall_seconds'])
        packets[spec['key']] = packet
    used, rss, max_used, max_rss = 0, 0, 0, 0
    for _, change, delta in sorted(events):
        used += change
        rss += delta
        assert 0 <= used <= 3 and 0 <= rss <= 6 * (1 << 30)
        max_used, max_rss = max(max_used, used), max(max_rss, rss)
    assert used == rss == 0
    assert summary['sum_recorded_job_seconds'] == sum(item['seconds'] for item in summary['jobs'])
    assert summary['max_single_job_seconds'] == max(item['seconds'] for item in summary['jobs'])
    assert summary['max_single_job_peak_rss_bytes'] == max(item['peak_rss_bytes'] for item in summary['jobs'])
    pause = read('dyadic_staged_P6400_col00_pause_d133')
    assert pause['completed_phases'] == 176 and pause['boundary'] == 'before low_begin_000'
    assert pause['checkpoint_at_pause'] == history[0]
    assert pause['checkpoint_payload_hashes_are_historical_after_resume']
    assert pause['configuration'] == summary['config'] and pause['coordinator'] == summary['coordinator']
    for previous, item in zip(pause['receipts'], summary['jobs'][:176]):
        assert previous == {key: item[key] for key in ('key', 'receipt', 'metadata')}
        assert item['reused_receipt']
    archive_driver = ROOT / 'dembele/pari/551_dyadic_staged_metadata_archive.py'
    assert len(summary['metadata_archives']) == 97
    archive_seconds = []
    for step, item in enumerate(summary['metadata_archives']):
        label = f'sweep_finish_{step:03d}'
        stem = BASE + '_archive_' + label
        args = ['--config', CONFIG, '--label', label, '--output', stem]
        row, packet = receipt(item['receipt'], item['metadata'], archive_driver, args)
        receipt_paths.add(item['receipt']['path'])
        cert = packet['certificates']
        assert cert['archive'] == source(STORE / ('archive_' + label + '.json'))
        archive = envelope('archive_' + label + '.json')
        assert cert['archived_records'] == len(archive['items'])
        assert cert['external_records_preserved'] and cert['occupied_bytes'] < CAP
        archive_seconds.append(row['wall_seconds'])
    expected_archived = {f"done_{spec['key']}.json" for spec in specs
                         if spec['phase'] not in ('verify-begin', 'verify', 'cm-begin', 'cm', 'coarse', 'seal')}
    assert archived == expected_archived
    actual_paths = {str(path.resolve()) for path in DATA.glob(BASE + '*_attempt*.job.json')}
    assert actual_paths == receipt_paths, 'unexpected, duplicate, failed, or unreviewed attempts'
    observed_phases = {key: {'jobs': len(values), 'summed_seconds': sum(values), 'maximum_seconds': max(values)}
                       for key, values in sorted(byphase.items())}
    inventory = read('dyadic_staged_lifetime_inventory_d132')['certificates']['schedules'][1]
    assert inventory['precision_pi'] == P and inventory['maximum_bound']['total_bytes'] == 973167872
    assert peak_store <= inventory['maximum_bound']['total_bytes'] < CAP
    return packets, receipt_paths, {
        'actual_phases': len(specs), 'metadata_archive_jobs': 97, 'corrections': 96,
        'seed_low_digits': [200, 400, 600, 800], 'phase_timings': observed_phases,
        'summed_actual_job_seconds': summary['sum_recorded_job_seconds'],
        'summed_archive_seconds': sum(archive_seconds), 'resumed_coordinator_wall_seconds': summary['wall_seconds'],
        'resumed_initializer_receipts': 176, 'maximum_measured_job_RSS_bytes': summary['max_single_job_peak_rss_bytes'],
        'maximum_recorded_phase_concurrency': max_used, 'conservative_sum_of_concurrent_measured_peaks_bytes': max_rss,
        'RAM_is_measured_admission_not_OS_hard_limit': True,
        'maximum_observed_working_store_bytes': peak_store, 'proved_inventory_bound_bytes': 973167872,
        'full_original_weighted_equation_scalars': N * P * 8, 'all_fixed_masses': N,
        'complete_CM_scalars': 17 * 2 * P * 8, 'coarse_values': 68,
        'coarse_errors_beta': [12832, 12848, 12832, 12864],
        'new_uniform_state_binary_retained': False}


def audit_review():
    plan_stem = 'dyadic_precision6400_audit_plan_d133'
    plan, summary = read(plan_stem), read(plan_stem + '_completed')
    assert plan['milestone'] == summary['milestone'] == 'D133'
    assert plan['requires_completed_and_sealed_actual_column']
    assert summary['completed_jobs'] == len(plan['jobs']) == 24 and summary['worker_limit'] == 3
    assert summary['plan'] == source(DATA / (plan_stem + '.json'))
    assert summary['coordinator'] == source(ROOT / 'dembele/pari/run_d133_audits.py')
    states, charts, ordinary_states, ordinary_charts, horner = [], [], [], [], []
    totals, receipt_paths = Counter(), set()
    for spec, item in zip(plan['jobs'], summary['jobs']):
        assert item['stem'] == spec['stem']
        assert spec['driver'] == 'dembele/pari/556_dyadic_precision6400_independent.py'
        args = spec['args'] + ['--output', spec['stem']]
        row, packet = receipt(item['receipt'], item['metadata'], ROOT / spec['driver'], args)
        receipt_paths.add(item['receipt']['path'])
        assert packet['milestone'] == 'D133' and packet['production_arithmetic_not_imported']
        assert packet['peak_rss_bytes'] <= RSS_CAP and packet['phase'] == spec['args'][1]
        assert item['seconds'] == row['wall_seconds'] and item['peak_rss_bytes'] == packet['peak_rss_bytes']
        cert = packet['certificates']
        phase = packet['phase']
        if phase == 'states':
            states += list(range(cert['first_state'], cert['last_state'] + 1))
            for key in ('complete_old_weighted_overlap_scalars', 'exact_masses', 'final_residual_zero_rows'):
                totals[key] += cert[key]
        elif phase == 'ordinary-state':
            ordinary_states.append(cert['state'])
            assert cert['degrees'] == [1, 2, 3] and not cert['complete_operator_independently_recomputed']
            totals['ordinary_state_scalars'] += cert['ordinary_original_scalar_checks']
        elif phase == 'cm':
            charts += list(range(cert['first_chart'], cert['last_chart'] + 1))
            totals['old_CM_overlap_scalars'] += cert['old_CM_overlap_scalars']
            totals['coarse_old_overlaps'] += cert['coarse_old_overlaps']
            assert cert['new_coarse_errors_beta'] == [12832, 12848, 12832, 12864]
        elif phase == 'ordinary-cm':
            ordinary_charts.append(cert['chart'])
            assert cert['degrees'] == [1, 2, 3] and not cert['complete_CM_operator_independently_recomputed']
            totals['ordinary_CM_scalars'] += cert['ordinary_CM_scalar_checks']
        elif phase == 'coarse-horner':
            horner.append((cert['chart'], cert['order']))
            assert cert['independent_integer_quotient_Horner_matches_direct_sum']
            totals['independent_Horner_beta_scalars'] += cert['complete_beta_scalar_checks']
        else:
            raise AssertionError(phase)
    assert states == list(range(N)) and charts == list(range(17))
    assert ordinary_states == [0, 83, 173] and ordinary_charts == [0, 8, 16]
    assert horner == [(ci, order) for ci in (0, 8, 16) for order in (0, 3)]
    assert totals == Counter(complete_old_weighted_overlap_scalars=4454400, exact_masses=174,
                             final_residual_zero_rows=174, ordinary_state_scalars=72,
                             old_CM_overlap_scalars=870400, coarse_old_overlaps=68,
                             ordinary_CM_scalars=72, independent_Horner_beta_scalars=96)
    return receipt_paths, dict(totals) | {
        'audit_jobs': 24, 'sampled_not_complete_independent_operators': True,
        'complete_old_overlap_checks_are_distinct_from_original_equation_samples': True,
        'audit_coordinator_wall_seconds': summary['wall_seconds']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        packet = json.loads(OUT.read_text())
        assert packet['status'] == 'pass' and packet['independent_finite_review_complete']
        checked(packet['sources'])
        print('PASS|557_DYADIC_PRECISION6400_REVIEW', flush=True)
        return
    assert not OUT.exists(), 'fixed review creation is not repeatable'
    tick = time.monotonic()
    prior = read('dyadic_staged_integration_review_d132')
    assert prior['one_P6400_column_admitted_after_completed_review'] and not prior['full_bank_launch_admitted']
    checked(prior['sources'])
    assert len(prior['sources']) == 18589
    completion = read('dyadic_staged_integration_completion_d132')
    controls = read('dyadic_continuation_controls_d133')
    assert controls['kind'] == 'nonmathematical_completion_controls'
    assert controls['passing_fixture_controls'] == 6 and controls['mathematical_driver_jobs_launched'] == 0
    checked(controls['sources'])
    history, archived, store = inspect_store()
    packets, actual_receipts, execution = execution_review(history, archived)
    audit_receipts, independent = audit_review()
    seal = packets['seal']
    assert seal['certificate'] == {'original_weighted_fixed_point': True, 'all_fixed_masses': True}
    assert seal['weighted_input'] and seal['state_file'] == source(STORE / history[-1]['state']['name'])
    all_inputs = actual_receipts | audit_receipts
    observed = {str(path.resolve()) for path in DATA.glob('*d133*_attempt*.job.json')
                if not path.name.startswith(OUT.stem)}
    assert observed == all_inputs, 'unreviewed D133 receipt exists'
    read('dyadic_precision6400_sources_d133')
    PATHS.add(ROOT / 'dembele/certificates/dyadic-precision6400-d133.md')
    for name in ('556_dyadic_precision6400_independent.py', 'run_d133_audits.py', 'run_d133_completion.py'):
        PATHS.add(ROOT / 'dembele/pari' / name)
    source_records = [source(path) for path in sorted(PATHS)]
    known = {row['path']: row['sha256'] for row in source_records}
    assert all(known[row['path']] == row['sha256'] for row in prior['sources'])
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert peak_rss <= RSS_CAP
    result = {
        'status': 'pass', 'milestone': 'D133', 'independent_finite_review_complete': True,
        'production_arithmetic_not_imported': True, 'inherited_D132_hashes_preserved': len(prior['sources']),
        'passing_input_jobs': len(all_inputs), 'failed_bounded_jobs': 0,
        'nonmathematical_continuation_fixture_controls': 6,
        'certificates': {'execution': execution, 'independent': independent, 'store': store},
        'actual_harmonic_precision_increased': True, 'full_bank_precision_pi': 800,
        'column_precisions': {'0': 6400, '1': 1600}, 'full_bank_launch_admitted': False,
        'positive_exact_zero_proved': False, 'candidate_identification_proved': False,
        'arithmetic_cover_identification_proved': False, 'field_polynomial_constructed': False,
        'P10552_is_conditional_sufficient_not_certified_or_necessary': True,
        'wall_seconds': time.monotonic() - tick, 'peak_rss_bytes': peak_rss, 'sources': source_records}
    with OUT.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print('D133_REVIEW_SOURCES|' + str(len(source_records)), flush=True)
    print('PASS|557_DYADIC_PRECISION6400_REVIEW', flush=True)


if __name__ == '__main__':
    main()
