"""Compiled high-precision residuals with one reusable double LU factorization.

Solves the finite stabilized system. Independent quadrature and all-side
checks measure its discrepancy from automorphic differentials; they are
diagnostics, not a rigorous truncation bound or an algebraic model.
"""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import lu_factor, lu_solve

from cm_acb import Backend, CauchyOperator, evaluate, weighted_difference

pilot = importlib.import_module('68_cm_differentials')
reference = importlib.import_module('78_mixed_precision_refinement')
DATA = pilot.DATA


def decimal(value):
    return mp.nstr(value, 16)


def relative_bounds(error, reference_values):
    return [decimal(e/r) if r else ('0.0' if not e else 'inf')
            for e, r in zip(error, reference_values)]


def geometry(n, samples, radius, offset, digits):
    points = radius*np.exp(2j*np.pi*(np.arange(samples)+float(offset))/(32*samples))
    words = [[] for _ in points]
    _, _, steps, _ = pilot.reduce_points(points, pilot.load_actions(), words=words)
    nodes, weights, metric_error = pilot.precise_nodes(
        points, words, radius, samples, offset, digits, as_numpy=False)
    stats = {'samples': samples, 'offset': str(offset),
             'metric_relative_error': decimal(metric_error),
             'max_scaled_node_absolute_value': decimal(max(map(abs, nodes))),
             'max_reduction_steps': int(max(steps)),
             'radius_power_32n_not_error_bound': decimal(mp.mpf(str(radius))**(32*n))}
    return nodes, weights, stats


def side_nodes(radius):
    """Same deterministic unused side points as script 70, without double returns."""
    raw = json.loads((DATA/'expansion_geometry.json').read_text(), parse_float=str)
    rng = np.random.default_rng(71420)
    left, right, weights = [], [], []
    r = mp.mpf(str(radius))
    for pair in raw['cm_actions']:
        a, b = mp.mpc(*pair[0]), mp.mpc(*pair[1])
        if abs(b) < mp.mpf('1e-10'):
            continue
        q = -b/a
        midpoint = q/(1+1/abs(a))
        perturb = mp.mpf('.005')*mp.sqrt(float(rng.random()))*mp.exp(2j*mp.pi*float(rng.random()))
        w = (midpoint+perturb)/(1+mp.conj(midpoint)*perturb)
        denominator = mp.conj(b)*w+mp.conj(a)
        v, derivative = (a*w+b)/denominator, 1/denominator**2
        if max(abs(w), abs(v)) >= r:
            raise RuntimeError('independent side sample leaves the expansion disk')
        left.append((w/r)**32)
        right.append((v/r)**32)
        weights.append(derivative*(v/w)**31)
    return left, right, weights


def audit_sides(backend, coefficients, radius, method):
    left, right, weights = side_nodes(radius)
    lhs = evaluate(coefficients, backend.vector(left), method)
    rhs = evaluate(coefficients, backend.vector(right), method)
    native_weights = backend.vector(weights)
    errors = weighted_difference(lhs, rhs, native_weights)
    # Normalize by the left side; no conversion of the evaluated series to double.
    return {'samples': len(left), 'norm': 'column infinity norm, normalized by left side',
            'relative_residuals': relative_bounds(errors.bounds(), lhs.bounds(0)),
            'arithmetic_radius_relative_bounds': relative_bounds(errors.bounds(1), lhs.bounds(0))}


