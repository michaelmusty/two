"""High-precision reconstruction in the fixed arithmetic monomial gauge.

Uses Sage's FLINT complex-ball polynomials and linear algebra. Balls bound
arithmetic on supplied values, not geometric or truncation errors. The
short formal gauge is computed with extra mpmath guard digits.
"""
import argparse
import hashlib
import importlib.util
from itertools import combinations_with_replacement
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import qr
from sage.all import ComplexBallField, RealBallField, PolynomialRing, matrix

HERE = Path(__file__).resolve().parent
DATA = HERE.parent/'data/computed'
spec = importlib.util.spec_from_file_location('precise_arithmetic', HERE/'85_arithmetic_quadrics.py')
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)


def read_source(path, length, digits):
    metadata = json.loads(path.with_suffix('.json').read_text())
    if path.suffix == '.acb':
        native_spec = importlib.util.spec_from_file_location('quadric_native', HERE/'cm_acb.py')
        native = importlib.util.module_from_spec(native_spec)
        native_spec.loader.exec_module(native)
        backend = native.Backend(digits)
        values = backend.read(path, metadata['n'], metadata['columns'])
        source = values.to_mpmath(rows=length)
        precision = f"native checkpoint at {metadata['decimal_digits']} working decimal digits"
    elif path.suffix == '.npz':
        with np.load(path) as bank:
            source = mp.matrix(bank['coefficients'][:length].tolist())
        precision = 'double source; extra arithmetic does not add input accuracy'
    else:
        raise ValueError('expected an acb checkpoint or npz bank')
    if source.rows != length or source.cols != 16:
        raise ValueError('a sufficiently long 16-column base bank is required')
    return source, {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'radius': metadata['radius'], 'precision': precision}


def midpoint(z):
    return [str(z.real().mid()), str(z.imag().mid())]


def decode(rows):
    return mp.matrix([[mp.mpc(*pair) for pair in row] for row in rows])


def float_matrix(values):
    return np.array([[complex(z.mid()) for z in row] for row in values.rows()])


def absolute_upper(values):
    return max(float(abs(z).upper()) for z in values.list())


