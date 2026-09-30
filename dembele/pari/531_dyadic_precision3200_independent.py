"""D129 independent finite arithmetic audit with selective integer-only readers.

High-seed power recurrences are split into short degree blocks, with
immutable coefficient checkpoints. No production arithmetic is imported.
Retired production iteration payloads are not replayed or claimed retained.
"""
import argparse
import importlib.util
import json
from math import comb
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
s = importlib.util.spec_from_file_location('separate', ROOT / 'dembele/pari/491_dyadic_staged_pilot_independent.py')
a = importlib.util.module_from_spec(s)
s.loader.exec_module(a)
r = a.r
PATHS = {Path(__file__), Path(a.__file__), Path(r.__file__)}
P, N, R = 3200, 174, 32
BASE = 'dyadic_streamed_P3200_col00'
STOPS = (400, 800, 1200, 1600, 2000, 2399, 2799, 3199)


def read(stem, retained=True):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    if retained:
        for record in packet.get('checkpoint_files', []):
            assert r.source(record['path']) == record
            PATHS.add(Path(record['path']))
    else:
        assert packet['checkpoint_payloads_prospectively_transient']
    return packet


class Rows:
    def __init__(self, record, count, bitcount, states=N, weighted=False):
        self.path = Path(record['path'])
        assert r.source(self.path) == record
        PATHS.add(self.path)
        self.count, self.states = count, states
        self.bits = [tuple(max(0, -((i - (P if k <= R else P - k)) // 8)) for i in range(8))
                     if weighted else (bitcount,) * 8 for k in range(count)]
        assert not weighted or count == P
        self.widths = [tuple((n + 7) // 8 for n in row) for row in self.bits]
        self.offsets = [0]
        for row in self.widths:
            self.offsets.append(self.offsets[-1] + sum(row))
        self.row_bytes = self.offsets[-1]
        assert self.path.stat().st_size == self.row_bytes * states
        self.file = self.path.open('rb')

    def row(self, state, count=None):
        count = self.count if count is None else count
        assert 0 <= state < self.states and 0 <= count <= self.count
        self.file.seek(state * self.row_bytes)
        raw = self.file.read(self.offsets[count])
        assert len(raw) == self.offsets[count]
        offset, out = 0, []
        for widths, bits in zip(self.widths[:count], self.bits[:count]):
            row = []
            for width, bound in zip(widths, bits):
                value = int.from_bytes(raw[offset:offset + width], 'little')
                offset += width
                assert 0 <= value < 1 << bound
                row.append(value)
            out.append(tuple(row))
        assert offset == len(raw)
        return out

    def __getitem__(self, state):
        return self.row(state)

    def close(self):
        self.file.close()


def final_state():
    packet = read(BASE + '_verified_d129')
    assert packet['certificate']['original_full_residual_zero']
    assert packet['certificate']['actual_new_precision_pi'] == P
    return packet, Rows(packet['state_file'], P, 400)


def states():
    packet, values = final_state()
    assert packet['certificate']['full_residual_uses_different_polynomial_backend_from_lift']
    path = Path(packet['residual_file']['path'])
    assert path.stat().st_size == N * P * 8 * 50
    with path.open('rb') as f:
        while raw := f.read(1 << 20):
            assert not any(raw)
    old = read('dyadic_weighted_P1600_col00_verified_d124')
    seed = Rows(old['state_file'], 1600, 200)
    mask = (1 << 200) - 1
    masses = read('dyadic_harmonic_certificate_d111')['harmonic_basis'][0]
    for e, mass in enumerate(masses):
        row = values.row(e, 1600)
        assert [tuple(v & mask for v in x) for x in row] == seed.row(e)
        assert row[0] == (mass & ((1 << 400) - 1),) + (0,) * 7
    seed.close()
    maps = read('dyadic_target_transports_d121')['transitions']
    ring, checked = r.Quotient(r.FP, P), 0
    for state in maps:
        for child in state['children']:
            aa, b, c = [ring.norm(x) for x in child['normalized_center'][:3]]
            assert child['normalized_error_pi'] >= P
            assert ring.value(c) >= 1 and ring.value(ring.sub(aa, ring.mul(b, c))) >= 1
    for e in (0, 98, 173):
        totals = a.recurrence(ring, maps, values, e, (1, 2, 33, 64), P)
        expected = values.row(e, 65)
        for n, x in totals.items():
            assert x == expected[n]
            checked += 8
    values.close()
    sweeps = {}
    for path in DATA.glob(BASE + '_*_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json'):
        row = read(path.stem, retained=False)
        assert r.source(row['input_metadata']['path']) == row['input_metadata']
        sweeps.setdefault((row['input_metadata']['path'], row['purpose']), []).append((row['first_state'], row['last_state']))
    assert len(sweeps) == 101
    for (_, purpose), rows in sweeps.items():
        assert len(rows) == (6 if purpose in ('seed-low-rhs', 'correction-low-rhs') else 29)
        cursor = 0
        for first, last in sorted(rows):
            assert first == cursor and last >= first
            cursor = last + 1
        assert cursor == N
    return {'production_full_original_residual_scalar_checks': N * P * 8,
        'old_P1600_low_scalar_overlaps': N * 1600 * 8, 'exact_masses_checked': N,
        'child_column_divisibility_checks': 348, 'independent_original_recurrence_scalar_checks': checked,
        'complete_disjoint_sweeps_checked': len(sweeps), 'complete_long_bank_decoded': False}


def seed_block(branch, block):
    assert branch in (0, 1) and 0 <= block < len(STOPS)
    ring = r.Quotient(r.FP, 1600)
    transport = read('dyadic_target_transports_d121')
    child = transport['transitions'][0]['children'][branch]
    aa, b, c = [ring.norm(x) for x in child['normalized_center'][:3]]
    start, stop = (0 if block == 0 else STOPS[block - 1]), STOPS[block]
    if block == 0:
        power = [ring.one] + [ring.zero] * 1599
    else:
        prior = read(f'dyadic_P3200_audit_seed_b{branch}_k{block-1:02d}_d129')
        assert prior['certificates']['branch'] == branch and prior['certificates']['last_degree'] == start
        source = Rows(prior['checkpoint_files'][0], 1600, 200, states=1)
        power = source.row(0)
        source.close()
    for n in range(start + 1, stop + 1):
        new = [ring.mul(b, power[0])]
        for k in range(1, 1600):
            new.append(ring.sub(ring.add(ring.mul(b, power[k]), ring.mul(aa, power[k - 1])), ring.mul(c, new[-1])))
        power = new
    contribution = None
    if stop in (1600, 2399, 3199):
        old = read('dyadic_weighted_P1600_col00_verified_d124')
        source = Rows(old['state_file'], 1600, 200)
        value = ring.zero
        for x, y in zip(power, source.row(child['target_edge'])):
            value = ring.add(value, ring.mul(x, y))
        contribution = list(value)
        source.close()
    path = DATA / f'dyadic_P3200_audit_seed_b{branch}_k{block:02d}_d129_power.bin'
    raw = b''.join(v.to_bytes(25, 'little') for row in power for v in row)
    assert len(raw) == 320000
    with path.open('xb') as f:
        f.write(raw)
    file = r.source(path)
    return {'branch': branch, 'block': block, 'state': 0, 'target_child': child['target_edge'],
        'first_input_degree': start, 'last_degree': stop, 'recurrence_steps': stop - start,
        'coefficient_count': 1600, 'modulus_pi': 1600,
        'known_old_moment_contribution': contribution, 'checkpoint_files': [file]}


def seed_final():
    packet, values = final_state()
    ring = r.Quotient(r.FP, 1600)
    totals = {n: ring.zero for n in (1600, 2399, 3199)}
    for branch in (0, 1):
        before = 0
        for block, stop in enumerate(STOPS):
            row = read(f'dyadic_P3200_audit_seed_b{branch}_k{block:02d}_d129')['certificates']
            assert row['branch'] == branch and row['block'] == block
            assert row['first_input_degree'] == before and row['last_degree'] == stop
            assert row['recurrence_steps'] == stop - before and row['coefficient_count'] == 1600
            before = stop
            if stop in totals:
                assert row['known_old_moment_contribution'] is not None
                totals[stop] = ring.add(totals[stop], tuple(row['known_old_moment_contribution']))
            else:
                assert row['known_old_moment_contribution'] is None
    expected = values.row(0)
    for n, value in totals.items():
        assert value == ring.norm(expected[n])
    values.close()
    assert packet['certificate']['old_extended_scalar_overlaps_checked'] == 4454400
    return {'independent_high_seed_degrees': list(totals), 'independent_high_seed_scalar_checks': 24,
        'independent_recurrence_blocks': 16, 'production_old_extended_scalar_overlaps': 4454400,
        'retired_production_seed_payloads_replayed': False}


def weighted():
    _, values = final_state()
    row = read(BASE + '_step48_d129')
    assert row['active_moment_count'] == 33 and row['weighted_residual_lower_bound_pi'] == 3184
    center = Rows(row['state_file'], P, 400, weighted=True)
    ring = r.Quotient(r.FP, P)
    for e in range(N):
        full, partial = values.row(e), center.row(e)
        assert full[0] == partial[0]
        for k, (x, y) in enumerate(zip(full, partial)):
            assert ring.value(ring.sub(x, y)) >= (P if k <= R else P - k)
    values.close()
    center.close()
    assert row['residual_power_of_two_shift'] == 398
    residual = Rows(row['residual_file'], 33, 2)
    for e in range(N):
        assert all(x == ring.zero for x in residual.row(e))
    residual.close()
    pilot = read('dyadic_streamed_pilot_P3200_col00_d129')
    assert pilot['completed_phases'] == 1905 and pilot['correction_steps'] == 48
    before = 1600
    for item in pilot['correction_history']:
        assert item['before_pi'] == before and item['after_pi'] == before + 33
        before = item['after_pi']
    assert before == 3184
    for step in range(49):
        suffix = 'seed' if step == 0 else f'step{step:02d}'
        historical = read(BASE + '_' + suffix + '_d129', retained=False)
        assert historical['weighted_residual_lower_bound_pi'] == 1600 + 33 * step
        assert historical['active_moment_count'] == max(33, 1600 - 33 * step)
    return {'final_weighted_reference_scalar_checks': N * P * 8,
        'final_scaled_residual_scalar_checks': N * 33 * 8, 'checkpoint_metadata_checked': 49,
        'recorded_correction_gains_checked': 48, 'retired_intermediate_payloads_replayed': False,
        'final_fixed_mass_original_residual_is_iteration_independent': True}


class CMRows:
    def __init__(self, packet):
        self.readers = []
        cursor = 0
        for item in packet['moment_chunks']:
            assert item['first_chart'] == cursor and cursor <= item['last_chart'] < 17
            assert r.source(item['metadata']['path']) == item['metadata']
            PATHS.add(Path(item['metadata']['path']))
            count = item['last_chart'] - cursor + 1
            self.readers.append((cursor, item['last_chart'], Rows(item['file'], 6400, 400, states=count)))
            cursor += count
        assert cursor == 17 and len(self.readers) == 6

    def row(self, chart):
        for first, last, source in self.readers:
            if first <= chart <= last:
                return source.row(chart - first)
        raise AssertionError(chart)

    def close(self):
        for _, _, source in self.readers:
            source.close()


def coarse(first, last):
    assert (first, last) in ((0, 5), (6, 11), (12, 16))
    cm = read('dyadic_CM_P3200_col00_d129')
    assert cm['coarse_error_beta'] == [6432, 6448, 6432, 6464]
    source = CMRows(cm)
    old = read('dyadic_CM_P1600_col00_d124')
    previous = Rows(old['checkpoint_files'][0], 3200, 200, states=17)
    ring = r.Quotient(r.MP, 6464)
    pi = ring.sub(ring.scale(ring.one, -2), ring.mul(ring.beta, ring.beta))
    q = ring.sub(tuple(r.MP[1:]), ring.beta)
    assert ring.mul(q, ring.beta) == pi
    powers = [ring.one]
    for _ in range(7):
        powers.append(ring.mul(powers[-1], pi))
    kernels = []
    for order in range(4):
        n = 2 * order + 2
        kernels.append([0] + [-sum(comb(n, i) * comb(n + k - i - 1, k - i)
            for i in range(min(n, k) + 1)) for k in range(1, 6400)])
    _, actual = final_state()
    transports = read('dyadic_target_transports_d121')
    maps = transports['transitions']
    charts = [x for x in transports['CM_charts'] if x['chart'] == 'A']
    small, checked, recurrences = r.Quotient(r.FP, P), 0, 0
    for ci in range(first, last + 1):
        values = source.row(ci)
        assert [tuple(v & ((1 << 200) - 1) for v in x) for x in values[:3200]] == previous.row(ci)
        embedded = []
        for row in values:
            x = ring.zero
            for coefficient, power in zip(row, powers):
                x = ring.add(x, ring.scale(power, coefficient))
            embedded.append(x)
        for order, cs in enumerate(kernels):
            x = ring.zero
            for coefficient, moment in reversed(list(zip(cs, embedded))):
                x = ring.add(ring.mul(x, q), ring.scale(moment, coefficient))
            assert x == tuple(cm['CM_values'][ci]['coarse_coefficients_beta'][order])
            assert ring.value(ring.sub(x, tuple(old['CM_values'][ci]['coarse_coefficients_beta'][order]))) >= old['coarse_error_beta'][order]
            checked += 1
        if ci not in (0, 8, 16):
            continue
        A, B, C = [small.norm(x) for x in charts[ci]['normalized_center'][:3]]
        assert charts[ci]['normalized_error_pi'] >= P and small.value(C) >= 1
        children = []
        for child in maps[charts[ci]['target_edge']]['children']:
            aa, bb, cc = [small.norm(x) for x in child['normalized_center'][:3]]
            denominator = small.add(small.one, small.mul(C, bb))
            inverse = small.one
            for _ in range(P.bit_length()):
                inverse = small.mul(inverse, small.sub(small.scale(small.one, 2), small.mul(denominator, inverse)))
            assert small.mul(denominator, inverse) == small.one
            pars = [small.mul(small.add(small.mul(A, aa), small.mul(B, cc)), inverse),
                small.mul(small.add(small.mul(A, bb), B), inverse),
                small.mul(small.add(cc, small.mul(C, aa)), inverse)]
            assert small.value(pars[2]) >= 1 and small.value(small.sub(pars[0], small.mul(pars[1], pars[2]))) >= 1
            children.append({'normalized_center': pars, 'target_edge': child['target_edge']})
        totals = a.recurrence(small, [{'children': children}], actual, 0, (1, 2, 7), P)
        for n, x in totals.items():
            assert x == values[n]
            recurrences += 8
    source.close()
    previous.close()
    actual.close()
    return {'first_chart': first, 'last_chart': last, 'independent_coarse_values_checked': checked,
        'independent_CM_recurrence_scalar_checks': recurrences,
        'old_CM_scalar_overlaps': (last - first + 1) * 3200 * 8,
        'new_CM_scalar_coefficients': (last - first + 1) * 6400 * 8,
        'old_coarse_values_checked': checked, 'coarse_error_beta': [6432, 6448, 6432, 6464]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('states', 'seed-block', 'seed-final', 'weighted', 'coarse'))
    parser.add_argument('--branch', type=int)
    parser.add_argument('--block', type=int)
    parser.add_argument('--first', type=int)
    parser.add_argument('--last', type=int)
    args = parser.parse_args()
    if args.phase == 'seed-block':
        label = f'seed_b{args.branch}_k{args.block:02d}'
    elif args.phase == 'coarse':
        label = f'coarse_c{args.first:02d}_{args.last:02d}'
    else:
        label = args.phase.replace('-', '_')
    out = DATA / ('dyadic_P3200_audit_' + label + '_d129.json')
    assert not out.exists()
    start = time.monotonic()
    if args.phase == 'seed-block':
        cert = seed_block(args.branch, args.block)
    elif args.phase == 'coarse':
        cert = coarse(args.first, args.last)
    else:
        cert = {'states': states, 'seed-final': seed_final, 'weighted': weighted}[args.phase]()
    files = cert.pop('checkpoint_files', [])
    result = {'status': 'pass', 'milestone': 'D129', 'phase': args.phase,
        'working_precision_pi': P, 'harmonic_basis_column': 0, 'certificates': cert,
        'checkpoint_files': files, 'full_sixteen_column_bank_precision_pi': 800,
        'production_arithmetic_not_imported': True, 'positive_exact_quadric_vanishing_proved': False,
        'candidate_identification_proved': False, 'target_field_polynomial_constructed': False,
        'wall_seconds': time.monotonic() - start,
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
        'sources': [r.source(path) for path in sorted(PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'sources'}), flush=True)
    print('PASS|531_DYADIC_PRECISION3200_INDEPENDENT', flush=True)
