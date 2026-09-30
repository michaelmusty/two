"""D120: price the Cartier inverse frame and rule out a Faltings-only rescue.

The companion report supplies the geometric and metric arguments.  All
numerical decisions here use rational, outward-rounded logarithm intervals.
No new moments or exact-zero claims are produced.
"""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
s = importlib.util.spec_from_file_location('logs', ROOT / 'dembele/pari/447_cm_disk_vanishing_budget.py')
b = importlib.util.module_from_spec(s)
s.loader.exec_module(b)


def build():
    prior = json.loads((DATA / 'cm_arithmetic_height_budget_d118.json').read_text())['budgets']
    hL = Q(prior['saved_Hodge_height_upper'])
    H = b.plus((2*hL, 2*hL), b.scale(b.LOG2, -Q(35, 34)))
    theta = Q(prior['tropical_Faltings_coefficient_log2'])
    pi = b.pi_interval()
    logpi = (b.log(pi[0])[0], b.log(pi[1])[1])
    logr = b.log(Q(5, 3))
    logB = b.plus(b.scale(logpi, -Q(1, 2)), logr)
    hFal = b.plus(b.scale(logpi, -16), b.scale(b.LOG2, theta-8))
    # A single nonzero cofactor has degree 16H-hFal and dyadic zero
    # degree (280+16*245)/272 log(2); every archimedean norm is <= B^16.
    hFal_upper = b.plus(b.scale(H, 16), b.scale(logB, 16), b.scale(b.LOG2, -Q(525, 34)))
    assert hFal_upper[1] < 31
    I = b.scale(b.LOG2, Q(33, 2))
    tau = b.scale(b.LOG2, Q(7, 8))
    clearing_gain = b.scale(b.LOG2, -Q(7, 4))
    pencil_lower = b.plus(b.scale(H, -17), hFal, I, tau,
                          b.scale(b.log(Q(17, 16)), -8), b.scale(logB, -16))
    C = {1: b.scale(b.sqrt_interval(2), 2),
         2: b.plus(b.scale(b.sqrt_interval(3), 2), (Q(2), Q(2))),
         3: b.plus(b.scale(b.sqrt_interval(6), 2), (Q(4), Q(4)))}
    L = prior['maximum_quadric_coefficient_l1_norm']
    assert L == 42550
    rows = []
    for old in prior['thresholds']:
        n = old['order']
        logC = (b.log(C[n][0])[0], b.log(C[n][1])[1])
        # Unsimplified determinant/adjugate estimate, before substituting
        # the pencil-line inequality.  This cross-check catches lost indices.
        direct = b.plus(b.scale(H, n+2), b.scale(pencil_lower, -30),
                        b.scale(hFal, -2), b.scale(I, 2), clearing_gain,
                        b.scale(logB, 32), b.scale(b.log(15), -15),
                        b.log(L), b.scale(b.LOG2, 70), logC, b.scale(logr, n))
        pieces = {
            'CM_fibre_degree': b.scale(H, 512+n),
            'finite_and_Faltings_log2': b.scale(b.LOG2, -164-32*theta),
            'net_pi_factor': b.scale(logpi, 256),
            'quadric_coefficient': b.log(L),
            'jet_constant': logC,
            'restriction_volume_AMGM': b.scale(b.log(Q(17, 16)), 240),
            'adjugate_Hilbert_Schmidt_gain': b.scale(b.log(15), -15),
            'disk_radius': b.scale(logr, 512+n),
        }
        total = b.plus(*pieces.values())
        assert max(total[0], direct[0]) < min(total[1], direct[1])
        Nlo, Nhi = 17*total[0]/b.LOG2[1], 17*total[1]/b.LOG2[0]
        required = Nhi.__floor__()+1
        assert required-1 < Nlo < Nhi < required
        # At 2 the cleared new frame is -17 psi, whereas the old integral
        # quadratic section is 17^2*(Delta/c_W^2)*Q(psi).
        removed = 4200-2*280
        actual = max(0, old['achieved_degree16_lower_beta']-removed)
        anchor = max(0, old['certified_anchor_lower_beta']-removed)
        assert anchor == 0
        old_total = tuple(map(Q, old['upper_bound_expression_interval']))
        old_zero = b.scale(b.LOG2, Q(16*old['achieved_degree16_lower_beta']+old['certified_anchor_lower_beta'], 272))
        # To close the *existing* D118 bound by changing hFal alone,
        # hFal must exceed hFal_lower+(old_total-measured_zero_degree)/15.
        needed = b.plus(hFal, b.scale(b.plus(old_total, b.scale(old_zero, -1)), Q(1, 15)))
        assert hFal_upper[1] < needed[0]
        new_margin = b.plus(total, b.scale(b.LOG2, -Q(actual, 17)))
        old_margin = b.plus(old_total, b.scale(old_zero, -1))
        assert new_margin[0] > old_margin[1] > 0
        rows.append({
            'order': n,
            'previous_exact_zero_orders_required': list(range(n)),
            'inverse_frame_bound_interval': list(map(str, total)),
            'inverse_frame_bound_pieces': {k: list(map(str, v)) for k, v in pieces.items()},
            'new_frame_sufficient_nonanchor_beta': required,
            'new_frame_achieved_nonanchor_beta': actual,
            'new_frame_achieved_anchor_beta': anchor,
            'removed_old_quadratic_scalar_beta': removed,
            'new_frame_valuation_gap': required-actual,
            'new_frame_degree_minus_measured_zeros_interval': list(map(str, new_margin)),
            'old_frame_degree_minus_measured_zeros_interval': list(map(str, old_margin)),
            'Faltings_only_rescue_required_strict_lower_interval': list(map(str, needed)),
            'Faltings_only_rescue_excluded_for_current_bound': True,
            'new_inverse_bound_worse_than_D118': True,
            'exact_vanishing_proved': False,
        })
    result = {
        'status': 'pass', 'milestone': 'D120',
        'CM_fibre_upper_interval': list(map(str, H)),
        'Faltings_lower_interval': list(map(str, hFal)),
        'Faltings_upper_from_existing_minors_interval': list(map(str, hFal_upper)),
        'pencil_line_lower_interval': list(map(str, pencil_lower)),
        'inverse_frame_formula': '(512+n)*H+(-164-32*theta)*log(2)+256*log(pi)+log(L)+log(C_n)+240*log(17/16)-15*log(15)+(512+n)*log(5/3)',
        'odd_residue_indices_cancel_using_Fitting_clearing': True,
        'rows': rows,
        'decision': 'Reject this inverse-frame estimate; retain D118 and develop a costed precision algorithm.',
        'limitation': 'This compares the proved estimates on the current bank, not every possible residue-frame or height argument.',
        'actual_moment_precision_increased': False,
        'positive_quadric_jet_exact_vanishing_proved': False,
        'candidate_identification_proved': False,
        'target_field_polynomial_constructed': False,
        'sources': [b.source(p) for p in [Path(__file__), Path(b.__file__),
            DATA/'cm_arithmetic_height_budget_d118.json', DATA/'cm_cartier_principal_parts_d119.json',
            DATA/'cm_cartier_frame_review_d119.json', ROOT/'dembele/certificates/cm-cartier-frame-d119.md']],
    }
    print('INVERSE_FRAME_BUDGET|'+json.dumps([{
        k: r[k] for k in ('order', 'new_frame_sufficient_nonanchor_beta',
                          'new_frame_achieved_nonanchor_beta', 'new_frame_valuation_gap')}
        for r in rows]), flush=True)
    print('FALTINGS_UPPER|'+str(float(hFal_upper[1])), flush=True)
    return result


if __name__ == '__main__':
    out = DATA/'cm_inverse_frame_budget_d120.json'
    assert not out.exists()
    out.write_text(json.dumps(build(), indent=2)+'\n')
    print('PASS|458_CM_INVERSE_FRAME_BUDGET', flush=True)
