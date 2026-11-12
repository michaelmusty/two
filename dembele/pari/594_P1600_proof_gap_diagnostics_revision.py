"""D141 revision: distinguish the covolume and max-Pluecker sufficient tests.

Derive a basis-independent exterior-lattice exclusion, and recompute the
Faltings-only exactness target with the completed P1600 lower bounds.
No unknown geometric height is assumed or inferred from candidate data.
"""
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb, isqrt
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PATHS = {Path(__file__)}
spec = importlib.util.spec_from_file_location('d141_logs', ROOT / 'dembele/pari/447_cm_disk_vanishing_budget.py')
logs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logs)
PATHS.add(Path(logs.__file__))


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    value = json.loads(path.read_text())
    assert value['status'] == 'pass'
    return value


def interval(value):
    return tuple(map(Q, value))


def encoded(value):
    return list(map(str, value))


def log_interval(value):
    # Round only the mantissa outwards before evaluating the rational series.
    # This avoids raising enormous Gram-determinant denominators to high powers.
    value = Q(value)
    assert value > 0
    k = value.numerator.bit_length() - value.denominator.bit_length()
    mantissa = value / (Q(2)**k)
    if mantissa < 1:
        mantissa *= 2
        k -= 1
    assert 1 <= mantissa < 2
    unit = 1 << 128
    lo = Q((mantissa*unit).__floor__(), unit)
    hi = Q((mantissa*unit).__ceil__(), unit)
    return logs.plus((logs.log(lo)[0], logs.log(hi)[1]), logs.scale(logs.LOG2, k))


