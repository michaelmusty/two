"""D129 fixed finite review of actual P=3200 refinement and bounded file lifetimes."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
SCRATCH = DATA / 'dyadic_streamed_scratch_col00_d129'
OUT = DATA / 'dyadic_precision3200_review_d129.json'
PATHS, CACHE = set(), {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        sha = hashlib.sha256()
        with path.open('rb') as f:
            while raw := f.read(1 << 20):
                sha.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': sha.hexdigest()}
    return CACHE[path]


def checked(rows):
    for row in rows:
        assert source(row['path']) == row, row['path']


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    result = json.loads(path.read_text())
    assert result['status'] == 'pass'
    return result


def payload_size(row):
    layout = row['layout']
    P, states, count = layout['precision_pi'], layout['states'], layout['moments']
    shift = layout['binary_shift']
    assert P == 3200 and states > 0 and count > 0 and 0 <= shift < 400
    if layout['weighted']:
        assert count == P and shift == 0
        row_size = sum((max(0, -((i - (P if k <= 32 else P - k)) // 8)) + 7) // 8
                       for k in range(P) for i in range(8))
    else:
        row_size = count * 8 * ((400 - shift + 7) // 8)
    assert row['bytes'] == row_size * states
    assert row['maximum_serialized_row_bytes'] == row_size
    assert row['full_size_reserved_before_writes']
    return row_size * states


def lifetime_review(pilot):
    inv = read('dyadic_streamed_inventory_d129')
    assert inv['scratch_limit_bytes'] == 2 * (1 << 30)
    assert inv['conservative_total_bytes'] == sum(inv['conservative_simultaneous_slots'].values()) == 1510359376
    assert inv['full_output_reservations_serialized_by_lock_and_hard_byte_check']
    assert inv['rows_written_concurrently_within_reserved_file_lengths']
    assert inv['maximum_serialized_state_row_bytes'] == 1280000
    assert inv['fixed_low_system_shape'] == [174, 32, 1, 8]
    assert inv['complete_long_state_bank_decoding_disabled']
    receipt_records = [row for row in pilot['sources'] if row['path'].endswith('.job.json')]
    assert len(receipt_records) == 1905
    ordered = []
    for record in receipt_records:
        checked([record])
        job = json.loads(Path(record['path']).read_text())
        assert job['status'] == 'pass' and Path(job['driver']['path']).name == '528_dyadic_streamed_precision3200.py'
        command = job['command']
        packet = read(command[command.index('--output') + 1])
        assert packet['checkpoint_payloads_prospectively_transient']
        assert packet['scratch_limit_bytes'] == 2 * (1 << 30)
        for key in ('scratch_bytes_before', 'scratch_bytes_after'):
            assert 0 <= packet[key] <= inv['scratch_limit_bytes']
        checked([job['driver'], job['log']])
        bindings = [json.loads(line.split('|', 1)[1]) for line in Path(job['log']['path']).read_text().splitlines()
                    if line.startswith('PHASE_METADATA|')]
        assert bindings == [source(DATA / (command[command.index('--output') + 1] + '.json'))]
        ordered.append((record, packet))
    index = {row['path']: i for i, (row, _) in enumerate(ordered)}
    events = sorted(DATA.glob('dyadic_streamed_retirement_d129_*.json'))
    assert len(events) == 103
    overhead = sum((SCRATCH / name).stat().st_size for name in ('OWNER.json', '.write.lock', '.coordinator.lock'))
    cursor, known, live, retired, peaks = 0, {}, {}, {}, []
    maximum_row = 0
    for barrier, path in enumerate(events, 1):
        event = read(path.stem)
        assert event['barrier'] == barrier and event['retired_payload_hashes_are_history_not_retained_sources']
        checked([event['coordinator'], event['anchor_receipt']])
        stop = index[event['anchor_receipt']['path']] + 1
        assert cursor < stop <= len(ordered)
        for _, packet in ordered[cursor:stop]:
            for payload in packet['new_payloads']:
                file = payload['source']
                key = file['path']
                assert Path(key).parent == SCRATCH and key not in known
                size = payload_size(payload)
                known[key] = live[key] = {'source': file, 'bytes': size}
                maximum_row = max(maximum_row, payload['maximum_serialized_row_bytes'])
            for file in packet['checkpoint_files']:
                assert file['path'] in live and live[file['path']]['source'] == file
        cursor = stop
        predicted = overhead + sum(row['bytes'] for row in live.values())
        assert predicted == event['before_scratch_bytes'] and predicted < inv['conservative_total_bytes']
        peaks.append(predicted)
        keep = {row['source']['path']: row for row in event['keep']}
        drop = {row['source']['path']: row for row in event['retire']}
        assert not keep.keys() & drop.keys() and live == keep | drop
        assert not retired.keys() & drop.keys()
        retired.update(drop)
        live = keep
    assert cursor == 1905 and len(known) == 1954 and len(retired) == 1950 and len(live) == 4
    assert maximum_row == 1280000
    for key, row in live.items():
        checked([row['source']])
        assert Path(key).stat().st_size == row['bytes']
    for key in retired:
        assert not Path(key).exists()
    assert {str(path) for path in SCRATCH.glob('*.bin')} == set(live)
    assert pilot['retired_payload_count'] == 1950
    assert pilot['retired_payload_bytes'] == sum(row['bytes'] for row in retired.values())
    assert pilot['sealed_payload_bytes'] == sum(row['bytes'] for row in live.values()) == 558829536
    sealpath = SCRATCH / 'SEALED.json'
    PATHS.add(sealpath)
    seal = json.loads(sealpath.read_text())
    assert seal['all_remaining_files_now_frozen'] and seal['verified_checkpoint'] == pilot['verified_checkpoint']
    assert seal['weighted_checkpoint'] == pilot['weighted_checkpoint']
    checked([seal['verified_checkpoint'], seal['weighted_checkpoint'], seal['final_retirement']])
    sealed = sum(p.stat().st_size for p in SCRATCH.iterdir())
    assert pilot['sealed_scratch_bytes'] == sealed
    assert pilot['maximum_observed_scratch_bytes'] == max(peaks + [sealed])
    PATHS.update(SCRATCH.iterdir())
    return {'phase_payload_records': 1954, 'retired_payloads': 1950, 'retained_payloads': 4,
        'retirement_barriers': 103, 'all_payload_sizes_and_live_sets_independently_replayed': True,
        'full_output_reservations_counted_at_every_barrier': True,
        'maximum_serialized_state_row_bytes': maximum_row,
        'conservative_scratch_bound_bytes': inv['conservative_total_bytes'],
        'scratch_limit_bytes': inv['scratch_limit_bytes'],
        'maximum_observed_scratch_bytes': pilot['maximum_observed_scratch_bytes'],
        'sealed_payload_bytes': 558829536, 'sealed_total_bytes': sealed,
        'retired_payload_bytes': pilot['retired_payload_bytes'],
        'retired_hashes_not_treated_as_retained_sources': True}


def arithmetic_review():
    pilot = read('dyadic_streamed_pilot_P3200_col00_d129')
    assert pilot['completed_phases'] == 1905 and pilot['state_arithmetic_phases'] == 1904
    assert pilot['writer_control_phases'] == 1 and pilot['correction_steps'] == 48
    assert pilot['working_precision_pi'] == 3200 and pilot['harmonic_basis_column'] == 0
    assert pilot['maximum_workers'] == 3 and pilot['operator_chunk_size'] == 6 and pilot['low_rhs_chunk_size'] == 29
    writer = read('dyadic_streamed_writer_control_d129')['certificate']
    assert writer['interleaved_reserved_files_checked'] == 2 and writer['direct_byte_comparisons'] == 11376
    assert writer['wrong_length_row_rejections'] == writer['oversized_reservation_rejections'] == 1
    state = read('dyadic_streamed_P3200_col00_verified_d129')
    checked(state['checkpoint_files'])
    cert = state['certificate']
    assert cert['original_full_residual_zero'] and cert['actual_new_precision_pi'] == 3200
    assert cert['scalar_coefficients_checked'] == cert['old_extended_scalar_overlaps_checked'] == 4454400
    assert cert['old_low_scalar_overlaps_checked'] == 2227200 and cert['exact_masses_checked'] == 174
    assert cert['full_residual_uses_different_polynomial_backend_from_lift']
    low = read('dyadic_streamed_P3200_col00_seed_low_d129')
    timed = [row for row in low['timings'] if row['operation'] == 'streamed_existing_factor_low_solve']
    assert len(timed) == 1 and timed[0]['modulus_bits'] == 400
    assert timed[0]['factor_blocks_decoded'] == 2452 and not timed[0]['larger_factor_built']
    assert timed[0]['higher_precision_original_sparse_scalar_checks'] == timed[0]['exact_residual_divisions_checked'] == 44544
    cm = read('dyadic_CM_P3200_col00_d129')
    checked(cm['checkpoint_files'])
    assert cm['CM_charts_checked'] == 17 and cm['composed_child_maps_checked'] == 34
    assert cm['CM_moment_scalar_coefficients'] == 870400 and cm['old_CM_moment_scalar_coefficients_checked'] == 435200
    assert cm['old_coarse_values_checked'] == 68 and cm['coarse_error_beta'] == [6432, 6448, 6432, 6464]
    assert cm['chunked_moment_payload_bytes'] == sum(Path(row['path']).stat().st_size for row in cm['checkpoint_files']) == 43520000
    assert len(cm['moment_chunks']) == 6 and not cm['duplicate_assembled_binary_written']
    audits = {}
    for phase in ('states', 'weighted', 'seed_final'):
        packet = read('dyadic_P3200_audit_' + phase + '_d129')
        assert packet['production_arithmetic_not_imported']
        audits[phase] = packet['certificates']
    assert audits['states']['production_full_original_residual_scalar_checks'] == 4454400
    assert audits['states']['old_P1600_low_scalar_overlaps'] == 2227200
    assert audits['states']['child_column_divisibility_checks'] == 348
    assert audits['states']['independent_original_recurrence_scalar_checks'] == 96
    assert audits['states']['complete_disjoint_sweeps_checked'] == 101
    assert audits['weighted']['final_weighted_reference_scalar_checks'] == 4454400
    assert audits['weighted']['final_scaled_residual_scalar_checks'] == 45936
    assert audits['weighted']['checkpoint_metadata_checked'] == 49
    assert audits['weighted']['recorded_correction_gains_checked'] == 48
    assert not audits['weighted']['retired_intermediate_payloads_replayed']
    assert audits['seed_final']['independent_high_seed_scalar_checks'] == 24
    assert audits['seed_final']['independent_high_seed_degrees'] == [1600, 2399, 3199]
    assert audits['seed_final']['independent_recurrence_blocks'] == 16
    assert not audits['seed_final']['retired_production_seed_payloads_replayed']
    stops = (400, 800, 1200, 1600, 2000, 2399, 2799, 3199)
    audit_bytes = 0
    for branch in (0, 1):
        before = 0
        for block, stop in enumerate(stops):
            packet = read(f'dyadic_P3200_audit_seed_b{branch}_k{block:02d}_d129')
            assert packet['production_arithmetic_not_imported']
            checked(packet['checkpoint_files'])
            assert len(packet['checkpoint_files']) == 1
            size = Path(packet['checkpoint_files'][0]['path']).stat().st_size
            assert size == 1600 * 8 * 25
            audit_bytes += size
            row = packet['certificates']
            assert row['branch'] == branch and row['block'] == block
            assert row['first_input_degree'] == before and row['last_degree'] == stop
            assert row['recurrence_steps'] == stop - before and row['coefficient_count'] == 1600
            before = stop
    coarse = []
    for first, last in ((0, 5), (6, 11), (12, 16)):
        packet = read(f'dyadic_P3200_audit_coarse_c{first:02d}_{last:02d}_d129')
        assert packet['production_arithmetic_not_imported']
        row = packet['certificates']
        assert row['first_chart'] == first and row['last_chart'] == last
        assert row['independent_coarse_values_checked'] == row['old_coarse_values_checked'] == 4 * (last - first + 1)
        coarse.append(row)
    assert sum(row['independent_coarse_values_checked'] for row in coarse) == 68
    assert sum(row['independent_CM_recurrence_scalar_checks'] for row in coarse) == 72
    assert sum(row['old_CM_scalar_overlaps'] for row in coarse) == 435200
    assert sum(row['new_CM_scalar_coefficients'] for row in coarse) == 870400
    assert audit_bytes == 5120000
    audits['coarse'] = coarse
    return pilot, {'working_precision_pi': 3200, 'actual_harmonic_column': 0,
        'original_residual_scalar_checks': 4454400, 'CM_scalar_coefficients': 870400,
        'coarse_error_beta': [6432, 6448, 6432, 6464], 'independent_audits': audits,
        'retained_independent_seed_checkpoint_bytes': audit_bytes,
        'new_factorization_required': False, 'writer_control': writer}


def build():
    prior = read('dyadic_selective_scaling_review_d128')
    assert prior['control_review_complete'] and len(prior['sources']) == 9648
    checked(prior['sources'])
    for stem in ('dyadic_selective_scaling_review_d128_attempt01', 'dyadic_selective_scaling_review_d128_recheck01'):
        job = read(stem + '.job')
        checked(job['sources'] + [job['driver'], job['log']])
    pilot, arithmetic = arithmetic_review()
    storage = lifetime_review(pilot)
    downstream = read('dyadic_precision3200_checks_d129')
    assert downstream['completed_check_jobs'] == 29 and downstream['maximum_workers'] == 3
    assert downstream['prior_state_coordinator_lock_acquired']
    checked(downstream['sources'])
    for row in downstream['jobs'].values():
        checked([row['receipt'], row['output']])
    PATHS.update([Path(__file__), ROOT / 'dembele/certificates/dyadic-precision3200-d129.md',
        DATA / 'dyadic_precision3200_sources_d129.json', ROOT / 'dembele/pari/run_d129_finish.py'])
    jobs, categories, measured_peaks = [], {}, []
    for path in sorted(DATA.glob('*d129*')):
        if path.is_dir() or path.name.startswith('dyadic_precision3200_review_d129'):
            continue
        PATHS.add(path)
        if path.suffix != '.json':
            if path.suffix == '.log':
                assert path.with_suffix('.job.json').exists()
            continue
        packet = json.loads(path.read_text())
        checked([row for row in packet.get('sources', []) if isinstance(row, dict) and 'sha256' in row])
        if 'peak_rss_bytes' in packet:
            measured_peaks.append(packet['peak_rss_bytes'])
        if not path.name.endswith('.job.json'):
            continue
        assert packet['status'] == 'pass' and packet['exit_code'] == 0
        assert packet['timeout_seconds'] == 180 and packet['timeout_terminates_process_group']
        checked([packet['driver'], packet['log']])
        driver = Path(packet['driver']['path']).name
        categories[driver] = categories.get(driver, 0) + 1
        jobs.append({'receipt': path.name, 'driver': driver, 'wall_seconds': packet['wall_seconds']})
    assert categories == {'528_dyadic_streamed_precision3200.py': 1905,
        '530_dyadic_chunked_CM_precision3200.py': 7, '531_dyadic_precision3200_independent.py': 22}, categories
    statistics = {'passed': len(jobs), 'failed': 0,
        'sum_wall_seconds': sum(row['wall_seconds'] for row in jobs),
        'maximum_wall_seconds': max(row['wall_seconds'] for row in jobs),
        'maximum_single_process_peak_rss_bytes': max(measured_peaks)}
    ledger = json.loads((DATA / 'dyadic_precision3200_sources_d129.json').read_text())
    assert ledger['execution_status'] == 'complete'
    for key, value in statistics.items():
        assert abs(ledger['bounded_input_jobs'][key] - value) < 1e-6, key
    report = (ROOT / 'dembele/certificates/dyadic-precision3200-d129.md').read_text()
    assert 'Draft while execution' not in report and 'Execution is in progress' not in report
    manifest = [source(path) for path in sorted(PATHS)]
    assert {(row['path'], row['sha256']) for row in prior['sources']} <= {(row['path'], row['sha256']) for row in manifest}
    return {'status': 'pass', 'milestone': 'D129', 'independent_finite_review_complete': True,
        'production_arithmetic_not_imported_by_reviewer': True, 'inherited_D128_hashes_preserved': 9648,
        'arithmetic_certificates': arithmetic, 'storage_certificates': storage,
        'bounded_input_jobs': jobs, 'input_job_categories': categories, 'input_job_statistics': statistics,
        'actual_column_at_precision_3200': 0, 'other_column_at_precision_1600': 1,
        'full_bank_precision_pi': 800, 'positive_exact_quadric_vanishing_proved': False,
        'candidate_identification_proved': False, 'target_field_polynomial_constructed': False,
        'complete_target_size_solve_costed': False, 'sources': manifest}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        result = json.loads(OUT.read_text())
        checked(result['sources'])
        assert result['status'] == 'pass' and result['independent_finite_review_complete']
    else:
        assert not OUT.exists()
        result = build()
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'sources': len(result['sources']), 'input_jobs': len(result['bounded_input_jobs'])}), flush=True)
    print('PASS|532_DYADIC_PRECISION3200_REVIEW', flush=True)
