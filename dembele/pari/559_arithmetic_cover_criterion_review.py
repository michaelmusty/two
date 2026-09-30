"""D134 independent review of the conditional arithmetic cover criterion.

Use integer denominator clearing and pseudo-remainders for the B3
identities, and a separate AST polynomial parser for the Hecke factors.
The missing marked-base identification remains an explicit hypothesis.
"""
import argparse
import ast
from fractions import Fraction as Q
import hashlib
import json
from math import lcm, prod
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'arithmetic_cover_criterion_review_d134.json'
PATHS, CACHE = {Path(__file__)}, {}
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


def checked(records):
    for row in records:
        assert source(row['path']) == row, row['path']


def read(stem):
    path = DATA / (stem+'.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet


def multiply(a, b):
    result = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def add(a, b, sign=1):
    out = [0]*max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += sign*value
    return out


def integral(row):
    values = list(map(Q, row))
    denominator = lcm(*(value.denominator for value in values))
    return [int(denominator*value) for value in values], denominator


def pseudo_remainder(coefficients, polynomial):
    result = list(coefficients)
    while result and result[-1] == 0:
        result.pop()
    while len(result) >= len(polynomial):
        shift = len(result)-len(polynomial)
        lead = result[-1]
        result = [polynomial[-1]*value for value in result]
        for j, value in enumerate(polynomial):
            result[shift+j] -= lead*value
        while result and result[-1] == 0:
            result.pop()
    return result


def identity(polynomial, factors, target, scalar=1):
    numerator, denominator = [scalar], 1
    for row in factors:
        value, den = integral(row)
        numerator = multiply(numerator, value)
        denominator *= den
    right, den = integral(target)
    difference = add([den*x for x in numerator], [denominator*x for x in right], -1)
    return not pseudo_remainder(difference, polynomial)


def polynomial_ast(node):
    if isinstance(node, ast.Constant):
        assert type(node.value) is int
        return [node.value]
    if isinstance(node, ast.Name):
        assert node.id == 'z'
        return [0, 1]
    if isinstance(node, ast.UnaryOp):
        assert isinstance(node.op, ast.USub)
        return [-x for x in polynomial_ast(node.operand)]
    assert isinstance(node, ast.BinOp)
    if isinstance(node.op, ast.Pow):
        assert isinstance(node.left, ast.Name) and node.left.id == 'z'
        assert isinstance(node.right, ast.Constant) and type(node.right.value) is int
        degree = node.right.value
        assert 0 <= degree <= 4
        return [0]*degree+[1]
    left, right = polynomial_ast(node.left), polynomial_ast(node.right)
    if isinstance(node.op, ast.Add):
        result = add(left, right)
    elif isinstance(node.op, ast.Sub):
        result = add(left, right, -1)
    else:
        assert isinstance(node.op, ast.Mult)
        result = multiply(left, right)
    assert len(result) <= 5
    return result


def finite(packet):
    fibre = read('cm_frame_B3_fiber')
    structure = read('cm_frame_B3_fiber_structure')
    legacy = read('cm_frame_B3_fiber_check')
    d, u = fibre['data'], structure['data']
    polynomial, _ = integral(d['nonic_coefficients'])
    assert len(polynomial) == 10 and polynomial[-1] > 0
    n2, d0, alpha = [d[key] for key in ('numerator_leading', 'denominator_value', 'unit')]
    s, lam, beta, ratio = [u[key] for key in (
        'squareclass_witness', 'parameter_slope', 'rational_parameter_unit', 'branch_ratio')]
    assert all(len(row) == 9 and any(Q(x) for x in row) for row in (n2, d0, alpha, s, lam, beta, ratio))
    results = [
        identity(polynomial, [d0, alpha], n2),
        identity(polynomial, [s, s], alpha, -3),
        identity(polynomial, [ratio, lam], s),
        identity(polynomial, [beta, lam, lam], alpha),
        identity(polynomial, [ratio, ratio], beta, -3)]
    assert all(results)
    changed = list(map(Q, alpha))
    changed[0] += 1
    assert not identity(polynomial, [d0, changed], n2)
    assert legacy['constant_C3_inertia_condition_passed'] and legacy['squareclass'] == -3
    assert fibre['base_residue_field_degree'] == packet['residue_degree_after_base_change'] == 9
    assert packet['base_field_degree_over_Q'] == 8
    assert packet['odd_degree_norm_identity_exponents'] == {'degree': 9, 'square_denominator_exponent': 4}
    assert packet['rational_coefficient_identities_checked'] == 45
    assert all(packet['exact_D77_fibre_identities_replayed'].values())
    log = DATA / 'f16_steinberg.out'
    source(log)
    block = log.read_text().split('R60|new orbits (charpoly of T_p31):', 1)[1].split(
        'R60|new charpoly(T_p31)', 1)[0]
    strings = re.findall(r'<4,\s*([^>]+)>', block)
    factors = [polynomial_ast(ast.parse(text.strip().replace('^', '**'), mode='eval').body) for text in strings]
    assert len(factors) == 4 and all(len(row) == 5 and row[-1] == 1 for row in factors)
    assert factors == packet['four_quartic_Hecke_factors']
    trace = [1]
    for row in factors:
        trace = multiply(trace, row)
    base = read('cm_frame_curve_verification')
    assert trace == packet['P16_coefficients_ascending'] == base['Hecke_trace_polynomial_coefficients_ascending']
    order = prod(sum(c*32**i for i, c in enumerate(row)) for row in factors)
    assert order == packet['canonical_Hecke_order_P16_at32'] == 1640801490553691915934375
    assert order % 2 == trace[0] % 2 == 1
    assert base['smoothness']['smooth_over_F31'] and not base['Shimura_identification_certified']
    for flag in ('candidate_Jacobian_order_proved_without_base_identification',
                 'marked_base_identification_proved', 'arithmetic_cover_identification_proved',
                 'global_cubic_or_Y_sections_constructed', 'field_polynomial_constructed'):
        assert not packet[flag]
    assert packet['canonical_Hecke_interpretation_is_required']
    assert packet['D77_conditional_scalar_twist_uniqueness_restored']
    assert packet['conditional_rational_branch_half_uniqueness']
    assert packet['historical_residual_image_verdicts_not_used']
    return {'independent_integer_polynomial_identities': 5, 'rational_coordinate_identities': 45,
            'corrupted_unit_rejected_independently': True,
            'Hecke_order_recomputed_as_product_of_four_quartic_values': order,
            'conditional_rational_branch_half_unique': True,
            'D77_conditional_scalar_twist_criterion_retained': True,
            'marked_base_and_canonical_Hecke_hypotheses_remain_required': True}


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        packet = read(OUT.stem)
        checked(packet['sources'])
        assert peak() <= 2*(1 << 30)
        print('PASS|559_ARITHMETIC_COVER_CRITERION_REVIEW', flush=True)
        return
    assert not OUT.exists()
    tick = time.monotonic()
    prior = read('dyadic_precision6400_review_d133')
    assert prior['independent_finite_review_complete'] and prior['column_precisions']['0'] == 6400
    checked(prior['sources'])
    stem = 'arithmetic_cover_criterion_d134'
    packet = read(stem)
    checked(packet['sources'])
    receipts = list(DATA.glob(stem+'_attempt*.job.json'))
    assert len(receipts) == 1
    path = receipts[0]
    PATHS.add(path)
    receipt = json.loads(path.read_text())
    assert receipt['status'] == 'pass' and receipt['exit_code'] == 0
    assert receipt['timeout_seconds'] == 180 and receipt['timeout_terminates_process_group']
    checked([receipt['driver'], receipt['log']]+receipt['sources'])
    driver = ROOT / 'dembele/pari/558_arithmetic_cover_criterion.py'
    assert receipt['command'] == ['python3', str(driver), '--output', stem]
    assert receipt['driver'] == source(driver)
    bindings = [json.loads(line.split('|', 1)[1]) for line in Path(receipt['log']['path']).read_text().splitlines()
                if line.startswith('PHASE_METADATA|')]
    assert bindings == [source(DATA / (stem+'.json'))]
    assert packet['peak_rss_bytes'] <= 2*(1 << 30)
    certificate = finite(packet)
    read('arithmetic_cover_criterion_sources_d134')
    PATHS.add(ROOT / 'dembele/certificates/arithmetic-twist-classification-d134.md')
    records = [source(path) for path in sorted(PATHS)]
    known = {row['path']: row['sha256'] for row in records}
    assert all(known[row['path']] == row['sha256'] for row in prior['sources'])
    assert peak() <= 2*(1 << 30)
    result = {
        'status': 'pass', 'milestone': 'D134', 'independent_finite_review_complete': True,
        'inherited_D133_hashes_preserved': len(prior['sources']), 'passing_input_jobs': 1,
        'failed_bounded_jobs': 0, 'certificates': certificate,
        'conditional_arithmetic_cover_criterion_reviewed': True,
        'actual_marked_base_identified': False, 'actual_arithmetic_cover_identified': False,
        'full_bank_precision_pi': 800, 'column_precisions': {'0': 6400, '1': 1600},
        'positive_exact_zero_proved': False, 'field_polynomial_constructed': False,
        'wall_seconds': time.monotonic()-tick, 'peak_rss_bytes': peak(), 'sources': records}
    with OUT.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print('D134_REVIEW_SOURCES|'+str(len(records)), flush=True)
    print('PASS|559_ARITHMETIC_COVER_CRITERION_REVIEW', flush=True)


if __name__ == '__main__':
    main()
