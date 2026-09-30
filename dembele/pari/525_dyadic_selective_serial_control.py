"""D128 control serial phases with bounded row decoding and serialization.

Every generated output byte is compared to a retained D124 certificate.
No duplicate binary is retained: incremental encoding/hashing is the
serialization control, not an executed larger arithmetic refinement.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
s = importlib.util.spec_from_file_location('rolling', ROOT / 'dembele/pari/519_dyadic_rolling_precision_chunks.py')
w = importlib.util.module_from_spec(s)
s.loader.exec_module(w)
h, b, q, c, a, l = w.h, w.b, w.q, w.c, w.a, w.l
P, R, N = 1600, 32, 174
BASE = 'dyadic_weighted_P1600_col00'


def packet(suffix):
    return h.read(BASE + '_' + suffix + '_d124')[0]


def reader(row, key='state_file', count=P, shift=0, weighted=False):
    return q.StateReader(row[key], count, P // 8 - shift,
        weighted_precision=P if weighted else None)


def scaled(row, shift):
    return [tuple(v << shift for v in x) for x in row]


def project(row):
    return [tuple(v & m for v, m in zip(x, mask)) for x, mask in zip(row, w.masks(P))]


def encode_weighted(row):
    assert len(row) == P
    raw = bytearray()
    for k, x in enumerate(row):
        for i, value in enumerate(x):
            bits = w.bits(P, k, i)
            assert 0 <= value < 1 << bits
            raw.extend(value.to_bytes((bits + 7) // 8, 'little'))
    return raw


def encode_scaled(row, shift):
    assert all(v & ((1 << shift) - 1) == 0 for x in row for v in x)
    return b.pack([[tuple(v >> shift for v in x) for x in row]], P // 8 - shift)


class ByteComparison:
    """Consume one serialized state at a time; compare actual bytes, not only hashes."""
    def __init__(self, record):
        self.record = record
        assert h.source(record['path']) == record
        h.PATHS.add(Path(record['path']))
        self.file = Path(record['path']).open('rb')
        self.sha = hashlib.sha256()
        self.rows = self.bytes = self.maximum_serialized_row_bytes = 0

    def append(self, raw):
        assert raw == self.file.read(len(raw))
        self.sha.update(raw)
        self.rows += 1
        self.bytes += len(raw)
        self.maximum_serialized_row_bytes = max(self.maximum_serialized_row_bytes, len(raw))

    def finish(self):
        assert self.rows == N and not self.file.read(1)
        self.file.close()
        assert self.sha.hexdigest() == self.record['sha256']
        return {'reference': self.record, 'serialized_sha256': self.sha.hexdigest(),
            'states': self.rows, 'bytes_compared_directly': self.bytes,
            'maximum_serialized_row_bytes': self.maximum_serialized_row_bytes}


def sweep_rows(prefix, previous, purpose, backend):
    """Validate all metadata first, then decode one state of one chunk at a time."""
    previous_path = DATA / (previous + '.json')
    h.read(previous)
    rows, cursor, count = [], 0, None
    for path in sorted(DATA.glob(prefix + '_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json')):
        row, _ = h.read(path.stem)
        assert row['input_metadata'] == h.source(previous_path)
        assert row['working_precision_pi'] == P and row['purpose'] == purpose and row['backend'] == backend
        assert row['first_state'] == cursor and cursor <= row['last_state'] < N
        count = row['output_count'] if count is None else count
        assert row['output_count'] == count
        cursor = row['last_state'] + 1
        rows.append(row)
    assert len(rows) == 6 and cursor == N
    for row in rows:
        shift = row['operator_power_of_two_shift']
        source = q.StateReader(row['checkpoint_files'][0], count, P // 8 - shift,
            states=row['last_state'] - row['first_state'] + 1)
        for j in range(source.states):
            yield row['first_state'] + j, scaled(source.row(j), shift)
        source.close()


def sweep(suffix, previous, purpose, backend='FLINT'):
    return sweep_rows(BASE + '_' + suffix + '_d124', BASE + '_' + previous + '_d124', purpose, backend)


def assembly():
    outputs, checks = {}, {}
    old, _ = h.read('dyadic_staged_P800_col00_verified_d123')
    prior = q.StateReader(old['state_file'], 800, 100)
    mask = (1 << 100) - 1
    sink = ByteComparison(packet('seed_assembled')['state_file'])
    for e, values in sweep('extend', 'input', 'extend'):
        assert [tuple(v & mask for v in x) for x in values[:800]] == prior.row(e)
        sink.append(encode_weighted(project(values)))
    outputs['seed_assembly'] = sink.finish()
    checks['seed_old_low_scalars'] = N * 800 * 8

    # The only assembled bank is the fixed 32-row low system, independent
    # of the long moment cutoff. All high-state work remains row-local.
    rhs = [[[x] for x in values[1:]] for _, values in sweep('seed_rhs', 'seed_assembled', 'seed-low-rhs')]
    factor = c.FactorReader(200)
    answer = factor.solve(rhs, b.Algebra(200))
    factor.close()
    assert factor.decoded_blocks == 1226
    source = reader(packet('seed_assembled'), weighted=True)
    sink = ByteComparison(packet('seed_low')['state_file'])
    for e in range(N):
        values = source.row(e)
        values[1:33] = [x[0] for x in answer[e]]
        assert [tuple(v & mask for v in x) for x in values[:800]] == prior.row(e)
        sink.append(encode_weighted(values))
    outputs['seed_low_assembly'] = sink.finish()
    source.close()
    del rhs, answer

    source = reader(packet('seed_low'), weighted=True)
    target = packet('seed')
    sink = ByteComparison(target['residual_file'])
    for e, values in sweep('seed_operator', 'seed_low', 'seed-residual'):
        residual = project(b.Algebra(200).sub([values], [source.row(e, len(values))])[0])
        assert all(x == b.ZERO for x in residual[:33]) and l.value([residual], P) >= 800
        sink.append(encode_scaled(residual, target['residual_power_of_two_shift']))
    outputs['seed_residual'] = sink.finish()
    source.close()

    for step in (1, 12, 24):
        suffix = f'step{step:02d}'
        prepared, target = packet(suffix + '_prepared'), packet(suffix)
        correction = reader(prepared, 'operator_input_file', prepared['input_count'], prepared['correction_power_of_two_shift'])
        sink = ByteComparison(target['residual_file'])
        for e, values in sweep(suffix + '_operator', suffix + '_prepared', 'correction'):
            assert values[:33] == scaled(correction.row(e, 33), prepared['correction_power_of_two_shift'])
            values[:33] = [b.ZERO] * 33
            residual = project(values)
            assert l.value([residual], P) >= target['weighted_residual_lower_bound_pi']
            sink.append(encode_scaled(residual, target['residual_power_of_two_shift']))
        outputs[suffix + '_residual'] = sink.finish()
        correction.close()

    weighted = reader(packet('step24'), weighted=True)
    sink = ByteComparison(packet('reconstructed')['state_file'])
    extension = sweep('extend', 'input', 'extend')
    for e, values in sweep('reconstruct_operator', 'step24', 'reconstruct', 'GMP'):
        assert project(values) == weighted.row(e)
        assert [tuple(v & mask for v in x) for x in values[:800]] == prior.row(e)
        j, extended = next(extension)
        assert e == j and [tuple(v & mask for v in x) for x in values] == [tuple(v & mask for v in x) for x in extended]
        sink.append(encode_scaled(values, 0))
    assert next(extension, None) is None
    outputs['uniform_reconstruction'] = sink.finish()
    checks['weighted_projection_scalars'] = checks['old_extended_scalars'] = N * P * 8
    weighted.close()
    prior.close()

    source = reader(packet('reconstructed'))
    sink = ByteComparison(packet('verified')['residual_file'])
    masses, _ = h.read('dyadic_harmonic_certificate_d111')
    for e, values in sweep('verify_operator', 'reconstructed', 'verify', 'GMP'):
        assert values == source.row(e)
        assert values[0] == (masses['harmonic_basis'][0][e] & ((1 << 200) - 1),) + (0,) * 7
        sink.append(bytes(P * 8 * 25))
    outputs['original_residual'] = sink.finish()
    checks['original_residual_scalars'] = N * P * 8
    checks['exact_masses'] = N
    source.close()
    return {'phase': 'assembly', 'streamed_outputs': outputs, 'scalar_checks': checks,
        'maximum_long_state_rows_retained': 8, 'complete_long_bank_decoded': False,
        'long_bank_memory_bound_independent_of_state_count': True,
        'fixed_low_bank_shape': [174, 32, 1, 8],
        'full_original_maps_not_recomputed': True,
        'new_binary_written': False, 'incremental_serialization_and_byte_comparison_only': True}


def prepare(step):
    assert step in (1, 12, 24)
    before = packet('seed' if step == 1 else f'step{step-1:02d}')
    after = packet(f'step{step:02d}_prepared')
    u, count = before['weighted_residual_lower_bound_pi'], before['active_moment_count']
    shift, bits = u // 8, P // 8 - u // 8
    residual = reader(before, 'residual_file', count, shift)
    targets, params, path = b.parameters(8 * bits)
    h.PATHS.add(path)
    groups = {}
    for e in range(N):
        for branch, child in enumerate(targets[e]):
            groups.setdefault(params[e][branch], []).append((e, child))
    cut = min(count, 8 * bits)
    ring, totals = a.Ring(bits), [[b.ZERO] * 33 for _ in range(N)]
    tick = time.monotonic()
    if 8 * bits > 33:
        for pars, destinations in groups.items():
            plan = l.Plan(ring, *pars, cut, 33)
            for e, child in destinations:
                values = residual.row(child, cut)
                assert all(x == b.ZERO for x in values[:33])
                totals[e] = ring.padd(totals[e], plan.apply(values))
                del values
            del plan
        rhs = [[[x] for x in edge[1:]] for edge in totals]
        factor = c.FactorReader(bits)
        answer = factor.solve(rhs, b.Algebra(bits))
        factor.close()
        assert factor.decoded_blocks == 1226
        low = [[row[0] for row in edge] for edge in answer]
        # Rebuild and check every original sparse low equation as well.
        algebra = b.Algebra(bits)
        check = list(answer)
        for pars, destinations in groups.items():
            block = b.coefficients(pars, 32, algebra)
            for e, child in destinations:
                check[e] = algebra.sub(check[e], algebra.mul(block, answer[child]))
            del block
        assert check == rhs
    else:
        low = [[b.ZERO] * 32 for _ in range(N)]
    seconds = time.monotonic() - tick
    source = reader(before, weighted=True)
    states, corrections = ByteComparison(after['state_file']), ByteComparison(after['operator_input_file'])
    for e in range(N):
        row = residual.row(e)
        assert all(x == b.ZERO for x in row[:33])
        assert l.value([scaled(row, shift)], P) >= u
        row[1:33] = low[e]
        correction = scaled(row, shift)
        assert l.value([correction], P) >= u
        values = source.row(e)
        for k, x in enumerate(correction):
            values[k] = tuple((v + d) & mask for v, d, mask in zip(values[k], x, w.masks(P)[k]))
        states.append(encode_weighted(values))
        corrections.append(encode_scaled(correction, shift))
    source.close()
    residual.close()
    return {'phase': 'prepare', 'step': step, 'before_pi': u, 'input_count': count,
        'working_modulus_bits': bits, 'streamed_outputs': {'state': states.finish(), 'correction': corrections.finish()},
        'weighted_state_scalars_compared': N * P * 8,
        'correction_scalars_compared': N * count * 8,
        'original_low_sparse_scalar_checks': N * 32 * 8 if 8 * bits > 33 else 0,
        'complete_long_bank_decoded': False, 'maximum_prepared_maps_held': 1,
        'maximum_decoded_factor_blocks_held': 1 if 8 * bits > 33 else 0,
        'maximum_long_state_rows_retained': 8, 'fixed_low_bank_shape': [174, 32, 1, 8],
        'low_rhs_solve_and_residual_seconds': seconds,
        'new_binary_written': False, 'incremental_serialization_and_byte_comparison_only': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('assembly', 'prepare'))
    parser.add_argument('--step', type=int)
    args = parser.parse_args()
    label = args.phase + (f'_step{args.step:02d}' if args.phase == 'prepare' else '')
    out = DATA / ('dyadic_selective_serial_' + label + '_d128.json')
    assert not out.exists()
    start = time.monotonic()
    # Verify the existing compiled adaptive kernel before first use.
    w.Engine(P)
    cert = assembly() if args.phase == 'assembly' else prepare(args.step)
    h.PATHS.update(c.h.PATHS)
    h.PATHS.update([Path(__file__), Path(w.__file__), Path(q.__file__), Path(c.__file__),
        Path(h.__file__), Path(b.__file__), Path(a.__file__), a.CSOURCE, a.LIBRARY,
        Path(l.__file__), Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY])
    result = {'status': 'pass', 'milestone': 'D128', 'working_precision_pi': P,
        'harmonic_basis_column': 0, 'certificates': cert, 'actual_harmonic_precision_increased': False,
        'wall_seconds': time.monotonic() - start, 'peak_rss_bytes': w.peak_rss(),
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|525_DYADIC_SELECTIVE_SERIAL_CONTROL', flush=True)
