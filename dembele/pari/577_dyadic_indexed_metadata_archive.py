"""D139 archive: source 551 transaction, with bounded receipt-path lookup.

External phase metadata, logs, receipts and arithmetic payloads are retained.
The 00..99 probes replace only the directory-wide receipt glob. All original
binding, intent-before-removal, replay and store-cap checks remain in place.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'dembele/pari' / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


j = module('store_d139', '547_dyadic_staged_store.py')
lookup = module('lookup_d139', '576_dyadic_receipt_lookup.py')


def source(path):
    path = Path(path).resolve()
    sha = hashlib.sha256()
    with path.open('rb') as stream:
        while raw := stream.read(1 << 20):
            sha.update(raw)
    return {'path': str(path), 'sha256': sha.hexdigest()}


def archive(config, label):
    cfg = json.loads((DATA / (config + '.json')).read_text())
    st = j.Store(DATA / cfg['namespace'])
    name, tick = 'archive_' + label + '.json', time.monotonic()
    with st.guard():
        if st._file(name).exists():
            packet = st._get(name)
        else:
            items = []
            for path in sorted(st.path.glob('done_*.json')):
                if path.name.startswith('done_coarse_'):
                    continue
                d = st._get(path.name)
                external = DATA / (cfg['output_prefix'] + '_' + d['request']['key'] + '.json')
                assert external.exists() and json.loads(external.read_text()) == d
                receipts = [p for p in lookup.exact_receipts(DATA, external.stem)
                            if json.loads(p.read_text())['status'] == 'pass']
                assert len(receipts) == 1
                receipt = receipts[0]
                r = json.loads(receipt.read_text())
                assert r['exit_code'] == 0 and r['driver'] == d['driver']
                assert source(r['driver']['path']) == r['driver']
                assert r['timeout_seconds'] == 180 and r['timeout_terminates_process_group']
                assert source(r['log']['path']) == r['log']
                bindings = [json.loads(x.split('|', 1)[1])
                            for x in Path(r['log']['path']).read_text().splitlines()
                            if x.startswith('PHASE_METADATA|')]
                assert bindings == [source(external)]
                items.append({'name': path.name, 'internal_sha256': source(path)['sha256'],
                              'bytes': path.stat().st_size, 'external_metadata': source(external),
                              'passing_receipt': source(receipt)})
            packet = {'kind': 'duplicate_job_record_archive', 'items': items,
                      'external_records_remain_frozen': True, 'arithmetic_payloads_removed': False,
                      'source': source(Path(__file__))}
            assert len(j.canonical(packet)) <= 512 * (1 << 10)
            st._put(name, packet)
            st._crash('archive_intent')
        for item in packet['items']:
            assert source(item['external_metadata']['path']) == item['external_metadata']
            assert source(item['passing_receipt']['path']) == item['passing_receipt']
            if st._file(item['name']).exists():
                assert source(st._file(item['name']))['sha256'] == item['internal_sha256']
                st._remove(item['name'])
                st._crash('archive_record_removed')
    return {'archived_records': len(packet['items']),
            'duplicate_record_bytes_retired': sum(x['bytes'] for x in packet['items']),
            'archive': source(st.path / name), 'external_records_preserved': True,
            'occupied_bytes': st.occupied(), 'wall_seconds': time.monotonic() - tick}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ('config', 'label', 'output'):
        ap.add_argument('--' + key, required=True)
    ap.add_argument('--fault', choices=('archive_intent', 'archive_record_removed'))
    args = ap.parse_args()
    out = DATA / (args.output + '.json')
    assert not out.exists()
    if args.fault:
        original = j.Store._crash
        def crash(st, point):
            if point == args.fault:
                os._exit(73)
            original(st, point)
        j.Store._crash = crash
    cert = archive(args.config, args.label)
    packet = {'status': 'pass', 'milestone': 'D139', 'certificates': cert,
              'sources': [source(Path(__file__)), source(Path(j.__file__)),
                          source(Path(lookup.__file__)), source(DATA / (args.config + '.json'))]}
    out.write_text(json.dumps(packet, indent=2) + '\n')
    print('PHASE_METADATA|' + json.dumps(source(out)), flush=True)
    print('PASS|577_DYADIC_INDEXED_METADATA_ARCHIVE', flush=True)