def normalized_jets(coefficients):
    """D46 gauge at arbitrary precision, with no projection onto real values."""
    raw = coefficients.to_mpmath(rows=64)
    normalized = raw * raw[:16, :]**-1
    alpha = 3*normalized[16, 15]
    if abs(alpha) < mp.mpf('1e-6'):
        raise ArithmeticError('degenerate period gauge')
    jets = mp.matrix([[normalized[i, j]*alpha**(j-i) for j in range(16)]
                      for i in range(raw.rows)])
    return jets, alpha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument('--columns', type=int, default=2)
    parser.add_argument('--threads', type=int, default=4, help='independent native column workers')
    parser.add_argument('--digits', type=int, default=50)
    parser.add_argument('--oversample', type=int, default=2)
    parser.add_argument('--check-oversample', type=int, default=3)
    parser.add_argument('--offset', default='0.37')
    parser.add_argument('--check-offset', default='0.19')
    parser.add_argument('--radius', type=float, default=.99991)
    parser.add_argument('--method', choices=['horner', 'rectangular'], default='rectangular')
    parser.add_argument('--iterations', type=int, default=5)
    parser.add_argument('--target', default='1e-40')
    parser.add_argument('--initial', type=Path, default=DATA/'cm_differentials_10240_refined.npz')
    parser.add_argument('--comparison', type=Path, help='another script 79 JSON with 16-column normalized jets')
    parser.add_argument('--output', type=Path, required=True, help='new JSON report; also writes .out and .acb')
    args = parser.parse_args()
    if not (64 <= args.n and 1 <= args.columns <= 16 and 20 <= args.digits <= 50 and 1 <= args.threads <= 16):
        parser.error('require n>=64, 1<=columns<=16, 1<=threads<=16, and 20<=digits<=50 with current geometry')
    if args.comparison and args.columns != 16:
        parser.error('gauge comparison requires all 16 columns')
    if not (args.oversample >= 1 and args.check_oversample > args.oversample and
            0 < args.radius < 1 and args.iterations >= 1):
        parser.error('require valid radius, positive iterations, and a larger check quadrature')
    if any(args.output.with_suffix(ext).exists() for ext in ('.json', '.out', '.acb')):
        parser.error('output artifacts already exist; choose a new output path')
    if args.output.suffix != '.json':
        parser.error('output must have a .json suffix')
    mp.mp.dps = args.digits+20
    target = mp.mpf(args.target)
    if not mp.isfinite(target) or not 0 < target < 1:
        parser.error('require a positive target below one')
    for value in (args.offset, args.check_offset):
        if not mp.isfinite(mp.mpf(value)):
            parser.error('quadrature offsets must be finite')
    started = time.monotonic()
    timings = {}
    backend = Backend(args.digits)
    bank = np.load(args.initial, allow_pickle=False)
    if float(bank['radius']) != args.radius or bank['coefficients'].shape[1] != 16:
        raise ValueError('initial basis must have 16 columns at the requested radius')
    seed = bank['coefficients'][:args.n]
    seed = np.pad(seed, ((0, max(0, args.n-len(seed))), (0, 0)))
    basis_double = np.linalg.qr(seed)[0]
    basis = backend.vector(basis_double, doubles=True)
    rhs = basis_double[:, :args.columns]
    rhs_norms = basis.bounds(0)[:args.columns]

    stage = time.monotonic()
    nodes, weights, geometry_stats = geometry(
        args.n, args.n*args.oversample, args.radius, args.offset, args.digits+20)
    timings['geometry_seconds'] = time.monotonic()-stage
    op = CauchyOperator(backend, args.n, backend.vector(nodes), backend.vector(weights),
                        args.offset, args.method, min(args.threads, args.columns))
    stage = time.monotonic()
    # LAPACK overwrites a Fortran-contiguous array. Building it in that
    # layout avoids a second n-by-n complex allocation before the LU.
    matrix = pilot.operator_from_nodes(args.n, nodes, weights, float(args.offset), order='F')
    matrix *= -1
    matrix[np.diag_indices(args.n)] += 1
    for start in range(0, args.n, 128):
        stop = min(start+128, args.n)
        matrix[:, start:stop] += basis_double@basis_double[start:stop].conj().T
    condition = float(np.linalg.cond(matrix)) if args.n <= 512 else None
    factor = lu_factor(matrix, overwrite_a=True, check_finite=False)
    lu_in_place = bool(np.shares_memory(matrix, factor[0]))
    del matrix
    x = backend.vector(lu_solve(factor, rhs, check_finite=False), doubles=True)
    timings['assembly_and_lu_seconds'] = time.monotonic()-stage
    print(json.dumps({'stage': 'factorized once', 'n': args.n, 'columns': args.columns,
                      'flint_version': backend.version, **timings}), flush=True)

    reference_control = None
    if args.n <= 128:
        stage = time.monotonic()
        raw = x.to_mpmath()
        expected = reference.cauchy_apply(raw[:, 0], nodes, weights, mp.mpf(args.offset))
        result = op.apply(x).to_mpmath()[:, 0]
        difference = mp.norm(result-expected)/mp.norm(expected)
        if difference >= mp.mpf(10)**(-(args.digits-5)):
            raise ArithmeticError('compiled action disagrees with script 78 reference')
        reference_control = decimal(difference)
        timings['reference_control_seconds'] = time.monotonic()-stage

    history = []
    solves = 1
    for step in range(args.iterations+1):
        stage = time.monotonic()
        residual, actual_defect = op.residual(x, basis, return_defect=True)
        relative = relative_bounds(residual.bounds(), rhs_norms)
        arithmetic = relative_bounds(residual.bounds(1), rhs_norms)
        record = {'step': step, 'relative_residuals': relative,
                  'arithmetic_radius_relative_bounds': arithmetic,
                  'residual_seconds': time.monotonic()-stage}
        history.append(record)
        print(json.dumps(record), flush=True)
        if max(map(mp.mpf, relative)) < target or step == args.iterations:
            break
        normalized, exponents = residual.scaled_doubles()
        stage = time.monotonic()
        correction = lu_solve(factor, normalized, check_finite=False)
        solves += 1
        x.add_correction(correction, exponents)
        record['correction_seconds'] = time.monotonic()-stage

    converged = max(map(mp.mpf, history[-1]['relative_residuals'])) < target
    # Save exact FLINT values before the more expensive independent audits.
    x.write(args.output.with_suffix('.acb'))
    stage = time.monotonic()
    finite_operator = relative_bounds(actual_defect.bounds(), x.bounds(0))
    timings['finite_operator_audit_seconds'] = time.monotonic()-stage
    op.close()
    del op, factor, actual_defect

    stage = time.monotonic()
    print(json.dumps({'stage': 'independent larger quadrature', 'samples': args.n*args.check_oversample}), flush=True)
    check_nodes, check_weights, check_stats = geometry(
        args.n, args.n*args.check_oversample, args.radius, args.check_offset, args.digits+20)
    check_op = CauchyOperator(backend, args.n, backend.vector(check_nodes),
                              backend.vector(check_weights), args.check_offset, args.method,
                              min(args.threads, args.columns))
    check_defect = x.subtract(check_op.apply(x))
    independent_operator = relative_bounds(check_defect.bounds(), x.bounds(0))
    timings['independent_quadrature_seconds'] = time.monotonic()-stage
    check_op.close()
    del check_op, check_defect
    stage = time.monotonic()
    print(json.dumps({'stage': 'independent side transformations'}), flush=True)
    sides = audit_sides(backend, x, args.radius, args.method)
    timings['all_side_audit_seconds'] = time.monotonic()-stage

    report = {'status': ('finite linear system converged; differential accuracy is limited by independent audits'
                         if converged else 'FAIL: finite linear refinement did not meet target'),
              'n': args.n, 'columns': args.columns, 'radius': args.radius,
              'decimal_digits': args.digits, 'working_bits': backend.bits,
              'geometry_replay_decimal_digits': args.digits+20,
              'geometry_source_sha256': hashlib.sha256((DATA/'expansion_geometry.json').read_bytes()).hexdigest(),
              'initial_basis': str(args.initial),
              'initial_basis_sha256': hashlib.sha256(args.initial.read_bytes()).hexdigest(),
              'stabilizing_basis_double_sha256': hashlib.sha256(basis_double.tobytes()).hexdigest(),
              'native_source_sha256': backend.source_sha256,
              'flint_version': backend.version, 'evaluation_method': args.method,
              'native_column_threads': min(args.threads, args.columns),
              'lu_factorizations': 1, 'lu_solves_including_initial': solves,
              'dense_matrix_layout': 'Fortran contiguous',
              'dense_matrix_bytes': args.n*args.n*np.dtype(complex).itemsize,
              'lu_overwrites_input': lu_in_place,
              'matrix_condition_2_double': condition,
              'script78_action_relative_difference': reference_control,
              'norm': 'column infinity norm; residual bounds normalized by midpoint norm upper bounds',
              'target_linear_relative_residual': str(args.target),
              'linear_system_converged': converged,
              'geometry': geometry_stats, 'refinement_history': history,
              'finite_operator_relative_residuals': finite_operator,
              'independent_quadrature': {**check_stats, 'relative_residuals': independent_operator},
              'all_side_audit': sides, 'timings': timings,
              'checkpoint': str(args.output.with_suffix('.acb')),
              'limitations': ['geometry input has about 57 decimal digits and is not interval certified',
                  'FLINT balls enclose arithmetic for supplied decimal data, not exact geometry or truncation',
                  'stabilized linear residual does not bound the differential or canonical coefficient error',
                  'independent quadrature and side checks are empirical diagnostics',
                  'no exact algebraic model, field recognition, or torsion calculation']}
    if args.columns == 16:
        jets, alpha = normalized_jets(x)
        report['normalized_jets_first64'] = [
            [[mp.nstr(z.real, args.digits), mp.nstr(z.imag, args.digits)] for z in row]
            for row in jets.tolist()]
        report['alpha'] = [mp.nstr(alpha.real, args.digits), mp.nstr(alpha.imag, args.digits)]
        report['normalized_jets_imaginary_relative_norm'] = decimal(
            mp.sqrt(sum(z.imag**2 for z in jets))/mp.norm(jets))
        if args.comparison:
            previous = json.loads(args.comparison.read_text())
            old = mp.matrix([[mp.mpc(*pair) for pair in row]
                             for row in previous['normalized_jets_first64']])
            report['comparison'] = {'path': str(args.comparison), 'n': previous['n'],
                                    'normalized_jet_relative_difference_first64': decimal(mp.norm(jets-old)/mp.norm(jets)),
                                    'normalized_jet_max_absolute_difference_first64': decimal(max(map(abs, jets-old)))}
    report['wall_seconds'] = time.monotonic()-started
    text = json.dumps(report, indent=2)+'\n'
    args.output.write_text(text)
    args.output.with_suffix('.out').write_text(text)
    print(json.dumps({k: v for k, v in report.items() if k != 'normalized_jets_first64'}, indent=2), flush=True)
    if not converged:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
