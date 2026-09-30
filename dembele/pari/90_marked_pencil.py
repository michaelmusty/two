"""Condition a canonical quadric pencil using its five marked coefficient zeros.

Enumerate all 60 ordered markings of three points by 0,infinity,1. Compare
the remaining points across truncations and fits before bounded arithmetic
recognition. Error estimates are empirical, including the optional estimate
from three equally spaced truncations; none is a certified enclosure.
"""
import argparse
import hashlib
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from scipy.linalg import qr, svdvals

HERE = Path(__file__).resolve().parent
DATA = HERE.parent/'data/computed'
spec = importlib.util.spec_from_file_location('marked_pencil_lattice', HERE/'89_quadric_lattice.py')
lattice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lattice)


def decimal(z, digits=55):
    return [mp.nstr(mp.re(z), digits), mp.nstr(mp.im(z), digits)]


def determinant(a, b):
    return a[0]*b[1]-a[1]*b[0]


def reconstruct_pencil(quotient, rank, gauge=None, allow_noisy=False, training=None):
    """Recover a two-dimensional kernel; all rows check the interpolated fit."""
    if quotient.cols != rank+2 or quotient.rows < rank:
        raise ValueError('expected a two-dimensional pencil')
    numeric = np.array(quotient.tolist(), complex)
    norms = np.linalg.norm(numeric, axis=0)
    if not np.isfinite(numeric).all() or min(norms) == 0:
        raise ValueError('nonfinite or zero product column')
    singular = svdvals(numeric/norms)
    observed = int(sum(singular > singular[0]*1e-12))
    tail = singular[rank]/singular[0]
    gap = singular[rank-1]/max(singular[rank], np.finfo(float).tiny)
    if observed != rank and not (allow_noisy and observed > rank and tail < 1e-6 and gap > 1e6):
        raise ValueError(f'product rank {observed}, expected {rank}')
    if gauge is None:
        training = quotient.rows if training is None else training
        if not rank <= training <= quotient.rows:
            raise ValueError('invalid interpolation window')
        _, _, order = qr(numeric[:training, :].T, mode='economic', pivoting=True)
        rows = [int(i) for i in order[:rank]]
        _, _, order = qr(numeric[rows, :], mode='economic', pivoting=True)
        pivots = [int(i) for i in order[:rank]]
        free = [i for i in range(quotient.cols) if i not in pivots]
        gauge = {'rows': rows, 'pivots': pivots, 'free': free}
    rows, pivots, free = (gauge[k] for k in ['rows', 'pivots', 'free'])
    left = mp.matrix([[quotient[i, j] for j in pivots] for i in rows])
    right = mp.matrix([[quotient[i, j] for j in free] for i in rows])
    fit = left**-1*right
    equations = mp.matrix(quotient.cols, 2)
    for i, j in enumerate(free):
        equations[j, i] = 1
    for i, j in enumerate(pivots):
        for k in range(2):
            equations[j, k] = -fit[i, k]
    residual = mp.norm(quotient*equations)/(mp.norm(quotient)*mp.norm(equations))
    return equations, gauge, {
        'selected_product_rank': rank, 'observed_rank_at_1e_12': observed,
        'noisy_reference_rank_truncated': observed != rank,
        'relative_singular_tail': float(tail), 'singular_gap_after_selected_rank': float(gap),
        'scaled_singular_values': singular.tolist(),
        'interpolation_condition_double': float(np.linalg.cond(numeric[np.ix_(rows, pivots)])),
        'all_constraint_relative_residual': mp.nstr(residual, 20),
        'constraints_fitted': len(rows), 'constraints_checked': quotient.rows}


def marked_values(lines, triple):
    """Covector i cuts out the marked point (b_i:-a_i) of the pencil."""
    if len(set(triple)) != 3:
        raise ValueError('three distinct markings are required')
    for i, j in combinations(range(len(lines)), 2):
        if determinant(lines[i], lines[j]) == 0:
            raise ValueError('marked coefficient zeros coincide')
    a, b, c = triple
    remaining = [i for i in range(len(lines)) if i not in triple]
    values = [determinant(lines[j], lines[a])*determinant(lines[c], lines[b]) /
              (determinant(lines[j], lines[b])*determinant(lines[c], lines[a])) for j in remaining]
    return remaining, values


