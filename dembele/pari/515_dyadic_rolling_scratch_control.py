"""D126 bounded, prospective scratch store with real checkpoint crash controls.

Only this newly created, marked directory is mutable. Frozen D124 files
are read as control inputs. The control replays stored checkpoints; it
does not implement a new arithmetic refinement. Process-crash recovery
is tested explicitly; power-loss durability is not claimed.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
SCRATCH = DATA / 'dyadic_rolling_scratch_d126'
s = importlib.util.spec_from_file_location('selective', ROOT / 'dembele/pari/514_dyadic_selective_state_control.py')
q = importlib.util.module_from_spec(s)
s.loader.exec_module(q)
h, w = q.h, q.w
OWNER = {'schema': 'D126-prospective-scratch-v1', 'driver': h.source(Path(__file__))}
MAX_GENERATION_PAYLOAD = 28831800 + 14476800
CAP = 2 * MAX_GENERATION_PAYLOAD + (1 << 20)


def durable_json(path, value):
    with path.open('x') as f:
        f.write(json.dumps(value, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())


def fault(point, selected):
    if point == selected:
        os._exit(86)  # Deliberate abrupt child exit, checked by the parent.


class Store:
    def __init__(self, create=False):
        if create:
            SCRATCH.mkdir()
            durable_json(SCRATCH / 'OWNER.json', OWNER)
        assert SCRATCH.is_dir() and not SCRATCH.is_symlink()
        assert SCRATCH.parent.resolve() == DATA.resolve()
        assert json.loads((SCRATCH / 'OWNER.json').read_text()) == OWNER
        assert not (SCRATCH / 'SEALED.json').exists()
        self.peak = 0
        self.observe()

    def observe(self):
        paths = list(SCRATCH.rglob('*'))
        assert all(not p.is_symlink() for p in paths)
        total = sum(p.stat().st_size for p in paths if p.is_file())
        assert total <= CAP, (total, CAP)
        self.peak = max(self.peak, total)
        return total

    def remove(self, path):
        assert path.parent == SCRATCH and not path.is_symlink()
        assert path.name == '.pending' or re.fullmatch(r'g[0-9]{6}', path.name)
        shutil.rmtree(path)

    def verify(self, generation):
        assert re.fullmatch(r'g[0-9]{6}', generation)
        path = SCRATCH / generation
        packet = json.loads((path / 'checkpoint.json').read_text())
        assert packet['generation'] == generation
        for row in packet['payloads']:
            assert row['name'] in ('state.bin', 'residual.bin')
            file = path / row['name']
            assert not file.is_symlink() and file.stat().st_size == row['bytes']
            assert h.source(file)['sha256'] == row['sha256']
        return packet

    def replace_head(self, value, selected=None):
        temporary = SCRATCH / 'HEAD.next'
        assert not temporary.exists()
        durable_json(temporary, value)
        fault('before_head', selected)
        os.replace(temporary, SCRATCH / 'HEAD.json')
        fault('after_head', selected)

    def recover(self):
        headpath = SCRATCH / 'HEAD.json'
        if headpath.exists():
            head = json.loads(headpath.read_text())
            try:
                self.verify(head['current'])
            except (AssertionError, OSError, ValueError):
                assert head['previous'] is not None
                self.verify(head['previous'])
                if (SCRATCH / 'HEAD.next').exists():
                    (SCRATCH / 'HEAD.next').unlink()
                head = {'current': head['previous'], 'previous': None}
                self.replace_head(head)
        else:
            head = {'current': None, 'previous': None}
        if (SCRATCH / 'HEAD.next').exists():
            (SCRATCH / 'HEAD.next').unlink()
        keep = {head['current'], head['previous']}
        for path in SCRATCH.iterdir():
            if path.is_dir() and path.name not in keep:
                self.remove(path)
        self.observe()
        return head

    def commit(self, input_stem, selected=None):
        head = self.recover()
        # Verify current before discarding its predecessor. During staging,
        # exactly one old complete generation and one pending generation live.
        if head['previous'] is not None:
            old = head['previous']
            head = {'current': head['current'], 'previous': None}
            self.replace_head(head)
            self.remove(SCRATCH / old)
        generation = 0 if head['current'] is None else int(head['current'][1:]) + 1
        name = f'g{generation:06d}'
        packet, inputpath = h.read(input_stem)
        assert packet['kind'] == 'checkpoint' and packet['working_precision_pi'] == 1600
        records = [packet['state_file'], packet['residual_file']]
        assert sum(Path(r['path']).stat().st_size for r in records) <= MAX_GENERATION_PAYLOAD
        pending = SCRATCH / '.pending'
        pending.mkdir()
        payloads = []
        for label, record in zip(('state.bin', 'residual.bin'), records):
            source = Path(record['path'])
            assert h.source(source) == record and source.parent.resolve() == DATA.resolve()
            with source.open('rb') as src, (pending / label).open('xb') as dst:
                while block := src.read(1 << 20):
                    dst.write(block)
                    dst.flush()
                    self.observe()
                    fault('mid_payload', selected)
                os.fsync(dst.fileno())
            copied = h.source(pending / label)
            assert copied['sha256'] == record['sha256']
            payloads.append({'name': label, 'sha256': copied['sha256'], 'bytes': source.stat().st_size})
        leaf = {key: packet[key] for key in ('working_precision_pi', 'harmonic_basis_column',
            'active_moment_count', 'weighted_residual_lower_bound_pi', 'residual_power_of_two_shift')}
        leaf.update(generation=name, input_metadata=h.source(inputpath), payloads=payloads,
            transient_payloads_may_be_deleted_after_successor_commit=True)
        durable_json(pending / 'checkpoint.json', leaf)
        os.replace(pending, SCRATCH / name)
        fault('after_generation', selected)
        self.replace_head({'current': name, 'previous': head['current']}, selected)
        self.observe()
        assert self.verify(name) == leaf
        return leaf


def control():
    store = Store(create=True)
    seed = 'dyadic_weighted_P1600_col00_seed_d124'
    first = 'dyadic_weighted_P1600_col00_step01_d124'
    leaves = [store.commit(seed)]
    interruptions = []
    for point in ('mid_payload', 'after_generation', 'before_head', 'after_head'):
        run = subprocess.run([sys.executable, str(Path(__file__)), '--fault', point],
            capture_output=True, text=True, timeout=40)
        assert run.returncode == 86, (point, run.returncode, run.stdout, run.stderr)
        occupied_at_crash = store.observe()
        head = store.recover()
        expected = 'g000001' if point == 'after_head' else 'g000000'
        assert head['current'] == expected
        interruptions.append({'point': point, 'expected_child_exit_code': 86,
            'resumed_generation': expected, 'scratch_bytes_at_crash': occupied_at_crash})
    # Corrupt only the new scratch copy; verify fallback to its intact predecessor.
    bad = SCRATCH / 'g000001/state.bin'
    with bad.open('r+b') as f:
        firstbyte = f.read(1)
        f.seek(0)
        f.write(bytes([firstbyte[0] ^ 1]))
        f.flush()
        os.fsync(f.fileno())
    assert store.recover() == {'current': 'g000000', 'previous': None}
    for step in range(1, 25):
        leaf = store.commit(f'dyadic_weighted_P1600_col00_step{step:02d}_d124')
        assert leaf['weighted_residual_lower_bound_pi'] == 800 + 33 * step
        leaves.append(leaf)
    head = store.recover()
    last = store.verify(head['current'])
    assert last['active_moment_count'] == 33 and last['weighted_residual_lower_bound_pi'] == 1592
    state = SCRATCH / head['current'] / 'state.bin'
    partial = q.StateReader(h.source(state), 1600, 200, weighted_precision=1600)
    original, _, _ = q.certified_inputs()
    full = q.StateReader(original['state_file'], 1600, 200)
    for e in range(174):
        left, right = partial.row(e), full.row(e)
        for x, y, bits in zip(left, right, partial.bitcounts):
            assert x == tuple(c & ((1 << n) - 1) for c, n in zip(y, bits))
        del left, right
    partial.close()
    full.close()
    durable_json(SCRATCH / 'SEALED.json', {'control_complete': True, 'head': head,
        'all_remaining_files_now_frozen': True})
    retained = store.observe()
    h.PATHS.update(p for p in SCRATCH.rglob('*') if p.is_file())
    return {'checkpoint_replays': 25, 'replayed_checkpoint_records': leaves,
        'expected_process_interruptions': interruptions, 'corrupt_latest_detected_and_rolled_back': True,
        'storage_limit_bytes_including_metadata': CAP, 'per_generation_payload_limit_bytes': MAX_GENERATION_PAYLOAD,
        'maximum_observed_scratch_bytes': store.peak, 'sealed_scratch_bytes': retained,
        'final_weighted_projection_scalar_checks': 2227200,
        'old_frozen_files_modified_or_deleted': False,
        'arithmetic_refinement_integrated': False, 'power_loss_durability_tested': False,
        'history_records_are_not_retained_payload_certificates': True,
        'final_correctness_still_requires_original_residual_and_exact_masses': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fault', choices=('mid_payload', 'after_generation', 'before_head', 'after_head'))
    args = parser.parse_args()
    if args.fault:
        Store().commit('dyadic_weighted_P1600_col00_step01_d124', args.fault)
        raise AssertionError('fault injection did not execute')
    out = DATA / 'dyadic_rolling_scratch_control_d126.json'
    assert not out.exists()
    start = time.monotonic()
    certificates = control()
    h.PATHS.update([Path(__file__), Path(q.__file__), Path(w.__file__), Path(h.__file__),
        Path(q.b.__file__), Path(q.p.__file__), Path(q.p.f.__file__)])
    result = {'status': 'pass', 'milestone': 'D126', 'certificates': certificates,
        'wall_seconds': time.monotonic() - start, 'peak_rss_bytes': w.peak_rss(),
        'actual_moment_precision_increased': False,
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|515_DYADIC_ROLLING_SCRATCH_CONTROL', flush=True)
