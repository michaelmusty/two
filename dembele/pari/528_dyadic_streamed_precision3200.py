"""D129 actual P=3200 column with selective serial phases and reserved row writes.

Only the new prospectively temporary namespace can be retired. Every
file reserves its complete size under the common lock before computation;
individual state rows are then written without serializing other workers.
Original GMP reconstruction and verification supply the final certificate.
"""
import argparse
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import time

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / 'dembele/data/computed'
DATA = META / 'dyadic_streamed_scratch_col00_d129'
CAP, P, R, N = 2 * (1 << 30), 3200, 32, 174
s = importlib.util.spec_from_file_location('rolling', ROOT / 'dembele/pari/519_dyadic_rolling_precision_chunks.py')
w = importlib.util.module_from_spec(s)
s.loader.exec_module(w)
h, b, l, p, a, c, q = w.h, w.b, w.l, w.p, w.a, w.c, w.q
ZERO = b.ZERO
NEW_PAYLOADS = []


def scratch_bytes():
    assert DATA.is_dir() and not DATA.is_symlink() and not (DATA / 'SEALED.json').exists()
    owner = json.loads((DATA / 'OWNER.json').read_text())
    assert owner['namespace'] == 'D129-column0' and owner['driver'] == h.source(Path(__file__))
    paths = list(DATA.iterdir())
    assert all(x.is_file() and not x.is_symlink() for x in paths)
    size = sum(x.stat().st_size for x in paths)
    assert size <= CAP
    return size


def scale(row, shift):
    return [tuple(v << shift for v in x) for x in row]


def project(row):
    assert len(row) <= P
    return [tuple(v & mask for v, mask in zip(x, masks)) for x, masks in zip(row, w.masks(P))]


