"""D139 bounded discovery equivalence, archive replay and interruption controls.

Completed arithmetic stores are read-only. Archive transactions run only in
new synthetic stores containing copies of already certified job records.
Intentional exit-73 children inherit this job's capped process group.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import resource
import statistics
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'dembele/pari' / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


a = module('archive_control_d139', '577_dyadic_indexed_metadata_archive.py')
q = a.lookup
PATHS = {Path(__file__), Path(a.__file__), Path(q.__file__), Path(a.j.__file__)}


def source(path):
    PATHS.add(Path(path).resolve())
    return a.source(path)


def reject(fn):
    try:
        fn()
    except (AssertionError, FileNotFoundError, json.JSONDecodeError):
        return True
    raise AssertionError('invalid control was accepted')


def lookup_controls():
    fixture = DATA / 'dyadic_receipt_fixture_d139'
    fixture.mkdir()
    def put(name, value):
        (fixture / name).write_text(json.dumps(value))
    prefix = 'd139_control'
    # The full old matching language includes 00 and 99, and arbitrary log suffixes.
    for suffix, status in [('00', 'pass'), ('99', 'pass'), ('05', 'fail'), ('1', 'pass'), ('100', 'pass')]:
        put(prefix + '_multiple_attempt' + suffix + '.job.json', {'status': status})
    for suffix in ('', 'ab', '00_extra_attempt07', '1', '100'):
        put(prefix + '_partial_attempt' + suffix + '.log', {})
    put(prefix + '_failed_attempt01.job.json', {'status': 'fail'})
    for number in ('00', '99'):
        put(prefix + '_duplicate_attempt' + number + '.job.json', {'status': 'pass'})
    put(prefix + '_orphan.json', {})
    put(prefix + '_passed_attempt00.job.json', {'status': 'pass'})
    put(prefix + '_passed_attempt00.log', {})
    (fixture / (prefix + '_broken_attempt01.job.json')).symlink_to('missing-target')
    idx = q.ReceiptInventory(fixture, prefix)
    stems = [prefix + '_' + x for x in ('multiple', 'duplicate', 'partial', 'failed', 'orphan', 'passed', 'fresh', 'broken')]
    for stem in stems:
        receipts = sorted(fixture.glob(stem + '_attempt[0-9][0-9].job.json'))
        logs = sorted(fixture.glob(stem + '_attempt*.log'))
        assert q.exact_receipts(fixture, stem) == receipts
        assert idx.lookup(stem) == (receipts, logs)
    for name in ('multiple', 'duplicate', 'partial', 'failed', 'orphan', 'broken'):
        reject(lambda name=name: idx.preflight(prefix + '_' + name))
    assert len(idx.preflight(prefix + '_passed')) == 1
    assert idx.preflight(prefix + '_fresh') == []
    put(prefix + '_fresh_attempt01.job.json', {'status': 'pass'})
    put(prefix + '_fresh_attempt01.log', {})
    reject(idx.reconcile)
    idx.register(prefix + '_fresh', 1)
    assert len(idx.preflight(prefix + '_fresh')) == 1
    idx.reconcile()
    # A passing and a failed receipt must still be rejected by the coordinator.
    put(prefix + '_passed_attempt01.job.json', {'status': 'fail'})
    resumed = q.ReceiptInventory(fixture, prefix)
    reject(lambda: resumed.preflight(prefix + '_passed'))
    for path in fixture.iterdir():
        if not path.is_symlink():
            source(path)

    prior = json.loads((DATA / 'dyadic_precision1600_review_d138.json').read_text())
    source(DATA / 'dyadic_precision1600_review_d138.json')
    known = {r['path']: r['sha256'] for r in prior['sources']}
    actual = []
    for col in (2, 15):
        prefix = f'dyadic_staged_P1600_col{col:02d}_r2_d137'
        summary_path = DATA / (prefix + '_completed.json')
        bound = source(summary_path)
        assert known[bound['path']] == bound['sha256']
        completed = json.loads(summary_path.read_text())
        tick = time.monotonic()
        index = q.ReceiptInventory(DATA, prefix)
        scan_seconds = time.monotonic() - tick
        tick = time.monotonic()
        for row in completed['jobs']:
            stem = Path(row['metadata']['path']).stem
            assert index.preflight(stem) == [Path(row['receipt']['path'])]
            assert a.source(row['receipt']['path']) == row['receipt']
        all_seconds = time.monotonic() - tick
        legacy_times, exact_times = [], []
        for row in [completed['jobs'][i] for i in (0, 1, 3294, -1)]:
            stem = Path(row['metadata']['path']).stem
            tick = time.monotonic()
            old = sorted(DATA.glob(stem + '_attempt[0-9][0-9].job.json'))
            legacy_times.append(time.monotonic() - tick)
            tick = time.monotonic()
            new = q.exact_receipts(DATA, stem)
            exact_times.append(time.monotonic() - tick)
            assert old == new == index.lookup(stem)[0]
        index.reconcile()
        actual.append({'column': col, 'all_production_receipts_checked': len(completed['jobs']),
                       'directory_entries': index.entries_scanned, 'one_scan_seconds': scan_seconds,
                       'all_preflights_and_receipt_rehashes_seconds': all_seconds,
                       'legacy_sample_seconds': legacy_times, 'exact_sample_seconds': exact_times,
                       'median_legacy_lookup_seconds': statistics.median(legacy_times),
                       'median_exact_lookup_seconds': statistics.median(exact_times)})
    return {'synthetic_stem_cases': len(stems), 'old_glob_matches_preserved': True,
            'failure_partial_duplicate_and_resume_controls_pass': True,
            'snapshot_requires_exclusive_prefix_ownership_and_final_reconciliation': True,
            'completed_column_checks': actual, 'actual_receipts_checked': 13176}


def archive_controls():
    original_path = DATA / 'dyadic_rowjournal_P1600_col15_r2_d132/archive_sweep_finish_000.json'
    original = json.loads(original_path.read_text())
    assert a.j.digest(a.j.canonical(original['value'])) == original['sha256']
    old = original['value']
    source(original_path)
    assert len(old['items']) == 422
    results = []
    for mode in ('complete', 'archive_intent', 'archive_record_removed'):
        namespace = f'dyadic_rowjournal_archive_control_{mode}_d139_d132'
        st = a.j.Store(DATA / namespace, create=True)
        config = f'dyadic_archive_control_{mode}_config_d139'
        cfg_path = DATA / (config + '.json')
        assert not cfg_path.exists()
        cfg_path.write_text(json.dumps({'namespace': namespace,
                                       'output_prefix': 'dyadic_staged_P1600_col15_r2_d137'}) + '\n')
        source(cfg_path)
        selected = old['items'] if mode == 'complete' else old['items'][:3]
        for item in selected:
            assert a.source(item['external_metadata']['path']) == item['external_metadata']
            packet = json.loads(Path(item['external_metadata']['path']).read_text())
            st._put(item['name'], packet)
            assert a.source(st.path / item['name'])['sha256'] == item['internal_sha256']
        st._put('done_coarse_sentinel.json', {'synthetic': True})
        (st.path / 'payload_sentinel.bin').write_bytes(b'D139 preserve arithmetic payloads\0' * 64)
        preserved = [a.source(st.path / n) for n in ('done_coarse_sentinel.json', 'payload_sentinel.bin', 'WORKSPACE.bin')]
        if mode != 'complete':
            child = subprocess.run(['python3', str(Path(a.__file__)), '--config', config,
                                    '--label', 'control', '--output', config + '_interrupted', '--fault', mode],
                                   cwd=ROOT, capture_output=True, text=True)
            assert child.returncode == 73, (child.returncode, child.stdout, child.stderr)
            assert not (DATA / (config + '_interrupted.json')).exists()
            remaining = sum((st.path / x['name']).exists() for x in selected)
            assert remaining == (3 if mode == 'archive_intent' else 2)
        else:
            remaining = len(selected)
        cert = a.archive(config, 'control')
        packet = st._get('archive_control.json')
        assert packet['items'] == selected
        assert packet['source'] == a.source(Path(a.__file__))
        assert cert['archived_records'] == len(selected)
        assert cert['duplicate_record_bytes_retired'] == sum(x['bytes'] for x in selected)
        assert not any((st.path / x['name']).exists() for x in selected)
        replay = a.archive(config, 'control')
        assert replay['archive'] == cert['archive']
        for ref in preserved:
            assert a.source(ref['path']) == ref
        # Seal synthetic fixtures against accidental future reuse.
        st._put('SEALED.json', {'synthetic_archive_control_only': True, 'mode': mode})
        reject(lambda: a.archive(config, 'control'))
        for path in st.path.iterdir():
            if path.name != '.lock':
                source(path)
        results.append({'mode': mode, 'copied_records': len(selected),
                        'remaining_at_interruption': remaining, 'archive': cert,
                        'repeat_seconds': replay['wall_seconds'], 'sentinels_preserved': preserved,
                        'intentional_exit': None if mode == 'complete' else 73})
    assert a.source(original_path) == source(original_path)
    return {'complete_archive_matches_all_422_original_items': True,
            'both_interruption_points_resume_idempotently': True,
            'old_sealed_store_never_mutated': True, 'synthetic_stores': results}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase', choices=('lookup', 'archive'), required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    tick = time.monotonic()
    cert = lookup_controls() if args.phase == 'lookup' else archive_controls()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    child_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform != 'darwin':
        rss *= 1024
        child_rss *= 1024
    assert rss + child_rss < 2 * (1 << 30)
    result = {'status': 'pass', 'milestone': 'D139', 'phase': args.phase, 'certificates': cert,
              'actual_harmonic_precision_increased': False, 'higher_precision_bank_admitted': False,
              'wall_seconds': time.monotonic() - tick, 'peak_rss_bytes': rss,
              'child_peak_rss_bytes': child_rss, 'sources': [a.source(p) for p in sorted(PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(a.source(out)), flush=True)
    print('PASS|578_DYADIC_RECEIPT_LOOKUP_CONTROLS', flush=True)
