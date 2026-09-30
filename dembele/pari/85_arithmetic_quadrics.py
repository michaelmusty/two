"""Recover canonical quadrics in D52's arithmetic basis, without long substitution.

Only a short jet determines the change of differential basis. Canonical
relations can then be recovered in the original analytic coordinate:
reparametrization multiplies all canonical coordinates by the same factor.
Field assertions remain conditional on the marked-point hypotheses.
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
from scipy.linalg import lstsq, qr, svdvals

HERE = Path(__file__).resolve().parent
DATA = HERE.parent/'data/computed'
spec = importlib.util.spec_from_file_location('quadric_pointed', HERE/'83_pointed_normalization.py')
pointed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pointed)


def arithmetic_change(source, orders, witness, rational_scale=12):
    """Return the basis change, up to one common scalar, in the OLD coordinate.

    If H_i(tau) are the intrinsic echelon forms and v=lambda*tau, the
    F-normalized differentials are lambda^(a_i+1) H_i(tau) d tau.
    Dropping their common factor lambda does not change canonical equations.
    """
    length = max(n for n, _, _ in witness)+1
    needed = length+orders[-1]
    if len(source) < needed:
        raise ValueError('insufficient source jets for the arithmetic basis')
    rows = mp.matrix(source[:needed].tolist() if hasattr(source, 'tolist') else source[:needed])
    forms, error, psi = pointed.intrinsic(rows, orders, length)
    _, scale = pointed.rescale(forms, orders, witness)
    scale *= rational_scale
    raw_pulled = pointed.pullback(rows, psi, length)
    pivot = mp.matrix([[raw_pulled[n, i] for i in range(rows.cols)] for n in orders])
    change = pivot**-1*mp.diag([scale**a for a in orders])
    short = pointed.apply_scale(forms, orders, scale)
    # Independent consistency between a raw-coordinate basis change and
    # the full short formal-coordinate calculation, including Jacobians.
    pulled_changed = pointed.pullback(rows*change, psi, length)
    difference = max(abs(pulled_changed[n, i]*scale**(-n)-short[n, i])
                     for n in range(length) for i in range(rows.cols))
    return change, short, {
        'source_jets_used': needed, 'orders': orders, 'weight_one_witness': witness,
        'rational_scale_factor': rational_scale, 'scale': pointed.decimal(scale),
        'short_formal_consistency_error': mp.nstr(difference, 10),
        'highest_line_formal_error': mp.nstr(error, 10),
        'basis_change_condition': float(np.linalg.cond(np.array(change.tolist(), complex))),
        'field_claim': 'conditional on the exact differential space, F-rational point, flag and nonzero scale'}


def products(series):
    pairs = list(combinations_with_replacement(range(series.shape[1]), 2))
    result = np.array([np.convolve(series[:, i], series[:, j])[:len(series)] for i, j in pairs]).T
    return result, pairs


def fit_relations(full, training, rank, pivots=None):
    if not rank < min(training, full.shape[1]) or training >= len(full):
        raise ValueError('the fit must leave equations and unused validation rows')
    if not np.isfinite(full).all():
        raise ValueError('nonfinite product data')
    train = full[:training]
    scales = np.linalg.norm(train, axis=0)
    if min(scales) <= 1e-200:
        raise ValueError('zero monomial column')
    scaled = train/scales
    singular = svdvals(scaled)
    observed = int(sum(singular > singular[0]*1e-9))
    if observed != rank:
        raise ValueError(f'product rank {observed}, expected {rank}')
    if pivots is None:
        _, _, order = qr(scaled, mode='economic', pivoting=True)
        pivots = [int(i) for i in order[:rank]]
    if len(pivots) != rank or len(set(pivots)) != rank:
        raise ValueError('distinct fixed pivot monomials are required')
    free = [i for i in range(full.shape[1]) if i not in pivots]
    fit = lstsq(scaled[:, pivots], scaled[:, free], lapack_driver='gelsy')[0]
    fit *= scales[free][None, :]/scales[pivots][:, None]
    equations = np.zeros((full.shape[1], len(free)), complex)
    equations[free, np.arange(len(free))] = 1
    equations[pivots] = -fit
    normalized = equations/np.linalg.norm(equations, axis=0)
    report = {'training_jets': training, 'validation_jets': len(full)-training,
              'product_rank': observed, 'equation_count': len(free),
              'scaled_singular_values': singular.tolist(),
              'pivot_product_condition': float(np.linalg.cond(scaled[:, pivots])),
              'coefficient_imaginary_relative_norm': float(np.linalg.norm(fit.imag)/np.linalg.norm(fit)),
              'max_absolute_equation_coefficient': float(np.max(abs(equations))),
              'held_out_relative_residual': float(np.linalg.norm(full[training:]@normalized)/np.linalg.norm(full[training:])),
              'fixed_pivot_monomials': pivots, 'free_monomials': free}
    return equations, report


def build(path, length, training, pivots=None):
    with np.load(path) as bank:
        source = bank['coefficients'][:length]
        radius = float(bank['radius'])
    if source.shape != (length, 16):
        raise ValueError('expected a sufficiently long 16-column base bank')
    change, short, gauge = arithmetic_change(source, list(range(16)), [(16, 14, -1), (16, 13, 1)])
    matrix = np.array(change.tolist(), complex)
    series = source@matrix
    full, pairs = products(series)
    equations, report = fit_relations(full, training, 45, pivots)
    report.update({'source': str(path), 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'radius': radius, 'arithmetic_gauge': gauge})
    return equations, full, matrix, np.array(short.tolist(), complex), pairs, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, default=DATA/'cm_differentials_10240_refined.npz')
    parser.add_argument('--comparison', type=Path, default=DATA/'cm_differentials_8192_refined.npz')
    parser.add_argument('--length', type=int, default=768)
    parser.add_argument('--training', type=int, default=256)
    parser.add_argument('--digits', type=int, default=60)
    parser.add_argument('--pivots-from', type=Path, help='reuse the monomial normalization from an earlier report')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    pivots = (json.loads(args.pivots_from.read_text())['current']['fixed_pivot_monomials']
              if args.pivots_from else None)
    with mp.workdps(args.digits):
        current, full, change, short, pairs, details = build(args.basis, args.length, args.training, pivots)
        old, old_full, old_change, old_short, _, previous = build(args.comparison, args.length, args.training,
                                                                 details['fixed_pivot_monomials'])
    if details['radius'] != previous['radius']:
        raise ValueError('independent banks must use the same source coordinate radius')
    pivots = details['fixed_pivot_monomials']
    difference = current[pivots]-old[pivots]
    report = {'status': '91 numerical quadrics in the conditional arithmetic basis; no exact model recognized',
              'input_precision': 'double', 'formal_working_digits': args.digits,
              'long_formal_coordinate_substitution': False, 'current': details, 'comparison': previous,
              'coefficient_relative_difference': float(np.linalg.norm(difference)/np.linalg.norm(current[pivots])),
              'coefficient_max_absolute_difference': float(np.max(abs(difference))),
              'other_bank_relative_residual': float(np.linalg.norm(old_full@(current/np.linalg.norm(current, axis=0)))/np.linalg.norm(old_full)),
              'arithmetic_recognition_attempted': False, 'wall_seconds': time.monotonic()-started}
    output = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(output)
    args.output.with_suffix('.out').write_text(output)
    np.savez(args.output.with_suffix('.npz'), quadrics=current, comparison_quadrics=old,
             pairs=np.asarray(pairs), pivots=np.asarray(pivots), free=np.asarray(details['free_monomials']),
             change=change, comparison_change=old_change, short_arithmetic_jets=short,
             comparison_short_arithmetic_jets=old_short)
    print(report['status'])
    print('coefficient relative difference:', report['coefficient_relative_difference'])
    print('held-out residual:', details['held_out_relative_residual'])


if __name__ == '__main__':
    main()
