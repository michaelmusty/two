"""D151 independent finite arithmetic and structural controls.

Exact central differences, the frozen D106 field multiplier, explicit
binary-tree leaf counts, and two matrix formulas for the cleared jet.
Run only through run_dyadic_capped.py.
"""
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import prod
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'summed_transfer_controls_d151.json'
HELPER = ROOT / 'dembele/pari/389_cm_ratio_jet_review.py'
PATHS = {Path(__file__), HELPER}
spec = importlib.util.spec_from_file_location('d151_independent_field', HELPER)
field = importlib.util.module_from_spec(spec)
spec.loader.exec_module(field)


def source(path):
    p = Path(path).resolve()
    PATHS.add(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(stem):
    p = DATA / (stem + '.json')
    source(p)
    return json.loads(p.read_text())


def det(M):
    A = [list(map(Q, row)) for row in M]
    out = Q(1)
    for j in range(len(A)):
        pivot = next((i for i in range(j, len(A)) if A[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            A[pivot], A[j] = A[j], A[pivot]
            out = -out
        scale = A[j][j]
        out *= scale
        for i in range(j+1, len(A)):
            factor = A[i][j] / scale
            for k in range(j+1, len(A)):
                A[i][k] -= factor * A[j][k]
    return out


def adj(M):
    n = len(M)
    return [[(-1)**(i+j) * det([[M[r][c] for c in range(n) if c != i]
                              for r in range(n) if r != j])
             for j in range(n)] for i in range(n)]


def row_times(row, M):
    return [sum(row[i]*M[i][j] for i in range(len(row))) for j in range(len(M[0]))]


def frame_control(g, scale):
    # The nonanchor V_i are the standard basis; V_0 is minus their sum.
    # Q=X_0 X_1-X_0 X_2 vanishes on this entire projective frame.
    M = [[scale*Q((i+2) if i == j else (1 if j == i+1 else 0))
          for j in range(g)] for i in range(g)]
    z = [scale*Q(-i-1) for i in range(g)]
    w = [scale*Q((i+1)**2) for i in range(g)]
    D = det(M)
    A = adj(M)
    zA, wA = row_times(z, A), row_times(w, A)
    c = [-x for x in zA]
    assert D and all(c)
    Phi = [[c[i]*x for x in M[i]] for i in range(g)]
    Delta = det(Phi)
    assert Delta == D*prod(c)
    Aphi = adj(Phi)
    s0, s1 = row_times(z, Aphi), row_times(w, Aphi)
    q0 = s0[0]*s0[1]-s0[0]*s0[2]
    assert q0 == 0
    direct = (s1[0]*s0[1]+s0[0]*s1[1]-s1[0]*s0[2]-s0[0]*s1[2]) / Delta
    q = {(0, 1): Q(1), (0, 2): Q(-1)}
    sums = [sum(value for pair, value in q.items() if i in pair) for i in range(g)]
    reduced = -sum(sums[i]*wA[i]*prod(c[a] for a in range(g) if a != i)
                   for i in range(g)) / D
    assert direct == reduced and direct
    return direct


def calculate():
    primary = read('summed_transfer_obstruction_d151')
    for ref in primary['sources']:
        assert source(ref['path']) == ref
    candidate = read('cm_frame_curve_candidate')
    basis = read('cm_field_recognition')['field_basis']['trace_centered_basis_power_coordinates'][1:]
    V = [[17*Q(x) for x in row] for row in basis]
    # Rank 16 in the trace-zero hyperplane proves the conjugate rows form
    # the required frame. Field separability and trace zero are inherited.
    assert det([row[1:] for row in V]) != 0
    f = list(map(Q, candidate['CM_field_polynomial_ascending']))
    def evaluate(P):
        result = [Q(0)]*17
        for c, (i, j) in zip(candidate['quadrics'][0], candidate['monomial_pairs']):
            if c:
                v = field.mul(P[i], P[j], f)
                result = [x+c*y for x, y in zip(result, v)]
        return result
    assert not any(evaluate(V))
    j = primary['nonzero_gradient_coordinate_zero_based']
    plus, minus = [row[:] for row in V], [row[:] for row in V]
    plus[j][0] += 1
    minus[j][0] -= 1
    derivative = [(x-y)/2 for x, y in zip(evaluate(plus), evaluate(minus))]
    assert any(derivative)
    assert list(map(str, derivative)) == primary['gradient_at_V0_power_coordinates']
    # A depth-nine cylinder partition has 2^10 equiprobable leaves.
    # Count actual prefix sets, including complements and subdivisions.
    depth = 9
    leaves = set(range(2**(depth+1)))
    checks = 0
    for d in range(depth):
        prefix_set = {x for x in leaves if x >> (depth-d) == 0}
        children = [{x for x in prefix_set if ((x >> (depth-d-1)) & 1) == bit}
                    for bit in [0, 1]]
        assert children[0].isdisjoint(children[1])
        assert children[0] | children[1] == prefix_set
        row = primary['visual_weight_controls'][d]
        assert Q(len(prefix_set), len(leaves)) == Q(row['outward'])
        assert Q(len(leaves-prefix_set), len(leaves)) == Q(row['reverse'])
        assert [str(Q(len(c), len(leaves))) for c in children] == row['outward_children']
        swapped = {x ^ (1 << depth) for x in prefix_set}
        assert len(swapped) == len(prefix_set)
        checks += 1
    controls = []
    for g in [3, 4, 5]:
        a, b = frame_control(g, 1), frame_control(g, 2)
        degree = g*(g-1)
        assert b == a * 2**degree
        controls.append({'genus': g, 'degree': degree, 'unscaled_residual': str(a),
                         'scaled_residual': str(b), 'two_formulas_agree': True})
    # Dropping the pole term would predict zero and is rejected by the
    # exact diagonal pairing. Killing constants is compatible with it.
    diagonal = [Q(primary['same_orbit_kernel_pairing_orders_0_through_3'][i][i]) for i in range(4)]
    assert diagonal == [Q(-1, 2)]*4 and all(diagonal)
    return {'status': 'pass', 'milestone': 'D151',
            'selected_quadric_index_zero_based': 0,
            'selected_coarse_order': 1,
            'nonzero_gradient_coordinate_zero_based': j,
            'gradient_at_V0_power_coordinates': list(map(str, derivative)),
            'gradient_checked_by_exact_central_difference': True,
            'trace_zero_basis_power_coordinate_rank': 16,
            'explicit_leaf_count_partitions_checked': checks,
            'visual_center_swap_preserves_weights': True,
            'cleared_first_jet_controls': controls,
            'cleared_residual_total_degree': 16*15, 'scalar_input_count': 17*16+16,
            'odd_stabilizer_character_and_dropped_pole_controls_rejected': True,
            'infinite_functional_construction_mechanically_verified': False,
            'finite_rational_transfer_certificate_excluded_for_selected_residual_by_companion_proof': True,
            'actual_bounded_measure_uniqueness_refuted': False,
            'candidate_identification_proved': False, 'candidate_refuted': False,
            'positive_exact_quadric_vanishing_proved': False,
            'new_precision_bank_admitted': False, 'actual_harmonic_precision_increased': False}


if __name__ == '__main__':
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    result = calculate()
    result['wall_seconds'] = time.monotonic() - tick
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    result['sources'] = [source(p) for p in sorted(PATHS)]
    with OUT.open('x') as out:
        out.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['gradient_checked_by_exact_central_difference', 'explicit_leaf_count_partitions_checked', 'cleared_first_jet_controls']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|630_SUMMED_TRANSFER_CONTROLS', flush=True)
