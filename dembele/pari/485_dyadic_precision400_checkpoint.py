"""D122 handoff provenance snapshot; NOT an independent mathematical audit.

Check every inherited D121 hash and all completed D122 receipts, then bind
the completed work. Draft sources 483--484 are intentionally not frozen.
Later artifacts do not change a replay of this particular checkpoint.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_precision400_checkpoint_d122.json'


def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while data:=f.read(1<<20):h.update(data)
    return {'path':str(path),'sha256':h.hexdigest()}


def checked(rows):
    paths=[]
    for row in rows:
        assert source(row['path'])==row,row['path'];paths.append(Path(row['path']))
    return paths


def build():
    priorpath=DATA/'dyadic_schur_review_d121.json';prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==1079
    paths=checked(prior['sources'])+[priorpath,Path(__file__),ROOT/'dembele/pari/run_dyadic_capped.py',
        ROOT/'dembele/certificates/dyadic-precision400-progress-d122.md',DATA/'dyadic_precision400_sources_d122.json']
    jobs=[]
    for path in sorted(DATA.glob('*d122*')):
        if path.name.startswith('dyadic_precision400_checkpoint_d122'):continue
        paths.append(path)
        if path.suffix!='.json':continue
        packet=json.loads(path.read_text())
        paths+=checked([x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        paths+=checked(packet.get('checkpoint_files',[]))
        if path.name.endswith('.job.json'):
            assert packet['status']=='pass' and packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
            paths+=checked([packet['driver'],packet['log']])
            jobs.append({'receipt':path.name,'wall_seconds':packet['wall_seconds'],'status':packet['status']})
    assert len(jobs)==155
    bank=json.loads((DATA/'dyadic_precision400_d122.json').read_text())
    assert bank['full_sixteen_column_bank_refined'] and bank['working_precision_pi']==400
    assert len(bank['state_columns'])==16 and bank['complete_original_residual_scalar_checks']==8908800
    assert bank['coarse_error_beta']==[832,848,832,864]
    assert not (DATA/'dyadic_residue_frame400_d122.json').exists()
    assert not (DATA/'dyadic_integral_quadrics400_d122.json').exists()
    return {'status':'pass','milestone':'D122','checkpoint_kind':'provenance and completion inventory',
        'independent_mathematical_review_complete':False,'D121_source_hashes_checked_unchanged':1079,
        'bounded_input_jobs':jobs,'complete_actual_harmonic_columns':16,'working_precision_pi':400,
        'coarse_error_beta':[832,848,832,864],'CM_frame_error_beta':21168,
        'next_unrun_sources':['dembele/pari/483_dyadic_precision400_residue_frame.py',
            'dembele/pari/484_dyadic_precision400_quadrics.py'],
        'batch_workers_finished':True,'positive_quadric_jet_exact_vanishing_proved':False,
        'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
        'sources':[source(p) for p in sorted(set(x.resolve() for x in paths))]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        result=json.loads(OUT.read_text());checked(result['sources'])
        assert result['status']=='pass' and not result['independent_mathematical_review_complete']
    else:
        assert not OUT.exists();result=build();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs']),
        'independent_mathematical_review_complete':False}),flush=True)
    print('PASS|485_DYADIC_PRECISION400_CHECKPOINT',flush=True)
