"""D155 fresh rational bounds and exact CM-frame checks.

Run only through run_dyadic_capped.py. No new harmonic data are computed.
All numerical decisions use outward rational intervals, never floats.
"""
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'proof_criterion_bounds_d155.json'
PATHS = {Path(__file__)}
UNIT = 1 << 192


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read(stem, passing=True):
    path = DATA / (stem + '.json')
    source(path)
    obj = json.loads(path.read_text())
    if passing:
        assert obj['status'] == 'pass', stem
    return obj


def rounded(a):
    return Q((a[0]*UNIT).__floor__(), UNIT), Q((a[1]*UNIT).__ceil__(), UNIT)


def plus(*args):
    return rounded((sum(a[0] for a in args), sum(a[1] for a in args)))


def scale(a, c):
    return rounded((a[0]*c, a[1]*c) if c >= 0 else (a[1]*c, a[0]*c))


def times(a, b):
    xs = [x*y for x in a for y in b]
    return rounded((min(xs), max(xs)))


def log_unit(q):
    # log(q)=2*atanh((q-1)/(q+1)); 96 terms and a uniform tail.
    assert 1 <= q <= 2
    z = Q(q-1, q+1)
    power = rounded((z, z))
    square = rounded((z*z, z*z))
    total = (Q(0), Q(0))
    for k in range(96):
        total = plus(total, scale(power, Q(2, 2*k+1)))
        power = times(power, square)
    tail = 2*Q(1, 3)**193 / (193*(1-Q(1, 9)))
    return plus(total, (Q(0), tail))


LOG2 = log_unit(Q(2))


def log(q):
    q = Q(q)
    assert q > 0
    exponent = 0
    while q >= 2:
        q /= 2
        exponent += 1
    while q < 1:
        q *= 2
        exponent -= 1
    return plus(log_unit(q), scale(LOG2, exponent))


def atan(q):
    partial = sum((-1)**k*q**(2*k+1)/Q(2*k+1) for k in range(96))
    return rounded((partial, partial+q**193/193))


def root(n):
    k = isqrt(n*UNIT*UNIT)
    assert k*k <= n*UNIT*UNIT < (k+1)*(k+1)
    return Q(k, UNIT), Q(k+1, UNIT)


def encode(a):
    return [str(x) for x in a]


def overlap(a, b):
    assert max(a[0], b[0]) <= min(a[1], b[1])


