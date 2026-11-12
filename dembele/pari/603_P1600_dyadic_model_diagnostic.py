"""D143: dyadic generic-component differents and graph comparison diagnostic.

Uses only the certified 164 stabilizers and 58 old local frames. Degree
identities test the proposed geometric interpretation independently of energy.
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
    from sage.all import QQ, NumberField, PolynomialRing, matrix, vector, identity_matrix, RealBallField
    P = PolynomialRing(QQ, 'x'); x = P.gen()
    F = NumberField(x**8-8*x**6+20*x**4-16*x*x+2, 'b')
    f = lambda row: F([QQ(c) for c in row])
    mat = lambda row: matrix(F, 2, 2, [f(c) for c in row])
    def val(c):
        return min((8*a.valuation(2)+i for i, a in enumerate(F(c).list()) if a), default=10**9)
    def mv(A):
        return min(map(val, A.list()))
    raw = json.loads((DATA/'dyadic_quotient_export_d111.json').read_text())
    frames = json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    split = json.loads((DATA/'definite_dyadic_certificate_d109.json').read_text())
    E = identity_matrix(F, 2)
    I, Jc, Jt = [mat(split[k]) for k in ('I_exact', 'J_constant', 'J_slope')]
    x0 = f(split['Hensel']['x0']); error = split['Hensel']['root_error_valuation']
    def image(q):
        slope = q[2]*Jt+q[3]*(I*Jt)
        return q[0]*E+q[1]*I+q[2]*Jc+q[3]*(I*Jc)+x0*slope, slope
    def mul(q, r):
        a,b,c,d = q; A,B,C,D = r
        return vector(F,[a*A-b*B-c*C-d*D,a*B+b*A+c*D-d*C,a*C+c*A+d*B-b*D,a*D+d*A+b*C-c*B])
    def projective_order(q):
        a = vector(F, [1,0,0,0])
        for k in range(1, 65):
            a = mul(a,q)
            if a[1] == a[2] == a[3] == 0:
                return k
        raise AssertionError('projective order exceeds 64')
    rows = []
    # The saved certificate names its local-frame records ideal_checks.
    checks = frames['ideal_checks']
    for j, item in enumerate(raw['ideals']):
        L = mat(checks[j]['local_frame']); Li = L.inverse()
        terms = []; n3_elements = 0
        for k, packed in enumerate(item['stabilizer_units']):
            q = vector(F, [f(c) for c in packed])
            order = projective_order(q)
            n3_elements += int(order == 3)
            if order == 1:
                continue
            A, S = image(q); A = Li*A*L; S = Li*S*L
            assert mv(A) >= 0 and val(A.det()) == 0
            lower = error+mv(S)
            a,b,c,d = A.list()
            level = min(val(b), val(c), val(a-d))
            assert 0 <= level < lower
            terms.append({'stabilizer_index': k, 'projective_order': order,
                          'difference_valuation_b': int(level), 'certified_error_lower': int(lower)})
        size = raw['stabilizers'][j]
        assert len(terms) == size-1
        n3 = QQ(3*n3_elements)/size
        assert n3.denominator() == 1
        n2 = 1 if j == 4 else (2 if j >= 50 else 0)
        n32 = int(j == 4)
        marks = QQ(n2)/2+QQ(2*n3)/3+QQ(31*n32)/32
        rows.append({'class_one_based': j+1, 'stabilizer_order': size,
                     'different_coefficient': sum(t['difference_valuation_b'] for t in terms),
                     'order3_points': int(n3), 'order2_points': n2, 'order32_points': n32,
                     'orbifold_mark_weight': str(marks), 'local_terms': terms})
    assert sum(r['order3_points'] for r in rows) == 9
    edges = []
    for i in range(58):
        for j in range(i+1, 58):
            if raw['matrix'][i][j]:
                assert min(raw['matrix'][i][j],raw['matrix'][j][i]) == 1
                length = QQ(raw['stabilizers'][i])/raw['matrix'][j][i]
                assert length.denominator() == 1
                edges.append([i+1,j+1,int(length)])
    assert len(edges) == 73
    ds = [r['different_coefficient'] for r in rows]
    ldeg = [QQ(1)/r['stabilizer_order'] for r in rows]
    wdeg = [-2+QQ(r['orbifold_mark_weight']) for r in rows]
    Ddeg = [QQ(0)]*58
    energy = QQ(0)
    for a,b,length in edges:
        wdeg[a-1] += 1; wdeg[b-1] += 1
        gap = ds[b-1]-ds[a-1]
        Ddeg[a-1] += QQ(gap)/length
        Ddeg[b-1] -= QQ(gap)/length
        energy += QQ(gap*gap)/length
    defects = [ldeg[j]-wdeg[j]-Ddeg[j] for j in range(58)]
    coarse_correction = -2*sum(ldeg[j]*ds[j] for j in range(58))-energy
    live = set(range(1,59)); remain = edges[:]
    mark = {r['class_one_based']: QQ(r['orbifold_mark_weight']) for r in rows}
    tail_energy = QQ(0); contractions = []
    while True:
        neighbors = {v: [] for v in live}
        for a,b,length in remain:
            neighbors[a].append((b,length)); neighbors[b].append((a,length))
        leaves = [v for v in sorted(live) if len(neighbors[v]) == 1]
        if not leaves:
            break
        v = leaves[0]; u,length = neighbors[v][0]
        step = length*(1-mark[v])**2
        contractions.append({'contracted': v, 'onto': u, 'length': length,
                             'mark_weight_carried': str(mark[v]), 'energy': str(step)})
        tail_energy += step; mark[u] += mark[v]
        live.remove(v); remain = [e for e in remain if v not in e[:2]]
    total = coarse_correction+tail_energy
    R = RealBallField(192); value = R(total)*R(2).log()/8
    result = {'status': 'pass', 'milestone': 'D143', 'components': rows, 'noninverted_edges': edges,
              'component_degree_defects': list(map(str, defects)),
              'all_component_degree_identities_hold': all(d == 0 for d in defects),
              'Hodge_degree': str(sum(ldeg)), 'orbifold_degree': str(sum(wdeg)),
              'different_graph_energy': str(energy),
              'coarse_model_correction_coefficient_b': str(coarse_correction),
              'tail_contractions': contractions, 'tail_correction_coefficient_b': str(tail_energy),
              'minimal_regular_model_correction_coefficient_b': str(total),
              'E_model_candidate_interval': [str(QQ(value.lower())), str(QQ(value.upper()))],
              'display_E_model_candidate': float(value.center()),
              'geometric_interpretation_requires_companion_proof': True,
              'Faltings_lower_29_proved': False, 'candidate_identification_proved': False,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2*(1 << 30)
    with out.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('D143_DYADIC_MODEL_WORKER_PASS', flush=True)


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', type=Path)
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
        sys.exit(0)
    start = time.monotonic()
    output = DATA/'P1600_dyadic_model_diagnostic_d143.json'
    child_path = DATA/'P1600_dyadic_model_diagnostic_d143_worker.json'
    assert not output.exists() and not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE/'local/bin')+':'+str(SAGE/'venv/bin')+':'+env.get('PATH', '')
    child = subprocess.run([str(PYTHON), str(Path(__file__).resolve()), '--worker', str(child_path)], cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D143_DYADIC_MODEL_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    result = json.loads(child_path.read_text())
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    child_rss = max(result['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*(1 if sys.platform == 'darwin' else 1024))
    assert rss+child_rss < 2*(1 << 30)
    result.update({'wall_seconds': time.monotonic()-start, 'peak_rss_bytes': rss,
                   'child_peak_rss_bytes': child_rss, 'conservative_peak_rss_bytes': rss+child_rss,
                   'sources': [source(p) for p in [Path(__file__), PYTHON, child_path,
                       DATA/'dyadic_quotient_export_d111.json', DATA/'dyadic_harmonic_certificate_d111.json',
                       DATA/'definite_dyadic_certificate_d109.json']]})
    with output.open('x') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print('DYADIC_MODEL_DIAGNOSTIC|'+json.dumps({k: result[k] for k in ('all_component_degree_identities_hold', 'different_graph_energy', 'coarse_model_correction_coefficient_b', 'tail_correction_coefficient_b', 'minimal_regular_model_correction_coefficient_b', 'display_E_model_candidate')}), flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)), flush=True)
    print('PASS|603_P1600_DYADIC_MODEL_DIAGNOSTIC', flush=True)
