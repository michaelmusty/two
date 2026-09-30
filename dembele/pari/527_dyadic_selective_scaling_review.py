"""D128 fixed review of selective serial and P=3200 transport controls.

Preserve the previous mathematical audit. Recompute byte inventories and
control coverage without importing production arithmetic. No new actual
P=3200 column or complete target-size resource certificate is claimed.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_selective_scaling_review_d128.json'
PATHS, CACHE = set(), {}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        digest = hashlib.sha256()
        with path.open('rb') as f:
            while raw := f.read(1 << 20):
                digest.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': digest.hexdigest()}
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


def serial_review():
    total, references, peaks = 0, [], []
    assembly = read('dyadic_selective_serial_assembly_d128')
    row = assembly['certificates']
    assert len(row['streamed_outputs']) == 8
    assert row['scalar_checks'] == {'seed_old_low_scalars': 1113600,
        'weighted_projection_scalars': 2227200, 'old_extended_scalars': 2227200,
        'original_residual_scalars': 2227200, 'exact_masses': 174}
    assert row['full_original_maps_not_recomputed']
    packets = [assembly]
    for step, u, count in ((1, 800, 800), (12, 1163, 437), (24, 1559, 41)):
        packet = read(f'dyadic_selective_serial_prepare_step{step:02d}_d128')
        row = packet['certificates']
        assert (row['step'], row['before_pi'], row['input_count']) == (step, u, count)
        assert row['weighted_state_scalars_compared'] == 2227200
        assert row['correction_scalars_compared'] == 174 * count * 8
        assert row['original_low_sparse_scalar_checks'] == 44544
        assert len(row['streamed_outputs']) == 2
        packets.append(packet)
    weighted = 174 * sum((max(0, -((i - (1600 if k <= 32 else 1600 - k)) // 8)) + 7) // 8
                        for k in range(1600) for i in range(8))
    assert weighted == 28831800
    expected = {
        'seed_assembly': weighted, 'seed_low_assembly': weighted,
        'seed_residual': 174 * 800 * 8 * 13,
        'step01_residual': 174 * 767 * 8 * 12,
        'step12_residual': 174 * 404 * 8 * 7,
        'step24_residual': 174 * 33 * 8,
        'uniform_reconstruction': 55680000, 'original_residual': 55680000}
    for packet in packets:
        row = packet['certificates']
        assert not packet['actual_harmonic_precision_increased']
        assert not row['complete_long_bank_decoded'] and not row['new_binary_written']
        assert row['incremental_serialization_and_byte_comparison_only']
        assert row['maximum_long_state_rows_retained'] == 8
        assert row['fixed_low_bank_shape'] == [174, 32, 1, 8]
        for name, value in row['streamed_outputs'].items():
            checked([value['reference']])
            assert value['serialized_sha256'] == value['reference']['sha256']
            if row['phase'] == 'assembly':
                size = expected[name]
            elif name == 'state':
                size = weighted
            else:
                assert name == 'correction'
                size = 174 * row['input_count'] * 8 * ((row['working_modulus_bits'] + 7) // 8)
            assert value['bytes_compared_directly'] == Path(value['reference']['path']).stat().st_size == size
            assert value['states'] == 174 and value['maximum_serialized_row_bytes'] * 174 == size
            total += size
            references.append(value['reference'])
        peaks.append(packet['peak_rss_bytes'])
    assert len(references) == 14 and len({r['path'] for r in references}) == 14
    assert total == 305582280
    return {'serialized_outputs': 14, 'bytes_compared_directly': total,
        'all_reference_hashes_and_lengths_checked': True, 'original_low_sparse_scalar_checks': 133632,
        'maximum_single_process_peak_rss_bytes': max(peaks),
        'complete_new_refinement_or_file_writer_executed': False}


def transport_review():
    comparisons = old = 0
    timings, peaks = {}, []
    for phase in ('extend', 'full', 'rhs'):
        timings[phase] = {'ADAPTIVE': 0.0, 'GMP': 0.0}
        for first, last in ((0, 5), (83, 88), (168, 173)):
            packet = read(f'dyadic_P3200_transport_{phase}_e{first:03d}_{last:03d}_d128')
            row = packet['certificates']
            assert row['phase'] == phase and row['working_precision_pi'] == 3200
            assert row['first_state'] == first and row['last_state'] == last
            count, rows = (1600 if phase == 'extend' else 3200), (33 if phase == 'rhs' else 3200)
            assert row['input_moment_count'] == count and row['output_moment_count'] == rows
            assert row['complete_backend_scalar_comparisons'] == 6 * rows * 8
            assert row['old_P1600_actual_scalar_overlaps'] == (76800 if phase == 'extend' else 0)
            assert row['input_kind'] == ('actual_P1600_canonical_lift_with_exact_masses' if phase == 'extend' else 'deterministic_dense_synthetic')
            assert not row['actual_harmonic_precision_increased'] and not row['complete_larger_solve_costed']
            assert not row['complete_original_state_coverage']
            assert {(r['state'], r['backend']) for r in row['state_timings']} == {
                (e, backend) for e in range(first, last + 1) for backend in ('ADAPTIVE', 'GMP')}
            for timing in row['state_timings']:
                assert timing['total_seconds'] >= timing['prepare_seconds'] + timing['apply_seconds']
                timings[phase][timing['backend']] += timing['total_seconds']
            comparisons += row['complete_backend_scalar_comparisons']
            old += row['old_P1600_actual_scalar_overlaps']
            peaks.append(packet['peak_rss_bytes'])
    assert comparisons == 926352 and old == 230400
    return {'sampled_states_per_mode': 18, 'backend_scalar_comparisons': comparisons,
        'old_P1600_actual_scalar_overlaps': old, 'summed_state_seconds': timings,
        'maximum_single_process_peak_rss_bytes': max(peaks),
        'full_174_state_coverage': False, 'complete_refinement_costed': False}


def prospective_inventory():
    P, seed, states = 3200, 1600, 174
    uniform = states * P * 8 * 50
    weighted = states * sum((max(0, -((i - (P if k <= 32 else P - k)) // 8)) + 7) // 8
                           for k in range(P) for i in range(8))
    scaled = states * (P - seed) * 8 * 25
    slots = {'old_seed_input': uniform // 2, 'seed_extension_chunks': uniform,
        'two_complete_checkpoints': 2 * (weighted + scaled),
        'new_prepared_weighted_state': weighted, 'prepared_correction': scaled,
        'one_active_operator_sweep': uniform, 'assembled_uniform_state': uniform,
        'final_full_residual': uniform, 'scratch_metadata_allowance': 1 << 20}
    assert (uniform, weighted, scaled) == (222720000, 113343600, 55680000)
    assert sum(slots.values()) == 1510359376 < 2 * (1 << 30)
    final = 2 * uniform + weighted + states * 33 * 8
    assert final == 558829536
    return {'working_precision_pi': P, 'conservative_simultaneous_slots': slots,
        'conservative_scratch_bytes': sum(slots.values()), 'proposed_scratch_limit_bytes': 2 * (1 << 30),
        'final_state_payload_bytes': final, 'direct_CM_payload_bytes': 17 * 2 * P * 8 * 50,
        'arithmetic_driver_not_yet_implemented': True, 'hard_cap_not_yet_enforced_at_P3200': True,
        'RSS_bound_or_complete_runtime_certificate': False}


def build():
    prior = read('dyadic_rolling_review_d127')
    assert prior['independent_finite_review_complete'] and len(prior['sources']) == 9599
    checked(prior['sources'])
    for stem in ('dyadic_rolling_review_d127_attempt01', 'dyadic_rolling_review_d127_recheck01'):
        packet = read(stem + '.job')
        checked(packet['sources'] + [packet['driver'], packet['log']])
    serial, transport = serial_review(), transport_review()
    inventory = prospective_inventory()
    PATHS.update([Path(__file__), ROOT / 'dembele/certificates/dyadic-selective-scaling-d128.md',
        DATA / 'dyadic_selective_scaling_sources_d128.json'])
    jobs, categories = [], {}
    for path in sorted(DATA.glob('*d128*')):
        assert path.is_file()
        if path.name.startswith('dyadic_selective_scaling_review_d128'):
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
    assert categories == {'525_dyadic_selective_serial_control.py': 4,
        '526_dyadic_precision3200_transport_control.py': 9}, categories
    manifest = [source(p) for p in sorted(PATHS)]
    assert {(r['path'], r['sha256']) for r in prior['sources']} <= {(r['path'], r['sha256']) for r in manifest}
    return {'status': 'pass', 'milestone': 'D128', 'control_review_complete': True,
        'reviewer_imports_production_arithmetic': False, 'inherited_D127_hashes_preserved': 9599,
        'serial_certificates': serial, 'transport_certificates': transport,
        'prospective_P3200_inventory': inventory, 'bounded_input_jobs': jobs,
        'input_job_categories': categories, 'full_bank_precision_pi': 800,
        'actual_columns_at_precision_1600': [0, 1], 'actual_harmonic_precision_increased': False,
        'positive_exact_quadric_vanishing_proved': False, 'candidate_identification_proved': False,
        'target_field_polynomial_constructed': False, 'sources': manifest}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        result = json.loads(OUT.read_text())
        checked(result['sources'])
        assert result['status'] == 'pass' and result['control_review_complete']
    else:
        assert not OUT.exists()
        result = build()
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'sources': len(result['sources']), 'input_jobs': len(result['bounded_input_jobs'])}), flush=True)
    print('PASS|527_DYADIC_SELECTIVE_SCALING_REVIEW', flush=True)
