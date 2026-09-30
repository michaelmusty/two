"""A scale-free pointed invariant and explicitly bounded field searches.

For the intrinsic base forms let A2=[tau^16]H14 and A3=[tau^16]H13.
J=A3^2/A2^3 is independent of the remaining scalar in tau. The D52
normalization gives J=G3^2/G2^3=1/(144*G2). It is conditionally in F,
but is neither a complete curve invariant nor an exact-model certificate.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

import mpmath as mp

HERE = Path(__file__).resolve().parent


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE/filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


precise = module('pointed_invariant_precise', '86_precise_quadrics.py')
recognition = module('pointed_invariant_recognition', '87_quadric_recognition.py')


def compute(path):
    source, provenance = precise.read_source(path, 32, 50)
    _, short, gauge = precise.arithmetic.arithmetic_change(
        source.tolist(), list(range(16)), [(16, 14, -1), (16, 13, 1)])
    g2, g3 = short[16, 14], short[16, 13]
    invariant = g3**2/g2**3
    if abs(invariant-1/(144*g2)) > mp.mpf('1e-60')*max(1, abs(invariant)):
        raise ArithmeticError('weight-one gauge is inconsistent')
    return invariant, {'source': provenance, 'gauge': gauge,
                       'G2': [mp.nstr(g2.real, 60), mp.nstr(g2.imag, 30)],
                       'J': [mp.nstr(invariant.real, 60), mp.nstr(invariant.imag, 30)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--basis', type=Path, required=True)
    parser.add_argument('--comparison', type=Path, required=True)
    parser.add_argument('--tolerance', default='1e-18')
    parser.add_argument('--heights', type=int, nargs='+', default=[4, 8, 16, 32, 64])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    mp.mp.dps = 80
    tolerance = mp.mpf(args.tolerance)
    if not 0 < tolerance < mp.mpf('1e-6') or min(args.heights) < 2:
        parser.error('require a tolerance between zero and 1e-6, and heights at least two')
    started = time.monotonic()
    value, current = compute(args.basis)
    previous, comparison = compute(args.comparison)
    results = []
    for degree, basis, default_height in recognition.field_bases('cosine'):
        for height in args.heights if degree == 8 else [default_height]:
            candidate = recognition.relation(value, basis, height, tolerance)
            if candidate:
                coefficients = candidate['relation']
                exact = -mp.fsum(a*b for a, b in zip(coefficients[:-1], basis))/coefficients[-1]
                candidate['comparison_absolute_residual'] = mp.nstr(abs(exact-previous), 30)
            results.append({'field_degree': degree, 'height': height, 'candidate': candidate})
    report = {'status': 'numerical pointed invariant; recognition is tentative',
              'formula': 'J=A3^2/A2^3=1/(144*G2)', 'current': current, 'comparison': comparison,
              'independent_absolute_difference': mp.nstr(abs(value-previous), 30),
              'empirical_absolute_tolerance': str(tolerance), 'guaranteed_input_digits': None,
              'field_basis': 'cosine integral basis as in script 87',
              'recognition': results, 'wall_seconds': time.monotonic()-started}
    output = json.dumps(report, indent=2, allow_nan=False)+'\n'
    args.output.write_text(output)
    args.output.with_suffix('.out').write_text(output)
    print('J:', current['J'])
    print('Independent absolute difference:', report['independent_absolute_difference'])
    print('Candidates:', sum(r['candidate'] is not None for r in results))


if __name__ == '__main__':
    main()
