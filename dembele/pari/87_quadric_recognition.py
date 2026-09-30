"""Bounded, explicitly tentative recognition of nontrivial quadric entries.

The tolerance is an empirical discovery setting, not a certified enclosure.
Input strings preserve the precise solver's values but not guaranteed digits
of the underlying algebraic curve. Candidates require exact model validation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

import mpmath as mp

DATA = Path(__file__).resolve().parents[1]/'data/computed'


def cosine_basis(generator, degree):
    """[1, 2*cos(theta), ..., 2*cos((d-1)*theta)], by recurrence.

    This is an integral, unimodular change from the power basis. For the
    real 2-power cyclotomic fields used here, Galois acts by signed
    permutations on its nonconstant entries, so the height bound does
    not privilege one field embedding.
    """
    values = [mp.mpf(1)]
    previous, current = mp.mpf(2), generator
    for _ in range(1, degree):
        values.append(current)
        previous, current = current, generator*current-previous
    return values


def field_bases(kind='power'):
    b = 2*mp.cos(7*mp.pi/16)
    c = 2-b*b
    a = c*c-2
    if kind == 'cosine':
        return [(1, [mp.mpf(1)], 1000), (2, cosine_basis(a, 2), 100),
                (4, cosine_basis(c, 4), 8), (8, cosine_basis(b, 8), 4)]
    if kind != 'power':
        raise ValueError('unknown field basis')
    return [(1, [mp.mpf(1)], 1000), (2, [mp.mpf(1), a], 100),
            (4, [c**i for i in range(4)], 8), (8, [b**i for i in range(8)], 4)]


def scale_invariant_ratios(rows, old, pivots, free, pairs):
    """Cancel parameter scaling between entries of equal monomial weight.

    On rescaling the parameter by mu, a normalized quadric entry scales
    by mu^(weight(free)-weight(pivot)). Choose one nonintegral anchor
    per nonzero weight, fixing its indices in both independent banks.
    Weight-zero entries need no anchor. This is a discovery coordinate
    choice, not an assertion that it decreases arithmetic height.
    """
    weights = [[sum(pairs[f])-sum(pairs[p]) for f in free] for p in pivots]
    anchors = {}
    for i, row in enumerate(rows):
        for j, z in enumerate(row):
            weight = weights[i][j]
            if weight == 0 or not mp.mpf('0.01') < abs(z) < 100:
                continue
            if abs(z-mp.nint(z.real)) < mp.mpf('1e-7') or abs(old[i][j]) < mp.mpf('1e-8'):
                continue
            score = abs(z-old[i][j])/abs(z)
            if weight not in anchors or score < anchors[weight][0]:
                anchors[weight] = (score, i, j)
    current, previous = [], []
    for i, row in enumerate(rows):
        new_row, old_row = [], []
        for j, z in enumerate(row):
            weight = weights[i][j]
            if weight == 0:
                new_row.append(z)
                old_row.append(old[i][j])
            elif weight in anchors:
                _, ai, aj = anchors[weight]
                new_row.append(z/rows[ai][aj])
                old_row.append(old[i][j]/old[ai][aj])
            else:
                new_row.append(mp.mpc(0))
                old_row.append(mp.mpc(0))
        current.append(new_row)
        previous.append(old_row)
    return current, previous, {str(w): {'row': i, 'column': j}
                              for w, (_, i, j) in sorted(anchors.items())}


def relation(value, basis, height, tolerance):
    vector = mp.matrix(basis+[mp.re(value)])
    candidate = mp.pslq(vector, tol=tolerance, maxcoeff=height, maxsteps=3000)
    if candidate is None or candidate[-1] == 0:
        return None
    exact_value = -mp.fsum(a*b for a, b in zip(candidate[:-1], basis))/candidate[-1]
    error = abs(exact_value-value)
    if error > tolerance:
        return None
    tighter = mp.pslq(vector, tol=tolerance/10, maxcoeff=height, maxsteps=3000)
    return {'relation': [int(x) for x in candidate],
            'absolute_residual': mp.nstr(error, 18),
            'same_relation_at_tighter_tolerance': tighter == candidate,
            'status': 'numerical candidate only; no algebraic equality certified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, required=True, help='script 86 JSON')
    parser.add_argument('--comparison', type=Path, required=True, help='independent script 86 JSON')
    parser.add_argument('--samples', type=int, default=128)
    parser.add_argument('--tolerance', default='1e-13')
    parser.add_argument('--field-basis', choices=['power', 'cosine'], default='power')
    parser.add_argument('--field-height', type=int, help='override the degree-eight height bound only')
    parser.add_argument('--scale-invariant', action='store_true', help='use ratios of entries with equal scaling weight')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    mp.mp.dps = 80
    tolerance = mp.mpf(args.tolerance)
    if not 0 < tolerance < mp.mpf('1e-6') or not 1 <= args.samples <= 4095:
        parser.error('require 1..4095 samples and a tolerance between 0 and 1e-6')
    if args.field_height is not None and args.field_height < 2:
        parser.error('field height must be at least two')
    started = time.monotonic()
    current, previous = (json.loads(path.read_text()) for path in [args.basis, args.comparison])
    if (current['pivots'] != previous['pivots'] or current['free'] != previous['free']
            or current['monomial_pairs'] != previous['monomial_pairs']):
        raise ValueError('the two reports use different normalized equations')
    rows = [[mp.mpc(*z) for z in row] for row in current['pivot_coefficients']]
    old = [[mp.mpc(*z) for z in row] for row in previous['pivot_coefficients']]
    anchors = None
    if args.scale_invariant:
        rows, old, anchors = scale_invariant_ratios(rows, old, current['pivots'], current['free'],
                                                  current['monomial_pairs'])
    slots = []
    omitted_integer = 0
    for i, row in enumerate(rows):
        for j, z in enumerate(row):
            if abs(z-mp.nint(z.real)) < mp.mpf('1e-7'):
                omitted_integer += 1
                continue
            if not mp.mpf('1e-4') < abs(z) < 1000:
                continue
            delta = abs(z-old[i][j])/max(1, abs(z))
            slots.append((delta, i, j))
    slots.sort()
    fields = field_bases(args.field_basis)
    if args.field_height is not None:
        fields[-1] = (8, fields[-1][1], args.field_height)
    attempts, candidates = [], []
    for delta, i, j in slots[:args.samples]:
        z = rows[i][j]
        entry = {'row': i, 'column': j, 'pivot_monomial': current['pivots'][i],
                 'free_monomial': current['free'][j],
                 'value': [mp.nstr(z.real, 40), mp.nstr(z.imag, 20)],
                 'independent_bank_relative_difference': mp.nstr(delta, 16), 'candidate': None}
        for degree, basis, height in fields:
            candidate = relation(z, basis, height, tolerance)
            if candidate:
                coefficients = candidate['relation']
                recognized = -mp.fsum(a*b for a, b in zip(coefficients[:-1], basis))/coefficients[-1]
                candidate.update({'field_degree': degree, 'height_bound': height})
                candidate['independent_bank_absolute_residual'] = mp.nstr(abs(recognized-old[i][j]), 18)
                entry['candidate'] = candidate
                candidates.append({'row': i, 'column': j, **candidate})
                break
        attempts.append(entry)
    report = {'status': 'bounded recognition candidates only; no exact curve model',
              'source': str(args.basis), 'source_sha256': hashlib.sha256(args.basis.read_bytes()).hexdigest(),
              'comparison': str(args.comparison),
              'comparison_sha256': hashlib.sha256(args.comparison.read_bytes()).hexdigest(),
              'field_bases': 'Q; Q(sqrt(2)); Q(2 cos(pi/8)); F=Q(2 cos(7 pi/16))',
              'field_basis_kind': args.field_basis,
              'basis_formula': '[1, g, ..., g^(d-1)]' if args.field_basis == 'power'
                               else '[1, 2 cos(theta), ..., 2 cos((d-1) theta)], g=2 cos(theta)',
              'coordinate_values': 'ratios of equal-weight entries' if args.scale_invariant else 'normalized quadric entries',
              'scale_invariant_anchors': anchors,
              'field_degree_height_bounds': [[d, h] for d, _, h in fields],
              'empirical_absolute_tolerance': str(tolerance),
              'guaranteed_input_digits': None, 'near_integer_entries_omitted': omitted_integer,
              'eligible_entries': len(slots), 'attempts': attempts, 'candidates': candidates,
              'wall_seconds': time.monotonic()-started}
    text = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(text)
    args.output.with_suffix('.out').write_text(text)
    print('Nontrivial entries attempted:', len(attempts), 'candidates:', len(candidates))
    print('Near-integer entries omitted:', omitted_integer)


if __name__ == '__main__':
    main()
