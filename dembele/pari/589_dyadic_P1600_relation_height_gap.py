"""D140 exact coefficient-height exclusion outside the recognized relation span.

For a full lattice basis b_i, any vector outside the span of its first 91
rows has norm at least min(||b_i*||: i>=91). Exact Gram leading minors
give these squared orthogonal lengths. This bounds ALL congruence-lattice
vectors, not only the vectors found by LLL. It is not a height bound for
the unknown curve's ideal.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
import resource
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def leading_gram_minors(basis):
    n = len(basis)
    gram = [[sum(x*y for x, y in zip(a, b)) for b in basis] for a in basis]
    previous, minors = 1, []
    for k in range(n):
        pivot = gram[k][k]
        assert pivot > 0
        minors.append(pivot)
        for i in range(k + 1, n):
            for j in range(i, n):
                numerator = pivot * gram[i][j] - gram[i][k] * gram[k][j]
                value, remainder = divmod(numerator, previous)
                assert remainder == 0
                gram[i][j] = gram[j][i] = value
        previous = pivot
    return minors


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--recognition', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    assert leading_gram_minors([[2, 0], [1, 3]]) == [4, 36]
    rec_path = DATA / (args.recognition + '.json')
    recognition = json.loads(rec_path.read_text())
    assert recognition['status'] == 'pass' and not recognition['candidate_equations_read']
    ref = recognition['lattice_output']
    assert source(ref['path']) == ref
    packet = json.loads(Path(ref['path']).read_text())
    basis = packet['reduced_basis']
    assert len(basis) == 136 and all(len(row) == 136 for row in basis)
    assert basis[:91] == recognition['recognized_integer_vectors']
    minors = leading_gram_minors(basis)
    assert minors[-1] == 1 << (2 * 45 * recognition['congruence_2_bits'])
    lengths = [Fraction(minors[i], minors[i-1]) for i in range(91, 136)]
    minimum = min(lengths)
    height = isqrt(minimum.numerator // (136 * minimum.denominator))
    if 136 * height * height >= minimum:
        height -= 1
    assert 136 * height * height < minimum <= 136 * (height + 1) ** 2
    result = {'status': 'pass', 'milestone': 'D140', 'recognition': source(rec_path),
              'candidate_equations_read': False, 'lattice_dimension': 136,
              'recognized_span_dimension': 91, 'congruence_2_bits': recognition['congruence_2_bits'],
              'leading_Gram_determinants_hex': [hex(x) for x in minors],
              'outside_span_squared_orthogonal_lengths': [str(x) for x in lengths],
              'minimum_outside_span_squared_norm_lower_bound': str(minimum),
              'every_congruence_relation_with_max_coefficient_at_most_H_is_in_recognized_span': height,
              'strict_norm_inequality_checked': True,
              'bound_is_exhaustive_for_congruence_lattice_not_only_LLL_output': True,
              'unknown_true_ideal_has_basis_below_H_proved': False,
              'exact_curve_identification_proved': False, 'actual_harmonic_precision_increased': False,
              'wall_seconds': time.monotonic()-tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
              'sources': [source(p) for p in [Path(__file__), rec_path, Path(ref['path'])]]}
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D140_HEIGHT_GAP|' + json.dumps({'coefficient_height_H': height, 'seconds': result['wall_seconds']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|589_DYADIC_P1600_RELATION_HEIGHT_GAP', flush=True)


if __name__ == '__main__':
    main()
