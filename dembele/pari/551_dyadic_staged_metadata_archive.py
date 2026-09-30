"""D132 retire duplicate durable job records only after immutable receipt binding.

Phase JSON, logs and passing receipts outside the store remain retained.
The archive intent is durable before removal; repeated application checks
the same external copies and completes interrupted removal. Arithmetic
payloads, row manifests, contexts and coarse records are never removed.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('store',ROOT/'dembele/pari/547_dyadic_staged_store.py')
j=importlib.util.module_from_spec(s);s.loader.exec_module(j)
def source(path):
    p=Path(path).resolve();sha=hashlib.sha256()
    with p.open('rb') as f:
        while raw:=f.read(1<<20):sha.update(raw)
    return {'path':str(p),'sha256':sha.hexdigest()}
def archive(config,label):
    cfg=json.loads((DATA/(config+'.json')).read_text());st=j.Store(DATA/cfg['namespace'])
    name='archive_'+label+'.json';tick=time.monotonic()
    with st.guard():
        if st._file(name).exists():packet=st._get(name)
        else:
            items=[]
            for path in sorted(st.path.glob('done_*.json')):
                if path.name.startswith('done_coarse_'):continue
                d=st._get(path.name);key=d['request']['key'];external=DATA/(cfg['output_prefix']+'_'+key+'.json')
                assert external.exists() and json.loads(external.read_text())==d
                receipts=[q for q in DATA.glob(external.stem+'_attempt[0-9][0-9].job.json') if json.loads(q.read_text())['status']=='pass']
                assert len(receipts)==1;receipt=receipts[0];r=json.loads(receipt.read_text())
                assert r['exit_code']==0 and r['driver']==d['driver'] and source(r['driver']['path'])==r['driver']
                assert r['timeout_seconds']==180 and r['timeout_terminates_process_group']
                assert source(r['log']['path'])==r['log']
                bindings=[json.loads(x.split('|',1)[1]) for x in Path(r['log']['path']).read_text().splitlines() if x.startswith('PHASE_METADATA|')]
                assert bindings==[source(external)]
                items.append({'name':path.name,'internal_sha256':source(path)['sha256'],'bytes':path.stat().st_size,
                              'external_metadata':source(external),'passing_receipt':source(receipt)})
            packet={'kind':'duplicate_job_record_archive','items':items,'external_records_remain_frozen':True,
                    'arithmetic_payloads_removed':False,'source':source(Path(__file__))}
            assert len(j.canonical(packet))<=512*(1<<10)
            st._put(name,packet);st._crash('archive_intent')
        for item in packet['items']:
            assert source(item['external_metadata']['path'])==item['external_metadata']
            assert source(item['passing_receipt']['path'])==item['passing_receipt']
            if st._file(item['name']).exists():
                assert source(st._file(item['name']))['sha256']==item['internal_sha256'];st._remove(item['name']);st._crash('archive_record_removed')
    return {'archived_records':len(packet['items']),'duplicate_record_bytes_retired':sum(x['bytes'] for x in packet['items']),
            'archive':source(st.path/name),'external_records_preserved':True,'occupied_bytes':st.occupied(),
            'wall_seconds':time.monotonic()-tick}
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ('config','label','output'):ap.add_argument('--'+key,required=True)
    ap.add_argument('--fault',choices=('archive_intent','archive_record_removed'))
    a=ap.parse_args();out=DATA/(a.output+'.json');assert not out.exists()
    if a.fault:
        original=j.Store._crash
        def crash(st,point):
            if point==a.fault:os._exit(73)
            original(st,point)
        j.Store._crash=crash
    cert=archive(a.config,a.label)
    result={'status':'pass','milestone':'D132','certificates':cert,'sources':[source(Path(__file__)),source(Path(j.__file__)),source(DATA/(a.config+'.json'))]}
    out.write_text(json.dumps(result,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|551_DYADIC_STAGED_METADATA_ARCHIVE',flush=True)
