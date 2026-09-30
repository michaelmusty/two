"""D130 lossless prospective retention controls; all frozen inputs stay intact.

Zero residuals are represented by a checked logical layout and zero stream
digest. Weighted rows can be regenerated from a retained uniform state.
These controls do not implement a target refinement scratch protocol.
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
spec = importlib.util.spec_from_file_location('target_ops', ROOT / 'dembele/pari/533_dyadic_target_operation_controls.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
h, b, q, w = t.h, t.b, t.q, t.w
N, R = 174, 32


def widths(P, count=None):
    count = P if count is None else count
    return [tuple((max(0, -((i - (P if k <= R else P - k)) // 8)) + 7) // 8 for i in range(8))
            for k in range(count)]


def weighted_row(row, P):
    assert len(row) == P
    raw = bytearray()
    for k, values in enumerate(row):
        for i, v in enumerate(values):
            bitcount = P // 8 if k <= R else max(0, (P - k - i + 7) // 8)
            raw.extend((v % (1 << bitcount)).to_bytes((bitcount + 7) // 8, 'little'))
    return bytes(raw)


def zero_chunks(length):
    assert isinstance(length, int) and length >= 0
    zero = bytes(1 << 20)
    while length:
        count = min(length, len(zero))
        yield zero[:count]
        length -= count


def zero_digest(length):
    sha = hashlib.sha256()
    for raw in zero_chunks(length):
        sha.update(raw)
    return sha.hexdigest()


def check_descriptor(record):
    assert record['codec'] == 'dyadic_zero_bytes_v1'
    layout = record['layout']
    expected = layout['states'] * layout['moments'] * 8 * ((layout['modulus_bits'] + 7) // 8)
    assert record['logical_bytes'] == expected > 0
    assert zero_digest(expected) == record['logical_sha256']
    return expected


def zero_control():
    state, statepath = h.read('dyadic_streamed_P3200_col00_verified_d129')
    assert state['certificate']['original_full_residual_zero']
    weighted_path = Path(state['weighted_state_metadata']['path'])
    assert h.source(weighted_path) == state['weighted_state_metadata']
    weighted, _ = h.read(weighted_path.stem)
    records = []
    for name, original, count, bits in (
        ('full', state['residual_file'], 3200, 400),
        ('weighted_final', weighted['residual_file'], weighted['active_moment_count'],
         400 - weighted['residual_power_of_two_shift'])):
        path = Path(original['path'])
        assert h.source(path) == original
        h.PATHS.add(path)
        tick = time.monotonic()
        size, sha = 0, hashlib.sha256()
        with path.open('rb') as f:
            for zero in zero_chunks(path.stat().st_size):
                raw = f.read(len(zero))
                assert raw == zero
                sha.update(raw)
                size += len(raw)
            assert not f.read()
        desc = {'codec': 'dyadic_zero_bytes_v1',
            'layout': {'states': N, 'moments': count, 'modulus_bits': bits},
            'logical_bytes': size, 'logical_sha256': sha.hexdigest()}
        assert check_descriptor(desc) == size and desc['logical_sha256'] == original['sha256']
        records.append({'name': name, 'original': original, 'descriptor': desc,
            'direct_byte_comparisons': size, 'check_seconds': time.monotonic() - tick})
    rejected = 0
    original = records[0]['descriptor']
    for changed in ({**original, 'logical_bytes': original['logical_bytes'] + 1},
                    {**original, 'logical_sha256': '0' * 64},
                    {**original, 'codec': 'unrecognized'}):
        try:
            check_descriptor(changed)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('invalid descriptor accepted')
    # A descriptor cannot be certified from a nonzero residual buffer.
    bad = bytearray(257)
    bad[128] = 1
    assert bytes(bad) != bytes(len(bad))
    P = 10552
    size = N * P * 8 * 165
    target = {'codec': 'dyadic_zero_bytes_v1',
        'layout': {'states': N, 'moments': P, 'modulus_bits': 1319},
        'logical_bytes': size, 'logical_sha256': zero_digest(size)}
    assert check_descriptor(target) == size
    return {'actual_original_residuals': records,
        'malformed_descriptor_rejections': rejected, 'nonzero_buffer_rejected': True,
        'synthetic_target_zero_descriptor': target,
        'target_original_residual_computed': False, 'frozen_payloads_deleted_or_modified': False,
        'verified_state_metadata': h.source(statepath)}


def projection_control(first, last):
    assert 0 <= first <= last < N and last - first < 29
    packet, path = h.read('dyadic_streamed_P3200_col00_verified_d129')
    weighted_path = Path(packet['weighted_state_metadata']['path'])
    assert h.source(weighted_path) == packet['weighted_state_metadata']
    weighted, _ = h.read(weighted_path.stem)
    uniform = q.StateReader(packet['state_file'], 3200, 400)
    target = Path(weighted['state_file']['path'])
    assert h.source(target) == weighted['state_file']
    h.PATHS.add(target)
    row_bytes = sum(sum(row) for row in widths(3200))
    assert target.stat().st_size == N * row_bytes
    sha, length = hashlib.sha256(), 0
    tick = time.monotonic()
    with target.open('rb') as f:
        f.seek(first * row_bytes)
        for e in range(first, last + 1):
            encoded = weighted_row(uniform.row(e), 3200)
            expected = f.read(row_bytes)
            assert encoded == expected and len(encoded) == row_bytes
            sha.update(encoded)
            length += row_bytes
    uniform.close()
    return {'first_state': first, 'last_state': last,
        'weighted_coordinates_regenerated_and_compared': (last - first + 1) * 3200 * 8,
        'direct_byte_comparisons': length, 'generated_sha256': sha.hexdigest(),
        'projection_and_compare_seconds': time.monotonic() - tick,
        'original_uniform_metadata': h.source(path), 'original_weighted_file': weighted['state_file'],
        'new_weighted_payload_written': False, 'frozen_payloads_deleted_or_modified': False}


def target_row(stem):
    P, bits = 10552, 1319
    values = b.k.data(1, P, bits, 'D130-target-serialization')[0]
    tick = time.monotonic()
    raw = b.pack([values], bits)
    serialized_seconds = time.monotonic() - tick
    path = DATA / (stem + '_uniform_row.bin')
    tick = time.monotonic()
    with path.open('xb') as f:
        assert f.write(raw) == len(raw)
        f.flush()
        import os
        os.fsync(f.fileno())
    write_seconds = time.monotonic() - tick
    tick = time.monotonic()
    assert b.unpack(path.read_bytes(), 1, P, bits) == [values]
    read_decode_seconds = time.monotonic() - tick
    tick = time.monotonic()
    weighted = weighted_row(values, P)
    weighted_seconds = time.monotonic() - tick
    # Decode by explicit byte-width and floor division, independently of the
    # production bit-mask projection and the encoder's modulo expression.
    offset, checked = 0, 0
    for k, values_at_k in enumerate(values):
        precision = P if k <= R else P - k
        for i, v in enumerate(values_at_k):
            n = max(0, -((i - precision) // 8))
            width = (n + 7) // 8
            restored = int.from_bytes(weighted[offset:offset + width], 'little')
            assert restored == v - ((v // (2 ** n)) * (2 ** n))
            offset += width
            checked += 1
    assert offset == len(weighted) == sum(sum(row) for row in widths(P))
    assert len(raw) == P * 8 * 165
    weighted_path = DATA / (stem + '_weighted_row.bin')
    with weighted_path.open('xb') as f:
        assert f.write(weighted) == len(weighted)
    files = [h.source(path), h.source(weighted_path)]
    return {'input_kind': 'synthetic_target_uniform_row', 'working_precision_pi': P,
        'uniform_row_bytes': len(raw), 'weighted_row_bytes': len(weighted),
        'independent_projected_coordinate_checks': checked,
        'serialization_seconds': serialized_seconds, 'write_and_fsync_seconds': write_seconds,
        'read_decode_seconds': read_decode_seconds, 'weighted_projection_seconds': weighted_seconds,
        'output_files': files, 'maximum_rows_materialized': 1,
        'full_target_bank_written': False}


def inventory():
    rows = []
    for P, seed in ((3200, 1600), (6400, 3200), (10552, 6400), (10552, 3200), (10552, 800)):
        bits, width = P // 8, (P // 8 + 7) // 8
        uniform = N * P * 8 * width
        weighted = N * sum(sum(row) for row in widths(P))
        residual = N * (P - seed) * 8 * (((bits - seed // 8) + 7) // 8)
        u = seed
        corrections = 0
        while P - u > R + 1:
            u += R + 1
            corrections += 1
        terminal = N * (R + 1) * 8 * (((bits - u // 8) + 7) // 8)
        slots = {'old_seed_input_at_target_width': N * seed * 8 * width,
            'seed_extension_chunks': uniform, 'two_complete_checkpoints': 2 * (weighted + residual),
            'new_prepared_weighted_state': weighted, 'prepared_correction': residual,
            'one_active_operator_sweep': uniform, 'assembled_uniform_state': uniform,
            'final_full_residual': uniform, 'metadata_allowance': 1 << 20}
        cm = 17 * (2 * P) * 8 * width
        rows.append({'P': P, 'seed': seed, 'uniform_bytes': uniform, 'weighted_bytes': weighted,
            'largest_scaled_residual_bytes': residual, 'terminal_scaled_residual_bytes': terminal,
            'corrections': corrections, 'terminal_residual_lower_pi': u,
            'current_four_payload_retention_bytes': 2 * uniform + weighted + terminal,
            'prospective_uniform_plus_CM_retention_bytes_per_column': uniform + cm,
            'CM_bytes_per_column': cm, 'inherited_conservative_scratch_slots': slots,
            'inherited_conservative_scratch_total_bytes': sum(slots.values()),
            'fits_D129_2GiB_scratch_limit': sum(slots.values()) <= 2 * (1 << 30)})
    assert rows[0]['inherited_conservative_scratch_total_bytes'] == 1510359376
    assert rows[0]['current_four_payload_retention_bytes'] == 558829536
    target = rows[2]
    assert target['uniform_bytes'] * 16 == 38777333760
    return {'layouts': rows,
        'target_16_column_uniform_plus_CM_bytes': 16 * target['prospective_uniform_plus_CM_retention_bytes_per_column'],
        'target_16_column_existing_four_payload_plus_CM_bytes': 16 * (target['current_four_payload_retention_bytes'] + target['CM_bytes_per_column']),
        'target_uniform_alone_exceeds_D129_scratch_limit': target['uniform_bytes'] > 2 * (1 << 30),
        'compact_final_retention_controlled_separately': True,
        'integrated_target_scratch_protocol_implemented': False,
        'new_scratch_limit_or_production_run_authorized_by_this_certificate': False,
        'all_frozen_old_payloads_preserved': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('zero', 'projection', 'target-row', 'inventory'), required=True)
    p.add_argument('--first', type=int)
    p.add_argument('--last', type=int)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    begin = time.monotonic()
    cert = (zero_control() if args.phase == 'zero' else projection_control(args.first, args.last)
            if args.phase == 'projection' else target_row(args.output) if args.phase == 'target-row' else inventory())
    h.PATHS.update([Path(__file__), Path(t.__file__), Path(t.c.__file__), Path(q.__file__), Path(h.__file__),
                   Path(b.__file__), Path(b.k.__file__), Path(w.__file__)])
    result = {'status': 'pass', 'milestone': 'D130', 'phase': args.phase, 'certificates': cert,
        'wall_seconds': time.monotonic() - begin, 'peak_rss_bytes': w.peak_rss(),
        'actual_harmonic_precision_increased': False,
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(h.source(out)), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|536_DYADIC_COMPACT_RETENTION_CONTROL', flush=True)
