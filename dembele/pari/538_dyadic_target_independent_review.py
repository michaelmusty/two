"""D130 independent finite checks of controls and the downstream twist witness.

No production arithmetic is imported. Original actions use ordinary power
recurrences in a separate integer quotient; target action checks are samples.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
spec = importlib.util.spec_from_file_location('separate', ROOT / 'dembele/pari/486_dyadic_precision400_independent.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
PATHS = {Path(__file__), Path(r.__file__)}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return r.source(path)


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet, path


def binary(record, rows, count, bits):
    assert source(record['path']) == record
    width = (bits + 7) // 8
    raw = Path(record['path']).read_bytes()
    assert len(raw) == rows * count * 8 * width
    return [[tuple(int.from_bytes(raw[((e * count + k) * 8 + i) * width:((e * count + k) * 8 + i + 1) * width], 'little')
                   for i in range(8)) for k in range(count)] for e in range(rows)]


def old_row(P, state):
    stem = {800: 'dyadic_staged_P800_col00_verified_d123',
            1600: 'dyadic_weighted_P1600_col00_verified_d124',
            3200: 'dyadic_streamed_P3200_col00_verified_d129'}[P]
    packet, _ = read(stem)
    record = packet['state_file']
    assert source(record['path']) == record
    width = (P // 8 + 7) // 8
    length = P * 8 * width
    with Path(record['path']).open('rb') as f:
        f.seek(state * length)
        raw = f.read(length)
    assert len(raw) == length
    return [tuple(int.from_bytes(raw[(k * 8 + i) * width:(k * 8 + i + 1) * width], 'little')
                  for i in range(8)) for k in range(P)]


def digest_row(values, bits):
    width = (bits + 7) // 8
    sha = hashlib.sha256()
    for x in values:
        for v in x:
            sha.update(v.to_bytes(width, 'little'))
    return sha.hexdigest()


def action(args):
    packet, path = read(args.input)
    cert = packet['certificates']
    P, bits, count = cert['working_precision_pi'], cert['modulus_bits'], cert['input_moment_count']
    ring = r.Quotient(r.FP, 8 * bits)
    transport, _ = read('dyadic_target_transports_d121')
    mode, e, branch = cert['mode'], cert['state_or_CM_index'], cert['branch']
    if mode == 'cm':
        charts = [x for x in transport['CM_charts'] if x['chart'] == 'A']
        chart = charts[e]
        child = transport['transitions'][chart['target_edge']]['children'][branch]
        A, B, C = map(ring.norm, chart['normalized_center'][:3])
        a, b, c = map(ring.norm, child['normalized_center'][:3])
        den = ring.add(ring.one, ring.mul(C, b))
        inv = ring.one
        for _ in range(P.bit_length()):
            inv = ring.mul(inv, ring.sub(ring.scale(ring.one, 2), ring.mul(den, inv)))
        assert ring.mul(den, inv) == ring.one
        pars = [ring.mul(ring.add(ring.mul(A, a), ring.mul(B, c)), inv),
                ring.mul(ring.add(ring.mul(A, b), B), inv),
                ring.mul(ring.add(c, ring.mul(C, a)), inv)]
    else:
        child = transport['transitions'][e]['children'][branch]
        pars = list(map(ring.norm, child['normalized_center'][:3]))
    assert child['target_edge'] == cert['target_child_state']
    assert digest_row(pars, bits) == cert['parameters_sha256']
    if mode == 'extend':
        values = old_row(cert['seed_precision_pi'], child['target_edge'])
        masses, _ = read('dyadic_harmonic_certificate_d111')
        values[0] = (masses['harmonic_basis'][0][child['target_edge']] & ring.mask,) + (0,) * 7
    else:
        label = f"D130-input-P{P}-u{cert['known_lower_valuation_pi']}-child{child['target_edge']}"
        width = (bits + 7) // 8
        values = [tuple(int.from_bytes(hashlib.shake_256(f'{label}:0:{k}:{i}'.encode()).digest(width), 'little') & ring.mask
                        for i in range(8)) for k in range(count)]
        if mode in ('rhs', 'correction-rhs'):
            values[1:33] = [ring.zero] * min(32, count - 1)
        if mode in ('correction', 'correction-rhs'):
            values[0] = ring.zero
    assert digest_row(values, bits) == cert['input_sha256']
    answer = binary(cert['answer'], 1, cert['output_moment_count'], bits)[0]
    degrees = (1, 2, 3)
    a, b, c = pars
    power = [ring.one] + [ring.zero] * (count - 1)
    begin = time.monotonic()
    for n in range(1, 4):
        new = [ring.mul(b, power[0])]
        for k in range(1, count):
            new.append(ring.sub(ring.add(ring.mul(b, power[k]), ring.mul(a, power[k - 1])), ring.mul(c, new[-1])))
        power = new
        value = ring.zero
        for x, y in zip(power, values):
            value = ring.add(value, ring.mul(x, y))
        assert value == answer[n], (mode, e, branch, n)
    assert answer[0] == values[0]
    return {'input_metadata': source(path), 'mode': mode, 'independent_power_degrees': list(degrees),
        'independent_original_action_scalar_checks': 24, 'zeroth_scalars_checked': 8,
        'input_moments': count, 'modulus_bits': bits,
        'recurrence_seconds': time.monotonic() - begin,
        'full_action_independently_recomputed': False}


def aggregate():
    names = ['dyadic_target_full_e000_b0_adaptive_d130', 'dyadic_target_full_e000_b0_gmp_d130',
             'dyadic_target_extend3200_e000_b0_adaptive_d130']
    for plan in ('dyadic_target_map_plan_d130', 'dyadic_target_dense_schedule_plan_d130'):
        packet, _ = read(plan + '_completed')
        names.extend(x['stem'] for x in packet['jobs'])
    assert len(names) == len(set(names)) == 74
    groups = {}
    for stem in names:
        packet, _ = read(stem)
        c = packet['certificates']
        assert source(c['answer']['path']) == c['answer']
        key = tuple(c[x] for x in ('working_precision_pi', 'mode', 'state_or_CM_index', 'branch',
                                   'seed_precision_pi', 'known_lower_valuation_pi'))
        groups.setdefault(key, {})[c['backend']] = c
    checks = pairs = 0
    for key, pair in groups.items():
        if len(pair) == 1:
            assert 'ADAPTIVE' in pair
            continue
        assert set(pair) == {'ADAPTIVE', 'GMP'}
        a, b = pair['ADAPTIVE'], pair['GMP']
        for field in ('input_sha256', 'parameters_sha256', 'input_moment_count', 'output_moment_count', 'modulus_bits'):
            assert a[field] == b[field]
        with Path(a['answer']['path']).open('rb') as x, Path(b['answer']['path']).open('rb') as y:
            while raw := x.read(1 << 20):
                assert raw == y.read(len(raw))
            assert not y.read(1)
        pairs += 1
        checks += 8 * a['output_moment_count']
    assert pairs == 26
    # The two actual extension children sum to the saved P=3200 state.
    packets = [read(f'dyadic_target_extend3200_e000_b{branch}_adaptive_d130')[0]['certificates'] for branch in (0, 1)]
    values = [binary(x['answer'], 1, 10552, 1319)[0] for x in packets]
    old = old_row(3200, 0)
    mask = (1 << 400) - 1
    assert [tuple((x + y) & mask for x, y in zip(a, b)) for a, b in zip(values[0][:3200], values[1][:3200])] == old
    cm = []
    for n in range(4):
        direct, _ = read(f'dyadic_target_coarse_c00_n{n}_direct_d130')
        horner, _ = read(f'dyadic_target_coarse_c00_n{n}_horner_d130')
        a, b = direct['certificates'], horner['certificates']
        assert a['input_sha256'] == b['input_sha256'] and a['coarse_value_beta'] == b['coarse_value_beta']
        cm.append({'order': n, 'old_coarse_error_beta': a['old_actual_coarse_overlap_beta']})
    for first, stop in ((0, 55), (55, 110), (110, 165)):
        one, _ = read(f'dyadic_target_low_profile_c01_g{first:03d}_{stop:03d}_d130')
        many, _ = read(f'dyadic_target_low_profile_c16_g{first:03d}_{stop:03d}_d130')
        assert one['certificates']['first_column_output_sha256'] == many['certificates']['first_column_output_sha256']
    frame, _ = read('dyadic_target_synthetic_frame_d130')
    assert frame['certificates']['minimum_change_error_beta'] >= 2 * 10552 + 32 - 296
    return {'map_control_jobs': 74, 'complete_backend_comparison_pairs': pairs,
        'complete_backend_scalar_comparisons': checks, 'additional_single_backend_cost_controls': 22,
        'actual_old_extension_sum_scalar_overlaps': 3200 * 8,
        'complete_CM_direct_Horner_value_comparisons': 4, 'CM_old_overlaps': cm,
        'low_profile_first_column_matches_for_all_165_groups': True,
        'synthetic_frame_error_meets_D120_design': True, 'actual_precision_increased': False}


def low():
    transport, _ = read('dyadic_target_transports_d121')
    prior_values = None
    prefix_checks = sampled = 0
    stages = []
    for bits in (200, 400, 600, 800, 1000, 1200, 1319):
        stem = f'dyadic_target_low_c01_bits{bits}_d130'
        solved, _ = read(stem + '_solve')
        checked, _ = read(stem + '_verify')
        cert = solved['certificates']
        assert checked['certificates']['all_original_sparse_equations_zero']
        assert checked['certificates']['original_sparse_scalar_equations_checked'] == 44544
        values = binary(cert['answer'], 174, 32, bits)
        if prior_values is not None:
            mask = (1 << cert['old_bits']) - 1
            assert [[tuple(v & mask for v in x) for x in row] for row in values] == prior_values
            prefix_checks += 44544
            residual, _ = read(stem + '_residual')
            assert residual['certificates']['exact_residual_divisions_checked'] == 44544
        ring = r.Quotient(r.FP, 8 * bits)
        for e in (0, 83, 173):
            totals = [ring.zero for _ in range(32)]
            for child in transport['transitions'][e]['children']:
                a, b, c = map(ring.norm, child['normalized_center'][:3])
                power = [ring.one] + [ring.zero] * 32
                for n in range(1, 33):
                    new = [ring.mul(b, power[0])]
                    for k in range(1, 33):
                        new.append(ring.sub(ring.add(ring.mul(b, power[k]), ring.mul(a, power[k - 1])), ring.mul(c, new[-1])))
                    power = new
                    for x, y in zip(power[1:], values[child['target_edge']]):
                        totals[n - 1] = ring.add(totals[n - 1], ring.mul(x, y))
            for n, total in enumerate(totals):
                expected = tuple(int.from_bytes(hashlib.shake_256(f'D130-low-rhs-state{e}:{n}:0:{i}'.encode()).digest(165), 'little') & ring.mask
                                 for i in range(8))
                assert ring.sub(values[e][n], total) == expected
                sampled += 8
        stages.append({'bits': bits, 'correction_bits': cert['correction_bits'],
            'complete_production_original_equations': 44544, 'independent_sampled_original_scalars': 768})
        prior_values = values
    assert stages[-1]['correction_bits'] == 119 and prefix_checks == 267264 and sampled == 5376
    return {'stages': stages, 'all_stage_prefix_scalar_comparisons': prefix_checks,
        'independent_ordinary_low_equation_scalar_checks': sampled,
        'new_factor_constructed': False, 'actual_harmonic_precision_increased': False}


def quadrics(ci):
    frame, _ = read('dyadic_target_synthetic_frame_d130')
    production, _ = read(f'dyadic_target_synthetic_quadrics_c{ci:02d}_d130')
    path = DATA / 'cm_frame_curve_candidate.json'
    PATHS.add(path)
    candidate = json.loads(path.read_text())
    ring = r.Quotient(r.MP, 21168)
    def center(ball):
        v = ball['beta_exponent']
        if v is None:
            return ring.zero
        assert v >= 0
        return ring.mul(ring.norm(ball['unit_beta']), ring.power_beta(v))
    jets = [[center(x) for x in row] for row in frame['certificates']['CM_values'][ci]['synthetic_residue_frame_jets']]
    monomials = []
    for i, j in candidate['monomial_pairs']:
        row = []
        for n in range(4):
            z = ring.zero
            for k in range(n + 1):
                z = ring.add(z, ring.mul(jets[k][i], jets[n - k][j]))
            row.append(z)
        monomials.append(row)
    count = 0
    for qi, coeffs in enumerate(candidate['quadrics']):
        for n in range(4):
            z = ring.zero
            for coeff, row in zip(coeffs, monomials):
                z = ring.add(z, ring.scale(row[n], coeff))
            ball = production['certificates']['synthetic_quadric_values'][qi][n]
            assert ring.value(ring.sub(z, center(ball))) >= min(21168, ball['error_beta'])
            count += 1
    return {'chart': ci, 'synthetic_quadric_coefficient_comparisons': count,
        'method': 'independent_integer_quotient_with_absolute_errors',
        'actual_candidate_mismatch_claimed': False}


def bridge():
    f = r.FP
    norm = sum(c * (-1) ** i for i, c in enumerate(f))
    value = sum(c * 27 ** i for i, c in enumerate(f))
    derivative = sum(i * c * 27 ** (i - 1) for i, c in enumerate(f) if i)
    assert norm == -1 and value % 31 == 0 and derivative % 31 != 0
    assert (1 + 27) % 31 == 20 ** 2 % 31 and (2 * 20) % 31 != 0
    return {'base_field_polynomial': list(f), 'unit_delta': '1+b', 'norm_delta': norm,
        'norm_identity': 'Norm(1+b)=f(-1)=-1; a square has square rational norm',
        'norm31_place_b_residue': 27, 'base_polynomial_residual_mod31': value % 31,
        'base_polynomial_derivative_mod31': derivative % 31,
        'delta_residue_mod31': 28, 'simple_square_root_mod31': 20,
        'square_root_derivative_mod31': (2 * 20) % 31,
        'quadratic_extension_unramified_away_from_2_reason': 'delta is an integral unit; discriminant of z^2-delta is 4*delta',
        'deduction': 'delta is nonsquare over F but square at the selected norm31 completion; local agreement and ramification support do not remove scalar twist ambiguity',
        'candidate_twist_identified_or_disproved': False,
        'reference': 'https://stacks.math.columbia.edu/tag/03PK'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('action', 'aggregate', 'low', 'quadrics', 'bridge'), required=True)
    p.add_argument('--input')
    p.add_argument('--chart', type=int)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    begin = time.monotonic()
    cert = action(args) if args.phase == 'action' else aggregate() if args.phase == 'aggregate' else low() if args.phase == 'low' else quadrics(args.chart) if args.phase == 'quadrics' else bridge()
    result = {'status': 'pass', 'milestone': 'D130', 'phase': args.phase, 'certificates': cert,
        'production_arithmetic_not_imported': True, 'wall_seconds': time.monotonic() - begin,
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
        'sources': [source(path) for path in sorted(PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|538_DYADIC_TARGET_INDEPENDENT_REVIEW', flush=True)