def normalize_pencil(equations, mark_rows, triple):
    """Fix a pencil basis by the marked roots and one coefficient equal to 1.

    z=k*ell_a/ell_b sends their zeros a,b,c to 0,infinity,1.
    E*U^-1 is unchanged by an arbitrary GL2 change of the input pencil.
    No change of the sixteen ambient canonical coordinates is made here.
    """
    lines = [[equations[i, j] for j in range(2)] for i in mark_rows]
    remaining, values = marked_values(lines, triple)
    a, b, c = triple
    k = determinant(lines[b], lines[c])/determinant(lines[a], lines[c])
    transform = mp.matrix([[k*z for z in lines[a]], lines[b]])
    return equations*transform**-1, remaining, values


def chordal(x, y):
    """Chordal distance on P1, with None denoting infinity."""
    if x is None and y is None:
        return mp.mpf(0)
    if x is None:
        return 1/mp.sqrt(1+abs(y)**2)
    if y is None:
        return 1/mp.sqrt(1+abs(x)**2)
    return abs(x-y)/mp.sqrt((1+abs(x)**2)*(1+abs(y)**2))


def orbit_key(triple, target):
    a, b, c = triple
    # Klein four symmetries give the same cross-ratio. There are 30
    # expressions among the 120 displayed coordinates, not 120 independent tests.
    return min((a, b, c, target), (b, a, target, c),
               (c, target, a, b), (target, c, b, a))


def cross_ratio_matrix(key):
    """Integer Mobius matrix relative to the sorted four-point marking."""
    a, b, c, d = key
    labels = sorted(key)
    variants = [(a, b, c, d), (b, a, d, c), (c, d, a, b), (d, c, b, a)]
    chosen = next(v for v in variants if v[-1] == labels[-1])
    order = tuple(labels.index(i) for i in chosen[:3])
    return {(0, 1, 2): (1, 0, 0, 1), (0, 2, 1): (1, 0, 1, -1),
            (1, 0, 2): (0, 1, 1, 0), (1, 2, 0): (0, 1, -1, 1),
            (2, 0, 1): (1, -1, 1, 0), (2, 1, 0): (-1, 1, 0, 1)}[order]


def canonical_cross_ratio(key, value):
    a, b, c, d = cross_ratio_matrix(key)
    return (d*value-b)/(a-c*value)


def marked_cross_ratio(key, canonical):
    a, b, c, d = cross_ratio_matrix(key)
    return (a*canonical+b)/(c*canonical+d)


