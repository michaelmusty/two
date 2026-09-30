"""D120: conditional sufficient precision and measured algorithm cost.

The higher-precision benchmarks use synthetic moments and compatible
synthetic maps. They are not a refinement of the certified P=200 bank.
"""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'


def module(name, file):
    s = importlib.util.spec_from_file_location(name, ROOT/'dembele/pari'/file)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


f = module('fast', '459_dyadic_mobius_transform.py')
r = module('smith', '457_cm_cartier_frame_review.py')
b = module('logs', '447_cm_disk_vanishing_budget.py')


def design():
    bank = json.loads((DATA/'dyadic_precision200_d115.json').read_text())
    # Prove the inverse-matrix norm used in the future precision propagation.
    q = r.r.FieldQuotient(64)
    matrix = [[q.norm(r.divide_beta(x, 33, bank['coarse_error_beta'][0]))
               for x in point['coarse_coefficients_beta'][0]] for point in bank['CM_values'][1:]]
    factors = r.smith(matrix)
    assert factors == [0]*8+[35]*8
    comparison = json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    assert [x['beta_exponent'] for x in comparison['frame_relation']] == [-35]*16
    prior = json.loads((DATA/'cm_arithmetic_height_budget_d118.json').read_text())['budgets']
    rows = []
    for old in prior['thresholds']:
        n = old['order']
        total = tuple(map(Q, old['upper_bound_expression_interval']))
        constant = 55744-824*n
        lo = 8*total[0]/b.LOG2[1]-Q(constant, 34)
        hi = 8*total[1]/b.LOG2[0]-Q(constant, 34)
        minimum = hi.__floor__()+1
        assert minimum-1 < lo < hi < minimum
        P = 8*((minimum+7)//8)
        N, A = 2*P+3310-33*n, 2*P+2784-296*n
        assert b.scale(b.LOG2, Q(16*N+A, 272))[0] > total[1]
        rows.append({'order': n, 'strict_working_precision_pi_interval': list(map(str, (lo, hi))),
                     'minimum_integer_P_for_this_propagation_bound': minimum,
                     'sufficient_P_rounded_to_multiple_of_eight': P,
                     'conditional_nonanchor_integral_jet_beta': N,
                     'conditional_anchor_integral_jet_beta': A})
    P = max(row['sufficient_P_rounded_to_multiple_of_eight'] for row in rows)
    bits = P//8
    coefficient_bytes = (bits+7)//8
    # Raw packed payload only: Python containers, buffers, charts and files
    # are additional. Streaming one harmonic column is a design requirement.
    payload = 174*P*8*coefficient_bytes
    dense = 165*(3*P-1)*P*8*coefficient_bytes
    return {'nonanchor_evaluation_Smith_beta': factors,
        'nonanchor_inverse_entry_lower_beta': -35,
        'frame_relation_entry_beta': -35,
        'raw_four_jet_error_beta_assumption': 'E=2*P+32',
        'normalized_leading_nonanchor_error_beta': 'E-33',
        'normalized_leading_anchor_error_beta': 'E-296',
        'inverse_matrix_error_beta': 'E-103',
        'frame_relation_error_beta': 'E-331',
        'reciprocal_frame_relation_error_beta': 'E-261',
        'frame_change_error_beta': 'E-296',
        'frame_change_entry_lower_beta': 0,
        'quadric_coarse_error_beta': 'E-296',
        'conditional_nonanchor_intrinsic_jet_lower_beta': '2*P+3310-33*n',
        'conditional_anchor_intrinsic_jet_lower_beta': '2*P+2784-296*n',
        'additional_required_eta_error_beta_at_least': 'E',
        'additional_required_beta_ring_precision_at_least': '2*P+64',
        'additional_required_all_transport_errors_pi_at_least': 'P',
        'rows': rows, 'sufficient_common_P_under_stated_hypotheses': P,
        'coefficient_modulus_bits': bits,
        'one_harmonic_column_low_moment_packed_payload_bytes': payload,
        'sixteen_harmonic_columns_low_moment_packed_payload_bytes': 16*payload,
        'old_dense_child_operator_packed_payload_bytes': dense,
        'essential_hypotheses': [
            'Refine transports, CM roots and eta values to the stated precision on the certified branches.',
            'Solve and independently verify all moments and all four coarse coefficients.',
            'Future quadric enclosures must contain zero through their proved errors.',
            'Establish successive exact vanishing in order before interpreting higher jets intrinsically.'],
        'precision_bound_is_conditional_not_a_prediction_of_candidate_equality': True}


def benchmarks():
    rows = []
    previous = None
    for P in (200, 400, 800, 1600):
        ring = f.Ring(P//8)
        pi = (0, 1, 0, 0, 0, 0, 0, 0)
        unit = tuple((ring.mod-7-19*j) % ring.mod for j in range(8))
        bb = tuple((ring.mod-3-11*j) % ring.mod for j in range(8))
        cc = ring.mul(pi, unit)
        aa = ring.add(pi, ring.mul(bb, cc))
        moments = [tuple((ring.mod-1-17*i-31*j) % ring.mod for j in range(8)) for i in range(P)]
        start = time.monotonic()
        result = ring.transform(moments, aa, bb, cc, P)
        elapsed = time.monotonic()-start
        if previous:
            oldP, old = previous
            modulus = 1 << (oldP//8)
            assert [tuple(c % modulus for c in row) for row in result[:oldP]] == old
        previous = P, result
        row = {'synthetic_P': P, 'coefficient_modulus_bits': P//8,
               'single_action_wall_seconds': elapsed,
               'maximum_packed_product_bytes': ring.maximum_packed_bytes,
               'polynomial_products': ring.product_count}
        rows.append(row)
        print('MOBIUS_COST|'+json.dumps(row), flush=True)
    return rows


def build():
    result = {'status': 'pass', 'milestone': 'D120', 'precision_design': design(),
              'synthetic_benchmarks': benchmarks()}
    last = result['synthetic_benchmarks'][-1]
    # This is the measured cost of repeating the last synthetic action,
    # not a timing forecast or lower bound for the proposed actual run.
    result['illustrative_seconds_for_348_times_16_last_synthetic_actions'] = 348*16*last['single_action_wall_seconds']
    result.update({
        'decision': 'Keep the D118 section certificate; develop preconditioned or compressed iteration before any large precision run.',
        'memory_bottleneck_addressed_by_prototype': 'No quadratic-size child or chart operator table.',
        'remaining_cost_bottleneck': '174 states, 16 columns and many precision-gain iterations; the prototype alone is insufficient.',
        'large_precision_run_ready': False,
        'actual_moment_precision_increased': False,
        'candidate_identification_proved': False,
        'sources': [f.source(p) for p in [Path(__file__), Path(f.__file__), Path(r.__file__), Path(b.__file__),
            DATA/'dyadic_precision200_d115.json', DATA/'dyadic_comparison200_d115.json',
            DATA/'cm_arithmetic_height_budget_d118.json', DATA/'dyadic_mobius_transform_d120.json']]})
    print('PRECISION_DESIGN|'+json.dumps(result['precision_design']['rows']), flush=True)
    return result


if __name__ == '__main__':
    out = DATA/'dyadic_precision_design_d120.json'
    assert not out.exists()
    out.write_text(json.dumps(build(), indent=2)+'\n')
    print('PASS|461_DYADIC_PRECISION_DESIGN', flush=True)
