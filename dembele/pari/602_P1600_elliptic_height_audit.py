"""D143: independent primitive-character, discriminant and jet audit."""
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
    from sage.all import (RealBallField, ComplexBallField, CyclotomicField,
                          DirichletGroup, QQ, NumberField, PowerSeriesRing, factorial)
    R, C = RealBallField(224), ComplexBallField(224)
    iv = lambda x: [str(QQ(x.lower())), str(QQ(x.upper()))]
    def ball(pair):
        a, b = map(QQ, pair)
        return R((a+b)/2, (b-a)/2)
    old = json.loads((DATA/'P1600_elliptic_heights_d143.json').read_text())
    fields = []
    Z = CyclotomicField(96); z = Z.gen()
    generator = z**3+z**(-3)+z**32-z**(-32)
    poly = generator.minpoly()
    assert poly.degree() == 16
    E3 = NumberField(poly, 'a')
    disc3 = E3.discriminant()
    disc32 = CyclotomicField(32).discriminant()
    assert disc3 == 2**62*3**8 and disc32 == 2**64
    for row in old['CM_heights']:
        m = row['elliptic_order']; q = row['common_modulus']
        chars = [chi for chi in DirichletGroup(q, CyclotomicField(8))
                 if chi(-1) == -1 and (m == 32 or chi(31) == 1)]
        assert len(chars) == 8
        total = C(0)
        conductors = []
        for chi in chars:
            primitive = chi.primitive_character()
            f = primitive.modulus()
            assert f == chi.conductor()
            conductors.append(int(f))
            A = -primitive.bernoulli(1)
            assert A != 0
            assert A == -sum(a*primitive(a) for a in range(1, f))/f
            value = -C(R(f).log())
            for a in range(1, f):
                value += C(primitive(a)/A)*R(QQ(a)/f).log_gamma()
            total += value
        assert total.imag().contains_zero()
        logder = total.real()
        assert sorted(conductors) == row['conductors']
        assert logder.overlaps(ball(row['finite_L_log_derivative_interval']))
        if m == 3:
            h = (-logder+(R(2).log()-8*R(3).log())/2)/8
        else:
            # Colmez -> twice nearby height -> singleton Zhao 7.4.
            average = -logder/2-(31*R(2).log()+R(4).log())/4
            nearby = (average+31*R(2).log()/4)/4
            h = nearby+R(8).log()/16
        H = m*h+sum(R(j).log() for j in range(1, m+1))
        assert h.overlaps(ball(row['absolute_Hodge_height_interval']))
        assert H.overlaps(ball(row['cotangent_height_upper_interval']))
        fields.append({'elliptic_order': m, 'field_discriminant': str(disc3 if m == 3 else disc32),
                       'primitive_conductors': sorted(conductors), 'L_log_derivative_interval': iv(logder),
                       'Hodge_height_interval': iv(h), 'cotangent_upper_interval': iv(H),
                       'display_Hodge_height': float(h.center()), 'display_cotangent_upper': float(H.center())})
    # Change both frames before repeated differentiation, using truncated series.
    P = PowerSeriesRing(QQ, 't', default_prec=36); t = P.gen()
    controls = []
    for m in (2, 3, 32):
        g = 1+t+2*t*t
        a = m*t**(m-1)*(3+t**m)/g
        for k in range(m-1):
            assert a[0] == 0
            a = a.derivative()/g
        assert a[0] == 3*factorial(m)
        controls.append({'order': m, 'changed_frame_coefficient': str(a[0])})
    H2 = ball(old['H2_upper_interval'])
    H3, H32 = [ball(f['cotangent_upper_interval']) for f in fields]
    psi = QQ(51)/4*H2+8*H3+QQ(1023)/1024*H32
    assert psi.overlaps(ball(old['total_elliptic_cotangent_upper_interval']))
    previous = json.loads((DATA/'P1600_height_routes_audit_d142.json').read_text())
    target = 348-ball(previous['RR_main_term_in_12F_interval'])+psi
    assert target.overlaps(ball(old['sufficient_model_intersection_spectral_target_interval']))
    # Conservative three-decimal upper enclosures, checked by balls.
    ceilings = [(1000*x.upper()).ceil()/QQ(1000) for x in (H3, H32, psi, target)]
    assert all(x < q for x, q in zip((H3, H32, psi, target), ceilings))
    result = {'status': 'pass', 'milestone': 'D143', 'arb_precision_bits': 224,
              'independent_primitive_character_construction': True,
              'independent_number_field_discriminants': True,
              'E3_generator_minpoly': str(poly), 'CM_fields': fields,
              'changed_frame_jet_controls': controls,
              'total_cotangent_upper_interval': iv(psi), 'sufficient_remaining_target_interval': iv(target),
              'strict_upper_bounds': dict(zip(('H3', 'H32', 'Psi', 'remaining_target'), map(str, ceilings))),
              'display_total_cotangent_upper': float(psi.center()),
              'display_remaining_target_upper': float(target.upper()),
              'E_model_computed': False, 'E_model_sign_proved': False,
              'Faltings_lower_29_proved': False, 'candidate_identification_proved': False,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D143_ELLIPTIC_HEIGHT_AUDIT_WORKER_PASS', flush=True)


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', type=Path)
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
        sys.exit(0)
    start = time.monotonic()
    output = DATA/'P1600_elliptic_height_audit_d143.json'
    child_path = DATA/'P1600_elliptic_height_audit_d143_worker.json'
    assert not output.exists() and not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH', '')
    child = subprocess.run([str(PYTHON), str(Path(__file__).resolve()), '--worker', str(child_path)], cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D143_ELLIPTIC_HEIGHT_AUDIT_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    result = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    child_rss = max(result['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform == 'darwin' else 1024))
    assert rss+child_rss < 2*(1 << 30)
    result.update({'wall_seconds': time.monotonic()-start, 'peak_rss_bytes': rss,
                   'child_peak_rss_bytes': child_rss, 'conservative_peak_rss_bytes': rss+child_rss,
                   'sources': [source(p) for p in [Path(__file__), PYTHON, child_path,
                       DATA/'P1600_elliptic_heights_d143.json', DATA/'P1600_height_routes_audit_d142.json']]})
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('ELLIPTIC_HEIGHTS|'+json.dumps({'points': [{k: row[k] for k in ('elliptic_order', 'display_Hodge_height', 'display_cotangent_upper')} for row in result['CM_fields']], 'strict_upper_bounds': result['strict_upper_bounds']}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)), flush=True)
    print('PASS|602_P1600_ELLIPTIC_HEIGHT_AUDIT', flush=True)
