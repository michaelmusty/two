"""D140 fixed review of candidate-independent recognition at saved P1600.

Standard library only. Recheck exact matrix certificates, authenticate the
independent Horner and determinant jobs, and replay the whole inherited graph.
The coefficient-height hypothesis for the unknown true ideal remains open.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'dyadic_P1600_recognition_review_d140.json'
PATHS = {Path(__file__), ROOT / 'dembele/certificates/dyadic-P1600-recognition-d140.md'}
DIGESTS = {}
INPUT_RECEIPTS = []


def raw_source(path):
    key = str(path)
    if key not in DIGESTS:
        h = hashlib.sha256()
        with Path(path).open('rb') as f:
            while raw := f.read(1 << 20):
                h.update(raw)
        DIGESTS[key] = h.hexdigest()
    return {'path': key, 'sha256': DIGESTS[key]}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return raw_source(path)


def checked(refs):
    for ref in refs:
        assert source(ref['path']) == ref, ref['path']


def read(stem, status='pass'):
    path = DATA / (stem + '.json')
    source(path)
    value = json.loads(path.read_text())
    assert value['status'] == status, stem
    return value


def inherited_graph(ref):
    assert raw_source(ref['path']) == ref
    parent = json.loads(Path(ref['path']).read_text())
    assert parent['status'] == 'pass' and parent['milestone'] == 'D139'
    assert parent['independent_finite_review_complete'] and parent['catalogue_graph_is_transitive']
    for item in parent['sources']:
        assert raw_source(item['path']) == item, item['path']
    previous_ref = parent['inherited_review']
    assert raw_source(previous_ref['path']) == previous_ref
    previous = json.loads(Path(previous_ref['path']).read_text())
    assert previous['status'] == 'pass' and previous['sixteen_column_checkpoint_complete']
    for item in previous['sources']:
        assert raw_source(item['path']) == item, item['path']
    inherited = set()
    occurrences = 0
    assert len(previous['inherited_catalogues']) == 15
    for ref in previous['inherited_catalogues']:
        assert raw_source(ref['path']) == ref
        catalogue = json.loads(Path(ref['path']).read_text())
        for item in catalogue['sources']:
            assert raw_source(item['path']) == item, item['path']
            inherited.add(item['path'])
            occurrences += 1
    assert occurrences == previous['catalogue_hash_replays'] == parent['inherited_catalogue_hash_occurrences'] == 380188
    assert len(inherited) == previous['unique_inherited_file_hashes'] == parent['unique_inherited_file_hashes'] == 379923
    return {'parent_direct_bindings': len(parent['sources']),
            'D138_direct_bindings': len(previous['sources']),
            'inherited_catalogue_roots': 15, 'inherited_catalogue_hash_occurrences': occurrences,
            'unique_inherited_file_hashes': len(inherited)}


def job(row, driver, args, output_ref):
    checked([row['driver'], row['log'], *row['sources']])
    assert row['driver'] == source(ROOT / 'dembele/pari' / driver)
    assert row['command'] == ['python3', row['driver']['path']] + args
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert 0 < row['wall_seconds'] < row['timeout_seconds'] == 180
    assert row['private_process_group'] > 0 and row['timeout_terminates_process_group']
    lines = Path(row['log']['path']).read_text().splitlines()
    marks = [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]
    assert marks == [output_ref]
    assert any(s.startswith('PASS|' + driver[:3] + '_') for s in lines)


def receipt(stem, driver, args):
    packet = read(stem)
    row = read(stem + '_attempt01.job')
    job(row, driver, args, source(DATA / (stem + '.json')))
    checked(packet['sources'])
    assert packet['peak_rss_bytes'] + packet.get('child_peak_rss_bytes', 0) < 2 * (1 << 30)
    INPUT_RECEIPTS.append({'receipt': source(DATA / (stem + '_attempt01.job.json')),
                           'wall_seconds': row['wall_seconds'],
                           'conservative_peak_rss_bytes': packet['peak_rss_bytes'] + packet.get('child_peak_rss_bytes', 0)})
    return packet


def product(left, right):
    assert all(len(row) == len(right) for row in left)
    columns = list(zip(*right))
    return [[sum(a*b for a, b in zip(row, col)) for col in columns] for row in left]


def determinant(rows):
    a = [list(row) for row in rows]
    n, sign, divisor = len(a), 1, 1
    assert all(len(row) == n for row in a)
    if n == 0:
        return 1
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, n):
            factor = a[i][k]
            for j in range(k+1, n):
                q, r = divmod(p*a[i][j] - factor*a[k][j], divisor)
                assert not r
                a[i][j] = q
            a[i][k] = 0
        divisor = p
    return sign*a[-1][-1]


def failures():
    specs = [
        ('dyadic_P1600_lattice96_d140', '584_dyadic_P1600_lattice_recognition.py',
         ['--probe', 'dyadic_P1600_relation_probe96_d140'], ['Could not find SageMath-10-6.app'], True),
        ('dyadic_P1600_lattice96_r2_d140', '585_dyadic_P1600_lattice_recognition_revision.py',
         ['--probe', 'dyadic_P1600_relation_probe96_d140'], ['FeatureNotPresentError', 'Singular', 'not found on PATH'], True),
        ('dyadic_P1600_recognized_lattice_comparison_d140', '588_dyadic_P1600_recognized_lattice_comparison.py',
         [], ["candidate = read('cm_frame_curve_candidate')", "assert value['status'] == 'pass'"], False)]
    refs = []
    for stem, driver, args, messages, has_input in specs:
        row = read(stem + '_attempt01.job', 'failed')
        checked([row['driver'], row['log'], row['failed_driver_snapshot'], *row['sources']])
        assert row['driver'] == source(ROOT / 'dembele/pari' / driver)
        assert row['driver']['sha256'] == row['failed_driver_snapshot']['sha256']
        assert row['command'] == ['python3', row['driver']['path']] + args + ['--output', stem]
        assert row['exit_code'] == 1 and 0 < row['wall_seconds'] < row['timeout_seconds'] == 180
        assert row['private_process_group'] > 0 and row['timeout_terminates_process_group']
        log = Path(row['log']['path']).read_text()
        assert all(s in log for s in messages) and 'PHASE_METADATA|' not in log
        assert not (DATA / (stem + '.json')).exists()
        assert not (DATA / (stem + '_worker.json')).exists()
        if has_input:
            source(DATA / (stem + '_input.json'))
        else:
            assert not (DATA / (stem + '_input.json')).exists()
        refs.append(source(DATA / (stem + '_attempt01.job.json')))
    return refs


def check_one(bits):
    probe_stem = f'dyadic_P1600_relation_probe{bits}_d140'
    rec_stem = f'dyadic_P1600_lattice{bits}_r3_d140'
    hold_stem = f'dyadic_P1600_recognition_holdout{bits}_d140'
    height_stem = f'dyadic_P1600_relation_height{bits}_d140'
    cert_stem = f'dyadic_P1600_recognition_certificates{bits}_d140'
    p = receipt(probe_stem, '583_dyadic_P1600_relation_probe.py', ['--bits', str(bits), '--output', probe_stem])
    r = receipt(rec_stem, '586_dyadic_P1600_lattice_recognition_environment.py', ['--probe', probe_stem, '--output', rec_stem])
    h = receipt(hold_stem, '587_dyadic_P1600_recognition_holdout.py', ['--recognition', rec_stem, '--output', hold_stem])
    g = receipt(height_stem, '589_dyadic_P1600_relation_height_gap.py', ['--recognition', rec_stem, '--output', height_stem])
    c = receipt(cert_stem, '591_dyadic_P1600_recognition_certificates.py', ['--bits', str(bits), '--output', cert_stem])
    pairs = [[i, j] for i in range(16) for j in range(i, 16)]
    assert p['monomial_pairs'] == r['monomial_pairs'] == pairs
    assert p['training_chart'] == 1 and p['training_orders'] == [0, 1, 2]
    assert p['training_2_bits'] == r['training_2_bits'] == c['training_2_bits'] == bits
    assert p['available_2_bits'] == r['available_2_bits'] == 180
    assert p['unused_higher_2_bits'] == h['unused_higher_training_2_bits'] == 180-bits
    assert p['controls'] == {'valued_elimination_rank_and_kernel': True, 'rational_reconstruction_examples': 5}
    assert p['reconstruction']['reconstructed_vectors'] == 0 and p['reconstruction']['integer_vectors'] == []
    assert len(p['reconstruction']['failed_vectors']) == 91 and p['higher_digit_validation'] == []
    assert p['matrix_labels'] == [{'chart': 1, 'order': k, 'beta_coordinate': d} for k in range(3) for d in range(16)]
    assert len(p['matrix_rows']) == 48 and all(len(row) == 136 for row in p['matrix_rows'])
    assert [v['coefficient_error_2_bits'] for v in p['block_error_bounds']] == [181, 181, 180]
    for value in (p, r, h, g, c):
        assert value['candidate_equations_read'] is False
    for value in (p, r, h, g):
        assert value['actual_harmonic_precision_increased'] is False
    for value in (p, r, g, c):
        assert value['exact_curve_identification_proved'] is False
    for value in (h, c):
        assert value['production_ball_arithmetic_imported'] is False
    assert c['independently_replayed_training_matrix_entries'] == 48*136
    assert c['unknown_true_ideal_height_bound_proved'] is False
    e, cert = p['elimination'], c['certificates']
    rank, loss, n = 45, 13, 136
    q, columns = bits-loss, e['column_order']
    assert e['rank_lower_bound'] == r['rank_lower_bound'] == cert['rank_lower_bound'] == rank
    assert e['remaining_2_bits'] == r['congruence_2_bits'] == g['congruence_2_bits'] == q
    assert e['total_2_precision_loss'] == cert['inverse_denominator_2_power'] == loss
    assert cert['inverse_certificate_modulus_2_bits'] == bits and sorted(columns) == list(range(n))
    selected = cert['selected_original_rows']
    assert selected == [v['original_row'] for v in e['pivots']] and len(set(selected)) == rank
    assert cert['pivot_columns'] == columns[:rank]
    assert cert['kernel_graph_checked_without_valued_elimination']
    assert cert['independent_Gram_leading_minor_sizes_checked'] == list(range(91, 137))
    transformed = product(cert['inverse_numerator_mod_2_power'], [p['matrix_rows'][i] for i in selected])
    transformed = [[row[j] % (1 << bits) for j in columns] for row in transformed]
    assert all(row[j] == ((1 << loss) if i == j else 0) for i, row in enumerate(transformed) for j in range(rank))
    assert all(x % (1 << loss) == 0 for row in transformed for x in row)
    assert [[x >> loss for x in row] for row in transformed] == e['rref_pivot_rows']
    assert all(row[j] == int(i == j) for i, row in enumerate(e['rref_pivot_rows']) for j in range(rank))
    checked([r['probe'], r['lattice_input'], r['lattice_output'], h['recognition'], g['recognition']])
    assert r['probe'] == source(DATA / (probe_stem + '.json'))
    assert h['recognition'] == g['recognition'] == source(DATA / (rec_stem + '.json'))
    initial = json.loads(Path(r['lattice_input']['path']).read_text())
    reduced = json.loads(Path(r['lattice_output']['path']).read_text())
    assert initial['rank'] == rank and initial['congruence_bits'] == q
    expected = []
    modulus = 1 << q
    for i in range(n):
        row = [0]*n
        row[columns[i]] = modulus if i < rank else 1
        if i >= rank:
            for k in range(rank):
                x = -e['rref_pivot_rows'][k][i] % modulus
                row[columns[k]] = x if x <= modulus//2 else x-modulus
        expected.append(row)
    assert initial['basis'] == expected
    full, transform = reduced['reduced_basis'], reduced['unimodular_transform']
    assert len(full) == len(transform) == n and all(len(row) == n for row in full+transform)
    assert product(transform, expected) == full
    transform_det = determinant(transform)
    assert abs(transform_det) == 1 and reduced['unimodular_transform_checked']
    vectors = r['recognized_integer_vectors']
    assert full[:91] == vectors and r['proposed_relation_count'] == 91
    norms = [sum(x*x for x in row) for row in full]
    assert norms == reduced['squared_norms'] == sorted(norms)
    assert r['largest_proposed_squared_norm'] == norms[90] and r['smallest_unselected_squared_norm'] == norms[91]
    for row in full:
        assert all(sum(row[columns[j]]*a[j] for j in range(n)) % modulus == 0 for a in e['rref_pivot_rows'])
    assert all(x % (1 << 180) == 0 for row in product(p['matrix_rows'], list(zip(*vectors))) for x in row)
    assert r['higher_training_digits_pass_count'] == 91 and r['all_proposed_relations_pass_higher_training_digits']
    max_height = max(abs(x) for row in vectors for x in row)
    assert max_height == r['maximum_recognized_coefficient_height'] == {96: 968, 160: 981}[bits]
    assert h['all_coefficients_checked'] == 17*4*91 == 6188
    assert h['withheld_chart_coefficients_checked'] == 16*4*91 == 5824
    assert h['additional_withheld_order_coefficients_checked'] == 91
    assert h['total_structurally_withheld_coefficients_checked'] == 5915
    assert h['certified_mismatches'] == [] and h['all_recovered_relations_compatible']
    assert h['one_coefficient_perturbation_rejected'] and h['exact_positive_vanishing_proved'] is False
    assert [row['chart'] for row in h['chart_results']] == list(range(17))
    for row in h['chart_results']:
        assert [v['order'] for v in row['orders']] == list(range(4))
        for v in row['orders']:
            assert v['tested'] == 91 and v['certified_mismatches'] == []
            assert v['minimum_center_or_error_beta'] == v['minimum_error_beta'] > 0
    minors = [int(s, 16) for s in g['leading_Gram_determinants_hex']]
    assert len(minors) == n and all(x > 0 for x in minors)
    assert minors[-1] == 1 << (2*rank*q)
    lengths = [Fraction(minors[i], minors[i-1]) for i in range(91, n)]
    assert lengths == [Fraction(s) for s in g['outside_span_squared_orthogonal_lengths']]
    minimum = min(lengths)
    assert minimum == Fraction(g['minimum_outside_span_squared_norm_lower_bound'])
    H = g['every_congruence_relation_with_max_coefficient_at_most_H_is_in_recognized_span']
    assert n*H*H < minimum <= n*(H+1)*(H+1)
    assert H == {96: 18234668645049602, 160: 223818092532287707686732450725941069}[bits]
    assert g['lattice_dimension'] == n and g['recognized_span_dimension'] == 91
    assert g['strict_norm_inequality_checked'] and g['bound_is_exhaustive_for_congruence_lattice_not_only_LLL_output']
    assert g['unknown_true_ideal_has_basis_below_H_proved'] is False
    return r, {'training_2_bits': bits, 'available_2_bits': 180, 'congruence_2_bits': q,
               'recognized_independent_relations': 91, 'maximum_recognized_coefficient_height': max_height,
               'full_lattice_transform_determinant': transform_det, 'all_coefficients_checked': 6188,
               'structurally_withheld_coefficients_checked': 5915, 'certified_mismatches': 0,
               'exhaustive_coefficient_height_bound': H}


def build():
    tick = time.monotonic()
    assert determinant([[0, 2], [3, 4]]) == -6
    assert determinant([[1, 2, 3], [2, 4, 6], [0, 1, 2]]) == 0
    parent_ref = source(DATA / 'dyadic_indexed_recost_review_r2_d139.json')
    graph = inherited_graph(parent_ref)
    print('D140_REVIEW_INHERITED_GRAPH_PASS', flush=True)
    parent_completion = read('dyadic_indexed_recost_completion_d139')
    assert parent_completion['fixed_review'] == parent_ref and parent_completion['successful_bounded_jobs'] == 6
    checked(parent_completion['review_receipts'])
    for i, ref in enumerate(parent_completion['review_receipts']):
        row = json.loads(Path(ref['path']).read_text())
        job(row, '582_dyadic_indexed_recost_review_revision.py', [] if i == 0 else ['--check'], parent_ref)
    failed = failures()
    recognized, summaries = [], []
    for bits in (96, 160):
        r, summary = check_one(bits)
        recognized.append(r)
        summaries.append(summary)
        print('D140_REVIEW_MATRIX_CERTIFICATES_PASS|' + str(bits), flush=True)
    assert read('dyadic_P1600_relation_probe96_d140')['matrix_rows'] == read('dyadic_P1600_relation_probe160_d140')['matrix_rows']
    stem = 'dyadic_P1600_recognized_lattice_comparison_r2_d140'
    comparison = receipt(stem, '590_dyadic_P1600_recognized_lattice_comparison_revision.py', ['--output', stem])
    assert comparison['candidate_read_only_after_discovery_and_holdout']
    assert comparison['candidate_inputs_used_in_discovery'] is False
    assert comparison['exact_curve_identification_proved'] is False and comparison['field_polynomial_constructed'] is False
    candidate = read('cm_frame_curve_candidate', 'integer curve candidate; Shimura identification not proved')
    assert candidate['saturated_integer_quadric_lattice'] and candidate['monomial_pairs'] == recognized[0]['monomial_pairs']
    cc = comparison['certificates']
    assert cc['recognized_rank'] == 91 and cc['same_saturated_integer_lattice_as_candidate']
    first = recognized[0]['recognized_integer_vectors']
    assert len(cc['pivot_columns']) == len(set(cc['pivot_columns'])) == 91
    assert determinant([[row[i] for i in cc['pivot_columns']] for row in first]) != 0
    for label, target in [('recognized160', recognized[1]['recognized_integer_vectors']), ('candidate', candidate['quadrics'])]:
        change = cc['integer_changes_of_basis'][label]
        assert len(change['rows']) == 91 and all(len(row) == 91 for row in change['rows'])
        assert all(type(x) is int for row in change['rows'] for x in row)
        assert product(change['rows'], first) == target
        assert determinant(change['rows']) == change['determinant'] and abs(change['determinant']) == 1
    for row, summary in zip(cc['congruence_lattice_certificates'], summaries):
        assert row['bits'] == summary['congruence_2_bits'] and row['full_basis_dimension'] == 136
        assert row['transformation_identity_checked'] and row['transform_determinant'] == summary['full_lattice_transform_determinant']
    assert len(INPUT_RECEIPTS) == 11
    return {'status': 'pass', 'milestone': 'D140', 'independent_finite_review_complete': True,
            'inherited_review': parent_ref, 'catalogue_graph_is_transitive': True, **graph,
            'completed_input_jobs': 11, 'preserved_failed_input_jobs': 3,
            'input_receipts': INPUT_RECEIPTS, 'preserved_failed_receipts': failed,
            'recognition_complete': True, 'candidate_equations_used_in_discovery': False,
            'entrywise_rational_reconstruction_complete_vectors': 0,
            'joint_integer_lattice_recognition_runs': summaries,
            'same_saturated_integer_lattice_as_candidate': True,
            'modular_rank_lower_bound': 45, 'exact_integral_relations_lie_in_certified_congruence_lattice': True,
            'height_gap_is_exhaustive_for_integer_congruence_lattice': True,
            'true_canonical_ideal_has_91_integral_quadrics_below_height_bound_proved': False,
            'positive_exact_quadric_vanishing_proved': False, 'candidate_identification_proved': False,
            'field_polynomial_constructed': False, 'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'actual_harmonic_precision_increased': False, 'next_precision_bank_admitted': False,
            'resource_caps_changed': False, 'P3200_default_recommendation_superseded': True,
            'next_work': 'Assess a true-ideal coefficient-height bound in the fixed rational residue frame, or an exact structural identification of the recovered curve.',
            'wall_seconds': time.monotonic()-tick, 'sources': [source(p) for p in sorted(PATHS)]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    tick = time.monotonic()
    if args.check:
        saved = json.loads(OUT.read_text())
        assert saved['status'] == 'pass' and saved['independent_finite_review_complete']
        checked(saved['sources'])
        graph = inherited_graph(saved['inherited_review'])
        assert all(saved[k] == v for k, v in graph.items())
    else:
        assert not OUT.exists()
        saved = build()
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2 * (1 << 30)
        with OUT.open('x') as f:
            f.write(json.dumps(saved, indent=2) + '\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert peak < 2 * (1 << 30)
    print('D140_REVIEW_RESOURCES|' + json.dumps({'seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|592_DYADIC_P1600_RECOGNITION_REVIEW', flush=True)
