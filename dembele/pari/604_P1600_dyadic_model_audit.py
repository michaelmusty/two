"""D143: reconstruct the model correction from multidegrees and one local unit.

Independent of the diagnostic's matrix-different evaluation: solve the exact
weighted graph Laplacian, anchor at the trivial-stabilizer component 58,
and contract rational tails in the opposite order.
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
    from sage.all import QQ, matrix, vector, PolynomialRing, NumberField, RealBallField
    raw = json.loads((DATA/'dyadic_quotient_export_d111.json').read_text())
    diag = json.loads((DATA/'P1600_dyadic_model_diagnostic_d143.json').read_text())
    P = PolynomialRing(QQ, 'x'); x = P.gen()
    F = NumberField(x**8-8*x**6+20*x**4-16*x*x+2, 'b')
    sizes = raw['stabilizers']
    assert sizes[57] == 1
    n3 = []
    for j, row in enumerate(raw['ideals']):
        # For norm-one quaternion q, projective order 3 iff trace(q)^2=1.
        count = sum(4*F([QQ(c) for c in q[0]])**2 == 1 for q in row['stabilizer_units'])
        value = QQ(3*count)/sizes[j]
        assert value.denominator() == 1
        n3.append(value)
    assert n3 == [r['order3_points'] for r in diag['components']] and sum(n3) == 9
    marks = vector(QQ, [QQ(2)*n/3 for n in n3])
    marks[4] += QQ(1)/2+QQ(31)/32
    for j in range(50, 58):
        marks[j] += 1
    edges = []
    N = matrix(QQ, 58)
    degrees = [0]*58
    for i in range(58):
        for j in range(i+1,58):
            if raw['matrix'][j][i]:
                length = QQ(sizes[j])/raw['matrix'][i][j]
                assert length.denominator() == 1
                edges.append((i,j,length))
                N[i,j] += 1/length; N[j,i] += 1/length
                N[i,i] -= 1/length; N[j,j] -= 1/length
                degrees[i] += 1; degrees[j] += 1
    hdeg = vector(QQ, [QQ(1)/e for e in sizes])
    wdeg = vector(QQ, [d-2 for d in degrees])+marks
    assert sum(hdeg) == sum(wdeg) == QQ(1455)/32
    rhs = hdeg-wdeg
    A = N.matrix_from_rows_and_columns(list(range(57)), list(range(57)))
    D = vector(QQ, list(A.solve_right(vector(QQ, list(rhs)[:57])))+[0])
    assert N*D == rhs
    assert all(d.denominator() == 1 for d in D)
    assert list(D) == [r['different_coefficient'] for r in diag['components']]
    coarse = D*N*D-2*hdeg.dot_product(D)
    assert coarse == -QQ(153)/4
    # Descending labels give a different contraction order from source 603.
    alive = set(range(58)); weights = dict(enumerate(marks)); remaining = edges[:]
    correction = QQ(0); contraction = []
    while True:
        incidence = {j: [] for j in alive}
        for a,b,length in remaining:
            incidence[a].append((b,length)); incidence[b].append((a,length))
        leaf = next((j for j in sorted(alive, reverse=True) if len(incidence[j]) == 1), None)
        if leaf is None:
            break
        onto, length = incidence[leaf][0]
        step = length*(weights[leaf]-1)**2
        correction += step
        contraction.append([leaf+1,onto+1,str(length),str(weights[leaf]),str(step)])
        weights[onto] += weights[leaf]
        alive.remove(leaf)
        remaining = [e for e in remaining if leaf not in e[:2]]
    assert len(alive) == 49 and len(remaining) == 64
    assert correction == QQ(16955)/768
    total = coarse+correction
    assert total == -QQ(12421)/768
    R = RealBallField(224)
    def ball(pair):
        a,b = map(QQ,pair)
        return R((a+b)/2,(b-a)/2)
    iv = lambda t: [str(QQ(t.lower())), str(QQ(t.upper()))]
    model = R(total)*R(2).log()/8
    assert model.overlaps(ball(diag['E_model_candidate_interval']))
    previous = json.loads((DATA/'P1600_height_routes_audit_d142.json').read_text())
    heights = json.loads((DATA/'P1600_elliptic_height_audit_d143.json').read_text())
    target = 348-ball(previous['RR_main_term_in_12F_interval'])-model+ball(heights['total_cotangent_upper_interval'])
    ceiling = QQ((1000*target.upper()).ceil())/1000
    assert target < ceiling
    # Conditional RR requirement with all finite model terms now explicit.
    spectral = -target/6
    main = ball(previous['RR_main_term_in_12F_interval'])+model
    result = {'status': 'pass', 'milestone': 'D143', 'arb_precision_bits': 224,
              'independent_grounded_Laplacian_solution': list(map(str,D)),
              'order3_points_by_component': list(map(int,n3)),
              'independent_tail_contractions': contraction,
              'coarse_correction_coefficient_b': str(coarse), 'tail_correction_coefficient_b': str(correction),
              'minimal_regular_model_correction_coefficient_b': str(total),
              'E_model_coefficient_log2': str(total/8), 'E_model_interval': iv(model),
              'E_model_computed': True, 'E_model_sign_proved': True,
              'good_reduction_away_from_2': True, 'delta_other': 0,
              'RR_main_term_after_model_interval': iv(main),
              'sufficient_I_plus_spectral_upper_target_interval': iv(-target),
              'safe_sufficient_negative_target': str(-ceiling),
              'equivalent_sufficient_log_CZ_plus_I_over6_upper': str(-ceiling/6),
              'display_E_model': float(model.center()),
              'display_negative_target': float(-ceiling),
              'geometric_claims_require_companion_proof': True,
              'corrected_global_RR_constant_certified': False,
              'Faltings_lower_29_proved': False, 'candidate_identification_proved': False,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D143_DYADIC_MODEL_AUDIT_WORKER_PASS', flush=True)


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', type=Path)
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
        sys.exit(0)
    start = time.monotonic()
    output = DATA/'P1600_dyadic_model_audit_d143.json'
    child_path = DATA/'P1600_dyadic_model_audit_d143_worker.json'
    assert not output.exists() and not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH', '')
    child = subprocess.run([str(PYTHON), str(Path(__file__).resolve()), '--worker', str(child_path)], cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D143_DYADIC_MODEL_AUDIT_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    result = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    child_rss = max(result['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform == 'darwin' else 1024))
    assert rss+child_rss < 2*(1 << 30)
    result.update({'wall_seconds': time.monotonic()-start, 'peak_rss_bytes': rss,
                   'child_peak_rss_bytes': child_rss, 'conservative_peak_rss_bytes': rss+child_rss,
                   'sources': [source(p) for p in [Path(__file__), PYTHON, child_path,
                       DATA/'dyadic_quotient_export_d111.json', DATA/'P1600_dyadic_model_diagnostic_d143.json',
                       DATA/'P1600_height_routes_audit_d142.json', DATA/'P1600_elliptic_height_audit_d143.json']]})
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('DYADIC_MODEL_AUDIT|'+json.dumps({k: result[k] for k in ('E_model_coefficient_log2', 'display_E_model', 'safe_sufficient_negative_target', 'equivalent_sufficient_log_CZ_plus_I_over6_upper')}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)), flush=True)
    print('PASS|604_P1600_DYADIC_MODEL_AUDIT', flush=True)
