"""Compare symmetric trace data for the saved degree-three cover Y -> C.

The selected differential is a complex analytic direction, not an F-defined
generator. These are conditioning and automorphy checks, not recognition.
The source banks were computed with the user's Belyi Cauchy implementation.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

import mpmath as mp
import numpy as np
from scipy.linalg import lstsq, solve

HERE = Path(__file__).resolve().parent
DATA = HERE.parent/'data/computed'
spec = importlib.util.spec_from_file_location('relative_cover', HERE/'81_belyi_cover.py')
cover = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cover
spec.loader.exec_module(cover)
polyval = np.polynomial.polynomial.polyval


def compare(left, right):
    left, right = np.asarray(left), np.asarray(right)
    if left.shape != right.shape or not left.size:
        raise ValueError('nonempty arrays of the same shape are required')
    if not np.isfinite(left).all() or not np.isfinite(right).all():
        raise ValueError('nonfinite comparison data')
    if left.ndim == 1:
        left, right = left[:, None], right[:, None]
    scales = np.maximum(np.linalg.norm(left, axis=1), np.linalg.norm(right, axis=1))
    valid = scales > 1e-200
    if not valid.any():
        raise ValueError('zero data do not provide a valid comparison')
    errors = np.linalg.norm(left-right, axis=1)[valid]/scales[valid]
    return {'relative_l2': float(np.linalg.norm(left-right)/max(np.linalg.norm(left), np.linalg.norm(right))),
            'pointwise_relative_median': float(np.median(errors)),
            'pointwise_relative_max': float(max(errors)),
            'nonzero_rows': int(sum(valid)), 'zero_rows': int(sum(~valid))}


def features(bank, start, stop, sectors):
    n = len(bank)//sectors
    if len(bank) % sectors or not 0 <= start < stop <= n:
        raise ValueError('insufficient sector coefficients')
    return np.concatenate([bank[j*n+start:j*n+stop] for j in range(sectors)])


def align(current, previous, sectors, length=128, column=0):
    """Fit one direction, and check disjoint coefficients beyond the fit."""
    target = features(current, 0, length, sectors)
    source = features(previous, 0, length, sectors)
    weights, _, rank, singular = lstsq(source, target[:, column])
    if rank != source.shape[1]:
        raise ValueError('alignment matrix does not have full column rank')
    held_current = features(current, length, 2*length, sectors)[:, column]
    held_previous = features(previous, length, 2*length, sectors)@weights
    return current[:, column], previous@weights, {
        'chosen_current_column': column, 'fit_coefficients_per_sector': length,
        'current_feature_condition': float(np.linalg.cond(target)),
        'previous_feature_condition': float(singular[0]/singular[-1]),
        'fit': compare(source@weights, target[:, column]),
        'held_out': compare(held_previous, held_current),
        'previous_basis_weights': [[float(z.real), float(z.imag)] for z in weights]}


def cubic_coefficients(a, b, c, u):
    """Coefficients of T^3,T,1, multiplied by u*c^3 to avoid division.

    Sheet values are -2a/c, (a+b/sqrt(u))/c, (a-b/sqrt(u))/c.
    The sign of sqrt(u) has no effect on these coefficients.
    """
    return np.stack((u*c**3, -(3*u*a*a+b*b)*c, -2*a*(b*b-u*a*a)), axis=-1)


def coarse_values(u, differential, base):
    n = len(differential)//2
    a, b, c = polyval(u, differential[:n]), polyval(u, differential[n:]), polyval(u, base)
    return cubic_coefficients(a, b, c, u), c


def disk_values(w, differential, base, radius):
    n = len(differential)//2
    h = w/radius
    u = h**32
    a = polyval(u, differential[:n])*h**31
    b = polyval(u, differential[n:])*h**15
    eta = polyval(u, base)*h**31
    second, third = 3*a*a+b*b, 2*a*(b*b-a*a)
    # All three polynomial coefficients transform by the cube of the
    # differential multiplier. No division by eta at its zeros is needed.
    polynomial = np.stack((eta**3, -second*eta, -third), axis=-1)
    return polynomial, (eta, second, third)


def side_audit(differential, base, geometry, radius, count=384, seed=8453):
    rng = np.random.default_rng(seed)
    q, phase, delta = geometry.actions
    selected = np.resize(np.arange(len(q)), count)
    rng.shuffle(selected)
    q, phase, delta = q[selected], phase[selected], delta[selected]
    w = q/(1+np.sqrt(delta)) + 2e-5*(rng.random(count)-.5)*np.exp(2j*np.pi*rng.random(count))
    v = phase*(w-q)/(1-q.conjugate()*w)
    derivative = phase*delta/(1-q.conjugate()*w)**2
    keep = (abs(w) < radius) & (abs(v) < radius)
    w, v, derivative = w[keep], v[keep], derivative[keep]
    lhs, traces = disk_values(w, differential, base, radius)
    rhs, other = disk_values(v, differential, base, radius)
    return {'samples': len(w), 'distinct_sides': len(set(selected[keep])), 'seed': seed,
            'homogeneous_cubic': compare(lhs, derivative[:, None]**3*rhs),
            'base_differential': compare(traces[0], derivative*other[0]),
            'quadratic_trace': compare(traces[1], derivative**2*other[1]),
            'cubic_trace': compare(traces[2], derivative**3*other[2])}


def load_bank(path, columns):
    with np.load(path) as bank:
        coefficients, radius = bank['coefficients'], float(bank['radius'])
    if coefficients.ndim != 2 or coefficients.shape[1] != columns:
        raise ValueError(f'expected {columns} differential columns in {path}')
    if not np.isfinite(coefficients).all() or not 0 < radius < 1:
        raise ValueError('invalid bank coefficients or radius')
    return coefficients, radius, {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def weighted_pullback(rows, psi, scale, exponent, pointed):
    """Exponent 1 for a(u)du, 1/2 for b(u)du/sqrt(u)."""
    length = len(psi)
    powers = [pointed.unit_power(psi, mp.mpf(n)+exponent) for n in range(length)]
    return np.array([[complex(mp.fsum(mp.mpc(z)*powers[n][n-k]
                                     for k, z in enumerate(rows[:n+1, j]))/scale**(n+exponent))
                      for j in range(rows.shape[1])] for n in range(length)])


def marked_scan(banks):
    """A bounded negative experiment: zero jets at both marked points.

    The resulting line would be F-defined under D52's hypotheses and
    exact rank conditions. The numerical rank and accuracy are uncertified.
    Both cover banks use the same current base parameter in this scan.
    """
    spec = importlib.util.spec_from_file_location('relative_pointed', HERE/'83_pointed_normalization.py')
    pointed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pointed)
    with mp.workdps(50):
        length = 34
        forms, _, psi = pointed.intrinsic(banks[2][0][:length+15].tolist(), list(range(16)), length)
        scale = 12*forms[16, 13]/forms[16, 14]
        transformed = []
        for raw, _, _ in banks[:2]:
            n = len(raw)//2
            transformed.append((raw,
                                weighted_pullback(raw[:length], psi, scale, mp.mpf(1), pointed),
                                weighted_pullback(raw[n:n+length], psi, scale, mp.mpf('.5'), pointed)))
        trials = []
        for m in (16, 20, 24, 28, 32):
            q = 47-m
            solutions, conditions = [], []
            for raw, a, b in transformed:
                matrix = np.concatenate([a[:m+1], b[:q]])
                rownorm = np.linalg.norm(matrix, axis=1)
                target = np.zeros(48)
                target[m] = 1
                weights = solve(matrix/rownorm[:, None], target/rownorm)
                solutions.append(features((raw@weights)[:, None], 0, 128, 2))
                conditions.append({'raw': float(np.linalg.cond(matrix)),
                                   'row_normalized': float(np.linalg.cond(matrix/rownorm[:, None]))})
            trials.append({'vanishing_a_coefficients': m, 'vanishing_b_coefficients': q,
                           'normalization': f'a[{m}]=1', 'conditions_current_previous': conditions,
                           'independent_banks': compare(*solutions)})
    return {'status': 'bounded marked-line comparison; no arithmetic coefficients recognized',
            'F_line_claim': 'conditional on D52 arithmetic parameter, exact spaces and rank',
            'common_base_source': banks[2][2], 'formal_working_digits': 50,
            'line_solve_precision': 'double after row normalization', 'trials': trials}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, default=DATA/'belyi_cover_pilot_4096.npz')
    parser.add_argument('--comparison', type=Path, default=DATA/'belyi_cover_pilot_2048.npz')
    parser.add_argument('--base', type=Path, default=DATA/'cm_differentials_10240_refined.npz')
    parser.add_argument('--base-comparison', type=Path, default=DATA/'cm_differentials_8192_refined.npz')
    parser.add_argument('--fit-length', type=int, default=128)
    parser.add_argument('--column', type=int, default=0)
    parser.add_argument('--marked-scan', action='store_true', help='also reproduce five unstable two-point line trials')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.column < 48 or args.fit_length < 24:
        parser.error('column must lie in [0,48), with fit length at least 24')
    started = time.monotonic()
    banks = [load_bank(path, columns) for path, columns in
             [(args.basis, 48), (args.comparison, 48), (args.base, 16), (args.base_comparison, 16)]]
    if len({x[1] for x in banks}) != 1:
        raise ValueError('all banks must use the same disk radius')
    radius = banks[0][1]
    new, old, alignment = align(banks[0][0], banks[1][0], 2, args.fit_length, args.column)
    base, base_old, base_alignment = align(banks[2][0], banks[3][0], 1, args.fit_length)
    geometry = cover.Geometry()
    report = {'status': 'empirical complex trace comparison; no arithmetic generator or curve recognized',
              'arithmetic_recognition_attempted': False, 'generator_field_certified': False,
              'input_precision': 'double', 'sources': [b[2] for b in banks],
              'geometry_sha256': geometry.sha256, 'radius': radius,
              'cover_alignment': alignment, 'base_alignment': base_alignment,
              'interior': [], 'side_checks': {}}
    for uradius in (.25, .6, .85):
        u = uradius*np.exp(2j*np.pi*(np.arange(48)+.271)/48)
        current, den = coarse_values(u, new, base)
        previous, old_den = coarse_values(u, old, base_old)
        if min(abs(den)) == 0 or min(abs(old_den)) == 0:
            raise ValueError('a sample is a pole of the chosen affine generator')
        # u*A and u*B remove the known simple pole at the CM base point.
        affine = np.stack((-current[:, 1]/den**3, -current[:, 2]/den**3), axis=-1)
        old_affine = np.stack((-previous[:, 1]/old_den**3, -previous[:, 2]/old_den**3), axis=-1)
        report['interior'].append({'u_radius': uradius, 'samples': len(u),
                                   'minimum_denominator_absolute_value': float(min(min(abs(den)), min(abs(old_den)))),
                                   'homogeneous_cubic': compare(current, previous),
                                   'pole_cleared_A': compare(affine[:, 0], old_affine[:, 0]),
                                   'pole_cleared_B': compare(affine[:, 1], old_affine[:, 1])})
    for label, differential, denominator in [('current', new, base), ('previous', old, base_old)]:
        report['side_checks'][label] = side_audit(differential, denominator, geometry, radius)
    if args.marked_scan:
        report['marked_line_scan'] = marked_scan(banks)
    report['wall_seconds'] = time.monotonic()-started
    output = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(output)
    args.output.with_suffix('.out').write_text(output)
    print(report['status'])
    print('cover held-out relative difference:', alignment['held_out']['relative_l2'])
    print('current cubic side check:', report['side_checks']['current']['homogeneous_cubic'])


if __name__ == '__main__':
    main()
