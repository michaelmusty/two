"""D140 exact lattice comparison after candidate-free discovery and holdout.

This is the first D140 discovery-chain stage that reads the old candidate.
It compares the two independently recognized bases and the candidate by
exact integer changes of basis. Sage runs inside the existing capped group.
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
DATA = ROOT / 'dembele/data/computed'
SAGE_BASE = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/Current')
SAGE_PYTHON = SAGE_BASE / 'venv/bin/python3'


def source(path):
    path = Path(path).resolve()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            h.update(raw)
    return {'path': str(path), 'sha256': h.hexdigest()}


def worker(input_path, output_path):
    from sage.all import QQ, ZZ, matrix
    packet = json.loads(Path(input_path).read_text())
    first, second, old = [matrix(ZZ, packet[k]) for k in ('recognized96', 'recognized160', 'candidate')]
    pivots = first.change_ring(QQ).pivots()
    assert len(pivots) == 91
    inverse = first.matrix_from_columns(pivots).change_ring(QQ).inverse()
    transforms = {}
    for label, target in [('recognized160', second), ('candidate', old)]:
        change = target.matrix_from_columns(pivots) * inverse
        assert change * first == target
        assert all(x.denominator() == 1 for row in change for x in row)
        integer_change = change.change_ring(ZZ)
        determinant = int(integer_change.det())
        assert abs(determinant) == 1
        transforms[label] = {'rows': [[int(x) for x in row] for row in integer_change],
                             'determinant': determinant}
    basis_certificates = []
    for record in packet['lll_records']:
        initial = matrix(ZZ, record['initial_basis'])
        transform = matrix(ZZ, record['transform'])
        reduced = matrix(ZZ, record['reduced_basis'])
        assert transform * initial == reduced
        determinant = int(transform.det())
        assert abs(determinant) == 1
        assert abs(initial.det()) == 2 ** (record['bits'] * 45)
        basis_certificates.append({'bits': record['bits'], 'transform_determinant': determinant,
                                   'full_basis_dimension': 136, 'transformation_identity_checked': True})
    result = {'status': 'pass', 'recognized_rank': 91, 'pivot_columns': list(pivots),
              'integer_changes_of_basis': transforms, 'congruence_lattice_certificates': basis_certificates,
              'same_saturated_integer_lattice_as_candidate': True,
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)}
    assert result['peak_rss_bytes'] < 2 * (1 << 30)
    with Path(output_path).open('x') as f:
        f.write(json.dumps(result, indent=2) + '\n')
    print('D140_LATTICE_COMPARISON_WORKER_PASS', flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    paths = {Path(__file__), SAGE_PYTHON}
    def read(name):
        path = DATA / (name + '.json')
        paths.add(path)
        value = json.loads(path.read_text())
        assert value['status'] == 'pass'
        return value
    holdout = read('dyadic_P1600_recognition_holdout96_d140')
    assert holdout['all_recovered_relations_compatible'] and not holdout['candidate_equations_read']
    recognized = [read(f'dyadic_P1600_lattice{bits}_r3_d140') for bits in (96, 160)]
    for packet in recognized:
        assert not packet['candidate_equations_read']
        assert packet['all_proposed_relations_pass_higher_training_digits']
    candidate = read('cm_frame_curve_candidate')
    assert candidate['saturated_integer_quadric_lattice']
    assert all(r['monomial_pairs'] == candidate['monomial_pairs'] for r in recognized)
    lll = []
    for record in recognized:
        for ref in (record['lattice_input'], record['lattice_output']):
            assert source(ref['path']) == ref
            paths.add(Path(ref['path']))
        initial = json.loads(Path(record['lattice_input']['path']).read_text())
        reduced = json.loads(Path(record['lattice_output']['path']).read_text())
        lll.append({'bits': record['congruence_2_bits'], 'initial_basis': initial['basis'],
                    'reduced_basis': reduced['reduced_basis'], 'transform': reduced['unimodular_transform']})
    input_path = DATA / (args.output + '_input.json')
    child_path = DATA / (args.output + '_worker.json')
    with input_path.open('x') as f:
        f.write(json.dumps({'recognized96': recognized[0]['recognized_integer_vectors'],
                           'recognized160': recognized[1]['recognized_integer_vectors'],
                           'candidate': candidate['quadrics'], 'lll_records': lll}, indent=2) + '\n')
    assert not child_path.exists()
    env = dict(os.environ, DOT_SAGE='/private/tmp/dembele_P1600_recognition_sage')
    env['PATH'] = str(SAGE_BASE / 'local/bin') + ':' + str(SAGE_BASE / 'venv/bin') + ':' + env.get('PATH', '')
    child = subprocess.run([str(SAGE_PYTHON), str(Path(__file__).resolve()), '--worker', str(input_path), str(child_path)],
                           cwd=ROOT, env=env, capture_output=True, text=True)
    assert child.returncode == 0 and 'D140_LATTICE_COMPARISON_WORKER_PASS' in child.stdout, (child.returncode, child.stdout, child.stderr)
    certified = json.loads(child_path.read_text())
    paths.update((input_path, child_path))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    child_rss = max(certified['peak_rss_bytes'], resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * (1 if sys.platform == 'darwin' else 1024))
    assert rss + child_rss < 2 * (1 << 30)
    packet = {'status': 'pass', 'milestone': 'D140', 'certificates': certified,
              'candidate_read_only_after_discovery_and_holdout': True,
              'candidate_inputs_used_in_discovery': False,
              'exact_curve_identification_proved': False, 'field_polynomial_constructed': False,
              'wall_seconds': time.monotonic()-tick, 'peak_rss_bytes': rss, 'child_peak_rss_bytes': child_rss,
              'sources': [source(p) for p in sorted(paths)]}
    with out.open('x') as f:
        f.write(json.dumps(packet, indent=2) + '\n')
    print('D140_EXACT_LATTICE|rank=91; same saturated integer lattice; both training precisions', flush=True)
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|588_DYADIC_P1600_RECOGNIZED_LATTICE_COMPARISON', flush=True)


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--worker':
        worker(sys.argv[2], sys.argv[3])
    else:
        main()
