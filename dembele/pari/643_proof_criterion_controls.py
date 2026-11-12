"""D155 independent rank replay, uncollected heights and failure controls.

The rank replay uses convolution in the Eisenstein quotient, not production
balls, source 587's Horner products, or a fresh elimination. The numerical
height replay uses source 450's different logarithm series. Run capped.
"""
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'proof_criterion_controls_d155.json'
HELPER = ROOT / 'dembele/pari/450_cm_disk_exactness_review.py'
PATHS = {Path(__file__), HELPER}
POLY = [2, 0, 64, 0, 336, 0, 672, 0, 660, 0, 352, 0, 104, 0, 16, 0, 1]
PRECISION = 4096
MODULUS = 1 << (PRECISION//16)
ZERO = (0,)*16


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read(stem):
    path = DATA / (stem+'.json')
    source(path)
    obj = json.loads(path.read_text())
    assert obj['status'] == 'pass', stem
    return obj


def multiply(a, b):
    answer = [0]*31
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            answer[i+j] += x*y
    for k in range(30, 15, -1):
        c = answer[k]
        for j in range(16):
            answer[k-16+j] -= c*POLY[j]
    return tuple(x % MODULUS for x in answer[:16])


def beta_power(n):
    value, base = (1,)+(0,)*15, (0, 1)+(0,)*14
    while n:
        if n & 1:
            value = multiply(value, base)
        base = multiply(base, base)
        n //= 2
    return value


def valuation(a):
    return min([PRECISION]+[16*((x & -x).bit_length()-1)+i for i, x in enumerate(a) if x])


def restore(obj):
    error = min(PRECISION, obj['error_beta'])
    n = obj['beta_exponent']
    if n is None:
        return ZERO, error
    assert n >= 0
    return multiply(tuple(x % MODULUS for x in obj['unit_beta']), beta_power(n)), error


def add(a, b):
    return tuple((x+y) % MODULUS for x, y in zip(a[0], b[0])), min(a[1], b[1])


def product(a, b):
    return multiply(a[0], b[0]), min(a[1]+min(valuation(b[0]), b[1]), b[1]+min(valuation(a[0]), a[1]), PRECISION)


def divide_beta(a, n):
    for _ in range(n):
        assert a[0] % 2 == 0
        half = a[0]//2
        a = tuple(((a[i+1] if i < 15 else 0)-half*POLY[i+1]) % MODULUS for i in range(16))
    return a


def rank_replay():
    frame = read('dyadic_residue_frame1600_d138')
    assert not frame['candidate_data_used'] and frame['working_precision_pi'] == 1600
    rows = []
    for bits in (96, 160):
        probe = read(f'dyadic_P1600_relation_probe{bits}_d140')
        packet = read(f'dyadic_P1600_recognition_certificates{bits}_d140')
        cert = packet['certificates']
        assert not probe['candidate_equations_read'] and not packet['candidate_equations_read']
        assert probe['training_chart'] == 1 and probe['training_orders'] == [0, 1, 2]
        pairs = [[i, j] for i in range(16) for j in range(i, 16)]
        assert probe['monomial_pairs'] == pairs
        jets = [[restore(v) for v in row] for row in frame['CM_values'][1]['actual_residue_frame_coarse_jets']]
        replay = []
        for record in probe['block_error_bounds']:
            n, shift = record['order'], record['divided_beta_power']
            assert n in (0, 1, 2)
            block = []
            for i, j in pairs:
                value = ZERO, PRECISION
                for k in range(n+1):
                    value = add(value, product(jets[k][i], jets[n-k][j]))
                block.append(value)
            assert all(min(valuation(c), e) >= shift for c, e in block)
            error = min(e-shift for _, e in block)
            assert error >= record['absolute_error_beta_after_division']
            usable = record['coefficient_error_2_bits']
            assert usable <= error//16 and usable >= bits
            centers = [divide_beta(c, shift) for c, _ in block]
            replay.extend([[a[j] % (1 << usable) for a in centers] for j in range(16)])
        assert replay == probe['matrix_rows'] and len(replay) == 48
        selected, columns = cert['selected_original_rows'], cert['pivot_columns']
        assert len(set(selected)) == len(set(columns)) == 45
        assert all(0 <= i < 48 for i in selected) and all(0 <= j < 136 for j in columns)
        B = [[replay[i][j] for j in columns] for i in selected]
        N = cert['inverse_numerator_mod_2_power']
        loss = cert['inverse_denominator_2_power']
        assert loss == 13 and bits == cert['inverse_certificate_modulus_2_bits'] > loss
        modulus = 1 << bits
        assert len(N) == 45 and all(len(row) == 45 for row in N)
        assert all(0 <= x < modulus for row in N for x in row)
        assert all((sum(N[i][k]*B[k][j] for k in range(45))-(1 << loss)*(i == j)) % modulus == 0
                   for i in range(45) for j in range(45))
        # Multiplying an uncertain matrix by integral N preserves its
        # entrywise 2^bits error. Dividing by 2^loss leaves a strict unit ball.
        assert bits-loss > 0
        rows.append({'training_2_bits': bits, 'replayed_actual_matrix_entries': 48*136,
                     'minor_size': 45, 'inverse_loss_bits': loss,
                     'Neumann_remainder_2_valuation_at_least': bits-loss,
                     'all_matrix_errors_cover_certificate_modulus': True})
    assert multiply((0, 1)+(0,)*14, (0, 1)+(0,)*14) == (0, 0, 1)+(0,)*13
    assert beta_power(16) == tuple(-x % MODULUS for x in POLY[:16])
    return rows


def independent_bounds():
    spec = importlib.util.spec_from_file_location('d155_other_log_series', HELPER)
    logs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(logs)
    packet = read('proof_criterion_bounds_d155')
    for ref in packet['sources']:
        assert source(ref['path']) == ref
    h = Q(packet['Hodge_height_upper'])
    theta = Q(packet['tropical_coefficient'])
    H = logs.plus((2*h, 2*h), logs.scale(logs.L2, -Q(35, 34)))
    pi = logs.rounded(logs.plus(logs.scale(logs.atan(Q(1, 5)), 16), logs.scale(logs.atan(Q(1, 239)), -4)))
    logpi = logs.log(pi[0])[0], logs.log(pi[1])[1]
    Fminus = logs.plus(logs.scale(logpi, -16), logs.scale(logs.L2, theta-8))
    logB = logs.plus(logs.scale(logpi, -Q(1, 2)), logs.log(Q(5, 3)))
    C = [logs.scale(logs.sqrt(2), 2), logs.plus(logs.scale(logs.sqrt(3), 2), (Q(2),)*2),
         logs.plus((Q(4),)*2, logs.scale(logs.sqrt(6), 2))]
    results = []
    for n, row in enumerate(packet['thresholds'], 1):
        logC = logs.log(C[n-1][0])[0], logs.log(C[n-1][1])[1]
        norm = logs.plus(logs.log(480*42550), logs.scale(logs.L2, 70), logs.scale(logB, 238),
                         logC, logs.scale(logpi, -1), logs.scale(logs.log(Q(5, 3)), n+2))
        upper = logs.plus(logs.scale(H, 240+n), logs.scale(Fminus, -15), norm)
        saved = tuple(map(Q, row['finite_zero_upper_interval']))
        assert max(upper[0], saved[0]) <= min(upper[1], saved[1])
        P = row['minimum_P_multiple_of_8']
        for p, positive in ((P, True), (P-8, False)):
            coefficient = Q(16*(2*p+3310-33*n)+(2*p+2784-296*n), 272)
            lower = logs.scale(logs.L2, coefficient)
            assert (lower[0] > upper[1]) if positive else (lower[1] < upper[0])
        results.append(P)
    assert results == [10416, 10480, 10552]
    return results


def failure_controls():
    # A zero-containing error ball need not be the singleton zero.
    assert (1 << 20) % (1 << 20) == 0 and (1 << 20) != 0
    # At equality the product formula does not contradict a nonzero section.
    assert Q(20) == Q(20) and not Q(20) > Q(20)
    # A modular inverse certificate needs modulus bits strictly beyond loss:
    # B=0, N=1 passes NB=2^13 modulo 2^13 despite rank(B)=0.
    assert (0-(1 << 13)) % (1 << 13) == 0
    assert (0-(1 << 13)) % (1 << 14) != 0
    # Restriction of scalars: 1, sqrt(2) span a 1-dimensional Q(sqrt(2))
    # target but have a rank-2 rational coordinate matrix.
    images_in_power_basis = [(1, 0), (0, 1)]
    rational_coordinate_determinant = (images_in_power_basis[0][0]*images_in_power_basis[1][1]
                                       -images_in_power_basis[0][1]*images_in_power_basis[1][0])
    assert rational_coordinate_determinant == 1
    # q(t)=a*t+b*t^2, t=s+c*s^2. Its order-two coefficient becomes
    # b+a*c; a merely divisible by 2^20 does not make this invariant.
    a, b, c = 1 << 20, 7, 3
    assert b+a*c != b and b+0*c == b
    # The nodal binomial operator is integral on all Laurent monomials;
    # D^2/2 is not integral without the lower-jet vanishing hypothesis.
    for exponent in range(-30, 31):
        for n in (1, 2, 3):
            value = Q(1)
            for k in range(n):
                value *= Q(exponent-k, k+1)
            assert value.denominator == 1
    assert Q(1, 2).denominator != 1
    # Exact affine error offsets, independently reconstructed from losses.
    E = 2*10480+32
    inverse_error = E-33-2*35
    relation_error = min((E-296)-35, inverse_error)
    reciprocal_error = relation_error+2*35
    change_error = min(inverse_error+35, reciprocal_error-35)
    assert (inverse_error, relation_error, reciprocal_error, change_error) == (E-103, E-331, E-261, E-296)
    assert (E-33)-35 > 0 and relation_error > -35
    return {'zero_containment_does_not_imply_exact_zero': True,
            'non_strict_height_inequality_rejected': True,
            'rank_certificate_at_precision_loss_boundary_rejected': True,
            'extension_field_dimension_cannot_bound_restricted_scalar_rank': True,
            'second_jet_depends_on_first_jet_until_exact_vanishing': True,
            'nodal_binomial_integrality_controls': 61*3,
            'matrix_error_offsets_reconstructed': [103, 331, 261, 296],
            'controls_are_examples_not_proofs_of_general_geometry': True}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    ranks = rank_replay()
    thresholds = independent_bounds()
    controls = failure_controls()
    result = {'status': 'pass', 'milestone': 'D155', 'rank_replays': ranks,
              'rank_replay_candidate_equations_read': False,
              'rank_replay_production_ball_arithmetic_imported': False,
              'independent_uncollected_height_thresholds': thresholds,
              'failure_controls': controls,
              'geometric_implications_require_companion_proof': True,
              'actual_harmonic_precision_increased': False,
              'exact_positive_vanishing_proved': False, 'new_precision_bank_admitted': False,
              'wall_seconds': time.monotonic()-tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    result['sources'] = [source(p) for p in sorted(PATHS)]
    with OUT.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print('D155_CONTROLS|'+json.dumps({'rank_replays': ranks, 'thresholds': thresholds, 'controls': controls}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(OUT)), flush=True)
    print('PASS|643_PROOF_CRITERION_CONTROLS', flush=True)