def audit_candidates(previous, current_entries):
    """Deduplicate earlier hits exactly over F and compare all six charts.

    Failure is numerical incompatibility at the stated empirical accuracy,
    not a proof of non-equality to the unknown exact curve invariant.
    """
    from sage.all import QQ, NumberField, PolynomialRing
    ring = PolynomialRing(QQ, 'x')
    x = ring.gen()
    field = NumberField(x**8-8*x**6+20*x**4-16*x**2+2, 'b')
    b = field.gen()
    generators = {2: (2-b*b)**2-2, 4: 2-b*b, 8: b}
    bases = {1: [field(1)]}
    for degree, generator in generators.items():
        basis, before, now = [field(1)], field(2), generator
        for _ in range(1, degree):
            basis.append(now)
            before, now = now, generator*now-before
        bases[degree] = basis
    grouped = {}
    for search in previous['recognition']:
        key = tuple(search['cross_ratio_orbit'])
        for trial in search['trials']:
            hit = trial['candidate']
            if not hit:
                continue
            relation = hit['relation']
            exact = -sum(a*z for a, z in zip(relation[:-1], bases[trial['field_degree']]))/relation[-1]
            canonical = canonical_cross_ratio(key, exact)
            identity = (tuple(sorted(key)), tuple(canonical))
            group = grouped.setdefault(identity, {'canonical': canonical, 'origins': []})
            group['origins'].append({'cross_ratio_orbit': list(key), 'field_degree': trial['field_degree'],
                                     'height_bound': trial['height_bound'], 'relation': relation})
    b_numeric = 2*mp.cos(7*mp.pi/16)
    reports = []
    for (labels, _), group in grouped.items():
        canonical = group['canonical']
        numeric = mp.fsum(mp.mpf(str(q.numerator()))/mp.mpf(str(q.denominator()))*b_numeric**i
                          for i, q in enumerate(canonical))
        checks = []
        for key, (entry, value, _, _, _) in sorted(current_entries.items()):
            if tuple(sorted(key)) != labels:
                continue
            predicted = marked_cross_ratio(key, numeric)
            error = abs(predicted-value)
            tolerance = mp.mpf(entry['accuracy']['exploratory_absolute_tolerance'])
            checks.append({'cross_ratio_orbit': list(key), 'absolute_residual': mp.nstr(error, 22),
                           'empirical_tolerance': str(tolerance),
                           'residual_divided_by_tolerance': mp.nstr(error/tolerance, 20),
                           'within_current_tolerance': error <= tolerance})
        consistent = bool(checks) and all(c['within_current_tolerance'] for c in checks)
        reports.append({'four_point_labels': list(labels),
                        'exact_candidate_coordinates_in_power_basis': [str(q) for q in canonical],
                        'origins': group['origins'], 'current_chart_checks': checks,
                        'consistent_with_current_accuracy': consistent,
                        'status': 'tentative candidate only' if consistent else 'incompatible with current empirical accuracy'})
    return reports


def accuracy(current, alternate, previous, older=None):
    fit = abs(current-alternate)
    late = abs(current-previous)
    early = abs(previous-older) if older is not None else None
    ratio = late/early if early else None
    tail = late*ratio/(1-ratio) if ratio is not None and ratio < mp.mpf('.5') else None
    # A geometric estimate is only a discovery diagnostic, not a theorem
    # about convergence. If it is unavailable, retain the coarser bank change.
    estimated = max(fit, abs(current.imag), tail if tail is not None else late)
    floor = mp.mpf(10)**(-mp.mp.dps+20)
    tolerance = mp.mpf(10)**mp.ceil(mp.log10(10*max(estimated, floor)))
    return {'same_bank_fit_absolute_difference': mp.nstr(fit, 20),
            'independent_bank_absolute_difference': mp.nstr(late, 20),
            'previous_bank_absolute_difference': mp.nstr(early, 20) if early is not None else None,
            'successive_difference_ratio': mp.nstr(ratio, 20) if ratio is not None else None,
            'geometric_tail_estimate': mp.nstr(tail, 20) if tail is not None else None,
            'imaginary_absolute_value': mp.nstr(abs(current.imag), 20),
            'exploratory_absolute_tolerance': mp.nstr(tolerance, 10),
            'tolerance_basis': '10 times largest of fit discrepancy, imaginary part, and empirical tail estimate; rounded up',
            'certified_input_error_bound': None}


def source_n(report):
    source = Path(report['source']['path']).with_suffix('.json')
    return int(json.loads(source.read_text())['n'])


