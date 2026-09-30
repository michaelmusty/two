"""D123 bounded shrinking-correction control, resumable from fixed receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
DRIVER='dembele/pari/493_dyadic_shrinking_schur.py';WRAPPER='dembele/pari/run_dyadic_capped.py'


def source(path):
    path=Path(path).resolve();sha=hashlib.sha256()
    with path.open('rb') as file:
        while block:=file.read(1<<20):sha.update(block)
    return {'path':str(path),'sha256':sha.hexdigest()}


def main():
    start=time.monotonic();summary=DATA/'dyadic_shrinking_pilot_d123.json';assert not summary.exists()
    receipts=[];stems=[]
    def job(phase,stem,previous=None):
        receipt=DATA/(stem+'_attempt01.job.json');log=DATA/(stem+'_attempt01.log');output=DATA/(stem+'.json')
        if not receipt.exists():
            assert not log.exists() and not output.exists(),('inspect partial output before restarting',stem)
            cmd=['python3',WRAPPER,DRIVER,stem+'_attempt01','PASS|493_DYADIC_SHRINKING_SCHUR',
                '--phase',phase,'--output',stem]
            if previous:cmd+=['--previous',previous]
            run=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
            if run.returncode:print(run.stdout+run.stderr,flush=True);raise RuntimeError(stem)
        row=json.loads(receipt.read_text());assert row['status']=='pass' and row['exit_code']==0
        assert row['timeout_seconds']==180 and row['timeout_terminates_process_group']
        assert source(row['driver']['path'])==row['driver'] and source(row['log']['path'])==row['log']
        packet=json.loads(output.read_text());assert packet['status']=='pass' and packet['phase']==phase
        receipts.append(receipt);stems.append(stem)
        print('SHRINKING_JOB|'+json.dumps({'stem':stem,'seconds':row['wall_seconds'],
            'active_moments':packet.get('active_moment_count'),'step':packet['correction_steps']}),flush=True)
        return packet
    previous='dyadic_shrinking_P800_col00_seed_d123';packet=job('init',previous)
    step=0
    while packet['active_moment_count']>33:
        step+=1;assert step<=12
        stem=f'dyadic_shrinking_P800_col00_step{step:02d}_d123';packet=job('step',stem,previous);previous=stem
    final='dyadic_shrinking_P800_col00_verified_d123';packet=job('finish',final,previous)
    assert packet['full_precision_reconstruction_equals_verified_column']
    jobs=[json.loads(path.read_text()) for path in receipts]
    state_bytes=sum(Path(x['path']).stat().st_size for stem in stems
        for x in json.loads((DATA/(stem+'.json')).read_text())['checkpoint_files'])
    result={'status':'pass','milestone':'D123','working_precision_pi':800,'harmonic_basis_column':0,
        'completed_phases':len(jobs),'correction_steps':step,'correction_history':packet['correction_history'],
        'sum_recorded_phase_seconds':sum(x['wall_seconds'] for x in jobs),
        'maximum_phase_seconds':max(x['wall_seconds'] for x in jobs),
        'coordinator_wall_seconds':time.monotonic()-start,'checkpoint_payload_bytes':state_bytes,
        'correction_stage_uses_existing_uniform_seed':True,'all_intermediate_weighted_baseline_overlaps_checked':True,
        'full_original_reconstruction_equals_verified_P800_column':True,
        'verified_checkpoint':source(DATA/(final+'.json')),
        'full_sixteen_column_bank_precision_pi':400,'complete_target_size_solve_costed':False,
        'sources':[source(path) for path in [Path(__file__),ROOT/DRIVER,ROOT/WRAPPER,*receipts]]}
    summary.write_text(json.dumps(result,indent=2)+'\n')
    print('SHRINKING_COMPLETE|'+json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)


if __name__=='__main__':main()
