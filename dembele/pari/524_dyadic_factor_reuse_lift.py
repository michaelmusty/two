"""D127 lift a low-system solution using an existing half-precision factor.

If A*x0=b mod 2^m, solve A*d=(b-A*x0)/2^m mod 2^m with the same
factor, then x=x0+2^m*d satisfies A*x=b mod 2^(2m). Check every
original sparse equation at the higher precision; no larger factor is built.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
s = importlib.util.spec_from_file_location('streamed', ROOT / 'dembele/pari/516_dyadic_factor_and_map_controls.py')
c = importlib.util.module_from_spec(s)
s.loader.exec_module(c)
b, h, w = c.b, c.h, c.w


def original_groups(bits):
    targets, params, path = b.parameters(8 * bits)
    h.PATHS.add(path)
    groups = {}
    for e in range(174):
        for branch, child in enumerate(targets[e]):
            groups.setdefault(params[e][branch], []).append((e, child))
    return groups


def original_apply(values, groups, algebra):
    result = list(values)
    for pars, destinations in groups.items():
        block = b.coefficients(pars, 32, algebra)
        for e, child in destinations:
            result[e] = algebra.sub(result[e], algebra.mul(block, values[child]))
        del block
    return result


def build(P):
    assert P in (1600, 3200)
    bits, lower = P // 8, P // 16
    mask = (1 << lower) - 1
    rhs = [b.k.data(32, 2, bits, f'D127-lift-P{P}-state{e}') for e in range(174)]
    groups = original_groups(bits)
    algebra = b.Algebra(bits)
    factor = c.FactorReader(lower)
    times = []
    start = time.monotonic()
    reduced_rhs = [b.reduce(edge, mask) for edge in rhs]
    x0 = factor.solve(reduced_rhs, b.Algebra(lower))
    times.append({'operation': 'initial_lower_precision_solve', 'seconds': time.monotonic() - start})
    start = time.monotonic()
    applied = original_apply(x0, groups, algebra)
    residual = [algebra.sub(edge, y) for edge, y in zip(rhs, applied)]
    assert all(v & mask == 0 for edge in residual for row in edge for x in row for v in x)
    reduced_residual = [[[tuple(v >> lower for v in x) for x in row] for row in edge] for edge in residual]
    times.append({'operation': 'higher_precision_residual_and_exact_division', 'seconds': time.monotonic() - start})
    start = time.monotonic()
    delta = factor.solve(reduced_residual, b.Algebra(lower))
    answer = [[[tuple(u + (v << lower) for u, v in zip(x, d)) for x, d in zip(row, dr)]
               for row, dr in zip(edge, de)] for edge, de in zip(x0, delta)]
    assert factor.decoded_blocks == 2452
    factor.close()
    times.append({'operation': 'same_factor_correction_solve', 'seconds': time.monotonic() - start})
    start = time.monotonic()
    assert original_apply(answer, groups, algebra) == rhs
    times.append({'operation': 'complete_higher_precision_original_residual', 'seconds': time.monotonic() - start})
    known_checks = 0
    if P == 1600:
        direct = c.FactorReader(bits)
        expected = direct.solve(rhs, algebra)
        direct.close()
        assert expected == answer
        known_checks = 89088
    sha = hashlib.sha256()
    for edge in answer:
        sha.update(b.pack(edge, bits))
    return {'target_low_system_precision_pi': P, 'reused_factor_precision_pi': P // 2,
        'rhs_columns': 2, 'original_sparse_scalar_equations_checked': 89088,
        'residual_scalar_coefficients_divisible_by_2_power': 89088, 'exact_binary_divisor_exponent': lower,
        'factor_blocks_decoded_for_two_solves': 2452, 'maximum_decoded_factor_blocks_held': 1,
        'distinct_original_maps': len(groups), 'maximum_original_coefficient_blocks_held': 1,
        'known_full_precision_factor_scalar_comparisons': known_checks,
        'known_full_precision_factor_comparison_performed': P == 1600,
        'larger_factor_constructed': False, 'actual_harmonic_precision_increased': False,
        'all_answers_sha256': sha.hexdigest(), 'timings': times,
        'factor_read_decode_seconds_for_two_solves': factor.read_seconds,
        'complete_target_size_solve_costed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--precision', type=int, choices=(1600, 3200), required=True)
    args = parser.parse_args()
    out = DATA / f'dyadic_factor_reuse_P{args.precision}_d127.json'
    assert not out.exists()
    start = time.monotonic()
    certificate = build(args.precision)
    h.PATHS.update([Path(__file__), Path(c.__file__), Path(c.q.__file__), Path(w.__file__),
        Path(h.__file__), Path(b.__file__), Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY,
        Path(c.q.p.__file__), Path(c.q.p.f.__file__)])
    result = {'status': 'pass', 'milestone': 'D127', 'certificates': certificate,
        'wall_seconds': time.monotonic() - start, 'peak_rss_bytes': w.peak_rss(),
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|524_DYADIC_FACTOR_REUSE_LIFT', flush=True)
