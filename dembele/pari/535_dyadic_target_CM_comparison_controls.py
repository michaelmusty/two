"""D130 target-size CM projection and comparison costs on labelled synthetic lifts.

Arbitrary high digits preserve old certified overlaps but are NOT new
arithmetic information. Synthetic quadric mismatches are never attributed
to the actual curve. Each CM order and each quadric chart is a capped job.
"""
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import re
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'dembele/pari' / filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


t = module('target_ops', '533_dyadic_target_operation_controls.py')
c = module('coarse', '475_dyadic_actual_CM_column.py')
r = module('independent', '486_dyadic_precision400_independent.py')
f = module('balls', '508_dyadic_precision800_balls.py')
h, b, w = t.h, t.b, t.w
P, BETA_PRECISION = 10552, 21168


def set_balls():
    f.PRECISION, f.R = BETA_PRECISION, f.Ring(BETA_PRECISION)
    f.beta_power.cache_clear()
    f.unit_inverse.cache_clear()
    f.BETA, f.TWO = f.Ball(f.BETACOORD), f.Ball(f.R.scale(f.ONE, 2))


def noise(label, count, bits):
    width, mask = (bits + 7) // 8, (1 << bits) - 1
    return tuple(int.from_bytes(hashlib.shake_256(f'D130-{label}-{i}'.encode()).digest(width), 'little') & mask
                 for i in range(count))


def cm_control(args):
    ci, order = args.chart, args.order
    assert ci in (0, 16) and 0 <= order < 4
    old, _ = h.read('dyadic_CM_P3200_col00_d129')
    chunk = next(row for row in old['moment_chunks'] if row['first_chart'] <= ci <= row['last_chart'])
    reader = t.q.StateReader(chunk['file'], 6400, 400, states=chunk['last_chart'] - chunk['first_chart'] + 1)
    prior = reader.row(ci - chunk['first_chart'])
    reader.close()
    values = []
    mask = (1 << 1319) - 1
    for k in range(2 * P):
        row = noise(f'CM-c{ci}-k{k}', 8, 1319)
        values.append(tuple(((v << 400) | u) & mask for v, u in zip(row, prior[k])) if k < 6400 else row)
    start = time.monotonic()
    if args.method == 'direct':
        ring = c.Ring(BETA_PRECISION)
        pi = ring.add(ring.scale(ring.mul(c.BETA, c.BETA), -1), ring.scale(c.ONE, -2))
        q = ring.add(tuple(c.MP[1:]), ring.scale(c.BETA, -1))
        powers = ring.powers(pi, 7)
        assert ring.mul(q, c.BETA) == pi
    else:
        ring = r.Quotient(r.MP, BETA_PRECISION)
        pi = ring.sub(ring.scale(ring.one, -2), ring.mul(ring.beta, ring.beta))
        q = ring.sub(tuple(r.MP[1:]), ring.beta)
        powers = [ring.one]
        for _ in range(7):
            powers.append(ring.mul(powers[-1], pi))
        assert ring.mul(q, ring.beta) == pi
    embedded = []
    for row in values:
        x = c.ZERO
        for v, power in zip(row, powers):
            x = ring.add(x, ring.scale(power, v))
        embedded.append(x)
    embedding_seconds = time.monotonic() - start
    n = 2 * order + 2
    tick = time.monotonic()
    if args.method == 'direct':
        qp = c.ONE
        answer = c.ZERO
        for k, moment in enumerate(embedded):
            answer = ring.add(answer, ring.mul(ring.scale(qp, c.coefficient(n, k)), moment))
            qp = ring.mul(qp, q)
    else:
        answer = c.ZERO
        for k in range(2 * P - 1, -1, -1):
            coefficient = -sum(comb(n, i) * comb(n + k - i - 1, k - i)
                              for i in range(min(n, k) + 1)) if k else 0
            answer = ring.add(ring.mul(answer, q), ring.scale(embedded[k], coefficient))
    projection_seconds = time.monotonic() - tick
    previous = tuple(old['CM_values'][ci]['coarse_coefficients_beta'][order])
    difference = ring.add(answer, ring.scale(previous, -1))
    assert ring.value(difference) >= old['coarse_error_beta'][order]
    return {'chart': ci, 'order': order, 'method': args.method,
        'input_kind': 'synthetic_high_digit_completion_of_actual_P3200_CM_row',
        'input_moments': 2 * P, 'input_modulus_bits': 1319,
        'CM_arithmetic_precision_beta': BETA_PRECISION,
        'old_actual_coarse_overlap_beta': old['coarse_error_beta'][order],
        'embedding_seconds': embedding_seconds, 'projection_seconds': projection_seconds,
        'coarse_value_beta': list(answer),
        'input_sha256': hashlib.sha256(b.pack([values], 1319)).hexdigest(),
        'actual_CM_precision_increased': False}


