"""D140 candidate-free rational relation probe on saved P1600 jets.

No candidate equation, coefficient bound, or candidate pivot list is read.
Flatten selected quadratic Taylor coefficients in the beta power basis,
eliminate with explicit loss of 2-adic precision, and try rational
reconstruction of the resulting kernel graph. This discovers candidates;
finite zero residues do not prove exact global relations.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import resource
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
spec = importlib.util.spec_from_file_location('balls_d140', ROOT / 'dembele/pari/570_dyadic_precision1600_balls.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)
PAIRS = [(i, j) for i in range(16) for j in range(i, 16)]


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while raw := stream.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def matrix(frame, charts, orders):
    rows, labels, blocks = [], [], []
    for ci in charts:
        jet = [[f.restore(x) for x in row] for row in frame['CM_values'][ci]['actual_residue_frame_coarse_jets']]
        for n in orders:
            values = []
            for i, j in PAIRS:
                value = f.Ball()
                for k in range(n + 1):
                    value = value + jet[k][i] * jet[n-k][j]
                values.append(value)
            shift = min(z.lower() for z in values)
            assert shift < f.INF
            error = min(z.error - shift for z in values)
            bits = error // 16
            assert bits > 0
            coordinates = [f.ZERO if z.u == f.ZERO else f.R.mul(z.u, f.beta_power(z.v - shift)) for z in values]
            rows.extend([[z[d] % (1 << bits) for z in coordinates] for d in range(16)])
            labels.extend([{'chart': ci, 'order': n, 'beta_coordinate': d} for d in range(16)])
            blocks.append({'chart': ci, 'order': n, 'divided_beta_power': shift,
                           'absolute_error_beta_after_division': error, 'coefficient_error_2_bits': bits})
    return rows, labels, blocks


def eliminate(input_rows, bits):
    a = [[x % (1 << bits) for x in row] for row in input_rows]
    m, n = len(a), len(a[0])
    columns, row_order = list(range(n)), list(range(m))
    initial_bits = bits
    pivots = []
    for k in range(min(m, n)):
        options = [((x & -x).bit_length() - 1, i, j)
                   for i in range(k, m) for j in range(k, n) if (x := a[i][j])]
        if not options:
            break
        valuation, i, j = min(options)
        assert valuation < bits
        a[k], a[i] = a[i], a[k]
        row_order[k], row_order[i] = row_order[i], row_order[k]
        for row in a:
            row[k], row[j] = row[j], row[k]
        columns[k], columns[j] = columns[j], columns[k]
        bits -= valuation
        modulus = 1 << bits
        for r in range(m):
            for c in range(n):
                if r >= k and c >= k:
                    assert a[r][c] % (1 << valuation) == 0
                    a[r][c] >>= valuation
                a[r][c] %= modulus
        inv = pow(a[k][k], -1, modulus)
        a[k] = [x * inv % modulus for x in a[k]]
        for r in range(m):
            if r != k and (factor := a[r][k]):
                a[r] = [(x - factor*y) % modulus for x, y in zip(a[r], a[k])]
        pivots.append({'original_row': row_order[k], 'original_column': columns[k],
                       'common_2_precision_loss': valuation, 'remaining_2_bits': bits})
    rank = len(pivots)
    assert all(a[i][j] == (1 if i == j else 0) for i in range(rank) for j in range(rank))
    assert all(not x for row in a[rank:] for x in row)
    return {'rank_lower_bound': rank, 'input_2_bits': initial_bits, 'remaining_2_bits': bits,
            'total_2_precision_loss': initial_bits - bits, 'pivots': pivots,
            'column_order': columns, 'rref_pivot_rows': a[:rank],
            'zero_trailing_block_is_finite_precision_only': True}


def reconstruct(value, modulus):
    bound = isqrt((modulus - 1) // 2)
    r0, r1, t0, t1 = modulus, value % modulus, 0, 1
    while abs(r1) > bound:
        q = r0 // r1
        r0, r1, t0, t1 = r1, r0 - q*r1, t1, t0 - q*t1
    if not t1 or abs(t1) > bound or gcd(r1, t1) != 1 or t1 % 2 == 0:
        return None
    answer = Fraction(r1, t1)
    assert (answer.numerator - value*answer.denominator) % modulus == 0
    return answer


def rational_kernel(reduced):
    rank = reduced['rank_lower_bound']
    columns = reduced['column_order']
    modulus = 1 << reduced['remaining_2_bits']
    vectors, failed, heights = [], [], []
    for free in range(rank, len(columns)):
        graph = [reconstruct(-row[free], modulus) for row in reduced['rref_pivot_rows']]
        bad = [i for i, value in enumerate(graph) if value is None]
        if bad:
            failed.append({'free_column': columns[free], 'failed_pivot_rows': bad})
            continue
        den = lcm(*(q.denominator for q in graph))
        row = [0] * len(columns)
        row[columns[free]] = den
        for pivot, value in enumerate(graph):
            row[columns[pivot]] = int(den * value)
        content = gcd(*row)
        assert content > 0
        row = [x // content for x in row]
        vectors.append(row)
        heights.append(max(map(abs, row)))
    return {'integer_vectors': vectors, 'reconstructed_vectors': len(vectors),
            'failed_vectors': failed, 'maximum_coefficient_height': max(heights, default=0),
            'entrywise_rational_reconstruction_bound': isqrt((modulus - 1) // 2)}


def controls():
    # Known rank two, nonunit leading entries, column swaps, and zero rows.
    rows = [[8, 16, 24, 40], [0, 4, 12, 20], [8, 20, 36, 60]]
    r = eliminate(rows, 48)
    assert r['rank_lower_bound'] == 2
    k = rational_kernel(r)
    assert k['reconstructed_vectors'] == 2
    assert all(sum(x*y for x, y in zip(row, v)) == 0 for row in rows for v in k['integer_vectors'])
    for q in [Fraction(0), Fraction(-7, 13), Fraction(127, 3), Fraction(1, 31)]:
        modulus = 1 << 32
        assert reconstruct(q.numerator * pow(q.denominator, -1, modulus), modulus) == q
    assert reconstruct(2, 4) is None
    return {'valued_elimination_rank_and_kernel': True, 'rational_reconstruction_examples': 5}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--chart', type=int, default=1, choices=range(17))
    ap.add_argument('--orders', type=int, default=3, choices=range(1, 5))
    ap.add_argument('--bits', type=int, default=96)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    cert = controls()
    frame_path = DATA / 'dyadic_residue_frame1600_d138.json'
    review_path = DATA / 'dyadic_precision1600_review_d138.json'
    review = json.loads(review_path.read_text())
    known = {row['path']: row['sha256'] for row in review['sources']}
    for path in (frame_path, Path(f.__file__)):
        ref = source(path)
        assert known[ref['path']] == ref['sha256']
    frame = json.loads(frame_path.read_text())
    assert frame['status'] == 'pass' and not frame['candidate_data_used']
    rows, labels, blocks = matrix(frame, [args.chart], range(args.orders))
    available = min(x['coefficient_error_2_bits'] for x in blocks)
    assert 8 <= args.bits <= available
    reduced = eliminate(rows, args.bits)
    print('D140_RANK|' + json.dumps({k: reduced[k] for k in ('rank_lower_bound', 'remaining_2_bits', 'total_2_precision_loss')}), flush=True)
    kernel = rational_kernel(reduced)
    validation = []
    for vector in kernel['integer_vectors']:
        residuals = [sum(x*y for x, y in zip(row, vector)) % (1 << available) for row in rows]
        agrees = all(x == 0 for x in residuals)
        agreement_bits = min([available] + [(x & -x).bit_length()-1 for x in residuals if x])
        validation.append({'full_available_training_matrix_agrees': agrees,
                           'agreement_2_bits': agreement_bits})
    result = {'status': 'pass', 'milestone': 'D140', 'candidate_equations_read': False,
              'scope': 'bounded candidate-free discovery, not exact relation certification',
              'training_chart': args.chart, 'training_orders': list(range(args.orders)),
              'training_2_bits': args.bits, 'available_2_bits': available,
              'unused_higher_2_bits': available - args.bits, 'monomial_pairs': PAIRS,
              'controls': cert, 'matrix_rows': rows, 'matrix_labels': labels,
              'block_error_bounds': blocks, 'elimination': reduced, 'reconstruction': kernel,
              'higher_digit_validation': validation,
              'all_reconstructed_vectors_pass_higher_digits': all(x['full_available_training_matrix_agrees'] for x in validation),
              'actual_harmonic_precision_increased': False, 'exact_curve_identification_proved': False,
              'wall_seconds': time.monotonic() - tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
              'sources': [source(p) for p in [Path(__file__), Path(f.__file__), frame_path, review_path]]}
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    with out.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print('D140_RECONSTRUCTION|' + json.dumps({'vectors': kernel['reconstructed_vectors'],
          'height': kernel['maximum_coefficient_height'], 'all_higher_digits_pass': result['all_reconstructed_vectors_pass_higher_digits'],
          'seconds': result['wall_seconds']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|583_DYADIC_P1600_RELATION_PROBE', flush=True)
