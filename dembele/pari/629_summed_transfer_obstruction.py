"""D151 finite witnesses for the rational summed-transfer obstruction.

Run through run_dyadic_capped.py. The infinite-dimensional functional
construction is a companion proof, not mechanically verified here.
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
OUT = DATA / 'summed_transfer_obstruction_d151.json'
PATHS = {Path(__file__)}


def source(path):
    p = Path(path).resolve()
    PATHS.add(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(stem):
    p = DATA / (stem + '.json')
    source(p)
    return json.loads(p.read_text())


def multiply(a, b, modulus):
    """Schoolbook polynomial multiplication and monic Euclidean remainder."""
    n = len(modulus) - 1
    out = [Q(0)] * (2 * n - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    while len(out) > n:
        lead = out.pop()
        shift = len(out) - n
        for j, c in enumerate(modulus[:-1]):
            out[shift + j] -= lead * c
    return out


def power_traces(f):
    n = len(f) - 1
    ans = [Q(n)]
    for k in range(1, n):
        ans.append(-sum(f[n-j] * ans[k-j] for j in range(1, k)) - k * f[n-k])
    return ans


def calculate():
    candidate = read('cm_frame_curve_candidate')
    field = read('cm_field_recognition')
    prior = read('structural_identification_review_d150')
    assert prior['status'] == 'pass' and not prior['candidate_identification_proved']
    f = list(map(Q, candidate['CM_field_polynomial_ascending']))
    assert len(f) == 18 and f[-1] == 1
    eta = [list(map(Q, row)) for row in field['field_basis']['trace_centered_basis_power_coordinates'][1:]]
    assert len(eta) == 16 and all(len(row) == 17 for row in eta)
    V = [[17*x for x in row] for row in eta]
    traces = power_traces(f)
    assert all(sum(x*t for x, t in zip(row, traces)) == 0 for row in V)
    pairs = candidate['monomial_pairs']
    assert len(pairs) == 136 and len(candidate['quadrics']) == 91
    quadric = candidate['quadrics'][0]
    value = [Q(0)] * 17
    gradient = [[Q(0)] * 17 for _ in range(16)]
    terms = []
    for coefficient, (i, j) in zip(quadric, pairs):
        if not coefficient:
            continue
        terms.append({'i': i, 'j': j, 'coefficient': coefficient})
        product = multiply(V[i], V[j], f)
        value = [a + coefficient*b for a, b in zip(value, product)]
        for k in range(17):
            gradient[i][k] += coefficient * V[j][k]
            gradient[j][k] += coefficient * V[i][k]
    assert not any(value)
    coordinate = next(i for i, row in enumerate(gradient) if any(row))
    # Exact visual weights on the residue-two tree. A central half-tree
    # has mass 1/2; outward depth d has mass 2^(-d-1).
    weights = []
    for depth in range(9):
        mass = Q(1, 2**(depth+1))
        child = mass / 2
        assert mass == child + child
        # Reverse of a depth-d edge partitions into the inward component
        # and its sibling. At the centre both other branches have mass 1/4.
        inward = Q(1, 4) if depth == 0 else 1 - 2*mass
        sibling = Q(1, 4) if depth == 0 else mass
        assert 1 - mass == inward + sibling
        assert mass + (1-mass) == 1
        weights.append({'depth': depth, 'outward': str(mass), 'reverse': str(1-mass),
                        'outward_children': [str(child)]*2,
                        'reverse_children': [str(inward), str(sibling)]})
    # In local w, the twice-A kernel is 1-w^(-2j-2).
    # Pullback by the point stabilizer is exactly w -> -w.
    laurent_kernels = [{0: Q(1), -2*j-2: Q(-1)} for j in range(4)]
    pairing = []
    for r in range(1, 5):
        row = []
        for kernel in laurent_kernels:
            assert all(c == c * (-1)**abs(power) for power, c in kernel.items())
            row.append(str(Q(1, 2) * kernel.get(-2*r, Q(0))))
        pairing.append(row)
    assert pairing == [[str(Q(-1, 2) if i == j else Q(0)) for j in range(4)] for i in range(4)]
    assert (-1)**(-1) != 1  # Odd Laurent coefficient is not stabilizer-invariant.
    return {'status': 'pass', 'milestone': 'D151',
            'selected_quadric_index_zero_based': 0, 'selected_CM_index_zero_based': 0,
            'selected_coarse_order': 1, 'frame_coordinates': 'V_i,j = sigma_i(17 eta_j)',
            'selected_quadric_terms': terms, 'selected_quadric_vanishes_on_V0_exactly': True,
            'V0_trace_zero_coordinates': 16,
            'nonzero_gradient_coordinate_zero_based': coordinate,
            'gradient_at_V0_power_coordinates': [str(x) for x in gradient[coordinate]],
            'formal_specialization': {'M': 'I_16', 'z': '(-1,...,-1)',
                                      'cofactors_c0_through_c16': [1]*17,
                                      'Delta': 1, 'Phi': 'I_16',
                                      'w': 'e_j * inverse(V_nonanchor)',
                                      'residual_at_w_zero': '0',
                                      'residual_at_w_selected': 'partial_j Q(V0) != 0'},
            'cleared_residual_total_degree': 16*15,
            'scalar_input_count': 17*16+16,
            'residual_is_nonconstant_by_companion_specialization_proof': True,
            'visual_weight_controls': weights, 'same_orbit_kernel_pairing_orders_0_through_3': pairing,
            'odd_principal_part_control_rejected': True,
            'distinct_orbit_cross_pairings_zero_by_D112': True,
            'all_polynomial_moments_annihilated_by_companion_proof': True,
            'finite_rational_transfer_certificate_excluded_for_selected_residual_by_companion_proof': True,
            'obstruction_functionals_are_discontinuous': True,
            'actual_bounded_measure_uniqueness_refuted': False,
            'candidate_identification_proved': False, 'candidate_refuted': False,
            'positive_exact_quadric_vanishing_proved': False,
            'field_polynomial_constructed': False, 'actual_harmonic_precision_increased': False,
            'new_precision_bank_admitted': False,
            'best_current_proved_relation_height_upper': 15237, 'sufficient_height_target': 623}


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
    print(json.dumps({k: result[k] for k in ['selected_quadric_index_zero_based', 'nonzero_gradient_coordinate_zero_based', 'gradient_at_V0_power_coordinates', 'cleared_residual_total_degree']}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|629_SUMMED_TRANSFER_OBSTRUCTION', flush=True)