def strict_sqrt(value):
    value = Q(value)
    h = isqrt(value.numerator // value.denominator)
    if h*h == value:
        h -= 1
    assert h*h < value <= (h+1)*(h+1)
    return h


def exterior(bits):
    saved = read(f'dyadic_P1600_relation_height{bits}_d140')
    determinants = [Q(1)] + [Q(int(s, 16)) for s in saved['leading_Gram_determinants_hex']]
    lengths = [determinants[i+1]/determinants[i] for i in range(136)]
    largest_inside = max(range(91), key=lambda i: lengths[i])
    smallest_outside = min(range(91, 136), key=lambda i: lengths[i])
    assert max(lengths[:91]) < min(lengths[91:])
    index_set = [i for i in range(91) if i != largest_inside] + [smallest_outside]
    lower = determinants[91] * lengths[smallest_outside] / lengths[largest_inside]
    direct = Q(1)
    for i in index_set:
        direct *= lengths[i]
    assert direct == lower
    coordinate_count = comb(136, 91)
    threshold = strict_sqrt(lower/coordinate_count)
    candidate_covolume_upper = isqrt(int(determinants[91])) + 1
    assert candidate_covolume_upper**2 > determinants[91]
    # The max-coordinate sufficient test loses a binomial factor.
    # It need not include the candidate at 96 digits; the covolume test does.
    assert determinants[91] < lower
    if bits == 160:
        assert candidate_covolume_upper <= threshold
    return {'training_2_bits': bits, 'ambient_dimension': 136, 'relation_dimension': 91,
            'all_outside_GS_lengths_exceed_all_inside': True,
            'minimizing_exterior_indices_one_based': [i+1 for i in index_set],
            'minimum_outside_exterior_squared_norm': str(lower),
            'primitive_Pluecker_coordinate_count': coordinate_count,
            'sufficient_inclusive_max_Pluecker_height': threshold,
            'candidate_squared_covolume': str(determinants[91]),
            'candidate_covolume_integer_upper': candidate_covolume_upper,
            'candidate_covolume_upper_within_max_Pluecker_threshold': candidate_covolume_upper <= threshold,
            'candidate_log_covolume_interval': encoded(logs.scale(log_interval(determinants[91]), Q(1, 2))),
            'sufficient_strict_log_covolume_interval': encoded(logs.scale(log_interval(lower), Q(1, 2))),
            'log_covolume_separation_interval': encoded(logs.scale(log_interval(lower/determinants[91]), Q(1, 2))),
            'true_ideal_height_bound_proved': False}


def sufficient_beta(bound, anchor):
    lo = 17*bound[0]/logs.LOG2[1] - Q(anchor, 16)
    hi = 17*bound[1]/logs.LOG2[0] - Q(anchor, 16)
    target = hi.__floor__() + 1
    assert target-1 < lo <= hi < target
    return target


def budgets():
    old = read('cm_arithmetic_height_budget_d118')['budgets']
    previous = read('cm_inverse_frame_budget_d120')
    current = read('dyadic_integral_quadrics1600_d138')['comparison_with_sufficient_bounds']
    lower = interval(old['Faltings_lower_bound_interval'])
    upper = interval(previous['Faltings_upper_from_existing_minors_interval'])
    L = old['maximum_quadric_coefficient_l1_norm']
    assert L == 42550
    lll_heights = {}
    for bits in (96, 160):
        recognized = read(f'dyadic_P1600_lattice{bits}_r3_d140')
        lll_heights[str(bits)] = max(sum(abs(x) for x in row) for row in recognized['recognized_integer_vectors'])
    best = min(lll_heights.values())
    rows = []
    for old_row, observed in zip(old['thresholds'], current):
        n = old_row['order']
        assert observed['order'] == n
        F = interval(old_row['upper_bound_expression_interval'])
        N, A = observed['degree16_achieved_lower_beta'], observed['anchor_achieved_lower_beta']
        zero = logs.scale(logs.LOG2, Q(16*N+A, 272))
        required = logs.plus(lower, logs.scale(logs.plus(F, logs.scale(zero, -1)), Q(1, 15)))
        integer_target = required[1].__floor__()+1
        assert integer_target-1 < required[0] < required[1] < integer_target
        assert required[1] < upper[0]
        assert sufficient_beta(F, A) == observed['sufficient_nonanchor_beta_with_new_anchor']
        cheap = logs.plus(F, logs.scale(log_interval(L), -1))
        disk_removed = logs.plus(cheap, logs.scale(interval(old_row['upper_bound_pieces']['disk_radius']), -1))
        recognized = logs.plus(F, log_interval(Q(best, L)))
        bounds = [sufficient_beta(v, A) for v in (cheap, disk_removed, recognized)]
        assert all(v > N for v in bounds)
        # Quantify the unproved terms needed in de Jong--Shokrieh (1.11).
        extra = logs.plus(required, logs.scale(lower, -1))
        rows.append({'order': n, 'nonanchor_lower_beta': N, 'anchor_lower_beta': A,
                     'measured_zero_degree_interval': encoded(zero),
                     'Faltings_strict_critical_value_interval': encoded(required),
                     'Faltings_sufficient_integer_lower_bound': integer_target,
                     'Faltings_only_route_no_longer_numerically_excluded': True,
                     'missing_nonnegative_height_terms_sufficient_total_interval': encoded(extra),
                     'unit_coefficient_cost_optimistic_sufficient_beta': bounds[0],
                     'unit_cost_and_radius_one_optimistic_sufficient_beta': bounds[1],
                     'recognized_basis_uniform_sufficient_beta': bounds[2],
                     'existing_section_inequality_still_fails': True,
                     'higher_order_integrality_requires_previous_exact_zeros': n > 1})
    total_target = max(r['Faltings_sufficient_integer_lower_bound'] for r in rows)
    assert total_target == 29 and lower[1] < 0 < total_target < upper[0] < 31
    # Either of these is a sufficient additional hypothesis, not a new estimate.
    hypothesis_lower = logs.plus(lower, (Q(52), Q(52)))
    assert all(hypothesis_lower[0] > interval(r['Faltings_strict_critical_value_interval'])[1] for r in rows)
    return {'Faltings_current_lower_interval': encoded(lower), 'Faltings_existing_upper_interval': encoded(upper),
            'old_max_coefficient_l1': L, 'recognized_basis_max_coefficient_l1': lll_heights,
            'best_recognized_max_coefficient_l1': best, 'rows': rows,
            'Faltings_29_would_suffice_for_all_three_orders': True,
            'theta_divisor_height_13_over_8_or_average_archimedean_I_26_would_suffice': True,
            'either_hypothesis_proved': False, 'Faltings_lower_29_proved': False,
            'D120_rejection_is_historical_for_its_P200_data': True}


if __name__ == '__main__':
    tick = time.monotonic()
    output = DATA / 'P1600_proof_gap_diagnostics_r2_d141.json'
    assert not output.exists()
    prior = read('dyadic_P1600_recognition_review_d140')
    assert prior['recognition_complete'] and prior['same_saturated_integer_lattice_as_candidate']
    assert strict_sqrt(Q(4)) == 1 and strict_sqrt(Q(9, 2)) == 2
    ext = [exterior(bits) for bits in (96, 160)]
    budget = budgets()
    result = {'status': 'pass', 'milestone': 'D141', 'inherited_review': source(DATA/'dyadic_P1600_recognition_review_d140.json'),
              'exterior_lattice_certificates': ext, 'section_budget_diagnostics': budget,
              'candidate_identification_proved': False, 'positive_exact_quadric_vanishing_proved': False,
              'true_ideal_height_bound_proved': False, 'field_polynomial_constructed': False,
              'actual_harmonic_precision_increased': False, 'next_precision_bank_admitted': False,
              'wall_seconds': time.monotonic()-tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
              'sources': [source(p) for p in sorted(PATHS)]}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D141_PROOF_TARGETS|' + json.dumps({'critical_Faltings': [float(Q(r['Faltings_strict_critical_value_interval'][1])) for r in budget['rows']],
          'max_coefficient_l1': budget['recognized_basis_max_coefficient_l1'],
          'log_covolume_thresholds': [float(Q(v['sufficient_strict_log_covolume_interval'][0])) for v in ext]}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(output)), flush=True)
    print('PASS|594_P1600_PROOF_GAP_DIAGNOSTICS_REVISION', flush=True)