def direct_products(report, pairs, basis_gauge='arithmetic'):
    """Use script 86's native products before its full-quadric interpolation."""
    native_spec = importlib.util.spec_from_file_location('marked_pencil_precise', HERE/'86_precise_quadrics.py')
    precise = importlib.util.module_from_spec(native_spec)
    native_spec.loader.exec_module(precise)
    from sage.all import ComplexBallField, RealBallField, PolynomialRing, matrix
    training = len(report['solve']['interpolation_rows'])+report['solve']['unused_training_rows']
    length = training+report['solve']['held_out_rows']
    source, provenance = precise.read_source(Path(report['source']['path']), length, 50)
    if basis_gauge == 'arithmetic':
        change, _, gauge = precise.arithmetic.arithmetic_change(
            source.tolist(), list(range(16)), [(16, 14, -1), (16, 13, 1)])
    elif basis_gauge == 'flag':
        # Only the vanishing flag is needed for the leading coefficient
        # zero points. Arbitrary nonzero diagonal balancing preserves them.
        jets = mp.matrix([[source[i, j] for j in range(16)] for i in range(16)])
        change = jets**-1
        transformed_mp = source*change
        scales = [1/mp.sqrt(mp.fsum(abs(transformed_mp[n, j])**2 for n in range(length))) for j in range(16)]
        change = change*mp.diag(scales)
        gauge = {'source_jets_for_flag': 16, 'column_balancing': 'unit coefficient norm over the fitted window',
                 'basis_is_asserted_F_defined': False,
                 'invariant_field_claim': 'cross-ratios depend only on the F-defined vanishing flag and relation space'}
    else:
        raise ValueError('unknown canonical basis gauge')
    bits = int(mp.ceil(mp.mp.dps*mp.log(10, 2)))+32
    field, reals = ComplexBallField(bits), RealBallField(bits)
    def ball(z):
        return field(reals(mp.nstr(z.real, mp.mp.dps)), reals(mp.nstr(z.imag, mp.mp.dps)))
    transformed = matrix(field, [[ball(z) for z in row] for row in source.tolist()]) * \
        matrix(field, [[ball(z) for z in row] for row in change.tolist()])
    ring = PolynomialRing(field, 'u')
    forms = [ring(transformed.column(i).list()) for i in range(16)]
    products = [(forms[i]*forms[j]).truncate(length) for i, j in pairs]
    numeric = mp.matrix([[mp.mpc(*precise.midpoint(p[n])) for p in products] for n in range(length)])
    return numeric, training, {'native_source': provenance, 'training_jets': training,
                              'product_jets': length, 'basis_gauge_kind': basis_gauge, 'basis_gauge': gauge,
                              'product_arithmetic_ball_bits': bits,
                              'ball_interpretation': 'arithmetic on supplied point data, not a geometric enclosure'}


def load_pencils(paths, method='quotient', basis_gauge='arithmetic'):
    reports = [json.loads(p.read_text()) for p in paths]
    for report in reports[1:]:
        for key in ['pivots', 'free', 'monomial_pairs']:
            if report[key] != reports[0][key]:
                raise ValueError('incompatible canonical coordinate or monomial normalizations')
    pairs = reports[0]['monomial_pairs']
    selected = [i for i, pair in enumerate(pairs) if sum(pair) >= 22]
    marks = [i for i, index in enumerate(selected) if sum(pairs[index]) == 22]
    if len(selected) != 25 or len(marks) != 5:
        raise ValueError('expected the genus-sixteen weight-22 pencil')
    pencils, details, gauge = [], [], None
    for index, (path, report) in enumerate(zip(paths, reports)):
        extra = {}
        if method == 'direct':
            quotient, training, extra = direct_products(report, [pairs[i] for i in selected], basis_gauge)
            pencil, used_gauge, info = reconstruct_pencil(quotient, 23, allow_noisy=index >= 2, training=training)
            extra['interpolation_gauge'] = used_gauge
        else:
            quotient = lattice.quotient_map(report)
            quotient = mp.matrix([[quotient[i, j] for j in selected] for i in range(quotient.rows)])
            pencil, gauge, info = reconstruct_pencil(quotient, 23, gauge, allow_noisy=index >= 2)
        info.update(extra)
        info.update({'source': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'analytic_truncation_n': source_n(report),
                     'pencil_coefficients': [[decimal(pencil[i, j]) for j in range(2)] for i in range(pencil.rows)],
                     'marked_covectors': [[decimal(pencil[i, j]) for j in range(2)] for i in marks]})
        pencils.append(pencil)
        details.append(info)
    return pencils, details, gauge, marks, [pairs[i] for i in selected]


