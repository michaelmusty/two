"""Recover a one-pole Riemann--Roch map from two differential denominators.

For genus 16 and an ordinary marked point P, take a,b of orders 15,14.
If they have no other common zero, pairs of quadratic differentials
A,B with A*b^2=B*a^2 and ord(A)>=30-m, ord(B)>=28-m give L(mP).
The numerical rank and accuracy checks are discovery diagnostics only.
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
from scipy.linalg import qr, svdvals
from sage.all import ComplexBallField, RealBallField, PolynomialRing, matrix

HERE = Path(__file__).resolve().parent
DATA = HERE.parent/'data/computed'
spec = importlib.util.spec_from_file_location('pointed_map_precise', HERE/'86_precise_quadrics.py')
precise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(precise)


def decimal(z, digits=55):
    return [mp.nstr(mp.re(z), digits), mp.nstr(mp.im(z), digits)]


def forms_from_source(path, length, digits, basis_gauge='arithmetic'):
    source, provenance = precise.read_source(path, length, 50)
    if basis_gauge == 'arithmetic':
        change, _, gauge = precise.arithmetic.arithmetic_change(
            source.tolist(), list(range(16)), [(16, 14, -1), (16, 13, 1)])
    elif basis_gauge == 'flag':
        change = source[:16,:]**-1
        gauge = {'source_jets_used': 16, 'basis_is_asserted_F_defined': False,
                 'field_claim': 'L(mP) is F-defined; coefficients in this complex basis need not be'}
    else:
        raise ValueError('unknown canonical basis gauge')
    bits = int(mp.ceil(digits*mp.log(10, 2)))+32
    field, reals = ComplexBallField(bits), RealBallField(bits)
    def ball(z):
        return field(reals(mp.nstr(z.real, digits)), reals(mp.nstr(z.imag, digits)))
    transformed = matrix(field, [[ball(z) for z in row] for row in source.tolist()]) * \
        matrix(field, [[ball(z) for z in row] for row in change.tolist()])
    ring = PolynomialRing(field, 'u')
    forms = [ring(transformed.column(i).list()) for i in range(16)]
    discarded = max(float(abs(forms[j][i]).upper()) for j in range(16) for i in range(j))
    forms = [ring([0]*j+f.list()[j:]) for j, f in enumerate(forms)]
    return forms, {'source': provenance, 'basis_gauge_kind': basis_gauge, 'arithmetic_gauge': gauge,
                   'imposed_vanishing_orders': list(range(16)),
                   'maximum_discarded_lower_jet': discarded,
                   'ball_interpretation': 'arithmetic on supplied point data only'}


def independent_products(forms, minimum, dimension, forced, length, training, fixed=None, power=2, rank_tolerance=1e-10):
    pairs = [pair for pair in combinations_with_replacement(range(len(forms)), power)
             if sum(pair) >= minimum]
    products = []
    for pair in pairs:
        product = forms[0].parent()(1)
        for i in pair:
            product = (product*forms[i]).truncate(length)
        products.append(product)
    numeric = np.array([[complex(p[n].mid()) for p in products] for n in range(training)])
    norms = np.linalg.norm(numeric, axis=0)
    if not np.isfinite(numeric).all() or min(norms) == 0:
        raise ValueError('nonfinite or zero product column')
    scaled = numeric/norms
    singular = svdvals(scaled)
    if fixed is None:
        first = pairs.index(tuple(forced))
        others = [i for i in range(len(pairs)) if i != first]
        direction = scaled[:, first]
        projected = scaled[:, others]-direction[:, None]*(direction.conj()@scaled[:, others])[None, :]
        _, _, order = qr(projected, mode='economic', pivoting=True)
        chosen = [first]+[others[i] for i in order[:dimension-1]]
    else:
        chosen = [pairs.index(tuple(pair)) for pair in fixed]
    if len(chosen) != dimension or pairs[chosen[0]] != tuple(forced):
        raise ValueError('invalid fixed product basis')
    info = {'minimum_weight': minimum, 'expected_dimension': dimension,
            'rank_tolerance': rank_tolerance,
            'observed_rank': int(sum(singular > singular[0]*rank_tolerance)),
            'relative_singular_values': (singular/singular[0]).tolist(),
            'basis_pairs': [pairs[i] for i in chosen],
            'scaled_basis_condition': float(np.linalg.cond(scaled[:, chosen]))}
    return [products[i] for i in chosen], info


def recover_map(forms, pole_order, length, training, fixed=None, power=2, rank_tolerance=1e-10):
    genus = len(forms)
    degree_bound = 2*power*(2*genus-2)
    if genus < 3 or power < 2 or not genus <= pole_order <= power*(genus-2) \
            or not degree_bound+1 <= training < length or length < 64+power*(genus-1):
        raise ValueError('invalid genus, denominator power, pole order or interpolation window')
    a_order, b_order = power*(genus-1), power*(genus-2)
    a2, b2 = (forms[-1]**power).truncate(length), (forms[-2]**power).truncate(length)
    a_min, b_min = a_order-pole_order, b_order-pole_order
    section_dimension = (2*power-1)*(genus-1)
    products_a, info_a = independent_products(forms, a_min, section_dimension-a_min, (genus-1,)*power,
        length, training, fixed['numerator']['basis_pairs'] if fixed else None, power, rank_tolerance)
    products_b, info_b = independent_products(forms, b_min, section_dimension-b_min, (genus-2,)*power,
        length, training, fixed['other_numerator']['basis_pairs'] if fixed else None, power, rank_tolerance)
    # The known constant pair is (a^2,b^2). Set its first numerator
    # coefficient to zero, leaving one representative modulo constants.
    columns = [(p*b2).truncate(length) for p in products_a[1:]] + \
              [-(p*a2).truncate(length) for p in products_b]
    full = matrix(forms[0].base_ring(), [[p[n] for p in columns] for n in range(length)])
    numeric = precise.float_matrix(full[:training, :])
    norms = np.linalg.norm(numeric, axis=0)
    singular = svdvals(numeric/norms)
    expected_nullity = pole_order-genus
    rank = len(columns)-expected_nullity
    observed = int(sum(singular > singular[0]*rank_tolerance))
    info = {'pole_order': pole_order, 'genus': genus, 'denominator_power': power,
            'relation_section_degree': degree_bound,
            'expected_dimension_including_constants': expected_nullity+1,
            'expected_product_rank': rank, 'observed_rank': observed, 'rank_tolerance': rank_tolerance,
            'relative_singular_values': (singular/singular[0]).tolist(),
            'numerator': info_a, 'other_numerator': info_b,
            'coefficient_normalization': f'coefficient of a^{power} in A is zero; free relation entries are the identity',
            'rank_hypotheses_pass': observed == rank and
                info_a['observed_rank'] == len(products_a) and info_b['observed_rank'] == len(products_b)}
    if not info['rank_hypotheses_pass']:
        raise ValueError('numerical product ranks do not support the proposed Riemann--Roch space: '
                         f"{observed}/{rank}, A {info_a['observed_rank']}/{len(products_a)}, "
                         f"B {info_b['observed_rank']}/{len(products_b)}")
    if not expected_nullity:
        return [], info
    if fixed:
        pivots, free = fixed['pivots'], fixed['free']
    else:
        _, _, order = qr(numeric/norms, mode='economic', pivoting=True)
        pivots = [int(i) for i in order[:rank]]
        free = [i for i in range(len(columns)) if i not in pivots]
    coefficients, solve = precise.solve_relations(full, pivots, free, training)
    equations = matrix(full.base_ring(), len(columns), expected_nullity)
    for j, i in enumerate(free):
        equations[i, j] = 1
    for i, index in enumerate(pivots):
        for j in range(expected_nullity):
            equations[index, j] = coefficients[i, j]
    result = []
    for column in range(expected_nullity):
        values = equations.column(column).list()
        aa = [full.base_ring()(0)]+values[:len(products_a)-1]
        bb = values[len(products_a)-1:]
        numerator = sum(c*p for c, p in zip(aa, products_a))
        other = sum(c*p for c, p in zip(bb, products_b))
        # Remove imposed known orders before division. No root finding.
        ring = forms[0].parent()
        denominator_unit = ring(a2.list()[a_order:])
        laurent_unit = (ring(numerator.list()[a_min:]) * denominator_unit.inverse_series_trunc(64)).truncate(64)
        result.append({'numerator_coefficients': [precise.midpoint(c) for c in aa],
                       'other_numerator_coefficients': [precise.midpoint(c) for c in bb],
                       'laurent_shift': -pole_order,
                       'raw_coordinate_laurent_coefficients': [precise.midpoint(laurent_unit[i]) for i in range(64)],
                       'leading_numerator_coefficient': precise.midpoint(numerator[a_min]),
                       'leading_denominator_coefficient': precise.midpoint(a2[a_order])})
    info.update({'pivots': pivots, 'free': free, 'solve': solve,
                 'maps': result})
    return result, info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, default=DATA/'acb_refinement_16384.acb')
    parser.add_argument('--comparison', type=Path, default=DATA/'acb_refinement_12288.acb')
    parser.add_argument('--length', type=int, default=512)
    parser.add_argument('--training', type=int, default=256)
    parser.add_argument('--digits', type=int, default=80)
    parser.add_argument('--basis-gauge', choices=['arithmetic','flag'], default='arithmetic')
    parser.add_argument('--pole-orders', type=int, nargs='+', default=[16, 17, 18])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    mp.mp.dps = args.digits
    start = time.monotonic()
    forms, source = forms_from_source(args.basis, args.length, args.digits, args.basis_gauge)
    previous, old_source = forms_from_source(args.comparison, args.length, args.digits, args.basis_gauge)
    reports = []
    for pole in args.pole_orders:
        maps, current = recover_map(forms, pole, args.length, args.training)
        old_maps, old = recover_map(previous, pole, args.length, args.training, current)
        if pole > 16:
            _, alternate = recover_map(forms, pole, args.length, 121, current)
        else:
            alternate = None
        comparison = []
        for i, result in enumerate(maps):
            current_values = [mp.mpc(*z) for z in result['numerator_coefficients']]
            previous_values = [mp.mpc(*z) for z in old_maps[i]['numerator_coefficients']]
            alternate_values = [mp.mpc(*z) for z in alternate['maps'][i]['numerator_coefficients']]
            norm = mp.sqrt(mp.fsum(abs(z)**2 for z in current_values))
            comparison.append({'map_index': i,
                'cross_bank_coefficient_relative_difference': mp.nstr(mp.sqrt(mp.fsum(abs(a-b)**2 for a,b in zip(current_values, previous_values)))/norm,22),
                'same_bank_fit_coefficient_relative_difference': mp.nstr(mp.sqrt(mp.fsum(abs(a-b)**2 for a,b in zip(current_values, alternate_values)))/norm,22)})
        reports.append({'current': current, 'previous': old, 'alternate_fit': alternate, 'comparison': comparison})
        print('pole', pole, 'rank', current['observed_rank'], '/', current['expected_product_rank'], comparison, flush=True)
    report = {'status': 'numerical Riemann--Roch maps; no exact algebraic coefficients certified',
              'current_source': source, 'previous_source': old_source, 'maps': reports,
              'working_decimal_digits': args.digits, 'length': args.length, 'training': args.training,
              'wall_seconds': time.monotonic()-start,
              'limitations': ['field assertions require the exact canonical model, marked point and vanishing flag',
                             'dimensions and pole assertions have numerical rank support, not exact certification',
                             'arithmetic balls do not enclose geometric or truncation errors']}
    text = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(text)
    args.output.with_suffix('.out').write_text(text)


if __name__ == '__main__':
    main()
