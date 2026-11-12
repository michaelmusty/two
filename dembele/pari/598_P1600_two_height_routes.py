"""D142: evaluate proved height estimates for both D141 proof targets.

All decision intervals are rational. The cone-constant numerical values
are labelled exploratory; no global corrected RR theorem is inferred.
"""
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
spec = importlib.util.spec_from_file_location('d142_logs', ROOT/'dembele/pari/447_cm_disk_vanishing_budget.py')
logs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logs)
PATHS = {Path(__file__), Path(logs.__file__)}


def source(path):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read(stem):
    p = DATA/(stem+'.json')
    PATHS.add(p)
    v = json.loads(p.read_text())
    assert v['status'] == 'pass'
    return v


def enc(x):
    return list(map(str, x))


def ceil_bound(x):
    n = x[1].numerator//x[1].denominator+1
    assert n-1 < x[0] < x[1] < n
    return n


def build():
    parent = read('P1600_proof_gap_review_d141')
    assert parent['Faltings_lower_29_would_suffice_at_P1600']
    assert not parent['Faltings_lower_29_proved']
    intrinsic = read('cm_intrinsic_height_review_d104')
    read('cm_compound_height_d116')
    read('cm_finite_height_review_d118')
    L2 = logs.LOG2
    pi = logs.pi_interval()
    Lpi = (logs.log(pi[0])[0], logs.log(pi[1])[1])
    plus, scale, log = logs.plus, logs.scale, logs.log
    hL = Q(intrinsic['independent_analytic']['Hodge_height_interval'][1])
    H = plus((2*hL, 2*hL), scale(L2, -Q(35, 34)))
    F = plus(scale(Lpi, -16), scale(L2, -8+Q(55817, 54150)))
    logB = plus(scale(Lpi, -Q(1, 2)), log(Q(5, 3)))
    # D116 complementary minors, with D117's larger certified disk.
    norms = [plus(scale(log(comb(16, k)*16**k), Q(1, 2)),
                  scale(L2, 35*k), scale(logB, 17*(16-k))) for k in (1, 2, 3)]
    # The Gaussian factor 2*sqrt(2) is conservative. Wronskian uses
    # derivative orders 0,1,2, including the factor 2!.
    logGamma = plus(scale(L2, Q(3, 2)), scale(Lpi, -1), scale(log(Q(5, 3)), 3))
    logWr = plus(L2, scale(log(6), Q(1, 2)), scale(Lpi, -Q(3, 2)), scale(log(Q(5, 3)), 6))
    logf = plus(norms[0], logB)
    loggamma = plus(norms[1], logGamma)
    logkappa = plus(norms[2], logWr)
    num = plus(scale(logf, 3), logkappa)
    den = plus(L2, scale(logB, 272), scale(loggamma, 3))
    maxnorm = (max(num[0], den[0]), max(num[1], den[1]))
    B1 = plus(scale(H, 241), scale(F, -15), loggamma, scale(L2, -Q(62681, 272)))
    B2 = plus(scale(H, 995), scale(F, -62), maxnorm, scale(L2, -Q(259649, 272)))
    b1, b2 = ceil_bound(B1), ceil_bound(B2)
    assert b1 < 4723 and b2 < 19438
    B0 = scale(L2, 35)
    # Heights of quadratic Taylor rows: multidegrees (2), (1,1), (1,2,1).
    C0 = scale(B0, 2)
    C1 = plus(B0, B1, L2)
    C2 = plus(B0, scale(B1, 2), B2, log(3))
    assert C0[1] < C1[0] < C1[1] < C2[0]
    # 17 order-zero rows can be extended to 45 using orders 1 and 2.
    # D140's certified rank-45 three-jet constraint supplies this fact.
    coarse = plus(scale(C0, 17), scale(C2, 28), scale(log(136), Q(45, 2)))
    # RR and strict Clifford give rank >=32 through order 1;
    # hence 17,15,13 is the most expensive admissible selection.
    refined = plus(scale(C0, 17), scale(C1, 15), scale(C2, 13), scale(log(136), Q(45, 2)))
    assert coarse[0] > refined[1] > 623
    # Cofactor Cauchy--Binet and AM--GM improve D120's Hadamard bound.
    old_upper = plus(scale(H, 16), scale(logB, 16), scale(L2, -Q(525, 34)))
    saving = plus(scale(log(17), Q(1, 2)), scale(log(Q(17, 16)), -8))
    new_upper = plus(old_upper, scale(saving, -1))
    assert 29 < new_upper[0] < new_upper[1] < 31
    signature = {2: 17, 3: 9, 32: 1}
    d = Q(30)+sum(n*(1-Q(1, m)) for m, n in signature.items())
    assert d == Q(1455, 32)
    psi = {str(m): str(n*(1-Q(1, m*m))) for m, n in signature.items()}
    # 12 F = W_hyp^2 + delta - psi - I - 96 log(pi)
    #        + 6 log(d) - 6 log(C_corrected Z'(1)).
    RR_target = plus((Q(348), Q(348)), scale(Lpi, 96), scale(log(d), -6))
    critical = tuple(map(Q, parent['Faltings_critical_intervals'][2]))
    RR_critical = plus(scale(critical, 12), scale(Lpi, 96), scale(log(d), -6))
    for name in ('cm-compound-height-d116.md', 'cm-disk-and-exactness-d117.md',
                 'cm-finite-height-d118.md', 'cm-cartier-frame-d119.md',
                 'cm-rational-frame-jets-d106.md', 'P1600-proof-gap-d141.md'):
        PATHS.add(ROOT/'dembele/certificates'/name)
    return {'status': 'pass', 'milestone': 'D142',
            'inherited_review': source(DATA/'P1600_proof_gap_review_d141.json'),
            'CM_height_upper_interval': enc(H), 'Faltings_lower_interval': enc(F),
            'new_joint_affine_ratio_height_intervals': [enc(B1), enc(B2)],
            'new_joint_affine_ratio_height_integer_bounds': [b1, b2],
            'quadratic_row_height_intervals': list(map(enc, [C0, C1, C2])),
            'true_relation_space_height_upper_interval': enc(refined),
            'true_relation_space_height_integer_upper': ceil_bound(refined),
            'without_Clifford_height_integer_upper': ceil_bound(coarse),
            'selected_row_counts_worst_case': [17, 15, 13],
            'actual_height_upper_bound_established': True,
            'height_bound_at_most_623_proved': False,
            'Cauchy_Binet_Faltings_upper_interval': enc(new_upper),
            'upper_bound_improvement_interval': enc(saving),
            'Faltings_29_still_numerically_possible': True,
            'orbifold_degree': str(d), 'elliptic_cotangent_weights': psi,
            'dyadic_discriminant_contribution': '19/2 * log(2)',
            'dyadic_order2_ordered_weighted_intersections': '33/4 * log(2)',
            'RR_combination_target_for_29_interval': enc(RR_target),
            'RR_combination_target_for_exactness_interval': enc(RR_critical),
            'RR_combination': 'W_hyp^2 + delta - psi - I - 6 average(log(C_corrected * Zprime(1)))',
            'RR_normalizer_finite_model_comparison_proved': False,
            'corrected_global_RR_constant_certified': False,
            'Faltings_lower_29_proved': False,
            'positive_exact_quadric_vanishing_proved': False,
            'candidate_identification_proved': False,
            'field_polynomial_constructed': False,
            'actual_harmonic_precision_increased': False,
            'next_precision_bank_admitted': False,
            'sources': [source(p) for p in sorted(PATHS)]}


if __name__ == '__main__':
    assert __debug__
    tick = time.monotonic()
    result = build()
    result['wall_seconds'] = time.monotonic()-tick
    result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    out = DATA/'P1600_two_height_routes_d142.json'
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('HEIGHT_ROUTES|' + json.dumps({k: result[k] for k in (
        'new_joint_affine_ratio_height_integer_bounds', 'true_relation_space_height_integer_upper',
        'without_Clifford_height_integer_upper')}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|598_P1600_TWO_HEIGHT_ROUTES', flush=True)