def frame_control():
    set_balls()
    packet, _ = h.read('dyadic_precision800_d125')
    algebraic, _ = h.read('dyadic_CM_frame_beta21168_d122')
    oldframe, _ = h.read('dyadic_residue_frame800_d125')
    errors = [2 * P + gain for gain in (32, 48, 32, 64)]
    assert algebraic['rational_residue_frame_error_beta'] >= max(errors)
    assert algebraic['all_original_Hensel_branches_preserved']
    begin = time.monotonic()
    jets = []
    for ci, row in enumerate(packet['CM_values']):
        jet = []
        for n, entries in enumerate(row['coarse_coefficients_beta']):
            balls = []
            for j, old in enumerate(entries):
                oldbits = (packet['coarse_error_beta'][n] + 15) // 16
                high = noise(f'frame-{ci}-{n}-{j}', 16, f.R.bits)
                center = tuple((int(v) + (z << oldbits)) & f.R.mask for v, z in zip(old, high))
                assert f.R.value(f.R.add(center, f.R.scale(tuple(old), -1))) >= packet['coarse_error_beta'][n]
                balls.append(f.center(center, errors[n]))
            jet.append(balls)
        jets.append(jet)
    scales, leading = [], []
    for ci, jet in enumerate(jets):
        v = min(x.v for x in jet[0] if x.known_nonzero())
        assert v == (296 if ci == 0 else 33)
        scale = f.BETA ** v
        scales.append(scale)
        leading.append([x / scale for x in jet[0]])
    inv, pivots = f.inverse(leading[1:])
    relation = f.multiply([leading[0]], inv)[0]
    assert all(x.known_nonzero() and x.v == -35 for x in relation)
    eta = [[f.center(x, algebraic['rational_residue_frame_error_beta']) for x in row]
           for row in algebraic['rational_residue_frame_values']]
    change = f.multiply(inv, [[x / relation[i] for x in eta[i + 1]] for i in range(16)])
    actual = [f.multiply(jet, change) for jet in jets]
    for ci in range(17):
        expected = [-x * scales[0] if ci == 0 else x * scales[ci] / relation[ci - 1] for x in eta[ci]]
        assert all(not (x - y).known_nonzero() for x, y in zip(actual[ci][0], expected))
        for n in range(4):
            for x, prior in zip(actual[ci][n], oldframe['CM_values'][ci]['actual_residue_frame_coarse_jets'][n]):
                assert not (x - f.restore(prior)).known_nonzero()
    assert min(x.lower() for row in change for x in row) >= 0
    return {'input_kind': 'synthetic_high_digit_completion_of_actual_P800_differential_bank',
        'arithmetic_precision_beta': BETA_PRECISION, 'synthetic_input_errors_beta': errors,
        'existing_algebraic_eta_error_beta': algebraic['rational_residue_frame_error_beta'],
        'existing_eta_precision_suffices_for_target': True,
        'frame_seconds': time.monotonic() - begin,
        'old_actual_jet_overlap_count': 1088, 'leading_frame_identities_checked': 272,
        'evaluation_inverse_pivots': pivots,
        'minimum_change_error_beta': min(x.error for row in change for x in row),
        'CM_values': [{'CM_index': ci, 'synthetic_residue_frame_jets': [[x.saved() for x in row] for row in jet]}
                      for ci, jet in enumerate(actual)],
        'candidate_data_used_to_construct_frame': False,
        'actual_differential_precision_increased': False}


def quadric_control(args):
    set_balls()
    packet, path = h.read(args.previous)
    assert packet['phase'] == 'frame'
    frame = packet['certificates']
    assert frame['input_kind'].startswith('synthetic_')
    candidate_path = DATA / 'cm_frame_curve_candidate.json'
    candidate = json.loads(candidate_path.read_text())
    h.PATHS.add(candidate_path)
    ci = args.chart
    assert 0 <= ci < 17
    jet = [[f.restore(x) for x in row] for row in frame['CM_values'][ci]['synthetic_residue_frame_jets']]
    begin = time.monotonic()
    monomials = []
    for i, j in candidate['monomial_pairs']:
        coefficients = []
        for n in range(4):
            z = f.Ball()
            for k in range(n + 1):
                z = z + jet[k][i] * jet[n - k][j]
            coefficients.append(z)
        monomials.append(coefficients)
    product_seconds = time.monotonic() - begin
    tick = time.monotonic()
    values = []
    counts = [0] * 4
    for quadric in candidate['quadrics']:
        row = []
        for n in range(4):
            z = f.Ball()
            for coeff, monomial in zip(quadric, monomials):
                if coeff:
                    z = z + monomial[n].scale_integer(coeff)
            counts[n] += int(z.known_nonzero())
            row.append(z.saved())
        values.append(row)
    relation_seconds = time.monotonic() - tick
    assert counts[0] == 0
    return {'input_kind': frame['input_kind'], 'synthetic_frame_metadata': h.source(path),
        'chart': ci, 'quadrics': 91, 'coarse_orders': 4,
        'monomial_product_seconds': product_seconds, 'quadric_relation_seconds': relation_seconds,
        'synthetic_nonzero_coefficients_by_order': counts,
        'synthetic_quadric_values': values,
        'synthetic_nonzeros_are_not_candidate_mismatches': True,
        'candidate_identification_proved': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('cm', 'frame', 'quadrics'), required=True)
    p.add_argument('--method', choices=('direct', 'horner'), default='direct')
    p.add_argument('--chart', type=int, default=0)
    p.add_argument('--order', type=int, default=0)
    p.add_argument('--previous')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    begin = time.monotonic()
    cert = cm_control(args) if args.phase == 'cm' else frame_control() if args.phase == 'frame' else quadric_control(args)
    h.PATHS.update([Path(__file__), Path(t.__file__), Path(c.__file__), Path(r.__file__), Path(f.__file__),
        Path(t.c.__file__), Path(t.q.__file__), Path(h.__file__), Path(b.__file__), Path(w.__file__)])
    result = {'status': 'pass', 'milestone': 'D130', 'phase': args.phase, 'certificates': cert,
        'wall_seconds': time.monotonic() - begin, 'peak_rss_bytes': w.peak_rss(),
        'actual_harmonic_precision_increased': False,
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(h.source(out)), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|535_DYADIC_TARGET_CM_COMPARISON_CONTROLS', flush=True)
