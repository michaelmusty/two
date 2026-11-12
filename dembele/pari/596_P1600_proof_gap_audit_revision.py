"""D141 independent audit revision: enforce rational LDL pivots.

Recompute early Gram minors by rational LDL, independent of the previous
fraction-free determinant calculation. Use a different logarithm series
and the uncollected height expression for all Faltings targets.
"""
from fractions import Fraction as Q
import hashlib
import importlib.util
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PATHS = {Path(__file__)}
spec = importlib.util.spec_from_file_location('d141_independent_logs', ROOT/'dembele/pari/450_cm_disk_exactness_review.py')
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
    path = DATA/(stem+'.json')
    PATHS.add(path)
    value = json.loads(path.read_text())
    assert value['status'] == 'pass'
    return value


def iv(x):
    return tuple(map(Q, x))


def agree(a, b):
    assert max(a[0], b[0]) <= min(a[1], b[1]), (a, b)


def fast_log(x):
    x = Q(x)
    k = x.numerator.bit_length()-x.denominator.bit_length()
    x /= Q(2)**k
    if x < 1:
        x *= 2
        k -= 1
    u = 1 << 112
    lower, upper = Q((x*u).__floor__(), u), Q((x*u).__ceil__(), u)
    return logs.plus((logs.log(lower)[0], logs.log(upper)[1]), logs.scale(logs.L2, k))


def gram_minors(rows):
    n = len(rows)
    gram = [[sum(a*b for a, b in zip(x, y)) for y in rows] for x in rows]
    lower = [[Q(0)]*n for _ in range(n)]
    diagonal, minors, running = [], [], Q(1)
    for i in range(n):
        lower[i][i] = Q(1)
        for j in range(i):
            lower[i][j] = (Q(gram[i][j]) - sum(lower[i][k]*lower[j][k]*diagonal[k] for k in range(j)))/diagonal[j]
        d = Q(gram[i][i]) - sum(lower[i][k]**2*diagonal[k] for k in range(i))
        assert d > 0
        diagonal.append(d)
        running *= d
        assert running.denominator == 1
        minors.append(int(running))
    return minors


def controls():
    assert gram_minors([[2, 0], [1, 3]]) == [4, 36]
    lengths = [1, 4, 100, 400]
    pairs = list(combinations(range(4), 2))
    nonzero = outside = 0
    for entries in product((-1, 0, 1), repeat=8):
        a, b = entries[:4], entries[4:]
        wedge = [a[i]*b[j]-a[j]*b[i] for i, j in pairs]
        if not any(wedge):
            continue
        nonzero += 1
        norm = sum(c*c*lengths[i]*lengths[j] for c, (i, j) in zip(wedge, pairs))
        if any(wedge[1:]):
            outside += 1
            assert norm >= 100
    assert 1*4 < 100 and 1*100 == 100
    # The boundary has equality and is not admitted by the strict criterion.
    assert not 100 < 100 and nonzero > outside > 0
    return {'coefficient_matrices_enumerated': 3**8, 'nonzero_wedges': nonzero,
            'outside_wedges_checked': outside, 'strict_boundary_rejected': True}


