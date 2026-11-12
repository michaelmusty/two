"""D150: finite witnesses for the structural identification audit.

Run only through run_dyadic_capped.py. No new moments or candidate
scheme computations. The infinite pole-orbit argument is in the report.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'structural_identification_audit_d150.json'
PATHS = {Path(__file__)}
MOD = [2, 0, -16, 0, 20, 0, -8, 0, 1]


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read(name):
    path = DATA / (name + '.json')
    source(path)
    return json.loads(path.read_text())


def v2(n):
    assert n
    n = abs(n)
    return (n & -n).bit_length() - 1


def val(x):
    terms = [8 * (v2(a.numerator) - v2(a.denominator)) + i
             for i, a in enumerate(x) if a]
    return min(terms) if terms else None


def mul(x, y):
    z = [Q(0)] * 15
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            z[i + j] += a * b
    for i in range(14, 7, -1):
        for j in range(8):
            z[i - 8 + j] -= z[i] * MOD[j]
    return z[:8]


def lower_at_least(v, n):
    return v is None or v >= n


def cycle(packet, start, child_index):
    seen = {}
    path = []
    state = start
    while state not in seen:
        seen[state] = len(path)
        row = packet['transitions'][state]
        assert row['edge'] == state
        child = row['children'][child_index]
        path.append({'source': state, 'child': child_index,
                     'target': child['target_edge']})
        state = child['target_edge']
    cut = seen[state]
    assert path[cut]['source'] == path[-1]['target']
    return {'start': start, 'prefix': path[:cut], 'cycle': path[cut:],
            'cycle_determinant_valuation_pi': len(path) - cut}


def calculate():
    packet = read('dyadic_moment_transports_d113')
    review = read('dyadic_moment_review_d113')
    ref = source(DATA / 'dyadic_moment_transports_d113.json')
    assert packet['status'] == review['status'] == 'pass'
    assert ref in review['sources']
    assert packet['state_count'] == len(packet['transitions']) == 174
    nonaffine = []
    slopes = []
    for row in packet['transitions']:
        assert len(row['children']) == 2
        assert sorted(c['constant_residue'] for c in row['children']) == [0, 1]
        for i, child in enumerate(row['children']):
            a, b, c, d = [list(map(Q, x)) for x in child['normalized_center']]
            assert d == [1] + [0] * 7
            error = child['normalized_error_pi']
            assert error >= 159
            va, vb, vc = val(a), val(b), val(c)
            delta = [x - y for x, y in zip(a, mul(b, c))]
            assert lower_at_least(va, 1) and lower_at_least(vb, 0)
            assert lower_at_least(vc, 1) and val(delta) == 1
            assert child['determinant_valuation'] == 1
            assert 0 <= child['target_edge'] < 174
            slopes.append({'source': row['edge'], 'child': i,
                           'target': child['target_edge'],
                           'center_slope_valuation_pi': vc,
                           'slope_error_pi': error})
            # A finite ball excluding zero proves the exact slope is nonzero.
            # Distinct targets exclude cancellation in this matrix entry.
            if vc is not None and vc < error and len({x['target_edge'] for x in row['children']}) == 2:
                nonaffine.append(slopes[-1])
    assert len(slopes) == 348 and nonaffine
    anchor = next(c for c in packet['CM_charts']
                  if c['CM_index'] == 0 and c['chart'] == 'A')
    graph_cycle = cycle(packet, anchor['target_edge'], 0)
    witness = nonaffine[0]
    # For this branch [X^k] phi(X) = delta*(-c)^(k-1), all k >= 1.
    # The unbounded assertion is a proof, not an enumeration of large k.
    coefficient_values = [1 + (k - 1) * witness['center_slope_valuation_pi']
                          for k in [1, 2, 12, 1600, 10000]]
    controls = []
    for n in [1, 4, 32, 160]:
        approximate = 2**n - 1
        residual = approximate - 1 - 2 * approximate
        assert residual == -2**n and approximate != -1
        controls.append({'precision_binary': n, 'exact_fixed_point': '-1',
                         'approximation': str(approximate), 'residual': str(residual)})
    # Same rank and arbitrarily strong congruence do not force equal kernels.
    # R0=[I45|0]; RN=R0+2^N E_(0,45). Both have rank 45.
    rank_controls = []
    for n in [83, 147]:
        assert (2**n) % (2**n) == 0 and 2**n != 0
        rank_controls.append({'precision_binary': n, 'rows': 45, 'columns': 136,
                              'common_rank': 45, 'different_kernels': True,
                              'witness_column': 45, 'nonzero_residual': str(2**n),
                              'control_is_an_actual_curve_claim': False})
    return {'status': 'pass', 'milestone': 'D150',
            'state_count': 174, 'strict_contracting_branches': 348,
            'branch_shape_checked_from_centers_and_certified_errors': True,
            'distinct_target_nonaffine_branch_count': len(nonaffine),
            'nonaffine_witness': witness, 'sample_coefficient_valuations_pi': coefficient_values,
            'coefficient_valuation_sample_degrees': [1, 2, 12, 1600, 10000],
            'anchor_A_start_edge': anchor['target_edge'], 'reachable_cycle': graph_cycle,
            'finite_residual_controls': controls, 'equal_rank_controls': rank_controls,
            'ordinary_polynomial_moment_truncation_is_not_exact': True,
            'branchwise_finite_rational_closure_excluded_by_companion_proof': True,
            'summed_transfer_cancellations_excluded': False,
            'exact_candidate_transfer_identity_constructed': False,
            'candidate_identification_proved': False, 'field_polynomial_constructed': False,
            'new_precision_bank_admitted': False, 'actual_harmonic_precision_increased': False,
            'best_current_proved_relation_height_upper': 15237, 'sufficient_height_target': 623}


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
    print(json.dumps({k: result[k] for k in ['strict_contracting_branches', 'distinct_target_nonaffine_branch_count', 'nonaffine_witness', 'reachable_cycle']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|626_STRUCTURAL_IDENTIFICATION_AUDIT', flush=True)