def polynomial_product(a, b, polynomial):
    degree = len(polynomial)-1
    answer = [Q(0)]*(2*degree-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            answer[i+j] += x*y
    for k in range(2*degree-2, degree-1, -1):
        for j in range(degree):
            answer[k-degree+j] -= answer[k]*polynomial[j]
    return answer[:degree]


def cm_frame_checks():
    candidate = read('cm_frame_curve_candidate', False)
    polynomial = candidate['CM_field_polynomial_ascending']
    assert len(polynomial) == 18 and polynomial[-1] == 1
    eta = [list(map(Q, row)) for row in candidate['CM_projective_coordinates_power_basis']]
    assert len(eta) == 16 and all(len(row) == 17 for row in eta)
    pairs = [[i, j] for i in range(16) for j in range(i, 16)]
    assert candidate['monomial_pairs'] == pairs
    products = [polynomial_product(eta[i], eta[j], polynomial) for i, j in pairs]
    quadrics = candidate['quadrics']
    assert len(quadrics) == 91 and all(len(row) == 136 for row in quadrics)
    assert all(all(sum(c*products[k][j] for k, c in enumerate(row)) == 0
                   for j in range(17)) for row in quadrics)
    norms = [sum(abs(c) for c in row) for row in quadrics]
    assert max(norms) == 42550
    # Reproduce the archimedean vector bound from |theta|<4, inherited
    # from D103. Integrality of the saved field basis remains inherited.
    bounds = [sum(abs(17*c)*4**j for j, c in enumerate(row)) for row in eta]
    assert max(bounds) < 2**35
    basis = read('cm_field_recognition', False)['field_basis']
    assert eta == [list(map(Q, row)) for row in basis['trace_centered_basis_power_coordinates'][1:]]
    integral = [list(map(Q, row)) for row in basis['integral_basis_power_coordinates']]
    for original, centered in zip(integral[1:], eta):
        difference = [17*(a-b) for a, b in zip(original, centered)]
        assert all(x == 0 for x in difference[1:]) and difference[0].denominator == 1
    return {'exact_quadric_values_in_degree17_algebra_checked': 91,
            'rational_scalar_coordinates_checked': 91*17,
            'maximum_quadric_L1': max(norms),
            'maximum_17eta_root_bound': str(max(bounds)),
            '17eta_integrality_reduces_to_inherited_integral_basis': True,
            'root_bound_4_and_integral_basis_are_inherited_D103_inputs': True}


def calculate():
    cm = cm_frame_checks()
    old = read('cm_arithmetic_height_budget_d118')['budgets']
    hodge = Q(read('cm_intrinsic_height_review_d104')['independent_analytic']['Hodge_height_interval'][1])
    assert hodge == Q(old['saved_Hodge_height_upper'])
    theta = Q(55817, 54150)
    assert theta == Q(old['tropical_Faltings_coefficient_log2'])
    assert Q(76, 8)-Q(67889, 27075)/2 == Q(223268, 27075)
    assert Q(223268, 27075)/8 == theta
    assert Q(280+16*17, 272) == Q(69, 34)
    # Zhao's squared-line degree is log(D)/g; halving gives log(D)/(2g).
    # Combined with nearby-pair and averaged Colmez identities:
    assert -Q(17, 16)+Q(1+17, 16) == Q(1, 16)
    pi = plus(scale(atan(Q(1, 5)), 16), scale(atan(Q(1, 239)), -4))
    logpi = log(pi[0])[0], log(pi[1])[1]
    log53 = log(Q(5, 3))
    H = plus((2*hodge, 2*hodge), scale(LOG2, -Q(35, 34)))
    Fminus = plus(scale(logpi, -16), scale(LOG2, theta-8))
    constants = [scale(root(2), 2), plus(scale(root(3), 2), (Q(2),)*2),
                 plus((Q(4),)*2, scale(root(6), 2))]
    results = []
    for n, C in enumerate(constants, 1):
        logC = log(C[0])[0], log(C[1])[1]
        F = plus(scale(H, 240+n), scale(LOG2, 190-15*theta), scale(logpi, 120),
                 log(480*cm['maximum_quadric_L1']), logC, scale(log53, 240+n))
        overlap(F, tuple(map(Q, old['thresholds'][n-1]['upper_bound_expression_interval'])))

        def zero(P):
            E = 2*P+32
            N = E-296+2*3920-4200-(n+2)*33
            A = E-296+2*3920-4200-(n+2)*296
            assert N == 2*P+3310-33*n and A == 2*P+2784-296*n
            assert Q(16*N+A, 272) == Q(P, 8)+Q(55744-824*n, 272)
            return scale(LOG2, Q(16*N+A, 272))

        def threshold(bound):
            first = next(P for P in range(8, 20001, 8) if zero(P)[0] > bound[1])
            assert zero(first-8)[1] < bound[0]
            return first

        samples = []
        for P in (1600, 3200, 6400, 10472, 10480, 10552):
            margin = plus(zero(P), scale(F, -1))
            samples.append({'P': P, 'strict_margin_interval': encode(margin),
                            'display_approximation_only': float(sum(margin)/2),
                            'inequality_certified': margin[0] > 0})
        minimum = threshold(F)
        short = threshold(plus(F, log(Q(29299, 42550))))
        # Diagnostic removal of favourable terms tests dependence on the
        # two most consequential inherited height inputs, not alternative proofs.
        no_content = threshold(plus(F, scale(LOG2, Q(69, 34)*(240+n))))
        no_tropical = threshold(plus(F, scale(LOG2, 15*theta)))
        results.append({'order': n, 'finite_zero_upper_interval': encode(F),
                        'minimum_P_multiple_of_8': minimum,
                        'shorter_basis_minimum_P_multiple_of_8': short,
                        'without_finite_fibre_content_minimum_P': no_content,
                        'without_tropical_Faltings_gain_minimum_P': no_tropical,
                        'samples': samples})
    assert [x['minimum_P_multiple_of_8'] for x in results] == [10416, 10480, 10552]
    assert [x['shorter_basis_minimum_P_multiple_of_8'] for x in results] == [10408, 10480, 10544]
    return {'status': 'pass', 'milestone': 'D155', 'exact_CM_frame_checks': cm,
            'interval_method': '192-bit outward rational intervals; 96-term atanh logs with explicit tail; Machin pi; integer square roots',
            'Hodge_height_upper': str(hodge), 'CM_fibre_height_upper_interval': encode(H),
            'Faltings_height_lower_interval': encode(Fminus), 'log2_interval': encode(LOG2),
            'pi_interval': encode(pi), 'tropical_coefficient': str(theta),
            'thresholds': results, 'conditional_two_order_target': 10480,
            'height_source_normalization_requires_companion_proof': True,
            'bounds_are_sufficient_not_necessary': True,
            'actual_harmonic_precision_increased': False,
            'exact_positive_vanishing_proved': False, 'new_precision_bank_admitted': False}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    start = time.monotonic()
    result = calculate()
    result['wall_seconds'] = time.monotonic()-start
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    result['sources'] = [source(p) for p in sorted(PATHS)]
    with OUT.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print('D155_BOUNDS|'+json.dumps(result['thresholds']), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(OUT)), flush=True)
    print('PASS|642_PROOF_CRITERION_BOUNDS', flush=True)