def exterior_review(packet):
    summaries = []
    for saved in packet['exterior_lattice_certificates']:
        bits = saved['training_2_bits']
        old = read(f'dyadic_P1600_relation_height{bits}_d140')
        rec = read(f'dyadic_P1600_lattice{bits}_r3_d140')
        worker = read(f'dyadic_P1600_lattice{bits}_r3_d140_worker')
        minors = [int(x, 16) for x in old['leading_Gram_determinants_hex']]
        recomputed = gram_minors(rec['recognized_integer_vectors'])
        assert recomputed == minors[:91] and rec['recognized_integer_vectors'] == worker['reduced_basis'][:91]
        native = read(f'dyadic_P1600_recognition_certificates{bits}_d140')['certificates']
        assert native['independent_Gram_leading_minor_sizes_checked'] == list(range(91, 137))
        D = [1]+minors
        d = [Q(D[i+1], D[i]) for i in range(136)]
        inside, outside = sorted(d[:91]), sorted(d[91:])
        prefix_in, prefix_out = [Q(1)], [Q(1)]
        for x in inside:
            prefix_in.append(prefix_in[-1]*x)
        for x in outside:
            prefix_out.append(prefix_out[-1]*x)
        # Enumerate every possible number of outside indices, not one swap.
        possibilities = [prefix_in[91-k]*prefix_out[k] for k in range(1, 46)]
        bound = min(possibilities)
        assert bound == Q(saved['minimum_outside_exterior_squared_norm'])
        assert possibilities.index(bound) == 0
        actual = Q(1)
        selected = saved['minimizing_exterior_indices_one_based']
        assert len(set(selected)) == len(selected) == 91
        for i in selected:
            actual *= d[i-1]
        assert actual == bound
        H = saved['sufficient_inclusive_max_Pluecker_height']
        count = comb(136, 91)
        assert saved['primitive_Pluecker_coordinate_count'] == count
        assert count*H*H < bound <= count*(H+1)*(H+1)
        assert Q(saved['candidate_squared_covolume']) == minors[90] < bound
        upper = saved['candidate_covolume_integer_upper']
        assert (upper-1)**2 <= minors[90] < upper**2
        assert saved['candidate_covolume_upper_within_max_Pluecker_threshold'] == (upper <= H) == (bits == 160)
        agree(logs.scale(fast_log(minors[90]), Q(1, 2)), iv(saved['candidate_log_covolume_interval']))
        agree(logs.scale(fast_log(bound), Q(1, 2)), iv(saved['sufficient_strict_log_covolume_interval']))
        agree(logs.scale(fast_log(bound/minors[90]), Q(1, 2)), iv(saved['log_covolume_separation_interval']))
        assert saved['true_ideal_height_bound_proved'] is False
        summaries.append({'training_2_bits': bits, 'independently_replayed_Gram_minors': list(range(1, 92)),
                          'outside_count_cases_checked': 45, 'h_exterior_at_most_623_suffices': bits == 160})
    assert Q(packet['exterior_lattice_certificates'][1]['sufficient_strict_log_covolume_interval'][0]) > 623
    return summaries