def recognize(value, alternate, previous, errors, heights):
    tolerance = mp.mpf(errors['exploratory_absolute_tolerance'])
    if tolerance >= mp.mpf('1e-8'):
        return {'status': 'insufficient empirical accuracy for this bounded search', 'trials': []}
    trials = []
    for degree, basis, default in lattice.fields.field_bases('cosine'):
        for height in heights if degree == 8 else [default]:
            candidate = lattice.fields.relation(value, basis, height, tolerance)
            if candidate:
                coefficients = candidate['relation']
                recognized = -mp.fsum(a*b for a, b in zip(coefficients[:-1], basis))/coefficients[-1]
                alternate_error, previous_error = abs(recognized-alternate), abs(recognized-previous)
                candidate.update({'alternate_fit_absolute_residual': mp.nstr(alternate_error, 20),
                                  'previous_bank_absolute_residual': mp.nstr(previous_error, 20),
                                  'alternate_fit_within_tolerance': alternate_error <= tolerance,
                                  'previous_bank_within_measured_change': previous_error <=
                                  2*mp.mpf(errors['independent_bank_absolute_difference'])+tolerance})
            trials.append({'field_degree': degree, 'height_bound': height, 'candidate': candidate})
    return {'status': 'numerical discovery only; no algebraic equality certified', 'trials': trials}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, default=DATA/'precise_quadrics_16384.json')
    parser.add_argument('--alternate', type=Path, default=DATA/'precise_quadrics_16384_shortfit.json')
    parser.add_argument('--comparison', type=Path, default=DATA/'precise_quadrics_12288.json')
    parser.add_argument('--older', type=Path, default=DATA/'precise_quadrics_8192.json')
    parser.add_argument('--digits', type=int, default=80)
    parser.add_argument('--method', choices=['quotient', 'direct'], default='direct')
    parser.add_argument('--basis-gauge', choices=['arithmetic', 'flag'], default='arithmetic')
    parser.add_argument('--heights', type=int, nargs='+', default=[4, 8, 16, 32])
    parser.add_argument('--skip-recognition', action='store_true')
    parser.add_argument('--best-only', action='store_true', help='recognize only the two coordinates of the best-ranked chart')
    parser.add_argument('--audit-candidates', type=Path, help='check hits from an earlier script-90 report against this reconstruction')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.digits < 50 or min(args.heights) < 2:
        parser.error('require at least 50 arithmetic digits and heights at least two')
    if args.method == 'quotient' and args.basis_gauge != 'arithmetic':
        parser.error('the saved quotient reports use the arithmetic basis')
    mp.mp.dps = args.digits
    started = time.monotonic()
    pencils, details, gauge, marks, pairs = load_pencils(
        [args.basis, args.alternate, args.comparison, args.older], args.method, args.basis_gauge)
    counts = [d['analytic_truncation_n'] for d in details]
    if not counts[0] == counts[1] or not counts[0]-counts[2] == counts[2]-counts[3] > 0:
        raise ValueError('tail diagnostic requires two current fits and three equally spaced truncations')
    normalizations, unique = [], {}
    for triple in permutations(range(5), 3):
        normalized = [normalize_pencil(p, marks, triple) for p in pencils]
        remaining, values = normalized[0][1:]
        points = [mp.mpf(0), None, mp.mpf(1)]+values
        separation = min(chordal(a, b) for a, b in combinations(points, 2))
        fit_error = max(chordal(a, b) for a, b in zip(values, normalized[1][2]))
        bank_error = max(chordal(a, b) for a, b in zip(values, normalized[2][2]))
        entries = []
        for j, target in enumerate(remaining):
            value, alt, prev, old = [n[2][j] for n in normalized]
            errors = accuracy(value, alt, prev, old)
            key = orbit_key(triple, target)
            entry = {'point': target, 'cross_ratio_orbit': list(key), 'value': decimal(value), 'accuracy': errors}
            entries.append(entry)
            if key not in unique:
                unique[key] = (entry, value, alt, prev, tuple(triple))
        normalizations.append({'zero_infinity_one': list(triple), 'remaining_coordinates': entries,
                               'minimum_chordal_separation': mp.nstr(separation, 20),
                               'same_bank_chordal_error': mp.nstr(fit_error, 20),
                               'cross_bank_chordal_error': mp.nstr(bank_error, 20),
                               'same_bank_error_divided_by_separation': mp.nstr(fit_error/separation, 20),
                               'cross_bank_error_divided_by_separation': mp.nstr(bank_error/separation, 20)})
    normalizations.sort(key=lambda n: (mp.mpf(n['same_bank_error_divided_by_separation']),
                                       mp.mpf(n['cross_bank_error_divided_by_separation']), n['zero_infinity_one']))
    best = normalizations[0]
    best_equations = normalize_pencil(pencils[0], marks, best['zero_infinity_one'])[0]
    searches = []
    best_keys = {tuple(e['cross_ratio_orbit']) for e in best['remaining_coordinates']}
    if not args.skip_recognition:
        for key, (entry, value, alt, prev, triple) in sorted(unique.items()):
            if args.best_only and key not in best_keys:
                continue
            search = recognize(value, alt, prev, entry['accuracy'], args.heights)
            searches.append({'cross_ratio_orbit': list(key), 'zero_infinity_one': list(triple),
                             **entry, **search})
    hits = sum(t['candidate'] is not None for s in searches for t in s['trials'])
    report = {'status': 'marked numerical pencil; no exact arithmetic model certified',
              'working_decimal_digits': args.digits, 'reconstruction_method': args.method,
              'canonical_basis_gauge': args.basis_gauge,
              'inputs': details, 'pencil_gauge': gauge,
              'monomial_pairs': pairs, 'marked_monomials': [pairs[i] for i in marks],
              'normalization_count': len(normalizations), 'distinct_cross_ratio_expressions': len(unique),
              'ranking': 'current fit chordal error / minimum marked-point separation; cross-bank error breaks ties',
              'normalizations': normalizations, 'best_zero_infinity_one': best['zero_infinity_one'],
              'best_normalized_pencil': [[decimal(best_equations[i, j]) for j in range(2)] for i in range(len(pairs))],
              'recognition': searches, 'positive_height_trials': hits,
              'recognition_scope': 'two best-chart coordinates' if args.best_only else 'all 30 cross-ratio expressions',
              'recognition_field_basis': 'cosine integral basis, b=2*cos(7*pi/16); script 87 subfield bases',
              'limitations': ['cross-ratio field assertions require an F-rational marking, the true differential space, the vanishing flag and pencil rank',
                              'complex flag-basis pencil coefficients are not asserted to lie in F',
                              'geometric tail prediction is empirical, not a certified input error bound',
                              'the 60 markings are rationally related and are not independent arithmetic evidence',
                              'pencil normalization fixes GL2 freedom, not the ambient GL16 canonical coordinates'],
              'wall_seconds': time.monotonic()-started}
    if args.audit_candidates:
        earlier = json.loads(args.audit_candidates.read_text())
        if earlier['marked_monomials'] != report['marked_monomials']:
            raise ValueError('candidate audit has different marked monomials')
        report['candidate_audit'] = {'source': str(args.audit_candidates),
                                     'sha256': hashlib.sha256(args.audit_candidates.read_bytes()).hexdigest(),
                                     'candidates': audit_candidates(earlier, unique)}
    report['wall_seconds'] = time.monotonic()-started
    output = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(output)
    args.output.with_suffix('.out').write_text(output)
    print('Normalizations:', len(normalizations), 'distinct expressions:', len(unique))
    print('Best zero,infinity,one:', best['zero_infinity_one'])
    for entry in best['remaining_coordinates']:
        print('Point', entry['point'], entry['value'], entry['accuracy'])
    print('Positive recognition height trials:', hits)
    if 'candidate_audit' in report:
        for candidate in report['candidate_audit']['candidates']:
            print('Earlier candidate:', candidate['status'])


if __name__ == '__main__':
    main()
