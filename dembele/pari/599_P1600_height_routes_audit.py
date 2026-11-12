"""D142: independent Arb audit, local cone correction and RR normalization.

Only the local special-function constants are certified. A global RR
constant and the actual normalizer model comparison remain unproved.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
SAGE_BASE = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
SAGE_PYTHON = SAGE_BASE/'venv/bin/python3'


def source(path):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import RealBallField, QQ, ZZ, matrix, gcd, prime_range, NumberField, PolynomialRing
    from itertools import combinations
    R = RealBallField(192)
    def iv(x):
        return [str(QQ(x.lower())), str(QQ(x.upper()))]
    def ball(pair):
        a, b = map(QQ, pair)
        return R((a+b)/2, (b-a)/2)
    diag = json.loads((DATA/'P1600_two_height_routes_d142.json').read_text())
    intrinsic = json.loads((DATA/'cm_intrinsic_height_review_d104.json').read_text())
    hL = R(QQ(intrinsic['independent_analytic']['Hodge_height_interval'][1]))
    l2, lp, lo = R(2).log(), R.pi().log(), R(QQ(5)/3).log()
    H = 2*hL-QQ(35)/34*l2
    F = -16*lp+(-8+QQ(55817)/54150)*l2
    # Collected expressions, independent of source 598's line/norm assembly.
    B1 = 241*H-15*F+(QQ(143)/2-QQ(62681)/272)*l2-120*lp+241*lo+R(30720).log()/2
    cn = 211*l2+R(256**3*2293760*6).log()/2
    cd = QQ(431)/2*l2+R(30720).log()*QQ(3)/2
    assert cn < cd
    B2 = 995*H-62*F-496*lp+995*lo-QQ(259649)/272*l2+cd
    for x, pair, target in zip((B1, B2), diag['new_joint_affine_ratio_height_intervals'], (871, 3532)):
        assert x.overlaps(ball(pair)) and target-1 < x < target
    c0 = 70*l2
    c1 = 36*l2+B1
    c2 = 35*l2+2*B1+B2+R(3).log()
    selection = []
    for rank in range(32, 35):
        val = 17*c0+(rank-17)*c1+(45-rank)*c2+QQ(45)/2*R(136).log()
        selection.append({'rank_through_order1': rank, 'height_upper_interval': iv(val)})
    refined = 17*c0+15*c1+13*c2+QQ(45)/2*R(136).log()
    assert refined.overlaps(ball(diag['true_relation_space_height_upper_interval']))
    assert 83239 < refined < 83240
    upper = 16*H-8*lp+16*lo-QQ(525)/34*l2+8*R(QQ(17)/16).log()-R(17).log()/2
    assert upper.overlaps(ball(diag['Cauchy_Binet_Faltings_upper_interval']))
    # Small exact controls for kernel-height duality and the cofactor inequalities.
    controls = 0
    for seed in range(1, 51):
        A = matrix(ZZ, 3, 5, [((seed+3*i+7*j)**2+11*i*j)%17-8 for i in range(3) for j in range(5)])
        if A.rank() != 3:
            continue
        minors = [A.matrix_from_columns(list(J)).det() for J in combinations(range(5), 3)]
        content = gcd(minors)
        K = A.right_kernel().basis_matrix()
        assert (A*A.transpose()).det()/content**2 == (K*K.transpose()).det()
        E = A.matrix_from_columns([0, 1, 2, 3]).transpose()
        G = E.transpose()*E
        cofs = [E.matrix_from_rows([j for j in range(4) if j != i]).det() for i in range(4)]
        assert sum(c*c for c in cofs) == G.det()
        assert 27*G.det() <= G.trace()**3
        product = ZZ(1)
        for c in cofs:
            product *= c*c
        assert 4**4*product <= sum(c*c for c in cofs)**4
        controls += 1
    assert controls >= 40
    # Local constant difference: Kalvin (1.5) minus F-vP Theorem 2.5.
    z, e = R(-1).zetaderiv(1), R.euler_constant()
    cone = []
    for m in (1, 2, 3, 32):
        lm = R(m).log()
        gammas = sum(R(j)*R(QQ(j)/m).log_gamma() for j in range(1, m))
        old = -m*(-2*z+QQ(1)/6-l2/6)-(QQ(5)/12-l2/6+e/6)/m+lm/2+m*lm/6+lm/(6*m)+QQ(1)/4
        new = -m*(l2/3+lp/2)-(2*z-2*gammas+QQ(5)/12-l2/6)/m+lm/2+m*lm/6+lm/(3*m)
        delta = m*(QQ(1)/6-2*z-(l2+lp)/2)+(-2*z+2*gammas+e/6+lm/6)/m-QQ(1)/4
        assert (new-old-delta).contains_zero()
        assert delta < 0
        cone.append({'order': m, 'new_minus_old_constant_interval': iv(delta)})
    total = 17*ball(cone[1]['new_minus_old_constant_interval'])+9*ball(cone[2]['new_minus_old_constant_interval'])+ball(cone[3]['new_minus_old_constant_interval'])
    # No local-to-global numerical substitution is asserted here.
    # A certified modular main term via the functional equation and Euler tail.
    P = PolynomialRing(QQ, 'x'); x = P.gen()
    number_field = NumberField(x**8-8*x**6+20*x**4-16*x**2+2, 'b')
    assert number_field.discriminant() == 2**31
    cut = 10000
    logarithmic_derivative_partial = -l2/3
    count = 0
    for p in prime_range(3, cut+1):
        f = next(k for k in (1, 2, 4, 8) if pow(int(p), k, 32) in (1, 31))
        logarithmic_derivative_partial -= 8*R(p).log()/(p**(2*f)-1)
        count += 1
    tail = 8*(R(cut).log()+1)/(cut*(1-QQ(1)/(cut+1)**2))
    lp2 = logarithmic_derivative_partial+R(-tail.upper()/2, tail.upper()/2)
    Y = QQ(97)/4*l2-8*lp-8*e+4+lp2
    d = QQ(1455)/32
    W = 2*d*Y/8+d*l2
    M = W+QQ(19)/2*l2-96*lp+6*R(d).log()
    RR29 = 348+96*lp-6*R(d).log()
    assert RR29.overlaps(ball(diag['RR_combination_target_for_29_interval']))
    result = {'status': 'pass', 'milestone': 'D142', 'arb_precision_bits': 192,
        'independent_joint_affine_ratio_bounds': [iv(B1), iv(B2)],
        'independent_true_relation_space_upper_interval': iv(refined),
        'row_selection_cases': selection, 'exact_small_lattice_controls': controls,
        'independent_Faltings_upper_interval': iv(upper),
        'cone_differences': cone, 'signature_sum_cone_difference_interval': iv(total),
        'formal_Faltings_shift_if_other_RR_ingredients_hold_interval': iv(total/2),
        'corrected_global_RR_constant_certified': False,
        'Dedekind_Euler_cutoff': cut, 'odd_Euler_factors_checked': count,
        'Dedekind_log_derivative_at_2_interval': iv(lp2),
        'Yuan_relative_modular_height_interval': iv(Y),
        'Yuan_absolute_modular_height_interval': iv(Y/8),
        'hyp_self_intersection_main_term_if_models_match_interval': iv(W),
        'RR_main_term_in_12F_interval': iv(M),
        'residual_needed_for_Faltings_29_interval': iv(348-M),
        'residual_formula': 'E_model + delta_other - psi - I - 6 average(log(C_corrected Zprime(1)))',
        'RR_model_remainder_assumed_zero': False,
        'Faltings_lower_29_proved': False, 'height_bound_at_most_623_proved': False,
        'candidate_identification_proved': False,
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D142_HEIGHT_AUDIT_WORKER_PASS', flush=True)


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', type=Path)
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
        sys.exit(0)
    tick = time.monotonic()
    output = DATA/'P1600_height_routes_audit_d142.json'
    child_path = DATA/'P1600_height_routes_audit_d142_worker.json'
    assert not output.exists() and not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE_BASE/'local/bin')+':'+str(SAGE_BASE/'venv/bin')+':'+env.get('PATH', '')
    child = subprocess.run([str(SAGE_PYTHON), str(Path(__file__).resolve()), '--worker', str(child_path)], cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D142_HEIGHT_AUDIT_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    result = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    child_rss = max(result['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform == 'darwin' else 1024))
    assert rss+child_rss < 2*(1 << 30)
    result.update({'wall_seconds': time.monotonic()-tick, 'peak_rss_bytes': rss,
                   'child_peak_rss_bytes': child_rss, 'conservative_peak_rss_bytes': rss+child_rss,
                   'sources': [source(p) for p in [Path(__file__), SAGE_PYTHON, child_path,
                       DATA/'P1600_two_height_routes_d142.json', DATA/'cm_intrinsic_height_review_d104.json']]})
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('PHASE_METADATA|' + json.dumps(source(output)), flush=True)
    print('PASS|599_P1600_HEIGHT_ROUTES_AUDIT', flush=True)
