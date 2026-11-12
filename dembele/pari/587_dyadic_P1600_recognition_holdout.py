"""D140 independent validation of recognized quadrics on all saved P1600 jets.

No production ball or candidate-equation module is imported. Integer Horner
products in the Eisenstein quotient propagate absolute errors. Candidate
equations are not read. Withheld charts, orders and digits are reported
separately; zero-containing enclosures remain finite-precision statements.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
POLY = (2, 0, 64, 0, 336, 0, 672, 0, 660, 0, 352, 0, 104, 0, 16, 0, 1)
PRECISION = 8192
MODULUS = 1 << (PRECISION // 16)
MASK = MODULUS - 1
ZERO, ONE = (0,) * 16, (1,) + (0,) * 15


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def mul(a, b):
    result = [0] * 16
    for x in reversed(a):
        leading = result[-1]
        result = [(x*b[0] - leading*POLY[0]) & MASK] + [
            (result[i-1] + x*b[i] - leading*POLY[i]) & MASK for i in range(1, 16)]
    return tuple(result)


def valuation(a):
    return min([PRECISION] + [16*((x & -x).bit_length()-1) + i for i, x in enumerate(a) if x])


def power_beta(n):
    assert n >= 0
    result, x = ONE, (0, 1) + (0,) * 14
    while n:
        if n & 1:
            result = mul(result, x)
        x = mul(x, x)
        n //= 2
    return result


class Ball:
    def __init__(self, center=ZERO, error=PRECISION):
        self.center = tuple(x & MASK for x in center)
        self.error = min(error, PRECISION)

    def lower(self):
        return min(valuation(self.center), self.error)

    def __add__(self, other):
        return Ball(tuple(x+y for x, y in zip(self.center, other.center)), min(self.error, other.error))

    def __mul__(self, other):
        return Ball(mul(self.center, other.center), min(self.error + other.lower(), other.error + self.lower()))

    def scale(self, c):
        if not c:
            return Ball()
        return Ball(tuple(c*x for x in self.center), self.error + 16*((abs(c) & -abs(c)).bit_length()-1))


def restore(record):
    if record['beta_exponent'] is None:
        return Ball(error=record['error_beta'])
    assert record['beta_exponent'] >= 0
    return Ball(mul(tuple(record['unit_beta']), power_beta(record['beta_exponent'])), record['error_beta'])


def products(frame, pairs):
    result = []
    for ci, record in enumerate(frame['CM_values']):
        jets = [[restore(x) for x in row] for row in record['actual_residue_frame_coarse_jets']]
        blocks = []
        for order in range(4):
            row = []
            for i, j in pairs:
                z = Ball()
                for k in range(order + 1):
                    z = z + jets[k][i] * jets[order-k][j]
                row.append(z)
            blocks.append(row)
        result.append(blocks)
    return result


def evaluate(row, vector):
    result = Ball()
    for value, coefficient in zip(row, vector):
        if coefficient:
            result = result + value.scale(coefficient)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--recognition', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    rec_path = DATA / (args.recognition + '.json')
    recognition = json.loads(rec_path.read_text())
    assert recognition['status'] == 'pass' and not recognition['candidate_equations_read']
    assert recognition['all_proposed_relations_pass_higher_training_digits']
    probe_ref = recognition['probe']
    assert source(probe_ref['path']) == probe_ref
    probe = json.loads(Path(probe_ref['path']).read_text())
    frame_path = DATA / 'dyadic_residue_frame1600_d138.json'
    frame = json.loads(frame_path.read_text())
    assert not frame['candidate_data_used']
    review_path = DATA / 'dyadic_precision1600_review_d138.json'
    known = {r['path']: r['sha256'] for r in json.loads(review_path.read_text())['sources']}
    assert known[str(frame_path)] == source(frame_path)['sha256']
    pairs = recognition['monomial_pairs']
    assert pairs == [[i, j] for i in range(16) for j in range(i, 16)]
    vectors = recognition['recognized_integer_vectors']
    assert len(vectors) == 91 and all(len(v) == 136 for v in vectors)
    rows = products(frame, pairs)
    results, mismatches = [], []
    tested = held_charts = held_orders = 0
    for ci, blocks in enumerate(rows):
        local = []
        for order, block in enumerate(blocks):
            values = [evaluate(block, v) for v in vectors]
            bad = [i for i, value in enumerate(values) if valuation(value.center) < value.error]
            mismatches.extend({'chart': ci, 'order': order, 'relation': i} for i in bad)
            tested += len(values)
            if ci != probe['training_chart']:
                held_charts += len(values)
            elif order not in probe['training_orders']:
                held_orders += len(values)
            local.append({'order': order, 'tested': len(values), 'certified_mismatches': bad,
                          'minimum_error_beta': min(v.error for v in values),
                          'minimum_center_or_error_beta': min(v.lower() for v in values)})
        results.append({'chart': ci, 'orders': local})
    # A perturbed recovered relation must be rejected at the withheld order.
    block = rows[probe['training_chart']][3]
    coordinate = next(i for i, value in enumerate(block) if valuation(value.center) < value.error)
    perturbed = vectors[0].copy()
    perturbed[coordinate] += 1
    bad = evaluate(block, perturbed)
    assert valuation(bad.center) < bad.error
    # Direct Horner multiplication controls, independent of saved equations.
    beta = (0, 1) + (0,) * 14
    assert mul(beta, beta) == (0, 0, 1) + (0,) * 13
    assert power_beta(16) == tuple(-x & MASK for x in POLY[:16])
    assert tested == 6188 and held_charts == 5824 and held_orders == 91
    packet = {'status': 'pass', 'milestone': 'D140', 'recognition': source(rec_path),
              'candidate_equations_read': False, 'production_ball_arithmetic_imported': False,
              'independent_arithmetic': 'absolute-error balls with integer Horner quotient products',
              'all_coefficients_checked': tested, 'withheld_chart_coefficients_checked': held_charts,
              'additional_withheld_order_coefficients_checked': held_orders,
              'total_structurally_withheld_coefficients_checked': held_charts + held_orders,
              'unused_higher_training_2_bits': probe['unused_higher_2_bits'],
              'certified_mismatches': mismatches, 'all_recovered_relations_compatible': not mismatches,
              'one_coefficient_perturbation_rejected': True, 'perturbed_coordinate': coordinate,
              'chart_results': results, 'exact_positive_vanishing_proved': False,
              'actual_harmonic_precision_increased': False,
              'wall_seconds': time.monotonic()-tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
              'sources': [source(p) for p in [Path(__file__), rec_path, Path(probe_ref['path']), frame_path, review_path]]}
    assert packet['peak_rss_bytes'] < 2 * (1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(packet, indent=2) + '\n')
    print('D140_HOLDOUT|' + json.dumps({'checked': tested, 'withheld': held_charts + held_orders,
          'mismatches': len(mismatches), 'seconds': packet['wall_seconds']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|587_DYADIC_P1600_RECOGNITION_HOLDOUT', flush=True)


if __name__ == '__main__':
    main()
