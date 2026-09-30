"""Bounded search for small equations in the whole canonical quadric space.

The lattice acts on all monomials at once; it need not recognize large
fractions in a row-reduced equation basis. Only one real field embedding
is available. Every numerical hit is tentative, and small embedded units
are rejected by normalizing with embedded coefficient size.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import mpmath as mp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('quadric_lattice_fields', HERE/'87_quadric_recognition.py')
fields = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fields)


def quotient_map(report):
    pivots, free = report['pivots'], report['free']
    result = mp.matrix(len(pivots), len(pivots)+len(free))
    for i, p in enumerate(pivots):
        result[i, p] = 1
        for j, f in enumerate(free):
            result[i, f] = -mp.mpc(*report['pivot_coefficients'][i][j])
    return result


def lattice_tail(quotient, basis, scale_digits):
    scales = [mp.sqrt(mp.fsum(abs(quotient[i, j])**2 for j in range(quotient.cols)))
              for i in range(quotient.rows)]
    scale = mp.mpf(10)**scale_digits
    return [[int(mp.nint(scale*b*quotient[i, j].real/scales[i]))
             for i in range(quotient.rows)]
            for j in range(quotient.cols) for b in basis]


def lll_worker(source, output):
    from sage.all import ZZ, matrix
    data = json.loads(Path(source).read_text())
    tail = data['tail']
    count, constraints = len(tail), len(tail[0])
    lattice = matrix(ZZ, count, count+constraints)
    for i, row in enumerate(tail):
        lattice[i, i] = 1
        for j, z in enumerate(row):
            lattice[i, count+j] = z
    started = time.monotonic()
    reduced = lattice.LLL(delta=0.99, algorithm='fpLLL:wrapper')
    Path(output).write_text(json.dumps({'rows': [[int(z) for z in row[:count]] for row in reduced.rows()],
                                       'lll_seconds': time.monotonic()-started}))


def reduce_tail(tail, timeout):
    with tempfile.TemporaryDirectory(prefix='dembele-quadric-lll-') as directory:
        source, output = Path(directory)/'input.json', Path(directory)/'output.json'
        source.write_text(json.dumps({'tail': tail}))
        try:
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(source), str(output)],
                                 capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, {'status': 'bounded lattice reduction timed out', 'timeout_seconds': timeout}
        if run.returncode:
            raise RuntimeError('lattice worker failed: '+run.stderr[-4000:])
        data = json.loads(output.read_text())
        return data['rows'], {'status': 'lattice reduction completed', 'lll_seconds': data['lll_seconds']}


def relation_residual(quotient, coordinates, basis):
    degree = len(basis)
    coefficients = mp.matrix([mp.fsum(coordinates[j*degree+k]*basis[k] for k in range(degree))
                              for j in range(quotient.cols)])
    size = mp.norm(coefficients)
    if size == 0:
        raise ValueError('zero embedded coefficient vector')
    residual = quotient*coefficients
    # This normalization matters: a small algebraic unit times an arbitrary
    # monomial must not look like a relation merely because its value is tiny.
    return mp.norm(residual)/(mp.norm(quotient)*size)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, required=True, help='script 86 JSON')
    parser.add_argument('--comparison', type=Path, required=True, help='same monomials, distinct interpolation or bank')
    parser.add_argument('--field-degree', type=int, choices=[1, 8], default=8)
    parser.add_argument('--scale-digits', type=int, default=17)
    parser.add_argument('--timeout', type=float, default=180)
    parser.add_argument('--tolerance', default='1e-20')
    parser.add_argument('--max-height', type=int, default=64, help='reject larger integer coefficient vectors as candidates')
    parser.add_argument('--min-weight', type=int, default=0,
                        help='restrict to X_i X_j with i+j at least this value (0..22)')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    mp.mp.dps = 80
    tolerance = mp.mpf(args.tolerance)
    if (not 1 <= args.scale_digits <= 40 or args.timeout <= 0 or not 0 < tolerance < 1
            or args.max_height < 1 or not 0 <= args.min_weight <= 22):
        parser.error('invalid lattice scale, time limit or tolerance')
    started = time.monotonic()
    current, previous = (json.loads(p.read_text()) for p in [args.basis, args.comparison])
    for key in ['pivots', 'free', 'monomial_pairs']:
        if current[key] != previous[key]:
            raise ValueError('incompatible quadric normalizations')
    quotient, older = quotient_map(current), quotient_map(previous)
    indices = [j for j, pair in enumerate(current['monomial_pairs']) if sum(pair) >= args.min_weight]
    if len(current['monomial_pairs']) != 136:
        raise ValueError('this CLI expects the genus-sixteen base')
    quotient = mp.matrix([[quotient[i, j] for j in indices] for i in range(quotient.rows)])
    older = mp.matrix([[older[i, j] for j in indices] for i in range(older.rows)])
    # Riemann--Roch: h0(2K-mP)=45-m for 0<=m<=22. Verify that
    # these monomials numerically span that dimension before reducing rows.
    # ALL 45 quotient constraints still enter candidate validation below.
    import numpy as np
    from scipy.linalg import qr, svdvals
    numeric = np.array(quotient.tolist(), complex)
    singular = svdvals(numeric/np.linalg.norm(numeric, axis=0))
    expected = 45-args.min_weight
    observed = int(sum(singular > singular[0]*1e-12))
    if observed != expected:
        raise ValueError(f'weighted product rank {observed}, expected {expected}')
    if args.min_weight == 0:
        constraint_rows = list(range(45))
    else:
        _, _, order = qr(numeric.T, mode='economic', pivoting=True)
        constraint_rows = [int(i) for i in order[:expected]]
    reduced_quotient = mp.matrix([[quotient[i, j] for j in range(quotient.cols)] for i in constraint_rows])
    basis = next(b for d, b, _ in fields.field_bases('cosine') if d == args.field_degree)
    tail = lattice_tail(reduced_quotient, basis, args.scale_digits)
    reduced, details = reduce_tail(tail, args.timeout)
    report = {'status': 'numerical lattice discovery only; no exact equation certified',
              'source': str(args.basis), 'source_sha256': hashlib.sha256(args.basis.read_bytes()).hexdigest(),
              'comparison': str(args.comparison), 'comparison_sha256': hashlib.sha256(args.comparison.read_bytes()).hexdigest(),
              'field_degree': args.field_degree, 'field_basis': 'cosine integral basis as in script 87',
              'lattice_rows': len(tail), 'lattice_columns': len(tail)+expected,
              'minimum_monomial_weight': args.min_weight, 'selected_monomials': indices,
              'constraint_rows_used_in_lattice': constraint_rows, 'constraints_checked': quotient.rows,
              'weighted_product_rank': observed, 'weighted_quadric_dimension': len(indices)-observed,
              'weighted_product_scaled_singular_values': singular.tolist(),
              'lattice_scale_decimal_digits': args.scale_digits,
              'candidate_integer_height_bound': args.max_height,
              'empirical_relative_tolerance': str(tolerance), 'worker': details,
              'residual_metric': 'norm(D*c)/(norm(D)*norm(c)) at the given field embedding',
              'monomial_pairs': [current['monomial_pairs'][j] for j in indices], 'best_rows': [], 'candidate_count': 0}
    if reduced is not None:
        scores = []
        for i, row in enumerate(reduced):
            error = relation_residual(quotient, row, basis)
            scores.append((error, i))
        scores.sort()
        for error, i in scores:
            if len(report['best_rows']) >= 20 and error >= tolerance:
                break
            independent = relation_residual(older, reduced[i], basis)
            height = max(map(abs, reduced[i]))
            accepted = error < tolerance and independent < tolerance and height <= args.max_height
            report['candidate_count'] += int(accepted)
            report['best_rows'].append({'lll_row': i, 'relative_residual': mp.nstr(error, 20),
                                        'comparison_relative_residual': mp.nstr(independent, 20),
                                        'integer_height': height,
                                        'numerical_candidate': accepted,
                                        'integer_coordinates': reduced[i]})
    report['wall_seconds'] = time.monotonic()-started
    output = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(output)
    args.output.with_suffix('.out').write_text(output)
    print(details)
    print('Numerical candidate count:', report['candidate_count'])
    if report['best_rows']:
        print('Best residual:', report['best_rows'][0]['relative_residual'])


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--worker':
        lll_worker(sys.argv[2], sys.argv[3])
    else:
        main()
