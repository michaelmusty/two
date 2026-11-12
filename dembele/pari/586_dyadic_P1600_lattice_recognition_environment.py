"""D140 simultaneous recognition with the installed Sage executable environment.

The full congruence lattice is LLL-reduced by Sage in this capped process
group. No old candidate equations or coefficient-height cutoff is used.
The first nullity-many short rows are proposed for withheld-data validation.
The unimodular transformation and full basis are retained for exact review.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
SAGE = '/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/python3'


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def worker(input_path, output_path):
    from sage.all import ZZ, matrix
    packet = json.loads(Path(input_path).read_text())
    basis = matrix(ZZ, packet['basis'])
    tick = time.monotonic()
    reduced, transform = basis.LLL(delta=.99, algorithm='fpLLL:wrapper', transformation=True)
    assert transform*basis == reduced
    assert abs(transform.det()) == 1
    order = sorted(range(reduced.nrows()), key=lambda i: sum(x*x for x in reduced[i]))
    reduced = reduced.matrix_from_rows(order)
    transform = transform.matrix_from_rows(order)
    assert transform*basis == reduced
    result = {'status': 'pass', 'reduced_basis': [[int(x) for x in row] for row in reduced],
              'unimodular_transform': [[int(x) for x in row] for row in transform],
              'unimodular_transform_checked': True,
              'squared_norms': [int(sum(x*x for x in row)) for row in reduced],
              'lll_seconds': time.monotonic() - tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    with Path(output_path).open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D140_LLL_WORKER_PASS', flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--probe', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    probe_path = DATA / (args.probe + '.json')
    probe = json.loads(probe_path.read_text())
    assert probe['status'] == 'pass' and not probe['candidate_equations_read']
    e = probe['elimination']
    rank, bits = e['rank_lower_bound'], e['remaining_2_bits']
    columns, rows = e['column_order'], e['rref_pivot_rows']
    modulus, n = 1 << bits, len(columns)
    basis = []
    for k in range(rank):
        row = [0] * n
        row[columns[k]] = modulus
        basis.append(row)
    for free in range(rank, n):
        row = [0] * n
        row[columns[free]] = 1
        for k in range(rank):
            value = -rows[k][free] % modulus
            row[columns[k]] = value if value <= modulus//2 else value - modulus
        basis.append(row)
    assert len(basis) == n
    input_path = DATA / (args.output + '_input.json')
    child_path = DATA / (args.output + '_worker.json')
    with input_path.open('x') as f:
        f.write(json.dumps({'basis': basis, 'congruence_bits': bits, 'rank': rank}, indent=2) + '\n')
    assert not child_path.exists()
    cache = Path('/private/tmp/dembele_P1600_recognition_sage')
    cache.mkdir(exist_ok=True)
    sage_base = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
    env = dict(os.environ, DOT_SAGE=str(cache))
    env['PATH'] = str(sage_base / 'local/bin') + ':' + str(sage_base / 'venv/bin') + ':' + env.get('PATH', '')
    child = subprocess.run([SAGE, str(Path(__file__).resolve()), '--worker', str(input_path), str(child_path)],
                           cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D140_LLL_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    reduced = json.loads(child_path.read_text())
    nullity = n - rank
    proposed = reduced['reduced_basis'][:nullity]
    assert reduced['unimodular_transform_checked']
    for vector in reduced['reduced_basis']:
        assert all(sum(vector[columns[j]] * row[j] for j in range(n)) % modulus == 0 for row in rows)
    available = probe['available_2_bits']
    higher = [all(sum(x*y for x, y in zip(row, v)) % (1 << available) == 0 for row in probe['matrix_rows']) for v in proposed]
    self_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    child_rss = max(reduced['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * (1 if sys.platform == 'darwin' else 1024))
    assert self_rss + child_rss < 2 * (1 << 30)
    result = {'status': 'pass', 'milestone': 'D140', 'candidate_equations_read': False,
              'probe': source(probe_path), 'lattice_input': source(input_path), 'lattice_output': source(child_path),
              'rank_lower_bound': rank, 'proposed_relation_count': nullity, 'congruence_2_bits': bits,
              'training_2_bits': probe['training_2_bits'], 'available_2_bits': available,
              'monomial_pairs': probe['monomial_pairs'], 'recognized_integer_vectors': proposed,
              'maximum_recognized_coefficient_height': max(abs(x) for v in proposed for x in v),
              'largest_proposed_squared_norm': reduced['squared_norms'][nullity-1],
              'smallest_unselected_squared_norm': reduced['squared_norms'][nullity],
              'higher_training_digits_pass_count': sum(higher),
              'all_proposed_relations_pass_higher_training_digits': all(higher),
              'lll_is_discovery_not_exhaustive_height_search': True,
              'exact_curve_identification_proved': False, 'actual_harmonic_precision_increased': False,
              'wall_seconds': time.monotonic() - tick, 'peak_rss_bytes': self_rss,
              'child_peak_rss_bytes': child_rss,
              'sources': [source(p) for p in [Path(__file__), probe_path, input_path, child_path, SAGE]]}
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D140_RECOGNIZED|' + json.dumps({'relations': nullity, 'height': result['maximum_recognized_coefficient_height'],
          'higher_digit_passes': sum(higher), 'seconds': result['wall_seconds']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|586_DYADIC_P1600_LATTICE_RECOGNITION_ENVIRONMENT', flush=True)


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--worker':
        worker(sys.argv[2], sys.argv[3])
    else:
        main()
