"""D120 independent budget, precision, norm-97 and provenance review."""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
OUT = DATA/'construction_reassessment_review_d120.json'


def module(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT/'dembele/pari'/path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


l = module('independent_logs', '450_cm_disk_exactness_review.py')


def read(name):
    return json.loads((DATA/(name+'.json')).read_text())


def source(p):
    p = Path(p).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def checked(rows):
    result = []
    for row in rows:
        p = Path(row['path'])
        assert source(p) == row
        result.append(p)
    return result


def overlap(a, b):
    assert max(a[0], Q(b[0])) <= min(a[1], Q(b[1]))


def budget_review():
    packet = read('cm_inverse_frame_budget_d120')
    design = read('dyadic_precision_design_d120')['precision_design']
    old = read('cm_arithmetic_height_budget_d118')['budgets']
    pi = l.rounded(l.plus(l.scale(l.atan(Q(1, 5)), 16), l.scale(l.atan(Q(1, 239)), -4)))
    logpi = l.log(pi[0])[0], l.log(pi[1])[1]
    hL, theta = Q(old['saved_Hodge_height_upper']), Q(55817, 54150)
    H = l.plus((2*hL, 2*hL), l.scale(l.L2, -Q(35, 34)))
    B = l.plus(l.scale(logpi, -Q(1, 2)), l.log(Q(5, 3)))
    F = l.plus(l.scale(logpi, -16), l.scale(l.L2, theta-8))
    I, tau = l.scale(l.L2, Q(33, 2)), l.scale(l.L2, Q(7, 8))
    pencil = l.plus(l.scale(H, -17), F, I, tau, l.scale(l.log(Q(17, 16)), -8), l.scale(B, -16))
    upper = l.plus(l.scale(H, 16), l.scale(B, 16), l.scale(l.L2, -Q(525, 34)))
    overlap(upper, packet['Faltings_upper_from_existing_minors_interval'])
    assert upper[1] < 31
    C = [l.scale(l.sqrt(2), 2), l.plus(l.scale(l.sqrt(3), 2), (Q(2), Q(2))),
         l.plus(l.scale(l.sqrt(6), 2), (Q(4), Q(4)))]
    new_targets, precision_targets = [], []
    for row, o, d, cn in zip(packet['rows'], old['thresholds'], design['rows'], C):
        n = row['order']
        logC = l.log(cn[0])[0], l.log(cn[1])[1]
        # Review the unsimplified metric/adjugate expression rather than
        # copying the coefficients of 458's final expanded formula.
        expression = l.plus(l.scale(H, n+2), l.scale(pencil, -30), l.scale(F, -2),
            l.scale(I, 2), l.scale(l.L2, -Q(7, 4)), l.scale(B, 32), l.scale(l.log(15), -15),
            l.log(42550), l.scale(l.L2, 70), logC, l.scale(l.log(Q(5, 3)), n))
        overlap(expression, row['inverse_frame_bound_interval'])
        target = (17*expression[1]/l.L2[0]).__floor__()+1
        assert target-1 < 17*expression[0]/l.L2[1] < target
        assert target == row['new_frame_sufficient_nonanchor_beta']
        assert row['new_frame_achieved_nonanchor_beta'] == o['achieved_degree16_lower_beta']-3640
        oldF = l.plus(l.scale(H, 240+n), l.scale(F, -15),
            l.scale(B, 238), l.log(480*42550), l.scale(l.L2, 70),
            logC, l.scale(B, 2), l.scale(l.log(Q(5, 3)), n))
        overlap(oldF, o['upper_bound_expression_interval'])
        zeros = l.scale(l.L2, Q(16*o['achieved_degree16_lower_beta']+o['certified_anchor_lower_beta'], 272))
        needed = l.plus(F, l.scale(l.plus(oldF, l.scale(zeros, -1)), Q(1, 15)))
        overlap(needed, row['Faltings_only_rescue_required_strict_lower_interval'])
        assert needed[0] > upper[1]
        # Derive the sufficient P directly from the two local error bounds.
        Nconst, Aconst = 3310-33*n, 2784-296*n
        low = 8*oldF[0]/l.L2[1]-Q(16*Nconst+Aconst, 34)
        high = 8*oldF[1]/l.L2[0]-Q(16*Nconst+Aconst, 34)
        minimum = high.__floor__()+1
        assert minimum-1 < low < high < minimum
        P = 8*((minimum+7)//8)
        assert P == d['sufficient_P_rounded_to_multiple_of_eight']
        new_targets.append(target)
        precision_targets.append(P)
    assert new_targets == [43459, 43553, 43642]
    assert precision_targets == [10416, 10480, 10552]
    return {'independent_logarithm_series': '-log(1-t), 256 terms',
            'rejected_inverse_frame_thresholds': new_targets,
            'Faltings_upper_strictly_below': 31,
            'conditional_P_by_order': precision_targets}


def inverse_and_precision_review():
    f = module('ball_inverse', '427_dyadic_second_order_comparison.py')
    bank = read('dyadic_precision200_d115')
    matrix = [[f.center(x, 432)/(f.BETA**33) for x in row['coarse_coefficients_beta'][0]]
              for row in bank['CM_values'][1:]]
    inverse, _, failed = f.inverse(matrix)
    assert failed is None
    assert min(x.lower() for row in inverse for x in row) == -35
    assert all(x.error > 0 for row in inverse for x in row)
    # This uses valuation-ball Gauss--Jordan, independent of 461's
    # quotient-ring Smith extraction. Its inverse routine checks H*H^-1.
    E = 30000
    inv_error = (E-33)-2*35
    relation_error = min((E-296)-35, inv_error)
    reciprocal_error = relation_error+70
    weighted_error = min(E+35, reciprocal_error)
    change_error = min(inv_error+35, weighted_error-35)
    assert (inv_error, relation_error, reciprocal_error, change_error) == (E-103, E-331, E-261, E-296)
    assert -35+35 == 0
    assert min(E, change_error) == E-296
    d = read('dyadic_precision_design_d120')['precision_design']
    P = d['sufficient_common_P_under_stated_hypotheses']
    assert P == 10552 and d['coefficient_modulus_bits'] == 1319
    byte = (P//8+7)//8
    assert d['one_harmonic_column_low_moment_packed_payload_bytes'] == 174*P*8*byte
    assert d['sixteen_harmonic_columns_low_moment_packed_payload_bytes'] == 16*174*P*8*byte
    assert d['old_dense_child_operator_packed_payload_bytes'] == 165*(3*P-1)*P*8*byte
    return {'inverse_entries_checked_by_ball_Gauss_Jordan': 256,
            'inverse_entry_lower_beta': -35,
            'independent_error_propagation_checked': True,
            'future_zero_enclosures_and_refined_inputs_remain_required': True}


def norm97_review():
    # List-polynomial arithmetic, independent of 460's bit-polynomial code.
    def trim(a):
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        return a
    def multiply(a, b):
        out = [0]*(len(a)+len(b)-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i+j] ^= x & y
        return trim(out)
    def rem(a, p):
        a = a[:]
        while len(a) >= len(p):
            if a[-1]:
                start = len(a)-len(p)
                for j, x in enumerate(p):
                    a[start+j] ^= x
            a.pop()
        return trim(a or [0])
    def powmod(a, n, p):
        ans = [1]
        for _ in range(n):
            ans = rem(multiply(ans, a), p)
        return ans
    p = read('norm97_target_isolation_d120')
    for index, row in enumerate(p['targets']):
        h = row['trace_polynomial_coefficients']
        psi = [0]*17
        q = [1]
        for i, c in enumerate(h):
            if c:
                for j, a in enumerate(q):
                    psi[8-i+j] ^= a
            q = multiply(q, [1, 0, 1])
        assert psi == row['torsion_polynomial_coefficients']
        product = [1]
        for factor in row['irreducible_factor_coefficients']:
            product = multiply(product, factor)
            order = 51 if index == 0 else 257
            assert powmod([0, 1], order, factor) == [1]
            for divisor in ([3, 17] if index == 0 else [1]):
                assert powmod([0, 1], divisor, factor) != [1]
        assert product == psi
        assert row['factor_degrees'] == ([8, 8] if index == 0 else [16])
    assert [(a, c) for a in range(5) for c in range(1, 5) if 3+2*a+c == 4] == [(0, 1)]
    assert p['T31_to_T97_target_factor_indices_one_based'] == [2, 1]
    assert p['target_torsion_rational_over_residue_extension_degrees'] == [51, 257]
    return {'cofactor_separation_uses_D51_and_frozen_Hecke_inputs': True,
            'independent_polynomial_arithmetic': 'coefficient lists',
            'target_orders': [51, 257], 'preferred_original_T31_factor_index': 2}


def transport_review():
    slow = read('dyadic_mobius_transform_d120')
    fast = read('dyadic_gmp_transport_d120')
    target = read('dyadic_gmp_target_cost_d120')
    for p in (slow, fast['actual_frozen_bank_checks']):
        assert [p[k] for k in ['state_equations_checked', 'child_actions_checked', 'distinct_child_maps_checked', 'CM_charts_checked']] == [174, 348, 165, 17]
        assert p['basis_columns_checked'] == [0]
        assert not p['actual_moment_precision_increased']
        assert p['state_coefficients_checked']+p['CM_coefficients_checked'] == 332800
    assert fast['large_buffer_python_integer_controls'] == target['large_buffer_python_integer_controls'] == 3
    assert target['synthetic_benchmarks'][0]['synthetic_P'] == 10552
    assert not target['actual_moment_precision_increased']
    # Verify the packing inequality over all design/probe precisions and
    # lengths, including the actual target. No machine-word wrap is allowed.
    controls = 0
    for bits in (3, 25, 50, 100, 200, 1319, 1536):
        for n in (1, 5, 199, 599, 1600, 10552):
            width = (2*bits+(8*n).bit_length()+7)//8
            assert 8*n*((1 << bits)-1)**2 < 1 << (8*width)
            controls += 1
    return {'actual_coefficients_checked_in_each_backend': 332800,
            'actual_harmonic_columns_checked': 1,
            'packing_bound_controls': controls,
            'synthetic_target_action_completed': True,
            'synthetic_target_is_not_an_actual_moment_refinement': True}


def calculations():
    result = {'budget': budget_review(), 'precision': inverse_and_precision_review(),
              'norm97': norm97_review(), 'transport': transport_review()}
    print('REASSESSMENT_REVIEW|independent norms, inverse, error propagation and target factors pass', flush=True)
    return result


def build(certificate):
    priorpath = DATA/'cm_cartier_frame_review_d119.json'
    prior = json.loads(priorpath.read_text())
    assert prior['status'] == 'pass' and len(prior['sources']) == 922
    paths = checked(prior['sources'])+[priorpath, Path(__file__),
        ROOT/'dembele/certificates/construction-reassessment-d120.md',
        DATA/'construction_reassessment_sources_d120.json']
    jobs = []
    for p in sorted(DATA.glob('*d120*')):
        if p.name.startswith('construction_reassessment_review_d120'):
            continue
        paths.append(p)
        if p.suffix != '.json':
            continue
        packet = json.loads(p.read_text())
        paths += checked([x for x in packet.get('sources', []) if isinstance(x, dict) and 'sha256' in x])
        if p.name.endswith('.job.json'):
            assert packet['timeout_seconds'] == 180 and packet['timeout_terminates_process_group']
            paths += checked([packet['log']])
            if packet['status'] == 'pass':
                paths += checked([packet['driver']])
            else:
                assert packet['status'] == 'failed'
                snap = packet['failed_driver_snapshot']
                paths += checked([snap])
                assert snap['sha256'] == packet['driver']['sha256']
            jobs.append({'receipt': p.name, 'status': packet['status'], 'wall_seconds': packet['wall_seconds']})
    assert len(jobs) == 8 and sum(j['status'] == 'pass' for j in jobs) == 7
    return {'status': 'pass', 'milestone': 'D120', 'D119_source_hashes_checked_unchanged': 922,
        'certificate': certificate, 'bounded_jobs': jobs,
        'inverse_frame_estimate_rejected': True,
        'Faltings_only_rescue_of_D118_current_bound_excluded': True,
        'conditional_sufficient_moment_precision_pi': 10552,
        'norm97_target_cofactor_separation_proved_via_companion_report': True,
        'actual_moment_precision_increased': False,
        'large_precision_solver_ready': False,
        'positive_quadric_jet_exact_vanishing_proved': False,
        'candidate_identification_proved': False,
        'target_field_polynomial_constructed': False,
        'sources': [source(p) for p in sorted(set(p.resolve() for p in paths))]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = calculations()
    if not args.probe:
        result = build(result)
        if args.check:
            previous = json.loads(OUT.read_text())
            checked(previous['sources'])
            assert previous == result
        else:
            assert not OUT.exists()
            OUT.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({'status': 'pass', 'sources': len(result['sources']), 'D119_preserved': 922}), flush=True)
    print('PASS|462_CONSTRUCTION_REASSESSMENT_REVIEW', flush=True)