class RowWriter:
    def __init__(self, stem, label, count, shift=0, weighted=False, states=N):
        assert re.fullmatch(r'[A-Za-z0-9_-]+', stem)
        assert count > 0 and states > 0 and 0 <= shift < P // 8
        assert not weighted or (count == P and shift == 0)
        self.path = DATA / (stem + '_' + label + '.bin')
        self.count, self.shift, self.weighted, self.states = count, shift, weighted, states
        self.row_bytes = (sum((w.bits(P, k, i) + 7) // 8 for k in range(P) for i in range(8))
                          if weighted else count * 8 * ((P // 8 - shift + 7) // 8))
        self.size, self.rows, self.maximum_serialized_bytes = self.row_bytes * states, 0, 0
        with (DATA / '.write.lock').open('a+b') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            before = scratch_bytes()
            assert before + self.size <= CAP, 'scratch reservation exceeds cap'
            self.file = self.path.open('x+b')
            self.file.truncate(self.size)
            self.file.flush()
            assert self.path.stat().st_size == self.size and scratch_bytes() <= CAP
        # The reserved file length accounts for all future writes. A partial
        # file is never accepted without its final passing phase receipt.
        self.file.seek(0)

    def append(self, row):
        assert self.rows < self.states and len(row) == self.count
        assert all(len(x) == 8 for x in row)
        if self.weighted:
            raw = bytearray()
            for k, x in enumerate(row):
                for i, v in enumerate(x):
                    bits = w.bits(P, k, i)
                    assert 0 <= v < 1 << bits
                    raw.extend(v.to_bytes((bits + 7) // 8, 'little'))
        else:
            assert all(0 <= v < 1 << (P // 8) and not (v & ((1 << self.shift) - 1)) for x in row for v in x)
            raw = b.pack([[tuple(v >> self.shift for v in x) for x in row]], P // 8 - self.shift)
        assert len(raw) == self.row_bytes
        assert self.file.tell() == self.rows * self.row_bytes
        assert self.file.write(raw) == len(raw)
        self.rows += 1
        self.maximum_serialized_bytes = max(self.maximum_serialized_bytes, len(raw))

    def finish(self):
        assert self.rows == self.states and self.file.tell() == self.size
        self.file.flush()
        os.fsync(self.file.fileno())
        self.file.close()
        assert self.path.stat().st_size == self.size
        record = h.source(self.path)
        NEW_PAYLOADS.append({'source': record, 'bytes': self.size,
            'layout': {'precision_pi': P, 'states': self.states, 'moments': self.count,
                'binary_shift': self.shift, 'weighted': self.weighted},
            'maximum_serialized_row_bytes': self.maximum_serialized_bytes,
            'full_size_reserved_before_writes': True})
        return record


def state_reader(packet, key='state_file', count=P, shift=0, weighted=False):
    return q.StateReader(packet[key], count, P // 8 - shift,
        weighted_precision=P if weighted else None)


def sweep_rows(previous, prefix, purpose, backend):
    prior, path = h.read(previous)
    assert prior['working_precision_pi'] == P
    rows, cursor, count = [], 0, None
    for item in sorted(META.glob(prefix + '_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json')):
        row, _ = h.read(item.stem)
        assert row['kind'] == 'operator_chunk' and row['input_metadata'] == h.source(path)
        assert row['purpose'] == purpose and row['backend'] == backend and row['working_precision_pi'] == P
        assert row['first_state'] == cursor and cursor <= row['last_state'] < N
        count = row['output_count'] if count is None else count
        assert row['output_count'] == count
        rows.append(row)
        cursor = row['last_state'] + 1
    assert cursor == N and len(rows) == (6 if purpose in ('seed-low-rhs', 'correction-low-rhs') else 29)
    for row in rows:
        shift = row['operator_power_of_two_shift']
        source = q.StateReader(row['checkpoint_files'][0], count, P // 8 - shift,
            states=row['last_state'] - row['first_state'] + 1)
        for i in range(source.states):
            yield row['first_state'] + i, scale(source.row(i), shift)
        source.close()


class Engine(h.Engine):
    def __init__(self):
        super().__init__(P)
        control, _ = h.read('dyadic_adaptive_kernel_control_d124')
        for path in (Path(a.__file__), a.CSOURCE, a.LIBRARY):
            expected = [r for r in control['sources'] if Path(r['path']) == path]
            assert len(expected) == 1 and h.source(path) == expected[0]
            h.PATHS.add(path)

    def original_low(self, values, bits):
        algebra = b.Algebra(bits)
        groups = {}
        for e in range(N):
            for branch, child in enumerate(self.targets[e]):
                pars = tuple(tuple(v & algebra.mask for v in x) for x in self.params[e][branch])
                groups.setdefault(pars, []).append((e, child))
        result = list(values)
        for pars, destinations in groups.items():
            block = b.coefficients(pars, R, algebra)
            for e, child in destinations:
                result[e] = algebra.sub(result[e], algebra.mul(block, values[child]))
            del block
        return result

    def solve_rhs(self, rhs, bits):
        start = time.monotonic()
        if bits <= 200:
            factor = c.FactorReader(bits)
            answer = factor.solve(rhs, b.Algebra(bits))
            assert factor.decoded_blocks == 1226
            checks = divisions = 0
        else:
            assert bits == 400
            control, _ = h.read('dyadic_factor_reuse_P3200_d127')
            assert control['certificates']['original_sparse_scalar_equations_checked'] == 89088
            factor = c.FactorReader(200)
            mask = (1 << 200) - 1
            x0 = factor.solve([b.reduce(edge, mask) for edge in rhs], b.Algebra(200))
            applied = self.original_low(x0, 400)
            residual = [b.Algebra(400).sub(edge, value) for edge, value in zip(rhs, applied)]
            assert all(v & mask == 0 for edge in residual for row in edge for x in row for v in x)
            quotient = [[[tuple(v >> 200 for v in x) for x in row] for row in edge] for edge in residual]
            delta = factor.solve(quotient, b.Algebra(200))
            answer = [[[tuple(u + (v << 200) for u, v in zip(x, d)) for x, d in zip(row, dr)]
                       for row, dr in zip(edge, de)] for edge, de in zip(x0, delta)]
            assert self.original_low(answer, 400) == rhs and factor.decoded_blocks == 2452
            checks = divisions = N * R * 8
        factor.close()
        self.times.append({'operation': 'streamed_existing_factor_low_solve', 'modulus_bits': bits,
            'factor_blocks_decoded': factor.decoded_blocks, 'maximum_decoded_factor_blocks': 1,
            'higher_precision_original_sparse_scalar_checks': checks,
            'exact_residual_divisions_checked': divisions, 'larger_factor_built': False,
            'factor_read_decode_seconds': factor.read_seconds, 'seconds': time.monotonic() - start})
        return answer

    def apply_rows(self, file, count, weighted, shift, rows, first, last, backend, zero_low):
        start = time.monotonic()
        bits, cut = P // 8 - shift, min(count, P - 8 * shift)
        assert not weighted or shift == 0
        source = q.StateReader(file, count, bits, weighted_precision=P if weighted else None)
        ring = (p.Ring if backend == 'GMP' else a.Ring)(bits)
        for e in range(first, last + 1):
            total = [ZERO] * rows
            for branch, child in enumerate(self.targets[e]):
                values = source.row(child, cut)
                if zero_low:
                    values[1:R + 1] = [ZERO] * min(R, max(0, cut - 1))
                pars = tuple(tuple(v & ring.mask for v in x) for x in self.params[e][branch])
                plan = l.Plan(ring, *pars, cut, rows)
                total = ring.padd(total, plan.apply(values))
                del plan, values
            assert len(total) == rows
            yield scale(total, shift)
        source.close()
        self.times.append({'operation': 'selective_original_operator_chunk', 'backend': backend,
            'first_state': first, 'last_state': last, 'known_binary_shift': shift, 'modulus_bits': bits,
            'input_count': cut, 'output_count': rows, 'zero_positive_low_inputs': zero_low,
            'maximum_prepared_maps_held': 1, 'maximum_decoded_input_rows': 1,
            'output_rows_serialized_individually': True, 'reader_statistics': source.stats(),
            'seconds': time.monotonic() - start})


def baseline(result, previous):
    for key in ('working_precision_pi', 'seed_precision_pi', 'harmonic_basis_column', 'seed_stem',
                'correction_history', 'seed_input_stem', 'seed_extension_prefix'):
        if key in previous:
            result[key] = previous[key]


def old_reader(packet):
    old, _ = h.read(packet['seed_stem'])
    assert old['certificate']['original_full_residual_zero'] and old['working_precision_pi'] == 1600
    return q.StateReader(old['state_file'], 1600, 200)


def check_old_row(values, expected):
    assert [tuple(v & ((1 << 200) - 1) for v in x) for x in values[:1600]] == expected


def residual_fields(result, record, u, count):
    result.update(residual_file=record, residual_power_of_two_shift=u // 8,
        active_moment_count=count, weighted_residual_lower_bound_pi=u)


def run(args):
    start, initial = time.monotonic(), scratch_bytes()
    phase, stem = args.phase, args.output
    result = {'status': 'pass', 'milestone': 'D129', 'phase': phase, 'working_precision_pi': P,
        'eliminated_positive_moments': R, 'harmonic_basis_column': 0,
        'actual_moment_precision_increased': False, 'full_sixteen_column_bank_precision_pi': 800}
    engine = None
    if phase == 'writer-control':
        left = RowWriter(stem, 'probe_a', 7, shift=17, states=2)
        right = RowWriter(stem, 'probe_b', 5, states=3)
        aa, bb = b.k.data(2, 7, 383, 'D129-write-left'), b.k.data(3, 5, 400, 'D129-write-right')
        try:
            left.append([ZERO] * 6)
        except AssertionError:
            pass
        else:
            raise AssertionError('wrong-length row accepted')
        left.append(scale(aa[0], 17))
        right.append(bb[0])
        left.append(scale(aa[1], 17))
        right.append(bb[1])
        right.append(bb[2])
        files = [left.finish(), right.finish()]
        assert Path(files[0]['path']).read_bytes() == b.pack(aa, 383)
        assert Path(files[1]['path']).read_bytes() == b.pack(bb, 400)
        try:
            RowWriter(stem, 'rejected', P, states=1740)
        except AssertionError as exc:
            assert str(exc) == 'scratch reservation exceeds cap'
        else:
            raise AssertionError('oversized reservation accepted')
        assert not (DATA / (stem + '_rejected.bin')).exists()
        result.update(kind='writer_control', checkpoint_files=files,
            certificate={'interleaved_reserved_files_checked': 2, 'direct_byte_comparisons': 11376,
                'wrong_length_row_rejections': 1, 'oversized_reservation_rejections': 1,
                'partial_files_never_accepted_without_pass_receipt': True})
    elif phase == 'init':
        old, oldpath = h.read(args.seed)
        assert old['working_precision_pi'] == 1600 and old['harmonic_basis_column'] == 0
        assert old['certificate']['original_full_residual_zero']
        source = q.StateReader(old['state_file'], 1600, 200)
        masses, _ = h.read('dyadic_harmonic_certificate_d111')
        target = RowWriter(stem, 'input', 1600)
        for e, mass in enumerate(masses['harmonic_basis'][0]):
            values = source.row(e)
            values[0] = (mass & ((1 << 400) - 1),) + (0,) * 7
            target.append(values)
        source.close()
        file = target.finish()
        result.update(seed_precision_pi=1600, seed_stem=args.seed, seed_input_stem=stem,
            kind='initial_input', input_count=1600, operator_input_file=file,
            correction_history=[], checkpoint_files=[file], verified_seed_metadata=h.source(oldpath))
    else:
        previous, path = h.read(args.previous)
        baseline(result, previous)
        assert result['working_precision_pi'] == P and result['seed_precision_pi'] == 1600
        assert result['harmonic_basis_column'] == 0
        result['previous_metadata'] = h.source(path)
        engine = Engine()
        if phase == 'sweep':
            purpose = args.purpose
            backend = 'GMP' if purpose in ('reconstruct', 'verify') else 'ADAPTIVE'
            maximum = 29 if purpose in ('seed-low-rhs', 'correction-low-rhs') else 6
            assert 0 <= args.first <= args.last < N and args.last - args.first < maximum
            weighted, shift, zero_low = False, 0, False
            if purpose == 'extend':
                assert previous['kind'] == 'initial_input'
                file, count, rows = previous['operator_input_file'], previous['input_count'], P
            elif purpose in ('seed-low-rhs', 'seed-residual'):
                assert previous['kind'] == ('weighted_seed' if purpose == 'seed-low-rhs' else 'weighted_low_seed')
                file, count, weighted = previous['state_file'], P, True
                zero_low = purpose == 'seed-low-rhs'
                rows = R + 1 if zero_low else 1600
            elif purpose == 'correction-low-rhs':
                assert previous['kind'] == 'checkpoint' and previous['active_moment_count'] > R + 1
                file, count = previous['residual_file'], previous['active_moment_count']
                shift, rows, zero_low = previous['residual_power_of_two_shift'], R + 1, True
            elif purpose == 'correction':
                assert previous['kind'] == 'prepared_correction'
                file, count = previous['operator_input_file'], previous['input_count']
                shift, rows = previous['correction_power_of_two_shift'], previous['next_active_moment_count']
            elif purpose == 'reconstruct':
                assert previous['kind'] == 'checkpoint' and previous['active_moment_count'] == R + 1
                file, count, weighted, rows = previous['state_file'], P, True, P
            elif purpose == 'verify':
                assert previous['kind'] == 'reconstructed'
                file, count, rows = previous['state_file'], P, P
            else:
                raise AssertionError(purpose)
            target = RowWriter(stem, 'operator', rows, shift, states=args.last - args.first + 1)
            for values in engine.apply_rows(file, count, weighted, shift, rows, args.first, args.last, backend, zero_low):
                target.append(values)
            file = target.finish()
            result.update(kind='operator_chunk', purpose=purpose, input_metadata=h.source(path), backend=backend,
                first_state=args.first, last_state=args.last, output_count=rows,
                operator_power_of_two_shift=shift, checkpoint_files=[file])
        elif phase == 'seed-assemble':
            assert previous['kind'] == 'initial_input'
            old = old_reader(previous)
            target = RowWriter(stem, 'state', P, weighted=True)
            for e, values in sweep_rows(args.previous, args.chunks, 'extend', 'ADAPTIVE'):
                assert len(values) == P
                check_old_row(values, old.row(e))
                target.append(project(values))
            old.close()
            file = target.finish()
            result.update(kind='weighted_seed', state_file=file, checkpoint_files=[file],
                seed_extension_prefix=args.chunks, old_low_scalar_overlaps_checked=N * 1600 * 8)
        elif phase == 'seed-low-finish':
            assert previous['kind'] == 'weighted_seed'
            rhs = []
            for e, values in sweep_rows(args.previous, args.chunks, 'seed-low-rhs', 'ADAPTIVE'):
                assert e == len(rhs) and len(values) == R + 1
                rhs.append([[x] for x in values[1:]])
            answer = engine.solve_rhs(rhs, 400)
            old, source = old_reader(previous), state_reader(previous, weighted=True)
            target = RowWriter(stem, 'state', P, weighted=True)
            for e in range(N):
                values = source.row(e)
                values[1:R + 1] = [row[0] for row in answer[e]]
                check_old_row(values, old.row(e))
                target.append(values)
            source.close()
            old.close()
            file = target.finish()
            result.update(kind='weighted_low_seed', state_file=file, checkpoint_files=[file],
                old_low_scalar_overlaps_checked=N * 1600 * 8)
        elif phase == 'finish-seed':
            assert previous['kind'] == 'weighted_low_seed'
            source = state_reader(previous, weighted=True)
            target = RowWriter(stem, 'residual', 1600, shift=200)
            algebra = b.Algebra(400)
            for e, values in sweep_rows(args.previous, args.chunks, 'seed-residual', 'ADAPTIVE'):
                assert len(values) == 1600
                residual = project(algebra.sub([values], [source.row(e, 1600)])[0])
                assert all(x == ZERO for x in residual[:R + 1]) and l.value([residual], P) >= 1600
                target.append(residual)
            source.close()
            file = target.finish()
            residual_fields(result, file, 1600, 1600)
            result.update(kind='checkpoint', state_file=previous['state_file'],
                checkpoint_files=[previous['state_file'], file])
        elif phase == 'prepare-step':
            assert previous['kind'] == 'checkpoint'
            u, count = previous['weighted_residual_lower_bound_pi'], previous['active_moment_count']
            assert count == max(R + 1, P - u) and count > R + 1
            shift, rhs = u // 8, []
            for e, values in sweep_rows(args.previous, args.chunks, 'correction-low-rhs', 'ADAPTIVE'):
                assert e == len(rhs) and len(values) == R + 1
                assert all(not (v & ((1 << shift) - 1)) for x in values for v in x)
                rhs.append([[tuple(v >> shift for v in x)] for x in values[1:]])
            answer = engine.solve_rhs(rhs, 400 - shift)
            residual = state_reader(previous, 'residual_file', count, shift)
            source = state_reader(previous, weighted=True)
            target = RowWriter(stem, 'state', P, weighted=True)
            correction_writer = RowWriter(stem, 'correction', count, shift)
            for e in range(N):
                values = residual.row(e)
                assert all(x == ZERO for x in values[:R + 1]) and l.value([scale(values, shift)], P) >= u
                values[1:R + 1] = [row[0] for row in answer[e]]
                correction = scale(values, shift)
                assert l.value([correction], P) >= u
                current = source.row(e)
                for k, x in enumerate(correction):
                    current[k] = tuple((v + d) & mask for v, d, mask in zip(current[k], x, w.masks(P)[k]))
                target.append(current)
                correction_writer.append(correction)
            residual.close()
            source.close()
            state, file = target.finish(), correction_writer.finish()
            result.update(kind='prepared_correction', state_file=state, operator_input_file=file,
                input_count=count, before_pi=u, after_pi=min(P, u + R + 1),
                next_active_moment_count=max(R + 1, P - u - R - 1),
                correction_power_of_two_shift=shift, checkpoint_files=[state, file])
        elif phase == 'finish-step':
            assert previous['kind'] == 'prepared_correction'
            count, u = previous['next_active_moment_count'], previous['after_pi']
            source = state_reader(previous, 'operator_input_file', previous['input_count'], previous['correction_power_of_two_shift'])
            target = RowWriter(stem, 'residual', count, shift=u // 8)
            for e, values in sweep_rows(args.previous, args.chunks, 'correction', 'ADAPTIVE'):
                assert len(values) == count
                assert values[:R + 1] == scale(source.row(e, R + 1), previous['correction_power_of_two_shift'])
                values[:R + 1] = [ZERO] * (R + 1)
                residual = project(values)
                assert l.value([residual], P) >= u
                target.append(residual)
            source.close()
            file = target.finish()
            residual_fields(result, file, u, count)
            history = previous['correction_history'] + [{'before_pi': previous['before_pi'], 'after_pi': u,
                'input_moments': previous['input_count'], 'output_moments': count}]
            result.update(kind='checkpoint', state_file=previous['state_file'],
                checkpoint_files=[previous['state_file'], file], correction_history=history)
        elif phase == 'finish-reconstruct':
            assert previous['kind'] == 'checkpoint' and previous['active_moment_count'] == R + 1
            assert previous['weighted_residual_lower_bound_pi'] + R + 1 >= P
            old, source = old_reader(previous), state_reader(previous, weighted=True)
            extended = sweep_rows(previous['seed_input_stem'], previous['seed_extension_prefix'], 'extend', 'ADAPTIVE')
            target = RowWriter(stem, 'state', P)
            for e, values in sweep_rows(args.previous, args.chunks, 'reconstruct', 'GMP'):
                assert len(values) == P and project(values) == source.row(e)
                check_old_row(values, old.row(e))
                j, prior = next(extended)
                assert e == j
                assert [tuple(v & ((1 << 200) - 1) for v in x) for x in values] == [
                    tuple(v & ((1 << 200) - 1) for v in x) for x in prior]
                target.append(values)
            assert next(extended, None) is None
            old.close()
            source.close()
            file = target.finish()
            result.update(kind='reconstructed', state_file=file, checkpoint_files=[file],
                weighted_state_metadata=h.source(path), weighted_residual_condition_checked=True,
                weighted_residual_scalar_checks=N * P * 8,
                old_low_scalar_overlaps_checked=N * 1600 * 8,
                old_extended_scalar_overlaps_checked=N * P * 8)
        elif phase == 'finish-verify':
            assert previous['kind'] == 'reconstructed' and previous['weighted_residual_condition_checked']
            source = state_reader(previous)
            target = RowWriter(stem, 'residual', P)
            masses, _ = h.read('dyadic_harmonic_certificate_d111')
            for e, values in sweep_rows(args.previous, args.chunks, 'verify', 'GMP'):
                assert len(values) == P and values == source.row(e)
                assert values[0] == (masses['harmonic_basis'][0][e] & ((1 << 400) - 1),) + (0,) * 7
                target.append([ZERO] * P)
            source.close()
            file = target.finish()
            result.update(kind='verified', state_file=previous['state_file'], residual_file=file,
                checkpoint_files=[previous['state_file'], file], residual_lower_bound_pi=P,
                actual_moment_precision_increased=True, weighted_state_metadata=previous['weighted_state_metadata'],
                certificate={'original_full_residual_zero': True, 'actual_new_precision_pi': P,
                    'scalar_coefficients_checked': N * P * 8, 'weighted_residual_condition_checked': True,
                    'old_low_scalar_overlaps_checked': previous['old_low_scalar_overlaps_checked'],
                    'old_extended_scalar_overlaps_checked': previous['old_extended_scalar_overlaps_checked'],
                    'exact_masses_checked': N, 'full_residual_uses_different_polynomial_backend_from_lift': True})
        else:
            raise AssertionError(phase)
    h.PATHS.update(c.h.PATHS)
    h.PATHS.update([Path(__file__), Path(w.__file__), Path(h.__file__), Path(a.__file__), a.CSOURCE, a.LIBRARY,
        Path(c.__file__), Path(q.__file__), Path(b.__file__), Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY,
        META / 'dyadic_selective_scaling_review_d128.json'])
    result.update(timings=engine.times if engine else [], wall_seconds=time.monotonic() - start,
        peak_rss_bytes=w.peak_rss(), scratch_bytes_before=initial, scratch_bytes_after=scratch_bytes(),
        scratch_limit_bytes=CAP, checkpoint_payloads_prospectively_transient=True, new_payloads=NEW_PAYLOADS,
        sources=[h.source(x) for x in sorted(h.PATHS) if not x.resolve().is_relative_to(DATA.resolve())])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('writer-control', 'init', 'sweep', 'seed-assemble',
        'seed-low-finish', 'finish-seed', 'prepare-step', 'finish-step', 'finish-reconstruct', 'finish-verify'))
    parser.add_argument('--output', required=True)
    parser.add_argument('--previous')
    parser.add_argument('--seed')
    parser.add_argument('--chunks')
    parser.add_argument('--purpose', choices=('extend', 'seed-low-rhs', 'seed-residual', 'correction-low-rhs',
        'correction', 'reconstruct', 'verify'))
    parser.add_argument('--first', type=int)
    parser.add_argument('--last', type=int)
    args = parser.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    output = META / (args.output + '.json')
    assert not output.exists()
    result = run(args)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(h.source(output)), flush=True)
    print('STREAMED_PHASE|' + json.dumps({k: result[k] for k in ('phase', 'wall_seconds', 'peak_rss_bytes',
        'scratch_bytes_after')} | {k: result[k] for k in ('weighted_residual_lower_bound_pi', 'active_moment_count') if k in result}), flush=True)
    print('PASS|528_DYADIC_STREAMED_PRECISION3200', flush=True)
