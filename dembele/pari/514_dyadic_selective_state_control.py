"""D126 selective state reads, controlled against the certified P=1600 column.

Hash complete files by streaming, then decode one requested state at a time.
The isolated phases never decode a full reference bank. Their output is a
control certificate; they do not refine harmonic precision.
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
s = importlib.util.spec_from_file_location('weighted', ROOT / 'dembele/pari/497_dyadic_weighted_chunks.py')
w = importlib.util.module_from_spec(s)
s.loader.exec_module(w)
h, b, l, p = w.h, w.b, w.l, w.p
P, R, STATES = 1600, 32, 174


class StateReader:
    """Fixed row offsets; no mmap or unbounded decoded-state cache."""
    def __init__(self, record, count, bitcount, weighted_precision=None, states=STATES):
        self.path = Path(record['path'])
        assert h.source(self.path) == record
        h.PATHS.add(self.path)
        self.count, self.states = count, states
        if weighted_precision is None:
            self.bitcounts = [(bitcount,) * 8 for _ in range(count)]
        else:
            assert count == weighted_precision and bitcount == weighted_precision // 8
            # Independent expression for pi-adic coordinate precision.
            self.bitcounts = [tuple(max(0, -((i - (weighted_precision if k <= R else
                weighted_precision - k)) // 8)) for i in range(8)) for k in range(count)]
        self.widths = [tuple((n + 7) // 8 for n in row) for row in self.bitcounts]
        self.offsets = [0]
        for row in self.widths:
            self.offsets.append(self.offsets[-1] + sum(row))
        self.row_bytes = self.offsets[-1]
        assert self.path.stat().st_size == self.row_bytes * states
        self.file = self.path.open('rb')
        self.row_reads = self.decoded_scalar_count = self.decoded_bytes = 0
        self.maximum_single_read_bytes = 0

    def row(self, state, count=None):
        count = self.count if count is None else count
        assert 0 <= state < self.states and 0 <= count <= self.count
        length = self.offsets[count]
        self.file.seek(state * self.row_bytes)
        raw = self.file.read(length)
        assert len(raw) == length
        offset, answer = 0, []
        for widths, bits in zip(self.widths[:count], self.bitcounts[:count]):
            row = []
            for width, bit in zip(widths, bits):
                value = int.from_bytes(raw[offset:offset + width], 'little')
                assert 0 <= value < 1 << bit
                row.append(value)
                offset += width
            answer.append(tuple(row))
        assert offset == length
        self.row_reads += 1
        self.decoded_scalar_count += 8 * count
        self.decoded_bytes += length
        self.maximum_single_read_bytes = max(self.maximum_single_read_bytes, length)
        return answer

    def stats(self):
        return {key: getattr(self, key) for key in ('row_bytes', 'row_reads',
            'decoded_scalar_count', 'decoded_bytes', 'maximum_single_read_bytes')}

    def close(self):
        self.file.close()


def certified_inputs():
    packet, path = h.read('dyadic_weighted_P1600_col00_verified_d124')
    assert packet['certificate']['original_full_residual_zero']
    assert packet['working_precision_pi'] == P and packet['harmonic_basis_column'] == 0
    weighted_record = packet['weighted_state_metadata']
    assert h.source(weighted_record['path']) == weighted_record
    weighted, _ = h.read(Path(weighted_record['path']).stem)
    assert weighted['active_moment_count'] == R + 1
    assert weighted['weighted_residual_lower_bound_pi'] + R + 1 >= P
    return packet, weighted, h.source(path)


def projection():
    packet, weighted, metadata = certified_inputs()
    uniform = StateReader(packet['state_file'], P, P // 8)
    reduced = StateReader(weighted['state_file'], P, P // 8, weighted_precision=P)
    masses, _ = h.read('dyadic_harmonic_certificate_d111')
    mask = (1 << (P // 8)) - 1
    for e, mass in enumerate(masses['harmonic_basis'][0]):
        full, partial = uniform.row(e), reduced.row(e)
        assert full[0] == (mass & mask,) + (0,) * 7
        for actual, stored, bits in zip(full, partial, reduced.bitcounts):
            assert tuple(c & ((1 << n) - 1) for c, n in zip(actual, bits)) == stored
        del full, partial
    uniform.close()
    reduced.close()
    return {'all_weighted_projection_scalar_checks': STATES * P * 8,
        'exact_masses_checked': STATES, 'certified_uniform_metadata': metadata,
        'uniform_reads': uniform.stats(), 'weighted_reads': reduced.stats(),
        'maximum_decoded_state_rows_held': 2}


def operator(mode, selected):
    packet, weighted, metadata = certified_inputs()
    reference = StateReader(packet['state_file'], P, P // 8)
    source = StateReader((weighted if mode == 'weighted' else packet)['state_file'], P,
        P // 8, weighted_precision=P if mode == 'weighted' else None)
    engine = h.Engine(P)
    ring = p.Ring(P // 8)
    sha = hashlib.sha256()
    times = []
    for e in selected:
        start = time.monotonic()
        total, preparation, application = [b.ZERO] * P, 0.0, 0.0
        for branch, child in enumerate(engine.targets[e]):
            values = source.row(child)
            tick = time.monotonic()
            plan = l.Plan(ring, *engine.params[e][branch], P, P)
            preparation += time.monotonic() - tick
            tick = time.monotonic()
            applied = plan.apply(values)
            application += time.monotonic() - tick
            total = ring.padd(total, applied)
            del values, plan, applied
        expected = reference.row(e)
        assert total == expected, (mode, e)
        sha.update(b.pack([total], P // 8))
        times.append({'state': e, 'prepare_seconds': preparation,
            'apply_seconds': application, 'total_seconds': time.monotonic() - start})
        del expected, total
    source.close()
    reference.close()
    return {'input_kind': mode, 'backend': 'original GMP', 'output_states': selected,
        'full_original_operator_scalar_checks': len(selected) * P * 8,
        'all_selected_rows_equal_certified_uniform_state': True,
        'computed_rows_sha256': sha.hexdigest(), 'certified_uniform_metadata': metadata,
        'source_reads': source.stats(), 'reference_reads': reference.stats(),
        'decoded_input_state_cache_capacity': 1,
        'no_common_valuation_scan_or_full_bank_decode': True, 'state_timings': times}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('projection', 'uniform', 'weighted'))
    parser.add_argument('--output', required=True)
    parser.add_argument('--first', type=int)
    parser.add_argument('--last', type=int)
    args = parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    start = time.monotonic()
    if args.first is None:
        assert args.last is None
        selected = [0, 17, 61, 98, 173]
    else:
        assert args.last is not None and 0 <= args.first <= args.last < STATES
        selected = list(range(args.first, args.last + 1))
    cert = projection() if args.phase == 'projection' else operator(args.phase, selected)
    h.PATHS.update([Path(__file__), Path(w.__file__), Path(h.__file__), Path(b.__file__),
        Path(l.__file__), Path(p.__file__), Path(w.f.__file__), Path(b.k.__file__),
        Path(p.f.__file__), w.f.CSOURCE, w.f.LIBRARY, b.k.LIBRARY])
    result = {'status': 'pass', 'milestone': 'D126', 'phase': args.phase,
        'working_precision_pi': P, 'harmonic_basis_column': 0,
        'actual_moment_precision_increased': False, 'full_bank_precision_pi': 800,
        'certificates': cert, 'wall_seconds': time.monotonic() - start,
        'peak_rss_bytes': w.peak_rss(),
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|514_DYADIC_SELECTIVE_STATE_CONTROL', flush=True)


if __name__ == '__main__':
    main()
