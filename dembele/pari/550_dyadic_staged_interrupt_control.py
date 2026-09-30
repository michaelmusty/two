"""D132 abrupt worker interruption inside the capped parent's process group."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
DRIVER=ROOT/'dembele/pari/548_dyadic_resumable_staged_driver.py'
def source(path):
    p=Path(path).resolve();h=hashlib.sha256()
    with p.open('rb') as f:
        while raw:=f.read(1<<20):h.update(raw)
    return {'path':str(p),'sha256':h.hexdigest()}
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ('config','spec','fault','output'):ap.add_argument('--'+key,required=True)
    a=ap.parse_args();spec=json.loads(a.spec);cfg=json.loads((DATA/(a.config+'.json')).read_text())
    stem=cfg['output_prefix']+'_'+spec['key'];out=DATA/(a.output+'.json');assert not out.exists()
    extra=['--config',a.config,'--output',stem,'--fault',a.fault]
    for k,value in spec.items():extra+=['--'+k.replace('_','-'),str(value)]
    tick=time.monotonic();result=subprocess.run(['python3',str(DRIVER)]+extra,cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==73,(result.returncode,result.stdout,result.stderr)
    assert not (DATA/(stem+'.json')).exists(),'fault must precede external completion publication'
    store=DATA/cfg['namespace'];names={p.name for p in store.iterdir()}
    expected='SEALED.json' if spec['phase']=='seal' else 'done_'+spec['key']+'.json' if a.fault=='job_committed' else 'WAL.json' if a.fault=='state_written' else 'TXN.json' if a.fault=='sweep_row_written' else None
    if expected:assert expected in names
    packet={'status':'pass','milestone':'D132','spec':spec,'fault':a.fault,'intentional_child_exit':73,
            'child_inherits_capped_parent_process_group':True,'parent_process_group':os.getpgrp(),
            'external_phase_metadata_absent':True,'durable_boundary_record':expected,
            'wall_seconds':time.monotonic()-tick,'sources':[source(DRIVER),source(Path(__file__)),source(DATA/(a.config+'.json'))]}
    out.write_text(json.dumps(packet,indent=2)+'\n');print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|550_DYADIC_STAGED_INTERRUPT_CONTROL',flush=True)
if __name__=='__main__':main()
