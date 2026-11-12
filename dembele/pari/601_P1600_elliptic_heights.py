"""D143: exact odd characters and certified order-3/order-32 CM heights.

The geometric derivative and model comparisons are proved in the report.
This bounded computation checks their constants, not the missing RR theorem.
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
SAGE = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
PYTHON = SAGE/'venv/bin/python3'


def source(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def worker(out):
    from sage.all import CyclotomicField, QQ, ZZ, RealBallField, PolynomialRing, factorial, gcd, prod
    K = CyclotomicField(8); w = K.gen()
    R = RealBallField(192)
    iv = lambda x: [str(QQ(x.lower())), str(QQ(x.upper()))]
    logs = {((-1)**e*pow(5, j, 32)) % 32: (e, j) for e in range(2) for j in range(8)}
    assert len(logs) == 16
    records = []
    for order, modulus in ((3, 96), (32, 32)):
        units = [a for a in range(1, modulus) if gcd(a, modulus) == 1]
        chars, common_A = [], []
        for m in range(8):
            vals = {}
            for a in units:
                e, j = logs[a % 32]
                sign = (-1)**e if order == 32 else (1 if a % 3 == 1 else -1)
                vals[a] = sign*w**(m*j)
            assert vals[modulus-1] == -1
            for a in units:
                for b in units:
                    assert vals[a*b % modulus] == vals[a]*vals[b]
            common_a = -sum(K(a)*vals[a] for a in units)/modulus
            assert common_a != 0
            common_A.append(common_a)
            for f in ZZ(modulus).divisors():
                table = {}
                agrees = True
                for a in units:
                    key = int(a % f)
                    if key in table and table[key] != vals[a]:
                        agrees = False
                        break
                    table[key] = vals[a]
                if agrees:
                    break
            primitive_a = -sum(K(a)*v for a, v in table.items())/f
            assert primitive_a != 0
            chars.append({'m': m, 'conductor': int(f), 'L0_exact': str(primitive_a),
                          'common_L0_exact': str(common_a), 'primitive_values': {str(a): str(v) for a, v in sorted(table.items())}})
        coeffs = {a: QQ(sum(((-1)**logs[a % 32][0] if order == 32 else (1 if a % 3 == 1 else -1))*w**(m*logs[a % 32][1])/common_A[m] for m in range(8))) for a in units}
        assert sum(coeffs.values()) == 0
        common_R = -8*R(modulus).log()+sum(R(c)*R(QQ(a)/modulus).log_gamma() for a, c in coeffs.items())
        # Modulus 96 removes only the p=2 Euler factor of chi_{-3}.
        correction = R(2).log()/2 if order == 3 else R(0)
        logder = common_R+correction
        conductors = sorted(c['conductor'] for c in chars)
        expected = [3, 24, 48, 48, 96, 96, 96, 96] if order == 3 else [4, 8, 16, 16, 32, 32, 32, 32]
        assert conductors == expected
        discriminant = ZZ(2)**31*prod(c['conductor'] for c in chars)
        rel_disc = discriminant//ZZ(2)**62
        assert rel_disc == (3**8 if order == 3 else 4)
        h = -logder/8+R(2).log()/16
        if order == 3:
            # Yuan 1.2 / published YZ 1.7, divided by [F:Q]=8.
            h -= R(rel_disc).log()/16
        H = order*h+R(factorial(order)).log()
        records.append({'elliptic_order': order, 'common_modulus': modulus,
                        'primitive_characters': chars, 'conductors': conductors,
                        'CM_field_discriminant': str(discriminant),
                        'relative_discriminant_norm': str(rel_disc),
                        'common_gamma_coefficients': {str(a): str(c) for a, c in coeffs.items()},
                        'Euler_inflation_log_derivative_correction_interval': iv(correction),
                        'finite_L_log_derivative_interval': iv(logder),
                        'absolute_Hodge_height_interval': iv(h),
                        'cotangent_height_upper_interval': iv(H),
                        'CM_formula': 'Yuan_1_2_no_common_ramification' if order == 3 else 'Zhao_7_4_common_dyadic_ramification_D104_normalization'})
    # Integral higher derivative: test the node derivation without factorial division.
    P = PolynomialRing(QQ, 't'); t = P.gen()
    derivative_controls = []
    for m in (2, 3, 32):
        a = QQ(m)/2*t**(m-1)*(1-t*t)
        for k in range(m-1):
            assert a(0) == 0
            a = (1-t*t)*a.derivative()/2
        assert a(0) == QQ(factorial(m))/2**m
        derivative_controls.append({'order': m, 'D_power_at_zero': str(a(0)), 'archimedean_norm': str(factorial(m))})
    intrinsic = json.loads((DATA/'cm_intrinsic_height_review_d104.json').read_text())
    h2_plus = R(QQ(intrinsic['independent_analytic']['Hodge_height_interval'][1]))
    H2 = 2*h2_plus-QQ(35)/34*R(2).log()
    def ball(pair):
        a, b = map(QQ, pair)
        return R((a+b)/2, (b-a)/2)
    H3, H32 = [ball(x['cotangent_height_upper_interval']) for x in records]
    psi = QQ(51)/4*H2+8*H3+QQ(1023)/1024*H32
    prior = json.loads((DATA/'P1600_height_routes_audit_d142.json').read_text())
    residual = ball(prior['residual_needed_for_Faltings_29_interval'])
    result = {'status': 'pass', 'milestone': 'D143', 'arb_precision_bits': 192,
              'CM_heights': records, 'higher_derivative_controls': derivative_controls,
              'H2_upper_interval': iv(H2), 'total_elliptic_cotangent_upper_interval': iv(psi),
              'sufficient_model_intersection_spectral_target_interval': iv(residual+psi),
              'target_formula': 'E_model - I - 6 average(log(C_corrected Zprime(1))) >= target_upper',
              'dyadic_only_model_comparison_support': True, 'good_reduction_away_from_2': True,
              'E_model_computed': False, 'E_model_sign_proved': False,
              'Faltings_lower_29_proved': False, 'height_bound_at_most_623_proved': False,
              'candidate_identification_proved': False, 'corrected_global_RR_constant_certified': False,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D143_ELLIPTIC_HEIGHT_WORKER_PASS', flush=True)


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', type=Path)
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
        sys.exit(0)
    start = time.monotonic()
    output = DATA/'P1600_elliptic_heights_d143.json'
    child_path = DATA/'P1600_elliptic_heights_d143_worker.json'
    assert not output.exists() and not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH', '')
    child = subprocess.run([str(PYTHON), str(Path(__file__).resolve()), '--worker', str(child_path)], cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D143_ELLIPTIC_HEIGHT_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    result = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    child_rss = max(result['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform == 'darwin' else 1024))
    assert rss+child_rss < 2*(1 << 30)
    result.update({'wall_seconds': time.monotonic()-start, 'peak_rss_bytes': rss,
                   'child_peak_rss_bytes': child_rss, 'conservative_peak_rss_bytes': rss+child_rss,
                   'sources': [source(p) for p in [Path(__file__), PYTHON, child_path,
                       DATA/'cm_intrinsic_height_review_d104.json', DATA/'P1600_height_routes_audit_d142.json']]})
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)), flush=True)
    print('PASS|601_P1600_ELLIPTIC_HEIGHTS', flush=True)
