"""D126 fixed provenance and independent byte-level review of resource controls.

No production arithmetic or new resource-control implementation is imported.
The prior mathematical review is preserved. New checks audit complete state
coverage, reference-byte digests, weighted coordinates, and sealed scratch.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_resource_controls_review_d126.json'
CACHE, PATHS = {}, set()


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


def checked(records):
    for record in records:
        assert source(record['path']) == record, record['path']


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def state_bytes():
    verified = read('dyadic_weighted_P1600_col00_verified_d124')
    checked([verified['state_file'], verified['weighted_state_metadata']])
    weighted = read(Path(verified['weighted_state_metadata']['path']).stem)
    checked([weighted['state_file']])
    harmonic = read('dyadic_harmonic_certificate_d111')['harmonic_basis'][0]
    uniform_path = Path(verified['state_file']['path'])
    count = 0
    with uniform_path.open('rb') as full, Path(weighted['state_file']['path']).open('rb') as small:
        for e in range(174):
            for k in range(1600):
                for i in range(8):
                    raw = full.read(25)
                    assert len(raw) == 25
                    x = int.from_bytes(raw, 'little')
                    precision = 1600 if k < 33 else 1600 - k
                    bits = max(0, (precision + 7 - i) // 8)
                    width = (bits + 7) // 8
                    reduced = small.read(width)
                    assert len(reduced) == width
                    assert int.from_bytes(reduced, 'little') == x % (1 << bits)
                    if k == 0:
                        assert x == (harmonic[e] % (1 << 200) if i == 0 else 0)
                    count += 1
        assert not full.read(1) and not small.read(1)
    assert count == 2227200
    counts, peaks, durations = {}, {}, {}
    for mode in ('uniform', 'weighted'):
        covered, checks, peak, seconds = [], 0, 0, 0.0
        for first in range(0, 174, 29):
            stem = f'dyadic_selective_{mode}_e{first:03d}_{first + 28:03d}_d126'
            packet = read(stem)
            cert = packet['certificates']
            indices = list(range(first, first + 29))
            assert cert['output_states'] == indices and cert['input_kind'] == mode
            assert cert['backend'] == 'original GMP'
            assert cert['full_original_operator_scalar_checks'] == len(indices) * 1600 * 8
            assert cert['source_reads']['row_reads'] == 2 * len(indices)
            sha = hashlib.sha256()
            with uniform_path.open('rb') as f:
                for e in indices:
                    f.seek(e * 1600 * 8 * 25)
                    row = f.read(1600 * 8 * 25)
                    assert len(row) == 1600 * 8 * 25
                    sha.update(row)
            assert sha.hexdigest() == cert['computed_rows_sha256']
            covered += indices
            checks += cert['full_original_operator_scalar_checks']
            peak = max(peak, packet['peak_rss_bytes'])
            seconds += packet['wall_seconds']
        assert covered == list(range(174)) and checks == count
        counts[mode], peaks[mode], durations[mode] = checks, peak, seconds
    projected = read('dyadic_selective_projection_d126')['certificates']
    assert projected['all_weighted_projection_scalar_checks'] == count
    selected = [read(f'dyadic_selective_{mode}_d126')['certificates'] for mode in ('uniform', 'weighted')]
    assert selected[0]['computed_rows_sha256'] == selected[1]['computed_rows_sha256']
    return {'independent_weighted_coordinate_checks': count, 'independent_exact_masses_checked': 174,
        'complete_original_operator_scalar_checks_per_input_kind': counts,
        'complete_chunk_peak_rss_bytes_by_input_kind': peaks,
        'summed_chunk_seconds_by_input_kind': durations}


def scratch():
    packet = read('dyadic_rolling_scratch_control_d126')
    cert = packet['certificates']
    assert cert['checkpoint_replays'] == 25 and len(cert['replayed_checkpoint_records']) == 25
    assert cert['maximum_observed_scratch_bytes'] <= cert['storage_limit_bytes_including_metadata'] == 87665776
    assert cert['maximum_observed_scratch_bytes'] == 84954288
    assert cert['corrupt_latest_detected_and_rolled_back']
    assert not cert['old_frozen_files_modified_or_deleted'] and not cert['arithmetic_refinement_integrated']
    for step, leaf in enumerate(cert['replayed_checkpoint_records']):
        checked([leaf['input_metadata']])
        original = json.loads(Path(leaf['input_metadata']['path']).read_text())
        assert leaf['generation'] == f'g{step:06d}'
        assert leaf['weighted_residual_lower_bound_pi'] == 800 + 33 * step
        for payload, role in zip(leaf['payloads'], ('state_file', 'residual_file')):
            file = original[role]
            checked([file])
            assert payload['sha256'] == file['sha256']
            assert payload['bytes'] == Path(file['path']).stat().st_size
    points = [x['point'] for x in cert['expected_process_interruptions']]
    assert points == ['mid_payload', 'after_generation', 'before_head', 'after_head']
    root = DATA / 'dyadic_rolling_scratch_d126'
    seal = json.loads((root / 'SEALED.json').read_text())
    head = json.loads((root / 'HEAD.json').read_text())
    assert seal['all_remaining_files_now_frozen'] and seal['head'] == head
    assert head == {'current': 'g000024', 'previous': 'g000023'}
    for step in (23, 24):
        directory = root / f'g{step:06d}'
        leaf = json.loads((directory / 'checkpoint.json').read_text())
        assert leaf == cert['replayed_checkpoint_records'][step]
        for row in leaf['payloads']:
            file = directory / row['name']
            assert source(file)['sha256'] == row['sha256'] and file.stat().st_size == row['bytes']
    files = [p for p in root.rglob('*') if p.is_file()]
    assert len(files) == 9 and sum(p.stat().st_size for p in files) == cert['sealed_scratch_bytes'] == 57768619
    PATHS.update(files)
    return {'replayed_checkpoints': 25, 'expected_abrupt_process_exits': 4,
        'corrupt_payload_rollback_control': True, 'storage_limit_bytes': 87665776,
        'maximum_observed_scratch_bytes': 84954288, 'sealed_scratch_bytes': 57768619,
        'deleted_scratch_payloads_not_treated_as_retained_sources': True}


def low_controls():
    resident = read('dyadic_factor_resident_b200_n2_d126')
    streamed = read('dyadic_factor_stream_b200_n2_d126')
    batch = read('dyadic_factor_stream_b200_n16_d126')
    assert resident['certificates']['all_answers_sha256'] == streamed['certificates']['all_answers_sha256']
    assert batch['certificates']['first_two_rhs_answers_sha256'] == streamed['certificates']['all_answers_sha256']
    scalar_checks = 0
    for packet, columns, mode in ((resident, 2, 'resident'), (streamed, 2, 'stream'), (batch, 16, 'stream')):
        cert = packet['certificates']
        assert cert['mode'] == mode and cert['unrelated_rhs_columns'] == columns
        assert cert['factor_blocks_decoded'] == 1226 and cert['modulus_bits'] == 200
        assert cert['complete_original_sparse_residual_scalar_checks'] == 174 * 32 * 8 * columns
        scalar_checks += cert['complete_original_sparse_residual_scalar_checks']
    reuse = read('dyadic_map_reuse_d126')['certificates']
    assert reuse['original_equation_scalar_checks_per_mode'] == 2640
    assert [x['prepared_plans'] for x in reuse['timings']] == [20, 8]
    actual = {}
    for phase, columns in (('harmonic', 2), ('correction', 1)):
        packet = read(f'dyadic_streamed_actual_low_{phase}_d126')
        cert = packet['certificates']
        assert cert['actual_columns'] == columns and cert['factor_blocks_decoded'] == 1226
        assert cert['full_known_low_scalar_comparisons'] == cert['original_sparse_residual_scalar_checks'] == 44544 * columns
        assert cert['exact_masses_checked'] == 174 * columns and cert['distinct_prepared_maps'] == 165
        assert cert['maximum_prepared_maps_held'] == cert['maximum_decoded_factor_blocks_held'] == 1
        actual[phase] = {'scalar_comparisons': cert['full_known_low_scalar_comparisons'],
            'peak_rss_bytes': packet['peak_rss_bytes'], 'wall_seconds': packet['wall_seconds']}
    return {'factor_original_sparse_scalar_checks': scalar_checks,
        'resident_two_rhs_peak_rss_bytes': resident['peak_rss_bytes'],
        'streamed_two_rhs_peak_rss_bytes': streamed['peak_rss_bytes'],
        'streamed_sixteen_rhs_peak_rss_bytes': batch['peak_rss_bytes'],
        'map_reuse_control_scalar_checks_per_mode': 2640, 'actual_low_controls': actual}


def build():
    prior = read('dyadic_precision800_review_d125')
    assert prior['independent_mathematical_review_complete'] and len(prior['sources']) == 8729
    checked(prior['sources'])
    for stem in ('dyadic_precision800_review_d125_attempt01', 'dyadic_precision800_review_d125_recheck01'):
        row = read(stem + '.job')
        checked(row['sources'] + [row['driver'], row['log']])
    PATHS.update([Path(__file__), ROOT / 'dembele/certificates/dyadic-resource-controls-d126.md',
        DATA / 'dyadic_resource_controls_sources_d126.json'])
    cert = {'state_reads': state_bytes(), 'scratch': scratch(), 'low_solve': low_controls()}
    jobs, categories = [], {}
    for path in sorted(DATA.glob('*d126*')):
        if path.name.startswith('dyadic_resource_controls_review_d126') or path.is_dir():
            continue
        PATHS.add(path)
        if path.suffix != '.json':
            if path.suffix == '.log':
                assert path.with_suffix('.job.json').exists()
            continue
        row = json.loads(path.read_text())
        checked([x for x in row.get('sources', []) if isinstance(x, dict) and 'sha256' in x])
        if not path.name.endswith('.job.json'):
            continue
        assert row['status'] == 'pass' and row['exit_code'] == 0 and row['timeout_seconds'] == 180
        assert row['timeout_terminates_process_group']
        checked([row['driver'], row['log']])
        driver = Path(row['driver']['path']).name
        categories[driver] = categories.get(driver, 0) + 1
        jobs.append({'receipt': path.name, 'driver': driver, 'wall_seconds': row['wall_seconds']})
    assert categories == {'514_dyadic_selective_state_control.py': 15,
        '515_dyadic_rolling_scratch_control.py': 1, '516_dyadic_factor_and_map_controls.py': 4,
        '517_dyadic_streamed_actual_low_control.py': 2}, categories
    manifests = [source(path) for path in sorted(PATHS)]
    assert {(r['path'], r['sha256']) for r in prior['sources']} <= {(r['path'], r['sha256']) for r in manifests}
    return {'status': 'pass', 'milestone': 'D126', 'resource_controls_review_complete': True,
        'production_arithmetic_not_imported_by_reviewer': True,
        'inherited_D125_hashes_preserved': 8729, 'certificates': cert,
        'bounded_input_jobs': jobs, 'job_categories': categories,
        'actual_moment_precision_increased': False, 'full_bank_precision_pi': 800,
        'positive_exact_quadric_vanishing_proved': False, 'candidate_identification_proved': False,
        'target_field_polynomial_constructed': False, 'complete_target_size_solve_costed': False,
        'sources': manifests}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        result = json.loads(OUT.read_text())
        checked(result['sources'])
        assert result['status'] == 'pass' and result['resource_controls_review_complete']
    else:
        assert not OUT.exists()
        result = build()
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'sources': len(result['sources']), 'input_jobs': len(result['bounded_input_jobs'])}), flush=True)
    print('PASS|518_DYADIC_RESOURCE_CONTROLS_REVIEW', flush=True)
