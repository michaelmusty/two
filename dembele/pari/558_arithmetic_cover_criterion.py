"""D134 exact finite inputs for conditional arithmetic double-cover uniqueness.

Replay the normalized D77 B3 fibre and the odd canonical Hecke order.
No new base, marking, Jacobian order for the unidentified candidate,
geometric-cover identity, or field polynomial is inferred by the script.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PATHS, CACHE, VISITED = {Path(__file__)}, {}, set()
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    if path not in CACHE:
        h = hashlib.sha256()
        with path.open('rb') as stream:
            while raw := stream.read(1 << 20):
                h.update(raw)
        CACHE[path] = {'path': str(path), 'sha256': h.hexdigest()}
    return CACHE[path]


def verify_links(obj):
    # D77 has its own frozen certificate chain, separate from the dyadic
    # catalogue. Merge it by checking every recorded source recursively.
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj:
            path = Path(obj['path']).resolve()
            assert source(path)['sha256'] == obj['sha256'], str(path)
            if path.suffix == '.json' and path not in VISITED:
                VISITED.add(path)
                verify_links(json.loads(path.read_text()))
        else:
            for value in obj.values():
                verify_links(value)
    elif isinstance(obj, list):
        for value in obj:
            verify_links(value)


def read(stem, known=None):
    path = DATA / (stem + '.json')
    record = source(path)
    if known is not None:
        assert known[record['path']] == record['sha256']
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def convolution(a, b):
    result = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


class Field:
    def __init__(self, coefficients):
        self.poly = tuple(map(Q, coefficients))
        self.degree = len(self.poly)-1
        assert self.degree == 9 and self.poly[-1] == 1
        self.one = (Q(1),)+(Q(0),)*8
    def element(self, row):
        assert len(row) == 9
        return tuple(map(Q, row))
    def mul(self, a, b):
        out = convolution(a, b)
        for k in range(len(out)-1, 8, -1):
            for j, c in enumerate(self.poly[:-1]):
                out[k-9+j] -= out[k]*c
        return tuple(out[:9])
    def scale(self, a, coefficient):
        return tuple(coefficient*x for x in a)


def evaluate(coefficients, value):
    result = 0
    for c in reversed(coefficients):
        result = result*value+c
    return result


def quartic(text):
    out = [0]*5
    for term in text.replace(' ', '').replace('-', '+-').split('+'):
        if not term:
            continue
        match = re.fullmatch(r'([+-]?\d*)\*?z(?:\^(\d+))?', term)
        if match:
            coefficient, degree = match.groups()
            coefficient = -1 if coefficient == '-' else 1 if coefficient in ('', '+') else int(coefficient)
            degree = int(degree) if degree else 1
            assert 0 <= degree <= 4
            out[degree] += coefficient
        else:
            out[0] += int(term)
    assert out[-1] == 1
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = DATA / (args.output+'.json')
    assert not output.exists()
    tick = time.monotonic()
    prior = read('dyadic_staged_integration_review_d132')
    known = {row['path']: row['sha256'] for row in prior['sources']}
    fibre = read('cm_frame_B3_fiber')
    structure = read('cm_frame_B3_fiber_structure')
    checked = read('cm_frame_B3_fiber_check')
    cover = read('cm_frame_B3_rational_check')
    base = read('cm_frame_curve_verification')
    for packet in (fibre, structure, checked, cover, base):
        verify_links(packet)
    for name in ('cm-frame-B3-fiber.md', 'cm-frame-resolvent.md', 'd88-cubic-identification-shortcut-review.md'):
        source(ROOT / 'dembele/certificates' / name)
    assert checked['positive_job']['status'] == checked['negative_job']['status'] == 'pass'
    assert checked['positive_job']['exit_code'] == 0 and checked['negative_job']['exit_code'] != 0
    positive_log = Path(checked['positive_job']['log']['path']).read_text()
    negative_log = Path(checked['negative_job']['log']['path']).read_text()
    assert 'PASS|161_CM_FRAME_B3_FIBER_CHECK' in positive_log
    assert 'assert n2 eq d0*alpha' in negative_log
    assert fibre['base_residue_field_degree'] == 9 and structure['fiber_is_a_field']
    assert structure['fiber_degree_over_Q'] == checked['fiber_field_degree'] == 18
    assert checked['squareclass'] == -3 and checked['constant_C3_inertia_condition_passed']
    assert not checked['arithmetic_curve_or_half_identified']
    data, units = fibre['data'], structure['data']
    field = Field(data['nonic_coefficients'])
    n2, d0, alpha = [field.element(data[key]) for key in ('numerator_leading', 'denominator_value', 'unit')]
    s, lam, beta, ratio = [field.element(units[key]) for key in (
        'squareclass_witness', 'parameter_slope', 'rational_parameter_unit', 'branch_ratio')]
    assert all(any(row) for row in (n2, d0, alpha, s, lam, beta, ratio))
    identities = {
        'leading_unit': field.mul(d0, alpha) == n2,
        'squareclass_minus3': field.scale(field.mul(s, s), -3) == alpha,
        'parameter_ratio': field.mul(ratio, lam) == s,
        'rational_parameter_unit': field.mul(beta, field.mul(lam, lam)) == alpha,
        'rational_parameter_squareclass': field.scale(field.mul(ratio, ratio), -3) == beta}
    assert all(identities.values())
    changed = tuple(x+y for x, y in zip(alpha, field.one))
    assert field.mul(d0, changed) != n2
    assert field.scale(alpha, -3) == field.mul(field.scale(s, 3), field.scale(s, 3))
    assert pow(11, 2, 31) == (-3) % 31
    assert gcd(8, 9) == 1 and 9 == 2*4+1
    log = DATA / 'f16_steinberg.out'
    record = source(log)
    assert known[record['path']] == record['sha256']
    block = log.read_text().split('R60|new orbits (charpoly of T_p31):', 1)[1].split(
        'R60|new charpoly(T_p31)', 1)[0]
    factors = [quartic(poly) for poly in re.findall(r'<4,\s*([^>]+)>', block)]
    assert len(factors) == 4
    trace = [1]
    for factor in factors:
        trace = convolution(trace, factor)
    assert trace == base['Hecke_trace_polynomial_coefficients_ascending']
    order = evaluate(trace, 32)
    assert order == 1640801490553691915934375 and order % 2 == 1
    assert base['smoothness']['smooth_over_F31'] and base['smoothness']['genus'] == 16
    assert not base['Shimura_identification_certified']
    report = ROOT / 'dembele/certificates/arithmetic-twist-classification-d134.md'
    PATHS.add(report)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert peak <= 2*(1 << 30)
    result = {
        'status': 'pass', 'milestone': 'D134', 'kind': 'conditional_arithmetic_cover_criterion',
        'exact_D77_fibre_identities_replayed': identities, 'rational_coefficient_identities_checked': 45,
        'corrupted_unit_rejected': True, 'locally_split_minus3_twist_has_split_B3_fibre': True,
        'residue_degree_over_Q': 9, 'base_field_degree_over_Q': 8, 'residue_degree_after_base_change': 9,
        'odd_degree_norm_identity_exponents': {'degree': 9, 'square_denominator_exponent': 4},
        'four_quartic_Hecke_factors': factors, 'P16_coefficients_ascending': trace,
        'canonical_Hecke_order_P16_at32': order, 'canonical_Hecke_order_is_odd': True,
        'canonical_Hecke_interpretation_is_required': True,
        'candidate_Jacobian_order_proved_without_base_identification': False,
        'conditional_rational_branch_half_uniqueness': True,
        'D77_conditional_scalar_twist_uniqueness_restored': True,
        'marked_base_identification_proved': False, 'arithmetic_cover_identification_proved': False,
        'global_cubic_or_Y_sections_constructed': False, 'field_polynomial_constructed': False,
        'historical_residual_image_verdicts_not_used': True,
        'inherited_full_curve_divisor_and_jet_checks_not_rerun': True,
        'separate_D77_source_chain_merged_by_recursive_hash_checks': True,
        'legacy_linked_JSON_records_checked': len(VISITED),
        'references': [
            {'url': 'https://stacks.math.columbia.edu/tag/09EE', 'checked': '2026-09-29',
             'role': 'Characteristic-zero faithful inertia character; D77 supplies its application.'},
            {'url': 'https://stacks.math.columbia.edu/tag/0BFH', 'checked': '2026-09-29',
             'role': 'Etaleness of multiplication by an invertible integer on an abelian variety.'},
            {'url': 'https://stacks.math.columbia.edu/tag/03RP', 'checked': '2026-09-29',
             'role': 'Finite torsion group schemes; specialization and cover comparison are our deductions.'}],
        'wall_seconds': time.monotonic()-tick, 'peak_rss_bytes': peak,
        'sources': [source(path) for path in sorted(PATHS)]}
    with output.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)), flush=True)
    print('PASS|558_ARITHMETIC_COVER_CRITERION', flush=True)


if __name__ == '__main__':
    main()