def height_review(packet):
    saved = packet['section_budget_diagnostics']
    old = read('cm_arithmetic_height_budget_d118')['budgets']
    actual = read('dyadic_integral_quadrics1600_d138')['comparison_with_sufficient_bounds']
    previous = read('cm_inverse_frame_budget_d120')
    hL, theta = Q(old['saved_Hodge_height_upper']), Q(old['tropical_Faltings_coefficient_log2'])
    H = logs.plus((2*hL, 2*hL), logs.scale(logs.L2, -Q(35, 34)))
    pi = logs.rounded(logs.plus(logs.scale(logs.atan(Q(1, 5)), 16), logs.scale(logs.atan(Q(1, 239)), -4)))
    logpi = (logs.log(pi[0])[0], logs.log(pi[1])[1])
    log_radius = logs.log(Q(5, 3))
    low = logs.plus(logs.scale(logpi, -16), logs.scale(logs.L2, theta-8))
    logB = logs.plus(logs.scale(logpi, -Q(1, 2)), log_radius)
    upper = logs.plus(logs.scale(H, 16), logs.scale(logB, 16), logs.scale(logs.L2, -Q(525, 34)))
    agree(low, iv(saved['Faltings_current_lower_interval']))
    agree(upper, iv(saved['Faltings_existing_upper_interval']))
    Cs = [logs.scale(logs.sqrt(2), 2), logs.plus(logs.scale(logs.sqrt(3), 2), (Q(2),)*2),
          logs.plus(logs.scale(logs.sqrt(6), 2), (Q(4),)*2)]
    best = min(saved['recognized_basis_max_coefficient_l1'].values())
    for bits in (96, 160):
        rec = read(f'dyadic_P1600_lattice{bits}_r3_d140')
        assert saved['recognized_basis_max_coefficient_l1'][str(bits)] == max(sum(abs(x) for x in v) for v in rec['recognized_integer_vectors'])
    for n, (row, current, C) in enumerate(zip(saved['rows'], actual, Cs), 1):
        assert row['order'] == current['order'] == n
        N, A = current['degree16_achieved_lower_beta'], current['anchor_achieved_lower_beta']
        assert [N, A] == [row['nonanchor_lower_beta'], row['anchor_lower_beta']]
        Z = logs.scale(logs.L2, Q(16*N+A, 272))
        logC = (logs.log(C[0])[0], logs.log(C[1])[1])
        # All terms except -15 F, before the old Faltings bound is substituted.
        base = logs.plus(logs.scale(H, 240+n), logs.scale(logs.L2, 70),
                         logs.scale(logpi, -120), logs.log(480*42550), logC,
                         logs.scale(log_radius, 240+n))
        critical = logs.scale(logs.plus(base, logs.scale(Z, -1)), Q(1, 15))
        agree(critical, iv(row['Faltings_strict_critical_value_interval']))
        assert critical[1] < upper[0] and critical[0] > low[1]
        assert row['Faltings_sufficient_integer_lower_bound'] == critical[1].__floor__()+1
        assert iv(previous['rows'][n-1]['Faltings_only_rescue_required_strict_lower_interval'])[0] > upper[1]
        for cost, radius, key in [(1, True, 'unit_coefficient_cost_optimistic_sufficient_beta'),
                                 (1, False, 'unit_cost_and_radius_one_optimistic_sufficient_beta'),
                                 (best, True, 'recognized_basis_uniform_sufficient_beta')]:
            expression = logs.plus(base, logs.scale(low, -15), logs.log(Q(cost, 42550)))
            if not radius:
                expression = logs.plus(expression, logs.scale(log_radius, -(240+n)))
            lo = 17*expression[0]/logs.L2[1]-Q(A, 16)
            hi = 17*expression[1]/logs.L2[0]-Q(A, 16)
            assert row[key]-1 < lo < hi < row[key] and row[key] > N
        assert critical[1] < low[0]+52
        assert row['higher_order_integrality_requires_previous_exact_zeros'] == (n > 1)
    assert max(r['Faltings_sufficient_integer_lower_bound'] for r in saved['rows']) == 29
    assert saved['Faltings_lower_29_proved'] is False and saved['either_hypothesis_proved'] is False
    return {'independent_logarithm_series': 'sum (1-1/x)^k/k with rational tail',
            'uncollected_Faltings_expression_checked': True, 'historical_D120_exclusion_preserved': True,
            'new_integer_targets': [28, 28, 29], 'no_geometric_height_hypothesis_established': True}


if __name__ == '__main__':
    tick = time.monotonic()
    output = DATA/'P1600_proof_gap_audit_r2_d141.json'
    assert not output.exists()
    packet = read('P1600_proof_gap_diagnostics_r2_d141')
    for ref in packet['sources']:
        assert source(ref['path']) == ref
        PATHS.add(Path(ref['path']))
    result = {'status': 'pass', 'milestone': 'D141', 'controls': controls(),
              'exterior_review': exterior_review(packet), 'height_review': height_review(packet),
              'candidate_identification_proved': False, 'true_ideal_height_bound_proved': False,
              'Faltings_lower_29_proved': False, 'actual_harmonic_precision_increased': False,
              'wall_seconds': time.monotonic()-tick,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
              'sources': [source(p) for p in sorted(PATHS)]}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D141_INDEPENDENT_AUDIT_PASS|' + json.dumps({'seconds': result['wall_seconds'], 'controls': result['controls']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(output)), flush=True)
    print('PASS|596_P1600_PROOF_GAP_AUDIT_REVISION', flush=True)
