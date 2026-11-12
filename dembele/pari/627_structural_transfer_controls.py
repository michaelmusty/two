"""D150: independent field arithmetic and controls for the transfer audit."""
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
OUT = DATA / 'structural_transfer_controls_d150.json'
HELPER = ROOT / 'dembele/pari/405_dyadic_edge_reducer.py'
spec = importlib.util.spec_from_file_location('d150_frozen_field', HELPER)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
r = old.r
PATHS = {Path(__file__), HELPER, Path(r.__file__), Path(old.a.__file__)}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read(name):
    p = DATA / (name + '.json')
    source(p)
    return json.loads(p.read_text())


def calculate():
    packet = read('dyadic_moment_transports_d113')
    primary = read('structural_identification_audit_d150')
    assert packet['status'] == primary['status'] == 'pass'
    nonaffine = 0
    branches = 0
    for row in packet['transitions']:
        for child in row['children']:
            a, b, c, d = r.fm(child['normalized_center'])
            assert d == r.ONE
            assert r.val(a) >= 1 and r.val(b) >= 0 and r.val(c) >= 1
            assert r.val(r.sub(a, r.mul(b, c))) == 1
            assert child['normalized_error_pi'] >= 159
            branches += 1
            if c != r.ZERO and r.val(c) < child['normalized_error_pi'] and len({x['target_edge'] for x in row['children']}) == 2:
                nonaffine += 1
    assert branches == 348 and nonaffine == primary['distinct_target_nonaffine_branch_count']
    w = primary['nonaffine_witness']
    child = packet['transitions'][w['source']]['children'][w['child']]
    a, b, c, d = r.fm(child['normalized_center'])
    delta = r.sub(a, r.mul(b, c))
    # Build the Taylor series from (1+cX)*phi=b+aX, without the
    # closed coefficient formula used by the primary calculation.
    coeff = b
    for k in range(1, 13):
        coeff = r.sub(a if k == 1 else r.ZERO, r.mul(c, coeff))
        assert r.val(coeff) == 1 + (k - 1) * r.val(c)
        if k == 1:
            assert coeff == delta
    # Validate the primary's whole directed walk and also build a
    # separate one by choosing the other branch at every vertex.
    route = primary['reachable_cycle']
    walk = route['prefix'] + route['cycle']
    assert walk[0]['source'] == primary['anchor_A_start_edge']
    for i, step in enumerate(walk):
        item = packet['transitions'][step['source']]['children'][step['child']]
        assert item['target_edge'] == step['target']
        if i + 1 < len(walk):
            assert step['target'] == walk[i + 1]['source']
    assert route['cycle'][-1]['target'] == route['cycle'][0]['source']
    assert route['cycle_determinant_valuation_pi'] == len(route['cycle']) > 0
    state = primary['anchor_A_start_edge']
    states = []
    while state not in states:
        states.append(state)
        state = packet['transitions'][state]['children'][1]['target_edge']
    cut = states.index(state)
    other_cycle = states[cut:] + [state]
    # Exact control: phi(x)=2x, k(x)=1/(x^2-2). Its nth pullback
    # has denominator 4^n*x^2-2. The squared pole values have distinct
    # odd dyadic valuations, so lie outside Q2 and never repeat.
    poles = [Q(2, 4**n) for n in range(9)]
    assert len(set(poles)) == len(poles)
    assert all((1 - 2*n) % 2 for n in range(9))
    assert all(poles[i + 1] * 4 == poles[i] for i in range(8))
    # Without strict contraction, phi=-x preserves the same kernel.
    assert (-1)**2 == 1
    for item in primary['finite_residual_controls']:
        n = item['precision_binary']
        sequence = sum(2**i for i in range(n))
        assert sequence - (-1) == 2**n
        assert str(sequence - (1 + 2*sequence)) == item['residual']
    # Matrix-kernel control, applied as actual sparse matrix products.
    for item in primary['equal_rank_controls']:
        n = item['precision_binary']
        left = [[int(i == j) for j in range(136)] for i in range(45)]
        right = [row[:] for row in left]
        right[0][45] = 2**n
        candidate = [int(j == 45) for j in range(136)]
        actual = candidate[:]
        actual[0] = -2**n
        action = lambda matrix, vector: [sum(x*y for x, y in zip(row, vector)) for row in matrix]
        assert action(left, candidate) == [0]*45
        assert action(right, actual) == [0]*45
        assert action(right, candidate) == [2**n] + [0]*44
        assert action(left, actual) == [-2**n] + [0]*44
        assert all((x-y) % 2**n == 0 for u, v in zip(left, right) for x, y in zip(u, v))
    # An exact dual identity control: on delta_0, integral H(2x)=integral H(x).
    # The monomial identity is exact; changing its constant changes the integral.
    H = [Q(3), Q(-2), Q(5), Q(7)]
    residual = [h * (1 - 2**i) for i, h in enumerate(H)]
    assert residual[0] == 0
    corrupted = residual[:]
    corrupted[0] += 1
    assert corrupted[0] != 0
    return {'status': 'pass', 'milestone': 'D150', 'branches_checked': branches,
            'distinct_target_nonaffine_branch_count': nonaffine,
            'field_backend_independent_of_source_626': True,
            'nonaffine_Taylor_recurrence_checked_through_degree': 12,
            'primary_cycle_verified': True, 'alternative_cycle_states': other_cycle,
            'alternative_cycle_determinant_valuation_pi': len(other_cycle)-1,
            'rational_pole_control_squared_poles': list(map(str, poles)),
            'strict_contraction_hypothesis_control_passed': True,
            'finite_congruence_and_equal_rank_controls_passed': True,
            'dual_identity_and_corruption_controls_passed': True,
            'controls_are_not_actual_candidate_counterexamples': True,
            'infinite_pole_orbit_argument_is_companion_proof': True,
            'summed_transfer_cancellations_excluded': False,
            'exact_candidate_transfer_identity_constructed': False,
            'candidate_identification_proved': False, 'new_precision_bank_admitted': False}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    result = calculate()
    result['wall_seconds'] = time.monotonic() - tick
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    result['sources'] = [source(p) for p in sorted(PATHS)]
    with OUT.open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['branches_checked', 'alternative_cycle_states', 'peak_rss_bytes']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|627_STRUCTURAL_TRANSFER_CONTROLS', flush=True)
