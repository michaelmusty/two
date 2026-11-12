"""D138 capped, incremental provenance replay of one frozen input catalogue.

The immutable catalogue hash binds its full file list. Do not duplicate the
inherited lists in each result; the final review authenticates all 15 roots.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while raw:=f.read(1<<20):h.update(raw)
    return {'path':str(path),'sha256':h.hexdigest()}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--index',type=int,required=True);p.add_argument('--output',required=True);a=p.parse_args()
    assert __debug__ and 0<=a.index<=14
    tick=time.monotonic();out=DATA/(a.output+'.json');assert not out.exists()
    parent=DATA/'dyadic_checkpoint_admission_r2_d137.json'
    root=parent if a.index==0 else DATA/f'dyadic_checkpoint_col{a.index+1:02d}_review_r2_d137.json'
    packet=json.loads(root.read_text());assert packet['status']=='pass' and packet['independent_finite_review_complete']
    if a.index==0:assert packet['P1600_checkpoint_admitted'] and len(packet['sources'])==94126
    else:
        assert packet['working_precision_pi']==1600 and packet['harmonic_basis_column']==a.index+1
        assert packet['incremental_provenance'] and packet['prior_fixed_review']==source(parent)
        assert packet['failed_bounded_input_jobs']==0 and packet['passing_input_jobs']==6637
    rows=packet['sources'];assert len({r['path'] for r in rows})==len(rows)
    for row in rows:assert source(row['path'])==row,row['path']
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<=2*(1<<30)
    result={'status':'pass','milestone':'D138','kind':'incremental_manifest_replay','index':a.index,
            'catalogue_root':source(root),'catalogue_sources_rehashed':len(rows),'all_catalogue_hashes_match':True,
            'prior_admission':source(parent),'full_source_list_bound_by_catalogue_root':True,
            'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak,
            'sources':[source(Path(__file__)),source(root),source(parent)]}
    with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|574_DYADIC_CHECKPOINT_MANIFEST_RECHECK',flush=True)

if __name__=='__main__':main()