def solve_relations(full, pivots, free, training, fit_rows=None):
    """Interpolation rows are separate from the later validation rows."""
    numeric = float_matrix(full[:training, :])
    if fit_rows is None:
        columns = numeric[:, pivots]
        columns /= np.linalg.norm(columns, axis=0)
        _, _, order = qr(columns.T, mode='economic', pivoting=True)
        fit_rows = sorted(int(i) for i in order[:len(pivots)])
    if len(fit_rows) != len(pivots) or len(set(fit_rows)) != len(pivots):
        raise ValueError('one distinct interpolation row per pivot is required')
    if min(fit_rows) < 0 or max(fit_rows) >= training:
        raise ValueError('interpolation rows must precede validation rows')
    lhs = full.matrix_from_rows_and_columns(fit_rows, pivots)
    rhs = full.matrix_from_rows_and_columns(fit_rows, free)
    fitted = lhs.solve_right(rhs)
    residual = full.matrix_from_columns(free)-full.matrix_from_columns(pivots)*fitted
    if not all(z.real().is_finite() and z.imag().is_finite() for z in fitted.list()+residual.list()):
        raise ArithmeticError('nonfinite solve; increase arithmetic precision or change interpolation rows')
    unused = [i for i in range(training) if i not in fit_rows]
    held = residual[training:, :]
    scale = absolute_upper(full)*max(1, absolute_upper(fitted))*max(1, len(pivots))
    condition = float(np.linalg.cond(float_matrix(lhs)))
    details = {'interpolation_rows': fit_rows,
               'interpolation_matrix_condition_double': condition if np.isfinite(condition) else None,
               'unused_training_rows': len(unused), 'held_out_rows': full.nrows()-training,
               'unused_training_absolute_residual_bound': absolute_upper(residual.matrix_from_rows(unused)),
               'held_out_absolute_residual_bound': absolute_upper(held),
               'held_out_scaled_residual_bound': absolute_upper(held)/scale,
               'residual_scaling': 'max|products| * max(1,max|fitted coefficients|) * pivot count'}
    return -fitted, details


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, required=True)
    parser.add_argument('--normalization', type=Path, default=DATA/'arithmetic_quadrics_10240.json')
    parser.add_argument('--comparison', type=Path, help='earlier precise-quadric JSON with the same monomials')
    parser.add_argument('--rows-from', type=Path, help='reuse interpolation rows from an earlier precise report')
    parser.add_argument('--length', type=int, default=512)
    parser.add_argument('--training', type=int, default=256)
    parser.add_argument('--digits', type=int, default=50)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 61 <= args.training < args.length or args.digits < 25:
        parser.error('require 61 <= training < length and at least 25 working digits')
    started = time.monotonic()
    mp.mp.dps = args.digits+25
    source, provenance = read_source(args.basis, args.length, args.digits)
    change, short, gauge = arithmetic.arithmetic_change(source.tolist(), list(range(16)),
                                                       [(16, 14, -1), (16, 13, 1)])
    bits = int(mp.ceil(args.digits*mp.log(10, 2)))+32
    field, reals = ComplexBallField(bits), RealBallField(bits)
    def ball(z):
        return field(reals(mp.nstr(z.real, args.digits+15)), reals(mp.nstr(z.imag, args.digits+15)))
    rows = matrix(field, [[ball(z) for z in row] for row in source.tolist()])
    transformed = rows*matrix(field, [[ball(z) for z in row] for row in change.tolist()])
    ring = PolynomialRing(field, 'u')
    forms = [ring(transformed.column(i).list()) for i in range(16)]
    pairs = list(combinations_with_replacement(range(16), 2))
    polynomials = [(forms[i]*forms[j]).truncate(args.length) for i, j in pairs]
    full = matrix(field, [[p[n] for p in polynomials] for n in range(args.length)])
    fixed = json.loads(args.normalization.read_text())['current']
    pivots, free = fixed['fixed_pivot_monomials'], fixed['free_monomials']
    fit_rows = json.loads(args.rows_from.read_text())['solve']['interpolation_rows'] if args.rows_from else None
    coefficients, solve = solve_relations(full, pivots, free, args.training, fit_rows)
    values = [[midpoint(z) for z in row] for row in coefficients.rows()]
    current = decode(values)
    report = {'status': 'high-precision numerical arithmetic quadrics; not exact algebraic equations',
              'source': provenance, 'working_decimal_digits': args.digits, 'ball_working_bits': bits,
              'arithmetic_gauge': gauge, 'solve': solve,
              'pivots': pivots, 'free': free, 'monomial_pairs': pairs,
              'pivot_coefficients': values,
              'imaginary_relative_norm': mp.nstr(mp.sqrt(mp.fsum(z.imag**2 for z in current))/mp.norm(current), 16),
              'arithmetic_recognition_attempted': False,
              'limitations': ['short formal gauge uses mpmath guard digits',
                             'balls enclose arithmetic on supplied values, not exact geometry or infinite-series tails',
                             'marked point, differential space, flag and nonzero scale must still be certified']}
    if args.comparison:
        old_report = json.loads(args.comparison.read_text())
        if old_report['pivots'] != pivots or old_report['free'] != free:
            raise ValueError('comparison uses different normalized equations')
        previous = decode(old_report['pivot_coefficients'])
        report['comparison'] = {'path': str(args.comparison),
                                'relative_difference': mp.nstr(mp.norm(current-previous)/mp.norm(current), 16),
                                'max_absolute_difference': mp.nstr(max(map(abs, current-previous)), 16)}
    report['wall_seconds'] = time.monotonic()-started
    text = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(text)
    args.output.with_suffix('.out').write_text(text)
    print(report['status'])
    print('imaginary relative norm:', report['imaginary_relative_norm'])
    print('held-out scaled residual:', solve['held_out_scaled_residual_bound'])
    if 'comparison' in report:
        print('comparison:', report['comparison'])


if __name__ == '__main__':
    main()
