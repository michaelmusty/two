"""Intrinsic marked-point gauges for the saved 48-dimensional cover pilot.

This is a numerical conditioning experiment, not algebraic recognition.
The source coefficients are doubles. Additional working digits only keep
the formal coordinate operations from adding appreciable roundoff.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import qr

DATA = Path(__file__).resolve().parents[1]/'data/computed'


def unit_power(unit, exponent):
    """Power of a formal series with constant coefficient one."""
    if unit[0] != 1:
        raise ValueError('a unit with constant coefficient one is required')
    result = [mp.mpc(1)]
    for n in range(1, len(unit)):
        result.append(mp.fsum((((exponent+1)*k-n)*unit[k]*result[n-k]
                               for k in range(1, n+1)))/n)
    return result


def intrinsic(coefficients, orders, length, coordinate_unit=None):
    """Lagrange-inversion implementation; exact reference uses substitution."""
    rows = mp.matrix(coefficients)
    rank, m = rows.cols, orders[-1]
    if len(orders) != rank or list(orders) != sorted(set(orders)):
        raise ValueError('one increasing vanishing order per column is required')
    needed = length+m if coordinate_unit is None else length
    if rows.rows < needed or length <= m:
        raise ValueError('insufficient input or output jets')
    pivots = mp.matrix([[rows[j, i] for i in range(rank)] for j in orders])
    h = rows*pivots**-1
    for j, a in enumerate(orders):
        for i in range(rank):
            h[a, i] = int(i == j)
    # Known lower zeros of the highest line; these are exact when the
    # proposed vanishing sequence and source differential space are exact.
    for n in range(m):
        h[n, rank-1] = 0
    if coordinate_unit is None:
        d = m+1
        unit = [d*h[m+k, rank-1]/(d+k) for k in range(length)]
        psi = unit_power(unit, -mp.mpf(1)/d)
    else:
        # psi = u/tau for an already chosen coordinate on the base curve.
        psi = coordinate_unit
    transformed = pullback(h, psi, length)
    # A change tau=u+... makes this pivot matrix unit lower triangular.
    # Back substitution avoids a generic LU's scale-based singularity test.
    out = mp.matrix(transformed)
    for i in reversed(range(rank)):
        for j in range(i+1, rank):
            coefficient = transformed[orders[j], i]
            for n in range(length):
                out[n, i] -= coefficient*out[n, j]
    top_error = max(abs(out[n, rank-1]-int(n == m)) for n in range(length))
    return out, top_error, psi


def pullback(coefficients, psi, length):
    """Transform arbitrary differential columns without choosing a basis."""
    h = mp.matrix(coefficients)
    if h.rows < length or len(psi) < length:
        raise ValueError('insufficient jets for pullback')
    power = psi[:length]
    transformed = mp.matrix(length, h.cols)
    for n in range(length):
        # [tau^n] H_i(tau) = [u^n] h_i(u) (u/tau)^(n+1).
        for i in range(h.cols):
            transformed[n, i] = mp.fsum(h[k, i]*power[n-k] for k in range(n+1))
        if n+1 < length:
            power = [mp.fsum(power[k]*psi[j-k] for k in range(j+1))
                     for j in range(length)]
    return transformed


def select_jets(forms, indices=None):
    """Choose fixed coefficient functionals in an arithmetic parameter.

    These indices need not be vanishing orders. Once selected, they must
    be held fixed for all subsequent comparisons and exact reconstruction.
    """
    numeric = np.array(forms.tolist(), dtype=complex)
    orthonormal, _ = qr(numeric, mode='economic')
    if indices is None:
        _, _, permutation = qr(orthonormal.T, pivoting=True, mode='economic')
        indices = sorted(int(i) for i in permutation[:forms.cols])
    if len(indices) != forms.cols or len(set(indices)) != len(indices):
        raise ValueError('one distinct jet index per column is required')
    pivot = mp.matrix([[forms[n, i] for i in range(forms.cols)] for n in indices])
    return forms*pivot**-1, indices, {
        'selected_jet_condition_number': float(np.linalg.cond(numeric[indices])),
        'selected_jet_condition_after_whitening': float(np.linalg.cond(orthonormal[indices]))}


def rescale(forms, orders, witness):
    if sum(e*(n-orders[i]) for n, i, e in witness) != 1:
        raise ValueError('the scale must have weight exactly one')
    scale = mp.mpc(1)
    for n, i, e in witness:
        if forms[n, i] == 0:
            raise ValueError('a scale coefficient vanishes')
        scale *= forms[n, i]**e
    return apply_scale(forms, orders, scale), scale


def apply_scale(forms, orders, scale):
    out = mp.matrix(forms.rows, forms.cols)
    for n in range(forms.rows):
        for i, a in enumerate(orders):
            out[n, i] = forms[n, i]*scale**(a-n)
    return out


def decimal(z):
    return [mp.nstr(mp.re(z), 30), mp.nstr(mp.im(z), 30)]


def read_jets(path, point, length):
    bank = np.load(path)
    coefficients = bank['coefficients']
    n = len(coefficients)//2
    if coefficients.shape != (2*n, 48):
        raise ValueError('expected the 48-column new-component bank')
    if point == 'P32':
        jets = coefficients[:length]
    else:
        jets = np.empty((length, 48), complex)
        jets[0::2] = coefficients[n:n+(length+1)//2]
        jets[1::2] = coefficients[:length//2]
    return jets


def analyze(path, length, base_path, gauge='initial', indices=None):
    point = 'P32'
    source = read_jets(path, point, length)
    coefficients = [[mp.mpc(float(z.real), float(z.imag)) for z in row] for row in source]
    base_bank = np.load(base_path)
    if float(base_bank['radius']) != float(np.load(path)['radius']):
        raise ValueError('the cover and base must use the same disk radius')
    base_source = base_bank['coefficients'][:length+15]
    base_coefficients = [[mp.mpc(float(z.real), float(z.imag)) for z in row] for row in base_source]
    base_forms, top_error, psi = intrinsic(base_coefficients, list(range(16)), length)
    witness = [(16, 14, -1), (16, 13, 1)]
    _, scale = rescale(base_forms, list(range(16)), witness)
    # A fixed rational factor keeps the parameter scale near unit size.
    scale *= 12
    base_normalized = apply_scale(base_forms, list(range(16)), scale)
    # Pull back the same formal parameter through the unramified P32 -> P
    # branch. No root extraction is needed on this branch of Y -> C.
    if gauge == 'initial':
        forms, _, _ = intrinsic(coefficients, list(range(48)), length, coordinate_unit=psi)
        normalized = apply_scale(forms, list(range(48)), scale)
        extra = {'proposed_vanishing_sequence': list(range(48)), 'vanishing_sequence_certified': False}
    else:
        forms = apply_scale(pullback(coefficients, psi, length), [0]*48, scale)
        normalized, indices, extra = select_jets(forms, indices)
        extra['selected_jet_indices'] = indices
        extra['new_vanishing_sequence_required'] = False
    raw = json.loads(path.with_suffix('.json').read_text())
    result = {'source': str(path), 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'point': point, 'basis_gauge': gauge, **extra,
              'source_jet_condition_number': float(np.linalg.cond(source[:48])),
              'source_side_defect': max(raw['side_audit']['relative_l2_by_column']),
              'source_quadrature_defect': raw['changed_quadrature_defect'],
              'base_anchor_source': str(base_path),
              'base_anchor_sha256': hashlib.sha256(base_path.read_bytes()).hexdigest(),
              'base_jet_condition_number': float(np.linalg.cond(base_source[:16])),
              'weight_one_witness': witness, 'rational_scale_factor': 12,
              'scale': decimal(scale),
              'scale_coefficients': [decimal(base_forms[16, 14]), decimal(base_forms[16, 13])],
              'base_normalized_samples': [decimal(base_normalized[n, i])
                                           for n, i in [(16, 12), (17, 14), (18, 14)]],
              'base_highest_form_monomial_arithmetic_error': mp.nstr(top_error, 8)}
    return normalized, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, default=DATA/'belyi_cover_pilot_4096.npz')
    parser.add_argument('--comparison', type=Path, default=DATA/'belyi_cover_pilot_2048.npz')
    parser.add_argument('--base', type=Path, default=DATA/'cm_differentials_10240_refined.npz')
    parser.add_argument('--base-comparison', type=Path, default=DATA/'cm_differentials_10240_refined.npz')
    parser.add_argument('--gauge', choices=('initial', 'selected'), default='selected')
    parser.add_argument('--length', type=int, default=60)
    parser.add_argument('--digits', type=int, default=60)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.length < 52:
        parser.error('at least 52 output coefficients are needed for the fixed pilot')
    started = time.monotonic()
    mp.mp.dps = args.digits
    report = {'status': 'empirical normalization comparison; no algebraic coefficient recognized',
              'working_digits': args.digits, 'input_precision': 'double',
              'output_jets': args.length,
              'field_claim': 'conditional on exact spaces, base flag, nonzero scale and invertible selected jets',
              'arithmetic_recognition_attempted': False, 'points': {}}
    for point in ('P32',):
        current, details = analyze(args.basis, args.length, args.base, args.gauge)
        previous, old_details = analyze(args.comparison, args.length, args.base_comparison,
                                        args.gauge, details.get('selected_jet_indices'))
        samples = []
        # All six new-component samples are independent of the base gauge.
        if args.gauge == 'initial':
            sample_indices = [(48, 44), (48, 43), (49, 46), (49, 45), (50, 46), (51, 44)]
            unused = list(range(48, args.length))
        else:
            unused = [n for n in range(args.length) if n not in details['selected_jet_indices']]
            sample_indices = [(unused[j], (9*j+5) % 48) for j in range(min(6, len(unused)))]
        for n, i in sample_indices:
            z, old = current[n, i], previous[n, i]
            difference = abs(z-old)/max(1, abs(z), abs(old))
            samples.append({'row': n, 'column': i, 'value': decimal(z),
                            'comparison_value': decimal(old), 'scaled_difference': float(difference)})
        details['comparison'] = old_details
        details['unused_gauge_samples'] = samples
        details['max_sample_scaled_difference'] = max(s['scaled_difference'] for s in samples)
        delta = mp.sqrt(mp.fsum(abs(current[n, i]-previous[n, i])**2 for n in unused for i in range(48)))
        norm = max(mp.sqrt(mp.fsum(abs(m[n, i])**2 for n in unused for i in range(48)))
                   for m in (current, previous))
        details['all_unused_jets_relative_difference'] = float(delta/norm)
        details['normalized_jet_start_index'] = 0
        details['normalized_jets'] = [[decimal(current[n, i]) for i in range(48)]
                                       for n in range(args.length)]
        report['points'][point] = details
        print(point, 'jet condition', details['source_jet_condition_number'],
              'sample difference', details['max_sample_scaled_difference'], flush=True)
    report['wall_seconds'] = time.monotonic()-started
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(report['status'], flush=True)


if __name__ == '__main__':
    main()
