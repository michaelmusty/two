"""D130 bounded authentication without whole-payload allocations or repeated hashes.

Build row digests in one streaming pass over the frozen actual P=3200 state.
A separate reader checks every requested row against that bound manifest.
No production file is modified; this is a prospective target-reader control.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
PATHS = {Path(__file__)}
BLOCK = 1 << 20


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    sha = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(BLOCK):
            sha.update(raw)
    return {'path': str(path), 'sha256': sha.hexdigest()}


def read(stem):
    path = DATA / (stem + '.json')
    PATHS.add(path)
    packet = json.loads(path.read_text())
    assert packet['status'] == 'pass'
    return packet, path


def manifest():
    state, statepath = read('dyadic_streamed_P3200_col00_verified_d129')
    review, _ = read('dyadic_precision3200_review_d129')
    expected = [x for x in review['sources'] if Path(x['path']) == statepath]
    assert expected == [source(statepath)] and state['certificate']['original_full_residual_zero']
    record = state['state_file']
    path = Path(record['path'])
    PATHS.add(path)
    row_bytes, states = 3200 * 8 * 50, 174
    assert path.stat().st_size == row_bytes * states
    begin = time.monotonic()
    full = hashlib.sha256()
    rows, largest = [], 0
    with path.open('rb') as f:
        for e in range(states):
            sha, remaining = hashlib.sha256(), row_bytes
            while remaining:
                raw = f.read(min(BLOCK, remaining))
                assert len(raw) == min(BLOCK, remaining)
                full.update(raw)
                sha.update(raw)
                remaining -= len(raw)
                largest = max(largest, len(raw))
            rows.append({'state': e, 'offset': e * row_bytes, 'bytes': row_bytes, 'sha256': sha.hexdigest()})
        assert not f.read(1)
    assert full.hexdigest() == record['sha256']
    legacy = ROOT / 'dembele/pari/459_dyadic_mobius_transform.py'
    text = legacy.read_text()
    assert "hashlib.sha256(p.read_bytes()).hexdigest()" in text
    PATHS.add(legacy)
    return {'actual_state_metadata': source(statepath), 'payload': record,
        'states': states, 'row_bytes': row_bytes, 'rows': rows,
        'all_rows_contiguous_and_full_digest_matches_frozen_payload': True,
        'maximum_hash_read_bytes': largest, 'authenticated_payload_bytes': path.stat().st_size,
        'stream_hash_and_row_manifest_seconds': time.monotonic() - begin,
        'legacy_hash_allocates_whole_payload': True, 'legacy_helper': source(legacy),
        'frozen_payload_modified': False, 'production_reader_replaced': False}


class Rows:
    def __init__(self, manifest):
        self.manifest = manifest
        self.path = Path(manifest['payload']['path'])
        assert manifest['all_rows_contiguous_and_full_digest_matches_frozen_payload']
        assert len(manifest['rows']) == manifest['states']
        assert self.path.stat().st_size == manifest['states'] * manifest['row_bytes']
        for e, row in enumerate(manifest['rows']):
            assert row['state'] == e and row['offset'] == e * manifest['row_bytes']
            assert row['bytes'] == manifest['row_bytes']
        self.file, self.maximum_read = self.path.open('rb'), 0

    def row(self, e):
        assert 0 <= e < self.manifest['states']
        spec = self.manifest['rows'][e]
        self.file.seek(spec['offset'])
        raw = self.file.read(spec['bytes'])
        assert len(raw) == spec['bytes']
        self.maximum_read = max(self.maximum_read, len(raw))
        assert hashlib.sha256(raw).hexdigest() == spec['sha256']
        return raw


def rows(stem):
    packet, path = read(stem)
    assert packet['phase'] == 'manifest'
    cert = packet['certificates']
    begin = time.monotonic()
    reader = Rows(cert)
    for e in range(173, -1, -1):
        raw = reader.row(e)
    reader.file.close()
    elapsed = time.monotonic() - begin
    # Corrupt only a private memory copy; old binaries are never writable.
    corrupted = bytearray(raw)
    corrupted[len(corrupted) // 2] ^= 1
    assert hashlib.sha256(corrupted).hexdigest() != cert['rows'][0]['sha256']
    rejected = 0
    for change in ('offset', 'length', 'state'):
        altered = dict(cert)
        altered['rows'] = [dict(x) for x in cert['rows']]
        key = {'offset': 'offset', 'length': 'bytes', 'state': 'state'}[change]
        altered['rows'][83][key] += 1
        try:
            Rows(altered)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('malformed row manifest accepted')
    return {'manifest_metadata': source(path), 'complete_reverse_order_row_checks': 174,
        'authenticated_row_bytes': 174 * cert['row_bytes'],
        'maximum_row_read_bytes': reader.maximum_read,
        'requested_rows_seconds': elapsed,
        'per_request_full_payload_hashes': 0, 'corrupt_private_row_copy_rejected': True,
        'malformed_row_manifest_rejections': rejected,
        'manifest_must_be_bound_to_a_verified_committed_generation': True,
        'frozen_payload_modified': False, 'production_reader_replaced': False}


def target():
    packet, _ = read('dyadic_compact_target_row_d130')
    cert = packet['certificates']
    record = cert['output_files'][0]
    assert source(record['path']) == record
    path = Path(record['path'])
    row_bytes = 10552 * 8 * 165
    assert path.stat().st_size == row_bytes == cert['uniform_row_bytes']
    # A logical repeated-row stream controls the target length and hashes
    # without creating a 2.4 GB synthetic file. It is not a disk benchmark.
    row = bytearray()
    with path.open('rb') as f:
        while raw := f.read(BLOCK):
            row.extend(raw)
    assert len(row) == row_bytes
    view = memoryview(row)
    sha, length, largest = hashlib.sha256(), 0, 0
    begin = time.monotonic()
    for _ in range(174):
        for first in range(0, row_bytes, BLOCK):
            block = view[first:first + BLOCK]
            sha.update(block)
            length += len(block)
            largest = max(largest, len(block))
    seconds = time.monotonic() - begin
    assert length == 2423583360 and largest <= BLOCK
    return {'input_kind': 'logical_repetition_of_synthetic_target_row',
        'row_payload': record, 'logical_target_uniform_bytes': length,
        'logical_sha256': sha.hexdigest(), 'maximum_hash_block_bytes': largest,
        'retained_synthetic_row_bytes': len(row), 'stream_hash_seconds': seconds,
        'full_target_file_created': False, 'disk_IO_throughput_measured': False,
        'whole_target_payload_materialized': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('manifest', 'rows', 'target'), required=True)
    p.add_argument('--previous')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_-]+', args.output)
    out = DATA / (args.output + '.json')
    assert not out.exists()
    begin = time.monotonic()
    cert = manifest() if args.phase == 'manifest' else rows(args.previous) if args.phase == 'rows' else target()
    result = {'status': 'pass', 'milestone': 'D130', 'phase': args.phase, 'certificates': cert,
        'wall_seconds': time.monotonic() - begin,
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
        'actual_harmonic_precision_increased': False, 'sources': [source(path) for path in sorted(PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|537_DYADIC_STREAMING_AUTHENTICATION_CONTROL', flush=True)
