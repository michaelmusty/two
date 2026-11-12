"""D140 independent certificates for the modular constraints and height gap.

Horner products replay every training-matrix entry. A separately computed
exact rational inverse supplies a small modular inverse certificate; it
does not replay the valued elimination. Sage determinants independently
check the 46 Gram minors needed for the exhaustive coefficient-height gap.
No candidate equations are read.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
SAGE_BASE = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
SAGE_PYTHON = SAGE_BASE / 'venv/bin/python3'


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def worker(input_path, output_path):
    from sage.all import QQ, ZZ, matrix
    packet = json.loads(Path(input_path).read_text())
    probe, height, reduced = packet['probe'], packet['height'], packet['reduced']
    e = probe['elimination']
    pivot_rows = [p['original_row'] for p in e['pivots']]
    pivot_columns = e['column_order'][:45]
    A = matrix(ZZ, probe['matrix_rows']).matrix_from_rows(pivot_rows)
    B = A.matrix_from_columns(pivot_columns)
    inverse = B.change_ring(QQ).inverse()
    def v2(x):
        x = abs(int(x))
        assert x
        return (x & -x).bit_length() - 1
    shift = max([0] + [v2(q.denominator()) - v2(q.numerator()) for row in inverse for q in row if q])
    assert shift <= e['total_2_precision_loss']
    modulus = 1 << probe['training_2_bits']
    numerator = []
    for row in inverse:
        values = []
        for q in row:
            q *= 1 << shift
            assert q.denominator() % 2
            values.append(int(q.numerator()) * pow(int(q.denominator()), -1, modulus) % modulus)
        numerator.append(values)
    N = matrix(ZZ, numerator)
    product = N * B
    assert all((int(product[i, j]) - ((1 << shift) if i == j else 0)) % modulus == 0 for i in range(45) for j in range(45))
    product = N * A
    graph = [[int(product[i, col]) % modulus for col in e['column_order']] for i in range(45)]
    assert all(x % (1 << shift) == 0 for row in graph for x in row)
    assert [[(x >> shift) % (1 << e['remaining_2_bits']) for x in row] for row in graph] == e['rref_pivot_rows']
    basis = matrix(ZZ, reduced['reduced_basis'])
    gram = basis * basis.transpose()
    checked = []
    for k in range(91, 137):
        indices = list(range(k))
        determinant = int(gram.matrix_from_rows_and_columns(indices, indices).det())
        assert determinant == int(height['leading_Gram_determinants_hex'][k-1], 16)
        checked.append(k)
    result = {'status': 'pass', 'inverse_numerator_mod_2_power': numerator,
              'inverse_denominator_2_power': shift, 'inverse_certificate_modulus_2_bits': probe['training_2_bits'],
              'selected_original_rows': pivot_rows, 'pivot_columns': pivot_columns,
              'rank_lower_bound': 45, 'kernel_graph_checked_without_valued_elimination': True,
              'independent_Gram_leading_minor_sizes_checked': checked,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    with Path(output_path).open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D140_CERTIFICATE_WORKER_PASS', flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bits', type=int, choices=(96, 160), required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    probe_path = DATA / f'dyadic_P1600_relation_probe{args.bits}_d140.json'
    rec_path = DATA / f'dyadic_P1600_lattice{args.bits}_r3_d140.json'
    height_path = DATA / f'dyadic_P1600_relation_height{args.bits}_d140.json'
    frame_path = DATA / 'dyadic_residue_frame1600_d138.json'
    helper = ROOT / 'dembele/pari/587_dyadic_P1600_recognition_holdout.py'
    probe, rec, height, frame = [json.loads(p.read_text()) for p in (probe_path, rec_path, height_path, frame_path)]
    assert all(v['status'] == 'pass' for v in (probe, rec, height, frame))
    assert not probe['candidate_equations_read'] and not rec['candidate_equations_read']
    assert not frame['candidate_data_used']
    spec = importlib.util.spec_from_file_location('independent_Horner_d140', helper)
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    blocks = h.products({'CM_values': [frame['CM_values'][probe['training_chart']]]}, probe['monomial_pairs'])[0]
    replayed = []
    def divide_beta(x, n):
        for _ in range(n):
            assert x[0] % 2 == 0
            half = x[0] // 2
            x = tuple(((x[i+1] if i < 15 else 0) - half*h.POLY[i+1]) & h.MASK for i in range(16))
        return x
    for record in probe['block_error_bounds']:
        block = blocks[record['order']]
        shift = record['divided_beta_power']
        assert all(v.lower() >= shift for v in block)
        assert min(v.error - shift for v in block) >= record['absolute_error_beta_after_division']
        modulus = 1 << record['coefficient_error_2_bits']
        coordinates = [divide_beta(v.center, shift) for v in block]
        replayed.extend([[row[d] % modulus for row in coordinates] for d in range(16)])
    assert replayed == probe['matrix_rows']
    reduced_ref = rec['lattice_output']
    assert source(reduced_ref['path']) == reduced_ref
    reduced = json.loads(Path(reduced_ref['path']).read_text())
    input_path = DATA / (args.output + '_input.json')
    child_path = DATA / (args.output + '_worker.json')
    with input_path.open('x') as f:
        f.write(json.dumps({'probe': probe, 'height': height, 'reduced': reduced}, indent=2) + '\n')
    assert not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE_BASE / 'local/bin') + ':' + str(SAGE_BASE / 'venv/bin') + ':' + env.get('PATH', '')
    child = subprocess.run([str(SAGE_PYTHON), str(Path(__file__).resolve()), '--worker', str(input_path), str(child_path)],
                           cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D140_CERTIFICATE_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    cert = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    child_rss = max(cert['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * (1 if sys.platform == 'darwin' else 1024))
    assert rss + child_rss < 2 * (1 << 30)
    result = {'status': 'pass', 'milestone': 'D140', 'training_2_bits': args.bits,
              'candidate_equations_read': False, 'production_ball_arithmetic_imported': False,
              'independently_replayed_training_matrix_entries': len(replayed) * 136,
              'certificates': cert, 'unknown_true_ideal_height_bound_proved': False,
              'exact_curve_identification_proved': False, 'wall_seconds': time.monotonic()-tick,
              'peak_rss_bytes': rss, 'child_peak_rss_bytes': child_rss,
              'sources': [source(p) for p in [Path(__file__), helper, probe_path, rec_path, height_path, frame_path,
                          Path(reduced_ref['path']), input_path, child_path, SAGE_PYTHON]]}
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D140_INDEPENDENT_CERTIFICATES|' + json.dumps({'matrix_entries': len(replayed)*136,
          'inverse_loss_2_bits': cert['inverse_denominator_2_power'], 'Gram_minors': len(cert['independent_Gram_leading_minor_sizes_checked']),
          'seconds': result['wall_seconds']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|591_DYADIC_P1600_RECOGNITION_CERTIFICATES', flush=True)


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--worker':
        worker(sys.argv[2], sys.argv[3])
    else:
        main()
