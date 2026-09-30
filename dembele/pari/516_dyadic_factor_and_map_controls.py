"""D126 isolate factor decoding, stream triangular solves, and reuse CM-free maps.

Factor phases run in separate processes so their resident-memory peaks are
comparable. Streamed factors have one decoded block, shared across all RHS
columns. Every solution is checked in the original sparse low equations.
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
s = importlib.util.spec_from_file_location('selective', ROOT / 'dembele/pari/514_dyadic_selective_state_control.py')
q = importlib.util.module_from_spec(s)
s.loader.exec_module(q)
h, b, w = q.h, q.b, q.w
s = importlib.util.spec_from_file_location('adaptive', ROOT / 'dembele/pari/503_dyadic_adaptive_kernel_control.py')
a = importlib.util.module_from_spec(s)
s.loader.exec_module(a)


class FactorReader:
    def __init__(self, bits):
        precision = 400 if bits <= 50 else 800 if bits <= 100 else 1600
        assert 1 <= bits <= 200
        suffix = 'd121' if precision == 400 else 'd123' if precision == 800 else 'd124'
        packet, path = h.read(f'dyadic_low_factor_P{precision}_r32_{suffix}')
        self.packet, self.bits = packet, bits
        binary = path.with_suffix('.bin')
        expected = [x for x in packet['sources'] if Path(x['path']) == binary]
        assert len(expected) == 1 and h.source(binary) == expected[0]
        h.PATHS.add(binary)
        self.width = packet['binary_coefficient_width_bytes']
        self.size = 32 * 32 * 8 * self.width
        self.keys = [tuple(row) for row in packet['binary_block_order']]
        assert len(set(self.keys)) == len(self.keys) == 1226
        self.index = {key: i for i, key in enumerate(self.keys)}
        assert binary.stat().st_size == self.size * len(self.keys)
        self.file = binary.open('rb')
        self.read_seconds, self.decoded_blocks = 0.0, 0

    def block(self, key):
        tick = time.monotonic()
        self.file.seek(self.index[key] * self.size)
        raw = self.file.read(self.size)
        assert len(raw) == self.size
        block = b.unpack(raw, 32, 32, self.packet['modulus_bits'])
        assert all(c < 1 << self.packet['modulus_bits'] for row in block for x in row for c in x)
        if self.bits < self.packet['modulus_bits']:
            block = b.reduce(block, (1 << self.bits) - 1)
        self.decoded_blocks += 1
        self.read_seconds += time.monotonic() - tick
        return block

    def solve(self, rhs, algebra):
        lower, upper = {}, {}
        for kind, i, j in self.keys:
            if kind == 'L':
                lower.setdefault(j, []).append((i, (kind, i, j)))
            elif kind == 'U':
                upper.setdefault(i, []).append((j, (kind, i, j)))
            else:
                assert kind == 'D' and i == j
        values, answer = list(rhs), [None] * 174
        for k in self.packet['order']:
            for i, key in lower.get(k, []):
                block = self.block(key)
                values[i] = algebra.sub(values[i], algebra.mul(block, values[k]))
                del block
        for k in reversed(self.packet['order']):
            value = values[k]
            for j, key in upper.get(k, []):
                assert answer[j] is not None
                block = self.block(key)
                value = algebra.sub(value, algebra.mul(block, answer[j]))
                del block
            block = self.block(('D', k, k))
            answer[k] = algebra.mul(block, value)
            del block
        return answer

    def close(self):
        self.file.close()


def factors(mode, bits, columns):
    start = time.monotonic()
    reader = FactorReader(bits)
    authentication_seconds = time.monotonic() - start
    algebra = b.Algebra(bits)
    rhs = [b.k.data(32, columns, bits, f'D126-factor-state{i}') for i in range(174)]
    begin = time.monotonic()
    if mode == 'resident':
        D, L, U = {}, {}, {}
        for key in reader.keys:
            kind, i, j = key
            block = reader.block(key)
            if kind == 'D':
                D[i] = block
            else:
                (L if kind == 'L' else U)[i, j] = block
        loaded_peak = w.peak_rss()
        answer = b.solve(rhs, reader.packet['order'], D, L, U, algebra)
        del D, L, U, block
    else:
        answer = reader.solve(rhs, algebra)
        loaded_peak = None
    solve_seconds = time.monotonic() - begin
    assert reader.decoded_blocks == 1226
    reader.close()
    before_residual_peak = w.peak_rss()
    begin = time.monotonic()
    targets, params, path = b.parameters(bits * 8)
    h.PATHS.add(path)
    # Rebuild each original edge block on demand, without the saved factors.
    # The original operator has only two child blocks per state.
    for e in range(174):
        value = answer[e]
        for branch, child in enumerate(targets[e]):
            original = b.coefficients(params[e][branch], 32, algebra)
            value = algebra.sub(value, algebra.mul(original, answer[child]))
            del original
        assert value == rhs[e], (mode, bits, e)
    residual_seconds = time.monotonic() - begin
    digest, prefix = hashlib.sha256(), hashlib.sha256()
    for edge in answer:
        digest.update(b.pack(edge, bits))
        prefix.update(b.pack([row[:2] for row in edge], bits))
    return {'mode': mode, 'modulus_bits': bits, 'unrelated_rhs_columns': columns,
        'complete_original_sparse_residual_scalar_checks': 174 * 32 * 8 * columns,
        'factor_blocks_decoded': reader.decoded_blocks, 'factor_payload_bytes': reader.size * 1226,
        'maximum_decoded_factor_blocks_held': 1226 if mode == 'resident' else 1,
        'authentication_seconds': authentication_seconds, 'factor_read_decode_seconds': reader.read_seconds,
        'solve_seconds_including_decode': solve_seconds,
        'solve_seconds_excluding_decode': solve_seconds - reader.read_seconds,
        'original_sparse_residual_seconds': residual_seconds,
        'peak_rss_after_load_bytes': loaded_peak, 'peak_rss_after_solve_bytes': before_residual_peak,
        'all_answers_sha256': digest.hexdigest(), 'first_two_rhs_answers_sha256': prefix.hexdigest(),
        'actual_harmonic_low_rhs_used': False}


def maps():
    control, _ = h.read('dyadic_adaptive_kernel_control_d124')
    for path in (Path(a.__file__), a.CSOURCE, a.LIBRARY):
        expected = [x for x in control['sources'] if Path(x['path']) == path]
        assert len(expected) == 1 and h.source(path) == expected[0]
        h.PATHS.add(path)
    targets, params, path = b.parameters(800)
    h.PATHS.add(path)
    readers = []
    for stem in ('dyadic_staged_P800_col00_verified_d123', 'dyadic_weighted_P800_col01_verified_d125'):
        packet, _ = h.read(stem)
        assert packet['certificate']['original_full_residual_zero']
        readers.append(q.StateReader(packet['state_file'], 800, 100))
    selected = [0, 17, 61, 98, 173]
    groups = {}
    for e in selected:
        for branch, child in enumerate(targets[e]):
            groups.setdefault(params[e][branch], []).append((e, child))
    timings, hashes = [], []
    for reused in (False, True):
        ring = a.Ring(100)
        totals = {(col, e): [b.ZERO] * 33 for col in range(2) for e in selected}
        prepare_seconds = apply_seconds = 0.0
        plan_count = 0
        tick = time.monotonic()
        for pars, destinations in groups.items():
            plan = None
            for col, reader in enumerate(readers):
                for e, child in destinations:
                    values = reader.row(child)
                    if plan is None or not reused:
                        begin = time.monotonic()
                        plan = q.l.Plan(ring, *pars, 800, 33)
                        prepare_seconds += time.monotonic() - begin
                        plan_count += 1
                    begin = time.monotonic()
                    totals[col, e] = ring.padd(totals[col, e], plan.apply(values))
                    apply_seconds += time.monotonic() - begin
                    del values
            del plan
        elapsed = time.monotonic() - tick
        sha = hashlib.sha256()
        for col, reader in enumerate(readers):
            for e in selected:
                assert totals[col, e] == reader.row(e, 33)
                sha.update(b.pack([totals[col, e]], 100))
        hashes.append(sha.hexdigest())
        timings.append({'reuse_one_map_across_columns_and_destinations': reused,
            'prepared_plans': plan_count, 'prepare_seconds': prepare_seconds,
            'apply_seconds': apply_seconds, 'total_seconds_including_selective_reads': elapsed})
    assert hashes[0] == hashes[1]
    for reader in readers:
        reader.close()
    return {'actual_harmonic_columns': [0, 1], 'working_precision_pi': 800,
        'output_states': selected, 'output_moments': 33,
        'original_equation_scalar_checks_per_mode': 2640,
        'maximum_prepared_plans_retained_in_reuse_mode': 1,
        'comparison_sha256': hashes[0], 'distinct_maps': len(groups), 'timings': timings,
        'timing_caveat': 'One bounded run in fixed order; a control, not a full-bank or target-size speedup claim.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('factors', 'maps'))
    parser.add_argument('--mode', choices=('resident', 'stream'), default='stream')
    parser.add_argument('--bits', type=int, choices=(100, 200), default=200)
    parser.add_argument('--columns', type=int, choices=(2, 16), default=2)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    start = time.monotonic()
    cert = factors(args.mode, args.bits, args.columns) if args.phase == 'factors' else maps()
    h.PATHS.update([Path(__file__), Path(q.__file__), Path(w.__file__), Path(h.__file__),
        Path(b.__file__), Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY,
        Path(q.p.__file__), Path(q.p.f.__file__), Path(q.l.__file__)])
    result = {'status': 'pass', 'milestone': 'D126', 'phase': args.phase, 'certificates': cert,
        'wall_seconds': time.monotonic() - start, 'peak_rss_bytes': w.peak_rss(),
        'actual_moment_precision_increased': False, 'complete_target_size_solve_costed': False,
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|516_DYADIC_FACTOR_AND_MAP_CONTROLS', flush=True)
