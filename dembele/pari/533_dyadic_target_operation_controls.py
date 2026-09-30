"""D130 capped individual original-map actions and schedule-shape controls.

One child and one backend per job. Full/RHS/correction inputs are dense
synthetic data; extension inputs are certified old column-0 rows with exact
masses. Target output is a control residue, never a new harmonic column.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
spec = importlib.util.spec_from_file_location('streamed', ROOT / 'dembele/pari/516_dyadic_factor_and_map_controls.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
q, h, b, a, w = c.q, c.h, c.b, c.a, c.w
SEEDS = {800: 'dyadic_staged_P800_col00_verified_d123',
         1600: 'dyadic_weighted_P1600_col00_verified_d124',
         3200: 'dyadic_streamed_P3200_col00_verified_d129'}


def controls():
    packet, _ = h.read('dyadic_adaptive_kernel_control_d124')
    for path in (Path(a.__file__), a.CSOURCE, a.LIBRARY):
        expected = [row for row in packet['sources'] if Path(row['path']) == path]
        assert len(expected) == 1 and h.source(path) == expected[0]
        h.PATHS.add(path)


def composed_cm(index, branch, P, ring):
    packet, path = h.read('dyadic_target_transports_d121')
    charts = [x for x in packet['CM_charts'] if x['chart'] == 'A']
    assert len(charts) == 17 and 0 <= index < 17
    chart = charts[index]
    child = packet['transitions'][chart['target_edge']]['children'][branch]
    assert chart['CM_index'] == index and min(chart['normalized_error_pi'], child['normalized_error_pi']) >= P
    A, B, C = [tuple(int(v) & ring.mask for v in x) for x in chart['normalized_center'][:3]]
    av, bv, cv = [tuple(int(v) & ring.mask for v in x) for x in child['normalized_center'][:3]]
    d = ring.add(b.ONE, ring.mul(C, bv))
    inverse = b.ONE
    two = (2,) + (0,) * 7
    for _ in range(P.bit_length()):
        inverse = ring.mul(inverse, ring.add(two, ring.neg(ring.mul(d, inverse))))
    assert ring.mul(d, inverse) == b.ONE
    pars = (ring.mul(ring.add(ring.mul(A, av), ring.mul(B, cv)), inverse),
            ring.mul(ring.add(ring.mul(A, bv), B), inverse),
            ring.mul(ring.add(cv, ring.mul(C, av)), inverse))
    assert ring.mul(d, pars[0]) == ring.add(ring.mul(A, av), ring.mul(B, cv))
    assert ring.mul(d, pars[1]) == ring.add(ring.mul(A, bv), B)
    assert ring.mul(d, pars[2]) == ring.add(cv, ring.mul(C, av))
    delta = ring.add(pars[0], ring.neg(ring.mul(pars[1], pars[2])))
    parent_delta = ring.add(A, ring.neg(ring.mul(B, C)))
    child_delta = ring.add(av, ring.neg(ring.mul(bv, cv)))
    assert ring.mul(ring.mul(d, d), delta) == ring.mul(parent_delta, child_delta)
    h.PATHS.add(path)
    return child['target_edge'], pars


def build(args):
    controls()
    P, mode = args.precision, args.mode
    assert P % 8 == 0 and 800 <= P <= 10552 and args.branch in (0, 1)
    assert 0 <= args.state < (17 if mode == 'cm' else 174)
    u = args.lower if mode in ('correction', 'correction-rhs') else 0
    assert 0 <= u < P - 33
    shift, bitcount = u // 8, P // 8 - u // 8
    ring = (a.Ring if args.backend == 'ADAPTIVE' else q.p.Ring)(bitcount)
    targets, params, path = b.parameters(P)
    h.PATHS.add(path)
    if mode == 'cm':
        child, pars = composed_cm(args.state, args.branch, P, ring)
    else:
        child = targets[args.state][args.branch]
        pars = tuple(tuple(v & ring.mask for v in x) for x in params[args.state][args.branch])
    count = args.seed if mode == 'extend' else P - u
    rows = 33 if mode in ('rhs', 'correction-rhs') else max(33, P - u - 33) if mode == 'correction' else 2 * P if mode == 'cm' else P
    assert 1 <= count <= 8 * bitcount and rows > 0
    if mode == 'extend':
        assert args.seed in SEEDS and args.seed < P
        packet, _ = h.read(SEEDS[args.seed])
        assert packet['certificate']['original_full_residual_zero']
        source = q.StateReader(packet['state_file'], args.seed, args.seed // 8)
        values = source.row(child)
        source.close()
        mass, _ = h.read('dyadic_harmonic_certificate_d111')
        values[0] = (mass['harmonic_basis'][0][child] & ring.mask,) + (0,) * 7
        kind = 'actual_old_column0_canonical_lift_with_exact_mass'
    else:
        values = b.k.data(1, count, bitcount, f'D130-input-P{P}-u{u}-child{child}')[0]
        if mode in ('rhs', 'correction-rhs'):
            values[1:33] = [b.ZERO] * min(32, count - 1)
        if mode in ('correction', 'correction-rhs'):
            values[0] = b.ZERO
        kind = 'deterministic_dense_synthetic'
    delta = ring.add(pars[0], ring.neg(ring.mul(pars[1], pars[2])))
    cv, dv = q.l.value([[pars[2]]], 8 * bitcount), q.l.value([[delta]], 8 * bitcount)
    assert cv >= 1 and dv >= 1
    tick = time.monotonic()
    plan = q.l.Plan(ring, *pars, count, rows)
    prepare = time.monotonic() - tick
    tick = time.monotonic()
    answer = plan.apply(values)
    apply = time.monotonic() - tick
    assert len(answer) == rows and answer[0] == values[0]
    cache = sum(map(len, plan.cache.values()))
    del plan
    print('TARGET_ACTION|' + json.dumps({'mode': mode, 'P': P, 'state': args.state,
          'branch': args.branch, 'backend': args.backend, 'bits': bitcount,
          'count': count, 'rows': rows, 'prepare_seconds': prepare, 'apply_seconds': apply}), flush=True)
    # All outputs at the first 25 binary digits must match a separately
    # prepared smaller action. Divisibility permits dropping inputs >=200.
    checkbits, checkcount, checkrows = min(25, bitcount), min(count, 200), min(rows, 200)
    small = q.p.Ring(checkbits)
    tick = time.monotonic()
    expected = q.l.Plan(small, *[tuple(v & small.mask for v in x) for x in pars], checkcount, checkrows).apply(
        [tuple(v & small.mask for v in x) for x in values[:checkcount]])
    assert [tuple(v & small.mask for v in x) for x in answer[:checkrows]] == expected
    low_seconds = time.monotonic() - tick
    raw = b.pack([answer], bitcount)
    binary = DATA / (args.output + '.bin')
    with binary.open('xb') as file:
        assert file.write(raw) == len(raw)
    output = h.source(binary)
    return {'working_precision_pi': P, 'mode': mode, 'state_or_CM_index': args.state,
        'branch': args.branch, 'target_child_state': child, 'backend': args.backend,
        'input_kind': kind, 'seed_precision_pi': args.seed if mode == 'extend' else None,
        'known_lower_valuation_pi': u, 'binary_shift': shift, 'modulus_bits': bitcount,
        'input_moment_count': count, 'output_moment_count': rows,
        'c_valuation_pi': cv, 'delta_valuation_pi': dv,
        'prepare_seconds': prepare, 'apply_seconds': apply, 'small_overlap_seconds': low_seconds,
        'small_precision_overlap_scalars': checkrows * 8, 'small_precision_bits': checkbits,
        'cached_polynomial_coefficient_count': cache,
        'GMP_wrapper_maximum_packed_product_bytes': ring.maximum_packed_bytes if args.backend == 'GMP' else None,
        'output_bytes': len(raw), 'answer': output,
        'input_sha256': hashlib.sha256(b.pack([values], bitcount)).hexdigest(),
        'parameters_sha256': hashlib.sha256(b.pack([pars], bitcount)).hexdigest(),
        'complete_state_or_chart_equation_checked': False,
        'actual_harmonic_precision_increased': False,
        'complete_target_size_solve_costed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--precision', type=int, default=10552)
    parser.add_argument('--mode', choices=('full', 'rhs', 'extend', 'correction', 'correction-rhs', 'cm'), required=True)
    parser.add_argument('--state', type=int, required=True)
    parser.add_argument('--branch', type=int, required=True)
    parser.add_argument('--backend', choices=('ADAPTIVE', 'GMP'), required=True)
    parser.add_argument('--seed', type=int, default=3200)
    parser.add_argument('--lower', type=int, default=0)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists() and not out.with_suffix('.bin').exists()
    begin = time.monotonic()
    cert = build(args)
    h.PATHS.update([Path(__file__), Path(c.__file__), Path(q.__file__), Path(h.__file__),
        Path(b.__file__), Path(w.__file__), Path(a.__file__), a.CSOURCE, a.LIBRARY,
        Path(q.l.__file__), Path(q.p.__file__), Path(q.p.g.__file__), Path(q.p.f.__file__),
        Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY])
    result = {'status': 'pass', 'milestone': 'D130', 'certificates': cert,
        'wall_seconds': time.monotonic() - begin, 'peak_rss_bytes': w.peak_rss(),
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(h.source(out)), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|533_DYADIC_TARGET_OPERATION_CONTROLS', flush=True)
