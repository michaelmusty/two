"""D130 repeated exact residual lifting with the frozen 200-bit low factor.

Residual formation, correction solving, and verification are separate capped
jobs. Seven stages reach 1319 bits. Every stage retains full original sparse
equation checks; synthetic RHS data do not refine an actual harmonic column.
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
spec = importlib.util.spec_from_file_location('reuse', ROOT / 'dembele/pari/524_dyadic_factor_reuse_lift.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
c, b, h, w = m.c, m.b, m.h, m.w
N, R, TARGET = 174, 32, 1319


def synthetic(columns, bits, label='rhs'):
    mask = (1 << bits) - 1
    return [b.reduce(b.k.data(R, columns, TARGET, f'D130-low-{label}-state{e}'), mask) for e in range(N)]


def save_values(stem, values, bits):
    path = DATA / (stem + '.bin')
    with path.open('xb') as f:
        for row in values:
            raw = b.pack(row, bits)
            assert f.write(raw) == len(raw)
    return h.source(path)


def read_values(record, columns, bits):
    path = Path(record['path'])
    assert h.source(path) == record
    h.PATHS.add(path)
    width = R * columns * 8 * ((bits + 7) // 8)
    assert path.stat().st_size == N * width
    values = []
    with path.open('rb') as f:
        for _ in range(N):
            values.append(b.unpack(f.read(width), R, columns, bits))
        assert not f.read()
    assert all(0 <= v < 1 << bits for edge in values for row in edge for x in row for v in x)
    return values


def digest(values, bits, prefix=False):
    sha = hashlib.sha256()
    for edge in values:
        sha.update(b.pack([row[:1] for row in edge] if prefix else edge, bits))
    return sha.hexdigest()


def original(values, bits, first=0, stop=None):
    groups = list(m.original_groups(bits).items())
    stop = len(groups) if stop is None else stop
    assert 0 <= first < stop <= len(groups)
    algebra, result = b.Algebra(bits), list(values)
    make = multiply = 0.0
    for index in range(first, stop):
        pars, destinations = groups[index]
        tick = time.monotonic()
        block = b.coefficients(pars, R, algebra)
        make += time.monotonic() - tick
        tick = time.monotonic()
        for e, child in destinations:
            result[e] = algebra.sub(result[e], algebra.mul(block, values[child]))
        multiply += time.monotonic() - tick
        del block
        if (index - first + 1) % 55 == 0:
            print('LOW_ORIGINAL|' + json.dumps({'bits': bits, 'groups': index - first + 1,
                'coefficient_seconds': make, 'multiply_seconds': multiply}), flush=True)
    return result, {'modulus_bits': bits, 'distinct_original_maps_total': len(groups),
        'first_group': first, 'stop_group': stop, 'complete_original_operator': first == 0 and stop == len(groups),
        'coefficient_block_seconds': make, 'multiply_seconds': multiply,
        'maximum_original_coefficient_blocks_held': 1}


def load_answer(stem):
    packet, path = h.read(stem)
    assert packet['phase'] == 'solve' and packet['milestone'] == 'D130'
    cert = packet['certificates']
    return packet, cert, read_values(cert['answer'], cert['columns'], cert['new_bits']), path


def build(args):
    phase, columns, new = args.phase, args.columns, args.bits
    assert columns in (1, 2, 16) and 1 <= new <= TARGET
    eqs = N * R * 8 * columns
    times = []
    if phase == 'residual':
        verified, vpath = h.read(args.previous)
        assert verified['phase'] == 'verify' and verified['certificates']['all_original_sparse_equations_zero']
        previous_path = Path(verified['certificates']['solution_metadata']['path'])
        assert h.source(previous_path) == verified['certificates']['solution_metadata']
        _, prior, answer, path = load_answer(previous_path.stem)
        old = prior['new_bits']
        assert prior['columns'] == columns and 0 < new - old <= 200
        rhs = synthetic(columns, new)
        applied, timing = original(answer, new)
        times.append(timing)
        algebra, mask = b.Algebra(new), (1 << old) - 1
        residual = [algebra.sub(x, y) for x, y in zip(rhs, applied)]
        assert all(v & mask == 0 for edge in residual for row in edge for x in row for v in x)
        quotient = [[[tuple(v >> old for v in x) for x in row] for row in edge] for edge in residual]
        record = save_values(args.output + '_quotient', quotient, new - old)
        return {'columns': columns, 'old_bits': old, 'new_bits': new, 'correction_bits': new - old,
            'previous_verified_metadata': h.source(vpath), 'previous_solution_metadata': h.source(path),
            'exact_residual_divisions_checked': eqs, 'exact_binary_divisor_exponent': old,
            'quotient': record, 'rhs_sha256': digest(rhs, new), 'timings': times}
    if phase == 'solve':
        if args.previous is None:
            assert new == 200
            old, step, prev_values, previous = 0, 200, None, None
            rhs = synthetic(columns, new)
        else:
            packet, path = h.read(args.previous)
            assert packet['phase'] == 'residual'
            previous = h.source(path)
            cert = packet['certificates']
            assert cert['columns'] == columns and cert['new_bits'] == new
            old, step = cert['old_bits'], cert['correction_bits']
            prior_path = Path(cert['previous_solution_metadata']['path'])
            assert h.source(prior_path) == cert['previous_solution_metadata']
            _, prior, prev_values, _ = load_answer(prior_path.stem)
            assert prior['columns'] == columns and prior['new_bits'] == old and 0 < step <= 200
            rhs = read_values(cert['quotient'], columns, step)
        tick = time.monotonic()
        factor = c.FactorReader(step)
        authenticate = time.monotonic() - tick
        tick = time.monotonic()
        delta = factor.solve(rhs, b.Algebra(step))
        solve_seconds = time.monotonic() - tick
        assert factor.decoded_blocks == 1226
        decode_seconds = factor.read_seconds
        factor.close()
        applied, timing = original(delta, step)
        assert applied == rhs
        times.append(timing)
        if old:
            answer = [[[tuple(u + (v << old) for u, v in zip(x, d)) for x, d in zip(row, dr)]
                for row, dr in zip(edge, de)] for edge, de in zip(prev_values, delta)]
            assert [b.reduce(edge, (1 << old) - 1) for edge in answer] == prev_values
        else:
            answer = delta
        file = save_values(args.output + '_answer', answer, new)
        return {'columns': columns, 'old_bits': old, 'new_bits': new, 'correction_bits': step,
            'previous_residual_metadata': previous, 'answer': file,
            'original_correction_equations_checked': eqs, 'all_original_correction_equations_zero': True,
            'factor_blocks_decoded': 1226, 'maximum_decoded_factor_blocks_held': 1,
            'factor_authentication_seconds': authenticate, 'factor_read_decode_seconds': decode_seconds,
            'factor_solve_seconds_including_decode': solve_seconds,
            'larger_factor_constructed': False, 'timings': times}
    if phase == 'verify':
        _, cert, answer, path = load_answer(args.previous)
        assert cert['columns'] == columns and cert['new_bits'] == new
        applied, timing = original(answer, new)
        rhs = synthetic(columns, new)
        assert applied == rhs
        return {'columns': columns, 'new_bits': new, 'solution_metadata': h.source(path),
            'original_sparse_scalar_equations_checked': eqs,
            'all_original_sparse_equations_zero': True,
            'rhs_sha256': digest(rhs, new), 'answer_sha256': digest(answer, new), 'timings': [timing]}
    assert phase == 'profile'
    values = synthetic(columns, new, label='profile')
    applied, timing = original(values, new, args.first_group, args.stop_group)
    return {'columns': columns, 'new_bits': new,
        'input_kind': 'deterministic_dense_synthetic_with_shared_first_column',
        'output_sha256': digest(applied, new), 'first_column_output_sha256': digest(applied, new, True),
        'timings': [timing], 'equation_solution_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=('residual', 'solve', 'verify', 'profile'), required=True)
    parser.add_argument('--bits', type=int, required=True)
    parser.add_argument('--columns', type=int, default=1)
    parser.add_argument('--previous')
    parser.add_argument('--first-group', type=int, default=0)
    parser.add_argument('--stop-group', type=int)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    begin = time.monotonic()
    cert = build(args)
    h.PATHS.update([Path(__file__), Path(m.__file__), Path(c.__file__), Path(c.q.__file__),
        Path(h.__file__), Path(b.__file__), Path(w.__file__), Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY,
        Path(b.p.__file__), Path(b.p.g.__file__), Path(b.p.f.__file__)])
    result = {'status': 'pass', 'milestone': 'D130', 'phase': args.phase,
        'certificates': cert, 'wall_seconds': time.monotonic() - begin,
        'peak_rss_bytes': w.peak_rss(), 'actual_harmonic_precision_increased': False,
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(h.source(out)), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|534_DYADIC_TARGET_LOW_LIFT', flush=True)
