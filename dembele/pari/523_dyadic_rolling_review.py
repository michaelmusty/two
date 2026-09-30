"""D127 fixed review, including an independent replay of scratch lifetimes.

Replay sizes and hashes from permanent phase/retirement records, never
pretend retired payloads remain available. Final arithmetic audits use
the retained final state and original equations, not iteration history.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
SCRATCH = DATA / 'dyadic_rolling_scratch_col01_d127'
OUT = DATA / 'dyadic_rolling_review_d127.json'
PATHS, CACHE = set(), {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        sha = hashlib.sha256()
        with path.open('rb') as f:
            while block := f.read(1 << 20):
                sha.update(block)
        CACHE[path] = {'path': str(path), 'sha256': sha.hexdigest()}
    return CACHE[path]


def checked(rows):
    for row in rows:
        assert source(row['path']) == row, row['path']


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def payload_size(packet, file):
    name = Path(file['path']).name
    assert Path(file['path']).parent == SCRATCH
    if name.endswith('_input.bin'):
        return 174 * packet['input_count'] * 8 * 25
    if name.endswith('_operator.bin'):
        return (packet['last_state'] - packet['first_state'] + 1) * packet['output_count'] * 8 * (
            (200 - packet['operator_power_of_two_shift'] + 7) // 8)
    if name.endswith('_correction.bin'):
        return 174 * packet['input_count'] * 8 * ((200 - packet['correction_power_of_two_shift'] + 7) // 8)
    if name.endswith('_residual.bin'):
        if packet['kind'] == 'verified':
            return 55680000
        return 174 * packet['active_moment_count'] * 8 * ((200 - packet['residual_power_of_two_shift'] + 7) // 8)
    assert name.endswith('_state.bin')
    return 55680000 if packet['kind'] in ('reconstructed', 'verified') else 28831800


def lifetime_review(pilot):
    inv = read('dyadic_rolling_inventory_d127')
    cap = 512 * (1 << 20)
    assert inv['scratch_limit_bytes'] == cap
    assert inv['conservative_total_bytes'] == sum(inv['conservative_simultaneous_slots'].values()) == 381534376
    assert inv['conservative_total_bytes'] < cap
    receipt_records = [r for r in pilot['sources'] if r['path'].endswith('.job.json')]
    assert len(receipt_records) == 228
    ordered = []
    for record in receipt_records:
        checked([record])
        job = json.loads(Path(record['path']).read_text())
        assert job['status'] == 'pass' and Path(job['driver']['path']).name == '519_dyadic_rolling_precision_chunks.py'
        command = job['command']
        stem = command[command.index('--output') + 1]
        packet = read(stem)
        assert packet['checkpoint_payloads_prospectively_transient'] and packet['scratch_limit_bytes'] == cap
        for key in ('scratch_bytes_before', 'scratch_bytes_after'):
            assert 0 <= packet[key] <= cap
        checked([job['driver'], job['log']])
        bindings = [json.loads(line.split('|', 1)[1]) for line in Path(job['log']['path']).read_text().splitlines()
                    if line.startswith('PHASE_METADATA|')]
        assert bindings == [source(DATA / (stem + '.json'))]
        ordered.append((record, packet))
    index = {row['path']: i for i, (row, _) in enumerate(ordered)}
    live, known, cursor, peaks, retired = {}, {}, 0, [], {}
    # Only these empty locks and the immutable owner predate the final seal.
    overhead = sum((SCRATCH / name).stat().st_size for name in ('OWNER.json', '.write.lock', '.coordinator.lock'))
    events = sorted(DATA.glob('dyadic_rolling_retirement_d127_*.json'))
    assert len(events) == 54
    for number, path in enumerate(events, 1):
        event = read(path.stem)
        checked([event['coordinator'], event['anchor_receipt']])
        assert event['barrier'] == number and event['retired_payload_hashes_are_history_not_retained_sources']
        stop = index[event['anchor_receipt']['path']] + 1
        assert cursor < stop <= len(ordered)
        for _, packet in ordered[cursor:stop]:
            for file in packet['checkpoint_files']:
                record = {'source': file, 'bytes': payload_size(packet, file)}
                key = file['path']
                if key in known:
                    assert known[key] == record and key in live
                else:
                    known[key] = record
                    live[key] = record
        cursor = stop
        predicted = overhead + sum(row['bytes'] for row in live.values())
        assert predicted == event['before_scratch_bytes'] and predicted < inv['conservative_total_bytes']
        peaks.append(predicted)
        keep = {row['source']['path']: row for row in event['keep']}
        drop = {row['source']['path']: row for row in event['retire']}
        assert not keep.keys() & drop.keys() and live == keep | drop
        assert all(key not in retired for key in drop)
        retired.update(drop)
        live = keep
    assert cursor == 228 and len(known) == 252 and len(live) == 4 and len(retired) == 248
    assert pilot['retired_payload_count'] == len(retired)
    assert pilot['retired_payload_bytes'] == sum(row['bytes'] for row in retired.values())
    for key, row in live.items():
        checked([row['source']])
        assert Path(key).stat().st_size == row['bytes']
    for key in retired:
        assert not Path(key).exists()
    assert {str(p) for p in SCRATCH.glob('*.bin')} == set(live)
    sealpath = SCRATCH / 'SEALED.json'
    PATHS.add(sealpath)
    seal = json.loads(sealpath.read_text())
    assert seal['all_remaining_files_now_frozen'] and seal['verified_checkpoint'] == pilot['verified_checkpoint']
    assert seal['weighted_checkpoint'] == pilot['weighted_checkpoint']
    checked([seal['verified_checkpoint'], seal['weighted_checkpoint'], seal['final_retirement']])
    sealed = sum(p.stat().st_size for p in SCRATCH.iterdir())
    assert pilot['sealed_scratch_bytes'] == sealed
    assert pilot['sealed_payload_bytes'] == sum(row['bytes'] for row in live.values()) == 140237736
    peak = max(peaks + [sealed])
    assert pilot['maximum_observed_scratch_bytes'] == peak
    PATHS.update(SCRATCH.iterdir())
    return {'phase_payload_records': len(known), 'retired_payloads': len(retired),
        'retained_payloads': len(live), 'retirement_barriers': 54,
        'all_phase_payload_sizes_independently_recomputed': True,
        'all_live_sets_and_barrier_byte_counts_independently_replayed': True,
        'conservative_scratch_bound_bytes': inv['conservative_total_bytes'],
        'scratch_limit_bytes': cap, 'maximum_observed_scratch_bytes': peak,
        'sealed_payload_bytes': 140237736, 'sealed_total_bytes': sealed,
        'retired_payload_bytes': pilot['retired_payload_bytes'],
        'retired_payloads_not_treated_as_retained_sources': True}


def arithmetic_review():
    pilot = read('dyadic_rolling_pilot_P1600_col01_d127')
    assert pilot['completed_phases'] == 228 and pilot['correction_steps'] == 24
    assert pilot['working_precision_pi'] == 1600 and pilot['harmonic_basis_column'] == 1
    assert pilot['maximum_workers'] == 3 and pilot['chunk_size'] == 29
    state = read('dyadic_rolling_P1600_col01_verified_d127')
    checked(state['checkpoint_files'])
    cert = state['certificate']
    assert cert['original_full_residual_zero'] and cert['scalar_coefficients_checked'] == 2227200
    assert cert['old_low_scalar_overlaps_checked'] == 1113600 and cert['old_extended_scalar_overlaps_checked'] == 2227200
    assert cert['exact_masses_checked'] == 174 and cert['full_residual_uses_different_polynomial_backend_from_lift']
    cm = read('dyadic_rolling_CM_P1600_col01_d127')
    checked(cm['checkpoint_files'])
    assert cm['coarse_error_beta'] == [3232, 3248, 3232, 3264]
    assert cm['CM_charts_checked'] == 17 and cm['CM_moment_scalar_coefficients'] == 435200
    assert cm['composed_child_maps_checked'] == 34 and cm['weighted_input_used']
    audits = {}
    for phase in ('states', 'seed', 'coarse', 'weighted'):
        packet = read(f'dyadic_rolling_audit_{phase}_d127')
        assert packet['production_arithmetic_not_imported']
        audits[phase] = packet['certificates']
    assert audits['states']['production_full_original_residual_scalar_checks'] == 2227200
    assert audits['states']['old_P800_low_scalar_overlaps'] == 1113600
    assert audits['states']['independent_original_recurrence_scalar_checks'] == 160
    assert audits['states']['child_column_divisibility_checks'] == 348
    assert audits['states']['complete_disjoint_sweeps_checked'] == 29
    assert audits['seed']['independent_high_seed_scalar_checks'] == 24
    assert not audits['seed']['retired_seed_extension_payloads_replayed']
    assert audits['coarse']['independent_coarse_values_checked'] == 68
    assert audits['coarse']['independent_CM_recurrence_scalar_checks'] == 72
    assert audits['coarse']['old_CM_scalar_overlaps'] == 217600
    assert audits['weighted']['final_weighted_reference_scalar_checks'] == 2227200
    assert audits['weighted']['final_scaled_residual_scalar_checks'] == 45936
    assert audits['weighted']['checkpoint_metadata_checked'] == 25
    assert not audits['weighted']['retired_intermediate_payloads_rechecked']
    reuse = {}
    for precision in (1600, 3200):
        packet = read(f'dyadic_factor_reuse_P{precision}_d127')
        row = packet['certificates']
        assert row['target_low_system_precision_pi'] == precision
        assert row['reused_factor_precision_pi'] == precision // 2
        assert row['original_sparse_scalar_equations_checked'] == 89088
        assert row['residual_scalar_coefficients_divisible_by_2_power'] == 89088
        assert row['exact_binary_divisor_exponent'] == precision // 16
        assert row['factor_blocks_decoded_for_two_solves'] == 2452
        assert not row['larger_factor_constructed'] and not row['actual_harmonic_precision_increased']
        assert row['known_full_precision_factor_scalar_comparisons'] == (89088 if precision == 1600 else 0)
        reuse[str(precision)] = row
    return pilot, {'actual_new_column': 1, 'working_precision_pi': 1600,
        'original_residual_scalar_checks': 2227200, 'coarse_error_beta': cm['coarse_error_beta'],
        'CM_scalar_coefficients': 435200, 'independent_audits': audits,
        'higher_precision_low_solution_with_existing_factor': reuse}


def build():
    prior = read('dyadic_resource_controls_review_d126')
    assert prior['resource_controls_review_complete'] and len(prior['sources']) == 8816
    checked(prior['sources'])
    for stem in ('dyadic_resource_controls_review_d126_attempt01', 'dyadic_resource_controls_review_d126_recheck01'):
        job = read(stem + '.job')
        checked(job['sources'] + [job['driver'], job['log']])
    PATHS.update([Path(__file__), ROOT / 'dembele/certificates/dyadic-rolling-pilot-d127.md',
        DATA / 'dyadic_rolling_sources_d127.json'])
    pilot, arithmetic = arithmetic_review()
    storage = lifetime_review(pilot)
    jobs, categories = [], {}
    for path in sorted(DATA.glob('*d127*')):
        if path.is_dir() or path.name.startswith('dyadic_rolling_review_d127'):
            continue
        PATHS.add(path)
        if path.suffix != '.json':
            if path.suffix == '.log':
                assert path.with_suffix('.job.json').exists()
            continue
        packet = json.loads(path.read_text())
        checked([r for r in packet.get('sources', []) if isinstance(r, dict) and 'sha256' in r])
        if not path.name.endswith('.job.json'):
            continue
        assert packet['status'] == 'pass' and packet['exit_code'] == 0
        assert packet['timeout_seconds'] == 180 and packet['timeout_terminates_process_group']
        checked([packet['driver'], packet['log']])
        driver = Path(packet['driver']['path']).name
        categories[driver] = categories.get(driver, 0) + 1
        jobs.append({'receipt': path.name, 'driver': driver, 'wall_seconds': packet['wall_seconds']})
    assert categories == {'519_dyadic_rolling_precision_chunks.py': 228,
        '521_dyadic_rolling_direct_CM.py': 1, '522_dyadic_rolling_independent.py': 4,
        '524_dyadic_factor_reuse_lift.py': 2}, categories
    manifest = [source(p) for p in sorted(PATHS)]
    assert {(r['path'], r['sha256']) for r in prior['sources']} <= {(r['path'], r['sha256']) for r in manifest}
    return {'status': 'pass', 'milestone': 'D127', 'independent_finite_review_complete': True,
        'production_arithmetic_not_imported_by_reviewer': True,
        'inherited_D126_hashes_preserved': 8816, 'arithmetic_certificates': arithmetic,
        'storage_certificates': storage, 'bounded_input_jobs': jobs, 'input_job_categories': categories,
        'two_actual_columns_at_precision_1600': [0, 1], 'full_bank_precision_pi': 800,
        'iteration_history_not_required_for_final_moment_certificate': True,
        'positive_exact_quadric_vanishing_proved': False, 'candidate_identification_proved': False,
        'target_field_polynomial_constructed': False, 'complete_target_size_solve_costed': False,
        'sources': manifest}


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
    print('PASS|523_DYADIC_ROLLING_REVIEW', flush=True)
